---
name: "Video Editor Setup"
description: "Install and verify the AI video-editing toolchain (FFmpeg+libass, faster-whisper, yt-dlp, Remotion, HyperFrames, Piper Arabic TTS, Tajawal font, music beds) and print a tool/version/works table. Use at the start of any video session, when a tool is missing, or when the user says 'جهّز أدوات المونتاج' / 'set up the editor'."
---

# Video Editor Setup

All editing work lives in `ai-editor/` (media folders `raw/ references/ done/ mine/ tts/ music/` are git-ignored).

## Steps
1. `cd ai-editor && bash scripts/setup.sh`
   - pip: yt-dlp, faster-whisper, piper-tts, gTTS, pillow
   - npm: remotion (+cli/bundler/renderer, react 18.3.1), hyperframes
   - Tajawal ExtraBold font → `~/.fonts` (from cdn.jsdelivr.net google/fonts)
   - Piper voice `ar_JO-kareem-medium` → `tts/` (huggingface.co rhasspy/piper-voices)
   - music beds → `music/` via `scripts/make_music.sh`
2. Show the user the printed table (tool | version | OK/FAIL). Every row must be OK before editing.

## Real tests (not just "installed")
- FFmpeg: libass `ass` filter present. Remotion: `npx remotion render remotion-src/index.tsx Test out.mp4 --browser-executable=/opt/pw-browsers/chromium-*/chrome-linux*/chrome`.
- HyperFrames: `npx hyperframes render -o out.mp4` inside a folder with an `index.html` composition.

## Network (cloud sessions)
Needs these hosts allowed: `tiktok.com tiktokcdn.com tiktokv.com youtube.com googlevideo.com ytimg.com huggingface.co image.pollinations.ai cdn.jsdelivr.net`.
A 403 from the proxy = host blocked → tell the user to add it under the environment's Network access. YouTube blocks cloud IPs ("Sign in to confirm you're not a bot"); use TikTok or uploads instead.

## Gotchas
- `grep -q` + `set -o pipefail` gives false FAILs; redirect to /dev/null instead.
- faster-whisper's bundled PyAV may reject files: decode with ffmpeg to 16 kHz PCM and pass a numpy array (done in `make_short.py`).
- Skip edge-tts: speech.platform.bing.com is unreachable from cloud sessions.

## External toolkits (reviewed Nov 2026, not vendored)
Cloned for reference to `/home/user/external` (`git clone --depth 1`):
| Repo | License | Use |
|---|---|---|
| `nateherkai/herk-edit-kit` | MIT | 15 skills plus `docs/EDITING-PLAYBOOK.md` (measured reel numbers, adopted in `short-from-assets`) |
| `haidrrrry/claude-remotion-skill` | MIT | Remotion motion-graphics skill |
| `calesthio/OpenMontage` | AGPL-3.0 | 49 skills, mostly needing paid API keys. Never copy its code into this repo |
| `SWivid/Habibi-TTS` (pip `habibi-tts`) | code MIT, SAU model CC-BY-NC-SA | Saudi voice cloning, see `scripts/tts_clone.sh` |
Running their own scripts (npm install, preflight) needs the user's explicit approval: the auto-mode safety check blocks unreviewed external code. Read their docs and port ideas into `ai-editor/scripts/` instead.
