#!/usr/bin/env python3
"""
LTG_CHAR_glitch_expression_sheet_v001.py
Glitch — Expression Sheet v001
"Luma & the Glitchkin" — Cycle 23 / Maya Santos

GLITCH CHARACTER DESIGN SPEC:
  Glitch is the primary Glitchkin antagonist — a fractured, corrupted entity
  that embodies the Corruption's destructive energy. Unlike Byte (reformed,
  oval, buoyant), Glitch is angular, asymmetric, and unstable.

  Shape language: diamond / rhombus body core — 45-degree rotated square.
    Asymmetric: left side larger than right (corrupted asymmetry, not cute asymmetry).
    No smooth curves. Every edge is hard. Spikes at top and bottom of the diamond.
    Pixel face occupies front surface — dual-eye system (both sides corrupted).

  Primary color: CORRUPT_AMBER #FF8C00 (GL-07) — bridge between worlds,
    "real world object consumed by glitch energy."
  Secondary: HOT_MAGENTA #FF2D6B — scar/crack lines, danger readout.
  Shadow: CORRUPTED_AMBER_SHADOW #A84C00.
  Highlight: SOFT_GOLD #E8C95A — echo of warm world origin.
  Body markings: UV_PURPLE #7B2FBE — deep corruption shadow.
  Line: VOID_BLACK #0A0A14 — canonical Glitch entity outline.
  Background: VOID_BLACK + glitch color ambients.

  Proportions: Similar scale to Byte. body_rx = 40-50, body_ry = 36-44.
    Diamond form: 4 vertices — top spike, left, bottom spike, right.
    Limbs: 3 total — one left arm-spike, one right arm-spike, one tail-spike.
    No friendly "legs" — Glitch hovers via corrupted confetti (Hot Magenta/UV Purple).

  Face: 3×3 pixel grid (smaller than Byte's 7×7 — rawer, less defined).
    Both "eyes" are pixel glyphs simultaneously — no organic eye.
    Left glyph: primary expression symbol.
    Right glyph: corruption bleed (partially destabilized version of left).

  Expressions (4-panel, 2×2 grid):
    1. NEUTRAL        — idle threat. Symmetric diamond lean, dim amber pixel eyes.
    2. MISCHIEVOUS    — tilted +20, asymmetric spikes, smirk mouth, one eye bright.
    3. PANICKED       — body squash 0.6, both eyes wide/alarmed, erratic confetti.
    4. TRIUMPHANT     — body stretch 1.3, arms fully extended, bright amber glow.

Standards:
  - show_guides=False for pitch export (GL-07 clean export)
  - 3-tier line weight: silhouette 3px, interior 2px, detail 1px (at 1x output)
    (drawn at 2x render, LANCZOS down to 1x)
  - Canvas: 800×800 (2×2 grid) — 4 expressions
  - Panel size: 360×360px at 1x (plus header + label areas)
  - After img.paste(), refresh draw = ImageDraw.Draw(img)

Output: output/characters/main/LTG_CHAR_glitch_expression_sheet_v001.png
Color model: output/characters/main/LTG_CHAR_glitch_color_model_v001.png (generated separately)

[Renamed from LTG_CHAR_glitch_expression_sheet_v001.py to LTG_TOOL_glitch_expression_sheet_v001.py
 in Cycle 28 — generator files use LTG_TOOL_ prefix. Output PNG names are unchanged.]
"""

from PIL import Image, ImageDraw, ImageFont
import math
import os

# ── Palette ────────────────────────────────────────────────────────────────────
CORRUPT_AMB   = (255, 140,   0)   # GL-07 #FF8C00 Corrupted Amber — primary body fill
CORRUPT_AMB_SH= (168,  76,   0)   # #A84C00 Corrupted Amber Shadow
CORRUPT_AMB_HL= (255, 185,  80)   # warm highlight on amber body
SOFT_GOLD     = (232, 201,  90)   # #E8C95A — echo of warm origin world
HOT_MAG       = (255,  45, 107)   # #FF2D6B Hot Magenta — crack/scar lines
UV_PURPLE     = (123,  47, 190)   # #7B2FBE UV Purple — deep shadow/corruption
ACID_GREEN    = ( 57, 255,  20)   # #39FF14 Acid Green — pixel eye "alive" state
ELEC_CYAN     = (  0, 240, 255)   # #00F0FF Electric Cyan — pixel bleed
VOID_BLACK    = ( 10,  10,  20)   # #0A0A14 Void Black — line + deep background
STATIC_WHITE  = (248, 246, 236)   # #F8F6EC near-white pixel highlight
CANVAS_BG     = ( 10,  10,  20)   # void black canvas (Glitch entity on dark ground)

