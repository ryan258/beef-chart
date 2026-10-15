# The Cow, Two Ways (Beef Chart)

An interactive Argentine/U.S. beef atlas with a stored, mixed-source retail-price snapshot and owner-entered local quotes. It supports exploration and contextual comparison; it does not stream live prices or establish current supplier offers.

Built with a Bauhaus page layout, vintage halftone illustrations, Saul Bass-inspired cut-paper SVG maps, and D3.js visualizations. The artwork supports identification and exploration; it does not certify a product's anatomy, trim, or purchasing specification.

---

## Overview

Both traditions combine anatomical boundaries, local retail practice, and culinary uses. Names, trim, bone, and preparation vary; the paired schematics provide context rather than exact purchase specifications.

**The Cow, Two Ways** bridges these two worlds:

- **Interactive Cut Maps**: Twenty Argentine cut controls and nine U.S. region controls, with shared hover/focus highlighting, full-name readouts, keyboard activation, and a complete directory alternative. Hatched lomo, entraña, and peceto overlays identify layered references.
- **Illustrated Dossiers**: All 24 catalog entries have transparent halftone illustrations. Six popular-cut cards and four specialty cards use the same illustration set; ribeye and sirloin have distinct shapes. The cow portrait, pasture scene, and cow favicon complete the visual treatment.
- **English / Castellano porteño**: The header toggle translates the page, all 24 dossiers, chart/table labels, search feedback, and price qualifications. Spanish uses Rioplatense voseo and light lunfardo; U.S. names remain available as cultural references. Search accepts names in either language, with or without accents, plus aliases such as *ojo de bife* and *tira de asado*.
- **Stored Retail Context**: Dated automatic observations and labeled manual quotes. Converted or native USD/lb values appear in the context chart; native-only ARS/kg stays visible in text and tables. Source, geography, interval, product form, availability, and FX basis qualify comparison. A 24-cut coverage summary makes missing, retained, withheld and manual observations explicit.
- **Manual Local Prices**: Ten Argentine cuts are prefilled in [the active manual file](data/manual-prices.json). Fill in a date and numeric price when available, save, and reload. Unfinished rows are skipped; automatic observations and original Carrefour evidence remain available. [Entry instructions and machine names](docs/manual-prices.md).
- **Advanced D3 Data Visualizations**:
  - **Sankey Flow Diagram**: Nine primal teaching allocations flow to culinary uses, including Other uses; 100 illustrative units in total.
  - **US vs Argentina Price Lollipop**: Mixed-source retail context by cut: USDA advertised features and BLS monthly averages for the U.S.; IPCVA AMBA survey prices, INDEC averages, retained Carrefour references and optional manual quotes for Argentina. Color identifies the country; hollow dots/asterisks mark retained references and daggers mark manual USD quotes. These are contextual pairs with product and date qualifications.
  - **Value Treemap**: Fixed illustrative retail-value allocation; not carcass weight, measured yield, or a current-price calculation.
  - **Editorial Radar**: Six heuristic trait scores; not measured sensory evidence or grades.
- **Specialized & Offal Cuts**: Dedicated entries for *bife de costilla*, *mollejas* (sweetbreads), *riñón* (kidney), and *lengua* (tongue). The three stored organ prices remain withheld because their unit scales are unverified.

---

## Architectural & Design System

The frontend combines a **Bauhaus layout with vintage print illustration**, with base styles in `index.html` refined by `assets/bauhaus.css`:

- **Grid Discipline**: Rigid 1px structural ink borders, asymmetrical hero compositions, and modular data cards.
- **Active Color Palette**: Canvas `#f1f0e8`, ink `#20211e`, red `#c73524`, gold `#edc445`, and blue `#234dba`. The maps use separate terracotta/ochre and muted blue/ochre inks; map fills do not change chart data colors.
- **Typography**: `Space Grotesk` and `Inter` for the page, `Oswald` for diagram labels, and `Playfair Display` for dossier titles.
- **Artwork**: Transparent 1024 × 1024 WebP cut illustrations, opaque halftone hero/pasture images, and native SVG diagrams. Prompts, asset mappings, references, and display checks are recorded in [the artwork record](docs/artwork-prompts.md).
- **Responsive Architecture**: Multi-tier CSS grid and flexbox breakpoints supporting desktop (1600px+), tablet, and mobile down to 320px.
- **Accessibility (a11y)**: Visible focus, skip links, and reduced-motion styles are implemented. The full directory and chart tables, named native dialogs, failure isolation, and narrow-screen reader layouts are implemented locally; full WCAG and device/assistive-technology acceptance are unverified.

