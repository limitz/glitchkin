#!/usr/bin/env python3
"""
LTG_TOOL_grandma_miri_expression_sheet_v001.py
Grandma Miri Expression Sheet v001
"Luma & the Glitchkin" — Cycle 17

5 expressions: WARM/WELCOMING, NOSTALGIC/WISTFUL, CONCERNED,
               SURPRISED/DELIGHTED, WISE/KNOWING

Layout: 5-in-a-row (1500x700)
  OR  : 3+2 grid  (1200x900)
Using: 3+2 grid, 1200x900 for compatibility with project layout standards.

Character spec from grandma_miri.md (MIRI-A canonical):
  - Silver hair in a bun (chopstick pair), round glasses
  - Compact build, warm olive/deep brown skin (#8C5430)
  - Knit cardigan (terracotta rust #B85C38)
  - 88% circular head (more compressed than Luma's 95%)
  - Smaller eyes (0.16x head) than Luma (0.22x)
  - Crow's feet (always present), smile lines
  - Softer/thinner brows than Luma, warm gray (#8A7A70)
  - Permanent cheek blush #D4956B (25% opacity feel)
  - Round glasses — defining silhouette element

Color palette from grandma_miri.md:
  SKIN_BASE    #8C5430  Deep Warm Brown
  SKIN_SH      #6A3A1E  Dark Sienna
  SKIN_HL      #A86A40  Warm Chestnut
  BLUSH_PERM   #D4956B  always present (light)
  HAIR_BASE    #D8D0C8  Silver White
  HAIR_SH      #A8988C  Warm Gray
  HAIR_HL      #F0ECE8  Bright Near-White
  EYE_IRIS     #8B5E3C  Deep Warm Amber
  EYE_PUP      #1A0F0A  Near-Black Espresso
  EYE_W        #FAF0DC  Warm Cream
  EYE_HL       #F0F0F0  Static White
  BROW_COL     #8A7A70  Warm Gray
  CARDIGAN     #B85C38  Warm Terracotta Rust
  CARDIGAN_SH  #8A3C1C  Deep Rust
  CARDIGAN_HL  #D4825A  Dusty Apricot
  GLASSES_COL  #3B2820  Deep Cocoa (line weight)
  LINE         #3B2820  Deep Cocoa

Output: output/characters/main/LTG_CHAR_grandma_miri_expression_sheet_v001.png
"""

from PIL import Image, ImageDraw, ImageFont
import math
import os

# -- Palette from grandma_miri.md canonical spec ------------------------------
SKIN_BASE   = (140, 84, 48)
SKIN_SH     = (106, 58, 30)
SKIN_HL     = (168, 106, 64)
BLUSH_PERM  = (212, 149, 107)
HAIR_BASE   = (216, 208, 200)
HAIR_SH     = (168, 152, 140)
HAIR_HL     = (240, 236, 232)
EYE_IRIS    = (139, 94, 60)
EYE_PUP     = (26, 15, 10)
EYE_W       = (250, 240, 220)
EYE_HL      = (240, 240, 240)
BROW_COL    = (138, 122, 112)
CARDIGAN    = (184, 92, 56)
CARDIGAN_SH = (138, 60, 28)
CARDIGAN_HL = (212, 130, 90)
GLASSES_COL = (59, 40, 32)
LINE        = (59, 40, 32)
CANVAS_BG   = (28, 20, 14)

# Panel backgrounds per expression
BG = {
    "WARM":      (248, 232, 210),
    "NOSTALGIC": (210, 220, 232),
    "CONCERNED": (200, 212, 225),
    "SURPRISED": (245, 228, 195),
    "WISE":      (220, 215, 205),
}

# -- Layout (3+2 grid, 1200x900) ---------------------------------------------
TOTAL_W = 1200
TOTAL_H = 900
COLS    = 3
ROWS    = 2
PAD     = 20
HEADER  = 58
LABEL_H = 36
PANEL_W = (TOTAL_W - PAD * (COLS + 1)) // COLS    # 380
PANEL_H = (TOTAL_H - HEADER - PAD * (ROWS + 1) - LABEL_H * ROWS) // ROWS  # 356

