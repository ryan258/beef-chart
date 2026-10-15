# IPCVA source discovery — 15 October 2026

IPCVA provides a usable public monthly retail price export. The September 2026 report confirms that the dashboard's current beef values correspond to AMBA. Rosario and Córdoba have separate tables in the report. These are regional survey averages in current Argentine pesos, not nationwide prices or live offers.

This directory records the initial source discovery. IPCVA integration and the subsequent direct-BCRA FX repair are now implemented; see `docs/data-pipeline.md` for current behavior. The receipts below remain evidence of the initial lookup.

## Public source routes

- Current homepage: https://ipcva.com.ar/ — directly linked the September report at retrieval. The old `vertodas2.php?se=84` report archive only listed reports through December 2024 during this check, so it is unsuitable for latest-report discovery.
- Form: https://ipcva.agrositio.com/estadisticas/vista_precios_consumidor2.php
- Export: https://ipcva.agrositio.com/estadisticas/vista_precios_consumidor_xls.php
- Current report: https://api.carneargentina.org.ar/web/uploads/globals/1/Informe%20Mensual%20de%20Precios%20SEP26_.pdf

The form submits a normal POST to itself with `mes_desde=01-01`, `ano_desde=2024`, `mes_hasta=10-01`, `ano_hasta=2026`, repeated `productos[]` IDs and `procesar=Procesar`. The response contains an ordinary HTML table and an export link. One bounded lookup for three cuts returned January 2024 through September 2026. October was requested but had no returned row; never infer a month from the requested range.

The export accepts GET parameters `productos` (comma-separated IDs), `desde` and `hasta` (YYYY-MM-DD). The `.xls` suffix serves an HTML table, not a binary Excel workbook. No credentials, browser automation or JavaScript execution were needed for these requests. This is an observed public export route, not a documented or guaranteed API.

Exact all-product request used:

https://ipcva.agrositio.com/estadisticas/vista_precios_consumidor_xls.php?productos=10,70,15,71,72,12,86,73,14,74,16,75,76,77,87,13,78,11,79,80,81,82,17,83,88,84,89,85&desde=2026-08-01&hasta=2026-10-01

## What was extracted and checked

- 28 dashboard product columns, including two old generic categories with `S/D` in both returned months.
- August and September 2026 values; all 22 named beef-cut/product values matched AMBA report table 3 exactly for both months (44 comparisons).
- Report tables 3, 5 and 7: 28 rows each for AMBA, Rosario and Córdoba, with September 2025, August 2026 and September 2026 prices plus monthly, year-to-date and annual percentage changes.
- AMBA reported average beef price: ARS 18,514/kg in September, up 0.5% monthly and 49.8% annually. This average is a price level; it is not a dimensionless index value.
- `extracted-prices.json` preserves the export values, product IDs, report rows, candidate cut mappings, retrieval time and raw receipt SHA-256 hashes. This was a bounded research extraction, not a production adapter acceptance check.

## Survey meaning

The September report says fieldwork took place during the first and third weeks of the month. AMBA has 120 points of sale: 80 butcher shops surveyed by phone and 40 supermarkets surveyed in person. Rosario and Córdoba each have 30 butcher shops and 15 supermarkets. Its methodology instructs surveyors to record the lowest price for each cut in each point of sale. These survey averages do not establish present availability, a specific package weight, or U.S./Argentine specification equivalence.

## Fit to the current chart

Nine of the 17 currently configured Carrefour keys have clear name counterparts:

| Project key | Export product | ID | September 2026, ARS/kg |
|---|---|---:|---:|
| bife_ancho | Bife Ancho | 70 | 17,803 |
| bife_angosto | Bife angosto | 15 | 18,617 |
| lomo | Lomo | 77 | 28,017 |
| vacio | Vacío | 85 | 21,331 |
| matambre | Matambre | 87 | 17,905 |
| colita | Colita de cuadril | 86 | 23,939 |
| peceto | Peceto | 79 | 23,737 |
| osobuco | Osobuco | 78 | 11,720 |
| cuadrada | Cuadrada | 73 | 19,536 |

These are candidate name mappings. The source does not establish boneless/bone-in, grade, trimming or other product specifications needed to make unlike observations directly comparable.

Five additional source names overlap the current INDEC keys: asado, cuadril, nalga, paleta, and common ground beef. Preserve the separate source identity and population if these are integrated.

The dashboard/report do not provide named molleja, riñón, lengua, entraña or tapa de cuadril rows. Tapa de asado and tapa de nalga must not substitute for tapa de cuadril. No direct aguja, pecho or specifically bone-in bife de costilla mapping was established. Asado de tira is a distinct source label.

## Parsing and integration constraints

- Keep `S/D` as missing data, never zero. A form checkbox does not prove current coverage.
- Dashboard values use decimal points; export values use Argentina-style currency separators (`$ 17.869,00`). Month abbreviations also vary between the two views (`Aug`/`Ago`).
- Beef cuts are ARS/kg, confirmed against the report. Frozen hamburgers are quoted per four units; they must not be treated as ARS/kg.
- Preserve observation month, retrieval timestamp, source label, geography and survey method. The source did not establish an exact publication date in the inspected evidence.
- Use matching monthly FX for any USD/lb conversion. A current daily rate would change the meaning of the monthly observation.
- A future adapter should use the public HTML export for AMBA and independently check the latest report's identity/period. Rosario/Córdoba currently require parsing separate PDF tables; no regional dashboard selector was established.
- Source changes require explicit promotion policy. A September survey average should not silently replace an October retailer observation merely because its source is preferred; preserve both evidence and the existing monotonic refresh contract.
- The initial discovery did not change production code or stored observations; subsequent integration is documented in `docs/data-pipeline.md`.

## Receipts

- `dashboard-form.html`: retrieved form and product IDs.
- `consumer-prices-export.html`: exact all-product export response for the requested interval.
- `monthly-prices-2026-09.pdf`: current report linked by IPCVA's homepage.
- `monthly-prices-2026-09.txt`: `pdftotext -layout` extraction of that report.
- `extracted-prices.json`: structured research extraction and comparison result.
