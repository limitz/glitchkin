#!/usr/bin/env python3
"""
LTG_CHAR_cosmo_turnaround_v002.py
Cosmo — 4-View Character Turnaround v002
"Luma & the Glitchkin" — Cycle 25 / Maya Santos

v002 FIX: Cosmo's SIDE view was an architecturally impossible flat rectangle
with no front-to-back depth. This was production-blocking.

FIX: Side view now shows:
  - Profile head (ellipse rotated to side, glasses as single lens + temple)
  - Torso has depth foreshortening (narrow front-to-back)
  - Shirt visible in profile (stripe lines go forward, not sideways)
  - Notebook visible tucked under left arm (2D from side = just the spine/edge)
  - Leg stance side-on (near leg visible, far leg partially behind)
  - Properly foregrounded 3D form

4 views: FRONT, 3/4, SIDE, BACK
Canvas: 1600×700px (4 × 400px panels)
2× render + LANCZOS for sub-pixel AA

Output: output/characters/main/turnarounds/LTG_CHAR_cosmo_turnaround_v002.png
"""

from PIL import Image, ImageDraw, ImageFont
import math
import os

# ── Palette (canonical cosmo_color_model.md) ──────────────────────────────────
SKIN       = (217, 192, 154)
SKIN_SH    = (184, 154, 120)
SKIN_HL    = (238, 212, 176)
HAIR       = ( 26,  24,  36)
HAIR_SH    = ( 14,  14,  24)
HAIR_HL    = ( 44,  43,  64)
EYE_W      = (250, 240, 220)
IRIS       = ( 61, 107,  69)
PUPIL      = ( 59,  40,  32)
EYE_HL     = (240, 240, 240)
GLASS_FR   = ( 92,  58,  32)
GLASS_LN   = (238, 244, 255)
GLASS_GL   = (240, 240, 240)
STRIPE_A   = ( 91, 141, 184)   # cerulean
STRIPE_B   = (122, 158, 126)   # sage
PANTS      = (140, 136, 128)
PANTS_SH   = (106, 100,  96)
PANTS_HL   = (174, 170, 164)
BELT       = ( 92,  58,  32)   # espresso (same as glass frame)
SHOE       = ( 92,  58,  32)
SHOE_SH    = ( 60,  34,  16)
SHOE_SOLE  = (184, 154, 120)
NOTEBOOK   = ( 91, 141, 184)
NOTEBK_SP  = ( 61, 107, 138)
NOTEBK_PG  = (250, 240, 220)
LINE       = ( 59,  40,  32)
CANVAS_BG  = (248, 244, 238)
SHADOW_COL = (210, 200, 185)
LABEL_COL  = ( 59,  40,  32)
HU_COL     = (160, 140, 120)

# ── Layout ────────────────────────────────────────────────────────────────────
CANVAS_W  = 1600
CANVAS_H  = 700
VIEWS     = ["FRONT", "3/4", "SIDE", "BACK"]
N_VIEWS   = 4
VIEW_W    = CANVAS_W // N_VIEWS   # 400px per panel
VIEW_H    = CANVAS_H

HEADER_H  = 52
LABEL_H   = 36
BODY_H    = VIEW_H - HEADER_H - LABEL_H   # 612px character area

SCALE = 2
CHAR_DRAW_H  = int(BODY_H * 0.86)   # ≈ 526 at 1x
CHAR_TOP_MARGIN = int(BODY_H * 0.05)


def hu():
    """One head unit at 1× — Cosmo is ~3.5 heads tall."""
    return CHAR_DRAW_H / 3.5


