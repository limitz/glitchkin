#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_char_cosmo.py — Canonical Cosmo Modular Renderer v1.0.0
"Luma & the Glitchkin" — Cycle 53 / Sam Kowalski

PURPOSE:
  Standalone canonical renderer for Cosmo. Extracted from LTG_TOOL_cosmo_expression_sheet.py
  (v009, Maya Santos / Sam Kowalski C52). One renderer, used everywhere.

  Exports: draw_cosmo(expression, pose, scale, facing, scene_lighting) -> cairo.ImageSurface

  6 expressions: AWKWARD, WORRIED, SURPRISED, SKEPTICAL, DETERMINED, FRUSTRATED
  Gesture spec from Lee Tanaka's cosmo_gesture_spec_c52.md: offset chain architecture,
  angular body language (joint breaks, not smooth curves), glasses tilt = head_tilt * 0.4.

INTERFACE CONTRACT:
  Same function signature pattern as the Luma canonical renderer.
  Returns cairo.ImageSurface (ARGB32, transparent background).
  Accepts scale parameter for resolution independence.
  Accepts scene_lighting dict for environment integration.

CHARACTER NOTES — COSMO:
  - Rectangular torso creates ANGULAR silhouette breaks (not smooth S-curves)
  - Glasses always tilt with head tilt (glasses_tilt = head_tilt * 0.4)
  - Arms default to asymmetric
  - SKEPTICAL is his signature pose (85/15 weight, dramatic hip pop)
  - Amplified cowlick (0.15 heads) + glasses bridge tape = visual hooks
  - Shoulder involvement (C47) on all poses