# Render scale for AA
RENDER_SCALE = 2
# Miri head radius at 1x (slightly smaller than Luma, 88% circularity)
HEAD_R = 98
HR = HEAD_R * RENDER_SCALE    # 196 at render scale

# Expressions: 5 total in 3+2 layout
EXPRESSIONS = ["WARM", "NOSTALGIC", "CONCERNED", "SURPRISED", "WISE"]
EXPR_LABELS = {
    "WARM":      "WARM / WELCOMING",
    "NOSTALGIC": "NOSTALGIC / WISTFUL",
    "CONCERNED": "CONCERNED",
    "SURPRISED": "SURPRISED / DELIGHTED",
    "WISE":      "WISE / KNOWING",
}

# -- Geometry helpers ---------------------------------------------------------

def bezier3(p0, p1, p2, steps=40):
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
    pts = []
    for i in range(steps + 1):
        t = math.radians(a0_deg + (a1_deg - a0_deg) * i / steps)
        pts.append((cx + rx * math.cos(t), cy + ry * math.sin(t)))
    polyline(draw, pts, color, width)


# -- Drawing primitives -------------------------------------------------------

def draw_construction_guide(img, cx, cy):
    guide = Image.new("RGBA", img.size, (0, 0, 0, 0))
    gd    = ImageDraw.Draw(guide)
    gc    = (180, 155, 128, 44)
    # Head is 88% circular — slightly compressed vertically
    gd.ellipse([cx - HR, cy - int(HR * 0.94), cx + HR, cy + int(HR * 0.94)],
               outline=gc, width=3)
    gd.line([(cx - HR - 18, cy), (cx + HR + 18, cy)], fill=gc, width=2)
    gd.line([(cx, cy - HR - 18), (cx, cy + HR + 18)], fill=gc, width=2)
    return Image.alpha_composite(img, guide)


def draw_head_miri(draw, cx, cy):
    """88% circular head (gently compressed vertically)."""
    ry = int(HR * 0.94)   # slight vertical compression
    draw.ellipse(
        [cx - HR, cy - ry, cx + HR, cy + ry],
        fill=SKIN_BASE
    )
    # Jaw softening
    jaw_r = int(HR * 0.55)
    jaw_y = cy + int(ry * 0.80)
    draw.ellipse(
        [cx - jaw_r, jaw_y - int(ry * 0.22),
         cx + jaw_r, jaw_y + int(ry * 0.22)],
        fill=SKIN_BASE
    )
    # Heavy silhouette outline
    draw.ellipse(
        [cx - HR, cy - ry, cx + HR, cy + ry],
        outline=LINE, width=8
    )


def draw_ears_miri(draw, cx, cy):
    er = int(HR * 0.12)
    ey = cy + int(HR * 0.08)
    ry = int(HR * 0.94)
    draw.ellipse(
        [cx - HR - er + 4, ey - er, cx - HR + er + 4, ey + er],
        fill=SKIN_BASE, outline=LINE, width=5
    )
    draw.ellipse(
        [cx + HR - er - 4, ey - er, cx + HR + er - 4, ey + er],
        fill=SKIN_BASE, outline=LINE, width=5
    )


