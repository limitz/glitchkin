#!/usr/bin/env python3
"""
LTG_CHAR_byte_expression_sheet_v004.py
Byte Expression Sheet Generator — "Luma & the Glitchkin"

v004 Cycle 22 (Maya Santos): Critique 10 fixes — Dmitri Volkov + Victoria Ashford.
  Fix 1a — STORM/CRACKED glyph corrected per Section 9B canonical spec:
    - 7x7 grid re-implemented row-by-row (CRACK is overlay only, not a pixel state).
    - DIM_PX color corrected: (18,52,60) #123C3C -> (0,80,100) #005064.
    - Crack line INSIDE dead_zone changed to void black LINE (#0A0A14), not HOT_MAG.
      HOT_MAG crack stays on body/frame EXTERIOR only per spec.
  Fix 1b — STORM arm asymmetry: arm_l_dy=6, arm_r_dy=22 (20+ unit diff).
    Suggests physical imbalance — STORM = damaged-asymmetric at thumbnail.
    RESIGNED arms remain symmetric (14,14).
  Fix 1c — RELUCTANT JOY: stronger "fighting against joy" signal.
    body_tilt 10->12, arm_l_dy changes to -2 (one arm resisting upward push).
  Fix 1d — POWERED DOWN squash: 0.88 -> 0.75, arm_dy maxed to 18.
# TODO: update import to LTG_TOOL_render_lib_v001 after Kai's rename

v003 Cycle 21 (Maya Santos): Added STORM/CRACKED variant panel.
  - 9th expression added: STORM/CRACKED — damage state extending RESIGNED.
  - Layout upgraded: 4×2 → 3×3 grid (9 panels total).
  - STORM/CRACKED spec:
      Right eye: 'cracked_storm' — 7×7 dead-pixel glyph per byte.md Section 9B.
                 Upper-right dead zone (void black pixels), Hot Magenta crack line diagonally.
                 Left eye (pixel display): dead-pixel glyph symbol (dead zone, no active symbol).
      Left eye (organic, viewer's right): RESIGNED droopy — 50% aperture, downcast pupil, flat HL.
      Mouth: flat/resigned, no energy.
      Body: storm posture — slightly more angular lean (+18 tilt), antenna bent (storm damage),
            body axis tilted further than RESIGNED.
      Background: stormy dark void with circuit trace texture + UV flash hint.
  - Scar magenta is #FF2D78 (Hot Magenta per byte.md Section 9B spec).
  - Byte body fill GL-01b #00D4E8 (RGB 0,212,232) — ALWAYS.
  - 3-tier line weight: silhouette 3-4px, interior 2px, detail 1px.
  - After img.paste(), refresh draw = ImageDraw.Draw(img).

v002 Cycle 16 color fixes (Sam Kowalski — Critique C8 / Naomi Bridges violations):
  1. BYTE_SH corrected: #0090B0 → #00A8C0 (GL-01a Deep Cyan).
  2. BG_ALARM corrected: warm cocoa → cold danger blue (18,28,44).
  3. Pixel faceplate scales with body_ry (not fixed s//4).

v002 Cycle 16 prev fix (Maya Santos): RESIGNED right eye 'droopy_resigned' reworked.
v002: Added RESIGNED expression (Cycle 15).
v001: 4×2 grid, 7 expressions.
"""
from PIL import Image, ImageDraw, ImageFont
import math

BYTE_TEAL  = (0, 212, 232)     # GL-01b #00D4E8 — body fill (ALWAYS)
BYTE_HL    = (0, 240, 255)     # GL-01  #00F0FF — highlights/circuit traces only
BYTE_SH    = (0, 168, 192)     # GL-01a #00A8C0 — Deep Cyan shadow companion
HOT_MAG    = (255, 45, 120)    # #FF2D78 — Hot Magenta crack line (Section 9B spec)
SCAR_MAG   = (255, 45, 107)    # #FF2D6B — body scar markings (body surface)
LINE       = (10, 10, 20)      # #0A0A14 void black
EYE_W      = (240, 240, 245)
BG         = (20, 18, 28)
VOID_BLACK = (10, 10, 20)      # #0A0A14

