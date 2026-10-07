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
   - Side-by-side synchronized SVG diagrams representing the bovine carcass in Argentine cuts vs American primal cuts.
   - Live hover bus: hovering over an Argentine cut highlights the corresponding American cut region and updates the shared market card.
   - Action buttons triggering full inspection modals.

4. **Market Ticker & Search Hub (`.market-box`)**:
   - Live price overview card displaying selected cut pricing in USD/lb across both US and AR markets, alongside month-over-month price delta indicators.
   - Quick-tag search chips for instant selection of staple cuts.

5. **Advanced D3 Data Visualizations (`#data-sankey`, `#data-scatter`)**:
   - **Sankey Flow (`#sankey-chart-svg`)**: Multi-stage carcass flow diagram illustrating the path from live steer through primals into retail portions.
   - **Scatter Quadrant (`#scatter-chart-svg`)**: Relational plot comparing tenderness ratings against retail price per pound.
   - **Yield Treemap (`#treemap-chart-svg`)**: Proportionate area map illustrating carcass percentage yields.

6. **Popular Cuts Gallery (`#popular-cuts`)**:
   - Carousel-driven grid of high-resolution photographic cards with live pricing lines, meat characteristics, and click-to-inspect triggers.

7. **Specialized & Offal Cuts (`.extra-cuts`)**:
   - Grid dedicated to traditional Latin American culinary staples (*bife de costilla*, *mollejas*, *riñón*, *lengua*).

8. **Inspection Modal Dialog (`#cut-modal-overlay`)**:
   - High-fidelity modal presenting cut terminology, primal origin, cooking recommendations, price history, and a four-axis D3 radar chart.

---

## 3. Styling & The Contemporary Bauhaus System

The UI design is implemented in `assets/bauhaus.css`, extending the foundational CSS with Bauhaus design principles:

### Design Tokens

```css
:root {
  --bg: #f1f0e8;          /* Warm parchment background */
  --ink: #20211e;         /* Pure carbon ink for text and borders */
  --mut: #5b5d55;         /* Muted editorial secondary grey */
  --line: #cecec3;        /* Subtle divider borders */
  --line-dark: #92948b;   /* Emphasized structural borders */
  --red: #c73524;         /* Primary Bauhaus Red */
  --gold: #edc445;        /* Primary Bauhaus Gold / Ochre */
  --navy: #234dba;        /* Primary Bauhaus Ultramarine Navy */
}
```

### Visual Characteristics
- **Structural 1px Inking**: Distinct borders frame cards and sections without soft drop-shadows or gradients.
- **Strict Geometry**: Circular badges, rectangular panels, and triangular accents evoke early 20th-century functionalism.
- **Typography**:
  - `Space Grotesk` (weights 500, 600, 700) for high-impact headlines and numeric price callouts.
  - `Inter` (weights 400, 500, 600) for legible, dense tabular data and prose.

---

## 4. D3 Visualization Implementations

### D3 Sankey Diagram
- **Library**: `d3-sankey` (v0.12.3) via CDN.
- **Topology**: Steer -> Primal Division -> Subprimal Cuts.
- **Interactivity**: Path highlighting on link hover with tooltips showing yield percentages.

### D3 Scatter Plot
- **Axes**: X-axis (Tenderness Score 1–10), Y-axis (Price USD/lb).
- **Points**: Sized by culinary demand and colored by country of origin or primal section.
- **Interactivity**: Cross-highlights connected SVG cuts on the anatomical diagrams.

### D3 Sensory Radar Chart
- **Axes**: 4 radial axes (Tenderness, Marbling/Fat, Cooking Speed, Grilling Intensity).
- **Rendering**: Closed SVG polygon filled with semi-transparent accent color and interactive vertex handles.

---

## 5. Accessibility (a11y) & Performance

- **Fast First Paint**: Core application requires zero npm bundles or transpilation steps.
- **Accessibility**:
  - Skip link (`.skip-link`) anchors directly to `#explore`.
  - Full keyboard accessibility for modal dialogs (Escape to close, Tab trapping).
  - ARIA landmark roles and descriptive labels across interactive SVGs and buttons.
- **Reduced Motion**: `@media (prefers-reduced-motion: reduce)` disables smooth scrolling and animations.
