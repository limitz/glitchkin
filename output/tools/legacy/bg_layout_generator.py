# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
#!/usr/bin/env python3
"""
Background Layout Generator — Luma & the Glitchkin
Generates 1920x1080px color-block layout compositions.
Cycle 6 v2: Takeshi Murakami Cycle 6 critique fixes applied.
- Luma's House: filled gradient glow (monitor + lamp), couch faces monitor wall,
  individual cables, atmospheric perspective on walls
- Glitch Layer: NEAR/MID contrast 50% step, randomized platform positions,
  pixel flora anchored to platforms, aurora sinusoidal variation, void trails y-weighted
- Millbrook: gap buildings added to fill void-black flanks of clock tower,
  pavement crack HIGH-contrast (lighter than street surface, 4px wide),
  awning shadow does not stack on dark gap regions, varied rooflines
- All: atmospheric perspective — far elements lighter/more desaturated
"""
from PIL import Image, ImageDraw, ImageFont
import math
import random

W, H = 1920, 1080

def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def _get_fonts():
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
        font_sm = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
        font_xs = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 15)
    except:
        font = font_title = font_sm = font_xs = ImageFont.load_default()
    return font, font_title, font_sm, font_xs

def _title_bar(draw, scene_name, font_title):
    draw.rectangle([0, 0, W, 52], fill=(10, 10, 20))
    draw.text((20, 10), f"LUMA & THE GLITCHKIN — {scene_name}", fill=(240, 235, 220), font=font_title)

def _draw_filled_glow(draw, cx, cy, rx, ry, glow_rgb, bg_rgb, steps=12):
    """Draw filled gradient glow as concentric filled ellipses from glow color to bg color."""
    for i in range(steps, 0, -1):
        t = i / steps  # 1.0 at edge, approaches 0 at center... reversed: draw outer first
        # outer steps are bg-colored, inner steps are glow-colored
        r_v = int(bg_rgb[0] + (glow_rgb[0] - bg_rgb[0]) * (1 - t))
        g_v = int(bg_rgb[1] + (glow_rgb[1] - bg_rgb[1]) * (1 - t))
        b_v = int(bg_rgb[2] + (glow_rgb[2] - bg_rgb[2]) * (1 - t))
        er = int(rx * t)
        er_y = int(ry * t)
        if er > 0 and er_y > 0:
            draw.ellipse([cx - er, cy - er_y, cx + er, cy + er_y], fill=(r_v, g_v, b_v))

def _atmos_desaturate(color, factor):
    """Push a color toward a neutral light gray to simulate atmospheric perspective.
    factor 0.0 = no change, 1.0 = fully neutral (200,200,200)"""
    target = (200, 200, 200)
    return tuple(int(c + (target[i] - c) * factor) for i, c in enumerate(color))


# ── Luma's House Interior ─────────────────────────────────────────────────────

