#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_byte_cracked_eye_glyph.py
Byte Cracked-Eye Dead-Pixel Glyph Reference Sheet Generator

Art Director: Alex Chen
Date: 2026-03-30
Cycle: 13

Purpose:
  Design and render the canonical pixel-art "dead pixel" eye symbol for Byte's
  cracked eye display. Required by Lee Tanaka before drawing storyboard panel A2-07.

Design brief:
  A pixel-art dead pixel / cracked screen symbol. 7x7 grid of pixel squares.
  Pattern: a broken screen zone — dark/off pixels in a cracked arrangement.
  The glyph must:
  1. Read as "cracked screen" / "dead zone" — not a random pattern
  2. Work inside the cracked eye's small interior (fills 60% of eye frame)
  3. Remain legible at 40–60px eye scale (Byte on shoulder in medium shot)
  4. Angular/sharp to counterbalance the oval body (byte.md DO NOT list rule)

  The crack pattern uses a diagonal fracture line crossing a 7x7 grid,
  with dead-zone pixels (off/black) on one side of the crack, and dim/glowing
  pixels on the other side — simulating a damaged LED panel.

Output: /home/wipkat/team/output/characters/main/LTG_CHAR_byte_cracked_eye_glyph.png
  Reference sheet at 1600x800px showing:
  - 7x7 glyph at 1x, 4x, 8x, 16x scale
  - Color specifications
  - Usage notes for Lee Tanaka

