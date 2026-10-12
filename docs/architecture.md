# Architecture and current behavior

Beef Chart is a zero-build static page combining a Bauhaus layout, vintage halftone artwork, interactive cut-paper cow maps, and D3 charts. It is an educational atlas and stored retail-context reference. Most frontend logic remains inline in `index.html`; `assets/bauhaus.css` supplies the active palette, layout, diagram styling, and responsive reader rules.

## Runtime boundaries

1. Embedded cut/primal records populate the full cut directory and search independently of D3.
2. Cow maps are progressive enhancement: 20 Argentine controls and nine U.S. region controls. Their paths expose names and Enter/Space activation; hover and focus update a full-name readout and highlight related regions across both maps. The directory provides a complete alternative.
3. Each chart checks its own dependencies. Missing Sankey affects the flow only. Missing D3 leaves search, dossiers, price text, and tables usable.
4. A single startup fetch loads `data/prices.json`. The frontend checks the v2 numeric/date/group contract before rendering; invalid/missing data gives a retry explanation without disabling the reference.
5. `FLOW_NODES`/`FLOW_LINKS` and `VALUE_MODEL` power both diagrams and tables. Flow totals 100 illustrative teaching units; the value model is fixed illustrative retail allocation. Neither is measured carcass yield or current valuation.
6. A native `<dialog>` isolates the background and handles the modal lifecycle. Button, Escape, and backdrop share close handling; each dossier has a visible/accessible title. Navigation inside a primal retains the original initiating focus for return.
7. On narrow screens, dense flow/price charts give way to readable table views. Dossiers stack their content and price evidence. Tables carry source/status/FX qualification; the radar has its own heuristic-score table.
8. Stored organ observations (*mollejas*, *riñón*, *lengua*) with `unit_scale_unverified: true` have their comparison and card prices withheld ("Price withheld") while retaining their amounts solely as "Stored evidence only" with explicit lineage notice.
9. Optional catalog `sampling` evidence is validated in both Python and JavaScript. `samplingContext` supplies the same bounded-sample explanation to dossiers and the price table, including unknown historical coverage when the metadata is absent.

Search is accent-insensitive and operates on names, aliases, and IDs. One result opens; ambiguous matches show choices; missing/empty queries explain recovery. Primal actions open an actual primal explanation rather than an arbitrary retail cut. Popular-card previous/next actions synchronize with the selected featured cut.

## Visual assets and diagrams

`CUT_IMAGE_MAP` connects every one of the 24 cut IDs to a transparent 1024 × 1024 WebP. `openCutModal` adds the illustration to regular and specialty dossiers. Six popular cards and four specialty cards use the same set. Chuck/aguja, strip/bife de chorizo, and sirloin/cuadril retain paired filenames with identical image content; ribeye and sirloin are distinct illustrations.

The cow portrait and pasture are opaque halftone WebPs. The hero uses a padded, contained circular frame; the pasture keeps its intentional partial circular crop, with space below quote text on mobile. SVG and 32px PNG cow favicons are declared in the page head. `vintage_barn.webp` remains unused by the page.

`renderCowSilhouette`, `renderCowMaps`, and `finishCowDrawing` build native SVG paths, decoration, and U.S. labels. The shared silhouette and region polygons use angular cut-paper geometry. `RETAIL_MAP_INKS` and `PRIMAL_MAP_INKS` control display colors independently of existing chart colors and teaching shares. Hatched lomo, entraña, and peceto references represent layers rather than exact surface boundaries. Decoration and permanent labels ignore pointer events; region paths retain the interactions. Maps stack through 800px. Small-region access remains available through the full-name directory.

The [artwork record](artwork-prompts.md) contains the asset map, retained prompts, anatomical reference links, and bounded browser evidence. Illustrations and schematics do not establish reviewed cutting specifications.

## Data operations

`fetch-prices.sh` invokes `scrape-retail.py --official`. The standard-library `official_prices.py` module attempts BLS, monthly FX and INDEC independently with the existing endpoints and series, validates each source before merging, and reports source status and complete configured-series coverage. Missing/failed sources retain original evidence; valid INDEC native observations can advance without a USD conversion when matching monthly FX is unavailable. The existing independent daily-FX, catalog-cut and USDA attempts still run after official failures. One final validated atomic write promotes the combined result; partial/empty/error official results produce a nonzero process exit after promotion. Targeted catalog refreshes and the internal local `--official-snapshot` import remain supported. The latter validates source groups independently but still runs retail network attempts.

`price_contract.py` supplies the minimal v2 qualification/validation/merge/atomic-write boundary. A replaced record retains one previous observation; empty matches and errors keep the original number/date with an inactive/failure qualification. This is bounded recovery, not a complete immutable history database. Source and cut attempt statuses are distinct from observation/retrieval/publication dates.

`serve.sh` copies only index, CSS/images, and prices into a temporary public directory and binds to `127.0.0.1`. The copy is static: restart after local edits. Repository, credentials, reports, private receipts, and optional BeefAPI caches are outside the artifact. `fetch-beef.sh` is optional archival enrichment and is not a visible glossary dependency.

## Scope and remaining acceptance

Local deterministic checks and bounded Chromium behavior are recorded in `docs/TRUTH-HARMONY.md`. They do not establish professional anatomical acceptance, production behavior, full WCAG conformance, Safari/Firefox/device operation, real screen-reader access, cold offline use, print quality, image/data rights, or live-provider correctness. USDA has no retained accepted real-layout fixture; unrecognized intervals/layout fail and its observations remain explicitly unverified. The project still uses external font/D3 assets and has no full historical store, supplier-quote engine, or costing workflow.