# Panel backgrounds — per-expression emotional read at panel scale
BG_NEUTRAL  = (28, 34, 42)
BG_GRUMPY   = (38, 20, 28)
BG_SEARCH   = (22, 30, 44)
BG_ALARM    = (18, 28, 44)
BG_RELJOY   = (22, 34, 32)
BG_CONFUSE  = (30, 24, 42)
BG_PWRDOWN  = (14, 12, 18)
BG_RESIGNED = (24, 26, 34)
BG_STORM    = (12, 10, 22)    # near-void storm dark, deeper than POWERED DOWN

EXPRESSIONS = [
    # ── NEUTRAL / DEFAULT-GRUMPY ─────────────────────────────────────────────
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
    # ── GRUMPY ──────────────────────────────────────────────────────────────
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
    # ── SEARCHING ───────────────────────────────────────────────────────────
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
    # ── ALARMED ─────────────────────────────────────────────────────────────
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
    # ── RELUCTANT JOY v004 FIX: stronger "fighting against joy" signal ─────────
    # arm_l_dy=-2 (one arm pushing UP = resisting joy impulse), arm_r_dy=12 (other hanging).
    # body_tilt=12 (was 10). Asymmetric arm differentiates from MILD DISCOMFORT.
    (
        "RELUCTANT JOY",
        "♥",
        "happy",
        {
            "arm_dy": 8, "arm_x_scale": 0.65, "leg_spread": 0.8,
            "body_tilt": 12, "body_squash": 1.0,
            "arm_l_dy": -2, "arm_r_dy": 12,         # v004: asymmetric — one arm up/resisting
            "reluctant_joy": True,                    # flag for raised antenna hint
        },
        "droopy",
        BG_RELJOY,
        "← was: GRUMPY",
        "→ next: DENYING IT"
    ),
    # ── CONFUSED ────────────────────────────────────────────────────────────
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
    # ── POWERED DOWN ────────────────────────────────────────────────────────
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
    # ── RESIGNED ────────────────────────────────────────────────────────────
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
    # ── STORM/CRACKED (NEW Cycle 21) ─────────────────────────────────────────
    # Section 9B canonical spec: 7×7 dead-pixel glyph, upper-right dead zone,
    # Hot Magenta crack line, storm posture (extended RESIGNED + damage).
    # Right eye (organic, viewer's right): RESIGNED droopy 50% aperture, downcast pupil.
    # Left eye (pixel display, viewer's left = CRACKED): dead_zone glyph.
    # Body: storm lean body_tilt=+18, antenna bent, arms slightly wider than RESIGNED.
    # BG: deep void storm with circuit trace hints.
    # ── STORM/CRACKED v004 FIX: arm asymmetry 20+ units — reads as damaged-asymmetric
    # at thumbnail vs RESIGNED (symmetric arms). Fix per Dmitri Volkov critique C10.
    (
        "STORM/CRACKED",
        "dead_zone",    # left/pixel eye: 7x7 dead-pixel glyph per Section 9B
        "storm",        # emotion tag — drives storm mouth (flat, no energy)
        {
            "arm_dy": 10, "arm_x_scale": 0.55, "leg_spread": 0.72,
            "body_tilt": 18, "body_squash": 1.0,   # more extreme lean than RESIGNED
            "arm_l_dy": 6, "arm_r_dy": 22,          # v004: 20+ unit asymmetry (was 12,10)
            "storm_damage": True,                    # triggers antenna bend + angular lean
        },
        "cracked_storm",   # right eye: cracked storm state (Section 9B)
        BG_STORM,
        "← was: RESIGNED",
        "→ next: DAMAGE STATE"
    ),
]

# ── Layout ─────────────────────────────────────────────────────────────────────
PANEL_W = 240
PANEL_H = 320
COLS    = 3
ROWS    = 3
PAD     = 16
HEADER  = 50


