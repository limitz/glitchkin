#!/usr/bin/env python3
"""
LTG_TOOL_byte_expression_sheet_v005.py
Byte Expression Sheet — v005 UNGUARDED WARMTH
"Luma & the Glitchkin" — Cycle 33 / Maya Santos

v005 ADDITION (Alex Chen C33 Directive):
  UNGUARDED WARMTH — 10th expression.
  Narrative: Luma has done something for Byte that he can't dismiss.
  He has looked away but the warmth is already on his face. He knows it.
  He isn't fighting it this time.

  Spec:
    Body:
      - body_tilt = -4 (very slight lean toward Luma — unconscious)
      - arm_l_dy = -5, arm_r_dy = -5 (limbs slightly forward/upward float)
      - leg_spread = 0.85 (left leg 2px forward — subtle turn)
      - body_squash = 1.0 (no squash)

    Eyes:
      - Left (pixel, viewer's left = cracked eye): HEART glyph in UV_PURPLE #7B2FBE.
        5×5 grid per Alex Chen spec. "He's been broken open."
      - Right (organic, viewer's right): star glyph at FULL SOFT_GOLD #E8C95A.
        Key difference from SECRETLY PLEASED (Expression 8): star at FULL brightness.
        "He has stopped trying to hide it."

    Mouth: "warmth" — very slight upward arc. Almost not there.

    Hover confetti: SOFT_GOLD (#E8C95A) — 3 small 10×10 squares.
      ONLY expression to use gold confetti. Subtle visual signal.

    Panel BG: warm cream leaning slightly cool — (240, 224, 198).
      "He exists at the border between his cold world and her warm one."

  Squint test:
    vs ACCIDENTAL AFFECTION (Expr 3): body NOT pulling away, star NOT gone.
    vs SECRETLY PLEASED (Expr 8): star at FULL brightness (not 50%), heart present
      on cracked eye, body leans slightly IN.

v005 GRID:
  4×3 layout (12 slots, 10 filled, slots 10 and 11 empty).
  Canvas: 1280×960 (4 rows × 320px + 50px header + 16px padding).
  Image will be thumbnail'd to ≤1280px.

v005 CHANGES FROM v004:
  - Grid: 3×3 → 4×3 (12 slots)
  - UNGUARDED WARMTH added (Expression 10, slot index 9)
  - New pixel symbol: "star_gold" (5×5) — SOFT_GOLD pixels
  - New pixel symbol: "heart_purple" (5×5) — UV_PURPLE pixels
  - New right eye style: "warmth_open" (star glyph, no organic eye)
  - New emotion: "warmth" (barely-there upward arc)
  - New confetti color: SOFT_GOLD (#E8C95A) — unguarded warmth only
  - Sheet title updated to v005

Output: output/characters/main/LTG_CHAR_byte_expression_sheet_v005.png
"""
from PIL import Image, ImageDraw, ImageFont
import math
import os

# ── Palette ────────────────────────────────────────────────────────────────────
BYTE_TEAL  = (0, 212, 232)     # GL-01b #00D4E8 — body fill (ALWAYS)
BYTE_HL    = (0, 240, 255)     # GL-01  #00F0FF — highlights/circuit traces only
BYTE_SH    = (0, 168, 192)     # GL-01a #00A8C0 — Deep Cyan shadow companion
HOT_MAG    = (255, 45, 120)    # #FF2D78 — Hot Magenta crack line (Section 9B)
SCAR_MAG   = (255, 45, 107)    # #FF2D6B — body scar markings
UV_PURPLE  = (123, 47, 190)    # #7B2FBE — UV Purple (cracked eye heart)
SOFT_GOLD  = (232, 201, 90)    # #E8C95A — Soft Gold (unguarded warmth confetti + star)
LINE       = (10, 10, 20)      # #0A0A14 void black
EYE_W      = (240, 240, 245)
BG         = (20, 18, 28)
VOID_BLACK = (10, 10, 20)

# Panel backgrounds
BG_NEUTRAL  = (28, 34, 42)
BG_GRUMPY   = (38, 20, 28)
BG_SEARCH   = (22, 30, 44)
BG_ALARM    = (18, 28, 44)
BG_RELJOY   = (22, 34, 32)
BG_CONFUSE  = (30, 24, 42)
BG_PWRDOWN  = (14, 12, 18)
BG_RESIGNED = (24, 26, 34)
BG_STORM    = (12, 10, 22)
BG_WARMTH   = (240, 224, 198)  # warm cream leaning cool — "border between worlds"

# ── Layout ─────────────────────────────────────────────────────────────────────
PANEL_W = 240
PANEL_H = 320
COLS    = 3
ROWS    = 4   # 4×3 for 12 slots
PAD     = 16
HEADER  = 50


# ── Expression definitions ─────────────────────────────────────────────────────
# Format: (name, pixel_symbol, emotion, body_data, right_eye_style, panel_bg, prev_st, next_st)

