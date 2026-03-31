#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_char_miri.py — Canonical Grandma Miri Renderer Module v1.0.0
"Luma & the Glitchkin" — Cycle 53 / Maya Santos

PURPOSE:
  Single canonical module for drawing Grandma Miri. All generators import from here.
  Full pycairo rebuild from legacy PIL engine (LTG_TOOL_grandma_miri_expression_sheet.py).

  Implements Lee Tanaka's C52 Miri gesture spec: offset chain, permanent forward lean,
  habitual left-hip weight, hands-never-idle rule, cardigan physics.

INTERFACE:
  draw_miri(expression, pose=None, scale=1.0, facing="right",
            scene_lighting=None) -> cairo.ImageSurface

EXPRESSIONS:
  WARM, SKEPTICAL, CONCERNED, SURPRISED, WISE, KNOWING

CHARACTER SPECS:
  - 3.2 heads tall (MIRI_HEAD_RATIO = 3.2)
  - 88% circular head (slightly compressed vertically)
  - Permanent forward lean: base_lean = -4 degrees
  - Habitual left hip weight in all poses
  - Wooden hairpins (color 92,58,32), NOT chopsticks
  - Permanent blush (0.0 alpha for CONCERNED only)
  - Round glasses always on
  - Cardigan follows shoulder tilt asymmetrically