def draw_hair_bun(draw, cx, cy, variant="default"):
    """
    Miri's hair: silver-white soft bun on upper-back of head,
    loose wisps framing face, slight center-right part.
    variant: default, wistful (slightly softer wisps), concerned (tighter)
    """
    ry = int(HR * 0.94)
    hair_top = cy - ry - int(HR * 0.28)   # bun adds ~0.25 head height

    # Hair mass over head (before bun)
    draw.ellipse(
        [cx - int(HR * 0.96), hair_top + int(HR * 0.12),
         cx + int(HR * 0.92), cy - int(ry * 0.60)],
        fill=HAIR_BASE
    )

    # Bun: rounded oval on upper-back of head (slightly right of center)
    bun_cx = cx + int(HR * 0.10)
    bun_cy = hair_top + int(HR * 0.18)
    bun_rx = int(HR * 0.52)
    bun_ry = int(HR * 0.38)
    draw.ellipse(
        [bun_cx - bun_rx, bun_cy - bun_ry,
         bun_cx + bun_rx, bun_cy + bun_ry],
        fill=HAIR_BASE
    )
    # Bun shadow
    draw.ellipse(
        [bun_cx - int(bun_rx * 0.70), bun_cy,
         bun_cx + int(bun_rx * 0.60), bun_cy + bun_ry],
        fill=HAIR_SH
    )
    # Bun highlight
    arc_draw(draw, bun_cx - int(bun_rx * 0.15), bun_cy - int(bun_ry * 0.30),
             int(bun_rx * 0.52), int(bun_ry * 0.38), 200, 330, HAIR_HL, width=4)
    # Chopstick pair (two thin dark lines crossing through bun)
    chop_x1 = bun_cx - int(bun_rx * 0.35)
    chop_x2 = bun_cx + int(bun_rx * 0.28)
    draw.line([(chop_x1, bun_cy - bun_ry - 12), (chop_x1 + 8, bun_cy + bun_ry + 8)],
              fill=LINE, width=4)
    draw.line([(chop_x2, bun_cy - bun_ry - 10), (chop_x2 + 8, bun_cy + bun_ry + 6)],
              fill=LINE, width=4)
    # Bun outline
    draw.ellipse(
        [bun_cx - bun_rx, bun_cy - bun_ry,
         bun_cx + bun_rx, bun_cy + bun_ry],
        outline=LINE, width=6
    )

    # Loose wisps framing face (3-4 fine strands)
    wisp_pts_l = [
        bezier3((cx - int(HR * 0.84), cy - ry + 10),
                (cx - int(HR * 0.74), cy - int(ry * 0.42)),
                (cx - int(HR * 0.80), cy - int(ry * 0.05))),
        bezier3((cx - int(HR * 0.78), cy - ry + 20),
                (cx - int(HR * 0.68), cy - int(ry * 0.30)),
                (cx - int(HR * 0.72), cy + int(ry * 0.08))),
    ]
    wisp_pts_r = [
        bezier3((cx + int(HR * 0.72), cy - ry + 16),
                (cx + int(HR * 0.80), cy - int(ry * 0.36)),
                (cx + int(HR * 0.74), cy)),
    ]
    for pts in wisp_pts_l + wisp_pts_r:
        polyline(draw, pts, HAIR_BASE, width=4)
        polyline(draw, pts, LINE, width=2)

    # Hair outline (over-head mass)
    draw.ellipse(
        [cx - int(HR * 0.96), hair_top + int(HR * 0.12),
         cx + int(HR * 0.92), cy - int(ry * 0.60)],
        outline=LINE, width=6
    )


