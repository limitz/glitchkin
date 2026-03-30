#!/usr/bin/env python3
"""
LTG_TOOL_sb_pilot_cold_open.py
Pilot Cold Open — 6-Panel Key-Beat Storyboard Contact Sheet
Diego Vargas, Storyboard Artist — Cycle 39

Changes from v002:
  - NEW P01: Exterior night shot — residential neighborhood, Luma's house with
    one upstairs light on. Grounds audience before we enter the house. Tight
    establish, not a full location shot. Added before old P1 (now P02).
  - P12 TWO-SHOT REFRAME: Center-weighted composition — both Luma (camera-left)
    and Byte (camera-right) have equal screen presence. Breathing negative space
    between them. Neither character cropped or edge-hugging.
  - P13 MIRROR COMPOSITION: Lee Tanaka brief — commitment beat. Byte camera-right
    (screen side), Luma camera-left. Both at eye-level. Mirror: Luma's open-left
    eye / Byte's organic-left eye face center. Byte: full-frontal, -3–4° forward
    lean, ELEC_CYAN glow directional toward Luma, quiet WARMTH arc mouth. This
    is the thematic fulcrum of the pitch — not UNGUARDED WARMTH (post-decision),
    but the THRESHOLD MOMENT still arriving.
  - OLD P6 "THE NOTICING" retired from contact sheet — superseded by P12/P13
    which carry forward the emotional beats in the correct staging.
  - Contact sheet updated to 6 panels (P01, P02, P04, P05, P12, P13) covering
    the full cold open arc from exterior night to commitment beat.

Panel naming in this contact sheet:
  P01 — EXTERIOR NIGHT: neighborhood, Luma's house
  P02 — WIDE ESTABLISHING: Luma enters Grandma's living room
  P04 — MCU PUSH-IN: glitch bleeds into warm room (from v002 P4)
  P05 — ECU TWO-WORLD TOUCH (from v002 P5)
  P12 — TWO-SHOT REFRAME: Luma and Byte, equal presence, breathing space
  P13 — MIRROR COMPOSITION: commitment beat / thematic fulcrum

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
# CANONICAL Luma Hoodie Orange #E6641A
LUMA_HOODIE   = (230, 100,  26)
LUMA_HAIR     = ( 60,  42,  28)
# Night sky palette
NIGHT_SKY     = ( 18,  20,  38)
NIGHT_DARK    = ( 22,  24,  42)
SIDEWALK_GREY = (148, 145, 138)
GRASS_NIGHT   = ( 42,  62,  36)
HOUSE_WALL    = (198, 185, 162)
ROOF_DARK     = ( 58,  48,  38)
WINDOW_WARM   = (252, 210, 100)    # lit upstairs window
WINDOW_DIM    = ( 58,  54,  46)    # dark windows
STREET_LAMP   = (242, 218, 130)
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
ARC_COMMIT  = ( 60, 200, 140)     # warm-cool blend — threshold / commitment


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

def draw_p01_exterior_night(img, rng):
    """
    P01 (NEW) — EXTERIOR NIGHT: Residential neighborhood
    A quiet residential street at night. Luma's house is visible — one
    upstairs window warm and lit. Grounds audience before we enter.
    Camera: WIDE EXTERIOR — slight low angle, 2-pt perspective.
    Tone: still, calm night — Real World warm vs cold night sky.
    """
    draw = ImageDraw.Draw(img)
    W, H = img.size

    # Night sky — deep dark blue-black
    draw.rectangle([0, 0, W, H], fill=NIGHT_SKY)

    # Stars — small dot scatter
    star_rng = random.Random(101)
    for _ in range(40):
        sx = star_rng.randint(0, W)
        sy = star_rng.randint(0, int(H * 0.45))
        sr = star_rng.choice([1, 1, 1, 2])
        brightness = star_rng.randint(170, 240)
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr],
                     fill=(brightness, brightness, brightness - 20))

    # Moon (upper right — soft disc)
    moon_x, moon_y = int(W * 0.82), int(H * 0.14)
    draw.ellipse([moon_x - 14, moon_y - 14, moon_x + 14, moon_y + 14],
                 fill=(240, 234, 210))
    add_glow(img, moon_x, moon_y, 28, (220, 214, 180), steps=3, max_alpha=20)
    draw = ImageDraw.Draw(img)

    # Horizon line / ground
    ground_y = int(H * 0.60)

    # BG NEIGHBORHOOD — dark silhouette houses (far, small)
    # Three background houses — dark silhouettes
    for hx, hw, hh_frac in [(int(W * 0.02), 60, 0.22),
                              (int(W * 0.18), 50, 0.20),
                              (int(W * 0.72), 68, 0.24),
                              (int(W * 0.84), 45, 0.18)]:
        hbase = ground_y
        htop  = int(hbase - H * hh_frac)
        # Main body
        draw.rectangle([hx, htop, hx + hw, hbase], fill=(38, 35, 50))
        # Gable roof
        roof_peak = (hx + hw // 2, htop - int(H * 0.06))
        draw.polygon([(hx - 2, htop), roof_peak, (hx + hw + 2, htop)],
                     fill=(30, 28, 42))
        # Dim windows
        for wx in range(hx + 8, hx + hw - 8, 14):
            for wy_off in [int(H * 0.06), int(H * 0.12)]:
                wy = htop + wy_off
                if wy < hbase - 4:
                    draw.rectangle([wx, wy, wx + 8, wy + 7],
                                   fill=WINDOW_DIM)

    # LUMA'S HOUSE — center-right, slightly larger, the hero building
    house_x   = int(W * 0.35)
    house_w   = 110
    house_base = ground_y + 4
    house_top  = int(house_base - H * 0.35)
    # Main facade
    draw.rectangle([house_x, house_top, house_x + house_w, house_base],
                   fill=HOUSE_WALL, outline=(170, 158, 138), width=1)
    # Gable roof
    roof_pk = (house_x + house_w // 2, house_top - int(H * 0.10))
    draw.polygon([(house_x - 4, house_top), roof_pk,
                  (house_x + house_w + 4, house_top)],
                 fill=ROOF_DARK, outline=(44, 38, 30), width=1)
    # Chimney
    chim_x = house_x + int(house_w * 0.62)
    draw.rectangle([chim_x, roof_pk[1] + 8, chim_x + 10,
                    house_top + 4], fill=(80, 68, 56))

    # Ground-floor windows (dark — everyone asleep)
    for wx in [house_x + 12, house_x + 42, house_x + 72]:
        draw.rectangle([wx, house_top + int(H * 0.12),
                        wx + 16, house_top + int(H * 0.20)],
                       fill=WINDOW_DIM, outline=(80, 72, 60), width=1)

    # UPSTAIRS WINDOW — THE LIT WINDOW (warm, story trigger)
    upwin_x = house_x + 52
    upwin_y = house_top + int(H * 0.04)
    upwin_w, upwin_h = 20, 16
    draw.rectangle([upwin_x, upwin_y, upwin_x + upwin_w, upwin_y + upwin_h],
                   fill=WINDOW_WARM, outline=(180, 140, 60), width=1)
    # Window pane divider
    draw.line([upwin_x + upwin_w // 2, upwin_y,
               upwin_x + upwin_w // 2, upwin_y + upwin_h],
              fill=(180, 140, 60), width=1)
    draw.line([upwin_x, upwin_y + upwin_h // 2,
               upwin_x + upwin_w, upwin_y + upwin_h // 2],
              fill=(180, 140, 60), width=1)
    # Warm window glow spill down facade
    add_glow(img, upwin_x + upwin_w // 2, upwin_y + upwin_h,
             36, WINDOW_WARM, steps=4, max_alpha=22)
    draw = ImageDraw.Draw(img)

    # Callout arrow to upstairs window
    draw_arrow(draw, int(W * 0.15), int(H * 0.18),
               upwin_x - 4, upwin_y + upwin_h // 2,
               color=(240, 210, 100), width=1)
    draw.text((4, int(H * 0.14)), "upstairs",
              font=load_font(8), fill=(230, 200, 80))
    draw.text((4, int(H * 0.21)), "still on",
              font=load_font(8), fill=(200, 175, 60))

    # Front porch / stoop
    porch_y = house_base - 8
    draw.rectangle([house_x + int(house_w * 0.38), porch_y,
                    house_x + int(house_w * 0.62), house_base],
                   fill=(168, 158, 140), outline=(140, 130, 116), width=1)

    # Front door (darker rectangle, center lower floor)
    door_x = house_x + int(house_w * 0.44)
    draw.rectangle([door_x, house_top + int(H * 0.21),
                    door_x + 14, house_base - 8],
                   fill=(78, 58, 38), outline=(55, 42, 28), width=1)

    # Ground / sidewalk / lawn
    # Grass
    draw.rectangle([0, ground_y, W, H], fill=GRASS_NIGHT)
    # Sidewalk strip
    walk_y = int(H * 0.70)
    draw.rectangle([0, walk_y, W, walk_y + int(H * 0.10)],
                   fill=SIDEWALK_GREY)
    # Sidewalk cracks (subtle)
    crack_rng = random.Random(55)
    for _ in range(6):
        cx0 = crack_rng.randint(10, W - 10)
        cy0 = walk_y + crack_rng.randint(3, int(H * 0.08))
        draw.line([cx0, cy0, cx0 + crack_rng.randint(-8, 8),
                   cy0 + crack_rng.randint(2, 6)],
                  fill=(130, 128, 122), width=1)

    # Street lamp (left of house) — orange sodium glow
    lamp_x = int(W * 0.26)
    lamp_base_y = walk_y + int(H * 0.06)
    draw.line([lamp_x, lamp_base_y, lamp_x, house_top - int(H * 0.02)],
              fill=(100, 95, 82), width=2)
    lamp_head_y = house_top - int(H * 0.06)
    draw.rectangle([lamp_x - 8, lamp_head_y - 4, lamp_x + 8, lamp_head_y + 4],
                   fill=(88, 82, 68))
    add_glow(img, lamp_x, lamp_head_y, 40, STREET_LAMP, steps=4, max_alpha=35)
    draw = ImageDraw.Draw(img)

    # Tree silhouette (left edge)
    tree_x = int(W * 0.06)
    tree_base_y = ground_y
    draw.line([tree_x, tree_base_y, tree_x, house_top + int(H * 0.08)],
              fill=(38, 30, 22), width=3)
    for br_y, br_r in [(house_top + int(H * 0.08), 22),
                        (house_top + int(H * 0.01), 18),
                        (house_top - int(H * 0.05), 14)]:
        draw.ellipse([tree_x - br_r, br_y - br_r, tree_x + br_r, br_y + br_r],
                     fill=(28, 40, 28))

    # Parked car silhouette (right BG)
    car_x = int(W * 0.74)
    car_y = walk_y - int(H * 0.08)
    draw.rounded_rectangle([car_x, car_y, car_x + 52, car_y + int(H * 0.10)],
                            radius=4, fill=(48, 44, 60))
    # Wheels
    for wx_off in [8, 38]:
        draw.ellipse([car_x + wx_off, car_y + int(H * 0.07),
                      car_x + wx_off + 10, car_y + int(H * 0.11)],
                     fill=(28, 26, 34))

    # Annotation
    font = load_font(9)
    draw.text((4, 4), "WIDE EXTERIOR — 2-pt perspective, night", font=font, fill=CAM_COL)
    draw.text((4, 14), "quiet street / one upstairs light still on", font=load_font(8),
              fill=(180, 175, 140))
    draw.rectangle([3, H - 18, 88, H - 3], fill=(14, 12, 22))
    draw.text((6, H - 16), "QUIET / STILL", font=load_font(8), fill=(200, 170, 80))


def draw_p02_establishing(img, rng):
    """
    P02 (was P1) — WIDE ESTABLISHING
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

    # Window (warm light from left)
    win_x, win_y = int(W * 0.15), int(H * 0.22)
    win_w, win_h = int(W * 0.18), int(H * 0.28)
    draw.rectangle([win_x, win_y, win_x + win_w, win_y + win_h],
                   fill=(255, 225, 145), outline=LINE_DARK, width=2)
    draw.line([win_x + win_w // 2, win_y, win_x + win_w // 2, win_y + win_h],
              fill=LINE_DARK, width=1)
    draw.line([win_x, win_y + win_h // 2, win_x + win_w, win_y + win_h // 2],
              fill=LINE_DARK, width=1)
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
                   fill=(168, 118, 88), outline=LINE_DARK, width=2)

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
    draw.polygon([
        (luma_x - 14, luma_y + int(luma_h * 0.32)),
        (luma_x + 14, luma_y + int(luma_h * 0.32)),
        (luma_x + 18, luma_y + int(luma_h * 0.82)),
        (luma_x - 18, luma_y + int(luma_h * 0.82)),
    ], fill=LUMA_HOODIE, outline=LINE_DARK, width=1)
    draw.ellipse([luma_x - 12, luma_y, luma_x + 12, luma_y + 24],
                 fill=LUMA_SKIN, outline=LINE_DARK, width=1)
    draw.ellipse([luma_x - 15, luma_y - 10, luma_x + 15, luma_y + 16],
                 fill=LUMA_HAIR)
    draw.rectangle([luma_x - 10, luma_y + int(luma_h * 0.82),
                    luma_x - 3, luma_y + luma_h],
                   fill=(80, 60, 40), outline=LINE_DARK, width=1)
    draw.rectangle([luma_x + 3, luma_y + int(luma_h * 0.82),
                    luma_x + 10, luma_y + luma_h],
                   fill=(80, 60, 40), outline=LINE_DARK, width=1)
    draw_arrow(draw, luma_x + 16, luma_y + 8, int(W * 0.60), int(H * 0.40),
               color=(200, 170, 80), width=1)

    # Annotation
    font = load_font(9)
    draw.text((4, 4), "WIDE — high 2-pt perspective", font=font, fill=CAM_COL)
    draw.text((int(W * 0.50), int(H * 0.28)), "CRT→",
              font=load_font(8), fill=GLOW_CYAN_DIM)
    draw.rectangle([3, H - 18, 90, H - 3], fill=(60, 50, 32))
    draw.text((6, H - 16), "QUIET / CURIOUS", font=load_font(8), fill=(220, 190, 90))


def draw_p04_luma_leans_in(img, rng):
    """
    P04 — MCU PUSH-IN
    Luma leans toward the CRT — glitch colors bleed into the warm room.
    Camera: MCU push-in — Luma from mid-chest up, TV in BG.
    Intrusion: visible SOURCE POINT on screen edge + directional vector toward Luma.
    """
    draw = ImageDraw.Draw(img)
    W, H = img.size

    draw.rectangle([0, 0, W, H], fill=(220, 200, 168))
    draw.rectangle([0, 0, W, int(H * 0.72)], fill=WALL_WARM)
    add_glow(img, W, int(H * 0.4), 200, ELEC_CYAN, steps=7, max_alpha=32)
    add_glow(img, 0, int(H * 0.3), 140, SUNLIT_AMB, steps=5, max_alpha=20)
    draw = ImageDraw.Draw(img)

    floor_y = int(H * 0.72)
    draw.rectangle([0, floor_y, W, H], fill=FLOOR_LIGHT)

    # CRT TV (right side, partially in-frame)
    tv_rx = int(W * 0.78)
    tv_ty = int(H * 0.28)
    tv_bh = int(H * 0.42)
    draw.rectangle([tv_rx, tv_ty, W + 10, tv_ty + tv_bh],
                   fill=(52, 44, 34), outline=(72, 60, 46), width=2)
    draw.rectangle([tv_rx + 6, tv_ty + 6, W + 10, tv_ty + tv_bh - 6],
                   fill=(20, 30, 28))
    add_glow(img, W, tv_ty + tv_bh // 2, 90, ELEC_CYAN, steps=5, max_alpha=55)
    draw = ImageDraw.Draw(img)

    # SOURCE PIXELS escaping screen edge (irregular polygons)
    src_rng = random.Random(44)
    for py in range(tv_ty + 8, tv_ty + tv_bh - 8, 9):
        col = ELEC_CYAN if py % 18 < 9 else HOT_MAGENTA
        draw_irregular_poly(draw, tv_rx - 4, py, 4, src_rng.randint(4, 6), col, src_rng)
    draw = ImageDraw.Draw(img)

    # DIRECTIONAL VECTOR: pixel trail from screen edge toward Luma's face
    luma_face_x = int(W * 0.48)
    luma_face_y = int(H * 0.18)
    src_y = tv_ty + tv_bh // 2
    vec_steps = 8
    trail_rng2 = random.Random(55)
    for step in range(vec_steps):
        t = step / (vec_steps - 1)
        trail_px = int(tv_rx + (luma_face_x - tv_rx) * t)
        trail_py = int(src_y + (luma_face_y - src_y) * t)
        trail_col = ELEC_CYAN if step % 2 == 0 else HOT_MAGENTA
        trail_r = max(2, int(5 * (1 - t * 0.6)))
        trail_sides = trail_rng2.randint(4, 6)
        draw_irregular_poly(draw, trail_px, trail_py, trail_r, trail_sides, trail_col, trail_rng2)
    draw_arrow(draw, tv_rx + 6, src_y, luma_face_x - 10, luma_face_y + 20,
               color=(0, 200, 220), width=1)
    draw = ImageDraw.Draw(img)

    # Luma — MCU from mid-chest up, LEANING FORWARD
    luma_cx = int(W * 0.40)
    body_pts = [
        (luma_cx - 38, int(H * 0.82)),
        (luma_cx - 30, int(H * 0.35)),
        (luma_cx + 30, int(H * 0.32)),
        (luma_cx + 42, int(H * 0.82)),
    ]
    draw.polygon(body_pts, fill=LUMA_HOODIE, outline=LINE_DARK, width=2)
    # Hoodie pixel pattern
    for px in range(luma_cx - 18, luma_cx + 18, 6):
        for py in range(int(H * 0.45), int(H * 0.60), 6):
            if rng.random() > 0.55:
                col = rng.choice([(0, 180, 200), (200, 150, 60), LUMA_HOODIE])
                draw.rectangle([px, py, px + 4, py + 4], fill=col)
    # Arms
    draw.polygon([
        (luma_cx + 28, int(H * 0.38)),
        (luma_cx + 70, int(H * 0.50)),
        (luma_cx + 65, int(H * 0.58)),
        (luma_cx + 22, int(H * 0.48)),
    ], fill=LUMA_HOODIE, outline=LINE_DARK, width=1)
    # Head
    head_cx = luma_cx + 8
    head_cy = int(H * 0.20)
    draw.ellipse([head_cx - 28, head_cy - 28, head_cx + 28, head_cy + 30],
                 fill=LUMA_SKIN, outline=LINE_DARK, width=2)
    draw.ellipse([head_cx - 32, head_cy - 38, head_cx + 32, head_cy + 10],
                 fill=LUMA_HAIR)
    draw.ellipse([head_cx - 20, head_cy - 42, head_cx + 10, head_cy - 18],
                 fill=LUMA_HAIR)
    # Eyes
    draw.ellipse([head_cx - 20, head_cy - 8, head_cx - 8, head_cy + 4],
                 fill=(255, 255, 255))
    draw.ellipse([head_cx - 17, head_cy - 6, head_cx - 11, head_cy + 2],
                 fill=(62, 42, 28))
    draw.ellipse([head_cx + 4, head_cy - 10, head_cx + 18, head_cy + 4],
                 fill=(255, 255, 255))
    draw.ellipse([head_cx + 6, head_cy - 8, head_cx + 14, head_cy + 2],
                 fill=(62, 42, 28))
    draw.arc([head_cx - 20, head_cy - 18, head_cx - 8, head_cy - 10],
             start=200, end=340, fill=LINE_DARK, width=2)
    draw.arc([head_cx + 3, head_cy - 22, head_cx + 20, head_cy - 10],
             start=200, end=340, fill=LINE_DARK, width=2)
    add_glow(img, head_cx + 30, head_cy, 18, ELEC_CYAN, steps=3, max_alpha=30)
    draw = ImageDraw.Draw(img)

    # PUSH-IN arrows
    arr_cx, arr_cy = luma_cx + 10, int(H * 0.55)
    for step in range(3):
        ax0 = arr_cx - 85 + step * 20
        draw_arrow(draw, ax0, arr_cy + step * 4, ax0 + 12, arr_cy + step * 4 + 1,
                   color=(180, 220, 180), width=1)

    font = load_font(9)
    draw.text((4, 4), "MCU — PUSH-IN toward screen", font=font, fill=CAM_COL)
    draw.text((4, 14), "Cyan bleeds in — SOURCE: screen edge→Luma", font=load_font(8),
              fill=(120, 200, 195))
    draw.rectangle([3, H - 18, 58, H - 3], fill=(14, 20, 18))
    draw.text((6, H - 16), "TENSE", font=load_font(8), fill=ARC_TENSE)


def draw_p05_two_world_touch(img, rng):
    """
    P05 — ECU TWO-WORLD TOUCH
    Byte presses against the glass from inside — two worlds touching.
    Camera: ECU — split composition: inside screen (cyan/magenta) / outside glass (warm).
    """
    draw = ImageDraw.Draw(img)
    W, H = img.size

    # LEFT HALF — outside (warm world, Luma's eye visible)
    draw.rectangle([0, 0, W // 2 + 8, H], fill=(230, 210, 175))
    # Glass surface (the screen boundary)
    draw.rectangle([W // 2 - 10, 0, W // 2 + 10, H], fill=(60, 70, 65))
    draw.line([W // 2 - 6, 0, W // 2 - 6, H], fill=(200, 220, 210), width=1)

    # RIGHT HALF — inside (Glitch World)
    draw.rectangle([W // 2 + 8, 0, W, H], fill=(12, 16, 24))
    for y in range(0, H, 3):
        draw.line([W // 2 + 8, y, W, y], fill=(8, 12, 18), width=1)

    add_glow(img, W, H // 2, 180, ELEC_CYAN, steps=6, max_alpha=40)
    add_glow(img, W, H // 2, 80, HOT_MAGENTA, steps=4, max_alpha=25)
    draw = ImageDraw.Draw(img)

    contact_x = W // 2
    contact_y = int(H * 0.45)
    add_glow(img, contact_x, contact_y, 50, ELEC_CYAN, steps=5, max_alpha=60)
    draw = ImageDraw.Draw(img)

    # Byte — pressing from inside
    byte_cx = int(W * 0.70)
    byte_cy = int(H * 0.42)
    byte_r  = 28
    draw.ellipse([byte_cx - byte_r, byte_cy - byte_r,
                  byte_cx + byte_r, byte_cy + byte_r],
                 fill=ELEC_CYAN, outline=(0, 160, 180), width=2)
    for bpx in range(byte_cx - byte_r + 4, byte_cx + byte_r - 4, 6):
        for bpy in range(byte_cy - byte_r + 4, byte_cy + byte_r - 4, 6):
            dist = math.sqrt((bpx - byte_cx) ** 2 + (bpy - byte_cy) ** 2)
            if dist < byte_r - 6 and rng.random() > 0.7:
                draw.rectangle([bpx, bpy, bpx + 4, bpy + 4],
                               fill=(0, 170, 190))
    for eye_off in [-10, 6]:
        eye_x = byte_cx + eye_off
        eye_y = byte_cy - 6
        draw.rectangle([eye_x - 5, eye_y - 5, eye_x + 5, eye_y + 5],
                       fill=VOID_BLACK)
        draw.rectangle([eye_x - 2, eye_y - 2, eye_x + 2, eye_y + 2],
                       fill=ELEC_CYAN)
    for hx_off, hy_off in [(-22, 12), (18, 10)]:
        hx = byte_cx + hx_off
        hy = byte_cy + hy_off
        arm_tip_x = contact_x + int(W * 0.04)
        draw.line([hx, hy, arm_tip_x, contact_y + rng.randint(-5, 5)],
                  fill=(0, 175, 195), width=3)
        draw.rectangle([arm_tip_x - 4, contact_y - 8,
                        arm_tip_x + 4, contact_y + 8],
                       fill=ELEC_CYAN, outline=(0, 160, 180), width=1)

    # Luma's eye (left half — extreme close-up)
    eye_cx = int(W * 0.24)
    eye_cy = int(H * 0.42)
    draw.ellipse([eye_cx - 28, eye_cy - 14, eye_cx + 28, eye_cy + 14],
                 fill=(250, 245, 235), outline=LINE_DARK, width=2)
    draw.ellipse([eye_cx - 12, eye_cy - 12, eye_cx + 12, eye_cy + 12],
                 fill=(100, 75, 50))
    draw.ellipse([eye_cx - 7, eye_cy - 7, eye_cx + 7, eye_cy + 7],
                 fill=(38, 28, 18))
    draw.ellipse([eye_cx + 2, eye_cy - 6, eye_cx + 7, eye_cy - 2],
                 fill=(255, 255, 255))
    draw.arc([eye_cx - 10, eye_cy - 10, eye_cx + 10, eye_cy + 10],
             start=270, end=90, fill=(0, 200, 220), width=1)
    draw.line([eye_cx - 28, eye_cy - 6, eye_cx + 28, eye_cy - 6],
              fill=LINE_DARK, width=2)
    draw.rectangle([0, eye_cy - 30, int(W * 0.35), H], fill=LUMA_SKIN)
    draw.ellipse([eye_cx - 28, eye_cy - 14, eye_cx + 28, eye_cy + 14],
                 fill=(250, 245, 235), outline=LINE_DARK, width=2)
    draw.ellipse([eye_cx - 12, eye_cy - 12, eye_cx + 12, eye_cy + 12],
                 fill=(100, 75, 50))
    draw.ellipse([eye_cx - 7, eye_cy - 7, eye_cx + 7, eye_cy + 7],
                 fill=(38, 28, 18))
    draw.ellipse([eye_cx + 2, eye_cy - 6, eye_cx + 7, eye_cy - 2],
                 fill=(255, 255, 255))

    font = load_font(9)
    draw.text((4, 4), "ECU — split: glass boundary, two worlds", font=font, fill=CAM_COL)
    draw.text((int(W * 0.52), 4), "INSIDE SCREEN", font=load_font(8), fill=ELEC_CYAN)
    draw.text((4, 14), "OUTSIDE", font=load_font(8), fill=(200, 175, 110))
    draw.rectangle([3, H - 18, 126, H - 3], fill=(10, 16, 20))
    draw.text((6, H - 16), "TWO-WORLD TOUCH", font=load_font(8), fill=(0, 220, 240))


def draw_p12_two_shot_reframe(img, rng):
    """
    P12 — TWO-SHOT REFRAME
    Luma (camera-left) and Byte (camera-right) — equal screen presence.
    Center-weighted composition. Breathing negative space between them.
    Neither character cropped or edge-hugging.
    Camera: MS TWO-SHOT — flat/even, warm room BG.
    """
    draw = ImageDraw.Draw(img)
    W, H = img.size

    # Background — warm room, CRT glow establishing both characters
    draw.rectangle([0, 0, W, H], fill=(225, 208, 178))
    draw.rectangle([0, 0, W, int(H * 0.68)], fill=WALL_WARM)
    # Warm ambient (room)
    add_glow(img, int(W * 0.25), int(H * 0.3), 140, SUNLIT_AMB, steps=5, max_alpha=18)
    # Cyan from CRT (camera-right BG)
    add_glow(img, int(W * 0.80), int(H * 0.35), 160, ELEC_CYAN, steps=6, max_alpha=28)
    draw = ImageDraw.Draw(img)

    floor_y = int(H * 0.68)
    draw.rectangle([0, floor_y, W, H], fill=FLOOR_LIGHT)

    # CRT (partially visible camera-right BG) — source of the situation
    tv_x = int(W * 0.72)
    tv_y = int(H * 0.30)
    draw.rectangle([tv_x, tv_y, tv_x + 52, tv_y + 40],
                   fill=(52, 44, 34), outline=(72, 60, 46), width=1)
    draw.rectangle([tv_x + 4, tv_y + 4, tv_x + 48, tv_y + 36],
                   fill=(20, 36, 34))
    add_glow(img, tv_x + 26, tv_y + 20, 30, ELEC_CYAN, steps=3, max_alpha=30)
    draw = ImageDraw.Draw(img)

    # ── LUMA — camera-left, ~30% of frame ──────────────────────────────────────
    luma_cx = int(W * 0.28)
    luma_top = int(H * 0.10)
    luma_body_bot = int(H * 0.90)
    luma_head_cy = int(H * 0.30)

    # Body
    draw.polygon([
        (luma_cx - 30, luma_body_bot),
        (luma_cx - 22, int(H * 0.50)),
        (luma_cx + 22, int(H * 0.50)),
        (luma_cx + 30, luma_body_bot),
    ], fill=LUMA_HOODIE, outline=LINE_DARK, width=2)
    # Hoodie pixel pattern (chest)
    for px in range(luma_cx - 14, luma_cx + 14, 6):
        for py in range(int(H * 0.55), int(H * 0.70), 6):
            if rng.random() > 0.5:
                draw.rectangle([px, py, px + 4, py + 4],
                               fill=rng.choice([(0, 180, 200), (200, 150, 60), LUMA_HOODIE]))
    # Arms — left arm relaxed at side, right arm slightly raised toward Byte
    # Left arm
    draw.polygon([
        (luma_cx - 22, int(H * 0.50)),
        (luma_cx - 36, int(H * 0.52)),
        (luma_cx - 32, int(H * 0.70)),
        (luma_cx - 18, int(H * 0.68)),
    ], fill=LUMA_HOODIE, outline=LINE_DARK, width=1)
    # Right arm — raised slightly, pointing/open toward Byte (center)
    draw.polygon([
        (luma_cx + 22, int(H * 0.50)),
        (luma_cx + 38, int(H * 0.48)),
        (luma_cx + 44, int(H * 0.60)),
        (luma_cx + 26, int(H * 0.62)),
    ], fill=LUMA_HOODIE, outline=LINE_DARK, width=1)

    # Head
    draw.ellipse([luma_cx - 26, luma_head_cy - 28,
                  luma_cx + 26, luma_head_cy + 28],
                 fill=LUMA_SKIN, outline=LINE_DARK, width=2)
    # Hair
    draw.ellipse([luma_cx - 30, luma_head_cy - 36,
                  luma_cx + 28, luma_head_cy + 8], fill=LUMA_HAIR)
    draw.ellipse([luma_cx - 16, luma_head_cy - 44,
                  luma_cx + 8, luma_head_cy - 20], fill=LUMA_HAIR)
    draw.ellipse([luma_cx + 12, luma_head_cy - 36,
                  luma_cx + 32, luma_head_cy - 16], fill=LUMA_HAIR)

    # Eyes — facing toward center-right (toward Byte)
    # Turned slightly — right eye (inner, facing Byte) more visible
    le_cx, le_cy = luma_cx - 10, luma_head_cy - 4
    re_cx, re_cy = luma_cx + 12, luma_head_cy - 4
    # Left eye (slightly smaller — turned away)
    draw.ellipse([le_cx - 10, le_cy - 9, le_cx + 10, le_cy + 9],
                 fill=(252, 248, 240), outline=LINE_DARK, width=1)
    draw.ellipse([le_cx - 5, le_cy - 5, le_cx + 5, le_cy + 5],
                 fill=(62, 42, 28))
    draw.ellipse([le_cx + 1, le_cy - 4, le_cx + 4, le_cy - 1],
                 fill=(255, 255, 255))
    # Right eye (larger — facing center)
    draw.ellipse([re_cx - 12, re_cy - 11, re_cx + 12, re_cy + 11],
                 fill=(252, 248, 240), outline=LINE_DARK, width=2)
    draw.ellipse([re_cx - 7, re_cy - 7, re_cx + 7, re_cy + 7],
                 fill=(62, 42, 28))
    draw.ellipse([re_cx - 4, re_cy - 4, re_cx + 4, re_cy + 4],
                 fill=(28, 20, 12))
    # Cyan catch in right eye — faces screen
    draw.ellipse([re_cx - 6, re_cy - 7, re_cx, re_cy - 1],
                 fill=(0, 200, 220))
    draw.ellipse([re_cx + 2, re_cy - 7, re_cx + 6, re_cy - 3],
                 fill=(255, 255, 255))
    # Brows — curious/hopeful
    draw.arc([le_cx - 12, le_cy - 20, le_cx + 12, le_cy - 8],
             start=200, end=340, fill=LUMA_HAIR, width=2)
    draw.arc([re_cx - 14, re_cy - 22, re_cx + 14, re_cy - 8],
             start=200, end=340, fill=LUMA_HAIR, width=3)
    # Nose + slight smile
    draw.arc([luma_cx - 6, luma_head_cy + 4, luma_cx + 6, luma_head_cy + 14],
             start=200, end=340, fill=(190, 140, 100), width=2)
    draw.arc([luma_cx - 12, luma_head_cy + 12, luma_cx + 12, luma_head_cy + 24],
             start=15, end=165, fill=LINE_DARK, width=2)

    # ── BYTE — camera-right, ~30% of frame, floating at Luma eye-level ──────────
    byte_cx = int(W * 0.72)
    byte_cy = luma_head_cy  # same height as Luma's eyes — eye-level float
    byte_r  = 22

    # Byte body — ELEC_CYAN
    draw.ellipse([byte_cx - byte_r, byte_cy - byte_r,
                  byte_cx + byte_r, byte_cy + byte_r],
                 fill=ELEC_CYAN, outline=(0, 160, 180), width=2)
    # Body pixel texture
    for bpx in range(byte_cx - byte_r + 3, byte_cx + byte_r - 3, 5):
        for bpy in range(byte_cy - byte_r + 3, byte_cy + byte_r - 3, 5):
            dist = math.sqrt((bpx - byte_cx) ** 2 + (bpy - byte_cy) ** 2)
            if dist < byte_r - 5 and rng.random() > 0.68:
                draw.rectangle([bpx, bpy, bpx + 3, bpy + 3],
                               fill=(0, 175, 195))

    # Byte eyes — 5×5 pixel grid system
    # Left eye (organic, faces center toward Luma)
    le_bx, le_by = byte_cx - 8, byte_cy - 5
    draw.rectangle([le_bx - 5, le_by - 5, le_bx + 5, le_by + 5],
                   fill=VOID_BLACK)
    draw.rectangle([le_bx - 2, le_by - 2, le_bx + 2, le_by + 2],
                   fill=ELEC_CYAN)
    # Right eye (cracked — faces outward)
    re_bx, re_by = byte_cx + 8, byte_cy - 5
    draw.rectangle([re_bx - 5, re_by - 5, re_bx + 5, re_by + 5],
                   fill=VOID_BLACK)
    # Cracked eye: alive zone lower-left (cyan), dead zone upper-right (void)
    draw.rectangle([re_bx - 3, re_by, re_bx + 2, re_by + 4],
                   fill=ELEC_CYAN)  # alive zone lower
    # Crack line — Hot Magenta diagonal
    draw.line([re_bx - 5, re_by - 5, re_bx + 5, re_by + 5],
              fill=HOT_MAGENTA, width=1)

    # Byte arms — slightly out from body (open, not reaching, not hiding)
    # Arms at ~30–40° out from center on each side
    for arm_side, arm_dir in [(-1, -1), (1, 1)]:
        arm_x0 = byte_cx + arm_side * (byte_r - 2)
        arm_y0 = byte_cy + 6
        arm_x1 = byte_cx + arm_side * (byte_r + 10)
        arm_y1 = byte_cy + 14
        draw.line([arm_x0, arm_y0, arm_x1, arm_y1],
                  fill=(0, 170, 190), width=3)
        # Small hand pixel
        draw.rectangle([arm_x1 - 3, arm_y1 - 3, arm_x1 + 3, arm_y1 + 3],
                       fill=ELEC_CYAN)

    # ELEC_CYAN directional glow toward Luma (left side of Byte brighter)
    add_glow(img, byte_cx - byte_r, byte_cy, 30, ELEC_CYAN, steps=4, max_alpha=60)
    add_glow(img, byte_cx, byte_cy, 20, ELEC_CYAN, steps=3, max_alpha=25)
    draw = ImageDraw.Draw(img)

    # Byte's glow spills onto negative space between characters
    add_glow(img, int(W * 0.50), byte_cy, 40, ELEC_CYAN, steps=3, max_alpha=12)
    draw = ImageDraw.Draw(img)

    # NEGATIVE SPACE — breathing gap annotated
    gap_x = int(W * 0.50)
    gap_y = int(H * 0.22)
    draw.text((gap_x - 18, gap_y), "·", font=load_font(9), fill=(120, 140, 160))
    draw.text((gap_x - 14, gap_y + 8), "space", font=load_font(7), fill=(100, 120, 140))

    # Annotation
    font = load_font(9)
    draw.text((4, 4), "MS TWO-SHOT — center-weighted, equal presence", font=font,
              fill=CAM_COL)
    draw.text((4, 14), "Breathing gap — neither character edge-hugging",
              font=load_font(8), fill=(160, 180, 170))
    draw.rectangle([3, H - 18, 100, H - 3], fill=(12, 18, 16))
    draw.text((6, H - 16), "TWO-SHOT / QUIET", font=load_font(8), fill=(180, 210, 190))


def draw_p13_mirror_commitment(img, rng):
    """
    P13 — MIRROR COMPOSITION: COMMITMENT BEAT
    Lee Tanaka brief: the thematic fulcrum — visual argument of the show in one frame.

    Byte: camera-right (screen side). Full-frontal toward Luma.
          Eye-level with her — descended from avoidance height.
          Arms slightly out — open, not reaching, not hiding.
          -3° to -4° forward lean.
          ELEC_CYAN glow directional — brighter facing Luma (left side).
          Cracked eye present but lid level — not droopy.
          Mouth: barely-there WARMTH arc, quiet not performed.

    Luma: camera-left. Facing center-right (toward Byte).
          Open-left eye faces center (toward Byte — first/unguarded eye).

    Mirror: Luma's open-left eye / Byte's organic-left eye BOTH FACE CENTER.
            Cracked eye and doubting eye both face outward.
            This is THRESHOLD, not UNGUARDED WARMTH (which is post-decision).

    Camera: MCU TWO-SHOT, CRT visible camera-right mid-ground.
            Warm rim (room) on Luma, cyan fill (screen) on Byte.
    """
    draw = ImageDraw.Draw(img)
    W, H = img.size

    # Background — dark warm room, CRT glow prominent from right
    draw.rectangle([0, 0, W, H], fill=(180, 162, 132))
    draw.rectangle([0, 0, W, int(H * 0.72)], fill=(200, 184, 152))

    # Warm ambient left (room lamp)
    add_glow(img, 0, int(H * 0.35), 120, SUNLIT_AMB, steps=5, max_alpha=20)
    # CRT cyan glow from right (screen behind Byte)
    add_glow(img, W, int(H * 0.4), 200, ELEC_CYAN, steps=7, max_alpha=40)
    draw = ImageDraw.Draw(img)

    floor_y = int(H * 0.72)
    draw.rectangle([0, floor_y, W, H], fill=FLOOR_DARK)

    # CRT (camera-right, mid-ground) — source and context
    tv_x = int(W * 0.78)
    tv_y = int(H * 0.28)
    draw.rectangle([tv_x, tv_y, tv_x + 50, tv_y + 40],
                   fill=(52, 44, 34), outline=(72, 60, 46), width=1)
    draw.rectangle([tv_x + 4, tv_y + 4, tv_x + 46, tv_y + 36],
                   fill=(14, 24, 24))
    add_glow(img, tv_x + 25, tv_y + 20, 35, ELEC_CYAN, steps=4, max_alpha=55)
    draw = ImageDraw.Draw(img)

    # ── LUMA — camera-left, MCU (head + chest) ───────────────────────────────
    luma_cx = int(W * 0.27)
    luma_head_cy = int(H * 0.35)
    head_rx, head_ry = 24, 26

    # Body / hoodie — slight 3/4 turn toward center-right
    draw.polygon([
        (luma_cx - 28, int(H * 0.92)),
        (luma_cx - 20, int(H * 0.56)),
        (luma_cx + 24, int(H * 0.54)),
        (luma_cx + 32, int(H * 0.92)),
    ], fill=LUMA_HOODIE, outline=LINE_DARK, width=2)
    # Hoodie collar
    draw.ellipse([luma_cx - 10, int(H * 0.52), luma_cx + 14, int(H * 0.62)],
                 fill=LUMA_HOODIE, outline=LINE_DARK, width=1)
    # Pixel pattern
    for px in range(luma_cx - 12, luma_cx + 16, 6):
        for py in range(int(H * 0.62), int(H * 0.76), 6):
            if rng.random() > 0.5:
                draw.rectangle([px, py, px + 4, py + 4],
                               fill=rng.choice([(0, 180, 200), (200, 150, 60), LUMA_HOODIE]))

    # Head
    draw.ellipse([luma_cx - head_rx, luma_head_cy - head_ry,
                  luma_cx + head_rx, luma_head_cy + head_ry],
                 fill=LUMA_SKIN, outline=LINE_DARK, width=2)
    # Hair
    draw.ellipse([luma_cx - head_rx - 10, luma_head_cy - head_ry - 12,
                  luma_cx + head_rx + 4, luma_head_cy + 4], fill=LUMA_HAIR)
    draw.ellipse([luma_cx - 10, luma_head_cy - head_ry - 18,
                  luma_cx + 12, luma_head_cy - head_ry - 2], fill=LUMA_HAIR)

    # Luma's eyes — 3/4 turned right (toward Byte and center)
    # Left eye (organic/open — faces center, the unguarded eye in the mirror)
    le_cx, le_cy = luma_cx + 2, luma_head_cy - 4
    draw.ellipse([le_cx - 12, le_cy - 10, le_cx + 12, le_cy + 10],
                 fill=(252, 248, 240), outline=LINE_DARK, width=2)
    draw.ellipse([le_cx - 6, le_cy - 6, le_cx + 6, le_cy + 6],
                 fill=(88, 68, 44))
    draw.ellipse([le_cx - 4, le_cy - 4, le_cx + 4, le_cy + 4],
                 fill=(28, 20, 12))
    # Cyan catch in left eye — this eye faces the screen
    draw.ellipse([le_cx - 5, le_cy - 6, le_cx + 1, le_cy - 1],
                 fill=(0, 210, 230))
    draw.ellipse([le_cx + 1, le_cy - 6, le_cx + 5, le_cy - 2],
                 fill=(255, 255, 255))
    # Left brow — slightly raised (open, wondering)
    draw.arc([le_cx - 14, le_cy - 20, le_cx + 14, le_cy - 8],
             start=200, end=340, fill=LUMA_HAIR, width=2)

    # Right eye (slightly less visible — turned away side, doubting/outward eye)
    re_cx, re_cy = luma_cx - 14, luma_head_cy - 4
    draw.ellipse([re_cx - 10, re_cy - 8, re_cx + 10, re_cy + 8],
                 fill=(252, 248, 240), outline=LINE_DARK, width=1)
    draw.ellipse([re_cx - 5, re_cy - 5, re_cx + 5, re_cy + 5],
                 fill=(78, 58, 38))
    draw.ellipse([re_cx - 3, re_cy - 3, re_cx + 3, re_cy + 3],
                 fill=(24, 18, 10))
    # Right brow — slightly furrowed (doubt faces outward)
    draw.line([re_cx - 12, re_cy - 18, re_cx + 10, re_cy - 14],
              fill=LUMA_HAIR, width=2)

    # Nose + quiet expression
    draw.arc([luma_cx - 4, luma_head_cy + 4, luma_cx + 8, luma_head_cy + 12],
             start=200, end=340, fill=(190, 140, 100), width=1)
    # Mouth — slight open uncertainty (not smiling yet, threshold moment)
    draw.arc([le_cx - 10, luma_head_cy + 10, le_cx + 10, luma_head_cy + 20],
             start=10, end=170, fill=LINE_DARK, width=2)

    # Warm rim on Luma's left side (room light)
    add_glow(img, luma_cx - head_rx - 8, luma_head_cy, 22,
             SUNLIT_AMB, steps=3, max_alpha=25)
    # Cyan fill light on Luma's right side (from screen)
    add_glow(img, luma_cx + head_rx + 4, luma_head_cy, 18,
             ELEC_CYAN, steps=3, max_alpha=22)
    draw = ImageDraw.Draw(img)

    # ── BYTE — camera-right, full-frontal, eye-level with Luma ────────────────
    byte_cx = int(W * 0.73)
    byte_cy = luma_head_cy   # eye-level: descended to her height — spec requirement
    byte_r  = 24

    # FORWARD LEAN: -3° to -4° — shift body center slightly left/down
    lean_offset_x = -2   # forward lean shifts toward Luma
    lean_offset_y = 2

    # Body — full-frontal (squared to Luma)
    draw.ellipse([byte_cx + lean_offset_x - byte_r,
                  byte_cy + lean_offset_y - byte_r,
                  byte_cx + lean_offset_x + byte_r,
                  byte_cy + lean_offset_y + byte_r],
                 fill=ELEC_CYAN, outline=(0, 160, 180), width=2)
    # Body pixel texture
    for bpx in range(byte_cx - byte_r + 3, byte_cx + byte_r - 3, 5):
        for bpy in range(byte_cy - byte_r + 3, byte_cy + byte_r - 3, 5):
            dist = math.sqrt((bpx - byte_cx) ** 2 + (bpy - byte_cy) ** 2)
            if dist < byte_r - 5 and rng.random() > 0.65:
                draw.rectangle([bpx, bpy, bpx + 3, bpy + 3],
                               fill=(0, 170, 192))

    # BYTE EYES — mirror composition key:
    # Left eye (organic, unguarded) — faces CENTER (toward Luma, camera-left)
    # Right eye (cracked) — faces outward (camera-right)
    # Both "first" eyes face the center of frame — the mirror
    le_bx, le_by = byte_cx - 9, byte_cy - 6
    re_bx, re_by = byte_cx + 9, byte_cy - 6

    # Left eye — organic (lid level, not droopy — damage doesn't change the decision)
    draw.rectangle([le_bx - 5, le_by - 5, le_bx + 5, le_by + 5],
                   fill=VOID_BLACK)
    draw.rectangle([le_bx - 2, le_by - 2, le_bx + 2, le_by + 2],
                   fill=ELEC_CYAN)  # clean pixel pupil
    # Top lid — level (NOT droopy)
    draw.line([le_bx - 5, le_by - 5, le_bx + 5, le_by - 5],
              fill=(0, 140, 160), width=1)

    # Right eye — CRACKED (damage present, lid level)
    draw.rectangle([re_bx - 5, re_by - 5, re_bx + 5, re_by + 5],
                   fill=VOID_BLACK)
    # Alive zone (lower-left) still glows
    draw.rectangle([re_bx - 3, re_by, re_bx + 1, re_by + 4],
                   fill=ELEC_CYAN)
    # Crack line — Hot Magenta diagonal (canonical dead-pixel glyph)
    draw.line([re_bx - 5, re_by - 5, re_bx + 5, re_by + 5],
              fill=HOT_MAGENTA, width=1)
    # Dead zone hint (upper-right dim)
    draw.rectangle([re_bx + 1, re_by - 4, re_bx + 4, re_by - 1],
                   fill=(20, 14, 30))
    # Top lid — level (NOT droopy — damage does not change decision)
    draw.line([re_bx - 5, re_by - 5, re_bx + 5, re_by - 5],
              fill=(0, 140, 160), width=1)

    # MOUTH — barely-there WARMTH arc (quiet, not performed)
    # Tiny upward arc at center bottom of face — present but understated
    mouth_y = byte_cy + byte_r - 8
    draw.arc([byte_cx - 8, mouth_y - 4, byte_cx + 8, mouth_y + 4],
             start=20, end=160, fill=(0, 185, 205), width=1)

    # Arms — slightly out from body, open (spec: not reaching, not hiding)
    for arm_side in [-1, 1]:
        ax0 = byte_cx + arm_side * (byte_r - 2)
        ay0 = byte_cy + 8
        ax1 = byte_cx + arm_side * (byte_r + 10)
        ay1 = byte_cy + 16
        draw.line([ax0, ay0, ax1, ay1], fill=(0, 172, 192), width=2)
        draw.rectangle([ax1 - 3, ay1 - 3, ax1 + 3, ay1 + 3],
                       fill=ELEC_CYAN)

    # DIRECTIONAL CYAN GLOW — brighter on left side (facing Luma), alpha 70–85
    add_glow(img, byte_cx - byte_r, byte_cy, 35, ELEC_CYAN, steps=5, max_alpha=75)  # toward Luma
    add_glow(img, byte_cx, byte_cy, 28, ELEC_CYAN, steps=4, max_alpha=35)           # body ambient
    add_glow(img, byte_cx + byte_r, byte_cy, 20, ELEC_CYAN, steps=3, max_alpha=18) # away from Luma
    draw = ImageDraw.Draw(img)

    # MIRROR ANNOTATION: visual callout of the compositional theme
    # Subtle vertical centerline marker
    center_x = W // 2
    draw.line([center_x, int(H * 0.08), center_x, int(H * 0.14)],
              fill=(80, 100, 90), width=1)
    draw.text((center_x - 16, int(H * 0.06)), "center",
              font=load_font(7), fill=(80, 100, 90))

    # "COMMITMENT BEAT" label
    label_w = 160
    lbl_x = (W - label_w) // 2
    lbl_y = int(H * 0.04)
    draw.rectangle([lbl_x - 2, lbl_y - 2, lbl_x + label_w + 2, lbl_y + 20],
                   fill=(14, 20, 18), outline=ARC_COMMIT, width=1)
    draw.text((lbl_x + 2, lbl_y + 2), "COMMITMENT BEAT — threshold",
              font=load_font(9, bold=True), fill=ARC_COMMIT)

    # Eye-level line notation
    draw.line([luma_cx + 8, luma_head_cy - 4, byte_cx - byte_r - 2, byte_cy - 4],
              fill=(60, 90, 80), width=1)
    draw.text((int(W * 0.45), luma_head_cy - 13), "EYE LEVEL",
              font=load_font(7), fill=(60, 90, 80))

    # Mirror gaze arrows (Luma's open-left eye ← center → Byte's organic-left eye)
    # Small arrows pointing to each "first" eye
    draw_arrow(draw, center_x - 6, luma_head_cy - 4,
               le_cx + 14, le_cy, color=(60, 110, 90), width=1)
    draw_arrow(draw, center_x + 6, byte_cy - 4,
               le_bx - 6, le_by, color=(60, 110, 90), width=1)

    # Annotation
    font = load_font(9)
    draw.text((4, 4), "MCU 2-SHOT — mirror: open eye|open eye face center",
              font=font, fill=CAM_COL)
    draw.text((4, 14), "Byte: frontal, descended, -3-4° lean, glow L>R",
              font=load_font(8), fill=(120, 200, 190))
    draw.rectangle([3, H - 18, 100, H - 3], fill=(10, 18, 14))
    draw.text((6, H - 16), "THRESHOLD / COMMIT", font=load_font(8), fill=ARC_COMMIT)


# ── Panel definitions ─────────────────────────────────────────────────────────

PANELS = [
    {
        "fn":    draw_p01_exterior_night,
        "label": "P01 — WIDE EXTERIOR: NIGHT",
        "cam":   "WIDE EXT — 2-pt perspective, night",
        "beat":  "Quiet residential street. Luma's house: one upstairs window still lit.",
        "arc":   ARC_QUIET,
    },
    {
        "fn":    draw_p02_establishing,
        "label": "P02 — WIDE INT: LUMA ENTERS",
        "cam":   "WIDE INT — high 2-pt perspective",
        "beat":  "Luma enters Grandma's warm, cluttered living room.",
        "arc":   ARC_QUIET,
    },
    {
        "fn":    draw_p04_luma_leans_in,
        "label": "P04 — MCU PUSH-IN: GLITCH BLEEDS",
        "cam":   "MCU — push-in / cyan bleeds FROM screen edge→Luma",
        "beat":  "Luma leans in — Glitch colors invade the Real World.",
        "arc":   ARC_TENSE,
    },
    {
        "fn":    draw_p05_two_world_touch,
        "label": "P05 — ECU: TWO-WORLD TOUCH",
        "cam":   "ECU — glass split: warm world / Glitch World",
        "beat":  "Byte presses from inside — two worlds touching at the glass.",
        "arc":   ARC_TENSE,
    },
    {
        "fn":    draw_p12_two_shot_reframe,
        "label": "P12 — MS TWO-SHOT REFRAME",
        "cam":   "MS 2-SHOT — center-weighted, equal presence",
        "beat":  "Luma (L) and Byte (R) — breathing space between them.",
        "arc":   ARC_CURIOUS,
    },
    {
        "fn":    draw_p13_mirror_commitment,
        "label": "P13 — MIRROR: COMMITMENT BEAT",
        "cam":   "MCU 2-SHOT — mirror comp / eye-level",
        "beat":  "Threshold: open-left eye / organic-left eye face center. Fulcrum.",
        "arc":   ARC_COMMIT,
    },
]


def make_contact_sheet():
    rng = random.Random(2039)

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
    draw.text((MARGIN, 26),
              "Key Beat Storyboard — 6 Panels — Diego Vargas, C39 v003",
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
        # W004 rule: refresh draw object after every paste
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
              "LTG_SB_pilot_cold_open_v003  |  output/storyboards/  |  ≤1280px  |  C39 fixes",
              font=load_font(9), fill=(100, 95, 78))

    # Image size rule: ≤ 1280px in both dimensions
    sheet.thumbnail((1280, 720), Image.LANCZOS)

    sheet.save(OUTPUT_PATH, "PNG")
    print(f"Saved: {OUTPUT_PATH}  ({sheet.size[0]}×{sheet.size[1]}px)")
    return OUTPUT_PATH


if __name__ == "__main__":
    make_contact_sheet()
    print("LTG_SB_pilot_cold_open_v003 generation complete (Cycle 39).")
    print("Changes from v002:")
    print("  - NEW P01: Exterior night shot — neighborhood, Luma's house, upstairs window lit")
    print("  - P12 TWO-SHOT: Center-weighted, equal Luma+Byte presence, breathing space")
    print("  - P13 MIRROR: Commitment beat — open-left eye / organic-left eye face center")
    print("  - P13 spec: Byte full-frontal, descended to eye-level, -3-4° lean,")
    print("             directional ELEC_CYAN glow L>R, cracked eye lid level, WARMTH arc mouth")
    print("  - P12/P13 added to contact sheet; arc-color system extended with ARC_COMMIT")
    print("  - W004 rule maintained: draw refreshed after every paste()")
