# The Cow, Two Ways (Beef Chart)

**English** · [Español (Argentina)](README.es.md)

An interactive atlas that sets Argentine and U.S. beef cuts side by side, with a stored, dated snapshot of retail prices and room for your own local quotes. It helps you explore and compare in context. It does not stream live prices, and it does not tell you what a supplier is offering today.

Argentine asado culture and the American steakhouse divide the same animal differently. Names, trim, bone, and preparation vary on both sides, so the maps and illustrations here are guides to *understanding* a cut, not purchasing specifications. The page pairs a Bauhaus layout with vintage halftone art, cut-paper SVG maps, and D3 charts.

---

## What you can do

- **Explore two maps of one cow.** Twenty Argentine cut controls and nine U.S. region controls share hover and focus highlighting, show full names, and work by keyboard. A complete directory is the alternative to the map. Hatching marks lomo, entraña, and peceto as layered references.
- **Open a dossier for any of 24 cuts.** Each has a halftone illustration, a cooking context, and its stored price evidence. Cards cover six popular cuts and four specialty cuts (*bife de costilla*, *mollejas*, *riñón*, *lengua*).
- **Return to a cut and take a note with you.** Every dossier has **Copy cut link** and a copyable **Butcher note** with both reference names, the existing relationship caution and preparation context. Valid selected manual quotes keep their native amount, unit and date. **Resume last cut** offers the last opened cut and its language when browser storage is available; it never opens an old cut automatically.
- **Read it in English or in castellano porteño.** The header toggle translates the whole page: dossiers, charts, tables, search feedback, and price qualifications. The Spanish uses Rioplatense voseo and a little lunfardo, and U.S. names stay visible as cross-references. Search understands both vocabularies, with or without accents, plus aliases such as *ojo de bife* and *tira de asado*.
- **Read prices with their context.** Every observation carries its source, geography, interval, product form, availability, and exchange-rate basis. Converted USD/lb values appear in the comparison chart; peso-only values stay in ARS/kg in the text and tables. A coverage summary shows which of the 24 cuts have an observation, a retained reference, a withheld price, a manual quote, or nothing.
- **Add your own local quotes.** Ten Argentine cuts are prefilled in [`data/manual-prices.json`](data/manual-prices.json). Add a date and a price, save, reload. Unfinished rows are ignored, and the automatic observations stay available underneath. See [Manual prices](docs/manual-prices.md).
- **Follow the bigger story with four D3 charts:**
  - **Sankey flow:** nine primal allocations flowing to culinary uses (100 illustrative units, not measured yield).
  - **U.S. vs. Argentina price lollipop:** USDA advertised features and BLS monthly averages against IPCVA survey prices, INDEC averages, retained Carrefour references, and optional manual quotes. Color identifies the country. Hollow dots and asterisks mark retained references; daggers mark manual USD quotes.
  - **Value treemap:** a fixed, illustrative retail-value split, not a price calculation.
  - **Editorial radar:** six heuristic trait scores, not sensory measurements or grades.

Three stored organ prices (*mollejas*, *riñón*, *lengua*) are withheld from comparison because their unit scales are unverified. The native values remain visible as labeled evidence.

### One animal, two vocabularies

| Argentina | United States | Careful with |
|---|---|---|
| Bife ancho | Ribeye | Bone-in or boneless, cap, trim |
| Bife de chorizo | Strip loin / NY strip | Not the same as a bone-in *costeleta* |
| Asado de tira | Cross-cut short ribs | Thickness and rib section matter |
| Vacío | Flank (partial overlap) | Not automatically a U.S. flank steak |
| Entraña | Skirt | Inside and outside skirt differ |
| Colita de cuadril | Tri-tip | Confirm trim |

The full table is in the [cuts guide](docs/cuts-guide.md).

---

## Design

The page is a **Bauhaus layout with vintage print illustration**. Base styles live in `index.html` and are refined by `assets/bauhaus.css`.

