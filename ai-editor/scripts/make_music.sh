#!/usr/bin/env bash
# Synthesize royalty-free music beds (no copyright): dark_ambient (anime/gaming), calm_warm (gardening).
set -euo pipefail
cd "$(dirname "$0")/.."; mkdir -p music
ffmpeg -loglevel error -y -f lavfi -i "sine=f=55:d=40" -f lavfi -i "sine=f=82.4:d=40" -f lavfi -i "sine=f=110:d=40" -f lavfi -i "sine=f=164.8:d=40" -f lavfi -i "anoisesrc=color=brown:amplitude=0.3:d=40" \
  -filter_complex "[0]volume=0.5[a];[1]volume=0.35,tremolo=f=0.15:d=0.5[b];[2]volume=0.25,tremolo=f=0.2:d=0.6[c];[3]volume=0.12,tremolo=f=0.11:d=0.7[d];[4]lowpass=f=400,volume=0.4[e];[a][b][c][d][e]amix=inputs=5:normalize=0,aecho=0.8:0.7:400|900:0.35|0.25,lowpass=f=2500,afade=t=in:d=1.5,aformat=channel_layouts=stereo,loudnorm=I=-20" \
  -ar 48000 music/dark_ambient.wav
ffmpeg -loglevel error -y -f lavfi -i "sine=f=130.8:d=40" -f lavfi -i "sine=f=164.8:d=40" -f lavfi -i "sine=f=196:d=40" -f lavfi -i "sine=f=261.6:d=40" \
  -filter_complex "[0]volume=0.4,tremolo=f=0.12:d=0.3[a];[1]volume=0.3,tremolo=f=0.17:d=0.4[b];[2]volume=0.3,tremolo=f=0.1:d=0.4[c];[3]volume=0.12,tremolo=f=0.21:d=0.6[d];[a][b][c][d]amix=inputs=4:normalize=0,aecho=0.8:0.6:350|700:0.3|0.2,lowpass=f=3000,afade=t=in:d=1.5,aformat=channel_layouts=stereo,loudnorm=I=-20" \
  -ar 48000 music/calm_warm.wav
echo "music/dark_ambient.wav music/calm_warm.wav"
