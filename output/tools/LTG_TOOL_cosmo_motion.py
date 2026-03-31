# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_cosmo_motion.py
Ryo Hasegawa / Cycle 53 — Full rebuild with pycairo + gesture-first construction

Motion Spec Sheet — COSMO
4 panels: Idle/Observing | Startled | Analysis Lean | Reluctant Move
Output: output/characters/motion/LTG_CHAR_cosmo_motion.png
Canvas: 1280x720 (within limit)

C53 REBUILD: All figures now use gesture_spine() + body_from_spine() from curve_draw.
Rendering via pycairo for anti-aliased bezier curves. Composited to PIL for annotations.
Lee's gesture spec (cosmo_gesture_spec_c52.md) drives all pose construction.

Cosmo motion vocabulary:
  - Upright, contained, deliberate. Angular joints (not smooth S-curves).
  - Arms hang close to body; notebook under left arm is a secondary-mass anchor.
  - Startled: glasses tilt peaks to 14°, BOTH arms jut briefly, then snap back.
  - Analysis lean: forward tilt 6-8° only; head tilts right; notebook out or open.
  - Reluctant move: body rigid, leans 10-12°, arm NOT pumping — notebook clutched.
  - Notebook secondary motion: lags body on all sudden shifts (+1.5 beat behind).
  - Glasses: neutral 7° CCW; Startled peak: 13-15°; Recovery to 9° by beat 3.
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

# Import curve_draw library
from LTG_TOOL_curve_draw import (
    gesture_spine, spine_point_at, spine_tangent_at, spine_perpendicular_at,
    body_from_spine, smooth_path,
)

# Import cairo primitives
from LTG_TOOL_cairo_primitives import (
    create_surface, to_pil_image, to_pil_rgba, set_color,
    draw_ellipse as cairo_prim_ellipse, draw_smooth_polygon,
    draw_tapered_stroke,
)

# --- RNG seed for reproducibility ---
random.seed(53)
np.random.seed(53)

# --- Load HEADER_H from sheet geometry config ---
_CONFIG_PATH = os.path.join(_TOOL_DIR, "sheet_geometry_config.json")


def _load_header_h(family="cosmo", default=54):
    try:
        with open(_CONFIG_PATH) as f:
            cfg = json.load(f)
        geo = cfg.get("families", {}).get(family, {})
        return geo.get("panel_top_abs", default)
    except Exception:
        return default


_COSMO_PANEL_TOP = _load_header_h("cosmo", default=54)

# --- CANONICAL COLORS (from char_cosmo.py / master_palette.md) ---
SKIN            = (217, 192, 154)   # Cosmo Skin Base
SKIN_SH         = (184, 154, 120)   # Cosmo Skin Shadow
SKIN_HL         = (238, 212, 176)   # Cosmo Skin Highlight
HAIR            = ( 26,  24,  36)   # Blue-Black
HAIR_SH         = ( 14,  14,  24)
GLASS_FRAME     = ( 92,  58,  32)   # Warm Espresso Brown
GLASS_LENS      = (238, 244, 255)   # Ghost Blue
GLASS_GLARE     = (240, 240, 240)
IRIS            = ( 61, 107,  69)   # Warm Forest Green
PUPIL           = ( 59,  40,  32)   # Deep Cocoa
EYE_W           = (250, 240, 220)   # Warm Cream
EYE_HL          = (240, 240, 240)
STRIPE_A        = ( 91, 141, 184)   # Cerulean Blue
STRIPE_B        = (122, 158, 126)   # Sage Green
PANTS           = (140, 136, 128)   # Warm Mid-Gray
PANTS_SH        = (106, 100,  96)
SHOE            = ( 92,  58,  32)   # Warm Espresso
NOTEBOOK        = ( 91, 141, 184)   # Cerulean Blue
NOTEBOOK_SH     = ( 61, 107, 138)   # Deep Cerulean
LINE_COLOR      = ( 59,  40,  32)   # Deep Cocoa
TAPE_COL        = (250, 240, 220)   # glasses bridge tape
BLUSH           = (210, 128,  80)
ANNOTATION_BG   = (248, 244, 238)   # warm cream panel bg
PANEL_BORDER    = (180, 165, 145)
LABEL_BG        = ( 50,  38,  28)
LABEL_TEXT      = (248, 244, 236)
MOTION_ARROW    = (220,  60,  20)   # orange — secondary motion
BEAT_COLOR      = ( 80, 120, 200)   # blue — timing beats
ACCENT_DASH     = (200, 190, 175)   # construction lines
GESTURE_RED     = (220,  50,  40)
ANCHOR_GREEN    = ( 60, 180,  80)

# --- CANVAS ---
W, H = 1280, 720
COLS, ROWS = 4, 1
PAD = 14
_TITLE_H = max(_COSMO_PANEL_TOP - PAD, 40)
PANEL_W = (W - PAD * (COLS + 1)) // COLS
PANEL_H = H - PAD * 2 - _TITLE_H

# Render scale for AA
RENDER_SCALE = 2


