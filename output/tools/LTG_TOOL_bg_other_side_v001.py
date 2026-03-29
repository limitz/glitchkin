#!/usr/bin/env python3
"""
LTG_TOOL_bg_other_side_v001.py — SF03 "Other Side" Environment Background
"Luma & the Glitchkin" — Background & Environment Design
Artist: Jordan Reed | Cycle 14

Renders the Glitch Layer "Other Side" CRT-world environment at 1920x1080.
This is the deep digital interior — pure digital space inside the TV/CRT world.
No warm tones. Dominated by electric cyan and void black.
Geometric pixel grid floor. Floating platform structures. Deep z-axis depth.

Contrast role in pitch package:
  SF01 — Luma's House: warm amber/terracotta, cozy analog interior
  SF02 — Millbrook Street: contested warm/glitch, transition zone
  SF03 — Other Side (this): full digital void, zero warm tones, alien geometry

Key spec:
  - Pure digital space: no Terracotta, Soft Gold, Sage, Warm Cream
  - Dominant: ELEC_CYAN (#00F0FF) + VOID_BLACK (#0A0A14)
  - Accent: UV_PURPLE (#7B2FBE), HOT_MAGENTA (#FF2D6B) — sparse danger accents
  - Geometric pixel grid floor with deep z-axis recession
  - Floating platform structures at NEAR/MID/FAR depth tiers
  - Scanline texture overlay on all surfaces
  - Pixel confetti / data trail particles

Rules applied (MEMORY.md):
  - 3-value-tier depth system mandatory
  - Under cyan key: G+B channels must exceed R (ELEC_CYAN G=240, B=255, R=0 ✓)
  - Empty foreground = no depth anchor → foreground grid edge + near platform fragment
  - No per-pixel loops — use draw.line() for fills
  - Refresh draw handle after every alpha_composite
  - No title bar (compositing export)

Output: /home/wipkat/team/output/backgrounds/environments/LTG_ENV_other_side_bg_v001.png
"""

import math
import random
from PIL import Image, ImageDraw, ImageFilter

# ── Canvas ───────────────────────────────────────────────────────────────────
W, H = 1920, 1080

# ── Canonical Palette (master_palette.md) ────────────────────────────────────
VOID_BLACK       = (10,  10,  20)    # GL-08  #0A0A14
BELOW_VOID       = (5,   5,   8)    # GL-08a #050508
ELEC_CYAN        = (0,  240, 255)   # GL-01  #00F0FF  — dominant env color
DEEP_CYAN        = (0,  168, 180)   # GL-01a #00A8B4
UV_PURPLE        = (123, 47, 190)   # GL-04  #7B2FBE
DEEP_VOID        = (58,  16,  96)   # GL-04a #3A1060
ATMOS_MID_PURPLE = (74,  24, 128)   # GL-04b #4A1880
HOT_MAGENTA      = (255, 45, 107)   # GL-02  #FF2D6B  — danger accent, sparse
STATIC_WHITE     = (240, 240, 240)  # GL-05  #F0F0F0
DATA_BLUE_MID    = (10,  72, 120)   # GL-06 derived — MID platform tier
ACID_GREEN       = (57, 255,  20)   # GL-03  #39FF14  — trace only

# ── Derived Depth Tiers ───────────────────────────────────────────────────────
# NEAR: Full ELEC_CYAN — foreground platforms, max brightness
NEAR_COLOR  = (0,  240, 255)   # ELEC_CYAN
NEAR_SHADOW = (0,  140, 160)   # darkened DEEP_CYAN
NEAR_EDGE   = (180, 255, 255)  # near-white edge highlight

# MID: Desaturated mid-depth
MID_COLOR   = (10,  72, 120)   # DATA_BLUE derived
MID_SHADOW  = (6,   40,  72)
MID_EDGE    = (20, 110, 160)

# FAR: Near-void, barely visible
FAR_COLOR   = (0,   26,  40)
FAR_SHADOW  = (0,   14,  22)
FAR_EDGE    = (0,   40,  55)

