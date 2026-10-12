# Product standards, market evidence, and exceptional dual-audience workflows

Research date: October 12, 2026, America/Chicago. This is a bounded primary-source review supporting the comprehensive project review. Read local README, cuts guide, price snapshot, and previous market research as background; reverified material sources below. No project data refresh, authenticated API call, paid source, implementation, or external publication occurred. A readable reference page demonstrates page access only; it does not demonstrate adapter readiness, current data delivery, redistribution permission, or workflow adoption. Recommendations are proposed scope, not shipped capability. The professional audience is explicitly requested; monetization, trade execution, and a broad futures platform are not assumed.

## 1. What authoritative identities and market evidence would make the existing US–Argentina comparison trustworthy?

### Takeaway

The strongest foundation is a versioned bilingual beef/specification registry paired with source-specific price observations. Unit and currency conversion should preserve evidence while exposing anatomical, quality, geography, channel, and time mismatches; it cannot make different products or market stages equivalent.

### Cited Findings

- USDA AMS maintains voluntary Institutional Meat Purchase Specifications used by foodservice and institutional buyers. Its catalog separates adopted series from drafts, including Fresh Beef 100 and Variety Meats 700, and provides Spanish series. Pin the actual published version rather than accidentally adopting the 2020 draft as current. [IMPS catalog](https://www.ams.usda.gov/grades-standards/imps); [published Fresh Beef Series 100](https://www.ams.usda.gov/sites/default/files/media/IMPS_100_Fresh_Beef%5B1%5D.pdf).
- SENASA Resolution 1128/1999 approves a bovine nomenclador covering basic cuts, variants, codes, location, and preparation. Its original annex distinguishes Vacío 2471, a collection of abdominal-wall muscles/fascias, from Bife de vacío 2472, the fleshy rectus-abdominis portion. It also identifies Molleja 607 as thymus with cervical/thoracic portions, and Entraña Gruesa 601 as diaphragm pillars. These are useful identity records, not universal culinary recipes or proof that a particular retailer SKU conforms. This review did not establish all later amendments or certify present statutory completeness. [Original resolution and annex](https://www.argentina.gob.ar/normativa/nacional/resoluci%C3%B3n-1128-1999-60581/texto).
- USMEF Sudamérica's country dictionary lists Argentine Entraña Fina against Outside Skirt (Diaphragm), Falsa Entraña against Inside Skirt, and Entraña Gruesa against Hanging Tender. Its table also separates Bife de Vacío from Vacío and warns names/despiece can vary with suppliers. This directly conflicts with the local guide's “entraña fina (inside skirt)” statement. [USMEF country dictionary](https://usmefsudamerica.org/corte-de-res/); [local guide](/Users/ryanjohnson/Projects/beef-chart/docs/cuts-guide.md).
- INAC offers a 2023 bovine cutting manual and other-species manuals. INAC is Uruguayan: useful regional technical support, not the Argentine nomenclador authority. [INAC manuals](https://www.inac.uy/innovaportal/v/9878/2/innova.front/manuales-de-cortes).
- USDA quality and yield grades are separate concepts: quality predicts palatability, while yield concerns closely trimmed boneless retail cuts from specified major wholesale sections. Neither is a universal cooking yield nor a translation of Argentine quality classes. [USDA carcass standard](https://www.ams.usda.gov/sites/default/files/media/CarcassBeefStandard.pdf).
- BLS average food prices are monthly price-level estimates from eligible CPI observations, rather than a CPI index. Food prices exclude sales tax and published averages exclude delivery/handling/shipping. Detailed product definitions matter; for example “regular 100% ground beef” and “lean/extra lean” are different series. [BLS average-price methodology](https://www.bls.gov/cpi/factsheets/average-prices.htm).
- USDA grocery feature reports cover weekly advertised prices from major supermarket outlets, gathered primarily from public retailer websites. They are an advertising sample, not realized nationwide purchases. [AMS grocery feature reports](https://www.ams.usda.gov/market-news/grocerystore).
- INDEC publishes average selected-item IPC prices for regions and GBA. The current readable landing page lists series through August 2026. Do not label a GBA series as all-Argentina retail merely because the wider IPC has national coverage. [INDEC IPC datasets](https://www.indec.gob.ar/indec/web/Nivel4-Tema-3-5-31).
- USDA's LM_XB403 boxed-beef report example labels figures USD per 100 lb, using negotiated cut prices and volumes delivered within 0–21 days and industry cutting yields. A cutout is calculated, not an individual retail price or an actual carcass supplier quote. [Official report example, February 18, 2026](https://mymarketnews.ams.usda.gov/filerepo/sites/default/files/2453/2026-02-18/1305325/ams_2453_01525.pdf); [cutout methodology](https://www.ams.usda.gov/sites/default/files/media/LMRBoxedBeefCutoutsUserGuide.pdf).
- SIO Carnes exposes operation-date, zone and animal/category filters. Its price-summary page explicitly excludes operations recorded as kg meat. The monitor explained methodology but rendered “Sin datos” in this read: that is not zero price and not proof that the system has no observations. [SIO price summary](https://siocarnes.magyp.gob.ar/GrillaSIOCarnes/ResumenPrecios?animal=BOVINO&idAnimal=1); [SIO monitor](https://siocarnes.magyp.gob.ar/MonitorSioCarnes/MonitorSioCarnes?animal=BOVINO&idAnimal=1).
- MAG's current public site calls its replacement indices INMAG and IGMAG, succeeding INML and IGML. Its October 12 landing state showed zero arrivals and missing index cells: interpreting that as price zero would be invalid. Public visibility does not establish extraction or redistribution rights. [Mercado Agroganadero](https://web.mercadoagroganadero.com.ar/).
- BCRA lists a separately documented exchange-statistics API v1.0 and monetary-statistics v4.0; its API catalog marks Principales indicadores v3.0 deprecated February 28, 2026. The statistics page separately labels A3500 wholesale reference and B9791 retail seller average. These are distinct FX conventions. [BCRA API catalog](https://www.bcra.gob.ar/apis-banco-central/); [BCRA statistics](https://www.bcra.gob.ar/estadisticas-indicadores/); [exchange API documentation](https://estadisticas-cambiarias.bcra.apidocs.ar/).

### Inferences

The current local snapshot has a recent retrieval timestamp but heterogeneous observation dates and source populations; the existing documentation's “real-time” promise needs replacement with source-specific cadence. The comparison should offer useful descriptive context without ranking it as directly interchangeable buying opportunities. Source: [local README](/Users/ryanjohnson/Projects/beef-chart/README.md), [local snapshot](/Users/ryanjohnson/Projects/beef-chart/data/prices.json).

Proposed minimal product registry: `species`, stable `cut_id`, authoritative code namespace/version, country-specific names and regional aliases, muscles, boundaries, bone, membrane, fat trim, portion/thickness, whole/subprimal/retail form, fresh/frozen, photos with provenance, culinary methods, reviewed source references. Crosswalk edges carry `exact within stated preparation`, `partial overlap`, `adjacent anatomy`, `culinary alternative`, or `unresolved`; their evidence belongs to the edge, not just the two names. “Bife de costilla” needs regional/bone/specification clarification before attaching a US T-bone or bone-in-strip quote. Do not collapse it into boneless strip.

Proposed observation contract: immutable original amount/currency/unit; market stage; source/report/item; raw description; geography; channel; product qualifications; observation period; publication date; retrieval date; revision; sample/store/product count and weighting method; taxes/freight coverage when known; original evidence hash; parser/schema version; transformation formula and FX rate/series/date. Unknowns stay explicit. The expected benchmark class must be declared before any cross-border difference is calculated.

The USD/lb display remains valuable, but native ARS/kg, USD/kg, USD/cwt, and live/dressed/product weight bases should stay recoverable. Monthly average ARS divided by monthly-average FX is a defined approximation, not necessarily the average of contemporaneously converted transactions. A newly retrieved old FX observation must remain visibly old.

### Gaps

- No new source adapter was exercised. Existing data and pipeline correctness are being reviewed by the owning project/code reviewers.
- The official pages/readable examples above establish documentation/access, not present end-to-end feeds. MMN documentation discusses API authentication and does not support open browser calls; keep credentials in ingestion infrastructure, never the static client. [MMN basic instructions](https://mymarketnews.ams.usda.gov/mars-api/getting-started/basic-instructions); [MMN reports documentation](https://mymarketnews.ams.usda.gov/mars-api/reports).
- IPCVA's statistics landing page was readable, but homepage/nomenclador/detail-PDF fetches failed through this research tool. Its monthly reports remain candidate Argentine retail-context sources; this pass did not reverify a current methodology, latest period, API, or automated redistribution entitlement. [IPCVA statistics](https://ipcva.agrositio.com/estadisticas.php).
- Data, diagrams, photos, and trademarks have different rights. This pass did not establish a blanket reuse permission for MAG, IPCVA, USMEF, retailer catalogs, or their images. Link to their references and prepare a source-rights register before copying assets; the code's MIT statement cannot grant upstream rights.
- A fuller review of nomenclature amendments, grade systems, and all existing crosswalks requires specialist validation; a map should show reviewed and unresolved relationships distinctly.

## 2. What substantive workflows should serve professionals and enthusiasts equally well?

### Takeaway

The differentiator is a connected sequence from understanding a cut to choosing, comparing, buying and preparing it, with every substitution and number explained. Professional specification and costing workflows and consumer meal/butcher workflows should share the evidence foundation while revealing detail appropriate to the task.

### Cited Findings

- Beef It's What's For Dinner supplies professional cut charts in English/Spanish, application-oriented cut finder, cutting guides and videos supporting training, portion control and yield optimization. These are verified table stakes from a primary operator, not evidence that this project has them or that one provider exhausts the market. [Foodservice resource collection](https://www.beefitswhatsfordinner.com/food-professionals/foodservice).
- Its yield documents expressly provide approximate guidance and recommend the operator's own yield testing. Reusing a general chart as guaranteed lot economics would be unjustified. [Yield data](https://www.beefitswhatsfordinner.com/food-professionals/food-professionals-resource-library/yield-data).
- USMEF provides international nomenclature/cut and cuisine resources, plus variety-meat and grading information. The international guide was announced in 2013 for common US cuts across 33 countries/regions; this historical scope does not mean every current retail name is validated. [Current resource collection](https://usmef.org/export-resources/meat-cut-information); [guide announcement](https://www.usmef.org/news/usmef-develops-international-beef-cuts-nomenclature-guide/).
- USDA FSIS recommends beef steaks/chops/roasts reach 145°F/62.8°C with at least a three-minute rest; ground meat 160°F/71.1°C; leftovers 165°F/73.9°C, measured with a thermometer. Time, color and a sensory “doneness” label do not replace this reference. [Safe-temperature chart](https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/safe-temperature-chart).
- FSIS gives cold-storage guidance: refrigerated whole cuts 3–5 days, ground beef and variety meats 1–2 days, refrigerator at 40°F/4.4°C or below. It describes refrigerator/cold-water/microwave thawing, and reheating leftovers. Its consumer guidance should be labeled by jurisdiction, not silently presented as a professional establishment's approved process. [Beef from farm to table](https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/meat-catfish/beef-farm-table).
- FSIS explains mechanical tenderization can move surface bacteria inward, labels identify it, and its guidance is 145°F with three-minute rest. A recipe engine therefore needs intact/tenderized/ground product form, rather than only a cut name. [Mechanically tenderized beef](https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/meat/mechanically-tenderized-beef).
- FoodData Central exposes food-search/details APIs requiring a key, with a default 1,000 requests/hour/IP. Its nutrient data are public domain/CC0, and USDA requests attribution. Downloaded curated records are a useful static/offline alternative to embedding a private API key. [API and licensing guide](https://fdc.nal.usda.gov/api-guide/); [downloadable datasets](https://fdc.nal.usda.gov/download-datasets/).
- FDC distinguishes Foundation Foods, SR Legacy, Survey and Branded datasets; SR Legacy is a final April 2018 release. Portions and weights are datatype-specific, and Foundation Foods includes analytical/sample metadata and nutrient variability. A generic “beef” nutrient record is inadequate for exact cut, raw/cooked, edible-fat and portion comparisons. [Foundation Foods documentation](https://fdc.nal.usda.gov/Foundation_Foods_Documentation/).

### Inferences

Proposals below are product design judgments based on these reference capabilities and the requested audiences, not externally measured demand or claims of competitor inferiority.

| Workflow | Proposed solution | What makes it practically useful | Acceptance example |
|---|---|---|---|
| Find a named cut | Bilingual, accent-insensitive alias search with country and anatomy; tolerate dictation variants | Fast use at butcher counter or on a supplier sheet | “entrana fina” finds the documented outside-skirt relationship and flags membrane preparation |
| Learn by anatomy | Diagram + searchable accessible list + grain/muscle/trim photos, all synchronized | Consumers understand what to ask for; staff have a shared training reference | Selecting a cut in the list exposes the same facts as diagram/hover |
| Buy for a meal | Filters for technique, equipment, available time, budget, people, texture; assumptions visible | An enthusiast can choose unfamiliar/value cuts without already knowing anatomy | “Braise for six” returns suitable sourced methods and editable serving/yield assumptions |
| Explain a substitution | Compare anatomy, preparation, cooking adaptations, texture and availability; rank culinary fit separately from product identity | Lower-cost alternatives become understandable instead of misleading equivalences | A replacement for vacío says what is smaller/different and what cooking/slicing changes |
| Speak to butcher | One-tap bilingual shopping/spec card: local name, alternate name, bone/trim, thickness, quantity and intended method; offline/print | Minimal input, voice-friendly recovery, easy handoff | Reopen last card in two actions, with no retyping; card says which details remain unspecified |
| Plan an asado or mixed meal | Portion estimator with explicit bone/edible/cooked bases; cooking-order planner and shopping list | Supports whole-meal enthusiasm and unfamiliar offal as real tasks | Adjusting guest count updates purchase quantity; changing yield explains why |
| Prepare safely | Cut-aware guide with technique, thickness/equipment assumptions, thermometer target, rest, slicing/grain, storage and thawing | Distinguishes enjoyable outcome from measured safety | Ground and mechanically tenderized selections do not inherit an intact-steak preference profile |
| Compare nutrition | Per 100 g and selected serving, raw/cooked/lean+fat qualifiers, exact FDC ID/date and unknowns | Consumer can compare consistent edible portions and preparation | A cooked lean-only record cannot silently represent a raw fat-on cut |
| Keep personal notes | Local saved cuts, favorite methods, actual weights/yields, equipment and results; export/import | Builds Ryan's low-effort repeatable reference without accounts | Browser restart recovers the last chosen cut and saved meal, with export backup |
| Request a professional quote | Specification builder with separate IMPS/SENASA identifiers, source version, trim/bone/portion/pack/state/grade fields | Name ambiguity becomes reviewable purchase detail | A completed card still calls out unknown grade and unreviewed crosswalk |
| Compare quotes | Private manual or CSV import; validity, delivery terms, weight basis, quantity, price and evidence attachments | Works before any elusive supplier API exists | Two eligible quotes normalize units while mismatched product specs stay visibly mismatched |
| Measure fabrication yield | Purchased mass → cuts/trim/byproducts/bone/fat/waste balance; actual measured outcomes separate from reference assumptions | Captures true shop economics and learning | The lot balances mass or explains a tolerance; editable yield retains original evidence |
| Cost effective portions | Saleable/cooked quantity, labor/freight/packaging and credited trim/byproducts; scenario sensitivity | Makes bone-in cheapness and subprimal fabrication meaningful | Reviewer reproduces a portion cost using native currency, weight and explicit losses |
| Track market context | Source-specific retail/advertising/cattle/boxed-beef views with comparable histories and freshness | Purchasing context without presenting one universal “beef price” | Every trend and spread has aligned stage, period and qualification or an explicit mismatch |
| Train/reuse/export | Short reference cards, cutting-source links, CSV/JSON evidence exports and printable summaries | Procurement staff and enthusiasts both keep inspectable results | Export contains sources/qualifications and reopens as the same saved scenario |

Suggested cost equations (design definitions, not validated business results): `saleable_weight = purchased_weight × fabrication_yield`; `saleable_cost_per_unit = (purchase_cost + allocated_costs − byproduct_credits) / saleable_weight`; `cooked_weight = saleable_weight × cooking_yield`; `cost_per_serving = allocated_total_cost / servings`. Define units, treatment of unsold/byproduct quantities, labor allocation and taxes before use. For a single subprimal, yield should be measured or explicitly assumed; a carcass yield grade cannot fill this field automatically. A simple domestic scenario should precede a cross-border landed-cost scenario.

Proposed side-by-side default jobs: “Understand / Buy / Cook” for consumers and “Specify / Compare / Cost” for professionals. One underlying cut registry and observation model avoids divergent facts. Ryan's short commands, voice input, one-tap repeat actions, large targets and recoverable state should apply throughout; high-density professional tables can coexist with concise everyday cards.

### Gaps

- This pass did not conduct customer interviews, butcher/specification review, cooking trials, lot-yield measurement, nutrition matching, device/screen-reader trials, or task usability testing. These are future validation gates, not assumed successes.
- Food-safety references above are US consumer guidance. Argentine-specific preparation/storage advice and professional kitchen/processor procedures need separate current authoritative sources and review before publication. Avoid inventing offal-specific targets from steak guidance.
- A detailed sous-vide/pasteurization engine, allergen/medical dietary advice, automated label certification, and a professional HACCP/compliance system are not necessary for the first useful release. Neither traditional medium-rare preference nor a timer should be presented as a verified safe process.
- The industry education sites establish content table stakes; this research did not compare every product, app or paywalled buyer tool. Exceptional positioning is a design hypothesis requiring representative users to complete real tasks.

## 3. Which enhancements should be prioritized, and what evidence would justify adoption?

### Takeaway

Repair truth and consistency first, then finish a small set of complete consumer and professional workflows. Add data breadth or other species only after shared identity, evidence, persistence, accessibility and testing boundaries are reliable; comprehensive should mean dependable task coverage rather than a long list of disconnected charts.

### Cited Findings

- The existing README presents an interactive comparison, multi-source pricing, Sankey, lollipop, yield treemap and sensory radar, but its terminology includes “live/real-time” and categorical accessibility claims. Documentation should align with verified functionality and measured evidence. [Local README](/Users/ryanjohnson/Projects/beef-chart/README.md).
- Published IMPS series already cover lamb/mutton, veal, pork, variety meats, goat and other products; Argentine Agriculture publishes a sheep-cut/offal nomenclador. These provide eventual expansion candidates, not permission to infer species-specific taxonomy or food safety from beef. [IMPS catalog](https://www.ams.usda.gov/grades-standards/imps); [Argentine ovine nomenclador](https://www.argentina.gob.ar/sites/default/files/cordero-argentino-nomenclador_de_cortes_de_carne_y_menudencias_ovinas_2023.pdf).
- Direct authoritative source pages above demonstrate distinct data definitions, published standards and food-safety/nutrition foundations. The sources do not by themselves demonstrate an automated ingestion SLA, retail license, lot economics, or current project conformance.

### Inferences

Priority/effort here are relative design estimates. S = bounded schema/content or UI repair; M = several connected components and targeted validation; L = a new end-to-end workflow or source/history subsystem. They are not promised schedules.

**Corrections versus expansion:** P0.1–P0.7 primarily repair current claims, semantics, consistency and evidence handling (some require foundational schema work). P0.8 adds missing safety detail before expanding cooking functionality. P1/P2 are proposed future capabilities or hardening work, with partial implementations to be reconciled against the live repository review. A new source route or new feature is not adopted by inclusion here.

| Rank | Opportunity and concrete proposal | Acceptance criteria | Effort/dependencies |
|---|---|---|---|
| P0.1 | Replace “live” promise and global refresh reassurance with actual cadence/observation age | Old observed dates remain old after a successful download; source outages visible | S; source metadata and wording owner |
| P0.2 | Correct entraña fina; separate vacío vs bife de vacío; audit bone-in strip/T-bone/bife de costilla and matambre relationships | Source/reviewer and relationship type for every reviewed mapping; unresolved entries explicitly marked | M; registry and bilingual meat specialist |
| P0.3 | Define stage and price basis; separate retail survey, ad survey, retailer offers, wholesale and cattle | No cross-stage implied price ranking; displays native unit/channel/geography/period | M; observation schema and migration |
| P0.4 | Make missing/stale/blocked/parser-error/carried-forward distinct | None renders as zero or freshly observed; last good value retains its actual date | M; pipeline semantics and UI states |
| P0.5 | Reconcile app, guide and documentation against one cut catalog | Same name/anatomy/code/source across card, diagram, chart and docs; orphan IDs checked | M; canonical registry/generation approach |
| P0.6 | Identify editorial sensory/yield assumptions and replace universal precision with qualifiers | Every score/yield has a source or clearly labeled heuristic/scenario; denominator visible | S–M; content audit |
| P0.7 | Verify source rights and artifact provenance | Each dataset/image/diagram has ownership, source/version and allowed use or “unknown”; no fabricated blanket open-data claim | S–M; rights evidence, accessible source links |
| P0.8 | Complete source-grounded safety overlays | Correct form/temperature/rest/storage references; preference timings never standalone safety claims | M; safety review and product-form metadata |
| P1.1 | Build bilingual searchable explorer, accessible table and compare tray | Common aliases/accents/dictation variants find correct entries; keyboard yields same information | M; catalog + focused usability checks |
| P1.2 | Ship enthusiast “choose cut → compare alternative → butcher card → prepare” | One representative meal completes without missing information, retyping or hover dependence | L; content and safety foundation |
| P1.3 | Add editable portions/asado meal planning and leftovers | Quantity calculations show edible/bone/cooked bases; assumptions and storage follow-up persist | M; measured/default yield ownership |
| P1.4 | Add private saved favorites, notes, last view and backup/export | Restart and import reproduce exact task state without account setup | M; persistence/version migration/accessibility |
| P1.5 | Ship professional “specification → two quotes → effective cost → saved comparison” | Reviewer reproduces normalized quote and saleable-cost result; unknowns never silently default | L; explicit units/specs + representative quote samples |
| P1.6 | Add lot fabrication/cooking yield measurements, credits and mass balance | Input and output quantities reconcile; reference vs measured data distinct; scenario sensitivity visible | L; costing model and actual operator review |
| P1.7 | Build append-only observation history with revision/provenance export | Old and revised releases remain retrievable; comparisons bind source vintage | L; raw evidence archive and schema |
| P1.8 | Evaluate one USDA wholesale/cattle and one Argentine cattle context source | Exact report/category/unit/geography documented; no-key/manual route or authorized backend works; cadence/outages tested | M per adapter; accepted rights/access and source-definition review |
| P1.9 | Replace brittle FX routes if evidence requires; pin correct A3500/B9791 convention | Endpoint/series contract is validated before switching; FX date/basis always visible; no fallback mislabel | M; BCRA current docs, adapter test and raw evidence |
| P1.10 | Curate matched nutrition data and consumer preference filters | FDC identity/raw-cooked/lean-fat basis retained; unknown nutrients not zero; portion math reproducible | M; offline licensed dataset and matching review |
| P1.11 | Provide cited training/print cards and compact saved market brief | Printed/offline content retains caveats/date/source; return view highlights meaningful changes | M; print/offline/persistence and data freshness |
| P2.1 | Add batch quote/cut imports, comparison exports and user-defined change alerts | Import errors explain row/field; exported calculations retain evidence; unchanged state stays quiet | M–L; completed manual workflow and permissions |
| P2.2 | Add procurement landed-cost scenario for explicitly chosen route | Costs/credits/yield/currency/freight basis reproducible; no inferred trade feasibility from cost alone | L; actual operator need and defined input coverage |
| P2.3 | Broaden beyond US/Argentina or beef in separate reviewed modules | Species-specific names/codes/market sources/nutrition/safety accepted; no silent beef defaults | L per module; beef foundation proven first |
| P2.4 | Add expert contribution/review history if collaboration demanded | Every change has evidence, reviewer scope and version; contributions cannot overwrite source truth | L; clear maintenance capacity and editorial policy |

Proposed release acceptance gates:

1. **Evidence:** pick ten displayed numbers/cut claims; independently trace each to original source, product specification, observation period and transformation.
2. **Comparison:** intentionally select different grade, bone, market stage, region and dates; the interface either explains the difference or declines an equivalence.
3. **Consumer task:** an enthusiast chooses a suitable unfamiliar cut, explains a substitute, gets a bilingual butcher card, calculates an editable quantity and finds preparation/storage guidance.
4. **Professional task:** a butcher/chef/buyer creates a spec, inputs two real quotes, records actual yield or an explicit scenario and independently reproduces effective cost.
5. **Recovery/accessibility:** Ryan performs the same tasks using keyboard/voice-friendly controls; a restart restores the task, and chart/diagram alternatives contain the same information. Real device/assistive-tech checks are separate evidence.
6. **Resilience:** simulated no-stock, no-trading, suppressed-value, stale-FX, source-block and parse-error states preserve prior evidence and never invent current zero prices.
7. **Maintenance:** each source/content section has a named update method/cadence, source version and bounded owner workflow; broaden only when this is sustainable.

Five bounded phases suggested for the report:

1. **Truth and harmony:** correct current content/claims/data semantics; consolidate cut identity, provenance and availability states; complete focused accessibility/functional defects from the repository reviewers.
2. **Exceptional enthusiast reference:** bilingual search/compare and aliases; butcher cards, safe preparation/storage, editable portions, local saved favorites and meal recovery. Acceptance is one complete shopping/cooking task.
3. **Practical professional workbench:** precise product cards, private manual quotes, yield/mass balance and effective cost. Acceptance is one independently reproducible real quote/yield comparison.
4. **Dependable market context:** immutable history, revisions and one validated context source per selected market stage/country, with current FX route and data-health evidence. Acceptance is an outage-safe, fully traceable comparison over time.
5. **Reviewed breadth:** nutrition completion, richer training and imports, then chosen other species/geographies or landed-cost scenarios only where users' tasks justify them. Acceptance is species/route-specific expert review and sustainable maintenance.

There is no requirement to introduce accounts, vendor marketplaces, payment processing, investment/futures analytics, or commercial infrastructure to meet the requested tool ambition.

### Gaps

- Ranking will need reconciliation with verified code/diff/functionality findings from the other reviewers. A requirement already partly implemented should become a repair/acceptance task, not redundant replacement work.
- All task gates are proposals. No consumer, professional, accessibility, nutrition or procurement acceptance has been completed by this research pass.
- Other species require deliberate content and validation scope. Pig/poultry/lamb diagrams, edible yields, safe temperatures and product terms cannot be mechanically cloned from beef.
