# Truth and harmony — local correction record

Records October 12–15, 2026. Each section preserves the scope, revision and evidence of its own pass. Historical statements about counts, hashes, source availability, uncommitted work and checks do not describe every later revision. The original October 12 scope excluded new feeds and price refreshes; later October 15 entries record IPCVA/BCRA integration, USDA repair, cut coverage, owner-entered quotes and reload-only manual edits. No passage authorizes staging, commits, pushing, deployment or publication.

## Current operating pointers — October 15

- Edit the ten prefilled cuts in [the active manual-price file](../data/manual-prices.json); date and price can be filled gradually. Unfinished rows are skipped. Numeric amount, currency and unit are separate fields.
- Save and reload for manual-price changes. A running pre-update server needs one restart to adopt the live route; copied HTML/assets/automatic-snapshot changes still need restarting.
- [Manual entry instructions](manual-prices.md), [architecture](architecture.md), [pipeline contract](data-pipeline.md), [cut qualifications](cuts-guide.md) and the [README](../README.md) describe current behavior.
- The most recent implementation checks were 18 manual-price cases plus seven HTTP-handler cases. The earlier 46-case display pass and browser evidence below remain dated results. The documentation reconciliation records static checks only; it does not rerun application acceptance.

## October 12 review and visual state

All current source, test, asset, and documentation changes were reviewed together before packaging. No blocking implementation regression was found in the reviewed paths. Documentation drift was corrected: the README no longer describes cut photography, the roadmap no longer says official monthly sources fail together, and the cut guide no longer presents map colors as a common anatomical key.

- C06 independent official-source recovery and C14 bounded catalog sampling are implemented. The bundled `data/prices.json` is unchanged from the start of these follow-ups, including all 36 observations and three organ unit-scale flags.
- All 24 cut IDs have transparent 1024 × 1024 illustrations. Six popular and four specialty cards use this set. Ribeye and sirloin are distinct; three paired filenames intentionally share artwork. The cow hero and pasture are opaque halftone illustrations. SVG and PNG cow favicons now resolve; the earlier missing-favicon note is historical.
- Cut-paper SVG maps provide 20 Argentine and nine U.S. controls, shared hover/focus highlighting, full-name readouts, permanent U.S. labels, and hatched layered references. Data identities, price connections, chart colors, and teaching shares were preserved. Prompts, source references, and detailed display evidence are in [artwork-prompts.md](artwork-prompts.md).
- Final targeted verification passed **36 Python tests and seven Node tests** covering official isolation, sampling, truth/retention/atomic-write contracts, organ-price withholding, and the existing alias/stock regression. No full suite or live provider request was run.
- All 24 dossier images were rechecked at 1280px and 320px: correct asset, successful decoding, contained layout, and no horizontal overflow. All 24 mapped images have transparent pixels and 1024 × 1024 dimensions. The narrow page retained all 36 price rows and exactly three withheld organ prices. Earlier 390px checks, all 29 map-region interactions, and native Enter/Escape focus restoration remain recorded in the artwork log. No console errors/warnings were reported in the final narrow run.
- Shell syntax, the no-network help route, bundled snapshot validation, inline JavaScript syntax, and whitespace checks passed. No Git submodules or gitlinks were found. An obsolete artwork contact sheet was preserved outside the repository rather than added as a site asset.

The combined graph review reports high risk across nine fetching/validation flows, which is why the targeted pipeline checks above are required evidence. Inline JavaScript is not resolved by the graph; source review and browser checks cover it. Existing documentation impacts are LOW; the new artwork log is UNKNOWN and its links/content were checked directly. A final `detect_changes` check precedes each logical commit. These results do not establish live-provider, specialist anatomical, rights, real-device/AT, other-browser, or production acceptance.

Repeat only the affected checks when needed:

```bash
PYTHONPATH=.:tests python3 -m unittest -q test_official_prices test_catalog_sampling test_truth_harmony test_organ_unit_scale test_retail_prices.PriceMatching.test_alias_dedup_conversion_and_stock
node --test tests/test_catalog_sampling.cjs tests/test_organ_unit_scale.cjs
```

## Implemented scope

| Review IDs | Result |
|---|---|
| C01–C02 | Same per-kg/unit/multiplier/raw-bovine contract across all catalog keys; unsupported offers fail closed |
| C03–C04 | Explicit current/prior intervals and publication separation; numeric collisions/layout drift fail. Real USDA layout acceptance remains unresolved |
| C05/C12 | Empty/error attempts retain original observations/dates; source/cut statuses and generation separated from retrieval; one prior observation on replacement |
| C06 | Independent official BLS/INDEC/monthly-FX and catalog-cut/USDA attempts, validated source merges and one atomic write. Official isolation added in the C06 follow-up below; live-provider acceptance remains open |
| C07–C11/C13 | Legacy FX recorded/inferred/unknown qualification, positive/date validation, real previous available BLS period, consistent inactive stock status, source/geography/method context |
| C14 | Per-query counts, eligible/selected listing counts, median population, first-seller evidence, unknown region and possible truncation recorded for new catalog observations; shared dossier/table explanations and honest legacy fallback |
| C15–C23 | Named native dialogs, unified close/restoration, full directory/chart tables, D3/plugin isolation, stacked narrow dossiers and table readers, candidate/no-result search |
| C25 | Public-file allowlist launcher on loopback; no repository/private paths in the served directory |
| C26–C32 | Honest docs, qualified crosswalks, conserved 100 teaching units, value-vs-yield wording, heuristic score tables, transparent recipe-search and cooking assumptions |
| E15 subset | Current architecture/pipeline/cut guide/roadmap and this bounded evidence record |

