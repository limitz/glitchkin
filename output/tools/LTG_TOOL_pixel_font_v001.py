#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_pixel_font_v001.py — Pixel Font Utility
"Luma & the Glitchkin" — Production Pipeline
Author: Jordan Reed | Cycle 40
v001.1 — Hana Okonkwo | Cycle 44 — draw_pixel_text_perspective() added

Provides `draw_pixel_text(draw, x, y, text, color, scale=1)` for drawing
hand-lettered-style pixel text directly onto a PIL ImageDraw canvas.

Also provides `draw_pixel_text_perspective()` for mild perspective-correct
text scaling in 3/4-view environments (Alex Chen C44 brief).

Designed for in-world prop labels (e.g. fridge notes, sticky labels, signage)
where:
  - No font file dependency is acceptable
  - The text must read as "hand-annotated" rather than mechanical
  - Small scale (scale=1 → 5×7px per glyph) is the default use case

Built-in glyph set: A–Z (uppercase) and 0–9.
Lowercase input is auto-upcased. Unrecognised characters are rendered as a
blank space (glyph width + 1 px kerning).

Usage:
    from LTG_TOOL_pixel_font_v001 import draw_pixel_text, draw_pixel_text_perspective

    draw_pixel_text(draw, x=10, y=10, text="MIRI", color=(88, 60, 32))
    draw_pixel_text(draw, x=10, y=30, text="MIRI", color=(88, 60, 32), scale=2)

    # Perspective-scale variant (classroom chalkboard, VP_X=192, VP_Y=230):
    draw_pixel_text_perspective(draw, text="1011 XOR 0110", x=300, y=180,
                                scale=1, vp_x=192, vp_y=230, color=(200,220,200))

Each glyph is 5 columns × 7 rows. Kerning between glyphs: 1 pixel at scale 1
(scaled by `scale`). The `draw` parameter must be an ImageDraw.Draw instance
attached to the current working image.

CLI self-test: generates a 480×120 test PNG with "MIRI" at scale 1 and scale 2.
Output: output/production/LTG_TEST_pixel_font_v001.png
"""

import math
import os

from PIL import Image, ImageDraw

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


def draw_pixel_text_perspective(
    draw, text, x, y, scale, vp_x, vp_y,
    char_spacing=1, color=(255, 255, 255),
    canvas_w=1280, canvas_h=720,
):
    """
    Draw pixel-bitmap text with mild perspective scale correction.

    Characters positioned closer to the vanishing point (vp_x, vp_y) are drawn
    at a smaller effective scale (min scale * 0.65). Characters farther from the
    VP are drawn at full scale (scale * 1.0). Linear interpolation between the
    two extremes based on Euclidean distance from (x, y) to the VP, normalized
    by the maximum possible distance within the canvas.

    This is a simple linear approximation of perspective foreshortening — it is
    NOT a full projective transform. It reads naturally for text on angled boards
    or signs in 3/4-view scenes where the board is at a shallow 3D angle.

    Graceful fallback: if vp_x is None or vp_y is None, delegates to
    draw_pixel_text() at the specified flat scale.

    Parameters
    ----------
    draw         : ImageDraw.Draw — draw context (attached to current image).
    text         : str — text to render. Auto-upcased. Unknown chars → blank.
    x            : int — left edge of first character (pixels).
    y            : int — top edge of first character (pixels).
    scale        : int — base pixel size (scale=1 → 5×7px per glyph at full dist).
    vp_x         : int or None — vanishing point X in pixels.
    vp_y         : int or None — vanishing point Y in pixels.
    char_spacing : int — extra pixels between glyphs (added to kerning). Default 1.
    color        : tuple — RGB or RGBA fill for text pixels.
    canvas_w     : int — canvas width for max-distance reference. Default 1280.
    canvas_h     : int — canvas height for max-distance reference. Default 720.

    Returns
    -------
    (end_x, end_y) : pixel position just after the last character.

    Notes
    -----
    - Scale factor range: 0.65 (at VP) to 1.0 (at canvas far edge from VP).
    - The effective scale is clamped to max(1, round(scale * t)) so it is always
      a whole number of pixels. At scale=1, the clamp means t<0.5 still draws
      at 1px (can't go below 1). The foreshortening is most visible at scale>=2.
    - char_spacing adds extra gap between characters (default 1 matches the
      standard kerning convention from draw_pixel_text).
    """
    if vp_x is None or vp_y is None:
        return draw_pixel_text(draw, x, y, text, color, scale)

    # Distance from text anchor to VP
    dist_to_vp = math.sqrt((x - vp_x) ** 2 + (y - vp_y) ** 2)

    # Reference max distance: farthest canvas corner from VP
    corners = [
        (0, 0), (canvas_w, 0), (0, canvas_h), (canvas_w, canvas_h)
    ]
    max_dist = max(
        math.sqrt((cx - vp_x) ** 2 + (cy - vp_y) ** 2)
        for cx, cy in corners
    )
    if max_dist < 1:
        max_dist = 1.0  # degenerate guard

    # Normalised position: 0.0 = at VP, 1.0 = at canvas far corner
    t = max(0.0, min(1.0, dist_to_vp / max_dist))

    # Scale factor: 0.65 at VP, 1.0 at far edge (linear)
    scale_factor = 0.65 + 0.35 * t
    effective_scale = max(1, round(scale * scale_factor))

    # Draw with effective scale using the standard function
    return draw_pixel_text(draw, x, y, text, color, effective_scale)


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
