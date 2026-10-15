#!/usr/bin/env python3
"""Explicit retail refresh into data/prices.json; ./fetch-prices.sh also attempts official monthly sources.

  US: USDA AMS weekly grocery-store beef ad report (PDF, needs `pdftotext` from poppler: brew install poppler).
      Advertised prices, store-weighted across conventional fresh items; not shelf-price averages.
  AR: Carrefour Argentina public catalog search (butcher-section items sold by the kg), median per cut.
      IPCVA AMBA is the primary monthly source for covered cuts; Carrefour evidence is retained.
  FX rule: INDEC uses the BCRA-derived valuation series' monthly average.
      IPCVA uses the monthly arithmetic mean of BCRA's published USD quotes.
      Carrefour records use the latest returned BCRA observation, which can lag. Each AR record stores fx_ars_per_usd,
      fx_date, and fx_basis so the page can display provenance without mixing bases.
"""
import argparse, os, math, json, re, statistics, subprocess, sys, tempfile, time, unicodedata, urllib.parse, urllib.request, hashlib
from http.client import HTTPException
from urllib.error import HTTPError
from html.parser import HTMLParser
from datetime import datetime, timedelta, timezone
from pathlib import Path
from price_contract import positive, valid_period, qualify_snapshot, validate_snapshot, merge_records, write_snapshot, timestamp, enable_ar_sources, source_records, select_ar_sources
from official_prices import fetch_official, merge_official
from ipcva_prices import refresh_ipcva

OUT = Path(os.environ.get("BEEF_PRICES_OUT", Path(__file__).parent / "data" / "prices.json"))
USDA_PDF = "https://www.ams.usda.gov/mnreports/AMS_3228.pdf"
USDA_REPORT_PAGE = "https://mymarketnews.ams.usda.gov/viewReport/3228"
USDA_END_WINDOW = 'advertisement_ending_dates_printed_in_pdf'
FX_URL = "https://apis.datos.gob.ar/series/api/series/?ids=92.2_TIPO_CAMBIION_0_0_21_24&last=1&format=json"
LB_PER_KG = 2.2046226
RETAIL_ERRORS = (OSError, ValueError, KeyError, IndexError, TypeError, OverflowError, HTTPException)


class PartialRefreshError(RuntimeError):
    """Expected incomplete provider work after a validated snapshot was saved."""
    def __init__(self, issues):
        self.issues = list(issues)
        super().__init__('Partial refresh: ' + ', '.join(self.issues))


class USDARequestError(OSError):
    def __init__(self, step, cause):
        self.step = step
        self.cause_type = type(cause).__name__
        super().__init__(f'{step}: {self.cause_type}: {cause}')


class USDAMissingInterval(ValueError):
    pass


def print_refresh_summary(data, issues, attempted_at):
    print(f"Stored snapshot; {len(issues)} source issues, retained observations keep their original dates")
    for source, state in data['source_status'].items():
        if state.get('attempted_at') != attempted_at:
            continue
        details = [state['status']]
        coverage = state.get('coverage', {})
        if coverage:
            accepted = sum(value in ('ok', 'observed', 'reference_only', 'unverified_layout') for value in coverage.values())
            failed = sum(value == 'error' for value in coverage.values())
            details.append(f'{accepted}/{len(coverage)} observations accepted')
            if failed:
                details.append(f'{failed} failed')
        if source == 'IPCVA':
            records = data.get('ar_sources', {}).get('IPCVA', {})
            periods = sorted({record['period'] for record in records.values()})
            if periods:
                details.append('stored price month ' + ', '.join(periods))
        if source == 'FX monthly' and data['fx'].get('period'):
            details.append('stored FX month ' + data['fx']['period'])
        if source == 'FX daily' and data['fx'].get('latest', {}).get('date'):
            details.append('stored FX date ' + data['fx']['latest']['date'])
        if source == 'IPCVA FX':
            for period, evidence in sorted(state.get('monthly_rates', {}).items()):
                details.append(f"{period}: {evidence['ars_per_usd']:.6f} ARS/USD from {evidence['quote_count']} published quotes")
        if state.get('note'):
            details.append(state['note'])
        elif state.get('error_type'):
            details.append(state['error_type'])
        print(f"  {source}: " + '; '.join(details))
    if data.get('carrefour_originals'):
        print(f"  Original Carrefour archive: {len(data['carrefour_originals'])} observations preserved")


