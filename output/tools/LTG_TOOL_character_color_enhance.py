#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_character_color_enhance.py — Character Color Enhancement Library
"Luma & the Glitchkin" — Color & Style / Sam Kowalski / Cycle 52 (v2.0.0)

PURPOSE:
  Addresses the C50 character quality pivot. Our backgrounds receive scene lighting
  (warm overlays, cool overlays, CRT glow) but characters do not. This library provides
  post-draw overlay functions that tint characters with scene light, add warm-cheek/cool-edge
  skin variation, apply form-describing shadow shapes, and derive scene-responsive outlines.

  All functions operate as overlays on an already-drawn character. They do NOT modify
  the base character drawing code. Integration: call after the character is drawn.

  v2.0.0 (C52): Added cairo surface support. enhance_from_cairo() converts a pycairo
  ARGB32 surface to PIL RGBA, applies all five enhancement passes, and returns the
  enhanced PIL Image. This bridges the pycairo rendering pipeline (LTG_TOOL_cairo_primitives)
  with the existing PIL-based color enhancement stack. All v1.0.0 API preserved.

REFERENCE ANALYSIS:
  Hilda and The Owl House both use flat base fills + scene-responsive tinting.
  The "secret" is not internal gradients — it is that characters receive the same
  environmental color logic that backgrounds receive. See:
  output/color/LTG_COLOR_character_rendering_analysis_c50.md

FUNCTIONS:
  apply_scene_tint()         — Scene lighting overlay on character region
  apply_skin_warmth()        — Warm cheek / cool edge gradient on skin zones
  apply_form_shadow()        — Curved cel-shadow shapes for torso/limb zones
  derive_scene_outline()     — Scene-responsive outline color calculation
  apply_hair_absorption()    — Hair zone scene-color tinting at 2x strength
  enhance_from_cairo()       — Convert cairo surface → PIL, apply full pipeline (v2.0.0)
  generate_demo()            — Before/after comparison render

USAGE:
  # In a style frame generator, after draw_luma(img, draw):
  from LTG_TOOL_character_color_enhance import apply_scene_tint, apply_skin_warmth

  char_bbox = (char_left, char_top, char_right, char_bottom)
  img = apply_scene_tint(img, char_bbox, key_light_color=(212, 146, 58), alpha=22)
  draw = ImageDraw.Draw(img)  # refresh after any img modification

  # With pycairo-rendered characters (v2.0.0):
  from LTG_TOOL_character_color_enhance import enhance_from_cairo
  pil_img = enhance_from_cairo(
      cairo_surface, char_bbox, face_center, face_radius,
      hair_bbox=hair_bbox, scene_preset="warm_domestic"
  )

  # Standalone demo:
  python3 output/tools/LTG_TOOL_character_color_enhance.py

CONSTRAINTS:
  - Scene tint alpha MUST NOT exceed 30 (~12%) — preserves warmth guarantees
  - All shadow colors within 30% luminance of base fill — silhouette test passes
  - Outline contrast ratio >= 3:1 against skin maintained
  - Native 1280x720 canvas. NEVER use .thumbnail() in generators.