EXPRESSIONS = [
    # ── Row 0 ──────────────────────────────────────────────────────────────────
    (
        "NEUTRAL / DEFAULT",
        "flat",
        "default",
        {
            "arm_dy": 4, "arm_x_scale": 0.75, "leg_spread": 0.85,
            "body_tilt": 0, "body_squash": 1.0,
            "arm_l_dy": 4, "arm_r_dy": 4,
        },
        "half_open",
        BG_NEUTRAL,
        "← was: ANY STATE",
        "→ next: SEARCHING / GRUMPY"
    ),
    (
        "GRUMPY",
        "grumpy",
        "disgust",
        {
            "arm_dy": -8, "arm_x_scale": 1.1, "leg_spread": 1.1,
            "body_tilt": -8, "body_squash": 1.0,
            "arm_l_dy": -6, "arm_r_dy": -10,
        },
        "angry",
        BG_GRUMPY,
        "← was: NEUTRAL",
        "→ next: REFUSING"
    ),
    (
        "SEARCHING",
        "loading",
        "curious",
        {
            "arm_dy": -4, "arm_x_scale": 1.1, "leg_spread": 1.2,
            "body_tilt": -8, "body_squash": 1.0,
            "arm_l_dy": 4, "arm_r_dy": -18,
        },
        "wide",
        BG_SEARCH,
        "← was: NEUTRAL",
        "→ next: ALARMED / FOUND"
    ),
    # ── Row 1 ──────────────────────────────────────────────────────────────────
    (
        "ALARMED",
        "!",
        "fear",
        {
            "arm_dy": -16, "arm_x_scale": 1.5, "leg_spread": 1.6,
            "body_tilt": 0, "body_squash": 0.92,
            "arm_l_dy": -10, "arm_r_dy": -22,
        },
        "wide_scared",
        BG_ALARM,
        "← was: SEARCHING",
        "→ next: FLEEING / FROZEN"
    ),
    (
        "RELUCTANT JOY",
        "♥",
        "happy",
        {
            "arm_dy": 8, "arm_x_scale": 0.65, "leg_spread": 0.8,
            "body_tilt": 12, "body_squash": 1.0,
            "arm_l_dy": -2, "arm_r_dy": 12,
            "reluctant_joy": True,
        },
        "droopy",
        BG_RELJOY,
        "← was: GRUMPY",
        "→ next: DENYING IT"
    ),
    (
        "CONFUSED",
        "?",
        "confused",
        {
            "arm_dy": -6, "arm_x_scale": 1.0, "leg_spread": 1.1,
            "body_tilt": -18, "body_squash": 1.0,
            "arm_l_dy": -14, "arm_r_dy": 2,
        },
        "squint",
        BG_CONFUSE,
        "← was: ANY STATE",
        "→ next: SEARCHING"
    ),
    # ── Row 2 ──────────────────────────────────────────────────────────────────
    (
        "POWERED DOWN",
        "flat",
        "neutral",
        {
            "arm_dy": 18, "arm_x_scale": 0.7, "leg_spread": 0.6,
            "body_tilt": 0, "body_squash": 0.88,
            "arm_l_dy": 18, "arm_r_dy": 18,
        },
        "flat",
        BG_PWRDOWN,
        "← was: ANY STATE",
        "→ next: BOOTING UP"
    ),
    (
        "RESIGNED",
        "↓",
        "resigned",
        {
            "arm_dy": 14, "arm_x_scale": 0.50, "leg_spread": 0.70,
            "body_tilt": 14, "body_squash": 1.0,
            "arm_l_dy": 14, "arm_r_dy": 14,
        },
        "droopy_resigned",
        BG_RESIGNED,
        "← was: NEUTRAL / GRUMPY",
        "→ next: COMPLYING"
    ),
    (
        "STORM/CRACKED",
        "dead_zone",
        "storm",
        {
            "arm_dy": 10, "arm_x_scale": 0.55, "leg_spread": 0.72,
            "body_tilt": 18, "body_squash": 1.0,
            "arm_l_dy": 6, "arm_r_dy": 22,
            "storm_damage": True,
        },
        "cracked_storm",
        BG_STORM,
        "← was: RESIGNED",
        "→ next: DAMAGE STATE"
    ),
    # ── Row 3 ──────────────────────────────────────────────────────────────────
    (
        "UNGUARDED WARMTH",
        "heart_purple",   # cracked/left eye: heart in UV_PURPLE — "broken open"
        "warmth",         # emotion: barely-there upward arc
        {
            "arm_dy": -5, "arm_x_scale": 0.72, "leg_spread": 0.85,
            "body_tilt": -4, "body_squash": 1.0,
            "arm_l_dy": -5, "arm_r_dy": -5,
            "unguarded_warmth": True,   # triggers gold confetti + star right eye
        },
        "star_gold",      # right/organic eye: STAR at full SOFT_GOLD
        BG_WARMTH,
        "← was: RELUCTANT JOY / ANY STATE",
        "→ He has stopped fighting it."
    ),
    # Slots 10 and 11 are empty
]


# ── Pixel symbol rendering ──────────────────────────────────────────────────────

