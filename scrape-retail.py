#!/usr/bin/env python3
"""Explicit retail refresh into data/prices.json; ./fetch-prices.sh also attempts official monthly sources.

  US: USDA AMS weekly grocery-store beef ad report (PDF, needs `pdftotext` from poppler: brew install poppler).
      Advertised prices, store-weighted across conventional fresh items; not shelf-price averages.
  AR: Carrefour Argentina public catalog search (butcher-section items sold by the kg), median per cut.
  FX rule: INDEC records use BCRA monthly average matched to the price month.
      Carrefour records use the latest returned BCRA observation, which can lag. Each AR record stores fx_ars_per_usd,
      fx_date, and fx_basis so the page can display provenance without mixing bases.
"""
import argparse, os, math, json, re, statistics, subprocess, sys, tempfile, time, unicodedata, urllib.parse, urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from price_contract import positive, valid_period, qualify_snapshot, merge_records, write_snapshot, timestamp
from official_prices import fetch_official, merge_official

OUT = Path(os.environ.get("BEEF_PRICES_OUT", Path(__file__).parent / "data" / "prices.json"))
USDA_PDF = "https://www.ams.usda.gov/mnreports/AMS_3228.pdf"
FX_URL = "https://apis.datos.gob.ar/series/api/series/?ids=92.2_TIPO_CAMBIION_0_0_21_24&last=1&format=json"
LB_PER_KG = 2.2046226
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
            continue
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
        for item in product.get("items", []):
            if item.get("measurementUnit") != "kg" or (item.get("unitMultiplier") != 1 or isinstance(item.get("unitMultiplier"), bool)):
                continue
            for seller in item.get("sellers", [])[:1]:
                offer = seller.get("commertialOffer", {})
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
    return urllib.request.urlopen(req, timeout=20).read()


def unaccent(s):
    return "".join(c for c in unicodedata.normalize("NFD", s.lower()) if unicodedata.category(c) != "Mn")


def usda_rows(text):
    """Yield (item, [cw_stores, cw_avg, pw_stores, pw_avg, py_stores, py_avg]) for conventional fresh rows."""
    cols = item_col = None
    for line in text.splitlines():
        if "Item" in line and "Environment" in line:
            item_col = line.index("Item")
        if "Stores" in line and "Wtd Avg" in line:
            found = [m.end() for m in re.finditer(r"Stores|Wtd Avg", line)]
            if len(found) == 6:
                cols = found
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


def usda_intervals(text):
    """Only explicit feature ranges establish current/prior dates; never report-date arithmetic."""
    ranges = {}
    pattern = r"(This Week|Current Week|Prior Week|Previous Week)\s*:?\s*(\d{2}/\d{2}/\d{4})\s*(?:-|to)\s*(\d{2}/\d{2}/\d{4})"
    for label, start, end in re.findall(pattern, text, re.I):
        begin = datetime.strptime(start, '%m/%d/%Y').strftime('%Y-%m-%d')
        finish = datetime.strptime(end, '%m/%d/%Y').strftime('%Y-%m-%d')
        if begin > finish:
            raise ValueError('Reversed USDA feature interval')
        ranges['prior' if label.lower().startswith(('prior', 'previous')) else 'current'] = (begin, finish)
    if 'current' not in ranges or 'prior' not in ranges:
        raise ValueError('USDA adapter unresolved: explicit current/prior feature intervals not recognized; retain old evidence')
    if ranges['prior'][1] >= ranges['current'][0]:
        raise ValueError('Overlapping USDA feature intervals')
    return ranges


