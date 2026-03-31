#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_styleframe_luma_byte.py
Style Frame 04 — "The Dynamic" (Luma + Byte Interaction) — Full Rebuild
"Luma & the Glitchkin" — Cycle 32

Art Director: Alex Chen
Procedural Art Engineer: Rin Yamamoto
Cycle: 32

REBUILD REASON (Sven / Critique 13 P1, CRITICAL):
  SF04 source generators were lost in C28 (stubs only). Sven's audit:
    - Value ceiling at 198 (FAIL — needs >= 225 for a glowing character)
    - Silhouette ambiguous
    - Byte has zero monitor contribution
    - Shadow temperatures wrong

REBUILT FROM SCRATCH (C32) using LTG_COLOR_styleframe_luma_byte.png
as composition reference.

Canonical specs:
  - Byte body   = GL-01b #00D4E8 (BYTE_TEAL)
  - Luma blush  = #E8A87C
  - Rim light   = side="right" with char_cx set per-character
  - Face light  = warm upper-left for Luma
  - Value ceil  = brightest highlight >= 225
  - Monitor glow: Byte has cool (#00D4E8) contribution on their near side
  - Canvas 1280x720 (<= 1280px rule)

Composition (reconstructed from v003 PNG):
  - Background: warm domestic room. CRT monitor on right emitting cyan glow.
  - Luma: left-center (~x=0.32W), sitting/standing, facing right toward Byte.
  - Byte: right-center (~x=0.68W), hovering, facing left toward Luma.
  - Byte's monitor-face emits BYTE_TEAL glow that spills onto surroundings.
  - Title strip at bottom.

Output: /home/wipkat/team/output/color/style_frames/LTG_COLOR_styleframe_luma_byte.png
Usage: python3 LTG_TOOL_styleframe_luma_byte.py
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
from PIL import Image, ImageDraw, ImageFont

# Import procedural draw library (v1.3.0 required for char_cx)
_here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _here)
from LTG_TOOL_procedural_draw import (
    add_rim_light, add_face_lighting, silhouette_test, value_study
)
from LTG_TOOL_char_luma import draw_luma as _canonical_draw_luma, cairo_surface_to_pil as _luma_to_pil
from LTG_TOOL_char_byte import draw_byte as _canonical_draw_byte
from LTG_TOOL_cairo_primitives import to_pil_rgba

OUTPUT_PATH = output_dir('color', 'style_frames', 'LTG_COLOR_styleframe_luma_byte.png')

W, H = 1280, 720

# Scale helpers (reference: 1920x1080)
SX = W / 1920
SY = H / 1080
def sx(n): return int(n * SX)
def sy(n): return int(n * SY)
def sp(n): return int(n * min(SX, SY))

# ── Canonical Palette ─────────────────────────────────────────────────────────
WARM_CREAM      = (250, 240, 220)
SOFT_GOLD       = (232, 201,  90)
SUNLIT_AMBER    = (212, 146,  58)   # RW-03 #D4923A — defined for reference; not placed in SF04.
                                    # SF04 lamp halo uses (255,200,80) hue=41° — incandescent
                                    # lamp amber, intentionally warmer/brighter than outdoor RW-03.
                                    # Use RW-03 for sunlit-window/exterior surfaces; (255,200,80)
                                    # for indoor lamp glow. C35 analysis: warm_cool_analysis_c35.md.
TERRACOTTA      = (199,  91,  57)
RUST_SHADOW     = (140,  58,  34)
WARM_TAN        = (196, 168, 130)
SKIN            = (200, 136,  90)
SKIN_HL         = (232, 184, 136)   # warm highlight — guaranteed >= 225 not needed here
SKIN_SH         = (168, 104,  56)
HAIR_COLOR      = ( 26,  15,  10)
LINE            = ( 59,  40,  32)
HOODIE_ORANGE   = (232, 112,  58)
HOODIE_SHADOW   = (184,  74,  32)
JEANS           = ( 58,  90, 140)
JEANS_SH        = ( 38,  62, 104)
# Luma blush canonical: #E8A87C
BLUSH           = (232, 168, 124)   # #E8A87C