def panel_origin(col):
    """Top-left (x, y) of panel col (0-based)."""
    x = PAD + col * (PANEL_W + PAD)
    y = _COSMO_PANEL_TOP
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


def cairo_rounded_rect(ctx, x, y, w, h, cr, fill_rgb, outline_rgb=None, line_w=2.0):
    """Draw a rectangle with rounded corners."""
    r, g, b = fill_rgb[0] / 255, fill_rgb[1] / 255, fill_rgb[2] / 255
    ctx.new_path()
    ctx.move_to(x + cr, y)
    ctx.line_to(x + w - cr, y)
    ctx.arc(x + w - cr, y + cr, cr, -math.pi / 2, 0)
    ctx.line_to(x + w, y + h - cr)
    ctx.arc(x + w - cr, y + h - cr, cr, 0, math.pi / 2)
    ctx.line_to(x + cr, y + h)
    ctx.arc(x + cr, y + h - cr, cr, math.pi / 2, math.pi)
    ctx.line_to(x, y + cr)
    ctx.arc(x + cr, y + cr, cr, math.pi, 3 * math.pi / 2)
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


def cairo_surface_to_pil(surface):
    w = surface.get_width()
    h = surface.get_height()
    data = surface.get_data()
    arr = np.frombuffer(data, dtype=np.uint8).reshape((h, w, 4)).copy()
    arr_rgba = np.zeros_like(arr)
    arr_rgba[:, :, 0] = arr[:, :, 2]  # BGRA -> RGBA
    arr_rgba[:, :, 1] = arr[:, :, 1]
    arr_rgba[:, :, 2] = arr[:, :, 0]
    arr_rgba[:, :, 3] = arr[:, :, 3]
    return Image.fromarray(arr_rgba, "RGBA")


# ===================================================================
# Arm geometry (v2, from Luma C52 pattern)
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
    scale=1.0, side=1, elbow_bend_factor=0.10, two_segment=True,
):
    """Compute arm geometry from a gesture spine shoulder point.
    Cosmo: elbow_bend_factor=0.10 (contained, less bend than Luma).
    """
    sx, sy = spine_shoulder_pt
    angle_rad = math.radians(arm_angle_deg)

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

    hand_x = shifted_sx + arm_dx
    hand_y = shifted_sy + arm_dy

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

    deltoid_r = max(2, int(4 * scale + 0.5))
    bump_offset = deltoid_r * 0.6
    deltoid_cx = shifted_sx + math.cos(angle_rad) * bump_offset * side
    deltoid_cy = shifted_sy - math.sin(angle_rad) * bump_offset

    # Cosmo: slightly narrower arms (contained)
    base_w = arm_length * 0.20
    upper_w1 = base_w * 1.15
    upper_w2 = base_w * 0.82
    lower_w1 = base_w * 0.82
    lower_w2 = base_w * 0.60

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
                     two_segment=True, hand_r=None):
    """Render an arm from ArmGeometry using cairo. Cosmo = fitted shirt style."""
    if hand_r is None:
        hand_r = max(3, geom.lower_w2 * 0.8)

    # Deltoid bump — fitted shirt: small circle (rounded corner per image-rules.md)
    dr = geom.deltoid_r
    cairo_circle(ctx, geom.deltoid_cx, geom.deltoid_cy, dr,
                 fill_rgb, outline_rgb, max(1, lw - 1))

    if two_segment:
        cairo_tapered_limb(ctx,
                           (geom.shoulder_x, geom.shoulder_y),
                           (geom.elbow_x, geom.elbow_y),
                           geom.upper_w1, geom.upper_w2,
                           fill_rgb, outline_rgb, lw, bend=0.03)
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
                           fill_rgb, outline_rgb, lw, bend=0.04)

    # Hand
    cairo_circle(ctx, geom.hand_x, geom.hand_y, hand_r,
                 skin_rgb, outline_rgb, max(1, lw - 1))


# ===================================================================
# Cosmo-specific drawing elements (cairo)
# ===================================================================

def draw_stripe_shirt_cairo(ctx, cx, top_y, bot_y, half_w, hr, lw=3.0):
    """Draw Cosmo's horizontal cerulean/sage striped shirt."""
    stripe_h = max(5 * (hr / 32.0), 4)
    y = top_y
    ci = 0
    cols = [STRIPE_A, STRIPE_B]
    while y < bot_y:
        end_y = min(y + stripe_h, bot_y)
        r, g, b = cols[ci % 2]
        ctx.new_path()
        ctx.rectangle(cx - half_w, y, half_w * 2, end_y - y)
        ctx.set_source_rgba(r / 255, g / 255, b / 255, 1.0)
        ctx.fill()
        ci += 1
        y = end_y


