#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_sb_cold_open_P07.py
Cold Open Panel P07 — MED WIDE — Monitor Bulging / Dutch 8° CW / Byte Phases Through
Diego Vargas, Storyboard Artist — Cycle 43

Beat: The moment before Byte fully crosses. The CRT is under physical pressure
      from inside. Dutch tilt signals the room's geometry can no longer be trusted.
      Byte is mid-phase: lower half still inside (desaturated, behind glass),
      upper half emerging into the real world (full teal + confetti burst at threshold).

Shot:   MED WIDE — low angle (floor level, looking slightly up)
Camera: Low angle — Byte's head breaks the upper horizon. Dutch 8° CW.
        Dutch tilt applied to full draw area, caption stays horizontal.
Palette: ELEC_CYAN dominant (multiple monitors bleeding), warm domestic light
         losing to cyan (visible far-left margin only). Void Black vacuum zones at
         screen edges. Confetti at crossing threshold.
Arc:    TENSE → BREACH (Hot Magenta border)

Monitor geometry:
  - Fills ~40–45% frame width at 55–65% x (camera-right of center)
  - Bows outward (convex distortion — curved rectangle face)
  - Screen: white-hot center, distortion rings breaking OUTSIDE bezel boundary
  - 2–3 stress cracks radiating from lower-left bezel corner
  - ELEC_CYAN dominant screen color, VOID_BLACK vacuum edges

Byte (mid-phase):
  - Lower half: inside screen, reduced opacity 50–60%, desaturated
  - Upper half: full teal, full opacity, pixel confetti bursting at boundary
  - Expression: DETERMINED + ALARMED — eyes wide, slight open mouth
  - Body vector slightly upward (rising as he comes through)

