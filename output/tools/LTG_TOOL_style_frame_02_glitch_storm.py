#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_style_frame_02_glitch_storm.py
Style Frame 02 — "Glitch Storm" — C54 Canonical Character Migration
"Luma & the Glitchkin"

Artist: Jordan Reed | Cycle 54
Based on: C53 pycairo + Wand migration (Jordan Reed, Cycle 53)

C54 changes (Jordan Reed):
  CANONICAL CHARACTER MIGRATION:
    - Luma, Cosmo, Byte now use canonical char_*.py modular renderers.
      draw_luma("DETERMINED"), draw_cosmo("WORRIED"), draw_byte("alarmed").
    - Glitch retains local pycairo renderer (background character, unchanged).
    - Canonical chars: cairo surface -> PIL RGBA -> resize to scene scale -> alpha composite.
    - PIL fallback retained if canonical renderers unavailable.

C53 changes (Jordan Reed):
  PYCAIRO CHARACTER MIGRATION + WAND COMPOSITING:
    - All characters (Luma, Cosmo, Byte, Glitch) rendered with pycairo bezier curves.
      Smooth anti-aliased body silhouettes replace PIL rectangle/ellipse primitives.
    - Characters drawn on separate transparent RGBA layers for Wand compositing.
    - Wand compositing pipeline: contact shadow -> character paste -> bounce light ->
      edge tint -> color transfer. Graceful PIL fallback if Wand unavailable.
    - Internal render at 2x (2560x1440) for AA, downscaled to 1280x720 with LANCZOS.
    - Environment layers (sky, confetti, town, street, storefront, ground lighting)
      remain PIL-based at 2x resolution.
    - All prior fixes carried forward: C47 shoulder involvement, C44 native canvas,
      C36 fill light, C35 face/lean/hair, C34 cyan specular, C22 palette/storefront.
    - SF02 is Glitch Layer — depth temperature rule is cool-ambient, UV_PURPLE dominant.

Output: /home/wipkat/team/output/color/style_frames/LTG_COLOR_styleframe_glitch_storm.png
Usage: python3 LTG_TOOL_style_frame_02_glitch_storm.py [--save-nolight]

--save-nolight: also save an unlit base image (no magenta fill light, no cyan
    specular) as LTG_COLOR_styleframe_glitch_storm_nolight.png alongside the
    normal composited output. Enables Section 10 (alpha_blend_lint) in
    precritique_qa.py. Dutch angle is still applied to both outputs.
