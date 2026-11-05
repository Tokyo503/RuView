# Tokyo 503 — Editing Style (v3)

Built from **my own channels**: TikTok `@tokyo.966` (224 videos) and YouTube `@tokyo_503` (367 shorts).
Stats are over all 591 videos. 37 TikToks (top 20 + newest 20) were measured with FFmpeg and transcribed with Whisper.
The anime reels in `references/` remain a visual mood board only.

## 1. What the data says
| Finding | Evidence |
|---|---|
| **Arabic wins by far** | TikTok: Arabic averages 220–320 views vs. 4–71 for English. YouTube: the top Arabic topics average 180–340 vs. 78–130 for English. |
| **Best topics** | TikTok: anime (avg 321, median 222), then general Arabic (300), games (224), balcony gardening (224). YouTube: gardening (avg 339), Arabic history (204), games (180), anime (178). |
| **Getting better** | Newest 50 vs. older: TikTok 370 vs. 190, YouTube 278 vs. 118 average views. The current format works, so keep it. |
| **Top hooks are questions/controversy** | "سؤال يقسم فانز Bleach نصفين", "أظلم آرك في ون بيس بلا معركة", "كل واحد يسأل مين بيلقى الكنز…" |
| **Ideal length** | Top 10 TikToks are 14–24 s (median 19 s). 100+ s news videos flopped. |

## 2. The current format (keep it)
- 9:16. 3–4 AI-generated illustrations per video, joined with slow crossfades (~4–6 s per image).
- Saudi-dialect voice-over, voice only, no music.
- Gold question title at the top for the first ~4 s.
- Word-by-word captions in the centre-bottom: white with the current word in gold.
- "Tokyo 503" signature in gold at the bottom, plus a thin gold rule.
- Slow Ken Burns on each image. Dark scene + one hot colour (fire orange, purple lightning, gold).
- The last line is the "payoff" (e.g. "الغياب نفسه هو الجواب").

## 3. What to fix (measured problems)
1. **Audio too quiet:** measured -22 to -25 LUFS on all 37. TikTok/Shorts play at about -14 LUFS, so the videos sound weak next to others. **Target -14 LUFS, true peak ≤ -1 dBTP.**
2. **Audio bitrate 32 kbps:** the voice sounds thin. Export AAC 192 kbps.
3. **Resolution 576×1024:** export 1080×1920.
4. **Silence after the voice:** the top video has about 4 s of dead air at the end. End 0.3 s after the last word.
5. **Captions are small:** make them about 2× larger, max 3 words, in the lower-middle safe zone.
6. **Slow first image:** a 4–5 s static first shot loses viewers. Change the image (or punch-zoom) by 2.5 s, then every 2.5–4 s.
7. **No music:** add a quiet ambient/epic bed (-28 dB under the voice, ducked) that matches the topic.

## 4. Rules for every new short
### Script (15–22 s, ~45–60 words)
- Line 1 = a question or a bold claim that splits the audience (≤ 2.5 s).
- 3–4 short sentences of build-up, one fact each.
- Final line = a twist/payoff, then **stop**. No outro, no "follow for more".
- Pinned comment question to drive replies.

### Visuals
- 5–7 images: one per sentence. Cut or quick 6-frame dissolve exactly on the sentence boundary.
- Ken Burns 4–8 % per image. Punch-zoom (+10 % in 4 frames) on the key word of the payoff.
- Same colour family across all images. One flash or glow only at the payoff.

### Text
- Title (top, gold `#F5C542`, bold, black stroke): the hook question, 0–3 s only.
- Captions: word-by-word from Whisper timings, white + gold active word, black stroke, centred at 62 % height, ≤ 3 words.
- Signature "Tokyo 503" small, gold, bottom-centre, above the TikTok UI safe area (bottom 15 %).

### Audio
- Voice: highpass 80 Hz, light compression, loudnorm → -14 LUFS.
- Music bed under the voice at -28 dB with sidechain ducking. Music swells for 1 s after the last word.

### Export
- 1080×1920, 30 fps, H.264 High CRF 18, AAC 192 kbps, `+faststart`, into `done/`.

### Topic plan (from the data)
- TikTok: anime theories (One Piece, Bleach, Dragon Ball, Naruto) plus game opinions.
- YouTube Shorts: balcony gardening in Riyadh plus Arabic history/legends.
- Stop English news content.
