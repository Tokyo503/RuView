# AI Editor — Tokyo 503

Short-form video editing pipeline driven by Claude Code: FFmpeg + libass, faster-whisper, yt-dlp, Remotion, HyperFrames.
House style lives in [`style.md`](style.md) and is derived from measurements of the `@tokyo.966` / `@tokyo_503` channels.

## Skills
Each workflow is a Claude Code skill in `.claude/skills/`: `video-editor-setup`, `video-style-from-references`, `channel-analytics`, `shorts-remaster`, `short-from-assets`, `ai-shorts-factory`, `beat-synced-reel`.

## Setup
`bash scripts/setup.sh` (or manually:)
```bash
pip install yt-dlp faster-whisper
npm install                     # remotion, hyperframes
# Arabic captions need a font with full Arabic shaping, e.g. Tajawal ExtraBold (Google Fonts)
```
Folders (git-ignored): `raw/` input, `references/` style references, `done/` output.

## Scripts
| Script | What it does |
|---|---|
| `scripts/setup.sh` | installs + verifies every tool, font, voice and music bed; prints an OK/FAIL table |
| `scripts/analyze_video.sh` | measures a video: cuts, silences, LUFS, beats, contact sheet |
| `scripts/channel_stats.py` | channel-wide views by topic/language via yt-dlp |
| `scripts/tts.sh` | Arabic AI voice for `raw/<slug>/script.txt` (Piper, offline) |
| `scripts/make_music.sh` | synthesizes royalty-free music beds |
| `scripts/make_short.py` | images + voice (+ script, music) → finished 1080×1920 short: Whisper word timings, one image per sentence, Ken Burns + payoff punch-zoom, gold title, word-by-word Arabic captions, ducked music, -14 LUFS |
| `scripts/remaster.sh` | fixes an existing short: 1080×1920, -14 LUFS, AAC 192k, trims trailing silence |
| `scripts/gen_images.py` | generates the 6 images per video listed in `content/next-5.md` (pollinations free tier, 1 image / 45 s) |
| `scripts/trim_borders.py` | trims flat white/black border strips some generators add |
| `scripts/build_all.sh` | builds every `raw/<slug>/` project (imgs + voice.wav + script.txt + title.txt) into `done/` |
| `scripts/edit_reel1.sh` | example beat-synced music reel (cuts on a 130 BPM grid, peak on the drop) |

```bash
python3 scripts/make_short.py --images raw/proj/imgs --voice raw/proj/voice.m4a \
  --script raw/proj/script.txt --title "سؤال يقسم الفانز؟" --music raw/music.mp3 --out done/proj.mp4
scripts/remaster.sh in.mp4 done/in_remastered.mp4
```

## AI voice
Piper (`ar_JO-kareem-medium`, from Hugging Face `rhasspy/piper-voices`) runs offline:
```bash
python3 -m piper -m tts/ar_JO-kareem-medium.onnx --length-scale 0.8 --sentence-silence 0.18 -f raw/<slug>/voice.wav < raw/<slug>/script.txt
```

## Notes
- Captions are rendered with `ass=...:shaping=complex` (HarfBuzz). Without it Arabic letters such as ا أ د و render as boxes.
- Caption styles use `Encoding -1` so libass auto-detects an RTL base direction (mixed Arabic + Latin lines keep word order).
- Whisper mishears dialect names; pass `--script` to keep its timing but use the correct words.
