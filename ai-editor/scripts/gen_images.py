#!/usr/bin/env python3
"""Generate images for a content plan via pollinations (free tier: 1 image / 45 s per IP).
Usage: gen_images.py [content/plan.md]   (default content/next-5.md)
Each video section is "## N) ..." with a "slug:" line (else the legacy slug list is used) and a
"**الصور:**" list. Writes raw/<slug>/imgs/0N.jpg (bottom 7% cropped for the watermark), plus
raw/<slug>/script.txt and title.txt. Skips images already present."""
import re, subprocess, time, urllib.parse, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STYLE = ("2D anime screencap, cel shading, bold clean lineart, flat colors, dark cinematic lighting, "
         "deep navy shadows, one glowing accent color, dramatic, vertical composition, no text, no watermark")
LEGACY = ["onepiece", "naruto", "dragonball", "minecraft", "mint"]
plan = sys.argv[1] if len(sys.argv) > 1 else "content/next-5.md"
md = open(os.path.join(ROOT, plan), encoding="utf-8").read()
blocks = re.split(r"\n## \d+\) ", md)[1:]
for n, b in enumerate(blocks):
    m = re.search(r"^slug: *([a-z0-9_-]+)", b, re.M)
    slug = m.group(1) if m else LEGACY[n]
    kind = (re.search(r"^type: *(\w+)", b, re.M) or [None, "anime"])[1]
    os.makedirs(os.path.join(ROOT, "raw", slug), exist_ok=True)
    title = re.search(r"\*\*العنوان:\*\* (.+)", b).group(1).strip()
    lines = re.findall(r"^\d\. (.*[\u0600-\u06FF].*)$", b.split("**السكربت:**")[1].split("**الصور:**")[0], re.M)
    open(os.path.join(ROOT, "raw", slug, "title.txt"), "w", encoding="utf-8").write(title)
    open(os.path.join(ROOT, "raw", slug, "script.txt"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
    prompts = re.findall(r"^\d\. ([a-zA-Z].*)$", b.split("**الصور:**")[1].split("**تعليق")[0], re.M)
    out = os.path.join(ROOT, "raw", slug, "imgs"); os.makedirs(out, exist_ok=True)
    style = STYLE.replace("2D anime screencap, cel shading, bold clean lineart, flat colors, dark cinematic lighting, deep navy shadows, ",
                          "soft cinematic photo, shallow depth of field, ") if (slug == "mint" or kind == "garden") else STYLE
    if slug == "minecraft":
        style = "voxel blocky 3D game art style, " + style.split(", ", 3)[3]
    elif kind == "game":
        style = "retro arcade video game art, glowing neon on dark background, crisp pixel details, dramatic, vertical composition, no text, no watermark"
    for i, p in enumerate(prompts, 1):
        dst = os.path.join(out, f"{i:02d}.jpg")
        if os.path.exists(dst):
            continue
        url = ("https://image.pollinations.ai/prompt/" + urllib.parse.quote(f"{p}, {style}")
               + f"?width=768&height=1440&nologo=true&model=flux&seed={503 + i}")
        for attempt in range(6):
            tmp = dst + ".part"
            subprocess.run(["curl", "-s", "--max-time", "180", "-o", tmp, url])
            ok = subprocess.run(["file", tmp], capture_output=True, text=True).stdout
            if "JPEG" in ok:
                subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", tmp, "-vf", "crop=iw:ih*0.93:0:0", dst])
                os.remove(tmp); print(slug, i, "ok", flush=True); break
            time.sleep(47)
        else:
            print(slug, i, "FAILED", flush=True)
        time.sleep(47)
print("ALL DONE")
