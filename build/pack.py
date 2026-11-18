#!/usr/bin/env python3
"""Quantize build/raw.png to a palette PNG at entry.png."""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
raw = ROOT / "build" / "raw.png"
out = ROOT / "entry.png"

# Flat inks median-cut drops when only a few dozen pixels use them.
PINS = [(240, 196, 0), (26, 86, 196)]  # flag gold, Korea blue

im = Image.open(raw).convert("RGB")
if im.size != (1024, 1024):
    raise SystemExit(f"raw size {im.size}, expected 1024x1024")

n_base = 128 - len(PINS)
base = im.quantize(colors=n_base, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
pal = base.getpalette()
colors = [(pal[i * 3], pal[i * 3 + 1], pal[i * 3 + 2]) for i in range(n_base)]
for pin in PINS:
    if pin not in colors:
        colors.append(pin)
flat = [channel for rgb in colors for channel in rgb]
flat.extend([0, 0, 0] * (256 - len(colors)))
palette = Image.new("P", (1, 1))
palette.putpalette(flat)
q = im.quantize(palette=palette, dither=Image.Dither.NONE)
q.save(out, format="PNG", optimize=True)

size = out.stat().st_size
check = Image.open(out)
if check.size != (1024, 1024):
    raise SystemExit(f"entry size {check.size}")
if size >= 1_000_000:
    raise SystemExit(f"entry.png is {size} bytes")
print(f"entry.png {check.size[0]}x{check.size[1]} mode={check.mode} colors={len(check.getcolors(256) or [])} bytes={size}")