def draw_glasses_cairo(ctx, gx, gy, hr, tilt_deg=7, lw=3.0):
    """Draw Cosmo's glasses at given center, tilted tilt_deg CCW. Cairo version."""
    lens_rx = hr * 0.38
    lens_ry = hr * 0.28
    sep = hr * 0.76
    rad = math.radians(tilt_deg)

    for side in [-1, 1]:
        lx = gx + side * sep / 2 + side * sep / 2 * math.sin(rad) * 0.2
        ly = gy + side * (sep / 2) * math.sin(rad) * 0.35

        # Lens fill + frame
        cairo_ellipse(ctx, lx, ly, lens_rx, lens_ry, GLASS_LENS, GLASS_FRAME, max(3, lw))
        # Glare crescent
        ctx.new_path()
        ctx.save()
        ctx.translate(lx, ly)
        ctx.scale(lens_rx - 2, lens_ry - 2)
        ctx.arc(0, 0, 1.0, math.radians(200), math.radians(340))
        ctx.restore()
        ctx.set_source_rgba(*rgb_to_cairo(GLASS_GLARE))
        ctx.set_line_width(max(2, lw * 0.6))
        ctx.stroke()

        # Eye behind glass
        ir = lens_rx * 0.50
        cairo_ellipse(ctx, lx, ly, ir, min(ir, lens_ry - 2), IRIS, None, 0)
        # Pupil
        pr = ir * 0.55
        cairo_circle(ctx, lx, ly, pr, PUPIL, None, 0)
        # Upper-right highlight
        hl_r = max(2, ir * 0.25)
        cairo_circle(ctx, lx + ir * 0.15, ly - lens_ry * 0.35, hl_r, EYE_HL, None, 0)

    # Nose bridge
    bridge_x0 = gx - sep / 2 + lens_rx - 2
    bridge_x1 = gx + sep / 2 - lens_rx + 2
    cairo_stroke_line(ctx, (bridge_x0, gy), (bridge_x1, gy), GLASS_FRAME, max(3, lw * 0.8))

    # Bridge tape (Cosmo visual hook)
    tape_cx = (bridge_x0 + bridge_x1) / 2
    tape_w = (bridge_x1 - bridge_x0) * 0.4
    tape_h = hr * 0.08
    ctx.new_path()
    ctx.rectangle(tape_cx - tape_w / 2, gy - tape_h, tape_w, tape_h * 2)
    ctx.set_source_rgba(*rgb_to_cairo(TAPE_COL))
    ctx.fill()

    # Temple arms
    for side in [-1, 1]:
        lx = gx + side * sep / 2 + side * sep / 2 * math.sin(rad) * 0.2
        arm_start_x = lx + side * lens_rx
        arm_end_x = arm_start_x + side * hr * 0.40
        arm_end_y = gy - hr * 0.08
        cairo_stroke_line(ctx, (arm_start_x, gy), (arm_end_x, arm_end_y),
                          GLASS_FRAME, max(3, lw * 0.8))


def draw_notebook_cairo(ctx, nb_cx, nb_cy, hr, lw=3.0, open_book=False):
    """Draw Cosmo's notebook as a small rectangle prop."""
    nb_w = hr * 0.36
    nb_h = hr * 0.56
    if open_book:
        nb_w *= 1.4
        nb_h *= 1.1

    # Main body
    cairo_rounded_rect(ctx, nb_cx - nb_w, nb_cy - nb_h / 2,
                       nb_w * 2, nb_h, hr * 0.04,
                       NOTEBOOK, LINE_COLOR, lw)
    # Spine (darker left edge)
    ctx.new_path()
    ctx.rectangle(nb_cx - nb_w, nb_cy - nb_h / 2, nb_w * 0.15, nb_h)
    ctx.set_source_rgba(*rgb_to_cairo(NOTEBOOK_SH))
    ctx.fill()
    # Page edge
    cairo_stroke_line(ctx, (nb_cx + nb_w - 2, nb_cy - nb_h / 2 + 3),
                      (nb_cx + nb_w - 2, nb_cy + nb_h / 2 - 3),
                      EYE_W, max(1, lw * 0.5))

    return nb_w, nb_h


# ===================================================================
# Gesture-first figure drawing — COSMO
# ===================================================================

