#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_luma_act2_standing_pose.py
Luma Act 2 Standing Reactive Pose Generator — "Luma & the Glitchkin"

Cycle 15: Standing reactive pose for Act 2 beats.
Beat context: Luma is in the tech den / on the street — investigating,
problem-solving, reacting. She is NOT seated. This pose covers:
  - A2-01: Tech den, trying to communicate with Byte (investigative urgency)
  - A2-03: Enthusiastic about Cosmo's plan (leaning in, engaged)
  - A2-05: On street, reading the streetlight signal (alert / wonder)
  - A2-08: Facing Grandma Miri (uncertain, a little guilty)

Character rendering: uses canonical LTG_TOOL_char_luma.draw_luma().
Expression: WORRIED (closest to the investigative/uncertain reactive pose).

Output: LTG_CHAR_luma_act2_standing_pose.png
Format: Character pose sheet — character on left, annotation panel on right.
Canvas: 900x600px
"""
import os
import sys
import math

_TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
if _TOOLS_DIR not in sys.path:
    sys.path.insert(0, _TOOLS_DIR)

from PIL import Image, ImageDraw, ImageFont
import numpy as np

from LTG_TOOL_char_luma import draw_luma, cairo_surface_to_pil

# Background — warm neutral
BG_WARM     = (234, 224, 208)
BG_PANEL    = (246, 240, 230)
LINE        = (59, 40, 32)

CANVAS_W = 900
CANVAS_H = 600
CHAR_AREA_W = 520
ANNO_AREA_X = 540


def draw_luma_standing(img, draw, cx, ground_y):
    """Draw standing Luma using canonical char_luma renderer.

    Returns approximate face center Y for annotation alignment.
    """
    # Render Luma with WORRIED expression (reactive/investigative)
    char_surface = draw_luma("WORRIED", scale=1.2, facing="right")
    char_pil = cairo_surface_to_pil(char_surface)

    # Crop to bounding box
    bbox = char_pil.getbbox()
    if bbox:
        char_pil = char_pil.crop(bbox)

    # Scale to fit: character should be ~430px tall (fills most of the panel)
    target_h = int((ground_y - 50) * 0.82)
    if target_h > 0 and char_pil.height > 0:
        scale_factor = target_h / char_pil.height
        new_w = max(1, int(char_pil.width * scale_factor))
        new_h = max(1, int(char_pil.height * scale_factor))
        char_pil = char_pil.resize((new_w, new_h), Image.LANCZOS)

    # Position: centered, feet on ground
    paste_x = cx - char_pil.width // 2
    paste_y = ground_y - char_pil.height
    img.paste(char_pil, (paste_x, paste_y), char_pil)

    # Return approximate face center Y (top ~30% of character)
    face_cy = paste_y + int(char_pil.height * 0.18)
    return face_cy


def draw_silhouette_blob(draw, cx, ground_y, scale=0.38):
    """Squint-test silhouette — simplified black blob at reduced scale.

    Per Cycle 4/5 rules: silhouette must be readable as a black blob.
    Uses canonical renderer at small scale, converted to black.
    """
    char_surface = draw_luma("WORRIED", scale=scale, facing="right")
    char_pil = cairo_surface_to_pil(char_surface)
    bbox = char_pil.getbbox()
    if bbox:
        char_pil = char_pil.crop(bbox)
    # Scale to small size
    target_h = int(80 * scale / 0.38)
    if target_h > 0 and char_pil.height > 0:
        sf = target_h / char_pil.height
        new_w = max(1, int(char_pil.width * sf))
        new_h = max(1, int(char_pil.height * sf))
        char_pil = char_pil.resize((new_w, new_h), Image.LANCZOS)

    # Convert to black silhouette
    arr = np.array(char_pil)
    mask = arr[:, :, 3] > 30  # alpha threshold
    arr[mask, 0:3] = 30  # near-black
    silhouette = Image.fromarray(arr)

    sx = cx - silhouette.width // 2
    sy = ground_y - silhouette.height
    draw._image.paste(silhouette, (sx, sy), silhouette)


def draw_annotation_panel(draw, x, y, w, h, font, font_sm):
    """Right-side annotation panel with pose callouts and silhouette test."""
    draw.rectangle([x, y, x + w, y + h], fill=BG_PANEL, outline=(180, 168, 150), width=2)

    title_c  = (80, 56, 32)
    label_c  = (59, 40, 32)
    detail_c = (110, 90, 68)
    beat_c   = (60, 100, 80)

    annotations = [
        ("BEATS", "A2-01, A2-03, A2-05, A2-08",    beat_c,   True),
        ("",      "",                                label_c,  False),
        ("EXPR",  "WORRIED / DETERMINED",           label_c,  True),
        ("",      "brow differential >= 8px",        detail_c, False),
        ("",      "corrugator kink (inner UP)",      detail_c, False),
        ("",      "jaw-open oval (not scream rect)", detail_c, False),
        ("",      "",                                label_c,  False),
        ("POSE",  "STANDING REACTIVE",              label_c,  True),
        ("",      "right arm raised/reaching",       detail_c, False),
        ("",      "left arm at waist (grounded)",    detail_c, False),
        ("",      "wide stance leg_spread=1.1",      detail_c, False),
        ("",      "body_tilt=-5 (forward lean)",     detail_c, False),
        ("",      "head tilt 5deg left (query)",     detail_c, False),
        ("",      "",                                label_c,  False),
        ("SRC",   "char_luma canonical renderer",   (100, 80, 60), False),
        ("",      "",                                label_c,  False),
        ("SIHL",  "Squint test — see blob below",   (100, 80, 60), False),
        ("",      "A-line + cloud hair + sneakers",  detail_c, False),
        ("",      "pocket bump: asymmetry hook",     detail_c, False),
    ]

    line_h = 22
    cur_y  = y + 18
    cur_x  = x + 14

    draw.text((cur_x, cur_y - 2),
              "LUMA — Act 2 Standing Pose  v002 (C16)",
              fill=title_c, font=font)
    cur_y += 28
    draw.line([(cur_x, cur_y), (x + w - 14, cur_y)],
              fill=(180, 168, 150), width=1)
    cur_y += 10

    for (prefix, text, color, bold) in annotations:
        if not text:
            cur_y += 8
            continue
        if prefix:
            draw.text((cur_x, cur_y),
                      f"{prefix}: ", fill=(100, 140, 110), font=font_sm)
            draw.text((cur_x + 52, cur_y), text, fill=color, font=font_sm)
        else:
            draw.text((cur_x + 52, cur_y), text, fill=color, font=font_sm)
        cur_y += line_h
        if cur_y > y + h - 100:
            break

    # Silhouette blob (squint test)
    blob_y  = y + h - 88
    blob_cx = x + w // 2
    blob_gy = y + h - 16

    draw.text((cur_x, blob_y - 16), "SQUINT TEST:", fill=(80, 60, 40), font=font_sm)
    draw_silhouette_blob(draw, blob_cx, blob_gy, scale=0.30)

    draw.line([(cur_x, y + h - 14), (x + w - 14, y + h - 14)],
              fill=(180, 168, 150), width=1)
    draw.text((cur_x, y + h - 10),
              "Cycle 15/16 — Maya Santos (char_luma import)",
              fill=detail_c, font=font_sm)


def generate_luma_act2_standing_pose(output_path):
    """Render Act 2 standing pose sheet for Luma."""
    img  = Image.new('RGB', (CANVAS_W, CANVAS_H), BG_WARM)
    draw = ImageDraw.Draw(img, 'RGBA')

    try:
        font       = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 15)
        font_sm    = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
        font_title = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 17)
    except Exception:
        font = font_sm = font_title = ImageFont.load_default()

    draw.text((18, 10),
              "LUMA — Act 2 Standing Pose  |  Beats A2-01/03/05/08  |  Cycle 15",
              fill=(80, 56, 32), font=font_title)
    draw.line([(18, 34), (CANVAS_W - 18, 34)], fill=(180, 168, 150), width=1)

    draw.rectangle([10, 40, CHAR_AREA_W, CANVAS_H - 10], fill=(238, 228, 210))

    char_cx  = CHAR_AREA_W // 2 + 20
    ground_y = CANVAS_H - 30
    cy = draw_luma_standing(img, draw, char_cx, ground_y)

    # Refresh draw context after paste
    draw = ImageDraw.Draw(img, 'RGBA')

    draw.line([(18, ground_y + 2), (CHAR_AREA_W - 10, ground_y + 2)],
              fill=(160, 144, 120), width=2)
    draw.ellipse([char_cx - 80, ground_y,
                  char_cx + 80, ground_y + 10],
                 fill=(180, 164, 140))

    draw_annotation_panel(draw, ANNO_AREA_X, 40,
                          CANVAS_W - ANNO_AREA_X - 10,
                          CANVAS_H - 50, font, font_sm)

    img.save(output_path)
    print(f"Saved: {output_path}")
    dims = img.size
    print(f"Dimensions: {dims[0]}x{dims[1]}px")


if __name__ == "__main__":
    output_path = (
        "/home/wipkat/team/output/characters/main/"
        "LTG_CHAR_luma_act2_standing_pose.png"
    )
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    generate_luma_act2_standing_pose(output_path)