def draw_pixel_symbol(draw, cx, cy, size, symbol):
    """Draw a pixel-eye symbol."""
    PIXEL_CYAN = (0, 240, 255)
    PIXEL_MAG  = (255, 45, 107)
    OFF        = (20, 18, 28)

    # ── 7×7 dead-pixel glyph (Section 9B canonical) ──────────────────────────
    if symbol == "dead_zone":
        cell = max(2, size // 7)
        ox = cx - (7 * cell) // 2
        oy = cy - (7 * cell) // 2

        DEAD_PX      = (10, 10, 20)
        DIM_PX       = (0, 80, 100)
        ALIVE_PX     = (0, 180, 200)
        BRIGHT_PX    = (200, 255, 255)
        DEEP_CYAN_BG = (26, 58, 64)

        glyph = [
            [3, 3, 3, 3, 0, 0, 0],
            [3, 1, 3, 3, 0, 0, 0],
            [1, 3, 3, 0, 0, 2, 0],
            [3, 3, 0, 0, 2, 0, 0],
            [3, 0, 0, 3, 3, 0, 3],
            [0, 0, 3, 1, 3, 3, 3],
            [0, 3, 3, 3, 1, 3, 3],
        ]
        color_map = {0: DEAD_PX, 1: ALIVE_PX, 2: BRIGHT_PX, 3: DIM_PX}

        draw.rectangle([ox - 2, oy - 2,
                        ox + 7 * cell + 2, oy + 7 * cell + 2],
                       fill=DEEP_CYAN_BG, outline=LINE, width=2)

        for row in range(7):
            for col in range(7):
                v = glyph[row][col]
                px = ox + col * cell
                py = oy + row * cell
                draw.rectangle([px + 1, py + 1, px + cell - 1, py + cell - 1],
                               fill=color_map[v])

        crack_x1 = ox + int(4.5 * cell)
        crack_y1 = oy
        crack_x2 = ox + int(2.0 * cell)
        crack_y2 = oy + 7 * cell
        draw.line([(crack_x1, crack_y1), (crack_x2, crack_y2)], fill=LINE, width=2)
        return

    # ── Standard 5×5 symbols ──────────────────────────────────────────────────
    cell = size // 5
    if cell < 2:
        cell = 2
    ox = cx - (5 * cell) // 2
    oy = cy - (5 * cell) // 2

    # Pixel color for this symbol
    if symbol == "star_gold":
        # Star glyph, SOFT_GOLD (#E8C95A) — per Alex Chen spec
        # 5×5 grid:
        # 0 1 0 1 0
        # 1 1 1 1 1
        # 0 1 1 1 0
        # 1 1 1 1 1
        # 0 1 0 1 0
        sym_color = SOFT_GOLD
        grid = [
            [0, 1, 0, 1, 0],
            [1, 1, 1, 1, 1],
            [0, 1, 1, 1, 0],
            [1, 1, 1, 1, 1],
            [0, 1, 0, 1, 0],
        ]
    elif symbol == "heart_purple":
        # Heart glyph, UV_PURPLE (#7B2FBE) — per Alex Chen spec
        # 5×5 grid:
        # 0 1 0 1 0
        # 1 1 1 1 1
        # 0 1 1 1 0
        # 0 0 1 0 0
        # 0 0 0 0 0
        sym_color = UV_PURPLE
        grid = [
            [0, 1, 0, 1, 0],
            [1, 1, 1, 1, 1],
            [0, 1, 1, 1, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0],
        ]
    else:
        sym_color = PIXEL_CYAN
        grids = {
            "!": [
                [0, 0, 1, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0],
            ],
            "?": [
                [0, 1, 1, 1, 0],
                [0, 0, 0, 1, 0],
                [0, 0, 1, 1, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0],
            ],
            "♥": [
                [0, 1, 0, 1, 0],
                [1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1],
                [0, 1, 1, 1, 0],
                [0, 0, 1, 0, 0],
            ],
            "loading": [
                [1, 0, 1, 0, 1],
                [0, 0, 0, 0, 0],
                [1, 0, 0, 0, 1],
                [0, 0, 0, 0, 0],
                [1, 0, 1, 0, 1],
            ],
            "flat": [
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [1, 1, 1, 1, 1],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
            ],
            "grumpy": [
                [0, 0, 0, 0, 0],
                [1, 0, 0, 0, 1],
                [1, 1, 1, 1, 1],
                [1, 0, 0, 0, 1],
                [0, 0, 0, 0, 0],
            ],
            "↓": [
                [0, 0, 1, 0, 0],
                [0, 0, 1, 0, 0],
                [1, 1, 1, 1, 1],
                [0, 1, 1, 1, 0],
                [0, 0, 1, 0, 0],
            ],
            "normal": None,
        }
        grid = grids.get(symbol)
        if grid is None:
            draw.ellipse([cx - cell * 2, cy - cell * 2, cx + cell * 2, cy + cell * 2], fill=EYE_W)
            draw.ellipse([cx - cell, cy - cell, cx + cell, cy + cell], fill=(60, 38, 20))
            draw.ellipse([cx - cell // 2, cy - cell // 2,
                          cx + cell // 2, cy + cell // 2], fill=LINE)
            draw.ellipse([cx + cell // 2, cy - cell, cx + cell * 2 - 2, cy - cell // 2],
                         fill=(255, 252, 245))
            return

    # Draw background bezel
    bg_color = (255, 255, 255) if sym_color != SOFT_GOLD else (40, 32, 20)  # dark bezel for gold
    draw.rectangle([ox - 2, oy - 2, ox + 5 * cell + 2, oy + 5 * cell + 2],
                   fill=bg_color, outline=LINE, width=1)

    for row in range(5):
        for col in range(5):
            v = grid[row][col]
            px = ox + col * cell
            py = oy + row * cell
            if sym_color == PIXEL_CYAN:
                color = PIXEL_CYAN if v == 1 else (20, 18, 28)
            else:
                color = sym_color if v == 1 else (OFF[0] if sym_color == PIXEL_CYAN else (20, 16, 32))
                if v == 0:
                    color = (10, 8, 20)  # dark background for colored symbols
            draw.rectangle([px + 1, py + 1, px + cell - 1, py + cell - 1], fill=color)


# ── Right eye renderer ─────────────────────────────────────────────────────────

def draw_right_eye(draw, cx, cy, size, style):
    """Draw Byte's right (organic) eye or STAR symbol for UNGUARDED WARMTH."""
    cell = size // 5
    if cell < 2:
        cell = 2

    if style == "star_gold":
        # UNGUARDED WARMTH: right eye shows STAR glyph at full SOFT_GOLD.
        # This uses the pixel symbol system on the organic eye too.
        # Render with warm dark background (he's looking toward warmth).
        draw_pixel_symbol(draw, cx, cy, size, "star_gold")
        return

    if style == "flat":
        draw_pixel_symbol(draw, cx, cy, size, "flat")
        return

    ew = cell * 2
    eh = cell * 2

    if style == "half_open":
        eye_h = int(eh * 0.6)
        draw.ellipse([cx - ew, cy - eye_h, cx + ew, cy + eye_h],
                     fill=EYE_W, outline=LINE, width=1)
        iris_r = int(cell * 1.5)
        draw.ellipse([cx - iris_r, cy - iris_r, cx + iris_r, cy + iris_r], fill=(45, 28, 14))
        draw.ellipse([cx - cell // 2 - 1, cy - cell // 2 - 1,
                      cx + cell // 2 + 1, cy + cell // 2 + 1], fill=LINE)
        draw.ellipse([cx + cell // 2, cy - iris_r + 2, cx + iris_r - 2, cy - cell // 2],
                     fill=(200, 195, 185))
        draw.arc([cx - ew, cy - eye_h, cx + ew, cy + eye_h],
                 start=200, end=340, fill=LINE, width=3)

    elif style == "wide":
        draw.ellipse([cx - ew, cy - eh, cx + ew, cy + eh], fill=EYE_W)
        draw.ellipse([cx - cell + 2, cy - cell + 2, cx + cell + 2, cy + cell + 2], fill=(60, 38, 20))
        draw.ellipse([cx - cell // 2 + 2, cy - cell // 2 + 2,
                      cx + cell // 2 + 2, cy + cell // 2 + 2], fill=LINE)
        draw.ellipse([cx + cell, cy - eh + 2, cx + ew - 2, cy - cell], fill=(255, 252, 245))

    elif style == "wide_scared":
        draw.ellipse([cx - ew - 2, cy - eh - 3, cx + ew + 2, cy + eh + 3],
                     fill=EYE_W, outline=LINE, width=2)
        draw.ellipse([cx - cell + 1, cy - cell + 1, cx + cell - 1, cy + cell - 1], fill=(60, 38, 20))
        draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=LINE)
        draw.ellipse([cx + cell - 2, cy - eh + 2, cx + ew - 2, cy - cell + 2], fill=(255, 252, 245))
        draw.arc([cx - ew - 2, cy - eh - 3, cx + ew + 2, cy + eh + 3],
                 start=200, end=340, fill=(220, 220, 230), width=2)

    elif style == "angry":
        draw.ellipse([cx - ew, cy - eh + 4, cx + ew, cy + eh], fill=EYE_W)
        draw.ellipse([cx - cell - 2, cy, cx + cell - 2, cy + cell * 2 - 2], fill=(60, 38, 20))
        draw.ellipse([cx - 4 - 2, cy + 4, cx + 4 - 2, cy + 4 + 8], fill=LINE)
        draw.ellipse([cx + 2, cy + 2, cx + cell + 2, cy + cell - 2], fill=(255, 252, 245))
        draw.arc([cx - ew, cy - eh + 4, cx + ew, cy + eh], start=195, end=345, fill=LINE, width=5)
        draw.line([(cx - ew, cy - eh // 2 + 4), (cx + ew, cy - eh // 2)], fill=LINE, width=3)

    elif style == "droopy":
        draw.ellipse([cx - ew, cy - eh + 6, cx + ew, cy + eh + 2], fill=EYE_W)
        draw.ellipse([cx - cell + 1, cy - cell + 4, cx + cell + 1, cy + cell + 4], fill=(60, 38, 20))
        draw.ellipse([cx - 4 + 1, cy + 1, cx + 4 + 1, cy + 8], fill=LINE)
        draw.ellipse([cx + cell, cy - 3, cx + ew - 2, cy + 3], fill=(255, 252, 245))
        draw.arc([cx - ew, cy - eh + 6, cx + ew, cy + eh + 2], start=195, end=345, fill=LINE, width=6)
        draw.line([(cx - ew, cy + 5), (cx - ew + 4, cy + 2)], fill=LINE, width=2)

    elif style == "droopy_resigned":
        eye_h = int(eh * 0.45)
        draw.ellipse([cx - ew, cy - eye_h + 6, cx + ew, cy + eye_h + 6], fill=EYE_W)
        draw.ellipse([cx - cell + 1, cy + 4, cx + cell + 1, cy + cell * 2 + 4], fill=(60, 38, 20))
        draw.ellipse([cx - 4 + 1, cy + 8, cx + 4 + 1, cy + 16], fill=LINE)
        draw.ellipse([cx + cell - 2, cy + 4, cx + ew - 5, cy + cell], fill=(165, 160, 150))
        draw.arc([cx - ew, cy - eye_h + 6, cx + ew, cy + eye_h + 6],
                 start=195, end=345, fill=LINE, width=8)
        droop_pts = []
        for i in range(11):
            t = i / 10.0
            dx = int(-ew + t * 2 * ew)
            sag = int(7 * 4 * t * (1 - t))
            dy = int(eye_h + 6 + sag)
            droop_pts.append((cx + dx, cy + dy))
        if len(droop_pts) > 1:
            draw.line(droop_pts, fill=LINE, width=3)

    elif style == "cracked_storm":
        eye_h = int(eh * 0.50)
        draw.ellipse([cx - ew, cy - eye_h + 4, cx + ew, cy + eye_h + 4], fill=EYE_W)
        draw.ellipse([cx - cell + 1, cy + 2, cx + cell + 1, cy + cell * 2 + 2],
                     fill=(35, 22, 10))
        draw.ellipse([cx - 4 + 1, cy + 6, cx + 4 + 1, cy + 14], fill=LINE)
        draw.ellipse([cx + cell - 2, cy + 2, cx + ew - 6, cy + cell - 2],
                     fill=(130, 128, 120))
        draw.arc([cx - ew, cy - eye_h + 4, cx + ew, cy + eye_h + 4],
                 start=195, end=345, fill=LINE, width=8)
        droop_pts = []
        for i in range(11):
            t = i / 10.0
            dx = int(-ew + t * 2 * ew)
            sag = int(8 * 4 * t * (1 - t))
            dy = int(eye_h + 4 + sag)
            droop_pts.append((cx + dx, cy + dy))
        if len(droop_pts) > 1:
            draw.line(droop_pts, fill=LINE, width=3)

    elif style == "squint":
        draw.ellipse([cx - ew, cy - eh + 4, cx + ew, cy + eh + 2], fill=EYE_W)
        draw.ellipse([cx - cell, cy - cell - 2, cx + cell, cy + cell - 2], fill=(60, 38, 20))
        draw.ellipse([cx - 4, cy - 8, cx + 4, cy], fill=LINE)
        draw.ellipse([cx + cell - 2, cy - eh + 4, cx + ew - 4, cy - cell], fill=(255, 252, 245))
        draw.line([(cx - ew, cy - eh // 2 + 4), (cx + ew, cy - eh // 2 + 2)], fill=LINE, width=3)

    else:
        draw.ellipse([cx - ew, cy - eh, cx + ew, cy + eh], fill=EYE_W)
        draw.ellipse([cx - cell, cy - cell, cx + cell, cy + cell], fill=(60, 38, 20))
        draw.ellipse([cx - cell // 2, cy - cell // 2, cx + cell // 2, cy + cell // 2], fill=LINE)
        draw.ellipse([cx + cell // 2, cy - cell, cx + cell * 2 - 2, cy - cell // 2],
                     fill=(255, 252, 245))


# ── Storm background texture ───────────────────────────────────────────────────

def draw_storm_bg_texture(draw, ppx, ppy, panel_w, panel_h, panel_bg):
    trace_color = (0, 40, 50)
    uv_color    = (40, 20, 60)
    for y_off in [40, 90, 140, 190, 240, 290]:
        y = ppy + y_off
        for x_start in [ppx + 10, ppx + 80, ppx + 140]:
            seg_len = 30 + (x_start % 40)
            draw.line([(x_start, y), (x_start + seg_len, y)], fill=trace_color, width=1)
        jx = ppx + 60 + (y_off % 50)
        draw.line([(jx, y), (jx, y + 18)], fill=trace_color, width=1)
    for i in range(3):
        x1 = ppx + i * 30
        y1 = ppy + 10
        x2 = ppx + panel_w
        y2 = ppy + panel_h // 2 + i * 20
        draw.line([(x1, y1), (x2, y2)], fill=uv_color, width=1)
    for (sx, sy) in [(ppx+20, ppy+50), (ppx+190, ppy+80), (ppx+55, ppy+170),
                     (ppx+210, ppy+220), (ppx+30, ppy+260)]:
        draw.rectangle([sx, sy, sx + 2, sy + 2], fill=(0, 100, 120))


# ── Warmth background atmosphere ──────────────────────────────────────────────

def draw_warmth_bg(draw, ppx, ppy, panel_w, panel_h):
    """Subtle warm glow at the bottom of the warmth panel — his world touching hers."""
    for i in range(8):
        alpha_ratio = (i + 1) / 8
        r = int(232 * alpha_ratio + 240 * (1 - alpha_ratio))
        g = int(201 * alpha_ratio + 224 * (1 - alpha_ratio))
        b = int(90 * alpha_ratio + 198 * (1 - alpha_ratio))
        y = ppy + int(panel_h * (0.75 + i * 0.03))
        if y < ppy + panel_h:
            draw.rectangle([ppx, y, ppx + panel_w, ppy + panel_h], fill=(r, g, b))


# ── Main draw function ─────────────────────────────────────────────────────────

def draw_byte(draw, cx, cy, size, expression_name, cracked_symbol, emotion,
              body_data, right_eye_style, img=None):
    """Draw Byte with per-expression body variation."""
    s = size

    arm_dy          = body_data.get("arm_dy", 0)
    arm_x_scale     = body_data.get("arm_x_scale", 1.0)
    leg_spread      = body_data.get("leg_spread", 1.0)
    body_tilt       = body_data.get("body_tilt", 0)
    body_squash     = body_data.get("body_squash", 1.0)
    arm_l_dy        = body_data.get("arm_l_dy", arm_dy)
    arm_r_dy        = body_data.get("arm_r_dy", arm_dy)
    storm_damage    = body_data.get("storm_damage", False)
    unguarded_warmth = body_data.get("unguarded_warmth", False)

    body_rx = s // 2
    body_ry = int(s * 0.55 * body_squash)
    bcx = cx + body_tilt
    bcy = cy

    # Main oval — GL-01b body fill ALWAYS
    draw.ellipse([bcx - body_rx, bcy - body_ry,
                  bcx + body_rx, bcy + body_ry],
                 fill=BYTE_TEAL, outline=LINE, width=3)

    # Right-side shadow
    shadow_pts = [
        (bcx,                bcy - body_ry),
        (bcx + body_rx,      bcy - body_ry + 4),
        (bcx + body_rx,      bcy + body_ry - 4),
        (bcx,                bcy + body_ry),
        (bcx + body_rx // 2, bcy + body_ry),
        (bcx + body_rx,      bcy + body_ry // 2),
        (bcx + body_rx,      bcy),
    ]
    draw.polygon(shadow_pts, fill=BYTE_SH)

    # Highlight arc
    draw.arc([bcx - body_rx, bcy - body_ry, bcx + body_rx, bcy + body_ry],
             start=200, end=310, fill=BYTE_HL, width=3)

    # Magenta scar markings
    crack_x = bcx - s // 4
    draw.line([(crack_x, bcy - body_ry // 2),
               (crack_x + s // 8, bcy - body_ry // 6)], fill=SCAR_MAG, width=2)
    draw.line([(crack_x + s // 8, bcy - body_ry // 6),
               (crack_x - s // 10, bcy + body_ry // 6)], fill=SCAR_MAG, width=2)

    # Damage notch
    notch_pts = [
        (bcx + body_rx - 4,         bcy - body_ry // 4),
        (bcx + body_rx + s // 12,   bcy - body_ry // 6),
        (bcx + body_rx - 4,         bcy + body_ry // 6),
    ]
    draw.polygon(notch_pts, fill=BG, outline=LINE, width=1)

    # Storm damage marks
    if storm_damage:
        sx = bcx + s // 6
        sy = bcy - body_ry + 10
        draw.line([(sx, sy), (sx + 8, sy + 12)], fill=HOT_MAG, width=2)
        draw.line([(sx + 8, sy + 12), (sx + 4, sy + 18)], fill=HOT_MAG, width=2)
        draw.line([(bcx + 10, bcy - body_ry // 3),
                   (bcx + 22, bcy + body_ry // 4)], fill=HOT_MAG, width=1)

    # Unguarded warmth: soft gold glow on right side of body
    if unguarded_warmth:
        # Very faint gold highlight — leaning toward warmth
        draw.arc([bcx - body_rx + 8, bcy - body_ry + 4, bcx + body_rx - 2, bcy + body_ry - 4],
                 start=320, end=90, fill=SOFT_GOLD, width=2)

    # Eyes
    eye_y    = bcy - body_ry // 5
    eye_size = max(14, int(body_ry * 0.46))

    # Left eye (pixel/cracked display) — viewer's left
    lx             = bcx - s // 5
    crack_frame_sz = eye_size + 4

    if storm_damage:
        fr = crack_frame_sz // 2
        chip_pts = [
            (lx - fr,         eye_y - fr),
            (lx + fr - 2,     eye_y - fr),
            (lx + fr,         eye_y - fr + 3),
            (lx + fr + 2,     eye_y - fr + 8),
            (lx + fr,         eye_y + fr),
            (lx - fr,         eye_y + fr),
        ]
        draw.polygon(chip_pts, fill=(26, 58, 64), outline=LINE, width=2)
        draw.line([(lx + fr - 2, eye_y - fr), (lx - fr + 3, eye_y + fr)],
                  fill=HOT_MAG, width=2)
    else:
        draw.rectangle([lx - crack_frame_sz // 2, eye_y - crack_frame_sz // 2,
                        lx + crack_frame_sz // 2, eye_y + crack_frame_sz // 2],
                       fill=(255, 255, 255), outline=LINE, width=2)
        draw.line([(lx + 2,  eye_y - crack_frame_sz // 2),
                   (lx - 4,  eye_y + crack_frame_sz // 2)], fill=LINE, width=2)

    draw_pixel_symbol(draw, lx, eye_y, eye_size, cracked_symbol)

    # Right eye
    rx = bcx + s // 5
    draw_right_eye(draw, rx, eye_y, eye_size, right_eye_style)

    # Mouth
    mouth_y = bcy + body_ry // 3
    mw = s // 3
    if emotion == "disgust":
        draw.arc([bcx - mw, mouth_y - 8, bcx + mw, mouth_y + 16],
                 start=200, end=340, fill=LINE, width=3)
    elif emotion == "curious":
        draw.ellipse([bcx - 8, mouth_y - 8, bcx + 8, mouth_y + 4], outline=LINE, width=2)
    elif emotion == "fear":
        draw.arc([bcx - mw + 4, mouth_y - 10, bcx + mw - 4, mouth_y + 22],
                 start=10, end=170, fill=LINE, width=3)
        draw.chord([bcx - mw + 8, mouth_y - 8, bcx + mw - 8, mouth_y + 18],
                   start=10, end=170, fill=(180, 160, 150))
    elif emotion == "happy":
        draw.arc([bcx - mw // 2, mouth_y - 6, bcx + mw // 2, mouth_y + 12],
                 start=20, end=160, fill=LINE, width=3)
    elif emotion == "confused":
        for i in range(4):
            x1 = bcx - mw + i * (mw // 2)
            y1 = mouth_y + (4 if i % 2 == 0 else -4)
            x2 = x1 + mw // 2
            y2 = mouth_y + (-4 if i % 2 == 0 else 4)
            draw.line([(x1, y1), (x2, y2)], fill=LINE, width=2)
    elif emotion == "neutral":
        pass
    elif emotion == "default":
        mid_x1 = bcx - mw // 2
        mid_x2 = bcx + mw // 2
        draw.line([(mid_x1, mouth_y), (mid_x2, mouth_y)], fill=LINE, width=2)
        draw.line([(mid_x1, mouth_y), (mid_x1 - 6, mouth_y + 4)], fill=LINE, width=2)
        draw.line([(mid_x2, mouth_y), (mid_x2 + 6, mouth_y + 4)], fill=LINE, width=2)
    elif emotion == "resigned":
        mid_x1 = bcx - mw // 3
        mid_x2 = bcx + mw // 3
        draw.line([(mid_x1, mouth_y), (mid_x2, mouth_y)], fill=LINE, width=2)
    elif emotion == "storm":
        mid_x1 = bcx - mw // 4
        mid_x2 = bcx + mw // 4
        draw.line([(mid_x1, mouth_y), (mid_x2, mouth_y)], fill=LINE, width=2)
    elif emotion == "warmth":
        # UNGUARDED WARMTH: very slight upward arc — almost not there.
        # Much more subtle than "happy" — barely perceptible lift.
        # arc from 25° to 155° (shallow), very small box (short arc)
        mw_s = mw // 3   # very narrow arc
        arc_h = 5        # very shallow lift
        draw.arc([bcx - mw_s, mouth_y - arc_h, bcx + mw_s, mouth_y + arc_h + 3],
                 start=25, end=155, fill=LINE, width=2)
    else:
        draw.line([(bcx - mw // 2, mouth_y), (bcx + mw // 2, mouth_y)], fill=LINE, width=2)

    # Antenna
    ant_base_x = bcx - s // 8
    ant_base_y = bcy - body_ry
    if storm_damage:
        ant_mid_x  = ant_base_x + 6
        ant_mid_y  = ant_base_y - s // 5
        ant_tip_x  = ant_mid_x - 8
        ant_tip_y  = ant_mid_y - s // 8
        draw.line([(ant_base_x, ant_base_y), (ant_mid_x, ant_mid_y)], fill=LINE, width=2)
        draw.line([(ant_mid_x, ant_mid_y), (ant_tip_x, ant_tip_y)], fill=LINE, width=2)
        draw.ellipse([ant_tip_x - 3, ant_tip_y - 3,
                      ant_tip_x + 3, ant_tip_y + 3], fill=HOT_MAG)
    elif unguarded_warmth:
        # Antenna tip slightly warmer — small soft gold sphere
        ant_tip_x = ant_base_x - s // 10
        ant_tip_y = ant_base_y - s // 3
        draw.line([(ant_base_x, ant_base_y), (ant_tip_x, ant_tip_y)], fill=LINE, width=2)
        draw.ellipse([ant_tip_x - 4, ant_tip_y - 4,
                      ant_tip_x + 4, ant_tip_y + 4], fill=SOFT_GOLD)
    else:
        ant_tip_x = ant_base_x - s // 10
        ant_tip_y = ant_base_y - s // 3
        draw.line([(ant_base_x, ant_base_y), (ant_tip_x, ant_tip_y)], fill=LINE, width=2)
        draw.ellipse([ant_tip_x - 4, ant_tip_y - 4,
                      ant_tip_x + 4, ant_tip_y + 4], fill=BYTE_HL)

    # Limbs
    lw         = s // 6
    lh         = s // 5
    arm_extend = int(lw * arm_x_scale)
    arm_base_y = bcy - body_ry // 5

    left_arm_y = arm_base_y + arm_l_dy
    draw.rectangle([bcx - body_rx - arm_extend, left_arm_y,
                    bcx - body_rx,              left_arm_y + lh],
                   fill=BYTE_TEAL, outline=LINE, width=2)

    right_arm_y = arm_base_y + arm_r_dy
    draw.rectangle([bcx + body_rx,              right_arm_y,
                    bcx + body_rx + arm_extend, right_arm_y + lh],
                   fill=BYTE_TEAL, outline=LINE, width=2)

    leg_offset = int(s // 4 * leg_spread)
    # UNGUARDED WARMTH: left leg 2px forward
    leg_l_offset = leg_offset + (2 if unguarded_warmth else 0)
    leg_h        = lh
    leg_w        = int(lw * 0.9)
    draw.rectangle([bcx - leg_l_offset - leg_w // 2, bcy + body_ry,
                    bcx - leg_l_offset + leg_w // 2, bcy + body_ry + leg_h],
                   fill=BYTE_TEAL, outline=LINE, width=2)
    draw.rectangle([bcx + leg_offset - leg_w // 2, bcy + body_ry,
                    bcx + leg_offset + leg_w // 2, bcy + body_ry + leg_h],
                   fill=BYTE_TEAL, outline=LINE, width=2)

    # Hover particles
    if unguarded_warmth:
        # ONLY expression with gold confetti — 3 small SOFT_GOLD squares
        confetti_positions = [
            (bcx - 18, bcy + body_ry + leg_h + 5),
            (bcx + 6,  bcy + body_ry + leg_h + 9),
            (bcx + 24, bcy + body_ry + leg_h + 3),
        ]
        for (ppx, ppy) in confetti_positions:
            draw.rectangle([ppx, ppy, ppx + 10, ppy + 10], fill=SOFT_GOLD)
    else:
        for (ppx, ppy, ppc) in [
            (bcx - 20, bcy + body_ry + leg_h + 5,  BYTE_HL),
            (bcx + 5,  bcy + body_ry + leg_h + 8,  SCAR_MAG),
            (bcx + 25, bcy + body_ry + leg_h + 3,  BYTE_HL),
            (bcx - 35, bcy + body_ry + leg_h + 10, (0, 200, 180)),
        ]:
            draw.rectangle([ppx, ppy, ppx + 10, ppy + 10], fill=ppc)


# ── Sheet generator ─────────────────────────────────────────────────────────────

def generate_byte_expression_sheet(output_path):
    """Render 4×3 expression grid for Byte. 10 expressions + 2 empty."""
    total_w = COLS * (PANEL_W + PAD) + PAD
    total_h = HEADER + ROWS * (PANEL_H + PAD) + PAD

    img  = Image.new('RGB', (total_w, total_h), BG)
    draw = ImageDraw.Draw(img)

    try:
        font_title = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
        font       = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 15)
        font_sm    = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11)
    except Exception:
        font_title = font = font_sm = ImageFont.load_default()

    draw.text((PAD, 12),
              "BYTE — Expression Sheet — Luma & the Glitchkin  |  v005  "
              "(10 expressions: +UNGUARDED WARMTH)",
              fill=(0, 240, 255), font=font_title)

    for i, (name, symbol, emotion, body_data, right_eye_style, panel_bg, prev_st, next_st) in \
            enumerate(EXPRESSIONS):

        col = i % COLS
        row = i // COLS
        ppx = PAD + col * (PANEL_W + PAD)
        ppy = HEADER + row * (PANEL_H + PAD)

        # Panel background
        draw.rectangle([ppx, ppy, ppx + PANEL_W, ppy + PANEL_H], fill=panel_bg)
        draw.rectangle([ppx, ppy, ppx + PANEL_W, ppy + PANEL_H], outline=(40, 35, 55), width=1)

        # Special panel backgrounds
        if emotion == "storm":
            draw_storm_bg_texture(draw, ppx, ppy, PANEL_W, PANEL_H, panel_bg)
            draw = ImageDraw.Draw(img)

        if name == "UNGUARDED WARMTH":
            draw_warmth_bg(draw, ppx, ppy, PANEL_W, PANEL_H)
            draw = ImageDraw.Draw(img)

        # Draw Byte
        byte_size = 88
        bcx_panel = ppx + PANEL_W // 2
        bcy_panel = ppy + PANEL_H // 2 - 20
        draw_byte(draw, bcx_panel, bcy_panel, byte_size,
                  name, symbol, emotion, body_data, right_eye_style, img)
        draw = ImageDraw.Draw(img)  # refresh after paste

        # Tag for new expressions
        if "STORM" in name:
            draw.text((ppx + PANEL_W - 56, ppy + 4), "[v003]",
                      fill=(255, 45, 120), font=font_sm)
        if "WARMTH" in name:
            draw.text((ppx + PANEL_W - 56, ppy + 4), "[NEW v005]",
                      fill=SOFT_GOLD, font=font_sm)

        # Label bar
        bar_h = 58
        draw.rectangle([ppx, ppy + PANEL_H - bar_h, ppx + PANEL_W, ppy + PANEL_H],
                       fill=(10, 8, 18))
        label_color = SOFT_GOLD if "WARMTH" in name else (0, 240, 255)
        draw.text((ppx + 6, ppy + PANEL_H - bar_h + 4),  name,    fill=label_color, font=font)
        draw.text((ppx + 6, ppy + PANEL_H - bar_h + 22), prev_st, fill=(120, 110, 140), font=font_sm)
        draw.text((ppx + 6, ppy + PANEL_H - bar_h + 36), next_st, fill=(120, 110, 140), font=font_sm)

    # Respect ≤1280px rule
    img.thumbnail((1280, 1280), Image.LANCZOS)

    img.save(output_path)
    w, h = img.size
    print(f"Saved: {output_path}  ({w}×{h}px)")


if __name__ == '__main__':
    out_dir = "/home/wipkat/team/output/characters/main"
    os.makedirs(out_dir, exist_ok=True)
    generate_byte_expression_sheet(
        os.path.join(out_dir, "LTG_CHAR_byte_expression_sheet_v005.png")
    )
    print("v005 additions:")
    print("  + UNGUARDED WARMTH (10th expression)")
    print("  + star_gold pixel symbol (SOFT_GOLD, full brightness)")
    print("  + heart_purple pixel symbol (UV_PURPLE)")
    print("  + warmth mouth style (barely-there upward arc)")
    print("  + SOFT_GOLD confetti (only this expression uses gold)")
    print("  + warmth atmosphere background layer")
    print("  + gold antenna tip")
