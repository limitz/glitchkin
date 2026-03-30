#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_elderly_proportion_reference.py
Elderly Proportion Reference & Comparison Overlay — v1.0.0
"Luma & the Glitchkin" — Cycle 47 / Maya Santos

PURPOSE:
  Generate a proportion comparison diagram showing realistic elderly (65-80 years)
  body proportions vs Miri's stylized 3.2-head proportions. This provides the
  canonical reference for validating Miri's design against real-world anatomy.

ELDERLY PROPORTION FACTS (65-80 years, female):
  - Real height: ~6.0-6.5 head units (down from 7.0-7.5 in prime — spinal compression)
  - Spinal kyphosis (forward thoracic curve): ~10-20° increase from young adult
  - Shoulder width narrows slightly, but appears broader due to posture change
  - Center of gravity shifts forward — head projects forward of shoulder line
  - Limb proportions preserved but muscle mass reduces — limbs appear thinner
  - Knee line drops slightly (femoral attrition)
  - Overall silhouette: more compact, slight forward lean, settled mass

MIRI STYLIZED (3.2 heads):
  - 2:1 compression from realistic ~6.2 heads
  - Head proportionally larger (toy-figure aesthetic, matches Luma)
  - Torso 1.05 heads (compact, settled)
  - Legs short and solid (0.55 + 0.52 heads)
  - Shoulder width 1.1x head width (broader than other cast — rooted)
  - Neck very short (0.08 heads)

OUTPUT:
  Two-panel diagram (1280x720):
    Left: Realistic elderly female proportion wireframe (6.2 heads)
    Right: Miri stylized proportion wireframe (3.2 heads)
    Overlay lines connecting equivalent body landmarks
    Head-unit grid for both figures
    Annotation of key proportion ratios

