#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_bg_glitch_layer_encounter.py
Glitch Layer Encounter Background Generator (Compositing Export)
"Luma & the Glitchkin" — Background & Environment Design
Artist: Jordan Reed | Cycle 11

NOTE (Cycle 14 — Alex Chen, Art Director):
  Original file: bg_glitch_layer_encounter.py in output/backgrounds/environments/
  That location and name are non-compliant. Pipeline tools must live in output/tools/
  and use the LTG_TOOL_ category prefix.
  This file is the LTG-compliant copy. Original is retained in environments/ unchanged.

Scene: Frame 02 — Luma and Byte face the Corruption together in the Glitch Layer.
       Low-angle wide shot looking slightly upward. The Corruption mass dominates
       the upper-center of the frame. Character foreground platform is large and
       centered — an arena quality. Two flanking NEAR platforms form a gauntlet.

Compositional intent vs. bg_glitch_layer_frame.py:
  - bg_glitch_layer_frame.py: neutral wide establishing, dispersed platform layout,
    aurora occupies the upper band — the world is vast and passive.
  - bg_glitch_layer_encounter.py: confrontation composition. Platforms converge toward
    the center lower frame, implying the characters are channeled toward a focal point.
    The upper-center void is dominated by a Corruption presence bloom (UV_PURPLE +
    HOT_MAGENTA + VOID_BLACK massing) that replaces the neutral aurora.
    Near platforms flanking left and right close the arena.

Key compositional differences:
  1. CORRUPTION BLOOM: Upper center ~30% of frame — deep UV_PURPLE/HOT_MAGENTA bloom
     instead of the standard aurora band. The Corruption has a physical presence in
     this composition, not just a color field.
  2. CHARACTER STAND PLATFORM: Centered foreground platform, wider, lower — where
     Luma and Byte stand. Occupies H*0.60-H*0.66. This is larger than the
     bg_glitch_layer_frame.py main platform.
  3. FLANKING NEAR PLATFORMS: Left and right near-tier platforms angled inward,
     creating converging sight lines toward center-lower frame (the character).
  4. MID PLATFORMS: Stepped and bridge variants positioned as mid-ground obstacles
     between the character and the Corruption — adds depth to the confrontation space.
  5. MAGENTA RIM on Corruption bloom perimeter — consistent with style_frame_02's
     storm edge spec (HOT_MAGENTA = active Corruption front perimeter color).
  6. REDUCED FLORA: Encounter tension = less ambient biological detail. Flora
     reduced to trace presence on far platforms only.
  7. CORRUPTION PIXEL SCATTER: Falling downward from the bloom (not rising like
     pixel trails) — data decay, not upward energy. Source = the Corruption overhead.