def error_detail(error):
    """Return a short diagnostic without exposing response bodies or request URLs."""
    if isinstance(error, HTTPError):
        detail = f'HTTP {error.code} {error.reason}'
    else:
        detail = f'{type(error).__name__}: {error}'
    return ' '.join(detail.split())[:200]


# not plain beef cuts, or premium/branded lines that would skew a "typical" price
SKIP = re.compile(r"cerdo|pollo|cordero|guanaco|congel|milanesa|etiqueta negra|huella natural|cabana|holis|premium")

# key: (label, report item prefix)
US_ITEMS = {
    "ribeye_bnls": ("Ribeye steak, boneless", "Ribeye Steak, Boneless,"),
    "strip_bnls": ("Strip steak, boneless", "Strip Steak, Boneless,"),
    "tenderloin": ("Tenderloin", "Tenderloin,"),
    "brisket_whole": ("Brisket, whole", "Brisket, Whole,"),
    "chuck_roast": ("Chuck roast, boneless", "Chuck Roast, Boneless,"),
    "short_ribs": ("Short ribs", "Short Ribs,"),
    "skirt": ("Skirt steak", "Skirt Steak,"),
    "flank": ("Flank steak", "Flank Steak,"),
    "tri_tip": ("Tri-tip", "Tri-Tip"),
    "eye_round": ("Eye of round roast", "Eye of Round Roast,"),
    "bottom_round": ("Bottom round roast", "Bottom Round Roast,"),
}

# key: (label, search words that must all appear in the product name)
AR_ITEMS = {
    "bife_costilla": ("Bife de costilla (bone-in)", "bife de costilla"),
    "molleja": ("Molleja (sweetbreads; organ unspecified by retailer)", "molleja"),
    "rinon": ("Riñón", "rinon"),
    "lengua": ("Lengua", "lengua"),
    "bife_ancho": ("Bife ancho", "bife ancho"),
    "bife_angosto": ("Bife de chorizo", "bife de chorizo"),
    "lomo": ("Lomo", "lomo"),
    "vacio": ("Vacío", "vacio"),
    "entrana": ("Entraña", "entrana"),
    "matambre": ("Matambre", "matambre"),
    "tapa": ("Tapa de cuadril", "tapa de cuadril"),
    "colita": ("Colita de cuadril", "colita de cuadril"),
    "peceto": ("Peceto", "peceto"),
    "osobuco": ("Osobuco", "osobuco"),
    "pecho": ("Pecho", "pecho"),
    "aguja": ("Aguja", "aguja"),
    "cuadrada": ("Cuadrada", "cuadrada"),
}


# Keep bone-in steak separate from boneless strip and T-bone. Generic molleja
# listings do not prove thymus; retain the retailer's wording in provenance.
NEW_AR_KEYS = {"bife_costilla", "molleja", "rinon", "lengua"}
AR_ALIASES = {
    "bife_costilla": ("bife de costilla", "bife angosto con hueso"),
    "molleja": ("molleja", "mollejas"),
    "rinon": ("rinon", "rinones"),
    "lengua": ("lengua",),
}
EXCLUDE_NEW = re.compile(r"cerdo|porcin|pollo|aviar|cordero|ovin|caprin|lenguado|vinagreta|cocid|escabeche|pancreas|con lomo|t[ -]?bone|sin hueso")


