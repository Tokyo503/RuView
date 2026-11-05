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
- **Pacing (recommended): `--max-shot 2.0`** splits long shots into punch-ins of the same image (1.42×/1.28×/1.55×, offset framing), so the average shot is about 1.4 s and the first cut lands at 0.9 s. Measured target from herk-edit-kit's playbook: avg 1.1–1.4 s, none over 2.8 s, first cut 0.6–1.0 s.
- **`--caption-box`** puts captions in a dark 25 %-transparent box, readable on any background ("never white on light").
- `--fit blur` keeps the whole art on a blurred background (use for wide or cropped images).
- Music: `dark_ambient.wav` for anime/gaming, `calm_warm.wav` for gardening.
- Rebuilding an old video: voice = `ffmpeg -i old.mp4 -vn -c:a copy voice.m4a`; old frames contain burned captions, so generate new images instead.

## QA (always, before sending)
1. `ffmpeg -i done/<slug>.mp4 -vf "fps=1,scale=200:-1,tile=11x2" -frames:v 1 raw/_c/<slug>.jpg`, then Read it: check images match sentences, no boxes in Arabic text, correct word order, no leftover old captions or watermarks, no TikTok outro.
2. Every word is whole: `python3 scripts/qa_transcript.py done/<slug>.mp4 raw/<slug>/script.txt`. Expect ≥ 75 % (dialect TTS plus Whisper never hits 100 %). Below 70 %, listen for a clipped or garbled line.
3. Loudness about -14 LUFS, duration within 15–24 s, ends ~0.35 s after the last word.

## Arabic caption rules (hard-won)
- Render with `ass=...:shaping=complex` (HarfBuzz). Without it ا أ د و render as boxes.
- Styles use Encoding `-1` (auto RTL base direction). Without it mixed lines like "سؤال يقسم فانز Bleach نصفين" come out in the wrong word order.
- Whisper mishears dialect and names ("أركف", "أهارة"): always pass `--script`; timings stay Whisper's.
- Font: Tajawal ExtraBold. Active word gold `#F5C542`, others white, max 3 words, 62 % height.
