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

Existing URLs/series remain unchanged and are now listed in `official_prices.py` and `scrape-retail.py`; no new market feeds were integrated. An endpoint is not proof of accepted transport, methodology, or reuse permission.

## Minimal v2 contract

The owning validator is `price_contract.py`; browser validation enforces the corresponding rendered price/date boundary.

- `schema_version: 2`; `us`/`ar` observation objects; `fx` and `source_status` objects.
- `generated_at` describes artifact generation. Legacy `fetched` is retained for compatibility and is not universal proof of record retrieval.
- Records retain `period`, native `usd_lb` or `ars_kg`, source, and qualifiers. Positive finite prices are required; booleans, zero, negative/nonfinite values and invalid dates fail validation. AR conversion may be null while native ARS/kg remains usable.
- `retrieved_at`, `publication_date`, `prev_period`, and explicit feature boundaries have different meanings. Unknown legacy fields remain null; USDA legacy report-date labels do not become verified effective intervals.
- `market_stage`, `geography`, `method`, `provenance_status`, `observation_status`, and catalog `availability` travel with displayed values.
- Optional boolean `unit_scale_unverified: true` withholds an observation from ordinary price display, rankings, value comparisons and buying estimates, including native-price fallbacks. Cards show “Price withheld”; dossiers and the price table retain the numbers only as explicitly labeled evidence. Missing/false is not proof of verified units, availability or overall comparability. The flag belongs to the observation: qualification, failed/empty attempts and bounded previous-observation retention preserve it.
- Optional `sampling` on new Carrefour observations describes the actual bounded sample (below). Python and browser validators reject malformed counts, query evidence, seller metadata and contradictory coverage classifications. Absence means historical sampling coverage is unknown; it is not reconstructed from prices or retained listings.
- AR records disclose `fx_ars_per_usd`, `fx_date`, `fx_basis`, and `fx_provenance`. Legacy metadata inferred from the bundled snapshot is labeled inferred, not original evidence. Daily FX later than a day observation is rejected; stale rates remain visibly old.
- `source_status` and `catalog_attempts` report source/cut attempt outcome and timestamp. No match, error, legacy unknown, and successful retrieval are distinct.
- Official source states use `ok`, `partial`, `no_match` or `error`. BLS/INDEC `coverage` includes every configured series, including missing ones; INDEC `native_only` lists new observations without matching monthly FX. `FX monthly` and `FX daily` are separate attempts. `fx.monthly_retrieved_at` dates a successful monthly-rate retrieval; it does not replace the rate's observation period or the separate daily `fx.latest` evidence.
- Carrefour aggregate states use `ok` (all requested cuts returned observations), `no_match` (all empty), `partial` (observations and empty cuts), `error` (all failed), or `partial_error` (mixed failures). Cut coverage retains `ok`, `no_match` or `error`. A successful reference observation may still be inactive or unverified; this is not offer eligibility.
- New records can retain `previous_observation` for bounded recovery. This keeps one previous version, not an append-only historical store.
- Display localization (`assets/i18n.js`) operates strictly at the presentation boundary: formatting dates and decimals for Argentina and prefixing dollar amounts with `US$` in Spanish. USD displays round to two fraction digits; native amounts and FX displays use up to six, consistently across table, dossier, native fallback and retained evidence. Benchmark percentage displays use one fraction digit. Display rounding is not a transformation of stored observations. Underlying price observations, numeric amounts, currency identities, measurement units ($/lb, ARS/kg), and validation invariants are never mutated by language switching.

The bundled October 7 snapshot was qualified locally on October 12: values, record periods, legacy fetched timestamp, and August 31 latest-returned FX were not refreshed. Original raw receipts are not reconstructed. The three stored organ observations also carry `unit_scale_unverified: true`; parser regressions do not prove the cause of their unusually low nominal values.

**Validation note — organ-price units pending verification:** The stored Carrefour Argentina observations for mollejas, riñón, and lengua have unusually low native prices and should be treated as unverified unit scale. Their USD/lb conversions are mathematically consistent with the recorded inputs, but the retained evidence does not establish the original sale unit or package-weight basis; the underlying listings were also out of stock. Exclude these observations from price rankings, value comparisons, and buying estimates until the original units and availability are verified. Preserve the native values and dates for traceability, and apply a scaling correction only when supported by source evidence.

This qualification preserves 1,830, 279.9 and median 1,680 recorded as ARS/kg (respectively $0.55, $0.08 and $0.50/lb), all dated October 7, 2026, plus their original listings and FX evidence. It does not identify a per-100g or package price, and no scaling correction has been applied. Requalification needs source evidence for the original sale unit/package-weight basis and availability; a changed amount or stock label alone does not resolve these stored observations. A genuinely new observation is separate, with the flagged old record retained in `previous_observation`. The existing illustrative value treemap uses fixed teaching shares, not these or any other snapshot prices.

## Matching, parsing, and promotion

Every catalog key requires explicit raw/crudo form evidence (structured metadata or the name) and bovine evidence, an explicit x/por kg basis, structured `measurementUnit=kg` and non-boolean multiplier 1, and a positive finite quote. Prepared/wrong-species/unknown-species/pack offers fail closed. Catalog section/name alone does not establish species. Accepted listings retain unit, species evidence, seller/SKU, name, and URL. Bone-in costilla stays separate from boneless strip and T-bone; generic sweetbreads do not prove thymus.

### Carrefour sampling transparency (C14)

The adapter still requests only the first 20 products for each configured query and examines the first seller per SKU. No pagination, additional sellers or delivery-region queries were added. Each new observation records:

- `queries`: query text and actual `returned_products` before matching/filtering. Counts are per response and can overlap across aliases; they are not unique retailer product totals. `per_query_limit` records the requested maximum (20), even if a response exceeds it.
- `eligible_count`: accepted listings after the existing product-ID/SKU-ID/name deduplication. `selected_count`, also retained as the legacy `products` count, is the number used for the median. These are listing counts, not a claim of unique products across every possible title/identifier variant.
- `population`: `available_listings` when at least one accepted listing was available, otherwise `out_of_stock_references`. The latter median remains an inactive reference. Availability describes the observation, not today's inventory; unit-scale withholding continues to apply independently.
- `seller_policy: first_seller_per_sku`, distinct known `seller_ids` for selected listings, and `unknown_seller_count`. Original listing seller IDs remain intact. `region` is null because the adapter does not establish a delivery region; Argentina-wide availability or representativeness is not inferred.
- `coverage: possibly_truncated` when any query returns at least its requested limit; otherwise `unknown`. A limit hit does not prove more results exist. A short response does not prove completeness. Neither state permits an exhaustive retailer-coverage claim.

Dossiers and the existing price-table source/status column use the same sampling explanation. Historical observations without `sampling` show any recorded selected count and retained sampling note, explicitly stating that original query counts, limit hits and seller/region coverage are unknown. This is a display qualification; the stored October 7 snapshot is unchanged. Failed/empty attempts retain the original sampling evidence with the original observation; replacement keeps it in `previous_observation`. Only successful future observations can supply new query evidence.

### Other adapters and promotion

USDA uses store-weighted current values and previous values from their explicit intervals. Prior-only fallback retains the prior interval and reason; publication-date subtraction is never used to invent an effective week. Header/column collisions or missing intervals classify a parse failure. No accepted real PDF/text fixture could be retained during this implementation; live layout compatibility remains unresolved and may result in retaining existing references rather than a refreshed USDA observation. Synthetic tests prove the date/failure contract, not live PDF acceptance.

`./fetch-prices.sh` invokes `scrape-retail.py --official`. `official_prices.py` independently requests and parses BLS, monthly FX, and INDEC using the existing endpoints/series and Python's standard library. Each request has a 20-second socket timeout and no automatic retry. These attempts run before the existing independent daily-FX, catalog-cut and USDA attempts. An official-source request/JSON/parser failure is recorded and does not stop other sources from being attempted. The previous internal `--official-snapshot` option still accepts a local staged file; its groups are validated independently, and an unreadable or malformed file records official failures while retail attempts continue. That option still runs the other retail requests; it is not an offline mode.

Every official source's candidate records are validated before merging. Malformed source batches are rejected as a source, with original records retained; missing individual series or successful empty responses retain their old observations as `retained_no_match`. Request/parse failures mark the affected source's retained records `retained_after_error`. Native/converted amounts, original observation/retrieval dates, FX evidence, unit-scale flags and listing evidence survive retention. Successful replacements keep the bounded `previous_observation` as before. Attempt timestamps describe the start of the current refresh, separately from the original observation dates.

INDEC conversions use only matching monthly rates from the current successful monthly-FX response. If that response fails, is malformed/empty, or lacks the relevant month, new native ARS/kg observations still advance with null USD conversion/rate/date and unknown FX provenance. Stored monthly FX and daily FX are not borrowed to fill the gap. Old converted observations remain in `previous_observation`. A monthly-FX failure/empty result retains the existing top-level FX evidence; a successful monthly update leaves the daily `latest` field intact.

Retail batches are validated against the v2 contract before merging, including keys/source identity, numeric/date/text fields, sampling and unit-scale flags. Nested product/items/sellers/offer shape errors classify as `ValueError`; HTTP failures including `IncompleteRead` are caught at daily-FX, catalog-cut and USDA boundaries. Response handles close on success or failure. A rejected retail batch retains its previous observations and does not contaminate healthy staged results.

One final validated snapshot is atomically replaced in the destination directory. A failed, empty or partial official source (including native-only INDEC coverage), a failed retail source/cut, or any requested catalog cut with no match produces a nonzero process result after healthy results and attempt statuses are saved. A catalog run with all empty cuts reports `no_match`, not `ok`; mixed success/no-match reports `partial`. A USDA empty batch also produces a nonzero result. Missing individual advertised USDA items are retained and do not by themselves classify an otherwise parsed report as a transport failure. If every source fails, observations remain unchanged apart from retention/attempt metadata; generation time may advance without implying a price refresh. Invalid resulting data never replaces the file. This is source-level isolation, not an append-only history store or proof of live-provider compatibility.

## Operator use

Opening the atlas reads the stored JSON once; illustrations and map redraws do not refresh or change observations. All 24 cut dossiers can be illustrated even when a price is missing or withheld. The current bundled snapshot is unchanged by the C06/C14 and artwork work.

```bash
./serve.sh
# Explicit provider refresh when wanted; updates local snapshot only:
./fetch-prices.sh
# Small catalog attempt:
python3 scrape-retail.py --cuts bife_costilla molleja rinon lengua
```

`python3 scrape-retail.py` without flags attempts daily FX, all configured catalog cuts, and USDA, leaving official monthly sources alone. `--cuts` limits catalog work and skips USDA. `./fetch-prices.sh --cuts ...` additionally attempts all official monthly sources because the wrapper supplies `--official`. Use `--help` to inspect arguments without provider requests. `BEEF_PRICES_OUT` selects an alternative existing snapshot file for a deliberate refresh; it is not an offline/dry-run switch.

These refresh commands make network requests and can write attempts/qualified observations even when returning nonzero. Inspect `source_status`, `catalog_attempts`, and original observation dates before treating the result as updated evidence. No refresh, staging, commits, publication, or automation is implicit in opening the app. Prerequisites: Python 3.10+ and pdftotext for USDA; curl/jq are no longer required for this price pipeline. No paid credentials were used here.