Image size rule: ≤ 1280px in both dimensions.
Output: output/storyboards/panels/LTG_SB_cold_open_P07.png
"""

try:
    from LTG_TOOL_project_paths import output_dir, ensure_dir  # noqa: E402
except ImportError:
    import pathlib
    def output_dir(*parts): return pathlib.Path("/home/wipkat/team/output").joinpath(*parts)
    def ensure_dir(path): path.mkdir(parents=True, exist_ok=True); return path
from PIL import Image, ImageDraw, ImageFont
import math, random, os
import sys
from LTG_TOOL_char_byte import draw_byte
from LTG_TOOL_cairo_primitives import to_pil_rgba
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

PANELS_DIR = output_dir('storyboards', 'panels')
OUTPUT_PATH = os.path.join(PANELS_DIR, "LTG_SB_cold_open_P07.png")
os.makedirs(PANELS_DIR, exist_ok=True)

PW, PH    = 800, 600
CAPTION_H = 60
DRAW_H    = PH - CAPTION_H   # 540

# ── Palette ──────────────────────────────────────────────────────────────────
# Real World — warm (on the losing side, far-left margin only)
WARM_CREAM   = (250, 240, 220)
WARM_AMB     = (212, 146, 58)
WALL_WARM    = (220, 200, 168)
WALL_COOL    = (80, 90, 110)      # cyan-contaminated wall
FLOOR_WARM   = (185, 158, 116)
FLOOR_CYAN   = (40, 80, 95)       # floor under cyan light
CABLE_DARK   = (45, 35, 22)
CABLE_MED    = (62, 50, 34)
# Glitch World / Monitor
ELEC_CYAN    = (0, 212, 232)
ELEC_CYAN_DIM= (0, 140, 160)
ELEC_CYAN_HI = (90, 248, 255)
WHITE_HOT    = (255, 255, 248)
HOT_MAGENTA  = (255, 45, 107)
VOID_BLACK   = (10, 10, 20)
DEEP_SPACE   = (8, 8, 18)         # Dutch tilt fill
CRT_PLASTIC  = (72, 68, 60)       # monitor casing — darker under cyan contamination
CRT_DARK     = (38, 34, 28)
BEZEL_STRESS = (90, 80, 65)       # bezel stress lines
# Byte
BYTE_TEAL    = (0, 212, 232)
BYTE_TEAL_DIM= (0, 130, 148)      # Byte lower half behind glass — desaturated
BYTE_EYE_W   = (230, 240, 248)
CRACK_LINE   = (200, 30, 100)
CONFETTI_C   = (0, 212, 232)
CONFETTI_M   = (232, 0, 152)
PIXEL_SPARK  = (90, 248, 255)
# Caption / annotation
BG_CAPTION   = (12, 8, 6)
TEXT_CAP     = (230, 222, 202)
ANN_COL      = (180, 155, 100)
ANN_DIM      = (130, 118, 88)
ARC_COLOR    = HOT_MAGENTA        # TENSE → BREACH

RNG = random.Random(707)


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
    """Additive alpha composite glow — never darkens."""
    for i in range(steps, 0, -1):
        r     = int(r_max * (i / steps))
        alpha = int(max_alpha * (1 - (i / steps) * 0.6))
        glow  = Image.new('RGBA', img.size, (0, 0, 0, 0))
        gd    = ImageDraw.Draw(glow)
        gd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(*color_rgb, alpha))
        base  = img.convert('RGBA')
        img.paste(Image.alpha_composite(base, glow).convert('RGB'))


def draw_irregular_poly(draw, cx, cy, r, sides, color, seed=0, outline=None, outline_w=1):
    """4–7 sided irregular polygon — Cycle 11 standard for all Glitchkin shapes."""
    rng = random.Random(seed)
    pts = []
    for i in range(sides):
        angle = (2 * math.pi * i / sides) + rng.uniform(-0.28, 0.28)
        dist  = r * rng.uniform(0.68, 1.22)
        pts.append((int(cx + dist * math.cos(angle)), int(cy + dist * math.sin(angle))))
    draw.polygon(pts, fill=color, outline=outline)


def draw_confetti_burst(draw, cx, cy, count, rng_seed, r_spread=60):
    """Pixel confetti burst at screen threshold — all irregular polys (Cycle 11 standard)."""
    rng = random.Random(rng_seed)
    for i in range(count):
        angle = rng.uniform(0, 2 * math.pi)
        dist  = rng.uniform(4, r_spread)
        px    = int(cx + dist * math.cos(angle))
        py    = int(cy + dist * math.sin(angle))
        r     = rng.randint(2, 5)
        sides = rng.randint(4, 7)
        col   = CONFETTI_C if rng.randint(0, 2) != 0 else CONFETTI_M
        draw_irregular_poly(draw, px, py, r, sides, col, seed=i * 31 + rng_seed)




def draw_monitor_hero(draw, mon_cx, mon_cy, mon_w, mon_h):
    """
    Hero CRT monitor: bowing convex face, white-hot center, distortion rings
    breaking OUTSIDE bezel boundary, stress cracks at lower-left corner.
    """
    # ── Monitor casing (outer shell) ─────────────────────────────────────────
    casing_pts = [
        (mon_cx - mon_w // 2 - 8,   mon_cy - mon_h // 2 - 6),
        (mon_cx + mon_w // 2 + 8,   mon_cy - mon_h // 2 - 6),
        (mon_cx + mon_w // 2 + 14,  mon_cy + mon_h // 2 + 10),
        (mon_cx - mon_w // 2 - 14,  mon_cy + mon_h // 2 + 10),
    ]
    draw.polygon(casing_pts, fill=CRT_PLASTIC, outline=CRT_DARK)

    # Casing depth detail (side face showing thickness)
    draw.polygon([
        (mon_cx + mon_w // 2 + 8,   mon_cy - mon_h // 2 - 6),
        (mon_cx + mon_w // 2 + 22,  mon_cy - mon_h // 2 + 10),
        (mon_cx + mon_w // 2 + 28,  mon_cy + mon_h // 2 + 22),
        (mon_cx + mon_w // 2 + 14,  mon_cy + mon_h // 2 + 10),
    ], fill=CRT_DARK, outline=CRT_DARK)

    # ── Screen face — BOWING CONVEX (the key visual) ─────────────────────────
    # Bezel rectangle (slightly recessed from casing)
    bezel_l = mon_cx - mon_w // 2 + 4
    bezel_r = mon_cx + mon_w // 2 - 4
    bezel_t = mon_cy - mon_h // 2 + 6
    bezel_b = mon_cy + mon_h // 2 - 4
    draw.rectangle([bezel_l, bezel_t, bezel_r, bezel_b],
                   fill=CRT_DARK, outline=BEZEL_STRESS, width=2)

    # Screen fill — ELEC_CYAN base with VOID_BLACK vacuum edges
    scr_l = bezel_l + 5
    scr_r = bezel_r - 5
    scr_t = bezel_t + 5
    scr_b = bezel_b - 5
    draw.rectangle([scr_l, scr_t, scr_r, scr_b], fill=ELEC_CYAN)

    # VOID_BLACK vacuum zone edges (screen losing containment at edges)
    void_w = int((scr_r - scr_l) * 0.12)
    void_h = int((scr_b - scr_t) * 0.12)
    # Top-left void
    draw.rectangle([scr_l, scr_t, scr_l + void_w, scr_t + void_h], fill=VOID_BLACK)
    # Bottom-right void
    draw.rectangle([scr_r - void_w, scr_b - void_h, scr_r, scr_b], fill=VOID_BLACK)

    # Convex bow effect: bright ellipse center creates illusion of bulging outward
    bow_cx = (scr_l + scr_r) // 2
    bow_cy = (scr_t + scr_b) // 2

    # White-hot center (overpressure luminance peak)
    draw.ellipse([bow_cx - int((scr_r - scr_l) * 0.16),
                  bow_cy - int((scr_b - scr_t) * 0.16),
                  bow_cx + int((scr_r - scr_l) * 0.16),
                  bow_cy + int((scr_b - scr_t) * 0.16)],
                 fill=WHITE_HOT)

    # Mid glow ring
    draw.ellipse([bow_cx - int((scr_r - scr_l) * 0.30),
                  bow_cy - int((scr_b - scr_t) * 0.30),
                  bow_cx + int((scr_r - scr_l) * 0.30),
                  bow_cy + int((scr_b - scr_t) * 0.30)],
                 fill=ELEC_CYAN_HI)

    # Scanlines on screen (analog monitor texture)
    for sl in range(scr_t + 1, scr_b, 3):
        draw.line([(scr_l, sl), (scr_r, sl)], fill=ELEC_CYAN_DIM, width=1)

    # ── Distortion rings BREAKING OUTSIDE bezel boundary ─────────────────────
    # This is the "physics violation / danger" signal — rings must pass the bezel edge
    for ring_i, (r_scale, r_alpha_ref) in enumerate([(0.52, 180), (0.68, 120), (0.84, 70)]):
        rw = int((scr_r - scr_l) * r_scale)
        rh = int((scr_b - scr_t) * r_scale)
        ring_l = bow_cx - rw
        ring_t = bow_cy - rh
        ring_r = bow_cx + rw
        ring_b = bow_cy + rh
        # Draw as outline only (ring = distortion)
        draw.ellipse([ring_l, ring_t, ring_r, ring_b],
                     outline=ELEC_CYAN_HI if ring_i == 0 else ELEC_CYAN,
                     width=2 if ring_i == 0 else 1)

    # ── Stress cracks — 2–3 lines from lower-left bezel corner ───────────────
    crack_ox = bezel_l + 5
    crack_oy = bezel_b - 5
    crack_defs = [
        (crack_ox, crack_oy, crack_ox - 18, crack_oy + 14, 2),   # main crack
        (crack_ox + 4, crack_oy, crack_ox + 18, crack_oy + 20, 1),  # secondary crack
        (crack_ox, crack_oy - 5, crack_ox - 10, crack_oy + 5, 1),   # small stress
    ]
    for x0, y0, x1, y1, w in crack_defs:
        draw.line([(x0, y0), (x1, y1)], fill=BEZEL_STRESS, width=w)

    # Note: bezel corner glow
    add_glow_coords = (crack_ox - 5, crack_oy)
    return (scr_l, scr_t, scr_r, scr_b), (bow_cx, bow_cy), (bezel_l, bezel_t, bezel_r, bezel_b)


def draw_secondary_monitors(draw, horizon_y, mon_cx, mon_cy):
    """Background monitors: cyan bleeding, warm domestic light losing."""
    # Left background monitor (far left, partially out of frame)
    for bm_x, bm_y, bm_w, bm_h, is_warm in [
        (int(PW * 0.04), int(DRAW_H * 0.08), int(PW * 0.14), int(DRAW_H * 0.24), True),   # far-left (warm residual)
        (int(PW * 0.25), int(DRAW_H * 0.12), int(PW * 0.12), int(DRAW_H * 0.20), False),  # left-center (cyan)
        (int(PW * 0.78), int(DRAW_H * 0.06), int(PW * 0.10), int(DRAW_H * 0.18), False),  # far-right (cyan)
    ]:
        # Monitor shell
        draw.rectangle([bm_x, bm_y, bm_x + bm_w, bm_y + bm_h],
                       fill=CRT_DARK, outline=(60, 55, 48))
        # Screen face
        sm = 6
        scr_fill = WARM_AMB if is_warm else ELEC_CYAN
        draw.rectangle([bm_x + sm, bm_y + sm, bm_x + bm_w - sm, bm_y + bm_h - sm],
                       fill=scr_fill)
        # Scanlines
        for sl in range(bm_y + sm + 1, bm_y + bm_h - sm, 3):
            dim_col = (160, 110, 40) if is_warm else ELEC_CYAN_DIM
            draw.line([(bm_x + sm, sl), (bm_x + bm_w - sm, sl)], fill=dim_col, width=1)
        if is_warm:
            draw.text((bm_x + sm, bm_y + bm_h + 2), "warm\n(losing)",
                      font=load_font(8), fill=(180, 140, 80))



def _char_to_pil(surface):
    """Convert a cairo.ImageSurface from canonical char module to cropped PIL RGBA."""
    from LTG_TOOL_cairo_primitives import to_pil_rgba
    pil_img = to_pil_rgba(surface)
    bbox = pil_img.getbbox()
    if bbox:
        pil_img = pil_img.crop(bbox)
    return pil_img


def _composite_char(base_img, char_pil, cx, cy):
    """Composite a character PIL RGBA image onto base_img centered at (cx, cy)."""
    x = cx - char_pil.width // 2
    y = cy - char_pil.height // 2
    overlay = Image.new('RGBA', base_img.size, (0, 0, 0, 0))
    overlay.paste(char_pil, (x, y), char_pil)
    base_rgba = base_img.convert('RGBA')
    result = Image.alpha_composite(base_rgba, overlay)
    base_img.paste(result.convert('RGB'))

def draw_byte_mid_phase(img, draw, byte_cx, byte_cy, body_h, screen_y2):
    """Byte mid-phase through monitor — canonical renderer + composite."""
    scale = body_h / 88.0
    surface = draw_byte(expression="alarmed", scale=scale, facing="front")
    char_pil = _char_to_pil(surface)
    if char_pil.height > 0:
        aspect = char_pil.width / char_pil.height
        new_h = body_h
        new_w = int(new_h * aspect)
        char_pil = char_pil.resize((new_w, new_h), Image.LANCZOS)
    # Lower half (below screen_y2) at reduced opacity to show mid-phase
    full_byte = char_pil.copy()
    paste_x = byte_cx - full_byte.width // 2
    paste_y = byte_cy - full_byte.height // 2
    # Create overlay with upper half full opacity, lower half faded
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    overlay.paste(full_byte, (paste_x, paste_y), full_byte)
    # Fade lower portion (below screen boundary)
    if screen_y2 < paste_y + full_byte.height:
        for y in range(max(0, screen_y2), min(img.size[1], paste_y + full_byte.height)):
            for x in range(max(0, paste_x), min(img.size[0], paste_x + full_byte.width)):
                r, g, b, a = overlay.getpixel((x, y))
                if a > 0:
                    overlay.putpixel((x, y), (r, g, b, int(a * 0.5)))
    base_rgba = img.convert('RGBA')
    result = Image.alpha_composite(base_rgba, overlay)
    img.paste(result.convert('RGB'))

    # Return geometry for annotations
    head_r = int(body_h * 0.20)
    head_cy = byte_cy - body_h // 2 + head_r
    return head_cy, head_r, body_h


def draw_scene(img):
    draw = ImageDraw.Draw(img)

    # ── 1. UNTILTED CANVAS: draw all scene content ──────────────────────────
    # We draw on the full canvas, then rotate the draw area by -8° and paste back.
    # Caption bar is added AFTER tilt and stays horizontal.

    horizon_y = int(DRAW_H * 0.42)   # low angle: floor dominant

    # Background fill — wall/room contaminated by cyan
    draw.rectangle([0, 0, PW, DRAW_H], fill=WALL_COOL)

    # Far-left warm margin (warm domestic light on the losing side)
    for wx in range(0, int(PW * 0.14)):
        warm_alpha = max(0, int(200 * (1 - wx / (PW * 0.14))))
        draw.line([(wx, 0), (wx, DRAW_H)], fill=(WALL_WARM[0], WALL_WARM[1], WALL_WARM[2]))

    # Warm remnant gradient (left 14% of frame only)
    warm_layer = Image.new('RGBA', (PW, PH), (0, 0, 0, 0))
    wld = ImageDraw.Draw(warm_layer)
    for wx in range(0, int(PW * 0.16)):
        a = max(0, int(180 * (1.0 - wx / (PW * 0.16))))
        wld.line([(wx, 0), (wx, DRAW_H)], fill=(*WARM_AMB, a))
    img.paste(Image.alpha_composite(img.convert('RGBA'), warm_layer).convert('RGB'))
    draw = ImageDraw.Draw(img)

    # ── Secondary monitors (BG) ───────────────────────────────────────────────
    mon_cx_hero = int(PW * 0.60)
    mon_cy_hero = int(DRAW_H * 0.42)
    mon_w_hero  = int(PW * 0.41)
    mon_h_hero  = int(DRAW_H * 0.52)

    draw_secondary_monitors(draw, horizon_y, mon_cx_hero, mon_cy_hero)

    # Ambient cyan bleeds from multiple monitors
    add_glow(img, int(PW * 0.28), int(DRAW_H * 0.22), 90, ELEC_CYAN, steps=4, max_alpha=22)
    draw = ImageDraw.Draw(img)
    add_glow(img, int(PW * 0.82), int(DRAW_H * 0.15), 70, ELEC_CYAN, steps=4, max_alpha=18)
    draw = ImageDraw.Draw(img)

    # ── Floor (low angle — floor dominant) ───────────────────────────────────
    draw.rectangle([0, horizon_y, PW, DRAW_H], fill=FLOOR_CYAN)
    vp_x = int(PW * 0.55)
    vp_y = horizon_y
    for frac in [0.06, 0.20, 0.36, 0.52, 0.68, 0.82, 0.94]:
        fx = int(frac * PW)
        draw.line([(vp_x, vp_y), (fx, DRAW_H)], fill=(30, 60, 75), width=1)

    # Table edge at bottom (low angle — table near camera)
    table_y = int(DRAW_H * 0.92)
    draw.rectangle([0, table_y, PW, DRAW_H],
                   fill=(55, 48, 36))
    draw.line([(0, table_y), (PW, table_y)], fill=(70, 60, 44), width=2)

    # Cable bundles at floor (low angle exaggerates)
    for ci in range(3):
        draw.line([(0, int(DRAW_H * 0.72) + ci * 6),
                   (int(PW * 0.38), int(DRAW_H * 0.88) + ci * 3)],
                  fill=CABLE_DARK if ci % 2 == 0 else CABLE_MED, width=5 - ci)
    for ci in range(3):
        draw.line([(PW, int(DRAW_H * 0.70) + ci * 5),
                   (int(PW * 0.80), int(DRAW_H * 0.86) + ci * 3)],
                  fill=CABLE_DARK if ci % 2 == 0 else CABLE_MED, width=5 - ci)

    # ── Hero monitor ─────────────────────────────────────────────────────────
    scr_bounds, bow_center, bezel_bounds = draw_monitor_hero(
        draw, mon_cx_hero, mon_cy_hero, mon_w_hero, mon_h_hero)
    scr_l, scr_t, scr_r, scr_b = scr_bounds
    bow_cx, bow_cy = bow_center
    bezel_l, bezel_t, bezel_r, bezel_b = bezel_bounds

    # Strong glow from hero monitor face
    add_glow(img, bow_cx, bow_cy, int(mon_w_hero * 0.65),
             ELEC_CYAN, steps=6, max_alpha=45)
    draw = ImageDraw.Draw(img)

    # ── Byte — mid-phase emergence ────────────────────────────────────────────
    # Byte's center: emerging from screen. Body vector slightly upward.
    byte_cx = int(PW * 0.57)
    byte_cy = int(DRAW_H * 0.42)      # body center at screen threshold region
    byte_bh = int(DRAW_H * 0.30)      # body height

    head_cy, head_r, body_h = draw_byte_mid_phase(
        img, draw, byte_cx, byte_cy, byte_bh, screen_y2=int(DRAW_H * 0.50))
    draw = ImageDraw.Draw(img)

    # ELEC_CYAN body glow (Byte's real-world emission — upper half)
    add_glow(img, byte_cx, byte_cy - int(byte_bh * 0.25), int(byte_bh * 0.45),
             ELEC_CYAN, steps=5, max_alpha=40)
    draw = ImageDraw.Draw(img)

    # Confetti burst at screen boundary (crossing threshold)
    threshold_y_burst = byte_cy + int(byte_bh * 0.04)
    draw_confetti_burst(draw, byte_cx, threshold_y_burst,
                        count=40, rng_seed=771, r_spread=int(byte_bh * 0.55))

    # Upward emergence vector annotation (body rising as he comes through)
    vec_x = byte_cx + int(byte_bh * 0.70)
    vec_y_start = byte_cy + int(byte_bh * 0.20)
    vec_y_end   = byte_cy - int(byte_bh * 0.28)
    draw.line([(vec_x, vec_y_start), (vec_x, vec_y_end)],
              fill=ELEC_CYAN_DIM, width=1)
    draw.polygon([(vec_x - 4, vec_y_end + 8), (vec_x + 4, vec_y_end + 8),
                  (vec_x, vec_y_end)], fill=ELEC_CYAN_DIM)
    draw.text((vec_x + 5, (vec_y_start + vec_y_end) // 2),
              "emergence\nvector", font=load_font(8), fill=ELEC_CYAN_DIM)

    # ── Annotations ──────────────────────────────────────────────────────────
    font_ann   = load_font(11)
    font_ann_b = load_font(11, bold=True)

    draw.text((10, 8),
              "P07  /  MED WIDE  /  LOW ANGLE  /  Dutch 8° CW applied to draw area",
              font=font_ann, fill=ANN_COL)
    draw.text((10, 20),
              "Monitor bowing convex. Rings break OUTSIDE bezel (physics violation = danger).",
              font=font_ann, fill=ANN_DIM)
    draw.text((10, 32),
              "Byte: lower half inside screen (dim), upper half real world (full teal). DETERMINED + ALARMED.",
              font=font_ann, fill=ANN_DIM)

    # Threshold line annotation
    thr_y = byte_cy + int(byte_bh * 0.04)
    draw.line([(byte_cx - int(byte_bh * 0.60), thr_y),
               (byte_cx + int(byte_bh * 0.60), thr_y)],
              fill=ELEC_CYAN_HI, width=1)
    draw.text((byte_cx + int(byte_bh * 0.62), thr_y - 6),
              "threshold", font=load_font(8), fill=ELEC_CYAN_HI)

    # Shot / arc labels
    draw.rectangle([10, DRAW_H - 24, 130, DRAW_H - 6], fill=(30, 10, 18))
    draw.text((14, DRAW_H - 22), "MED WIDE / DUTCH 8° / LOW",
              font=font_ann_b, fill=(240, 200, 100))
    draw.rectangle([PW - 155, DRAW_H - 24, PW - 10, DRAW_H - 6], fill=(40, 0, 20))
    draw.text((PW - 151, DRAW_H - 22), "ARC: TENSE → BREACH",
              font=font_ann_b, fill=ARC_COLOR)

    return draw


def make_panel():
    font_cap = load_font(12)
    font_ann = load_font(11)
    font_sm  = load_font(10)

    # ── Render scene content ─────────────────────────────────────────────────
    img = Image.new('RGB', (PW, PH), WALL_COOL)
    draw_scene(img)

    # ── Apply Dutch tilt 8° CW to draw area only (caption stays horizontal) ──
    draw_area = img.crop([0, 0, PW, DRAW_H])
    tilted    = draw_area.rotate(-8, expand=False, fillcolor=DEEP_SPACE)
    img.paste(tilted, (0, 0))

    # ── Caption bar (post-tilt, stays horizontal) ─────────────────────────────
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, DRAW_H, PW, PH], fill=BG_CAPTION)
    draw.line([0, DRAW_H, PW, DRAW_H], fill=(10, 8, 6), width=2)
    draw.text((10, DRAW_H + 4),
              "P07  MED WIDE  low angle  Dutch 8° CW  |  Byte phases through — monitor breach",
              font=font_cap, fill=(155, 148, 122))
    draw.text((10, DRAW_H + 18),
              "Monitor bowing convex. Distortion rings break bezel. Byte: lower half inside / upper half real world.",
              font=font_cap, fill=TEXT_CAP)
    draw.text((10, DRAW_H + 33),
              "Expression: DETERMINED + ALARMED. Warm domestic light far-left only — losing to ELEC_CYAN.",
              font=font_ann, fill=(145, 135, 102))
    draw.text((PW - 230, DRAW_H + 46),
              "LTG_SB_cold_open_P07  /  Diego Vargas  /  C43",
              font=font_sm, fill=(95, 88, 72))

    # Arc border (Hot Magenta — TENSE → BREACH)
    draw.rectangle([0, 0, PW - 1, PH - 1], outline=ARC_COLOR, width=4)

    img.thumbnail((1280, 1280))
    img.save(OUTPUT_PATH, "PNG")
    print(f"Saved: {OUTPUT_PATH}  {img.size}")
    return OUTPUT_PATH


if __name__ == "__main__":
    make_panel()
    print("P07 standalone panel generation complete.")
