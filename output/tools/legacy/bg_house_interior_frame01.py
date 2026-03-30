#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
bg_house_interior_frame01.py — Luma's House Interior Background
"Luma & the Glitchkin" — Background & Environment Design
Artist: Jordan Reed | Cycle 8

Renders the full Luma's House interior at 1920x1080, NO characters.
Canonical layout per production_bible.md and lumas_house_interior.md.

Color authority: master_palette.md v2.0
- ELEC_CYAN  #00F0FF  — screen glow / light source (world's electric color)
- BYTE_TEAL  #00D4E8  — Byte's body only (NOT used here)
- Monitor screens emit ELEC_CYAN, not Byte Teal

Key design decisions:
- Warm amber walls (~60% left/center) vs cold monitor wall (~40% right)
- Monitor wall IS the light source: gradient spill onto floor AND ceiling planes
- Bookshelves on warm wall (left), desk below monitor wall (right)
- Window + warm curtains far left
- Individual cable strands across floor foreground
- Couch centered-left, angled to face monitor wall
- Atmospheric perspective: BG elements lighter/more desaturated

Save: /home/wipkat/team/output/backgrounds/environments/frame01_house_interior.png
"""

import math
import random
from PIL import Image, ImageDraw, ImageFont

# ── Canvas ──────────────────────────────────────────────────────────────────
W, H = 1920, 1080

# ── Palette (master_palette.md canonical) ───────────────────────────────────
# Real World warm
WARM_CREAM        = (250, 240, 220)   # RW-01  #FAF0DC
SOFT_GOLD         = (232, 201, 90)    # RW-02  #E8C95A
SUNLIT_AMBER      = (212, 146, 58)    # RW-03  #D4923A
TERRACOTTA        = (199, 91, 57)     # RW-04  #C75B39
RUST_SHADOW       = (140, 58, 34)     # RW-05  #8C3A22
SAGE_GREEN        = (122, 158, 126)   # RW-06  #7A9E7E
DEEP_SAGE         = (74, 107, 78)     # RW-07  #4A6B4E
DUSTY_LAV         = (168, 155, 191)   # RW-08  #A89BBF
SHADOW_PLUM       = (92, 74, 114)     # RW-09  #5C4A72
WARM_TAN          = (196, 168, 130)   # RW-10  #C4A882
DEEP_COCOA        = (59, 40, 32)      # RW-11  #3B2820
MUTED_TEAL        = (91, 140, 138)    # RW-12  #5B8C8A
OCHRE_BRICK       = (184, 148, 74)    # RW-13  #B8944A
# Environmental
ENV07_DARK_WOOD   = (90, 56, 32)      # ENV-07 #5A3820 — dark warm wood / floor
# Glitch
ELEC_CYAN         = (0, 240, 255)     # GL-01  #00F0FF — screen glow (world electric color)
DEEP_CYAN         = (0, 168, 180)     # GL-01a #00A8B4
VOID_BLACK        = (10, 10, 20)      # GL-05  #0A0A14

# Derived interior-specific
WALL_FAR          = (228, 194, 138)   # atmospheric back wall (lighter/desaturated)
WALL_MID          = (212, 163, 80)    # amber mid wall
WALL_NEAR         = (196, 140, 58)    # warmer foreground wainscot
CEILING_COLOR     = (200, 170, 110)   # slightly darker warm ceiling
MONITOR_WALL_BG   = (14, 10, 22)      # near-void behind monitors
FLOOR_BASE        = (90, 56, 32)      # ENV-07 dark warm wood floor
FLOOR_LIGHT       = (130, 88, 46)     # floor worn-path (lighter honey oak area)
FLOOR_GLOW_ZONE   = (14, 40, 56)      # floor under monitor glow (dark cyan wash)
COUCH_BODY        = (96, 122, 100)    # faded sage green couch #607A64 area
COUCH_SHAD        = (60, 80, 62)      # couch shadow side
COUCH_CUSHION_A   = (184, 80, 48)     # terracotta cushion
COUCH_CUSHION_B   = (212, 176, 64)    # soft gold cushion
COUCH_CUSHION_C   = (144, 128, 168)   # dusty lavender cushion
COFFEE_TABLE      = (74, 48, 32)      # deep cocoa table
SHELF_WOOD        = (130, 82, 32)     # honey oak shelf
SHELF_SHADOW      = (80, 48, 18)      # underside of shelves (deep warm)
CRT_CASING        = (216, 206, 180)   # yellowed CRT plastic
CRT_SCREEN_OFF    = (16, 32, 40)      # off monitor: dark teal
DESK_WOOD         = (122, 80, 32)     # roll-top desk medium oak
DESK_LAMP_SHADE   = (200, 112, 16)    # amber desk lamp
WINDOW_FRAME      = (232, 223, 204)   # soft white window frame
CURTAIN           = (250, 240, 220)   # WARM_CREAM sheer curtain
CURTAIN_SHADOW    = (220, 195, 150)   # curtain fold shadow
BOOK_COLORS = [
    (199, 91, 57),    # terracotta
    (232, 201, 90),   # soft gold
    (122, 158, 126),  # sage green
    (168, 155, 191),  # dusty lavender
    (212, 146, 58),   # sunlit amber
    (91, 140, 138),   # muted teal
    (184, 148, 74),   # ochre brick
    (140, 58, 34),    # rust shadow
]
CABLE_COLORS = [
    (0, 212, 232),      # near-cyan cable
    (255, 45, 107),     # hot magenta cable
    (180, 140, 80),     # tan/brown cable
    (0, 168, 255),      # data blue
    (255, 200, 0),      # yellow cable
    (200, 80, 200),     # purple cable
    (0, 240, 255),      # ELEC_CYAN cable
    (100, 180, 80),     # green cable
    (200, 104, 16),     # origin cable — Grandma's special orange braided
]


# ── Helpers ──────────────────────────────────────────────────────────────────

def _get_fonts():
    try:
        font   = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
        font_b = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
        font_s = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 15)
    except Exception:
        font = font_b = font_s = ImageFont.load_default()
    return font, font_b, font_s


def _lerp_color(ca, cb, t):
    """Linearly interpolate between two RGB tuples. t=0 → ca, t=1 → cb."""
    return tuple(int(ca[i] + (cb[i] - ca[i]) * t) for i in range(3))


def _draw_filled_glow(draw, cx, cy, rx, ry, glow_rgb, bg_rgb, steps=14):
    """Gradient-filled ellipse glow (concentric fills, outer → bg, inner → glow)."""
    for i in range(steps, 0, -1):
        t = i / steps  # 1 at outer edge, near-0 at center
        color = _lerp_color(glow_rgb, bg_rgb, t)  # outer steps → bg color
        er = max(1, int(rx * t))
        ery = max(1, int(ry * t))
        draw.ellipse([cx - er, cy - ery, cx + er, cy + ery], fill=color)


def _draw_gradient_rect_v(draw, x0, y0, x1, y1, color_top, color_bot):
    """Vertical gradient fill rectangle, scanline by scanline."""
    for y in range(y0, y1):
        t = (y - y0) / max(1, y1 - y0)
        draw.line([(x0, y), (x1, y)], fill=_lerp_color(color_top, color_bot, t))


def _draw_gradient_rect_h(draw, x0, y0, x1, y1, color_left, color_right):
    """Horizontal gradient fill rectangle."""
    for x in range(x0, x1):
        t = (x - x0) / max(1, x1 - x0)
        draw.line([(x, y0), (x, y1)], fill=_lerp_color(color_left, color_right, t))


def _cable_arc(draw, x0, x1, base_y, sag, color, width=2):
    """Draw a cable as a catenary-like parabolic arc."""
    steps = 60
    pts = []
    for s in range(steps + 1):
        t = s / steps
        px = int(x0 + (x1 - x0) * t)
        py = int(base_y + sag * 4 * t * (1 - t))  # parabolic sag down
        pts.append((px, py))
    for i in range(len(pts) - 1):
        draw.line([pts[i], pts[i + 1]], fill=color, width=width)


# ── Main render ──────────────────────────────────────────────────────────────

def render_house_interior(output_path):
    img  = Image.new('RGB', (W, H), VOID_BLACK)
    draw = ImageDraw.Draw(img)
    font, font_b, font_s = _get_fonts()
    rng  = random.Random(42)  # deterministic for reproducibility

    # ── Z-PLANE KEY ───────────────────────────────────────────────────────────
    # Ceiling top:   y=0 to y=ceil_y   (12% from top)
    # Wall:          y=ceil_y to y=wainscot_y  (~55% H)
    # Wainscot:      y=wainscot_y to y=floor_y (~75% H)
    # Floor:         y=floor_y to y=H
    # Monitor wall:  x=mw_x onwards (rightmost ~42% of frame)
    # Warm wall:     x=0 to mw_x      (left ~58% of frame)

    ceil_y      = int(H * 0.12)
    wainscot_y  = int(H * 0.56)
    floor_y     = int(H * 0.74)
    mw_x        = int(W * 0.58)   # monitor wall starts here (cold zone ~42%)

    # ════════════════════════════════════════════════════════════════════════
    # STEP 1 — BASE WARM WALL (left 58%)
    # Atmospheric perspective: far (top) is lighter/more desaturated
    # ════════════════════════════════════════════════════════════════════════
    for y in range(ceil_y, wainscot_y):
        t = (y - ceil_y) / max(1, wainscot_y - ceil_y)
        # Top of wall = farthest = lighter/desaturated; bottom = warmer/richer
        row_color = _lerp_color(WALL_FAR, WALL_MID, t)
        draw.line([(0, y), (mw_x, y)], fill=row_color)

    # Wainscot strip — slightly darker warm panel
    draw.rectangle([0, wainscot_y, mw_x, floor_y], fill=WALL_NEAR)
    # Wainscot top rail line
    draw.line([(0, wainscot_y), (mw_x, wainscot_y)], fill=RUST_SHADOW, width=3)

    # ════════════════════════════════════════════════════════════════════════
    # STEP 2 — CEILING PLANE
    # Warm ceiling with atmospheric desaturation toward back
    # Monitor glow spills UP onto ceiling — gradient from monitor wall left
    # ════════════════════════════════════════════════════════════════════════
    # Base ceiling fill — warm
    draw.rectangle([0, 0, W, ceil_y], fill=CEILING_COLOR)

    # Ceiling warm gradient (slightly darker near-center, lighter at back/top)
    _draw_gradient_rect_v(draw, 0, 0, W, ceil_y,
                          color_top=(215, 185, 125),   # slightly lighter at very top
                          color_bot=(190, 155, 90))    # deeper at join with wall

    # Monitor glow spill on ceiling — light source cast from right onto ceiling
    # The glow spreads left from the monitor wall across the ceiling plane
    for x in range(W, mw_x - 300, -1):
        t = (W - x) / max(1, W - (mw_x - 300))  # 0 at far right, 1 at spill edge
        t = max(0.0, min(1.0, t))
        glow_strength = (1.0 - t) ** 1.5  # bright near monitor wall, falls off
        if glow_strength < 0.01:
            continue
        # Blend ELEC_CYAN tint into ceiling color
        ceil_base = (215, 185, 125)
        cyan_tint = (0, 80, 100)
        blended = _lerp_color(ceil_base, cyan_tint, glow_strength * 0.55)
        draw.line([(x, 0), (x, ceil_y)], fill=blended)

    # Ceiling gradient: warm far-left is darkest/warmest, lightens toward monitor wall
    # (monitor cyan spill brightens ceiling as it approaches the right)
    # Inverted from Cycle 7: darkest at warm edge, lightest near monitor wall
    _draw_gradient_rect_h(draw, 0, 0, int(W * 0.58), ceil_y,
                          color_left=(170, 130, 72),    # darker/warmer at far warm edge
                          color_right=(210, 182, 122))  # lighter near monitor wall

    # ════════════════════════════════════════════════════════════════════════
    # STEP 3 — FLOOR PLANE
    # Warm dark wood with monitor glow spill on right, window light on left
    # ════════════════════════════════════════════════════════════════════════
    # Base floor
    draw.rectangle([0, floor_y, W, H], fill=FLOOR_BASE)
    # Subtle floor plank lines
    for px in range(0, W, 48):
        draw.line([(px, floor_y), (px, H)], fill=(70, 42, 22), width=1)

    # Window warm light spill on floor (far left)
    _draw_gradient_rect_h(draw, 0, floor_y, int(W * 0.22), H,
                          color_left=_lerp_color(FLOOR_BASE, SOFT_GOLD, 0.35),
                          color_right=FLOOR_BASE)

    # Monitor glow spill onto floor — LIGHT SOURCE, not just a tinted zone
    # Gradient from monitor wall leftward across floor
    for x in range(W, int(W * 0.25), -1):
        t = (W - x) / max(1, W - int(W * 0.25))
        t = max(0.0, min(1.0, t))
        glow_strength = (1.0 - t) ** 1.8
        if glow_strength < 0.01:
            continue
        floor_base_c = FLOOR_BASE
        if x > mw_x:
            # Right of divider: full cold glow zone
            floor_base_c = FLOOR_GLOW_ZONE
        cyan_floor = (0, 60, 88)
        blended = _lerp_color(floor_base_c, cyan_floor, glow_strength * 0.7)
        draw.line([(x, floor_y), (x, H)], fill=blended)

    # Worn path — gradual scanline lightening with soft horizontal taper, NOT a flat rectangle.
    # Technique: alpha-composite overlay strips per scanline — fast, no per-pixel getpixel.
    # The worn zone toward the monitor wall picks up a faint cyan tint from glow above.
    wp_x0 = int(W * 0.18)
    wp_x1 = int(W * 0.52)
    wp_y0 = floor_y
    wp_y1 = floor_y + int((H - floor_y) * 0.42)
    wp_cx = (wp_x0 + wp_x1) // 2
    wp_hw = (wp_x1 - wp_x0) // 2

    # Build worn-path overlay as RGBA layer
    path_overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    path_draw = ImageDraw.Draw(path_overlay)
    steps_h = 12   # horizontal segments for soft edge taper
    for wy in range(wp_y0, wp_y1):
        vy = (wy - wp_y0) / max(1, wp_y1 - wp_y0)
        v_strength = max(0.0, 1.0 - vy * 1.6)
        if v_strength < 0.02:
            continue
        # Draw column segments with decreasing alpha toward edges (bell curve approximation)
        for seg in range(steps_h):
            seg_t = seg / steps_h         # 0 = left edge, 1 = right edge
            seg_cx = (seg + 0.5) / steps_h
            # Distance from center (0..1)
            dist_from_center = abs(seg_cx - 0.5) * 2
            h_strength = max(0.0, 1.0 - dist_from_center ** 2)
            strength = v_strength * h_strength
            if strength < 0.04:
                continue
            seg_x0 = wp_x0 + int(seg * (wp_x1 - wp_x0) / steps_h)
            seg_x1 = wp_x0 + int((seg + 1) * (wp_x1 - wp_x0) / steps_h)
            alpha = int(strength * 0.82 * 255)
            # Cyan tint for right side of path (near monitor wall influence)
            right_bias = max(0.0, (seg_cx - 0.55) / 0.45)
            light_col = _lerp_color(FLOOR_LIGHT, (18, 55, 72), right_bias * 0.28)
            path_draw.line([(seg_x0, wy), (seg_x1, wy)],
                           fill=(*light_col, alpha))
    img = img.convert('RGBA')
    img = Image.alpha_composite(img, path_overlay)
    img = img.convert('RGB')
    draw = ImageDraw.Draw(img)

    # Scuff marks — short diagonal strokes along the worn path (texture change cue)
    scuff_rng = random.Random(77)
    for _ in range(28):
        sx = scuff_rng.randint(wp_x0 + 20, wp_x1 - 20)
        sy = scuff_rng.randint(wp_y0 + 4, wp_y0 + int((H - floor_y) * 0.22))
        length = scuff_rng.randint(8, 22)
        angle = scuff_rng.choice([-1, 1]) * scuff_rng.randint(10, 35)
        ex = sx + int(length * math.cos(math.radians(angle)))
        ey = sy + int(length * math.sin(math.radians(angle)))
        scuff_col = _lerp_color(FLOOR_BASE, FLOOR_LIGHT, 0.6)
        draw.line([(sx, sy), (ex, ey)], fill=scuff_col, width=1)

    # ════════════════════════════════════════════════════════════════════════
    # STEP 4 — MONITOR WALL (cold zone, right ~42%)
    # Near-void background, 6 screens in 3x2 grid, ELEC_CYAN glow
    # Glow spills: left onto warm wall, up onto ceiling, down onto floor
    # ════════════════════════════════════════════════════════════════════════
    # Monitor wall background
    draw.rectangle([mw_x, ceil_y, W, floor_y], fill=MONITOR_WALL_BG)
    # Slight wall panel frame
    draw.line([(mw_x, ceil_y), (mw_x, floor_y)], fill=(40, 32, 60), width=4)

    # 6 screens in 3 columns × 2 rows
    mon_cols  = 3
    mon_rows  = 2
    pad_h     = 32   # horizontal padding within monitor wall
    pad_v     = 28   # vertical padding within monitor wall
    gap_h     = 18   # gap between screens horizontally
    gap_v     = 22   # gap between screens vertically
    mw_zone_w = W - mw_x
    mw_zone_h = floor_y - ceil_y
    mon_w     = (mw_zone_w - 2 * pad_h - (mon_cols - 1) * gap_h) // mon_cols
    mon_h     = (mw_zone_h - 2 * pad_v - (mon_rows - 1) * gap_v) // mon_rows

    monitor_rects = []
    for row in range(mon_rows):
        for col in range(mon_cols):
            mx = mw_x + pad_h + col * (mon_w + gap_h)
            my = ceil_y + pad_v + row * (mon_h + gap_v)
            monitor_rects.append((mx, my, mon_w, mon_h))

    # --- Draw monitor glow FIRST (light source backdrop), then screens on top ---

    # Overall monitor wall ambient glow — spills left onto warm wall.
    # FIX (Cycle 8): glow is drawn as a cyan-tinted overlay using alpha-composite so
    # the Step 1 atmospheric gradient is redrawn on top afterwards (it must survive).
    # The glow pass here only draws the cyan modulation; Step 1 gradient is reapplied below.
    glow_reach = int(W * 0.38)   # how far the light spills left
    glow_overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_overlay)
    for x in range(mw_x, mw_x - glow_reach, -1):
        dist = mw_x - x
        t_dist = dist / glow_reach
        glow_str = (1.0 - t_dist) ** 1.4  # steeper falloff
        if glow_str < 0.005:
            continue
        alpha = int(glow_str * 0.42 * 255)
        glow_draw.line([(x, ceil_y), (x, floor_y)], fill=(0, 50, 75, alpha))
    img_rgba = img.convert('RGBA')
    img_rgba = Image.alpha_composite(img_rgba, glow_overlay)
    img = img_rgba.convert('RGB')
    draw = ImageDraw.Draw(img)  # refresh draw handle after alpha composite

    # Re-apply Step 1 atmospheric gradient AFTER the glow pass so it survives.
    # The gradient is drawn as a semi-transparent overlay so the cyan modulation
    # beneath remains visible — both effects coexist.
    atmos_repass = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    atmos_draw = ImageDraw.Draw(atmos_repass)
    for y in range(ceil_y, wainscot_y):
        t = (y - ceil_y) / max(1, wainscot_y - ceil_y)
        row_color = _lerp_color(WALL_FAR, WALL_MID, t)
        # Alpha 180 — strong enough to restore warm gradient, low enough for glow to show
        atmos_draw.line([(0, y), (mw_x, y)], fill=(*row_color, 180))
    img_rgba = img.convert('RGBA')
    img_rgba = Image.alpha_composite(img_rgba, atmos_repass)
    img = img_rgba.convert('RGB')
    draw = ImageDraw.Draw(img)  # refresh draw handle

    # Monitor glow on ceiling (already applied in step 2 above)
    # Monitor glow on floor (already applied in step 3 above)

    # Draw monitor casings and screens
    for mx, my, mw_s, mh_s in monitor_rects:
        # CRT casing (thicker frame on top/sides, stand at bottom)
        casing_pad = 8
        draw.rectangle([mx - casing_pad, my - casing_pad,
                        mx + mw_s + casing_pad, my + mh_s + casing_pad],
                       fill=(20, 16, 28), outline=(50, 40, 72), width=2)
        draw.rectangle([mx - casing_pad + 2, my - casing_pad + 2,
                        mx + mw_s + casing_pad - 2, my + mh_s + casing_pad - 2],
                       fill=CRT_CASING, outline=(170, 160, 140), width=1)
        # Screen glass recess
        draw.rectangle([mx, my, mx + mw_s, my + mh_s], fill=(12, 24, 32))

    # Per-screen glow fill (drawn under screens — so glow bleeds around bezels)
    for mx, my, mw_s, mh_s in monitor_rects:
        cx_m = mx + mw_s // 2
        cy_m = my + mh_s // 2
        _draw_filled_glow(draw, cx_m, cy_m,
                          rx=mw_s // 2 + 35, ry=mh_s // 2 + 28,
                          glow_rgb=_lerp_color(ELEC_CYAN, (0, 80, 120), 0.5),
                          bg_rgb=MONITOR_WALL_BG,
                          steps=10)

    # Draw screen content ON TOP (ELEC_CYAN)
    for mx, my, mw_s, mh_s in monitor_rects:
        # Screen fill — ELEC_CYAN gradient (brighter at center = hotspot)
        cx_m = mx + mw_s // 2
        cy_m = my + mh_s // 2
        # Scanline fill with center-brightest gradient
        for sy in range(my, my + mh_s):
            ty = abs(sy - cy_m) / (mh_s / 2)
            row_col = _lerp_color(ELEC_CYAN, (0, 120, 160), ty * 0.7)
            draw.line([(mx, sy), (mx + mw_s, sy)], fill=row_col)
        # Scanlines (subtle horizontal lines)
        for sl in range(my, my + mh_s, 4):
            draw.line([(mx, sl), (mx + mw_s, sl)], fill=(0, 180, 200), width=1)
        # Screen hotspot glow (center brightest)
        _draw_filled_glow(draw, cx_m, cy_m,
                          rx=mw_s // 3, ry=mh_s // 3,
                          glow_rgb=(200, 255, 255),
                          bg_rgb=ELEC_CYAN,
                          steps=8)
        # CRT bezel border (thin dark line around screen)
        draw.rectangle([mx, my, mx + mw_s, my + mh_s], outline=(8, 8, 16), width=2)

    # Monitor wall surface texture (subtle vertical lines suggesting panels)
    for px in range(mw_x + 10, W, 60):
        draw.line([(px, ceil_y), (px, floor_y)], fill=(20, 14, 32), width=1)

    # ════════════════════════════════════════════════════════════════════════
    # STEP 5 — WINDOW + CURTAINS (far left)
    # Bay window with warm afternoon light, sheer curtains
    # ════════════════════════════════════════════════════════════════════════
    win_x     = int(W * 0.03)
    win_top   = ceil_y + 20
    win_bot   = wainscot_y - 20
    win_w     = int(W * 0.13)
    win_right = win_x + win_w

    # Window reveal / alcove — slightly recessed lighter wall
    draw.rectangle([win_x - 8, win_top - 8, win_right + 8, win_bot + 8],
                   fill=(224, 196, 130))
    # Window glass — warm exterior light (overexposed impression)
    draw.rectangle([win_x, win_top, win_right, win_bot], fill=SOFT_GOLD)
    # Bright center — window light diffusion
    _draw_filled_glow(draw, win_x + win_w // 2, win_top + (win_bot - win_top) // 2,
                      rx=win_w // 2, ry=(win_bot - win_top) // 2,
                      glow_rgb=WARM_CREAM,
                      bg_rgb=SOFT_GOLD,
                      steps=8)
    # Mullion (cross divider)
    mid_x_win = win_x + win_w // 2
    mid_y_win = win_top + (win_bot - win_top) // 2
    draw.line([(mid_x_win, win_top), (mid_x_win, win_bot)], fill=WINDOW_FRAME, width=4)
    draw.line([(win_x, mid_y_win), (win_right, mid_y_win)],  fill=WINDOW_FRAME, width=4)
    # Window frame outer
    draw.rectangle([win_x, win_top, win_right, win_bot], outline=WINDOW_FRAME, width=5)

    # Curtains — left panel and right panel, gathered fabric
    curt_width = 22
    # Left curtain panel
    left_curt_pts = [
        (win_x - curt_width, win_top - 4),
        (win_x + 10,         win_top - 4),
        (win_x + 6,          mid_y_win),
        (win_x + 12,         win_bot + 4),
        (win_x - curt_width, win_bot + 4),
    ]
    draw.polygon(left_curt_pts, fill=CURTAIN)
    draw.polygon(left_curt_pts, outline=CURTAIN_SHADOW, width=1)
    # Curtain fold lines
    for fy in range(win_top, win_bot, 30):
        draw.line([(win_x - curt_width + 4, fy), (win_x + 4, fy + 14)],
                  fill=CURTAIN_SHADOW, width=1)
    # Right curtain panel
    right_curt_pts = [
        (win_right + curt_width, win_top - 4),
        (win_right - 10,         win_top - 4),
        (win_right - 6,          mid_y_win),
        (win_right - 12,         win_bot + 4),
        (win_right + curt_width, win_bot + 4),
    ]
    draw.polygon(right_curt_pts, fill=CURTAIN)
    draw.polygon(right_curt_pts, outline=CURTAIN_SHADOW, width=1)

    # Curtain rod
    rod_y = win_top - 10
    draw.line([(win_x - curt_width - 8, rod_y), (win_right + curt_width + 8, rod_y)],
              fill=OCHRE_BRICK, width=5)
    # Rod finials
    draw.ellipse([win_x - curt_width - 18, rod_y - 6,
                  win_x - curt_width,       rod_y + 6], fill=SOFT_GOLD)
    draw.ellipse([win_right + curt_width,       rod_y - 6,
                  win_right + curt_width + 18,  rod_y + 6], fill=SOFT_GOLD)

    # Window warm light spill pool on floor
    pool_pts = [
        (win_x - 10,       floor_y),
        (win_right + 10,   floor_y),
        (win_right + 80,   H),
        (win_x - 80,       H),
    ]
    draw.polygon(pool_pts, fill=_lerp_color(FLOOR_BASE, SOFT_GOLD, 0.4))

    # ════════════════════════════════════════════════════════════════════════
    # STEP 6 — BOOKSHELVES on warm wall (center-left, between window and monitor wall)
    # 3 shelves of books/manuals — atmospheric perspective applied
    # ════════════════════════════════════════════════════════════════════════
    shelf_x_start = int(W * 0.19)
    shelf_x_end   = int(W * 0.55)
    shelf_ys      = [ceil_y + 30, ceil_y + 155, ceil_y + 280]
    shelf_depth   = 38  # visible depth of shelf face

    for si, sy in enumerate(shelf_ys):
        atmos_factor = si * 0.06  # top shelves are slightly farther = slightly desaturated
        # Shelf bracket pair
        for bx in [shelf_x_start + 20, shelf_x_end - 40]:
            draw.rectangle([bx - 6, sy - 20, bx + 6, sy + shelf_depth + 8],
                           fill=_lerp_color(SHELF_WOOD, (200, 190, 180), atmos_factor))
        # Shelf board
        draw.rectangle([shelf_x_start, sy, shelf_x_end, sy + shelf_depth],
                       fill=_lerp_color(SHELF_WOOD, (200, 190, 180), atmos_factor))
        draw.rectangle([shelf_x_start, sy + shelf_depth, shelf_x_end, sy + shelf_depth + 4],
                       fill=_lerp_color(SHELF_SHADOW, (160, 150, 140), atmos_factor))

        # Books on this shelf
        bx = shelf_x_start + 8
        book_idx = (si * 7) % len(BOOK_COLORS)
        while bx < shelf_x_end - 20:
            book_width = rng.randint(12, 28)
            book_height = rng.randint(22, shelf_depth - 4)
            raw_col = BOOK_COLORS[book_idx % len(BOOK_COLORS)]
            book_col = _lerp_color(raw_col, (200, 190, 180), atmos_factor + 0.05)
            draw.rectangle([bx, sy - book_height, bx + book_width - 1, sy],
                           fill=book_col)
            # Book spine line
            draw.line([(bx, sy - book_height), (bx, sy)], fill=DEEP_COCOA, width=1)
            bx += book_width + rng.randint(1, 3)
            book_idx += 1

    # Wall clock above bookshelves (center-left wall)
    clock_cx = int(W * 0.37)
    clock_cy = int(H * 0.09)
    draw.ellipse([clock_cx - 28, clock_cy - 28, clock_cx + 28, clock_cy + 28],
                 fill=(215, 200, 175), outline=DEEP_COCOA, width=3)
    draw.line([(clock_cx, clock_cy), (clock_cx + 12, clock_cy - 8)],
              fill=DEEP_COCOA, width=2)   # hour hand
    draw.line([(clock_cx, clock_cy), (clock_cx - 4, clock_cy + 16)],
              fill=DEEP_COCOA, width=1)   # minute hand

    # ════════════════════════════════════════════════════════════════════════
    # STEP 7 — COUCH (center-left, faces monitor wall)
    # Worn sage-green couch, angled in forced perspective toward right
    # Back cushion is on LEFT side — character sitting here faces RIGHT → monitors
    # ════════════════════════════════════════════════════════════════════════
    # Couch shifted right: left edge ~18%, right edge ~52% (was 9%-43%)
    # A character on this couch faces the monitor wall (right side of frame) correctly.
    couch_seat_pts = [
        (int(W * 0.18), int(H * 0.69)),   # front-left (near camera)
        (int(W * 0.18), int(H * 0.59)),   # back-left
        (int(W * 0.52), int(H * 0.55)),   # back-right (farther)
        (int(W * 0.52), int(H * 0.65)),   # front-right
    ]
    draw.polygon(couch_seat_pts, fill=COUCH_BODY)
    draw.polygon(couch_seat_pts, outline=COUCH_SHAD, width=3)

    # Seat cushions (3 pads along the seat)
    cushion_colors = [COUCH_CUSHION_A, COUCH_CUSHION_B, COUCH_CUSHION_C]
    for ci in range(3):
        t0 = ci / 3
        t1 = (ci + 1) / 3
        # Interpolate along the front edge and back edge
        def lerp_pt(A, B, t):
            return (int(A[0] + (B[0] - A[0]) * t), int(A[1] + (B[1] - A[1]) * t))
        fl = lerp_pt(couch_seat_pts[0], couch_seat_pts[3], t0)
        fr = lerp_pt(couch_seat_pts[0], couch_seat_pts[3], t1)
        bl = lerp_pt(couch_seat_pts[1], couch_seat_pts[2], t0)
        br = lerp_pt(couch_seat_pts[1], couch_seat_pts[2], t1)
        # Inset slightly
        cushion_poly = [
            (fl[0] + 4, fl[1] - 4),
            (bl[0] + 4, bl[1] + 2),
            (br[0] - 4, br[1] + 2),
            (fr[0] - 4, fr[1] - 4),
        ]
        draw.polygon(cushion_poly, fill=cushion_colors[ci])
        draw.polygon(cushion_poly, outline=_lerp_color(cushion_colors[ci], DEEP_COCOA, 0.4), width=1)

    # Couch back — LEFT side (character faces RIGHT toward monitors)
    back_pts = [
        (int(W * 0.18),  int(H * 0.59)),
        (int(W * 0.18),  int(H * 0.50)),
        (int(W * 0.31),  int(H * 0.48)),
        (int(W * 0.31),  int(H * 0.57)),
    ]
    draw.polygon(back_pts, fill=_lerp_color(COUCH_BODY, (80, 100, 84), 0.25))
    draw.polygon(back_pts, outline=COUCH_SHAD, width=2)

    # Armrests — shifted right to match couch body
    arm_l_pts = [
        (int(W * 0.16), int(H * 0.68)),
        (int(W * 0.16), int(H * 0.56)),
        (int(W * 0.20), int(H * 0.54)),
        (int(W * 0.20), int(H * 0.66)),
    ]
    draw.polygon(arm_l_pts, fill=_lerp_color(COUCH_BODY, COUCH_SHAD, 0.3))
    draw.polygon(arm_l_pts, outline=COUCH_SHAD, width=2)

    # Crocheted throw blanket over right armrest (shifted right)
    throw_pts = [
        (int(W * 0.47), int(H * 0.54)),
        (int(W * 0.53), int(H * 0.52)),
        (int(W * 0.55), int(H * 0.62)),
        (int(W * 0.49), int(H * 0.64)),
    ]
    draw.polygon(throw_pts, fill=(210, 100, 60))  # terracotta throw
    # Simple crochet pattern suggestion
    for ty in range(int(H * 0.53), int(H * 0.64), 10):
        draw.line([(int(W * 0.48), ty), (int(W * 0.54), ty - 4)],
                  fill=(230, 200, 150), width=1)

    # Coffee table (low, in front of couch)
    # Coffee table shifted right to match couch repositioning
    ct_x = int(W * 0.23)
    ct_y = int(H * 0.71)
    ct_w = int(W * 0.22)
    ct_h = int(H * 0.04)
    draw.rectangle([ct_x, ct_y, ct_x + ct_w, ct_y + ct_h], fill=COFFEE_TABLE)
    # Table legs
    for lx in [ct_x + 8, ct_x + ct_w - 8]:
        draw.rectangle([lx - 4, ct_y + ct_h, lx + 4, ct_y + ct_h + 14],
                       fill=DEEP_COCOA)
    # Items on coffee table
    # Magazine stack
    draw.rectangle([ct_x + 20, ct_y - 10, ct_x + 80, ct_y],
                   fill=(212, 190, 140))
    draw.rectangle([ct_x + 22, ct_y - 8,  ct_x + 78, ct_y - 2],
                   fill=(184, 148, 74))
    # Mug
    draw.rectangle([ct_x + 100, ct_y - 16, ct_x + 122, ct_y],
                   fill=(230, 210, 165))
    draw.line([(ct_x + 122, ct_y - 12), (ct_x + 132, ct_y - 6)],
              fill=(200, 180, 130), width=3)  # mug handle

    # ════════════════════════════════════════════════════════════════════════
    # STEP 7b — STANDING FLOOR LAMP (warm zone counterbalance)
    # A tall floor lamp that explains the warm amber glow source in the room.
    # Placed near the right edge of the warm zone, between couch and monitor wall.
    # This counterbalances the 6 bright ELEC_CYAN monitor screens visually.
    # ════════════════════════════════════════════════════════════════════════
    lamp_stand_x = int(W * 0.535)
    lamp_stand_base_y = floor_y
    lamp_stand_top_y = ceil_y + int(H * 0.06)
    lamp_stand_w = 6

    # Lamp base plate (wide foot for stability)
    draw.rectangle([lamp_stand_x - 18, lamp_stand_base_y - 10,
                    lamp_stand_x + 18, lamp_stand_base_y],
                   fill=DEEP_COCOA)
    # Lamp pole — thin vertical stand
    draw.rectangle([lamp_stand_x - lamp_stand_w // 2, lamp_stand_top_y,
                    lamp_stand_x + lamp_stand_w // 2, lamp_stand_base_y - 10],
                   fill=DEEP_COCOA)
    # Curved arm / gooseneck at top
    arm_tip_x = lamp_stand_x - 28
    arm_tip_y = lamp_stand_top_y + 22
    draw.line([(lamp_stand_x, lamp_stand_top_y),
               (lamp_stand_x - 14, lamp_stand_top_y + 8),
               (arm_tip_x, arm_tip_y)],
              fill=DEEP_COCOA, width=5)
    # Lamp shade (truncated trapezoid, open bottom)
    shade_pts = [
        (arm_tip_x - 22, arm_tip_y),          # top-left
        (arm_tip_x + 22, arm_tip_y),          # top-right
        (arm_tip_x + 34, arm_tip_y + 44),     # bottom-right (wide open bottom)
        (arm_tip_x - 34, arm_tip_y + 44),     # bottom-left
    ]
    draw.polygon(shade_pts, fill=SUNLIT_AMBER, outline=_lerp_color(SUNLIT_AMBER, DEEP_COCOA, 0.5), width=2)
    # Shade interior (slightly brighter inner face)
    shade_inner = [
        (arm_tip_x - 18, arm_tip_y + 4),
        (arm_tip_x + 18, arm_tip_y + 4),
        (arm_tip_x + 29, arm_tip_y + 40),
        (arm_tip_x - 29, arm_tip_y + 40),
    ]
    draw.polygon(shade_inner, fill=_lerp_color(SUNLIT_AMBER, WARM_CREAM, 0.45))
    # Warm glow cast downward from lamp onto floor/wainscot zone
    _draw_filled_glow(draw, lamp_stand_x - 12, wainscot_y + 20,
                      rx=110, ry=55,
                      glow_rgb=(230, 155, 35),
                      bg_rgb=WALL_NEAR,
                      steps=12)
    # Warm upward spill onto ceiling from lamp
    _draw_filled_glow(draw, lamp_stand_x - 12, ceil_y + 10,
                      rx=80, ry=30,
                      glow_rgb=(200, 130, 20),
                      bg_rgb=CEILING_COLOR,
                      steps=8)

    # Small side table beside lamp (simple dark rectangle)
    side_t_x = lamp_stand_x - 60
    side_t_y = floor_y - 28
    side_t_w = 52
    side_t_h = 8
    draw.rectangle([side_t_x, side_t_y, side_t_x + side_t_w, side_t_y + side_t_h],
                   fill=COFFEE_TABLE)
    # Side table legs
    for stl_x in [side_t_x + 6, side_t_x + side_t_w - 6]:
        draw.rectangle([stl_x - 3, side_t_y + side_t_h, stl_x + 3, floor_y],
                       fill=DEEP_COCOA)
    # Mug on side table
    draw.rectangle([side_t_x + 8, side_t_y - 18, side_t_x + 26, side_t_y],
                   fill=(228, 208, 162))
    draw.line([(side_t_x + 26, side_t_y - 14), (side_t_x + 34, side_t_y - 8)],
              fill=(195, 174, 128), width=2)  # mug handle
    # Small book on side table (lying flat)
    draw.rectangle([side_t_x + 30, side_t_y - 6, side_t_x + 50, side_t_y],
                   fill=(122, 158, 126))  # sage green book cover

    # ════════════════════════════════════════════════════════════════════════
    # STEP 8 — DESK BELOW MONITOR WALL (right zone)
    # Roll-top desk at bottom of monitor wall, cable clutter
    # ════════════════════════════════════════════════════════════════════════
    desk_x   = mw_x + 18
    desk_y   = floor_y - int(H * 0.18)
    desk_w   = int(W * 0.32)
    desk_h   = int(H * 0.18)

    # Desk body
    draw.rectangle([desk_x, desk_y, desk_x + desk_w, floor_y], fill=DESK_WOOD)
    draw.rectangle([desk_x, desk_y, desk_x + desk_w, desk_y + 8],
                   fill=_lerp_color(DESK_WOOD, OCHRE_BRICK, 0.4))
    # Roll-top slats (horizontal lines)
    for sl_y in range(desk_y + 14, desk_y + int(desk_h * 0.55), 7):
        draw.line([(desk_x, sl_y), (desk_x + desk_w, sl_y)],
                  fill=_lerp_color(DESK_WOOD, DEEP_COCOA, 0.3), width=1)
    # Desk surface clutter
    # Component drawer / USB hub
    draw.rectangle([desk_x + 30, desk_y + 18, desk_x + 120, desk_y + 46],
                   fill=(160, 150, 130), outline=DEEP_COCOA, width=1)
    # Circuit board shape
    draw.rectangle([desk_x + 140, desk_y + 20, desk_x + 240, desk_y + 44],
                   fill=(60, 100, 60), outline=(40, 80, 40), width=1)
    # Desk lamp
    lamp_bx = desk_x + desk_w - 80
    lamp_by = desk_y - 80
    draw.line([(lamp_bx, desk_y + 10), (lamp_bx + 10, lamp_by + 50)],
              fill=DEEP_COCOA, width=4)   # lamp neck
    draw.line([(lamp_bx + 10, lamp_by + 50), (lamp_bx + 50, lamp_by)],
              fill=DEEP_COCOA, width=4)
    # Lamp shade
    draw.polygon([
        (lamp_bx + 30, lamp_by),
        (lamp_bx + 70, lamp_by),
        (lamp_bx + 65, lamp_by + 30),
        (lamp_bx + 35, lamp_by + 30),
    ], fill=DESK_LAMP_SHADE)
    # Desk lamp warm glow pool (small, downward cone on desk surface)
    _draw_filled_glow(draw, lamp_bx + 50, desk_y + 4,
                      rx=70, ry=18,
                      glow_rgb=(230, 160, 40),
                      bg_rgb=DESK_WOOD,
                      steps=8)

    # Keyboard on desk
    draw.rectangle([desk_x + 20, desk_y + 54, desk_x + 180, desk_y + 74],
                   fill=(195, 185, 162), outline=DEEP_COCOA, width=1)
    # Key nubs
    for kx in range(desk_x + 25, desk_x + 175, 12):
        draw.rectangle([kx, desk_y + 57, kx + 9, desk_y + 68],
                       fill=(175, 165, 142), outline=(150, 140, 118), width=1)

    # Cable drawer cabinet (right, next to desk)
    cab_x = desk_x + desk_w + 10
    if cab_x + 120 < W:
        draw.rectangle([cab_x, desk_y, cab_x + 110, floor_y],
                       fill=(208, 196, 160), outline=DEEP_COCOA, width=2)
        # Small drawers grid (4 cols × 5 rows)
        for dr in range(5):
            for dc in range(4):
                dw, dh = 22, 16
                dx_ = cab_x + 6 + dc * (dw + 4)
                dy_ = desk_y + 10 + dr * (dh + 4)
                draw.rectangle([dx_, dy_, dx_ + dw, dy_ + dh],
                               fill=(190, 178, 142), outline=(150, 140, 110), width=1)
                # Tiny drawer pull
                draw.ellipse([dx_ + dw // 2 - 2, dy_ + dh // 2 - 2,
                               dx_ + dw // 2 + 2, dy_ + dh // 2 + 2],
                              fill=OCHRE_BRICK)

    # ════════════════════════════════════════════════════════════════════════
    # STEP 9 — INDIVIDUAL CABLE STRANDS (foreground floor)
    # Distinct cables, varied colors, run from monitor wall toward viewer
    # ════════════════════════════════════════════════════════════════════════
    # Dark foreground strip base
    draw.rectangle([0, int(H * 0.90), W, H], fill=(42, 26, 16))

    cable_defs = [
        # (x0, x1, base_y, sag, color, width)
        (mw_x,       mw_x - 280, int(H * 0.916), 50,  ELEC_CYAN,         2),
        (mw_x + 80,  mw_x - 180, int(H * 0.932), 65,  (255, 45, 107),    2),   # magenta
        (mw_x + 180, mw_x - 80,  int(H * 0.910), 40,  (180, 140, 80),    2),   # tan
        (mw_x + 60,  int(W*0.1), int(H * 0.948), 80,  (0, 168, 255),     1),   # data blue
        (mw_x + 240, int(W*0.3), int(H * 0.922), 90,  (255, 200, 0),     2),   # yellow
        (mw_x + 120, int(W*0.4), int(H * 0.938), 55,  (200, 80, 200),    1),   # purple
        (mw_x + 300, int(W*0.6), int(H * 0.912), 70,  ELEC_CYAN,         2),   # second cyan
        (mw_x + 20,  int(W*0.7), int(H * 0.950), 35,  (200, 104, 16),    3),   # origin cable (thick orange-braided)
        (mw_x + 160, int(W*0.8), int(H * 0.958), 30,  (100, 100, 100),   1),   # grey shadow cable
    ]
    for x0, x1, base_y, sag, color, width in cable_defs:
        _cable_arc(draw, x0, x1, base_y, sag, color, width)

    # ════════════════════════════════════════════════════════════════════════
    # STEP 10 — FOREGROUND DEPTH ANCHORS
    # Couch back visible at bottom edge (viewer feels IN the scene)
    # ════════════════════════════════════════════════════════════════════════
    # Couch arm/back sliver at absolute bottom-left (pulling viewer in)
    draw.rectangle([0, H - 60, int(W * 0.12), H], fill=COUCH_SHAD)
    draw.rectangle([0, H - 58, int(W * 0.10), H], fill=COUCH_BODY)
    # Crocheted blanket hem at bottom-left edge
    draw.rectangle([int(W * 0.02), H - 55, int(W * 0.09), H - 40],
                   fill=(210, 100, 60))

    # ════════════════════════════════════════════════════════════════════════
    # STEP 11 — ATMOSPHERIC PERSPECTIVE PASS
    # Far background (top of warm wall) gets a faint warm haze overlay using
    # alpha compositing — avoids slow per-pixel getpixel/putpixel loops.
    # ════════════════════════════════════════════════════════════════════════
    haze_y_top  = ceil_y
    haze_y_bot  = ceil_y + int(H * 0.20)  # extended from 8% to 20% (Cycle 8 fix)
    haze_img    = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    haze_draw   = ImageDraw.Draw(haze_img)
    # Gradient haze: stronger at top (farthest), fades to zero at haze_y_bot
    steps = 16
    for s in range(steps):
        t = 1.0 - s / steps
        alpha = int(28 * t)
        strip_y = haze_y_top + int(s * (haze_y_bot - haze_y_top) / steps)
        strip_y2 = haze_y_top + int((s + 1) * (haze_y_bot - haze_y_top) / steps)
        haze_draw.rectangle([0, strip_y, mw_x, strip_y2], fill=(215, 200, 180, alpha))
    img = img.convert('RGBA')
    img = Image.alpha_composite(img, haze_img)
    img = img.convert('RGB')

    # ════════════════════════════════════════════════════════════════════════
    # FINAL — No title bar (this is a clean background export, not a layout card)
    # ════════════════════════════════════════════════════════════════════════
    img.save(output_path)
    print(f"Saved: {output_path}")


if __name__ == '__main__':
    import os
    out_dir = "/home/wipkat/team/output/backgrounds/environments"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "frame01_house_interior.png")
    render_house_interior(out_path)
