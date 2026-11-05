#!/usr/bin/env bash
# Measure a reference/own video: duration, size, scene cuts, silences, loudness, contact sheet.
# Usage: scripts/analyze_video.sh file.mp4 [outdir]
set -uo pipefail
f=$1; out=${2:-$(dirname "$f")/_analysis}; mkdir -p "$out"; b=$(basename "$f" .mp4)
ffprobe -v error -show_entries format=duration:stream=codec_type,width,height,r_frame_rate -of compact "$f"
echo "cuts: $(ffmpeg -hide_banner -i "$f" -vf "select='gt(scene,0.3)',showinfo" -an -f null - 2>&1 | grep -o 'pts_time:[0-9.]*' | cut -d: -f2 | tr '\n' ' ')"
ffmpeg -hide_banner -i "$f" -af "silencedetect=n=-35dB:d=0.3,ebur128=peak=true" -vn -f null - 2>&1 | grep -E "silence_(start|end)|^ +(I|LRA|Peak):"
ffmpeg -loglevel error -y -i "$f" -vf "fps=1,scale=200:-1,tile=8x4" -frames:v 1 "$out/$b.jpg" && echo "contact sheet: $out/$b.jpg"
echo "beats: $(npx --no-install hyperframes beats "$f" --json 2>/dev/null | python3 -c 'import json,sys;d=json.load(sys.stdin);print(d.get("bpm"),"bpm",len(d.get("beatTimes",[])),"beats")' 2>/dev/null || echo n/a)"
