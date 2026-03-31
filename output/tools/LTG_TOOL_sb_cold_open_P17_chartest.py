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
from LTG_TOOL_curve_utils import quadratic_bezier_pts as _cu_quadratic, cubic_bezier_pts as _cu_cubic
import math, random, os
import sys
from LTG_TOOL_char_luma import draw_luma
from LTG_TOOL_char_byte import draw_byte
from LTG_TOOL_cairo_primitives import to_pil_rgba
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

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
    """Delegates to curve_utils.quadratic_bezier_pts."""
    return _cu_quadratic(p0, p1, p2, steps=steps)


def bezier4(p0, p1, p2, p3, steps=60):
    """Delegates to curve_utils.cubic_bezier_pts."""
    return _cu_cubic(p0, p1, p2, p3, steps=steps)


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






def _char_to_pil(surface):
    """Convert a cairo.ImageSurface from canonical char module to cropped PIL RGBA."""
    from LTG_TOOL_cairo_primitives import to_pil_rgba
    pil_img = to_pil_rgba(surface)
    bbox = pil_img.getbbox()
    if bbox:
        pil_img = pil_img.crop(bbox)
    return pil_img


def _composite_char(base_img, char_pil, cx, cy):
    """Composite a character PIL RGBA image onto base_img centered at (cx, cy)."""
    x = cx - char_pil.width // 2
    y = cy - char_pil.height // 2
    overlay = Image.new('RGBA', base_img.size, (0, 0, 0, 0))
    overlay.paste(char_pil, (x, y), char_pil)
    base_rgba = base_img.convert('RGBA')
    result = Image.alpha_composite(base_rgba, overlay)
    base_img.paste(result.convert('RGB'))

def draw_luma_sitting(draw, img, luma_cx, luma_floor_y):
    """Luma sitting — canonical renderer (CURIOUS expression)."""
    scale = 0.5
    surface = draw_luma(expression="CURIOUS", scale=scale, facing="right")
    char_pil = _char_to_pil(surface)
    if char_pil.height > 0:
        target_h = int(luma_floor_y * 0.35)
        aspect = char_pil.width / char_pil.height
        new_w = int(target_h * aspect)
        char_pil = char_pil.resize((new_w, target_h), Image.LANCZOS)
    _composite_char(img, char_pil, luma_cx, luma_floor_y - char_pil.height // 2)


def draw_byte_hovering(draw, img, byte_cx, byte_cy, body_h, body_w):
    """Byte hovering — canonical renderer (neutral expression).

    Returns (face_cy, face_r, body_cx, body_w) for annotation placement.
    """
    scale = body_h / 88.0
    surface = draw_byte(expression="neutral", scale=scale, facing="front")
    char_pil = _char_to_pil(surface)
    if char_pil.height > 0:
        aspect = char_pil.width / char_pil.height
        new_h = body_h
        new_w = int(new_h * aspect)
        char_pil = char_pil.resize((new_w, new_h), Image.LANCZOS)
    _composite_char(img, char_pil, byte_cx, byte_cy)
    # Return approximate geometry for annotation placement
    face_cy = byte_cy - body_h // 4
    face_r = int(body_h * 0.25)
    return (face_cy, face_r, byte_cx, body_w)


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
