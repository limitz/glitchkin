#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_sb_panel_a205.py
Storyboard Panel A2-05 — Millbrook Street Exterior — Cycle 17
Lee Tanaka, Storyboard Artist

Beat: Walk-and-talk transition. Luma pitching her plan to Cosmo on
Millbrook Main Street. Cosmo's skepticism is growing.
Day exterior — normal world, shows stakes.

Camera: MEDIUM / eye-level / tracking with characters
  - Medium two-shot: Luma FG (slightly left), Cosmo slightly behind/right
  - Millbrook suburban street receding behind them
  - Walk-and-talk feel — both mid-stride
  - Afternoon warm light

Expression callouts:
  - Luma: ENTHUSIASTIC / pitching (gesticulating, mid-gesture)
  - Cosmo: SKEPTICAL (arms crossed or one hand up, flat brow)

Output:
  /home/wipkat/team/output/storyboards/act2/panels/LTG_SB_act2_panel_a205.png
"""

from PIL import Image, ImageDraw, ImageFont
import math
import random
import os

ACT2_PANELS_DIR = "/home/wipkat/team/output/storyboards/act2/panels"
PANELS_DIR      = "/home/wipkat/team/output/storyboards/panels"
OUTPUT_PATH     = os.path.join(ACT2_PANELS_DIR, "LTG_SB_act2_panel_a205.png")

os.makedirs(ACT2_PANELS_DIR, exist_ok=True)
os.makedirs(PANELS_DIR, exist_ok=True)

PW, PH    = 800, 600
CAPTION_H = 60
DRAW_H    = PH - CAPTION_H   # 540px scene area

# ── Palette ──────────────────────────────────────────────────────────────────
BG_CAPTION   = (22, 18, 14)
TEXT_CAPTION = (235, 228, 210)
BORDER_COL   = (18, 12, 8)

# Exterior sky + street
SKY_TOP      = (180, 200, 230)   # pale afternoon sky
SKY_BOT      = (230, 215, 180)   # warm horizon
ROAD_COL     = (100, 92, 82)     # pavement
SIDEWALK_COL = (175, 162, 145)   # lighter sidewalk
BUILDING_1   = (185, 155, 120)   # warm brick building
BUILDING_2   = (155, 175, 145)   # green-tinted building
BUILDING_3   = (205, 175, 130)   # another warm building
WINDOW_COL   = (200, 230, 250)   # window glass
TREE_TRUNK   = (80, 60, 40)
TREE_LEAVES  = (90, 140, 80)
TREE_LIGHT   = (130, 175, 110)

# Luma (FG — full warm colors, mid-stride)
LUMA_SKIN    = (210, 142, 96)
LUMA_HAIR    = (22, 14, 8)
LUMA_JACKET  = (190, 80, 50)     # warm red
LUMA_PANTS   = (60, 80, 120)
LUMA_OUTLINE = (42, 28, 14)

# Cosmo (slightly BG — slightly muted)
COSMO_SKIN   = (165, 115, 70)
COSMO_HAIR   = (14, 10, 6)
COSMO_SHIRT  = (70, 90, 160)
COSMO_PANTS  = (38, 52, 95)
COSMO_OUTLINE= (28, 18, 8)

STATIC_WHITE = (240, 240, 240)
ANN_COL      = (220, 200, 130)
ANN_DIM      = (160, 145, 95)
CALLOUT_LUMA = (220, 160, 80)
CALLOUT_COS  = (100, 180, 220)


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


def add_glow(img, cx, cy, r_max, color_rgb, steps=6, max_alpha=60):
    """ADD light via alpha_composite — never darkens."""
    for i in range(steps, 0, -1):
        r     = int(r_max * (i / steps))
        alpha = int(max_alpha * (1 - (i / steps) * 0.6))
        glow  = Image.new('RGBA', img.size, (0, 0, 0, 0))
        gd    = ImageDraw.Draw(glow)
        gd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(*color_rgb, alpha))
        base  = img.convert('RGBA')
        img.paste(Image.alpha_composite(base, glow).convert('RGB'))


def draw_millbrook_bg(draw, img):
    """
    Millbrook Main Street — afternoon exterior.
    Single-point perspective: street recedes to VP center-right.
    Suburban but warm, lived-in buildings flanking the street.
    """
    vp_x = int(PW * 0.62)
    horizon_y = int(DRAW_H * 0.44)   # eye-level horizon

    # Sky gradient (two-tone: blue top, warm bottom near horizon)
    for y in range(horizon_y + 1):
        t = y / max(horizon_y, 1)
        r = int(SKY_TOP[0] + (SKY_BOT[0] - SKY_TOP[0]) * t)
        g = int(SKY_TOP[1] + (SKY_BOT[1] - SKY_TOP[1]) * t)
        b = int(SKY_TOP[2] + (SKY_BOT[2] - SKY_TOP[2]) * t)
        draw.line([0, y, PW, y], fill=(r, g, b))

    # Road (receding from camera)
    road_left_bot  = 0
    road_right_bot = PW
    road_left_top  = vp_x - 30
    road_right_top = vp_x + 30
    draw.polygon([
        (road_left_bot, DRAW_H),
        (road_right_bot, DRAW_H),
        (road_right_top, horizon_y),
        (road_left_top, horizon_y),
    ], fill=ROAD_COL)

    # Road center line
    draw.line([PW // 2, DRAW_H, vp_x, horizon_y], fill=(200, 185, 140), width=2)
    # Dashed road lines
    rng = random.Random(2205)
    steps_n = 8
    for i in range(steps_n):
        t1 = i / steps_n
        t2 = (i + 0.5) / steps_n
        x1l = int(road_left_bot + (road_left_top - road_left_bot) * t1)
        x1r = int(road_right_bot + (road_right_top - road_right_bot) * t1)
        x2l = int(road_left_bot + (road_left_top - road_left_bot) * t2)
        x2r = int(road_right_bot + (road_right_top - road_right_bot) * t2)
        y1  = int(DRAW_H + (horizon_y - DRAW_H) * t1)
        y2  = int(DRAW_H + (horizon_y - DRAW_H) * t2)
        cx1 = (x1l + x1r) // 2
        cx2 = (x2l + x2r) // 2
        draw.line([cx1, y1, cx2, y2], fill=(230, 210, 160), width=max(1, 3 - i // 3))

    # Sidewalks flanking road
    sw_left  = int(PW * 0.04)
    sw_right = int(PW * 0.96)
    draw.polygon([
        (sw_left, DRAW_H), (road_left_bot, DRAW_H),
        (road_left_top, horizon_y), (sw_left + 5, horizon_y)
    ], fill=SIDEWALK_COL)
    draw.polygon([
        (road_right_bot, DRAW_H), (sw_right, DRAW_H),
        (sw_right - 5, horizon_y), (road_right_top, horizon_y)
    ], fill=SIDEWALK_COL)

    # ── Left-side buildings ─────────────────────────────────────────────────
    # Building 1 (far left, warm brick)
    b1_x = -10
    b1_w = int(PW * 0.28)
    b1_h = int(DRAW_H * 0.62)
    b1_y = horizon_y - b1_h + 10
    draw.rectangle([b1_x, b1_y, b1_x + b1_w, horizon_y], fill=BUILDING_1)
    draw.line([b1_x, b1_y, b1_x + b1_w, b1_y], fill=(140, 115, 85), width=2)
    # Windows (left building)
    for wr in range(2):
        for wc in range(3):
            wx = b1_x + 18 + wc * 48
            wy = b1_y + 14 + wr * 38
            draw.rectangle([wx, wy, wx + 28, wy + 22], fill=WINDOW_COL,
                            outline=(140, 115, 85), width=1)

    # Building 2 (slightly right of center, greenish)
    b2_x = int(PW * 0.06)
    b2_w = int(PW * 0.18)
    b2_h = int(DRAW_H * 0.44)
    b2_y = horizon_y - b2_h
    draw.rectangle([b2_x, b2_y, b2_x + b2_w, horizon_y], fill=BUILDING_2)
    # Awning (shop-front detail)
    draw.polygon([(b2_x, horizon_y - 22), (b2_x + b2_w, horizon_y - 22),
                  (b2_x + b2_w + 8, horizon_y - 30), (b2_x - 8, horizon_y - 30)],
                 fill=(160, 60, 40))
    # Sign
    draw.rectangle([b2_x + 10, horizon_y - 42, b2_x + b2_w - 10, horizon_y - 26],
                   fill=(240, 220, 180), outline=(120, 90, 60))

    # ── Right-side buildings ────────────────────────────────────────────────
    b3_x = int(PW * 0.72)
    b3_w = int(PW * 0.36)
    b3_h = int(DRAW_H * 0.55)
    b3_y = horizon_y - b3_h
    draw.rectangle([b3_x, b3_y, b3_x + b3_w, horizon_y], fill=BUILDING_3)
    draw.line([b3_x, b3_y, b3_x + b3_w, b3_y], fill=(160, 130, 95), width=2)
    for wr in range(2):
        for wc in range(3):
            wx = b3_x + 12 + wc * 52
            wy = b3_y + 16 + wr * 42
            draw.rectangle([wx, wy, wx + 30, wy + 28], fill=WINDOW_COL,
                            outline=(160, 130, 95), width=1)

    # ── Street trees (left side) ────────────────────────────────────────────
    for tx_frac, scale_t in [(0.10, 1.0), (0.18, 0.72)]:
        tx = int(PW * tx_frac)
        ty_base = int(DRAW_H * (0.78 + (1 - scale_t) * 0.1))
        trunk_h = int(55 * scale_t)
        trunk_w = int(8 * scale_t)
        canopy_r = int(38 * scale_t)
        draw.rectangle([tx - trunk_w // 2, ty_base - trunk_h,
                        tx + trunk_w // 2, ty_base],
                       fill=TREE_TRUNK)
        draw.ellipse([tx - canopy_r, ty_base - trunk_h - canopy_r,
                      tx + canopy_r, ty_base - trunk_h + canopy_r],
                     fill=TREE_LEAVES)
        draw.ellipse([tx - canopy_r + 8, ty_base - trunk_h - canopy_r + 6,
                      tx + canopy_r - 4, ty_base - trunk_h + canopy_r - 8],
                     fill=TREE_LIGHT)

    return horizon_y, vp_x


def draw_cosmo_med(draw, img):
    """
    Cosmo — medium shot, slightly behind/right of Luma.
    SKEPTICAL: arms crossed, one brow raised, flat mouth.
    Mid-stride (walk-and-talk).
    Slightly smaller scale than Luma (depth relationship).
    """
    cx = int(PW * 0.62)
    feet_y = int(DRAW_H * 0.96)   # feet near bottom
    scale = 0.88

    head_r  = int(30 * scale)
    body_w  = int(62 * scale)
    body_h  = int(105 * scale)

    head_cy = feet_y - body_h - head_r * 2

    # ── Body (facing slightly left toward Luma) ─────────────────────────────
    # Slight right lean (weight on back foot, skeptical posture)
    lean = -6
    body_cx = cx + lean

    draw.ellipse([body_cx - body_w // 2, head_cy + head_r + 2,
                  body_cx + body_w // 2, head_cy + head_r + 2 + body_h],
                 fill=COSMO_SHIRT, outline=COSMO_OUTLINE, width=2)

    # Pants / lower body
    draw.ellipse([body_cx - body_w // 2 + 6, head_cy + head_r + 2 + body_h - 15,
                  body_cx + body_w // 2 - 6, head_cy + head_r + 2 + body_h + 30],
                 fill=COSMO_PANTS, outline=COSMO_OUTLINE, width=2)

    # Legs (mid-stride — weight shifting back)
    leg_top_y = head_cy + head_r + 2 + body_h + 15
    # Left leg (slightly forward)
    draw.line([body_cx - 12, leg_top_y,
               body_cx - 8, feet_y],
              fill=COSMO_PANTS, width=18)
    # Right leg (back — stride)
    draw.line([body_cx + 12, leg_top_y,
               body_cx + 22, feet_y],
              fill=COSMO_PANTS, width=18)

    # ── ARMS CROSSED (skeptical) ────────────────────────────────────────────
    arm_y = head_cy + head_r + 2 + int(body_h * 0.38)
    arm_band_h = 14
    # Crossed arm band across torso
    draw.rectangle([body_cx - body_w // 2 - 6, arm_y,
                    body_cx + body_w // 2 + 6, arm_y + arm_band_h],
                   fill=COSMO_SKIN, outline=COSMO_OUTLINE, width=1)
    # Left arm crossing over (visible forearm)
    draw.line([body_cx - body_w // 2 + 4, arm_y + arm_band_h // 2,
               body_cx + 10, arm_y + arm_band_h // 2 - 4],
              fill=COSMO_SKIN, width=11)
    # Right arm tucked under
    draw.line([body_cx + body_w // 2 - 4, arm_y + arm_band_h // 2 + 2,
               body_cx - 8, arm_y + arm_band_h // 2 + 6],
              fill=COSMO_SHIRT, width=10)

    # ── HEAD ───────────────────────────────────────────────────────────────
    head_cx = cx + lean
    draw.ellipse([head_cx - head_r, head_cy - head_r,
                  head_cx + head_r, head_cy + head_r],
                 fill=COSMO_SKIN, outline=COSMO_OUTLINE, width=2)

    # Hair
    draw.ellipse([head_cx - head_r, head_cy - head_r - 2,
                  head_cx + head_r, head_cy + 6],
                 fill=COSMO_HAIR)

    # Eyes (facing slightly left toward Luma)
    eye_y = head_cy - 4
    for i, ex_off in enumerate([-11, 10]):
        ex = head_cx + ex_off
        draw.ellipse([ex - 6, eye_y - 5, ex + 6, eye_y + 5],
                     fill=STATIC_WHITE)
        draw.ellipse([ex - 2, eye_y - 2, ex + 2, eye_y + 2],
                     fill=(40, 60, 80))

    # Glasses
    gl_y = eye_y
    for ex_off in [-11, 10]:
        ex = head_cx + ex_off
        draw.rectangle([ex - 8, gl_y - 6, ex + 8, gl_y + 6],
                       outline=(80, 55, 30), width=2)

    # SKEPTICAL BROWS — asymmetric
    # Raised brow (left eye, viewer's left = Cosmo's right — skeptical side)
    draw.arc([head_cx - 20, eye_y - 18, head_cx - 3, eye_y - 6],
             start=200, end=340, fill=COSMO_HAIR, width=2)
    # Flat brow (right eye — other side flat/lower)
    draw.line([head_cx + 2, eye_y - 9, head_cx + 17, eye_y - 9],
              fill=COSMO_HAIR, width=2)

    # SKEPTICAL MOUTH — flat with slight downturn at one corner
    mouth_y = head_cy + 10
    draw.line([head_cx - 9, mouth_y, head_cx + 9, mouth_y],
              fill=COSMO_OUTLINE, width=2)
    draw.line([head_cx - 9, mouth_y, head_cx - 11, mouth_y + 2],
              fill=COSMO_OUTLINE, width=2)

    return cx, head_cy


def draw_luma_fg(draw, img):
    """
    Luma — FG left of frame, medium shot.
    ENTHUSIASTIC: gesticulating, mid-stride, leaning forward.
    Larger scale than Cosmo (she's closer to camera).
    """
    luma_cx = int(PW * 0.32)
    feet_y  = int(DRAW_H * 1.0)   # feet at or just below frame bottom (FG depth)
    scale   = 1.0                  # full size

    head_r  = 36
    body_w  = 72
    body_h  = 115

    head_cy = feet_y - body_h - head_r * 2 - 8

    # ── Body (facing right toward Cosmo, mid-stride lean forward) ──────────
    body_cx = luma_cx
    lean_x  = 10   # forward lean

    draw.ellipse([body_cx - body_w // 2 + lean_x, head_cy + head_r + 2,
                  body_cx + body_w // 2 + lean_x, head_cy + head_r + 2 + body_h],
                 fill=LUMA_JACKET, outline=LUMA_OUTLINE, width=2)

    # Pants / lower body
    draw.ellipse([body_cx - body_w // 2 + lean_x + 6,
                  head_cy + head_r + 2 + body_h - 15,
                  body_cx + body_w // 2 + lean_x - 6,
                  head_cy + head_r + 2 + body_h + 32],
                 fill=LUMA_PANTS, outline=LUMA_OUTLINE, width=2)

    # Legs (mid-stride — forward momentum)
    leg_top_y = head_cy + head_r + 2 + body_h + 18
    # Left leg (back — stride)
    draw.line([body_cx + lean_x - 14, leg_top_y,
               body_cx - 30, feet_y],
              fill=LUMA_PANTS, width=20)
    # Right leg (forward)
    draw.line([body_cx + lean_x + 14, leg_top_y,
               body_cx + lean_x + 40, feet_y],
              fill=LUMA_PANTS, width=20)

    # ── ARMS GESTICULATING (enthusiastic pitch) ──────────────────────────
    arm_y_base = head_cy + head_r + 2 + int(body_h * 0.25)
    # Right arm (extended up and out — making a point)
    draw.line([body_cx + body_w // 2 + lean_x - 4, arm_y_base,
               body_cx + body_w // 2 + lean_x + 48, arm_y_base - 35],
              fill=LUMA_SKIN, width=12)
    # Hand/finger pointing
    draw.ellipse([body_cx + body_w // 2 + lean_x + 38, arm_y_base - 42,
                  body_cx + body_w // 2 + lean_x + 56, arm_y_base - 26],
                 fill=LUMA_SKIN, outline=LUMA_OUTLINE, width=1)

    # Left arm (bent upward, gesturing)
    draw.line([body_cx - body_w // 2 + lean_x + 4, arm_y_base,
               body_cx - body_w // 2 + lean_x - 24, arm_y_base - 22],
              fill=LUMA_SKIN, width=12)
    draw.line([body_cx - body_w // 2 + lean_x - 24, arm_y_base - 22,
               body_cx - body_w // 2 + lean_x - 8, arm_y_base - 46],
              fill=LUMA_SKIN, width=10)
    # Second hand
    draw.ellipse([body_cx - body_w // 2 + lean_x - 18, arm_y_base - 54,
                  body_cx - body_w // 2 + lean_x + 2, arm_y_base - 38],
                 fill=LUMA_SKIN, outline=LUMA_OUTLINE, width=1)

    # ── HEAD ──────────────────────────────────────────────────────────────
    head_cx = luma_cx + lean_x - 4   # face turned slightly right toward Cosmo
    draw.ellipse([head_cx - head_r, head_cy - head_r,
                  head_cx + head_r, head_cy + head_r],
                 fill=LUMA_SKIN, outline=LUMA_OUTLINE, width=2)

    # Hair
    draw.ellipse([head_cx - head_r, head_cy - head_r - 2,
                  head_cx + head_r, head_cy + 8],
                 fill=LUMA_HAIR)

    # ENTHUSIASTIC eyes — wide open, turned toward Cosmo
    eye_y = head_cy - 5
    for i, ex_off in enumerate([-12, 12]):
        ex = head_cx + ex_off
        draw.ellipse([ex - 8, eye_y - 6, ex + 8, eye_y + 6],
                     fill=STATIC_WHITE)
        # Iris shifted right (looking at Cosmo)
        draw.ellipse([ex, eye_y - 4, ex + 6, eye_y + 4],
                     fill=(60, 80, 120))
        # Highlight
        draw.rectangle([ex + 5, eye_y - 3, ex + 7, eye_y - 1], fill=STATIC_WHITE)

    # ENTHUSIASTIC BROWS — both raised (energy/excitement)
    draw.arc([head_cx - 22, eye_y - 18, head_cx - 4, eye_y - 6],
             start=200, end=340, fill=LUMA_HAIR, width=2)
    draw.arc([head_cx + 4, eye_y - 18, head_cx + 22, eye_y - 6],
             start=200, end=340, fill=LUMA_HAIR, width=2)

    # ENTHUSIASTIC MOUTH — open, mid-word (talking)
    draw.ellipse([head_cx - 10, head_cy + 5, head_cx + 10, head_cy + 18],
                 fill=(40, 20, 15), outline=LUMA_OUTLINE, width=1)
    # Teeth (upper)
    draw.rectangle([head_cx - 7, head_cy + 6, head_cx + 7, head_cy + 11],
                   fill=STATIC_WHITE)

    # Motion lines near right arm (gesticulating energy)
    rng = random.Random(2205)
    for _ in range(4):
        mx = body_cx + body_w // 2 + lean_x + rng.randint(20, 50)
        my = arm_y_base + rng.randint(-30, -10)
        dl = rng.randint(10, 18)
        draw.line([mx, my, mx + dl, my - dl // 2], fill=(240, 200, 100), width=1)

    return luma_cx, head_cy, lean_x


def draw_annotations(draw, luma_cx, luma_head_cy, luma_lean,
                      cosmo_cx, cosmo_head_cy, font_ann):
    """Shot type, character positions, and expression callouts."""
    # Shot type
    draw.text((10, 8), "MEDIUM  /  eye-level  /  tracking with characters",
              font=font_ann, fill=ANN_COL)

    # Luma annotation
    ann_x = luma_cx + luma_lean + 60
    ann_y = luma_head_cy - 24
    draw.line([luma_cx + luma_lean + 30, luma_head_cy - 10,
               ann_x, ann_y],
              fill=CALLOUT_LUMA, width=1)
    draw.text((ann_x + 2, ann_y - 4), "LUMA — ENTHUSIASTIC",
              font=font_ann, fill=CALLOUT_LUMA)
    draw.text((ann_x + 2, ann_y + 6), "mid-gesture / pitching plan",
              font=font_ann, fill=(200, 160, 80))

    # Cosmo annotation
    cos_ann_x = cosmo_cx + 50
    cos_ann_y = cosmo_head_cy - 22
    draw.line([cosmo_cx + 28, cosmo_head_cy - 8,
               cos_ann_x, cos_ann_y],
              fill=CALLOUT_COS, width=1)
    draw.text((cos_ann_x + 2, cos_ann_y - 4), "COSMO — SKEPTICAL",
              font=font_ann, fill=CALLOUT_COS)
    draw.text((cos_ann_x + 2, cos_ann_y + 6), "arms crossed / raised brow",
              font=font_ann, fill=(100, 160, 200))

    # Walk-and-talk annotation
    draw.text((PW - 230, DRAW_H - 18), "walk-and-talk — both mid-stride",
              font=font_ann, fill=ANN_DIM)

    # Depth labels
    draw.text((10, DRAW_H - 20), "FG: Luma",
              font=font_ann, fill=(220, 170, 100))
    draw.text((int(PW * 0.56), DRAW_H - 20), "BG: Cosmo",
              font=font_ann, fill=(140, 170, 210))

    # Afternoon light note
    draw.text((PW - 190, 8), "afternoon / warm exterior",
              font=font_ann, fill=ANN_DIM)


def make_panel():
    font      = load_font(14)
    font_bold = load_font(14, bold=True)
    font_cap  = load_font(12)
    font_ann  = load_font(11)

    img  = Image.new('RGB', (PW, PH), SKY_TOP)
    draw = ImageDraw.Draw(img)

    horizon_y, vp_x = draw_millbrook_bg(draw, img)
    draw = ImageDraw.Draw(img)

    cosmo_cx, cosmo_head_cy = draw_cosmo_med(draw, img)
    draw = ImageDraw.Draw(img)

    luma_cx, luma_head_cy, luma_lean = draw_luma_fg(draw, img)
    draw = ImageDraw.Draw(img)

    # Warm afternoon sun glow from upper right
    add_glow(img, PW - 80, 30, 120, (255, 220, 140), steps=5, max_alpha=22)
    draw = ImageDraw.Draw(img)

    draw_annotations(draw, luma_cx, luma_head_cy, luma_lean,
                     cosmo_cx, cosmo_head_cy, font_ann)

    # Caption bar
    draw.rectangle([0, DRAW_H, PW, PH], fill=BG_CAPTION)
    draw.line([0, DRAW_H, PW, DRAW_H], fill=BORDER_COL, width=2)
    draw.text((10, DRAW_H + 6), "A2-05  MEDIUM  eye-level  tracking",
              font=font_cap, fill=(160, 155, 130))
    draw.text((10, DRAW_H + 22),
              "Millbrook Street — Luma (FG, ENTHUSIASTIC/pitching) + Cosmo (BG, SKEPTICAL / arms crossed)",
              font=font_cap, fill=TEXT_CAPTION)
    draw.text((10, DRAW_H + 38),
              "Walk-and-talk transition | afternoon exterior | both mid-stride | suburban Millbrook Main St",
              font=font_ann, fill=(150, 140, 110))
    draw.text((PW - 200, DRAW_H + 46), "LTG_SB_act2_panel_a205_v001",
              font=font_ann, fill=(100, 95, 78))

    # Border
    draw.rectangle([0, 0, PW - 1, PH - 1], outline=BORDER_COL, width=2)

    img.save(OUTPUT_PATH, "PNG")
    print(f"Saved: {OUTPUT_PATH}")

    panels_path = os.path.join(PANELS_DIR, "LTG_SB_act2_panel_a205.png")
    img.save(panels_path, "PNG")
    print(f"Also saved: {panels_path}")

    return OUTPUT_PATH


if __name__ == "__main__":
    make_panel()
    print("A2-05 panel generation complete (Cycle 17).")
