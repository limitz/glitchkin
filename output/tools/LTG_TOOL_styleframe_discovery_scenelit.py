#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_styleframe_discovery_scenelit.py
Style Frame 01 — Scene-Lit Character Prototype (C50)
"Luma & the Glitchkin" — Cycle 50

C50 character-background integration prototype. Demonstrates scene-aware
character lighting by modifying SF01 Discovery to:

  1. Apply scene-colored skin shading (CRT-side cyan tint, lamp-side warm tint)
  2. Scene-responsive body gradient (direction derived from CRT position)
  3. Contact shadow on couch surface
  4. Post-character lighting overlay (character receives scene light)
  5. Bounce light on character lower half from floor/couch

This is a PROTOTYPE — rough output to test whether scene-lit characters
close the character-background integration gap identified in the C50 audit.

Output: output/color/style_frames/LTG_COLOR_styleframe_discovery_scenelit.png
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
from PIL import Image, ImageDraw, ImageFont, ImageFilter

_here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _here)
from LTG_TOOL_procedural_draw import (
    wobble_line, wobble_polygon, variable_stroke,
    add_rim_light, add_face_lighting
)
from LTG_TOOL_cairo_primitives import to_pil_rgba
from LTG_TOOL_char_luma import draw_luma as _canonical_draw_luma, cairo_surface_to_pil as _luma_to_pil
from LTG_TOOL_char_byte import draw_byte as _canonical_draw_byte

OUTPUT_PATH = output_dir('color', 'style_frames', 'LTG_COLOR_styleframe_discovery_scenelit.png')

W, H = 1280, 720
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
# CRT is to the RIGHT of Luma. Lamp is upper-LEFT.
# scene_light_warm = lamp (upper left): SOFT_GOLD family
# scene_light_cool = CRT (right): ELEC_CYAN / BYTE_TEAL family

SCENE_WARM_TINT = (232, 190, 100)   # lamp influence on character
SCENE_COOL_TINT = (  0, 200, 220)   # CRT influence on character
SCENE_WARM_INFLUENCE = 0.15          # how much warm light tints character
SCENE_COOL_INFLUENCE = 0.25          # CRT is the KEY light — stronger influence


def blend_color(base, tint, influence):
    """Blend base color toward tint by influence factor (0.0-1.0)."""
    return tuple(int(base[i] * (1 - influence) + tint[i] * influence) for i in range(3))


def scene_tinted_skin(t_x, light_dir_x=1.0):
    """Return skin color tinted by scene lighting.

    t_x: -1 (left edge of face) to +1 (right edge)
    light_dir_x: +1 = CRT on right (SF01), -1 = CRT on left

    CRT-facing side gets cyan tint, away side gets warm tint.
    """
    # How much this pixel faces the CRT vs the lamp
    crt_facing = max(0, t_x * light_dir_x)     # 0 to 1, strongest on CRT side
    lamp_facing = max(0, -t_x * light_dir_x)    # 0 to 1, strongest on lamp side

    # Base skin with scene light influence
    base = SKIN
    # CRT side: blend toward cyan-tinted highlight
    crt_highlight = blend_color(SKIN_HL, SCENE_COOL_TINT, SCENE_COOL_INFLUENCE)
    # Lamp side: blend toward warm-tinted shadow
    lamp_shadow = blend_color(SKIN_SH, SCENE_WARM_TINT, SCENE_WARM_INFLUENCE)

    r = int(lamp_shadow[0] * lamp_facing + base[0] * (1 - crt_facing - lamp_facing) + crt_highlight[0] * crt_facing)
    g = int(lamp_shadow[1] * lamp_facing + base[1] * (1 - crt_facing - lamp_facing) + crt_highlight[1] * crt_facing)
    b = int(lamp_shadow[2] * lamp_facing + base[2] * (1 - crt_facing - lamp_facing) + crt_highlight[2] * crt_facing)
    return (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))


