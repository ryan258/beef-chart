# Price evidence and refresh contract

The page loads one stored snapshot, not live prices. Sources measure different populations, product forms, geographies, and intervals. USD/lb normalization does not make them identical products or purchasing opportunities.

## Sources

| Source | Native meaning | Cadence and qualification |
|---|---|---|
| BLS Average Price Data | U.S. monthly retail consumer-price averages, USD/lb | Valid M01–M12 rows are sorted; previous means previous available observation with its own period, not necessarily last month |
| INDEC IPC-GBA via datos.gob.ar | Greater Buenos Aires selected-item averages, ARS/kg | Monthly; retain native value if matching positive monthly FX is missing |
| Carrefour Argentina catalog | Bounded sample of retailer SKU quotes, ARS/kg | On-demand; max 20 products per query, first seller, deduplicated SKUs; availability belongs to retrieval, not today |
| USDA AMS grocery features | Store-weighted advertised conventional/fresh features, USD/lb | Explicit current/prior feature ranges required; report publication is separate; real-layout acceptance unresolved |
| BCRA-derived datos.gob.ar FX | Named ARS/USD observation | INDEC uses matching monthly average; catalog uses latest returned daily observation, which can lag; native U.S. prices use no FX |

Existing URLs/series remain as listed in `fetch-prices.sh` and `scrape-retail.py`; no new market feeds were integrated. An endpoint is not proof of accepted transport, methodology, or reuse permission.

## Minimal v2 contract

The owning validator is `price_contract.py`; browser validation enforces the corresponding rendered price/date boundary.

- `schema_version: 2`; `us`/`ar` observation objects; `fx` and `source_status` objects.
- `generated_at` describes artifact generation. Legacy `fetched` is retained for compatibility and is not universal proof of record retrieval.
- Records retain `period`, native `usd_lb` or `ars_kg`, source, and qualifiers. Positive finite prices are required; booleans, zero, negative/nonfinite values and invalid dates fail validation. AR conversion may be null while native ARS/kg remains usable.
- `retrieved_at`, `publication_date`, `prev_period`, and explicit feature boundaries have different meanings. Unknown legacy fields remain null; USDA legacy report-date labels do not become verified effective intervals.
- `market_stage`, `geography`, `method`, `provenance_status`, `observation_status`, and catalog `availability` travel with displayed values.
- Optional boolean `unit_scale_unverified: true` withholds an observation from ordinary price display, rankings, value comparisons and buying estimates, including native-price fallbacks. Cards show “Price withheld”; dossiers and the price table retain the numbers only as explicitly labeled evidence. Missing/false is not proof of verified units, availability or overall comparability. The flag belongs to the observation: qualification, failed/empty attempts and bounded previous-observation retention preserve it.
- AR records disclose `fx_ars_per_usd`, `fx_date`, `fx_basis`, and `fx_provenance`. Legacy metadata inferred from the bundled snapshot is labeled inferred, not original evidence. Daily FX later than a day observation is rejected; stale rates remain visibly old.
- `source_status` and `catalog_attempts` report source/cut attempt outcome and timestamp. No match, error, legacy unknown, and successful retrieval are distinct.
- New records can retain `previous_observation` for bounded recovery. This keeps one previous version, not an append-only historical store.

The bundled October 7 snapshot was qualified locally on October 12: values, record periods, legacy fetched timestamp, and August 31 latest-returned FX were not refreshed. Original raw receipts are not reconstructed. The three stored organ observations also carry `unit_scale_unverified: true`; parser regressions do not prove the cause of their unusually low nominal values.

**Validation note — organ-price units pending verification:** The stored Carrefour Argentina observations for mollejas, riñón, and lengua have unusually low native prices and should be treated as unverified unit scale. Their USD/lb conversions are mathematically consistent with the recorded inputs, but the retained evidence does not establish the original sale unit or package-weight basis; the underlying listings were also out of stock. Exclude these observations from price rankings, value comparisons, and buying estimates until the original units and availability are verified. Preserve the native values and dates for traceability, and apply a scaling correction only when supported by source evidence.

This qualification preserves 1,830, 279.9 and median 1,680 recorded as ARS/kg (respectively $0.55, $0.08 and $0.50/lb), all dated October 7, 2026, plus their original listings and FX evidence. It does not identify a per-100g or package price, and no scaling correction has been applied. Requalification needs source evidence for the original sale unit/package-weight basis and availability; a changed amount or stock label alone does not resolve these stored observations. A genuinely new observation is separate, with the flagged old record retained in `previous_observation`. The existing illustrative value treemap uses fixed teaching shares, not these or any other snapshot prices.

## Matching, parsing, and promotion

Every catalog key requires explicit raw/crudo form evidence (structured metadata or the name) and bovine evidence, an explicit x/por kg basis, structured `measurementUnit=kg` and non-boolean multiplier 1, and a positive finite quote. Prepared/wrong-species/unknown-species/pack offers fail closed. Catalog section/name alone does not establish species. Accepted listings retain unit, species evidence, seller/SKU, name, and URL. Bone-in costilla stays separate from boneless strip and T-bone; generic sweetbreads do not prove thymus.

USDA uses store-weighted current values and previous values from their explicit intervals. Prior-only fallback retains the prior interval and reason; publication-date subtraction is never used to invent an effective week. Header/column collisions or missing intervals classify a parse failure. No accepted real PDF/text fixture could be retained during this implementation; live layout compatibility remains unresolved and may result in retaining existing references rather than a refreshed USDA observation. Synthetic tests prove the date/failure contract, not live PDF acceptance.

Validated snapshots are atomically replaced in the destination directory. A failed/empty cut retains old evidence and its date with a status; healthy cuts and staged official observations can advance. A partial source failure writes the qualified valid snapshot and returns a nonzero status to draw operator attention. Invalid resulting data never replaces the file. A completely failed official shell stage preserves the existing snapshot and exits before the scraper; independent official-source attempts remain future work.

## Operator use

```bash
./serve.sh
# Explicit provider refresh when wanted; updates local snapshot only:
./fetch-prices.sh
# Small catalog attempt:
python3 scrape-retail.py --cuts bife_costilla molleja rinon lengua
```

These refresh commands make network requests and can write attempts/qualified observations even when returning nonzero. Inspect `source_status`, `catalog_attempts`, and original observation dates before treating the result as updated evidence. No refresh, staging, commits, publication, or automation is implicit in opening the app. Prerequisites: Python 3, curl/jq for the official stage, pdftotext for USDA; no paid credentials were used here.
