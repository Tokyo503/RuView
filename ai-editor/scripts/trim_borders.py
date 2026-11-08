#!/usr/bin/env python3
"""Trim flat (near-uniform) border strips that some generators add. Usage: trim_borders.py img [img ...]"""
import sys
from PIL import Image

def flat(im, box):
    """A strip is a border if >=80% of its pixels are near-white, or >=95% near-black."""
    px = list(im.crop(box).convert("L").getdata())
    n = len(px)
    return sum(v > 200 for v in px) / n >= 0.8 or sum(v < 12 for v in px) / n >= 0.95

for p in sys.argv[1:]:
    im = Image.open(p); w, h = im.size
    l, t, r, b = 0, 0, w, h
    while r - l > w * 0.8 and flat(im, (r - 2, t, r, b)): r -= 2
    while r - l > w * 0.8 and flat(im, (l, t, l + 2, b)): l += 2
    while b - t > h * 0.8 and flat(im, (l, b - 2, r, b)): b -= 2
    while b - t > h * 0.8 and flat(im, (l, t, r, t + 2)): t += 2
    if (l, t, r, b) != (0, 0, w, h):
        m = 4  # small safety margin past the strip's soft edge
        im.crop((l + (m if l else 0), t + (m if t else 0), r - (m if r < w else 0), b - (m if b < h else 0))).save(p, quality=95)
        print(f"trimmed {p}: {w}x{h} -> box {l},{t},{r},{b}")
