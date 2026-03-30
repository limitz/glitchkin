#!/usr/bin/env python3
"""
LTG_TOOL_cosmo_turnaround.py
Cosmo — 4-View Character Turnaround v002
"Luma & the Glitchkin" — Cycle 25 / Maya Santos
Rebuilt C32 (Kai Nakamura) — original LTG_CHAR_ source deleted by C29 cleanup.

v002 FIX from v001 (per pitch_package_index.md):
  - Side view had no 3D depth (architecturally broken).
  - Fix: Side view now shows head profile (offset eye/nose/mouth positions),
    foreshortened torso depth (trapezoidal shoulder), profile arm placement,
    and shoes at side angle showing sole depth.

Cosmo spec (cosmo.md + cosmo_color_model.md):
  - Rectangular head (height:width = 1.16:1), corner radius 0.12 units
  - 4.0 heads tall
  - Glasses: always present, 7° CCW tilt, thick warm espresso frames
  - Notebook: tucked under left arm (right side in FRONT view)
  - Striped shirt: cerulean + sage horizontal stripes
  - Slim chinos, low-profile shoes

4 views: FRONT, 3/4, SIDE, BACK
Canvas: 1600×700px raw → thumbnail to 1280×560 (≤ 1280px rule)
2× render + LANCZOS for sub-pixel AA

Output: output/characters/main/turnarounds/LTG_CHAR_cosmo_turnaround.png
"""

from PIL import Image, ImageDraw, ImageFont
import math
import os
import random

# ── Palette (from cosmo_color_model.md) ──────────────────────────────────────
SKIN        = (217, 192, 154)   # #D9C09A Light Warm Olive
SKIN_SH     = (184, 154, 120)   # #B89A78 Warm Sand
SKIN_HL     = (238, 212, 176)   # #EED4B0 Pale Golden
HAIR        = ( 26,  24,  36)   # #1A1824 Blue-Black
HAIR_SH     = ( 14,  14,  24)   # #0E0E18 Near-Void
HAIR_HL     = ( 44,  43,  64)   # #2C2B40 Dark Slate
EYE_W       = (250, 240, 220)   # #FAF0DC Warm Cream
IRIS        = ( 61, 107,  69)   # #3D6B45 Forest Green
PUPIL       = ( 59,  40,  32)   # #3B2820 Deep Cocoa
EYE_HL      = (240, 240, 240)   # #F0F0F0 Static White
GLASS_FRAME = ( 92,  58,  32)   # #5C3A20 Warm Espresso Brown
GLASS_LENS  = (238, 244, 255)   # #EEF4FF Ghost Blue
GLASS_GLARE = (240, 240, 240)   # #F0F0F0 Static White
STRIPE_A    = ( 91, 141, 184)   # #5B8DB8 Cerulean Blue
STRIPE_B    = (122, 158, 126)   # #7A9E7E Sage Green
STRIPE_A_SH = ( 61, 107, 138)   # #3D6B8A Deep Cerulean
PANTS       = (140, 136, 128)   # #8C8880 Warm Mid-Gray
PANTS_SH    = (106, 100,  96)   # #6A6460 Mid-Dark Gray
SHOE        = ( 92,  58,  32)   # #5C3A20 Warm Espresso
SHOE_SOLE   = (184, 154, 120)   # #B89A78 Warm Sand
NOTEBOOK    = ( 91, 141, 184)   # #5B8DB8 Cerulean Blue
LINE        = ( 59,  40,  32)   # #3B2820 Deep Cocoa
CANVAS_BG   = (248, 244, 238)
SHADOW_COL  = (210, 200, 185)
PANEL_BG    = (242, 238, 232)

# ── Layout ────────────────────────────────────────────────────────────────────
CANVAS_W  = 1600
CANVAS_H  = 700
VIEWS     = ["FRONT", "3/4", "SIDE", "BACK"]
N_VIEWS   = 4
VIEW_W    = CANVAS_W // N_VIEWS
VIEW_H    = CANVAS_H
HEADER_H  = 52
LABEL_H   = 36
BODY_H    = VIEW_H - HEADER_H - LABEL_H   # 612px character area

SCALE = 2
CHAR_DRAW_H = int(BODY_H * 0.84)  # ~514px at 2x render


def hu():
    """One head unit. Cosmo is 4.0 heads tall."""
    return CHAR_DRAW_H / 4.0


def draw_stripe_shirt(draw, cx, top_y, bot_y, width, stripe_h=None):
    """Draw horizontal cerulean/sage stripes on shirt zone."""
    if stripe_h is None:
        stripe_h = max(6, int(hu() * SCALE * 0.12))
    y = top_y
    color_cycle = [STRIPE_A, STRIPE_B]
    ci = 0
    while y < bot_y:
        end_y = min(y + stripe_h, bot_y)
        x0 = cx - width // 2
        x1 = cx + width // 2
        draw.rectangle([x0, y, x1, end_y], fill=color_cycle[ci % 2])
        ci += 1
        y = end_y