def usda_prices():
    with tempfile.NamedTemporaryFile(suffix=".pdf") as f:
        f.write(get(USDA_PDF)); f.flush()
        text = subprocess.run(["pdftotext", "-layout", f.name, "-"], capture_output=True, text=True, check=True, timeout=20).stdout
    d = re.search(r"(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun) (\w{3}) (\d+), (\d{4})", text)
    if not d:
        raise ValueError('USDA report publication date missing')
    publication = datetime.strptime(" ".join(d.groups()), "%b %d %Y").strftime("%Y-%m-%d")
    intervals = usda_intervals(text)
    rows = list(usda_rows(text))
    def wavg(prefix, si, ai):
        pts = [(v[si], v[ai]) for item, v in rows if item.startswith(prefix) and "Lbs" not in item and positive(v[si]) and positive(v[ai])]
        n = sum(s for s, _ in pts)
        return (sum(s * a for s, a in pts) / n, n) if n else (None, 0)
    out = {}
    for key, (label, prefix) in US_ITEMS.items():
        cur, n = wavg(prefix, 0, 1)
        prev, pn = wavg(prefix, 2, 3)
        fallback = cur is None
        if fallback:
            cur, n = prev, pn
        if cur is None:
            continue
        start, end = intervals['prior' if fallback else 'current']
        out[key] = {"label":label, "usd_lb":round(cur,2), "prev_usd_lb":round(prev,2) if prev and not fallback else None,
                    "prev_period":intervals['prior'][1] if prev and not fallback else None,
                    "period":end, "effective_start":start, "effective_end":end, "publication_date":publication,
                    "fallback_reason":"not_advertised_current_interval" if fallback else None,
                    "stores":int(n), "source":"USDA ad survey", "adapter_status":"unresolved_real_layout",
                    "provenance_status":"parsed_unverified", "observation_status":"unverified_layout"}
    if not out:
        raise ValueError('No verified USDA numeric rows; adapter unresolved')
    return out


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


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cuts", nargs="+", choices=sorted(AR_ITEMS))
    official_mode = parser.add_mutually_exclusive_group()
    official_mode.add_argument("--official", action="store_true", help="Attempt BLS, INDEC and monthly FX independently")
    official_mode.add_argument("--official-snapshot", type=Path, help="Merge a local staged official snapshot by source")
    args = parser.parse_args()
    data = qualify_snapshot(json.loads(OUT.read_text()))
    attempted = timestamp()
    errors = []
    if args.official or args.official_snapshot:
        if args.official:
            official = fetch_official(attempted)
        else:
            try:
                official = json.loads(args.official_snapshot.read_text())
            except (OSError, ValueError):
                official = None  # Classify all official sources as failed; retail still runs.
        errors.extend(merge_official(data, official, attempted))
    fx_row = None
    try:
        fx_row = json.loads(get(FX_URL))["data"][0]
        if not positive(fx_row[1]) or not valid_period(fx_row[0]) or fx_row[0] > attempted[:10]:
            raise ValueError("Invalid/future FX observation")
        data["fx"]["latest"] = {"ars_per_usd":fx_row[1], "date":fx_row[0], "basis":"Latest returned daily observation (BCRA via datos.gob.ar)"}
        data['source_status']['FX daily'] = {'status':'ok', 'attempted_at':attempted, 'observation_date':fx_row[0]}
    except (OSError, ValueError, KeyError, IndexError, TypeError) as error:
        fx_row = None
        errors.append('FX daily')
        data['source_status']['FX daily'] = {'status':'error', 'attempted_at':attempted, 'error_type':type(error).__name__}
    keys = args.cuts or list(AR_ITEMS)
    # Each cut is independent: one blocked request cannot erase or block other observations.
    for key in keys:
        try:
            if fx_row is None:
                raise ValueError('FX unavailable; retaining original native and converted observations')
            records = carrefour_prices(fx_row[1], [key])
            for record in records.values():
                record.update(fx_ars_per_usd=fx_row[1], fx_date=fx_row[0], fx_provenance='recorded', fx_basis='Latest returned daily observation (BCRA via datos.gob.ar)')
            merge_records(data, 'ar', 'Carrefour AR', records, [key], attempted)
            data.setdefault('catalog_attempts', {})[key] = data['source_status']['Carrefour AR']
        except (OSError, ValueError, KeyError, TypeError) as error:
            errors.append('Carrefour ' + key)
            data.setdefault('catalog_attempts', {})[key] = {'status':'error', 'attempted_at':attempted, 'error_type':type(error).__name__}
            if key in data['ar']:
                data['ar'][key]['observation_status'] = 'retained_after_error'
    data['source_status']['Carrefour AR'] = {'status':'partial_error' if any(e.startswith('Carrefour') for e in errors) else 'ok', 'attempted_at':attempted, 'coverage':{k:data['catalog_attempts'][k]['status'] for k in keys}}
    if not args.cuts:
        try:
            us = usda_prices()
            merge_records(data, 'us', 'USDA ad survey', us, list(US_ITEMS), attempted)
        except (OSError, ValueError, subprocess.SubprocessError, KeyError, TypeError) as error:
            errors.append('USDA')
            data['source_status']['USDA ad survey'] = {'status':'error', 'attempted_at':attempted, 'error_type':type(error).__name__}
            for record in data['us'].values():
                if record.get('source') == 'USDA ad survey':
                    record['observation_status'] = 'retained_after_error'
    data['sources'].update(us_ads='USDA AMS Weekly Grocery Store Beef Feature Activity', ar_retail='Carrefour Argentina online catalog')
    write_snapshot(OUT, data)
    print(f"Stored snapshot; {len(errors)} source issues, retained observations keep their original dates")
    if errors:
        raise RuntimeError('Partial refresh: ' + ', '.join(errors))


if __name__ == "__main__":
    main()
