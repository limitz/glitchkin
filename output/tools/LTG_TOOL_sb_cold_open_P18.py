#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_sb_cold_open_P18.py
Cold Open Panel P18 — CU / INSERT — Notebook Doodles
Diego Vargas, Storyboard Artist — Cycle 46

Beat: Luma's notebook page with doodle drawings of the face she saw in the CRT static.
      This is the bridge from THE NOTICING to COMMITMENT — she is processing what she saw.
      The notebook is her method: she doesn't react with wonder or fear, she draws.
      The doodles are crude but accurate — shapes suspiciously Glitchkin-like. Two eyes
      (one round, one cracked), a teardrop body, pixel squares. She has been noticing
      for longer than tonight.

      Context from Priya's beat outline: P18 is where curiosity replaces fear. Luma shows
      Byte her notebook margin doodles. The notebook establishes Luma's processing method —
      she draws what she sees, what she half-sees, what she suspects.

Camera: CU or INSERT on the notebook page itself. The notebook fills the frame.
        Luma's hand visible at bottom edge (holding the notebook open / pointing).
        Warm ambient light from the den — the page is lit warmly.
        No full character staging — this is a PROP SHOT.

Key staging:
  - Notebook page fills 85%+ of the draw area
  - Ruled lines visible (standard composition notebook)
  - Multiple doodles scattered across the page:
    * Central doodle: a face with two eyes — one round, one with crack lines (Byte)
    * Smaller doodles: teardrop shapes, pixel squares, static-like scribbles
    * Margin doodles: older, lighter, from previous pages bleeding through
    * One doodle circled with an arrow pointing to it (Luma annotating her own notes)
  - Luma's hand and hoodie cuff visible bottom-left (canonical orange)
  - Pencil visible on the page (prop continuity)
  - Warm paper color under warm ambient light
  - Faint cyan cast on the page from CRT monitor glow (still present in the room)

Arc: CURIOUS / PROCESSING (ELEC_CYAN border — she is working through it, not frozen).

