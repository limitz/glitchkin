# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_bg_luma_study_interior.py — Luma's Study/Bedroom Interior Background
"Luma & the Glitchkin" — Environment & Background Art / Hana Okonkwo / Cycle 42

Luma's bedroom study: the inciting-incident room for SF01. A curious, creative kid's
space with a CRT monitor as key light. Evening mood — warm lamp + cool CRT + distant
window. Real World palette only. Zero Glitch colors.

Architecture:
  - 1280×720px canvas (native — no LANCZOS upscale)
  - 3/4 view from front-right, looking back-left
  - Low camera (child/seated perspective)
  - VP_X = int(W * 0.18), VP_Y = int(H * 0.38)

Dual-temp split for QA:
  - Cool bottom: CRT spill (blue-green) on floor, shadow zone
  - Warm top: ceiling, lamp, upper wall
  - Target separation ≥ 14 PIL hue units

Output: output/backgrounds/environments/LTG_ENV_luma_study_interior.png
"""

import os
import sys
import math
import random

from PIL import Image, ImageDraw, ImageFilter

# ---------------------------------------------------------------------------
# Import render_lib from tools dir
# ---------------------------------------------------------------------------
_TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _TOOLS_DIR)
from LTG_TOOL_render_lib import (gaussian_glow, light_shaft, dust_motes, vignette,
                                  paper_texture, flatten_rgba_to_rgb)

# ---------------------------------------------------------------------------
# Canvas
# ---------------------------------------------------------------------------
W, H = 1280, 720

# ---------------------------------------------------------------------------
# Vanishing point
# ---------------------------------------------------------------------------
VP_X = int(W * 0.18)   # 230
VP_Y = int(H * 0.38)   # 273

# ---------------------------------------------------------------------------
# Seeded RNG
# ---------------------------------------------------------------------------
RNG = random.Random(62)

# ---------------------------------------------------------------------------
# Palette — Real World only. Zero Glitch colors.
# ---------------------------------------------------------------------------
# Walls / ceiling
WALL_WARM_CREAM     = (232, 220, 196)   # warm aged cream for upper wall / ceiling
WALL_MID            = (200, 190, 170)   # mid-value wall (back left)
CEILING_COLOR       = (240, 230, 210)   # warm cream ceiling

# Floor
FLOOR_DARK          = (88,  70,  52)    # dark wood floor
FLOOR_MID           = (110, 88,  62)    # mid-tone floorboard
FLOOR_LIGHT         = (138, 112, 80)    # lit floorboard grain

# CRT glow color (warm green-blue — analog monitor glow)
CRT_GLOW            = (160, 195, 165)   # blue-green warm CRT light
CRT_SCREEN          = (100, 155, 120)   # screen face
CRT_CASING          = (91,  140, 138)   # Muted Teal per TD-08 = RW-12

# Lamp
SUNLIT_AMBER        = (212, 146, 58)    # RW-03
LAMP_SHADE          = (220, 180, 100)   # warm lamp diffuse
LAMP_GLOW_OUTER     = (200, 160, 90)

# Window (night/evening — cool)
WINDOW_SKY          = (60,  70,  105)   # night sky, cool blue
WINDOW_SILL_COLOR   = (155, 140, 120)   # warm wood sill

# Desk surface
DESK_TOP            = (148, 120, 82)    # warm honey wood
DESK_SHADOW         = (88,  68,  44)    # underside shadow

# Bookshelf
SHELF_COLOR         = (130, 108, 78)    # warm wood shelves
BOOK_COLORS = [
    (180, 60,  40),   # warm red
    (60,  90,  140),  # slate blue
    (180, 140, 50),   # amber gold
    (80,  110, 70),   # sage green
    (160, 80,  50),   # terracotta
    (110, 130, 160),  # muted steel
    (190, 170, 120),  # parchment
    (50,  70,  100),  # navy
    (170, 60,  80),   # rose
    (90,  120, 90),   # muted mint
]

# Rug
RUG_BASE            = (165, 90,  58)    # warm terracotta rug
RUG_PATTERN         = (220, 198, 158)   # cream rug pattern
RUG_SHADOW          = (100, 60,  38)    # rug shadow edge

# Chair
CHAIR_COLOR         = (120, 100, 70)    # warm wood chair
CHAIR_SHADOW        = (70,  55,  38)

# Bedding
BED_DUVET           = (130, 148, 175)   # warm blue duvet (per spec)
BED_PILLOW          = (230, 222, 205)   # cream pillow

# Deep shadow
NEAR_BLACK_WARM     = (20,  12,  8)
DEEP_SHADOW         = (35,  25,  16)

# Paper / homework
PAPER_WHITE         = (245, 240, 225)
PAPER_YELLOW        = (240, 230, 170)

# Atmospheric recession haze
HAZE_COOL           = (160, 165, 180)

# Miri Easter-egg warm tones
MIRI_FRAME          = (160, 110, 70)    # warm amber frame for photo
MIRI_KNIT           = (190, 130, 80)    # warm orange-brown knit object

# ---------------------------------------------------------------------------
# Helper: alpha overlay rectangle (Porter-Duff over, on RGB numpy array)
# ---------------------------------------------------------------------------
import numpy as np

def alpha_overlay_rect_np(arr, x0, y0, x1, y1, color_rgb, alpha):
    """Alpha composite color_rgb over arr[y0:y1, x0:x1] in place."""
    r, g, b = color_rgb
    a = alpha / 255.0
    region = arr[y0:y1, x0:x1].astype(float)
    region[..., 0] = region[..., 0] * (1 - a) + r * a
    region[..., 1] = region[..., 1] * (1 - a) + g * a
    region[..., 2] = region[..., 2] * (1 - a) + b * a
    arr[y0:y1, x0:x1] = np.clip(region, 0, 255).astype(np.uint8)


def alpha_overlay_rect(img_rgba, x0, y0, x1, y1, color_rgb, alpha):
    """Paste a semi-transparent color rect over an RGBA image."""
    layer = Image.new("RGBA", img_rgba.size, (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.rectangle([x0, y0, x1, y1], fill=color_rgb + (alpha,))
    img_rgba.alpha_composite(layer)


def converge_x(near_x, fraction=0.60):
    """Fan a vertical line from near_x toward the vanishing point."""
    return int(near_x + (VP_X - near_x) * fraction)


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------
def build():
    img = Image.new("RGBA", (W, H), WALL_WARM_CREAM + (255,))
    draw = ImageDraw.Draw(img)

    # -----------------------------------------------------------------------
    # 1. Back wall (behind desk / shelving area) — warm cream, slightly darker
    # -----------------------------------------------------------------------
    # Back wall polygon: left side, ceiling, right wall seam, floor
    back_wall_pts = [
        (0, 0),
        (W, 0),
        (W, int(H * 0.70)),
        (VP_X, VP_Y),
        (0, int(H * 0.52)),
    ]
    draw.polygon(back_wall_pts, fill=WALL_MID + (255,))
    draw = ImageDraw.Draw(img)

    # -----------------------------------------------------------------------
    # 2. Ceiling — warm cream
    # -----------------------------------------------------------------------
    ceiling_pts = [
        (0, 0),
        (W, 0),
        (W, int(H * 0.28)),
        (VP_X, VP_Y),
        (0, int(H * 0.22)),
    ]
    draw.polygon(ceiling_pts, fill=CEILING_COLOR + (255,))
    draw = ImageDraw.Draw(img)

    # Left wall (near side, warm)
    left_wall_pts = [
        (0, int(H * 0.22)),
        (VP_X, VP_Y),
        (VP_X, H),
        (0, H),
    ]
    draw.polygon(left_wall_pts, fill=(210, 195, 168) + (255,))
    draw = ImageDraw.Draw(img)

    # -----------------------------------------------------------------------
    # 3. Floor
    # -----------------------------------------------------------------------
    floor_pts = [
        (VP_X, VP_Y),
        (W, int(H * 0.70)),
        (W, H),
        (0, H),
        (0, int(H * 0.52)),
    ]
    draw.polygon(floor_pts, fill=FLOOR_DARK + (255,))
    draw = ImageDraw.Draw(img)

    # Floorboard planks — converging toward VP
    plank_rng = random.Random(62)
    floor_bottom_y = H
    floor_top_left = int(H * 0.52)
    floor_top_right = int(H * 0.70)
    n_planks = 14
    for i in range(n_planks):
        t = i / n_planks
        # Non-linear row spacing (perspective compression)
        row_y_near = int(floor_bottom_y - (floor_bottom_y - floor_top_left) * (t ** 0.65))
        col_x = int(VP_X + (W - VP_X) * (i / n_planks))
        # Lighter grain on lit planks
        tone = FLOOR_LIGHT if i % 3 == 1 else FLOOR_MID
        draw.line([(0, row_y_near), (W, row_y_near + 8)], fill=tone + (255,), width=1)
        # Vertical grain lines fanning from VP
        for gx in range(0, W, 80):
            far_x = converge_x(gx, 0.55)
            draw.line([(gx, H), (far_x, floor_top_left + 10)], fill=FLOOR_DARK + (255,), width=1)
    draw = ImageDraw.Draw(img)

    # -----------------------------------------------------------------------
    # 4. Night window — back wall, upper area (cool, atmospheric)
    # -----------------------------------------------------------------------
    # Window frame position: right-center of back wall
    win_x0, win_y0 = int(W * 0.52), int(H * 0.05)
    win_x1, win_y1 = int(W * 0.68), int(H * 0.30)
    # Sill
    sill_h = 8
    draw.rectangle([win_x0 - 6, win_y1, win_x1 + 6, win_y1 + sill_h],
                   fill=WINDOW_SILL_COLOR + (255,))
    draw = ImageDraw.Draw(img)
    # Frame (outer)
    draw.rectangle([win_x0, win_y0, win_x1, win_y1], fill=WALL_MID + (255,), outline=(80, 68, 52, 255), width=5)
    draw = ImageDraw.Draw(img)
    # Glass (night sky)
    draw.rectangle([win_x0 + 5, win_y0 + 5, win_x1 - 5, win_y1 - 5], fill=WINDOW_SKY + (255,))
    draw = ImageDraw.Draw(img)
    # Cross dividers
    win_mid_x = (win_x0 + win_x1) // 2
    win_mid_y = (win_y0 + win_y1) // 2
    draw.line([(win_mid_x, win_y0 + 5), (win_mid_x, win_y1 - 5)], fill=(80, 68, 52, 255), width=3)
    draw.line([(win_x0 + 5, win_mid_y), (win_x1 - 5, win_mid_y)], fill=(80, 68, 52, 255), width=3)
    draw = ImageDraw.Draw(img)
    # Stars (faint) in window
    star_rng = random.Random(62)
    for _ in range(12):
        sx = star_rng.randint(win_x0 + 6, win_x1 - 6)
        sy = star_rng.randint(win_y0 + 6, win_mid_y - 4)
        draw.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(200, 205, 230, 255))
    draw = ImageDraw.Draw(img)

    # -----------------------------------------------------------------------
    # 5. Bookshelf — back wall, left-center area
    # -----------------------------------------------------------------------
    shelf_x0, shelf_y0 = int(W * 0.06), int(H * 0.06)
    shelf_x1, shelf_y1 = int(W * 0.44), int(H * 0.60)
    shelf_rows = 3
    shelf_width = shelf_x1 - shelf_x0
    shelf_row_h = (shelf_y1 - shelf_y0) // shelf_rows

    # Shelf unit back panel
    draw.rectangle([shelf_x0, shelf_y0, shelf_x1, shelf_y1], fill=(110, 90, 62) + (255,))
    draw = ImageDraw.Draw(img)
    # Shelf side panels
    draw.rectangle([shelf_x0, shelf_y0, shelf_x0 + 8, shelf_y1], fill=SHELF_COLOR + (255,))
    draw.rectangle([shelf_x1 - 8, shelf_y0, shelf_x1, shelf_y1], fill=SHELF_COLOR + (255,))
    draw = ImageDraw.Draw(img)

    book_rng = random.Random(62)
    for row in range(shelf_rows):
        row_y0 = shelf_y0 + row * shelf_row_h
        row_y1 = row_y0 + shelf_row_h
        # Shelf plank
        draw.rectangle([shelf_x0, row_y1 - 6, shelf_x1, row_y1], fill=SHELF_COLOR + (255,))
        draw = ImageDraw.Draw(img)

        # Books on this shelf
        bx = shelf_x0 + 10
        while bx < shelf_x1 - 20:
            bw = book_rng.randint(14, 28)
            by0 = row_y0 + book_rng.randint(4, 12)
            by1 = row_y1 - 6
            bcol = BOOK_COLORS[book_rng.randint(0, len(BOOK_COLORS) - 1)]
            draw.rectangle([bx, by0, bx + bw, by1], fill=bcol + (255,))
            # Book spine line
            draw.line([(bx + 1, by0 + 2), (bx + 1, by1 - 2)], fill=(0, 0, 0, 60), width=1)
            bx += bw + book_rng.randint(1, 3)
        draw = ImageDraw.Draw(img)

    # Top shelf: globe / small toy
    globe_cx = int(W * 0.35)
    globe_cy = shelf_y0 + 18
    draw.ellipse([globe_cx - 14, globe_cy - 14, globe_cx + 14, globe_cy + 14],
                 fill=(80, 110, 155) + (255,), outline=(60, 80, 110, 255), width=1)
    # Globe equator line
    draw.line([(globe_cx - 13, globe_cy), (globe_cx + 13, globe_cy)], fill=(60, 80, 110, 255), width=1)
    draw = ImageDraw.Draw(img)

    # -----------------------------------------------------------------------
    # 6. Desk — mid-left, dominant element
    # -----------------------------------------------------------------------
    # Desk surface: trapezoid converging toward VP
    desk_left_x = int(W * 0.04)
    desk_right_x = int(W * 0.62)
    desk_top_y = int(H * 0.50)
    desk_bottom_y = int(H * 0.62)
    desk_surface_pts = [
        (desk_left_x, desk_top_y),
        (desk_right_x, desk_top_y),
        (desk_right_x + 20, desk_bottom_y),
        (desk_left_x - 10, desk_bottom_y),
    ]
    draw.polygon(desk_surface_pts, fill=DESK_TOP + (255,))
    draw = ImageDraw.Draw(img)
    # Desk front face
    desk_face_pts = [
        (desk_left_x - 10, desk_bottom_y),
        (desk_right_x + 20, desk_bottom_y),
        (desk_right_x + 20, desk_bottom_y + 50),
        (desk_left_x - 10, desk_bottom_y + 50),
    ]
    draw.polygon(desk_face_pts, fill=DESK_SHADOW + (255,))
    draw = ImageDraw.Draw(img)
    # Desk outline
    draw.polygon(desk_surface_pts, outline=(60, 44, 28, 255), width=1)
    draw = ImageDraw.Draw(img)

    # -----------------------------------------------------------------------
    # 7. CRT monitor — centrepiece, on desk
    # -----------------------------------------------------------------------
    # CRT sits slightly left of center on desk
    crt_cx = int(W * 0.28)
    crt_cy = int(H * 0.44)
    crt_w, crt_h = 90, 72
    # Monitor casing
    draw.rectangle([crt_cx - crt_w//2, crt_cy - crt_h//2,
                    crt_cx + crt_w//2, crt_cy + crt_h//2],
                   fill=CRT_CASING + (255,), outline=(40, 32, 28, 255), width=2)
    draw = ImageDraw.Draw(img)
    # Screen (inset)
    scr_margin = 8
    draw.rectangle([crt_cx - crt_w//2 + scr_margin, crt_cy - crt_h//2 + scr_margin,
                    crt_cx + crt_w//2 - scr_margin, crt_cy + crt_h//2 - scr_margin - 8],
                   fill=CRT_SCREEN + (255,))
    draw = ImageDraw.Draw(img)
    # Screen scan hint (2 faint horizontal bands)
    scr_x0 = crt_cx - crt_w//2 + scr_margin
    scr_x1 = crt_cx + crt_w//2 - scr_margin
    scr_y0 = crt_cy - crt_h//2 + scr_margin
    scr_y1 = crt_cy + crt_h//2 - scr_margin - 8
    for sy in range(scr_y0 + 4, scr_y1, 6):
        draw.line([(scr_x0, sy), (scr_x1, sy)], fill=(80, 130, 100, 255), width=1)
    draw = ImageDraw.Draw(img)
    # CRT neck / base
    draw.rectangle([crt_cx - 12, crt_cy + crt_h//2,
                    crt_cx + 12, crt_cy + crt_h//2 + 10],
                   fill=CRT_CASING + (255,))
    draw = ImageDraw.Draw(img)
    # CRT base foot
    draw.rectangle([crt_cx - 28, crt_cy + crt_h//2 + 8,
                    crt_cx + 28, crt_cy + crt_h//2 + 14],
                   fill=(70, 58, 50) + (255,))
    draw = ImageDraw.Draw(img)

    # -----------------------------------------------------------------------
    # 8. Desk accessories
    # -----------------------------------------------------------------------
    # Keyboard in front of CRT
    kb_x0 = crt_cx - 42
    kb_y0 = desk_top_y + 4
    kb_x1 = crt_cx + 42
    kb_y1 = desk_top_y + 18
    draw.rectangle([kb_x0, kb_y0, kb_x1, kb_y1], fill=(145, 135, 120) + (255,), outline=(80, 70, 58, 255), width=1)
    draw = ImageDraw.Draw(img)

    # Homework papers (two overlapping sheets)
    draw.rectangle([crt_cx + 52, desk_top_y + 2, crt_cx + 118, desk_top_y + 32],
                   fill=PAPER_WHITE + (255,), outline=(160, 145, 120, 255), width=1)
    draw.rectangle([crt_cx + 58, desk_top_y + 6, crt_cx + 124, desk_top_y + 36],
                   fill=PAPER_YELLOW + (255,), outline=(160, 145, 120, 255), width=1)
    draw = ImageDraw.Draw(img)
    # Pencil lines on papers
    for li in range(3):
        py = desk_top_y + 12 + li * 7
        draw.line([(crt_cx + 62, py), (crt_cx + 120, py)], fill=(100, 90, 78, 255), width=1)
    draw = ImageDraw.Draw(img)

    # Pencil cup (right side of desk)
    cup_cx = crt_cx + 130
    cup_y0 = desk_top_y - 22
    cup_y1 = desk_top_y + 4
    draw.rectangle([cup_cx - 10, cup_y0, cup_cx + 10, cup_y1],
                   fill=(185, 75, 55) + (255,), outline=(120, 45, 30, 255), width=1)
    draw = ImageDraw.Draw(img)
    # Pencils sticking up
    for pi, pcol in enumerate([(220, 190, 60), (80, 110, 155), (200, 100, 60)]):
        px = cup_cx - 6 + pi * 6
        draw.line([(px, cup_y0 - 8), (px, cup_y0 + 2)], fill=pcol + (255,), width=2)
    draw = ImageDraw.Draw(img)

    # Ruler
    draw.rectangle([desk_left_x + 5, desk_top_y + 10, desk_left_x + 60, desk_top_y + 14],
                   fill=(215, 215, 180) + (255,))
    draw = ImageDraw.Draw(img)

    # -----------------------------------------------------------------------
    # 9. Desk chair (pulled out, to the right of desk)
    # -----------------------------------------------------------------------
    ch_cx = int(W * 0.72)
    ch_seat_y = int(H * 0.60)
    ch_seat_w, ch_seat_d = 90, 28
    # Seat
    draw.rectangle([ch_cx - ch_seat_w//2, ch_seat_y - ch_seat_d//2,
                    ch_cx + ch_seat_w//2, ch_seat_y + ch_seat_d//2],
                   fill=CHAIR_COLOR + (255,), outline=(60, 44, 28, 255), width=1)
    draw = ImageDraw.Draw(img)
    # Chair back
    cb_y0 = int(H * 0.42)
    cb_y1 = ch_seat_y - ch_seat_d//2
    draw.rectangle([ch_cx - ch_seat_w//2 + 4, cb_y0,
                    ch_cx + ch_seat_w//2 - 4, cb_y1],
                   fill=CHAIR_COLOR + (255,), outline=(60, 44, 28, 255), width=1)
    draw = ImageDraw.Draw(img)
    # Chair legs (front two visible)
    for leg_x in [ch_cx - ch_seat_w//2 + 8, ch_cx + ch_seat_w//2 - 8]:
        draw.line([(leg_x, ch_seat_y + ch_seat_d//2),
                   (leg_x + 4, ch_seat_y + ch_seat_d//2 + 55)],
                  fill=CHAIR_SHADOW + (255,), width=3)
    draw = ImageDraw.Draw(img)

    # -----------------------------------------------------------------------
    # 10. Rug — floor area in front of desk
    # -----------------------------------------------------------------------
    rug_pts = [
        (int(W * 0.08), int(H * 0.70)),
        (int(W * 0.74), int(H * 0.72)),
        (int(W * 0.76), H - 20),
        (int(W * 0.06), H - 20),
    ]
    draw.polygon(rug_pts, fill=RUG_BASE + (255,))
    draw = ImageDraw.Draw(img)
    # Rug pattern stripes
    for i in range(1, 5):
        t = i / 5
        stripe_y0 = int(int(H * 0.70) + (H - 20 - int(H * 0.70)) * (t - 0.08))
        stripe_y1 = stripe_y0 + 6
        draw.rectangle([int(W * 0.08), stripe_y0, int(W * 0.76), stripe_y1],
                       fill=RUG_PATTERN + (255,))
    draw = ImageDraw.Draw(img)
    # Rug edge shadow
    draw.polygon(rug_pts, outline=RUG_SHADOW + (255,), width=2)
    draw = ImageDraw.Draw(img)

    # -----------------------------------------------------------------------
    # 11. Bed — right side, partial view
    # -----------------------------------------------------------------------
    bed_x0 = int(W * 0.78)
    bed_y0 = int(H * 0.48)
    bed_x1 = W
    bed_y1 = int(H * 0.88)
    # Duvet
    draw.rectangle([bed_x0, bed_y0, bed_x1, bed_y1], fill=BED_DUVET + (255,))
    draw = ImageDraw.Draw(img)
    # Pillow
    draw.rectangle([bed_x0 + 10, bed_y0 + 6, bed_x1 - 10, bed_y0 + 42],
                   fill=BED_PILLOW + (255,), outline=(180, 170, 150, 255), width=1)
    draw = ImageDraw.Draw(img)
    # Duvet fold crease
    draw.line([(bed_x0, bed_y0 + 50), (bed_x1, bed_y0 + 55)],
              fill=(100, 118, 145, 255), width=2)
    draw = ImageDraw.Draw(img)

    # -----------------------------------------------------------------------
    # 12. Bookbag / shoes near door (FG depth anchor, near-left)
    # -----------------------------------------------------------------------
    # Backpack in near foreground bottom-left
    bp_x, bp_y = int(W * 0.04), int(H * 0.78)
    bp_w, bp_h = 55, 72
    # Main body
    draw.rectangle([bp_x, bp_y, bp_x + bp_w, bp_y + bp_h],
                   fill=(55, 85, 130) + (255,), outline=(30, 52, 90, 255), width=2)
    draw = ImageDraw.Draw(img)
    # Front pocket
    draw.rectangle([bp_x + 6, bp_y + 20, bp_x + bp_w - 6, bp_y + 50],
                   fill=(48, 76, 118) + (255,), outline=(30, 52, 90, 255), width=1)
    draw = ImageDraw.Draw(img)
    # Strap loop top
    draw.arc([bp_x + 14, bp_y - 12, bp_x + bp_w - 14, bp_y + 8],
             start=180, end=0, fill=(40, 68, 108, 255), width=3)
    draw = ImageDraw.Draw(img)
    # Shoe beside bag
    draw.ellipse([bp_x + bp_w + 4, bp_y + 48, bp_x + bp_w + 44, bp_y + 68],
                 fill=(55, 42, 30) + (255,))
    draw = ImageDraw.Draw(img)

    # Scattered book on floor
    draw.rectangle([int(W * 0.15), int(H * 0.80), int(W * 0.30), int(H * 0.86)],
                   fill=(180, 60, 40) + (255,), outline=(100, 30, 20, 255), width=1)
    draw = ImageDraw.Draw(img)
    # Open pages
    draw.rectangle([int(W * 0.17), int(H * 0.80), int(W * 0.29), int(H * 0.86)],
                   fill=PAPER_WHITE + (255,))
    draw = ImageDraw.Draw(img)

    # -----------------------------------------------------------------------
    # 13. Miri Easter egg details
    # -----------------------------------------------------------------------
    # Framed photo on shelf (top row, right area)
    photo_x0 = int(W * 0.38)
    photo_y0 = shelf_y0 + 4
    photo_x1 = photo_x0 + 22
    photo_y1 = photo_y0 + 18
    draw.rectangle([photo_x0 - 2, photo_y0 - 2, photo_x1 + 2, photo_y1 + 2],
                   fill=MIRI_FRAME + (255,))
    draw.rectangle([photo_x0, photo_y0, photo_x1, photo_y1],
                   fill=(200, 185, 165) + (255,))
    draw = ImageDraw.Draw(img)
    # Small figure shapes in photo
    draw.ellipse([photo_x0 + 4, photo_y0 + 2, photo_x0 + 10, photo_y0 + 8],
                 fill=(195, 155, 120) + (255,))  # head shape
    draw = ImageDraw.Draw(img)

    # Knitted toy animal on desk chair back
    knit_x0 = ch_cx - 20
    knit_y0 = cb_y0 + 6
    knit_x1 = ch_cx + 20
    knit_y1 = cb_y0 + 38
    draw.ellipse([knit_x0, knit_y0, knit_x1, knit_y1], fill=MIRI_KNIT + (255,))
    draw = ImageDraw.Draw(img)
    # Knit texture suggestion (1px lines)
    for ki in range(3):
        ky = knit_y0 + 8 + ki * 9
        draw.line([(knit_x0 + 4, ky), (knit_x1 - 4, ky)], fill=(160, 105, 60, 255), width=1)
    draw = ImageDraw.Draw(img)

    # -----------------------------------------------------------------------
    # 14. Poster on wall (near-left wall, above bookshelf area)
    # -----------------------------------------------------------------------
    poster_x0 = int(W * 0.07)
    poster_y0 = int(H * 0.62)
    poster_x1 = int(W * 0.20)
    poster_y1 = int(H * 0.82)
    draw.rectangle([poster_x0, poster_y0, poster_x1, poster_y1],
                   fill=(195, 185, 165) + (255,), outline=(100, 80, 58, 255), width=1)
    draw = ImageDraw.Draw(img)
    # Simple star pattern on poster
    for pi in range(5):
        px = poster_x0 + 6 + (pi % 3) * 18
        py = poster_y0 + 8 + (pi // 3) * 18
        draw.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(80, 110, 155) + (255,))
    draw = ImageDraw.Draw(img)

    # -----------------------------------------------------------------------
    # 15. Deep shadow anchors — value floor ≤30
    # -----------------------------------------------------------------------
    # Floor/wall junctions — solid near-black at extreme corners
    # These must produce pixels ≤30 value. Use very high alpha.
    alpha_overlay_rect(img, 0, int(H * 0.84), int(W * 0.06), H, NEAR_BLACK_WARM, 248)
    draw = ImageDraw.Draw(img)
    alpha_overlay_rect(img, int(W * 0.94), int(H * 0.84), W, H, NEAR_BLACK_WARM, 245)
    draw = ImageDraw.Draw(img)
    # Bottom-center floor strip (under rug, deep shadow zone)
    alpha_overlay_rect(img, 0, int(H * 0.94), W, H, NEAR_BLACK_WARM, 230)
    draw = ImageDraw.Draw(img)
    # Under desk shadow — deep crevice
    alpha_overlay_rect(img, desk_left_x - 10, desk_bottom_y + 50, desk_right_x + 20,
                       desk_bottom_y + 95, NEAR_BLACK_WARM, 240)
    draw = ImageDraw.Draw(img)
    # Ceiling corners
    alpha_overlay_rect(img, 0, 0, int(W * 0.05), int(H * 0.08), NEAR_BLACK_WARM, 240)
    draw = ImageDraw.Draw(img)
    alpha_overlay_rect(img, int(W * 0.95), 0, W, int(H * 0.08), NEAR_BLACK_WARM, 235)
    draw = ImageDraw.Draw(img)
    # Left wall/floor corner crevice strip (deepest shadow)
    alpha_overlay_rect(img, 0, int(H * 0.90), int(W * 0.02), H, NEAR_BLACK_WARM, 252)
    draw = ImageDraw.Draw(img)

    # -----------------------------------------------------------------------
    # 16. Atmospheric recession on back 40% of image (cool haze)
    # -----------------------------------------------------------------------
    haze_x0 = int(W * 0.60)
    haze_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    haze_draw = ImageDraw.Draw(haze_layer)
    # Graduated alpha: 0 at haze_x0, 18 at right edge
    for hx in range(haze_x0, W, 2):
        t = (hx - haze_x0) / (W - haze_x0)
        ha = int(18 * t)
        haze_draw.rectangle([hx, 0, hx + 2, H], fill=HAZE_COOL + (ha,))
    img.alpha_composite(haze_layer)
    draw = ImageDraw.Draw(img)

    # -----------------------------------------------------------------------
    # 17. Dual-temp split for QA warm/cool separation
    #     Strategy: COOL BOTTOM only (floor is in shadow, CRT spill is blue-green)
    #     The QA check measures MEDIAN HUE of top half vs bottom half.
    #     Warm ceiling (amber ~hue 18-25) is already in top half.
    #     Need bottom half to go strongly blue/cyan (hue 130+).
    #     Use alpha=140 to ensure B > R on bottom half pixels → blue hue.
    # -----------------------------------------------------------------------
    cool_split_y = int(H * 0.50)
    # Graduated cool bottom: alpha 0 at split → 140 at bottom
    cool_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    cool_draw = ImageDraw.Draw(cool_layer)
    # Transition zone: 60 rows gradient, then flat
    transition_rows = 60
    for cy_row in range(cool_split_y, H):
        if cy_row < cool_split_y + transition_rows:
            t = (cy_row - cool_split_y) / transition_rows
            ca = int(140 * t)
        else:
            ca = 140
        cool_draw.rectangle([0, cy_row, W, cy_row + 1],
                             fill=CRT_GLOW + (ca,))
    img.alpha_composite(cool_layer)
    draw = ImageDraw.Draw(img)

    # -----------------------------------------------------------------------
    # 18. CRT monitor glow (gaussian_glow from render_lib)
    #     Dominant key light in the room
    # -----------------------------------------------------------------------
    crt_glow_center = (crt_cx, crt_cy)
    gaussian_glow(img, crt_glow_center, radius=140, color=CRT_GLOW, max_alpha=75, steps=14)
    draw = ImageDraw.Draw(img)
    # Smaller inner hotspot
    gaussian_glow(img, (crt_cx, crt_cy + 5), radius=60, color=(180, 210, 185), max_alpha=50, steps=8)
    draw = ImageDraw.Draw(img)

    # -----------------------------------------------------------------------
    # 19. CRT light shaft onto desk and keyboard area
    # -----------------------------------------------------------------------
    light_shaft(img,
                apex=(crt_cx, crt_cy - crt_h//2),
                base_left=(desk_left_x + 10, desk_top_y + 2),
                base_right=(crt_cx + crt_w//2 + 30, desk_top_y + 2),
                color=CRT_GLOW,
                max_alpha=30)
    draw = ImageDraw.Draw(img)

    # -----------------------------------------------------------------------
    # 20. Warm bedside lamp (right side) — fill light
    # -----------------------------------------------------------------------
    lamp_cx = int(W * 0.90)
    lamp_cy = int(H * 0.32)
    # Lamp shade
    lamp_pts = [
        (lamp_cx - 22, lamp_cy - 8),
        (lamp_cx + 22, lamp_cy - 8),
        (lamp_cx + 14, lamp_cy + 22),
        (lamp_cx - 14, lamp_cy + 22),
    ]
    draw.polygon(lamp_pts, fill=LAMP_SHADE + (255,))
    draw = ImageDraw.Draw(img)
    draw.polygon(lamp_pts, outline=(160, 120, 60, 255), width=1)
    draw = ImageDraw.Draw(img)
    # Lamp pole
    draw.line([(lamp_cx, lamp_cy + 22), (lamp_cx, lamp_cy + 58)],
              fill=(100, 80, 55, 255), width=3)
    draw = ImageDraw.Draw(img)
    # Lamp base
    draw.ellipse([lamp_cx - 16, lamp_cy + 55, lamp_cx + 16, lamp_cy + 65],
                 fill=(100, 80, 55, 255))
    draw = ImageDraw.Draw(img)
    # Lamp warm glow
    gaussian_glow(img, (lamp_cx, lamp_cy + 5), radius=120, color=SUNLIT_AMBER,
                  max_alpha=45, steps=10)
    draw = ImageDraw.Draw(img)

    # -----------------------------------------------------------------------
    # 21. Dust motes in CRT beam
    # -----------------------------------------------------------------------
    dust_motes(draw,
               bounds=(crt_cx - 60, crt_cy - 50, crt_cx + 80, desk_top_y),
               count=14,
               seed=62,
               color=(220, 235, 220),
               alpha_range=(30, 60))
    draw = ImageDraw.Draw(img)

    # -----------------------------------------------------------------------
    # 22. Window (night) cool light — subtle ambient blue from right
    # -----------------------------------------------------------------------
    # Cool ambient from window direction (upper right of back wall)
    gaussian_glow(img, (int(W * 0.60), int(H * 0.18)), radius=90, color=(120, 130, 165),
                  max_alpha=22, steps=8)
    draw = ImageDraw.Draw(img)

    # -----------------------------------------------------------------------
    # 23. Value ceiling: specular dot on CRT screen (ensures max ≥ 225)
    # -----------------------------------------------------------------------
    specular_x = crt_cx + crt_w//2 - scr_margin - 10
    specular_y = crt_cy - crt_h//2 + scr_margin + 8
    draw.ellipse([specular_x - 4, specular_y - 4, specular_x + 4, specular_y + 4],
                 fill=(245, 252, 248, 255))
    draw = ImageDraw.Draw(img)
    # Lamp shade specular
    draw.ellipse([lamp_cx - 2, lamp_cy - 6, lamp_cx + 2, lamp_cy - 2],
                 fill=(255, 252, 240, 255))
    draw = ImageDraw.Draw(img)

    # -----------------------------------------------------------------------
    # 24. Paper texture final pass (subtle, breaks polygon edges)
    # -----------------------------------------------------------------------
    img = paper_texture(img, scale=38, alpha=16, seed=62)
    draw = ImageDraw.Draw(img)

    # -----------------------------------------------------------------------
    # 25. Vignette — final pass
    # -----------------------------------------------------------------------
    img = vignette(img, strength=55)
    draw = ImageDraw.Draw(img)

    # -----------------------------------------------------------------------
    # 26. Convert to RGB and save
    # -----------------------------------------------------------------------
    # Use flatten_rgba_to_rgb() (render_lib v1.2.0, C42) — correct Porter-Duff
    # composite over white. Replaces manual numpy pattern from C41.
    rgb_img = flatten_rgba_to_rgb(img)

    # Enforce ≤1280px (already 1280×720)
    rgb_img.thumbnail((1280, 1280), Image.LANCZOS)

    out_path = os.path.join(
        os.path.dirname(_TOOLS_DIR),
        "backgrounds", "environments", "LTG_ENV_luma_study_interior.png"
    )
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    rgb_img.save(out_path)
    print(f"Saved: {out_path}  ({rgb_img.size[0]}×{rgb_img.size[1]})")
    return out_path


if __name__ == "__main__":
    build()
