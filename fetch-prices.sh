#!/usr/bin/env bash
# Explicit refresh: independent official/retail attempts, one validated atomic write.
set -euo pipefail
cd "$(dirname "$0")"
exec python3 ./scrape-retail.py --official "$@"
