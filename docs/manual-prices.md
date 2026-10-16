# Enter a manual price

**English** · [Español (Argentina)](manual-prices.es.md)

Edit `data/manual-prices.json`. Each quote has six fields: **date, item, machine_name, price, currency, unit**. Put Argentine-market quotes under `ar` and U.S.-market quotes under `us`. The section tells the page which market a quote belongs to; currency alone does not.

The active file already lists ten Argentine cuts with null dates and prices. Fill those rows in place rather than replacing the file with the example below. The amounts here are examples only:

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

## The six fields

These rules apply to completed rows. Unfinished rows are skipped, as described below.

- **date:** the day you saw the price, as `YYYY-MM-DD`. Future and impossible dates are rejected.
- **item:** your own description. Put the butcher, the city, bone-in or boneless, or your friend's exact words here if useful. There are no separate location or source fields, and missing details stay unspecified.
- **machine_name:** the stable key from the [table below](#machine-names). The visible dossier ID is accepted as an alias. A name never proves product equivalence: you choose the cut the quote actually describes.
- **price:** a positive JSON number, with no quotation marks or thousands separators. Use a decimal point for fractions, such as `8.50`.
- **currency:** `"ARS"` for Argentine pesos or `"USD"` for U.S. dollars. Currency symbols and mixed amount-and-unit strings are rejected.
- **unit:** `"kg"` or `"lb"`. Only `"ARS"` with `"kg"` and `"USD"` with `"lb"` are supported. Any other combination is rejected explicitly; no conversion is guessed.

Save the file and reload the page. The local server reads manual prices fresh on every request and disables caching for that route. A server that was already running before this feature needs one restart; after that, a page reload is enough.

## Fill the ten cuts gradually

`data/manual-prices.json` already contains Cogote, Pecho, Garrón, Bife de costilla, Mollejas, Riñón, Lengua, Aguja, Entraña, and Tapa de cuadril, each with its name, machine name, `"ARS"` currency, and `"kg"` unit. Replace `"date": null` with the real observation date in quotes, and `"price": null` with a positive number. No copying or importing is needed. `data/manual-prices.template.json` is an optional blank worksheet that the app neither loads nor requires.

A row with no date or no price is a **draft** and is skipped. Null, an omitted field, an empty string, and a whitespace-only string all count as blank. Filling in only one field changes nothing on screen: the existing source observation stays selected until both are filled and the row passes validation. Leave other cuts unfinished for as long as you like.

Once both date and price are present, the full rules apply: the six-field schema and the number, date, currency, unit, and machine-name checks. Zero, negative amounts, booleans, and numeric strings are not blanks and are rejected. A completed invalid row rejects the whole manual overlay with an explanation; it is never silently skipped. Non-object rows and unknown field names also reject, so a typo can't hide.

## What an entry does

A manual entry overrides the displayed observation for that cut in that market, even when an automatic observation is newer. Its real date stays visible, and the page labels it **Manual quote**, with availability and exact product specification unverified. Both countries can use either supported currency/unit format.

- **Native ARS/kg stays ARS/kg.** No exchange rate is guessed, and these entries don't appear as USD/lb chart points.
- **Native USD/lb can appear on the chart,** marked with a dagger (`†`).
- **Cards, coverage, dossiers, and the evidence table** all show the selected manual entry. Source observations remain in the full evidence table and, when overridden, in an expandable dossier section. Original Carrefour evidence and its withholding flags are unchanged.
- **A manual organ quote is a separate observation.** It doesn't verify or rescale the old catalog record.

Clearing the date or the price turns a row back into a draft, and the next eligible manual quote or the automatic observation takes over. If several entries map to the same market and cut, the latest observation date wins; on the same date, the later row wins. The file keeps every row. Removing the selected entry brings back the next manual entry, or the automatic source if none remain. An empty `ar` or `us` array turns overrides off for that market.

If a completed row is invalid or a row is malformed, the page rejects the manual overlay and shows the market and row number when it can. Automatic evidence stays usable. A valid automatic snapshot is required before manual quotes apply, and the rows are parsed separately from the automatic-source contract, which still validates the scraper snapshot first.

Scrapers write only `data/prices.json` and never touch this file. There is no import command and no front-end editor. The launcher serves the manual file as public application data, so enter only descriptions you are happy to see in the atlas.

## Machine names

Use the key for the market section you are editing. Cuts without automatic coverage can take manual quotes too.

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

`node --test tests/test_manual_prices.cjs` runs focused offline cases for number format, source preservation, local display output, file-load fallback, and restoring the original after an override is removed. Sample quotes exist only in memory, and the checks neither edit the production price files nor contact any source. They also cover unfinished drafts and gradual completion next to the neighboring price-display checks. This verifies functions and chart callbacks with local doubles; it does not verify browser layout or assistive-technology behavior.

For the local reload route, `PYTHONPATH=.:tests python3 -m unittest -q test_live_manual_server` runs seven handler cases with no browser and no listener. Those seven and the 18 manual-price cases passed for the reload-only update.
