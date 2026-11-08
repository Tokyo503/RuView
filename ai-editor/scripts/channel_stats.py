#!/usr/bin/env python3
"""Channel analytics: list every video with yt-dlp, group views by topic + language.
Usage: channel_stats.py <channel_url> [more urls...]   e.g. https://www.tiktok.com/@tokyo.966
Writes mine/<host>_list.txt (id|views|duration|title) and prints per-topic avg/median."""
import re, subprocess, statistics as st, sys, os
CATS = {"anime": r"ون بيس|دراغون|بليتش|Bleach|ناروتو|أنمي|anime|غوكو|أكاينو|هانتر|جوجوتسو|غوجو|قاتل الشياطين|تانجيرو|سولو",
        "games": r"GTA|ماين كرافت|لاست أوف|لعبة|بلايستيشن|Minecraft|زيلدا|ماريو|باك مان|كول أوف|سايبربانك|EA Sports",
        "garden": r"بلكونة|زراعة|شتلة|أصيص|الفراولة|السبانخ|الفلفل|نباتات|الطماطم|ريحان|الخس|نعناع|الثوم|البصل"}
os.makedirs("mine", exist_ok=True)
for url in sys.argv[1:]:
    host = re.sub(r"\W+", "_", url.split("//")[-1])[:40]
    out = subprocess.run(["yt-dlp", "--no-warnings", "--flat-playlist", "--print",
                          "%(id)s|%(view_count)s|%(duration)s|%(title).80s", url], capture_output=True, text=True).stdout
    open(f"mine/{host}_list.txt", "w").write(out)
    rows = [l.split("|", 3) for l in out.splitlines() if l.count("|") >= 3]
    print(f"== {url}: {len(rows)} videos")
    g = {}
    for vid, v, d, t in rows:
        c = next((k for k, p in CATS.items() if re.search(p, t, re.I)), "other")
        lang = "AR" if re.search(r"[؀-ۿ]", t) else "EN"
        g.setdefault((c, lang), []).append(int(v) if v.isdigit() else 0)
    for (c, l), vs in sorted(g.items(), key=lambda x: -st.mean(x[1])):
        print(f"  {c:7} {l} n={len(vs):3} avg={st.mean(vs):6.0f} median={st.median(vs):5.0f} max={max(vs)}")
    vs = [int(r[1]) if r[1].isdigit() else 0 for r in rows]
    if len(vs) > 50: print(f"  newest 50 avg {st.mean(vs[:50]):.0f} | older avg {st.mean(vs[50:]):.0f}")
