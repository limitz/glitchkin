#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_sf_miri_luma_handoff.py
Style Frame — "The Hand-Off" (SF_MIRI_LUMA_HANDOFF / SF06 candidate)
"Luma & the Glitchkin" — Cycle 49 / Maya Santos

Cycle 53 changes (C53 — CANONICAL CHARACTER RENDERER MIGRATION):
  - Replaced inline draw_miri_character() and draw_luma_character() (530+ lines
    of PIL drawing) with canonical char_miri.draw_miri() and char_luma.draw_luma()
    imports. Characters rendered via pycairo, converted to PIL RGBA for compositing.
  - Scene composition (placement, foot shadows, Wand pipeline) preserved.
  - Per modular rendering architecture: one canonical renderer per entity.

Cycle 52 changes (Hana Okonkwo, C52 — CHARACTER-ENVIRONMENT INTEGRATION):
  - WAND COMPOSITING PIPELINE: Characters now drawn on separate transparent
    layers and composited using LTG_TOOL_wand_composite.py.
  - Compositing pass order (per C50 spec):
    BG > CRT glow > lamp glow > contact shadows (Wand Gaussian) > characters
    > scene lighting (Wand Screen blend) > bounce light (Wand Screen)
    > edge tint (Wand morphology) > color transfer (Wand Soft Light)
    > dual temp overlay > deep shadows > caption
  - PER-ENVIRONMENT LIGHTING: Living Room settings from
    character_environment_lighting_c50.md applied.
    Warm lamp left (Miri zone), CRT cool spill center-right (Luma zone).
    Surface color (185,165,125), shadow alpha 50, bounce alpha 20.
  - GRACEFUL FALLBACK: If Wand/libmagickwand missing, falls back to legacy
    PIL compositing (pre-C52 direct-draw path).

Cycle 49 changes (Maya Santos, C49):
  - MIRI ELDER POSTURE: Forward lean (3-5 degrees) via head/torso offset.
    Head shifts +3px rightward (toward CRT), torso 60% of that, feet stay.
    Rounded shoulders: shoulder rest drops 3px, inward 2px.
    Stacks with existing C48 shoulder involvement.
  - Per Alex Chen C49 brief (Miri posture update P1).

Cycle 48 changes (Maya Santos, C48):
  - SHOULDER INVOLVEMENT: Both Miri and Luma torsos now use polyline shoulder
    points with deltoid bumps that respond to arm position.
    Miri: right shoulder shifts outward +5px (forward pull for hand-off gesture).
    Luma: left shoulder slight rise -3px (curious lean), right shoulder outward
    +5px (forward/outward arm).
    Per image-rules.md Shoulder Involvement Rule (codified C47).
    Per-character clothing reads: Miri = cardigan crease, Luma = hoodie bunch.

Cycle 44 / Maya Santos (original)

Concept: "The Hand-Off"
Miri and Luma together in the living room, at the CRT. Miri's hand is on
the TV. Luma's posture is attentive curiosity — she's being shown something,
not just standing near it. The CRT is between them in composition. Warm,
intergenerational, specific. This is the origin point of the show.

Setting: Grandma Miri's living room (the cold-open setting — CRT is here).
Palette: Real World only. No Glitch Layer colors.
Canvas: 1280×720px

Character relative scale (from lineup):
  Miri:  3.2 heads tall. HEAD_UNIT = 52px in style frame scale.
  Luma:  3.5 heads tall. HEAD_UNIT = 52px in style frame scale.
  (Lineup uses 87.5px HU. Style frame uses ~60% — characters read at
   ~2/3 lineup scale against background depth.)

Composition:
  - CRT center-left (x ~490–680)
  - Miri stands LEFT of CRT, facing slight 3/4 right. Hand toward TV.
  - Luma stands RIGHT of CRT, facing slight 3/4 left. Attentive lean.
  - Both characters at same ground line (foreground, not on BG wall plane)
  - Warm/cool split: Miri in warm zone (left lamp), Luma in cool zone (CRT glow)

Face test gate: Luma face drawn via draw_luma_face_handoff() at sprint scale.
  Miri face drawn via draw_miri_face_handoff(). No automated gate for Miri.

