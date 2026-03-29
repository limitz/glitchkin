#!/usr/bin/env python3
"""
LTG_CHAR_glitch_turnaround_v002.py
Glitch — 4-View Character Turnaround v002
"Luma & the Glitchkin" — Cycle 24 / Maya Santos

Cycle 24 shadow contrast fix (Alex Chen review):
  PROBLEM (v001): UV_PURPLE shadow fill on SIDE and BACK view body was nearly
  invisible against the void-dark canvas. SIDE view read as a flat amber kite
  with no internal structure. BACK view HOT_MAG scars had insufficient contrast.

  FIX applied in v002:
  - draw_body_side(): body fill changed from CORRUPT_AMB_SH (was UV_PURPLE) as
    the dominant side body. Central lit stripe (CORRUPT_AMB) retained. Added
    Void Black edge divider line between lit stripe and shadow areas (2px) to
    define facet geometry independent of color contrast.
  - draw_body_back(): base fill changed from UV_PURPLE to CORRUPT_AMB_SH
    (dark amber). HOT_MAG scar lines now have clear contrast against amber base.
    UV_PURPLE structural line on back retained as secondary detail element only.
  - FRONT and 3/4 views unchanged (UV_PURPLE shadow offset reads correctly there).

4 views: FRONT, 3/4, SIDE, BACK
Canvas: 1600×700 (4 panels × 400w, single header bar)

Output: output/characters/main/turnarounds/LTG_CHAR_glitch_turnaround_v002.png
Supersedes: LTG_CHAR_glitch_turnaround_v001.png

[Renamed from LTG_CHAR_glitch_turnaround_v002.py to LTG_TOOL_glitch_turnaround_v002.py
 in Cycle 28 — generator files use LTG_TOOL_ prefix. Output PNG names are unchanged.]
"""

from PIL import Image, ImageDraw, ImageFont
import math
import os

# ── Palette ────────────────────────────────────────────────────────────────────
CORRUPT_AMB    = (255, 140,   0)
CORRUPT_AMB_SH = (168,  76,   0)
CORRUPT_AMB_HL = (255, 185,  80)
SOFT_GOLD      = (232, 201,  90)
HOT_MAG        = (255,  45, 107)
UV_PURPLE      = (123,  47, 190)
VOID_BLACK     = ( 10,  10,  20)
ACID_GREEN     = ( 57, 255,  20)
STATIC_WHITE   = (248, 246, 236)
ELEC_CYAN      = (  0, 240, 255)

LINE        = VOID_BLACK
CANVAS_BG   = ( 16,  14,  24)    # deep void purple canvas
PANEL_BG    = ( 20,  16,  28)    # per-panel background
HEADER_BG   = ( 12,  10,  20)    # header bar
LABEL_COL   = CORRUPT_AMB
HU_LINE_COL = ( 80,  50,  80)    # subtle purple ruler lines

CANVAS_W = 1600
CANVAS_H = 700
HEADER_H = 52
LABEL_H  = 32
VIEWS    = ["FRONT", "3/4", "SIDE", "BACK"]
N_VIEWS  = 4
PANEL_W  = CANVAS_W // N_VIEWS   # 400
PANEL_H  = CANVAS_H - HEADER_H - LABEL_H   # 616

SCALE    = 2  # internal 2x render, downsample to 1x at end


# ─────────────────────────────────────────────────────────────────────────────
# Drawing helpers (all coords in 1x space, SCALE applied at render call)
# ─────────────────────────────────────────────────────────────────────────────

def diamond_pts_2d(cx, cy, rx, ry, tilt_deg=0):
    """4-point diamond (top, right, bottom, left)."""
    angle = math.radians(tilt_deg)
    top   = (cx + int(rx * 0.1 * math.sin(angle)),  cy - ry)
    right = (cx + rx,  cy + int(rx * 0.1))
    bot   = (cx - int(rx * 0.1 * math.sin(angle)),  cy + int(ry * 1.1))
    left  = (cx - rx,  cy - int(rx * 0.1))
    return [top, right, bot, left]


