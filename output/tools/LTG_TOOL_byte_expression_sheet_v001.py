#!/usr/bin/env python3
"""
LTG_TOOL_byte_expression_sheet_v001.py
Byte Expression Sheet Generator — "Luma & the Glitchkin"

v001: Migrated from byte_expressions_generator.py (Cycle 6-10 iterations).
      Added NEUTRAL/DEFAULT-GRUMPY panel (Cycle 13, Dmitri Priority 1).
      Layout upgraded: 4×2 grid (was 3×2) to accommodate 7 expressions.

Expressions (7):
  1. NEUTRAL / DEFAULT           — new Cycle 13
  2. GRUMPY                      — confrontational, carried from prior cycles
  3. SEARCHING                   — scanning, arm extended
  4. ALARMED                     — startle, arms wide
  5. RELUCTANT JOY               — suppressed happiness
  6. CONFUSED                    — head tilt, one arm raised
  7. POWERED DOWN                — flat-line, dormant

Byte anatomy:
  - Body: OVAL (ellipse). Chamfered-box retired Cycle 8.
  - Left eye: pixel-symbol display (cracked screen)
  - Right eye: organic, carries emotion
  - Hover particles: 10×10px canonical spec
  - Magenta scar markings on body (permanent character detail)
"""
from PIL import Image, ImageDraw, ImageFont
import math

BYTE_TEAL  = (0, 212, 232)    # #00D4E8 — body fill
BYTE_HL    = (0, 240, 255)    # #00F0FF — highlights only
BYTE_SH    = (0, 144, 176)    # #0090B0 — shadow
SCAR_MAG   = (255, 45, 107)   # #FF2D6B
LINE       = (10, 10, 20)     # #0A0A14 void black
EYE_W      = (240, 240, 245)
BG         = (20, 18, 28)

# Panel backgrounds — per-expression emotional read at panel scale
BG_NEUTRAL = (28, 34, 42)     # deep blue-grey — resting default, no emotional temperature
BG_GRUMPY  = (38, 20, 28)     # deep red-plum — confrontational
BG_SEARCH  = (22, 30, 44)     # dark slate blue — scanning
BG_ALARM   = (44, 22, 18)     # deep warm red — danger
BG_RELJOY  = (22, 34, 32)     # deep teal-green — suppressed warmth
BG_CONFUSE = (30, 24, 42)     # deep indigo — confusion
BG_PWRDOWN = (14, 12, 18)     # near-black — powered down

# Each expression:
# (name, left_eye_symbol, emotion, body_data, right_eye_style,
#  panel_bg, prev_state, next_state)
#
# body_data keys:
#   arm_dy        — shared arm vertical offset from neutral (fallback)
#   arm_x_scale   — how far arms extend horizontally
#   leg_spread    — leg x offset multiplier
#   body_tilt     — horizontal skew of body top (negative = forward lean)
#   body_squash   — vertical scale (1.0 = normal)
#   arm_l_dy      — left arm independent vertical offset
#   arm_r_dy      — right arm independent vertical offset
#
# right_eye_style options:
#   'wide'         — SEARCHING: wide open, wandering
#   'wide_scared'  — ALARMED: whites showing, deer-in-headlights
#   'angry'        — GRUMPY: heavy upper lid, glare
#   'droopy'       — RELUCTANT JOY: half-closed, suppressing it
#   'squint'       — CONFUSED: tilted, upward glance
#   'flat'         — POWERED DOWN: pixel flat-line
#   'half_open'    — NEUTRAL: 60% aperture, centered pupil, iris not glowing