- **Grid:** 1px ink borders, asymmetric hero compositions, modular data cards.
- **Palette:** canvas `#f1f0e8`, ink `#20211e`, red `#c73524`, gold `#edc445`, blue `#234dba`. The maps use their own terracotta/ochre and muted blue/ochre inks and never change chart colors.
- **Type:** `Space Grotesk` and `Inter` for the page, `Oswald` for diagram labels, `Playfair Display` for dossier titles.
- **Artwork:** transparent 1024 × 1024 WebP cut illustrations, opaque halftone hero and pasture images, native SVG diagrams. Prompts, mappings, references, and display checks are in the [artwork record](docs/artwork-prompts.md).
- **Responsive:** CSS grid and flexbox breakpoints from 1600px+ down to 320px.
- **Accessibility:** visible focus, skip links, reduced-motion styles, full directory and chart tables, named native dialogs, failure isolation, and narrow-screen reader layouts are implemented. Full WCAG conformance and device/assistive-technology acceptance have not been verified.

---

## Data sources

| Market | Source | Cadence | What it measures |
|---|---|---|---|
| US | **Bureau of Labor Statistics (BLS)** | Monthly | National average consumer prices, USD/lb |
| US | **USDA AMS Grocery Feature Survey** | Weekly | Store-weighted advertised retail features, parsed from PDF |
| AR | **IPCVA consumer-price export** | Monthly | AMBA survey averages for 22 beef rows, ARS/kg; primary automatic source for the cuts it covers |
| AR | **INDEC IPC-GBA** via `datos.gob.ar` | Monthly | Greater Buenos Aires retail averages, ARS/kg |
| AR | **Carrefour Argentina online catalog** | On demand; no schedule installed | Median raw butcher-counter offers per kg, converted at the latest returned BCRA observation |
| FX | **BCRA direct USD quote history** | Matching completed months for IPCVA | Arithmetic mean of returned published USD quotes; distinct from the valuation-rate series |
| FX | **BCRA** via `datos.gob.ar` | Monthly average for INDEC; latest returned daily value for the catalog | ARS per USD, with per-record basis, date, and recorded/inferred/unknown provenance |

Automatic output is consolidated in [`data/prices.json`](data/prices.json), alongside separate Argentine source ledgers and the preserved original Carrefour archive. [Manual prices](data/manual-prices.json) are an independent display overlay that refresh scripts never write, and they require a valid automatic snapshot first. The [data contract](docs/data-pipeline.md) covers selection, dates, FX, and failure behavior.

---

## Project layout

```
beef-chart/
├── index.html                      # Cut catalog, search, validation, charts, dossiers
├── assets/
│   ├── bauhaus.css                 # Layout and responsive reader rules
│   ├── i18n.js                     # English / Argentine-Spanish catalog and formatting
│   ├── manual-prices.js            # Draft handling, validation, manual display selection
│   ├── reference-tools.js          # Cut links, optional resume storage, plain-text notes
│   ├── snapshot-summary.js         # Source-owned period summary, separate from assembly
│   └── *.webp / favicon*           # Cut, cow, and pasture illustrations; browser icons
├── data/
│   ├── prices.json                 # Automatic snapshot, source ledgers, FX, original archive
│   ├── manual-prices.json          # Active ten-cut worksheet: edit date/price and reload
│   └── manual-prices.template.json # Optional blank worksheet; not loaded by the app
├── docs/                           # Guides have Spanish editions (*.es.md); dated records do not
│   ├── manual-prices.md            # Entry workflow, units, machine names, recovery
│   ├── architecture.md             # Runtime, data, and serving boundaries
│   ├── cuts-guide.md               # Cut terminology and preparation context
│   ├── data-pipeline.md            # Sources, adapters, FX, observation contract
│   ├── artwork-prompts.md          # Artwork sources, prompts, dated display evidence
│   └── TRUTH-HARMONY.md            # Dated implementation and verification record
├── price_contract.py               # Automatic v2 validation, merge, atomic writes
├── official_prices.py              # Independent BLS, INDEC, and valuation-FX attempts
├── ipcva_prices.py                 # IPCVA AMBA export and primary-source selection
├── bcra_fx.py                      # Direct BCRA USD quote means for IPCVA months
├── scrape-retail.py                # Source orchestration, catalog and USDA PDF adapters
├── fetch-prices.sh                 # Full explicit refresh; source-only modes run via Python
├── serve.sh                        # Loopback public-file launcher
├── serve_public.py                 # Live uncached manual route; other files use the public copy
├── fetch-beef.sh                   # Optional archival enrichment; the page does not need it
├── tests/                          # Source, contract, display, and serving checks
│   └── fixtures/                   # Fixed historical snapshots and retained source examples
├── reports/                        # Historical review reports and optional proposals
├── research_notes/                 # Dated review and source-discovery evidence
├── roadmap.md                      # Implemented scope and optional future work
└── README.md
```

