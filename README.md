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
  - **Sankey Flow Diagram**: Primal-to-retail cut mapping across both traditions.
  - **Tenderness vs Price Scatter Plot**: Visualizing cost-efficiency and culinary suitability.
  - **Primal Yield Treemap**: Relative proportion and weight yield per carcass section.
  - **Sensory & Culinary Radar Charts**: Per-cut multidimensional profiles for tenderness, fat content, cooking speed, and heat intensity.
- **Specialized & Offal Cuts**: Dedicated tracking for cuts beyond standard steaks—including *bife de costilla*, *mollejas* (sweetbreads), *riñón* (kidneys), and *lengua* (tongue).

---

## Architectural & Design System

The front-end is crafted in a **Contemporary Bauhaus** visual language:
- **Grid Discipline**: Rigid 1px structural ink borders (`#20211e`), asymmetrical hero compositions, and modular data cards.
- **Primary Color Palette**: Bold primary accents (Bauhaus Red `#c73524`, Gold `#edc445`, Navy Blue `#234dba`, warm off-white canvas `#f1f0e8`).
- **Typography**: Paired modernist geometry (`Space Grotesk` headings, `Inter` body text).
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
| **AR** | **Carrefour Argentina Online Catalog** | On-demand / Weekly | Median raw butcher-counter offerings per kg |
| **FX** | **Banco Central (BCRA)** via `datos.gob.ar` | Daily / Monthly Avg | ARS per USD official exchange rate |

Normalized output is consolidated in [`data/prices.json`](data/prices.json).

---

## Directory Structure

```
beef-chart/
├── assets/
│   ├── bauhaus.css          # Contemporary Bauhaus design system & responsive overrides
│   ├── cut_*.webp           # High-resolution photographic assets for individual cuts
│   ├── hero_cow.webp        # Hero graphic assets
│   ├── pasture_fence.webp   # Thematic imagery
│   └── vintage_barn.webp    # Background & card artwork
├── data/
│   └── prices.json          # Consolidated normalized price data
├── docs/
│   ├── architecture.md      # Detailed system architecture & component breakdown
│   ├── cuts-guide.md        # Comprehensive butchery terminology & cut cross-reference
│   └── data-pipeline.md     # Pipeline documentation, APIs, and scraper specifications
├── tests/
│   └── test_retail_prices.py # Unit tests for scraper parsing and verification rules
├── fetch-beef.sh            # Ingestion script for BeefAPI v2 cuts metadata
├── fetch-prices.sh          # Pipeline orchestrator for BLS, INDEC, FX, and USDA/retail data
├── scrape-retail.py         # Resilient parser for USDA AMS PDFs and Carrefour catalog
├── index.html               # Main interactive single-page application
├── roadmap.md               # Milestones, release status, and upcoming roadmap
└── README.md                # Project documentation overview
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