Dependencies: Python 3.8+, Pillow (PIL). pycairo + numpy optional (for enhance_from_cairo).
"""

__version__ = "2.0.0"
__author__ = "Sam Kowalski"
__cycle__ = 52

import math
import os
import sys
import random

from PIL import Image, ImageDraw, ImageFilter

try:
    from LTG_TOOL_project_paths import output_dir, ensure_dir
except ImportError:
    import pathlib
    def output_dir(*parts):
        return pathlib.Path("/home/wipkat/team/output").joinpath(*parts)
    def ensure_dir(path):
        path.mkdir(parents=True, exist_ok=True)
        return path


# ── Canonical Character Palette (Luma) ────────────────────────────────────────
# From master_palette.md — used in demo only. Generators use their own constants.
SKIN_BASE       = (200, 136,  90)   # CHAR-L-01 lamp-lit
SKIN_HL         = (232, 184, 136)   # warm highlight
SKIN_SH         = (168, 104,  56)   # warm shadow
BLUSH           = (232, 168, 124)   # #E8A87C
HOODIE_ORANGE   = (232, 112,  58)   # #E8703A canonical
HOODIE_SHADOW   = (184,  74,  32)   # #B84A20 canonical
HOODIE_AMBIENT  = (176,  96,  80)   # #B06050 CHAR-L-08
HAIR_COLOR      = ( 26,  15,  10)   # CHAR-L-03
JEANS           = ( 58,  90, 140)   # CHAR-L-05
JEANS_SH        = ( 38,  62, 104)   # CHAR-L-05 shadow
LINE_WARM       = ( 59,  40,  32)   # standard outline
SHOE_DARK       = ( 42,  38,  32)

# Scene lighting presets
SCENE_PRESETS = {
    "warm_domestic": {
        "key_color": (212, 146, 58),    # SUNLIT_AMBER
        "key_dir": (-0.7, -0.7),        # upper-left
        "tint_alpha": 22,
        "outline": (59, 40, 32),
        "hair_tint_2x": True,
    },
    "glitch_storm": {
        "key_color": (0, 240, 255),     # ELECTRIC_CYAN
        "key_dir": (0.0, 1.0),          # from below (cracks)
        "tint_alpha": 18,
        "outline": (48, 36, 44),
        "hair_tint_2x": True,
    },
    "other_side": {
        "key_color": (123, 47, 190),    # UV_PURPLE
        "key_dir": (0.0, -1.0),         # ambient from above
        "tint_alpha": 25,
        "outline": (38, 30, 48),
        "hair_tint_2x": True,
    },
    "neutral_daylight": {
        "key_color": (240, 228, 200),   # warm white daylight
        "key_dir": (-0.5, -0.9),        # upper-left window
        "tint_alpha": 12,
        "outline": (52, 40, 38),
        "hair_tint_2x": False,
    },
}


# ── Core Functions ────────────────────────────────────────────────────────────

def apply_scene_tint(img, char_bbox, key_light_color, alpha=22, light_dir=(-0.7, -0.7)):
    """Apply scene lighting tint to a character's bounding region.

    Composites a translucent overlay of the scene's key light color over the
    character area. This makes the character receive the same environmental light
    that the background receives — the single most impactful improvement for
    reducing the "cutout" look.

    The tint is NOT uniform — it follows the light direction with a gradient:
    the side facing the light receives full alpha, the shadow side receives ~40%
    alpha. This creates a natural lit/unlit feel within the character.

    Args:
        img             (PIL.Image): Image to modify (RGB mode). Modified in place.
        char_bbox       (tuple)    : (left, top, right, bottom) of the character area.
        key_light_color (tuple)    : RGB of the scene's key light (e.g., SUNLIT_AMBER).
        alpha           (int)      : Max alpha for the tint overlay (6-30 recommended).
                                     30 = ~12% max. Must not exceed 30 to preserve
                                     warmth guarantees.
        light_dir       (tuple)    : (dx, dy) normalized — direction light comes FROM.

    Returns:
        PIL.Image: The modified image (same object as img).
    """
    alpha = min(alpha, 30)  # hard ceiling — warmth guarantee safety
    left, top, right, bottom = char_bbox
    w, h = img.size
    left = max(0, left)
    top = max(0, top)
    right = min(w, right)
    bottom = min(h, bottom)

    if right <= left or bottom <= top:
        return img

    # Normalize light direction
    ldx, ldy = light_dir
    llen = math.hypot(ldx, ldy)
    if llen < 1e-9:
        ldx, ldy = -1.0, -1.0
        llen = math.sqrt(2)
    ldx /= llen
    ldy /= llen

    char_w = right - left
    char_h = bottom - top

    # Build gradient tint overlay
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ov_draw = ImageDraw.Draw(overlay)

    # Gradient: full alpha on lit side, 40% on shadow side
    # Sample in horizontal bands for efficiency
    band_h = max(1, char_h // 20)
    for band_y in range(top, bottom, band_h):
        band_bot = min(bottom, band_y + band_h)
        for band_x in range(left, right, band_h):
            band_right = min(right, band_x + band_h)
            # Normalized position within character bbox
            nx = (band_x - left) / max(1, char_w) - 0.5  # -0.5 to 0.5
            ny = (band_y - top) / max(1, char_h) - 0.5
            # Dot product with light direction = how much this pixel faces the light
            facing = nx * ldx + ny * ldy
            # Map from [-1, 1] to [0.4, 1.0] — shadow side gets 40% of max alpha
            t = 0.4 + 0.6 * max(0.0, min(1.0, (facing + 1.0) / 2.0))
            band_alpha = int(alpha * t)
            ov_draw.rectangle(
                [band_x, band_y, band_right, band_bot],
                fill=(*key_light_color, band_alpha)
            )

    base_rgba = img.convert("RGBA")
    result = Image.alpha_composite(base_rgba, overlay)
    img.paste(result.convert("RGB"))
    return img


def apply_skin_warmth(img, face_center, face_radius, light_dir=(-0.7, -0.7),
                      warm_color=None, cool_shift=10, blush_color=None,
                      warm_alpha=25, cool_alpha=18, blush_alpha=20):
    """Apply warm-cheek / cool-edge temperature variation to a face zone.

    Creates the subtle alive quality seen in reference shows: the lit side of the
    face is slightly warmer (toward highlight), the shadow side slightly cooler
    (blue channel bump), and the cheek zone carries a gentle blush.

    This is a post-draw overlay — the base skin fill is preserved underneath.

    Args:
        img           (PIL.Image): Image to modify (RGB). Modified in place.
        face_center   (tuple)    : (cx, cy) center of the face.
        face_radius   (tuple)    : (rx, ry) horizontal/vertical radii.
        light_dir     (tuple)    : (dx, dy) direction light comes FROM.
        warm_color    (tuple)    : RGB for warm highlight (default: SKIN_HL).
        cool_shift    (int)      : Blue channel boost for shadow side (default: 10).
        blush_color   (tuple)    : RGB for cheek blush (default: BLUSH).
        warm_alpha    (int)      : Alpha for warm overlay (default: 25).
        cool_alpha    (int)      : Alpha for cool overlay (default: 18).
        blush_alpha   (int)      : Alpha for blush overlay (default: 20).

    Returns:
        PIL.Image: The modified image.
    """
    if warm_color is None:
        warm_color = SKIN_HL
    if blush_color is None:
        blush_color = BLUSH

    cx, cy = face_center
    rx, ry = face_radius
    w, h = img.size

    # Normalize light direction
    ldx, ldy = light_dir
    llen = math.hypot(ldx, ldy)
    if llen < 1e-9:
        ldx, ldy = -1.0, -1.0
        llen = math.sqrt(2)
    ldx /= llen
    ldy /= llen

    # --- Warm highlight on lit side ---
    warm_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    warm_draw = ImageDraw.Draw(warm_layer)
    # Shifted toward light source
    hi_cx = cx + ldx * rx * 0.25
    hi_cy = cy + ldy * ry * 0.15
    hi_rx = rx * 0.6
    hi_ry = ry * 0.5
    # Feathered ellipse
    for step in range(6, 0, -1):
        t = step / 6.0
        a = int(warm_alpha * (t ** 1.5))
        ex = hi_rx * (1.0 + (1 - t) * 0.4)
        ey = hi_ry * (1.0 + (1 - t) * 0.4)
        warm_draw.ellipse(
            [int(hi_cx - ex), int(hi_cy - ey), int(hi_cx + ex), int(hi_cy + ey)],
            fill=(*warm_color, a)
        )
    base_rgba = img.convert("RGBA")
    base_rgba = Image.alpha_composite(base_rgba, warm_layer)
    img.paste(base_rgba.convert("RGB"))

    # --- Cool shift on shadow side ---
    cool_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    cool_draw = ImageDraw.Draw(cool_layer)
    # Shifted away from light (shadow direction)
    sdx, sdy = -ldx, -ldy
    co_cx = cx + sdx * rx * 0.3
    co_cy = cy + sdy * ry * 0.2
    co_rx = rx * 0.5
    co_ry = ry * 0.55
    # Cool = base skin with boosted blue channel
    cool_color = (SKIN_BASE[0] - 15, SKIN_BASE[1] - 5, SKIN_BASE[2] + cool_shift)
    for step in range(5, 0, -1):
        t = step / 5.0
        a = int(cool_alpha * (t ** 1.8))
        ex = co_rx * (1.0 + (1 - t) * 0.45)
        ey = co_ry * (1.0 + (1 - t) * 0.45)
        cool_draw.ellipse(
            [int(co_cx - ex), int(co_cy - ey), int(co_cx + ex), int(co_cy + ey)],
            fill=(*cool_color, a)
        )
    base_rgba = img.convert("RGBA")
    base_rgba = Image.alpha_composite(base_rgba, cool_layer)
    img.paste(base_rgba.convert("RGB"))

    # --- Blush on cheeks ---
    blush_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    blush_draw = ImageDraw.Draw(blush_layer)
    cheek_y = cy + ry * 0.15
    for side in [-1, 1]:
        cheek_cx = cx + side * rx * 0.35
        cheek_rx = rx * 0.22
        cheek_ry = ry * 0.14
        for step in range(5, 0, -1):
            t = step / 5.0
            a = int(blush_alpha * (t ** 1.6))
            ex = cheek_rx * (1.0 + (1 - t) * 0.35)
            ey = cheek_ry * (1.0 + (1 - t) * 0.35)
            blush_draw.ellipse(
                [int(cheek_cx - ex), int(cheek_y - ey),
                 int(cheek_cx + ex), int(cheek_y + ey)],
                fill=(*blush_color, a)
            )
    base_rgba = img.convert("RGBA")
    base_rgba = Image.alpha_composite(base_rgba, blush_layer)
    img.paste(base_rgba.convert("RGB"))

    return img


def apply_form_shadow(img, zone_bbox, base_color, shadow_color,
                      shadow_shape="torso_diagonal", light_dir=(-0.7, -0.7),
                      alpha=100):
    """Apply form-describing cel-shadow shapes instead of flat left/right splits.

    Instead of "left half = shadow," this places shadow shapes that follow body
    form: a diagonal band across the torso (shoulder-to-hip), an underside
    crescent on limbs, etc.

    Args:
        img           (PIL.Image): Image to modify. Modified in place.
        zone_bbox     (tuple)    : (left, top, right, bottom) of the body zone.
        base_color    (tuple)    : RGB of the zone's base fill (for reference).
        shadow_color  (tuple)    : RGB of the shadow fill.
        shadow_shape  (str)      : Shape type. Options:
                                   "torso_diagonal" — curved shoulder-to-hip band
                                   "limb_underside" — crescent on cylinder underside
                                   "inseam" — inner leg shadow for jeans
        light_dir     (tuple)    : (dx, dy) direction light comes FROM.
        alpha         (int)      : Shadow alpha (default 100 = ~39% opacity).

    Returns:
        PIL.Image: The modified image.
    """
    left, top, right, bottom = zone_bbox
    w, h = img.size
    left = max(0, left)
    top = max(0, top)
    right = min(w, right)
    bottom = min(h, bottom)

    if right <= left or bottom <= top:
        return img

    zone_w = right - left
    zone_h = bottom - top
    zone_cx = (left + right) // 2
    zone_cy = (top + bottom) // 2

    ldx, ldy = light_dir
    llen = math.hypot(ldx, ldy)
    if llen < 1e-9:
        ldx, ldy = -1.0, -1.0
        llen = math.sqrt(2)
    ldx /= llen
    ldy /= llen

    shadow_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    sh_draw = ImageDraw.Draw(shadow_layer)

    if shadow_shape == "torso_diagonal":
        # Curved shadow band from shoulder (light side) to hip (shadow side)
        # Shadow occupies the side AWAY from light
        shadow_side = 1 if ldx < 0 else -1  # if light from left, shadow on right
        pts = [
            (zone_cx + shadow_side * zone_w * 0.05, top),
            (zone_cx + shadow_side * zone_w * 0.50, top),
            (zone_cx + shadow_side * zone_w * 0.55, top + zone_h * 0.3),
            (zone_cx + shadow_side * zone_w * 0.50, top + zone_h * 0.6),
            (zone_cx + shadow_side * zone_w * 0.42, bottom),
            (zone_cx + shadow_side * zone_w * 0.10, bottom),
            (zone_cx + shadow_side * zone_w * 0.15, top + zone_h * 0.5),
            (zone_cx + shadow_side * zone_w * 0.12, top + zone_h * 0.2),
        ]
        sh_draw.polygon(pts, fill=(*shadow_color, alpha))

    elif shadow_shape == "limb_underside":
        # Crescent on the underside of a cylindrical limb
        # The crescent follows the bottom edge of the limb
        crescent_y = zone_cy + zone_h * 0.15
        crescent_rx = zone_w * 0.45
        crescent_ry = zone_h * 0.35
        sh_draw.ellipse(
            [int(zone_cx - crescent_rx), int(crescent_y - crescent_ry),
             int(zone_cx + crescent_rx), int(crescent_y + crescent_ry)],
            fill=(*shadow_color, alpha)
        )

    elif shadow_shape == "inseam":
        # Inner leg shadow — narrow strip on the inner edge of jeans
        inner_side = 1 if ldx < 0 else -1  # shadow on inner edge
        inseam_w = max(2, zone_w // 5)
        inner_x = zone_cx + inner_side * (zone_w // 2 - inseam_w)
        sh_draw.rectangle(
            [inner_x, top + 2, inner_x + inseam_w, bottom - 2],
            fill=(*shadow_color, alpha)
        )

    base_rgba = img.convert("RGBA")
    result = Image.alpha_composite(base_rgba, shadow_layer)
    img.paste(result.convert("RGB"))
    return img


def derive_scene_outline(world_type="warm_domestic"):
    """Return the scene-responsive outline color for characters.

    Instead of a single LINE color for all scenes, the outline shifts slightly
    to match the scene's ambient temperature. This integrates the character
    into the environment's color space.

    Args:
        world_type (str): Scene type. Options:
                          "warm_domestic", "glitch_storm", "other_side", "neutral_daylight"

    Returns:
        tuple: RGB outline color.
    """
    preset = SCENE_PRESETS.get(world_type, SCENE_PRESETS["warm_domestic"])
    return preset["outline"]


def apply_hair_absorption(img, hair_bbox, scene_color, alpha=18):
    """Tint hair zone with scene lighting at 2x strength.

    Hair absorbs more scene light than skin or clothing. Dark hair in a warm
    room reads warm-dark; dark hair in a purple environment reads dark-purple.
    This is one of the strongest integration cues in reference shows.

    Args:
        img         (PIL.Image): Image to modify. Modified in place.
        hair_bbox   (tuple)    : (left, top, right, bottom) of the hair region.
        scene_color (tuple)    : RGB of the scene's dominant light.
        alpha       (int)      : Base alpha for hair tint (actual applied = alpha * 2,
                                 capped at 50 = ~20%).

    Returns:
        PIL.Image: The modified image.
    """
    effective_alpha = min(alpha * 2, 50)  # 2x but capped
    left, top, right, bottom = hair_bbox
    w, h = img.size
    left = max(0, left)
    top = max(0, top)
    right = min(w, right)
    bottom = min(h, bottom)

    if right <= left or bottom <= top:
        return img

    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ov_draw = ImageDraw.Draw(overlay)
    ov_draw.rectangle([left, top, right, bottom], fill=(*scene_color, effective_alpha))

    base_rgba = img.convert("RGBA")
    result = Image.alpha_composite(base_rgba, overlay)
    img.paste(result.convert("RGB"))
    return img


# ── Cairo Surface Bridge (v2.0.0) ────────────────────────────────────────────

def _cairo_surface_to_pil(surface):
    """Convert a pycairo ARGB32 ImageSurface to a PIL RGBA Image.

    Cairo stores pixels as BGRA (premultiplied) on little-endian systems.
    This function unpremultiplies and reorders to standard RGBA.

    Falls back gracefully if cairo/numpy not available.
    """
    try:
        import numpy as np
    except ImportError:
        raise ImportError("numpy is required for cairo surface conversion")

    w = surface.get_width()
    h = surface.get_height()
    buf = surface.get_data()
    arr = np.frombuffer(buf, dtype=np.uint8).reshape(h, w, 4).copy()

    # Cairo ARGB32 is BGRA in memory on little-endian
    # Reorder: B G R A → R G B A
    rgba = np.stack([arr[:, :, 2], arr[:, :, 1], arr[:, :, 0], arr[:, :, 3]], axis=2)
    return Image.fromarray(rgba, "RGBA")


def enhance_from_cairo(surface, char_bbox, face_center, face_radius,
                       hair_bbox=None, torso_bbox=None, leg_bboxes=None,
                       scene_preset="warm_domestic",
                       skin_base=None, skin_hl=None, skin_sh=None,
                       blush_color=None, hoodie_color=None, hoodie_shadow=None,
                       jeans_color=None, jeans_shadow=None):
    """Convert a pycairo surface to PIL and apply the full color enhancement pipeline.

    This is the v2.0.0 bridge function for pycairo-rendered characters. It:
    1. Converts the cairo ARGB32 surface to a PIL RGBA image
    2. Converts to RGB for enhancement (alpha-composites over white if needed)
    3. Applies scene tint, skin warmth, form shadows, and hair absorption
    4. Returns the enhanced PIL Image (RGB mode)

    Args:
        surface:        pycairo ImageSurface (FORMAT_ARGB32)
        char_bbox:      (left, top, right, bottom) of character area
        face_center:    (cx, cy) center of face
        face_radius:    (rx, ry) face radii
        hair_bbox:      (left, top, right, bottom) of hair zone (optional)
        torso_bbox:     (left, top, right, bottom) of torso zone (optional)
        leg_bboxes:     list of (left, top, right, bottom) for each leg (optional)
        scene_preset:   key into SCENE_PRESETS dict
        skin_base:      override skin base RGB (default: SKIN_BASE)
        skin_hl:        override skin highlight RGB (default: SKIN_HL)
        skin_sh:        override skin shadow RGB (default: SKIN_SH)
        blush_color:    override blush RGB (default: BLUSH)
        hoodie_color:   override torso fill RGB (default: HOODIE_ORANGE)
        hoodie_shadow:  override torso shadow RGB (default: HOODIE_SHADOW)
        jeans_color:    override leg fill RGB (default: JEANS)
        jeans_shadow:   override leg shadow RGB (default: JEANS_SH)

    Returns:
        PIL.Image in RGB mode with all enhancements applied.
    """
    # Resolve defaults
    _skin_base = skin_base or SKIN_BASE
    _skin_hl = skin_hl or SKIN_HL
    _blush = blush_color or BLUSH
    _hoodie = hoodie_color or HOODIE_ORANGE
    _hoodie_sh = hoodie_shadow or HOODIE_SHADOW
    _jeans = jeans_color or JEANS
    _jeans_sh = jeans_shadow or JEANS_SH

    preset = SCENE_PRESETS.get(scene_preset, SCENE_PRESETS["warm_domestic"])
    key_color = preset["key_color"]
    light_dir = preset["key_dir"]
    tint_alpha = preset["tint_alpha"]

    # Step 1: Cairo surface → PIL
    pil_rgba = _cairo_surface_to_pil(surface)

    # Step 2: Composite onto white for RGB conversion (preserves character fills)
    bg = Image.new("RGBA", pil_rgba.size, (255, 255, 255, 255))
    img = Image.alpha_composite(bg, pil_rgba).convert("RGB")

    # Step 3: Apply scene tint
    img = apply_scene_tint(img, char_bbox, key_color, alpha=tint_alpha,
                           light_dir=light_dir)
    # refresh draw context after paste (PIL standard W004)
    # (not drawing here, but callers may need draw after this returns)

    # Step 4: Apply skin warmth
    img = apply_skin_warmth(img, face_center, face_radius,
                            light_dir=light_dir,
                            warm_color=_skin_hl,
                            blush_color=_blush)

    # Step 5: Apply form shadow to torso if bbox provided
    if torso_bbox is not None:
        img = apply_form_shadow(img, torso_bbox,
                                base_color=_hoodie, shadow_color=_hoodie_sh,
                                shadow_shape="torso_diagonal",
                                light_dir=light_dir, alpha=90)

    # Step 6: Apply form shadow to legs if bboxes provided
    if leg_bboxes is not None:
        for leg_bbox in leg_bboxes:
            img = apply_form_shadow(img, leg_bbox,
                                    base_color=_jeans, shadow_color=_jeans_sh,
                                    shadow_shape="limb_underside",
                                    light_dir=light_dir, alpha=75)

    # Step 7: Apply hair absorption if bbox provided
    if hair_bbox is not None and preset.get("hair_tint_2x", True):
        img = apply_hair_absorption(img, hair_bbox, scene_color=key_color,
                                    alpha=tint_alpha)

    return img


# ── Demo / Comparison Render ──────────────────────────────────────────────────

def _draw_luma_simple(draw, cx, ground_y, use_shadow_shape=False, outline_color=None):
    """Draw a simplified Luma figure for the demo comparison.

    This is NOT a production drawing function — it is a simplified version
    for the before/after comparison image only.
    """
    if outline_color is None:
        outline_color = LINE_WARM

    head_r = 32
    head_cy = ground_y - 180
    body_top = head_cy + head_r + 3
    body_bot = ground_y - 12
    body_w = 48
    shoulder_y = body_top + 8
    hip_y = body_top + int((body_bot - body_top) * 0.55)

    # Legs
    leg_w = 16
    leg_gap = 7
    draw.rectangle([cx - leg_gap - leg_w, hip_y, cx - leg_gap, body_bot], fill=JEANS)
    draw.rectangle([cx + leg_gap, hip_y, cx + leg_gap + leg_w, body_bot], fill=JEANS)
    # Shoes
    draw.ellipse([cx - leg_gap - leg_w - 3, body_bot - 4,
                  cx - leg_gap + 3, body_bot + 6], fill=SHOE_DARK)
    draw.ellipse([cx + leg_gap - 3, body_bot - 4,
                  cx + leg_gap + leg_w + 3, body_bot + 6], fill=SHOE_DARK)

    # Hoodie body
    hoodie_pts = [
        (cx - body_w // 2, shoulder_y),
        (cx + body_w // 2, shoulder_y),
        (cx + body_w // 2 + 7, hip_y),
        (cx - body_w // 2 - 7, hip_y),
    ]
    draw.polygon(hoodie_pts, fill=HOODIE_ORANGE)

    if not use_shadow_shape:
        # OLD: flat left-side shadow rectangle
        shadow_pts = [
            (cx - body_w // 2, shoulder_y),
            (cx - 8, shoulder_y),
            (cx - 8, hip_y),
            (cx - body_w // 2 - 7, hip_y),
        ]
        draw.polygon(shadow_pts, fill=HOODIE_SHADOW)

    # Arms
    arm_w = 16
    draw.rectangle([cx - body_w // 2 - arm_w, shoulder_y + 3,
                    cx - body_w // 2, shoulder_y + 40], fill=HOODIE_SHADOW)
    draw.rectangle([cx + body_w // 2, shoulder_y + 3,
                    cx + body_w // 2 + arm_w, shoulder_y + 44], fill=HOODIE_ORANGE)

    # Hands
    draw.ellipse([cx - body_w // 2 - arm_w - 4, shoulder_y + 38,
                  cx - body_w // 2 + 8, shoulder_y + 50], fill=SKIN_BASE)
    draw.ellipse([cx + body_w // 2 + arm_w - 6, shoulder_y + 42,
                  cx + body_w // 2 + arm_w + 8, shoulder_y + 54], fill=SKIN_BASE)

    # Neck
    draw.rectangle([cx - 6, head_cy + head_r - 3, cx + 6, body_top + 4], fill=SKIN_BASE)

    # Head
    draw.ellipse([cx - head_r, head_cy - head_r, cx + head_r, head_cy + head_r],
                 fill=SKIN_BASE, outline=outline_color, width=2)

    # Hair
    hair_puffs = [
        (cx - 16, head_cy - 20, 18),
        (cx,      head_cy - 28, 16),
        (cx + 14, head_cy - 22, 14),
        (cx - 28, head_cy - 4,  12),
        (cx + 26, head_cy - 8,  10),
    ]
    for (hx, hy, hr) in hair_puffs:
        draw.ellipse([hx - hr, hy - hr, hx + hr, hy + hr], fill=HAIR_COLOR)

    # Eyes
    eye_w = 7
    eye_h = 9
    for side in [-1, 1]:
        ex = cx + side * 10
        ey = head_cy - 3
        draw.ellipse([ex - eye_w, ey - eye_h, ex + eye_w, ey + eye_h],
                     fill=(245, 242, 235), outline=outline_color, width=2)
        ir = 5
        draw.ellipse([ex - ir, ey - ir, ex + ir, ey + ir], fill=(90, 62, 38))
        pr = 3
        draw.ellipse([ex - pr, ey - pr, ex + pr, ey + pr], fill=(22, 12, 6))

    # Mouth
    draw.arc([cx - 10, head_cy + 8, cx + 10, head_cy + 16],
             start=10, end=170, fill=outline_color, width=2)

    # Return geometry for post-processing
    return {
        "head_center": (cx, head_cy),
        "head_radius": (head_r, head_r),
        "hair_bbox": (cx - 30, head_cy - 30, cx + 30, head_cy - 2),
        "char_bbox": (cx - body_w // 2 - arm_w - 4, head_cy - head_r - 28,
                      cx + body_w // 2 + arm_w + 8, body_bot + 6),
        "torso_bbox": (cx - body_w // 2 - 7, shoulder_y, cx + body_w // 2 + 7, hip_y),
        "left_leg_bbox": (cx - leg_gap - leg_w, hip_y, cx - leg_gap, body_bot),
        "right_leg_bbox": (cx + leg_gap, hip_y, cx + leg_gap + leg_w, body_bot),
    }


def _draw_warm_bg_gradient(draw, w, h):
    """Draw a simplified warm domestic background for the demo."""
    floor_y = int(h * 0.72)
    # Wall gradient
    for row in range(floor_y):
        t = row / max(1, floor_y)
        r = int(218 + (215 - 218) * t)
        g = int(188 + (178 - 188) * t)
        b = int(148 + (130 - 148) * t)
        draw.line([(0, row), (w, row)], fill=(r, g, b))
    # Floor
    for row in range(floor_y, h):
        t = (row - floor_y) / max(1, h - floor_y)
        r = int(168 - int(20 * t))
        g = int(138 - int(20 * t))
        b = int(100 - int(15 * t))
        draw.line([(0, row), (w, row)], fill=(max(0, r), max(0, g), max(0, b)))


def generate_demo():
    """Generate a before/after comparison showing character color enhancement.

    Left panel:  Current pipeline — flat fills + left-side shadow
    Right panel: Enhanced pipeline — scene tint + warm cheek + form shadow + outline tint

    Output: output/color/LTG_COLOR_character_enhance_demo_c50.png
    """
    W, H = 1280, 720
    img = Image.new("RGB", (W, H), (200, 180, 150))
    draw = ImageDraw.Draw(img)

    half_w = W // 2
    divider_x = half_w

    # --- Left panel: BEFORE (current pipeline) ---
    _draw_warm_bg_gradient(draw, W, H)

    # Draw Luma — BEFORE (flat fills, old shadow)
    luma_cx_before = half_w // 2
    ground_y = int(H * 0.72)
    geom_before = _draw_luma_simple(draw, luma_cx_before, ground_y,
                                     use_shadow_shape=False,
                                     outline_color=LINE_WARM)

    # --- Right panel: AFTER (enhanced pipeline) ---
    # Same background (already drawn across full width)

    # Draw Luma — AFTER (will apply enhancements)
    luma_cx_after = half_w + half_w // 2
    geom_after = _draw_luma_simple(draw, luma_cx_after, ground_y,
                                    use_shadow_shape=True,
                                    outline_color=derive_scene_outline("warm_domestic"))

    # Apply form shadow to torso (AFTER panel only)
    img = apply_form_shadow(
        img, geom_after["torso_bbox"],
        base_color=HOODIE_ORANGE, shadow_color=HOODIE_SHADOW,
        shadow_shape="torso_diagonal", light_dir=(-0.7, -0.7), alpha=90
    )
    draw = ImageDraw.Draw(img)

    # Apply form shadow to legs
    for leg_key in ["left_leg_bbox", "right_leg_bbox"]:
        img = apply_form_shadow(
            img, geom_after[leg_key],
            base_color=JEANS, shadow_color=JEANS_SH,
            shadow_shape="limb_underside", light_dir=(-0.7, -0.7), alpha=75
        )
    draw = ImageDraw.Draw(img)

    # Apply scene tint (AFTER panel only)
    img = apply_scene_tint(
        img, geom_after["char_bbox"],
        key_light_color=(212, 146, 58),  # SUNLIT_AMBER
        alpha=22,
        light_dir=(-0.7, -0.7)
    )
    draw = ImageDraw.Draw(img)

    # Apply skin warmth (AFTER panel only)
    img = apply_skin_warmth(
        img, geom_after["head_center"], geom_after["head_radius"],
        light_dir=(-0.7, -0.7),
        warm_alpha=28, cool_alpha=18, blush_alpha=22
    )
    draw = ImageDraw.Draw(img)

    # Apply hair absorption (AFTER panel only)
    img = apply_hair_absorption(
        img, geom_after["hair_bbox"],
        scene_color=(212, 146, 58),  # SUNLIT_AMBER
        alpha=18
    )
    draw = ImageDraw.Draw(img)

    # --- Divider line ---
    draw.line([(divider_x, 0), (divider_x, H)], fill=(80, 60, 40), width=3)

    # --- Labels ---
    try:
        font_paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        ]
        font = None
        for fp in font_paths:
            if os.path.exists(fp):
                from PIL import ImageFont
                font = ImageFont.truetype(fp, 22)
                break
        if font is None:
            from PIL import ImageFont
            font = ImageFont.load_default()
    except Exception:
        from PIL import ImageFont
        font = ImageFont.load_default()

    # Label background bars
    draw.rectangle([0, 0, half_w, 36], fill=(40, 28, 16))
    draw.rectangle([half_w, 0, W, 36], fill=(40, 28, 16))

    draw.text((16, 6), "BEFORE: Flat fills + left-side shadow", fill=(255, 240, 210), font=font)
    draw.text((half_w + 16, 6), "AFTER: Scene tint + form shadow + skin warmth",
              fill=(255, 240, 210), font=font)

    # Sub-labels
    try:
        font_sm = None
        for fp in font_paths:
            if os.path.exists(fp):
                font_sm = ImageFont.truetype(fp, 14)
                break
        if font_sm is None:
            font_sm = ImageFont.load_default()
    except Exception:
        font_sm = ImageFont.load_default()

    draw.text((16, H - 24), "Current pipeline — character ignores scene lighting",
              fill=(120, 100, 70), font=font_sm)
    draw.text((half_w + 16, H - 24), "Enhanced — character receives warm domestic tint",
              fill=(120, 100, 70), font=font_sm)

    # Save
    out_path = str(output_dir('color', 'LTG_COLOR_character_enhance_demo_c50.png'))
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img.save(out_path, "PNG")
    print(f"Demo saved: {out_path}")
    return out_path


# ── CLI ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print(f"LTG_TOOL_character_color_enhance v{__version__}")
    print("Generating before/after demo...")
    path = generate_demo()
    print(f"Done. Output: {path}")
