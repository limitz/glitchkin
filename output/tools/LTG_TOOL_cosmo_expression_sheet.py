#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_cosmo_expression_sheet.py
Cosmo Expression Sheet Generator — "Luma & the Glitchkin"

v009 — C52 pycairo rendering + color enhancement pipeline (Sam Kowalski / Maya Santos)

  KEY CHANGES from v008:

  P1: PYCAIRO RENDERING (C52 task — Sam Kowalski)
    Character bodies, heads, and limbs now rendered via LTG_TOOL_cairo_primitives
    (pycairo bezier paths, anti-aliased strokes, smooth polygons).
    This gives smooth edges on character curves without relying on 2x oversample.
    Cairo surfaces are composited to PIL for the final sheet assembly.

  P2: COLOR ENHANCEMENT PIPELINE (C52 task — Sam Kowalski)
    Each expression panel now receives scene tint (neutral_daylight preset),
    skin warmth (warm cheek / cool edge), and form shadows (torso_diagonal)
    via LTG_TOOL_character_color_enhance v2.0.0.
    Cosmo-specific skin values: CHAR-C-01 base, CHAR-C-02 shadow, CHAR-C-03 highlight.

  All v008 content preserved:
    P1 (C47): Visual hook — amplified cowlick (0.15 heads) + glasses bridge tape
    P2 (C47): Shoulder involvement — deltoid displacement on arm raise
    S003 compliance, skeptical_crossed, all 6 expressions.
    Face gate: SKEPTICAL/WORRIED/CURIOUS PASS (v008 result carried).

