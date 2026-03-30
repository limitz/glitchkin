#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_sb_cold_open_P06.py
Cold Open Panel P06 — CU MONITOR SCREEN — Byte's First Appearance
Diego Vargas, Storyboard Artist — Cycle 41

Beat: The REVEAL. Byte's face pressed against the inside of the CRT glass.
FIRST APPEARANCE OF BYTE. Expression: DISGUSTED / RELUCTANT CURIOSITY.
NOT menacing — he is the world's most unimpressed food critic.

Shot:   CU — Monitor screen (screen fills frame)
Camera: Straight-on, eye level to the screen surface. STATIC.
Palette: Full Glitch Palette (screen surface) / warm den edges (bezel shadow)
Arc:    CURIOUS/DISCOVERY — pitch-beat reveal

Expression art direction (from ep01_cold_open.md):
- Normal eye (viewer's right): 70% aperture, slight squint — assessment not aggression.
- Cracked eye (viewer's left): SEARCHING/PROCESSING — 3 rotating dots cyan/magenta.
- Mouth: horizontal "ugh" grimace, corners pressed OUTWARD. Not a snarl. Disgust.
- Body tilt: leaning FORWARD, face pressed to glass — curious not threatening.
- Overall read: very small, very opinionated food critic. Dissatisfied but engaged.

Image size rule: ≤ 1280px in both dimensions.
Output: output/storyboards/panels/LTG_SB_cold_open_P06.png
"""

from PIL import Image, ImageDraw, ImageFont
import math, random, os

PANELS_DIR  = "/home/wipkat/team/output/storyboards/panels"
OUTPUT_PATH = os.path.join(PANELS_DIR, "LTG_SB_cold_open_P06.png")
os.makedirs(PANELS_DIR, exist_ok=True)

PW, PH    = 800, 600
CAPTION_H = 60
DRAW_H    = PH - CAPTION_H   # 540

# ── Palette ──────────────────────────────────────────────────────────────────
ELEC_CYAN    = (0, 212, 232)
ELEC_CYAN_DIM= (0, 160, 180)
ELEC_CYAN_HI = (80, 240, 252)
HOT_MAGENTA  = (232, 0, 152)
VOID_BLACK   = (10, 10, 20)
STATIC_BASE  = (148, 138, 128)     # static grey
STATIC_CYAN  = (90, 140, 148)     # static tinted towards cyan (glitch contamination)
STATIC_LIGHT = (200, 196, 186)
STATIC_DARK  = (100, 96, 88)
BEZEL_WARM   = (155, 145, 112)    # monitor bezel corners (warm shadow)
PLASTIC_OLD  = (185, 172, 138)    # monitor plastic surround
LINE_DARK    = (80, 64, 44)
SCREEN_EDGE_GLOW = (0, 180, 200)  # subtle glitch glow bleeding off screen edges
# Byte body
BYTE_TEAL    = (0, 212, 232)      # canonical Byte body color
BYTE_DARK    = (0, 80, 100)       # darker fill for depth
BYTE_EYE_W   = (220, 230, 240)    # eye white/sclera
BYTE_EYE_CYAN= (0, 212, 232)      # cyan iris
CRACK_LINE   = (200, 30, 100)     # hot mag crack line
PROCESS_DOT_C= (0, 212, 232)      # processing dot cyan
PROCESS_DOT_M= (232, 0, 152)      # processing dot magenta
CONFETTI_1   = (0, 212, 232)
CONFETTI_2   = (232, 0, 152)
# Caption
BG_CAPTION   = (14, 10, 8)
TEXT_CAP     = (235, 228, 210)
ANN_COL      = (200, 175, 120)
ANN_DIM      = (150, 135, 100)
ARC_DISCOVER = (0, 212, 232)      # CURIOUS/DISCOVERY arc

RNG = random.Random(606)


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
    """Add light via alpha_composite — never darkens."""
    for i in range(steps, 0, -1):
        r     = int(r_max * (i / steps))
        alpha = int(max_alpha * (1 - (i / steps) * 0.6))
        glow  = Image.new('RGBA', img.size, (0, 0, 0, 0))
        gd    = ImageDraw.Draw(glow)
        gd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(*color_rgb, alpha))
        base  = img.convert('RGBA')
        img.paste(Image.alpha_composite(base, glow).convert('RGB'))


def draw_irregular_poly(draw, cx, cy, r, sides, color, seed=0, outline=None):
    """Draw an irregular polygon (Glitchkin pixel standard — no rectangles)."""
    rng = random.Random(seed)
    pts = []
    for i in range(sides):
        angle = (2 * math.pi * i / sides) + rng.uniform(-0.2, 0.2)
        dist  = r * rng.uniform(0.72, 1.18)
        pts.append((int(cx + dist * math.cos(angle)), int(cy + dist * math.sin(angle))))
    draw.polygon(pts, fill=color, outline=outline)


def draw_static_texture(draw, x0, y0, x1, y1, rng, tint=False):
    """CRT static with optional cyan tint for Glitch contamination zones."""
    w = x1 - x0
    h = y1 - y0
    base = STATIC_CYAN if tint else STATIC_BASE
    draw.rectangle([x0, y0, x1, y1], fill=base)
    for _ in range(w * h // 14):
        sx = x0 + rng.randint(0, max(1, w - 1))
        sy = y0 + rng.randint(0, max(1, h - 1))
        v  = rng.randint(0, 3)
        if v == 0:
            draw.point((sx, sy), fill=STATIC_LIGHT)
        elif v == 1:
            draw.point((sx, sy), fill=STATIC_DARK)
    # Scan lines
    for sl_y in range(y0, y1, 3):
        col = (base[0] - 14, base[1] - 14, base[2] - 14)
        draw.line([(x0, sl_y), (x1, sl_y)], fill=col, width=1)


def draw_byte_face(img, draw, face_cx, face_cy, face_r):
    """
    Draw Byte's face pressed against the screen glass from inside.
    face_cx, face_cy: center of face
    face_r: approximate radius of face area

    Expression: DISGUSTED / RELUCTANT CURIOSITY
    - He is pressed flat against the glass — face slightly squished
    - Normal eye (viewer's right): 70% aperture squint
    - Cracked eye (viewer's left): SEARCHING/PROCESSING dots
    - Mouth: horizontal "ugh" flat grimace — corners pressed OUT
    - Triangle-heavy, jagged angular shapes
    - ELEC_CYAN + VOID_BLACK — no warm colors
    """

    # ── Head/body shape (angular, triangle-heavy — pressed against glass) ────
    # Byte presses his face flat — so we draw his front-facing shape as
    # a somewhat flattened oval/angular form

    # Head is pressed — slightly squashed horizontally to suggest glass contact
    head_w = int(face_r * 1.30)
    head_h = int(face_r * 1.10)

    # Head body — irregular polygon with jagged edges (Glitchkin pixel standard)
    # 6-sided irregular polygon for head silhouette
    head_pts = []
    sides = 6
    for i in range(sides):
        base_angle = 2 * math.pi * i / sides - math.pi / 2
        jitter = [0.12, -0.10, 0.15, -0.08, 0.13, -0.11][i]
        angle = base_angle + jitter
        rx = head_w * (1.0 + [0.05, 0.08, 0.04, 0.06, 0.03, 0.07][i])
        ry = head_h * (1.0 + [0.04, 0.07, 0.08, 0.05, 0.06, 0.04][i])
        head_pts.append((int(face_cx + rx * math.cos(angle)),
                         int(face_cy + ry * math.sin(angle))))
    draw.polygon(head_pts, fill=BYTE_TEAL, outline=VOID_BLACK)

    # Darker inner core (depth on the face)
    inner_pts = []
    for i in range(sides):
        base_angle = 2 * math.pi * i / sides - math.pi / 2
        angle = base_angle
        rx = head_w * 0.65
        ry = head_h * 0.60
        inner_pts.append((int(face_cx + rx * math.cos(angle)),
                          int(face_cy + ry * math.sin(angle))))
    draw.polygon(inner_pts, fill=BYTE_DARK)

    # ── Arm stubs pressed against glass ──────────────────────────────────────
    # Short stubby arms pressed flat — left and right
    arm_cy = face_cy + int(face_r * 0.30)
    for side in [-1, 1]:
        arm_cx = face_cx + side * int(face_r * 1.20)
        arm_pts = [
            (face_cx + side * int(face_r * 0.88), arm_cy - 10),
            (arm_cx + side * 8, arm_cy - 14),
            (arm_cx + side * 18, arm_cy - 2),
            (arm_cx + side * 14, arm_cy + 12),
            (arm_cx - side * 2, arm_cy + 10),
            (face_cx + side * int(face_r * 0.90), arm_cy + 6),
        ]
        draw.polygon(arm_pts, fill=BYTE_TEAL, outline=VOID_BLACK)

    # Hand/palm pressed against glass — flat splat shape
    for side in [-1, 1]:
        palm_cx = face_cx + side * int(face_r * 1.48)
        palm_cy = arm_cy + 4
        palm_pts = [
            (palm_cx - 10, palm_cy - 12),
            (palm_cx + 4,  palm_cy - 16),
            (palm_cx + 14, palm_cy - 8),
            (palm_cx + 18, palm_cy + 4),
            (palm_cx + 8,  palm_cy + 14),
            (palm_cx - 6,  palm_cy + 10),
            (palm_cx - 14, palm_cy + 0),
        ]
        draw.polygon(palm_pts, fill=ELEC_CYAN_HI, outline=VOID_BLACK)

    # ── Eyes ─────────────────────────────────────────────────────────────────
    eye_cy = face_cy - int(face_r * 0.15)
    eye_sep = int(face_r * 0.52)

    # NORMAL EYE — viewer's right (character's left)
    # 70% aperture — slight squint, assessment not aggression
    ne_cx = face_cx + eye_sep
    ne_cy = eye_cy
    ne_r  = int(face_r * 0.22)

    # Eye white
    draw.ellipse([ne_cx - ne_r, ne_cy - int(ne_r * 0.70),
                  ne_cx + ne_r, ne_cy + int(ne_r * 0.70)],
                 fill=BYTE_EYE_W, outline=VOID_BLACK, width=2)

    # Top lid at 70% — slightly squinted
    lid_drop = int(ne_r * 0.30)     # lid covers top 30%
    draw.ellipse([ne_cx - ne_r, ne_cy - int(ne_r * 0.70),
                  ne_cx + ne_r, ne_cy - int(ne_r * 0.70) + lid_drop * 2],
                 fill=VOID_BLACK)
    draw.line([(ne_cx - ne_r, ne_cy - int(ne_r * 0.70) + lid_drop),
               (ne_cx + ne_r, ne_cy - int(ne_r * 0.70) + lid_drop)],
              fill=VOID_BLACK, width=3)

    # Iris — cyan (smaller than full eye)
    iris_r = int(ne_r * 0.55)
    draw.ellipse([ne_cx - iris_r, ne_cy - iris_r + lid_drop // 2,
                  ne_cx + iris_r, ne_cy + iris_r - lid_drop // 4],
                 fill=BYTE_EYE_CYAN, outline=VOID_BLACK, width=1)

    # Pupil (small void center)
    pu_r = int(iris_r * 0.38)
    draw.ellipse([ne_cx - pu_r, ne_cy - pu_r + lid_drop // 3,
                  ne_cx + pu_r, ne_cy + pu_r - lid_drop // 6],
                 fill=VOID_BLACK)

    # CRACKED EYE — viewer's left (character's right)
    # Showing SEARCHING/PROCESSING state: 3 rotating dots cyan/magenta
    ce_cx = face_cx - eye_sep
    ce_cy = eye_cy
    ce_r  = int(face_r * 0.22)

    # Cracked eye socket (rectangular-ish, cracked glass look)
    crack_eye_pts = [
        (ce_cx - ce_r,     ce_cy - int(ce_r * 0.62)),
        (ce_cx + ce_r,     ce_cy - int(ce_r * 0.62)),
        (ce_cx + ce_r + 3, ce_cy),
        (ce_cx + ce_r,     ce_cy + int(ce_r * 0.62)),
        (ce_cx - ce_r,     ce_cy + int(ce_r * 0.62)),
        (ce_cx - ce_r - 3, ce_cy),
    ]
    draw.polygon(crack_eye_pts, fill=VOID_BLACK, outline=ELEC_CYAN_DIM, width=2)

    # Processing dots: 3 dots in a triangle arrangement, alt cyan/magenta
    # CRACKED EYE DIVERGENCE (Lee Tanaka sight-line note):
    # The cracked eye registers the environment differently from the normal eye.
    # Shift dot cluster ~6° off-axis toward viewer's right (away from normal eye aim).
    # Normal eye aims at center/Luma (slightly left of 0°). Cracked eye diverges outward.
    # Divergence offset: shift dot cluster +int(ce_r*0.20) in X toward outer frame edge.
    div_x = -int(ce_r * 0.20)   # diverge LEFT (away from normal eye) in viewer's frame
    dot_r = int(ce_r * 0.18)
    dot_positions = [
        (ce_cx + div_x,          ce_cy - int(ce_r * 0.28)),  # top (diverged)
        (ce_cx + div_x - int(ce_r * 0.28), ce_cy + int(ce_r * 0.15)),  # bottom-left
        (ce_cx + div_x + int(ce_r * 0.28), ce_cy + int(ce_r * 0.15)),  # bottom-right
    ]
    dot_colors = [PROCESS_DOT_C, PROCESS_DOT_M, PROCESS_DOT_C]
    for (dx, dy), dc in zip(dot_positions, dot_colors):
        draw.ellipse([dx - dot_r, dy - dot_r, dx + dot_r, dy + dot_r], fill=dc)

    # Crack lines across the eye (diagonal fracture — Byte's signature)
    # Main crack: upper-left to lower-right diagonal
    crack_x0 = ce_cx - ce_r + 4
    crack_y0 = ce_cy - int(ce_r * 0.55)
    crack_x1 = ce_cx + ce_r - 4
    crack_y1 = ce_cy + int(ce_r * 0.55)
    draw.line([(crack_x0, crack_y0), (crack_x1, crack_y1)], fill=CRACK_LINE, width=2)
    # Branch crack
    mid_cx = (crack_x0 + crack_x1) // 2
    mid_cy = (crack_y0 + crack_y1) // 2
    draw.line([(mid_cx, mid_cy), (mid_cx - 8, mid_cy - 12)], fill=CRACK_LINE, width=1)
    draw.line([(mid_cx, mid_cy), (mid_cx + 10, mid_cy + 6)], fill=CRACK_LINE, width=1)

    # ── Brow / upper face ridge ───────────────────────────────────────────────
    # Angular brow ridges — part of Byte's triangle-heavy design
    # Normal eye side (right): brow is furrowed — pressed down in center (disgust/assessment)
    ne_brow_y = ne_cy - int(ne_r * 1.10)
    draw.polygon([
        (ne_cx - ne_r, ne_brow_y + 4),
        (ne_cx + int(ne_r * 0.4), ne_brow_y - 4),
        (ne_cx + ne_r + 4, ne_brow_y + 2),
        (ne_cx + ne_r + 2, ne_brow_y + 8),
        (ne_cx - ne_r + 2, ne_brow_y + 10),
    ], fill=VOID_BLACK)

    # Cracked eye side (left): brow also furrowed — slightly raised at outer edge
    ce_brow_y = ce_cy - int(ce_r * 1.05)
    draw.polygon([
        (ce_cx - ce_r - 4, ce_brow_y + 4),
        (ce_cx - int(ce_r * 0.4), ce_brow_y - 2),
        (ce_cx + ce_r, ce_brow_y + 4),
        (ce_cx + ce_r - 2, ce_brow_y + 9),
        (ce_cx - ce_r - 2, ce_brow_y + 10),
    ], fill=VOID_BLACK)

    # ── Mouth — horizontal "ugh" grimace ─────────────────────────────────────
    # Corners pressed OUTWARD — flat, not curled. Disgust, not snarl.
    # Slight openness, pixel-teeth visible in row
    mouth_cy = face_cy + int(face_r * 0.40)
    mouth_w  = int(face_r * 0.80)
    mouth_h  = int(face_r * 0.18)

    # Mouth opening — flat horizontal ellipse
    draw.ellipse([face_cx - mouth_w // 2, mouth_cy - mouth_h // 2,
                  face_cx + mouth_w // 2, mouth_cy + mouth_h // 2],
                 fill=VOID_BLACK, outline=ELEC_CYAN_DIM, width=1)

    # Pixel teeth — small rectangles along top edge of mouth
    teeth_y = mouth_cy - mouth_h // 2 + 1
    tooth_w = 7
    tooth_h = 6
    num_teeth = mouth_w // (tooth_w + 2)
    start_tx = face_cx - (num_teeth * (tooth_w + 2)) // 2
    for ti in range(num_teeth):
        tx = start_tx + ti * (tooth_w + 2)
        draw.rectangle([tx, teeth_y, tx + tooth_w, teeth_y + tooth_h],
                       fill=BYTE_EYE_W, outline=VOID_BLACK, width=1)

    # Mouth corners pressed slightly OUT (not curled down) — small angular flares
    for side in [-1, 1]:
        corner_x = face_cx + side * mouth_w // 2
        corner_y = mouth_cy
        flare_pts = [
            (corner_x, corner_y - 4),
            (corner_x + side * 8, corner_y - 2),
            (corner_x + side * 10, corner_y + 4),
            (corner_x + side * 4, corner_y + 6),
            (corner_x, corner_y + 4),
        ]
        draw.polygon(flare_pts, fill=BYTE_TEAL, outline=VOID_BLACK)

    # ── Pixel confetti bleeding out from screen edges near hands ────────────
    # Some confetti pixels are escaping — suggests screen membrane being breached
    for conf_seed in range(12):
        conf_rng = random.Random(conf_seed * 77)
        # Near hand areas (left and right sides)
        for side in [-1, 1]:
            cx_conf = face_cx + side * int(face_r * 1.6) + conf_rng.randint(-20, 20)
            cy_conf = arm_cy + conf_rng.randint(-30, 40)
            conf_size = conf_rng.randint(3, 7)
            col = CONFETTI_1 if conf_rng.randint(0, 1) == 0 else CONFETTI_2
            draw.rectangle([cx_conf, cy_conf, cx_conf + conf_size, cy_conf + conf_size],
                           fill=col)

    # ── Screen distortion ripple at face contact points ──────────────────────
    # Where face is pressed against screen — pixel bleed / distortion rings
    add_glow(img, face_cx, face_cy, int(face_r * 1.6), ELEC_CYAN, steps=5, max_alpha=40)
    draw = ImageDraw.Draw(img)


def draw_scene(img):
    draw = ImageDraw.Draw(img)

    # ── Screen fills entire panel — this is a CU of the screen itself ────────
    # The screen surface fills the frame. Very thin bezel edges visible.
    BZ = 22   # bezel thickness at edges (barely visible)

    # Bezel (narrow strip at edges — warm plastic)
    draw.rectangle([0, 0, PW, DRAW_H], fill=PLASTIC_OLD)

    # Screen area
    sx0 = BZ
    sx1 = PW - BZ
    sy0 = BZ
    sy1 = DRAW_H - BZ

    # Static texture — left half still analog, right half increasingly tinted cyan
    mid_x = (sx0 + sx1) // 2
    draw_static_texture(draw, sx0, sy0, mid_x, sy1, RNG, tint=False)
    draw_static_texture(draw, mid_x, sy0, sx1, sy1, RNG, tint=True)

    # Scan lines over full screen
    for sl_y in range(sy0, sy1, 3):
        draw.line([(sx0, sl_y), (sx1, sl_y)], fill=(100, 95, 90), width=1)

    # Screen edge glow (the whole screen is lit from within)
    add_glow(img, (sx0 + sx1) // 2, (sy0 + sy1) // 2,
             (sx1 - sx0) // 2, (60, 160, 180), steps=4, max_alpha=22)
    draw = ImageDraw.Draw(img)

    # ── Byte's face pressed against glass ────────────────────────────────────
    face_cx = int(PW * 0.52)
    face_cy = int(DRAW_H * 0.46)
    face_r  = int(min(PW, DRAW_H) * 0.28)

    draw_byte_face(img, draw, face_cx, face_cy, face_r)
    draw = ImageDraw.Draw(img)

    # ── Screen surface distortion at face/hand contact ────────────────────────
    # Subtle convex bulge suggestion — pixel distortion ripple rings (concentric ovals)
    for ring in range(1, 4):
        rw = face_r * (1.0 + ring * 0.18)
        rh = face_r * (0.85 + ring * 0.10)
        alpha_val = max(0, 30 - ring * 8)
        ov_x0 = int(face_cx - rw)
        ov_y0 = int(face_cy - rh)
        ov_x1 = int(face_cx + rw)
        ov_y1 = int(face_cy + rh)
        if ov_x0 >= 0 and ov_y0 >= 0 and ov_x1 < PW and ov_y1 < DRAW_H:
            draw.ellipse([ov_x0, ov_y0, ov_x1, ov_y1],
                         outline=(*ELEC_CYAN, alpha_val), width=1)

    # ── Panel annotations ─────────────────────────────────────────────────────
    font_ann  = load_font(11)
    font_ann_b = load_font(11, bold=True)

    draw.text((10, 8), "P06  /  CU — MONITOR SCREEN  /  straight-on eye level  /  STATIC camera",
              font=font_ann, fill=ANN_COL)
    draw.text((10, 20), "BYTE: face pressed flat against inside of glass — FIRST APPEARANCE",
              font=font_ann, fill=ANN_DIM)
    draw.text((10, 32), "Expression: DISGUSTED / RELUCTANT CURIOSITY — not menacing",
              font=font_ann, fill=(0, 200, 220))

    # Eye callout labels
    eye_cy = int(DRAW_H * 0.46) - int(min(PW, DRAW_H) * 0.28 * 0.15)
    eye_sep = int(min(PW, DRAW_H) * 0.28 * 0.52)
    ne_cx = int(PW * 0.52) + eye_sep
    ce_cx = int(PW * 0.52) - eye_sep
    draw.text((ne_cx - 20, eye_cy - int(min(PW, DRAW_H) * 0.28 * 0.50)),
              "70% aperture\nassessment squint",
              font=load_font(9), fill=(0, 200, 220))
    draw.text((ce_cx - 52, eye_cy - int(min(PW, DRAW_H) * 0.28 * 0.50)),
              "CRACKED EYE:\nSEARCHING/PROCESS",
              font=load_font(9), fill=HOT_MAGENTA)

    # Shot label
    draw.rectangle([10, DRAW_H - 24, 155, DRAW_H - 6], fill=(20, 12, 8))
    draw.text((14, DRAW_H - 22), "CU / MONITOR SCREEN",
              font=font_ann_b, fill=(240, 220, 140))

    # Arc indicator
    draw.rectangle([PW - 160, DRAW_H - 24, PW - 10, DRAW_H - 6], fill=(0, 30, 40))
    draw.text((PW - 156, DRAW_H - 22), "ARC: DISCOVERY",
              font=font_ann_b, fill=ELEC_CYAN)

    return draw


def make_panel():
    font_cap  = load_font(12)
    font_ann  = load_font(11)
    font_sm   = load_font(10)

    img  = Image.new('RGB', (PW, PH), STATIC_BASE)
    draw_scene(img)
    draw = ImageDraw.Draw(img)

    # Caption bar
    draw.rectangle([0, DRAW_H, PW, PH], fill=BG_CAPTION)
    draw.line([0, DRAW_H, PW, DRAW_H], fill=(10, 8, 6), width=2)
    draw.text((10, DRAW_H + 4),
              "P06  CU  MONITOR SCREEN  straight-on  |  FIRST APPEARANCE: Byte",
              font=font_cap, fill=(160, 155, 130))
    draw.text((10, DRAW_H + 18),
              "Byte pressed flat against inside of CRT glass. Expression: DISGUSTED / RELUCTANT CURIOSITY.",
              font=font_cap, fill=TEXT_CAP)
    draw.text((10, DRAW_H + 33),
              "Cracked eye divergent aim (~6° off-axis outward). Pixel confetti at both hands (symmetric).",
              font=font_ann, fill=(150, 140, 110))
    draw.text((PW - 230, DRAW_H + 46), "LTG_SB_cold_open_P06  /  Diego Vargas  /  C42",
              font=font_sm, fill=(100, 95, 78))

    # Arc border
    draw.rectangle([0, 0, PW - 1, PH - 1], outline=ARC_DISCOVER, width=3)

    img.thumbnail((1280, 1280))
    img.save(OUTPUT_PATH, "PNG")
    print(f"Saved: {OUTPUT_PATH}  {img.size}")
    return OUTPUT_PATH


if __name__ == "__main__":
    make_panel()
    print("P06 standalone panel generation complete.")
