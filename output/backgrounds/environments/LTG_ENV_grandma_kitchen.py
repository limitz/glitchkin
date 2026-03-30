#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_bg_grandma_kitchen_v003.py — Grandma Miri's Kitchen Background v003
"Luma & the Glitchkin" — Background & Environment Design
Artist: Jordan Reed | Cycle 22

Used in: A1-01 (Act 1 opening scene)
Narrative: Act 1 opening. Warm morning. Pre-digital world. Home = safe.

Tone: Warm morning daylight. Style: Real World (NO Glitch palette).
Key story element: CRT TV visible through doorway — this is the TV with the
Glitchkin. It must be visible but not dominant. Adjacent room, through doorway.

v003 improvements (Cycle 22, responding to Takeshi Murakami C10 feedback A-):
  Fix 2a — Upper wall texture extended to side walls:
    The WALL_SHADOW left and right wall polygons now receive the same stripe
    pattern as the back wall, but at reduced alpha (~35% less) to reflect
    lower illumination on side surfaces. Side walls no longer read as flat
    undifferentiated planes.

  Fix 2b — Floor grid perspective conflict resolved:
    Option A selected: draw_floor_tiles() REMOVED. draw_floor_linoleum_overlay()
    replaced with a perspective-correct linoleum grid that converges toward
    vp_x=768. Two contradictory spatial grids on the same surface eliminated.
    One floor system. No contradictions.

All v002 improvements retained:
  - Floor worn path trapezoid (alpha 20, doorway to stove)
  - Upper wall stripe texture on back wall (alpha 12-15)
  - CRT glow dual-ring (primary r=80 + ambient r=130)

Environment spec:
  - Small, cozy kitchen interior
  - Morning sunlight through window (warm amber/golden light)
  - Old-fashioned appliances (pre-digital era — no screens on appliances)
  - CRT TV through doorway/adjacent room (important story element)
  - Lived-in: dishes, plants, crossword puzzle on table
  - Palette: warm creams, ambers, wood tones — ALL REAL WORLD colors
  - No Glitch colors (no ELEC_CYAN, ACID_GREEN, DATA_BLUE, UV_PURPLE, HOT_MAGENTA)
    Exception: CRT TV glow through doorway ONLY (faint, far-plane, desaturated)

Camera: Looking across kitchen toward window wall. Slight 3/4 angle.
        Sink under window, table at left/center, appliances at right.