def draw_eyes_miri(draw, cx, cy, params):
    """
    Miri's eyes: smaller (0.16x head), rounded almond, calm aperture.
    Crow's feet always present (2 lines at outer corners).
    Slightly heavier lower lid curve (smile crinkle).
    """
    eye_y   = cy + int(HR * 0.10)
    sep     = int(HR * 0.58)     # smaller separation than Luma
    lx      = cx - sep // 2
    rx      = cx + sep // 2
    ew      = int(HR * 0.32)     # smaller than Luma's 0.44
    eh_full = int(HR * 0.22)     # smaller height
    p       = params

    for (ex, open_f, is_right) in [(lx, p["l_open"], False), (rx, p["r_open"], True)]:
        actual_h = max(3, int(eh_full * open_f))
        if p.get("eyes_closed"):
            actual_h = max(2, int(eh_full * 0.08))

        # Eye white
        draw.ellipse(
            [ex - ew, eye_y - actual_h, ex + ew, eye_y + actual_h],
            fill=EYE_W
        )
        # Iris (smaller relative proportion)
        ir  = int(ew * 0.62)
        iry = min(ir, actual_h - 2)
        if iry < 2:
            iry = 2
        pdx = int(p.get("gaze_dx", 0) * HR * 0.08)
        pdy = int(p.get("gaze_dy", 0) * HR * 0.06)
        draw.ellipse(
            [ex + pdx - ir, eye_y + pdy - iry,
             ex + pdx + ir, eye_y + pdy + iry],
            fill=EYE_IRIS
        )
        # Pupil
        pr = int(ir * 0.52)
        if p.get("pupils_wide"):
            pr = int(ir * 0.68)
        draw.ellipse(
            [ex + pdx - pr, eye_y + pdy - pr,
             ex + pdx + pr, eye_y + pdy + pr],
            fill=EYE_PUP
        )
        # Highlight
        if not p.get("eyes_closed"):
            hr_s = max(int(pr * 0.38), 4)
            hlx  = ex + pdx - int(ir * 0.26)
            hly  = eye_y + pdy - int(iry * 0.34)
            draw.ellipse([hlx - hr_s, hly - hr_s, hlx + hr_s, hly + hr_s], fill=EYE_HL)

        # Eyelid line (lighter interior weight)
        draw.arc(
            [ex - ew, eye_y - actual_h, ex + ew, eye_y + actual_h],
            start=200, end=340, fill=LINE, width=4
        )
        # Slight lower-lid crinkle (Miri's characteristic warm lower lid)
        if not p.get("eyes_closed"):
            arc_draw(draw, ex, eye_y + actual_h - int(eh_full * 0.30),
                     int(ew * 0.78), int(eh_full * 0.28),
                     15, 165, LINE, width=3)

        # Crow's feet: 2 small curved lines at outer corner (ALWAYS PRESENT)
        dsign = 1 if is_right else -1
        outer_x = ex + ew * dsign
        for k in range(2):
            dy_k = int(HR * 0.06) * k
            draw.line(
                [(outer_x, eye_y - int(HR * 0.02) + dy_k),
                 (outer_x + dsign * int(HR * 0.12),
                  eye_y - int(HR * 0.10) + dy_k)],
                fill=LINE, width=3
            )

        # Eye silhouette outline
        draw.ellipse(
            [ex - ew, eye_y - actual_h, ex + ew, eye_y + actual_h],
            outline=LINE, width=6
        )

    # Glasses — round wire frames over the eyes
    glasses_r_x = int(ew * 1.18)
    glasses_r_y = int(eh_full * 1.35)
    for (gx, is_right_g) in [(lx, False), (rx, True)]:
        draw.ellipse(
            [gx - glasses_r_x, eye_y - glasses_r_y,
             gx + glasses_r_x, eye_y + glasses_r_y],
            outline=GLASSES_COL, width=5
        )
    # Bridge between glasses
    bridge_y = eye_y - int(glasses_r_y * 0.10)
    draw.line([(lx + glasses_r_x, bridge_y), (rx - glasses_r_x, bridge_y)],
              fill=GLASSES_COL, width=5)
    # Glasses arms (temples going back to ears)
    draw.line(
        [(lx - glasses_r_x, bridge_y),
         (lx - glasses_r_x - int(HR * 0.20), bridge_y - int(HR * 0.04))],
        fill=GLASSES_COL, width=4
    )
    draw.line(
        [(rx + glasses_r_x, bridge_y),
         (rx + glasses_r_x + int(HR * 0.20), bridge_y - int(HR * 0.04))],
        fill=GLASSES_COL, width=4
    )

    # Eyebrows — Miri's brows: softer, thinner, warm gray, slight amused arch
    brow_base_y = eye_y - int(eh_full * 1.38) - glasses_r_y + int(eh_full * 0.40)

    for (bx, b_dy, b_in_worry) in [
        (lx, p.get("brow_l_dy", 0), p.get("brow_worry", False)),
        (rx, p.get("brow_r_dy", 0), p.get("brow_worry", False)),
    ]:
        by = brow_base_y + b_dy
        is_right_b = (bx == rx)
        inner_x = bx + int(HR * 0.08) if is_right_b else bx - int(HR * 0.08)
        outer_x = bx - int(HR * 0.28) if is_right_b else bx + int(HR * 0.28)
        inner_y = by + (int(HR * 0.14) if b_in_worry else 0)
        outer_y = by
        pts = bezier3((outer_x, outer_y), (bx, by - int(HR * 0.03)), (inner_x, inner_y))
        polyline(draw, pts, BROW_COL, width=7)

    # Smile lines (always present, 40% weight feel = lighter line)
    for side in [-1, 1]:
        sl_pts = bezier3(
            (cx + side * int(HR * 0.16), cy + int(HR * 0.24)),
            (cx + side * int(HR * 0.26), cy + int(HR * 0.42)),
            (cx + side * int(HR * 0.30), cy + int(HR * 0.58))
        )
        polyline(draw, sl_pts, LINE, width=3)


