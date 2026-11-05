---
name: "Short From Assets"
description: "Build one finished 1080×1920 Arabic short from images + voice (+ correct script, + optional music) with Tokyo 503 style: one image per sentence, Ken Burns, payoff punch-zoom, gold hook title, word-by-word captions, ducked music, -14 LUFS. Use when the user sends images and a voice recording, or to rebuild an old video with clean images."
---

# Short From Assets

## Inputs → `ai-editor/raw/<slug>/`
- `imgs/01.jpg … 06.jpg`: 5–7 images **without any text**, in sentence order
- `voice.wav` (or .m4a/.mp3), `script.txt` (one sentence per line, correct spelling), `title.txt` (hook question)

## Build
```bash
cd ai-editor
python3 scripts/trim_borders.py raw/<slug>/imgs/*.jpg      # strip generator border strips
python3 scripts/make_short.py --images raw/<slug>/imgs --voice raw/<slug>/voice.wav \
  --script raw/<slug>/script.txt --title "$(cat raw/<slug>/title.txt)" \
  --music music/dark_ambient.wav --fit fill --out done/<slug>.mp4
```
- `--fit blur` keeps the whole art on a blurred background (use for wide or cropped images).
- Music: `dark_ambient.wav` for anime/gaming, `calm_warm.wav` for gardening.
- Rebuilding an old video: voice = `ffmpeg -i old.mp4 -vn -c:a copy voice.m4a`; old frames contain burned captions, so generate new images instead.

## QA (always, before sending)
1. `ffmpeg -i done/<slug>.mp4 -vf "fps=1,scale=200:-1,tile=11x2" -frames:v 1 raw/_c/<slug>.jpg`, then Read it: check images match sentences, no boxes in Arabic text, correct word order, no leftover old captions or watermarks, no TikTok outro.
2. Loudness about -14 LUFS, duration within 15–24 s, ends ~0.35 s after the last word.

## Arabic caption rules (hard-won)
- Render with `ass=...:shaping=complex` (HarfBuzz). Without it ا أ د و render as boxes.
- Styles use Encoding `-1` (auto RTL base direction). Without it mixed lines like "سؤال يقسم فانز Bleach نصفين" come out in the wrong word order.
- Whisper mishears dialect and names ("أركف", "أهارة"): always pass `--script`; timings stay Whisper's.
- Font: Tajawal ExtraBold. Active word gold `#F5C542`, others white, max 3 words, 62 % height.
