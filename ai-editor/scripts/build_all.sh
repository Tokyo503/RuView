#!/usr/bin/env bash
# Build every project in raw/<slug>/ that has imgs/, voice.wav, script.txt, title.txt -> done/<slug>.mp4
# Music bed by raw/<slug>/type.txt (written by gen_images.py): garden -> calm_warm, anything else -> dark_ambient.
# One failed project no longer stops the batch; a summary is printed at the end (exit 1 if any failed).
# Optional: QA=1 re-transcribes each finished short and prints its word match vs the script (qa_transcript.py).
#           ONLY=<slug> builds just that project.
set -uo pipefail
cd "$(dirname "$0")/.."
[ -s music/dark_ambient.wav ] && [ -s music/calm_warm.wav ] || bash scripts/make_music.sh
ok=(); failed=()
for d in raw/*/; do
  d=${d%/}; s=$(basename "$d")
  [ -n "${ONLY:-}" ] && [ "$s" != "$ONLY" ] && continue
  [ -f "$d/voice.wav" ] && [ -f "$d/script.txt" ] && [ -d "$d/imgs" ] || continue
  [ "$(ls "$d/imgs" | wc -l)" -ge 1 ] || continue
  python3 scripts/trim_borders.py "$d"/imgs/*.jpg 2>/dev/null || true
  kind=""; [ -f "$d/type.txt" ] && kind=$(tr -d '[:space:]' < "$d/type.txt")
  music=music/dark_ambient.wav; [ "$kind" = garden ] && music=music/calm_warm.wav
  title=$(cat "$d/title.txt" 2>/dev/null || true)
  echo "== $s (${kind:-anime}, $(basename "$music"))"
  if python3 scripts/make_short.py --images "$d/imgs" --voice "$d/voice.wav" --script "$d/script.txt" \
       --title "$title" --music "$music" --fit fill --out "done/$s.mp4" 2>&1 | grep -v Warning; then
    ok+=("$s")
    [ "${QA:-0}" = "1" ] && python3 scripts/qa_transcript.py "done/$s.mp4" "$d/script.txt" | head -1
  else
    failed+=("$s")
  fi
done
echo "built ${#ok[@]}: ${ok[*]:-}"
[ ${#failed[@]} -eq 0 ] || { echo "FAILED ${#failed[@]}: ${failed[*]}"; exit 1; }