Dependencies: pycairo, math, random
"""

__version__ = "1.0.0"
__author__ = "Maya Santos"
__cycle__ = 53

import math
import random

import cairo

# ── Palette ──────────────────────────────────────────────────────────────────
SKIN       = (140/255, 84/255, 48/255)
SKIN_SH    = (106/255, 58/255, 30/255)
SKIN_HL    = (168/255, 106/255, 64/255)
BLUSH      = (212/255, 149/255, 107/255, 0.35)
BLUSH_ZERO = (212/255, 149/255, 107/255, 0.0)
HAIR       = (216/255, 208/255, 200/255)
HAIR_SH    = (168/255, 152/255, 140/255)
HAIR_HL    = (240/255, 236/255, 232/255)
EYE_W      = (250/255, 240/255, 220/255)
EYE_IRIS   = (139/255, 94/255, 60/255)
EYE_PUP    = (26/255, 15/255, 10/255)
EYE_HL     = (240/255, 240/255, 240/255)
BROW_COL   = (138/255, 122/255, 112/255)
CARDIGAN   = (184/255, 92/255, 56/255)
CARDIGAN_SH = (138/255, 60/255, 28/255)
CARDIGAN_HL = (212/255, 130/255, 90/255)
UNDERSHIRT = (245/255, 232/255, 212/255)
PANTS      = (200/255, 174/255, 138/255)
PANTS_SH   = (160/255, 138/255, 106/255)
SLIPPER    = (196/255, 144/255, 122/255)
GLASSES_COL = (59/255, 40/255, 32/255)
HAIRPIN_COL = (92/255, 58/255, 32/255)
LINE_COL   = (59/255, 40/255, 32/255)

# Expression-specific panel BGs (for sheet use)
PANEL_BG = {
    "WARM":      (248/255, 232/255, 210/255),
    "SKEPTICAL": (210/255, 218/255, 208/255),
    "CONCERNED": (200/255, 212/255, 225/255),
    "SURPRISED": (245/255, 228/255, 195/255),
    "WISE":      (218/255, 214/255, 205/255),
    "KNOWING":   (228/255, 218/255, 200/255),
}

# ── Constants ────────────────────────────────────────────────────────────────
SEED = 53
MIRI_HEAD_RATIO = 0.3125  # 1/3.2 = head is 31.25% of total height
MIRI_HEADS = 3.2
MIRI_BASE_LEAN = -4  # degrees forward (permanent)
MIRI_HABITUAL_HIP = "LEFT"

EXPRESSIONS = ["WARM", "SKEPTICAL", "CONCERNED", "SURPRISED", "WISE", "KNOWING"]

# ── Gesture Specs (Lee Tanaka C52) ───────────────────────────────────────────
# torso_lean values ADD to MIRI_BASE_LEAN.
# All pixel values at 2x render scale.

GESTURE_SPECS = {
    "WARM": {
        "hip_shift": -8,
        "shoulder_offset": 10,
        "head_offset": -12,
        "torso_lean": -6,       # total: -10 forward
        "hip_tilt": 4.0,
        "shoulder_tilt": -5.0,
        "head_tilt": 10.0,
        "weight_front": 0.55,
        "weight_back": 0.45,
        "front_foot_lift": 0,
        "back_foot_lift": 2,
        "front_foot_angle": 10,
        "back_foot_angle": 15,
        "left_arm": "wide_open_extended",
        "right_arm": "wide_open_with_towel",
        "brow_lift_l": 8,
        "brow_lift_r": 10,
        "mouth": "warm_smile",
        "eye_openness": 0.90,   # slightly narrowed (warm smile)
        "gaze_dx": -2,
        "gaze_dy": 1,
        "blush_alpha": 0.35,
    },
    "SKEPTICAL": {
        "hip_shift": -18,
        "shoulder_offset": 12,
        "head_offset": -10,
        "torso_lean": -2,       # total: -6
        "hip_tilt": 7.0,
        "shoulder_tilt": -5.0,
        "head_tilt": 8.0,
        "weight_front": 0.25,
        "weight_back": 0.75,
        "front_foot_lift": 3,
        "back_foot_lift": 0,
        "front_foot_angle": -5,
        "back_foot_angle": 20,
        "left_arm": "hand_on_hip",
        "right_arm": "chin_evaluation",
        "brow_lift_l": 4,
        "brow_lift_r": 16,      # one brow raised high
        "mouth": "oblique_smile",
        "eye_openness": 0.85,
        "gaze_dx": -3,
        "gaze_dy": 2,
        "blush_alpha": 0.25,
    },
    "CONCERNED": {
        "hip_shift": -6,
        "shoulder_offset": 6,
        "head_offset": -16,
        "torso_lean": -10,      # total: -14 (deepest forward lean)
        "hip_tilt": 3.0,
        "shoulder_tilt": -3.0,
        "head_tilt": -12.0,     # forward and down
        "weight_front": 0.65,
        "weight_back": 0.35,
        "front_foot_lift": 0,
        "back_foot_lift": 0,
        "front_foot_angle": -5,
        "back_foot_angle": -3,
        "left_arm": "chest_touch",
        "right_arm": "reaching_palm_up",
        "brow_lift_l": 14,
        "brow_lift_r": 16,      # corrugator kink (worry)
        "mouth": "concerned_frown",
        "eye_openness": 1.05,
        "gaze_dx": 0,
        "gaze_dy": 3,
        "blush_alpha": 0.0,     # no blush when CONCERNED
    },
    "SURPRISED": {
        "hip_shift": -4,
        "shoulder_offset": 6,
        "head_offset": 8,       # back (unusual for Miri)
        "torso_lean": 2,        # reduces lean — approaches vertical
        "hip_tilt": 3.0,
        "shoulder_tilt": -4.0,
        "head_tilt": 8.0,
        "shoulder_raise": 4,    # surprise reflex
        "weight_front": 0.50,
        "weight_back": 0.50,
        "front_foot_lift": 2,
        "back_foot_lift": 2,
        "front_foot_angle": 8,
        "back_foot_angle": 10,
        "left_arm": "mouth_cover",
        "right_arm": "cheek_touch",
        "brow_lift_l": 18,
        "brow_lift_r": 16,
        "mouth": "open_oh",
        "eye_openness": 1.30,
        "gaze_dx": 0,
        "gaze_dy": -2,
        "blush_alpha": 0.35,
    },
    "WISE": {
        "hip_shift": -12,
        "shoulder_offset": 8,
        "head_offset": -6,
        "torso_lean": -1,       # total: -5
        "hip_tilt": 5.0,
        "shoulder_tilt": -3.0,
        "head_tilt": 6.0,
        "weight_front": 0.40,
        "weight_back": 0.60,
        "front_foot_lift": 0,
        "back_foot_lift": 0,
        "front_foot_angle": -5,
        "back_foot_angle": 15,
        "left_arm": "resting_on_hip",
        "right_arm": "forearm_across_waist",
        "brow_lift_l": 6,
        "brow_lift_r": 8,
        "mouth": "gentle_closed",
        "eye_openness": 0.85,
        "gaze_dx": 2,
        "gaze_dy": 1,
        "blush_alpha": 0.25,
    },
    "KNOWING": {
        "hip_shift": -10,
        "shoulder_offset": 8,
        "head_offset": -8,
        "torso_lean": -3,       # total: -7 (more forward than WISE)
        "hip_tilt": 4.0,
        "shoulder_tilt": -3.0,
        "head_tilt": 4.0,
        "head_forward": 3.0,
        "weight_front": 0.55,
        "weight_back": 0.45,
        "front_foot_lift": 0,
        "back_foot_lift": 0,
        "front_foot_angle": 2,
        "back_foot_angle": 10,
        "left_arm": "dropped_with_released_object",
        "right_arm": "palm_to_chest",
        "brow_lift_l": 6,
        "brow_lift_r": 6,
        "mouth": "oblique_closed",
        "eye_openness": 0.88,
        "gaze_dx": 1,
        "gaze_dy": 0,
        "blush_alpha": 0.30,
    },
}


# ── Cairo Helpers ────────────────────────────────────────────────────────────

def _set_color(ctx, color, alpha=1.0):
    if len(color) == 4:
        ctx.set_source_rgba(color[0], color[1], color[2], color[3])
    else:
        ctx.set_source_rgba(color[0], color[1], color[2], alpha)


def _draw_ellipse_path(ctx, cx, cy, rx, ry):
    ctx.save()
    ctx.translate(cx, cy)
    ctx.scale(rx, ry)
    ctx.arc(0, 0, 1.0, 0, 2 * math.pi)
    ctx.restore()


def _bezier_points(p0, p1, p2, p3, steps=40):
    pts = []
    for i in range(steps + 1):
        t = i / steps
        x = ((1-t)**3 * p0[0] + 3*(1-t)**2*t * p1[0] +
             3*(1-t)*t**2 * p2[0] + t**3 * p3[0])
        y = ((1-t)**3 * p0[1] + 3*(1-t)**2*t * p1[1] +
             3*(1-t)*t**2 * p2[1] + t**3 * p3[1])
        pts.append((x, y))
    return pts


def _draw_variable_stroke_limb(ctx, points, w_start, w_end, fill_color, line_color, line_w):
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

    ctx.new_path()
    ctx.move_to(*left_edge[0])
    for p in left_edge[1:]:
        ctx.line_to(*p)
    for p in reversed(right_edge):
        ctx.line_to(*p)
    ctx.close_path()
    _set_color(ctx, fill_color)
    ctx.fill_preserve()
    _set_color(ctx, line_color)
    ctx.set_line_width(line_w)
    ctx.stroke()


def _draw_rounded_torso(ctx, cx, cy, w_top, w_bot, h, lean_dx, hip_tilt_px, shoulder_tilt_px):
    """Draw Miri's rounded torso (softer than Luma's bean — more maternal).
    Returns (left_shoulder, right_shoulder, left_hip, right_hip)."""
    top_y = cy - h / 2
    bot_y = cy + h / 2

    ls_x = cx + lean_dx - w_top
    ls_y = top_y + shoulder_tilt_px
    rs_x = cx + lean_dx + w_top
    rs_y = top_y - shoulder_tilt_px

    lh_x = cx + lean_dx * 0.5 - w_bot + hip_tilt_px
    lh_y = bot_y
    rh_x = cx + lean_dx * 0.5 + w_bot - hip_tilt_px
    rh_y = bot_y

    ctx.new_path()
    ctx.move_to(ls_x, ls_y)
    # Left side — more outward bulge (rounder than Luma)
    cp1x = ls_x - w_top * 0.22
    cp1y = ls_y + h * 0.35
    cp2x = lh_x - w_bot * 0.12
    cp2y = lh_y - h * 0.15
    ctx.curve_to(cp1x, cp1y, cp2x, cp2y, lh_x, lh_y)

    # Bottom
    ctx.curve_to(lh_x + w_bot * 0.3, bot_y + h * 0.05,
                 rh_x - w_bot * 0.3, bot_y + h * 0.05,
                 rh_x, rh_y)

    # Right side
    cp3x = rh_x + w_bot * 0.12
    cp3y = rh_y - h * 0.15
    cp4x = rs_x + w_top * 0.22
    cp4y = rs_y + h * 0.35
    ctx.curve_to(cp3x, cp3y, cp4x, cp4y, rs_x, rs_y)

    # Top (rounded shoulders)
    ctx.curve_to(rs_x - w_top * 0.3, top_y + h * 0.04,
                 ls_x + w_top * 0.3, top_y + h * 0.04,
                 ls_x, ls_y)

    ctx.close_path()
    return (ls_x, ls_y), (rs_x, rs_y), (lh_x, lh_y), (rh_x, rh_y)


# ── Arm Drawing Functions ────────────────────────────────────────────────────

def _draw_mitten_hand(ctx, hx, hy, hand_r, s, lw_minor):
    """Draw a soft mitten hand."""
    _draw_ellipse_path(ctx, hx, hy, hand_r, hand_r * 0.78)
    _set_color(ctx, SKIN)
    ctx.fill_preserve()
    _set_color(ctx, LINE_COL)
    ctx.set_line_width(lw_minor)
    ctx.stroke()


def _draw_arm_wide_open_extended(ctx, ls_pt, s, cardigan, lw_major, lw_minor, lw_accent, arm_w_top, arm_w_bot, hand_r_s):
    """WARM: left arm wide open for embrace."""
    la_shoulder = (ls_pt[0] + 8*s, ls_pt[1] + 6*s)
    la_elbow = (la_shoulder[0] - 60*s, la_shoulder[1] - 10*s)
    la_hand = (la_elbow[0] - 40*s, la_elbow[1] - 30*s)
    upper = _bezier_points(la_shoulder, (la_shoulder[0] - 15*s, la_shoulder[1] - 2*s),
                           (la_elbow[0] + 8*s, la_elbow[1] + 5*s), la_elbow, steps=25)
    fore = _bezier_points(la_elbow, (la_elbow[0] - 10*s, la_elbow[1] - 5*s),
                          (la_hand[0] + 8*s, la_hand[1] + 8*s), la_hand, steps=25)
    _draw_variable_stroke_limb(ctx, upper, arm_w_top, arm_w_bot * 1.1, cardigan, LINE_COL, lw_major)
    _draw_variable_stroke_limb(ctx, fore, arm_w_bot * 1.1, arm_w_bot, cardigan, LINE_COL, lw_major)
    _draw_mitten_hand(ctx, la_hand[0], la_hand[1], hand_r_s, s, lw_minor)
    # Open fingers
    for angle_deg in [-40, -15, 10, 35]:
        rad = math.radians(angle_deg - 120)
        fx = la_hand[0] + math.cos(rad) * hand_r_s * 1.3
        fy = la_hand[1] + math.sin(rad) * hand_r_s * 1.1
        ctx.new_path()
        ctx.move_to(la_hand[0] + math.cos(rad) * hand_r_s * 0.5,
                    la_hand[1] + math.sin(rad) * hand_r_s * 0.4)
        ctx.line_to(fx, fy)
        _set_color(ctx, SKIN)
        ctx.set_line_width(2.5*s)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.stroke()
        ctx.new_path()
        ctx.move_to(la_hand[0] + math.cos(rad) * hand_r_s * 0.5,
                    la_hand[1] + math.sin(rad) * hand_r_s * 0.4)
        ctx.line_to(fx, fy)
        _set_color(ctx, LINE_COL)
        ctx.set_line_width(lw_accent)
        ctx.stroke()


def _draw_arm_wide_open_with_towel(ctx, rs_pt, s, cardigan, lw_major, lw_minor, lw_accent, arm_w_top, arm_w_bot, hand_r_s):
    """WARM: right arm wide open, holding dish towel."""
    ra_shoulder = (rs_pt[0] - 8*s, rs_pt[1] + 6*s)
    ra_elbow = (ra_shoulder[0] + 55*s, ra_shoulder[1] - 8*s)
    ra_hand = (ra_elbow[0] + 35*s, ra_elbow[1] - 25*s)
    upper = _bezier_points(ra_shoulder, (ra_shoulder[0] + 12*s, ra_shoulder[1] - 2*s),
                           (ra_elbow[0] - 6*s, ra_elbow[1] + 4*s), ra_elbow, steps=25)
    fore = _bezier_points(ra_elbow, (ra_elbow[0] + 8*s, ra_elbow[1] - 4*s),
                          (ra_hand[0] - 6*s, ra_hand[1] + 6*s), ra_hand, steps=25)
    _draw_variable_stroke_limb(ctx, upper, arm_w_top, arm_w_bot * 1.1, cardigan, LINE_COL, lw_major)
    _draw_variable_stroke_limb(ctx, fore, arm_w_bot * 1.1, arm_w_bot, cardigan, LINE_COL, lw_major)
    _draw_mitten_hand(ctx, ra_hand[0], ra_hand[1], hand_r_s, s, lw_minor)
    # Dish towel: small rectangle draping from hand
    towel_w = hand_r_s * 1.5
    towel_h = hand_r_s * 2.5
    ctx.new_path()
    ctx.move_to(ra_hand[0] - towel_w * 0.3, ra_hand[1] + hand_r_s * 0.5)
    ctx.line_to(ra_hand[0] + towel_w * 0.5, ra_hand[1] + hand_r_s * 0.5)
    ctx.line_to(ra_hand[0] + towel_w * 0.4, ra_hand[1] + hand_r_s * 0.5 + towel_h)
    ctx.line_to(ra_hand[0] - towel_w * 0.4, ra_hand[1] + hand_r_s * 0.5 + towel_h * 0.9)
    ctx.close_path()
    _set_color(ctx, (245/255, 238/255, 225/255))
    ctx.fill_preserve()
    _set_color(ctx, LINE_COL)
    ctx.set_line_width(lw_accent)
    ctx.stroke()


def _draw_arm_hand_on_hip(ctx, ls_pt, torso_cx, torso_cy, torso_h, s, cardigan, lw_major, lw_minor, lw_accent, arm_w_top, arm_w_bot, hand_r_s):
    """SKEPTICAL: left hand on hip, elbow pointed out."""
    la_shoulder = (ls_pt[0] + 6*s, ls_pt[1] + 5*s)
    la_elbow = (la_shoulder[0] - 40*s, la_shoulder[1] + 20*s)
    hip_x = torso_cx - 25*s
    hip_y = torso_cy + torso_h * 0.35
    la_hand = (hip_x, hip_y)
    upper = _bezier_points(la_shoulder, (la_shoulder[0] - 10*s, la_shoulder[1] + 6*s),
                           (la_elbow[0] + 5*s, la_elbow[1] - 5*s), la_elbow, steps=25)
    fore = _bezier_points(la_elbow, (la_elbow[0] - 5*s, la_elbow[1] + 8*s),
                          (la_hand[0] - 8*s, la_hand[1] - 5*s), la_hand, steps=25)
    _draw_variable_stroke_limb(ctx, upper, arm_w_top, arm_w_bot * 1.1, cardigan, LINE_COL, lw_major)
    _draw_variable_stroke_limb(ctx, fore, arm_w_bot * 1.1, arm_w_bot, cardigan, LINE_COL, lw_major)
    _draw_mitten_hand(ctx, la_hand[0], la_hand[1], hand_r_s * 0.85, s, lw_minor)


def _draw_arm_chin_evaluation(ctx, rs_pt, head_cx, head_cy, head_r, s, cardigan, lw_major, lw_minor, lw_accent, arm_w_top, arm_w_bot, hand_r_s):
    """SKEPTICAL: right hand to chin, evaluating."""
    ra_shoulder = (rs_pt[0] - 6*s, rs_pt[1] + 5*s)
    chin_x = head_cx + 4*s
    chin_y = head_cy + head_r * 0.60
    ra_elbow = (ra_shoulder[0] + 10*s, ra_shoulder[1] + 28*s)
    ra_hand = (chin_x + 6*s, chin_y + 4*s)
    upper = _bezier_points(ra_shoulder, (ra_shoulder[0] + 5*s, ra_shoulder[1] + 10*s),
                           (ra_elbow[0] - 3*s, ra_elbow[1] - 6*s), ra_elbow, steps=25)
    fore = _bezier_points(ra_elbow, (ra_elbow[0] + 2*s, ra_elbow[1] + 6*s),
                          (ra_hand[0] + 8*s, ra_hand[1] + 10*s), ra_hand, steps=25)
    _draw_variable_stroke_limb(ctx, upper, arm_w_top, arm_w_bot * 1.1, cardigan, LINE_COL, lw_major)
    _draw_variable_stroke_limb(ctx, fore, arm_w_bot * 1.1, arm_w_bot, cardigan, LINE_COL, lw_major)
    _draw_mitten_hand(ctx, ra_hand[0], ra_hand[1], hand_r_s * 0.85, s, lw_minor)
    # Index finger extended to chin
    ctx.new_path()
    ctx.move_to(ra_hand[0] - 2*s, ra_hand[1] - hand_r_s * 0.4)
    ctx.line_to(chin_x, chin_y)
    _set_color(ctx, SKIN)
    ctx.set_line_width(2.5*s)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.stroke()
    ctx.new_path()
    ctx.move_to(ra_hand[0] - 2*s, ra_hand[1] - hand_r_s * 0.4)
    ctx.line_to(chin_x, chin_y)
    _set_color(ctx, LINE_COL)
    ctx.set_line_width(lw_accent)
    ctx.stroke()


def _draw_arm_chest_touch(ctx, ls_pt, torso_cx, torso_cy, s, cardigan, lw_major, lw_minor, lw_accent, arm_w_top, arm_w_bot, hand_r_s):
    """CONCERNED/KNOWING: left hand to chest (empathy/resonance)."""
    la_shoulder = (ls_pt[0] + 6*s, ls_pt[1] + 5*s)
    chest_x = torso_cx - 4*s
    chest_y = torso_cy - 10*s
    la_elbow = (la_shoulder[0] + 15*s, la_shoulder[1] + 22*s)
    la_hand = (chest_x, chest_y)
    upper = _bezier_points(la_shoulder, (la_shoulder[0] + 4*s, la_shoulder[1] + 8*s),
                           (la_elbow[0] - 2*s, la_elbow[1] - 5*s), la_elbow, steps=25)
    fore = _bezier_points(la_elbow, (la_elbow[0] + 3*s, la_elbow[1] + 5*s),
                          (la_hand[0] - 5*s, la_hand[1] + 3*s), la_hand, steps=25)
    _draw_variable_stroke_limb(ctx, upper, arm_w_top, arm_w_bot * 1.1, cardigan, LINE_COL, lw_major)
    _draw_variable_stroke_limb(ctx, fore, arm_w_bot * 1.1, arm_w_bot, cardigan, LINE_COL, lw_major)
    _draw_mitten_hand(ctx, la_hand[0], la_hand[1], hand_r_s * 0.9, s, lw_minor)
    # Spread fingers on chest
    for angle_deg in [-30, 0, 30]:
        rad = math.radians(angle_deg + 180)
        fx = la_hand[0] + math.cos(rad) * hand_r_s * 0.9
        fy = la_hand[1] + math.sin(rad) * hand_r_s * 0.7
        ctx.new_path()
        ctx.move_to(la_hand[0], la_hand[1])
        ctx.line_to(fx, fy)
        _set_color(ctx, SKIN)
        ctx.set_line_width(2*s)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.stroke()


def _draw_arm_reaching_palm_up(ctx, rs_pt, s, cardigan, lw_major, lw_minor, lw_accent, arm_w_top, arm_w_bot, hand_r_s):
    """CONCERNED: right hand reaching forward, palm up."""
    ra_shoulder = (rs_pt[0] - 6*s, rs_pt[1] + 5*s)
    ra_elbow = (ra_shoulder[0] + 35*s, ra_shoulder[1] + 18*s)
    ra_hand = (ra_elbow[0] + 40*s, ra_elbow[1] - 5*s)
    upper = _bezier_points(ra_shoulder, (ra_shoulder[0] + 10*s, ra_shoulder[1] + 6*s),
                           (ra_elbow[0] - 5*s, ra_elbow[1] - 4*s), ra_elbow, steps=25)
    fore = _bezier_points(ra_elbow, (ra_elbow[0] + 8*s, ra_elbow[1] - 2*s),
                          (ra_hand[0] - 8*s, ra_hand[1] + 4*s), ra_hand, steps=25)
    _draw_variable_stroke_limb(ctx, upper, arm_w_top, arm_w_bot * 1.1, cardigan, LINE_COL, lw_major)
    _draw_variable_stroke_limb(ctx, fore, arm_w_bot * 1.1, arm_w_bot, cardigan, LINE_COL, lw_major)
    # Palm-up hand (wider, flatter)
    _draw_ellipse_path(ctx, ra_hand[0], ra_hand[1], hand_r_s * 1.1, hand_r_s * 0.6)
    _set_color(ctx, SKIN)
    ctx.fill_preserve()
    _set_color(ctx, LINE_COL)
    ctx.set_line_width(lw_minor)
    ctx.stroke()


def _draw_arm_mouth_cover(ctx, ls_pt, head_cx, head_cy, head_r, s, cardigan, lw_major, lw_minor, lw_accent, arm_w_top, arm_w_bot, hand_r_s):
    """SURPRISED: left hand covering mouth."""
    la_shoulder = (ls_pt[0] + 6*s, ls_pt[1] + 5*s)
    mouth_x = head_cx - 5*s
    mouth_y = head_cy + head_r * 0.45
    la_elbow = (la_shoulder[0] + 12*s, la_shoulder[1] - 15*s)
    la_hand = (mouth_x, mouth_y)
    upper = _bezier_points(la_shoulder, (la_shoulder[0] + 3*s, la_shoulder[1] - 5*s),
                           (la_elbow[0] - 2*s, la_elbow[1] + 5*s), la_elbow, steps=25)
    fore = _bezier_points(la_elbow, (la_elbow[0] + 3*s, la_elbow[1] - 5*s),
                          (la_hand[0] - 5*s, la_hand[1] + 8*s), la_hand, steps=25)
    _draw_variable_stroke_limb(ctx, upper, arm_w_top, arm_w_bot * 1.1, cardigan, LINE_COL, lw_major)
    _draw_variable_stroke_limb(ctx, fore, arm_w_bot * 1.1, arm_w_bot, cardigan, LINE_COL, lw_major)
    _draw_mitten_hand(ctx, la_hand[0], la_hand[1], hand_r_s, s, lw_minor)
    # Spread fingers near mouth
    for angle_deg in [-25, 0, 25]:
        rad = math.radians(angle_deg - 90)
        fx = la_hand[0] + math.cos(rad) * hand_r_s * 1.0
        fy = la_hand[1] + math.sin(rad) * hand_r_s * 0.8
        ctx.new_path()
        ctx.move_to(la_hand[0] + math.cos(rad) * hand_r_s * 0.4,
                    la_hand[1] + math.sin(rad) * hand_r_s * 0.3)
        ctx.line_to(fx, fy)
        _set_color(ctx, SKIN)
        ctx.set_line_width(2*s)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.stroke()


def _draw_arm_cheek_touch(ctx, rs_pt, head_cx, head_cy, head_r, s, cardigan, lw_major, lw_minor, lw_accent, arm_w_top, arm_w_bot, hand_r_s):
    """SURPRISED: right hand to cheek."""
    ra_shoulder = (rs_pt[0] - 6*s, rs_pt[1] + 5*s)
    cheek_x = head_cx + head_r * 0.5
    cheek_y = head_cy + head_r * 0.15
    ra_elbow = (ra_shoulder[0] + 8*s, ra_shoulder[1] - 12*s)
    ra_hand = (cheek_x, cheek_y)
    upper = _bezier_points(ra_shoulder, (ra_shoulder[0] + 3*s, ra_shoulder[1] - 4*s),
                           (ra_elbow[0] - 2*s, ra_elbow[1] + 4*s), ra_elbow, steps=25)
    fore = _bezier_points(ra_elbow, (ra_elbow[0] + 2*s, ra_elbow[1] - 4*s),
                          (ra_hand[0] + 6*s, ra_hand[1] + 8*s), ra_hand, steps=25)
    _draw_variable_stroke_limb(ctx, upper, arm_w_top, arm_w_bot * 1.1, cardigan, LINE_COL, lw_major)
    _draw_variable_stroke_limb(ctx, fore, arm_w_bot * 1.1, arm_w_bot, cardigan, LINE_COL, lw_major)
    _draw_mitten_hand(ctx, ra_hand[0], ra_hand[1], hand_r_s * 0.9, s, lw_minor)


def _draw_arm_resting_on_hip(ctx, ls_pt, torso_cx, torso_cy, torso_h, s, cardigan, lw_major, lw_minor, lw_accent, arm_w_top, arm_w_bot, hand_r_s):
    """WISE: left hand resting on hip (relaxed, not demanding)."""
    la_shoulder = (ls_pt[0] + 6*s, ls_pt[1] + 5*s)
    hip_x = torso_cx - 20*s
    hip_y = torso_cy + torso_h * 0.30
    la_elbow = (la_shoulder[0] - 18*s, la_shoulder[1] + 20*s)
    la_hand = (hip_x, hip_y)
    upper = _bezier_points(la_shoulder, (la_shoulder[0] - 4*s, la_shoulder[1] + 6*s),
                           (la_elbow[0] + 3*s, la_elbow[1] - 4*s), la_elbow, steps=25)
    fore = _bezier_points(la_elbow, (la_elbow[0] - 2*s, la_elbow[1] + 6*s),
                          (la_hand[0] - 4*s, la_hand[1] - 3*s), la_hand, steps=25)
    _draw_variable_stroke_limb(ctx, upper, arm_w_top, arm_w_bot * 1.1, cardigan, LINE_COL, lw_major)
    _draw_variable_stroke_limb(ctx, fore, arm_w_bot * 1.1, arm_w_bot, cardigan, LINE_COL, lw_major)
    _draw_mitten_hand(ctx, la_hand[0], la_hand[1], hand_r_s * 0.85, s, lw_minor)


def _draw_arm_forearm_across_waist(ctx, rs_pt, torso_cx, torso_cy, s, cardigan, lw_major, lw_minor, lw_accent, arm_w_top, arm_w_bot, hand_r_s):
    """WISE: right forearm across waist, hand holding opposite elbow."""
    ra_shoulder = (rs_pt[0] - 6*s, rs_pt[1] + 5*s)
    ra_elbow = (ra_shoulder[0] - 5*s, ra_shoulder[1] + 25*s)
    ra_hand = (torso_cx - 15*s, torso_cy + 5*s)  # toward opposite elbow
    upper = _bezier_points(ra_shoulder, (ra_shoulder[0] - 2*s, ra_shoulder[1] + 8*s),
                           (ra_elbow[0] + 2*s, ra_elbow[1] - 5*s), ra_elbow, steps=25)
    fore = _bezier_points(ra_elbow, (ra_elbow[0] - 3*s, ra_elbow[1] + 5*s),
                          (ra_hand[0] + 5*s, ra_hand[1] - 3*s), ra_hand, steps=25)
    _draw_variable_stroke_limb(ctx, upper, arm_w_top, arm_w_bot * 1.1, cardigan, LINE_COL, lw_major)
    _draw_variable_stroke_limb(ctx, fore, arm_w_bot * 1.1, arm_w_bot, cardigan, LINE_COL, lw_major)
    _draw_mitten_hand(ctx, ra_hand[0], ra_hand[1], hand_r_s * 0.8, s, lw_minor)


def _draw_arm_dropped_with_released(ctx, ls_pt, s, cardigan, lw_major, lw_minor, lw_accent, arm_w_top, arm_w_bot, hand_r_s):
    """KNOWING: left arm dropped, fingers slightly curled (just let go)."""
    la_shoulder = (ls_pt[0] + 6*s, ls_pt[1] + 5*s)
    la_elbow = (la_shoulder[0] - 8*s, la_shoulder[1] + 32*s)
    la_hand = (la_elbow[0] - 4*s, la_elbow[1] + 35*s)
    upper = _bezier_points(la_shoulder, (la_shoulder[0] - 2*s, la_shoulder[1] + 10*s),
                           (la_elbow[0] + 2*s, la_elbow[1] - 6*s), la_elbow, steps=25)
    fore = _bezier_points(la_elbow, (la_elbow[0] - 1*s, la_elbow[1] + 8*s),
                          (la_hand[0] + 1*s, la_hand[1] - 5*s), la_hand, steps=25)
    _draw_variable_stroke_limb(ctx, upper, arm_w_top, arm_w_bot * 1.1, cardigan, LINE_COL, lw_major)
    _draw_variable_stroke_limb(ctx, fore, arm_w_bot * 1.1, arm_w_bot, cardigan, LINE_COL, lw_major)
    _draw_mitten_hand(ctx, la_hand[0], la_hand[1], hand_r_s * 0.85, s, lw_minor)
    # Slightly curled fingers (she just released something)
    for angle_deg in [140, 170, 200]:
        rad = math.radians(angle_deg)
        fx = la_hand[0] + math.cos(rad) * hand_r_s * 0.8
        fy = la_hand[1] + math.sin(rad) * hand_r_s * 0.6
        ctx.new_path()
        ctx.move_to(la_hand[0], la_hand[1])
        ctx.curve_to(la_hand[0] + math.cos(rad) * hand_r_s * 0.3,
                     la_hand[1] + math.sin(rad) * hand_r_s * 0.4,
                     fx + 2*s, fy + 2*s, fx, fy)
        _set_color(ctx, SKIN)
        ctx.set_line_width(2*s)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.stroke()


def _draw_arm_palm_to_chest(ctx, rs_pt, torso_cx, torso_cy, s, cardigan, lw_major, lw_minor, lw_accent, arm_w_top, arm_w_bot, hand_r_s):
    """KNOWING: right palm flat to center chest (emotional resonance)."""
    ra_shoulder = (rs_pt[0] - 6*s, rs_pt[1] + 5*s)
    chest_x = torso_cx + 2*s
    chest_y = torso_cy - 8*s
    ra_elbow = (ra_shoulder[0] - 5*s, ra_shoulder[1] + 20*s)
    ra_hand = (chest_x, chest_y)
    upper = _bezier_points(ra_shoulder, (ra_shoulder[0] - 2*s, ra_shoulder[1] + 6*s),
                           (ra_elbow[0] + 1*s, ra_elbow[1] - 4*s), ra_elbow, steps=25)
    fore = _bezier_points(ra_elbow, (ra_elbow[0] + 2*s, ra_elbow[1] + 5*s),
                          (ra_hand[0] + 5*s, ra_hand[1] + 3*s), ra_hand, steps=25)
    _draw_variable_stroke_limb(ctx, upper, arm_w_top, arm_w_bot * 1.1, cardigan, LINE_COL, lw_major)
    _draw_variable_stroke_limb(ctx, fore, arm_w_bot * 1.1, arm_w_bot, cardigan, LINE_COL, lw_major)
    _draw_mitten_hand(ctx, ra_hand[0], ra_hand[1], hand_r_s * 0.9, s, lw_minor)
    # Spread fingers on chest
    for angle_deg in [-20, 0, 20]:
        rad = math.radians(angle_deg + 180)
        fx = ra_hand[0] + math.cos(rad) * hand_r_s * 0.8
        fy = ra_hand[1] + math.sin(rad) * hand_r_s * 0.6
        ctx.new_path()
        ctx.move_to(ra_hand[0], ra_hand[1])
        ctx.line_to(fx, fy)
        _set_color(ctx, SKIN)
        ctx.set_line_width(2*s)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.stroke()


def _draw_arms(ctx, expression, spec, ls_pt, rs_pt, head_cx, head_cy, head_r,
               torso_cx, torso_cy, torso_h, s, cardigan, lw_major, lw_minor, lw_accent,
               arm_w_top, arm_w_bot, hand_r_s):
    """Dispatch arm drawing by expression spec."""
    la = spec["left_arm"]
    ra = spec["right_arm"]

    # Left arm dispatch
    if la == "wide_open_extended":
        _draw_arm_wide_open_extended(ctx, ls_pt, s, cardigan, lw_major, lw_minor, lw_accent, arm_w_top, arm_w_bot, hand_r_s)
    elif la == "hand_on_hip":
        _draw_arm_hand_on_hip(ctx, ls_pt, torso_cx, torso_cy, torso_h, s, cardigan, lw_major, lw_minor, lw_accent, arm_w_top, arm_w_bot, hand_r_s)
    elif la == "chest_touch":
        _draw_arm_chest_touch(ctx, ls_pt, torso_cx, torso_cy, s, cardigan, lw_major, lw_minor, lw_accent, arm_w_top, arm_w_bot, hand_r_s)
    elif la == "mouth_cover":
        _draw_arm_mouth_cover(ctx, ls_pt, head_cx, head_cy, head_r, s, cardigan, lw_major, lw_minor, lw_accent, arm_w_top, arm_w_bot, hand_r_s)
    elif la == "resting_on_hip":
        _draw_arm_resting_on_hip(ctx, ls_pt, torso_cx, torso_cy, torso_h, s, cardigan, lw_major, lw_minor, lw_accent, arm_w_top, arm_w_bot, hand_r_s)
    elif la == "dropped_with_released_object":
        _draw_arm_dropped_with_released(ctx, ls_pt, s, cardigan, lw_major, lw_minor, lw_accent, arm_w_top, arm_w_bot, hand_r_s)

    # Right arm dispatch
    if ra == "wide_open_with_towel":
        _draw_arm_wide_open_with_towel(ctx, rs_pt, s, cardigan, lw_major, lw_minor, lw_accent, arm_w_top, arm_w_bot, hand_r_s)
    elif ra == "wide_open_extended":
        # Mirror of left wide open (no towel)
        _draw_arm_wide_open_with_towel(ctx, rs_pt, s, cardigan, lw_major, lw_minor, lw_accent, arm_w_top, arm_w_bot, hand_r_s)
    elif ra == "chin_evaluation":
        _draw_arm_chin_evaluation(ctx, rs_pt, head_cx, head_cy, head_r, s, cardigan, lw_major, lw_minor, lw_accent, arm_w_top, arm_w_bot, hand_r_s)
    elif ra == "reaching_palm_up":
        _draw_arm_reaching_palm_up(ctx, rs_pt, s, cardigan, lw_major, lw_minor, lw_accent, arm_w_top, arm_w_bot, hand_r_s)
    elif ra == "cheek_touch":
        _draw_arm_cheek_touch(ctx, rs_pt, head_cx, head_cy, head_r, s, cardigan, lw_major, lw_minor, lw_accent, arm_w_top, arm_w_bot, hand_r_s)
    elif ra == "forearm_across_waist":
        _draw_arm_forearm_across_waist(ctx, rs_pt, torso_cx, torso_cy, s, cardigan, lw_major, lw_minor, lw_accent, arm_w_top, arm_w_bot, hand_r_s)
    elif ra == "palm_to_chest":
        _draw_arm_palm_to_chest(ctx, rs_pt, torso_cx, torso_cy, s, cardigan, lw_major, lw_minor, lw_accent, arm_w_top, arm_w_bot, hand_r_s)


# ── Main Drawing Function ───────────────────────────────────────────────────

def _draw_miri_on_context(ctx, cx, ground_y, char_h, expression, spec, scale=1.0):
    """Draw Grandma Miri on an existing cairo context.

    Returns dict with character layout info.
    """
    rng = random.Random(SEED + hash(expression))

    # ── Proportions ──
    head_h = char_h * MIRI_HEAD_RATIO
    head_r = head_h / 2
    body_h = char_h - head_h
    s = head_r / 100.0

    # Effective lean = base + per-expression
    effective_lean_deg = MIRI_BASE_LEAN + spec["torso_lean"]

    # Line weights (three-tier)
    lw_silhouette = max(4.0, 5.0 * s)
    lw_major = max(3.0, 3.5 * s)
    lw_minor = max(2.0, 2.5 * s)
    lw_accent = max(1.5, 2.0 * s)

    # ── Offset Chain ──
    hip_shift = spec["hip_shift"] * s
    shoulder_offset = spec["shoulder_offset"] * s
    head_offset = spec["head_offset"] * s
    torso_lean = effective_lean_deg * s * 1.5  # scale lean to pixels

    hip_cx = cx + hip_shift
    torso_cx = hip_cx + shoulder_offset
    head_cx = torso_cx + head_offset

    # ── Vertical layout ──
    head_cy = ground_y - char_h + head_r
    neck_bot_y = head_cy + head_r + head_r * 0.22
    torso_h = body_h * 0.40  # slightly longer torso than Luma (elder proportions)
    torso_cy = neck_bot_y + torso_h / 2
    torso_bot_y = neck_bot_y + torso_h
    leg_h = ground_y - torso_bot_y

    hip_tilt_px = spec["hip_tilt"] * s * 0.8
    shoulder_tilt_px = spec["shoulder_tilt"] * s * 0.8
    shoulder_raise = spec.get("shoulder_raise", 0) * s

    # Miri has wider shoulders relative to head (maternal build)
    sh_w = head_r * 0.85

    # Elder posture: shoulders drop + round inward
    elder_drop = 3 * s
    elder_inward = 2 * s

    # ══ LEGS ══
    leg_offset = head_r * 0.40
    leg_w_top = head_r * 0.20
    leg_w_bot = head_r * 0.16

    weight_front = spec["weight_front"]
    front_foot_lift = spec["front_foot_lift"] * s
    back_foot_lift = spec["back_foot_lift"] * s

    front_leg_x = hip_cx - leg_offset * (1.0 if weight_front > 0.5 else 0.7)
    back_leg_x = hip_cx + leg_offset * (1.0 if weight_front <= 0.5 else 0.7)

    fl_top = (front_leg_x, torso_bot_y)
    fl_knee = (front_leg_x - 2 * s, torso_bot_y + leg_h * 0.46)
    fl_ankle = (front_leg_x + 1 * s, ground_y - front_foot_lift - head_r * 0.22)
    front_leg_pts = _bezier_points(fl_top, fl_knee,
                                   (fl_knee[0] + 1*s, fl_knee[1] + leg_h * 0.2),
                                   fl_ankle, steps=30)
    _draw_variable_stroke_limb(ctx, front_leg_pts, leg_w_top, leg_w_bot,
                               PANTS, LINE_COL, lw_major)

    bl_top = (back_leg_x, torso_bot_y)
    bl_knee = (back_leg_x + 1 * s, torso_bot_y + leg_h * 0.48)
    bl_ankle = (back_leg_x + 1 * s, ground_y - back_foot_lift - head_r * 0.22)
    back_leg_pts = _bezier_points(bl_top, bl_knee,
                                  (bl_knee[0] - 1*s, bl_knee[1] + leg_h * 0.2),
                                  bl_ankle, steps=30)
    _draw_variable_stroke_limb(ctx, back_leg_pts, leg_w_top, leg_w_bot,
                               PANTS, LINE_COL, lw_major)

    # ── Slippers ──
    slipper_w = head_r * 0.28
    slipper_h = head_r * 0.15
    for foot_x, foot_y, foot_angle in [
        (front_leg_pts[-1][0], ground_y - front_foot_lift, spec["front_foot_angle"]),
        (back_leg_pts[-1][0], ground_y - back_foot_lift, spec["back_foot_angle"])
    ]:
        ctx.save()
        ctx.translate(foot_x, foot_y - slipper_h * 0.3)
        ctx.rotate(math.radians(foot_angle))
        _draw_ellipse_path(ctx, 0, 0, slipper_w, slipper_h)
        _set_color(ctx, SLIPPER)
        ctx.fill_preserve()
        _set_color(ctx, LINE_COL)
        ctx.set_line_width(lw_major)
        ctx.stroke()
        ctx.restore()

    # ══ TORSO ══
    w_top = sh_w - elder_inward
    w_bot = head_r * 0.58  # wider at hips than Luma
    attach = _draw_rounded_torso(ctx, torso_cx, torso_cy, w_top, w_bot, torso_h,
                                 torso_lean, hip_tilt_px, shoulder_tilt_px - elder_drop + shoulder_raise)
    ls_pt, rs_pt, lh_pt, rh_pt = attach
    _set_color(ctx, CARDIGAN)
    ctx.fill_preserve()
    _set_color(ctx, LINE_COL)
    ctx.set_line_width(lw_silhouette)
    ctx.stroke()

    # Form shadow on torso
    shadow_x1 = torso_cx + torso_lean + sh_w * 0.15
    shadow_y1 = torso_cy - torso_h / 2
    shadow_x2 = torso_cx + torso_lean * 0.5 - w_bot * 0.1
    shadow_y2 = torso_cy + torso_h / 2
    ctx.new_path()
    ctx.move_to(shadow_x1, shadow_y1)
    ctx.curve_to(shadow_x1 + sh_w * 0.25, shadow_y1 + torso_h * 0.3,
                 shadow_x2 + w_bot * 0.3, shadow_y2 - torso_h * 0.2,
                 shadow_x2, shadow_y2)
    ctx.line_to(torso_cx + torso_lean * 0.5 + w_bot, shadow_y2)
    ctx.curve_to(torso_cx + torso_lean + sh_w * 0.4, shadow_y2 - torso_h * 0.3,
                 shadow_x1 + sh_w * 0.4, shadow_y1 + torso_h * 0.2,
                 torso_cx + torso_lean + sh_w * 0.8, shadow_y1)
    ctx.close_path()
    _set_color(ctx, CARDIGAN_SH, 0.45)
    ctx.fill()

    # Undershirt V-neck
    collar_cx = torso_cx + torso_lean
    collar_y = torso_cy - torso_h / 2
    collar_w = head_r * 0.28
    ctx.new_path()
    ctx.move_to(collar_cx - collar_w, collar_y + 2 * s)
    ctx.curve_to(collar_cx - collar_w * 0.3, collar_y + 12 * s,
                 collar_cx + collar_w * 0.3, collar_y + 12 * s,
                 collar_cx + collar_w, collar_y + 2 * s)
    _set_color(ctx, UNDERSHIRT)
    ctx.set_line_width(max(4, 5 * s))
    ctx.stroke_preserve()
    _set_color(ctx, LINE_COL)
    ctx.set_line_width(lw_minor)
    ctx.stroke()

    # Cardigan hem — hangs longer on dropped-shoulder side
    hem_y = torso_bot_y - torso_h * 0.08
    cardigan_ext = 6 * s  # longer on dropped side
    ctx.new_path()
    ctx.move_to(lh_pt[0] + 2*s, hem_y - cardigan_ext)
    ctx.curve_to(hip_cx - w_bot * 0.3, hem_y + 3*s,
                 hip_cx + w_bot * 0.3, hem_y + 3*s,
                 rh_pt[0] - 2*s, hem_y)
    _set_color(ctx, CARDIGAN_SH)
    ctx.set_line_width(max(3, 3.5 * s))
    ctx.stroke()

    # ══ ARMS ══
    arm_w_top = head_r * 0.13
    arm_w_bot = head_r * 0.09
    hand_r_s = head_r * 0.11
    _draw_arms(ctx, expression, spec, ls_pt, rs_pt, head_cx, head_cy, head_r,
               torso_cx, torso_cy, torso_h, s, CARDIGAN, lw_major, lw_minor, lw_accent,
               arm_w_top, arm_w_bot, hand_r_s)

    # ══ NECK ══
    neck_top_y = head_cy + head_r * 0.90
    neck_w_top = head_r * 0.20
    neck_w_bot = head_r * 0.26

    ctx.new_path()
    ctx.move_to(head_cx - neck_w_top, neck_top_y)
    ctx.curve_to(head_cx - neck_w_top - 1*s, (neck_top_y + neck_bot_y) / 2,
                 torso_cx + torso_lean - neck_w_bot - 1*s, neck_bot_y - 2*s,
                 torso_cx + torso_lean - neck_w_bot, neck_bot_y)
    ctx.line_to(torso_cx + torso_lean + neck_w_bot, neck_bot_y)
    ctx.curve_to(torso_cx + torso_lean + neck_w_bot + 1*s, neck_bot_y - 2*s,
                 head_cx + neck_w_top + 1*s, (neck_top_y + neck_bot_y) / 2,
                 head_cx + neck_w_top, neck_top_y)
    ctx.close_path()
    _set_color(ctx, SKIN)
    ctx.fill_preserve()
    _set_color(ctx, LINE_COL)
    ctx.set_line_width(lw_minor)
    ctx.stroke()

    # ══ HEAD ══
    head_rx = head_r * 1.04  # 88% circular (slightly wider)
    head_ry = head_r * 0.92
    tilt_rad = math.radians(spec["head_tilt"])
    head_fwd = spec.get("head_forward", 0) * s

    ctx.save()
    ctx.translate(head_cx + head_fwd, head_cy)
    ctx.rotate(tilt_rad)

    # Head shape (rounder, softer jaw than Luma)
    ctx.new_path()
    steps = 100
    for i in range(steps):
        angle = i * 2 * math.pi / steps
        rx = head_rx
        ry = head_ry
        # Softer jaw (less pointed chin)
        chin_f = max(0, math.cos(angle - math.pi / 2)) ** 3
        ry += head_r * 0.06 * chin_f
        # Fuller cheeks
        for sign in [1, -1]:
            cheek_f = max(0, math.cos(angle - sign * 0.4)) ** 4
            rx += head_r * 0.05 * cheek_f
        px = rx * math.cos(angle)
        py = ry * math.sin(angle)
        if i == 0:
            ctx.move_to(px, py)
        else:
            ctx.line_to(px, py)
    ctx.close_path()
    _set_color(ctx, SKIN)
    ctx.fill_preserve()
    ctx.set_line_width(lw_silhouette)
    _set_color(ctx, LINE_COL)
    ctx.stroke()

    # ── Hair (grey bun + wisps) ──
    # Top hair mass
    hair_top_y = -head_ry * 0.85
    ctx.new_path()
    ctx.move_to(-head_rx * 0.90, -head_ry * 0.15)
    ctx.curve_to(-head_rx * 0.95, hair_top_y,
                 head_rx * 0.10, hair_top_y - head_ry * 0.25,
                 head_rx * 0.85, -head_ry * 0.20)
    ctx.curve_to(head_rx * 0.70, -head_ry * 0.55,
                 -head_rx * 0.50, -head_ry * 0.60,
                 -head_rx * 0.90, -head_ry * 0.15)
    ctx.close_path()
    _set_color(ctx, HAIR)
    ctx.fill_preserve()
    _set_color(ctx, LINE_COL)
    ctx.set_line_width(lw_major)
    ctx.stroke()

    # Bun
    bun_cx = head_rx * 0.08
    bun_cy = hair_top_y - head_ry * 0.15
    bun_rx = head_rx * 0.40
    bun_ry = head_ry * 0.30
    _draw_ellipse_path(ctx, bun_cx, bun_cy, bun_rx, bun_ry)
    _set_color(ctx, HAIR)
    ctx.fill_preserve()
    _set_color(ctx, LINE_COL)
    ctx.set_line_width(lw_major)
    ctx.stroke()

    # Bun shadow
    _draw_ellipse_path(ctx, bun_cx + bun_rx * 0.1, bun_cy + bun_ry * 0.3,
                       bun_rx * 0.6, bun_ry * 0.5)
    _set_color(ctx, HAIR_SH)
    ctx.fill()

    # Bun highlight
    ctx.new_path()
    for i in range(20):
        a = math.radians(200 + 140 * i / 19)
        px = bun_cx + bun_rx * 0.5 * math.cos(a)
        py = bun_cy + bun_ry * 0.4 * math.sin(a)
        if i == 0:
            ctx.move_to(px, py)
        else:
            ctx.line_to(px, py)
    _set_color(ctx, HAIR_HL)
    ctx.set_line_width(lw_accent)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.stroke()

    # Wooden hairpins
    hp_x1 = bun_cx - bun_rx * 0.30
    hp_x2 = bun_cx + bun_rx * 0.25
    for hp_x in [hp_x1, hp_x2]:
        ctx.new_path()
        ctx.move_to(hp_x, bun_cy - bun_ry - 5*s)
        ctx.line_to(hp_x + 3*s, bun_cy + bun_ry + 3*s)
        _set_color(ctx, HAIRPIN_COL)
        ctx.set_line_width(max(2.5, 3*s))
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.stroke()
        # Pin head
        ctx.new_path()
        ctx.arc(hp_x, bun_cy - bun_ry - 5*s, 2*s, 0, 2 * math.pi)
        _set_color(ctx, HAIRPIN_COL)
        ctx.fill()

    # Hair wisps at temples
    for side in [-1, 1]:
        ctx.new_path()
        tx = side * head_rx * 0.82
        ty = -head_ry * 0.10
        ctx.move_to(tx, ty)
        ctx.curve_to(tx + side * 3*s, ty + 8*s,
                     tx + side * 1*s, ty + 18*s,
                     tx - side * 2*s, ty + 22*s)
        _set_color(ctx, HAIR)
        ctx.set_line_width(lw_minor)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.stroke()

    # Face skin overlay (covers bottom of hair)
    face_cy_off = head_r * 0.12
    face_rx = head_rx * 0.85
    face_ry = head_ry * 0.68
    _draw_ellipse_path(ctx, 0, face_cy_off, face_rx, face_ry)
    _set_color(ctx, SKIN)
    ctx.fill()

    # ── Ears ──
    ear_r = head_r * 0.10
    ear_y = head_r * 0.06
    for side in [-1, 1]:
        _draw_ellipse_path(ctx, side * (head_rx - 2*s), ear_y, ear_r, ear_r * 1.1)
        _set_color(ctx, SKIN)
        ctx.fill_preserve()
        _set_color(ctx, LINE_COL)
        ctx.set_line_width(lw_minor)
        ctx.stroke()

    # ── Eyes (round glasses) ──
    eye_spacing = head_rx * 0.38
    eye_y = head_r * 0.08
    eye_rx = head_rx * 0.24
    eye_ry = head_ry * 0.28 * spec["eye_openness"]

    for side in [-1, 1]:
        ex = side * eye_spacing
        ey = eye_y

        # Glasses frame (drawn first, behind eye)
        glass_rx = eye_rx * 1.35
        glass_ry = eye_ry * 1.25
        _draw_ellipse_path(ctx, ex, ey, glass_rx, glass_ry)
        _set_color(ctx, GLASSES_COL, 0.15)
        ctx.fill_preserve()
        _set_color(ctx, GLASSES_COL)
        ctx.set_line_width(lw_major)
        ctx.stroke()

        # Eye white
        _draw_ellipse_path(ctx, ex, ey, eye_rx, eye_ry)
        _set_color(ctx, EYE_W)
        ctx.fill_preserve()
        _set_color(ctx, LINE_COL)
        ctx.set_line_width(lw_minor)
        ctx.stroke()

        # Upper lid
        ctx.new_path()
        for i in range(25):
            a = math.radians(200 + 140 * i / 24)
            px = ex + eye_rx * 1.01 * math.cos(a)
            py = ey + eye_ry * 0.95 * math.sin(a)
            if i == 0:
                ctx.move_to(px, py)
            else:
                ctx.line_to(px, py)
        _set_color(ctx, LINE_COL)
        ctx.set_line_width(lw_silhouette)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.stroke()

        # Iris
        gaze_dx = spec["gaze_dx"] * s
        gaze_dy = spec["gaze_dy"] * s
        iris_r = eye_rx * 0.65
        iris_ry = eye_ry * 0.58
        iris_cx = ex + gaze_dx
        iris_cy = ey + gaze_dy
        _draw_ellipse_path(ctx, iris_cx, iris_cy, iris_r, iris_ry)
        _set_color(ctx, EYE_IRIS)
        ctx.fill()

        # Pupil
        pup_r = iris_r * 0.48
        pup_ry = iris_ry * 0.48
        _draw_ellipse_path(ctx, iris_cx, iris_cy, pup_r, pup_ry)
        _set_color(ctx, EYE_PUP)
        ctx.fill()

        # Highlight
        hl_r = max(pup_r * 0.40, 2.5)
        ctx.new_path()
        ctx.arc(iris_cx + iris_r * 0.28, iris_cy - iris_ry * 0.28, hl_r, 0, 2 * math.pi)
        _set_color(ctx, EYE_HL)
        ctx.fill()

    # Glasses bridge
    ctx.new_path()
    ctx.move_to(-eye_spacing + eye_rx * 1.35, eye_y)
    ctx.line_to(eye_spacing - eye_rx * 1.35, eye_y)
    _set_color(ctx, GLASSES_COL)
    ctx.set_line_width(lw_major)
    ctx.stroke()

    # ── Brows (grey, thinner than young chars) ──
    for side, lift in [(-1, spec["brow_lift_l"] * s), (1, spec["brow_lift_r"] * s)]:
        bx = side * eye_spacing
        by = eye_y - eye_ry - 5*s - lift
        inner_x = bx + side * 14*s
        outer_x = bx - side * 16*s
        ctx.new_path()
        ctx.move_to(outer_x, by + 3*s)
        ctx.curve_to((outer_x + bx) / 2, by - 3*s,
                     (bx + inner_x) / 2, by - 1*s,
                     inner_x, by + 2*s)
        _set_color(ctx, BROW_COL)
        ctx.set_line_width(lw_minor)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.stroke()

    # ── Nose (softer, rounder) ──
    nose_y = head_r * 0.30
    ctx.new_path()
    ctx.move_to(-3*s, nose_y - 1*s)
    ctx.curve_to(-1*s, nose_y + 4*s, 2*s, nose_y + 3*s, 4*s, nose_y)
    _set_color(ctx, SKIN_SH)
    ctx.set_line_width(lw_minor)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.stroke()

    # ── Mouth ──
    mouth_y = head_r * 0.46
    mouth_w = head_rx * 0.28
    mouth_type = spec["mouth"]

    if mouth_type == "warm_smile":
        ctx.new_path()
        ctx.move_to(-mouth_w, mouth_y)
        ctx.curve_to(-mouth_w * 0.3, mouth_y - 5*s,
                     mouth_w * 0.3, mouth_y - 5*s,
                     mouth_w, mouth_y)
        _set_color(ctx, LINE_COL)
        ctx.set_line_width(lw_minor)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.stroke()
        # Smile crinkles
        for sx in [-1, 1]:
            ctx.new_path()
            ctx.move_to(sx * mouth_w, mouth_y)
            ctx.line_to(sx * (mouth_w + 3*s), mouth_y - 2*s)
            _set_color(ctx, SKIN_SH)
            ctx.set_line_width(lw_accent)
            ctx.stroke()

    elif mouth_type == "oblique_smile":
        # Asymmetric knowing smile
        ctx.new_path()
        ctx.move_to(-mouth_w, mouth_y + 1*s)
        ctx.curve_to(-mouth_w * 0.3, mouth_y - 3*s,
                     mouth_w * 0.3, mouth_y - 4*s,
                     mouth_w, mouth_y - 2*s)
        _set_color(ctx, LINE_COL)
        ctx.set_line_width(lw_minor)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.stroke()

    elif mouth_type == "concerned_frown":
        ctx.new_path()
        ctx.move_to(-mouth_w * 0.75, mouth_y - 1*s)
        ctx.curve_to(-mouth_w * 0.2, mouth_y + 3*s,
                     mouth_w * 0.2, mouth_y + 3*s,
                     mouth_w * 0.75, mouth_y - 1*s)
        _set_color(ctx, LINE_COL)
        ctx.set_line_width(lw_minor)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.stroke()

    elif mouth_type == "open_oh":
        mouth_rx = mouth_w * 0.5
        mouth_ry = head_r * 0.09
        _draw_ellipse_path(ctx, 0, mouth_y + 1*s, mouth_rx, mouth_ry)
        _set_color(ctx, (0.15, 0.08, 0.06))
        ctx.fill_preserve()
        _set_color(ctx, LINE_COL)
        ctx.set_line_width(lw_minor)
        ctx.stroke()

    elif mouth_type == "gentle_closed":
        ctx.new_path()
        ctx.move_to(-mouth_w * 0.7, mouth_y)
        ctx.curve_to(-mouth_w * 0.2, mouth_y - 3*s,
                     mouth_w * 0.2, mouth_y - 3*s,
                     mouth_w * 0.7, mouth_y)
        _set_color(ctx, LINE_COL)
        ctx.set_line_width(lw_minor)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.stroke()

    elif mouth_type == "oblique_closed":
        # Like oblique_smile but more contained
        ctx.new_path()
        ctx.move_to(-mouth_w * 0.6, mouth_y)
        ctx.curve_to(-mouth_w * 0.15, mouth_y - 2*s,
                     mouth_w * 0.15, mouth_y - 3*s,
                     mouth_w * 0.6, mouth_y - 1*s)
        _set_color(ctx, LINE_COL)
        ctx.set_line_width(lw_minor)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.stroke()

    # ── Permanent blush ──
    blush_alpha = spec.get("blush_alpha", 0.35)
    if blush_alpha > 0:
        blush_c = (BLUSH[0], BLUSH[1], BLUSH[2], blush_alpha)
        for side in [-1, 1]:
            cheek_cx = side * eye_spacing * 0.82
            cheek_cy = head_r * 0.26
            _draw_ellipse_path(ctx, cheek_cx, cheek_cy, 14*s, 8*s)
            _set_color(ctx, blush_c)
            ctx.fill()

    # ── Wrinkle lines (crow's feet, forehead) ──
    # Crow's feet at eye corners
    for side in [-1, 1]:
        ex = side * eye_spacing
        for i, angle_off in enumerate([15, 25, 35]):
            rad = math.radians(side * angle_off)
            start_x = ex + side * eye_rx * 1.3
            start_y = eye_y - 2*s + i * 3*s
            end_x = start_x + side * 5*s
            end_y = start_y + (i - 1) * 2*s
            ctx.new_path()
            ctx.move_to(start_x, start_y)
            ctx.line_to(end_x, end_y)
            _set_color(ctx, SKIN_SH, 0.4)
            ctx.set_line_width(lw_accent * 0.8)
            ctx.set_line_cap(cairo.LINE_CAP_ROUND)
            ctx.stroke()

    ctx.restore()  # End head tilt transform

    # ══ GESTURE LINE OVERLAY ══
    ctx.save()
    ctx.set_dash([8*s, 4*s])
    ctx.set_line_width(2.0)
    _set_color(ctx, (0.2, 0.6, 0.9, 0.35))
    ctx.new_path()
    g_head = (head_cx + head_fwd, head_cy - head_r * 0.4)
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
        "head_cx": head_cx + head_fwd,
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


# ── Public Interface ─────────────────────────────────────────────────────────

def draw_miri(expression, pose=None, scale=1.0, facing="right", scene_lighting=None):
    """Draw Grandma Miri and return a cairo.ImageSurface (ARGB32, transparent bg).

    Args:
        expression: str — one of EXPRESSIONS (e.g. "WARM", "CONCERNED")
        pose: dict or None — custom gesture spec overrides
        scale: float — base character height multiplier (1.0 = 380px at 2x)
        facing: str — "right" (default) or "left"
        scene_lighting: dict or None — future integration placeholder

    Returns:
        cairo.ImageSurface (FORMAT_ARGB32) with transparent background.
    """
    expression = expression.upper()
    if expression == "KNOWING STILLNESS":
        expression = "KNOWING"
    if expression not in GESTURE_SPECS:
        raise ValueError(f"Unknown expression: {expression}. Must be one of {EXPRESSIONS}")

    spec = dict(GESTURE_SPECS[expression])
    if pose:
        spec.update(pose)

    base_char_h = 380  # slightly shorter than Luma at same scale (elder)
    char_h = int(base_char_h * scale)
    canvas_w = int(char_h * 1.6)
    canvas_h = int(char_h * 1.2)
    cx = canvas_w // 2
    ground_y = canvas_h - int(char_h * 0.08)

    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, canvas_w, canvas_h)
    ctx = cairo.Context(surface)
    ctx.set_antialias(cairo.ANTIALIAS_BEST)

    if facing == "left":
        ctx.translate(canvas_w, 0)
        ctx.scale(-1, 1)

    _draw_miri_on_context(ctx, cx, ground_y, char_h, expression, spec, scale)

    return surface


def draw_miri_on_context(ctx, cx, ground_y, char_h, expression, pose=None, scale=1.0):
    """Draw Miri directly onto an existing cairo context (for sheet/scene use).

    Args:
        ctx: cairo.Context to draw on
        cx: horizontal center position
        ground_y: Y position of ground plane
        char_h: total character height in pixels
        expression: str — one of EXPRESSIONS
        pose: dict or None — custom gesture spec overrides

    Returns:
        dict with character layout info
    """
    expression = expression.upper()
    if expression == "KNOWING STILLNESS":
        expression = "KNOWING"
    if expression not in GESTURE_SPECS:
        raise ValueError(f"Unknown expression: {expression}. Must be one of {EXPRESSIONS}")

    spec = dict(GESTURE_SPECS[expression])
    if pose:
        spec.update(pose)

    return _draw_miri_on_context(ctx, cx, ground_y, char_h, expression, spec, scale)


def cairo_surface_to_pil(surface):
    """Convert cairo ImageSurface (ARGB32) to PIL RGBA Image."""
    from PIL import Image
    w = surface.get_width()
    h = surface.get_height()
    buf = surface.get_data()
    img = Image.frombuffer("RGBA", (w, h), bytes(buf), "raw", "BGRa", 0, 1)
    return img.copy()


# ── Self-test ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import os
    import sys
    from PIL import Image

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

    print("LTG_TOOL_char_miri.py — Self-test render")
    print(f"  Expressions: {', '.join(EXPRESSIONS)}")

    for expr in EXPRESSIONS:
        surf = draw_miri(expr, scale=1.0)
        pil_img = cairo_surface_to_pil(surf)
        pil_img.thumbnail((1280, 1280), Image.LANCZOS)
        out_path = str(output_dir("characters", "main", f"LTG_CHAR_miri_{expr.lower()}_test.png"))
        ensure_dir(output_dir("characters", "main"))
        pil_img.save(out_path)
        print(f"  {expr}: {pil_img.size[0]}x{pil_img.size[1]} -> {out_path}")

    print("Done.")