def draw_glasses(draw, cx, cy, h, tilt_deg=7, lens_r_x=None, lens_r_y=None):
    """Draw Cosmo's signature glasses (7° tilt, thick espresso frames)."""
    if lens_r_x is None:
        lens_r_x = int(h * 0.20)
    if lens_r_y is None:
        lens_r_y = int(h * 0.14)
    sep = int(h * 0.36)
    rad = math.radians(tilt_deg)
    for side in [-1, 1]:
        lx = cx + side * sep // 2
        # Lens fill (ghost blue tint)
        draw.ellipse([lx - lens_r_x, cy - lens_r_y,
                      lx + lens_r_x, cy + lens_r_y], fill=GLASS_LENS)
        # Lens outline (thick frame)
        draw.ellipse([lx - lens_r_x, cy - lens_r_y,
                      lx + lens_r_x, cy + lens_r_y], outline=GLASS_FRAME, width=5)
        # Lens glare (upper edge crescent)
        draw.arc([lx - lens_r_x + 3, cy - lens_r_y + 3,
                  lx + lens_r_x - 3, cy + lens_r_y - 3],
                 start=200, end=340, fill=GLASS_GLARE, width=3)
    # Bridge
    bridge_y = cy - int(lens_r_y * 0.15)
    draw.line([cx - sep // 2 + lens_r_x - 3, bridge_y,
               cx + sep // 2 - lens_r_x + 3, bridge_y],
              fill=GLASS_FRAME, width=4)
    # Temple arms
    for side in [-1, 1]:
        lx = cx + side * sep // 2
        draw.line([lx + side * lens_r_x, cy,
                   lx + side * (lens_r_x + int(h * 0.22)), cy - int(h * 0.06)],
                  fill=GLASS_FRAME, width=4)


def draw_head_rect(draw, cx, cy, h):
    """Rectangular head with rounded corners (Cosmo canonical)."""
    hw = int(h * 0.86 / 2)   # width = 0.86 head units
    hh = int(h * 0.50)        # half-height
    cr = int(h * 0.12)        # corner radius
    # Main face fill (rounded rect via polygon + ellipses)
    draw.rectangle([cx - hw + cr, cy - hh, cx + hw - cr, cy + hh], fill=SKIN)
    draw.rectangle([cx - hw, cy - hh + cr, cx + hw, cy + hh - cr], fill=SKIN)
    for (ox, oy) in [(cx - hw + cr, cy - hh + cr),
                     (cx + hw - cr, cy - hh + cr),
                     (cx - hw + cr, cy + hh - cr),
                     (cx + hw - cr, cy + hh - cr)]:
        draw.ellipse([ox - cr, oy - cr, ox + cr, oy + cr], fill=SKIN)
    # Outline (simulate rounded-rect outline)
    draw.line([cx - hw + cr, cy - hh, cx + hw - cr, cy - hh], fill=LINE, width=4)
    draw.line([cx - hw + cr, cy + hh, cx + hw - cr, cy + hh], fill=LINE, width=4)
    draw.line([cx - hw, cy - hh + cr, cx - hw, cy + hh - cr], fill=LINE, width=4)
    draw.line([cx + hw, cy - hh + cr, cx + hw, cy + hh - cr], fill=LINE, width=4)
    for (ox, oy, a0, a1) in [(cx - hw + cr, cy - hh + cr, 180, 270),
                               (cx + hw - cr, cy - hh + cr, 270, 360),
                               (cx - hw + cr, cy + hh - cr, 90, 180),
                               (cx + hw - cr, cy + hh - cr, 0, 90)]:
        draw.arc([ox - cr, oy - cr, ox + cr, oy + cr], start=a0, end=a1, fill=LINE, width=4)


def draw_eyes_on_rect(draw, cx, cy, h):
    """Draw eyes inside rectangular head with iris/pupil/highlight."""
    sep   = int(h * 0.30)
    er_x  = int(h * 0.16)
    er_y  = int(h * 0.12)
    eye_y = cy + int(h * 0.04)
    for ex in [cx - sep // 2, cx + sep // 2]:
        draw.ellipse([ex - er_x, eye_y - er_y, ex + er_x, eye_y + er_y], fill=EYE_W)
        ir = int(er_x * 0.60)
        draw.ellipse([ex - ir, eye_y - min(ir, er_y - 2),
                      ex + ir, eye_y + min(ir, er_y - 2)], fill=IRIS)
        draw.ellipse([ex - int(ir * 0.5), eye_y - int(ir * 0.5),
                      ex + int(ir * 0.5), eye_y + int(ir * 0.5)], fill=PUPIL)
        # Upper-right highlight (Cosmo DNA: opposite of Luma's upper-left)
        draw.ellipse([ex + int(ir * 0.10), eye_y - int(er_y * 0.50),
                      ex + int(ir * 0.10) + 6, eye_y - int(er_y * 0.50) + 6],
                     fill=EYE_HL)
        draw.ellipse([ex - er_x, eye_y - er_y, ex + er_x, eye_y + er_y],
                     outline=LINE, width=3)


def draw_hair_cosmo(draw, cx, head_top_y, h):
    """Minimal flat hair (barely adds height in silhouette — cosmo spec)."""
    hw = int(h * 0.86 / 2)
    hair_top = head_top_y - int(h * 0.06)
    # Hair fill (flat cap shape)
    draw.rectangle([cx - hw + 4, hair_top, cx + hw - 4, head_top_y + 4], fill=HAIR)
    # Slight cowlick at right
    draw.ellipse([cx + int(hw * 0.55), hair_top - int(h * 0.04),
                  cx + int(hw * 0.95), hair_top + int(h * 0.07)], fill=HAIR)
    # Hair highlight
    draw.arc([cx - int(hw * 0.4), hair_top,
              cx + int(hw * 0.4), hair_top + int(h * 0.12)],
             start=200, end=340, fill=HAIR_HL, width=2)


# ── FRONT VIEW ────────────────────────────────────────────────────────────────

def render_front(draw, cx, base_y):
    S = SCALE
    h = int(hu() * S)
    top_y   = base_y - int(CHAR_DRAW_H * S)
    head_cy = top_y + h
    head_top_y = head_cy - int(h * 0.50)
    hw = int(h * 0.86 / 2)

    # Hair
    draw_hair_cosmo(draw, cx, head_top_y, h)
    # Head (rectangular)
    draw_head_rect(draw, cx, head_cy, h)
    # Eyes
    draw_eyes_on_rect(draw, cx, head_cy, h)
    # Nose
    draw.arc([cx - int(h * 0.05), head_cy + int(h * 0.14),
              cx + int(h * 0.05), head_cy + int(h * 0.23)],
             start=135, end=305, fill=LINE, width=3)
    # Mouth (slight contained smile — Cosmo is reserved)
    draw.arc([cx - int(h * 0.15), head_cy + int(h * 0.26),
              cx + int(h * 0.15), head_cy + int(h * 0.40)],
             start=15, end=165, fill=LINE, width=3)
    # Brows (horizontal/slightly arch — analytical, not expressive)
    brow_y = head_cy - int(h * 0.10)
    for bx in [cx - int(h * 0.27), cx + int(h * 0.08)]:
        draw.line([bx, brow_y, bx + int(h * 0.22), brow_y - int(h * 0.02)],
                  fill=HAIR, width=3)
    # Glasses (over eyes)
    draw_glasses(draw, cx, head_cy + int(h * 0.04), h)

    # Neck
    neck_top = head_cy + int(h * 0.50)
    neck_bot = neck_top + int(h * 0.14)
    neck_w   = int(h * 0.11)
    draw.rectangle([cx - neck_w, neck_top, cx + neck_w, neck_bot], fill=SKIN, outline=LINE)

    # Torso (striped shirt, slim torso — Cosmo is taller/narrower)
    torso_top = neck_bot
    torso_bot = top_y + int(h * 2.40)
    torso_w   = int(h * 0.37)
    draw_stripe_shirt(draw, cx, torso_top, torso_bot, torso_w * 2)
    draw.rectangle([cx - torso_w, torso_top, cx + torso_w, torso_bot],
                   outline=LINE, width=3)
    # Belt
    belt_y = torso_bot - int(h * 0.14)
    draw.rectangle([cx - torso_w, belt_y, cx + torso_w, belt_y + int(h * 0.07)],
                   fill=GLASS_FRAME, outline=LINE, width=2)
    # Belt buckle
    bkl = int(h * 0.06)
    draw.rectangle([cx - bkl, belt_y + 2, cx + bkl, belt_y + int(h * 0.07) - 2],
                   fill=SKIN_SH, outline=LINE, width=2)

    # Arms (slim, held close to body)
    arm_w  = int(h * 0.11)
    arm_h  = int(h * 0.52)
    arm_top = torso_top + int(h * 0.06)
    # Left arm (with notebook tucked)
    draw.rectangle([cx - torso_w - arm_w, arm_top,
                    cx - torso_w, arm_top + arm_h], fill=STRIPE_A, outline=LINE, width=3)
    hand_r = int(h * 0.09)
    draw.ellipse([cx - torso_w - arm_w - hand_r // 2, arm_top + arm_h - hand_r,
                  cx - torso_w - arm_w // 2 + hand_r, arm_top + arm_h + hand_r],
                 fill=SKIN, outline=LINE, width=3)
    # Notebook (tucked under left arm, visible as cerulean slab)
    nb_x0 = cx - torso_w - arm_w - int(h * 0.22)
    nb_y0 = arm_top + int(h * 0.18)
    nb_x1 = cx - torso_w + int(h * 0.05)
    nb_y1 = nb_y0 + int(h * 0.28)
    draw.rectangle([nb_x0, nb_y0, nb_x1, nb_y1], fill=NOTEBOOK, outline=LINE, width=3)
    # Notebook spine
    draw.rectangle([nb_x0, nb_y0, nb_x0 + int(h * 0.06), nb_y1],
                   fill=STRIPE_A_SH, outline=LINE, width=2)
    # Right arm
    draw.rectangle([cx + torso_w, arm_top,
                    cx + torso_w + arm_w, arm_top + arm_h], fill=STRIPE_B, outline=LINE, width=3)
    draw.ellipse([cx + torso_w + arm_w // 2 - hand_r, arm_top + arm_h - hand_r,
                  cx + torso_w + arm_w // 2 + hand_r, arm_top + arm_h + hand_r],
                 fill=SKIN, outline=LINE, width=3)

    # Pants (slim chinos)
    pants_top = torso_bot
    pants_bot = top_y + int(h * 3.20)
    leg_w     = int(h * 0.16)
    gap       = int(h * 0.03)
    for side in [-1, 1]:
        lx0 = cx + side * gap
        lx1 = cx + side * (gap + leg_w * 2)
        if side < 0:
            lx0, lx1 = lx1, lx0
        draw.rectangle([lx0, pants_top, lx1, pants_bot], fill=PANTS, outline=LINE, width=3)
        # Center crease line
        lmid = (lx0 + lx1) // 2
        draw.line([lmid, pants_top + int(h * 0.06), lmid, pants_bot],
                  fill=PANTS_SH, width=2)

    # Shoes (low-profile)
    shoe_y0 = pants_bot
    shoe_w  = int(h * 0.24)
    shoe_h  = int(h * 0.14)
    sole_h  = int(h * 0.06)
    for side in [-1, 1]:
        sx = cx + side * (gap + leg_w + int(h * 0.06))
        draw.ellipse([sx - shoe_w + 2, shoe_y0 + shoe_h - sole_h // 2,
                      sx + shoe_w - 2, shoe_y0 + shoe_h + sole_h], fill=SHOE_SOLE)
        draw.ellipse([sx - shoe_w + 4, shoe_y0 - int(h * 0.03),
                      sx + shoe_w - 4, shoe_y0 + shoe_h], fill=SHOE, outline=LINE, width=3)
        # Lace dots
        for li in range(3):
            ly = shoe_y0 + li * 3 + 2
            draw.line([sx - int(shoe_w * 0.3), ly, sx + int(shoe_w * 0.3), ly],
                      fill=PANTS_SH, width=1)

    # Ground shadow
    sh_y = shoe_y0 + shoe_h + sole_h
    draw.ellipse([cx - int(h * 0.60), sh_y, cx + int(h * 0.60), sh_y + int(h * 0.07)],
                 fill=SHADOW_COL)


# ── 3/4 VIEW ──────────────────────────────────────────────────────────────────

def render_three_quarter(draw, cx, base_y):
    S = SCALE
    h = int(hu() * S)
    top_y   = base_y - int(CHAR_DRAW_H * S)
    head_cy = top_y + h
    head_top_y = head_cy - int(h * 0.50)
    hw = int(h * 0.86 / 2)

    # Foreshortened head (still rect, slightly narrower)
    hw34 = int(hw * 0.80)
    hh   = int(h * 0.50)
    cr   = int(h * 0.12)
    draw.rectangle([cx - hw34 + cr, head_cy - hh, cx + hw34 - cr, head_cy + hh], fill=SKIN)
    draw.rectangle([cx - hw34, head_cy - hh + cr, cx + hw34, head_cy + hh - cr], fill=SKIN)
    for (ox, oy) in [(cx - hw34 + cr, head_cy - hh + cr), (cx + hw34 - cr, head_cy - hh + cr),
                     (cx - hw34 + cr, head_cy + hh - cr), (cx + hw34 - cr, head_cy + hh - cr)]:
        draw.ellipse([ox - cr, oy - cr, ox + cr, oy + cr], fill=SKIN)
    # Ear on right side (visible in 3/4)
    ear_x = cx + hw34 - int(h * 0.02)
    ear_r = int(h * 0.10)
    draw.ellipse([ear_x - ear_r // 2, head_cy - ear_r,
                  ear_x + ear_r, head_cy + ear_r], fill=SKIN, outline=LINE, width=3)
    # Outline
    draw.rectangle([cx - hw34 + cr, head_cy - hh, cx + hw34 - cr, head_cy - hh], fill=None)
    draw.line([cx - hw34 + cr, head_cy - hh, cx + hw34 - cr, head_cy - hh], fill=LINE, width=4)
    draw.line([cx - hw34 + cr, head_cy + hh, cx + hw34 - cr, head_cy + hh], fill=LINE, width=4)
    draw.line([cx - hw34, head_cy - hh + cr, cx - hw34, head_cy + hh - cr], fill=LINE, width=4)
    draw.line([cx + hw34, head_cy - hh + cr, cx + hw34, head_cy + hh - cr], fill=LINE, width=4)
    for (ox, oy, a0, a1) in [(cx - hw34 + cr, head_cy - hh + cr, 180, 270),
                               (cx + hw34 - cr, head_cy - hh + cr, 270, 360),
                               (cx - hw34 + cr, head_cy + hh - cr, 90, 180),
                               (cx + hw34 - cr, head_cy + hh - cr, 0, 90)]:
        draw.arc([ox - cr, oy - cr, ox + cr, oy + cr], start=a0, end=a1, fill=LINE, width=4)

    # Hair
    hair_top = head_cy - hh - int(h * 0.06)
    draw.rectangle([cx - hw34 + 4, hair_top, cx + hw34 - 4, head_cy - hh + 4], fill=HAIR)
    draw.ellipse([cx + int(hw34 * 0.50), hair_top - int(h * 0.04),
                  cx + int(hw34 * 0.90), hair_top + int(h * 0.07)], fill=HAIR)

    # 3/4 eyes (asymmetric: L eye slightly occluded)
    eye_y  = head_cy + int(h * 0.04)
    r_ex   = cx + int(hw34 * 0.18)
    l_ex   = cx - int(hw34 * 0.32)
    for (ex, visible) in [(l_ex, 0.7), (r_ex, 1.0)]:
        er_x = int(h * 0.14 * visible)
        er_y = int(h * 0.11)
        draw.ellipse([ex - er_x, eye_y - er_y, ex + er_x, eye_y + er_y], fill=EYE_W)
        ir = int(er_x * 0.65)
        draw.ellipse([ex - ir, eye_y - min(ir, er_y - 2),
                      ex + ir, eye_y + min(ir, er_y - 2)], fill=IRIS)
        draw.ellipse([ex - int(ir * 0.5), eye_y - int(ir * 0.5),
                      ex + int(ir * 0.5), eye_y + int(ir * 0.5)], fill=PUPIL)
        draw.ellipse([ex - er_x, eye_y - er_y, ex + er_x, eye_y + er_y], outline=LINE, width=3)
    # Nose (3/4 — shifted right)
    draw.arc([cx, head_cy + int(h * 0.14), cx + int(h * 0.12), head_cy + int(h * 0.24)],
             start=135, end=305, fill=LINE, width=3)
    # Mouth
    draw.arc([cx - int(h * 0.06), head_cy + int(h * 0.26),
              cx + int(h * 0.22), head_cy + int(h * 0.40)],
             start=15, end=165, fill=LINE, width=3)
    # Glasses (3/4 — right lens prominent)
    lens_rx = int(h * 0.17)
    lens_ry = int(h * 0.12)
    draw.ellipse([r_ex - lens_rx, eye_y - lens_ry, r_ex + lens_rx, eye_y + lens_ry],
                 fill=GLASS_LENS, outline=GLASS_FRAME, width=5)
    draw.arc([r_ex - lens_rx + 3, eye_y - lens_ry + 3, r_ex + lens_rx - 3, eye_y + lens_ry - 3],
             start=200, end=340, fill=GLASS_GLARE, width=3)
    lens_lx_small = int(lens_rx * 0.55)
    draw.ellipse([l_ex - lens_lx_small, eye_y - lens_ry,
                  l_ex + lens_lx_small, eye_y + lens_ry],
                 fill=GLASS_LENS, outline=GLASS_FRAME, width=5)
    # Bridge
    draw.line([l_ex + lens_lx_small, eye_y, r_ex - lens_rx, eye_y],
              fill=GLASS_FRAME, width=4)

    # Neck
    neck_top = head_cy + int(h * 0.50)
    neck_bot = neck_top + int(h * 0.14)
    draw.rectangle([cx - int(h * 0.09), neck_top, cx + int(h * 0.09), neck_bot],
                   fill=SKIN, outline=LINE, width=3)

    # Torso (3/4 — near shoulder wider)
    torso_top = neck_bot
    torso_bot = top_y + int(h * 2.40)
    torso_near_w = int(h * 0.38)
    torso_far_w  = int(h * 0.26)
    draw_stripe_shirt(draw, cx + int(h * 0.08), torso_top, torso_bot,
                      (torso_near_w + torso_far_w))
    torso_pts = [(cx - torso_far_w, torso_top), (cx + torso_near_w, torso_top),
                 (cx + torso_near_w, torso_bot), (cx - torso_far_w, torso_bot)]
    draw.polygon(torso_pts, outline=LINE, width=3)
    # Belt
    belt_y = torso_bot - int(h * 0.14)
    draw.rectangle([cx - torso_far_w, belt_y, cx + torso_near_w, belt_y + int(h * 0.07)],
                   fill=GLASS_FRAME, outline=LINE, width=2)

    # Far arm (partially behind torso)
    draw.rectangle([cx - torso_far_w - int(h * 0.06), torso_top + int(h * 0.06),
                    cx - torso_far_w + int(h * 0.03), torso_top + int(h * 0.48)],
                   fill=STRIPE_B, outline=LINE, width=3)
    # Near arm + notebook
    arm_right_x0 = cx + torso_near_w
    arm_right_x1 = arm_right_x0 + int(h * 0.11)
    draw.rectangle([arm_right_x0, torso_top + int(h * 0.06),
                    arm_right_x1, torso_top + int(h * 0.54)], fill=STRIPE_A, outline=LINE, width=3)
    draw.ellipse([arm_right_x0 + int(h * 0.01), torso_top + int(h * 0.46),
                  arm_right_x1 + int(h * 0.06), torso_top + int(h * 0.58)],
                 fill=SKIN, outline=LINE, width=3)

    # Pants (3/4)
    pants_top = torso_bot
    pants_bot = top_y + int(h * 3.20)
    for (lx0, lx1) in [(cx - torso_far_w - int(h * 0.02), cx + int(h * 0.06)),
                        (cx + int(h * 0.06), cx + int(h * 0.38))]:
        draw.rectangle([lx0, pants_top, lx1, pants_bot], fill=PANTS, outline=LINE, width=3)
        # crease
        mid = (lx0 + lx1) // 2
        draw.line([mid, pants_top + int(h * 0.06), mid, pants_bot], fill=PANTS_SH, width=2)

    # Shoes (3/4 stagger)
    shoe_y0 = pants_bot
    for (side, offset) in [(-1, int(h * 0.06)), (1, -int(h * 0.04))]:
        sx = cx + side * int(h * 0.18) + offset
        shoe_w = int(h * 0.20)
        shoe_h = int(h * 0.13)
        sole_h = int(h * 0.06)
        draw.ellipse([sx - shoe_w + 2, shoe_y0 + shoe_h - sole_h // 2,
                      sx + shoe_w - 2, shoe_y0 + shoe_h + sole_h], fill=SHOE_SOLE)
        draw.ellipse([sx - shoe_w + 4, shoe_y0 - 2, sx + shoe_w - 4, shoe_y0 + shoe_h],
                     fill=SHOE, outline=LINE, width=3)

    # Ground shadow
    sh_y = shoe_y0 + int(h * 0.19)
    draw.ellipse([cx - int(h * 0.60), sh_y, cx + int(h * 0.60), sh_y + int(h * 0.07)],
                 fill=SHADOW_COL)


# ── SIDE VIEW ─────────────────────────────────────────────────────────────────
# v002 FIX: proper 3D depth (foreshortened profile, depth cues, sole visible)

def render_side(draw, cx, base_y):
    S = SCALE
    h = int(hu() * S)
    top_y   = base_y - int(CHAR_DRAW_H * S)
    head_cy = top_y + h

    # Side head — profile (narrower: width = depth of head ≈ 0.72x)
    hw_side = int(h * 0.86 / 2 * 0.72)
    hh      = int(h * 0.50)
    cr      = int(h * 0.10)
    draw.rectangle([cx - hw_side + cr, head_cy - hh, cx + hw_side - cr, head_cy + hh], fill=SKIN)
    draw.rectangle([cx - hw_side, head_cy - hh + cr, cx + hw_side, head_cy + hh - cr], fill=SKIN)
    for (ox, oy) in [(cx - hw_side + cr, head_cy - hh + cr), (cx + hw_side - cr, head_cy - hh + cr),
                     (cx - hw_side + cr, head_cy + hh - cr), (cx + hw_side - cr, head_cy + hh - cr)]:
        draw.ellipse([ox - cr, oy - cr, ox + cr, oy + cr], fill=SKIN)
    draw.line([cx - hw_side + cr, head_cy - hh, cx + hw_side - cr, head_cy - hh], fill=LINE, width=4)
    draw.line([cx - hw_side + cr, head_cy + hh, cx + hw_side - cr, head_cy + hh], fill=LINE, width=4)
    draw.line([cx - hw_side, head_cy - hh + cr, cx - hw_side, head_cy + hh - cr], fill=LINE, width=4)
    draw.line([cx + hw_side, head_cy - hh + cr, cx + hw_side, head_cy + hh - cr], fill=LINE, width=4)
    for (ox, oy, a0, a1) in [(cx - hw_side + cr, head_cy - hh + cr, 180, 270),
                               (cx + hw_side - cr, head_cy - hh + cr, 270, 360),
                               (cx - hw_side + cr, head_cy + hh - cr, 90, 180),
                               (cx + hw_side - cr, head_cy + hh - cr, 0, 90)]:
        draw.arc([ox - cr, oy - cr, ox + cr, oy + cr], start=a0, end=a1, fill=LINE, width=4)

    # Ear (side view — prominent)
    ear_x = cx + hw_side - int(h * 0.03)
    ear_r = int(h * 0.11)
    draw.ellipse([ear_x - ear_r // 2, head_cy - ear_r,
                  ear_x + ear_r, head_cy + ear_r], fill=SKIN, outline=LINE, width=3)

    # Hair (side silhouette — flat top, slight rear bump)
    hair_top = head_cy - hh - int(h * 0.06)
    draw.rectangle([cx - hw_side + 4, hair_top, cx + hw_side - 4, head_cy - hh + 4], fill=HAIR)
    # Side hair rear bump
    draw.ellipse([cx - hw_side - int(h * 0.08), head_cy - hh - int(h * 0.03),
                  cx - hw_side + int(h * 0.05), head_cy - hh + int(h * 0.14)], fill=HAIR)

    # Side profile features (nose, mouth — visible from side)
    # Nose (slight bump on front face)
    nose_x = cx + hw_side - int(h * 0.04)
    draw.arc([nose_x - int(h * 0.08), head_cy + int(h * 0.10),
              nose_x + int(h * 0.12), head_cy + int(h * 0.24)],
             start=270, end=60, fill=SKIN_SH, width=3)
    draw.arc([nose_x - int(h * 0.08), head_cy + int(h * 0.10),
              nose_x + int(h * 0.12), head_cy + int(h * 0.24)],
             start=300, end=30, fill=LINE, width=3)
    # Mouth
    draw.arc([nose_x - int(h * 0.03), head_cy + int(h * 0.30),
              nose_x + int(h * 0.10), head_cy + int(h * 0.42)],
             start=290, end=10, fill=LINE, width=3)
    # Eye (side — partial, one eye visible through lens)
    eye_x = cx + int(hw_side * 0.30)
    eye_y = head_cy + int(h * 0.04)
    lens_rx = int(h * 0.16)
    lens_ry = int(h * 0.12)
    draw.ellipse([eye_x - int(lens_rx * 0.60), eye_y - lens_ry,
                  eye_x + int(lens_rx * 0.50), eye_y + lens_ry],
                 fill=GLASS_LENS, outline=GLASS_FRAME, width=5)
    # Ear of glasses temple arm extending behind head
    draw.line([eye_x - int(lens_rx * 0.55), eye_y,
               cx - hw_side + int(h * 0.10), eye_y - int(h * 0.06)],
              fill=GLASS_FRAME, width=4)

    # Neck
    neck_top = head_cy + int(h * 0.50)
    neck_bot = neck_top + int(h * 0.14)
    neck_depth = int(h * 0.08)
    draw.rectangle([cx - neck_depth, neck_top, cx + neck_depth, neck_bot],
                   fill=SKIN, outline=LINE, width=3)

    # Torso (side — shows depth, shoulder foreshortened)
    torso_top = neck_bot
    torso_bot = top_y + int(h * 2.40)
    torso_depth = int(h * 0.28)
    # Draw side-visible torso as narrow rectangle (depth dimension)
    draw_stripe_shirt(draw, cx, torso_top, torso_bot, torso_depth * 2)
    # Shoulder shape (front edge rounded, back edge straight)
    shoulder_pts = [
        (cx - int(torso_depth * 0.6), torso_top),
        (cx + torso_depth,            torso_top),
        (cx + torso_depth,            torso_bot),
        (cx - int(torso_depth * 0.6), torso_bot),
    ]
    draw.polygon(shoulder_pts, outline=LINE, width=3)
    # Belt (side visible)
    belt_y = torso_bot - int(h * 0.14)
    draw.rectangle([cx - int(torso_depth * 0.6), belt_y,
                    cx + torso_depth, belt_y + int(h * 0.07)],
                   fill=GLASS_FRAME, outline=LINE, width=2)
    # Shoulder depth shadow
    draw.rectangle([cx + int(torso_depth * 0.70), torso_top,
                    cx + torso_depth, torso_bot], fill=STRIPE_A_SH)

    # Arms (side — front arm visible, back arm partially visible)
    arm_w  = int(h * 0.10)
    arm_h  = int(h * 0.52)
    arm_depth = int(h * 0.12)
    # Front arm (near side)
    draw.rectangle([cx - int(torso_depth * 0.60) - arm_depth, torso_top + int(h * 0.06),
                    cx - int(torso_depth * 0.60), torso_top + int(h * 0.06) + arm_h],
                   fill=STRIPE_B, outline=LINE, width=3)
    draw.ellipse([cx - int(torso_depth * 0.60) - arm_depth - int(h * 0.03),
                  torso_top + int(h * 0.06) + arm_h - int(h * 0.05),
                  cx - int(torso_depth * 0.60) + int(h * 0.04),
                  torso_top + int(h * 0.06) + arm_h + int(h * 0.09)],
                 fill=SKIN, outline=LINE, width=3)
    # Notebook tuck (visible from side, edge-on)
    nb_edge_x = cx - int(torso_depth * 0.60) - arm_depth - int(h * 0.04)
    nb_y0 = torso_top + int(h * 0.20)
    nb_y1 = nb_y0 + int(h * 0.28)
    draw.rectangle([nb_edge_x - int(h * 0.04), nb_y0,
                    nb_edge_x + int(h * 0.02), nb_y1],
                   fill=NOTEBOOK, outline=LINE, width=3)

    # Pants (side — shows slim profile and crease)
    pants_top = torso_bot
    pants_bot = top_y + int(h * 3.20)
    draw.rectangle([cx - int(h * 0.15), pants_top,
                    cx + int(h * 0.18), pants_bot], fill=PANTS, outline=LINE, width=3)
    # Crease line (center of visible leg depth)
    draw.line([cx + int(h * 0.02), pants_top + int(h * 0.06),
               cx + int(h * 0.02), pants_bot], fill=PANTS_SH, width=2)

    # Shoes (side — CRITICAL v002 FIX: show sole depth from profile)
    shoe_y0 = pants_bot
    shoe_len = int(h * 0.35)   # longer from side (full foot length visible)
    shoe_h   = int(h * 0.12)
    sole_h   = int(h * 0.08)
    # Sole (visible from side as thick band)
    draw.rectangle([cx - int(h * 0.12), shoe_y0 + shoe_h,
                    cx + shoe_len - int(h * 0.08), shoe_y0 + shoe_h + sole_h],
                   fill=SHOE_SOLE, outline=LINE, width=3)
    # Upper (shoe profile)
    draw.ellipse([cx - int(h * 0.12), shoe_y0 - int(h * 0.02),
                  cx + shoe_len - int(h * 0.08), shoe_y0 + shoe_h],
                 fill=SHOE, outline=LINE, width=3)
    # Back foot (partially visible)
    draw.ellipse([cx - int(h * 0.30), shoe_y0,
                  cx + int(h * 0.08), shoe_y0 + shoe_h * 2 // 3],
                 fill=SHOE, outline=LINE, width=2)
    # Lace details (side)
    for li in range(3):
        lx_s = cx + int(h * 0.05) + li * int(h * 0.07)
        draw.line([lx_s, shoe_y0 + 2, lx_s, shoe_y0 + shoe_h - 2], fill=PANTS_SH, width=2)

    # Ground shadow
    sh_y = shoe_y0 + shoe_h + sole_h
    draw.ellipse([cx - int(h * 0.55), sh_y, cx + int(h * 0.55), sh_y + int(h * 0.07)],
                 fill=SHADOW_COL)


# ── BACK VIEW ─────────────────────────────────────────────────────────────────

def render_back(draw, cx, base_y):
    S = SCALE
    h = int(hu() * S)
    top_y   = base_y - int(CHAR_DRAW_H * S)
    head_cy = top_y + h
    hw      = int(h * 0.86 / 2)
    hh      = int(h * 0.50)
    cr      = int(h * 0.12)

    # Back of head — same rect shape
    draw.rectangle([cx - hw + cr, head_cy - hh, cx + hw - cr, head_cy + hh], fill=SKIN)
    draw.rectangle([cx - hw, head_cy - hh + cr, cx + hw, head_cy + hh - cr], fill=SKIN)
    for (ox, oy) in [(cx - hw + cr, head_cy - hh + cr), (cx + hw - cr, head_cy - hh + cr),
                     (cx - hw + cr, head_cy + hh - cr), (cx + hw - cr, head_cy + hh - cr)]:
        draw.ellipse([ox - cr, oy - cr, ox + cr, oy + cr], fill=SKIN)
    draw.line([cx - hw + cr, head_cy - hh, cx + hw - cr, head_cy - hh], fill=LINE, width=4)
    draw.line([cx - hw + cr, head_cy + hh, cx + hw - cr, head_cy + hh], fill=LINE, width=4)
    draw.line([cx - hw, head_cy - hh + cr, cx - hw, head_cy + hh - cr], fill=LINE, width=4)
    draw.line([cx + hw, head_cy - hh + cr, cx + hw, head_cy + hh - cr], fill=LINE, width=4)
    for (ox, oy, a0, a1) in [(cx - hw + cr, head_cy - hh + cr, 180, 270),
                               (cx + hw - cr, head_cy - hh + cr, 270, 360),
                               (cx - hw + cr, head_cy + hh - cr, 90, 180),
                               (cx + hw - cr, head_cy + hh - cr, 0, 90)]:
        draw.arc([ox - cr, oy - cr, ox + cr, oy + cr], start=a0, end=a1, fill=LINE, width=4)

    # Hair (back — full cap)
    hair_top = head_cy - hh - int(h * 0.06)
    draw.rectangle([cx - hw + 4, hair_top, cx + hw - 4, head_cy - hh + 4], fill=HAIR)
    draw.ellipse([cx - int(hw * 0.7), hair_top - int(h * 0.03),
                  cx + int(hw * 0.7), hair_top + int(h * 0.10)], fill=HAIR)
    # Neck (back visible)
    neck_top = head_cy + hh
    neck_bot = neck_top + int(h * 0.14)
    draw.rectangle([cx - int(h * 0.11), neck_top, cx + int(h * 0.11), neck_bot],
                   fill=SKIN, outline=LINE, width=3)

    # Glasses temple arms visible at back of ears
    for side in [-1, 1]:
        draw.arc([cx + side * (hw - int(h * 0.02)) - int(h * 0.10),
                  head_cy - int(h * 0.15),
                  cx + side * (hw - int(h * 0.02)) + int(h * 0.10),
                  head_cy + int(h * 0.15)],
                 start=(150 if side < 0 else 30),
                 end=(210 if side < 0 else 90),
                 fill=GLASS_FRAME, width=4)

    # Torso back — striped shirt back panel
    torso_top = neck_bot
    torso_bot = top_y + int(h * 2.40)
    torso_w   = int(h * 0.37)
    draw_stripe_shirt(draw, cx, torso_top, torso_bot, torso_w * 2)
    draw.rectangle([cx - torso_w, torso_top, cx + torso_w, torso_bot],
                   outline=LINE, width=3)
    # Belt back
    belt_y = torso_bot - int(h * 0.14)
    draw.rectangle([cx - torso_w, belt_y, cx + torso_w, belt_y + int(h * 0.07)],
                   fill=GLASS_FRAME, outline=LINE, width=2)

    # Arms (back — like front but mirrored notebook side)
    arm_w  = int(h * 0.11)
    arm_h  = int(h * 0.52)
    arm_top = torso_top + int(h * 0.06)
    # Left arm (back view: notebook on right from our perspective)
    draw.rectangle([cx - torso_w - arm_w, arm_top,
                    cx - torso_w, arm_top + arm_h], fill=STRIPE_B, outline=LINE, width=3)
    draw.ellipse([cx - torso_w - arm_w - int(h * 0.05), arm_top + arm_h - int(h * 0.05),
                  cx - torso_w + int(h * 0.05), arm_top + arm_h + int(h * 0.09)],
                 fill=SKIN, outline=LINE, width=3)
    # Right arm (back view: was notebook arm in front)
    draw.rectangle([cx + torso_w, arm_top,
                    cx + torso_w + arm_w, arm_top + arm_h], fill=STRIPE_A, outline=LINE, width=3)
    draw.ellipse([cx + torso_w + arm_w // 2 - int(h * 0.09), arm_top + arm_h - int(h * 0.05),
                  cx + torso_w + arm_w // 2 + int(h * 0.09), arm_top + arm_h + int(h * 0.09)],
                 fill=SKIN, outline=LINE, width=3)
    # Notebook visible from back at right side
    nb_x0 = cx + torso_w + arm_w // 2 - int(h * 0.04)
    nb_y0 = arm_top + int(h * 0.18)
    nb_x1 = cx + torso_w + arm_w + int(h * 0.22)
    nb_y1 = nb_y0 + int(h * 0.28)
    draw.rectangle([nb_x0, nb_y0, nb_x1, nb_y1], fill=NOTEBOOK, outline=LINE, width=3)
    draw.rectangle([nb_x1 - int(h * 0.06), nb_y0, nb_x1, nb_y1],
                   fill=STRIPE_A_SH, outline=LINE, width=2)

    # Pants (back — crease visible)
    pants_top = torso_bot
    pants_bot = top_y + int(h * 3.20)
    leg_w     = int(h * 0.16)
    gap       = int(h * 0.03)
    for side in [-1, 1]:
        lx0 = cx + side * gap
        lx1 = cx + side * (gap + leg_w * 2)
        if side < 0:
            lx0, lx1 = lx1, lx0
        draw.rectangle([lx0, pants_top, lx1, pants_bot], fill=PANTS, outline=LINE, width=3)
        lmid = (lx0 + lx1) // 2
        draw.line([lmid, pants_top + int(h * 0.06), lmid, pants_bot], fill=PANTS_SH, width=2)

    # Shoes (back)
    shoe_y0 = pants_bot
    shoe_w  = int(h * 0.22)
    shoe_h  = int(h * 0.12)
    sole_h  = int(h * 0.06)
    for side in [-1, 1]:
        sx = cx + side * (gap + leg_w + int(h * 0.04))
        draw.ellipse([sx - shoe_w + 2, shoe_y0 + shoe_h - sole_h // 2,
                      sx + shoe_w - 2, shoe_y0 + shoe_h + sole_h], fill=SHOE_SOLE)
        draw.ellipse([sx - shoe_w + 4, shoe_y0 - 2,
                      sx + shoe_w - 4, shoe_y0 + shoe_h], fill=SHOE, outline=LINE, width=3)
        # Heel detail
        draw.arc([sx - shoe_w + 4, shoe_y0 - 2, sx + shoe_w - 4, shoe_y0 + shoe_h],
                 start=160, end=20, fill=SKIN_SH, width=2)

    # Ground shadow
    sh_y = shoe_y0 + shoe_h + sole_h
    draw.ellipse([cx - int(h * 0.60), sh_y, cx + int(h * 0.60), sh_y + int(h * 0.07)],
                 fill=SHADOW_COL)


# ── BUILD TURNAROUND ──────────────────────────────────────────────────────────

def build_turnaround():
    """Build the 4-view Cosmo turnaround at 2x, then downscale."""
    W_2x = CANVAS_W * SCALE
    H_2x = CANVAS_H * SCALE
    img = Image.new("RGB", (W_2x, H_2x), CANVAS_BG)
    draw = ImageDraw.Draw(img)

    # Try to load fonts
    try:
        font_title = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28 * SCALE)
        font_label = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16 * SCALE)
        font_sub   = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14 * SCALE)
    except Exception:
        font_title = ImageFont.load_default()
        font_label = font_title
        font_sub   = font_title

    # Header
    draw.text((20 * SCALE, 6 * SCALE),
              "COSMO — 4-View Character Turnaround v002  |  Luma & the Glitchkin",
              fill=LINE, font=font_title)
    draw.text((20 * SCALE, 30 * SCALE),
              "Maya Santos / Cycle 25  |  4.0 heads  |  Rectangular head  |  Glasses always present  |  Notebook always tucked  |  v002: side view 3D depth fix",
              fill=(140, 120, 100), font=font_sub)

    # Dividers
    for vi in range(1, N_VIEWS):
        x = vi * VIEW_W * SCALE
        draw.line([x, HEADER_H * SCALE, x, H_2x - LABEL_H * SCALE],
                  fill=(200, 192, 180), width=2)

    # Render each view
    render_funcs = [render_front, render_three_quarter, render_side, render_back]
    for vi, (vname, rfunc) in enumerate(zip(VIEWS, render_funcs)):
        cx     = vi * VIEW_W * SCALE + VIEW_W * SCALE // 2
        base_y = H_2x - LABEL_H * SCALE - int(h * 0.05)  if (h := int(hu() * SCALE)) else 0
        base_y = H_2x - LABEL_H * SCALE - int(int(hu() * SCALE) * 0.05)

        # Panel background tint
        draw.rectangle([vi * VIEW_W * SCALE, HEADER_H * SCALE,
                        (vi + 1) * VIEW_W * SCALE, H_2x - LABEL_H * SCALE],
                       fill=PANEL_BG)
        rfunc(draw, cx, base_y)
        # CRITICAL: refresh draw after any compositing
        draw = ImageDraw.Draw(img)

        # View label
        label_y = H_2x - LABEL_H * SCALE
        draw.rectangle([vi * VIEW_W * SCALE, label_y,
                        (vi + 1) * VIEW_W * SCALE, H_2x], fill=(228, 220, 210))
        bbox = draw.textbbox((0, 0), vname, font=font_label)
        tw = bbox[2] - bbox[0]
        draw.text((cx - tw // 2, label_y + 4 * SCALE), vname, fill=LINE, font=font_label)

    # Scale down from 2x
    out = img.resize((CANVAS_W, CANVAS_H), Image.LANCZOS)
    return out


def main():
    out_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "characters", "main", "turnarounds"
    )
    os.makedirs(out_dir, exist_ok=True)

    img = build_turnaround()
    # Image size rule: ≤ 1280px in both dimensions
    img.thumbnail((1280, 1280), Image.LANCZOS)
    out_path = os.path.join(out_dir, "LTG_CHAR_cosmo_turnaround.png")
    img.save(out_path)
    print(f"Saved: {out_path}")
    print(f"  Size: {img.size[0]}x{img.size[1]}px")
    print("  v002: Side view 3D depth fix (profile head, visible sole, proper arm placement)")


if __name__ == "__main__":
    main()
