# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
#!/usr/bin/env python3
"""
LTG_TOOL_bg_glitchlayer_frame.py — Glitch Layer Background v003
"Luma & the Glitchkin" — Background & Environment Design
Artist: Kai Nakamura | Cycle 21

Based on: LTG_TOOL_bg_glitch_layer_frame.py (Jordan Reed, Cycle 9)

Change from v001/v002:
  - scanline_overlay() from ltg_render_lib applied as the final compositing pass.
    The Glitch Layer is literally a CRT screen interior — scanlines are canonical.
    spacing=4, alpha=18 — visible but not overpowering; reinforces CRT quality.

All visual content (aurora bands, platforms, pixel trails, flora, ghost platforms)
is unchanged from v001 — only the final step is added.

Output: /home/wipkat/team/output/backgrounds/environments/LTG_ENV_glitchlayer_frame.png
"""

import math
import random
import os
import sys
from PIL import Image, ImageDraw

# Import shared rendering library (same directory)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from LTG_TOOL_render_lib import scanline_overlay  # noqa: E402

# ── Canvas ──────────────────────────────────────────────────────────────────
W, H = 1920, 1080

# ── Palette (master_palette.md canonical) ───────────────────────────────────
VOID_BLACK        = (10,  10,  20)
BELOW_VOID        = (5,   5,   8)
ELEC_CYAN         = (0,  240, 255)
DEEP_CYAN         = (0,  168, 180)
UV_PURPLE         = (123, 47, 190)
DEEP_VOID         = (58,  16,  96)
ATMOS_MID_PURPLE  = (74,  24, 128)
DATA_BLUE         = (43, 127, 255)
DEEP_DATA_BLUE    = (16,  64, 160)
ACID_GREEN        = (57, 255,  20)

# Depth tiers
NEAR_COLOR   = ELEC_CYAN
NEAR_SHADOW  = DEEP_CYAN
NEAR_EDGE    = (180, 255, 255)

MID_COLOR    = (10,  72, 120)
MID_SHADOW   = (6,   40,  72)
MID_EDGE     = (20, 110, 160)

FAR_COLOR    = (0,   26,  40)
FAR_SHADOW   = (0,   14,  22)
FAR_EDGE     = (0,   40,  55)

GHOST_COLOR  = (0,   28,  38)
GHOST_EDGE   = (0,   48,  62)