def generate_lumas_house(output_path):
    img = Image.new('RGB', (W, H), (10, 10, 20))
    draw = ImageDraw.Draw(img)
    font, font_title, font_sm, font_xs = _get_fonts()

    # ── CEILING PLANE (12% from top) ──────────────────────────────────────────
    ceiling_y = int(H * 0.12)
    draw.rectangle([0, 0, W, ceiling_y], fill=(90, 55, 22))  # dark warm amber — ceiling
    draw.line([(0, ceiling_y), (W, ceiling_y)], fill=(60, 36, 14), width=3)
    draw.text((20, 14), "Ceiling — Dark Amber #5A3716", fill=(200, 160, 100), font=font_xs)

    # ── UPPER WALL — atmospheric perspective: back wall lighter/more desaturated ─
    # Interpolate per scanline from ceiling_y down to wainscot, gradually lightening
    wall_top_y = ceiling_y
    wall_bot_y = int(H * 0.55)
    base_wall = (212, 146, 58)   # full warm amber at midground
    far_wall  = (228, 185, 120)  # lighter, more desaturated at back (distance)
    for y in range(wall_top_y, wall_bot_y):
        t = (y - wall_top_y) / max(1, wall_bot_y - wall_top_y)
        # top of wall is the farthest away — lighter
        r_v = int(far_wall[0] + (base_wall[0] - far_wall[0]) * t)
        g_v = int(far_wall[1] + (base_wall[1] - far_wall[1]) * t)
        b_v = int(far_wall[2] + (base_wall[2] - far_wall[2]) * t)
        draw.line([(0, y), (W, y)], fill=(r_v, g_v, b_v), width=1)

    # ── LOWER WALL / WAINSCOT ─────────────────────────────────────────────────
    draw.rectangle([0, int(H * 0.55), W, int(H * 0.75)], fill=(140, 90, 26))

    # ── FLOOR ─────────────────────────────────────────────────────────────────
    draw.rectangle([0, int(H * 0.75), W, H], fill=(90, 56, 32))
    draw.text((20, int(H * 0.76)), "Floor — Deep Terracotta", fill=(200, 160, 100), font=font_xs)

    # ── MONITOR WALL — dominant cold element (right side, mid-height) ─────────
    # Monitor wall background (darker alcove)
    mw_x, mw_y = int(W * 0.52), ceiling_y + 5
    mw_w, mw_h = int(W * 0.36), int(H * 0.55)
    draw.rectangle([mw_x, mw_y, mw_x + mw_w, mw_y + mw_h], fill=(22, 16, 30))
    draw.text((mw_x + 10, mw_y + 8), "Monitor Wall — Void #16101E", fill=(100, 90, 140), font=font_xs)

    # Multiple monitor screens — varied sizes
    monitor_specs = [
        (mw_x + 30,  mw_y + 20,  220, 140),
        (mw_x + 270, mw_y + 15,  280, 170),
        (mw_x + 570, mw_y + 30,  200, 120),
        (mw_x + 40,  mw_y + 175, 240, 150),
        (mw_x + 295, mw_y + 200, 260, 155),
        (mw_x + 570, mw_y + 165, 190, 140),
    ]
    for mx, my, mw_s, mh_s in monitor_specs:
        # Monitor casing
        draw.rectangle([mx - 4, my - 4, mx + mw_s + 4, my + mh_s + 4],
                       fill=(12, 10, 18), outline=(30, 24, 42), width=2)
        # Screen — active electric cyan
        draw.rectangle([mx, my, mx + mw_s, my + mh_s], fill=(0, 212, 232))
        # Screen hot center — filled gradient glow (not outline rings)
        cx_m, cy_m = mx + mw_s // 2, my + mh_s // 2
        _draw_filled_glow(draw, cx_m, cy_m,
                          mw_s // 2, mh_s // 2,
                          glow_rgb=(180, 255, 255),
                          bg_rgb=(0, 212, 232),
                          steps=10)

    # ── MONITOR GLOW AS LIGHT SOURCE ──────────────────────────────────────────
    # The monitors are a LIGHT SOURCE — the glow extends as a gradient spill
    # onto three planes: the warm wall to the left, the floor below, and the
    # ceiling above.  There is NO circular halo around the monitor panel.

    # 1) WALL SPILL — horizontal gradient from monitor wall leftward onto warm wall
    #    Warm wall base: (212, 146, 58).  Glow tint at source: (0, 55, 80) cyan.
    #    We sample at the vertical midpoint of the wall for the column color, which
    #    is close enough for a layout pass and avoids a nested per-pixel loop.
    glow_reach_wall = int(W * 0.30)  # how far the glow spills left
    wall_mid_y = (ceiling_y + int(H * 0.75)) // 2
    for x in range(mw_x, mw_x - glow_reach_wall, -1):
        dist = mw_x - x
        t = dist / glow_reach_wall          # 0 at wall edge, 1 at spill limit
        strength = (1.0 - t) ** 1.5
        if strength < 0.005:
            continue
        # Use a single representative warm color for this column (mid-wall tone)
        warm_base = (190, 140, 65)
        cyan_tint = (0, 55, 80)
        blended = (
            int(warm_base[0] + (cyan_tint[0] - warm_base[0]) * strength * 0.45),
            int(warm_base[1] + (cyan_tint[1] - warm_base[1]) * strength * 0.40),
            int(warm_base[2] + (cyan_tint[2] - warm_base[2]) * strength * 0.40),
        )
        draw.line([(x, ceiling_y), (x, int(H * 0.75))], fill=blended)

    # 2) FLOOR SPILL — gradient from monitor wall base spreading left across floor
    #    Floor base: (90, 56, 32).  Glow tint: (0, 40, 65) dark cyan.
    floor_y_ln = int(H * 0.75)
    glow_reach_floor = int(W * 0.42)  # floor spill extends further (light travels along floor)
    for x in range(W, int(mw_x - glow_reach_floor), -1):
        dist = W - x
        t = dist / max(1, W - (mw_x - glow_reach_floor))
        strength = (1.0 - t) ** 1.6
        if strength < 0.005:
            continue
        floor_base = (90, 56, 32)
        if x > mw_x:
            floor_base = (0, 35, 50)  # under the monitor wall itself — deep cold
        cyan_floor = (0, 48, 70)
        blended = (
            int(floor_base[0] + (cyan_floor[0] - floor_base[0]) * strength * 0.80),
            int(floor_base[1] + (cyan_floor[1] - floor_base[1]) * strength * 0.72),
            int(floor_base[2] + (cyan_floor[2] - floor_base[2]) * strength * 0.72),
        )
        draw.line([(x, floor_y_ln), (x, H)], fill=blended)

    # 3) CEILING SPILL — gradient from monitor wall spreading left across ceiling
    #    Ceiling base: (90, 55, 22).  Glow tint: (0, 50, 75) dark cyan.
    glow_reach_ceil = int(W * 0.32)
    for x in range(W, int(mw_x - glow_reach_ceil), -1):
        dist = W - x
        t = dist / max(1, W - (mw_x - glow_reach_ceil))
        strength = (1.0 - t) ** 1.8
        if strength < 0.005:
            continue
        ceil_base = (90, 55, 22)
        cyan_ceil = (0, 50, 75)
        blended = (
            int(ceil_base[0] + (cyan_ceil[0] - ceil_base[0]) * strength * 0.60),
            int(ceil_base[1] + (cyan_ceil[1] - ceil_base[1]) * strength * 0.55),
            int(ceil_base[2] + (cyan_ceil[2] - ceil_base[2]) * strength * 0.55),
        )
        draw.line([(x, 0), (x, ceiling_y)], fill=blended)

    # Re-draw the actual monitor content on top of all glow layers
    for mx, my, mw_s, mh_s in monitor_specs:
        draw.rectangle([mx - 4, my - 4, mx + mw_s + 4, my + mh_s + 4],
                       fill=(12, 10, 18), outline=(30, 24, 42), width=2)
        draw.rectangle([mx, my, mx + mw_s, my + mh_s], fill=(0, 212, 232))
        cx_m, cy_m = mx + mw_s // 2, my + mh_s // 2
        _draw_filled_glow(draw, cx_m, cy_m,
                          mw_s // 2, mh_s // 2,
                          glow_rgb=(180, 255, 255),
                          bg_rgb=(0, 212, 232),
                          steps=8)
    draw.text((mw_x + 20, int(H * 0.78)), "Monitor glow — LIGHT SOURCE spill (floor/ceiling/wall)", fill=(0, 160, 180), font=font_xs)

    # ── COUCH — faces monitor wall (couch on left, sightline toward right/monitors) ─
    # Couch positioned at left/center of frame.
    # Right side of couch is the "back" (farther away), angled so the character
    # sitting here would be looking toward the RIGHT — directly at the monitor wall.
    # The couch's long axis points left-to-right: near end bottom-left, far end upper-right.
    # But the "face" of the couch (where someone sits looking forward) opens RIGHTWARD.
    # We achieve this by rotating the couch: back is on the LEFT, seat faces RIGHT.
    couch_pts = [
        (int(W * 0.06),  int(H * 0.68)),  # front-left corner (near camera)
        (int(W * 0.06),  int(H * 0.58)),  # back-left corner
        (int(W * 0.38),  int(H * 0.54)),  # back-right corner (farther away)
        (int(W * 0.38),  int(H * 0.64)),  # front-right corner
    ]
    draw.polygon(couch_pts, fill=(107, 48, 24))
    draw.polygon(couch_pts, outline=(70, 30, 14), width=3)
    # Couch back cushion — on the LEFT (back of the couch, character faces right)
    back_pts = [
        (int(W * 0.06),  int(H * 0.58)),
        (int(W * 0.06),  int(H * 0.52)),
        (int(W * 0.16),  int(H * 0.50)),
        (int(W * 0.16),  int(H * 0.56)),
    ]
    draw.polygon(back_pts, fill=(128, 60, 28))
    draw.polygon(back_pts, outline=(80, 40, 16), width=2)
    # Arrow suggesting sightline from couch to monitor wall
    draw.line([(int(W*0.25), int(H*0.60)), (int(W*0.48), int(H*0.55))],
              fill=(220, 160, 60), width=2)
    draw.text((int(W * 0.08), int(H * 0.59)), "Couch — faces monitor wall (sightline ->)", fill=(220, 180, 120), font=font_xs)

    # ── LAMP — pure warm zone only (not overlapping monitor cold zone) ─────────
    lamp_x = int(W * 0.40)
    lamp_y = ceiling_y + 20
    # Lamp glow: FILLED gradient (warm), stays LEFT of monitor wall
    _draw_filled_glow(draw, lamp_x + 28, lamp_y + 40,
                      rx=140, ry=80,
                      glow_rgb=(245, 200, 66),
                      bg_rgb=(212, 146, 58),
                      steps=10)
    # Lamp body on top
    draw.rectangle([lamp_x, lamp_y, lamp_x + 55, lamp_y + 75], fill=(245, 200, 66))
    draw.text((lamp_x - 60, lamp_y + 80), "Lamp — filled warm glow, no cold overlap", fill=(200, 170, 80), font=font_xs)

    # ── CABLE CLUTTER foreground — individual distinct cables ─────────────────
    # Dark floor strip base
    draw.rectangle([0, int(H * 0.90), W, H], fill=(42, 26, 16))
    # Individual cables: varied arc paths, colors, heights, radii
    cable_defs = [
        # (x_start, x_end, arc_height_base, arc_radius, color, thickness)
        (60,   380, int(H*0.915), 55,  (0, 212, 232),   2),   # cyan cable, left sweep
        (200,  700, int(H*0.930), 80,  (255, 45, 107),   2),   # pink cable, wider arc
        (350,  900, int(H*0.910), 40,  (180, 140, 80),   2),   # tan/brown cable
        (500, 1100, int(H*0.945), 65,  (0, 180, 255),    1),   # blue cable
        (750, 1400, int(H*0.920), 90,  (255, 200, 0),    2),   # yellow cable
        (900, 1600, int(H*0.938), 50,  (200, 80, 200),   1),   # purple cable
        (1100,1850, int(H*0.912), 70,  (0, 212, 232),    2),   # second cyan
        (1400,1900, int(H*0.950), 35,  (255, 45, 107),   1),   # short pink at far right
        (80,   550, int(H*0.955), 30,  (100, 100, 100),  1),   # gray shadow cable
    ]
    for x0, x1, base_y, arc_r, color, thickness in cable_defs:
        mid_x = (x0 + x1) // 2
        pts = []
        steps = 30
        for s in range(steps + 1):
            t = s / steps
            # Quadratic bezier-like arc: sag down at midpoint
            px = int(x0 + (x1 - x0) * t)
            # parabolic sag
            sag = int(arc_r * 4 * t * (1 - t))
            py = base_y + sag
            pts.append((px, py))
        for i in range(len(pts) - 1):
            draw.line([pts[i], pts[i+1]], fill=color, width=thickness)
    draw.text((20, int(H * 0.915)), "Cable clutter — individual distinct cables", fill=(160, 130, 90), font=font_xs)

    # ── TITLE BAR ─────────────────────────────────────────────────────────────
    _title_bar(draw, "Luma's House Interior — Layout v4 (Cycle 6 Rev2)", font_title)

    img.save(output_path)
    print(f"Saved: {output_path}")


