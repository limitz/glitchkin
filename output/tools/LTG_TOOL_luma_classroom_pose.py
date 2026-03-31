#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_luma_classroom_pose.py
Luma Classroom Pose Generator — "Luma & the Glitchkin"

Cycle 14: Sitting-in-class pose for storyboard beat A1-04.
Beat description: Luma seated at desk, slight slouch, pen tapping desk,
head tilting toward blackboard. Near-miss moment — she's ALMOST connecting
the binary lesson to Byte.

Pose spec:
  - Body: seated (torso upright-ish, slight slouch)
  - Left arm: elbow on desk, hand supports chin lightly (distracted lean)
  - Right arm: extended forward, pen tip touching desk surface (tapping)
  - Head: slight rightward tilt (toward blackboard) — tilt_deg = 8deg
  - Expression: CURIOUS (canonical, closest to at-rest curiosity)

Output: LTG_CHAR_luma_classroom_pose.png
Format: Single pose sheet — character on left, annotation panel on right.
Canvas: 900x560px

Character rendering: uses canonical LTG_TOOL_char_luma.draw_luma().
"""
import os
import sys

_TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
if _TOOLS_DIR not in sys.path:
    sys.path.insert(0, _TOOLS_DIR)

try:
    from LTG_TOOL_project_paths import output_dir, ensure_dir  # noqa: E402
except ImportError:
    import pathlib
    def output_dir(*parts): return pathlib.Path("/home/wipkat/team/output").joinpath(*parts)
    def ensure_dir(path): path.mkdir(parents=True, exist_ok=True); return path

from PIL import Image, ImageDraw, ImageFont
import math
import numpy as np

from LTG_TOOL_char_luma import draw_luma, cairo_surface_to_pil

# ── Palette (scene props only — character colors come from char_luma) ────────
LINE        = (59, 40, 32)
PANTS       = (60, 50, 80)
SKIN        = (200, 136, 90)

# Environment colors
DESK_TOP    = (180, 155, 120)
DESK_FRONT  = (148, 124, 90)
DESK_SHADOW = (120, 100, 70)
PEN_BODY    = (200, 60, 80)
PEN_TIP     = (40, 34, 28)

BG_WARM     = (238, 228, 210)
BG_PANEL    = (248, 244, 236)
CANVAS_BG   = (238, 228, 210)

# ── Canvas ────────────────────────────────────────────────────────────────────
CANVAS_W = 900
CANVAS_H = 560
CHAR_AREA_W = 520
ANNO_AREA_X = 540


def draw_luma_seated(img, draw, cx, cy):
    """Draw seated Luma using canonical char_luma renderer + desk environment.

    Uses draw_luma() from LTG_TOOL_char_luma.py for the character figure.
    Desk, pen, and leg hints are scene props drawn locally.

    cy is the approximate face center Y. Desk surface at cy + ~295px.
    """
    # ── Desk environment (drawn first — behind character) ───────────────────
    desk_y   = cy + 295
    desk_x1  = cx - 260
    desk_x2  = cx + 280
    desk_h   = 28

    draw.rectangle([desk_x1 + 6, desk_y + desk_h,
                    desk_x2 + 6, desk_y + desk_h + 12], fill=DESK_SHADOW)
    draw.rectangle([desk_x1, desk_y, desk_x2, desk_y + desk_h],
                   fill=DESK_TOP, outline=LINE, width=2)
    draw.rectangle([desk_x1, desk_y + desk_h,
                    desk_x2, desk_y + desk_h + 40],
                   fill=DESK_FRONT, outline=LINE, width=2)
    for gi in range(3):
        gy = desk_y + 8 + gi * 8
        draw.line([(desk_x1 + 20, gy), (desk_x2 - 20, gy)],
                  fill=DESK_SHADOW, width=1)

    # ── Render Luma via canonical char_luma renderer ─────────────────────────
    char_surface = draw_luma("CURIOUS", scale=1.0, facing="right")
    char_pil = cairo_surface_to_pil(char_surface)

    # Crop to bounding box and scale to fit the scene
    bbox = char_pil.getbbox()
    if bbox:
        char_pil = char_pil.crop(bbox)

    # Target height: character should fill from above head area down to desk
    target_h = int((desk_y - (cy - 120)) * 0.92)
    if target_h > 0 and char_pil.height > 0:
        scale_factor = target_h / char_pil.height
        new_w = max(1, int(char_pil.width * scale_factor))
        new_h = max(1, int(char_pil.height * scale_factor))
        char_pil = char_pil.resize((new_w, new_h), Image.LANCZOS)

    # Position: center horizontally, bottom at desk level
    paste_x = cx - char_pil.width // 2
    paste_y = desk_y - char_pil.height
    img.paste(char_pil, (paste_x, paste_y), char_pil)
    draw = ImageDraw.Draw(img, 'RGBA')

    # ── Pen prop (scene element, drawn on desk surface) ──────────────────────
    hand_cx = cx + 28
    hand_cy = desk_y
    pen_x1 = hand_cx + 6
    pen_y1 = hand_cy - 8
    pen_x2 = pen_x1 + 40
    pen_y2 = pen_y1 + 6
    draw.line([(pen_x1, pen_y1), (pen_x2, pen_y2)], fill=PEN_BODY, width=5)
    draw.line([(pen_x2, pen_y2), (pen_x2 + 6, desk_y - 2)], fill=PEN_TIP, width=3)
    draw.line([(pen_x1 + 4, pen_y1 - 2), (pen_x1 + 10, pen_y2 + 4)],
              fill=(240, 240, 240), width=1)

    # ── Upper legs (hint visible below desk) ─────────────────────────────────
    hu = 140
    leg_w = int(hu * 0.18)
    leg_l = cx - int(hu * 0.35)
    leg_r = cx + int(hu * 0.25)
    draw.rectangle([leg_l - leg_w, desk_y + desk_h,
                    leg_l + leg_w, desk_y + desk_h + 30],
                   fill=PANTS, outline=LINE, width=1)
    draw.rectangle([leg_r - leg_w, desk_y + desk_h,
                    leg_r + leg_w, desk_y + desk_h + 30],
                   fill=PANTS, outline=LINE, width=1)

    return draw


def draw_annotation_panel(draw, x, y, w, h, font, font_sm):
    """Right-side annotation panel with pose callouts."""
    draw.rectangle([x, y, x + w, y + h], fill=BG_PANEL, outline=(180, 168, 150), width=2)

    title_color  = (80, 56, 32)
    label_color  = (59, 40, 32)
    detail_color = (110, 90, 68)
    beat_color   = (60, 100, 80)

    annotations = [
        ("BEAT", "A1-04 — NEAR-MISS MICRO-BEAT",    beat_color,  True),
        ("",     "",                                  label_color, False),
        ("EXPR", "AT-REST CURIOSITY",                label_color, True),
        ("",     "eyes shift right (blackboard)",     detail_color, False),
        ("",     "asymm. mouth corner (right rises)", detail_color, False),
        ("",     "collar tilt 3deg (orienting)",      detail_color, False),
        ("",     "",                                  label_color, False),
        ("POSE", "DISTRACTED LEAN",                  label_color, True),
        ("",     "left elbow on desk",                detail_color, False),
        ("",     "right hand tapping pen",            detail_color, False),
        ("",     "head tilt 8deg right",              detail_color, False),
        ("",     "",                                  label_color, False),
        ("NOTE", "Byte is NOT shown here —",         label_color, True),
        ("",     "he is in the desk tray pocket",    detail_color, False),
        ("",     "(asleep in eraser bits)",           detail_color, False),
        ("",     "",                                  label_color, False),
        ("SRC",  "char_luma canonical renderer",     (120, 100, 60), False),
        ("RULE", "Character > BG saturation",        (120, 100, 60), False),
    ]

    line_h = 22
    cur_y  = y + 18
    cur_x  = x + 14

    draw.text((cur_x, cur_y - 2),
              "LUMA — Classroom Pose  v003",
              fill=title_color, font=font)
    cur_y += 28
    draw.line([(cur_x, cur_y), (x + w - 14, cur_y)], fill=(180, 168, 150), width=1)
    cur_y += 10

    for (prefix, text, color, bold) in annotations:
        if not text:
            cur_y += 8
            continue
        if prefix:
            draw.text((cur_x, cur_y),
                      f"{prefix}: ", fill=(100, 140, 110), font=font_sm)
            draw.text((cur_x + 42, cur_y), text, fill=color, font=font_sm)
        else:
            draw.text((cur_x + 42, cur_y), text, fill=color, font=font_sm)
        cur_y += line_h
        if cur_y > y + h - 20:
            break

    draw.line([(cur_x, y + h - 30), (x + w - 14, y + h - 30)],
              fill=(180, 168, 150), width=1)
    draw.text((cur_x, y + h - 24),
              "Cycle 21 — Maya Santos (v003: char_luma import)",
              fill=detail_color, font=font_sm)


def generate_luma_classroom_pose(output_path):
    """Render seated classroom pose sheet for Luma."""
    img  = Image.new('RGB', (CANVAS_W, CANVAS_H), CANVAS_BG)
    draw = ImageDraw.Draw(img, 'RGBA')

    try:
        font       = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
        font_sm    = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 13)
        font_title = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
    except Exception:
        font = font_sm = font_title = ImageFont.load_default()

    draw.text((20, 12),
              "LUMA — Classroom Pose  |  Beat A1-04: Near-Miss  |  v003 Cycle 21",
              fill=(80, 56, 32), font=font_title)

    draw.rectangle([0, 40, CHAR_AREA_W, CANVAS_H], fill=(235, 224, 206))

    char_cx = 270
    char_cy = 200
    draw = draw_luma_seated(img, draw, char_cx, char_cy)

    draw_annotation_panel(draw, ANNO_AREA_X, 40,
                          CANVAS_W - ANNO_AREA_X - 10,
                          CANVAS_H - 50, font, font_sm)

    draw.line([(CHAR_AREA_W, 40), (CHAR_AREA_W, CANVAS_H)],
              fill=(180, 168, 150), width=2)

    img_rgb = img.convert('RGB')
    img_rgb.save(output_path)
    print(f"Saved: {output_path}  ({CANVAS_W}x{CANVAS_H}px)")


if __name__ == '__main__':
    out_dir = output_dir('characters', 'main')
    os.makedirs(out_dir, exist_ok=True)
    generate_luma_classroom_pose(
        os.path.join(out_dir, "LTG_CHAR_luma_classroom_pose.png")
    )
