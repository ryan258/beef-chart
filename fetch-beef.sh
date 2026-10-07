#!/usr/bin/env bash
# Snapshot BeefAPI v2 cut data into data/us-cuts.json (run once; re-run to refresh).
# Raw responses are cached in data/raw/ so re-runs only fetch what's missing: rm -r data/raw to force.
set -euo pipefail
cd "$(dirname "$0")"

[ -f .env ] || { echo "missing .env" >&2; exit 1; }
set -a; . ./.env; set +a
: "${BEEFAPI_APP_ID:?set BEEFAPI_APP_ID in .env}" "${BEEFAPI_APP_KEY:?set BEEFAPI_APP_KEY in .env}"
BASE="${BEEFAPI_BASE:-https://beefapi.beef.org}/api/v2/beefcut"
command -v jq >/dev/null || { echo "jq required (brew install jq)" >&2; exit 1; }

get() { # keys go in headers, not the URL, so they stay out of logs/history
  curl -fsS -H "AuthorizationAppID: $BEEFAPI_APP_ID" -H "AuthorizationAppKey: $BEEFAPI_APP_KEY" -H "Accept: application/json" "$1"
}

mkdir -p data/raw
get "$BASE" > data/raw/_list.json
get "$BASE/primal" > data/raw/_primals.json

ids=$(jq -r '.ingredientList[].ingredientID' data/raw/_list.json)
total=$(echo "$ids" | wc -l | tr -d ' '); n=0
for id in $ids; do
  n=$((n+1))
  [ -s "data/raw/$id.json" ] && continue
  echo "[$n/$total] cut $id"
  get "$BASE/$id" > "data/raw/$id.json"
  sleep 0.2 # ponytail: fixed delay, rate limits aren't documented
done

# Slim each record to what the page needs; nutritionals (large) are left in raw/.
jq -s '{fetched: (now|todate), primals: .[0].ingredientListing, cuts: .[1:]}' data/raw/_primals.json $(for id in $ids; do echo "data/raw/$id.json"; done) \
| jq '.cuts |= map({ingredientID, ingredientName, ingredientNameSlug, ingredientText, marketingText, preparationText, orderingText, butchersTip, showcaseNutrients, aliases, alternatives, primalIngredient, media})' \
> data/us-cuts.json
echo "wrote data/us-cuts.json ($total cuts)"