def draw_body_front(d, cx, cy, rx, ry):
    """FRONT view — full diamond body."""
    pts = diamond_pts_2d(cx, cy, rx, ry)
    # Shadow
    sh = [(x+3, y+4) for x, y in pts]
    d.polygon(sh, fill=UV_PURPLE)
    d.polygon(pts, fill=CORRUPT_AMB)
    # Highlight facet
    top, right, bot, left = pts
    ctr = (cx, cy - ry // 4)
    mid_tl = ((top[0]+left[0])//2, (top[1]+left[1])//2)
    d.polygon([top, ctr, mid_tl], fill=CORRUPT_AMB_HL)
    # Outline
    d.polygon(pts, outline=LINE, width=3)
    # Crack lines
    d.line([(cx - rx//2, cy - ry//3), (cx + rx//3, cy + ry//2)],
           fill=HOT_MAG, width=2)
    d.line([((cx - rx//2 + cx + rx//3)//2, (cy - ry//3 + cy + ry//2)//2),
            (cx + rx//2, cy - ry//4)], fill=HOT_MAG, width=1)


def draw_body_threequarter(d, cx, cy, rx, ry):
    """3/4 view — slightly foreshortened (left side narrower)."""
    # Skew: left side compressed to 60% of rx
    rx_near = rx
    rx_far  = int(rx * 0.55)
    pts = [
        (cx,          cy - ry),          # top
        (cx + rx_near, cy + int(rx*0.1)), # right (near side)
        (cx,           cy + int(ry*1.1)), # bottom
        (cx - rx_far,  cy - int(rx*0.1)), # left (far side)
    ]
    sh = [(x+3, y+4) for x, y in pts]
    d.polygon(sh, fill=UV_PURPLE)
    d.polygon(pts, fill=CORRUPT_AMB)
    # Far-face shadow
    far_pts = [pts[0], pts[3], pts[2]]
    d.polygon(far_pts, fill=CORRUPT_AMB_SH)
    # Near highlight
    ctr = (cx + rx//4, cy - ry//4)
    d.polygon([pts[0], ctr, pts[1]], fill=CORRUPT_AMB_HL)
    d.polygon(pts, outline=LINE, width=3)
    # Crack on near face only
    d.line([(cx, cy - ry//4), (cx + rx//2, cy + ry//3)],
           fill=HOT_MAG, width=2)


def draw_body_side(d, cx, cy, rx, ry):
    """SIDE view — diamond foreshortened to near-sliver.
    v002: fill changed to CORRUPT_AMB_SH (was UV_PURPLE base).
    Lit central stripe (CORRUPT_AMB) retained. Added Void Black divider lines
    between lit stripe and shadow areas to define facet geometry independent
    of color contrast (Alex Chen shadow-contrast fix, Cycle 24).
    """
    rx_side = int(rx * 0.4)
    pts = [
        (cx,             cy - ry),
        (cx + rx_side,   cy + int(ry * 0.1)),
        (cx,             cy + int(ry * 1.1)),
        (cx - rx_side,   cy - int(ry * 0.1)),
    ]
    # Shadow offset (use dim amber, not UV purple — contrast against dark BG)
    sh = [(x+2, y+4) for x, y in pts]
    d.polygon(sh, fill=CORRUPT_AMB_SH)
    # Main side body fill: dark amber shadow (CORRUPT_AMB_SH)
    d.polygon(pts, fill=CORRUPT_AMB_SH)
    # Lit central stripe (narrower, clearly distinct from shadow)
    stripe_x = cx + rx_side // 4
    d.polygon([pts[0], (stripe_x, cy), pts[2]], fill=CORRUPT_AMB)
    # Void Black divider lines between lit stripe and shadow areas
    d.line([pts[0], (stripe_x, cy)], fill=LINE, width=2)
    d.line([(stripe_x, cy), pts[2]], fill=LINE, width=2)
    # Silhouette outline
    d.polygon(pts, outline=LINE, width=3)
    # Top spike still visible at side
    d.line([(cx - 2, cy - ry), (cx + 2, cy - ry - 18)], fill=HOT_MAG, width=2)


def draw_body_back(d, cx, cy, rx, ry):
    """BACK view — full diamond, no face, scar lines on back surface.
    v002: base fill changed from UV_PURPLE to CORRUPT_AMB_SH (dark amber).
    HOT_MAG scar lines now have adequate contrast against amber base.
    UV_PURPLE structural line retained as secondary detail only.
    """
    pts = diamond_pts_2d(cx, cy, rx, ry)
    # Shadow offset (dark amber — visible against dark canvas)
    sh = [(x+3, y+4) for x, y in pts]
    d.polygon(sh, fill=CORRUPT_AMB_SH)
    # Main back body: dark amber (was UV_PURPLE — invisible against canvas)
    d.polygon(pts, fill=CORRUPT_AMB_SH)
    # Back highlight (dim amber lit area — right facet)
    top, right, bot, left = pts
    ctr = (cx, cy - ry // 4)
    d.polygon([top, ctr, right], fill=CORRUPT_AMB)
    d.polygon(pts, outline=LINE, width=3)
    # Back-surface scar marks (corruption internal structure)
    d.line([(cx + rx//3, cy - ry//2), (cx - rx//4, cy + ry//2)],
           fill=HOT_MAG, width=2)
    # UV_PURPLE secondary structural line (now reads as detail, not competing)
    d.line([(cx - rx//3, cy - ry//3), (cx + rx//5, cy + ry//4)],
           fill=UV_PURPLE, width=1)


def draw_spikes_front(d, cx, cy_top, cy_bot, rx, spike_top=18, spike_bot=12):
    """Top and bottom spikes for FRONT view."""
    # Top spike
    top_pts = [
        (cx - spike_top//2, cy_top),
        (cx - spike_top,    cy_top - spike_top),
        (cx,                cy_top - spike_top*2),
        (cx + spike_top,    cy_top - spike_top),
        (cx + spike_top//2, cy_top),
    ]
    d.polygon(top_pts, fill=CORRUPT_AMB)
    d.polygon(top_pts, outline=LINE, width=2)
    d.line([(cx, cy_top - spike_top*2), (cx, cy_top - spike_top*2 - 6)],
           fill=HOT_MAG, width=2)
    # Bottom spike
    bot_pts = [
        (cx - spike_bot//2, cy_bot),
        (cx + spike_bot//2, cy_bot),
        (cx,                cy_bot + spike_bot + 4),
    ]
    d.polygon(bot_pts, fill=CORRUPT_AMB_SH)
    d.polygon(bot_pts, outline=LINE, width=2)


def draw_arms_front(d, cx, cy, rx):
    """Left and right arm-spikes FRONT view — neutral position."""
    # Left arm
    la_pts = [(cx - rx - 4, cy - 4),
              (cx - rx - 4, cy + 4),
              (cx - rx - 20, cy - 6)]
    d.polygon(la_pts, fill=CORRUPT_AMB)
    d.polygon(la_pts, outline=LINE, width=2)
    # Right arm
    ra_pts = [(cx + rx + 4, cy - 4),
              (cx + rx + 4, cy + 4),
              (cx + rx + 20, cy - 6)]
    d.polygon(ra_pts, fill=CORRUPT_AMB)
    d.polygon(ra_pts, outline=LINE, width=2)


def draw_face_front(d, cx, cy, ry):
    """FRONT view face: dual pixel eyes + neutral mouth."""
    face_cy = cy - ry // 6
    cell = 6
    # Left eye glyph: neutral cross
    NEUTRAL = [[0, 2, 0], [2, 1, 2], [0, 2, 0]]
    PIXEL_COLORS = {0: VOID_BLACK, 1: CORRUPT_AMB_SH, 2: CORRUPT_AMB, 3: SOFT_GOLD}
    leye_x = cx - 22
    leye_y = face_cy - cell*3//2
    for row in range(3):
        for col in range(3):
            c = PIXEL_COLORS[NEUTRAL[row][col]]
            d.rectangle([leye_x + col*cell, leye_y + row*cell,
                          leye_x + col*cell + cell-1, leye_y + row*cell + cell-1], fill=c)
    # Right eye glyph: destabilized
    DESTAB = [[1, 2, 0], [2, 0, 1], [0, 2, 1]]
    reye_x = cx + 4
    reye_y = face_cy - cell*3//2
    for row in range(3):
        for col in range(3):
            c = PIXEL_COLORS.get(DESTAB[row][col], VOID_BLACK)
            d.rectangle([reye_x + col*cell, reye_y + row*cell,
                          reye_x + col*cell + cell-1, reye_y + row*cell + cell-1], fill=c)
    # Mouth: 3 dim pixel dots
    mouth_y = face_cy + cell*3//2 + 6
    for i in range(3):
        d.rectangle([cx - 8 + i*6, mouth_y, cx - 6 + i*6, mouth_y + 2],
                    fill=CORRUPT_AMB_SH)
    # Brow lines (dim, flat)
    d.line([(leye_x, leye_y - 3), (leye_x + cell*3 - 1, leye_y - 3)],
           fill=CORRUPT_AMB_SH, width=1)
    d.line([(reye_x, reye_y - 3), (reye_x + cell*3 - 1, reye_y - 3)],
           fill=CORRUPT_AMB_SH, width=1)


def draw_hover_confetti_view(d, cx, cy_bot, seed=5):
    """Hot Magenta/UV Purple confetti beneath Glitch."""
    import random
    rng = random.Random(seed)
    cols = [HOT_MAG, UV_PURPLE, VOID_BLACK, HOT_MAG]
    for _ in range(10):
        px = rng.randint(cx - 28, cx + 28)
        py = rng.randint(cy_bot + 2, cy_bot + 16)
        sz = rng.choice([2, 3])
        d.rectangle([px, py, px+sz, py+sz], fill=rng.choice(cols))


def render_view(d, view_idx, base_cx, base_cy, rx=38, ry=42):  # ry > rx: spec §2.1
    """Render one view of Glitch at (base_cx, base_cy)."""
    view = VIEWS[view_idx]
    cy_top = base_cy - ry
    cy_bot = base_cy + int(ry * 1.1) + 6
    cy_spike_bot = cy_bot

    # Hover confetti (always present)
    draw_hover_confetti_view(d, base_cx, cy_spike_bot, seed=view_idx + 3)

    # Bottom spike
    bot_pts = [
        (base_cx - 8, cy_spike_bot),
        (base_cx + 8, cy_spike_bot),
        (base_cx, cy_spike_bot + 14),
    ]
    d.polygon(bot_pts, fill=CORRUPT_AMB_SH)
    d.polygon(bot_pts, outline=LINE, width=2)

    if view == "FRONT":
        draw_body_front(d, base_cx, base_cy, rx, ry)
        draw_spikes_front(d, base_cx, cy_top, cy_spike_bot, rx)
        draw_arms_front(d, base_cx, base_cy, rx)
        draw_face_front(d, base_cx, base_cy, ry)

    elif view == "3/4":
        draw_body_threequarter(d, base_cx, base_cy, rx, ry)
        # Top spike slightly offset (3/4 perspective)
        top_pts = [
            (base_cx - 7, cy_top),
            (base_cx - 14, cy_top - 16),
            (base_cx + 2, cy_top - 34),
            (base_cx + 14, cy_top - 16),
            (base_cx + 7, cy_top),
        ]
        d.polygon(top_pts, fill=CORRUPT_AMB)
        d.polygon(top_pts, outline=LINE, width=2)
        d.line([(base_cx + 2, cy_top - 34), (base_cx + 4, cy_top - 40)],
               fill=HOT_MAG, width=2)
        # Arms: near arm extended, far arm compact
        ra_pts = [(base_cx + rx + 4, base_cy - 4),
                  (base_cx + rx + 4, base_cy + 4),
                  (base_cx + rx + 22, base_cy - 6)]
        d.polygon(ra_pts, fill=CORRUPT_AMB)
        d.polygon(ra_pts, outline=LINE, width=2)
        fa_pts = [(base_cx - int(rx*0.55) - 4, base_cy - 3),
                  (base_cx - int(rx*0.55) - 4, base_cy + 3),
                  (base_cx - int(rx*0.55) - 14, base_cy - 4)]
        d.polygon(fa_pts, fill=CORRUPT_AMB_SH)
        d.polygon(fa_pts, outline=LINE, width=2)
        # Face (near-front, slightly offset)
        face_cy = base_cy - ry // 6
        cell = 5
        NEUTRAL = [[0, 2, 0], [2, 1, 2], [0, 2, 0]]
        PIXEL_COLORS = {0: VOID_BLACK, 1: CORRUPT_AMB_SH, 2: CORRUPT_AMB, 3: SOFT_GOLD}
        leye_x = base_cx - 8
        leye_y = face_cy - cell*3//2
        for row in range(3):
            for col in range(3):
                c = PIXEL_COLORS[NEUTRAL[row][col]]
                d.rectangle([leye_x + col*cell, leye_y + row*cell,
                              leye_x + col*cell + cell-1, leye_y + row*cell + cell-1], fill=c)
        mouth_y = face_cy + cell*3//2 + 4
        for i in range(3):
            d.rectangle([base_cx + i*5 - 7, mouth_y,
                          base_cx + i*5 - 5, mouth_y + 2], fill=CORRUPT_AMB_SH)

    elif view == "SIDE":
        draw_body_side(d, base_cx, base_cy, rx, ry)
        # Top spike — side profile (thin)
        d.polygon([(base_cx - 5, cy_top),
                   (base_cx + 5, cy_top),
                   (base_cx, cy_top - 34)],
                  fill=CORRUPT_AMB)
        d.polygon([(base_cx - 5, cy_top),
                   (base_cx + 5, cy_top),
                   (base_cx, cy_top - 34)],
                  outline=LINE, width=2)
        d.line([(base_cx, cy_top - 34), (base_cx, cy_top - 40)],
               fill=HOT_MAG, width=2)
        # Single arm silhouette (near arm only at side)
        rx_side = int(rx * 0.4)
        d.polygon([(base_cx + rx_side + 2, base_cy - 3),
                   (base_cx + rx_side + 2, base_cy + 3),
                   (base_cx + rx_side + 14, base_cy - 4)],
                  fill=CORRUPT_AMB)
        d.polygon([(base_cx + rx_side + 2, base_cy - 3),
                   (base_cx + rx_side + 2, base_cy + 3),
                   (base_cx + rx_side + 14, base_cy - 4)],
                  outline=LINE, width=2)

    elif view == "BACK":
        draw_body_back(d, base_cx, base_cy, rx, ry)
        # Top spike back
        top_pts = [
            (base_cx - 9, cy_top),
            (base_cx - 16, cy_top - 16),
            (base_cx,     cy_top - 34),
            (base_cx + 16, cy_top - 16),
            (base_cx + 9, cy_top),
        ]
        d.polygon(top_pts, fill=CORRUPT_AMB_SH)
        d.polygon(top_pts, outline=LINE, width=2)
        # Arms (back — reversed)
        la_back = [(base_cx - rx - 4, base_cy - 4),
                   (base_cx - rx - 4, base_cy + 4),
                   (base_cx - rx - 20, base_cy - 6)]
        d.polygon(la_back, fill=CORRUPT_AMB_SH)
        d.polygon(la_back, outline=LINE, width=2)
        ra_back = [(base_cx + rx + 4, base_cy - 4),
                   (base_cx + rx + 4, base_cy + 4),
                   (base_cx + rx + 20, base_cy - 6)]
        d.polygon(ra_back, fill=CORRUPT_AMB_SH)
        d.polygon(ra_back, outline=LINE, width=2)


def build_turnaround():
    """Render 4-view turnaround at 2x, downsample to 1x."""
    W2 = CANVAS_W * SCALE
    H2 = CANVAS_H * SCALE
    PW2 = PANEL_W * SCALE
    PH2 = PANEL_H * SCALE
    HEADER_H2 = HEADER_H * SCALE
    LABEL_H2  = LABEL_H * SCALE

    img = Image.new("RGB", (W2, H2), CANVAS_BG)
    draw = ImageDraw.Draw(img)

    try:
        font_title = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22 * SCALE)
        font_label = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 10 * SCALE)
        font_small = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 7 * SCALE)
    except Exception:
        font_title = ImageFont.load_default()
        font_label = ImageFont.load_default()
        font_small = font_label

    # Header bar
    draw.rectangle([0, 0, W2, HEADER_H2], fill=HEADER_BG)
    title = "GLITCH — Character Turnaround v002  [Shadow Contrast Fix]"
    try:
        tb = draw.textbbox((0, 0), title, font=font_title)
        tw = tb[2] - tb[0]; th = tb[3] - tb[1]
    except Exception:
        tw, th = len(title) * 14 * SCALE, 22 * SCALE
    draw.text(((W2 - tw) // 2, (HEADER_H2 - th) // 2),
              title, fill=CORRUPT_AMB, font=font_title)

    sub = "Antagonist  |  GL-07 Corrupt Amber  |  Cycle 24  |  4-View  |  Shadow contrast fix: SIDE/BACK facets"
    try:
        sb = draw.textbbox((0, 0), sub, font=font_small)
        sw = sb[2] - sb[0]
        draw.text(((W2 - sw) // 2, HEADER_H2 - 14 * SCALE),
                  sub, fill=(100, 60, 30), font=font_small)
    except Exception:
        pass

    # Panels
    rx_1x = 38  # horizontal half-extent (ry > rx: body taller than wide — spec §2.1)
    ry_1x = 42  # vertical half-extent

    for vi, view in enumerate(VIEWS):
        px = vi * PW2
        py = HEADER_H2
        draw.rectangle([px, py, px + PW2, py + PH2], fill=PANEL_BG)
        # Panel border
        draw.rectangle([px, py, px + PW2, py + PH2 - 1],
                       outline=(40, 28, 50), width=1)

        # Character position: centered horizontally, base at ~78% of panel height
        char_cx = px + PW2 // 2
        char_cy = py + int(PH2 * 0.50)

        # Scale geometry to 2x
        render_view(draw, vi, char_cx, char_cy,
                    rx=rx_1x * SCALE, ry=ry_1x * SCALE)

        # HU ruler line (subtle) — single height mark at character top
        char_top_y = char_cy - ry_1x * SCALE - 40 * SCALE
        char_bot_y = char_cy + int(ry_1x * SCALE * 1.1) + 14 * SCALE + 16 * SCALE
        ru_x = px + PW2 - 18 * SCALE
        draw.line([(ru_x, char_top_y), (ru_x, char_bot_y)],
                  fill=HU_LINE_COL, width=1)
        draw.line([(ru_x - 4 * SCALE, char_top_y),
                   (ru_x + 4 * SCALE, char_top_y)],
                  fill=HU_LINE_COL, width=1)
        draw.line([(ru_x - 4 * SCALE, char_bot_y),
                   (ru_x + 4 * SCALE, char_bot_y)],
                  fill=HU_LINE_COL, width=1)

        # View label in bottom bar
        label_y = py + PH2 + 6 * SCALE
        try:
            lb = draw.textbbox((0, 0), view, font=font_label)
            lw = lb[2] - lb[0]
        except Exception:
            lw = len(view) * 8 * SCALE
        draw.text((px + (PW2 - lw) // 2, label_y),
                  view, fill=LABEL_COL, font=font_label)

    # Bottom label bar background
    label_bar_y = HEADER_H2 + PH2
    draw.rectangle([0, label_bar_y, W2, H2], fill=HEADER_BG)

    # Downsample
    img_out = img.resize((CANVAS_W, CANVAS_H), Image.LANCZOS)
    return img_out


def main():
    out_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "characters", "main", "turnarounds"
    )
    os.makedirs(out_dir, exist_ok=True)

    turnaround = build_turnaround()
    out_path = os.path.join(out_dir, "LTG_CHAR_glitch_turnaround_v002.png")
    turnaround.save(out_path)
    print(f"Saved: {out_path}")
    print(f"  Size: {turnaround.size[0]}x{turnaround.size[1]}px")
    print("  Views: FRONT, 3/4, SIDE, BACK")
    print("  v002: Shadow contrast fix — SIDE/BACK facets use CORRUPT_AMB_SH not UV_PURPLE")


if __name__ == "__main__":
    main()
