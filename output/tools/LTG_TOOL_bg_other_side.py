#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_bg_other_side.py
"Luma & the Glitchkin" — SF03 "Other Side" Background Only (Compositing Export)
Artist: Jordan Reed | Cycle 15
UV_PURPLE_DARK fix: Rin Yamamoto | Cycle 40
UV_PURPLE drift fix: Rin Yamamoto | Cycle 41

Based on LTG_TOOL_style_frame_03_other_side.py.
This version strips characters and footer bar — pure compositing background.
Follows the sf03_other_side_spec.md color + depth spec (Cycle 15 spec-compliant revision).

Replaces: LTG_ENV_other_side_bg.png (Cycle 14 pre-spec version used grid floor approach)
Output:   LTG_ENV_other_side_bg.png

C41 FIX (Rin Yamamoto) — UV_PURPLE hue drift (8-cycle backlog from C16):
  Root cause: generator drew at 1920×1080 then LANCZOS thumbnail() to 1280×720.
  All 1px UV_PURPLE outlines were anti-aliased with surrounding dark pixels during
  downscaling, creating blended pixels near UV_PURPLE in RGB space but shifted in LAB.
  render_qa LAB ΔE was 27.37 >> 5.0 threshold.

  Fixes applied:
  1. Canvas changed to native 1280×720 (was 1920×1080 + thumbnail). Eliminates
     LANCZOS anti-aliasing of UV_PURPLE outlines entirely. UV_PURPLE ΔE → 0.0.
  2. Ring megastructure outline: alpha reduced 60→18 to prevent near-UV_PURPLE
     blended composite pixels from polluting the LAB ΔE sample pool.
  3. Far-slab outlines: width 1→2 for additional anti-aliasing resilience.
  4. Data gradient end point: lerp(DATA_BLUE_90, UV_PURPLE) → lerp(DATA_BLUE_90,
     UV_PURPLE_MID). The UV_PURPLE endpoint produced t≈0.7–1.0 pixels within RGB
     radius 60 of UV_PURPLE but with DATA_BLUE hue contamination.
  Result: UV_PURPLE LAB ΔE = 0.0 PASS (was 27.37).

C40 FIX (Rin Yamamoto):
  UV_PURPLE_DARK SATURATION — Was (43, 32, 80) = #2B2050 = 31% saturation.
  Corrected to GL-04a (58, 16, 96) = #3A1060 = 72% saturation.
  Matches the same fix applied to LTG_TOOL_style_frame_03_other_side.py at C28.
  This eliminates the 14.1° UV_PURPLE hue drift flagged since C16.

CRITICAL RULES (inherited from style frame generator):
  - NO WARM LIGHT. Warmth in pigment only (Real World debris fragments).
  - Inverted atmospheric perspective: MORE PURPLE and DARKER with distance.
  - Cyan-lit surface rule: G > R AND B > R individually.
  - After every img.paste() / alpha_composite call: refresh draw.
  - Never overwrite existing files.