Dependencies: pycairo, Pillow (for optional color enhancement), math
"""

__version__ = "1.0.0"
__author__ = "Sam Kowalski"
__cycle__ = 53

import math
import os
import sys

import cairo

_TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
if _TOOLS_DIR not in sys.path:
    sys.path.insert(0, _TOOLS_DIR)

from LTG_TOOL_cairo_primitives import (
    create_surface, draw_smooth_polygon, draw_ellipse as cairo_ellipse,
    to_pil_image, to_pil_rgba,
)

try:
    from LTG_TOOL_character_color_enhance import (
        enhance_from_cairo, apply_scene_tint, apply_skin_warmth,
        apply_form_shadow, apply_hair_absorption, SCENE_PRESETS,
    )
    _ENHANCE_AVAILABLE = True
except ImportError:
    _ENHANCE_AVAILABLE = False


# ── Palette ──────────────────────────────────────────────────────────────────
# Cosmo character colors from master_palette.md
SKIN        = (217, 192, 154)   # CHAR-C-01 Cosmo Skin Base
SKIN_SH     = (184, 154, 120)   # CHAR-C-02 Cosmo Skin Shadow
SKIN_HL     = (238, 212, 176)   # CHAR-C-03 Cosmo Skin Highlight
HAIR        = (26, 24, 36)
HAIR_SH     = (14, 14, 24)
HAIR_HL     = (44, 43, 64)
EYE_WHITE   = (250, 240, 220)
IRIS        = (61, 107, 69)
PUPIL       = (59, 40, 32)
EYE_HL      = (240, 240, 240)
GLASS_FRAME = (92, 58, 32)
GLASS_LENS  = (238, 244, 255)
GLASS_GLARE = (240, 240, 240)
STRIPE_A    = (91, 141, 184)    # Cerulean stripe (cool — NOT in warm guarantee)
STRIPE_B    = (122, 158, 126)   # Sage stripe (cool — NOT in warm guarantee)
PANTS       = (140, 136, 128)
PANTS_SH    = (106, 100, 96)
SHOE        = (92, 58, 32)
SHOE_SOLE   = (184, 154, 120)
NOTEBOOK    = (91, 141, 184)
NOTEBOOK_SP = (61, 107, 138)
LINE        = (59, 40, 32)
BLUSH       = (210, 128, 80)
BLUSH_HI    = (228, 162, 120)
TAPE_COL    = (250, 240, 220)   # warm cream — glasses bridge tape
TAPE_HL     = (255, 252, 245)   # tape highlight


# ── Gesture Specs (from Lee Tanaka cosmo_gesture_spec_c52.md) ───────────────
GESTURE_SPECS = {
    "AWKWARD": {
        "hip_shift": 14,
        "shoulder_offset": -16,
        "head_offset": 14,           # same direction as hips = Z-break
        "torso_lean": 6,             # slight backward lean
        "hip_tilt": 5.0,
        "shoulder_tilt": -6.0,
        "head_tilt": 8.0,
        "weight_front": 0.35,
        "weight_back": 0.65,
        "front_foot_lift": 4,        # toe tip
        "back_foot_lift": 0,
        "front_foot_angle": -15,     # inward
        "back_foot_angle": 20,       # outward
        "shoulder_raise": 0,
        "left_arm": "dead_hang",
        "right_arm": "neck_rub",
        "glasses_tilt": None,        # auto = head_tilt * 0.4
        # Face
        "brow_data": {"l_raise": 12, "r_raise": 2, "l_furrow": 3, "r_furrow": 0},
        "mouth": "grimace",
        "blush": True,
        "eye_openness": 1.0,
    },
    "WORRIED": {
        "hip_shift": 6,              # slight shift for gesture read (near-symmetric)
        "shoulder_offset": -8,       # slight counter-shift — compressed asymmetry
        "head_offset": -22,          # head forward (monitoring) — amplified for gesture read
        "torso_lean": -14,           # forward lean amplified — bracing posture
        "hip_tilt": 2.0,
        "shoulder_tilt": 0.0,
        "head_tilt": -6.0,
        "weight_front": 0.50,
        "weight_back": 0.50,
        "front_foot_lift": 0,
        "back_foot_lift": 0,
        "front_foot_angle": -8,
        "back_foot_angle": -8,
        "shoulder_raise": 10,        # both shoulders UP (hunch)
        "left_arm": "bracket_grip_right",
        "right_arm": "bracket_grip_left",
        "glasses_tilt": None,
        "brow_data": {"l_raise": 6, "r_raise": 6, "l_furrow": 10, "r_furrow": 10},
        "mouth": "compressed",
        "blush": False,
        "eye_openness": 0.9,
    },
    "SURPRISED": {
        "hip_shift": -20,
        "shoulder_offset": 16,
        "head_offset": -14,          # head whips opposite to shoulders
        "torso_lean": 22,            # backward lean (rigid tilt)
        "hip_tilt": -6.0,
        "shoulder_tilt": 7.0,
        "head_tilt": -10.0,
        "weight_front": 0.25,
        "weight_back": 0.75,
        "front_foot_lift": 12,
        "back_foot_lift": 0,
        "front_foot_angle": 0,       # flat, parallel to ground
        "back_foot_angle": 15,
        "shoulder_raise": 6,         # startle hunch
        "left_arm": "stop_palm",
        "right_arm": "flung_horizontal",
        "glasses_tilt": None,
        "brow_data": {"l_raise": 16, "r_raise": 16, "l_furrow": 0, "r_furrow": 0},
        "mouth": "open_surprised",
        "blush": True,
        "eye_openness": 1.4,
    },
    "SKEPTICAL": {
        "hip_shift": 22,             # dramatic hip pop
        "shoulder_offset": -18,
        "head_offset": 12,           # back toward hip side
        "torso_lean": -2,            # nearly upright (confidence)
        "hip_tilt": 8.0,
        "shoulder_tilt": -7.0,
        "head_tilt": 6.0,
        "weight_front": 0.15,
        "weight_back": 0.85,
        "front_foot_lift": 2,        # barely touching
        "back_foot_lift": 0,
        "front_foot_angle": -10,     # inward
        "back_foot_angle": 25,       # planted
        "shoulder_raise": 0,
        "left_arm": "crossed_over",
        "right_arm": "crossed_under",
        "glasses_tilt": 3.0,
        "brow_data": {"l_raise": 18, "r_raise": 0, "l_furrow": 0, "r_furrow": 1},
        "mouth": "flat",
        "blush": False,
        "eye_openness": 0.95,
    },
    "DETERMINED": {
        "hip_shift": -12,            # backward (hips as fulcrum) — amplified
        "shoulder_offset": 16,       # amplified for gesture read
        "head_offset": 12,           # head leads forward — amplified
        "torso_lean": -20,           # forward lean amplified (angular, committed)
        "hip_tilt": -3.0,
        "shoulder_tilt": 4.0,
        "head_tilt": -3.0,
        "weight_front": 0.70,
        "weight_back": 0.30,
        "front_foot_lift": 0,
        "back_foot_lift": 0,
        "front_foot_angle": 0,       # pointing straight ahead
        "back_foot_angle": 20,       # push-off angle
        "shoulder_raise": 0,
        "left_arm": "pointing_forward",
        "right_arm": "fist_at_hip",
        "glasses_tilt": None,
        "brow_data": {"l_raise": 2, "r_raise": 2, "l_furrow": 2, "r_furrow": 2},
        "mouth": "slight_smile",
        "blush": False,
        "eye_openness": 0.95,
    },
    "FRUSTRATED": {
        "hip_shift": 18,
        "shoulder_offset": -20,
        "head_offset": -6,           # drops forward
        "torso_lean": 4,             # slight backward (twist reads as tension)
        "hip_tilt": 7.0,
        "shoulder_tilt": -8.0,
        "head_tilt": -10.0,
        "weight_front": 0.20,
        "weight_back": 0.80,
        "front_foot_lift": 3,
        "back_foot_lift": 0,
        "front_foot_angle": -18,     # sharply inward (closed)
        "back_foot_angle": 15,
        "shoulder_raise": 0,
        "left_arm": "rigid_fist",
        "right_arm": "forehead_grip",
        "glasses_tilt": None,
        "brow_data": {"l_raise": -3, "r_raise": -3, "l_furrow": 4, "r_furrow": 4},
        "mouth": "compressed",
        "blush": False,
        "eye_openness": 0.85,
    },
}

VALID_EXPRESSIONS = list(GESTURE_SPECS.keys())


# ── Helper: RGB 0-255 to cairo 0.0-1.0 ─────────────────────────────────────
def _c(rgb):
    """Convert (R,G,B) 0-255 to cairo (r,g,b) 0.0-1.0."""
    return (rgb[0] / 255.0, rgb[1] / 255.0, rgb[2] / 255.0)


# ── Shoulder mechanics (C47) ────────────────────────────────────────────────
def _shoulder_dy(arm_mode, shoulder_raise=0):
    """Calculate shoulder displacement from arm mode and raise value."""
    arm_modes_raising = {
        "bracket_grip_right", "bracket_grip_left",
        "stop_palm", "flung_horizontal",
        "neck_rub", "forehead_grip",
    }
    base = -shoulder_raise
    if arm_mode in arm_modes_raising:
        base = min(base, -6)
    return base


# ── Offset chain (Lee Tanaka C50/C52 spec) ──────────────────────────────────
def _compute_chain(spec, cx, base_y, hu):
    """Compute the offset chain positions for hip, torso, head.

    At 2x scale, spec values are used directly. At other scales, multiply.
    Returns dict with all computed positions.
    """
    # Scale factor: spec values are at 2x (2560x1440). Adjust by hu ratio.
    # Reference hu at 2x for expression sheet is ~84px (PANEL_H*0.190)
    # We use the spec values as-is and let the caller set scale via hu.
    hip_shift = spec["hip_shift"]
    shoulder_offset = spec["shoulder_offset"]
    head_offset = spec["head_offset"]
    torso_lean = spec["torso_lean"]

    hip_cx = cx + hip_shift
    torso_cx = hip_cx + shoulder_offset
    head_cx = torso_cx + head_offset

    # Torso geometry
    torso_hw = int(hu * 0.41)
    torso_h = int(hu * 1.2)
    body_top_y = base_y + int(hu * 0.55)
    torso_bot_y = body_top_y + torso_h
    tilt_off = int(torso_lean * 2.5)

    # Head geometry
    hw = int(hu * 0.43)
    hh = int(hu * 0.50)
    head_cy = base_y

    return {
        "hip_cx": hip_cx,
        "torso_cx": torso_cx,
        "head_cx": head_cx,
        "body_top_y": body_top_y,
        "torso_bot_y": torso_bot_y,
        "torso_hw": torso_hw,
        "torso_h": torso_h,
        "tilt_off": tilt_off,
        "head_hw": hw,
        "head_hh": hh,
        "head_cy": head_cy,
    }


# ══════════════════════════════════════════════════════════════════════════════
# Drawing sub-functions (cairo)
# ══════════════════════════════════════════════════════════════════════════════

def _draw_head(ctx, cx, cy, hu):
    """Draw Cosmo's rectangular head with rounded corners."""
    hw = int(hu * 0.43)
    hh = int(hu * 0.50)
    r = int(hu * 0.12)
    x0, y0 = cx - hw, cy - hh
    x1, y1 = cx + hw, cy + hh

    ctx.new_path()
    ctx.move_to(x0 + r, y0)
    ctx.line_to(x1 - r, y0)
    ctx.arc(x1 - r, y0 + r, r, -math.pi / 2, 0)
    ctx.line_to(x1, y1 - r)
    ctx.arc(x1 - r, y1 - r, r, 0, math.pi / 2)
    ctx.line_to(x0 + r, y1)
    ctx.arc(x0 + r, y1 - r, r, math.pi / 2, math.pi)
    ctx.line_to(x0, y0 + r)
    ctx.arc(x0 + r, y0 + r, r, math.pi, 3 * math.pi / 2)
    ctx.close_path()

    ctx.set_source_rgb(*_c(SKIN))
    ctx.fill_preserve()
    ctx.set_source_rgb(*_c(LINE))
    ctx.set_line_width(2.0)
    ctx.stroke()


