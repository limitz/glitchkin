#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_sb_panel_a204.py
Storyboard Panel A2-04 — Investigation Montage + Byte Non-Participant (Cycle 16)
Lee Tanaka, Storyboard Artist

Changes from v001 (per Carmen Reyes / Cycle 8 feedback):
  1. Add Byte as visible non-participant in second quadrant (TR)
     - Back to the action, floating near corner
     - Communicates: "I refuse to participate in this"
     - Changes scene meaning: Luma trying / Cosmo helping / Byte refusing
  2. Top two quadrants (TL/TR) now have different camera angles/staging
     for visual variety
  3. Version string updated to Cycle 16

Grid layout:
  TL — Luma searching behind TV (same — established, works)
  TR — Byte REFUSING to help (back turned, floating in corner, ignoring)
       [was: Luma under furniture — moved to BL for better arc flow]
  BL — Luma under furniture / examining desk area
  BR — Luma CLUE FOUND (same — best panel, keep it)

Byte as non-participant (TR quadrant):
  - Floating near upper-right corner of quadrant
  - Back fully turned to the action — angular body facing away
  - Arms folded tight (from behind — we see a fold silhouette)
  - Body language: pointed non-engagement
  - Caption: "search: BYTE?" or "BYTE: nope"
  - Subtle pixel confetti around him (Glitch Layer — he IS still present)
  - NO looking over shoulder — fully committed to ignoring

Output:
  /home/wipkat/team/output/storyboards/panels/LTG_SB_act2_panel_a204.png