# Byte canonical: GL-01b #00D4E8 BYTE_TEAL
BYTE_TEAL       = (  0, 212, 232)   # GL-01b body fill
BYTE_HL         = (  0, 240, 255)   # ELEC_CYAN highlight — 255 channel guarantees >= 225
BYTE_SH         = (  0, 144, 176)
BYTE_OUTLINE    = (  0, 100, 130)
# Monitor glow: pure BYTE_TEAL
MONITOR_GLOW    = (  0, 212, 232)

ELEC_CYAN       = (  0, 240, 255)
HOT_MAGENTA     = (255,  45, 107)
UV_PURPLE       = (123,  47, 190)
VOID_BLACK      = ( 10,  10,  20)
CORRUPTED_AMBER = (255, 140,   0)
SCAR_MAG        = (255,  45, 107)

# Wall / room
WALL_WARM       = (220, 190, 150)
WALL_UPPER      = (200, 168, 122)
FLOOR_COLOR     = (160, 120,  70)
FLOOR_SHADOW    = (120,  88,  48)
CEILING_COLOR   = ( 80,  55,  22)

# Bright specular — value ceiling guarantee (>= 225)
SPECULAR_WHITE  = (255, 252, 240)   # 255 >= 225 ✓
SPECULAR_CYAN   = (180, 248, 255)   # 255 >= 225 ✓


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