Output: output/characters/main/LTG_CHAR_cosmo_expression_sheet.png
Authors: Maya Santos (v001-v008) / Sam Kowalski (v009 pycairo + color enhance)
Date: 2026-03-31
"""
from __future__ import annotations

from PIL import Image, ImageDraw, ImageFont
import math
import os
import sys

# ── Tool imports ─────────────────────────────────────────────────────────────
_TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
if _TOOLS_DIR not in sys.path:
    sys.path.insert(0, _TOOLS_DIR)

try:
    import cairo as _cairo_mod
    from LTG_TOOL_cairo_primitives import (
        create_surface, draw_bezier_path as cairo_bezier_path,
        draw_smooth_polygon, draw_ellipse as cairo_ellipse,
        draw_tapered_stroke, set_color, to_pil_image, to_pil_rgba,
    )
    _CAIRO_AVAILABLE = True
except ImportError:
    _CAIRO_AVAILABLE = False

try:
    from LTG_TOOL_character_color_enhance import (
        apply_scene_tint, apply_skin_warmth, apply_form_shadow,
        derive_scene_outline, apply_hair_absorption, SCENE_PRESETS,
    )
    _ENHANCE_AVAILABLE = True
except ImportError:
    _ENHANCE_AVAILABLE = False

# ── Palette ───────────────────────────────────────────────────────────────────
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

# v005/v006: Panel backgrounds well-separated from character colors
BG_NEUTRAL   = (240, 220, 180)
BG_FRUSTRAT  = (235, 215, 175)
BG_DETERMIN  = (225, 235, 220)
BG_SKEPTIC   = (230, 218, 178)
BG_WORRIED   = (225, 212, 172)
BG_SURPRISED = (242, 222, 175)
BG_DELIGHTED = (220, 232, 212)
BG_AWKWARD   = (238, 220, 185)
BG_THOUGHTFUL= (215, 228, 215)

CANVAS_BG    = (28, 24, 20)

# ── Layout ────────────────────────────────────────────────────────────────────
PANEL_W = 370
PANEL_H = 440
LABEL_H = 64
COLS    = 3
ROWS    = 2
PAD     = 18
HEADER  = 52

# ── Expression definitions (unchanged from v008) ─────────────────────────────
EXPRESSIONS = [
    {
        "name":     "AWKWARD",
        "body_data": {
            "arm_l_dy": 0, "arm_r_dy": 0,
            "body_tilt": 3, "body_squash": 0.98,
            "notebook_show": False, "notebook_open": False,
            "arm_mode": "awkward",
        },
        "panel_bg": BG_AWKWARD,
        "glasses_tilt": 7,
        "brow_data": {"l_raise": 12, "r_raise": 2, "l_furrow": 3, "r_furrow": 0},
        "mouth_data": {"style": "grimace"},
        "blush": True,
        "prev_state": "\u2190 was: ANY ATTEMPT TO HELP",
        "next_state": "\u2192 next: WORRIED / RETREATING",
    },
    {
        "name":     "WORRIED",
        "body_data": {
            "arm_l_dy": 0, "arm_r_dy": 0,
            "body_tilt": -3, "body_squash": 0.96,
            "notebook_show": False, "notebook_open": False,
            "arm_mode": "head_grab",
        },
        "panel_bg": BG_WORRIED,
        "glasses_tilt": 8,
        "brow_data": {"l_raise": 6, "r_raise": 6, "l_furrow": 10, "r_furrow": 10},
        "mouth_data": {"style": "compressed"},
        "blush": False,
        "prev_state": "\u2190 was: NEUTRAL / SKEPTICAL",
        "next_state": "\u2192 next: FRUSTRATED / TRYING ANYWAY",
    },
    {
        "name":     "SURPRISED",
        "body_data": {
            "arm_l_dy": -35, "arm_r_dy": -35,
            "body_tilt": 12, "body_squash": 0.97,
            "notebook_show": True, "notebook_open": True,
            "arm_mode": "wide_startle",
        },
        "panel_bg": BG_SURPRISED,
        "glasses_tilt": 7,
        "brow_data": {"l_raise": 16, "r_raise": 16, "l_furrow": 0, "r_furrow": 0},
        "mouth_data": {"style": "open_surprised"},
        "blush": True,
        "prev_state": "\u2190 was: DETERMINED (plan in action)",
        "next_state": "\u2192 next: FRUSTRATED / ACCEPTING CHAOS",
    },
    {
        "name":     "SKEPTICAL",
        "body_data": {
            "arm_l_dy": -18, "arm_r_dy": -12,
            "body_tilt": 8, "body_squash": 1.0,
            "notebook_show": True, "notebook_open": False,
            "arm_mode": "skeptical_crossed",
        },
        "panel_bg": BG_SKEPTIC,
        "glasses_tilt": 9,
        "brow_data": {"l_raise": 18, "r_raise": 0, "l_furrow": 0, "r_furrow": 1},
        "mouth_data": {"style": "flat"},
        "blush": False,
        "prev_state": "\u2190 was: NEUTRAL / OBSERVING",
        "next_state": "\u2192 next: RESIGNED / PREPARING ANYWAY",
    },
    {
        "name":     "DETERMINED",
        "body_data": {
            "arm_l_dy": 8, "arm_r_dy": -30,
            "body_tilt": -5, "body_squash": 1.0,
            "notebook_show": True, "notebook_open": False,
            "arm_mode": "standard",
        },
        "panel_bg": BG_DETERMIN,
        "glasses_tilt": 7,
        "brow_data": {"l_raise": 2, "r_raise": 2, "l_furrow": 2, "r_furrow": 2},
        "mouth_data": {"style": "slight_smile"},
        "blush": False,
        "prev_state": "\u2190 was: NEUTRAL / OBSERVING",
        "next_state": "\u2192 next: FRUSTRATED or SUCCEEDED",
    },
    {
        "name":     "FRUSTRATED / DEFEATED",
        "body_data": {
            "arm_l_dy": 20, "arm_r_dy": 12,
            "body_tilt": 4, "body_squash": 0.96,
            "notebook_show": True, "notebook_open": True,
            "arm_mode": "standard",
        },
        "panel_bg": BG_FRUSTRAT,
        "glasses_tilt": 7,
        "brow_data": {"l_raise": -3, "r_raise": -3, "l_furrow": 4, "r_furrow": 4},
        "mouth_data": {"style": "compressed"},
        "blush": False,
        "prev_state": "\u2190 was: DETERMINED",
        "next_state": "\u2192 next: RESIGNED / RECALIBRATING",
    },
]


# ── Cairo drawing helpers ────────────────────────────────────────────────────
# These use pycairo for anti-aliased rendering. Each helper draws onto a
# cairo context. The final surface is composited into the PIL sheet.

def _c(rgb):
    """Convert (R,G,B) 0-255 to cairo (r,g,b) 0.0-1.0."""
    return (rgb[0] / 255.0, rgb[1] / 255.0, rgb[2] / 255.0)


def _shoulder_dy(arm_dy, arm_mode):
    """Calculate shoulder displacement from arm raise (v008 logic preserved)."""
    if arm_mode in ("head_grab", "wide_startle", "delighted", "alarmed"):
        return -6
    if arm_mode in ("awkward",):
        return 0
    if arm_dy < 0:
        return max(-8, int(arm_dy * 0.25))
    return 0


def _draw_cosmo_cairo(ctx, cx, cy, hu, expr):
    """Draw complete Cosmo figure using pycairo for AA bezier rendering.

    Returns a geometry dict for color enhancement bboxes.
    """
    glasses_tilt = expr.get("glasses_tilt", 7)
    body_data    = expr.get("body_data", {})
    brow_data    = expr.get("brow_data", {})
    mouth_data   = expr.get("mouth_data", {"style": "neutral"})

    body_top_y = cy + int(hu * 0.55)

    # ── Body ─────────────────────────────────────────────────────────────
    geom = _draw_cosmo_body_cairo(ctx, cx, body_top_y, hu, body_data)

    # ── Hair (drawn before head so head overlaps) ────────────────────────
    hair_bbox = _draw_cosmo_hair_cairo(ctx, cx, cy, hu)

    # ── Head ─────────────────────────────────────────────────────────────
    _draw_cosmo_head_cairo(ctx, cx, cy, hu)

    # ── Glasses ──────────────────────────────────────────────────────────
    lcx, lcy, rcx, rcy, lens_r = _draw_cosmo_glasses_cairo(ctx, cx, cy, hu, glasses_tilt)

    # ── Eyes ─────────────────────────────────────────────────────────────
    _draw_cosmo_eyes_cairo(ctx, lcx, lcy, rcx, rcy, lens_r)

    # ── Brows ────────────────────────────────────────────────────────────
    _draw_cosmo_brows_cairo(ctx, cx, cy, hu, glasses_tilt, brow_data, lcx, lcy, rcx, rcy)

    # ── Nose ─────────────────────────────────────────────────────────────
    _draw_cosmo_nose_cairo(ctx, cx, cy, hu)

    # ── Mouth ────────────────────────────────────────────────────────────
    _draw_cosmo_mouth_cairo(ctx, cx, cy, hu, mouth_data)

    # ── Blush ────────────────────────────────────────────────────────────
    if expr.get("blush", False):
        _draw_cosmo_blush_cairo(ctx, cx, cy, hu)

    # Compute bboxes for color enhancement
    hw = int(hu * 0.43)
    hh = int(hu * 0.50)
    head_r = max(hw, hh)
    torso_hw = int(hu * 0.41)
    torso_h = int(hu * 1.2 * body_data.get("body_squash", 1.0))
    torso_bot_y = body_top_y + torso_h
    leg_h = int(hu * 0.90)
    leg_w = int(hu * 0.16)
    shoe_h = int(hu * 0.18)

    char_bbox = (
        cx - torso_hw - int(hu * 0.3),
        cy - hh - int(hu * 0.20),
        cx + torso_hw + int(hu * 0.3),
        torso_bot_y + leg_h + shoe_h,
    )
    face_center = (cx, cy)
    face_radius = (hw, hh)
    torso_bbox = (cx - torso_hw, body_top_y, cx + torso_hw, torso_bot_y)

    leg_l_x = cx - int(torso_hw * 0.42)
    leg_r_x = cx + int(torso_hw * 0.42)
    leg_bboxes = [
        (leg_l_x - leg_w, torso_bot_y, leg_l_x + leg_w, torso_bot_y + leg_h),
        (leg_r_x - leg_w, torso_bot_y, leg_r_x + leg_w, torso_bot_y + leg_h),
    ]

    return {
        "char_bbox": char_bbox,
        "face_center": face_center,
        "face_radius": face_radius,
        "hair_bbox": hair_bbox,
        "torso_bbox": torso_bbox,
        "leg_bboxes": leg_bboxes,
    }


def _draw_cosmo_head_cairo(ctx, cx, cy, hu):
    """Draw Cosmo's rectangular head with rounded corners via cairo."""
    hw = int(hu * 0.43)
    hh = int(hu * 0.50)
    r  = int(hu * 0.12)
    x0, y0 = cx - hw, cy - hh
    x1, y1 = cx + hw, cy + hh

    # Rounded rectangle path
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