Image size rule: <= 1280px both dimensions.
Output: output/storyboards/panels/LTG_SB_cold_open_P18.png
"""

from PIL import Image, ImageDraw, ImageFont
import math, random, os

PANELS_DIR  = "/home/wipkat/team/output/storyboards/panels"
OUTPUT_PATH = os.path.join(PANELS_DIR, "LTG_SB_cold_open_P18.png")
os.makedirs(PANELS_DIR, exist_ok=True)

PW, PH    = 800, 600
CAPTION_H = 72
DRAW_H    = PH - CAPTION_H   # 528

# ── Palette ──────────────────────────────────────────────────────────────────
WARM_CREAM    = (250, 240, 220)
SUNLIT_AMB    = (212, 146, 58)
VOID_BLACK    = (10, 10, 20)
ELEC_CYAN     = (0, 212, 232)
ELEC_CYAN_DIM = (0, 100, 120)
HOT_MAGENTA   = (232, 0, 152)
LUMA_HOODIE   = (232, 112, 58)   # canonical orange
LUMA_SKIN     = (218, 172, 128)
DEEP_SPACE    = (6, 4, 14)

# Notebook colors
PAPER_WHITE   = (248, 244, 232)    # warm cream paper
PAPER_SHADOW  = (230, 222, 204)    # page shadow/crease area
RULE_LINE     = (180, 200, 220)    # faint blue ruled lines
MARGIN_LINE   = (210, 160, 160)    # red margin line
PENCIL_GRAY   = (80, 72, 60)      # pencil graphite marks (doodles)
PENCIL_LIGHT  = (140, 130, 115)   # lighter pencil (older doodles)
PENCIL_DARK   = (55, 48, 38)      # darker pencil (emphatic marks)
SPIRAL_METAL  = (180, 175, 168)   # spiral binding

# Caption
BG_CAPTION    = (12, 8, 6)
TEXT_SHOT     = (232, 224, 204)
TEXT_DESC     = (155, 148, 122)
TEXT_META     = (88, 82, 66)
ARC_COLOR     = ELEC_CYAN
ANN_COLOR     = (220, 200, 80)
ANN_CYAN      = (0, 180, 210)
ANN_DIM       = (80, 90, 100)

RNG = random.Random(1818)


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


def lerp_color(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def add_glow(img, cx, cy, r_max, color_rgb, steps=6, max_alpha=50):
    """Additive alpha composite glow — never darkens."""
    for i in range(steps, 0, -1):
        r     = int(r_max * (i / steps))
        alpha = int(max_alpha * (1 - (i / steps) * 0.6))
        glow  = Image.new('RGBA', img.size, (0, 0, 0, 0))
        gd    = ImageDraw.Draw(glow)
        gd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(*color_rgb, alpha))
        base  = img.convert('RGBA')
        img.paste(Image.alpha_composite(base, glow).convert('RGB'))


def draw_irregular_poly(draw, cx, cy, r, sides, color, rng, fill=True):
    """Draw a slightly irregular polygon for Glitchkin pixel shapes."""
    pts = []
    for i in range(sides):
        angle = (2 * math.pi * i / sides) + rng.uniform(-0.2, 0.2)
        rr    = r * rng.uniform(0.72, 1.0)
        pts.append((int(cx + rr * math.cos(angle)),
                    int(cy + rr * math.sin(angle))))
    if fill:
        draw.polygon(pts, fill=color)
    else:
        draw.polygon(pts, outline=color)


def draw_byte_doodle(draw, cx, cy, scale, pencil_color, rng, detail=True):
    """Draw a pencil-sketch version of Byte on the notebook page.
    Crude but recognizable: teardrop body, two eyes (one cracked), stubby limbs.
    """
    # Body — teardrop (ellipse top + triangle bottom)
    body_h = int(48 * scale)
    body_w = int(34 * scale)

    # Teardrop outline: upper ellipse
    draw.ellipse([cx - body_w // 2, cy - body_h // 2,
                  cx + body_w // 2, cy + body_h // 6],
                 outline=pencil_color, width=max(1, int(2 * scale)))

    # Lower triangle / taper
    draw.line([(cx - body_w // 2, cy - body_h // 12),
               (cx, cy + body_h // 2)],
              fill=pencil_color, width=max(1, int(2 * scale)))
    draw.line([(cx + body_w // 2, cy - body_h // 12),
               (cx, cy + body_h // 2)],
              fill=pencil_color, width=max(1, int(2 * scale)))

    if detail:
        # Normal eye (left of face in doodle)
        ne_cx = cx - int(8 * scale)
        ne_cy = cy - int(12 * scale)
        ne_r  = int(6 * scale)
        draw.ellipse([ne_cx - ne_r, ne_cy - ne_r, ne_cx + ne_r, ne_cy + ne_r],
                     outline=pencil_color, width=max(1, int(1.5 * scale)))
        # Pupil dot
        draw.ellipse([ne_cx - 2, ne_cy - 2, ne_cx + 2, ne_cy + 2],
                     fill=pencil_color)

        # Cracked eye (right of face in doodle)
        ce_cx = cx + int(8 * scale)
        ce_cy = cy - int(12 * scale)
        ce_r  = int(6 * scale)
        draw.ellipse([ce_cx - ce_r, ce_cy - ce_r, ce_cx + ce_r, ce_cy + ce_r],
                     outline=pencil_color, width=max(1, int(1.5 * scale)))
        # Crack lines radiating from center
        for crack_a in [40, 100, 150]:
            ca = math.radians(crack_a)
            draw.line([(int(ce_cx + ce_r * 0.15 * math.cos(ca)),
                        int(ce_cy + ce_r * 0.15 * math.sin(ca))),
                       (int(ce_cx + ce_r * 0.85 * math.cos(ca)),
                        int(ce_cy + ce_r * 0.85 * math.sin(ca)))],
                      fill=pencil_color, width=1)

        # Mouth — flat grimace (one pixel line)
        mouth_y = cy - int(2 * scale)
        mouth_w = int(10 * scale)
        draw.line([(cx - mouth_w, mouth_y), (cx + mouth_w, mouth_y)],
                  fill=pencil_color, width=max(1, int(1.5 * scale)))

        # Stubby arms
        arm_y = cy - int(4 * scale)
        draw.line([(cx - body_w // 2, arm_y),
                   (cx - body_w // 2 - int(8 * scale), arm_y + int(6 * scale))],
                  fill=pencil_color, width=max(1, int(1.5 * scale)))
        draw.line([(cx + body_w // 2, arm_y),
                   (cx + body_w // 2 + int(8 * scale), arm_y + int(6 * scale))],
                  fill=pencil_color, width=max(1, int(1.5 * scale)))

        # Stubby legs
        leg_y = cy + body_h // 2
        draw.line([(cx - int(6 * scale), leg_y),
                   (cx - int(6 * scale), leg_y + int(8 * scale))],
                  fill=pencil_color, width=max(1, int(1.5 * scale)))
        draw.line([(cx + int(6 * scale), leg_y),
                   (cx + int(6 * scale), leg_y + int(8 * scale))],
                  fill=pencil_color, width=max(1, int(1.5 * scale)))


def draw_pixel_square_doodle(draw, cx, cy, size, pencil_color, rng):
    """Draw a small pixel-square doodle (Glitchkin pixel element)."""
    half = size // 2
    # Slightly wobbly rectangle (hand-drawn look)
    pts = [
        (cx - half + rng.randint(-2, 2), cy - half + rng.randint(-2, 2)),
        (cx + half + rng.randint(-2, 2), cy - half + rng.randint(-2, 2)),
        (cx + half + rng.randint(-2, 2), cy + half + rng.randint(-2, 2)),
        (cx - half + rng.randint(-2, 2), cy + half + rng.randint(-2, 2)),
    ]
    draw.polygon(pts, outline=pencil_color)
    # Inner grid lines (pixel feel)
    draw.line([(pts[0][0] + size // 3, pts[0][1]),
               (pts[3][0] + size // 3, pts[3][1])],
              fill=pencil_color, width=1)


def draw_static_scribble(draw, cx, cy, w, h, pencil_color, rng):
    """Draw a small patch of 'CRT static' scribbles — short horizontal dashes."""
    for _ in range(int(w * h / 40)):
        sx = cx + rng.randint(-w // 2, w // 2)
        sy = cy + rng.randint(-h // 2, h // 2)
        sl = rng.randint(2, 8)
        draw.line([(sx, sy), (sx + sl, sy)], fill=pencil_color, width=1)


def draw_panel():
    img  = Image.new('RGB', (PW, PH), DEEP_SPACE)
    draw = ImageDraw.Draw(img)

    # ── Notebook page fills the frame ────────────────────────────────────────
    # Page area — slightly inset from edges with slight rotation feel
    page_left   = 38
    page_top    = 18
    page_right  = PW - 22
    page_bottom = DRAW_H - 14
    page_w = page_right - page_left
    page_h = page_bottom - page_top

    # Page shadow (slight 3D effect — page is angled toward camera)
    draw.rectangle([page_left + 4, page_top + 4, page_right + 4, page_bottom + 4],
                   fill=(40, 35, 28))

    # Paper base
    draw.rectangle([page_left, page_top, page_right, page_bottom],
                   fill=PAPER_WHITE)

    # Paper texture — subtle noise grain
    for _ in range(1200):
        gx = RNG.randint(page_left + 2, page_right - 2)
        gy = RNG.randint(page_top + 2, page_bottom - 2)
        gv = RNG.randint(-8, 8)
        gc = tuple(max(0, min(255, PAPER_WHITE[i] + gv)) for i in range(3))
        draw.point((gx, gy), fill=gc)

    # Spiral binding holes along left edge
    spiral_x = page_left + 14
    for sy in range(page_top + 20, page_bottom - 10, 22):
        draw.ellipse([spiral_x - 4, sy - 4, spiral_x + 4, sy + 4],
                     outline=SPIRAL_METAL, width=2)
        # Wire arc
        draw.arc([spiral_x - 8, sy - 6, spiral_x + 8, sy + 6],
                 start=90, end=270, fill=SPIRAL_METAL, width=2)

    # Ruled lines
    rule_start_y = page_top + 56  # first line after top margin
    rule_spacing = 20
    for ry in range(rule_start_y, page_bottom - 10, rule_spacing):
        draw.line([(page_left + 30, ry), (page_right - 8, ry)],
                  fill=RULE_LINE, width=1)

    # Red margin line
    margin_x = page_left + 70
    draw.line([(margin_x, page_top + 8), (margin_x, page_bottom - 6)],
              fill=MARGIN_LINE, width=1)

    # ── Doodles on the page ──────────────────────────────────────────────────

    # --- CENTRAL DOODLE: Byte face (large, detailed) ---
    # This is the main drawing — a clear Byte face with the cracked eye
    central_cx = int(page_left + page_w * 0.50)
    central_cy = int(page_top + page_h * 0.38)
    draw_byte_doodle(draw, central_cx, central_cy, 1.8, PENCIL_DARK, RNG, detail=True)

    # Circle around it with annotation arrow (Luma marking "THIS ONE")
    circle_r = 70
    draw.ellipse([central_cx - circle_r, central_cy - circle_r - 10,
                  central_cx + circle_r, central_cy + circle_r + 10],
                 outline=PENCIL_GRAY, width=2)
    # Arrow from circle to margin note
    arrow_start_x = central_cx + circle_r + 2
    arrow_start_y = central_cy - 20
    arrow_end_x   = central_cx + circle_r + 50
    arrow_end_y   = central_cy - 45
    draw.line([(arrow_start_x, arrow_start_y), (arrow_end_x, arrow_end_y)],
              fill=PENCIL_GRAY, width=2)
    # Arrowhead
    draw.polygon([
        (arrow_end_x, arrow_end_y),
        (arrow_end_x - 8, arrow_end_y + 4),
        (arrow_end_x - 4, arrow_end_y + 8),
    ], fill=PENCIL_GRAY)

    # Handwritten note next to arrow: "this one!! →" (rendered as text)
    font_hw = load_font(10, bold=False)
    draw.text((arrow_end_x + 4, arrow_end_y - 6), "this one!",
              font=font_hw, fill=PENCIL_DARK)

    # --- SMALLER DOODLE: teardrop body (Byte body, less detail) ---
    sm1_cx = int(page_left + page_w * 0.22)
    sm1_cy = int(page_top + page_h * 0.25)
    draw_byte_doodle(draw, sm1_cx, sm1_cy, 0.8, PENCIL_LIGHT, RNG, detail=False)
    # Question mark next to it
    draw.text((sm1_cx + 20, sm1_cy - 18), "?", font=load_font(14, bold=True),
              fill=PENCIL_LIGHT)

    # --- PIXEL SQUARE DOODLES (scattered) ---
    pixel_positions = [
        (int(page_left + page_w * 0.75), int(page_top + page_h * 0.20), 14),
        (int(page_left + page_w * 0.80), int(page_top + page_h * 0.26), 10),
        (int(page_left + page_w * 0.72), int(page_top + page_h * 0.28), 12),
        (int(page_left + page_w * 0.78), int(page_top + page_h * 0.15), 8),
    ]
    for px, py, psz in pixel_positions:
        draw_pixel_square_doodle(draw, px, py, psz, PENCIL_GRAY, RNG)

    # Label near pixel squares: "pixels?? squares?"
    draw.text((int(page_left + page_w * 0.68), int(page_top + page_h * 0.32)),
              "pixels??", font=font_hw, fill=PENCIL_GRAY)

    # --- STATIC SCRIBBLE PATCH (CRT texture attempt) ---
    static_cx = int(page_left + page_w * 0.30)
    static_cy = int(page_top + page_h * 0.62)
    # Small rectangle representing the CRT screen
    scr_w, scr_h = 60, 44
    draw.rectangle([static_cx - scr_w, static_cy - scr_h,
                    static_cx + scr_w, static_cy + scr_h],
                   outline=PENCIL_GRAY, width=2)
    # Antenna stubs on top
    draw.line([(static_cx - 15, static_cy - scr_h),
               (static_cx - 25, static_cy - scr_h - 20)],
              fill=PENCIL_GRAY, width=2)
    draw.line([(static_cx + 15, static_cy - scr_h),
               (static_cx + 25, static_cy - scr_h - 20)],
              fill=PENCIL_GRAY, width=2)
    # Static texture inside the screen doodle
    draw_static_scribble(draw, static_cx, static_cy,
                         scr_w * 2 - 12, scr_h * 2 - 12, PENCIL_LIGHT, RNG)
    # Small face in the static (the face she saw)
    # Just two dots for eyes and a flat line for mouth
    draw.ellipse([static_cx - 10, static_cy - 6, static_cx - 4, static_cy + 0],
                 outline=PENCIL_DARK, width=1)
    draw.ellipse([static_cx + 4, static_cy - 6, static_cx + 10, static_cy + 0],
                 outline=PENCIL_DARK, width=1)
    # Crack lines on right eye
    draw.line([(static_cx + 7, static_cy - 5), (static_cx + 12, static_cy - 9)],
              fill=PENCIL_DARK, width=1)
    draw.line([(static_cx + 7, static_cy - 2), (static_cx + 13, static_cy + 2)],
              fill=PENCIL_DARK, width=1)
    # Flat mouth
    draw.line([(static_cx - 6, static_cy + 6), (static_cx + 6, static_cy + 6)],
              fill=PENCIL_DARK, width=1)
    # Label under CRT doodle
    draw.text((static_cx - scr_w + 4, static_cy + scr_h + 4),
              "face in the static", font=font_hw, fill=PENCIL_GRAY)

    # --- MARGIN DOODLES (older, lighter — bleeding through from previous thinking) ---
    # These are in the left margin area, before the margin line
    # Small teardrop shapes and eye symbols
    for my_offset in range(3):
        mdy = int(page_top + page_h * (0.45 + my_offset * 0.12))
        mdx = page_left + 48
        # Tiny eye
        draw.ellipse([mdx - 5, mdy - 3, mdx + 5, mdy + 3],
                     outline=PENCIL_LIGHT, width=1)
        draw.ellipse([mdx - 1, mdy - 1, mdx + 1, mdy + 1],
                     fill=PENCIL_LIGHT)

    # A couple of older teardrop shapes in the upper margin
    for mt_i, (mt_x, mt_y) in enumerate([
        (page_left + 50, page_top + page_h * 0.15),
        (page_left + 44, page_top + page_h * 0.80),
    ]):
        mt_x, mt_y = int(mt_x), int(mt_y)
        # Small teardrop
        draw.ellipse([mt_x - 6, mt_y - 8, mt_x + 6, mt_y - 1],
                     outline=PENCIL_LIGHT, width=1)
        draw.line([(mt_x - 6, mt_y - 4), (mt_x, mt_y + 6)],
                  fill=PENCIL_LIGHT, width=1)
        draw.line([(mt_x + 6, mt_y - 4), (mt_x, mt_y + 6)],
                  fill=PENCIL_LIGHT, width=1)

    # --- BOTTOM RIGHT: another Byte sketch with "2 eyes - 1 broken?" ---
    br_cx = int(page_left + page_w * 0.70)
    br_cy = int(page_top + page_h * 0.70)
    # Just the face portion (two eyes, one cracked)
    br_r = 18
    draw.ellipse([br_cx - br_r, br_cy - br_r, br_cx + br_r, br_cy + br_r],
                 outline=PENCIL_GRAY, width=2)
    # Left eye (normal)
    draw.ellipse([br_cx - 10, br_cy - 6, br_cx - 2, br_cy + 2],
                 outline=PENCIL_GRAY, width=1)
    draw.ellipse([br_cx - 7, br_cy - 3, br_cx - 5, br_cy - 1],
                 fill=PENCIL_GRAY)
    # Right eye (cracked)
    draw.ellipse([br_cx + 2, br_cy - 6, br_cx + 10, br_cy + 2],
                 outline=PENCIL_GRAY, width=1)
    draw.line([(br_cx + 6, br_cy - 5), (br_cx + 12, br_cy - 9)],
              fill=PENCIL_GRAY, width=1)
    draw.line([(br_cx + 6, br_cy - 1), (br_cx + 13, br_cy + 3)],
              fill=PENCIL_GRAY, width=1)
    # Annotation
    draw.text((br_cx - br_r, br_cy + br_r + 4),
              "2 eyes - 1 broken?", font=font_hw, fill=PENCIL_GRAY)

    # --- Written notes (Luma's handwriting — observations) ---
    font_hw_sm = load_font(9, bold=False)
    notes = [
        (int(page_left + page_w * 0.35), int(page_top + page_h * 0.14),
         "saw it again tonight"),
        (int(page_left + page_w * 0.35), int(page_top + page_h * 0.51),
         "not random. it LOOKED at me."),
        (int(page_left + page_w * 0.50), int(page_top + page_h * 0.84),
         "grumpy. definitely grumpy."),
    ]
    for nx, ny, txt in notes:
        draw.text((nx, ny), txt, font=font_hw_sm, fill=PENCIL_GRAY)

    # Underline "LOOKED" for emphasis
    draw.line([(int(page_left + page_w * 0.35) + 68, int(page_top + page_h * 0.51) + 11),
               (int(page_left + page_w * 0.35) + 120, int(page_top + page_h * 0.51) + 11)],
              fill=PENCIL_DARK, width=2)

    # ── Luma's hand visible at bottom-left ───────────────────────────────────
    # Hoodie cuff + hand holding the notebook open
    hand_y = page_bottom - 8
    hand_x = page_left + 60

    # Hoodie cuff (CANONICAL ORANGE)
    draw.rectangle([hand_x - 40, hand_y, hand_x + 30, hand_y + 28],
                   fill=LUMA_HOODIE)
    # Cuff ribbing
    for cx_rib in range(hand_x - 38, hand_x + 28, 4):
        draw.line([(cx_rib, hand_y), (cx_rib, hand_y + 28)],
                  fill=lerp_color(LUMA_HOODIE, (180, 80, 38), 0.3), width=1)

    # Hand (fingers pressing the page open)
    # Thumb
    draw.ellipse([hand_x + 30, hand_y - 6, hand_x + 46, hand_y + 10],
                 fill=LUMA_SKIN)
    # Fingers curving onto page
    for fi in range(4):
        fx = hand_x + 50 + fi * 12
        draw.ellipse([fx, hand_y - 4, fx + 10, hand_y + 8],
                     fill=LUMA_SKIN)

    # Pencil on the page (diagonal, resting)
    pencil_x1 = int(page_left + page_w * 0.55)
    pencil_y1 = int(page_top + page_h * 0.88)
    pencil_x2 = pencil_x1 + 80
    pencil_y2 = pencil_y1 - 14
    # Body
    draw.line([(pencil_x1, pencil_y1), (pencil_x2, pencil_y2)],
              fill=(220, 195, 50), width=5)  # yellow pencil body
    # Tip
    draw.line([(pencil_x1 - 6, pencil_y1 + 1), (pencil_x1, pencil_y1)],
              fill=PENCIL_DARK, width=3)
    # Eraser end
    draw.ellipse([pencil_x2 - 2, pencil_y2 - 4, pencil_x2 + 6, pencil_y2 + 4],
                 fill=(210, 140, 140))
    # Metal ferrule
    draw.line([(pencil_x2 - 4, pencil_y2 - 3), (pencil_x2, pencil_y2 - 2)],
              fill=SPIRAL_METAL, width=3)

    # ── Faint cyan cast from CRT monitor glow ────────────────────────────────
    add_glow(img, PW - 40, int(DRAW_H * 0.30), int(PW * 0.45),
             ELEC_CYAN, steps=6, max_alpha=10)
    draw = ImageDraw.Draw(img)

    # Warm ambient glow (den lamp, camera-left)
    add_glow(img, -30, int(DRAW_H * 0.20), int(PW * 0.50),
             SUNLIT_AMB, steps=8, max_alpha=14)
    draw = ImageDraw.Draw(img)

    # ── Annotations ──────────────────────────────────────────────────────────
    font_ann  = load_font(9,  bold=False)
    font_ann_b = load_font(9, bold=True)
    font_sm   = load_font(8,  bold=False)

    # Camera note
    draw.text((8, 8), 'CU / INSERT  |  NOTEBOOK PAGE  |  PROCESSING BEAT',
              font=font_ann, fill=ANN_COLOR)

    # Annotation: she has been drawing these before tonight
    draw.text((page_left + 34, page_top + page_h * 0.45 - 4),
              "← older doodles (margin)", font=font_sm, fill=ANN_DIM)

    # Annotation: the central doodle is the key
    draw.text((central_cx - circle_r - 10, central_cy + circle_r + 14),
              "HERO DOODLE: Byte's face", font=font_ann_b, fill=ANN_CYAN)
    draw.text((central_cx - circle_r - 10, central_cy + circle_r + 26),
              "(she drew it before she knew what it was)", font=font_sm, fill=ANN_DIM)

    # Annotation: CRT doodle
    draw.text((static_cx + scr_w + 8, static_cy - 12),
              "CRT with face in static", font=font_sm, fill=ANN_DIM)

    # ── Three-tier caption bar ────────────────────────────────────────────────
    font_t1   = load_font(13, bold=True)
    font_t2   = load_font(11, bold=False)
    font_t3   = load_font(9,  bold=False)
    font_meta = load_font(8,  bold=False)

    draw.rectangle([0, DRAW_H, PW, PH], fill=BG_CAPTION)
    draw.line([0, DRAW_H, PW, DRAW_H], fill=(8, 6, 4), width=2)

    # Tier 1 — Shot code
    draw.text((10, DRAW_H + 4),
              "P18  |  CU / INSERT  |  NOTEBOOK DOODLES  |  PROCESSING BEAT",
              font=font_t1, fill=TEXT_SHOT)

    # Tier 2 — Arc label
    draw.text((PW - 220, DRAW_H + 5),
              "ARC: CURIOUS / PROCESSING", font=font_t2, fill=ELEC_CYAN)

    # Tier 3 — Narrative description
    draw.text((10, DRAW_H + 22),
              "Luma's notebook page with doodle drawings of the face she saw in the CRT static.",
              font=font_t3, fill=TEXT_DESC)
    draw.text((10, DRAW_H + 35),
              "She drew it before she knew what it was. Bridges THE NOTICING to COMMITMENT.",
              font=font_t3, fill=(120, 112, 90))

    # Metadata
    draw.text((PW - 276, DRAW_H + 56),
              "LTG_SB_cold_open_P18  /  Diego Vargas  /  C46",
              font=font_meta, fill=TEXT_META)

    # Arc border — ELEC_CYAN (CURIOUS / PROCESSING)
    draw.rectangle([0, 0, PW - 1, PH - 1], outline=ARC_COLOR, width=4)

    img.thumbnail((1280, 1280))
    img.save(OUTPUT_PATH, "PNG")
    print(f"Saved: {OUTPUT_PATH}  {img.size}")
    return OUTPUT_PATH


if __name__ == "__main__":
    draw_panel()
    print("P18 standalone panel generation complete.")
    print("Beat: Luma's notebook page — doodle drawings of the face in the CRT static.")
    print("She has been noticing for longer than tonight. Bridges THE NOTICING → COMMITMENT.")
    print("ELEC_CYAN border. CU/INSERT on notebook prop.")
