#!/usr/bin/env bash
# Serve a public copy on loopback, reading manual prices live on every request.
set -euo pipefail
cd "$(dirname "$0")"
public_dir=$(mktemp -d "${TMPDIR:-/tmp}/beef-chart-public.XXXXXX")
trap 'rm -rf "$public_dir"' EXIT
mkdir -p "$public_dir/assets" "$public_dir/data"
[ ! -L index.html ] && [ ! -L data/prices.json ] || { echo "Refusing symlink entry files" >&2; exit 1; }
cp index.html "$public_dir/index.html"
cp data/prices.json "$public_dir/data/prices.json"
shopt -s nullglob
for asset in assets/*.css assets/*.js assets/*.webp assets/*.png assets/*.jpg assets/*.svg; do
  [ ! -L "$asset" ] || { echo "Refusing symlink asset: $asset" >&2; exit 1; }
  cp "$asset" "$public_dir/assets/"
done
port=${BEEF_CHART_PORT:-8792}
printf 'Beef Chart: http://127.0.0.1:%s — Ctrl-C to stop; save manual prices and reload. Other files: restart after edits.\n' "$port"
python3 serve_public.py --port "$port" --directory "$public_dir"