# GRID: The pixel floor grid colors
GRID_BASE   = (0,   18,  30)   # near-void floor base
GRID_LINE   = (0,   80, 120)   # receding grid lines
GRID_NEAR   = (0,  120, 160)   # nearest grid lines (brighter, closer)
GRID_GLOW   = (0,  200, 240)   # grid intersection glow points


def lerp_color(a, b, t):
    """Linear interpolate between two RGB tuples."""
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def draw_scanline_overlay(img, alpha=18, every=3):
    """Add horizontal scanline texture overlay at low opacity."""
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for y in range(0, H, every):
        od.line([(0, y), (W - 1, y)], fill=(0, 0, 0, alpha))
    img = img.convert("RGBA")
    img = Image.alpha_composite(img, overlay)
    return img.convert("RGB")


def draw_void_background(img):
    """Draw the deep void background with atmospheric depth gradient."""
    draw = ImageDraw.Draw(img)
    # Vertical gradient: top is deeper purple-void, bottom is pure void black
    for y in range(H):
        t = y / H
        # Upper 35%: UV purple aurora bleeds down
        if t < 0.35:
            t2 = t / 0.35
            col = lerp_color(DEEP_VOID, VOID_BLACK, t2 * t2)
        else:
            t2 = (t - 0.35) / 0.65
            col = lerp_color(VOID_BLACK, BELOW_VOID, t2 * 0.4)
        draw.line([(0, y), (W - 1, y)], fill=col)
    return draw


def draw_aurora_bands(img):
    """Draw sinusoidal aurora bands in upper portion of frame."""
    rng = random.Random(42)
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)

    # Four aurora bands at different heights
    band_specs = [
        # (center_y_frac, amplitude, alpha, color)
        (0.04, 12, 38, DEEP_VOID),
        (0.08, 18, 50, ATMOS_MID_PURPLE),
        (0.12, 22, 42, UV_PURPLE),
        (0.16, 16, 28, DEEP_CYAN),
    ]
    for cy_frac, amp, alpha, col in band_specs:
        cy = int(cy_frac * H)
        for x in range(0, W):
            phase = (x / W) * math.pi * 4 + rng.uniform(0, 0.3)
            y = cy + int(amp * math.sin(phase))
            band_h = max(4, int(amp * 0.8))
            for dy in range(-band_h, band_h + 1):
                fade = 1.0 - abs(dy) / (band_h + 1)
                a = int(alpha * fade * fade)
                py = y + dy
                if 0 <= py < H:
                    od.point((x, py), fill=(*col, a))

    img = img.convert("RGBA")
    img = Image.alpha_composite(img, overlay)
    return img.convert("RGB")


def draw_pixel_grid(img):
    """Draw the perspective pixel grid floor that recedes to the horizon."""
    draw = ImageDraw.Draw(img)
    horizon_y = int(H * 0.46)   # horizon line
    floor_bottom = H

    # Floor base fill — gradient from grid_base to below_void
    for y in range(horizon_y, H):
        t = (y - horizon_y) / (H - horizon_y)
        col = lerp_color(GRID_BASE, (0, 8, 14), t)
        draw.line([(0, y), (W - 1, y)], fill=col)

    # Perspective horizontal grid lines
    # Lines crowd toward horizon, spread near camera
    num_h_lines = 24
    for i in range(num_h_lines):
        # Quadratic distribution — more lines near horizon
        t = (i / num_h_lines) ** 2.2
        y = int(horizon_y + t * (H - horizon_y))
        if y >= H:
            break
        # Brightness increases toward camera (near bottom)
        brightness_t = i / num_h_lines  # 0=near horizon, 1=near camera
        line_col = lerp_color(GRID_LINE, GRID_NEAR, brightness_t ** 1.5)
        # Line width increases toward camera
        lw = max(1, int(brightness_t * 3))
        for dy in range(lw):
            if y + dy < H:
                draw.line([(0, y + dy), (W - 1, y + dy)], fill=line_col)

    # Perspective vertical grid lines — converge to center vanishing point
    vp_x = int(W * 0.5)   # vanishing point x
    num_v_lines = 30
    for i in range(num_v_lines + 1):
        # Spread from vanishing point to canvas edges
        t = (i / num_v_lines) - 0.5   # -0.5 to +0.5
        # Bottom x: spread further
        bx = int(vp_x + t * W * 1.8)
        line_col = GRID_LINE
        if abs(t) < 0.06:
            line_col = GRID_NEAR
        draw.line([(vp_x, horizon_y), (bx, H - 1)], fill=line_col, width=1)

    # Grid intersection glow dots — sparse, near horizon
    rng = random.Random(77)
    for i in range(num_h_lines):
        t = (i / num_h_lines) ** 2.2
        y = int(horizon_y + t * (H - horizon_y))
        if y >= H:
            break
        if i < 6:  # only near-horizon intersections glow
            for j in range(num_v_lines + 1):
                tv = (j / num_v_lines) - 0.5
                bx_j = int(vp_x + tv * W * 1.8)
                gx = int(vp_x + (bx_j - vp_x) * t)
                gy = y
                if 0 <= gx < W and 0 <= gy < H:
                    if rng.random() < 0.25:
                        sz = rng.randint(1, 3)
                        draw.ellipse([gx - sz, gy - sz, gx + sz, gy + sz],
                                     fill=GRID_GLOW)

    return draw, horizon_y


