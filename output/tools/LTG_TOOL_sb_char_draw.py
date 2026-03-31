#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_sb_char_draw.py — Shared Storyboard Character Drawing Module
"Luma & the Glitchkin" — Diego Vargas, Storyboard Artist — Cycle 51

Reusable pycairo-based character drawing functions for storyboard panels.
All characters are drawn at storyboard scale (50-200px height) with:
  - Organic bezier curves via LTG_TOOL_cairo_primitives
  - Gesture-line-based construction via LTG_TOOL_curve_draw
  - Three-tier line weight system (anchor/structure/detail)
  - Anti-aliased rendering at 2x with LANCZOS downscale

Characters:
  - draw_luma_sb()   — Luma at storyboard scale, configurable pose
  - draw_byte_sb()   — Byte at storyboard scale, configurable expression
  - draw_chip()      — Falling pixel chip prop

Import pattern:
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
    from LTG_TOOL_sb_char_draw import draw_luma_sb, draw_byte_sb, draw_chip

Dependencies: pycairo, numpy, PIL/Pillow, LTG_TOOL_cairo_primitives.
"""

__version__ = "1.0.0"

import math
import os
import sys

# Ensure sibling tool imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import cairo
import numpy as np
from PIL import Image

from LTG_TOOL_cairo_primitives import (
    create_surface, draw_bezier_path, draw_tapered_stroke,
    draw_gradient_fill, draw_wobble_path, draw_smooth_polygon,
    draw_ellipse, to_pil_image, to_pil_rgba, set_color,
    stroke_path, fill_background, flatten_path,
    LINE_WEIGHT_ANCHOR, LINE_WEIGHT_STRUCTURE, LINE_WEIGHT_DETAIL,
    shoulder_offset,
)

# ══════════════════════════════════════════════════════════════════════════════
# Palette constants (canonical)
# ══════════════════════════════════════════════════════════════════════════════

LUMA_HOODIE   = (232, 112, 58)    # canonical orange #E8703A
LUMA_SKIN     = (218, 172, 128)
LUMA_SKIN_SH  = (175, 128, 88)
LUMA_HAIR     = (38, 22, 14)
LUMA_HAIR_HL  = (61, 31, 15)
LUMA_PANTS    = (70, 80, 110)
LUMA_SHOE     = (42, 36, 30)
LINE_COLOR    = (59, 40, 32)
LINE_THIN     = (80, 55, 40)

BYTE_TEAL     = (0, 212, 232)     # ELEC_CYAN
BYTE_DARK     = (8, 40, 50)
BYTE_SCAR     = (232, 0, 152)     # HOT_MAGENTA
ELEC_CYAN     = (0, 212, 232)
HOT_MAGENTA   = (232, 0, 152)
VOID_BLACK    = (10, 10, 20)
DEEP_CYAN     = (0, 155, 175)

COLLAR_COLOR  = (250, 232, 200)
IRIS_BROWN    = (130, 78, 40)

# ══════════════════════════════════════════════════════════════════════════════
# Scale helper — all measurements relative to character height
# ══════════════════════════════════════════════════════════════════════════════

def _scale(value, char_h, ref_h=140):
    """Scale a measurement from reference character height (140px) to actual."""
    return value * char_h / ref_h


# ══════════════════════════════════════════════════════════════════════════════
# LUMA — Storyboard scale drawing
# ══════════════════════════════════════════════════════════════════════════════

def draw_luma_sb(ctx, cx, floor_y, char_h=140, pose="sitting", lean_deg=3.0,
                 expression="assessing", facing="right", seed=1717):
    """Draw Luma at storyboard scale using pycairo.

    Args:
        ctx:        cairo Context to draw on
        cx:         horizontal center of character
        floor_y:    y-coordinate of the floor/ground line
        char_h:     visible character height in pixels (50-200)
        pose:       "sitting" or "standing" (sitting = cross-legged)
        lean_deg:   gesture lean in degrees (positive = toward facing direction)
        expression: "assessing", "alarmed", "happy", "neutral"
        facing:     "right" or "left" — which direction Luma faces
        seed:       RNG seed for hair randomization

    Returns:
        dict with key positions: {head_cx, head_cy, head_r, shoulder_y}
    """
    import random
    rng = random.Random(seed)

    s = lambda v: _scale(v, char_h)
    face_dir = 1 if facing == "right" else -1

    # Head proportions: 37% of visible height
    head_h = int(char_h * 0.37)
    head_r = head_h // 2

    # Gesture lean
    lean_dx = int(s(6) * lean_deg / 3.0) * face_dir

    # Key position anchors
    head_cy = floor_y - int(s(104))
    head_cx = cx + lean_dx

    # ── Legs (sitting cross-legged) ──
    if pose == "sitting":
        leg_w = int(s(62))
        _draw_luma_legs_sitting(ctx, cx, floor_y, leg_w, s, rng)
    else:
        leg_w = int(s(35))
        _draw_luma_legs_standing(ctx, cx, floor_y, char_h, s, face_dir, rng)

    # ── Torso — organic bean shape ──
    torso_top_y = floor_y - int(s(86))
    torso_bot_y = floor_y + int(s(2))
    shoulder_w = int(s(48))
    waist_w = int(s(38))

    _draw_luma_torso(ctx, head_cx, cx, torso_top_y, torso_bot_y,
                     shoulder_w, waist_w, s)

    # ── Arms ──
    if pose == "sitting":
        _draw_luma_arms_sitting(ctx, head_cx, cx, torso_top_y,
                                floor_y, shoulder_w, leg_w, s)
    else:
        _draw_luma_arms_standing(ctx, head_cx, cx, torso_top_y,
                                 floor_y, shoulder_w, s, face_dir)

    # ── Neck ──
    _draw_luma_neck(ctx, head_cx, torso_top_y, head_cy, head_r, s)

    # ── Head ──
    _draw_luma_head(ctx, head_cx, head_cy, head_r)

    # ── Face ──
    _draw_luma_face(ctx, head_cx, head_cy, head_r, expression, face_dir, s)

    # ── Hair (drawn last — overlaps head) ──
    _draw_luma_hair(ctx, head_cx, head_cy, head_r, rng, s)

    return {
        "head_cx": head_cx,
        "head_cy": head_cy,
        "head_r": head_r,
        "shoulder_y": torso_top_y,
    }


def _draw_luma_legs_sitting(ctx, cx, floor_y, leg_w, s, rng):
    """Cross-legged sitting legs."""
    # Build leg shape as smooth curved polygon
    pts = [
        (cx - leg_w, floor_y),
        (cx - leg_w // 2, floor_y - int(s(12))),
        (cx, floor_y - int(s(6))),
        (cx + leg_w // 2, floor_y - int(s(12))),
        (cx + leg_w, floor_y),
        (cx, floor_y + int(s(22))),
    ]
    draw_smooth_polygon(ctx, pts, bulge_frac=0.08)
    set_color(ctx, LUMA_PANTS)
    ctx.fill_preserve()
    stroke_path(ctx, LINE_COLOR, weight_tier="structure")

    # Shoes
    for shoe_x in [cx - leg_w - int(s(4)), cx + leg_w + int(s(4))]:
        draw_ellipse(ctx, shoe_x, floor_y, int(s(10)), int(s(6)))
        set_color(ctx, LUMA_SHOE)
        ctx.fill_preserve()
        stroke_path(ctx, LINE_THIN, weight_tier="detail")


def _draw_luma_legs_standing(ctx, cx, floor_y, char_h, s, face_dir, rng):
    """Standing legs."""
    leg_top_y = floor_y - int(s(52))
    leg_w = int(s(14))
    gap = int(s(6))
    for side in [-1, 1]:
        lx = cx + side * gap
        pts = [
            (lx - leg_w // 2, leg_top_y),
            (lx + leg_w // 2, leg_top_y),
            (lx + int(leg_w * 0.4), floor_y),
            (lx - int(leg_w * 0.4), floor_y),
        ]
        draw_smooth_polygon(ctx, pts, bulge_frac=0.06)
        set_color(ctx, LUMA_PANTS)
        ctx.fill_preserve()
        stroke_path(ctx, LINE_COLOR, weight_tier="structure")

        # Shoe
        draw_ellipse(ctx, lx, floor_y + int(s(3)), int(s(10)), int(s(5)))
        set_color(ctx, LUMA_SHOE)
        ctx.fill_preserve()
        stroke_path(ctx, LINE_THIN, weight_tier="detail")


def _draw_luma_torso(ctx, head_cx, cx, torso_top_y, torso_bot_y,
                     shoulder_w, waist_w, s):
    """Organic bean-shape torso using bezier curves."""
    # Build torso outline as bezier path
    th = torso_bot_y - torso_top_y
    pts = [
        (head_cx - shoulder_w, torso_top_y),
        # left side curves: cubic control points to create organic bulge
        (head_cx - shoulder_w - int(s(4)),
         torso_top_y + th * 0.3,
         cx - waist_w - int(s(2)),
         torso_top_y + th * 0.6,
         cx - waist_w + int(s(2)),
         torso_bot_y),
        # bottom edge
        (cx + waist_w - int(s(2)), torso_bot_y),
        # right side curves
        (cx + waist_w + int(s(2)),
         torso_top_y + th * 0.6,
         head_cx + shoulder_w + int(s(4)),
         torso_top_y + th * 0.3,
         head_cx + shoulder_w,
         torso_top_y),
    ]
    draw_bezier_path(ctx, pts, closed=True)
    set_color(ctx, LUMA_HOODIE)
    ctx.fill_preserve()
    stroke_path(ctx, LINE_COLOR, weight_tier="anchor")

    # Collar V-neck
    ctx.new_path()
    ctx.move_to(head_cx - int(s(14)), torso_top_y + int(s(2)))
    ctx.line_to(head_cx, torso_top_y + int(s(16)))
    ctx.line_to(head_cx + int(s(14)), torso_top_y + int(s(2)))
    set_color(ctx, COLLAR_COLOR)
    ctx.fill_preserve()
    stroke_path(ctx, LINE_THIN, weight_tier="detail")

    # Hoodie hem
    hem_y = torso_bot_y - int(s(4))
    hem_pts = [
        (cx - waist_w + int(s(4)), hem_y),
        (cx, hem_y - int(s(4))),
        (cx + waist_w - int(s(4)), hem_y),
    ]
    ctx.new_path()
    ctx.move_to(hem_pts[0][0], hem_pts[0][1])
    qcx, qcy = hem_pts[1]
    ex, ey = hem_pts[2]
    cx_cur, cy_cur = hem_pts[0]
    c1x = cx_cur + 2/3 * (qcx - cx_cur)
    c1y = cy_cur + 2/3 * (qcy - cy_cur)
    c2x = ex + 2/3 * (qcx - ex)
    c2y = ey + 2/3 * (qcy - ey)
    ctx.curve_to(c1x, c1y, c2x, c2y, ex, ey)
    stroke_path(ctx, LINE_THIN, weight_tier="detail")


def _draw_luma_arms_sitting(ctx, head_cx, cx, torso_top_y,
                            floor_y, shoulder_w, leg_w, s):
    """Arms for sitting pose — crossed loosely in lap."""
    # Left arm
    la_pts = [
        (head_cx - shoulder_w + int(s(6)), torso_top_y + int(s(12))),
        (head_cx - shoulder_w - int(s(8)), torso_top_y + int(s(38))),
        (cx - int(s(10)), floor_y - int(s(28))),
        (cx + int(s(18)), floor_y - int(s(16))),
    ]
    draw_tapered_stroke(ctx, la_pts, _scale(11, 140) * 2, _scale(7, 140) * 2,
                        LUMA_HOODIE, segments=24)

    # Left hand
    lh_x = cx + int(s(18))
    lh_y = floor_y - int(s(16))
    draw_ellipse(ctx, lh_x, lh_y, int(s(8)), int(s(6)))
    set_color(ctx, LUMA_SKIN)
    ctx.fill_preserve()
    stroke_path(ctx, LINE_THIN, weight_tier="detail")

    # Right arm
    ra_pts = [
        (head_cx + shoulder_w - int(s(6)), torso_top_y + int(s(12))),
        (head_cx + shoulder_w + int(s(6)), torso_top_y + int(s(36))),
        (cx + int(s(30)), floor_y - int(s(26))),
        (cx + leg_w - int(s(12)), floor_y - int(s(10))),
    ]
    draw_tapered_stroke(ctx, ra_pts, _scale(11, 140) * 2, _scale(7, 140) * 2,
                        LUMA_HOODIE, segments=24)

    # Right hand
    rh_x = cx + leg_w - int(s(12))
    rh_y = floor_y - int(s(10))
    draw_ellipse(ctx, rh_x, rh_y, int(s(8)), int(s(6)))
    set_color(ctx, LUMA_SKIN)
    ctx.fill_preserve()
    stroke_path(ctx, LINE_THIN, weight_tier="detail")


def _draw_luma_arms_standing(ctx, head_cx, cx, torso_top_y,
                             floor_y, shoulder_w, s, face_dir):
    """Arms for standing pose — hanging with slight gesture."""
    arm_end_y = torso_top_y + int(s(68))
    for side in [-1, 1]:
        sx = head_cx + side * (shoulder_w - int(s(6)))
        elbow_x = sx + side * int(s(8))
        hand_x = sx + side * int(s(4))
        pts = [
            (sx, torso_top_y + int(s(12))),
            (elbow_x, torso_top_y + int(s(38))),
            (hand_x, arm_end_y),
        ]
        draw_tapered_stroke(ctx, pts, _scale(11, 140) * 2, _scale(7, 140) * 2,
                            LUMA_HOODIE, segments=16)
        # Hand
        draw_ellipse(ctx, hand_x, arm_end_y, int(s(8)), int(s(6)))
        set_color(ctx, LUMA_SKIN)
        ctx.fill_preserve()
        stroke_path(ctx, LINE_THIN, weight_tier="detail")


def _draw_luma_neck(ctx, head_cx, torso_top_y, head_cy, head_r, s):
    """Short neck connecting head to torso."""
    nw = int(s(10))
    pts = [
        (head_cx - nw, torso_top_y + int(s(2))),
        (head_cx + nw, torso_top_y + int(s(2))),
        (head_cx + nw - int(s(2)), head_cy + head_r - int(s(2))),
        (head_cx - nw + int(s(2)), head_cy + head_r - int(s(2))),
    ]
    ctx.new_path()
    ctx.move_to(pts[0][0], pts[0][1])
    for p in pts[1:]:
        ctx.line_to(p[0], p[1])
    ctx.close_path()
    set_color(ctx, LUMA_SKIN)
    ctx.fill()


def _draw_luma_head(ctx, head_cx, head_cy, head_r):
    """Head — slightly oval (taller than wide)."""
    draw_ellipse(ctx, head_cx, head_cy, head_r, int(head_r * 1.05))
    set_color(ctx, LUMA_SKIN)
    ctx.fill_preserve()
    stroke_path(ctx, LINE_COLOR, weight_tier="anchor")


def _draw_luma_face(ctx, head_cx, head_cy, head_r, expression, face_dir, s):
    """Face features — eyes, brows, nose, mouth."""
    # Eye size: 30-35% of head width
    eye_size = int(head_r * 0.65)
    eye_h = int(eye_size * 0.65)

    # Primary eye (facing direction)
    pe_cx = head_cx + int(head_r * 0.28) * face_dir
    pe_cy = head_cy - int(head_r * 0.08)

    # Eye white
    draw_ellipse(ctx, pe_cx, pe_cy, eye_size // 2, eye_h // 2)
    set_color(ctx, (245, 238, 228))
    ctx.fill_preserve()
    stroke_path(ctx, LINE_COLOR, weight_tier="structure")

    # Iris
    ir_r = int(eye_size * 0.35)
    ir_cx = pe_cx + int(ir_r * 0.30) * face_dir
    draw_ellipse(ctx, ir_cx, pe_cy, ir_r, ir_r)
    set_color(ctx, IRIS_BROWN)
    ctx.fill()

    # Pupil
    pr = int(ir_r * 0.55)
    draw_ellipse(ctx, ir_cx, pe_cy, pr, pr)
    set_color(ctx, VOID_BLACK)
    ctx.fill()

    # Highlight
    hl_r = max(2, int(ir_r * 0.25))
    draw_ellipse(ctx, ir_cx - int(ir_r * 0.25), pe_cy - int(ir_r * 0.3), hl_r, hl_r)
    set_color(ctx, (255, 255, 255))
    ctx.fill()

    # Upper eyelid
    lid_drop = 2 if expression == "assessing" else 0
    ctx.new_path()
    ctx.move_to(pe_cx - eye_size // 2 - 1, pe_cy - 1)
    qcx = pe_cx
    qcy = pe_cy - eye_h // 2 + lid_drop
    ex = pe_cx + eye_size // 2 + 1
    ey = pe_cy - 1
    c1x = (pe_cx - eye_size // 2 - 1) + 2/3 * (qcx - (pe_cx - eye_size // 2 - 1))
    c1y = (pe_cy - 1) + 2/3 * (qcy - (pe_cy - 1))
    c2x = ex + 2/3 * (qcx - ex)
    c2y = ey + 2/3 * (qcy - ey)
    ctx.curve_to(c1x, c1y, c2x, c2y, ex, ey)
    stroke_path(ctx, LINE_COLOR, weight_tier="structure")

    # Secondary eye (partially visible at 3/4)
    se_cx = head_cx - int(head_r * 0.18) * face_dir
    se_cy = head_cy - int(head_r * 0.06)
    se_size = int(eye_size * 0.65)
    se_h = int(eye_h * 0.65)

    draw_ellipse(ctx, se_cx, se_cy, se_size // 2, se_h // 2)
    set_color(ctx, (245, 238, 228))
    ctx.fill_preserve()
    stroke_path(ctx, LINE_COLOR, weight_tier="detail")

    # Secondary iris
    sir_r = int(se_size * 0.35)
    draw_ellipse(ctx, se_cx, se_cy, sir_r, sir_r)
    set_color(ctx, IRIS_BROWN)
    ctx.fill()
    # Secondary pupil
    spr = sir_r - 2
    if spr > 0:
        draw_ellipse(ctx, se_cx, se_cy, spr, spr)
        set_color(ctx, VOID_BLACK)
        ctx.fill()

    # Brows
    brow_thick = max(2, int(s(3)))
    # Primary brow
    pb_outer_drop = -4 if expression == "assessing" else -6
    ctx.new_path()
    ctx.move_to(pe_cx - eye_size // 2, pe_cy - eye_h // 2 - int(s(6)))
    qcx2 = pe_cx
    qcy2 = pe_cy - eye_h // 2 - int(s(10))
    ex2 = pe_cx + eye_size // 2 + int(s(2))
    ey2 = pe_cy - eye_h // 2 + pb_outer_drop
    c1x2 = (pe_cx - eye_size // 2) + 2/3 * (qcx2 - (pe_cx - eye_size // 2))
    c1y2 = (pe_cy - eye_h // 2 - int(s(6))) + 2/3 * (qcy2 - (pe_cy - eye_h // 2 - int(s(6))))
    c2x2 = ex2 + 2/3 * (qcx2 - ex2)
    c2y2 = ey2 + 2/3 * (qcy2 - ey2)
    ctx.curve_to(c1x2, c1y2, c2x2, c2y2, ex2, ey2)
    ctx.set_line_width(brow_thick)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    set_color(ctx, (42, 22, 10))
    ctx.stroke()

    # Secondary brow
    ctx.new_path()
    ctx.move_to(se_cx - se_size // 2 - 1, se_cy - se_h // 2 - int(s(5)))
    qcx3 = se_cx
    qcy3 = se_cy - se_h // 2 - int(s(8))
    ex3 = se_cx + se_size // 2
    ey3 = se_cy - se_h // 2 - int(s(4))
    c1x3 = (se_cx - se_size // 2 - 1) + 2/3 * (qcx3 - (se_cx - se_size // 2 - 1))
    c1y3 = (se_cy - se_h // 2 - int(s(5))) + 2/3 * (qcy3 - (se_cy - se_h // 2 - int(s(5))))
    c2x3 = ex3 + 2/3 * (qcx3 - ex3)
    c2y3 = ey3 + 2/3 * (qcy3 - ey3)
    ctx.curve_to(c1x3, c1y3, c2x3, c2y3, ex3, ey3)
    ctx.set_line_width(max(1, brow_thick - 1))
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    set_color(ctx, (42, 22, 10))
    ctx.stroke()

    # Nose
    nose_x = head_cx + int(s(2)) * face_dir
    ctx.new_path()
    ctx.move_to(nose_x, head_cy + int(head_r * 0.10))
    ctx.curve_to(
        nose_x + int(s(3)) * face_dir, head_cy + int(head_r * 0.20),
        nose_x + int(s(4)) * face_dir, head_cy + int(head_r * 0.25),
        nose_x, head_cy + int(head_r * 0.35)
    )
    stroke_path(ctx, LUMA_SKIN_SH, weight_tier="detail")

    # Mouth
    mouth_y = head_cy + int(head_r * 0.52)
    ctx.new_path()
    ctx.move_to(head_cx - int(s(8)), mouth_y + 1)
    qmx = head_cx + int(s(2))
    qmy = mouth_y - 2
    emx = head_cx + int(s(10))
    emy = mouth_y
    c1mx = (head_cx - int(s(8))) + 2/3 * (qmx - (head_cx - int(s(8))))
    c1my = (mouth_y + 1) + 2/3 * (qmy - (mouth_y + 1))
    c2mx = emx + 2/3 * (qmx - emx)
    c2my = emy + 2/3 * (qmy - emy)
    ctx.curve_to(c1mx, c1my, c2mx, c2my, emx, emy)
    ctx.set_line_width(max(1, int(s(2))))
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    set_color(ctx, (120, 72, 44))
    ctx.stroke()


def _draw_luma_hair(ctx, head_cx, head_cy, head_r, rng, s):
    """Asymmetric messy hair with volume — key silhouette element."""
    # Build hair mass as wobble polygon for organic quality
    hair_pts = []
    for ha in range(180, 540, 8):
        angle = math.radians(ha)
        base_r = head_r + int(s(14))
        # Left side bigger (her characteristic messy side)
        if 200 < ha < 320:
            base_r += rng.randint(int(s(4)), int(s(12)))
        elif 320 < ha < 400:
            base_r += rng.randint(int(s(2)), int(s(8)))
        else:
            base_r += rng.randint(0, int(s(6)))
        hx = head_cx + int(base_r * math.cos(angle))
        hy = head_cy + int(base_r * 0.95 * math.sin(angle))
        if hy < head_cy + int(head_r * 0.45):
            hair_pts.append((hx, hy))

    # Close along face edge
    hair_pts.append((head_cx + int(head_r * 0.9), head_cy + int(head_r * 0.4)))
    hair_pts.append((head_cx - int(head_r * 0.7), head_cy + int(head_r * 0.4)))

    if len(hair_pts) > 3:
        # Use wobble path for organic quality
        draw_wobble_path(ctx, hair_pts, amplitude=1.0, frequency=0.12,
                         seed=rng.randint(0, 9999), closed=True, jitter=0.3)
        set_color(ctx, LUMA_HAIR)
        ctx.fill()

    # Hair strands — spikes breaking silhouette
    strand_angles = [195, 215, 240, 260, 280, 310, 340, 370, 395, 420, 450]
    for sa in strand_angles:
        angle = math.radians(sa)
        base_r_s = head_r + int(s(10))
        strand_len = rng.randint(int(s(12)), int(s(24)))
        strand_w = rng.choice([1.5, 2.0, 2.0, 2.5])
        sx = head_cx + int(base_r_s * math.cos(angle))
        sy = head_cy + int(base_r_s * 0.90 * math.sin(angle))
        ex_s = head_cx + int((base_r_s + strand_len) * math.cos(angle + rng.uniform(-0.15, 0.15)))
        ey_s = head_cy + int((base_r_s + strand_len) * 0.90 * math.sin(angle + rng.uniform(-0.15, 0.15)))
        if sy < head_cy + int(head_r * 0.3):
            ctx.new_path()
            ctx.move_to(sx, sy)
            ctx.line_to(ex_s, ey_s)
            ctx.set_line_width(strand_w)
            ctx.set_line_cap(cairo.LINE_CAP_ROUND)
            set_color(ctx, LUMA_HAIR)
            ctx.stroke()

    # Highlight strands
    for ha in [240, 280, 350]:
        angle = math.radians(ha)
        r_inner = head_r + int(s(6))
        r_outer = head_r + int(s(14))
        hx1 = head_cx + int(r_inner * math.cos(angle))
        hy1 = head_cy + int(r_inner * 0.90 * math.sin(angle))
        hx2 = head_cx + int(r_outer * math.cos(angle + 0.08))
        hy2 = head_cy + int(r_outer * 0.90 * math.sin(angle + 0.08))
        if hy1 < head_cy + int(head_r * 0.2):
            ctx.new_path()
            ctx.move_to(hx1, hy1)
            ctx.line_to(hx2, hy2)
            ctx.set_line_width(max(1, int(s(2))))
            ctx.set_line_cap(cairo.LINE_CAP_ROUND)
            set_color(ctx, LUMA_HAIR_HL)
            ctx.stroke()


# ══════════════════════════════════════════════════════════════════════════════
# BYTE — Storyboard scale drawing
# ══════════════════════════════════════════════════════════════════════════════

def draw_byte_sb(ctx, cx, cy, body_h=75, expression="still", facing="left",
                 lean_deg=0.0, hovering=True, seed=1718):
    """Draw Byte at storyboard scale using pycairo.

    Args:
        ctx:        cairo Context to draw on
        cx:         horizontal center of character
        cy:         vertical center of character body
        body_h:     total body height in pixels
        expression: "still", "grumpy", "alarmed", "spotted", "offended"
        facing:     "left" or "right"
        lean_deg:   forward lean in degrees
        hovering:   if True, no ground contact
        seed:       RNG seed

    Returns:
        dict with key positions: {face_cx, face_cy, face_r, body_cx}
    """
    import random
    rng = random.Random(seed)

    face_dir = -1 if facing == "left" else 1
    body_w = int(body_h * 0.72)
    lean_dx = int(body_h * 0.03 * lean_deg) * face_dir

    body_cx = cx + lean_dx
    body_top_y = cy - body_h // 2

    # ── Body — inverted teardrop shape via smooth polygon ──
    # Top: wide ellipse; bottom: tapered point
    top_w = body_w // 2
    top_pts = [
        (body_cx, body_top_y),                             # top center
        (body_cx + top_w, body_top_y + body_h * 0.30),    # right shoulder
        (body_cx + int(body_w * 0.35), cy + body_h * 0.10),  # right waist
        (body_cx, cy + body_h // 2),                       # bottom point
        (body_cx - int(body_w * 0.35), cy + body_h * 0.10),  # left waist
        (body_cx - top_w, body_top_y + body_h * 0.30),    # left shoulder
    ]
    draw_smooth_polygon(ctx, top_pts, bulge_frac=0.15)

    # Gradient fill: lighter top to darker bottom
    draw_gradient_fill(ctx, "linear",
                       [(0.0, BYTE_TEAL), (1.0, (0, 160, 180))],
                       x0=body_cx, y0=body_top_y,
                       x1=body_cx, y1=cy + body_h // 2)

    # Shadow on the side away from facing
    draw_smooth_polygon(ctx, top_pts, bulge_frac=0.15)
    shadow_side = -face_dir
    # Clip shadow to body half
    ctx.save()
    ctx.rectangle(body_cx + min(0, shadow_side * top_w),
                  body_top_y, top_w, body_h)
    ctx.clip()
    draw_smooth_polygon(ctx, top_pts, bulge_frac=0.15)
    set_color(ctx, BYTE_DARK + (80,))
    ctx.fill()
    ctx.restore()

    # Body outline
    draw_smooth_polygon(ctx, top_pts, bulge_frac=0.15)
    stroke_path(ctx, LINE_COLOR, weight_tier="anchor")

    # ── Face ──
    face_cx = body_cx + int(body_w * 0.08) * face_dir
    face_cy = body_top_y + int(body_h * 0.25)
    face_r = int(body_w * 0.45)

    _draw_byte_face(ctx, face_cx, face_cy, face_r, expression, face_dir, rng)

    # ── Arms — curved tubes ──
    arm_top_y = body_top_y + int(body_h * 0.35)
    for side in [-1, 1]:
        arm_x = body_cx + side * (body_w // 2 + 2)
        elbow_x = arm_x + side * int(body_h * 0.08)
        hand_x = arm_x + side * int(body_h * 0.03)
        arm_pts = [
            (arm_x, arm_top_y),
            (elbow_x, arm_top_y + int(body_h * 0.14)),
            (hand_x, arm_top_y + int(body_h * 0.22)),
        ]
        draw_tapered_stroke(ctx, arm_pts, 6, 4, BYTE_TEAL, segments=12)

    # ── Legs — stubby ──
    leg_top_y = cy + int(body_h * 0.35)
    for leg_off in [-int(body_h * 0.07), int(body_h * 0.07)]:
        leg_pts = [
            (body_cx + leg_off, leg_top_y),
            (body_cx + leg_off - 1, leg_top_y + int(body_h * 0.12)),
            (body_cx + leg_off, leg_top_y + int(body_h * 0.22)),
        ]
        draw_tapered_stroke(ctx, leg_pts, 7, 5, BYTE_TEAL, segments=8)

    return {
        "face_cx": face_cx,
        "face_cy": face_cy,
        "face_r": face_r,
        "body_cx": body_cx,
    }


def _draw_byte_face(ctx, face_cx, face_cy, face_r, expression, face_dir, rng):
    """Byte's face — normal eye + cracked eye + pixel mouth."""
    # Normal eye (toward facing)
    ne_cx = face_cx + int(face_r * 0.35) * face_dir
    ne_cy = face_cy - int(face_r * 0.18)
    ne_r = int(face_r * 0.30)

    # Eye socket
    draw_ellipse(ctx, ne_cx, ne_cy, ne_r, ne_r)
    set_color(ctx, (8, 8, 18))
    ctx.fill()

    # Iris
    draw_ellipse(ctx, ne_cx, ne_cy, ne_r - 3, ne_r - 3)
    set_color(ctx, DEEP_CYAN)
    ctx.fill()

    # Pupil with iris shift for gaze direction
    iris_shift = int(ne_r * 0.30) * face_dir
    draw_ellipse(ctx, ne_cx + iris_shift, ne_cy, 5, 5)
    set_color(ctx, VOID_BLACK)
    ctx.fill()

    # Lid expression adjustments
    if expression in ("assessing", "grumpy", "offended"):
        # Narrowed lid
        ctx.new_path()
        ctx.move_to(ne_cx - ne_r, ne_cy - int(ne_r * 0.1))
        ctx.line_to(ne_cx + ne_r, ne_cy - int(ne_r * 0.3))
        ctx.set_line_width(max(2, ne_r // 2))
        set_color(ctx, BYTE_TEAL)
        ctx.stroke()

    # Cracked eye (outward from facing)
    ce_cx = face_cx - int(face_r * 0.32) * face_dir
    ce_cy = face_cy - int(face_r * 0.18)
    ce_r = int(face_r * 0.28)

    draw_ellipse(ctx, ce_cx, ce_cy, ce_r, ce_r)
    set_color(ctx, (8, 8, 18))
    ctx.fill()

    # Crack lines (HOT_MAGENTA scar)
    for crack_ang in [30, 70, 120, 160]:
        ca = math.radians(crack_ang)
        ctx.new_path()
        ctx.move_to(ce_cx + int(ce_r * 0.2 * math.cos(ca)),
                    ce_cy + int(ce_r * 0.2 * math.sin(ca)))
        ctx.line_to(ce_cx + int(ce_r * 0.9 * math.cos(ca)),
                    ce_cy + int(ce_r * 0.9 * math.sin(ca)))
        ctx.set_line_width(1)
        set_color(ctx, HOT_MAGENTA)
        ctx.stroke()

    # Divergent processing dot
    div_x = -int(ce_r * 0.20)
    draw_ellipse(ctx, ce_cx + div_x, ce_cy, 3, 3)
    set_color(ctx, ELEC_CYAN)
    ctx.fill()

    # Mouth — pixel grimace
    mouth_y = face_cy + int(face_r * 0.40)
    mouth_w = int(face_r * 0.60)
    ctx.new_path()
    ctx.rectangle(face_cx - mouth_w, mouth_y - 2, mouth_w * 2, 4)
    set_color(ctx, VOID_BLACK)
    ctx.fill()

    # Pixel teeth
    for mx_tooth in range(int(face_cx - mouth_w + 2), int(face_cx + mouth_w - 2), 5):
        ctx.new_path()
        ctx.rectangle(mx_tooth, mouth_y - 1, 1, 1)
        set_color(ctx, (200, 200, 210))
        ctx.fill()


# ══════════════════════════════════════════════════════════════════════════════
# Props
# ══════════════════════════════════════════════════════════════════════════════

def draw_chip(ctx, x, y, size=7, trail_len=40, trail_step=6):
    """Draw a falling pixel chip with dotted descent trail.

    Args:
        ctx:        cairo Context
        x, y:       center of chip
        size:       half-size of chip square
        trail_len:  length of dotted trail above chip
        trail_step: spacing between trail dots
    """
    # Chip body
    ctx.new_path()
    ctx.rectangle(x - size, y - size, size * 2, size * 2)
    set_color(ctx, ELEC_CYAN)
    ctx.fill()

    # Inner border
    ctx.new_path()
    ctx.rectangle(x - size + 1, y - size + 1, size * 2 - 2, size * 2 - 2)
    set_color(ctx, VOID_BLACK)
    ctx.set_line_width(1)
    ctx.stroke()

    # Dotted descent trail
    for dy in range(0, trail_len, trail_step):
        ctx.new_path()
        ctx.rectangle(x - 0.5, y - size - 4 - dy - 0.5, 1, 1)
        set_color(ctx, (0, 100, 120))
        ctx.fill()


# ══════════════════════════════════════════════════════════════════════════════
# Self-test
# ══════════════════════════════════════════════════════════════════════════════

def _self_test():
    """Generate a test image showing both characters."""
    import time

    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
    PROD_DIR = os.path.join(PROJECT_ROOT, "output", "production")
    os.makedirs(PROD_DIR, exist_ok=True)

    W, H = 800, 400
    surface, ctx, _, _ = create_surface(W, H)
    t0 = time.time()

    # BG
    fill_background(ctx, W, H, (32, 28, 24))

    # Floor line
    floor_y = 340
    ctx.new_path()
    ctx.move_to(0, floor_y)
    ctx.line_to(W, floor_y)
    set_color(ctx, (80, 70, 60))
    ctx.set_line_width(1)
    ctx.stroke()

    # Luma sitting
    luma_info = draw_luma_sb(ctx, 200, floor_y, char_h=140, pose="sitting",
                              lean_deg=3.0, expression="assessing", facing="right")

    # Luma standing
    draw_luma_sb(ctx, 500, floor_y, char_h=160, pose="standing",
                 lean_deg=2.0, expression="neutral", facing="left")

    # Byte
    byte_info = draw_byte_sb(ctx, 650, 280, body_h=75, expression="still",
                              facing="left", lean_deg=2.0)

    # Chip
    draw_chip(ctx, 400, 280)

    elapsed = time.time() - t0

    # Label
    ctx.select_font_face("monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(12)
    set_color(ctx, (200, 200, 200))
    ctx.move_to(10, H - 10)
    ctx.show_text(f"LTG_TOOL_sb_char_draw v{__version__} self-test  |  {elapsed*1000:.1f}ms")

    img = to_pil_image(surface)
    if img.width > 1280 or img.height > 1280:
        img.thumbnail((1280, 1280), Image.LANCZOS)

    out_path = os.path.join(PROD_DIR, "LTG_RENDER_sb_char_draw_selftest_c51.png")
    img.save(out_path)
    print(f"Self-test saved: {out_path}")
    print(f"  Size: {img.size[0]}x{img.size[1]}")
    print(f"  Render time: {elapsed*1000:.1f}ms")


if __name__ == "__main__":
    _self_test()
