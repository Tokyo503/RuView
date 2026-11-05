#!/usr/bin/env bash
# Saudi-dialect AI voice that clones a reference voice (Habibi-TTS, Specialized SAU model, F5-TTS based).
# Usage: scripts/tts_clone.sh <slug> [ref.wav] ["ref transcript"] [speed=1.0]
# Default ref = tts/habibi/ref_tokyo.wav (owner's own voice, first 7.2 s of the Aizen short).
# LICENSE: the SAU model is CC-BY-NC-SA-4.0 (non-commercial). Monetised/sponsored posts need another voice.
# Install once: python3 -m venv --system-site-packages /root/hbenv && /root/hbenv/bin/pip install -U pip setuptools wheel habibi-tts \
#   && /root/hbenv/bin/pip install torchaudio==2.8.0 --index-url https://download.pytorch.org/whl/cpu
set -euo pipefail
cd "$(dirname "$0")/.."
s=$1; ref=${2:-tts/habibi/ref_tokyo.wav}
reftxt=${3:-"ليش آيزن ما طلع بانكاي ولا مرة؟ لأن البانكاي سقف الشينيغامي. وأي شينيغامي قوي لازم يوصله."}
speed=${4:-1.0}
/root/hbenv/bin/habibi-tts_infer-cli -m Specialized -d SAU -r "$ref" -s "$reftxt" -f "raw/$s/script.txt" \
  --nfe_step 32 --speed "$speed" --remove_silence --device cpu -o "raw/$s" -w voice_raw.wav 2>&1 | grep -E "^Error|Traceback" || true
ffmpeg -loglevel error -y -i "raw/$s/voice_raw.wav" -af "highpass=f=70,aresample=48000" "raw/$s/voice.wav"
printf "%s %.1fs\n" "$s" "$(ffprobe -v error -show_entries format=duration -of csv=p=0 "raw/$s/voice.wav")"