Color authority: master_palette.md
Key rules from MEMORY.md applied:
  - NO title bar — compositing export only (Cycle 7 lesson)
  - NO per-pixel getpixel/putpixel — draw.line() for fills (Cycle 7 lesson)
  - Refresh draw handle after every alpha_composite (Cycle 8 lesson)
  - All depth-tier colors are named constants with GL parent references (Cycle 10 lesson)
  - Glow = filled ellipses or alpha-composite overlay, never outline-only (Cycle 6 lesson)
  - ELEC_CYAN (#00F0FF) for screen/world glow; BYTE_TEAL (#00D4E8) for Byte ONLY (Cycle 7 lesson)
  - Aurora/bloom pass: per-row draw.line() with sinusoidal phase modulation (Cycle 9 lesson)

Save: /home/wipkat/team/output/backgrounds/environments/bg_glitch_layer_encounter.png
"""

import math
import random
from PIL import Image, ImageDraw

# ── Canvas ──────────────────────────────────────────────────────────────────
W, H = 1920, 1080

# ── Canonical Palette (master_palette.md) ───────────────────────────────────
VOID_BLACK        = (10,  10,  20)    # GL-08  #0A0A14 — base background
BELOW_VOID        = (5,   5,   8)    # GL-08a #050508 — abyss under platforms
ELEC_CYAN         = (0,  240, 255)   # GL-01  #00F0FF — near platforms / world glow
DEEP_CYAN         = (0,  168, 180)   # GL-01a #00A8B4 — near platform shadow/edge
UV_PURPLE         = (123, 47, 190)   # GL-04  #7B2FBE — Corruption dominant / aurora
DEEP_VOID         = (58,  16,  96)   # GL-04a #3A1060 — aurora dark band
ATMOS_MID_PURPLE  = (74,  24, 128)   # GL-04b #4A1880 — aurora/bloom mid band
DATA_BLUE         = (43, 127, 255)   # GL-06  #2B7FFF — mid platform reference
ACID_GREEN        = (57, 255,  20)   # GL-03  #39FF14 — pixel flora (trace only)
HOT_MAGENTA       = (255, 45, 107)   # GL-05  #FF2D6B — Corruption active front/edge

# ── Derived Depth-Tier Colors ────────────────────────────────────────────────
# Rendering constructs derived from canonical GL swatches.
# Documented per Naomi Bridges C9-1 / MEMORY.md Cycle 10 lessons.

# NEAR tier: full GL-01 ELEC_CYAN — maximum saturation, maximum brightness
NEAR_COLOR   = ELEC_CYAN              # GL-01 ELEC_CYAN (#00F0FF) — near platforms, full value
NEAR_SHADOW  = DEEP_CYAN              # GL-01a DEEP_CYAN (#00A8B4) — underside shadow
NEAR_EDGE    = (180, 255, 255)        # GL-01 ELEC_CYAN brightened ~30% — top-edge highlight

# MID tier: GL-06 DATA_BLUE desaturated 60% and darkened ~53%
MID_COLOR    = (10,  72, 120)         # GL-06 DATA_BLUE desaturated 60% and darkened 53%
MID_SHADOW   = (6,   40,  72)         # MID_COLOR darkened ~44%
MID_EDGE     = (20, 110, 160)         # MID_COLOR lightened ~53%

# FAR tier: GL-08 VOID_BLACK shifted minimally toward cyan — near-void
FAR_COLOR    = (0,   26,  40)         # GL-08 VOID_BLACK shifted +cyan
FAR_SHADOW   = (0,   14,  22)         # FAR_COLOR darkened ~46%
FAR_EDGE     = (0,   40,  55)         # FAR_COLOR lightened ~54%

# Ghost platforms (lower void — rendering construct only)
GHOST_COLOR  = (0,   28,  38)         # GL-08a BELOW_VOID shifted +cyan for ghost fill
GHOST_EDGE   = (0,   48,  62)         # GHOST_COLOR lightened

# Aurora/bloom cyan-blue bleed (derived from GL-01 ELEC_CYAN desaturated+darkened 14%)
AURORA_CYAN_BLEED = (0, 160, 220)     # GL-01 ELEC_CYAN desaturated and darkened 14%

# Corruption bloom colors (derived from GL-04/GL-05 — encounter-specific rendering)
CORRUPTION_CORE  = (38,  8,  72)      # GL-04a DEEP_VOID (#3A1060) + slight magenta push — Corruption mass fill
CORRUPTION_MID   = (90, 20, 140)      # GL-04 UV_PURPLE (#7B2FBE) darkened 25% — Corruption mid-mass
CORRUPTION_BLOOM = UV_PURPLE          # GL-04 UV_PURPLE (#7B2FBE) — bloom outer edge


def _platform_polygon(draw, px, py, pw, ph, color, shadow_color, edge_color,
                       angle_deg=0, edge_width=1):
    """Draw a (possibly rotated) platform polygon with top-edge highlight and shadow."""
    if angle_deg == 0:
        draw.rectangle([px, py, px + pw, py + ph], fill=color)
        shadow_h = max(3, ph // 3)
        draw.rectangle([px, py + ph, px + pw, py + ph + shadow_h], fill=shadow_color)
        draw.line([(px, py), (px + pw, py)], fill=edge_color, width=edge_width)
    else:
        rad = math.radians(angle_deg)
        cx_p, cy_p = px + pw / 2, py + ph / 2
        corners = [(-pw / 2, -ph / 2), (pw / 2, -ph / 2),
                   (pw / 2,  ph / 2), (-pw / 2,  ph / 2)]
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


def _platform_l_shaped(draw, px, py, pw, ph, color, shadow_color, edge_color,
                        edge_width=1, step_frac=0.45):
    """L-shaped / stepped platform — raised left ledge."""
    draw.rectangle([px, py + ph // 2, px + pw, py + ph], fill=color)
    draw.rectangle([px, py + ph, px + pw, py + ph + max(3, ph // 3)],
                   fill=shadow_color)
    step_w = int(pw * step_frac)
    draw.rectangle([px, py, px + step_w, py + ph // 2], fill=color)
    draw.rectangle([px, py + ph // 2, px + step_w, py + ph // 2 + max(2, ph // 4)],
                   fill=shadow_color)
    draw.line([(px, py), (px + step_w, py)], fill=edge_color, width=edge_width)
    draw.line([(px, py + ph // 2), (px + pw, py + ph // 2)], fill=edge_color, width=edge_width)
    draw.line([(px + step_w, py), (px + step_w, py + ph // 2)],
              fill=edge_color, width=edge_width)


def _platform_bridge(draw, px, py, pw, ph, color, shadow_color, edge_color,
                     edge_width=1):
    """Narrow bridge platform — wide but very thin, suspended quality."""
    thin_h = max(6, min(ph, 8))
    draw.rectangle([px, py, px + pw, py + thin_h], fill=color)
    draw.rectangle([px, py + thin_h, px + pw, py + thin_h + 2], fill=shadow_color)
    draw.line([(px, py), (px + pw, py)], fill=edge_color, width=edge_width)


def _platform_fragmented(draw, px, py, pw, ph, color, shadow_color, edge_color,
                          rng, n_segments=3, edge_width=1):
    """Broken/fragmented platform — 2-3 disconnected segments with randomised gaps."""
    gap_min, gap_max = max(4, pw // 12), max(10, pw // 6)
    total_gap = sum(rng.randint(gap_min, gap_max) for _ in range(n_segments - 1))
    seg_total_w = pw - total_gap
    seg_w = seg_total_w // n_segments
    x_cursor = px
    for i in range(n_segments):
        vy = py + rng.randint(-3, 3)
        vh = max(6, ph + rng.randint(-4, 4))
        draw.rectangle([x_cursor, vy, x_cursor + seg_w, vy + vh], fill=color)
        draw.rectangle([x_cursor, vy + vh, x_cursor + seg_w, vy + vh + max(2, vh // 3)],
                       fill=shadow_color)
        draw.line([(x_cursor, vy), (x_cursor + seg_w, vy)],
                  fill=edge_color, width=edge_width)
        x_cursor += seg_w
        if i < n_segments - 1:
            x_cursor += rng.randint(gap_min, gap_max)


def _draw_flora_cluster(draw, fx, fy, color, rng, size=6):
    """Faint pixel flora cluster hanging below a platform edge (trace presence)."""
    offsets = [(-1, 1), (0, 1), (1, 1), (-1, 2), (1, 2), (0, 3)]
    for (di, dj) in offsets:
        if rng.random() < 0.55:
            sx = fx + di * size
            sy = fy + dj * size
            draw.rectangle([sx, sy, sx + size - 1, sy + size - 1], fill=color)


def generate_glitch_layer_encounter(output_path, seed=77):
    """
    Generate a 1920x1080 Glitch Layer encounter background — compositing export.
    No title bar. No legend. Pure environment configured for the confrontation scene.

    Composition: low-angle, slightly upward-facing.
      - Corruption bloom mass occupies upper-center (~y=0 to y=H*0.38)
      - FAR platforms ring the upper void at mid-horizontal positions
      - MID platforms form the middle-ground obstacle layer
      - NEAR flanking platforms (left and right) angle inward toward center
      - CHARACTER STAND platform: wide centered foreground element
      - Ghost/void platforms populate the lower void
    """
    rng = random.Random(seed)

    # ── BASE: Void Black fill ─────────────────────────────────────────────────
    img = Image.new('RGB', (W, H), VOID_BLACK)
    draw = ImageDraw.Draw(img)

    # ── CORRUPTION BLOOM — upper-center, replaces neutral aurora ─────────────
    # The Corruption has a physical mass presence here — not just ambient color.
    # 3-zone structure (top to bottom):
    #   Zone A: Corruption core — deep UV_PURPLE/DEEP_VOID massing, upper 15%
    #   Zone B: Bloom mid — UV_PURPLE + slight HOT_MAGENTA edge bleed, 10-28%
    #   Zone C: Bloom fade — aurora-style fade to void, 25-40%
    # Central horizontal focus: sinusoidal intensity peaks at frame center (x=W//2)

    # Zone A: Hard mass fill — irregular Corruption silhouette blocks
    # These are drawn as overlapping polygons to break the symmetry of a pure oval.
    corruption_mass_polys = [
        # (center_x_frac, center_y_frac, rx_frac, ry_frac, angle_deg)
        (0.50, 0.09, 0.22, 0.10,   0),   # central core oval
        (0.38, 0.11, 0.14, 0.08,  12),   # left lobe
        (0.62, 0.10, 0.15, 0.07, -10),   # right lobe
        (0.50, 0.04, 0.12, 0.06,   5),   # upper spike
        (0.44, 0.14, 0.10, 0.06, -15),   # lower-left tendril
        (0.56, 0.13, 0.09, 0.05,  18),   # lower-right tendril
    ]
    for (cx_frac, cy_frac, rx_frac, ry_frac, ang) in corruption_mass_polys:
        cx = int(cx_frac * W)
        cy = int(cy_frac * H)
        rx = int(rx_frac * W)
        ry = int(ry_frac * H)
        # Rotate a bounding ellipse approximation using polygon
        rad = math.radians(ang)
        n_pts = 18
        pts = []
        for i in range(n_pts):
            theta = 2 * math.pi * i / n_pts
            ox = rx * math.cos(theta)
            oy = ry * math.sin(theta)
            rx2 = ox * math.cos(rad) - oy * math.sin(rad)
            ry2 = ox * math.sin(rad) + oy * math.cos(rad)
            pts.append((cx + int(rx2), cy + int(ry2)))
        draw.polygon(pts, fill=CORRUPTION_CORE)

    # Zone B: Bloom mid — per-row draw.line() radiating outward from center top
    # Sinusoidal modulation gives the bloom an organic/turbulent edge quality.
    bloom_y0 = 0
    bloom_y1 = int(H * 0.30)
    bloom_center_x = W // 2
    bloom_half_w = int(W * 0.48)  # bloom spreads nearly full width at its widest

    for y in range(bloom_y0, bloom_y1):
        t = y / bloom_y1  # 0 at top, 1 at bottom of bloom
        # Width of active bloom zone grows as we go down, peaks at ~55% depth, fades
        if t < 0.55:
            env = t / 0.55
        else:
            env = 1.0 - (t - 0.55) / 0.45
        env = env ** 1.2

        # Choose color based on zone: upper = CORRUPTION_CORE, lower = UV_PURPLE fade
        if t < 0.30:
            col = CORRUPTION_MID
            alpha_max = 90
        elif t < 0.60:
            col = CORRUPTION_BLOOM
            alpha_max = 70
        else:
            col = ATMOS_MID_PURPLE
            alpha_max = 40

        phase_y = y * 0.030
        active_w = int(bloom_half_w * env)
        for x in range(bloom_center_x - active_w, bloom_center_x + active_w, 3):
            # Radial falloff from center — power-law toward edge of active zone
            dist_frac = abs(x - bloom_center_x) / max(1, active_w)
            radial_env = max(0.0, 1.0 - dist_frac ** 1.6)
            sin_mod = 0.50 + 0.50 * math.sin(x / 180.0 + phase_y)
            alpha = int(alpha_max * env * radial_env * sin_mod)
            if alpha < 4:
                continue
            cr = int(col[0] * alpha / alpha_max)
            cg = int(col[1] * alpha / alpha_max)
            cb = int(col[2] * alpha / alpha_max)
            draw.line([(x, y), (x + 2, y)], fill=(cr, cg, cb))

    # HOT_MAGENTA perimeter rim — the active Corruption front edge
    # A thin sinusoidal band just outside the core mass at y = H*0.14 to H*0.22
    magenta_band_y0 = int(H * 0.13)
    magenta_band_y1 = int(H * 0.23)
    for y in range(magenta_band_y0, magenta_band_y1):
        t = (y - magenta_band_y0) / (magenta_band_y1 - magenta_band_y0)
        # Peak intensity at mid of band
        env = 1.0 - abs(t - 0.5) * 2.0
        env = max(0.0, env) ** 1.5
        # Only paint the outer edges (left and right of center), not the center fill
        edge_w = int(W * 0.12 * (0.6 + 0.4 * math.sin(y * 0.05)))
        bloom_edge = int(bloom_half_w * 0.72 * (0.85 + 0.15 * math.sin(y * 0.04)))
        for side in [-1, 1]:
            x_start = bloom_center_x + side * bloom_edge
            x_end = bloom_center_x + side * (bloom_edge + edge_w)
            if side == -1:
                x_start, x_end = x_end, x_start
            for x in range(x_start, x_end, 2):
                dist_frac = abs(x - (bloom_center_x + side * (bloom_edge + edge_w // 2))) / max(1, edge_w // 2)
                radial_env = max(0.0, 1.0 - dist_frac)
                alpha = int(55 * env * radial_env)
                if alpha < 4:
                    continue
                cr = int(HOT_MAGENTA[0] * alpha / 55)
                cg = int(HOT_MAGENTA[1] * alpha / 55)
                cb = int(HOT_MAGENTA[2] * alpha / 55)
                draw.line([(x, y), (x + 1, y)], fill=(cr, cg, cb))

    # ── FAR PLATFORMS — upper void, flanking the bloom ───────────────────────
    # Positioned at sides to avoid occluding the Corruption mass center.
    far_plats = [
        (int(W * 0.02),  int(H * 0.30), int(W * 0.07),  12,  -6),
        (int(W * 0.14),  int(H * 0.27), int(W * 0.06),  11,   8),
        (int(W * 0.68),  int(H * 0.26), int(W * 0.07),  11,  -7),
        (int(W * 0.81),  int(H * 0.29), int(W * 0.08),  13,   5),
        (int(W * 0.92),  int(H * 0.31), int(W * 0.06),  10,  -4),
        # Two far platforms partially visible behind/below the bloom
        (int(W * 0.28),  int(H * 0.34), int(W * 0.05),  10,   9),
        (int(W * 0.62),  int(H * 0.33), int(W * 0.06),  11,  -8),
    ]
    far_flora_positions = []
    for px, py, pw, ph, angle in far_plats:
        _platform_polygon(draw, px, py, pw, ph, FAR_COLOR, FAR_SHADOW, FAR_EDGE,
                          angle_deg=angle, edge_width=1)
        far_flora_positions.append((px + pw // 2, py))

    # ── MID PLATFORMS — obstacle layer between Corruption and character ────────
    # 3 rect + 1 L-shaped + 1 bridge — distributed left/right of center
    mid_plats_rect = [
        (int(W * 0.03),  int(H * 0.41), int(W * 0.12),  26,  -5),
        (int(W * 0.24),  int(H * 0.44), int(W * 0.09),  24,   7),
        (int(W * 0.63),  int(H * 0.43), int(W * 0.11),  25,  -6),
    ]
    mid_flora_positions = []
    for px, py, pw, ph, angle in mid_plats_rect:
        _platform_polygon(draw, px, py, pw, ph, MID_COLOR, MID_SHADOW, MID_EDGE,
                          angle_deg=angle, edge_width=1)
        mid_flora_positions.append((px, py))
        mid_flora_positions.append((px + pw, py))

    # MID: L-shaped (raised left ledge — gives the mid-ground a stepped quality)
    mid_l_px, mid_l_py = int(W * 0.79), int(H * 0.39)
    mid_l_pw, mid_l_ph = int(W * 0.11), 28
    _platform_l_shaped(draw, mid_l_px, mid_l_py, mid_l_pw, mid_l_ph,
                       MID_COLOR, MID_SHADOW, MID_EDGE, edge_width=1)
    mid_flora_positions.append((mid_l_px, mid_l_py))

    # MID: narrow bridge — crossing element, slightly right of center
    mid_br_px, mid_br_py = int(W * 0.40), int(H * 0.415)
    mid_br_pw, mid_br_ph = int(W * 0.14), 7
    _platform_bridge(draw, mid_br_px, mid_br_py, mid_br_pw, mid_br_ph,
                     MID_COLOR, MID_SHADOW, MID_EDGE, edge_width=1)
    mid_flora_positions.append((mid_br_px, mid_br_py))
    mid_flora_positions.append((mid_br_px + mid_br_pw, mid_br_py))

    # ── NEAR PLATFORMS — flanking, angled inward, confrontation arena walls ───
    # Left flank: angled 8 degrees clockwise (points right — toward center)
    near_flora_positions = []
    near_left_px = int(W * 0.02)
    near_left_py = int(H * 0.50)
    near_left_pw = int(W * 0.18)
    near_left_ph = 44
    _platform_polygon(draw, near_left_px, near_left_py,
                      near_left_pw, near_left_ph,
                      NEAR_COLOR, NEAR_SHADOW, NEAR_EDGE, angle_deg=8, edge_width=2)
    near_flora_positions.append((near_left_px, near_left_py))
    near_flora_positions.append((near_left_px + near_left_pw, near_left_py))

    # Right flank: angled -8 degrees (points left — toward center)
    near_right_px = int(W * 0.79)
    near_right_py = int(H * 0.51)
    near_right_pw = int(W * 0.18)
    near_right_ph = 42
    _platform_polygon(draw, near_right_px, near_right_py,
                      near_right_pw, near_right_ph,
                      NEAR_COLOR, NEAR_SHADOW, NEAR_EDGE, angle_deg=-8, edge_width=2)
    near_flora_positions.append((near_right_px, near_right_py))
    near_flora_positions.append((near_right_px + near_right_pw, near_right_py))

    # NEAR: fragmented platform — upper center, between the flanks and the mid layer
    # Reads as broken debris between the character's position and the Corruption
    near_fr_px = int(W * 0.37)
    near_fr_py = int(H * 0.485)
    near_fr_pw = int(W * 0.26)
    near_fr_ph = 38
    _platform_fragmented(draw, near_fr_px, near_fr_py, near_fr_pw, near_fr_ph,
                         NEAR_COLOR, NEAR_SHADOW, NEAR_EDGE, rng, n_segments=4,
                         edge_width=2)
    near_flora_positions.append((near_fr_px, near_fr_py))
    near_flora_positions.append((near_fr_px + near_fr_pw, near_fr_py))

    # ── CHARACTER STAND PLATFORM — wide, centered, foreground ─────────────────
    # This is where Luma and Byte stand to face the Corruption.
    # Wider and lower than bg_glitch_layer_frame.py's main platform to give the
    # scene an arena floor quality. Slight inward taper (notch on right side)
    # adds visual tension — the platform is not entirely safe.
    stand_py   = int(H * 0.62)
    stand_ph   = 66
    stand_x0   = int(W * 0.12)
    stand_x1   = int(W * 0.88)
    draw.rectangle([stand_x0, stand_py, stand_x1, stand_py + stand_ph], fill=NEAR_COLOR)
    draw.rectangle([stand_x0, stand_py + stand_ph, stand_x1, stand_py + stand_ph + 22],
                   fill=NEAR_SHADOW)
    draw.line([(stand_x0, stand_py), (stand_x1, stand_py)], fill=NEAR_EDGE, width=3)
    # Edge notch — a cracked/missing section right of center (Corruption damage)
    notch_x0 = int(W * 0.58)
    notch_x1 = int(W * 0.66)
    draw.rectangle([notch_x0, stand_py, notch_x1, stand_py + stand_ph // 3], fill=VOID_BLACK)
    # Notch edge in NEAR_SHADOW (exposed underside)
    draw.line([(notch_x0, stand_py + stand_ph // 3), (notch_x1, stand_py + stand_ph // 3)],
              fill=NEAR_SHADOW, width=2)
    near_flora_positions.append((stand_x0, stand_py))
    near_flora_positions.append((stand_x1, stand_py))
    near_flora_positions.append((stand_x0 + (stand_x1 - stand_x0) // 2, stand_py))

    void_floor_y = stand_py + stand_ph + 22

    # ── PIXEL TRAILS — rising from near and mid platforms ─────────────────────
    # Same upward-rising mechanic as bg_glitch_layer_frame.py (Cycle 9 lesson:
    # trails rise upward from platform surfaces, y-weighted near platform top).
    for (flora_x, flora_y) in near_flora_positions + mid_flora_positions:
        n_trails = rng.randint(1, 4)
        for _ in range(n_trails):
            tx = flora_x + rng.randint(-25, 25)
            t_len = rng.randint(20, 75)
            base_br = rng.randint(40, 110)
            for t_i in range(t_len):
                ty = flora_y - t_i
                if ty < 0:
                    break
                fade = int(base_br * (1.0 - t_i / t_len) ** 1.4)
                if fade < 6:
                    continue
                draw.line([(tx, ty), (tx + 1, ty)], fill=(0, fade, int(fade * 1.05)))

    # ── CORRUPTION PIXEL SCATTER — falling DOWNWARD from the bloom ────────────
    # This is the compositional inverse of the upward-rising pixel trails.
    # Data decay from the Corruption falls toward the character's platform.
    # Colors: UV_PURPLE and HOT_MAGENTA tones — Corruption palette only.
    # ACID_GREEN is NOT present (Corruption is hostile, not healthy).
    corruption_scatter_colors = [
        (60, 12, 100),    # GL-04 UV_PURPLE at ~50% luminance
        (35, 6,  65),     # GL-04 UV_PURPLE at ~30% luminance
        (90, 14,  40),    # GL-05 HOT_MAGENTA at ~35% luminance
        (50, 8,   22),    # GL-05 HOT_MAGENTA at ~20% luminance
    ]
    for _ in range(45):
        tx = rng.randint(int(W * 0.15), int(W * 0.85))
        t_len = rng.randint(10, 55)
        t_col = rng.choice(corruption_scatter_colors)
        # y-weighted: concentrate near top of the void (just above mid platforms)
        # falling from bloom region (y=H*0.25) toward mid-platform level
        rel_y = rng.random() ** 1.8
        ty_start = int(H * 0.25) + int(rel_y * (stand_py - int(H * 0.25) - t_len))
        for t_i in range(t_len):
            ty = ty_start + t_i  # falling downward
            if ty >= stand_py:
                break
            fade = int(75 * (1.0 - t_i / t_len) ** 1.2)
            if fade < 6:
                continue
            draw.rectangle([tx, ty, tx + 2, ty + 1], fill=t_col)

    # ── LOWER VOID — ghost pixel debris (same approach as bg_glitch_layer_frame) ─
    # Rendering construct: dim near-void variants, y-weighted toward platform base.
    lower_debris_colors = [
        (0, 45, 65),    # GL-01 ELEC_CYAN at ~25% luminance
        (0, 30, 48),    # GL-01 ELEC_CYAN at ~19% luminance
        (20, 8, 50),    # GL-04 UV_PURPLE at ~8% luminance
        (0, 18, 28),    # FAR_COLOR dimmed ~50%
    ]
    for _ in range(50):
        tx = rng.randint(0, W)
        t_len = rng.randint(10, 70)
        t_col = rng.choice(lower_debris_colors)
        rel_y = rng.random() ** 2.2
        ty_start = void_floor_y + int(rel_y * (H - void_floor_y - t_len - 10))
        for t_i in range(t_len):
            ty = ty_start + t_i
            if ty >= H:
                break
            fade = int(80 * (1.0 - t_i / t_len))
            if fade < 8:
                continue
            draw.rectangle([tx, ty, tx + 2, ty + 1], fill=t_col)

    # ── GHOST / DISTANT PLATFORMS in lower void ───────────────────────────────
    ghost_count = rng.randint(6, 10)
    for _ in range(ghost_count):
        gx = rng.randint(30, W - 220)
        gy = rng.randint(void_floor_y + 12, H - 24)
        gw = rng.randint(50, 180)
        draw.rectangle([gx, gy, gx + gw, gy + 7], fill=GHOST_COLOR)
        draw.rectangle([gx, gy + 7, gx + gw, gy + 10], fill=BELOW_VOID)
        draw.line([(gx, gy), (gx + gw, gy)], fill=GHOST_EDGE, width=1)

    # ── PIXEL FLORA — trace only on FAR platforms (reduced for encounter tension) ─
    # In a confrontation scene, the biological ambient detail is suppressed.
    # Only far platforms get minimal flora — the near and mid platforms are stripped.
    flora_dim_far = (int(ACID_GREEN[0] * 0.05), int(ACID_GREEN[1] * 0.05), int(ACID_GREEN[2] * 0.05))
    for (fx, fy) in far_flora_positions[:4]:
        if rng.random() < 0.30:
            _draw_flora_cluster(draw, fx, fy, flora_dim_far, rng, size=3)

    # ── CORRUPTION BLOOM GLOW OVERLAY — alpha-composite soft luminous depth ────
    # A separate RGBA pass that adds smooth gradient wash beneath the scan-line bloom.
    # Refreshes the draw handle after composite (Cycle 8 lesson).
    bloom_overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    bov_draw = ImageDraw.Draw(bloom_overlay)

    bloom_glow_regions = [
        # (y_center_frac, half_height_frac, color, peak_alpha)
        (0.07,  0.10, CORRUPTION_BLOOM,  60),
        (0.14,  0.08, ATMOS_MID_PURPLE,  45),
        (0.22,  0.07, UV_PURPLE,         35),
        (0.28,  0.06, HOT_MAGENTA,       20),  # Magenta perimeter glow
    ]
    for (yc_frac, hy_frac, color, alpha_peak) in bloom_glow_regions:
        yc = int(yc_frac * H)
        hy = int(hy_frac * H)
        for y in range(max(0, yc - hy), min(H, yc + hy)):
            t = abs(y - yc) / hy
            alpha = int(alpha_peak * (1.0 - t) ** 2)
            if alpha < 3:
                continue
            bov_draw.line([(0, y), (W, y)],
                          fill=(color[0], color[1], color[2], alpha))

    img = img.convert('RGBA')
    img.alpha_composite(bloom_overlay)
    img = img.convert('RGB')
    draw = ImageDraw.Draw(img)  # refresh draw after composite (Cycle 8 lesson)

    # ── SAVE ──────────────────────────────────────────────────────────────────
    img.save(output_path)
    print(f"Saved: {output_path}")


if __name__ == '__main__':
    generate_glitch_layer_encounter(
        '/home/wipkat/team/output/backgrounds/environments/bg_glitch_layer_encounter.png'
    )
