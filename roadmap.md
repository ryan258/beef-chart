# Roadmap and evidence status

**English** · [Español (Argentina)](roadmap.es.md)

Status reconciled October 16, 2026. **Personal-reference v1 is complete within the bounded local scope below.** The project is a bilingual educational atlas and a personal retail-context reference, with low-effort entry of local quotes. The October 9, 12, and 14 reports in `reports/` are dated assessments and proposals. They do not make every professional extension below a requirement or an implemented feature.

## Personal-reference v1 finish — October 16

- **Return:** stable cut/language URLs, Copy cut link, and an explicit Resume last cut button. Unknown IDs recover to search; blocked storage does not prevent lookup.
- **Take away:** every dossier has a selectable, copyable butcher note with both reference names, existing relationship/preparation context and any selected valid manual quote in its original amount, unit and date. Clipboard denial selects the text for ordinary copying.
- **Understand:** Compare reaches prices, Read Value Shares opens its table, and the snapshot card summarizes source-owned periods independently of assembly. Detailed source/attempt qualifications remain available under Sources and methods.
- **Accepted local path:** bilingual search → dossier → note/link → close/reopen/resume; native keyboard focus and tab wrapping; desktop and 320px reader layout; temporary manual quote save/reload/clear through the real handler using an isolated file. Targeted checks passed; the [dated record](docs/TRUTH-HARMONY.md) names their scope and browser-tool limitations.

This closes the personal-reference implementation. Complete price coverage, verified original organ units, professional specifications/costing, full history, additional species and classroom modules are optional future work. Human assistive-technology/device, specialist and public-release acceptance remain distinct from this bounded local completion. Changes remain uncommitted; no publication is implied.

## October 15 follow-up (implemented)

- **IPCVA** is the primary AMBA monthly source for 22 covered beef rows. Matching direct-BCRA USD quote means have their own provenance, and original Carrefour observations keep their dates and FX.
- **USDA's October 9 PDF/text example** is retained, and its explicit October 3–15 advertisement-ending window parses without the release-page request that timed out. One source-only run accepted 11 observations. Unfamiliar future layouts and continuing provider availability remain unproven.
- **Bola de lomo** connects to its own IPCVA observation. All 24 dossiers expose coverage, so retained, missing, withheld, and manual values are visible, and every visual family labels sourced observations versus illustration. Product equivalence stays qualified.
- **Manual prices:** the active file holds ten prefilled ARS/kg cuts. Fill in date and numeric price gradually; unfinished rows are skipped. Valid owner quotes override only the display selection, while source observations and the original organ warnings remain available.
- **Reload:** saving a manual-price edit and reloading is enough, through the live uncached loopback route. Only a server running the older launcher needs one adoption restart; edits to other public files still need a restart.
- **Validation and recovery:** shared automatic semantic validation and same-source stale-input retention are in place. One previous observation plus the separate original-Carrefour archive give bounded recovery, not a complete immutable history.

The [manual guide](docs/manual-prices.md), [pipeline contract](docs/data-pipeline.md), [architecture](docs/architecture.md), and dated [verification record](docs/TRUTH-HARMONY.md) describe current behavior. The manual and reload checks passed 18 Node integration cases and seven Python HTTP-handler cases. Earlier, broader display checks and browser evidence stay tied to their own passes.

## Visual state, October 12–13, 2026 (implemented)

All 24 catalog cuts have transparent vintage halftone illustrations, used by six popular cards, four specialty cards, and the cut dossiers. Ribeye and sirloin are distinct. The cow hero and the pasture use matching halftone art, and SVG and PNG cow favicons are installed. The interactive cut-paper diagrams keep 20 Argentine cut controls and nine U.S. region controls, with full-name hover and focus readouts, keyboard activation, and hatched layer references. Maps stack through 800px, and narrow dossiers reserve room for the close control.

The [artwork record](docs/artwork-prompts.md) holds the retained prompts, asset mappings, sources, and desktop and mobile browser evidence. The artwork and diagram work kept cut identities, price mappings, chart colors, and teaching shares intact. The correction follow-up below then connected the previously omitted Pecho and Cuadrada series. Source rights and specialist anatomical acceptance are still open.

## October 13 correction follow-up (implemented)