C14 sampling transparency is implemented in the follow-up below; catalog pagination remains bounded and coverage is never claimed exhaustive. C24 primal actions now show actual primal/context rather than arbitrary children, though full contextual gallery navigation remains limited to the featured list. Complete history, original receipts, specialist acceptance, rights, and owner-controlled release remain separate work.

## Impact evidence

Ryan restored the local GitNexus runtime and rebuilt the index. Python impacts were LOW: catalog_matches → carrefour_prices → main; usda_rows/wavg → usda_prices → main; get has catalog/USDA/main callers. Inline-JavaScript impacts returned UNKNOWN/target-not-found; actual boot, event, render, and dialog callers were confirmed from source before editing, and targeted browser regressions cover those boundaries. Test helper/method and new validator impacts were UNKNOWN with their actual import/validation/test callers confirmed in source. This is not a frontend graph all-clear. No reindex or commit graph gate was run by the agent.

## Validation

Targeted checks passed locally:

- 15 focused correction regressions in `tests/test_truth_harmony.py` (14 together, then the added qualification-type rejection case separately), plus four selected existing parser/matching/failure tests; no full suite or live sources.
- Shell syntax for launcher/orchestrator, inline JavaScript syntax, bundled v2 validation, and `git diff --check`.
- Chromium at 1440 px: 24 cut buttons, nine primal buttons, 29 named/focusable map paths, 36 price rows; flow total 100 and each primal's outgoing sum equals its teaching share.
- Named native retail dialog with background absent from the accessibility tree; explicit Tab/Shift-Tab wrap, Escape/restored card focus; Enter opens Cogote from the SVG path and Escape returns to that path. Source markup stays literal rather than creating injected elements.
- At 390 px: modal client/scroll widths both 364 px (previously clipped). At 320 px: document width 320 px, no horizontal overflow across all 24 cut dossiers or reader tables. Dense flow/price charts use the open table route.
- Temporary absence fixtures: no D3 retains directory/search/dialog/prices/36 rows; missing Sankey retains price/value charts and maps; missing or invalid JSON retains reference with unavailable data state. No uncaught application errors in those fixtures.
- Public-file launcher: `.env`, `.git/config`, scraper and report requests return 404. Standard assets and JSON load. The browser's automatic missing favicon request can return 404; this is not an app-runtime failure.

Screenshots were inspected for preserved desktop design and mobile dossier readability; they were not saved as review artifacts. Full suite, live-provider ingestion, real screen-reader/device/other-browser checks, production, printing, cold offline, and professional anatomical/culinary acceptance are not established by this local correction phase.

## Provider and data limits

The bundled 17 U.S./19 Argentine values, old periods, legacy fetched label and August 31 FX remain unchanged. Added qualifiers are metadata, including inferred legacy rates and unknown retrieval/publication/previous dates. Original source receipts were not invented. The organ-price follow-up below additionally withholds the three out-of-stock organ observations from comparisons while retaining their original evidence; their unusually low native values have an unverified cause.

The USDA report could not be retrieved: the research tool was inaccessible and a bounded direct retrieval failed DNS resolution. No accepted real-layout fixture was retained. Unrecognized intervals/columns retain existing evidence with an error state. Synthetic tests establish conservative parsing/date behavior and unresolved classification, not real-provider correctness.

## Organ-price unit-scale qualification — October 12 follow-up

Completed the focused follow-up for stored Carrefour molleja, rinon and lengua observations. Each now carries `unit_scale_unverified: true`. Cards and dossier price headings show **Price withheld**; the price table's ordinary USD/lb cell does the same. Dossiers and the table retain the amounts only as **Stored evidence only**, with the original date, out-of-stock status, FX lineage and explicit exclusion from price rankings, value comparisons and buying estimates until units and availability are verified. The shared price gate also excludes flagged records from the comparison chart and benchmark change calculation. The illustrative value treemap uses fixed teaching shares and does not consume observation prices.

The [owning methodology](data-pipeline.md) now includes the requested validation note and the optional boolean contract. Neither the original sale unit nor a per-100g/package explanation was inferred, and no scaling correction was applied. Removing the three new flags produces data identical to the pre-follow-up snapshot, including all 36 observations, original listings, values, dates, FX and generation/retrieval labels. A missing/false flag is not positive verification. Existing qualification, failed/empty attempts and previous-observation storage retain flags on the corresponding evidence; a new observation is separate from the flagged previous record.

Pre-edit impact: the index metadata recorded `2026-10-12T18:37:08.037Z`, and the five existing files involved matched its hashes before editing. The Hermes Node/GitNexus 1.6.12 runner worked. `validate_snapshot` was LOW: `write_snapshot` → scraper `main`, with the two snapshot-validation process paths. The file-level `index.html` result was LOW with one research-note import and no function/process coverage; this is not a frontend all-clear. `validPrice`, `priceLine`, `validatePrices`, `recordStatus`, `retainedPriceEvidence`, `priceBlock`, `renderPrices` and the new test class were UNKNOWN/not found. Source confirmed card/map-tooltip → priceLine, dossier → priceBlock, fetched validation → renderPrices/table/chart, and shared validPrice filtering before editing. The CLI reported that the sandbox prevented persisting its pruned global registry and continued with its in-memory view; graph results were returned. No reindex was run.

Actual focused verification:

- **4 Python regressions passed**: original organ values/listings/dates and flags; malformed flags cannot replace a snapshot; mocked empty/error attempts preserve all original evidence and flags; replacement retains the flagged previous observation.
- **4 Node regressions passed** against the actual inline price functions: no ordinary dollar/native fallback even after a stock/attempt-state change; labeled dossier evidence; all 36 table rows with exactly three withheld prices and consistent cards; malformed flag rejection in browser validation. Unflagged strip and absent-price behavior were also checked. These function tests use lightweight DOM/table stubs, not browser acceptance.
- Bundled Python validation, inline JavaScript syntax, the exact snapshot comparison above and `git diff --check` passed. Only the two new focused test files were run; no full suite or live source calls.
- Chromium at **1440px**: three withheld cards/table rows, bife de costilla still unavailable, other displayed prices retained. A temporary in-page fixture added all three organs to the chart's comparison rows: zero organ rows/points appeared, existing point count stayed 24, and the data remained identical afterward. The fixture was removed.
- Chromium mobile emulation at **390px and 320px**: all three dossier headings read Price withheld; modal client/scroll widths were 364/364px and 294/294px respectively. At 320px, all three evidence rows were 250/250px and document width stayed 320px. Desktop cards, the 390px Mollejas dossier and the 320px table were visually inspected. No stylesheet/design changes were needed.
- Actual Enter opened the named Mollejas native dialog; Escape closed it and returned focus to its initiating card. The accessibility tree included the withholding reason and retained evidence. No browser console errors/warnings were reported in this bounded run.

Repeat only these regressions when relevant:

```bash
python3 -m unittest discover -s tests -p 'test_organ_unit_scale.py'
node --test tests/test_organ_unit_scale.cjs
```

These are local synthetic/browser results, not original-unit verification, live-provider, real-device/screen-reader, WCAG or professional acceptance. At the end of this organ-price pass, USDA-layout, official-stage transaction, bounded-history, specialist-crosswalk and rights limits remained open; the C06 follow-up below resolves the official-stage transaction limit. The earlier correction package and untracked review/research artifacts were preserved. The organ-price changes were left unstaged and uncommitted; no price refresh, provider spending, scheduling, push, deployment or publication occurred.

## C06 official-source failure isolation — October 12 follow-up

Implemented independent BLS, INDEC and monthly-FX attempts in `official_prices.py`, retaining the same source endpoints, series and monthly conversion basis. `fetch-prices.sh` remains the entry command and invokes the existing scraper with `--official`. Python replaces the shell's shared curl/jq exit path; no new runtime dependency was added. BLS monthly ordering/previous-available behavior was moved with its existing regression. The internal `--official-snapshot` path remains supported with source-group validation and retail continuation after malformed input.

Official candidates validate before merge. Missing series and successful empty responses retain original observations with `no_match` coverage; failed/malformed sources retain their evidence with an error state. Healthy sources and downstream catalog/USDA attempts continue. INDEC native prices advance even if matching monthly FX is failed, empty, malformed or absent for their month, with null conversion/rate/date and unknown FX provenance. Cached monthly/daily rates are not substituted. Official `source_status` exposes complete configured-series coverage, partial/native-only results, and separate monthly/daily FX attempts. One existing atomic write saves the validated result; a non-success official source returns nonzero afterward. Complete failure retains every original observation, including dates, converted/native amounts, listings and unit-scale flags, while attempt/generation metadata can change.

Pre-edit state was clean at `4c9b3af`. GitNexus 1.6.12 reported its index four commits behind, but the source hashes for `fetch-prices.sh`, `scrape-retail.py`, `price_contract.py` and `tests/test_truth_harmony.py` matched the indexed content. Upstream impacts were LOW for scraper `main` (script entry caller, no resolved process membership) and `merge_records` (main and script entry, no resolved process membership). The shell entry, affected BLS test and new module/functions were UNKNOWN/not found; source confirmed the launcher → scraper → official attempts → existing merge/write path and unittest discovery. This is a qualified graph result, not an all-clear for new/shell code. No reindex, staging or commit gate was run.

Actual validation:

- **12 targeted tests passed**: nine new C06 integration/regression methods plus the moved BLS-period and existing atomic-rejection regressions (11 together), then one added transport-contract test. Tests block live `urlopen`; source responses are synthetic fixtures and writes go only to temporary files.
- Covered normal source updates, BLS failure with INDEC/catalog/USDA progress, INDEC failure with BLS progress, failed/empty/unmatched monthly FX, partial/missing series, successful empty sources, malformed numeric/date/shape/API responses, all-source failure, and malformed staged input. The new transport fixture checks BLS POST/year/series arguments, GET routes and timeout, and isolates malformed JSON. These checks do not establish provider acceptance.
- Integration fixtures validate the resulting v2 snapshot and assert exactly one final write. The all-source-failure fixture compares every original observation except explicit retention/attempt metadata; the organ flags remain intact. Successful replacements retain their previous observations and FX evidence.
- Shell syntax, the harmless `./fetch-prices.sh --help` route and `git diff --check` passed. No full suite or browser recheck was needed for the unchanged frontend.
- Final preservation hashes confirm `data/prices.json`, `index.html`, `assets/bauhaus.css`, and every report/research artifact are byte-for-byte unchanged from this pass's start.

Focused repeat command:

```bash
PYTHONPATH=.:tests python3 -m unittest test_official_prices test_truth_harmony.TruthHarmony.test_bls_period_sorting_skips_m13_and_records_actual_previous test_truth_harmony.TruthHarmony.test_invalid_data_never_replaces_good_file
```

This closes the local C06 official-stage isolation implementation, with source-level rejection of malformed batches and explicit missing-series coverage. Real-provider compatibility and original-source acceptance remain unverified; no live refresh was performed. C04's real USDA fixture, bounded history, specialist crosswalks, rights and human/device acceptance remain open. This pass leaves all changes unstaged and uncommitted and performs no push, deployment, publication, automation or provider spending.