def draw_nose_miri(draw, cx, cy):
    """Miri's more defined nose: soft arc with slight nostril indication."""
    ny = cy + int(HR * 0.28)
    # Main arc
    arc_draw(draw, cx, ny, int(HR * 0.10), int(HR * 0.09), 130, 310, LINE, width=4)
    # Slight nostril suggestions
    for side in [-1, 1]:
        arc_draw(draw, cx + side * int(HR * 0.09), ny + int(HR * 0.06),
                 int(HR * 0.05), int(HR * 0.04), 180, 350, LINE, width=3)


def draw_mouth_miri(draw, cx, cy, style="warm_closed"):
    """
    Mouth styles:
      warm_closed - default, gentle upward curve, full
      wistful     - small tender smile, slightly asymmetric
      pursed      - concerned, corners slightly inward
      open_delight- wide, eyes closed delight (teeth showing)
      knowing     - subtle closed smile
    """
    my = cy + int(HR * 0.54)
    mw = int(HR * 0.38)
    lx = cx - mw
    rx = cx + mw

    if style == "warm_closed":
        pts = bezier3((lx, my + 4), (cx, my - 22), (rx, my + 4))
        polyline(draw, pts, LINE, width=5)
        draw.line([(lx, my + 4), (lx - 5, my + 12)], fill=LINE, width=4)
        draw.line([(rx, my + 4), (rx + 5, my + 12)], fill=LINE, width=4)

    elif style == "wistful":
        # Small tender smile — narrower, slightly asymmetric
        mw2 = int(mw * 0.72)
        pts = bezier3((cx - mw2, my + 4), (cx, my - 14), (cx + mw2, my + 2))
        polyline(draw, pts, LINE, width=5)

    elif style == "pursed":
        # Slightly pressed together, corners slightly inward
        pts = bezier3((lx + int(mw * 0.14), my + 2), (cx, my + 8),
                      (rx - int(mw * 0.14), my + 2))
        polyline(draw, pts, LINE, width=6)

    elif style == "open_delight":
        # Open laugh, warm oval, teeth visible
        sh = int(HR * 0.20)
        top_pts = bezier3((lx, my), (cx, my - 26), (rx, my))
        bot_pts = bezier3((lx, my + sh), (cx, my + sh + 10), (rx, my + sh))
        fill_pts = top_pts + bot_pts[::-1]
        draw.polygon(fill_pts, fill=(200, 65, 45))
        tw = int(mw * 0.80)
        draw.rectangle([cx - tw, my - 2, cx + tw, my + sh - 4], fill=(248, 242, 230))
        polyline(draw, top_pts, LINE, width=6)
        polyline(draw, bot_pts, LINE, width=5)
        draw.line([(lx, my), (lx, my + sh)], fill=LINE, width=5)
        draw.line([(rx, my), (rx, my + sh)], fill=LINE, width=5)

    elif style == "knowing":
        # Subtle closed smile — warm but narrow
        mw2 = int(mw * 0.68)
        pts = bezier3((cx - mw2, my + 6), (cx, my - 12), (cx + mw2, my + 6))
        polyline(draw, pts, LINE, width=5)


def draw_blush_miri(draw, cx, cy, strength=1.0):
    """Miri's permanent warm cheek blush (always present, varies in intensity)."""
    if strength <= 0:
        return
    bw = int(HR * 0.22)
    bh = int(HR * 0.10)
    by = cy + int(HR * 0.34)
    for bx in [cx - int(HR * 0.46), cx + int(HR * 0.46)]:
        draw.ellipse([bx - bw, by - bh, bx + bw, by + bh], fill=BLUSH_PERM)


