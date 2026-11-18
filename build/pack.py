#!/usr/bin/env python3
"""Quantize build/raw.png to a palette PNG at entry.png."""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
raw = ROOT / "build" / "raw.png"
out = ROOT / "entry.png"

im = Image.open(raw).convert("RGB")
if im.size != (1024, 1024):
    raise SystemExit(f"raw size {im.size}, expected 1024x1024")

q = im.quantize(colors=128, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
q.save(out, format="PNG", optimize=True)

size = out.stat().st_size
check = Image.open(out)
if check.size != (1024, 1024):
    raise SystemExit(f"entry size {check.size}")
if size >= 1_000_000:
    raise SystemExit(f"entry.png is {size} bytes")
print(f"entry.png {check.size[0]}x{check.size[1]} mode={check.mode} colors={len(check.getcolors(256) or [])} bytes={size}")
