# Enter a manual price

Edit `data/manual-prices.json`. Each quote has six fields: **date, item, machine_name, price, currency, unit**. Put Argentine-market quotes under `ar` and U.S.-market quotes under `us`. The market section identifies where the quote belongs; currency alone does not identify the market.

The active file is prefilled with ten Argentine cuts and null dates/prices; fill those entries directly rather than replacing the file with the example below. These completed amounts are examples only:

```json
{
  "ar": [
    {
      "date": "2026-10-15",
      "item": "Pecho — quote reported by my friend",
      "machine_name": "pecho",
      "price": 18500,
      "currency": "ARS",
      "unit": "kg"
    }
  ],
  "us": [
    {
      "date": "2026-10-15",
      "item": "Whole brisket — local shop",
      "machine_name": "brisket_whole",
      "price": 8.50,
      "currency": "USD",
      "unit": "lb"
    }
  ]
}
```

The field rules below apply to completed rows; unfinished date/price fields are skipped as described below.

- **date:** the day the price was observed, in `YYYY-MM-DD` form. Future dates and impossible dates are rejected.
- **item:** your description. Include the butcher, city, bone-in/boneless detail or your friend's wording here if useful. No separate location/source fields are required. Missing details remain unspecified.
- **machine_name:** the stable key from the table below. The visible dossier ID is also accepted as an alias. Names do not prove product equivalence; you choose the cut the quote actually describes.
- **price:** a positive JSON number, without quotation marks or thousands separators. Use a decimal point for fractional amounts, such as `8.50`.
- **currency:** `"ARS"` for Argentine pesos or `"USD"` for U.S. dollars. Currency symbols and mixed amount/unit strings are rejected.
- **unit:** `"kg"` or `"lb"`. Currently supported combinations are `"ARS"` with `"kg"`, and `"USD"` with `"lb"`. Other combinations are rejected explicitly; no conversion or unit is guessed.

Save the file and reload the page. The local server reads manual prices afresh on every request and disables caching for that route. An older server already running before this update needs one restart to adopt it; later manual-price edits need only a page reload.

## Fill the ten cuts gradually

`data/manual-prices.json` already contains Cogote, Pecho, Garrón, Bife de costilla, Mollejas, Riñón, Lengua, Aguja, Entraña and Tapa de cuadril. Each name, machine name, `"ARS"` currency and `"kg"` unit is filled in. Replace `"date": null` with the actual observation date in quotes and `"price": null` with a positive number, directly in this file. No copying or importing is needed. `data/manual-prices.template.json` is only an optional original blank worksheet and is not loaded or required by the app.

Rows without both a date and a price are drafts and are skipped. A null, omitted field, empty string or whitespace-only string counts as blank. Completing only one field has no effect on displayed prices. Existing source observations stay selected until both are filled and the row passes validation. Keep other cuts unfinished for as long as needed. Save and reload the page; a server restart is not needed for manual-price edits.

Once both date and price are supplied, the six-field schema, number, date, currency, unit and machine-name rules apply. Zero, negative amounts, booleans and numeric strings are not blanks and are rejected. A completed invalid row rejects the manual overlay with an explanation; it is not silently skipped. Non-object rows and unknown field names also reject rather than hiding a typo.

## What an entry does

A manual entry overrides that market's displayed observation for that cut, even if an automatic observation is newer. Its actual date stays visible. The page labels it **Manual quote**, with availability and exact product specifications unverified. Both countries can use either supported currency/unit format.

Native ARS/kg stays ARS/kg: no exchange rate is guessed, and these entries do not appear as USD/lb chart points. Native dollar-per-pound entries can appear on that chart, marked with a dagger (`†`). Cards, coverage, dossiers and the evidence table show the selected manual entry. Source observations remain in the full evidence table and, when overridden, in an expandable dossier section. Original Carrefour evidence and its withholding flags remain unchanged. A new manual quote for an organ is a separate observation; it does not verify or rescale the old catalog record.

Clearing either date or price makes a row a draft again, restoring the next eligible manual quote or the automatic observation. If several entries map to one market/cut, the latest observation date wins. For the same date, the later row wins. The file keeps all rows. Removing the selected entry restores the next manual entry, or the automatic source if none remain. An empty `ar`/`us` array disables overrides for that market.

The page rejects the manual overlay if a completed row is invalid or a row has a malformed structure, with the market and row number shown when available. Automatic evidence remains usable. A valid automatic snapshot is required before manual quotes are applied. Row parsing is separate from the automatic-source contract, which continues to validate the scraper snapshot first.

Scrapers only write `data/prices.json`; they do not modify this file. No import command or front-end editor is needed. The launcher serves the manual file as public application data, so enter only descriptions you want visible in the atlas.

## Machine names

Use the key for the market section you are editing. Keys for cuts without automatic coverage are available for manual quotes too.

| Cut | `ar` machine_name | `us` machine_name |
|---|---|---|
| Cogote | `cogote` | `cogote` |
| Aguja | `aguja` | `chuck_roast` |
| Paleta | `paleta` | `paleta` |
| Pecho | `pecho` | `brisket_whole` |
| Brazuelo | `osobuco` | `brazuelo` |
| Bife ancho | `bife_ancho` | `ribeye_bnls` |
| Asado de tira | `asado` | `short_ribs` |
| Matambre | `matambre` | `matambre` |
| Bife de chorizo | `bife_angosto` | `strip_bnls` |
| Vacío | `vacio` | `flank` |
| Tapa de cuadril | `tapa` | `tapa` |
| Cuadril | `cuadril` | `sirloin_steak` |
| Colita de cuadril | `colita` | `tri_tip` |
| Bola de lomo | `bola_lomo` | `round_roast` |
| Nalga | `nalga` | `round_steak` |
| Cuadrada | `cuadrada` | `bottom_round` |
| Garrón | `garron` | `garron` |
| Lomo | `lomo` | `tenderloin` |
| Entraña | `entrana` | `skirt` |
| Peceto | `peceto` | `eye_round` |
| Bife de costilla | `bife_costilla` | `bife-costilla` |
| Mollejas | `molleja` | `molleja` |
| Riñón | `rinon` | `rinon` |
| Lengua | `lengua` | `lengua` |
| Ground beef benchmark | `ground_beef` | `ground_beef` |

## Targeted verification

`node --test tests/test_manual_prices.cjs` runs focused offline cases for the numeric format, source preservation, local display output, file-load fallback and restoration after removing an override. Sample quotes are created only in memory; the checks do not edit either production price file or contact sources. The checks also cover unfinished drafts and gradual completion alongside the neighboring price-display checks. This verifies functions and chart callbacks with local doubles, not browser layout or assistive-technology behavior.

For the local reload route, `PYTHONPATH=.:tests python3 -m unittest -q test_live_manual_server` runs seven handler cases without opening a browser or binding a listener. These and the 18 manual-price cases passed for the reload-only update.
