# AI Editor — Tokyo 503

Short-form video editing pipeline driven by Claude Code: FFmpeg + libass, faster-whisper, yt-dlp, Remotion, HyperFrames.
House style lives in [`style.md`](style.md) and is derived from measurements of the `@tokyo.966` / `@tokyo_503` channels.

## Setup
```bash
pip install yt-dlp faster-whisper
npm install                     # remotion, hyperframes
# Arabic captions need a font with full Arabic shaping, e.g. Tajawal ExtraBold (Google Fonts)
```
Folders (git-ignored): `raw/` input, `references/` style references, `done/` output.

## Scripts
| Script | What it does |
|---|---|
| `scripts/make_short.py` | images + voice (+ script, music) → finished 1080×1920 short: Whisper word timings, one image per sentence, Ken Burns + payoff punch-zoom, gold title, word-by-word Arabic captions, ducked music, -14 LUFS |
| `scripts/remaster.sh` | fixes an existing short: 1080×1920, -14 LUFS, AAC 192k, trims trailing silence |
| `scripts/edit_reel1.sh` | example beat-synced music reel (cuts on a 130 BPM grid, peak on the drop) |

```bash
python3 scripts/make_short.py --images raw/proj/imgs --voice raw/proj/voice.m4a \
  --script raw/proj/script.txt --title "سؤال يقسم الفانز؟" --music raw/music.mp3 --out done/proj.mp4
scripts/remaster.sh in.mp4 done/in_remastered.mp4
```

## Notes
- Captions are rendered with `ass=...:shaping=complex` (HarfBuzz). Without it Arabic letters such as ا أ د و render as boxes.
- Whisper mishears dialect names; pass `--script` to keep its timing but use the correct words.
