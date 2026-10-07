# The Cow, Two Ways (Beef Chart)

An interactive, dual-perspective comparative exploration and live market price tracker contrasting Argentine (*asado*) and United States butchery traditions.

Built with contemporary Bauhaus aesthetics, semantic HTML5, pure CSS layout systems, interactive SVG vector anatomical maps, and D3.js data visualizations.

---

## Overview

The bovine carcass is partitioned according to deeply cultural and culinary logic. Where American butchery divides the animal along muscle and bone seams optimized for high-heat steakhouse grilling, braising, or smoking, the Argentine tradition follows anatomical muscle separations tailored for the parrillada and asado.

**The Cow, Two Ways** bridges these two worlds:
- **Interactive Anatomical Anatomy**: Synchronized vector diagrams of Argentine vs American cuts with live cross-hover highlighting and detail inspection.
- **Live Market Price Intelligence**: Real-time cross-border retail price comparisons normalized to USD per pound ($/lb), backed by public statistical agencies and live supermarket catalogs.
- **Advanced D3 Data Visualizations**:
  - **Sankey Flow Diagram**: Primal to culinary use flow with distinct Other primals and Other uses nodes.
  - **US vs Argentina Price Lollipop**: Retail price per lb by cut with store weighted USDA dots and Carrefour medians.
  - **Primal Yield Treemap**: Relative proportion and weight yield per carcass section.
  - **Sensory Radar Charts**: Six axis per cut profiles for tenderness and marbling and flavor and speed and sear crust and gelatin.
- **Specialized & Offal Cuts**: Dedicated tracking for cuts beyond standard steaks—including *bife de costilla*, *mollejas* (sweetbreads), *riñón* (kidneys), and *lengua* (tongue).

---

## Architectural & Design System

The front-end is crafted in a **Contemporary Bauhaus** visual language with base tokens in `index.html` refined by `assets/bauhaus.css`:
- **Grid Discipline**: Rigid 1px structural ink borders, asymmetrical hero compositions, and modular data cards.
- **Primary Color Palette**: Shipped base uses canvas `#f5f0e6` and ink `#141414` and red `#a82b2b` and gold `#e5a93c` and navy `#1a3e63`, with Bauhaus overrides in `assets/bauhaus.css`.
- **Typography**: Shipped page loads `Space Grotesk` and `Inter` plus `Oswald` for labels and `Playfair Display` for editorial quotes.
- **Responsive Architecture**: Multi-tier CSS grid and flexbox breakpoints supporting desktop (1600px+), tablet, and mobile down to 320px.
- **Accessibility (a11y)**: Complete keyboard navigation, visible focus rings, skip-to-content links, ARIA labels, and `prefers-reduced-motion` compliance.

---

## Data Pipeline & Sources

The project consumes multi-tiered public economic and retail datasets:

| Market | Source | Update Cadence | Metric / Basis |
|---|---|---|---|
| **US** | **Bureau of Labor Statistics (BLS)** | Monthly | National average consumer prices (USD/lb) |
| **US** | **USDA AMS Grocery Feature Survey** | Weekly | Store-weighted advertised retail features via parsed PDF |
| **AR** | **INDEC IPC-GBA** via `datos.gob.ar` | Monthly | Greater Buenos Aires retail averages (ARS/kg) |
| **AR** | **Carrefour Argentina Online Catalog** | On-demand / Weekly | Median raw butcher-counter offerings per kg, converted at daily latest BCRA rate |
| **FX** | **Banco Central (BCRA)** via `datos.gob.ar` | Monthly avg for INDEC plus daily latest for Carrefour | ARS per USD official rate stored per AR record with fx basis |

Normalized output is consolidated in [`data/prices.json`](data/prices.json).

---

## Directory Structure

```
beef-chart/
├── assets/
│   ├── bauhaus.css          # Contemporary Bauhaus overrides applied over index.html base
│   ├── cut_*.webp           # Cut photography referenced by popular cuts grid
│   ├── hero_cow.webp        # Hero portrait referenced by hero collage
│   ├── pasture_fence.webp   # Editorial quote artwork
│   └── vintage_barn.webp    # Reserved artwork for future PDF charts, not referenced by page
├── data/
│   └── prices.json          # Consolidated normalized price snapshot with per record FX basis
├── docs/
│   ├── architecture.md      # System architecture and component breakdown
│   ├── cuts-guide.md        # Butchery terminology and cut cross reference
│   └── data-pipeline.md     # Pipeline APIs and scraper and FX rules
├── tests/
│   └── test_retail_prices.py # Unit tests for Carrefour matching and USDA parsing and FX guards
├── fetch-beef.sh            # Optional archival BeefAPI fetcher, not required by page, needs .env
├── fetch-prices.sh          # Pipeline orchestrator for BLS and INDEC and FX and USDA plus retail merge
├── scrape-retail.py         # USDA PDF parser and Carrefour catalog merger with atomic writes
├── index.html               # Single page app with cows and D3 charts and modal
├── roadmap.md               # Milestones and release status
└── README.md                # Project overview
```

---

## Getting Started

### Prerequisites

- Modern web browser (Chrome, Safari, Firefox, Edge).
- Optional tools for running the data ingestion scripts:
  - `jq` (JSON processor): `brew install jq`
  - `poppler` (`pdftotext` for USDA PDF ingestion): `brew install poppler`
  - Python 3.10+ (for `scrape-retail.py` and test suite)

### Running the Web Application

Simply open [`index.html`](index.html) in any browser, or launch a lightweight static server:

```bash
# Python 3
python3 -m http.server 8000

# or with Node.js npx
npx serve .
```

Navigate to `http://localhost:8000` to interact with the chart.

### Running Tests

Execute the automated test suite for the price scraping engine:

```bash
pytest tests/test_retail_prices.py -q
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

MIT License. Open data derived from US BLS, USDA AMS, and Argentine INDEC/datos.gob.ar is subject to respective government open data policies.