# Panel backgrounds — per expression
BG_NEUTRAL    = ( 22,  18,  32)   # deep purple-void
BG_MISCHIEVOUS= ( 28,  12,  18)   # near-void with warm ember hint
BG_PANICKED   = ( 12,  12,  22)   # cold void panic
BG_TRIUMPHANT = ( 32,  22,   8)   # warm amber glow from triumphant Glitch

HEADER_H  = 54
LABEL_H   = 36
PAD       = 18
COLS      = 2
ROWS      = 2
SCALE     = 2  # 2x internal render, LANCZOS to 1x

# At 1x: 2 cols × 2 rows = 4 panels
# Canvas: 800px wide — PAD on sides + between
# Each panel slot: (800 - 3*PAD) / 2 wide
PANEL_W_1X = (800 - 3 * PAD) // COLS   # 391 — but we use round 382
PANEL_H_1X = (800 - HEADER_H - LABEL_H * ROWS - (ROWS + 1) * PAD) // ROWS  # ~316

CANVAS_W_1X = 800
CANVAS_H_1X = HEADER_H + ROWS * (PANEL_H_1X + LABEL_H) + (ROWS + 1) * PAD

# ── Geometry: Diamond body ────────────────────────────────────────────────────
# At 2x render, character is drawn at 2x scale then LANCZOS to 1x output.
# All geometry values below are in 1x space unless marked "2x".

def diamond_pts(cx, cy, rx, ry, tilt_deg=0, squash=1.0, stretch=1.0):
    """Return [top, right, bottom, left] vertices of diamond (rhombus).
    tilt_deg: clockwise rotation of the diamond axis.
    squash: vertical compression (< 1.0).
    stretch: vertical extension (> 1.0).
    """
    ry_eff = int(ry * squash * stretch)
    angle = math.radians(tilt_deg)
    # Top spike (up)
    top    = (cx + int(rx * 0.15 * math.sin(angle)),
              cy - ry_eff + int(rx * 0.15 * math.cos(angle)))
    # Right point
    right  = (cx + int(rx * math.cos(-angle)),
              cy + int(rx * 0.2 * math.sin(-angle)))
    # Bottom spike (down — slightly longer than top for asymmetry)
    bot    = (cx - int(rx * 0.15 * math.sin(angle)),
              cy + int(ry_eff * 1.15))
    # Left point
    left   = (cx - int(rx * math.cos(-angle)),
              cy - int(rx * 0.2 * math.sin(-angle)))
    return [top, right, bot, left]