---

## Getting started

### Prerequisites

- A modern browser (Chrome, Safari, Firefox, Edge).
- Python 3.10+ for the local launcher and the price pipeline.
- Optional, for refreshing data or running checks: `poppler` for `pdftotext` (`brew install poppler`) and Node.js for the browser-contract tests.

### Run the app

Use the public-file launcher. It makes the JSON route work and keeps repository and private files outside the served directory.

```bash
./serve.sh
```

Open `http://127.0.0.1:8792`. Set `BEEF_CHART_PORT` to use another port. Stop with Ctrl-C.

- **Manual-price edits** appear after you save and reload. The server reads only that one file directly from the project, with caching disabled.
- **Any other edit** needs a restart, because the launcher serves a temporary copy of the rest. Do not serve the repository root, and do not rely on `file://`, which cannot fetch the JSON.

**Language.** The toggle remembers your choice in that browser and updates the URL. To open in Argentine Spanish, append `?lang=es-AR` before any `#section`; `?lang=en` opens English. A language in the URL wins over the saved preference, and storage is optional. Search covers both languages regardless of display language. Currencies and units are identical in both languages; Spanish formats dates, decimals, percentages, native prices, and FX for Argentina and writes dollar amounts as `US$`, including chart ticks. Display rounding never changes stored evidence: USD uses two decimals, benchmark changes one, and native amounts and FX up to six.

**Small screens and loading.** Anchor navigation accounts for the sticky header. At 600px and below, the dense flow and price charts open as tables first. A dossier opened before prices arrive shows a loading state, then updates in place while keeping your focus and reading position. A failed load explains how to recover; a successful load with no observation for that cut is shown as a distinct "missing" state. Pecho and Cuadrada can show their own future Argentine observations under the same qualifications.

**Cut links and copying.** A link such as `http://127.0.0.1:8792/?cut=vacio&lang=es-AR` opens that dossier directly. Closing the dossier removes the cut parameter; the optional resume button remains available beside search. Notes are readable and selectable in the dossier. If clipboard access is blocked, the copy action selects the text for your usual copy command. The snapshot card summarizes actual source periods separately from the assembly date; **Sources and methods** holds the detailed qualifications.

### Run the tests

Run only what your change touches. None of these contact live providers.

```bash
# Cut links, optional resume storage, butcher notes, snapshot summary and UI integration
node --test tests/test_reference_tools.cjs tests/test_snapshot_summary.cjs tests/test_v1_finish.cjs
```

```bash
# Manual prices and the reload route
node --test tests/test_manual_prices.cjs
PYTHONPATH=.:tests python3 -m unittest -q test_live_manual_server
```

That is 18 manual-price cases and seven HTTP-handler cases. The handler checks use in-memory connections: no listener, no browser.

```bash
# Cut coverage and localization display
node --test tests/test_price_coverage.cjs tests/test_ipcva_ui.cjs tests/test_harmony_ui.cjs tests/test_language.cjs tests/test_organ_unit_scale.cjs
```

Other focused checks:

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

### Refresh price data

Refreshing is always an explicit command. Opening the app never requests new prices.