---

## Data Pipeline & Sources

The project consumes multi-tiered public economic and retail datasets:

| Market | Source | Update Cadence | Metric / Basis |
|---|---|---|---|
| **US** | **Bureau of Labor Statistics (BLS)** | Monthly | National average consumer prices (USD/lb) |
| **US** | **USDA AMS Grocery Feature Survey** | Weekly | Store-weighted advertised retail features via parsed PDF |
| **AR** | **IPCVA consumer-price export** | Monthly | AMBA survey averages for 22 beef rows, ARS/kg; primary automatic source for covered cuts |
| **AR** | **INDEC IPC-GBA** via `datos.gob.ar` | Monthly | Greater Buenos Aires retail averages (ARS/kg) |
| **AR** | **Carrefour Argentina Online Catalog** | On-demand; no schedule installed | Median raw butcher-counter offerings per kg, converted at latest returned BCRA observation |
| **FX** | **BCRA direct USD quote history** | Matching completed months for IPCVA | Arithmetic mean of returned published USD quotes; distinct from the valuation-rate series |
| **FX** | **Banco Central (BCRA)** via `datos.gob.ar` | Matching monthly average for INDEC; latest returned daily observation for catalog | ARS per USD observation with per-record basis/date and recorded/inferred/unknown provenance |

Automatic output is consolidated in [`data/prices.json`](data/prices.json), with separate Argentine source ledgers and the preserved original Carrefour archive. [Manual prices](data/manual-prices.json) are an independent display overlay; refresh scripts never write that file. They require a valid automatic snapshot first. The [data contract](docs/data-pipeline.md) describes selection, dates, FX and failure behavior.

---

## Directory Structure

```
beef-chart/
├── index.html                      # Cut catalog, search, validation, charts and dossiers
├── assets/
│   ├── bauhaus.css                 # Active layout and responsive reader rules
│   ├── i18n.js                     # English / Argentine-Spanish catalog and formatting
│   ├── manual-prices.js            # Draft handling, validation and manual display selection
│   └── *.webp / favicon*           # Cut, cow and pasture illustrations; browser icons
├── data/
│   ├── prices.json                 # Automatic snapshot, source ledgers, FX and original archive
│   ├── manual-prices.json          # Active ten-cut worksheet; edit date/price and reload
│   └── manual-prices.template.json # Optional original blank worksheet; not loaded by the app
├── docs/
│   ├── manual-prices.md            # Entry workflow, units, machine names and recovery
│   ├── architecture.md             # Runtime, data and serving boundaries
│   ├── cuts-guide.md               # Qualified cut terminology and preparation context
│   ├── data-pipeline.md            # Sources, adapters, FX and observation contract
│   ├── artwork-prompts.md          # Artwork sources, prompts and dated display evidence
│   └── TRUTH-HARMONY.md            # Dated implementation and verification record
├── price_contract.py               # Automatic v2 validation, merge and atomic writes
├── official_prices.py              # Independent BLS, INDEC and valuation-FX attempts
├── ipcva_prices.py                 # IPCVA AMBA export and primary-source selection
├── bcra_fx.py                      # Direct BCRA USD quote means for IPCVA months
├── scrape-retail.py                # Source orchestration, catalog and USDA PDF adapters
├── fetch-prices.sh                 # Full explicit refresh; source-only modes run via Python
├── serve.sh                        # Loopback public-file launcher
├── serve_public.py                 # Live uncached manual route; other files use the public copy
├── fetch-beef.sh                   # Optional archival enrichment; not required by the page
├── tests/                          # Targeted source, contract, display and serving checks
│   └── fixtures/                   # Fixed historical snapshots and retained source examples
├── reports/                        # Historical review reports and optional proposals
├── research_notes/                 # Dated review/source-discovery evidence
├── roadmap.md                      # Implemented scope and optional future work
└── README.md
```

---

## Getting Started

### Prerequisites

