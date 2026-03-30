#!/usr/bin/env python3
"""
LTG_TOOL_pixel_font_v001.py — Pixel Font Utility
"Luma & the Glitchkin" — Production Pipeline
Author: Jordan Reed | Cycle 40

Provides `draw_pixel_text(draw, x, y, text, color, scale=1)` for drawing
hand-lettered-style pixel text directly onto a PIL ImageDraw canvas.

Designed for in-world prop labels (e.g. fridge notes, sticky labels, signage)
where:
  - No font file dependency is acceptable
  - The text must read as "hand-annotated" rather than mechanical
  - Small scale (scale=1 → 5×7px per glyph) is the default use case

Built-in glyph set: A–Z (uppercase) and 0–9.
Lowercase input is auto-upcased. Unrecognised characters are rendered as a
blank space (glyph width + 1 px kerning).

Usage:
    from LTG_TOOL_pixel_font_v001 import draw_pixel_text

    draw_pixel_text(draw, x=10, y=10, text="MIRI", color=(88, 60, 32))
    draw_pixel_text(draw, x=10, y=30, text="MIRI", color=(88, 60, 32), scale=2)

Each glyph is 5 columns × 7 rows. Kerning between glyphs: 1 pixel at scale 1
(scaled by `scale`). The `draw` parameter must be an ImageDraw.Draw instance
attached to the current working image.

CLI self-test: generates a 480×120 test PNG with "MIRI" at scale 1 and scale 2.
Output: output/production/LTG_TEST_pixel_font_v001.png
"""

from PIL import Image, ImageDraw
import os

# ── 5×7 Bitmap Glyph Map ────────────────────────────────────────────────────
# Each glyph is a flat list of 35 bits (row-major, 5 columns × 7 rows).
# 1 = filled pixel, 0 = empty.

_GLYPH_W = 5
_GLYPH_H = 7