"""

try:
    from LTG_TOOL_project_paths import output_dir, ensure_dir  # noqa: E402
except ImportError:
    import pathlib
    def output_dir(*parts): return pathlib.Path("/home/wipkat/team/output").joinpath(*parts)
    def ensure_dir(path): path.mkdir(parents=True, exist_ok=True); return path
import os
import sys
import math
import random
import argparse
from PIL import Image, ImageDraw, ImageFilter, ImageChops
import numpy as np

# Import tools
_TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _TOOLS_DIR)

# Procedural draw library for add_rim_light
try:
    from LTG_TOOL_procedural_draw import add_rim_light
    PROCEDURAL_DRAW_AVAILABLE = True
except ImportError:
    PROCEDURAL_DRAW_AVAILABLE = False
    print("WARNING: LTG_TOOL_procedural_draw not found — rim light passes will use fallback.")

# Cairo primitives for character rendering
try:
    from LTG_TOOL_cairo_primitives import (
        create_surface, draw_bezier_path, draw_tapered_stroke,
        draw_gradient_fill, draw_wobble_path, draw_smooth_polygon,
        draw_ellipse, to_pil_image, to_pil_rgba, set_color
    )
    import cairo
    _CAIRO_OK = True
except ImportError:
    _CAIRO_OK = False
    print("WARNING: pycairo/cairo_primitives not found — falling back to PIL character rendering.")

# Canonical character renderers (C54 migration)
try:
    from LTG_TOOL_char_luma import draw_luma as _draw_luma_canonical
    from LTG_TOOL_char_cosmo import draw_cosmo as _draw_cosmo_canonical
    from LTG_TOOL_char_byte import draw_byte as _draw_byte_canonical
    _CHAR_CANONICAL = True
except ImportError:
    _CHAR_CANONICAL = False
    print("WARNING: canonical char renderers not found — falling back to local PIL character rendering.")

# Wand compositing — graceful fallback to PIL
_WAND_OK = False
try:
    from LTG_TOOL_wand_composite import (
        wand_contact_shadow, wand_bounce_light, wand_edge_tint,
        wand_color_transfer, _WAND_AVAILABLE
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

OUTPUT_PATH = output_dir('color', 'style_frames', 'LTG_COLOR_styleframe_glitch_storm.png')
NOLIGHT_PATH = output_dir('color', 'style_frames', 'LTG_COLOR_styleframe_glitch_storm_nolight.png')

# ── C53: Render at 2x for AA, downscale to 1280x720 ─────────────────────────
W_OUT, H_OUT = 1280, 720
SCALE = 2
W, H = W_OUT * SCALE, H_OUT * SCALE   # 2560 x 1440

# Scale factors from 1280x720 reference to 2560x1440 internal
SX = SCALE
SY = SCALE
def sx(n): return int(n * SX)
def sy(n): return int(n * SY)
def sp(n): return int(n * min(SX, SY))

# ── Master Palette ────────────────────────────────────────────────────────────
WARM_CREAM      = (250, 240, 220)
SOFT_GOLD       = (232, 201,  90)
SUNLIT_AMBER    = (212, 146,  58)
TERRACOTTA      = (199,  91,  57)
SAGE_GREEN      = (122, 158, 126)
DUSTY_LAVENDER  = (168, 155, 191)

VOID_BLACK      = ( 10,  10,  20)
ELEC_CYAN       = (  0, 240, 255)   # GL-01a #00F0FF — CHAR-L-11 Constraint 1
ACID_GREEN      = ( 57, 255,  20)
DATA_BLUE       = ( 10,  79, 140)   # #0A4F8C — dominant storm confetti color
UV_PURPLE       = (123,  47, 190)
HOT_MAGENTA     = (255,  45, 107)   # GL-02 #FF2D6B — canonical (NOT #FF0090)
STATIC_WHITE    = (240, 240, 240)
CORRUPT_AMBER   = (255, 140,   0)   # GL-07 canonical #FF8C00

# ENV colors
NIGHT_SKY_DEEP  = ( 26,  20,  40)
DARK_ASPHALT    = ( 42,  42,  56)
CYAN_ROAD       = ( 42,  90, 106)
WARM_ROAD       = ( 74,  58,  42)
COOL_SIDEWALK   = ( 58,  56,  72)
TERRA_CYAN_LIT  = (150, 172, 162)  # ENV-06 fix: G=172>R=150, B=162>R=150
DEEP_WARM_SHAD  = ( 90,  56,  32)
ROOF_EDGE       = ( 26,  24,  32)
DEEP_COCOA      = ( 59,  40,  32)

WIN_GLOW_WARM   = (200, 160,  80)

# Character storm colors
DRW_HOODIE_STORM    = (200, 105,  90)
DRW_SKIN_STORM      = (106, 180, 174)
DRW_HOODIE_SHADOW   = ( 58,  26,  20)
DRW_JACKET_STORM    = (128, 192, 204)
DRW_JACKET_SHADOW   = ( 42,  26,  50)
DRW_HAIR_MAGENTA    = (106,  42,  58)
BYTE_TEAL           = (  0, 212, 232)   # GL-01b BYTE_TEAL — NEVER Void Black

# Storm edge-lighting colors for buildings
STORM_RIM_CYAN  = (  0, 180, 220)
STORM_RIM_UV    = ( 80,  30, 120)

RNG = random.Random(42)


def _cairo_char_to_pil(surface):
    """Convert a canonical char cairo.ImageSurface to cropped PIL RGBA."""
    pil_img = to_pil_rgba(surface)
    bbox = pil_img.getbbox()
    if bbox:
        pil_img = pil_img.crop(bbox)
    return pil_img


def _composite_canonical_char(img, char_pil, cx, foot_y):
    """Composite a canonical char PIL RGBA onto img.
    cx: horizontal center; foot_y: Y of the character's feet (bottom of image).
    """
    x = cx - char_pil.width // 2
    y = foot_y - char_pil.height
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    overlay.paste(char_pil, (x, y), char_pil)
    base_rgba = img.convert("RGBA")
    result = Image.alpha_composite(base_rgba, overlay)
    img = result.convert("RGB")

    # GL storm scene tint: cool UV-ambient overlay on character area (shifts warm hoodie
    # toward GL cold palette). Alpha 40 = ~16% tint — enough to shift hue, not flatten.
    char_x0 = max(0, x)
    char_y0 = max(0, y)
    char_x1 = min(W, x + char_pil.width)
    char_y1 = min(H, foot_y)

    tint_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    td = ImageDraw.Draw(tint_layer)
    td.rectangle([char_x0, char_y0, char_x1, char_y1],
                 fill=(*NIGHT_SKY_DEEP, 40))
    base_rgba2 = img.convert("RGBA")
    result2 = Image.alpha_composite(base_rgba2, tint_layer)
    return result2.convert("RGB")


def lerp_color(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))


def blend_color(base, tint, influence):
    """Blend base color toward tint by influence factor (0.0-1.0)."""
    return tuple(int(base[i] * (1 - influence) + tint[i] * influence) for i in range(3))


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


def _c(rgb):
    """(R,G,B) 0-255 -> cairo (r,g,b) 0.0-1.0."""
    return (rgb[0] / 255.0, rgb[1] / 255.0, rgb[2] / 255.0)


def _ca(rgba):
    """(R,G,B,A) 0-255 -> cairo (r,g,b,a) 0.0-1.0."""
    return (rgba[0] / 255.0, rgba[1] / 255.0, rgba[2] / 255.0, rgba[3] / 255.0)


def alpha_paste(base, overlay_rgba):
    base_rgba = base.convert("RGBA")
    base_rgba.alpha_composite(overlay_rgba)
    return base_rgba.convert("RGB")


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
    mx = (x0 + x1) / 2.0 + nx * (hw0 + hw1) * 0.3
    my = (y0 + y1) / 2.0 + ny * (hw0 + hw1) * 0.3
    ctx.curve_to(x0 + nx * hw0 + dx * 0.33, y0 + ny * hw0 + dy * 0.33,
                 mx, my,
                 x1 + nx * hw1, y1 + ny * hw1)
    ctx.line_to(x1 - nx * hw1, y1 - ny * hw1)
    mx2 = (x0 + x1) / 2.0 - nx * (hw0 + hw1) * 0.3
    my2 = (y0 + y1) / 2.0 - ny * (hw0 + hw1) * 0.3
    ctx.curve_to(mx2, my2,
                 x0 - nx * hw0 + dx * 0.33, y0 - ny * hw0 + dy * 0.33,
                 x0 - nx * hw0, y0 - ny * hw0)
    ctx.close_path()
    set_color(ctx, color)
    ctx.fill()


# ═══════════════════════════════════════════════════════════════════════════════
# Environment layers — rendered at W_OUT x H_OUT (1280x720), then upscaled
# ═══════════════════════════════════════════════════════════════════════════════
# Environment functions use W_ENV/H_ENV for their own coordinate system.
# This avoids rewriting hundreds of hardcoded C44 coordinates.
W_ENV, H_ENV = W_OUT, H_OUT


# ── Layer 1: Sky ──────────────────────────────────────────────────────────────

def draw_sky(img):
    draw = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        col = lerp_color(VOID_BLACK, NIGHT_SKY_DEEP, min(t * 2.5, 1.0))
        draw.line([(0, y), (W, y)], fill=col)
    _draw_uv_cloud_masses(img)
    _draw_horizon_haze(img)
    _draw_main_crack(img)
    _draw_sub_cracks(img)
    _draw_storm_edges(img)
    return img


def _draw_uv_cloud_masses(img):
    # C44: all pixel coords scaled × 2/3 from 1920×1080 originals
    cloud_shapes = [
        (0,    0,  347, 147), (53,  40,  253, 107),
        (13,  80,  173,  53), (307,  0,  133,  93), (253, 53,  120,  80),
    ]
    for (cx, cy, cw, ch) in cloud_shapes:
        overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        od = ImageDraw.Draw(overlay)
        od.rectangle([cx, cy, cx + cw, cy + ch], fill=(*UV_PURPLE, 200))
        bite_x = cx + int(cw * 0.55)
        bite_y = cy + int(ch * 0.30)
        od.rectangle([bite_x, bite_y, cx + cw, bite_y + int(ch * 0.40)], fill=(*VOID_BLACK, 255))
        img = alpha_paste(img, overlay)
    cloud_shapes_r = [
        (920,  0,  360, 200), (1000, 40,  280, 133), (1080, 13,  200, 107),
        (1173, 53,  107, 160), (900, 107,  253,  93),
    ]
    for (cx, cy, cw, ch) in cloud_shapes_r:
        overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        od = ImageDraw.Draw(overlay)
        od.rectangle([cx, cy, cx + cw, cy + ch], fill=(*UV_PURPLE, 210))
        core_x = cx + int(cw * 0.25)
        core_y = cy + int(ch * 0.25)
        od.rectangle([core_x, core_y, core_x + int(cw * 0.50),
                      core_y + int(ch * 0.50)], fill=(*VOID_BLACK, 255))
        img = alpha_paste(img, overlay)
    return img


def _draw_horizon_haze(img):
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    horizon_y = int(H * 0.55)
    haze_height = int(H * 0.15)
    for dy in range(haze_height):
        t = 1.0 - (dy / haze_height)
        a = int(40 * t)
        od.line([(0, horizon_y - dy), (W, horizon_y - dy)], fill=(*UV_PURPLE, a))
    return alpha_paste(img, overlay)


def _draw_main_crack(img):
    # C44: crack_pts scaled × 2/3
    crack_pts = [
        (1213, 0), (1133, 53), (1133, 93), (1067, 147), (1013, 147),
        (973, 227), (920, 280), (920, 333), (853, 387), (800, 427),
    ]
    glow_specs = [
        (HOT_MAGENTA, 12, 80), (ELEC_CYAN, 8, 180), (ELEC_CYAN, 4, 240), (STATIC_WHITE, 2, 220),
    ]
    for (color, half_w, alpha) in glow_specs:
        overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        od = ImageDraw.Draw(overlay)
        for i in range(len(crack_pts) - 1):
            x0, y0 = crack_pts[i]; x1, y1 = crack_pts[i + 1]
            od.line([(x0, y0), (x1, y1)], fill=(*color, alpha), width=max(1, half_w * 2))
        img = alpha_paste(img, overlay)
    return img


def _draw_sub_cracks(img):
    # C44: sub_cracks coords scaled × 2/3
    sub_cracks = [
        (1133, 93, 1167, 33), (1067, 147, 1040, 107), (973, 227, 1013, 267),
        (920, 280, 880, 253), (853, 387, 827, 347), (920, 333, 960, 373),
        (800, 427, 773, 453),
    ]
    for (x0, y0, x1, y1) in sub_cracks:
        overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        od = ImageDraw.Draw(overlay)
        od.line([(x0, y0), (x1, y1)], fill=(*ELEC_CYAN, 160), width=3)
        mid_x = (x0 + x1) // 2; mid_y = (y0 + y1) // 2
        od.line([(mid_x, mid_y), (x1, y1)], fill=(*DATA_BLUE, 120), width=2)
        img = alpha_paste(img, overlay)
    return img


def _draw_storm_edges(img):
    draw = ImageDraw.Draw(img)
    # C44: burn_line coords scaled × 2/3
    burn_lines = [
        ((307,  0), (347, 20)), ((253, 53), (293, 73)), ((53,  40), (73, 60)),
        ((920,  0), (907, 33)), ((1000, 40), (987, 73)), ((1173, 53), (1147, 87)),
        ((900, 107), (920, 133)),
    ]
    for pt1, pt2 in burn_lines:
        draw.line([pt1, pt2], fill=HOT_MAGENTA, width=2)
    return img


# ── Layer 2: Storm Confetti — dominant cold confetti ──────────────────────────

def draw_storm_confetti(img):
    """Dominant cold confetti — DATA_BLUE 70%, VOID_BLACK 20%, ELEC_CYAN 10%."""
    draw = ImageDraw.Draw(img)

    cold_dominant = (
        [DATA_BLUE] * 7 +
        [VOID_BLACK] * 2 +
        [ELEC_CYAN] * 1
    )
    accent_pool = cold_dominant + [UV_PURPLE]

    # C44: x/y ranges and sizes scaled × 2/3; confetti count unchanged
    for _ in range(240):
        cx = RNG.randint(733, 1267); cy = RNG.randint(0, int(H * 0.55))
        dist = math.sqrt((cx - 933) ** 2 + (cy - 200) ** 2)
        t = clamp(dist / 467.0, 0.0, 1.0)
        size = int(10 - (10 - 2) * t)
        color = RNG.choice(cold_dominant)
        draw.rectangle([cx, cy, cx + size, cy + size], fill=color)

    for _ in range(160):
        cx = RNG.randint(400, 1267); cy = RNG.randint(int(H * 0.25), int(H * 0.60))
        size = RNG.randint(2, 5)
        color = RNG.choice(accent_pool)
        alpha_draw = RNG.randint(140, 220)
        overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        od = ImageDraw.Draw(overlay)
        od.rectangle([cx, cy, cx + size, cy + size], fill=(*color, alpha_draw))
        img = alpha_paste(img, overlay)
    draw = ImageDraw.Draw(img)

    for _ in range(80):
        cx = RNG.randint(200, 600); cy = RNG.randint(int(H * 0.65), H)
        size = RNG.randint(1, 3)
        color = RNG.choice(cold_dominant)
        draw.rectangle([cx, cy, cx + size, cy + size], fill=color)
    return img


# ── Layer 3: Town Silhouette ───────────────────────────────────────────────────

def draw_town_silhouette(img):
    draw = ImageDraw.Draw(img)
    horizon_y = int(H * 0.58)
    # C44: building x coords and heights scaled × 2/3
    buildings = [
        (0,    horizon_y - 107, 120,  horizon_y, DEEP_WARM_SHAD),
        (100,  horizon_y - 133, 213,  horizon_y, DEEP_WARM_SHAD),
        (200,  horizon_y -  93, 293,  horizon_y, TERRA_CYAN_LIT),
        (280,  horizon_y - 173, 373,  horizon_y, DEEP_WARM_SHAD),
        (360,  horizon_y - 120, 453,  horizon_y, TERRA_CYAN_LIT),
        (440,  horizon_y - 227, 507,  horizon_y, DEEP_WARM_SHAD),
        (460,  horizon_y - 280, 487,  horizon_y - 227, DEEP_WARM_SHAD),
        (507,  horizon_y - 127, 600,  horizon_y, TERRA_CYAN_LIT),
        (587,  horizon_y - 100, 680,  horizon_y, DEEP_WARM_SHAD),
        (667,  horizon_y - 147, 760,  horizon_y, TERRA_CYAN_LIT),
        (747,  horizon_y - 113, 840,  horizon_y, DEEP_WARM_SHAD),
        (827,  horizon_y - 160, 920,  horizon_y, TERRA_CYAN_LIT),
        (907,  horizon_y -  87, 1000, horizon_y, DEEP_WARM_SHAD),
        (987,  horizon_y - 133, 1080, horizon_y, TERRA_CYAN_LIT),
        (1067, horizon_y - 107, 1160, horizon_y, DEEP_WARM_SHAD),
        (1147, horizon_y - 140, W,    horizon_y, TERRA_CYAN_LIT),
    ]
    for (lx, ry, rx, gy, col) in buildings:
        draw.rectangle([lx, ry, rx, gy], fill=col)

    # C44: chimney coords scaled × 2/3
    chimneys = [
        (133, horizon_y - 147, 143, horizon_y - 127),
        (253, horizon_y - 143, 263, horizon_y - 127),
        (320, horizon_y - 187, 330, horizon_y - 167),
        (580, horizon_y - 140, 590, horizon_y - 120),
        (700, horizon_y - 160, 710, horizon_y - 140),
        (867, horizon_y - 173, 877, horizon_y - 153),
        (1033, horizon_y - 147, 1043, horizon_y - 127),
    ]
    for (x0, y0, x1, y1) in chimneys:
        draw.rectangle([x0, y0, x1, y1], fill=DEEP_COCOA)

    _draw_building_windows_with_glow(img, buildings, horizon_y)
    _draw_power_lines(img, horizon_y)
    _draw_building_storm_rims(img, buildings, horizon_y)

    draw = ImageDraw.Draw(img)
    for (x0, y0, x1, y1) in chimneys[:3]:
        draw.line([(x0, y0), (x0, y1)], fill=(*ELEC_CYAN, 60), width=1)
    return img


def _draw_building_windows_with_glow(img, buildings, horizon_y):
    """
    C22 fix: window pane alpha reduced to 115/110 (from 160/180).
    FIX 2 (C19): warm amber light cone below each lit window.
    """
    win_colors = [(*SOFT_GOLD, 115), (*WARM_CREAM, 110)]
    glow_overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(glow_overlay)

    for (lx, ry, rx, gy, _) in buildings:
        bld_w = rx - lx
        bld_h = gy - ry
        if bld_w < 40 or bld_h < 40:
            continue
        win_w = max(8, bld_w // 5)
        win_h = max(7, bld_h // 6)
        for row in range(2):
            for col in range(2):
                wx = lx + int(bld_w * (0.2 + col * 0.45))
                wy = ry + int(bld_h * (0.20 + row * 0.40))
                col_choice = RNG.choice(win_colors)
                if RNG.random() < 0.35:
                    continue

                od.rectangle([wx, wy, wx + win_w, wy + win_h], fill=col_choice)

                win_cx = wx + win_w // 2
                cone_top_y = wy + win_h
                cone_bot_y = min(gy, horizon_y + 20)
                if cone_bot_y <= cone_top_y:
                    continue
                cone_height = cone_bot_y - cone_top_y
                half_spread_top = win_w // 2
                half_spread_bot = int(win_w * 0.9)
                n_steps = max(6, cone_height // 6)
                for step in range(n_steps):
                    t_step = step / n_steps
                    step_y = int(cone_top_y + t_step * cone_height)
                    next_y = int(cone_top_y + (step + 1) / n_steps * cone_height)
                    half_w_step = int(half_spread_top + t_step * (half_spread_bot - half_spread_top))
                    a = int((1.0 - t_step ** 0.8) * 105)
                    a = max(0, min(255, a))
                    if a > 5 and step_y < next_y:
                        od.rectangle([win_cx - half_w_step, step_y,
                                      win_cx + half_w_step, next_y],
                                     fill=(*WIN_GLOW_WARM, a))

    img = alpha_paste(img, glow_overlay)
    return img


def _draw_building_storm_rims(img, buildings, horizon_y):
    """Storm edge-lighting on buildings — right/top edges ELEC_CYAN, base UV bounce."""
    crack_x = 933  # C44: 1400 × 2/3
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)

    for (lx, ry, rx, gy, col) in buildings:
        bld_cx = (lx + rx) / 2
        dist = abs(bld_cx - crack_x)
        rim_strength = clamp(1.0 - dist / 800.0, 0.0, 1.0)
        rim_alpha = int(30 + rim_strength * 90)

        rim_width = max(2, int(4 * rim_strength) + 1)
        od.rectangle([rx - rim_width, ry, rx, gy],
                     fill=(*STORM_RIM_CYAN, rim_alpha))

        top_alpha = int(20 + rim_strength * 60)
        od.rectangle([lx, ry, rx, ry + rim_width],
                     fill=(*STORM_RIM_CYAN, top_alpha))

        base_h = max(3, int((gy - ry) * 0.08))
        uv_alpha = int(25 + rim_strength * 40)
        od.rectangle([lx, gy - base_h, rx, gy],
                     fill=(*STORM_RIM_UV, uv_alpha))

    img = alpha_paste(img, overlay)
    return img


def _draw_power_lines(img, horizon_y):
    draw = ImageDraw.Draw(img)
    # C44: pole positions scaled × 2/3
    poles = [80, 213, 347, 507, 633, 767, 900, 1033, 1167]
    wire_y = horizon_y - 67  # C44: 100 × 2/3
    for i in range(len(poles) - 1):
        x0, x1 = poles[i], poles[i + 1]
        sag = int((x1 - x0) * 0.06)
        pts = []
        for s in range(6):
            t = s / 5.0
            x = int(x0 + t * (x1 - x0))
            y = wire_y + int(sag * 4 * t * (1 - t))
            pts.append((x, y))
        for j in range(len(pts) - 1):
            draw.line([pts[j], pts[j + 1]], fill=DEEP_COCOA, width=1)
    return img


# ── Layer 4: Street ───────────────────────────────────────────────────────────

def draw_street(img):
    draw = ImageDraw.Draw(img)
    horizon_y = int(H * 0.58)
    street_bottom = H
    draw.rectangle([0, horizon_y, W, street_bottom], fill=DARK_ASPHALT)
    sidewalk_top = horizon_y
    sidewalk_bottom = horizon_y + int((street_bottom - horizon_y) * 0.12)
    draw.rectangle([0, sidewalk_top, W, sidewalk_bottom], fill=COOL_SIDEWALK)

    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    crack_floor_x = 800   # C44: 1200 × 2/3
    pool_width = 373      # C44: 560 × 2/3
    pool_height = int((street_bottom - horizon_y) * 0.7)
    for col in range(pool_width):
        t = col / pool_width
        falloff = (1 - t) ** 2.0
        a = int(55 * falloff)
        x = crack_floor_x - col
        od.line([(x, horizon_y), (x, horizon_y + pool_height)], fill=(*CYAN_ROAD, a))
    img = alpha_paste(img, overlay)

    draw = ImageDraw.Draw(img)
    draw.line([(0, sidewalk_bottom), (W, sidewalk_bottom)], fill=VOID_BLACK, width=2)
    return img


# ── Layer 5: Damaged Storefront Window (lower-right) ─────────────────────────

def draw_storefront(img):
    """
    FIX 1 (C19): Genuine DAMAGED STOREFRONT WINDOW — structural frame + dividers +
    crack lines from 2 impact points + missing panes + debris scatter.
    """
    draw = ImageDraw.Draw(img)
    horizon_y = int(H * 0.58)

    sf_left  = int(W * 0.80)
    sf_right = int(W * 0.96)
    sf_top   = horizon_y - 67   # C44: 100 × 2/3
    sf_bot   = horizon_y + int((H - horizon_y) * 0.58)
    sf_w     = sf_right - sf_left
    sf_h     = sf_bot - sf_top

    FRAME_COL    = (60, 70, 80)
    INTERIOR     = (15, 12, 22)
    GLASS_REMAIN = (60, 90, 110)
    SHARD_EDGE   = (140, 200, 220)
    MISSING_PANE = (10, 10, 20)
    DEBRIS_COL   = (80, 72, 60)

    draw.rectangle([sf_left, sf_top, sf_right, sf_bot], fill=INTERIOR)

    frame_w = 5  # C44: 8 × 2/3 ≈ 5
    draw.rectangle([sf_left, sf_top, sf_right, sf_bot],
                   outline=FRAME_COL, width=frame_w)

    vert_1 = sf_left + sf_w // 3
    vert_2 = sf_left + 2 * sf_w // 3
    horiz_1 = sf_top + sf_h // 2
    bar_w = 4  # C44: 6 × 2/3 ≈ 4
    draw.rectangle([vert_1 - bar_w//2, sf_top, vert_1 + bar_w//2, sf_bot], fill=FRAME_COL)
    draw.rectangle([vert_2 - bar_w//2, sf_top, vert_2 + bar_w//2, sf_bot], fill=FRAME_COL)
    draw.rectangle([sf_left, horiz_1 - bar_w//2, sf_right, horiz_1 + bar_w//2], fill=FRAME_COL)

    panes = [
        (sf_left + frame_w, sf_top + frame_w, vert_1 - bar_w//2, horiz_1 - bar_w//2, False),
        (vert_1 + bar_w//2, sf_top + frame_w, vert_2 - bar_w//2, horiz_1 - bar_w//2, True),
        (vert_2 + bar_w//2, sf_top + frame_w, sf_right - frame_w, horiz_1 - bar_w//2, False),
        (sf_left + frame_w, horiz_1 + bar_w//2, vert_1 - bar_w//2, sf_bot - frame_w, True),
        (vert_1 + bar_w//2, horiz_1 + bar_w//2, vert_2 - bar_w//2, sf_bot - frame_w, False),
        (vert_2 + bar_w//2, horiz_1 + bar_w//2, sf_right - frame_w, sf_bot - frame_w, True),
    ]
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for (px0, py0, px1, py1, has_glass) in panes:
        if px1 <= px0 or py1 <= py0:
            continue
        if has_glass:
            od.rectangle([px0, py0, px1, py1], fill=(*GLASS_REMAIN, 160))
        else:
            od.rectangle([px0, py0, px1, py1], fill=(*MISSING_PANE, 255))
    img = alpha_paste(img, overlay)
    draw = ImageDraw.Draw(img)

    impact_pts = [
        (vert_1 + 20, sf_top + sf_h // 4),
        (sf_left + sf_w // 2 + 13, horiz_1 + 10),
    ]
    rng_crack = random.Random(77)
    for (ox, oy) in impact_pts:
        n_rays = rng_crack.randint(6, 8)
        for ri in range(n_rays):
            angle = (2 * math.pi * ri / n_rays) + rng_crack.uniform(-0.2, 0.2)
            length = rng_crack.randint(33, 80)  # C44: 50–120 × 2/3
            ex = int(ox + math.cos(angle) * length)
            ey = int(oy + math.sin(angle) * length)
            ex = clamp(ex, sf_left + frame_w, sf_right - frame_w)
            ey = clamp(ey, sf_top + frame_w, sf_bot - frame_w)
            draw.line([(ox, oy), (ex, ey)], fill=SHARD_EDGE, width=1)
            if rng_crack.random() < 0.5:
                mid_x = (ox + ex) // 2
                mid_y = (oy + ey) // 2
                branch_angle = angle + rng_crack.uniform(-0.8, 0.8)
                branch_len = rng_crack.randint(13, 37)  # C44: 20–55 × 2/3
                bx = int(mid_x + math.cos(branch_angle) * branch_len)
                by = int(mid_y + math.sin(branch_angle) * branch_len)
                bx = clamp(bx, sf_left + frame_w, sf_right - frame_w)
                by = clamp(by, sf_top + frame_w, sf_bot - frame_w)
                draw.line([(mid_x, mid_y), (bx, by)], fill=SHARD_EDGE, width=1)
        draw.ellipse([ox - 3, oy - 3, ox + 3, oy + 3], fill=INTERIOR)

    debris_y_base = sf_bot
    debris_zone_x0 = sf_left - 13
    debris_zone_x1 = sf_right + 7
    rng_debris = random.Random(44)
    for _ in range(22):
        dx = rng_debris.randint(debris_zone_x0, debris_zone_x1)
        dy = debris_y_base + rng_debris.randint(1, 30)
        if dy >= H:
            continue
        shard_w = rng_debris.randint(3, 9)
        shard_h = rng_debris.randint(2, 6)
        shard_pts = [
            (dx, dy - shard_h),
            (dx + shard_w, dy - shard_h + rng_debris.randint(-2, 2)),
            (dx + shard_w - 1, dy),
            (dx - 1, dy),
        ]
        draw.polygon(shard_pts, fill=GLASS_REMAIN, outline=SHARD_EDGE)
    for _ in range(30):
        dx = rng_debris.randint(debris_zone_x0, debris_zone_x1)
        dy = debris_y_base + rng_debris.randint(0, 20)
        if dy >= H:
            continue
        ds = rng_debris.randint(1, 3)
        draw.ellipse([dx - ds, dy - ds//2, dx + ds, dy + ds//2], fill=DEBRIS_COL)

    draw.rectangle([sf_left, sf_top, sf_right, sf_bot],
                   outline=(*HOT_MAGENTA,), width=2)

    return img


# ═══════════════════════════════════════════════════════════════════════════════
# Layer 6: Characters — pycairo bezier rendering (C53)
# ═══════════════════════════════════════════════════════════════════════════════

SCENE_COOL_TINT = (0, 200, 220)
SCENE_WARM_TINT = (255, 140, 0)
SCENE_COOL_INFLUENCE = 0.20
SCENE_WARM_INFLUENCE = 0.08


def _draw_glitch_storm_cairo(cx, cy, body_h):
    """Draw Glitch using pycairo bezier curves. Returns RGBA PIL image at W x H.
    G007: VOID_BLACK outline width=3 as spec 2.2. Crown spike, pixel-art eyes.
    Falls back to PIL if pycairo unavailable.
    """
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)

    rx = int(body_h * 0.88)
    ry = body_h
    tilt_deg = 8
    angle = math.radians(tilt_deg)

    top   = (cx + int(rx * 0.15 * math.sin(angle)),  cy - ry + int(rx * 0.15 * math.cos(angle)))
    right = (cx + int(rx * math.cos(-angle)),          cy + int(rx * 0.2 * math.sin(-angle)))
    bot   = (cx - int(rx * 0.15 * math.sin(angle)),  cy + int(ry * 1.15))
    left  = (cx - int(rx * math.cos(-angle)),          cy - int(rx * 0.2 * math.sin(-angle)))
    pts = [top, right, bot, left]

    sh_pts = [(x + 2, y + 3) for x, y in pts]
    od.polygon(sh_pts, fill=(*UV_PURPLE, 200))

    od.polygon(pts, fill=(*CORRUPT_AMBER, 240))

    ctr = (cx, cy - ry // 4)
    mid_tl = ((top[0] + left[0]) // 2, (top[1] + left[1]) // 2)
    od.polygon([top, ctr, mid_tl], fill=(*((255, 185, 80)), 220))

    od.polygon(pts, outline=(*VOID_BLACK, 255), width=3)

    cs = (cx - rx // 2, cy - ry // 3)
    ce = (cx + rx // 3, cy + ry // 2)
    od.line([cs, ce], fill=(*HOT_MAGENTA, 230), width=2)
    mid_c = ((cs[0] + ce[0]) // 2, (cs[1] + ce[1]) // 2)
    od.line([mid_c, (cx + rx // 2, cy - ry // 4)], fill=(*HOT_MAGENTA, 200), width=1)

    spike_h = max(3, ry // 2)
    spk_x = cx + int(rx * 0.15 * math.sin(angle))
    cy_top = top[1]
    spike_pts = [
        (spk_x - spike_h // 2, cy_top),
        (spk_x - spike_h,      cy_top - spike_h),
        (spk_x,                cy_top - spike_h * 2),
        (spk_x + spike_h,      cy_top - spike_h),
        (spk_x + spike_h // 2, cy_top),
    ]
    od.polygon(spike_pts, fill=(*CORRUPT_AMBER, 240))
    od.polygon(spike_pts, outline=(*VOID_BLACK, 255), width=2)
    od.line([(spk_x, cy_top - spike_h * 2), (spk_x, cy_top - spike_h * 2 - max(1, ry // 8))],
            fill=(*HOT_MAGENTA, 220), width=2)

    eye_cell = max(2, rx // 5)
    face_cy = cy - ry // 6
    le_cx = cx - rx // 3
    od.rectangle([le_cx - eye_cell, face_cy - eye_cell, le_cx + eye_cell, face_cy + eye_cell],
                 fill=(*UV_PURPLE, 230))
    od.rectangle([le_cx - eye_cell // 2, face_cy - eye_cell // 2,
                  le_cx + eye_cell // 2, face_cy + eye_cell // 2],
                 fill=(*ACID_GREEN, 255))
    re_cx = cx + rx // 3
    od.rectangle([re_cx - eye_cell, face_cy - eye_cell, re_cx + eye_cell, face_cy + eye_cell],
                 fill=(*UV_PURPLE, 230))
    od.rectangle([re_cx - eye_cell // 2, face_cy - eye_cell // 2,
                  re_cx + eye_cell // 2, face_cy + eye_cell // 2],
                 fill=(*ACID_GREEN, 255))

    rng_gc = random.Random(77)
    for _ in range(6):
        px = cx + rng_gc.randint(-rx * 2, rx * 2)
        py = cy + rng_gc.randint(-ry * 2, ry * 2)
        ps = rng_gc.randint(2, 3)
        od.rectangle([px, py, px + ps, py + ps], fill=(*ACID_GREEN, 180))

    return overlay


def draw_characters(img):
    """Character layout — sprinting left-to-right across frame.
    C54: Luma, Cosmo, Byte use canonical char_*.py renderers.
    Glitch uses local pycairo renderer (unchanged).
    """
    horizon_y = int(H * 0.58)
    ground_y  = horizon_y + int((H - horizon_y) * 0.12)
    char_h = int(H * 0.18)

    luma_cx = int(W * 0.45)
    luma_foot_y = ground_y + sp(7)
    luma_head_cy = luma_foot_y - char_h

    byte_cx = int(W * 0.28)
    byte_float_y = luma_head_cy + int(char_h * 0.30)

    cosmo_cx = int(W * 0.62)
    cosmo_foot_y = ground_y + sp(9)

    glitch_cx = int(W * 0.78)
    glitch_cy = int(H * 0.32)
    glitch_body_h = int(char_h * 0.50)

    # Glitch — pycairo local renderer (background character, unchanged)
    glitch_layer = _draw_glitch_storm_cairo(glitch_cx, glitch_cy, glitch_body_h)
    base_rgba = img.convert("RGBA")
    base_rgba = Image.alpha_composite(base_rgba, glitch_layer)
    img = base_rgba.convert("RGB")

    # ── C54: Canonical character renderers ───────────────────────────────────
    if _CHAR_CANONICAL and _CAIRO_OK:
        # Luma — DETERMINED sprint: scale = char_h / 400 (base_char_h in char_luma)
        luma_scale = char_h / 400.0
        luma_surf = _draw_luma_canonical(
            "DETERMINED", scale=luma_scale, facing="right",
            scene_lighting={"key_light_dir": "left", "ambient": (26, 20, 40)})
        luma_pil = _cairo_char_to_pil(luma_surf)
        if luma_pil.height > 0:
            aspect = luma_pil.width / luma_pil.height
            luma_pil = luma_pil.resize((int(char_h * aspect), char_h), Image.LANCZOS)
        img = _composite_canonical_char(img, luma_pil, luma_cx, luma_foot_y)

        # Cosmo — WORRIED panic run: base_hu=84, char_h ≈ 3.5*hu → scale = char_h / (3.5*84)
        cosmo_scale = char_h / (3.5 * 84.0)
        cosmo_surf, _cosmo_geom = _draw_cosmo_canonical(
            "WORRIED", scale=cosmo_scale, facing="right", notebook_show=False,
            scene_lighting={"preset": "neutral_daylight"})
        cosmo_pil = _cairo_char_to_pil(cosmo_surf)
        if cosmo_pil.height > 0:
            aspect = cosmo_pil.width / cosmo_pil.height
            cosmo_pil = cosmo_pil.resize((int(char_h * aspect), char_h), Image.LANCZOS)
        img = _composite_canonical_char(img, cosmo_pil, cosmo_cx, cosmo_foot_y)

        # Byte — alarmed hovering: target height = char_h * 0.40 (preserves original scale)
        byte_target_h = int(char_h * 0.40)
        byte_scale = byte_target_h / 88.0
        byte_surf = _draw_byte_canonical(
            "alarmed", scale=byte_scale, facing="front",
            scene_lighting={"tint": ELEC_CYAN, "intensity": 0.25})
        byte_pil = _cairo_char_to_pil(byte_surf)
        if byte_pil.height > 0:
            aspect = byte_pil.width / byte_pil.height
            byte_pil = byte_pil.resize((int(byte_target_h * aspect), byte_target_h), Image.LANCZOS)
        # Byte hovers: center at byte_float_y (feet at float_y + half height)
        byte_foot_y = byte_float_y + byte_pil.height // 2
        img = _composite_canonical_char(img, byte_pil, byte_cx, byte_foot_y)

    else:
        # Fallback: original PIL character rendering
        print("  [C54 FALLBACK] Using original PIL characters (canonical renderers unavailable).")
        img = _draw_luma(img, luma_cx, luma_foot_y, char_h)
        img = _draw_cosmo(img, cosmo_cx, cosmo_foot_y, char_h)
        img = _draw_byte_hovering(img, byte_cx, byte_float_y, char_h)

    img = _draw_townspeople(img, horizon_y)

    return img


def _draw_luma_face_sprint(draw, cx, head_cy, head_r):
    """
    C35: FOCUSED DETERMINATION expression for Luma in sprint.
    Asymmetric eyes, inward left brow, level right brow, compressed jaw-set mouth.
    """
    eye_r_left  = max(2, int(head_r * 0.26))
    eye_r_right = max(2, int(head_r * 0.17))

    eye_y_offset  = -int(head_r * 0.15)
    left_eye_cx   = cx - int(head_r * 0.30)
    right_eye_cx  = cx + int(head_r * 0.22)
    left_eye_cy   = head_cy + eye_y_offset
    right_eye_cy  = head_cy + eye_y_offset + int(head_r * 0.08)

    draw.ellipse([left_eye_cx  - eye_r_left,  left_eye_cy  - eye_r_left,
                  left_eye_cx  + eye_r_left,  left_eye_cy  + eye_r_left],
                 fill=WARM_CREAM)
    draw.ellipse([right_eye_cx - eye_r_right, right_eye_cy - eye_r_right,
                  right_eye_cx + eye_r_right, right_eye_cy + eye_r_right],
                 fill=WARM_CREAM)

    pupil_r = max(1, int(head_r * 0.09))
    lp_cx = left_eye_cx  + max(1, int(eye_r_left  * 0.25))
    lp_cy = left_eye_cy  + max(1, int(eye_r_left  * 0.20))
    rp_cx = right_eye_cx + max(1, int(eye_r_right * 0.25))
    rp_cy = right_eye_cy + max(1, int(eye_r_right * 0.20))
    draw.ellipse([lp_cx - pupil_r, lp_cy - pupil_r, lp_cx + pupil_r, lp_cy + pupil_r],
                 fill=DEEP_COCOA)
    draw.ellipse([rp_cx - pupil_r, rp_cy - pupil_r, rp_cx + pupil_r, rp_cy + pupil_r],
                 fill=DEEP_COCOA)

    draw.ellipse([left_eye_cx  - eye_r_left,  left_eye_cy  - eye_r_left,
                  left_eye_cx  + eye_r_left,  left_eye_cy  + eye_r_left],
                 outline=DEEP_COCOA, width=1)
    draw.ellipse([right_eye_cx - eye_r_right, right_eye_cy - eye_r_right,
                  right_eye_cx + eye_r_right, right_eye_cy + eye_r_right],
                 outline=DEEP_COCOA, width=1)

    brow_y_base = head_cy - int(head_r * 0.40)
    brow_width  = int(head_r * 0.35)

    lbrow_x0 = left_eye_cx  - brow_width // 2
    lbrow_y0 = brow_y_base
    lbrow_x1 = left_eye_cx  + brow_width // 2
    lbrow_y1 = brow_y_base + int(head_r * 0.12)
    draw.line([(lbrow_x0, lbrow_y0), (lbrow_x1, lbrow_y1)],
              fill=DEEP_COCOA, width=max(1, int(head_r * 0.08)))

    rbrow_x0 = right_eye_cx - brow_width // 2
    rbrow_y0 = brow_y_base
    rbrow_x1 = right_eye_cx + brow_width // 2
    rbrow_y1 = brow_y_base
    draw.line([(rbrow_x0, rbrow_y0), (rbrow_x1, rbrow_y1)],
              fill=DEEP_COCOA, width=max(1, int(head_r * 0.07)))

    mouth_y = head_cy + int(head_r * 0.42)
    mouth_w = int(head_r * 0.40)
    draw.line([(cx - mouth_w // 2, mouth_y), (cx + mouth_w // 2, mouth_y)],
              fill=DEEP_COCOA, width=max(1, int(head_r * 0.09)))


def _draw_luma(img, cx, foot_y, h):
    """Luma sprinting. CORRUPT_AMBER outline, C35 lean/face. Returns composited img."""
    head_r  = int(h * 0.12)
    torso_h = int(h * 0.28)
    torso_w = int(h * 0.17)
    leg_h   = int(h * 0.38)

    head_cy   = foot_y - h + head_r

    lean_offset = int(torso_h * math.tan(math.radians(10)))
    torso_top = head_cy + head_r + 2
    torso_bot = torso_top + torso_h

    torso_cx_top  = cx - lean_offset
    torso_cx_bot  = cx
    torso_left_top  = torso_cx_top  - torso_w // 2
    torso_right_top = torso_cx_top  + torso_w // 2
    torso_left_bot  = torso_cx_bot  - torso_w // 2
    torso_right_bot = torso_cx_bot  + torso_w // 2

    head_cx = cx - lean_offset // 2

    outline_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ol = ImageDraw.Draw(outline_layer)
    torso_outline_pts = [
        (torso_left_top - 2,  torso_top - 2),
        (torso_right_top + 2, torso_top - 2),
        (torso_right_bot + 2, torso_bot + 2),
        (torso_left_bot - 2,  torso_bot + 2),
    ]
    ol.polygon(torso_outline_pts, outline=(*CORRUPT_AMBER, 220))
    ol.ellipse([head_cx - head_r - 2, head_cy - head_r - 2,
                head_cx + head_r + 2, head_cy + head_r + 2],
               outline=(*CORRUPT_AMBER, 180), width=2)
    img = alpha_paste(img, outline_layer)

    shadow_overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow_overlay)
    shadow_pts = [
        (torso_left_top,     torso_top),
        ((torso_cx_top),     torso_top),
        ((torso_cx_bot),     torso_bot),
        (torso_left_bot,     torso_bot),
    ]
    sd.polygon(shadow_pts, fill=(*DRW_HOODIE_SHADOW, 255))
    img = alpha_paste(img, shadow_overlay)

    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)

    torso_fill_pts = [
        (torso_left_top,  torso_top),
        (torso_right_top, torso_top),
        (torso_right_bot, torso_bot),
        (torso_left_bot,  torso_bot),
    ]
    od.polygon(torso_fill_pts, fill=(*DRW_HOODIE_STORM, 255))

    od.ellipse([head_cx - head_r, head_cy - head_r,
                head_cx + head_r, head_cy + head_r],
               fill=(*DRW_SKIN_STORM, 255))

    od.arc([head_cx - head_r, head_cy - head_r,
            head_cx + head_r, head_cy + head_r],
           start=190, end=360, fill=DEEP_COCOA, width=int(head_r * 0.5))
    od.arc([head_cx - head_r + 2, head_cy - head_r + 2,
            head_cx + head_r - 2, head_cy + head_r - 2],
           start=190, end=330, fill=DRW_HAIR_MAGENTA, width=2)

    left_leg_pts = [(cx - 5, torso_bot), (cx + 20, torso_bot + int(leg_h * 0.55)), (cx + 33, foot_y)]
    for i in range(len(left_leg_pts) - 1):
        od.line([left_leg_pts[i], left_leg_pts[i + 1]], fill=(*DRW_HOODIE_STORM, 255), width=int(torso_w * 0.35))

    right_leg_pts = [(cx + 5, torso_bot), (cx - 17, torso_bot + int(leg_h * 0.50)), (cx - 27, foot_y - int(leg_h * 0.15))]
    for i in range(len(right_leg_pts) - 1):
        od.line([right_leg_pts[i], right_leg_pts[i + 1]], fill=(*DRW_HOODIE_SHADOW, 255), width=int(torso_w * 0.30))

    od.line([(torso_cx_bot - int(torso_w * 0.45), torso_top + int(torso_h * 0.20)),
             (torso_cx_bot + int(torso_w * 0.30), torso_top - int(h * 0.45 * 0.45))],
            fill=(*DRW_HOODIE_STORM, 255), width=int(torso_w * 0.30))
    od.line([(torso_cx_bot + int(torso_w * 0.35), torso_top + int(torso_h * 0.20)),
             (torso_cx_bot - int(torso_w * 0.60), torso_top + int(h * 0.26 * 0.65))],
            fill=(*DRW_HOODIE_SHADOW, 255), width=int(torso_w * 0.28))

    hair_anchor = (head_cx - head_r + 3, head_cy)
    hair_stream = [
        hair_anchor,
        (head_cx - head_r - int(h * 0.09), head_cy + int(h * 0.01)),
        (head_cx - head_r - int(h * 0.16), head_cy + int(h * 0.005)),
    ]
    for i in range(len(hair_stream) - 1):
        od.line([hair_stream[i], hair_stream[i + 1]], fill=DEEP_COCOA, width=4)
    od.line([hair_stream[0], hair_stream[-1]], fill=DRW_HAIR_MAGENTA, width=2)

    fine_strand = [
        (head_cx - head_r + 1, head_cy + int(head_r * 0.20)),
        (head_cx - head_r - int(h * 0.07), head_cy + int(h * 0.02)),
        (head_cx - head_r - int(h * 0.13), head_cy + int(h * 0.015)),
    ]
    for i in range(len(fine_strand) - 1):
        od.line([fine_strand[i], fine_strand[i + 1]], fill=DEEP_COCOA, width=2)

    shadow_pts = [
        (cx - int(torso_w * 0.8), foot_y + 3), (cx + int(torso_w * 0.8), foot_y + 3),
        (cx + int(torso_w * 1.8), foot_y + 9), (cx - int(torso_w * 1.2), foot_y + 9),
    ]
    od.polygon(shadow_pts, fill=(10, 42, 58, 120))

    img = alpha_paste(img, overlay)

    face_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    face_draw = ImageDraw.Draw(face_img)
    _draw_luma_face_sprint(face_draw, head_cx, head_cy, head_r)
    img = alpha_paste(img, face_img)

    return img


def _draw_cosmo(img, cx, foot_y, h):
    """Cosmo: one stride behind Luma, panic run, glasses."""
    head_r  = int(h * 0.115)
    torso_h = int(h * 0.26)
    torso_w = int(h * 0.155)
    leg_h   = int(h * 0.37)

    head_cy   = foot_y - h + head_r
    torso_top = head_cy + head_r + 2
    torso_bot = torso_top + torso_h
    torso_left  = cx - torso_w // 2
    torso_right = cx + torso_w // 2

    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)

    od.ellipse([torso_left, torso_top, torso_right, torso_bot], fill=(*DRW_JACKET_STORM, 255))
    od.ellipse([torso_left, torso_top, cx, torso_bot], fill=(*DRW_JACKET_SHADOW, 255))
    od.ellipse([cx - head_r, head_cy - head_r, cx + head_r, head_cy + head_r],
               fill=(*DRW_SKIN_STORM, 255))

    gx0 = cx - int(head_r * 0.55); gy0 = head_cy - int(head_r * 0.08)
    gw, gh = int(head_r * 0.60), int(head_r * 0.40)
    od.rectangle([gx0, gy0, gx0 + gw, gy0 + gh], outline=DEEP_COCOA, width=2)
    od.rectangle([gx0 + 2, gy0 + 2, gx0 + gw - 2, gy0 + gh - 2], fill=(*ELEC_CYAN, 100))
    od.rectangle([gx0 + gw + 3, gy0, gx0 + gw * 2 + 3, gy0 + gh], outline=DEEP_COCOA, width=2)
    od.rectangle([gx0 + gw + 4, gy0 + 2, gx0 + gw * 2 + 1, gy0 + gh - 2], fill=(*ELEC_CYAN, 100))

    od.ellipse([cx - int(head_r * 0.35), head_cy + int(head_r * 0.30),
                cx + int(head_r * 0.35), head_cy + int(head_r * 0.65)], fill=VOID_BLACK)

    for (dx, dy, shadow) in [(-8, torso_bot, False), (8, torso_bot, True)]:
        lx = cx + dx
        endx = lx + (17 if not shadow else -13)
        endy = foot_y - int(leg_h * 0.10 if not shadow else 0.25)
        col = DRW_JACKET_STORM if not shadow else DRW_JACKET_SHADOW
        od.line([(lx, dy), (endx, endy), (endx + (10 if not shadow else -7), foot_y)],
                fill=(*col, 255), width=int(torso_w * 0.32))

    od.line([(cx - int(torso_w * 0.4), torso_top + int(torso_h * 0.15)),
             (cx + int(torso_w * 0.2), head_cy - int(h * 0.08))],
            fill=(*DRW_JACKET_STORM, 255), width=int(torso_w * 0.28))
    od.line([(cx + int(torso_w * 0.4), torso_top + int(torso_h * 0.15)),
             (cx - int(torso_w * 0.2), head_cy - int(h * 0.08))],
            fill=(*DRW_JACKET_SHADOW, 255), width=int(torso_w * 0.28))

    od.line([(cx - int(torso_w * 0.35), torso_top + 3),
             (cx - int(torso_w * 0.50), torso_top + int(torso_h * 0.60))],
            fill=WARM_CREAM, width=2)

    img = alpha_paste(img, overlay)
    return img


def _draw_byte_hovering(img, cx, cy, char_h):
    """Byte hovering in storm. CORRUPT_AMBER outline + void body + BYTE_TEAL inner trace."""
    byte_h = int(char_h * 0.40)
    byte_w = int(byte_h * 1.30)

    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)

    body_top  = cy - byte_h // 2
    body_bot  = cy + byte_h // 2
    body_left = cx - byte_w // 2
    body_right= cx + byte_w // 2

    od.rectangle([body_left, body_top, body_right, body_bot],
                 fill=(*VOID_BLACK, 255), outline=(*CORRUPT_AMBER, 255), width=3)

    screen_pad = max(3, byte_w // 8)
    screen_left  = body_left  + screen_pad
    screen_right = body_right - screen_pad
    screen_top   = body_top   + screen_pad
    screen_bot   = body_bot   - int(byte_h * 0.28)
    od.rectangle([screen_left, screen_top, screen_right, screen_bot],
                 fill=(*BYTE_TEAL, 255), outline=(*CORRUPT_AMBER, 180), width=1)

    eye_y = screen_top + (screen_bot - screen_top) // 2
    eye_spacing = (screen_right - screen_left) // 3
    left_eye_x  = screen_left  + eye_spacing
    right_eye_x = screen_right - eye_spacing
    eye_r = max(2, byte_h // 8)
    od.ellipse([left_eye_x  - eye_r, eye_y - eye_r,
                left_eye_x  + eye_r, eye_y + eye_r], fill=VOID_BLACK)
    od.ellipse([right_eye_x - eye_r, eye_y - eye_r,
                right_eye_x + eye_r, eye_y + eye_r], fill=VOID_BLACK)

    ant_x = cx
    ant_base_y = body_top
    ant_top_y  = body_top - int(byte_h * 0.40)
    od.line([(ant_x, ant_base_y), (ant_x, ant_top_y)],
            fill=(*CORRUPT_AMBER, 200), width=2)
    ball_r = max(2, byte_h // 10)
    od.ellipse([ant_x - ball_r, ant_top_y - ball_r,
                ant_x + ball_r, ant_top_y + ball_r], fill=(*ELEC_CYAN, 255))

    leg_y = body_bot
    for leg_dx in [-int(byte_w * 0.35), int(byte_w * 0.35)]:
        od.line([(cx + leg_dx, leg_y), (cx + leg_dx, leg_y + int(byte_h * 0.30))],
                fill=(*CORRUPT_AMBER, 180), width=2)

    img = alpha_paste(img, overlay)
    return img


def _draw_townspeople(img, horizon_y):
    """Background townspeople — tiny silhouettes running or cowering."""
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)

    ground_y = horizon_y + int((H - horizon_y) * 0.12)
    # C44: x positions scaled × 2/3; head heights scaled × 2/3
    people = [
        (133, ground_y, 8), (173, ground_y, 7), (227, ground_y - 3, 7),
        (333, ground_y, 9), (367, ground_y, 6),
        (453, ground_y - 1, 7), (480, ground_y, 5),
        (680, ground_y, 8), (720, ground_y, 7),
        (1000, ground_y, 7), (1027, ground_y, 6),
        (1093, ground_y, 7), (1120, ground_y - 2, 8),
        (1187, ground_y, 5), (1213, ground_y, 7),
    ]
    for (px, py, ph) in people:
        body_col = (*DEEP_WARM_SHAD, 200)
        od.ellipse([px - ph // 3, py - ph,
                    px + ph // 3, py - int(ph * 0.65)], fill=body_col)
        od.rectangle([px - ph // 4, py - int(ph * 0.65),
                      px + ph // 4, py - int(ph * 0.25)], fill=body_col)
        od.line([(px - ph // 4, py - int(ph * 0.25)),
                 (px - ph // 2, py + 1)], fill=body_col, width=1)
        od.line([(px + ph // 4, py - int(ph * 0.25)),
                 (px + ph // 3, py + 1)], fill=body_col, width=1)

    img = alpha_paste(img, overlay)
    return img


# ── Layer 6b: Magenta Fill Light (C36 — corrected direction + character mask) ─

def _make_char_silhouette_mask(img, char_cx, char_h, char_cy, threshold=60):
    """
    Build per-character silhouette mask at native resolution (W×H).
    C44: renamed from _make_char_silhouette_mask_1080 — no longer 1080p-specific.
    """
    zone_w = int(char_h * 2.0)
    zone_h = int(char_h * 2.5)
    x0 = max(0, char_cx - zone_w // 2)
    y0 = max(0, char_cy - zone_h // 2)
    x1 = min(W, char_cx + zone_w // 2)
    y1 = min(H, char_cy + zone_h)

    crop = img.crop((x0, y0, x1, y1))
    gray = crop.convert("L")
    mask_crop = gray.point(lambda p: 255 if p > threshold else 0, mode="L")

    full_mask = Image.new("L", (W, H), 0)
    full_mask.paste(mask_crop, (x0, y0))

    full_mask_blur = full_mask.filter(ImageFilter.GaussianBlur(radius=4))
    full_mask_dilated = full_mask_blur.point(lambda p: 255 if p > 30 else 0, mode="L")

    return full_mask_dilated


def draw_magenta_fill_light_c36(img, luma_cx, byte_cx, cosmo_cx, char_h):
    """
    C36 CORRECTED HOT_MAGENTA fill light.
    Source: UPPER-RIGHT of each character (matching storm crack at upper-right canvas).
    Per-character silhouette mask applied via ImageChops.multiply — no BG tint.
    """
    horizon_y = int(H * 0.58)
    ground_y  = horizon_y + int((H - horizon_y) * 0.12)

    FILL_ALPHA_MAX    = 35
    FILL_RADIUS_SCALE = 1.6

    char_centers = [
        (luma_cx,  int(H * 0.65), "luma"),
        (byte_cx,  int(H * 0.60), "byte"),
        (cosmo_cx, int(H * 0.65), "cosmo"),
    ]

    for (char_cx_pos, char_cy_pos, char_name) in char_centers:
        char_mask = _make_char_silhouette_mask(
            img, char_cx_pos, char_h, char_cy_pos, threshold=60
        )

        fill_overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        fd = ImageDraw.Draw(fill_overlay)

        fill_src_x = char_cx_pos + int(char_h * 0.5)
        fill_src_y = char_cy_pos - int(char_h * 0.8)
        fill_r = int(char_h * FILL_RADIUS_SCALE)

        for r_step in range(fill_r, 0, -max(1, fill_r // 30)):
            t = 1.0 - (r_step / fill_r)
            a = int(FILL_ALPHA_MAX * (t ** 1.3))
            a = max(0, min(255, a))
            if a < 2:
                continue
            fd.ellipse([fill_src_x - r_step, fill_src_y - r_step,
                        fill_src_x + r_step, fill_src_y + r_step],
                       fill=(*HOT_MAGENTA, a))

        r_ch, g_ch, b_ch, a_ch = fill_overlay.split()
        masked_alpha = ImageChops.multiply(a_ch, char_mask)
        masked_fill = Image.merge("RGBA", (r_ch, g_ch, b_ch, masked_alpha))

        img = alpha_paste(img, masked_fill)

    return img


# ── Layer 6c: Cyan Specular on Luma (C34, fixed C35) ──────────────────────────

def draw_cyan_specular_luma(img, luma_cx, char_h):
    """
    C34 FIX 2 / C35 BUG FIX: ELEC_CYAN specular on Luma hair/shoulders.
    C35 FIX: use luma_cx directly — do NOT call get_char_bbox on full frame.
    C44: No post-thumbnail specular restore needed — native canvas renders correctly.
    """
    if PROCEDURAL_DRAW_AVAILABLE:
        add_rim_light(
            img,
            threshold=180,
            light_color=ELEC_CYAN,
            width=2,
            side="right",
            char_cx=luma_cx
        )
    else:
        head_r = int(char_h * 0.12)
        luma_foot_y_approx = int(H * 0.58) + int((H - int(H * 0.58)) * 0.12) + 7
        head_cy = luma_foot_y_approx - char_h + head_r
        overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        od = ImageDraw.Draw(overlay)
        od.arc([luma_cx - head_r - 2, head_cy - head_r - 2,
                luma_cx + head_r + 2, head_cy + head_r + 2],
               start=310, end=60, fill=(*ELEC_CYAN, 140), width=2)
        torso_h = int(char_h * 0.28)
        torso_w = int(char_h * 0.17)
        torso_top = head_cy + head_r + 2
        od.arc([luma_cx - torso_w // 2, torso_top,
                luma_cx + torso_w // 2, torso_top + int(torso_h * 0.5)],
               start=340, end=60, fill=(*ELEC_CYAN, 100), width=2)
        img = alpha_paste(img, overlay)

    return img


# ── Layer 7: Ground lighting ──────────────────────────────────────────────────

def draw_ground_lighting(img):
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    horizon_y = int(H * 0.58)
    crack_x = 867     # C44: 1300 × 2/3
    pool_w = 467      # C44: 700 × 2/3
    for col in range(pool_w):
        x = crack_x - col
        if x < 0: break
        t = col / pool_w; falloff = (1 - t) ** 1.8; a = int(45 * falloff)
        od.line([(x, horizon_y), (x, H)], fill=(*ELEC_CYAN, a))
    img = alpha_paste(img, overlay)
    return img


# ── Layer 8: Dutch Angle ──────────────────────────────────────────────────────

def apply_dutch_angle(img, degrees=4.0):
    """4.0° Dutch angle as final step — visibly perceptible camera tilt."""
    rotated = img.rotate(-degrees, expand=True, resample=Image.BICUBIC, fillcolor=VOID_BLACK)
    rw, rh = rotated.size
    cx, cy = rw // 2, rh // 2
    left   = cx - W // 2
    top    = cy - H // 2
    cropped = rotated.crop((left, top, left + W, top + H))
    return cropped


# ── Main ──────────────────────────────────────────────────────────────────────

def render_environment():
    """Render environment at W_ENV x H_ENV (1280x720). Returns PIL RGB image.

    Temporarily swaps W, H globals so environment functions use 1280x720 coordinates.
    """
    global W, H
    W_save, H_save = W, H
    W, H = W_ENV, H_ENV

    img = Image.new("RGB", (W, H), VOID_BLACK)
    img = draw_sky(img)
    img = draw_storm_confetti(img)
    img = draw_town_silhouette(img)
    img = draw_street(img)
    img = draw_ground_lighting(img)
    img = draw_storefront(img)

    W, H = W_save, H_save
    return img


def main(skip_fill_light=False):
    """
    Render Style Frame 02 — Glitch Storm.
    C53: pycairo characters + Wand compositing + 2x AA render.

    Args:
        skip_fill_light (bool): If True, omit fill light and specular.
    """
    out_path = NOLIGHT_PATH if skip_fill_light else OUTPUT_PATH
    print("LTG_TOOL_style_frame_02_glitch_storm.py")
    print(f"Rendering SF02 Glitch Storm (C54 canonical characters)...")
    print(f"  pycairo={_CAIRO_OK}, canonical_chars={_CHAR_CANONICAL}, Wand={_WAND_OK}, scipy={_SCIPY_OK}")
    print(f"  Internal: {W}x{H} -> Output: {W_OUT}x{H_OUT}")
    if skip_fill_light:
        print("  [nolight mode] Skipping fill light + specular")

    # STEP 1: Environment at 1280x720
    print("  [1/10] Environment layers at 1280x720...")
    env_img = render_environment()

    # STEP 2: Upscale environment to 2x for compositing with characters
    print("  [2/10] Upscaling environment to 2x (2560x1440)...")
    img = env_img.resize((W, H), Image.LANCZOS)

    # Character geometry at 2x
    char_h    = int(H * 0.18)
    luma_cx   = int(W * 0.45)
    byte_cx   = int(W * 0.28)
    cosmo_cx  = int(W * 0.62)

    # STEP 3: Characters at 2x (uses W, H = 2560x1440)
    print("  [3/10] Characters (pycairo bezier + Wand compositing at 2x)...")
    img = draw_characters(img)

    # STEP 4: Fill light + specular at 2x
    if skip_fill_light:
        print("  [4/10] Magenta fill light — SKIPPED (nolight mode)")
        print("  [5/10] Cyan specular — SKIPPED (nolight mode)")
    else:
        print("  [4/10] Magenta fill light (C36: UPPER-RIGHT, per-char mask at 2x)...")
        img = draw_magenta_fill_light_c36(img, luma_cx, byte_cx, cosmo_cx, char_h)

        print("  [5/10] Cyan specular on Luma at 2x...")
        img = draw_cyan_specular_luma(img, luma_cx, char_h)

    # STEP 6: Dutch angle at 2x
    print("  [6/10] Dutch angle (4.0 deg) at 2x...")
    img = apply_dutch_angle(img, degrees=4.0)

    # STEP 7: Downscale 2x -> 1280x720 with LANCZOS
    print("  [7/10] LANCZOS downscale to 1280x720...")
    img = img.resize((W_OUT, H_OUT), Image.LANCZOS)

    # Size rule enforcement
    assert img.size[0] <= 1280 and img.size[1] <= 1280, \
        f"Canvas exceeds 1280px limit: {img.size}"

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img.save(out_path, "PNG")
    label = "nolight base" if skip_fill_light else "composited"
    print(f"\nSaved ({label}): {out_path}")
    size_bytes = os.path.getsize(out_path)
    print(f"File size: {size_bytes:,} bytes ({size_bytes // 1024} KB)")
    print(f"Image size: {img.size[0]}x{img.size[1]}px")
    print("\nC54 verification:")
    print(f"  [C54] Canonical character renderers: {_CHAR_CANONICAL}")
    print(f"  [C54] draw_luma(DETERMINED) + draw_cosmo(WORRIED) + draw_byte(alarmed)")
    print(f"  [C53] pycairo character rendering: {_CAIRO_OK}")
    print(f"  [C53] Wand compositing: {_WAND_OK}")
    print(f"  [C53] 2x internal render ({W}x{H}) -> LANCZOS downscale ({W_OUT}x{H_OUT})")
    print("  [C53] Environment at 1280x720, upscaled for character compositing")
    print("  [C47] Shoulder involvement on character shapes")
    print("  [C36] Fill light: UPPER-RIGHT, per-char silhouette mask")
    print("  [C35] Focused determination face, 10 deg lean, hair stream")
    print("  [C34] Cyan specular: ELEC_CYAN add_rim_light side='right'")
    print("  [C22] CORRUPT_AMBER = (255,140,0) #FF8C00 GL-07")
    print("  [C19] Storefront: frame + dividers + cracked panes + debris")
    print("  [C16] Dutch angle: 4.0 deg, cold confetti DATA_BLUE 70%")
    print("\nDone.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="LTG_TOOL_style_frame_02_glitch_storm.py — Style Frame 02: Glitch Storm"
    )
    parser.add_argument(
        "--save-nolight",
        action="store_true",
        help=(
            "Also save an unlit base image (no magenta fill light, no cyan specular) "
            "as LTG_COLOR_styleframe_glitch_storm_nolight.png. Dutch angle is still "
            "applied. Enables Section 10 (alpha_blend_lint) in precritique_qa.py."
        ),
    )
    args = parser.parse_args()

    main()
    if args.save_nolight:
        main(skip_fill_light=True)
