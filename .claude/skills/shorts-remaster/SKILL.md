---
name: "Shorts Remaster"
description: "Batch-fix existing published shorts: upscale to 1080×1920, voice chain + loudnorm to -14 LUFS (TP -1.5), AAC 192 kbps, trim dead air after the last word. Use when the user wants old videos improved ('حسّن فيديوهاتي القديمة') without re-editing."
---

# Shorts Remaster

## Steps
1. One file: `cd ai-editor && bash scripts/remaster.sh in.mp4 done/remastered/<name>.mp4`
2. Batch (run in background):
   `for f in mine/tiktok/*.mp4; do id=$(basename $f .mp4); [ -f done/remastered/$id.mp4 ] || bash scripts/remaster.sh $f done/remastered/$id.mp4; done`
3. Verify every output: integrated loudness between -13.5 and -15 LUFS, 1080×1920:
   `ffmpeg -i X -af ebur128=peak=true -f null - 2>&1 | grep -E "I:|Peak:"`
4. Deliver: zip with `zip -0`. Keep each zip under 400 MB (the send limit), so split into parts.

## Limits (say so to the user)
Burned-in captions and slow first shots can't be fixed by remastering; those need a rebuild with `short-from-assets`.
Re-uploading identical content can be flagged as a duplicate: replace the old post, or re-post the remaster as a new version.
