#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_character_lineup.py
Character Lineup Generator — Luma & the Glitchkin
Cycle 52 / v012: pycairo rebuild for Luma, Byte, Cosmo (Alex Chen C52).

v012 changes (C52 — Alex Chen, Art Director):
  Luma, Byte, Cosmo rebuilt with pycairo bezier curves and native AA.
  Each character renders on a separate cairo surface at 2x, then composites
  to the PIL canvas via RGBA alpha composite. Miri and Glitch remain PIL
  (Miri pycairo rebuild pending; Glitch is non-humanoid/low-priority).
  All layout geometry, two-tier staging, depth temperature, annotations
  preserved from v011.

  pycairo characters: smooth silhouettes, organic curves, variable-width
  outlines, gradient fills. Quality matches C52 expression sheets.

Prior history (compressed):
  v011 (C47): Cosmo visual hook (cowlick + bridge tape).
  v010 (C45): Two-tier depth bands (Option C, Lee Tanaka).
  v009 (C44): Miri wooden hairpin rename.
  v008 (C42): Two-tier ground plane staging (FG/BG tiers).
  v007 (C33): BYTE_SH / MIRI_SLIPPER color fixes.
  v006 (C29): Luma 3.2 heads, canonical eye width.
  v005 (C27): Luma v006 canonical style.
  v004-v001: Glitch added, dimension arrows, ground annotations, initial.

