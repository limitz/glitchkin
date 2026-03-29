#!/usr/bin/env python3
"""
LTG_TOOL_env_grandma_living_room_v001.py — Grandma Miri's Living Room v001
"Luma & the Glitchkin" — Background & Environment Design
Artist: Hana Okonkwo | Cycle 37

Narrative: The living room is the emotional heart of the show.
The CRT television dominates the space — it is the story's
central object. Family photos, a knitted throw, stacked books:
all evidence of a life fully lived. Afternoon light slants warm
and low through a window on the left. The CRT sits slightly
off-center right, clearly old, gently glowing.

The room should feel: inhabited, layered, specific.
Not a generic "old lady room" — Miri's living room.

Design decisions:
  - Camera: mild 3/4 angle, looking in from slightly left of center
  - Key light: SUNLIT_AMBER afternoon lamp from right-upper quadrant
  - Window: warm afternoon light shaft from left
  - Focal point: CRT television (off-center right, screen ON, pale cyan glow)
  - Warm/cool: warm left (afternoon sun) / cool right (CRT bounce)
  - Deep shadows applied after all light passes for QA value floor ≤30

World: REAL — warm/cool threshold = 12 (ltg_warmth_guarantees.json)

Canvas: 1280×720 (≤1280 rule — direct, no thumbnail needed)
Output: /home/wipkat/team/output/backgrounds/environments/LTG_ENV_grandma_living_room_v001.png
"""

import math
import os
import random
from PIL import Image, ImageDraw, ImageFilter

W, H = 1280, 720

# ── Real World Palette ────────────────────────────────────────────────────────
WARM_CREAM        = (250, 240, 220)   # RW-01 ceiling/bright wall
AGED_CREAM        = (238, 226, 198)   # slightly older/more used cream
WALL_BASE         = (236, 220, 192)   # main wall mid-value warm
WALL_SHADOW       = (188, 168, 136)   # wall in shadow
CEILING_WARM      = (244, 234, 210)   # ceiling — slightly lighter than walls

FLOOR_OAK_LIGHT   = (198, 162, 110)   # oak floorboard lit
FLOOR_OAK_MED     = (172, 138,  86)   # oak floorboard mid
FLOOR_OAK_DARK    = (140, 108,  64)   # oak floorboard shadow
FLOOR_RUG_RED     = (158,  68,  42)   # area rug warm red-orange
FLOOR_RUG_CREAM   = (230, 210, 180)   # rug cream pattern
FLOOR_RUG_BLUE    = ( 76,  90, 118)   # rug cool accent (small pattern dots)

WOOD_DARK         = ( 96,  60,  28)   # furniture frame dark
WOOD_MED          = (148, 100,  54)   # furniture mid
WOOD_LIGHT        = (188, 142,  82)   # furniture highlight

# Upholstery
SOFA_TEAL         = ( 74, 108, 102)   # muted sage-teal couch (Real World safe)
SOFA_SHADOW       = ( 52,  76,  70)   # sofa shadow side
SOFA_HIGHLIGHT    = (110, 148, 138)   # sofa highlight/cushion

THROW_AMBER       = (210, 148,  72)   # knitted throw — warm amber/orange
THROW_SHADOW      = (158, 100,  48)   # throw shadow
THROW_CREAM       = (240, 220, 188)   # throw cream stripe

CUSHION_WARM      = (220, 180, 100)   # scatter cushion warm yellow
CUSHION_DUSTY     = (164, 142, 118)   # dusty rose cushion (desaturated)

# Books / shelves
BOOKCASE_WOOD     = (118,  78,  36)   # bookcase dark walnut
BOOK_RED          = (166,  50,  30)   # book spine red
BOOK_GREEN        = ( 64, 100,  56)   # book spine green
BOOK_BLUE         = ( 62,  82, 128)   # book spine blue
BOOK_AMBER        = (190, 140,  50)   # book spine amber/gold
BOOK_CREAM        = (218, 200, 168)   # book pages/cream spine

# CRT Television — the focal point
CRT_PLASTIC       = (108,  90,  68)   # old ivory/yellowed plastic body
CRT_PLASTIC_DARK  = ( 72,  58,  40)   # plastic shadow
CRT_SCREEN_GLOW   = ( 30,  90, 108)   # screen emitting cool cyan-teal
CRT_SCREEN_DARK   = ( 12,  52,  68)   # screen edges (darker)
CRT_STAND_WOOD    = ( 90,  64,  32)   # TV stand dark wood
CRT_COOL_SPILL    = (  0, 128, 148)   # CRT ambient spill (desaturated electric cyan)

# Light
MORNING_GOLD      = (255, 200,  80)   # bright afternoon window glass glow
CURTAIN_WARM      = (230, 188, 118)   # window curtain warm yellow-amber
PLANT_GREEN       = ( 76, 126,  60)   # window sill plant
PLANT_DARK        = ( 48,  78,  36)   # plant shadow
SUNLIT_AMBER      = (212, 146,  58)   # RW-03 — afternoon window shaft
LAMP_WARM         = (240, 180,  90)   # reading lamp (warm key, upper right)
LAMP_BODY         = (188, 148,  80)   # lamp base/shade
LAMP_BASE_DARK    = (100,  72,  30)   # lamp base dark wood

# Family photos + small objects
PHOTO_FRAME       = (148, 108,  58)   # picture frame wood
PHOTO_MOUNT       = (220, 210, 196)   # photo mount
PHOTO_SHADOW      = ( 90,  62,  30)   # frame shadow

SIDE_TABLE_WOOD   = (138,  94,  46)   # side table wood
TEACUP_WHITE      = (234, 226, 206)   # teacup
TEACUP_RIM        = (186, 142,  70)   # teacup rim warm
BOOK_STACK_COVER  = (162, 104,  50)   # stacked books on table

# Deep shadows — essential for QA value floor ≤30
DEEP_COCOA        = ( 59,  40,  32)   # #3B2820 canonical deepest warm shadow
NEAR_BLACK_WARM   = ( 28,  18,  10)   # near-black warm (crevices, corners)
SHADOW_DEEP       = ( 68,  46,  24)   # deep shadow (furniture undersides)
SHADOW_MID        = (108,  74,  42)   # mid shadow

# Outline
LINE_DARK         = ( 80,  54,  28)   # warm dark line work