def draw_gesture_cosmo(ctx, panel_w, panel_h, ground_y, center_x, hr,
                       gesture_params, lw=4.0, draw_gesture_line=True):
    """Draw Cosmo using gesture-first construction via pycairo.

    Cosmo differences from Luma:
    - ANGULAR body: rectangular torso with stripe shirt, not smooth bezier torso
    - Glasses on face, tilt tracks head * 0.4
    - Notebook prop attached to one arm
    - Shorter hair (flat cap + cowlick)
    - 4.0 heads tall (vs Luma's 3.2)

    Args:
        ctx: cairo Context (at render scale)
        panel_w, panel_h: panel dimensions at render scale
        ground_y: Y position of ground line at render scale
        center_x: horizontal center at render scale
        hr: head radius at render scale
        gesture_params: dict with keys:
            curve_amount, curve_direction, curve_type,
            head_offset_x, head_offset_y,
            weight_foot_offset, free_foot_offset, free_foot_lift,
            shoulder_rise_l, shoulder_rise_r,
            hip_tilt_px,
            left_arm_angle, right_arm_angle,
            left_arm_bend, right_arm_bend,
            glasses_tilt, head_tilt_deg,
            notebook_side ('left'|'right'), notebook_open (bool),
            body_lean_deg, cowlick_scale
        lw: line width
        draw_gesture_line: if True, draw the red dashed gesture spine
    Returns:
        dict with key positions for annotation placement
    """
    gp = gesture_params
    # Cosmo is 4.0 heads tall
    body_height = hr * 2 / 0.28  # head_r is ~28% of total height for 4-head character

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
        curve_amount=gp.get('curve_amount', 0.03),
        curve_direction=gp.get('curve_direction', 'right'),
        curve_type=gp.get('curve_type', 's'),
        num_points=40,
    )

    # Body landmarks from spine — Cosmo is narrower/more angular
    shoulder_width = hr * 1.8
    waist_width = hr * 1.3
    hip_width = hr * 1.4
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
    shoulder_l_s = (shoulder_l[0] - hr * 0.02, shoulder_l[1] - sr_l)
    shoulder_r_s = (shoulder_r[0] + hr * 0.02, shoulder_r[1] - sr_r)

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
    foot_w = hr * 0.72
    foot_h = hr * 0.28
    wf_x = center_x + wf_offset
    cairo_ellipse(ctx, wf_x, ground_y - foot_h / 2, foot_w / 2, foot_h / 2,
                  SHOE, LINE_COLOR, lw)

    ff_offset = gp.get('free_foot_offset', -hr * 0.7)
    ff_lift = gp.get('free_foot_lift', 0)
    ff_x = center_x + ff_offset
    ff_w = foot_w * 0.90
    ff_h = foot_h * 0.85
    cairo_ellipse(ctx, ff_x, ground_y - ff_lift - ff_h / 2, ff_w / 2, ff_h / 2,
                  SHOE, LINE_COLOR, lw)

    # --- LEGS (rectangular — Cosmo's angular style) ---
    leg_w_top = hr * 0.50
    leg_w_bot = hr * 0.38

    wl_top = (hip_r_s[0], hip_r_s[1]) if wf_offset >= 0 else (hip_l_s[0], hip_l_s[1])
    wl_bot = (wf_x, ground_y - foot_h)
    cairo_tapered_limb(ctx, wl_top, wl_bot, leg_w_top, leg_w_bot,
                       PANTS, LINE_COLOR, lw, bend=0.02)

    fl_top = (hip_l_s[0], hip_l_s[1]) if wf_offset >= 0 else (hip_r_s[0], hip_r_s[1])
    fl_bot = (ff_x, ground_y - ff_lift - ff_h)
    knee_x = (fl_top[0] + fl_bot[0]) / 2 + gp.get('free_knee_offset_x', 0)
    knee_y = fl_top[1] + (fl_bot[1] - fl_top[1]) * 0.5
    cairo_tapered_limb(ctx, fl_top, (knee_x, knee_y),
                       leg_w_top, leg_w_top * 0.88,
                       PANTS, LINE_COLOR, lw, bend=-0.04)
    cairo_tapered_limb(ctx, (knee_x, knee_y), fl_bot,
                       leg_w_top * 0.88, leg_w_bot * 0.92,
                       PANTS, LINE_COLOR, lw, bend=0.03)

    # Belt (thin dark strip at waist/hip junction)
    belt_y = (waist_l_s[1] + hip_l_s[1]) / 2
    belt_hw = abs(waist_r_s[0] - waist_l_s[0]) / 2
    belt_cx = (waist_l_s[0] + waist_r_s[0]) / 2
    belt_h = hr * 0.08
    ctx.new_path()
    ctx.rectangle(belt_cx - belt_hw, belt_y - belt_h / 2, belt_hw * 2, belt_h)
    ctx.set_source_rgba(*rgb_to_cairo(GLASS_FRAME))
    ctx.fill_preserve()
    ctx.set_source_rgba(*rgb_to_cairo(LINE_COLOR))
    ctx.set_line_width(max(1, lw * 0.5))
    ctx.stroke()

    # --- TORSO (striped shirt — ANGULAR, not smooth bezier) ---
    torso_hw = abs(shoulder_r_s[0] - shoulder_l_s[0]) / 2
    torso_cx = (shoulder_l_s[0] + shoulder_r_s[0]) / 2
    torso_top = min(shoulder_l_s[1], shoulder_r_s[1])
    torso_bot = belt_y - belt_h / 2

    # Draw stripes first, then outline
    draw_stripe_shirt_cairo(ctx, torso_cx, torso_top, torso_bot, torso_hw, hr, lw)

    # Torso outline (angular — straight lines, not bezier)
    torso_pts = [
        shoulder_l_s, shoulder_r_s,
        (waist_r_s[0], torso_bot), (waist_l_s[0], torso_bot),
    ]
    cairo_fill_path(ctx, torso_pts, STRIPE_A, LINE_COLOR, lw)
    # Re-draw stripes ON TOP of outline fill (outline fill is just for the border)
    draw_stripe_shirt_cairo(ctx, torso_cx, torso_top + lw, torso_bot - lw,
                            torso_hw - lw, hr, lw)

    # --- ARMS ---
    sh_perp_l = spine_perpendicular_at(spine, 0.20)
    sh_perp_r = spine_perpendicular_at(spine, 0.20)
    arm_length = hr * 1.8

    left_geom = compute_arm_geometry(
        shoulder_l_s, sh_perp_l,
        arm_angle_deg=gp.get('left_arm_angle', -25),
        arm_length=arm_length, scale=hr / 60.0, side=-1,
        elbow_bend_factor=gp.get('left_arm_bend', 0.10),
    )
    render_arm_cairo(ctx, left_geom, STRIPE_A, LINE_COLOR, SKIN, lw=lw)

    right_geom = compute_arm_geometry(
        shoulder_r_s, sh_perp_r,
        arm_angle_deg=gp.get('right_arm_angle', -155),
        arm_length=arm_length, scale=hr / 60.0, side=1,
        elbow_bend_factor=gp.get('right_arm_bend', 0.10),
    )
    render_arm_cairo(ctx, right_geom, STRIPE_A, LINE_COLOR, SKIN, lw=lw)

    # --- NOTEBOOK (on specified arm side) ---
    nb_side = gp.get('notebook_side', 'left')
    nb_open = gp.get('notebook_open', False)
    nb_geom = left_geom if nb_side == 'left' else right_geom
    nb_cx = nb_geom.hand_x + (hr * 0.2 if nb_side == 'left' else -hr * 0.2)
    nb_cy = nb_geom.hand_y - hr * 0.1
    nb_w, nb_h = draw_notebook_cairo(ctx, nb_cx, nb_cy, hr, lw, open_book=nb_open)

    # --- NECK ---
    neck_pt = landmarks["neck"]
    cairo_tapered_limb(ctx, (neck_pt[0], neck_pt[1]),
                       (head_center[0], head_center[1] + hr * 0.55),
                       hr * 0.40, hr * 0.55,
                       SKIN, LINE_COLOR, max(1, lw - 1), bend=0)

    # --- HEAD (rectangular with rounded corners — Cosmo DNA) ---
    hw = hr * 0.86  # head half-width
    cr = hr * 0.12  # corner radius
    head_top = head_center[1] - hr
    head_bot = head_center[1] + hr
    cairo_rounded_rect(ctx, head_center[0] - hw, head_top,
                       hw * 2, hr * 2, cr,
                       SKIN, LINE_COLOR, lw)

    # --- HAIR (flat cap + amplified cowlick) ---
    hair_top = head_top - hr * 0.12
    hair_lx = head_center[0] - hw + hr * 0.06
    hair_rx = head_center[0] + hw - hr * 0.06
    hair_h = head_top - hair_top + hr * 0.08
    ctx.new_path()
    ctx.rectangle(hair_lx, hair_top, hair_rx - hair_lx, hair_h)
    ctx.set_source_rgba(*rgb_to_cairo(HAIR))
    ctx.fill()

    # Cowlick (amplified — 0.15 heads, Cosmo visual hook)
    cowlick_s = gp.get('cowlick_scale', 1.0)
    cwk_cx = head_center[0] + hw * 0.55
    cwk_cy = hair_top - hr * 0.04 * cowlick_s
    cwk_rx = hr * 0.22 * cowlick_s
    cwk_ry = hr * 0.12 * cowlick_s
    cairo_ellipse(ctx, cwk_cx, cwk_cy, cwk_rx, cwk_ry, HAIR, None, 0)

    # --- FACE FEATURES ---
    face_cy = head_center[1] + hr * 0.05
    head_tilt_deg = gp.get('head_tilt_deg', 0)

    # Brows (analytical, horizontal-ish)
    brow_y = face_cy - hr * 0.42
    brow_sep = hw * 0.52
    brow_w = hr * 0.22
    brow_thick = max(2, 2.5 * (hr / 60.0))
    for side_m in [-1, 1]:
        bx = head_center[0] + side_m * brow_sep
        tilt_offset = side_m * math.sin(math.radians(head_tilt_deg)) * 3
        ctx.new_path()
        ctx.move_to(bx - brow_w, brow_y + tilt_offset + 2)
        ctx.line_to(bx, brow_y + tilt_offset)
        ctx.line_to(bx + brow_w, brow_y + tilt_offset + 2)
        ctx.set_source_rgba(*rgb_to_cairo(HAIR))
        ctx.set_line_width(brow_thick)
        ctx.stroke()

    # Nose
    ctx.new_path()
    ctx.arc(head_center[0], face_cy + hr * 0.14, hr * 0.08, 0, math.pi)
    ctx.set_source_rgba(*rgb_to_cairo(LINE_COLOR))
    ctx.set_line_width(max(1, lw - 1))
    ctx.stroke()

    # Mouth
    mouth_y = face_cy + hr * 0.45
    mouth_spec = gp.get('mouth', 'neutral')
    if mouth_spec == 'grimace':
        ctx.new_path()
        ctx.move_to(head_center[0] - hr * 0.15, mouth_y)
        ctx.line_to(head_center[0], mouth_y + hr * 0.04)
        ctx.line_to(head_center[0] + hr * 0.15, mouth_y)
        ctx.set_source_rgba(*rgb_to_cairo(LINE_COLOR))
        ctx.set_line_width(max(1, lw - 1))
        ctx.stroke()
    elif mouth_spec == 'open':
        cairo_ellipse(ctx, head_center[0], mouth_y, hr * 0.12, hr * 0.08,
                      (80, 50, 40), LINE_COLOR, max(1, lw - 1))
    elif mouth_spec == 'compressed':
        cairo_stroke_line(ctx, (head_center[0] - hr * 0.14, mouth_y),
                          (head_center[0] + hr * 0.14, mouth_y),
                          LINE_COLOR, max(2, lw - 1))
    else:
        ctx.new_path()
        ctx.arc(head_center[0], mouth_y, hr * 0.15,
                math.radians(15), math.radians(165))
        ctx.set_source_rgba(*rgb_to_cairo(LINE_COLOR))
        ctx.set_line_width(max(1, lw - 1))
        ctx.stroke()

    # Blush (if specified)
    if gp.get('blush', False):
        for side_m in [-1, 1]:
            blush_cx = head_center[0] + side_m * hw * 0.55
            blush_cy = face_cy + hr * 0.22
            cairo_ellipse(ctx, blush_cx, blush_cy, hr * 0.12, hr * 0.07,
                          BLUSH, None, 0)

    # Glasses (drawn OVER eyes — Cosmo's defining feature)
    glasses_tilt = gp.get('glasses_tilt', 7)
    draw_glasses_cairo(ctx, head_center[0], face_cy - hr * 0.08, hr,
                       tilt_deg=glasses_tilt, lw=lw)

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
        "nb_cx": nb_cx,
        "nb_cy": nb_cy,
        "nb_h": nb_h,
    }


