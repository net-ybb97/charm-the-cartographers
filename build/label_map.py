#!/usr/bin/env python3
"""Build the treasure map entry image.

The base artwork (assets/base.webp) is an AI-drawn antique map with no
lettering on it — generated text garbles, so every place name is
typeset here instead, in a bold serif with a parchment halo, placed
next to the feature it names. The island is the Isle of Spare Keys;
its nine labeled places are:

  Mt. Probably Harmless        the volcano (it is not harmless)
  the S.S. Wrong Turn          the ship that missed the island
  Bay of Lost Socks            the crescent bay (single socks only)
  Lake Excuses                 the pond, for why the gold is late
  The Overconfident Peaks      the mountain range
  X — Definitely Not a Trap    the hill with the X
  Forest of Mild Inconvenience the palm forest
  Kevin (he's friendly)        the whale
  here be mildly annoyed dragons   the sea serpents' waters

Output: assets/map.png at exactly 1024x1024, palette-quantised to
stay under the competition's 1 MiB gate.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / "assets" / "base.webp"
OUT = ROOT / "assets" / "map.png"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
FONT_LIGHT = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
INK = (56, 40, 22)
HALO = (233, 217, 176)

img = Image.open(BASE).convert("RGB")
W, H = img.size  # 1600x1600; labels drawn at this scale, then downscaled


def label(text, fx, fy, size, angle=0, light=False):
    """Draw one rotated label centred near fractional position (fx, fy)."""
    font = ImageFont.truetype(FONT_LIGHT if light else FONT, size)
    tmp = Image.new("RGBA", (10, 10))
    td = ImageDraw.Draw(tmp)
    box = td.textbbox((0, 0), text, font=font, stroke_width=3)
    tw, th = box[2] - box[0] + 24, box[3] - box[1] + 24
    layer = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.text((12 - box[0], 12 - box[1]), text, font=font, fill=INK + (255,),
            stroke_width=3, stroke_fill=HALO + (255,))
    layer = layer.rotate(angle, expand=True, resample=Image.BICUBIC)
    x = int(fx * W - layer.width / 2)
    y = int(fy * H - layer.height / 2)
    img.paste(layer, (x, y), layer)


label("THE ISLE OF SPARE KEYS", 0.285, 0.062, 46)
label("Mt. Probably Harmless", 0.215, 0.245, 38, angle=-4)
label("the S.S. Wrong Turn", 0.625, 0.232, 34, light=True)
label("Bay of Lost Socks", 0.175, 0.345, 38, angle=-10)
label("Lake Excuses", 0.565, 0.408, 34)
label("The Overconfident Peaks", 0.715, 0.292, 36, angle=-5)
label("X — Definitely Not a Trap", 0.335, 0.552, 36, angle=3)
label("Forest of Mild Inconvenience", 0.475, 0.822, 38)
label("here be mildly annoyed dragons", 0.235, 0.918, 32, light=True)
label("Kevin (he's friendly)", 0.615, 0.90, 32, light=True)

img = img.resize((1024, 1024), Image.LANCZOS)
img = img.quantize(colors=256, method=Image.MEDIANCUT,
                   dither=Image.FLOYDSTEINBERG)
img.save(OUT, optimize=True)
print("saved", OUT)