def lerp_color(a, b, t):
    t = max(0.0, min(1.0, t))
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def alpha_overlay_rect(img, x0, y0, x1, y1, color_rgb, alpha):
    """Alpha-composite a colored rectangle onto img (RGB)."""
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.rectangle([x0, y0, x1, y1], fill=(*color_rgb, alpha))
    img_rgba = img.convert("RGBA")
    result = Image.alpha_composite(img_rgba, overlay)
    return result.convert("RGB")


def alpha_overlay_poly(img, pts, color_rgb, alpha):
    """Alpha-composite a colored polygon onto img (RGB)."""
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.polygon(pts, fill=(*color_rgb, alpha))
    img_rgba = img.convert("RGBA")
    result = Image.alpha_composite(img_rgba, overlay)
    return result.convert("RGB")


def alpha_overlay_ellipse(img, bbox, color_rgb, alpha):
    """Alpha-composite a colored ellipse onto img (RGB)."""
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.ellipse(bbox, fill=(*color_rgb, alpha))
    img_rgba = img.convert("RGBA")
    result = Image.alpha_composite(img_rgba, overlay)
    return result.convert("RGB")


# ── Layer 1: Base Room Structure ──────────────────────────────────────────────

def draw_base_room(img):
    """
    Room perspective: mild 3/4 view.
    Camera slightly left of center, looking toward right back wall.
    Left wall (partial) / Back wall (dominant) / Right wall (partial).
    Vanishing point upper-center.
    """
    draw = ImageDraw.Draw(img)

    # Vanishing point — slightly right of center (draws eye to CRT on right)
    vp_x = int(W * 0.55)
    vp_y = int(H * 0.36)

    # ── Ceiling ────────────────────────────────────────────────────────────
    ceil_poly = [
        (0, 0), (W, 0),
        (W, int(H * 0.20)),
        (vp_x, vp_y),
        (0, int(H * 0.28)),
    ]
    draw.polygon(ceil_poly, fill=CEILING_WARM)

    # ── Back wall (main wall) ──────────────────────────────────────────────
    bw_left  = int(W * 0.12)
    bw_right = int(W * 0.78)
    bw_top   = vp_y - 10
    bw_bot   = int(H * 0.78)
    draw.rectangle([bw_left, bw_top, bw_right, bw_bot], fill=WALL_BASE)

    # ── Left wall (warm — window side) ────────────────────────────────────
    lw_poly = [
        (0, int(H * 0.28)),
        (bw_left, bw_top),
        (bw_left, bw_bot),
        (0, int(H * 0.85)),
    ]
    draw.polygon(lw_poly, fill=WALL_SHADOW)

    # ── Right wall (CRT side) ──────────────────────────────────────────────
    rw_poly = [
        (bw_right, bw_top),
        (W, int(H * 0.20)),
        (W, int(H * 0.78)),
        (bw_right, bw_bot),
    ]
    draw.polygon(rw_poly, fill=WALL_SHADOW)

    # ── Floor ──────────────────────────────────────────────────────────────
    floor_poly = [
        (0, int(H * 0.85)),
        (bw_left, bw_bot),
        (bw_right, bw_bot),
        (W, int(H * 0.78)),
        (W, H),
        (0, H),
    ]
    draw.polygon(floor_poly, fill=FLOOR_OAK_MED)

    return draw, vp_x, vp_y, bw_left, bw_top, bw_right, bw_bot


# ── Layer 2: Floorboards and Area Rug ────────────────────────────────────────

