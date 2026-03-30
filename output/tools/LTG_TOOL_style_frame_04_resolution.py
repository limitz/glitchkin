#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_style_frame_04_resolution.py
Style Frame 04 — "Resolution" (Luma returns to the Real World)
"Luma & the Glitchkin"

Author: Jordan Reed — Style Frame Art Specialist
Cycle: 42

CONCEPT:
  SF04 completes the emotional arc of the pitch package:
    SF01: Discovery (warm domestic, pre-Glitch Layer)
    SF02: Glitch Storm (cold contested street, Glitch invasion)
    SF03: Other Side (alien cold void, the Glitch Layer itself)
    SF04: Resolution (return to domestic warmth — but changed)

  Luma stands in Grandma Miri's kitchen doorway, back home. The kitchen is warm
  and familiar (morning amber, same palette as SF01). But the experience has
  marked both worlds: a faint ELEC_CYAN glow bleeds from the CRT through the
  doorway (Byte as a returning signal, barely legible — the connection remains).
  A single detail on Luma — one cyan pixel-grid streak in her hoodie sleeve —
  marks the crossing. Everything else is Real World.

WARM/COOL STRATEGY:
  - Top half: dominant SUNLIT_AMBER from window (upper-left) + lamp halo
    → hue in warm zone 20°–45°
  - Bottom half: cool floor bounce from doorway CRT glow (ELEC_CYAN bleed)
    → asymmetric alpha (warm top alpha 90, cool bottom alpha 75)
  - Target separation ≥ 12.0

FACE TEST GATE:
  Luma at pitch scale: head_r = 42px → above sprint-scale threshold (20–25px).
  Face test gate does NOT trigger at pitch scale per face_test_gate_policy.
  (Sprint scale threshold = 20–25px. head_r = 42px ≥ threshold.)

OUTPUT:
  /home/wipkat/team/output/style_frames/LTG_COLOR_styleframe_sf04.png
  1280×720 — ≤ 1280px hard limit

Usage:
  python3 output/tools/LTG_TOOL_style_frame_04_resolution.py
