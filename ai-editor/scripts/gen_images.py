#!/usr/bin/env python3
"""Generate images for content/next-5.md via pollinations (free tier: 1 image / 45 s per IP).
Writes raw/<slug>/imgs/0N.jpg, cropping the bottom 7% (watermark). Skips images already present."""
import re, subprocess, time, urllib.parse, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STYLE = ("2D anime screencap, cel shading, bold clean lineart, flat colors, dark cinematic lighting, "
         "deep navy shadows, one glowing accent color, dramatic, vertical composition, no text, no watermark")
SLUGS = ["onepiece", "naruto", "dragonball", "minecraft", "mint"]
md = open(os.path.join(ROOT, "content/next-5.md"), encoding="utf-8").read()
blocks = re.split(r"\n## \d\) ", md)[1:]
for slug, b in zip(SLUGS, blocks):
    prompts = re.findall(r"^\d\. ([a-zA-Z].*)$", b.split("**الصور:**")[1].split("**تعليق")[0], re.M)
    out = os.path.join(ROOT, "raw", slug, "imgs"); os.makedirs(out, exist_ok=True)
    style = STYLE.replace("2D anime screencap, cel shading, bold clean lineart, flat colors, dark cinematic lighting, deep navy shadows, ",
                          "soft cinematic photo, shallow depth of field, ") if slug == "mint" else STYLE
    if slug == "minecraft":
        style = "voxel blocky 3D game art style, " + style.split(", ", 3)[3]
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