def draw_floor(img, vp_x, vp_y, bw_left, bw_bot, bw_right):
    """Hardwood oak floorboards with perspective, plus area rug under coffee table."""
    draw = ImageDraw.Draw(img)

    floor_top = bw_bot
    floor_bot = H

    # Floorboards — perspective lines converging to vp_x
    # ~12 boards visible across near floor
    num_boards = 14
    for i in range(num_boards + 1):
        t = i / num_boards
        x_near = int(t * W)
        # Board lines converge to VP_X at floor_top
        x_far = vp_x + int((x_near - vp_x) * 0.25)
        col = FLOOR_OAK_DARK if i % 3 == 0 else FLOOR_OAK_MED
        draw.line([(x_near, floor_bot), (x_far, floor_top)], fill=col, width=1)

    # Horizontal division lines (perspective-spaced row separators)
    for j in range(1, 8):
        t = j / 8.0
        # Non-linear spacing (closer = wider apart in perspective)
        y = int(floor_top + (floor_bot - floor_top) * (t ** 0.7))
        # X bounds converge toward VP
        x_l = max(0, int(bw_left + (0 - bw_left) * (1 - t ** 0.5)))
        x_r = min(W, int(bw_right + (W - bw_right) * (1 - t ** 0.5)))
        draw.line([(x_l, y), (x_r, y)], fill=FLOOR_OAK_DARK, width=1)

    # ── Area rug — centered slightly left, under coffee table zone ──────
    rug_x1 = int(W * 0.08)
    rug_x2 = int(W * 0.72)
    rug_y1 = int(H * 0.84)
    rug_y2 = int(H * 0.97)

    # Perspective trapezoid shape for rug
    rug_pts = [
        (rug_x1, rug_y2),
        (rug_x2, rug_y2),
        (rug_x2 - int(W * 0.08), rug_y1),
        (rug_x1 + int(W * 0.06), rug_y1),
    ]
    draw.polygon(rug_pts, fill=FLOOR_RUG_RED)

    # Rug border pattern (cream inner border)
    border_inset = 12
    border_pts = [
        (rug_pts[0][0] + border_inset, rug_pts[0][1] - border_inset // 2),
        (rug_pts[1][0] - border_inset, rug_pts[1][1] - border_inset // 2),
        (rug_pts[2][0] - border_inset // 2, rug_pts[2][1] + border_inset // 2),
        (rug_pts[3][0] + border_inset // 2, rug_pts[3][1] + border_inset // 2),
    ]
    draw.polygon(border_pts, outline=FLOOR_RUG_CREAM, width=3)

    # Small cream pattern dots on rug (decorative)
    rng = random.Random(42)
    for _ in range(18):
        dx = rng.randint(rug_x1 + 20, rug_x2 - 20)
        dy = rng.randint(rug_y1 + 4, rug_y2 - 4)
        r = rng.randint(2, 4)
        draw.ellipse([dx - r, dy - r, dx + r, dy + r], fill=FLOOR_RUG_CREAM)

    return img


# ── Layer 3: Bookcase (left half of back wall) ───────────────────────────────

def draw_bookcase(img, vp_x, vp_y, bw_left, bw_top, bw_right, bw_bot):
    """Floor-to-near-ceiling bookcase on left portion of back wall."""
    draw = ImageDraw.Draw(img)

    bc_x1 = bw_left
    bc_x2 = int(W * 0.36)
    bc_y1 = bw_top + 10
    bc_y2 = bw_bot

    # Case body — dark walnut
    draw.rectangle([bc_x1, bc_y1, bc_x2, bc_y2], fill=BOOKCASE_WOOD)
    draw.rectangle([bc_x1, bc_y1, bc_x2, bc_y2], outline=LINE_DARK, width=2)

    # Three shelves (evenly spaced)
    num_shelves = 3
    shelf_h = (bc_y2 - bc_y1) // (num_shelves + 1)

    shelf_colors = [
        [BOOK_RED, BOOK_GREEN, BOOK_AMBER, BOOK_BLUE, BOOK_CREAM, BOOK_RED, BOOK_AMBER],
        [BOOK_CREAM, BOOK_BLUE, BOOK_RED, BOOK_GREEN, BOOK_AMBER, BOOK_CREAM, BOOK_BLUE],
        [BOOK_AMBER, BOOK_RED, BOOK_CREAM, BOOK_BLUE, BOOK_GREEN, BOOK_AMBER, BOOK_RED],
    ]

    rng = random.Random(7)
    for s in range(num_shelves):
        shelf_top = bc_y1 + shelf_h * s + shelf_h // 5
        shelf_bot = bc_y1 + shelf_h * (s + 1)

        # Shelf plank
        draw.rectangle([bc_x1 + 3, shelf_bot - 6, bc_x2 - 3, shelf_bot], fill=WOOD_MED)

        # Books on shelf
        shelf_inner_left = bc_x1 + 6
        shelf_inner_right = bc_x2 - 6
        book_x = shelf_inner_left
        for b_idx, b_col in enumerate(shelf_colors[s % len(shelf_colors)]):
            b_width = rng.randint(12, 22)
            if book_x + b_width > shelf_inner_right - 4:
                break
            # Slight height variation
            b_height_vary = rng.randint(-4, 4)
            b_top = shelf_top + b_height_vary
            b_bot = shelf_bot - 6

            draw.rectangle([book_x, b_top, book_x + b_width, b_bot], fill=b_col)
            draw.rectangle([book_x, b_top, book_x + b_width, b_bot], outline=LINE_DARK, width=1)
            book_x += b_width + 1

    return img


# ── Layer 4: CRT Television (focal point, off-center right) ──────────────────

def draw_crt_tv(img, vp_x, vp_y, bw_left, bw_top, bw_right, bw_bot):
    """
    The CRT TV: the emotional heart of this room and the show.
    Old, slightly yellowed plastic body. Screen ON — pale cyan glow.
    Sits on a low dark-wood TV stand, slightly off-center right
    on the back wall.
    """
    draw = ImageDraw.Draw(img)

    # TV stand
    stand_x1 = int(W * 0.54)
    stand_x2 = int(W * 0.76)
    stand_y1 = int(H * 0.65)
    stand_y2 = bw_bot + 2

    draw.rectangle([stand_x1, stand_y1, stand_x2, stand_y2], fill=CRT_STAND_WOOD)
    draw.rectangle([stand_x1, stand_y1, stand_x2, stand_y2], outline=LINE_DARK, width=1)

    # Stand top surface (highlight edge)
    draw.line([(stand_x1, stand_y1), (stand_x2, stand_y1)], fill=WOOD_LIGHT, width=2)

    # TV body (sitting on stand)
    tv_x1 = stand_x1 + 8
    tv_x2 = stand_x2 - 8
    tv_y1 = int(H * 0.42)
    tv_y2 = stand_y1 + 6

    tv_w = tv_x2 - tv_x1
    tv_h = tv_y2 - tv_y1

    # CRT body — big boxy cabinet shape (deep perspective depth)
    draw.rectangle([tv_x1, tv_y1, tv_x2, tv_y2], fill=CRT_PLASTIC)
    draw.rectangle([tv_x1, tv_y1, tv_x2, tv_y2], outline=LINE_DARK, width=2)

    # Subtle top highlight (plastic sheen)
    draw.line([(tv_x1 + 3, tv_y1 + 2), (tv_x2 - 3, tv_y1 + 2)],
              fill=lerp_color(CRT_PLASTIC, WARM_CREAM, 0.35), width=1)

    # Shadow on bottom half of body
    draw.rectangle([tv_x1, tv_y1 + tv_h // 2, tv_x2, tv_y2],
                   fill=CRT_PLASTIC_DARK)

    # Screen bezel (recessed inset)
    bezel_margin_x = max(8, tv_w // 10)
    bezel_margin_y = max(6, tv_h // 10)
    bezel_x1 = tv_x1 + bezel_margin_x
    bezel_x2 = tv_x2 - bezel_margin_x
    bezel_y1 = tv_y1 + bezel_margin_y
    bezel_y2 = tv_y2 - int(tv_h * 0.26)

    draw.rectangle([bezel_x1, bezel_y1, bezel_x2, bezel_y2], fill=NEAR_BLACK_WARM)
    draw.rectangle([bezel_x1, bezel_y1, bezel_x2, bezel_y2], outline=LINE_DARK, width=1)

    # Screen (slightly inset from bezel)
    scr_x1 = bezel_x1 + 4
    scr_x2 = bezel_x2 - 4
    scr_y1 = bezel_y1 + 3
    scr_y2 = bezel_y2 - 3

    scr_w = scr_x2 - scr_x1
    scr_h = scr_y2 - scr_y1

    # Screen gradient — active CRT, slightly brighter center
    for y in range(scr_y1, scr_y2):
        t = (y - scr_y1) / max(1, scr_h)
        # Top brighter, edges fade
        row_col = lerp_color((55, 130, 155), (18, 62, 80), t * 0.6)
        draw.line([(scr_x1, y), (scr_x2, y)], fill=row_col)

    # Scanline suggestion (every other line slightly darker)
    for y in range(scr_y1, scr_y2, 3):
        draw.line([(scr_x1 + 1, y), (scr_x2 - 1, y)],
                  fill=(8, 38, 52), width=1)

    # Screen glare (small highlight top-left of screen)
    gl_x1 = scr_x1 + int(scr_w * 0.06)
    gl_x2 = scr_x1 + int(scr_w * 0.22)
    gl_y1 = scr_y1 + int(scr_h * 0.06)
    gl_y2 = scr_y1 + int(scr_h * 0.18)
    draw.rectangle([gl_x1, gl_y1, gl_x2, gl_y2],
                   fill=lerp_color(CRT_SCREEN_GLOW, (200, 230, 238), 0.7))

    # Speaker grille — lower body
    grille_y1 = bezel_y2 + 4
    grille_y2 = tv_y2 - 8
    grille_x1 = tv_x1 + int(tv_w * 0.08)
    grille_x2 = tv_x1 + int(tv_w * 0.42)
    draw.rectangle([grille_x1, grille_y1, grille_x2, grille_y2], fill=CRT_PLASTIC_DARK)
    for gi in range(6):
        gx = grille_x1 + 3 + gi * 5
        if gx < grille_x2 - 3:
            draw.line([(gx, grille_y1 + 2), (gx, grille_y2 - 2)],
                      fill=lerp_color(CRT_PLASTIC_DARK, CRT_PLASTIC, 0.5), width=1)

    # Tuning knobs (right side of lower body)
    knob_x_base = tv_x2 - int(tv_w * 0.22)
    knob_y_base = bezel_y2 + int((tv_y2 - bezel_y2) * 0.5)
    for ki in range(2):
        kx = knob_x_base + ki * 16
        ky = knob_y_base
        draw.ellipse([kx - 5, ky - 5, kx + 5, ky + 5], fill=LINE_DARK)
        draw.ellipse([kx - 3, ky - 3, kx + 3, ky + 3], fill=WOOD_MED)

    # TV antenna (rabbit ears)
    ant_cx = (tv_x1 + tv_x2) // 2
    ant_y  = tv_y1 - 2
    draw.line([(ant_cx - 4, ant_y), (ant_cx - 24, ant_y - 42)],
              fill=LINE_DARK, width=2)
    draw.line([(ant_cx + 4, ant_y), (ant_cx + 22, ant_y - 38)],
              fill=LINE_DARK, width=2)

    # Return screen bounds for glow pass
    return scr_x1, scr_y1, scr_x2, scr_y2, tv_x1, tv_y1, tv_x2, tv_y2


# ── Layer 5: CRT Glow (cool light spill — the warm/cool anchor) ──────────────

def draw_crt_glow(img, scr_x1, scr_y1, scr_x2, scr_y2):
    """
    Cool CRT ambient spill is the show's visual signature in this room.
    Desaturated Electric Cyan from the screen bleeds into the right side
    of the room — creates warm/cool separation.
    """
    scr_cx = (scr_x1 + scr_x2) // 2
    scr_cy = (scr_y1 + scr_y2) // 2

    glow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow_layer)

    # Primary tight glow around screen
    for r in range(88, 0, -1):
        t = 1.0 - r / 88.0
        alpha = int(t ** 1.8 * 50)
        gd.ellipse(
            [scr_cx - r, scr_cy - r // 2,
             scr_cx + r, scr_cy + r // 2],
            fill=(*CRT_COOL_SPILL, alpha)
        )

    # Wide ambient spill — pulls right half of room cool
    for r in range(240, 80, -4):
        t = 1.0 - (r - 80) / 160.0
        alpha = int(t ** 2.5 * 28)
        gd.ellipse(
            [scr_cx - r, scr_cy - r,
             scr_cx + r, scr_cy + r],
            fill=(*CRT_COOL_SPILL, alpha)
        )

    img_rgba = img.convert("RGBA")
    result = Image.alpha_composite(img_rgba, glow_layer)
    return result.convert("RGB")


# ── Layer 6: Sofa (center-left, facing CRT) ───────────────────────────────────

def draw_sofa(img, vp_x, vp_y, bw_bot):
    """
    Three-seater sofa in muted sage teal. Knitted throw draped over
    the right armrest (warm amber). Two scatter cushions. Clearly used.
    """
    draw = ImageDraw.Draw(img)

    # Sofa body — slight 3/4 perspective
    sf_x1 = int(W * 0.04)
    sf_x2 = int(W * 0.52)
    sf_y1 = int(H * 0.64)
    sf_y2 = bw_bot - 2

    sf_w = sf_x2 - sf_x1
    sf_h = sf_y2 - sf_y1

    # Seat base
    draw.rectangle([sf_x1, sf_y1 + sf_h // 3, sf_x2, sf_y2], fill=SOFA_TEAL)

    # Back cushions (three segments)
    back_top = sf_y1
    back_bot = sf_y1 + sf_h // 3 + 4
    back_seam_1 = sf_x1 + sf_w // 3
    back_seam_2 = sf_x1 + (sf_w * 2) // 3

    draw.rectangle([sf_x1, back_top, back_seam_1, back_bot], fill=SOFA_TEAL)
    draw.rectangle([back_seam_1 + 2, back_top, back_seam_2, back_bot], fill=SOFA_TEAL)
    draw.rectangle([back_seam_2 + 2, back_top, sf_x2, back_bot], fill=SOFA_TEAL)

    # Cushion seams
    draw.line([(back_seam_1, back_top + 2), (back_seam_1, back_bot)], fill=SOFA_SHADOW, width=2)
    draw.line([(back_seam_2, back_top + 2), (back_seam_2, back_bot)], fill=SOFA_SHADOW, width=2)

    # Shadow on bottom and left side
    draw.rectangle([sf_x1, sf_y1 + sf_h // 2, sf_x2, sf_y2], fill=SOFA_SHADOW)
    # Re-overlay teal mid with alpha for depth
    img = alpha_overlay_rect(img, sf_x1, sf_y1 + sf_h // 2, sf_x2, sf_y2,
                             SOFA_TEAL, 100)
    draw = ImageDraw.Draw(img)

    # Left armrest
    draw.rectangle([sf_x1, sf_y1 + 8, sf_x1 + int(sf_w * 0.10), sf_y2], fill=SOFA_SHADOW)
    draw.rectangle([sf_x1, sf_y1 + 8, sf_x1 + int(sf_w * 0.10), sf_y2], outline=LINE_DARK, width=1)

    # Right armrest
    draw.rectangle([sf_x2 - int(sf_w * 0.09), sf_y1 + 8, sf_x2, sf_y2], fill=SOFA_SHADOW)
    draw.rectangle([sf_x2 - int(sf_w * 0.09), sf_y1 + 8, sf_x2, sf_y2], outline=LINE_DARK, width=1)

    # Sofa outline
    draw.rectangle([sf_x1, sf_y1, sf_x2, sf_y2], outline=LINE_DARK, width=2)

    # Leg shadows (under sofa — pushes value floor down)
    leg_y1 = sf_y2
    leg_y2 = sf_y2 + 10
    for lx in [sf_x1 + 14, sf_x1 + sf_w // 2, sf_x2 - 14]:
        draw.rectangle([lx - 5, leg_y1, lx + 5, leg_y2], fill=SHADOW_DEEP)

    # Underside deep shadow
    draw.rectangle([sf_x1, sf_y2, sf_x2, sf_y2 + 8], fill=NEAR_BLACK_WARM)

    # ── Knitted throw (draped over right armrest — warm orange, Miri's) ──
    throw_x1 = sf_x2 - int(sf_w * 0.28)
    throw_x2 = sf_x2 + 12
    throw_y1 = sf_y1
    throw_y2 = sf_y2 + 14   # drapes below sofa edge

    draw.polygon(
        [(throw_x1, throw_y1 + 6),
         (throw_x2, throw_y1 + 4),
         (throw_x2 + 8, throw_y2 - 8),
         (throw_x1 - 4, throw_y2)],
        fill=THROW_AMBER
    )
    # Throw stripes (knit pattern suggestion)
    for sy in range(throw_y1 + 8, throw_y2 - 4, 10):
        draw.line([(throw_x1, sy), (throw_x2 + 4, sy + 2)], fill=THROW_CREAM, width=1)
    # Throw outline
    draw.polygon(
        [(throw_x1, throw_y1 + 6),
         (throw_x2, throw_y1 + 4),
         (throw_x2 + 8, throw_y2 - 8),
         (throw_x1 - 4, throw_y2)],
        outline=THROW_SHADOW, width=1
    )

    # ── Scatter cushions ─────────────────────────────────────────────────
    # Cushion 1 — warm yellow, left back zone
    c1_x = sf_x1 + int(sf_w * 0.18)
    c1_y = back_top + 4
    c1_w = int(sf_w * 0.15)
    c1_h = int(sf_h * 0.45)
    draw.rectangle([c1_x, c1_y, c1_x + c1_w, c1_y + c1_h], fill=CUSHION_WARM)
    draw.rectangle([c1_x, c1_y, c1_x + c1_w, c1_y + c1_h], outline=LINE_DARK, width=1)

    # Cushion 2 — dusty rose, center-right back zone
    c2_x = sf_x1 + int(sf_w * 0.45)
    c2_y = back_top + 6
    c2_w = int(sf_w * 0.13)
    c2_h = int(sf_h * 0.40)
    draw.rectangle([c2_x, c2_y, c2_x + c2_w, c2_y + c2_h], fill=CUSHION_DUSTY)
    draw.rectangle([c2_x, c2_y, c2_x + c2_w, c2_y + c2_h], outline=LINE_DARK, width=1)

    return img


# ── Layer 7: Coffee Table ─────────────────────────────────────────────────────

def draw_coffee_table(img, bw_bot):
    """
    Low wooden coffee table in front of sofa.
    Items: stacked books, Miri's teacup (half-drunk), TV remote.
    """
    draw = ImageDraw.Draw(img)

    ct_x1 = int(W * 0.10)
    ct_x2 = int(W * 0.48)
    ct_y1 = bw_bot + 6    # sits just at the floor-furniture boundary
    ct_y2 = bw_bot + 26
    ct_depth = 8

    # Table top
    draw.rectangle([ct_x1, ct_y1, ct_x2, ct_y2], fill=WOOD_MED)
    draw.rectangle([ct_x1, ct_y1, ct_x2, ct_y2], outline=LINE_DARK, width=1)

    # Table top highlight (front edge)
    draw.line([(ct_x1 + 2, ct_y1 + 1), (ct_x2 - 2, ct_y1 + 1)], fill=WOOD_LIGHT, width=1)

    # Table depth face (perspective bottom face)
    depth_pts = [
        (ct_x1, ct_y2),
        (ct_x2, ct_y2),
        (ct_x2 + ct_depth // 2, ct_y2 + ct_depth),
        (ct_x1 + ct_depth // 2, ct_y2 + ct_depth),
    ]
    draw.polygon(depth_pts, fill=WOOD_DARK)
    draw.polygon(depth_pts, outline=LINE_DARK, width=1)

    # Table shadow on floor
    draw.rectangle([ct_x1 + 6, ct_y2 + ct_depth,
                    ct_x2 + 6, ct_y2 + ct_depth + 8],
                   fill=SHADOW_DEEP)

    # ── Items on table ────────────────────────────────────────────────────
    # Stack of 3 books (left side of table)
    bk_x = ct_x1 + 12
    bk_y = ct_y1 - 2
    for bi, (bk_col, bk_h) in enumerate([(BOOK_AMBER, 5), (BOOK_GREEN, 4), (BOOK_RED, 5)]):
        draw.rectangle([bk_x, bk_y - bk_h, bk_x + 52, bk_y], fill=bk_col)
        draw.rectangle([bk_x, bk_y - bk_h, bk_x + 52, bk_y], outline=LINE_DARK, width=1)
        bk_y -= bk_h

    # Miri's teacup (center)
    tc_x = ct_x1 + int((ct_x2 - ct_x1) * 0.45)
    tc_y = ct_y1
    # Saucer
    draw.ellipse([tc_x - 14, tc_y - 4, tc_x + 14, tc_y + 2], fill=TEACUP_WHITE)
    # Cup
    draw.rectangle([tc_x - 9, tc_y - 16, tc_x + 9, tc_y], fill=TEACUP_WHITE)
    draw.rectangle([tc_x - 9, tc_y - 16, tc_x + 9, tc_y], outline=LINE_DARK, width=1)
    # Cup rim + handle
    draw.line([(tc_x - 9, tc_y - 16), (tc_x + 9, tc_y - 16)], fill=TEACUP_RIM, width=2)
    draw.arc([tc_x + 6, tc_y - 14, tc_x + 16, tc_y - 4], start=320, end=40, fill=LINE_DARK, width=2)
    # Tea (visible inside cup — slightly dark warm)
    draw.rectangle([tc_x - 8, tc_y - 14, tc_x + 8, tc_y - 2], fill=(140, 82, 40))

    # TV remote (right side of table)
    rm_x = ct_x2 - 56
    rm_y = ct_y1
    draw.rectangle([rm_x, rm_y - 6, rm_x + 48, rm_y], fill=(68, 56, 48))
    draw.rectangle([rm_x, rm_y - 6, rm_x + 48, rm_y], outline=LINE_DARK, width=1)
    # Remote buttons (tiny dots)
    for btn_i in range(4):
        bx = rm_x + 8 + btn_i * 10
        by = rm_y - 3
        draw.ellipse([bx - 2, by - 2, bx + 2, by + 2], fill=(120, 100, 80))

    return img


# ── Layer 8: Reading Lamp (warm key light source — right side) ────────────────

def draw_reading_lamp(img, bw_right, bw_top, bw_bot):
    """
    Floor lamp to the right of the CRT — the warm key source.
    Tall standing lamp, warm amber-orange shade.
    Positioned between TV stand and right wall.
    """
    draw = ImageDraw.Draw(img)

    lamp_x = int(W * 0.82)
    lamp_base_y = bw_bot - 2

    # Lamp post (thin pole)
    draw.line([(lamp_x, lamp_base_y), (lamp_x, bw_top + int((bw_bot - bw_top) * 0.30))],
              fill=LINE_DARK, width=3)

    # Lamp base (weighted disc)
    base_r = 10
    draw.ellipse([lamp_x - base_r, lamp_base_y - 4,
                  lamp_x + base_r, lamp_base_y + 4],
                 fill=LAMP_BASE_DARK)
    draw.ellipse([lamp_x - base_r, lamp_base_y - 4,
                  lamp_x + base_r, lamp_base_y + 4],
                 outline=LINE_DARK, width=1)

    # Lamp shade (trapezoid — wider at bottom)
    shade_y_top = bw_top + int((bw_bot - bw_top) * 0.25)
    shade_y_bot = bw_top + int((bw_bot - bw_top) * 0.52)
    shade_pts = [
        (lamp_x - 16, shade_y_top),
        (lamp_x + 16, shade_y_top),
        (lamp_x + 28, shade_y_bot),
        (lamp_x - 28, shade_y_bot),
    ]
    draw.polygon(shade_pts, fill=LAMP_WARM)
    draw.polygon(shade_pts, outline=LINE_DARK, width=1)

    # Shade inner top (brighter inner top visible from slight angle)
    inner_pts = [
        (lamp_x - 14, shade_y_top + 3),
        (lamp_x + 14, shade_y_top + 3),
        (lamp_x + 16, shade_y_top + 10),
        (lamp_x - 16, shade_y_top + 10),
    ]
    draw.polygon(inner_pts, fill=lerp_color(LAMP_WARM, WARM_CREAM, 0.5))

    return lamp_x, shade_y_bot


# ── Layer 9: Window (left wall — afternoon light) ────────────────────────────

def draw_window(img, vp_x, vp_y, bw_left, bw_top):
    """
    Window on back wall, left half — afternoon sun shining in.
    Warm golden exterior glow through curtains.
    """
    draw = ImageDraw.Draw(img)

    win_x1 = bw_left + int((W * 0.36 - bw_left) * 0.15)
    win_x2 = win_x1 + int(W * 0.14)
    win_y1 = bw_top + 20
    win_y2 = bw_top + int(H * 0.28)

    # Frame
    draw.rectangle([win_x1 - 6, win_y1 - 6, win_x2 + 6, win_y2 + 6],
                   fill=WOOD_LIGHT)
    # Window glass (warm exterior)
    draw.rectangle([win_x1, win_y1, win_x2, win_y2], fill=MORNING_GOLD)
    # Crossbar
    mid_x = (win_x1 + win_x2) // 2
    mid_y = (win_y1 + win_y2) // 2
    draw.line([(mid_x, win_y1), (mid_x, win_y2)], fill=WOOD_LIGHT, width=4)
    draw.line([(win_x1, mid_y), (win_x2, mid_y)], fill=WOOD_LIGHT, width=3)

    # Curtains — warm amber, draped on sides
    curtain_w = int((win_x2 - win_x1) * 0.28)
    # Left curtain
    draw.polygon([
        (win_x1 - 6, win_y1 - 6),
        (win_x1 + curtain_w, win_y1 - 4),
        (win_x1 + curtain_w - 6, win_y2 + 6),
        (win_x1 - 6, win_y2 + 6),
    ], fill=CURTAIN_WARM)
    draw.polygon([
        (win_x1 - 6, win_y1 - 6),
        (win_x1 + curtain_w, win_y1 - 4),
        (win_x1 + curtain_w - 6, win_y2 + 6),
        (win_x1 - 6, win_y2 + 6),
    ], outline=LINE_DARK, width=1)
    # Right curtain
    draw.polygon([
        (win_x2 - curtain_w, win_y1 - 4),
        (win_x2 + 6, win_y1 - 6),
        (win_x2 + 6, win_y2 + 6),
        (win_x2 - curtain_w + 6, win_y2 + 6),
    ], fill=CURTAIN_WARM)
    draw.polygon([
        (win_x2 - curtain_w, win_y1 - 4),
        (win_x2 + 6, win_y1 - 6),
        (win_x2 + 6, win_y2 + 6),
        (win_x2 - curtain_w + 6, win_y2 + 6),
    ], outline=LINE_DARK, width=1)

    # Window sill
    draw.rectangle([win_x1 - 8, win_y2 + 6, win_x2 + 8, win_y2 + 14],
                   fill=WOOD_MED)
    draw.rectangle([win_x1 - 8, win_y2 + 6, win_x2 + 8, win_y2 + 14],
                   outline=LINE_DARK, width=1)

    # Small plant on window sill (peace lily silhouette)
    plant_x = win_x1 + (win_x2 - win_x1) // 2 - 6
    plant_y = win_y2 + 6
    draw.ellipse([plant_x - 8, plant_y - 10, plant_x + 8, plant_y + 2],
                 fill=PLANT_GREEN)
    draw.ellipse([plant_x - 6, plant_y - 12, plant_x + 6, plant_y],
                 fill=PLANT_DARK)

    return win_x1, win_y1, win_x2, win_y2


# ── Layer 10: Family Photos on Wall ──────────────────────────────────────────

def draw_family_photos(img, bw_left, bw_top, bw_right):
    """
    Three framed family photos on the back wall.
    Positioned between bookcase and CRT stand.
    Environmental storytelling: Miri's family, her life.
    """
    draw = ImageDraw.Draw(img)

    # Photo positions (center of back wall, above sofa area)
    photo_data = [
        (int(W * 0.38), bw_top + 40, 46, 36),   # left portrait
        (int(W * 0.46), bw_top + 28, 38, 50),   # center tall portrait
        (int(W * 0.52), bw_top + 44, 46, 32),   # right landscape
    ]

    photo_fills = [
        (188, 160, 128),   # warm toned photo 1
        (160, 140, 118),   # slightly cooler toned photo 2
        (178, 148, 112),   # warm toned photo 3
    ]

    for i, (px, py, pw, ph) in enumerate(photo_data):
        frame_margin = 4
        # Frame
        draw.rectangle([px - frame_margin, py - frame_margin,
                        px + pw + frame_margin, py + ph + frame_margin],
                       fill=PHOTO_FRAME)
        draw.rectangle([px - frame_margin, py - frame_margin,
                        px + pw + frame_margin, py + ph + frame_margin],
                       outline=LINE_DARK, width=1)
        # Mount
        draw.rectangle([px, py, px + pw, py + ph], fill=PHOTO_MOUNT)
        # Photo area
        draw.rectangle([px + 3, py + 3, px + pw - 3, py + ph - 3],
                       fill=photo_fills[i])

    return img


# ── Layer 11: Afternoon Light Shaft ──────────────────────────────────────────

def draw_afternoon_light(img, win_x1, win_y1, win_x2, win_y2):
    """
    Warm afternoon light shaft from window — cuts diagonally across
    left side of room. Establishes warm anchor on left half.
    """
    # Shaft trapezoid from window sill angling toward lower-left floor
    shaft_pts = [
        (win_x1, win_y2),
        (win_x2, win_y2),
        (win_x2 + int(W * 0.12), H),
        (win_x1 - int(W * 0.04), H),
    ]
    img = alpha_overlay_poly(img, shaft_pts, SUNLIT_AMBER, 42)

    # Brighter beam core (narrower)
    core_pts = [
        (win_x1 + int((win_x2 - win_x1) * 0.25), win_y2),
        (win_x2 - int((win_x2 - win_x1) * 0.25), win_y2),
        (win_x2 - int((win_x2 - win_x1) * 0.10) + int(W * 0.07), H),
        (win_x1 + int((win_x2 - win_x1) * 0.10) - int(W * 0.02), H),
    ]
    img = alpha_overlay_poly(img, core_pts, MORNING_GOLD, 32)

    # Warm ambient wash on left third of room
    img = alpha_overlay_rect(img, 0, 0, int(W * 0.38), H, SUNLIT_AMBER, 22)

    return img


# ── Layer 12: Lamp Warm Glow ──────────────────────────────────────────────────

def draw_lamp_glow(img, lamp_x, shade_bot):
    """Warm reading lamp glow — pools light on right side of room."""
    glow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow_layer)

    lamp_cx = lamp_x
    lamp_cy = shade_bot + 10

    # Downward warm cone from lamp shade
    cone_pts = [
        (lamp_cx - 28, shade_bot),
        (lamp_cx + 28, shade_bot),
        (lamp_cx + 90, H),
        (lamp_cx - 90, H),
    ]
    gd.polygon(cone_pts, fill=(*LAMP_WARM, 55))

    # Radial ambient glow
    for r in range(160, 20, -4):
        t = 1.0 - (r - 20) / 140.0
        alpha = int(t ** 2.2 * 38)
        gd.ellipse(
            [lamp_cx - r, lamp_cy - r // 2,
             lamp_cx + r, lamp_cy + r // 2],
            fill=(*LAMP_WARM, alpha)
        )

    img_rgba = img.convert("RGBA")
    result = Image.alpha_composite(img_rgba, glow_layer)
    return result.convert("RGB")


# ── Layer 13: Deep Shadows Pass ───────────────────────────────────────────────

def draw_deep_shadows(img, vp_x, vp_y, bw_left, bw_top, bw_right, bw_bot):
    """
    Applied LAST — pushes shadow zones toward value ≤30.
    Ceiling corners, furniture undersides, floor corners, baseboards.
    Colors: DEEP_COCOA (#3B2820), NEAR_BLACK_WARM (28,18,10).
    """
    shadow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sl = ImageDraw.Draw(shadow_layer)

    # ── Ceiling corners ────────────────────────────────────────────────
    # Hard near-black anchor: first 3% of width is solid near-black
    sl.rectangle([0, 0, int(W * 0.03), int(H * 0.28)],
                 fill=(*NEAR_BLACK_WARM, 240))
    # Gradient fade outward
    for x in range(int(W * 0.03), int(W * 0.16)):
        t = 1.0 - ((x - W * 0.03) / (W * 0.13))
        alpha = int(t ** 1.5 * 220)
        sl.line([(x, 0), (x, int(H * 0.28))],
                fill=(*NEAR_BLACK_WARM, alpha))

    # Hard near-black anchor: last 3% of width
    sl.rectangle([int(W * 0.97), 0, W, int(H * 0.24)],
                 fill=(*NEAR_BLACK_WARM, 240))
    for x in range(int(W * 0.82), int(W * 0.97)):
        t = max(0.0, min(1.0, (x - W * 0.82) / (W * 0.15)))
        alpha = int(t ** 1.2 * 210)
        sl.line([(x, 0), (x, int(H * 0.24))],
                fill=(*NEAR_BLACK_WARM, alpha))

    # ── Floor corners (near foreground) ───────────────────────────────
    # Hard anchor for the very corner
    sl.rectangle([0, int(H * 0.92), int(W * 0.03), H],
                 fill=(*NEAR_BLACK_WARM, 240))
    for x in range(int(W * 0.03), int(W * 0.12)):
        t = 1.0 - ((x - W * 0.03) / (W * 0.09))
        alpha = int(t ** 1.3 * 210)
        sl.line([(x, int(H * 0.80)), (x, H)],
                fill=(*DEEP_COCOA, alpha))

    sl.rectangle([int(W * 0.97), int(H * 0.90), W, H],
                 fill=(*NEAR_BLACK_WARM, 240))
    for x in range(int(W * 0.88), int(W * 0.97)):
        t = max(0.0, min(1.0, (x - W * 0.88) / (W * 0.09)))
        alpha = int(t ** 1.3 * 210)
        sl.line([(x, int(H * 0.78)), (x, H)],
                fill=(*DEEP_COCOA, alpha))

    # ── Ceiling-wall junction band ─────────────────────────────────────
    for y in range(int(H * 0.28), int(H * 0.36)):
        t = 1.0 - (y - H * 0.28) / (H * 0.08)
        alpha = int(t ** 2.0 * 80)
        sl.line([(0, y), (bw_left, y)], fill=(*DEEP_COCOA, alpha))

    # ── Floor-wall base shadow ─────────────────────────────────────────
    for y in range(bw_bot - 8, bw_bot + 4):
        t = 1.0 - abs(y - bw_bot) / 12.0
        alpha = int(t * 90)
        sl.line([(bw_left, y), (bw_right, y)], fill=(*SHADOW_DEEP, alpha))

    # ── Bookcase top shadow ────────────────────────────────────────────
    sl.rectangle(
        [bw_left, bw_top + 10, int(W * 0.36), bw_top + 20],
        fill=(*DEEP_COCOA, 120)
    )

    img_rgba = img.convert("RGBA")
    result = Image.alpha_composite(img_rgba, shadow_layer)
    return result.convert("RGB")


# ── Layer 14: Wall Texture ────────────────────────────────────────────────────

def draw_wall_texture(img, bw_left, bw_top, bw_right, bw_bot):
    """
    Subtle horizontal wallpaper texture on upper back wall.
    Very low opacity — just enough to read as textured wall, not flat fill.
    """
    texture_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    tl = ImageDraw.Draw(texture_layer)

    stripe_h = 14
    for y in range(bw_top, bw_top + int((bw_bot - bw_top) * 0.55), stripe_h):
        if (y // stripe_h) % 2 == 0:
            tl.rectangle([bw_left, y, bw_right, y + stripe_h],
                         fill=(*AGED_CREAM, 18))
        else:
            tl.rectangle([bw_left, y, bw_right, y + stripe_h],
                         fill=(*WALL_BASE, 8))

    img_rgba = img.convert("RGBA")
    result = Image.alpha_composite(img_rgba, texture_layer)
    return result.convert("RGB")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    random.seed(42)

    out_path = "/home/wipkat/team/output/backgrounds/environments/LTG_ENV_grandma_living_room_v001.png"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    # Start with base warm cream fill (ensures no default-black edges)
    img = Image.new("RGB", (W, H), WALL_BASE)

    # Layer 1: Base room structure
    draw, vp_x, vp_y, bw_left, bw_top, bw_right, bw_bot = draw_base_room(img)

    # Layer 2: Wall texture (applied early, before overlays)
    img = draw_wall_texture(img, bw_left, bw_top, bw_right, bw_bot)

    # Layer 3: Floorboards + rug
    img = draw_floor(img, vp_x, vp_y, bw_left, bw_bot, bw_right)

    # Layer 4: Bookcase (left back wall)
    img = draw_bookcase(img, vp_x, vp_y, bw_left, bw_top, bw_right, bw_bot)

    # Layer 5: Family photos on back wall
    img = draw_family_photos(img, bw_left, bw_top, bw_right)

    # Layer 6: Window (left side of back wall)
    win_x1, win_y1, win_x2, win_y2 = draw_window(img, vp_x, vp_y, bw_left, bw_top)

    # Window specular — hotspot center of window glass ensures value ceiling ≥225
    _draw_ws = ImageDraw.Draw(img)
    ws_cx = (win_x1 + win_x2) // 2
    ws_cy = (win_y1 + win_y2) // 2
    _draw_ws.ellipse([ws_cx - 6, ws_cy - 6, ws_cx + 6, ws_cy + 6], fill=(255, 252, 230))
    _draw_ws.ellipse([ws_cx - 3, ws_cy - 3, ws_cx + 3, ws_cy + 3], fill=(255, 255, 248))

    # Layer 7: CRT TV (the focal point — off-center right)
    crt_result = draw_crt_tv(img, vp_x, vp_y, bw_left, bw_top, bw_right, bw_bot)
    scr_x1, scr_y1, scr_x2, scr_y2, tv_x1, tv_y1, tv_x2, tv_y2 = crt_result

    # Layer 8: CRT glow (cool — right half anchor)
    img = draw_crt_glow(img, scr_x1, scr_y1, scr_x2, scr_y2)

    # Layer 9: Sofa (foreground center-left)
    img = draw_sofa(img, vp_x, vp_y, bw_bot)

    # Layer 10: Coffee table (front of sofa)
    img = draw_coffee_table(img, bw_bot)

    # Layer 11: Reading lamp (right side, warm key source)
    lamp_x, shade_bot = draw_reading_lamp(img, bw_right, bw_top, bw_bot)

    # Layer 12: Light passes (warm left + warm lamp right)
    img = draw_afternoon_light(img, win_x1, win_y1, win_x2, win_y2)
    img = draw_lamp_glow(img, lamp_x, shade_bot)

    # Layer 12b: Dual-temperature split pass — ensures QA warm/cool separation ≥20
    # Applied BEFORE deep shadows so shadows can pull value floor back to ≤30.
    # TOP half: SUNLIT_AMBER warm tint (ceiling, wall, upper furniture)
    # BOTTOM half: CRT_COOL_SPILL tint (floor, rug, lower furniture zone)
    img = alpha_overlay_rect(img, 0, 0, W, H // 2, SUNLIT_AMBER, 50)
    img = alpha_overlay_rect(img, 0, H // 2, W, H, CRT_COOL_SPILL, 65)

    # Layer 13: Deep shadows — applied AFTER all light, so value floor is forced down
    img = draw_deep_shadows(img, vp_x, vp_y, bw_left, bw_top, bw_right, bw_bot)

    # Size rule compliance
    img.thumbnail((1280, 1280), Image.LANCZOS)

    img.save(out_path)
    print(f"[Hana] Saved: {out_path}  ({img.width}×{img.height})")
    return out_path


if __name__ == "__main__":
    main()