Output: /home/wipkat/team/output/characters/main/LTG_CHAR_character_lineup.png
Usage: python3 LTG_TOOL_character_lineup.py
"""
import sys
import os

_TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
if _TOOLS_DIR not in sys.path:
    sys.path.insert(0, _TOOLS_DIR)

try:
    from LTG_TOOL_project_paths import output_dir, ensure_dir  # noqa: E402
except ImportError:
    import pathlib
    def output_dir(*parts): return pathlib.Path("/home/wipkat/team/output").joinpath(*parts)
    def ensure_dir(path): path.mkdir(parents=True, exist_ok=True); return path
from PIL import Image, ImageDraw, ImageFont
import math

# ── pycairo imports for character rendering ──────────────────────────────────
import cairo
import numpy as np
from LTG_TOOL_cairo_primitives import (
    create_surface, draw_bezier_path, draw_smooth_polygon,
    draw_ellipse as cairo_ellipse, draw_tapered_stroke,
    to_pil_rgba, set_color, _c, _ca,
    stroke_path, fill_background,
    LINE_WEIGHT_ANCHOR, LINE_WEIGHT_STRUCTURE, LINE_WEIGHT_DETAIL,
)
from LTG_TOOL_curve_utils import quadratic_bezier_pts as _cu_quadratic, polyline as _cu_polyline

# ── Canvas ────────────────────────────────────────────────────────────────────
BG           = (250, 248, 244)
PANEL_BG     = (245, 241, 235)
LINE_COL     = (59, 40, 32)       # #3B2820 Deep Cocoa
LABEL_COL    = (50, 40, 35)
TICK_COL     = (160, 148, 138)
BASELINE_COL = (180, 165, 150)

# ── Height system ─────────────────────────────────────────────────────────────
LUMA_RENDER_H = 280
LUMA_HEADS    = 3.2   # v006 FIX: was 3.5, canonical is 3.2 (C28 directive)
HEAD_UNIT     = LUMA_RENDER_H / LUMA_HEADS   # ~87.5px

COSMO_HEADS   = 4.0
COSMO_H       = int(COSMO_HEADS * HEAD_UNIT)  # ~320px

MIRI_HEADS    = 3.2
MIRI_H        = int(MIRI_HEADS * HEAD_UNIT)   # ~256px

BYTE_H        = int(LUMA_RENDER_H * 0.58)     # ~162px

# Glitch: floating antagonist, slightly taller than Byte
GLITCH_H      = int(BYTE_H * 1.05)            # ~170px

# ── Layout ────────────────────────────────────────────────────────────────────
CHAR_SPACING  = 240     # tighter spacing to fit 5 characters
LEFT_MARGIN   = 100
N_CHARS       = 5
IMG_W         = LEFT_MARGIN * 2 + CHAR_SPACING * (N_CHARS - 1) + 180
TITLE_H       = 50
LABEL_AREA    = 90     # slightly taller for tier annotation
IMG_H         = 560    # bumped for two-tier geometry (was computed from HEADROOM)

# ── Two-tier ground planes (v008) ─────────────────────────────────────────────
# FG tier: Luma + Byte — visually closest to camera
# BG tier: Cosmo + Miri + Glitch — one step behind
FG_GROUND_Y  = int(IMG_H * 0.78)   # ~436 — FG chars stand here
BG_GROUND_Y  = int(IMG_H * 0.70)   # ~392 — BG chars stand here

# Legacy alias: BASELINE_Y used by existing height-marker + annotation helpers
# Points to FG tier (the reference tier for head-unit comparisons)
BASELINE_Y   = FG_GROUND_Y

# ── FG scale factor (post-calculation, proportion constants unchanged) ────────
FG_SCALE     = 1.03   # +3% height for FG characters (Luma + Byte)
BG_SCALE     = 1.00   # baseline for BG characters

# Scaled render heights (used for drawing and labels)
LUMA_RENDER_H_FG  = int(LUMA_RENDER_H * FG_SCALE)   # ~288px
BYTE_H_FG         = int(BYTE_H * FG_SCALE)           # ~167px
GLITCH_H_BG       = GLITCH_H                          # unscaled

# ── Character order: left → right ────────────────────────────────────────────
# Cosmo (left bookend) | Miri | Luma (center protagonist) | Byte | Glitch (right)
CHAR_ORDER    = ["cosmo", "miri", "luma", "byte", "glitch"]
CHAR_X        = {
    "cosmo":  LEFT_MARGIN + 60,
    "miri":   LEFT_MARGIN + 60 + CHAR_SPACING,
    "luma":   LEFT_MARGIN + 60 + CHAR_SPACING * 2,
    "byte":   LEFT_MARGIN + 60 + CHAR_SPACING * 3 - 20,
    "glitch": LEFT_MARGIN + 60 + CHAR_SPACING * 4,
}

# Ground Y per character (FG or BG tier)
CHAR_GROUND_Y = {
    "luma":   FG_GROUND_Y,
    "byte":   FG_GROUND_Y,
    "cosmo":  BG_GROUND_Y,
    "miri":   BG_GROUND_Y,
    "glitch": BG_GROUND_Y,
}

# Draw heights (FG chars use scaled height)
CHAR_HEIGHTS  = {
    "luma":   LUMA_RENDER_H_FG,
    "byte":   BYTE_H_FG,
    "cosmo":  COSMO_H,
    "miri":   MIRI_H,
    "glitch": GLITCH_H_BG,
}
CHAR_LABELS   = {
    "luma":   f"LUMA [FG]\n3.2 heads / {LUMA_RENDER_H}px (+3%)",
    "byte":   f"BYTE [FG]\n~Luma chest / {BYTE_H}px (+3%)",
    "cosmo":  f"COSMO [BG]\n4.0 heads / {COSMO_H}px",
    "miri":   f"MIRI [BG]\n3.2 heads / {MIRI_H}px",
    "glitch": f"GLITCH [BG]\n~Byte scale / {GLITCH_H}px",
}

# ── Colors ────────────────────────────────────────────────────────────────────
# Luma — canonical palette (matches expression sheet v006 and classroom pose)
LUMA_SKIN      = (200, 136, 90)    # matches v006 SKIN
LUMA_SKIN_SH   = (160, 104, 64)    # shadow
LUMA_HAIR      = (26, 15, 10)      # matches v006 HAIR
LUMA_HAIR_HL   = (61, 31, 15)      # hair highlight
LUMA_EYE_W     = (250, 240, 220)   # matches v006 EYE_W
LUMA_EYE_IRIS  = (200, 125, 62)    # matches v006 EYE_IRIS
LUMA_EYE_PUP   = (59, 40, 32)      # matches v006 EYE_PUP
LUMA_EYE_HL    = (240, 240, 240)
LUMA_HOODIE    = (232, 114, 42)
LUMA_PANTS     = (42, 40, 80)
LUMA_SHOE_UP   = (245, 232, 208)
LUMA_SHOE_SOLE = (199, 91, 57)
PX_CYAN        = (0, 240, 255)
PX_MAG         = (255, 45, 107)

# Byte
BYTE_TEAL     = (0, 212, 232)
BYTE_HL       = (0, 240, 255)
BYTE_SH       = (0, 168, 180)  # C33 FIX: was (0, 144, 176) wrong; canonical Deep Cyan GL-01a #00A8B4
SCAR_MAG      = (255, 45, 107)
BYTE_EYE_W   = (240, 240, 245)

# Cosmo
COSMO_SKIN     = (217, 192, 154)
COSMO_HAIR     = (26, 24, 36)
COSMO_JACKET   = (168, 155, 191)
COSMO_SHIRT_B  = (91, 141, 184)
COSMO_SHIRT_G  = (122, 158, 126)
COSMO_PANTS    = (140, 136, 128)
COSMO_FRAMES   = (92, 58, 32)
COSMO_LENS_BG  = (238, 244, 255)
COSMO_SHOE     = (92, 58, 32)
COSMO_NB       = (91, 141, 184)

# Miri
MIRI_SKIN      = (140, 84, 48)
MIRI_HAIR      = (216, 208, 200)
MIRI_CARDIGAN  = (184, 92, 56)
MIRI_PANTS     = (200, 174, 138)
MIRI_SLIPPER   = (196, 144, 122)  # C33 FIX: was (90, 122, 90) Deep Sage (cool green) violates warm palette guarantee; now #C4907A Dusty Warm Apricot per Sam C32 master_palette.md correction

# Glitch
GLITCH_AMB    = (255, 140,   0)   # CORRUPT_AMBER GL-07
GLITCH_AMB_SH = (168,  76,   0)   # CORRUPT_AMB_SHADOW
GLITCH_AMB_HL = (255, 185,  80)   # warm highlight
GLITCH_HOT    = (255,  45, 107)   # HOT_MAGENTA — crack/scar
GLITCH_UV     = (123,  47, 190)   # UV_PURPLE — shadow
GLITCH_GOLD   = (232, 201,  90)   # SOFT_GOLD — pixel eye glow
GLITCH_VB     = ( 10,  10,  20)   # VOID_BLACK — outline
GLITCH_ACID   = ( 57, 255,  20)   # ACID_GREEN — pixel alive state

NEG_SPACE = BG


# ── Geometry helpers — migrated to LTG_TOOL_curve_utils (C52) ────────────────

def _bezier3(p0, p1, p2, steps=20):
    """Delegates to curve_utils.quadratic_bezier_pts."""
    return _cu_quadratic(p0, p1, p2, steps=steps)


def _polyline(draw, pts, color, width=1):
    """Delegates to curve_utils.polyline."""
    _cu_polyline(draw, pts, color, width=width)


def _render_cairo_character(draw_fn, cx, base_y, h):
    """Render a character using pycairo and return PIL RGBA image.

    draw_fn(ctx, cx, base_y, h) draws the character on a cairo context.
    Returns a PIL RGBA image the size of the full canvas (IMG_W x IMG_H).
    """
    surface, ctx, aw, ah = create_surface(IMG_W, IMG_H, scale=2)
    draw_fn(ctx, cx, base_y, h)
    # Convert to PIL at 2x then downscale with LANCZOS for AA
    big = to_pil_rgba(surface)
    return big.resize((IMG_W, IMG_H), Image.LANCZOS)


# ── Cairo drawing helpers ────────────────────────────────────────────────────

def _cairo_filled_ellipse(ctx, cx, cy, rx, ry, fill, outline=None, lw=2.0):
    """Draw a filled ellipse with optional outline using cairo."""
    cairo_ellipse(ctx, cx, cy, rx, ry)
    set_color(ctx, fill)
    if outline:
        ctx.fill_preserve()
        set_color(ctx, outline)
        ctx.set_line_width(lw)
        ctx.stroke()
    else:
        ctx.fill()


def _cairo_filled_polygon(ctx, pts, fill, outline=None, lw=1.0):
    """Draw a filled polygon with optional outline using cairo."""
    if len(pts) < 2:
        return
    ctx.new_path()
    ctx.move_to(pts[0][0], pts[0][1])
    for p in pts[1:]:
        ctx.line_to(p[0], p[1])
    ctx.close_path()
    set_color(ctx, fill)
    if outline:
        ctx.fill_preserve()
        set_color(ctx, outline)
        ctx.set_line_width(lw)
        ctx.stroke()
    else:
        ctx.fill()


def _cairo_filled_rect(ctx, x0, y0, x1, y1, fill, outline=None, lw=1.0):
    """Draw a filled rectangle with optional outline using cairo."""
    ctx.new_path()
    ctx.rectangle(x0, y0, x1 - x0, y1 - y0)
    set_color(ctx, fill)
    if outline:
        ctx.fill_preserve()
        set_color(ctx, outline)
        ctx.set_line_width(lw)
        ctx.stroke()
    else:
        ctx.fill()


def _cairo_arc(ctx, cx, cy, rx, ry, start_deg, end_deg, color, lw=2.0):
    """Draw an arc stroke using cairo (angles in degrees, clockwise like PIL)."""
    ctx.save()
    ctx.translate(cx, cy)
    if rx != 0 and ry != 0:
        ctx.scale(rx, ry)
    ctx.new_path()
    ctx.arc(0, 0, 1.0, math.radians(start_deg), math.radians(end_deg))
    ctx.restore()
    set_color(ctx, color)
    ctx.set_line_width(lw)
    ctx.stroke()


def _cairo_line(ctx, pts, color, lw=1.0):
    """Draw a polyline using cairo."""
    if len(pts) < 2:
        return
    ctx.new_path()
    ctx.move_to(pts[0][0], pts[0][1])
    for p in pts[1:]:
        ctx.line_to(p[0], p[1])
    set_color(ctx, color)
    ctx.set_line_width(lw)
    ctx.stroke()


def _cairo_bezier3(p0, p1, p2, steps=20):
    """Quadratic bezier sampling for cairo polylines."""
    pts = []
    for i in range(steps + 1):
        t  = i / steps
        x  = (1-t)**2 * p0[0] + 2*(1-t)*t * p1[0] + t**2 * p2[0]
        y  = (1-t)**2 * p0[1] + 2*(1-t)*t * p1[1] + t**2 * p2[1]
        pts.append((x, y))
    return pts


# ══════════════════════════════════════════════════════════════════════════════
# LUMA — v012 pycairo rebuild (canonical 3.2 heads, bezier curves, native AA)
# ══════════════════════════════════════════════════════════════════════════════

def _draw_luma_cairo(ctx, cx, base_y, h):
    """Luma full body at lineup height h, pycairo v012. 3.2 heads canonical.
    Bezier curves for all organic forms. Native AA via cairo."""
    hu = h / 3.2
    r  = int(hu * 0.46)
    s  = r / 100.0
    hy = base_y - h

    head_cy = hy + int(hu * 0.46) + int(r * 0.5)

    # ── HAIR — overlapping ellipses (curl cloud) ─────────────────────────────
    v_off = 0
    hair_ellipses = [
        (-int(s*155), -int(s*195)+v_off, int(s*145), int(s*40)),
        (-int(s*175), -int(s*170)+v_off, -int(s*80), -int(s*60)),
        (-int(s*165), -int(s*140)+v_off, -int(s*95), -int(s*30)),
        ( int(s*80),  -int(s*160)+v_off,  int(s*155), -int(s*60)),
        ( int(s*90),  -int(s*130)+v_off,  int(s*145), -int(s*40)),
        (-int(s*60),  -int(s*215)+v_off,  int(s*20),  -int(s*140)),
        (-int(s*20),  -int(s*225)+v_off,  int(s*70),  -int(s*145)),
        (-int(s*100), -int(s*200)+v_off, -int(s*30),  -int(s*130)),
    ]
    for (x1, y1, x2, y2) in hair_ellipses:
        ecx = cx + (x1 + x2) / 2.0
        ecy = head_cy + (y1 + y2) / 2.0
        erx = abs(x2 - x1) / 2.0
        ery = abs(y2 - y1) / 2.0
        _cairo_filled_ellipse(ctx, ecx, ecy, erx, ery, LUMA_HAIR)

    # Foreground strand arcs
    _cairo_arc(ctx, cx - int(s*35), head_cy - int(s*167.5) + v_off,
               int(s*25), int(s*27.5), 0.52, 3.49, LUMA_HAIR, 1.0)
    _cairo_arc(ctx, cx + int(s*10), head_cy - int(s*160) + v_off,
               int(s*30), int(s*30), 0.17, 3.32, LUMA_HAIR, 1.0)

    # ── HEAD — ellipse + chin fill + cheek nubs ──────────────────────────────
    _cairo_filled_ellipse(ctx, cx, head_cy + int(r * 0.075), r, r + int(r * 0.075),
                          LUMA_SKIN, LINE_COL, 2.0)

    # Chin fill (softens jaw)
    chin_rx = int(r * 0.95)
    _cairo_filled_ellipse(ctx, cx, head_cy + r * 0.025 + int(r * 0.025),
                          chin_rx, int(r * 0.225) + r, LUMA_SKIN)
    _cairo_arc(ctx, cx, head_cy + r * 0.025 + int(r * 0.025),
               chin_rx, int(r * 0.225) + r, 0, math.pi, LINE_COL, 1.0)

    # Cheek nubs
    nub_w = int(r * 0.18)
    nub_h = int(r * 0.24)
    nub_y = head_cy - int(r * 0.12)
    _cairo_filled_ellipse(ctx, cx - r + int(r * 0.06), nub_y, nub_w, nub_h // 2,
                          LUMA_SKIN, LINE_COL, 1.0)
    _cairo_filled_ellipse(ctx, cx + r - int(r * 0.06), nub_y, nub_w, nub_h // 2,
                          LUMA_SKIN, LINE_COL, 1.0)

    # ── EYES ─────────────────────────────────────────────────────────────────
    eye_y = head_cy - int(s * 18)
    lex   = cx - int(s * 38)
    rex   = cx + int(s * 38)
    ew    = int(r * 0.22)
    leh   = int(r * 0.27)
    reh   = int(r * 0.22)

    for (ex, eh) in [(lex, leh), (rex, reh)]:
        _cairo_filled_ellipse(ctx, ex, eye_y, ew, eh, LUMA_EYE_W, LINE_COL, 1.0)
        # Iris
        iris_r = int(ew * 0.54)
        iry    = max(2, min(iris_r, eh - 1))
        _cairo_filled_ellipse(ctx, ex, eye_y, iris_r, iry, LUMA_EYE_IRIS)
        # Pupil
        pr = int(iris_r * 0.50)
        if pr >= 1:
            _cairo_filled_ellipse(ctx, ex, eye_y, pr, pr, LUMA_EYE_PUP)
        # Highlight
        hl_s = max(1, int(pr * 0.38))
        hl_x = ex + int(iris_r * 0.42)
        hl_y = eye_y - int(iry * 0.48)
        _cairo_filled_ellipse(ctx, hl_x, hl_y, hl_s, hl_s, LUMA_EYE_HL)
        # Eyelid arc
        _cairo_arc(ctx, ex, eye_y, ew, eh, 3.49, 5.93, LINE_COL, 1.0)

    # Brows
    brow_y = eye_y - int(leh * 1.35)
    for (bx, sign) in [(lex, -1), (rex, 1)]:
        bx0 = bx + sign * int(s * 22)
        bx1 = bx - sign * int(s * 26)
        _cairo_line(ctx, [(bx1, brow_y + int(s * 2)), (bx, brow_y - int(s * 6)),
                          (bx0, brow_y + int(s * 2))], LUMA_HAIR, 1.0)

    # Nose — nostril dots
    _cairo_filled_ellipse(ctx, cx - int(s*5), head_cy + int(s*11), int(s*3), int(s*3),
                          LUMA_SKIN_SH)
    _cairo_filled_ellipse(ctx, cx + int(s*5), head_cy + int(s*11), int(s*3), int(s*3),
                          LUMA_SKIN_SH)

    # Mouth — bezier curve
    my = head_cy + int(s * 30)
    mw = int(s * 36)
    ctx.new_path()
    ctx.move_to(cx - mw, my + int(s*4))
    ctx.curve_to(cx - mw*0.3, my - int(s*8), cx + mw*0.3, my - int(s*8),
                 cx + mw, my + int(s*4))
    set_color(ctx, LINE_COL)
    ctx.set_line_width(1.0)
    ctx.stroke()

    # ── BODY — hoodie (smooth polygon for organic trapezoid) ─────────────────
    neck_top = head_cy + r + int(r * 0.25)
    sw  = int(hu * 0.38)
    hw2 = int(hu * 0.70)
    bt  = neck_top + int(hu * 0.08)
    bh  = int(hu * 2.0)
    bb  = bt + bh

    # Organic hoodie shape using smooth polygon
    body_pts = [(cx - sw, bt), (cx + sw, bt), (cx + hw2, bb), (cx - hw2, bb)]
    draw_smooth_polygon(ctx, body_pts, bulge_frac=0.04)
    set_color(ctx, LUMA_HOODIE)
    ctx.fill_preserve()
    set_color(ctx, LINE_COL)
    ctx.set_line_width(1.0)
    ctx.stroke()

    # Pocket / sleeve detail
    mid_frac = 0.55
    hem_mid  = cx + int(sw + (hw2 - sw) * mid_frac)
    py2 = bt + int(bh * 0.50)
    _cairo_filled_rect(ctx, hem_mid, py2, hem_mid + int(hu*0.30), py2 + int(hu*0.42),
                       LUMA_HOODIE, LINE_COL, 1.0)

    # Pixel accent on hoodie chest
    pix_y = bt + int(bh * 0.20)
    _cairo_filled_rect(ctx, cx - int(hu*0.14), pix_y, cx - int(hu*0.06), pix_y + int(hu*0.06),
                       PX_CYAN)
    _cairo_filled_rect(ctx, cx - int(hu*0.04), pix_y, cx + int(hu*0.04), pix_y + int(hu*0.06),
                       PX_MAG)
    _cairo_filled_rect(ctx, cx + int(hu*0.06), pix_y, cx + int(hu*0.14), pix_y + int(hu*0.06),
                       PX_CYAN)

    # ── LEGS ─────────────────────────────────────────────────────────────────
    lw = int(hu * 0.20)
    leg_h = int(hu * 0.55)
    _cairo_filled_rect(ctx, cx - lw*2, bb, cx - 4, bb + leg_h, LUMA_PANTS, LINE_COL, 1.0)
    _cairo_filled_rect(ctx, cx + 4, bb, cx + lw*2, bb + leg_h, LUMA_PANTS, LINE_COL, 1.0)

    # ── SHOES ────────────────────────────────────────────────────────────────
    fw = int(hu * 0.52)
    fh = int(hu * 0.28)
    sole_h = int(fh * 0.35)
    # Left shoe
    lsx = cx - lw*2 - fw + int(fw*0.3)
    lse = cx - lw*2 + int(fw*0.5)
    _cairo_filled_ellipse(ctx, (lsx + lse)/2, base_y - fh/2,
                          (lse - lsx)/2, fh/2, LUMA_SHOE_UP, LINE_COL, 1.0)
    # Right shoe
    rsx = cx + lw*2 - int(fw*0.5)
    rse = cx + lw*2 + fw - int(fw*0.3)
    _cairo_filled_ellipse(ctx, (rsx + rse)/2, base_y - fh/2,
                          (rse - rsx)/2, fh/2, LUMA_SHOE_UP, LINE_COL, 1.0)
    # Soles
    _cairo_filled_rect(ctx, lsx, base_y - sole_h, lse, base_y, LUMA_SHOE_SOLE)
    _cairo_filled_rect(ctx, rsx, base_y - sole_h, rse, base_y, LUMA_SHOE_SOLE)


def draw_luma_lineup(draw, cx, base_y, h):
    """Luma v012 — dispatches to cairo, composites to PIL image."""
    # This is a wrapper; actual drawing happens in generate_lineup via cairo
    pass  # Cairo drawing handled in generate_lineup


# ══════════════════════════════════════════════════════════════════════════════
# BYTE — v012 pycairo rebuild (smooth elliptical body, native AA)
# ══════════════════════════════════════════════════════════════════════════════

def _draw_byte_cairo(ctx, cx, base_y, h):
    """Byte full body at lineup height h, pycairo v012."""
    s         = h
    float_gap = int(s * 0.18)
    body_rx   = s // 2
    body_ry   = int(s * 0.55)
    bcy       = base_y - float_gap - body_ry

    # Body ellipse
    _cairo_filled_ellipse(ctx, cx, bcy, body_rx, body_ry, BYTE_TEAL, LINE_COL, 3.0)

    # Shadow side (half body)
    shadow_pts = [
        (cx,               bcy - body_ry),
        (cx + body_rx,     bcy - body_ry + 4),
        (cx + body_rx,     bcy + body_ry - 4),
        (cx,               bcy + body_ry),
        (cx + body_rx//2,  bcy + body_ry),
        (cx + body_rx,     bcy + body_ry//2),
        (cx + body_rx,     bcy),
    ]
    _cairo_filled_polygon(ctx, shadow_pts, BYTE_SH)

    # Highlight arc
    _cairo_arc(ctx, cx, bcy, body_rx, body_ry, 3.49, 5.41, BYTE_HL, 3.0)

    # Crack / scar (Hot Magenta) — bezier crack line
    crack_x = cx - s//4
    ctx.new_path()
    ctx.move_to(crack_x, bcy - body_ry//2)
    ctx.curve_to(crack_x + s//12, bcy - body_ry//4, crack_x + s//10, bcy - body_ry//8,
                 crack_x + s//8, bcy - body_ry//6)
    ctx.curve_to(crack_x + s//16, bcy, crack_x - s//14, bcy + body_ry//10,
                 crack_x - s//10, bcy + body_ry//6)
    set_color(ctx, SCAR_MAG)
    ctx.set_line_width(2.0)
    ctx.stroke()

    # Pixel grid eye (left)
    eye_y  = bcy - body_ry // 5
    eye_sz = s // 4
    lx     = cx - s//5
    cell   = max(1, eye_sz // 5)
    ox = lx - (5*cell)//2
    oy = eye_y - (5*cell)//2
    _cairo_filled_rect(ctx, ox-2, oy-2, ox+5*cell+2, oy+5*cell+2,
                       (255,255,255), LINE_COL, 1.0)
    for row in range(2):
        for col in range(2):
            px = lx + col * (cell*2 + 2) - cell*2
            py = eye_y + row * (cell*2 + 2)
            _cairo_filled_rect(ctx, px, py, px + cell*2, py + cell*2, (0, 240, 255))

    # Organic eye (right)
    rx = cx + s//5
    er = s // 10
    _cairo_filled_ellipse(ctx, rx, eye_y, er, er, BYTE_EYE_W, LINE_COL, 1.0)
    _cairo_filled_ellipse(ctx, rx, eye_y, er//2, er//2, (60, 38, 20))

    # Arms (rounded rectangles via smooth polygon)
    lw = s // 6
    lh = s // 5
    arm_y = bcy - body_ry // 5
    _cairo_filled_rect(ctx, cx - body_rx - lw, arm_y, cx - body_rx, arm_y + lh,
                       BYTE_TEAL, LINE_COL, 2.0)
    _cairo_filled_rect(ctx, cx + body_rx, arm_y, cx + body_rx + lw, arm_y + lh,
                       BYTE_TEAL, LINE_COL, 2.0)

    # Legs
    leg_offset = s // 4
    leg_h = lh
    leg_w = int(lw * 0.9)
    _cairo_filled_rect(ctx, cx - leg_offset - leg_w//2, bcy + body_ry,
                       cx - leg_offset + leg_w//2, bcy + body_ry + leg_h,
                       BYTE_TEAL, LINE_COL, 2.0)
    _cairo_filled_rect(ctx, cx + leg_offset - leg_w//2, bcy + body_ry,
                       cx + leg_offset + leg_w//2, bcy + body_ry + leg_h,
                       BYTE_TEAL, LINE_COL, 2.0)

    # Hover confetti (pixel particles)
    particle_y = bcy + body_ry + leg_h + 4
    for (px, pc) in [(cx - int(s*0.28), BYTE_HL), (cx - int(s*0.08), SCAR_MAG),
                     (cx + int(s*0.08), BYTE_HL), (cx + int(s*0.24), (0, 200, 180))]:
        py = particle_y + (abs(px - cx) % 8)
        _cairo_filled_rect(ctx, px, py, px + 10, py + 10, pc)


def draw_byte_lineup(draw, cx, base_y, h):
    """Byte v012 — dispatches to cairo, composites to PIL image."""
    pass  # Cairo drawing handled in generate_lineup


# ══════════════════════════════════════════════════════════════════════════════
# COSMO — v012 pycairo rebuild (4.0 heads, visual hooks, native AA)
# ══════════════════════════════════════════════════════════════════════════════

def _draw_cosmo_cairo(ctx, cx, base_y, h):
    """Cosmo full body at lineup height h, pycairo v012. 4.0 heads canonical."""
    hu = h / 4.0
    hy = base_y - h

    hw = int(hu * 0.40)
    hh = int(hu * 0.95)

    # Hair mass
    _cairo_filled_ellipse(ctx, cx, hy + int(hu*0.02), hw + 4, int(hu*0.10), COSMO_HAIR)
    _cairo_filled_ellipse(ctx, cx - int(hw*0.6), hy - int(hu*0.085),
                          int(hw*0.4), int(hu*0.135), COSMO_HAIR)

    # Cowlick (C47 visual hook) — bezier sproing
    cowlick_cx = cx + int(hw * 0.10)
    cowlick_base = hy - int(hu * 0.08)
    cowlick_tip = cowlick_base - int(hu * 0.15)
    cw = int(hu * 0.06)
    ctx.new_path()
    ctx.move_to(cowlick_cx - cw, cowlick_base)
    ctx.curve_to(cowlick_cx - cw*0.5, cowlick_tip + int(hu*0.02),
                 cowlick_cx + cw*0.5, cowlick_tip - int(hu*0.01),
                 cowlick_cx, cowlick_tip)
    ctx.curve_to(cowlick_cx + cw*0.3, cowlick_tip + int(hu*0.03),
                 cowlick_cx + cw*0.8, cowlick_base - int(hu*0.02),
                 cowlick_cx + cw, cowlick_base)
    ctx.close_path()
    set_color(ctx, COSMO_HAIR)
    ctx.fill_preserve()
    set_color(ctx, LINE_COL)
    ctx.set_line_width(max(1, int(hu * 0.02)))
    ctx.stroke()

    # Head (rounded rectangle via smooth polygon)
    head_pts = [
        (cx - hw, hy), (cx + hw, hy),
        (cx + hw, hy + hh), (cx - hw, hy + hh),
    ]
    draw_smooth_polygon(ctx, head_pts, bulge_frac=0.08)
    set_color(ctx, COSMO_SKIN)
    ctx.fill_preserve()
    set_color(ctx, LINE_COL)
    ctx.set_line_width(2.0)
    ctx.stroke()

    # Glasses frames + lenses
    gr  = int(hu * 0.18)
    gy  = hy + int(hh * 0.48)
    rim = 3
    lcx = cx - int(hu * 0.30)
    rcx = cx + int(hu * 0.30)
    # Frame rims
    _cairo_filled_ellipse(ctx, lcx, gy, gr + rim, gr + rim, COSMO_FRAMES, LINE_COL, 1.0)
    _cairo_filled_ellipse(ctx, rcx, gy, gr + rim, gr + rim, COSMO_FRAMES, LINE_COL, 1.0)
    # Lenses
    _cairo_filled_ellipse(ctx, lcx, gy, gr, gr, COSMO_LENS_BG)
    _cairo_filled_ellipse(ctx, rcx, gy, gr, gr, COSMO_LENS_BG)
    # Bridge
    _cairo_filled_rect(ctx, lcx + gr, gy - 2, rcx - gr, gy + 2, COSMO_FRAMES)
    # Bridge tape (C47 visual hook)
    tape_w = max(2, int(hu * 0.04))
    tape_h = max(2, int(hu * 0.03))
    _cairo_filled_rect(ctx, cx - tape_w, gy - tape_h, cx + tape_w, gy + tape_h,
                       (250, 240, 220), LINE_COL, 1.0)
    # Lens glints
    _cairo_arc(ctx, lcx, gy - gr*0.3, gr - 2, gr*0.5, 3.49, 5.93, (240,240,240), 2.0)
    _cairo_arc(ctx, rcx, gy - gr*0.3, gr - 2, gr*0.5, 3.49, 5.93, (240,240,240), 2.0)

    # Pupils
    ep = int(gr * 0.5)
    _cairo_filled_ellipse(ctx, lcx, gy, ep, ep, (61, 107, 69))
    _cairo_filled_ellipse(ctx, rcx, gy, ep, ep, (61, 107, 69))

    # Body (shirt + stripes)
    bw     = int(hu * 0.38)
    body_h = int(hu * 2.4)
    bt     = hy + hh
    bb     = bt + body_h
    _cairo_filled_rect(ctx, cx - bw, bt, cx + bw, bb, COSMO_SHIRT_B, LINE_COL, 2.0)

    stripe_h = int(hu * 0.15)
    sy = bt + int(body_h * 0.25)
    while sy + stripe_h < bb - int(body_h * 0.15):
        _cairo_filled_rect(ctx, cx - bw + 2, sy, cx + bw - 2, sy + stripe_h, COSMO_SHIRT_G)
        sy += stripe_h * 2

    # Jacket lapels
    jw = int(hu * 0.14)
    _cairo_filled_rect(ctx, cx - bw, bt, cx - bw + jw, bb, COSMO_JACKET, LINE_COL, 1.0)
    _cairo_filled_rect(ctx, cx + bw - jw, bt, cx + bw, bb, COSMO_JACKET, LINE_COL, 1.0)

    # Notebook
    nw   = int(hu * 0.48)
    nh   = int(hu * 0.58)
    nb_y = bt + int(body_h * 0.28)
    _cairo_filled_rect(ctx, cx - bw - nw + 10, nb_y, cx - bw + 10, nb_y + nh,
                       COSMO_NB, LINE_COL, 1.0)

    # Legs
    lw    = int(hu * 0.18)
    leg_h = int(hu * 0.60)
    _cairo_filled_rect(ctx, cx - bw + 4, bb, cx - lw, bb + leg_h, COSMO_PANTS, LINE_COL, 1.0)
    _cairo_filled_rect(ctx, cx + lw, bb, cx + bw - 4, bb + leg_h, COSMO_PANTS, LINE_COL, 1.0)
    _cairo_line(ctx, [(cx, bb + int(leg_h*0.3)), (cx, bb + leg_h)], LINE_COL, 1.0)

    # Shoes
    fw = int(hu * 0.28)
    fh = int(hu * 0.18)
    lsx = cx - bw + 4 - int(fw*0.4)
    lse = cx - lw + int(fw*0.6)
    rsx = cx + lw - int(fw*0.3)
    rse = cx + bw - 4 + int(fw*0.4)
    _cairo_filled_ellipse(ctx, (lsx+lse)/2, base_y - fh/2, (lse-lsx)/2, fh/2,
                          COSMO_SHOE, LINE_COL, 1.0)
    _cairo_filled_ellipse(ctx, (rsx+rse)/2, base_y - fh/2, (rse-rsx)/2, fh/2,
                          COSMO_SHOE, LINE_COL, 1.0)
    # Soles
    _cairo_filled_ellipse(ctx, (lsx+lse)/2, base_y - int(fh*0.175),
                          (lse-lsx)/2, int(fh*0.175), (184, 154, 120))
    _cairo_filled_ellipse(ctx, (rsx+rse)/2, base_y - int(fh*0.175),
                          (rse-rsx)/2, int(fh*0.175), (184, 154, 120))


def draw_cosmo_lineup(draw, cx, base_y, h):
    """Cosmo v012 — dispatches to cairo, composites to PIL image."""
    pass  # Cairo drawing handled in generate_lineup


# ══════════════════════════════════════════════════════════════════════════════
# MIRI
# ══════════════════════════════════════════════════════════════════════════════

def draw_miri_lineup(draw, cx, base_y, h):
    hu = h / 3.2
    hy = base_y - h
    r  = int(hu * 0.46)

    bun_cx = cx + int(hu * 0.05)
    bun_cy = hy - int(hu * 0.32)
    bun_rx = int(hu * 0.38)
    bun_ry = int(hu * 0.46)
    draw.ellipse([bun_cx - bun_rx, bun_cy - bun_ry,
                  bun_cx + bun_rx, bun_cy + bun_ry],
                 fill=MIRI_HAIR, outline=LINE_COL, width=2)
    draw.arc([bun_cx - bun_rx + 4, bun_cy, bun_cx + bun_rx - 4, bun_cy + bun_ry],
             start=0, end=180, fill=(168, 152, 140), width=2)

    # WOODEN HAIRPINS — pair of dark-stained wooden hairpins piercing the bun (C44 rename from chopstick)
    hairpin_col = (92, 58, 32)  # wooden hairpins — dark warm wood brown
    draw.polygon([(bun_cx - int(hu*0.22), bun_cy - bun_ry - int(hu*0.55)),
                  (bun_cx - int(hu*0.14), bun_cy - bun_ry - int(hu*0.55)),
                  (bun_cx - int(hu*0.06), bun_cy + bun_ry - int(hu*0.12)),
                  (bun_cx - int(hu*0.13), bun_cy + bun_ry - int(hu*0.12))],
                 fill=hairpin_col, outline=LINE_COL, width=1)
    draw.polygon([(bun_cx + int(hu*0.14), bun_cy - bun_ry - int(hu*0.50)),
                  (bun_cx + int(hu*0.22), bun_cy - bun_ry - int(hu*0.50)),
                  (bun_cx + int(hu*0.13), bun_cy + bun_ry - int(hu*0.12)),
                  (bun_cx + int(hu*0.06), bun_cy + bun_ry - int(hu*0.12))],
                 fill=hairpin_col, outline=LINE_COL, width=1)

    draw.ellipse([cx - r, hy, cx + r, hy + int(hu)],
                 fill=MIRI_SKIN, outline=LINE_COL, width=2)
    ey = hy + int(hu * 0.44)
    ew = int(hu * 0.12)
    draw.ellipse([cx - int(hu*0.22) - ew, ey - ew, cx - int(hu*0.22) + ew, ey + ew],
                 fill=(250,240,220), outline=LINE_COL, width=1)
    draw.ellipse([cx + int(hu*0.10) - ew, ey - ew, cx + int(hu*0.10) + ew, ey + ew],
                 fill=(250,240,220), outline=LINE_COL, width=1)
    ep = int(ew * 0.55)
    draw.ellipse([cx - int(hu*0.22) - ep, ey - ep, cx - int(hu*0.22) + ep, ey + ep],
                 fill=(139, 94, 60))
    draw.ellipse([cx + int(hu*0.10) - ep, ey - ep, cx + int(hu*0.10) + ep, ey + ep],
                 fill=(139, 94, 60))
    draw.arc([cx - int(hu*0.22), ey + int(hu*0.20), cx + int(hu*0.22), ey + int(hu*0.44)],
             start=20, end=160, fill=LINE_COL, width=2)
    blush_r = int(hu * 0.14)
    draw.ellipse([cx - int(hu*0.40) - blush_r, ey + int(hu*0.08),
                  cx - int(hu*0.40) + blush_r, ey + int(hu*0.08) + blush_r*2],
                 fill=(212, 149, 107))
    draw.ellipse([cx + int(hu*0.28) - blush_r, ey + int(hu*0.08),
                  cx + int(hu*0.28) + blush_r, ey + int(hu*0.08) + blush_r*2],
                 fill=(212, 149, 107))
    draw.line([(cx - int(hu*0.36), ey - int(hu*0.26)), (cx - int(hu*0.10), ey - int(hu*0.22))],
              fill=(138, 122, 112), width=2)
    draw.line([(cx + int(hu*0.00), ey - int(hu*0.22)), (cx + int(hu*0.26), ey - int(hu*0.26))],
              fill=(138, 122, 112), width=2)

    shoulder_w = int(hu * 0.78)
    hip_w      = int(hu * 0.62)
    body_top_y = hy + int(hu * 0.88)
    body_h     = int(hu * 1.82)
    body_bot_y = body_top_y + body_h
    draw.polygon([(cx - shoulder_w, body_top_y), (cx + shoulder_w, body_top_y),
                  (cx + hip_w, body_bot_y), (cx - hip_w, body_bot_y)],
                 fill=MIRI_CARDIGAN, outline=LINE_COL, width=2)
    for i in range(3):
        ridge_y = body_top_y + int(body_h * (0.22 + i * 0.22))
        draw.line([(cx - int(shoulder_w * 0.6), ridge_y), (cx + int(shoulder_w * 0.6), ridge_y)],
                  fill=(212, 130, 90), width=2)
    btn_col = (232, 216, 184)
    bx = cx - int(hu*0.08)
    for i in range(4):
        by = body_top_y + int(body_h * (0.12 + i * 0.22))
        draw.ellipse([bx - 4, by - 4, bx + 4, by + 4], fill=btn_col, outline=LINE_COL, width=1)

    bag_x = cx + hip_w
    bag_y = body_top_y + int(body_h * 0.52)
    bag_w = int(hu * 0.32)
    bag_h = int(hu * 0.46)
    draw.rectangle([bag_x, bag_y, bag_x + bag_w, bag_y + bag_h],
                   fill=(140, 100, 60), outline=LINE_COL, width=1)

    iron_x   = bag_x + bag_w
    iron_y   = bag_y + bag_h - int(hu * 0.04)
    iron_len = int(hu * 0.50)
    iron_w   = int(hu * 0.07)
    draw.rectangle([iron_x, iron_y, iron_x + iron_len - int(iron_len*0.22), iron_y + iron_w + 2],
                   fill=(184, 92, 56), outline=LINE_COL, width=1)
    draw.polygon([(iron_x + iron_len - int(iron_len*0.22), iron_y),
                  (iron_x + iron_len - int(iron_len*0.22), iron_y + iron_w + 2),
                  (iron_x + iron_len, iron_y + (iron_w + 2)//2)],
                 fill=(200, 200, 200), outline=LINE_COL, width=1)

    lw    = int(hu * 0.22)
    leg_h = int(hu * 0.45)
    draw.rectangle([cx - hip_w + 6, body_bot_y, cx - lw, body_bot_y + leg_h],
                   fill=MIRI_PANTS, outline=LINE_COL, width=1)
    draw.rectangle([cx + lw, body_bot_y, cx + hip_w - 6, body_bot_y + leg_h],
                   fill=MIRI_PANTS, outline=LINE_COL, width=1)

    fw = int(hu * 0.30)
    fh = int(hu * 0.18)
    draw.rectangle([cx - hip_w + 4, base_y - fh, cx - lw + int(fw*0.4), base_y],
                   fill=MIRI_SLIPPER, outline=LINE_COL, width=1)
    draw.rectangle([cx + lw - int(fw*0.4), base_y - fh, cx + hip_w - 4, base_y],
                   fill=MIRI_SLIPPER, outline=LINE_COL, width=1)
    draw.rectangle([cx - hip_w + 4, base_y - fh,
                    cx - lw + int(fw*0.4), base_y - fh + int(fh*0.30)],
                   fill=(250, 240, 220))
    draw.rectangle([cx + lw - int(fw*0.4), base_y - fh,
                    cx + hip_w - 4, base_y - fh + int(fh*0.30)],
                   fill=(250, 240, 220))


# ══════════════════════════════════════════════════════════════════════════════
# GLITCH — floating antagonist Glitchkin (unchanged from v004)
# ══════════════════════════════════════════════════════════════════════════════

def draw_glitch_lineup(draw, cx, base_y, h):
    """Glitch at lineup height h, in canonical Corrupt Amber palette."""
    import math as _math

    float_gap = int(h * 0.18)
    rx = int(h * 0.38)
    ry = int(h * 0.44)
    bcy = base_y - float_gap - ry

    # Diamond / rhombus body (filled polygon)
    body_pts = [
        (cx,      bcy - ry),   # top spike
        (cx + rx, bcy),        # right
        (cx,      bcy + ry),   # bottom spike
        (cx - rx, bcy),        # left
    ]
    draw.polygon(body_pts, fill=GLITCH_AMB)

    # Shadow side (UV Purple — corrupted)
    shadow_pts = [
        (cx,      bcy),
        (cx + rx, bcy),
        (cx,      bcy + ry),
    ]
    draw.polygon(shadow_pts, fill=GLITCH_UV)

    # Outline
    draw.polygon(body_pts, outline=GLITCH_VB, width=3)

    # Crack / scar (Hot Magenta)
    crack_s = (cx - rx // 3, bcy - ry // 3)
    crack_m = (cx + rx // 6, bcy)
    crack_e = (cx - rx // 5, bcy + ry // 3)
    draw.line([crack_s, crack_m], fill=GLITCH_HOT, width=2)
    draw.line([crack_m, crack_e], fill=GLITCH_HOT, width=2)
    mid_c = ((crack_s[0] + crack_m[0])//2, (crack_s[1] + crack_m[1])//2)
    draw.line([mid_c, (cx + rx // 2, bcy - ry // 4)], fill=GLITCH_HOT, width=1)

    # Top spike
    tsp_h = int(h * 0.16)
    spike_pts = [
        (cx,                bcy - ry - tsp_h),
        (cx + int(rx*0.15), bcy - ry + int(tsp_h*0.3)),
        (cx - int(rx*0.15), bcy - ry + int(tsp_h*0.3)),
    ]
    draw.polygon(spike_pts, fill=GLITCH_AMB)
    draw.polygon(spike_pts, outline=GLITCH_VB, width=2)
    draw.arc([cx - int(rx*0.10), bcy - ry - tsp_h + 4,
              cx + int(rx*0.10), bcy - ry + int(tsp_h*0.2)],
             start=200, end=340, fill=GLITCH_AMB_HL, width=2)

    # Bottom spike
    bsp_h = int(h * 0.14)
    bsp_pts = [
        (cx - int(rx*0.12), bcy + ry - int(bsp_h*0.3)),
        (cx + int(rx*0.12), bcy + ry - int(bsp_h*0.3)),
        (cx,                bcy + ry + bsp_h),
    ]
    draw.polygon(bsp_pts, fill=GLITCH_AMB)
    draw.polygon(bsp_pts, outline=GLITCH_VB, width=2)

    # Pixel eyes (dual — one stable, one glitching)
    cell = max(3, int(h * 0.05))
    face_cy = bcy - int(ry * 0.15)

    PIXEL_COLS = {0: GLITCH_AMB_SH, 1: GLITCH_GOLD, 2: (0, 0, 0)}
    NEUTRAL_L = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]
    NEUTRAL_R = [[2, 1, 2], [1, 2, 1], [2, 1, 2]]

    leye_x = cx - rx // 2 - cell * 3 // 2
    leye_y = face_cy - cell * 3 // 2
    reye_x = cx + rx // 2 - cell * 3 // 2
    reye_y = face_cy - cell * 3 // 2

    for row in range(3):
        for col in range(3):
            state = NEUTRAL_L[row][col]
            px = leye_x + col * cell
            py = leye_y + row * cell
            draw.rectangle([px, py, px + cell - 1, py + cell - 1],
                            fill=PIXEL_COLS[state])
            state = NEUTRAL_R[row][col]
            px = reye_x + col * cell
            py = reye_y + row * cell
            draw.rectangle([px, py, px + cell - 1, py + cell - 1],
                            fill=PIXEL_COLS[state])

    # Flat neutral mouth
    mouth_cx = cx - 5
    mouth_cy = face_cy + cell * 3 // 2 + 3
    for i in range(3):
        draw.rectangle([mouth_cx + i * 4, mouth_cy,
                        mouth_cx + i * 4 + 2, mouth_cy + 2],
                       fill=GLITCH_AMB_SH)

    # Flat brow bars
    draw.line([(leye_x, leye_y - 3), (leye_x + cell * 3, leye_y - 3)],
              fill=GLITCH_AMB_SH, width=1)
    draw.line([(reye_x, reye_y - 3), (reye_x + cell * 3, reye_y - 3)],
              fill=GLITCH_AMB_SH, width=1)

    # Hover confetti
    import random as _random
    rng = _random.Random(42)
    confetti_y = bcy + ry + bsp_h + 5
    for _ in range(8):
        px  = rng.randint(cx - 20, cx + 20)
        py  = rng.randint(confetti_y, confetti_y + 14)
        col = rng.choice([GLITCH_HOT, GLITCH_UV, GLITCH_VB])
        draw.rectangle([px, py, px + 3, py + 3], fill=col)


# ══════════════════════════════════════════════════════════════════════════════
# HEIGHT COMPARISON MARKERS
# ══════════════════════════════════════════════════════════════════════════════

def draw_height_markers(draw, font_small):
    # Heights measured from each character's own ground tier
    luma_top   = FG_GROUND_Y - CHAR_HEIGHTS["luma"]
    cosmo_top  = BG_GROUND_Y - CHAR_HEIGHTS["cosmo"]
    luma_chest = FG_GROUND_Y - int(CHAR_HEIGHTS["luma"] * 0.62)
    miri_top   = BG_GROUND_Y - CHAR_HEIGHTS["miri"]

    lines = [
        (cosmo_top,  TICK_COL,           "Cosmo top [BG]"),
        (luma_top,   (180, 140, 80),      "Luma top [FG]"),
        (miri_top,   (140, 160, 120),     "Miri top [BG]"),
        (luma_chest, (80, 160, 200),      "Byte / Glitch height ref"),
    ]

    x_start = 30
    x_end   = IMG_W - 100

    for y, col, label in lines:
        x = x_start
        while x < x_end:
            draw.line([(x, y), (min(x + 8, x_end), y)], fill=col, width=1)
            x += 13
        draw.text((x_end + 4, y - 7), label, fill=col, font=font_small)


# ══════════════════════════════════════════════════════════════════════════════
# BYTE FLOAT-GAP DIMENSION ARROW (retained from v003/v004)
# ══════════════════════════════════════════════════════════════════════════════

def draw_byte_float_dimension(draw, font_small):
    GROUNDFLOOR_COL = (100, 168, 200)

    byte_cx   = CHAR_X["byte"]
    # Use unscaled BYTE_H for the float-gap engineering annotation
    # (the gap proportions are a characteristic of Byte's design, not the FG scale)
    s         = BYTE_H
    float_gap = int(s * 0.18)
    body_rx   = s // 2

    arrow_x = byte_cx + body_rx + 14
    top_y   = FG_GROUND_Y - float_gap
    bot_y   = FG_GROUND_Y

    if bot_y - top_y < 6:
        return

    draw.line([(arrow_x, top_y), (arrow_x, bot_y)], fill=GROUNDFLOOR_COL, width=2)

    tip_size = 5
    draw.polygon([(arrow_x, top_y),
                  (arrow_x - tip_size, top_y + tip_size * 2),
                  (arrow_x + tip_size, top_y + tip_size * 2)],
                 fill=GROUNDFLOOR_COL)
    draw.polygon([(arrow_x, bot_y),
                  (arrow_x - tip_size, bot_y - tip_size * 2),
                  (arrow_x + tip_size, bot_y - tip_size * 2)],
                 fill=GROUNDFLOOR_COL)

    serif_w = 7
    draw.line([(arrow_x - serif_w, top_y), (arrow_x + serif_w, top_y)],
              fill=GROUNDFLOOR_COL, width=2)
    draw.line([(arrow_x - serif_w, bot_y), (arrow_x + serif_w, bot_y)],
              fill=GROUNDFLOOR_COL, width=2)

    label   = "0.25 HU"
    label_x = arrow_x + serif_w + 4
    label_y = (top_y + bot_y) // 2 - 5
    draw.text((label_x, label_y), label, fill=GROUNDFLOOR_COL, font=font_small)

    gf_x0 = byte_cx - 70
    gf_x1 = byte_cx + 70
    gf_y  = FG_GROUND_Y
    x = gf_x0
    while x < gf_x1:
        draw.line([(x, gf_y), (min(x + 10, gf_x1), gf_y)],
                  fill=GROUNDFLOOR_COL, width=1)
        x += 14


# ══════════════════════════════════════════════════════════════════════════════
# MAIN GENERATOR
# ══════════════════════════════════════════════════════════════════════════════

def generate_lineup(output_path):
    img  = Image.new('RGB', (IMG_W, IMG_H), BG)
    draw = ImageDraw.Draw(img)

    try:
        font_title = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
        font_label = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 13)
        font_small = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)
    except Exception:
        font_title = font_label = font_small = ImageFont.load_default()

    draw.rectangle([0, 0, IMG_W, IMG_H], fill=BG)

    title = ("LUMA & THE GLITCHKIN — Full Cast Lineup — C52 v012"
             " (pycairo rebuild: Luma+Byte+Cosmo | two-tier staging: FG/WARM + BG/COOL)")
    draw.text((20, 14), title, fill=LABEL_COL, font=font_title)
    draw.line([(0, TITLE_H - 4), (IMG_W, TITLE_H - 4)], fill=TICK_COL, width=1)

    # ── Two-tier gradient depth bands (v010 — Option C, Lee Tanaka C45) ─────────
    # Drawn BEFORE characters. Both bands ≤10px tall — below all character geometry.
    # Warm/cool encoding: warm = FG/close, cool = BG/far. Reads at thumbnail scale.
    _BG_SHADOW_COL = (180, 195, 210)   # cool slate
    _BG_SHADOW_H   = 8                  # px
    _FG_SHADOW_COL = (220, 200, 160)   # warm amber
    _FG_SHADOW_H   = 10                 # px

    # BG tier drop-shadow (cool slate) — drawn first
    for row in range(_BG_SHADOW_H):
        alpha_frac = 1.0 - row / _BG_SHADOW_H    # fades to 0 downward
        r = int(_BG_SHADOW_COL[0] + (BG[0] - _BG_SHADOW_COL[0]) * (1 - alpha_frac))
        g = int(_BG_SHADOW_COL[1] + (BG[1] - _BG_SHADOW_COL[1]) * (1 - alpha_frac))
        b = int(_BG_SHADOW_COL[2] + (BG[2] - _BG_SHADOW_COL[2]) * (1 - alpha_frac))
        draw.line([(0, BG_GROUND_Y + row), (IMG_W, BG_GROUND_Y + row)],
                  fill=(r, g, b), width=1)

    # FG tier drop-shadow (warm amber)
    for row in range(_FG_SHADOW_H):
        alpha_frac = 1.0 - row / _FG_SHADOW_H
        r = int(_FG_SHADOW_COL[0] + (BG[0] - _FG_SHADOW_COL[0]) * (1 - alpha_frac))
        g = int(_FG_SHADOW_COL[1] + (BG[1] - _FG_SHADOW_COL[1]) * (1 - alpha_frac))
        b = int(_FG_SHADOW_COL[2] + (BG[2] - _FG_SHADOW_COL[2]) * (1 - alpha_frac))
        draw.line([(0, FG_GROUND_Y + row), (IMG_W, FG_GROUND_Y + row)],
                  fill=(r, g, b), width=1)

    # Tier labels (updated with warm/cool grammar)
    _tier_col_bg = (148, 165, 180)   # cool label color
    _tier_col_fg = (180, 150, 90)    # warm label color
    draw.text((IMG_W - 110, BG_GROUND_Y + 5), "BG tier (COOL)",
              fill=_tier_col_bg, font=font_small)
    draw.text((IMG_W - 110, FG_GROUND_Y + 5), "FG tier (WARM)",
              fill=_tier_col_fg, font=font_small)

    draw_byte_float_dimension(draw, font_small)
    draw = ImageDraw.Draw(img)  # refresh after annotations

    draw_height_markers(draw, font_small)
    draw = ImageDraw.Draw(img)

    # ── Cairo characters (Luma, Byte, Cosmo) — render on cairo, composite ──
    _cairo_drawers = {
        "luma":  _draw_luma_cairo,
        "byte":  _draw_byte_cairo,
        "cosmo": _draw_cosmo_cairo,
    }
    # PIL characters (Miri, Glitch) — draw directly
    _pil_drawers = {
        "miri":   draw_miri_lineup,
        "glitch": draw_glitch_lineup,
    }

    for char in CHAR_ORDER:
        cx       = CHAR_X[char]
        h        = CHAR_HEIGHTS[char]
        ground_y = CHAR_GROUND_Y[char]
        if char in _cairo_drawers:
            char_layer = _render_cairo_character(_cairo_drawers[char], cx, ground_y, h)
            img = Image.alpha_composite(img.convert("RGBA"), char_layer).convert("RGB")
            draw = ImageDraw.Draw(img)
        else:
            _pil_drawers[char](draw, cx, ground_y, h)
            draw = ImageDraw.Draw(img)  # refresh after each character

    # Character name labels below their respective ground lines
    for char in CHAR_ORDER:
        cx      = CHAR_X[char]
        ground_y = CHAR_GROUND_Y[char]
        lines   = CHAR_LABELS[char].split("\n")
        label_y = ground_y + 8
        for line in lines:
            lw = len(line) * 6
            draw.text((cx - lw // 2, label_y), line, fill=LABEL_COL, font=font_small)
            label_y += 13

    # Vertical height brackets — measured from each char's own ground tier
    for char in CHAR_ORDER:
        cx       = CHAR_X[char] - 44
        h        = CHAR_HEIGHTS[char]
        ground_y = CHAR_GROUND_Y[char]
        top_y    = ground_y - h
        if char in ("byte", "glitch"):
            s         = h
            float_gap = int(s * 0.18)
            body_ry   = int(s * 0.55)
            top_y     = ground_y - float_gap - body_ry * 2
        draw.line([(cx, top_y), (cx, ground_y)], fill=TICK_COL, width=1)
        draw.line([(cx - 4, top_y), (cx + 4, top_y)], fill=TICK_COL, width=1)
        draw.line([(cx - 4, ground_y), (cx + 4, ground_y)], fill=TICK_COL, width=1)
        draw.text((cx - 20, (top_y + ground_y)//2 - 5),
                  f"{h}px", fill=TICK_COL, font=font_small)

    # Staging annotation bar
    annotation = (
        f"Staging: FG tier (y={FG_GROUND_Y}, WARM) = Luma+Byte @+3% scale.  "
        f"BG tier (y={BG_GROUND_Y}, COOL) = Cosmo+Miri+Glitch @baseline scale.  "
        "WARM = FG / COOL = BG.  "
        "Proportion constants unchanged — uniform post-scale only."
    )
    draw.text((20, IMG_H - 34), annotation, fill=(140, 120, 100), font=font_small)

    footer = (
        f"Full cast: Cosmo | Miri | LUMA | Byte | Glitch.  "
        f"Reference: 1 head unit = {HEAD_UNIT:.0f}px.  "
        "Colors per master_palette.md (canonical).  C52 v012 (pycairo: Luma+Byte+Cosmo)."
    )
    draw.text((20, IMG_H - 18), footer, fill=TICK_COL, font=font_small)

    # IMAGE SIZE RULE: ≤ 1280px in both dimensions
    if img.size[0] > 1280 or img.size[1] > 1280:
        img.thumbnail((1280, 1280), Image.LANCZOS)

    img.save(output_path)
    print(f"Saved: {output_path}")
    print(f"  Size: {img.size[0]}x{img.size[1]}px")


def main():
    import os
    out_dir = output_dir('characters', 'main')
    os.makedirs(out_dir, exist_ok=True)
    generate_lineup(os.path.join(out_dir, "LTG_CHAR_character_lineup.png"))
    print("Character lineup v012 generation complete.")
    print("  C52 changes: pycairo rebuild for Luma, Byte, Cosmo (native bezier AA)")
    print(f"  FG_GROUND_Y={FG_GROUND_Y}, BG_GROUND_Y={BG_GROUND_Y}, FG_SCALE={FG_SCALE}")
    print(f"  Character order (L→R): cosmo | miri | luma | byte | glitch")
    print(f"  Luma: {LUMA_RENDER_H_FG}px drawn ({LUMA_RENDER_H}px base ×{FG_SCALE}), "
          f"{LUMA_HEADS} heads, head unit = {HEAD_UNIT:.1f}px")
    print(f"  Byte: {BYTE_H_FG}px drawn ({BYTE_H}px base ×{FG_SCALE})")


if __name__ == '__main__':
    main()