## C14 catalog sampling transparency — October 12 follow-up

Added observation-owned `sampling` metadata to new Carrefour results without changing the matching, first-seller selection, alias deduplication or median calculation. Metadata records actual product counts per query, the requested limit, eligible and selected listing counts, available-listing versus out-of-stock-reference population, known selected seller IDs and missing-ID count, unknown delivery region, and `possibly_truncated` or `unknown` coverage. A response reaching the request limit is only possibly truncated; a shorter response does not establish completeness. There is no pagination or extra provider coverage in this pass.

Python and browser validators enforce the optional sampling shape, count relationships, supported population/seller policy and truthful limit-based coverage classification. A shared formatter supplies sampling text to dossiers and the existing price-table source/status column. Legacy records show their retained selected count/note where present and explicitly unknown historical query/coverage evidence. The bundled JSON is untouched; no missing original counts or regions were invented. The organ unit-scale flags and withheld headings continue to apply independently.

Pre-edit state included the unstaged/untracked C06 work at HEAD `4c9b3af`. GitNexus 1.6.12 metadata was indexed at `2026-10-12T19:12:18.367Z`; scraper, contract and inline-page hashes matched the index before editing. Upstream impact was LOW for `carrefour_prices` (scraper `main` and entry path) and `validate_snapshot` (official merge, atomic writer and scraper paths). Inline render/validation functions and new sampling/test symbols returned UNKNOWN/not found. Source confirmed fetch → validation → price table, both dossier price-block paths, the new helper call sites and test entry points. These unknown graph results are not an all-clear. No reindex or commit gate was run.

Actual focused verification:

- **15 targeted regressions passed:** six new Python sampling tests, the existing alias/stock calculation and atomic-rejection regressions (eight Python tests); three new Node sampling tests plus four existing organ-withholding tests (seven Node tests). The Python sampling tests block live `urlopen` and use mocked catalog responses; all writes use temporary files.
- Covered overlapping alias responses, pre-filter query counts, rejected listings, available-only selection, out-of-stock-only medians, empty alias responses, 19/20/21-result coverage classifications, first-seller selection, known/missing seller IDs, unknown region, malformed/contradictory sampling metadata, atomic rejection, legacy evidence, failure/empty retention and previous-observation preservation. Node tests execute actual inline functions and verify shared dossier/table text, escaping and unchanged organ suppression.
- Both inline scripts and the changed Python files passed syntax checks; bundled snapshot validation and `git diff --check` passed. An initial syntax-check extraction included an intervening HTML script tag; correcting the check to extract each script separately resolved that harness error without a source change.
- Bounded Chromium: all 36 price-table rows remained present, all 14 catalog rows showed legacy sampling uncertainty, and exactly three organ prices remained withheld. A temporary in-page synthetic sample exercised the new explanatory text at desktop 1440px and mobile 390/320px; at 390px the dossier width/scroll width was 364/364px, and at 320px it was 294/294px. The 320px table row and source/status cell were each 250/250px, with the sampling text present and no horizontal clipping. Desktop and narrow dossier screenshots were inspected; no stylesheet/design changes were needed. The browser harness was corrected to pass a cut object to the existing modal API and to reapply fixtures after viewport emulation reset the page.
- The final browser check reported no console errors/warnings. Temporary browser sample data was removed by reloading the local stored JSON; legacy uncertainty and three withheld prices were reconfirmed before stopping the preview server and clearing the test page. The browser tool cannot close its last tab.
- Preservation hashes verified 25 pre-existing data, asset, report/research and C06-only files unchanged from this pass's start, including the entire `data/prices.json`, stylesheet and official-source implementation/tests. Shared files retain the C06 changes. The new sampling tests are untracked; all changes remain unstaged and uncommitted.

Focused repeat commands:

```bash
PYTHONPATH=.:tests python3 -m unittest test_catalog_sampling test_retail_prices.PriceMatching.test_alias_dedup_conversion_and_stock test_truth_harmony.TruthHarmony.test_invalid_data_never_replaces_good_file
node --test tests/test_catalog_sampling.cjs tests/test_organ_unit_scale.cjs
```

This completes the bounded local C14 transparency correction. Tests do not establish actual retailer coverage, live transport compatibility, inventory, original organ units, real-device/screen-reader acceptance or professional acceptance. C04's accepted real USDA fixture and the other previously documented limits remain open. No full suite, live price refresh, new feeds, provider spending, scheduling, staging, commit, push, deployment or publication was performed.

## Bilingual operation (English / Castellano porteño) — October 12–13 follow-up

Implemented bilingual operation via `assets/i18n.js` and an in-place header toggle, providing full English and Castellano porteño (Rioplatense Spanish with voseo) presentation.

