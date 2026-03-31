#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_luma_cairo_expressions.py — Luma Full Expression Sheet (Cairo Engine) v2.0.0
"Luma & the Glitchkin" — Cycle 52 / Maya Santos

PURPOSE:
  Full Luma expression sheet with all 6 expressions using pycairo engine.
  Replaces PIL polygon-based construction with native bezier curves, variable-width
  strokes, anti-aliased rendering, and form shadows.

  Implements Lee Tanaka's gesture spec (C50): offset chain for hip/torso/head,
  weight distribution, counterpose, and per-expression gesture lines.

  Integrates Sam Kowalski's color enhancements (C50): scene tint, form shadow,
  skin warmth via PIL compositing after cairo render.

EXPRESSIONS (all 6):
  CURIOUS    — Forward C-curve, leaning in, 60/40 front weight
  DETERMINED — Backward S-curve, power pose, wide planted stance
  SURPRISED  — Backward C-curve, startle recoil, 70/30 back weight
  WORRIED    — Compressed S-curve, inward curl, self-hold arms
  DELIGHTED  — Upward erupting S-curve, tiptoe, asymmetric celebration
  FRUSTRATED — Aggressive diagonal, dramatic weight shift, stomp

CONSTRUCTION:
  - 37% head ratio (head height = 37% of total body height)
  - Eyes = 30% of head width (large, expressive)
  - Pycairo bezier paths for all organic forms
  - Variable-width stroke via manual tapering on limbs
  - Form shadows as overlaid alpha shapes
  - Gesture line visualization overlay
  - C47 shoulder involvement on all poses

RENDER PIPELINE:
  1. Cairo renders at 2x (2560x1440) to ImageSurface
  2. Convert to PIL Image
  3. Apply Sam's color enhancements (scene tint, skin warmth, form shadow)
  4. Downscale to 1280x720 with LANCZOS
  5. Save PNG

OUTPUT:
  output/characters/main/LTG_CHAR_luma_expression_sheet.png (1280x720)
  output/production/LTG_PROD_luma_cairo_expressions.png (1280x720) [copy]