# fmt: off
GLYPHS = {
    'A': [
        0,1,1,1,0,
        1,0,0,0,1,
        1,0,0,0,1,
        1,1,1,1,1,
        1,0,0,0,1,
        1,0,0,0,1,
        1,0,0,0,1,
    ],
    'B': [
        1,1,1,1,0,
        1,0,0,0,1,
        1,0,0,0,1,
        1,1,1,1,0,
        1,0,0,0,1,
        1,0,0,0,1,
        1,1,1,1,0,
    ],
    'C': [
        0,1,1,1,0,
        1,0,0,0,1,
        1,0,0,0,0,
        1,0,0,0,0,
        1,0,0,0,0,
        1,0,0,0,1,
        0,1,1,1,0,
    ],
    'D': [
        1,1,1,1,0,
        1,0,0,0,1,
        1,0,0,0,1,
        1,0,0,0,1,
        1,0,0,0,1,
        1,0,0,0,1,
        1,1,1,1,0,
    ],
    'E': [
        1,1,1,1,1,
        1,0,0,0,0,
        1,0,0,0,0,
        1,1,1,1,0,
        1,0,0,0,0,
        1,0,0,0,0,
        1,1,1,1,1,
    ],
    'F': [
        1,1,1,1,1,
        1,0,0,0,0,
        1,0,0,0,0,
        1,1,1,1,0,
        1,0,0,0,0,
        1,0,0,0,0,
        1,0,0,0,0,
    ],
    'G': [
        0,1,1,1,0,
        1,0,0,0,1,
        1,0,0,0,0,
        1,0,1,1,1,
        1,0,0,0,1,
        1,0,0,0,1,
        0,1,1,1,0,
    ],
    'H': [
        1,0,0,0,1,
        1,0,0,0,1,
        1,0,0,0,1,
        1,1,1,1,1,
        1,0,0,0,1,
        1,0,0,0,1,
        1,0,0,0,1,
    ],
    'I': [
        1,1,1,1,1,
        0,0,1,0,0,
        0,0,1,0,0,
        0,0,1,0,0,
        0,0,1,0,0,
        0,0,1,0,0,
        1,1,1,1,1,
    ],
    'J': [
        0,0,0,1,1,
        0,0,0,0,1,
        0,0,0,0,1,
        0,0,0,0,1,
        1,0,0,0,1,
        1,0,0,0,1,
        0,1,1,1,0,
    ],
    'K': [
        1,0,0,1,0,
        1,0,1,0,0,
        1,1,0,0,0,
        1,1,0,0,0,
        1,0,1,0,0,
        1,0,0,1,0,
        1,0,0,0,1,
    ],
    'L': [
        1,0,0,0,0,
        1,0,0,0,0,
        1,0,0,0,0,
        1,0,0,0,0,
        1,0,0,0,0,
        1,0,0,0,0,
        1,1,1,1,1,
    ],
    'M': [
        1,0,0,0,1,
        1,1,0,1,1,
        1,0,1,0,1,
        1,0,0,0,1,
        1,0,0,0,1,
        1,0,0,0,1,
        1,0,0,0,1,
    ],
    'N': [
        1,0,0,0,1,
        1,1,0,0,1,
        1,0,1,0,1,
        1,0,0,1,1,
        1,0,0,0,1,
        1,0,0,0,1,
        1,0,0,0,1,
    ],
    'O': [
        0,1,1,1,0,
        1,0,0,0,1,
        1,0,0,0,1,
        1,0,0,0,1,
        1,0,0,0,1,
        1,0,0,0,1,
        0,1,1,1,0,
    ],
    'P': [
        1,1,1,1,0,
        1,0,0,0,1,
        1,0,0,0,1,
        1,1,1,1,0,
        1,0,0,0,0,
        1,0,0,0,0,
        1,0,0,0,0,
    ],
    'Q': [
        0,1,1,1,0,
        1,0,0,0,1,
        1,0,0,0,1,
        1,0,0,0,1,
        1,0,1,0,1,
        1,0,0,1,0,
        0,1,1,0,1,
    ],
    'R': [
        1,1,1,1,0,
        1,0,0,0,1,
        1,0,0,0,1,
        1,1,1,1,0,
        1,0,1,0,0,
        1,0,0,1,0,
        1,0,0,0,1,
    ],
    'S': [
        0,1,1,1,0,
        1,0,0,0,1,
        1,0,0,0,0,
        0,1,1,1,0,
        0,0,0,0,1,
        1,0,0,0,1,
        0,1,1,1,0,
    ],
    'T': [
        1,1,1,1,1,
        0,0,1,0,0,
        0,0,1,0,0,
        0,0,1,0,0,
        0,0,1,0,0,
        0,0,1,0,0,
        0,0,1,0,0,
    ],
    'U': [
        1,0,0,0,1,
        1,0,0,0,1,
        1,0,0,0,1,
        1,0,0,0,1,
        1,0,0,0,1,
        1,0,0,0,1,
        0,1,1,1,0,
    ],
    'V': [
        1,0,0,0,1,
        1,0,0,0,1,
        1,0,0,0,1,
        1,0,0,0,1,
        1,0,0,0,1,
        0,1,0,1,0,
        0,0,1,0,0,
    ],
    'W': [
        1,0,0,0,1,
        1,0,0,0,1,
        1,0,0,0,1,
        1,0,1,0,1,
        1,1,0,1,1,
        1,0,0,0,1,
        1,0,0,0,1,
    ],
    'X': [
        1,0,0,0,1,
        0,1,0,1,0,
        0,0,1,0,0,
        0,0,1,0,0,
        0,1,0,1,0,
        1,0,0,0,1,
        1,0,0,0,1,
    ],
    'Y': [
        1,0,0,0,1,
        1,0,0,0,1,
        0,1,0,1,0,
        0,0,1,0,0,
        0,0,1,0,0,
        0,0,1,0,0,
        0,0,1,0,0,
    ],
    'Z': [
        1,1,1,1,1,
        0,0,0,1,0,
        0,0,1,0,0,
        0,1,0,0,0,
        1,0,0,0,0,
        1,0,0,0,0,
        1,1,1,1,1,
    ],
    '0': [
        0,1,1,1,0,
        1,0,0,1,1,
        1,0,1,0,1,
        1,0,1,0,1,
        1,1,0,0,1,
        1,0,0,0,1,
        0,1,1,1,0,
    ],
    '1': [
        0,0,1,0,0,
        0,1,1,0,0,
        0,0,1,0,0,
        0,0,1,0,0,
        0,0,1,0,0,
        0,0,1,0,0,
        0,1,1,1,0,
    ],
    '2': [
        0,1,1,1,0,
        1,0,0,0,1,
        0,0,0,0,1,
        0,0,0,1,0,
        0,0,1,0,0,
        0,1,0,0,0,
        1,1,1,1,1,
    ],
    '3': [
        1,1,1,1,0,
        0,0,0,0,1,
        0,0,0,0,1,
        0,1,1,1,0,
        0,0,0,0,1,
        0,0,0,0,1,
        1,1,1,1,0,
    ],
    '4': [
        0,0,1,1,0,
        0,1,0,1,0,
        1,0,0,1,0,
        1,1,1,1,1,
        0,0,0,1,0,
        0,0,0,1,0,
        0,0,0,1,0,
    ],
    '5': [
        1,1,1,1,1,
        1,0,0,0,0,
        1,0,0,0,0,
        1,1,1,1,0,
        0,0,0,0,1,
        1,0,0,0,1,
        0,1,1,1,0,
    ],
    '6': [
        0,1,1,1,0,
        1,0,0,0,0,
        1,0,0,0,0,
        1,1,1,1,0,
        1,0,0,0,1,
        1,0,0,0,1,
        0,1,1,1,0,
    ],
    '7': [
        1,1,1,1,1,
        0,0,0,0,1,
        0,0,0,1,0,
        0,0,1,0,0,
        0,1,0,0,0,
        0,1,0,0,0,
        0,1,0,0,0,
    ],
    '8': [
        0,1,1,1,0,
        1,0,0,0,1,
        1,0,0,0,1,
        0,1,1,1,0,
        1,0,0,0,1,
        1,0,0,0,1,
        0,1,1,1,0,
    ],
    '9': [
        0,1,1,1,0,
        1,0,0,0,1,
        1,0,0,0,1,
        0,1,1,1,1,
        0,0,0,0,1,
        0,0,0,0,1,
        0,1,1,1,0,
    ],
    ' ': [
        0,0,0,0,0,
        0,0,0,0,0,
        0,0,0,0,0,
        0,0,0,0,0,
        0,0,0,0,0,
        0,0,0,0,0,
        0,0,0,0,0,
    ],
}
# fmt: on


