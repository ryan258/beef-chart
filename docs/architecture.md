# Architecture and current behavior

Beef Chart remains a zero-build static page with the current Bauhaus palette, typography, hero, cow maps, cards, and charts. It is an educational atlas and stored retail-context reference, not a live trading/procurement system. Most frontend logic remains inline in `index.html`; `assets/bauhaus.css` adds responsive and accessible-reader rules without a design replacement.

## Runtime boundaries

1. Embedded cut/primal records populate the full cut directory and search independently of D3.
2. Cow maps are progressive enhancement. Their paths expose names and keyboard activation; the directory provides a complete alternative.
3. Each chart checks its own dependencies. Missing Sankey affects the flow only. Missing D3 leaves search, dossiers, price text, and tables usable.
4. A single startup fetch loads `data/prices.json`. The frontend checks the v2 numeric/date/group contract before rendering; invalid/missing data gives a retry explanation without disabling the reference.
5. `FLOW_NODES`/`FLOW_LINKS` and `VALUE_MODEL` power both diagrams and tables. Flow totals 100 illustrative teaching units; the value model is fixed illustrative retail allocation. Neither is measured carcass yield or current valuation.
6. A native `<dialog>` isolates the background and handles the modal lifecycle. Button, Escape, and backdrop share close handling; each dossier has a visible/accessible title. Navigation inside a primal retains the original initiating focus for return.
7. On narrow screens, dense flow/price charts give way to readable table views. Dossiers stack their content and price evidence. Tables carry source/status/FX qualification; the radar has its own heuristic-score table.
8. Stored organ observations (*mollejas*, *riñón*, *lengua*) with `unit_scale_unverified: true` have their comparison and card prices withheld ("Price withheld") while retaining their amounts solely as "Stored evidence only" with explicit lineage notice.

Search is accent-insensitive and operates on names, aliases, and IDs. One result opens; ambiguous matches show choices; missing/empty queries explain recovery. Primal actions open an actual primal explanation rather than an arbitrary retail cut. Popular-card previous/next actions synchronize with the selected featured cut.

## Data operations

`fetch-prices.sh` stages official monthly BLS/INDEC/FX data. `scrape-retail.py --official-snapshot` merges those observations with the existing snapshot, retaining other sources and prior evidence. Targeted catalog refreshes remain supported. Catalog cuts and USDA are independent attempts after official staging; a blocked cut does not prevent another cut from advancing. The official BLS/INDEC/monthly-FX shell stage still fails as a unit before promotion if an official request fails: fully independent official adapters are deferred.

`price_contract.py` supplies the minimal v2 qualification/validation/merge/atomic-write boundary. A replaced record retains one previous observation; empty matches and errors keep the original number/date with an inactive/failure qualification. This is bounded recovery, not a complete immutable history database. Source and cut attempt statuses are distinct from observation/retrieval/publication dates.

`serve.sh` copies only index, CSS/images, and prices into a temporary public directory and binds to `127.0.0.1`. The copy is static: restart after local edits. Repository, credentials, reports, private receipts, and optional BeefAPI caches are outside the artifact. `fetch-beef.sh` is optional archival enrichment and is not a visible glossary dependency.

## Scope and remaining acceptance

Local deterministic checks and bounded Chromium behavior are recorded in `docs/TRUTH-HARMONY.md`. They do not establish professional anatomical acceptance, production behavior, full WCAG conformance, Safari/Firefox/device operation, real screen-reader access, cold offline use, print quality, image/data rights, or live-provider correctness. USDA has no retained accepted real-layout fixture; unrecognized intervals/layout fail and its observations remain explicitly unverified. The project still uses external font/D3 assets and has no full historical store, supplier-quote engine, or costing workflow.