EXPRESSIONS = [
    # ── NEUTRAL / DEFAULT-GRUMPY (Cycle 13 — Dmitri Priority 1) ─────────────────
    # byte.md Section 7, Expression 1:
    #   Normal eye: half-open, 60% aperture, centered pupil, iris not glowing maximally
    #   Cracked eye: flat line display, dark background, white horizontal pixel line
    #   Mouth: thin horizontal line, slightly downturned ends
    #   Limbs: arms close to body sides, lower limbs pointing straight down
    # Body: centered, standard oval, no lean (body_tilt=0), no squash, arms at sides (arm_dy=4)
    (
        "NEUTRAL / DEFAULT",
        "flat",         # left/pixel eye: flat horizontal line (resting display state)
        "default",      # emotion tag — drives mouth render
        {
            "arm_dy": 4, "arm_x_scale": 0.75, "leg_spread": 0.85,
            "body_tilt": 0, "body_squash": 1.0,
            "arm_l_dy": 4, "arm_r_dy": 4,     # arms close to sides, hanging
        },
        "half_open",    # right eye: half-open, 60% aperture — not glowing maximally
        BG_NEUTRAL,
        "← was: ANY STATE",
        "→ next: SEARCHING / GRUMPY"
    ),
    # ── GRUMPY ──────────────────────────────────────────────────────────────────
    # Confrontational posture (Cycle 8 fix — Dmitri + Marcus mandates):
    # body_tilt=-8: negative = forward lean TOWARD adversary.
    # arm_l_dy=-6, arm_r_dy=-10: both arms raised, asymmetric (ready to refuse/block).
    # arm_x_scale=1.1: arms extend OUT slightly (defensive-aggressive stance).
    # leg_spread=1.1: planted, squared-up feet.
    (
        "GRUMPY",
        "grumpy",       # pixel eye: scowl-bar grid with corner ticks
        "disgust",
        {
            "arm_dy": -8, "arm_x_scale": 1.1, "leg_spread": 1.1,
            "body_tilt": -8, "body_squash": 1.0,
            "arm_l_dy": -6, "arm_r_dy": -10,
        },
        "angry",        # right eye: heavy upper lid, glare
        BG_GRUMPY,
        "← was: NEUTRAL",
        "→ next: REFUSING"
    ),
    # ── SEARCHING ───────────────────────────────────────────────────────────────
    (
        "SEARCHING",
        "loading",      # pixel eye: scanning dot grid
        "curious",
        {
            "arm_dy": -4, "arm_x_scale": 1.1, "leg_spread": 1.2,
            "body_tilt": -8, "body_squash": 1.0,
            "arm_l_dy": 4, "arm_r_dy": -18,   # right arm extended/raised (scanning)
        },
        "wide",         # right eye: wide open, wandering
        BG_SEARCH,
        "← was: NEUTRAL",
        "→ next: ALARMED / FOUND"
    ),
    # ── ALARMED ─────────────────────────────────────────────────────────────────
    (
        "ALARMED",
        "!",            # pixel eye: exclamation mark
        "fear",
        {
            "arm_dy": -16, "arm_x_scale": 1.5, "leg_spread": 1.6,
            "body_tilt": 0, "body_squash": 0.92,
            "arm_l_dy": -10, "arm_r_dy": -22,  # asymmetric startle
        },
        "wide_scared",  # right eye: whites showing, deer-in-headlights
        BG_ALARM,
        "← was: SEARCHING",
        "→ next: FLEEING / FROZEN"
    ),
    # ── RELUCTANT JOY ───────────────────────────────────────────────────────────
    (
        "RELUCTANT JOY",
        "♥",            # pixel eye: heart symbol
        "happy",
        {
            "arm_dy": 8, "arm_x_scale": 0.6, "leg_spread": 0.8,
            "body_tilt": 10, "body_squash": 1.0,
            "arm_l_dy": 8, "arm_r_dy": 8,
        },
        "droopy",       # right eye: heavy-lidded, suppressing emotion
        BG_RELJOY,
        "← was: GRUMPY",
        "→ next: DENYING IT"
    ),
    # ── CONFUSED ────────────────────────────────────────────────────────────────
    (
        "CONFUSED",
        "?",            # pixel eye: question mark
        "confused",
        {
            "arm_dy": -6, "arm_x_scale": 1.0, "leg_spread": 1.1,
            "body_tilt": -18, "body_squash": 1.0,
            "arm_l_dy": -14, "arm_r_dy": 2,   # one arm raised (questioning), one low
        },
        "squint",       # right eye: tilted squint, upward glance
        BG_CONFUSE,
        "← was: ANY STATE",
        "→ next: SEARCHING"
    ),
    # ── POWERED DOWN ────────────────────────────────────────────────────────────
    (
        "POWERED DOWN",
        "flat",         # pixel eye: flat centre-line
        "neutral",      # emotion tag → no mouth rendered
        {
            "arm_dy": 18, "arm_x_scale": 0.7, "leg_spread": 0.6,
            "body_tilt": 0, "body_squash": 0.88,
            "arm_l_dy": 18, "arm_r_dy": 18,
        },
        "flat",         # right eye: flat pixel line (matches left — full shutdown)
        BG_PWRDOWN,
        "← was: ANY STATE",
        "→ next: BOOTING UP"
    ),
]

