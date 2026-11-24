#!/usr/bin/env python3
"""Compose the labelled treasure map for "Charm the Cartographers".

The AI-generated base (assets/base.webp) carries no lettering, because
generated text comes out garbled. All wording is set here instead:
each place name is rendered in DejaVu Serif (bold for the landmarks,
regular for the asides) with dark ink and a parchment-coloured halo so
it stays readable over the busy map artwork.

Labels are described in a table below as (text, x, y, point size,
rotation in degrees, light?) where x/y are fractions of the canvas
edge, so the layout scales with the base image. After every label is
drawn, the canvas is downscaled to 1024x1024 and palette-quantised to
256 colours so the PNG stays comfortably under the 1 MiB size gate.

Run:  python3 build/label_map.py   (writes assets/map.png)
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SRC = ROOT / "assets" / "base.webp"
DST = ROOT / "assets" / "map.png"

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"

INK = (56, 40, 22)
GLOW = (233, 217, 176)
STROKE = 3
PAD = 14

# text, centre-x, centre-y, size, angle, light (regular instead of bold)
LABELS = [
    ("THE ISLE OF SPARE KEYS", 0.285, 0.062, 46, 0, False),
    ("Mt. Probably Harmless", 0.215, 0.245, 38, -4, False),
    ("the S.S. Wrong Turn", 0.625, 0.232, 34, 0, True),
    ("Bay of Lost Socks", 0.175, 0.345, 38, -10, False),
    ("Lake Excuses", 0.565, 0.408, 34, 0, False),
    ("The Overconfident Peaks", 0.715, 0.292, 36, -5, False),
    ("X — Definitely Not a Trap", 0.335, 0.552, 36, 3, False),
    ("Forest of Mild Inconvenience", 0.475, 0.822, 38, 0, False),
    ("here be mildly annoyed dragons", 0.235, 0.918, 32, 0, True),
    ("Kevin (he's friendly)", 0.615, 0.90, 32, 0, True),
]


def make_label_layer(text, size, light):
    """Render one label onto its own transparent layer."""
    font = ImageFont.truetype(REGULAR if light else BOLD, size)
    probe = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    left, top, right, bottom = probe.textbbox(
        (0, 0), text, font=font, stroke_width=STROKE)
    layer = Image.new(
        "RGBA", (right - left + 2 * PAD, bottom - top + 2 * PAD),
        (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    draw.text((PAD - left, PAD - top), text, font=font,
              fill=INK + (255,), stroke_width=STROKE,
              stroke_fill=GLOW + (255,))
    return layer


def compose():
    canvas = Image.open(SRC).convert("RGB")
    width, height = canvas.size
    for text, fx, fy, size, angle, light in LABELS:
        layer = make_label_layer(text, size, light)
        if angle:
            layer = layer.rotate(angle, expand=True,
                                 resample=Image.BICUBIC)
        px = round(fx * width - layer.width / 2)
        py = round(fy * height - layer.height / 2)
        canvas.paste(layer, (px, py), layer)
    return canvas


def main():
    canvas = compose()
    canvas = canvas.resize((1024, 1024), Image.LANCZOS)
    palette_img = canvas.quantize(
        colors=256, method=Image.MEDIANCUT, dither=Image.FLOYDSTEINBERG)
    palette_img.save(DST, optimize=True)
    size = DST.stat().st_size
    print(f"wrote {DST} ({size} bytes)")
    assert size < 1024 * 1024, "map.png exceeds the 1 MiB gate"


if __name__ == "__main__":
    main()
