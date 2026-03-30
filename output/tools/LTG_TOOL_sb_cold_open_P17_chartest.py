#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_sb_cold_open_P17_chartest.py
Cold Open Panel P17 — CHARACTER QUALITY PROTOTYPE
Diego Vargas, Storyboard Artist — Cycle 50

PURPOSE: Same composition/staging as P17 (Beat of Stillness / Chip Falls) but with
IMPROVED character rendering. This is a comparison prototype to demonstrate that
organic-curve character construction reads better at storyboard panel scale.

CHANGES FROM ORIGINAL P17:
  1. Luma: Larger head (37% body height), asymmetric messy hair with volume,
     organic torso (bezier tapered bean shape, not rectangle), gesture line with
     slight forward lean (ASSESSING), tapered arms as tubes, mitten hands
  2. Byte: Slight forward lean toward chip (curiosity in body, not just face),
     curved arm shapes instead of rectangles
  3. Both: Weight distribution and gesture visible at panel scale

IDENTICAL to original P17:
  - Background, staging positions, negative space
  - Falling chip, annotations, caption bar
  - Camera, arc color, depth temperature

Output: output/storyboards/panels/LTG_SB_cold_open_P17_chartest.png
"""

try:
    from LTG_TOOL_project_paths import output_dir, ensure_dir
except ImportError:
    import pathlib
    def output_dir(*parts): return pathlib.Path("/home/wipkat/team/output").joinpath(*parts)
    def ensure_dir(path): path.mkdir(parents=True, exist_ok=True); return path
from PIL import Image, ImageDraw, ImageFont
import math, random, os

PANELS_DIR = output_dir('storyboards', 'panels')
OUTPUT_PATH = os.path.join(PANELS_DIR, "LTG_SB_cold_open_P17_chartest.png")
os.makedirs(str(PANELS_DIR), exist_ok=True)

PW, PH    = 800, 600
CAPTION_H = 72
DRAW_H    = PH - CAPTION_H   # 528

# ── Palette ──────────────────────────────────────────────────────────────────
WARM_CREAM    = (250, 240, 220)
SUNLIT_AMB    = (212, 146, 58)
SUNLIT_DIM    = (180, 120, 50)
VOID_BLACK    = (10, 10, 20)
ELEC_CYAN     = (0, 212, 232)
ELEC_CYAN_DIM = (0, 100, 120)
ELEC_CYAN_FD  = (0, 60, 80)
HOT_MAGENTA   = (232, 0, 152)
LUMA_HOODIE   = (232, 112, 58)   # canonical orange
LUMA_SKIN     = (218, 172, 128)
LUMA_SKIN_SH  = (175, 128, 88)
LUMA_HAIR     = (38, 22, 14)
LUMA_HAIR_HL  = (61, 31, 15)
LUMA_PANTS    = (70, 80, 110)
FLOOR_WARM    = (155, 128, 92)
FLOOR_GRAIN   = (130, 108, 76)
WALL_WARM     = (190, 170, 138)
CRT_BG        = (32, 42, 32)
CRT_STATIC    = (56, 70, 56)
CRT_BEZEL     = (50, 45, 40)
BYTE_TEAL     = (0, 212, 232)
BYTE_DARK     = (8, 40, 50)
DEEP_SPACE    = (6, 4, 14)
DESAT_RING    = (200, 195, 190)
LINE          = (59, 40, 32)
LINE_THIN     = (80, 55, 40)

# Caption
BG_CAPTION    = (12, 8, 6)
TEXT_SHOT     = (232, 224, 204)
TEXT_DESC     = (155, 148, 122)
TEXT_META     = (88, 82, 66)
ARC_COLOR     = ELEC_CYAN
ANN_COLOR     = (220, 200, 80)
ANN_CYAN      = (0, 180, 210)
ANN_DIM       = (80, 90, 100)

RNG = random.Random(1717)

# ── Geometry Helpers (from Maya Santos construction prototype) ────────────────

def bezier3(p0, p1, p2, steps=48):
    """Quadratic bezier, returns list of (x,y) tuples."""
    pts = []
    for i in range(steps + 1):
        t = i / steps
        x = (1-t)**2 * p0[0] + 2*(1-t)*t * p1[0] + t**2 * p2[0]
        y = (1-t)**2 * p0[1] + 2*(1-t)*t * p1[1] + t**2 * p2[1]
        pts.append((x, y))
    return pts


def bezier4(p0, p1, p2, p3, steps=60):
    """Cubic bezier for smoother S-curves."""
    pts = []
    for i in range(steps + 1):
        t = i / steps
        x = ((1-t)**3 * p0[0] + 3*(1-t)**2*t * p1[0] +
             3*(1-t)*t**2 * p2[0] + t**3 * p3[0])
        y = ((1-t)**3 * p0[1] + 3*(1-t)**2*t * p1[1] +
             3*(1-t)*t**2 * p2[1] + t**3 * p3[1])
        pts.append((x, y))
    return pts


def ellipse_points(cx, cy, rx, ry, steps=64, a0=0, a1=360):
    """Generate points along an elliptical arc."""
    pts = []
    for i in range(steps + 1):
        angle = math.radians(a0 + (a1 - a0) * i / steps)
        pts.append((cx + rx * math.cos(angle), cy + ry * math.sin(angle)))
    return pts


def polyline(draw, pts, color, width=2):
    for i in range(len(pts) - 1):
        draw.line([pts[i], pts[i+1]], fill=color, width=width)


def smooth_polygon(draw, pts, fill=None, outline=None, width=1):
    """Draw a filled polygon from a list of points, then optional outline."""
    if fill:
        draw.polygon(pts, fill=fill)
    if outline:
        polyline(draw, pts + [pts[0]], outline, width)


def tube_polygon(centerline, w_start, w_end):
    """Build a filled polygon from a centerline with tapering width."""
    n = len(centerline)
    if n < 2:
        return centerline
    left_edge = []
    right_edge = []
    for i in range(n):
        t = i / max(1, n - 1)
        w = w_start + (w_end - w_start) * t
        if i == 0:
            dx = centerline[1][0] - centerline[0][0]
            dy = centerline[1][1] - centerline[0][1]
        elif i == n - 1:
            dx = centerline[-1][0] - centerline[-2][0]
            dy = centerline[-1][1] - centerline[-2][1]
        else:
            dx = centerline[i+1][0] - centerline[i-1][0]
            dy = centerline[i+1][1] - centerline[i-1][1]
        length = math.sqrt(dx*dx + dy*dy) or 1.0
        nx = -dy / length
        ny = dx / length
        left_edge.append((centerline[i][0] + nx * w, centerline[i][1] + ny * w))
        right_edge.append((centerline[i][0] - nx * w, centerline[i][1] - ny * w))
    return left_edge + right_edge[::-1]


def load_font(size=14, bold=False):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()


def lerp_color(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def add_glow(img, cx, cy, r_max, color_rgb, steps=6, max_alpha=50):
    """Additive alpha composite glow."""
    for i in range(steps, 0, -1):
        r     = int(r_max * (i / steps))
        alpha = int(max_alpha * (1 - (i / steps) * 0.6))
        glow  = Image.new('RGBA', img.size, (0, 0, 0, 0))
        gd    = ImageDraw.Draw(glow)
        gd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(*color_rgb, alpha))
        base  = img.convert('RGBA')
        img.paste(Image.alpha_composite(base, glow).convert('RGB'))


def draw_irregular_poly(draw, cx, cy, r, sides, color, rng, fill=True):
    """Draw a slightly irregular polygon for Glitchkin pixels."""
    pts = []
    for i in range(sides):
        angle = (2 * math.pi * i / sides) + rng.uniform(-0.2, 0.2)
        rr    = r * rng.uniform(0.72, 1.0)
        pts.append((int(cx + rr * math.cos(angle)),
                    int(cy + rr * math.sin(angle))))
    if fill:
        draw.polygon(pts, fill=color)
    else:
        draw.polygon(pts, outline=color)


# ══════════════════════════════════════════════════════════════════════════════
# IMPROVED CHARACTER DRAWING — ORGANIC CURVES
# ══════════════════════════════════════════════════════════════════════════════

def draw_luma_sitting(draw, img, luma_cx, luma_floor_y):
    """
    Draw Luma sitting cross-legged with IMPROVED organic curve construction.

    Key improvements over original:
    - Head = 37% of visible character height (was ~25%)
    - Organic bezier torso (bean shape, not rectangle)
    - Gesture line: slight forward lean (assessing posture)
    - Asymmetric messy hair with volume and overlap
    - Tapered arms as tube polygons
    - Mitten hands
    - Larger eyes (30-35% of head width)
    """
    # Character proportions at sitting scale
    # Visible height from top of hair to floor: ~140px
    visible_h = 140
    head_h = int(visible_h * 0.37)  # ~52px
    head_r = head_h // 2  # ~26px

    # Gesture line: slight forward lean (3-4 degrees toward Byte = camera-right)
    lean_dx = 6  # pixels of forward lean at head

    # Head center — HIGHER and LARGER than original
    head_cy = luma_floor_y - 104
    head_cx = luma_cx + lean_dx

    # ── Cross-legged base (legs folded) ──
    leg_w = 62
    leg_h = 26
    # Use bezier curves for leg shapes instead of flat polygon
    left_leg = bezier3(
        (luma_cx - leg_w, luma_floor_y),
        (luma_cx - leg_w // 2, luma_floor_y - 12),
        (luma_cx, luma_floor_y - 6),
        steps=24
    )
    right_leg = bezier3(
        (luma_cx, luma_floor_y - 6),
        (luma_cx + leg_w // 2, luma_floor_y - 12),
        (luma_cx + leg_w, luma_floor_y),
        steps=24
    )
    # Build leg polygon with bottom curve
    leg_bottom = bezier3(
        (luma_cx + leg_w, luma_floor_y),
        (luma_cx, luma_floor_y + leg_h - 4),
        (luma_cx - leg_w, luma_floor_y),
        steps=24
    )
    leg_poly = left_leg + right_leg + leg_bottom
    smooth_polygon(draw, leg_poly, fill=LUMA_PANTS, outline=LINE, width=2)

    # Shoes (tips of feet poking out) — rounded
    for shoe_x in [luma_cx - leg_w - 4, luma_cx + leg_w + 4]:
        shoe_pts = ellipse_points(shoe_x, luma_floor_y, 10, 6)
        smooth_polygon(draw, shoe_pts, fill=(42, 36, 30), outline=LINE_THIN, width=1)

    # ── Torso — ORGANIC BEAN SHAPE (not rectangle) ──
    # Tapered: wider at shoulders, narrower at waist/hips
    torso_top_y = luma_floor_y - 86
    torso_bot_y = luma_floor_y + 2
    shoulder_w = 48
    waist_w = 38

    # Build torso as bezier-outlined organic shape with gesture lean
    # Left side (convex outward curve)
    torso_left = bezier4(
        (head_cx - shoulder_w, torso_top_y),
        (head_cx - shoulder_w - 4, torso_top_y + (torso_bot_y - torso_top_y) * 0.3),
        (luma_cx - waist_w - 2, torso_top_y + (torso_bot_y - torso_top_y) * 0.6),
        (luma_cx - waist_w + 2, torso_bot_y),
        steps=32
    )
    # Right side (convex outward curve)
    torso_right = bezier4(
        (luma_cx + waist_w - 2, torso_bot_y),
        (luma_cx + waist_w + 2, torso_top_y + (torso_bot_y - torso_top_y) * 0.6),
        (head_cx + shoulder_w + 4, torso_top_y + (torso_bot_y - torso_top_y) * 0.3),
        (head_cx + shoulder_w, torso_top_y),
        steps=32
    )
    # Top edge (shoulder line — slight curve)
    torso_top = bezier3(
        (head_cx + shoulder_w, torso_top_y),
        (head_cx, torso_top_y - 4),  # slight upward curve
        (head_cx - shoulder_w, torso_top_y),
        steps=16
    )
    torso_poly = torso_left + torso_right + torso_top
    smooth_polygon(draw, torso_poly, fill=LUMA_HOODIE, outline=LINE, width=2)

    # Hoodie collar — V-neck shape
    collar_pts = [
        (head_cx - 14, torso_top_y + 2),
        (head_cx, torso_top_y + 16),
        (head_cx + 14, torso_top_y + 2),
    ]
    draw.polygon(collar_pts, fill=(250, 232, 200))
    polyline(draw, collar_pts, LINE_THIN, width=1)

    # Hoodie hem line (slightly curved)
    hem_pts = bezier3(
        (luma_cx - waist_w + 4, torso_bot_y - 4),
        (luma_cx, torso_bot_y - 8),
        (luma_cx + waist_w - 4, torso_bot_y - 4),
        steps=16
    )
    polyline(draw, hem_pts, LINE_THIN, width=1)

    # Wrinkle lines at waist (minimal fabric detail)
    for wx, wy in [(head_cx - 18, torso_top_y + 40), (head_cx + 12, torso_top_y + 38)]:
        wrinkle = bezier3((wx - 8, wy), (wx, wy - 3), (wx + 8, wy + 1), steps=8)
        polyline(draw, wrinkle, LINE_THIN, width=1)

    # ── Arms — tapered tube polygons, crossed loosely in lap ──
    # Left arm: from left shoulder, curves across to right lap
    la_centerline = bezier4(
        (head_cx - shoulder_w + 6, torso_top_y + 12),    # shoulder
        (head_cx - shoulder_w - 8, torso_top_y + 38),    # elbow out
        (luma_cx - 10, luma_floor_y - 28),               # forearm curves in
        (luma_cx + 18, luma_floor_y - 16),               # hand in lap
        steps=24
    )
    la_poly = tube_polygon(la_centerline, 11, 7)  # tapers from shoulder to wrist
    smooth_polygon(draw, la_poly, fill=LUMA_HOODIE, outline=LINE, width=2)

    # Left hand (mitten shape)
    lh_x, lh_y = int(luma_cx + 18), int(luma_floor_y - 16)
    hand_pts = ellipse_points(lh_x, lh_y, 8, 6)
    smooth_polygon(draw, hand_pts, fill=LUMA_SKIN, outline=LINE_THIN, width=1)
    # Thumb bump
    draw.ellipse([lh_x + 4, lh_y - 6, lh_x + 10, lh_y], fill=LUMA_SKIN)

    # Right arm: from right shoulder, rests on right knee area
    ra_centerline = bezier4(
        (head_cx + shoulder_w - 6, torso_top_y + 12),    # shoulder
        (head_cx + shoulder_w + 6, torso_top_y + 36),    # elbow out slightly
        (luma_cx + 30, luma_floor_y - 26),               # forearm
        (luma_cx + leg_w - 12, luma_floor_y - 10),       # hand on knee
        steps=24
    )
    ra_poly = tube_polygon(ra_centerline, 11, 7)
    smooth_polygon(draw, ra_poly, fill=LUMA_HOODIE, outline=LINE, width=2)

    # Right hand
    rh_x, rh_y = int(luma_cx + leg_w - 12), int(luma_floor_y - 10)
    hand_pts = ellipse_points(rh_x, rh_y, 8, 6)
    smooth_polygon(draw, hand_pts, fill=LUMA_SKIN, outline=LINE_THIN, width=1)
    draw.ellipse([rh_x + 4, rh_y - 5, rh_x + 10, rh_y + 1], fill=LUMA_SKIN)

    # ── Neck — short, slightly angled with lean ──
    neck_pts = [
        (head_cx - 10, torso_top_y + 2),
        (head_cx + 10, torso_top_y + 2),
        (head_cx + 8, head_cy + head_r - 2),
        (head_cx - 8, head_cy + head_r - 2),
    ]
    draw.polygon(neck_pts, fill=LUMA_SKIN)

    # ── Head — LARGER, organic circle ──
    # Slightly taller than wide (oval, not perfect circle)
    head_pts = ellipse_points(head_cx, head_cy, head_r, int(head_r * 1.05))
    smooth_polygon(draw, head_pts, fill=LUMA_SKIN, outline=LINE, width=2)

    # ── Face — 3/4 toward camera-right (toward Byte) ──
    # EXPRESSION: ASSESSING — level eyes, slightly set brow, closed neutral mouth

    # Eyes — LARGER (30-35% of head width = ~16-18px wide)
    eye_size = int(head_r * 0.65)  # ~17px diameter per eye
    eye_h = int(eye_size * 0.65)   # slightly taller than wide for expression range

    # Right eye (facing Byte — primary visible eye at 3/4)
    re_cx = head_cx + int(head_r * 0.28)
    re_cy = head_cy - int(head_r * 0.08)
    # Eye white — organic shape (not circle)
    re_pts = ellipse_points(re_cx, re_cy, eye_size // 2, eye_h // 2)
    smooth_polygon(draw, re_pts, fill=(245, 238, 228), outline=LINE, width=2)
    # Iris — large, takes up most of eye
    ir_r = int(eye_size * 0.35)
    ir_cx = re_cx + int(ir_r * 0.30)  # looking slightly toward Byte
    draw.ellipse([ir_cx - ir_r, re_cy - ir_r, ir_cx + ir_r, re_cy + ir_r],
                 fill=(130, 78, 40))
    # Pupil
    pr = int(ir_r * 0.55)
    draw.ellipse([ir_cx - pr, re_cy - pr, ir_cx + pr, re_cy + pr],
                 fill=VOID_BLACK)
    # Highlight
    draw.ellipse([ir_cx - pr + 2, re_cy - pr + 1, ir_cx - pr + 5, re_cy - pr + 4],
                 fill=(255, 255, 255))
    # Upper eyelid — SHAPED (slightly lowered = ASSESSING, not fully open)
    lid_pts = bezier3(
        (re_cx - eye_size // 2 - 1, re_cy - 1),
        (re_cx, re_cy - eye_h // 2 + 2),  # lid drops 2px = assessing squint
        (re_cx + eye_size // 2 + 1, re_cy - 1),
        steps=16
    )
    polyline(draw, lid_pts, LINE, width=2)

    # Left eye (partially visible at 3/4 — narrower)
    le_cx = head_cx - int(head_r * 0.18)
    le_cy = head_cy - int(head_r * 0.06)
    le_size = int(eye_size * 0.65)  # narrower at 3/4
    le_h = int(eye_h * 0.65)
    le_pts = ellipse_points(le_cx, le_cy, le_size // 2, le_h // 2)
    smooth_polygon(draw, le_pts, fill=(245, 238, 228), outline=LINE, width=1)
    # Left iris
    lir_r = int(le_size * 0.35)
    draw.ellipse([le_cx - lir_r, le_cy - lir_r, le_cx + lir_r, le_cy + lir_r],
                 fill=(130, 78, 40))
    draw.ellipse([le_cx - lir_r + 2, le_cy - lir_r + 2,
                  le_cx + lir_r - 2, le_cy + lir_r - 2],
                 fill=VOID_BLACK)

    # Brows — CURVED, not straight lines. Slightly set (assessing)
    # Right brow: slight lowering at outer edge (concentrating)
    rbrow = bezier3(
        (re_cx - eye_size // 2, re_cy - eye_h // 2 - 6),
        (re_cx, re_cy - eye_h // 2 - 10),  # apex higher
        (re_cx + eye_size // 2 + 2, re_cy - eye_h // 2 - 4),  # drops at outer
        steps=12
    )
    polyline(draw, rbrow, (42, 22, 10), width=3)

    # Left brow: matching curve at 3/4
    lbrow = bezier3(
        (le_cx - le_size // 2 - 1, le_cy - le_h // 2 - 5),
        (le_cx, le_cy - le_h // 2 - 8),
        (le_cx + le_size // 2, le_cy - le_h // 2 - 4),
        steps=12
    )
    polyline(draw, lbrow, (42, 22, 10), width=2)

    # Nose — small bridge shape
    nose_pts = bezier3(
        (head_cx + 2, head_cy + int(head_r * 0.10)),
        (head_cx + 5, head_cy + int(head_r * 0.28)),
        (head_cx + 1, head_cy + int(head_r * 0.35)),
        steps=8
    )
    polyline(draw, nose_pts, LUMA_SKIN_SH, width=2)

    # Mouth — closed, neutral with slight asymmetry (thinking)
    mouth_y = head_cy + int(head_r * 0.52)
    mouth_pts = bezier3(
        (head_cx - 8, mouth_y + 1),
        (head_cx + 2, mouth_y - 2),  # slightly asymmetric
        (head_cx + 10, mouth_y),
        steps=12
    )
    polyline(draw, mouth_pts, (120, 72, 44), width=2)

    # ── Hair — ASYMMETRIC, MESSY, WITH VOLUME ──
    # Hair is drawn LAST to overlap the head boundary
    # This is the key silhouette differentiator for Luma

    # Base hair mass — irregular cloud that breaks the head circle
    hair_base_pts = []
    hair_angles = list(range(180, 540, 8))  # top half of head + overlap
    for ha in hair_angles:
        angle = math.radians(ha)
        # Vary radius to create messy asymmetric silhouette
        base_r = head_r + 14
        # LEFT side bigger (her characteristic messy side)
        if 200 < ha < 320:
            base_r += RNG.randint(4, 12)
        elif 320 < ha < 400:
            base_r += RNG.randint(2, 8)
        else:
            base_r += RNG.randint(0, 6)
        hx = head_cx + int(base_r * math.cos(angle))
        hy = head_cy + int(base_r * 0.95 * math.sin(angle))
        # Only draw hair above mouth level
        if hy < head_cy + int(head_r * 0.45):
            hair_base_pts.append((hx, hy))

    # Close the hair shape along the face edge
    hair_base_pts.append((head_cx + int(head_r * 0.9), head_cy + int(head_r * 0.4)))
    hair_base_pts.append((head_cx - int(head_r * 0.7), head_cy + int(head_r * 0.4)))

    if len(hair_base_pts) > 3:
        smooth_polygon(draw, hair_base_pts, fill=LUMA_HAIR)

    # Hair strands — individual spikes/wisps breaking the silhouette
    strand_angles = [195, 215, 240, 260, 280, 310, 340, 370, 395, 420, 450]
    for sa in strand_angles:
        angle = math.radians(sa)
        base_r = head_r + 10
        strand_len = RNG.randint(12, 24)
        strand_w = RNG.choice([2, 3, 3, 4])
        sx = head_cx + int(base_r * math.cos(angle))
        sy = head_cy + int(base_r * 0.90 * math.sin(angle))
        ex = head_cx + int((base_r + strand_len) * math.cos(angle + RNG.uniform(-0.15, 0.15)))
        ey = head_cy + int((base_r + strand_len) * 0.90 * math.sin(angle + RNG.uniform(-0.15, 0.15)))
        if sy < head_cy + int(head_r * 0.3):
            draw.line([(sx, sy), (ex, ey)], fill=LUMA_HAIR, width=strand_w)

    # Hair highlight strand (lighter, shows volume)
    for ha in [240, 280, 350]:
        angle = math.radians(ha)
        r_inner = head_r + 6
        r_outer = head_r + 14
        hx1 = head_cx + int(r_inner * math.cos(angle))
        hy1 = head_cy + int(r_inner * 0.90 * math.sin(angle))
        hx2 = head_cx + int(r_outer * math.cos(angle + 0.08))
        hy2 = head_cy + int(r_outer * 0.90 * math.sin(angle + 0.08))
        if hy1 < head_cy + int(head_r * 0.2):
            draw.line([(hx1, hy1), (hx2, hy2)], fill=LUMA_HAIR_HL, width=2)

    # ── Blush (subtle, under eyes) ──
    blush_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    bd = ImageDraw.Draw(blush_layer)
    for boff in [int(head_r * 0.35), -int(head_r * 0.15)]:
        bx = head_cx + boff
        by = head_cy + int(head_r * 0.15)
        bd.ellipse([bx - 10, by - 5, bx + 10, by + 5],
                   fill=(232, 148, 100, 50))
    img.paste(Image.alpha_composite(img.convert('RGBA'), blush_layer).convert('RGB'))
    return ImageDraw.Draw(img)  # refresh draw context after paste


def draw_byte_hovering(draw, img, byte_cx, byte_cy, body_h, body_w):
    """
    Draw Byte hovering with SLIGHT IMPROVEMENTS.

    Byte's design already works (audit: PASS for identity). Changes:
    - Slight forward lean toward the chip (curiosity in body language)
    - Arms as curved shapes, not rectangles
    - Subtle body tilt (2-3 degrees)
    """
    # Slight forward lean (toward chip = camera-left)
    lean_dx = -4
    body_cx = byte_cx + lean_dx
    body_top_y = byte_cy - body_h // 2

    # Body fill — teardrop with lean
    # Top half: ellipse
    draw.ellipse([body_cx - body_w // 2, body_top_y,
                  body_cx + body_w // 2, byte_cy + body_h // 4],
                 fill=BYTE_TEAL)
    # Bottom half: tapered triangle
    draw.polygon([
        (body_cx - body_w // 2, byte_cy + body_h // 8),
        (body_cx, byte_cy + body_h // 2),
        (body_cx + body_w // 2, byte_cy + body_h // 8),
    ], fill=BYTE_TEAL)

    # Body shadow (left/cool side)
    draw.ellipse([body_cx - body_w // 2, body_top_y,
                  body_cx, byte_cy + body_h // 4],
                 fill=BYTE_DARK)

    # ── Face: 3/4 toward Luma — STILL expression ──
    face_cx = body_cx - int(body_w * 0.08)
    face_cy = body_top_y + int(body_h * 0.25)
    face_r  = int(body_w * 0.45)

    draw.ellipse([face_cx - face_r, face_cy - face_r,
                  face_cx + face_r, face_cy + face_r],
                 fill=BYTE_TEAL)

    # Normal eye (toward Luma)
    ne_cx = face_cx - int(face_r * 0.35)
    ne_cy = face_cy - int(face_r * 0.18)
    ne_r  = int(face_r * 0.30)
    draw.ellipse([ne_cx - ne_r, ne_cy - ne_r, ne_cx + ne_r, ne_cy + ne_r],
                 fill=(8, 8, 18))
    DEEP_CYAN = (0, 155, 175)
    draw.ellipse([ne_cx - ne_r + 3, ne_cy - ne_r + 3,
                  ne_cx + ne_r - 3, ne_cy + ne_r - 3],
                 fill=DEEP_CYAN)
    iris_shift_x = -int(ne_r * 0.30)
    draw.ellipse([ne_cx + iris_shift_x - 5, ne_cy - 5,
                  ne_cx + iris_shift_x + 5, ne_cy + 5],
                 fill=VOID_BLACK)

    # Cracked eye (outward)
    ce_cx = face_cx + int(face_r * 0.32)
    ce_cy = face_cy - int(face_r * 0.18)
    ce_r  = int(face_r * 0.28)
    draw.ellipse([ce_cx - ce_r, ce_cy - ce_r, ce_cx + ce_r, ce_cy + ce_r],
                 fill=(8, 8, 18))
    for crack_ang in [30, 70, 120, 160]:
        ca = math.radians(crack_ang)
        draw.line([(int(ce_cx + ce_r * 0.2 * math.cos(ca)),
                    int(ce_cy + ce_r * 0.2 * math.sin(ca))),
                   (int(ce_cx + ce_r * 0.9 * math.cos(ca)),
                    int(ce_cy + ce_r * 0.9 * math.sin(ca)))],
                  fill=HOT_MAGENTA, width=1)
    div_x = -int(ce_r * 0.20)
    draw.ellipse([ce_cx + div_x - 3, ce_cy - 3,
                  ce_cx + div_x + 3, ce_cy + 3],
                 fill=ELEC_CYAN)

    # Mouth — neutral, slight pixel grimace
    mouth_y = face_cy + int(face_r * 0.40)
    mouth_w = int(face_r * 0.60)
    draw.rectangle([face_cx - mouth_w, mouth_y - 2,
                    face_cx + mouth_w, mouth_y + 2],
                   fill=VOID_BLACK)
    for mx_tooth in range(face_cx - mouth_w + 2, face_cx + mouth_w - 2, 5):
        draw.point((mx_tooth, mouth_y), fill=(200, 200, 210))

    # Arms — CURVED tube shapes, not rectangles
    arm_top_y = body_top_y + int(body_h * 0.35)

    # Left arm: slight curve hanging down (not rectangular)
    la_center = bezier3(
        (body_cx - body_w // 2 - 2, arm_top_y),
        (body_cx - body_w // 2 - 10, arm_top_y + int(body_h * 0.14)),
        (body_cx - body_w // 2 - 4, arm_top_y + int(body_h * 0.22)),
        steps=12
    )
    la_poly = tube_polygon(la_center, 6, 4)
    smooth_polygon(draw, la_poly, fill=BYTE_TEAL)

    # Right arm: similar curve
    ra_center = bezier3(
        (body_cx + body_w // 2 + 2, arm_top_y),
        (body_cx + body_w // 2 + 10, arm_top_y + int(body_h * 0.14)),
        (body_cx + body_w // 2 + 4, arm_top_y + int(body_h * 0.22)),
        steps=12
    )
    ra_poly = tube_polygon(ra_center, 6, 4)
    smooth_polygon(draw, ra_poly, fill=BYTE_TEAL)

    # Legs — short stubs with slight curve
    leg_top_y = byte_cy + int(body_h * 0.35)
    for leg_off in [-10, 10]:
        leg_center = bezier3(
            (body_cx + leg_off, leg_top_y),
            (body_cx + leg_off - 1, leg_top_y + int(body_h * 0.12)),
            (body_cx + leg_off, leg_top_y + int(body_h * 0.22)),
            steps=8
        )
        leg_poly = tube_polygon(leg_center, 7, 5)
        smooth_polygon(draw, leg_poly, fill=BYTE_TEAL)

    return face_cy, face_r, body_cx, body_w


def draw_panel():
    img  = Image.new('RGB', (PW, PH), WALL_WARM)
    draw = ImageDraw.Draw(img)

    # ── Background: den room — restoring to calm ──────────────────────────────
    # (IDENTICAL to original P17)
    wall_h = int(DRAW_H * 0.38)
    floor_y = wall_h

    for x in range(PW):
        t = x / PW
        c = lerp_color(WALL_WARM, (130, 148, 148), t * 0.55)
        draw.line([(x, 0), (x, wall_h)], fill=c)

    for x in range(PW):
        t = x / PW
        c = lerp_color(FLOOR_WARM, (130, 135, 128), t * 0.35)
        draw.line([(x, floor_y), (x, DRAW_H)], fill=c)

    for py in range(floor_y, DRAW_H, 24):
        draw.line([(0, py), (PW, py)], fill=FLOOR_GRAIN, width=1)

    # CRT Monitors
    mon_specs = [
        (int(PW * 0.60), int(DRAW_H * 0.05), int(PW * 0.24), int(DRAW_H * 0.26)),
        (int(PW * 0.86), int(DRAW_H * 0.08), int(PW * 0.12), int(DRAW_H * 0.22)),
    ]
    for mx, my, mw, mh in mon_specs:
        draw.rectangle([mx, my, mx + mw, my + mh], fill=CRT_BEZEL)
        screen_pad = 6
        draw.rectangle([mx + screen_pad, my + screen_pad,
                         mx + mw - screen_pad, my + mh - screen_pad],
                        fill=CRT_BG)
        for _ in range(60):
            sx = RNG.randint(mx + screen_pad + 2, mx + mw - screen_pad - 2)
            sy = RNG.randint(my + screen_pad + 2, my + mh - screen_pad - 2)
            draw.point((sx, sy), fill=CRT_STATIC)

    # Warm lamp glow
    add_glow(img, -20, int(DRAW_H * 0.20), int(PW * 0.55),
             SUNLIT_AMB, steps=10, max_alpha=18)
    draw = ImageDraw.Draw(img)

    # ── LUMA — sitting cross-legged, camera-left ──────────────────────────────
    luma_floor_y = floor_y + int((DRAW_H - floor_y) * 0.82)
    luma_cx      = int(PW * 0.24)

    # IMPROVED character drawing
    draw = draw_luma_sitting(draw, img, luma_cx, luma_floor_y)

    # ── BYTE — hovering camera-right ──────────────────────────────────────────
    byte_cx = int(PW * 0.76)
    byte_cy = int(DRAW_H * 0.52)

    # Pixel trails (fading ghost wisps)
    for t_step in range(4):
        t    = t_step / 5.0
        ghost_x = int(byte_cx + (1 - t) * 80 * math.cos(math.radians(130)))
        ghost_y = int(byte_cy + (1 - t) * 60 * math.sin(math.radians(130)))
        ghost_r = int(18 * (1 - t * 0.7))
        ghost_a = int(35 * (1 - t))
        glow  = Image.new('RGBA', img.size, (0, 0, 0, 0))
        gd    = ImageDraw.Draw(glow)
        gd.ellipse([ghost_x - ghost_r, ghost_y - ghost_r,
                    ghost_x + ghost_r, ghost_y + ghost_r],
                   fill=(*ELEC_CYAN_FD, ghost_a))
        img.paste(Image.alpha_composite(img.convert('RGBA'), glow).convert('RGB'))
    draw = ImageDraw.Draw(img)

    # Desaturation ring
    desat_floor_y = floor_y + int((DRAW_H - floor_y) * 0.88)
    draw.ellipse([byte_cx - 38, desat_floor_y - 10,
                  byte_cx + 38, desat_floor_y + 10],
                 outline=DESAT_RING, width=2)

    # IMPROVED Byte drawing
    body_h = int((DRAW_H - floor_y) * 0.42)
    body_w = int(body_h * 0.72)
    face_cy, face_r, body_cx, _ = draw_byte_hovering(
        draw, img, byte_cx, byte_cy, body_h, body_w
    )

    # Byte glow
    add_glow(img, byte_cx, byte_cy, int(body_w * 2.2), ELEC_CYAN,
             steps=8, max_alpha=22)
    draw = ImageDraw.Draw(img)

    # ── Falling pixel chip ────────────────────────────────────────────────────
    chip_x = int(PW * 0.50)
    chip_y = int(DRAW_H * 0.55)
    chip_sz = 7
    draw.rectangle([chip_x - chip_sz, chip_y - chip_sz,
                    chip_x + chip_sz, chip_y + chip_sz],
                   fill=ELEC_CYAN)
    draw.rectangle([chip_x - chip_sz + 1, chip_y - chip_sz + 1,
                    chip_x + chip_sz - 1, chip_y + chip_sz - 1],
                   outline=VOID_BLACK, width=1)

    for dy in range(0, 40, 6):
        draw.point((chip_x, chip_y - chip_sz - 4 - dy), fill=ELEC_CYAN_DIM)

    # ── Annotations ──────────────────────────────────────────────────────────
    font_ann  = load_font(9,  bold=False)
    font_ann_b= load_font(9,  bold=True)
    font_sm   = load_font(8,  bold=False)

    draw.text((8, 8), 'MED  |  4-5FT  |  FLAT HORIZON  |  BEAT OF STILLNESS',
              font=font_ann, fill=ANN_COLOR)

    # Chip
    draw.text((chip_x + chip_sz + 6, chip_y - 6), '"soft tick"',
              font=font_ann_b, fill=ANN_CYAN)
    draw.text((chip_x + chip_sz + 6, chip_y + 6), "only thing moving",
              font=font_sm, fill=ANN_DIM)

    # Character annotations
    luma_head_cy = luma_floor_y - 104
    draw.text((luma_cx - 35, luma_head_cy - 50),
              "ASSESSING", font=font_ann_b, fill=ANN_COLOR)
    draw.text((luma_cx - 30, luma_head_cy - 40),
              "(fear gone, processing)", font=font_sm, fill=(130, 120, 100))

    draw.text((byte_cx + body_w // 2 + 10, face_cy - 10),
              "STILL", font=font_ann_b, fill=ANN_CYAN)
    draw.text((byte_cx + body_w // 2 + 10, face_cy + 2),
              "(mirror of Luma's beat)", font=font_sm, fill=ANN_DIM)

    draw.text((int(PW * 0.58), int(DRAW_H * 0.15)),
              "trail fading", font=font_sm, fill=ELEC_CYAN_DIM)
    draw.text((int(PW * 0.58), int(DRAW_H * 0.15) + 10),
              "(last wisps)", font=font_sm, fill=ELEC_CYAN_DIM)

    draw.text((byte_cx + 42, desat_floor_y - 5),
              "desat ring", font=font_sm, fill=(160, 155, 150))

    draw.text((int(PW * 0.08), DRAW_H - 16),
              "WARM (Luma zone)", font=font_sm, fill=(180, 130, 60))
    draw.text((int(PW * 0.68), DRAW_H - 16),
              "COOL (Byte zone)", font=font_sm, fill=ELEC_CYAN_DIM)

    gap_label_x = int(PW * 0.42)
    gap_label_y = int(DRAW_H * 0.75)
    draw.text((gap_label_x - 24, gap_label_y), "NEGATIVE SPACE",
              font=font_sm, fill=(100, 96, 88))
    draw.text((gap_label_x - 16, gap_label_y + 10), "(their distance)",
              font=font_sm, fill=(80, 76, 70))

    # Character quality test label
    draw.text((8, DRAW_H - 28), "CHARACTER QUALITY PROTOTYPE — C50",
              font=font_ann_b, fill=(200, 180, 100))

    # ── Three-tier caption bar ────────────────────────────────────────────────
    font_t1   = load_font(13, bold=True)
    font_t2   = load_font(11, bold=False)
    font_t3   = load_font(9,  bold=False)
    font_meta = load_font(8,  bold=False)

    draw.rectangle([0, DRAW_H, PW, PH], fill=BG_CAPTION)
    draw.line([0, DRAW_H, PW, DRAW_H], fill=(8, 6, 4), width=2)

    draw.text((10, DRAW_H + 4),
              "P17  |  MED  |  4-5FT  |  BEAT OF STILLNESS  |  CHIP FALLS",
              font=font_t1, fill=TEXT_SHOT)

    draw.text((PW - 260, DRAW_H + 5),
              "ARC: CURIOUS / FIRST ENCOUNTER", font=font_t2, fill=ELEC_CYAN)

    draw.text((10, DRAW_H + 22),
              "Luma sitting cross-legged. Byte hovering across room. Trails fading. Everything stops.",
              font=font_t3, fill=TEXT_DESC)
    draw.text((10, DRAW_H + 35),
              "One pixel chip falls between them. \"Soft tick.\" This cracks the standoff.",
              font=font_t3, fill=(120, 112, 90))

    draw.text((PW - 310, DRAW_H + 56),
              "LTG_SB_cold_open_P17_chartest  /  Diego Vargas  /  C50",
              font=font_meta, fill=TEXT_META)

    # Arc border
    draw.rectangle([0, 0, PW - 1, PH - 1], outline=ARC_COLOR, width=4)

    img.thumbnail((1280, 1280))
    img.save(str(OUTPUT_PATH), "PNG")
    print(f"Saved: {OUTPUT_PATH}  {img.size}")
    return str(OUTPUT_PATH)


if __name__ == "__main__":
    draw_panel()
    print("P17 CHARACTER QUALITY PROTOTYPE complete.")
    print("Compare with original: LTG_SB_cold_open_P17.png")