def catalog_matches(products, key, words):
    """Uniform conservative unit/species/form rules for all catalog keys."""
    listed = []
    aliases = AR_ALIASES.get(key, (unaccent(words),))
    excluded = re.compile(r"cerdo|porcin|pollo|aviar|cordero|ovin|caprin|cabra|conejo|rabbit|pavo|pescad|lenguado|vinagreta|cocid|cocinad|escabeche|preparad|empanad|marinad|rebozad|ahumad|curad|salam|vegetal|soja|pancreas")
    for product in products:
        if not isinstance(product, dict):
            raise ValueError('Catalog product must be an object')
        name = unaccent(str(product.get("productName", "")))
        if not any(re.match(re.escape(alias) + r"\b", name) for alias in aliases):
            continue
        if product.get("EC_Sección") != ["CARNICERIA"] or SKIP.search(name) or excluded.search(name):
            continue
        # Require structured species evidence; counter location/name alone does not prove beef.
        species = unaccent(" ".join(str(product.get(k, "")) for k in ("Especie", "Tipo de carne", "Categoría", "categoryName")) + " " + name)
        if excluded.search(species) or not re.search(r"\b(?:vacun[ao]|bovin[ao]|novillito|novillo|ternera|ternero|beef)\b", species):
            continue
        form = unaccent(" ".join(str(product.get(k, "")) for k in ("product_form", "Preparación", "Estado")))
        if excluded.search(form) or not re.search(r"\b(?:raw|crud[ao])\b", form + " " + name):
            continue
        if key == "bife_costilla" and re.search(r"con lomo|t[ -]?bone|sin hueso", name):
            continue
        if not re.search(r"(?:x|por)\s*(?:1\s*)?kg\b", name):
            continue
        items = product.get("items", [])
        if not isinstance(items, list):
            raise ValueError('Catalog items must be a list')
        for item in items:
            if not isinstance(item, dict):
                raise ValueError('Catalog item must be an object')
            if item.get("measurementUnit") != "kg" or (item.get("unitMultiplier") != 1 or isinstance(item.get("unitMultiplier"), bool)):
                continue
            sellers = item.get("sellers", [])
            if not isinstance(sellers, list):
                raise ValueError('Catalog sellers must be a list')
            for seller in sellers[:1]:
                if not isinstance(seller, dict):
                    raise ValueError('Catalog seller must be an object')
                offer = seller.get("commertialOffer", {})
                if not isinstance(offer, dict):
                    raise ValueError('Catalog offer must be an object')
                price = offer.get("Price")
                if not positive(price):
                    continue
                listed.append({"ars_kg":price, "available":offer.get("IsAvailable") is True,
                               "product_id":product.get("productId"), "sku_id":item.get("itemId"),
                               "name":product.get("productName"), "url":product.get("link"),
                               "measurement_unit":"kg", "unit_multiplier":1, "species":"bovine", "product_form":"raw",
                               "species_evidence":species, "form_evidence":form, "seller_id":seller.get("sellerId")})
    return listed


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; beef-chart price snapshot)"})
    with urllib.request.urlopen(req, timeout=20) as response:
        return response.read()


def unaccent(s):
    return "".join(c for c in unicodedata.normalize("NFD", s.lower()) if unicodedata.category(c) != "Mn")


def usda_rows(text):
    """Yield (item, [cw_stores, cw_avg, pw_stores, pw_avg, py_stores, py_avg]) for conventional fresh rows."""
    cols = item_col = None
    for line in text.splitlines():
        if re.match(r'^[A-Z][A-Z -]+ REGION\b', line.strip()):
            break  # Regional price-range tables have a different column layout.
        if "Item" in line and "Environment" in line:
            item_col = line.index("Item")
        if "Stores" in line and "Wtd Avg" in line:
            found = [m.end() for m in re.finditer(r"Stores|Wtd Avg", line)]
            cols = found if len(found) == 6 else None
            continue
        m = re.search(r"Conventional\s+Fresh", line)
        if not (m and cols and item_col is not None):
            continue
        item = line[item_col:m.start()].strip()
        vals = [None] * 6
        for t in re.finditer(r"\d[\d,]*(?:\.\d\d)?", line[m.end():]):
            end = m.end() + t.end()
            i = min(range(6), key=lambda j: abs(cols[j] - end))
            if abs(cols[i] - end) <= 5:
                if vals[i] is not None:
                    raise ValueError('USDA numeric columns collide; layout unresolved')
                vals[i] = float(t.group().replace(",", ""))
        yield item, vals


