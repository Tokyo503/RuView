---
name: "AI Shorts Factory"
description: "Produce a whole batch of fully AI-made shorts (script, AI images, AI Arabic voice, synthesized music, captions) from a content plan, then QA and deliver them. Topics: anime, gaming, gardening only. Use when the user says 'كلها ai', asks for the next N videos, or 'استمر' after a batch."
---

# AI Shorts Factory

Owner rule: topics are **anime, gaming, gardening only** (anime and gaming → TikTok, gardening → YouTube Shorts).

## 1. Content plan → `ai-editor/content/<batch>.md`
Per video, use exactly this format (the parsers depend on it):
```
## 1) <topic name>
slug: <ascii-slug>
type: anime | game | garden
**العنوان:** <dividing question / bold claim>
**السكربت:**
1. … (6 short Saudi-dialect sentences, 45–60 words, line 1 = hook, line 6 = payoff)
**الصور:**
1. <English image prompt, one per sentence, no character names, no text>
**تعليق مثبت:** <question that drives replies>
```
Facts must be correct (canon, game history, real horticulture). Re-check each claim before writing.

## 2. Images (background: ~1.5 min each, free tier 1 image / 45 s)
`python3 scripts/gen_images.py content/<batch>.md > raw/_gen_<batch>.log 2>&1` (run_in_background).
It also writes each `raw/<slug>/script.txt` and `title.txt`, but only when it reaches that video, so extract all scripts first if voices are needed sooner.
Style by type: anime = 2D cel-shaded; game = retro arcade neon (minecraft = voxel); garden = soft photo.

## 3. Voices
`bash scripts/tts.sh <slug>` per video. If the voice runs over 23 s, rerun with `bash scripts/tts.sh <slug> 0.74`.
Piper speaks Jordanian/MSA, not Saudi: tell the user, and offer to swap in their own recordings.

## 4. Build as images finish (background loop)
For each slug: wait until 6 images exist (or the log says `ALL DONE`), then run `trim_borders.py`, then `make_short.py` with `--script/--title/--music` (dark for anime/game, calm for garden), then the contact sheet. See `short-from-assets` for the QA rules. Or run `bash scripts/build_all.sh` once all images exist.

## 5. QA + deliver
- Read every contact sheet. List weak images honestly (wrong subject, human face where pixel art was asked, etc.) and offer to regenerate them with a new prompt and seed.
- Table per video: duration, LUFS, platform. Send one preview mp4 and a `zip -0` of the batch (< 400 MB).
- Point to the pinned comments in the plan file.

## Known limits
Free pollinations output is 560×977, soft, adds a watermark (bottom 7 % cropped) and sometimes white side strips (`trim_borders.py`). It can't draw licensed characters accurately. A better image tool (Midjourney/Leonardo) plugs straight in: drop images into `raw/<slug>/imgs/`.