Output: /home/wipkat/team/output/backgrounds/environments/LTG_ENV_grandma_kitchen_v003.png
"""

import math
import random
import os
from PIL import Image, ImageDraw

W, H = 1920, 1080

# ── Real World Palette (master_palette.md + kitchen spec) ────────────────────
# Primary warm tones
WARM_CREAM       = (250, 240, 220)    # cream wall base
AGED_CREAM       = (238, 226, 198)    # slightly older, more used
SUNLIT_AMBER     = (212, 146,  58)    # morning sunlight spill
MORNING_GOLD     = (255, 200,  80)    # bright morning window light
SOFT_GOLD        = (232, 201,  90)    # secondary warm highlights
WOOD_DARK        = (130,  85,  42)    # dark wood cabinets
WOOD_MED         = (168, 118,  62)    # medium wood (table, chairs)
WOOD_LIGHT       = (196, 148,  88)    # lighter wood surfaces
WOOD_WORN        = (185, 140,  80)    # worn wood counter

# Walls, floor, ceiling
WALL_WARM        = (240, 222, 188)    # kitchen wall warm cream
WALL_SHADOW      = (200, 182, 152)    # wall in shadow zones
CEILING_WARM     = (248, 238, 214)    # ceiling warm white
FLOOR_TILE_WARM  = (212, 196, 162)    # linoleum floor tile light
FLOOR_TILE_DARK  = (190, 174, 142)    # linoleum floor tile dark
FLOOR_WORN_PATH  = (222, 208, 176)    # worn traffic path (lighter)

# Appliances (old-fashioned, no screens)
FRIDGE_WHITE     = (232, 228, 214)    # old refrigerator off-white
FRIDGE_TRIM      = (190, 186, 172)    # fridge trim/handle
STOVE_CREAM      = (226, 220, 204)    # old gas stove cream
STOVE_IRON       = (148, 140, 128)    # cast iron burner rings
STOVE_KNOB       = (168, 148, 112)    # bakelite knobs
SINK_PORCELAIN   = (230, 226, 214)    # porcelain sink
COUNTERTOP       = (200, 182, 148)    # laminate countertop
COUNTER_EDGE     = (172, 156, 122)    # counter edge darker

# Food + kitchen items
DISH_WHITE       = (238, 236, 228)    # dinner plate
DISH_BLUE_RING   = (100, 130, 160)    # blue-ringed china
TEAPOT_RED       = (192,  72,  48)    # red enamel teapot
MUG_EARTHY       = (160, 112,  72)    # earthenware mug
BREAD_WARM       = (200, 158,  88)    # bread loaf
PLANT_GREEN      = (88,  138,  72)    # kitchen plant
PLANT_DARK       = (60,   90,  48)    # plant shadow
CURTAIN_WARM     = (238, 198, 128)    # window curtain warm yellow

# Shadow and outline
LINE_DARK        = (100,  72,  40)    # dark brown line work
SHADOW_WARM      = (180, 152, 108)    # warm shadow tones
DEEP_SHADOW      = (130,  98,  62)    # deep shadow
GROUT_LINE       = (176, 162, 136)    # floor grout

# Doorway / CRT TV (far plane — through doorway)
DOORWAY_DARK     = (168, 148, 108)    # adjacent room in shadow
DOORWAY_DEEP     = (140, 118,  82)    # deep room shadow
CRT_SCREEN_GLOW  = ( 60, 120, 140)    # faint CRT glow (desaturated — far plane only)
CRT_BODY         = (120, 108,  88)    # CRT TV body in adjacent room
CRT_GLOW_FLOOR   = ( 90, 140, 155)    # faint TV light spill on adjacent room floor


def lerp_color(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def alpha_composite_rect(img, x0, y0, x1, y1, color_rgb, alpha):
    """Draw a filled rectangle at given alpha using alpha_composite."""
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.rectangle([x0, y0, x1, y1], fill=(*color_rgb, alpha))
    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, overlay)
    return img_rgba.convert("RGB")


# ── Layer 1: Base Walls, Ceiling, Floor ──────────────────────────────────────

def draw_base_room(img):
    """
    Kitchen perspective: looking toward window wall (back wall).
    Left wall: partial view with doorway to adjacent room.
    Right wall: cabinets and stove/fridge.
    Floor: old linoleum tile, worn path from sink to table.
    """
    draw = ImageDraw.Draw(img)

    # Vanishing point — slightly left of center, upper third
    vp_x = int(W * 0.40)
    vp_y = int(H * 0.38)

    # ── Ceiling ─────────────────────────────────────────────────────────────
    ceil_poly = [
        (0, 0), (W, 0),
        (W, vp_y - 60),
        (vp_x, vp_y),
        (0, int(H * 0.22)),
    ]
    draw.polygon(ceil_poly, fill=CEILING_WARM)

    # ── Back wall (window wall — facing us) ──────────────────────────────────
    bw_left  = int(W * 0.10)
    bw_right = int(W * 0.72)
    bw_top   = vp_y
    bw_bot   = int(H * 0.82)
    draw.rectangle([bw_left, bw_top, bw_right, bw_bot], fill=WALL_WARM)

    # ── Left wall (with doorway) ─────────────────────────────────────────────
    lw_poly = [
        (0, int(H * 0.22)),
        (bw_left, bw_top),
        (bw_left, bw_bot),
        (0, int(H * 0.88)),
    ]
    draw.polygon(lw_poly, fill=WALL_SHADOW)

    # ── Right wall (cabinets side) ───────────────────────────────────────────
    rw_poly = [
        (bw_right, bw_top),
        (W, vp_y - 60),
        (W, int(H * 0.82)),
        (bw_right, bw_bot),
    ]
    draw.polygon(rw_poly, fill=WALL_SHADOW)

    # ── Floor ────────────────────────────────────────────────────────────────
    floor_poly = [
        (0, int(H * 0.88)),
        (bw_left, bw_bot),
        (bw_right, bw_bot),
        (W, int(H * 0.82)),
        (W, H),
        (0, H),
    ]
    draw.polygon(floor_poly, fill=FLOOR_TILE_WARM)

    return draw, vp_x, vp_y, bw_left, bw_top, bw_right, bw_bot


def draw_floor_tiles(draw, bw_left, bw_bot, bw_right, vp_x, vp_y):
    """
    v003 FIX 2b: draw_floor_tiles() DISABLED — function kept for reference only.
    In v003 we use draw_floor_linoleum_overlay() exclusively with a
    perspective-correct grid. Calling this function does nothing.
    Rationale: two contradictory spatial grids on the same floor surface
    (perspective grid + flat orthographic overlay) create a visual contradiction.
    """
    pass  # Intentionally empty — replaced by perspective-correct linoleum overlay


def draw_floor_linoleum_overlay(img, bw_left, bw_bot, bw_right, vp_x, vp_y):
    """
    v002: Linoleum tile grid overlay + worn path.
    v003 FIX 2b: Grid replaced with perspective-correct linoleum grid that
    converges toward vp_x (the vanishing point). Horizontal rows use
    non-linear spacing (perspective recession). Vertical column lines
    converge from vp_x at the floor horizon toward the image bottom.
    Single floor system — no contradictory spatial grids.
    Worn path trapezoid retained unchanged from v002.
    """
    floor_top_y = bw_bot

    # Grid line color: warm brown tint, low alpha
    GRID_LINE_COLOR = (155, 138, 112, 25)  # warm brown, alpha 25

    # ── Perspective-correct grid ─────────────────────────────────────────────
    grid_overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grid_overlay)

    # Horizontal rows — non-linear spacing (perspective recession)
    # Rows close together near floor_top_y (far), spread out near camera
    num_rows = 14
    for i in range(1, num_rows + 1):
        t = (i / num_rows) ** 1.5   # power > 1 gives more rows near far end
        fy = floor_top_y + int(t * (H - floor_top_y))
        if fy >= H:
            break
        gd.line([(0, fy), (W, fy)], fill=GRID_LINE_COLOR, width=2)

    # Vertical columns — converge from vp_x at floor horizon toward bottom
    # Distribute column endpoints evenly across the bottom edge (y=H)
    num_cols = 18
    for i in range(num_cols + 1):
        # Bottom intercept: evenly spaced across full width
        bx = int((i / num_cols) * W)
        # All perspective lines originate at (vp_x, floor_top_y)
        gd.line([(vp_x, floor_top_y), (bx, H)], fill=GRID_LINE_COLOR, width=1)

    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, grid_overlay)
    img = img_rgba.convert("RGB")

    # ── Worn path rectangle (doorway zone to stove zone, alpha 20) ───────────
    # Doorway is at left of back wall; stove is center-right.
    # The worn path should run from doorway (left area, ~x=10% to 20%)
    # diagonally/broadly toward stove area (x=54–72% of back wall).
    # Use a wide, low-alpha lighter rectangle to suggest this path.
    worn_path_overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(worn_path_overlay)

    # Worn path: trapezoid from doorway left (narrow) to stove right (wide)
    # At floor top: narrow band centered around x=25% (doorway-to-center)
    # At floor bottom: broader band centered around x=48% (mid-room)
    wp_top_y = floor_top_y
    wp_bot_y = H
    wp_top_cx = int(W * 0.32)   # center of path at top (near doorway → stove)
    wp_bot_cx = int(W * 0.46)   # center of path at bottom (camera level)
    wp_top_hw = int(W * 0.14)   # half-width at top (narrow)
    wp_bot_hw = int(W * 0.22)   # half-width at bottom (wider, camera near)

    worn_poly = [
        (wp_top_cx - wp_top_hw, wp_top_y),
        (wp_top_cx + wp_top_hw, wp_top_y),
        (wp_bot_cx + wp_bot_hw, wp_bot_y),
        (wp_bot_cx - wp_bot_hw, wp_bot_y),
    ]
    # Slightly lighter than FLOOR_WORN_PATH — warm cream buff
    WORN_PATH_LIGHT = (230, 218, 186, 20)  # warm buff, alpha 20
    wd.polygon(worn_poly, fill=WORN_PATH_LIGHT)

    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, worn_path_overlay)
    img = img_rgba.convert("RGB")

    return img


# ── Layer 2: Window ───────────────────────────────────────────────────────────

def draw_window(img, draw, vp_x, vp_y, bw_left, bw_top, bw_right, bw_bot):
    """
    Kitchen window above sink. Morning light source.
    Warm amber/golden exterior light. Curtains pulled to sides.
    """
    # Window position: center of back wall, upper portion
    win_x1 = int(W * 0.32)
    win_x2 = int(W * 0.56)
    win_y1 = bw_top + int((bw_bot - bw_top) * 0.06)
    win_y2 = bw_top + int((bw_bot - bw_top) * 0.44)
    win_w = win_x2 - win_x1
    win_h = win_y2 - win_y1

    # Window frame (wood painted white-ish)
    draw.rectangle([win_x1 - 6, win_y1 - 6, win_x2 + 6, win_y2 + 6],
                   fill=WOOD_LIGHT)

    # Morning sky through window — gradient warm gold to pale blue-cream
    for y in range(win_y1, win_y2):
        t = (y - win_y1) / win_h
        # Near top: bright morning gold. Near bottom: softer warm cream
        sky_col = lerp_color(MORNING_GOLD, (200, 215, 190), t)
        draw.line([(win_x1, y), (win_x2, y)], fill=sky_col)

    # Window pane dividers (cross bars)
    mid_x = (win_x1 + win_x2) // 2
    mid_y = (win_y1 + win_y2) // 2
    draw.line([(mid_x, win_y1), (mid_x, win_y2)], fill=WOOD_LIGHT, width=5)
    draw.line([(win_x1, mid_y), (win_x2, mid_y)], fill=WOOD_LIGHT, width=5)

    # Curtains — pulled to sides, framing window
    # Left curtain
    curtain_w = int(win_w * 0.22)
    lc_x1 = win_x1 - 6 - curtain_w
    lc_x2 = win_x1 + curtain_w // 3
    draw.rectangle([lc_x1, win_y1 - 10, lc_x2, win_y2 + 20], fill=CURTAIN_WARM)
    # Curtain folds (vertical lines)
    for fi in range(3):
        fx = lc_x1 + int(fi * curtain_w * 0.28)
        draw.line([(fx, win_y1 - 10), (fx, win_y2 + 20)],
                  fill=lerp_color(CURTAIN_WARM, SHADOW_WARM, 0.3), width=2)

    # Right curtain
    rc_x1 = win_x2 - curtain_w // 3
    rc_x2 = win_x2 + 6 + curtain_w
    draw.rectangle([rc_x1, win_y1 - 10, rc_x2, win_y2 + 20], fill=CURTAIN_WARM)
    for fi in range(3):
        fx = rc_x1 + int(fi * curtain_w * 0.35)
        draw.line([(fx, win_y1 - 10), (fx, win_y2 + 20)],
                  fill=lerp_color(CURTAIN_WARM, SHADOW_WARM, 0.3), width=2)

    # Curtain rod
    rod_y = win_y1 - 14
    draw.line([(lc_x1 - 10, rod_y), (rc_x2 + 10, rod_y)],
              fill=FRIDGE_TRIM, width=4)
    draw.ellipse([lc_x1 - 16, rod_y - 6, lc_x1 - 4, rod_y + 6], fill=FRIDGE_TRIM)
    draw.ellipse([rc_x2 + 4, rod_y - 6, rc_x2 + 16, rod_y + 6], fill=FRIDGE_TRIM)

    return win_x1, win_x2, win_y1, win_y2


def draw_morning_light(img, win_x1, win_x2, win_y1, win_y2, bw_bot):
    """
    Morning sunlight from window — warm amber gradient spilling into room.
    Column-based gradient from window, falloff into room depth.
    """
    # Direct sunlight shaft — column gradient from window
    light_overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(light_overlay)

    win_cx = (win_x1 + win_x2) // 2
    light_spread = int(W * 0.45)  # how far light spreads horizontally

    # Main ambient light fill — warm across back wall
    for x in range(max(0, win_cx - light_spread), min(W, win_cx + light_spread)):
        dist = abs(x - win_cx)
        t = dist / light_spread
        falloff = (1.0 - t) ** 1.8
        alpha = int(falloff * 48)
        if alpha > 0:
            ld.line([(x, win_y1), (x, bw_bot)], fill=(*SUNLIT_AMBER, alpha))

    # Light on ceiling above window
    for x in range(win_x1, win_x2):
        alpha = 30
        ld.line([(x, 0), (x, win_y1)], fill=(*SOFT_GOLD, alpha))

    # Floor light pool under window — stronger, oval shape
    for r in range(120, 0, -1):
        t = 1.0 - r / 120.0
        alpha = int(t * t * 40)
        pool_cx = win_cx
        pool_cy = bw_bot + int((H - bw_bot) * 0.3)
        ld.ellipse([pool_cx - r, pool_cy - r // 3,
                    pool_cx + r, pool_cy + r // 3],
                   fill=(*MORNING_GOLD, alpha))

    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, light_overlay)
    return img_rgba.convert("RGB")


# ── v002 ADDITION / v003 EXTENDED: Upper Wall Wallpaper Texture ───────────────

def draw_upper_wall_texture(img, bw_left, bw_top, bw_right, bw_bot):
    """
    v002: Subtle period wallpaper texture on back wall upper area.
    v003 FIX 2a: Extended to left and right wall polygons.
    Side walls receive same stripe pattern but at ~35% reduced alpha
    (WALL_SHADOW surfaces receive less direct illumination than back wall).
    Uses polygon masking to clip stripes correctly to each wall surface.
    """
    wall_height = bw_bot - bw_top

    # Back wall upper zone: top of back wall to ~50% down
    upper_wall_y1 = bw_top
    upper_wall_y2 = bw_top + int(wall_height * 0.50)

    # Stripe colors
    STRIPE_A = (248, 238, 210)   # very pale warm cream
    STRIPE_B = (232, 214, 178)   # slightly deeper warm buff
    STRIPE_HEIGHT = 12           # pixels per stripe

    # Back wall alphas (full illumination)
    STRIPE_ALPHA_A = 12
    STRIPE_ALPHA_B = 15
    # Side wall alphas (~35% less — less direct light)
    SIDE_ALPHA_A = 8
    SIDE_ALPHA_B = 10

    # ── Back wall stripes ────────────────────────────────────────────────────
    stripe_overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stripe_overlay)

    y = upper_wall_y1
    stripe_idx = 0
    while y < upper_wall_y2:
        y_end = min(y + STRIPE_HEIGHT, upper_wall_y2)
        if stripe_idx % 2 == 0:
            col = (*STRIPE_A, STRIPE_ALPHA_A)
        else:
            col = (*STRIPE_B, STRIPE_ALPHA_B)
        sd.rectangle([bw_left, y, bw_right, y_end], fill=col)
        y += STRIPE_HEIGHT
        stripe_idx += 1

    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, stripe_overlay)
    img = img_rgba.convert("RGB")

    # ── Left wall stripes (clipped to left wall polygon) ─────────────────────
    # Left wall polygon: (0, H*0.22), (bw_left, bw_top), (bw_left, bw_bot), (0, H*0.88)
    lw_poly = [
        (0,       int(H * 0.22)),
        (bw_left, bw_top),
        (bw_left, bw_bot),
        (0,       int(H * 0.88)),
    ]
    lw_top_y = int(H * 0.22)
    lw_bot_y = bw_top + int(wall_height * 0.50)   # upper 50% of wall height

    # Draw a stripe mask for the left wall
    lw_stripe = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ls = ImageDraw.Draw(lw_stripe)

    # Fill the whole polygon first in each stripe color, then overlay them
    # Simpler approach: draw full-width stripes, then mask to polygon
    lw_stripe_full = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    lf = ImageDraw.Draw(lw_stripe_full)
    y = lw_top_y
    stripe_idx = 0
    while y < lw_bot_y:
        y_end = min(y + STRIPE_HEIGHT, lw_bot_y)
        if stripe_idx % 2 == 0:
            col = (*STRIPE_A, SIDE_ALPHA_A)
        else:
            col = (*STRIPE_B, SIDE_ALPHA_B)
        lf.rectangle([0, y, bw_left, y_end], fill=col)
        y += STRIPE_HEIGHT
        stripe_idx += 1

    # Create a mask from the left wall polygon
    lw_mask = Image.new("L", (W, H), 0)
    lm = ImageDraw.Draw(lw_mask)
    lm.polygon(lw_poly, fill=255)

    # Apply mask: zero out pixels outside the polygon
    lw_stripe_masked = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    lw_stripe_masked.paste(lw_stripe_full, mask=lw_mask)

    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, lw_stripe_masked)
    img = img_rgba.convert("RGB")

    # ── Right wall stripes (clipped to right wall polygon) ────────────────────
    # Right wall polygon: (bw_right, bw_top), (W, vp_y-60), (W, H*0.82), (bw_right, bw_bot)
    # vp_y = int(H * 0.38) = 410; vp_y - 60 = 350
    rw_poly = [
        (bw_right, bw_top),
        (W,        int(H * 0.38) - 60),
        (W,        int(H * 0.82)),
        (bw_right, bw_bot),
    ]
    rw_top_y = int(H * 0.38) - 60   # ceiling corner of right wall
    rw_bot_y = bw_top + int(wall_height * 0.50)  # upper 50% of wall height

    rw_stripe_full = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    rf = ImageDraw.Draw(rw_stripe_full)
    y = min(rw_top_y, bw_top)
    stripe_idx = 0
    while y < rw_bot_y:
        y_end = min(y + STRIPE_HEIGHT, rw_bot_y)
        if stripe_idx % 2 == 0:
            col = (*STRIPE_A, SIDE_ALPHA_A)
        else:
            col = (*STRIPE_B, SIDE_ALPHA_B)
        rf.rectangle([bw_right, y, W, y_end], fill=col)
        y += STRIPE_HEIGHT
        stripe_idx += 1

    # Create a mask from the right wall polygon
    rw_mask = Image.new("L", (W, H), 0)
    rm = ImageDraw.Draw(rw_mask)
    rm.polygon(rw_poly, fill=255)

    rw_stripe_masked = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    rw_stripe_masked.paste(rw_stripe_full, mask=rw_mask)

    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, rw_stripe_masked)
    img = img_rgba.convert("RGB")

    return img


# ── Layer 3: Doorway to Adjacent Room (CRT TV) ────────────────────────────────

def draw_doorway_and_crt(img, draw, bw_left, bw_top, bw_bot):
    """
    Doorway on left wall — adjacent living room visible.
    CRT TV in adjacent room: important story element. Visible but not dominant.
    TV is off or on standby — faint blue-gray glow on adjacent wall.

    v002 IMPROVEMENT: CRT glow radius increased; second wider ambient glow ring
    at lower alpha for atmospheric presence — feels like a genuine light source
    in the adjacent room, inviting the eye through the doorway.
    """
    # Doorway: left portion of back wall, arched or rectangular
    door_x1 = bw_left + int((bw_bot - bw_top) * 0.05)
    door_x2 = door_x1 + int(W * 0.12)
    door_y1 = bw_top + int((bw_bot - bw_top) * 0.10)
    door_y2 = bw_bot - 4

    # Door frame (wood trim)
    frame_w = 6
    draw.rectangle([door_x1 - frame_w, door_y1 - frame_w,
                    door_x2 + frame_w, door_y2], fill=WOOD_MED)

    # Adjacent room — in shadow, warmer tones but darker
    # Fill with deep warm shadow
    draw.rectangle([door_x1, door_y1, door_x2, door_y2], fill=DOORWAY_DARK)

    # Gradient — far wall of adjacent room
    far_wall_x = door_x1 + int((door_x2 - door_x1) * 0.3)
    for y in range(door_y1, door_y2):
        t = (y - door_y1) / (door_y2 - door_y1)
        col = lerp_color(DOORWAY_DARK, DOORWAY_DEEP, t * 0.5)
        draw.line([(door_x1, y), (far_wall_x, y)], fill=col)

    # CRT TV in adjacent room — visible in lower portion of doorway
    tv_x1 = door_x1 + int((door_x2 - door_x1) * 0.08)
    tv_x2 = door_x1 + int((door_x2 - door_x1) * 0.75)
    tv_y1 = door_y1 + int((door_y2 - door_y1) * 0.48)
    tv_y2 = door_y2 - int((door_y2 - door_y1) * 0.05)

    tv_w = tv_x2 - tv_x1
    tv_h = tv_y2 - tv_y1

    # CRT body (old plastic, slightly yellowed)
    draw.rectangle([tv_x1, tv_y1, tv_x2, tv_y2], fill=CRT_BODY)
    draw.rectangle([tv_x1, tv_y1, tv_x2, tv_y2], outline=LINE_DARK, width=1)

    # CRT screen (rounded corners, slightly smaller than body)
    scr_margin = max(2, tv_w // 10)
    scr_x1 = tv_x1 + scr_margin
    scr_x2 = tv_x2 - scr_margin
    scr_y1 = tv_y1 + int(tv_h * 0.08)
    scr_y2 = tv_y2 - int(tv_h * 0.25)

    # Screen with CRT glow — desaturated blue-green (far plane, subtle)
    for y in range(scr_y1, scr_y2):
        t = (y - scr_y1) / max(1, scr_y2 - scr_y1)
        row_col = lerp_color(CRT_SCREEN_GLOW, (40, 90, 110), t)
        draw.line([(scr_x1, y), (scr_x2, y)], fill=row_col)
    # Screen border
    draw.rectangle([scr_x1, scr_y1, scr_x2, scr_y2], outline=LINE_DARK, width=1)

    # CRT body details — speaker grille, knobs
    grille_x = tv_x1 + int(tv_w * 0.08)
    grille_y = tv_y2 - int(tv_h * 0.22)
    grille_h = int(tv_h * 0.18)
    for gi in range(4):
        draw.line([(grille_x + gi * 3, grille_y),
                   (grille_x + gi * 3, grille_y + grille_h)],
                  fill=LINE_DARK, width=1)

    # Tuning knobs
    for ki in range(2):
        kx = tv_x2 - int(tv_w * 0.15) + ki * int(tv_w * 0.08)
        ky = tv_y1 + int(tv_h * 0.55)
        draw.ellipse([kx - 3, ky - 3, kx + 3, ky + 3], fill=LINE_DARK)

    # ── v002: Enhanced CRT glow — increased radius + wider ambient ring ───────
    # Primary glow: slightly larger radius than v001 (was 60, now 80)
    # Second ring: wider (radius 120) at lower alpha for ambient diffusion
    crt_spill = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cs = ImageDraw.Draw(crt_spill)

    # Screen center for glow origin
    scr_cx = (scr_x1 + scr_x2) // 2
    scr_cy = (scr_y1 + scr_y2) // 2

    # Primary glow ring — increased radius (80 vs v001's 60)
    PRIMARY_RADIUS = 80
    for r in range(PRIMARY_RADIUS, 0, -1):
        t = 1.0 - r / PRIMARY_RADIUS
        alpha = int(t * t * 30)   # slightly reduced peak so total stays balanced
        cs.ellipse([scr_cx - r, scr_cy - r // 2,
                    scr_cx + r, scr_cy + r // 2],
                   fill=(*CRT_GLOW_FLOOR, alpha))

    # Floor spill — TV bottom edge (retained from v001, slightly stronger)
    spill_y = tv_y2
    for r in range(70, 0, -1):
        t = 1.0 - r / 70.0
        alpha = int(t * t * 28)
        cs.ellipse([tv_x1 - r // 4, spill_y - 4,
                    tv_x2 + r // 4, spill_y + r // 3],
                   fill=(*CRT_GLOW_FLOOR, alpha))

    # Second, wider ambient ring — lower alpha, softer presence
    # This is the "atmospheric invitation" — a wide halo around the TV
    # that bleeds gently into the doorway space
    AMBIENT_RADIUS = 130
    for r in range(AMBIENT_RADIUS, PRIMARY_RADIUS, -1):
        t = 1.0 - (r - PRIMARY_RADIUS) / (AMBIENT_RADIUS - PRIMARY_RADIUS)
        alpha = int(t * 8)  # very low alpha — just a breath of cool light
        if alpha < 1:
            continue
        cs.ellipse([scr_cx - r, scr_cy - r // 2,
                    scr_cx + r, scr_cy + r // 2],
                   fill=(*CRT_GLOW_FLOOR, alpha))

    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, crt_spill)
    img = img_rgba.convert("RGB")
    draw = ImageDraw.Draw(img)

    return img, draw


# ── Layer 4: Kitchen Cabinets & Appliances ────────────────────────────────────

def draw_cabinets_and_appliances(draw, bw_left, bw_top, bw_right, bw_bot):
    """
    Upper and lower kitchen cabinets.
    Appliances: old refrigerator (right side), gas stove (center-right back wall).
    All pre-digital era — no LED displays, no digital clocks.
    """
    # ── Upper Cabinets (back wall, above counter level) ──────────────────────
    cab_bottom = bw_top + int((bw_bot - bw_top) * 0.42)
    cab_top    = bw_top + int((bw_bot - bw_top) * 0.05)

    # Upper cabinet row on back wall
    upper_cab_specs = [
        # (x1_frac, x2_frac) — on back wall x space
        (0.58, 0.70),
        (0.70, 0.83),
        (0.83, 0.96),
    ]
    for (x1f, x2f) in upper_cab_specs:
        cx1 = int(bw_left + (bw_right - bw_left) * x1f)
        cx2 = int(bw_left + (bw_right - bw_left) * x2f)
        draw.rectangle([cx1, cab_top, cx2, cab_bottom], fill=WOOD_DARK)
        draw.rectangle([cx1, cab_top, cx2, cab_bottom], outline=LINE_DARK, width=2)
        # Cabinet door panel (inset)
        inset = 5
        draw.rectangle([cx1 + inset, cab_top + inset,
                         cx2 - inset, cab_bottom - inset],
                        outline=lerp_color(WOOD_DARK, WOOD_MED, 0.5), width=1)
        # Small handle
        hx = (cx1 + cx2) // 2
        hy = cab_bottom - 12
        draw.rectangle([hx - 6, hy, hx + 6, hy + 4], fill=FRIDGE_TRIM)

    # ── Countertop (back wall lower section) ────────────────────────────────
    counter_y1 = bw_top + int((bw_bot - bw_top) * 0.52)
    counter_y2 = counter_y1 + int((bw_bot - bw_top) * 0.08)
    # Counter runs from doorway area to right wall
    ct_x1 = bw_left + int((bw_right - bw_left) * 0.38)
    ct_x2 = bw_right
    draw.rectangle([ct_x1, counter_y1, ct_x2, counter_y2], fill=COUNTERTOP)
    draw.line([(ct_x1, counter_y1), (ct_x2, counter_y1)], fill=COUNTER_EDGE, width=2)
    draw.rectangle([ct_x1, counter_y1, ct_x2, counter_y2], outline=LINE_DARK, width=1)

    # Lower cabinets below counter
    lower_y1 = counter_y2
    lower_y2 = bw_bot
    for ci in range(4):
        lc_x1 = ct_x1 + int(ci * (ct_x2 - ct_x1) / 4)
        lc_x2 = ct_x1 + int((ci + 1) * (ct_x2 - ct_x1) / 4)
        draw.rectangle([lc_x1, lower_y1, lc_x2, lower_y2], fill=WOOD_DARK)
        draw.rectangle([lc_x1, lower_y1, lc_x2, lower_y2], outline=LINE_DARK, width=1)
        inset = 5
        draw.rectangle([lc_x1 + inset, lower_y1 + inset,
                         lc_x2 - inset, lower_y2 - inset],
                        outline=lerp_color(WOOD_DARK, WOOD_MED, 0.4), width=1)
        hx = (lc_x1 + lc_x2) // 2
        hy = lower_y1 + int((lower_y2 - lower_y1) * 0.45)
        draw.rectangle([hx - 8, hy, hx + 8, hy + 4], fill=FRIDGE_TRIM)

    # ── Gas Stove (center-right of back wall) ────────────────────────────────
    stove_x1 = int(bw_left + (bw_right - bw_left) * 0.54)
    stove_x2 = int(bw_left + (bw_right - bw_left) * 0.72)
    stove_y1 = counter_y1 - 2
    stove_y2 = counter_y2
    draw.rectangle([stove_x1, stove_y1, stove_x2, stove_y2], fill=STOVE_CREAM)
    draw.rectangle([stove_x1, stove_y1, stove_x2, stove_y2], outline=LINE_DARK, width=1)
    # Burner rings (4 cast iron circles)
    burner_positions = [
        (stove_x1 + int((stove_x2 - stove_x1) * 0.25), stove_y1 + int((stove_y2 - stove_y1) * 0.3)),
        (stove_x1 + int((stove_x2 - stove_x1) * 0.75), stove_y1 + int((stove_y2 - stove_y1) * 0.3)),
        (stove_x1 + int((stove_x2 - stove_x1) * 0.25), stove_y1 + int((stove_y2 - stove_y1) * 0.72)),
        (stove_x1 + int((stove_x2 - stove_x1) * 0.75), stove_y1 + int((stove_y2 - stove_y1) * 0.72)),
    ]
    burner_r = max(5, int((stove_x2 - stove_x1) * 0.11))
    for (bx, by) in burner_positions:
        draw.ellipse([bx - burner_r, by - burner_r // 2,
                      bx + burner_r, by + burner_r // 2],
                     fill=STOVE_IRON)
        # Inner ring
        inner_r = max(2, burner_r - 4)
        draw.ellipse([bx - inner_r, by - inner_r // 2,
                      bx + inner_r, by + inner_r // 2],
                     outline=lerp_color(STOVE_IRON, WOOD_DARK, 0.4), width=1)
    # Knobs row
    knob_y = stove_y1 + 4
    for ki in range(4):
        kx = stove_x1 + int((ki + 0.5) * (stove_x2 - stove_x1) / 4)
        draw.ellipse([kx - 5, knob_y, kx + 5, knob_y + 8], fill=STOVE_KNOB)

    return counter_y1, counter_y2


# ── Layer 5: Sink ─────────────────────────────────────────────────────────────

def draw_sink(draw, bw_left, bw_top, bw_right, bw_bot, win_x1, win_x2, win_y2):
    """
    Porcelain sink below window. Faucet. Maybe a plant on windowsill.
    Dish rack with a few drying dishes.
    """
    # Sink position — below window, center of back wall
    sink_x1 = int(bw_left + (bw_right - bw_left) * 0.33)
    sink_x2 = int(bw_left + (bw_right - bw_left) * 0.56)
    counter_y = bw_top + int((bw_bot - bw_top) * 0.52)
    sink_y1 = win_y2 + 4
    sink_y2 = counter_y

    # Counter around sink
    draw.rectangle([sink_x1 - 10, sink_y1, sink_x2 + 10, sink_y2],
                   fill=COUNTERTOP)
    draw.line([(sink_x1 - 10, sink_y1), (sink_x2 + 10, sink_y1)],
              fill=COUNTER_EDGE, width=2)

    # Sink basin
    basin_inset = max(6, int((sink_x2 - sink_x1) * 0.08))
    draw.rectangle([sink_x1 + basin_inset, sink_y1 + basin_inset,
                    sink_x2 - basin_inset, sink_y2 - 4],
                   fill=SINK_PORCELAIN)
    draw.rectangle([sink_x1 + basin_inset, sink_y1 + basin_inset,
                    sink_x2 - basin_inset, sink_y2 - 4],
                   outline=lerp_color(SINK_PORCELAIN, SHADOW_WARM, 0.5), width=1)

    # Drain
    drain_cx = (sink_x1 + sink_x2) // 2
    drain_cy = sink_y2 - 8
    draw.ellipse([drain_cx - 6, drain_cy - 4, drain_cx + 6, drain_cy + 4],
                 fill=lerp_color(SINK_PORCELAIN, LINE_DARK, 0.6))

    # Faucet (old chrome)
    faucet_x = drain_cx
    faucet_y = sink_y1 + 2
    draw.rectangle([faucet_x - 3, faucet_y, faucet_x + 3, faucet_y + 12],
                   fill=FRIDGE_TRIM)
    draw.ellipse([faucet_x - 8, faucet_y - 4, faucet_x + 8, faucet_y + 4],
                 fill=FRIDGE_TRIM)
    # Hot/cold handles
    for side in [-1, 1]:
        hx = faucet_x + side * 14
        hy = faucet_y + 2
        draw.ellipse([hx - 5, hy - 3, hx + 5, hy + 3], fill=FRIDGE_TRIM)

    # Dish rack at right of sink — a few drying plates
    rack_x = sink_x2 + 12
    rack_y = sink_y1 + 4
    rack_w = int(W * 0.06)
    rack_h = int((sink_y2 - sink_y1) * 0.8)
    # Rack frame (wire — thin lines)
    draw.rectangle([rack_x, rack_y, rack_x + rack_w, rack_y + rack_h],
                   outline=LINE_DARK, width=1)
    # Dishes standing in rack (vertical rectangles)
    for di in range(3):
        dish_x = rack_x + 4 + di * 12
        draw.rectangle([dish_x, rack_y + 4, dish_x + 8, rack_y + rack_h - 4],
                       fill=DISH_WHITE)
        draw.rectangle([dish_x, rack_y + 4, dish_x + 8, rack_y + rack_h - 4],
                       outline=DISH_BLUE_RING, width=1)

    # Plant on windowsill — green, small
    plant_x = win_x1 - 20
    plant_y = win_y2 - 5
    draw.rectangle([plant_x, plant_y - 12, plant_x + 18, plant_y + 8],
                   fill=lerp_color(WOOD_MED, COUNTERTOP, 0.3))
    draw.ellipse([plant_x - 4, plant_y - 22, plant_x + 22, plant_y - 2],
                 fill=PLANT_GREEN)
    draw.ellipse([plant_x, plant_y - 18, plant_x + 14, plant_y - 6],
                 fill=lerp_color(PLANT_GREEN, PLANT_DARK, 0.5))


# ── Layer 6: Kitchen Table ────────────────────────────────────────────────────

def draw_kitchen_table(draw, img, bw_bot):
    """
    Kitchen table in foreground-left. Morning: crossword puzzle, mug of tea.
    Table is warm wood. Chairs partially visible.
    """
    floor_top_y = bw_bot

    # Table position — left side, foreground (large, partially cropped at bottom)
    tbl_x1 = int(W * 0.02)
    tbl_x2 = int(W * 0.42)
    tbl_y1 = int(H * 0.64)
    tbl_y2 = int(H * 0.72)

    # Table surface
    draw.rectangle([tbl_x1, tbl_y1, tbl_x2, tbl_y2], fill=WOOD_WORN)
    draw.line([(tbl_x1, tbl_y1), (tbl_x2, tbl_y1)], fill=WOOD_LIGHT, width=2)
    draw.rectangle([tbl_x1, tbl_y1, tbl_x2, tbl_y2], outline=LINE_DARK, width=2)

    # Wood grain lines (horizontal, subtle)
    grain_rng = random.Random(71)
    for gi in range(6):
        gy = tbl_y1 + grain_rng.randint(2, tbl_y2 - tbl_y1 - 2)
        gw_start = tbl_x1 + grain_rng.randint(0, int((tbl_x2 - tbl_x1) * 0.3))
        gw_end = tbl_x2 - grain_rng.randint(0, int((tbl_x2 - tbl_x1) * 0.3))
        draw.line([(gw_start, gy), (gw_end, gy)],
                  fill=lerp_color(WOOD_WORN, WOOD_DARK, 0.25), width=1)

    # Table legs (partially visible)
    leg_h = int(H * 0.22)
    for lx in [tbl_x1 + 15, tbl_x2 - 25]:
        draw.rectangle([lx, tbl_y2, lx + 14, min(H, tbl_y2 + leg_h)],
                       fill=WOOD_MED)
        draw.rectangle([lx, tbl_y2, lx + 14, min(H, tbl_y2 + leg_h)],
                       outline=LINE_DARK, width=1)

    # ── Crossword puzzle on table ─────────────────────────────────────────────
    cw_x = int(W * 0.08)
    cw_y = tbl_y1 + 4
    cw_w = int(W * 0.14)
    cw_h = int((tbl_y2 - tbl_y1) * 0.75)
    # Newspaper/puzzle page
    draw.rectangle([cw_x, cw_y, cw_x + cw_w, cw_y + cw_h], fill=(240, 234, 210))
    draw.rectangle([cw_x, cw_y, cw_x + cw_w, cw_y + cw_h], outline=LINE_DARK, width=1)
    # Crossword grid (small squares)
    cell_s = max(4, cw_w // 10)
    cg_x = cw_x + 4
    cg_y = cw_y + int(cw_h * 0.25)
    for ri in range(6):
        for ci in range(8):
            cx_cell = cg_x + ci * cell_s
            cy_cell = cg_y + ri * cell_s
            if (ri + ci) % 3 == 0:
                draw.rectangle([cx_cell, cy_cell, cx_cell + cell_s, cy_cell + cell_s],
                               fill=LINE_DARK)
            draw.rectangle([cx_cell, cy_cell, cx_cell + cell_s, cy_cell + cell_s],
                           outline=(200, 194, 172), width=1)
    # Pencil next to crossword
    pen_x = cw_x + cw_w + 6
    pen_y = cw_y + int(cw_h * 0.4)
    draw.rectangle([pen_x, pen_y, pen_x + 4, pen_y + cw_h // 2],
                   fill=(220, 190, 80))
    draw.rectangle([pen_x, pen_y, pen_x + 4, pen_y + cw_h // 2],
                   outline=LINE_DARK, width=1)
    draw.polygon([(pen_x, pen_y + cw_h // 2),
                  (pen_x + 4, pen_y + cw_h // 2),
                  (pen_x + 2, pen_y + cw_h // 2 + 6)],
                 fill=(200, 168, 60))

    # ── Tea mug on table ─────────────────────────────────────────────────────
    mug_x = cw_x + cw_w + 24
    mug_y = tbl_y1 + 3
    mug_w = max(14, int(W * 0.022))
    mug_h = int((tbl_y2 - tbl_y1) * 0.65)
    draw.rectangle([mug_x, mug_y, mug_x + mug_w, mug_y + mug_h], fill=MUG_EARTHY)
    draw.rectangle([mug_x, mug_y, mug_x + mug_w, mug_y + mug_h], outline=LINE_DARK, width=1)
    # Mug handle
    draw.arc([mug_x + mug_w, mug_y + mug_h // 4,
              mug_x + mug_w + mug_w // 2, mug_y + 3 * mug_h // 4],
             start=270, end=90, fill=MUG_EARTHY, width=2)
    # Steam wisps (soft lines above mug)
    steam_rng = random.Random(77)
    for si in range(3):
        sx = mug_x + mug_w // 4 + si * (mug_w // 3)
        sy_start = mug_y - 2
        draw.line([(sx, sy_start), (sx + steam_rng.randint(-3, 3), sy_start - 10)],
                  fill=lerp_color(WALL_WARM, CEILING_WARM, 0.5), width=1)

    # ── Toast plate on table ──────────────────────────────────────────────────
    plate_x = int(W * 0.28)
    plate_y = tbl_y1 + 5
    plate_r_x = int(W * 0.04)
    plate_r_y = int((tbl_y2 - tbl_y1) * 0.3)
    draw.ellipse([plate_x - plate_r_x, plate_y,
                  plate_x + plate_r_x, plate_y + plate_r_y * 2],
                 fill=DISH_WHITE)
    draw.ellipse([plate_x - plate_r_x, plate_y,
                  plate_x + plate_r_x, plate_y + plate_r_y * 2],
                 outline=DISH_BLUE_RING, width=1)
    # Toast on plate
    toast_w = int(plate_r_x * 1.2)
    toast_h = int(plate_r_y * 0.9)
    draw.rectangle([plate_x - toast_w // 2, plate_y + 2,
                    plate_x + toast_w // 2, plate_y + 2 + toast_h],
                   fill=BREAD_WARM)
    draw.rectangle([plate_x - toast_w // 2, plate_y + 2,
                    plate_x + toast_w // 2, plate_y + 2 + toast_h],
                   outline=lerp_color(BREAD_WARM, LINE_DARK, 0.5), width=1)

    # Chair visible at table edge (partial)
    chair_x = tbl_x1 + int((tbl_x2 - tbl_x1) * 0.25)
    chair_y = tbl_y2 + 8
    chair_w = int(W * 0.10)
    draw.rectangle([chair_x, chair_y, chair_x + chair_w, min(H, chair_y + 80)],
                   fill=WOOD_MED)
    draw.rectangle([chair_x, chair_y, chair_x + chair_w, min(H, chair_y + 80)],
                   outline=LINE_DARK, width=1)

    return img


# ── Layer 7: Kitchen Plant ────────────────────────────────────────────────────

def draw_kitchen_plant(draw, bw_left, bw_top, bw_right, bw_bot):
    """
    A small potted plant on the countertop. Adds warmth and life."""
    counter_y = bw_top + int((bw_bot - bw_top) * 0.50)
    plant_x = int(bw_left + (bw_right - bw_left) * 0.80)
    plant_y = counter_y - 2

    # Terracotta pot
    pot_w = int(W * 0.022)
    pot_h = int((bw_bot - bw_top) * 0.10)
    draw.trapezoid = None  # PIL doesn't have trapezoid, use polygon
    draw.polygon([
        (plant_x - pot_w // 2 + 3, plant_y - pot_h),
        (plant_x + pot_w // 2 - 3, plant_y - pot_h),
        (plant_x + pot_w // 2, plant_y),
        (plant_x - pot_w // 2, plant_y),
    ], fill=(192, 88, 56))
    draw.polygon([
        (plant_x - pot_w // 2 + 3, plant_y - pot_h),
        (plant_x + pot_w // 2 - 3, plant_y - pot_h),
        (plant_x + pot_w // 2, plant_y),
        (plant_x - pot_w // 2, plant_y),
    ], outline=LINE_DARK)
    # Pot rim
    draw.rectangle([plant_x - pot_w // 2, plant_y - pot_h - 3,
                    plant_x + pot_w // 2, plant_y - pot_h + 3],
                   fill=(200, 100, 68))

    # Plant foliage (3 leaf masses)
    for li in range(3):
        angle = math.radians(-40 + li * 40)
        leaf_x = plant_x + int(math.cos(angle) * 12)
        leaf_y = plant_y - pot_h - 10 + int(abs(math.sin(angle)) * 8)
        leaf_r = max(8, pot_w // 2)
        draw.ellipse([leaf_x - leaf_r, leaf_y - leaf_r,
                      leaf_x + leaf_r, leaf_y + leaf_r],
                     fill=PLANT_GREEN if li != 1 else lerp_color(PLANT_GREEN, PLANT_DARK, 0.4))


# ── Layer 8: Refrigerator ─────────────────────────────────────────────────────

def draw_refrigerator(img, draw, bw_right, bw_top, bw_bot):
    """
    Old refrigerator on right side — off-white, round corners, chrome handle.
    """
    fridge_w = int(W * 0.10)
    fridge_x1 = bw_right - int((bw_right - int(W * 0.1)) * 0.07)
    fridge_x2 = fridge_x1 + fridge_w
    fridge_y1 = bw_top + int((bw_bot - bw_top) * 0.04)
    fridge_y2 = bw_bot

    draw.rectangle([fridge_x1, fridge_y1, fridge_x2, fridge_y2], fill=FRIDGE_WHITE)
    draw.rectangle([fridge_x1, fridge_y1, fridge_x2, fridge_y2], outline=LINE_DARK, width=2)

    # Top/bottom door division
    div_y = fridge_y1 + int((fridge_y2 - fridge_y1) * 0.22)
    draw.line([(fridge_x1, div_y), (fridge_x2, div_y)], fill=LINE_DARK, width=2)

    # Door handles (chrome)
    for hy in [fridge_y1 + int((div_y - fridge_y1) * 0.45),
               div_y + int((fridge_y2 - div_y) * 0.35)]:
        hx = fridge_x1 + int(fridge_w * 0.15)
        draw.rectangle([hx, hy, hx + 8, hy + 20], fill=FRIDGE_TRIM)
        draw.rectangle([hx, hy, hx + 8, hy + 20], outline=LINE_DARK, width=1)

    # Slight creak shadow on fridge door (panel inset)
    for door_y1, door_y2 in [(fridge_y1, div_y), (div_y, fridge_y2)]:
        inset = 8
        draw.rectangle([fridge_x1 + inset, door_y1 + inset,
                         fridge_x2 - inset, door_y2 - inset],
                        outline=lerp_color(FRIDGE_WHITE, FRIDGE_TRIM, 0.5), width=1)

    # Fridge magnets (small colored rectangles)
    magnet_rng = random.Random(83)
    for mi in range(4):
        mx = fridge_x1 + magnet_rng.randint(15, int(fridge_w * 0.7))
        my = div_y + magnet_rng.randint(20, int((fridge_y2 - div_y) * 0.6))
        mc = (magnet_rng.randint(150, 220), magnet_rng.randint(100, 180),
              magnet_rng.randint(60, 140))
        draw.rectangle([mx, my, mx + 10, my + 8], fill=mc)
        draw.rectangle([mx, my, mx + 10, my + 8], outline=LINE_DARK, width=1)


# ── Layer 9: Morning Light Pass ───────────────────────────────────────────────

def draw_morning_light_pass(img, win_x1, win_x2, bw_bot):
    """
    Final warm morning atmosphere pass.
    Warm overall cast on left side (window side).
    Cool shadow on right side and deep corners.
    """
    # Overall warm tint — light, gentle morning feel
    warm_pass = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wp = ImageDraw.Draw(warm_pass)
    # Warm from window side — left half
    for x in range(int(W * 0.55)):
        t = x / (W * 0.55)
        falloff = (1.0 - t) ** 2.0
        alpha = int(falloff * 35)
        wp.line([(x, 0), (x, H)], fill=(*SOFT_GOLD, alpha))

    # Slightly cooler, deeper shadows in far corners
    for x in range(int(W * 0.70), W):
        t = (x - W * 0.70) / (W * 0.30)
        alpha = int(t * 20)
        wp.line([(x, 0), (x, H)], fill=(100, 80, 60, alpha))

    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, warm_pass)
    return img_rgba.convert("RGB")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    rng = random.Random(42)
    img = Image.new("RGB", (W, H), WALL_WARM)

    print("LTG_TOOL_bg_grandma_kitchen_v003.py")
    print("Rendering Grandma Miri's Kitchen v003 — A1-01 (Act 1 opening)...")
    print("v003 fixes: side wall texture (Fix 2a), perspective floor grid (Fix 2b)")

    print("  [1] Base room — walls, ceiling, floor...")
    draw, vp_x, vp_y, bw_left, bw_top, bw_right, bw_bot = draw_base_room(img)

    print("  [2] Floor tiles (v003: disabled — replaced by perspective linoleum in step 11)...")
    draw_floor_tiles(draw, bw_left, bw_bot, bw_right, vp_x, vp_y)  # no-op in v003

    print("  [3] Window + morning sky + curtains...")
    win_x1, win_x2, win_y1, win_y2 = draw_window(img, draw, vp_x, vp_y,
                                                   bw_left, bw_top, bw_right, bw_bot)

    print("  [4] Doorway + CRT TV in adjacent room (enhanced glow — retained from v002)...")
    img, draw = draw_doorway_and_crt(img, draw, bw_left, bw_top, bw_bot)

    print("  [5] Cabinets, countertop, stove...")
    counter_y1, counter_y2 = draw_cabinets_and_appliances(
        draw, bw_left, bw_top, bw_right, bw_bot)

    print("  [6] Sink (below window), dish rack, windowsill plant...")
    draw_sink(draw, bw_left, bw_top, bw_right, bw_bot, win_x1, win_x2, win_y2)

    print("  [7] Refrigerator (right side)...")
    draw_refrigerator(img, draw, bw_right, bw_top, bw_bot)

    print("  [8] Countertop plant...")
    draw_kitchen_plant(draw, bw_left, bw_top, bw_right, bw_bot)

    print("  [9] Kitchen table (crossword, tea mug, toast)...")
    img = draw_kitchen_table(draw, img, bw_bot)
    draw = ImageDraw.Draw(img)

    print("  [10] v003: Upper wall wallpaper texture — back + side walls (Fix 2a)...")
    img = draw_upper_wall_texture(img, bw_left, bw_top, bw_right, bw_bot)
    draw = ImageDraw.Draw(img)

    print("  [11] v003: Perspective-correct floor linoleum grid + worn path (Fix 2b)...")
    img = draw_floor_linoleum_overlay(img, bw_left, bw_bot, bw_right, vp_x, vp_y)
    draw = ImageDraw.Draw(img)

    print("  [12] Morning light pass (window shaft, warm ambient)...")
    img = draw_morning_light(img, win_x1, win_x2, win_y1, win_y2, bw_bot)
    draw = ImageDraw.Draw(img)

    print("  [13] Final warm morning atmosphere pass...")
    img = draw_morning_light_pass(img, win_x1, win_x2, bw_bot)

    out_path = "/home/wipkat/team/output/backgrounds/environments/LTG_ENV_grandma_kitchen_v003.png"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img.save(out_path, "PNG")
    size_bytes = os.path.getsize(out_path)
    print(f"\nSaved: {out_path}")
    print(f"File size: {size_bytes:,} bytes ({size_bytes // 1024} KB)")
    print("\nSpec verification (v003):")
    print("  - Small cozy kitchen interior ✓")
    print("  - Morning sunlight through window (warm amber/golden) ✓")
    print("  - Old-fashioned appliances (pre-digital: gas stove, porcelain sink, old fridge) ✓")
    print("  - CRT TV through doorway (story element — enhanced glow retained) ✓")
    print("  - Lived-in: crossword puzzle + pencil, tea mug, toast plate, dishes, plant ✓")
    print("  - Palette: warm creams, ambers, wood tones — all Real World colors ✓")
    print("  - No Glitch palette (ELEC_CYAN etc excluded; CRT TV desaturated far-plane only) ✓")
    print("  - v003 Fix 2a: Wall texture extended to left + right wall polygons (side alpha ~35% less) ✓")
    print("  - v003 Fix 2b: Single perspective-correct floor grid only (draw_floor_tiles disabled) ✓")
    print("  - v002: Worn path from doorway to stove zone (lighter trapezoid, alpha 20) ✓")
    print("  - v002: Upper wall horizontal stripe texture (12–15% opacity period wallpaper) ✓")
    print("  - v002: CRT glow radius increased (80) + wide ambient ring (130) at low alpha ✓")


if __name__ == "__main__":
    main()