# ===================================================================
# Panel rendering (cairo figure + PIL annotation overlay)
# ===================================================================

def render_panel_figure(gesture_params, draw_gesture_line=True):
    """Render a single panel figure with cairo, return as PIL RGBA."""
    rs = RENDER_SCALE
    rw = PANEL_W * rs
    rh = PANEL_H * rs

    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, rw, rh)
    ctx = cairo.Context(surface)

    # Background
    ctx.set_source_rgba(*rgb_to_cairo(ANNOTATION_BG))
    ctx.paint()

    hr = 28 * rs  # head radius at render scale (Cosmo is taller — smaller head ratio)
    ground_y = rh - 55 * rs
    center_x = rw // 2

    lw = 3.0 * rs

    positions = draw_gesture_cosmo(
        ctx, rw, rh, ground_y, center_x, hr,
        gesture_params, lw=lw, draw_gesture_line=draw_gesture_line,
    )

    # Convert to PIL and downscale
    pil = cairo_surface_to_pil(surface)
    pil = pil.resize((PANEL_W, PANEL_H), Image.LANCZOS)

    # Scale positions back
    scaled_pos = {}
    for k, v in positions.items():
        if k == "spine":
            scaled_pos[k] = [(x / rs, y / rs) for x, y in v]
        elif isinstance(v, tuple) and len(v) == 2:
            scaled_pos[k] = (v[0] / rs, v[1] / rs)
        else:
            scaled_pos[k] = v / rs if isinstance(v, (int, float)) else v
    return pil, scaled_pos


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
# Panel 0: IDLE / OBSERVING
# ===================================================================