"""

import os
import sys
import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

_here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _here)
from LTG_TOOL_procedural_draw import (
    wobble_line, wobble_polygon, variable_stroke,
    add_rim_light, add_face_lighting, silhouette_test, value_study,
    get_char_bbox
)

OUTPUT_PATH = "/home/wipkat/team/output/style_frames/LTG_COLOR_styleframe_sf04.png"

W, H = 1280, 720

SX = W / 1920
SY = H / 1080
def sx(n): return int(n * SX)
def sy(n): return int(n * SY)
def sp(n): return int(n * min(SX, SY))


# ── Canonical Palette ─────────────────────────────────────────────────────────
# Real World — warm domestic
WARM_CREAM      = (250, 240, 220)
WALL_UPPER      = (218, 188, 148)   # warm upper wall
WALL_MID        = (232, 200, 158)   # mid wall
WALL_LOWER      = (215, 178, 130)   # wall near floor
FLOOR_LINO      = (168, 138, 100)   # linoleum warm tan
FLOOR_DARK      = ( 90,  64,  38)   # deep shadow under furniture
CEIL_COLOR      = (190, 162, 118)   # warm cream ceiling
CEIL_DARK       = (155, 130,  90)   # ceiling shadow zone

# Lighting sources
SUNLIT_AMBER    = (212, 146,  58)   # canonical (212,146,58) — window top half
LAMP_AMBER      = (255, 140,   0)   # canonical #FF8C00 indoor lamp
SPECULAR_WHITE  = (255, 252, 240)   # value ceiling ≥ 225

# Kitchen props — Real World palette
LINOLEUM_EDGE   = (145, 118,  82)
CABINET_WARM    = (188, 156, 112)
CABINET_HL      = (210, 180, 140)
CABINET_SH      = (138, 108,  72)
COUNTER_WARM    = (196, 168, 128)
STOVE_DARK      = ( 65,  55,  45)
STOVE_MID       = ( 95,  82,  68)
FRIDGE_CREAM    = (235, 228, 210)
FRIDGE_SH       = (198, 192, 175)
WINDOW_GLASS    = (200, 220, 240)
WINDOW_FRAME    = (215, 188, 148)
MUG_RED         = (190,  62,  52)
MUG_HL          = (220,  90,  75)

# CRT through doorway — Glitch residue source
CRT_TEAL        = (  0, 212, 232)   # BYTE_TEAL — CRT screen color
CRT_GLOW        = (  0, 180, 200)   # floor bounce from CRT
DOOR_DARK       = ( 48,  36,  24)   # doorway opening (dark interior)
DOOR_FRAME      = (176, 148, 108)

# Glitch residue — subtle contamination only
ELEC_CYAN       = (  0, 240, 255)   # GL-01 — used sparingly for residue
COOL_FILL       = (160, 195, 215)   # monitor-cool floor spill
BYTE_GHOST      = ( 20, 180, 200)   # Byte as faded signal — desaturated teal

# Character — Luma
LINE            = ( 59,  40,  32)
HAIR_COLOR      = ( 26,  15,  10)
SKIN            = (200, 136,  90)
SKIN_HL         = (232, 184, 136)
SKIN_SH         = (168, 104,  56)
BLUSH           = (232, 168, 124)   # #E8A87C canonical
HOODIE_ORANGE   = (232, 112,  58)
HOODIE_SHADOW   = (184,  74,  32)
HOODIE_PIXEL    = ( 38, 200, 220)   # single Glitch-residue cyan pixel in sleeve
JEANS           = ( 58,  90, 140)
JEANS_SH        = ( 38,  62, 104)
SHOE_DARK       = ( 42,  38,  32)

# Deep shadows
DEEP_COCOA      = ( 40,  24,  12)
NEAR_BLACK_WARM = ( 28,  18,   8)


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


def alpha_over(base_img, color_rgb, alpha, region=None):
    """Alpha-composite a solid color over a region of base_img in-place."""
    overlay = Image.new("RGBA", base_img.size, (0, 0, 0, 0))
    ov_draw = ImageDraw.Draw(overlay)
    if region is None:
        region = [0, 0, base_img.width, base_img.height]
    ov_draw.rectangle(region, fill=(*color_rgb, alpha))
    base_rgba = base_img.convert("RGBA")
    result = Image.alpha_composite(base_rgba, overlay)
    base_img.paste(result.convert("RGB"))
    return ImageDraw.Draw(base_img)


def draw_background(img, draw):
    """Kitchen background — warm domestic interior, morning light."""
    rng = random.Random(77)

    ceil_y  = sy(90)
    floor_y = sy(660)

    # ── Ceiling ──────────────────────────────────────────────────────────────
    img.paste(CEIL_DARK, [0, 0, W, ceil_y])
    for row in range(ceil_y):
        t = row / max(1, ceil_y)
        r = int(CEIL_DARK[0] + (CEIL_COLOR[0] - CEIL_DARK[0]) * t)
        g = int(CEIL_DARK[1] + (CEIL_COLOR[1] - CEIL_DARK[1]) * t)
        b = int(CEIL_DARK[2] + (CEIL_COLOR[2] - CEIL_DARK[2]) * t)
        draw.line([(0, row), (W, row)], fill=(r, g, b))

    # ── Back wall — warm gradient top→mid→lower ───────────────────────────────
    for row in range(ceil_y, floor_y):
        t = (row - ceil_y) / max(1, floor_y - ceil_y)
        r = int(WALL_UPPER[0] + (WALL_LOWER[0] - WALL_UPPER[0]) * t)
        g = int(WALL_UPPER[1] + (WALL_LOWER[1] - WALL_UPPER[1]) * t)
        b = int(WALL_UPPER[2] + (WALL_LOWER[2] - WALL_UPPER[2]) * t)
        draw.line([(0, row), (W, row)], fill=(r, g, b))

    # ── Floor ─────────────────────────────────────────────────────────────────
    for row in range(floor_y, H):
        t = (row - floor_y) / max(1, H - floor_y)
        r = int(FLOOR_LINO[0] - int(20 * t))
        g = int(FLOOR_LINO[1] - int(20 * t))
        b = int(FLOOR_LINO[2] - int(15 * t))
        draw.line([(0, row), (W, row)], fill=(max(0,r), max(0,g), max(0,b)))

    # Floor linoleum grid — perspective-correct
    vp_x = W // 2
    floor_top = floor_y
    # Horizontal rows (non-linear spacing)
    num_rows = 8
    for i in range(num_rows):
        t_row = ((i + 1) / num_rows) ** 1.4
        ry = int(floor_top + (H - floor_top) * t_row)
        alpha_v = int(28 + 18 * t_row)
        draw.line([(0, ry), (W, ry)], fill=LINOLEUM_EDGE + (alpha_v,) if False else LINOLEUM_EDGE, width=1)
    # Simplified: just draw the lines directly
    for i in range(num_rows):
        t_row = ((i + 1) / num_rows) ** 1.4
        ry = int(floor_top + (H - floor_top) * t_row)
        r_ = max(0, FLOOR_LINO[0] - 20)
        g_ = max(0, FLOOR_LINO[1] - 20)
        b_ = max(0, FLOOR_LINO[2] - 15)
        draw.line([(0, ry), (W, ry)], fill=(r_, g_, b_), width=1)

    # Vertical lines converging to VP
    num_cols = 10
    for j in range(num_cols + 1):
        bx = int(W * j / num_cols)
        draw.line([(vp_x, floor_top), (bx, H)], fill=LINOLEUM_EDGE, width=1)

    draw = ImageDraw.Draw(img)

    # ── Kitchen window — upper left ───────────────────────────────────────────
    win_x0 = sx(60)
    win_y0 = sy(120)
    win_x1 = sx(310)
    win_y1 = sy(360)
    frame_w = sp(10)

    # Window frame
    draw.rectangle([win_x0 - frame_w, win_y0 - frame_w,
                    win_x1 + frame_w, win_y1 + frame_w],
                   fill=WINDOW_FRAME)
    # Window glass — bright sky
    draw.rectangle([win_x0, win_y0, win_x1, win_y1], fill=WINDOW_GLASS)
    # Window pane dividers (cross)
    mid_wx = (win_x0 + win_x1) // 2
    mid_wy = (win_y0 + win_y1) // 2
    draw.rectangle([mid_wx - sp(3), win_y0, mid_wx + sp(3), win_y1], fill=WINDOW_FRAME)
    draw.rectangle([win_x0, mid_wy - sp(3), win_x1, mid_wy + sp(3)], fill=WINDOW_FRAME)

    # ── Upper cabinets (right half of back wall) ─────────────────────────────
    cab_y0 = sy(140)
    cab_y1 = sy(390)
    cab_x0 = sx(640)
    cab_x1 = W

    draw.rectangle([cab_x0, cab_y0, cab_x1, cab_y1], fill=CABINET_WARM)
    # Cabinet door panels (3 doors)
    door_w = (cab_x1 - cab_x0) // 3
    for di in range(3):
        dx0 = cab_x0 + di * door_w + sp(6)
        dx1 = cab_x0 + (di + 1) * door_w - sp(6)
        draw.rectangle([dx0, cab_y0 + sp(8), dx1, cab_y1 - sp(8)],
                       outline=CABINET_SH, width=sp(2))
        # Door handle
        hx = (dx0 + dx1) // 2
        hy = (cab_y0 + cab_y1) // 2
        draw.ellipse([hx - sp(4), hy - sp(4), hx + sp(4), hy + sp(4)],
                     fill=CABINET_SH)
    # Cabinet bottom trim
    draw.rectangle([cab_x0, cab_y1, cab_x1, cab_y1 + sp(8)],
                   fill=CABINET_SH)

    # ── Counter / benchtop ────────────────────────────────────────────────────
    ctr_y0 = sy(390)
    ctr_y1 = sy(420)
    draw.rectangle([sx(640), ctr_y0, W, ctr_y1], fill=COUNTER_WARM)
    draw.rectangle([sx(640), ctr_y0, W, ctr_y0 + sp(5)], fill=CABINET_HL)

    # ── Stove (right of center, back wall) ───────────────────────────────────
    stv_x0 = sx(800)
    stv_x1 = sx(1020)
    stv_y0 = ctr_y1
    stv_y1 = floor_y
    draw.rectangle([stv_x0, stv_y0, stv_x1, stv_y1], fill=STOVE_DARK)
    # Burner rings
    for bri, (brx, bry) in enumerate([(sx(870), sy(470)), (sx(960), sy(470)),
                                       (sx(870), sy(560)), (sx(960), sy(560))]):
        draw.ellipse([brx - sp(22), bry - sp(22), brx + sp(22), bry + sp(22)],
                     outline=STOVE_MID, width=sp(3))
        draw.ellipse([brx - sp(14), bry - sp(14), brx + sp(14), bry + sp(14)],
                     outline=(75, 65, 55), width=sp(2))

    # ── Teapot on stove ───────────────────────────────────────────────────────
    tp_cx = sx(900)
    tp_cy = sy(440)
    draw.ellipse([tp_cx - sp(28), tp_cy - sp(32), tp_cx + sp(28), tp_cy + sp(24)],
                 fill=(150, 85, 50), outline=LINE, width=sp(2))
    # Spout
    draw.polygon([(tp_cx + sp(24), tp_cy - sp(10)),
                  (tp_cx + sp(48), tp_cy - sp(22)),
                  (tp_cx + sp(52), tp_cy - sp(14)),
                  (tp_cx + sp(26), tp_cy - sp(2))],
                 fill=(130, 70, 40))
    # Handle
    draw.arc([tp_cx - sp(42), tp_cy - sp(12), tp_cx - sp(22), tp_cy + sp(12)],
             start=40, end=320, fill=LINE, width=sp(4))
    # Lid
    draw.ellipse([tp_cx - sp(16), tp_cy - sp(38), tp_cx + sp(16), tp_cy - sp(28)],
                 fill=(160, 90, 55), outline=LINE, width=sp(2))

    # ── Red mug (Miri's) on counter ───────────────────────────────────────────
    mug_x = sx(1100)
    mug_y = ctr_y1 - sp(42)
    draw.rectangle([mug_x, mug_y, mug_x + sp(26), mug_y + sp(40)],
                   fill=MUG_RED)
    draw.rectangle([mug_x + sp(4), mug_y + sp(4), mug_x + sp(22), mug_y + sp(10)],
                   fill=MUG_HL)
    draw.arc([mug_x + sp(24), mug_y + sp(10), mug_x + sp(38), mug_y + sp(30)],
             start=270, end=90, fill=LINE, width=sp(3))
    # Steam from mug
    for si in range(3):
        sx0 = mug_x + sp(8 + si * 6)
        for sj in range(4):
            amp = sp(3)
            y_top = mug_y - sp(8 + sj * 10)
            y_bot = mug_y - sp(2 + sj * 10)
            draw.arc([sx0 - amp, y_top, sx0 + amp, y_bot],
                     start=0, end=180, fill=(220, 210, 200), width=sp(1))

    # ── Fridge (far left of back wall) ────────────────────────────────────────
    fr_x0 = sx(340)
    fr_x1 = sx(590)
    fr_y0 = ceil_y + sp(8)
    fr_y1 = floor_y
    fr_mid = (fr_y0 + fr_y1) // 2

    draw.rectangle([fr_x0, fr_y0, fr_x1, fr_y1], fill=FRIDGE_CREAM)
    draw.rectangle([fr_x0 + sp(5), fr_y0 + sp(5), fr_x1 - sp(5), fr_mid - sp(5)],
                   outline=FRIDGE_SH, width=sp(2))
    draw.rectangle([fr_x0 + sp(5), fr_mid + sp(5), fr_x1 - sp(5), fr_y1 - sp(5)],
                   outline=FRIDGE_SH, width=sp(2))
    # Fridge handles
    handle_x = fr_x1 - sp(18)
    draw.rectangle([handle_x, fr_y0 + sp(20), handle_x + sp(8), fr_mid - sp(20)],
                   fill=FRIDGE_SH, outline=CABINET_SH, width=sp(1))
    draw.rectangle([handle_x, fr_mid + sp(20), handle_x + sp(8), fr_y1 - sp(20)],
                   fill=FRIDGE_SH, outline=CABINET_SH, width=sp(1))

    # Fridge magnets (colourful — lived-in detail)
    magnet_data = [
        (sx(370), sy(310), (210, 75, 60)),   # red
        (sx(398), sy(300), (65, 140, 195)),  # blue
        (sx(426), sy(315), (85, 170, 80)),   # green
        (sx(454), sy(305), (220, 190, 55)),  # yellow
        (sx(480), sy(312), (180, 90, 200)),  # purple
    ]
    for mx, my, mc in magnet_data:
        draw.ellipse([mx - sp(7), my - sp(7), mx + sp(7), my + sp(7)], fill=mc)

    # MIRI label on lower fridge door (Dual-Miri plant — subtle)
    miri_x = sx(380)
    miri_y = sy(490)
    draw.rectangle([miri_x, miri_y, miri_x + sp(34), miri_y + sp(14)],
                   fill=(235, 230, 215))
    fnt_small = load_font(size=sp(9))
    draw.text((miri_x + sp(3), miri_y + sp(2)), "MIRI", fill=(45, 35, 25), font=fnt_small)

    return draw


def draw_doorway(img, draw):
    """Doorway on right wall — leading to hallway with CRT glow (Byte signal)."""
    # Doorway opening dimensions
    door_x0 = sx(1540)
    door_x1 = sx(1780)
    door_y0 = sy(200)
    door_y1 = sy(760)

    # Clip to canvas
    door_x0 = min(door_x0, W - sp(4))
    door_x1 = min(door_x1, W)
    door_y0 = max(door_y0, 0)
    door_y1 = min(door_y1, H)

    # ── Doorway: dark interior beyond ────────────────────────────────────────
    draw.rectangle([door_x0, door_y0, door_x1, door_y1], fill=DOOR_DARK)

    # ── CRT glow through doorway (Byte as faded signal) ─────────────────────
    crt_glow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    crt_glow_draw  = ImageDraw.Draw(crt_glow_layer)
    # CRT screen shape (faint, upper part of doorway opening)
    crt_cx = (door_x0 + door_x1) // 2
    crt_cy = door_y0 + (door_y1 - door_y0) // 3
    crt_w  = door_x1 - door_x0 - sp(16)
    crt_h  = int(crt_w * 0.75)
    # Radial glow layers — CRT bleed through door
    for step in range(18, 0, -1):
        t = step / 18
        r_w = int(crt_w * 0.5 + crt_w * 0.8 * (1 - t))
        r_h = int(crt_h * 0.5 + crt_h * 0.8 * (1 - t))
        alpha = int(60 * t)
        glow_r = int(CRT_TEAL[0] * t * 0.3)
        glow_g = int(CRT_TEAL[1] * t * 0.85)
        glow_b = int(CRT_TEAL[2] * t * 0.95)
        crt_glow_draw.ellipse(
            [crt_cx - r_w, crt_cy - r_h, crt_cx + r_w, crt_cy + r_h],
            fill=(glow_r, glow_g, glow_b, alpha)
        )

    # Byte ghost form in doorway — barely legible faded silhouette
    ghost_cx = crt_cx
    ghost_cy = door_y0 + (door_y1 - door_y0) // 2
    ghost_h  = int((door_y1 - door_y0) * 0.55)
    ghost_w  = int(ghost_h * 0.55)
    # Byte body (very faint — returning signal)
    for step in range(8, 0, -1):
        t = step / 8
        bw = int(ghost_w * 0.4 + ghost_w * 0.5 * t)
        bh = int(ghost_h * 0.4 + ghost_h * 0.45 * t)
        alpha = int(35 * t)
        crt_glow_draw.ellipse(
            [ghost_cx - bw, ghost_cy - bh, ghost_cx + bw, ghost_cy + bh],
            fill=(*BYTE_GHOST, alpha)
        )
    # Byte eyes — two faint pixel-dots
    eye_r = sp(5)
    eye_y  = ghost_cy - int(ghost_h * 0.15)
    eye_dx = int(ghost_w * 0.3)
    for ex in [ghost_cx - eye_dx, ghost_cx + eye_dx]:
        crt_glow_draw.ellipse([ex - eye_r, eye_y - eye_r, ex + eye_r, eye_y + eye_r],
                              fill=(*ELEC_CYAN, 55))

    base_rgba = img.convert("RGBA")
    result = Image.alpha_composite(base_rgba, crt_glow_layer)
    img.paste(result.convert("RGB"))
    draw = ImageDraw.Draw(img)

    # Door frame
    draw.rectangle([door_x0 - sp(12), door_y0 - sp(6),
                    door_x1 + sp(4), door_y1 + sp(4)],
                   outline=DOOR_FRAME, width=sp(10))

    return draw


def draw_table_foreground(img, draw):
    """Kitchen table in foreground — establishes depth."""
    rng = random.Random(33)
    table_y = sy(620)
    table_h = H - table_y

    # Table surface
    draw.rectangle([sx(-20), table_y, sx(900), H],
                   fill=(148, 112, 72))
    # Table edge highlight
    draw.rectangle([sx(-20), table_y, sx(900), table_y + sp(6)],
                   fill=(175, 140, 95))
    # Table underside shadow
    draw.rectangle([sx(-20), table_y + sp(6), sx(900), table_y + sp(24)],
                   fill=(108, 78, 48))

    # Items on table: crossword, tea mug, toast
    # Crossword newspaper (bottom-left)
    np_x0 = sx(40)
    np_y0 = table_y + sp(14)
    np_x1 = sx(290)
    np_y1 = table_y + sp(56)
    draw.rectangle([np_x0, np_y0, np_x1, np_y1], fill=(230, 220, 200))
    # Crossword grid (tiny — suggestive)
    for gi in range(5):
        for gj in range(5):
            gx = np_x0 + sp(14) + gi * sp(20)
            gy = np_y0 + sp(8) + gj * sp(8)
            if rng.random() < 0.3:
                draw.rectangle([gx, gy, gx + sp(16), gy + sp(6)],
                               fill=(38, 32, 28))
            else:
                draw.rectangle([gx, gy, gx + sp(16), gy + sp(6)],
                               outline=(160, 150, 130), width=sp(1))

    # Tea mug on table (warm)
    tm_cx = sx(370)
    tm_y0 = table_y + sp(8)
    draw.ellipse([tm_cx - sp(20), tm_y0, tm_cx + sp(20), tm_y0 + sp(36)],
                 fill=MUG_RED, outline=LINE, width=sp(2))
    draw.arc([tm_cx + sp(18), tm_y0 + sp(8), tm_cx + sp(30), tm_y0 + sp(26)],
             start=270, end=90, fill=LINE, width=sp(3))

    # Toast plate (right side)
    pt_cx = sx(580)
    pt_y  = table_y + sp(28)
    draw.ellipse([pt_cx - sp(38), pt_y - sp(12), pt_cx + sp(38), pt_y + sp(12)],
                 fill=(200, 190, 170), outline=(170, 160, 140), width=sp(1))
    draw.rectangle([pt_cx - sp(22), pt_y - sp(22), pt_cx + sp(22), pt_y - sp(4)],
                   fill=(190, 140, 70))
    draw.rectangle([pt_cx - sp(22), pt_y - sp(22), pt_cx + sp(22), pt_y - sp(16)],
                   fill=(140, 92, 38))

    draw = ImageDraw.Draw(img)
    return draw


def draw_warm_light(img, draw):
    """
    Warm light passes — top half dominant.
    SUNLIT_AMBER from window (upper-left) dominates top half (alpha 90).
    Lamp halo center-upper.
    """
    light_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(light_layer)

    # ── Window shaft (upper-left → spreading to right) ───────────────────────
    shaft_poly = [
        (sx(60), sy(120)),
        (sx(310), sy(120)),
        (sx(700), sy(280)),
        (sx(580), sy(340)),
        (sx(-20), sy(240)),
    ]
    ld.polygon(shaft_poly, fill=(*SUNLIT_AMBER, 42))
    # Second softer shaft pass
    shaft_poly2 = [
        (sx(80), sy(120)),
        (sx(295), sy(120)),
        (sx(620), sy(310)),
        (sx(520), sy(360)),
        (sx(40), sy(250)),
    ]
    ld.polygon(shaft_poly2, fill=(*SUNLIT_AMBER, 28))

    # ── Top half warm overlay (dominant warm tone for top/bottom separation) ──
    # C35 lesson: must be strong (alpha 90) to push median hue into warm zone.
    half_h = H // 2
    for i in range(half_h):
        t = 1.0 - i / half_h          # strongest at top, fades to middle
        alpha = int(115 * t)            # linear from 115 at top to 0 at midpoint
        ld.line([(0, i), (W, i)], fill=(*SUNLIT_AMBER, alpha))

    # ── Lamp halo (upper-left ceiling fixture) ────────────────────────────────
    lamp_cx = sx(760)
    lamp_cy = sy(40)
    for step in range(20, 0, -1):
        t = step / 20
        r_x = int(sx(260) * (1 - t * 0.5))
        r_y = int(sy(180) * (1 - t * 0.5))
        alpha = int(55 * t * t)
        ld.ellipse([lamp_cx - r_x, lamp_cy - r_y, lamp_cx + r_x, lamp_cy + r_y],
                   fill=(*LAMP_AMBER, alpha))

    # Lamp bulb specular (value ceiling)
    ld.ellipse([lamp_cx - sp(12), lamp_cy - sp(8), lamp_cx + sp(12), lamp_cy + sp(8)],
               fill=(*SPECULAR_WHITE, 200))

    base_rgba = img.convert("RGBA")
    result = Image.alpha_composite(base_rgba, light_layer)
    img.paste(result.convert("RGB"))
    draw = ImageDraw.Draw(img)
    return draw


def draw_cool_floor_bounce(img, draw):
    """
    Cool bottom-half bounce from CRT glow through doorway.
    Keeps warm/cool separation high by cooling the floor zone.
    Target: bottom-half median hue well into cool range.
    """
    cool_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(cool_layer)

    half_h = H // 2

    # ── Bottom half cool overlay (CRT bleed on floor) ─────────────────────────
    # C35 lesson: cool must be STRONGER than warm floor to dominate median hue.
    # Floor is warm lino — asymmetric alpha required (cool alpha 95 > warm alpha).
    for i in range(half_h):
        t = i / half_h                 # 0 at midpoint, 1 at bottom
        alpha = int(95 * t)            # linear — strongest at floor
        cd.line([(0, half_h + i), (W, half_h + i)],
                fill=(*CRT_GLOW, alpha))

    # ── CRT floor spill pool — wide spread across full bottom half ────────────
    # Use full-width spread so the cool hue covers the entire floor zone.
    spill_cx = W // 2
    spill_cy = H - sy(60)
    for step in range(18, 0, -1):
        t = step / 18
        r_x = int(W * 0.7 * t)
        r_y = int(sy(140) * t)
        alpha = int(65 * t)
        cd.ellipse([spill_cx - r_x, spill_cy - r_y, spill_cx + r_x, spill_cy + r_y],
                   fill=(*CRT_GLOW, alpha))

    base_rgba = img.convert("RGBA")
    result = Image.alpha_composite(base_rgba, cool_layer)
    img.paste(result.convert("RGB"))
    draw = ImageDraw.Draw(img)
    return draw


def draw_luma(img, draw):
    """
    Draw Luma in the kitchen doorway area — returning home.
    Standing pose, facing slightly right (toward camera/viewer).
    Pitch scale: head_r = 42px. Face test gate NOT triggered (pitch scale).
    Glitch-residue detail: one cyan pixel-grid streak in left hoodie sleeve.
    """
    rng = random.Random(55)

    # Character geometry
    head_r = 42
    luma_cx = sx(640)   # center-left of frame — just entered kitchen
    head_cy = sy(280)

    body_top = head_cy + head_r + sp(4)
    body_bot = sy(640)
    body_w   = sp(62)

    shoulder_y = body_top + sp(12)
    hip_y      = body_top + int((body_bot - body_top) * 0.55)

    # ── Legs ──────────────────────────────────────────────────────────────────
    leg_h   = body_bot - hip_y
    leg_w   = sp(22)
    leg_gap = sp(10)
    # Left leg
    draw.rectangle([luma_cx - leg_gap - leg_w, hip_y,
                    luma_cx - leg_gap, body_bot],
                   fill=JEANS)
    # Right leg (slight step forward — returning home pose)
    draw.rectangle([luma_cx + leg_gap, hip_y,
                    luma_cx + leg_gap + leg_w, body_bot - sp(8)],
                   fill=JEANS)
    # Leg shadow sides
    draw.rectangle([luma_cx - leg_gap - leg_w, hip_y,
                    luma_cx - leg_gap - leg_w + sp(5), body_bot],
                   fill=JEANS_SH)
    draw.rectangle([luma_cx + leg_gap + leg_w - sp(5), hip_y,
                    luma_cx + leg_gap + leg_w, body_bot - sp(8)],
                   fill=JEANS_SH)
    # Shoes
    draw.ellipse([luma_cx - leg_gap - leg_w - sp(4), body_bot - sp(8),
                  luma_cx - leg_gap + sp(4), body_bot + sp(8)],
                 fill=SHOE_DARK)
    draw.ellipse([luma_cx + leg_gap - sp(4), body_bot - sp(16),
                  luma_cx + leg_gap + leg_w + sp(4), body_bot],
                 fill=SHOE_DARK)

    # ── Hoodie body (A-line silhouette) ───────────────────────────────────────
    hoodie_poly = [
        (luma_cx - body_w // 2, shoulder_y),
        (luma_cx + body_w // 2, shoulder_y),
        (luma_cx + body_w // 2 + sp(10), hip_y),
        (luma_cx - body_w // 2 - sp(10), hip_y),
    ]
    draw.polygon(hoodie_poly, fill=HOODIE_ORANGE)
    # Hoodie shadow side (left)
    shadow_poly = [
        (luma_cx - body_w // 2, shoulder_y),
        (luma_cx - sp(12), shoulder_y),
        (luma_cx - sp(12), hip_y),
        (luma_cx - body_w // 2 - sp(10), hip_y),
    ]
    draw.polygon(shadow_poly, fill=HOODIE_SHADOW)
    draw = ImageDraw.Draw(img)

    # ── Pixel grid on chest (hoodie design) ───────────────────────────────────
    grid_cx = luma_cx + sp(6)
    grid_cy = shoulder_y + sp(28)
    px_size = sp(4)
    pixel_pattern = [
        (1,0),(2,0),(0,1),(3,1),(1,2),(2,2),(0,3),(3,3),(1,4),(2,4)
    ]
    for (px, py) in pixel_pattern:
        draw.rectangle([grid_cx + px * (px_size + 1),
                        grid_cy + py * (px_size + 1),
                        grid_cx + px * (px_size + 1) + px_size,
                        grid_cy + py * (px_size + 1) + px_size],
                       fill=HOODIE_SHADOW)

    # ── GLITCH RESIDUE: cyan pixel streak in left sleeve ─────────────────────
    # One subtle ELEC_CYAN detail — marks the crossing between worlds
    sleeve_x = luma_cx - body_w // 2 - sp(12)
    sleeve_y = shoulder_y + sp(18)
    residue_pixels = [(0,0),(1,0),(0,1),(2,1),(1,2),(0,3),(1,3)]
    px_tiny = sp(3)
    for (rpx, rpy) in residue_pixels:
        draw.rectangle([sleeve_x + rpx * (px_tiny + 1),
                        sleeve_y + rpy * (px_tiny + 1),
                        sleeve_x + rpx * (px_tiny + 1) + px_tiny,
                        sleeve_y + rpy * (px_tiny + 1) + px_tiny],
                       fill=HOODIE_PIXEL)

    # ── Arms ──────────────────────────────────────────────────────────────────
    # Left arm (slightly out, backpack strap implied)
    arm_l_x0 = luma_cx - body_w // 2 - sp(22)
    arm_l_y0 = shoulder_y + sp(4)
    arm_l_x1 = luma_cx - body_w // 2
    arm_l_y1 = shoulder_y + sp(52)
    draw.rectangle([arm_l_x0, arm_l_y0, arm_l_x1, arm_l_y1], fill=HOODIE_SHADOW)
    # Right arm (slightly forward — reaching/open)
    arm_r_x0 = luma_cx + body_w // 2
    arm_r_y0 = shoulder_y + sp(4)
    arm_r_x1 = luma_cx + body_w // 2 + sp(22)
    arm_r_y1 = shoulder_y + sp(56)
    draw.rectangle([arm_r_x0, arm_r_y0, arm_r_x1, arm_r_y1], fill=HOODIE_ORANGE)

    # Hands
    draw.ellipse([arm_l_x0 - sp(6), arm_l_y1 - sp(4),
                  arm_l_x0 + sp(14), arm_l_y1 + sp(14)],
                 fill=SKIN)
    draw.ellipse([arm_r_x1 - sp(8), arm_r_y1 - sp(4),
                  arm_r_x1 + sp(14), arm_r_y1 + sp(14)],
                 fill=SKIN)

    # ── Neck ──────────────────────────────────────────────────────────────────
    neck_w = sp(16)
    draw.rectangle([luma_cx - neck_w // 2, head_cy + head_r - sp(4),
                    luma_cx + neck_w // 2, body_top + sp(6)],
                   fill=SKIN)

    # ── Head (circle) ─────────────────────────────────────────────────────────
    draw.ellipse([luma_cx - head_r, head_cy - head_r,
                  luma_cx + head_r, head_cy + head_r],
                 fill=SKIN, outline=LINE, width=sp(2))

    # ── Hair cloud (asymmetric) ───────────────────────────────────────────────
    hair_puffs = [
        (luma_cx - sp(22), head_cy - sp(28), sp(24)),
        (luma_cx,          head_cy - sp(38), sp(22)),
        (luma_cx + sp(20), head_cy - sp(30), sp(20)),
        (luma_cx - sp(38), head_cy - sp(8),  sp(18)),
        (luma_cx + sp(36), head_cy - sp(12), sp(16)),
    ]
    for (hx, hy, hr) in hair_puffs:
        draw.ellipse([hx - hr, hy - hr, hx + hr, hy + hr], fill=HAIR_COLOR)

    # ── Face features ─────────────────────────────────────────────────────────
    # Eyes (warm, wide — HOME expression)
    eye_w = int(head_r * 0.22)   # canonical: eye_w = int(head_r * 0.22)
    eye_h = int(eye_w * 1.3)
    eye_l_cx = luma_cx - sp(14)
    eye_r_cx = luma_cx + sp(14)
    eye_cy   = head_cy - sp(4)

    # Eye whites
    draw.ellipse([eye_l_cx - eye_w, eye_cy - eye_h,
                  eye_l_cx + eye_w, eye_cy + eye_h],
                 fill=(245, 242, 235), outline=LINE, width=sp(2))
    draw.ellipse([eye_r_cx - eye_w, eye_cy - eye_h,
                  eye_r_cx + eye_w, eye_cy + eye_h],
                 fill=(245, 242, 235), outline=LINE, width=sp(2))
    # Iris (warm brown — REAL WORLD, no cyan residue in eyes)
    iris_r = int(eye_w * 0.72)
    draw.ellipse([eye_l_cx - iris_r, eye_cy - iris_r,
                  eye_l_cx + iris_r, eye_cy + iris_r],
                 fill=(90, 62, 38))
    draw.ellipse([eye_r_cx - iris_r, eye_cy - iris_r,
                  eye_r_cx + iris_r, eye_cy + iris_r],
                 fill=(90, 62, 38))
    # Pupils
    pup_r = int(iris_r * 0.55)
    draw.ellipse([eye_l_cx - pup_r, eye_cy - pup_r,
                  eye_l_cx + pup_r, eye_cy + pup_r],
                 fill=(22, 12, 6))
    draw.ellipse([eye_r_cx - pup_r, eye_cy - pup_r,
                  eye_r_cx + pup_r, eye_cy + pup_r],
                 fill=(22, 12, 6))
    # Eye highlight (value ceiling)
    hl_r = max(2, int(pup_r * 0.45))
    draw.ellipse([eye_l_cx + pup_r // 2 - hl_r, eye_cy - pup_r // 2 - hl_r,
                  eye_l_cx + pup_r // 2 + hl_r, eye_cy - pup_r // 2 + hl_r],
                 fill=SPECULAR_WHITE)
    draw.ellipse([eye_r_cx + pup_r // 2 - hl_r, eye_cy - pup_r // 2 - hl_r,
                  eye_r_cx + pup_r // 2 + hl_r, eye_cy - pup_r // 2 + hl_r],
                 fill=SPECULAR_WHITE)

    # Brows (soft — relief/home expression)
    brow_y = eye_cy - eye_h - sp(6)
    draw.arc([eye_l_cx - sp(14), brow_y - sp(5), eye_l_cx + sp(14), brow_y + sp(5)],
             start=200, end=340, fill=HAIR_COLOR, width=sp(3))
    draw.arc([eye_r_cx - sp(14), brow_y - sp(5), eye_r_cx + sp(14), brow_y + sp(5)],
             start=200, end=340, fill=HAIR_COLOR, width=sp(3))

    # Mouth (soft smile — relief)
    mouth_y = head_cy + sp(12)
    draw.arc([luma_cx - sp(14), mouth_y - sp(6), luma_cx + sp(14), mouth_y + sp(6)],
             start=10, end=170, fill=LINE, width=sp(3))

    # Nose (simple)
    draw.arc([luma_cx - sp(5), head_cy + sp(2), luma_cx + sp(5), head_cy + sp(10)],
             start=200, end=340, fill=(160, 100, 65), width=sp(2))

    # Blush
    draw.ellipse([eye_l_cx - sp(12), eye_cy + sp(4),
                  eye_l_cx + sp(12), eye_cy + sp(14)],
                 fill=(*BLUSH, 120))
    draw.ellipse([eye_r_cx - sp(12), eye_cy + sp(4),
                  eye_r_cx + sp(12), eye_cy + sp(14)],
                 fill=(*BLUSH, 120))

    draw = ImageDraw.Draw(img)

    # ── Rim light on Luma (warm — from window, right side) ────────────────────
    luma_cx_val = luma_cx  # per-character cx, NOT canvas midpoint
    img_out = add_rim_light(img, side="right", char_cx=luma_cx_val,
                            light_color=SUNLIT_AMBER, threshold=160, width=sp(2))
    if img_out is not None:
        img = img_out
    draw = ImageDraw.Draw(img)

    return img, draw


def draw_film_grain(img, draw):
    """Film grain overlay — as if through CRT frame (SF04 concept)."""
    rng = random.Random(101)
    grain_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grain_layer)
    n_grains = int(W * H * 0.008)
    for _ in range(n_grains):
        gx = rng.randint(0, W - 1)
        gy = rng.randint(0, H - 1)
        brightness = rng.randint(0, 255)
        alpha = rng.randint(8, 22)
        gd.point((gx, gy), fill=(brightness, brightness, brightness, alpha))

    base_rgba = img.convert("RGBA")
    result = Image.alpha_composite(base_rgba, grain_layer)
    img.paste(result.convert("RGB"))
    draw = ImageDraw.Draw(img)
    return draw


def draw_scanline_hint(img, draw):
    """Faint scanline overlay — scene is viewed through CRT frame."""
    sl_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sld = ImageDraw.Draw(sl_layer)
    spacing = 4
    for y in range(0, H, spacing):
        sld.line([(0, y), (W, y)], fill=(0, 0, 0, 12))
    base_rgba = img.convert("RGBA")
    result = Image.alpha_composite(base_rgba, sl_layer)
    img.paste(result.convert("RGB"))
    draw = ImageDraw.Draw(img)
    return draw


def draw_vignette(img, draw):
    """Soft edge vignette — frames the scene."""
    vig_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    vd = ImageDraw.Draw(vig_layer)
    cx, cy = W // 2, H // 2
    max_r = math.hypot(cx, cy)
    num_steps = 28
    for i in range(num_steps, 0, -1):
        t = i / num_steps
        r_w = int(cx * (1.0 + t * 0.6))
        r_h = int(cy * (1.0 + t * 0.6))
        alpha = int(55 * (1 - t) ** 2)
        vd.ellipse([cx - r_w, cy - r_h, cx + r_w, cy + r_h],
                   fill=(10, 6, 4, alpha))
    base_rgba = img.convert("RGBA")
    result = Image.alpha_composite(base_rgba, vig_layer)
    img.paste(result.convert("RGB"))
    draw = ImageDraw.Draw(img)
    return draw


def draw_title_strip(img, draw):
    """Title strip at bottom — SF04 label."""
    strip_h = sy(48)
    strip_y = H - strip_h

    # Strip background (dark, warm-tinted)
    strip_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(strip_layer)
    sd.rectangle([0, strip_y, W, H], fill=(20, 14, 10, 210))
    base_rgba = img.convert("RGBA")
    result = Image.alpha_composite(base_rgba, strip_layer)
    img.paste(result.convert("RGB"))
    draw = ImageDraw.Draw(img)

    # Title text
    fnt_large = load_font(size=sp(18), bold=True)
    fnt_small  = load_font(size=sp(11))
    title  = "Luma & the Glitchkin"
    ep_tag = "SF04 — Resolution"
    draw.text((sp(24), strip_y + sp(8)),  title,  fill=(232, 200, 140), font=fnt_large)
    draw.text((sp(24), strip_y + sp(28)), ep_tag, fill=(140, 195, 210), font=fnt_small)

    # Warm/cool arc indicator (small bar at bottom-right)
    arc_x = W - sp(200)
    arc_y = strip_y + sp(10)
    arc_w = sp(170)
    arc_h = sp(12)
    # Gradient bar warm→cool
    for xi in range(arc_w):
        t = xi / arc_w
        r_ = int(212 + (0 - 212) * t)
        g_ = int(146 + (180 - 146) * t)
        b_ = int(58  + (200 - 58)  * t)
        draw.line([(arc_x + xi, arc_y), (arc_x + xi, arc_y + arc_h)],
                  fill=(max(0, r_), max(0, g_), b_))
    # Marker at SF04 position (biased warm — near left)
    marker_x = arc_x + int(arc_w * 0.32)
    draw.line([(marker_x, arc_y - sp(3)), (marker_x, arc_y + arc_h + sp(3))],
              fill=(255, 252, 240), width=sp(2))
    draw.text((arc_x, arc_y + arc_h + sp(3)), "WARM←  →COLD",
              fill=(160, 155, 148), font=load_font(size=sp(8)))

    draw = ImageDraw.Draw(img)
    return draw


def main():
    print(f"[SF04] Drawing Resolution style frame — {W}×{H}")

    img  = Image.new("RGB", (W, H), WALL_MID)
    draw = ImageDraw.Draw(img)

    # Pass 1: Background
    print("[SF04] Pass 1: Background kitchen...")
    draw = draw_background(img, draw)

    # Pass 2: Doorway with CRT glow / Byte signal
    print("[SF04] Pass 2: Doorway / Byte signal...")
    draw = draw_doorway(img, draw)

    # Pass 3: Foreground table
    print("[SF04] Pass 3: Foreground table...")
    draw = draw_table_foreground(img, draw)

    # Pass 4: Warm light (top half dominant)
    print("[SF04] Pass 4: Warm light passes...")
    draw = draw_warm_light(img, draw)

    # Pass 5: Cool floor bounce (bottom half — separation)
    print("[SF04] Pass 5: Cool floor bounce...")
    draw = draw_cool_floor_bounce(img, draw)

    # Pass 6: Luma character
    print("[SF04] Pass 6: Luma character...")
    img, draw = draw_luma(img, draw)

    # Pass 7: Film grain
    print("[SF04] Pass 7: Film grain...")
    draw = draw_film_grain(img, draw)

    # Pass 8: Scanline hint
    print("[SF04] Pass 8: Scanline hint...")
    draw = draw_scanline_hint(img, draw)

    # Pass 9: Vignette
    print("[SF04] Pass 9: Vignette...")
    draw = draw_vignette(img, draw)

    # Pass 10: Title strip
    print("[SF04] Pass 10: Title strip...")
    draw = draw_title_strip(img, draw)

    # Enforce ≤ 1280px hard limit
    img.thumbnail((1280, 1280), Image.LANCZOS)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    img.save(OUTPUT_PATH)
    print(f"[SF04] Saved: {OUTPUT_PATH}  ({img.width}×{img.height})")


if __name__ == "__main__":
    main()
