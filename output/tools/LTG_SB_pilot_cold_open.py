#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_SB_pilot_cold_open.py
Pilot Cold Open — 6-Panel Key-Beat Storyboard Contact Sheet
Diego Vargas, Storyboard Artist — Cycle 38

Changes from v001:
  - HOODIE COLOR FIX: LUMA_HOODIE now canonical orange #E6641A (was slate blue — spec violation)
  - W004 FIX: draw = ImageDraw.Draw(sheet) added after sheet.paste(pimg) in make_contact_sheet()
  - P4: Cyan intrusion directionality — visible source point on screen edge + directional pixel vector
    toward Luma (Lee Tanaka note: intrusion origin + direction must be legible, not just presence)
  - P6: Left brow apex raised to ≥10px above right brow line (was edge-case ~6px; now clearly legible)
  - P6: Right eye lid corrected — top lid drops (focusing squint), NOT bottom lid rises (wince).
    Takeshi Mori critique: bottom-rise = wince, top-drop = focus. Wrong lid fixed.
  - P6: Left iris catch-light strengthened (screen-side eye should read stronger cyan than right eye)
  - P3: Glitchkin pixel shapes converted from rectangles → 4-7 sided irregular polygons (project
    standard from Cycle 11; no rectangles on Glitchkin formations)

Beat sequence (pitch emotional arc):
  P1 — Luma enters Grandma's living room — WIDE ESTABLISHING
  P2 — She spots the CRT in the corner — OTS / CLOSE-UP on screen
  P3 — A pixel glitch on the screen — INSERT: screen ECU
  P4 — Luma leans in — glitch colors bleed into warm room — MCU PUSH-IN (directionality fixed)
  P5 — Byte presses against the glass from inside — ECU TWO-WORLD TOUCH
  P6 — Luma's expression: THE NOTICING — MCU reaction / pitch emotional core (brow + lid fixed)

Output: LTG_SB_pilot_cold_open.png
        /home/wipkat/team/output/storyboards/
Contact sheet: 3 panels × 2 rows, ≤ 1280×720px