def draw_cardigan_collar(draw, cx, cy):
    """Miri's cardigan collar — V-neck, terracotta rust."""
    nt = cy + int(HR * 0.92)
    nb = cy + int(HR * 1.15)
    nw = int(HR * 0.26)
    cw = int(HR * 1.05)
    ch = int(HR * 0.44)
    draw.rectangle([cx - nw, nt, cx + nw, nb], fill=SKIN_BASE)
    draw.ellipse(
        [cx - cw, nb - ch // 2, cx + cw, nb + ch],
        fill=CARDIGAN
    )
    draw.ellipse(
        [cx - cw, nb - ch // 2, cx + cw, nb + ch],
        outline=LINE, width=7
    )
    # V-neck opening
    draw.polygon(
        [(cx, nt + int(HR * 0.18)), (cx - int(nw * 0.80), nb), (cx + int(nw * 0.80), nb)],
        fill=SKIN_BASE
    )
    # Cable-knit indication: 3 vertical paired lines on each side
    for side in [-1, 1]:
        for k in range(3):
            kx = cx + side * (int(HR * 0.38) + k * int(HR * 0.18))
            ky0 = nb + int(HR * 0.04)
            ky1 = nb + ch - 4
            draw.line([(kx, ky0), (kx, ky1)], fill=CARDIGAN_SH, width=3)
            draw.line([(kx + 5, ky0), (kx + 5, ky1)], fill=CARDIGAN_HL, width=2)
    draw.rectangle([cx - nw, nt, cx + nw, nb], outline=LINE, width=5)


# -- Expression specifications -----------------------------------------------

EXPR_SPECS = {
    "WARM": {
        "hair":    "default",
        "blush":   1.0,        # full permanent blush
        "eyes": {
            "l_open": 0.80, "r_open": 0.80,
            "brow_l_dy": -int(HR * 0.08), "brow_r_dy": -int(HR * 0.08),
            "gaze_dx": 0, "gaze_dy": 0,
        },
        "mouth":   "warm_closed",
        "cy_offset": 0,
    },
    "NOSTALGIC": {
        "hair":    "default",
        "blush":   0.6,        # softer
        "eyes": {
            "l_open": 0.72, "r_open": 0.70,
            "brow_l_dy": -int(HR * 0.05), "brow_r_dy": -int(HR * 0.06),
            "gaze_dx": 0.15, "gaze_dy": 0.10,   # slightly unfocused
        },
        "mouth":   "wistful",
        "cy_offset": 0,
    },
    "CONCERNED": {
        "hair":    "default",
        "blush":   0.0,        # blush fades in concern (production note)
        "eyes": {
            "l_open": 0.88, "r_open": 0.88,
            "brow_l_dy": -int(HR * 0.14), "brow_r_dy": -int(HR * 0.14),
            "brow_worry": True,
            "gaze_dx": 0, "gaze_dy": 0.06,
        },
        "mouth":   "pursed",
        "cy_offset": 0,
    },
    "SURPRISED": {
        "hair":    "default",
        "blush":   1.0,        # full — surprised delight
        "eyes": {
            "l_open": 1.0, "r_open": 1.0,
            "brow_l_dy": -int(HR * 0.26), "brow_r_dy": -int(HR * 0.26),
            "pupils_wide": True,
            "gaze_dx": 0, "gaze_dy": 0,
        },
        "mouth":   "open_delight",
        "cy_offset": 0,
    },
    "WISE": {
        "hair":    "default",
        "blush":   0.7,
        "eyes": {
            "l_open": 0.68, "r_open": 0.68,
            "brow_l_dy": 0, "brow_r_dy": 0,
            "gaze_dx": 0, "gaze_dy": 0.08,
        },
        "mouth":   "knowing",
        "cy_offset": 0,
    },
}


# -- Face renderer ------------------------------------------------------------

def render_face_miri(expr, face_w, face_h):
    rw = face_w * RENDER_SCALE
    rh = face_h * RENDER_SCALE
    img = Image.new("RGBA", (rw, rh), (0, 0, 0, 0))

    cx   = rw // 2
    spec = EXPR_SPECS[expr]
    cy   = int(rh * 0.54) + spec.get("cy_offset", 0)

    img  = draw_construction_guide(img, cx, cy)
    draw = ImageDraw.Draw(img)

    draw_head_miri(draw, cx, cy)
    draw_ears_miri(draw, cx, cy)
    draw_hair_bun(draw, cx, cy)
    draw_blush_miri(draw, cx, cy, strength=spec["blush"])
    draw_eyes_miri(draw, cx, cy, spec["eyes"])
    draw_nose_miri(draw, cx, cy)
    draw_mouth_miri(draw, cx, cy, style=spec["mouth"])
    draw_cardigan_collar(draw, cx, cy)

    return img.resize((face_w, face_h), Image.LANCZOS)


# -- Sheet assembly -----------------------------------------------------------

def build_sheet():
    sheet = Image.new("RGB", (TOTAL_W, TOTAL_H), CANVAS_BG)
    draw  = ImageDraw.Draw(sheet)

    try:
        font_title = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 26)
        font_label = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14)
        font_sub   = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 13)
    except Exception:
        font_title = ImageFont.load_default()
        font_label = font_title
        font_sub   = font_title

    title = "GRANDMA MIRI — Expression Sheet v001  |  Luma & the Glitchkin"
    sub   = ("Designer: Maya Santos  |  Cycle 17  |  MIRI-A canonical  |  "
             "5 expressions  |  Construction guides visible")
    draw.text((PAD, 10), title, fill=(235, 218, 196), font=font_title)
    draw.text((PAD, 38), sub,   fill=(165, 150, 130), font=font_sub)

    face_w = PANEL_W - PAD * 2
    face_h = PANEL_H - PAD

    for idx, expr in enumerate(EXPRESSIONS):
        # 3+2 layout: row 0 = 3 panels, row 1 = 2 panels centered
        row = idx // COLS
        col_in_row = idx % COLS

        if row == 0:
            px = PAD + col_in_row * (PANEL_W + PAD)
        else:
            # Row 1: 2 panels centered
            n_in_row = len(EXPRESSIONS) - COLS   # should be 2
            total_row_w = n_in_row * PANEL_W + (n_in_row - 1) * PAD
            start_x = (TOTAL_W - total_row_w) // 2
            px = start_x + col_in_row * (PANEL_W + PAD)

        py = HEADER + PAD + row * (PANEL_H + LABEL_H + PAD)

        bg = BG[expr]
        draw.rectangle([px, py, px + PANEL_W, py + PANEL_H], fill=bg)
        draw.rectangle([px, py, px + PANEL_W, py + PANEL_H], outline=LINE, width=2)

        face_img = render_face_miri(expr, face_w, face_h)
        ox = px + PAD
        oy = py + PAD // 2
        sheet.paste(face_img, (ox, oy), face_img)

        # IMPORTANT: refresh draw after paste
        draw = ImageDraw.Draw(sheet)

        label    = EXPR_LABELS[expr]
        label_y  = py + PANEL_H + 2
        label_bg = tuple(max(0, int(c * 0.88)) for c in bg)
        draw.rectangle([px, label_y, px + PANEL_W, label_y + LABEL_H], fill=label_bg)
        bbox = draw.textbbox((0, 0), label, font=font_label)
        tw   = bbox[2] - bbox[0]
        th   = bbox[3] - bbox[1]
        tx   = px + (PANEL_W - tw) // 2
        ty   = label_y + (LABEL_H - th) // 2
        draw.text((tx, ty), label, fill=LINE, font=font_label)

    return sheet


if __name__ == "__main__":
    out_dir  = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "..", "characters", "main")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "LTG_CHAR_grandma_miri_expression_sheet_v001.png")
    sheet    = build_sheet()
    sheet.save(out_path)
    print(f"Saved: {os.path.abspath(out_path)}")
    print(f"Canvas: {sheet.size[0]}x{sheet.size[1]}")
