# Project Roadmap: The Cow, Two Ways

This document tracks completed milestones, architectural iterations, and planned future enhancements for the Beef Chart application.

---

## Completed Milestones

### Phase 1: Dual-Tradition Anatomical Core ✅
- [x] Defined foundational SVG paths for the bovine carcass.
- [x] Mapped American primal cuts (Chuck, Rib, Loin, Round, Flank, Plate, Brisket, Shank).
- [x] Mapped Argentine primals and subprimals (*Cuarto Delantero*, *Costillar*, *Cuarto Trasero*, *Vacío*, *Matambre*, *Nalga*, *Lomo*, etc.).
- [x] Bi-directional hover highlighting: hovering an Argentine cut illuminates corresponding US anatomical sections and vice-versa.
- [x] Modal inspection dialog with culinary descriptions, recommended cooking methods, and Spanish/English naming equivalents.

### Phase 2: Live Multi-Source Market Intelligence ✅
- [x] Automated BLS API v2 integration for monthly US national retail beef price benchmarks.
- [x] Automated INDEC IPC-GBA integration via `datos.gob.ar` API for Argentine peso prices.
- [x] Integrated Banco Central de la República Argentina (BCRA) monthly average foreign exchange series to normalize ARS/kg into USD/lb.
- [x] Automated USDA AMS weekly grocery store advertised feature PDF scraping using `pdftotext` extraction.
- [x] Live Carrefour Argentina catalog scraper (`scrape-retail.py`) targeting butcher-counter per-kilogram fresh beef items.
- [x] Consolidated atomic snapshot output in `data/prices.json`.

### Phase 3: Contemporary Bauhaus Visual Identity ✅
- [x] Full visual overhaul into a Contemporary Bauhaus aesthetic (`assets/bauhaus.css`).
- [x] Geometric layout with strict 1px ink structural borders, primary color accents (Bauhaus Red `#c73524`, Bauhaus Gold `#edc445`, Bauhaus Navy `#234dba`).
- [x] Modern typography scale using `Space Grotesk` for headlines and `Inter` for data density and body text.
- [x] Responsive layout refactoring with comprehensive breakpoints (1600px desktop grid down to 320px mobile).
- [x] Accessible UX enhancements: skip links, keyboard navigation focus indicators, and WCAG AA contrast compliance.

### Phase 4: Advanced D3 Data Visualizations ✅
- [x] **D3 Sankey Flow**: Visualizes primal divisions on the left to culinary uses on the right with distinct "Other primals" and "Other uses" nodes and resilient CDN fallbacks.
- [x] **D3 US vs Argentina Price Comparison**: Lollipop chart comparing retail price per lb across cuts with connecting range lines and store-weighted USDA vs Carrefour dots.
- [x] **Primal Yield Treemap**: Carcass volume and weight distribution across major carcass zones with fallback messaging.
- [x] **Sensory Radar Chart**: Six-axis interactive radar visualization inside cut detail modals mapping tenderness, marbling, flavor, cooking speed, sear crust, and gelatin.

### Phase 5: Specialized Cuts, Pipeline Hardening & Accessibility ✅
- [x] Introduced the "Beyond the usual cuts" section for traditional Latin American and specialty butcher offerings (*bife de costilla*, *mollejas*, *riñón*, *lengua*).
- [x] Hardened Carrefour catalog scraper with strict unit multiplier checks, cross-species exclusions, per-kg price validation, and explicit daily latest FX basis tracking.
- [x] Stored explicit FX basis per record: INDEC records use BCRA monthly average matched to the price month; Carrefour records use BCRA daily latest.
- [x] Enhanced anatomical interactive anatomy with synchronized dual-cow primal highlighting (`highlightPrimal`).
- [x] Implemented WCAG-compliant accessible modal dialog (`role="dialog"`, `aria-modal="true"`, focus trapping, focus restoration on close, Escape key handler).
- [x] Expanded test suite (`tests/test_retail_prices.py`) with 8 unit tests covering USDA AMS PDF parsing, store-weighted averages, non-conventional row filtering, stock detection, and FX basis guards.

---

## Upcoming & Future Work

### Phase 6: Historical Time-Series & Inflation Trends ⏳
- [ ] Implement historical price tracking with month-over-month and year-over-year percentage change graphs.
- [ ] D3 line chart displaying rolling 12-month price trajectory for key flagship cuts (*Bife de chorizo* vs *NY Strip*, *Asado* vs *Short Rib*).
- [ ] Inflation-adjusted price indexes comparing relative purchasing power across Argentina and the US.

### Phase 7: International Butchery Expansions 🔮
- [ ] **Brazilian Rodízio Cuts**: Add *Picanha* (tapa de cuadril/rump cap), *Fraldinha* (vacío), *Costela de chão*, and *Alcatra*.
- [ ] **French / European Cuts**: Cross-reference *Entrecôte*, *Faux-filet*, *Bavette d'aloyau*, and *Onglet*.
- [ ] **Japanese Wagyu Grading & Yield**: Compare A5 yield cuts (*Ichibo*, *Shin-shin*, *Zabuton*) against Western primals.

### Phase 8: Automation & Application Polishing 🔮
- [ ] GitHub Actions scheduled cron job to run `./fetch-prices.sh` monthly and commit updated `data/prices.json`.
- [ ] Bilingual UI toggle: Full Spanish / English interface translation switcher.
- [ ] Offline PWA support with service worker caching for offline butcher reference.
- [ ] High-resolution downloadable PDF butcher charts styled in the Bauhaus visual language.