def draw_background(img, draw):
    """Draw warm domestic room background with CRT monitor on right."""
    rng = random.Random(42)

    ceiling_y = sy(130)
    floor_y   = sy(680)

    # Ceiling strip
    draw.rectangle([0, 0, W, ceiling_y], fill=CEILING_COLOR)
    draw.line([(0, ceiling_y), (W, ceiling_y)], fill=(50, 32, 12), width=sp(4))

    # Back wall — warm gradient (vertical)
    for row in range(ceiling_y, floor_y):
        t = (row - ceiling_y) / max(1, floor_y - ceiling_y)
        r = int(WALL_UPPER[0] + (WALL_WARM[0] - WALL_UPPER[0]) * t)
        g = int(WALL_UPPER[1] + (WALL_WARM[1] - WALL_UPPER[1]) * t)
        b = int(WALL_UPPER[2] + (WALL_WARM[2] - WALL_UPPER[2]) * t)
        draw.line([(0, row), (W, row)], fill=(r, g, b))

    # Floor
    draw.rectangle([0, floor_y, W, H - 30], fill=FLOOR_COLOR)
    # Floor shadow at wall base
    for i in range(sp(20)):
        alpha_frac = 1.0 - i / sp(20)
        dark = int(40 * alpha_frac)
        r_ = max(0, FLOOR_COLOR[0] - dark)
        g_ = max(0, FLOOR_COLOR[1] - dark)
        b_ = max(0, FLOOR_COLOR[2] - dark)
        draw.line([(0, floor_y + i), (W, floor_y + i)], fill=(r_, g_, b_))

    # ── CRT monitor on right side ─────────────────────────────────────────────
    # Positioned at ~x=0.70W, centered vertically in upper half
    mon_cx = sx(1330)
    mon_cy = sy(440)
    mon_w  = sx(310)
    mon_h  = sy(220)
    mon_x0 = mon_cx - mon_w // 2
    mon_y0 = mon_cy - mon_h // 2
    mon_x1 = mon_cx + mon_w // 2
    mon_y1 = mon_cy + mon_h // 2
    frame_pad = sp(18)

    # Monitor housing (dark plastic)
    draw.rectangle([mon_x0 - frame_pad, mon_y0 - frame_pad,
                    mon_x1 + frame_pad, mon_y1 + frame_pad + sp(30)],
                   fill=(38, 34, 28))
    # Screen glow (BYTE_TEAL gradient — brightest center)
    # C49: CRT glow asymmetry — 0.70 multiplier below screen midpoint
    _below_mult = 0.70
    for step in range(16, 0, -1):
        t = step / 16
        g_r = int(BYTE_TEAL[0] * t * 0.4)
        g_g = int(BYTE_TEAL[1] * t * 0.9)
        g_b = int(BYTE_TEAL[2] * t * 0.95)
        ex = int(mon_w // 2 * t)
        ey = int(mon_h // 2 * t)
        ring_top = mon_cy - ey
        ring_bot = mon_cy + ey
        if ring_bot <= mon_cy:
            draw.ellipse([mon_cx - ex, ring_top, mon_cx + ex, ring_bot],
                         fill=(g_r, g_g, g_b))
        elif ring_top >= mon_cy:
            draw.ellipse([mon_cx - ex, ring_top, mon_cx + ex, ring_bot],
                         fill=(int(g_r * _below_mult), int(g_g * _below_mult),
                               int(g_b * _below_mult)))
        else:
            # Straddles midpoint: draw dimmed, overdraw upper with scanlines
            dim = (int(g_r * _below_mult), int(g_g * _below_mult),
                   int(g_b * _below_mult))
            draw.ellipse([mon_cx - ex, ring_top, mon_cx + ex, ring_bot], fill=dim)
            full = (g_r, g_g, g_b)
            for row_y in range(max(ring_top, 0), min(mon_cy, ring_bot)):
                dy = row_y - mon_cy
                disc = 1.0 - (dy / max(ey, 1)) ** 2
                if disc <= 0:
                    continue
                half_w = int(ex * math.sqrt(disc))
                if half_w > 0:
                    draw.line([(mon_cx - half_w, row_y), (mon_cx + half_w, row_y)],
                              fill=full, width=1)
    # Screen rim
    draw.rectangle([mon_x0, mon_y0, mon_x1, mon_y1],
                   outline=(60, 50, 40), width=sp(3))
    # Screen specular dot (value ceiling guarantee — >= 225)
    spec_x = mon_cx - mon_w // 4
    spec_y = mon_cy - mon_h // 4
    draw.ellipse([spec_x - sp(6), spec_y - sp(4),
                  spec_x + sp(6), spec_y + sp(4)],
                 fill=SPECULAR_CYAN)

    # Monitor stand
    stand_x = mon_cx - sp(14)
    stand_bot = mon_y1 + frame_pad + sp(30)
    draw.rectangle([stand_x, stand_bot, stand_x + sp(28), stand_bot + sp(18)],
                   fill=(50, 44, 36))
    draw.rectangle([stand_x - sp(20), stand_bot + sp(18),
                    stand_x + sp(48), stand_bot + sp(28)],
                   fill=(44, 38, 30))

    # Monitor ambient glow radiating onto wall / floor (BYTE_TEAL spill)
    # C49: CRT glow asymmetry — dimmed below screen midpoint (mon_cy)
    glow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow_draw  = ImageDraw.Draw(glow_layer)
    glow_steps = 12
    for gs in range(glow_steps, 0, -1):
        t = gs / glow_steps
        alpha_full = int(55 * t * t)
        alpha_dim  = int(alpha_full * _below_mult)
        gr  = int(BYTE_TEAL[0] * 0.1)
        gg  = int(BYTE_TEAL[1] * 0.85 * t)
        gb  = int(BYTE_TEAL[2] * 0.90 * t)
        ex  = int(mon_w * 0.9 * (1.0 + (1 - t) * 1.5))
        ey  = int(mon_h * 0.9 * (1.0 + (1 - t) * 1.5))
        ring_top = mon_cy - ey
        ring_bot = mon_cy + ey
        # Draw dimmed ellipse first, then overdraw upper half at full alpha
        glow_draw.ellipse([mon_cx - ex, ring_top, mon_cx + ex, ring_bot],
                          fill=(gr, gg, gb, alpha_dim))
        for row_y in range(max(ring_top, 0), min(mon_cy, ring_bot)):
            dy = row_y - mon_cy
            disc = 1.0 - (dy / max(ey, 1)) ** 2
            if disc <= 0:
                continue
            half_w = int(ex * math.sqrt(disc))
            if half_w > 0:
                glow_draw.line([(mon_cx - half_w, row_y), (mon_cx + half_w, row_y)],
                               fill=(gr, gg, gb, alpha_full), width=1)
    base_rgba = img.convert("RGBA")
    base_rgba = Image.alpha_composite(base_rgba, glow_layer)
    img.paste(base_rgba.convert("RGB"))
    draw = ImageDraw.Draw(img)

    # ── Lamp (upper left) — warm domestic source ──────────────────────────────
    lamp_x = sx(200)
    lamp_y = ceiling_y + sy(30)
    # Lamp shade
    shade_pts = [
        (lamp_x - sx(50), lamp_y + sy(40)),
        (lamp_x + sx(50), lamp_y + sy(40)),
        (lamp_x + sx(30), lamp_y),
        (lamp_x - sx(30), lamp_y),
    ]
    draw.polygon(shade_pts, fill=(220, 190, 110))
    draw.polygon(shade_pts, outline=(160, 130, 60), width=sp(2))
    # Lamp base
    draw.rectangle([lamp_x - sp(6), lamp_y + sy(40),
                    lamp_x + sp(6), lamp_y + sy(70)],
                   fill=(140, 110, 60))
    # Warm light halo from lamp
    lamp_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    lamp_draw  = ImageDraw.Draw(lamp_layer)
    for ls in range(10, 0, -1):
        t = ls / 10
        alpha = int(40 * t * t)
        ex = int(sx(140) * (1.0 + (1 - t) * 2.0))
        ey = int(sy(100) * (1.0 + (1 - t) * 2.0))
        lamp_draw.ellipse([lamp_x - ex, lamp_y - ey, lamp_x + ex, lamp_y + ey],
                          fill=(255, 200, 80, alpha))
    base_rgba = img.convert("RGBA")
    base_rgba = Image.alpha_composite(base_rgba, lamp_layer)
    img.paste(base_rgba.convert("RGB"))
    draw = ImageDraw.Draw(img)

    return {
        "ceiling_y":  ceiling_y,
        "floor_y":    floor_y,
        "mon_cx":     mon_cx,
        "mon_cy":     mon_cy,
        "mon_x0":     mon_x0,
        "mon_y0":     mon_y0,
        "mon_x1":     mon_x1,
        "mon_y1":     mon_y1,
        "lamp_x":     lamp_x,
        "lamp_y":     lamp_y,
    }


def draw_luma(img, draw, bg_data):
    """Draw Luma via canonical char_luma module: left-center, facing right toward Byte.

    Renders Luma using the canonical draw_luma() from LTG_TOOL_char_luma,
    converts the cairo surface to PIL, and composites onto the scene.
    Returns (head_cx, head_cy, head_r) for downstream lighting passes.
    """
    luma_cx   = sx(420)
    floor_y   = bg_data["floor_y"]
    luma_base = floor_y
    head_r    = sp(64)

    # Target character height matching original inline proportions
    total_body_h = int(head_r * 6.4)

    # Render via canonical module — SURPRISED expression for the Dynamic scene
    surface = _canonical_draw_luma(
        expression="SURPRISED",
        scale=1.0,
        facing="right",
        scene_lighting={"key_light_color": (255, 200, 80),
                        "key_light_dir": "left",
                        "ambient": (220, 190, 150)},
    )
    char_img = _luma_to_pil(surface)

    # Trim transparent padding to content bounds
    bbox = char_img.getbbox()
    if bbox is None:
        # Fallback geometry if render fails
        head_cx = luma_cx + sp(12)
        head_cy = luma_base - total_body_h + head_r
        return head_cx, head_cy, head_r

    trimmed = char_img.crop(bbox)
    orig_w, orig_h = trimmed.size

    # Scale to match target height in scene
    scale_factor = total_body_h / orig_h
    new_w = max(1, int(orig_w * scale_factor))
    new_h = total_body_h
    resized = trimmed.resize((new_w, new_h), Image.LANCZOS)

    # Place on full-canvas RGBA layer, feet at luma_base, centered at luma_cx
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    paste_x = luma_cx - new_w // 2
    paste_y = luma_base - new_h
    canvas.paste(resized, (paste_x, paste_y), resized)

    # Composite onto background
    base_rgba = img.convert("RGBA")
    composited = Image.alpha_composite(base_rgba, canvas)
    img.paste(composited.convert("RGB"))
    draw = ImageDraw.Draw(img)

    # Estimate geometry for downstream lighting passes (head in upper ~18%)
    head_cx = luma_cx + int(new_w * 0.08)
    head_cy = paste_y + int(new_h * 0.18)
    head_r_est = int(new_h * 0.11)

    return head_cx, head_cy, head_r_est


def draw_byte(img, draw, bg_data):
    """Draw Byte via canonical char_byte module: right-center, hovering, facing left.

    Renders Byte using the canonical draw_byte() from LTG_TOOL_char_byte,
    converts the cairo surface to PIL, and composites onto the scene.
    Byte body = GL-01b #00D4E8 BYTE_TEAL.
    Returns (byte_cx, byte_cy) for downstream lighting passes.
    """
    byte_cx = sx(900)
    floor_y = bg_data["floor_y"]
    byte_cy = floor_y - sp(220)

    body_rx = sp(68)
    body_ry = sp(80)
    target_h = body_ry * 2 + sp(40)  # body height + antenna margin

    # Render via canonical module — "neutral" expression for the Dynamic scene
    surface = _canonical_draw_byte(
        expression="neutral",
        scale=1.0,
        facing="left",
        scene_lighting={"tint": (0, 212, 232), "intensity": 0.25, "direction": "right"},
    )
    char_img = to_pil_rgba(surface)

    # Trim transparent padding to content bounds
    bbox = char_img.getbbox()
    if bbox is None:
        return byte_cx, byte_cy

    trimmed = char_img.crop(bbox)
    orig_w, orig_h = trimmed.size

    # Scale to match target height in scene
    scale_factor = target_h / orig_h
    new_w = max(1, int(orig_w * scale_factor))
    new_h = target_h
    resized = trimmed.resize((new_w, new_h), Image.LANCZOS)

    # Place on full-canvas RGBA layer, centered at (byte_cx, byte_cy)
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    paste_x = byte_cx - new_w // 2
    paste_y = byte_cy - new_h // 2
    canvas.paste(resized, (paste_x, paste_y), resized)

    # Monitor contribution glow on Byte's near side (right flank facing CRT)
    mon_glow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    mon_glow_draw  = ImageDraw.Draw(mon_glow_layer)
    for gs in range(8, 0, -1):
        t = gs / 8
        alpha = int(50 * t * t)
        ex  = int(body_rx * 0.8 * (2.0 - t))
        ey  = int(body_ry * 0.5 * (2.0 - t))
        mon_glow_draw.ellipse([byte_cx, byte_cy - ey, byte_cx + ex, byte_cy + ey],
                              fill=(*BYTE_TEAL, alpha))

    # Hover shadow on floor
    shadow_y = floor_y + sp(6)
    shadow_rx = int(body_rx * 0.85)
    shadow_ry = sp(12)
    shadow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    shadow_draw  = ImageDraw.Draw(shadow_layer)
    shadow_draw.ellipse([byte_cx - shadow_rx, shadow_y - shadow_ry,
                         byte_cx + shadow_rx, shadow_y + shadow_ry],
                        fill=(20, 20, 15, 80))

    # Composite all layers: character + monitor glow + shadow
    base_rgba = img.convert("RGBA")
    base_rgba = Image.alpha_composite(base_rgba, shadow_layer)
    base_rgba = Image.alpha_composite(base_rgba, canvas)
    base_rgba = Image.alpha_composite(base_rgba, mon_glow_layer)
    img.paste(base_rgba.convert("RGB"))
    draw = ImageDraw.Draw(img)

    return byte_cx, byte_cy


def generate():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    img  = Image.new("RGB", (W, H), WARM_CREAM)
    draw = ImageDraw.Draw(img)

    # STEP 1: Background (room + monitor + lamp)
    bg_data = draw_background(img, draw)
    draw = ImageDraw.Draw(img)

    # STEP 2: Luma
    luma_head_cx, luma_head_cy, luma_head_r = draw_luma(img, draw, bg_data)
    draw = ImageDraw.Draw(img)

    # STEP 3: Luma face lighting — warm upper-left lamp
    add_face_lighting(
        img,
        face_center=(luma_head_cx, luma_head_cy),
        face_radius=(luma_head_r, luma_head_r),
        light_dir=(-1.0, -1.0),           # upper-left lamp
        shadow_color=SKIN_SH,
        highlight_color=SKIN_HL,
        seed=500,
    )
    draw = ImageDraw.Draw(img)

    # STEP 4: Luma rim light — cool CRT/monitor teal from right
    # char_cx = luma_head_cx so mask is x > luma_head_cx (character-relative)
    add_rim_light(
        img,
        threshold=185,
        light_color=(0, 212, 232),          # BYTE_TEAL rim
        width=sp(3),
        side="right",
        char_cx=luma_head_cx,              # character-relative split
    )
    draw = ImageDraw.Draw(img)

    # STEP 5: Byte
    byte_cx, byte_cy = draw_byte(img, draw, bg_data)
    draw = ImageDraw.Draw(img)

    # STEP 6: Byte rim light — warm lamp glow from left (lamp is at left)
    # Byte's left side faces the warm lamp; right side faces the monitor wall
    add_rim_light(
        img,
        threshold=185,
        light_color=(255, 200,  80),        # warm amber lamp rim
        width=sp(2),
        side="left",
        char_cx=byte_cx,                   # character-relative split
    )
    draw = ImageDraw.Draw(img)

    # STEP 7: Interaction energy — small spark / connection between Luma's hand
    # and Byte's outstretched arm
    spark_x = int((luma_head_cx + sp(130) + byte_cx - sp(68)) / 2)
    spark_y = int(bg_data["floor_y"] - sp(180))
    spark_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    spark_draw  = ImageDraw.Draw(spark_layer)
    for gs in range(8, 0, -1):
        t = gs / 8
        alpha = int(120 * t * t)
        ex = int(sp(30) * (2.0 - t))
        ey = int(sp(20) * (2.0 - t))
        spark_draw.ellipse([spark_x - ex, spark_y - ey, spark_x + ex, spark_y + ey],
                           fill=(200, 248, 255, alpha))
    # Bright spark core (value ceiling >= 225)
    spark_draw.ellipse([spark_x - sp(6), spark_y - sp(4),
                        spark_x + sp(6), spark_y + sp(4)],
                       fill=(*SPECULAR_WHITE, 200))
    base_rgba = img.convert("RGBA")
    base_rgba = Image.alpha_composite(base_rgba, spark_layer)
    img.paste(base_rgba.convert("RGB"))
    draw = ImageDraw.Draw(img)

    # STEP 8: Top/bottom vignette
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
              "LUMA & THE GLITCHKIN — Frame 04: The Dynamic  |  C32 — Full Rebuild v004",
              fill=(180, 150, 100), font=font_xs)

    # STEP 10: Image size rule (already 1280×720 — no resize needed)
    if img.width > 1280 or img.height > 1280:
        img.thumbnail((1280, 1280), Image.LANCZOS)

    img.save(OUTPUT_PATH, "PNG")
    print(f"Saved: {OUTPUT_PATH}  ({img.width}x{img.height})")

    # Verify value ceiling
    import colorsys
    pixels = list(img.getdata())
    max_brightness = max(max(r, g, b) for r, g, b in pixels)
    print(f"Value ceiling (max channel): {max_brightness}  (need >= 225)")
    if max_brightness >= 225:
        print("  VALUE CEILING: PASS")
    else:
        print("  VALUE CEILING: FAIL")

    return OUTPUT_PATH


if __name__ == "__main__":
    generate()