def make_panel0():
    """Idle/Observing: upright, contained, slight lean. Notebook tucked, glasses 7deg."""
    gp = {
        'curve_amount': 0.03,
        'curve_direction': 'right',
        'curve_type': 's',
        'head_offset_x': 5,
        'head_offset_y': 0,
        'weight_foot_offset': 8,
        'free_foot_offset': -14,
        'free_foot_lift': 0,
        'free_knee_offset_x': -4,
        'shoulder_rise_l': 2,
        'shoulder_rise_r': 4,
        'hip_tilt_px': 2,
        'left_arm_angle': -20,
        'right_arm_angle': -160,
        'left_arm_bend': 0.10,
        'right_arm_bend': 0.08,
        'glasses_tilt': 7,
        'head_tilt_deg': 3,
        'notebook_side': 'left',
        'notebook_open': False,
        'mouth': 'neutral',
        'blush': False,
        'cowlick_scale': 1.0,
    }
    return render_panel_figure(gp, draw_gesture_line=True)


# ===================================================================
# Panel 1: STARTLED
# ===================================================================

def make_panel1():
    """Startled: glasses peak 14deg, arms jut, backward lean, notebook jostled."""
    gp = {
        'curve_amount': 0.08,
        'curve_direction': 'left',
        'curve_type': 'c',
        'head_offset_x': -12,
        'head_offset_y': 6,
        'weight_foot_offset': 12,
        'free_foot_offset': -18,
        'free_foot_lift': 6,
        'free_knee_offset_x': -8,
        'shoulder_rise_l': 10,
        'shoulder_rise_r': 10,
        'hip_tilt_px': 0,
        'left_arm_angle': -40,
        'right_arm_angle': -140,
        'left_arm_bend': 0.16,
        'right_arm_bend': 0.14,
        'glasses_tilt': 14,
        'head_tilt_deg': -4,
        'notebook_side': 'left',
        'notebook_open': False,
        'mouth': 'open',
        'blush': False,
        'cowlick_scale': 1.2,
    }
    return render_panel_figure(gp, draw_gesture_line=True)