- `assets/i18n.js` defines the authored translation dictionary, string templates (`t`), locale selection (`locale`), and DOM translator `translateStaticPage()`. `usd` and `monthLabel` remain inline in `index.html`; the October 13 correction adds `formatNumber` and `currencyTick` to the translation module.
- `index.html` adds the accessible header language bar (`aria-pressed`, `aria-label`, visible focus), `data-i18n` attributes across static markup, and translated dynamic renderers (directories, cow maps, Sankey, scatter, treemap, radar, cut dossiers, search status, data tables, and price summaries).
- Cow map idle readouts and reset states translate on render and pointer reset.
- URL parameter `?lang=es-AR` / `?lang=en` takes precedence over optional `localStorage` preference; storage blockage does not prevent URL selection or in-page toggling.
- Presentation boundary guarantee: underlying price data in `data/prices.json`, numeric amounts, currency identities, measurement units ($/lb, ARS/kg), and organ withholding invariants (`unit_scale_unverified: true`) are never mutated by language switching. Spanish displays dollar amounts as `US$` with Argentine comma-decimal conventions and translates qualifications without modifying retained price evidence.
- Search accepts cut names, English equivalents, and local aliases (*ojo de bife*, *tira de asado*, *achuras*) in either language with accent insensitivity.
- `serve.sh` allows `assets/*.js` in the public loopback directory.
- Regressions in `tests/test_language.cjs` verify language precedence, denied storage fallback, translation coverage for all 24 cut dossiers and 9 primals, template interpolation/escaping, and immutable price/validator independence. Existing sampling and organ tests (`test_catalog_sampling.cjs`, `test_organ_unit_scale.cjs`) pass with `assets/i18n.js` integrated.

Focused repeat command:

```bash
node --test tests/test_language.cjs tests/test_catalog_sampling.cjs tests/test_organ_unit_scale.cjs
```

This completes the local bilingual operation pass. Tests do not establish native-speaker or assistive-technology acceptance across all screen readers or operating systems. All price evidence, official sources, and previous boundaries remain unchanged.

## October 13 correction pass

Implemented the bounded correction pass from the project review, leaving all changes unstaged and uncommitted.

- Retail recovery now classifies incomplete HTTP responses at daily-FX, catalog-cut and USDA boundaries. Response handles close on failed reads. Malformed nested catalog products/items/sellers/offers raise a classified `ValueError`; each catalog/USDA candidate batch validates before merge so a rejected batch cannot contaminate healthy staged results.
- Catalog aggregate health distinguishes `ok`, `no_match`, `partial`, `error` and `partial_error` with per-cut coverage. Requested catalog no-match outcomes, retail failures and empty USDA batches save qualified results/statuses and then exit nonzero. Updated existing empty-retention fixtures to assert this exit policy without changing their evidence-preservation expectations.
- Search uses a stable index of both English and Spanish equivalents plus aliases, independent of display language. The same query retains the same matching cut IDs after toggling.
- Sticky-header height supplies the anchor offset, including language/mobile wrapping. Blue-panel controls use contrasting gold focus. The 600px reader breakpoint matches CSS and opens tables on startup/entry while preserving manual choices within the same viewport range.
- Price loading has distinct loading/ready/unavailable states. A dossier opened before JSON arrival updates after loading, preserving the focused control and dossier scroll position. Pecho and Cuadrada now connect to their own Argentine series when observations exist; absent observations remain absent and cross-market relationships remain qualified.
- The legend, axis dollar ticks, unavailable chart text, benchmark percentage, numeric table cells, teaching shares, FX displays and new-record geography localize consistently. Molleja copy identifies sweetbreads with the gland unspecified rather than asserting thymus in the primary label. Stored values and currency/unit identities remain unchanged.
- README, architecture, pipeline, cut guide and roadmap now describe these boundaries. The obsolete Other-primals node and uniform USDA/Carrefour chart-source claims were corrected. Historical review reports remain dated evidence.

Pre-edit GitNexus impact reported LOW for `catalog_matches` and scraper `main`. Shared HTTP helper `get` was HIGH, with daily-FX, catalog and USDA callers; this was announced before editing. The request interface and 20-second timeout were retained, with response lifecycle and all three failure boundaries checked. Inline UI functions and unittest-discovered methods were UNKNOWN/not resolved; their boot/event/render/source callers were inspected directly. Ryan refreshed the index during this pass; no agent reanalysis was run. The subsequent change analysis reported HIGH risk across nine fetching/validation flows. Its inline-JavaScript and untracked-test coverage remains limited, so it is not a frontend all-clear.

Actual targeted verification:

- **28 Python tests passed:** eight new refresh-harmony tests, ten official-isolation tests, four organ tests, the sampling-retention test, the cut-failure and atomic-rejection tests, the alias/stock test, plus uniform-unit and species/prepared-product rejection checks. Network is blocked in the new fixtures; writes go to temporary files. Covered incomplete responses for all three retail boundaries, malformed nested and candidate batches, one final write, retained values/dates/organ flags, aggregate success/no-match/partial/error behavior and response closure.
- **18 Node tests passed:** five new harmony UI tests plus language, sampling and organ-price regressions. Covered both-language search, future mapped series without price borrowing, localized rendered evidence and unchanged values, loading/failure distinction, and active-dossier focus/scroll restoration. These use actual source functions with bounded DOM doubles; browser evidence is separate.
- Chromium desktop: identical search IDs in both languages; Spanish legend and `US$` axis ticks; comma-decimal benchmark; all 36 price rows and three withheld organ rows; unchanged in-memory price evidence after switching.
- At **320 × 740**, document width remained 320px, all 24 illustrated dossiers fit, and the explorer began at approximately 193px below a 181px sticky header, with its heading below the header. The gold search-result focus was visually inspected. Native Enter opened the named Mollejas dialog; Escape restored its initiating control.
- At **600 × 900**, the hidden dense charts had open reader tables; manually closing a table and toggling language preserved that choice. Synthetic Pecho/Cuadrada records connected to their own dossiers and were removed afterward.
- A delayed JSON browser fixture showed a loading message, then updated the open Lomo dossier to its stored price while preserving recipe-link focus and a 200px dossier scroll position. Invalid JSON produced a translated unavailable-chart/recovery state; runtime D3 absence retained search, directory and dialog access. No console errors/warnings were reported in these bounded checks.
- Inline/external JavaScript and shell syntax, bundled snapshot validation, current relative documentation links and whitespace checks passed. The bundled snapshot and artwork remain byte-for-byte unchanged. No full suite, live price refresh, paid provider run, staging, commit, push, deployment or publication was performed.

