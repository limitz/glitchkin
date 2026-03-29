#!/usr/bin/env python3
"""
LTG_TOOL_styleframe_luma_byte_v002.py
Style Frame 04 "The Dynamic" — Luma + Byte Interaction v002
"Luma & the Glitchkin" — Cycle 27 / Sam Kowalski

C32 STUB FIX (Kai Nakamura):
  Original: LTG_COLOR_styleframe_luma_byte_v002.py (deleted by C29 naming cleanup)
  The original generator code is not recoverable. The output PNG is preserved at:
    output/color/style_frames/LTG_COLOR_styleframe_luma_byte_v002.png

  This generator is a preservation stub: it locates the existing output PNG and
  re-saves it to the canonical output path. This ensures the generator runs
  without error and produces the correct output without requiring the deleted source.

  Per pitch_package_index.md: SF04 v002 was a procedural quality upgrade (C27).
  Superseded by v003 (C28 — Rin Yamamoto).

Output: output/color/style_frames/LTG_COLOR_styleframe_luma_byte_v002.png
"""

import os
import sys
from PIL import Image

_TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.dirname(_TOOLS_DIR)

OUTPUT_PATH = os.path.join(_PROJECT_ROOT, "color", "style_frames",
                           "LTG_COLOR_styleframe_luma_byte_v002.png")


def generate(output_path=None):
    """
    Preservation stub: re-saves the existing v002 output PNG.
    The original generator was deleted by C29 cleanup; artwork is preserved.
    """
    if output_path is None:
        output_path = OUTPUT_PATH

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    if os.path.exists(output_path):
        img = Image.open(output_path)
        img.thumbnail((1280, 1280), Image.LANCZOS)
        img.save(output_path)
        print(f"Re-saved (identity): {output_path}  ({img.size[0]}x{img.size[1]}px)")
        return img

    print(f"WARNING: Source PNG not found at {output_path}")
    print("Generating placeholder. Original generator was deleted C29.")
    from PIL import ImageDraw, ImageFont
    W, H = 1280, 720
    img = Image.new("RGB", (W, H), (20, 15, 35))
    draw = ImageDraw.Draw(img)
    for y in range(0, H, 4):
        alpha_band = int(10 + 15 * abs(y - H // 2) / (H // 2))
        draw.line([(0, y), (W, y)], fill=(0, max(0, 30 - alpha_band), max(0, 50 - alpha_band)))
    draw.text((W // 2 - 200, H // 2 - 40),
              "SF04 — Luma + Byte Dynamic v002",
              fill=(0, 212, 232), font=ImageFont.load_default())
    draw.text((W // 2 - 180, H // 2),
              "Original generator deleted C29 — placeholder",
              fill=(150, 140, 130), font=ImageFont.load_default())
    img.save(output_path)
    print(f"Saved placeholder: {output_path}")
    return img


def main():
    generate()


if __name__ == "__main__":
    main()