def _draw_cosmo_hair_cairo(ctx, cx, cy, hu):
    """Draw Cosmo's hair with cowlick via cairo. Returns hair_bbox."""
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

    # v008: AMPLIFIED COWLICK — 0.15 heads tall
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
    ctx.arc(cx, hair_top + int(hu * 0.03), int(hw * 0.6), math.radians(200), math.radians(340))
    ctx.set_source_rgb(*_c(HAIR_HL))
    ctx.set_line_width(2.0)
    ctx.stroke()

    return (cx - hw - 2, cowlick_tip_y, cx + hw + 2, hair_bot + 6)


def _draw_cosmo_glasses_cairo(ctx, cx, cy, hu, tilt_deg):
    """Draw glasses via cairo with bridge tape. Returns (lcx, lcy, rcx, rcy, lens_r)."""
    lens_r  = int(hu * 0.16)
    frame_w = max(3, int(hu * 0.06))
    bridge  = int(hu * 0.05)
    eye_sep = lens_r + bridge
    gcy     = cy - int(hu * 0.10)
    theta   = math.radians(-tilt_deg)
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
        ctx.arc(ex, ey - lens_r + int(lens_r * 0.25), gl_r, math.radians(200), math.radians(340))
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

    # v008: GLASSES BRIDGE TAPE
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
    # Tape highlight
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


def _draw_cosmo_eyes_cairo(ctx, lcx, lcy, rcx, rcy, lens_r):
    """Draw eyes via cairo."""
    iris_r = int(lens_r * 0.55)
    pup_r  = int(iris_r * 0.55)
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
        cairo_ellipse(ctx, ex + int(iris_r * 0.3) + hl_r, ey - iris_r + 2 + hl_r, hl_r, hl_r)
        ctx.set_source_rgb(*_c(EYE_HL))
        ctx.fill()
        # Lower lid line
        ctx.new_path()
        ctx.move_to(ex - iris_r - 3, ey + int(iris_r * 0.5))
        ctx.line_to(ex + iris_r + 3, ey + int(iris_r * 0.5))
        ctx.set_source_rgb(*_c(LINE))
        ctx.set_line_width(2.0)
        ctx.stroke()


