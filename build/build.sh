#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
node build/render.mjs
node /home/box/makefun/tools/shot.mjs build/page.html build/raw.png 1024 1024 18796
python3 build/pack.py
