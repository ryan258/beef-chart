# Data Pipeline Specification

This document details the automated price data ingestion, normalization, parsing logic, and verification routines for **The Cow, Two Ways**.

---

## 1. Pipeline Architecture

The ingestion pipeline produces an atomic, consolidated data snapshot at [`data/prices.json`](../data/prices.json) by combining official government macroeconomic statistical data with weekly retail ad surveys and live supermarket catalogs.

```
+--------------------------------------------------------------------------------+
|                             fetch-prices.sh                                    |
|                                                                                |
|  1. US BLS API v2           --> Monthly US average retail steak & roast series |
|  2. INDEC via datos.gob.ar  --> Monthly Greater Buenos Aires average prices    |
|  3. BCRA via datos.gob.ar   --> Monthly average official ARS/USD rate          |
|                                                                                |
|  Writes temporary snapshot: data/prices.XXXXXX                                 |
+--------------------------------------------------------------------------------+
                                       |
                                       v
+--------------------------------------------------------------------------------+
|                             scrape-retail.py                                   |
|                                                                                |
|  4. USDA AMS Weekly Ad PDF  --> pdftotext extraction of store-weighted features|
|  5. Carrefour Argentina API --> Real-time butcher per-kg listings             |
|                                                                                |
|  Merges into snapshot, validates schema, atomically replaces data/prices.json   |
+--------------------------------------------------------------------------------+
```

---

## 2. Data Sources & Integration Details

### US Bureau of Labor Statistics (BLS)
- **Endpoint**: `https://api.bls.gov/publicAPI/v2/timeseries/data/`
- **Method**: HTTP POST with JSON payload containing series IDs.
- **Tracked Series**:
  - `APU0000703112`: Ground beef, 100% beef ($/lb)
  - `APU0000703111`: Ground chuck, 100% beef ($/lb)
  - `APU0000703113`: Ground beef, lean & extra lean ($/lb)
  - `APU0000703311`: Round roast, USDA Choice, boneless ($/lb)
  - `APU0000703511`: Round steak, USDA Choice, boneless ($/lb)
  - `APU0000703613`: Sirloin steak, USDA Choice, boneless ($/lb)
- **Cadence**: Monthly publication.

### Argentine INDEC IPC-GBA (via `datos.gob.ar`)
- **Endpoint**: `https://apis.datos.gob.ar/series/api/series/`
- **Tracked Series**:
  - `105.1_I2CPC_2016_M_27`: Carne picada común (ARS/kg)
  - `105.1_I2A_2016_M_14`: Asado (ARS/kg)
  - `105.1_I2C_2016_M_16`: Cuadril (ARS/kg)
  - `105.1_I2N_2016_M_14`: Nalga (ARS/kg)
  - `105.1_I2P_2016_M_15`: Paleta (ARS/kg)

### Banco Central de la República Argentina (BCRA)
- **Series ID**: `92.2_TIPO_CAMBIION_0_0_21_24` (Tipo de cambio minorista / oficial)
- **Transformation Formula**:
  $$\text{USD/lb} = \frac{\text{ARS/kg}}{\text{FX Rate}} \times \frac{1}{2.2046226}$$
- **FX Rule**: INDEC records use the monthly average rate matched to the price month with `fx_basis` set to BCRA monthly average. Carrefour records use the daily latest rate with `fx_basis` set to BCRA daily latest. Every AR record stores `fx_ars_per_usd` plus `fx_date` plus `fx_basis`. Top level `fx` keeps the monthly average while `fx.latest` keeps the daily latest with basis labels.

### USDA AMS Weekly Grocery Feature Activity (AMS_3228)
- **Source**: `https://www.ams.usda.gov/mnreports/AMS_3228.pdf`
- **Parser**: Extracted via `pdftotext -layout` in Python.
- **Computation**: Store-weighted average across conventional fresh beef offerings:
  $$\bar{x} = \frac{\sum (\text{stores}_i \times \text{price}_i)}{\sum \text{stores}_i}$$
- **Tracked Items**: Boneless Ribeye, Boneless Strip, Tenderloin, Whole Brisket, Chuck Roast, Short Ribs, Skirt Steak, Flank Steak, Tri-Tip, Eye of Round, Bottom Round.

### Carrefour Argentina Catalog Scraper
- **Endpoint**: `https://www.carrefour.com.ar/api/catalog_system/pub/products/search`
- **Target Category**: `CARNICERIA` (fresh butcher section).
- **Strict Verification Rules**:
  1. **Strict per-kg pricing**: Listings must explicitly advertise `x kg` or `por kg` to prevent fixed-weight pre-packaged items (e.g., 500g trays) from polluting the per-kilogram rate.
  2. **Species Exclusions**: Excludes non-beef meats via regex (`cerdo`, `pollo`, `cordero`, `guanaco`, etc.).
  3. **Preparation Exclusions**: Filters out breaded (*milanesa*), marinated, pickled (*escabeche*, *vinagreta*), or pre-cooked items.
  4. **Dedicated Gland / Cut Differentiation**: Keeps *bife de costilla* (bone-in) distinct from boneless *bife de chorizo* and T-bone; handles sweetbreads (*mollejas*) with provenance warnings acknowledging retailer generic descriptions.
  5. **Deduplication**: Multi-alias queries deduplicate SKUs by `(product_id, sku_id, name)`.
  6. **Median Price**: Aggregates available in-stock items using statistical median.

---

## 3. Atomic Updates & Fault Tolerance

The pipeline guarantees that a network glitch, bad API response, or parsing failure never leaves `data/prices.json` corrupted:
1. `fetch-prices.sh` creates a temporary file `data/prices.XXXXXX` via `mktemp`.
2. Python scraper loads the temporary file, fetches FX and catalog items.
3. If any step fails (e.g. HTTP 403 or schema mismatch), the process exits with an error and the trap cleans up the tempfile, leaving the original `data/prices.json` intact.
4. Python scraper performs an atomic write using `tempfile.NamedTemporaryFile` in `data/` followed by an atomic `replace()`.

---

## 4. Testing & Verification

Unit tests in [`tests/test_retail_prices.py`](../tests/test_retail_prices.py) execute deterministically with zero network calls:
- **`test_new_names_and_accents`**: Confirms normalization of accented queries (*Riñón*, *Mollejas*, *Bife de costilla*).
- **`test_wrong_species_prepared_and_ambiguous_units_rejected`**: Ensures non-bovine meats and non-kg packaging are rejected.
- **`test_alias_dedup_conversion_and_stock`**: Verifies SKU deduplication, currency conversion math, stock status, and daily latest FX basis.
- **`test_chorizo_stays_separate`**: Confirms bone-in vs boneless cut discrimination.
- **`test_failed_refresh_preserves_snapshot`**: Tests atomic rollback on HTTP failure.
- **`test_invalid_fx`**: Verifies that non-finite or negative exchange rates raise errors.
- **`test_usda_rows_and_weighted_average`**: Verifies USDA layout parsing and store weighted math and fallback to prior week.
- **`test_usda_ignores_non_conventional_rows`**: Verifies that non fresh rows and Lbs rows do not pollute the average.

Run tests:
```bash
pytest tests/test_retail_prices.py -q
```