Author: Maya Santos — Cycle 47
"""
from PIL import Image, ImageDraw, ImageFont
import os

# ── Colors ───────────────────────────────────────────────────────────────────
BG          = (28, 24, 20)
PANEL_BG    = (38, 34, 30)
LINE_REAL   = (180, 140, 100)    # warm for realistic figure
LINE_MIRI   = (120, 160, 200)    # cool for stylized figure
GRID_REAL   = (80, 70, 60)       # subtle grid
GRID_MIRI   = (50, 70, 90)       # subtle grid
CONNECT     = (200, 180, 80, 120)  # landmark connection lines (semi-transparent)
TEXT_COL    = (220, 210, 195)
TEXT_DIM    = (140, 130, 120)
ACCENT      = (210, 170, 100)
MIRI_ACCENT = (120, 180, 220)

# ── Layout ───────────────────────────────────────────────────────────────────
CANVAS_W = 1280
CANVAS_H = 720
HEADER_H = 56
PANEL_W  = CANVAS_W // 2
BODY_H   = CANVAS_H - HEADER_H - 40  # room for footer

# ── Proportion data ──────────────────────────────────────────────────────────
# Realistic elderly female (65-80 years): 6.2 head units total
REAL_HEADS = 6.2
REAL_SEGMENTS = {
    "head":       (0.0, 1.0),
    "neck":       (1.0, 1.15),
    "torso":      (1.15, 3.1),    # longer torso proportionally (kyphosis compresses it visually)
    "upper_leg":  (3.1, 4.6),
    "lower_leg":  (4.6, 5.8),
    "feet":       (5.8, 6.2),
}
REAL_WIDTHS = {
    "head":       0.85,   # head width in head-units
    "shoulders":  1.10,   # slightly narrower than young adult
    "torso_mid":  1.00,
    "hips":       1.05,
    "upper_leg":  0.32,
    "lower_leg":  0.24,
}

# Miri stylized: 3.2 head units total (from grandma_miri.md)
MIRI_HEADS = 3.2
MIRI_SEGMENTS = {
    "head":       (0.0, 1.0),
    "neck":       (1.0, 1.08),
    "torso":      (1.08, 2.13),
    "upper_leg":  (2.13, 2.68),
    "lower_leg":  (2.68, 3.04),
    "feet":       (3.04, 3.20),
}
MIRI_WIDTHS = {
    "head":       1.00,   # head width = 1 head unit (rounder, toy-figure)
    "shoulders":  1.10,   # 1.1x head width per spec
    "torso_mid":  1.20,   # torso width 1.2x head width per spec
    "hips":       1.05,
    "upper_leg":  0.35,
    "lower_leg":  0.28,
}

LANDMARKS = ["head_top", "chin", "shoulders", "waist", "hips", "knee", "ankle", "feet"]
REAL_LANDMARKS = [0.0, 1.0, 1.15, 2.1, 3.1, 4.6, 5.8, 6.2]
MIRI_LANDMARKS = [0.0, 1.0, 1.08, 1.6, 2.13, 2.68, 3.04, 3.2]


def _draw_figure(draw, cx, base_y, total_h, heads, segments, widths, line_col, grid_col, label):
    """Draw a proportion wireframe figure with head-unit grid."""
    hu_px = total_h / heads  # pixels per head unit

    # Draw head-unit grid lines
    for i in range(int(heads) + 2):
        y = base_y - int(i * hu_px)
        if y < base_y - total_h - 10:
            break
        draw.line([(cx - int(hu_px * 0.8), y), (cx + int(hu_px * 0.8), y)],
                  fill=grid_col, width=1)
        # Grid label
        try:
            font_sm = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)
        except Exception:
            font_sm = ImageFont.load_default()
        draw.text((cx + int(hu_px * 0.85), y - 5), f"{i}", fill=grid_col, font=font_sm)

    # Draw body segments as connected wireframe
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11)
    except Exception:
        font = ImageFont.load_default()

    for seg_name, (start_hu, end_hu) in segments.items():
        y_top = base_y - int(start_hu * hu_px)
        y_bot = base_y - int(end_hu * hu_px)

        if seg_name == "head":
            # Draw head as oval
            hw = int(widths["head"] * hu_px * 0.5)
            draw.ellipse([cx - hw, y_bot, cx + hw, y_top], outline=line_col, width=2)
        elif seg_name == "neck":
            neck_w = int(hu_px * 0.15)
            draw.rectangle([cx - neck_w, y_bot, cx + neck_w, y_top], outline=line_col, width=2)
        elif seg_name == "torso":
            # Trapezoid: shoulders wider at top, hips at bottom
            sh_w = int(widths["shoulders"] * hu_px * 0.5)
            hip_w = int(widths["hips"] * hu_px * 0.5)
            pts = [(cx - sh_w, y_top), (cx + sh_w, y_top),
                   (cx + hip_w, y_bot), (cx - hip_w, y_bot)]
            draw.polygon(pts, outline=line_col, width=2)
            # Waist line
            waist_y = y_top + (y_bot - y_top) // 2
            waist_w = int(widths["torso_mid"] * hu_px * 0.5)
            draw.line([(cx - waist_w, waist_y), (cx + waist_w, waist_y)],
                      fill=grid_col, width=1)
        elif seg_name in ("upper_leg", "lower_leg"):
            w_key = seg_name
            w = int(widths[w_key] * hu_px * 0.5)
            for side in [-1, 1]:
                leg_cx = cx + side * int(widths["hips"] * hu_px * 0.25)
                draw.rectangle([leg_cx - w, y_bot, leg_cx + w, y_top],
                               outline=line_col, width=2)
        elif seg_name == "feet":
            fw = int(hu_px * 0.20)
            fh = y_top - y_bot
            for side in [-1, 1]:
                foot_cx = cx + side * int(widths["hips"] * hu_px * 0.25)
                draw.ellipse([foot_cx - fw - 4, y_bot, foot_cx + fw + 4, y_top],
                             outline=line_col, width=2)

    # Label
    draw.text((cx - 40, base_y + 8), label, fill=line_col, font=font)

    return hu_px


def generate_proportion_reference(output_path):
    """Generate the two-panel elderly proportion comparison diagram."""
    img = Image.new("RGB", (CANVAS_W, CANVAS_H), BG)
    draw = ImageDraw.Draw(img)

    try:
        font_title = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
        font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
        font_sm = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)
    except Exception:
        font_title = font = font_sm = ImageFont.load_default()

    # Header
    draw.text((16, 14),
              "MIRI PROPORTION REFERENCE — Elderly (65-80) vs Stylized (3.2 heads)  |  v1.0.0  |  C47",
              fill=ACCENT, font=font_title)
    draw.text((16, 36),
              "Left: Realistic elderly female (6.2 heads)  |  Right: Miri stylized (3.2 heads)  |  Grid = 1 head unit",
              fill=TEXT_DIM, font=font_sm)

    # Panel divider
    draw.line([(PANEL_W, HEADER_H), (PANEL_W, CANVAS_H - 20)], fill=(60, 55, 50), width=2)

    # Calculate figure heights — both fill the same vertical space for comparison
    fig_area_h = BODY_H - 40  # leave room for labels
    base_y = CANVAS_H - 30

    # Left panel: Realistic elderly
    real_cx = PANEL_W // 2
    real_total_h = fig_area_h
    _draw_figure(draw, real_cx, base_y, real_total_h,
                 REAL_HEADS, REAL_SEGMENTS, REAL_WIDTHS,
                 LINE_REAL, GRID_REAL, "REALISTIC (6.2 heads)")

    # Right panel: Miri stylized
    miri_cx = PANEL_W + PANEL_W // 2
    miri_total_h = fig_area_h
    _draw_figure(draw, miri_cx, base_y, miri_total_h,
                 MIRI_HEADS, MIRI_SEGMENTS, MIRI_WIDTHS,
                 LINE_MIRI, GRID_MIRI, "MIRI STYLIZED (3.2 heads)")

    # Draw connection lines between equivalent landmarks
    real_hu_px = real_total_h / REAL_HEADS
    miri_hu_px = miri_total_h / MIRI_HEADS

    for i, (name, real_hu, miri_hu) in enumerate(
            zip(LANDMARKS, REAL_LANDMARKS, MIRI_LANDMARKS)):
        real_y = base_y - int(real_hu * real_hu_px)
        miri_y = base_y - int(miri_hu * miri_hu_px)
        # Dotted connection line
        x_start = real_cx + int(real_hu_px * 0.9)
        x_end = miri_cx - int(miri_hu_px * 0.9)
        for x in range(x_start, x_end, 8):
            draw.line([(x, real_y), (x + 4, miri_y + (miri_y - real_y) * (x - x_start) // max(1, x_end - x_start))],
                      fill=(200, 180, 80), width=1)
        # Label the landmark
        label_x = (x_start + x_end) // 2 - 20
        label_y = (real_y + miri_y) // 2 - 6
        draw.text((label_x, label_y), name, fill=TEXT_DIM, font=font_sm)

    # Proportion ratio annotations
    annotations = [
        "Head:Body ratio — Real: 1:5.2 / Miri: 1:2.2 (2.4x compression)",
        "Torso:Total — Real: 31% / Miri: 33% (preserved)",
        "Leg:Total — Real: 37% / Miri: 33% (legs more compressed — grounded feel)",
        "Shoulder:Head — Real: 1.10x / Miri: 1.10x (preserved — rooted stance)",
        "Kyphosis: Realistic has 15° forward lean; Miri has subtle forward head tilt",
    ]
    ann_y = HEADER_H + 2
    for ann in annotations:
        draw.text((16, ann_y), ann, fill=TEXT_DIM, font=font_sm)
        ann_y += 14

    # Save
    img.thumbnail((1280, 1280), Image.LANCZOS)
    img.save(output_path)
    print(f"Saved: {output_path}  ({img.size[0]}x{img.size[1]}px)")
    print("v1.0.0: Elderly proportion reference — realistic vs Miri stylized")


if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "..", "production")
    os.makedirs(out_dir, exist_ok=True)
    generate_proportion_reference(
        os.path.join(out_dir, "LTG_PROD_elderly_proportion_reference.png")
    )
