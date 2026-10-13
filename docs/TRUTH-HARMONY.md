# Truth and harmony — local correction record

October 12, 2026. Records the first correction phase, C06/C14 follow-ups, and the illustrated atlas update. The sections below preserve the evidence and limits of each pass; historical statements about uncommitted work or earlier visuals describe that pass, not the current repository state. The final review and documentation reconciliation prepare this work for Ryan-authorized local commits. No push, deployment, live price refresh, new feed, account, or costing engine is included.

## Current review and visual state

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

- `assets/i18n.js` defines the authored translation dictionary, string templates, number/date formatting helpers (`usd`, `monthLabel`, `t`, `locale`), and DOM translator `translateStaticPage()`.
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
