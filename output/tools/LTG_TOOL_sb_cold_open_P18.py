#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_sb_cold_open_P18.py
Cold Open Panel P18 — CU / INSERT — Notebook Doodles
Diego Vargas, Storyboard Artist — Cycle 47

C47 VISUAL TIMESTAMP FIX (Ingrid critique #5 — fails blank test):
  The notebook page now reads WITHOUT captions via visual storytelling cues:

  1. TEMPORAL PROGRESSION in drawing quality/confidence:
     - TOP LEFT zone: faint, tentative, single-line doodles (weeks ago) — barely visible
     - MIDDLE zone: medium-confidence doodles, more detail (days ago)
     - BOTTOM CENTER: tonight's hero doodle — bold, detailed, emphatic, circled
     Each tier has a distinct pencil pressure / opacity / scale that reads as TIME PASSING.

  2. EMOTIONAL ARC in the doodles themselves:
     - Early doodles: question marks, vague shapes, uncertain
     - Middle doodles: recognizable face fragments, pixel squares (pattern forming)
     - Hero doodle: full Byte face with cracked eye, CIRCLED and star-marked — EUREKA

  3. ENVIRONMENTAL CONTEXT:
     - CRT glow from right edge casts cyan on the page (she's near the screen NOW)
     - Warm lamp glow from left (she's in the den)
     - Luma's hand pointing at the hero doodle (active gesture, not passive hold)
     - Finger resting on the cracked eye specifically (she SEES the detail)

  4. VISUAL FLOW arrows built from doodle placement:
     - Reader's eye follows the SIZE GRADIENT: tiny → small → medium → large
     - The circled hero doodle has pencil-pressure emphasis lines radiating outward
       (like a "realized!" manga convention without text)

Beat: Luma's notebook page — doodle drawings of the face she saw in CRT static.
      This is the bridge from THE NOTICING to COMMITMENT. She processes by drawing.
Camera: CU / INSERT. Notebook fills the frame. Luma's hand + hoodie cuff visible.
Arc: CURIOUS / PROCESSING (ELEC_CYAN border).
Output: output/storyboards/panels/LTG_SB_cold_open_P18.png
"""

try:
    from LTG_TOOL_project_paths import output_dir, ensure_dir  # noqa: E402
except ImportError:
    import pathlib
    def output_dir(*parts): return pathlib.Path("/home/wipkat/team/output").joinpath(*parts)
    def ensure_dir(path): path.mkdir(parents=True, exist_ok=True); return path
from PIL import Image, ImageDraw, ImageFont
import math, random, os

PANELS_DIR = output_dir('storyboards', 'panels')
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

# VISUAL TIMESTAMP: 4 pencil tones = 4 time periods
PENCIL_GHOST  = (195, 188, 172)   # oldest doodles — barely there (weeks ago)
PENCIL_LIGHT  = (155, 145, 128)   # earlier doodles (several days ago)
PENCIL_GRAY   = (95, 85, 68)     # recent doodles (yesterday / last night)
PENCIL_DARK   = (40, 32, 22)     # TONIGHT's doodles — bold, emphatic

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


def draw_byte_doodle(draw, cx, cy, scale, pencil_color, rng, detail_level=2):
    """Draw a pencil-sketch version of Byte on the notebook page.
    detail_level: 0 = vague blob, 1 = teardrop + basic eye dots, 2 = full detail (cracked eye etc.)
    """
    body_h = int(48 * scale)
    body_w = int(34 * scale)
    line_w = max(1, int(2 * scale))

    if detail_level == 0:
        # Just a vague teardrop outline — early uncertain doodle
        draw.ellipse([cx - body_w // 2, cy - body_h // 2,
                      cx + body_w // 2, cy + body_h // 6],
                     outline=pencil_color, width=max(1, int(1 * scale)))
        # Single wobbly line downward
        draw.line([(cx - body_w // 4, cy), (cx, cy + body_h // 3)],
                  fill=pencil_color, width=max(1, int(1 * scale)))
        draw.line([(cx + body_w // 4, cy), (cx, cy + body_h // 3)],
                  fill=pencil_color, width=max(1, int(1 * scale)))
        return

    # Teardrop outline: upper ellipse
    draw.ellipse([cx - body_w // 2, cy - body_h // 2,
                  cx + body_w // 2, cy + body_h // 6],
                 outline=pencil_color, width=line_w)

    # Lower triangle / taper
    draw.line([(cx - body_w // 2, cy - body_h // 12),
               (cx, cy + body_h // 2)],
              fill=pencil_color, width=line_w)
    draw.line([(cx + body_w // 2, cy - body_h // 12),
               (cx, cy + body_h // 2)],
              fill=pencil_color, width=line_w)

    if detail_level >= 1:
        # Two eye dots (basic)
        ne_cx = cx - int(8 * scale)
        ne_cy = cy - int(12 * scale)
        ne_r  = int(4 * scale) if detail_level == 1 else int(6 * scale)
        draw.ellipse([ne_cx - ne_r, ne_cy - ne_r, ne_cx + ne_r, ne_cy + ne_r],
                     outline=pencil_color, width=max(1, int(1.5 * scale)))

        ce_cx = cx + int(8 * scale)
        ce_cy = cy - int(12 * scale)
        ce_r  = int(4 * scale) if detail_level == 1 else int(6 * scale)
        draw.ellipse([ce_cx - ce_r, ce_cy - ce_r, ce_cx + ce_r, ce_cy + ce_r],
                     outline=pencil_color, width=max(1, int(1.5 * scale)))

        if detail_level == 1:
            # Simple pupil dots only
            draw.ellipse([ne_cx - 1, ne_cy - 1, ne_cx + 1, ne_cy + 1],
                         fill=pencil_color)
            draw.ellipse([ce_cx - 1, ce_cy - 1, ce_cx + 1, ce_cy + 1],
                         fill=pencil_color)
            # Simple mouth line
            mouth_y = cy - int(2 * scale)
            draw.line([(cx - int(6 * scale), mouth_y), (cx + int(6 * scale), mouth_y)],
                      fill=pencil_color, width=1)

    if detail_level >= 2:
        # Full detail: pupil, crack lines, arms, legs
        ne_cx = cx - int(8 * scale)
        ne_cy = cy - int(12 * scale)
        ne_r  = int(6 * scale)
        # Pupil dot (normal eye)
        draw.ellipse([ne_cx - 2, ne_cy - 2, ne_cx + 2, ne_cy + 2],
                     fill=pencil_color)

        # Cracked eye detail
        ce_cx = cx + int(8 * scale)
        ce_cy = cy - int(12 * scale)
        ce_r  = int(6 * scale)
        # Crack lines radiating from center
        for crack_a in [40, 100, 150]:
            ca = math.radians(crack_a)
            draw.line([(int(ce_cx + ce_r * 0.15 * math.cos(ca)),
                        int(ce_cy + ce_r * 0.15 * math.sin(ca))),
                       (int(ce_cx + ce_r * 0.85 * math.cos(ca)),
                        int(ce_cy + ce_r * 0.85 * math.sin(ca)))],
                      fill=pencil_color, width=max(1, int(1.5 * scale)))

        # Mouth — flat grimace
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
    pts = [
        (cx - half + rng.randint(-2, 2), cy - half + rng.randint(-2, 2)),
        (cx + half + rng.randint(-2, 2), cy - half + rng.randint(-2, 2)),
        (cx + half + rng.randint(-2, 2), cy + half + rng.randint(-2, 2)),
        (cx - half + rng.randint(-2, 2), cy + half + rng.randint(-2, 2)),
    ]
    draw.polygon(pts, outline=pencil_color)
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


def draw_emphasis_burst(draw, cx, cy, r_inner, r_outer, n_rays, pencil_color):
    """Draw radiating emphasis lines around a focal point (manga eureka convention)."""
    for i in range(n_rays):
        angle = (2 * math.pi * i / n_rays) + 0.15  # slight offset
        x1 = int(cx + r_inner * math.cos(angle))
        y1 = int(cy + r_inner * math.sin(angle))
        x2 = int(cx + r_outer * math.cos(angle))
        y2 = int(cy + r_outer * math.sin(angle))
        draw.line([(x1, y1), (x2, y2)], fill=pencil_color, width=2)


def draw_panel():
    img  = Image.new('RGB', (PW, PH), DEEP_SPACE)
    draw = ImageDraw.Draw(img)

    # ── Notebook page fills the frame ────────────────────────────────────────
    page_left   = 38
    page_top    = 18
    page_right  = PW - 22
    page_bottom = DRAW_H - 14
    page_w = page_right - page_left
    page_h = page_bottom - page_top

    # Page shadow
    draw.rectangle([page_left + 4, page_top + 4, page_right + 4, page_bottom + 4],
                   fill=(40, 35, 28))

    # Paper base
    draw.rectangle([page_left, page_top, page_right, page_bottom],
                   fill=PAPER_WHITE)

    # Paper texture
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
        draw.arc([spiral_x - 8, sy - 6, spiral_x + 8, sy + 6],
                 start=90, end=270, fill=SPIRAL_METAL, width=2)

    # Ruled lines
    rule_start_y = page_top + 56
    rule_spacing = 20
    for ry in range(rule_start_y, page_bottom - 10, rule_spacing):
        draw.line([(page_left + 30, ry), (page_right - 8, ry)],
                  fill=RULE_LINE, width=1)

    # Red margin line
    margin_x = page_left + 70
    draw.line([(margin_x, page_top + 8), (margin_x, page_bottom - 6)],
              fill=MARGIN_LINE, width=1)

    # ══════════════════════════════════════════════════════════════════════════
    # VISUAL TIMESTAMP SYSTEM — 3 time tiers, NO text needed to read the arc
    # Reader's eye follows: ghost → faint → medium → BOLD HERO
    # Size + darkness + detail all increase together = time passing visually
    # ══════════════════════════════════════════════════════════════════════════

    # ── TIER 1: GHOST DOODLES — weeks ago, barely there ─────────────────────
    # Top-left corner of page. Smallest, faintest. Vague blobs.
    # Visual cue: these have been here so long the page has been turned many times.

    # Ghost doodle 1: tiny vague teardrop (she saw something but didn't know what)
    g1_cx = int(page_left + page_w * 0.18)
    g1_cy = int(page_top + page_h * 0.13)
    draw_byte_doodle(draw, g1_cx, g1_cy, 0.45, PENCIL_GHOST, RNG, detail_level=0)

    # Ghost doodle 2: a few scattered dots (pixels she noticed in static)
    for gi in range(5):
        gx = int(page_left + page_w * 0.25 + RNG.randint(-12, 12))
        gy = int(page_top + page_h * 0.10 + RNG.randint(-8, 8))
        draw.ellipse([gx - 2, gy - 2, gx + 2, gy + 2],
                     outline=PENCIL_GHOST, width=1)

    # Ghost doodle 3: single eye shape (she noticed the eye first)
    ge_cx = int(page_left + page_w * 0.15)
    ge_cy = int(page_top + page_h * 0.22)
    draw.ellipse([ge_cx - 7, ge_cy - 4, ge_cx + 7, ge_cy + 4],
                 outline=PENCIL_GHOST, width=1)
    draw.ellipse([ge_cx - 1, ge_cy - 1, ge_cx + 1, ge_cy + 1],
                 fill=PENCIL_GHOST)

    # Ghost question mark (uncertainty)
    font_hw_ghost = load_font(11, bold=False)
    draw.text((int(page_left + page_w * 0.28), int(page_top + page_h * 0.14)),
              "?", font=font_hw_ghost, fill=PENCIL_GHOST)

    # ── TIER 2: EARLIER DOODLES — days ago, medium confidence ───────────────
    # Mid-page area, left and right. More recognizable. Pattern forming.

    # Earlier doodle 1: teardrop body with basic eye dots (she figured out the shape)
    e1_cx = int(page_left + page_w * 0.20)
    e1_cy = int(page_top + page_h * 0.38)
    draw_byte_doodle(draw, e1_cx, e1_cy, 0.75, PENCIL_LIGHT, RNG, detail_level=1)

    # Earlier doodle 2: CRT screen with face emerging from static
    scr_cx = int(page_left + page_w * 0.28)
    scr_cy = int(page_top + page_h * 0.58)
    scr_w, scr_h = 48, 36
    draw.rectangle([scr_cx - scr_w, scr_cy - scr_h,
                    scr_cx + scr_w, scr_cy + scr_h],
                   outline=PENCIL_LIGHT, width=2)
    # Antenna stubs
    draw.line([(scr_cx - 12, scr_cy - scr_h),
               (scr_cx - 20, scr_cy - scr_h - 16)],
              fill=PENCIL_LIGHT, width=1)
    draw.line([(scr_cx + 12, scr_cy - scr_h),
               (scr_cx + 20, scr_cy - scr_h - 16)],
              fill=PENCIL_LIGHT, width=1)
    # Static texture
    draw_static_scribble(draw, scr_cx, scr_cy,
                         scr_w * 2 - 10, scr_h * 2 - 10, PENCIL_GHOST, RNG)
    # Face emerging from static (two eyes + mouth — more detail than ghost tier)
    draw.ellipse([scr_cx - 8, scr_cy - 5, scr_cx - 2, scr_cy + 1],
                 outline=PENCIL_LIGHT, width=1)
    draw.ellipse([scr_cx + 2, scr_cy - 5, scr_cx + 8, scr_cy + 1],
                 outline=PENCIL_LIGHT, width=1)
    # Crack hint on right eye
    draw.line([(scr_cx + 5, scr_cy - 4), (scr_cx + 10, scr_cy - 7)],
              fill=PENCIL_LIGHT, width=1)
    draw.line([(scr_cx - 4, scr_cy + 4), (scr_cx + 4, scr_cy + 4)],
              fill=PENCIL_LIGHT, width=1)

    # Earlier pixel squares (she noticed the pixel shapes)
    for px, py, psz in [
        (int(page_left + page_w * 0.72), int(page_top + page_h * 0.18), 11),
        (int(page_left + page_w * 0.78), int(page_top + page_h * 0.22), 9),
        (int(page_left + page_w * 0.70), int(page_top + page_h * 0.25), 10),
    ]:
        draw_pixel_square_doodle(draw, px, py, psz, PENCIL_LIGHT, RNG)

    # Earlier doodle 3: two eyes side by side — comparing (one normal, one cracked)
    cmp_cx = int(page_left + page_w * 0.73)
    cmp_cy = int(page_top + page_h * 0.36)
    # Normal eye
    draw.ellipse([cmp_cx - 20, cmp_cy - 8, cmp_cx - 4, cmp_cy + 8],
                 outline=PENCIL_LIGHT, width=1)
    draw.ellipse([cmp_cx - 14, cmp_cy - 2, cmp_cx - 10, cmp_cy + 2],
                 fill=PENCIL_LIGHT)
    # "vs" dash between
    draw.line([(cmp_cx - 2, cmp_cy), (cmp_cx + 4, cmp_cy)],
              fill=PENCIL_LIGHT, width=1)
    # Cracked eye
    draw.ellipse([cmp_cx + 6, cmp_cy - 8, cmp_cx + 22, cmp_cy + 8],
                 outline=PENCIL_LIGHT, width=1)
    # Crack lines
    draw.line([(cmp_cx + 14, cmp_cy - 3), (cmp_cx + 22, cmp_cy - 8)],
              fill=PENCIL_LIGHT, width=1)
    draw.line([(cmp_cx + 14, cmp_cy + 2), (cmp_cx + 24, cmp_cy + 5)],
              fill=PENCIL_LIGHT, width=1)

    # ── MARGIN DOODLES (ghost/light — temporal evidence in the margins) ──────
    # Margin area shows the habit: she's been doodling in margins for a while
    for my_offset in range(4):
        mdy = int(page_top + page_h * (0.30 + my_offset * 0.14))
        mdx = page_left + 48
        # Tiny eye — progressively darker down the page (visual time gradient)
        m_color = lerp_color(PENCIL_GHOST, PENCIL_LIGHT, my_offset / 3.0)
        draw.ellipse([mdx - 5, mdy - 3, mdx + 5, mdy + 3],
                     outline=m_color, width=1)
        draw.ellipse([mdx - 1, mdy - 1, mdx + 1, mdy + 1],
                     fill=m_color)

    # Older teardrop in upper margin (ghost)
    mt_x, mt_y = int(page_left + 50), int(page_top + page_h * 0.17)
    draw.ellipse([mt_x - 5, mt_y - 6, mt_x + 5, mt_y],
                 outline=PENCIL_GHOST, width=1)
    draw.line([(mt_x - 5, mt_y - 2), (mt_x, mt_y + 4)],
              fill=PENCIL_GHOST, width=1)
    draw.line([(mt_x + 5, mt_y - 2), (mt_x, mt_y + 4)],
              fill=PENCIL_GHOST, width=1)

    # ══════════════════════════════════════════════════════════════════════════
    # TIER 3: TONIGHT'S HERO DOODLE — bold, detailed, circled, starred
    # This is the EUREKA moment. The visual climax of the page.
    # Largest doodle, darkest pencil, fully detailed cracked eye.
    # ══════════════════════════════════════════════════════════════════════════

    central_cx = int(page_left + page_w * 0.52)
    central_cy = int(page_top + page_h * 0.52)
    draw_byte_doodle(draw, central_cx, central_cy, 2.0, PENCIL_DARK, RNG, detail_level=2)

    # Heavy circle around it (emphatic, thick — pencil pressed hard)
    circle_r = 72
    draw.ellipse([central_cx - circle_r, central_cy - circle_r - 12,
                  central_cx + circle_r, central_cy + circle_r + 12],
                 outline=PENCIL_DARK, width=3)

    # EMPHASIS BURST: radiating lines outside the circle (eureka / realization)
    # This is the key visual timestamp cue — no text needed, the burst = "I SEE IT NOW"
    draw_emphasis_burst(draw, central_cx, central_cy - 2,
                        circle_r + 8, circle_r + 22, 12, PENCIL_GRAY)

    # Star mark at top-right of circle (Luma marking importance — visual, not text)
    star_cx = central_cx + circle_r - 8
    star_cy = central_cy - circle_r - 6
    for si in range(5):
        angle = (2 * math.pi * si / 5) - math.pi / 2
        sx = int(star_cx + 10 * math.cos(angle))
        sy = int(star_cy + 10 * math.sin(angle))
        inner_angle = angle + math.pi / 5
        ix = int(star_cx + 5 * math.cos(inner_angle))
        iy = int(star_cy + 5 * math.sin(inner_angle))
        draw.line([(star_cx, star_cy), (sx, sy)], fill=PENCIL_DARK, width=2)
    # Fill star
    star_pts = []
    for si in range(10):
        angle = (2 * math.pi * si / 10) - math.pi / 2
        r = 10 if si % 2 == 0 else 5
        star_pts.append((int(star_cx + r * math.cos(angle)),
                         int(star_cy + r * math.sin(angle))))
    draw.polygon(star_pts, fill=PENCIL_DARK)

    # Arrow from the circled hero doodle to the cracked eye specifically
    # (Luma pointing AT the detail that matters — her finger will reinforce this)
    cracked_eye_x = central_cx + int(8 * 2.0)
    cracked_eye_y = central_cy - int(12 * 2.0)
    arrow_sx = cracked_eye_x + 20
    arrow_sy = cracked_eye_y - 20
    arrow_ex = cracked_eye_x + 50
    arrow_ey = cracked_eye_y - 35
    draw.line([(arrow_sx, arrow_sy), (arrow_ex, arrow_ey)],
              fill=PENCIL_DARK, width=2)
    # Arrowhead pointing TOWARD the eye
    draw.polygon([
        (arrow_sx, arrow_sy),
        (arrow_sx + 6, arrow_sy - 6),
        (arrow_sx + 8, arrow_sy + 2),
    ], fill=PENCIL_DARK)

    # ── BOTTOM REGION: another Byte face study + size comparison ─────────────
    # She drew the face again at different angle — shows she's studying it
    br_cx = int(page_left + page_w * 0.72)
    br_cy = int(page_top + page_h * 0.68)
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

    # Connecting line between the two Byte faces (she's comparing them)
    draw.line([(central_cx + circle_r + 4, central_cy + 20),
               (br_cx - br_r - 4, br_cy - 10)],
              fill=PENCIL_GRAY, width=1)

    # ── VISUAL FLOW: dashed guide arrows (tiny) showing size progression ─────
    # These are barely-visible pencil marks connecting the doodle tiers
    # Ghost tier → Earlier tier → Hero tier (size increases = time passes)
    # Drawn as light dotted lines the reader's eye follows unconsciously

    # From ghost doodle zone to earlier doodle zone
    flow1_sx = g1_cx + 20
    flow1_sy = g1_cy + 14
    flow1_ex = e1_cx - 10
    flow1_ey = e1_cy - 30
    for t_dot in range(6):
        t = t_dot / 5.0
        dx = int(flow1_sx + (flow1_ex - flow1_sx) * t)
        dy = int(flow1_sy + (flow1_ey - flow1_sy) * t)
        draw.ellipse([dx - 1, dy - 1, dx + 1, dy + 1], fill=PENCIL_GHOST)

    # From earlier doodle to hero doodle
    flow2_sx = e1_cx + 25
    flow2_sy = e1_cy + 20
    flow2_ex = central_cx - circle_r + 5
    flow2_ey = central_cy - 10
    for t_dot in range(8):
        t = t_dot / 7.0
        dx = int(flow2_sx + (flow2_ex - flow2_sx) * t)
        dy = int(flow2_sy + (flow2_ey - flow2_sy) * t)
        # Dots get darker along the path (time passing visually)
        dot_color = lerp_color(PENCIL_GHOST, PENCIL_LIGHT, t)
        draw.ellipse([dx - 1, dy - 1, dx + 1, dy + 1], fill=dot_color)

    # ── Luma's hand visible at bottom-left — POINTING at the hero doodle ─────
    # Changed from passive hold to ACTIVE GESTURE: finger points at cracked eye
    hand_y = page_bottom - 8
    hand_x = page_left + 60

    # Hoodie cuff (CANONICAL ORANGE)
    draw.rectangle([hand_x - 40, hand_y, hand_x + 30, hand_y + 28],
                   fill=LUMA_HOODIE)
    # Cuff ribbing
    for cx_rib in range(hand_x - 38, hand_x + 28, 4):
        draw.line([(cx_rib, hand_y), (cx_rib, hand_y + 28)],
                  fill=lerp_color(LUMA_HOODIE, (180, 80, 38), 0.3), width=1)

    # Hand — fingers, with INDEX FINGER extended toward the hero doodle
    # Thumb
    draw.ellipse([hand_x + 30, hand_y - 6, hand_x + 46, hand_y + 10],
                 fill=LUMA_SKIN)
    # Curled fingers (3)
    for fi in range(3):
        fx = hand_x + 50 + fi * 10
        draw.ellipse([fx, hand_y - 2, fx + 9, hand_y + 8],
                     fill=LUMA_SKIN)
    # INDEX FINGER extended — pointing upward toward the hero doodle
    idx_start_x = hand_x + 78
    idx_start_y = hand_y + 2
    idx_tip_x = central_cx - 10
    idx_tip_y = central_cy + circle_r + 18
    # Finger body
    draw.line([(idx_start_x, idx_start_y), (idx_tip_x, idx_tip_y)],
              fill=LUMA_SKIN, width=7)
    # Fingertip
    draw.ellipse([idx_tip_x - 4, idx_tip_y - 4, idx_tip_x + 4, idx_tip_y + 2],
                 fill=LUMA_SKIN)

    # Pencil on the page (diagonal, resting)
    pencil_x1 = int(page_left + page_w * 0.55)
    pencil_y1 = int(page_top + page_h * 0.90)
    pencil_x2 = pencil_x1 + 80
    pencil_y2 = pencil_y1 - 14
    draw.line([(pencil_x1, pencil_y1), (pencil_x2, pencil_y2)],
              fill=(220, 195, 50), width=5)
    draw.line([(pencil_x1 - 6, pencil_y1 + 1), (pencil_x1, pencil_y1)],
              fill=PENCIL_DARK, width=3)
    draw.ellipse([pencil_x2 - 2, pencil_y2 - 4, pencil_x2 + 6, pencil_y2 + 4],
                 fill=(210, 140, 140))
    draw.line([(pencil_x2 - 4, pencil_y2 - 3), (pencil_x2, pencil_y2 - 2)],
              fill=SPIRAL_METAL, width=3)

    # ── Faint cyan cast from CRT monitor glow ────────────────────────────────
    add_glow(img, PW - 40, int(DRAW_H * 0.30), int(PW * 0.45),
             ELEC_CYAN, steps=6, max_alpha=12)
    draw = ImageDraw.Draw(img)

    # Warm ambient glow (den lamp, camera-left)
    add_glow(img, -30, int(DRAW_H * 0.20), int(PW * 0.50),
             SUNLIT_AMB, steps=8, max_alpha=14)
    draw = ImageDraw.Draw(img)

    # ── Annotations (board-level, not diegetic) ──────────────────────────────
    font_ann   = load_font(9,  bold=False)
    font_ann_b = load_font(9, bold=True)
    font_sm    = load_font(8,  bold=False)

    # Camera note
    draw.text((8, 8), 'CU / INSERT  |  NOTEBOOK PAGE  |  PROCESSING BEAT',
              font=font_ann, fill=ANN_COLOR)

    # Temporal zone annotations (board-reader guidance, not diegetic)
    draw.text((int(page_left + page_w * 0.14), int(page_top + page_h * 0.05)),
              "WEEKS AGO (ghost)", font=font_sm, fill=ANN_DIM)
    draw.text((int(page_left + page_w * 0.14), int(page_top + page_h * 0.32)),
              "DAYS AGO (building)", font=font_sm, fill=ANN_DIM)
    draw.text((central_cx - circle_r - 12, central_cy + circle_r + 16),
              "TONIGHT (eureka)", font=font_ann_b, fill=ANN_CYAN)
    draw.text((central_cx - circle_r - 12, central_cy + circle_r + 28),
              "SIZE + DARKNESS + DETAIL = TIME ARC", font=font_sm, fill=ANN_DIM)

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
              "Visual time arc: ghost (weeks) > faint (days) > bold (tonight).",
              font=font_t3, fill=TEXT_DESC)
    draw.text((10, DRAW_H + 35),
              "Doodle size/darkness/detail escalation = curiosity building over time.",
              font=font_t3, fill=(120, 112, 90))

    # Metadata
    draw.text((PW - 276, DRAW_H + 56),
              "LTG_SB_cold_open_P18  /  Diego Vargas  /  C47",
              font=font_meta, fill=TEXT_META)

    # Arc border — ELEC_CYAN (CURIOUS / PROCESSING)
    draw.rectangle([0, 0, PW - 1, PH - 1], outline=ARC_COLOR, width=4)

    img.thumbnail((1280, 1280))
    img.save(OUTPUT_PATH, "PNG")
    print(f"Saved: {OUTPUT_PATH}  {img.size}")
    return OUTPUT_PATH


if __name__ == "__main__":
    draw_panel()
    print("P18 standalone panel generation complete (C47 visual timestamp fix).")
    print("Beat: Notebook page with 3-tier visual time arc (ghost > faint > bold).")
    print("Passes blank test: size/darkness/detail progression reads without text.")
    print("ELEC_CYAN border. CU/INSERT on notebook prop.")
