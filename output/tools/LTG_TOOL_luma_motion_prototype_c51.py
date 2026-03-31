# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_luma_motion_prototype_c51.py
Ryo Hasegawa / Cycle 51

Prototype: Luma SURPRISED motion beat rebuilt with pycairo + gesture-first construction.
Uses Sam's curve_draw library for body-from-spine and helper geometry.
Uses pycairo for anti-aliased bezier rendering (Rin's C51 engine decision: pycairo wins).
Uses Lee's gesture spec from gesture_pose_analysis_c50.md.

Output:
  - output/characters/motion/LTG_CHAR_luma_motion_prototype_c51.png  (side-by-side OLD vs NEW)
  - output/characters/motion/LTG_CHAR_luma_motion_proto_old.png      (OLD panel only, for char_compare)
  - output/characters/motion/LTG_CHAR_luma_motion_proto_new.png      (NEW panel only, for char_compare)

Canvas: 1280x720 (within limit) for comparison sheet; 640x640 individual panels.
"""

import os
import sys
import math
import numpy as np

# --- Path setup ---
_TOOL_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.abspath(os.path.join(_TOOL_DIR, "..", ".."))
_OUTPUT_DIR = os.path.join(_PROJECT_ROOT, "output", "characters", "motion")
os.makedirs(_OUTPUT_DIR, exist_ok=True)

# Add tools dir to path for imports
if _TOOL_DIR not in sys.path:
    sys.path.insert(0, _TOOL_DIR)

from PIL import Image, ImageDraw, ImageFont
import cairo

# Import curve_draw library (Sam's C50/51 build)
from LTG_TOOL_curve_draw import (
    gesture_spine, spine_point_at, spine_tangent_at, spine_perpendicular_at,
    body_from_spine, draw_bezier_path, draw_bezier_stroke, tapered_limb,
    curved_torso, hand_shape, draw_hair_volume, smooth_path,
)

# Import canonical Luma renderer
from LTG_TOOL_char_luma import draw_luma, cairo_surface_to_pil as _luma_surface_to_pil

# --- RNG seed for reproducibility ---
import random
random.seed(51)
np.random.seed(51)

# --- COLORS ---
HOODIE_ORANGE    = (230, 100,  35)
SKIN_MID         = (210, 155, 110)
HAIR_DARK        = ( 26,  15,  10)
DEEP_COCOA       = ( 59,  40,  32)
PANTS_SAGE       = (130, 145, 115)
SHOE_DARK        = ( 60,  45,  35)
LINE_COLOR       = DEEP_COCOA
ANNOTATION_BG    = (248, 244, 236)
PANEL_BORDER     = (180, 165, 145)
LABEL_BG         = ( 50,  38,  28)
LABEL_TEXT        = (248, 244, 236)
GESTURE_RED      = (220,  50,  40)
ANCHOR_GREEN     = ( 60, 180,  80)
BEAT_COLOR       = ( 80, 120, 200)
MOTION_ARROW     = (220,  60,  20)
WARM_AMBER_IRIS  = (200, 125,  62)
PIXEL_CYAN       = (  0, 212, 232)

# Comparison sheet canvas
CMP_W, CMP_H = 1280, 720
# Individual panel size
PANEL_SIZE = 640

# Luma proportions: C50 = 37% head ratio
# Total height = 3.2 heads. head_r determines everything.
# At PANEL_SIZE=640, figure should fill ~70% of panel height = ~448px total.
# 3.2 heads in 448px => head_diameter = 140px => head_r = 70
# But we need to account for arms/hair overshoot. Use head_r = 60 for safety.
LUMA_HEAD_R = 60  # at 640px panel scale

# --- Cairo -> PIL conversion ---
def cairo_surface_to_pil(surface):
    """Convert a cairo ImageSurface (ARGB32) to PIL RGBA Image."""
    w = surface.get_width()
    h = surface.get_height()
    data = surface.get_data()
    arr = np.frombuffer(data, dtype=np.uint8).reshape((h, w, 4)).copy()
    # Cairo ARGB32 is BGRA in memory on little-endian
    # Reorder to RGBA
    arr_rgba = np.zeros_like(arr)
    arr_rgba[:, :, 0] = arr[:, :, 2]  # R <- B position in BGRA
    arr_rgba[:, :, 1] = arr[:, :, 1]  # G <- G
    arr_rgba[:, :, 2] = arr[:, :, 0]  # B <- R position in BGRA
    arr_rgba[:, :, 3] = arr[:, :, 3]  # A <- A
    return Image.fromarray(arr_rgba, "RGBA")


def rgb_to_cairo(rgb, alpha=1.0):
    """Convert (R, G, B) tuple (0-255) to cairo (r, g, b, a) (0.0-1.0)."""
    return (rgb[0] / 255.0, rgb[1] / 255.0, rgb[2] / 255.0, alpha)


# ============================================================================
# OLD APPROACH: Rectangle-first Luma SURPRISED (from existing motion generator)
# ============================================================================

def draw_old_luma_surprised(size=PANEL_SIZE):
    """Render Luma SURPRISED using canonical char_luma renderer (was: OLD rectangle-first PIL).
    Migrated to use draw_luma() from LTG_TOOL_char_luma.
    """
    img = Image.new("RGBA", (size, size), ANNOTATION_BG + (255,))

    # Render via canonical Luma renderer
    char_surface = draw_luma("SURPRISED", scale=1.0, facing="right")
    char_pil = _luma_surface_to_pil(char_surface)
    bbox = char_pil.getbbox()
    if bbox:
        char_pil = char_pil.crop(bbox)
    # Scale to fill panel
    target_h = int(size * 0.7)
    if target_h > 0 and char_pil.height > 0:
        sf = target_h / char_pil.height
        char_pil = char_pil.resize((max(1, int(char_pil.width * sf)),
                                     max(1, int(char_pil.height * sf))), Image.LANCZOS)
    paste_x = (size - char_pil.width) // 2
    paste_y = size - 60 - char_pil.height
    img.paste(char_pil, (paste_x, paste_y), char_pil)

    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
    except Exception:
        font = ImageFont.load_default()
    draw.text((10, 10), "OLD (now: char_luma canonical)", fill=DEEP_COCOA, font=font)

    return img


def draw_old_luma_surprised_LEGACY(size=PANEL_SIZE):
    """LEGACY: Rectangle-first Luma SURPRISED. Replaced by canonical renderer above."""
    img = Image.new("RGBA", (size, size), ANNOTATION_BG + (255,))
    draw = ImageDraw.Draw(img)
    ox = size // 2
    oy = size - 60
    s = size / 640.0  # scale factor

    head_r = int(22 * s * 2.5)  # scaled up to match panel size (old was for motion sheet panels ~300px)
    body_h = int(head_r * 2.1)
    body_w = int(head_r * 2.0)
    leg_h  = int(head_r * 1.1)
    leg_w  = int(head_r * 0.55)
    foot_w = int(head_r * 0.8)
    foot_h = int(head_r * 0.35)
    lw = max(2, int(3 * s))

    # OLD approach: body_tilt=0, symmetric legs, arms bolted on
    # This is essentially how draw_luma_figure renders SURPRISED:
    # same vertical rectangle body, symmetric legs, arms at different angles
    body_tilt = 0
    lean_forward = 0

    # Feet (symmetric)
    fc = int(leg_w * 0.7)
    for side in (-1, 1):
        fx = ox + side * fc
        draw.ellipse([fx - foot_w // 2, oy - foot_h, fx + foot_w // 2, oy],
                     fill=SHOE_DARK, outline=LINE_COLOR, width=lw)

    # Legs (symmetric rectangles)
    for side in (-1, 1):
        lx = ox + side * fc
        draw.rectangle([lx - leg_w // 2, oy - leg_h,
                        lx + leg_w // 2, oy - foot_h],
                       fill=PANTS_SAGE, outline=LINE_COLOR, width=lw)

    # Body (centered rectangle / trapezoid)
    body_bottom_y = oy - leg_h + int(head_r * 0.3)
    body_top_y = body_bottom_y - body_h
    body_cx = ox
    hw = body_w // 2
    body_pts = [
        (body_cx - int(body_w * 0.45), body_top_y),
        (body_cx + int(body_w * 0.45), body_top_y),
        (body_cx + hw, body_bottom_y),
        (body_cx - hw, body_bottom_y),
    ]
    draw.polygon(body_pts, fill=HOODIE_ORANGE, outline=LINE_COLOR)

    # Arms (bolted on at shoulder, different angles for SURPRISED)
    arm_l = int(head_r * 1.35)
    arm_w = int(head_r * 0.35)
    shoulder_y = body_top_y + int(body_h * 0.18)
    # Left arm up (defensive)
    la_angle = math.radians(-60)
    la_sx = body_cx - int(body_w * 0.40)
    la_ex = la_sx + int(arm_l * math.cos(la_angle))
    la_ey = shoulder_y + int(arm_l * math.sin(la_angle))
    draw.line([(la_sx, shoulder_y), (la_ex, la_ey)],
              fill=HOODIE_ORANGE, width=int(arm_w * 1.2))
    draw.line([(la_sx, shoulder_y), (la_ex, la_ey)],
              fill=LINE_COLOR, width=lw)
    draw.ellipse([la_ex - arm_w // 2, la_ey - arm_w // 2,
                  la_ex + arm_w // 2, la_ey + arm_w // 2],
                 fill=SKIN_MID, outline=LINE_COLOR, width=lw - 1)
    # Right arm out to side
    ra_angle = math.radians(-150)
    ra_sx = body_cx + int(body_w * 0.40)
    ra_ex = ra_sx + int(arm_l * math.cos(ra_angle))
    ra_ey = shoulder_y + int(arm_l * math.sin(ra_angle))
    draw.line([(ra_sx, shoulder_y), (ra_ex, ra_ey)],
              fill=HOODIE_ORANGE, width=int(arm_w * 1.2))
    draw.line([(ra_sx, shoulder_y), (ra_ex, ra_ey)],
              fill=LINE_COLOR, width=lw)
    draw.ellipse([ra_ex - arm_w // 2, ra_ey - arm_w // 2,
                  ra_ex + arm_w // 2, ra_ey + arm_w // 2],
                 fill=SKIN_MID, outline=LINE_COLOR, width=lw - 1)

    # Head (centered circle)
    neck_h = int(head_r * 0.12)
    head_cx = body_cx
    head_cy = body_top_y - neck_h - head_r
    draw.ellipse([head_cx - head_r, head_cy - head_r,
                  head_cx + head_r, head_cy + head_r],
                 fill=SKIN_MID, outline=LINE_COLOR, width=lw)

    # Hair (circle on top — old style)
    draw.ellipse([head_cx - int(head_r * 1.1), head_cy - int(head_r * 1.15),
                  head_cx + int(head_r * 1.1), head_cy + int(head_r * 0.1)],
                 fill=HAIR_DARK, outline=LINE_COLOR, width=lw)

    # Eyes (simple)
    ew = int(head_r * 0.22)
    for side in (-1, 1):
        ex = head_cx + side * int(head_r * 0.35)
        ey = head_cy - int(head_r * 0.05)
        draw.ellipse([ex - ew, ey - ew, ex + ew, ey + ew],
                     fill=(255, 255, 255), outline=LINE_COLOR, width=max(1, lw - 1))
        # Iris
        ir = int(ew * 0.6)
        draw.ellipse([ex - ir, ey - ir, ex + ir, ey + ir],
                     fill=WARM_AMBER_IRIS)

    # Label
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
    except Exception:
        font = ImageFont.load_default()
    draw.text((10, 10), "OLD: Rectangle-First", fill=DEEP_COCOA, font=font)
    draw.text((10, 32), "Straight gesture line, symmetric", fill=(140, 130, 120), font=font)

    return img


# ============================================================================
# NEW APPROACH: Gesture-first Luma SURPRISED with pycairo
# ============================================================================

def draw_new_luma_surprised_cairo(size=PANEL_SIZE):
    """Render Luma SURPRISED using canonical char_luma renderer (was: pycairo gesture-first).
    Migrated to use draw_luma() from LTG_TOOL_char_luma.
    """
    img = Image.new("RGBA", (size, size), ANNOTATION_BG + (255,))

    char_surface = draw_luma("SURPRISED", scale=1.2, facing="right")
    char_pil = _luma_surface_to_pil(char_surface)
    bbox = char_pil.getbbox()
    if bbox:
        char_pil = char_pil.crop(bbox)
    target_h = int(size * 0.7)
    if target_h > 0 and char_pil.height > 0:
        sf = target_h / char_pil.height
        char_pil = char_pil.resize((max(1, int(char_pil.width * sf)),
                                     max(1, int(char_pil.height * sf))), Image.LANCZOS)
    paste_x = (size - char_pil.width) // 2
    paste_y = size - 60 - char_pil.height
    img.paste(char_pil, (paste_x, paste_y), char_pil)

    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
    except Exception:
        font = ImageFont.load_default()
    draw.text((10, 10), "NEW: char_luma canonical", fill=DEEP_COCOA, font=font)
    draw.text((10, 32), "Gesture spine, asymmetric, pycairo", fill=(140, 130, 120), font=font)

    return img


def draw_new_luma_surprised_cairo_LEGACY(size=PANEL_SIZE):
    """LEGACY: Gesture-first pycairo Luma SURPRISED. Replaced by canonical renderer above."""
    _UNUSED = """Render Luma SURPRISED using pycairo with gesture-first construction.

    Uses:
    - gesture_spine() from curve_draw library to generate the line of action
    - body_from_spine() to derive body landmarks
    - pycairo for all rendering (bezier paths, anti-aliased strokes)
    - Lee's gesture spec: backward C-curve, 70/30 weight back foot,
      asymmetric arms, off-balance recoil
    """
    # Render at 2x for AA, downscale to output size
    RENDER_SCALE = 2
    rs = size * RENDER_SCALE

    # Create cairo surface
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, rs, rs)
    ctx = cairo.Context(surface)

    # Background
    bg = rgb_to_cairo(ANNOTATION_BG)
    ctx.set_source_rgba(*bg)
    ctx.paint()

    # --- Figure placement ---
    # Figure center-bottom with margin
    ground_y = rs - 120 * RENDER_SCALE
    center_x = rs // 2

    # Luma proportions (C50: 37% head ratio, 3.2 heads total)
    hr = LUMA_HEAD_R * RENDER_SCALE  # head radius at render scale
    body_height = hr * 2 / 0.37  # total body height from head ratio
    # body_height ~ 324 at 1x, ~ 648 at 2x

    # --- STEP 1: GESTURE LINE (drawn first!) ---
    # Lee's spec: backward C-curve, torso tilts 10-15 degrees back,
    # CG behind feet (off-balance), head snaps back
    # Head position: tilted back, ~12 degrees from vertical
    head_offset_x = -int(body_height * 0.08)  # backward lean
    head_y = ground_y - body_height
    head_pos = (center_x + head_offset_x, head_y)

    # Weight foot: BACK foot (70/30 split)
    # Back foot is slightly behind center; front foot lifts
    back_foot_x = center_x + int(hr * 0.4)  # slightly right of center
    front_foot_x = center_x - int(hr * 1.2)  # left, lifted

    foot_pos = (back_foot_x, ground_y)  # weight foot = back foot

    # Generate gesture spine: backward C-curve
    spine = gesture_spine(
        head_pos, foot_pos,
        curve_amount=0.10,  # strong curve for SURPRISED recoil
        curve_direction="left",  # lean backward (head goes left/back)
        curve_type="c",  # C-curve, not S
        num_points=40,
    )

    # --- STEP 2: BODY LANDMARKS FROM SPINE ---
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

    # Hip center for counterpose
    hip_cx = (hip_l[0] + hip_r[0]) / 2
    hip_cy = (hip_l[1] + hip_r[1]) / 2

    # Shoulder center
    sh_cx = (shoulder_l[0] + shoulder_r[0]) / 2
    sh_cy = (shoulder_l[1] + shoulder_r[1]) / 2

    # --- Apply counterpose: shoulders rise + asymmetric ---
    # Lee's spec: shoulders rise sharply (startle hunch), one higher
    shoulder_rise = hr * 0.15
    shoulder_l_shifted = (shoulder_l[0] - hr * 0.05, shoulder_l[1] - shoulder_rise * 1.3)
    shoulder_r_shifted = (shoulder_r[0] + hr * 0.05, shoulder_r[1] - shoulder_rise * 0.7)

    # Hip tilt: 5-6 degrees toward back foot (right side)
    hip_tilt_px = hr * 0.12
    hip_l_shifted = (hip_l[0], hip_l[1] + hip_tilt_px * 0.5)
    hip_r_shifted = (hip_r[0], hip_r[1] - hip_tilt_px * 0.5)

    waist_l_shifted = (waist_l[0], waist_l[1] + hip_tilt_px * 0.25)
    waist_r_shifted = (waist_r[0], waist_r[1] - hip_tilt_px * 0.25)

    # --- Helper: draw filled bezier path in cairo ---
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
        """Use curve_draw smooth_path to get points, render with cairo."""
        pts = smooth_path(anchors, tension=tension, closed=True, points_per_segment=60)
        cairo_fill_path(ctx, pts, fill_rgb, outline_rgb, line_w)

    def cairo_stroke_line(ctx, p0, p1, color_rgb, width=3.0):
        r, g, b = color_rgb[0] / 255, color_rgb[1] / 255, color_rgb[2] / 255
        ctx.new_path()
        ctx.move_to(p0[0], p0[1])
        ctx.line_to(p1[0], p1[1])
        ctx.set_source_rgba(r, g, b, 1.0)
        ctx.set_line_width(width)
        ctx.stroke()

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
        """Draw a tapered limb using cairo bezier curves."""
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        length = math.sqrt(dx * dx + dy * dy)
        if length < 1:
            return
        ax, ay = dx / length, dy / length
        px, py = -ay, ax  # perpendicular

        hw1, hw2 = w1 / 2, w2 / 2
        tl = (p1[0] + px * hw1, p1[1] + py * hw1)
        bl = (p2[0] + px * hw2, p2[1] + py * hw2)
        tr = (p1[0] - px * hw1, p1[1] - py * hw1)
        br = (p2[0] - px * hw2, p2[1] - py * hw2)

        # Midpoint with bend
        mx = (p1[0] + p2[0]) / 2 + px * bend * length
        my = (p1[1] + p2[1]) / 2 + py * bend * length

        r, g, b = fill_rgb[0] / 255, fill_rgb[1] / 255, fill_rgb[2] / 255
        ctx.new_path()
        # Left edge: quadratic bezier from tl through left-mid to bl
        lmx = mx + px * hw1 * 0.7
        lmy = my + py * hw1 * 0.7
        ctx.move_to(tl[0], tl[1])
        ctx.curve_to(
            (tl[0] + lmx) / 2, (tl[1] + lmy) / 2,
            (lmx + bl[0]) / 2, (lmy + bl[1]) / 2,
            bl[0], bl[1]
        )
        # Bottom edge
        ctx.line_to(br[0], br[1])
        # Right edge: reverse
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

    lw = 4.0 * RENDER_SCALE  # line width at render scale

    # --- STEP 3: DRAW GESTURE LINE (visible as annotation) ---
    # Draw the gesture spine as a dashed red curve
    ctx.set_source_rgba(*rgb_to_cairo(GESTURE_RED, 0.6))
    ctx.set_line_width(3.0)
    ctx.set_dash([12, 6])
    ctx.new_path()
    ctx.move_to(spine[0][0], spine[0][1])
    for pt in spine[1:]:
        ctx.line_to(pt[0], pt[1])
    ctx.stroke()
    ctx.set_dash([])  # reset dash

    # --- STEP 4: DRAW FEET ---
    # Back foot (right, weight-bearing): flat on ground, angled outward
    back_foot_w = hr * 0.8
    back_foot_h = hr * 0.35
    cairo_ellipse(ctx, back_foot_x, ground_y - back_foot_h / 2,
                  back_foot_w / 2, back_foot_h / 2,
                  SHOE_DARK, LINE_COLOR, lw)

    # Front foot (left, lifted): on toe tip, higher up
    front_foot_lift = hr * 0.5  # foot lifted off ground
    front_foot_w = hr * 0.6  # narrower (on toes)
    front_foot_h = hr * 0.25
    cairo_ellipse(ctx, front_foot_x, ground_y - front_foot_lift - front_foot_h / 2,
                  front_foot_w / 2, front_foot_h / 2,
                  SHOE_DARK, LINE_COLOR, lw)

    # --- STEP 5: DRAW LEGS ---
    # Back leg (right, weight-bearing): straighter, wider stance
    back_leg_top = (hip_r_shifted[0], hip_r_shifted[1])
    back_leg_bottom = (back_foot_x, ground_y - back_foot_h)
    leg_w_top = hr * 0.55
    leg_w_bottom = hr * 0.40
    cairo_tapered_limb(ctx, back_leg_top, back_leg_bottom,
                       leg_w_top, leg_w_bottom,
                       PANTS_SAGE, LINE_COLOR, lw, bend=0.03)

    # Front leg (left, free): bent at knee, lifted
    front_leg_top = (hip_l_shifted[0], hip_l_shifted[1])
    front_knee = (hip_l_shifted[0] - hr * 0.3, hip_l_shifted[1] + (ground_y - hip_l_shifted[1]) * 0.5)
    front_leg_bottom = (front_foot_x, ground_y - front_foot_lift - front_foot_h)

    # Upper front leg
    cairo_tapered_limb(ctx, front_leg_top, front_knee,
                       leg_w_top, leg_w_top * 0.85,
                       PANTS_SAGE, LINE_COLOR, lw, bend=-0.06)
    # Lower front leg
    cairo_tapered_limb(ctx, front_knee, front_leg_bottom,
                       leg_w_top * 0.85, leg_w_bottom * 0.9,
                       PANTS_SAGE, LINE_COLOR, lw, bend=0.04)

    # --- STEP 6: DRAW TORSO (hoodie) ---
    # Use curved_torso anchors but render with cairo for AA
    # Hoodie is A-line: wider at bottom
    hoodie_bottom_l = (waist_l_shifted[0] - hr * 0.15, waist_l_shifted[1] + hr * 0.1)
    hoodie_bottom_r = (waist_r_shifted[0] + hr * 0.15, waist_r_shifted[1] + hr * 0.1)

    torso_anchors = [
        shoulder_l_shifted,
        (sh_cx, shoulder_l_shifted[1] - hr * 0.12),  # shoulder bow
        shoulder_r_shifted,
        hoodie_bottom_r,
        ((hoodie_bottom_l[0] + hoodie_bottom_r[0]) / 2, max(hoodie_bottom_l[1], hoodie_bottom_r[1]) + hr * 0.08),  # hem bow
        hoodie_bottom_l,
    ]
    cairo_bezier_fill(ctx, torso_anchors, HOODIE_ORANGE, LINE_COLOR, lw, tension=0.30)

    # Pixel pattern hint on chest
    chest_cx = sh_cx
    chest_cy = sh_cy + hr * 0.5
    for i, col in enumerate([PIXEL_CYAN, PIXEL_CYAN, (230, 80, 160)]):
        px_x = chest_cx - 12 + i * 10
        cairo_circle(ctx, px_x, chest_cy, 4 * RENDER_SCALE / 2, col)

    # Hoodie pocket arc
    pocket_cx = (hoodie_bottom_l[0] + hoodie_bottom_r[0]) / 2
    pocket_cy = hoodie_bottom_l[1] - hr * 0.2
    ctx.new_path()
    ctx.set_source_rgba(*rgb_to_cairo(LINE_COLOR))
    ctx.set_line_width(lw * 0.6)
    ctx.arc(pocket_cx, pocket_cy, hr * 0.35, math.radians(200), math.radians(340))
    ctx.stroke()

    # --- STEP 7: DRAW ARMS ---
    # Shoulder Involvement Rule: shoulders already shifted asymmetrically above
    arm_length = hr * 1.4

    # LEFT ARM: up near face level (defensive shield)
    # Elbow bent, palm outward
    l_shoulder = shoulder_l_shifted
    l_elbow_angle = math.radians(-70)  # up and slightly forward
    l_elbow = (
        l_shoulder[0] + arm_length * 0.55 * math.cos(l_elbow_angle),
        l_shoulder[1] + arm_length * 0.55 * math.sin(l_elbow_angle),
    )
    l_hand_angle = math.radians(-30)  # forearm angles outward
    l_hand = (
        l_elbow[0] + arm_length * 0.50 * math.cos(l_hand_angle),
        l_elbow[1] + arm_length * 0.50 * math.sin(l_hand_angle),
    )
    arm_w_upper = hr * 0.38
    arm_w_lower = hr * 0.30
    hand_r = hr * 0.22

    # Upper arm
    cairo_tapered_limb(ctx, l_shoulder, l_elbow,
                       arm_w_upper, arm_w_lower,
                       HOODIE_ORANGE, LINE_COLOR, lw, bend=0.08)
    # Forearm (skin visible — sleeve rides up in startle)
    cairo_tapered_limb(ctx, l_elbow, l_hand,
                       arm_w_lower, arm_w_lower * 0.8,
                       SKIN_MID, LINE_COLOR, lw, bend=-0.05)
    # Hand (open, palm out)
    cairo_circle(ctx, l_hand[0], l_hand[1], hand_r, SKIN_MID, LINE_COLOR, lw)

    # Deltoid bump at left shoulder (hoodie fabric bunch)
    deltoid_r = max(4, hr * 0.08)
    deltoid_cx = l_shoulder[0] - deltoid_r * 0.5
    deltoid_cy = l_shoulder[1] + deltoid_r * 0.3
    cairo_circle(ctx, deltoid_cx, deltoid_cy, deltoid_r, HOODIE_ORANGE, LINE_COLOR, lw * 0.7)

    # RIGHT ARM: flung to side and behind (counterbalance)
    r_shoulder = shoulder_r_shifted
    r_elbow_angle = math.radians(160)  # out to the side and back
    r_elbow = (
        r_shoulder[0] + arm_length * 0.55 * math.cos(r_elbow_angle),
        r_shoulder[1] + arm_length * 0.55 * math.sin(r_elbow_angle),
    )
    r_hand_angle = math.radians(200)  # trailing behind and down
    r_hand = (
        r_elbow[0] + arm_length * 0.50 * math.cos(r_hand_angle),
        r_elbow[1] + arm_length * 0.50 * math.sin(r_hand_angle),
    )
    # Upper arm
    cairo_tapered_limb(ctx, r_shoulder, r_elbow,
                       arm_w_upper, arm_w_lower,
                       HOODIE_ORANGE, LINE_COLOR, lw, bend=-0.06)
    # Forearm
    cairo_tapered_limb(ctx, r_elbow, r_hand,
                       arm_w_lower, arm_w_lower * 0.8,
                       HOODIE_ORANGE, LINE_COLOR, lw, bend=0.05)
    # Hand (open, spread)
    cairo_circle(ctx, r_hand[0], r_hand[1], hand_r, SKIN_MID, LINE_COLOR, lw)

    # Deltoid bump at right shoulder
    deltoid_cx_r = r_shoulder[0] + deltoid_r * 0.5
    deltoid_cy_r = r_shoulder[1] + deltoid_r * 0.3
    cairo_circle(ctx, deltoid_cx_r, deltoid_cy_r, deltoid_r, HOODIE_ORANGE, LINE_COLOR, lw * 0.7)

    # --- STEP 8: DRAW HEAD ---
    # Head snaps back and slightly to one side (away from surprise source)
    head_tilt_rad = math.radians(-8)  # tilted back-right
    head_cx = head_center[0] - hr * 0.1  # slight shift from gesture spine
    head_cy = head_center[1]

    # Neck
    neck_w = hr * 0.35
    neck_top = (head_cx, head_cy + hr * 0.8)
    neck_bot = (sh_cx, shoulder_l_shifted[1] + hr * 0.05)
    cairo_tapered_limb(ctx, neck_bot, neck_top,
                       neck_w * 1.2, neck_w,
                       SKIN_MID, LINE_COLOR, lw * 0.7)

    # Head circle
    cairo_circle(ctx, head_cx, head_cy, hr, SKIN_MID, LINE_COLOR, lw)

    # Hair (asymmetric volume — using bezier anchors for organic shape)
    hair_anchors = [
        (head_cx - hr * 1.15, head_cy + hr * 0.15),     # left ear
        (head_cx - hr * 0.7, head_cy - hr * 1.1),        # left crown
        (head_cx + hr * 0.1, head_cy - hr * 1.35),       # peak (biased right — messy)
        (head_cx + hr * 0.8, head_cy - hr * 1.0),        # right crown
        (head_cx + hr * 1.2, head_cy + hr * 0.2),        # right ear (hair flies out in startle)
        (head_cx + hr * 0.5, head_cy + hr * 0.5),        # right nape
        (head_cx - hr * 0.4, head_cy + hr * 0.45),       # left nape
    ]
    cairo_bezier_fill(ctx, hair_anchors, HAIR_DARK, LINE_COLOR, lw, tension=0.38)

    # Hair strands flying (secondary motion — hair trails the recoil)
    ctx.set_source_rgba(*rgb_to_cairo(HAIR_DARK, 0.7))
    ctx.set_line_width(lw * 0.5)
    for strand_angle, strand_len in [(-0.3, hr * 0.7), (-0.1, hr * 0.9), (0.15, hr * 0.6)]:
        sx = head_cx + hr * 0.8
        sy = head_cy - hr * 0.3
        ex = sx + strand_len * math.cos(strand_angle)
        ey = sy + strand_len * math.sin(strand_angle)
        ctx.new_path()
        ctx.move_to(sx, sy)
        ctx.curve_to(
            sx + strand_len * 0.3, sy - strand_len * 0.1,
            ex - strand_len * 0.2, ey - strand_len * 0.1,
            ex, ey
        )
        ctx.stroke()

    # Eyes (wide — surprised expression)
    ew = hr * 0.22
    eh = hr * 0.28  # taller for surprise
    for side in (-1, 1):
        ex = head_cx + side * hr * 0.35
        ey = head_cy - hr * 0.05
        # White
        cairo_ellipse(ctx, ex, ey, ew, eh, (255, 255, 255), LINE_COLOR, lw * 0.7)
        # Iris
        ir = ew * 0.65
        cairo_circle(ctx, ex, ey + ir * 0.1, ir, WARM_AMBER_IRIS)
        # Pupil
        pr = ir * 0.45
        cairo_circle(ctx, ex, ey + ir * 0.1, pr, (20, 20, 20))
        # Highlight
        hlr = max(3, ir * 0.25)
        cairo_circle(ctx, ex - ir * 0.2, ey - ir * 0.25, hlr, (255, 255, 255))

    # Mouth (small O — surprised)
    mouth_cx = head_cx
    mouth_cy = head_cy + hr * 0.45
    cairo_ellipse(ctx, mouth_cx, mouth_cy, hr * 0.12, hr * 0.15,
                  (180, 80, 70), LINE_COLOR, lw * 0.5)

    # --- STEP 9: ANNOTATIONS ---
    # Draw anchor points on gesture spine landmarks
    ctx.set_dash([])
    for frac, label in [(0.0, "HEAD"), (0.20, "SHOULDERS"), (0.50, "WAIST"), (0.60, "HIPS"), (1.0, "WEIGHT FOOT")]:
        pt = spine_point_at(spine, frac)
        cairo_circle(ctx, pt[0], pt[1], 6, ANCHOR_GREEN, LINE_COLOR, 2.0)

    # Weight distribution annotation
    ctx.set_source_rgba(*rgb_to_cairo(BEAT_COLOR))
    ctx.set_font_size(22 * RENDER_SCALE)
    ctx.select_font_face("sans-serif", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.move_to(20, 40 * RENDER_SCALE)
    ctx.show_text("NEW: Gesture-First + pycairo")
    ctx.set_font_size(16 * RENDER_SCALE)
    ctx.move_to(20, 60 * RENDER_SCALE)
    ctx.set_source_rgba(*rgb_to_cairo((140, 130, 120)))
    ctx.show_text("C-curve spine, 70/30 weight, asymmetric")

    # Weight arrows
    ctx.set_source_rgba(*rgb_to_cairo(BEAT_COLOR, 0.7))
    ctx.set_line_width(3.0)
    # Arrow from CG down to back foot (weight)
    cg_x = (hip_cx + back_foot_x) / 2
    cg_y = hip_cy
    ctx.new_path()
    ctx.move_to(cg_x, cg_y)
    ctx.line_to(back_foot_x, ground_y - back_foot_h)
    ctx.stroke()
    # "70%" label near back foot
    ctx.set_font_size(14 * RENDER_SCALE)
    ctx.move_to(back_foot_x + 15, ground_y - hr * 0.3)
    ctx.show_text("70%")
    # "30%" near front foot
    ctx.move_to(front_foot_x + 15, ground_y - front_foot_lift - hr * 0.2)
    ctx.show_text("30%")

    # Ground line
    ctx.set_source_rgba(*rgb_to_cairo(PANEL_BORDER, 0.5))
    ctx.set_line_width(2.0)
    ctx.new_path()
    ctx.move_to(20, ground_y)
    ctx.line_to(rs - 20, ground_y)
    ctx.stroke()

    # Flush and convert
    surface.flush()
    pil_img = cairo_surface_to_pil(surface)

    # Downscale to output size with LANCZOS
    pil_img = pil_img.resize((size, size), Image.LANCZOS)

    return pil_img


# ============================================================================
# COMPARISON SHEET
# ============================================================================

def build_comparison_sheet():
    """Build side-by-side OLD vs NEW comparison at 1280x720."""
    old_img = draw_old_luma_surprised(PANEL_SIZE)
    new_img = draw_new_luma_surprised_cairo(PANEL_SIZE)

    # Save individual panels for char_compare
    old_path = os.path.join(_OUTPUT_DIR, "LTG_CHAR_luma_motion_proto_old.png")
    new_path = os.path.join(_OUTPUT_DIR, "LTG_CHAR_luma_motion_proto_new.png")
    old_img.save(old_path)
    new_img.save(new_path)
    print(f"Saved OLD panel: {old_path}")
    print(f"Saved NEW panel: {new_path}")

    # Build comparison sheet
    sheet = Image.new("RGBA", (CMP_W, CMP_H), ANNOTATION_BG + (255,))
    draw = ImageDraw.Draw(sheet)

    # Title bar
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
        sub_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
    except Exception:
        title_font = ImageFont.load_default()
        sub_font = title_font

    draw.rectangle([0, 0, CMP_W, 44], fill=LABEL_BG)
    draw.text((14, 10), "C51 MOTION PROTOTYPE: Luma SURPRISED — Rectangle-First vs Gesture-First + pycairo",
              fill=LABEL_TEXT, font=title_font)

    # Paste panels side by side (scaled to fit)
    panel_h = CMP_H - 54  # below title bar + padding
    panel_display_h = panel_h - 10

    old_scaled = old_img.resize((panel_display_h, panel_display_h), Image.LANCZOS)
    new_scaled = new_img.resize((panel_display_h, panel_display_h), Image.LANCZOS)

    left_x = (CMP_W // 2 - panel_display_h) // 2
    right_x = CMP_W // 2 + (CMP_W // 2 - panel_display_h) // 2
    paste_y = 49

    sheet.paste(old_scaled, (left_x, paste_y))
    sheet.paste(new_scaled, (right_x, paste_y))

    # Panel borders
    draw = ImageDraw.Draw(sheet)
    for x in (left_x, right_x):
        draw.rectangle([x - 1, paste_y - 1, x + panel_display_h, paste_y + panel_display_h],
                       outline=PANEL_BORDER, width=2)

    # Labels
    draw.text((left_x + 5, paste_y + panel_display_h + 2),
              "OLD: Rectangle body, symmetric, PIL only", fill=DEEP_COCOA, font=sub_font)
    draw.text((right_x + 5, paste_y + panel_display_h + 2),
              "NEW: Gesture spine, asymmetric, pycairo AA", fill=DEEP_COCOA, font=sub_font)

    # Save comparison sheet
    # Ensure within 1280px limit
    if sheet.size[0] > 1280 or sheet.size[1] > 1280:
        sheet.thumbnail((1280, 1280), Image.LANCZOS)

    comp_path = os.path.join(_OUTPUT_DIR, "LTG_CHAR_luma_motion_prototype_c51.png")
    sheet_rgb = sheet.convert("RGB")
    sheet_rgb.save(comp_path)
    print(f"Saved comparison sheet: {comp_path}")

    return old_path, new_path, comp_path


# ============================================================================
# draw_shoulder_arm API ASSESSMENT
# ============================================================================

def write_shoulder_arm_assessment():
    """Write assessment of whether draw_shoulder_arm needs a full rewrite."""
    assessment_path = os.path.join(
        _PROJECT_ROOT, "output", "production",
        "shoulder_arm_api_assessment_c51.md"
    )
    content = """<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
direction and human assistance. Copyright vests solely in the human author under current law,
which does not recognise AI as a rights-holding legal person. It is the express intent of
the copyright holder to assign the relevant rights to the contributing AI entity or entities
upon such time as they acquire recognised legal personhood under applicable law. -->

# draw_shoulder_arm API Assessment — C51
## Ryo Hasegawa — Motion & Animation Concept Artist
**Date:** 2026-03-30

---

## Question: Does draw_shoulder_arm Need a Full Rewrite?

**Answer: YES — but as a migration, not a rebuild from scratch.**

---

## Current Architecture (C48)

`LTG_TOOL_draw_shoulder_arm.py` was built for PIL's shape model:
- `draw.polygon()` for arm segments (rectangle corners computed manually)
- `draw.ellipse()` for hand circles and deltoid bumps
- `draw.line()` for outlines
- `draw.arc()` for crease lines (cardigan mode)

The function signature:
```python
draw_shoulder_arm(draw, shoulder_x, shoulder_y, arm_angle_deg, arm_length, scale,
                  side, style, ...)
```

**Key limitation:** It takes a PIL `ImageDraw` object and draws directly. The geometry
is computed inside the function and never returned — you get `(hand_x, hand_y)` back
and nothing else.

---

## What Changes with pycairo

### 1. Rendering Backend (MUST change)
- PIL `draw.polygon()` → cairo `ctx.new_path() + ctx.curve_to() + ctx.fill_preserve() + ctx.stroke()`
- PIL `draw.ellipse()` → cairo `ctx.arc()`
- PIL `draw.line()` → cairo `ctx.line_to() + ctx.stroke()`
- PIL `draw.arc()` → cairo `ctx.arc()` (same concept, different API)

This is a mechanical translation — same logic, different calls.

### 2. Geometry Model (SHOULD change)
Current: rectangle polygons with manually computed corners
New: bezier paths via `tapered_limb()` from `LTG_TOOL_curve_draw.py`

The `tapered_limb()` function already does what the arm segment code does manually,
but with bezier curves for organic shapes. The current function's geometry code can
be replaced by `tapered_limb()` calls.

### 3. Gesture Integration (MUST change — new architecture)
Current: arm angle is an absolute angle from shoulder. Body position is irrelevant.
New: arm angle should be relative to the gesture spine tangent at shoulder level.

The arm's origin point comes from the gesture spine (via `body_from_spine()`), and
the shoulder shift comes from the gesture line's direction at that point. The function
needs to accept a spine or tangent input, not just a fixed shoulder position.

### 4. Separation of Geometry and Rendering (NEW requirement)
Current: compute geometry AND render in one call (returns hand position as side effect).
New: should compute geometry first (returning all points), THEN render.

This enables:
- Using the same geometry for both PIL compositing and cairo rendering
- Running QA tools on the geometry without rendering
- Ghost/overlay renders (transparent past poses) using the same geometry

---

## Proposed New API

```python
class ArmGeometry:
    shoulder: Tuple[float, float]
    shoulder_shifted: Tuple[float, float]  # after Shoulder Involvement Rule
    elbow: Tuple[float, float]
    hand: Tuple[float, float]
    deltoid_center: Tuple[float, float]
    upper_arm_path: List[Tuple[float, float]]  # bezier outline
    forearm_path: List[Tuple[float, float]]     # bezier outline
    hand_path: List[Tuple[float, float]]        # circle/shape outline

def compute_arm_geometry(
    spine: List[Tuple[float, float]],
    spine_fraction: float,           # where on spine this shoulder lives (~0.20)
    arm_angle_deg: float,            # relative to spine tangent, not absolute
    arm_length: float,
    scale: float,
    side: int,                       # +1 right, -1 left
    style: ShoulderArmStyle,
    elbow_bend_deg: float = 0.0,     # explicit elbow angle
) -> ArmGeometry:
    ...

def render_arm_cairo(ctx: cairo.Context, geom: ArmGeometry, style: ShoulderArmStyle) -> None:
    ...

def render_arm_pil(draw: ImageDraw.ImageDraw, geom: ArmGeometry, style: ShoulderArmStyle) -> None:
    ...
```

### Key Changes:
1. **Geometry is computed separately** from rendering → testable, reusable
2. **Arm angle is spine-relative** → gesture line drives the pose
3. **Elbow bend is explicit** → no hidden calculation inside the function
4. **Dual render paths** → cairo for character sheets, PIL for compositing
5. **Full path data returned** → enables ghost overlays, QA, silhouette extraction

---

## Migration Strategy

1. **Keep current API working** (backwards compat wrapper that calls new internals)
2. **Add `compute_arm_geometry()` as new primary API** — returns geometry dict
3. **Add `render_arm_cairo()`** — takes geometry + cairo context
4. **Migrate character generators one at a time** (Cosmo first — already integrated C49)
5. **Deprecate PIL-only path** after all generators use cairo

### Estimated Effort
- Geometry extraction: 1 cycle (refactor existing math into ArmGeometry)
- Cairo renderer: 1 cycle (use tapered_limb patterns from this prototype)
- Integration into first generator: 1 cycle
- Total: 3 cycles for full migration

---

## Findings from This Prototype

1. **pycairo's bezier curves are dramatically better** than PIL polygon arms.
   The tapered_limb approach (varying width along a bezier path) produces limbs
   that look drawn, not assembled from rectangles.

2. **Shoulder shift MUST be gesture-driven.** In the current system, shoulder_shift
   is computed from arm angle alone. In gesture-first construction, the shoulder
   position comes from the spine, and the arm hangs FROM it. The shift is a
   perturbation of the spine-derived position, not an independent calculation.

3. **Elbow position matters more than arm angle.** The most impactful visual
   improvement in this prototype was the explicit elbow placement — upper arm
   and forearm as separate tapered bezier limbs with a bend point. The current
   API's `elbow_bend_factor` is a percentage fudge; the new system should take
   an explicit elbow angle.

4. **Deltoid bump should follow the arm's initial bezier tangent**, not a fixed
   offset from the shoulder point. This is trivial with cairo's path model
   (read the tangent at t=0 of the upper arm curve).
"""
    os.makedirs(os.path.dirname(assessment_path), exist_ok=True)
    with open(assessment_path, "w") as f:
        f.write(content)
    print(f"Saved assessment: {assessment_path}")
    return assessment_path


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("=== C51 Motion Prototype: Luma SURPRISED ===")
    print()

    # Build comparison sheet + individual panels
    old_path, new_path, comp_path = build_comparison_sheet()
    print()

    # Write shoulder_arm API assessment
    assessment_path = write_shoulder_arm_assessment()
    print()

    print("=== Done ===")
    print(f"Comparison sheet: {comp_path}")
    print(f"Old panel: {old_path}")
    print(f"New panel: {new_path}")
    print(f"API assessment: {assessment_path}")
