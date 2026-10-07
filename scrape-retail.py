#!/usr/bin/env python3
"""Scrape current retail beef prices and merge them into data/prices.json (run after fetch-prices.sh).

  US: USDA AMS weekly grocery-store beef ad report (PDF, needs `pdftotext` from poppler: brew install poppler).
      Advertised prices, store-weighted across conventional fresh items; not shelf-price averages.
  AR: Carrefour Argentina public catalog search (butcher-section items sold by the kg), median per cut.
"""
import argparse, os, math, json, re, statistics, subprocess, sys, tempfile, time, unicodedata, urllib.parse, urllib.request
from datetime import datetime
from pathlib import Path

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
    """Return auditable per-kg offers; never interpret a pack price as a kg price."""
    listed = []
    aliases = AR_ALIASES.get(key, (unaccent(words),))
    for product in products:
        name = unaccent(product.get("productName", ""))
        if not any(re.match(re.escape(alias) + r"\b", name) for alias in aliases):
            continue
        if product.get("EC_Sección") != ["CARNICERIA"] or SKIP.search(name):
            continue
        if key in NEW_AR_KEYS and EXCLUDE_NEW.search(name):
            continue
        # Carrefour's x kg names explicitly declare the price basis. Reject
        # fixed-weight packs and ambiguous unit listings for the new entries.
        if key in NEW_AR_KEYS:
            if not re.search(r"(?:x|por)\s*(?:1\s*)?kg\b", name):
                continue
        elif "kg" not in name:
            continue
        for item in product.get("items", []):
            if key in NEW_AR_KEYS and (item.get("measurementUnit") not in (None, "kg")
                                      or item.get("unitMultiplier", 1) != 1):
                continue
            for seller in item.get("sellers", [])[:1]:
                offer = seller.get("commertialOffer", {})
                price = offer.get("Price")
                if not isinstance(price, (int, float)) or isinstance(price, bool) or not math.isfinite(price) or price <= 0:
                    continue
                listed.append({"ars_kg": price, "available": offer.get("IsAvailable") is True,
                               "product_id": product.get("productId"), "sku_id": item.get("itemId"),
                               "name": product.get("productName"), "url": product.get("link")})
    return listed


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; beef-chart price snapshot)"})
    return urllib.request.urlopen(req, timeout=60).read()


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
                vals[i] = float(t.group().replace(",", ""))
        yield item, vals


def usda_prices():
    with tempfile.NamedTemporaryFile(suffix=".pdf") as f:
        f.write(get(USDA_PDF)); f.flush()
        text = subprocess.run(["pdftotext", "-layout", f.name, "-"], capture_output=True, text=True, check=True).stdout
    d = re.search(r"(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun) (\w{3}) (\d+), (\d{4})", text)
    period = datetime.strptime(" ".join(d.groups()), "%b %d %Y").strftime("%Y-%m-%d")
    rows = list(usda_rows(text))

    def wavg(prefix, si, ai):  # store-weighted average over matching rows
        pts = [(v[si], v[ai]) for item, v in rows if item.startswith(prefix) and "Lbs" not in item and v[si] and v[ai]]
        n = sum(s for s, _ in pts)
        return (sum(s * a for s, a in pts) / n, n) if n else (None, 0)

    out = {}
    for key, (label, prefix) in US_ITEMS.items():
        cur, n = wavg(prefix, 0, 1)
        prev, _ = wavg(prefix, 2, 3)
        if cur is None:  # not advertised this week: fall back to last week's figure
            cur, n, prev = prev, wavg(prefix, 2, 3)[1], None
        if cur is None:
            print(f"  USDA: no rows for {label}", file=sys.stderr); continue
        out[key] = {"label": label, "usd_lb": round(cur, 2), "prev_usd_lb": round(prev, 2) if prev else None,
                    "period": period, "stores": int(n), "source": "USDA ad survey"}
    return out


def carrefour_prices(fx, keys=None):
    if not isinstance(fx, (int, float)) or not math.isfinite(fx) or fx <= 0:
        raise ValueError("Exchange rate must be a positive finite number")
    out = {}
    for key, (label, words) in AR_ITEMS.items():
        if keys is not None and key not in keys:
            continue
        listed = []
        for query in AR_ALIASES.get(key, (words,)):
            q = urllib.parse.quote(query)
            found = json.loads(get(f"https://www.carrefour.com.ar/api/catalog_system/pub/products/search?ft={q}&_from=0&_to=19"))
            if not isinstance(found, list):
                raise ValueError("Unexpected Carrefour response; previous snapshot retained")
            listed.extend(catalog_matches(found, key, words))
            time.sleep(1)
        # Alias queries may return the same SKU; count it only once.
        listed = list({(p["product_id"], p["sku_id"], p["name"]): p for p in listed}.values())
        selected = [p for p in listed if p["available"]] or listed
        if selected:
            ars = statistics.median(p["ars_kg"] for p in selected)
            out[key] = {"label": label, "ars_kg": ars, "usd_lb": round(ars / fx / LB_PER_KG, 2), "prev_usd_lb": None,
                        "period": datetime.now().strftime("%Y-%m-%d"), "products": len(selected), "source": "Carrefour AR",
                        "availability": "in_stock" if any(p["available"] for p in selected) else "out_of_stock",
                        "listings": selected}
        else:
            print(f"  Carrefour: no verified per-kg matches for {label}", file=sys.stderr)
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cuts", nargs="+", choices=sorted(AR_ITEMS),
                        help="Refresh only these Argentine cuts; retain all other series")
    args = parser.parse_args()
    data = json.loads(OUT.read_text())
    fx_row = json.loads(get(FX_URL))["data"][0]
    # Fetch everything before modifying the snapshot. Any network/parsing error
    # leaves the last good file intact, including for targeted refreshes.
    ar = carrefour_prices(fx_row[1], args.cuts)
    us = None if args.cuts else usda_prices()
    data["fx"]["latest"] = {"ars_per_usd": fx_row[1], "date": fx_row[0]}
    if args.cuts:
        for key in args.cuts:
            data["ar"].pop(key, None)
    else:
        for group in ("us", "ar"):
            data[group] = {k: v for k, v in data[group].items() if v.get("source") in ("BLS", "INDEC")}
        data["us"].update(us)
    for record in ar.values():
        record["fx_ars_per_usd"] = fx_row[1]
        record["fx_date"] = fx_row[0]
    data["ar"].update(ar)
    data["sources"].update(us_ads="USDA AMS Weekly Grocery Store Beef Feature Activity", ar_retail="Carrefour Argentina online catalog")
    with tempfile.NamedTemporaryFile(mode="w", dir=OUT.parent, delete=False) as f:
        json.dump(data, f, indent=1, ensure_ascii=False)
        temp = Path(f.name)
    temp.replace(OUT)
    print(f"merged scraped prices: {len(data['us'])} US, {len(data['ar'])} AR series")


if __name__ == "__main__":
    main()