def draw_glitch_body(draw, cx, cy, rx, ry,
                     tilt_deg=0, squash=1.0, stretch=1.0,
                     crack_visible=True):
    """Draw Glitch's diamond body with Corrupt Amber fill, scar lines, shadow."""
    pts = diamond_pts(cx, cy, rx, ry, tilt_deg, squash, stretch)
    # Shadow layer (slightly enlarged, UV purple offset)
    sh_pts = [(x + 3, y + 4) for x, y in pts]
    draw.polygon(sh_pts, fill=UV_PURPLE)
    # Main body fill
    draw.polygon(pts, fill=CORRUPT_AMB)
    # Highlight: top-left facet
    top, right, bot, left = pts
    mid_tl = ((top[0] + left[0]) // 2, (top[1] + left[1]) // 2)
    ctr = (cx, cy - ry // 4)
    draw.polygon([top, ctr, mid_tl], fill=CORRUPT_AMB_HL)
    # Silhouette outline
    draw.polygon(pts, outline=VOID_BLACK, width=3)
    # Hot Magenta crack line across body (interior structure weight)
    if crack_visible:
        crack_start = (cx - rx // 2, cy - ry // 3)
        crack_end   = (cx + rx // 3, cy + ry // 2)
        draw.line([crack_start, crack_end], fill=HOT_MAG, width=2)
        # Secondary crack branch
        mid_crack = ((crack_start[0] + crack_end[0]) // 2,
                     (crack_start[1] + crack_end[1]) // 2)
        draw.line([mid_crack, (cx + rx // 2, cy - ry // 4)],
                  fill=HOT_MAG, width=1)


def draw_top_spike(draw, cx, cy_top, rx, spike_h=12, tilt_off=0):
    """Jagged triple-spike at top of diamond."""
    sx = cx + tilt_off
    pts = [
        (sx - spike_h // 2, cy_top),
        (sx - spike_h, cy_top - spike_h),
        (sx, cy_top - spike_h * 2),
        (sx + spike_h, cy_top - spike_h),
        (sx + spike_h // 2, cy_top),
    ]
    draw.polygon(pts, fill=CORRUPT_AMB)
    draw.polygon(pts, outline=VOID_BLACK, width=2)
    # Hot mag tip
    draw.line([(sx, cy_top - spike_h * 2), (sx, cy_top - spike_h * 2 - 4)],
              fill=HOT_MAG, width=2)


def draw_bottom_spike(draw, cx, cy_bot, spike_h=10):
    """Single bottom tail spike (data packet drag)."""
    pts = [
        (cx - spike_h // 2, cy_bot),
        (cx + spike_h // 2, cy_bot),
        (cx, cy_bot + spike_h + 4),
    ]
    draw.polygon(pts, fill=CORRUPT_AMB_SH)
    draw.polygon(pts, outline=VOID_BLACK, width=2)


def draw_arm(draw, cx, cy, side='left', arm_dy=0, arm_dx=0, rx=40):
    """Draw an arm-spike. side='left'|'right'."""
    if side == 'left':
        ax = cx - rx - 6
        ay = cy + arm_dy
        tip = (ax - 14 + arm_dx, ay - 8)
    else:
        ax = cx + rx + 6
        ay = cy + arm_dy
        tip = (ax + 14 + arm_dx, ay - 8)
    # Arm stub as triangle spike
    pts = [(ax, ay - 5), (ax, ay + 5), tip]
    draw.polygon(pts, fill=CORRUPT_AMB)
    draw.polygon(pts, outline=VOID_BLACK, width=2)


def draw_pixel_eye(draw, ex, ey, cell=5, expr='neutral', side='left'):
    """Draw a 3×3 pixel face-glyph eye for Glitch.
    cell: pixel cell size in px (at render scale).
    expr: 'neutral'|'mischievous'|'panicked'|'triumphant'
    side: 'left'|'right' — right eye is partially destabilized.

    Color states:
      0 = VOID (void black — dead pixel)
      1 = DIM (corrupted amber shadow — barely alive)
      2 = ACTIVE (corrupt amber — on)
      3 = BRIGHT (soft gold — maximum energy)
      4 = HOT (hot magenta — danger/anger)
      5 = ACID (acid green — mischief)
    """
    PIXEL_COLORS = {
        0: VOID_BLACK,
        1: CORRUPT_AMB_SH,
        2: CORRUPT_AMB,
        3: SOFT_GOLD,
        4: HOT_MAG,
        5: ACID_GREEN,
    }

    # Glyph definitions: list of 3 rows × 3 cols
    GLYPHS = {
        'neutral':     [[0, 2, 0],
                        [2, 1, 2],
                        [0, 2, 0]],   # cross/diamond — watchful

        'mischievous': [[5, 0, 5],
                        [0, 5, 0],
                        [5, 0, 5]],   # X pattern — acid green mischief

        'panicked':    [[4, 4, 4],
                        [4, 0, 4],
                        [4, 4, 4]],   # hot mag ring — alarm

        'triumphant':  [[3, 3, 3],
                        [3, 3, 3],
                        [3, 3, 3]],   # solid gold — maximum energy
    }

    # Destabilized right eye: some bright pixels become void or dim
    DESTAB = {
        'neutral':     [[1, 2, 0],
                        [2, 0, 1],
                        [0, 2, 1]],
        'mischievous': [[5, 0, 0],
                        [0, 5, 5],
                        [5, 0, 0]],
        'panicked':    [[4, 0, 4],
                        [0, 4, 0],
                        [4, 0, 4]],
        'triumphant':  [[3, 3, 1],
                        [3, 3, 3],
                        [1, 3, 3]],
    }

    glyph = DESTAB[expr] if side == 'right' else GLYPHS[expr]

    for row in range(3):
        for col in range(3):
            state = glyph[row][col]
            color = PIXEL_COLORS[state]
            px = ex + col * cell
            py = ey + row * cell
            draw.rectangle([px, py, px + cell - 1, py + cell - 1],
                            fill=color)


def draw_mouth(draw, mx, my, expr='neutral', w=14):
    """Draw Glitch's pixel-style mouth."""
    if expr == 'neutral':
        # Flat 3-pixel line
        for i in range(3):
            draw.rectangle([mx + i * 4, my, mx + i * 4 + 2, my + 2],
                            fill=CORRUPT_AMB_SH)

    elif expr == 'mischievous':
        # Asymmetric upward curl — left flat, right raised
        pts = [(mx, my), (mx + w // 2, my - 2), (mx + w, my - 4)]
        draw.line(pts, fill=HOT_MAG, width=2)
        # Pixel dot accent
        draw.rectangle([mx + w - 1, my - 5, mx + w + 1, my - 3],
                        fill=ACID_GREEN)

    elif expr == 'panicked':
        # Wide open O-gap — alarm
        draw.ellipse([mx, my - 4, mx + w, my + 4],
                     outline=HOT_MAG, width=2)

    elif expr == 'triumphant':
        # Wide upward sweep — gloat
        pts = [(mx, my + 2), (mx + w // 2, my - 6), (mx + w, my + 2)]
        draw.line(pts, fill=SOFT_GOLD, width=2)
        # Gleam dots
        for gx in [mx + 3, mx + w // 2 - 1, mx + w - 4]:
            draw.rectangle([gx, my - 8, gx + 1, my - 6],
                            fill=STATIC_WHITE)


def draw_hover_confetti(draw, cx, cy_bot, expr='neutral', seed=7):
    """Pixel confetti beneath Glitch — Hot Magenta/UV Purple (corrupted hover)."""
    import random
    rng = random.Random(seed)
    confetti_colors = {
        'neutral':     [HOT_MAG, UV_PURPLE, VOID_BLACK],
        'mischievous': [ACID_GREEN, HOT_MAG, ACID_GREEN],
        'panicked':    [HOT_MAG, HOT_MAG, ELEC_CYAN],
        'triumphant':  [CORRUPT_AMB, SOFT_GOLD, HOT_MAG],
    }
    cols = confetti_colors.get(expr, [HOT_MAG, UV_PURPLE])
    count = {'neutral': 8, 'mischievous': 12, 'panicked': 16, 'triumphant': 14}.get(expr, 8)
    for _ in range(count):
        px = rng.randint(cx - 24, cx + 24)
        py = rng.randint(cy_bot + 4, cy_bot + 18)
        sz = rng.choice([2, 3, 4])
        col = rng.choice(cols)
        draw.rectangle([px, py, px + sz, py + sz], fill=col)


def draw_expression(draw, panel_cx, panel_cy, panel_w, panel_h,
                    expr='neutral', show_guides=False):
    """Draw one expression of Glitch centered in the panel area."""
    cx = panel_cx
    cy = panel_cy + panel_h // 10  # slight upward offset from center

    # Expression parameters
    params = {
        'neutral':     dict(tilt=0,   squash=1.0,  stretch=1.0,
                            arm_l_dy=0, arm_r_dy=0,
                            spike_h=10, crack=True),
        'mischievous': dict(tilt=15,  squash=0.92, stretch=1.0,
                            arm_l_dy=-8, arm_r_dy=6,
                            spike_h=14, crack=True),
        'panicked':    dict(tilt=-8,  squash=0.62, stretch=1.0,
                            arm_l_dy=12, arm_r_dy=14,
                            spike_h=6,  crack=True),
        'triumphant':  dict(tilt=0,   squash=1.0,  stretch=1.28,
                            arm_l_dy=-12, arm_r_dy=-14,
                            spike_h=18, crack=True),
    }
    p = params.get(expr, params['neutral'])

    # Body dimensions
    rx = 38
    ry = 34

    # Draw hover confetti beneath body
    cy_bot = cy + int(ry * p['squash'] * p['stretch'] * 1.15) + 6
    draw_hover_confetti(draw, cx, cy_bot, expr=expr, seed=hash(expr) % 100 + 1)

    # Bottom spike
    draw_bottom_spike(draw, cx, cy_bot - 2, spike_h=10)

    # Draw body
    draw_glitch_body(draw, cx, cy, rx, ry,
                     tilt_deg=p['tilt'],
                     squash=p['squash'],
                     stretch=p['stretch'],
                     crack_visible=p['crack'])

    # Arms (drawn after body so they appear over body edge)
    draw_arm(draw, cx, cy, side='left',  arm_dy=p['arm_l_dy'], rx=rx)
    draw_arm(draw, cx, cy, side='right', arm_dy=p['arm_r_dy'], rx=rx)

    # Top spike
    cy_top = cy - int(ry * p['squash'] * p['stretch'])
    tilt_off = int(p['tilt'] * 0.4)
    draw_top_spike(draw, cx, cy_top, rx,
                   spike_h=p['spike_h'], tilt_off=tilt_off)

    # Face: pixel eyes + mouth
    # Eye positions relative to body center
    face_cy = cy - ry // 6
    cell = 5  # pixel cell size

    # Left eye block (3×3 cells = 15px wide)
    leye_x = cx - rx // 2 - cell * 3 // 2
    leye_y = face_cy - cell * 3 // 2
    draw_pixel_eye(draw, leye_x, leye_y, cell=cell, expr=expr, side='left')

    # Right eye block
    reye_x = cx + rx // 2 - cell * 3 // 2
    reye_y = face_cy - cell * 3 // 2
    draw_pixel_eye(draw, reye_x, reye_y, cell=cell, expr=expr, side='right')

    # Mouth
    mouth_cx = cx - 7
    mouth_cy = face_cy + cell * 3 // 2 + 4
    draw_mouth(draw, mouth_cx, mouth_cy, expr=expr, w=14)

    # Brow bar: single pixel line over each eye (interior structure weight)
    if expr == 'panicked':
        # Both brows raised steeply outward
        draw.line([(leye_x - 2, leye_y - 5), (leye_x + 14, leye_y - 2)],
                  fill=HOT_MAG, width=2)
        draw.line([(reye_x - 2, reye_y - 2), (reye_x + 14, reye_y - 5)],
                  fill=HOT_MAG, width=2)
    elif expr == 'mischievous':
        # Asymmetric: left brow low, right brow sharply angled
        draw.line([(leye_x, leye_y - 2), (leye_x + 14, leye_y - 2)],
                  fill=CORRUPT_AMB_SH, width=2)
        draw.line([(reye_x, reye_y - 5), (reye_x + 14, reye_y - 1)],
                  fill=ACID_GREEN, width=2)
    elif expr == 'triumphant':
        # Both brows high and outward-angled
        draw.line([(leye_x, leye_y - 6), (leye_x + 14, leye_y - 2)],
                  fill=SOFT_GOLD, width=2)
        draw.line([(reye_x, reye_y - 2), (reye_x + 14, reye_y - 6)],
                  fill=SOFT_GOLD, width=2)
    else:
        # Neutral: flat dim bars
        draw.line([(leye_x, leye_y - 3), (leye_x + 14, leye_y - 3)],
                  fill=CORRUPT_AMB_SH, width=1)
        draw.line([(reye_x, reye_y - 3), (reye_x + 14, reye_y - 3)],
                  fill=CORRUPT_AMB_SH, width=1)

    if show_guides:
        # Construction circle overlay (for review only)
        guide = Image.new("RGBA", (panel_w, panel_h), (0, 0, 0, 0))
        gd = ImageDraw.Draw(guide)
        r_guide = ry + 8
        gd.ellipse(
            [panel_cx - r_guide, panel_cy - r_guide,
             panel_cx + r_guide, panel_cy + r_guide],
            outline=(180, 120, 60, 48), width=1
        )


def build_sheet(show_guides=False):
    """Render the 2×2 expression sheet at 2x, downsample to 1x output."""
    W2 = CANVAS_W_1X * SCALE
    H2 = CANVAS_H_1X * SCALE
    PW2 = PANEL_W_1X * SCALE
    PH2 = PANEL_H_1X * SCALE
    PAD2 = PAD * SCALE
    HEADER_H2 = HEADER_H * SCALE
    LABEL_H2 = LABEL_H * SCALE

    img = Image.new("RGB", (W2, H2), CANVAS_BG)
    draw = ImageDraw.Draw(img)

    EXPRESSIONS = [
        ("NEUTRAL",      BG_NEUTRAL),
        ("MISCHIEVOUS",  BG_MISCHIEVOUS),
        ("PANICKED",     BG_PANICKED),
        ("TRIUMPHANT",   BG_TRIUMPHANT),
    ]

    # ── Header ────────────────────────────────────────────────────────────────
    try:
        font_title  = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                                         24 * SCALE)
        font_label  = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                                         10 * SCALE)
    except Exception:
        font_title = ImageFont.load_default()
        font_label = ImageFont.load_default()

    draw.rectangle([0, 0, W2, HEADER_H2], fill=(18, 14, 26))
    title_text = "GLITCH — Expression Sheet v001"
    try:
        tb = draw.textbbox((0, 0), title_text, font=font_title)
        tw = tb[2] - tb[0]
        th = tb[3] - tb[1]
    except Exception:
        tw, th = len(title_text) * 14 * SCALE, 24 * SCALE
    draw.text(((W2 - tw) // 2, (HEADER_H2 - th) // 2),
              title_text, fill=CORRUPT_AMB, font=font_title)

    # Subtitle bar
    sub_text = "ANTAGONIST  |  GL-07 CORRUPT AMBER  |  CYCLE 23  |  show_guides=False"
    try:
        sb = draw.textbbox((0, 0), sub_text, font=font_label)
        sw = sb[2] - sb[0]
        draw.text(((W2 - sw) // 2, HEADER_H2 - 18 * SCALE),
                  sub_text, fill=(120, 80, 40), font=font_label)
    except Exception:
        pass

    # ── Panels ────────────────────────────────────────────────────────────────
    for idx, (expr_name, bg_col) in enumerate(EXPRESSIONS):
        col = idx % COLS
        row = idx // COLS

        px = PAD2 + col * (PW2 + PAD2)
        py = HEADER_H2 + PAD2 + row * (PH2 + LABEL_H2 + PAD2)

        # Panel background
        draw.rectangle([px, py, px + PW2, py + PH2], fill=bg_col)

        # Character draw at 2x scale
        panel_cx = px + PW2 // 2
        panel_cy = py + PH2 // 2
        expr_key = expr_name.lower()

        draw_expression(draw,
                        panel_cx, panel_cy,
                        PW2, PH2,
                        expr=expr_key,
                        show_guides=show_guides)

        # Panel border (subtle)
        draw.rectangle([px, py, px + PW2, py + PH2],
                       outline=(40, 30, 50), width=1)

        # ── Label ─────────────────────────────────────────────────────────────
        label_y = py + PH2 + 4 * SCALE
        try:
            lb = draw.textbbox((0, 0), expr_name, font=font_label)
            lw = lb[2] - lb[0]
        except Exception:
            lw = len(expr_name) * 8 * SCALE
        draw.text((px + (PW2 - lw) // 2, label_y),
                  expr_name, fill=CORRUPT_AMB, font=font_label)

    # ── Downsample ────────────────────────────────────────────────────────────
    img_out = img.resize((CANVAS_W_1X, CANVAS_H_1X), Image.LANCZOS)
    return img_out


def main():
    out_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "characters", "main"
    )
    os.makedirs(out_dir, exist_ok=True)

    # Pitch export (show_guides=False)
    sheet = build_sheet(show_guides=False)
    out_path = os.path.join(out_dir, "LTG_CHAR_glitch_expression_sheet_v001.png")
    sheet.save(out_path)
    print(f"Saved: {out_path}")
    print(f"  Size: {sheet.size[0]}×{sheet.size[1]}px")
    print("  Expressions: NEUTRAL, MISCHIEVOUS, PANICKED, TRIUMPHANT")
    print("  show_guides=False (pitch export)")


if __name__ == "__main__":
    main()
