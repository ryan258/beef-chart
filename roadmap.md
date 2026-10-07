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
- [x] **D3 Sankey Flow**: Visualizes the anatomical yield progression from whole steer to primal divisions down to retail and specialty cuts.
- [x] **Tenderness vs. Price Scatter Plot**: Visualizes culinary value quadrant (high tenderness/low cost vs. premium cuts).
- [x] **Primal Yield Treemap**: Carcass volume and weight distribution across major carcass zones.
- [x] **Cut Profile Radar Chart**: Interactive radar visualization inside cut detail modals mapping tenderness, fat marbling, cooking speed, and grilling intensity.

### Phase 5: Specialized & Offal Cuts Expansion ✅
- [x] Introduced the "Beyond the usual cuts" section for traditional Latin American and specialty butcher offerings:
  - *Bife de costilla* (bone-in steak vs boneless strip/T-bone)
  - *Mollejas* (sweetbreads / thymus)
  - *Riñón* (beef kidneys)
  - *Lengua* (beef tongue)
- [x] Hardened Carrefour catalog scraper with strict unit multiplier checks, cross-species exclusions (avian/porcine/fish), and per-kg price validation.
- [x] Added automated test suite (`tests/test_retail_prices.py`) validating scraper parsing, unit enforcement, stock detection, and error preservation.

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
