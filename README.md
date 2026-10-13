# The Cow, Two Ways (Beef Chart)

An interactive Argentine/U.S. beef atlas with a stored, mixed-source retail-price snapshot. It supports exploration and contextual comparison; it does not stream live prices or establish current supplier offers.

Built with a Bauhaus page layout, vintage halftone illustrations, Saul Bass-inspired cut-paper SVG maps, and D3.js visualizations. The artwork supports identification and exploration; it does not certify a product's anatomy, trim, or purchasing specification.

---

## Overview

Both traditions combine anatomical boundaries, local retail practice, and culinary uses. Names, trim, bone, and preparation vary; the paired schematics provide context rather than exact purchase specifications.

**The Cow, Two Ways** bridges these two worlds:

- **Interactive Cut Maps**: Twenty Argentine cut controls and nine U.S. region controls, with shared hover/focus highlighting, full-name readouts, keyboard activation, and a complete directory alternative. Hatched lomo, entraña, and peceto overlays identify layered references.
- **Illustrated Dossiers**: All 24 catalog entries have transparent halftone illustrations. Six popular-cut cards and four specialty cards use the same illustration set; ribeye and sirloin have distinct shapes. The cow portrait, pasture scene, and cow favicon complete the visual treatment.
- **English / Castellano porteño**: The header toggle translates the page, all 24 dossiers, chart/table labels, search feedback, and price qualifications. Spanish uses Rioplatense voseo and light lunfardo; U.S. names remain available as cultural references. Search accepts names in either language, with or without accents, plus aliases such as *ojo de bife* and *tira de asado*.
- **Stored Retail Context**: Dated observations normalized to USD per pound ($/lb). Source, geography, interval, product form, availability, and FX basis qualify comparison.
- **Advanced D3 Data Visualizations**:
  - **Sankey Flow Diagram**: Nine primal teaching allocations flow to culinary uses, including Other uses; 100 illustrative units in total.
  - **US vs Argentina Price Lollipop**: Mixed-source retail context by cut: USDA advertised features and BLS monthly averages for the U.S., Carrefour catalog medians and INDEC monthly averages for Argentina. Color identifies the country; it does not identify one uniform source or product.
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
| **AR** | **INDEC IPC-GBA** via `datos.gob.ar` | Monthly | Greater Buenos Aires retail averages (ARS/kg) |
| **AR** | **Carrefour Argentina Online Catalog** | On-demand; no schedule installed | Median raw butcher-counter offerings per kg, converted at latest returned BCRA observation |
| **FX** | **Banco Central (BCRA)** via `datos.gob.ar` | Matching monthly average for INDEC; latest returned daily observation for catalog | ARS per USD observation with per-record basis/date and recorded/inferred/unknown provenance |

Normalized output is consolidated in [`data/prices.json`](data/prices.json).

---

## Directory Structure

```
beef-chart/
├── assets/
│   ├── bauhaus.css                 # Contemporary Bauhaus overrides applied over index.html base
│   ├── cut_*.webp                  # 24 cut illustrations plus three card/dossier filename aliases
│   ├── hero_cow.webp               # Halftone cow portrait in the hero collage
│   ├── i18n.js                     # Authored English-to-Argentine-Spanish catalog and display helpers
│   ├── pasture_fence.webp          # Halftone pasture in the editorial quote card
│   ├── favicon.svg                # Cow icon with a cream background
│   ├── favicon-32.png             # 32px browser fallback
│   └── vintage_barn.webp           # Reserved artwork for future PDF charts, not referenced by page
├── data/
│   └── prices.json                 # Consolidated normalized price snapshot with per record FX basis
├── docs/
│   ├── architecture.md             # System architecture and component breakdown
│   ├── cuts-guide.md               # Butchery terminology and cut cross reference
│   ├── data-pipeline.md            # Pipeline APIs, scraper contract, and FX rules
│   ├── artwork-prompts.md          # Illustration prompts, SVG design, asset map, display evidence
│   └── TRUTH-HARMONY.md            # Correction scope, targeted evidence, and limits
├── reports/                        # Comprehensive and professional review reports
├── research_notes/                 # Supporting evidence notes across review passes
├── tests/
│   ├── test_catalog_sampling.py    # Offline catalog sample evidence and retention fixtures
│   ├── test_catalog_sampling.cjs   # Browser sampling contract, shared display text, escaping
│   ├── test_language.cjs           # Language selection, translations, formatting, and price independence
│   ├── test_harmony_ui.cjs         # Both-language search, price mappings, formatting, loading and dossier recovery
│   ├── test_refresh_harmony.py     # Retail transport/batch isolation and aggregate refresh health
│   ├── test_official_prices.py     # Offline official-source isolation and retention fixtures
│   ├── test_organ_unit_scale.cjs   # Node/DOM tests verifying organ price withholding and evidence display
│   ├── test_organ_unit_scale.py    # Python tests for organ unit-scale qualification and immutability
│   ├── test_retail_prices.py       # Unit tests for Carrefour matching, USDA parsing, and FX guards
│   └── test_truth_harmony.py       # Core qualification, merge, schema invariant, and error resilience regressions
├── price_contract.py               # V2 validation, qualification, and atomic promotion
├── official_prices.py              # Independent BLS/INDEC/monthly-FX fetch, parsing, and validated merge
├── serve.sh                       # Temporary public allowlist, loopback only
├── fetch-beef.sh                   # Optional archival BeefAPI fetcher, not required by page, needs .env
├── fetch-prices.sh                 # Entry command for independent official and retail attempts
├── scrape-retail.py                # USDA PDF parser and Carrefour catalog merger with atomic writes
├── index.html                      # Single page app with cows and D3 charts and modal
├── roadmap.md                      # Milestones and release status
└── README.md                       # Project overview
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

Open `http://127.0.0.1:8792`. Stop with Ctrl-C and restart after edits; the launcher copies the public files into a temporary directory. Set `BEEF_CHART_PORT` to choose another port. Do not serve the repository root or rely on `file://` for JSON fetching.

