#!/usr/bin/env bash
# Install + verify the editing toolchain. Run from ai-editor/. Idempotent.
set -uo pipefail
cd "$(dirname "$0")/.."
mkdir -p raw references done tts music content ~/.fonts
pip install -q yt-dlp faster-whisper piper-tts gTTS pillow 2>&1 | grep -v -i warn | tail -1
[ -d node_modules/remotion ] || npm install --silent remotion @remotion/cli @remotion/bundler @remotion/renderer react@18.3.1 react-dom@18.3.1 hyperframes >/dev/null 2>&1
fc-list | grep -i tajawal >/dev/null || { curl -sSL -o ~/.fonts/Tajawal-ExtraBold.ttf "https://cdn.jsdelivr.net/gh/google/fonts@main/ofl/tajawal/Tajawal-ExtraBold.ttf"; fc-cache -f >/dev/null; }
for f in ar_JO-kareem-medium.onnx ar_JO-kareem-medium.onnx.json; do
  [ -s tts/$f ] || curl -sSL -o tts/$f "https://huggingface.co/rhasspy/piper-voices/resolve/main/ar/ar_JO/kareem/medium/$f"
done
[ -s music/dark_ambient.wav ] && [ -s music/calm_warm.wav ] || bash scripts/make_music.sh
# verification table
T=$(mktemp -d)
chk(){ printf "%-16s %-22s %s\n" "$1" "$2" "$3"; }
ffmpeg -loglevel error -y -f lavfi -i testsrc=s=320x240:d=1 -vf "drawtext=text=ok" -frames:v 1 $T/a.png 2>/dev/null
ffmpeg -hide_banner -filters 2>/dev/null | grep " ass " >/dev/null && chk FFmpeg+libass "$(ffmpeg -version | head -1 | cut -d' ' -f3)" OK || chk FFmpeg+libass - FAIL
python3 -c "import faster_whisper" 2>/dev/null && chk faster-whisper "$(python3 -c 'import faster_whisper;print(faster_whisper.__version__)')" OK || chk faster-whisper - FAIL
chk yt-dlp "$(yt-dlp --version 2>/dev/null)" "$( [ -n "$(yt-dlp --version 2>/dev/null)" ] && echo OK || echo FAIL)"
chk Remotion "$(node -e "console.log(require('remotion/package.json').version)" 2>/dev/null)" "$( [ -d node_modules/remotion ] && echo OK || echo FAIL)"
chk HyperFrames "$(npx --no-install hyperframes --version 2>/dev/null | head -1)" "$( [ -d node_modules/hyperframes ] && echo OK || echo FAIL)"
echo "تجربة" | python3 -m piper -m tts/ar_JO-kareem-medium.onnx -f $T/v.wav >/dev/null 2>&1 && chk Piper-TTS ar_JO-kareem OK || chk Piper-TTS - FAIL
fc-list | grep -i tajawal >/dev/null && chk "Tajawal font" ExtraBold OK || chk "Tajawal font" - FAIL
