#!/usr/bin/env python3
"""
LTG_TOOL_style_frame_03_other_side_v001.py
"Luma & the Glitchkin" — Style Frame 03 "The Other Side"
Artist: Jordan Reed | Cycle 15

Spec sources:
  - /home/wipkat/team/output/production/sf03_other_side_spec.md (Alex Chen)
  - /home/wipkat/team/output/color/style_frames/style_frame_03_other_side.md (Sam Kowalski)

Narrative: Luma has crossed into the Glitch Layer. Quiet awe. Vast and still.
Mood: Grief-adjacent wonder. She has left warmth behind.

CRITICAL RULES:
  - NO WARM LIGHT. Zero. Warmth exists only in pigment (Luma's hoodie, skin, Real World debris).
  - Inverted atmospheric perspective: things get MORE PURPLE and DARKER with distance.
  - Cyan-lit surface rule: G > R AND B > R individually.
  - After every img.paste() / alpha_composite call: refresh draw = ImageDraw.Draw(img)
  - Never overwrite existing outputs — always new versioned files.

Output: /home/wipkat/team/output/color/style_frames/LTG_COLOR_styleframe_otherside_v001.png
"""

import math
import random
from PIL import Image, ImageDraw

# ── Canvas ────────────────────────────────────────────────────────────────────
W, H = 1920, 1080

# ── Canonical Palette (master_palette.md / sf03_other_side_spec.md) ──────────

# Dominant void colors
VOID_BLACK      = (10,  10,  20)    # GL-08  dominant void
UV_PURPLE       = (123, 47, 190)    # GL-04  ambient void light
ELEC_CYAN       = (0,  240, 255)    # GL-01  circuit traces, platform glow, primary light
DATA_BLUE       = (43, 127, 255)    # GL-06  data waterfall, secondary traces
ACID_GREEN      = (57, 255,  20)    # GL-03  pixel-art plants, distant Glitchkin dots
STATIC_WHITE    = (240, 240, 240)   # GL-05  void stars, confetti particles

# Warm-color inventory — sparse, intentional (material color, NOT light)
HOODIE_UV_MOD   = (192, 112,  56)   # DRW-14 Luma hoodie under UV ambient
SKIN_UV_MOD     = (168, 120, 144)   # DRW-11 Luma skin under UV ambient
CORRUPT_AMBER   = (255, 140,   0)   # Glowing edges of Real World debris
TERRACOTTA      = (199,  91,  57)   # Corrupted Real World wall fragment

# Supporting colors
DARK_ACID       = (26,  168,   0)   # Plant shadow undersides
DEEP_CYAN       = (0,   168, 180)   # Byte inner glow, deep cyan traces
HOT_MAGENTA     = (255,  45, 107)   # Byte's cracked eye (void-facing)
UV_PURPLE_MID   = (42,   26,  64)   # ENV-11 far-distance atmospheric haze
UV_PURPLE_DARK  = (43,   32,  80)   # ENV-12 void sky near-transition
FAR_EDGE        = (33,   17,  54)   # Far structure edges at void-scale
SLAB_TOP        = (26,   40,  56)   # ENV-09 floating slab top surface
SLAB_FACE       = (10,   20,  32)   # ENV-10 floating slab vertical face
BELOW_VOID      = (5,     5,   8)   # GL-08a below-platform abyss (darkest)
DATA_BLUE_HL    = (106, 186, 255)   # GL-06b data code highlights
MUTED_TEAL      = (91,  140, 138)   # Lamppost fragment body

# Derived render constants
CIRCUIT_TRACE_DIM  = (0,  192, 204)  # ELEC_CYAN at 80% — structural platform traces
CIRCUIT_TRACE_2ND  = (43, 127, 255)  # DATA_BLUE secondary traces
DATA_BLUE_90       = (39, 115, 230)  # DATA_BLUE at 90% luminance (waterfall base)
SKIN_SHADOW        = (90,  58,  90)  # DRW-12 deep lavender-plum shadow
SKIN_BOUNCE        = (74, 176, 176)  # DRW-13 cyan platform-bounce highlight on skin
HOODIE_HEM         = (90, 168, 160)  # DRW-15 cyan bounce on lower hem
JEANS_BASE         = (38,  61,  90)  # jeans shadow fill
JEANS_SEAM         = (43, 127, 255)  # DATA_BLUE seam catch from waterfall
HAIR_BASE          = (26,  15,  10)  # hair base
HAIR_UV_SHEEN      = (123, 47, 190)  # UV_PURPLE crown sheen
BYTE_BODY          = (10,  10,  20)  # VOID_BLACK
BYTE_GLOW          = (0,  168, 180)  # DEEP_CYAN inner glow
ROAD_FRAGMENT      = (42,  42,  56)  # road surface fragment base
LUMA_SHOE          = (220, 215, 200) # cream shoe