The language toggle remembers the reader's preference in that browser and updates the URL. To open directly in Argentine Spanish, append `?lang=es-AR` to the page URL, before any `#section`; `?lang=en` opens English. An explicit URL choice wins over the saved preference. Storage is optional. Search includes both English and Spanish terms independently of the display language. Currency and measurement units remain the same in both languages; Spanish formats dates, decimals, percentages, native-price and FX displays for Argentina and labels dollar amounts, including chart ticks, as `US$`. Formatting rounds display only: USD amounts use two decimals, benchmark changes use one, and native amounts/FX use up to six consistently in tables, dossiers and evidence. Stored evidence stays unchanged.

Navigation accounts for the actual sticky-header height. At 600px and below, dense flow/price charts use initially open tables; entering that width opens the reader views without overriding manual choices while staying within it. An early-opened dossier shows a loading state and updates when prices arrive, preserving its focused control and reading position. A failed load shows a recovery explanation inside the dossier; a successfully loaded snapshot with no observation for that cut remains a distinct missing-observation state. Pecho and Cuadrada can display their own future Argentine catalog observations, with the same product/source qualifications; absent observations remain absent.

### Running Tests

Run only the regressions relevant to the change (no live providers):

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
# Explicit monthly refresh (requires pdftotext and Python 3.10+)
./fetch-prices.sh

# Or targeted Carrefour scrape for specific cuts:
python3 scrape-retail.py --cuts bife_costilla molleja rinon lengua
```

Official and retail sources fail independently for classified transport, parsing and validation errors. Retail batches validate before merging; a malformed cut or USDA batch cannot prevent healthy batches from reaching the final write. A partial, empty-match or failed refresh saves healthy observations and dated attempt states, then exits nonzero. Carrefour summaries distinguish `ok`, `no_match`, `partial`, `error` and `partial_error`; inspect per-cut coverage. `ok` describes successfully obtained reference observations, not a current purchasable offer. INDEC native prices can advance with USD unavailable when matching monthly FX is missing. New catalog observations record bounded sampling evidence; a query limit hit means possible truncation, and a short response still has unknown coverage. Historical observations do not acquire invented query counts. Inspect source statuses and original observation dates before treating data as refreshed; see [the pipeline contract](docs/data-pipeline.md).

---

## License

There is currently no tracked LICENSE or completed asset/data-rights manifest. Code, images, and upstream data require separate provenance/use review; public access to a source is not blanket redistribution permission.

## Current correction evidence

See [the correction and review record](docs/TRUTH-HARMONY.md) for verification and [the roadmap](roadmap.md) for remaining work. C06 source isolation and C14 sampling disclosure are implemented and checked with offline fixtures. All 24 illustrations and the interactive diagrams have local desktop/mobile checks. The October 13 correction pass adds retail batch/transport isolation, truthful incomplete-refresh exits, independent bilingual search, header/focus/reader corrections and active-dossier loading recovery, with targeted regression and bounded browser evidence recorded in the correction log, including the final review follow-up. The bundled snapshot retains its old price values, observation periods, and FX dates; this work did not refresh prices. Live-provider compatibility, USDA real-layout acceptance, specialist anatomy/rights review, and production/device/AT behavior remain open.