Output: output/color/style_frames/LTG_COLOR_sf_miri_luma_handoff.png
"""

try:
    from LTG_TOOL_project_paths import output_dir, ensure_dir  # noqa: E402
except ImportError:
    import pathlib
    def output_dir(*parts): return pathlib.Path("/home/wipkat/team/output").joinpath(*parts)
    def ensure_dir(path): path.mkdir(parents=True, exist_ok=True); return path
import math
import os
import sys
import random
from PIL import Image, ImageDraw, ImageFilter

# Canonical character renderer imports
_here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _here)
from LTG_TOOL_char_miri import draw_miri as _canonical_draw_miri
from LTG_TOOL_char_luma import draw_luma as _canonical_draw_luma
from LTG_TOOL_cairo_primitives import to_pil_rgba as _to_pil_rgba

random.seed(44)

W, H = 1280, 720

# ── Real World Palette ─────────────────────────────────────────────────────────
# Room palette (from living room env tool)
WARM_CREAM       = (250, 240, 220)
AGED_CREAM       = (238, 226, 198)
WALL_BASE        = (236, 220, 192)
WALL_SHADOW      = (188, 168, 136)
CEILING_WARM     = (244, 234, 210)
FLOOR_OAK_LIGHT  = (198, 162, 110)
FLOOR_OAK_MED   = (172, 138,  86)
FLOOR_OAK_DARK  = (140, 108,  64)
FLOOR_RUG_RED   = (158,  68,  42)
FLOOR_RUG_EDGE  = (128,  48,  28)
LINE_DARK        = ( 59,  40,  32)
NEAR_BLACK_WARM  = ( 28,  18,  10)
SHADOW_DEEP      = ( 44,  28,  16)
SUNLIT_AMBER     = (255, 200, 100)
CRT_PLASTIC      = (108,  90,  68)
CRT_PLASTIC_DARK = ( 72,  58,  40)
CRT_SCREEN_GLOW  = ( 30,  90, 108)
CRT_SCREEN_DARK  = ( 12,  52,  68)
CRT_STAND_WOOD   = ( 90,  64,  32)
CRT_COOL_SPILL   = (  0, 128, 148)
LAMP_WARM        = (255, 200, 120)
WOOD_LIGHT       = (210, 178, 130)
WOOD_MED         = (160, 128,  80)

# Miri palette
MIRI_SKIN        = (140,  84,  48)
MIRI_SKIN_SH     = (106,  58,  30)
MIRI_HAIR        = (216, 208, 200)
MIRI_HAIR_SH     = (168, 152, 136)
MIRI_CARDIGAN    = (184,  92,  56)
MIRI_CARD_SH     = (138,  60,  28)
MIRI_PANTS       = (200, 174, 138)
MIRI_SLIPPER     = ( 90, 122,  90)
MIRI_EYE_IRIS    = (139,  94,  60)
MIRI_HAIRPIN     = ( 92,  58,  32)
MIRI_BLUSH       = (212, 149, 107)

# Luma palette
LUMA_SKIN        = (200, 136,  90)
LUMA_SKIN_SH     = (164, 100,  60)
LUMA_HAIR        = ( 44,  28,  18)
LUMA_HOODIE      = (232, 114,  42)
LUMA_HOODIE_SH   = (180,  76,  20)
LUMA_JEANS       = ( 72,  96, 138)
LUMA_JEANS_SH    = ( 52,  72, 110)
LUMA_SHOES       = ( 52,  36,  24)
LUMA_EYE_IRIS    = (200, 125,  62)

SPEC_WHITE       = (248, 248, 240)


# ── Utility ────────────────────────────────────────────────────────────────────

def lerp_color(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def alpha_overlay_rect(img, x1, y1, x2, y2, color, alpha):
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.rectangle([x1, y1, x2, y2], fill=(*color, alpha))
    out = Image.alpha_composite(img.convert("RGBA"), layer)
    return out.convert("RGB")


def arc_pts(cx, cy, rx, ry, a0, a1, steps=40):
    pts = []
    for i in range(steps + 1):
        t = a0 + (a1 - a0) * i / steps
        r = math.radians(t)
        pts.append((int(cx + rx * math.cos(r)), int(cy + ry * math.sin(r))))
    return pts


def polyline(draw, pts, color, width=2):
    for i in range(len(pts) - 1):
        draw.line([pts[i], pts[i+1]], fill=color, width=width)


# ── Background: Living Room Simplified ────────────────────────────────────────

def draw_background(img):
    """
    Simplified living room for style frame — key elements only.
    Perspective: mild 3/4, vp slightly right of center, elevated.
    Back wall center, floor in foreground, warm/cool split.
    """
    draw = ImageDraw.Draw(img)

    # Vanishing point
    vp_x = int(W * 0.52)
    vp_y = int(H * 0.38)

    # Back wall bounding box
    bw_left  = int(W * 0.04)
    bw_top   = int(H * 0.08)
    bw_right = int(W * 0.96)
    bw_bot   = int(H * 0.62)

    # Ceiling
    draw.rectangle([0, 0, W, bw_top], fill=CEILING_WARM)

    # Back wall fill
    draw.rectangle([bw_left, bw_top, bw_right, bw_bot], fill=WALL_BASE)

    # Left side wall (receding, warm shadow)
    draw.polygon([0, bw_top, bw_left, bw_top, bw_left, bw_bot, 0, H],
                 fill=WALL_SHADOW)

    # Right side wall
    draw.polygon([bw_right, bw_top, W, bw_top, W, H, bw_right, bw_bot],
                 fill=lerp_color(WALL_BASE, WALL_SHADOW, 0.4))

    # Baseboard on back wall
    draw.rectangle([bw_left, bw_bot - 8, bw_right, bw_bot], fill=AGED_CREAM)
    draw.line([(bw_left, bw_bot - 8), (bw_right, bw_bot - 8)], fill=LINE_DARK, width=1)

    # Floor
    for y in range(bw_bot, H + 4, 8):
        t = (y - bw_bot) / max(1, H - bw_bot)
        col = lerp_color(FLOOR_OAK_MED, FLOOR_OAK_DARK, t * 0.5)
        draw.line([(0, y), (W, y)], fill=col)

    # Floor planks (perspective lines from vp)
    for px in range(0, W + 80, 80):
        draw.line([(vp_x, bw_bot), (px, H)], fill=FLOOR_OAK_DARK, width=1)

    # Area rug (warm red, foreground center)
    rug_pts = [
        (int(W * 0.10), H),
        (int(W * 0.90), H),
        (int(W * 0.80), int(H * 0.76)),
        (int(W * 0.20), int(H * 0.76)),
    ]
    draw.polygon(rug_pts, fill=FLOOR_RUG_RED)
    draw.polygon(rug_pts, outline=FLOOR_RUG_EDGE, width=3)

    # Rug inner border (decorative)
    inner = [
        (int(W * 0.15), H - 6),
        (int(W * 0.85), H - 6),
        (int(W * 0.77), int(H * 0.78)),
        (int(W * 0.23), int(H * 0.78)),
    ]
    draw.polygon(inner, outline=lerp_color(FLOOR_RUG_RED, AGED_CREAM, 0.35), width=2)

    # Warm wallpaper texture hint
    for y in range(bw_top + 4, bw_bot - 8, 18):
        if (y // 18) % 3 == 0:
            draw.line([(bw_left, y), (bw_right, y)],
                      fill=(*AGED_CREAM, ), width=1)

    # Family photos suggestion — upper back wall, L and R of CRT
    for px, pw in [(int(W * 0.18), 42), (int(W * 0.30), 30), (int(W * 0.76), 36)]:
        py = int(H * 0.14)
        ph = int(pw * 0.75)
        draw.rectangle([px, py, px + pw, py + ph], fill=AGED_CREAM, outline=LINE_DARK, width=1)
        draw.rectangle([px + 3, py + 3, px + pw - 3, py + ph - 3],
                       fill=lerp_color(WALL_SHADOW, AGED_CREAM, 0.5))

    draw = ImageDraw.Draw(img)
    return draw, vp_x, vp_y, bw_left, bw_top, bw_right, bw_bot


# ── CRT Television ─────────────────────────────────────────────────────────────

def draw_crt_tv(img):
    """
    CRT — center composition. Screen ON. Warm plastic body.
    Smaller than living room env (style frame characters in FG).
    CRT sits on stand center-left of room.
    Returns screen bounds and TV body bounds.
    """
    draw = ImageDraw.Draw(img)

    # Stand
    stand_x1 = int(W * 0.36)
    stand_x2 = int(W * 0.64)
    stand_y1 = int(H * 0.57)
    stand_y2 = int(H * 0.63)

    draw.rectangle([stand_x1, stand_y1, stand_x2, stand_y2], fill=CRT_STAND_WOOD)
    draw.line([(stand_x1, stand_y1), (stand_x2, stand_y1)], fill=WOOD_LIGHT, width=2)
    draw.rectangle([stand_x1, stand_y1, stand_x2, stand_y2], outline=LINE_DARK, width=1)

    # TV body
    tv_x1 = stand_x1 + 10
    tv_x2 = stand_x2 - 10
    tv_y1 = int(H * 0.30)
    tv_y2 = stand_y1 + 8

    tv_w = tv_x2 - tv_x1
    tv_h = tv_y2 - tv_y1

    draw.rectangle([tv_x1, tv_y1, tv_x2, tv_y2], fill=CRT_PLASTIC)
    draw.rectangle([tv_x1, tv_y1, tv_x2, tv_y2], outline=LINE_DARK, width=2)

    # Plastic top highlight
    draw.line([(tv_x1 + 4, tv_y1 + 2), (tv_x2 - 4, tv_y1 + 2)],
              fill=lerp_color(CRT_PLASTIC, WARM_CREAM, 0.35), width=1)

    # Shadow bottom half
    draw.rectangle([tv_x1, tv_y1 + tv_h // 2, tv_x2, tv_y2], fill=CRT_PLASTIC_DARK)

    # Screen bezel
    bm_x = max(6, tv_w // 10)
    bm_y = max(5, tv_h // 10)
    bezel_x1 = tv_x1 + bm_x
    bezel_x2 = tv_x2 - bm_x
    bezel_y1 = tv_y1 + bm_y
    bezel_y2 = tv_y2 - int(tv_h * 0.28)

    draw.rectangle([bezel_x1, bezel_y1, bezel_x2, bezel_y2], fill=NEAR_BLACK_WARM)
    draw.rectangle([bezel_x1, bezel_y1, bezel_x2, bezel_y2], outline=LINE_DARK, width=1)

    # Screen
    scr_x1 = bezel_x1 + 4
    scr_x2 = bezel_x2 - 4
    scr_y1 = bezel_y1 + 3
    scr_y2 = bezel_y2 - 3
    scr_w = scr_x2 - scr_x1
    scr_h = scr_y2 - scr_y1

    # Screen gradient
    for y in range(scr_y1, scr_y2):
        t = (y - scr_y1) / max(1, scr_h)
        col = lerp_color((55, 130, 155), (18, 62, 80), t * 0.6)
        draw.line([(scr_x1, y), (scr_x2, y)], fill=col)

    # Scanlines
    for y in range(scr_y1, scr_y2, 3):
        draw.line([(scr_x1 + 1, y), (scr_x2 - 1, y)], fill=(8, 38, 52), width=1)

    # Screen glare
    gl_x1 = scr_x1 + int(scr_w * 0.06)
    gl_x2 = scr_x1 + int(scr_w * 0.22)
    gl_y1 = scr_y1 + int(scr_h * 0.06)
    gl_y2 = scr_y1 + int(scr_h * 0.18)
    draw.rectangle([gl_x1, gl_y1, gl_x2, gl_y2],
                   fill=lerp_color(CRT_SCREEN_GLOW, (200, 230, 238), 0.65))

    # Speaker grille
    gr_y1 = bezel_y2 + 3
    gr_y2 = tv_y2 - 8
    gr_x1 = tv_x1 + int(tv_w * 0.07)
    gr_x2 = tv_x1 + int(tv_w * 0.44)
    draw.rectangle([gr_x1, gr_y1, gr_x2, gr_y2], fill=CRT_PLASTIC_DARK)
    for gi in range(5):
        gx = gr_x1 + 3 + gi * 5
        if gx < gr_x2 - 3:
            draw.line([(gx, gr_y1 + 2), (gx, gr_y2 - 2)],
                      fill=lerp_color(CRT_PLASTIC_DARK, CRT_PLASTIC, 0.45), width=1)

    # Knobs
    kx_base = tv_x2 - int(tv_w * 0.20)
    ky_base = bezel_y2 + int((tv_y2 - bezel_y2) * 0.5)
    for ki in range(2):
        kx = kx_base + ki * 14
        draw.ellipse([kx - 5, ky_base - 5, kx + 5, ky_base + 5], fill=LINE_DARK)
        draw.ellipse([kx - 3, ky_base - 3, kx + 3, ky_base + 3], fill=WOOD_MED)

    # Antenna (rabbit ears)
    ant_cx = (tv_x1 + tv_x2) // 2
    ant_y  = tv_y1 - 2
    draw.line([(ant_cx - 4, ant_y), (ant_cx - 22, ant_y - 38)], fill=LINE_DARK, width=2)
    draw.line([(ant_cx + 4, ant_y), (ant_cx + 20, ant_y - 34)], fill=LINE_DARK, width=2)

    draw = ImageDraw.Draw(img)
    return scr_x1, scr_y1, scr_x2, scr_y2, tv_x1, tv_y1, tv_x2, tv_y2


def draw_crt_glow(img, scr_x1, scr_y1, scr_x2, scr_y2):
    """Cool CRT ambient spill — rightward and downward."""
    scr_cx = (scr_x1 + scr_x2) // 2
    scr_cy = (scr_y1 + scr_y2) // 2

    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)

    for r in range(280, 20, -8):
        t = 1.0 - (r - 20) / 260.0
        alpha = int(t ** 2.0 * 48)
        gd.ellipse(
            [scr_cx - r, scr_cy - r // 2,
             scr_cx + r, scr_cy + r // 2],
            fill=(*CRT_COOL_SPILL, alpha)
        )

    out = Image.alpha_composite(img.convert("RGBA"), glow)
    return out.convert("RGB")


# ── Shoulder Involvement (C48 — codified C47 image-rules.md) ─────────────────
# When an arm moves past ~30 degrees from rest, the shoulder line must change.
# Per-character clothing reads: Miri = cardigan shoulder crease; Luma = hoodie
# fabric bunch. Implemented as torso polyline with deltoid bump vertices.

# ── Character Drawing ──────────────────────────────────────────────────────────
# Characters via canonical char_*.py renderers (C53 modular architecture).
# Ground line: GROUND_Y = int(H * 0.90)
# Canonical renderers handle: shoulder involvement, elder posture, expressions,
# clothing physics, face features — all per-character specs.

GROUND_Y = int(H * 0.90)

# Character scale reference (head radii at style-frame scale)
MIRI_HR = 42   # head radius — 3.2 heads tall
MIRI_HU = int(MIRI_HR * 2)
LUMA_HR = 46   # head radius — 3.5 heads tall
LUMA_HU = int(LUMA_HR * 2)


def _cairo_char_to_pil(surface, target_h):
    """Convert a cairo.ImageSurface character to a cropped, resized PIL RGBA image.

    Crops to bounding box, scales to fit target_h while preserving aspect ratio.
    """
    pil_img = _to_pil_rgba(surface)
    bbox = pil_img.getbbox()
    if bbox:
        pil_img = pil_img.crop(bbox)
    if pil_img.height > 0:
        scale_factor = target_h / pil_img.height
        new_w = max(1, int(pil_img.width * scale_factor))
        new_h = max(1, int(pil_img.height * scale_factor))
        pil_img = pil_img.resize((new_w, new_h), Image.LANCZOS)
    return pil_img

def draw_miri_character(img, draw, cx, ground_y, transparent_layer=False):
    """
    Grandma Miri via canonical char_miri renderer.
    WARM expression, facing right (toward CRT/Luma).
    Height: 3.2 heads (MIRI_HU x 3.2).
    C53: Replaced inline drawing with canonical char_miri.draw_miri() import.
    C52: transparent_layer=True skips foot shadow (handled by Wand compositing).
    """
    HU = MIRI_HU
    total_h = int(HU * 3.2)

    # Render via canonical module — WARM expression, facing right (toward CRT/Luma)
    # Warm lamp scene lighting from left (Miri's zone)
    scene_lighting = {
        "key_light_color": (245, 208, 140),   # warm lamp
        "key_light_dir": "left",
        "ambient": (200, 170, 130),
    }
    scale = max(0.3, total_h / 380.0)  # char_miri: 1.0 = 380px at 2x
    surface = _canonical_draw_miri(
        expression="WARM", scale=scale, facing="right",
        scene_lighting=scene_lighting)
    char_pil = _cairo_char_to_pil(surface, total_h)

    # Paste — anchor at foot position (cx, ground_y)
    paste_x = cx - char_pil.width // 2
    paste_y = ground_y - char_pil.height
    img_rgba = img.convert("RGBA")
    img_rgba.paste(char_pil, (paste_x, paste_y), char_pil)
    img.paste(img_rgba.convert("RGB"))
    draw = ImageDraw.Draw(img)

    # Shadow at feet (only when compositing directly onto BG)
    if not transparent_layer:
        draw.ellipse([cx - int(HU * 0.55), ground_y - 4,
                      cx + int(HU * 0.55), ground_y + 10],
                     fill=lerp_color(FLOOR_OAK_DARK, NEAR_BLACK_WARM, 0.55))
    draw = ImageDraw.Draw(img)

    return img, draw



def draw_luma_character(img, draw, cx, ground_y, transparent_layer=False):
    """
    Luma via canonical char_luma renderer.
    CURIOUS expression, facing left (toward Miri and CRT).
    Height: 3.5 heads (LUMA_HU x 3.5).
    C53: Replaced inline drawing with canonical char_luma.draw_luma() import.
    C52: transparent_layer=True skips foot shadow (handled by Wand compositing).
    """
    HU = LUMA_HU
    total_h = int(HU * 3.5)

    # Render via canonical module — CURIOUS expression, facing left (toward Miri/CRT)
    # Mixed scene lighting: warm lamp from left, CRT cool spill from center-right
    scene_lighting = {
        "key_light_color": (130, 175, 160),   # CRT cool spill (Luma is on CRT side)
        "key_light_dir": "left",
        "ambient": (200, 180, 150),
    }
    scale = max(0.3, total_h / 400.0)  # char_luma: 1.0 = 400px at 2x
    surface = _canonical_draw_luma(
        expression="CURIOUS", scale=scale, facing="left",
        scene_lighting=scene_lighting)
    char_pil = _cairo_char_to_pil(surface, total_h)

    # Paste — anchor at foot position (cx, ground_y)
    paste_x = cx - char_pil.width // 2
    paste_y = ground_y - char_pil.height
    img_rgba = img.convert("RGBA")
    img_rgba.paste(char_pil, (paste_x, paste_y), char_pil)
    img.paste(img_rgba.convert("RGB"))
    draw = ImageDraw.Draw(img)

    # Shadow at feet (only when compositing directly onto BG)
    if not transparent_layer:
        draw.ellipse([cx - int(HU * 0.52), ground_y - 4,
                      cx + int(HU * 0.52), ground_y + 10],
                     fill=lerp_color(FLOOR_OAK_DARK, NEAR_BLACK_WARM, 0.55))
    draw = ImageDraw.Draw(img)

    return img, draw


# ── Lighting Passes ────────────────────────────────────────────────────────────

def draw_warm_lamp_glow(img):
    """Warm key light from left — Miri's side."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    lamp_cx = int(W * 0.12)
    lamp_cy = int(H * 0.25)
    for r in range(360, 20, -8):
        t = 1.0 - (r - 20) / 340.0
        alpha = int(t ** 2.0 * 40)
        ld.ellipse([lamp_cx - r, lamp_cy - r // 2,
                    lamp_cx + r, lamp_cy + r // 2],
                   fill=(*LAMP_WARM, alpha))
    out = Image.alpha_composite(img.convert("RGBA"), layer)
    return out.convert("RGB")


def draw_deep_shadow_pass(img):
    """Push corners and edges toward value floor ≤30."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    # Top left corner
    for x in range(0, int(W * 0.14)):
        t = max(0.0, 1.0 - x / (W * 0.14))
        ld.line([(x, 0), (x, int(H * 0.25))],
                fill=(*NEAR_BLACK_WARM, int(t ** 1.5 * 200)))
    # Top right corner
    for x in range(int(W * 0.86), W):
        t = max(0.0, (x - W * 0.86) / max(1, W * 0.14))
        ld.line([(x, 0), (x, int(H * 0.20))],
                fill=(*NEAR_BLACK_WARM, int(t ** 1.5 * 200)))
    # Floor depth vignette
    for y in range(int(H * 0.88), H):
        t = max(0.0, (y - H * 0.88) / max(1, H * 0.12))
        ld.line([(0, y), (W, y)],
                fill=(*NEAR_BLACK_WARM, int(t * 80)))
    out = Image.alpha_composite(img.convert("RGBA"), layer)
    return out.convert("RGB")


# ── Caption / Label ────────────────────────────────────────────────────────────

def draw_caption(img):
    """Minimal style frame label: title + scene ID bottom-left."""
    draw = ImageDraw.Draw(img)
    try:
        from PIL import ImageFont
        font = ImageFont.load_default()
    except Exception:
        font = None

    label = "SF06 — THE HAND-OFF  |  Miri + Luma + CRT  |  REAL WORLD  |  C52 Hana Okonkwo (Wand composite)"
    draw.rectangle([0, H - 22, W, H], fill=NEAR_BLACK_WARM)
    draw.text((8, H - 18), label, fill=AGED_CREAM, font=font)


# ── Main ───────────────────────────────────────────────────────────────────────

def _make_char_mask(char_layer):
    """Extract a binary mask (mode 'L') from the alpha channel of an RGBA layer."""
    if char_layer.mode != "RGBA":
        char_layer = char_layer.convert("RGBA")
    return char_layer.split()[3]


def _char_bbox(mask):
    """Return (x1, y1, x2, y2) bounding box of non-zero pixels in mask."""
    bbox = mask.getbbox()
    if bbox is None:
        return (0, 0, 1, 1)
    return bbox


def main():
    random.seed(44)

    _here = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, _here)

    out_dir = output_dir('color', 'style_frames')
    out_path = os.path.join(out_dir, "LTG_COLOR_sf_miri_luma_handoff.png")
    os.makedirs(out_dir, exist_ok=True)

    # ── Background (Layers 1-4) ───────────────────────────────────────────────
    img = Image.new("RGB", (W, H), WALL_BASE)

    # Layer 1: Background room
    draw, vp_x, vp_y, bw_left, bw_top, bw_right, bw_bot = draw_background(img)

    # Layer 2: CRT — the central compositional object
    crt_result = draw_crt_tv(img)
    scr_x1, scr_y1, scr_x2, scr_y2, tv_x1, tv_y1, tv_x2, tv_y2 = crt_result
    draw = ImageDraw.Draw(img)

    # Layer 3: CRT cool glow (sets warm/cool right-side tone before characters)
    img = draw_crt_glow(img, scr_x1, scr_y1, scr_x2, scr_y2)
    draw = ImageDraw.Draw(img)

    # Layer 4: Warm lamp glow (Miri's left side)
    img = draw_warm_lamp_glow(img)
    draw = ImageDraw.Draw(img)

    # Save background-only layer for compositing reference
    bg_only = img.copy()

    # ── Character positions ───────────────────────────────────────────────────
    miri_cx = int(W * 0.285)
    luma_cx = int(W * 0.72)

    # ── Wand compositing pipeline ─────────────────────────────────────────────
    # Per C52 assignment: characters on separate transparent layers, composited
    # with Wand contact shadows, bounce light, scene tint, blend modes.
    # Per C50 lighting spec: Living Room settings.
    #   - Reading lamp LEFT: SUNLIT_AMBER (245, 208, 140) = key (Miri zone)
    #   - CRT center-left: CRT_COOL_SPILL (130, 175, 160) = cool accent
    #   - Contact shadow surface: (185, 165, 125), alpha 50
    #   - Bounce light: warm floor/carpet bounce, alpha 20

    _use_wand = True
    try:
        from LTG_TOOL_wand_composite import (
            wand_contact_shadow, wand_bounce_light, wand_edge_tint,
            wand_scene_lighting_overlay, wand_color_transfer,
            pil_to_wand, wand_to_pil
        )
        from LTG_TOOL_contact_shadow import sample_surface_color
    except ImportError:
        _use_wand = False
        print("[C52] Wand not available — falling back to legacy compositing.")

    if _use_wand:
        # Living Room lighting spec (C50 document)
        SURFACE_COLOR = (185, 165, 125)   # carpet/floor
        SHADOW_ALPHA = 50
        BOUNCE_ALPHA = 20
        EDGE_TINT_ALPHA = 18
        COLOR_TRANSFER_STRENGTH = 0.12
        BOUNCE_GROUND_COLOR = (185, 165, 125)  # warm carpet

        # --- Draw Miri on transparent layer ---
        miri_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        miri_draw = ImageDraw.Draw(miri_layer)
        miri_layer, miri_draw = draw_miri_character(
            miri_layer, miri_draw, miri_cx, GROUND_Y, transparent_layer=True)
        miri_mask = _make_char_mask(miri_layer)
        miri_bbox = _char_bbox(miri_mask)
        miri_width = miri_bbox[2] - miri_bbox[0]
        miri_height = miri_bbox[3] - miri_bbox[1]

        # --- Draw Luma on transparent layer ---
        luma_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        luma_draw = ImageDraw.Draw(luma_layer)
        luma_layer, luma_draw = draw_luma_character(
            luma_layer, luma_draw, luma_cx, GROUND_Y, transparent_layer=True)
        luma_mask = _make_char_mask(luma_layer)
        luma_bbox = _char_bbox(luma_mask)
        luma_width = luma_bbox[2] - luma_bbox[0]
        luma_height = luma_bbox[3] - luma_bbox[1]

        # --- Compositing pass order (C50 spec): ---
        # BG > overlay > shadow > character > scene shading > bounce > edge tint > color transfer

        # Convert BG to RGBA for Wand operations
        composite = img.convert("RGBA")

        # Step 1: Contact shadows (Wand Gaussian blur — proper soft falloff)
        composite = wand_contact_shadow(
            composite, miri_cx, GROUND_Y, miri_width,
            surface_color=SURFACE_COLOR, shadow_alpha=SHADOW_ALPHA,
            blur_sigma=5.0, height_px=12)
        composite = wand_contact_shadow(
            composite, luma_cx, GROUND_Y, luma_width,
            surface_color=SURFACE_COLOR, shadow_alpha=SHADOW_ALPHA,
            blur_sigma=5.0, height_px=12)

        # Step 2: Paste characters onto composite
        composite = Image.alpha_composite(composite, miri_layer)
        draw = ImageDraw.Draw(composite)  # refresh draw context
        composite = Image.alpha_composite(composite, luma_layer)
        draw = ImageDraw.Draw(composite)  # refresh draw context

        # Step 3: Scene lighting via Wand Screen blend
        # Warm lamp glow on Miri's side (left)
        composite = wand_scene_lighting_overlay(
            composite, light_color=(245, 208, 140),
            light_x=int(W * 0.12), light_y=int(H * 0.40),
            radius=320, intensity=0.18, blend_mode="screen")
        # CRT cool spill on Luma's side (right of center)
        composite = wand_scene_lighting_overlay(
            composite, light_color=(130, 175, 160),
            light_x=(scr_x1 + scr_x2) // 2, light_y=(scr_y1 + scr_y2) // 2,
            radius=260, intensity=0.14, blend_mode="screen")

        # Step 4: Bounce light on characters (warm carpet color from below)
        miri_bounced = wand_bounce_light(
            miri_layer, miri_mask, GROUND_Y, miri_height,
            ground_color=BOUNCE_GROUND_COLOR, bounce_alpha=BOUNCE_ALPHA, coverage=0.25)
        luma_bounced = wand_bounce_light(
            luma_layer, luma_mask, GROUND_Y, luma_height,
            ground_color=BOUNCE_GROUND_COLOR, bounce_alpha=BOUNCE_ALPHA, coverage=0.25)
        composite = Image.alpha_composite(composite, miri_bounced)
        draw = ImageDraw.Draw(composite)
        composite = Image.alpha_composite(composite, luma_bounced)
        draw = ImageDraw.Draw(composite)

        # Step 5: Edge tint (environment color bleed on character edges)
        # Miri: warm side — tint from lamp amber
        miri_tinted = wand_edge_tint(
            miri_layer, miri_mask, bg_color=(245, 208, 140),
            tint_alpha=EDGE_TINT_ALPHA, edge_width=3)
        composite = Image.alpha_composite(composite, miri_tinted)
        draw = ImageDraw.Draw(composite)
        # Luma: cool side — tint from CRT spill
        luma_tinted = wand_edge_tint(
            luma_layer, luma_mask, bg_color=(130, 175, 160),
            tint_alpha=EDGE_TINT_ALPHA, edge_width=3)
        composite = Image.alpha_composite(composite, luma_tinted)
        draw = ImageDraw.Draw(composite)

        # Step 6: Color transfer (environment-to-character tinting via Soft Light)
        miri_transferred = wand_color_transfer(
            miri_layer, miri_mask, bg_only,
            miri_cx, GROUND_Y, sample_radius=80,
            tint_strength=COLOR_TRANSFER_STRENGTH)
        composite = Image.alpha_composite(composite, miri_transferred)
        draw = ImageDraw.Draw(composite)
        luma_transferred = wand_color_transfer(
            luma_layer, luma_mask, bg_only,
            luma_cx, GROUND_Y, sample_radius=80,
            tint_strength=COLOR_TRANSFER_STRENGTH)
        composite = Image.alpha_composite(composite, luma_transferred)
        draw = ImageDraw.Draw(composite)

        img = composite.convert("RGB")

    else:
        # Legacy path: draw characters directly onto BG (pre-C52 behavior)
        img, draw = draw_miri_character(img, draw, miri_cx, GROUND_Y)
        draw = ImageDraw.Draw(img)
        img, draw = draw_luma_character(img, draw, luma_cx, GROUND_Y)
        draw = ImageDraw.Draw(img)

    # ── Post-compositing passes (same as before) ─────────────────────────────

    # Dual temperature overlay (warm left / cool right)
    img = alpha_overlay_rect(img, 0, 0, W // 2, H, SUNLIT_AMBER, 28)
    img = alpha_overlay_rect(img, W // 2, 0, W, H, CRT_COOL_SPILL, 32)
    draw = ImageDraw.Draw(img)

    # Deep shadow pass (value floor <=30)
    img = draw_deep_shadow_pass(img)
    draw = ImageDraw.Draw(img)

    # Caption
    draw_caption(img)

    # Size rule compliance
    img.thumbnail((1280, 1280), Image.LANCZOS)
    img.save(out_path)
    print(f"[Hana C52] Saved: {out_path}  ({img.width}x{img.height}px)")
    print("  Composition: Miri (L) + CRT (C) + Luma (R) — The Hand-Off")
    print("  Pipeline: PIL generates > Wand composites (contact shadow, bounce,")
    print("            edge tint, color transfer, scene lighting) > PIL QA")
    print("  Lighting: Living Room spec (C50) — warm lamp L, CRT cool spill C-R")
    print("  Palette: Real World only. No GL colors.")


if __name__ == "__main__":
    main()