Usage: python3 LTG_TOOL_byte_cracked_eye_glyph.py
"""

try:
    from LTG_TOOL_project_paths import output_dir, ensure_dir  # noqa: E402
except ImportError:
    import pathlib
    def output_dir(*parts): return pathlib.Path("/home/wipkat/team/output").joinpath(*parts)
    def ensure_dir(path): path.mkdir(parents=True, exist_ok=True); return path
import os
from PIL import Image, ImageDraw, ImageFont

OUTPUT_PATH = output_dir('characters', 'main', 'LTG_CHAR_byte_cracked_eye_glyph.png')

# Colors from master_palette.md
VOID_BLACK      = ( 10,  10,  20)
ELEC_CYAN       = (  0, 240, 255)
HOT_MAGENTA     = (255,  45, 107)
DEEP_CYAN       = (  0, 168, 180)
STATIC_WHITE    = (240, 240, 240)
BYTE_TEAL       = (  0, 212, 232)
UV_PURPLE       = (123,  47, 190)
WARM_CREAM      = (250, 240, 220)

# Cracked-eye background (the "bezel" / eye frame)
EYE_FRAME_BG    = ( 26,  58,  64)   # Deep Cyan-Gray #1A3A40 from byte.md

# Sheet background — near-void
SHEET_BG        = ( 18,  14,  28)


def load_font(size=14, bold=False):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()


# ── 7x7 Dead-Pixel Glyph Definition ──────────────────────────────────────────
#
# Coordinate system: [row][col], 0=top-left, 6=bottom-right
# Pixel states:
#   0 = DEAD (off — Void Black with very faint tint)
#   1 = ALIVE_DIM (dim alive — Deep Cyan at 40%)
#   2 = ALIVE_MID (mid alive — Electric Cyan)
#   3 = CRACK_LINE (crack fracture — Hot Magenta / bright)
#   4 = ALIVE_BRIGHT (bright alive — Static White + Cyan)
#
# Pattern description:
#   A diagonal crack runs from approximately (row 0, col 4) to (row 6, col 2).
#   Left-of-crack (upper-right quadrant): dead zone — pixel damage.
#   Right-of-crack (lower-left quadrant): dim alive — surviving display area.
#   The crack itself: Hot Magenta fracture line.
#   A few isolated bright pixels scattered near the crack edge — pixel corona.
#
GLYPH_7x7 = [
    # row 0: top edge — mixed alive and starting crack
    [1, 1, 1, 1, 3, 0, 0],
    # row 1: crack starts crossing
    [1, 2, 1, 3, 0, 0, 0],
    # row 2: crack midway, dead zone expanding right
    [2, 1, 3, 0, 0, 4, 0],
    # row 3: center — crack and bright flare near crack edge
    [1, 3, 0, 0, 4, 0, 0],
    # row 4: crack past center, lower region
    [3, 0, 0, 1, 1, 0, 1],
    # row 5: lower section — alive fragments near crack
    [0, 0, 1, 2, 1, 1, 1],
    # row 6: bottom — mostly alive, trace of crack
    [0, 3, 1, 1, 2, 1, 1],
]

# Color mapping for each pixel state
PIXEL_COLORS = {
    0: (VOID_BLACK[0] + 5, VOID_BLACK[1] + 3, VOID_BLACK[2] + 8),  # DEAD — near-void
    1: (  0,  80, 100),    # ALIVE_DIM — dark cyan, dim
    2: DEEP_CYAN,          # ALIVE_MID — Deep Cyan
    3: HOT_MAGENTA,        # CRACK_LINE — Hot Magenta fracture
    4: (200, 255, 255),    # ALIVE_BRIGHT — overexposed white-cyan near crack
}


def render_glyph(draw, origin_x, origin_y, pixel_size):
    """Render the 7x7 glyph at (origin_x, origin_y) with pixel_size per cell."""
    for row_idx, row in enumerate(GLYPH_7x7):
        for col_idx, state in enumerate(row):
            color = PIXEL_COLORS[state]
            px = origin_x + col_idx * pixel_size
            py = origin_y + row_idx * pixel_size
            draw.rectangle([px, py, px + pixel_size - 1, py + pixel_size - 1], fill=color)
    # Outer pixel grid border (faint)
    glyph_w = 7 * pixel_size
    glyph_h = 7 * pixel_size
    draw.rectangle([origin_x - 1, origin_y - 1,
                    origin_x + glyph_w, origin_y + glyph_h],
                   outline=(40, 60, 70), width=1)


def render_in_eye_frame(draw, img, origin_x, origin_y, eye_frame_w, eye_frame_h):
    """
    Render the glyph inside a cracked eye frame mockup.
    Shows how the glyph sits inside the actual eye bezel at ~60% fill.
    """
    # Eye frame background (the "bezel")
    draw.rectangle([origin_x, origin_y, origin_x + eye_frame_w, origin_y + eye_frame_h],
                   fill=EYE_FRAME_BG, outline=VOID_BLACK, width=2)

    # Crack line diagonally across the frame (represents the physical screen crack)
    draw.line([(origin_x + int(eye_frame_w * 0.60), origin_y + 2),
               (origin_x + int(eye_frame_w * 0.20), origin_y + eye_frame_h - 2)],
              fill=VOID_BLACK, width=2)

    # LEFT half: cracked eye displaying the glyph
    # Glyph fills 60% of eye frame interior
    glyph_area_w = int(eye_frame_w * 0.50)  # left half only
    glyph_area_h = int(eye_frame_h * 0.80)
    pixel_size = max(1, min(glyph_area_w // 7, glyph_area_h // 7))
    glyph_w = 7 * pixel_size
    glyph_h = 7 * pixel_size
    g_origin_x = origin_x + (glyph_area_w - glyph_w) // 2 + 3
    g_origin_y = origin_y + (eye_frame_h - glyph_h) // 2

    # Clip glyph to left half of eye
    temp = Image.new("RGBA", (eye_frame_w, eye_frame_h), (0, 0, 0, 0))
    td = ImageDraw.Draw(temp)
    for row_idx, row in enumerate(GLYPH_7x7):
        for col_idx, state in enumerate(row):
            color = PIXEL_COLORS[state]
            px = g_origin_x - origin_x + col_idx * pixel_size
            py = g_origin_y - origin_y + row_idx * pixel_size
            if px < int(eye_frame_w * 0.56):  # only draw on cracked side
                td.rectangle([px, py, px + pixel_size - 1, py + pixel_size - 1],
                              fill=(*color, 220))
    # Paste temp onto main image
    base_rgba = img.convert("RGBA")
    crop = base_rgba.crop((origin_x, origin_y, origin_x + eye_frame_w, origin_y + eye_frame_h))
    merged = Image.alpha_composite(crop.convert("RGBA"), temp)
    base_rgba.paste(merged.convert("RGBA"), (origin_x, origin_y))
    img.paste(base_rgba.convert("RGB"))
    draw = ImageDraw.Draw(img)

    # RIGHT half: normal eye (for comparison)
    # Simple cyan iris with black pupil
    rx_center = origin_x + int(eye_frame_w * 0.77)
    ry_center = origin_y + eye_frame_h // 2
    iris_r = int(eye_frame_h * 0.35)
    draw.ellipse([rx_center - iris_r, ry_center - iris_r,
                  rx_center + iris_r, ry_center + iris_r],
                 fill=ELEC_CYAN)
    pupil_r = int(iris_r * 0.5)
    draw.ellipse([rx_center - pupil_r, ry_center - pupil_r,
                  rx_center + pupil_r, ry_center + pupil_r],
                 fill=VOID_BLACK)
    draw.ellipse([rx_center + int(pupil_r * 0.2), ry_center - int(pupil_r * 0.5),
                  rx_center + int(pupil_r * 0.7), ry_center],
                 fill=(200, 255, 255))


def generate():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    W_SHEET, H_SHEET = 1600, 900
    img  = Image.new("RGB", (W_SHEET, H_SHEET), SHEET_BG)
    draw = ImageDraw.Draw(img)

    font_title = load_font(24, bold=True)
    font_label = load_font(16, bold=False)
    font_small = load_font(13, bold=False)

    # ── Title ──────────────────────────────────────────────────────────────────
    draw.text((30, 18), "BYTE — Cracked Eye Dead-Pixel Glyph", fill=WARM_CREAM, font=font_title)
    draw.text((30, 50), "LTG_CHAR_byte_cracked_eye_glyph_v001  |  Cycle 13  |  Alex Chen",
              fill=(140, 130, 120), font=font_small)
    draw.line([(30, 74), (W_SHEET - 30, 74)], fill=(40, 60, 70), width=1)

    # ── Section 1: Glyph at multiple scales ───────────────────────────────────
    draw.text((30, 86), "GLYPH SCALES — 1×, 4×, 8×, 16×", fill=ELEC_CYAN, font=font_label)

    scales = [
        (1,  "1× (7px wide — minimum production size)"),
        (4,  "4× (28px wide — Byte on shoulder, close-up)"),
        (8,  "8× (56px wide — standard reference)"),
        (16, "16× (112px wide — production art detail)"),
    ]
    glyph_x = 50
    glyph_y = 120
    for pixel_size, label in scales:
        render_glyph(draw, glyph_x, glyph_y, pixel_size)
        glyph_w = 7 * pixel_size
        label_x = glyph_x
        label_y = glyph_y + 7 * pixel_size + 4
        draw.text((label_x, label_y), label, fill=(180, 170, 160), font=font_small)
        glyph_x += glyph_w + 60

    # ── Section 2: In-eye context mockup ──────────────────────────────────────
    draw.line([(30, 340), (W_SHEET - 30, 340)], fill=(40, 60, 70), width=1)
    draw.text((30, 350), "IN-EYE CONTEXT — Cracked eye (left) vs Normal eye (right) at 3 sizes",
              fill=ELEC_CYAN, font=font_label)

    eye_specs = [
        (50,  40, "Small: shoulder-ride shot (~40px eye)"),
        (180, 70, "Medium: mid-shot close (~70px eye)"),
        (370, 110, "Large: expression close-up (~110px eye)"),
    ]
    eye_x = 50
    for eye_w, eye_h, label in eye_specs:
        render_in_eye_frame(draw, img, eye_x, 380, eye_w, eye_h)
        draw = ImageDraw.Draw(img)
        draw.text((eye_x, 380 + eye_h + 6), label, fill=(160, 150, 140), font=font_small)
        eye_x += eye_w + 40

    # ── Section 3: Color specification ────────────────────────────────────────
    draw.line([(30, 530), (W_SHEET - 30, 530)], fill=(40, 60, 70), width=1)
    draw.text((30, 540), "PIXEL COLOR SPECIFICATION", fill=ELEC_CYAN, font=font_label)

    color_specs = [
        (0, "DEAD pixel",        PIXEL_COLORS[0], "Off-zone — physical damage. Near-void, slightly blue-tinted."),
        (1, "ALIVE_DIM",         PIXEL_COLORS[1], "Surviving display — dark cyan. Dim, low power."),
        (2, "ALIVE_MID (GL-02)", DEEP_CYAN,       "Deep Cyan #00A8B4 — standard alive pixel state."),
        (3, "CRACK_LINE (GL-03)",HOT_MAGENTA,     "Hot Magenta #FF2D6B — fracture line through pixel panel."),
        (4, "ALIVE_BRIGHT",      PIXEL_COLORS[4], "Pixel corona near crack — overexposed, near white-cyan."),
    ]

    spec_x = 50
    spec_y = 570
    for state, name, color, desc in color_specs:
        # Color swatch
        draw.rectangle([spec_x, spec_y, spec_x + 24, spec_y + 16], fill=color, outline=(60, 70, 80))
        # Label
        draw.text((spec_x + 32, spec_y), f"{name}", fill=WARM_CREAM, font=font_label)
        draw.text((spec_x + 32, spec_y + 18), f"  {desc}", fill=(150, 140, 130), font=font_small)
        spec_y += 44

    # ── Section 4: Usage notes for Lee Tanaka ─────────────────────────────────
    draw.line([(30, 780), (W_SHEET - 30, 780)], fill=(40, 60, 70), width=1)
    draw.text((30, 790), "USAGE NOTES FOR LEE TANAKA — Panel A2-07",
              fill=(255, 180, 80), font=font_label)
    notes = [
        "1. The cracked eye is the RIGHT eye of Byte's face (faces toward danger / crack in SF02).",
        "2. The crack line runs upper-right to lower-left across the eye bezel. Dead zone is upper-right.",
        "3. Glyph fills 60% of the cracked-eye interior. The physical crack line is always visible over it.",
        "4. In panel A2-07, Byte's cracked eye should display the dead-pixel glyph — no other symbol.",
        "5. The normal (left) eye can show any expression glyph appropriate to Byte's state in that panel.",
        "6. Keep all detail lines sharp/angular — no smooth curves on the glyph. (byte.md DO NOT rule)",
    ]
    note_y = 815
    for note in notes:
        draw.text((50, note_y), note, fill=(170, 165, 155), font=font_small)
        note_y += 16

    img.save(OUTPUT_PATH, "PNG")
    print(f"Saved: {OUTPUT_PATH}")
    return OUTPUT_PATH


if __name__ == "__main__":
    generate()
