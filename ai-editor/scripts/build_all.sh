#!/usr/bin/env bash
# Build every project in raw/<slug>/ that has imgs/, voice.wav, script.txt, title.txt -> done/<slug>.mp4
set -euo pipefail
cd "$(dirname "$0")/.."
for d in raw/*/; do
  s=$(basename "$d")
  [ -f "$d/voice.wav" ] && [ -f "$d/script.txt" ] && [ -d "$d/imgs" ] || continue
  [ "$(ls "$d/imgs" | wc -l)" -ge 1 ] || continue
  python3 scripts/trim_borders.py "$d"/imgs/*.jpg 2>/dev/null || true
  fit=fill
  python3 scripts/make_short.py --images "$d/imgs" --voice "$d/voice.wav" --script "$d/script.txt" \
    --title "$(cat "$d/title.txt")" --music music/dark_ambient.wav --fit $fit --out "done/$s.mp4" 2>&1 | grep -v Warning
done