- Modern web browser (Chrome, Safari, Firefox, Edge).
- Python 3.10+ for the local preview launcher and price pipeline.
- Optional tools for refreshing data or running checks:
  - `poppler` (`pdftotext` for USDA PDF ingestion): `brew install poppler`
  - Node.js (for running browser contract unit tests)

### Running the Web Application

Use the public-file launcher so the JSON route works and repository/private files stay outside the served directory:

```bash
./serve.sh
```

Open `http://127.0.0.1:8792`. Manual-price edits appear after saving and reloading the page. Stop with Ctrl-C and restart after changes to other files, which the launcher copies into a temporary directory. The server reads only the named manual-price file directly from the project, with caching disabled. Set `BEEF_CHART_PORT` to choose another port. Do not serve the repository root or rely on `file://` for JSON fetching.

The language toggle remembers the reader's preference in that browser and updates the URL. To open directly in Argentine Spanish, append `?lang=es-AR` to the page URL, before any `#section`; `?lang=en` opens English. An explicit URL choice wins over the saved preference. Storage is optional. Search includes both English and Spanish terms independently of the display language. Currency and measurement units remain the same in both languages; Spanish formats dates, decimals, percentages, native-price and FX displays for Argentina and labels dollar amounts, including chart ticks, as `US$`. Formatting rounds display only: USD amounts use two decimals, benchmark changes use one, and native amounts/FX use up to six consistently in tables, dossiers and evidence. Stored evidence stays unchanged.

Navigation accounts for the actual sticky-header height. At 600px and below, dense flow/price charts use initially open tables; entering that width opens the reader views without overriding manual choices while staying within it. An early-opened dossier shows a loading state and updates when prices arrive, preserving its focused control and reading position. A failed load shows a recovery explanation inside the dossier; a successfully loaded snapshot with no observation for that cut remains a distinct missing-observation state. Pecho and Cuadrada can display their own future Argentine catalog observations, with the same product/source qualifications; absent observations remain absent.

### Running Tests

Run only the regressions relevant to the change (no live providers). For the current manual-price and reload workflow:

```bash
node --test tests/test_manual_prices.cjs
PYTHONPATH=.:tests python3 -m unittest -q test_live_manual_server
```

These are 18 manual-price and seven HTTP-handler cases. The handler checks use in-memory connections; they do not start a listener or open a browser. For the broader cut-coverage/localization display pass:

```bash
node --test tests/test_price_coverage.cjs tests/test_ipcva_ui.cjs tests/test_harmony_ui.cjs tests/test_language.cjs tests/test_organ_unit_scale.cjs
```

Other focused source and earlier correction checks:

```bash
# C06 official-source isolation and the affected BLS/atomic-write regressions
PYTHONPATH=.:tests python3 -m unittest test_official_prices test_truth_harmony.TruthHarmony.test_bls_period_sorting_skips_m13_and_records_actual_previous test_truth_harmony.TruthHarmony.test_invalid_data_never_replaces_good_file

# Organ-price browser contract, when changing price display
node --test tests/test_organ_unit_scale.cjs

# Catalog sample evidence and shared dossier/table disclosure
PYTHONPATH=.:tests python3 -m unittest -q test_catalog_sampling
node --test tests/test_catalog_sampling.cjs

# Language selection, translations, formatting, and unchanged price qualification
node --test tests/test_language.cjs tests/test_organ_unit_scale.cjs tests/test_catalog_sampling.cjs

# October 13 correction regressions and affected evidence/recovery paths
PYTHONPATH=.:tests python3 -m unittest -q test_refresh_harmony test_official_prices test_organ_unit_scale test_catalog_sampling.CatalogSampling.test_failed_empty_and_replacement_preserve_observation_owned_evidence test_truth_harmony.TruthHarmony.test_cut_failures_do_not_block_healthy_cut_or_change_dates test_truth_harmony.TruthHarmony.test_invalid_data_never_replaces_good_file test_retail_prices.PriceMatching.test_alias_dedup_conversion_and_stock test_truth_harmony.TruthHarmony.test_uniform_unit_contract_for_all_cuts test_truth_harmony.TruthHarmony.test_species_and_prepared_products_fail_closed
node --test tests/test_harmony_ui.cjs tests/test_language.cjs tests/test_organ_unit_scale.cjs tests/test_catalog_sampling.cjs
```

