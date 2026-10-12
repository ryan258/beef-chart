# The Cow, Two Ways (Beef Chart)

An interactive Argentine/U.S. beef atlas with a stored, mixed-source retail-price snapshot. It supports exploration and contextual comparison; it does not stream live prices or establish current supplier offers.

Built with contemporary Bauhaus aesthetics, semantic HTML5, pure CSS layout systems, interactive SVG vector anatomical maps, and D3.js data visualizations.

---

## Overview

Both traditions combine anatomical boundaries, local retail practice, and culinary uses. Names, trim, bone, and preparation vary; the paired schematics provide context rather than exact purchase specifications.

**The Cow, Two Ways** bridges these two worlds:
- **Interactive Cut Maps**: Synchronized vector diagrams of Argentine vs American cuts with live cross-hover highlighting and detail inspection.
- **Stored Retail Context**: Dated observations normalized to USD per pound ($/lb). Source, geography, interval, product form, availability, and FX basis qualify comparison.
- **Advanced D3 Data Visualizations**:
  - **Sankey Flow Diagram**: Primal to culinary use flow with distinct Other primals and Other uses nodes.
  - **US vs Argentina Price Lollipop**: Retail price per lb by cut with store weighted USDA dots and Carrefour medians.
  - **Value Treemap**: Fixed illustrative retail-value allocation; not carcass weight, measured yield, or a current-price calculation.
  - **Editorial Radar**: Six heuristic trait scores; not measured sensory evidence or grades.
- **Specialized & Offal Cuts**: Dedicated tracking for cuts beyond standard steaks—including *bife de costilla*, *mollejas* (sweetbreads), *riñón* (kidneys), and *lengua* (tongue).

---

## Architectural & Design System

The front-end is crafted in a **Contemporary Bauhaus** visual language with base tokens in `index.html` refined by `assets/bauhaus.css`:
- **Grid Discipline**: Rigid 1px structural ink borders, asymmetrical hero compositions, and modular data cards.
- **Primary Color Palette**: Shipped base uses canvas `#f5f0e6` and ink `#141414` and red `#a82b2b` and gold `#e5a93c` and navy `#1a3e63`, with Bauhaus overrides in `assets/bauhaus.css`.
- **Typography**: Shipped page loads `Space Grotesk` and `Inter` plus `Oswald` for labels and `Playfair Display` for editorial quotes.
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
│   ├── cut_*.webp                  # Cut photography referenced by popular cuts grid
│   ├── hero_cow.webp               # Hero portrait referenced by hero collage
│   ├── pasture_fence.webp          # Editorial quote artwork
│   └── vintage_barn.webp           # Reserved artwork for future PDF charts, not referenced by page
├── data/
│   └── prices.json                 # Consolidated normalized price snapshot with per record FX basis
├── docs/
│   ├── architecture.md             # System architecture and component breakdown
│   ├── cuts-guide.md               # Butchery terminology and cut cross reference
│   ├── data-pipeline.md            # Pipeline APIs, scraper contract, and FX rules
│   └── TRUTH-HARMONY.md            # Correction scope, targeted evidence, and limits
├── reports/                        # Comprehensive and professional review reports
├── research_notes/                 # Supporting evidence notes across review passes
├── tests/
│   ├── test_organ_unit_scale.cjs   # Node/DOM tests verifying organ price withholding and evidence display
│   ├── test_organ_unit_scale.py    # Python tests for organ unit-scale qualification and immutability
│   ├── test_retail_prices.py       # Unit tests for Carrefour matching, USDA parsing, and FX guards
│   └── test_truth_harmony.py       # Core qualification, merge, schema invariant, and error resilience regressions
├── price_contract.py               # V2 validation, qualification, and atomic promotion
├── serve.sh                       # Temporary public allowlist, loopback only
├── fetch-beef.sh                   # Optional archival BeefAPI fetcher, not required by page, needs .env
├── fetch-prices.sh                 # Pipeline orchestrator for BLS and INDEC and FX and USDA plus retail merge
├── scrape-retail.py                # USDA PDF parser and Carrefour catalog merger with atomic writes
├── index.html                      # Single page app with cows and D3 charts and modal
├── roadmap.md                      # Milestones and release status
└── README.md                       # Project overview
```

---

## Getting Started

### Prerequisites

- Modern web browser (Chrome, Safari, Firefox, Edge).
- Optional tools for running the data ingestion scripts:
  - `jq` (JSON processor): `brew install jq`
  - `poppler` (`pdftotext` for USDA PDF ingestion): `brew install poppler`
  - Python 3.10+ (for `scrape-retail.py` and test suite)
  - Node.js (for running browser contract unit tests)

### Running the Web Application

Use the public-file launcher so the JSON route works and repository/private files stay outside the served directory:

```bash
./serve.sh
```

Open `http://127.0.0.1:8792`. Stop with Ctrl-C and restart after edits; the launcher copies the public files into a temporary directory. Set `BEEF_CHART_PORT` to choose another port. Do not serve the repository root or rely on `file://` for JSON fetching.

### Running Tests

Run the targeted correction regressions (no live providers):

```bash
# Python regression suite
python3 -m pytest tests/

# Browser contract tests
node --test tests/test_organ_unit_scale.cjs
```

### Refreshing Price Data

To execute a complete data refresh:

```bash
# Full monthly pipeline (requires curl, jq, pdftotext, python3)
./fetch-prices.sh

# Or targeted Carrefour scrape for specific cuts:
python3 scrape-retail.py --cuts bife_costilla molleja rinon lengua
```

---

## License

There is currently no tracked LICENSE or completed asset/data-rights manifest. Code, images, and upstream data require separate provenance/use review; public access to a source is not blanket redistribution permission.

## Current correction evidence

See [the phase record](docs/TRUTH-HARMONY.md) for targeted verification and remaining acceptance. The bundled snapshot contains metadata qualifications only; its old price values, observation periods, and FX dates are preserved. Complete USDA real-layout acceptance, production/device/AT behavior, and independent official-source refreshes remain open.