Repeat only the affected checks when needed; the README contains the combined targeted command. Current provider/real-USDA-layout compatibility, specialist anatomy/rights review, physical-device/screen-reader acceptance, print and cold-offline acceptance remain open. That pass used a copy-based preview. Current manual-price edits use the live reload route; copied HTML/assets/automatic-snapshot edits still require restarting.

## October 13 final working-tree review

Reviewed all 13 modified tracked files and both new test files against HEAD, including the existing correction diff, documentation and changed fixture expectations. Found and repaired four remaining UI inconsistencies:

- Native amounts used three fraction digits in dossiers/fallbacks/retained evidence but up to six in the table. All now share `formatNumber`, with the same display precision in both languages and unchanged stored amounts. USD and benchmark rounding remain two and one fraction digits respectively.
- A failed snapshot load produced a cut-level missing-observation message. Dossiers now show the load/validation failure and reload recovery; a ready snapshot without that cut's observation keeps its separate missing-observation explanation.
- The treemap Other-value dialog captured already-translated Spanish copy. Its renderer now passes canonical English strings to the reference dialog, allowing Spanish-to-English rerendering. Primal dialogs already regenerate from their canonical records.
- The blue-panel gold focus rule also reached the white search box. Controls on blue retain gold; the white input/button container now uses ink for a contrasting outline.

The final review left pipeline behavior intact and added explicit regressions for empty USDA batches and catalog FX dates incompatible with an observation. Both save healthy results in one write, retain affected evidence and report non-success as documented. README, architecture, pipeline and roadmap wording now matches the display precision, load recovery, canonical reference content and focus contexts. The architecture's public-file description now includes JavaScript assets.

Final targeted verification:

- **10 Python refresh-harmony tests passed**, covering all previously added retail recovery/health cases plus empty USDA and derived-FX rejection. Existing broader targeted results above remain dated evidence; no full suite or live providers ran in this review.
- **20 distinct Node checks passed** across harmony UI, language, organ and sampling tests. The initial run passed 19; the new isolated treemap test lacked tooltip callback stubs in its DOM/D3 harness. Adding those fixture stubs made its isolated retry pass. No application change was required for that harness failure, and passing unaffected tests were not rerun.
- Browser reproduced each UI issue before repair and verified the result afterward: Other-value text restores English; a six-decimal native amount agrees in table/dossier/fallback/evidence in both languages; failed-load dossiers show localized recovery. Temporary browser data was restored to the stored snapshot afterward, with 36 rows and three withheld organ prices.
- Actual window resize from 1200px to 600px, without reloading the document, opened all reader tables and hid the dense charts. Closing one table then resizing within the reader range to 550px preserved that choice.
- At 320 × 740, document width stayed 320px; the explorer heading stayed below the 181px header; focus outlines were ink on white and gold on blue. No console errors/warnings were reported in the final browser checks.
- Final source syntax, snapshot validation, documentation-link and whitespace gates passed. Stored price data and artwork remain unchanged; the staged diff is empty and all implementation/docs/test changes remain uncommitted. The review preview was stopped after verification.

GitNexus change review still flags the combined pricing diff HIGH across nine flows. Inline UI symbols and untracked test methods remain UNKNOWN/not resolved; direct source callers and bounded regressions cover the reviewed paths. No reanalysis, staging, commits, push, deployment or publication occurred. No further blocking inconsistency was found in this correction scope; the provider, specialist and human/device acceptance boundaries above remain open.

## October 14 R01 ambiguous search correction

Both header and quick-search Enter handlers now cancel the native key default before calling `filterAndOpenCut`. An ambiguous search can focus its first result without the same Enter activating that button. A separate Enter on a chosen result still opens its dossier. Matching, result order, translations, styling and stored price data are unchanged.

Pre-edit GitNexus impact ran through the recorded local CLI/runtime: `index.html` reported LOW file-level risk with one historical research-note reference and no reported processes. `filterAndOpenCut` was not found and reported UNKNOWN; direct source inspection covered the two Enter handlers, explicit search button and language re-render caller. File-level results do not establish inline-JavaScript graph coverage. The project wrapper timed out; no reindex was run.

Targeted verification on the local allowlisted preview:

- All 13 tests in `tests/test_harmony_ui.cjs` and `tests/test_language.cjs` passed. These existing checks cover bilingual matching and UI/localization contracts; native key defaults were verified separately in Chromium.
- Native Enter in **both inputs**, in English (`rib`) and Spanish (`lomo`), left both matching choices visible, focused the first result and opened no dialog. Tab then a separate Enter opened the intended second result; Escape closed it.
- Both inputs still opened unique English (`tenderloin`) and Spanish alias (`ojo de bife`) matches. Blank and no-match searches retained localized feedback with no result buttons or open dialog, checked across both inputs and languages.
- Both inline scripts passed JavaScript syntax checks. The browser reported no console errors or warnings, and `git diff --check` passed.

The preview was stopped after verification. This is bounded Chromium/local regression evidence, not a human assistive-technology or device acceptance claim. No full suite, provider refresh, staging, commit, push, deployment or publication was performed. Earlier review artifacts remain preserved.

## October 14 R30–R32 semantic validation correction

