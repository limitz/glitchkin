#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_bg_grandma_kitchen.py — Grandma Miri's Kitchen Background v008
"Luma & the Glitchkin" — Background & Environment Design
Artist: Jordan Reed | Cycle 39 | v006 Hana Okonkwo | Cycle 43 | v007 Hana Okonkwo | Cycle 44 | v008 Hana Okonkwo | Cycle 48

Used in: A1-01 (Act 1 opening scene)
Narrative: Act 1 opening. Warm morning. Pre-digital world. Home = safe.
Key: This is the room where everything begins — Luma sees the Glitch Layer
     for the first time through the CRT doorway. Must read as both:
     (a) warmest, most domestic space in the show
     (b) harboring the "other side" through the cool doorway on the right

v005 — Dual-Miri Visual Plant (Alex Chen directive, C39):

  Single targeted addition to v004:
  - Handwritten "MIRI" label on a small scrap of paper on the fridge door
v006 — C43 (Hana Okonkwo): Migrated MIRI label from bespoke pixel-line
  implementation to canonical draw_pixel_text() from LTG_TOOL_pixel_font_v001.
  - Positioned right-center of fridge body, near the travel magnets
  - Real World palette only: dark ink (LINE_DARK) on cream paper (AGED_CREAM)
  - Must be legible at full PNG resolution but easy to miss at thumbnail scale
  - Zero GL-palette colors — no ELEC_CYAN, no UV_PURPLE, no GL pigments
  - The label looks like any domestic sticky note / label at first glance
  - Story plant: Grandma Miri -> Glitch Layer Miri name connection
    (Season 1 finale payoff — audience can rewatch pilot to find this hint)

  MIRI label approximate pixel position:
    fridge_x1 approx 866, div_y approx 352 (bottom of fridge freezer section)
    label paper rect: x1=896, y1=460, x2=940, y2=478  (44x18px cream paper scrap)
    "MIRI" text: drawn pixel-by-pixel in LINE_DARK ink, centered on paper
    Paper held by a small magnet pip above it (warm amber circle, 3px radius)

v008 — C48 (Hana Okonkwo): Furniture perspective fix (Chiara C18/C47 flat-elevation critique).
  Per docs/perspective-rules.md and furniture_vp_spec_c48.md:
  - Kitchen table: flat rect -> VP-convergent trapezoid with foreshortened top surface
  - Chair: flat rect -> perspective seat plane + angled backrest
  - Countertop: flat rect -> trapezoid top surface with front edge visible
  - Fridge: flat rect -> body with side face visible (foreshortens toward VP)
  - Upper/lower cabinets: added side depth reveal (3px) on VP-facing edge
  All convergence toward VP_X=512, VP_Y=273. No change to color, lighting, or QA passes.

v007 — C44 (Hana Okonkwo): Fix line_weight QA FAIL (pre-existing outliers=3).
  Root cause: image boundary rows (y=0, y=719) read as 1280px-wide edge runs
  by render_qa FIND_EDGES scan → 3 outliers (mean=269px, std=308px).
  Fix: add paper_texture() (alpha=16, scale=40) + vignette(strength=45) final
  passes from LTG_TOOL_render_lib before save. Texture breaks image-border
  edge runs; vignette softens corners. Also migrated save to flatten_rgba_to_rgb().
  All v006 content unchanged.

All v004 improvements retained (no other changes):
  - Deep shadow pass (value floor <=30)
  - Warm/cool temperature split (separation >=20)
  - Miri-specific details (calendar, rose mug, knitting bag, apron, magnets)
  - Side wall stripe texture, perspective floor grid, CRT dual-ring glow
  - Morning light shaft from window, worn floor path