# ===================================================================
# Panel 2: ANALYSIS LEAN
# ===================================================================

def make_panel2():
    """Analysis Lean: forward tilt 6-8deg, head tilts right, notebook extended."""
    gp = {
        'curve_amount': 0.06,
        'curve_direction': 'right',
        'curve_type': 'c',
        'head_offset_x': 10,
        'head_offset_y': 8,
        'weight_foot_offset': 6,
        'free_foot_offset': -16,
        'free_foot_lift': 0,
        'free_knee_offset_x': -5,
        'shoulder_rise_l': 4,
        'shoulder_rise_r': 8,
        'hip_tilt_px': 3,
        'left_arm_angle': -30,
        'right_arm_angle': -120,
        'left_arm_bend': 0.12,
        'right_arm_bend': 0.15,
        'glasses_tilt': 9,
        'head_tilt_deg': 6,
        'notebook_side': 'right',
        'notebook_open': True,
        'mouth': 'compressed',
        'blush': False,
        'cowlick_scale': 1.0,
    }
    return render_panel_figure(gp, draw_gesture_line=True)


# ===================================================================
# Panel 3: RELUCTANT MOVE
# ===================================================================

def make_panel3():
    """Reluctant Move: rigid body lean 10-12deg, notebook clutched, no arm pump."""
    gp = {
        'curve_amount': 0.09,
        'curve_direction': 'left',
        'curve_type': 'c',
        'head_offset_x': -16,
        'head_offset_y': 4,
        'weight_foot_offset': 14,
        'free_foot_offset': -20,
        'free_foot_lift': 4,
        'free_knee_offset_x': -6,
        'shoulder_rise_l': 3,
        'shoulder_rise_r': 3,
        'hip_tilt_px': 1,
        'left_arm_angle': -25,
        'right_arm_angle': -155,
        'left_arm_bend': 0.08,
        'right_arm_bend': 0.08,
        'glasses_tilt': 9,
        'head_tilt_deg': -2,
        'notebook_side': 'left',
        'notebook_open': False,
        'mouth': 'grimace',
        'blush': False,
        'cowlick_scale': 0.9,
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
    draw.text((PAD, 8), "COSMO — Motion Spec Sheet v002 (Gesture-First)",
              fill=LABEL_TEXT, font=font_bold)
    draw.text((PAD, 22),
              "RYO HASEGAWA  |  Luma & the Glitchkin  |  C53  |  pycairo + curve_draw",
              fill=(180, 165, 140), font=font_sm)

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
        ("B1: IDLE / OBSERVING", "beat: 1-2-3-4 loop"),
        ("B2: STARTLED", "peak beat 1 | snap-back beat 2.5"),
        ("B3: ANALYSIS LEAN", "fwd tilt 6-8deg | notebook consult"),
        ("B4: RELUCTANT MOVE", "rigid lean | no arm pump"),
    ]

    for col in range(4):
        px, py = panel_origin(col)
        panel_img, pos = panels[col]

        # Paste cairo-rendered figure
        img.paste(panel_img, (px, py), panel_img)
        draw = ImageDraw.Draw(img)  # refresh after paste (PIL standards W004)

        # Panel border
        draw.rectangle([px, py, px + PANEL_W, py + PANEL_H], outline=PANEL_BORDER, width=1)

        # Beat badge (top-left) — BEAT_COLOR fill for lint detection (>=15% non-bg)
        badge_text = f"B{col + 1}"
        bx, by = px + 3, py + 3
        draw.rectangle([bx, by, bx + 36, by + 22], fill=BEAT_COLOR)
        draw.text((bx + 4, by + 3), badge_text, fill=(240, 248, 255), font=font_bold)

        # Title strip at bottom
        draw.rectangle([px, py + PANEL_H - 32, px + PANEL_W, py + PANEL_H], fill=LABEL_BG)
        draw.text((px + 6, py + PANEL_H - 28), panel_titles[col][0],
                  fill=LABEL_TEXT, font=font_bold)
        draw.text((px + 6, py + PANEL_H - 14), panel_titles[col][1],
                  fill=(200, 190, 170), font=font_sm)

    # --- Per-panel annotations (PIL overlay) ---

    # Panel 0: IDLE / OBSERVING annotations
    px0, py0 = panel_origin(0)
    pos0 = panels[0][1]
    draw.text((px0 + 8, py0 + 26), "TIMING", fill=LABEL_BG, font=font_bold)
    draw.text((px0 + 8, py0 + 38), "Weight shift:  beat 1", fill=BEAT_COLOR, font=font_sm)
    draw.text((px0 + 8, py0 + 49), "Head settle:   beat 2", fill=BEAT_COLOR, font=font_sm)
    draw.text((px0 + 8, py0 + 60), "Notebook lag:  beat 2.5", fill=MOTION_ARROW, font=font_sm)
    draw.text((px0 + 8, py0 + 71), "Return:        beat 4 -> loop", fill=BEAT_COLOR, font=font_sm)
    draw.text((px0 + 8, py0 + PANEL_H - 72), "S-curve upright", fill=GESTURE_RED, font=font_sm)
    draw.text((px0 + 8, py0 + PANEL_H - 60), "55/45 weight fwd", fill=MOTION_ARROW, font=font_sm)
    draw.text((px0 + 8, py0 + PANEL_H - 48), "glasses: 7deg CCW", fill=BEAT_COLOR, font=font_sm)

    # Panel 1: STARTLED annotations
    px1, py1 = panel_origin(1)
    draw.text((px1 + 8, py1 + 26), "TIMING", fill=LABEL_BG, font=font_bold)
    draw.text((px1 + 8, py1 + 38), "Beat 0: neutral", fill=BEAT_COLOR, font=font_sm)
    draw.text((px1 + 8, py1 + 49), "Beat 1: PEAK startle", fill=MOTION_ARROW, font=font_sm)
    draw.text((px1 + 8, py1 + 60), "  glasses: 14deg", fill=(200, 80, 20), font=font_sm)
    draw.text((px1 + 8, py1 + 71), "  arms jut outward", fill=MOTION_ARROW, font=font_sm)
    draw.text((px1 + 8, py1 + 82), "Beat 2.5: snap back", fill=BEAT_COLOR, font=font_sm)
    draw.text((px1 + 8, py1 + 93), "  glasses: 14->9deg", fill=BEAT_COLOR, font=font_sm)
    draw.text((px1 + 8, py1 + PANEL_H - 72), "C-curve backward lean", fill=GESTURE_RED, font=font_sm)
    draw.text((px1 + 8, py1 + PANEL_H - 60), "notebook jostled +1.5b", fill=MOTION_ARROW, font=font_sm)
    draw.text((px1 + 8, py1 + PANEL_H - 48), "both shoulders UP", fill=BEAT_COLOR, font=font_sm)

    # Panel 2: ANALYSIS LEAN annotations
    px2, py2 = panel_origin(2)
    draw.text((px2 + 8, py2 + 26), "TIMING", fill=LABEL_BG, font=font_bold)
    draw.text((px2 + 8, py2 + 38), "Beat 1: torso tilts fwd", fill=BEAT_COLOR, font=font_sm)
    draw.text((px2 + 8, py2 + 49), "Beat 1.5: head tilts R", fill=BEAT_COLOR, font=font_sm)
    draw.text((px2 + 8, py2 + 60), "Beat 2: notebook OPEN", fill=MOTION_ARROW, font=font_sm)
    draw.text((px2 + 8, py2 + 71), "Beat 3: hold (read)", fill=BEAT_COLOR, font=font_sm)
    draw.text((px2 + 8, py2 + PANEL_H - 84), "GESTURE-FIRST LEAN:", fill=GESTURE_RED, font=font_sm)
    draw.text((px2 + 8, py2 + PANEL_H - 72), "Forward C-curve 6-8deg", fill=GESTURE_RED, font=font_sm)
    draw.text((px2 + 8, py2 + PANEL_H - 60), "glasses: 9deg (analysis)", fill=BEAT_COLOR, font=font_sm)
    draw.text((px2 + 8, py2 + PANEL_H - 48), "notebook out + open", fill=MOTION_ARROW, font=font_sm)

    # Panel 3: RELUCTANT MOVE annotations
    px3, py3 = panel_origin(3)
    draw.text((px3 + 8, py3 + 26), "TIMING", fill=LABEL_BG, font=font_bold)
    draw.text((px3 + 8, py3 + 38), "Beat 1: body TILTS", fill=BEAT_COLOR, font=font_sm)
    draw.text((px3 + 8, py3 + 49), "  rigid lean 10-12deg", fill=BEAT_COLOR, font=font_sm)
    draw.text((px3 + 8, py3 + 60), "Beat 2: legs follow", fill=BEAT_COLOR, font=font_sm)
    draw.text((px3 + 8, py3 + 71), "  NO arm pump", fill=MOTION_ARROW, font=font_sm)
    draw.text((px3 + 8, py3 + 82), "Beat 3: notebook lag", fill=MOTION_ARROW, font=font_sm)
    draw.text((px3 + 8, py3 + 93), "  +1.5 beats behind", fill=MOTION_ARROW, font=font_sm)
    draw.text((px3 + 8, py3 + PANEL_H - 72), "C-curve rigid lean", fill=GESTURE_RED, font=font_sm)
    draw.text((px3 + 8, py3 + PANEL_H - 60), "arms CLOSE to body", fill=MOTION_ARROW, font=font_sm)
    draw.text((px3 + 8, py3 + PANEL_H - 48), "notebook CLUTCHED", fill=MOTION_ARROW, font=font_sm)

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

    out_path = os.path.join(_OUTPUT_DIR, "LTG_CHAR_cosmo_motion.png")
    img.save(out_path)
    print(f"Saved: {out_path} ({img.width}x{img.height}px)")
    return out_path


if __name__ == "__main__":
    main()
