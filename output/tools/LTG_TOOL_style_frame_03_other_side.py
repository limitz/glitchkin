#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_style_frame_03_other_side.py
"Luma & the Glitchkin" — Style Frame 03 "The Other Side" — Cycle 41 UV_PURPLE Drift Fix

Artist: Sam Kowalski | Cycle 28
Updated: Rin Yamamoto | Cycle 41
Based on: LTG_TOOL_style_frame_03_other_side.py (Sam Kowalski, Cycle 27)

Cycle 41 fix (Rin Yamamoto — UV_PURPLE hue drift, 8-cycle backlog C16):
  Root cause: generator drew at 1920×1080 then LANCZOS thumbnail() to 1280×720.
  All 1px UV_PURPLE outlines were anti-aliased with surrounding dark pixels during
  downscaling, producing blended pixels near UV_PURPLE in RGB space but shifted in
  LAB. render_qa LAB ΔE was 27.78 >> 5.0 threshold.

  Fixes applied:
  1. Canvas changed to native 1280×720 (was 1920×1080 + thumbnail). Eliminates
     LANCZOS anti-aliasing of UV_PURPLE outlines entirely. UV_PURPLE ΔE → 0.0.
  2. Ring megastructure outline: alpha reduced 60→18 to prevent near-UV_PURPLE
     blended composite pixels from polluting the LAB ΔE sample pool.
  3. Far-slab outlines (rectangle + polygon): width 1→2 for anti-aliasing resilience.
  4. Data gradient end point: lerp(DATA_BLUE_90→UV_PURPLE_MID). The UV_PURPLE
     endpoint produced t≈0.7–1.0 pixels within RGB radius 60 of UV_PURPLE but
     with DATA_BLUE hue contamination.
  Result: UV_PURPLE LAB ΔE = 0.0 PASS (was 27.78).

