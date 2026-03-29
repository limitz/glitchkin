#!/usr/bin/env python3
"""
LTG_TOOL_luma_expression_sheet_v002.py
Luma Expression Sheet — Refined v002
"Luma & the Glitchkin" — Cycle 17 Refinement Pass

REPLACES previous v002 (Cycle 12, 4x2, 8 expressions).
This is the Cycle 17 dedicated refinement: 3x2 grid, 6 core expressions,
construction guide marks visible, varied line weight.

6 expressions: CURIOUS, DETERMINED, SURPRISED, WORRIED, DELIGHTED, FRUSTRATED
Layout: 3x2 grid
Canvas: 1200x900

Design principles:
  - Visible construction circle as head base (faint guide overlay)
  - Varied line weight: ~4px silhouette (8px at 2x render), ~2px interior (4px at 2x)
  - Clear shape language — hair is key silhouette element
  - Each expression reads at 200px thumbnail scale
  - Luma: 12yo, spirited, round face, shoulder-length hair with choppy fringe,
           large expressive eyes, small nose

Color palette from luma.md canonical spec:
  SKIN     #C8885A  Warm Caramel
  HAIR     #1A0F0A  Near-Black Espresso
  EYE_W    #FAF0DC  Warm Cream
  EYE_IRIS #C87D3E  Warm Amber
  EYE_PUP  #3B2820  Deep Cocoa
  EYE_HL   #F0F0F0  Static White
  LINE     #3B2820  Deep Cocoa

Output: output/characters/main/LTG_CHAR_luma_expression_sheet_v002.png
"""

from PIL import Image, ImageDraw, ImageFont
import math
import os

# -- Palette ------------------------------------------------------------------
SKIN        = (200, 136, 90)
SKIN_SH     = (160, 104, 64)
SKIN_HL     = (223, 160, 112)
HAIR        = (26, 15, 10)
HAIR_HL     = (61, 31, 15)
EYE_W       = (250, 240, 220)
EYE_IRIS    = (200, 125, 62)
EYE_PUP     = (59, 40, 32)
EYE_HL      = (240, 240, 240)
BLUSH_C     = (232, 148, 100)
LINE        = (59, 40, 32)
HOODIE      = (232, 114, 42)
CANVAS_BG   = (28, 20, 14)

# Panel backgrounds per expression (distinct at thumbnail scale)
BG = {
    "CURIOUS":    (200, 225, 215),
    "DETERMINED": (215, 205, 190),
    "SURPRISED":  (240, 218, 175),
    "WORRIED":    (198, 215, 235),
    "DELIGHTED":  (250, 222, 192),
    "FRUSTRATED": (215, 198, 208),
}

# Hoodie tones per mood
HOODIE_MAP = {
    "CURIOUS":    (160, 185, 205),
    "DETERMINED": (155, 85, 45),
    "SURPRISED":  (232, 114, 42),
    "WORRIED":    (80, 100, 140),
    "DELIGHTED":  (232, 114, 42),
    "FRUSTRATED": (135, 75, 65),
}

# -- Layout -------------------------------------------------------------------
COLS    = 3
ROWS    = 2
PAD     = 20
HEADER  = 58
LABEL_H = 36
# Derived panel dimensions for 1200x900 canvas
PANEL_W = (1200 - PAD * (COLS + 1)) // COLS      # 380
PANEL_H = (900 - HEADER - PAD * (ROWS + 1) - LABEL_H * ROWS) // ROWS  # 356
TOTAL_W = 1200
TOTAL_H = 900

# Render scale: faces rendered at 2x for anti-aliasing, then downscaled
RENDER_SCALE = 2
HEAD_R = 105    # head radius at 1x panel size (px)
HR = HEAD_R * RENDER_SCALE   # head radius at render scale = 210

# -- Geometry helpers ---------------------------------------------------------

def bezier3(p0, p1, p2, steps=40):
    """Quadratic Bezier curve."""
    pts = []
    for i in range(steps + 1):
        t = i / steps
        x = (1-t)**2 * p0[0] + 2*(1-t)*t * p1[0] + t**2 * p2[0]
        y = (1-t)**2 * p0[1] + 2*(1-t)*t * p1[1] + t**2 * p2[1]
        pts.append((x, y))
    return pts


def polyline(draw, pts, color, width=2):
    for i in range(len(pts) - 1):
        draw.line([pts[i], pts[i+1]], fill=color, width=width)