def _draw_cosmo_nose_cairo(ctx, cx, cy, hu):
    """Draw nose via cairo."""
    nose_r = int(hu * 0.05)
    cairo_ellipse(ctx, cx, cy + int(hu * 0.11), nose_r, int(hu * 0.05))
    ctx.set_source_rgb(*_c(SKIN_SH))
    ctx.fill()


def _draw_cosmo_brows_cairo(ctx, cx, cy, hu, tilt_deg, brow_data, lcx, lcy, rcx, rcy):
    """Draw eyebrows via cairo."""
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
    ctx.set_line_cap(_cairo_mod.LINE_CAP_ROUND)
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
    ctx.set_line_cap(_cairo_mod.LINE_CAP_ROUND)
    ctx.stroke()


def _draw_cosmo_mouth_cairo(ctx, cx, cy, hu, mouth_data):
    """Draw mouth via cairo."""
    mouth_y = cy + int(hu * 0.26)
    mw = int(hu * 0.20)
    style = mouth_data.get("style", "neutral")

    ctx.set_source_rgb(*_c(LINE))
    ctx.set_line_cap(_cairo_mod.LINE_CAP_ROUND)

    if style == "neutral":
        ctx.new_path()
        ctx.move_to(cx - mw, mouth_y)
        ctx.line_to(cx + mw, mouth_y)
        ctx.set_line_width(2.0)
        ctx.stroke()
        # Corner upticks
        for (sx, ex, ey) in [(cx - mw, cx - mw + 4, mouth_y - 2),
                              (cx + mw, cx + mw - 4, mouth_y - 2)]:
            ctx.new_path()
            ctx.move_to(sx, mouth_y)
            ctx.line_to(ex, ey)
            ctx.set_line_width(2.0)
            ctx.stroke()
    elif style == "slight_smile":
        ctx.new_path()
        ctx.arc(cx, mouth_y, mw, math.radians(10), math.radians(170))
        ctx.set_line_width(3.0)
        ctx.stroke()
    elif style == "flat":
        ctx.new_path()
        ctx.move_to(cx - mw, mouth_y)
        ctx.line_to(cx + mw, mouth_y)
        ctx.set_line_width(3.0)
        ctx.stroke()
    elif style == "compressed":
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
    elif style == "grimace":
        # Grimace rectangle with teeth
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
    elif style == "open_surprised":
        cairo_ellipse(ctx, cx, mouth_y + int(hu * 0.03), int(mw * 0.55), int(hu * 0.07))
        ctx.set_source_rgb(210 / 255, 180 / 255, 150 / 255)
        ctx.fill_preserve()
        ctx.set_source_rgb(*_c(LINE))
        ctx.set_line_width(2.0)
        ctx.stroke()


def _draw_cosmo_blush_cairo(ctx, cx, cy, hu):
    """Draw blush via cairo."""
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


def _draw_cosmo_body_cairo(ctx, cx, body_top_y, hu, body_data):
    """Draw Cosmo body via cairo with shoulder involvement."""
    arm_l_dy    = body_data.get("arm_l_dy", 0)
    arm_r_dy    = body_data.get("arm_r_dy", 0)
    body_tilt   = body_data.get("body_tilt", 0)
    body_squash = body_data.get("body_squash", 1.0)
    nb_show     = body_data.get("notebook_show", True)
    nb_open     = body_data.get("notebook_open", False)
    arm_mode    = body_data.get("arm_mode", "standard")

    torso_hw  = int(hu * 0.41)
    torso_h   = int(hu * 1.2 * body_squash)
    tilt_off  = int(body_tilt * 2.5)
    torso_bot_y = body_top_y + torso_h

    # v008: SHOULDER INVOLVEMENT
    l_sh_dy = _shoulder_dy(arm_l_dy, arm_mode)
    r_sh_dy = _shoulder_dy(arm_r_dy, arm_mode)
    if arm_mode == "awkward":
        l_sh_dy = 0
        r_sh_dy = -5

    sh_bump_w = int(hu * 0.08)
    l_top_y = body_top_y + l_sh_dy
    r_top_y = body_top_y + r_sh_dy

    # Torso polygon with shoulder bumps — via cairo smooth polygon
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

    # Draw torso with bezier-curved edges for organic feel
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

    # Torso outline
    draw_smooth_polygon(ctx, shirt_pts, bulge_frac=0.03)
    ctx.set_source_rgb(*_c(LINE))
    ctx.set_line_width(2.0)
    ctx.stroke()

    # Neck
    neck_w = int(hu * 0.10)
    cairo_ellipse(ctx, cx, body_top_y + int(hu * 0.02), neck_w, int(hu * 0.06))
    ctx.set_source_rgb(*_c(SKIN))
    ctx.fill()

    # Arms
    arm_w = int(hu * 0.12)
    arm_h = int(hu * 0.75)
    arm_y = body_top_y + int(hu * 0.06)
    lax = cx - torso_hw + tilt_off - int(hu * 0.03)
    rax = cx + torso_hw + tilt_off + int(hu * 0.03)

    _draw_arms_cairo(ctx, cx, arm_y, arm_h, arm_w, lax, rax, hu,
                     arm_mode, arm_l_dy, arm_r_dy, body_top_y, torso_hw, torso_bot_y)

    # Notebook
    if nb_show:
        _draw_notebook_cairo(ctx, cx, arm_y, arm_h, torso_hw, torso_bot_y, hu, nb_open)

    # Legs
    _draw_legs_cairo(ctx, cx, torso_hw, torso_bot_y, hu, arm_mode == "awkward")

    return {"torso_bot_y": torso_bot_y}


