#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_char_luma.py — Canonical Luma Renderer Module v1.2.0
"Luma & the Glitchkin" — Cycle 55 / Maya Santos

PURPOSE:
  Single canonical module for drawing Luma. All generators (expression sheets,
  style frames, storyboard panels, motion sheets) import from here.

  Extracted from LTG_TOOL_luma_cairo_expressions.py (C52) and refactored
  into the modular char_*.py interface.

INTERFACE:
  draw_luma(expression, pose=None, scale=1.0, facing="right",
            scene_lighting=None, pose_mode="side") -> cairo.ImageSurface

  Returns a cairo ImageSurface (FORMAT_ARGB32) with transparent background.
  The character is drawn centered horizontally, standing on the bottom edge.

EXPRESSIONS:
  CURIOUS, DETERMINED, SURPRISED, WORRIED, DELIGHTED, FRUSTRATED,
  DOUBT-IN-CERTAINTY

POSE MODES:
  side (default) — true side-facing profile view (right-facing)
  front         — full frontal, both eyes visible, symmetric/near-symmetric
  threequarter  — 3/4 angle between front and side (right-facing)
  back          — rear view: hair from behind, no face, clothing rear
  side_l        — left-facing side profile, distinct pose (not a mirror)

Dependencies: pycairo, Pillow (for conversion utilities), math, random
"""

__version__ = "1.2.0"
__author__ = "Maya Santos"
__cycle__ = 55

import math
import random

import cairo

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

HOODIE_CURIOUS     = (150/255, 175/255, 200/255)
HOODIE_CURIOUS_SH  = (120/255, 145/255, 170/255)
HOODIE_SURPRISED   = (232/255, 112/255, 58/255)
HOODIE_SURPRISED_SH = (184/255, 74/255, 32/255)
HOODIE_DETERMINED  = (220/255, 130/255, 55/255)
HOODIE_DETERMINED_SH = (180/255, 95/255, 35/255)
HOODIE_WORRIED     = (165/255, 155/255, 185/255)
HOODIE_WORRIED_SH  = (135/255, 125/255, 155/255)
HOODIE_DELIGHTED   = (245/255, 155/255, 65/255)
HOODIE_DELIGHTED_SH = (200/255, 115/255, 40/255)
HOODIE_FRUSTRATED  = (210/255, 95/255, 55/255)
HOODIE_FRUSTRATED_SH = (170/255, 65/255, 35/255)
# DOUBT-IN-CERTAINTY: muted teal-grey — halfway between decisive amber and anxious violet
HOODIE_DOUBT       = (110/255, 145/255, 160/255)
HOODIE_DOUBT_SH    = (82/255, 112/255, 128/255)

PANTS      = (42/255, 40/255, 80/255)
PANTS_SH   = (26/255, 24/255, 48/255)
SHOE       = (245/255, 232/255, 208/255)
SHOE_SOLE  = (199/255, 91/255, 57/255)
LACES      = (0, 240/255, 1.0)
PX_CYAN    = (0, 240/255, 1.0)
PX_MAG     = (1.0, 45/255, 107/255)

HOODIE_COLORS = {
    "CURIOUS":             (HOODIE_CURIOUS, HOODIE_CURIOUS_SH),
    "DETERMINED":          (HOODIE_DETERMINED, HOODIE_DETERMINED_SH),
    "SURPRISED":           (HOODIE_SURPRISED, HOODIE_SURPRISED_SH),
    "WORRIED":             (HOODIE_WORRIED, HOODIE_WORRIED_SH),
    "DELIGHTED":           (HOODIE_DELIGHTED, HOODIE_DELIGHTED_SH),
    "FRUSTRATED":          (HOODIE_FRUSTRATED, HOODIE_FRUSTRATED_SH),
    "DOUBT-IN-CERTAINTY":  (HOODIE_DOUBT, HOODIE_DOUBT_SH),
}

# ── Constants ────────────────────────────────────────────────────────────────
SEED = 52
LUMA_HEAD_RATIO = 0.37  # head height = 37% of total body height
LUMA_HEADS = 3.2        # body is 3.2 heads tall

EXPRESSIONS = ["CURIOUS", "DETERMINED", "SURPRISED", "WORRIED", "DELIGHTED", "FRUSTRATED",
               "DOUBT-IN-CERTAINTY"]

# ── Gesture Specs (from Lee's C50 analysis, amplified 40-60% for silhouette) ─
GESTURE_SPECS = {
    "CURIOUS": {
        "hip_shift": 18,
        "shoulder_offset": -16,
        "head_offset": -28,
        "torso_lean": -24,
        "hip_tilt": 5.0,
        "shoulder_tilt": -5.0,
        "head_tilt": -12.0,
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
        "hip_shift": 6,
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
        "stance_wide": 1.45,
    },
    "SURPRISED": {
        "hip_shift": -36,
        "shoulder_offset": 26,
        "head_offset": 24,
        "torso_lean": 38,
        "hip_tilt": -9.0,
        "shoulder_tilt": 10.0,
        "head_tilt": 16.0,
        "weight_front": 0.20,
        "weight_back": 0.80,
        "front_foot_lift": 20,
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
        "hip_shift": 12,
        "shoulder_offset": -8,
        "head_offset": 6,
        "torso_lean": 10,
        "hip_tilt": -5.0,
        "shoulder_tilt": 8.0,
        "head_tilt": 14.0,
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
        "hip_shift": -16,
        "shoulder_offset": 14,
        "head_offset": 10,
        "torso_lean": 8,
        "hip_tilt": -7.0,
        "shoulder_tilt": 6.0,
        "head_tilt": 18.0,
        "weight_front": 0.50,
        "weight_back": 0.50,
        "front_foot_lift": 12,
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
        "heel_lift": 10,
    },
    "FRUSTRATED": {
        "hip_shift": 20,
        "shoulder_offset": -14,
        "head_offset": -10,
        "torso_lean": -14,
        "hip_tilt": 8.0,
        "shoulder_tilt": -7.0,
        "head_tilt": -18.0,
        "weight_front": 0.80,
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
        "stance_wide": 1.5,
    },
    # ── DOUBT-IN-CERTAINTY ────────────────────────────────────────────────────
    # Pilot emotional climax: forced confidence on the outside, leaking doubt.
    # Stiff, planted stance (weight anchored, slight forward lean = "committed")
    # but: ONE brow raised (leaking doubt), gaze averted slightly downward,
    # jaw set (firm_line mouth), right hand fist at chest (resolve gesture)
    # left arm crossed tight over body (self-protective contradiction).
    # Does NOT read as pure confident or pure worried — it's the tension.
    "DOUBT-IN-CERTAINTY": {
        "hip_shift": 4,
        "shoulder_offset": -6,
        "head_offset": 2,
        "torso_lean": 6,          # slight forward lean = outward commitment
        "hip_tilt": 2.0,
        "shoulder_tilt": -4.0,
        "head_tilt": 4.0,         # nearly upright — stiff controlled posture
        "weight_front": 0.60,
        "weight_back": 0.40,
        "front_foot_lift": 0,
        "back_foot_lift": 0,
        "front_foot_angle": 10,
        "back_foot_angle": -12,
        "left_arm": "self_hold_grip",    # arm crossed = protective/doubt leak
        "right_arm": "fist_hip",         # fist planted at hip = forced resolve
        "brow_lift_l": 20,               # L brow raises sharply — the doubt signal
        "brow_lift_r": 4,                # R brow near neutral — the certainty mask
        "mouth": "firm_line",            # set jaw — outward certainty
        "eye_openness": 0.92,            # slightly narrowed — suppressed uncertainty
        "gaze_dx": 2,
        "gaze_dy": 4,                    # gaze drifts slightly down-right — averted
        "doubt_wince": True,             # flag: draw inner-brow corrugator kink on L
    },
}


# ── Cairo Helpers ────────────────────────────────────────────────────────────

def _set_color(ctx, color, alpha=1.0):
    """Set source color, handling 3-tuple or 4-tuple."""
    if len(color) == 4:
        ctx.set_source_rgba(color[0], color[1], color[2], color[3])
    else:
        ctx.set_source_rgba(color[0], color[1], color[2], alpha)


def _draw_ellipse_path(ctx, cx, cy, rx, ry):
    """Add an ellipse to the current path using bezier approximation."""
    ctx.save()
    ctx.translate(cx, cy)
    ctx.scale(rx, ry)
    ctx.arc(0, 0, 1.0, 0, 2 * math.pi)
    ctx.restore()


def _bezier_points(p0, p1, p2, p3, steps=40):
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


def _draw_variable_stroke_limb(ctx, points, w_start, w_end, fill_color, line_color, line_w):
    """Draw a limb as a filled tapered tube with variable-width stroke."""
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


def _draw_bean_torso(ctx, cx, cy, w_top, w_bot, h, lean_dx, hip_tilt_px, shoulder_tilt_px):
    """Draw an organic bean-shaped torso. Returns attachment points."""
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
    cp1x = ls_x - w_top * 0.15
    cp1y = ls_y + h * 0.35
    cp2x = lh_x - w_bot * 0.08
    cp2y = lh_y - h * 0.15
    ctx.curve_to(cp1x, cp1y, cp2x, cp2y, lh_x, lh_y)

    ctx.curve_to(lh_x + w_bot * 0.3, bot_y + h * 0.04,
                 rh_x - w_bot * 0.3, bot_y + h * 0.04,
                 rh_x, rh_y)

    cp3x = rh_x + w_bot * 0.08
    cp3y = rh_y - h * 0.15
    cp4x = rs_x + w_top * 0.15
    cp4y = rs_y + h * 0.35
    ctx.curve_to(cp3x, cp3y, cp4x, cp4y, rs_x, rs_y)

    ctx.curve_to(rs_x - w_top * 0.3, top_y + h * 0.03,
                 ls_x + w_top * 0.3, top_y + h * 0.03,
                 ls_x, ls_y)

    ctx.close_path()
    return (ls_x, ls_y), (rs_x, rs_y), (lh_x, lh_y), (rh_x, rh_y)


# ── Arm Drawing Functions ────────────────────────────────────────────────────

def _draw_arm_forward_reaching(ctx, ls_pt, head_cx, head_r, s, hoodie, lw_major, lw_minor, lw_accent, arm_w_top, arm_w_bot, hand_r_s):
    la_shoulder = (ls_pt[0] + 10*s, ls_pt[1] + 8*s)
    la_elbow = (la_shoulder[0] - 70*s, la_shoulder[1] + 14*s)
    la_hand = (la_elbow[0] - 40*s, la_elbow[1] - 42*s)
    upper = _bezier_points(la_shoulder, (la_shoulder[0] - 15*s, la_shoulder[1] + 5*s),
                           (la_elbow[0] + 5*s, la_elbow[1] - 8*s), la_elbow, steps=25)
    fore = _bezier_points(la_elbow, (la_elbow[0] - 8*s, la_elbow[1] - 12*s),
                          (la_hand[0] + 8*s, la_hand[1] + 10*s), la_hand, steps=25)
    _draw_unified_arm(ctx, upper + fore[1:], arm_w_top, arm_w_bot, hoodie, LINE_COL, lw_major)
    _draw_ellipse_path(ctx, la_hand[0], la_hand[1], hand_r_s, hand_r_s * 0.75)
    _set_color(ctx, SKIN); ctx.fill_preserve()
    _set_color(ctx, LINE_COL); ctx.set_line_width(lw_minor); ctx.stroke()
    _draw_ellipse_path(ctx, la_hand[0] + 5*s, la_hand[1] + 5*s, 4*s, 3*s)
    _set_color(ctx, SKIN); ctx.fill_preserve()
    _set_color(ctx, LINE_COL); ctx.set_line_width(lw_accent); ctx.stroke()


def _draw_arm_chin_touch(ctx, rs_pt, head_cx, head_cy, head_r, s, hoodie, lw_major, lw_minor, lw_accent, arm_w_top, arm_w_bot, hand_r_s):
    ra_shoulder = (rs_pt[0] - 10*s, rs_pt[1] + 8*s)
    chin_x = head_cx + 5*s
    chin_y = head_cy + head_r * 0.55
    ra_elbow = (ra_shoulder[0] + 5*s, ra_shoulder[1] + 30*s)
    ra_hand = (chin_x + 8*s, chin_y + 5*s)
    upper = _bezier_points(ra_shoulder, (ra_shoulder[0] + 8*s, ra_shoulder[1] + 12*s),
                           (ra_elbow[0] - 3*s, ra_elbow[1] - 10*s), ra_elbow, steps=25)
    fore = _bezier_points(ra_elbow, (ra_elbow[0] - 2*s, ra_elbow[1] + 8*s),
                          (ra_hand[0] + 10*s, ra_hand[1] + 15*s), ra_hand, steps=25)
    _draw_unified_arm(ctx, upper + fore[1:], arm_w_top, arm_w_bot, hoodie, LINE_COL, lw_major)
    _draw_ellipse_path(ctx, ra_hand[0], ra_hand[1], hand_r_s, hand_r_s * 0.75)
    _set_color(ctx, SKIN); ctx.fill_preserve()
    _set_color(ctx, LINE_COL); ctx.set_line_width(lw_minor); ctx.stroke()
    ctx.new_path()
    ctx.move_to(ra_hand[0] - 3*s, ra_hand[1] - hand_r_s * 0.5)
    ctx.line_to(chin_x, chin_y)
    _set_color(ctx, SKIN); ctx.set_line_width(3*s); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    ctx.new_path()
    ctx.move_to(ra_hand[0] - 3*s, ra_hand[1] - hand_r_s * 0.5)
    ctx.line_to(chin_x, chin_y)
    _set_color(ctx, LINE_COL); ctx.set_line_width(lw_accent); ctx.stroke()


def _draw_arm_defensive_high(ctx, ls_pt, s, hoodie, lw_major, lw_minor, lw_accent, arm_w_top, arm_w_bot, hand_r_s):
    la_shoulder = (ls_pt[0] + 10*s, ls_pt[1] + 5*s)
    la_elbow = (la_shoulder[0] - 38*s, la_shoulder[1] - 48*s)
    la_hand = (la_elbow[0] - 20*s, la_elbow[1] - 50*s)
    upper = _bezier_points(la_shoulder, (la_shoulder[0] - 12*s, la_shoulder[1] - 8*s),
                           (la_elbow[0] + 5*s, la_elbow[1] + 10*s), la_elbow, steps=25)
    fore = _bezier_points(la_elbow, (la_elbow[0] - 5*s, la_elbow[1] - 10*s),
                          (la_hand[0] + 5*s, la_hand[1] + 12*s), la_hand, steps=25)
    _draw_unified_arm(ctx, upper + fore[1:], arm_w_top, arm_w_bot, hoodie, LINE_COL, lw_major)
    _draw_ellipse_path(ctx, la_hand[0], la_hand[1], hand_r_s * 1.1, hand_r_s * 0.9)
    _set_color(ctx, SKIN); ctx.fill_preserve()
    _set_color(ctx, LINE_COL); ctx.set_line_width(lw_minor); ctx.stroke()
    for angle_deg in [-30, -10, 10, 30]:
        rad = math.radians(angle_deg - 90)
        fx = la_hand[0] + math.cos(rad) * hand_r_s * 1.2
        fy = la_hand[1] + math.sin(rad) * hand_r_s * 1.0
        ctx.new_path()
        ctx.move_to(la_hand[0] + math.cos(rad) * hand_r_s * 0.6,
                    la_hand[1] + math.sin(rad) * hand_r_s * 0.5)
        ctx.line_to(fx, fy)
        _set_color(ctx, LINE_COL); ctx.set_line_width(lw_accent); ctx.stroke()


def _draw_arm_flung_back(ctx, rs_pt, s, hoodie, lw_major, lw_minor, lw_accent, arm_w_top, arm_w_bot, hand_r_s):
    ra_shoulder = (rs_pt[0] - 8*s, rs_pt[1] + 5*s)
    ra_elbow = (ra_shoulder[0] + 65*s, ra_shoulder[1] + 8*s)
    ra_hand = (ra_elbow[0] + 45*s, ra_elbow[1] + 30*s)
    upper = _bezier_points(ra_shoulder, (ra_shoulder[0] + 15*s, ra_shoulder[1] + 3*s),
                           (ra_elbow[0] - 8*s, ra_elbow[1] - 5*s), ra_elbow, steps=25)
    fore = _bezier_points(ra_elbow, (ra_elbow[0] + 10*s, ra_elbow[1] + 3*s),
                          (ra_hand[0] - 8*s, ra_hand[1] - 5*s), ra_hand, steps=25)
    _draw_unified_arm(ctx, upper + fore[1:], arm_w_top, arm_w_bot, hoodie, LINE_COL, lw_major)
    _draw_ellipse_path(ctx, ra_hand[0], ra_hand[1], hand_r_s * 1.0, hand_r_s * 0.8)
    _set_color(ctx, SKIN); ctx.fill_preserve()
    _set_color(ctx, LINE_COL); ctx.set_line_width(lw_minor); ctx.stroke()
    for angle_deg in [20, 45, 70, 95]:
        rad = math.radians(angle_deg)
        fx = ra_hand[0] + math.cos(rad) * hand_r_s * 1.2
        fy = ra_hand[1] - math.sin(rad) * hand_r_s * 1.0
        ctx.new_path()
        ctx.move_to(ra_hand[0] + math.cos(rad) * hand_r_s * 0.6,
                    ra_hand[1] - math.sin(rad) * hand_r_s * 0.5)
        ctx.line_to(fx, fy)
        _set_color(ctx, LINE_COL); ctx.set_line_width(lw_accent); ctx.stroke()


def _draw_arm_fist_forward(ctx, ls_pt, s, hoodie, lw_major, lw_minor, lw_accent, arm_w_top, arm_w_bot, hand_r_s):
    la_shoulder = (ls_pt[0] + 8*s, ls_pt[1] + 6*s)
    la_elbow = (la_shoulder[0] + 12*s, la_shoulder[1] + 30*s)
    la_hand = (la_elbow[0] + 18*s, la_elbow[1] + 8*s)
    upper = _bezier_points(la_shoulder, (la_shoulder[0] + 4*s, la_shoulder[1] + 10*s),
                           (la_elbow[0] - 2*s, la_elbow[1] - 8*s), la_elbow, steps=25)
    fore = _bezier_points(la_elbow, (la_elbow[0] + 6*s, la_elbow[1] + 4*s),
                          (la_hand[0] - 4*s, la_hand[1] - 2*s), la_hand, steps=25)
    _draw_unified_arm(ctx, upper + fore[1:], arm_w_top, arm_w_bot, hoodie, LINE_COL, lw_major)
    _draw_ellipse_path(ctx, la_hand[0], la_hand[1], hand_r_s * 0.85, hand_r_s * 0.85)
    _set_color(ctx, SKIN); ctx.fill_preserve()
    _set_color(ctx, LINE_COL); ctx.set_line_width(lw_minor); ctx.stroke()
    ctx.new_path()
    ctx.move_to(la_hand[0] - hand_r_s * 0.4, la_hand[1] - hand_r_s * 0.3)
    ctx.curve_to(la_hand[0], la_hand[1] - hand_r_s * 0.5,
                 la_hand[0] + hand_r_s * 0.3, la_hand[1] - hand_r_s * 0.3,
                 la_hand[0] + hand_r_s * 0.5, la_hand[1] - hand_r_s * 0.1)
    _set_color(ctx, SKIN_SH); ctx.set_line_width(lw_accent); ctx.stroke()


def _draw_arm_fist_hip(ctx, rs_pt, s, hoodie, lw_major, lw_minor, lw_accent, arm_w_top, arm_w_bot, hand_r_s):
    ra_shoulder = (rs_pt[0] - 8*s, rs_pt[1] + 6*s)
    ra_elbow = (ra_shoulder[0] + 25*s, ra_shoulder[1] + 22*s)
    ra_hand = (ra_elbow[0] + 5*s, ra_elbow[1] + 20*s)
    upper = _bezier_points(ra_shoulder, (ra_shoulder[0] + 10*s, ra_shoulder[1] + 8*s),
                           (ra_elbow[0] - 5*s, ra_elbow[1] - 6*s), ra_elbow, steps=25)
    fore = _bezier_points(ra_elbow, (ra_elbow[0] + 3*s, ra_elbow[1] + 6*s),
                          (ra_hand[0] - 2*s, ra_hand[1] - 5*s), ra_hand, steps=25)
    _draw_unified_arm(ctx, upper + fore[1:], arm_w_top, arm_w_bot, hoodie, LINE_COL, lw_major)
    _draw_ellipse_path(ctx, ra_hand[0], ra_hand[1], hand_r_s * 0.8, hand_r_s * 0.8)
    _set_color(ctx, SKIN); ctx.fill_preserve()
    _set_color(ctx, LINE_COL); ctx.set_line_width(lw_minor); ctx.stroke()


def _draw_arm_self_hold_grip(ctx, ls_pt, torso_cx, torso_cy, s, hoodie, lw_major, lw_minor, lw_accent, arm_w_top, arm_w_bot, hand_r_s):
    la_shoulder = (ls_pt[0] + 8*s, ls_pt[1] + 5*s)
    la_elbow = (la_shoulder[0] + 22*s, la_shoulder[1] + 28*s)
    la_hand = (torso_cx + 18*s, torso_cy + 5*s)
    upper = _bezier_points(la_shoulder, (la_shoulder[0] + 6*s, la_shoulder[1] + 10*s),
                           (la_elbow[0] - 4*s, la_elbow[1] - 6*s), la_elbow, steps=25)
    fore = _bezier_points(la_elbow, (la_elbow[0] + 8*s, la_elbow[1] + 6*s),
                          (la_hand[0] - 4*s, la_hand[1] - 4*s), la_hand, steps=25)
    _draw_unified_arm(ctx, upper + fore[1:], arm_w_top, arm_w_bot, hoodie, LINE_COL, lw_major)
    _draw_ellipse_path(ctx, la_hand[0], la_hand[1], hand_r_s * 0.85, hand_r_s * 0.7)
    _set_color(ctx, SKIN); ctx.fill_preserve()
    _set_color(ctx, LINE_COL); ctx.set_line_width(lw_minor); ctx.stroke()


def _draw_arm_self_hold_cross(ctx, rs_pt, torso_cx, torso_cy, s, hoodie, lw_major, lw_minor, lw_accent, arm_w_top, arm_w_bot, hand_r_s):
    ra_shoulder = (rs_pt[0] - 8*s, rs_pt[1] + 5*s)
    ra_elbow = (ra_shoulder[0] - 5*s, ra_shoulder[1] + 26*s)
    ra_hand = (torso_cx + 10*s, torso_cy + 12*s)
    upper = _bezier_points(ra_shoulder, (ra_shoulder[0] - 3*s, ra_shoulder[1] + 10*s),
                           (ra_elbow[0] + 2*s, ra_elbow[1] - 6*s), ra_elbow, steps=25)
    fore = _bezier_points(ra_elbow, (ra_elbow[0] + 2*s, ra_elbow[1] + 8*s),
                          (ra_hand[0] - 3*s, ra_hand[1] - 4*s), ra_hand, steps=25)
    _draw_unified_arm(ctx, upper + fore[1:], arm_w_top, arm_w_bot, hoodie, LINE_COL, lw_major)
    _draw_ellipse_path(ctx, ra_hand[0], ra_hand[1], hand_r_s * 0.8, hand_r_s * 0.65)
    _set_color(ctx, SKIN); ctx.fill_preserve()
    _set_color(ctx, LINE_COL); ctx.set_line_width(lw_minor); ctx.stroke()


def _draw_arm_celebration_high(ctx, ls_pt, s, hoodie, lw_major, lw_minor, lw_accent, arm_w_top, arm_w_bot, hand_r_s):
    la_shoulder = (ls_pt[0] + 8*s, ls_pt[1] + 4*s)
    la_elbow = (la_shoulder[0] - 28*s, la_shoulder[1] - 55*s)
    la_hand = (la_elbow[0] - 15*s, la_elbow[1] - 48*s)
    upper = _bezier_points(la_shoulder, (la_shoulder[0] - 8*s, la_shoulder[1] - 12*s),
                           (la_elbow[0] + 4*s, la_elbow[1] + 10*s), la_elbow, steps=25)
    fore = _bezier_points(la_elbow, (la_elbow[0] - 4*s, la_elbow[1] - 10*s),
                          (la_hand[0] + 3*s, la_hand[1] + 8*s), la_hand, steps=25)
    _draw_unified_arm(ctx, upper + fore[1:], arm_w_top, arm_w_bot, hoodie, LINE_COL, lw_major)
    _draw_ellipse_path(ctx, la_hand[0], la_hand[1], hand_r_s * 1.0, hand_r_s * 0.85)
    _set_color(ctx, SKIN); ctx.fill_preserve()
    _set_color(ctx, LINE_COL); ctx.set_line_width(lw_minor); ctx.stroke()
    for angle_deg in [-50, -25, 0, 25, 50]:
        rad = math.radians(angle_deg - 90)
        fx = la_hand[0] + math.cos(rad) * hand_r_s * 1.4
        fy = la_hand[1] + math.sin(rad) * hand_r_s * 1.2
        ctx.new_path()
        ctx.move_to(la_hand[0] + math.cos(rad) * hand_r_s * 0.5,
                    la_hand[1] + math.sin(rad) * hand_r_s * 0.4)
        ctx.line_to(fx, fy)
        _set_color(ctx, SKIN); ctx.set_line_width(2.5*s); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
        ctx.new_path()
        ctx.move_to(la_hand[0] + math.cos(rad) * hand_r_s * 0.5,
                    la_hand[1] + math.sin(rad) * hand_r_s * 0.4)
        ctx.line_to(fx, fy)
        _set_color(ctx, LINE_COL); ctx.set_line_width(lw_accent); ctx.stroke()


def _draw_arm_celebration_pump(ctx, rs_pt, s, hoodie, lw_major, lw_minor, lw_accent, arm_w_top, arm_w_bot, hand_r_s):
    ra_shoulder = (rs_pt[0] - 6*s, rs_pt[1] + 4*s)
    ra_elbow = (ra_shoulder[0] + 30*s, ra_shoulder[1] - 38*s)
    ra_hand = (ra_elbow[0] + 10*s, ra_elbow[1] - 30*s)
    upper = _bezier_points(ra_shoulder, (ra_shoulder[0] + 8*s, ra_shoulder[1] - 8*s),
                           (ra_elbow[0] - 4*s, ra_elbow[1] + 8*s), ra_elbow, steps=25)
    fore = _bezier_points(ra_elbow, (ra_elbow[0] + 3*s, ra_elbow[1] - 6*s),
                          (ra_hand[0] - 2*s, ra_hand[1] + 5*s), ra_hand, steps=25)
    _draw_unified_arm(ctx, upper + fore[1:], arm_w_top, arm_w_bot, hoodie, LINE_COL, lw_major)
    _draw_ellipse_path(ctx, ra_hand[0], ra_hand[1], hand_r_s * 0.85, hand_r_s * 0.85)
    _set_color(ctx, SKIN); ctx.fill_preserve()
    _set_color(ctx, LINE_COL); ctx.set_line_width(lw_minor); ctx.stroke()


def _draw_arm_flung_down_wide(ctx, ls_pt, s, hoodie, lw_major, lw_minor, lw_accent, arm_w_top, arm_w_bot, hand_r_s):
    la_shoulder = (ls_pt[0] + 8*s, ls_pt[1] + 5*s)
    la_elbow = (la_shoulder[0] - 15*s, la_shoulder[1] + 38*s)
    la_hand = (la_elbow[0] - 8*s, la_elbow[1] + 48*s)
    upper = _bezier_points(la_shoulder, (la_shoulder[0] - 14*s, la_shoulder[1] + 6*s),
                           (la_elbow[0] + 8*s, la_elbow[1] - 4*s), la_elbow, steps=25)
    fore = _bezier_points(la_elbow, (la_elbow[0] - 10*s, la_elbow[1] + 8*s),
                          (la_hand[0] + 6*s, la_hand[1] - 6*s), la_hand, steps=25)
    _draw_unified_arm(ctx, upper + fore[1:], arm_w_top, arm_w_bot, hoodie, LINE_COL, lw_major)
    _draw_ellipse_path(ctx, la_hand[0], la_hand[1], hand_r_s * 1.0, hand_r_s * 0.85)
    _set_color(ctx, SKIN); ctx.fill_preserve()
    _set_color(ctx, LINE_COL); ctx.set_line_width(lw_minor); ctx.stroke()
    for angle_deg in [110, 135, 160, 185]:
        rad = math.radians(angle_deg)
        fx = la_hand[0] + math.cos(rad) * hand_r_s * 1.3
        fy = la_hand[1] - math.sin(rad) * hand_r_s * 1.1
        ctx.new_path()
        ctx.move_to(la_hand[0] + math.cos(rad) * hand_r_s * 0.5,
                    la_hand[1] - math.sin(rad) * hand_r_s * 0.4)
        ctx.line_to(fx, fy)
        _set_color(ctx, LINE_COL); ctx.set_line_width(lw_accent); ctx.stroke()


def _draw_arm_hair_pull(ctx, rs_pt, head_cx, head_cy, head_r, s, hoodie, lw_major, lw_minor, lw_accent, arm_w_top, arm_w_bot, hand_r_s):
    ra_shoulder = (rs_pt[0] - 6*s, rs_pt[1] + 5*s)
    ra_elbow = (ra_shoulder[0] - 10*s, ra_shoulder[1] + 25*s)
    ra_hand = (ra_elbow[0] - 12*s, ra_elbow[1] + 15*s)
    upper = _bezier_points(ra_shoulder, (ra_shoulder[0] + 5*s, ra_shoulder[1] - 6*s),
                           (ra_elbow[0] - 3*s, ra_elbow[1] + 6*s), ra_elbow, steps=25)
    fore = _bezier_points(ra_elbow, (ra_elbow[0] + 4*s, ra_elbow[1] - 6*s),
                          (ra_hand[0] - 4*s, ra_hand[1] + 6*s), ra_hand, steps=25)
    _draw_unified_arm(ctx, upper + fore[1:], arm_w_top, arm_w_bot, hoodie, LINE_COL, lw_major)
    _draw_ellipse_path(ctx, ra_hand[0], ra_hand[1], hand_r_s * 0.9, hand_r_s * 0.75)
    _set_color(ctx, SKIN); ctx.fill_preserve()
    _set_color(ctx, LINE_COL); ctx.set_line_width(lw_minor); ctx.stroke()
    for dx, dy in [(-4*s, -5*s), (2*s, -6*s), (6*s, -3*s)]:
        ctx.new_path()
        ctx.move_to(ra_hand[0] + dx * 0.3, ra_hand[1] + dy * 0.3)
        ctx.line_to(ra_hand[0] + dx, ra_hand[1] + dy)
        _set_color(ctx, SKIN_SH); ctx.set_line_width(lw_accent); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()


def _draw_unified_arm(ctx, all_pts, w_shoulder, w_wrist, fill_color, line_color, lw,
                      shoulder_open=True):
    """Draw an entire arm (upper + forearm combined) as ONE unified silhouette shape.

    Instead of outlining each segment separately (which creates visible seams),
    this builds a single closed polygon from the combined point list, then fills
    and strokes it once. The result reads as a solid connected limb form.

    Args:
        all_pts: list of (x, y) points along arm centerline (shoulder to wrist)
        w_shoulder: half-width at shoulder end
        w_wrist: half-width at wrist end
        fill_color: RGB/RGBA tuple for fill
        line_color: RGB/RGBA tuple for outline stroke
        lw: outline stroke width
        shoulder_open: if True (default), the shoulder end is NOT stroked — the
            arm fill blends into the hoodie body outline without a visible seam.
            The torso stroke covers the junction. If False, strokes the full
            closed path including the shoulder end (creates visible seam).
    """
    n = len(all_pts)
    if n < 2:
        return
    left_edge = []
    right_edge = []
    for i in range(n):
        t = i / max(1, n - 1)
        w = w_shoulder + (w_wrist - w_shoulder) * t
        if i == 0:
            dx = all_pts[1][0] - all_pts[0][0]
            dy = all_pts[1][1] - all_pts[0][1]
        elif i == n - 1:
            dx = all_pts[-1][0] - all_pts[-2][0]
            dy = all_pts[-1][1] - all_pts[-2][1]
        else:
            dx = all_pts[i+1][0] - all_pts[i-1][0]
            dy = all_pts[i+1][1] - all_pts[i-1][1]
        length = math.hypot(dx, dy) or 1.0
        nx = -dy / length
        ny = dx / length
        left_edge.append((all_pts[i][0] + nx * w, all_pts[i][1] + ny * w))
        right_edge.append((all_pts[i][0] - nx * w, all_pts[i][1] - ny * w))

    # Fill the whole arm shape (always closed for fill)
    ctx.new_path()
    ctx.move_to(*left_edge[0])
    for p in left_edge[1:]:
        ctx.line_to(*p)
    ctx.arc(all_pts[-1][0], all_pts[-1][1], w_wrist, 0, math.pi)
    for p in reversed(right_edge):
        ctx.line_to(*p)
    ctx.close_path()
    _set_color(ctx, fill_color)
    ctx.fill()

    # Stroke: open at shoulder end to avoid double outline where arm meets torso
    _set_color(ctx, line_color)
    ctx.set_line_width(lw)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    if shoulder_open:
        # Stroke only the outer silhouette edges: left edge top-to-wrist + wrist cap + right edge wrist-to-top
        # This leaves the shoulder end open — the torso outline covers the join.
        ctx.new_path()
        ctx.move_to(*left_edge[0])
        for p in left_edge[1:]:
            ctx.line_to(*p)
        # Wrist cap arc (lower half of circle — from left_edge end around to right_edge end)
        ctx.arc(all_pts[-1][0], all_pts[-1][1], w_wrist, 0, math.pi)
        for p in reversed(right_edge):
            ctx.line_to(*p)
        ctx.stroke()
    else:
        # Full closed stroke (legacy behaviour)
        ctx.new_path()
        ctx.move_to(*left_edge[0])
        for p in left_edge[1:]:
            ctx.line_to(*p)
        ctx.arc(all_pts[-1][0], all_pts[-1][1], w_wrist, 0, math.pi)
        for p in reversed(right_edge):
            ctx.line_to(*p)
        ctx.close_path()
        ctx.stroke()


def _draw_arms(ctx, expression, spec, ls_pt, rs_pt, head_cx, head_cy, head_r, torso_cx, torso_cy, s, hoodie, lw_major, lw_minor, lw_accent, arm_w_top, arm_w_bot, hand_r_s):
    """Dispatch arm drawing by expression spec."""
    la = spec["left_arm"]
    ra = spec["right_arm"]

    ARM_LEFT = {
        "forward_reaching": lambda: _draw_arm_forward_reaching(ctx, ls_pt, head_cx, head_r, s, hoodie, lw_major, lw_minor, lw_accent, arm_w_top, arm_w_bot, hand_r_s),
        "defensive_high": lambda: _draw_arm_defensive_high(ctx, ls_pt, s, hoodie, lw_major, lw_minor, lw_accent, arm_w_top, arm_w_bot, hand_r_s),
        "fist_forward": lambda: _draw_arm_fist_forward(ctx, ls_pt, s, hoodie, lw_major, lw_minor, lw_accent, arm_w_top, arm_w_bot, hand_r_s),
        "self_hold_grip": lambda: _draw_arm_self_hold_grip(ctx, ls_pt, torso_cx, torso_cy, s, hoodie, lw_major, lw_minor, lw_accent, arm_w_top, arm_w_bot, hand_r_s),
        "celebration_high": lambda: _draw_arm_celebration_high(ctx, ls_pt, s, hoodie, lw_major, lw_minor, lw_accent, arm_w_top, arm_w_bot, hand_r_s),
        "flung_down_wide": lambda: _draw_arm_flung_down_wide(ctx, ls_pt, s, hoodie, lw_major, lw_minor, lw_accent, arm_w_top, arm_w_bot, hand_r_s),
    }
    ARM_RIGHT = {
        "chin_touch": lambda: _draw_arm_chin_touch(ctx, rs_pt, head_cx, head_cy, head_r, s, hoodie, lw_major, lw_minor, lw_accent, arm_w_top, arm_w_bot, hand_r_s),
        "flung_back": lambda: _draw_arm_flung_back(ctx, rs_pt, s, hoodie, lw_major, lw_minor, lw_accent, arm_w_top, arm_w_bot, hand_r_s),
        "fist_hip": lambda: _draw_arm_fist_hip(ctx, rs_pt, s, hoodie, lw_major, lw_minor, lw_accent, arm_w_top, arm_w_bot, hand_r_s),
        "self_hold_cross": lambda: _draw_arm_self_hold_cross(ctx, rs_pt, torso_cx, torso_cy, s, hoodie, lw_major, lw_minor, lw_accent, arm_w_top, arm_w_bot, hand_r_s),
        "celebration_pump": lambda: _draw_arm_celebration_pump(ctx, rs_pt, s, hoodie, lw_major, lw_minor, lw_accent, arm_w_top, arm_w_bot, hand_r_s),
        "hair_pull": lambda: _draw_arm_hair_pull(ctx, rs_pt, head_cx, head_cy, head_r, s, hoodie, lw_major, lw_minor, lw_accent, arm_w_top, arm_w_bot, hand_r_s),
    }

    if la in ARM_LEFT:
        ARM_LEFT[la]()
    if ra in ARM_RIGHT:
        ARM_RIGHT[ra]()


# ── Main Drawing Function ───────────────────────────────────────────────────

def _draw_luma_on_context(ctx, cx, ground_y, char_h, expression, spec, scale=1.0):
    """Draw Luma in the given expression on an existing cairo context.

    Args:
        ctx: cairo.Context to draw on
        cx: horizontal center of character
        ground_y: Y position of ground plane
        char_h: total character height in pixels
        expression: name string (e.g. "CURIOUS")
        spec: gesture spec dict from GESTURE_SPECS
        scale: additional scale factor (default 1.0)

    Returns:
        dict with character layout info (head_cx, head_cy, head_r, etc.)
    """
    rng = random.Random(SEED + hash(expression))

    # ── Proportions ──
    head_h = char_h * LUMA_HEAD_RATIO
    head_r = head_h / 2
    body_h = char_h - head_h
    s = head_r / 100.0

    # Line weights (three-tier hierarchy)
    lw_silhouette = max(4.0, 5.0 * s)
    lw_major = max(3.0, 3.5 * s)
    lw_minor = max(2.0, 2.5 * s)
    lw_accent = max(1.5, 2.0 * s)

    # ── Offset Chain ──
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

    hip_tilt_px = spec["hip_tilt"] * s * 0.8
    shoulder_tilt_px = spec["shoulder_tilt"] * s * 0.8
    # Side view: torso is seen near-edge-on. ~50% of front view width (front=0.95).
    sh_w = head_r * 0.50

    hoodie, hoodie_sh = HOODIE_COLORS.get(expression, (HOODIE_SURPRISED, HOODIE_SURPRISED_SH))

    # ══ LEGS (side view — staggered fore/aft, not left/right) ══
    # In side view, both legs are near center-x. The near leg (in front of body in space)
    # steps slightly forward (+x in right-facing), the far leg steps slightly back (-x).
    # Y-difference: near foot lower on canvas (closer to viewer), far foot at ground.
    leg_w_top = head_r * 0.22
    leg_w_bot = head_r * 0.18
    leg_overlap = leg_w_top * 0.8

    weight_front = spec["weight_front"]
    front_foot_lift = spec["front_foot_lift"] * s
    back_foot_lift = spec["back_foot_lift"] * s
    heel_lift = spec.get("heel_lift", 0) * s

    # Side view: both legs centered at hip_cx; depth read via y-axis only
    near_leg_x = hip_cx  # near leg centered
    far_leg_x  = hip_cx  # far leg centered

    # Near foot is slightly lower Y (closer = lower in perspective), far at ground
    near_foot_lift = front_foot_lift
    far_foot_lift  = back_foot_lift + head_r * 0.04  # far foot slightly higher = receding

    leg_overlap = leg_w_top * 0.8

    # Far leg drawn first (behind); slight knee bow for visual interest
    bl_top = (far_leg_x, torso_bot_y - leg_overlap)
    bl_knee = (far_leg_x - 2 * s, torso_bot_y + leg_h * 0.50)
    bl_ankle = (far_leg_x, ground_y - far_foot_lift - heel_lift - head_r * 0.25)
    back_leg_pts = _bezier_points(bl_top, bl_knee,
                                  (bl_knee[0], bl_knee[1] + leg_h * 0.2),
                                  bl_ankle, steps=30)
    _draw_variable_stroke_limb(ctx, back_leg_pts, leg_w_top, leg_w_bot,
                               PANTS, LINE_COL, lw_major)

    # Near leg drawn in front; slight knee bow forward
    fl_top = (near_leg_x, torso_bot_y - leg_overlap)
    fl_knee = (near_leg_x + 3 * s, torso_bot_y + leg_h * 0.48)
    fl_ankle = (near_leg_x + 2 * s, ground_y - near_foot_lift - heel_lift - head_r * 0.25)
    front_leg_pts = _bezier_points(fl_top, fl_knee,
                                   (fl_knee[0] - 1*s, fl_knee[1] + leg_h * 0.2),
                                   fl_ankle, steps=30)
    _draw_variable_stroke_limb(ctx, front_leg_pts, leg_w_top, leg_w_bot,
                               PANTS, LINE_COL, lw_major)

    # Hip bridge: filled shape over the torso-leg junction (side view: narrow band)
    hip_bridge_y_top = torso_bot_y - torso_h * 0.04
    hip_bridge_y_bot = torso_bot_y + leg_w_top * 1.2
    hip_bw = leg_w_top * 1.4  # legs centered, so width from leg_w_top only
    hip_bridge_cx = hip_cx
    ctx.new_path()
    ctx.move_to(hip_bridge_cx - hip_bw, hip_bridge_y_top)
    ctx.curve_to(hip_bridge_cx - hip_bw * 0.8, hip_bridge_y_bot + 4*s,
                 hip_bridge_cx + hip_bw * 0.8, hip_bridge_y_bot + 4*s,
                 hip_bridge_cx + hip_bw, hip_bridge_y_top)
    ctx.curve_to(hip_bridge_cx + hip_bw * 0.6, hip_bridge_y_top - 4*s,
                 hip_bridge_cx - hip_bw * 0.6, hip_bridge_y_top - 4*s,
                 hip_bridge_cx - hip_bw, hip_bridge_y_top)
    ctx.close_path()
    _set_color(ctx, PANTS); ctx.fill()

    # Pants shadow
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
            _set_color(ctx, PANTS_SH, 0.5)
            ctx.set_line_width(leg_w_bot * 1.5)
            ctx.set_line_cap(cairo.LINE_CAP_ROUND)
            ctx.stroke()

    # ── Shoes (side view: near shoe faces forward, far shoe smaller/receding) ──
    shoe_w = head_r * 0.32
    shoe_h = head_r * 0.18
    # Far shoe (behind): slightly smaller, points slightly back
    ctx.save()
    ctx.translate(back_leg_pts[-1][0], ground_y - far_foot_lift - heel_lift - shoe_h * 0.3)
    ctx.rotate(math.radians(-8))
    _draw_ellipse_path(ctx, 0, 0, shoe_w * 0.85, shoe_h * 0.85)
    _set_color(ctx, SHOE); ctx.fill_preserve()
    _set_color(ctx, LINE_COL); ctx.set_line_width(lw_major); ctx.stroke()
    ctx.new_path()
    ctx.move_to(-shoe_w * 0.7, shoe_h * 0.4)
    ctx.curve_to(-shoe_w * 0.2, shoe_h * 0.65, shoe_w * 0.2, shoe_h * 0.65, shoe_w * 0.65, shoe_h * 0.3)
    _set_color(ctx, SHOE_SOLE); ctx.set_line_width(lw_minor); ctx.stroke()
    ctx.restore()
    # Near shoe (foreground): full size, points forward
    ctx.save()
    ctx.translate(front_leg_pts[-1][0], ground_y - near_foot_lift - heel_lift - shoe_h * 0.3)
    ctx.rotate(math.radians(12))
    _draw_ellipse_path(ctx, 0, 0, shoe_w, shoe_h)
    _set_color(ctx, SHOE); ctx.fill_preserve()
    _set_color(ctx, LINE_COL); ctx.set_line_width(lw_major); ctx.stroke()
    ctx.new_path()
    ctx.move_to(-shoe_w * 0.8, shoe_h * 0.4)
    ctx.curve_to(-shoe_w * 0.3, shoe_h * 0.7, shoe_w * 0.3, shoe_h * 0.7,
                 shoe_w * 0.8, shoe_h * 0.3)
    _set_color(ctx, SHOE_SOLE); ctx.set_line_width(lw_minor); ctx.stroke()
    ctx.new_path()
    ctx.arc(0, -shoe_h * 0.2, 2 * s, 0, 2 * math.pi)
    _set_color(ctx, LACES); ctx.fill()
    ctx.restore()

    # ══ TORSO ══
    w_top = sh_w
    # Side profile: hips also foreshortened. w_bot proportional to narrower sh_w.
    w_bot = head_r * 0.40
    attach = _draw_bean_torso(ctx, torso_cx, torso_cy, w_top, w_bot, torso_h,
                              torso_lean, hip_tilt_px, shoulder_tilt_px)
    ls_pt, rs_pt, lh_pt, rh_pt = attach
    _set_color(ctx, hoodie); ctx.fill_preserve()
    _set_color(ctx, LINE_COL); ctx.set_line_width(lw_silhouette); ctx.stroke()

    # Form shadow on torso
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
    _set_color(ctx, hoodie_sh, 0.5); ctx.fill()

    # Collar V-neck
    collar_cx = torso_cx + torso_lean
    collar_y = torso_cy - torso_h / 2
    collar_w = head_r * 0.30
    ctx.new_path()
    ctx.move_to(collar_cx - collar_w, collar_y + 2 * s)
    ctx.curve_to(collar_cx - collar_w * 0.3, collar_y + 14 * s,
                 collar_cx + collar_w * 0.3, collar_y + 14 * s,
                 collar_cx + collar_w, collar_y + 2 * s)
    _set_color(ctx, (250/255, 232/255, 200/255)); ctx.set_line_width(max(5, 6 * s)); ctx.stroke_preserve()
    _set_color(ctx, LINE_COL); ctx.set_line_width(lw_minor); ctx.stroke()

    # Hoodie hem
    hem_y = torso_bot_y - torso_h * 0.10
    ctx.new_path()
    ctx.move_to(lh_pt[0] + 3*s, hem_y)
    ctx.curve_to(hip_cx - w_bot * 0.3, hem_y + 4*s,
                 hip_cx + w_bot * 0.3, hem_y + 4*s,
                 rh_pt[0] - 3*s, hem_y)
    _set_color(ctx, hoodie_sh); ctx.set_line_width(max(3, 4 * s)); ctx.stroke()

    # Pixel accents
    for _ in range(12):
        px_x = torso_cx + torso_lean + rng.uniform(-18*s, 18*s)
        px_y = torso_cy + rng.uniform(-12*s, 12*s)
        psz = max(2, rng.choice([2*s, 3*s, 4*s]))
        pc = rng.choice([PX_CYAN, PX_MAG, (0.94, 0.94, 0.94)])
        ctx.rectangle(px_x, px_y, psz, psz)
        _set_color(ctx, pc); ctx.fill()

    # ══ ARMS (side view — foreshortened, hand stays at hip/waist height) ══
    # Arms in side view are drawn inline (not via _draw_arms dispatch which is
    # tuned for front view). In profile, arms hang roughly parallel to the body.
    # Near arm (forward-of-body): hangs with slight forward bend; hand at ~hip height.
    # Far arm (behind body): slightly bent back; hand at ~waist height.
    arm_w_top = head_r * 0.14
    arm_w_bot = head_r * 0.10
    hand_r_s = head_r * 0.12

    # Near arm attaches at rs_pt (right/forward side from viewer in right-facing profile)
    na_shoulder = (rs_pt[0] + 6*s, rs_pt[1] + 5*s)
    na_elbow    = (na_shoulder[0] + 16*s, na_shoulder[1] + 28*s)
    na_hand     = (na_elbow[0] + 8*s,    na_elbow[1]    + 28*s)
    near_arm_pts = (_bezier_points(na_shoulder,
                                   (na_shoulder[0] + 4*s, na_shoulder[1] + 10*s),
                                   (na_elbow[0] - 4*s, na_elbow[1] - 8*s), na_elbow, steps=25) +
                    _bezier_points(na_elbow,
                                   (na_elbow[0] + 4*s, na_elbow[1] + 8*s),
                                   (na_hand[0] - 3*s, na_hand[1] - 4*s), na_hand, steps=25)[1:])
    _draw_unified_arm(ctx, near_arm_pts, arm_w_top, arm_w_bot, hoodie, LINE_COL, lw_major)
    _draw_ellipse_path(ctx, na_hand[0], na_hand[1], hand_r_s, hand_r_s * 0.80)
    _set_color(ctx, SKIN); ctx.fill_preserve()
    _set_color(ctx, LINE_COL); ctx.set_line_width(lw_minor); ctx.stroke()

    # Far arm attaches at ls_pt (left/back side of torso)
    fa_shoulder = (ls_pt[0] - 6*s, ls_pt[1] + 5*s)
    fa_elbow    = (fa_shoulder[0] - 18*s, fa_shoulder[1] + 24*s)
    fa_hand     = (fa_elbow[0] + 6*s,    fa_elbow[1]    + 26*s)
    far_arm_pts = (_bezier_points(fa_shoulder,
                                  (fa_shoulder[0] - 6*s, fa_shoulder[1] + 8*s),
                                  (fa_elbow[0] + 4*s, fa_elbow[1] - 6*s), fa_elbow, steps=25) +
                   _bezier_points(fa_elbow,
                                  (fa_elbow[0] - 4*s, fa_elbow[1] + 8*s),
                                  (fa_hand[0] + 3*s, fa_hand[1] - 4*s), fa_hand, steps=25)[1:])
    _draw_unified_arm(ctx, far_arm_pts, arm_w_top, arm_w_bot, hoodie, LINE_COL, lw_major)
    _draw_ellipse_path(ctx, fa_hand[0], fa_hand[1], hand_r_s * 0.85, hand_r_s * 0.70)
    _set_color(ctx, SKIN); ctx.fill_preserve()
    _set_color(ctx, LINE_COL); ctx.set_line_width(lw_minor); ctx.stroke()

    # ══ NECK ══
    neck_top_y = head_cy + head_r * 0.95
    neck_w_top = head_r * 0.22
    neck_w_bot = head_r * 0.30

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
    _set_color(ctx, SKIN); ctx.fill_preserve()
    _set_color(ctx, LINE_COL); ctx.set_line_width(lw_minor); ctx.stroke()

    # ══ HEAD (side view — true profile, right-facing) ══
    # Profile head: oval that bulges toward the back (left) and has a slight
    # point/flatness toward the face direction (right). Hair cloud on back half only.
    # ONE eye visible (the near/only visible eye in profile).
    # Profile nose: bump protruding from the face silhouette.
    head_rx = head_r * 0.92   # slightly narrower in profile (depth = x-axis)
    head_ry = head_r * 1.00
    tilt_rad = math.radians(spec["head_tilt"] * 0.6)

    ctx.save()
    ctx.translate(head_cx, head_cy)
    ctx.rotate(tilt_rad)

    # Profile head shape: broader at the back (-x), narrower at the face (+x side)
    # Use custom point loop: left side (back of head) is rounder, right side tapers
    ctx.new_path()
    steps = 120
    for i in range(steps):
        angle = i * 2 * math.pi / steps
        rx = head_rx
        ry = head_ry
        # Chin: projects slightly forward and down
        chin_f = max(0, math.cos(angle - math.pi / 2)) ** 2.0
        ry += head_r * 0.12 * chin_f
        # Crown: flat top
        crown_f = max(0, math.cos(angle + math.pi / 2)) ** 3.0
        ry -= head_r * 0.06 * crown_f
        # Back of head (left = -x direction = angle near pi): rounded/bulging
        back_f = max(0, math.cos(angle - math.pi)) ** 4
        rx += head_r * 0.14 * back_f
        # Face side (right = +x = angle near 0): slight taper (jaw line)
        face_f = max(0, math.cos(angle)) ** 8
        rx -= head_r * 0.06 * face_f
        px = rx * math.cos(angle)
        py = ry * math.sin(angle)
        if i == 0:
            ctx.move_to(px, py)
        else:
            ctx.line_to(px, py)
    ctx.close_path()
    _set_color(ctx, SKIN); ctx.fill_preserve()
    ctx.set_line_width(lw_silhouette)
    _set_color(ctx, LINE_COL); ctx.stroke()

    # ── Profile nose bump (protrudes from face silhouette on +x side) ──
    # nose_x_base is anchored AT the face edge so the bump protrudes clearly outside.
    nose_x_base = head_rx * 0.94   # start at face edge (not inside)
    nose_y = head_r * 0.18         # slightly above mid-face
    # Nose: a bezier curve bump protruding to the right, clearly outside head oval
    ctx.new_path()
    ctx.move_to(nose_x_base, nose_y - 8*s)
    ctx.curve_to(nose_x_base + 14*s, nose_y - 6*s,
                 nose_x_base + 18*s, nose_y + 4*s,
                 nose_x_base + 10*s, nose_y + 11*s)
    ctx.curve_to(nose_x_base + 5*s, nose_y + 16*s,
                 nose_x_base, nose_y + 13*s,
                 nose_x_base - 2*s, nose_y + 8*s)
    _set_color(ctx, SKIN); ctx.fill_preserve()
    _set_color(ctx, LINE_COL); ctx.set_line_width(lw_minor); ctx.stroke()
    # Nostril shadow
    ctx.new_path()
    ctx.move_to(nose_x_base + 5*s, nose_y + 11*s)
    ctx.curve_to(nose_x_base + 2*s, nose_y + 14*s,
                 nose_x_base - 1*s, nose_y + 13*s,
                 nose_x_base - 2*s, nose_y + 8*s)
    _set_color(ctx, SKIN_SH); ctx.set_line_width(lw_accent); ctx.stroke()

    # ── Hair cloud (back of head only in profile — left half = negative x) ──
    hair_blobs_side = [
        # Back crown blobs (upper left quadrant)
        (-0.55, -0.75, 0.55, 0.48), (-0.30, -1.00, 0.42, 0.36),
        (-0.70, -0.50, 0.42, 0.38), (-0.80, -0.25, 0.38, 0.35),
        (0.00, -0.80, 0.40, 0.34), (0.10, -1.05, 0.34, 0.30),
        (-0.15, -0.60, 0.50, 0.44), (-0.50, -0.92, 0.30, 0.26),
        (-0.85, 0.02, 0.30, 0.32), (-0.60, 0.08, 0.35, 0.30),
        # A few blobs spilling over the top toward the front
        (0.20, -0.70, 0.30, 0.26), (-0.10, -1.10, 0.28, 0.24),
        # Side blobs (further back)
        (-0.90, -0.50, 0.26, 0.30),
    ]
    for (bx, by, brx, bry) in hair_blobs_side:
        _draw_ellipse_path(ctx, bx * head_rx, by * head_ry, brx * head_rx, bry * head_ry)
        _set_color(ctx, HAIR); ctx.fill()
    # Hair highlights
    for (bx, by, brx, bry) in [(-0.42, -0.85, 0.20, 0.12),
                                 (-0.65, -0.60, 0.14, 0.10),
                                 (-0.18, -0.95, 0.16, 0.10)]:
        _draw_ellipse_path(ctx, bx * head_rx, by * head_ry, brx * head_rx, bry * head_ry)
        _set_color(ctx, HAIR_HL); ctx.fill()

    # Face skin (right half of head — covers hair from face area)
    _draw_ellipse_path(ctx, head_rx * 0.10, head_r * 0.08, head_rx * 0.78, head_ry * 0.80)
    _set_color(ctx, SKIN); ctx.fill()

    # ── Profile eye (ONE eye — near the face side, toward +x) ──
    eye_x = head_rx * 0.28    # positioned toward the front of the profile
    eye_y_pos = head_r * 0.02
    eye_rx_p = head_rx * 0.22
    eye_ry_p = head_ry * 0.28 * spec["eye_openness"]

    _draw_ellipse_path(ctx, eye_x, eye_y_pos, eye_rx_p, eye_ry_p)
    _set_color(ctx, EYE_W); ctx.fill_preserve()
    _set_color(ctx, LINE_COL); ctx.set_line_width(lw_minor); ctx.stroke()
    # Upper lid
    ctx.new_path()
    for i in range(30):
        a = math.radians(195 + 150 * i / 29)
        px = eye_x + eye_rx_p * 1.01 * math.cos(a)
        py = eye_y_pos + eye_ry_p * 0.97 * math.sin(a)
        if i == 0:
            ctx.move_to(px, py)
        else:
            ctx.line_to(px, py)
    _set_color(ctx, LINE_COL)
    ctx.set_line_width(lw_silhouette); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    # Iris
    gaze_dx = spec["gaze_dx"] * s * 0.6   # gaze along profile axis
    gaze_dy = spec["gaze_dy"] * s
    iris_r = eye_rx_p * 0.70
    iris_ry = eye_ry_p * 0.64
    _draw_ellipse_path(ctx, eye_x + gaze_dx, eye_y_pos + gaze_dy, iris_r, iris_ry)
    _set_color(ctx, EYE_IRIS); ctx.fill()
    pup_r = iris_r * 0.52
    pup_ry = iris_ry * 0.52
    _draw_ellipse_path(ctx, eye_x + gaze_dx, eye_y_pos + gaze_dy, pup_r, pup_ry)
    _set_color(ctx, EYE_PUP); ctx.fill()
    hl_r = max(pup_r * 0.42, 3)
    ctx.new_path()
    ctx.arc(eye_x + gaze_dx + iris_r * 0.30, eye_y_pos + gaze_dy - iris_ry * 0.32,
            hl_r, 0, 2 * math.pi)
    _set_color(ctx, EYE_HL); ctx.fill()

    # ── Profile brow ──
    doubt_wince = spec.get("doubt_wince", False)
    brow_lift = spec["brow_lift_l"] * s  # use left brow lift in profile
    brow_y = eye_y_pos - eye_ry_p - 5*s - brow_lift
    brow_x_inner = eye_x + eye_rx_p * 0.6
    brow_x_outer = eye_x - eye_rx_p * 1.1
    ctx.new_path()
    ctx.move_to(brow_x_outer, brow_y + 4*s)
    ctx.curve_to((brow_x_outer + eye_x) / 2, brow_y - 4*s,
                 (eye_x + brow_x_inner) / 2, brow_y - 2*s,
                 brow_x_inner, brow_y + 2*s)
    _set_color(ctx, HAIR)
    ctx.set_line_width(lw_major); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    if doubt_wince:
        ctx.new_path()
        ctx.move_to(brow_x_inner, brow_y + 2*s)
        ctx.curve_to(brow_x_inner + 3*s, brow_y - 6*s,
                     brow_x_inner + 5*s, brow_y - 10*s,
                     brow_x_inner + 3*s, brow_y - 12*s)
        _set_color(ctx, HAIR)
        ctx.set_line_width(lw_minor); ctx.stroke()

    # ── Profile mouth ──
    mouth_y = head_r * 0.42
    mouth_w = head_rx * 0.26
    # mouth_x_base: anchor on the face surface near the silhouette edge.
    # In profile the mouth sits close to the face edge, not at 30% of head_rx.
    mouth_x_base = head_rx * 0.62   # mouth near the face side (+x profile edge)
    mouth_type = spec["mouth"]
    if mouth_type == "gentle_smile":
        ctx.new_path()
        ctx.move_to(mouth_x_base - mouth_w * 0.5, mouth_y + 1*s)
        ctx.curve_to(mouth_x_base - mouth_w * 0.1, mouth_y - 5*s,
                     mouth_x_base + mouth_w * 0.1, mouth_y - 4*s,
                     mouth_x_base + mouth_w * 0.4, mouth_y + 1*s)
        _set_color(ctx, LINE_COL); ctx.set_line_width(lw_minor); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    elif mouth_type == "firm_line":
        ctx.new_path()
        ctx.move_to(mouth_x_base - mouth_w * 0.4, mouth_y)
        ctx.curve_to(mouth_x_base, mouth_y - 2*s,
                     mouth_x_base + mouth_w * 0.2, mouth_y - 1*s,
                     mouth_x_base + mouth_w * 0.4, mouth_y + 1*s)
        _set_color(ctx, LINE_COL); ctx.set_line_width(lw_major); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    elif mouth_type == "open_o":
        _draw_ellipse_path(ctx, mouth_x_base, mouth_y + 2*s, mouth_w * 0.35, head_r * 0.10)
        _set_color(ctx, (0.15, 0.08, 0.06)); ctx.fill_preserve()
        _set_color(ctx, LINE_COL); ctx.set_line_width(lw_minor); ctx.stroke()
    elif mouth_type == "tight_frown":
        ctx.new_path()
        ctx.move_to(mouth_x_base - mouth_w * 0.5, mouth_y - 2*s)
        ctx.curve_to(mouth_x_base, mouth_y + 4*s,
                     mouth_x_base + mouth_w * 0.3, mouth_y + 3*s,
                     mouth_x_base + mouth_w * 0.5, mouth_y - 1*s)
        _set_color(ctx, LINE_COL); ctx.set_line_width(lw_minor); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    elif mouth_type == "wide_grin":
        _draw_ellipse_path(ctx, mouth_x_base, mouth_y + 1*s, mouth_w * 0.55, head_r * 0.09)
        _set_color(ctx, (0.15, 0.08, 0.06)); ctx.fill_preserve()
        _set_color(ctx, LINE_COL); ctx.set_line_width(lw_minor); ctx.stroke()
    elif mouth_type == "gritted_teeth":
        _draw_ellipse_path(ctx, mouth_x_base, mouth_y + 2*s, mouth_w * 0.42, head_r * 0.07)
        _set_color(ctx, (0.15, 0.08, 0.06)); ctx.fill_preserve()
        _set_color(ctx, LINE_COL); ctx.set_line_width(lw_minor); ctx.stroke()

    # ── Profile cheek blush (single, on face side) ──
    _draw_ellipse_path(ctx, eye_x * 0.9, head_r * 0.24, 14*s, 8*s)
    _set_color(ctx, BLUSH_C); ctx.fill()

    ctx.restore()  # End head tilt transform

    # ══ GESTURE LINE OVERLAY ══
    ctx.save()
    ctx.set_dash([8*s, 4*s])
    ctx.set_line_width(2.0)
    _set_color(ctx, (0.2, 0.6, 0.9, 0.35))
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


# ── Alternate Pose Mode Renderers ────────────────────────────────────────────

def _draw_luma_front(ctx, cx, ground_y, char_h, expression, spec, scale=1.0):
    """Render Luma from the FRONT — full frontal view, both eyes visible.

    Body is symmetric/near-symmetric. No offset chain dominates.
    Torso wider (both shoulders visible). Two arms visible on both sides.
    Returns layout dict matching _draw_luma_on_context.
    """
    rng = random.Random(SEED + hash(expression) + 1001)

    head_h = char_h * LUMA_HEAD_RATIO
    head_r = head_h / 2
    body_h = char_h - head_h
    s = head_r / 100.0

    lw_silhouette = max(4.0, 5.0 * s)
    lw_major = max(3.0, 3.5 * s)
    lw_minor = max(2.0, 2.5 * s)
    lw_accent = max(1.5, 2.0 * s)

    # Front view: body centered, no offset chain
    torso_cx = cx
    head_cx = cx
    hip_cx = cx

    # Mild hip tilt for life (not stiff)
    hip_tilt_px = spec["hip_tilt"] * s * 0.4
    shoulder_tilt_px = spec["shoulder_tilt"] * s * 0.3
    torso_lean = spec["torso_lean"] * s * 0.15  # minimal lean in front view

    head_cy = ground_y - char_h + head_r
    neck_bot_y = head_cy + head_r + head_r * 0.25
    torso_h = body_h * 0.38
    torso_cy = neck_bot_y + torso_h / 2
    torso_bot_y = neck_bot_y + torso_h
    leg_h = ground_y - torso_bot_y

    # Front view torso: wider (both sides visible)
    sh_w = head_r * 0.95
    w_top = sh_w
    w_bot = head_r * 0.62

    hoodie, hoodie_sh = HOODIE_COLORS.get(expression, (HOODIE_SURPRISED, HOODIE_SURPRISED_SH))

    # ══ LEGS — both legs near-symmetrical, slight spread ══
    leg_offset = head_r * 0.40
    stance_mult = spec.get("stance_wide", 1.0) * 0.9
    leg_offset *= stance_mult
    leg_w_top = head_r * 0.24
    leg_w_bot = head_r * 0.19
    leg_overlap = leg_w_top * 0.8

    fl_x = hip_cx - leg_offset  # left leg from viewer perspective
    fr_x = hip_cx + leg_offset  # right leg

    front_foot_lift = spec["front_foot_lift"] * s * 0.5
    back_foot_lift = spec["back_foot_lift"] * s * 0.5
    heel_lift = spec.get("heel_lift", 0) * s

    for (lx, foot_lift) in [(fl_x, front_foot_lift), (fr_x, back_foot_lift)]:
        lp_top = (lx, torso_bot_y - leg_overlap)
        lp_knee = (lx + (4*s if lx > cx else -4*s), torso_bot_y + leg_h * 0.48)
        lp_ankle = (lx, ground_y - foot_lift - heel_lift - head_r * 0.25)
        leg_pts = _bezier_points(lp_top, lp_knee,
                                 (lp_knee[0], lp_knee[1] + leg_h * 0.2),
                                 lp_ankle, steps=30)
        _draw_variable_stroke_limb(ctx, leg_pts, leg_w_top, leg_w_bot,
                                   PANTS, LINE_COL, lw_major)

    # Hip bridge
    hip_bw = leg_offset + leg_w_top * 1.3
    hip_bridge_y_top = torso_bot_y - torso_h * 0.04
    hip_bridge_y_bot = torso_bot_y + leg_w_top * 1.2
    ctx.new_path()
    ctx.move_to(hip_cx - hip_bw, hip_bridge_y_top)
    ctx.curve_to(hip_cx - hip_bw * 0.8, hip_bridge_y_bot + 4*s,
                 hip_cx + hip_bw * 0.8, hip_bridge_y_bot + 4*s,
                 hip_cx + hip_bw, hip_bridge_y_top)
    ctx.curve_to(hip_cx + hip_bw * 0.6, hip_bridge_y_top - 4*s,
                 hip_cx - hip_bw * 0.6, hip_bridge_y_top - 4*s,
                 hip_cx - hip_bw, hip_bridge_y_top)
    ctx.close_path()
    _set_color(ctx, PANTS); ctx.fill()

    # ── Shoes ──
    shoe_w = head_r * 0.30
    shoe_h = head_r * 0.18
    for (sx, foot_lift, fa) in [
        (fl_x, front_foot_lift, -8),
        (fr_x, back_foot_lift, 8),
    ]:
        ctx.save()
        ctx.translate(sx, ground_y - foot_lift - heel_lift - shoe_h * 0.3)
        ctx.rotate(math.radians(fa))
        _draw_ellipse_path(ctx, 0, 0, shoe_w, shoe_h)
        _set_color(ctx, SHOE); ctx.fill_preserve()
        _set_color(ctx, LINE_COL); ctx.set_line_width(lw_major); ctx.stroke()
        ctx.new_path()
        ctx.move_to(-shoe_w * 0.8, shoe_h * 0.4)
        ctx.curve_to(-shoe_w * 0.3, shoe_h * 0.7, shoe_w * 0.3, shoe_h * 0.7,
                     shoe_w * 0.8, shoe_h * 0.3)
        _set_color(ctx, SHOE_SOLE); ctx.set_line_width(lw_minor); ctx.stroke()
        ctx.new_path()
        ctx.arc(0, -shoe_h * 0.2, 2 * s, 0, 2 * math.pi)
        _set_color(ctx, LACES); ctx.fill()
        ctx.restore()

    # ══ TORSO ══
    attach = _draw_bean_torso(ctx, torso_cx, torso_cy, w_top, w_bot, torso_h,
                              torso_lean, hip_tilt_px, shoulder_tilt_px)
    ls_pt, rs_pt, lh_pt, rh_pt = attach
    _set_color(ctx, hoodie); ctx.fill_preserve()
    _set_color(ctx, LINE_COL); ctx.set_line_width(lw_silhouette); ctx.stroke()

    # Form shadow center stripe
    ctx.new_path()
    ctx.move_to(torso_cx, torso_cy - torso_h * 0.45)
    ctx.curve_to(torso_cx + w_top * 0.15, torso_cy,
                 torso_cx + w_bot * 0.12, torso_cy + torso_h * 0.3,
                 torso_cx + w_bot * 0.05, torso_cy + torso_h * 0.45)
    ctx.curve_to(torso_cx - w_bot * 0.08, torso_cy + torso_h * 0.3,
                 torso_cx - w_top * 0.1, torso_cy,
                 torso_cx, torso_cy - torso_h * 0.45)
    _set_color(ctx, hoodie_sh, 0.35); ctx.fill()

    # Collar V-neck (centered, symmetric in front view)
    collar_cx = torso_cx
    collar_y = torso_cy - torso_h / 2
    collar_w = head_r * 0.35
    ctx.new_path()
    ctx.move_to(collar_cx - collar_w, collar_y + 2 * s)
    ctx.curve_to(collar_cx - collar_w * 0.3, collar_y + 14 * s,
                 collar_cx + collar_w * 0.3, collar_y + 14 * s,
                 collar_cx + collar_w, collar_y + 2 * s)
    _set_color(ctx, (250/255, 232/255, 200/255)); ctx.set_line_width(max(5, 6 * s)); ctx.stroke_preserve()
    _set_color(ctx, LINE_COL); ctx.set_line_width(lw_minor); ctx.stroke()

    # Hoodie hem
    hem_y = torso_bot_y - torso_h * 0.10
    ctx.new_path()
    ctx.move_to(lh_pt[0] + 3*s, hem_y)
    ctx.curve_to(hip_cx - w_bot * 0.3, hem_y + 4*s,
                 hip_cx + w_bot * 0.3, hem_y + 4*s,
                 rh_pt[0] - 3*s, hem_y)
    _set_color(ctx, hoodie_sh); ctx.set_line_width(max(3, 4 * s)); ctx.stroke()

    # Pixel accents (center chest in front view)
    for _ in range(12):
        px_x = torso_cx + rng.uniform(-14*s, 14*s)
        px_y = torso_cy + rng.uniform(-12*s, 12*s)
        psz = max(2, rng.choice([2*s, 3*s, 4*s]))
        pc = rng.choice([PX_CYAN, PX_MAG, (0.94, 0.94, 0.94)])
        ctx.rectangle(px_x, px_y, psz, psz)
        _set_color(ctx, pc); ctx.fill()

    # ══ ARMS — symmetric spread for front view ══
    arm_w_top = head_r * 0.14
    arm_w_bot = head_r * 0.10
    hand_r_s = head_r * 0.12

    # Left arm (viewer left = character's right side)
    la_sh = (ls_pt[0] + 8*s, ls_pt[1] + 6*s)
    la_el = (la_sh[0] - 40*s, la_sh[1] + 22*s)
    la_hd = (la_el[0] - 20*s, la_el[1] + 18*s)
    l_pts = (_bezier_points(la_sh, (la_sh[0] - 10*s, la_sh[1] + 8*s),
                            (la_el[0] + 4*s, la_el[1] - 6*s), la_el, steps=20) +
             _bezier_points(la_el, (la_el[0] - 6*s, la_el[1] + 6*s),
                            (la_hd[0] + 4*s, la_hd[1] - 4*s), la_hd, steps=20)[1:])
    _draw_unified_arm(ctx, l_pts, arm_w_top, arm_w_bot, hoodie, LINE_COL, lw_major)
    _draw_ellipse_path(ctx, la_hd[0], la_hd[1], hand_r_s, hand_r_s * 0.8)
    _set_color(ctx, SKIN); ctx.fill_preserve()
    _set_color(ctx, LINE_COL); ctx.set_line_width(lw_minor); ctx.stroke()

    # Right arm (viewer right = character's left side)
    ra_sh = (rs_pt[0] - 8*s, rs_pt[1] + 6*s)
    ra_el = (ra_sh[0] + 40*s, ra_sh[1] + 22*s)
    ra_hd = (ra_el[0] + 20*s, ra_el[1] + 18*s)
    r_pts = (_bezier_points(ra_sh, (ra_sh[0] + 10*s, ra_sh[1] + 8*s),
                            (ra_el[0] - 4*s, ra_el[1] - 6*s), ra_el, steps=20) +
             _bezier_points(ra_el, (ra_el[0] + 6*s, ra_el[1] + 6*s),
                            (ra_hd[0] - 4*s, ra_hd[1] - 4*s), ra_hd, steps=20)[1:])
    _draw_unified_arm(ctx, r_pts, arm_w_top, arm_w_bot, hoodie, LINE_COL, lw_major)
    _draw_ellipse_path(ctx, ra_hd[0], ra_hd[1], hand_r_s, hand_r_s * 0.8)
    _set_color(ctx, SKIN); ctx.fill_preserve()
    _set_color(ctx, LINE_COL); ctx.set_line_width(lw_minor); ctx.stroke()

    # ══ NECK ══
    neck_top_y = head_cy + head_r * 0.95
    neck_w_top = head_r * 0.22
    neck_w_bot = head_r * 0.30
    ctx.new_path()
    ctx.move_to(head_cx - neck_w_top, neck_top_y)
    ctx.curve_to(head_cx - neck_w_top - 1*s, (neck_top_y + neck_bot_y) / 2,
                 torso_cx - neck_w_bot - 1*s, neck_bot_y - 3*s,
                 torso_cx - neck_w_bot, neck_bot_y)
    ctx.line_to(torso_cx + neck_w_bot, neck_bot_y)
    ctx.curve_to(torso_cx + neck_w_bot + 1*s, neck_bot_y - 3*s,
                 head_cx + neck_w_top + 1*s, (neck_top_y + neck_bot_y) / 2,
                 head_cx + neck_w_top, neck_top_y)
    ctx.close_path()
    _set_color(ctx, SKIN); ctx.fill_preserve()
    _set_color(ctx, LINE_COL); ctx.set_line_width(lw_minor); ctx.stroke()

    # ══ HEAD (front view — both eyes visible and symmetric) ══
    head_rx = head_r * 1.06
    head_ry = head_r
    tilt_rad = math.radians(spec["head_tilt"] * 0.4)

    ctx.save()
    ctx.translate(head_cx, head_cy)
    ctx.rotate(tilt_rad)

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
    _set_color(ctx, SKIN); ctx.fill_preserve()
    ctx.set_line_width(lw_silhouette)
    _set_color(ctx, LINE_COL); ctx.stroke()

    # Hair cloud
    hair_blobs = [
        (0, -0.65, 0.70, 0.55), (-0.50, -0.50, 0.55, 0.50),
        (0.50, -0.50, 0.55, 0.50), (-0.30, -0.95, 0.40, 0.35),
        (0.30, -0.95, 0.40, 0.35), (0, -1.10, 0.35, 0.30),
        (-0.85, -0.30, 0.35, 0.38), (0.85, -0.30, 0.35, 0.38),
        (-0.70, -0.60, 0.35, 0.32), (0.70, -0.60, 0.35, 0.32),
        (-0.15, -0.45, 0.60, 0.42), (0.15, -0.45, 0.60, 0.42),
        (-0.50, -0.80, 0.32, 0.28), (0.50, -0.80, 0.32, 0.28),
        (-0.45, -1.05, 0.25, 0.22), (0.45, -1.05, 0.25, 0.22),
        (0.15, -1.15, 0.22, 0.20),
    ]
    for (bx, by, brx, bry) in hair_blobs:
        _draw_ellipse_path(ctx, bx * head_rx, by * head_ry, brx * head_rx, bry * head_ry)
        _set_color(ctx, HAIR); ctx.fill()
    for (bx, by, brx, bry) in [(-0.30, -0.85, 0.22, 0.13),
                                 (0.20, -0.72, 0.16, 0.10),
                                 (-0.55, -0.55, 0.14, 0.10)]:
        _draw_ellipse_path(ctx, bx * head_rx, by * head_ry, brx * head_rx, bry * head_ry)
        _set_color(ctx, HAIR_HL); ctx.fill()

    face_cy_off = head_r * 0.10
    face_rx = head_rx * 0.88
    face_ry = head_ry * 0.70
    _draw_ellipse_path(ctx, 0, face_cy_off, face_rx, face_ry)
    _set_color(ctx, SKIN); ctx.fill()

    # ── Eyes: both visible, symmetric ──
    eye_spacing = head_rx * 0.40
    eye_y = head_r * 0.05
    eye_rx = head_rx * 0.28
    eye_ry = head_ry * 0.32 * spec["eye_openness"]

    for side in [-1, 1]:
        ex = side * eye_spacing
        ey = eye_y
        _draw_ellipse_path(ctx, ex, ey, eye_rx, eye_ry)
        _set_color(ctx, EYE_W); ctx.fill_preserve()
        _set_color(ctx, LINE_COL); ctx.set_line_width(lw_minor); ctx.stroke()
        ctx.new_path()
        for i in range(30):
            a = math.radians(195 + 150 * i / 29)
            px = ex + eye_rx * 1.01 * math.cos(a)
            py = ey + eye_ry * 0.97 * math.sin(a)
            if i == 0:
                ctx.move_to(px, py)
            else:
                ctx.line_to(px, py)
        _set_color(ctx, LINE_COL)
        ctx.set_line_width(lw_silhouette); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
        # Iris and pupil — gaze dx shared both eyes in front view
        gaze_dx = spec["gaze_dx"] * s * 0.5  # reduced offset in front view
        gaze_dy = spec["gaze_dy"] * s
        iris_r = eye_rx * 0.68
        iris_ry = eye_ry * 0.62
        iris_cx = ex + gaze_dx
        iris_cy = ey + gaze_dy
        _draw_ellipse_path(ctx, iris_cx, iris_cy, iris_r, iris_ry)
        _set_color(ctx, EYE_IRIS); ctx.fill()
        pup_r = iris_r * 0.52
        pup_ry = iris_ry * 0.52
        _draw_ellipse_path(ctx, iris_cx, iris_cy, pup_r, pup_ry)
        _set_color(ctx, EYE_PUP); ctx.fill()
        hl_r = max(pup_r * 0.42, 3)
        ctx.new_path()
        ctx.arc(iris_cx + iris_r * 0.32, iris_cy - iris_ry * 0.32, hl_r, 0, 2 * math.pi)
        _set_color(ctx, EYE_HL); ctx.fill()

    # ── Brows ──
    doubt_wince = spec.get("doubt_wince", False)
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
        _set_color(ctx, HAIR)
        ctx.set_line_width(lw_major); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
        if doubt_wince and side == -1:
            kink_x = inner_x
            kink_y = by + 2*s
            ctx.new_path()
            ctx.move_to(kink_x, kink_y)
            ctx.curve_to(kink_x - 4*s, kink_y - 8*s,
                         kink_x - 8*s, kink_y - 12*s,
                         kink_x - 6*s, kink_y - 14*s)
            _set_color(ctx, HAIR)
            ctx.set_line_width(lw_minor); ctx.stroke()

    # ── Nose (front — simple centered dot-comma) ──
    nose_y = head_r * 0.28
    ctx.new_path()
    ctx.arc(0, nose_y, 2.5*s, 0, 2*math.pi)
    _set_color(ctx, SKIN_SH, 0.8); ctx.fill()

    # ── Mouth ──
    mouth_y = head_r * 0.44
    mouth_w = head_rx * 0.30
    mouth_type = spec["mouth"]
    if mouth_type == "gentle_smile":
        ctx.new_path()
        ctx.move_to(-mouth_w, mouth_y + 1*s)
        ctx.curve_to(-mouth_w * 0.3, mouth_y - 6*s, mouth_w * 0.3, mouth_y - 6*s,
                     mouth_w, mouth_y - 1*s)
        _set_color(ctx, LINE_COL); ctx.set_line_width(lw_minor); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    elif mouth_type == "firm_line":
        ctx.new_path()
        ctx.move_to(-mouth_w * 0.8, mouth_y)
        ctx.curve_to(-mouth_w * 0.2, mouth_y - 2*s, mouth_w * 0.2, mouth_y - 2*s,
                     mouth_w * 0.8, mouth_y)
        _set_color(ctx, LINE_COL); ctx.set_line_width(lw_major); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    elif mouth_type == "open_o":
        mouth_rx = mouth_w * 0.6
        mouth_ry = head_r * 0.12
        _draw_ellipse_path(ctx, 0, mouth_y + 2*s, mouth_rx, mouth_ry)
        _set_color(ctx, (0.15, 0.08, 0.06)); ctx.fill_preserve()
        _set_color(ctx, LINE_COL); ctx.set_line_width(lw_minor); ctx.stroke()
    elif mouth_type == "tight_frown":
        ctx.new_path()
        ctx.move_to(-mouth_w * 0.7, mouth_y - 2*s)
        ctx.curve_to(-mouth_w * 0.2, mouth_y + 4*s, mouth_w * 0.2, mouth_y + 4*s,
                     mouth_w * 0.7, mouth_y - 2*s)
        _set_color(ctx, LINE_COL); ctx.set_line_width(lw_minor); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    elif mouth_type == "wide_grin":
        mouth_rx = mouth_w * 0.85
        mouth_ry = head_r * 0.10
        _draw_ellipse_path(ctx, 0, mouth_y + 1*s, mouth_rx, mouth_ry)
        _set_color(ctx, (0.15, 0.08, 0.06)); ctx.fill_preserve()
        _set_color(ctx, LINE_COL); ctx.set_line_width(lw_minor); ctx.stroke()
        ctx.new_path()
        ctx.move_to(-mouth_rx * 0.7, mouth_y + 1*s)
        ctx.line_to(mouth_rx * 0.7, mouth_y + 1*s)
        _set_color(ctx, EYE_W); ctx.set_line_width(3*s); ctx.stroke()
    elif mouth_type == "gritted_teeth":
        mouth_rx = mouth_w * 0.65
        mouth_ry = head_r * 0.07
        _draw_ellipse_path(ctx, 0, mouth_y + 2*s, mouth_rx, mouth_ry)
        _set_color(ctx, (0.15, 0.08, 0.06)); ctx.fill_preserve()
        _set_color(ctx, LINE_COL); ctx.set_line_width(lw_minor); ctx.stroke()

    # Blush
    for side in [-1, 1]:
        _draw_ellipse_path(ctx, side * eye_spacing * 0.85, head_r * 0.24, 18*s, 10*s)
        _set_color(ctx, BLUSH_C); ctx.fill()

    ctx.restore()

    return {
        "head_cx": head_cx, "head_cy": head_cy,
        "head_r": head_r, "head_rx": head_rx, "head_ry": head_ry,
        "torso_cx": torso_cx, "torso_cy": torso_cy,
        "hip_cx": hip_cx, "ground_y": ground_y, "char_h": char_h,
    }


def _draw_luma_threequarter(ctx, cx, ground_y, char_h, expression, spec, scale=1.0):
    """Render Luma in 3/4 view — angle between front and side.

    One eye dominant (near side), one eye partially visible (far side, smaller/narrower).
    Torso slightly narrowed on far side. Uses side-view skeleton with adjustments.
    Returns layout dict.
    """
    rng = random.Random(SEED + hash(expression) + 2002)

    head_h = char_h * LUMA_HEAD_RATIO
    head_r = head_h / 2
    body_h = char_h - head_h
    s = head_r / 100.0

    lw_silhouette = max(4.0, 5.0 * s)
    lw_major = max(3.0, 3.5 * s)
    lw_minor = max(2.0, 2.5 * s)
    lw_accent = max(1.5, 2.0 * s)

    # 3/4 view: offset chain active but compressed vs side view
    hip_shift = spec["hip_shift"] * s * 0.5
    shoulder_offset = spec["shoulder_offset"] * s * 0.5
    head_offset = spec["head_offset"] * s * 0.5
    torso_lean = spec["torso_lean"] * s * 0.4

    hip_cx = cx + hip_shift
    torso_cx = hip_cx + shoulder_offset
    head_cx = torso_cx + head_offset

    hip_tilt_px = spec["hip_tilt"] * s * 0.6
    shoulder_tilt_px = spec["shoulder_tilt"] * s * 0.6
    # 3/4 view torso: foreshortened, ~70-75% of front view width (front=0.95).
    sh_w = head_r * 0.70

    head_cy = ground_y - char_h + head_r
    neck_bot_y = head_cy + head_r + head_r * 0.25
    torso_h = body_h * 0.38
    torso_cy = neck_bot_y + torso_h / 2
    torso_bot_y = neck_bot_y + torso_h
    leg_h = ground_y - torso_bot_y

    hoodie, hoodie_sh = HOODIE_COLORS.get(expression, (HOODIE_SURPRISED, HOODIE_SURPRISED_SH))

    # ══ LEGS (3/4 view — fore/aft stagger + slight X offset) ══
    # In 3/4 view, the legs are NOT spread purely left/right (that's front view).
    # Near leg (closer to viewer) is lower on canvas and slightly to the near side.
    # Far leg is higher on canvas and slightly to the far side.
    # Both X positions stagger: near leg slightly forward in the picture plane,
    # far leg slightly behind — creating a genuine depth read.
    leg_w_top = head_r * 0.22
    leg_w_bot = head_r * 0.18
    leg_overlap = leg_w_top * 0.8

    weight_front = spec["weight_front"]
    front_foot_lift = spec["front_foot_lift"] * s
    back_foot_lift = spec["back_foot_lift"] * s
    heel_lift = spec.get("heel_lift", 0) * s
    stance_mult = spec.get("stance_wide", 1.0)

    # Legs centered at hip_cx; depth read via y-axis only
    near_leg_x = hip_cx  # near leg centered
    far_leg_x  = hip_cx  # far leg centered
    # Y offset: near foot sits lower (front of body plane), far foot slightly higher
    near_extra_y = 0   # near leg at normal ground
    far_extra_lift = head_r * 0.06  # far foot slightly raised = depth recession

    # Far leg first (behind near); slight knee bow for visual interest
    bl_top = (far_leg_x, torso_bot_y - leg_overlap)
    bl_knee = (far_leg_x - 2*s, torso_bot_y + leg_h * 0.49)
    bl_ankle = (far_leg_x + 1*s, ground_y - back_foot_lift - far_extra_lift - heel_lift - head_r * 0.25)
    back_leg_pts = _bezier_points(bl_top, bl_knee,
                                  (bl_knee[0], bl_knee[1] + leg_h * 0.2),
                                  bl_ankle, steps=30)
    _draw_variable_stroke_limb(ctx, back_leg_pts, leg_w_top, leg_w_bot * 0.90,
                               PANTS, LINE_COL, lw_major)

    # Near leg on top; slight knee bow forward
    fl_top = (near_leg_x, torso_bot_y - leg_overlap)
    fl_knee = (near_leg_x + 3*s, torso_bot_y + leg_h * 0.48)
    fl_ankle = (near_leg_x + 2*s, ground_y - front_foot_lift - heel_lift - head_r * 0.25)
    front_leg_pts = _bezier_points(fl_top, fl_knee,
                                   (fl_knee[0] - 1*s, fl_knee[1] + leg_h * 0.2),
                                   fl_ankle, steps=30)
    _draw_variable_stroke_limb(ctx, front_leg_pts, leg_w_top, leg_w_bot,
                               PANTS, LINE_COL, lw_major)

    # Hip bridge
    hip_bw = leg_w_top * 1.4  # legs centered, so width from leg_w_top only
    hip_bridge_cx = hip_cx
    hip_bridge_y_top = torso_bot_y - torso_h * 0.04
    hip_bridge_y_bot = torso_bot_y + leg_w_top * 1.2
    ctx.new_path()
    ctx.move_to(hip_bridge_cx - hip_bw, hip_bridge_y_top)
    ctx.curve_to(hip_bridge_cx - hip_bw * 0.8, hip_bridge_y_bot + 4*s,
                 hip_bridge_cx + hip_bw * 0.8, hip_bridge_y_bot + 4*s,
                 hip_bridge_cx + hip_bw, hip_bridge_y_top)
    ctx.curve_to(hip_bridge_cx + hip_bw * 0.6, hip_bridge_y_top - 4*s,
                 hip_bridge_cx - hip_bw * 0.6, hip_bridge_y_top - 4*s,
                 hip_bridge_cx - hip_bw, hip_bridge_y_top)
    ctx.close_path()
    _set_color(ctx, PANTS); ctx.fill()

    # Shoes
    shoe_w = head_r * 0.30
    shoe_h = head_r * 0.18
    # Far shoe (receding): slightly smaller and angled back
    ctx.save()
    ctx.translate(back_leg_pts[-1][0], ground_y - back_foot_lift - far_extra_lift - heel_lift - shoe_h * 0.3)
    ctx.rotate(math.radians(spec["back_foot_angle"] * 0.4))
    _draw_ellipse_path(ctx, 0, 0, shoe_w * 0.88, shoe_h * 0.88)
    _set_color(ctx, SHOE); ctx.fill_preserve()
    _set_color(ctx, LINE_COL); ctx.set_line_width(lw_major); ctx.stroke()
    ctx.new_path()
    ctx.move_to(-shoe_w * 0.7, shoe_h * 0.4)
    ctx.curve_to(-shoe_w * 0.2, shoe_h * 0.65, shoe_w * 0.2, shoe_h * 0.65, shoe_w * 0.65, shoe_h * 0.3)
    _set_color(ctx, SHOE_SOLE); ctx.set_line_width(lw_minor); ctx.stroke()
    ctx.restore()
    # Near shoe (foreground): full size
    ctx.save()
    ctx.translate(front_leg_pts[-1][0], ground_y - front_foot_lift - heel_lift - shoe_h * 0.3)
    ctx.rotate(math.radians(spec["front_foot_angle"] * 0.6))
    _draw_ellipse_path(ctx, 0, 0, shoe_w, shoe_h)
    _set_color(ctx, SHOE); ctx.fill_preserve()
    _set_color(ctx, LINE_COL); ctx.set_line_width(lw_major); ctx.stroke()
    ctx.new_path()
    ctx.move_to(-shoe_w * 0.8, shoe_h * 0.4)
    ctx.curve_to(-shoe_w * 0.3, shoe_h * 0.7, shoe_w * 0.3, shoe_h * 0.7,
                 shoe_w * 0.8, shoe_h * 0.3)
    _set_color(ctx, SHOE_SOLE); ctx.set_line_width(lw_minor); ctx.stroke()
    ctx.new_path()
    ctx.arc(0, -shoe_h * 0.2, 2 * s, 0, 2 * math.pi)
    _set_color(ctx, LACES); ctx.fill()
    ctx.restore()

    # ══ TORSO ══
    w_top = sh_w
    # 3/4 view: hips also foreshortened. w_bot proportional to narrower sh_w.
    w_bot = head_r * 0.48
    attach = _draw_bean_torso(ctx, torso_cx, torso_cy, w_top, w_bot, torso_h,
                              torso_lean, hip_tilt_px, shoulder_tilt_px)
    ls_pt, rs_pt, lh_pt, rh_pt = attach
    _set_color(ctx, hoodie); ctx.fill_preserve()
    _set_color(ctx, LINE_COL); ctx.set_line_width(lw_silhouette); ctx.stroke()

    shadow_x1 = torso_cx + torso_lean + sh_w * 0.2
    shadow_y1 = torso_cy - torso_h / 2
    ctx.new_path()
    ctx.move_to(shadow_x1, shadow_y1)
    ctx.curve_to(shadow_x1 + sh_w * 0.3, shadow_y1 + torso_h * 0.3,
                 shadow_x1 + w_bot * 0.4, shadow_y1 + torso_h * 0.8,
                 shadow_x1 + w_bot * 0.1, shadow_y1 + torso_h)
    ctx.line_to(torso_cx + torso_lean * 0.5 + w_bot, shadow_y1 + torso_h)
    ctx.line_to(shadow_x1 + sh_w * 0.5, shadow_y1)
    ctx.close_path()
    _set_color(ctx, hoodie_sh, 0.4); ctx.fill()

    collar_cx = torso_cx + torso_lean * 0.5
    collar_y = torso_cy - torso_h / 2
    collar_w = head_r * 0.32
    ctx.new_path()
    ctx.move_to(collar_cx - collar_w, collar_y + 2 * s)
    ctx.curve_to(collar_cx - collar_w * 0.3, collar_y + 14 * s,
                 collar_cx + collar_w * 0.3, collar_y + 14 * s,
                 collar_cx + collar_w, collar_y + 2 * s)
    _set_color(ctx, (250/255, 232/255, 200/255)); ctx.set_line_width(max(5, 6 * s)); ctx.stroke_preserve()
    _set_color(ctx, LINE_COL); ctx.set_line_width(lw_minor); ctx.stroke()

    hem_y = torso_bot_y - torso_h * 0.10
    ctx.new_path()
    ctx.move_to(lh_pt[0] + 3*s, hem_y)
    ctx.curve_to(hip_cx - w_bot * 0.3, hem_y + 4*s,
                 hip_cx + w_bot * 0.3, hem_y + 4*s,
                 rh_pt[0] - 3*s, hem_y)
    _set_color(ctx, hoodie_sh); ctx.set_line_width(max(3, 4 * s)); ctx.stroke()

    for _ in range(12):
        px_x = torso_cx + torso_lean + rng.uniform(-16*s, 16*s)
        px_y = torso_cy + rng.uniform(-12*s, 12*s)
        psz = max(2, rng.choice([2*s, 3*s, 4*s]))
        pc = rng.choice([PX_CYAN, PX_MAG, (0.94, 0.94, 0.94)])
        ctx.rectangle(px_x, px_y, psz, psz)
        _set_color(ctx, pc); ctx.fill()

    # ══ ARMS (3/4 — inline for correct height; near arm prominent, far arm partially hidden) ══
    # Arms drawn inline (not via _draw_arms dispatch which is tuned for front view).
    # In 3/4 view, arms hang down naturally with hands at hip/waist height.
    # Near arm (rs_pt = right/near shoulder): hangs relaxed with slight forward bend.
    # Far arm (ls_pt = left/far shoulder): partially behind body, bent back.
    arm_w_top = head_r * 0.14
    arm_w_bot = head_r * 0.10
    hand_r_s = head_r * 0.12

    # Near arm (rs_pt side, prominent)
    na_shoulder = (rs_pt[0] + 6*s, rs_pt[1] + 5*s)
    na_elbow    = (na_shoulder[0] + 18*s, na_shoulder[1] + 26*s)
    na_hand     = (na_elbow[0] + 10*s,   na_elbow[1]    + 26*s)
    near_arm_pts = (_bezier_points(na_shoulder,
                                   (na_shoulder[0] + 5*s, na_shoulder[1] + 10*s),
                                   (na_elbow[0] - 4*s, na_elbow[1] - 8*s), na_elbow, steps=25) +
                    _bezier_points(na_elbow,
                                   (na_elbow[0] + 4*s, na_elbow[1] + 8*s),
                                   (na_hand[0] - 3*s, na_hand[1] - 4*s), na_hand, steps=25)[1:])
    _draw_unified_arm(ctx, near_arm_pts, arm_w_top, arm_w_bot, hoodie, LINE_COL, lw_major)
    _draw_ellipse_path(ctx, na_hand[0], na_hand[1], hand_r_s, hand_r_s * 0.80)
    _set_color(ctx, SKIN); ctx.fill_preserve()
    _set_color(ctx, LINE_COL); ctx.set_line_width(lw_minor); ctx.stroke()

    # Far arm (ls_pt side, partially behind body, drawn at reduced opacity/width)
    fa_shoulder = (ls_pt[0] - 5*s, ls_pt[1] + 5*s)
    fa_elbow    = (fa_shoulder[0] - 16*s, fa_shoulder[1] + 22*s)
    fa_hand     = (fa_elbow[0] + 4*s,    fa_elbow[1]    + 24*s)
    far_arm_pts = (_bezier_points(fa_shoulder,
                                  (fa_shoulder[0] - 5*s, fa_shoulder[1] + 8*s),
                                  (fa_elbow[0] + 4*s, fa_elbow[1] - 6*s), fa_elbow, steps=25) +
                   _bezier_points(fa_elbow,
                                  (fa_elbow[0] - 3*s, fa_elbow[1] + 7*s),
                                  (fa_hand[0] + 3*s, fa_hand[1] - 4*s), fa_hand, steps=25)[1:])
    _draw_unified_arm(ctx, far_arm_pts, arm_w_top * 0.85, arm_w_bot * 0.85, hoodie, LINE_COL, lw_major)
    _draw_ellipse_path(ctx, fa_hand[0], fa_hand[1], hand_r_s * 0.80, hand_r_s * 0.65)
    _set_color(ctx, SKIN); ctx.fill_preserve()
    _set_color(ctx, LINE_COL); ctx.set_line_width(lw_minor); ctx.stroke()

    # ══ NECK ══
    neck_top_y = head_cy + head_r * 0.95
    neck_w_top = head_r * 0.22
    neck_w_bot = head_r * 0.30
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
    _set_color(ctx, SKIN); ctx.fill_preserve()
    _set_color(ctx, LINE_COL); ctx.set_line_width(lw_minor); ctx.stroke()

    # ══ HEAD (3/4) — near eye normal, far eye narrower ══
    head_rx = head_r * 1.06
    head_ry = head_r
    tilt_rad = math.radians(spec["head_tilt"] * 0.7)

    ctx.save()
    ctx.translate(head_cx, head_cy)
    ctx.rotate(tilt_rad)

    # 3/4 head shape: bulges toward the near side (left = -x = near side facing viewer).
    # Right side (+x = far side) is tapered/compressed — partial profile silhouette.
    ctx.new_path()
    steps = 120
    for i in range(steps):
        angle = i * 2 * math.pi / steps
        rx = head_rx
        ry = head_ry
        # Chin projects down
        chin_f = max(0, math.cos(angle - math.pi / 2)) ** 2.5
        ry += head_r * 0.10 * chin_f
        rx -= head_r * 0.03 * chin_f
        # Near cheek (left = -x = angle near pi): fuller/rounder
        near_cheek_f = max(0, math.cos(angle - math.pi)) ** 5
        rx += head_r * 0.12 * near_cheek_f
        # Far side (+x = angle near 0): slightly compressed
        far_f = max(0, math.cos(angle)) ** 6
        rx -= head_r * 0.08 * far_f
        # Near-side cheek bump (around -0.4 radians offset from pi)
        side_cheek_f = max(0, math.cos(angle - (math.pi - 0.5))) ** 8
        rx += head_r * 0.06 * side_cheek_f
        px = rx * math.cos(angle)
        py = ry * math.sin(angle)
        if i == 0:
            ctx.move_to(px, py)
        else:
            ctx.line_to(px, py)
    ctx.close_path()
    _set_color(ctx, SKIN); ctx.fill_preserve()
    ctx.set_line_width(lw_silhouette)
    _set_color(ctx, LINE_COL); ctx.stroke()

    # Hair cloud (3/4 — weighted toward near side/back)
    hair_blobs = [
        (0, -0.65, 0.70, 0.55), (-0.50, -0.50, 0.60, 0.52),
        (0.40, -0.50, 0.45, 0.42), (-0.30, -0.95, 0.42, 0.36),
        (0.25, -0.95, 0.35, 0.30), (0, -1.10, 0.36, 0.30),
        (-0.85, -0.30, 0.38, 0.40), (0.75, -0.28, 0.30, 0.34),
        (-0.75, -0.62, 0.36, 0.34), (0.65, -0.58, 0.28, 0.28),
        (-0.15, -0.45, 0.62, 0.44), (0.12, -0.45, 0.55, 0.40),
        (-0.52, -0.80, 0.34, 0.28), (0.45, -0.78, 0.26, 0.24),
        (-0.45, -1.05, 0.26, 0.22), (0.40, -1.02, 0.22, 0.18),
        (0.10, -1.15, 0.22, 0.20), (-0.92, -0.48, 0.24, 0.28),
    ]
    for (bx, by, brx, bry) in hair_blobs:
        _draw_ellipse_path(ctx, bx * head_rx, by * head_ry, brx * head_rx, bry * head_ry)
        _set_color(ctx, HAIR); ctx.fill()
    for (bx, by, brx, bry) in [(-0.35, -0.85, 0.22, 0.13),
                                 (0.18, -0.72, 0.14, 0.10),
                                 (-0.58, -0.55, 0.14, 0.10)]:
        _draw_ellipse_path(ctx, bx * head_rx, by * head_ry, brx * head_rx, bry * head_ry)
        _set_color(ctx, HAIR_HL); ctx.fill()

    # Face skin — offset toward near side (slightly -x), leaving far corner less covered
    _draw_ellipse_path(ctx, -head_rx * 0.06, head_r * 0.10, head_rx * 0.85, head_ry * 0.70)
    _set_color(ctx, SKIN); ctx.fill()

    # Eyes: near side normal, far side foreshortened
    # Near eye at standard spacing; far eye compressed by 3/4 foreshortening
    eye_y = head_r * 0.05
    near_eye_x = -head_rx * 0.38   # near eye (left, toward viewer)
    far_eye_x = head_rx * 0.26     # far eye (right, receding)
    eye_rx_near = head_rx * 0.26
    eye_ry_near = head_ry * 0.30 * spec["eye_openness"]
    eye_rx_far = head_rx * 0.14   # far eye foreshortened
    eye_ry_far = eye_ry_near * 0.88

    gaze_dx = spec["gaze_dx"] * s
    gaze_dy = spec["gaze_dy"] * s

    for (ex, eye_rx_v, eye_ry_v, g_dx) in [
        (near_eye_x, eye_rx_near, eye_ry_near, gaze_dx * 0.8),
        (far_eye_x, eye_rx_far, eye_ry_far, gaze_dx * 0.3),
    ]:
        _draw_ellipse_path(ctx, ex, eye_y, eye_rx_v, eye_ry_v)
        _set_color(ctx, EYE_W); ctx.fill_preserve()
        _set_color(ctx, LINE_COL); ctx.set_line_width(lw_minor); ctx.stroke()
        ctx.new_path()
        for i in range(30):
            a = math.radians(195 + 150 * i / 29)
            px = ex + eye_rx_v * 1.01 * math.cos(a)
            py = eye_y + eye_ry_v * 0.97 * math.sin(a)
            if i == 0:
                ctx.move_to(px, py)
            else:
                ctx.line_to(px, py)
        _set_color(ctx, LINE_COL)
        ctx.set_line_width(lw_silhouette); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
        iris_r = eye_rx_v * 0.68
        iris_ry = eye_ry_v * 0.62
        _draw_ellipse_path(ctx, ex + g_dx, eye_y + gaze_dy, iris_r, iris_ry)
        _set_color(ctx, EYE_IRIS); ctx.fill()
        _draw_ellipse_path(ctx, ex + g_dx, eye_y + gaze_dy, iris_r * 0.52, iris_ry * 0.52)
        _set_color(ctx, EYE_PUP); ctx.fill()
        hl_r = max(iris_r * 0.42 * 0.52, 3)
        ctx.new_path()
        ctx.arc(ex + g_dx + iris_r * 0.32, eye_y + gaze_dy - iris_ry * 0.32, hl_r, 0, 2*math.pi)
        _set_color(ctx, EYE_HL); ctx.fill()

    # Brows: near brow normal, far brow foreshortened
    doubt_wince = spec.get("doubt_wince", False)
    for (side, lift, is_near) in [(-1, spec["brow_lift_l"] * s, True),
                                   (1, spec["brow_lift_r"] * s, False)]:
        bx = near_eye_x if is_near else far_eye_x
        by = eye_y - (eye_ry_near if is_near else eye_ry_far) - 6*s - lift
        inner_x = bx + side * (18*s if is_near else 10*s)
        outer_x = bx - side * (20*s if is_near else 10*s)
        ctx.new_path()
        ctx.move_to(outer_x, by + 4*s)
        ctx.curve_to((outer_x + bx) / 2, by - 4*s,
                     (bx + inner_x) / 2, by - 2*s,
                     inner_x, by + 2*s)
        _set_color(ctx, HAIR)
        ctx.set_line_width(lw_major if is_near else lw_minor)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
        if doubt_wince and is_near:
            kink_x = inner_x
            kink_y = by + 2*s
            ctx.new_path()
            ctx.move_to(kink_x, kink_y)
            ctx.curve_to(kink_x - 4*s, kink_y - 8*s,
                         kink_x - 8*s, kink_y - 12*s,
                         kink_x - 6*s, kink_y - 14*s)
            _set_color(ctx, HAIR)
            ctx.set_line_width(lw_accent); ctx.stroke()

    # Nose (3/4 — asymmetric, shows bridge angle)
    nose_x = head_rx * 0.08
    nose_y = head_r * 0.28
    ctx.new_path()
    ctx.move_to(nose_x - 3*s, nose_y)
    ctx.curve_to(nose_x, nose_y + 3*s, nose_x + 3*s, nose_y + 1*s, nose_x + 5*s, nose_y - 1*s)
    _set_color(ctx, SKIN_SH)
    ctx.set_line_width(lw_minor); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()

    # Mouth (3/4 — offset toward near side)
    mouth_y = head_r * 0.44
    mouth_w = head_rx * 0.28
    mouth_ox = -head_rx * 0.06  # slight offset toward near side
    mouth_type = spec["mouth"]
    if mouth_type == "gentle_smile":
        ctx.new_path()
        ctx.move_to(mouth_ox - mouth_w, mouth_y + 1*s)
        ctx.curve_to(mouth_ox - mouth_w * 0.3, mouth_y - 6*s,
                     mouth_ox + mouth_w * 0.3, mouth_y - 6*s,
                     mouth_ox + mouth_w, mouth_y - 1*s)
        _set_color(ctx, LINE_COL); ctx.set_line_width(lw_minor); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    elif mouth_type == "firm_line":
        ctx.new_path()
        ctx.move_to(mouth_ox - mouth_w * 0.8, mouth_y)
        ctx.curve_to(mouth_ox - mouth_w * 0.2, mouth_y - 2*s,
                     mouth_ox + mouth_w * 0.2, mouth_y - 2*s,
                     mouth_ox + mouth_w * 0.8, mouth_y)
        _set_color(ctx, LINE_COL); ctx.set_line_width(lw_major); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    elif mouth_type == "open_o":
        mouth_rx2 = mouth_w * 0.5
        mouth_ry2 = head_r * 0.10
        _draw_ellipse_path(ctx, mouth_ox, mouth_y + 2*s, mouth_rx2, mouth_ry2)
        _set_color(ctx, (0.15, 0.08, 0.06)); ctx.fill_preserve()
        _set_color(ctx, LINE_COL); ctx.set_line_width(lw_minor); ctx.stroke()
    elif mouth_type == "wide_grin":
        mouth_rx2 = mouth_w * 0.80
        mouth_ry2 = head_r * 0.09
        _draw_ellipse_path(ctx, mouth_ox, mouth_y + 1*s, mouth_rx2, mouth_ry2)
        _set_color(ctx, (0.15, 0.08, 0.06)); ctx.fill_preserve()
        _set_color(ctx, LINE_COL); ctx.set_line_width(lw_minor); ctx.stroke()
    elif mouth_type in ("tight_frown", "gritted_teeth"):
        ctx.new_path()
        ctx.move_to(mouth_ox - mouth_w * 0.7, mouth_y - 2*s)
        ctx.curve_to(mouth_ox - mouth_w * 0.2, mouth_y + 4*s,
                     mouth_ox + mouth_w * 0.2, mouth_y + 4*s,
                     mouth_ox + mouth_w * 0.7, mouth_y - 2*s)
        _set_color(ctx, LINE_COL); ctx.set_line_width(lw_minor); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()

    # Blush (near cheek only in 3/4)
    _draw_ellipse_path(ctx, near_eye_x * 0.85, head_r * 0.24, 18*s, 10*s)
    _set_color(ctx, BLUSH_C); ctx.fill()

    ctx.restore()

    return {
        "head_cx": head_cx, "head_cy": head_cy,
        "head_r": head_r, "head_rx": head_rx, "head_ry": head_ry,
        "torso_cx": torso_cx, "torso_cy": torso_cy,
        "hip_cx": hip_cx, "ground_y": ground_y, "char_h": char_h,
    }


def _draw_luma_back(ctx, cx, ground_y, char_h, expression, spec, scale=1.0):
    """Render Luma from the BACK — rear view.

    Shows: cloud hair from behind, hoodie back (no collar V, back seam),
    rear leg silhouette, feet visible under torso.
    No face features. Back of neck visible.
    Returns layout dict.
    """
    rng = random.Random(SEED + hash(expression) + 3003)

    head_h = char_h * LUMA_HEAD_RATIO
    head_r = head_h / 2
    body_h = char_h - head_h
    s = head_r / 100.0

    lw_silhouette = max(4.0, 5.0 * s)
    lw_major = max(3.0, 3.5 * s)
    lw_minor = max(2.0, 2.5 * s)
    lw_accent = max(1.5, 2.0 * s)

    # Back view: near-symmetric, small hip shift for life
    hip_shift = spec["hip_shift"] * s * 0.25
    torso_lean = spec["torso_lean"] * s * 0.1
    hip_cx = cx + hip_shift
    torso_cx = hip_cx
    head_cx = cx

    hip_tilt_px = spec["hip_tilt"] * s * 0.5
    shoulder_tilt_px = spec["shoulder_tilt"] * s * 0.4
    sh_w = head_r * 0.90

    head_cy = ground_y - char_h + head_r
    neck_bot_y = head_cy + head_r + head_r * 0.25
    torso_h = body_h * 0.38
    torso_cy = neck_bot_y + torso_h / 2
    torso_bot_y = neck_bot_y + torso_h
    leg_h = ground_y - torso_bot_y

    hoodie, hoodie_sh = HOODIE_COLORS.get(expression, (HOODIE_SURPRISED, HOODIE_SURPRISED_SH))

    leg_offset = head_r * 0.42 * spec.get("stance_wide", 1.0)
    leg_w_top = head_r * 0.22
    leg_w_bot = head_r * 0.18
    leg_overlap = leg_w_top * 0.8

    front_foot_lift = spec["front_foot_lift"] * s * 0.5
    back_foot_lift = spec["back_foot_lift"] * s * 0.5
    heel_lift = spec.get("heel_lift", 0) * s

    fl_x = hip_cx - leg_offset
    fr_x = hip_cx + leg_offset

    for (lx, foot_lift, knee_drift) in [
        (fl_x, front_foot_lift, 2),
        (fr_x, back_foot_lift, -2),
    ]:
        lp_top = (lx, torso_bot_y - leg_overlap)
        lp_knee = (lx + knee_drift * s, torso_bot_y + leg_h * 0.48)
        lp_ankle = (lx, ground_y - foot_lift - heel_lift - head_r * 0.25)
        leg_pts = _bezier_points(lp_top, lp_knee,
                                 (lp_knee[0], lp_knee[1] + leg_h * 0.2),
                                 lp_ankle, steps=30)
        _draw_variable_stroke_limb(ctx, leg_pts, leg_w_top, leg_w_bot,
                                   PANTS, LINE_COL, lw_major)

    # Hip bridge
    hip_bw = leg_offset + leg_w_top * 1.3
    hip_bridge_y_top = torso_bot_y - torso_h * 0.04
    hip_bridge_y_bot = torso_bot_y + leg_w_top * 1.2
    ctx.new_path()
    ctx.move_to(cx - hip_bw, hip_bridge_y_top)
    ctx.curve_to(cx - hip_bw * 0.8, hip_bridge_y_bot + 4*s,
                 cx + hip_bw * 0.8, hip_bridge_y_bot + 4*s,
                 cx + hip_bw, hip_bridge_y_top)
    ctx.curve_to(cx + hip_bw * 0.6, hip_bridge_y_top - 4*s,
                 cx - hip_bw * 0.6, hip_bridge_y_top - 4*s,
                 cx - hip_bw, hip_bridge_y_top)
    ctx.close_path()
    _set_color(ctx, PANTS); ctx.fill()

    # Shoes (seen from behind — show heel/sole)
    shoe_w = head_r * 0.28
    shoe_h = head_r * 0.18
    for (sx, foot_lift) in [(fl_x, front_foot_lift), (fr_x, back_foot_lift)]:
        ctx.save()
        ctx.translate(sx, ground_y - foot_lift - heel_lift - shoe_h * 0.2)
        _draw_ellipse_path(ctx, 0, 0, shoe_w * 0.75, shoe_h * 0.85)
        _set_color(ctx, SHOE); ctx.fill_preserve()
        _set_color(ctx, LINE_COL); ctx.set_line_width(lw_major); ctx.stroke()
        # Heel visible from back
        ctx.new_path()
        ctx.move_to(-shoe_w * 0.6, shoe_h * 0.5)
        ctx.curve_to(-shoe_w * 0.2, shoe_h * 0.8,
                     shoe_w * 0.2, shoe_h * 0.8,
                     shoe_w * 0.6, shoe_h * 0.5)
        _set_color(ctx, SHOE_SOLE); ctx.set_line_width(lw_minor); ctx.stroke()
        ctx.restore()

    # ══ TORSO (back) ══
    w_top = sh_w
    w_bot = head_r * 0.58
    attach = _draw_bean_torso(ctx, torso_cx, torso_cy, w_top, w_bot, torso_h,
                              torso_lean, hip_tilt_px, shoulder_tilt_px)
    ls_pt, rs_pt, lh_pt, rh_pt = attach
    _set_color(ctx, hoodie); ctx.fill_preserve()
    _set_color(ctx, LINE_COL); ctx.set_line_width(lw_silhouette); ctx.stroke()

    # Hoodie back: center seam line
    seam_top_y = torso_cy - torso_h / 2
    seam_bot_y = torso_cy + torso_h / 2
    ctx.new_path()
    ctx.move_to(torso_cx, seam_top_y + 4*s)
    ctx.curve_to(torso_cx + 2*s, torso_cy - torso_h * 0.1,
                 torso_cx - 2*s, torso_cy + torso_h * 0.1,
                 torso_cx, seam_bot_y - 4*s)
    _set_color(ctx, hoodie_sh, 0.7)
    ctx.set_line_width(lw_minor); ctx.stroke()

    # Hoodie back shadow panel (right side slightly darker)
    ctx.new_path()
    ctx.move_to(torso_cx, seam_top_y)
    ctx.curve_to(torso_cx + w_top * 0.2, seam_top_y + torso_h * 0.3,
                 torso_cx + w_bot * 0.3, seam_bot_y - torso_h * 0.2,
                 torso_cx + w_bot * 0.5, seam_bot_y)
    ctx.line_to(rs_pt[0], rs_pt[1])
    ctx.line_to(torso_cx, seam_top_y)
    ctx.close_path()
    _set_color(ctx, hoodie_sh, 0.3); ctx.fill()

    # Hoodie hem at back
    hem_y = torso_bot_y - torso_h * 0.10
    ctx.new_path()
    ctx.move_to(lh_pt[0] + 3*s, hem_y)
    ctx.curve_to(hip_cx - w_bot * 0.3, hem_y + 4*s,
                 hip_cx + w_bot * 0.3, hem_y + 4*s,
                 rh_pt[0] - 3*s, hem_y)
    _set_color(ctx, hoodie_sh); ctx.set_line_width(max(3, 4 * s)); ctx.stroke()

    # Pixel accents on back of hoodie
    for _ in range(8):
        px_x = torso_cx + rng.uniform(-14*s, 14*s)
        px_y = torso_cy + rng.uniform(-10*s, 10*s)
        psz = max(2, rng.choice([2*s, 3*s]))
        pc = rng.choice([PX_CYAN, PX_MAG])
        ctx.rectangle(px_x, px_y, psz, psz)
        _set_color(ctx, pc); ctx.fill()

    # ══ ARMS (back — simplified side view, arms hang or gesture behind) ══
    arm_w_top = head_r * 0.13
    arm_w_bot = head_r * 0.09
    hand_r_s = head_r * 0.11

    # Left arm (falls naturally to left side, seen from back)
    la_sh = (ls_pt[0] + 8*s, ls_pt[1] + 6*s)
    la_el = (la_sh[0] - 12*s, la_sh[1] + 38*s)
    la_hd = (la_el[0] - 4*s, la_el[1] + 32*s)
    l_pts = (_bezier_points(la_sh, (la_sh[0] - 6*s, la_sh[1] + 12*s),
                            (la_el[0] + 3*s, la_el[1] - 8*s), la_el, steps=20) +
             _bezier_points(la_el, (la_el[0] - 2*s, la_el[1] + 8*s),
                            (la_hd[0] + 2*s, la_hd[1] - 6*s), la_hd, steps=20)[1:])
    _draw_unified_arm(ctx, l_pts, arm_w_top, arm_w_bot, hoodie, LINE_COL, lw_major)
    _draw_ellipse_path(ctx, la_hd[0], la_hd[1], hand_r_s, hand_r_s * 0.8)
    _set_color(ctx, SKIN); ctx.fill_preserve()
    _set_color(ctx, LINE_COL); ctx.set_line_width(lw_minor); ctx.stroke()

    # Right arm
    ra_sh = (rs_pt[0] - 8*s, rs_pt[1] + 6*s)
    ra_el = (ra_sh[0] + 12*s, ra_sh[1] + 38*s)
    ra_hd = (ra_el[0] + 4*s, ra_el[1] + 32*s)
    r_pts = (_bezier_points(ra_sh, (ra_sh[0] + 6*s, ra_sh[1] + 12*s),
                            (ra_el[0] - 3*s, ra_el[1] - 8*s), ra_el, steps=20) +
             _bezier_points(ra_el, (ra_el[0] + 2*s, ra_el[1] + 8*s),
                            (ra_hd[0] - 2*s, ra_hd[1] - 6*s), ra_hd, steps=20)[1:])
    _draw_unified_arm(ctx, r_pts, arm_w_top, arm_w_bot, hoodie, LINE_COL, lw_major)
    _draw_ellipse_path(ctx, ra_hd[0], ra_hd[1], hand_r_s, hand_r_s * 0.8)
    _set_color(ctx, SKIN); ctx.fill_preserve()
    _set_color(ctx, LINE_COL); ctx.set_line_width(lw_minor); ctx.stroke()

    # ══ NECK (back — shows nape) ══
    neck_top_y = head_cy + head_r * 0.90
    neck_w_top = head_r * 0.20
    neck_w_bot = head_r * 0.28
    ctx.new_path()
    ctx.move_to(head_cx - neck_w_top, neck_top_y)
    ctx.curve_to(head_cx - neck_w_top, (neck_top_y + neck_bot_y) / 2,
                 torso_cx - neck_w_bot, neck_bot_y - 2*s,
                 torso_cx - neck_w_bot, neck_bot_y)
    ctx.line_to(torso_cx + neck_w_bot, neck_bot_y)
    ctx.curve_to(torso_cx + neck_w_bot, neck_bot_y - 2*s,
                 head_cx + neck_w_top, (neck_top_y + neck_bot_y) / 2,
                 head_cx + neck_w_top, neck_top_y)
    ctx.close_path()
    _set_color(ctx, SKIN); ctx.fill_preserve()
    _set_color(ctx, LINE_COL); ctx.set_line_width(lw_minor); ctx.stroke()
    # Nape crease
    ctx.new_path()
    ctx.move_to(head_cx - neck_w_top * 0.4, neck_top_y + 4*s)
    ctx.line_to(head_cx + neck_w_top * 0.4, neck_top_y + 4*s)
    _set_color(ctx, SKIN_SH); ctx.set_line_width(lw_accent); ctx.stroke()

    # ══ HEAD (back — hair cloud, no face) ══
    head_rx = head_r * 1.06
    head_ry = head_r
    tilt_rad = math.radians(spec["head_tilt"] * 0.3)

    ctx.save()
    ctx.translate(head_cx, head_cy)
    ctx.rotate(-tilt_rad)  # mirrored for back view

    # Head shape from behind (same silhouette, no face)
    ctx.new_path()
    steps = 100
    for i in range(steps):
        angle = i * 2 * math.pi / steps
        rx = head_rx
        ry = head_ry
        chin_f = max(0, math.cos(angle - math.pi / 2)) ** 2.5
        ry += head_r * 0.08 * chin_f
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
    _set_color(ctx, SKIN); ctx.fill_preserve()
    ctx.set_line_width(lw_silhouette)
    _set_color(ctx, LINE_COL); ctx.stroke()

    # Hair cloud from behind (fills the full head visible area)
    hair_blobs_back = [
        (0, -0.65, 0.75, 0.58), (-0.50, -0.50, 0.58, 0.52),
        (0.50, -0.50, 0.58, 0.52), (-0.30, -0.95, 0.42, 0.37),
        (0.30, -0.95, 0.42, 0.37), (0, -1.10, 0.38, 0.32),
        (-0.85, -0.30, 0.38, 0.40), (0.85, -0.30, 0.38, 0.40),
        (-0.70, -0.60, 0.38, 0.34), (0.70, -0.60, 0.38, 0.34),
        (-0.15, -0.45, 0.65, 0.45), (0.15, -0.45, 0.65, 0.45),
        (-0.50, -0.80, 0.35, 0.30), (0.50, -0.80, 0.35, 0.30),
        (-0.45, -1.05, 0.28, 0.24), (0.45, -1.05, 0.28, 0.24),
        (0.15, -1.15, 0.25, 0.22),
        # Extra blobs to cover face area in back view
        (0, 0.0, 0.72, 0.52), (-0.45, 0.0, 0.42, 0.38),
        (0.45, 0.0, 0.42, 0.38), (0, 0.20, 0.55, 0.40),
    ]
    for (bx, by, brx, bry) in hair_blobs_back:
        _draw_ellipse_path(ctx, bx * head_rx, by * head_ry, brx * head_rx, bry * head_ry)
        _set_color(ctx, HAIR); ctx.fill()

    # Hair highlights from behind
    for (bx, by, brx, bry) in [(0.30, -0.85, 0.22, 0.13),
                                 (-0.20, -0.72, 0.16, 0.10),
                                 (0.55, -0.55, 0.14, 0.10),
                                 (-0.10, -0.30, 0.18, 0.12)]:
        _draw_ellipse_path(ctx, bx * head_rx, by * head_ry, brx * head_rx, bry * head_ry)
        _set_color(ctx, HAIR_HL); ctx.fill()

    ctx.restore()

    return {
        "head_cx": head_cx, "head_cy": head_cy,
        "head_r": head_r, "head_rx": head_rx, "head_ry": head_ry,
        "torso_cx": torso_cx, "torso_cy": torso_cy,
        "hip_cx": hip_cx, "ground_y": ground_y, "char_h": char_h,
    }


def _draw_luma_side_l(ctx, cx, ground_y, char_h, expression, spec, scale=1.0):
    """Render Luma in SIDE-L view — native left-facing profile, distinct pose.

    NOT a mirror of the side view. This is a genuinely different stance:
    - Character faces LEFT (negative x direction)
    - Weight shifted to the back foot (right foot in world space = left in canvas)
    - Leading arm is in a relaxed-forward position
    - Trailing arm shows a different gesture read (bent behind hip)
    - Overall silhouette differs from SIDE view in arm and weight distribution

    Returns layout dict matching _draw_luma_on_context.
    """
    rng = random.Random(SEED + hash(expression) + 5005)

    head_h = char_h * LUMA_HEAD_RATIO
    head_r = head_h / 2
    body_h = char_h - head_h
    s = head_r / 100.0

    lw_silhouette = max(4.0, 5.0 * s)
    lw_major = max(3.0, 3.5 * s)
    lw_minor = max(2.0, 2.5 * s)
    lw_accent = max(1.5, 2.0 * s)

    # Side-L uses a different weight distribution: expression hip_shift is reversed/reduced,
    # weight is on the back foot creating a relaxed lean-back stance (distinct from SIDE lean-fwd).
    # Use a fixed moderate gesture spec regardless of expression — the pose beat is "returning/resting".
    SIDE_L_SPEC_OVERRIDES = {
        "hip_shift": -spec["hip_shift"] * 0.6,     # reversed lean
        "shoulder_offset": -spec["shoulder_offset"] * 0.5,
        "head_offset": spec["head_offset"] * 0.3,
        "torso_lean": -spec["torso_lean"] * 0.5,   # lean is now backward/reversed
        "hip_tilt": -spec["hip_tilt"] * 0.7,
        "shoulder_tilt": -spec["shoulder_tilt"] * 0.7,
        "head_tilt": -spec["head_tilt"] * 0.5,
        "weight_front": 1.0 - spec["weight_front"],   # weight reversed
        "front_foot_lift": spec["back_foot_lift"],
        "back_foot_lift": spec["front_foot_lift"],
    }
    merged = dict(spec)
    merged.update(SIDE_L_SPEC_OVERRIDES)
    spec_l = merged

    hip_shift = spec_l["hip_shift"] * s
    shoulder_offset = spec_l["shoulder_offset"] * s
    head_offset = spec_l["head_offset"] * s
    torso_lean = spec_l["torso_lean"] * s

    hip_cx = cx + hip_shift
    torso_cx = hip_cx + shoulder_offset
    head_cx = torso_cx + head_offset

    hip_tilt_px = spec_l["hip_tilt"] * s * 0.8
    shoulder_tilt_px = spec_l["shoulder_tilt"] * s * 0.8
    # Side-L is same viewing angle as SIDE — match the foreshortened torso width.
    sh_w = head_r * 0.50

    head_cy = ground_y - char_h + head_r
    neck_bot_y = head_cy + head_r + head_r * 0.25
    torso_h = body_h * 0.38
    torso_cy = neck_bot_y + torso_h / 2
    torso_bot_y = neck_bot_y + torso_h
    leg_h = ground_y - torso_bot_y

    hoodie, hoodie_sh = HOODIE_COLORS.get(expression, (HOODIE_SURPRISED, HOODIE_SURPRISED_SH))

    # ══ LEGS (side-L: left-facing, fore/aft stagger) ══
    leg_w_top = head_r * 0.22
    leg_w_bot = head_r * 0.18
    leg_overlap = leg_w_top * 0.8

    weight_front = spec_l["weight_front"]
    front_foot_lift = spec_l["front_foot_lift"] * s
    back_foot_lift = spec_l["back_foot_lift"] * s
    heel_lift = spec.get("heel_lift", 0) * s

    # Side-L faces left; both legs centered at hip_cx, depth read via y-axis only
    near_leg_x = hip_cx  # near leg centered
    far_leg_x  = hip_cx  # far leg centered
    far_extra_lift = head_r * 0.04  # far foot slightly higher = receding

    # Far leg first; slight knee bow for visual interest
    bl_top = (far_leg_x, torso_bot_y - leg_overlap)
    bl_knee = (far_leg_x + 2 * s, torso_bot_y + leg_h * 0.50)
    bl_ankle = (far_leg_x, ground_y - back_foot_lift - far_extra_lift - heel_lift - head_r * 0.25)
    back_leg_pts = _bezier_points(bl_top, bl_knee,
                                  (bl_knee[0], bl_knee[1] + leg_h * 0.2),
                                  bl_ankle, steps=30)
    _draw_variable_stroke_limb(ctx, back_leg_pts, leg_w_top, leg_w_bot,
                               PANTS, LINE_COL, lw_major)

    # Near leg on top; slight knee bow forward (leftward)
    fl_top = (near_leg_x, torso_bot_y - leg_overlap)
    fl_knee = (near_leg_x - 3 * s, torso_bot_y + leg_h * 0.48)
    fl_ankle = (near_leg_x - 2 * s, ground_y - front_foot_lift - heel_lift - head_r * 0.25)
    front_leg_pts = _bezier_points(fl_top, fl_knee,
                                   (fl_knee[0] + 1*s, fl_knee[1] + leg_h * 0.2),
                                   fl_ankle, steps=30)
    _draw_variable_stroke_limb(ctx, front_leg_pts, leg_w_top, leg_w_bot,
                               PANTS, LINE_COL, lw_major)

    # Hip bridge
    hip_bridge_y_top = torso_bot_y - torso_h * 0.04
    hip_bridge_y_bot = torso_bot_y + leg_w_top * 1.2
    hip_bw = leg_w_top * 1.4  # legs centered, so width from leg_w_top only
    hip_bridge_cx = hip_cx
    ctx.new_path()
    ctx.move_to(hip_bridge_cx - hip_bw, hip_bridge_y_top)
    ctx.curve_to(hip_bridge_cx - hip_bw * 0.8, hip_bridge_y_bot + 4*s,
                 hip_bridge_cx + hip_bw * 0.8, hip_bridge_y_bot + 4*s,
                 hip_bridge_cx + hip_bw, hip_bridge_y_top)
    ctx.curve_to(hip_bridge_cx + hip_bw * 0.6, hip_bridge_y_top - 4*s,
                 hip_bridge_cx - hip_bw * 0.6, hip_bridge_y_top - 4*s,
                 hip_bridge_cx - hip_bw, hip_bridge_y_top)
    ctx.close_path()
    _set_color(ctx, PANTS); ctx.fill()

    # Pants shadow
    for leg_pts in [front_leg_pts, back_leg_pts]:
        n = len(leg_pts)
        shadow_pts = []
        for i in range(n):
            t = i / max(1, n-1)
            w = (leg_w_top + (leg_w_bot - leg_w_top) * t) * 0.3
            shadow_pts.append((leg_pts[i][0] - w * 0.5, leg_pts[i][1]))
        if len(shadow_pts) > 2:
            ctx.new_path()
            ctx.move_to(*shadow_pts[0])
            for p in shadow_pts[1:]:
                ctx.line_to(*p)
            _set_color(ctx, PANTS_SH, 0.5)
            ctx.set_line_width(leg_w_bot * 1.5)
            ctx.set_line_cap(cairo.LINE_CAP_ROUND)
            ctx.stroke()

    # Shoes (left-facing: near shoe points left)
    shoe_w = head_r * 0.32
    shoe_h = head_r * 0.18
    # Far shoe (behind): smaller, points slightly right
    ctx.save()
    ctx.translate(back_leg_pts[-1][0], ground_y - back_foot_lift - far_extra_lift - heel_lift - shoe_h * 0.3)
    ctx.rotate(math.radians(8))
    _draw_ellipse_path(ctx, 0, 0, shoe_w * 0.85, shoe_h * 0.85)
    _set_color(ctx, SHOE); ctx.fill_preserve()
    _set_color(ctx, LINE_COL); ctx.set_line_width(lw_major); ctx.stroke()
    ctx.new_path()
    ctx.move_to(shoe_w * 0.7, shoe_h * 0.4)
    ctx.curve_to(shoe_w * 0.2, shoe_h * 0.65, -shoe_w * 0.2, shoe_h * 0.65, -shoe_w * 0.65, shoe_h * 0.3)
    _set_color(ctx, SHOE_SOLE); ctx.set_line_width(lw_minor); ctx.stroke()
    ctx.restore()
    # Near shoe (facing left): points left
    ctx.save()
    ctx.translate(front_leg_pts[-1][0], ground_y - front_foot_lift - heel_lift - shoe_h * 0.3)
    ctx.rotate(math.radians(-12))
    _draw_ellipse_path(ctx, 0, 0, shoe_w, shoe_h)
    _set_color(ctx, SHOE); ctx.fill_preserve()
    _set_color(ctx, LINE_COL); ctx.set_line_width(lw_major); ctx.stroke()
    ctx.new_path()
    ctx.move_to(shoe_w * 0.8, shoe_h * 0.4)
    ctx.curve_to(shoe_w * 0.3, shoe_h * 0.7, -shoe_w * 0.3, shoe_h * 0.7,
                 -shoe_w * 0.8, shoe_h * 0.3)
    _set_color(ctx, SHOE_SOLE); ctx.set_line_width(lw_minor); ctx.stroke()
    ctx.new_path()
    ctx.arc(0, -shoe_h * 0.2, 2 * s, 0, 2 * math.pi)
    _set_color(ctx, LACES); ctx.fill()
    ctx.restore()

    # ══ TORSO ══
    w_top = sh_w
    # Side-L is same viewing angle as SIDE — match foreshortened w_bot.
    w_bot = head_r * 0.40
    attach = _draw_bean_torso(ctx, torso_cx, torso_cy, w_top, w_bot, torso_h,
                              torso_lean, hip_tilt_px, shoulder_tilt_px)
    ls_pt, rs_pt, lh_pt, rh_pt = attach
    _set_color(ctx, hoodie); ctx.fill_preserve()
    _set_color(ctx, LINE_COL); ctx.set_line_width(lw_silhouette); ctx.stroke()

    # Form shadow (reversed for left-facing)
    shadow_x1 = torso_cx + torso_lean - sh_w * 0.2
    shadow_y1 = torso_cy - torso_h / 2
    ctx.new_path()
    ctx.move_to(shadow_x1, shadow_y1)
    ctx.curve_to(shadow_x1 - sh_w * 0.3, shadow_y1 + torso_h * 0.3,
                 shadow_x1 - w_bot * 0.4, shadow_y1 + torso_h * 0.8,
                 shadow_x1 - w_bot * 0.1, shadow_y1 + torso_h)
    ctx.line_to(torso_cx + torso_lean * 0.5 - w_bot, shadow_y1 + torso_h)
    ctx.line_to(shadow_x1 - sh_w * 0.5, shadow_y1)
    ctx.close_path()
    _set_color(ctx, hoodie_sh, 0.5); ctx.fill()

    # Collar V-neck
    collar_cx = torso_cx + torso_lean
    collar_y = torso_cy - torso_h / 2
    collar_w = head_r * 0.30
    ctx.new_path()
    ctx.move_to(collar_cx - collar_w, collar_y + 2 * s)
    ctx.curve_to(collar_cx - collar_w * 0.3, collar_y + 14 * s,
                 collar_cx + collar_w * 0.3, collar_y + 14 * s,
                 collar_cx + collar_w, collar_y + 2 * s)
    _set_color(ctx, (250/255, 232/255, 200/255)); ctx.set_line_width(max(5, 6 * s)); ctx.stroke_preserve()
    _set_color(ctx, LINE_COL); ctx.set_line_width(lw_minor); ctx.stroke()

    # Hoodie hem
    hem_y = torso_bot_y - torso_h * 0.10
    ctx.new_path()
    ctx.move_to(lh_pt[0] + 3*s, hem_y)
    ctx.curve_to(hip_cx - w_bot * 0.3, hem_y + 4*s,
                 hip_cx + w_bot * 0.3, hem_y + 4*s,
                 rh_pt[0] - 3*s, hem_y)
    _set_color(ctx, hoodie_sh); ctx.set_line_width(max(3, 4 * s)); ctx.stroke()

    # Pixel accents
    for _ in range(12):
        px_x = torso_cx + torso_lean + rng.uniform(-18*s, 18*s)
        px_y = torso_cy + rng.uniform(-12*s, 12*s)
        psz = max(2, rng.choice([2*s, 3*s, 4*s]))
        pc = rng.choice([PX_CYAN, PX_MAG, (0.94, 0.94, 0.94)])
        ctx.rectangle(px_x, px_y, psz, psz)
        _set_color(ctx, pc); ctx.fill()

    # ══ ARMS (side-L — distinct from side-R: relaxed near arm + bent far arm) ══
    arm_w_top = head_r * 0.14
    arm_w_bot = head_r * 0.10
    hand_r_s = head_r * 0.12

    # Near arm (left side = rs_pt in this view): relaxed down with slight forward bend
    # NOTE: side-L near arm attaches at rs_pt (right shoulder from torso perspective)
    # because the character is facing left.
    na_shoulder = (rs_pt[0] - 8*s, rs_pt[1] + 6*s)
    na_elbow = (na_shoulder[0] - 20*s, na_shoulder[1] + 30*s)
    na_hand = (na_elbow[0] - 12*s, na_elbow[1] + 28*s)
    near_arm_pts = (_bezier_points(na_shoulder, (na_shoulder[0] - 6*s, na_shoulder[1] + 10*s),
                                  (na_elbow[0] + 4*s, na_elbow[1] - 8*s), na_elbow, steps=25) +
                    _bezier_points(na_elbow, (na_elbow[0] - 4*s, na_elbow[1] + 8*s),
                                  (na_hand[0] + 3*s, na_hand[1] - 4*s), na_hand, steps=25)[1:])
    _draw_unified_arm(ctx, near_arm_pts, arm_w_top, arm_w_bot, hoodie, LINE_COL, lw_major)
    _draw_ellipse_path(ctx, na_hand[0], na_hand[1], hand_r_s, hand_r_s * 0.8)
    _set_color(ctx, SKIN); ctx.fill_preserve()
    _set_color(ctx, LINE_COL); ctx.set_line_width(lw_minor); ctx.stroke()

    # Far arm (ls_pt): bent backward/up — shows Luma just turned around
    fa_shoulder = (ls_pt[0] + 8*s, ls_pt[1] + 6*s)
    fa_elbow = (fa_shoulder[0] - 30*s, fa_shoulder[1] + 18*s)
    fa_hand = (fa_elbow[0] + 12*s, fa_elbow[1] + 22*s)
    far_arm_pts = (_bezier_points(fa_shoulder, (fa_shoulder[0] - 8*s, fa_shoulder[1] + 6*s),
                                 (fa_elbow[0] + 4*s, fa_elbow[1] - 8*s), fa_elbow, steps=25) +
                   _bezier_points(fa_elbow, (fa_elbow[0] + 6*s, fa_elbow[1] + 6*s),
                                 (fa_hand[0] - 3*s, fa_hand[1] - 4*s), fa_hand, steps=25)[1:])
    _draw_unified_arm(ctx, far_arm_pts, arm_w_top, arm_w_bot, hoodie, LINE_COL, lw_major)
    _draw_ellipse_path(ctx, fa_hand[0], fa_hand[1], hand_r_s * 0.85, hand_r_s * 0.7)
    _set_color(ctx, SKIN); ctx.fill_preserve()
    _set_color(ctx, LINE_COL); ctx.set_line_width(lw_minor); ctx.stroke()

    # ══ NECK ══
    neck_top_y = head_cy + head_r * 0.95
    neck_w_top = head_r * 0.22
    neck_w_bot = head_r * 0.30
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
    _set_color(ctx, SKIN); ctx.fill_preserve()
    _set_color(ctx, LINE_COL); ctx.set_line_width(lw_minor); ctx.stroke()

    # ══ HEAD (side-L — left-facing profile) ══
    head_rx = head_r * 0.92
    head_ry = head_r * 1.00
    tilt_rad = math.radians(-spec["head_tilt"] * 0.6)  # mirror tilt

    ctx.save()
    ctx.translate(head_cx, head_cy)
    ctx.rotate(tilt_rad)

    # Left-facing profile head: mirror of side-R. Back of head is now on +x side,
    # face (nose bump) protrudes to the LEFT (-x direction).
    ctx.new_path()
    steps = 120
    for i in range(steps):
        angle = i * 2 * math.pi / steps
        rx = head_rx
        ry = head_ry
        chin_f = max(0, math.cos(angle - math.pi / 2)) ** 2.0
        ry += head_r * 0.12 * chin_f
        crown_f = max(0, math.cos(angle + math.pi / 2)) ** 3.0
        ry -= head_r * 0.06 * crown_f
        # Back of head on RIGHT (+x = angle near 0) in left-facing view
        back_f = max(0, math.cos(angle)) ** 4
        rx += head_r * 0.14 * back_f
        # Face side on LEFT (-x = angle near pi): slight taper
        face_f = max(0, math.cos(angle - math.pi)) ** 8
        rx -= head_r * 0.06 * face_f
        side_cheek_f = max(0, math.cos(angle - 0.5)) ** 8
        rx += head_r * 0.06 * side_cheek_f
        px = rx * math.cos(angle)
        py = ry * math.sin(angle)
        if i == 0:
            ctx.move_to(px, py)
        else:
            ctx.line_to(px, py)
    ctx.close_path()
    _set_color(ctx, SKIN); ctx.fill_preserve()
    ctx.set_line_width(lw_silhouette)
    _set_color(ctx, LINE_COL); ctx.stroke()

    # Profile nose bump on -x (LEFT side, face direction)
    nose_x_base = -head_rx * 0.82
    nose_y = head_r * 0.18
    ctx.new_path()
    ctx.move_to(nose_x_base, nose_y - 8*s)
    ctx.curve_to(nose_x_base - 12*s, nose_y - 6*s,
                 nose_x_base - 14*s, nose_y + 4*s,
                 nose_x_base - 8*s, nose_y + 10*s)
    ctx.curve_to(nose_x_base - 4*s, nose_y + 14*s,
                 nose_x_base, nose_y + 12*s,
                 nose_x_base + 2*s, nose_y + 8*s)
    _set_color(ctx, SKIN); ctx.fill_preserve()
    _set_color(ctx, LINE_COL); ctx.set_line_width(lw_minor); ctx.stroke()
    ctx.new_path()
    ctx.move_to(nose_x_base - 4*s, nose_y + 10*s)
    ctx.curve_to(nose_x_base - 2*s, nose_y + 13*s,
                 nose_x_base + 1*s, nose_y + 12*s,
                 nose_x_base + 2*s, nose_y + 8*s)
    _set_color(ctx, SKIN_SH); ctx.set_line_width(lw_accent); ctx.stroke()

    # Hair cloud (left-facing: back of head is on +x side)
    hair_blobs_sl = [
        (0.55, -0.75, 0.55, 0.48), (0.30, -1.00, 0.42, 0.36),
        (0.70, -0.50, 0.42, 0.38), (0.80, -0.25, 0.38, 0.35),
        (0.00, -0.80, 0.40, 0.34), (-0.10, -1.05, 0.34, 0.30),
        (0.15, -0.60, 0.50, 0.44), (0.50, -0.92, 0.30, 0.26),
        (0.85, 0.02, 0.30, 0.32), (0.60, 0.08, 0.35, 0.30),
        (-0.20, -0.70, 0.30, 0.26), (0.10, -1.10, 0.28, 0.24),
        (0.90, -0.50, 0.26, 0.30),
    ]
    for (bx, by, brx, bry) in hair_blobs_sl:
        _draw_ellipse_path(ctx, bx * head_rx, by * head_ry, brx * head_rx, bry * head_ry)
        _set_color(ctx, HAIR); ctx.fill()
    for (bx, by, brx, bry) in [(0.42, -0.85, 0.20, 0.12),
                                 (0.65, -0.60, 0.14, 0.10),
                                 (0.18, -0.95, 0.16, 0.10)]:
        _draw_ellipse_path(ctx, bx * head_rx, by * head_ry, brx * head_rx, bry * head_ry)
        _set_color(ctx, HAIR_HL); ctx.fill()

    # Face skin (left half of head)
    _draw_ellipse_path(ctx, -head_rx * 0.10, head_r * 0.08, head_rx * 0.78, head_ry * 0.80)
    _set_color(ctx, SKIN); ctx.fill()

    # Profile eye (left-facing: eye on left side = -x)
    eye_x = -head_rx * 0.28
    eye_y_pos = head_r * 0.02
    eye_rx_p = head_rx * 0.22
    eye_ry_p = head_ry * 0.28 * spec["eye_openness"]

    _draw_ellipse_path(ctx, eye_x, eye_y_pos, eye_rx_p, eye_ry_p)
    _set_color(ctx, EYE_W); ctx.fill_preserve()
    _set_color(ctx, LINE_COL); ctx.set_line_width(lw_minor); ctx.stroke()
    ctx.new_path()
    for i in range(30):
        a = math.radians(195 + 150 * i / 29)
        px = eye_x + eye_rx_p * 1.01 * math.cos(a)
        py = eye_y_pos + eye_ry_p * 0.97 * math.sin(a)
        if i == 0:
            ctx.move_to(px, py)
        else:
            ctx.line_to(px, py)
    _set_color(ctx, LINE_COL)
    ctx.set_line_width(lw_silhouette); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    gaze_dx = -spec["gaze_dx"] * s * 0.6   # reversed for left-facing
    gaze_dy = spec["gaze_dy"] * s
    iris_r = eye_rx_p * 0.70
    iris_ry = eye_ry_p * 0.64
    _draw_ellipse_path(ctx, eye_x + gaze_dx, eye_y_pos + gaze_dy, iris_r, iris_ry)
    _set_color(ctx, EYE_IRIS); ctx.fill()
    _draw_ellipse_path(ctx, eye_x + gaze_dx, eye_y_pos + gaze_dy, iris_r * 0.52, iris_ry * 0.52)
    _set_color(ctx, EYE_PUP); ctx.fill()
    hl_r = max(iris_r * 0.42, 3)
    ctx.new_path()
    ctx.arc(eye_x + gaze_dx - iris_r * 0.30, eye_y_pos + gaze_dy - iris_ry * 0.32,
            hl_r, 0, 2 * math.pi)
    _set_color(ctx, EYE_HL); ctx.fill()

    # Profile brow (left-facing)
    doubt_wince = spec.get("doubt_wince", False)
    brow_lift = spec["brow_lift_r"] * s  # right brow lift (now the visible near brow)
    brow_y = eye_y_pos - eye_ry_p - 5*s - brow_lift
    brow_x_inner = eye_x - eye_rx_p * 0.6
    brow_x_outer = eye_x + eye_rx_p * 1.1
    ctx.new_path()
    ctx.move_to(brow_x_outer, brow_y + 4*s)
    ctx.curve_to((brow_x_outer + eye_x) / 2, brow_y - 4*s,
                 (eye_x + brow_x_inner) / 2, brow_y - 2*s,
                 brow_x_inner, brow_y + 2*s)
    _set_color(ctx, HAIR)
    ctx.set_line_width(lw_major); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    if doubt_wince:
        ctx.new_path()
        ctx.move_to(brow_x_inner, brow_y + 2*s)
        ctx.curve_to(brow_x_inner - 3*s, brow_y - 6*s,
                     brow_x_inner - 5*s, brow_y - 10*s,
                     brow_x_inner - 3*s, brow_y - 12*s)
        _set_color(ctx, HAIR)
        ctx.set_line_width(lw_minor); ctx.stroke()

    # Profile mouth (left-facing: mouth toward -x)
    mouth_y = head_r * 0.42
    mouth_w = head_rx * 0.28
    mouth_x_base = -head_rx * 0.30
    mouth_type = spec["mouth"]
    if mouth_type == "gentle_smile":
        ctx.new_path()
        ctx.move_to(mouth_x_base + mouth_w * 0.6, mouth_y + 1*s)
        ctx.curve_to(mouth_x_base + mouth_w * 0.1, mouth_y - 5*s,
                     mouth_x_base - mouth_w * 0.2, mouth_y - 4*s,
                     mouth_x_base - mouth_w * 0.5, mouth_y + 1*s)
        _set_color(ctx, LINE_COL); ctx.set_line_width(lw_minor); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    elif mouth_type == "firm_line":
        ctx.new_path()
        ctx.move_to(mouth_x_base + mouth_w * 0.5, mouth_y)
        ctx.curve_to(mouth_x_base, mouth_y - 2*s,
                     mouth_x_base - mouth_w * 0.3, mouth_y - 1*s,
                     mouth_x_base - mouth_w * 0.5, mouth_y + 1*s)
        _set_color(ctx, LINE_COL); ctx.set_line_width(lw_major); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    elif mouth_type == "open_o":
        _draw_ellipse_path(ctx, mouth_x_base, mouth_y + 2*s, mouth_w * 0.35, head_r * 0.10)
        _set_color(ctx, (0.15, 0.08, 0.06)); ctx.fill_preserve()
        _set_color(ctx, LINE_COL); ctx.set_line_width(lw_minor); ctx.stroke()
    elif mouth_type == "tight_frown":
        ctx.new_path()
        ctx.move_to(mouth_x_base + mouth_w * 0.5, mouth_y - 2*s)
        ctx.curve_to(mouth_x_base, mouth_y + 4*s,
                     mouth_x_base - mouth_w * 0.3, mouth_y + 3*s,
                     mouth_x_base - mouth_w * 0.5, mouth_y - 1*s)
        _set_color(ctx, LINE_COL); ctx.set_line_width(lw_minor); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    elif mouth_type in ("wide_grin", "gritted_teeth"):
        _draw_ellipse_path(ctx, mouth_x_base, mouth_y + 1*s, mouth_w * 0.50, head_r * 0.09)
        _set_color(ctx, (0.15, 0.08, 0.06)); ctx.fill_preserve()
        _set_color(ctx, LINE_COL); ctx.set_line_width(lw_minor); ctx.stroke()

    # Cheek blush (left side)
    _draw_ellipse_path(ctx, eye_x * 0.9, head_r * 0.24, 14*s, 8*s)
    _set_color(ctx, BLUSH_C); ctx.fill()

    ctx.restore()

    return {
        "head_cx": head_cx, "head_cy": head_cy,
        "head_r": head_r, "head_rx": head_rx, "head_ry": head_ry,
        "torso_cx": torso_cx, "torso_cy": torso_cy,
        "hip_cx": hip_cx, "ground_y": ground_y, "char_h": char_h,
    }


# ── Public Interface ─────────────────────────────────────────────────────────

def draw_luma(expression, pose=None, scale=1.0, facing="right", scene_lighting=None,
              pose_mode="side"):
    """Draw Luma and return a cairo.ImageSurface (ARGB32, transparent bg).

    Args:
        expression: str — one of EXPRESSIONS (e.g. "CURIOUS", "DETERMINED",
            "DOUBT-IN-CERTAINTY")
        pose: dict or None — custom gesture spec overrides (merged with GESTURE_SPECS)
        scale: float — base character height multiplier (1.0 = 400px at 2x)
        facing: str — "right" (default) or "left" (horizontally flipped).
            Only applies to pose_mode="side" and "threequarter".
        scene_lighting: dict or None — {key_light_color, key_light_dir, ambient}
            for future integration. Currently unused placeholder.
        pose_mode: str — one of:
            "side"         — (default) true right-facing profile view
            "front"        — full frontal, both eyes visible
            "threequarter" — 3/4 angle between front and side (right-facing)
            "back"         — rear view, no face
            "side_l"       — native left-facing profile, distinct pose (not a mirror)

    Returns:
        cairo.ImageSurface (FORMAT_ARGB32) with transparent background.
        Character centered horizontally, standing on bottom edge.
    """
    expression = expression.upper()
    if expression not in GESTURE_SPECS:
        raise ValueError(f"Unknown expression: {expression}. Must be one of {EXPRESSIONS}")

    spec = dict(GESTURE_SPECS[expression])
    if pose:
        spec.update(pose)

    # Character dimensions at 2x render scale
    base_char_h = 400  # px at 2x
    char_h = int(base_char_h * scale)
    # Canvas: enough room for widest arm extension + some margin
    canvas_w = int(char_h * 1.6)
    canvas_h = int(char_h * 1.2)
    cx = canvas_w // 2
    ground_y = canvas_h - int(char_h * 0.08)

    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, canvas_w, canvas_h)
    ctx = cairo.Context(surface)
    ctx.set_antialias(cairo.ANTIALIAS_BEST)

    # Flip for left-facing (side and threequarter only — not side_l which is native)
    if facing == "left" and pose_mode in ("side", "threequarter"):
        ctx.translate(canvas_w, 0)
        ctx.scale(-1, 1)

    pose_mode = pose_mode.lower()
    if pose_mode == "front":
        _draw_luma_front(ctx, cx, ground_y, char_h, expression, spec, scale)
    elif pose_mode == "threequarter":
        _draw_luma_threequarter(ctx, cx, ground_y, char_h, expression, spec, scale)
    elif pose_mode == "back":
        _draw_luma_back(ctx, cx, ground_y, char_h, expression, spec, scale)
    elif pose_mode == "side_l":
        _draw_luma_side_l(ctx, cx, ground_y, char_h, expression, spec, scale)
    else:
        # Default: "side" (right-facing profile)
        _draw_luma_on_context(ctx, cx, ground_y, char_h, expression, spec, scale)

    return surface


def draw_luma_on_context(ctx, cx, ground_y, char_h, expression, pose=None, scale=1.0):
    """Draw Luma directly onto an existing cairo context (for sheet/scene use).

    Args:
        ctx: cairo.Context to draw on
        cx: horizontal center position
        ground_y: Y position of ground plane
        char_h: total character height in pixels
        expression: str — one of EXPRESSIONS
        pose: dict or None — custom gesture spec overrides
        scale: float — unused (char_h controls size directly)

    Returns:
        dict with character layout info
    """
    expression = expression.upper()
    if expression not in GESTURE_SPECS:
        raise ValueError(f"Unknown expression: {expression}. Must be one of {EXPRESSIONS}")

    spec = dict(GESTURE_SPECS[expression])
    if pose:
        spec.update(pose)

    return _draw_luma_on_context(ctx, cx, ground_y, char_h, expression, spec, scale)


def cairo_surface_to_pil(surface):
    """Convert cairo ImageSurface (ARGB32) to PIL RGBA Image."""
    from PIL import Image
    w = surface.get_width()
    h = surface.get_height()
    buf = surface.get_data()
    img = Image.frombuffer("RGBA", (w, h), bytes(buf), "raw", "BGRa", 0, 1)
    return img.copy()


# ── Self-test: render all expressions when run directly ──────────────────────

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

    print("LTG_TOOL_char_luma.py — Self-test render")
    print(f"  Expressions: {', '.join(EXPRESSIONS)}")

    ensure_dir(output_dir("characters", "main"))

    for expr in EXPRESSIONS:
        safe_name = expr.lower().replace("-", "_")
        surf = draw_luma(expr, scale=1.0)
        pil_img = cairo_surface_to_pil(surf)
        pil_img.thumbnail((1280, 1280), Image.LANCZOS)
        out_path = str(output_dir("characters", "main", f"LTG_CHAR_luma_{safe_name}_test.png"))
        pil_img.save(out_path)
        print(f"  {expr}: {pil_img.size[0]}x{pil_img.size[1]} -> {out_path}")

    # Test pose modes with CURIOUS expression
    print("\n  Pose mode tests:")
    for pm in ("front", "threequarter", "side_l", "back"):
        surf = draw_luma("CURIOUS", scale=1.0, pose_mode=pm)
        pil_img = cairo_surface_to_pil(surf)
        pil_img.thumbnail((1280, 1280), Image.LANCZOS)
        out_path = str(output_dir("characters", "main", f"LTG_CHAR_luma_curious_{pm}_test.png"))
        pil_img.save(out_path)
        print(f"  CURIOUS ({pm}): {pil_img.size[0]}x{pil_img.size[1]} -> {out_path}")

    print("Done.")