Dependencies: pycairo, Pillow, math, random
"""

__version__ = "2.0.0"
__author__ = "Maya Santos"
__cycle__ = 52

import math
import os
import sys
import random

import cairo
from PIL import Image, ImageDraw

# Add tools dir to path for imports
TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, TOOLS_DIR)

try:
    from LTG_TOOL_project_paths import output_dir, ensure_dir
except ImportError:
    import pathlib
    def output_dir(*parts):
        return pathlib.Path("/home/wipkat/team/output").joinpath(*parts)
    def ensure_dir(path):
        path.mkdir(parents=True, exist_ok=True)
        return path

try:
    from LTG_TOOL_character_color_enhance import (
        apply_scene_tint, apply_skin_warmth, apply_form_shadow
    )
    HAS_COLOR_ENHANCE = True
except ImportError:
    HAS_COLOR_ENHANCE = False

# ── Palette ──────────────────────────────────────────────────────────────────
SKIN       = (200/255, 136/255, 90/255)
SKIN_SH    = (160/255, 104/255, 64/255)
SKIN_HL    = (223/255, 160/255, 112/255)
HAIR       = (26/255, 15/255, 10/255)
HAIR_HL    = (61/255, 31/255, 15/255)
EYE_W      = (250/255, 240/255, 220/255)
EYE_IRIS   = (200/255, 125/255, 62/255)
EYE_PUP    = (59/255, 40/255, 32/255)
EYE_HL     = (1.0, 1.0, 1.0)
BLUSH_C    = (232/255, 148/255, 100/255, 0.33)
LINE_COL   = (59/255, 40/255, 32/255)

# Expression-specific hoodie colors
HOODIE_CURIOUS     = (150/255, 175/255, 200/255)
HOODIE_CURIOUS_SH  = (120/255, 145/255, 170/255)
HOODIE_SURPRISED   = (232/255, 112/255, 58/255)
HOODIE_SURPRISED_SH= (184/255, 74/255, 32/255)
HOODIE_DETERMINED  = (220/255, 130/255, 55/255)
HOODIE_DETERMINED_SH= (180/255, 95/255, 35/255)
HOODIE_WORRIED     = (165/255, 155/255, 185/255)
HOODIE_WORRIED_SH  = (135/255, 125/255, 155/255)
HOODIE_DELIGHTED   = (245/255, 155/255, 65/255)
HOODIE_DELIGHTED_SH= (200/255, 115/255, 40/255)
HOODIE_FRUSTRATED  = (210/255, 95/255, 55/255)
HOODIE_FRUSTRATED_SH= (170/255, 65/255, 35/255)

PANTS      = (42/255, 40/255, 80/255)
PANTS_SH   = (26/255, 24/255, 48/255)
SHOE       = (245/255, 232/255, 208/255)
SHOE_SOLE  = (199/255, 91/255, 57/255)
LACES      = (0, 240/255, 1.0)
PX_CYAN    = (0, 240/255, 1.0)
PX_MAG     = (1.0, 45/255, 107/255)
CANVAS_BG  = (235/255, 224/255, 206/255)

# PIL palette for color enhance integration
SKIN_PIL       = (200, 136, 90)
SKIN_HL_PIL    = (232, 184, 136)
SKIN_SH_PIL    = (168, 104, 56)
BLUSH_PIL      = (232, 168, 124)
HOODIE_PIL     = (232, 112, 58)
HOODIE_SH_PIL  = (184, 74, 32)

# Hoodie color lookup
HOODIE_COLORS = {
    "CURIOUS":    (HOODIE_CURIOUS, HOODIE_CURIOUS_SH),
    "DETERMINED": (HOODIE_DETERMINED, HOODIE_DETERMINED_SH),
    "SURPRISED":  (HOODIE_SURPRISED, HOODIE_SURPRISED_SH),
    "WORRIED":    (HOODIE_WORRIED, HOODIE_WORRIED_SH),
    "DELIGHTED":  (HOODIE_DELIGHTED, HOODIE_DELIGHTED_SH),
    "FRUSTRATED": (HOODIE_FRUSTRATED, HOODIE_FRUSTRATED_SH),
}

# ── Constants ────────────────────────────────────────────────────────────────
RENDER_W = 2560
RENDER_H = 1440
OUTPUT_W = 1280
OUTPUT_H = 720
SEED = 52

# ── Gesture Specs (from Lee's C50 analysis) ─────────────────────────────────
# Offset chain: hip_shift, shoulder_offset, head_offset (pixels at 2x)
# Weight: (front_pct, back_pct), front_foot_lift, back_foot_lift
# Angles: hip_tilt_deg, shoulder_tilt_deg, head_tilt_deg
# Torso_lean: degrees from vertical (positive = forward)

GESTURE_SPECS = {
    "CURIOUS": {
        "hip_shift": 18,           # amplified from 12
        "shoulder_offset": -16,    # amplified from -10
        "head_offset": -28,        # amplified from -18
        "torso_lean": -24,         # amplified from -16
        "hip_tilt": 5.0,
        "shoulder_tilt": -5.0,
        "head_tilt": -12.0,        # amplified from -8
        "weight_front": 0.60,
        "weight_back": 0.40,
        "front_foot_lift": 0,
        "back_foot_lift": 0,
        "front_foot_angle": -15,
        "back_foot_angle": 18,
        "left_arm": "forward_reaching",
        "right_arm": "chin_touch",
        "brow_lift_l": 14,
        "brow_lift_r": 22,
        "mouth": "gentle_smile",
        "eye_openness": 1.1,
        "gaze_dx": 4,
        "gaze_dy": -2,
    },
    "DETERMINED": {
        "hip_shift": 6,            # subtle — power stance is centered
        "shoulder_offset": -4,
        "head_offset": 6,
        "torso_lean": 8,
        "hip_tilt": 2.0,
        "shoulder_tilt": -3.0,
        "head_tilt": 6.0,
        "weight_front": 0.55,
        "weight_back": 0.45,
        "front_foot_lift": 0,
        "back_foot_lift": 0,
        "front_foot_angle": 15,
        "back_foot_angle": -15,
        "left_arm": "fist_forward",
        "right_arm": "fist_hip",
        "brow_lift_l": 6,
        "brow_lift_r": 4,
        "mouth": "firm_line",
        "eye_openness": 0.95,
        "gaze_dx": 2,
        "gaze_dy": -1,
        "stance_wide": 1.45,       # amplified from 1.25 — WIDEST stance
    },
    "SURPRISED": {
        "hip_shift": -36,          # amplified from -26
        "shoulder_offset": 26,     # amplified from 18
        "head_offset": 24,         # amplified from 16
        "torso_lean": 38,          # amplified from 28
        "hip_tilt": -9.0,
        "shoulder_tilt": 10.0,
        "head_tilt": 16.0,         # amplified from 12
        "weight_front": 0.20,
        "weight_back": 0.80,
        "front_foot_lift": 20,     # amplified from 14
        "back_foot_lift": 0,
        "front_foot_angle": 18,
        "back_foot_angle": -12,
        "left_arm": "defensive_high",
        "right_arm": "flung_back",
        "brow_lift_l": 26,
        "brow_lift_r": 20,
        "mouth": "open_o",
        "eye_openness": 1.45,
        "gaze_dx": -3,
        "gaze_dy": -4,
    },
    "WORRIED": {
        # MOST COMPRESSED pose — pulls tight, arms close, shoulders up
        # Opposite direction lean from CURIOUS (CURIOUS leans left, WORRIED leans right)
        "hip_shift": 12,           # positive = shift right
        "shoulder_offset": -8,
        "head_offset": 6,          # head shifts right (opposite to CURIOUS)
        "torso_lean": 10,          # lean RIGHT (positive, opposite to CURIOUS negative)
        "hip_tilt": -5.0,
        "shoulder_tilt": 8.0,      # shoulders hunched UP
        "head_tilt": 14.0,         # head tilts RIGHT (opposite to CURIOUS left tilt)
        "weight_front": 0.40,
        "weight_back": 0.60,
        "front_foot_lift": 4,
        "back_foot_lift": 0,
        "front_foot_angle": -18,
        "back_foot_angle": 10,
        "left_arm": "self_hold_grip",
        "right_arm": "self_hold_cross",
        "brow_lift_l": 18,
        "brow_lift_r": 12,
        "mouth": "tight_frown",
        "eye_openness": 1.05,
        "gaze_dx": 0,
        "gaze_dy": 3,
    },
    "DELIGHTED": {
        # TALLEST pose — erupting upward, tiptoe, head thrown back
        # Lean direction: slight RIGHT lean (opposite to CURIOUS's left lean)
        "hip_shift": -16,          # hip shifts LEFT (opposite to CURIOUS right)
        "shoulder_offset": 14,     # shoulders RIGHT
        "head_offset": 10,         # head RIGHT and UP
        "torso_lean": 8,           # lean RIGHT slightly (opposite to CURIOUS)
        "hip_tilt": -7.0,          # opposite to CURIOUS
        "shoulder_tilt": 6.0,
        "head_tilt": 18.0,         # head thrown back RIGHT (opposite to CURIOUS left)
        "weight_front": 0.50,
        "weight_back": 0.50,
        "front_foot_lift": 12,     # both feet lifting — tiptoe
        "back_foot_lift": 8,
        "front_foot_angle": 10,
        "back_foot_angle": -8,
        "left_arm": "celebration_high",
        "right_arm": "celebration_pump",
        "brow_lift_l": 20,
        "brow_lift_r": 16,
        "mouth": "wide_grin",
        "eye_openness": 1.25,
        "gaze_dx": 2,
        "gaze_dy": -3,
        "heel_lift": 10,           # big tiptoe
    },
    "FRUSTRATED": {
        # COMPACT CROUCH — opposite to SURPRISED's open, tall recoil.
        # SURPRISED is tall+wide+backward. FRUSTRATED is short+tight+forward.
        # Arms both LOW and CLOSE to body. Widest leg stance but shortest torso.
        "hip_shift": 20,           # OPPOSITE direction to SURPRISED (-36)
        "shoulder_offset": -14,
        "head_offset": -10,
        "torso_lean": -14,         # lean FORWARD (opposite to SURPRISED's backward lean)
        "hip_tilt": 8.0,           # OPPOSITE to SURPRISED (-9)
        "shoulder_tilt": -7.0,
        "head_tilt": -18.0,        # head tilted FAR LEFT and DOWN — opposite to SURPRISED (+16)
        "weight_front": 0.80,      # weight FORWARD (stomp)
        "weight_back": 0.20,
        "front_foot_lift": 0,
        "back_foot_lift": 6,
        "front_foot_angle": -22,
        "back_foot_angle": 25,
        "left_arm": "flung_down_wide",
        "right_arm": "hair_pull",
        "brow_lift_l": 4,
        "brow_lift_r": 8,
        "mouth": "gritted_teeth",
        "eye_openness": 0.85,
        "gaze_dx": -2,
        "gaze_dy": 1,
        "stance_wide": 1.5,        # WIDEST stance — stomp
    },
}


# ── Cairo Helpers ────────────────────────────────────────────────────────────

def cairo_surface_to_pil(surface):
    """Convert cairo ImageSurface (ARGB32) to PIL RGBA Image."""
    w = surface.get_width()
    h = surface.get_height()
    buf = surface.get_data()
    img = Image.frombuffer("RGBA", (w, h), bytes(buf), "raw", "BGRa", 0, 1)
    return img.copy()


def set_color(ctx, color, alpha=1.0):
    """Set source color, handling 3-tuple or 4-tuple."""
    if len(color) == 4:
        ctx.set_source_rgba(color[0], color[1], color[2], color[3])
    else:
        ctx.set_source_rgba(color[0], color[1], color[2], alpha)


def draw_ellipse_path(ctx, cx, cy, rx, ry):
    """Add an ellipse to the current path using bezier approximation."""
    ctx.save()
    ctx.translate(cx, cy)
    ctx.scale(rx, ry)
    ctx.arc(0, 0, 1.0, 0, 2 * math.pi)
    ctx.restore()


def draw_bean_torso(ctx, cx, cy, w_top, w_bot, h, lean_dx, hip_tilt_px, shoulder_tilt_px):
    """Draw an organic bean-shaped torso using cubic bezier curves.
    Returns (left_shoulder, right_shoulder, left_hip, right_hip) attachment points."""
    top_y = cy - h / 2
    bot_y = cy + h / 2

    # Shoulder points (affected by lean and shoulder tilt)
    ls_x = cx + lean_dx - w_top
    ls_y = top_y + shoulder_tilt_px
    rs_x = cx + lean_dx + w_top
    rs_y = top_y - shoulder_tilt_px

    # Hip points (affected by lean and hip tilt)
    lh_x = cx + lean_dx * 0.5 - w_bot + hip_tilt_px
    lh_y = bot_y
    rh_x = cx + lean_dx * 0.5 + w_bot - hip_tilt_px
    rh_y = bot_y

    ctx.new_path()
    # Left side: shoulder to hip (outward bulge for organic shape)
    ctx.move_to(ls_x, ls_y)
    cp1x = ls_x - w_top * 0.15
    cp1y = ls_y + h * 0.35
    cp2x = lh_x - w_bot * 0.08
    cp2y = lh_y - h * 0.15
    ctx.curve_to(cp1x, cp1y, cp2x, cp2y, lh_x, lh_y)

    # Bottom: left hip to right hip (gentle curve)
    ctx.curve_to(lh_x + w_bot * 0.3, bot_y + h * 0.04,
                 rh_x - w_bot * 0.3, bot_y + h * 0.04,
                 rh_x, rh_y)

    # Right side: right hip up to right shoulder
    cp3x = rh_x + w_bot * 0.08
    cp3y = rh_y - h * 0.15
    cp4x = rs_x + w_top * 0.15
    cp4y = rs_y + h * 0.35
    ctx.curve_to(cp3x, cp3y, cp4x, cp4y, rs_x, rs_y)

    # Top: right shoulder to left shoulder (gentle curve for neck gap)
    ctx.curve_to(rs_x - w_top * 0.3, top_y + h * 0.03,
                 ls_x + w_top * 0.3, top_y + h * 0.03,
                 ls_x, ls_y)

    ctx.close_path()
    return (ls_x, ls_y), (rs_x, rs_y), (lh_x, lh_y), (rh_x, rh_y)


def draw_variable_stroke_limb(ctx, points, w_start, w_end, fill_color, line_color, line_w):
    """Draw a limb as a filled tapered tube with variable-width stroke.
    points: list of (x, y) along centerline."""
    n = len(points)
    if n < 2:
        return
    left_edge = []
    right_edge = []
    for i in range(n):
        t = i / max(1, n - 1)
        w = w_start + (w_end - w_start) * t
        if i == 0:
            dx = points[1][0] - points[0][0]
            dy = points[1][1] - points[0][1]
        elif i == n - 1:
            dx = points[-1][0] - points[-2][0]
            dy = points[-1][1] - points[-2][1]
        else:
            dx = points[i+1][0] - points[i-1][0]
            dy = points[i+1][1] - points[i-1][1]
        length = math.hypot(dx, dy) or 1.0
        nx = -dy / length
        ny = dx / length
        left_edge.append((points[i][0] + nx * w, points[i][1] + ny * w))
        right_edge.append((points[i][0] - nx * w, points[i][1] - ny * w))

    # Draw filled shape
    ctx.new_path()
    ctx.move_to(*left_edge[0])
    for p in left_edge[1:]:
        ctx.line_to(*p)
    for p in reversed(right_edge):
        ctx.line_to(*p)
    ctx.close_path()
    set_color(ctx, fill_color)
    ctx.fill_preserve()
    set_color(ctx, line_color)
    ctx.set_line_width(line_w)
    ctx.stroke()


def bezier_points(p0, p1, p2, p3, steps=40):
    """Generate points along a cubic bezier curve."""
    pts = []
    for i in range(steps + 1):
        t = i / steps
        x = ((1-t)**3 * p0[0] + 3*(1-t)**2*t * p1[0] +
             3*(1-t)*t**2 * p2[0] + t**3 * p3[0])
        y = ((1-t)**3 * p0[1] + 3*(1-t)**2*t * p1[1] +
             3*(1-t)*t**2 * p2[1] + t**3 * p3[1])
        pts.append((x, y))
    return pts


def qbezier_points(p0, p1, p2, steps=30):
    """Quadratic bezier points."""
    pts = []
    for i in range(steps + 1):
        t = i / steps
        x = (1-t)**2 * p0[0] + 2*(1-t)*t * p1[0] + t**2 * p2[0]
        y = (1-t)**2 * p0[1] + 2*(1-t)*t * p1[1] + t**2 * p2[1]
        pts.append((x, y))
    return pts


# ── Arm Drawing Functions (per-expression) ──────────────────────────────────

def draw_arm_forward_reaching(ctx, ls_pt, head_cx, head_r, s, hoodie, lw_major, lw_minor, lw_accent, arm_w_top, arm_w_bot, hand_r_s):
    """CURIOUS: left arm extended forward, palm-down (far reach)."""
    la_shoulder = (ls_pt[0] + 10*s, ls_pt[1] + 8*s)
    la_elbow = (la_shoulder[0] - 70*s, la_shoulder[1] + 14*s)
    la_hand = (la_elbow[0] - 40*s, la_elbow[1] - 42*s)
    upper = bezier_points(la_shoulder,
                          (la_shoulder[0] - 15*s, la_shoulder[1] + 5*s),
                          (la_elbow[0] + 5*s, la_elbow[1] - 8*s),
                          la_elbow, steps=25)
    fore = bezier_points(la_elbow,
                         (la_elbow[0] - 8*s, la_elbow[1] - 12*s),
                         (la_hand[0] + 8*s, la_hand[1] + 10*s),
                         la_hand, steps=25)
    draw_variable_stroke_limb(ctx, upper, arm_w_top, arm_w_bot * 1.1, hoodie, LINE_COL, lw_major)
    draw_variable_stroke_limb(ctx, fore, arm_w_bot * 1.1, arm_w_bot, hoodie, LINE_COL, lw_major)
    # Hand (mitten)
    draw_ellipse_path(ctx, la_hand[0], la_hand[1], hand_r_s, hand_r_s * 0.75)
    set_color(ctx, SKIN)
    ctx.fill_preserve()
    set_color(ctx, LINE_COL)
    ctx.set_line_width(lw_minor)
    ctx.stroke()
    # Thumb
    draw_ellipse_path(ctx, la_hand[0] + 5*s, la_hand[1] + 5*s, 4*s, 3*s)
    set_color(ctx, SKIN)
    ctx.fill_preserve()
    set_color(ctx, LINE_COL)
    ctx.set_line_width(lw_accent)
    ctx.stroke()


def draw_arm_chin_touch(ctx, rs_pt, head_cx, head_cy, head_r, s, hoodie, lw_major, lw_minor, lw_accent, arm_w_top, arm_w_bot, hand_r_s):
    """CURIOUS: right hand near chin."""
    ra_shoulder = (rs_pt[0] - 10*s, rs_pt[1] + 8*s)
    chin_x = head_cx + 5*s
    chin_y = head_cy + head_r * 0.55
    ra_elbow = (ra_shoulder[0] + 5*s, ra_shoulder[1] + 30*s)
    ra_hand = (chin_x + 8*s, chin_y + 5*s)
    upper = bezier_points(ra_shoulder,
                          (ra_shoulder[0] + 8*s, ra_shoulder[1] + 12*s),
                          (ra_elbow[0] - 3*s, ra_elbow[1] - 10*s),
                          ra_elbow, steps=25)
    fore = bezier_points(ra_elbow,
                         (ra_elbow[0] - 2*s, ra_elbow[1] + 8*s),
                         (ra_hand[0] + 10*s, ra_hand[1] + 15*s),
                         ra_hand, steps=25)
    draw_variable_stroke_limb(ctx, upper, arm_w_top, arm_w_bot * 1.1, hoodie, LINE_COL, lw_major)
    draw_variable_stroke_limb(ctx, fore, arm_w_bot * 1.1, arm_w_bot, hoodie, LINE_COL, lw_major)
    draw_ellipse_path(ctx, ra_hand[0], ra_hand[1], hand_r_s, hand_r_s * 0.75)
    set_color(ctx, SKIN)
    ctx.fill_preserve()
    set_color(ctx, LINE_COL)
    ctx.set_line_width(lw_minor)
    ctx.stroke()
    # Index finger extended toward chin
    ctx.new_path()
    ctx.move_to(ra_hand[0] - 3*s, ra_hand[1] - hand_r_s * 0.5)
    ctx.line_to(chin_x, chin_y)
    set_color(ctx, SKIN)
    ctx.set_line_width(3*s)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.stroke()
    ctx.new_path()
    ctx.move_to(ra_hand[0] - 3*s, ra_hand[1] - hand_r_s * 0.5)
    ctx.line_to(chin_x, chin_y)
    set_color(ctx, LINE_COL)
    ctx.set_line_width(lw_accent)
    ctx.stroke()


def draw_arm_defensive_high(ctx, ls_pt, s, hoodie, lw_major, lw_minor, lw_accent, arm_w_top, arm_w_bot, hand_r_s):
    """SURPRISED: left arm raised high near face, palm outward (amplified)."""
    la_shoulder = (ls_pt[0] + 10*s, ls_pt[1] + 5*s)
    la_elbow = (la_shoulder[0] - 38*s, la_shoulder[1] - 48*s)
    la_hand = (la_elbow[0] - 20*s, la_elbow[1] - 50*s)
    upper = bezier_points(la_shoulder,
                          (la_shoulder[0] - 12*s, la_shoulder[1] - 8*s),
                          (la_elbow[0] + 5*s, la_elbow[1] + 10*s),
                          la_elbow, steps=25)
    fore = bezier_points(la_elbow,
                         (la_elbow[0] - 5*s, la_elbow[1] - 10*s),
                         (la_hand[0] + 5*s, la_hand[1] + 12*s),
                         la_hand, steps=25)
    draw_variable_stroke_limb(ctx, upper, arm_w_top, arm_w_bot * 1.1, hoodie, LINE_COL, lw_major)
    draw_variable_stroke_limb(ctx, fore, arm_w_bot * 1.1, arm_w_bot, hoodie, LINE_COL, lw_major)
    draw_ellipse_path(ctx, la_hand[0], la_hand[1], hand_r_s * 1.1, hand_r_s * 0.9)
    set_color(ctx, SKIN)
    ctx.fill_preserve()
    set_color(ctx, LINE_COL)
    ctx.set_line_width(lw_minor)
    ctx.stroke()
    for angle_deg in [-30, -10, 10, 30]:
        rad = math.radians(angle_deg - 90)
        fx = la_hand[0] + math.cos(rad) * hand_r_s * 1.2
        fy = la_hand[1] + math.sin(rad) * hand_r_s * 1.0
        ctx.new_path()
        ctx.move_to(la_hand[0] + math.cos(rad) * hand_r_s * 0.6,
                    la_hand[1] + math.sin(rad) * hand_r_s * 0.5)
        ctx.line_to(fx, fy)
        set_color(ctx, LINE_COL)
        ctx.set_line_width(lw_accent)
        ctx.stroke()


def draw_arm_flung_back(ctx, rs_pt, s, hoodie, lw_major, lw_minor, lw_accent, arm_w_top, arm_w_bot, hand_r_s):
    """SURPRISED: right arm flung wide to side and behind (amplified)."""
    ra_shoulder = (rs_pt[0] - 8*s, rs_pt[1] + 5*s)
    ra_elbow = (ra_shoulder[0] + 65*s, ra_shoulder[1] + 8*s)
    ra_hand = (ra_elbow[0] + 45*s, ra_elbow[1] + 30*s)
    upper = bezier_points(ra_shoulder,
                          (ra_shoulder[0] + 15*s, ra_shoulder[1] + 3*s),
                          (ra_elbow[0] - 8*s, ra_elbow[1] - 5*s),
                          ra_elbow, steps=25)
    fore = bezier_points(ra_elbow,
                         (ra_elbow[0] + 10*s, ra_elbow[1] + 3*s),
                         (ra_hand[0] - 8*s, ra_hand[1] - 5*s),
                         ra_hand, steps=25)
    draw_variable_stroke_limb(ctx, upper, arm_w_top, arm_w_bot * 1.1, hoodie, LINE_COL, lw_major)
    draw_variable_stroke_limb(ctx, fore, arm_w_bot * 1.1, arm_w_bot, hoodie, LINE_COL, lw_major)
    draw_ellipse_path(ctx, ra_hand[0], ra_hand[1], hand_r_s * 1.0, hand_r_s * 0.8)
    set_color(ctx, SKIN)
    ctx.fill_preserve()
    set_color(ctx, LINE_COL)
    ctx.set_line_width(lw_minor)
    ctx.stroke()
    for angle_deg in [20, 45, 70, 95]:
        rad = math.radians(angle_deg)
        fx = ra_hand[0] + math.cos(rad) * hand_r_s * 1.2
        fy = ra_hand[1] - math.sin(rad) * hand_r_s * 1.0
        ctx.new_path()
        ctx.move_to(ra_hand[0] + math.cos(rad) * hand_r_s * 0.6,
                    ra_hand[1] - math.sin(rad) * hand_r_s * 0.5)
        ctx.line_to(fx, fy)
        set_color(ctx, LINE_COL)
        ctx.set_line_width(lw_accent)
        ctx.stroke()


def draw_arm_fist_forward(ctx, ls_pt, s, hoodie, lw_major, lw_minor, lw_accent, arm_w_top, arm_w_bot, hand_r_s):
    """DETERMINED: left arm crosses body slightly, hand forward with fist."""
    la_shoulder = (ls_pt[0] + 8*s, ls_pt[1] + 6*s)
    la_elbow = (la_shoulder[0] + 12*s, la_shoulder[1] + 30*s)
    la_hand = (la_elbow[0] + 18*s, la_elbow[1] + 8*s)
    upper = bezier_points(la_shoulder,
                          (la_shoulder[0] + 4*s, la_shoulder[1] + 10*s),
                          (la_elbow[0] - 2*s, la_elbow[1] - 8*s),
                          la_elbow, steps=25)
    fore = bezier_points(la_elbow,
                         (la_elbow[0] + 6*s, la_elbow[1] + 4*s),
                         (la_hand[0] - 4*s, la_hand[1] - 2*s),
                         la_hand, steps=25)
    draw_variable_stroke_limb(ctx, upper, arm_w_top, arm_w_bot * 1.1, hoodie, LINE_COL, lw_major)
    draw_variable_stroke_limb(ctx, fore, arm_w_bot * 1.1, arm_w_bot, hoodie, LINE_COL, lw_major)
    # Fist
    draw_ellipse_path(ctx, la_hand[0], la_hand[1], hand_r_s * 0.85, hand_r_s * 0.85)
    set_color(ctx, SKIN)
    ctx.fill_preserve()
    set_color(ctx, LINE_COL)
    ctx.set_line_width(lw_minor)
    ctx.stroke()
    # Knuckle line
    ctx.new_path()
    ctx.move_to(la_hand[0] - hand_r_s * 0.4, la_hand[1] - hand_r_s * 0.3)
    ctx.curve_to(la_hand[0], la_hand[1] - hand_r_s * 0.5,
                 la_hand[0] + hand_r_s * 0.3, la_hand[1] - hand_r_s * 0.3,
                 la_hand[0] + hand_r_s * 0.5, la_hand[1] - hand_r_s * 0.1)
    set_color(ctx, SKIN_SH)
    ctx.set_line_width(lw_accent)
    ctx.stroke()


def draw_arm_fist_hip(ctx, rs_pt, s, hoodie, lw_major, lw_minor, lw_accent, arm_w_top, arm_w_bot, hand_r_s):
    """DETERMINED: right arm in fist at hip level, elbow bent back."""
    ra_shoulder = (rs_pt[0] - 8*s, rs_pt[1] + 6*s)
    ra_elbow = (ra_shoulder[0] + 25*s, ra_shoulder[1] + 22*s)
    ra_hand = (ra_elbow[0] + 5*s, ra_elbow[1] + 20*s)
    upper = bezier_points(ra_shoulder,
                          (ra_shoulder[0] + 10*s, ra_shoulder[1] + 8*s),
                          (ra_elbow[0] - 5*s, ra_elbow[1] - 6*s),
                          ra_elbow, steps=25)
    fore = bezier_points(ra_elbow,
                         (ra_elbow[0] + 3*s, ra_elbow[1] + 6*s),
                         (ra_hand[0] - 2*s, ra_hand[1] - 5*s),
                         ra_hand, steps=25)
    draw_variable_stroke_limb(ctx, upper, arm_w_top, arm_w_bot * 1.1, hoodie, LINE_COL, lw_major)
    draw_variable_stroke_limb(ctx, fore, arm_w_bot * 1.1, arm_w_bot, hoodie, LINE_COL, lw_major)
    # Tight fist
    draw_ellipse_path(ctx, ra_hand[0], ra_hand[1], hand_r_s * 0.8, hand_r_s * 0.8)
    set_color(ctx, SKIN)
    ctx.fill_preserve()
    set_color(ctx, LINE_COL)
    ctx.set_line_width(lw_minor)
    ctx.stroke()


def draw_arm_self_hold_grip(ctx, ls_pt, torso_cx, torso_cy, s, hoodie, lw_major, lw_minor, lw_accent, arm_w_top, arm_w_bot, hand_r_s):
    """WORRIED: left arm crosses body, hand gripping opposite elbow."""
    la_shoulder = (ls_pt[0] + 8*s, ls_pt[1] + 5*s)
    la_elbow = (la_shoulder[0] + 22*s, la_shoulder[1] + 28*s)
    la_hand = (torso_cx + 18*s, torso_cy + 5*s)  # gripping right elbow area
    upper = bezier_points(la_shoulder,
                          (la_shoulder[0] + 6*s, la_shoulder[1] + 10*s),
                          (la_elbow[0] - 4*s, la_elbow[1] - 6*s),
                          la_elbow, steps=25)
    fore = bezier_points(la_elbow,
                         (la_elbow[0] + 8*s, la_elbow[1] + 6*s),
                         (la_hand[0] - 4*s, la_hand[1] - 4*s),
                         la_hand, steps=25)
    draw_variable_stroke_limb(ctx, upper, arm_w_top, arm_w_bot * 1.1, hoodie, LINE_COL, lw_major)
    draw_variable_stroke_limb(ctx, fore, arm_w_bot * 1.1, arm_w_bot, hoodie, LINE_COL, lw_major)
    draw_ellipse_path(ctx, la_hand[0], la_hand[1], hand_r_s * 0.85, hand_r_s * 0.7)
    set_color(ctx, SKIN)
    ctx.fill_preserve()
    set_color(ctx, LINE_COL)
    ctx.set_line_width(lw_minor)
    ctx.stroke()


def draw_arm_self_hold_cross(ctx, rs_pt, torso_cx, torso_cy, s, hoodie, lw_major, lw_minor, lw_accent, arm_w_top, arm_w_bot, hand_r_s):
    """WORRIED: right arm crosses body, hand near left wrist."""
    ra_shoulder = (rs_pt[0] - 8*s, rs_pt[1] + 5*s)
    ra_elbow = (ra_shoulder[0] - 5*s, ra_shoulder[1] + 26*s)
    ra_hand = (torso_cx + 10*s, torso_cy + 12*s)
    upper = bezier_points(ra_shoulder,
                          (ra_shoulder[0] - 3*s, ra_shoulder[1] + 10*s),
                          (ra_elbow[0] + 2*s, ra_elbow[1] - 6*s),
                          ra_elbow, steps=25)
    fore = bezier_points(ra_elbow,
                         (ra_elbow[0] + 2*s, ra_elbow[1] + 8*s),
                         (ra_hand[0] - 3*s, ra_hand[1] - 4*s),
                         ra_hand, steps=25)
    draw_variable_stroke_limb(ctx, upper, arm_w_top, arm_w_bot * 1.1, hoodie, LINE_COL, lw_major)
    draw_variable_stroke_limb(ctx, fore, arm_w_bot * 1.1, arm_w_bot, hoodie, LINE_COL, lw_major)
    draw_ellipse_path(ctx, ra_hand[0], ra_hand[1], hand_r_s * 0.8, hand_r_s * 0.65)
    set_color(ctx, SKIN)
    ctx.fill_preserve()
    set_color(ctx, LINE_COL)
    ctx.set_line_width(lw_minor)
    ctx.stroke()


def draw_arm_celebration_high(ctx, ls_pt, s, hoodie, lw_major, lw_minor, lw_accent, arm_w_top, arm_w_bot, hand_r_s):
    """DELIGHTED: left arm fully extended upward, fingers spread (amplified)."""
    la_shoulder = (ls_pt[0] + 8*s, ls_pt[1] + 4*s)
    la_elbow = (la_shoulder[0] - 28*s, la_shoulder[1] - 55*s)
    la_hand = (la_elbow[0] - 15*s, la_elbow[1] - 48*s)
    upper = bezier_points(la_shoulder,
                          (la_shoulder[0] - 8*s, la_shoulder[1] - 12*s),
                          (la_elbow[0] + 4*s, la_elbow[1] + 10*s),
                          la_elbow, steps=25)
    fore = bezier_points(la_elbow,
                         (la_elbow[0] - 4*s, la_elbow[1] - 10*s),
                         (la_hand[0] + 3*s, la_hand[1] + 8*s),
                         la_hand, steps=25)
    draw_variable_stroke_limb(ctx, upper, arm_w_top, arm_w_bot * 1.1, hoodie, LINE_COL, lw_major)
    draw_variable_stroke_limb(ctx, fore, arm_w_bot * 1.1, arm_w_bot, hoodie, LINE_COL, lw_major)
    draw_ellipse_path(ctx, la_hand[0], la_hand[1], hand_r_s * 1.0, hand_r_s * 0.85)
    set_color(ctx, SKIN)
    ctx.fill_preserve()
    set_color(ctx, LINE_COL)
    ctx.set_line_width(lw_minor)
    ctx.stroke()
    # Spread fingers (joy!)
    for angle_deg in [-50, -25, 0, 25, 50]:
        rad = math.radians(angle_deg - 90)
        fx = la_hand[0] + math.cos(rad) * hand_r_s * 1.4
        fy = la_hand[1] + math.sin(rad) * hand_r_s * 1.2
        ctx.new_path()
        ctx.move_to(la_hand[0] + math.cos(rad) * hand_r_s * 0.5,
                    la_hand[1] + math.sin(rad) * hand_r_s * 0.4)
        ctx.line_to(fx, fy)
        set_color(ctx, SKIN)
        ctx.set_line_width(2.5*s)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.stroke()
        ctx.new_path()
        ctx.move_to(la_hand[0] + math.cos(rad) * hand_r_s * 0.5,
                    la_hand[1] + math.sin(rad) * hand_r_s * 0.4)
        ctx.line_to(fx, fy)
        set_color(ctx, LINE_COL)
        ctx.set_line_width(lw_accent)
        ctx.stroke()


def draw_arm_celebration_pump(ctx, rs_pt, s, hoodie, lw_major, lw_minor, lw_accent, arm_w_top, arm_w_bot, hand_r_s):
    """DELIGHTED: right arm bent, fist pump celebration (amplified)."""
    ra_shoulder = (rs_pt[0] - 6*s, rs_pt[1] + 4*s)
    ra_elbow = (ra_shoulder[0] + 30*s, ra_shoulder[1] - 38*s)
    ra_hand = (ra_elbow[0] + 10*s, ra_elbow[1] - 30*s)
    upper = bezier_points(ra_shoulder,
                          (ra_shoulder[0] + 8*s, ra_shoulder[1] - 8*s),
                          (ra_elbow[0] - 4*s, ra_elbow[1] + 8*s),
                          ra_elbow, steps=25)
    fore = bezier_points(ra_elbow,
                         (ra_elbow[0] + 3*s, ra_elbow[1] - 6*s),
                         (ra_hand[0] - 2*s, ra_hand[1] + 5*s),
                         ra_hand, steps=25)
    draw_variable_stroke_limb(ctx, upper, arm_w_top, arm_w_bot * 1.1, hoodie, LINE_COL, lw_major)
    draw_variable_stroke_limb(ctx, fore, arm_w_bot * 1.1, arm_w_bot, hoodie, LINE_COL, lw_major)
    # Tight celebration fist
    draw_ellipse_path(ctx, ra_hand[0], ra_hand[1], hand_r_s * 0.85, hand_r_s * 0.85)
    set_color(ctx, SKIN)
    ctx.fill_preserve()
    set_color(ctx, LINE_COL)
    ctx.set_line_width(lw_minor)
    ctx.stroke()


def draw_arm_flung_down_wide(ctx, ls_pt, s, hoodie, lw_major, lw_minor, lw_accent, arm_w_top, arm_w_bot, hand_r_s):
    """FRUSTRATED: left arm slams DOWN close to body (not wide — differentiates from SURPRISED)."""
    la_shoulder = (ls_pt[0] + 8*s, ls_pt[1] + 5*s)
    la_elbow = (la_shoulder[0] - 15*s, la_shoulder[1] + 38*s)
    la_hand = (la_elbow[0] - 8*s, la_elbow[1] + 48*s)
    upper = bezier_points(la_shoulder,
                          (la_shoulder[0] - 14*s, la_shoulder[1] + 6*s),
                          (la_elbow[0] + 8*s, la_elbow[1] - 4*s),
                          la_elbow, steps=25)
    fore = bezier_points(la_elbow,
                         (la_elbow[0] - 10*s, la_elbow[1] + 8*s),
                         (la_hand[0] + 6*s, la_hand[1] - 6*s),
                         la_hand, steps=25)
    draw_variable_stroke_limb(ctx, upper, arm_w_top, arm_w_bot * 1.1, hoodie, LINE_COL, lw_major)
    draw_variable_stroke_limb(ctx, fore, arm_w_bot * 1.1, arm_w_bot, hoodie, LINE_COL, lw_major)
    # Open hand, fingers spread in exasperation
    draw_ellipse_path(ctx, la_hand[0], la_hand[1], hand_r_s * 1.0, hand_r_s * 0.85)
    set_color(ctx, SKIN)
    ctx.fill_preserve()
    set_color(ctx, LINE_COL)
    ctx.set_line_width(lw_minor)
    ctx.stroke()
    for angle_deg in [110, 135, 160, 185]:
        rad = math.radians(angle_deg)
        fx = la_hand[0] + math.cos(rad) * hand_r_s * 1.3
        fy = la_hand[1] - math.sin(rad) * hand_r_s * 1.1
        ctx.new_path()
        ctx.move_to(la_hand[0] + math.cos(rad) * hand_r_s * 0.5,
                    la_hand[1] - math.sin(rad) * hand_r_s * 0.4)
        ctx.line_to(fx, fy)
        set_color(ctx, LINE_COL)
        ctx.set_line_width(lw_accent)
        ctx.stroke()


def draw_arm_hair_pull(ctx, rs_pt, head_cx, head_cy, head_r, s, hoodie, lw_major, lw_minor, lw_accent, arm_w_top, arm_w_bot, hand_r_s):
    """FRUSTRATED: right arm crosses body tightly, fist clenched at chest (compact, not raised)."""
    ra_shoulder = (rs_pt[0] - 6*s, rs_pt[1] + 5*s)
    # Arm crosses to LEFT side of chest — tight, frustrated self-grip
    ra_elbow = (ra_shoulder[0] - 10*s, ra_shoulder[1] + 25*s)
    ra_hand = (ra_elbow[0] - 12*s, ra_elbow[1] + 15*s)  # low, tight to body
    upper = bezier_points(ra_shoulder,
                          (ra_shoulder[0] + 5*s, ra_shoulder[1] - 6*s),
                          (ra_elbow[0] - 3*s, ra_elbow[1] + 6*s),
                          ra_elbow, steps=25)
    fore = bezier_points(ra_elbow,
                         (ra_elbow[0] + 4*s, ra_elbow[1] - 6*s),
                         (ra_hand[0] - 4*s, ra_hand[1] + 6*s),
                         ra_hand, steps=25)
    draw_variable_stroke_limb(ctx, upper, arm_w_top, arm_w_bot * 1.1, hoodie, LINE_COL, lw_major)
    draw_variable_stroke_limb(ctx, fore, arm_w_bot * 1.1, arm_w_bot, hoodie, LINE_COL, lw_major)
    # Gripping hand on head
    draw_ellipse_path(ctx, ra_hand[0], ra_hand[1], hand_r_s * 0.9, hand_r_s * 0.75)
    set_color(ctx, SKIN)
    ctx.fill_preserve()
    set_color(ctx, LINE_COL)
    ctx.set_line_width(lw_minor)
    ctx.stroke()
    # Grabbing lines
    for dx, dy in [(-4*s, -5*s), (2*s, -6*s), (6*s, -3*s)]:
        ctx.new_path()
        ctx.move_to(ra_hand[0] + dx * 0.3, ra_hand[1] + dy * 0.3)
        ctx.line_to(ra_hand[0] + dx, ra_hand[1] + dy)
        set_color(ctx, SKIN_SH)
        ctx.set_line_width(lw_accent)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.stroke()


# ── Main Drawing Function ───────────────────────────────────────────────────

def draw_arms(ctx, expression, spec, ls_pt, rs_pt, head_cx, head_cy, head_r, torso_cx, torso_cy, s, hoodie, lw_major, lw_minor, lw_accent, arm_w_top, arm_w_bot, hand_r_s):
    """Dispatch arm drawing by expression spec."""
    la = spec["left_arm"]
    ra = spec["right_arm"]

    # Left arm
    if la == "forward_reaching":
        draw_arm_forward_reaching(ctx, ls_pt, head_cx, head_r, s, hoodie, lw_major, lw_minor, lw_accent, arm_w_top, arm_w_bot, hand_r_s)
    elif la == "defensive_high":
        draw_arm_defensive_high(ctx, ls_pt, s, hoodie, lw_major, lw_minor, lw_accent, arm_w_top, arm_w_bot, hand_r_s)
    elif la == "fist_forward":
        draw_arm_fist_forward(ctx, ls_pt, s, hoodie, lw_major, lw_minor, lw_accent, arm_w_top, arm_w_bot, hand_r_s)
    elif la == "self_hold_grip":
        draw_arm_self_hold_grip(ctx, ls_pt, torso_cx, torso_cy, s, hoodie, lw_major, lw_minor, lw_accent, arm_w_top, arm_w_bot, hand_r_s)
    elif la == "celebration_high":
        draw_arm_celebration_high(ctx, ls_pt, s, hoodie, lw_major, lw_minor, lw_accent, arm_w_top, arm_w_bot, hand_r_s)
    elif la == "flung_down_wide":
        draw_arm_flung_down_wide(ctx, ls_pt, s, hoodie, lw_major, lw_minor, lw_accent, arm_w_top, arm_w_bot, hand_r_s)

    # Right arm
    if ra == "chin_touch":
        draw_arm_chin_touch(ctx, rs_pt, head_cx, head_cy, head_r, s, hoodie, lw_major, lw_minor, lw_accent, arm_w_top, arm_w_bot, hand_r_s)
    elif ra == "flung_back":
        draw_arm_flung_back(ctx, rs_pt, s, hoodie, lw_major, lw_minor, lw_accent, arm_w_top, arm_w_bot, hand_r_s)
    elif ra == "fist_hip":
        draw_arm_fist_hip(ctx, rs_pt, s, hoodie, lw_major, lw_minor, lw_accent, arm_w_top, arm_w_bot, hand_r_s)
    elif ra == "self_hold_cross":
        draw_arm_self_hold_cross(ctx, rs_pt, torso_cx, torso_cy, s, hoodie, lw_major, lw_minor, lw_accent, arm_w_top, arm_w_bot, hand_r_s)
    elif ra == "celebration_pump":
        draw_arm_celebration_pump(ctx, rs_pt, s, hoodie, lw_major, lw_minor, lw_accent, arm_w_top, arm_w_bot, hand_r_s)
    elif ra == "hair_pull":
        draw_arm_hair_pull(ctx, rs_pt, head_cx, head_cy, head_r, s, hoodie, lw_major, lw_minor, lw_accent, arm_w_top, arm_w_bot, hand_r_s)


def draw_luma_expression(ctx, cx, ground_y, char_h, expression, spec, scale=1.0):
    """Draw Luma in the given expression using cairo.

    Args:
        ctx: cairo context
        cx: horizontal center of character
        ground_y: Y position of ground plane
        char_h: total character height in pixels
        expression: name string
        spec: gesture spec dict
        scale: additional scale factor
    """
    rng = random.Random(SEED + hash(expression))

    # ── Proportions ──
    head_h = char_h * 0.37
    head_r = head_h / 2
    body_h = char_h - head_h
    s = head_r / 100.0  # scale factor for details

    # Line weights (variable-width stroke hierarchy)
    lw_silhouette = max(4.0, 5.0 * s)
    lw_major = max(3.0, 3.5 * s)
    lw_minor = max(2.0, 2.5 * s)
    lw_accent = max(1.5, 2.0 * s)

    # ── Offset Chain (Lee's gesture spec) ──
    hip_shift = spec["hip_shift"] * s
    shoulder_offset = spec["shoulder_offset"] * s
    head_offset = spec["head_offset"] * s
    torso_lean = spec["torso_lean"] * s

    hip_cx = cx + hip_shift
    torso_cx = hip_cx + shoulder_offset
    head_cx = torso_cx + head_offset

    # ── Vertical layout ──
    head_cy = ground_y - char_h + head_r
    neck_bot_y = head_cy + head_r + head_r * 0.25
    torso_h = body_h * 0.38
    torso_cy = neck_bot_y + torso_h / 2
    torso_bot_y = neck_bot_y + torso_h
    leg_h = ground_y - torso_bot_y

    # Hip and shoulder tilt in pixels
    hip_tilt_px = spec["hip_tilt"] * s * 0.8
    shoulder_tilt_px = spec["shoulder_tilt"] * s * 0.8

    # Shoulder widths
    sh_w = head_r * 0.80

    # Hoodie color by expression
    hoodie, hoodie_sh = HOODIE_COLORS.get(expression, (HOODIE_SURPRISED, HOODIE_SURPRISED_SH))

    # ══════════════════════════════════════════════════════════════════════
    # LEGS — Draw first (behind torso)
    # ══════════════════════════════════════════════════════════════════════
    leg_offset = head_r * 0.45
    # Wide stance for DETERMINED
    stance_mult = spec.get("stance_wide", 1.0)
    leg_offset *= stance_mult

    leg_w_top = head_r * 0.22
    leg_w_bot = head_r * 0.18

    weight_front = spec["weight_front"]
    front_foot_lift = spec["front_foot_lift"] * s
    back_foot_lift = spec["back_foot_lift"] * s
    heel_lift = spec.get("heel_lift", 0) * s  # DELIGHTED tiptoe

    front_leg_x = hip_cx - leg_offset * (1.0 if weight_front > 0.5 else 0.7)
    back_leg_x = hip_cx + leg_offset * (1.0 if weight_front <= 0.5 else 0.7)

    # Front leg
    fl_top = (front_leg_x, torso_bot_y)
    fl_knee = (front_leg_x - 3 * s, torso_bot_y + leg_h * 0.48)
    fl_ankle = (front_leg_x + 2 * s, ground_y - front_foot_lift - heel_lift - head_r * 0.25)
    front_leg_pts = bezier_points(fl_top, fl_knee,
                                   (fl_knee[0] + 2*s, fl_knee[1] + leg_h * 0.2),
                                   fl_ankle, steps=30)
    draw_variable_stroke_limb(ctx, front_leg_pts, leg_w_top, leg_w_bot,
                               PANTS, LINE_COL, lw_major)

    # Back leg
    bl_top = (back_leg_x, torso_bot_y)
    bl_knee = (back_leg_x + 2 * s, torso_bot_y + leg_h * 0.50)
    bl_ankle = (back_leg_x + 1 * s, ground_y - back_foot_lift - heel_lift - head_r * 0.25)
    back_leg_pts = bezier_points(bl_top, bl_knee,
                                  (bl_knee[0] - 1*s, bl_knee[1] + leg_h * 0.2),
                                  bl_ankle, steps=30)
    draw_variable_stroke_limb(ctx, back_leg_pts, leg_w_top, leg_w_bot,
                               PANTS, LINE_COL, lw_major)

    # Pants shadow (inseam)
    for leg_pts in [front_leg_pts, back_leg_pts]:
        n = len(leg_pts)
        shadow_pts = []
        for i in range(n):
            t = i / max(1, n-1)
            w = (leg_w_top + (leg_w_bot - leg_w_top) * t) * 0.3
            shadow_pts.append((leg_pts[i][0] + w * 0.5, leg_pts[i][1]))
        if len(shadow_pts) > 2:
            ctx.new_path()
            ctx.move_to(*shadow_pts[0])
            for p in shadow_pts[1:]:
                ctx.line_to(*p)
            set_color(ctx, PANTS_SH, 0.5)
            ctx.set_line_width(leg_w_bot * 1.5)
            ctx.set_line_cap(cairo.LINE_CAP_ROUND)
            ctx.stroke()

    # ── Shoes ──
    shoe_w = head_r * 0.32
    shoe_h = head_r * 0.18
    for foot_x, foot_y, foot_angle in [
        (front_leg_pts[-1][0], ground_y - front_foot_lift - heel_lift, spec["front_foot_angle"]),
        (back_leg_pts[-1][0], ground_y - back_foot_lift - heel_lift, spec["back_foot_angle"])
    ]:
        ctx.save()
        ctx.translate(foot_x, foot_y - shoe_h * 0.3)
        ctx.rotate(math.radians(foot_angle))
        draw_ellipse_path(ctx, 0, 0, shoe_w, shoe_h)
        set_color(ctx, SHOE)
        ctx.fill_preserve()
        set_color(ctx, LINE_COL)
        ctx.set_line_width(lw_major)
        ctx.stroke()
        # Sole line
        ctx.new_path()
        ctx.move_to(-shoe_w * 0.8, shoe_h * 0.4)
        ctx.curve_to(-shoe_w * 0.3, shoe_h * 0.7, shoe_w * 0.3, shoe_h * 0.7,
                     shoe_w * 0.8, shoe_h * 0.3)
        set_color(ctx, SHOE_SOLE)
        ctx.set_line_width(lw_minor)
        ctx.stroke()
        # Lace dot
        ctx.new_path()
        ctx.arc(0, -shoe_h * 0.2, 2 * s, 0, 2 * math.pi)
        set_color(ctx, LACES)
        ctx.fill()
        ctx.restore()

    # ══════════════════════════════════════════════════════════════════════
    # TORSO — Bean shape with cairo beziers
    # ══════════════════════════════════════════════════════════════════════
    w_top = sh_w
    w_bot = head_r * 0.55
    attach = draw_bean_torso(ctx, torso_cx, torso_cy, w_top, w_bot, torso_h,
                              torso_lean, hip_tilt_px, shoulder_tilt_px)
    ls_pt, rs_pt, lh_pt, rh_pt = attach
    set_color(ctx, hoodie)
    ctx.fill_preserve()
    set_color(ctx, LINE_COL)
    ctx.set_line_width(lw_silhouette)
    ctx.stroke()

    # Form shadow on torso (diagonal band)
    shadow_x1 = torso_cx + torso_lean + sh_w * 0.2
    shadow_y1 = torso_cy - torso_h / 2
    shadow_x2 = torso_cx + torso_lean * 0.5 - w_bot * 0.1
    shadow_y2 = torso_cy + torso_h / 2
    ctx.new_path()
    ctx.move_to(shadow_x1, shadow_y1)
    ctx.curve_to(shadow_x1 + sh_w * 0.3, shadow_y1 + torso_h * 0.3,
                 shadow_x2 + w_bot * 0.4, shadow_y2 - torso_h * 0.2,
                 shadow_x2, shadow_y2)
    ctx.line_to(torso_cx + torso_lean * 0.5 + w_bot, shadow_y2)
    ctx.curve_to(torso_cx + torso_lean + sh_w * 0.5, shadow_y2 - torso_h * 0.3,
                 shadow_x1 + sh_w * 0.5, shadow_y1 + torso_h * 0.2,
                 torso_cx + torso_lean + sh_w, shadow_y1)
    ctx.close_path()
    set_color(ctx, hoodie_sh, 0.5)
    ctx.fill()

    # Collar V-neck
    collar_cx = torso_cx + torso_lean
    collar_y = torso_cy - torso_h / 2
    collar_w = head_r * 0.30
    ctx.new_path()
    ctx.move_to(collar_cx - collar_w, collar_y + 2 * s)
    ctx.curve_to(collar_cx - collar_w * 0.3, collar_y + 14 * s,
                 collar_cx + collar_w * 0.3, collar_y + 14 * s,
                 collar_cx + collar_w, collar_y + 2 * s)
    set_color(ctx, (250/255, 232/255, 200/255))
    ctx.set_line_width(max(5, 6 * s))
    ctx.stroke_preserve()
    set_color(ctx, LINE_COL)
    ctx.set_line_width(lw_minor)
    ctx.stroke()

    # Hoodie hem
    hem_y = torso_bot_y - torso_h * 0.10
    ctx.new_path()
    ctx.move_to(lh_pt[0] + 3*s, hem_y)
    ctx.curve_to(hip_cx - w_bot * 0.3, hem_y + 4*s,
                 hip_cx + w_bot * 0.3, hem_y + 4*s,
                 rh_pt[0] - 3*s, hem_y)
    set_color(ctx, hoodie_sh)
    ctx.set_line_width(max(3, 4 * s))
    ctx.stroke()

    # Pixel accents on hoodie
    for _ in range(12):
        px_x = torso_cx + torso_lean + rng.uniform(-18*s, 18*s)
        px_y = torso_cy + rng.uniform(-12*s, 12*s)
        psz = max(2, rng.choice([2*s, 3*s, 4*s]))
        pc = rng.choice([PX_CYAN, PX_MAG, (0.94, 0.94, 0.94)])
        ctx.rectangle(px_x, px_y, psz, psz)
        set_color(ctx, pc)
        ctx.fill()

    # ══════════════════════════════════════════════════════════════════════
    # ARMS — Expression-specific poses
    # ══════════════════════════════════════════════════════════════════════
    arm_w_top = head_r * 0.14
    arm_w_bot = head_r * 0.10
    hand_r_s = head_r * 0.12

    draw_arms(ctx, expression, spec, ls_pt, rs_pt, head_cx, head_cy, head_r,
              torso_cx, torso_cy, s, hoodie, lw_major, lw_minor, lw_accent,
              arm_w_top, arm_w_bot, hand_r_s)

    # ══════════════════════════════════════════════════════════════════════
    # NECK — Organic taper
    # ══════════════════════════════════════════════════════════════════════
    neck_top_y = head_cy + head_r * 0.95
    neck_w_top = head_r * 0.22
    neck_w_bot = head_r * 0.30
    neck_lean = (torso_cx - head_cx) * 0.5

    ctx.new_path()
    ctx.move_to(head_cx - neck_w_top, neck_top_y)
    ctx.curve_to(head_cx - neck_w_top - 2*s, (neck_top_y + neck_bot_y) / 2,
                 torso_cx + torso_lean - neck_w_bot - 1*s, neck_bot_y - 3*s,
                 torso_cx + torso_lean - neck_w_bot, neck_bot_y)
    ctx.line_to(torso_cx + torso_lean + neck_w_bot, neck_bot_y)
    ctx.curve_to(torso_cx + torso_lean + neck_w_bot + 1*s, neck_bot_y - 3*s,
                 head_cx + neck_w_top + 2*s, (neck_top_y + neck_bot_y) / 2,
                 head_cx + neck_w_top, neck_top_y)
    ctx.close_path()
    set_color(ctx, SKIN)
    ctx.fill_preserve()
    set_color(ctx, LINE_COL)
    ctx.set_line_width(lw_minor)
    ctx.stroke()

    # ══════════════════════════════════════════════════════════════════════
    # HEAD — Organic shape with chin and cheek modulation
    # ══════════════════════════════════════════════════════════════════════
    head_rx = head_r * 1.06
    head_ry = head_r

    tilt_rad = math.radians(spec["head_tilt"])

    ctx.save()
    ctx.translate(head_cx, head_cy)
    ctx.rotate(tilt_rad)

    # Build organic head path
    ctx.new_path()
    steps = 100
    for i in range(steps):
        angle = i * 2 * math.pi / steps
        rx = head_rx
        ry = head_ry
        chin_f = max(0, math.cos(angle - math.pi / 2)) ** 2.5
        ry += head_r * 0.10 * chin_f
        rx -= head_r * 0.04 * chin_f
        for sign in [1, -1]:
            cheek_f = max(0, math.cos(angle - sign * 0.4)) ** 6
            rx += head_r * 0.04 * cheek_f
        px = rx * math.cos(angle)
        py = ry * math.sin(angle)
        if i == 0:
            ctx.move_to(px, py)
        else:
            ctx.line_to(px, py)
    ctx.close_path()
    set_color(ctx, SKIN)
    ctx.fill_preserve()
    ctx.set_line_width(lw_silhouette)
    set_color(ctx, LINE_COL)
    ctx.stroke()

    # ── Hair: cloud of overlapping ellipses ──
    hair_blobs = [
        (0, -0.65, 0.70, 0.55),
        (-0.50, -0.50, 0.55, 0.50),
        (0.50, -0.50, 0.55, 0.50),
        (-0.30, -0.95, 0.40, 0.35),
        (0.30, -0.95, 0.40, 0.35),
        (0, -1.10, 0.35, 0.30),
        (-0.85, -0.30, 0.35, 0.38),
        (0.85, -0.30, 0.35, 0.38),
        (-0.70, -0.60, 0.35, 0.32),
        (0.70, -0.60, 0.35, 0.32),
        (-0.15, -0.45, 0.60, 0.42),
        (0.15, -0.45, 0.60, 0.42),
        (-0.50, -0.80, 0.32, 0.28),
        (0.50, -0.80, 0.32, 0.28),
        (-0.45, -1.05, 0.25, 0.22),
        (0.45, -1.05, 0.25, 0.22),
        (0.15, -1.15, 0.22, 0.20),
    ]
    for (bx, by, brx, bry) in hair_blobs:
        hcx = bx * head_rx
        hcy = by * head_ry
        hrx = brx * head_rx
        hry = bry * head_ry
        draw_ellipse_path(ctx, hcx, hcy, hrx, hry)
        set_color(ctx, HAIR)
        ctx.fill()

    # Hair highlights
    for (bx, by, brx, bry) in [(-0.30, -0.85, 0.22, 0.13),
                                 (0.20, -0.72, 0.16, 0.10),
                                 (-0.55, -0.55, 0.14, 0.10)]:
        hcx = bx * head_rx
        hcy = by * head_ry
        hrx = brx * head_rx
        hry = bry * head_ry
        draw_ellipse_path(ctx, hcx, hcy, hrx, hry)
        set_color(ctx, HAIR_HL)
        ctx.fill()

    # Redraw face area (skin over bottom hair)
    face_cy_off = head_r * 0.10
    face_rx = head_rx * 0.88
    face_ry = head_ry * 0.70
    draw_ellipse_path(ctx, 0, face_cy_off, face_rx, face_ry)
    set_color(ctx, SKIN)
    ctx.fill()

    # ── EYES ──
    eye_spacing = head_rx * 0.40
    eye_y = head_r * 0.05
    eye_rx = head_rx * 0.28
    eye_ry = head_ry * 0.32 * spec["eye_openness"]

    for side in [-1, 1]:
        ex = side * eye_spacing
        ey = eye_y

        draw_ellipse_path(ctx, ex, ey, eye_rx, eye_ry)
        set_color(ctx, EYE_W)
        ctx.fill_preserve()
        set_color(ctx, LINE_COL)
        ctx.set_line_width(lw_minor)
        ctx.stroke()

        # Upper lid emphasis
        ctx.new_path()
        for i in range(30):
            a = math.radians(195 + 150 * i / 29)
            px = ex + eye_rx * 1.01 * math.cos(a)
            py = ey + eye_ry * 0.97 * math.sin(a)
            if i == 0:
                ctx.move_to(px, py)
            else:
                ctx.line_to(px, py)
        set_color(ctx, LINE_COL)
        ctx.set_line_width(lw_silhouette)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.stroke()

        # Lower lash
        ctx.new_path()
        for i in range(20):
            a = math.radians(15 + 150 * i / 19)
            px = ex + eye_rx * 0.98 * math.cos(a)
            py = ey + eye_ry * 1.01 * math.sin(a)
            if i == 0:
                ctx.move_to(px, py)
            else:
                ctx.line_to(px, py)
        set_color(ctx, LINE_COL)
        ctx.set_line_width(lw_minor)
        ctx.stroke()

        # Iris
        gaze_dx = spec["gaze_dx"] * s
        gaze_dy = spec["gaze_dy"] * s
        iris_r = eye_rx * 0.68
        iris_ry = eye_ry * 0.62
        iris_cx = ex + gaze_dx
        iris_cy = ey + gaze_dy

        draw_ellipse_path(ctx, iris_cx, iris_cy, iris_r, iris_ry)
        set_color(ctx, EYE_IRIS)
        ctx.fill()

        # Pupil
        pup_r = iris_r * 0.52
        pup_ry = iris_ry * 0.52
        draw_ellipse_path(ctx, iris_cx, iris_cy, pup_r, pup_ry)
        set_color(ctx, EYE_PUP)
        ctx.fill()

        # Highlight dots
        hl_r = max(pup_r * 0.42, 3)
        hl_x = iris_cx + iris_r * 0.32
        hl_y = iris_cy - iris_ry * 0.32
        ctx.new_path()
        ctx.arc(hl_x, hl_y, hl_r, 0, 2 * math.pi)
        set_color(ctx, EYE_HL)
        ctx.fill()
        hl2_r = max(hl_r * 0.45, 2)
        ctx.new_path()
        ctx.arc(iris_cx - iris_r * 0.22, iris_cy + iris_ry * 0.18,
                hl2_r, 0, 2 * math.pi)
        set_color(ctx, (0.94, 0.94, 0.94))
        ctx.fill()

    # ── Brows ──
    for side, lift in [(-1, spec["brow_lift_l"] * s), (1, spec["brow_lift_r"] * s)]:
        bx = side * eye_spacing
        by = eye_y - eye_ry - 6*s - lift
        inner_x = bx + side * 18*s
        outer_x = bx - side * 20*s
        ctx.new_path()
        ctx.move_to(outer_x, by + 4*s)
        ctx.curve_to((outer_x + bx) / 2, by - 4*s,
                     (bx + inner_x) / 2, by - 2*s,
                     inner_x, by + 2*s)
        set_color(ctx, HAIR)
        ctx.set_line_width(lw_major)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.stroke()

    # ── Nose ──
    nose_y = head_r * 0.28
    ctx.new_path()
    ctx.move_to(-4*s, nose_y)
    ctx.curve_to(0, nose_y + 3*s, 2*s, nose_y + 1*s, 3*s, nose_y - 1*s)
    set_color(ctx, SKIN_SH)
    ctx.set_line_width(lw_minor)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.stroke()

    # ── Mouth ──
    mouth_y = head_r * 0.44
    mouth_w = head_rx * 0.30
    mouth_type = spec["mouth"]

    if mouth_type == "gentle_smile":
        ctx.new_path()
        ctx.move_to(-mouth_w, mouth_y + 1*s)
        ctx.curve_to(-mouth_w * 0.3, mouth_y - 6*s,
                     mouth_w * 0.3, mouth_y - 6*s,
                     mouth_w, mouth_y - 1*s)
        set_color(ctx, LINE_COL)
        ctx.set_line_width(lw_minor)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.stroke()
        ctx.new_path()
        ctx.move_to(-mouth_w, mouth_y + 1*s)
        ctx.line_to(-mouth_w - 2*s, mouth_y - 2*s)
        ctx.stroke()
        ctx.new_path()
        ctx.move_to(mouth_w, mouth_y - 1*s)
        ctx.line_to(mouth_w + 2*s, mouth_y - 3*s)
        ctx.stroke()

    elif mouth_type == "open_o":
        mouth_rx = mouth_w * 0.6
        mouth_ry = head_r * 0.12
        draw_ellipse_path(ctx, 0, mouth_y + 2*s, mouth_rx, mouth_ry)
        set_color(ctx, (0.15, 0.08, 0.06))
        ctx.fill_preserve()
        set_color(ctx, LINE_COL)
        ctx.set_line_width(lw_minor)
        ctx.stroke()

    elif mouth_type == "firm_line":
        # Determined: firm, slightly pursed line
        ctx.new_path()
        ctx.move_to(-mouth_w * 0.8, mouth_y)
        ctx.curve_to(-mouth_w * 0.2, mouth_y - 2*s,
                     mouth_w * 0.2, mouth_y - 2*s,
                     mouth_w * 0.8, mouth_y)
        set_color(ctx, LINE_COL)
        ctx.set_line_width(lw_major)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.stroke()

    elif mouth_type == "tight_frown":
        # Worried: downturned, tight
        ctx.new_path()
        ctx.move_to(-mouth_w * 0.7, mouth_y - 2*s)
        ctx.curve_to(-mouth_w * 0.2, mouth_y + 4*s,
                     mouth_w * 0.2, mouth_y + 4*s,
                     mouth_w * 0.7, mouth_y - 2*s)
        set_color(ctx, LINE_COL)
        ctx.set_line_width(lw_minor)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.stroke()
        # Downturn corners
        for sx in [-1, 1]:
            ctx.new_path()
            ctx.move_to(sx * mouth_w * 0.7, mouth_y - 2*s)
            ctx.line_to(sx * (mouth_w * 0.7 + 2*s), mouth_y + 1*s)
            ctx.stroke()

    elif mouth_type == "wide_grin":
        # Delighted: wide open grin
        mouth_rx = mouth_w * 0.85
        mouth_ry = head_r * 0.10
        # Dark interior
        draw_ellipse_path(ctx, 0, mouth_y + 1*s, mouth_rx, mouth_ry)
        set_color(ctx, (0.15, 0.08, 0.06))
        ctx.fill_preserve()
        set_color(ctx, LINE_COL)
        ctx.set_line_width(lw_minor)
        ctx.stroke()
        # Teeth line
        ctx.new_path()
        ctx.move_to(-mouth_rx * 0.7, mouth_y + 1*s)
        ctx.line_to(mouth_rx * 0.7, mouth_y + 1*s)
        set_color(ctx, EYE_W)
        ctx.set_line_width(3*s)
        ctx.stroke()
        # Upturn corners
        for sx in [-1, 1]:
            ctx.new_path()
            ctx.move_to(sx * mouth_rx, mouth_y + 1*s)
            ctx.line_to(sx * (mouth_rx + 3*s), mouth_y - 3*s)
            set_color(ctx, LINE_COL)
            ctx.set_line_width(lw_accent)
            ctx.stroke()

    elif mouth_type == "gritted_teeth":
        # Frustrated: bared gritted teeth
        mouth_rx = mouth_w * 0.65
        mouth_ry = head_r * 0.07
        draw_ellipse_path(ctx, 0, mouth_y + 2*s, mouth_rx, mouth_ry)
        set_color(ctx, (0.15, 0.08, 0.06))
        ctx.fill_preserve()
        set_color(ctx, LINE_COL)
        ctx.set_line_width(lw_minor)
        ctx.stroke()
        # Teeth grid
        for tx in range(-3, 4):
            ctx.new_path()
            ctx.move_to(tx * mouth_rx * 0.25, mouth_y + 2*s - mouth_ry * 0.8)
            ctx.line_to(tx * mouth_rx * 0.25, mouth_y + 2*s + mouth_ry * 0.8)
            set_color(ctx, EYE_W)
            ctx.set_line_width(1.5*s)
            ctx.stroke()
        # Downturn corners
        for sx in [-1, 1]:
            ctx.new_path()
            ctx.move_to(sx * mouth_rx, mouth_y + 2*s)
            ctx.line_to(sx * (mouth_rx + 2*s), mouth_y + 4*s)
            set_color(ctx, LINE_COL)
            ctx.set_line_width(lw_accent)
            ctx.stroke()

    # ── Blush ──
    for side in [-1, 1]:
        cheek_cx = side * eye_spacing * 0.85
        cheek_cy = head_r * 0.24
        draw_ellipse_path(ctx, cheek_cx, cheek_cy, 18*s, 10*s)
        set_color(ctx, BLUSH_C)
        ctx.fill()

    ctx.restore()  # End head tilt transform

    # ══════════════════════════════════════════════════════════════════════
    # GESTURE LINE OVERLAY
    # ══════════════════════════════════════════════════════════════════════
    ctx.save()
    ctx.set_dash([8*s, 4*s])
    ctx.set_line_width(2.0)
    set_color(ctx, (0.2, 0.6, 0.9, 0.35))
    ctx.new_path()
    g_head = (head_cx, head_cy - head_r * 0.5)
    g_neck = (head_cx + (torso_cx - head_cx) * 0.5, neck_bot_y * 0.7 + head_cy * 0.3)
    g_torso = (torso_cx + torso_lean * 0.5, torso_cy)
    g_hip = (hip_cx, torso_bot_y)
    g_foot = (hip_cx + hip_shift * 0.5, ground_y)
    ctx.move_to(*g_head)
    ctx.curve_to(*g_neck, *g_torso, *g_hip)
    ctx.line_to(*g_foot)
    ctx.stroke()
    ctx.set_dash([])
    ctx.restore()

    return {
        "head_cx": head_cx,
        "head_cy": head_cy,
        "head_r": head_r,
        "head_rx": head_rx,
        "head_ry": head_ry,
        "torso_cx": torso_cx,
        "torso_cy": torso_cy,
        "hip_cx": hip_cx,
        "ground_y": ground_y,
        "char_h": char_h,
    }


# ── Main Render ──────────────────────────────────────────────────────────────

def render_expression_sheet():
    """Render all 6 Luma expressions in a 3x2 grid."""

    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, RENDER_W, RENDER_H)
    ctx = cairo.Context(surface)
    ctx.set_antialias(cairo.ANTIALIAS_BEST)

    # Background
    set_color(ctx, CANVAS_BG)
    ctx.rectangle(0, 0, RENDER_W, RENDER_H)
    ctx.fill()

    # 3x2 grid layout
    cols = 3
    rows = 2
    margin = 30
    top_margin = 50  # room for title
    panel_w = (RENDER_W - (cols + 1) * margin) // cols
    panel_h = (RENDER_H - top_margin - (rows + 1) * margin) // rows

    expressions = ["CURIOUS", "DETERMINED", "SURPRISED", "WORRIED", "DELIGHTED", "FRUSTRATED"]
    panel_colors = [
        (230/255, 240/255, 235/255),   # warm mint
        (240/255, 232/255, 218/255),   # warm cream
        (240/255, 225/255, 230/255),   # warm rose
        (225/255, 230/255, 240/255),   # cool lavender
        (245/255, 238/255, 220/255),   # warm gold
        (238/255, 225/255, 225/255),   # muted coral
    ]

    char_data = []

    for idx, expr in enumerate(expressions):
        col = idx % cols
        row = idx // cols
        px = margin + col * (panel_w + margin)
        py = top_margin + margin + row * (panel_h + margin)

        # Panel background
        ctx.rectangle(px, py, panel_w, panel_h)
        set_color(ctx, panel_colors[idx])
        ctx.fill_preserve()
        set_color(ctx, LINE_COL, 0.15)
        ctx.set_line_width(2)
        ctx.stroke()

        # Ground plane
        ground_y = py + panel_h - 45

        # Ground line
        ctx.new_path()
        ctx.move_to(px + 15, ground_y)
        ctx.line_to(px + panel_w - 15, ground_y)
        set_color(ctx, LINE_COL, 0.2)
        ctx.set_line_width(2)
        ctx.stroke()

        # Drop shadow band (warm)
        ctx.rectangle(px + 15, ground_y, panel_w - 30, 10)
        set_color(ctx, (0.85, 0.78, 0.65, 0.3))
        ctx.fill()

        # Character
        char_h = panel_h - 100  # leave room for label and ground
        char_cx = px + panel_w / 2
        spec = GESTURE_SPECS[expr]

        info = draw_luma_expression(ctx, char_cx, ground_y, char_h, expr, spec)
        char_data.append((expr, info))

        # Label
        ctx.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(22)
        set_color(ctx, LINE_COL)
        text_ext = ctx.text_extents(expr)
        ctx.move_to(px + panel_w / 2 - text_ext.width / 2,
                    py + panel_h - 12)
        ctx.show_text(expr)

        # Sub-label
        ctx.set_font_size(11)
        set_color(ctx, LINE_COL, 0.5)
        sub = f"37% head | gesture line | cairo v{__version__}"
        sub_ext = ctx.text_extents(sub)
        ctx.move_to(px + panel_w / 2 - sub_ext.width / 2, py + 18)
        ctx.show_text(sub)

    # Title bar
    ctx.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(18)
    set_color(ctx, LINE_COL, 0.6)
    title = "LUMA — Full Expression Sheet C52 / Maya Santos / pycairo"
    title_ext = ctx.text_extents(title)
    ctx.move_to(RENDER_W / 2 - title_ext.width / 2, 32)
    ctx.show_text(title)

    # Convert to PIL for color enhancement and final output
    pil_img = cairo_surface_to_pil(surface)

    # Apply Sam's color enhancements if available
    if HAS_COLOR_ENHANCE:
        pil_rgb = pil_img.convert("RGB")

        for expr, info in char_data:
            char_left = int(info["head_cx"] - info["head_rx"] * 2)
            char_top = int(info["head_cy"] - info["head_r"] * 1.5)
            char_right = int(info["head_cx"] + info["head_rx"] * 2)
            char_bottom = int(info["ground_y"])
            char_bbox = (char_left, char_top, char_right, char_bottom)

            pil_rgb = apply_scene_tint(pil_rgb, char_bbox,
                                        key_light_color=(212, 146, 58), alpha=18)

            face_center = (int(info["head_cx"]), int(info["head_cy"]))
            face_radius = (int(info["head_rx"]), int(info["head_ry"]))
            pil_rgb = apply_skin_warmth(pil_rgb, face_center, face_radius)

            torso_left = int(info["torso_cx"] - info["head_r"] * 0.8)
            torso_top = int(info["torso_cy"] - info["char_h"] * 0.19)
            torso_right = int(info["torso_cx"] + info["head_r"] * 0.8)
            torso_bottom = int(info["torso_cy"] + info["char_h"] * 0.19)
            pil_rgb = apply_form_shadow(pil_rgb,
                                         (torso_left, torso_top, torso_right, torso_bottom),
                                         HOODIE_PIL, HOODIE_SH_PIL,
                                         shadow_shape="torso_diagonal")

        pil_img = pil_rgb.convert("RGBA")

    # Downscale to output resolution with LANCZOS
    pil_out = pil_img.convert("RGB").resize((OUTPUT_W, OUTPUT_H), Image.LANCZOS)

    # Save to BOTH locations (production + main character sheet)
    prod_path = str(output_dir("production", "LTG_PROD_luma_cairo_expressions.png"))
    ensure_dir(output_dir("production"))
    pil_out.save(prod_path)

    main_path = str(output_dir("characters", "main", "LTG_CHAR_luma_expression_sheet.png"))
    ensure_dir(output_dir("characters", "main"))
    pil_out.save(main_path)

    print(f"Saved: {prod_path}")
    print(f"Saved: {main_path}")
    print(f"  Size: {pil_out.size[0]}x{pil_out.size[1]}")
    print(f"  Expressions: {', '.join(expressions)}")
    print(f"  Engine: pycairo {cairo.version}")
    print(f"  Color enhance: {'applied' if HAS_COLOR_ENHANCE else 'skipped (import failed)'}")

    return main_path, char_data


if __name__ == "__main__":
    out_path, char_data = render_expression_sheet()
    print(f"\nDone. Output at: {out_path}")