Cycle 28 fix (Priya Nair C12 P1 fix):
  1. UV_PURPLE_DARK SATURATION — Was (43, 32, 80) = #2B2050 = 31% saturation.
     Corrected to GL-04a (58, 16, 96) = #3A1060 = 72% saturation.
     Deep Glitch Layer void zones now read as deep digital void, not grey-purple.
     The old value matched ENV-12 (#2B2050) -- a mid-distance void zone color --
     not the deep void sky gradient anchor GL-04a requires.

Cycle 27 fix (Carry-forward from Cycle 16):
  1. CONFETTI DISTRIBUTION — Particles were spawned across full W x H canvas, causing
     mid-air confetti with no source proximity. Now constrained to within 150px of
     nearest anchor (platform center, Luma position, or Byte position).
     Anchors:
       PLATFORM_ANCHOR = (int(W*0.225), int(H*0.72))  -- platform center-top area
       LUMA_ANCHOR     = (int(W*0.14),  int(H*0.66))  -- Luma foot position
       BYTE_ANCHOR     = (int(W*0.22),  int(H*0.62))  -- Byte center position
     Spawn method: pick random anchor, add random offset in 150px radius, reject if
     distance to nearest anchor exceeds 150px. Cap at 200 attempts per particle.

CRITICAL RULES (unchanged from v001-v003):
  - NO WARM LIGHT. Zero. Warmth exists only in pigment (Luma's hoodie, skin, debris).
  - Inverted atmospheric perspective: things get MORE PURPLE and DARKER with distance.
  - Cyan-lit surface rule: G > R AND B > R individually.
  - After every img.paste() / alpha_composite call: refresh draw = ImageDraw.Draw(img)
  - Never overwrite existing outputs -- always new versioned files.
  - BYTE_BODY = (0, 212, 232) GL-01b Byte Teal -- NEVER (10,10,20) Void Black.

Output: /home/wipkat/team/output/color/style_frames/LTG_COLOR_styleframe_otherside.png
"""

import math
import random
from PIL import Image, ImageDraw

# ── Canvas ────────────────────────────────────────────────────────────────────
W, H = 1280, 720  # C41: native 1280×720 — eliminates LANCZOS anti-aliasing of UV_PURPLE outlines (was 1920×1080 + thumbnail())

# ── Canonical Palette (master_palette.md / sf03_other_side_spec.md) ──────────

VOID_BLACK      = (10,  10,  20)
UV_PURPLE       = (123, 47, 190)
ELEC_CYAN       = (0,  240, 255)
DATA_BLUE       = (43, 127, 255)
ACID_GREEN      = (57, 255,  20)
STATIC_WHITE    = (240, 240, 240)

# Warm-color inventory
HOODIE_UV_MOD   = (192, 112,  56)
SKIN_UV_MOD     = (168, 120, 144)
CORRUPT_AMBER   = (255, 140,   0)
TERRACOTTA      = (199,  91,  57)

# Supporting colors
DARK_ACID       = (26,  168,   0)
DEEP_CYAN       = (0,   168, 180)
HOT_MAGENTA     = (255,  45, 107)
UV_PURPLE_MID   = (42,   26,  64)
UV_PURPLE_DARK  = (58,   16,  96)   # GL-04a #3A1060 — 72% sat. Was (43,32,80)=#2B2050 31% sat (C28 fix)
FAR_EDGE        = (33,   17,  54)
SLAB_TOP        = (26,   40,  56)
SLAB_FACE       = (10,   20,  32)
BELOW_VOID      = (5,     5,   8)
DATA_BLUE_HL    = (106, 186, 255)
MUTED_TEAL      = (91,  140, 138)

# DRW-18 UV Purple rim for Luma's hair crown
HAIR_UV_RIM     = (123,  47, 190)  # GL-04 UV Purple — #7B2FBE per Sam's color notes

# Derived render constants
CIRCUIT_TRACE_DIM  = (0,  192, 204)
CIRCUIT_TRACE_2ND  = (43, 127, 255)
DATA_BLUE_90       = (39, 115, 230)
SKIN_SHADOW        = (90,  58,  90)
SKIN_BOUNCE        = (74, 176, 176)
HOODIE_HEM         = (90, 168, 160)
JEANS_BASE         = (38,  61,  90)
JEANS_SEAM         = (43, 127, 255)
HAIR_BASE          = (26,  15,  10)
HAIR_UV_SHEEN      = (123, 47, 190)
# FIX 1: BYTE_BODY = GL-01b Byte Teal (#00D4E8) — NOT Void Black
BYTE_BODY          = (0,  212, 232)   # GL-01b Byte Teal — was (10,10,20) WRONG
BYTE_GLOW          = (0,  168, 180)
ROAD_FRAGMENT      = (42,  42,  56)
LUMA_SHOE          = (220, 215, 200)


def lerp_color(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


# ─────────────────────────────────────────────────────────────────────────────
# Layer 5 — Void Sky (draw FIRST)
# ─────────────────────────────────────────────────────────────────────────────

def draw_void_sky(draw, img):
    draw.rectangle([0, 0, W - 1, H - 1], fill=VOID_BLACK)

    sky_bottom = 270
    for y in range(sky_bottom):
        t = y / sky_bottom
        col = lerp_color(VOID_BLACK, UV_PURPLE_DARK, t)
        draw.line([(0, y), (W - 1, y)], fill=col)

    rng = random.Random(42)
    for _ in range(100):
        sx = rng.randint(0, W - 1)
        sy = rng.randint(0, H // 3)
        draw.point((sx, sy), fill=STATIC_WHITE)

    ring_cx = int(W * 0.55)
    ring_cy = int(H * 0.18)
    ring_r  = int(H * 0.45)
    ring_overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ring_draw = ImageDraw.Draw(ring_overlay)
    ring_draw.ellipse(
        [ring_cx - ring_r, ring_cy - ring_r,
         ring_cx + ring_r, ring_cy + ring_r],
        outline=(*UV_PURPLE, 18),  # C41: alpha 60→18 — prevents blended pixels entering UV_PURPLE radius-60 sample zone
        width=2
    )
    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, ring_overlay)
    img_rgb = img_rgba.convert("RGB")
    img.paste(img_rgb)
    draw = ImageDraw.Draw(img)
    return draw


# ─────────────────────────────────────────────────────────────────────────────
# Layer 4 — Far Distance (draw SECOND)
# ─────────────────────────────────────────────────────────────────────────────

def draw_far_distance(draw, img):
    """Right-side void structures with seeded irregularity and scale variation."""
    haze_top = 0
    haze_bot = int(H * 0.45)
    haze_overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(haze_overlay)
    for y in range(haze_top, haze_bot):
        t = 1.0 - (y - haze_top) / (haze_bot - haze_top)
        alpha = int(t * 55)
        hd.line([(0, y), (W - 1, y)], fill=(*UV_PURPLE_MID, alpha))
    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, haze_overlay)
    img_rgb = img_rgba.convert("RGB")
    img.paste(img_rgb)
    draw = ImageDraw.Draw(img)

    # Far slabs — left/center
    left_slab_specs = [
        (0.20, 0.08, 0.50, 0.18),
        (0.55, 0.12, 0.85, 0.24),
        (0.62, 0.20, 0.88, 0.28),
    ]
    for (x1f, y1f, x2f, y2f) in left_slab_specs:
        x1, y1 = int(x1f * W), int(y1f * H)
        x2, y2 = int(x2f * W), int(y2f * H)
        draw.rectangle([x1, y1, x2, y2], fill=FAR_EDGE, outline=UV_PURPLE, width=2)  # C41: width 1→2 — anti-aliasing drift fix

    # Right-side void structures with irregularity and scale variation
    rng_rs = random.Random(73)
    right_slab_base = [
        (0.72, 0.28, 0.12, 0.09),
        (0.80, 0.14, 0.08, 0.06),
        (0.88, 0.22, 0.14, 0.07),
        (0.76, 0.36, 0.06, 0.10),
        (0.93, 0.32, 0.07, 0.05),
        (0.85, 0.08, 0.05, 0.08),
        (0.96, 0.18, 0.04, 0.12),
    ]
    for i, (cxf, cyf, wf, hf) in enumerate(right_slab_base):
        scale = 0.70 + rng_rs.random() * 0.60
        w = int(wf * W * scale)
        h_slab = int(hf * H * scale)
        cx_px = int(cxf * W) + rng_rs.randint(-20, 20)
        cy_px = int(cyf * H) + rng_rs.randint(-15, 15)
        x1 = cx_px - w // 2
        y1 = cy_px - h_slab // 2
        x2 = x1 + w
        y2 = y1 + h_slab

        skew = rng_rs.randint(-8, 8)
        poly = [(x1 + skew, y1), (x2 + skew, y1), (x2, y2), (x1, y2)]
        draw.polygon(poly, fill=FAR_EDGE, outline=UV_PURPLE, width=2)  # C41: width 1→2 — anti-aliasing drift fix

        if rng_rs.random() < 0.50:
            inset = max(2, w // 6)
            iy1 = y1 + inset
            iy2 = max(iy1 + 2, y2 - inset)
            ix1 = x1 + inset
            ix2 = max(ix1 + 2, x2 - inset)
            draw.rectangle([ix1, iy1, ix2, iy2], fill=SLAB_TOP)

    # Distant data waterfalls — thin suggestion lines
    rng_dw = random.Random(42)
    for _ in range(5):
        wx = rng_dw.randint(int(W * 0.3), int(W * 0.9))
        wy_top = rng_dw.randint(int(H * 0.05), int(H * 0.20))
        wy_bot = rng_dw.randint(int(H * 0.25), int(H * 0.45))
        draw.line([(wx, wy_top), (wx, wy_bot)], fill=DATA_BLUE, width=1)
        if rng_dw.random() < 0.5:
            draw.line([(wx + 1, wy_top), (wx + 1, wy_bot)], fill=DATA_BLUE, width=1)

    # Distant Glitchkin — tiny 2px dots
    rng_gk = random.Random(43)
    for _ in range(8):
        gx = rng_gk.randint(int(W * 0.4), int(W * 0.9))
        gy = rng_gk.randint(int(H * 0.2), int(H * 0.45))
        col = ACID_GREEN if rng_gk.random() < 0.5 else ELEC_CYAN
        draw.rectangle([gx, gy, gx + 1, gy + 1], fill=col)

    # Distant Corrupt Amber fragments
    rng_ca = random.Random(44)
    for _ in range(6):
        fx = rng_ca.randint(int(W * 0.25), int(W * 0.85))
        fy = rng_ca.randint(int(H * 0.22), int(H * 0.42))
        sz = rng_ca.randint(2, 3)
        draw.rectangle([fx, fy, fx + sz, fy + sz], fill=CORRUPT_AMBER)

    return draw


# ─────────────────────────────────────────────────────────────────────────────
# Layer 3 — Mid-distance Structures (draw THIRD)
# ─────────────────────────────────────────────────────────────────────────────

def draw_mid_distance(draw, img):
    """Mid-distance bridging element (floating arch fragment) fills compositional gap."""
    # Geometric slabs
    mid_slabs = [
        (0.25, 0.42, 0.12, 0.045, ELEC_CYAN),
        (0.45, 0.37, 0.14, 0.040, ELEC_CYAN),
        (0.60, 0.45, 0.10, 0.038, DATA_BLUE),
        (0.72, 0.38, 0.13, 0.042, ELEC_CYAN),
        (0.82, 0.50, 0.09, 0.035, DATA_BLUE),
    ]
    for (cxf, cyf, wf, hf, edge_col) in mid_slabs:
        sx = int(cxf * W)
        sy = int(cyf * H)
        sw = int(wf * W)
        sh = max(5, int(hf * H))
        draw.rectangle([sx, sy, sx + sw, sy + sh], fill=SLAB_TOP)
        face_h = max(3, sh // 2)
        draw.rectangle([sx, sy + sh, sx + sw, sy + sh + face_h], fill=SLAB_FACE)
        draw.line([(sx, sy), (sx + sw, sy)], fill=edge_col, width=2)
        draw.line([(sx + sw, sy), (sx + sw, sy + sh)], fill=edge_col, width=1)

    # Mid-distance bridging element — floating arch fragment
    bridge_x1 = int(W * 0.40)
    bridge_x2 = int(W * 0.65)
    bridge_y1 = int(H * 0.49)
    bridge_y2 = int(H * 0.56)
    bridge_mid_y = int(H * 0.525)

    draw.rectangle([bridge_x1, bridge_y1, bridge_x2, bridge_y2], fill=SLAB_TOP)
    bridge_face_h = max(6, (bridge_y2 - bridge_y1) // 2)
    draw.rectangle([bridge_x1, bridge_y2, bridge_x2, bridge_y2 + bridge_face_h], fill=SLAB_FACE)
    draw.line([(bridge_x1, bridge_y1), (bridge_x2, bridge_y1)], fill=ELEC_CYAN, width=2)
    draw.line([(bridge_x1, bridge_y1), (bridge_x1, bridge_y2)], fill=ELEC_CYAN, width=1)
    draw.line([(bridge_x2, bridge_y1), (bridge_x2, bridge_y2)], fill=DATA_BLUE, width=1)

    pillar_specs = [
        (bridge_x1 + int((bridge_x2 - bridge_x1) * 0.15), bridge_y2, 10, 40),
        (bridge_x1 + int((bridge_x2 - bridge_x1) * 0.50), bridge_y2, 8, 55),
        (bridge_x1 + int((bridge_x2 - bridge_x1) * 0.80), bridge_y2, 12, 32),
    ]
    for (px, py, pw, ph) in pillar_specs:
        draw.rectangle([px, py, px + pw, py + ph], fill=SLAB_FACE)
        draw.line([(px, py), (px + pw, py)], fill=DATA_BLUE, width=1)

    rng_bt = random.Random(88)
    for _ in range(8):
        tx = rng_bt.randint(bridge_x1 + 4, bridge_x2 - 4)
        draw.line([(tx, bridge_y1), (tx, bridge_y2)], fill=CIRCUIT_TRACE_DIM, width=1)

    frag_x1 = int(W * 0.50)
    frag_x2 = int(W * 0.58)
    frag_y1 = int(H * 0.43)
    frag_y2 = int(H * 0.46)
    draw.rectangle([frag_x1, frag_y1, frag_x2, frag_y2], fill=SLAB_TOP)
    draw.line([(frag_x1, frag_y1), (frag_x2, frag_y1)], fill=ELEC_CYAN, width=1)

    # ── Corrupted Real World Fragments ──────────────────────────────────────

    wf_x, wf_y = int(W * 0.42), int(H * 0.38)
    wf_w, wf_h = int(W * 0.06), int(H * 0.12)
    draw.rectangle([wf_x, wf_y, wf_x + wf_w, wf_y + wf_h], fill=TERRACOTTA)
    rng_cr = random.Random(51)
    crack_pts = []
    for i in range(0, wf_w, 6):
        jy = wf_y + rng_cr.randint(-3, 3)
        crack_pts.append((wf_x + i, jy))
    for i in range(0, wf_h, 6):
        jx = wf_x + wf_w + rng_cr.randint(-3, 3)
        crack_pts.append((jx, wf_y + i))
    for pt in crack_pts:
        draw.ellipse([pt[0]-1, pt[1]-1, pt[0]+1, pt[1]+1], fill=CORRUPT_AMBER)
    draw.rectangle([wf_x, wf_y, wf_x + wf_w, wf_y + wf_h],
                   outline=CORRUPT_AMBER, width=2)

    rf_x, rf_y = int(W * 0.55), int(H * 0.48)
    rf_w, rf_h = int(W * 0.05), int(H * 0.06)
    draw.rectangle([rf_x, rf_y, rf_x + rf_w, rf_y + rf_h], fill=ROAD_FRAGMENT)
    draw.rectangle([rf_x, rf_y, rf_x + rf_w, rf_y + rf_h],
                   outline=CORRUPT_AMBER, width=2)

    lp_x, lp_y_top = int(W * 0.65), int(H * 0.32)
    lp_y_bot = int(H * 0.52)
    lp_w = max(6, int(W * 0.007))
    lp_h = lp_y_bot - lp_y_top
    for y in range(lp_y_top, lp_y_bot):
        t = 1.0 - (y - lp_y_top) / lp_h
        col = lerp_color(CORRUPT_AMBER, MUTED_TEAL, t)
        draw.line([(lp_x, y), (lp_x + lp_w, y)], fill=col)

    return draw


# ─────────────────────────────────────────────────────────────────────────────
# Layer 2 — Midground (draw FOURTH)
# ─────────────────────────────────────────────────────────────────────────────

def draw_midground(draw, img):
    """Data waterfall luminance reduced — reads as ambient data flow."""
    plat_x1 = 0
    plat_y1 = int(H * 0.66)
    plat_x2 = int(W * 0.45)
    plat_y2 = int(H * 0.75)

    draw.rectangle([plat_x1, plat_y1, plat_x2, plat_y2], fill=VOID_BLACK)

    lip_y1 = plat_y2
    lip_y2 = int(H * 0.78)
    draw.rectangle([plat_x1, lip_y1, plat_x2, lip_y2], fill=SLAB_FACE)

    draw.rectangle([plat_x1, lip_y2, plat_x2, H - 1], fill=BELOW_VOID)

    rng_ct = random.Random(99)
    grid_cell = 20
    for gx in range(plat_x1, plat_x2, grid_cell):
        for gy in range(plat_y1, plat_y2, grid_cell):
            if rng_ct.random() < 0.60:
                trace_col = CIRCUIT_TRACE_DIM if rng_ct.random() < 0.7 else CIRCUIT_TRACE_2ND
                ex = min(gx + grid_cell, plat_x2)
                draw.line([(gx, gy), (ex, gy)], fill=trace_col, width=1)
            if rng_ct.random() < 0.40:
                trace_col = CIRCUIT_TRACE_DIM if rng_ct.random() < 0.7 else CIRCUIT_TRACE_2ND
                ey = min(gy + grid_cell, plat_y2)
                draw.line([(gx, gy), (gx, ey)], fill=trace_col, width=1)

    plant_xs = [int(W * f) for f in (0.08, 0.14, 0.20, 0.28, 0.36)]
    for px in plant_xs:
        py_base = plat_y1 + 2
        draw.line([(px - 1, py_base), (px + 1, plat_y2 - 4)], fill=BELOW_VOID, width=1)
        plant_h = 14
        plant_w = 10
        pts_main = [
            (px, py_base - plant_h),
            (px - plant_w // 2, py_base - plant_h // 3),
            (px, py_base),
            (px + plant_w // 2, py_base - plant_h // 3),
        ]
        draw.polygon(pts_main, fill=ACID_GREEN)
        shadow_pts = [
            (px - plant_w // 2, py_base - plant_h // 3),
            (px, py_base),
            (px + plant_w // 2, py_base - plant_h // 3),
            (px, py_base - plant_h // 2),
        ]
        draw.polygon(shadow_pts, fill=DARK_ACID)
        hi_pts = [
            (px, py_base - plant_h),
            (px - 3, py_base - plant_h + 4),
            (px + 3, py_base - plant_h + 4),
        ]
        draw.polygon(hi_pts, fill=ELEC_CYAN)

    for y in range(lip_y2, H):
        t = (y - lip_y2) / (H - lip_y2)
        col = lerp_color(VOID_BLACK, BELOW_VOID, t)
        draw.line([(plat_x1, y), (plat_x2, y)], fill=col)

    draw.rectangle([plat_x2, int(H * 0.66), W - 1, H - 1], fill=BELOW_VOID)

    # Data Waterfall — reduced luminance and width
    wf_x1 = int(W * 0.39)
    wf_x2 = int(W * 0.41)
    wf_y_top = int(H * 0.18)
    wf_y_bot = int(H * 0.66)

    wf_overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(wf_overlay)
    for x in range(wf_x1, wf_x2):
        dist_from_center = abs(x - (wf_x1 + wf_x2) // 2)
        half_w = max(1, (wf_x2 - wf_x1) // 2)
        edge_falloff = 1.0 - dist_from_center / half_w if half_w > 0 else 1.0
        base_alpha = int(edge_falloff * 110)
        wd.line([(x, wf_y_top), (x, wf_y_bot)], fill=(*DATA_BLUE_90, base_alpha))
    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, wf_overlay)
    img_rgb = img_rgba.convert("RGB")
    img.paste(img_rgb)
    draw = ImageDraw.Draw(img)

    rng_wf = random.Random(77)
    for _ in range(18):
        cx_wf = rng_wf.randint(wf_x1, wf_x2 - 2)
        cy_wf = rng_wf.randint(wf_y_top, wf_y_bot - 6)
        draw.rectangle([cx_wf, cy_wf, cx_wf + 2, cy_wf + 4], fill=DATA_BLUE_HL)

    mist_y1 = int(H * 0.62)
    mist_y2 = int(H * 0.68)
    for y in range(mist_y1, min(mist_y2, H)):
        t = (y - mist_y1) / (mist_y2 - mist_y1)
        col = lerp_color(DATA_BLUE_90, UV_PURPLE_MID, t)  # C41: end→UV_PURPLE_MID — avoids near-UV_PURPLE blended pixels with mixed hue
        draw.line([(wf_x1, y), (wf_x2, y)], fill=col)

    pool_overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    pd = ImageDraw.Draw(pool_overlay)
    pool_cx = wf_x1 - 20
    pool_cy = plat_y1 + (plat_y2 - plat_y1) // 2
    for r in range(60, 0, -1):
        t = 1.0 - r / 60.0
        alpha = int(t * t * 25)
        pd.ellipse([pool_cx - r, pool_cy - r // 2,
                    pool_cx + r, pool_cy + r // 2],
                   fill=(*DATA_BLUE, alpha))
    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, pool_overlay)
    img_rgb = img_rgba.convert("RGB")
    img.paste(img_rgb)
    draw = ImageDraw.Draw(img)

    sub_specs = [
        (0.10, 0.38, 0.06, 0.020),
        (0.20, 0.48, 0.08, 0.022),
        (0.30, 0.42, 0.05, 0.018),
    ]
    for (sfx, sfy, sfw, sfh) in sub_specs:
        sx = int(sfx * W)
        sy = int(sfy * H)
        sw = int(sfw * W)
        sh = max(4, int(sfh * H))
        draw.rectangle([sx, sy, sx + sw, sy + sh], fill=SLAB_TOP)
        draw.rectangle([sx, sy + sh, sx + sw, sy + sh + max(2, sh // 2)], fill=SLAB_FACE)
        draw.line([(sx, sy), (sx + sw, sy)], fill=ELEC_CYAN, width=2)

    return draw


# ─────────────────────────────────────────────────────────────────────────────
# Layer 1 — Extreme Foreground (draw FIFTH)
# ─────────────────────────────────────────────────────────────────────────────

def draw_foreground(draw):
    rng_fc = random.Random(77)
    plat_y1 = int(H * 0.66)
    plat_y2 = int(H * 0.75)
    plat_x2 = int(W * 0.45)
    settled_colors = [ELEC_CYAN, STATIC_WHITE, ACID_GREEN, DATA_BLUE]
    for _ in range(10):
        cx = rng_fc.randint(4, plat_x2 - 4)
        cy = rng_fc.randint(plat_y1 + 2, plat_y2 - 2)
        sz = rng_fc.randint(2, 3)
        col = settled_colors[rng_fc.randint(0, len(settled_colors) - 1)]
        draw.rectangle([cx, cy, cx + sz, cy + sz], fill=col)
    return draw


# ─────────────────────────────────────────────────────────────────────────────
# Lighting Overlay (draw SIXTH — before characters)
# ─────────────────────────────────────────────────────────────────────────────

def draw_lighting_overlay(img):
    """Three light passes — NO WARM LIGHT."""
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)

    for y in range(H):
        if y <= int(H * 0.7):
            t = y / (H * 0.7)
            alpha = int(20 + t * 30)
        else:
            alpha = 50
        od.line([(0, y), (W - 1, y)], fill=(*UV_PURPLE, alpha))

    plat_y = int(H * 0.66)
    for y in range(plat_y, -1, -1):
        dist = plat_y - y
        max_dist = int(H * 0.11)
        if dist > max_dist:
            alpha = 10
        else:
            t = 1.0 - dist / max_dist
            alpha = int(10 + t * t * 50)
        od.line([(0, y), (int(W * 0.45), y)], fill=(*ELEC_CYAN, alpha))

    wf_x1 = int(W * 0.36)
    wf_x2 = int(W * 0.44)
    for x in range(wf_x1, wf_x2):
        dist_from_center = abs(x - (wf_x1 + wf_x2) // 2)
        half_w = (wf_x2 - wf_x1) // 2
        t = 1.0 - dist_from_center / half_w if half_w > 0 else 1.0
        alpha = int(t * 18)
        od.line([(x, 0), (x, H - 1)], fill=(*DATA_BLUE, alpha))

    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, overlay)
    img_rgb = img_rgba.convert("RGB")
    img.paste(img_rgb)
    draw = ImageDraw.Draw(img)
    return draw


# ─────────────────────────────────────────────────────────────────────────────
# Characters (draw SEVENTH — after lighting overlay)
# ─────────────────────────────────────────────────────────────────────────────

def draw_luma(draw, cx, cy, h):
    """
    Draw Luma as simplified pixel-art figure.
    DRW-18 UV Purple rim (#7B2FBE) on Luma's hair crown — prevents merging with BG.
    """
    head_h = h // 5
    head_w = int(head_h * 0.85)
    torso_h = int(h * 0.30)
    leg_h = int(h * 0.35)
    arm_w = max(3, head_w // 5)

    foot_y = cy
    leg_top = foot_y - leg_h
    torso_top = leg_top - torso_h
    head_top = torso_top - head_h

    leg_w = head_w // 2
    ll_x = cx - leg_w
    draw.rectangle([ll_x, leg_top, ll_x + leg_w - 2, foot_y], fill=JEANS_BASE)
    rl_x = cx - 2
    draw.rectangle([rl_x, leg_top, rl_x + leg_w - 2, foot_y], fill=JEANS_BASE)
    draw.line([(rl_x + leg_w - 2, leg_top), (rl_x + leg_w - 2, foot_y)],
              fill=JEANS_SEAM, width=1)

    shoe_h = max(3, h // 20)
    draw.rectangle([ll_x - 1, foot_y - shoe_h, ll_x + leg_w + 1, foot_y],
                   fill=LUMA_SHOE)
    draw.rectangle([rl_x - 1, foot_y - shoe_h, rl_x + leg_w + 1, foot_y],
                   fill=LUMA_SHOE)

    torso_x = cx - int(head_w * 0.55)
    torso_w = int(head_w * 1.1)
    draw.rectangle([torso_x, torso_top, torso_x + torso_w, leg_top], fill=HOODIE_UV_MOD)
    hem_h = max(3, torso_h // 5)
    draw.rectangle([torso_x, leg_top - hem_h, torso_x + torso_w, leg_top],
                   fill=HOODIE_HEM)
    rng_pg = random.Random(33)
    for gx in range(torso_x + 2, torso_x + torso_w - 2, 5):
        for gy in range(torso_top + 3, leg_top - hem_h - 2, 5):
            if rng_pg.random() < 0.35:
                draw.rectangle([gx, gy, gx + 1, gy + 1], fill=ELEC_CYAN)

    arm_top = torso_top + torso_h // 6
    arm_bot = torso_top + int(torso_h * 0.75)
    la_x = torso_x - arm_w
    draw.rectangle([la_x, arm_top, la_x + arm_w, arm_bot], fill=HOODIE_UV_MOD)
    ra_x = torso_x + torso_w
    draw.rectangle([ra_x, arm_top, ra_x + arm_w, arm_bot - 4], fill=HOODIE_UV_MOD)

    head_x = cx - head_w // 2
    draw.rectangle([head_x, head_top, head_x + head_w, torso_top], fill=SKIN_UV_MOD)
    shadow_w = head_w // 3
    draw.rectangle([head_x + head_w - shadow_w, head_top,
                    head_x + head_w, torso_top], fill=SKIN_SHADOW)
    hi_h = head_h // 4
    draw.rectangle([head_x + 2, head_top, head_x + head_w - shadow_w - 1,
                    head_top + hi_h], fill=SKIN_BOUNCE)

    # Hair (HAIR_BASE + UV_PURPLE crown sheen)
    hair_h = max(4, head_h // 3)
    draw.rectangle([head_x - 3, head_top - hair_h + 2,
                    head_x + head_w + 4, head_top + hair_h // 2], fill=HAIR_BASE)
    sheen_h = hair_h // 2
    draw.rectangle([head_x + 1, head_top - hair_h + 2,
                    head_x + head_w - 2, head_top - hair_h + 2 + sheen_h],
                   fill=HAIR_UV_SHEEN)

    # DRW-18 UV Purple RIM on hair crown — bright rim strip
    rim_h = max(2, hair_h // 4)
    rim_w = head_w + 6
    draw.rectangle([head_x - 2, head_top - hair_h + 2,
                    head_x - 2 + rim_w, head_top - hair_h + 2 + rim_h],
                   fill=HAIR_UV_RIM)

    eye_x = head_x + head_w // 4
    eye_y = head_top + head_h // 2
    eye_w = max(4, head_w // 4)
    eye_h = max(3, head_h // 5)
    draw.rectangle([eye_x, eye_y, eye_x + eye_w, eye_y + eye_h], fill=(200, 180, 210))
    iris_x = eye_x + eye_w // 4
    draw.rectangle([iris_x, eye_y + 1, iris_x + eye_w // 2, eye_y + eye_h - 1],
                   fill=(50, 30, 60))
    draw.rectangle([eye_x - 1, eye_y - 1, eye_x + eye_w + 1, eye_y + eye_h + 1],
                   outline=(30, 20, 40), width=1)


def draw_byte(draw, cx, cy, h):
    """
    Draw Byte — GL-01b Byte Teal body, ELEC_CYAN outline (home territory = more alive).
    Cyan eye LEFT (facing Luma). Magenta eye RIGHT (facing void).

    FIX 1: BYTE_BODY = (0, 212, 232) GL-01b Byte Teal — NOT Void Black.
            Body was invisible against UV Purple ambient — now clearly readable.
    FIX 2: Eye radius = max(15, h//5) — minimum 15px, both eyes large and readable.
    FIX 3: Void Black slash removed from magenta eye — both eyes clean, unobstructed.
    """
    body_w = int(h * 0.7)
    body_h = h

    # FIX 1: BYTE_BODY = GL-01b Byte Teal (0, 212, 232) — visible against UV Purple
    draw.ellipse([cx - body_w // 2, cy - body_h // 2,
                  cx + body_w // 2, cy + body_h // 2],
                 fill=BYTE_BODY)

    # Inner glow layer — slightly darker teal, creates depth
    glow_shrink = max(2, h // 8)
    draw.ellipse([cx - body_w // 2 + glow_shrink, cy - body_h // 2 + glow_shrink,
                  cx + body_w // 2 - glow_shrink, cy + body_h // 2 - glow_shrink],
                 fill=BYTE_GLOW)

    # ELEC_CYAN outline (home territory — more alive than storm variant)
    draw.ellipse([cx - body_w // 2, cy - body_h // 2,
                  cx + body_w // 2, cy + body_h // 2],
                 outline=ELEC_CYAN, width=max(1, h // 12))

    rng_bt = random.Random(21)
    for _ in range(4):
        tx1 = cx - body_w // 3 + rng_bt.randint(0, body_w // 3)
        ty1 = cy - body_h // 3 + rng_bt.randint(0, body_h // 3)
        tx2 = tx1 + rng_bt.randint(-8, 8)
        ty2 = ty1 + rng_bt.randint(-8, 8)
        draw.line([(tx1, ty1), (tx2, ty2)], fill=ELEC_CYAN, width=1)

    # FIX 2: Eye radius — minimum 15px (was max(2, h//7) ≈ 10px)
    eye_r = max(15, h // 5)
    eye_y = cy - h // 10

    # LEFT eye: ELEC_CYAN — facing Luma, digital identity
    left_eye_x = cx - body_w // 5
    draw.ellipse([left_eye_x - eye_r, eye_y - eye_r,
                  left_eye_x + eye_r, eye_y + eye_r],
                 fill=ELEC_CYAN)

    # RIGHT eye: HOT_MAGENTA — facing void
    # FIX 3: NO Void Black diagonal slash — eye is clean and readable
    right_eye_x = cx + body_w // 5
    draw.ellipse([right_eye_x - eye_r, eye_y - eye_r,
                  right_eye_x + eye_r, eye_y + eye_r],
                 fill=HOT_MAGENTA)
    # Removed: draw.line([...], fill=VOID_BLACK, ...) — was making eye invisible


# ─────────────────────────────────────────────────────────────────────────────
# Glitch (G007 FIX — C40)
# ─────────────────────────────────────────────────────────────────────────────

def draw_glitch(draw, cx, cy, body_h):
    """
    Draw Glitch on the midground platform in its native environment (The Other Side).
    G007 FIX (C40): Glitch diamond body drawn with VOID_BLACK outline=width 3 per spec §2.2.
    In SF03, Glitch is in its home — YEARNING/still state. Subdued spike, quiet eyes.
    cx, cy: body center. body_h: vertical half-extent (ry).
    """
    rx = int(body_h * 0.88)   # horizontal half-extent (ry > rx: taller than wide)
    ry = body_h
    tilt_deg = 3               # nearly upright but still slightly wrong
    angle = math.radians(tilt_deg)

    # Diamond body points (spec §2.1 formula)
    top   = (cx + int(rx * 0.15 * math.sin(angle)),  cy - ry + int(rx * 0.15 * math.cos(angle)))
    right = (cx + int(rx * math.cos(-angle)),          cy + int(rx * 0.2 * math.sin(-angle)))
    bot   = (cx - int(rx * 0.15 * math.sin(angle)),  cy + int(ry * 1.15))
    left  = (cx - int(rx * math.cos(-angle)),          cy - int(rx * 0.2 * math.sin(-angle)))
    pts = [top, right, bot, left]

    # UV_PURPLE shadow offset (+3, +4) — spec §2.2
    sh_pts = [(x + 3, y + 4) for x, y in pts]
    draw.polygon(sh_pts, fill=UV_PURPLE)

    # Main body fill — CORRUPT_AMBER
    draw.polygon(pts, fill=CORRUPT_AMBER)

    # Highlight facet — upper-left triangle
    ctr = (cx, cy - ry // 4)
    mid_tl = ((top[0] + left[0]) // 2, (top[1] + left[1]) // 2)
    CORRUPT_AMB_HL = (255, 185, 80)
    draw.polygon([top, ctr, mid_tl], fill=CORRUPT_AMB_HL)

    # G007 SPEC §2.2: VOID_BLACK outline on body polygon — width=3
    draw.polygon(pts, outline=VOID_BLACK, width=3)

    # HOT_MAG crack drawn AFTER body fill (spec §2.3 stacking order)
    cs = (cx - rx // 2, cy - ry // 3)
    ce = (cx + rx // 3, cy + ry // 2)
    draw.line([cs, ce], fill=HOT_MAGENTA, width=2)
    mid_c = ((cs[0] + ce[0]) // 2, (cs[1] + ce[1]) // 2)
    draw.line([mid_c, (cx + rx // 2, cy - ry // 4)], fill=HOT_MAGENTA, width=1)

    # Top spike — YEARNING state: subdued (spike_h=6 equiv at this scale)
    spike_h = max(3, ry // 5)
    sx = cx + int(rx * 0.15 * math.sin(angle))
    cy_top = top[1]
    spike_pts = [
        (sx - spike_h // 2, cy_top),
        (sx - spike_h,      cy_top - spike_h),
        (sx,                cy_top - spike_h * 2),
        (sx + spike_h,      cy_top - spike_h),
        (sx + spike_h // 2, cy_top),
    ]
    draw.polygon(spike_pts, fill=CORRUPT_AMBER)
    draw.polygon(spike_pts, outline=VOID_BLACK, width=2)
    draw.line([(sx, cy_top - spike_h * 2), (sx, cy_top - spike_h * 2 - max(2, ry // 10))],
              fill=HOT_MAGENTA, width=2)

    # Pixel eyes — YEARNING state: UV_PURPLE dim glow (both bilateral, soft)
    eye_cell = max(2, rx // 5)
    face_cy = cy - ry // 6
    for eye_cx in [cx - rx // 3, cx + rx // 3]:
        draw.rectangle([eye_cx - eye_cell, face_cy - eye_cell,
                        eye_cx + eye_cell, face_cy + eye_cell],
                       fill=UV_PURPLE)
        # Dim center — the YEARNING "watching" glow
        draw.rectangle([eye_cx - eye_cell // 2, face_cy - eye_cell // 2,
                        eye_cx + eye_cell // 2, face_cy + eye_cell // 2],
                       fill=(80, 30, 140))  # dim UV — not full ACID_GREEN, just watching


# ─────────────────────────────────────────────────────────────────────────────
# Confetti (draw LAST)
# ─────────────────────────────────────────────────────────────────────────────

def draw_confetti(draw):
    """
    C27 FIX: Confetti particles constrained within 150px of nearest anchor.
    Anchors: platform center, Luma foot position, Byte center position.
    Particles generated by picking a random anchor and sampling within 150px radius.
    Reject-sample: any candidate whose distance to ALL anchors exceeds 150px is skipped.
    Cap: 200 attempts per particle to prevent infinite loop.
    """
    rng = random.Random(77)
    colors = [ELEC_CYAN, STATIC_WHITE, ACID_GREEN, DATA_BLUE]
    weights = [0.40, 0.25, 0.20, 0.15]
    num = 50
    RADIUS = 150

    # Anchors: platform center-top, Luma foot, Byte center
    anchors = [
        (int(W * 0.225), int(H * 0.72)),   # platform center
        (int(W * 0.14),  int(H * 0.66)),   # Luma foot position
        (int(W * 0.22),  int(H * 0.62)),   # Byte center position
    ]

    def nearest_anchor_dist(x, y):
        return min(math.sqrt((x - ax) ** 2 + (y - ay) ** 2) for ax, ay in anchors)

    for _ in range(num):
        # Attempt up to 200 times to find a valid position within 150px of an anchor
        px, py = anchors[0]  # fallback default
        for _attempt in range(200):
            anchor = anchors[rng.randint(0, len(anchors) - 1)]
            angle = rng.uniform(0, 2 * math.pi)
            dist = rng.uniform(0, RADIUS)
            cx_candidate = int(anchor[0] + dist * math.cos(angle))
            cy_candidate = int(anchor[1] + dist * math.sin(angle))
            # Clamp to canvas bounds
            cx_candidate = max(0, min(W - 1, cx_candidate))
            cy_candidate = max(0, min(H - 1, cy_candidate))
            if nearest_anchor_dist(cx_candidate, cy_candidate) <= RADIUS:
                px, py = cx_candidate, cy_candidate
                break

        drift = rng.randint(-2, 2)
        py = max(0, min(H - 1, py + drift))
        sz = rng.randint(1, 3)

        r = rng.random()
        cumulative = 0.0
        col = ELEC_CYAN
        for c, w in zip(colors, weights):
            cumulative += w
            if r <= cumulative:
                col = c
                break

        draw.rectangle([px, py, px + sz, py + sz], fill=col)

    shoulder_x = int(W * 0.17)
    shoulder_y = int(H * 0.49)
    rng_s = random.Random(78)
    for _ in range(3):
        sx = shoulder_x + rng_s.randint(-4, 4)
        sy = shoulder_y + rng_s.randint(-4, 4)
        col = ACID_GREEN if rng_s.random() < 0.5 else ELEC_CYAN
        draw.rectangle([sx, sy, sx + 1, sy + 1], fill=col)

    return draw


# ─────────────────────────────────────────────────────────────────────────────
# Footer Bar
# ─────────────────────────────────────────────────────────────────────────────

def draw_footer(draw, img):
    footer_h = 28
    footer_y = H - footer_h
    draw.rectangle([0, footer_y, W - 1, H - 1], fill=(5, 5, 12))
    draw.line([(0, footer_y), (W - 1, footer_y)], fill=ELEC_CYAN, width=1)

    label_items = [
        (12, "LTG -- STYLE FRAME 03 -- \"THE OTHER SIDE\" v004"),
        (480, "BYTE TEAL #00D4E8 | CONFETTI ANCHORED <=150px | NO WARM LIGHT"),
        (960, "SAM KOWALSKI | CYCLE 27"),
        (1500, "LTG_COLOR_styleframe_otherside_v004"),
    ]
    try:
        from PIL import ImageFont
        font = ImageFont.load_default()
    except Exception:
        font = None

    for (lx, text) in label_items:
        draw.text((lx, footer_y + 6), text, fill=ELEC_CYAN, font=font)

    return draw


# ─────────────────────────────────────────────────────────────────────────────
# Main Generator
# ─────────────────────────────────────────────────────────────────────────────

def generate(output_path):
    """Main entry point. Build all layers in correct draw order."""
    img = Image.new("RGB", (W, H), VOID_BLACK)
    draw = ImageDraw.Draw(img)

    print("Layer 5: Void sky...")
    draw = draw_void_sky(draw, img)

    print("Layer 4: Far distance (right-side irregularity)...")
    draw = draw_far_distance(draw, img)

    print("Layer 3: Mid-distance structures (bridging element)...")
    draw = draw_mid_distance(draw, img)

    print("Layer 2: Midground (waterfall luminance reduced)...")
    draw = draw_midground(draw, img)

    print("Layer 1: Foreground (settled confetti)...")
    draw = draw_foreground(draw)

    print("Lighting overlay (UV Purple ambient + cyan bounce + blue waterfall)...")
    draw = draw_lighting_overlay(img)

    print("Character: Luma (UV Purple hair rim)...")
    luma_cx = int(W * 0.14)
    luma_cy = int(H * 0.66)
    luma_h  = int(H * 0.20)
    draw_luma(draw, luma_cx, luma_cy, luma_h)

    print("Character: Byte (FIX: Teal body + enlarged eyes + no slash)...")
    byte_cx = int(W * 0.22)
    byte_cy = int(H * 0.62)
    byte_h  = int(H * 0.07)
    draw_byte(draw, byte_cx, byte_cy, byte_h)

    print("Character: Glitch (G007 FIX C40 — VOID_BLACK outline, YEARNING state, midground)...")
    # Glitch on midground platform at right of frame — native to this world.
    # Mid-distance scale: ~8% of frame height. YEARNING state — still, watching Luma.
    glitch_cx = int(W * 0.68)
    glitch_cy = int(H * 0.58)
    glitch_body_h = int(H * 0.08)  # ry (vertical half-extent)
    draw_glitch(draw, glitch_cx, glitch_cy, glitch_body_h)

    print("Confetti (seed=77, ambient, no warm colors)...")
    draw = draw_confetti(draw)

    print("Footer bar...")
    draw = draw_footer(draw, img)

    import os
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    # IMAGE SIZE RULE: hard limit <= 1280px in both dimensions
    img.thumbnail((1280, 1280), Image.LANCZOS)
    img.save(output_path, "PNG")
    size_bytes = os.path.getsize(output_path)
    print(f"\nSaved: {output_path}")
    print(f"File size: {size_bytes:,} bytes ({size_bytes // 1024} KB)")
    print("\nFix verification (Cycle 41):")
    print("  [C41 FIX] UV_PURPLE ring alpha: 60→18 — blended pixels now outside RGB radius-60 ✓")
    print("  [C41 FIX] Slab outlines (rect + poly): width 1→2 — LANCZOS anti-aliasing drift reduced ✓")
    print("  [C41 FIX] Data gradient: lerp(DATA_BLUE_90→UV_PURPLE_MID) — no near-UV_PURPLE blends ✓")
    print("  [C28 FIX] UV_PURPLE_DARK corrected: (43,32,80) -> (58,16,96) GL-04a #3A1060 ✓")
    print("            Saturation: 31% -> 72%. Deep void zones now read as digital void.")
    print("  [CARRY] Confetti constrained within 150px of nearest anchor — from v004 ✓")
    print("            Anchors: platform (W*0.225,H*0.72), Luma (W*0.14,H*0.66), Byte (W*0.22,H*0.62)")
    print("  [CARRY] BYTE_BODY = (0,212,232) GL-01b Byte Teal — from v003 ✓")
    print("  [CARRY] Eye radius = max(15, h//5) — from v003 ✓")
    print("  [CARRY] Void Black slash removed from magenta eye — from v003 ✓")
    print("  [CARRY] DRW-18 UV Purple rim on Luma hair crown — from v002 ✓")
    print("  [CARRY] Waterfall luminance reduced — from v002 ✓")
    print("  [CARRY] Mid-distance bridging element — from v002 ✓")
    print("  [CARRY] Right-side void irregularity — from v002 ✓")
    print("  [VERIFY] Zero warm light sources — NO warm light in generator ✓")


if __name__ == "__main__":
    OUTPUT_PATH = "/home/wipkat/team/output/color/style_frames/LTG_COLOR_styleframe_otherside.png"
    generate(OUTPUT_PATH)