def _platform_polygon(draw, px, py, pw, ph, color, shadow_color, edge_color,
                      angle_deg=0, edge_width=1):
    """Draw a platform as a (possibly rotated) polygon with a top-edge highlight."""
    if angle_deg == 0:
        draw.rectangle([px, py, px + pw, py + ph], fill=color)
        shadow_h = max(3, ph // 3)
        draw.rectangle([px, py + ph, px + pw, py + ph + shadow_h], fill=shadow_color)
        draw.line([(px, py), (px + pw, py)], fill=edge_color, width=edge_width)
    else:
        rad = math.radians(angle_deg)
        cx_p, cy_p = px + pw / 2, py + ph / 2
        corners = [(-pw / 2, -ph / 2), (pw / 2, -ph / 2),
                   (pw / 2,  ph / 2),  (-pw / 2, ph / 2)]
        rotated = []
        for (ox, oy) in corners:
            rx2 = ox * math.cos(rad) - oy * math.sin(rad)
            ry2 = ox * math.sin(rad) + oy * math.cos(rad)
            rotated.append((cx_p + rx2, cy_p + ry2))
        draw.polygon(rotated, fill=color)
        shadow_offset = ph // 3
        shadow_pts = [(x, y + shadow_offset) for x, y in rotated]
        draw.polygon(shadow_pts, fill=shadow_color)
        draw.line([rotated[0], rotated[1]], fill=edge_color, width=edge_width)


def _draw_flora_cluster(draw, fx, fy, color, rng, size=6):
    """Draw a faint pixel flora cluster hanging below a platform edge."""
    offsets = [
        (-1, 1), (0, 1), (1, 1),
        (-1, 2), (1, 2),
        (0, 3),
    ]
    for (di, dj) in offsets:
        if rng.random() < 0.65:
            sx = fx + di * size
            sy = fy + dj * size
            draw.rectangle([sx, sy, sx + size - 1, sy + size - 1], fill=color)


def generate_glitch_layer_frame(output_path, seed=42):
    """
    Generate a full 1920x1080 Glitch Layer background with CRT scanline overlay.
    All platform/aurora/flora/pixel-trail content from v001 is preserved.
    Final pass applies ltg_render_lib.scanline_overlay() for CRT screen authenticity.
    """
    rng = random.Random(seed)

    # ── BASE: Void Black fill ─────────────────────────────────────────────────
    img = Image.new('RGB', (W, H), VOID_BLACK)
    draw = ImageDraw.Draw(img)

    # ── AURORA BAND ───────────────────────────────────────────────────────────
    aurora_spec = [
        (0.00, 0.12,  UV_PURPLE,       110),
        (0.05, 0.18,  ATMOS_MID_PURPLE, 90),
        (0.11, 0.24,  DATA_BLUE,        70),
        (0.19, 0.30,  (0, 160, 220),    50),
    ]

    for (y_frac_start, y_frac_end, color, alpha_max) in aurora_spec:
        y0 = int(y_frac_start * H)
        y1 = int(y_frac_end * H)
        band_h = max(1, y1 - y0)
        for y in range(y0, y1):
            t = (y - y0) / band_h
            if t < 0.3:
                env = t / 0.3
            else:
                env = 1.0 - (t - 0.3) / 0.7
            env = env ** 1.5

            phase_y = y * 0.025
            for x in range(0, W, 3):
                sin_mod = 0.55 + 0.45 * math.sin(x / 220.0 + phase_y)
                alpha = int(alpha_max * env * sin_mod)
                if alpha < 4:
                    continue
                cr = int(color[0] * alpha / alpha_max)
                cg = int(color[1] * alpha / alpha_max)
                cb = int(color[2] * alpha / alpha_max)
                draw.line([(x, y), (x + 2, y)], fill=(cr, cg, cb))

    # ── FAR PLATFORMS ─────────────────────────────────────────────────────────
    far_plats = [
        (int(W * 0.05),  int(H * 0.28), int(W * 0.08),  14, -5),
        (int(W * 0.22),  int(H * 0.25), int(W * 0.07),  12,  7),
        (int(W * 0.43),  int(H * 0.23), int(W * 0.06),  11, -9),
        (int(W * 0.62),  int(H * 0.27), int(W * 0.09),  13,  4),
        (int(W * 0.79),  int(H * 0.24), int(W * 0.08),  12, -6),
        (int(W * 0.92),  int(H * 0.29), int(W * 0.06),  10,  8),
    ]
    far_flora_positions = []
    for px, py, pw, ph, angle in far_plats:
        _platform_polygon(draw, px, py, pw, ph, FAR_COLOR, FAR_SHADOW, FAR_EDGE,
                          angle_deg=angle, edge_width=1)
        far_flora_positions.append((px + pw // 2, py))
        far_flora_positions.append((px, py))
        far_flora_positions.append((px + pw, py))

    # ── MID PLATFORMS ─────────────────────────────────────────────────────────
    mid_plats = [
        (int(W * 0.02),  int(H * 0.40), int(W * 0.14),  28, -6),
        (int(W * 0.22),  int(H * 0.43), int(W * 0.10),  26,  8),
        (int(W * 0.42),  int(H * 0.37), int(W * 0.12),  30, -5),
        (int(W * 0.61),  int(H * 0.45), int(W * 0.14),  25,  7),
        (int(W * 0.80),  int(H * 0.39), int(W * 0.11),  24, -9),
    ]
    mid_flora_positions = []
    for px, py, pw, ph, angle in mid_plats:
        _platform_polygon(draw, px, py, pw, ph, MID_COLOR, MID_SHADOW, MID_EDGE,
                          angle_deg=angle, edge_width=1)
        mid_flora_positions.append((px, py))
        mid_flora_positions.append((px + pw, py))

    # ── NEAR PLATFORMS ────────────────────────────────────────────────────────
    near_plats = [
        (int(W * 0.06),  int(H * 0.52), int(W * 0.16),  46, -3),
        (int(W * 0.34),  int(H * 0.48), int(W * 0.12),  40,  5),
        (int(W * 0.54),  int(H * 0.55), int(W * 0.18),  44, -4),
        (int(W * 0.79),  int(H * 0.50), int(W * 0.15),  38,  7),
    ]
    near_flora_positions = []
    for px, py, pw, ph, angle in near_plats:
        _platform_polygon(draw, px, py, pw, ph, NEAR_COLOR, NEAR_SHADOW, NEAR_EDGE,
                          angle_deg=angle, edge_width=2)
        near_flora_positions.append((px, py))
        near_flora_positions.append((px + pw, py))

    # ── MAIN FOREGROUND PLATFORM ──────────────────────────────────────────────
    main_py  = int(H * 0.63)
    main_ph  = 58
    main_x0  = int(W * 0.15)
    main_x1  = int(W * 0.82)
    draw.rectangle([main_x0, main_py, main_x1, main_py + main_ph], fill=NEAR_COLOR)
    draw.rectangle([main_x0, main_py + main_ph, main_x1, main_py + main_ph + 20],
                   fill=NEAR_SHADOW)
    draw.line([(main_x0, main_py), (main_x1, main_py)], fill=NEAR_EDGE, width=3)
    near_flora_positions.append((main_x0, main_py))
    near_flora_positions.append((main_x1, main_py))
    near_flora_positions.append((main_x0 + (main_x1 - main_x0) // 2, main_py))

    # ── PIXEL TRAILS ──────────────────────────────────────────────────────────
    void_floor_y = main_py + main_ph + 20

    for (flora_x, flora_y) in near_flora_positions + mid_flora_positions:
        n_trails = rng.randint(2, 5)
        for _ in range(n_trails):
            tx = flora_x + rng.randint(-30, 30)
            t_len = rng.randint(25, 90)
            base_br = rng.randint(50, 120)
            for t_i in range(t_len):
                ty = flora_y - t_i
                if ty < 0:
                    break
                fade = int(base_br * (1.0 - t_i / t_len) ** 1.4)
                if fade < 6:
                    continue
                draw.line([(tx, ty), (tx + 1, ty)], fill=(0, fade, int(fade * 1.05)))

    # ── LOWER VOID GHOST DEBRIS ───────────────────────────────────────────────
    for _ in range(60):
        tx = rng.randint(0, W)
        t_len = rng.randint(12, 80)
        t_col_choice = rng.choice([
            (0, 45, 65),
            (0, 30, 48),
            (20, 8, 50),
            (0, 18, 28),
        ])
        rel_y = rng.random() ** 2.2
        ty_start = void_floor_y + int(rel_y * (H - void_floor_y - t_len - 10))
        for t_i in range(t_len):
            ty = ty_start + t_i
            if ty >= H:
                break
            fade = int(80 * (1.0 - t_i / t_len))
            if fade < 8:
                continue
            draw.rectangle([tx, ty, tx + 2, ty + 1], fill=t_col_choice)

    # ── GHOST PLATFORMS in lower void ─────────────────────────────────────────
    ghost_count = rng.randint(7, 12)
    for _ in range(ghost_count):
        gx = rng.randint(30, W - 250)
        gy = rng.randint(void_floor_y + 15, H - 28)
        gw = rng.randint(60, 200)
        draw.rectangle([gx, gy, gx + gw, gy + 7], fill=GHOST_COLOR)
        draw.rectangle([gx, gy + 7, gx + gw, gy + 10], fill=BELOW_VOID)
        draw.line([(gx, gy), (gx + gw, gy)], fill=GHOST_EDGE, width=1)

    # ── PIXEL FLORA ───────────────────────────────────────────────────────────
    flora_dim_near = (int(ACID_GREEN[0] * 0.22), int(ACID_GREEN[1] * 0.22),
                      int(ACID_GREEN[2] * 0.22))
    flora_dim_mid  = (int(ACID_GREEN[0] * 0.12), int(ACID_GREEN[1] * 0.12),
                      int(ACID_GREEN[2] * 0.12))
    flora_dim_far  = (int(ACID_GREEN[0] * 0.06), int(ACID_GREEN[1] * 0.06),
                      int(ACID_GREEN[2] * 0.06))

    for (fx, fy) in near_flora_positions[:8]:
        if rng.random() < 0.75:
            _draw_flora_cluster(draw, fx, fy, flora_dim_near, rng, size=5)
    for (fx, fy) in mid_flora_positions[:6]:
        if rng.random() < 0.60:
            _draw_flora_cluster(draw, fx, fy, flora_dim_mid, rng, size=4)
    for (fx, fy) in far_flora_positions[:5]:
        if rng.random() < 0.40:
            _draw_flora_cluster(draw, fx, fy, flora_dim_far, rng, size=3)

    # ── AURORA GLOW OVERLAY ───────────────────────────────────────────────────
    aurora_overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    aov_draw = ImageDraw.Draw(aurora_overlay)

    aurora_glow_regions = [
        (0.06,  0.08,  UV_PURPLE,        55),
        (0.13,  0.07,  ATMOS_MID_PURPLE, 40),
        (0.20,  0.06,  DATA_BLUE,        30),
    ]
    for (yc_frac, hy_frac, color, alpha_peak) in aurora_glow_regions:
        yc = int(yc_frac * H)
        hy = int(hy_frac * H)
        for y in range(max(0, yc - hy), min(H, yc + hy)):
            t = abs(y - yc) / hy
            alpha = int(alpha_peak * (1.0 - t) ** 2)
            if alpha < 3:
                continue
            aov_draw.line([(0, y), (W, y)],
                          fill=(color[0], color[1], color[2], alpha))

    img = img.convert('RGBA')
    img.alpha_composite(aurora_overlay)
    img = img.convert('RGB')
    draw = ImageDraw.Draw(img)  # refresh draw after composite

    # ── CRT SCANLINE OVERLAY — final pass via ltg_render_lib ─────────────────
    # The Glitch Layer is literally the interior of a CRT screen.
    # scanline_overlay() adds authentic phosphor-row gaps — spacing=4, alpha=18.
    img = scanline_overlay(img, spacing=4, alpha=18)
    draw = ImageDraw.Draw(img)

    # ── SAVE ──────────────────────────────────────────────────────────────────
    # scanline_overlay returns RGBA; convert back to RGB for final save
    img.convert('RGB').save(output_path)
    print(f"Saved: {output_path}")


if __name__ == '__main__':
    generate_glitch_layer_frame(
        '/home/wipkat/team/output/backgrounds/environments/LTG_ENV_glitchlayer_frame.png'
    )
