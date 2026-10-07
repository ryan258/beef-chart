# Architecture & Component Design

This document details the architectural layout, frontend rendering system, D3 data visualization modules, and styling architecture of **The Cow, Two Ways**.

---

## 1. System Overview

The project is structured as a zero-build, standards-compliant single-page web application (SPA) backed by pre-computed, atomically updated JSON datasets.

```
                      +-----------------------------+
                      |   Public Data Providers     |
                      |  (BLS, INDEC, USDA, BCRA,   |
                      |    Carrefour Argentina)     |
                      +--------------+--------------+
                                     |
                                     v
                       [ Ingestion Scripts ]
                 fetch-prices.sh + scrape-retail.py
                                     |
                                     v
                           data/prices.json
                                     | (fetch)
                                     v
                     +---------------+---------------+
                     |          index.html           |
                     |  - State & Data Layer         |
                     |  - Dual Cow SVG Diagrams      |
                     |  - D3 Visualizations          |
                     |  - Detail Inspection Modal    |
                     +---------------+---------------+
                                     |
                       [ Contemporary Bauhaus CSS ]
                         inline base + bauhaus.css
```

---

## 2. Frontend Structure

### HTML & DOM Hierarchy (`index.html`)

1. **Header & Navigation (`.site-header`)**:
   - Fixed, high-contrast navigation bar with inline cow brand mark.
   - Jump links to `#explore`, `#data-sankey`, `#data-scatter`, and `#about`.
   - Unified search filter (`#nav-search-input`) for instantaneous cut filtering.

2. **Hero Presentation (`.hero`)**:
   - Bold typographical Bauhaus composition with Space Grotesk headline.
   - Primary art quadrant featuring circular masked cow motif with Bauhaus geometric accents.
   - Quick navigational index bar highlighting the three core application pillars.

3. **Dual Anatomical Explorer (`#explore`)**:
   - Side-by-side SVG diagrams with retail Argentine cuts on the left and US wholesale primals on the right.
   - Live hover uses primal keys to add on and dim classes across both cows for anatomical correspondence.
   - Action buttons open the inspection modal for ribeye and strip reference cuts.

4. **Market Ticker & Search Hub (`.market-box`)**:
   - Ground beef benchmark card in USD per lb with month over month delta and null safe fallback text.
   - Quick-tag search chips for instant selection of staple cuts.

5. **Advanced D3 Data Visualizations (`#data-sankey`, `#data-scatter`)**:
   - **Sankey Flow (`#sankey-chart-svg`)**: Primal to culinary use flow with distinct Other primals and Other uses nodes.
   - **Price Lollipop (`#scatter-chart-svg`)**: US versus Argentina USD per lb by cut with connecting range lines.
   - **Yield Treemap (`#treemap-chart-svg`)**: Proportionate area map illustrating carcass percentage yields.

6. **Popular Cuts Gallery (`#popular-cuts`)**:
   - Carousel-driven grid of high-resolution photographic cards with live pricing lines, meat characteristics, and click-to-inspect triggers.

7. **Specialized & Offal Cuts (`.extra-cuts`)**:
   - Grid dedicated to traditional Latin American culinary staples (*bife de costilla*, *mollejas*, *riñón*, *lengua*).

8. **Inspection Modal Dialog (`#cut-modal-overlay`)**:
   - Dialog with aria modal behavior and focus trap and focus return and Escape to close.
   - Modal presents cut terminology and primal origin and cooking guidance and per source pricing with FX basis plus a six axis D3 radar chart.

---

## 3. Styling & The Contemporary Bauhaus System

The UI base lives inline in `index.html` with Bauhaus refinements in `assets/bauhaus.css`:

### Design Tokens

Shipped base in `index.html` uses canvas `#f5f0e6` and ink `#141414` and red `#a82b2b` and gold `#e5a93c` and navy `#1a3e63`. The Bauhaus override adjusts layout and borders and hero geometry. Single source edits should start from the inline base and mirror intentional changes into `assets/bauhaus.css` until the styles are consolidated.

### Visual Characteristics
- **Structural 1px Inking**: Borders frame cards and sections with Bauhaus overrides removing soft shadows.
- **Strict Geometry**: Circular cow disc and square accents plus triangular footer motifs.
- **Typography**:
  - `Space Grotesk` for headlines and price callouts.
  - `Inter` for body and tabular data.
  - `Oswald` for labels and chart text.
  - `Playfair Display` for editorial quotes and modal titles.

---

## 4. D3 Visualization Implementations

### D3 Sankey Diagram
- **Library**: `d3-sankey` (v0.12.3) via jsDelivr with unpkg fallback and unavailable messaging.
- **Topology**: Primals on the left to culinary uses on the right.
- **Interactivity**: Link hover tooltips showing carcass percent with distinct Other primals and Other uses labels.

### D3 Price Lollipop
- **Axes**: X-axis USD per lb with banded cut rows on the Y-axis.
- **Points**: Navy for Argentina and red for United States with range lines where both exist.
- **Interactivity**: Hover tooltips with source and period and USD per lb values.

### D3 Sensory Radar Chart
- **Axes**: 6 radial axes for tenderness and marbling and flavor and speed and sear crust and gelatin.
- **Rendering**: Closed SVG polygon with semi transparent fill plus web rings and spokes.

---

## 5. Accessibility (a11y) & Performance

- **Fast First Paint**: Core application requires zero npm bundles or transpilation steps.
- **Accessibility**:
  - Skip link (`.skip-link`) anchors directly to `#explore`.
  - Modal dialog uses role dialog and aria modal and labelled title plus Escape to close and Tab trap and focus return.
  - Charts show text fallback when D3 is unavailable and tooltips supplement SVG hover.
- **Reduced Motion**: `@media (prefers-reduced-motion: reduce)` disables smooth scrolling and animations.
