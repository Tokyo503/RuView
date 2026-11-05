#!/usr/bin/env bash
# Arabic AI voice from raw/<slug>/script.txt -> raw/<slug>/voice.wav (Piper, offline).
# Usage: scripts/tts.sh <slug> [length_scale=0.8]   Target 15-24 s; lower length_scale (0.74) if longer.
set -euo pipefail
cd "$(dirname "$0")/.."
s=$1; ls_=${2:-0.8}
python3 -m piper -m tts/ar_JO-kareem-medium.onnx --length-scale "$ls_" --sentence-silence 0.18 -f "raw/$s/voice_raw.wav" < "raw/$s/script.txt" 2>/dev/null
ffmpeg -loglevel error -y -i "raw/$s/voice_raw.wav" -af "highpass=f=70,equalizer=f=180:t=q:w=1:g=2,equalizer=f=3500:t=q:w=1.5:g=2,aresample=48000" "raw/$s/voice.wav"
printf "%s %.1fs\n" "$s" "$(ffprobe -v error -show_entries format=duration -of csv=p=0 "raw/$s/voice.wav")"