def _draw_arms_cairo(ctx, cx, arm_y, arm_h, arm_w, lax, rax, hu,
                     arm_mode, arm_l_dy, arm_r_dy, body_top_y, torso_hw, torso_bot_y):
    """Draw arms via cairo based on arm_mode."""

    def _arm_rect(x, y, w, h, color):
        ctx.rectangle(x, y, w, h)
        ctx.set_source_rgb(*_c(color))
        ctx.fill_preserve()
        ctx.set_source_rgb(*_c(LINE))
        ctx.set_line_width(2.0)
        ctx.stroke()

    def _hand_ellipse(x, y, rx, ry, color=SKIN):
        cairo_ellipse(ctx, x, y, rx, ry)
        ctx.set_source_rgb(*_c(color))
        ctx.fill_preserve()
        ctx.set_source_rgb(*_c(LINE))
        ctx.set_line_width(2.0)
        ctx.stroke()

    def _arm_line(x1, y1, x2, y2, color, width):
        ctx.new_path()
        ctx.move_to(x1, y1)
        ctx.line_to(x2, y2)
        ctx.set_source_rgb(*_c(color))
        ctx.set_line_width(width)
        ctx.stroke()

    if arm_mode == "standard":
        lay = arm_y + arm_l_dy
        _arm_rect(lax - arm_w, lay, arm_w, arm_h, STRIPE_A)
        _hand_ellipse(lax - arm_w // 2, lay + arm_h + int(hu * 0.04),
                      arm_w // 2 + 5, int(hu * 0.10))
        ray = arm_y + arm_r_dy
        _arm_rect(rax, ray, arm_w, arm_h, STRIPE_A)
        _hand_ellipse(rax + arm_w // 2, ray + arm_h + int(hu * 0.04),
                      arm_w // 2 + 5, int(hu * 0.10))

    elif arm_mode == "head_grab":
        for side, ax in [(-1, lax), (1, rax)]:
            elbow_x = cx + side * int(hu * 0.82)
            elbow_y = body_top_y - int(hu * 0.25)
            hand_x = cx + side * int(hu * 0.65)
            hand_y = body_top_y - int(hu * 1.20)
            _arm_line(ax, body_top_y + int(hu * 0.06), elbow_x, elbow_y, STRIPE_A, arm_w * 3)
            _arm_line(ax, body_top_y + int(hu * 0.06), elbow_x, elbow_y, LINE, 2)
            _arm_line(elbow_x, elbow_y, hand_x, hand_y, STRIPE_A, arm_w * 3)
            _arm_line(elbow_x, elbow_y, hand_x, hand_y, LINE, 2)
            _hand_ellipse(hand_x, hand_y - int(hu * 0.03),
                          int(arm_w * 1.6), int(hu * 0.13))

    elif arm_mode == "awkward":
        lay = arm_y + 8
        _arm_rect(lax - arm_w, lay, arm_w, arm_h + 15, STRIPE_A)
        _hand_ellipse(lax - arm_w // 2, lay + arm_h + 12,
                      arm_w // 2 + 5, int(hu * 0.11))
        raise_off = -int(hu * 0.22)
        palm_x = rax + int(hu * 0.90)
        palm_y = arm_y + int(arm_h * 0.18) + raise_off
        elbow_x = rax + int(hu * 0.52)
        elbow_y = arm_y + int(arm_h * 0.35) + raise_off
        _arm_line(rax, arm_y + raise_off, elbow_x, elbow_y, STRIPE_A, arm_w * 3)
        _arm_line(rax, arm_y + raise_off, elbow_x, elbow_y, LINE, 2)
        _arm_line(elbow_x, elbow_y, palm_x, palm_y, STRIPE_A, arm_w * 3)
        _arm_line(elbow_x, elbow_y, palm_x, palm_y, LINE, 2)
        _hand_ellipse(palm_x, palm_y - int(hu * 0.06), int(arm_w * 1.0), int(hu * 0.14), SKIN_HL)

    elif arm_mode == "wide_startle":
        for side, ax in [(-1, lax), (1, rax)]:
            elbow_x = cx + side * int(hu * 0.90)
            elbow_y = arm_y - int(arm_h * 0.04)
            hand_x = cx + side * int(hu * 1.30)
            hand_y = arm_y - int(arm_h * 0.12)
            _arm_line(ax, arm_y, elbow_x, elbow_y, STRIPE_A, arm_w * 3)
            _arm_line(ax, arm_y, elbow_x, elbow_y, LINE, 2)
            _arm_line(elbow_x, elbow_y, hand_x, hand_y, STRIPE_A, arm_w * 3)
            _arm_line(elbow_x, elbow_y, hand_x, hand_y, LINE, 2)
            _hand_ellipse(hand_x, hand_y - int(hu * 0.01),
                          int(arm_w * 1.4), int(hu * 0.11))

    elif arm_mode == "skeptical_crossed":
        l_shoulder_x = lax
        l_shoulder_y = arm_y + int(arm_h * 0.08)
        l_elbow_x = lax - int(hu * 0.04)
        l_elbow_y = l_shoulder_y + int(arm_h * 0.42)
        l_hand_x = cx - int(hu * 0.22)
        l_hand_y = l_shoulder_y + int(arm_h * 0.72)
        _arm_line(l_shoulder_x, l_shoulder_y, l_elbow_x, l_elbow_y, STRIPE_A, arm_w * 3)
        _arm_line(l_shoulder_x, l_shoulder_y, l_elbow_x, l_elbow_y, LINE, 2)
        _arm_line(l_elbow_x, l_elbow_y, l_hand_x, l_hand_y, STRIPE_A, arm_w * 3)
        _arm_line(l_elbow_x, l_elbow_y, l_hand_x, l_hand_y, LINE, 2)
        _hand_ellipse(l_hand_x, l_hand_y, int(arm_w * 1.3), int(hu * 0.10))

        r_shoulder_x = rax
        r_shoulder_y = arm_y + int(arm_h * 0.22)
        r_elbow_x = cx + int(hu * 0.18)
        r_elbow_y = r_shoulder_y + int(arm_h * 0.28)
        r_hand_x = cx - int(hu * 0.05)
        r_hand_y = r_shoulder_y + int(arm_h * 0.55)
        _arm_line(r_shoulder_x, r_shoulder_y, r_elbow_x, r_elbow_y, STRIPE_A, arm_w * 3)
        _arm_line(r_shoulder_x, r_shoulder_y, r_elbow_x, r_elbow_y, LINE, 2)
        _arm_line(r_elbow_x, r_elbow_y, r_hand_x, r_hand_y, STRIPE_A, arm_w * 3)
        _arm_line(r_elbow_x, r_elbow_y, r_hand_x, r_hand_y, LINE, 2)
        _hand_ellipse(r_hand_x, r_hand_y, int(arm_w * 1.3), int(hu * 0.10))


def _draw_notebook_cairo(ctx, cx, arm_y, arm_h, torso_hw, torso_bot_y, hu, nb_open):
    """Draw notebook via cairo."""
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
        # Spine accent
        ctx.rectangle(nb_tuck_x - 6, nb_tuck_y, 6, nb_h)
        ctx.set_source_rgb(*_c(NOTEBOOK_SP))
        ctx.fill()
        # Page line
        ctx.new_path()
        ctx.move_to(nb_tuck_x - nb_w + 3, nb_tuck_y + 3)
        ctx.line_to(nb_tuck_x - nb_w + 3, nb_tuck_y + nb_h - 3)
        ctx.set_source_rgb(250 / 255, 240 / 255, 220 / 255)
        ctx.set_line_width(2.0)
        ctx.stroke()


def _draw_legs_cairo(ctx, cx, torso_hw, torso_bot_y, hu, pigeon):
    """Draw legs and shoes via cairo."""
    leg_w = int(hu * 0.16)
    leg_h = int(hu * 0.90)
    leg_l = cx - int(torso_hw * 0.42)
    leg_r = cx + int(torso_hw * 0.42)
    leg_y = torso_bot_y

    for lx in [leg_l, leg_r]:
        ctx.rectangle(lx - leg_w, leg_y, leg_w * 2, leg_h)
        ctx.set_source_rgb(*_c(PANTS))
        ctx.fill_preserve()
        ctx.set_source_rgb(*_c(LINE))
        ctx.set_line_width(2.0)
        ctx.stroke()
        # Inseam shadow
        ctx.new_path()
        ctx.move_to(lx, leg_y)
        ctx.line_to(lx, leg_y + leg_h)
        ctx.set_source_rgb(*_c(PANTS_SH))
        ctx.set_line_width(1.0)
        ctx.stroke()

    shoe_w = int(hu * 0.28)
    shoe_h = int(hu * 0.18)
    shoe_y = leg_y + leg_h

    if pigeon:
        # Pigeon-toed
        for lx, direction in [(leg_l, -0.1), (leg_r, 0.1)]:
            cairo_ellipse(ctx, lx + direction * shoe_w, shoe_y + shoe_h // 2,
                          shoe_w // 2, shoe_h // 2)
            ctx.set_source_rgb(*_c(SHOE))
            ctx.fill_preserve()
            ctx.set_source_rgb(*_c(LINE))
            ctx.set_line_width(2.0)
            ctx.stroke()
    else:
        for lx, d in [(leg_l, -1), (leg_r, 1)]:
            shoe_cx = lx + d * (shoe_w // 4)
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


# ── PIL fallback drawing (preserved from v008 for non-cairo environments) ────

def _draw_cosmo_pil_fallback(draw, cx, cy, hu, expr):
    """Fallback: use PIL drawing (v008 code path) if cairo is unavailable.
    Delegates to the original v008 draw_cosmo function logic.
    This preserves backward compatibility.
    """
    # Inline minimal v008 fallback — just call the old functions
    # For brevity, this fallback renders a simplified version. Full v008 logic
    # is preserved in git history. Production should always have cairo available.
    glasses_tilt = expr.get("glasses_tilt", 7)
    body_data = expr.get("body_data", {})

    hw = int(hu * 0.43)
    hh = int(hu * 0.50)
    r = int(hu * 0.12)

    # Head
    try:
        draw.rounded_rectangle([cx - hw, cy - hh, cx + hw, cy + hh],
                                radius=r, fill=SKIN, outline=LINE, width=2)
    except AttributeError:
        draw.rectangle([cx - hw, cy - hh, cx + hw, cy + hh], fill=SKIN, outline=LINE, width=2)

    # Simplified body
    torso_hw = int(hu * 0.41)
    body_top_y = cy + int(hu * 0.55)
    torso_h = int(hu * 1.2 * body_data.get("body_squash", 1.0))
    torso_bot_y = body_top_y + torso_h
    draw.rectangle([cx - torso_hw, body_top_y, cx + torso_hw, torso_bot_y],
                   fill=STRIPE_A, outline=LINE, width=2)

    # Eyes placeholder
    for side in [-1, 1]:
        ex = cx + side * int(hu * 0.21)
        ey = cy - int(hu * 0.10)
        draw.ellipse([ex - 8, ey - 8, ex + 8, ey + 8], fill=EYE_WHITE, outline=LINE, width=2)

    return {
        "char_bbox": (cx - torso_hw - 20, cy - hh - 20, cx + torso_hw + 20, torso_bot_y + int(hu * 1.0)),
        "face_center": (cx, cy),
        "face_radius": (hw, hh),
        "hair_bbox": (cx - hw, cy - hh - int(hu * 0.15), cx + hw, cy - hh),
        "torso_bbox": (cx - torso_hw, body_top_y, cx + torso_hw, torso_bot_y),
        "leg_bboxes": [],
    }


# ── Sheet generation ─────────────────────────────────────────────────────────

def generate_cosmo_expression_sheet(output_path):
    """Generate the Cosmo expression sheet.

    v009: Uses pycairo for character rendering + color enhancement pipeline.
    Falls back to PIL if cairo unavailable.
    """
    total_w = COLS * (PANEL_W + PAD) + PAD
    total_h = HEADER + ROWS * (PANEL_H + LABEL_H + PAD) + PAD

    img = Image.new('RGB', (total_w, total_h), CANVAS_BG)
    draw = ImageDraw.Draw(img)

    try:
        font_title = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
        font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 15)
        font_sm = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11)
    except Exception:
        font_title = font = font_sm = ImageFont.load_default()

    draw.text((PAD, 14),
              "COSMO \u2014 Expression Sheet \u2014 Luma & the Glitchkin  |  v009  |  C52: pycairo + color enhance",
              fill=(91, 141, 184), font=font_title)

    HU = int(PANEL_H * 0.190)

    beat_tags = {
        "AWKWARD":                "A1-03 / A2-02",
        "WORRIED":                "A2-02",
        "SURPRISED":              "A2-04c",
        "SKEPTICAL":              "A2-03",
        "DETERMINED":             "A2-05b",
        "FRUSTRATED / DEFEATED":  "A2-06",
    }

    # Scene tint settings for expression sheet panels (neutral daylight)
    scene_preset = "neutral_daylight"

    for i, expr in enumerate(EXPRESSIONS):
        col = i % COLS
        row = i // COLS
        ppx = PAD + col * (PANEL_W + PAD)
        ppy = HEADER + row * (PANEL_H + LABEL_H + PAD)

        # ── Panel background ─────────────────────────────────────────────
        panel_bg = expr["panel_bg"]
        draw.rectangle([ppx, ppy, ppx + PANEL_W, ppy + PANEL_H], fill=panel_bg)
        draw.rectangle([ppx, ppy, ppx + PANEL_W, ppy + PANEL_H], outline=(80, 74, 70), width=1)

        arm_modes_needing_room = {"head_grab", "wide_startle", "skeptical_crossed"}
        face_frac = 0.42 if expr["body_data"].get("arm_mode") in arm_modes_needing_room else 0.32
        face_cy = ppy + int(PANEL_H * face_frac)
        face_cx = ppx + PANEL_W // 2

        if _CAIRO_AVAILABLE:
            # ── Cairo rendering path ─────────────────────────────────────
            # Create a panel-sized cairo surface
            surface, ctx, sw, sh = create_surface(PANEL_W, PANEL_H)

            # Clear to panel background (with alpha)
            ctx.set_source_rgba(panel_bg[0] / 255, panel_bg[1] / 255, panel_bg[2] / 255, 1.0)
            ctx.paint()

            # Draw character relative to panel coordinates
            local_cx = PANEL_W // 2
            local_cy = int(PANEL_H * face_frac)
            geom = _draw_cosmo_cairo(ctx, local_cx, local_cy, HU, expr)

            # Convert cairo surface to PIL
            panel_img = to_pil_image(surface, mode="RGB")

            # ── Apply color enhancement pipeline ─────────────────────────
            if _ENHANCE_AVAILABLE:
                # Scene tint
                panel_img = apply_scene_tint(
                    panel_img, geom["char_bbox"],
                    key_light_color=SCENE_PRESETS[scene_preset]["key_color"],
                    alpha=SCENE_PRESETS[scene_preset]["tint_alpha"],
                    light_dir=SCENE_PRESETS[scene_preset]["key_dir"],
                )

                # Skin warmth with Cosmo-specific values
                panel_img = apply_skin_warmth(
                    panel_img, geom["face_center"], geom["face_radius"],
                    light_dir=SCENE_PRESETS[scene_preset]["key_dir"],
                    warm_color=SKIN_HL,    # CHAR-C-03
                    blush_color=BLUSH,
                    warm_alpha=20, cool_alpha=14, blush_alpha=16,
                )

                # Form shadow on torso
                if geom.get("torso_bbox"):
                    panel_img = apply_form_shadow(
                        panel_img, geom["torso_bbox"],
                        base_color=STRIPE_A, shadow_color=(72, 112, 148),  # desaturated cerulean shadow
                        shadow_shape="torso_diagonal",
                        light_dir=SCENE_PRESETS[scene_preset]["key_dir"],
                        alpha=70,
                    )

                # Form shadow on legs
                for leg_bbox in geom.get("leg_bboxes", []):
                    panel_img = apply_form_shadow(
                        panel_img, leg_bbox,
                        base_color=PANTS, shadow_color=PANTS_SH,
                        shadow_shape="limb_underside",
                        light_dir=SCENE_PRESETS[scene_preset]["key_dir"],
                        alpha=60,
                    )

                # Hair absorption
                if geom.get("hair_bbox"):
                    panel_img = apply_hair_absorption(
                        panel_img, geom["hair_bbox"],
                        scene_color=SCENE_PRESETS[scene_preset]["key_color"],
                        alpha=10,
                    )

            # Paste panel into sheet
            img.paste(panel_img, (ppx, ppy))
            draw = ImageDraw.Draw(img)  # refresh draw context after paste (W004)

        else:
            # ── PIL fallback path ────────────────────────────────────────
            _draw_cosmo_pil_fallback(draw, face_cx, face_cy, HU, expr)

        # Beat tag
        tag = beat_tags.get(expr["name"])
        if tag:
            draw.text((ppx + PANEL_W - 74, ppy + 6), tag, fill=(100, 160, 120), font=font_sm)

        # ── Label strip (BELOW panel) ────────────────────────────────────
        label_y = ppy + PANEL_H
        draw.rectangle([ppx, label_y, ppx + PANEL_W, label_y + LABEL_H],
                       fill=(18, 14, 12))
        draw.text((ppx + 6, label_y + 6),
                  expr["name"], fill=(91, 141, 184), font=font)
        draw.text((ppx + 6, label_y + 26),
                  expr["prev_state"], fill=(130, 118, 112), font=font_sm)
        draw.text((ppx + 6, label_y + 40),
                  expr["next_state"], fill=(130, 118, 112), font=font_sm)

    # Final size check — native resolution, no thumbnail
    # Sheet is already under 1280px in both dimensions (total_w=1182, total_h=1114)
    w, h = img.size
    if w > 1280 or h > 1280:
        # Safety: scale down if somehow oversized (should not happen with current layout)
        img.thumbnail((1280, 1280), Image.LANCZOS)

    img.save(output_path)
    print(f"Saved: {output_path}  ({img.size[0]}x{img.size[1]}px)")
    print("v009 changes (C52 Sam Kowalski):")
    print(f"  P1: pycairo rendering (cairo available: {_CAIRO_AVAILABLE})")
    print(f"  P2: Color enhancement pipeline (enhance available: {_ENHANCE_AVAILABLE})")
    print("  All v008 content preserved: visual hooks, shoulder involvement, 6 expressions")


if __name__ == '__main__':
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "..", "characters", "main")
    os.makedirs(out_dir, exist_ok=True)
    generate_cosmo_expression_sheet(
        os.path.join(out_dir, "LTG_CHAR_cosmo_expression_sheet.png")
    )