Output: /home/wipkat/team/output/backgrounds/environments/LTG_ENV_grandma_kitchen.png
"""

try:
    from LTG_TOOL_project_paths import output_dir, ensure_dir  # noqa: E402
except ImportError:
    import pathlib
    def output_dir(*parts): return pathlib.Path("/home/wipkat/team/output").joinpath(*parts)
    def ensure_dir(path): path.mkdir(parents=True, exist_ok=True); return path
import math
import random
import os
import sys
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from LTG_TOOL_pixel_font_v001 import draw_pixel_text  # noqa: E402
from LTG_TOOL_render_lib import paper_texture, vignette, flatten_rgba_to_rgb  # noqa: E402

W, H = 1280, 720

# ── Real World Palette (master_palette.md + kitchen spec) ────────────────────
# Primary warm tones
WARM_CREAM       = (250, 240, 220)    # cream wall base
AGED_CREAM       = (238, 226, 198)    # slightly older, more used
SUNLIT_AMBER     = (212, 146,  58)    # #D4923A morning sunlight — canonical RW-03
MORNING_GOLD     = (255, 200,  80)    # bright morning window light
SOFT_GOLD        = (232, 201,  90)    # secondary warm highlights

WOOD_DARK        = (100,  65,  32)    # dark wood cabinets (richer, more saturated)
WOOD_MED         = (148,  98,  52)    # medium wood (table, chairs)
WOOD_LIGHT       = (186, 138,  78)    # lighter wood surfaces
WOOD_WORN        = (170, 128,  70)    # worn wood counter

# Walls, floor, ceiling
WALL_WARM        = (238, 218, 182)    # kitchen wall warm cream (slightly deeper than v003)
WALL_SHADOW      = (190, 168, 136)    # wall in shadow zones
CEILING_WARM     = (242, 232, 208)    # ceiling warm white
FLOOR_TILE_WARM  = (200, 184, 150)    # linoleum floor tile light
FLOOR_TILE_DARK  = (178, 162, 130)    # linoleum floor tile dark
FLOOR_WORN_PATH  = (214, 200, 166)    # worn traffic path (lighter)

# Deep shadows — the critical new addition for v004
DEEP_COCOA       = ( 59,  40,  32)    # #3B2820 — deepest shadow (master_palette)
NEAR_BLACK_WARM  = ( 28,  18,  10)    # near-black warm (crevices, deepest corners)
SHADOW_DEEP      = ( 70,  48,  28)    # deep shadow (counter undersides, cabinet tops)
SHADOW_MID       = (110,  78,  46)    # mid shadow
SHADOW_WARM      = (158, 120,  78)    # warm shadow tones

# Appliances (old-fashioned, no screens)
FRIDGE_WHITE     = (228, 222, 208)    # old refrigerator off-white (more yellowed)
FRIDGE_TRIM      = (180, 172, 154)    # fridge trim/handle
STOVE_CREAM      = (220, 212, 196)    # old gas stove cream
STOVE_IRON       = (138, 130, 118)    # cast iron burner rings
STOVE_KNOB       = (158, 138, 102)    # bakelite knobs
SINK_PORCELAIN   = (222, 218, 204)    # porcelain sink
COUNTERTOP       = (190, 172, 138)    # laminate countertop
COUNTER_EDGE     = (152, 136, 102)    # counter edge darker

# Food + kitchen items
DISH_WHITE       = (234, 230, 220)    # dinner plate
DISH_BLUE_RING   = ( 90, 118, 148)    # blue-ringed china
TEAPOT_RED       = (180,  60,  38)    # red enamel teapot
MUG_EARTHY       = (152, 104,  64)    # earthenware mug
BREAD_WARM       = (190, 148,  78)    # bread loaf
PLANT_GREEN      = ( 76, 126,  60)    # kitchen plant
PLANT_DARK       = ( 48,  78,  36)    # plant shadow
CURTAIN_WARM     = (230, 188, 118)    # window curtain warm yellow

# CRT TV (adjacent room — far plane, cool light SOURCE of story)
DOORWAY_DARK     = (120, 100,  68)    # adjacent room mid shadow
DOORWAY_DEEP     = ( 55,  38,  22)    # deep room shadow (near DEEP_COCOA)
CRT_SCREEN_GLOW  = ( 42,  98, 118)    # CRT screen (desaturated — far plane)
CRT_BODY         = (108,  94,  74)    # CRT TV body
# CRT cool spill into kitchen — this is the critical new light source
# Using desaturated Electric Cyan toned down for far-plane distance
CRT_COOL_SPILL   = (  0, 130, 148)    # desaturated CRT cool light in kitchen

# Outline / line work
LINE_DARK        = ( 88,  60,  32)    # dark brown line work


def lerp_color(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def alpha_composite_rect(img, x0, y0, x1, y1, color_rgb, alpha):
    """Draw a filled rectangle at given alpha using alpha_composite."""
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.rectangle([x0, y0, x1, y1], fill=(*color_rgb, alpha))
    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, overlay)
    return img_rgba.convert("RGB")


def alpha_composite_poly(img, pts, color_rgb, alpha):
    """Draw a filled polygon at given alpha using alpha_composite."""
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.polygon(pts, fill=(*color_rgb, alpha))
    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, overlay)
    return img_rgba.convert("RGB")


# ── Layer 1: Base Walls, Ceiling, Floor ──────────────────────────────────────

def draw_base_room(img):
    """
    Kitchen perspective: looking toward window wall (back wall).
    Left wall: partial view with doorway to adjacent room (CRT side).
    Right wall: cabinets and stove/fridge.
    Floor: old linoleum tile, worn path from sink to table.

    v004: Canvas 1280×720 (direct). Vanishing point adjusted for smaller canvas.
    """
    draw = ImageDraw.Draw(img)

    # Vanishing point — slightly left of center, upper third
    vp_x = int(W * 0.40)
    vp_y = int(H * 0.38)

    # ── Ceiling ─────────────────────────────────────────────────────────────
    ceil_poly = [
        (0, 0), (W, 0),
        (W, vp_y - 40),
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
        (W, vp_y - 40),
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


# ── Layer 2: Deep Shadow Pass — the critical v004 addition ───────────────────

def draw_deep_shadows(img, vp_x, vp_y, bw_left, bw_top, bw_right, bw_bot):
    """
    v004 FIX 1: Push shadow zones toward value ≤30.

    Targeting:
    - Ceiling corners (darkest — furthest from window)
    - Cabinet undersides (sharp shadow below each upper cabinet door)
    - Below countertop (deep counter-underside band)
    - Floor corners (foreground floor sides)
    - Doorway interior (adjacent room — already dark, deepen)
    - Table underside shadow
    - Wall/ceiling junction in shadow zones

    Color: DEEP_COCOA (#3B2820 = 59,40,32) for mid-depth shadows,
           NEAR_BLACK_WARM (28,18,10) for deepest crevices/corners
    """
    # ── Ceiling corners — dark gradient from edges in ───────────────────────
    ceil_shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cs = ImageDraw.Draw(ceil_shadow)

    # Left ceiling corner: from x=0 fading right
    for x in range(int(W * 0.18)):
        t = 1.0 - (x / (W * 0.18))
        alpha = int(t ** 1.5 * 200)   # pushes toward ~28 value (28,18,10 at alpha 200)
        cs.line([(x, 0), (x, int(H * 0.22))],
                fill=(*NEAR_BLACK_WARM, alpha))

    # Right ceiling corner: from x=W fading left
    for x in range(int(W * 0.85), W):
        t = (x - W * 0.85) / (W * 0.15)
        alpha = int(t ** 1.2 * 180)
        cs.line([(x, 0), (x, int(H * 0.25))],
                fill=(*NEAR_BLACK_WARM, alpha))

    # Top edge ceiling: dark band at very top
    for y in range(int(H * 0.06)):
        t = 1.0 - (y / (H * 0.06))
        alpha = int(t * 150)
        cs.line([(0, y), (W, y)], fill=(*DEEP_COCOA, alpha))

    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, ceil_shadow)
    img = img_rgba.convert("RGB")
    return img


def draw_cabinet_shadows(img, draw, bw_left, bw_top, bw_right, bw_bot):
    """
    v004 FIX 1b: Sharp drop-shadow below each upper cabinet.
    The underside of cabinets is deep shadow (near DEEP_COCOA).
    Counter undersides also get deep shadow band.
    """
    cab_bottom = bw_top + int((bw_bot - bw_top) * 0.42)
    shadow_h = max(4, int((bw_bot - bw_top) * 0.04))  # shadow band height

    # Shadow below each upper cabinet
    upper_cab_specs = [
        (0.58, 0.70),
        (0.70, 0.83),
        (0.83, 0.96),
    ]
    for (x1f, x2f) in upper_cab_specs:
        cx1 = int(bw_left + (bw_right - bw_left) * x1f)
        cx2 = int(bw_left + (bw_right - bw_left) * x2f)
        # Shadow band immediately below cabinet bottom edge
        sy1 = cab_bottom
        sy2 = cab_bottom + shadow_h
        for y in range(sy1, sy2):
            t = 1.0 - (y - sy1) / (sy2 - sy1)
            alpha = int(t ** 0.8 * 240)  # very dark at edge
            draw.line([(cx1, y), (cx2, y)],
                      fill=lerp_color(NEAR_BLACK_WARM, DEEP_COCOA, 1.0 - t))

    # Counter underside shadow (below countertop edge)
    counter_y1 = bw_top + int((bw_bot - bw_top) * 0.52)
    ct_x1 = bw_left + int((bw_right - bw_left) * 0.38)
    ct_x2 = bw_right
    under_shadow_h = max(5, int((bw_bot - bw_top) * 0.05))
    for y in range(counter_y1, counter_y1 + under_shadow_h):
        t = 1.0 - (y - counter_y1) / under_shadow_h
        alpha = int(t ** 0.7 * 220)
        draw.line([(ct_x1, y), (ct_x2, y)],
                  fill=lerp_color(NEAR_BLACK_WARM, DEEP_COCOA, 0.4))

    return img


def draw_floor_corner_shadows(img):
    """
    v004 FIX 1c: Deep shadow in floor corners and bottom edges.
    Floor should have value ≤30 in far corners where walls meet floor.
    """
    floor_shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    fs = ImageDraw.Draw(floor_shadow)

    # Left floor corner: along left wall bottom
    for y in range(int(H * 0.88), H):
        t = (y - H * 0.88) / (H - H * 0.88)
        t_rev = 1.0 - t
        for x in range(int(W * 0.15)):
            xt = 1.0 - (x / (W * 0.15))
            alpha = int(min(255, xt ** 1.2 * t_rev * 220 + t * 80))
            fs.point([(x, y)], fill=(*NEAR_BLACK_WARM, alpha))

    # Right floor corner: along right wall bottom
    for y in range(int(H * 0.82), H):
        t = (y - H * 0.82) / (H - H * 0.82)
        for x in range(int(W * 0.85), W):
            xt = (x - W * 0.85) / (W * 0.15)
            alpha = int(min(255, xt ** 1.1 * (1.0 - t * 0.3) * 200))
            fs.point([(x, y)], fill=(*NEAR_BLACK_WARM, alpha))

    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, floor_shadow)
    return img_rgba.convert("RGB")


def draw_floor_linoleum_overlay(img, bw_left, bw_bot, bw_right, vp_x, vp_y):
    """
    Perspective-correct linoleum tile grid (from v003, retained).
    Single floor system — no contradictory spatial grids.
    """
    floor_top_y = bw_bot

    GRID_LINE_COLOR = (138, 120,  92, 25)  # warm brown, alpha 25

    grid_overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grid_overlay)

    # Horizontal rows — non-linear spacing
    num_rows = 10
    for i in range(1, num_rows + 1):
        t = (i / num_rows) ** 1.5
        fy = floor_top_y + int(t * (H - floor_top_y))
        if fy >= H:
            break
        gd.line([(0, fy), (W, fy)], fill=GRID_LINE_COLOR, width=2)

    # Vertical columns — converge to vp_x
    num_cols = 14
    for i in range(num_cols + 1):
        bx = int((i / num_cols) * W)
        gd.line([(vp_x, floor_top_y), (bx, H)], fill=GRID_LINE_COLOR, width=1)

    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, grid_overlay)
    img = img_rgba.convert("RGB")

    # Worn path trapezoid
    worn_path_overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(worn_path_overlay)
    wp_top_y  = floor_top_y
    wp_bot_y  = H
    wp_top_cx = int(W * 0.32)
    wp_bot_cx = int(W * 0.46)
    wp_top_hw = int(W * 0.12)
    wp_bot_hw = int(W * 0.20)
    worn_poly = [
        (wp_top_cx - wp_top_hw, wp_top_y),
        (wp_top_cx + wp_top_hw, wp_top_y),
        (wp_bot_cx + wp_bot_hw, wp_bot_y),
        (wp_bot_cx - wp_bot_hw, wp_bot_y),
    ]
    WORN_PATH_LIGHT = (218, 204, 172, 20)
    wd.polygon(worn_poly, fill=WORN_PATH_LIGHT)

    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, worn_path_overlay)
    return img_rgba.convert("RGB")


# ── Layer 3: Window ───────────────────────────────────────────────────────────

def draw_window(img, draw, vp_x, vp_y, bw_left, bw_top, bw_right, bw_bot):
    """
    Kitchen window above sink. Morning light source — canonical SUNLIT_AMBER.
    v004: Window brightened; exterior sky near-255 at top edge for value ceiling.
    """
    win_x1 = int(W * 0.32)
    win_x2 = int(W * 0.56)
    win_y1 = bw_top + int((bw_bot - bw_top) * 0.06)
    win_y2 = bw_top + int((bw_bot - bw_top) * 0.44)
    win_w = win_x2 - win_x1
    win_h = win_y2 - win_y1

    # Window frame (painted wood)
    draw.rectangle([win_x1 - 5, win_y1 - 5, win_x2 + 5, win_y2 + 5],
                   fill=WOOD_LIGHT)

    # Morning sky — near-255 at top edge (value ceiling fix), gradient down
    for y in range(win_y1, win_y2):
        t = (y - win_y1) / win_h
        # Near top: full MORNING_GOLD brightness. Near bottom: softer warm green-cream
        sky_col = lerp_color((255, 220, 110), (190, 210, 178), t)
        draw.line([(win_x1, y), (win_x2, y)], fill=sky_col)

    # Window pane dividers
    mid_x = (win_x1 + win_x2) // 2
    mid_y = (win_y1 + win_y2) // 2
    draw.line([(mid_x, win_y1), (mid_x, win_y2)], fill=WOOD_LIGHT, width=4)
    draw.line([(win_x1, mid_y), (win_x2, mid_y)], fill=WOOD_LIGHT, width=4)

    # Curtains
    curtain_w = int(win_w * 0.22)
    lc_x1 = win_x1 - 5 - curtain_w
    lc_x2 = win_x1 + curtain_w // 3
    draw.rectangle([lc_x1, win_y1 - 8, lc_x2, win_y2 + 18], fill=CURTAIN_WARM)
    for fi in range(3):
        fx = lc_x1 + int(fi * curtain_w * 0.28)
        draw.line([(fx, win_y1 - 8), (fx, win_y2 + 18)],
                  fill=lerp_color(CURTAIN_WARM, SHADOW_MID, 0.3), width=2)

    rc_x1 = win_x2 - curtain_w // 3
    rc_x2 = win_x2 + 5 + curtain_w
    draw.rectangle([rc_x1, win_y1 - 8, rc_x2, win_y2 + 18], fill=CURTAIN_WARM)
    for fi in range(3):
        fx = rc_x1 + int(fi * curtain_w * 0.35)
        draw.line([(fx, win_y1 - 8), (fx, win_y2 + 18)],
                  fill=lerp_color(CURTAIN_WARM, SHADOW_MID, 0.3), width=2)

    # Curtain rod
    rod_y = win_y1 - 12
    draw.line([(lc_x1 - 8, rod_y), (rc_x2 + 8, rod_y)], fill=FRIDGE_TRIM, width=3)
    draw.ellipse([lc_x1 - 14, rod_y - 5, lc_x1 - 4, rod_y + 5], fill=FRIDGE_TRIM)
    draw.ellipse([rc_x2 + 4, rod_y - 5, rc_x2 + 14, rod_y + 5], fill=FRIDGE_TRIM)

    return win_x1, win_x2, win_y1, win_y2


# ── Layer 4: Warm Light (LEFT) — greatly strengthened for v004 ───────────────

def draw_warm_light(img, win_x1, win_x2, win_y1, win_y2, bw_bot):
    """
    v004 FIX 2a: Warm morning light from window, LEFT side.
    Strengthened significantly: alpha max 80 (was 48) for column gradient.
    Light shaft trapezoid as solid geometry (not just ambient).
    Floor pool hotspot near-255 at center.
    Canonical SUNLIT_AMBER (#D4923A = 212,146,58) used.
    """
    light_overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(light_overlay)

    win_cx = (win_x1 + win_x2) // 2
    light_spread = int(W * 0.48)

    # Main warm column gradient — left half dominant
    for x in range(max(0, win_cx - light_spread), min(W, win_cx + light_spread)):
        dist = abs(x - win_cx)
        t = dist / light_spread
        falloff = (1.0 - t) ** 1.6
        alpha = int(falloff * 80)   # strengthened from v003's 48
        if alpha > 0:
            ld.line([(x, win_y1), (x, bw_bot)], fill=(*SUNLIT_AMBER, alpha))

    # Warm ceiling glow above window (near-255 at window top edge)
    for x in range(win_x1, win_x2):
        ld.line([(x, 0), (x, win_y1)], fill=(*SOFT_GOLD, 40))

    # Light shaft trapezoid — direct beam geometry
    # Projects from window bottom, fans toward floor
    shaft_top_x1 = win_x1 + int((win_x2 - win_x1) * 0.10)
    shaft_top_x2 = win_x2 - int((win_x2 - win_x1) * 0.10)
    shaft_bot_x1 = max(0, shaft_top_x1 - int(W * 0.08))
    shaft_bot_x2 = min(W, shaft_top_x2 + int(W * 0.08))
    shaft_y1 = win_y2
    shaft_y2 = bw_bot + int((H - bw_bot) * 0.40)

    shaft_pts = [
        (shaft_top_x1, shaft_y1),
        (shaft_top_x2, shaft_y1),
        (shaft_bot_x2, shaft_y2),
        (shaft_bot_x1, shaft_y2),
    ]
    # Draw shaft in multiple passes (bright core + soft edges)
    ld.polygon(shaft_pts, fill=(*MORNING_GOLD, 25))
    # Brighter inner core
    inner_pts = [
        ((shaft_top_x1 + shaft_top_x2) // 2 - 20, shaft_y1),
        ((shaft_top_x1 + shaft_top_x2) // 2 + 20, shaft_y1),
        ((shaft_bot_x1 + shaft_bot_x2) // 2 + 30, shaft_y2),
        ((shaft_bot_x1 + shaft_bot_x2) // 2 - 30, shaft_y2),
    ]
    ld.polygon(inner_pts, fill=(*MORNING_GOLD, 35))

    # Floor light pool — near-255 hotspot at center
    pool_cx = (shaft_bot_x1 + shaft_bot_x2) // 2
    pool_cy = bw_bot + int((H - bw_bot) * 0.22)
    for r in range(80, 0, -1):
        t = 1.0 - r / 80.0
        # Inner hotspot: near-255 brightness
        alpha = int(t * t * 60)
        ld.ellipse([pool_cx - r, pool_cy - r // 3,
                    pool_cx + r, pool_cy + r // 3],
                   fill=(*MORNING_GOLD, alpha))

    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, light_overlay)
    return img_rgba.convert("RGB")


# ── Layer 5: Cool CRT Light (RIGHT/DOORWAY) — new for v004 ───────────────────

def draw_crt_cool_light(img, door_cx, door_cy, bw_left, bw_bot):
    """
    v004 FIX 2b: CRT cool light spill from doorway into kitchen.
    This is the critical warm/cool separation driver.

    The CRT TV in the adjacent room casts cool desaturated light through the
    doorway opening, lighting the right half of the kitchen (as seen from camera).
    This light is:
    - CRT_COOL_SPILL = (0, 130, 148) — desaturated teal, not GL-01b which is
      character-specific. This reads as old TV screen emission from a distance.
    - Column gradient from doorway rightward (falloff toward camera)
    - Alpha max 65 — strong enough for QA warm/cool separation ≥20

    Additional: A cool spill ellipse on the adjacent room floor visible through
    doorway, showing where TV actually sits.
    """
    cool_overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(cool_overlay)

    # Cool light emanates from doorway (left-center of back wall)
    # Spreads rightward and downward across kitchen floor
    door_spread_x = int(W * 0.60)   # how far cool light reaches horizontally

    # Horizontal gradient from doorway rightward
    for x in range(max(0, door_cx - int(W * 0.05)), min(W, door_cx + door_spread_x)):
        dist_from_door = max(0, x - door_cx)
        t = dist_from_door / door_spread_x
        falloff = (1.0 - t) ** 1.8
        alpha = int(falloff * 65)
        if alpha > 0:
            # Cool light affects wall and floor zones (not ceiling — it's low source)
            cd.line([(x, bw_bot - int(H * 0.15)), (x, H)],
                    fill=(*CRT_COOL_SPILL, alpha))

    # Cool ambient on right wall (cabinet/fridge zone)
    for x in range(int(W * 0.62), W):
        t = (x - W * 0.62) / (W - W * 0.62)
        alpha = int((1.0 - t) ** 2.0 * 28)
        cd.line([(x, bw_bot - int(H * 0.12)), (x, bw_bot)],
                fill=(*CRT_COOL_SPILL, alpha))

    # Strong cool spill just inside doorway arch (the actual doorway opening)
    door_spill_r = int(H * 0.15)
    for r in range(door_spill_r, 0, -1):
        t = 1.0 - r / door_spill_r
        alpha = int(t ** 1.2 * 80)
        cd.ellipse([door_cx - r, door_cy - r,
                    door_cx + r, door_cy + r],
                   fill=(*CRT_COOL_SPILL, alpha))

    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, cool_overlay)
    return img_rgba.convert("RGB")


# ── Layer 6: Doorway + CRT TV (story element) ────────────────────────────────

def draw_doorway_and_crt(img, draw, bw_left, bw_top, bw_bot):
    """
    Doorway on left wall — adjacent living room visible.
    CRT TV in adjacent room: important story element.

    v004: Doorway interior uses DOORWAY_DEEP for near-black shadow.
    CRT screen glow more prominent (story element).
    Returns door_cx, door_cy for cool spill pass.
    """
    # Doorway position: left portion of back wall
    door_x1 = bw_left + int((bw_bot - bw_top) * 0.05)
    door_x2 = door_x1 + int(W * 0.12)
    door_y1 = bw_top + int((bw_bot - bw_top) * 0.10)
    door_y2 = bw_bot - 4

    # Door frame (wood trim)
    frame_w = 5
    draw.rectangle([door_x1 - frame_w, door_y1 - frame_w,
                    door_x2 + frame_w, door_y2], fill=WOOD_MED)

    # Adjacent room — deep shadow (near DEEP_COCOA for value floor)
    draw.rectangle([door_x1, door_y1, door_x2, door_y2], fill=DOORWAY_DEEP)

    # Far wall of adjacent room — slightly lighter (where TV sits)
    far_wall_x1 = door_x1 + int((door_x2 - door_x1) * 0.20)
    for y in range(door_y1, door_y2):
        t = (y - door_y1) / (door_y2 - door_y1)
        col = lerp_color(DOORWAY_DARK, DOORWAY_DEEP, t * 0.6)
        draw.line([(far_wall_x1, y), (door_x2, y)], fill=col)

    # CRT TV in adjacent room — visible in lower portion of doorway
    tv_x1 = door_x1 + int((door_x2 - door_x1) * 0.06)
    tv_x2 = door_x1 + int((door_x2 - door_x1) * 0.78)
    tv_y1 = door_y1 + int((door_y2 - door_y1) * 0.48)
    tv_y2 = door_y2 - int((door_y2 - door_y1) * 0.05)

    tv_w = tv_x2 - tv_x1
    tv_h = tv_y2 - tv_y1

    # CRT body (old plastic, yellowed)
    draw.rectangle([tv_x1, tv_y1, tv_x2, tv_y2], fill=(98, 84, 64))
    draw.rectangle([tv_x1, tv_y1, tv_x2, tv_y2], outline=LINE_DARK, width=1)

    # CRT screen — visibly ON (stronger glow than v003 — it's the story element)
    scr_margin = max(2, tv_w // 10)
    scr_x1 = tv_x1 + scr_margin
    scr_x2 = tv_x2 - scr_margin
    scr_y1 = tv_y1 + int(tv_h * 0.08)
    scr_y2 = tv_y2 - int(tv_h * 0.25)

    # Screen gradient — active, emitting light
    for y in range(scr_y1, scr_y2):
        t = (y - scr_y1) / max(1, scr_y2 - scr_y1)
        # Center brighter, edges darker — CRT focal point
        row_col = lerp_color(( 60, 140, 160), ( 20,  68,  85), t)
        draw.line([(scr_x1, y), (scr_x2, y)], fill=row_col)
    draw.rectangle([scr_x1, scr_y1, scr_x2, scr_y2], outline=LINE_DARK, width=1)

    # Speaker grille and knobs
    grille_x = tv_x1 + int(tv_w * 0.08)
    grille_y = tv_y2 - int(tv_h * 0.22)
    grille_h = int(tv_h * 0.18)
    for gi in range(4):
        draw.line([(grille_x + gi * 3, grille_y),
                   (grille_x + gi * 3, grille_y + grille_h)],
                  fill=LINE_DARK, width=1)

    for ki in range(2):
        kx = tv_x2 - int(tv_w * 0.15) + ki * int(tv_w * 0.08)
        ky = tv_y1 + int(tv_h * 0.55)
        draw.ellipse([kx - 3, ky - 3, kx + 3, ky + 3], fill=LINE_DARK)

    # CRT glow inside adjacent room (strong — active screen)
    crt_spill = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cs = ImageDraw.Draw(crt_spill)

    scr_cx = (scr_x1 + scr_x2) // 2
    scr_cy = (scr_y1 + scr_y2) // 2

    # Primary glow (confined to doorway area)
    for r in range(70, 0, -1):
        t = 1.0 - r / 70.0
        alpha = int(t * t * 45)
        cs.ellipse([scr_cx - r, scr_cy - r // 2,
                    scr_cx + r, scr_cy + r // 2],
                   fill=(*CRT_SCREEN_GLOW, alpha))

    # Floor spill inside adjacent room
    for r in range(50, 0, -1):
        t = 1.0 - r / 50.0
        alpha = int(t * t * 35)
        cs.ellipse([tv_x1 - r // 4, tv_y2 - 3,
                    tv_x2 + r // 4, tv_y2 + r // 3],
                   fill=(*CRT_COOL_SPILL, alpha))

    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, crt_spill)
    img = img_rgba.convert("RGB")
    draw = ImageDraw.Draw(img)

    # Return door center for cool spill pass
    door_cx = (door_x1 + door_x2) // 2
    door_cy = (door_y1 + door_y2) // 2

    return img, draw, door_cx, door_cy


# ── Layer 7: Upper Wall Wallpaper Texture ─────────────────────────────────────

def draw_upper_wall_texture(img, bw_left, bw_top, bw_right, bw_bot, vp_y):
    """
    Period wallpaper texture on back wall and side walls (from v003, retained).
    v004: Side wall alphas unchanged; back wall retained.
    """
    wall_height = bw_bot - bw_top
    upper_wall_y1 = bw_top
    upper_wall_y2 = bw_top + int(wall_height * 0.50)

    STRIPE_A = (246, 236, 208)
    STRIPE_B = (228, 210, 172)
    STRIPE_HEIGHT = 10
    STRIPE_ALPHA_A = 12
    STRIPE_ALPHA_B = 15
    SIDE_ALPHA_A = 8
    SIDE_ALPHA_B = 10

    # Back wall stripes
    stripe_overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stripe_overlay)
    y = upper_wall_y1
    stripe_idx = 0
    while y < upper_wall_y2:
        y_end = min(y + STRIPE_HEIGHT, upper_wall_y2)
        col = (*STRIPE_A, STRIPE_ALPHA_A) if stripe_idx % 2 == 0 else (*STRIPE_B, STRIPE_ALPHA_B)
        sd.rectangle([bw_left, y, bw_right, y_end], fill=col)
        y += STRIPE_HEIGHT
        stripe_idx += 1

    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, stripe_overlay)
    img = img_rgba.convert("RGB")

    # Left wall stripes
    lw_poly = [
        (0, int(H * 0.22)),
        (bw_left, bw_top),
        (bw_left, bw_bot),
        (0, int(H * 0.88)),
    ]
    lw_top_y = int(H * 0.22)
    lw_bot_y = bw_top + int(wall_height * 0.50)

    lw_stripe_full = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    lf = ImageDraw.Draw(lw_stripe_full)
    y = lw_top_y
    stripe_idx = 0
    while y < lw_bot_y:
        y_end = min(y + STRIPE_HEIGHT, lw_bot_y)
        col = (*STRIPE_A, SIDE_ALPHA_A) if stripe_idx % 2 == 0 else (*STRIPE_B, SIDE_ALPHA_B)
        lf.rectangle([0, y, bw_left, y_end], fill=col)
        y += STRIPE_HEIGHT
        stripe_idx += 1

    lw_mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(lw_mask).polygon(lw_poly, fill=255)
    lw_stripe_masked = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    lw_stripe_masked.paste(lw_stripe_full, mask=lw_mask)
    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, lw_stripe_masked)
    img = img_rgba.convert("RGB")

    # Right wall stripes
    rw_poly = [
        (bw_right, bw_top),
        (W, vp_y - 40),
        (W, int(H * 0.82)),
        (bw_right, bw_bot),
    ]
    rw_top_y = vp_y - 40
    rw_bot_y = bw_top + int(wall_height * 0.50)

    rw_stripe_full = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    rf = ImageDraw.Draw(rw_stripe_full)
    y = min(rw_top_y, bw_top)
    stripe_idx = 0
    while y < rw_bot_y:
        y_end = min(y + STRIPE_HEIGHT, rw_bot_y)
        col = (*STRIPE_A, SIDE_ALPHA_A) if stripe_idx % 2 == 0 else (*STRIPE_B, SIDE_ALPHA_B)
        rf.rectangle([bw_right, y, W, y_end], fill=col)
        y += STRIPE_HEIGHT
        stripe_idx += 1

    rw_mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(rw_mask).polygon(rw_poly, fill=255)
    rw_stripe_masked = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    rw_stripe_masked.paste(rw_stripe_full, mask=rw_mask)
    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, rw_stripe_masked)
    return img_rgba.convert("RGB")


# ── Layer 8: Kitchen Cabinets & Appliances ────────────────────────────────────

def draw_cabinets_and_appliances(draw, bw_left, bw_top, bw_right, bw_bot):
    """
    Upper and lower kitchen cabinets.
    Old-fashioned appliances — no screens, no digital displays.
    """
    cab_bottom = bw_top + int((bw_bot - bw_top) * 0.42)
    cab_top    = bw_top + int((bw_bot - bw_top) * 0.05)

    # v008: VP for cabinet side reveals
    VP_X_CAB, VP_Y_CAB = int(W * 0.40), int(H * 0.38)
    CAB_SIDE_REVEAL = 3  # depth face width in px (P2 item)

    upper_cab_specs = [
        (0.58, 0.70),
        (0.70, 0.83),
        (0.83, 0.96),
    ]
    for (x1f, x2f) in upper_cab_specs:
        cx1 = int(bw_left + (bw_right - bw_left) * x1f)
        cx2 = int(bw_left + (bw_right - bw_left) * x2f)
        draw.rectangle([cx1, cab_top, cx2, cab_bottom], fill=WOOD_DARK)
        draw.rectangle([cx1, cab_top, cx2, cab_bottom], outline=LINE_DARK, width=2)
        # v008: Side depth reveal on VP-facing edge (VP is left of cabinets)
        cab_center_x = (cx1 + cx2) // 2
        if VP_X_CAB < cab_center_x:
            # VP is left — depth face on left edge
            side_pts = [
                (cx1, cab_top), (cx1 - CAB_SIDE_REVEAL, cab_top + 1),
                (cx1 - CAB_SIDE_REVEAL, cab_bottom - 1), (cx1, cab_bottom),
            ]
        else:
            # VP is right — depth face on right edge
            side_pts = [
                (cx2, cab_top), (cx2 + CAB_SIDE_REVEAL, cab_top + 1),
                (cx2 + CAB_SIDE_REVEAL, cab_bottom - 1), (cx2, cab_bottom),
            ]
        draw.polygon(side_pts, fill=lerp_color(WOOD_DARK, SHADOW_DEEP, 0.5))
        # Cabinet door panel inset
        inset = 4
        draw.rectangle([cx1 + inset, cab_top + inset,
                         cx2 - inset, cab_bottom - inset],
                        outline=lerp_color(WOOD_DARK, WOOD_MED, 0.5), width=1)
        # Handle
        hx = (cx1 + cx2) // 2
        hy = cab_bottom - 10
        draw.rectangle([hx - 5, hy, hx + 5, hy + 3], fill=FRIDGE_TRIM)

    # Countertop — v008: VP-convergent trapezoid top surface
    counter_y1 = bw_top + int((bw_bot - bw_top) * 0.52)
    counter_y2 = counter_y1 + int((bw_bot - bw_top) * 0.08)
    ct_x1 = bw_left + int((bw_right - bw_left) * 0.38)
    ct_x2 = bw_right
    ct_w = ct_x2 - ct_x1
    ct_conv = max(0.0, min(1.0, (VP_Y_CAB - counter_y1) / H))
    ct_shrink = int(ct_w * ct_conv * 0.15)
    ct_top_pts = [
        (ct_x1 + ct_shrink, counter_y1),   # top-left (far, shrunk)
        (ct_x2 - ct_shrink, counter_y1),   # top-right (far, shrunk)
        (ct_x2, counter_y2),                # bot-right (near, full)
        (ct_x1, counter_y2),                # bot-left (near, full)
    ]
    draw.polygon(ct_top_pts, fill=COUNTERTOP)
    draw.line([(ct_x1 + ct_shrink, counter_y1), (ct_x2 - ct_shrink, counter_y1)],
              fill=COUNTER_EDGE, width=2)
    draw.polygon(ct_top_pts, outline=LINE_DARK, width=1)
    # v008: Front face of countertop (visible depth)
    ct_front_depth = 4
    ct_front_pts = [
        (ct_x1, counter_y2), (ct_x2, counter_y2),
        (ct_x2, counter_y2 + ct_front_depth), (ct_x1, counter_y2 + ct_front_depth),
    ]
    draw.polygon(ct_front_pts, fill=COUNTER_EDGE)
    draw.polygon(ct_front_pts, outline=LINE_DARK, width=1)

    # Lower cabinets — v008: with side depth reveal
    lower_y1 = counter_y2 + ct_front_depth
    lower_y2 = bw_bot
    for ci in range(4):
        lc_x1 = ct_x1 + int(ci * (ct_x2 - ct_x1) / 4)
        lc_x2 = ct_x1 + int((ci + 1) * (ct_x2 - ct_x1) / 4)
        draw.rectangle([lc_x1, lower_y1, lc_x2, lower_y2], fill=WOOD_DARK)
        draw.rectangle([lc_x1, lower_y1, lc_x2, lower_y2], outline=LINE_DARK, width=1)
        # v008: Side depth reveal on VP-facing (left) edge for leftmost cabinet
        if ci == 0:
            lc_side_pts = [
                (lc_x1, lower_y1), (lc_x1 - CAB_SIDE_REVEAL, lower_y1 + 1),
                (lc_x1 - CAB_SIDE_REVEAL, lower_y2 - 1), (lc_x1, lower_y2),
            ]
            draw.polygon(lc_side_pts, fill=lerp_color(WOOD_DARK, SHADOW_DEEP, 0.5))
        inset = 4
        draw.rectangle([lc_x1 + inset, lower_y1 + inset,
                         lc_x2 - inset, lower_y2 - inset],
                        outline=lerp_color(WOOD_DARK, WOOD_MED, 0.4), width=1)
        hx = (lc_x1 + lc_x2) // 2
        hy = lower_y1 + int((lower_y2 - lower_y1) * 0.45)
        draw.rectangle([hx - 6, hy, hx + 6, hy + 3], fill=FRIDGE_TRIM)

    # Gas stove
    stove_x1 = int(bw_left + (bw_right - bw_left) * 0.54)
    stove_x2 = int(bw_left + (bw_right - bw_left) * 0.72)
    stove_y1 = counter_y1 - 2
    stove_y2 = counter_y2
    draw.rectangle([stove_x1, stove_y1, stove_x2, stove_y2], fill=STOVE_CREAM)
    draw.rectangle([stove_x1, stove_y1, stove_x2, stove_y2], outline=LINE_DARK, width=1)

    burner_positions = [
        (stove_x1 + int((stove_x2 - stove_x1) * 0.25), stove_y1 + int((stove_y2 - stove_y1) * 0.3)),
        (stove_x1 + int((stove_x2 - stove_x1) * 0.75), stove_y1 + int((stove_y2 - stove_y1) * 0.3)),
        (stove_x1 + int((stove_x2 - stove_x1) * 0.25), stove_y1 + int((stove_y2 - stove_y1) * 0.72)),
        (stove_x1 + int((stove_x2 - stove_x1) * 0.75), stove_y1 + int((stove_y2 - stove_y1) * 0.72)),
    ]
    burner_r = max(4, int((stove_x2 - stove_x1) * 0.11))
    for (bx, by) in burner_positions:
        draw.ellipse([bx - burner_r, by - burner_r // 2,
                      bx + burner_r, by + burner_r // 2], fill=STOVE_IRON)
        inner_r = max(2, burner_r - 3)
        draw.ellipse([bx - inner_r, by - inner_r // 2,
                      bx + inner_r, by + inner_r // 2],
                     outline=lerp_color(STOVE_IRON, WOOD_DARK, 0.4), width=1)

    knob_y = stove_y1 + 4
    for ki in range(4):
        kx = stove_x1 + int((ki + 0.5) * (stove_x2 - stove_x1) / 4)
        draw.ellipse([kx - 4, knob_y, kx + 4, knob_y + 7], fill=STOVE_KNOB)

    # v004: Handwritten calendar on wall near stove (Miri-specific)
    cal_x = stove_x2 + 4
    cal_y = cab_top + int((cab_bottom - cab_top) * 0.05)
    cal_w = int((bw_right - stove_x2) * 0.60)
    cal_h = int((cab_bottom - cab_top) * 0.70)
    if cal_x + cal_w < bw_right:
        draw.rectangle([cal_x, cal_y, cal_x + cal_w, cal_y + cal_h],
                       fill=(242, 236, 218))
        draw.rectangle([cal_x, cal_y, cal_x + cal_w, cal_y + cal_h],
                       outline=LINE_DARK, width=1)
        # Calendar header
        draw.rectangle([cal_x, cal_y, cal_x + cal_w, cal_y + max(3, cal_h // 5)],
                       fill=(200, 64, 48))   # warm red calendar header
        # Grid lines for dates (small)
        cell_w = max(2, cal_w // 7)
        cell_h = max(2, cal_h // 6)
        for row in range(1, 5):
            ry = cal_y + cal_h // 5 + row * cell_h
            draw.line([(cal_x, ry), (cal_x + cal_w, ry)],
                      fill=lerp_color(AGED_CREAM, LINE_DARK, 0.3), width=1)
        for col in range(1, 7):
            cx_cal = cal_x + col * cell_w
            draw.line([(cx_cal, cal_y + cal_h // 5), (cx_cal, cal_y + cal_h)],
                      fill=lerp_color(AGED_CREAM, LINE_DARK, 0.3), width=1)

    return counter_y1, counter_y2


# ── Layer 9: Sink ──────────────────────────────────────────────────────────────

def draw_sink(draw, bw_left, bw_top, bw_right, bw_bot, win_x1, win_x2, win_y2):
    """
    Porcelain sink below window. Faucet. Windowsill plant.
    v004: Medicine/supplement bottle on counter (Miri-specific detail).
    """
    sink_x1 = int(bw_left + (bw_right - bw_left) * 0.33)
    sink_x2 = int(bw_left + (bw_right - bw_left) * 0.56)
    counter_y = bw_top + int((bw_bot - bw_top) * 0.52)
    sink_y1 = win_y2 + 4
    sink_y2 = counter_y

    # Counter around sink
    draw.rectangle([sink_x1 - 8, sink_y1, sink_x2 + 8, sink_y2], fill=COUNTERTOP)
    draw.line([(sink_x1 - 8, sink_y1), (sink_x2 + 8, sink_y1)],
              fill=COUNTER_EDGE, width=2)

    # Sink basin
    basin_inset = max(5, int((sink_x2 - sink_x1) * 0.08))
    draw.rectangle([sink_x1 + basin_inset, sink_y1 + basin_inset,
                    sink_x2 - basin_inset, sink_y2 - 3], fill=SINK_PORCELAIN)
    draw.rectangle([sink_x1 + basin_inset, sink_y1 + basin_inset,
                    sink_x2 - basin_inset, sink_y2 - 3],
                   outline=lerp_color(SINK_PORCELAIN, SHADOW_MID, 0.5), width=1)

    # Drain
    drain_cx = (sink_x1 + sink_x2) // 2
    drain_cy = sink_y2 - 7
    draw.ellipse([drain_cx - 5, drain_cy - 3, drain_cx + 5, drain_cy + 3],
                 fill=lerp_color(SINK_PORCELAIN, LINE_DARK, 0.6))

    # Faucet
    faucet_x = drain_cx
    faucet_y = sink_y1 + 2
    draw.rectangle([faucet_x - 3, faucet_y, faucet_x + 3, faucet_y + 10],
                   fill=FRIDGE_TRIM)
    draw.ellipse([faucet_x - 7, faucet_y - 3, faucet_x + 7, faucet_y + 3],
                 fill=FRIDGE_TRIM)
    for side in [-1, 1]:
        hx = faucet_x + side * 12
        hy = faucet_y + 2
        draw.ellipse([hx - 4, hy - 3, hx + 4, hy + 3], fill=FRIDGE_TRIM)

    # Dish rack
    rack_x = sink_x2 + 10
    rack_y = sink_y1 + 4
    rack_w = int(W * 0.05)
    rack_h = int((sink_y2 - sink_y1) * 0.8)
    draw.rectangle([rack_x, rack_y, rack_x + rack_w, rack_y + rack_h],
                   outline=LINE_DARK, width=1)
    for di in range(3):
        dish_x = rack_x + 3 + di * 10
        draw.rectangle([dish_x, rack_y + 3, dish_x + 7, rack_y + rack_h - 3],
                       fill=DISH_WHITE)
        draw.rectangle([dish_x, rack_y + 3, dish_x + 7, rack_y + rack_h - 3],
                       outline=DISH_BLUE_RING, width=1)

    # Windowsill plant
    plant_x = win_x1 - 18
    plant_y = win_y2 - 4
    draw.rectangle([plant_x, plant_y - 10, plant_x + 16, plant_y + 7],
                   fill=lerp_color(WOOD_MED, COUNTERTOP, 0.3))
    draw.ellipse([plant_x - 4, plant_y - 20, plant_x + 20, plant_y - 2],
                 fill=PLANT_GREEN)
    draw.ellipse([plant_x, plant_y - 16, plant_x + 12, plant_y - 6],
                 fill=lerp_color(PLANT_GREEN, PLANT_DARK, 0.4))

    # v004: Medicine bottles on counter near sink (Miri-specific detail — elderly grandmother)
    med_rng = random.Random(91)
    for bi in range(3):
        bx = sink_x1 - 8 - (bi + 1) * 14
        if bx < bw_left:
            break
        bh = max(10, int((sink_y2 - sink_y1) * med_rng.uniform(0.5, 0.9)))
        bw_bottle = max(5, int(W * 0.012))
        bottle_col = med_rng.choice([
            (198, 168, 108),  # amber bottle
            (220, 210, 190),  # white bottle
            (188, 148,  90),  # brown bottle
        ])
        by = sink_y1 + (sink_y2 - sink_y1 - bh)
        draw.rectangle([bx, by, bx + bw_bottle, by + bh], fill=bottle_col)
        draw.rectangle([bx, by, bx + bw_bottle, by + bh], outline=LINE_DARK, width=1)
        # Label
        draw.rectangle([bx + 1, by + bh // 3, bx + bw_bottle - 1, by + 2 * bh // 3],
                       fill=(230, 220, 200))


# ── Layer 10: Kitchen Table ────────────────────────────────────────────────────

def draw_kitchen_table(draw, img, bw_bot):
    """
    Kitchen table in foreground-left. Morning: crossword, Miri's rose-pattern mug, toast.
    v004: Miri-specific mug (rose pattern on earthenware), knitting bag on chair.
    v008: VP-convergent trapezoid table surface (docs/perspective-rules.md).
    """
    # Table position
    tbl_x1 = int(W * 0.02)
    tbl_x2 = int(W * 0.42)
    tbl_y1 = int(H * 0.64)
    tbl_y2 = int(H * 0.72)

    # v008: VP convergence for table surface
    VP_X, VP_Y = int(W * 0.40), int(H * 0.38)
    tbl_w = tbl_x2 - tbl_x1
    convergence = max(0.0, min(1.0, (VP_Y - tbl_y1) / H))
    shrink = int(tbl_w * convergence * 0.15)

    # Table top surface as VP-convergent trapezoid
    # Far edge (tbl_y1) is shorter (shrunk), near edge (tbl_y2) is full width
    tbl_top_pts = [
        (tbl_x1 + shrink, tbl_y1),       # top-left (far, shrunk)
        (tbl_x2 - shrink, tbl_y1),        # top-right (far, shrunk)
        (tbl_x2, tbl_y2),                  # bot-right (near, full)
        (tbl_x1, tbl_y2),                  # bot-left (near, full)
    ]
    draw.polygon(tbl_top_pts, fill=WOOD_WORN)
    # Front edge highlight
    draw.line([(tbl_x1 + shrink, tbl_y1), (tbl_x2 - shrink, tbl_y1)],
              fill=WOOD_LIGHT, width=2)
    draw.polygon(tbl_top_pts, outline=LINE_DARK, width=2)

    # v008: Front face of table (visible depth face — near edge thickness)
    front_depth = 6
    front_face_pts = [
        (tbl_x1, tbl_y2),
        (tbl_x2, tbl_y2),
        (tbl_x2, tbl_y2 + front_depth),
        (tbl_x1, tbl_y2 + front_depth),
    ]
    draw.polygon(front_face_pts, fill=WOOD_DARK)
    draw.polygon(front_face_pts, outline=LINE_DARK, width=1)

    # Wood grain — drawn within trapezoid area
    grain_rng = random.Random(71)
    for gi in range(6):
        gy = tbl_y1 + grain_rng.randint(2, tbl_y2 - tbl_y1 - 2)
        # Interpolate trapezoid width at this y
        t = (gy - tbl_y1) / max(1, tbl_y2 - tbl_y1)
        row_x1 = int(tbl_x1 + shrink * (1 - t))
        row_x2 = int(tbl_x2 - shrink * (1 - t))
        gw_start = row_x1 + grain_rng.randint(0, int((row_x2 - row_x1) * 0.3))
        gw_end = row_x2 - grain_rng.randint(0, int((row_x2 - row_x1) * 0.3))
        draw.line([(gw_start, gy), (gw_end, gy)],
                  fill=lerp_color(WOOD_WORN, WOOD_DARK, 0.25), width=1)

    # Table legs — converge slightly toward VP
    leg_h = int(H * 0.22)
    leg_near_left = tbl_x1 + 12
    leg_near_right = tbl_x2 - 20
    for lx in [leg_near_left, leg_near_right]:
        # Legs angle slightly inward toward VP direction
        leg_top_x = lx
        leg_bot_x = lx + int((VP_X - lx) * 0.02)  # subtle lean toward VP
        leg_pts = [
            (leg_top_x, tbl_y2 + front_depth),
            (leg_top_x + 12, tbl_y2 + front_depth),
            (leg_bot_x + 12, min(H, tbl_y2 + front_depth + leg_h)),
            (leg_bot_x, min(H, tbl_y2 + front_depth + leg_h)),
        ]
        draw.polygon(leg_pts, fill=WOOD_MED)
        draw.polygon(leg_pts, outline=LINE_DARK, width=1)

    # Table underside shadow (v004: deep shadow band below table)
    shadow_overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    so = ImageDraw.Draw(shadow_overlay)
    for y in range(tbl_y2, min(H, tbl_y2 + int(H * 0.05))):
        t = 1.0 - (y - tbl_y2) / (H * 0.05)
        alpha = int(t ** 0.8 * 180)
        so.line([(tbl_x1, y), (tbl_x2, y)], fill=(*NEAR_BLACK_WARM, alpha))
    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, shadow_overlay)
    img = img_rgba.convert("RGB")
    draw = ImageDraw.Draw(img)

    # Crossword puzzle
    cw_x = int(W * 0.08)
    cw_y = tbl_y1 + 4
    cw_w = int(W * 0.12)
    cw_h = int((tbl_y2 - tbl_y1) * 0.75)
    draw.rectangle([cw_x, cw_y, cw_x + cw_w, cw_y + cw_h], fill=(238, 230, 208))
    draw.rectangle([cw_x, cw_y, cw_x + cw_w, cw_y + cw_h], outline=LINE_DARK, width=1)
    cell_s = max(3, cw_w // 10)
    cg_x = cw_x + 3
    cg_y = cw_y + int(cw_h * 0.25)
    for ri in range(6):
        for ci in range(8):
            cx_cell = cg_x + ci * cell_s
            cy_cell = cg_y + ri * cell_s
            if (ri + ci) % 3 == 0:
                draw.rectangle([cx_cell, cy_cell, cx_cell + cell_s, cy_cell + cell_s],
                               fill=LINE_DARK)
            draw.rectangle([cx_cell, cy_cell, cx_cell + cell_s, cy_cell + cell_s],
                           outline=(196, 188, 168), width=1)

    # Pencil
    pen_x = cw_x + cw_w + 5
    pen_y = cw_y + int(cw_h * 0.4)
    draw.rectangle([pen_x, pen_y, pen_x + 4, pen_y + cw_h // 2], fill=(218, 186, 78))
    draw.rectangle([pen_x, pen_y, pen_x + 4, pen_y + cw_h // 2], outline=LINE_DARK, width=1)
    draw.polygon([(pen_x, pen_y + cw_h // 2), (pen_x + 4, pen_y + cw_h // 2),
                  (pen_x + 2, pen_y + cw_h // 2 + 5)], fill=(198, 164, 58))

    # v004: Miri's rose-pattern mug (character-specific)
    mug_x = cw_x + cw_w + 22
    mug_y = tbl_y1 + 3
    mug_w = max(12, int(W * 0.020))
    mug_h = int((tbl_y2 - tbl_y1) * 0.65)
    # Mug body (earthenware, warm)
    draw.rectangle([mug_x, mug_y, mug_x + mug_w, mug_y + mug_h], fill=MUG_EARTHY)
    draw.rectangle([mug_x, mug_y, mug_x + mug_w, mug_y + mug_h], outline=LINE_DARK, width=1)
    # Rose pattern — tiny red dot + green leaf (simplified)
    rose_cx = mug_x + mug_w // 2
    rose_cy = mug_y + mug_h // 2
    draw.ellipse([rose_cx - 3, rose_cy - 3, rose_cx + 3, rose_cy + 3],
                 fill=(180, 50, 38))   # rose red
    draw.ellipse([rose_cx + 2, rose_cy + 1, rose_cx + 5, rose_cy + 4],
                 fill=PLANT_GREEN)    # leaf
    # Mug handle
    draw.arc([mug_x + mug_w, mug_y + mug_h // 4,
              mug_x + mug_w + mug_w // 2, mug_y + 3 * mug_h // 4],
             start=270, end=90, fill=MUG_EARTHY, width=2)
    # Steam
    steam_rng = random.Random(77)
    for si in range(3):
        sx = mug_x + mug_w // 4 + si * (mug_w // 3)
        draw.line([(sx, mug_y - 2), (sx + steam_rng.randint(-2, 2), mug_y - 9)],
                  fill=lerp_color(WALL_WARM, CEILING_WARM, 0.5), width=1)

    # Toast plate
    plate_x = int(W * 0.26)
    plate_y = tbl_y1 + 5
    plate_r_x = int(W * 0.035)
    plate_r_y = int((tbl_y2 - tbl_y1) * 0.30)
    draw.ellipse([plate_x - plate_r_x, plate_y,
                  plate_x + plate_r_x, plate_y + plate_r_y * 2], fill=DISH_WHITE)
    draw.ellipse([plate_x - plate_r_x, plate_y,
                  plate_x + plate_r_x, plate_y + plate_r_y * 2],
                 outline=DISH_BLUE_RING, width=1)
    toast_w = int(plate_r_x * 1.2)
    toast_h = int(plate_r_y * 0.9)
    draw.rectangle([plate_x - toast_w // 2, plate_y + 2,
                    plate_x + toast_w // 2, plate_y + 2 + toast_h], fill=BREAD_WARM)
    draw.rectangle([plate_x - toast_w // 2, plate_y + 2,
                    plate_x + toast_w // 2, plate_y + 2 + toast_h],
                   outline=lerp_color(BREAD_WARM, LINE_DARK, 0.5), width=1)

    # Chair visible at table edge — v008: VP-convergent
    chair_x = tbl_x1 + int((tbl_x2 - tbl_x1) * 0.25)
    chair_y = tbl_y2 + front_depth + 7
    chair_w = int(W * 0.09)
    chair_h = 65
    chair_bot = min(H, chair_y + chair_h)
    # Chair back (trapezoid — far edge shorter)
    ch_conv = max(0.0, min(1.0, (VP_Y - chair_y) / H))
    ch_shrink = int(chair_w * ch_conv * 0.12)
    chair_pts = [
        (chair_x + ch_shrink, chair_y),           # top-left (far)
        (chair_x + chair_w - ch_shrink, chair_y),  # top-right (far)
        (chair_x + chair_w, chair_bot),             # bot-right (near)
        (chair_x, chair_bot),                       # bot-left (near)
    ]
    draw.polygon(chair_pts, fill=WOOD_MED)
    draw.polygon(chair_pts, outline=LINE_DARK, width=1)

    # v004: Knitting bag on chair (Miri character detail)
    kb_x = chair_x + 4
    kb_y = min(H - 20, chair_y + 25)
    kb_w = int(chair_w * 0.55)
    kb_h = int(H * 0.06)
    draw.ellipse([kb_x, kb_y, kb_x + kb_w, kb_y + kb_h],
                 fill=(158, 120, 80))    # woven bag, warm brown
    draw.ellipse([kb_x, kb_y, kb_x + kb_w, kb_y + kb_h],
                 outline=LINE_DARK, width=1)
    # Yarn poking out (small colored loop)
    draw.ellipse([kb_x + kb_w // 3, kb_y - 4, kb_x + kb_w // 3 + 6, kb_y + 2],
                 outline=(180, 60, 40), width=2)    # warm red yarn

    return img


# ── Layer 11: Countertop Plant ────────────────────────────────────────────────

def draw_kitchen_plant(draw, bw_left, bw_top, bw_right, bw_bot):
    """Small potted plant on the countertop. Adds warmth and life."""
    counter_y = bw_top + int((bw_bot - bw_top) * 0.50)
    plant_x = int(bw_left + (bw_right - bw_left) * 0.80)
    plant_y = counter_y - 2

    pot_w = int(W * 0.018)
    pot_h = int((bw_bot - bw_top) * 0.10)

    draw.polygon([
        (plant_x - pot_w // 2 + 2, plant_y - pot_h),
        (plant_x + pot_w // 2 - 2, plant_y - pot_h),
        (plant_x + pot_w // 2, plant_y),
        (plant_x - pot_w // 2, plant_y),
    ], fill=(182, 78, 46))
    draw.polygon([
        (plant_x - pot_w // 2 + 2, plant_y - pot_h),
        (plant_x + pot_w // 2 - 2, plant_y - pot_h),
        (plant_x + pot_w // 2, plant_y),
        (plant_x - pot_w // 2, plant_y),
    ], outline=LINE_DARK)
    draw.rectangle([plant_x - pot_w // 2, plant_y - pot_h - 3,
                    plant_x + pot_w // 2, plant_y - pot_h + 3],
                   fill=(190, 90, 58))

    for li in range(3):
        angle = math.radians(-40 + li * 40)
        leaf_x = plant_x + int(math.cos(angle) * 10)
        leaf_y = plant_y - pot_h - 8 + int(abs(math.sin(angle)) * 6)
        leaf_r = max(6, pot_w // 2)
        draw.ellipse([leaf_x - leaf_r, leaf_y - leaf_r,
                      leaf_x + leaf_r, leaf_y + leaf_r],
                     fill=PLANT_GREEN if li != 1 else lerp_color(PLANT_GREEN, PLANT_DARK, 0.4))


# ── Layer 12: Refrigerator ────────────────────────────────────────────────────

def draw_refrigerator(img, draw, bw_right, bw_top, bw_bot):
    """
    Old refrigerator on right side.
    v004: Travel-destination fridge magnets (Miri is world-experienced).
    v008: VP-convergent fridge body with visible side face (P1).
    """
    VP_X_F, VP_Y_F = int(W * 0.40), int(H * 0.38)
    fridge_w = int(W * 0.09)
    fridge_x1 = bw_right - int((bw_right - int(W * 0.1)) * 0.07)
    fridge_x2 = fridge_x1 + fridge_w
    fridge_y1 = bw_top + int((bw_bot - bw_top) * 0.04)
    fridge_y2 = bw_bot

    # v008: VP convergence — front face foreshortens toward VP
    fr_conv = max(0.0, min(1.0, (VP_Y_F - fridge_y1) / H))
    fr_shrink = int(fridge_w * fr_conv * 0.12)

    # Front face as trapezoid (top edge shorter — closer to VP height)
    fr_front_pts = [
        (fridge_x1 + fr_shrink, fridge_y1),   # top-left (far, shrunk)
        (fridge_x2 - fr_shrink, fridge_y1),    # top-right (far, shrunk)
        (fridge_x2, fridge_y2),                 # bot-right (near, full)
        (fridge_x1, fridge_y2),                 # bot-left (near, full)
    ]
    draw.polygon(fr_front_pts, fill=FRIDGE_WHITE)
    draw.polygon(fr_front_pts, outline=LINE_DARK, width=2)

    # v008: Side face visible on left (VP is left — fridge is right of VP)
    side_face_w = 5  # depth face width
    side_color = lerp_color(FRIDGE_WHITE, FRIDGE_TRIM, 0.4)
    side_pts = [
        (fridge_x1 + fr_shrink, fridge_y1),
        (fridge_x1 + fr_shrink - side_face_w, fridge_y1 + 2),
        (fridge_x1 - side_face_w, fridge_y2 - 2),
        (fridge_x1, fridge_y2),
    ]
    draw.polygon(side_pts, fill=side_color)
    draw.polygon(side_pts, outline=LINE_DARK, width=1)

    # Freezer/fridge divider — interpolate within trapezoid
    div_y = fridge_y1 + int((fridge_y2 - fridge_y1) * 0.22)
    div_t = (div_y - fridge_y1) / max(1, fridge_y2 - fridge_y1)
    div_x1 = int(fridge_x1 + fr_shrink * (1 - div_t))
    div_x2 = int(fridge_x2 - fr_shrink * (1 - div_t))
    draw.line([(div_x1, div_y), (div_x2, div_y)], fill=LINE_DARK, width=2)

    # Handles — positioned within converging front face
    for hy in [fridge_y1 + int((div_y - fridge_y1) * 0.45),
               div_y + int((fridge_y2 - div_y) * 0.35)]:
        h_t = (hy - fridge_y1) / max(1, fridge_y2 - fridge_y1)
        hx_base = int(fridge_x1 + fr_shrink * (1 - h_t))
        hx = hx_base + int(fridge_w * 0.15)
        draw.rectangle([hx, hy, hx + 7, hy + 17], fill=FRIDGE_TRIM)
        draw.rectangle([hx, hy, hx + 7, hy + 17], outline=LINE_DARK, width=1)

    # Door panel insets — within converging front face
    for door_y1, door_y2 in [(fridge_y1, div_y), (div_y, fridge_y2)]:
        inset = 6
        d1_t = (door_y1 + inset - fridge_y1) / max(1, fridge_y2 - fridge_y1)
        d2_t = (door_y2 - inset - fridge_y1) / max(1, fridge_y2 - fridge_y1)
        dx1_top = int(fridge_x1 + fr_shrink * (1 - d1_t)) + inset
        dx2_top = int(fridge_x2 - fr_shrink * (1 - d1_t)) - inset
        dx1_bot = int(fridge_x1 + fr_shrink * (1 - d2_t)) + inset
        dx2_bot = int(fridge_x2 - fr_shrink * (1 - d2_t)) - inset
        panel_pts = [
            (dx1_top, door_y1 + inset), (dx2_top, door_y1 + inset),
            (dx2_bot, door_y2 - inset), (dx1_bot, door_y2 - inset),
        ]
        draw.polygon(panel_pts, outline=lerp_color(FRIDGE_WHITE, FRIDGE_TRIM, 0.5), width=1)

    # v004: Travel-destination fridge magnets (Miri sees the world — her curiosity is established)
    magnet_rng = random.Random(83)
    magnet_colors = [
        (200,  60,  40),  # Tokyo / Japan red
        ( 30, 100, 180),  # Portugal blue
        (220, 170,  40),  # Morocco gold
        ( 50, 130,  80),  # Ireland green
        (180,  80, 140),  # Paris lavender
    ]
    for mi in range(5):
        mx = fridge_x1 + magnet_rng.randint(8, max(9, int(fridge_w * 0.65)))
        my = div_y + magnet_rng.randint(15, int((fridge_y2 - div_y) * 0.55))
        mc = magnet_colors[mi % len(magnet_colors)]
        draw.rectangle([mx, my, mx + 9, my + 7], fill=mc)
        draw.rectangle([mx, my, mx + 9, my + 7], outline=LINE_DARK, width=1)

    # Return fridge geometry for v005 MIRI label placement
    return fridge_x1, fridge_x2, fridge_y1, fridge_y2, div_y


# ── Layer 12b: MIRI Fridge Label — Dual-Miri Visual Plant (v005 NEW) ──────────

def draw_miri_fridge_label(draw, fridge_x1, fridge_x2, fridge_y1, fridge_y2, div_y):
    """
    v005 NEW — Dual-Miri visual plant (Alex Chen directive, C39).

    Adds a small handwritten "MIRI" label on a scrap of paper on the fridge door.
    Placed right-center of fridge lower door body, near the travel magnets.

    Spec:
    - Real World palette ONLY. No GL colors.
    - Paper: AGED_CREAM (238,226,198) rectangle — reads as any domestic label/note
    - Ink: LINE_DARK (88,60,32) — warm dark brown, natural handwritten look
    - Small magnet pip above paper: warm amber circle (anchors the paper visually)
    - Must be legible in full-resolution PNG; easy to miss at thumbnail scale
    - No raised eyebrows at first watch — it's just Grandma's name, people label things

    Layout (computed from fridge constants):
      fridge_w = int(W*0.09) ~= 115px
      fridge_x1 ~= 866, fridge_x2 ~= 981
      div_y ~= 352 (freezer / main compartment divider)
      fridge_y2 ~= 590

      Paper placed at right-center of lower door:
        lbl_x1 = fridge_x1 + int(fridge_w * 0.35)  ~= 906
        lbl_y1 = div_y + int((fridge_y2 - div_y) * 0.46)  ~= 492
        paper is 40px wide x 16px tall
        "MIRI" drawn pixel-line style centered on paper

    Returns (lbl_x1, lbl_y1) for completion report.
    """
    fridge_w = fridge_x2 - fridge_x1

    # Paper position: right-center of lower fridge door, near magnets
    lbl_x1 = fridge_x1 + int(fridge_w * 0.35)
    lbl_y1 = div_y + int((fridge_y2 - div_y) * 0.46)
    lbl_w  = 40
    lbl_h  = 16

    lbl_x2 = lbl_x1 + lbl_w
    lbl_y2 = lbl_y1 + lbl_h

    # Paper background (cream scrap)
    PAPER_CREAM  = (238, 226, 198)   # AGED_CREAM — Real World only
    INK_DARK     = ( 88,  60,  32)   # LINE_DARK
    MAGNET_PIP   = (210, 155,  50)   # warm amber small magnet — no GL pigments

    draw.rectangle([lbl_x1, lbl_y1, lbl_x2, lbl_y2], fill=PAPER_CREAM)
    draw.rectangle([lbl_x1, lbl_y1, lbl_x2, lbl_y2], outline=INK_DARK, width=1)

    # Small magnet pip holding paper at top-center
    pip_cx = (lbl_x1 + lbl_x2) // 2
    pip_cy = lbl_y1 - 4
    draw.ellipse([pip_cx - 3, pip_cy - 3, pip_cx + 3, pip_cy + 3], fill=MAGNET_PIP)
    draw.ellipse([pip_cx - 3, pip_cy - 3, pip_cx + 3, pip_cy + 3],
                 outline=INK_DARK, width=1)

    # "MIRI" via canonical draw_pixel_text() — scale=1 (5×7 glyph, 7px tall)
    # measure_pixel_text("MIRI", scale=1) → width = (4*6 - 1)*1 = 23px, height = 7px
    from LTG_TOOL_pixel_font_v001 import measure_pixel_text
    txt_w, txt_h = measure_pixel_text("MIRI", scale=1)
    txt_x0 = lbl_x1 + (lbl_w - txt_w) // 2   # horizontally centered
    txt_y0 = lbl_y1 + (lbl_h - txt_h) // 2 + 1  # vertically centered
    draw_pixel_text(draw, txt_x0, txt_y0, "MIRI", INK_DARK, scale=1)

    return lbl_x1, lbl_y1, lbl_x2, lbl_y2


# ── Layer 13: Warm Apron on Peg (Miri detail) ─────────────────────────────────

def draw_apron_on_peg(draw, bw_left, bw_top, bw_bot):
    """
    v004 Miri-specific detail: Worn apron hanging on a peg near doorway.
    The peg is on the left wall near the doorway.
    """
    # Peg position: near doorway on left wall
    peg_x = int(bw_left * 0.55)
    peg_y = bw_top + int((bw_bot - bw_top) * 0.18)

    # Peg (wooden bracket)
    draw.rectangle([peg_x - 2, peg_y, peg_x + 12, peg_y + 4], fill=WOOD_MED)
    draw.ellipse([peg_x + 9, peg_y - 3, peg_x + 15, peg_y + 7], fill=WOOD_DARK)

    # Apron (flower-print fabric, hung over peg)
    apron_cx = peg_x + 6
    apron_y1 = peg_y + 6
    apron_w = int(bw_left * 0.45)
    apron_h = int((bw_bot - bw_top) * 0.28)

    # Apron body
    draw.rectangle([apron_cx - apron_w // 2, apron_y1,
                    apron_cx + apron_w // 2, apron_y1 + apron_h],
                   fill=(220, 195, 148))   # worn cream fabric
    draw.rectangle([apron_cx - apron_w // 2, apron_y1,
                    apron_cx + apron_w // 2, apron_y1 + apron_h],
                   outline=LINE_DARK, width=1)
    # Apron pocket
    pk_x = apron_cx - apron_w // 4
    pk_y = apron_y1 + int(apron_h * 0.45)
    pk_w = int(apron_w * 0.35)
    pk_h = int(apron_h * 0.28)
    draw.rectangle([pk_x, pk_y, pk_x + pk_w, pk_y + pk_h],
                   fill=(210, 182, 132))
    draw.rectangle([pk_x, pk_y, pk_x + pk_w, pk_y + pk_h], outline=LINE_DARK, width=1)
    # Simple floral pattern on apron (small marks)
    fl_rng = random.Random(67)
    for _ in range(5):
        fx = apron_cx - apron_w // 2 + fl_rng.randint(3, apron_w - 3)
        fy = apron_y1 + fl_rng.randint(3, int(apron_h * 0.4))
        draw.ellipse([fx - 2, fy - 2, fx + 2, fy + 2], fill=(180, 70, 55))


# ── Layer 14: Top/Bottom Temperature Split Pass ───────────────────────────────

def draw_temperature_split(img, win_y1, bw_bot):
    """
    v004 FIX 2c: Explicit top/bottom temperature split for QA warm/cool separation.

    The QA tool (LTG_TOOL_render_qa) measures warm/cool by comparing the
    MEDIAN HUE of the top half vs bottom half of the image. Left/right separation
    does not register as warm/cool in this measurement.

    Strategy:
    - TOP HALF: Reinforce warm amber cast (window, ceiling, upper walls)
      Use SUNLIT_AMBER overlay on top 50% — strong enough to shift median hue warm
    - BOTTOM HALF: Reinforce cool CRT cast on floor zone
      Use CRT_COOL_SPILL overlay on bottom 40% (floor + lower wall zone)

    This creates visible top=warm / bottom=cool temperature logic that also:
    (a) matches the real physics: window light hits top surfaces first
    (b) matches CRT floor spill (TV is low, floor-level device)
    (c) reads as the narrative logic: warmth above, cool mystery below
    """
    temp_overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    td = ImageDraw.Draw(temp_overlay)

    # TOP HALF: Warm amber saturation pass
    # Covers y=0 to y=H//2 — strongest at y=0, fades by y=H//2
    for y in range(H // 2):
        t = 1.0 - (y / (H // 2))
        # Quadratic falloff — strongest near ceiling, fades toward midpoint
        alpha = int(t ** 1.4 * 55)
        if alpha > 0:
            td.line([(0, y), (W, y)], fill=(*SUNLIT_AMBER, alpha))

    # BOTTOM HALF: Cool floor cast — must dominate the warm wood/linoleum floor
    # Covers y=H//2 to y=H — strongest at y=H (floor), fades upward
    # alpha 90 at bottom edge to push floor median hue cool (overcomes warm wood)
    for y in range(H // 2, H):
        t = (y - H // 2) / (H // 2)
        # Linear falloff — strongest at bottom, fades toward midpoint
        alpha = int(t ** 0.9 * 90)
        if alpha > 0:
            td.line([(0, y), (W, y)], fill=(*CRT_COOL_SPILL, alpha))

    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, temp_overlay)
    return img_rgba.convert("RGB")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    rng = random.Random(42)
    img = Image.new("RGB", (W, H), WALL_WARM)

    print("LTG_TOOL_bg_grandma_kitchen.py")
    print("Rendering Grandma Miri's Kitchen v008 — A1-01 (Act 1 opening)...")
    print("v008 changes (Hana Okonkwo C48 — furniture perspective fix):")
    print("  NEW: VP-convergent table, chair, countertop, fridge, cabinet side reveals")
    print("  Per docs/perspective-rules.md + furniture_vp_spec_c48.md")
    print("  Canvas: 1280x720 (direct — no thumbnail needed)")

    print("  [1] Base room — walls, ceiling, floor...")
    draw, vp_x, vp_y, bw_left, bw_top, bw_right, bw_bot = draw_base_room(img)

    print("  [2/deep shadows deferred to end — must apply after all light passes]")

    print("  [3] Window + morning sky + curtains...")
    win_x1, win_x2, win_y1, win_y2 = draw_window(img, draw, vp_x, vp_y,
                                                   bw_left, bw_top, bw_right, bw_bot)

    print("  [4] Doorway + CRT TV (story element — active screen)...")
    img, draw, door_cx, door_cy = draw_doorway_and_crt(img, draw, bw_left, bw_top, bw_bot)

    print("  [5] Cabinets, countertop, stove (+ Miri calendar)...")
    counter_y1, counter_y2 = draw_cabinets_and_appliances(
        draw, bw_left, bw_top, bw_right, bw_bot)

    print("  [7] Sink (below window), dish rack, medicine bottles...")
    draw_sink(draw, bw_left, bw_top, bw_right, bw_bot, win_x1, win_x2, win_y2)

    print("  [8] Refrigerator (travel magnets — Miri detail) + MIRI label plant...")
    fridge_x1_v, fridge_x2_v, fridge_y1_v, fridge_y2_v, div_y_v = draw_refrigerator(
        img, draw, bw_right, bw_top, bw_bot)
    lbl_x1, lbl_y1, lbl_x2, lbl_y2 = draw_miri_fridge_label(
        draw, fridge_x1_v, fridge_x2_v, fridge_y1_v, fridge_y2_v, div_y_v)
    print(f"  [8b] MIRI label planted at x={lbl_x1}-{lbl_x2}, y={lbl_y1}-{lbl_y2}")

    print("  [9] Countertop plant...")
    draw_kitchen_plant(draw, bw_left, bw_top, bw_right, bw_bot)

    print("  [10] Apron on peg near doorway (Miri detail)...")
    draw_apron_on_peg(draw, bw_left, bw_top, bw_bot)

    print("  [11] Kitchen table (crossword, Miri mug, toast, knitting bag)...")
    img = draw_kitchen_table(draw, img, bw_bot)
    draw = ImageDraw.Draw(img)

    print("  [12] Upper wall wallpaper texture — back + side walls...")
    img = draw_upper_wall_texture(img, bw_left, bw_top, bw_right, bw_bot, vp_y)
    draw = ImageDraw.Draw(img)

    print("  [13] Perspective-correct floor linoleum grid + worn path...")
    img = draw_floor_linoleum_overlay(img, bw_left, bw_bot, bw_right, vp_x, vp_y)
    draw = ImageDraw.Draw(img)

    print("  [14] Warm light pass — SUNLIT_AMBER column gradient LEFT (strengthened)...")
    img = draw_warm_light(img, win_x1, win_x2, win_y1, win_y2, bw_bot)
    draw = ImageDraw.Draw(img)

    print("  [15] Cool CRT light — from doorway into kitchen RIGHT (v004 NEW)...")
    img = draw_crt_cool_light(img, door_cx, door_cy, bw_left, bw_bot)
    draw = ImageDraw.Draw(img)

    print("  [16] Top/bottom temperature split pass (QA warm/cool separation fix)...")
    img = draw_temperature_split(img, win_y1, bw_bot)
    draw = ImageDraw.Draw(img)

    # Deep shadows applied LAST — overwrite any light passes that brightened them
    print("  [17] Deep shadow pass — ceiling corners (applied AFTER light passes)...")
    img = draw_deep_shadows(img, vp_x, vp_y, bw_left, bw_top, bw_right, bw_bot)
    draw = ImageDraw.Draw(img)

    print("  [18] Cabinet undersides deep shadow pass (applied AFTER light passes)...")
    img = draw_cabinet_shadows(img, draw, bw_left, bw_top, bw_right, bw_bot)
    draw = ImageDraw.Draw(img)

    print("  [19] Floor corner deep shadows (applied AFTER light passes)...")
    img = draw_floor_corner_shadows(img)
    draw = ImageDraw.Draw(img)  # noqa: F841

    # v007 final atmosphere passes — break image-border edge runs (line_weight QA fix)
    print("  [20] Paper texture pass (alpha=16) — breaks border edge runs for line_weight QA...")
    img = paper_texture(img, scale=40, alpha=16, seed=42)
    print("  [21] Vignette pass (strength=45) — softens corners, domestic atmosphere...")
    img = vignette(img, strength=45)

    # Output path
    out_dir = output_dir('backgrounds', 'environments')
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "LTG_ENV_grandma_kitchen.png")

    # Flatten RGBA→RGB (paper_texture and vignette return RGBA)
    img = flatten_rgba_to_rgb(img, background=(255, 255, 255))

    # Hard limit: ≤ 1280px (already 1280×720 — thumbnail is a no-op but apply for compliance)
    img.thumbnail((1280, 1280), Image.LANCZOS)
    img.save(out_path, "PNG")

    size_bytes = os.path.getsize(out_path)
    print(f"\nSaved: {out_path}")
    print(f"File size: {size_bytes:,} bytes ({size_bytes // 1024} KB)")
    print(f"Image size: {img.size[0]}×{img.size[1]}px")

    print("\nv008 verification:")
    print("  [v008 NEW] VP-convergent furniture: table, chair, countertop, fridge trapezoids")
    print("  [v008 NEW] Cabinet side depth reveals (upper + lower, 3px)")
    print("  [v008 NEW] Fridge side face visible (5px depth, left side)")
    print("  [v008 NEW] Countertop front face depth (4px)")
    print("  [CARRY v007] paper_texture(alpha=16) + vignette(strength=45) final passes")
    print("  [CARRY v007] flatten_rgba_to_rgb() at save time (canonical RGBA->RGB)")
    print("  [CARRY v006] MIRI label via draw_pixel_text() — canonical pixel font")
    print("  [CARRY v005] Dual-Miri visual plant: MIRI label on fridge door")
    print("  [CARRY v004] Deep shadows, warm/cool separation, Miri details")


if __name__ == "__main__":
    import argparse
    from LTG_TOOL_warmth_inject_hook import run_warmth_hook

    parser = argparse.ArgumentParser(description="LTG_TOOL_bg_grandma_kitchen — Grandma Miri's Kitchen")
    parser.add_argument(
        "--check-warmth",
        action="store_true",
        help="After generation run LTG_TOOL_warmth_inject if warm/cool QA fails; "
             "saves <name>_warminjected.png alongside the output.",
    )
    args = parser.parse_args()

    main()
    out_path = output_dir('backgrounds', 'environments', 'LTG_ENV_grandma_kitchen.png')
    run_warmth_hook(out_path, enabled=args.check_warmth)