def arc_draw(draw, cx, cy, rx, ry, a0_deg, a1_deg, color, width=3, steps=50):
    """Draw an arc as polyline for smooth rendering."""
    pts = []
    for i in range(steps + 1):
        t = math.radians(a0_deg + (a1_deg - a0_deg) * i / steps)
        pts.append((cx + rx * math.cos(t), cy + ry * math.sin(t)))
    polyline(draw, pts, color, width)


# -- Drawing primitives -------------------------------------------------------

def draw_construction_guide(img, cx, cy):
    """Overlay faint construction circle + cross as RGBA layer."""
    guide = Image.new("RGBA", img.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(guide)
    gc = (180, 155, 128, 48)
    gd.ellipse([cx - HR, cy - HR, cx + HR, cy + HR], outline=gc, width=3)
    gd.line([(cx - HR - 20, cy), (cx + HR + 20, cy)], fill=gc, width=2)
    gd.line([(cx, cy - HR - 20), (cx, cy + HR + 20)], fill=gc, width=2)
    return Image.alpha_composite(img, guide)


def draw_head(draw, cx, cy):
    """Head circle with softened jaw + heavy silhouette outline."""
    draw.ellipse(
        [cx - HR, cy - HR, cx + HR, cy + HR],
        fill=SKIN
    )
    # Soften jaw: skin ellipse at chin area
    jaw_r = int(HR * 0.52)
    jaw_y = cy + int(HR * 0.82)
    draw.ellipse(
        [cx - jaw_r, jaw_y - int(HR * 0.20),
         cx + jaw_r, jaw_y + int(HR * 0.20)],
        fill=SKIN
    )
    # Heavy silhouette outline (8px at 2x render = ~4px output)
    draw.ellipse(
        [cx - HR, cy - HR, cx + HR, cy + HR],
        outline=LINE, width=8
    )


def draw_ears(draw, cx, cy):
    er = int(HR * 0.13)
    ey = cy + int(HR * 0.12)
    draw.ellipse(
        [cx - HR - er + 4, ey - er, cx - HR + er + 4, ey + er],
        fill=SKIN, outline=LINE, width=5
    )
    draw.ellipse(
        [cx + HR - er - 4, ey - er, cx + HR + er - 4, ey + er],
        fill=SKIN, outline=LINE, width=5
    )


def draw_hair(draw, cx, cy, variant="default"):
    """
    Luma's hair: dark cloud with choppy fringe, 5 curl indicators (LOCKED spec).
    variants: default, excited, drooped, tight
    """
    if variant == "excited":
        top_lift = int(HR * 1.44)
        spread_l = int(HR * 1.14)
        spread_r = int(HR * 1.08)
    elif variant == "drooped":
        top_lift = int(HR * 1.24)
        spread_l = int(HR * 1.00)
        spread_r = int(HR * 0.96)
    elif variant == "tight":
        top_lift = int(HR * 1.30)
        spread_l = int(HR * 1.04)
        spread_r = int(HR * 0.98)
    else:
        top_lift = int(HR * 1.36)
        spread_l = int(HR * 1.08)
        spread_r = int(HR * 1.02)

    hair_top_y = cy - top_lift
    hair_mid_y = cy - int(HR * 0.84)

    # Main hair mass
    draw.ellipse(
        [cx - spread_l, hair_top_y, cx + spread_r, hair_mid_y + int(HR * 0.24)],
        fill=HAIR
    )
    # Left lobe
    draw.ellipse(
        [cx - int(spread_l * 0.94), hair_top_y + int(HR * 0.10),
         cx - int(HR * 0.10),       hair_mid_y + int(HR * 0.38)],
        fill=HAIR
    )
    # Right lobe
    draw.ellipse(
        [cx + int(HR * 0.06),       hair_top_y + int(HR * 0.18),
         cx + int(spread_r * 0.90), hair_mid_y + int(HR * 0.30)],
        fill=HAIR
    )
    # Choppy fringe: two overlapping ellipses
    fringe_top = cy - int(HR * 0.66)
    fringe_bot = cy - int(HR * 0.30)
    draw.ellipse(
        [cx - int(HR * 0.82), fringe_top, cx + int(HR * 0.26), fringe_bot + int(HR * 0.12)],
        fill=HAIR
    )
    draw.ellipse(
        [cx - int(HR * 0.30), fringe_top - int(HR * 0.06),
         cx + int(HR * 0.74), fringe_bot],
        fill=HAIR
    )
    # Choppy fringe teeth: 3 dip points
    for dx in [-int(HR * 0.46), int(HR * 0.04), int(HR * 0.50)]:
        draw.ellipse(
            [cx + dx - int(HR * 0.17), fringe_bot - int(HR * 0.06),
             cx + dx + int(HR * 0.17), fringe_bot + int(HR * 0.18)],
            fill=HAIR
        )

    # Crown highlight
    hl = bezier3(
        (cx - int(HR * 0.30), hair_top_y + int(HR * 0.22)),
        (cx + int(HR * 0.02), hair_top_y + int(HR * 0.06)),
        (cx + int(HR * 0.36), hair_top_y + int(HR * 0.26))
    )
    polyline(draw, hl, HAIR_HL, width=5)

    # 5 curl indicators (LOCKED count per production spec)
    curls = [
        (cx - int(HR * 0.62), hair_top_y + int(HR * 0.42)),
        (cx - int(HR * 0.28), hair_top_y + int(HR * 0.14)),
        (cx + int(HR * 0.10), hair_top_y + int(HR * 0.08)),
        (cx + int(HR * 0.48), hair_top_y + int(HR * 0.34)),
        (cx + int(HR * 0.16), hair_top_y + int(HR * 0.60)),
    ]
    cr = int(HR * 0.17)
    for (hx, hy) in curls:
        arc_draw(draw, hx, hy, cr, cr, 200, 335, HAIR_HL, width=4)

    # Hair silhouette outline (heavy)
    draw.ellipse(
        [cx - spread_l, hair_top_y, cx + spread_r, hair_mid_y + int(HR * 0.24)],
        outline=LINE, width=8
    )

    # Escaping ringlet near left ear
    esc_x = cx - int(HR * 0.80)
    esc_y = cy - int(HR * 0.08)
    arc_draw(draw, esc_x, esc_y, int(HR * 0.14), int(HR * 0.20), 55, 290, HAIR, width=7)
    arc_draw(draw, esc_x, esc_y, int(HR * 0.14), int(HR * 0.20), 55, 290, LINE, width=3)


def draw_eyes_full(draw, cx, cy, params):
    """
    Full eye renderer with expression params dict.
    Keys: l_open, r_open, brow_l_dy, brow_r_dy,
          brow_furrow_l, brow_furrow_r, pupils_wide,
          gaze_dx, gaze_dy, crinkle, half_lid
    """
    eye_y   = cy + int(HR * 0.08)
    sep     = int(HR * 0.70)
    lx      = cx - sep // 2
    rx      = cx + sep // 2
    ew      = int(HR * 0.44)
    eh_full = int(HR * 0.30)
    p       = params

    for (ex, open_f, is_right) in [(lx, p["l_open"], False), (rx, p["r_open"], True)]:
        if p.get("half_lid"):
            actual_h = int(eh_full * 0.52)
        else:
            actual_h = max(3, int(eh_full * open_f))

        # Eye white
        draw.ellipse(
            [ex - ew, eye_y - actual_h, ex + ew, eye_y + actual_h],
            fill=EYE_W
        )
        # Iris
        ir  = int(ew * 0.68)
        iry = min(ir, actual_h - 2)
        if iry < 2:
            iry = 2
        pdx = int(p.get("gaze_dx", 0) * HR * 0.10)
        pdy = int(p.get("gaze_dy", 0) * HR * 0.08)
        draw.ellipse(
            [ex + pdx - ir, eye_y + pdy - iry,
             ex + pdx + ir, eye_y + pdy + iry],
            fill=EYE_IRIS
        )
        # Pupil
        pr = int(ir * 0.68) if p.get("pupils_wide") else int(ir * 0.50)
        draw.ellipse(
            [ex + pdx - pr, eye_y + pdy - pr,
             ex + pdx + pr, eye_y + pdy + pr],
            fill=EYE_PUP
        )
        # Highlight — upper-left (canonical position per spec)
        hr_small = max(int(pr * 0.38), 5)
        hlx = ex + pdx - int(ir * 0.28)
        hly = eye_y + pdy - int(iry * 0.36)
        draw.ellipse(
            [hlx - hr_small, hly - hr_small, hlx + hr_small, hly + hr_small],
            fill=EYE_HL
        )
        # Upper eyelid curve (interior, lighter weight = 4px at 2x = ~2px output)
        draw.arc(
            [ex - ew, eye_y - actual_h, ex + ew, eye_y + actual_h],
            start=200, end=340, fill=LINE, width=4
        )
        # Crinkle lines at outer corners (delighted)
        if p.get("crinkle"):
            dsign = 1 if is_right else -1
            outer_x = ex + ew * dsign
            for k in range(3):
                dy_k = int(HR * 0.04) * k
                draw.line(
                    [(outer_x, eye_y + dy_k),
                     (outer_x + dsign * int(HR * 0.11), eye_y + dy_k - int(HR * 0.07))],
                    fill=LINE, width=3
                )
        # Eye silhouette outline (heavy = 6px at 2x = ~3px output)
        draw.ellipse(
            [ex - ew, eye_y - actual_h, ex + ew, eye_y + actual_h],
            outline=LINE, width=6
        )

    # Eyebrows
    brow_base_y = eye_y - int(eh_full * 1.42)

    for (bx, b_dy, b_furrow) in [
        (lx, p.get("brow_l_dy", 0), p.get("brow_furrow_l", False)),
        (rx, p.get("brow_r_dy", 0), p.get("brow_furrow_r", False)),
    ]:
        by = brow_base_y + b_dy
        is_right_b = (bx == rx)
        inner_x = bx + int(HR * 0.10) if is_right_b else bx - int(HR * 0.10)
        outer_x = bx - int(HR * 0.38) if is_right_b else bx + int(HR * 0.38)
        # Corrugator furrow: inner end pushed down (worry / anger)
        inner_y = by + (int(HR * 0.16) if b_furrow else 0)
        outer_y = by

        pts = bezier3((outer_x, outer_y), (bx, by - int(HR * 0.04)), (inner_x, inner_y))
        polyline(draw, pts, LINE, width=10)


def draw_nose(draw, cx, cy):
    """Minimal apostrophe nose — lighter interior line weight."""
    arc_draw(draw, cx, cy + int(HR * 0.32), int(HR * 0.09), int(HR * 0.07),
             135, 305, LINE, width=4)


def draw_mouth(draw, cx, cy, style="neutral"):
    my = cy + int(HR * 0.58)
    mw = int(HR * 0.42)
    lx, rx = cx - mw, cx + mw

    if style == "neutral":
        pts = bezier3((lx, my + 6), (cx, my - 14), (rx, my + 6))
        polyline(draw, pts, LINE, width=5)

    elif style == "smile_closed":
        pts = bezier3((lx, my + 4), (cx, my - 30), (rx, my + 4))
        polyline(draw, pts, LINE, width=6)
        draw.line([(lx, my + 4), (lx - 6, my + 16)], fill=LINE, width=4)
        draw.line([(rx, my + 4), (rx + 6, my + 16)], fill=LINE, width=4)

    elif style == "smile_big":
        sh = int(HR * 0.22)
        top_pts = bezier3((lx, my), (cx, my - 34), (rx, my))
        bot_pts = bezier3((lx, my + sh), (cx, my + sh + 12), (rx, my + sh))
        fill_pts = top_pts + bot_pts[::-1]
        draw.polygon(fill_pts, fill=(210, 70, 50))
        tw = int(mw * 0.82)
        draw.rectangle([cx - tw, my - 2, cx + tw, my + sh - 4], fill=(248, 242, 230))
        polyline(draw, top_pts, LINE, width=6)
        polyline(draw, bot_pts, LINE, width=5)
        draw.line([(lx, my), (lx, my + sh)], fill=LINE, width=5)
        draw.line([(rx, my), (rx, my + sh)], fill=LINE, width=5)

    elif style == "open_oval":
        ow = int(mw * 0.54)
        oh = int(HR * 0.28)
        draw.ellipse(
            [cx - ow, my - int(oh * 0.38), cx + ow, my + int(oh * 0.62)],
            fill=(210, 65, 48)
        )
        draw.ellipse(
            [cx - ow, my - int(oh * 0.38), cx + ow, my + int(oh * 0.62)],
            outline=LINE, width=5
        )

    elif style == "pressed_flat":
        pts = bezier3((lx, my + 4), (cx, my + 10), (rx, my + 4))
        polyline(draw, pts, LINE, width=6)

    elif style == "corners_down":
        pts = bezier3((lx, my - 14), (cx, my + 18), (rx, my - 14))
        polyline(draw, pts, LINE, width=5)

    elif style == "frown_slight":
        pts = bezier3((lx, my - 8), (cx, my + 18), (rx, my - 8))
        polyline(draw, pts, LINE, width=5)


def draw_blush(draw, cx, cy, alpha=120):
    if alpha <= 0:
        return
    bw = int(HR * 0.26)
    bh = int(HR * 0.11)
    by = cy + int(HR * 0.38)
    for bx in [cx - int(HR * 0.56), cx + int(HR * 0.56)]:
        draw.ellipse([bx - bw, by - bh, bx + bw, by + bh], fill=BLUSH_C)


def draw_collar(draw, cx, cy, hoodie_col):
    """Neck + hoodie collar."""
    nt = cy + int(HR * 0.88)
    nb = cy + int(HR * 1.18)
    nw = int(HR * 0.28)
    cw = int(HR * 1.02)
    ch = int(HR * 0.40)
    draw.rectangle([cx - nw, nt, cx + nw, nb], fill=SKIN)
    draw.ellipse(
        [cx - cw, nb - ch // 2, cx + cw, nb + ch],
        fill=hoodie_col
    )
    draw.ellipse(
        [cx - cw, nb - ch // 2, cx + cw, nb + ch],
        outline=LINE, width=7
    )
    draw.rectangle([cx - nw, nt, cx + nw, nb], outline=LINE, width=5)


# -- Expression specification table ------------------------------------------

EXPR_SPECS = {
    "CURIOUS": {
        "hair": "default",
        "blush": 80,
        "eyes": {
            "l_open": 0.90, "r_open": 0.86,
            "brow_l_dy": -int(HR * 0.18), "brow_r_dy": -int(HR * 0.24),
            "gaze_dx": 0.4, "gaze_dy": -0.2,
            "brow_furrow_l": False, "brow_furrow_r": False,
        },
        "mouth": "neutral",
        "cy_offset": 0,
    },
    "DETERMINED": {
        "hair": "tight",
        "blush": 0,
        "eyes": {
            "l_open": 0.80, "r_open": 0.80,
            "brow_l_dy": int(HR * 0.10), "brow_r_dy": int(HR * 0.10),
            "gaze_dx": 0, "gaze_dy": 0.12,
            "brow_furrow_l": False, "brow_furrow_r": False,
        },
        "mouth": "pressed_flat",
        "cy_offset": int(HR * 0.06),
    },
    "SURPRISED": {
        "hair": "excited",
        "blush": 0,
        "eyes": {
            "l_open": 1.0, "r_open": 1.0,
            "brow_l_dy": -int(HR * 0.32), "brow_r_dy": -int(HR * 0.32),
            "gaze_dx": 0, "gaze_dy": 0,
            "pupils_wide": True,
            "brow_furrow_l": False, "brow_furrow_r": False,
        },
        "mouth": "open_oval",
        "cy_offset": 0,
    },
    "WORRIED": {
        "hair": "drooped",
        "blush": 0,
        "eyes": {
            "l_open": 0.72, "r_open": 0.72,
            "brow_l_dy": -int(HR * 0.18), "brow_r_dy": -int(HR * 0.18),
            "gaze_dx": 0, "gaze_dy": 0.18,
            "brow_furrow_l": True, "brow_furrow_r": True,
        },
        "mouth": "corners_down",
        "cy_offset": 0,
    },
    "DELIGHTED": {
        "hair": "excited",
        "blush": 140,
        "eyes": {
            "l_open": 0.60, "r_open": 0.60,
            "brow_l_dy": -int(HR * 0.16), "brow_r_dy": -int(HR * 0.16),
            "gaze_dx": 0, "gaze_dy": 0,
            "crinkle": True,
            "brow_furrow_l": False, "brow_furrow_r": False,
        },
        "mouth": "smile_big",
        "cy_offset": 0,
    },
    "FRUSTRATED": {
        "hair": "tight",
        "blush": 0,
        "eyes": {
            "l_open": 0.55, "r_open": 0.55,
            "brow_l_dy": int(HR * 0.14), "brow_r_dy": int(HR * 0.14),
            "gaze_dx": 0, "gaze_dy": 0.22,
            "half_lid": True,
            "brow_furrow_l": True, "brow_furrow_r": True,
        },
        "mouth": "frown_slight",
        "cy_offset": 0,
    },
}


# -- Expression renderer ------------------------------------------------------

def render_face(expr, face_w, face_h):
    """Render one expression at 2x scale for AA, return RGBA downscaled image."""
    rw = face_w * RENDER_SCALE
    rh = face_h * RENDER_SCALE
    img = Image.new("RGBA", (rw, rh), (0, 0, 0, 0))

    cx   = rw // 2
    spec = EXPR_SPECS[expr]
    cy_off = spec.get("cy_offset", 0)
    cy   = int(rh * 0.52) + cy_off

    # Construction guide as RGBA overlay
    img  = draw_construction_guide(img, cx, cy)
    draw = ImageDraw.Draw(img)

    draw_head(draw, cx, cy)
    draw_ears(draw, cx, cy)
    draw_hair(draw, cx, cy, variant=spec["hair"])
    draw_blush(draw, cx, cy, alpha=spec["blush"])
    draw_eyes_full(draw, cx, cy, spec["eyes"])
    draw_nose(draw, cx, cy)
    draw_mouth(draw, cx, cy, style=spec["mouth"])
    draw_collar(draw, cx, cy, HOODIE_MAP[expr])

    # Downscale 2x -> 1x with LANCZOS for anti-aliasing
    return img.resize((face_w, face_h), Image.LANCZOS)


# -- Sheet assembly -----------------------------------------------------------

EXPRESSIONS = ["CURIOUS", "DETERMINED", "SURPRISED",
               "WORRIED",  "DELIGHTED",  "FRUSTRATED"]


def build_sheet():
    sheet = Image.new("RGB", (TOTAL_W, TOTAL_H), CANVAS_BG)
    draw  = ImageDraw.Draw(sheet)

    try:
        font_title = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 26)
        font_label = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 17)
        font_sub   = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 13)
    except Exception:
        font_title = ImageFont.load_default()
        font_label = font_title
        font_sub   = font_title

    title = "LUMA — Expression Sheet v002  |  Luma & the Glitchkin"
    sub   = ("Designer: Maya Santos  |  Cycle 17 Refinement  |  "
             "3x2 grid  |  6 core expressions  |  Construction guides visible")
    draw.text((PAD, 10), title, fill=(235, 218, 196), font=font_title)
    draw.text((PAD, 38), sub,   fill=(165, 150, 130), font=font_sub)

    face_w = PANEL_W - PAD * 2
    face_h = PANEL_H - PAD

    for idx, expr in enumerate(EXPRESSIONS):
        col = idx % COLS
        row = idx // COLS
        px  = PAD + col * (PANEL_W + PAD)
        py  = HEADER + PAD + row * (PANEL_H + LABEL_H + PAD)

        # Panel background
        bg = BG[expr]
        draw.rectangle([px, py, px + PANEL_W, py + PANEL_H], fill=bg)
        draw.rectangle([px, py, px + PANEL_W, py + PANEL_H], outline=LINE, width=2)

        # Render and paste face
        face_img = render_face(expr, face_w, face_h)
        ox = px + PAD
        oy = py + PAD // 2
        sheet.paste(face_img, (ox, oy), face_img)

        # IMPORTANT: refresh draw object after paste
        draw = ImageDraw.Draw(sheet)

        # Label strip
        label_y  = py + PANEL_H + 2
        label_bg = tuple(max(0, int(c * 0.88)) for c in bg)
        draw.rectangle([px, label_y, px + PANEL_W, label_y + LABEL_H], fill=label_bg)
        bbox = draw.textbbox((0, 0), expr, font=font_label)
        tw   = bbox[2] - bbox[0]
        th   = bbox[3] - bbox[1]
        tx   = px + (PANEL_W - tw) // 2
        ty   = label_y + (LABEL_H - th) // 2
        draw.text((tx, ty), expr, fill=LINE, font=font_label)

    return sheet


if __name__ == "__main__":
    out_dir  = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "..", "characters", "main")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "LTG_CHAR_luma_expression_sheet_v002.png")
    sheet    = build_sheet()
    sheet.save(out_path)
    print(f"Saved: {os.path.abspath(out_path)}")
    print(f"Canvas: {sheet.size[0]}x{sheet.size[1]}")
