---
name: "Video Style From References"
description: "Derive a house editing style (style.md) by measuring reference reels: pacing, cuts, loudness, palette, music, hook (first 3 s). Use when the user sends reels/links they like ('خذ إلهام بس لا تنسخ') or asks to update style.md."
---

# Video Style From References

Rule: **take inspiration, don't copy.** Write the user's own rules, not a clone of a creator.

## Steps
1. Put references in `ai-editor/references/` (uploads, or `yt-dlp -o 'references/refN.%(ext)s' <url>`).
   Files from TikTok carry a ~3 s TikTok outro: exclude it from all numbers.
2. Measure each: `bash scripts/analyze_video.sh references/refN.mp4`
   → duration, resolution, scene-cut times (`scene>0.3`), silences, integrated LUFS/peak, BPM/beats, contact sheet.
   Note: crossfaded slideshows show 0 cuts; read the contact sheet instead.
3. Look at the contact sheets (Read the jpg) for palette, subject framing, overlays, transitions, text.
4. Write `ai-editor/style.md`:
   - a table of what was measured per reference
   - the common DNA they share
   - concrete rules: hook (0-3 s), structure and shot lengths, transitions (max 2 kinds, one flash), look (FFmpeg grade line), motion, music/SFX and mix target (-14 LUFS, TP ≤ -1), text, export (1080×1920, 30 fps, CRF 18, AAC 192k), safe area (bottom 15 %, right 12 %).
5. When the user's **own channel** is available, it outranks references: run the `channel-analytics` skill and base style.md on their data (v3 in this repo is channel-based).