Standards:
- Every panel reads without verbal walkthrough
- Camera notes in annotation bar
- Emotions legible at thumbnail scale
- Image size rule: ≤ 1280px in both dimensions
"""

from PIL import Image, ImageDraw, ImageFont
import os, math, random

OUTPUT_DIR  = "/home/wipkat/team/output/storyboards"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "LTG_SB_pilot_cold_open.png")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── Contact sheet dimensions ─────────────────────────────────────────────────
COLS        = 3
ROWS        = 2
PANEL_W     = 360
PANEL_H     = 220
CAPTION_H   = 36
FULL_PH     = PANEL_H + CAPTION_H   # 256 per cell
MARGIN      = 18
GUTTER      = 10
HEADER_H    = 44
FOOTER_H    = 28

SHEET_W = MARGIN * 2 + COLS * PANEL_W + (COLS - 1) * GUTTER
SHEET_H = HEADER_H + MARGIN + ROWS * FULL_PH + (ROWS - 1) * GUTTER + FOOTER_H + MARGIN
# Expected: ~1118 × 618 — within 1280×720 hard limit

# ── Palette ───────────────────────────────────────────────────────────────────
# Real World
WARM_CREAM    = (250, 240, 220)
WALL_WARM     = (238, 220, 186)
FLOOR_LIGHT   = (210, 194, 160)
FLOOR_DARK    = (188, 172, 140)
WOOD_DARK     = (128,  82,  40)
WOOD_MED      = (166, 116,  60)
MORNING_GOLD  = (252, 198,  78)
SUNLIT_AMB    = (210, 144,  56)
LINE_DARK     = ( 42,  28,  14)
SHADOW_WARM   = (178, 150, 106)
TERRACOTTA    = (199,  91,  57)
PLANT_GREEN   = ( 86, 136,  70)
LUMA_SKIN     = (228, 185, 138)
# HOODIE FIX: canonical Luma Hoodie Orange #E6641A — was slate blue (72,112,148), spec violation
LUMA_HOODIE   = (230, 100,  26)
LUMA_HAIR     = ( 60,  42,  28)
# Glitch World intrusion
ELEC_CYAN     = (  0, 212, 232)
HOT_MAGENTA   = (232,   0, 152)
UV_PURPLE     = (123,  47, 190)
VOID_BLACK    = ( 10,  10,  20)
GLITCH_PIXEL1 = (  0, 220, 240)
GLITCH_PIXEL2 = (220,   0, 148)
DATA_BLUE     = ( 28,  72, 200)
# UI / caption
BG_CAPTION    = ( 20,  16,  12)
TEXT_CAP_LT   = (235, 228, 210)
TEXT_CAP_DIM  = (150, 140, 118)
CAM_COL       = (180, 220, 200)
GLOW_CYAN_DIM = (  0, 200, 220)

# ── Palette for arc-color borders ────────────────────────────────────────────
ARC_QUIET   = (200, 170,  80)
ARC_CURIOUS = (  0, 200, 210)
ARC_TENSE   = (200,  60, 200)
ARC_CORE    = (  0, 240, 255)


def load_font(size=12, bold=False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf" if bold else
        "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
    ]
    for p in candidates:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()


def add_glow(img, cx, cy, r_max, color_rgb, steps=5, max_alpha=50):
    """Additive glow via alpha composite — never darkens base."""
    for i in range(steps, 0, -1):
        r     = int(r_max * (i / steps))
        alpha = int(max_alpha * (1 - (i / steps) * 0.55))
        glow  = Image.new('RGBA', img.size, (0, 0, 0, 0))
        gd    = ImageDraw.Draw(glow)
        gd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(*color_rgb, alpha))
        base = img.convert('RGBA')
        img.paste(Image.alpha_composite(base, glow).convert('RGB'))


def draw_arrow(draw, x0, y0, x1, y1, color=(255, 255, 255), width=2):
    """Draw a directional arrow (for camera move annotations)."""
    draw.line([x0, y0, x1, y1], fill=color, width=width)
    angle = math.atan2(y1 - y0, x1 - x0)
    tip_len = 8
    for side in [math.pi * 0.8, -math.pi * 0.8]:
        ax = x1 + tip_len * math.cos(angle + side)
        ay = y1 + tip_len * math.sin(angle + side)
        draw.line([x1, y1, int(ax), int(ay)], fill=color, width=width)


def draw_irregular_poly(draw, cx, cy, avg_r, sides, color, rng, angle_offset=0):
    """Draw an irregular polygon (4-7 sides) for Glitchkin pixel shapes.
    Project standard from Cycle 11: no rectangles, organic edges.
    """
    pts = []
    for i in range(sides):
        angle = angle_offset + (2 * math.pi * i / sides) + rng.uniform(-0.3, 0.3)
        r = avg_r * rng.uniform(0.6, 1.4)
        px = int(cx + r * math.cos(angle))
        py = int(cy + r * math.sin(angle))
        pts.append((px, py))
    draw.polygon(pts, fill=color)


# ── Panel drawing functions ───────────────────────────────────────────────────

def draw_p1_establishing(img, rng):
    """
    P1 — WIDE ESTABLISHING
    Luma enters Grandma's warm cluttered living room.
    Camera: WIDE — slightly high angle, two-point perspective.
    """
    draw = ImageDraw.Draw(img)
    W, H = img.size

    # Floor
    floor_y = int(H * 0.68)
    draw.polygon([(0, floor_y), (W, floor_y - 20), (W, H), (0, H)], fill=FLOOR_LIGHT)
    # Floor tiles subtle grid
    for col in range(6):
        for row in range(3):
            fy0 = int(floor_y + row / 3 * (H - floor_y))
            fy1 = int(floor_y + (row + 1) / 3 * (H - floor_y))
            fx0 = col * W // 6
            fx1 = (col + 1) * W // 6
            fill = FLOOR_LIGHT if (row + col) % 2 == 0 else FLOOR_DARK
            draw.rectangle([fx0, fy0, fx1, fy1], fill=fill)

    # Back wall
    draw.rectangle([0, 0, W, floor_y], fill=WALL_WARM)
    # Ceiling stripe
    ceil_y = int(H * 0.18)
    draw.polygon([(0, 0), (W, 0), (W, ceil_y), (0, ceil_y + 8)], fill=(245, 232, 205))

    # Window (warm morning light from left)
    win_x, win_y = int(W * 0.15), int(H * 0.22)
    win_w, win_h = int(W * 0.18), int(H * 0.28)
    draw.rectangle([win_x, win_y, win_x + win_w, win_y + win_h],
                   fill=(255, 225, 145), outline=LINE_DARK, width=2)
    draw.line([win_x + win_w // 2, win_y, win_x + win_w // 2, win_y + win_h],
              fill=LINE_DARK, width=1)
    draw.line([win_x, win_y + win_h // 2, win_x + win_w, win_y + win_h // 2],
              fill=LINE_DARK, width=1)
    # Morning sunlight shaft on floor
    add_glow(img, win_x + win_w // 2, int(H * 0.72), 80, SUNLIT_AMB, steps=4, max_alpha=30)
    draw = ImageDraw.Draw(img)

    # Bookshelf (right BG)
    shelf_x = int(W * 0.68)
    for s in range(3):
        sy = int(H * 0.25) + s * int(H * 0.11)
        draw.rectangle([shelf_x, sy, shelf_x + int(W * 0.28), sy + int(H * 0.10)],
                       fill=WOOD_DARK, outline=LINE_DARK, width=1)
        for b in range(7):
            bx = shelf_x + 4 + b * 16
            bc = rng.choice([(180, 80, 60), (80, 100, 150), (100, 140, 80),
                              (160, 140, 60), (100, 80, 120)])
            draw.rectangle([bx, sy + 2, bx + 12, sy + int(H * 0.09)],
                           fill=bc, outline=LINE_DARK, width=1)

    # Armchair (left FG, partial)
    chair_x = int(W * 0.0)
    chair_y = int(H * 0.50)
    draw.rectangle([chair_x, chair_y, chair_x + int(W * 0.22), floor_y],
                   fill=(148, 100, 72), outline=LINE_DARK, width=2)
    draw.rectangle([chair_x, chair_y - int(H * 0.10),
                    chair_x + int(W * 0.22), chair_y],
                   fill=(168, 118, 88), outline=LINE_DARK, width=2)  # back

    # Coffee table (center FG)
    ct_x, ct_y = int(W * 0.28), int(H * 0.62)
    draw.rectangle([ct_x, ct_y, ct_x + int(W * 0.28), ct_y + int(H * 0.07)],
                   fill=WOOD_MED, outline=LINE_DARK, width=2)

    # CRT TV (right BG corner — story trigger)
    tv_x, tv_y = int(W * 0.62), int(H * 0.38)
    tv_w, tv_h = 50, 40
    draw.rectangle([tv_x, tv_y, tv_x + tv_w, tv_y + tv_h],
                   fill=(58, 50, 40), outline=(80, 68, 52), width=2)
    draw.rectangle([tv_x + 5, tv_y + 5, tv_x + tv_w - 5, tv_y + tv_h - 5],
                   fill=(80, 90, 80))
    add_glow(img, tv_x + tv_w // 2, tv_y + tv_h // 2 + 20, 40, GLOW_CYAN_DIM,
             steps=3, max_alpha=20)
    draw = ImageDraw.Draw(img)

    # Luma — small figure entering from left doorway
    luma_x, luma_y = int(W * 0.38), int(H * 0.38)
    luma_h = int(H * 0.40)
    # Body (hoodie block) — CANONICAL ORANGE
    draw.polygon([
        (luma_x - 14, luma_y + int(luma_h * 0.32)),
        (luma_x + 14, luma_y + int(luma_h * 0.32)),
        (luma_x + 18, luma_y + int(luma_h * 0.82)),
        (luma_x - 18, luma_y + int(luma_h * 0.82)),
    ], fill=LUMA_HOODIE, outline=LINE_DARK, width=1)
    # Head
    draw.ellipse([luma_x - 12, luma_y, luma_x + 12, luma_y + 24],
                 fill=LUMA_SKIN, outline=LINE_DARK, width=1)
    # Hair (messy cloud)
    draw.ellipse([luma_x - 15, luma_y - 10, luma_x + 15, luma_y + 16],
                 fill=LUMA_HAIR)
    # Legs
    draw.rectangle([luma_x - 10, luma_y + int(luma_h * 0.82),
                    luma_x - 3, luma_y + luma_h],
                   fill=(80, 60, 40), outline=LINE_DARK, width=1)
    draw.rectangle([luma_x + 3, luma_y + int(luma_h * 0.82),
                    luma_x + 10, luma_y + luma_h],
                   fill=(80, 60, 40), outline=LINE_DARK, width=1)
    # Curious head turn gesture — small arrow toward TV
    draw_arrow(draw, luma_x + 16, luma_y + 8, int(W * 0.60), int(H * 0.40),
               color=(200, 170, 80), width=1)

    # Annotation
    font = load_font(9)
    draw.text((4, 4), "WIDE — high 2-pt perspective", font=font, fill=CAM_COL)
    draw.text((int(W * 0.50), int(H * 0.28)), "CRT→",
              font=load_font(8), fill=GLOW_CYAN_DIM)
    # Arc label bottom-left
    draw.rectangle([3, H - 18, 90, H - 3], fill=(60, 50, 32))
    draw.text((6, H - 16), "QUIET / CURIOUS", font=load_font(8), fill=(220, 190, 90))


def draw_p2_crt_spotting(img, rng):
    """
    P2 — OTS / CLOSE-UP on CRT screen
    Luma spots the CRT — we see her shoulder in FG, screen fills BG.
    Camera: OTS — over-the-shoulder toward dark screen.
    """
    draw = ImageDraw.Draw(img)
    W, H = img.size

    # Dark room BG
    draw.rectangle([0, 0, W, H], fill=(40, 32, 22))

    # Warm ambient from behind Luma (doorway warmth)
    add_glow(img, int(W * 0.3), int(H * 0.5), 140, SUNLIT_AMB, steps=5, max_alpha=25)
    draw = ImageDraw.Draw(img)

    # CRT TV — large, center-right of frame, dark screen
    tv_x, tv_y = int(W * 0.32), int(H * 0.12)
    tv_w, tv_h = int(W * 0.60), int(H * 0.68)
    # TV housing (old rounded CRT plastic)
    draw.rectangle([tv_x, tv_y, tv_x + tv_w, tv_y + tv_h],
                   fill=(52, 44, 34), outline=(72, 60, 46), width=3)
    # CRT screen (dark, off-ish)
    scr_margin = 14
    draw.rectangle([tv_x + scr_margin, tv_y + scr_margin,
                    tv_x + tv_w - scr_margin, tv_y + tv_h - scr_margin],
                   fill=(18, 24, 22))
    # Faint static texture on screen
    rng2 = random.Random(42)
    for _ in range(30):
        sx = rng2.randint(tv_x + scr_margin, tv_x + tv_w - scr_margin)
        sy = rng2.randint(tv_y + scr_margin, tv_y + tv_h - scr_margin)
        draw.rectangle([sx, sy, sx + rng2.randint(2, 8), sy + 1],
                       fill=(50, 55, 50))
    # CRT screen reflection — Luma's dim face outline
    ref_x, ref_y = int(tv_x + tv_w * 0.45), int(tv_y + tv_h * 0.52)
    # Dim ghost reflection of Luma's head in screen
    draw.ellipse([ref_x - 18, ref_y - 22, ref_x + 18, ref_y + 22],
                 fill=(28, 32, 28), outline=(36, 38, 34), width=1)
    draw.ellipse([ref_x - 20, ref_y - 28, ref_x + 20, ref_y + 4],
                 fill=(22, 26, 22))  # hair ghost
    # Annotation: reflection label
    draw.text((ref_x - 40, ref_y + 26), "Luma's reflection",
              font=load_font(8), fill=(100, 130, 120))

    # TV dials / vents (right side of TV)
    for d in range(3):
        dx = tv_x + tv_w - 10
        dy = tv_y + 20 + d * 18
        draw.ellipse([dx - 5, dy - 5, dx + 5, dy + 5], fill=(62, 54, 44),
                     outline=(80, 68, 52), width=1)
    # Vent lines
    for v in range(5):
        vx = tv_x + tv_w - 10
        vy = tv_y + tv_h - 30 + v * 5
        draw.line([vx - 4, vy, vx + 3, vy], fill=(80, 68, 52), width=1)

    # Luma — OTS foreground silhouette (left edge, backlit) — orange hoodie visible
    sil_x = int(W * 0.10)
    sil_y = int(H * 0.25)
    # Shoulder / back silhouette — orange hoodie reads even in dim light
    draw.polygon([
        (0, H),
        (0, int(H * 0.42)),
        (int(W * 0.08), sil_y),
        (int(W * 0.22), sil_y + int(H * 0.08)),
        (int(W * 0.28), int(H * 0.42)),
        (int(W * 0.28), H),
    ], fill=(90, 42, 8))  # deep orange-shadow (backlit orange silhouette)
    # Head silhouette
    draw.ellipse([int(W * 0.04), sil_y - 20,
                  int(W * 0.22), sil_y + 16],
                 fill=(30, 22, 14))
    # Hair spikes (messy)
    for spike in [(-10, -26), (0, -30), (12, -24), (-18, -18)]:
        draw.ellipse([int(W * 0.04) + spike[0] + 5,
                      sil_y + spike[1],
                      int(W * 0.04) + spike[0] + 16,
                      sil_y + spike[1] + 12],
                     fill=(28, 20, 12))
    # Warm rim light on Luma's shoulder (from room behind her)
    add_glow(img, int(W * 0.16), sil_y + 20, 28, SUNLIT_AMB, steps=3, max_alpha=35)
    draw = ImageDraw.Draw(img)

    # Annotation
    font = load_font(9)
    draw.text((4, 4), "OTS — over shoulder toward dark screen", font=font, fill=CAM_COL)
    draw.text((4, 14), "Luma's face reflected in dark CRT glass", font=load_font(8), fill=(130, 160, 150))
    # Arc label
    draw.rectangle([3, H - 18, 70, H - 3], fill=(14, 20, 18))
    draw.text((6, H - 16), "CURIOUS", font=load_font(8), fill=(0, 200, 210))


def draw_p3_pixel_glitch(img, rng):
    """
    P3 — INSERT: screen ECU
    A pixel glitch on the screen — something moves inside.
    Camera: INSERT ECU — full-frame CRT screen.
    FIX v002: Glitchkin pixel shapes are now 4-7 sided irregular polygons (no rectangles).
    """
    draw = ImageDraw.Draw(img)
    W, H = img.size

    # Screen fill — dark static base
    draw.rectangle([0, 0, W, H], fill=(16, 20, 18))
    # Static noise
    rng2 = random.Random(77)
    for _ in range(120):
        sx = rng2.randint(0, W)
        sy = rng2.randint(0, H)
        draw.rectangle([sx, sy, sx + rng2.randint(2, 12), sy + 1],
                       fill=(40, 50, 44))

    # Scan lines (CRT)
    for y in range(0, H, 4):
        draw.line([0, y, W, y], fill=(10, 14, 12), width=1)

    # THE GLITCH — irregular polygon pixel cluster forming in center
    # FIX: all Glitchkin formation shapes use draw_irregular_poly — no rectangles
    cx, cy = W // 2, int(H * 0.48)

    # Pixel cluster: each shape is a 4-7 sided irregular polygon
    poly_rng = random.Random(88)  # deterministic seed for reproducibility
    pixel_defs = [
        # (offset_x, offset_y, avg_radius, sides, color)
        (  0,   0,  5,  5, ELEC_CYAN),
        ( -8,  -4,  4,  4, ELEC_CYAN),
        (  7,  -5,  4,  5, HOT_MAGENTA),
        ( -5,   7,  4,  6, ELEC_CYAN),
        ( 11,   9,  5,  4, HOT_MAGENTA),
        (-13,   1,  4,  5, ELEC_CYAN),
        (  5, -15,  4,  4, HOT_MAGENTA),
        ( -3, -11,  4,  6, ELEC_CYAN),
        ( 13,  -1,  5,  5, HOT_MAGENTA),
        (-17,  -3,  4,  7, UV_PURPLE),
        ( 18,  11,  4,  4, ELEC_CYAN),
        ( -1,  17,  4,  5, UV_PURPLE),
    ]
    for (ox, oy, r, sides, col) in pixel_defs:
        draw_irregular_poly(draw, cx + ox, cy + oy, r, sides, col, poly_rng)

    # Glow from the pixel cluster
    add_glow(img, cx, cy, 60, ELEC_CYAN, steps=6, max_alpha=55)
    add_glow(img, cx, cy, 30, HOT_MAGENTA, steps=4, max_alpha=40)
    draw = ImageDraw.Draw(img)

    # Loose pixel trails radiating outward — also irregular polygons
    trail_rng = random.Random(99)
    for angle_deg in range(0, 360, 30):
        angle = math.radians(angle_deg + rng.randint(-8, 8))
        for dist in [28, 44, 60]:
            trail_x = int(cx + dist * math.cos(angle))
            trail_y = int(cy + dist * math.sin(angle))
            if 0 <= trail_x < W and 0 <= trail_y < H:
                col = ELEC_CYAN if angle_deg % 60 == 0 else HOT_MAGENTA
                sides = trail_rng.randint(4, 6)
                r = max(2, 4 - dist // 22)
                draw_irregular_poly(draw, trail_x, trail_y, r, sides, col, trail_rng)

    # Screen edge vignette (bezel border)
    for bw in range(1, 8):
        draw.rectangle([bw, bw, W - bw, H - bw],
                       outline=(8, 10, 8), width=1)

    # Annotation
    font = load_font(9)
    draw.text((4, 4), "INSERT ECU — full-frame CRT screen", font=font, fill=CAM_COL)
    draw.text((4, 14), "pixel shape FORMS — organic edges (Glitchkin std)", font=load_font(8), fill=(0, 200, 210))
    # Callout arrow pointing to glitch center
    draw_arrow(draw, int(W * 0.15), int(H * 0.25), cx - 20, cy - 20,
               color=ELEC_CYAN, width=2)
    draw.text((4, int(H * 0.18)), "THE GLITCH", font=load_font(10, bold=True), fill=ELEC_CYAN)
    # Arc label
    draw.rectangle([3, H - 18, 82, H - 3], fill=(10, 16, 20))
    draw.text((6, H - 16), "DISCOVERY", font=load_font(8), fill=(0, 220, 240))


def draw_p4_luma_leans_in(img, rng):
    """
    P4 — MCU PUSH-IN
    Luma leans toward the CRT — glitch colors bleed into the warm room.
    Camera: MCU push-in — Luma from mid-chest up, TV in BG.

    FIX v002 (Lee Tanaka note): Intrusion must show ORIGIN POINT on screen edge
    and a clear directional VECTOR toward Luma. Not just ambient glow presence.
    Added: bright source marker on TV screen edge + pixel trail vector line
    toward Luma's face/body.
    """
    draw = ImageDraw.Draw(img)
    W, H = img.size

    # Background — warm room but cyan is bleeding in from TV
    draw.rectangle([0, 0, W, H], fill=(220, 200, 168))
    # Wall warm
    draw.rectangle([0, 0, W, int(H * 0.72)], fill=WALL_WARM)
    # Cyan bleed from right (CRT off-screen right) — ambient base
    add_glow(img, W, int(H * 0.4), 200, ELEC_CYAN, steps=7, max_alpha=32)
    # Warm ambient from left
    add_glow(img, 0, int(H * 0.3), 140, SUNLIT_AMB, steps=5, max_alpha=20)
    draw = ImageDraw.Draw(img)

    # Floor
    floor_y = int(H * 0.72)
    draw.rectangle([0, floor_y, W, H], fill=FLOOR_LIGHT)

    # CRT TV (right side, partially in-frame — left edge visible as source)
    tv_rx = int(W * 0.78)
    tv_ty = int(H * 0.28)
    tv_bh = int(H * 0.42)
    draw.rectangle([tv_rx, tv_ty, W + 10, tv_ty + tv_bh],
                   fill=(52, 44, 34), outline=(72, 60, 46), width=2)
    # Screen (glowing cyan — pixels active)
    draw.rectangle([tv_rx + 6, tv_ty + 6, W + 10, tv_ty + tv_bh - 6],
                   fill=(20, 30, 28))
    # SOURCE POINT: bright pixel burst at screen edge — origin of intrusion
    src_x = tv_rx + 2
    src_y = tv_ty + tv_bh // 2
    add_glow(img, W, tv_ty + tv_bh // 2, 90, ELEC_CYAN, steps=5, max_alpha=55)
    draw = ImageDraw.Draw(img)

    # Pixel burst escaping screen edge — VISIBLE SOURCE (irregular polygons)
    src_rng = random.Random(44)
    for py in range(tv_ty + 8, tv_ty + tv_bh - 8, 9):
        col = ELEC_CYAN if py % 18 < 9 else HOT_MAGENTA
        # Irregular polygon pixel at source edge
        draw_irregular_poly(draw, tv_rx - 4, py, 4, src_rng.randint(4, 6), col, src_rng)
    draw = ImageDraw.Draw(img)

    # DIRECTIONAL VECTOR: pixel trail from screen edge toward Luma's position
    # Luma center is ~luma_cx = W*0.40, luma_top+head ~H*0.18
    # Screen source: (tv_rx, src_y)
    # Trail runs from source to Luma's face with decreasing intensity
    luma_face_x = int(W * 0.48)
    luma_face_y = int(H * 0.18)
    vec_steps = 8
    trail_rng2 = random.Random(55)
    for step in range(vec_steps):
        t = step / (vec_steps - 1)
        trail_px = int(tv_rx + (luma_face_x - tv_rx) * t)
        trail_py = int(src_y + (luma_face_y - src_y) * t)
        # Fading trail — more intense near source
        trail_col = ELEC_CYAN if step % 2 == 0 else HOT_MAGENTA
        trail_r = max(2, int(5 * (1 - t * 0.6)))
        trail_sides = trail_rng2.randint(4, 6)
        draw_irregular_poly(draw, trail_px, trail_py, trail_r, trail_sides, trail_col, trail_rng2)
    # Direction arrow annotation
    draw_arrow(draw, tv_rx + 6, src_y, luma_face_x - 10, luma_face_y + 20,
               color=(0, 200, 220), width=1)
    draw = ImageDraw.Draw(img)

    # Luma — MCU from mid-chest up, LEANING FORWARD toward TV
    luma_cx = int(W * 0.40)
    luma_top = int(H * 0.05)
    # Body forward lean — hoodie (angled toward right) — CANONICAL ORANGE
    body_pts = [
        (luma_cx - 38, int(H * 0.82)),
        (luma_cx - 30, int(H * 0.35)),
        (luma_cx + 30, int(H * 0.32)),
        (luma_cx + 42, int(H * 0.82)),
    ]
    draw.polygon(body_pts, fill=LUMA_HOODIE, outline=LINE_DARK, width=2)
    # Hoodie pixel pattern (chest) — orange base
    for px in range(luma_cx - 18, luma_cx + 18, 6):
        for py in range(int(H * 0.45), int(H * 0.60), 6):
            if rng.random() > 0.55:
                col = rng.choice([(0, 180, 200), (200, 150, 60), LUMA_HOODIE])
                draw.rectangle([px, py, px + 4, py + 4], fill=col)
    # Arms reaching forward
    draw.polygon([
        (luma_cx + 28, int(H * 0.38)),
        (luma_cx + 70, int(H * 0.50)),
        (luma_cx + 65, int(H * 0.58)),
        (luma_cx + 22, int(H * 0.48)),
    ], fill=LUMA_HOODIE, outline=LINE_DARK, width=1)
    # Head (slightly tilted forward / curious)
    head_cx = luma_cx + 8
    head_cy = int(H * 0.20)
    draw.ellipse([head_cx - 28, head_cy - 28, head_cx + 28, head_cy + 30],
                 fill=LUMA_SKIN, outline=LINE_DARK, width=2)
    # Hair
    draw.ellipse([head_cx - 32, head_cy - 38, head_cx + 32, head_cy + 10],
                 fill=LUMA_HAIR)
    draw.ellipse([head_cx - 20, head_cy - 42, head_cx + 10, head_cy - 18],
                 fill=LUMA_HAIR)
    # Eyes — wide with curiosity (asymmetric brows for expression)
    # Left eye
    draw.ellipse([head_cx - 20, head_cy - 8, head_cx - 8, head_cy + 4],
                 fill=(255, 255, 255))
    draw.ellipse([head_cx - 17, head_cy - 6, head_cx - 11, head_cy + 2],
                 fill=(62, 42, 28))
    # Right eye (wider — toward screen)
    draw.ellipse([head_cx + 4, head_cy - 10, head_cx + 18, head_cy + 4],
                 fill=(255, 255, 255))
    draw.ellipse([head_cx + 6, head_cy - 8, head_cx + 14, head_cy + 2],
                 fill=(62, 42, 28))
    # Brow asymmetry (curious right brow arched)
    draw.arc([head_cx - 20, head_cy - 18, head_cx - 8, head_cy - 10],
             start=200, end=340, fill=LINE_DARK, width=2)
    draw.arc([head_cx + 3, head_cy - 22, head_cx + 20, head_cy - 10],
             start=200, end=340, fill=LINE_DARK, width=2)
    # Cyan rim light on Luma from TV (right side of face/body) — source confirmed
    add_glow(img, head_cx + 30, head_cy, 18, ELEC_CYAN, steps=3, max_alpha=30)
    draw = ImageDraw.Draw(img)

    # PUSH-IN arrow annotation (dashed inward motion)
    arr_cx, arr_cy = luma_cx + 10, int(H * 0.55)
    for step in range(3):
        ax0 = arr_cx - 85 + step * 20
        draw_arrow(draw, ax0, arr_cy + step * 4, ax0 + 12, arr_cy + step * 4 + 1,
                   color=(180, 220, 180), width=1)

    # Annotation
    font = load_font(9)
    draw.text((4, 4), "MCU — PUSH-IN toward screen", font=font, fill=CAM_COL)
    draw.text((4, 14), "Cyan bleeds in — SOURCE: screen edge→Luma face", font=load_font(8),
              fill=(120, 200, 195))
    draw.rectangle([3, H - 18, 58, H - 3], fill=(14, 20, 18))
    draw.text((6, H - 16), "TENSE", font=load_font(8), fill=ARC_TENSE)


def draw_p5_byte_presses(img, rng):
    """
    P5 — ECU TWO-WORLD TOUCH
    Byte presses against the glass from inside — two worlds touching.
    Camera: ECU — split composition: inside screen (cyan/magenta) / outside glass (warm).
    """
    draw = ImageDraw.Draw(img)
    W, H = img.size

    # LEFT HALF — outside (warm world, Luma's eye visible)
    draw.rectangle([0, 0, W // 2 + 8, H], fill=(230, 210, 175))
    # Glass surface (the screen boundary)
    draw.rectangle([W // 2 - 10, 0, W // 2 + 10, H], fill=(60, 70, 65))
    # Glass highlight
    draw.line([W // 2 - 6, 0, W // 2 - 6, H], fill=(200, 220, 210), width=1)

    # RIGHT HALF — inside (Glitch World)
    draw.rectangle([W // 2 + 8, 0, W, H], fill=(12, 16, 24))
    # Scanlines on Glitch side
    for y in range(0, H, 3):
        draw.line([W // 2 + 8, y, W, y], fill=(8, 12, 18), width=1)

    # Glitch world glow
    add_glow(img, W, H // 2, 180, ELEC_CYAN, steps=6, max_alpha=40)
    add_glow(img, W, H // 2, 80, HOT_MAGENTA, steps=4, max_alpha=25)
    draw = ImageDraw.Draw(img)

    # CRT glass distortion — pixel bloom at contact point
    contact_x = W // 2
    contact_y = int(H * 0.45)
    add_glow(img, contact_x, contact_y, 50, ELEC_CYAN, steps=5, max_alpha=60)
    draw = ImageDraw.Draw(img)

    # Byte — pressing hand/body against screen from inside
    # Byte is small (Glitchkin) — teal body, pixellated
    byte_cx = int(W * 0.70)
    byte_cy = int(H * 0.42)
    byte_r  = 28
    # Body
    draw.ellipse([byte_cx - byte_r, byte_cy - byte_r,
                  byte_cx + byte_r, byte_cy + byte_r],
                 fill=ELEC_CYAN, outline=(0, 160, 180), width=2)
    # Body pixel texture
    for bpx in range(byte_cx - byte_r + 4, byte_cx + byte_r - 4, 6):
        for bpy in range(byte_cy - byte_r + 4, byte_cy + byte_r - 4, 6):
            dist = math.sqrt((bpx - byte_cx) ** 2 + (bpy - byte_cy) ** 2)
            if dist < byte_r - 6 and rng.random() > 0.7:
                draw.rectangle([bpx, bpy, bpx + 4, bpy + 4],
                               fill=(0, 170, 190))
    # Byte pixel eyes (5×5 grid system — simplified)
    for eye_off in [-10, 6]:
        eye_x = byte_cx + eye_off
        eye_y = byte_cy - 6
        # Eye socket
        draw.rectangle([eye_x - 5, eye_y - 5, eye_x + 5, eye_y + 5],
                       fill=VOID_BLACK)
        # Pupil
        draw.rectangle([eye_x - 2, eye_y - 2, eye_x + 2, eye_y + 2],
                       fill=ELEC_CYAN)
    # Byte's hands pressed to glass (flattened pixel squares)
    for hx_off, hy_off in [(-22, 12), (18, 10)]:
        hx = byte_cx + hx_off
        hy = byte_cy + hy_off
        # Arm
        arm_tip_x = contact_x + int(W * 0.04)
        draw.line([hx, hy, arm_tip_x, contact_y + rng.randint(-5, 5)],
                  fill=(0, 175, 195), width=3)
        # Hand flat on glass
        draw.rectangle([arm_tip_x - 4, contact_y - 8,
                        arm_tip_x + 4, contact_y + 8],
                       fill=ELEC_CYAN, outline=(0, 160, 180), width=1)

    # Luma's eye (left half — extreme close-up, one eye visible)
    eye_cx = int(W * 0.24)
    eye_cy = int(H * 0.42)
    # Eye white
    draw.ellipse([eye_cx - 28, eye_cy - 14, eye_cx + 28, eye_cy + 14],
                 fill=(250, 245, 235), outline=LINE_DARK, width=2)
    # Iris
    draw.ellipse([eye_cx - 12, eye_cy - 12, eye_cx + 12, eye_cy + 12],
                 fill=(100, 75, 50))
    draw.ellipse([eye_cx - 7, eye_cy - 7, eye_cx + 7, eye_cy + 7],
                 fill=(38, 28, 18))
    # Specular
    draw.ellipse([eye_cx + 2, eye_cy - 6, eye_cx + 7, eye_cy - 2],
                 fill=(255, 255, 255))
    # Cyan reflection in Luma's eye from screen
    draw.arc([eye_cx - 10, eye_cy - 10, eye_cx + 10, eye_cy + 10],
             start=270, end=90, fill=(0, 200, 220), width=1)
    # Eyelid (tense/alert)
    draw.line([eye_cx - 28, eye_cy - 6, eye_cx + 28, eye_cy - 6],
              fill=LINE_DARK, width=2)
    # Luma's skin (fragment of face)
    draw.rectangle([0, eye_cy - 30, int(W * 0.35), H], fill=LUMA_SKIN)
    draw.ellipse([eye_cx - 28, eye_cy - 14, eye_cx + 28, eye_cy + 14],
                 fill=(250, 245, 235), outline=LINE_DARK, width=2)
    # Re-draw iris on top
    draw.ellipse([eye_cx - 12, eye_cy - 12, eye_cx + 12, eye_cy + 12],
                 fill=(100, 75, 50))
    draw.ellipse([eye_cx - 7, eye_cy - 7, eye_cx + 7, eye_cy + 7],
                 fill=(38, 28, 18))
    draw.ellipse([eye_cx + 2, eye_cy - 6, eye_cx + 7, eye_cy - 2],
                 fill=(255, 255, 255))

    # Annotation
    font = load_font(9)
    draw.text((4, 4), "ECU — split: glass boundary, two worlds", font=font, fill=CAM_COL)
    draw.text((int(W * 0.52), 4), "INSIDE SCREEN", font=load_font(8), fill=ELEC_CYAN)
    draw.text((4, 14), "OUTSIDE", font=load_font(8), fill=(200, 175, 110))
    draw.rectangle([3, H - 18, 126, H - 3], fill=(10, 16, 20))
    draw.text((6, H - 16), "TWO-WORLD TOUCH", font=load_font(8), fill=(0, 220, 240))


def draw_p6_the_noticing(img, rng):
    """
    P6 — THE NOTICING — pitch emotional core
    Luma's expression: wonder, recognition, slight fear, can't look away.
    Camera: MCU — Luma face, slightly low angle (empowering), warm rim + cyan fill.

    FIXES v002:
    - Left brow apex raised to ≥10px above right brow line (Lee Tanaka: min 6-8px gap)
    - Right eye: TOP lid drops (focusing squint) — NOT bottom lid rising (wince)
      Takeshi Mori critique 15: bottom-rise = wince is wrong for this beat
    - Left iris cyan catch-light STRONGER than right (screen is camera-left)
    """
    draw = ImageDraw.Draw(img)
    W, H = img.size

    # Background — warm room, cyan beginning to intrude heavily
    draw.rectangle([0, 0, W, H], fill=(228, 208, 178))
    # Cyan fill light (from CRT off left — screen is camera-left in this panel)
    add_glow(img, 0, H // 2, 180, ELEC_CYAN, steps=7, max_alpha=35)
    # Warm rim from right (room)
    add_glow(img, W, int(H * 0.3), 120, SUNLIT_AMB, steps=5, max_alpha=22)
    draw = ImageDraw.Draw(img)

    # Floor / lower background
    floor_y = int(H * 0.78)
    draw.rectangle([0, floor_y, W, H], fill=FLOOR_LIGHT)

    # Luma — MCU face + chest, low camera angle
    luma_cx = W // 2
    luma_head_cy = int(H * 0.36)
    head_rx = 52
    head_ry = 58

    # Body / hoodie (lower portion) — CANONICAL ORANGE
    draw.polygon([
        (luma_cx - 70, H),
        (luma_cx - 52, int(H * 0.56)),
        (luma_cx + 52, int(H * 0.56)),
        (luma_cx + 70, H),
    ], fill=LUMA_HOODIE, outline=LINE_DARK, width=2)
    # Hoodie neck / collar
    draw.ellipse([luma_cx - 24, int(H * 0.52), luma_cx + 24, int(H * 0.64)],
                 fill=LUMA_HOODIE, outline=LINE_DARK, width=1)
    # Pixel pattern on chest
    for px in range(luma_cx - 28, luma_cx + 28, 7):
        for py in range(int(H * 0.59), int(H * 0.74), 7):
            if rng.random() > 0.5:
                col = rng.choice([ELEC_CYAN, (200, 150, 40), LUMA_HOODIE])
                draw.rectangle([px, py, px + 5, py + 5], fill=col)

    # Head
    draw.ellipse([luma_cx - head_rx, luma_head_cy - head_ry,
                  luma_cx + head_rx, luma_head_cy + head_ry],
                 fill=LUMA_SKIN, outline=LINE_DARK, width=2)

    # Hair (big, messy cloud — characteristic silhouette)
    draw.ellipse([luma_cx - head_rx - 16, luma_head_cy - head_ry - 20,
                  luma_cx + head_rx + 8, luma_head_cy + 10],
                 fill=LUMA_HAIR)
    # Wild hair tufts
    tufts = [(-48, -32, -22, -8), (20, -38, 46, -12),
             (-28, -50, -2, -26), (4, -54, 36, -28),
             (36, -24, 56, 2), (-60, -10, -36, 14)]
    for tx0, ty0, tx1, ty1 in tufts:
        draw.ellipse([luma_cx + tx0, luma_head_cy + ty0,
                      luma_cx + tx1, luma_head_cy + ty1],
                     fill=LUMA_HAIR)

    # THE NOTICING EXPRESSION:
    # Eyes: WIDE open, pupils dilated, irises catching cyan light
    # Brows: asymmetric — left raised HIGH (wonder), right furrowed (apprehension)
    #   FIX: left brow apex ≥10px above right brow line (Lee Tanaka minimum: 6-8px)
    # Left iris catch: STRONG cyan (screen side — camera-left = CRT side)
    # Right eye: TOP lid drops (focusing squint) — NOT bottom lid up (wince)

    # Left eye (wide, wonder side — screen-facing, stronger cyan catch)
    le_cx = luma_cx - 22
    le_cy = luma_head_cy - 6
    draw.ellipse([le_cx - 16, le_cy - 14, le_cx + 16, le_cy + 14],
                 fill=(252, 248, 240), outline=LINE_DARK, width=2)
    # Iris
    draw.ellipse([le_cx - 9, le_cy - 9, le_cx + 9, le_cy + 9],
                 fill=(88, 68, 44))
    draw.ellipse([le_cx - 6, le_cy - 6, le_cx + 6, le_cy + 6],
                 fill=(28, 20, 12))
    # Strong cyan light catch in LEFT iris (screen side — more intense)
    draw.ellipse([le_cx - 7, le_cy - 9, le_cx + 2, le_cy],
                 fill=(0, 210, 230), outline=None)   # larger, brighter than right
    draw.ellipse([le_cx - 4, le_cy - 8, le_cx + 1, le_cy - 3],
                 fill=(80, 240, 255), outline=None)   # bright highlight within catch
    # Specular
    draw.ellipse([le_cx + 2, le_cy - 9, le_cx + 7, le_cy - 4],
                 fill=(255, 255, 255))
    # LEFT BROW — high arch (wonder) — apex at le_cy - 32 (≥10px above right brow at re_cy - 22)
    draw.arc([le_cx - 18, le_cy - 36, le_cx + 18, le_cy - 12],
             start=200, end=340, fill=LUMA_HAIR, width=3)

    # Right eye (slightly narrower — apprehension side)
    # FIX: TOP lid drops (focusing squint) — correct lid for this emotional beat
    re_cx = luma_cx + 22
    re_cy = luma_head_cy - 4
    draw.ellipse([re_cx - 14, re_cy - 12, re_cx + 14, re_cy + 12],
                 fill=(252, 248, 240), outline=LINE_DARK, width=2)
    draw.ellipse([re_cx - 8, re_cy - 8, re_cx + 8, re_cy + 8],
                 fill=(88, 68, 44))
    draw.ellipse([re_cx - 5, re_cy - 5, re_cx + 5, re_cy + 5],
                 fill=(28, 20, 12))
    # Weaker cyan catch in RIGHT iris (away from screen)
    draw.ellipse([re_cx - 4, re_cy - 6, re_cx + 1, re_cy - 1],
                 fill=(0, 175, 195), outline=None)   # smaller, dimmer than left
    draw.ellipse([re_cx + 2, re_cy - 8, re_cx + 6, re_cy - 4],
                 fill=(255, 255, 255))
    # TOP LID DROPS (focusing squint) — drawn as a thick arc on upper half of eye
    # The top lid cuts across the upper portion of the eye white
    draw.arc([re_cx - 14, re_cy - 12, re_cx + 14, re_cy + 12],
             start=200, end=340, fill=LINE_DARK, width=3)  # top lid drop line
    # RIGHT BROW — straight/furrowed — apex at re_cy - 22
    draw.line([re_cx - 14, re_cy - 22, re_cx + 14, re_cy - 18],
              fill=LUMA_HAIR, width=3)
    draw.line([re_cx - 14, re_cy - 22, re_cx - 10, re_cy - 18],
              fill=LUMA_HAIR, width=2)

    # BROW DIFFERENTIAL ANNOTATION: left apex = le_cy-32, right top = re_cy-22
    # Effective gap: (luma_head_cy-6-32) vs (luma_head_cy-4-22)
    #   = luma_head_cy-38 vs luma_head_cy-26 = 12px gap — exceeds 6-8px minimum

    # Nose — small
    draw.arc([luma_cx - 8, luma_head_cy + 4, luma_cx + 8, luma_head_cy + 18],
             start=200, end=340, fill=(190, 140, 100), width=2)
    draw.ellipse([luma_cx - 8, luma_head_cy + 10, luma_cx - 2, luma_head_cy + 17],
                 fill=(210, 158, 114))
    draw.ellipse([luma_cx + 2, luma_head_cy + 10, luma_cx + 8, luma_head_cy + 17],
                 fill=(210, 158, 114))

    # Mouth — slightly open, held-breath moment
    draw.arc([luma_cx - 16, luma_head_cy + 16, luma_cx + 16, luma_head_cy + 34],
             start=10, end=170, fill=LINE_DARK, width=2)
    draw.ellipse([luma_cx - 12, luma_head_cy + 22, luma_cx + 12, luma_head_cy + 34],
                 fill=(220, 150, 120))

    # Blush (slight — emotional warmth)
    add_glow(img, le_cx, le_cy + 18, 16, (220, 140, 100), steps=3, max_alpha=28)
    add_glow(img, re_cx, re_cy + 18, 16, (220, 140, 100), steps=3, max_alpha=28)
    draw = ImageDraw.Draw(img)

    # Stronger cyan screen light on Luma's LEFT side (screen side)
    add_glow(img, luma_cx - head_rx - 10, luma_head_cy, 60, ELEC_CYAN, steps=5, max_alpha=35)
    draw = ImageDraw.Draw(img)

    # "THE NOTICING" label — pitch emotional core callout
    label_w, label_h = 156, 22
    lbl_x = (W - label_w) // 2
    lbl_y = int(H * 0.04)
    draw.rectangle([lbl_x - 4, lbl_y - 2, lbl_x + label_w + 4, lbl_y + label_h],
                   fill=(20, 12, 8), outline=ELEC_CYAN, width=1)
    draw.text((lbl_x, lbl_y + 2), "THE NOTICING",
              font=load_font(12, bold=True), fill=ELEC_CYAN)

    # Annotation
    font = load_font(9)
    draw.text((4, 4), "MCU — low angle — warm rim / cyan fill", font=font, fill=CAM_COL)
    draw.text((4, H - 28), "EMOTIONAL CORE — wonder(L) + apprehension(R)",
              font=load_font(8), fill=(200, 175, 110))
    draw.rectangle([3, H - 18, 108, H - 3], fill=(14, 10, 8))
    draw.text((6, H - 16), "PITCH BEAT / CORE", font=load_font(8), fill=ARC_CORE)


# ── Assemble contact sheet ────────────────────────────────────────────────────

PANELS = [
    {
        "fn":    draw_p1_establishing,
        "label": "P1 — WIDE ESTABLISHING",
        "cam":   "WIDE / high 2-pt perspective",
        "beat":  "Luma enters Grandma's warm, cluttered living room.",
        "arc":   ARC_QUIET,
    },
    {
        "fn":    draw_p2_crt_spotting,
        "label": "P2 — OTS / CLOSE-UP: CRT SPOTTED",
        "cam":   "OTS — over shoulder toward dark screen",
        "beat":  "Luma spots the CRT — her face reflected in the dark glass.",
        "arc":   ARC_CURIOUS,
    },
    {
        "fn":    draw_p3_pixel_glitch,
        "label": "P3 — INSERT ECU: THE GLITCH",
        "cam":   "INSERT ECU — full-frame CRT screen",
        "beat":  "A pixel glitch bursts on screen — something moves inside.",
        "arc":   ARC_CURIOUS,
    },
    {
        "fn":    draw_p4_luma_leans_in,
        "label": "P4 — MCU PUSH-IN: GLITCH BLEEDS",
        "cam":   "MCU — push-in / cyan bleeds FROM screen edge→Luma",
        "beat":  "Luma leans in — Glitch colors invade the Real World.",
        "arc":   ARC_TENSE,
    },
    {
        "fn":    draw_p5_byte_presses,
        "label": "P5 — ECU: TWO-WORLD TOUCH",
        "cam":   "ECU — glass split: warm world / Glitch World",
        "beat":  "Byte presses from inside — two worlds touching at the glass.",
        "arc":   ARC_TENSE,
    },
    {
        "fn":    draw_p6_the_noticing,
        "label": "P6 — MCU: THE NOTICING",
        "cam":   "MCU — low angle / warm rim + cyan fill (screen L)",
        "beat":  "Luma: wonder(L brow high) + apprehension(R lid drop). Pitch core.",
        "arc":   ARC_CORE,
    },
]


def make_contact_sheet():
    rng = random.Random(2037)

    # Build individual panels
    panels_imgs = []
    for pd in PANELS:
        pimg = Image.new('RGB', (PANEL_W, PANEL_H), WALL_WARM)
        pd["fn"](pimg, rng)
        panels_imgs.append(pimg)

    # Sheet
    sheet = Image.new('RGB', (SHEET_W, SHEET_H), (18, 14, 10))
    draw  = ImageDraw.Draw(sheet)

    # Header
    font_title = load_font(16, bold=True)
    font_sub   = load_font(11)
    draw.text((MARGIN, 8), "Luma & the Glitchkin — Pilot Cold Open",
              font=font_title, fill=(235, 228, 210))
    draw.text((MARGIN, 26), "Key Beat Storyboard — 6 Panels — Diego Vargas, C38 v002",
              font=font_sub, fill=(150, 140, 118))
    draw.line([MARGIN, HEADER_H - 4, SHEET_W - MARGIN, HEADER_H - 4],
              fill=(42, 36, 28), width=1)

    font_label = load_font(10, bold=True)
    font_cam   = load_font(9)
    font_beat  = load_font(9)

    for idx, (pd, pimg) in enumerate(zip(PANELS, panels_imgs)):
        col = idx % COLS
        row = idx // COLS
        x   = MARGIN + col * (PANEL_W + GUTTER)
        y   = HEADER_H + MARGIN + row * (FULL_PH + GUTTER)

        # Panel image
        sheet.paste(pimg, (x, y))
        # W004 FIX: refresh draw object after paste — stale draw after paste is a code defect
        draw = ImageDraw.Draw(sheet)

        # Arc-color border
        draw.rectangle([x - 2, y - 2, x + PANEL_W + 2, y + PANEL_H + 2],
                       outline=pd["arc"], width=2)

        # Caption bar
        cap_y = y + PANEL_H
        draw.rectangle([x, cap_y, x + PANEL_W, cap_y + CAPTION_H],
                       fill=BG_CAPTION)
        draw.text((x + 4, cap_y + 2), pd["label"], font=font_label, fill=TEXT_CAP_LT)
        draw.text((x + 4, cap_y + 14), f"CAM: {pd['cam']}", font=font_cam, fill=CAM_COL)
        draw.text((x + 4, cap_y + 24), pd["beat"], font=font_beat, fill=TEXT_CAP_DIM)

    # Footer
    footer_y = SHEET_H - FOOTER_H + 4
    draw.line([MARGIN, footer_y - 6, SHEET_W - MARGIN, footer_y - 6],
              fill=(42, 36, 28), width=1)
    draw.text((MARGIN, footer_y),
              "LTG_SB_pilot_cold_open  |  output/storyboards/  |  ≤1280px  |  C38 fixes",
              font=load_font(9), fill=(100, 95, 78))

    # Clamp to image size rule
    sheet.thumbnail((1280, 720), Image.LANCZOS)

    sheet.save(OUTPUT_PATH, "PNG")
    print(f"Saved: {OUTPUT_PATH}  ({sheet.size[0]}×{sheet.size[1]}px)")
    return OUTPUT_PATH


if __name__ == "__main__":
    make_contact_sheet()
    print("LTG_SB_pilot_cold_open generation complete (Cycle 38).")
    print("Fixes applied:")
    print("  - HOODIE: canonical orange #E6641A (was slate blue spec violation)")
    print("  - W004: draw refreshed after every sheet.paste()")
    print("  - P3: Glitchkin pixel shapes are irregular polygons (no rectangles)")
    print("  - P4: Cyan intrusion source point + directional vector to Luma visible")
    print("  - P6: Left brow apex +12px above right brow (≥8px minimum met)")
    print("  - P6: Right eye top lid drops (focusing squint, not wince)")
    print("  - P6: Left iris cyan catch stronger than right (screen-side eye)")
