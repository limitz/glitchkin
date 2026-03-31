# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_luma_motion.py
Ryo Hasegawa / Cycle 52 — Full rebuild with pycairo + gesture-first construction

Motion Spec Sheet — LUMA
4 panels: Idle/Curious | Sprint Anticipation | Discovery Reaction (2-beat) | Landing/Stop
Output: output/characters/motion/LTG_CHAR_luma_motion.png
Canvas: 1280x720 (within limit)

C52 REBUILD: All figures now use gesture_spine() + body_from_spine() from curve_draw.
Rendering via pycairo for anti-aliased bezier curves. Composited to PIL for annotations.
Lee's gesture spec (gesture_pose_analysis_c50.md) drives all pose construction.

NOTE: This is the canonical LTG_TOOL_ version.
"""

import os
import sys
import math
import random
import json

import numpy as np

# --- Path setup ---
_TOOL_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.abspath(os.path.join(_TOOL_DIR, "..", ".."))
_OUTPUT_DIR = os.path.join(_PROJECT_ROOT, "output", "characters", "motion")
os.makedirs(_OUTPUT_DIR, exist_ok=True)

if _TOOL_DIR not in sys.path:
    sys.path.insert(0, _TOOL_DIR)

from PIL import Image, ImageDraw, ImageFont
import cairo

# Import curve_draw library (Sam's C50/51 build)
from LTG_TOOL_curve_draw import (
    gesture_spine, spine_point_at, spine_tangent_at, spine_perpendicular_at,
    body_from_spine, smooth_path,
)

# Import cairo primitives (Rin's C51 build)
from LTG_TOOL_cairo_primitives import (
    create_surface, to_pil_image, to_pil_rgba, set_color,
    draw_ellipse, draw_smooth_polygon, draw_tapered_stroke,
)

# Import canonical Luma renderer
from LTG_TOOL_char_luma import (
    draw_luma, draw_luma_on_context, cairo_surface_to_pil as _char_surface_to_pil,
)

# --- RNG seed for reproducibility ---
random.seed(52)
np.random.seed(52)

# --- C40: Load HEADER_H from sheet geometry config ---
_CONFIG_PATH = os.path.join(_TOOL_DIR, "sheet_geometry_config.json")

def _load_header_h(family="luma", default=54):
    try:
        with open(_CONFIG_PATH) as f:
            cfg = json.load(f)
        geo = cfg.get("families", {}).get(family, {})
        return geo.get("panel_top_abs", default)
    except Exception:
        return default

_LUMA_PANEL_TOP = _load_header_h("luma", default=54)

# --- CANONICAL COLORS (from master_palette.md) ---
HOODIE_ORANGE    = (230, 100,  35)
SKIN_MID         = (210, 155, 110)
HAIR_DARK        = ( 26,  15,  10)
DEEP_COCOA       = ( 59,  40,  32)
WARM_AMBER_IRIS  = (200, 125,  62)
PANTS_SAGE       = (130, 145, 115)
SHOE_DARK        = ( 60,  45,  35)
PIXEL_CYAN       = (  0, 212, 232)
ANNOTATION_BG    = (248, 244, 236)
PANEL_BORDER     = (180, 165, 145)
LABEL_BG         = ( 50,  38,  28)
LABEL_TEXT       = (248, 244, 236)
LINE_COLOR       = DEEP_COCOA
MOTION_ARROW     = (220,  60,  20)
BEAT_COLOR       = ( 80, 120, 200)
ACCENT_DASH      = (200, 190, 175)
GESTURE_RED      = (220,  50,  40)
ANCHOR_GREEN     = ( 60, 180,  80)

# --- CANVAS ---
W, H = 1280, 720
COLS, ROWS = 4, 1
PAD = 14
_TITLE_H = max(_LUMA_PANEL_TOP - PAD, 40)
PANEL_W = (W - PAD * (COLS + 1)) // COLS
PANEL_H = H - PAD * 2 - _TITLE_H

# Render scale for AA
RENDER_SCALE = 2


def panel_origin(col):
    """Top-left (x, y) of panel col (0-based)."""
    x = PAD + col * (PANEL_W + PAD)
    y = _LUMA_PANEL_TOP
    return x, y


# ===================================================================
# Cairo helpers
# ===================================================================

def rgb_to_cairo(rgb, alpha=1.0):
    return (rgb[0] / 255.0, rgb[1] / 255.0, rgb[2] / 255.0, alpha)


def cairo_fill_path(ctx, points, fill_rgb, outline_rgb=None, line_w=3.0):
    if not points:
        return
    r, g, b = fill_rgb[0] / 255, fill_rgb[1] / 255, fill_rgb[2] / 255
    ctx.new_path()
    ctx.move_to(points[0][0], points[0][1])
    for pt in points[1:]:
        ctx.line_to(pt[0], pt[1])
    ctx.close_path()
    ctx.set_source_rgba(r, g, b, 1.0)
    if outline_rgb:
        ctx.fill_preserve()
        ro, go, bo = outline_rgb[0] / 255, outline_rgb[1] / 255, outline_rgb[2] / 255
        ctx.set_source_rgba(ro, go, bo, 1.0)
        ctx.set_line_width(line_w)
        ctx.stroke()
    else:
        ctx.fill()


def cairo_bezier_fill(ctx, anchors, fill_rgb, outline_rgb=None, line_w=3.0, tension=0.33):
    pts = smooth_path(anchors, tension=tension, closed=True, points_per_segment=60)
    cairo_fill_path(ctx, pts, fill_rgb, outline_rgb, line_w)


def cairo_circle(ctx, cx, cy, r, fill_rgb, outline_rgb=None, line_w=2.0):
    rr, gg, bb = fill_rgb[0] / 255, fill_rgb[1] / 255, fill_rgb[2] / 255
    ctx.new_path()
    ctx.arc(cx, cy, r, 0, 2 * math.pi)
    ctx.set_source_rgba(rr, gg, bb, 1.0)
    if outline_rgb:
        ctx.fill_preserve()
        ro, go, bo = outline_rgb[0] / 255, outline_rgb[1] / 255, outline_rgb[2] / 255
        ctx.set_source_rgba(ro, go, bo, 1.0)
        ctx.set_line_width(line_w)
        ctx.stroke()
    else:
        ctx.fill()


def cairo_ellipse(ctx, cx, cy, rx, ry, fill_rgb, outline_rgb=None, line_w=2.0):
    rr, gg, bb = fill_rgb[0] / 255, fill_rgb[1] / 255, fill_rgb[2] / 255
    ctx.save()
    ctx.translate(cx, cy)
    ctx.scale(rx, ry)
    ctx.new_path()
    ctx.arc(0, 0, 1.0, 0, 2 * math.pi)
    ctx.restore()
    ctx.set_source_rgba(rr, gg, bb, 1.0)
    if outline_rgb:
        ctx.fill_preserve()
        ro, go, bo = outline_rgb[0] / 255, outline_rgb[1] / 255, outline_rgb[2] / 255
        ctx.set_source_rgba(ro, go, bo, 1.0)
        ctx.set_line_width(line_w)
        ctx.stroke()
    else:
        ctx.fill()


def cairo_tapered_limb(ctx, p1, p2, w1, w2, fill_rgb, outline_rgb, line_w=3.0, bend=0.0):
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    length = math.sqrt(dx * dx + dy * dy)
    if length < 1:
        return
    ax, ay = dx / length, dy / length
    px, py = -ay, ax

    hw1, hw2 = w1 / 2, w2 / 2
    tl = (p1[0] + px * hw1, p1[1] + py * hw1)
    bl = (p2[0] + px * hw2, p2[1] + py * hw2)
    tr = (p1[0] - px * hw1, p1[1] - py * hw1)
    br = (p2[0] - px * hw2, p2[1] - py * hw2)

    mx = (p1[0] + p2[0]) / 2 + px * bend * length
    my = (p1[1] + p2[1]) / 2 + py * bend * length

    r, g, b = fill_rgb[0] / 255, fill_rgb[1] / 255, fill_rgb[2] / 255
    ctx.new_path()
    lmx = mx + px * hw1 * 0.7
    lmy = my + py * hw1 * 0.7
    ctx.move_to(tl[0], tl[1])
    ctx.curve_to(
        (tl[0] + lmx) / 2, (tl[1] + lmy) / 2,
        (lmx + bl[0]) / 2, (lmy + bl[1]) / 2,
        bl[0], bl[1]
    )
    ctx.line_to(br[0], br[1])
    rmx = mx - px * hw2 * 0.7
    rmy = my - py * hw2 * 0.7
    ctx.curve_to(
        (br[0] + rmx) / 2, (br[1] + rmy) / 2,
        (rmx + tr[0]) / 2, (rmy + tr[1]) / 2,
        tr[0], tr[1]
    )
    ctx.close_path()
    ctx.set_source_rgba(r, g, b, 1.0)
    ctx.fill_preserve()
    if outline_rgb:
        ro, go, bo = outline_rgb[0] / 255, outline_rgb[1] / 255, outline_rgb[2] / 255
        ctx.set_source_rgba(ro, go, bo, 1.0)
        ctx.set_line_width(line_w)
        ctx.stroke()


def cairo_stroke_line(ctx, p0, p1, color_rgb, width=3.0):
    r, g, b = color_rgb[0] / 255, color_rgb[1] / 255, color_rgb[2] / 255
    ctx.new_path()
    ctx.move_to(p0[0], p0[1])
    ctx.line_to(p1[0], p1[1])
    ctx.set_source_rgba(r, g, b, 1.0)
    ctx.set_line_width(width)
    ctx.stroke()


def cairo_surface_to_pil(surface):
    w = surface.get_width()
    h = surface.get_height()
    data = surface.get_data()
    arr = np.frombuffer(data, dtype=np.uint8).reshape((h, w, 4)).copy()
    arr_rgba = np.zeros_like(arr)
    arr_rgba[:, :, 0] = arr[:, :, 2]
    arr_rgba[:, :, 1] = arr[:, :, 1]
    arr_rgba[:, :, 2] = arr[:, :, 0]
    arr_rgba[:, :, 3] = arr[:, :, 3]
    return Image.fromarray(arr_rgba, "RGBA")


# ===================================================================
# draw_shoulder_arm v2 — geometry-compute layer
# ===================================================================

class ArmGeometry:
    """Pure geometry result from compute_arm_geometry(). No rendering."""
    __slots__ = (
        'shoulder_x', 'shoulder_y', 'elbow_x', 'elbow_y',
        'hand_x', 'hand_y', 'deltoid_cx', 'deltoid_cy', 'deltoid_r',
        'upper_w1', 'upper_w2', 'lower_w1', 'lower_w2',
        'shoulder_shifted', 'arm_angle_deg', 'side',
    )

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


def compute_arm_geometry(
    spine_shoulder_pt, spine_shoulder_perp, arm_angle_deg, arm_length,
    scale=1.0, side=1, elbow_bend_factor=0.12, two_segment=True,
):
    """Compute arm geometry from a gesture spine shoulder point.

    Works with gesture spines: shoulder position and perpendicular come from
    body_from_spine landmarks, not from a rectangle torso.

    Args:
        spine_shoulder_pt: (x, y) from body_from_spine landmarks
        spine_shoulder_perp: (px, py) perpendicular unit vector at shoulder
        arm_angle_deg: angle of arm, 0=horizontal out, +up, -down
        arm_length: total arm length in pixels
        scale: character scale
        side: +1 right shoulder (viewer's left), -1 left shoulder (viewer's right)
        elbow_bend_factor: elbow offset as fraction of arm_length
        two_segment: if True, compute elbow position

    Returns:
        ArmGeometry with all computed points
    """
    sx, sy = spine_shoulder_pt
    angle_rad = math.radians(arm_angle_deg)

    # Shoulder involvement: shift based on arm angle
    arm_dx = math.cos(angle_rad) * arm_length * side
    arm_dy = -math.sin(angle_rad) * arm_length
    rise_ratio = max(0.0, -arm_dy / arm_length)
    shoulder_rise = rise_ratio * 5.0 * scale
    spread_ratio = abs(arm_dx) / arm_length if arm_length > 0 else 0.0
    shoulder_spread = spread_ratio * 4.0 * scale
    arm_going_outward = (arm_dx * side) > 0

    if arm_going_outward:
        shift_x = side * shoulder_spread
        shift_y = -shoulder_rise
    else:
        cross_ratio = min(1.0, abs(arm_dx) / (arm_length * 0.5)) if arm_length > 0 else 0.0
        shift_x = -side * cross_ratio * 3.5 * scale
        shift_y = cross_ratio * 1.5 * scale - shoulder_rise * 0.5

    shifted_sx = sx + shift_x
    shifted_sy = sy + shift_y

    # Hand position
    hand_x = shifted_sx + arm_dx
    hand_y = shifted_sy + arm_dy

    # Elbow (midpoint with bend offset)
    if two_segment:
        mid_x = (shifted_sx + hand_x) / 2
        mid_y = (shifted_sy + hand_y) / 2
        arm_perp_x = -arm_dy / arm_length if arm_length > 0 else 0
        arm_perp_y = arm_dx / arm_length if arm_length > 0 else 1
        elbow_offset = elbow_bend_factor * arm_length
        elbow_x = mid_x + arm_perp_x * elbow_offset * side
        elbow_y = mid_y + arm_perp_y * elbow_offset * side
    else:
        elbow_x = (shifted_sx + hand_x) / 2
        elbow_y = (shifted_sy + hand_y) / 2

    # Deltoid
    deltoid_r = max(2, int(4 * scale + 0.5))
    bump_offset = deltoid_r * 0.6
    deltoid_cx = shifted_sx + math.cos(angle_rad) * bump_offset * side
    deltoid_cy = shifted_sy - math.sin(angle_rad) * bump_offset

    # Widths (tapered)
    base_w = arm_length * 0.22
    upper_w1 = base_w * 1.2  # shoulder end wider
    upper_w2 = base_w * 0.85  # elbow
    lower_w1 = base_w * 0.85  # elbow
    lower_w2 = base_w * 0.65  # wrist

    return ArmGeometry(
        shoulder_x=shifted_sx, shoulder_y=shifted_sy,
        elbow_x=elbow_x, elbow_y=elbow_y,
        hand_x=hand_x, hand_y=hand_y,
        deltoid_cx=deltoid_cx, deltoid_cy=deltoid_cy, deltoid_r=deltoid_r,
        upper_w1=upper_w1, upper_w2=upper_w2,
        lower_w1=lower_w1, lower_w2=lower_w2,
        shoulder_shifted=(shifted_sx, shifted_sy),
        arm_angle_deg=arm_angle_deg, side=side,
    )


def render_arm_cairo(ctx, geom, fill_rgb, outline_rgb, skin_rgb, lw=3.0,
                     clothing="hoodie", two_segment=True, hand_r=None):
    """Render an arm from ArmGeometry using cairo.

    Args:
        ctx: cairo Context
        geom: ArmGeometry from compute_arm_geometry
        fill_rgb: sleeve color
        outline_rgb: line color
        skin_rgb: hand color
        lw: line width
        clothing: hoodie/cardigan/fitted/bare for deltoid style
        two_segment: draw upper+lower or single segment
        hand_r: hand circle radius (auto from geometry if None)
    """
    if hand_r is None:
        hand_r = max(3, geom.lower_w2 * 0.8)

    # Deltoid bump
    dr = geom.deltoid_r
    if clothing == "hoodie":
        cairo_ellipse(ctx, geom.deltoid_cx, geom.deltoid_cy,
                      dr * 1.4, dr, fill_rgb, outline_rgb, max(1, lw - 1))
    elif clothing == "cardigan":
        cairo_circle(ctx, geom.deltoid_cx, geom.deltoid_cy, dr,
                     fill_rgb, outline_rgb, max(1, lw - 1))
    else:
        cairo_circle(ctx, geom.deltoid_cx, geom.deltoid_cy, dr,
                     fill_rgb, outline_rgb, max(1, lw - 1))

    if two_segment:
        # Upper arm
        cairo_tapered_limb(ctx,
                           (geom.shoulder_x, geom.shoulder_y),
                           (geom.elbow_x, geom.elbow_y),
                           geom.upper_w1, geom.upper_w2,
                           fill_rgb, outline_rgb, lw, bend=0.04)
        # Lower arm
        cairo_tapered_limb(ctx,
                           (geom.elbow_x, geom.elbow_y),
                           (geom.hand_x, geom.hand_y),
                           geom.lower_w1, geom.lower_w2,
                           fill_rgb, outline_rgb, lw, bend=-0.02)
    else:
        cairo_tapered_limb(ctx,
                           (geom.shoulder_x, geom.shoulder_y),
                           (geom.hand_x, geom.hand_y),
                           geom.upper_w1, geom.lower_w2,
                           fill_rgb, outline_rgb, lw, bend=0.05)

    # Hand
    cairo_circle(ctx, geom.hand_x, geom.hand_y, hand_r,
                 skin_rgb, outline_rgb, max(1, lw - 1))


# ===================================================================
# Gesture-first figure drawing
# ===================================================================

def draw_gesture_luma(ctx, panel_w, panel_h, ground_y, center_x, hr,
                      gesture_params, lw=4.0, draw_gesture_line=True):
    """Draw Luma using gesture-first construction via pycairo.

    Args:
        ctx: cairo Context (at render scale)
        panel_w, panel_h: panel dimensions at render scale
        ground_y: Y position of ground line at render scale
        center_x: horizontal center at render scale
        hr: head radius at render scale
        gesture_params: dict with keys:
            curve_amount, curve_direction, curve_type,
            head_offset_x, head_offset_y (relative to body_height),
            weight_foot_offset, free_foot_offset, free_foot_lift,
            shoulder_rise_l, shoulder_rise_r,
            hip_tilt_px,
            left_arm_angle, right_arm_angle,
            left_arm_bend, right_arm_bend,
            hair_trail_dx (px), hair_lift (px),
            hoodie_flare (px), show_hoodie_settle (bool)
        lw: line width
        draw_gesture_line: if True, draw the red dashed gesture spine
    Returns:
        dict with key positions for annotation placement
    """
    gp = gesture_params
    body_height = hr * 2 / 0.37  # from 37% head ratio

    # Head position
    head_y = ground_y - body_height + gp.get('head_offset_y', 0)
    head_x = center_x + gp.get('head_offset_x', 0)
    head_pos = (head_x, head_y)

    # Weight foot position
    wf_offset = gp.get('weight_foot_offset', 0)
    weight_foot_pos = (center_x + wf_offset, ground_y)

    # Generate gesture spine
    spine = gesture_spine(
        head_pos, weight_foot_pos,
        curve_amount=gp.get('curve_amount', 0.05),
        curve_direction=gp.get('curve_direction', 'right'),
        curve_type=gp.get('curve_type', 's'),
        num_points=40,
    )

    # Body landmarks from spine
    shoulder_width = hr * 2.0
    waist_width = hr * 1.5
    hip_width = hr * 1.6
    landmarks = body_from_spine(spine, hr, shoulder_width, waist_width, hip_width)

    head_center = landmarks["head_center"]
    shoulder_l = landmarks["shoulder_l"]
    shoulder_r = landmarks["shoulder_r"]
    waist_l = landmarks["waist_l"]
    waist_r = landmarks["waist_r"]
    hip_l = landmarks["hip_l"]
    hip_r = landmarks["hip_r"]

    # Apply counterpose
    sr_l = gp.get('shoulder_rise_l', 0)
    sr_r = gp.get('shoulder_rise_r', 0)
    shoulder_l_s = (shoulder_l[0] - hr * 0.03, shoulder_l[1] - sr_l)
    shoulder_r_s = (shoulder_r[0] + hr * 0.03, shoulder_r[1] - sr_r)

    hip_tilt = gp.get('hip_tilt_px', 0)
    hip_l_s = (hip_l[0], hip_l[1] + hip_tilt * 0.5)
    hip_r_s = (hip_r[0], hip_r[1] - hip_tilt * 0.5)
    waist_l_s = (waist_l[0], waist_l[1] + hip_tilt * 0.25)
    waist_r_s = (waist_r[0], waist_r[1] - hip_tilt * 0.25)

    # --- DRAW GESTURE LINE ---
    if draw_gesture_line:
        ctx.set_source_rgba(*rgb_to_cairo(GESTURE_RED, 0.5))
        ctx.set_line_width(3.0)
        ctx.set_dash([12, 6])
        ctx.new_path()
        ctx.move_to(spine[0][0], spine[0][1])
        for pt in spine[1:]:
            ctx.line_to(pt[0], pt[1])
        ctx.stroke()
        ctx.set_dash([])

    # --- FEET ---
    foot_w = hr * 0.8
    foot_h = hr * 0.35
    wf_x = center_x + wf_offset
    cairo_ellipse(ctx, wf_x, ground_y - foot_h / 2, foot_w / 2, foot_h / 2,
                  SHOE_DARK, LINE_COLOR, lw)

    ff_offset = gp.get('free_foot_offset', -hr * 0.8)
    ff_lift = gp.get('free_foot_lift', 0)
    ff_x = center_x + ff_offset
    ff_w = foot_w * 0.85
    ff_h = foot_h * 0.8
    cairo_ellipse(ctx, ff_x, ground_y - ff_lift - ff_h / 2, ff_w / 2, ff_h / 2,
                  SHOE_DARK, LINE_COLOR, lw)

    # --- LEGS ---
    leg_w_top = hr * 0.55
    leg_w_bot = hr * 0.40

    # Weight-bearing leg (straighter)
    wl_top = (hip_r_s[0], hip_r_s[1]) if wf_offset >= 0 else (hip_l_s[0], hip_l_s[1])
    wl_bot = (wf_x, ground_y - foot_h)
    cairo_tapered_limb(ctx, wl_top, wl_bot, leg_w_top, leg_w_bot,
                       PANTS_SAGE, LINE_COLOR, lw, bend=0.03)

    # Free leg (bent at knee)
    fl_top = (hip_l_s[0], hip_l_s[1]) if wf_offset >= 0 else (hip_r_s[0], hip_r_s[1])
    fl_bot = (ff_x, ground_y - ff_lift - ff_h)
    knee_x = (fl_top[0] + fl_bot[0]) / 2 + gp.get('free_knee_offset_x', 0)
    knee_y = fl_top[1] + (fl_bot[1] - fl_top[1]) * 0.5
    # Upper free leg
    cairo_tapered_limb(ctx, fl_top, (knee_x, knee_y),
                       leg_w_top, leg_w_top * 0.85,
                       PANTS_SAGE, LINE_COLOR, lw, bend=-0.05)
    # Lower free leg
    cairo_tapered_limb(ctx, (knee_x, knee_y), fl_bot,
                       leg_w_top * 0.85, leg_w_bot * 0.9,
                       PANTS_SAGE, LINE_COLOR, lw, bend=0.04)

    # --- TORSO (hoodie) ---
    hoodie_flare = gp.get('hoodie_flare', 0)
    hoodie_bottom_l = (waist_l_s[0] - hr * 0.15 - hoodie_flare, waist_l_s[1] + hr * 0.1)
    hoodie_bottom_r = (waist_r_s[0] + hr * 0.15 + hoodie_flare, waist_r_s[1] + hr * 0.1)
    torso_anchors = [
        shoulder_l_s, shoulder_r_s,
        hoodie_bottom_r, hoodie_bottom_l,
    ]
    cairo_bezier_fill(ctx, torso_anchors, HOODIE_ORANGE, LINE_COLOR, lw, tension=0.25)

    # Pixel pattern hints on chest
    chest_pt = spine_point_at(spine, 0.35)
    for i, col in enumerate([PIXEL_CYAN, PIXEL_CYAN, (230, 80, 160)]):
        px_x = chest_pt[0] - 8 + i * 6
        px_y = chest_pt[1]
        r, g, b = col[0] / 255, col[1] / 255, col[2] / 255
        ctx.new_path()
        ctx.rectangle(px_x, px_y, 4, 4)
        ctx.set_source_rgba(r, g, b, 1.0)
        ctx.fill()

    # Hoodie pocket bump
    pocket_y = waist_l_s[1]
    pocket_cx = (waist_l_s[0] + waist_r_s[0]) / 2
    ctx.new_path()
    ctx.arc(pocket_cx, pocket_y, hr * 0.5, math.radians(200), math.radians(340))
    ctx.set_source_rgba(*rgb_to_cairo(LINE_COLOR))
    ctx.set_line_width(max(1, lw - 1))
    ctx.stroke()

    # --- ARMS (using v2 geometry-compute layer) ---
    sh_perp_l = spine_perpendicular_at(spine, 0.20)
    sh_perp_r = spine_perpendicular_at(spine, 0.20)
    arm_length = hr * 1.8

    left_geom = compute_arm_geometry(
        shoulder_l_s, sh_perp_l,
        arm_angle_deg=gp.get('left_arm_angle', -30),
        arm_length=arm_length, scale=hr / 60.0, side=-1,
        elbow_bend_factor=gp.get('left_arm_bend', 0.12),
    )
    render_arm_cairo(ctx, left_geom, HOODIE_ORANGE, LINE_COLOR, SKIN_MID,
                     lw=lw, clothing="hoodie")

    right_geom = compute_arm_geometry(
        shoulder_r_s, sh_perp_r,
        arm_angle_deg=gp.get('right_arm_angle', -150),
        arm_length=arm_length, scale=hr / 60.0, side=1,
        elbow_bend_factor=gp.get('right_arm_bend', 0.12),
    )
    render_arm_cairo(ctx, right_geom, HOODIE_ORANGE, LINE_COLOR, SKIN_MID,
                     lw=lw, clothing="hoodie")

    # --- HEAD ---
    neck_pt = landmarks["neck"]
    cairo_tapered_limb(ctx, (neck_pt[0], neck_pt[1]),
                       (head_center[0], head_center[1] + hr * 0.6),
                       hr * 0.5, hr * 0.7,
                       SKIN_MID, LINE_COLOR, max(1, lw - 1), bend=0)

    cairo_circle(ctx, head_center[0], head_center[1], hr,
                 SKIN_MID, LINE_COLOR, lw)

    # Eyes
    ew = int(hr * 0.22)
    eh = int(ew * 1.1)
    for side_m in [-1, 1]:
        ex = head_center[0] + side_m * hr * 0.35
        ey = head_center[1]
        # Sclera
        cairo_ellipse(ctx, ex, ey, ew, eh, (250, 240, 220), DEEP_COCOA, max(1, lw - 1))
        # Iris
        ir = ew * 0.6
        cairo_circle(ctx, ex, ey, ir, WARM_AMBER_IRIS, None, 0)
        # Pupil
        pr = ew * 0.3
        cairo_circle(ctx, ex, ey, pr, DEEP_COCOA, None, 0)
        # Highlight
        cairo_ellipse(ctx, ex - ew * 0.1, ey - ew * 0.25,
                      ew * 0.15, ew * 0.2, (240, 240, 240), None, 0)

    # Brows
    brow_y = head_center[1] - eh - hr * 0.18
    brow_w = hr * 0.30
    brow_thick = max(2, 2.5 * (hr / 60.0))
    for side_m in [-1, 1]:
        bx = head_center[0] + side_m * hr * 0.35
        ctx.new_path()
        ctx.move_to(bx - brow_w, brow_y + 2)
        ctx.line_to(bx, brow_y)
        ctx.line_to(bx + brow_w, brow_y + 2)
        ctx.set_source_rgba(*rgb_to_cairo(DEEP_COCOA))
        ctx.set_line_width(brow_thick)
        ctx.stroke()

    # Nose
    ctx.new_path()
    ctx.arc(head_center[0], head_center[1] + hr * 0.14,
            hr * 0.08, 0, math.pi)
    ctx.set_source_rgba(*rgb_to_cairo(LINE_COLOR))
    ctx.set_line_width(max(1, lw - 1))
    ctx.stroke()

    # Mouth
    m_y = head_center[1] + hr * 0.45
    ctx.new_path()
    ctx.arc(head_center[0], m_y, hr * 0.18,
            math.radians(20), math.radians(160))
    ctx.set_source_rgba(*rgb_to_cairo(LINE_COLOR))
    ctx.set_line_width(max(1, lw - 1))
    ctx.stroke()

    # --- HAIR ---
    hair_trail_dx = gp.get('hair_trail_dx', 0)
    hair_lift = gp.get('hair_lift', 0)
    hair_cx = head_center[0] + hair_trail_dx
    hair_top = head_center[1] - hr - hr * 0.85 - hair_lift
    hair_anchors = [
        (hair_cx - hr * 1.25, head_center[1] + hr * 0.1),
        (hair_cx - hr * 0.7, hair_top + hr * 0.3),
        (hair_cx + hair_trail_dx * 0.5, hair_top),
        (hair_cx + hr * 0.7, hair_top + hr * 0.25),
        (hair_cx + hr * 1.15, head_center[1] + hr * 0.1),
        (hair_cx + hr * 0.3, head_center[1] + hr * 0.4),
        (hair_cx - hr * 0.3, head_center[1] + hr * 0.4),
    ]
    cairo_bezier_fill(ctx, hair_anchors, HAIR_DARK, LINE_COLOR, lw, tension=0.35)

    # Curl indicators
    rng = random.Random(42)
    for i in range(5):
        cx_c = hair_cx + rng.randint(int(-hr * 0.7), int(hr * 0.6))
        cy_c = head_center[1] - hr - rng.randint(int(hr * 0.2), int(hr * 0.8))
        cr = rng.randint(int(hr * 0.15), int(hr * 0.30))
        ctx.new_path()
        start_a = rng.randint(0, 120)
        end_a = rng.randint(200, 340)
        ctx.arc(cx_c, cy_c, cr, math.radians(start_a), math.radians(end_a))
        ctx.set_source_rgba(60 / 255, 30 / 255, 15 / 255, 1.0)
        ctx.set_line_width(max(1, lw - 1))
        ctx.stroke()

    # Hoodie settle indicator
    if gp.get('show_hoodie_settle', False):
        ctx.set_source_rgba(*rgb_to_cairo(MOTION_ARROW, 0.7))
        ctx.set_line_width(2.0)
        ctx.set_dash([6, 4])
        hb_y = waist_l_s[1] + hr * 0.1
        hb_cx = (waist_l_s[0] + waist_r_s[0]) / 2
        hb_hw = abs(waist_r_s[0] - waist_l_s[0]) / 2 + hoodie_flare + 4
        ctx.new_path()
        ctx.arc(hb_cx, hb_y, hb_hw, math.radians(190), math.radians(350))
        ctx.stroke()
        ctx.set_dash([])

    # Anchor dots on gesture spine
    if draw_gesture_line:
        for frac, label in [(0.0, "H"), (0.20, "S"), (0.50, "W"), (0.60, "Hip"), (1.0, "F")]:
            pt = spine_point_at(spine, frac)
            cairo_circle(ctx, pt[0], pt[1], 3, ANCHOR_GREEN, None, 0)

    return {
        "head_center": head_center,
        "spine": spine,
        "shoulder_l": shoulder_l_s,
        "shoulder_r": shoulder_r_s,
        "hip_l": hip_l_s,
        "hip_r": hip_r_s,
        "waist_l": waist_l_s,
        "waist_r": waist_r_s,
        "left_hand": (left_geom.hand_x, left_geom.hand_y),
        "right_hand": (right_geom.hand_x, right_geom.hand_y),
        "ground_y": ground_y,
        "body_height": body_height,
    }


# ===================================================================
# Panel rendering (cairo figure + PIL annotation overlay)
# ===================================================================

def render_panel_figure(gesture_params, draw_gesture_line=True):
    """Render a single panel figure using canonical char_luma renderer.

    Returns (pil_img, positions_dict) where pil_img is PANEL_W x PANEL_H.
    Uses draw_luma_on_context() from LTG_TOOL_char_luma for character rendering.
    """
    rs = RENDER_SCALE
    rw = PANEL_W * rs
    rh = PANEL_H * rs

    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, rw, rh)
    ctx = cairo.Context(surface)

    # Background
    ctx.set_source_rgba(*rgb_to_cairo(ANNOTATION_BG))
    ctx.paint()

    hr = 32 * rs
    ground_y = rh - 60 * rs
    center_x = rw // 2
    char_h = int(hr * 2 / 0.37)  # from 37% head ratio

    # Map gesture_params to canonical expression
    expression = gesture_params.get('_expression', 'CURIOUS')
    pose_overrides = {}
    for k in ('hip_shift', 'shoulder_offset', 'head_offset', 'torso_lean'):
        if k in gesture_params:
            pose_overrides[k] = gesture_params[k]

    # Draw character using canonical renderer
    info = draw_luma_on_context(ctx, center_x, ground_y, char_h,
                                expression, pose=pose_overrides, scale=1.0)

    # Draw gesture line if requested (annotation overlay)
    if draw_gesture_line:
        ctx.set_source_rgba(*rgb_to_cairo(GESTURE_RED, 0.5))
        ctx.set_line_width(3.0)
        ctx.set_dash([12, 6])
        ctx.new_path()
        ctx.move_to(center_x, ground_y - char_h)
        ctx.line_to(center_x, ground_y)
        ctx.stroke()
        ctx.set_dash([])

    # Draw ground line
    ctx.set_source_rgba(*rgb_to_cairo(PANEL_BORDER, 0.5))
    ctx.set_line_width(2.0)
    ctx.new_path()
    ctx.move_to(20, ground_y)
    ctx.line_to(rw - 20, ground_y)
    ctx.stroke()

    # Convert to PIL and downscale
    pil = cairo_surface_to_pil(surface)
    pil = pil.resize((PANEL_W, PANEL_H), Image.LANCZOS)

    # Build approximate positions dict for annotations
    head_cy = (ground_y - char_h + hr) / rs
    positions = {
        'head_center': (center_x / rs, head_cy),
        'ground_y': ground_y / rs,
        'center_x': center_x / rs,
        'head_r': hr / rs,
        'spine': [(center_x / rs, (ground_y - char_h) / rs),
                  (center_x / rs, ground_y / rs)],
    }
    if isinstance(info, dict):
        for k, v in info.items():
            if isinstance(v, tuple) and len(v) == 2:
                positions[k] = v
            elif isinstance(v, (int, float)):
                positions[k] = v

    return pil, positions


# ===================================================================
# PIL annotation helpers
# ===================================================================

def get_font(size=11):
    try:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)
    except Exception:
        return ImageFont.load_default()


def get_font_bold(size=11):
    try:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size)
    except Exception:
        return ImageFont.load_default()


def draw_arrow(draw, x0, y0, x1, y1, color=MOTION_ARROW, width=2, head=8):
    draw.line([(x0, y0), (x1, y1)], fill=color, width=width)
    angle = math.atan2(y1 - y0, x1 - x0)
    for da in (-0.4, 0.4):
        ax = x1 - head * math.cos(angle + da)
        ay = y1 - head * math.sin(angle + da)
        draw.line([(x1, y1), (int(ax), int(ay))], fill=color, width=width)


def label_box(draw, x, y, text, bg=LABEL_BG, fg=LABEL_TEXT, font=None, pad=4):
    if font:
        bbox = draw.textbbox((0, 0), text, font=font)
    else:
        bbox = draw.textbbox((0, 0), text)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.rectangle([x, y, x + tw + pad * 2, y + th + pad * 2], fill=bg)
    draw.text((x + pad, y + pad), text, fill=fg, font=font)
    return tw + pad * 2, th + pad * 2


# ===================================================================
# Panel 0: IDLE / CURIOUS
# ===================================================================

def make_panel0():
    """Idle/Curious: forward-leaning C-curve, weight on front foot, head tilt."""
    gp = {
        '_expression': 'CURIOUS',
        'curve_amount': 0.06,
        'curve_direction': 'right',
        'curve_type': 'c',
        'head_offset_x': 8,
        'head_offset_y': 0,
        'weight_foot_offset': 10,
        'free_foot_offset': -18,
        'free_foot_lift': 4,
        'free_knee_offset_x': -6,
        'shoulder_rise_l': 4,
        'shoulder_rise_r': 8,
        'hip_tilt_px': 4,
        'left_arm_angle': -20,
        'right_arm_angle': -155,
        'left_arm_bend': 0.14,
        'right_arm_bend': 0.10,
        'hair_trail_dx': 0,
        'hair_lift': 0,
        'hoodie_flare': 0,
        'show_hoodie_settle': True,
    }
    return render_panel_figure(gp, draw_gesture_line=True)


# ===================================================================
# Panel 1: SPRINT ANTICIPATION
# ===================================================================

def make_panel1():
    """Sprint Anticipation: strong forward lean, arms back, wide stance."""
    gp = {
        '_expression': 'DETERMINED',
        'curve_amount': 0.10,
        'curve_direction': 'left',
        'curve_type': 'c',
        'head_offset_x': -20,
        'head_offset_y': 10,
        'weight_foot_offset': 14,
        'free_foot_offset': -22,
        'free_foot_lift': 0,
        'free_knee_offset_x': -8,
        'shoulder_rise_l': 2,
        'shoulder_rise_r': 2,
        'hip_tilt_px': 2,
        'left_arm_angle': -45,
        'right_arm_angle': -135,
        'left_arm_bend': 0.15,
        'right_arm_bend': 0.15,
        'hair_trail_dx': -8,
        'hair_lift': 4,
        'hoodie_flare': 0,
        'show_hoodie_settle': False,
    }
    return render_panel_figure(gp, draw_gesture_line=True)


# ===================================================================
# Panel 2: DISCOVERY REACTION (SURPRISED recoil)
# ===================================================================

def make_panel2():
    """Discovery Reaction / SURPRISED: backward C-curve, 70/30 weight back foot,
    asymmetric arms, off-balance recoil. Uses Lee's C50 gesture spec."""
    gp = {
        '_expression': 'SURPRISED',
        'curve_amount': 0.12,
        'curve_direction': 'left',
        'curve_type': 'c',
        'head_offset_x': -16,
        'head_offset_y': 4,
        'weight_foot_offset': 16,
        'free_foot_offset': -28,
        'free_foot_lift': 12,
        'free_knee_offset_x': -10,
        'shoulder_rise_l': 12,
        'shoulder_rise_r': 6,
        'hip_tilt_px': 8,
        'left_arm_angle': 30,
        'right_arm_angle': -120,
        'left_arm_bend': 0.18,
        'right_arm_bend': 0.10,
        'hair_trail_dx': 14,
        'hair_lift': 10,
        'hoodie_flare': 0,
        'show_hoodie_settle': False,
    }
    return render_panel_figure(gp, draw_gesture_line=True)