def scene_tinted_hoodie(t_x, light_dir_x=1.0):
    """Return hoodie color tinted by scene lighting.

    CRT-facing side gets cyan-tinted orange, away side gets warm-shadowed orange.
    """
    crt_facing = max(0, t_x * light_dir_x)
    lamp_facing = max(0, -t_x * light_dir_x)

    # CRT side: hoodie shifts toward cyan-lit variant with stronger influence
    crt_hoodie = blend_color(HOODIE_ORANGE, SCENE_COOL_TINT, 0.30)
    # Lamp side: hoodie in warm shadow
    lamp_hoodie = blend_color(HOODIE_SHADOW, SCENE_WARM_TINT, 0.12)
    # Neutral center
    mid = HOODIE_ORANGE

    r = int(lamp_hoodie[0] * lamp_facing + mid[0] * (1 - crt_facing - lamp_facing) + crt_hoodie[0] * crt_facing)
    g = int(lamp_hoodie[1] * lamp_facing + mid[1] * (1 - crt_facing - lamp_facing) + crt_hoodie[1] * crt_facing)
    b = int(lamp_hoodie[2] * lamp_facing + mid[2] * (1 - crt_facing - lamp_facing) + crt_hoodie[2] * crt_facing)
    return (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))


def draw_contact_shadow(draw, cx, base_y, width, surface_color, alpha_img):
    """Draw a soft contact shadow beneath the character.

    Draws onto alpha_img (RGBA) for compositing — uses darkened surface color.
    """
    shadow_color = tuple(max(0, int(c * 0.45)) for c in surface_color)
    shadow_w = int(width * 1.1)
    shadow_h = sp(10)
    shadow_draw = ImageDraw.Draw(alpha_img)

    # Soft elliptical shadow with gradient alpha
    for i in range(shadow_h):
        t = 1.0 - (i / shadow_h)
        a = int(55 * t * t)  # quadratic falloff
        y = base_y + i
        # Narrower at edges
        row_w = int(shadow_w * (1.0 - 0.3 * (i / shadow_h)))
        shadow_draw.ellipse(
            [cx - row_w, y - 2, cx + row_w, y + 2],
            fill=(*shadow_color, a)
        )