Implemented matching v2 semantic validation in Python and the browser, documented in `docs/data-pipeline.md`. Known AR conversions must reconcile with their observation-owned native/FX inputs and source rounding; known INDEC FX must match the observation month. Effective boundaries, source-aware future windows, typed ISO timestamps, enumerated attempt/evidence states, one-level previous observations and bounded nested metadata now validate before promotion or display. Legacy missing/null optional evidence remains unknown, native-only observations remain valid, and neither qualification nor validation invents receipts or dates. An October 15 promotion guard now keeps comparable older price and FX observations from replacing the stored latest values. It reports stale periods and retains the existing record, but it does not archive replayed price payloads or provide append-only revision history; full history remains open.

Pre-edit GitNexus impact was HIGH for `validate_snapshot`, `valid_period` and `validate_sampling`, covering official merges, retail batch validation and final writes. The warning was reported before edits. Browser functions were UNKNOWN/not found; direct source inspection covered the fetch/validate/catch/accept chain and date-display callers. Final structured change analysis reported HIGH across 11 flows, with no payload partial/truncated flags. Its hunk-based symbol mapping includes shifted neighbors; it does not establish coverage of new helpers, inline JavaScript or untracked tests. No reindex was run.

Targeted verification:

- `tests/fixtures/price_contract_v2.json` identifies semantic revision `v2-2026-10-14` and supplies **104 identical cases** to Python and the actual inline browser validator: 25 accepted compatibility cases and 79 malformed/contradictory cases rejected. Cases cover unknown legacy evidence, native-only values, rounding limits, monthly FX lineage, partial/prior/future intervals, offsets, previous evidence, statuses, listings and metadata limits. Both validators leave their inputs unchanged.
- **28 selected Python tests passed:** new contract cases, atomic rejection/preservation, official-source isolation, retail recovery and organ withholding. **23 selected Node tests passed:** shared contract cases, localization, sampling, organ withholding and existing UI contracts. No full suite or provider calls were run.
- Chromium loaded all 36 stored rows and withheld exactly three organ rows in English and Spanish; switching left in-memory evidence unchanged. An intercepted local response with a corrupt Lomo conversion produced the localized unavailable-data state in both languages, while the 24-cut directory and bilingual search remained usable. No console errors/warnings were reported.
- Python/inline-JavaScript syntax and `git diff --check` passed. `data/prices.json` stayed byte-identical: SHA-256 `8456a7dc30742a9d0d1492a0fd44dcb94923df3685e2887364d8bfc14a09db65`. No observation values, dates, FX inputs, legacy unknowns or unit-scale flags were rewritten.

The owned preview was stopped after verification. R01 and prior review artifacts remain preserved. All changes remain unstaged and uncommitted; no push, deployment or publication occurred. Live provider/layout, professional, rights and human assistive-technology/device acceptance remain outside this correction.

## October 15 cut coverage and visual evidence pass

Connected IPCVA's stored Bola de lomo observation to its dossier, keeping the generic U.S. round-roast context explicitly unverified as an exact product match. Expanded chart rows to include the connected cut observations previously omitted. Added a live-from-snapshot 24-cut coverage summary and bilingual table; missing country observations now remain visible in cards/tooltips/dossiers. Retained references have explicit text, hollow chart points, asterisks and dashed connectors; three unresolved organ prices stay withheld. The original Carrefour archive and all observation/FX dates remain intact.

Visible labels distinguish sourced price observations from the anatomical and cut illustrations, fixed-input flow/value models and editorial radar scores. The value chart explicitly states it does not use stored prices. GitNexus file impact reported LOW with one upstream file relationship; inline display functions remained UNKNOWN/not indexed. Direct callers were inspected across cards, map tooltips, modal lifecycle, resize, loading and language switching; UNKNOWN was not treated as a safety guarantee.

Verification: 28 selected Node checks cover coverage, source connections, retained chart styling, missing/native/withheld states, localization, original evidence preservation and modal refresh behavior. Inline JavaScript syntax and `git diff --check` also pass. The production snapshot remains 346,086 bytes with SHA-256 `287d323ab052066369a44280a19fab676f177430558d560c7e38a25d4099177d`; no provider refresh, browser/device/assistive-technology check, full suite, reindex or publication is claimed for this pass.

## October 15 manual price file

Added owner-edited `data/manual-prices.json` with separate `ar`/`us` arrays and six fields per quote: date, item, machine_name, numeric price, currency, unit. At that initial step, the manual file was empty; the later gradual-entry pass below prefills ten drafts. A pure client-side adapter validates entries and selects manual display overrides while preserving the automatic observation and original archive. Manual observations have visible bilingual labels and their own date/unit evidence; ARS/kg is not assigned a guessed exchange rate, and native USD/lb chart points carry a dagger. Missing automatic coverage can be filled for any dossier, including previously unmapped country connections. Invalid manual input falls back to the validated automatic snapshot with a visible message. Scraper-owned data is unchanged.

GitNexus file impact for the page remained LOW (one upstream file relationship); inline functions and the launcher remained unresolved/UNKNOWN. Callers were inspected directly across loading, cards, coverage, map tooltips, chart rendering, dossiers and language switching. This is not a graph all-clear. JavaScript/JSON/shell syntax and whitespace checks were performed; automated tests, provider refreshes, browser/device checks and publication were not run for this addition.


### Manual price numeric-field correction

Separated the owner-entered amount, currency and unit: `price` is a positive JSON number; `currency` is `ARS` or `USD`; `unit` is `kg` or `lb`. Supported pairs remain ARS/kg and USD/lb. The adapter rejects numeric strings, booleans, missing fields and unsupported combinations. Display normalization, date selection, source preservation and native-ARS behavior remain unchanged. The live file was empty, so no owner observations needed migration. Updated bilingual errors and all current examples. Syntax and whitespace checks only; no automated tests or browser checks were run for this correction.