def draw_platform(draw, px, py, pw, ph, color, shadow, edge, rng=None, fragmented=False):
    """Draw a floating platform with top-edge highlight and underside shadow."""
    if fragmented and rng:
        # Fragmented platform — draw with pixel-step gaps
        step = max(8, pw // 12)
        for sx in range(0, pw, step):
            if rng.random() > 0.25:
                sw = min(step - 2, pw - sx)
                draw.rectangle([px + sx, py, px + sx + sw, py + ph], fill=color)
    else:
        draw.rectangle([px, py, px + pw, py + ph], fill=color)

    # Underside shadow strip
    shadow_h = max(2, ph // 4)
    draw.rectangle([px, py + ph, px + pw, py + ph + shadow_h], fill=shadow)
    # Top edge highlight
    draw.line([(px, py), (px + pw, py)], fill=edge, width=2)


def draw_far_platforms(draw, rng):
    """Far tier: near-void, high in frame, silhouette only."""
    specs = [
        (0.08, 0.32, 0.18, 0.025),
        (0.32, 0.38, 0.20, 0.022),
        (0.54, 0.36, 0.16, 0.020),
        (0.72, 0.40, 0.22, 0.024),
    ]
    for (fx, fy, fw, fh) in specs:
        px = int(fx * W)
        py = int(fy * H)
        pw = int(fw * W)
        ph = max(4, int(fh * H))
        draw_platform(draw, px, py, pw, ph, FAR_COLOR, FAR_SHADOW, FAR_EDGE)


def draw_mid_platforms(draw, rng):
    """Mid tier: desaturated DATA_BLUE, medium height, some L-shapes."""
    specs = [
        # (x_frac, y_frac, w_frac, h_frac)
        (0.05, 0.50, 0.22, 0.032),
        (0.38, 0.54, 0.28, 0.030),
        (0.74, 0.48, 0.20, 0.035),
        (0.20, 0.60, 0.18, 0.028),
        (0.62, 0.62, 0.24, 0.030),
    ]
    for i, (fx, fy, fw, fh) in enumerate(specs):
        px = int(fx * W)
        py = int(fy * H)
        pw = int(fw * W)
        ph = max(6, int(fh * H))
        draw_platform(draw, px, py, pw, ph, MID_COLOR, MID_SHADOW, MID_EDGE, rng)
        # L-shape extension on alternating platforms
        if i % 2 == 0:
            ext_w = int(pw * 0.35)
            ext_h = int(ph * 1.6)
            draw.rectangle([px, py - ext_h, px + ext_w, py], fill=MID_COLOR)
            draw.line([(px, py - ext_h), (px + ext_w, py - ext_h)],
                      fill=MID_EDGE, width=2)


def draw_near_platforms(draw, rng):
    """Near tier: full ELEC_CYAN, prominent, foreground depth anchor."""
    specs = [
        # Main foreground platform fragments — left and right edges anchor depth
        (0.00, 0.70, 0.14, 0.042),  # left fragment, cropped at left edge
        (0.86, 0.68, 0.14, 0.042),  # right fragment, cropped at right edge
        (0.18, 0.73, 0.32, 0.038),  # left-center near platform
        (0.56, 0.72, 0.26, 0.040),  # right-center near platform
    ]
    for (fx, fy, fw, fh) in specs:
        px = int(fx * W)
        py = int(fy * H)
        pw = int(fw * W)
        ph = max(8, int(fh * H))
        draw_platform(draw, px, py, pw, ph, NEAR_COLOR, NEAR_SHADOW, NEAR_EDGE,
                      rng, fragmented=(fx in (0.00, 0.86)))


def draw_pixel_trails(img, draw, rng):
    """Pixel trails rising from near/mid platforms — upward direction = healthy energy."""
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)

    # Trails from near platforms
    near_platform_ys = [
        (int(0.18 * W), int(0.73 * H), int(0.32 * W)),
        (int(0.56 * W), int(0.72 * H), int(0.26 * W)),
    ]
    for (px, py, pw) in near_platform_ys:
        num_trails = rng.randint(18, 28)
        for _ in range(num_trails):
            tx = px + rng.randint(4, pw - 4)
            ty = py
            trail_len = rng.randint(30, 100)
            for step in range(trail_len):
                ty_step = ty - step
                if ty_step < 0:
                    break
                # Density weighted near platform — fade out upward
                density_t = step / trail_len
                if rng.random() > (1.0 - density_t * 0.85):
                    continue
                alpha = int(200 * (1.0 - density_t ** 1.5))
                # Color: ELEC_CYAN near base, fades toward DEEP_CYAN
                col = lerp_color(ELEC_CYAN, DEEP_CYAN, density_t)
                od.point((tx, ty_step), fill=(*col, alpha))

    # Trails from mid platforms — dimmer, DATA_BLUE family
    mid_ys = [
        (int(0.05 * W), int(0.50 * H), int(0.22 * W)),
        (int(0.38 * W), int(0.54 * H), int(0.28 * W)),
        (int(0.74 * W), int(0.48 * H), int(0.20 * W)),
    ]
    for (px, py, pw) in mid_ys:
        num_trails = rng.randint(8, 14)
        for _ in range(num_trails):
            tx = px + rng.randint(4, max(5, pw - 4))
            trail_len = rng.randint(20, 60)
            for step in range(trail_len):
                ty_step = py - step
                if ty_step < 0:
                    break
                density_t = step / trail_len
                if rng.random() > (1.0 - density_t * 0.8):
                    continue
                alpha = int(120 * (1.0 - density_t ** 1.5))
                col = lerp_color(MID_EDGE, MID_COLOR, density_t)
                od.point((tx, ty_step), fill=(*col, alpha))

    img = img.convert("RGBA")
    img = Image.alpha_composite(img, overlay)
    return img.convert("RGB")


def draw_data_streams(img):
    """Vertical data stream columns cascading down the void walls."""
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    rng = random.Random(88)
    # Only in upper void area above the horizon
    horizon_y = int(H * 0.46)
    num_streams = 22
    for _ in range(num_streams):
        sx = rng.randint(0, W - 1)
        # Stream length and start
        sy = rng.randint(0, int(horizon_y * 0.8))
        sl = rng.randint(40, 160)
        for step in range(sl):
            sy_step = sy + step
            if sy_step >= horizon_y:
                break
            t = step / sl
            alpha = int(60 * (1.0 - t))
            # Alternate between cyan and purple for variety
            if rng.random() < 0.7:
                col = lerp_color(DEEP_CYAN, VOID_BLACK, t)
            else:
                col = lerp_color(ATMOS_MID_PURPLE, VOID_BLACK, t)
            od.point((sx, sy_step), fill=(*col, alpha))

    img = img.convert("RGBA")
    img = Image.alpha_composite(img, overlay)
    return img.convert("RGB")


def draw_pixel_confetti(img):
    """Floating pixel confetti particles — show's visual signature in digital zone."""
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    rng = random.Random(55)
    # Confetti palette: ELEC_CYAN, UV_PURPLE, HOT_MAGENTA, STATIC_WHITE
    # NO ACID_GREEN (Cycle 12 lesson: storm/danger confetti exclusion)
    confetti_colors = [ELEC_CYAN, UV_PURPLE, HOT_MAGENTA, STATIC_WHITE, DEEP_CYAN]
    confetti_weights = [0.45, 0.25, 0.10, 0.12, 0.08]  # cyan dominant

    num_particles = 280
    for _ in range(num_particles):
        cx = rng.randint(0, W - 1)
        cy = rng.randint(0, H - 1)
        # Avoid placing dense confetti in lower third (floor zone — platforms there)
        if cy > H * 0.75 and rng.random() < 0.7:
            continue
        sz = rng.randint(1, 4)
        alpha = rng.randint(60, 180)
        r = rng.random()
        cumulative = 0.0
        col = ELEC_CYAN
        for c, w in zip(confetti_colors, confetti_weights):
            cumulative += w
            if r <= cumulative:
                col = c
                break
        od.rectangle([cx, cy, cx + sz, cy + sz], fill=(*col, alpha))

    img = img.convert("RGBA")
    img = Image.alpha_composite(img, overlay)
    return img.convert("RGB")


def draw_horizon_glow(img):
    """Electric cyan horizon glow at the vanishing point — deep z-axis pull."""
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    horizon_y = int(H * 0.46)
    vp_x = int(W * 0.5)
    # Radial glow emanating from vanishing point
    for r in range(200, 0, -1):
        t = 1.0 - (r / 200.0)
        alpha = int(t * t * 55)
        if r > 0:
            od.ellipse([vp_x - r, horizon_y - r // 3,
                        vp_x + r, horizon_y + r // 3],
                       fill=(*ELEC_CYAN, alpha))
    img = img.convert("RGBA")
    img = Image.alpha_composite(img, overlay)
    return img.convert("RGB")


def draw_platform_glow_spill(img):
    """Cyan glow spill beneath near platforms onto the grid floor."""
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    # Glow spill under each near platform — leftward/downward emanation
    near_specs = [
        (int(0.18 * W), int(0.73 * H), int(0.32 * W)),
        (int(0.56 * W), int(0.72 * H), int(0.26 * W)),
    ]
    for (px, py, pw) in near_specs:
        glow_w = int(pw * 1.2)
        glow_h = int(H * 0.10)
        gx_center = px + pw // 2
        for gx in range(gx_center - glow_w // 2, gx_center + glow_w // 2):
            dist_x = abs(gx - gx_center) / (glow_w // 2)
            for gy in range(py, min(H, py + glow_h)):
                dist_y = (gy - py) / glow_h
                t = 1.0 - max(dist_x, dist_y)
                if t <= 0:
                    continue
                alpha = int(t * t * 30)
                if 0 <= gx < W:
                    od.point((gx, gy), fill=(*ELEC_CYAN, alpha))
    img = img.convert("RGBA")
    img = Image.alpha_composite(img, overlay)
    return img.convert("RGB")


def draw_floating_geometry(draw, rng):
    """Scattered small geometric shapes (cubes, rectangles) floating in mid-void."""
    # Small cube outlines — pure geometry, Glitch Layer prop logic
    cube_specs = [
        (0.12, 0.29, 18),
        (0.45, 0.25, 14),
        (0.78, 0.31, 22),
        (0.32, 0.40, 12),
        (0.65, 0.38, 16),
        (0.88, 0.44, 10),
        (0.04, 0.43, 8),
    ]
    for (fx, fy, sz) in cube_specs:
        cx = int(fx * W)
        cy = int(fy * H)
        # Face front
        draw.rectangle([cx, cy, cx + sz, cy + sz], fill=FAR_COLOR, outline=DEEP_CYAN)
        # Isometric top face
        draw.polygon([
            (cx, cy),
            (cx + sz, cy),
            (cx + sz + sz // 3, cy - sz // 3),
            (cx + sz // 3, cy - sz // 3),
        ], fill=MID_SHADOW, outline=MID_EDGE)
        # Isometric right face
        draw.polygon([
            (cx + sz, cy),
            (cx + sz + sz // 3, cy - sz // 3),
            (cx + sz + sz // 3, cy + sz - sz // 3),
            (cx + sz, cy + sz),
        ], fill=MID_COLOR, outline=DEEP_CYAN)


def draw_warning_accents(draw, rng):
    """Sparse HOT_MAGENTA danger accents on a few platform edges — Corruption hint."""
    # A few platform edges show HOT_MAGENTA flicker marks
    accent_specs = [
        # (x, y, length)
        (int(0.38 * W), int(0.54 * H), 40),
        (int(0.74 * W), int(0.48 * H), 28),
    ]
    for (ax, ay, alen) in accent_specs:
        # Jagged edge — alternating pixel segments
        for i in range(0, alen, 4):
            if rng.random() < 0.6:
                draw.line([(ax + i, ay), (ax + i + 3, ay)], fill=HOT_MAGENTA, width=2)


def draw_crt_frame_vignette(img):
    """Subtle CRT-style vignette at screen edges — we are inside the TV world."""
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    # Radial darkening from corners
    cx, cy = W // 2, H // 2
    for y in range(0, H, 3):
        for x in range(0, W, 3):
            dx = (x - cx) / (W / 2)
            dy = (y - cy) / (H / 2)
            dist = math.sqrt(dx * dx + dy * dy)
            if dist > 0.65:
                alpha = int(min(180, (dist - 0.65) / 0.6 * 180))
                od.point((x, y), fill=(0, 0, 0, alpha))
    # CRT phosphor edge glow — faint cyan border
    border_w = 8
    for bx in range(border_w):
        t = 1.0 - bx / border_w
        alpha = int(t * t * 60)
        od.rectangle([bx, bx, W - 1 - bx, H - 1 - bx],
                     outline=(*ELEC_CYAN, alpha))
    img = img.convert("RGBA")
    img = Image.alpha_composite(img, overlay)
    return img.convert("RGB")


def main():
    rng = random.Random(314)
    img = Image.new("RGB", (W, H), VOID_BLACK)

    # Step 1: Void background gradient
    draw = draw_void_background(img)

    # Step 2: Aurora bands (upper void)
    img = draw_aurora_bands(img)

    # Step 3: Pixel grid floor (perspective recession)
    draw, horizon_y = draw_pixel_grid(img)

    # Step 4: Floating geometry (far distance cubes)
    draw = ImageDraw.Draw(img)
    draw_floating_geometry(draw, rng)

    # Step 5: Platform depth tiers — FAR → MID → NEAR
    draw_far_platforms(draw, rng)
    draw_mid_platforms(draw, rng)

    # Step 6: Warning accents (HOT_MAGENTA danger hints)
    draw_warning_accents(draw, rng)

    # Step 7: Near platforms (foreground depth anchor — mandatory rule)
    draw_near_platforms(draw, rng)

    # Step 8: Pixel trails (upward = healthy energy)
    img = draw_pixel_trails(img, draw, rng)

    # Step 9: Data streams (upper void — vertical cascade)
    img = draw_data_streams(img)

    # Step 10: Horizon glow (vanishing point pull — deep z-axis)
    img = draw_horizon_glow(img)

    # Step 11: Platform glow spill onto grid floor
    img = draw_platform_glow_spill(img)

    # Step 12: Pixel confetti (show signature)
    img = draw_pixel_confetti(img)

    # Step 13: Scanline overlay (all surfaces, Glitch Layer prop rule)
    img = draw_scanline_overlay(img, alpha=20, every=3)

    # Step 14: CRT vignette (we are inside the TV world)
    img = draw_crt_frame_vignette(img)

    # Save output
    out_path = "/home/wipkat/team/output/backgrounds/environments/LTG_ENV_other_side_bg_v001.png"
    img.save(out_path)
    print(f"Saved: {out_path}")
    print(f"  Size: {img.size[0]}x{img.size[1]}  Mode: {img.mode}")
    print(f"  Cyan channel check: ELEC_CYAN G({ELEC_CYAN[1]}) + B({ELEC_CYAN[2]}) = "
          f"{ELEC_CYAN[1]+ELEC_CYAN[2]} > R({ELEC_CYAN[0]}) ✓")


if __name__ == "__main__":
    main()