def draw_bounce_light(img, char_cx, char_base_y, char_top_y, char_width,
                      bounce_color, influence=0.12):
    """Apply bounce light from the floor/surface to the lower quarter of the character.

    bounce_color: the color of the surface the character is on.
    """
    bounce_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    bounce_draw = ImageDraw.Draw(bounce_layer)

    # Bounce affects the lower 30% of the character
    bounce_start_y = char_base_y - int((char_base_y - char_top_y) * 0.30)
    bounce_end_y = char_base_y

    for y in range(bounce_start_y, bounce_end_y):
        t = (y - bounce_start_y) / max(1, bounce_end_y - bounce_start_y)
        # Stronger at bottom
        alpha = int(40 * t * t)
        half_w = int(char_width * 0.5 * (0.8 + 0.2 * t))
        bounce_draw.line(
            [(char_cx - half_w, y), (char_cx + half_w, y)],
            fill=(*bounce_color, alpha),
            width=1
        )

    base_rgba = img.convert("RGBA")
    result = Image.alpha_composite(base_rgba, bounce_layer)
    img.paste(result.convert("RGB"))
    return img


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
                    dy = row_y - cy
                    disc = 1.0 - (dy / er_y) ** 2
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
    """Draw the full background — identical to original SF01."""
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

    # CRT unit
    crt_x = mw_x + int(mw_w * 0.24)
    crt_y = mw_y + int(mw_h * 0.08)
    crt_w = int(mw_w * 0.52)
    crt_h = int(mw_h * 0.62)
    draw.rectangle([crt_x, crt_y, crt_x + crt_w, crt_y + crt_h],
                   fill=(38, 30, 50), outline=(55, 44, 72), width=sp(4))

    scr_pad = sp(24)
    scr_x0 = crt_x + scr_pad
    scr_y0 = crt_y + scr_pad
    scr_x1 = crt_x + crt_w - scr_pad
    scr_y1 = crt_y + crt_h - scr_pad * 2
    for y in range(scr_y0, scr_y1):
        t_s = (y - scr_y0) / max(1, scr_y1 - scr_y0)
        r_v = int(0 + (20 - 0) * t_s)
        g_v = int(160 + (40 - 160) * t_s)
        b_v = int(200 + (80 - 200) * t_s)
        draw.line([(scr_x0, y), (scr_x1, y)], fill=(r_v, g_v, b_v))

    for y_s in range(scr_y0, scr_y1, sp(4)):
        draw.line([(scr_x0, y_s), (scr_x1, y_s)], fill=(20, 80, 100), width=1)

    emerge_cx = (scr_x0 + scr_x1) // 2
    emerge_cy = (scr_y0 + scr_y1) // 2 - sp(10)
    emerge_rx = (scr_x1 - scr_x0) // 3
    emerge_ry = (scr_y1 - scr_y0) // 3

    draw_amber_outline(draw, emerge_cx, emerge_cy, emerge_rx, emerge_ry, width=sp(4))

    # Ghost Byte reflection
    ghost = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(ghost)
    gx = sx(int(1920 * 0.24))
    gy = sy(int(1080 * 0.32))
    gs = sp(48)
    gd.ellipse([gx, gy, gx + gs * 2, gy + gs * 2], fill=(0, 212, 232, 90))
    gd.ellipse([gx + gs - sp(12), gy + sp(6), gx + gs + sp(12), gy + sp(26)],
               fill=(240, 240, 240, 80))
    gd.ellipse([gx + gs - sp(6), gy + sp(10), gx + gs + sp(6), gy + sp(22)],
               fill=(10, 10, 20, 120))
    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, ghost)
    img.paste(img_rgba.convert("RGB"))
    draw = ImageDraw.Draw(img)

    # Bookshelf
    shelf_x = sx(20)
    shelf_w = sx(int(1920 * 0.20))
    shelf_tops = [sy(int(1080 * 0.16)), sy(int(1080 * 0.36))]
    for st in shelf_tops:
        draw.rectangle([shelf_x, st, shelf_x + shelf_w, st + sy(int(1080 * 0.16))],
                       fill=(60, 36, 18), outline=(45, 26, 12), width=sp(2))
        b_rng = random.Random(st)
        for bx in range(shelf_x + sp(8), shelf_x + shelf_w - sp(8), sp(14)):
            bh = b_rng.randint(sp(28), sp(48))
            bc = b_rng.choice([(SUNLIT_AMBER), (TERRACOTTA), (SAGE_GREEN),
                               (DUSTY_LAVENDER), (OCHRE_BRICK), (WARM_TAN)])
            draw.rectangle([bx, st + sy(int(1080 * 0.16)) - bh,
                           bx + sp(10), st + sy(int(1080 * 0.16))], fill=bc)

    # Cables
    cable_specs = [
        (mw_x + sx(120), mw_y + mw_h, W - sx(80), H - sy(50), CABLE_BRONZE, sp(3)),
        (mw_x + sx(320), mw_y + mw_h, sx(200), H - sy(20), CABLE_DATA_CYAN, sp(2)),
        (mw_x + sx(480), mw_y + mw_h, W - sx(180), H - sy(80), CABLE_MAG_PURP, sp(2)),
    ]
    for cx0, cy0, cx1, cy1, ccol, cw in cable_specs:
        sag_y = max(cy0, cy1) + sp(40)
        pts = []
        for t_c in [i / 20 for i in range(21)]:
            px_c = int(cx0 + (cx1 - cx0) * t_c)
            py_c = int(cy0 + (cy1 - cy0) * t_c + (sag_y - min(cy0, cy1)) * 4 * t_c * (1 - t_c))
            pts.append((px_c, py_c))
        for j in range(len(pts) - 1):
            draw.line([pts[j], pts[j+1]], fill=ccol, width=cw)

    # Lamp
    lamp_x = sx(int(1920 * 0.38))
    lamp_y = ceiling_y + sy(18)
    draw.line([(lamp_x, ceiling_y), (lamp_x, lamp_y + sy(24))],
              fill=CABLE_BRONZE, width=sp(3))
    draw.polygon([(lamp_x - sp(18), lamp_y + sy(24)),
                  (lamp_x + sp(18), lamp_y + sy(24)),
                  (lamp_x + sp(12), lamp_y + sy(14)),
                  (lamp_x - sp(12), lamp_y + sy(14))],
                 fill=WARM_TAN, outline=LINE, width=sp(2))
    draw.ellipse([lamp_x - sp(6), lamp_y + sy(24),
                  lamp_x + sp(6), lamp_y + sy(32)], fill=LAMP_PEAK)

    # Window
    win_x = sx(int(1920 * 0.01))
    win_y = sy(int(1080 * 0.05))
    win_w = sx(int(1920 * 0.14))
    win_h = sy(int(1080 * 0.25))
    draw.rectangle([win_x, win_y, win_x + win_w, win_y + win_h],
                   fill=(78, 64, 92), outline=LINE, width=sp(3))
    draw.line([(win_x + win_w // 2, win_y), (win_x + win_w // 2, win_y + win_h)],
              fill=LINE, width=sp(2))
    draw.line([(win_x, win_y + win_h // 2), (win_x + win_w, win_y + win_h // 2)],
              fill=LINE, width=sp(2))

    return {
        "mw_x": mw_x, "mw_y": mw_y, "mw_w": mw_w, "mw_h": mw_h,
        "ceiling_y": ceiling_y,
        "scr_x0": scr_x0, "scr_y0": scr_y0, "scr_x1": scr_x1, "scr_y1": scr_y1,
        "emerge_cx": emerge_cx, "emerge_cy": emerge_cy,
        "emerge_rx": emerge_rx, "emerge_ry": emerge_ry,
    }


def draw_couch(draw, luma_cx, luma_base_y):
    """Identical to original SF01 couch."""
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


def render_luma_for_scenelit(img, luma_cx, luma_base_y):
    """Render Luma via canonical char_luma module for scene-lit prototype.

    Returns (updated img, geometry dict with head_cx/cy, hand_cx/cy, torso_top, head_r).
    """
    target_h = sp(430)  # matches original body+head height

    surface = _canonical_draw_luma(
        expression="SURPRISED",
        scale=2.0,
        facing="right",
        scene_lighting={"key_light_color": SCENE_COOL_TINT,
                        "key_light_dir": "right",
                        "ambient": SCENE_WARM_TINT},
    )
    char_img = _luma_to_pil(surface)

    bbox = char_img.getbbox()
    if bbox is None:
        return img, {"head_cx": luma_cx, "head_cy": luma_base_y - target_h // 2,
                     "hand_cx": luma_cx + sp(80), "hand_cy": luma_base_y - sp(200),
                     "torso_top": luma_base_y - sp(260), "torso_half_w": sp(44),
                     "head_r": sp(48)}
    trimmed = char_img.crop(bbox)
    orig_w, orig_h = trimmed.size

    scale_factor = target_h / orig_h
    new_w = max(1, int(orig_w * scale_factor))
    new_h = target_h
    resized = trimmed.resize((new_w, new_h), Image.LANCZOS)

    # Paste onto scene — feet at luma_base_y, centered at luma_cx
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    paste_x = luma_cx - new_w // 2
    paste_y = luma_base_y - new_h
    canvas.paste(resized, (paste_x, paste_y), resized)

    base_rgba = img.convert("RGBA")
    base_rgba = Image.alpha_composite(base_rgba, canvas)
    img = base_rgba.convert("RGB")

    # Estimate geometry for lighting passes
    head_r = int(new_h * 0.11)
    lean_offset = sp(44)
    head_cx = luma_cx + int(new_w * 0.08)
    head_cy = paste_y + int(new_h * 0.18)
    hand_cx = luma_cx + int(new_w * 0.45)
    hand_cy = paste_y + int(new_h * 0.42)
    torso_top = paste_y + int(new_h * 0.28)

    return img, {
        "head_cx": head_cx, "head_cy": head_cy,
        "hand_cx": hand_cx, "hand_cy": hand_cy,
        "torso_top": torso_top,
        "torso_half_w": sp(44),
        "head_r": head_r,
    }


def render_byte_for_scenelit(img, emerge_cx, emerge_cy, emerge_rx, emerge_ry,
                             luma_hand_x, luma_hand_y):
    """Render Byte via canonical char_byte module for scene-lit prototype.

    Returns updated img with Byte composited.
    """
    target_h = int(emerge_ry * 2 + sp(20))

    surface = _canonical_draw_byte(
        expression="searching",
        scale=2.0,
        facing="left",
        scene_lighting={"tint": SCENE_COOL_TINT, "intensity": 0.25, "direction": "left"},
    )
    char_img = to_pil_rgba(surface)

    bbox = char_img.getbbox()
    if bbox is None:
        return img
    trimmed = char_img.crop(bbox)
    orig_w, orig_h = trimmed.size
    scale_factor = target_h / orig_h
    new_w = max(1, int(orig_w * scale_factor))
    new_h = target_h
    resized = trimmed.resize((new_w, new_h), Image.LANCZOS)

    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    paste_x = emerge_cx - new_w // 2
    paste_y = emerge_cy - new_h // 2
    canvas.paste(resized, (paste_x, paste_y), resized)

    base_rgba = img.convert("RGBA")
    base_rgba = Image.alpha_composite(base_rgba, canvas)
    return base_rgba.convert("RGB")


def draw_lighting_overlay_post_character(img, lamp_x, lamp_y, monitor_cx, monitor_cy):
    """
    SCENE-LIT VERSION: Lighting overlay applied AFTER character draw.

    This is the key structural change — the warm/cool overlay now affects
    both the background AND the character, creating lighting continuity.
    Alpha is slightly reduced vs original to avoid washing out character detail.
    """
    # Warm lamp glow (left half)
    warm_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    warm_draw  = ImageDraw.Draw(warm_layer)
    lamp_glow_cx = lamp_x + sx(32)
    lamp_glow_cy = lamp_y + sy(int(1080 * 0.35))
    for step in range(14, 0, -1):
        t = step / 14
        rx  = int(W * 0.30 * t)
        ry  = int(H * 0.55 * t)
        alpha = int(50 * (1 - t))  # reduced from 70 — gentler on character
        warm_draw.ellipse([lamp_glow_cx - rx, lamp_glow_cy - ry,
                           lamp_glow_cx + rx, lamp_glow_cy + ry],
                          fill=(*SOFT_GOLD, alpha))
    warm_np = warm_layer.crop((0, 0, W // 2, H))
    base_left  = img.crop((0, 0, W // 2, H)).convert("RGBA")
    composited_left = Image.alpha_composite(base_left, warm_np)
    img.paste(composited_left.convert("RGB"), (0, 0))

    # Cool CRT glow (right half — extends into character zone)
    cold_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cold_draw  = ImageDraw.Draw(cold_layer)
    for step in range(14, 0, -1):
        t = step / 14
        rx  = int(W * 0.55 * t)
        ry  = int(H * 0.65 * t)
        alpha = int(45 * (1 - t))  # reduced from 60
        cold_draw.ellipse([monitor_cx - rx, monitor_cy - ry,
                           monitor_cx + rx, monitor_cy + ry],
                          fill=(*ELEC_CYAN, alpha))
    split_x = W // 2 - sx(120)  # wider overlap — CRT light reaches Luma
    cold_np    = cold_layer.crop((split_x, 0, W, H))
    base_right = img.crop((split_x, 0, W, H)).convert("RGBA")
    composited_right = Image.alpha_composite(base_right, cold_np)
    img.paste(composited_right.convert("RGB"), (split_x, 0))
    return img


def generate():
    """Generate the scene-lit prototype of SF01."""
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

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

    # STEP 3: Contact shadow on couch (BEFORE character, ON the couch surface)
    contact_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    lean_offset = sp(44)
    draw_contact_shadow(draw=None,
                        cx=luma_cx + lean_offset // 2,
                        base_y=luma_base_y - sp(85),  # where body meets couch
                        width=sp(80),
                        surface_color=COUCH_BODY,
                        alpha_img=contact_layer)
    base_rgba = img.convert("RGBA")
    base_rgba = Image.alpha_composite(base_rgba, contact_layer)
    img.paste(base_rgba.convert("RGB"))
    draw = ImageDraw.Draw(img)

    # STEP 4+5: Luma — SCENE-LIT VERSION (canonical char_luma renderer)
    img, body_data = render_luma_for_scenelit(img, luma_cx, luma_base_y)
    draw = ImageDraw.Draw(img)
    head_cx = body_data["head_cx"]
    head_cy = body_data["head_cy"]
    head_r = body_data["head_r"]

    # STEP 5b: Bounce light from couch/floor onto character lower half
    img = draw_bounce_light(
        img,
        char_cx=luma_cx + lean_offset // 2,
        char_base_y=luma_base_y,
        char_top_y=body_data["torso_top"],
        char_width=sp(88),
        bounce_color=COUCH_BODY,  # warm brown from couch
        influence=0.15
    )
    draw = ImageDraw.Draw(img)

    # STEP 6: Byte (canonical char_byte renderer)
    luma_hand_x = body_data["hand_cx"]
    luma_hand_y = body_data["hand_cy"]
    img = render_byte_for_scenelit(img, emerge_cx, emerge_cy, emerge_rx, emerge_ry,
                                   luma_hand_x, luma_hand_y)
    draw = ImageDraw.Draw(img)

    # STEP 7: Lighting overlay — AFTER character draw (key structural change)
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

    # STEP 7b: Face lighting — with SCENE-COLORED highlight
    # Light comes from upper-right (CRT direction) — highlight is cyan-tinted
    scene_highlight = blend_color(SKIN_HL, SCENE_COOL_TINT, 0.20)
    scene_shadow = blend_color(SKIN_SH, SCENE_WARM_TINT, 0.10)
    add_face_lighting(
        img,
        face_center=(head_cx, head_cy),
        face_radius=(head_r, head_r),
        light_dir=(1.0, -0.5),  # CRT is to the RIGHT and slightly above
        shadow_color=scene_shadow,
        highlight_color=scene_highlight,
        seed=500,
    )
    draw = ImageDraw.Draw(img)

    # STEP 7c: Rim light — CRT cyan from right (same as original but stronger)
    add_rim_light(
        img,
        threshold=175,  # slightly lower threshold to catch more character edge
        light_color=(0, 220, 232),
        width=sp(4),  # slightly wider for more visible rim
        side="right",
        char_cx=head_cx,
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

    # STEP 9: Title strip
    font_xs = load_font(11)
    draw.rectangle([0, H - 30, W, H], fill=(20, 12, 8))
    draw.text((10, H - 22),
              "LUMA & THE GLITCHKIN — Frame 01: The Discovery  |  C50 SCENE-LIT PROTOTYPE",
              fill=(180, 150, 100), font=font_xs)

    # STEP 10: Size rule
    if img.width > 1280 or img.height > 1280:
        img.thumbnail((1280, 1280), Image.LANCZOS)

    img.save(OUTPUT_PATH, "PNG")
    print(f"Saved (scene-lit prototype): {OUTPUT_PATH}  ({img.width}x{img.height})")
    return OUTPUT_PATH


if __name__ == "__main__":
    generate()