def _draw_hair(ctx, cx, cy, hu):
    """Draw Cosmo's hair with amplified cowlick (0.15 heads). Returns hair_bbox."""
    hw = int(hu * 0.43)
    hh = int(hu * 0.50)
    hair_top = cy - hh - int(hu * 0.05)
    hair_bot = cy - hh + int(hu * 0.15)

    # Left hair mass
    cairo_ellipse(ctx, cx - int(hw * 0.4), (hair_top + hair_bot + 6) / 2,
                  hw * 0.6 + 2, (hair_bot + 6 - hair_top) / 2)
    ctx.set_source_rgb(*_c(HAIR))
    ctx.fill()

    # Right hair mass
    cairo_ellipse(ctx, cx + int(hw * 0.4), (hair_top + 2 + hair_bot + 4) / 2,
                  hw * 0.6 + 2, (hair_bot + 4 - hair_top - 2) / 2)
    ctx.set_source_rgb(*_c(HAIR))
    ctx.fill()

    # Part line
    part_x = cx + int(hw * 0.12)
    ctx.move_to(part_x, hair_top + 4)
    ctx.line_to(part_x, hair_bot)
    ctx.set_source_rgb(*_c(SKIN))
    ctx.set_line_width(2.0)
    ctx.stroke()

    # Amplified cowlick — 0.15 heads tall (visual hook)
    cowlick_x = cx + int(hw * 0.05)
    cowlick_base_y = hair_top
    cowlick_tip_y = cowlick_base_y - int(hu * 0.15)
    cowlick_w = int(hu * 0.08)

    tuft_pts = [
        (cowlick_x - cowlick_w // 2, cowlick_base_y + 2),
        (cowlick_x - int(cowlick_w * 0.3), cowlick_tip_y + int(hu * 0.04)),
        (cowlick_x + int(cowlick_w * 0.1), cowlick_tip_y),
        (cowlick_x + int(cowlick_w * 0.6), cowlick_tip_y + int(hu * 0.06)),
        (cowlick_x + cowlick_w // 2, cowlick_base_y + 2),
    ]
    ctx.new_path()
    ctx.move_to(*tuft_pts[0])
    for pt in tuft_pts[1:]:
        ctx.line_to(*pt)
    ctx.close_path()
    ctx.set_source_rgb(*_c(HAIR))
    ctx.fill()

    # Highlight on cowlick
    ctx.new_path()
    ctx.move_to(*tuft_pts[1])
    ctx.line_to(*tuft_pts[2])
    ctx.line_to(*tuft_pts[3])
    ctx.set_source_rgb(*_c(HAIR_HL))
    ctx.set_line_width(2.0)
    ctx.stroke()

    # Outline for cowlick
    ctx.new_path()
    ctx.move_to(*tuft_pts[0])
    for pt in tuft_pts[1:]:
        ctx.line_to(*pt)
    ctx.set_source_rgb(*_c(LINE))
    ctx.set_line_width(2.0)
    ctx.stroke()

    # Hair shine arc
    ctx.new_path()
    ctx.arc(cx, hair_top + int(hu * 0.03), int(hw * 0.6),
            math.radians(200), math.radians(340))
    ctx.set_source_rgb(*_c(HAIR_HL))
    ctx.set_line_width(2.0)
    ctx.stroke()

    return (cx - hw - 2, cowlick_tip_y, cx + hw + 2, hair_bot + 6)


def _draw_glasses(ctx, cx, cy, hu, tilt_deg):
    """Draw glasses with bridge tape. Returns (lcx, lcy, rcx, rcy, lens_r)."""
    lens_r = int(hu * 0.16)
    frame_w = max(3, int(hu * 0.06))
    bridge = int(hu * 0.05)
    eye_sep = lens_r + bridge
    gcy = cy - int(hu * 0.10)
    theta = math.radians(-tilt_deg)
    cos_t, sin_t = math.cos(theta), math.sin(theta)

    def rot(dx, dy):
        return (cx + dx * cos_t - dy * sin_t, gcy + dx * sin_t + dy * cos_t)

    lcx, lcy = rot(-eye_sep, 0)
    rcx, rcy = rot(+eye_sep, 0)

    # Lens fills
    for (ex, ey) in [(lcx, lcy), (rcx, rcy)]:
        cairo_ellipse(ctx, ex, ey, lens_r, lens_r)
        ctx.set_source_rgb(*_c(GLASS_LENS))
        ctx.fill()

    # Glare arcs
    gl_r = int(lens_r * 0.7)
    for (ex, ey) in [(lcx, lcy), (rcx, rcy)]:
        ctx.new_path()
        ctx.arc(ex, ey - lens_r + int(lens_r * 0.25), gl_r,
                math.radians(200), math.radians(340))
        ctx.set_source_rgb(*_c(GLASS_GLARE))
        ctx.set_line_width(2.0)
        ctx.stroke()

    # Frames
    for (ex, ey) in [(lcx, lcy), (rcx, rcy)]:
        cairo_ellipse(ctx, ex, ey, lens_r, lens_r)
        ctx.set_source_rgb(*_c(GLASS_FRAME))
        ctx.set_line_width(frame_w)
        ctx.stroke()

    # Bridge
    bridge_l = rot(-bridge, 0)
    bridge_r = rot(+bridge, 0)
    ctx.new_path()
    ctx.move_to(*bridge_l)
    ctx.line_to(*bridge_r)
    ctx.set_source_rgb(*_c(GLASS_FRAME))
    ctx.set_line_width(frame_w)
    ctx.stroke()

    # Bridge tape (visual hook)
    tape_w = max(4, int(hu * 0.04))
    tape_half_h = max(3, int(hu * 0.03))
    tape_cx = (bridge_l[0] + bridge_r[0]) / 2
    tape_cy = (bridge_l[1] + bridge_r[1]) / 2
    ctx.rectangle(tape_cx - tape_w, tape_cy - tape_half_h, tape_w * 2, tape_half_h * 2)
    ctx.set_source_rgb(*_c(TAPE_COL))
    ctx.fill_preserve()
    ctx.set_source_rgb(*_c(LINE))
    ctx.set_line_width(1.0)
    ctx.stroke()
    ctx.new_path()
    ctx.move_to(tape_cx - tape_w + 1, tape_cy - 1)
    ctx.line_to(tape_cx + tape_w - 1, tape_cy - 1)
    ctx.set_source_rgb(*_c(TAPE_HL))
    ctx.set_line_width(1.0)
    ctx.stroke()

    # Temples
    l_ts = rot(-eye_sep - lens_r, 0)
    l_te = rot(-eye_sep - lens_r - int(hu * 0.06), int(hu * 0.02))
    r_ts = rot(+eye_sep + lens_r, 0)
    r_te = rot(+eye_sep + lens_r + int(hu * 0.06), int(hu * 0.02))
    for (s, e) in [(l_ts, l_te), (r_ts, r_te)]:
        ctx.new_path()
        ctx.move_to(*s)
        ctx.line_to(*e)
        ctx.set_source_rgb(*_c(GLASS_FRAME))
        ctx.set_line_width(max(2, frame_w - 1))
        ctx.stroke()

    return lcx, lcy, rcx, rcy, lens_r


def _draw_eyes(ctx, lcx, lcy, rcx, rcy, lens_r, eye_openness=1.0):
    """Draw eyes inside glasses lenses."""
    iris_r = int(lens_r * 0.55 * eye_openness)
    pup_r = int(iris_r * 0.55)
    for (ex, ey) in [(lcx, lcy), (rcx, rcy)]:
        # White
        cairo_ellipse(ctx, ex, ey, iris_r + 4, iris_r + 4)
        ctx.set_source_rgb(*_c(EYE_WHITE))
        ctx.fill()
        # Iris
        cairo_ellipse(ctx, ex, ey, iris_r, iris_r)
        ctx.set_source_rgb(*_c(IRIS))
        ctx.fill()
        # Pupil
        cairo_ellipse(ctx, ex, ey, pup_r, pup_r)
        ctx.set_source_rgb(*_c(PUPIL))
        ctx.fill()
        # Highlight
        hl_r = max(2, int(iris_r * 0.28))
        cairo_ellipse(ctx, ex + int(iris_r * 0.3) + hl_r, ey - iris_r + 2 + hl_r,
                      hl_r, hl_r)
        ctx.set_source_rgb(*_c(EYE_HL))
        ctx.fill()
        # Lower lid line
        ctx.new_path()
        ctx.move_to(ex - iris_r - 3, ey + int(iris_r * 0.5))
        ctx.line_to(ex + iris_r + 3, ey + int(iris_r * 0.5))
        ctx.set_source_rgb(*_c(LINE))
        ctx.set_line_width(2.0)
        ctx.stroke()


def _draw_brows(ctx, cx, cy, hu, tilt_deg, brow_data, lcx, lcy, rcx, rcy):
    """Draw eyebrows."""
    lens_r = int(hu * 0.16)
    brow_y_base = lcy - lens_r - int(hu * 0.06)
    l_raise = brow_data.get("l_raise", 0)
    r_raise = brow_data.get("r_raise", 0)
    l_furrow = brow_data.get("l_furrow", 0)
    r_furrow = brow_data.get("r_furrow", 0)
    brow_w = int(hu * 0.18)
    brow_thick = max(3.0, hu * 0.028)

    # Left brow
    l_inner_y = brow_y_base - l_raise - l_furrow
    l_outer_y = brow_y_base - l_raise + l_furrow // 2
    ctx.new_path()
    ctx.move_to(lcx - brow_w, l_outer_y)
    ctx.line_to(lcx, l_inner_y)
    ctx.line_to(lcx + brow_w, l_outer_y + 2)
    ctx.set_source_rgb(*_c(HAIR))
    ctx.set_line_width(brow_thick)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.stroke()

    # Right brow
    r_inner_y = brow_y_base - r_raise - r_furrow
    r_outer_y = brow_y_base - r_raise + r_furrow // 2
    ctx.new_path()
    ctx.move_to(rcx - brow_w, r_outer_y + 2)
    ctx.line_to(rcx, r_inner_y)
    ctx.line_to(rcx + brow_w, r_outer_y)
    ctx.set_source_rgb(*_c(HAIR))
    ctx.set_line_width(brow_thick)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.stroke()


def _draw_nose(ctx, cx, cy, hu):
    """Draw nose."""
    nose_r = int(hu * 0.05)
    cairo_ellipse(ctx, cx, cy + int(hu * 0.11), nose_r, int(hu * 0.05))
    ctx.set_source_rgb(*_c(SKIN_SH))
    ctx.fill()


def _draw_mouth(ctx, cx, cy, hu, mouth_style):
    """Draw mouth based on style."""
    mouth_y = cy + int(hu * 0.26)
    mw = int(hu * 0.20)

    ctx.set_source_rgb(*_c(LINE))
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)

    if mouth_style == "neutral":
        ctx.new_path()
        ctx.move_to(cx - mw, mouth_y)
        ctx.line_to(cx + mw, mouth_y)
        ctx.set_line_width(2.0)
        ctx.stroke()
        for (sx, ex, ey) in [(cx - mw, cx - mw + 4, mouth_y - 2),
                              (cx + mw, cx + mw - 4, mouth_y - 2)]:
            ctx.new_path()
            ctx.move_to(sx, mouth_y)
            ctx.line_to(ex, ey)
            ctx.set_line_width(2.0)
            ctx.stroke()
    elif mouth_style == "slight_smile":
        ctx.new_path()
        ctx.arc(cx, mouth_y, mw, math.radians(10), math.radians(170))
        ctx.set_line_width(3.0)
        ctx.stroke()
    elif mouth_style == "flat":
        ctx.new_path()
        ctx.move_to(cx - mw, mouth_y)
        ctx.line_to(cx + mw, mouth_y)
        ctx.set_line_width(3.0)
        ctx.stroke()
    elif mouth_style == "compressed":
        ctx.new_path()
        ctx.move_to(cx - mw + 4, mouth_y - 1)
        ctx.line_to(cx + mw - 4, mouth_y - 1)
        ctx.set_line_width(3.0)
        ctx.stroke()
        for (sx, sy, ex, ey) in [(cx - mw, mouth_y + 3, cx - mw + 6, mouth_y - 2),
                                  (cx + mw, mouth_y + 3, cx + mw - 6, mouth_y - 2)]:
            ctx.new_path()
            ctx.move_to(sx, sy)
            ctx.line_to(ex, ey)
            ctx.set_line_width(2.0)
            ctx.stroke()
    elif mouth_style == "grimace":
        ctx.rectangle(cx - mw + 4, mouth_y - 4, 2 * (mw - 4), 10)
        ctx.set_source_rgb(245 / 255, 240 / 255, 232 / 255)
        ctx.fill_preserve()
        ctx.set_source_rgb(*_c(LINE))
        ctx.set_line_width(2.0)
        ctx.stroke()
        for i in range(4):
            tx = cx - mw + 8 + i * int(mw * 0.45)
            ctx.new_path()
            ctx.move_to(tx, mouth_y - 4)
            ctx.line_to(tx, mouth_y + 6)
            ctx.set_source_rgb(*_c(LINE))
            ctx.set_line_width(1.0)
            ctx.stroke()
    elif mouth_style == "open_surprised":
        cairo_ellipse(ctx, cx, mouth_y + int(hu * 0.03),
                      int(mw * 0.55), int(hu * 0.07))
        ctx.set_source_rgb(210 / 255, 180 / 255, 150 / 255)
        ctx.fill_preserve()
        ctx.set_source_rgb(*_c(LINE))
        ctx.set_line_width(2.0)
        ctx.stroke()


def _draw_blush(ctx, cx, cy, hu):
    """Draw blush on cheeks."""
    blush_rx = int(hu * 0.22)
    blush_ry = int(hu * 0.09)
    cheek_y = cy + int(hu * 0.20)
    for side in [-1, 1]:
        bcx = cx + side * int(hu * 0.35)
        cairo_ellipse(ctx, bcx, cheek_y, blush_rx, blush_ry)
        ctx.set_source_rgba(*_c(BLUSH), 0.6)
        ctx.fill()
        inner_rx = int(blush_rx * 0.55)
        inner_ry = int(blush_ry * 0.55)
        cairo_ellipse(ctx, bcx, cheek_y, inner_rx, inner_ry)
        ctx.set_source_rgba(*_c(BLUSH_HI), 0.5)
        ctx.fill()


# ── Arm drawing ──────────────────────────────────────────────────────────────

def _arm_rect(ctx, x, y, w, h, color):
    ctx.rectangle(x, y, w, h)
    ctx.set_source_rgb(*_c(color))
    ctx.fill_preserve()
    ctx.set_source_rgb(*_c(LINE))
    ctx.set_line_width(2.0)
    ctx.stroke()


def _hand_ellipse(ctx, x, y, rx, ry, color=SKIN):
    cairo_ellipse(ctx, x, y, rx, ry)
    ctx.set_source_rgb(*_c(color))
    ctx.fill_preserve()
    ctx.set_source_rgb(*_c(LINE))
    ctx.set_line_width(2.0)
    ctx.stroke()


def _arm_line(ctx, x1, y1, x2, y2, color, width):
    ctx.new_path()
    ctx.move_to(x1, y1)
    ctx.line_to(x2, y2)
    ctx.set_source_rgb(*_c(color))
    ctx.set_line_width(width)
    ctx.stroke()


def _draw_arms(ctx, spec, chain, hu):
    """Draw arms based on gesture spec arm modes.

    Uses the offset chain for positioning arms relative to torso.
    """
    cx = chain["torso_cx"]
    body_top_y = chain["body_top_y"]
    torso_hw = chain["torso_hw"]
    torso_bot_y = chain["torso_bot_y"]
    tilt_off = chain["tilt_off"]

    arm_w = int(hu * 0.12)
    arm_h = int(hu * 0.75)
    arm_y = body_top_y + int(hu * 0.06)
    lax = cx - torso_hw + tilt_off - int(hu * 0.03)
    rax = cx + torso_hw + tilt_off + int(hu * 0.03)

    left_arm = spec["left_arm"]
    right_arm = spec["right_arm"]

    # ── Left arm ─────────────────────────────────────────────────────────
    if left_arm == "dead_hang":
        lay = arm_y + 8
        _arm_rect(ctx, lax - arm_w, lay, arm_w, arm_h + 15, STRIPE_A)
        _hand_ellipse(ctx, lax - arm_w // 2, lay + arm_h + 12,
                      arm_w // 2 + 5, int(hu * 0.11))

    elif left_arm == "bracket_grip_right":
        # Self-hug: left hand grips right bicep
        elbow_x = cx - int(hu * 0.55)
        elbow_y = body_top_y + int(hu * 0.35)
        hand_x = cx + int(hu * 0.25)
        hand_y = body_top_y + int(hu * 0.30)
        _arm_line(ctx, lax, arm_y, elbow_x, elbow_y, STRIPE_A, arm_w * 3)
        _arm_line(ctx, lax, arm_y, elbow_x, elbow_y, LINE, 2)
        _arm_line(ctx, elbow_x, elbow_y, hand_x, hand_y, STRIPE_A, arm_w * 3)
        _arm_line(ctx, elbow_x, elbow_y, hand_x, hand_y, LINE, 2)
        _hand_ellipse(ctx, hand_x, hand_y, int(arm_w * 1.2), int(hu * 0.10))

    elif left_arm == "stop_palm":
        # Defensive palm-out stop gesture
        elbow_x = lax - int(hu * 0.25)
        elbow_y = arm_y - int(hu * 0.15)
        hand_x = lax - int(hu * 0.55)
        hand_y = arm_y - int(hu * 0.40)
        _arm_line(ctx, lax, arm_y, elbow_x, elbow_y, STRIPE_A, arm_w * 3)
        _arm_line(ctx, lax, arm_y, elbow_x, elbow_y, LINE, 2)
        _arm_line(ctx, elbow_x, elbow_y, hand_x, hand_y, STRIPE_A, arm_w * 3)
        _arm_line(ctx, elbow_x, elbow_y, hand_x, hand_y, LINE, 2)
        # Open palm (wider ellipse)
        _hand_ellipse(ctx, hand_x, hand_y, int(arm_w * 1.8), int(hu * 0.14), SKIN_HL)

    elif left_arm == "crossed_over":
        # Crossed arms: left arm OVER right
        l_shoulder_x = lax
        l_shoulder_y = arm_y + int(arm_h * 0.08)
        l_elbow_x = lax - int(hu * 0.04)
        l_elbow_y = l_shoulder_y + int(arm_h * 0.42)
        l_hand_x = cx - int(hu * 0.22)
        l_hand_y = l_shoulder_y + int(arm_h * 0.72)
        _arm_line(ctx, l_shoulder_x, l_shoulder_y, l_elbow_x, l_elbow_y, STRIPE_A, arm_w * 3)
        _arm_line(ctx, l_shoulder_x, l_shoulder_y, l_elbow_x, l_elbow_y, LINE, 2)
        _arm_line(ctx, l_elbow_x, l_elbow_y, l_hand_x, l_hand_y, STRIPE_A, arm_w * 3)
        _arm_line(ctx, l_elbow_x, l_elbow_y, l_hand_x, l_hand_y, LINE, 2)
        _hand_ellipse(ctx, l_hand_x, l_hand_y, int(arm_w * 1.3), int(hu * 0.10))

    elif left_arm == "pointing_forward":
        # Pointing/gesturing forward at target
        elbow_x = lax - int(hu * 0.20)
        elbow_y = arm_y + int(arm_h * 0.20)
        hand_x = lax - int(hu * 0.65)
        hand_y = arm_y + int(arm_h * 0.12)
        _arm_line(ctx, lax, arm_y, elbow_x, elbow_y, STRIPE_A, arm_w * 3)
        _arm_line(ctx, lax, arm_y, elbow_x, elbow_y, LINE, 2)
        _arm_line(ctx, elbow_x, elbow_y, hand_x, hand_y, STRIPE_A, arm_w * 3)
        _arm_line(ctx, elbow_x, elbow_y, hand_x, hand_y, LINE, 2)
        _hand_ellipse(ctx, hand_x, hand_y, int(arm_w * 1.4), int(hu * 0.10), SKIN)

    elif left_arm == "rigid_fist":
        # Rigid fist at side — controlled rage
        lay = arm_y
        _arm_rect(ctx, lax - arm_w, lay, arm_w, arm_h, STRIPE_A)
        # Clenched fist (smaller, tighter)
        _hand_ellipse(ctx, lax - arm_w // 2, lay + arm_h + int(hu * 0.02),
                      int(arm_w * 0.6), int(hu * 0.08))

    # ── Right arm ────────────────────────────────────────────────────────
    if right_arm == "neck_rub":
        # Self-soothing neck rub
        raise_off = -int(hu * 0.22)
        palm_x = rax + int(hu * 0.90)
        palm_y = arm_y + int(arm_h * 0.18) + raise_off
        elbow_x = rax + int(hu * 0.52)
        elbow_y = arm_y + int(arm_h * 0.35) + raise_off
        _arm_line(ctx, rax, arm_y + raise_off, elbow_x, elbow_y, STRIPE_A, arm_w * 3)
        _arm_line(ctx, rax, arm_y + raise_off, elbow_x, elbow_y, LINE, 2)
        _arm_line(ctx, elbow_x, elbow_y, palm_x, palm_y, STRIPE_A, arm_w * 3)
        _arm_line(ctx, elbow_x, elbow_y, palm_x, palm_y, LINE, 2)
        _hand_ellipse(ctx, palm_x, palm_y - int(hu * 0.06),
                      int(arm_w * 1.0), int(hu * 0.14), SKIN_HL)

    elif right_arm == "bracket_grip_left":
        # Self-hug: right hand grips left bicep
        elbow_x = cx + int(hu * 0.55)
        elbow_y = body_top_y + int(hu * 0.35)
        hand_x = cx - int(hu * 0.25)
        hand_y = body_top_y + int(hu * 0.30)
        _arm_line(ctx, rax, arm_y, elbow_x, elbow_y, STRIPE_A, arm_w * 3)
        _arm_line(ctx, rax, arm_y, elbow_x, elbow_y, LINE, 2)
        _arm_line(ctx, elbow_x, elbow_y, hand_x, hand_y, STRIPE_A, arm_w * 3)
        _arm_line(ctx, elbow_x, elbow_y, hand_x, hand_y, LINE, 2)
        _hand_ellipse(ctx, hand_x, hand_y, int(arm_w * 1.2), int(hu * 0.10))

    elif right_arm == "flung_horizontal":
        # Flung outward at full extension, horizontal — counterbalance
        hand_x = rax + int(hu * 1.30)
        hand_y = arm_y - int(arm_h * 0.04)
        elbow_x = rax + int(hu * 0.65)
        elbow_y = arm_y - int(arm_h * 0.02)
        _arm_line(ctx, rax, arm_y, elbow_x, elbow_y, STRIPE_A, arm_w * 3)
        _arm_line(ctx, rax, arm_y, elbow_x, elbow_y, LINE, 2)
        _arm_line(ctx, elbow_x, elbow_y, hand_x, hand_y, STRIPE_A, arm_w * 3)
        _arm_line(ctx, elbow_x, elbow_y, hand_x, hand_y, LINE, 2)
        _hand_ellipse(ctx, hand_x, hand_y, int(arm_w * 1.4), int(hu * 0.11))

    elif right_arm == "crossed_under":
        # Crossed arms: right arm under left
        r_shoulder_x = rax
        r_shoulder_y = arm_y + int(arm_h * 0.22)
        r_elbow_x = cx + int(hu * 0.18)
        r_elbow_y = r_shoulder_y + int(arm_h * 0.28)
        r_hand_x = cx - int(hu * 0.05)
        r_hand_y = r_shoulder_y + int(arm_h * 0.55)
        _arm_line(ctx, r_shoulder_x, r_shoulder_y, r_elbow_x, r_elbow_y, STRIPE_A, arm_w * 3)
        _arm_line(ctx, r_shoulder_x, r_shoulder_y, r_elbow_x, r_elbow_y, LINE, 2)
        _arm_line(ctx, r_elbow_x, r_elbow_y, r_hand_x, r_hand_y, STRIPE_A, arm_w * 3)
        _arm_line(ctx, r_elbow_x, r_elbow_y, r_hand_x, r_hand_y, LINE, 2)
        _hand_ellipse(ctx, r_hand_x, r_hand_y, int(arm_w * 1.3), int(hu * 0.10))

    elif right_arm == "fist_at_hip":
        # Fist pulled back at hip — cocked, ready to act
        ray = arm_y + int(arm_h * 0.30)
        _arm_rect(ctx, rax, arm_y, arm_w, int(arm_h * 0.55), STRIPE_A)
        _hand_ellipse(ctx, rax + arm_w // 2, ray + int(hu * 0.12),
                      int(arm_w * 0.7), int(hu * 0.09))

    elif right_arm == "forehead_grip":
        # Hand on forehead / pushing through hair — self-blame frustration
        elbow_x = rax + int(hu * 0.40)
        elbow_y = arm_y - int(hu * 0.10)
        hand_x = cx + int(hu * 0.15)
        hand_y = chain["head_cy"] - int(hu * 0.20)
        _arm_line(ctx, rax, arm_y, elbow_x, elbow_y, STRIPE_A, arm_w * 3)
        _arm_line(ctx, rax, arm_y, elbow_x, elbow_y, LINE, 2)
        _arm_line(ctx, elbow_x, elbow_y, hand_x, hand_y, STRIPE_A, arm_w * 3)
        _arm_line(ctx, elbow_x, elbow_y, hand_x, hand_y, LINE, 2)
        _hand_ellipse(ctx, hand_x, hand_y, int(arm_w * 1.5), int(hu * 0.12), SKIN_HL)


def _draw_torso(ctx, spec, chain, hu):
    """Draw Cosmo's rectangular torso with angular shoulder breaks.

    Cosmo's body language is ANGULAR — the rectangular torso creates visible
    angle breaks at joints, not smooth curves.
    """
    cx = chain["torso_cx"]
    body_top_y = chain["body_top_y"]
    torso_hw = chain["torso_hw"]
    torso_h = chain["torso_h"]
    torso_bot_y = chain["torso_bot_y"]
    tilt_off = chain["tilt_off"]
    shoulder_raise = spec.get("shoulder_raise", 0)

    # Shoulder involvement (C47)
    l_arm = spec["left_arm"]
    r_arm = spec["right_arm"]
    l_sh_dy = _shoulder_dy(l_arm, shoulder_raise)
    r_sh_dy = _shoulder_dy(r_arm, shoulder_raise)

    sh_bump_w = int(hu * 0.08)
    l_top_y = body_top_y + l_sh_dy
    r_top_y = body_top_y + r_sh_dy

    # Torso polygon with shoulder bumps
    # Angular: use low bulge_frac to keep the rectangular shape visible
    shirt_pts = [
        (cx - torso_hw + tilt_off - sh_bump_w, body_top_y),
        (cx - torso_hw + tilt_off, l_top_y),
        (cx - int(torso_hw * 0.3) + tilt_off, body_top_y),
        (cx + int(torso_hw * 0.3) + tilt_off, body_top_y),
        (cx + torso_hw + tilt_off, r_top_y),
        (cx + torso_hw + tilt_off + sh_bump_w, body_top_y),
        (cx + torso_hw, torso_bot_y),
        (cx - torso_hw, torso_bot_y),
    ]

    # Angular: keep bulge_frac low (0.03) to preserve rectangular feel
    draw_smooth_polygon(ctx, shirt_pts, bulge_frac=0.03)
    ctx.set_source_rgb(*_c(STRIPE_A))
    ctx.fill_preserve()
    ctx.set_source_rgb(*_c(LINE))
    ctx.set_line_width(2.0)
    ctx.stroke()

    # Horizontal stripes
    stripe_h = max(4, int(hu * 0.055))
    n_stripes = torso_h // stripe_h
    for i in range(n_stripes):
        if i % 2 == 0:
            continue
        sy = body_top_y + i * stripe_h
        ey = min(sy + stripe_h, torso_bot_y)
        t_frac = (sy - body_top_y) / max(1, torso_h)
        s_tilt = tilt_off * (1 - t_frac)
        sw_l = int(torso_hw - abs(s_tilt) * 0.1)
        ctx.new_path()
        ctx.move_to(cx - sw_l + int(s_tilt), sy)
        ctx.line_to(cx + sw_l + int(s_tilt), sy)
        ctx.line_to(cx + sw_l, ey)
        ctx.line_to(cx - sw_l, ey)
        ctx.close_path()
        ctx.set_source_rgb(*_c(STRIPE_B))
        ctx.fill()

    # Torso outline (redraw over stripes)
    draw_smooth_polygon(ctx, shirt_pts, bulge_frac=0.03)
    ctx.set_source_rgb(*_c(LINE))
    ctx.set_line_width(2.0)
    ctx.stroke()

    # Neck
    neck_w = int(hu * 0.10)
    cairo_ellipse(ctx, cx, body_top_y + int(hu * 0.02), neck_w, int(hu * 0.06))
    ctx.set_source_rgb(*_c(SKIN))
    ctx.fill()


def _draw_legs(ctx, spec, chain, hu):
    """Draw legs and shoes with weight distribution from gesture spec."""
    cx = chain["hip_cx"]  # Legs follow hip position
    torso_hw = chain["torso_hw"]
    torso_bot_y = chain["torso_bot_y"]

    leg_w = int(hu * 0.16)
    leg_h = int(hu * 0.90)
    leg_l = cx - int(torso_hw * 0.42)
    leg_r = cx + int(torso_hw * 0.42)
    leg_y = torso_bot_y

    front_lift = spec.get("front_foot_lift", 0)
    back_lift = spec.get("back_foot_lift", 0)
    front_angle = spec.get("front_foot_angle", 0)
    back_angle = spec.get("back_foot_angle", 0)

    # Left leg = front, Right leg = back (convention)
    for idx, (lx, foot_lift, foot_angle) in enumerate([
        (leg_l, front_lift, front_angle),
        (leg_r, back_lift, back_angle),
    ]):
        ly = leg_y - foot_lift
        ctx.rectangle(lx - leg_w, ly, leg_w * 2, leg_h)
        ctx.set_source_rgb(*_c(PANTS))
        ctx.fill_preserve()
        ctx.set_source_rgb(*_c(LINE))
        ctx.set_line_width(2.0)
        ctx.stroke()
        # Inseam shadow
        ctx.new_path()
        ctx.move_to(lx, ly)
        ctx.line_to(lx, ly + leg_h)
        ctx.set_source_rgb(*_c(PANTS_SH))
        ctx.set_line_width(1.0)
        ctx.stroke()

    # Shoes
    shoe_w = int(hu * 0.28)
    shoe_h = int(hu * 0.18)

    pigeon = abs(front_angle) > 10 and front_angle < 0
    for idx, (lx, foot_lift, foot_angle) in enumerate([
        (leg_l, front_lift, front_angle),
        (leg_r, back_lift, back_angle),
    ]):
        shoe_y = leg_y - foot_lift + leg_h
        d = 1 if foot_angle >= 0 else -1
        shoe_cx = lx + d * (shoe_w // 4)
        if pigeon and idx == 0:
            shoe_cx = lx + (-0.1) * shoe_w
        cairo_ellipse(ctx, shoe_cx, shoe_y + shoe_h // 2, shoe_w // 2, shoe_h // 2)
        ctx.set_source_rgb(*_c(SHOE))
        ctx.fill_preserve()
        ctx.set_source_rgb(*_c(LINE))
        ctx.set_line_width(2.0)
        ctx.stroke()
        # Sole arc
        ctx.new_path()
        ctx.arc(shoe_cx, shoe_y + shoe_h // 2, int(shoe_w * 0.35),
                math.radians(200), math.radians(340))
        ctx.set_source_rgb(*_c(SHOE_SOLE))
        ctx.set_line_width(2.0)
        ctx.stroke()


def _draw_notebook(ctx, chain, hu, show=True, nb_open=False):
    """Draw Cosmo's notebook (optional prop)."""
    if not show:
        return
    cx = chain["torso_cx"]
    torso_hw = chain["torso_hw"]
    torso_bot_y = chain["torso_bot_y"]
    body_top_y = chain["body_top_y"]
    arm_h = int(hu * 0.75)
    arm_y = body_top_y + int(hu * 0.06)

    nb_h = int(hu * 0.30)
    nb_w = int(hu * 0.18)
    if nb_open:
        nb_x = cx - int(nb_w * 0.5)
        nb_y = torso_bot_y - int(hu * 0.55)
        ctx.rectangle(nb_x, nb_y, nb_w * 2, nb_h)
        ctx.set_source_rgb(*_c(NOTEBOOK))
        ctx.fill_preserve()
        ctx.set_source_rgb(*_c(LINE))
        ctx.set_line_width(2.0)
        ctx.stroke()
        # Spine
        ctx.new_path()
        ctx.move_to(nb_x + nb_w, nb_y)
        ctx.line_to(nb_x + nb_w, nb_y + nb_h)
        ctx.set_source_rgb(250 / 255, 240 / 255, 220 / 255)
        ctx.set_line_width(3.0)
        ctx.stroke()
        ctx.new_path()
        ctx.move_to(nb_x + nb_w, nb_y)
        ctx.line_to(nb_x + nb_w, nb_y + nb_h)
        ctx.set_source_rgb(*_c(LINE))
        ctx.set_line_width(1.0)
        ctx.stroke()
    else:
        nb_tuck_x = cx - torso_hw - int(hu * 0.02)
        nb_tuck_y = arm_y + int(arm_h * 0.35)
        ctx.rectangle(nb_tuck_x - nb_w, nb_tuck_y, nb_w, nb_h)
        ctx.set_source_rgb(*_c(NOTEBOOK))
        ctx.fill_preserve()
        ctx.set_source_rgb(*_c(LINE))
        ctx.set_line_width(2.0)
        ctx.stroke()
        ctx.rectangle(nb_tuck_x - 6, nb_tuck_y, 6, nb_h)
        ctx.set_source_rgb(*_c(NOTEBOOK_SP))
        ctx.fill()
        ctx.new_path()
        ctx.move_to(nb_tuck_x - nb_w + 3, nb_tuck_y + 3)
        ctx.line_to(nb_tuck_x - nb_w + 3, nb_tuck_y + nb_h - 3)
        ctx.set_source_rgb(250 / 255, 240 / 255, 220 / 255)
        ctx.set_line_width(2.0)
        ctx.stroke()


# ══════════════════════════════════════════════════════════════════════════════
# Main export function
# ══════════════════════════════════════════════════════════════════════════════

def draw_cosmo(expression="SKEPTICAL", pose=None, scale=1.0,
               facing="front", scene_lighting=None,
               enhance_color=False, notebook_show=True, notebook_open=False):
    """Draw Cosmo and return a cairo.ImageSurface (ARGB32, transparent bg).

    Args:
        expression: One of VALID_EXPRESSIONS (AWKWARD, WORRIED, SURPRISED,
                    SKEPTICAL, DETERMINED, FRUSTRATED). Case insensitive.
        pose:       Optional dict to override individual gesture spec values.
        scale:      Resolution scale factor. 1.0 = expression-sheet scale
                    (hu ~84px). 2.0 = double size, etc.
        facing:     "front" (default). "left"/"right" = horizontal flip.
        scene_lighting: Optional dict with scene lighting parameters:
                    {"preset": "warm_domestic", "key_color": (R,G,B),
                     "tint_alpha": int, "key_dir": "left"|"right"|"above"}
        enhance_color: If True and LTG_TOOL_character_color_enhance is
                       available, apply the full color enhancement pipeline.
        notebook_show: Whether to draw the notebook prop.
        notebook_open: Whether the notebook is open.

    Returns:
        cairo.ImageSurface (FORMAT_ARGB32) with transparent background.
        The surface is sized to fit the character with padding.

    Also returns a geometry dict as second value for downstream use:
        (surface, geom_dict)
    """
    expr_key = expression.upper()
    if expr_key not in GESTURE_SPECS:
        raise ValueError(
            f"Unknown expression '{expression}'. "
            f"Valid: {VALID_EXPRESSIONS}"
        )

    spec = dict(GESTURE_SPECS[expr_key])
    if pose:
        spec.update(pose)

    # Compute head unit based on scale
    base_hu = 84  # Reference hu at expression-sheet scale
    hu = int(base_hu * scale)

    # Compute glasses tilt
    if spec.get("glasses_tilt") is None:
        spec["glasses_tilt"] = spec["head_tilt"] * 0.4

    # Surface size: enough to contain the character at this scale
    # Character height ~= 3.5 * hu. Width ~= 2.5 * hu (with extended arms).
    # Add generous padding for arm extensions.
    char_w = int(hu * 4.0)
    char_h = int(hu * 4.5)
    pad_x = int(hu * 1.0)
    pad_y = int(hu * 0.5)
    surf_w = char_w + 2 * pad_x
    surf_h = char_h + 2 * pad_y

    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, surf_w, surf_h)
    ctx = cairo.Context(surface)

    # Character center
    cx = surf_w // 2
    base_y = pad_y + int(hu * 1.0)  # Head center Y

    # Compute offset chain
    chain = _compute_chain(spec, cx, base_y, hu)

    # Handle facing by mirroring
    if facing in ("left", "right"):
        # Mirror: scale x by -1 around center
        if facing == "left":
            ctx.translate(surf_w, 0)
            ctx.scale(-1, 1)

    # ── Draw order: body -> hair -> head -> glasses -> eyes -> brows -> nose -> mouth -> blush
    _draw_torso(ctx, spec, chain, hu)
    _draw_legs(ctx, spec, chain, hu)
    _draw_arms(ctx, spec, chain, hu)
    _draw_notebook(ctx, chain, hu, show=notebook_show, nb_open=notebook_open)

    head_cx = chain["head_cx"]
    head_cy = chain["head_cy"]

    hair_bbox = _draw_hair(ctx, head_cx, head_cy, hu)
    _draw_head(ctx, head_cx, head_cy, hu)
    glasses_tilt = spec["glasses_tilt"]
    lcx, lcy, rcx, rcy, lens_r = _draw_glasses(ctx, head_cx, head_cy, hu, glasses_tilt)
    _draw_eyes(ctx, lcx, lcy, rcx, rcy, lens_r, spec.get("eye_openness", 1.0))
    _draw_brows(ctx, head_cx, head_cy, hu, glasses_tilt,
                spec.get("brow_data", {}), lcx, lcy, rcx, rcy)
    _draw_nose(ctx, head_cx, head_cy, hu)
    _draw_mouth(ctx, head_cx, head_cy, hu, spec.get("mouth", "neutral"))
    if spec.get("blush", False):
        _draw_blush(ctx, head_cx, head_cy, hu)

    # ── Compute geometry dict for color enhancement / downstream ─────────
    hw = int(hu * 0.43)
    hh = int(hu * 0.50)
    torso_hw = chain["torso_hw"]
    torso_bot_y = chain["torso_bot_y"]
    leg_h = int(hu * 0.90)
    leg_w = int(hu * 0.16)
    shoe_h = int(hu * 0.18)

    char_bbox = (
        cx - torso_hw - int(hu * 0.3),
        head_cy - hh - int(hu * 0.20),
        cx + torso_hw + int(hu * 0.3),
        torso_bot_y + leg_h + shoe_h,
    )
    torso_bbox = (cx - torso_hw, chain["body_top_y"], cx + torso_hw, torso_bot_y)

    hip_cx = chain["hip_cx"]
    leg_l_x = hip_cx - int(torso_hw * 0.42)
    leg_r_x = hip_cx + int(torso_hw * 0.42)
    leg_bboxes = [
        (leg_l_x - leg_w, torso_bot_y, leg_l_x + leg_w, torso_bot_y + leg_h),
        (leg_r_x - leg_w, torso_bot_y, leg_r_x + leg_w, torso_bot_y + leg_h),
    ]

    geom = {
        "char_bbox": char_bbox,
        "face_center": (head_cx, head_cy),
        "face_radius": (hw, hh),
        "hair_bbox": hair_bbox,
        "torso_bbox": torso_bbox,
        "leg_bboxes": leg_bboxes,
        "surface_size": (surf_w, surf_h),
        "center": (cx, base_y),
    }

    # ── Optional color enhancement ───────────────────────────────────────
    if enhance_color and _ENHANCE_AVAILABLE:
        preset = "neutral_daylight"
        if scene_lighting and "preset" in scene_lighting:
            preset = scene_lighting["preset"]

        pil_img = enhance_from_cairo(
            surface, char_bbox,
            face_center=(head_cx, head_cy),
            face_radius=(hw, hh),
            hair_bbox=hair_bbox,
            torso_bbox=torso_bbox,
            leg_bboxes=leg_bboxes,
            scene_preset=preset,
            skin_base=SKIN, skin_hl=SKIN_HL, skin_sh=SKIN_SH,
            blush_color=BLUSH,
        )
        geom["enhanced_pil"] = pil_img

    return surface, geom


# ── Convenience: render to PIL Image directly ────────────────────────────────

def render_cosmo_pil(expression="SKEPTICAL", pose=None, scale=1.0,
                     facing="front", scene_lighting=None,
                     enhance_color=True, **kwargs):
    """Render Cosmo and return a PIL Image (RGBA).

    Convenience wrapper around draw_cosmo(). Returns PIL Image directly.
    """
    surface, geom = draw_cosmo(
        expression=expression, pose=pose, scale=scale,
        facing=facing, scene_lighting=scene_lighting,
        enhance_color=enhance_color, **kwargs,
    )

    if enhance_color and "enhanced_pil" in geom:
        return geom["enhanced_pil"], geom

    pil_img = to_pil_rgba(surface)
    return pil_img, geom


# ══════════════════════════════════════════════════════════════════════════════
# Self-test: render all 6 expressions to a test sheet
# ══════════════════════════════════════════════════════════════════════════════

def _self_test():
    """Render all 6 expressions to a test sheet PNG for validation."""
    from PIL import Image, ImageDraw, ImageFont

    COLS = 3
    ROWS = 2
    PANEL_W = 370
    PANEL_H = 440
    PAD = 12
    HEADER = 48

    total_w = COLS * (PANEL_W + PAD) + PAD
    total_h = HEADER + ROWS * (PANEL_H + PAD) + PAD

    sheet = Image.new("RGB", (total_w, total_h), (28, 24, 20))
    draw = ImageDraw.Draw(sheet)

    try:
        font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
        font_title = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
    except Exception:
        font = font_title = ImageFont.load_default()

    draw.text((PAD, 12),
              "COSMO -- Canonical Renderer Test | char_cosmo v1.0.0 | C53",
              fill=(91, 141, 184), font=font_title)

    for i, expr_name in enumerate(VALID_EXPRESSIONS):
        col = i % COLS
        row = i // COLS
        px = PAD + col * (PANEL_W + PAD)
        py = HEADER + row * (PANEL_H + PAD)

        # Draw panel background
        draw.rectangle([px, py, px + PANEL_W, py + PANEL_H],
                       fill=(240, 220, 180))

        # Render character
        surface, geom = draw_cosmo(expression=expr_name, scale=1.0,
                                   enhance_color=False)
        panel_img = to_pil_rgba(surface)

        # Compute paste offset to center character in panel
        sw, sh = geom["surface_size"]
        ccx, ccy = geom["center"]
        paste_x = px + PANEL_W // 2 - ccx
        paste_y = py + int(PANEL_H * 0.35) - ccy

        # Composite onto sheet
        sheet.paste(panel_img, (paste_x, paste_y), panel_img)
        draw = ImageDraw.Draw(sheet)  # refresh after paste (W004)

        # Label
        draw.text((px + 6, py + PANEL_H - 24), expr_name,
                  fill=(59, 40, 32), font=font)

    # Save
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "..", "characters", "main")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "LTG_CHAR_cosmo_canonical_test.png")

    w, h = sheet.size
    if w > 1280 or h > 1280:
        sheet.thumbnail((1280, 1280), Image.LANCZOS)

    sheet.save(out_path)
    print(f"Saved: {out_path} ({sheet.size[0]}x{sheet.size[1]}px)")
    print(f"Expressions rendered: {VALID_EXPRESSIONS}")
    return out_path


if __name__ == "__main__":
    _self_test()