### Refreshing Price Data

To execute a complete data refresh:

```bash
# Full explicit refresh (requires pdftotext and Python 3.10+)
./fetch-prices.sh

# IPCVA and its matching direct-BCRA monthly means only:
python3 scrape-retail.py --ipcva-only

# USDA advertised-feature PDF only:
python3 scrape-retail.py --usda-only

# Or targeted Carrefour scrape for specific cuts:
python3 scrape-retail.py --cuts bife_costilla molleja rinon lengua
```

Official and retail sources fail independently for classified transport, parsing and validation errors. Retail batches validate before merging; a malformed cut or USDA batch cannot prevent healthy batches from reaching the final write. A partial, empty-match or failed refresh saves healthy observations and dated attempt states, then exits nonzero. Carrefour summaries distinguish `ok`, `no_match`, `partial`, `error` and `partial_error`; inspect per-cut coverage. `ok` describes successfully obtained reference observations, not a current purchasable offer. INDEC native prices can advance with USD unavailable when matching monthly FX is missing. New catalog observations record bounded sampling evidence; a query limit hit means possible truncation, and a short response still has unknown coverage. Historical observations do not acquire invented query counts. Inspect source statuses and original observation dates before treating data as refreshed; see [the pipeline contract](docs/data-pipeline.md).

---

## License

There is currently no tracked LICENSE or completed asset/data-rights manifest. Code, images, and upstream data require separate provenance/use review; public access to a source is not blanket redistribution permission.

## Current correction evidence

The [correction record](docs/TRUTH-HARMONY.md) preserves dated scope and results; the [roadmap](roadmap.md) separates implemented features from optional extensions. C06/C14 source isolation and catalog sampling, shared semantic validation, IPCVA/BCRA ingestion, the USDA PDF repair, source-qualified cut coverage and manual quotes are implemented. The October 9 USDA PDF/text fixture and a successful 11-row source-only refresh are recorded; that establishes one checked layout, not continuing provider availability or acceptance of every report.

The current manual workflow passed 18 integration cases plus seven HTTP-handler cases. Earlier atlas/browser, pipeline and 46-case display results remain dated evidence, not checks rerun for every later edit. Three original organ observations remain withheld, and exact product equivalence, specialist anatomy/rights review, device/assistive-technology behavior and production acceptance remain open.

### Documentation guide

- [Manual prices](docs/manual-prices.md): the everyday edit → save → reload workflow and all machine names.
- [Architecture](docs/architecture.md) and [data pipeline](docs/data-pipeline.md): current implementation and data contracts.
- [Cut guide](docs/cuts-guide.md) and [artwork record](docs/artwork-prompts.md): terminology, illustration meaning and retained artwork evidence.
- [Truth and harmony](docs/TRUTH-HARMONY.md): chronological implementation and verification results. Old counts, hashes and limitations refer to the pass that recorded them.
- [Roadmap](roadmap.md): current scope and future options. Reports under `reports/` and their supporting `research_notes/` describe their reviewed dates/revisions; they are historical assessments and proposals, not current running instructions. Later changes are recorded in the current docs and correction record.

Historical review baselines: [October 9 market review](reports/Beef%20market%20professional%20review.md), [October 12 comprehensive review](reports/Beef%20chart%20comprehensive%20review.md), and [October 14 readiness review](reports/Beef%20professional%20readiness%20review.md). Their findings and supporting research notes retain their original review scope; current instructions and later implementation results are in the docs above.

## Manual prices

Enter local quotes in [`data/manual-prices.json`](data/manual-prices.json), using `date`, `item`, `machine_name`, numeric `price`, `currency` and `unit`. Argentine-market entries go under `ar`, U.S.-market entries under `us`. Supported examples: `"price": 18500, "currency": "ARS", "unit": "kg"` and `"price": 8.50, "currency": "USD", "unit": "lb"`. Ten Argentine cuts are prefilled with null dates and prices. Unfinished rows are skipped until both fields are filled. [Format and machine-name reference](docs/manual-prices.md).

Manual entries override display selection while preserving automatic and original Carrefour evidence. Scraper refreshes leave the manual file alone. Peso quotes retain native units without an assumed FX conversion. Save manual-price edits and reload the page; no server restart is needed. A server started before this feature was installed needs one restart to adopt it.
