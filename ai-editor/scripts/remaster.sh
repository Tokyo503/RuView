#!/usr/bin/env bash
# Remaster an existing short per style.md v3 §3: 1080x1920, -14 LUFS, AAC 192k, trim trailing silence.
# Usage: scripts/remaster.sh input.mp4 output.mp4
set -euo pipefail
in="$1"; out="$2"
# End = last non-silent audio + 0.3 s (cap at file duration)
dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$in")
last=$(ffmpeg -hide_banner -i "$in" -af "silencedetect=n=-40dB:d=0.4" -vn -f null - 2>&1 | grep -o "silence_start: [0-9.]*" | tail -1 | cut -d' ' -f2 || true)
end=$dur
if [ -n "$last" ] && python3 -c "import sys; sys.exit(0 if $dur-$last>0.8 else 1)"; then end=$(python3 -c "print(round($last+0.3,2))"); fi
ffmpeg -loglevel error -y -i "$in" -t "$end" \
  -vf "scale=1080:1920:flags=lanczos,unsharp=5:5:0.6:5:5:0.0,fps=30" \
  -af "highpass=f=80,acompressor=threshold=-20dB:ratio=3:attack=5:release=80:makeup=2,loudnorm=I=-14:TP=-1.5:LRA=7,aresample=48000" \
  -c:v libx264 -preset medium -crf 18 -profile:v high -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart "$out"
echo "$out  (${dur}s -> ${end}s)"
