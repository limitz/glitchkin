#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_sb_panel_a101.py
Storyboard Panel A1-01 — ESTABLISHING — Grandma Miri's Kitchen — Cycle 18
Lee Tanaka, Storyboard Artist

Beat: Cold open. Morning. Grandma Miri's kitchen.
Warm, cozy, analogue. No characters yet.
CRT TV visible through doorway into adjacent room — glow on, static.
This is the world before the intrusion. Safe. Familiar.

Shot: WIDE — interior establishing
Camera: Slightly high angle (10-15° down), three-quarter view of kitchen.
        Two-point perspective. Sink under window BG-center. Table FG-left.
        Doorway to adjacent room visible at right edge — CRT glow bleeds through.

Palette: ALL REAL WORLD warm tones (cream, amber, wood).
         Exception: faint cyan glow ONLY through doorway (distant CRT).

Arc: QUIET — establishing warmth before intrusion.
"""

from PIL import Image, ImageDraw, ImageFont
import math, random, os

PANELS_DIR  = "/home/wipkat/team/output/storyboards/panels"
OUTPUT_PATH = os.path.join(PANELS_DIR, "LTG_SB_act1_panel_a101.png")
os.makedirs(PANELS_DIR, exist_ok=True)

PW, PH    = 800, 600
CAPTION_H = 60
DRAW_H    = PH - CAPTION_H   # 540

# ── Palette ─────────────────────────────────────────────────────────────────
WARM_CREAM   = (250, 240, 220)
WALL_WARM    = (240, 222, 188)
WALL_SHADOW  = (200, 182, 152)
CEILING_WARM = (248, 238, 214)
FLOOR_LIGHT  = (212, 196, 162)
FLOOR_DARK   = (190, 174, 142)
WOOD_DARK    = (130,  85,  42)
WOOD_MED     = (168, 118,  62)
WOOD_WORN    = (185, 140,  80)
COUNTERTOP   = (200, 182, 148)
SINK_WHITE   = (230, 226, 214)
MORNING_GOLD = (255, 200,  80)
SUNLIT_AMB   = (212, 146,  58)
CURTAIN_WARM = (238, 198, 128)
PLANT_GREEN  = (88,  138,  72)
TEAPOT_RED   = (192,  72,  48)
MUG_EARTHY   = (160, 112,  72)
LINE_DARK    = (100,  72,  40)
SHADOW_WARM  = (180, 152, 108)
DEEP_SHADOW  = (130,  98,  62)
# CRT glow (faint — distant room, far plane)
CRT_CYAN_DIM = (0, 220, 240)
BG_CAPTION   = (22, 18, 14)
TEXT_CAP     = (235, 228, 210)
ANN_COL      = (200, 175, 120)
ANN_DIM      = (150, 135, 100)


def load_font(size=14, bold=False):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, size)
            except Exception: pass
    return ImageFont.load_default()


def add_glow(img, cx, cy, r_max, color_rgb, steps=6, max_alpha=50):
    """ADD light via alpha_composite — never darkens."""
    for i in range(steps, 0, -1):
        r     = int(r_max * (i / steps))
        alpha = int(max_alpha * (1 - (i / steps) * 0.6))
        glow  = Image.new('RGBA', img.size, (0, 0, 0, 0))
        gd    = ImageDraw.Draw(glow)
        gd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(*color_rgb, alpha))
        base  = img.convert('RGBA')
        img.paste(Image.alpha_composite(base, glow).convert('RGB'))


def draw_scene(img):
    draw = ImageDraw.Draw(img)
    rng  = random.Random(101)

    # ── Background: ceiling + walls ──────────────────────────────────────────
    draw.rectangle([0, 0, PW, DRAW_H], fill=WALL_WARM)

    # Ceiling plane (slightly lighter, angled in 2-pt perspective)
    ceiling_pts = [(0, 0), (PW, 0), (PW, int(DRAW_H * 0.22)), (0, int(DRAW_H * 0.28))]
    draw.polygon(ceiling_pts, fill=CEILING_WARM)
    # Ceiling-wall seam
    draw.line([(0, int(DRAW_H * 0.28)), (PW, int(DRAW_H * 0.22))], fill=SHADOW_WARM, width=2)

    # Morning light wash from window area (upper center-left)
    add_glow(img, int(PW * 0.38), int(DRAW_H * 0.15), 200, MORNING_GOLD, steps=7, max_alpha=30)
    draw = ImageDraw.Draw(img)

    # ── Floor plane ──────────────────────────────────────────────────────────
    floor_y = int(DRAW_H * 0.72)
    floor_pts = [(0, floor_y), (PW, floor_y - 30), (PW, DRAW_H), (0, DRAW_H)]
    draw.polygon(floor_pts, fill=FLOOR_LIGHT)
    # Checkerboard linoleum tiles (light/dark, 2-pt perspective)
    tile_cols = 10
    tile_rows = 4
    for row in range(tile_rows + 1):
        for col in range(tile_cols):
            # Perspective: tiles foreshorten toward horizon
            frac_y0 = row / (tile_rows + 1)
            frac_y1 = (row + 1) / (tile_rows + 1)
            ty0 = int(floor_y + frac_y0 * (DRAW_H - floor_y))
            ty1 = int(floor_y + frac_y1 * (DRAW_H - floor_y))
            tx0 = int((col / tile_cols) * PW)
            tx1 = int(((col + 1) / tile_cols) * PW)
            if (row + col) % 2 == 0:
                draw.rectangle([tx0, ty0, tx1, ty1], fill=FLOOR_LIGHT)
            else:
                draw.rectangle([tx0, ty0, tx1, ty1], fill=FLOOR_DARK)
    # Floor-wall seam
    draw.line([(0, floor_y), (PW, floor_y - 30)], fill=SHADOW_WARM, width=2)

    # ── Left wall: cabinets + counter ────────────────────────────────────────
    # Base cabinet (lower-left)
    cab_left_x  = 0
    cab_right_x = int(PW * 0.25)
    cab_top_y   = int(DRAW_H * 0.48)
    cab_bot_y   = floor_y
    draw.rectangle([cab_left_x, cab_top_y, cab_right_x, cab_bot_y], fill=WOOD_DARK)
    # Counter surface
    ctr_h = 10
    draw.rectangle([cab_left_x, cab_top_y - ctr_h, cab_right_x + 8, cab_top_y],
                   fill=COUNTERTOP, outline=LINE_DARK, width=1)
    # Cabinet doors (2 doors on lower)
    door_mid = cab_left_x + (cab_right_x - cab_left_x) // 2
    for dx, dw in [(cab_left_x + 4, door_mid - cab_left_x - 8),
                   (door_mid + 4, cab_right_x - door_mid - 8)]:
        draw.rectangle([dx, cab_top_y + 5, dx + dw, cab_bot_y - 3],
                       fill=WOOD_MED, outline=LINE_DARK, width=1)
        # Knob
        draw.ellipse([dx + dw // 2 - 3, (cab_top_y + cab_bot_y) // 2 - 3,
                      dx + dw // 2 + 3, (cab_top_y + cab_bot_y) // 2 + 3],
                     fill=SHADOW_WARM, outline=LINE_DARK, width=1)
    # Upper cabinet (wall-mounted)
    ucab_top = int(DRAW_H * 0.28)
    ucab_bot = int(DRAW_H * 0.44)
    draw.rectangle([0, ucab_top, int(PW * 0.22), ucab_bot],
                   fill=WOOD_DARK, outline=LINE_DARK, width=1)
    # Upper cabinet door
    draw.rectangle([4, ucab_top + 4, int(PW * 0.22) - 4, ucab_bot - 4],
                   fill=WOOD_MED, outline=LINE_DARK, width=1)

    # ── Background wall: window with morning light ────────────────────────────
    # Window frame (center-back)
    win_cx   = int(PW * 0.42)
    win_top  = int(DRAW_H * 0.28)
    win_bot  = int(DRAW_H * 0.55)
    win_w    = int(PW * 0.22)
    draw.rectangle([win_cx - win_w // 2, win_top, win_cx + win_w // 2, win_bot],
                   fill=MORNING_GOLD, outline=LINE_DARK, width=3)
    # Window interior (bright morning sky)
    draw.rectangle([win_cx - win_w // 2 + 5, win_top + 5,
                    win_cx + win_w // 2 - 5, win_bot - 5],
                   fill=(255, 220, 140))
    # Window cross-bars
    draw.line([win_cx, win_top, win_cx, win_bot], fill=LINE_DARK, width=2)
    draw.line([win_cx - win_w // 2, (win_top + win_bot) // 2,
               win_cx + win_w // 2, (win_top + win_bot) // 2], fill=LINE_DARK, width=2)
    # Curtains (half-drawn)
    for side, sign in [(-1, -1), (1, 1)]:
        cx0 = win_cx + sign * win_w // 2 - sign * 15
        cx1 = win_cx + sign * win_w // 2 + sign * 20
        draw.rectangle([min(cx0, cx1), win_top - 4, max(cx0, cx1), win_bot],
                       fill=CURTAIN_WARM, outline=LINE_DARK, width=1)
        # Curtain folds
        for fy in range(win_top, win_bot, 12):
            draw.arc([min(cx0, cx1), fy, max(cx0, cx1), fy + 10],
                     start=0 if sign == 1 else 180, end=180 if sign == 1 else 360,
                     fill=SHADOW_WARM, width=1)
    # Morning sunlight pour from window onto counter
    add_glow(img, win_cx, int(DRAW_H * 0.62), 140, SUNLIT_AMB, steps=5, max_alpha=28)
    draw = ImageDraw.Draw(img)

    # Sink under window
    sink_cx = int(PW * 0.42)
    sink_top = int(DRAW_H * 0.55)
    sink_bot = int(DRAW_H * 0.66)
    sink_w   = int(PW * 0.18)
    # Counter under sink
    draw.rectangle([sink_cx - sink_w // 2 - 10, sink_top - 5,
                    sink_cx + sink_w // 2 + 10, sink_top + 2],
                   fill=COUNTERTOP, outline=LINE_DARK, width=1)
    # Sink basin
    draw.rectangle([sink_cx - sink_w // 2, sink_top,
                    sink_cx + sink_w // 2, sink_bot],
                   fill=SINK_WHITE, outline=LINE_DARK, width=2)
    # Faucet
    draw.line([sink_cx, sink_top - 8, sink_cx, sink_top - 22], fill=LINE_DARK, width=3)
    draw.arc([sink_cx - 10, sink_top - 26, sink_cx + 10, sink_top - 14],
             start=0, end=180, fill=LINE_DARK, width=3)
    # Dish by sink
    draw.ellipse([sink_cx + sink_w // 2 + 4, sink_top - 5,
                  sink_cx + sink_w // 2 + 28, sink_top + 4],
                 fill=(238, 236, 228), outline=LINE_DARK, width=1)

    # Small plant on counter (window sill)
    plant_x = int(PW * 0.32)
    plant_y = int(DRAW_H * 0.50)
    # Pot
    draw.polygon([(plant_x - 8, plant_y + 12), (plant_x + 8, plant_y + 12),
                  (plant_x + 6, plant_y + 22), (plant_x - 6, plant_y + 22)],
                 fill=MUG_EARTHY, outline=LINE_DARK)
    # Leaves
    for lx, ly, lr in [(plant_x - 6, plant_y, 9), (plant_x + 5, plant_y - 5, 8),
                        (plant_x, plant_y - 10, 7)]:
        draw.ellipse([lx - lr, ly - lr, lx + lr, ly + lr], fill=PLANT_GREEN,
                     outline=(60, 90, 48), width=1)

    # Teapot on stove (right of sink)
    tp_x = int(PW * 0.57)
    tp_y = int(DRAW_H * 0.57)
    draw.ellipse([tp_x - 18, tp_y - 14, tp_x + 18, tp_y + 12],
                 fill=TEAPOT_RED, outline=LINE_DARK, width=2)
    draw.rectangle([tp_x - 20, tp_y - 16, tp_x + 20, tp_y - 10],
                   fill=TEAPOT_RED, outline=LINE_DARK, width=1)
    draw.line([tp_x + 16, tp_y - 8, tp_x + 28, tp_y - 4], fill=LINE_DARK, width=2)  # spout
    draw.arc([tp_x + 14, tp_y - 12, tp_x + 24, tp_y], start=270, end=90,
             fill=LINE_DARK, width=2)  # handle

    # Mug on table (FG)
    mug_x = int(PW * 0.18)
    mug_y = int(DRAW_H * 0.62)
    draw.rectangle([mug_x - 10, mug_y - 14, mug_x + 10, mug_y + 2],
                   fill=MUG_EARTHY, outline=LINE_DARK, width=2)
    draw.arc([mug_x + 8, mug_y - 10, mug_x + 18, mug_y - 2],
             start=270, end=90, fill=LINE_DARK, width=2)

    # ── Table (FG-left) ───────────────────────────────────────────────────────
    tbl_left  = 0
    tbl_right = int(PW * 0.3)
    tbl_top   = int(DRAW_H * 0.60)
    tbl_bot   = int(DRAW_H * 0.67)
    draw.rectangle([tbl_left, tbl_top, tbl_right, tbl_bot],
                   fill=WOOD_MED, outline=LINE_DARK, width=2)
    # Table surface grain
    for gx in range(0, tbl_right, 18):
        draw.line([gx, tbl_top + 1, gx + 5, tbl_bot - 1], fill=WOOD_WORN, width=1)
    # Table leg (visible FG-left)
    draw.rectangle([4, tbl_bot, 14, floor_y], fill=WOOD_DARK, outline=LINE_DARK, width=1)
    # Crossword puzzle on table
    cw_x = int(PW * 0.07)
    cw_y = tbl_top - 16
    draw.rectangle([cw_x - 20, cw_y, cw_x + 32, cw_y + 18],
                   fill=WARM_CREAM, outline=LINE_DARK, width=1)
    # Crossword grid lines
    for i in range(3):
        draw.line([cw_x - 20, cw_y + i * 6, cw_x + 32, cw_y + i * 6],
                  fill=LINE_DARK, width=1)
    for j in range(5):
        draw.line([cw_x - 20 + j * 10, cw_y, cw_x - 20 + j * 10, cw_y + 18],
                  fill=LINE_DARK, width=1)
    # Some filled squares
    for sq_x, sq_y in [(cw_x - 10, cw_y), (cw_x, cw_y + 6), (cw_x + 10, cw_y + 12)]:
        draw.rectangle([sq_x, sq_y, sq_x + 9, sq_y + 5], fill=LINE_DARK)

    # ── Right wall: doorway to adjacent room (CRT TV visible) ────────────────
    # Right-side wall with door opening
    door_left  = int(PW * 0.76)
    door_right = PW
    door_top   = int(DRAW_H * 0.26)
    # Dark doorway opening
    draw.rectangle([door_left, door_top, door_right, floor_y - 10],
                   fill=(38, 30, 20))
    # Doorframe
    draw.rectangle([door_left - 5, door_top - 3, door_left + 2, floor_y - 8],
                   fill=WOOD_DARK, outline=LINE_DARK, width=1)
    draw.rectangle([door_left - 5, door_top - 5, door_right, door_top + 2],
                   fill=WOOD_DARK, outline=LINE_DARK, width=1)

    # CRT TV visible through doorway — far plane, partially visible
    tv_x   = int(PW * 0.84)
    tv_y   = int(DRAW_H * 0.37)
    tv_w   = 52
    tv_h   = 42
    # TV body (old CRT — rounded corners, deep plastic)
    draw.rectangle([tv_x - tv_w // 2, tv_y,
                    tv_x + tv_w // 2, tv_y + tv_h],
                   fill=(60, 52, 42), outline=(80, 70, 55), width=2)
    # CRT screen (showing static — warm grey with cyan glow on)
    screen_margin = 5
    draw.rectangle([tv_x - tv_w // 2 + screen_margin,
                    tv_y + screen_margin,
                    tv_x + tv_w // 2 - screen_margin,
                    tv_y + tv_h - screen_margin - 2],
                   fill=(100, 112, 100))  # static grey-green
    # Screen glow (the TV is ON — static)
    add_glow(img, tv_x, tv_y + tv_h // 2, 55, CRT_CYAN_DIM, steps=5, max_alpha=35)
    draw = ImageDraw.Draw(img)
    # TV base/legs
    draw.rectangle([tv_x - 8, tv_y + tv_h, tv_x + 8, tv_y + tv_h + 5],
                   fill=(50, 42, 32), outline=(70, 60, 48), width=1)
    # Small stand/shelf under TV
    draw.rectangle([tv_x - tv_w // 2 - 4, tv_y + tv_h + 4,
                    tv_x + tv_w // 2 + 4, tv_y + tv_h + 8],
                   fill=WOOD_MED, outline=LINE_DARK, width=1)

    # CRT glow bleeds into kitchen doorway (faint cyan wash on kitchen floor/right wall)
    add_glow(img, door_left + 10, int(DRAW_H * 0.58), 80, CRT_CYAN_DIM,
             steps=4, max_alpha=18)
    draw = ImageDraw.Draw(img)

    # ── Annotations ──────────────────────────────────────────────────────────
    font_ann = load_font(11)
    draw.text((10, 8), "A1-01  /  WIDE  /  slightly high angle  /  two-point perspective",
              font=font_ann, fill=ANN_COL)
    draw.text((10, 20), "Grandma Miri's kitchen — morning — no characters",
              font=font_ann, fill=ANN_DIM)

    # Arrow pointing to doorway / CRT TV
    draw.line([(int(PW * 0.72), int(DRAW_H * 0.35)),
               (int(PW * 0.78), int(DRAW_H * 0.40))], fill=(0, 200, 220), width=2)
    draw.text((int(PW * 0.58), int(DRAW_H * 0.28)), "CRT TV — glow on",
              font=font_ann, fill=(0, 200, 220))
    draw.text((int(PW * 0.58), int(DRAW_H * 0.28) + 10), "static (KEY STORY ELEMENT)",
              font=font_ann, fill=(0, 170, 190))

    # Window sunlight callout
    draw.text((int(PW * 0.29), int(DRAW_H * 0.16)), "morning sunlight",
              font=font_ann, fill=(220, 180, 80))

    # "ESTABLISHING" label
    draw.rectangle([10, DRAW_H - 22, 130, DRAW_H - 5], fill=(60, 50, 35))
    draw.text((14, DRAW_H - 20), "ESTABLISHING SHOT",
              font=font_ann, fill=(240, 220, 140))

    return draw


def make_panel():
    font_cap = load_font(12)
    font_ann = load_font(11)

    img  = Image.new('RGB', (PW, PH), WALL_WARM)
    draw_scene(img)
    draw = ImageDraw.Draw(img)

    # Caption bar
    draw.rectangle([0, DRAW_H, PW, PH], fill=BG_CAPTION)
    draw.line([0, DRAW_H, PW, DRAW_H], fill=(18, 12, 8), width=2)
    draw.text((10, DRAW_H + 5), "A1-01  WIDE  slightly high angle  kitchen establishing — no characters",
              font=font_cap, fill=(160, 155, 130))
    draw.text((10, DRAW_H + 20),
              "Grandma Miri's kitchen, morning. CRT TV in adjacent room — glow on, static.",
              font=font_cap, fill=TEXT_CAP)
    draw.text((10, DRAW_H + 36),
              "QUIET arc beat — warm, analogue, safe. World before intrusion. CRT = story trigger.",
              font=font_ann, fill=(150, 140, 110))
    draw.text((PW - 240, DRAW_H + 46), "LTG_SB_act1_panel_a101_v001",
              font=font_ann, fill=(100, 95, 78))

    # Border
    draw.rectangle([0, 0, PW - 1, PH - 1], outline=(18, 12, 8), width=2)

    img.save(OUTPUT_PATH, "PNG")
    print(f"Saved: {OUTPUT_PATH}")
    return OUTPUT_PATH


if __name__ == "__main__":
    make_panel()
    print("A1-01 panel generation complete (Cycle 18).")