"""

from PIL import Image, ImageDraw, ImageFont
import math
import random
import os

PANELS_DIR = "/home/wipkat/team/output/storyboards/panels"
OUTPUT_PATH = os.path.join(PANELS_DIR, "LTG_SB_act2_panel_a204.png")

os.makedirs(PANELS_DIR, exist_ok=True)

PW, PH    = 480, 270
CAPTION_H = 48
DRAW_H    = PH - CAPTION_H

BG_CAPTION   = (25, 20, 18)
TEXT_CAPTION = (235, 228, 210)
BORDER_COL   = (20, 15, 12)
STATIC_WHITE = (240, 240, 240)

LUMA_SKIN    = (200, 136, 90)
LUMA_HAIR    = (22, 14, 8)
LUMA_PJ      = (160, 200, 180)
LUMA_OUTLINE = (42, 28, 14)

BYTE_BODY    = (0, 212, 232)
BYTE_MID     = (0, 160, 175)
BYTE_DARK    = (0, 105, 115)
BYTE_OUTLINE = (10, 10, 20)
BYTE_SCAR    = (255, 45, 107)
BYTE_BEZEL   = (26, 58, 64)

GLYPH_DEAD   = (10, 10, 24)
GLYPH_DIM    = (0, 80, 100)
GLYPH_MID    = (0, 168, 180)
GLYPH_CRACK  = (255, 45, 107)
GLYPH_BRIGHT = (200, 255, 255)

GLITCH_CYAN  = (0, 240, 255)
GLITCH_MAG   = (255, 0, 200)
GLITCH_ACID  = (180, 255, 40)
GLITCH_PURPLE= (123, 47, 190)
GLITCH_WHITE = (240, 240, 240)


def load_font(size=14, bold=False):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()


def add_glow(img, cx, cy, r_max, color_rgb, steps=6, max_alpha=60):
    """ADD light via alpha_composite — never darkens."""
    for i in range(steps, 0, -1):
        r     = int(r_max * (i / steps))
        alpha = int(max_alpha * (1 - (i / steps) * 0.6))
        glow  = Image.new('RGBA', img.size, (0, 0, 0, 0))
        gd    = ImageDraw.Draw(glow)
        gd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(*color_rgb, alpha))
        base  = img.convert('RGBA')
        img.paste(Image.alpha_composite(base, glow).convert('RGB'))


def pixel_confetti(draw, cx, cy, spread_x, spread_y, rng, n=10, colors=None):
    if colors is None:
        colors = [GLITCH_CYAN, GLITCH_MAG, GLITCH_ACID, GLITCH_PURPLE, GLITCH_WHITE]
    for _ in range(n):
        px  = cx + rng.randint(-spread_x, spread_x)
        py  = cy + rng.randint(-spread_y, spread_y)
        sz  = rng.randint(2, 5)
        col = rng.choice(colors)
        draw.rectangle([px, py, px + sz, py + sz], fill=col)


def draw_montage_panel(img, draw, font, font_bold, font_cap, font_ann):
    """
    A2-04 v002: 2×2 investigation montage with Byte as non-participant in TR.
    TL: Luma behind TV (camera angle: front-on, low)
    TR: Byte REFUSING (back turned, floating in corner — camera angle: slight high angle)
    BL: Luma under furniture (camera angle: floor-level, horizontal — different from TL)
    BR: Luma CLUE FOUND (same triumphant beat — highest energy, keep)
    """
    rng = random.Random(2204)

    grid_margin = 6
    gutter      = 5
    cell_w = (PW - grid_margin * 2 - gutter) // 2
    cell_h = (DRAW_H - grid_margin * 2 - gutter) // 2

    cells = {
        'TL': (grid_margin,                          grid_margin),
        'TR': (grid_margin + cell_w + gutter,        grid_margin),
        'BL': (grid_margin,                          grid_margin + cell_h + gutter),
        'BR': (grid_margin + cell_w + gutter,        grid_margin + cell_h + gutter),
    }

    # Overall background
    draw.rectangle([0, 0, PW, DRAW_H], fill=(35, 28, 20))

    # Cell backgrounds
    cell_bgs = {
        'TL': (52, 38, 24),      # warm amber — near the TV
        'TR': (20, 28, 38),      # COOL/DARK — Byte's corner (he's making it colder)
        'BL': (40, 32, 20),      # darker — under furniture shadow
        'BR': (30, 24, 36),      # discovery — slightly cooler/purple
    }
    for key, (cx, cy) in cells.items():
        draw.rectangle([cx, cy, cx + cell_w, cy + cell_h],
                       fill=cell_bgs[key], outline=(15, 12, 8), width=2)

    # Vignette labels
    vignette_labels = {
        'TL': "search: TV  [front-on]",
        'TR': "BYTE: nope  [high angle]",
        'BL': "search: under  [floor-level]",
        'BR': "CLUE FOUND",
    }

    # ── TL: Luma behind TV (front-on, low camera) ────────────────────────────
    cx_tl, cy_tl = cells['TL']
    # Camera: front-on, slightly low (TV screen is at eye level)
    tv_x = cx_tl + cell_w // 2 - 28
    tv_y = cy_tl + cell_h // 2 - 24
    draw.rectangle([tv_x, tv_y, tv_x + 52, tv_y + 42],
                   fill=(35, 30, 25), outline=(70, 65, 58), width=3)
    draw.rectangle([tv_x + 5, tv_y + 5, tv_x + 45, tv_y + 32],
                   fill=(15, 30, 40))
    # Screen: glitch contamination
    draw.rectangle([tv_x + 8, tv_y + 8, tv_x + 28, tv_y + 20],
                   fill=(0, 80, 100))
    # TV legs
    draw.line([tv_x + 12, tv_y + 42, tv_x + 12, tv_y + 50], fill=(60, 55, 45), width=4)
    draw.line([tv_x + 40, tv_y + 42, tv_x + 40, tv_y + 50], fill=(60, 55, 45), width=4)

    # Luma peeking around left side of TV
    l_cx = tv_x - 10
    l_cy = cy_tl + cell_h // 2
    draw.ellipse([l_cx - 14, l_cy - 18, l_cx + 6, l_cy - 2], fill=LUMA_HAIR)
    draw.ellipse([l_cx - 10, l_cy - 14, l_cx + 8, l_cy + 4],
                 fill=LUMA_SKIN, outline=LUMA_OUTLINE, width=1)
    draw.ellipse([l_cx - 5, l_cy - 8, l_cx - 1, l_cy - 4], fill=(30, 20, 10))
    draw.ellipse([l_cx + 1, l_cy - 8, l_cx + 5, l_cy - 4], fill=(30, 20, 10))
    draw.ellipse([tv_x - 6, l_cy - 4, tv_x + 2, l_cy + 4],
                 fill=LUMA_SKIN, outline=LUMA_OUTLINE, width=1)
    pixel_confetti(draw, tv_x + 26, tv_y + 16, 18, 14, rng, n=6)

    # Camera angle annotation (small)
    draw.text((cx_tl + 4, cy_tl + 3), "↕ front-on", font=font_ann,
              fill=(150, 180, 150))
    draw.text((cx_tl + 4, cy_tl + cell_h - 14), vignette_labels['TL'],
              font=font_ann, fill=(200, 190, 150))

    # ── TR: Byte — REFUSING TO PARTICIPATE ───────────────────────────────────
    # Camera: slight high angle (looking down into his corner — diminishes him,
    # emphasizes his isolation, but also makes his refusal deliberate)
    cx_tr, cy_tr = cells['TR']

    # Corner indicators (we're looking into a room corner)
    # Back wall (slightly angled — high angle perspective)
    draw.rectangle([cx_tr, cy_tr, cx_tr + cell_w, cy_tr + cell_h],
                   fill=(22, 30, 40))
    # Corner shadow lines
    corner_x = cx_tr + int(cell_w * 0.75)
    draw.line([corner_x, cy_tr, corner_x, cy_tr + cell_h], fill=(16, 22, 30), width=3)
    draw.line([cx_tr, cy_tr + int(cell_h * 0.35), cx_tr + cell_w, cy_tr + int(cell_h * 0.35)],
              fill=(16, 22, 30), width=2)
    # Floor plane suggestion (high angle — we see it more)
    floor_pts_tr = [(cx_tr, cy_tr + int(cell_h * 0.60)),
                    (cx_tr + cell_w, cy_tr + int(cell_h * 0.50)),
                    (cx_tr + cell_w, cy_tr + cell_h),
                    (cx_tr, cy_tr + cell_h)]
    draw.polygon(floor_pts_tr, fill=(26, 36, 48))

    # ── BYTE — back turned, floating in corner, refusing ──────────────────
    # Byte floats slightly above floor, in upper-right corner of this cell
    # BACK TO CAMERA (we see his back — no face visible)
    byte_cx = cx_tr + int(cell_w * 0.68)
    byte_cy = cy_tr + int(cell_h * 0.42)

    byte_w = 36    # body width
    byte_h = 30    # body height

    # Body (oval, seen from behind — slightly compressed due to angle)
    # Back face: slightly darker than front body color
    draw.ellipse([byte_cx - byte_w // 2, byte_cy - byte_h // 2,
                  byte_cx + byte_w // 2, byte_cy + byte_h // 2],
                 fill=BYTE_MID, outline=BYTE_OUTLINE, width=2)
    # Back center seam (visible from behind)
    draw.line([byte_cx, byte_cy - byte_h // 2 + 4,
               byte_cx, byte_cy + byte_h // 2 - 4],
              fill=BYTE_DARK, width=1)

    # ARMS: tight against body from behind — folded/drawn in
    # Left arm (his left, our left — visible from behind as slight bulge)
    draw.ellipse([byte_cx - byte_w // 2 - 6, byte_cy - 4,
                  byte_cx - byte_w // 2 + 8, byte_cy + 16],
                 fill=BYTE_MID, outline=BYTE_OUTLINE, width=1)
    # Right arm (his right, our right)
    draw.ellipse([byte_cx + byte_w // 2 - 8, byte_cy - 4,
                  byte_cx + byte_w // 2 + 6, byte_cy + 16],
                 fill=BYTE_MID, outline=BYTE_OUTLINE, width=1)

    # Legs (slightly pulled inward — retreating posture from behind)
    draw.ellipse([byte_cx - 12, byte_cy + byte_h // 2 - 4,
                  byte_cx - 2,  byte_cy + byte_h // 2 + 18],
                 fill=BYTE_DARK, outline=BYTE_OUTLINE, width=1)
    draw.ellipse([byte_cx + 2,  byte_cy + byte_h // 2 - 4,
                  byte_cx + 12, byte_cy + byte_h // 2 + 18],
                 fill=BYTE_DARK, outline=BYTE_OUTLINE, width=1)

    # Head (oval, seen from behind — just the back of the head)
    head_w_b = 28
    head_h_b = 24
    head_top_b = byte_cy - byte_h // 2 - head_h_b - 2
    draw.ellipse([byte_cx - head_w_b // 2, head_top_b,
                  byte_cx + head_w_b // 2, head_top_b + head_h_b],
                 fill=BYTE_BODY, outline=BYTE_OUTLINE, width=2)
    # Back-of-head glint (visible from behind — we only see the back)
    draw.arc([byte_cx - head_w_b // 2 + 3, head_top_b + 2,
              byte_cx + head_w_b // 2 - 3, head_top_b + head_h_b - 2],
             start=180, end=360, fill=(0, 200, 220), width=1)

    # "Eye slash" suggestion on back of head (since we CAN'T see his face)
    # Small X marks where eyes would be — communicating "face turned away"
    ex_y = head_top_b + head_h_b // 2 - 2
    draw.line([byte_cx - 8, ex_y - 3, byte_cx - 3, ex_y + 3],
              fill=BYTE_OUTLINE, width=1)
    draw.line([byte_cx - 3, ex_y - 3, byte_cx - 8, ex_y + 3],
              fill=BYTE_OUTLINE, width=1)
    draw.line([byte_cx + 3, ex_y - 3, byte_cx + 8, ex_y + 3],
              fill=BYTE_OUTLINE, width=1)
    draw.line([byte_cx + 8, ex_y - 3, byte_cx + 3, ex_y + 3],
              fill=BYTE_OUTLINE, width=1)

    # Subtle Byte glow (he IS present digitally even if refusing physically)
    add_glow(img, byte_cx, byte_cy, 22, (0, 180, 200), steps=4, max_alpha=25)
    draw = ImageDraw.Draw(img)

    # Pixel confetti around Byte (Glitch Layer — his digital nature)
    pixel_confetti(draw, byte_cx, byte_cy, 20, 20, rng, n=8,
                   colors=[GLITCH_CYAN, (0, 120, 140), (0, 80, 100)])

    # "NOPE" thought-cloud above Byte (floating away from him)
    draw.text((byte_cx - cell_w + 14, cy_tr + 5),
              '"nope."', font=font_cap, fill=(140, 180, 180))

    # Camera angle annotation
    draw.text((cx_tr + 4, cy_tr + 3), "↓ high angle", font=font_ann,
              fill=(120, 160, 180))
    draw.text((cx_tr + 4, cy_tr + cell_h - 14), vignette_labels['TR'],
              font=font_ann, fill=(100, 200, 220))

    # ── BL: Luma under furniture (floor-level camera — distinctly different from TL) ──
    cx_bl, cy_bl = cells['BL']
    # Camera: floor level — we look HORIZONTALLY from floor level
    # This means we see a lot of ceiling, furniture bottom, and just Luma's head/shoulders
    floor_bl = cy_bl + int(cell_h * 0.72)
    draw.rectangle([cx_bl, cy_bl, cx_bl + cell_w, floor_bl], fill=(36, 28, 18))
    draw.rectangle([cx_bl, floor_bl, cx_bl + cell_w, cy_bl + cell_h], fill=(55, 42, 28))
    draw.line([cx_bl, floor_bl, cx_bl + cell_w, floor_bl], fill=(40, 30, 18), width=2)

    # Camera angle annotation
    draw.text((cx_bl + 4, cy_bl + 3), "→ floor-level", font=font_ann,
              fill=(180, 160, 120))

    # Furniture bottom (camera at floor = we see furniture underside)
    for leg_x in [cx_bl + 8, cx_bl + cell_w - 18]:
        draw.rectangle([leg_x, cy_bl + int(cell_h * 0.20), leg_x + 10, floor_bl + 2],
                       fill=(90, 70, 50), outline=(55, 42, 28), width=1)
    # Furniture base (bottom surface visible from floor cam)
    draw.rectangle([cx_bl + 4, cy_bl + int(cell_h * 0.18),
                    cx_bl + cell_w - 4, cy_bl + int(cell_h * 0.24)],
                   fill=(110, 85, 55), outline=(80, 60, 40), width=1)

    # Luma on hands and knees, seen from side/front (floor cam = only upper body visible)
    l_cx = cx_bl + cell_w // 2
    l_cy = floor_bl - 14
    # Body (just upper torso at this camera angle)
    draw.ellipse([l_cx - 20, l_cy - 8, l_cx + 18, l_cy + 8],
                 fill=LUMA_PJ, outline=LUMA_OUTLINE, width=1)
    # Head (looking into the under-furniture area — forward)
    draw.ellipse([l_cx + 8, l_cy - 16, l_cx + 30, l_cy + 2],
                 fill=LUMA_SKIN, outline=LUMA_OUTLINE, width=1)
    draw.ellipse([l_cx + 8, l_cy - 26, l_cx + 28, l_cy - 12], fill=LUMA_HAIR)
    draw.ellipse([l_cx + 20, l_cy - 11, l_cx + 24, l_cy - 7], fill=(30, 20, 10))
    # Arm reaching under
    draw.line([l_cx + 22, l_cy - 4, l_cx + 42, l_cy + 8], fill=LUMA_SKIN, width=5)
    # Dust motes (floor level = lots of floor detail)
    for _ in range(8):
        dx = cx_bl + rng.randint(8, cell_w - 8)
        dy = floor_bl - rng.randint(2, 12)
        draw.rectangle([dx, dy, dx + rng.randint(3, 8), dy + 1],
                       fill=(55, 45, 30))

    draw.text((cx_bl + 4, cy_bl + cell_h - 14), vignette_labels['BL'],
              font=font_ann, fill=(190, 180, 140))

    # ── BR: Luma FOUND A CLUE — triumphant (UNCHANGED — best panel) ──────────
    cx_br, cy_br = cells['BR']

    l_cx = cx_br + cell_w // 2
    l_cy = cy_br + cell_h // 2 + 5
    # Body
    draw.rounded_rectangle([l_cx - 16, l_cy, l_cx + 16, l_cy + 28],
                            radius=6, fill=LUMA_PJ, outline=LUMA_OUTLINE, width=1)
    # Head
    draw.ellipse([l_cx - 14, l_cy - 28, l_cx + 14, l_cy + 2],
                 fill=LUMA_SKIN, outline=LUMA_OUTLINE, width=1)
    draw.ellipse([l_cx - 18, l_cy - 42, l_cx + 18, l_cy - 18], fill=LUMA_HAIR)
    # Big excited eyes
    draw.ellipse([l_cx - 8, l_cy - 20, l_cx - 2, l_cy - 13], fill=(235, 215, 180))
    draw.ellipse([l_cx + 2, l_cy - 20, l_cx + 8, l_cy - 13], fill=(235, 215, 180))
    draw.ellipse([l_cx - 6, l_cy - 19, l_cx - 3, l_cy - 15], fill=(30, 20, 10))
    draw.ellipse([l_cx + 3, l_cy - 19, l_cx + 6, l_cy - 15], fill=(30, 20, 10))
    draw.rectangle([l_cx - 6, l_cy - 19, l_cx - 5, l_cy - 18], fill=STATIC_WHITE)
    draw.rectangle([l_cx + 3, l_cy - 19, l_cx + 4, l_cy - 18], fill=STATIC_WHITE)
    draw.ellipse([l_cx - 5, l_cy - 10, l_cx + 5, l_cy - 4], fill=(20, 14, 10))

    # Raised arm holding glowing clue
    draw.line([l_cx + 12, l_cy + 4, l_cx + 28, l_cy - 28], fill=LUMA_SKIN, width=7)
    clue_cx = l_cx + 30
    clue_cy = l_cy - 34
    draw.rectangle([clue_cx - 6, clue_cy - 6, clue_cx + 6, clue_cy + 6],
                   fill=GLITCH_CYAN, outline=(0, 180, 200), width=2)
    draw.rectangle([clue_cx - 3, clue_cy - 3, clue_cx + 3, clue_cy + 3],
                   fill=GLYPH_BRIGHT)

    # Glow from clue
    add_glow(img, clue_cx, clue_cy, 22, (0, 220, 240), steps=5, max_alpha=55)
    draw = ImageDraw.Draw(img)

    # Pixel confetti from clue
    pixel_confetti(draw, clue_cx, clue_cy, 28, 28, rng, n=10)
    draw.text((l_cx - 12, l_cy - 50), "AHA!", font=font_bold, fill=(0, 230, 255))
    draw.text((cx_br + 4, cy_br + cell_h - 14), vignette_labels['BR'],
              font=font_ann, fill=(160, 240, 220))

    # ── Grid divider lines ────────────────────────────────────────────────────
    mid_x = grid_margin + cell_w + gutter // 2
    mid_y = grid_margin + cell_h + gutter // 2
    draw.line([mid_x, grid_margin, mid_x, DRAW_H - grid_margin],
              fill=(20, 16, 12), width=gutter)
    draw.line([grid_margin, mid_y, PW - grid_margin, mid_y],
              fill=(20, 16, 12), width=gutter)

    # ── Montage header ────────────────────────────────────────────────────────
    draw.text((PW // 2 - 58, 3), "MONTAGE — INVESTIGATION + REFUSAL",
              font=font_ann, fill=(180, 170, 130))


def generate():
    font     = load_font(13)
    font_b   = load_font(13, bold=True)
    font_cap = load_font(11)
    font_ann = load_font(9)

    img  = Image.new('RGB', (PW, PH), (35, 28, 20))
    draw = ImageDraw.Draw(img)

    draw_montage_panel(img, draw, font, font_b, font_cap, font_ann)

    # Caption bar
    draw.rectangle([0, DRAW_H, PW, PH], fill=BG_CAPTION)
    draw.line([0, DRAW_H, PW, DRAW_H], fill=BORDER_COL, width=2)
    draw.text((8, DRAW_H + 6), "A2-04  MONTAGE 2×2  mixed camera angles",
              font=font_cap, fill=(160, 160, 160))
    draw.text((8, DRAW_H + 20),
              "Luma searches (TL/BL/BR) — Byte REFUSES in corner (TR). Luma trying / Byte pointedly not.",
              font=font_cap, fill=TEXT_CAPTION)
    draw.text((8, DRAW_H + 34),
              "TR high angle isolates Byte's refusal  |  BL floor-level = varied camera from TL",
              font=font_ann, fill=(150, 140, 110))

    # Border
    draw.rectangle([0, 0, PW - 1, PH - 1], outline=BORDER_COL, width=2)

    img.save(OUTPUT_PATH, "PNG")
    print(f"Saved: {OUTPUT_PATH}")
    return OUTPUT_PATH


if __name__ == "__main__":
    generate()
    print("A2-04 v002 generation complete (Cycle 16).")