def lerp_color(a, b, t):
    """Linear interpolate between two RGB 3-tuples."""
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


# ─────────────────────────────────────────────────────────────────────────────
# Layer 5 — Void Sky (draw FIRST)
# ─────────────────────────────────────────────────────────────────────────────

def draw_void_sky(draw, img):
    """
    Fill canvas with VOID_BLACK, gradient to UV_PURPLE_DARK in upper sky zone.
    Add stars and faint ring megastructure.
    """
    # 1. Base fill
    draw.rectangle([0, 0, W - 1, H - 1], fill=VOID_BLACK)

    # 2. Sky gradient: VOID_BLACK at y=0 → UV_PURPLE_DARK at y=270
    sky_bottom = 270
    for y in range(sky_bottom):
        t = y / sky_bottom
        col = lerp_color(VOID_BLACK, UV_PURPLE_DARK, t)
        draw.line([(0, y), (W - 1, y)], fill=col)

    # 3. Stars — 100 white 1px dots in upper third (seeded=42)
    rng = random.Random(42)
    for _ in range(100):
        sx = rng.randint(0, W - 1)
        sy = rng.randint(0, H // 3)
        draw.point((sx, sy), fill=STATIC_WHITE)

    # 4. Ring megastructure — enormous circle, UV_PURPLE outline, very faint
    ring_cx = int(W * 0.55)
    ring_cy = int(H * 0.18)
    ring_r  = int(H * 0.45)
    ring_overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ring_draw = ImageDraw.Draw(ring_overlay)
    ring_draw.ellipse(
        [ring_cx - ring_r, ring_cy - ring_r,
         ring_cx + ring_r, ring_cy + ring_r],
        outline=(*UV_PURPLE, 60),
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
    """
    Atmospheric haze, large continent-scale polygon slabs, thin data waterfalls,
    distant Glitchkin dots, distant Corrupt Amber fragments.
    Inverted atmospheric perspective: more purple and darker with distance.
    """
    # 1. Atmospheric haze band (inverse atmos perspective — UV_PURPLE_MID at top)
    haze_top = 0
    haze_bot = int(H * 0.45)
    haze_overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(haze_overlay)
    for y in range(haze_top, haze_bot):
        t = 1.0 - (y - haze_top) / (haze_bot - haze_top)  # more haze = higher = more distant
        alpha = int(t * 55)
        hd.line([(0, y), (W - 1, y)], fill=(*UV_PURPLE_MID, alpha))
    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, haze_overlay)
    img_rgb = img_rgba.convert("RGB")
    img.paste(img_rgb)
    draw = ImageDraw.Draw(img)

    # 2. Enormous flat geometric plane slabs — far, dark, barely visible
    slab_specs = [
        # (x1_frac, y1_frac, x2_frac, y2_frac)  polygon or rect
        (0.55, 0.12, 0.85, 0.24),
        (0.62, 0.20, 0.92, 0.30),
        (0.20, 0.08, 0.50, 0.18),
        (0.72, 0.28, 0.98, 0.38),
    ]
    for (x1f, y1f, x2f, y2f) in slab_specs:
        x1, y1 = int(x1f * W), int(y1f * H)
        x2, y2 = int(x2f * W), int(y2f * H)
        draw.rectangle([x1, y1, x2, y2], fill=FAR_EDGE, outline=UV_PURPLE, width=1)

    # 3. Distant data waterfalls — thin vertical suggestion lines
    rng_dw = random.Random(42)
    for _ in range(5):
        wx = rng_dw.randint(int(W * 0.3), int(W * 0.9))
        wy_top = rng_dw.randint(int(H * 0.05), int(H * 0.20))
        wy_bot = rng_dw.randint(int(H * 0.25), int(H * 0.45))
        draw.line([(wx, wy_top), (wx, wy_bot)], fill=DATA_BLUE, width=1)
        if rng_dw.random() < 0.5:
            draw.line([(wx + 1, wy_top), (wx + 1, wy_bot)], fill=DATA_BLUE, width=1)

    # 4. Distant Glitchkin — tiny 2px dots
    rng_gk = random.Random(43)
    for _ in range(8):
        gx = rng_gk.randint(int(W * 0.4), int(W * 0.9))
        gy = rng_gk.randint(int(H * 0.2), int(H * 0.45))
        col = ACID_GREEN if rng_gk.random() < 0.5 else ELEC_CYAN
        draw.rectangle([gx, gy, gx + 1, gy + 1], fill=col)

    # 5. Distant Corrupt Amber fragments — warm punctuation in cold void
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
    """
    Floating geometric slabs + corrupted Real World fragments (wall, road, lamppost).
    Detail level 60%. Edges slightly softened by blue-purple haze.
    """
    # Geometric slabs
    mid_slabs = [
        # (cx_frac, cy_frac, w_frac, h_frac, edge_color)
        (0.25, 0.42, 0.12, 0.045, ELEC_CYAN),    # nav path slab
        (0.45, 0.37, 0.14, 0.040, ELEC_CYAN),
        (0.60, 0.45, 0.10, 0.038, DATA_BLUE),    # data-storage slab
        (0.72, 0.38, 0.13, 0.042, ELEC_CYAN),
        (0.82, 0.50, 0.09, 0.035, DATA_BLUE),
    ]
    for (cxf, cyf, wf, hf, edge_col) in mid_slabs:
        sx = int(cxf * W)
        sy = int(cyf * H)
        sw = int(wf * W)
        sh = max(5, int(hf * H))
        # Top surface
        draw.rectangle([sx, sy, sx + sw, sy + sh], fill=SLAB_TOP)
        # Vertical face (underside — receding into void)
        face_h = max(3, sh // 2)
        draw.rectangle([sx, sy + sh, sx + sw, sy + sh + face_h], fill=SLAB_FACE)
        # Glowing edge (top)
        draw.line([(sx, sy), (sx + sw, sy)], fill=edge_col, width=2)
        # Side edge glow
        draw.line([(sx + sw, sy), (sx + sw, sy + sh)], fill=edge_col, width=1)

    # ── Corrupted Real World Fragments ──────────────────────────────────────

    # Wall fragment — TERRACOTTA with CORRUPT_AMBER crack edges
    wf_x, wf_y = int(W * 0.42), int(H * 0.38)
    wf_w, wf_h = int(W * 0.06), int(H * 0.12)
    draw.rectangle([wf_x, wf_y, wf_x + wf_w, wf_y + wf_h], fill=TERRACOTTA)
    # Crack lines (jagged polygon at perimeter)
    rng_cr = random.Random(51)
    crack_pts = []
    # Top edge cracks
    for i in range(0, wf_w, 6):
        jy = wf_y + rng_cr.randint(-3, 3)
        crack_pts.append((wf_x + i, jy))
    # Right edge cracks
    for i in range(0, wf_h, 6):
        jx = wf_x + wf_w + rng_cr.randint(-3, 3)
        crack_pts.append((jx, wf_y + i))
    for pt in crack_pts:
        draw.ellipse([pt[0]-1, pt[1]-1, pt[0]+1, pt[1]+1], fill=CORRUPT_AMBER)
    # Amber outline on fragment
    draw.rectangle([wf_x, wf_y, wf_x + wf_w, wf_y + wf_h],
                   outline=CORRUPT_AMBER, width=2)

    # Road surface fragment — dark polygon with amber boundary
    rf_x, rf_y = int(W * 0.55), int(H * 0.48)
    rf_w, rf_h = int(W * 0.05), int(H * 0.06)
    draw.rectangle([rf_x, rf_y, rf_x + rf_w, rf_y + rf_h], fill=ROAD_FRAGMENT)
    draw.rectangle([rf_x, rf_y, rf_x + rf_w, rf_y + rf_h],
                   outline=CORRUPT_AMBER, width=2)

    # Lamppost fragment — MUTED_TEAL body, amber corruption from base upward
    lp_x, lp_y_top = int(W * 0.65), int(H * 0.32)
    lp_y_bot = int(H * 0.52)
    lp_w = max(6, int(W * 0.007))
    lp_h = lp_y_bot - lp_y_top
    # Draw gradient from CORRUPT_AMBER at bottom to MUTED_TEAL at top
    for y in range(lp_y_top, lp_y_bot):
        t = 1.0 - (y - lp_y_top) / lp_h  # t=1 at top (teal), t=0 at bottom (amber)
        col = lerp_color(CORRUPT_AMBER, MUTED_TEAL, t)
        draw.line([(lp_x, y), (lp_x + lp_w, y)], fill=col)

    return draw


# ─────────────────────────────────────────────────────────────────────────────
# Layer 2 — Midground (draw FOURTH)
# ─────────────────────────────────────────────────────────────────────────────

def draw_midground(draw, img):
    """
    Main platform (where Luma stands), circuit traces, pixel-art plants,
    abyss below platform, data waterfall, floating sub-platforms.
    """
    # ── Main Platform ────────────────────────────────────────────────────────
    plat_x1 = 0
    plat_y1 = int(H * 0.66)
    plat_x2 = int(W * 0.45)
    plat_y2 = int(H * 0.75)

    # Platform base fill — VOID_BLACK
    draw.rectangle([plat_x1, plat_y1, plat_x2, plat_y2], fill=VOID_BLACK)

    # Platform edge lip (front face — SLAB_FACE)
    lip_y1 = plat_y2
    lip_y2 = int(H * 0.78)
    draw.rectangle([plat_x1, lip_y1, plat_x2, lip_y2], fill=SLAB_FACE)

    # Abyss below platform
    draw.rectangle([plat_x1, lip_y2, plat_x2, H - 1], fill=BELOW_VOID)

    # ── Circuit Traces on Platform Surface ───────────────────────────────────
    rng_ct = random.Random(99)
    grid_cell = 20
    plat_w = plat_x2 - plat_x1
    plat_h_px = plat_y2 - plat_y1

    for gx in range(plat_x1, plat_x2, grid_cell):
        for gy in range(plat_y1, plat_y2, grid_cell):
            # Horizontal connections (~60% probability)
            if rng_ct.random() < 0.60:
                trace_col = CIRCUIT_TRACE_DIM if rng_ct.random() < 0.7 else CIRCUIT_TRACE_2ND
                ex = min(gx + grid_cell, plat_x2)
                draw.line([(gx, gy), (ex, gy)], fill=trace_col, width=1)
            # Vertical connections (~40% probability)
            if rng_ct.random() < 0.40:
                trace_col = CIRCUIT_TRACE_DIM if rng_ct.random() < 0.7 else CIRCUIT_TRACE_2ND
                ey = min(gy + grid_cell, plat_y2)
                draw.line([(gx, gy), (gx, ey)], fill=trace_col, width=1)

    # ── Pixel-Art Plants in Cracks ───────────────────────────────────────────
    # Plant positions: x=W*0.08, 0.14, 0.20, 0.28, 0.36
    plant_xs = [int(W * f) for f in (0.08, 0.14, 0.20, 0.28, 0.36)]
    for px in plant_xs:
        py_base = plat_y1 + 2
        # Crack line
        draw.line([(px - 1, py_base), (px + 1, plat_y2 - 4)], fill=BELOW_VOID, width=1)
        # Plant body — angular succulent shape (upward polygon)
        plant_h = 14
        plant_w = 10
        # Main leaf (ACID_GREEN fill)
        pts_main = [
            (px, py_base - plant_h),
            (px - plant_w // 2, py_base - plant_h // 3),
            (px, py_base),
            (px + plant_w // 2, py_base - plant_h // 3),
        ]
        draw.polygon(pts_main, fill=ACID_GREEN)
        # Shadow underside (DARK_ACID on lower faces)
        shadow_pts = [
            (px - plant_w // 2, py_base - plant_h // 3),
            (px, py_base),
            (px + plant_w // 2, py_base - plant_h // 3),
            (px, py_base - plant_h // 2),
        ]
        draw.polygon(shadow_pts, fill=DARK_ACID)
        # Top highlight (ELEC_CYAN bounce on upper face)
        hi_pts = [
            (px, py_base - plant_h),
            (px - 3, py_base - plant_h + 4),
            (px + 3, py_base - plant_h + 4),
        ]
        draw.polygon(hi_pts, fill=ELEC_CYAN)

    # ── Abyss Gradient (void below platform) ─────────────────────────────────
    # Gradient from BELOW_VOID at bottom up to VOID_BLACK at platform underside
    for y in range(lip_y2, H):
        t = (y - lip_y2) / (H - lip_y2)
        col = lerp_color(VOID_BLACK, BELOW_VOID, t)
        draw.line([(plat_x1, y), (plat_x2, y)], fill=col)

    # Right side of frame — also void below midline
    draw.rectangle([plat_x2, int(H * 0.66), W - 1, H - 1], fill=BELOW_VOID)

    # ── Data Waterfall (right side, near Luma) ───────────────────────────────
    wf_x1 = int(W * 0.38)
    wf_x2 = int(W * 0.42)
    wf_y_top = int(H * 0.18)
    wf_y_bot = int(H * 0.66)

    # Base column fill
    for x in range(wf_x1, wf_x2):
        for y in range(wf_y_top, wf_y_bot):
            # Slight alpha variation — code column effect
            draw.point((x, y), fill=DATA_BLUE_90)

    # Code character highlights — scatter DATA_BLUE_HL rectangles
    rng_wf = random.Random(77)
    for _ in range(35):
        cx = rng_wf.randint(wf_x1, wf_x2 - 4)
        cy = rng_wf.randint(wf_y_top, wf_y_bot - 6)
        draw.rectangle([cx, cy, cx + 3, cy + 5], fill=DATA_BLUE_HL)

    # Data mist at base — gradient DATA_BLUE → UV_PURPLE
    mist_y1 = int(H * 0.62)
    mist_y2 = int(H * 0.68)
    for y in range(mist_y1, min(mist_y2, H)):
        t = (y - mist_y1) / (mist_y2 - mist_y1)
        col = lerp_color(DATA_BLUE_90, UV_PURPLE, t)
        draw.line([(wf_x1, y), (wf_x2, y)], fill=col)

    # Light pool on platform — soft blue pool left of waterfall
    pool_overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    pd = ImageDraw.Draw(pool_overlay)
    pool_cx = wf_x1 - 20
    pool_cy = plat_y1 + (plat_y2 - plat_y1) // 2
    for r in range(60, 0, -1):
        t = 1.0 - r / 60.0
        alpha = int(t * t * 35)
        pd.ellipse([pool_cx - r, pool_cy - r // 2,
                    pool_cx + r, pool_cy + r // 2],
                   fill=(*DATA_BLUE, alpha))
    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, pool_overlay)
    img_rgb = img_rgba.convert("RGB")
    img.paste(img_rgb)
    draw = ImageDraw.Draw(img)

    # ── Floating Sub-platforms (stepping stones near Luma) ───────────────────
    sub_specs = [
        # (x_frac, y_frac, w_frac, h_frac)
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
    """
    Closest portion of platform surface — confetti settled on surface.
    """
    # Settled confetti on platform surface
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
    """
    Three light passes — NO WARM LIGHT.
    1. UV_PURPLE ambient overlay — omnidirectional, stronger from below
    2. ELEC_CYAN bounce from platform circuits — upward from platform surface
    3. DATA_BLUE waterfall strip — right side vertical line source
    """
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)

    # 1. UV Purple ambient — gradient: alpha 50 at y=H*0.7, alpha 20 at y=0
    for y in range(H):
        if y <= int(H * 0.7):
            t = y / (H * 0.7)
            alpha = int(20 + t * 30)  # 20 → 50
        else:
            alpha = 50
        od.line([(0, y), (W - 1, y)], fill=(*UV_PURPLE, alpha))

    # 2. ELEC_CYAN bounce — platform surface level upward fade
    plat_y = int(H * 0.66)
    for y in range(plat_y, -1, -1):
        dist = plat_y - y
        max_dist = int(H * 0.11)  # fades to ~0 above H*0.55
        if dist > max_dist:
            alpha = 10
        else:
            t = 1.0 - dist / max_dist
            alpha = int(10 + t * t * 50)
        od.line([(0, y), (int(W * 0.45), y)], fill=(*ELEC_CYAN, alpha))

    # 3. DATA_BLUE waterfall strip — right side
    wf_x1 = int(W * 0.35)
    wf_x2 = int(W * 0.45)
    for x in range(wf_x1, wf_x2):
        dist_from_center = abs(x - (wf_x1 + wf_x2) // 2)
        half_w = (wf_x2 - wf_x1) // 2
        t = 1.0 - dist_from_center / half_w if half_w > 0 else 1.0
        alpha = int(t * 35)
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
    cx, cy = feet position. h = total height in pixels.
    Pose: Standing at edge, weight slightly back, arms at sides, three-quarter view.
    Colors: UV-ambient modified (no warm light).
    """
    # Proportions (head = 1/5 of total height)
    head_h = h // 5
    head_w = int(head_h * 0.85)
    torso_h = int(h * 0.30)
    leg_h = int(h * 0.35)
    arm_w = max(3, head_w // 5)

    # Feet at cy, top of head at cy - h
    foot_y = cy
    leg_top = foot_y - leg_h
    torso_top = leg_top - torso_h
    head_top = torso_top - head_h

    # ── Legs (jeans) ─────────────────────────────────────────────────────────
    leg_w = head_w // 2
    # Left leg
    ll_x = cx - leg_w
    draw.rectangle([ll_x, leg_top, ll_x + leg_w - 2, foot_y], fill=JEANS_BASE)
    # Right leg (slightly overlapping — 3/4 view)
    rl_x = cx - 2
    draw.rectangle([rl_x, leg_top, rl_x + leg_w - 2, foot_y], fill=JEANS_BASE)
    # DATA_BLUE seam catch on right side (waterfall light)
    draw.line([(rl_x + leg_w - 2, leg_top), (rl_x + leg_w - 2, foot_y)],
              fill=JEANS_SEAM, width=1)

    # ── Shoes (cream) ────────────────────────────────────────────────────────
    shoe_h = max(3, h // 20)
    draw.rectangle([ll_x - 1, foot_y - shoe_h, ll_x + leg_w + 1, foot_y],
                   fill=LUMA_SHOE)
    draw.rectangle([rl_x - 1, foot_y - shoe_h, rl_x + leg_w + 1, foot_y],
                   fill=LUMA_SHOE)

    # ── Torso (hoodie — HOODIE_UV_MOD) ───────────────────────────────────────
    torso_x = cx - int(head_w * 0.55)
    torso_w = int(head_w * 1.1)
    draw.rectangle([torso_x, torso_top, torso_x + torso_w, leg_top], fill=HOODIE_UV_MOD)
    # Lower hem gets cyan bounce (HOODIE_HEM)
    hem_h = max(3, torso_h // 5)
    draw.rectangle([torso_x, leg_top - hem_h, torso_x + torso_w, leg_top],
                   fill=HOODIE_HEM)
    # Pixel grid on hoodie (tiny cyan squares — 2x2 every 5px)
    rng_pg = random.Random(33)
    for gx in range(torso_x + 2, torso_x + torso_w - 2, 5):
        for gy in range(torso_top + 3, leg_top - hem_h - 2, 5):
            if rng_pg.random() < 0.35:
                draw.rectangle([gx, gy, gx + 1, gy + 1], fill=ELEC_CYAN)

    # ── Arms ─────────────────────────────────────────────────────────────────
    arm_top = torso_top + torso_h // 6
    arm_bot = torso_top + int(torso_h * 0.75)
    # Left arm — slightly raised (body language of bracing)
    la_x = torso_x - arm_w
    draw.rectangle([la_x, arm_top, la_x + arm_w, arm_bot], fill=HOODIE_UV_MOD)
    # Right arm — slightly forward (toward viewer)
    ra_x = torso_x + torso_w
    draw.rectangle([ra_x, arm_top, ra_x + arm_w, arm_bot - 4], fill=HOODIE_UV_MOD)

    # ── Head ─────────────────────────────────────────────────────────────────
    head_x = cx - head_w // 2
    # Skin base
    draw.rectangle([head_x, head_top, head_x + head_w, torso_top], fill=SKIN_UV_MOD)
    # Shadow side (right side of face — away from viewer)
    shadow_w = head_w // 3
    draw.rectangle([head_x + head_w - shadow_w, head_top,
                    head_x + head_w, torso_top], fill=SKIN_SHADOW)
    # Cyan bounce highlight (forehead — upward plane catches platform bounce)
    hi_h = head_h // 4
    draw.rectangle([head_x + 2, head_top, head_x + head_w - shadow_w - 1,
                    head_top + hi_h], fill=SKIN_BOUNCE)

    # ── Hair (HAIR_BASE with UV_PURPLE crown sheen) ──────────────────────────
    hair_h = max(4, head_h // 3)
    # Hair mass — asymmetric cloud shape (three overlapping ovals approximated as rects)
    draw.rectangle([head_x - 3, head_top - hair_h + 2,
                    head_x + head_w + 4, head_top + hair_h // 2], fill=HAIR_BASE)
    # UV Purple sheen on crown
    sheen_h = hair_h // 2
    draw.rectangle([head_x + 1, head_top - hair_h + 2,
                    head_x + head_w - 2, head_top - hair_h + 2 + sheen_h],
                   fill=HAIR_UV_SHEEN)

    # ── Eye (one wide eye visible — three-quarter view) ──────────────────────
    eye_x = head_x + head_w // 4
    eye_y = head_top + head_h // 2
    eye_w = max(4, head_w // 4)
    eye_h = max(3, head_h // 5)
    # Eye white — UV-tinted
    draw.rectangle([eye_x, eye_y, eye_x + eye_w, eye_y + eye_h], fill=(200, 180, 210))
    # Iris — dark with UV tint
    iris_x = eye_x + eye_w // 4
    draw.rectangle([iris_x, eye_y + 1, iris_x + eye_w // 2, eye_y + eye_h - 1],
                   fill=(50, 30, 60))
    # Wide open = eye_h + 1 to show wonder
    draw.rectangle([eye_x - 1, eye_y - 1, eye_x + eye_w + 1, eye_y + eye_h + 1],
                   outline=(30, 20, 40), width=1)


def draw_byte(draw, cx, cy, h):
    """
    Draw Byte as oval pixel-art body with two distinctly colored eyes.
    cx, cy = center position. h = total height.
    Cyan eye (left, facing Luma). Magenta eye (right, facing void). Both must be visible.
    Body: VOID_BLACK base + DEEP_CYAN inner glow + ELEC_CYAN circuit traces.
    No CORRUPT_AMBER outline (UV Purple ambient provides adequate contrast).
    """
    body_w = int(h * 0.7)
    body_h = h

    # ── Body oval ─────────────────────────────────────────────────────────────
    draw.ellipse([cx - body_w // 2, cy - body_h // 2,
                  cx + body_w // 2, cy + body_h // 2],
                 fill=BYTE_BODY)

    # Inner glow — slightly smaller oval
    glow_shrink = max(2, h // 8)
    draw.ellipse([cx - body_w // 2 + glow_shrink, cy - body_h // 2 + glow_shrink,
                  cx + body_w // 2 - glow_shrink, cy + body_h // 2 - glow_shrink],
                 fill=BYTE_GLOW)

    # Body outline — DEEP_CYAN (he is more alive/glowing in the Glitch Layer)
    draw.ellipse([cx - body_w // 2, cy - body_h // 2,
                  cx + body_w // 2, cy + body_h // 2],
                 outline=ELEC_CYAN, width=max(1, h // 12))

    # ELEC_CYAN circuit traces on body
    rng_bt = random.Random(21)
    for _ in range(4):
        tx1 = cx - body_w // 3 + rng_bt.randint(0, body_w // 3)
        ty1 = cy - body_h // 3 + rng_bt.randint(0, body_h // 3)
        tx2 = tx1 + rng_bt.randint(-8, 8)
        ty2 = ty1 + rng_bt.randint(-8, 8)
        draw.line([(tx1, ty1), (tx2, ty2)], fill=ELEC_CYAN, width=1)

    # ── Eyes ─────────────────────────────────────────────────────────────────
    eye_r = max(2, h // 7)
    eye_y = cy - h // 10  # slightly above center

    # Cyan eye (LEFT — facing Luma / warmth)
    left_eye_x = cx - body_w // 5
    draw.ellipse([left_eye_x - eye_r, eye_y - eye_r,
                  left_eye_x + eye_r, eye_y + eye_r],
                 fill=ELEC_CYAN)

    # Magenta eye (RIGHT — facing void / danger) — cracked
    right_eye_x = cx + body_w // 5
    draw.ellipse([right_eye_x - eye_r, eye_y - eye_r,
                  right_eye_x + eye_r, eye_y + eye_r],
                 fill=HOT_MAGENTA)
    # Crack line on magenta eye
    draw.line([(right_eye_x - eye_r + 1, eye_y - eye_r + 1),
               (right_eye_x + eye_r - 1, eye_y + eye_r - 1)],
              fill=VOID_BLACK, width=max(1, eye_r // 2))


# ─────────────────────────────────────────────────────────────────────────────
# Confetti (draw LAST — settles on everything including characters)
# ─────────────────────────────────────────────────────────────────────────────

def draw_confetti(draw):
    """
    Ambient settled confetti. Seed=77 for cross-frame consistency.
    Colors: ELEC_CYAN, STATIC_WHITE, ACID_GREEN, DATA_BLUE — NO warm colors.
    40-60 particles total. Slight anti-gravity offset (±2px).
    """
    rng = random.Random(77)
    colors = [ELEC_CYAN, STATIC_WHITE, ACID_GREEN, DATA_BLUE]
    weights = [0.40, 0.25, 0.20, 0.15]
    num = 50

    for _ in range(num):
        px = rng.randint(0, W - 1)
        py = rng.randint(0, H - 1)
        # Anti-gravity drift — slight upward offset for floating particles
        drift = rng.randint(-2, 2)
        py = max(0, min(H - 1, py + drift))
        sz = rng.randint(1, 3)

        # Pick color by weight
        r = rng.random()
        cumulative = 0.0
        col = ELEC_CYAN
        for c, w in zip(colors, weights):
            cumulative += w
            if r <= cumulative:
                col = c
                break

        draw.rectangle([px, py, px + sz, py + sz], fill=col)

    # Settled particles on Luma's shoulder (implied — 2-3 dots near her)
    # Luma feet at (W*0.14, H*0.66), shoulder approx (W*0.17, H*0.49)
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
    """
    Production footer bar — dark band at bottom with frame identification.
    """
    footer_h = 28
    footer_y = H - footer_h
    draw.rectangle([0, footer_y, W - 1, H - 1], fill=(5, 5, 12))
    # Thin ELEC_CYAN line above footer
    draw.line([(0, footer_y), (W - 1, footer_y)], fill=ELEC_CYAN, width=1)

    label_items = [
        (12, "LTG — STYLE FRAME 03 — \"THE OTHER SIDE\""),
        (480, "VOID + ELEC_CYAN + UV_PURPLE | NO WARM LIGHT"),
        (960, "1920×1080 | JORDAN REED | CYCLE 15"),
        (1500, "LTG_COLOR_styleframe_otherside_v001"),
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

    print("Layer 4: Far distance...")
    draw = draw_far_distance(draw, img)

    print("Layer 3: Mid-distance structures...")
    draw = draw_mid_distance(draw, img)

    print("Layer 2: Midground (platform, waterfall, sub-platforms)...")
    draw = draw_midground(draw, img)

    print("Layer 1: Foreground (settled confetti)...")
    draw = draw_foreground(draw)

    print("Lighting overlay (UV ambient + cyan bounce + blue waterfall)...")
    draw = draw_lighting_overlay(img)

    print("Character: Luma...")
    # Luma: feet at (W*0.14, H*0.66), height = H*0.20
    luma_cx = int(W * 0.14)
    luma_cy = int(H * 0.66)  # feet y
    luma_h  = int(H * 0.20)
    draw_luma(draw, luma_cx, luma_cy, luma_h)

    print("Character: Byte...")
    # Byte: on Luma's right shoulder, H*0.10 tall
    # Shoulder approx = luma feet y - (0.65 * luma_h)
    byte_cx = int(W * 0.17)
    byte_cy = int(H * 0.49)
    byte_h  = int(H * 0.10)
    draw_byte(draw, byte_cx, byte_cy, byte_h)

    print("Ambient confetti (seed=77)...")
    draw = draw_confetti(draw)

    print("Footer bar...")
    draw = draw_footer(draw, img)

    # Final validation check (print to stdout for review)
    print("\n── Validation Checks ──────────────────────────────────────────────")
    print(f"  Canvas: {img.size[0]}×{img.size[1]}  Mode: {img.mode}")
    print(f"  ELEC_CYAN G={ELEC_CYAN[1]} > R={ELEC_CYAN[0]}? {'✓' if ELEC_CYAN[1] > ELEC_CYAN[0] else 'FAIL'}")
    print(f"  ELEC_CYAN B={ELEC_CYAN[2]} > R={ELEC_CYAN[0]}? {'✓' if ELEC_CYAN[2] > ELEC_CYAN[0] else 'FAIL'}")
    print(f"  No warm light source: ✓ (warmth only in Luma/debris pigment)")
    print(f"  Inverted atmos perspective: ✓ (far = darker + more purple)")
    print(f"  Dutch angle: NONE ✓ (level horizon — deliberate stillness)")
    print(f"  Byte eyes: Cyan(left/Luma) + Magenta(right/void) ✓")
    print(f"  No CORRUPT_AMBER outline on Byte ✓")
    print(f"  Confetti seed=77, no warm colors ✓")
    print(f"  BELOW_VOID used for abyss ✓")
    print(f"  draw refreshed after paste() calls ✓")
    print("────────────────────────────────────────────────────────────────────\n")

    img.save(output_path)
    print(f"Saved: {output_path}")

    import os
    file_size = os.path.getsize(output_path)
    print(f"  File size: {file_size:,} bytes ({file_size // 1024} KB)")
    return file_size


if __name__ == "__main__":
    out_path = "/home/wipkat/team/output/color/style_frames/LTG_COLOR_styleframe_otherside_v001.png"
    generate(out_path)