# ── Layout ─────────────────────────────────────────────────────────────────────
PANEL_W = 240
PANEL_H = 320
COLS    = 4
ROWS    = 2
PAD     = 16
HEADER  = 50


def draw_pixel_symbol(draw, cx, cy, size, symbol):
    """Draw a pixel-eye symbol using a 5×5 grid at given position and size."""
    cell = size // 5
    if cell < 2:
        cell = 2
    ox = cx - (5 * cell) // 2
    oy = cy - (5 * cell) // 2

    PIXEL_CYAN = (0, 240, 255)
    PIXEL_MAG  = (255, 45, 107)
    OFF        = (20, 18, 28)

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
        # POWERED DOWN: flat centre-line — distinct from NEUTRAL which has border ticks
        "flat": [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ],
        # GRUMPY: minus-sign bar with downward corner ticks — distinct from POWERED DOWN flat
        "grumpy": [
            [0, 0, 0, 0, 0],
            [1, 0, 0, 0, 1],
            [1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1],
            [0, 0, 0, 0, 0],
        ],
        "normal": None,  # organic eye fallback
    }

    grid = grids.get(symbol)
    if grid is None:
        # Organic eye fallback
        draw.ellipse([cx - cell * 2, cy - cell * 2, cx + cell * 2, cy + cell * 2], fill=EYE_W)
        draw.ellipse([cx - cell, cy - cell, cx + cell, cy + cell], fill=(60, 38, 20))
        draw.ellipse([cx - cell // 2, cy - cell // 2, cx + cell // 2, cy + cell // 2], fill=LINE)
        draw.ellipse([cx + cell // 2, cy - cell, cx + cell * 2 - 2, cy - cell // 2], fill=(255, 252, 245))
        return

    # Pixel eye background
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
    """Draw Byte's right (organic) eye with emotion-specific expression.

    Styles:
      half_open    — NEUTRAL: 60% aperture, centered pupil, iris not glowing maximally
      wide         — SEARCHING: wide open, wandering
      wide_scared  — ALARMED: whites showing, centered pupil, terror
      angry        — GRUMPY: heavy upper lid, glare
      droopy        — RELUCTANT JOY: half-closed, suppressed
      squint       — CONFUSED: tilted, upward glance
      flat         — POWERED DOWN: flat pixel line
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
        # NEUTRAL / DEFAULT — 60% aperture, centered pupil, iris not glowing maximally
        # Slightly reduced height (half-open = ey_open at 60% of full ew)
        eye_h = int(eh * 0.6)
        draw.ellipse([cx - ew, cy - eye_h, cx + ew, cy + eye_h], fill=EYE_W, outline=LINE, width=1)
        # Iris — smaller than full expressions (not glowing maximally)
        iris_r = int(cell * 1.5)
        draw.ellipse([cx - iris_r, cy - iris_r, cx + iris_r, cy + iris_r], fill=(45, 28, 14))
        # Pupil — small, centered (neither tracking nor avoiding)
        draw.ellipse([cx - cell // 2 - 1, cy - cell // 2 - 1,
                      cx + cell // 2 + 1, cy + cell // 2 + 1], fill=LINE)
        # Minimal highlight — iris not glowing maximally
        draw.ellipse([cx + cell // 2, cy - iris_r + 2,
                      cx + iris_r - 2, cy - cell // 2], fill=(200, 195, 185))
        # Half-open lid line (upper lid covers top 40% of aperture)
        draw.arc([cx - ew, cy - eye_h, cx + ew, cy + eye_h],
                 start=200, end=340, fill=LINE, width=3)

    elif style == "wide":
        # SEARCHING — wide open, slightly wandering
        draw.ellipse([cx - ew, cy - eh, cx + ew, cy + eh], fill=EYE_W)
        draw.ellipse([cx - cell + 2, cy - cell + 2, cx + cell + 2, cy + cell + 2], fill=(60, 38, 20))
        draw.ellipse([cx - cell // 2 + 2, cy - cell // 2 + 2,
                      cx + cell // 2 + 2, cy + cell // 2 + 2], fill=LINE)
        draw.ellipse([cx + cell, cy - eh + 2, cx + ew - 2, cy - cell], fill=(255, 252, 245))

    elif style == "wide_scared":
        # ALARMED — whites showing all around, pupil centered, deer-in-headlights
        draw.ellipse([cx - ew - 2, cy - eh - 3, cx + ew + 2, cy + eh + 3],
                     fill=EYE_W, outline=LINE, width=2)
        draw.ellipse([cx - cell + 1, cy - cell + 1, cx + cell - 1, cy + cell - 1], fill=(60, 38, 20))
        draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=LINE)
        draw.ellipse([cx + cell - 2, cy - eh + 2, cx + ew - 2, cy - cell + 2], fill=(255, 252, 245))
        draw.arc([cx - ew - 2, cy - eh - 3, cx + ew + 2, cy + eh + 3],
                 start=200, end=340, fill=(220, 220, 230), width=2)

    elif style == "angry":
        # GRUMPY — heavy upper lid pressing down, pupil shifted down-inward (glare)
        draw.ellipse([cx - ew, cy - eh + 4, cx + ew, cy + eh], fill=EYE_W)
        draw.ellipse([cx - cell - 2, cy, cx + cell - 2, cy + cell * 2 - 2], fill=(60, 38, 20))
        draw.ellipse([cx - 4 - 2, cy + 4, cx + 4 - 2, cy + 4 + 8], fill=LINE)
        draw.ellipse([cx + 2, cy + 2, cx + cell + 2, cy + cell - 2], fill=(255, 252, 245))
        draw.arc([cx - ew, cy - eh + 4, cx + ew, cy + eh], start=195, end=345, fill=LINE, width=5)
        draw.line([(cx - ew, cy - eh // 2 + 4), (cx + ew, cy - eh // 2)], fill=LINE, width=3)

    elif style == "droopy":
        # RELUCTANT JOY — heavy-lidded, trying NOT to smile, failing
        draw.ellipse([cx - ew, cy - eh + 6, cx + ew, cy + eh + 2], fill=EYE_W)
        draw.ellipse([cx - cell + 1, cy - cell + 4, cx + cell + 1, cy + cell + 4], fill=(60, 38, 20))
        draw.ellipse([cx - 4 + 1, cy + 1, cx + 4 + 1, cy + 8], fill=LINE)
        draw.ellipse([cx + cell, cy - 3, cx + ew - 2, cy + 3], fill=(255, 252, 245))
        draw.arc([cx - ew, cy - eh + 6, cx + ew, cy + eh + 2], start=195, end=345, fill=LINE, width=6)
        draw.line([(cx - ew, cy + 5), (cx - ew + 4, cy + 2)], fill=LINE, width=2)

    elif style == "squint":
        # CONFUSED — slightly squinted/tilted, upward glance
        draw.ellipse([cx - ew, cy - eh + 4, cx + ew, cy + eh + 2], fill=EYE_W)
        draw.ellipse([cx - cell, cy - cell - 2, cx + cell, cy + cell - 2], fill=(60, 38, 20))
        draw.ellipse([cx - 4, cy - 8, cx + 4, cy], fill=LINE)
        draw.ellipse([cx + cell - 2, cy - eh + 4, cx + ew - 4, cy - cell], fill=(255, 252, 245))
        draw.line([(cx - ew, cy - eh // 2 + 4), (cx + ew, cy - eh // 2 + 2)], fill=LINE, width=3)

    else:
        # Default organic eye
        draw.ellipse([cx - ew, cy - eh, cx + ew, cy + eh], fill=EYE_W)
        draw.ellipse([cx - cell, cy - cell, cx + cell, cy + cell], fill=(60, 38, 20))
        draw.ellipse([cx - cell // 2, cy - cell // 2, cx + cell // 2, cy + cell // 2], fill=LINE)
        draw.ellipse([cx + cell // 2, cy - cell, cx + cell * 2 - 2, cy - cell // 2], fill=(255, 252, 245))


def draw_byte(draw, cx, cy, size, expression_name, cracked_symbol, emotion, body_data, right_eye_style):
    """Draw Byte with per-expression body variation.

    BODY SHAPE: OVAL (ellipse). Canonical since Cycle 8.
    The chamfered-box polygon from earlier cycles is RETIRED everywhere.

    HOVER PARTICLES: 10×10px. Canonical spec. No exceptions.
    """
    s = size

    arm_dy      = body_data.get("arm_dy", 0)
    arm_x_scale = body_data.get("arm_x_scale", 1.0)
    leg_spread  = body_data.get("leg_spread", 1.0)
    body_tilt   = body_data.get("body_tilt", 0)
    body_squash = body_data.get("body_squash", 1.0)
    arm_l_dy    = body_data.get("arm_l_dy", arm_dy)
    arm_r_dy    = body_data.get("arm_r_dy", arm_dy)

    # Oval body — rx/ry derived from size + squash
    body_rx = s // 2
    body_ry = int(s * 0.55 * body_squash)
    bcx = cx + body_tilt
    bcy = cy

    # Main oval
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

    # Highlight arc — top-left
    draw.arc([bcx - body_rx, bcy - body_ry, bcx + body_rx, bcy + body_ry],
             start=200, end=310, fill=BYTE_HL, width=3)

    # Magenta scar markings
    crack_x = bcx - s // 4
    draw.line([(crack_x, bcy - body_ry // 2),
               (crack_x + s // 8, bcy - body_ry // 6)], fill=SCAR_MAG, width=2)
    draw.line([(crack_x + s // 8, bcy - body_ry // 6),
               (crack_x - s // 10, bcy + body_ry // 6)], fill=SCAR_MAG, width=2)

    # Damage notch on right side
    notch_pts = [
        (bcx + body_rx - 4,         bcy - body_ry // 4),
        (bcx + body_rx + s // 12,   bcy - body_ry // 6),
        (bcx + body_rx - 4,         bcy + body_ry // 6),
    ]
    draw.polygon(notch_pts, fill=BG, outline=LINE, width=1)

    # Eyes
    eye_y      = bcy - body_ry // 5
    eye_size   = s // 4

    # Left eye (pixel display)
    lx              = bcx - s // 5
    crack_frame_sz  = eye_size + 4
    draw.rectangle([lx - crack_frame_sz // 2, eye_y - crack_frame_sz // 2,
                    lx + crack_frame_sz // 2, eye_y + crack_frame_sz // 2],
                   fill=(255, 255, 255), outline=LINE, width=2)
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
        # Grumpy: downward arc (frown)
        draw.arc([bcx - mw, mouth_y - 8, bcx + mw, mouth_y + 16],
                 start=200, end=340, fill=LINE, width=3)
    elif emotion == "curious":
        # Searching: small oval mouth (engaged, slightly open)
        draw.ellipse([bcx - 8, mouth_y - 8, bcx + 8, mouth_y + 4], outline=LINE, width=2)
    elif emotion == "fear":
        # Alarmed: open mouth oval + fill
        draw.arc([bcx - mw + 4, mouth_y - 10, bcx + mw - 4, mouth_y + 22],
                 start=10, end=170, fill=LINE, width=3)
        draw.chord([bcx - mw + 8, mouth_y - 8, bcx + mw - 8, mouth_y + 18],
                   start=10, end=170, fill=(180, 160, 150))
    elif emotion == "happy":
        # Reluctant Joy: small upward arc (tiny smile he's trying to suppress)
        draw.arc([bcx - mw // 2, mouth_y - 6, bcx + mw // 2, mouth_y + 12],
                 start=20, end=160, fill=LINE, width=3)
    elif emotion == "confused":
        # Confused: wavy line
        for i in range(4):
            x1 = bcx - mw + i * (mw // 2)
            y1 = mouth_y + (4 if i % 2 == 0 else -4)
            x2 = x1 + mw // 2
            y2 = mouth_y + (-4 if i % 2 == 0 else 4)
            draw.line([(x1, y1), (x2, y2)], fill=LINE, width=2)
    elif emotion == "neutral":
        pass  # POWERED DOWN — no mouth rendered
    elif emotion == "default":
        # NEUTRAL / DEFAULT-GRUMPY:
        # byte.md spec: "thin horizontal line, slightly downturned ends"
        # A flat line with the endpoints pulled slightly below center = subtle frown
        mid_x1 = bcx - mw // 2
        mid_x2 = bcx + mw // 2
        draw.line([(mid_x1, mouth_y), (mid_x2, mouth_y)], fill=LINE, width=2)
        # Slightly downturned ends
        draw.line([(mid_x1, mouth_y), (mid_x1 - 6, mouth_y + 4)], fill=LINE, width=2)
        draw.line([(mid_x2, mouth_y), (mid_x2 + 6, mouth_y + 4)], fill=LINE, width=2)
    else:
        draw.line([(bcx - mw // 2, mouth_y), (bcx + mw // 2, mouth_y)], fill=LINE, width=2)

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
    leg_h      = lh
    leg_w      = int(lw * 0.9)
    draw.rectangle([bcx - leg_offset - leg_w // 2, bcy + body_ry,
                    bcx - leg_offset + leg_w // 2, bcy + body_ry + leg_h],
                   fill=BYTE_TEAL, outline=LINE, width=2)
    draw.rectangle([bcx + leg_offset - leg_w // 2, bcy + body_ry,
                    bcx + leg_offset + leg_w // 2, bcy + body_ry + leg_h],
                   fill=BYTE_TEAL, outline=LINE, width=2)

    # Hover particles — 10×10px canonical spec (Cycle 10 fix — no exceptions)
    for (ppx, ppy, ppc) in [
        (bcx - 20, bcy + body_ry + leg_h + 5,  BYTE_HL),
        (bcx + 5,  bcy + body_ry + leg_h + 8,  SCAR_MAG),
        (bcx + 25, bcy + body_ry + leg_h + 3,  BYTE_HL),
        (bcx - 35, bcy + body_ry + leg_h + 10, (0, 200, 180)),
    ]:
        draw.rectangle([ppx, ppy, ppx + 10, ppy + 10], fill=ppc)


def generate_byte_expression_sheet(output_path):
    """Render 4×2 expression grid for Byte. 7 expressions + 1 empty slot."""
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
    draw.text((PAD, 12), "BYTE — Expression Sheet — Luma & the Glitchkin  |  v001",
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

        # Draw Byte — centered, slightly raised to leave room for label bar
        byte_size = 88
        bcx = ppx + PANEL_W // 2
        bcy = ppy + PANEL_H // 2 - 20
        draw_byte(draw, bcx, bcy, byte_size, name, symbol, emotion, body_data, right_eye_style)

        # NEW tag for Neutral panel (Cycle 13 addition)
        if "NEUTRAL" in name:
            draw.text((ppx + PANEL_W - 46, ppy + 4), "[NEW]",
                      fill=(100, 200, 130), font=font_sm)

        # Label bar at bottom
        bar_h = 58
        draw.rectangle([ppx, ppy + PANEL_H - bar_h, ppx + PANEL_W, ppy + PANEL_H], fill=(10, 8, 18))
        draw.text((ppx + 6, ppy + PANEL_H - bar_h + 4),  name,    fill=(0, 240, 255), font=font)
        draw.text((ppx + 6, ppy + PANEL_H - bar_h + 22), prev_st, fill=(120, 110, 140), font=font_sm)
        draw.text((ppx + 6, ppy + PANEL_H - bar_h + 36), next_st, fill=(120, 110, 140), font=font_sm)

    # Fill 8th slot (empty — reserved for future expression)
    empty_col = (len(EXPRESSIONS)) % COLS
    empty_row = (len(EXPRESSIONS)) // COLS
    epx = PAD + empty_col * (PANEL_W + PAD)
    epy = HEADER + empty_row * (PANEL_H + PAD)
    draw.rectangle([epx, epy, epx + PANEL_W, epy + PANEL_H], fill=(16, 14, 22))
    draw.rectangle([epx, epy, epx + PANEL_W, epy + PANEL_H], outline=(30, 28, 40), width=1)
    draw.text((epx + PANEL_W // 2 - 30, epy + PANEL_H // 2 - 8), "[RESERVED]",
              fill=(40, 38, 55), font=font_sm)

    img.save(output_path)
    print(f"Saved: {output_path}  ({total_w}×{total_h}px)")


if __name__ == '__main__':
    import os
    out_dir = "/home/wipkat/team/output/characters/main"
    os.makedirs(out_dir, exist_ok=True)
    generate_byte_expression_sheet(
        os.path.join(out_dir, "LTG_CHAR_byte_expression_sheet_v001.png")
    )