```bash
# Full refresh (requires pdftotext and Python 3.10+)
./fetch-prices.sh

# IPCVA and its matching direct-BCRA monthly means only
python3 scrape-retail.py --ipcva-only

# USDA advertised-feature PDF only
python3 scrape-retail.py --usda-only

# Targeted Carrefour scrape for specific cuts
python3 scrape-retail.py --cuts bife_costilla molleja rinon lengua
```

Sources fail independently, and each batch is validated before it is merged, so one malformed cut or USDA batch cannot block healthy ones from the final write. A partial, empty-match, or failed refresh saves the healthy observations and dated attempt states, then exits nonzero. Carrefour summaries use `ok`, `no_match`, `partial`, `error`, and `partial_error`; check per-cut coverage. `ok` means reference observations were obtained, not that an offer is purchasable now. INDEC native prices can advance with USD unavailable when matching monthly FX is missing. New catalog observations record bounded sampling evidence: hitting a query limit means results may be truncated, and a short response still has unknown coverage. Historical observations do not gain invented query counts. Check source statuses and original observation dates before treating data as refreshed; the [pipeline contract](docs/data-pipeline.md) has the details.

---

## Manual prices

Enter local quotes in [`data/manual-prices.json`](data/manual-prices.json) using `date`, `item`, `machine_name`, a numeric `price`, `currency`, and `unit`. Argentine-market entries go under `ar`, U.S.-market entries under `us`.

```json
{ "price": 18500, "currency": "ARS", "unit": "kg" }
{ "price": 8.50,  "currency": "USD", "unit": "lb" }
```

Ten Argentine cuts are prefilled with null dates and prices; a row is skipped until both are filled. A manual entry overrides what is *displayed* for that cut, while automatic observations and the original Carrefour evidence are preserved. Peso quotes keep their native units with no assumed conversion. Save and reload; no restart is needed. A server started before this feature existed needs one restart to adopt it. [Format and machine-name reference](docs/manual-prices.md).

---

## Status and records

**Official v1 release as of October 16, 2026**, establishing the complete personal-reference atlas within the local lookup, note/link, resume and manual-quote workflow recorded in the roadmap. Professional extensions and broader acceptance remain optional and separately scoped.

The [correction record](docs/TRUTH-HARMONY.md) preserves dated scope and results; the [roadmap](roadmap.md) separates what is implemented from optional extensions. Implemented so far: C06/C14 source isolation and catalog sampling, shared semantic validation, IPCVA/BCRA ingestion, the USDA PDF repair, source-qualified cut coverage, and manual quotes. One October 9 USDA PDF/text fixture and one successful 11-row source-only refresh are recorded. That establishes one checked layout, not continuing provider availability or acceptance of every report.

The current manual workflow passed 18 integration cases plus seven HTTP-handler cases. Earlier atlas, browser, pipeline, and 46-case display results are dated evidence, not checks rerun after every later edit. Still open: exact product equivalence, specialist anatomy and rights review, device and assistive-technology behavior, the three withheld organ observations, and production acceptance.

### Where to read next

- [Manual prices](docs/manual-prices.md): the everyday edit → save → reload workflow and every machine name.
- [Architecture](docs/architecture.md) and [data pipeline](docs/data-pipeline.md): how it works and the data contracts.
- [Cuts guide](docs/cuts-guide.md) and [artwork record](docs/artwork-prompts.md): terminology, illustration meaning, retained artwork evidence.
- [Truth and harmony](docs/TRUTH-HARMONY.md): chronological implementation and verification results. Counts, hashes, and limitations refer to the pass that recorded them.
- [Roadmap](roadmap.md): current scope and future options.

Reports in `reports/` and their `research_notes/` are historical assessments tied to their review dates: [October 9 market review](reports/Beef%20market%20professional%20review.md), [October 12 comprehensive review](reports/Beef%20chart%20comprehensive%20review.md), and [October 14 readiness review](reports/Beef%20professional%20readiness%20review.md). Current instructions and later results live in the docs above.

## License

There is currently no tracked LICENSE or completed asset/data-rights manifest. Code, images, and upstream data need separate provenance and use review; public access to a source is not blanket permission to redistribute it.
