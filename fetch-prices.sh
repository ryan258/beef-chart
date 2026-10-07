#!/usr/bin/env bash
# Snapshot open retail beef prices into data/prices.json (no API keys needed; re-run monthly).
#   US: BLS Average Price Data (USD/lb, monthly national average)
#   AR: INDEC IPC-GBA average prices via datos.gob.ar (ARS/kg, Greater Buenos Aires), converted at the same month's average BCRA rate
set -euo pipefail
cd "$(dirname "$0")"
command -v jq >/dev/null || { echo "jq required (brew install jq)" >&2; exit 1; }
mkdir -p data
snapshot=$(mktemp data/prices.XXXXXX)
trap 'rm -f "$snapshot"' EXIT

# key|BLS series id|label
US="ground_beef|APU0000703112|Ground beef, 100% beef
ground_chuck|APU0000703111|Ground chuck, 100% beef
ground_lean|APU0000703113|Ground beef, lean & extra lean
round_roast|APU0000703311|Round roast, USDA Choice, boneless
round_steak|APU0000703511|Round steak, USDA Choice, boneless
sirloin_steak|APU0000703613|Sirloin steak, USDA Choice, boneless"

# key|datos.gob.ar series id|label
AR="ground_beef|105.1_I2CPC_2016_M_27|Carne picada común
asado|105.1_I2A_2016_M_14|Asado
cuadril|105.1_I2C_2016_M_16|Cuadril
nalga|105.1_I2N_2016_M_14|Nalga
paleta|105.1_I2P_2016_M_15|Paleta"
FX_ID="92.2_TIPO_CAMBIION_0_0_21_24"

year=$(date +%Y)
ids=$(echo "$US" | cut -d'|' -f2 | jq -R . | jq -sc .)
bls=$(curl -fsS -X POST https://api.bls.gov/publicAPI/v2/timeseries/data/ -H 'Content-type: application/json' \
  -d "{\"seriesid\":$ids,\"startyear\":\"$((year-1))\",\"endyear\":\"$year\"}")
[ "$(echo "$bls" | jq -r .status)" = REQUEST_SUCCEEDED ] || { echo "BLS error: $(echo "$bls" | jq -c .message)" >&2; exit 1; }

arids=$(echo "$AR" | cut -d'|' -f2 | paste -sd, -)
ar=$(curl -fsS "https://apis.datos.gob.ar/series/api/series/?ids=$arids&last=2&format=json")
fx=$(curl -fsS "https://apis.datos.gob.ar/series/api/series/?ids=$FX_ID&collapse=month&collapse_aggregation=avg&last=12&format=json")

# ponytail: BLS skips months (e.g. Oct 2025 lapse), so "prev" is the previous *available* month, not strictly last month
us_json=$(echo "$US" | while IFS='|' read -r k sid label; do
  echo "$bls" | jq --arg k "$k" --arg sid "$sid" --arg label "$label" '
    [.Results.series[] | select(.seriesID==$sid) | .data[] | select(.value!="-" and (.period|startswith("M")))] as $d
    | if ($d|length)<1 then empty else
      {($k): {label:$label, series:$sid, source:"BLS", usd_lb:($d[0].value|tonumber), period:"\($d[0].year)-\($d[0].period[1:])",
              prev_usd_lb:(if ($d|length)>1 then ($d[1].value|tonumber) else null end)}} end'
done | jq -s add)

ar_json=$(echo "$AR" | while IFS='|' read -r k sid label; do
  col=$(echo "$AR" | cut -d'|' -f2 | grep -nxF "$sid" | cut -d: -f1)
  jq -n --argjson r "$ar" --argjson fx "$fx" --arg k "$k" --arg sid "$sid" --arg label "$label" --argjson col "$col" '
    def rate_for($row): ($fx.data | map(select(.[0]==$row[0]))[0]);
    def usdlb($row): rate_for($row)[1] as $rate
      | if $rate then ($row[$col]/$rate/2.2046226) else null end;
    $r.data as $d
    | (rate_for($d[-1]) // [null, null]) as $fxrow
    | {($k): {label:$label, series:$sid, source:"INDEC", ars_kg:$d[-1][$col], period:($d[-1][0][0:7]),
      usd_lb:usdlb($d[-1]), prev_usd_lb:(if ($d|length)>1 then usdlb($d[-2]) else null end),
      fx_ars_per_usd:$fxrow[1], fx_date:$fxrow[0], fx_basis:"BCRA monthly average"}}'
done | jq -s add)

jq -n --argjson us "$us_json" --argjson ar "$ar_json" --argjson fx "$fx" '
  {fetched:(now|todate), us:$us, ar:$ar,
   fx:{series:"'"$FX_ID"'", ars_per_usd:($fx.data[-1][1]), period:($fx.data[-1][0][0:7]), source:"BCRA via datos.gob.ar (monthly average)", basis:"INDEC conversions use monthly average matched to price month. Carrefour and USDA records use daily latest, stored per record."},
   sources:{us:"US Bureau of Labor Statistics, Average Price Data", ar:"INDEC IPC-GBA average prices via datos.gob.ar"}}' > "$snapshot"

# scrape USDA ad prices + Argentine supermarket prices for the cuts the open APIs lack (needs pdftotext)
BEEF_PRICES_OUT="$snapshot" ./scrape-retail.py
mv "$snapshot" data/prices.json
echo "Updated data/prices.json"