# ── Glitch Layer ───────────────────────────────────────────────────────────────

def generate_glitch_layer(output_path, seed=99):
    img = Image.new('RGB', (W, H), (8, 6, 14))  # Deep void
    draw = ImageDraw.Draw(img)
    font, font_title, font_sm, font_xs = _get_fonts()
    rng = random.Random(seed)

    # ── UPPER AURORA / DATA STREAMS (~top 25%) — sinusoidal horizontal variation ──
    aurora_bands = [
        (0,           int(H * 0.08),  (123, 47, 190), "UV Aurora"),
        (int(H*0.05), int(H * 0.10),  (0, 120, 200),  "Data Blue"),
        (int(H*0.12), int(H * 0.10),  (0, 200, 232),  "Cyan fade"),
    ]
    for band_y, band_h, color, label in aurora_bands:
        for y in range(band_y, band_y + band_h):
            t = (y - band_y) / band_h
            base_fade = int(90 * (1 - t) * (1 - t))
            for x in range(0, W, 4):
                # Sinusoidal variation across x: phase shifts per y for streaming effect
                phase = y * 0.03
                sin_mod = 0.5 + 0.5 * math.sin(x / 180.0 + phase)
                fade = int(base_fade * (0.6 + 0.4 * sin_mod))
                r_c = int(color[0] * fade / 90)
                g_c = int(color[1] * fade / 90)
                b_c = int(color[2] * fade / 90)
                draw.rectangle([x, y, x + 3, y], fill=(r_c, g_c, b_c))

    # Code waterfall (right side)
    for i in range(0, int(H * 0.6), 18):
        intensity = max(0, 140 - i // 4)
        draw.text((W - 72, i + 60), "01", fill=(0, intensity, 0), font=font_xs)
        draw.text((W - 45, i + 68), "10", fill=(0, max(0, intensity - 20), 0), font=font_xs)

    # ── 3-TIER PLATFORM VALUE HIERARCHY — 50% contrast step NEAR/MID ────────────
    # NEAR platforms: brightest #00F0FF
    near_color  = (0, 240, 255)
    near_shadow = (0, 144, 176)
    # MID platforms: ~50% value step down from NEAR — (0,120,145)
    mid_color   = (0, 120, 145)
    mid_shadow  = (0, 72, 90)
    # FAR platforms: deep background — desaturated, darker
    far_color   = (0, 55, 72)
    far_shadow  = (0, 32, 45)

    # Helper: draw platform as rotated polygon for far/mid platforms (adds alienness)
    def _platform_polygon(draw, px, py, pw, ph, color, shadow_color, angle_deg=0):
        """Draw a platform as a (possibly rotated) polygon."""
        if angle_deg == 0:
            draw.rectangle([px, py, px + pw, py + ph], fill=color)
            draw.rectangle([px, py + ph, px + pw, py + ph + max(4, ph//3)], fill=shadow_color)
        else:
            rad = math.radians(angle_deg)
            cx_p, cy_p = px + pw / 2, py + ph / 2
            corners = [(-pw/2, -ph/2), (pw/2, -ph/2), (pw/2, ph/2), (-pw/2, ph/2)]
            rotated = []
            for (ox, oy) in corners:
                rx2 = ox * math.cos(rad) - oy * math.sin(rad)
                ry2 = ox * math.sin(rad) + oy * math.cos(rad)
                rotated.append((cx_p + rx2, cy_p + ry2))
            draw.polygon(rotated, fill=color)
            # Shadow: shift corners down by ph//3
            shad = [(x, y + ph // 3) for x, y in rotated]
            draw.polygon(shad, fill=shadow_color)

    # Far platforms — small, high in frame, desaturated, slight rotation, irregular spacing
    far_plats = [
        (int(W * 0.07),  int(H * 0.22), int(W * 0.09), 16,  -4),
        (int(W * 0.28),  int(H * 0.19), int(W * 0.07), 14,   6),
        (int(W * 0.51),  int(H * 0.17), int(W * 0.06), 12,  -8),
        (int(W * 0.72),  int(H * 0.23), int(W * 0.10), 15,   3),
        (int(W * 0.89),  int(H * 0.20), int(W * 0.07), 14,  -5),
    ]
    for px, py, pw, ph, angle in far_plats:
        _platform_polygon(draw, px, py, pw, ph, far_color, far_shadow, angle)

    # Mid platforms — varied heights, irregular x, slight rotation
    mid_plats = [
        (int(W * 0.04),  int(H * 0.35), int(W * 0.13), 26,  -6),
        (int(W * 0.26),  int(H * 0.38), int(W * 0.09), 24,   9),
        (int(W * 0.47),  int(H * 0.32), int(W * 0.11), 28,  -5),
        (int(W * 0.65),  int(H * 0.42), int(W * 0.13), 24,   7),
        (int(W * 0.82),  int(H * 0.36), int(W * 0.10), 22, -10),
    ]
    pixel_flora_positions = []  # collect platform edges for flora placement
    for px, py, pw, ph, angle in mid_plats:
        _platform_polygon(draw, px, py, pw, ph, mid_color, mid_shadow, angle)
        # Top edge highlight
        draw.line([(px, py), (px + pw, py)], fill=(0, 180, 210), width=1)
        # Record corners for flora anchoring
        pixel_flora_positions.append((px, py))
        pixel_flora_positions.append((px + pw, py))

    # Near / foreground platforms — largest, brightest, most saturated, more irregular
    near_plats = [
        (int(W * 0.08),  int(H * 0.50), int(W * 0.18), 44,  -3),
        (int(W * 0.38),  int(H * 0.46), int(W * 0.11), 38,   5),
        (int(W * 0.56),  int(H * 0.53), int(W * 0.17), 42,  -4),
        (int(W * 0.80),  int(H * 0.48), int(W * 0.14), 36,   8),
    ]
    for px, py, pw, ph, angle in near_plats:
        _platform_polygon(draw, px, py, pw, ph, near_color, near_shadow, angle)
        draw.line([(px, py), (px + pw, py)], fill=(180, 255, 255), width=2)
        pixel_flora_positions.append((px, py))
        pixel_flora_positions.append((px + pw, py))

    # MAIN FOREGROUND PLATFORM
    main_py = int(H * 0.62)
    main_ph = 55
    draw.rectangle([int(W * 0.18), main_py, int(W * 0.80), main_py + main_ph], fill=near_color)
    draw.rectangle([int(W * 0.18), main_py + main_ph, int(W * 0.80), main_py + main_ph + 18],
                   fill=near_shadow)
    draw.line([(int(W * 0.18), main_py), (int(W * 0.80), main_py)], fill=(180, 255, 255), width=3)
    draw.text((int(W * 0.20), main_py + 14), "Main Platform — NEAR tier — #00F0FF full sat",
              fill=(0, 20, 30), font=font_xs)
    # Add main platform edges to flora positions
    pixel_flora_positions.append((int(W * 0.18), main_py))
    pixel_flora_positions.append((int(W * 0.80), main_py))

    # ── LOWER VOID — y-weighted trails (dense near top of void, sparse below) ───
    void_y = main_py + main_ph + 18
    void_h = H - void_y

    rng.seed(seed)  # ensure determinism
    for _ in range(50):
        tx = rng.randint(0, W)
        t_len = rng.randint(20, 140)
        t_color_choice = rng.choice([(0, 60, 80), (0, 40, 60), (30, 10, 60)])
        # y-weighted: concentrate trails near top of void using inverse square
        rel_y = rng.random() ** 2.5  # bias toward 0 (top of void)
        ty_start = void_y + int(rel_y * (void_h - t_len))
        for t_i in range(t_len):
            ty = ty_start + t_i
            # fade alpha as trail descends
            fade = int(100 * (1 - t_i / t_len))
            if ty < H and fade > 10:
                draw.rectangle([tx, ty, tx + 2, ty + 2], fill=t_color_choice)

    # Distant void platforms (barely visible, deep background)
    for _ in range(8):
        vx = rng.randint(50, W - 200)
        vy = rng.randint(void_y + 20, H - 30)
        vw = rng.randint(80, 250)
        draw.rectangle([vx, vy, vx + vw, vy + 8], fill=(0, 28, 38))
        draw.line([(vx, vy), (vx + vw, vy)], fill=(0, 48, 62), width=1)

    # ── PIXEL FLORA — anchored to platform edges (corners/undersides) ───────────
    def _draw_flora(draw, fx, fy, color=(255, 45, 107)):
        """Draw a pixel flora cluster anchored at (fx, fy)."""
        for di in range(-1, 2):
            for dj in range(0, 3):  # grow downward from edge
                if (di + dj) % 2 == 0:
                    draw.rectangle([fx + di * 10, fy + dj * 10,
                                    fx + di * 10 + 8, fy + dj * 10 + 8],
                                   fill=color)

    # Place flora at platform edges
    flora_colors = [(255, 45, 107), (200, 20, 80), (255, 100, 140)]
    for i, (fx, fy) in enumerate(pixel_flora_positions[:8]):
        _draw_flora(draw, fx - 5, fy, flora_colors[i % len(flora_colors)])

    # ── LEGEND ────────────────────────────────────────────────────────────────
    legend_y = int(H * 0.04)
    for label, color in [("NEAR — full #00F0FF", near_color),
                         ("MID — #007891 (~50% step)", mid_color),
                         ("FAR — #003748", far_color)]:
        draw.rectangle([20, legend_y, 40, legend_y + 14], fill=color)
        draw.text((48, legend_y), label, fill=(200, 200, 200), font=font_xs)
        legend_y += 20

    # ── TITLE BAR ─────────────────────────────────────────────────────────────
    _title_bar(draw, "The Glitch Layer — 50% NEAR/MID contrast + alien grid (Cycle 6 Rev2)", font_title)

    img.save(output_path)
    print(f"Saved: {output_path}")


# ── Millbrook Main Street ──────────────────────────────────────────────────────

def generate_millbrook_street(output_path):
    img = Image.new('RGB', (W, H), (10, 10, 20))
    draw = ImageDraw.Draw(img)
    font, font_title, font_sm, font_xs = _get_fonts()

    # ── SKY ────────────────────────────────────────────────────────────────────
    sky_bot = int(H * 0.42)
    for y in range(sky_bot):
        t = y / sky_bot
        r = int(184 + t * (172 - 184))
        g = int(200 + t * (196 - 200))
        b = int(212 + t * (208 - 212))
        draw.line([(0, y), (W, y)], fill=(r, g, b), width=1)

    # ── BUILDINGS LEFT — atmospheric perspective: far bg buildings desaturated ──
    # Building A (tallest, leftmost) — midground, slight desaturation
    bld_a_color = _atmos_desaturate((200, 104, 32), 0.15)
    draw.rectangle([0, int(H * 0.22), int(W * 0.14), int(H * 0.78)], fill=bld_a_color)
    # Building B
    bld_b_color = _atmos_desaturate((212, 146, 58), 0.12)
    draw.rectangle([int(W * 0.05), int(H * 0.30), int(W * 0.24), int(H * 0.78)], fill=bld_b_color)
    # Building C (cream/pale)
    draw.rectangle([int(W * 0.18), int(H * 0.38), int(W * 0.32), int(H * 0.78)], fill=(250, 240, 220))
    # Window details — left buildings
    for bx, by, rows, cols, ww, wh, wc in [
        (int(W*0.02), int(H*0.26), 4, 2, 28, 22, (255, 220, 100)),
        (int(W*0.08), int(H*0.33), 3, 3, 22, 18, (230, 190, 80)),
    ]:
        for r in range(rows):
            for c in range(cols):
                wx = bx + c * (ww + 10)
                wy = by + r * (wh + 12)
                draw.rectangle([wx, wy, wx + ww, wy + wh], fill=(20, 15, 10), outline=wc, width=1)

    # ── BUILDINGS RIGHT — varied rooflines ────────────────────────────────────
    # Building R1
    r1_color = _atmos_desaturate((200, 104, 32), 0.12)
    draw.rectangle([int(W * 0.68), int(H * 0.26), int(W * 0.82), int(H * 0.78)], fill=r1_color)
    # Building R1 parapet (roofline variation)
    draw.rectangle([int(W * 0.68), int(H * 0.23), int(W * 0.75), int(H * 0.26)], fill=r1_color)
    draw.rectangle([int(W * 0.77), int(H * 0.24), int(W * 0.82), int(H * 0.26)], fill=r1_color)

    # Building R2 (tallest right)
    r2_color = _atmos_desaturate((140, 58, 34), 0.10)
    draw.rectangle([int(W * 0.76), int(H * 0.20), int(W * 0.92), int(H * 0.78)], fill=r2_color)
    # Water tower suggestion on R2 rooftop
    draw.rectangle([int(W * 0.82), int(H * 0.14), int(W * 0.88), int(H * 0.20)], fill=r2_color)
    draw.ellipse([int(W * 0.81), int(H * 0.13), int(W * 0.89), int(H * 0.17)],
                 fill=_atmos_desaturate((120, 50, 28), 0.15))

    # Building R3 (pale, rightmost)
    draw.rectangle([int(W * 0.88), int(H * 0.28), W, int(H * 0.78)], fill=(250, 240, 220))
    # R3 rooftop fire escape markers
    draw.rectangle([int(W * 0.90), int(H * 0.27), int(W * 0.92), int(H * 0.28)],
                   fill=(180, 160, 130))
    draw.line([(int(W*0.90), int(H*0.35)), (int(W*0.90), int(H*0.50))],
              fill=(160, 140, 110), width=3)  # fire escape vertical

    # Window details — right buildings
    for bx, by, rows, cols, ww, wh, wc in [
        (int(W*0.70), int(H*0.30), 3, 2, 26, 20, (255, 220, 100)),
        (int(W*0.78), int(H*0.24), 4, 2, 24, 18, (230, 190, 80)),
    ]:
        for r in range(rows):
            for c in range(cols):
                wx = bx + c * (ww + 10)
                wy = by + r * (wh + 12)
                draw.rectangle([wx, wy, wx + ww, wy + wh], fill=(20, 15, 10), outline=wc, width=1)

    # ── GAP BUILDINGS — fill void-black flanks of clock tower ────────────────
    # Without these, the (10,10,20) background shows as two black monolith gaps
    # flanking the tower (x=0.32..0.44 left, x=0.56..0.68 right).
    # Left gap: brick building, medium brown, slightly taller than Building C
    gap_l_color = _atmos_desaturate((186, 114, 60), 0.18)
    draw.rectangle([int(W * 0.30), int(H * 0.28), int(W * 0.45), int(H * 0.78)],
                   fill=gap_l_color)
    # Gap-left parapet
    draw.rectangle([int(W * 0.31), int(H * 0.25), int(W * 0.38), int(H * 0.28)],
                   fill=gap_l_color)
    # Gap-left windows
    for ri in range(3):
        for ci in range(2):
            gwx = int(W * 0.32) + ci * 52
            gwy = int(H * 0.31) + ri * 50
            draw.rectangle([gwx, gwy, gwx + 32, gwy + 28],
                           fill=(20, 15, 10), outline=(220, 185, 80), width=1)
    # Right gap: slightly different warm tone
    gap_r_color = _atmos_desaturate((196, 130, 70), 0.16)
    draw.rectangle([int(W * 0.55), int(H * 0.26), int(W * 0.70), int(H * 0.78)],
                   fill=gap_r_color)
    # Gap-right parapet
    draw.rectangle([int(W * 0.58), int(H * 0.23), int(W * 0.65), int(H * 0.26)],
                   fill=gap_r_color)
    draw.rectangle([int(W * 0.66), int(H * 0.24), int(W * 0.70), int(H * 0.26)],
                   fill=gap_r_color)
    # Gap-right windows
    for ri in range(3):
        for ci in range(2):
            gwx = int(W * 0.57) + ci * 52
            gwy = int(H * 0.29) + ri * 50
            draw.rectangle([gwx, gwy, gwx + 30, gwy + 26],
                           fill=(20, 15, 10), outline=(220, 185, 80), width=1)

    # ── CLOCK TOWER (center background) ────────────────────────────────────────
    # Apply atmospheric perspective — background buildings slightly lighter/desaturated
    tower_color = _atmos_desaturate((140, 122, 104), 0.20)
    tower_x = int(W * 0.44)
    draw.rectangle([tower_x, int(H * 0.12), tower_x + int(W * 0.12), int(H * 0.78)],
                   fill=tower_color)
    # Clock face
    cx_t, cy_t = tower_x + int(W * 0.06), int(H * 0.22)
    draw.ellipse([cx_t - 40, cy_t - 40, cx_t + 40, cy_t + 40],
                 fill=(230, 222, 200), outline=(80, 68, 50), width=3)
    # Clock hands
    draw.line([(cx_t, cy_t), (cx_t + 22, cy_t - 18)], fill=(40, 30, 20), width=3)
    draw.line([(cx_t, cy_t), (cx_t - 12, cy_t - 28)], fill=(40, 30, 20), width=2)

    # ── STREET ─────────────────────────────────────────────────────────────────
    street_y = int(H * 0.70)
    draw.rectangle([0, street_y, W, H], fill=(140, 122, 104))
    # Sidewalk edge
    draw.line([(0, street_y), (W, street_y)], fill=(100, 85, 70), width=3)
    # Center line (dashed)
    for x in range(0, W, 80):
        draw.rectangle([x, street_y + int(H * 0.12), x + 50, street_y + int(H * 0.14)],
                       fill=(200, 185, 160))

    # ── AWNING — visible colored shape (not just its shadow) ───────────────────
    # Left storefront awning: visible striped trapezoid above storefront opening
    awning_pts = [
        (0,              int(H * 0.72)),   # bottom-left
        (int(W * 0.20),  int(H * 0.72)),   # bottom-right
        (int(W * 0.17),  int(H * 0.67)),   # top-right
        (0,              int(H * 0.67)),    # top-left
    ]
    draw.polygon(awning_pts, fill=(160, 40, 40))   # red awning
    # Awning stripes
    for stripe_i in range(4):
        sx = int(stripe_i * W * 0.05)
        draw.line([(sx, int(H * 0.67)), (sx, int(H * 0.72))],
                  fill=(200, 200, 200), width=6)
    # Awning shadow (below awning — lighter, not the dominant dark region)
    draw.polygon([
        (0,              int(H * 0.72)),
        (int(W * 0.16),  int(H * 0.72)),
        (int(W * 0.13),  int(H * 0.76)),
        (0,              int(H * 0.76)),
    ], fill=(118, 98, 78))
    draw.text((20, int(H * 0.68)), "Left awning — storefront + shadow", fill=(220, 180, 150), font=font_xs)

    # ── STREET FURNITURE — mailbox at human scale ──────────────────────────────
    mb_x = int(W * 0.58)
    mb_y = int(H * 0.73)
    # Mailbox post
    draw.rectangle([mb_x + 10, mb_y + 36, mb_x + 20, mb_y + 75], fill=(60, 50, 40))
    # Mailbox body
    draw.rectangle([mb_x, mb_y, mb_x + 40, mb_y + 36], fill=(30, 60, 120))
    draw.ellipse([mb_x, mb_y, mb_x + 40, mb_y + 16], fill=(36, 70, 140))  # rounded top
    draw.text((mb_x - 10, mb_y + 76), "Mailbox — street scale", fill=(180, 155, 120), font=font_xs)

    # ── GUTTER + PAVEMENT CRACK — visible depth anchor ─────────────────────────
    # Gutter line
    draw.line([(0, int(H * 0.78)), (W, int(H * 0.78))], fill=(90, 72, 56), width=3)
    # Pavement crack: HIGH contrast — lighter than the street surface to be readable.
    # Street surface is (140,122,104). Crack uses a light warm tone (195,178,155) —
    # clearly visible as a bright split in the asphalt. 4px wide.
    crack_x = int(W * 0.35)
    crack_pts = [
        (crack_x,      int(H * 0.80)),
        (crack_x + 28, int(H * 0.845)),
        (crack_x + 12, int(H * 0.875)),
        (crack_x + 40, int(H * 0.915)),
        (crack_x + 22, int(H * 0.945)),
    ]
    for i in range(len(crack_pts) - 1):
        draw.line([crack_pts[i], crack_pts[i+1]], fill=(195, 178, 155), width=4)
    draw.text((crack_x + 44, int(H * 0.83)), "Pavement crack — 4px, high-contrast (foreground depth anchor)",
              fill=(180, 155, 120), font=font_xs)

    # ── POWER LINES — thin, semi-transparent, suggestion only ──────────────────
    pole_positions = [int(W * 0.28), int(W * 0.38), int(W * 0.62), int(W * 0.72)]
    pole_top = int(H * 0.32)
    pole_bot = street_y + 8
    for px in pole_positions:
        draw.line([(px, pole_top), (px, pole_bot)], fill=(50, 42, 34), width=3)
        draw.line([(px - 22, pole_top + 8), (px + 22, pole_top + 8)], fill=(50, 42, 34), width=2)

    # Wires — THIN (1px), catenary sag
    wire_ys = [int(H * 0.33), int(H * 0.36), int(H * 0.38)]
    wire_colors = [(55, 46, 36), (48, 40, 30), (44, 36, 26)]
    for wy, wc in zip(wire_ys, wire_colors):
        pts = []
        for i, wx in enumerate(range(0, W + 1, W // 8)):
            sag = int(8 * math.sin(i * math.pi / 8))
            pts.append((wx, wy + sag))
        for i in range(len(pts) - 1):
            draw.line([pts[i], pts[i+1]], fill=wc, width=1)

    draw.text((int(W * 0.30), int(H * 0.34)), "Power lines — thin 1px, catenary sag",
              fill=(100, 88, 72), font=font_xs)

    # ── TITLE BAR ─────────────────────────────────────────────────────────────
    _title_bar(draw, "Millbrook Main Street — Exterior Layout v4 (Cycle 6 Rev2)", font_title)

    img.save(output_path)
    print(f"Saved: {output_path}")


if __name__ == '__main__':
    generate_lumas_house(
        "/home/wipkat/team/output/backgrounds/environments/layouts/lumas_house_layout.png")
    generate_glitch_layer(
        "/home/wipkat/team/output/backgrounds/environments/layouts/glitch_layer_layout.png")
    generate_millbrook_street(
        "/home/wipkat/team/output/backgrounds/environments/layouts/millbrook_main_street_layout.png")
