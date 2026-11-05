---
name: "Channel Analytics"
description: "Analyse the user's own TikTok/YouTube channel: list every video, views by topic and language, newest-vs-older trend, top hooks, ideal length, and measured technical problems (loudness, bitrate, resolution, dead air). Use when the user shares their channel link or asks what works on their account."
---

# Channel Analytics

## Steps
1. Stats over **all** videos: `cd ai-editor && python3 scripts/channel_stats.py https://www.tiktok.com/@<user> [https://www.youtube.com/@<user>/shorts]`
   Topic regexes live in `CATS` (anime / games / garden); extend them for new topics.
2. Sample to measure: top 20 by views + newest 20 (deduplicated):
   `yt-dlp --write-info-json -o "mine/tiktok/%(id)s.%(ext)s" -a list.txt` (YouTube usually refuses cloud IPs).
3. For each sample: `bash scripts/analyze_video.sh mine/tiktok/<id>.mp4` and collect views, likes, length, cuts, LUFS, size.
4. Transcribe 2–3 top videos with Whisper (`small`, language `ar`) to learn the hook and the payoff pattern.
5. Report to the user (Arabic), as tables:
   - what wins (language, topics, length, hook type), trend newest vs older
   - measured problems with numbers, e.g. "-24 LUFS vs -14 target", "32 kbps audio", "576×1024", "3.5 s silence at end"
   - what to keep, what to fix, the topic plan
6. Update `style.md` (sections: data, current format, fixes, rules, topic plan).

## Findings for @tokyo.966 / @tokyo_503 (Nov 2026)
Arabic ≫ English. Best topics: anime (TikTok), gardening (YouTube), gaming. Top length 14–24 s. Hooks are dividing questions. All videos were about -23 LUFS at 32 kbps. Owner decision: **anime, gaming, gardening only.**