def draw_striped_rect(draw, x0, y0, x1, y1, tilt=0):
    """Draw a striped shirt region (horizontal stripes)."""
    height = y1 - y0
    stripe_h = max(3, height // 14)
    for i in range(14):
        sy = y0 + i * stripe_h
        col = STRIPE_A if i % 2 == 0 else STRIPE_B
        ey  = min(y0 + (i + 1) * stripe_h, y1)
        if tilt != 0:
            draw.polygon([
                (x0 + tilt * i // 14, sy),
                (x1 + tilt * i // 14, sy),
                (x1 + tilt * (i+1) // 14, ey),
                (x0 + tilt * (i+1) // 14, ey),
            ], fill=col)
        else:
            draw.rectangle([x0, sy, x1, ey], fill=col)


# ── FRONT VIEW ─────────────────────────────────────────────────────────────────

def render_front(draw, cx, base_y):
    """Draw Cosmo front view. base_y = foot ground line."""
    S = SCALE
    h = int(hu() * S)   # 1 head unit at 2x

    # Character top = base_y - CHAR_DRAW_H * S
    top_y = base_y - int(CHAR_DRAW_H * S)

    # --- HEAD ---
    head_cy = top_y + h   # head center = 1 HU from top
    head_rx = int(h * 0.44)
    head_ry = int(h * 0.52)

    # Ears
    ear_r = int(h * 0.13)
    ear_y = head_cy + int(h * 0.10)
    draw.ellipse([cx - head_rx - ear_r + 4, ear_y - ear_r,
                  cx - head_rx + ear_r + 4, ear_y + ear_r],
                 fill=SKIN, outline=LINE, width=4)
    draw.ellipse([cx + head_rx - ear_r - 4, ear_y - ear_r,
                  cx + head_rx + ear_r - 4, ear_y + ear_r],
                 fill=SKIN, outline=LINE, width=4)

    # Head fill
    draw.ellipse([cx - head_rx, head_cy - head_ry,
                  cx + head_rx, head_cy + head_ry], fill=SKIN)

    # Hair (side part, covering top)
    hair_top = head_cy - head_ry - int(h * 0.10)
    hair_bot = head_cy - head_ry + int(h * 0.52)
    draw.ellipse([cx - head_rx - 4, hair_top,
                  cx + int(head_rx * 0.25), hair_bot + 4], fill=HAIR)
    draw.ellipse([cx - int(head_rx * 0.25), hair_top + 4,
                  cx + head_rx + 4, hair_bot + 2], fill=HAIR)
    # Part line (visible)
    part_x = cx + int(head_rx * 0.15)
    draw.line([part_x, hair_top + 4, part_x, hair_bot],
              fill=SKIN, width=3)
    # Cowlick arc
    draw.arc([cx - int(h * 0.08), hair_top - int(h * 0.06),
              cx + int(h * 0.08), hair_top + int(h * 0.08)],
             start=280, end=80, fill=HAIR_HL, width=int(h * 0.04))
    # Head outline
    draw.ellipse([cx - head_rx, head_cy - head_ry,
                  cx + head_rx, head_cy + head_ry],
                 outline=LINE, width=6)

    # --- GLASSES (7° tilt, front view — both lenses + bridge + temples) ---
    lens_r  = int(h * 0.18)
    frame_w = max(4, int(h * 0.07))
    bridge  = int(h * 0.06)
    eye_sep = lens_r + bridge
    gcy     = head_cy + int(h * 0.08)
    theta   = math.radians(-7)
    cos_t   = math.cos(theta)
    sin_t   = math.sin(theta)

    def rot(dx, dy):
        return (int(cx + dx * cos_t - dy * sin_t),
                int(gcy + dx * sin_t + dy * cos_t))

    lcx_g, lcy_g = rot(-eye_sep, 0)
    rcx_g, rcy_g = rot(+eye_sep, 0)

    for (ex, ey) in [(lcx_g, lcy_g), (rcx_g, rcy_g)]:
        draw.ellipse([ex - lens_r, ey - lens_r, ex + lens_r, ey + lens_r], fill=GLASS_LN)
        draw.arc([ex - int(lens_r * 0.7), ey - lens_r + 2,
                  ex + int(lens_r * 0.7), ey - lens_r + int(lens_r * 0.5)],
                 start=200, end=340, fill=GLASS_GL, width=3)
        draw.ellipse([ex - lens_r, ey - lens_r, ex + lens_r, ey + lens_r],
                     outline=GLASS_FR, width=frame_w)

    # Eyes inside glasses
    for (ex, ey) in [(lcx_g, lcy_g), (rcx_g, rcy_g)]:
        iris_r = int(lens_r * 0.55)
        pup_r  = int(iris_r * 0.55)
        draw.ellipse([ex - iris_r, ey - iris_r, ex + iris_r, ey + iris_r], fill=EYE_W)
        draw.ellipse([ex - int(iris_r * 0.7), ey - int(iris_r * 0.7),
                      ex + int(iris_r * 0.7), ey + int(iris_r * 0.7)], fill=IRIS)
        draw.ellipse([ex - pup_r, ey - pup_r, ex + pup_r, ey + pup_r], fill=PUPIL)
        draw.ellipse([ex + int(iris_r * 0.3), ey - iris_r + 2,
                      ex + int(iris_r * 0.3) + 4, ey - iris_r + 6], fill=EYE_HL)

    # Bridge
    bl = rot(-bridge, 0)
    br = rot(+bridge, 0)
    draw.line([bl, br], fill=GLASS_FR, width=frame_w)
    # Temples
    lt_s = rot(-eye_sep - lens_r, 0)
    lt_e = rot(-eye_sep - lens_r - int(h * 0.07), int(h * 0.02))
    rt_s = rot(+eye_sep + lens_r, 0)
    rt_e = rot(+eye_sep + lens_r + int(h * 0.07), int(h * 0.02))
    draw.line([lt_s, lt_e], fill=GLASS_FR, width=max(3, frame_w - 1))
    draw.line([rt_s, rt_e], fill=GLASS_FR, width=max(3, frame_w - 1))

    # Nose
    draw.arc([cx - int(h * 0.06), head_cy + int(h * 0.28),
              cx + int(h * 0.06), head_cy + int(h * 0.40)],
             start=0, end=180, fill=SKIN_SH, width=3)

    # Mouth
    mouth_y = head_cy + int(h * 0.55)
    draw.arc([cx - int(h * 0.14), mouth_y,
              cx + int(h * 0.14), mouth_y + int(h * 0.16)],
             start=10, end=170, fill=LINE, width=3)

    # Brows
    for side in [-1, 1]:
        bx = cx + side * eye_sep
        by = gcy - lens_r - int(h * 0.08)
        draw.arc([bx - int(h * 0.16), by - int(h * 0.04),
                  bx + int(h * 0.16), by + int(h * 0.06)],
                 start=200 if side < 0 else 340,
                 end=340 if side < 0 else 200,
                 fill=HAIR, width=3)

    # --- NECK ---
    neck_top_y = head_cy + head_ry - int(h * 0.10)
    neck_bot_y = neck_top_y + int(h * 0.30)
    neck_w     = int(h * 0.24)
    draw.rectangle([cx - neck_w, neck_top_y, cx + neck_w, neck_bot_y], fill=SKIN)
    draw.rectangle([cx - neck_w, neck_top_y, cx + neck_w, neck_bot_y],
                   outline=LINE, width=4)

    # --- TORSO (shirt, tucked in, belt) ---
    torso_top = neck_bot_y
    torso_bot = top_y + int(h * 3.0)
    torso_w   = int(h * 0.75)
    # Shirt stripes
    draw_striped_rect(draw, cx - torso_w, torso_top, cx + torso_w, torso_bot)
    # Shirt outline
    draw.rectangle([cx - torso_w, torso_top, cx + torso_w, torso_bot],
                   outline=LINE, width=5)

    # Belt
    belt_y = torso_bot - int(h * 0.12)
    draw.rectangle([cx - torso_w + 4, belt_y,
                    cx + torso_w - 4, belt_y + int(h * 0.08)], fill=BELT)
    # Belt buckle
    draw.rectangle([cx - int(h * 0.07), belt_y - int(h * 0.02),
                    cx + int(h * 0.07), belt_y + int(h * 0.10)],
                   fill=BELT, outline=LINE, width=2)

    # --- ARMS ---
    arm_w   = int(h * 0.20)
    arm_h   = int(h * 0.80)
    shoulder_y = torso_top + int(h * 0.06)
    # Left arm (NOTEBOOK SIDE — just arm, notebook covers it)
    draw.rectangle([cx - torso_w - arm_w + int(h * 0.04), shoulder_y,
                    cx - torso_w + int(h * 0.04), shoulder_y + arm_h],
                   fill=STRIPE_A, outline=LINE, width=3)
    # Right arm
    draw.rectangle([cx + torso_w - int(h * 0.04), shoulder_y,
                    cx + torso_w + arm_w - int(h * 0.04), shoulder_y + arm_h],
                   fill=STRIPE_B, outline=LINE, width=3)
    # Hands
    hand_r = int(h * 0.14)
    # Left hand
    draw.ellipse([cx - torso_w - arm_w // 2 - hand_r + int(h * 0.04),
                  shoulder_y + arm_h - hand_r,
                  cx - torso_w - arm_w // 2 + hand_r + int(h * 0.04),
                  shoulder_y + arm_h + hand_r],
                 fill=SKIN, outline=LINE, width=3)
    # Right hand
    draw.ellipse([cx + torso_w + arm_w // 2 - hand_r - int(h * 0.04),
                  shoulder_y + arm_h - hand_r,
                  cx + torso_w + arm_w // 2 + hand_r - int(h * 0.04),
                  shoulder_y + arm_h + hand_r],
                 fill=SKIN, outline=LINE, width=3)

    # --- NOTEBOOK (always under left arm — mandatory) ---
    nb_x0 = cx - torso_w - arm_w - int(h * 0.10)
    nb_y0 = torso_top + int(h * 0.20)
    nb_x1 = nb_x0 + int(h * 0.20)
    nb_y1 = nb_y0 + int(h * 0.72)
    draw.rectangle([nb_x0, nb_y0, nb_x1, nb_y1], fill=NOTEBOOK)
    draw.line([nb_x0 + int(h * 0.04), nb_y0, nb_x0 + int(h * 0.04), nb_y1],
              fill=NOTEBK_SP, width=int(h * 0.04))
    draw.rectangle([nb_x0, nb_y0, nb_x1, nb_y1], outline=LINE, width=3)

    # --- PANTS ---
    pants_top  = torso_bot
    pants_bot  = top_y + int(h * 3.45)
    pants_w    = int(h * 0.68)
    leg_w      = int(h * 0.28)
    gap        = int(h * 0.04)
    # Left leg
    draw.rectangle([cx - pants_w, pants_top,
                    cx - gap, pants_bot], fill=PANTS)
    draw.line([cx - pants_w // 2 - gap // 2, pants_top,
               cx - pants_w // 2 - gap // 2, pants_bot],
              fill=PANTS_SH, width=2)   # center crease
    draw.rectangle([cx - pants_w, pants_top, cx - gap, pants_bot],
                   outline=LINE, width=3)
    # Right leg
    draw.rectangle([cx + gap, pants_top,
                    cx + pants_w, pants_bot], fill=PANTS)
    draw.line([cx + pants_w // 2 + gap // 2, pants_top,
               cx + pants_w // 2 + gap // 2, pants_bot],
              fill=PANTS_SH, width=2)
    draw.rectangle([cx + gap, pants_top, cx + pants_w, pants_bot],
                   outline=LINE, width=3)

    # --- SHOES ---
    shoe_y0 = pants_bot
    shoe_w  = int(h * 0.36)
    shoe_h  = int(h * 0.18)
    sole_h  = int(h * 0.08)
    for side in [-1, 1]:
        sx = cx + side * (pants_w // 2 + gap // 2)
        # Sole
        draw.ellipse([sx - shoe_w + 2, shoe_y0 + shoe_h - sole_h // 2,
                      sx + shoe_w - 2, shoe_y0 + shoe_h + sole_h],
                     fill=SHOE_SOLE)
        # Upper
        draw.ellipse([sx - shoe_w + 4, shoe_y0 - int(h * 0.04),
                      sx + shoe_w - 4, shoe_y0 + shoe_h],
                     fill=SHOE)
        draw.ellipse([sx - shoe_w + 4, shoe_y0 - int(h * 0.04),
                      sx + shoe_w - 4, shoe_y0 + shoe_h],
                     outline=LINE, width=3)

    # Cast shadow on ground
    sh_y = shoe_y0 + shoe_h + sole_h
    draw.ellipse([cx - int(h * 0.85), sh_y,
                  cx + int(h * 0.85), sh_y + int(h * 0.10)], fill=SHADOW_COL)


# ── 3/4 VIEW ──────────────────────────────────────────────────────────────────

def render_three_quarter(draw, cx, base_y):
    """3/4 view — head turned ~40°, body in 3/4."""
    S = SCALE
    h = int(hu() * S)
    top_y = base_y - int(CHAR_DRAW_H * S)
    head_cy = top_y + h

    # Head (slightly squished on far side)
    head_rx = int(h * 0.40)   # slightly narrower than front (foreshortened)
    head_ry = int(h * 0.52)

    # Near ear
    ear_r = int(h * 0.13)
    ear_y = head_cy + int(h * 0.10)
    draw.ellipse([cx - head_rx - ear_r + 4, ear_y - ear_r,
                  cx - head_rx + ear_r + 4, ear_y + ear_r],
                 fill=SKIN, outline=LINE, width=4)

    draw.ellipse([cx - head_rx, head_cy - head_ry,
                  cx + head_rx, head_cy + head_ry], fill=SKIN)

    # Hair
    hair_top = head_cy - head_ry - int(h * 0.10)
    hair_bot = head_cy - head_ry + int(h * 0.52)
    draw.ellipse([cx - head_rx - 4, hair_top,
                  cx + int(head_rx * 0.20), hair_bot + 4], fill=HAIR)
    draw.ellipse([cx - int(head_rx * 0.25), hair_top + 4,
                  cx + head_rx + 4, hair_bot + 2], fill=HAIR)
    draw.ellipse([cx - head_rx, head_cy - head_ry,
                  cx + head_rx, head_cy + head_ry],
                 outline=LINE, width=6)

    # Glasses (3/4): near lens full, far lens 65% wide
    lens_r     = int(h * 0.18)
    lens_r_far = int(lens_r * 0.65)
    frame_w    = max(4, int(h * 0.07))
    gcy        = head_cy + int(h * 0.08)
    lcx_g = cx - int(h * 0.25)
    lcy_g = gcy + int(h * 0.02)
    rcx_g = cx + int(h * 0.22)
    rcy_g = gcy - int(h * 0.02)

    # Near lens (full)
    draw.ellipse([lcx_g - lens_r, lcy_g - lens_r,
                  lcx_g + lens_r, lcy_g + lens_r], fill=GLASS_LN)
    draw.arc([lcx_g - int(lens_r * 0.7), lcy_g - lens_r + 2,
              lcx_g + int(lens_r * 0.7), lcy_g - lens_r + int(lens_r * 0.5)],
             start=200, end=340, fill=GLASS_GL, width=3)
    draw.ellipse([lcx_g - lens_r, lcy_g - lens_r,
                  lcx_g + lens_r, lcy_g + lens_r],
                 outline=GLASS_FR, width=frame_w)

    # Far lens (foreshortened)
    draw.ellipse([rcx_g - lens_r_far, rcy_g - lens_r,
                  rcx_g + lens_r_far, rcy_g + lens_r], fill=GLASS_LN)
    draw.arc([rcx_g - int(lens_r_far * 0.7), rcy_g - lens_r + 2,
              rcx_g + int(lens_r_far * 0.7), rcy_g - lens_r + int(lens_r * 0.5)],
             start=200, end=340, fill=GLASS_GL, width=3)
    draw.ellipse([rcx_g - lens_r_far, rcy_g - lens_r,
                  rcx_g + lens_r_far, rcy_g + lens_r],
                 outline=GLASS_FR, width=frame_w)

    # Bridge
    draw.line([lcx_g + lens_r, lcy_g, rcx_g - lens_r_far, rcy_g],
              fill=GLASS_FR, width=frame_w)
    # Near temple
    draw.line([lcx_g - lens_r, lcy_g,
               lcx_g - lens_r - int(h * 0.07), lcy_g + int(h * 0.02)],
              fill=GLASS_FR, width=max(3, frame_w - 1))
    # Far temple (going back)
    draw.line([rcx_g + lens_r_far, rcy_g,
               rcx_g + lens_r_far + int(h * 0.04), rcy_g + int(h * 0.02)],
              fill=GLASS_FR, width=max(2, frame_w - 2))

    # Eyes
    for (ex, ey, ir) in [(lcx_g, lcy_g, int(lens_r * 0.55)),
                          (rcx_g, rcy_g, int(lens_r_far * 0.55))]:
        pup_r = int(ir * 0.55)
        draw.ellipse([ex - ir, ey - ir, ex + ir, ey + ir], fill=EYE_W)
        draw.ellipse([ex - int(ir * 0.7), ey - int(ir * 0.7),
                      ex + int(ir * 0.7), ey + int(ir * 0.7)], fill=IRIS)
        draw.ellipse([ex - pup_r, ey - pup_r, ex + pup_r, ey + pup_r], fill=PUPIL)
        draw.ellipse([ex + int(ir * 0.3), ey - ir + 2,
                      ex + int(ir * 0.3) + 4, ey - ir + 6], fill=EYE_HL)

    # Nose (3/4 — slightly off-center)
    nose_cx = cx + int(h * 0.06)
    draw.arc([nose_cx - int(h * 0.06), head_cy + int(h * 0.28),
              nose_cx + int(h * 0.06), head_cy + int(h * 0.40)],
             start=0, end=180, fill=SKIN_SH, width=3)

    # Mouth
    mouth_y = head_cy + int(h * 0.55)
    draw.arc([cx - int(h * 0.10), mouth_y,
              cx + int(h * 0.16), mouth_y + int(h * 0.16)],
             start=10, end=170, fill=LINE, width=3)

    # Brows
    for (bx, side_sign) in [(lcx_g, -1), (rcx_g, 1)]:
        by = gcy - lens_r - int(h * 0.08)
        draw.arc([bx - int(h * 0.14), by - int(h * 0.04),
                  bx + int(h * 0.14), by + int(h * 0.06)],
                 start=200 if side_sign < 0 else 340,
                 end=340 if side_sign < 0 else 200,
                 fill=HAIR, width=3)

    # Neck
    neck_top_y = head_cy + head_ry - int(h * 0.10)
    neck_bot_y = neck_top_y + int(h * 0.30)
    neck_w     = int(h * 0.22)
    draw.rectangle([cx - neck_w, neck_top_y, cx + neck_w, neck_bot_y], fill=SKIN)
    draw.rectangle([cx - neck_w, neck_top_y, cx + neck_w, neck_bot_y],
                   outline=LINE, width=4)

    # Torso (3/4 — slightly narrower, shifted)
    torso_top = neck_bot_y
    torso_bot = top_y + int(h * 3.0)
    torso_w   = int(h * 0.68)
    draw_striped_rect(draw, cx - int(h * 0.05) - torso_w, torso_top,
                      cx - int(h * 0.05) + torso_w, torso_bot, tilt=int(h * 0.15))
    draw.rectangle([cx - int(h * 0.05) - torso_w, torso_top,
                    cx - int(h * 0.05) + torso_w, torso_bot],
                   outline=LINE, width=5)
    belt_y = torso_bot - int(h * 0.12)
    draw.rectangle([cx - int(h * 0.05) - torso_w + 4, belt_y,
                    cx - int(h * 0.05) + torso_w - 4, belt_y + int(h * 0.08)],
                   fill=BELT)

    # Arms (near arm more visible, far arm peeking)
    arm_w = int(h * 0.18)
    arm_h = int(h * 0.80)
    # Near arm (left)
    draw.rectangle([cx - int(h * 0.05) - torso_w - arm_w + int(h * 0.04),
                    torso_top + int(h * 0.06),
                    cx - int(h * 0.05) - torso_w + int(h * 0.04),
                    torso_top + int(h * 0.06) + arm_h],
                   fill=STRIPE_A, outline=LINE, width=3)
    hand_r = int(h * 0.14)
    draw.ellipse([cx - int(h * 0.05) - torso_w - arm_w // 2 - hand_r + int(h * 0.04),
                  torso_top + int(h * 0.06) + arm_h - hand_r,
                  cx - int(h * 0.05) - torso_w - arm_w // 2 + hand_r + int(h * 0.04),
                  torso_top + int(h * 0.06) + arm_h + hand_r],
                 fill=SKIN, outline=LINE, width=3)
    # Notebook (tucked, near arm)
    nb_x0 = cx - int(h * 0.05) - torso_w - arm_w - int(h * 0.12)
    nb_y0 = torso_top + int(h * 0.24)
    nb_x1 = nb_x0 + int(h * 0.20)
    nb_y1 = nb_y0 + int(h * 0.72)
    draw.rectangle([nb_x0, nb_y0, nb_x1, nb_y1], fill=NOTEBOOK)
    draw.line([nb_x0 + int(h * 0.04), nb_y0, nb_x0 + int(h * 0.04), nb_y1],
              fill=NOTEBK_SP, width=int(h * 0.04))
    draw.rectangle([nb_x0, nb_y0, nb_x1, nb_y1], outline=LINE, width=3)

    # Far arm (peeking)
    draw.rectangle([cx - int(h * 0.05) + torso_w - int(h * 0.04),
                    torso_top + int(h * 0.06),
                    cx - int(h * 0.05) + torso_w + arm_w - int(h * 0.04),
                    torso_top + int(h * 0.06) + int(arm_h * 0.85)],
                   fill=STRIPE_B, outline=LINE, width=3)

    # Pants
    pants_top  = torso_bot
    pants_bot  = top_y + int(h * 3.45)
    leg_w      = int(h * 0.28)
    gap        = int(h * 0.04)
    left_cx    = cx - int(h * 0.05) - int(h * 0.38)
    right_cx   = cx - int(h * 0.05) + int(h * 0.38)
    draw.rectangle([left_cx  - leg_w, pants_top, left_cx  + leg_w, pants_bot], fill=PANTS)
    draw.line([left_cx, pants_top, left_cx, pants_bot], fill=PANTS_SH, width=2)
    draw.rectangle([left_cx  - leg_w, pants_top, left_cx  + leg_w, pants_bot],
                   outline=LINE, width=3)
    draw.rectangle([right_cx - leg_w, pants_top, right_cx + leg_w, pants_bot], fill=PANTS)
    draw.line([right_cx, pants_top, right_cx, pants_bot], fill=PANTS_SH, width=2)
    draw.rectangle([right_cx - leg_w, pants_top, right_cx + leg_w, pants_bot],
                   outline=LINE, width=3)

    # Shoes
    shoe_y0 = pants_bot
    shoe_w  = int(h * 0.34)
    shoe_h  = int(h * 0.18)
    sole_h  = int(h * 0.08)
    for sx in [left_cx, right_cx]:
        draw.ellipse([sx - shoe_w + 2, shoe_y0 + shoe_h - sole_h // 2,
                      sx + shoe_w - 2, shoe_y0 + shoe_h + sole_h],
                     fill=SHOE_SOLE)
        draw.ellipse([sx - shoe_w + 4, shoe_y0 - int(h * 0.04),
                      sx + shoe_w - 4, shoe_y0 + shoe_h],
                     fill=SHOE)
        draw.ellipse([sx - shoe_w + 4, shoe_y0 - int(h * 0.04),
                      sx + shoe_w - 4, shoe_y0 + shoe_h],
                     outline=LINE, width=3)

    # Ground shadow
    sh_y = shoe_y0 + shoe_h + sole_h
    draw.ellipse([cx - int(h * 0.85), sh_y,
                  cx + int(h * 0.85), sh_y + int(h * 0.10)], fill=SHADOW_COL)


# ── SIDE VIEW ─────────────────────────────────────────────────────────────────
# CRITICAL FIX: Previous side view was a flat rectangle.
# This version shows believable 3D form:
#   - Head in true profile (facing left)
#   - Torso shown as a narrow depth strip (front-to-back depth visible)
#   - Shirt stripe lines run horizontally (perpendicular to viewing direction)
#   - Notebook visible as edge-on (spine visible from side)
#   - Near leg in front, far leg behind
#   - Shoe shows the side profile (length visible)

def render_side(draw, cx, base_y):
    """Side profile view. Character faces RIGHT (viewer left = back of head)."""
    S = SCALE
    h = int(hu() * S)
    top_y  = base_y - int(CHAR_DRAW_H * S)
    head_cy = top_y + h

    # HEAD IN PROFILE — oval squished to profile view
    # Profile: narrow L-R but taller (head depth = front-to-back)
    head_front_x = cx + int(h * 0.48)   # nose/chin forward
    head_back_x  = cx - int(h * 0.40)   # back of skull
    head_top_y   = head_cy - int(h * 0.52)
    head_bot_y   = head_cy + int(h * 0.52)

    # Ear (on side — the visible ear)
    ear_cx = cx - int(h * 0.06)
    ear_cy = head_cy + int(h * 0.10)
    ear_rx = int(h * 0.12)
    ear_ry = int(h * 0.16)
    draw.ellipse([ear_cx - ear_rx, ear_cy - ear_ry,
                  ear_cx + ear_rx, ear_cy + ear_ry], fill=SKIN)
    # Inner ear detail
    draw.ellipse([ear_cx - int(ear_rx * 0.6), ear_cy - int(ear_ry * 0.6),
                  ear_cx + int(ear_rx * 0.6), ear_cy + int(ear_ry * 0.6)],
                 fill=SKIN_SH)
    draw.ellipse([ear_cx - ear_rx, ear_cy - ear_ry,
                  ear_cx + ear_rx, ear_cy + ear_ry], outline=LINE, width=4)

    # Head shape (profile polygon approximation)
    head_pts = [
        (cx, head_top_y - int(h * 0.04)),      # crown top-center
        (head_front_x - int(h * 0.12), head_top_y),  # forehead
        (head_front_x, head_cy - int(h * 0.22)),     # mid-forehead
        (head_front_x + int(h * 0.06), head_cy + int(h * 0.10)),  # nose bump
        (head_front_x - int(h * 0.04), head_cy + int(h * 0.30)),  # upper lip
        (head_front_x - int(h * 0.08), head_cy + int(h * 0.44)),  # chin
        (cx - int(h * 0.14), head_bot_y),      # jaw
        (head_back_x + int(h * 0.04), head_cy + int(h * 0.30)),  # back lower
        (head_back_x, head_cy),                  # back of skull center
        (head_back_x + int(h * 0.04), head_cy - int(h * 0.40)),  # back upper
    ]
    draw.polygon(head_pts, fill=SKIN)
    draw.polygon(head_pts, outline=LINE, width=5)

    # Hair (profile — main mass going backward over skull)
    hair_back_x  = head_back_x - int(h * 0.04)
    hair_top_y   = head_top_y - int(h * 0.12)
    hair_pts = [
        (cx - int(h * 0.02), hair_top_y),
        (head_front_x - int(h * 0.16), head_top_y + int(h * 0.02)),  # forehead hairline
        (head_front_x - int(h * 0.26), head_top_y + int(h * 0.16)),  # front fade
        (cx - int(h * 0.08), head_top_y + int(h * 0.12)),
        (hair_back_x, head_cy - int(h * 0.22)),  # back of head
        (hair_back_x + int(h * 0.02), head_cy + int(h * 0.06)),      # nape
        (head_back_x + int(h * 0.06), head_cy + int(h * 0.22)),      # lower nape
    ]
    draw.polygon(hair_pts + [(cx, hair_top_y)], fill=HAIR)
    # Hair highlight
    draw.arc([cx - int(h * 0.04), hair_top_y - int(h * 0.04),
              cx + int(h * 0.08), hair_top_y + int(h * 0.12)],
             start=260, end=60, fill=HAIR_HL, width=3)

    # GLASSES (SIDE VIEW): single lens visible as circle protruding past nose,
    # temple arm going straight back over ear.
    glasses_cx = head_front_x + int(h * 0.06)   # lens protrudes past face plane
    glasses_cy = head_cy - int(h * 0.14)          # eye level
    lens_r     = int(h * 0.18)
    frame_w    = max(4, int(h * 0.07))
    # Lens circle
    draw.ellipse([glasses_cx - lens_r, glasses_cy - lens_r,
                  glasses_cx + lens_r, glasses_cy + lens_r], fill=GLASS_LN)
    # Glare
    draw.arc([glasses_cx - int(lens_r * 0.7), glasses_cy - lens_r + 2,
              glasses_cx + int(lens_r * 0.7), glasses_cy - lens_r + int(lens_r * 0.5)],
             start=200, end=340, fill=GLASS_GL, width=3)
    draw.ellipse([glasses_cx - lens_r, glasses_cy - lens_r,
                  glasses_cx + lens_r, glasses_cy + lens_r],
                 outline=GLASS_FR, width=frame_w)
    # Temple (going straight back over ear)
    temple_start = (glasses_cx - lens_r, glasses_cy)
    temple_end   = (ear_cx - ear_rx, ear_cy - int(ear_ry * 0.6))
    draw.line([temple_start, temple_end], fill=GLASS_FR,
              width=max(3, frame_w - 1))
    # Nose bridge attachment (bridge nub going toward face)
    draw.line([glasses_cx - lens_r - 2, glasses_cy,
               head_front_x + int(h * 0.01), glasses_cy],
              fill=GLASS_FR, width=max(2, frame_w - 2))

    # Eye (inside glasses, profile — just iris + pupil)
    iris_r = int(lens_r * 0.55)
    pup_r  = int(iris_r * 0.55)
    ex, ey = glasses_cx - int(h * 0.04), glasses_cy
    draw.ellipse([ex - iris_r, ey - iris_r, ex + iris_r, ey + iris_r], fill=EYE_W)
    draw.ellipse([ex - int(iris_r * 0.7), ey - int(iris_r * 0.7),
                  ex + int(iris_r * 0.7), ey + int(iris_r * 0.7)], fill=IRIS)
    draw.ellipse([ex - pup_r, ey - pup_r, ex + pup_r, ey + pup_r], fill=PUPIL)

    # Brow (single — above glasses)
    brow_y = glasses_cy - lens_r - int(h * 0.09)
    draw.arc([glasses_cx - int(h * 0.16), brow_y - int(h * 0.04),
              glasses_cx + int(h * 0.12), brow_y + int(h * 0.06)],
             start=190, end=0, fill=HAIR, width=3)

    # Nose (profile — distinct protrusion)
    nose_x = head_front_x + int(h * 0.06)
    nose_y = head_cy + int(h * 0.10)
    draw.arc([nose_x - int(h * 0.14), nose_y - int(h * 0.10),
              nose_x + int(h * 0.04), nose_y + int(h * 0.14)],
             start=270, end=90, fill=SKIN_SH, width=4)

    # Mouth (profile — closed)
    mouth_x = head_front_x - int(h * 0.06)
    mouth_y = head_cy + int(h * 0.40)
    draw.line([mouth_x, mouth_y, mouth_x + int(h * 0.12), mouth_y + int(h * 0.02)],
              fill=LINE, width=3)

    # --- NECK (profile — narrow strip) ---
    neck_top_y = head_bot_y - int(h * 0.30)
    neck_bot_y = neck_top_y + int(h * 0.32)
    neck_front = cx + int(h * 0.16)
    neck_back  = cx - int(h * 0.16)
    draw.rectangle([neck_back, neck_top_y, neck_front, neck_bot_y], fill=SKIN)
    draw.rectangle([neck_back, neck_top_y, neck_front, neck_bot_y],
                   outline=LINE, width=3)

    # --- TORSO (SIDE VIEW — KEY FIX) ---
    # Show the depth of the torso: front face + depth strip.
    # Cosmo has a slim-fit shirt, so depth ≈ 0.42 head units.
    torso_top    = neck_bot_y
    torso_bot    = top_y + int(h * 3.0)
    torso_front  = cx + int(h * 0.30)   # chest face
    torso_back   = cx - int(h * 0.28)   # back face
    torso_depth  = torso_front - torso_back

    # Draw torso body (front face visible — stripes horizontal, across depth)
    # Stripe lines horizontal = proper profile shirt read
    stripe_count = 12
    total_h_torso = torso_bot - torso_top
    stripe_h_t = total_h_torso // stripe_count
    for i in range(stripe_count):
        sy = torso_top + i * stripe_h_t
        ey = min(torso_top + (i+1) * stripe_h_t, torso_bot)
        col = STRIPE_A if i % 2 == 0 else STRIPE_B
        draw.rectangle([torso_back, sy, torso_front, ey], fill=col)

    # Front edge (visible face of torso)
    draw.line([torso_front, torso_top, torso_front, torso_bot],
              fill=LINE, width=5)
    # Back edge
    draw.line([torso_back, torso_top, torso_back, torso_bot],
              fill=LINE, width=5)
    # Top edge (shoulder line)
    draw.line([torso_back, torso_top, torso_front, torso_top],
              fill=LINE, width=4)
    # Bottom edge (hem)
    draw.line([torso_back, torso_bot, torso_front, torso_bot],
              fill=LINE, width=4)

    # Belt (visible in side — thin strip across depth)
    belt_y = torso_bot - int(h * 0.12)
    draw.rectangle([torso_back + 2, belt_y,
                    torso_front - 2, belt_y + int(h * 0.08)], fill=BELT)

    # --- NOTEBOOK from side (edge-on — showing the book as a thin rectangle) ---
    # From side, notebook tucked under front arm = visible as a vertical rectangle
    # at the front of the body, under left arm.
    nb_w  = int(h * 0.06)   # thin edge (front-to-back of notebook)
    nb_h  = int(h * 0.72)
    nb_x0 = torso_front - nb_w
    nb_y0 = torso_top + int(h * 0.24)
    nb_x1 = torso_front + int(h * 0.22)   # extends past front face
    nb_y1 = nb_y0 + nb_h
    draw.rectangle([nb_x0, nb_y0, nb_x1, nb_y1], fill=NOTEBOOK)
    # Page edge (cream) visible at bottom
    draw.line([nb_x0, nb_y1, nb_x1, nb_y1], fill=NOTEBK_PG, width=3)
    draw.rectangle([nb_x0, nb_y0, nb_x1, nb_y1], outline=LINE, width=3)

    # --- ARM visible from side (the near arm — front of body) ---
    arm_front_x = torso_front
    arm_top_y   = torso_top + int(h * 0.06)
    arm_bot_y   = arm_top_y + int(h * 0.82)
    arm_depth_w = int(h * 0.22)
    draw.rectangle([arm_front_x - arm_depth_w, arm_top_y,
                    arm_front_x, arm_bot_y], fill=STRIPE_A)
    draw.rectangle([arm_front_x - arm_depth_w, arm_top_y,
                    arm_front_x, arm_bot_y], outline=LINE, width=3)
    # Hand
    hand_r = int(h * 0.14)
    hand_cx = arm_front_x - arm_depth_w // 2
    draw.ellipse([hand_cx - hand_r, arm_bot_y - hand_r,
                  hand_cx + hand_r, arm_bot_y + hand_r],
                 fill=SKIN, outline=LINE, width=3)

    # --- PANTS (side view) ---
    pants_top = torso_bot
    pants_bot = top_y + int(h * 3.45)
    # Near leg (foreground)
    near_front  = torso_front
    near_back   = cx - int(h * 0.12)
    leg_depth   = near_front - near_back
    # Near leg: full depth visible
    draw.rectangle([near_back, pants_top, near_front, pants_bot], fill=PANTS)
    # Center crease (vertical down middle)
    mid_x = (near_back + near_front) // 2
    draw.line([mid_x, pants_top, mid_x, pants_bot], fill=PANTS_SH, width=2)
    draw.rectangle([near_back, pants_top, near_front, pants_bot],
                   outline=LINE, width=4)
    # Far leg (behind — only back edge visible, offset)
    far_front = near_back - int(h * 0.04)
    far_back  = far_front - leg_depth
    draw.rectangle([far_back, pants_top, far_front, pants_bot], fill=PANTS_SH)
    draw.line([far_back, pants_top, far_back, pants_bot], fill=LINE, width=3)
    draw.line([far_front, pants_top, far_front, pants_bot], fill=LINE, width=2)

    # --- SHOES (side profile) ---
    shoe_y0  = pants_bot
    shoe_len = int(h * 0.60)   # shoe length in profile (clearly shows length depth)
    shoe_h_s = int(h * 0.20)
    sole_h   = int(h * 0.08)
    # Near shoe (profile — elongated)
    shoe_x0  = cx - int(h * 0.18)   # heel
    shoe_x1  = shoe_x0 + shoe_len   # toe
    # Sole
    draw.rectangle([shoe_x0, shoe_y0 + shoe_h_s,
                    shoe_x1, shoe_y0 + shoe_h_s + sole_h], fill=SHOE_SOLE)
    draw.rectangle([shoe_x0, shoe_y0 + shoe_h_s,
                    shoe_x1, shoe_y0 + shoe_h_s + sole_h],
                   outline=LINE, width=2)
    # Upper (rounded at toe)
    draw.rectangle([shoe_x0, shoe_y0 - int(h * 0.04),
                    shoe_x1 - int(h * 0.10), shoe_y0 + shoe_h_s], fill=SHOE)
    draw.ellipse([shoe_x1 - int(h * 0.22), shoe_y0 + int(h * 0.01),
                  shoe_x1, shoe_y0 + shoe_h_s], fill=SHOE)
    draw.polygon([
        (shoe_x0, shoe_y0 - int(h * 0.04)),
        (shoe_x1 - int(h * 0.10), shoe_y0 - int(h * 0.04)),
        (shoe_x1, shoe_y0 + int(h * 0.01)),
        (shoe_x1, shoe_y0 + shoe_h_s),
        (shoe_x0, shoe_y0 + shoe_h_s),
    ], outline=LINE, width=4)

    # Far shoe (behind, just heel visible)
    far_shoe_x0 = shoe_x0 - int(h * 0.12)
    draw.rectangle([far_shoe_x0, shoe_y0 - int(h * 0.02),
                    shoe_x0 + int(h * 0.15), shoe_y0 + shoe_h_s + sole_h],
                   fill=SHOE_SH, outline=LINE, width=2)

    # Ground shadow
    sh_y = shoe_y0 + shoe_h_s + sole_h
    draw.ellipse([cx - int(h * 0.70), sh_y,
                  cx + int(h * 0.70), sh_y + int(h * 0.08)], fill=SHADOW_COL)


# ── BACK VIEW ─────────────────────────────────────────────────────────────────

def render_back(draw, cx, base_y):
    """Back view. Glasses not visible. Back of hair + shirt stripes (back)."""
    S = SCALE
    h = int(hu() * S)
    top_y = base_y - int(CHAR_DRAW_H * S)
    head_cy = top_y + h

    head_rx = int(h * 0.44)
    head_ry = int(h * 0.52)

    # Ears
    ear_r = int(h * 0.13)
    ear_y = head_cy + int(h * 0.10)
    draw.ellipse([cx - head_rx - ear_r + 4, ear_y - ear_r,
                  cx - head_rx + ear_r + 4, ear_y + ear_r],
                 fill=SKIN, outline=LINE, width=4)
    draw.ellipse([cx + head_rx - ear_r - 4, ear_y - ear_r,
                  cx + head_rx + ear_r - 4, ear_y + ear_r],
                 fill=SKIN, outline=LINE, width=4)

    # Head (shows back of skull)
    draw.ellipse([cx - head_rx, head_cy - head_ry,
                  cx + head_rx, head_cy + head_ry], fill=SKIN)

    # Hair (back — full mass, no part visible)
    hair_top = head_cy - head_ry - int(h * 0.12)
    hair_bot = head_cy - head_ry + int(h * 0.58)
    draw.ellipse([cx - head_rx - 4, hair_top,
                  cx + head_rx + 4, hair_bot + 4], fill=HAIR)
    # Some hair highlight
    draw.arc([cx - int(head_rx * 0.6), hair_top + int(h * 0.06),
              cx + int(head_rx * 0.6), hair_top + int(h * 0.26)],
             start=200, end=340, fill=HAIR_HL, width=3)
    draw.ellipse([cx - head_rx, head_cy - head_ry,
                  cx + head_rx, head_cy + head_ry],
                 outline=LINE, width=6)

    # Neck
    neck_top_y = head_cy + head_ry - int(h * 0.10)
    neck_bot_y = neck_top_y + int(h * 0.30)
    neck_w     = int(h * 0.24)
    draw.rectangle([cx - neck_w, neck_top_y, cx + neck_w, neck_bot_y], fill=SKIN)
    draw.rectangle([cx - neck_w, neck_top_y, cx + neck_w, neck_bot_y],
                   outline=LINE, width=4)

    # Torso (back — same stripes, shirt back)
    torso_top = neck_bot_y
    torso_bot = top_y + int(h * 3.0)
    torso_w   = int(h * 0.75)
    draw_striped_rect(draw, cx - torso_w, torso_top, cx + torso_w, torso_bot)
    draw.rectangle([cx - torso_w, torso_top, cx + torso_w, torso_bot],
                   outline=LINE, width=5)
    belt_y = torso_bot - int(h * 0.12)
    draw.rectangle([cx - torso_w + 4, belt_y,
                    cx + torso_w - 4, belt_y + int(h * 0.08)], fill=BELT)

    # Arms (no notebook visible from back)
    arm_w = int(h * 0.20)
    arm_h = int(h * 0.80)
    shoulder_y = torso_top + int(h * 0.06)
    for side in [-1, 1]:
        col = STRIPE_B if side < 0 else STRIPE_A
        draw.rectangle([cx + side * torso_w + (int(h * 0.04) if side < 0 else -int(h * 0.04)) - (arm_w if side < 0 else 0),
                        shoulder_y,
                        cx + side * torso_w + (int(h * 0.04) + arm_w if side < 0 else -int(h * 0.04)),
                        shoulder_y + arm_h],
                       fill=col, outline=LINE, width=3)
    hand_r = int(h * 0.14)
    draw.ellipse([cx - torso_w - arm_w // 2 - hand_r + int(h * 0.04),
                  shoulder_y + arm_h - hand_r,
                  cx - torso_w - arm_w // 2 + hand_r + int(h * 0.04),
                  shoulder_y + arm_h + hand_r],
                 fill=SKIN, outline=LINE, width=3)
    draw.ellipse([cx + torso_w + arm_w // 2 - hand_r - int(h * 0.04),
                  shoulder_y + arm_h - hand_r,
                  cx + torso_w + arm_w // 2 + hand_r - int(h * 0.04),
                  shoulder_y + arm_h + hand_r],
                 fill=SKIN, outline=LINE, width=3)

    # Pants (back)
    pants_top = torso_bot
    pants_bot = top_y + int(h * 3.45)
    pants_w   = int(h * 0.68)
    gap       = int(h * 0.04)
    draw.rectangle([cx - pants_w, pants_top, cx - gap, pants_bot], fill=PANTS)
    draw.line([cx - pants_w // 2 - gap // 2, pants_top,
               cx - pants_w // 2 - gap // 2, pants_bot], fill=PANTS_SH, width=2)
    draw.rectangle([cx - pants_w, pants_top, cx - gap, pants_bot],
                   outline=LINE, width=3)
    draw.rectangle([cx + gap, pants_top, cx + pants_w, pants_bot], fill=PANTS)
    draw.line([cx + pants_w // 2 + gap // 2, pants_top,
               cx + pants_w // 2 + gap // 2, pants_bot], fill=PANTS_SH, width=2)
    draw.rectangle([cx + gap, pants_top, cx + pants_w, pants_bot],
                   outline=LINE, width=3)

    # Shoes (back)
    shoe_y0 = pants_bot
    shoe_w  = int(h * 0.36)
    shoe_h  = int(h * 0.18)
    sole_h  = int(h * 0.08)
    for sx in [cx - pants_w // 2 - gap // 2, cx + pants_w // 2 + gap // 2]:
        draw.ellipse([sx - shoe_w + 2, shoe_y0 + shoe_h - sole_h // 2,
                      sx + shoe_w - 2, shoe_y0 + shoe_h + sole_h],
                     fill=SHOE_SOLE)
        draw.ellipse([sx - shoe_w + 4, shoe_y0 - int(h * 0.04),
                      sx + shoe_w - 4, shoe_y0 + shoe_h],
                     fill=SHOE)
        draw.ellipse([sx - shoe_w + 4, shoe_y0 - int(h * 0.04),
                      sx + shoe_w - 4, shoe_y0 + shoe_h],
                     outline=LINE, width=3)

    sh_y = shoe_y0 + shoe_h + sole_h
    draw.ellipse([cx - int(h * 0.85), sh_y,
                  cx + int(h * 0.85), sh_y + int(h * 0.10)], fill=SHADOW_COL)


# ── MAIN ASSEMBLY ─────────────────────────────────────────────────────────────

def build_turnaround():
    # Render at 2× then scale
    canvas_w2 = CANVAS_W * SCALE
    canvas_h2 = CANVAS_H * SCALE
    img2 = Image.new("RGB", (canvas_w2, canvas_h2), CANVAS_BG)
    draw2 = ImageDraw.Draw(img2)

    # Panel backgrounds
    for v in range(N_VIEWS):
        x0 = v * VIEW_W * SCALE
        x1 = (v + 1) * VIEW_W * SCALE
        col = (245, 240, 232) if v % 2 == 0 else (240, 236, 228)
        draw2.rectangle([x0, 0, x1, canvas_h2], fill=col)

    # Draw views
    render_fns = [render_front, render_three_quarter, render_side, render_back]

    for v, fn in enumerate(render_fns):
        panel_cx  = v * VIEW_W * SCALE + VIEW_W * SCALE // 2
        body_top2 = HEADER_H * SCALE
        body_bot2 = (VIEW_H - LABEL_H) * SCALE
        base_y2   = body_bot2 - int(BODY_H * SCALE * 0.04)   # ground line
        fn(draw2, panel_cx, base_y2)

    # HU ruler line (top header area) + view dividers
    for v in range(1, N_VIEWS):
        x = v * VIEW_W * SCALE
        draw2.line([(x, 0), (x, canvas_h2)], fill=(180, 170, 155), width=2 * SCALE)

    # Scale back to 1×
    img = img2.resize((CANVAS_W, CANVAS_H), Image.LANCZOS)
    draw = ImageDraw.Draw(img)

    # Header text
    try:
        font_title = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
        font_label = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14)
        font_sub   = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)
    except Exception:
        font_title = ImageFont.load_default()
        font_label = font_title
        font_sub   = font_title

    title = "COSMO — Character Turnaround v002  |  Luma & the Glitchkin  |  Cycle 25 / Maya Santos"
    sub   = "v002 FIX: SIDE view now shows full 3D depth — profile head, depth torso, near/far legs"
    draw.text((16, 6), title, fill=LABEL_COL, font=font_title)
    draw.text((16, 28), sub, fill=(120, 100, 80), font=font_sub)

    # View labels (bottom bar)
    for v, label in enumerate(VIEWS):
        lx = v * VIEW_W + VIEW_W // 2
        ly = VIEW_H - LABEL_H + 6
        try:
            lb = draw.textbbox((0, 0), label, font=font_label)
            lw = lb[2] - lb[0]
            draw.text((lx - lw // 2, ly), label, fill=LABEL_COL, font=font_label)
        except Exception:
            draw.text((lx - 20, ly), label, fill=LABEL_COL)

    # Dividers at 1×
    for v in range(1, N_VIEWS):
        x = v * VIEW_W
        draw.line([(x, 0), (x, CANVAS_H)], fill=(150, 138, 120), width=1)

    return img


def main():
    out_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "characters", "main", "turnarounds"
    )
    os.makedirs(out_dir, exist_ok=True)

    img = build_turnaround()
    out_path = os.path.join(out_dir, "LTG_CHAR_cosmo_turnaround_v002.png")
    img.save(out_path)
    print(f"Saved: {out_path}")
    print(f"  Size: {img.size[0]}x{img.size[1]}px")
    print("  v002 FIX: Side view now shows believable 3D form:")
    print("    - Profile head (polygon, not ellipse)")
    print("    - Torso has front-to-back depth (horizontal stripe lines)")
    print("    - Notebook edge-on visible from side")
    print("    - Near leg front / far leg behind")
    print("    - Shoe shows side profile with length depth")


if __name__ == "__main__":
    main()
