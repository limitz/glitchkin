#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_styleframe_discovery.py
Style Frame 01 — The Discovery (C52 pycairo character migration)
"Luma & the Glitchkin" — Cycle 52

Art Director: Alex Chen
Procedural Art Engineer: Jordan Reed (C52)

C52 changes (Jordan Reed):
  SF01 CHARACTER MIGRATION to pycairo:
    - Luma body/head rendered with cairo bezier curves via cairo_primitives +
      curve_draw. Smooth anti-aliased character silhouettes replace PIL rectangle
      primitives. All character geometry now uses cubic beziers for organic shapes.
    - Byte rendered with pycairo smooth ellipses and gradient fills.
    - Scene lighting from C50 prototype applied: CRT tint on skin, contact shadow,
      bounce light, cyan catch-lights, post-character lighting overlay.
    - Wand compositing for Gaussian blur contact shadows (proper kernel blur).
    - Internal render at 2x (2560x1440) for AA, downscaled to 1280x720 with LANCZOS.
    - All prior C47 sight-line fix geometry preserved.
    - All prior C38 posture/expression changes preserved.
    - C49 CRT glow asymmetry rule preserved.

Output: /home/wipkat/team/output/color/style_frames/LTG_COLOR_styleframe_discovery.png
Usage: python3 LTG_TOOL_styleframe_discovery.py [--save-nolight]
"""

try:
    from LTG_TOOL_project_paths import output_dir, ensure_dir
except ImportError:
    import pathlib
    def output_dir(*parts): return pathlib.Path("/home/wipkat/team/output").joinpath(*parts)
    def ensure_dir(path): path.mkdir(parents=True, exist_ok=True); return path

import os
import sys
import math
import random
import argparse
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# Import tools
_here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _here)
from LTG_TOOL_procedural_draw import (
    wobble_line, wobble_polygon, variable_stroke,
    add_rim_light, add_face_lighting
)
from LTG_TOOL_cairo_primitives import (
    create_surface, draw_bezier_path, draw_tapered_stroke,
    draw_gradient_fill, draw_wobble_path, draw_smooth_polygon,
    draw_ellipse, to_pil_image, to_pil_rgba, set_color
)

# Wand compositing — graceful fallback to PIL if unavailable
_WAND_OK = False
try:
    from LTG_TOOL_wand_composite import (
        wand_contact_shadow, wand_bounce_light, _WAND_AVAILABLE
    )
    _WAND_OK = _WAND_AVAILABLE
except ImportError:
    _WAND_OK = False

# scipy for PIL fallback blur
try:
    from scipy.ndimage import gaussian_filter
    _SCIPY_OK = True
except ImportError:
    _SCIPY_OK = False

import numpy as np
import cairo

OUTPUT_PATH = output_dir('color', 'style_frames', 'LTG_COLOR_styleframe_discovery.png')
NOLIGHT_PATH = output_dir('color', 'style_frames', 'LTG_COLOR_styleframe_discovery_nolight.png')

# ── Render at 2x for AA, downscale to 1280x720 ────────────────────────────
W_OUT, H_OUT = 1280, 720
SCALE = 2
W, H = W_OUT * SCALE, H_OUT * SCALE   # 2560 x 1440

# Scale factors from 1920x1080 reference to 2560x1440 internal
SX = W / 1920
SY = H / 1080

def sx(n): return int(n * SX)
def sy(n): return int(n * SY)
def sp(n): return int(n * min(SX, SY))

# ── Master Palette ──────────────────────────────────────────────────────────
WARM_CREAM      = (250, 240, 220)
SOFT_GOLD       = (232, 201,  90)
SUNLIT_AMBER    = (212, 146,  58)
TERRACOTTA      = (199,  91,  57)
RUST_SHADOW     = (140,  58,  34)
SAGE_GREEN      = (122, 158, 126)
DUSTY_LAVENDER  = (168, 155, 191)
SHADOW_PLUM     = ( 92,  74, 114)
WARM_TAN        = (196, 168, 130)
SKIN_SHADOW     = (140,  90,  56)
DEEP_COCOA      = ( 59,  40,  32)
OCHRE_BRICK     = (184, 148,  74)
ELEC_CYAN       = (  0, 240, 255)
BYTE_TEAL       = (  0, 212, 232)
DEEP_CYAN       = (  0, 168, 180)
HOT_MAGENTA     = (255,  45, 107)
UV_PURPLE       = (123,  47, 190)
VOID_BLACK      = ( 10,  10,  20)
CORRUPTED_AMBER = (255, 140,   0)
STATIC_WHITE    = (240, 240, 240)
SKIN            = (200, 136,  90)
SKIN_HL         = (232, 184, 136)
SKIN_SH         = (168, 104,  56)
CYAN_SKIN       = (122, 188, 186)
HOODIE_ORANGE   = (232, 112,  58)
HOODIE_SHADOW   = (184,  74,  32)
HOODIE_CYAN_LIT = (191, 138, 120)
HAIR_COLOR      = ( 26,  15,  10)
LINE            = ( 59,  40,  32)
BYTE_HL         = (  0, 240, 255)
BYTE_SH         = (  0, 144, 176)
SCAR_MAG        = (255,  45, 107)
HOODIE_AMBIENT  = (179,  98,  80)
JEANS           = ( 58,  90, 140)
JEANS_SH        = ( 38,  62, 104)
COUCH_BODY      = (107,  48,  24)
COUCH_BACK      = (128,  60,  28)
COUCH_ARM       = (115,  52,  26)
BLUSH_LEFT      = (232, 168, 124)
BLUSH_RIGHT     = (228, 162, 118)
LAMP_PEAK       = (245, 200,  66)
CABLE_BRONZE    = (180, 140,  80)
CABLE_DATA_CYAN = (  0, 180, 255)
CABLE_MAG_PURP  = (200,  80, 200)
CABLE_NEUTRAL_PLUM = ( 80,  64, 100)

# ── Scene Light Parameters (SF01-specific) ──────────────────────────────────
SCENE_WARM_TINT = (232, 190, 100)
SCENE_COOL_TINT = (  0, 200, 220)
SCENE_WARM_INFLUENCE = 0.15
SCENE_COOL_INFLUENCE = 0.25


def blend_color(base, tint, influence):
    """Blend base color toward tint by influence factor (0.0-1.0)."""
    return tuple(int(base[i] * (1 - influence) + tint[i] * influence) for i in range(3))


def _c(rgb):
    """(R,G,B) 0-255 -> cairo (r,g,b) 0.0-1.0."""
    return (rgb[0] / 255.0, rgb[1] / 255.0, rgb[2] / 255.0)


def _ca(rgba):
    """(R,G,B,A) 0-255 -> cairo (r,g,b,a) 0.0-1.0."""
    return (rgba[0] / 255.0, rgba[1] / 255.0, rgba[2] / 255.0, rgba[3] / 255.0)


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


# ═══════════════════════════════════════════════════════════════════════════
# Background Drawing (PIL — no change from original, just scaled to 2x)
# ═══════════════════════════════════════════════════════════════════════════

def draw_filled_glow(draw, cx, cy, rx, ry, glow_rgb, bg_rgb, steps=14,
                     screen_mid_y=None, below_mult=0.70):
    """Draw concentric ellipse glow with CRT asymmetry rule (C49)."""
    for i in range(steps, 0, -1):
        t = i / steps
        r_v = int(bg_rgb[0] + (glow_rgb[0] - bg_rgb[0]) * (1 - t))
        g_v = int(bg_rgb[1] + (glow_rgb[1] - bg_rgb[1]) * (1 - t))
        b_v = int(bg_rgb[2] + (glow_rgb[2] - bg_rgb[2]) * (1 - t))
        er   = max(1, int(rx * t))
        er_y = max(1, int(ry * t))

        if screen_mid_y is None:
            draw.ellipse([cx - er, cy - er_y, cx + er, cy + er_y],
                         fill=(r_v, g_v, b_v))
        else:
            ring_top = cy - er_y
            ring_bot = cy + er_y
            if ring_bot <= screen_mid_y:
                draw.ellipse([cx - er, ring_top, cx + er, ring_bot],
                             fill=(r_v, g_v, b_v))
            elif ring_top >= screen_mid_y:
                dim = (int(r_v * below_mult),
                       int(g_v * below_mult),
                       int(b_v * below_mult))
                draw.ellipse([cx - er, ring_top, cx + er, ring_bot], fill=dim)
            else:
                dim = (int(r_v * below_mult),
                       int(g_v * below_mult),
                       int(b_v * below_mult))
                draw.ellipse([cx - er, ring_top, cx + er, ring_bot], fill=dim)
                full = (r_v, g_v, b_v)
                for row_y in range(max(ring_top, 0), min(screen_mid_y, ring_bot)):
                    dy_r = row_y - cy
                    disc = 1.0 - (dy_r / er_y) ** 2
                    if disc <= 0:
                        continue
                    half_w = int(er * math.sqrt(disc))
                    if half_w > 0:
                        draw.line([(cx - half_w, row_y), (cx + half_w, row_y)],
                                  fill=full, width=1)


def draw_amber_outline(draw, cx, cy, rx, ry, width=3):
    for i in range(width):
        draw.ellipse(
            [cx - rx - i, cy - ry - i, cx + rx + i, cy + ry + i],
            outline=CORRUPTED_AMBER
        )


def draw_background(draw, img):
    rng = random.Random(42)
    ceiling_y = sy(int(1080 * 0.12))
    draw.rectangle([0, 0, W, ceiling_y], fill=(90, 55, 22))
    draw.line([(0, ceiling_y), (W, ceiling_y)], fill=(60, 36, 14), width=sp(4))

    wall_top_y = ceiling_y
    wall_bot_y = sy(int(1080 * 0.54))
    far_wall   = (228, 185, 120)
    base_wall  = (212, 146,  58)
    for y in range(wall_top_y, wall_bot_y):
        t = (y - wall_top_y) / max(1, wall_bot_y - wall_top_y)
        r_v = int(far_wall[0] + (base_wall[0] - far_wall[0]) * t)
        g_v = int(far_wall[1] + (base_wall[1] - far_wall[1]) * t)
        b_v = int(far_wall[2] + (base_wall[2] - far_wall[2]) * t)
        draw.line([(0, y), (W, y)], fill=(r_v, g_v, b_v))

    draw.rectangle([0, sy(int(1080 * 0.54)), W, sy(int(1080 * 0.75))], fill=(140, 90, 26))
    draw.line([(0, sy(int(1080 * 0.54))), (W, sy(int(1080 * 0.54)))], fill=(100, 64, 18), width=sp(3))
    draw.rectangle([0, sy(int(1080 * 0.75)), W, H], fill=(90, 56, 32))
    for y in range(sy(int(1080 * 0.75)), H, sp(28)):
        draw.line([(0, y), (W, y)], fill=RUST_SHADOW, width=1)
    for y in range(sy(int(1080 * 0.76)), H, sp(56)):
        draw.line([(0, y + sp(4)), (W, y + sp(4))], fill=(110, 70, 42), width=1)

    # Monitor wall
    mw_x  = sx(int(1920 * 0.50))
    mw_y  = ceiling_y + sp(5)
    mw_w  = sx(int(1920 * 0.46))
    mw_h  = sy(int(1080 * 0.57))
    draw.rectangle([mw_x, mw_y, mw_x + mw_w, mw_y + mw_h], fill=(14, 10, 22))

    _crt_y  = mw_y + int(mw_h * 0.08)
    _crt_h  = int(mw_h * 0.62)
    _scr_pad = sp(24)
    _scr_y0 = _crt_y + _scr_pad
    _scr_y1 = _crt_y + _crt_h - _scr_pad * 2
    crt_screen_mid_y = (_scr_y0 + _scr_y1) // 2

    monitor_specs = [
        (mw_x + sx(40),  mw_y + sy(20),  sx(260), sy(150)),
        (mw_x + sx(330), mw_y + sy(15),  sx(320), sy(180)),
        (mw_x + sx(680), mw_y + sy(28),  sx(230), sy(140)),
        (mw_x + sx(50),  mw_y + sy(190), sx(280), sy(165)),
        (mw_x + sx(360), mw_y + sy(215), sx(300), sy(170)),
        (mw_x + sx(685), mw_y + sy(185), sx(210), sy(150)),
    ]

    cx_glow = mw_x + mw_w // 2
    cy_glow = mw_y + mw_h // 2
    draw_filled_glow(draw, cx_glow, cy_glow,
                     rx=sx(720), ry=sy(420),
                     glow_rgb=(0, 60, 100),
                     bg_rgb=(14, 10, 22),
                     steps=16,
                     screen_mid_y=crt_screen_mid_y)

    for mx, my, mw_s, mh_s in monitor_specs:
        draw.rectangle([mx - sp(6), my - sp(6), mx + mw_s + sp(6), my + mh_s + sp(6)],
                       fill=(12, 10, 18), outline=(28, 22, 40), width=sp(2))
        draw.rectangle([mx, my, mx + mw_s, my + mh_s], fill=ELEC_CYAN)
        cx_m = mx + mw_s // 2
        cy_m = my + mh_s // 2
        draw_filled_glow(draw, cx_m, cy_m,
                         mw_s // 2, mh_s // 2,
                         glow_rgb=(180, 255, 255),
                         bg_rgb=ELEC_CYAN,
                         steps=8,
                         screen_mid_y=cy_m)
        for sy_scan in range(my + sp(3), my + mh_s, sp(5)):
            draw.line([(mx, sy_scan), (mx + mw_s, sy_scan)], fill=(0, 168, 180), width=1)
        draw.line([(mx, my), (mx + mw_s, my)], fill=(40, 40, 60), width=sp(2))

    # Ghost Byte
    ghost_screens = [monitor_specs[2], monitor_specs[3]]
    for gs_mx, gs_my, gs_mw, gs_mh in ghost_screens:
        ghost_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ghost_draw  = ImageDraw.Draw(ghost_layer)
        g_cx  = gs_mx + gs_mw // 2
        g_cy  = gs_my + gs_mh // 2 - int(gs_mh * 0.08)
        g_rx  = int(gs_mw * 0.28)
        g_ry  = int(gs_mh * 0.38)
        ghost_draw.ellipse([g_cx - g_rx, g_cy - g_ry, g_cx + g_rx, g_cy + g_ry],
                           fill=(0, 53, 58, 90))
        eye_y = g_cy - int(g_ry * 0.15)
        e_r   = max(2, int(g_rx * 0.20))
        ghost_draw.rectangle([g_cx - int(g_rx * 0.35) - e_r, eye_y - e_r,
                               g_cx - int(g_rx * 0.35) + e_r, eye_y + e_r],
                              fill=(0, 220, 240, 105))
        ghost_draw.ellipse([g_cx + int(g_rx * 0.20) - e_r, eye_y - e_r,
                            g_cx + int(g_rx * 0.20) + e_r, eye_y + e_r],
                           fill=(0, 220, 240, 105))
        base_rgba = img.convert("RGBA")
        img_with_ghost = Image.alpha_composite(base_rgba, ghost_layer)
        img.paste(img_with_ghost.convert("RGB"))
    draw = ImageDraw.Draw(img)

    # CRT screen
    crt_x  = mw_x + int(mw_w * 0.22)
    crt_y  = mw_y + int(mw_h * 0.08)
    crt_w  = int(mw_w * 0.52)
    crt_h  = int(mw_h * 0.62)

    crt_frame_pts = [
        (crt_x - sp(10), crt_y - sp(10)),
        (crt_x + crt_w + sp(10), crt_y - sp(10)),
        (crt_x + crt_w + sp(10), crt_y + crt_h + sp(20)),
        (crt_x - sp(10), crt_y + crt_h + sp(20)),
    ]
    wobble_polygon(draw, crt_frame_pts, color=(44, 36, 56),
                   width=sp(3), amplitude=sp(2), frequency=4, seed=200,
                   fill=(44, 36, 56))

    draw.rectangle([crt_x + crt_w // 3, crt_y + crt_h + sp(18),
                    crt_x + crt_w * 2 // 3, crt_y + crt_h + sp(40)],
                   fill=(36, 28, 46))
    scr_pad = sp(24)
    scr_x0  = crt_x + scr_pad
    scr_y0  = crt_y + scr_pad
    scr_x1  = crt_x + crt_w - scr_pad
    scr_y1  = crt_y + crt_h - scr_pad * 2
    draw.rectangle([scr_x0, scr_y0, scr_x1, scr_y1], fill=ELEC_CYAN)

    scr_mid_x = (scr_x0 + scr_x1) // 2
    scr_mid_y_s = (scr_y0 + scr_y1) // 2
    grid_color = (0, 168, 180)
    for i in range(1, 6):
        t = i / 5.0
        lx = int(scr_x0 + (scr_mid_x - scr_x0) * t)
        rx = int(scr_x1 - (scr_x1 - scr_mid_x) * t)
        draw.line([(lx, scr_y0), (scr_mid_x, scr_mid_y_s)], fill=grid_color, width=1)
        draw.line([(rx, scr_y0), (scr_mid_x, scr_mid_y_s)], fill=grid_color, width=1)
    for i in range(1, 5):
        t = i / 4.0
        ty = int(scr_y0 + (scr_mid_y_s - scr_y0) * t)
        draw.line([(scr_x0, ty), (scr_mid_x, scr_mid_y_s)], fill=grid_color, width=1)
        draw.line([(scr_x1, ty), (scr_mid_x, scr_mid_y_s)], fill=grid_color, width=1)

    scr_rng = random.Random(99)
    fig_x = scr_x0 + sp(14)
    fig_y = scr_y0 + sp(12)
    fig_color = (0, 80, 100)
    draw.rectangle([fig_x + sp(5), fig_y,      fig_x + sp(10), fig_y + sp(4)],  fill=fig_color)
    draw.rectangle([fig_x + sp(3), fig_y + sp(4),  fig_x + sp(12), fig_y + sp(9)],  fill=fig_color)
    draw.rectangle([fig_x,         fig_y + sp(4),  fig_x + sp(3),  fig_y + sp(6)],  fill=fig_color)
    draw.rectangle([fig_x + sp(12), fig_y + sp(4), fig_x + sp(15), fig_y + sp(6)],  fill=fig_color)
    draw.rectangle([fig_x + sp(3),  fig_y + sp(9), fig_x + sp(6),  fig_y + sp(14)], fill=fig_color)
    draw.rectangle([fig_x + sp(9),  fig_y + sp(9), fig_x + sp(12), fig_y + sp(14)], fill=fig_color)

    fig_x2 = scr_x1 - sp(30)
    fig_y2 = scr_y0 + sp(10)
    fig_color2 = (0, 60, 80)
    draw.rectangle([fig_x2 + sp(5), fig_y2,      fig_x2 + sp(10), fig_y2 + sp(4)],  fill=fig_color2)
    draw.rectangle([fig_x2 + sp(3), fig_y2 + sp(4), fig_x2 + sp(12), fig_y2 + sp(9)],  fill=fig_color2)
    draw.rectangle([fig_x2 - sp(6), fig_y2 + sp(4), fig_x2 + sp(3), fig_y2 + sp(6)],   fill=fig_color2)
    draw.rectangle([fig_x2 + sp(12), fig_y2 + sp(4), fig_x2 + sp(15), fig_y2 + sp(6)], fill=fig_color2)
    draw.rectangle([fig_x2 + sp(3),  fig_y2 + sp(9), fig_x2 + sp(6),  fig_y2 + sp(14)], fill=fig_color2)
    draw.rectangle([fig_x2 + sp(9),  fig_y2 + sp(9), fig_x2 + sp(12), fig_y2 + sp(14)], fill=fig_color2)

    for _ in range(28):
        px_x = scr_x0 + scr_rng.randint(0, scr_x1 - scr_x0)
        px_y = scr_y0 + scr_rng.randint(0, scr_y1 - scr_y0)
        dist_from_center = ((px_x - scr_mid_x) ** 2 + (px_y - scr_mid_y_s) ** 2) ** 0.5
        min_dist = min(scr_x1 - scr_x0, scr_y1 - scr_y0) * 0.30
        if dist_from_center > min_dist:
            ps = scr_rng.choice([2, 3])
            pc = scr_rng.choice([(0, 100, 120), (0, 60, 80), (0, 140, 160)])
            draw.rectangle([px_x, px_y, px_x + ps, px_y + ps], fill=pc)

    emerge_cx = (scr_x0 + scr_x1) // 2
    emerge_cy = (scr_y0 + scr_y1) // 2
    emerge_rx = int((scr_x1 - scr_x0) * 0.34)
    emerge_ry = int((scr_y1 - scr_y0) * 0.44)
    draw.ellipse([emerge_cx - emerge_rx, emerge_cy - emerge_ry,
                  emerge_cx + emerge_rx, emerge_cy + emerge_ry],
                 fill=(14, 14, 30))
    draw.ellipse([emerge_cx - emerge_rx - sp(8), emerge_cy - emerge_ry - sp(8),
                  emerge_cx + emerge_rx + sp(8), emerge_cy + emerge_ry + sp(8)],
                 outline=DEEP_CYAN, width=sp(4))
    draw.ellipse([emerge_cx - emerge_rx - sp(14), emerge_cy - emerge_ry - sp(14),
                  emerge_cx + emerge_rx + sp(14), emerge_cy + emerge_ry + sp(14)],
                 outline=(0, 80, 100), width=sp(2))
    draw.rectangle([scr_x0, scr_y0, scr_x1, scr_y1], outline=DEEP_CYAN, width=sp(5))
    for sy_scan in range(scr_y0 + sp(4), scr_y1, sp(7)):
        draw.line([(scr_x0, sy_scan), (scr_x1, sy_scan)], fill=(0, 168, 180), width=1)

    rng_confetti = random.Random(42)
    for _ in range(80):
        px = rng_confetti.randint(scr_x0 - sx(120), scr_x1 + sx(60))
        py = rng_confetti.randint(scr_y0 - sy(80), sy(int(1080 * 0.75)))
        ps = rng_confetti.choice([3, 4, 5, 6])
        pc = rng_confetti.choice([ELEC_CYAN, STATIC_WHITE, BYTE_TEAL, (0, 200, 220)])
        draw.rectangle([px, py, px + ps, py + ps], fill=pc)

    floor_glow_pts = [
        (crt_x,            sy(int(1080 * 0.75))),
        (crt_x + crt_w,    sy(int(1080 * 0.75))),
        (crt_x + crt_w + sx(160), H),
        (crt_x - sx(100),  H),
    ]
    _floor_mult = 0.70
    draw.polygon(floor_glow_pts, fill=(0, int(22 * _floor_mult), int(38 * _floor_mult)))
    draw_filled_glow(draw, mw_x - sp(20), mw_y + mw_h // 2,
                     rx=sx(160), ry=sy(220),
                     glow_rgb=(0, 40, 70),
                     bg_rgb=(180, 130, 60),
                     steps=10,
                     screen_mid_y=crt_screen_mid_y)

    # Window
    win_x0, win_y0 = sx(60), ceiling_y + sy(20)
    win_x1, win_y1 = sx(340), ceiling_y + sy(260)
    draw.rectangle([win_x0 - sx(30), win_y0 - sy(10), win_x0 + sx(14), win_y1 + sy(20)], fill=(168, 108, 48))
    draw.rectangle([win_x1 - sx(14), win_y0 - sy(10), win_x1 + sx(30), win_y1 + sy(20)], fill=(168, 108, 48))
    draw.rectangle([win_x0, win_y0, win_x1, win_y1], fill=SOFT_GOLD)
    draw.rectangle([win_x0, win_y0, win_x1, win_y1], outline=DEEP_COCOA, width=sp(4))
    mid_win_x = (win_x0 + win_x1) // 2
    mid_win_y = (win_y0 + win_y1) // 2
    draw.line([(mid_win_x, win_y0), (mid_win_x, win_y1)], fill=DEEP_COCOA, width=sp(3))
    draw.line([(win_x0, mid_win_y), (win_x1, mid_win_y)], fill=DEEP_COCOA, width=sp(3))

    # Bookshelves
    shelf_x = sx(int(1920 * 0.20))
    shelf_y = ceiling_y
    shelf_w = sx(int(1920 * 0.28))
    shelf_h = sy(int(1080 * 0.45))
    draw.rectangle([shelf_x, shelf_y, shelf_x + shelf_w, shelf_y + shelf_h], fill=SUNLIT_AMBER)
    book_colors = [TERRACOTTA, SAGE_GREEN, DUSTY_LAVENDER, OCHRE_BRICK,
                   RUST_SHADOW, (96, 144, 180), (184, 160, 100)]
    rng_books = random.Random(42)
    for row in range(shelf_y + sp(4), shelf_y + shelf_h, sy(50)):
        draw.line([(shelf_x, row + sy(44)), (shelf_x + shelf_w, row + sy(44))], fill=DEEP_COCOA, width=sp(2))
        bx = shelf_x + sp(8)
        col_idx = 0
        while bx + sp(20) < shelf_x + shelf_w:
            bw = rng_books.randint(sx(18), sx(36))
            bc = book_colors[col_idx % len(book_colors)]
            draw.rectangle([bx, row + sp(4), bx + bw, row + sy(42)], fill=bc)
            draw.line([(bx, row + sp(4)), (bx, row + sy(42))], fill=DEEP_COCOA, width=1)
            bx += bw + sp(2)
            col_idx += 1

    # Desk
    desk_y = sy(int(1080 * 0.60))
    desk_x0 = mw_x - sx(80)
    desk_x1 = W
    draw.rectangle([desk_x0, desk_y, desk_x1, desk_y + sy(70)], fill=OCHRE_BRICK)
    draw.line([(desk_x0, desk_y), (desk_x1, desk_y)], fill=DEEP_COCOA, width=sp(3))
    draw.rectangle([desk_x0 + sx(30), desk_y + sy(10), desk_x0 + sx(240), desk_y + sy(46)],
                   fill=DUSTY_LAVENDER, outline=DEEP_COCOA, width=sp(2))
    for ky in range(desk_y + sy(16), desk_y + sy(40), sy(10)):
        for kx in range(desk_x0 + sx(38), desk_x0 + sx(234), sx(18)):
            draw.rectangle([kx, ky, kx + sx(14), ky + sy(7)], fill=(148, 135, 175))
    draw.rectangle([desk_x0 + sx(260), desk_y + sy(8), desk_x0 + sx(310), desk_y + sy(55)],
                   fill=TERRACOTTA, outline=DEEP_COCOA, width=sp(2))
    draw.arc([desk_x0 + sx(308), desk_y + sy(20), desk_x0 + sx(332), desk_y + sy(44)],
             start=270, end=90, fill=DEEP_COCOA, width=sp(3))
    cable_colors = [ELEC_CYAN, HOT_MAGENTA, CABLE_BRONZE, CABLE_DATA_CYAN]
    for ci, cc in enumerate(cable_colors):
        cx_s = desk_x0 + sx(40) + ci * sx(60)
        cx_e = desk_x0 + sx(120) + ci * sx(80)
        draw.arc([cx_s, desk_y + sy(50), cx_e, desk_y + sy(100)], 0, 180, fill=cc, width=sp(2))

    # Lamp
    lamp_x = sx(int(1920 * 0.40))
    lamp_y = ceiling_y + sy(18)
    draw_filled_glow(draw, lamp_x + sx(32), lamp_y + sy(50),
                     rx=sx(180), ry=sy(110),
                     glow_rgb=LAMP_PEAK,
                     bg_rgb=base_wall,
                     steps=12)
    draw.rectangle([lamp_x, lamp_y, lamp_x + sx(64), lamp_y + sy(86)],
                   fill=(245, 200, 66), outline=DEEP_COCOA, width=sp(2))
    draw.ellipse([lamp_x + sx(12), lamp_y + sy(80), lamp_x + sx(52), lamp_y + sy(96)],
                 fill=SUNLIT_AMBER)
    draw_filled_glow(draw, lamp_x + sx(32), sy(int(1080 * 0.85)),
                     rx=sx(120), ry=sy(44),
                     glow_rgb=LAMP_PEAK,
                     bg_rgb=(90, 56, 32),
                     steps=10)

    # Cable clutter foreground
    draw.rectangle([0, sy(int(1080 * 0.92)), W, H], fill=(42, 26, 16))
    fg_cables = [
        (sx(80),   sx(460),  sy(int(1080*0.935)), sy(60),  ELEC_CYAN,          2),
        (sx(240),  sx(780),  sy(int(1080*0.950)), sy(85),  HOT_MAGENTA,        2),
        (sx(420),  sx(980),  sy(int(1080*0.930)), sy(44),  CABLE_BRONZE,       2),
        (sx(600),  sx(1200), sy(int(1080*0.960)), sy(70),  CABLE_DATA_CYAN,    1),
        (sx(840),  sx(1500), sy(int(1080*0.940)), sy(92),  SOFT_GOLD,          2),
        (sx(980),  sx(1720), sy(int(1080*0.952)), sy(52),  CABLE_MAG_PURP,     1),
        (sx(1200), sx(1880), sy(int(1080*0.928)), sy(74),  ELEC_CYAN,          2),
        (sx(1460), sx(1920), sy(int(1080*0.962)), sy(38),  HOT_MAGENTA,        1),
        (sx(100),  sx(600),  sy(int(1080*0.970)), sy(32),  CABLE_NEUTRAL_PLUM, 1),
    ]
    for x0c, x1c, base_yc, arc_r, color, thickness in fg_cables:
        pts = []
        for s in range(31):
            t = s / 30
            px_c = int(x0c + (x1c - x0c) * t)
            sag = int(arc_r * 4 * t * (1 - t))
            pts.append((px_c, base_yc + sag))
        for i in range(len(pts) - 1):
            draw.line([pts[i], pts[i+1]], fill=color, width=thickness)

    # Mid-air transition element
    air_rng = random.Random(77)
    zone_x0 = sx(int(1920 * 0.40))
    zone_x1 = sx(int(1920 * 0.50))
    zone_mid = (zone_x0 + zone_x1) // 2
    for _ in range(60):
        px = air_rng.randint(zone_x0 - sx(20), zone_x1 + sx(20))
        py = air_rng.randint(sy(200), sy(700))
        ps = air_rng.choice([3, 4, 5, 6])
        if px < zone_mid:
            pc = air_rng.choice([SOFT_GOLD, SUNLIT_AMBER, (245, 200, 66), WARM_CREAM])
        else:
            pc = air_rng.choice([ELEC_CYAN, BYTE_TEAL, DEEP_CYAN, STATIC_WHITE])
        draw.rectangle([px, py, px + ps, py + ps], fill=pc)

    return {
        "scr_x0": scr_x0, "scr_y0": scr_y0,
        "scr_x1": scr_x1, "scr_y1": scr_y1,
        "emerge_cx": emerge_cx, "emerge_cy": emerge_cy,
        "emerge_rx": emerge_rx, "emerge_ry": emerge_ry,
        "mw_x": mw_x, "mw_y": mw_y, "mw_w": mw_w, "mw_h": mw_h,
        "ceiling_y": ceiling_y,
        "lamp_x": lamp_x, "lamp_y": lamp_y,
        "base_wall": base_wall,
    }


def draw_couch(draw, luma_cx, luma_base_y):
    couch_left  = sx(int(1920 * 0.16))
    couch_right = sx(int(1920 * 0.38))
    couch_y_bot = luma_base_y + sp(44)
    couch_y_top = luma_base_y - sp(40)

    seat_pts = [
        (couch_left,  couch_y_bot + sp(10)), (couch_left,  couch_y_bot - sp(60)),
        (couch_right, couch_y_top - sp(40)), (couch_right, couch_y_bot + sp(4)),
    ]
    wobble_polygon(draw, seat_pts, color=(70, 30, 14),
                   width=sp(3), amplitude=sp(2), frequency=4, seed=400,
                   fill=(107, 48, 24))

    mid_couch_x = (couch_left + couch_right) // 2
    draw.line([(mid_couch_x - sp(10), couch_y_bot - sp(20)), (mid_couch_x, couch_y_top - sp(30))],
              fill=(80, 36, 14), width=sp(2))

    back_left_inner = sx(int(1920 * 0.22))
    back_pts = [
        (couch_left, couch_y_bot - sp(60)), (couch_left, couch_y_bot - sp(150)),
        (back_left_inner, couch_y_top - sp(120)), (back_left_inner, couch_y_top - sp(50)),
    ]
    wobble_polygon(draw, back_pts, color=(80, 40, 16),
                   width=sp(2), amplitude=sp(2), frequency=3, seed=401,
                   fill=(128, 60, 28))

    arm_pts = [
        (couch_right, couch_y_bot + sp(4)), (couch_right, couch_y_bot - sp(70)),
        (couch_right + sp(40), couch_y_bot - sp(60)), (couch_right + sp(40), couch_y_bot + sp(14)),
    ]
    wobble_polygon(draw, arm_pts, color=(80, 36, 14),
                   width=sp(2), amplitude=sp(1), frequency=3, seed=402,
                   fill=(115, 52, 26))

    draw.line([(couch_left, couch_y_bot - sp(60)), (couch_left, couch_y_bot + sp(10))],
              fill=SOFT_GOLD, width=sp(4))


# ═══════════════════════════════════════════════════════════════════════════
# PYCAIRO CHARACTER RENDERING — Luma (C52)
# ═══════════════════════════════════════════════════════════════════════════

def draw_luma_cairo(luma_cx, luma_base_y, facing_monitor_x, byte_cx_target,
                    byte_cy_target, crt_cx):
    """Draw Luma using pycairo bezier curves. Returns RGBA PIL image + geometry dict.

    Scene-lit: CRT tint on skin/hoodie, cyan catch-lights, shoulder involvement.
    """
    surface, ctx, w_px, h_px = create_surface(W, H, scale=1)

    luma_x = luma_cx
    y_base = luma_base_y
    lean_offset = sp(44)

    # ── Jeans (scene-lit) ──
    jeans_crt = blend_color(JEANS, SCENE_COOL_TINT, 0.08)
    jeans_shadow = blend_color(JEANS_SH, SCENE_WARM_TINT, 0.05)

    # Left leg (away-side — warm shadow)
    ctx.new_path()
    draw_smooth_polygon(ctx, [
        (luma_x - sp(48), y_base), (luma_x - sp(50), y_base - sp(88)),
        (luma_x - sp(15), y_base - sp(90)), (luma_x - sp(20), y_base),
    ], bulge_frac=0.04)
    set_color(ctx, jeans_shadow)
    ctx.fill()

    # Right leg (CRT-side — brighter)
    ctx.new_path()
    draw_smooth_polygon(ctx, [
        (luma_x + sp(14), y_base), (luma_x + sp(12), y_base - sp(86)),
        (luma_x + sp(46), y_base - sp(84)), (luma_x + sp(44), y_base - sp(4)),
    ], bulge_frac=0.04)
    set_color(ctx, jeans_crt)
    ctx.fill()

    # Shoes
    for shoe_x0, shoe_x1 in [(luma_x - sp(60), luma_x - sp(8)),
                               (luma_x + sp(2), luma_x + sp(58))]:
        ctx.rectangle(shoe_x0, y_base - sp(10), shoe_x1 - shoe_x0, sp(32))
        set_color(ctx, WARM_CREAM)
        ctx.fill()
        ctx.rectangle(shoe_x0 - sp(2), y_base + sp(16), shoe_x1 - shoe_x0 + sp(4), sp(10))
        set_color(ctx, DEEP_COCOA)
        ctx.fill()

    # ── Torso (scene-lit hoodie with gradient via cairo linear gradient) ──
    torso_top = y_base - sp(260)
    torso_bot = y_base - sp(90)
    torso_half_w = sp(44)

    # Build torso as a filled shape with hoodie gradient
    # The lean makes the top offset to the right
    tl = (luma_x - torso_half_w + lean_offset, torso_top)
    tr = (luma_x + torso_half_w + lean_offset, torso_top)
    br = (luma_x + torso_half_w, torso_bot)
    bl = (luma_x - torso_half_w, torso_bot)

    # C47 shoulder involvement: screen-side shoulder raised
    # CRT-facing shoulder rises 5px, shifts outward 6px
    shoulder_raise = sp(5)
    shoulder_out = sp(6)
    tr_adj = (tr[0] + shoulder_out, tr[1] - shoulder_raise)

    ctx.new_path()
    draw_smooth_polygon(ctx, [tl, tr_adj, br, bl], bulge_frac=0.06)

    # Linear gradient: warm shadow (left/away-side) to CRT-lit hoodie (right)
    hoodie_crt = blend_color(HOODIE_ORANGE, SCENE_COOL_TINT, 0.25)
    hoodie_warm = blend_color(HOODIE_SHADOW, SCENE_WARM_TINT, 0.12)
    pat = cairo.LinearGradient(bl[0], torso_top, br[0], torso_top)
    pat.add_color_stop_rgb(0.0, *_c(hoodie_warm))
    pat.add_color_stop_rgb(0.4, *_c(HOODIE_ORANGE))
    pat.add_color_stop_rgb(1.0, *_c(hoodie_crt))
    ctx.set_source(pat)
    ctx.fill()

    # Hoodie bottom band
    ctx.rectangle(luma_x - torso_half_w, torso_bot - sp(8),
                  torso_half_w * 2, sp(8))
    set_color(ctx, HOODIE_AMBIENT)
    ctx.fill()

    # Hoodie pixel pattern squares (C38: 12 pixels)
    rng_px = random.Random(55)
    for i in range(12):
        ppx = luma_x - torso_half_w + lean_offset + rng_px.randint(sp(2), torso_half_w * 2 - sp(6))
        ppy = torso_top + rng_px.randint(sp(4), sp(50))
        pps = rng_px.choice([sp(4), sp(6), sp(8)])
        col_choices = [ELEC_CYAN, BYTE_TEAL, (0, 200, 220), (0, 240, 240)]
        pc = rng_px.choice(col_choices)
        ctx.rectangle(ppx, ppy, pps, pps)
        set_color(ctx, pc)
        ctx.fill()

    # ── Neck ──
    head_cx = luma_x + lean_offset
    head_cy = torso_top - sp(70)
    ctx.rectangle(head_cx - sp(6), torso_top, sp(12), sp(30))
    set_color(ctx, HOODIE_ORANGE)
    ctx.fill()

    # Neck visible skin
    for row in range(torso_top + sp(2), head_cy + sp(60)):
        t_n = (row - (torso_top + sp(2))) / max(1, (head_cy + sp(60)) - (torso_top + sp(2)))
        half_w_n = sp(18) - int(t_n * sp(4))
        ctx.rectangle(luma_x - half_w_n + int(t_n * sp(4)), row, half_w_n * 2, 1)
        set_color(ctx, HOODIE_ORANGE)
        ctx.fill()

    # ── Reaching arm (C38) — scene-lit ──
    arm_shoulder_x = luma_x - sp(10) + lean_offset
    arm_shoulder_y = torso_top + sp(25)
    arm_target_x = facing_monitor_x - sp(10)
    arm_target_y = torso_top + sp(45)
    elbow_x = (arm_shoulder_x + arm_target_x) // 2 + sp(16)
    elbow_y = arm_shoulder_y - sp(32)

    arm_color_crt = blend_color(CYAN_SKIN, SCENE_COOL_TINT, 0.20)
    arm_w = sp(18)

    # Upper arm
    _draw_tapered_limb_cairo(ctx, arm_shoulder_x, arm_shoulder_y,
                              elbow_x, elbow_y, arm_w, arm_w - sp(2), arm_color_crt)
    # Forearm
    _draw_tapered_limb_cairo(ctx, elbow_x, elbow_y,
                              arm_target_x, arm_target_y, arm_w - sp(2), arm_w - sp(4), arm_color_crt)

    hand_cx = arm_target_x
    hand_cy = arm_target_y

    # Hand — open palm
    draw_ellipse(ctx, hand_cx, hand_cy + sp(4), sp(14), sp(14))
    set_color(ctx, arm_color_crt)
    ctx.fill()

    # Fingers (C38 — spread open, reaching)
    finger_offsets = [(-sp(12), -sp(20)), (-sp(6), -sp(24)), (sp(2), -sp(24)), (sp(10), -sp(20))]
    for fdx, fdy in finger_offsets:
        ctx.set_line_width(sp(6))
        ctx.move_to(hand_cx + fdx // 2, hand_cy - sp(4))
        ctx.line_to(hand_cx + fdx, hand_cy + fdy)
        set_color(ctx, arm_color_crt)
        ctx.stroke()
    # Thumb
    ctx.set_line_width(sp(6))
    ctx.move_to(hand_cx - sp(12), hand_cy + sp(6))
    ctx.line_to(hand_cx - sp(22), hand_cy - sp(4))
    set_color(ctx, arm_color_crt)
    ctx.stroke()

    # Palm CRT glow particles
    rng_palm = random.Random(91)
    for _ in range(8):
        px_g = hand_cx + rng_palm.randint(-sp(14), sp(14))
        py_g = hand_cy + rng_palm.randint(-sp(10), sp(6))
        ps_g = rng_palm.choice([2, 3, 4])
        pc = rng_palm.choice([ELEC_CYAN, (180, 240, 255), BYTE_TEAL])
        ctx.rectangle(px_g, py_g, ps_g, ps_g)
        set_color(ctx, pc)
        ctx.fill()

    # ── Head (scene-lit with pycairo) ──
    head_gaze_offset = sp(18)
    head_cx_final = head_cx + head_gaze_offset
    head_cy_final = head_cy + sp(6)
    scale_h = 0.92
    def p(n): return int(n * scale_h * min(SX, SY))
    head_r = p(72)

    # Head fill — scene-lit gradient (CRT side cyan, away side warm)
    skin_crt = blend_color(SKIN_HL, SCENE_COOL_TINT, SCENE_COOL_INFLUENCE)
    skin_warm = blend_color(SKIN_SH, SCENE_WARM_TINT, SCENE_WARM_INFLUENCE)

    draw_ellipse(ctx, head_cx_final, head_cy_final, head_r, head_r)
    pat_head = cairo.LinearGradient(head_cx_final - head_r, head_cy_final,
                                     head_cx_final + head_r, head_cy_final)
    pat_head.add_color_stop_rgb(0.0, *_c(skin_warm))
    pat_head.add_color_stop_rgb(0.5, *_c(SKIN))
    pat_head.add_color_stop_rgb(1.0, *_c(skin_crt))
    ctx.set_source(pat_head)
    ctx.fill()

    # Head outline — wobble via draw_wobble_path
    num_pts = 24
    head_pts = []
    for i in range(num_pts):
        angle = (2 * math.pi * i / num_pts) - math.pi / 2
        hx = head_cx_final + head_r * math.cos(angle)
        hy = head_cy_final + head_r * math.sin(angle)
        head_pts.append((hx, hy))

    draw_wobble_path(ctx, head_pts, amplitude=sp(2), frequency=0.15,
                     seed=101, closed=True, jitter=0.5)
    ctx.set_line_width(sp(3))
    set_color(ctx, LINE)
    ctx.stroke()

    # Hair base
    draw_ellipse(ctx, head_cx_final, head_cy_final - head_r * 0.15, head_r, head_r * 0.55)
    set_color(ctx, HAIR_COLOR)
    ctx.fill()

    # ── Eyes (C38 + C47 sight-line geometry) ──
    EYE_W_C = (242, 240, 248)
    EYE_IRIS = (58, 32, 18)
    EYE_PUP  = (20, 12, 8)

    lex = head_cx_final + p(4)
    ley = head_cy_final - p(10)
    ew  = int(head_r * 0.22)
    leh = p(34)

    # Screen-side eye (wider — wonder)
    draw_ellipse(ctx, lex, ley, ew, leh)
    set_color(ctx, EYE_W_C)
    ctx.fill()
    draw_ellipse(ctx, lex, ley, ew, leh)
    ctx.set_line_width(sp(2))
    set_color(ctx, LINE)
    ctx.stroke()

    # Iris
    iris_r = p(15)
    draw_ellipse(ctx, lex, ley + p(2), iris_r, iris_r)
    set_color(ctx, EYE_IRIS)
    ctx.fill()
    # Pupil
    draw_ellipse(ctx, lex, ley + p(1), p(9), p(8))
    set_color(ctx, EYE_PUP)
    ctx.fill()
    # Catch-light — cyan-tinted (scene-lit)
    draw_ellipse(ctx, lex + p(6), ley - p(6), p(4), p(4))
    set_color(ctx, (180, 255, 255))
    ctx.fill()

    # Away-side eye (squinted — intensity)
    rex = head_cx_final + p(38)
    rey = head_cy_final - p(8)
    reh = p(22)

    draw_ellipse(ctx, rex, rey, ew, reh)
    set_color(ctx, EYE_W_C)
    ctx.fill()
    draw_ellipse(ctx, rex, rey, ew, reh)
    ctx.set_line_width(sp(2))
    set_color(ctx, LINE)
    ctx.stroke()

    # Iris
    draw_ellipse(ctx, rex, rey + p(2), iris_r, iris_r)
    set_color(ctx, EYE_IRIS)
    ctx.fill()

    # C47 sight-line fix: pupil shift aimed at Byte
    mid_eye_x = (lex + rex) // 2
    mid_eye_y = (ley + rey) // 2
    _byte_cy = byte_cy_target if byte_cy_target is not None else mid_eye_y
    aim_dx = byte_cx_target - mid_eye_x
    aim_dy = _byte_cy - mid_eye_y
    aim_dist = max(1, (aim_dx**2 + aim_dy**2) ** 0.5)
    pupil_mag = p(8)
    psx = int(pupil_mag * aim_dx / aim_dist)
    psy = int(pupil_mag * aim_dy / aim_dist)

    # Away-side pupil + catch-light
    draw_ellipse(ctx, rex + psx, rey + psy + p(1), p(9), p(8))
    set_color(ctx, EYE_PUP)
    ctx.fill()
    draw_ellipse(ctx, rex + psx + p(6), rey + psy - p(6), p(4), p(4))
    set_color(ctx, (180, 255, 255))
    ctx.fill()

    # Screen-side pupil shifted too
    draw_ellipse(ctx, lex + psx, ley + psy + p(1), p(9), p(8))
    set_color(ctx, EYE_PUP)
    ctx.fill()

    # ── Brows (C38) ──
    # Screen-side brow — raised high (wonder)
    ctx.set_line_width(p(6))
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.move_to(lex - p(30), ley - p(54))
    ctx.curve_to(lex - p(15), ley - p(64), lex + p(5), ley - p(62), lex + p(22), ley - p(46))
    set_color(ctx, HAIR_COLOR)
    ctx.stroke()

    # Away-side brow — doubt variant
    ctx.set_line_width(p(5))
    ctx.move_to(rex - p(22), rey - p(38))
    ctx.curve_to(rex - p(12), rey - p(36), rex + p(5), rey - p(32), rex + p(26), rey - p(26))
    set_color(ctx, HAIR_COLOR)
    ctx.stroke()

    # ── Nose ──
    draw_ellipse(ctx, head_cx_final - p(3), head_cy_final + p(11), p(3), p(3))
    set_color(ctx, SKIN_SH)
    ctx.fill()
    draw_ellipse(ctx, head_cx_final + p(5) + p(4), head_cy_final + p(11), p(3), p(3))
    set_color(ctx, SKIN_SH)
    ctx.fill()

    # ── Mouth (C38 — barely parted, held breath) ──
    m_off = p(2)
    ctx.set_line_width(p(3))
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    # Upper lip arc
    ctx.new_path()
    m_cx = head_cx_final + m_off
    m_cy = head_cy_final + p(35)
    ctx.move_to(m_cx - p(28), m_cy)
    ctx.curve_to(m_cx - p(14), m_cy - p(6), m_cx + p(14), m_cy - p(6), m_cx + p(28), m_cy)
    set_color(ctx, LINE)
    ctx.stroke()

    # Lip fill (pale interior)
    ctx.new_path()
    ctx.move_to(m_cx - p(24), m_cy)
    ctx.curve_to(m_cx - p(12), m_cy + p(10), m_cx + p(12), m_cy + p(10), m_cx + p(24), m_cy)
    ctx.close_path()
    set_color(ctx, (240, 212, 190))
    ctx.fill()

    # Thin parting line
    ctx.set_line_width(p(1))
    ctx.move_to(m_cx - p(10), m_cy + p(2))
    ctx.line_to(m_cx + p(10), m_cy + p(2))
    set_color(ctx, (160, 100, 60))
    ctx.stroke()

    # ── Blush ──
    draw_ellipse(ctx, head_cx_final - head_r + p(34), head_cy_final + p(22), p(28), p(18))
    ctx.set_source_rgba(*_ca((*BLUSH_LEFT, 80)))
    ctx.fill()
    draw_ellipse(ctx, head_cx_final + head_r - p(34), head_cy_final + p(22), p(28), p(18))
    ctx.set_source_rgba(*_ca((*BLUSH_RIGHT, 80)))
    ctx.fill()

    # ── Hair strands (C38 — screen-side forward pull) ──
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)

    # Strand 1: away-side arc (counterweight float-back)
    ctx.set_line_width(p(8))
    ctx.new_path()
    ctx.arc(head_cx_final - p(35), head_cy_final - p(168), p(25), math.radians(30), math.radians(200))
    set_color(ctx, HAIR_COLOR)
    ctx.stroke()

    # Strand 2: screen-side arc (forward pull toward CRT)
    ctx.set_line_width(p(7))
    ctx.new_path()
    ctx.arc(head_cx_final + p(35), head_cy_final - p(150), p(35), math.radians(330), math.radians(545))
    set_color(ctx, HAIR_COLOR)
    ctx.stroke()

    # Strand 3: crown tuft (upward energy)
    ctx.set_line_width(p(6))
    ctx.new_path()
    ctx.arc(head_cx_final, head_cy_final - p(180), p(20), math.radians(225), math.radians(355))
    set_color(ctx, HAIR_COLOR)
    ctx.stroke()

    # Strand 4: fine trailing wisp
    ctx.set_line_width(p(4))
    ctx.new_path()
    ctx.arc(head_cx_final + p(43), head_cy_final - p(148), p(25), math.radians(290), math.radians(495))
    set_color(ctx, HAIR_COLOR)
    ctx.stroke()

    # Hair edge highlight from CRT — cyan fringe (key anti-cutout detail)
    ctx.set_line_width(p(2))
    ctx.new_path()
    ctx.arc(head_cx_final + p(42), head_cy_final - p(150), p(32), math.radians(310), math.radians(520))
    set_color(ctx, (0, 180, 200))
    ctx.stroke()

    # ── Collar ──
    collar_offset = p(6)
    draw_ellipse(ctx, head_cx_final + collar_offset, head_cy_final + head_r + p(45),
                 p(90), p(35))
    set_color(ctx, HOODIE_ORANGE)
    ctx.fill()
    # Collar outline (lower half arc)
    ctx.new_path()
    ctx.save()
    ctx.translate(head_cx_final + collar_offset, head_cy_final + head_r + p(45))
    ctx.scale(p(90), p(35))
    ctx.arc(0, 0, 1.0, 0, math.pi)
    ctx.restore()
    ctx.set_line_width(p(3))
    set_color(ctx, LINE)
    ctx.stroke()

    # Convert cairo surface to PIL RGBA
    luma_img = to_pil_rgba(surface)

    return luma_img, {
        "head_cx": head_cx_final, "head_cy": head_cy_final,
        "head_r": head_r,
        "hand_cx": hand_cx, "hand_cy": hand_cy,
        "torso_top": torso_top,
        "torso_half_w": torso_half_w,
        "lean_offset": lean_offset,
    }


def _draw_tapered_limb_cairo(ctx, x0, y0, x1, y1, w0, w1, color):
    """Draw a tapered limb segment using cairo bezier envelope."""
    dx = x1 - x0
    dy = y1 - y0
    length = math.sqrt(dx * dx + dy * dy) or 1.0
    nx = -dy / length
    ny = dx / length
    hw0 = w0 / 2.0
    hw1 = w1 / 2.0

    ctx.new_path()
    ctx.move_to(x0 + nx * hw0, y0 + ny * hw0)
    # Slight outward curve on left side
    mx = (x0 + x1) / 2.0 + nx * (hw0 + hw1) * 0.3
    my = (y0 + y1) / 2.0 + ny * (hw0 + hw1) * 0.3
    ctx.curve_to(x0 + nx * hw0 + dx * 0.33, y0 + ny * hw0 + dy * 0.33,
                 mx, my,
                 x1 + nx * hw1, y1 + ny * hw1)
    # End cap
    ctx.line_to(x1 - nx * hw1, y1 - ny * hw1)
    # Right side back
    mx2 = (x0 + x1) / 2.0 - nx * (hw0 + hw1) * 0.3
    my2 = (y0 + y1) / 2.0 - ny * (hw0 + hw1) * 0.3
    ctx.curve_to(mx2, my2,
                 x0 - nx * hw0 + dx * 0.33, y0 - ny * hw0 + dy * 0.33,
                 x0 - nx * hw0, y0 - ny * hw0)
    ctx.close_path()
    set_color(ctx, color)
    ctx.fill()


# ═══════════════════════════════════════════════════════════════════════════
# PYCAIRO CHARACTER RENDERING — Byte (C52)
# ═══════════════════════════════════════════════════════════════════════════

def draw_byte_cairo(emerge_cx, emerge_cy, emerge_rx, emerge_ry,
                    luma_hand_x, luma_hand_y):
    """Draw Byte using pycairo smooth curves. Returns RGBA PIL image."""
    surface, ctx, w_px, h_px = create_surface(W, H, scale=1)

    byte_cx = emerge_cx
    byte_cy = emerge_cy - int(emerge_ry * 0.20)
    byte_rx = int(emerge_rx * 0.78)
    byte_ry = int(emerge_ry * 0.80)

    # Distortion rings (3 concentric)
    for i in range(3):
        dist_rx = byte_rx + sp(12) + i * sp(10)
        dist_ry = byte_ry + sp(8)  + i * sp(7)
        draw_ellipse(ctx, byte_cx, byte_cy, dist_rx, dist_ry)
        ctx.set_line_width(sp(2))
        set_color(ctx, (0, 168 + i * 20, 180 + i * 18))
        ctx.stroke()

    # Byte body — smooth ellipse with gradient fill
    draw_ellipse(ctx, byte_cx, byte_cy, byte_rx, byte_ry)
    pat_byte = cairo.RadialGradient(byte_cx - int(byte_rx * 0.2),
                                     byte_cy - int(byte_ry * 0.25),
                                     0,
                                     byte_cx, byte_cy,
                                     max(byte_rx, byte_ry))
    pat_byte.add_color_stop_rgb(0.0, *_c(BYTE_HL))
    pat_byte.add_color_stop_rgb(0.5, *_c(BYTE_TEAL))
    pat_byte.add_color_stop_rgb(1.0, *_c(BYTE_SH))
    ctx.set_source(pat_byte)
    ctx.fill()

    # Submerge fade into void at lower body
    VOID_POCKET = (14, 14, 30)
    submerge_y = byte_cy + int(byte_ry * 0.50)
    for row_offset in range(0, int(byte_ry * 0.38), sp(4)):
        y_row = submerge_y + row_offset
        t_fade = row_offset / max(1, int(byte_ry * 0.38))
        fade_rx = int(byte_rx * (1 - t_fade * 0.3))
        col = (
            int(VOID_POCKET[0] * t_fade + BYTE_TEAL[0] * (1 - t_fade)),
            int(VOID_POCKET[1] * t_fade + BYTE_TEAL[1] * (1 - t_fade)),
            int(VOID_POCKET[2] * t_fade + BYTE_TEAL[2] * (1 - t_fade)),
        )
        ctx.move_to(byte_cx - fade_rx, y_row)
        ctx.line_to(byte_cx + fade_rx, y_row)
        ctx.set_line_width(sp(4))
        set_color(ctx, col)
        ctx.stroke()

    # Amber outline (corrupted amber)
    for i in range(sp(3)):
        draw_ellipse(ctx, byte_cx, byte_cy, byte_rx + i, byte_ry + i)
        ctx.set_line_width(1)
        set_color(ctx, CORRUPTED_AMBER)
        ctx.stroke()

    # ── Eyes ──
    # Left eye — glitch-style square brackets
    eye_size = max(sp(8), int(byte_rx * 0.22))
    lex_b = byte_cx - int(byte_rx * 0.30)
    ley_b = byte_cy - int(byte_ry * 0.12)
    ctx.rectangle(lex_b - eye_size // 2, ley_b - eye_size,
                  eye_size, eye_size // 3 + eye_size)
    # Two horizontal bars (glitch bracket eye)
    ctx.rectangle(lex_b - eye_size // 2, ley_b - eye_size, eye_size, eye_size // 3)
    set_color(ctx, ELEC_CYAN)
    ctx.fill()
    ctx.rectangle(lex_b - eye_size // 2, ley_b + eye_size // 2, eye_size, eye_size // 2)
    set_color(ctx, ELEC_CYAN)
    ctx.fill()

    # Right eye — round (organic/human side)
    rex_b = byte_cx + int(byte_rx * 0.30)
    rey_b = byte_cy - int(byte_ry * 0.12)
    r_eye_w = int(byte_rx * 0.36)
    r_eye_h = int(byte_ry * 0.36)
    draw_ellipse(ctx, rex_b, rey_b, r_eye_w, r_eye_h)
    set_color(ctx, (240, 240, 245))
    ctx.fill()
    draw_ellipse(ctx, rex_b, rey_b, r_eye_w, r_eye_h)
    ctx.set_line_width(sp(2))
    set_color(ctx, LINE)
    ctx.stroke()

    # Pupil
    pupil_r = int(r_eye_w * 0.55)
    draw_ellipse(ctx, rex_b - sp(4), rey_b, pupil_r, pupil_r)
    set_color(ctx, LINE)
    ctx.fill()
    # Iris highlight
    draw_ellipse(ctx, rex_b - sp(2), rey_b - int(r_eye_h * 0.2),
                 int(r_eye_w * 0.15), int(r_eye_h * 0.2))
    set_color(ctx, ELEC_CYAN)
    ctx.fill()

    # Scar
    scar_x = byte_cx + int(byte_rx * 0.10)
    scar_y = byte_cy - int(byte_ry * 0.30)
    ctx.set_line_width(sp(3))
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.move_to(scar_x, scar_y)
    ctx.line_to(scar_x + int(byte_rx * 0.18), scar_y + int(byte_ry * 0.22))
    set_color(ctx, SCAR_MAG)
    ctx.stroke()
    ctx.set_line_width(sp(2))
    ctx.move_to(scar_x + int(byte_rx * 0.06), scar_y + int(byte_ry * 0.08))
    ctx.line_to(scar_x + int(byte_rx * 0.24), scar_y + int(byte_ry * 0.16))
    set_color(ctx, SCAR_MAG)
    ctx.stroke()

    # ── Tendril arm reaching toward Luma ──
    arm_start_x = byte_cx - byte_rx
    arm_start_y = byte_cy + int(byte_ry * 0.10)
    target_x = luma_hand_x
    target_y = luma_hand_y
    steps = 30
    tendril_pts = []
    cp1x = arm_start_x + int((target_x - arm_start_x) * 0.33)
    cp1y = arm_start_y - int(byte_ry * 0.5)
    for i in range(steps + 1):
        t = i / steps
        px_t = (1-t)**2 * arm_start_x + 2*(1-t)*t * cp1x + t**2 * target_x
        py_t = (1-t)**2 * arm_start_y + 2*(1-t)*t * cp1y + t**2 * target_y
        tendril_pts.append((px_t, py_t))

    # Draw tapered tendril with cairo
    for i in range(len(tendril_pts) - 1):
        thickness = max(sp(2), int(sp(8) * (1 - i / len(tendril_pts))))
        ctx.set_line_width(thickness)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.move_to(tendril_pts[i][0], tendril_pts[i][1])
        ctx.line_to(tendril_pts[i+1][0], tendril_pts[i+1][1])
        set_color(ctx, BYTE_TEAL)
        ctx.stroke()

    # Tendril tip glow
    if tendril_pts:
        tx, ty = tendril_pts[-1]
        draw_ellipse(ctx, tx, ty, sp(8), sp(8))
        set_color(ctx, ELEC_CYAN)
        ctx.fill()

    # Gap glow between tendril and hand
    gap_cx = (tendril_pts[-1][0] + luma_hand_x) // 2 if tendril_pts else luma_hand_x - sp(40)
    gap_cy = (tendril_pts[-1][1] + luma_hand_y) // 2 if tendril_pts else luma_hand_y
    # Radial glow
    draw_ellipse(ctx, gap_cx, gap_cy, sx(55), sy(38))
    pat_gap = cairo.RadialGradient(gap_cx, gap_cy, 0, gap_cx, gap_cy, max(sx(55), sy(38)))
    pat_gap.add_color_stop_rgba(0.0, *_ca((180, 255, 255, 120)))
    pat_gap.add_color_stop_rgba(0.5, *_ca((0, 240, 255, 60)))
    pat_gap.add_color_stop_rgba(1.0, 0, 0, 0, 0)
    ctx.set_source(pat_gap)
    ctx.fill()

    # Spark particles
    rng_gap = random.Random(77)
    for _ in range(18):
        spx = gap_cx + rng_gap.randint(-sx(52), sx(52))
        spy = gap_cy + rng_gap.randint(-sy(32), sy(32))
        sps = rng_gap.choice([2, 3, 4])
        spc = rng_gap.choice([ELEC_CYAN, STATIC_WHITE, (180, 255, 255)])
        ctx.rectangle(spx, spy, sps, sps)
        set_color(ctx, spc)
        ctx.fill()

    # Antenna
    ant_x = byte_cx + int(byte_rx * 0.20)
    ant_y = byte_cy - byte_ry
    ctx.set_line_width(sp(3))
    ctx.move_to(ant_x, ant_y)
    ctx.line_to(ant_x + sp(10), ant_y - sp(30))
    set_color(ctx, BYTE_TEAL)
    ctx.stroke()
    draw_ellipse(ctx, ant_x + sp(11), ant_y - sp(33), sp(5), sp(5))
    set_color(ctx, ELEC_CYAN)
    ctx.fill()

    # Data particles
    rng_p = random.Random(77)
    for _ in range(18):
        pdx = rng_p.randint(-int(emerge_rx * 1.6), int(emerge_rx * 1.6))
        pdy = rng_p.randint(-int(emerge_ry * 1.6), int(emerge_ry * 1.6))
        ps  = rng_p.choice([sp(2), sp(3), sp(4)])
        pc  = rng_p.choice([ELEC_CYAN, BYTE_TEAL, (0, 200, 220)])
        ctx.rectangle(emerge_cx + pdx, emerge_cy + pdy, ps, ps)
        set_color(ctx, pc)
        ctx.fill()

    byte_img = to_pil_rgba(surface)
    return byte_img


# ═══════════════════════════════════════════════════════════════════════════
# Compositing & Lighting
# ═══════════════════════════════════════════════════════════════════════════

def apply_contact_shadow(img, char_cx, char_base_y, char_width, surface_color):
    """Apply contact shadow using Wand (Gaussian blur) or PIL fallback."""
    if _WAND_OK:
        result = wand_contact_shadow(
            img, char_cx, char_base_y, char_width,
            surface_color=surface_color,
            shadow_alpha=55, spread=1.1, height_px=sp(10),
            blur_sigma=sp(4), darken=0.45
        )
        return result
    else:
        # PIL fallback: draw concentric ellipses with quadratic falloff
        shadow_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
        shadow_draw = ImageDraw.Draw(shadow_layer)
        shadow_color = tuple(max(0, int(c * 0.45)) for c in surface_color)
        shadow_w = int(char_width * 1.1)
        shadow_h = sp(10)
        for i in range(shadow_h):
            t = 1.0 - (i / shadow_h)
            a = int(55 * t * t)
            y = char_base_y + i
            row_w = int(shadow_w * (1.0 - 0.3 * (i / shadow_h)))
            shadow_draw.ellipse(
                [char_cx - row_w, y - 2, char_cx + row_w, y + 2],
                fill=(*shadow_color, a)
            )
        if _SCIPY_OK:
            # Gaussian blur the shadow layer for smoother result
            arr = np.array(shadow_layer)
            arr[:, :, 3] = gaussian_filter(arr[:, :, 3].astype(float), sigma=sp(3)).astype(np.uint8)
            shadow_layer = Image.fromarray(arr, "RGBA")
        base = img.convert("RGBA")
        result = Image.alpha_composite(base, shadow_layer)
        return result


def apply_bounce_light(img, char_cx, char_base_y, char_top_y, char_width,
                       bounce_color, influence=0.15):
    """Apply bounce light from floor/surface to character lower quarter."""
    bounce_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    bounce_draw = ImageDraw.Draw(bounce_layer)
    bounce_start_y = char_base_y - int((char_base_y - char_top_y) * 0.30)
    bounce_end_y = char_base_y

    for y in range(bounce_start_y, bounce_end_y):
        t = (y - bounce_start_y) / max(1, bounce_end_y - bounce_start_y)
        alpha = int(40 * t * t)
        half_w = int(char_width * 0.5 * (0.8 + 0.2 * t))
        bounce_draw.line(
            [(char_cx - half_w, y), (char_cx + half_w, y)],
            fill=(*bounce_color, alpha),
            width=1
        )
    base_rgba = img.convert("RGBA")
    result = Image.alpha_composite(base_rgba, bounce_layer)
    return result.convert("RGB")


def draw_lighting_overlay_post_character(img, lamp_x, lamp_y, monitor_cx, monitor_cy):
    """Post-character lighting overlay — warm/cool split affects character too."""
    warm_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    warm_draw  = ImageDraw.Draw(warm_layer)
    lamp_glow_cx = lamp_x + sx(32)
    lamp_glow_cy = lamp_y + sy(int(1080 * 0.35))
    for step in range(14, 0, -1):
        t = step / 14
        rx  = int(W * 0.30 * t)
        ry  = int(H * 0.55 * t)
        alpha = int(50 * (1 - t))
        warm_draw.ellipse([lamp_glow_cx - rx, lamp_glow_cy - ry,
                           lamp_glow_cx + rx, lamp_glow_cy + ry],
                          fill=(*SOFT_GOLD, alpha))
    warm_np = warm_layer.crop((0, 0, W // 2, H))
    base_left  = img.crop((0, 0, W // 2, H)).convert("RGBA")
    composited_left = Image.alpha_composite(base_left, warm_np)
    img.paste(composited_left.convert("RGB"), (0, 0))

    cold_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cold_draw  = ImageDraw.Draw(cold_layer)
    for step in range(14, 0, -1):
        t = step / 14
        rx  = int(W * 0.55 * t)
        ry  = int(H * 0.65 * t)
        alpha = int(45 * (1 - t))
        cold_draw.ellipse([monitor_cx - rx, monitor_cy - ry,
                           monitor_cx + rx, monitor_cy + ry],
                          fill=(*ELEC_CYAN, alpha))
    split_x = W // 2 - sx(120)
    cold_np    = cold_layer.crop((split_x, 0, W, H))
    base_right = img.crop((split_x, 0, W, H)).convert("RGBA")
    composited_right = Image.alpha_composite(base_right, cold_np)
    img.paste(composited_right.convert("RGB"), (split_x, 0))
    return img


# ═══════════════════════════════════════════════════════════════════════════
# Main Generate
# ═══════════════════════════════════════════════════════════════════════════

def generate(skip_fill_light=False):
    """Generate Style Frame 01 — The Discovery (C52 pycairo migration).

    Args:
        skip_fill_light: If True, omit lighting passes for nolight base image.
    """
    out_path = NOLIGHT_PATH if skip_fill_light else OUTPUT_PATH
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    img = Image.new("RGB", (W, H), WARM_CREAM)
    draw = ImageDraw.Draw(img)

    # STEP 1: Background
    bg_data = draw_background(draw, img)
    draw = ImageDraw.Draw(img)
    scr_x0 = bg_data["scr_x0"]; scr_y0 = bg_data["scr_y0"]
    scr_x1 = bg_data["scr_x1"]; scr_y1 = bg_data["scr_y1"]
    emerge_cx = bg_data["emerge_cx"]; emerge_cy = bg_data["emerge_cy"]
    emerge_rx = bg_data["emerge_rx"]; emerge_ry = bg_data["emerge_ry"]

    # STEP 2: Couch
    luma_cx     = sx(int(1920 * 0.29))
    luma_base_y = sy(int(1080 * 0.90))
    draw_couch(draw, luma_cx, luma_base_y)

    # STEP 3: Contact shadow (Wand Gaussian blur or PIL fallback)
    lean_offset = sp(44)
    shadow_cx = luma_cx + lean_offset // 2
    img = apply_contact_shadow(img, shadow_cx, luma_base_y - sp(85),
                               sp(80), COUCH_BODY)
    if hasattr(img, 'convert') and img.mode == "RGBA":
        img = img.convert("RGB")
    draw = ImageDraw.Draw(img)

    # STEP 4: Luma — pycairo character rendering
    arm_target_x = scr_x0 - sx(20)
    crt_cx = bg_data["mw_x"] + bg_data["mw_w"] // 2

    luma_img, luma_data = draw_luma_cairo(
        luma_cx, luma_base_y, arm_target_x,
        byte_cx_target=emerge_cx, byte_cy_target=emerge_cy,
        crt_cx=crt_cx
    )

    # Composite Luma onto background
    base_rgba = img.convert("RGBA")
    base_rgba = Image.alpha_composite(base_rgba, luma_img)
    img = base_rgba.convert("RGB")
    draw = ImageDraw.Draw(img)

    # STEP 5: Bounce light from couch onto character lower half
    img = apply_bounce_light(
        img,
        char_cx=shadow_cx,
        char_base_y=luma_base_y,
        char_top_y=luma_data["torso_top"],
        char_width=sp(88),
        bounce_color=COUCH_BODY,
        influence=0.15
    )
    draw = ImageDraw.Draw(img)

    # STEP 6: Byte — pycairo character rendering
    byte_img = draw_byte_cairo(emerge_cx, emerge_cy, emerge_rx, emerge_ry,
                                luma_data["hand_cx"], luma_data["hand_cy"])
    base_rgba = img.convert("RGBA")
    base_rgba = Image.alpha_composite(base_rgba, byte_img)
    img = base_rgba.convert("RGB")
    draw = ImageDraw.Draw(img)

    # STEP 7: Lighting overlay — AFTER character (scene-lit structural change)
    if not skip_fill_light:
        mw_x = bg_data["mw_x"]; mw_y = bg_data["mw_y"]
        mw_w = bg_data["mw_w"]; mw_h = bg_data["mw_h"]
        lamp_x_pos = sx(int(1920 * 0.40))
        lamp_y_pos = bg_data["ceiling_y"] + sy(18)
        monitor_cx_pos = mw_x + mw_w // 2
        monitor_cy_pos = mw_y + mw_h // 2
        img = draw_lighting_overlay_post_character(img,
                                                    lamp_x=lamp_x_pos, lamp_y=lamp_y_pos,
                                                    monitor_cx=monitor_cx_pos, monitor_cy=monitor_cy_pos)
        draw = ImageDraw.Draw(img)

    # STEP 7b: Face lighting — scene-colored
    if not skip_fill_light:
        scene_highlight = blend_color(SKIN_HL, SCENE_COOL_TINT, 0.20)
        scene_shadow = blend_color(SKIN_SH, SCENE_WARM_TINT, 0.10)
        add_face_lighting(
            img,
            face_center=(luma_data["head_cx"], luma_data["head_cy"]),
            face_radius=(luma_data["head_r"], luma_data["head_r"]),
            light_dir=(1.0, -0.5),
            shadow_color=scene_shadow,
            highlight_color=scene_highlight,
            seed=500,
        )
        draw = ImageDraw.Draw(img)

    # STEP 7c: Rim light — CRT cyan
    if not skip_fill_light:
        add_rim_light(
            img,
            threshold=175,
            light_color=(0, 220, 232),
            width=sp(4),
            side="right",
            char_cx=luma_data["head_cx"],
        )
        draw = ImageDraw.Draw(img)

    # STEP 8: Vignette
    vignette = Image.new("RGB", (W, H), (0, 0, 0))
    v_alpha  = Image.new("L", (W, H), 0)
    v_draw   = ImageDraw.Draw(v_alpha)
    for i in range(60):
        t = 1.0 - i / 60.0
        alpha_val = int(70 * t)
        v_draw.line([(0, i), (W, i)], fill=alpha_val)
        v_draw.line([(0, H - 1 - i), (W, H - 1 - i)], fill=alpha_val)
    img = Image.composite(vignette, img, v_alpha)
    draw = ImageDraw.Draw(img)

    # STEP 9: Downscale 2x -> 1280x720 with LANCZOS
    img = img.resize((W_OUT, H_OUT), Image.LANCZOS)
    draw = ImageDraw.Draw(img)

    # STEP 10: Title strip
    font_xs = load_font(11)
    draw.rectangle([0, H_OUT - 30, W_OUT, H_OUT], fill=(20, 12, 8))
    draw.text((10, H_OUT - 22),
              "LUMA & THE GLITCHKIN — Frame 01: The Discovery  |  C52 — pycairo character migration",
              fill=(180, 150, 100), font=font_xs)

    # STEP 11: Size rule enforcement
    if img.width > 1280 or img.height > 1280:
        img.thumbnail((1280, 1280), Image.LANCZOS)

    img.save(out_path, "PNG")
    label = "nolight base" if skip_fill_light else "composited"
    print(f"Saved ({label}): {out_path}  ({img.width}x{img.height})")
    return out_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="LTG_TOOL_styleframe_discovery.py — Style Frame 01: The Discovery"
    )
    parser.add_argument(
        "--save-nolight",
        action="store_true",
        help=(
            "Also save an unlit base image (no fill-light overlay, no face lighting, "
            "no rim light) as LTG_COLOR_styleframe_discovery_nolight.png alongside the "
            "normal composited output."
        ),
    )
    args = parser.parse_args()

    generate()
    if args.save_nolight:
        generate(skip_fill_light=True)