class VisibleText(HTMLParser):
    """Collect visible text from an HTML source page without external dependencies."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []

    def handle_data(self, data):
        self.parts.append(data)

    def text(self):
        return " ".join(self.parts)


def usda_intervals(text, release_listing=None):
    """Resolve CW/PW from explicit PDF headings or USDA landing-page release ranges."""
    ranges = {}
    pattern = r"(This Week|Current Week|Prior Week|Previous Week)\s*:?\s*(\d{2}/\d{2}/\d{4})\s*(?:-|to)\s*(\d{2}/\d{2}/\d{4})"
    for label, start, end in re.findall(pattern, text, re.I):
        begin = datetime.strptime(start, '%m/%d/%Y').strftime('%Y-%m-%d')
        finish = datetime.strptime(end, '%m/%d/%Y').strftime('%Y-%m-%d')
        if begin > finish:
            raise ValueError('Reversed USDA feature interval')
        ranges['prior' if label.lower().startswith(('prior', 'previous')) else 'current'] = (begin, finish)

    # This report prints a window for advertisement ENDING dates, which is not
    # a guarantee that each offer is valid throughout the complete window.
    printed = re.search(r'Advertised Prices for Beef Products at Major Grocery Store Outlets\s+ending during the period of\s+(\d{1,2}/\d{1,2}/\d{4})\s+to\s+(\d{1,2}/\d{1,2}/\d{4})', text.split('\f', 1)[0], re.I)
    if 'current' not in ranges and printed:
        begin, finish = (datetime.strptime(value, '%m/%d/%Y').strftime('%Y-%m-%d') for value in printed.groups())
        if begin > finish:
            raise ValueError('Reversed USDA advertisement ending window')
        ranges.update(current=(begin, finish), current_basis=USDA_END_WINDOW)

    listing_ranges = []
    if release_listing and ranges.get('current_basis') != USDA_END_WINDOW:
        date_pattern = r"(?<!\d)(\d{1,2}/\d{1,2}/\d{4})\s*(?:-|\u2013|to)\s*(\d{1,2}/\d{1,2}/\d{4})(?!\d)"
        for start, end in re.findall(date_pattern, release_listing, re.I):
            begin = datetime.strptime(start, '%m/%d/%Y').strftime('%Y-%m-%d')
            finish = datetime.strptime(end, '%m/%d/%Y').strftime('%Y-%m-%d')
            if begin > finish:
                raise ValueError('Reversed USDA release interval')
            interval = (begin, finish)
            if interval not in listing_ranges:
                listing_ranges.append(interval)
        listing_ranges.sort(key=lambda interval: interval[1], reverse=True)

    # The current USDA PDF uses CW/PW/PY table labels and omits their dates.
    # The official report landing page publishes the corresponding explicit
    # release windows. If it exposes only the current release, omit PW dates.
    if 'current' not in ranges and listing_ranges:
        ranges['current'] = listing_ranges[0]
    if 'current' in ranges and 'prior' not in ranges:
        earlier = [interval for interval in listing_ranges if interval[1] < ranges['current'][0]]
        if earlier:
            ranges['prior'] = earlier[0]
    if 'current' not in ranges:
        raise USDAMissingInterval('USDA adapter unresolved: explicit current feature interval not recognized; retain old evidence')
    if 'prior' in ranges and ranges['prior'][1] >= ranges['current'][0]:
        raise ValueError('Overlapping USDA feature intervals')
    return ranges


def get_usda_resource(url, step):
    try:
        return get(url)
    except (OSError, HTTPException) as error:
        raise USDARequestError(step, error) from error


def usda_prices():
    pdf = get_usda_resource(USDA_PDF, 'PDF download')
    with tempfile.NamedTemporaryFile(suffix=".pdf") as f:
        f.write(pdf); f.flush()
        text = subprocess.run(["pdftotext", "-layout", f.name, "-"], capture_output=True, text=True, check=True, timeout=20).stdout
    d = re.search(r"(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun) (\w{3}) (\d+), (\d{4})", text)
    if not d:
        raise ValueError('USDA report publication date missing')
    publication = datetime.strptime(" ".join(d.groups()), "%b %d %Y").strftime("%Y-%m-%d")
    try:
        intervals = usda_intervals(text)
    except USDAMissingInterval:
        listing = VisibleText()
        listing.feed(get_usda_resource(USDA_REPORT_PAGE, 'Release-date page').decode('utf-8', errors='replace'))
        intervals = usda_intervals(text, listing.text())
    rows = list(usda_rows(text))
    printed_window = intervals.get('current_basis') == USDA_END_WINDOW
    if printed_window:
        if not re.search(r'(?m)^\s*NATIONAL\s*$', text) or not re.search(r'\bCW\s+CW\s+PW\s+PW\s+PY\s+PY\b', text):
            raise ValueError('USDA national CW/PW/PY table not recognized')
        for _, values in rows:
            for si, ai in ((0, 1), (2, 3), (4, 5)):
                if (values[si] is None) != (values[ai] is None) or (values[si] is not None and (not positive(values[si]) or not values[si].is_integer() or not positive(values[ai]))):
                    raise ValueError('USDA national store/price pair incomplete or invalid')
    def wavg(prefix, si, ai):
        pts = [(v[si], v[ai]) for item, v in rows if item.startswith(prefix) and "Lbs" not in item and positive(v[si]) and positive(v[ai])]
        n = sum(s for s, _ in pts)
        return (sum(s * a for s, a in pts) / n, n) if n else (None, 0)
    out = {}
    for key, (label, prefix) in US_ITEMS.items():
        cur, n = wavg(prefix, 0, 1)
        prev, pn = wavg(prefix, 2, 3)
        fallback = cur is None and 'prior' in intervals
        if fallback:
            cur, n = prev, pn
        if cur is None:
            continue
        start, end = intervals['prior' if fallback else 'current']
        prior_value = round(prev,2) if prev and not fallback and 'prior' in intervals else None
        out[key] = {"label":label, "usd_lb":round(cur,2), "prev_usd_lb":prior_value,
                    "prev_period":intervals['prior'][1] if prior_value is not None else None,
                    "period":end, "effective_start":start, "effective_end":end, "publication_date":publication,
                    "fallback_reason":"not_advertised_current_interval" if fallback else None,
                    "stores":int(n), "source":"USDA ad survey", "adapter_status":"unresolved_real_layout",
                    "provenance_status":"parsed_unverified", "observation_status":"unverified_layout"}
        out[key]['source_receipt'] = {'url':USDA_PDF, 'sha256':hashlib.sha256(pdf).hexdigest()}
        if printed_window:
            out[key].update(interval_basis=USDA_END_WINDOW, adapter_status='unknown', observation_status='observed',
                            method='Store-count-weighted national advertised features', geography='United States',
                            interval_note='Dates identify advertisements ending in this window; individual offer dates vary')
    if not out:
        raise ValueError('No verified USDA numeric rows; adapter unresolved')
    return out


def refresh_usda(data, attempted_at):
    data['sources']['us_ads'] = 'USDA AMS Weekly Grocery Store Beef Feature Activity'
    try:
        records = usda_prices()
        validate_retail_records('us', 'USDA ad survey', records, list(US_ITEMS))
        merge_records(data, 'us', 'USDA ad survey', records, list(US_ITEMS), attempted_at)
        status = data['source_status']['USDA ad survey']['status']
        if status == 'no_match':
            return ['USDA: no match']
        if status == 'partial':
            return ['USDA: older observations retained']
        return []
    except (*RETAIL_ERRORS, subprocess.SubprocessError) as error:
        state = {'status':'error', 'attempted_at':attempted_at,
                 'error_type':getattr(error, 'cause_type', type(error).__name__), 'note':error_detail(error)}
        if isinstance(error, USDARequestError):
            state['step'] = error.step
        elif isinstance(error, subprocess.SubprocessError):
            state['step'] = 'PDF text extraction'
        data['source_status']['USDA ad survey'] = state
        for record in data['us'].values():
            if record.get('source') == 'USDA ad survey':
                record.update(observation_status='retained_after_error', last_attempt_at=attempted_at)
        return ['USDA: ' + error_detail(error)]


def carrefour_prices(fx, keys=None):
    if not positive(fx):
        raise ValueError("Exchange rate must be a positive finite number")
    out = {}
    for key, (label, words) in AR_ITEMS.items():
        if keys is not None and key not in keys:
            continue
        listed = []
        queries = []
        query_limit = 20
        for query in AR_ALIASES.get(key, (words,)):
            q = urllib.parse.quote(query)
            found = json.loads(get(f"https://www.carrefour.com.ar/api/catalog_system/pub/products/search?ft={q}&_from=0&_to={query_limit - 1}"))
            if not isinstance(found, list):
                raise ValueError("Unexpected Carrefour response; previous snapshot retained")
            queries.append({"query": query, "returned_products": len(found)})
            listed.extend(catalog_matches(found, key, words))
            time.sleep(1)
        # Alias queries may return the same SKU; count it only once.
        listed = list({(p["product_id"], p["sku_id"], p["name"]): p for p in listed}.values())
        selected = [p for p in listed if p["available"]] or listed
        if selected:
            ars = statistics.median(p["ars_kg"] for p in selected)
            seller_ids = {p['seller_id'] for p in selected if isinstance(p['seller_id'], str) and p['seller_id'].strip()}
            sampling = {
                "queries": queries, "per_query_limit": query_limit,
                "eligible_count": len(listed), "selected_count": len(selected),
                "population": "available_listings" if any(p['available'] for p in selected) else "out_of_stock_references",
                "seller_policy": "first_seller_per_sku", "seller_ids": sorted(seller_ids),
                "unknown_seller_count": sum(not isinstance(p['seller_id'], str) or not p['seller_id'].strip() for p in selected),
                "region": None,
                "coverage": "possibly_truncated" if any(q['returned_products'] >= query_limit for q in queries) else "unknown",
            }
            out[key] = {"label": label, "ars_kg": ars, "usd_lb": round(ars / fx / LB_PER_KG, 2), "prev_usd_lb": None,
                        "period": datetime.now(timezone.utc).strftime("%Y-%m-%d"), "products": len(selected), "source": "Carrefour AR",
                        "availability": "in_stock" if any(p["available"] for p in selected) else "out_of_stock",
                        "fx_basis": "Latest returned daily observation (BCRA via datos.gob.ar)", "listings": selected,
                        "sampling":sampling,
                        "sampling_note":"At most 20 products/query, first seller; deduplicated SKU sample", "availability_as_of":timestamp()}
        else:
            print(f"  Carrefour: no verified per-kg matches for {label}", file=sys.stderr)
    return out


def validate_retail_records(region, source, records, keys):
    """Reject one malformed adapter batch before it can contaminate other sources."""
    if not isinstance(records, dict) or set(records) - set(keys):
        raise ValueError('Unexpected retail observation keys')
    if any(not isinstance(p, dict) or p.get('source') != source for p in records.values()):
        raise ValueError('Unexpected retail observation source')
    candidate = {'us': {}, 'ar': {}, 'fx': {}}
    candidate[region] = records
    validate_snapshot(qualify_snapshot(candidate))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cuts", nargs="+", choices=sorted(AR_ITEMS))
    official_mode = parser.add_mutually_exclusive_group()
    official_mode.add_argument("--official", action="store_true", help="Attempt BLS, INDEC, monthly FX and IPCVA independently")
    official_mode.add_argument("--official-snapshot", type=Path, help="Merge a local staged official snapshot by source")
    official_mode.add_argument("--ipcva-only", action="store_true", help="Refresh IPCVA AMBA and matching direct-BCRA USD quote means; preserve other sources")
    official_mode.add_argument("--usda-only", action="store_true", help="Refresh USDA advertised features only; preserve other sources")
    args = parser.parse_args()
    if args.cuts and (args.ipcva_only or args.usda_only):
        parser.error(('--ipcva-only' if args.ipcva_only else '--usda-only') + ' cannot be combined with --cuts')
    data = qualify_snapshot(json.loads(OUT.read_text()))
    attempted = timestamp()
    errors = []
    if args.usda_only:
        errors.extend(refresh_usda(data, attempted))
        write_snapshot(OUT, data)
        print_refresh_summary(data, errors, attempted)
        if errors:
            raise PartialRefreshError(errors)
        return
    if args.official or args.ipcva_only or 'ar_sources' in data:
        enable_ar_sources(data)
    if args.ipcva_only:
        errors.extend(refresh_ipcva(data, attempted))
        write_snapshot(OUT, data)
        print_refresh_summary(data, errors, attempted)
        if errors:
            raise SystemExit('Partial refresh: ' + ', '.join(errors))
        return
    if args.official or args.official_snapshot:
        if args.official:
            official = fetch_official(attempted)
        else:
            try:
                official = json.loads(args.official_snapshot.read_text())
            except (OSError, ValueError):
                official = None  # Classify all official sources as failed; retail still runs.
        errors.extend(merge_official(data, official, attempted))
        if args.official:
            errors.extend(refresh_ipcva(data, attempted))
    fx_row = None
    try:
        incoming_fx = json.loads(get(FX_URL))["data"][0]
        if not positive(incoming_fx[1]) or not valid_period(incoming_fx[0]) or len(incoming_fx[0]) != 10 or incoming_fx[0] > attempted[:10]:
            raise ValueError("Invalid/future FX observation")
        retained_fx = data['fx'].get('latest')
        if retained_fx and retained_fx.get('date') and incoming_fx[0] < retained_fx['date']:
            data['source_status']['FX daily'] = {
                'status': 'partial',
                'attempted_at': attempted,
                'observation_date': retained_fx['date'],
                'stale_observations': {
                    'FX daily': {
                        'received_period': incoming_fx[0],
                        'retained_period': retained_fx['date'],
                    }
                },
            }
            errors.append('FX daily: older observation retained')
            if positive(retained_fx.get('ars_per_usd')):
                # This rate was already accepted from the same source and is
                # newer than the current response, so it remains the best FX
                # evidence available for fresh catalog conversions.
                fx_row = [retained_fx['date'], retained_fx['ars_per_usd']]
        else:
            fx_row = incoming_fx
            data['fx']['latest'] = {
                'ars_per_usd': fx_row[1],
                'date': fx_row[0],
                'basis': 'Latest returned daily observation (BCRA via datos.gob.ar)',
            }
            data['source_status']['FX daily'] = {'status':'ok', 'attempted_at':attempted, 'observation_date':fx_row[0]}
    except RETAIL_ERRORS as error:
        fx_row = None
        errors.append('FX daily')
        data['source_status']['FX daily'] = {'status':'error', 'attempted_at':attempted, 'error_type':type(error).__name__, 'note':error_detail(error)}
    keys = args.cuts or list(AR_ITEMS)
    catalog_failures = {}
    # Each cut is independent: one blocked request cannot erase or block other observations.
    for key in keys:
        try:
            if fx_row is None:
                raise ValueError('FX unavailable; retaining original native and converted observations')
            records = carrefour_prices(fx_row[1], [key])
            validate_retail_records('ar', 'Carrefour AR', records, [key])
            for record in records.values():
                if not isinstance(record, dict):
                    raise ValueError('Catalog observation must be an object')
                record.update(fx_ars_per_usd=fx_row[1], fx_date=fx_row[0], fx_provenance='recorded', fx_basis='Latest returned daily observation (BCRA via datos.gob.ar)')
            validate_retail_records('ar', 'Carrefour AR', records, [key])
            merge_records(data, 'ar', 'Carrefour AR', records, [key], attempted)
            data.setdefault('catalog_attempts', {})[key] = data['source_status']['Carrefour AR']
            if data['source_status']['Carrefour AR']['status'] == 'partial':
                errors.append('Carrefour ' + key + ': older observation retained')
        except RETAIL_ERRORS as error:
            catalog_failures.setdefault(error_detail(error), []).append(key)
            data.setdefault('catalog_attempts', {})[key] = {'status':'error', 'attempted_at':attempted, 'error_type':type(error).__name__, 'note':error_detail(error)}
            catalog_records = source_records(data, 'ar', 'Carrefour AR')
            if key in catalog_records:
                catalog_records[key]['observation_status'] = 'retained_after_error'
    for detail, failed_keys in catalog_failures.items():
        errors.append('Carrefour ' + ', '.join(failed_keys) + ': ' + detail)
    coverage = {k:data['catalog_attempts'][k]['status'] for k in keys}
    outcomes = set(coverage.values())
    catalog_status = ('error' if outcomes == {'error'} else 'partial_error' if 'error' in outcomes
                      else 'no_match' if outcomes == {'no_match'} else 'partial' if 'no_match' in outcomes or 'partial' in outcomes else 'ok')
    catalog_summary = {'status':catalog_status, 'attempted_at':attempted, 'coverage':coverage}
    if catalog_failures:
        catalog_summary['note'] = '; '.join(catalog_failures)
    stale_catalog = {
        key: data['catalog_attempts'][key]['stale_observations'][key]
        for key in keys
        if key in data.get('catalog_attempts', {})
        and key in data['catalog_attempts'][key].get('stale_observations', {})
    }
    if stale_catalog:
        catalog_summary['stale_observations'] = stale_catalog
    data['source_status']['Carrefour AR'] = catalog_summary
    if 'no_match' in outcomes:
        errors.append('Carrefour AR: no match for ' + ', '.join(k for k, state in coverage.items() if state == 'no_match'))
    if not args.cuts:
        errors.extend(refresh_usda(data, attempted))
    data['sources'].update(us_ads='USDA AMS Weekly Grocery Store Beef Feature Activity', ar_retail='Carrefour Argentina online catalog')
    select_ar_sources(data)
    write_snapshot(OUT, data)
    print_refresh_summary(data, errors, attempted)
    if errors:
        raise PartialRefreshError(errors)


def cli():
    try:
        main()
    except PartialRefreshError as error:
        raise SystemExit(f'Partial refresh: {len(error.issues)} source issues; see results above.') from None


if __name__ == "__main__":
    cli()