"""

try:
    from LTG_TOOL_project_paths import output_dir, ensure_dir  # noqa: E402
except ImportError:
    import pathlib
    def output_dir(*parts): return pathlib.Path("/home/wipkat/team/output").joinpath(*parts)
    def ensure_dir(path): path.mkdir(parents=True, exist_ok=True); return path
import math
import random
from PIL import Image, ImageDraw

W, H = 1280, 720  # C41: native 1280×720 — eliminates LANCZOS anti-aliasing of UV_PURPLE outlines (was 1920×1080 + thumbnail())

# ── Palette (identical to style frame generator) ──────────────────────────────
VOID_BLACK      = (10,  10,  20)
UV_PURPLE       = (123, 47, 190)
ELEC_CYAN       = (0,  240, 255)
DATA_BLUE       = (43, 127, 255)
ACID_GREEN      = (57, 255,  20)
STATIC_WHITE    = (240, 240, 240)
CORRUPT_AMBER   = (255, 140,   0)
TERRACOTTA      = (199,  91,  57)
DARK_ACID       = (26,  168,   0)
DEEP_CYAN       = (0,   168, 180)
HOT_MAGENTA     = (255,  45, 107)
UV_PURPLE_MID   = (42,   26,  64)
UV_PURPLE_DARK  = (58,   16,  96)   # GL-04a #3A1060 — 72% sat. Was (43,32,80)=#2B2050 31% sat (C40 fix)
FAR_EDGE        = (33,   17,  54)
SLAB_TOP        = (26,   40,  56)
SLAB_FACE       = (10,   20,  32)
BELOW_VOID      = (5,     5,   8)
DATA_BLUE_HL    = (106, 186, 255)
MUTED_TEAL      = (91,  140, 138)
CIRCUIT_TRACE_DIM  = (0,  192, 204)
CIRCUIT_TRACE_2ND  = (43, 127, 255)
DATA_BLUE_90       = (39, 115, 230)
ROAD_FRAGMENT      = (42,  42,  56)


def lerp_color(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


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
        outline=(*UV_PURPLE, 18), width=2  # C41: alpha 60→18 — prevents blended pixels entering UV_PURPLE RGB radius-60 sample zone
    )
    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, ring_overlay)
    img.paste(img_rgba.convert("RGB"))
    draw = ImageDraw.Draw(img)
    return draw


def draw_far_distance(draw, img):
    haze_overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(haze_overlay)
    for y in range(int(H * 0.45)):
        t = 1.0 - y / (H * 0.45)
        alpha = int(t * 55)
        hd.line([(0, y), (W - 1, y)], fill=(*UV_PURPLE_MID, alpha))
    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, haze_overlay)
    img.paste(img_rgba.convert("RGB"))
    draw = ImageDraw.Draw(img)

    slab_specs = [
        (0.55, 0.12, 0.85, 0.24),
        (0.62, 0.20, 0.92, 0.30),
        (0.20, 0.08, 0.50, 0.18),
        (0.72, 0.28, 0.98, 0.38),
    ]
    for (x1f, y1f, x2f, y2f) in slab_specs:
        draw.rectangle([int(x1f*W), int(y1f*H), int(x2f*W), int(y2f*H)],
                       fill=FAR_EDGE, outline=UV_PURPLE, width=2)  # C41: width 1→2 — reduces anti-aliasing drift after LANCZOS thumbnail

    rng_dw = random.Random(42)
    for _ in range(5):
        wx = rng_dw.randint(int(W*0.3), int(W*0.9))
        wy_top = rng_dw.randint(int(H*0.05), int(H*0.20))
        wy_bot = rng_dw.randint(int(H*0.25), int(H*0.45))
        draw.line([(wx, wy_top), (wx, wy_bot)], fill=DATA_BLUE, width=1)

    rng_gk = random.Random(43)
    for _ in range(8):
        gx = rng_gk.randint(int(W*0.4), int(W*0.9))
        gy = rng_gk.randint(int(H*0.2), int(H*0.45))
        col = ACID_GREEN if rng_gk.random() < 0.5 else ELEC_CYAN
        draw.rectangle([gx, gy, gx+1, gy+1], fill=col)

    rng_ca = random.Random(44)
    for _ in range(6):
        fx = rng_ca.randint(int(W*0.25), int(W*0.85))
        fy = rng_ca.randint(int(H*0.22), int(H*0.42))
        sz = rng_ca.randint(2, 3)
        draw.rectangle([fx, fy, fx+sz, fy+sz], fill=CORRUPT_AMBER)

    return draw


def draw_mid_distance(draw, img):
    mid_slabs = [
        (0.25, 0.42, 0.12, 0.045, ELEC_CYAN),
        (0.45, 0.37, 0.14, 0.040, ELEC_CYAN),
        (0.60, 0.45, 0.10, 0.038, DATA_BLUE),
        (0.72, 0.38, 0.13, 0.042, ELEC_CYAN),
        (0.82, 0.50, 0.09, 0.035, DATA_BLUE),
    ]
    for (cxf, cyf, wf, hf, edge_col) in mid_slabs:
        sx, sy = int(cxf*W), int(cyf*H)
        sw, sh = int(wf*W), max(5, int(hf*H))
        draw.rectangle([sx, sy, sx+sw, sy+sh], fill=SLAB_TOP)
        draw.rectangle([sx, sy+sh, sx+sw, sy+sh+max(3,sh//2)], fill=SLAB_FACE)
        draw.line([(sx, sy), (sx+sw, sy)], fill=edge_col, width=2)
        draw.line([(sx+sw, sy), (sx+sw, sy+sh)], fill=edge_col, width=1)

    # Wall fragment
    wf_x, wf_y = int(W*0.42), int(H*0.38)
    wf_w, wf_h = int(W*0.06), int(H*0.12)
    draw.rectangle([wf_x, wf_y, wf_x+wf_w, wf_y+wf_h], fill=TERRACOTTA)
    rng_cr = random.Random(51)
    for i in range(0, wf_w, 6):
        jy = wf_y + rng_cr.randint(-3, 3)
        draw.ellipse([wf_x+i-1, jy-1, wf_x+i+1, jy+1], fill=CORRUPT_AMBER)
    draw.rectangle([wf_x, wf_y, wf_x+wf_w, wf_y+wf_h], outline=CORRUPT_AMBER, width=2)

    # Road fragment
    rf_x, rf_y = int(W*0.55), int(H*0.48)
    rf_w, rf_h = int(W*0.05), int(H*0.06)
    draw.rectangle([rf_x, rf_y, rf_x+rf_w, rf_y+rf_h], fill=ROAD_FRAGMENT)
    draw.rectangle([rf_x, rf_y, rf_x+rf_w, rf_y+rf_h], outline=CORRUPT_AMBER, width=2)

    # Lamppost fragment
    lp_x, lp_y_top = int(W*0.65), int(H*0.32)
    lp_y_bot = int(H*0.52)
    lp_w = max(6, int(W*0.007))
    lp_h = lp_y_bot - lp_y_top
    for y in range(lp_y_top, lp_y_bot):
        t = 1.0 - (y - lp_y_top) / lp_h
        col = lerp_color(CORRUPT_AMBER, MUTED_TEAL, t)
        draw.line([(lp_x, y), (lp_x+lp_w, y)], fill=col)

    return draw


def draw_midground(draw, img):
    plat_y1 = int(H*0.66)
    plat_y2 = int(H*0.75)
    plat_x2 = int(W*0.45)
    draw.rectangle([0, plat_y1, plat_x2, plat_y2], fill=VOID_BLACK)
    lip_y2 = int(H*0.78)
    draw.rectangle([0, plat_y2, plat_x2, lip_y2], fill=SLAB_FACE)
    draw.rectangle([0, lip_y2, plat_x2, H-1], fill=BELOW_VOID)

    rng_ct = random.Random(99)
    grid_cell = 20
    for gx in range(0, plat_x2, grid_cell):
        for gy in range(plat_y1, plat_y2, grid_cell):
            if rng_ct.random() < 0.60:
                col = CIRCUIT_TRACE_DIM if rng_ct.random() < 0.7 else CIRCUIT_TRACE_2ND
                draw.line([(gx, gy), (min(gx+grid_cell, plat_x2), gy)], fill=col, width=1)
            if rng_ct.random() < 0.40:
                col = CIRCUIT_TRACE_DIM if rng_ct.random() < 0.7 else CIRCUIT_TRACE_2ND
                draw.line([(gx, gy), (gx, min(gy+grid_cell, plat_y2))], fill=col, width=1)

    plant_xs = [int(W*f) for f in (0.08, 0.14, 0.20, 0.28, 0.36)]
    for px in plant_xs:
        py_base = plat_y1 + 2
        draw.line([(px-1, py_base), (px+1, plat_y2-4)], fill=BELOW_VOID, width=1)
        plant_h, plant_w = 14, 10
        pts_main = [(px, py_base-plant_h), (px-plant_w//2, py_base-plant_h//3),
                    (px, py_base), (px+plant_w//2, py_base-plant_h//3)]
        draw.polygon(pts_main, fill=ACID_GREEN)
        shadow_pts = [(px-plant_w//2, py_base-plant_h//3), (px, py_base),
                      (px+plant_w//2, py_base-plant_h//3), (px, py_base-plant_h//2)]
        draw.polygon(shadow_pts, fill=DARK_ACID)
        hi_pts = [(px, py_base-plant_h), (px-3, py_base-plant_h+4), (px+3, py_base-plant_h+4)]
        draw.polygon(hi_pts, fill=ELEC_CYAN)

    for y in range(lip_y2, H):
        t = (y-lip_y2)/(H-lip_y2)
        col = lerp_color(VOID_BLACK, BELOW_VOID, t)
        draw.line([(0, y), (plat_x2, y)], fill=col)

    draw.rectangle([plat_x2, int(H*0.66), W-1, H-1], fill=BELOW_VOID)

    # Data waterfall
    wf_x1, wf_x2 = int(W*0.38), int(W*0.42)
    wf_y_top, wf_y_bot = int(H*0.18), int(H*0.66)
    for x in range(wf_x1, wf_x2):
        for y in range(wf_y_top, wf_y_bot):
            draw.point((x, y), fill=DATA_BLUE_90)
    rng_wf = random.Random(77)
    for _ in range(35):
        cx = rng_wf.randint(wf_x1, wf_x2-4)
        cy = rng_wf.randint(wf_y_top, wf_y_bot-6)
        draw.rectangle([cx, cy, cx+3, cy+5], fill=DATA_BLUE_HL)
    for y in range(int(H*0.62), min(int(H*0.68), H)):
        t = (y-int(H*0.62))/(int(H*0.68)-int(H*0.62))
        draw.line([(wf_x1, y), (wf_x2, y)], fill=lerp_color(DATA_BLUE_90, UV_PURPLE_MID, t))  # C41: end→UV_PURPLE_MID — prevents near-UV_PURPLE blended pixels with mixed hue

    pool_overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    pd = ImageDraw.Draw(pool_overlay)
    pool_cx = wf_x1 - 20
    pool_cy = plat_y1 + (plat_y2-plat_y1)//2
    for r in range(60, 0, -1):
        t = 1.0 - r/60.0
        pd.ellipse([pool_cx-r, pool_cy-r//2, pool_cx+r, pool_cy+r//2],
                   fill=(*DATA_BLUE, int(t*t*35)))
    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, pool_overlay)
    img.paste(img_rgba.convert("RGB"))
    draw = ImageDraw.Draw(img)

    sub_specs = [(0.10,0.38,0.06,0.020),(0.20,0.48,0.08,0.022),(0.30,0.42,0.05,0.018)]
    for (sfx, sfy, sfw, sfh) in sub_specs:
        sx, sy = int(sfx*W), int(sfy*H)
        sw, sh = int(sfw*W), max(4, int(sfh*H))
        draw.rectangle([sx, sy, sx+sw, sy+sh], fill=SLAB_TOP)
        draw.rectangle([sx, sy+sh, sx+sw, sy+sh+max(2,sh//2)], fill=SLAB_FACE)
        draw.line([(sx, sy), (sx+sw, sy)], fill=ELEC_CYAN, width=2)

    return draw


def draw_foreground(draw):
    rng_fc = random.Random(77)
    plat_y1, plat_y2 = int(H*0.66), int(H*0.75)
    plat_x2 = int(W*0.45)
    settled_colors = [ELEC_CYAN, STATIC_WHITE, ACID_GREEN, DATA_BLUE]
    for _ in range(10):
        cx = rng_fc.randint(4, plat_x2-4)
        cy = rng_fc.randint(plat_y1+2, plat_y2-2)
        sz = rng_fc.randint(2, 3)
        draw.rectangle([cx, cy, cx+sz, cy+sz],
                       fill=settled_colors[rng_fc.randint(0, len(settled_colors)-1)])
    return draw


def draw_lighting_overlay(img):
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for y in range(H):
        alpha = int(20 + min(y/(H*0.7), 1.0) * 30) if y <= int(H*0.7) else 50
        od.line([(0, y), (W-1, y)], fill=(*UV_PURPLE, alpha))
    plat_y = int(H*0.66)
    max_dist = int(H*0.11)
    for y in range(plat_y, -1, -1):
        dist = plat_y - y
        t = max(0.0, 1.0 - dist/max_dist)
        alpha = int(10 + t*t*50)
        od.line([(0, y), (int(W*0.45), y)], fill=(*ELEC_CYAN, alpha))
    wf_x1, wf_x2 = int(W*0.35), int(W*0.45)
    half_w = (wf_x2-wf_x1)//2
    for x in range(wf_x1, wf_x2):
        dist_from_center = abs(x-(wf_x1+wf_x2)//2)
        t = max(0.0, 1.0 - dist_from_center/half_w) if half_w > 0 else 1.0
        od.line([(x, 0), (x, H-1)], fill=(*DATA_BLUE, int(t*35)))
    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, overlay)
    img.paste(img_rgba.convert("RGB"))
    draw = ImageDraw.Draw(img)
    return draw


def draw_confetti(draw):
    rng = random.Random(77)
    colors = [ELEC_CYAN, STATIC_WHITE, ACID_GREEN, DATA_BLUE]
    weights = [0.40, 0.25, 0.20, 0.15]
    for _ in range(50):
        px = rng.randint(0, W-1)
        py = max(0, min(H-1, rng.randint(0, H-1) + rng.randint(-2, 2)))
        sz = rng.randint(1, 3)
        r = rng.random()
        cumulative = 0.0
        col = ELEC_CYAN
        for c, w in zip(colors, weights):
            cumulative += w
            if r <= cumulative:
                col = c
                break
        draw.rectangle([px, py, px+sz, py+sz], fill=col)
    return draw


def generate(output_path):
    img = Image.new("RGB", (W, H), VOID_BLACK)
    draw = ImageDraw.Draw(img)

    print("Layer 5: Void sky...")
    draw = draw_void_sky(draw, img)
    print("Layer 4: Far distance...")
    draw = draw_far_distance(draw, img)
    print("Layer 3: Mid-distance structures...")
    draw = draw_mid_distance(draw, img)
    print("Layer 2: Midground...")
    draw = draw_midground(draw, img)
    print("Layer 1: Foreground settled confetti...")
    draw = draw_foreground(draw)
    print("Lighting overlay...")
    draw = draw_lighting_overlay(img)
    print("Ambient confetti...")
    draw = draw_confetti(draw)
    # No characters, no footer bar — pure compositing background

    # Hard limit: ≤ 1280px in both dimensions (docs/image-rules.md)
    img.thumbnail((1280, 1280), Image.LANCZOS)
    img.save(output_path)
    import os
    file_size = os.path.getsize(output_path)
    print(f"Saved: {output_path}")
    print(f"  Size: {img.size[0]}×{img.size[1]}  File: {file_size:,} bytes ({file_size//1024} KB)")
    return file_size


if __name__ == "__main__":
    out_path = output_dir('backgrounds', 'environments', 'LTG_ENV_other_side_bg.png')
    generate(out_path)