### Targeted manual-price verification

Added `tests/test_manual_prices.cjs` and ran its 13 targeted cases together with the 28 neighboring coverage, IPCVA/original-source, modal, localization and organ-withholding checks: **41 passed, 0 failed**. The new cases exercise the production adapter, mocked-fetch file loader and display functions. Coverage includes numeric price/currency/unit validation, latest-date and equal-date selection, native ARS without inherited FX, USD/lb output, both display languages, cards/tooltips/dossiers/coverage/evidence rows, manual chart markers, missing country connections, original organ warnings, removal/restoration, HTML escaping, rejected manual files and rejection of an invalid automatic snapshot.

A full-snapshot case confirms every original Carrefour record, source ledger, source attempt and FX field survives loading and language rerendering unchanged, including the replaced automatic observations and their prior receipts. Both production files remained byte-for-byte unchanged: `data/prices.json` SHA-256 `287d323ab052066369a44280a19fab676f177430558d560c7e38a25d4099177d`; empty `data/manual-prices.json` SHA-256 `123f1dc3b2dd2d2c806685d5311d9bf06d28719762908d1bfde0a08b182add9b`. No application fixes were needed. These are local function/DOM-double/chart-callback checks; browser layout, real D3 rendering, device/assistive-technology behavior and live providers were not checked. No full suite or publication was run.


### Gradual entry in the active manual file

Prefilled `data/manual-prices.json` with the ten requested Argentine cuts, ARS and kg, leaving dates/prices null. The adapter now skips rows whose date or price is null, omitted, empty or whitespace-only. Such drafts never mask completed quotes or automatic observations. Once both values are supplied, all six fields and the existing numeric/date/unit/key rules are validated. Zero, false, negative values and numeric strings are not draft blanks; invalid completed rows still reject the manual overlay atomically. Non-object rows and unknown fields still reject.

Five new draft/gradual-completion cases and the prior targeted checks pass together: **46 tests, 0 failures**. Cases cover both markets, completed quotes mixed with drafts, one-field-at-a-time completion, clearing an override, correct error row numbers, strict completed-row validation and preservation of original observations, source ledgers, FX and organ withholding. Tests use in-memory draft worksheets so later owner edits to the active file do not invalidate fixed pending-row expectations. No browser, provider refresh or full suite was run. `data/prices.json` remains unchanged with SHA-256 `287d323ab052066369a44280a19fab676f177430558d560c7e38a25d4099177d`. The active manual file intentionally changed to hold the ten drafts. GitNexus adapter impact remained UNKNOWN/not indexed; the page's sole adapter call site was inspected directly.


### Reload-only manual-price edits

`serve.sh` now launches the standard-library `serve_public.py` helper. The public copy still supplies the page, assets and automatic snapshot, while only `/data/manual-prices.json` is opened directly from the project on each GET/HEAD request. Successful manual responses carry `Cache-Control: no-store`; the client already uses `fetch(..., {cache: 'no-store'})`. The route observes saves and atomic file replacement without restart and ignores conditional-cache dates. A server already running the previous launcher requires one restart to adopt this code; subsequent manual-price edits need only saving and reloading. Other public-file changes still need a restart.

The live file is read through non-following file/directory descriptors, checked as a regular file, and bounded to 256 KiB. Missing files return empty manual arrays. Symlink/nonregular replacements are refused, and other project/private paths remain outside the public copy. No source observations or manual drafts were edited by this change. GitNexus launcher impact remained UNKNOWN; its command and documented entry points were inspected directly.

Verification: **7 targeted Python HTTP-handler cases and 18 manual-price integration cases passed**. Handler cases use in-memory HTTP connections, checking successive saves, atomic replacement, cache headers, HEAD/query behavior, missing-file creation/removal, malformed file types, parent/file symlinks, bounded reads/recovery and public-only routes. Existing manual tests cover gradual completion and original source preservation. Shell/Python syntax and whitespace checks pass. Automatic and manual file hashes remain unchanged (`287d323ab052066369a44280a19fab676f177430558d560c7e38a25d4099177d` and `de1e5630b97a4a41e45cdda1815a4f78b8d074c9a65443c919c25824d3aebf94`, respectively). No browser, running-owner-server restart, live-provider request or full suite was performed.


### Documentation reconciliation after manual-price reload support

Reviewed all eight active Markdown documents (README, roadmap and the six files under docs). Updated the README, architecture, data pipeline, cut guide, manual entry guide, roadmap and this record to agree on the active ten-cut worksheet, numeric amount/currency/unit fields, draft skipping, original-source preservation, native ARS behavior and save/reload serving. Documented the one-time restart for an already-running old server separately from ongoing manual edits. The README now lists the IPCVA/direct-BCRA source path, source-only refresh commands, relevant files and targeted checks. Architecture and roadmap no longer claim the USDA example is unretained or manual quotes are entirely future work.

Historical report/research scope and dated verification counts/hashes remain historical evidence; the README links each review baseline and the current instructions. The artwork record was reviewed and its dated artwork checks remain applicable to their recorded pass. Documentation impact results were LOW for the resolved files (one to four upstream file relationships, no affected execution processes); the unindexed manual guide and ambiguous README lookup remain graph limitations and were checked directly through their content and links.

Static documentation checks passed: 66 local link targets across the eight active documents, the manual JSON example's numeric/six-field structure, all 25 market-key pairs against the catalog, balanced code fences and whitespace. External links were not re-fetched. No application tests, browser pass or source refresh was rerun for this documentation-only change; the most recent implementation checks remain the separately recorded 18 manual-price plus seven HTTP-handler cases. Both production price files remain unchanged.