# ===================================================================
# Panel 3: LANDING / STOP
# ===================================================================

def make_panel3():
    """Landing/Stop: slight forward lean, hoodie and hair follow-through."""
    gp = {
        '_expression': 'CURIOUS',
        'curve_amount': 0.04,
        'curve_direction': 'right',
        'curve_type': 's',
        'head_offset_x': 4,
        'head_offset_y': 0,
        'weight_foot_offset': 8,
        'free_foot_offset': -12,
        'free_foot_lift': 0,
        'free_knee_offset_x': -4,
        'shoulder_rise_l': 3,
        'shoulder_rise_r': 5,
        'hip_tilt_px': 3,
        'left_arm_angle': -35,
        'right_arm_angle': -145,
        'left_arm_bend': 0.12,
        'right_arm_bend': 0.12,
        'hair_trail_dx': 16,
        'hair_lift': 0,
        'hoodie_flare': 8,
        'show_hoodie_settle': False,
    }
    return render_panel_figure(gp, draw_gesture_line=True)


# ===================================================================
# Compose full sheet
# ===================================================================

def main():
    img = Image.new("RGB", (W, H), color=(235, 228, 215))
    draw = ImageDraw.Draw(img)

    font = get_font(11)
    font_bold = get_font_bold(12)
    font_sm = get_font(9)

    # Title bar
    draw.rectangle([0, 0, W, PAD + 40], fill=LABEL_BG)
    draw.text((PAD, 8), "LUMA — Motion Spec Sheet v002 (Gesture-First)", fill=LABEL_TEXT, font=font_bold)
    draw.text((PAD, 22), "RYO HASEGAWA  |  Luma & the Glitchkin  |  C52  |  pycairo + curve_draw", fill=(180, 165, 140), font=font_sm)

    # Legend strip
    legend_x = W - 340
    draw.rectangle([legend_x - 6, 6, legend_x + 330, PAD + 36], fill=(70, 55, 42))
    draw.text((legend_x, 8), "--- Gesture spine", fill=GESTURE_RED, font=font_sm)
    draw.text((legend_x + 100, 8), "-> Secondary motion", fill=MOTION_ARROW, font=font_sm)
    draw.text((legend_x + 220, 8), "Timing beats", fill=BEAT_COLOR, font=font_sm)
    draw.text((legend_x, 22), "o Anchor points", fill=ANCHOR_GREEN, font=font_sm)
    draw.text((legend_x + 100, 22), "-- Ground/construction", fill=ACCENT_DASH, font=font_sm)

    # Generate panels
    panels = [make_panel0(), make_panel1(), make_panel2(), make_panel3()]

    panel_titles = [
        ("B1: IDLE / CURIOUS", "beat: 1-2-3-4 loop"),
        ("B2: SPRINT ANTICIPATION", "beat: 0-1 (2-frame hold)"),
        ("B3: DISCOVERY REACTION", "recoil beat | C-curve back"),
        ("B4: LANDING / STOP", "secondary: hoodie + hair lag"),
    ]

    for col in range(4):
        px, py = panel_origin(col)
        panel_img, pos = panels[col]

        # Paste cairo-rendered figure
        img.paste(panel_img, (px, py), panel_img)
        draw = ImageDraw.Draw(img)  # refresh after paste

        # Panel border
        draw.rectangle([px, py, px + PANEL_W, py + PANEL_H], outline=PANEL_BORDER, width=1)

        # Beat badge (top-left) — BEAT_COLOR fill for lint detection (>=15% non-bg)
        badge_text = f"B{col + 1}"
        bx, by = px + 3, py + 3
        draw.rectangle([bx, by, bx + 36, by + 22], fill=BEAT_COLOR)
        draw.text((bx + 4, by + 3), badge_text, fill=(240, 248, 255), font=font_bold)

        # Title strip at bottom
        draw.rectangle([px, py + PANEL_H - 32, px + PANEL_W, py + PANEL_H], fill=LABEL_BG)
        draw.text((px + 6, py + PANEL_H - 28), panel_titles[col][0], fill=LABEL_TEXT, font=font_bold)
        draw.text((px + 6, py + PANEL_H - 14), panel_titles[col][1], fill=(200, 190, 170), font=font_sm)

    # --- Per-panel annotations (PIL overlay) ---
    # Panel 0 annotations
    px0, py0 = panel_origin(0)
    pos0 = panels[0][1]
    draw.text((px0 + 8, py0 + 26), "TIMING", fill=LABEL_BG, font=font_bold)
    draw.text((px0 + 8, py0 + 38), "Body shift: beat 1", fill=BEAT_COLOR, font=font_sm)
    draw.text((px0 + 8, py0 + 49), "Head tilt: beat 1.5", fill=BEAT_COLOR, font=font_sm)
    draw.text((px0 + 8, py0 + 60), "Hoodie settle: beat 3", fill=MOTION_ARROW, font=font_sm)
    draw.text((px0 + 8, py0 + 71), "Return: beat 4 -> loop", fill=BEAT_COLOR, font=font_sm)
    draw.text((px0 + 8, py0 + PANEL_H - 72), "C-curve fwd lean", fill=GESTURE_RED, font=font_sm)
    draw.text((px0 + 8, py0 + PANEL_H - 60), "60/40 weight front", fill=MOTION_ARROW, font=font_sm)
    draw.text((px0 + 8, py0 + PANEL_H - 48), "hoodie hem: +2b lag", fill=MOTION_ARROW, font=font_sm)

    # Panel 1 annotations
    px1, py1 = panel_origin(1)
    draw.text((px1 + 8, py1 + 26), "TIMING", fill=LABEL_BG, font=font_bold)
    draw.text((px1 + 8, py1 + 38), "Beat 0: neutral", fill=BEAT_COLOR, font=font_sm)
    draw.text((px1 + 8, py1 + 49), "Beat 1: ANTICIPATION", fill=MOTION_ARROW, font=font_sm)
    draw.text((px1 + 8, py1 + 60), "  torso dips forward", fill=BEAT_COLOR, font=font_sm)
    draw.text((px1 + 8, py1 + 71), "  arms back (load)", fill=BEAT_COLOR, font=font_sm)
    draw.text((px1 + 8, py1 + 82), "Beat 2: LAUNCH", fill=(220, 60, 20), font=font_sm)
    draw.text((px1 + 8, py1 + PANEL_H - 72), "C-curve fwd lean 10deg", fill=GESTURE_RED, font=font_sm)
    draw.text((px1 + 8, py1 + PANEL_H - 60), "hair: -12deg pre-lean", fill=MOTION_ARROW, font=font_sm)
    draw.text((px1 + 8, py1 + PANEL_H - 48), "wide stance (1.15x)", fill=BEAT_COLOR, font=font_sm)

    # Panel 2 annotations
    px2, py2 = panel_origin(2)
    draw.text((px2 + 8, py2 + 26), "TIMING", fill=LABEL_BG, font=font_bold)
    draw.text((px2 + 8, py2 + 38), "Beat A: recoil (1 frame)", fill=MOTION_ARROW, font=font_sm)
    draw.text((px2 + 8, py2 + 49), "Beat B: lean-in recovery", fill=BEAT_COLOR, font=font_sm)
    draw.text((px2 + 8, py2 + 60), "hair lags +1.0 beat", fill=MOTION_ARROW, font=font_sm)
    draw.text((px2 + 8, py2 + PANEL_H - 84), "GESTURE-FIRST RECOIL:", fill=GESTURE_RED, font=font_sm)
    draw.text((px2 + 8, py2 + PANEL_H - 72), "Backward C-curve", fill=GESTURE_RED, font=font_sm)
    draw.text((px2 + 8, py2 + PANEL_H - 60), "70/30 weight back foot", fill=MOTION_ARROW, font=font_sm)
    draw.text((px2 + 8, py2 + PANEL_H - 48), "Front foot LIFTED", fill=MOTION_ARROW, font=font_sm)

    # Panel 3 annotations
    px3, py3 = panel_origin(3)
    draw.text((px3 + 8, py3 + 26), "TIMING", fill=LABEL_BG, font=font_bold)
    draw.text((px3 + 8, py3 + 38), "Beat 1: body STOPS", fill=BEAT_COLOR, font=font_sm)
    draw.text((px3 + 8, py3 + 49), "Beat 1.5: hoodie peaks", fill=MOTION_ARROW, font=font_sm)
    draw.text((px3 + 8, py3 + 60), "  at +8px flare", fill=MOTION_ARROW, font=font_sm)
    draw.text((px3 + 8, py3 + 71), "Beat 2: hair peaks fwd", fill=MOTION_ARROW, font=font_sm)
    draw.text((px3 + 8, py3 + 82), "Beat 3: hoodie settles", fill=BEAT_COLOR, font=font_sm)
    draw.text((px3 + 8, py3 + 93), "Beat 4: hair settles", fill=BEAT_COLOR, font=font_sm)
    draw.text((px3 + 8, py3 + PANEL_H - 72), "S-curve subtle lean", fill=GESTURE_RED, font=font_sm)
    draw.text((px3 + 8, py3 + PANEL_H - 60), "hair: +16px fwd trail", fill=MOTION_ARROW, font=font_sm)
    draw.text((px3 + 8, py3 + PANEL_H - 48), "hoodie: +8px flare", fill=MOTION_ARROW, font=font_sm)

    # Ground lines for each panel
    for col in range(4):
        px_c, py_c = panel_origin(col)
        pos = panels[col][1]
        gy = py_c + int(pos['ground_y'])
        draw.line([(px_c + 8, gy), (px_c + PANEL_W - 8, gy)],
                  fill=ACCENT_DASH, width=1)
        draw.text((px_c + 10, gy + 2), "GROUND", fill=ACCENT_DASH, font=font_sm)

    # Enforce <= 1280px
    img.thumbnail((1280, 1280), Image.LANCZOS)

    out_path = os.path.join(_OUTPUT_DIR, "LTG_CHAR_luma_motion.png")
    img.save(out_path)
    print(f"Saved: {out_path} ({img.width}x{img.height}px)")
    return out_path


if __name__ == "__main__":
    main()
