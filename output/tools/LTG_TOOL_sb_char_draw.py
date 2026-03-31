#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_sb_char_draw.py — Shared Storyboard Character Drawing Module
"Luma & the Glitchkin" — Diego Vargas, Storyboard Artist — Cycle 53

Delegates character rendering to canonical char_*.py modules
(LTG_TOOL_char_luma, LTG_TOOL_char_byte, etc.). All 11 panel scripts that
import from this module get the canonical characters automatically.

Characters:
  - draw_luma_sb()   — Luma at storyboard scale via LTG_TOOL_char_luma
  - draw_byte_sb()   — Byte at storyboard scale via LTG_TOOL_char_byte
  - draw_chip()      — Falling pixel chip prop (inline — not a character)

Import pattern:
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
    from LTG_TOOL_sb_char_draw import draw_luma_sb, draw_byte_sb, draw_chip

Dependencies: pycairo, numpy, PIL/Pillow, LTG_TOOL_cairo_primitives,
              LTG_TOOL_char_luma, LTG_TOOL_char_byte.
"""

__version__ = "2.0.0"

import math
import os
import sys

# Ensure sibling tool imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import cairo
import numpy as np
from PIL import Image

from LTG_TOOL_cairo_primitives import (
    create_surface, draw_bezier_path, draw_tapered_stroke,
    draw_gradient_fill, draw_wobble_path, draw_smooth_polygon,
    draw_ellipse, to_pil_image, to_pil_rgba, set_color,
    stroke_path, fill_background, flatten_path,
    LINE_WEIGHT_ANCHOR, LINE_WEIGHT_STRUCTURE, LINE_WEIGHT_DETAIL,
    shoulder_offset,
)

# ── Canonical character renderers ────────────────────────────────────────────
from LTG_TOOL_char_luma import draw_luma as _canonical_draw_luma
from LTG_TOOL_char_byte import draw_byte as _canonical_draw_byte


# ══════════════════════════════════════════════════════════════════════════════
# Palette constants (kept for draw_chip and any direct callers)
# ══════════════════════════════════════════════════════════════════════════════

LUMA_HOODIE   = (232, 112, 58)
LUMA_SKIN     = (218, 172, 128)
LUMA_SKIN_SH  = (175, 128, 88)
LUMA_HAIR     = (38, 22, 14)
LUMA_HAIR_HL  = (61, 31, 15)
LUMA_PANTS    = (70, 80, 110)
LUMA_SHOE     = (42, 36, 30)
LINE_COLOR    = (59, 40, 32)
LINE_THIN     = (80, 55, 40)

BYTE_TEAL     = (0, 212, 232)
BYTE_DARK     = (8, 40, 50)
BYTE_SCAR     = (232, 0, 152)
ELEC_CYAN     = (0, 212, 232)
HOT_MAGENTA   = (232, 0, 152)
VOID_BLACK    = (10, 10, 20)
DEEP_CYAN     = (0, 155, 175)

COLLAR_COLOR  = (250, 232, 200)
IRIS_BROWN    = (130, 78, 40)


# ══════════════════════════════════════════════════════════════════════════════
# Expression mapping: storyboard names → canonical renderer names
# ══════════════════════════════════════════════════════════════════════════════

_LUMA_EXPR_MAP = {
    "assessing":  "CURIOUS",
    "alarmed":    "WORRIED",
    "happy":      "DELIGHTED",
    "neutral":    "CURIOUS",       # closest neutral-ish expression
    "curious":    "CURIOUS",
    "determined": "DETERMINED",
    "worried":    "WORRIED",
    "surprised":  "SURPRISED",
    "frustrated": "FRUSTRATED",
}

_BYTE_EXPR_MAP = {
    "still":     "neutral",
    "grumpy":    "grumpy",
    "alarmed":   "alarmed",
    "spotted":   "searching",
    "offended":  "resigned",
    "neutral":   "neutral",
    "searching": "searching",
    "confused":  "confused",
}


# ══════════════════════════════════════════════════════════════════════════════
# Internal helper: paint a PIL RGBA image onto a cairo context
# ══════════════════════════════════════════════════════════════════════════════

def _pil_to_cairo_surface(pil_img):
    """Convert a PIL RGBA image to a cairo ImageSurface (ARGB32).

    Args:
        pil_img: PIL.Image in RGBA mode

    Returns:
        cairo.ImageSurface (FORMAT_ARGB32)
    """
    if pil_img.mode != "RGBA":
        pil_img = pil_img.convert("RGBA")
    w, h = pil_img.size
    arr = np.array(pil_img, dtype=np.uint8)
    # PIL RGBA → cairo BGRA (little-endian ARGB32)
    bgra = np.empty_like(arr)
    bgra[:, :, 0] = arr[:, :, 2]  # B
    bgra[:, :, 1] = arr[:, :, 1]  # G
    bgra[:, :, 2] = arr[:, :, 0]  # R
    bgra[:, :, 3] = arr[:, :, 3]  # A
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    buf = np.frombuffer(surface.get_data(), dtype=np.uint8).reshape(h, w, 4)
    np.copyto(buf, bgra)
    surface.mark_dirty()
    return surface


def _render_canonical_char(draw_fn, expression, scale, facing, char_target_h):
    """Render a character via its canonical draw_X() function and return a
    cropped, resized PIL RGBA image ready for storyboard compositing.

    Args:
        draw_fn:        canonical draw function (e.g. draw_luma)
        expression:     expression string (already mapped to canonical name)
        scale:          canonical renderer scale param (controls internal detail)
        facing:         "left" or "right"
        char_target_h:  desired character height in storyboard pixels

    Returns:
        PIL.Image (RGBA), cropped to content and scaled to char_target_h
    """
    # Render at a scale that gives good detail for the target size.
    # Canonical renderers produce ~400px character at scale=1.0.
    # We render at scale=1.0 and then resize to target, ensuring quality.
    surface = draw_fn(expression=expression, scale=1.0, facing=facing,
                      scene_lighting=None)
    pil_img = to_pil_rgba(surface)

    # Crop to content bounding box
    bbox = pil_img.getbbox()
    if bbox:
        pil_img = pil_img.crop(bbox)

    # Resize to target storyboard height, preserving aspect ratio
    if pil_img.height > 0:
        aspect = pil_img.width / pil_img.height
        new_h = max(1, int(char_target_h))
        new_w = max(1, int(new_h * aspect))
        pil_img = pil_img.resize((new_w, new_h), Image.LANCZOS)

    return pil_img


def _composite_pil_onto_ctx(ctx, pil_img, dest_cx, dest_bottom_y):
    """Composite a PIL RGBA image onto a cairo context, centered at dest_cx
    with the bottom edge at dest_bottom_y.

    Args:
        ctx:            cairo.Context to draw on
        pil_img:        PIL.Image (RGBA) — character image
        dest_cx:        horizontal center in canvas coords
        dest_bottom_y:  y-coordinate where bottom of image should sit
    """
    w, h = pil_img.size
    x = dest_cx - w // 2
    y = dest_bottom_y - h

    char_surface = _pil_to_cairo_surface(pil_img)
    ctx.save()
    ctx.set_source_surface(char_surface, x, y)
    ctx.paint()
    ctx.restore()

    return x, y, w, h


# ══════════════════════════════════════════════════════════════════════════════
# LUMA — Storyboard scale drawing (delegates to canonical renderer)
# ══════════════════════════════════════════════════════════════════════════════

def draw_luma_sb(ctx, cx, floor_y, char_h=140, pose="sitting", lean_deg=3.0,
                 expression="assessing", facing="right", seed=1717):
    """Draw Luma at storyboard scale using the canonical Luma renderer.

    Args:
        ctx:        cairo Context to draw on
        cx:         horizontal center of character
        floor_y:    y-coordinate of the floor/ground line
        char_h:     visible character height in pixels (50-200)
        pose:       "sitting" or "standing" (pose hint — canonical renderer
                    uses its own gesture system)
        lean_deg:   gesture lean in degrees (applied as facing bias)
        expression: "assessing", "alarmed", "happy", "neutral", etc.
        facing:     "right" or "left" — which direction Luma faces
        seed:       RNG seed (unused — canonical renderer handles its own)

    Returns:
        dict with key positions: {head_cx, head_cy, head_r, shoulder_y}
    """
    # Map storyboard expression to canonical expression
    canonical_expr = _LUMA_EXPR_MAP.get(expression, "CURIOUS")

    # Map facing
    canon_facing = "left" if facing == "left" else "right"

    # Render via canonical renderer and composite
    pil_img = _render_canonical_char(
        _canonical_draw_luma, canonical_expr, 1.0, canon_facing, char_h
    )

    img_x, img_y, img_w, img_h = _composite_pil_onto_ctx(
        ctx, pil_img, cx, floor_y
    )

    # Estimate key positions for callers that use them
    head_r = int(char_h * 0.37) // 2
    head_cx = cx
    head_cy = floor_y - int(char_h * 0.74)  # head center ~ 74% up
    shoulder_y = floor_y - int(char_h * 0.61)

    return {
        "head_cx": head_cx,
        "head_cy": head_cy,
        "head_r": head_r,
        "shoulder_y": shoulder_y,
    }


# ══════════════════════════════════════════════════════════════════════════════
# BYTE — Storyboard scale drawing (delegates to canonical renderer)
# ══════════════════════════════════════════════════════════════════════════════

def draw_byte_sb(ctx, cx, cy, body_h=75, expression="still", facing="left",
                 lean_deg=0.0, hovering=True, seed=1718):
    """Draw Byte at storyboard scale using the canonical Byte renderer.

    Args:
        ctx:        cairo Context to draw on
        cx:         horizontal center of character
        cy:         vertical center of character body
        body_h:     total body height in pixels
        expression: "still", "grumpy", "alarmed", "spotted", "offended", etc.
        facing:     "left" or "right"
        lean_deg:   forward lean in degrees (compositing offset)
        hovering:   if True, no ground contact (visual hint only)
        seed:       RNG seed (unused — canonical renderer handles its own)

    Returns:
        dict with key positions: {face_cx, face_cy, face_r, body_cx}
    """
    # Map storyboard expression to canonical expression
    canonical_expr = _BYTE_EXPR_MAP.get(expression, "neutral")

    # Map facing
    canon_facing = "left" if facing == "left" else "right"

    # Render via canonical renderer and composite
    pil_img = _render_canonical_char(
        _canonical_draw_byte, canonical_expr, 1.0, canon_facing, body_h
    )

    # Apply lean offset
    face_dir = -1 if facing == "left" else 1
    lean_dx = int(body_h * 0.03 * lean_deg) * face_dir

    # Byte is centered at cy (not floor-anchored), so bottom = cy + body_h/2
    img_x, img_y, img_w, img_h = _composite_pil_onto_ctx(
        ctx, pil_img, cx + lean_dx, cy + body_h // 2
    )

    # Estimate key positions for callers
    body_cx = cx + lean_dx
    body_w = int(body_h * 0.72)
    face_cx = body_cx + int(body_w * 0.08) * face_dir
    face_cy = cy - int(body_h * 0.25)
    face_r = int(body_w * 0.45)

    return {
        "face_cx": face_cx,
        "face_cy": face_cy,
        "face_r": face_r,
        "body_cx": body_cx,
    }


# ══════════════════════════════════════════════════════════════════════════════
# Props (inline — not characters, no canonical module needed)
# ══════════════════════════════════════════════════════════════════════════════

def draw_chip(ctx, x, y, size=7, trail_len=40, trail_step=6):
    """Draw a falling pixel chip with dotted descent trail.

    Args:
        ctx:        cairo Context
        x, y:       center of chip
        size:       half-size of chip square
        trail_len:  length of dotted trail above chip
        trail_step: spacing between trail dots
    """
    # Chip body
    ctx.new_path()
    ctx.rectangle(x - size, y - size, size * 2, size * 2)
    set_color(ctx, ELEC_CYAN)
    ctx.fill()

    # Inner border
    ctx.new_path()
    ctx.rectangle(x - size + 1, y - size + 1, size * 2 - 2, size * 2 - 2)
    set_color(ctx, VOID_BLACK)
    ctx.set_line_width(1)
    ctx.stroke()

    # Dotted descent trail
    for dy in range(0, trail_len, trail_step):
        ctx.new_path()
        ctx.rectangle(x - 0.5, y - size - 4 - dy - 0.5, 1, 1)
        set_color(ctx, (0, 100, 120))
        ctx.fill()


# ══════════════════════════════════════════════════════════════════════════════
# Self-test
# ══════════════════════════════════════════════════════════════════════════════

def _self_test():
    """Generate a test image showing both characters via canonical renderers."""
    import time

    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
    PROD_DIR = os.path.join(PROJECT_ROOT, "output", "production")
    os.makedirs(PROD_DIR, exist_ok=True)

    W, H = 800, 400
    surface, ctx, _, _ = create_surface(W, H)
    t0 = time.time()

    # BG
    fill_background(ctx, W, H, (32, 28, 24))

    # Floor line
    floor_y = 340
    ctx.new_path()
    ctx.move_to(0, floor_y)
    ctx.line_to(W, floor_y)
    set_color(ctx, (80, 70, 60))
    ctx.set_line_width(1)
    ctx.stroke()

    # Luma sitting
    luma_info = draw_luma_sb(ctx, 200, floor_y, char_h=140, pose="sitting",
                              lean_deg=3.0, expression="assessing", facing="right")

    # Luma standing
    draw_luma_sb(ctx, 500, floor_y, char_h=160, pose="standing",
                 lean_deg=2.0, expression="neutral", facing="left")

    # Byte
    byte_info = draw_byte_sb(ctx, 650, 280, body_h=75, expression="still",
                              facing="left", lean_deg=2.0)

    # Chip
    draw_chip(ctx, 400, 280)

    elapsed = time.time() - t0

    # Label
    ctx.select_font_face("monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(12)
    set_color(ctx, (200, 200, 200))
    ctx.move_to(10, H - 10)
    ctx.show_text(f"LTG_TOOL_sb_char_draw v{__version__} self-test  |  {elapsed*1000:.1f}ms")

    img = to_pil_image(surface)
    if img.width > 1280 or img.height > 1280:
        img.thumbnail((1280, 1280), Image.LANCZOS)

    out_path = os.path.join(PROD_DIR, "LTG_RENDER_sb_char_draw_selftest_c53.png")
    img.save(out_path)
    print(f"Self-test saved: {out_path}")
    print(f"  Size: {img.size[0]}x{img.size[1]}")
    print(f"  Render time: {elapsed*1000:.1f}ms")


if __name__ == "__main__":
    _self_test()