def draw_pixel_symbol(draw, cx, cy, size, symbol):
    """Draw a pixel-eye symbol. Supports 5×5 standard symbols and 7×7 dead_zone glyph."""
    PIXEL_CYAN = (0, 240, 255)
    PIXEL_MAG  = (255, 45, 107)
    OFF        = (20, 18, 28)

    # ── 7×7 dead-pixel glyph (Section 9B canonical) ──────────────────────────
    if symbol == "dead_zone":
        cell = max(2, size // 7)
        ox = cx - (7 * cell) // 2
        oy = cy - (7 * cell) // 2

        # Color constants per Section 9B spec
        DEAD_PX      = (10, 10, 20)      # DEAD — Void Black, absolute zero
        DIM_PX       = (0, 80, 100)       # DIM_ALIVE — #005064 per Section 9B spec (was #123C3C WRONG)
        ALIVE_PX     = (0, 180, 200)     # ALIVE_NORMAL — dim active cyan
        BRIGHT_PX    = (200, 255, 255)   # ALIVE_BRIGHT — White-Cyan corona near crack
        DEEP_CYAN_BG = (26, 58, 64)      # Eye bezel background (#1A3A40)

        # 7x7 glyph layout per Section 9B CANONICAL SPEC (v004 fix):
        # Key: 0=DEAD(void black), 1=ALIVE_NORMAL(dim active cyan), 2=ALIVE_BRIGHT(white-cyan),
        #      3=DIM(barely-alive deep cyan #005064)
        # CRACK is NOT a pixel state — it is a void-black LINE drawn OVER the glyph as overlay.
        # At CRACK positions: underlying pixels are DIM (alive side) or DEAD (dead zone side).
        # Spec row-by-row:
        #   Row 0:  DIM  DIM  DIM  DIM  [CRACK=DEAD]  DEAD  DEAD
        #   Row 1:  DIM  MID  DIM  [CRACK=DIM]  DEAD  DEAD  DEAD
        #   Row 2:  MID  DIM  [CRACK=DIM]  DEAD  DEAD  BRIG  DEAD
        #   Row 3:  DIM  [CRACK=DIM]  DEAD  DEAD  BRIG  DEAD  DEAD
        #   Row 4:  [CRACK=DIM]  DEAD  DEAD  DIM  DIM  DEAD  DIM
        #   Row 5:  DEAD  DEAD  DIM  MID  DIM  DIM  DIM
        #   Row 6:  DEAD  [CRACK=DIM]  DIM  DIM  MID  DIM  DIM
        glyph = [
            [3, 3, 3, 3, 0, 0, 0],   # row 0: DIM DIM DIM DIM | DEAD DEAD DEAD
            [3, 1, 3, 3, 0, 0, 0],   # row 1: DIM MID DIM DIM(crack) | DEAD DEAD DEAD
            [1, 3, 3, 0, 0, 2, 0],   # row 2: MID DIM DIM(crack) DEAD DEAD BRIG DEAD
            [3, 3, 0, 0, 2, 0, 0],   # row 3: DIM DIM(crack) DEAD DEAD BRIG DEAD DEAD
            [3, 0, 0, 3, 3, 0, 3],   # row 4: DIM(crack) DEAD DEAD DIM DIM DEAD DIM
            [0, 0, 3, 1, 3, 3, 3],   # row 5: DEAD DEAD DIM MID DIM DIM DIM
            [0, 3, 3, 3, 1, 3, 3],   # row 6: DEAD DIM(crack) DIM DIM MID DIM DIM
        ]

        color_map = {0: DEAD_PX, 1: ALIVE_PX, 2: BRIGHT_PX, 3: DIM_PX}

        # Background: eye bezel deep cyan-gray
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

        # Void-black crack overlay over the dead-zone glyph — per Section 9B spec (v004 fix):
        # "The crack is rendered in Void Black (#0A0A14) as a 1-2px line OVER the glyph display."
        # HOT_MAG crack belongs on body/frame EXTERIOR only — NOT inside the dead-zone pixel glyph.
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
        draw.ellipse([cx - cell // 2, cy - cell // 2, cx + cell // 2, cy + cell // 2], fill=LINE)
        draw.ellipse([cx + cell // 2, cy - cell, cx + cell * 2 - 2, cy - cell // 2], fill=(255, 252, 245))
        return

    draw.rectangle([ox - 2, oy - 2, ox + 5 * cell + 2, oy + 5 * cell + 2], fill=(255, 255, 255))
    draw.rectangle([ox - 2, oy - 2, ox + 5 * cell + 2, oy + 5 * cell + 2], outline=LINE, width=1)

    for row in range(5):
        for col in range(5):
            v = grid[row][col]
            px = ox + col * cell
            py = oy + row * cell
            color = PIXEL_CYAN if v == 1 else PIXEL_MAG if v == 2 else OFF
            draw.rectangle([px + 1, py + 1, px + cell - 1, py + cell - 1], fill=color)


def draw_right_eye(draw, cx, cy, size, style):
    """Draw Byte's right (organic) eye.

    Styles: half_open, wide, wide_scared, angry, droopy, droopy_resigned,
            droopy_storm, squint, flat, cracked_storm
    """
    cell = size // 5
    if cell < 2:
        cell = 2

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
        draw.ellipse([cx + cell // 2, cy - iris_r + 2,
                      cx + iris_r - 2, cy - cell // 2], fill=(200, 195, 185))
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
        # RESIGNED — 45% aperture, pupil strongly downward, parabolic drooping lower lid
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
        # STORM/CRACKED — right organic eye in storm/damage context.
        # Spec: RESIGNED droopy 50% aperture, downcast pupil, flat/dim highlight.
        # Eye appears damaged: iris color shifted to very dim (near-dead).
        # This is the organic right eye in its most resigned state.
        eye_h = int(eh * 0.50)   # 50% aperture per task spec
        # Eye white — slightly shifted down (weight of storm)
        draw.ellipse([cx - ew, cy - eye_h + 4, cx + ew, cy + eye_h + 4], fill=EYE_W)
        # Iris: shifted DOWN strongly — avoidance/damage gaze
        draw.ellipse([cx - cell + 1, cy + 2, cx + cell + 1, cy + cell * 2 + 2],
                     fill=(35, 22, 10))   # darker iris — dim/damaged
        # Pupil: downcast, shifted down
        draw.ellipse([cx - 4 + 1, cy + 6, cx + 4 + 1, cy + 14], fill=LINE)
        # Flat/dim highlight — barely-there (storm damage = no energy)
        draw.ellipse([cx + cell - 2, cy + 2, cx + ew - 6, cy + cell - 2],
                     fill=(130, 128, 120))  # even dimmer than RESIGNED
        # Heavy upper lid — storm weight pressing down
        draw.arc([cx - ew, cy - eye_h + 4, cx + ew, cy + eye_h + 4],
                 start=195, end=345, fill=LINE, width=8)
        # Drooping lower lid (parabolic sag — same geometry as droopy_resigned)
        droop_pts = []
        for i in range(11):
            t = i / 10.0
            dx = int(-ew + t * 2 * ew)
            sag = int(8 * 4 * t * (1 - t))  # slightly deeper sag than RESIGNED
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
        draw.ellipse([cx + cell // 2, cy - cell, cx + cell * 2 - 2, cy - cell // 2], fill=(255, 252, 245))


def draw_storm_bg_texture(draw, ppx, ppy, panel_w, panel_h, panel_bg):
    """Draw stormy dark void background with circuit trace texture + UV flash hint."""
    # Base fill already done by caller; add circuit traces and storm flicker.

    # Circuit trace lines — very dim cyan, near-invisible against dark BG
    trace_color = (0, 40, 50)     # near-void cyan trace
    uv_color    = (40, 20, 60)    # dim UV violet flash

    # Horizontal trace fragments
    for y_off in [40, 90, 140, 190, 240, 290]:
        y = ppy + y_off
        for x_start in [ppx + 10, ppx + 80, ppx + 140]:
            seg_len = 30 + (x_start % 40)
            draw.line([(x_start, y), (x_start + seg_len, y)], fill=trace_color, width=1)
        # Right-angle junction
        jx = ppx + 60 + (y_off % 50)
        draw.line([(jx, y), (jx, y + 18)], fill=trace_color, width=1)

    # UV flash hint — faint diagonal gradient-like band from upper-left
    for i in range(3):
        x1 = ppx + i * 30
        y1 = ppy + 10
        x2 = ppx + panel_w
        y2 = ppy + panel_h // 2 + i * 20
        draw.line([(x1, y1), (x2, y2)], fill=uv_color, width=1)

    # Small spark/pixel noise
    spark_positions = [
        (ppx + 20,  ppy + 50),
        (ppx + 190, ppy + 80),
        (ppx + 55,  ppy + 170),
        (ppx + 210, ppy + 220),
        (ppx + 30,  ppy + 260),
    ]
    for (sx, sy) in spark_positions:
        draw.rectangle([sx, sy, sx + 2, sy + 2], fill=(0, 100, 120))  # dim cyan spark


def draw_byte(draw, cx, cy, size, expression_name, cracked_symbol, emotion, body_data, right_eye_style, img=None):
    """Draw Byte with per-expression body variation.

    BODY SHAPE: OVAL (ellipse). Canonical since Cycle 8.
    HOVER PARTICLES: 10×10px. Canonical spec.
    img param: required for storm_damage antenna (paste operations).
    """
    s = size

    arm_dy      = body_data.get("arm_dy", 0)
    arm_x_scale = body_data.get("arm_x_scale", 1.0)
    leg_spread  = body_data.get("leg_spread", 1.0)
    body_tilt   = body_data.get("body_tilt", 0)
    body_squash = body_data.get("body_squash", 1.0)
    arm_l_dy    = body_data.get("arm_l_dy", arm_dy)
    arm_r_dy    = body_data.get("arm_r_dy", arm_dy)
    storm_damage = body_data.get("storm_damage", False)

    body_rx = s // 2
    body_ry = int(s * 0.55 * body_squash)
    bcx = cx + body_tilt
    bcy = cy

    # Main oval — GL-01b body fill ALWAYS
    draw.ellipse([bcx - body_rx, bcy - body_ry,
                  bcx + body_rx, bcy + body_ry],
                 fill=BYTE_TEAL, outline=LINE, width=3)  # silhouette: 3px

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

    # Highlight arc — top-left
    draw.arc([bcx - body_rx, bcy - body_ry, bcx + body_rx, bcy + body_ry],
             start=200, end=310, fill=BYTE_HL, width=3)  # interior: 3px (highlight on silhouette edge)

    # Magenta scar markings — body surface detail
    crack_x = bcx - s // 4
    draw.line([(crack_x, bcy - body_ry // 2),
               (crack_x + s // 8, bcy - body_ry // 6)], fill=SCAR_MAG, width=2)  # interior: 2px
    draw.line([(crack_x + s // 8, bcy - body_ry // 6),
               (crack_x - s // 10, bcy + body_ry // 6)], fill=SCAR_MAG, width=2)

    # Damage notch on right side
    notch_pts = [
        (bcx + body_rx - 4,         bcy - body_ry // 4),
        (bcx + body_rx + s // 12,   bcy - body_ry // 6),
        (bcx + body_rx - 4,         bcy + body_ry // 6),
    ]
    draw.polygon(notch_pts, fill=BG, outline=LINE, width=1)

    # Storm damage — additional crack/angular marks on body
    if storm_damage:
        # Extra Hot Magenta crack mark on upper-right body surface
        sx = bcx + s // 6
        sy = bcy - body_ry + 10
        draw.line([(sx, sy), (sx + 8, sy + 12)], fill=HOT_MAG, width=2)
        draw.line([(sx + 8, sy + 12), (sx + 4, sy + 18)], fill=HOT_MAG, width=2)
        # Angular body stress mark (diagonal slash, storm angular lean read)
        draw.line([(bcx + 10, bcy - body_ry // 3),
                   (bcx + 22, bcy + body_ry // 4)], fill=HOT_MAG, width=1)  # detail: 1px

    # Eyes
    eye_y    = bcy - body_ry // 5
    eye_size = max(14, int(body_ry * 0.46))

    # Left eye (pixel/cracked display) — per Section 9B: cracked eye is viewer's left
    lx             = bcx - s // 5
    crack_frame_sz = eye_size + 4

    if storm_damage:
        # Storm variant: cracked eye frame with irregular border (damage warped frame)
        # Outer frame — slightly larger + jitter effect via irregular polygon
        fr = crack_frame_sz // 2
        chip_pts = [
            (lx - fr,         eye_y - fr),         # top-left
            (lx + fr - 2,     eye_y - fr),         # top near-right
            (lx + fr,         eye_y - fr + 3),     # top-right-chip: corner missing
            (lx + fr + 2,     eye_y - fr + 8),     # chipped corner
            (lx + fr,         eye_y + fr),         # bottom-right
            (lx - fr,         eye_y + fr),         # bottom-left
        ]
        draw.polygon(chip_pts, fill=(26, 58, 64), outline=LINE, width=2)  # interior: 2px frame
        # Hot Magenta crack line over the frame — physical crack line per spec
        draw.line([(lx + fr - 2, eye_y - fr), (lx - fr + 3, eye_y + fr)],
                  fill=HOT_MAG, width=2)  # interior: 2px crack
    else:
        draw.rectangle([lx - crack_frame_sz // 2, eye_y - crack_frame_sz // 2,
                        lx + crack_frame_sz // 2, eye_y + crack_frame_sz // 2],
                       fill=(255, 255, 255), outline=LINE, width=2)  # interior: 2px
        draw.line([(lx + 2,  eye_y - crack_frame_sz // 2),
                   (lx - 4,  eye_y + crack_frame_sz // 2)], fill=LINE, width=2)

    draw_pixel_symbol(draw, lx, eye_y, eye_size, cracked_symbol)

    # Right eye (organic, emotion-carrying)
    rx = bcx + s // 5
    draw_right_eye(draw, rx, eye_y, eye_size, right_eye_style)

    # Mouth — varies by emotion
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
        # STORM/CRACKED: flat mouth — no energy, shorter than resigned
        # Exactly flat, absolutely no upturned or downturned ends
        mid_x1 = bcx - mw // 4
        mid_x2 = bcx + mw // 4
        draw.line([(mid_x1, mouth_y), (mid_x2, mouth_y)], fill=LINE, width=2)
    else:
        draw.line([(bcx - mw // 2, mouth_y), (bcx + mw // 2, mouth_y)], fill=LINE, width=2)

    # Antenna
    ant_base_x = bcx - s // 8
    ant_base_y = bcy - body_ry
    if storm_damage:
        # Bent antenna — storm physical damage; kink at midpoint
        ant_mid_x  = ant_base_x + 6   # bent rightward midpoint
        ant_mid_y  = ant_base_y - s // 5
        ant_tip_x  = ant_mid_x - 8    # tip veers left after kink
        ant_tip_y  = ant_mid_y - s // 8
        draw.line([(ant_base_x, ant_base_y),
                   (ant_mid_x, ant_mid_y)], fill=LINE, width=2)  # interior: 2px
        draw.line([(ant_mid_x, ant_mid_y),
                   (ant_tip_x, ant_tip_y)], fill=LINE, width=2)
        # Damaged tip — small magenta spark
        draw.ellipse([ant_tip_x - 3, ant_tip_y - 3,
                      ant_tip_x + 3, ant_tip_y + 3], fill=HOT_MAG)  # detail
    else:
        ant_tip_x = ant_base_x - s // 10
        ant_tip_y = ant_base_y - s // 3
        draw.line([(ant_base_x, ant_base_y),
                   (ant_tip_x, ant_tip_y)], fill=LINE, width=2)
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
                   fill=BYTE_TEAL, outline=LINE, width=2)  # interior: 2px

    right_arm_y = arm_base_y + arm_r_dy
    draw.rectangle([bcx + body_rx,              right_arm_y,
                    bcx + body_rx + arm_extend, right_arm_y + lh],
                   fill=BYTE_TEAL, outline=LINE, width=2)

    leg_offset = int(s // 4 * leg_spread)
    leg_h      = lh
    leg_w      = int(lw * 0.9)
    draw.rectangle([bcx - leg_offset - leg_w // 2, bcy + body_ry,
                    bcx - leg_offset + leg_w // 2, bcy + body_ry + leg_h],
                   fill=BYTE_TEAL, outline=LINE, width=2)
    draw.rectangle([bcx + leg_offset - leg_w // 2, bcy + body_ry,
                    bcx + leg_offset + leg_w // 2, bcy + body_ry + leg_h],
                   fill=BYTE_TEAL, outline=LINE, width=2)

    # Hover particles — 10×10px canonical spec
    for (ppx, ppy, ppc) in [
        (bcx - 20, bcy + body_ry + leg_h + 5,  BYTE_HL),
        (bcx + 5,  bcy + body_ry + leg_h + 8,  SCAR_MAG),
        (bcx + 25, bcy + body_ry + leg_h + 3,  BYTE_HL),
        (bcx - 35, bcy + body_ry + leg_h + 10, (0, 200, 180)),
    ]:
        draw.rectangle([ppx, ppy, ppx + 10, ppy + 10], fill=ppc)


def generate_byte_expression_sheet(output_path):
    """Render 3×3 expression grid for Byte. 9 expressions."""
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

    # Sheet header
    draw.text((PAD, 12),
              "BYTE — Expression Sheet — Luma & the Glitchkin  |  v003  (9 expressions: +STORM/CRACKED)",
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

        # Storm panel gets texture overlay
        if emotion == "storm":
            draw_storm_bg_texture(draw, ppx, ppy, PANEL_W, PANEL_H, panel_bg)

        # Draw Byte — centered, slightly raised to leave room for label bar
        byte_size = 88
        bcx_panel = ppx + PANEL_W // 2
        bcy_panel = ppy + PANEL_H // 2 - 20
        draw_byte(draw, bcx_panel, bcy_panel, byte_size,
                  name, symbol, emotion, body_data, right_eye_style, img)

        # NEW tag for STORM/CRACKED panel
        if "STORM" in name:
            draw.text((ppx + PANEL_W - 56, ppy + 4), "[NEW v003]",
                      fill=(255, 45, 120), font=font_sm)

        # Label bar at bottom
        bar_h = 58
        draw.rectangle([ppx, ppy + PANEL_H - bar_h, ppx + PANEL_W, ppy + PANEL_H], fill=(10, 8, 18))
        draw.text((ppx + 6, ppy + PANEL_H - bar_h + 4),  name,    fill=(0, 240, 255), font=font)
        draw.text((ppx + 6, ppy + PANEL_H - bar_h + 22), prev_st, fill=(120, 110, 140), font=font_sm)
        draw.text((ppx + 6, ppy + PANEL_H - bar_h + 36), next_st, fill=(120, 110, 140), font=font_sm)

    img.save(output_path)
    print(f"Saved: {output_path}  ({total_w}×{total_h}px)")


if __name__ == '__main__':
    import os
    out_dir = "/home/wipkat/team/output/characters/main"
    os.makedirs(out_dir, exist_ok=True)
    generate_byte_expression_sheet(
        os.path.join(out_dir, "LTG_CHAR_byte_expression_sheet_v003.png")
    )