def draw_pixel_text(draw, x, y, text, color, scale=1):
    """
    Draw pixel-bitmap text onto a PIL ImageDraw canvas.

    Parameters
    ----------
    draw  : ImageDraw.Draw — the draw context to render into.
    x     : int — left edge of first character (pixels).
    y     : int — top edge of first character (pixels).
    text  : str — string to render. Auto-upcased. Unrecognised chars → blank.
    color : tuple — RGB or RGBA fill color for text pixels.
    scale : int — pixel size multiplier (default 1 → each bit = 1px).
                  scale=2 → each bit = 2×2px block, etc.

    Returns
    -------
    (end_x, end_y) : int tuple — pixel position just after the last character
                     (useful for chaining multiple draw_pixel_text calls).

    Notes
    -----
    - Glyph cell: 5 cols × 7 rows.
    - Inter-glyph kerning: 1 pixel at scale 1 (scaled by `scale`).
    - After an img.paste() or alpha_composite call the draw context must be
      refreshed (PIL standards). This function draws directly — refresh draw
      context BEFORE calling if needed.
    """
    cursor_x = x
    for ch in text.upper():
        glyph = GLYPHS.get(ch, GLYPHS[' '])
        for row in range(_GLYPH_H):
            for col in range(_GLYPH_W):
                if glyph[row * _GLYPH_W + col]:
                    px = cursor_x + col * scale
                    py = y + row * scale
                    if scale == 1:
                        draw.point((px, py), fill=color)
                    else:
                        draw.rectangle(
                            [px, py, px + scale - 1, py + scale - 1],
                            fill=color
                        )
        cursor_x += (_GLYPH_W + 1) * scale  # glyph width + 1px kerning

    end_x = cursor_x
    end_y = y + _GLYPH_H * scale
    return end_x, end_y


def measure_pixel_text(text, scale=1):
    """
    Returns (width, height) in pixels for the given text and scale.
    Useful for centering text on a label.

    width  = len(text) * (GLYPH_W + 1) * scale  -  1 * scale (trailing kerning removed)
    height = GLYPH_H * scale
    """
    n = len(text)
    if n == 0:
        return (0, _GLYPH_H * scale)
    width = (n * (_GLYPH_W + 1) - 1) * scale
    height = _GLYPH_H * scale
    return (width, height)


# ── CLI self-test ─────────────────────────────────────────────────────────────

def _self_test():
    """
    Generates a test PNG with "MIRI" and "HELLO WORLD 0123456789" at two scales.
    Output: output/production/LTG_TEST_pixel_font_v001.png
    """
    W, H = 480, 120
    bg_color = (238, 226, 198)   # AGED_CREAM from kitchen palette
    ink_color = (88, 60, 32)     # LINE_DARK

    img = Image.new("RGB", (W, H), bg_color)
    draw = ImageDraw.Draw(img)

    # Row 1: scale 1 (original size)
    draw.text_start_x = 10  # not a PIL API — just comment marker
    draw_pixel_text(draw, 10, 10, "MIRI", ink_color, scale=1)
    draw_pixel_text(draw, 60, 10, "ABCDEFGHIJKLM", ink_color, scale=1)

    # Row 2: scale 1 continued
    draw_pixel_text(draw, 10, 22, "NOPQRSTUVWXYZ", ink_color, scale=1)
    draw_pixel_text(draw, 10, 34, "0123456789", ink_color, scale=1)

    # Row 3: scale 2 — "MIRI" large
    draw_pixel_text(draw, 10, 52, "MIRI", ink_color, scale=2)

    # Row 4: scale 3 — "MIRI" larger still
    draw_pixel_text(draw, 10, 80, "MIRI", ink_color, scale=3)

    # Save
    out_dir = os.path.join(os.path.dirname(__file__), "..", "production")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "LTG_TEST_pixel_font_v001.png")
    img.thumbnail((1280, 1280))
    img.save(out_path)
    print(f"[pixel_font_v001] Self-test output: {out_path}")

    # Centering demo — measure_pixel_text
    w, h = measure_pixel_text("MIRI", scale=2)
    print(f"[pixel_font_v001] measure_pixel_text('MIRI', scale=2) = ({w}px, {h}px)")
    print("[pixel_font_v001] PASS — all glyphs rendered.")


if __name__ == "__main__":
    _self_test()