- **Retail refresh boundaries:** recovery from incomplete HTTP responses is classified; nested catalog shapes are validated; each catalog and USDA batch is validated before merge; catalog health honestly reports no-match, partial, and error; incomplete refreshes exit nonzero.
- **Search and layout:** search indexes both languages whatever the display language; anchor offsets follow the measured sticky-header height; the search panel has contrasting focus (gold on the blue panel, ink inside the white box).
- **Loading states:** loading, ready, and unavailable are distinct, and the active dossier refreshes while preserving focus and scroll.
- **Prices and localization:** Pecho and Cuadrada price mappings; localized chart ticks, legend, percentages, table numbers, and new-record geography; matching 600px table-reader behavior; consistent gland-unspecified molleja copy.
- **Final review:** native amount precision is aligned across all evidence views, failed-load recovery stays distinct from absent observations, and the Other-value dialog keeps its canonical copy when the language changes.

That follow-up left the then-stored snapshot and artwork untouched; the October 15 source refreshes are separate work. Targeted evidence and residual limits are in [TRUTH-HARMONY.md](docs/TRUTH-HARMONY.md). It does not implement the later saved-state, butcher-card, source-history, or professional-workbench features.

## Phase 1: Truth and harmony (implemented)

Consistent rejection of catalog unit, species, and form mismatches. An explicit USDA effective-week contract, with unresolved layouts failing closed. Positive-value and date validation. Qualified legacy FX. Source and cut attempt states with retained references. Native prices when conversion is missing. Snapshot, status, and source context. Native dialogs with full directory and table alternatives. D3 and plugin isolation. Readable narrow-screen dossiers and table views. A 100-unit teaching flow with explicit value and radar semantics. Qualified anatomical names. Organ-price unit-scale qualification (*mollejas*, *riñón*, and *lengua* prices withheld, stored evidence retained). A safe loopback public launcher. Reconciled docs.

Also implemented: **C06**, independent BLS, INDEC, and monthly-FX attempts with per-source validation, retained observations, native-only INDEC recovery, and one atomic write; and **C14**, observation-owned catalog sampling evidence with consistent dossier and table disclosure, stating unknown legacy coverage and possible query truncation explicitly.

Validation and residual limits are in [TRUTH-HARMONY.md](docs/TRUTH-HARMONY.md). Deterministic and local browser checks are not professional, production, real-provider, device or assistive-technology, or WCAG acceptance. One October 9 USDA layout and one source-only run are recorded; other layouts and continuing live-source compatibility remain open. One previous observation is kept, and a complete history store is not implemented. Catalog pagination and delivery-region coverage are not implemented. Source and image rights and specialist crosswalk acceptance remain open. The original correction passes did not refresh prices, and the later IPCVA/BCRA and USDA refreshes preserve each observation's own date and evidence.

## Phase 2: An exceptional enthusiast reference

**Implemented:** bilingual operation (English / castellano porteño) through `assets/i18n.js` and the in-place header toggle, with Rioplatense voseo; a URL parameter (`?lang=es-AR` / `?lang=en`) that takes precedence over the optional `localStorage` preference; full-page dynamic translation across all 24 dossiers, diagrams, tables, and search feedback; accent-insensitive bilingual search with Argentine aliases; and preserved price evidence, numeric units, and organ-withholding invariants.

**Optional extensions beyond v1:** a reviewed, canonical catalog expansion; explained substitutes and comparisons; print-designed butcher cards; product-aware preparation and safety references; editable quantities; and saved multi-cut tasks. Basic cut links, resume and text notes are implemented above. *Extension exit test:* someone picks an unfamiliar cut, makes a request the butcher understands, reaches sourced preparation guidance, and resumes a saved multi-cut task with minimal re-entry.

## Phase 3: A practical professional workbench

Optional extensions that build on the owner-entered quote file: reviewed product specifications, qualified private supplier quotes, actual or explicitly assumed fabrication yield, usable-portion costing, and reproducible saved or exported scenarios. *Exit test:* a professional compares two real, qualified offers and independently reproduces the usable-cost decision.

## Phase 4: Dependable market context

Independent accepted adapters, original receipts, immutable observations and revisions, a chosen professional source for each of the U.S. and Argentine markets, and a reviewed current-FX transport and convention. *Exit test:* each adopted series reconciles to retained native source evidence and survives missing, revised, and error states without false comparability.

## Phase 5: Reviewed breadth and use

Selected nutrition, training, offline and print, import, and meaningful-change features, then chosen regions, species, or landed-cost needs. Expansion follows real task value and domain acceptance. A planned feature is not shipped evidence, and future scheduling, provider access, commits, pushing, and publication remain separate, owner-controlled actions.
