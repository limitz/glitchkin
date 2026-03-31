#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_sb_cold_open_P23.py
Cold Open Panel P23 — MED — SHOW'S PROMISE SHOT
Diego Vargas, Storyboard Artist — Cycle 42

Beat: THE PROMISE SHOT. Luma and Byte from behind, both looking at the monitor
      wall ahead of them. Every screen blazing at max intensity. Room gone Full
      Glitch Chaos palette. Luma's posture: shoulders square, chin up — FACING THIS.
      Byte on her shoulder — grumpy, reluctant, but PRESENT.
      Despite having met 3 minutes ago, they are already standing side-by-side.
      THIS IS THE SHOW'S THESIS IN ONE IMAGE.

Shot:   MED — backs to camera, OTS/reverse — we see what they see
Camera: Behind them at their eye levels. Luma standing, Byte shoulder-height.
        Camera begins slight PUSH IN (toward their backs, toward the chaos).
Palette: Warm (Luma) vs Full Glitch (room/monitors). The two palettes together.
Arc:    TENSE (pre-apex) — building to P24

DIALOGUE:
LUMA (quiet, 12-year-old energy): "Grandma's gonna be so mad."
BYTE: "This is ENTIRELY not my problem."
BYTE: "...I will observe from your shoulder."

Image size rule: ≤ 1280px in both dimensions.
Output: output/storyboards/panels/LTG_SB_cold_open_P23.png
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
from LTG_TOOL_char_luma import draw_luma
from LTG_TOOL_char_byte import draw_byte
from LTG_TOOL_cairo_primitives import to_pil_rgba
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

PANELS_DIR = output_dir('storyboards', 'panels')
OUTPUT_PATH = os.path.join(PANELS_DIR, "LTG_SB_cold_open_P23.png")
os.makedirs(PANELS_DIR, exist_ok=True)

PW, PH    = 800, 600
CAPTION_H = 60
DRAW_H    = PH - CAPTION_H   # 540

# ── Palette ──────────────────────────────────────────────────────────────────
# FULL GLITCH CHAOS PALETTE — warm has been mostly overwritten
ELEC_CYAN    = (0, 212, 232)
ELEC_CYAN_DIM= (0, 140, 160)
ELEC_CYAN_HI = (80, 240, 252)
HOT_MAGENTA  = (232, 0, 152)
UV_PURPLE    = (123, 47, 190)
VOID_BLACK   = (10, 10, 20)
DEEP_SPACE   = (18, 16, 32)
# Luma — warm identity (back view — mostly hoodie and hair)
LUMA_HOODIE  = (232, 112, 58)   # canonical orange #E8703A
LUMA_HAIR    = (52, 38, 24)
LUMA_HAIR_HI = (80, 56, 32)
LUMA_PANT    = (140, 112, 168)  # lavender shorts
LUMA_SOCK    = (240, 230, 215)  # cream socks (not shoes)
# Byte
BYTE_TEAL    = (0, 212, 232)
BYTE_DARK    = (0, 80, 100)
BYTE_EYE_W   = (220, 230, 240)
CRACK_LINE   = (200, 30, 100)
# Room (chaos state)
FLOOR_WARM   = (130, 102, 70)   # mostly washed
WALL_DARK    = (22, 18, 30)
SHELF_DARK   = (38, 30, 22)
CRT_PLASTIC  = (48, 40, 32)
# Caption
BG_CAPTION   = (8, 6, 14)
TEXT_CAP     = (220, 215, 235)
ANN_COL      = (180, 155, 100)
ANN_DIM      = (130, 115, 90)
ARC_TENSE    = (232, 0, 152)    # TENSE arc

RNG = random.Random(2323)


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
    for i in range(steps, 0, -1):
        r     = int(r_max * (i / steps))
        alpha = int(max_alpha * (1 - (i / steps) * 0.6))
        glow  = Image.new('RGBA', img.size, (0, 0, 0, 0))
        gd    = ImageDraw.Draw(glow)
        gd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(*color_rgb, alpha))
        base  = img.convert('RGBA')
        img.paste(Image.alpha_composite(base, glow).convert('RGB'))


def draw_irregular_poly(draw, cx, cy, r, sides, color, seed=0, outline=None):
    rng = random.Random(seed)
    pts = []
    for i in range(sides):
        angle = (2 * math.pi * i / sides) + rng.uniform(-0.25, 0.25)
        dist  = r * rng.uniform(0.70, 1.20)
        pts.append((int(cx + dist * math.cos(angle)), int(cy + dist * math.sin(angle))))
    draw.polygon(pts, fill=color, outline=outline)


def draw_monitor_wall(draw, img):
    """
    Draw the monitor wall — every screen blazing at max intensity.
    Bowing forward, screens bulging. Glitch confetti erupting.
    This is what Luma and Byte are LOOKING AT.
    Wall reads from mid-frame upward.
    """
    # Monitor layout: back wall, spread across full width
    monitor_data = [
        # (cx_frac, cy_frac, w_frac, h_frac, brightness)
        (0.07,  0.12, 0.11, 0.18, 0.90),   # far left
        (0.20,  0.08, 0.13, 0.20, 1.00),   # left-center top
        (0.34,  0.06, 0.14, 0.22, 1.00),   # center-left top (main breach)
        (0.50,  0.04, 0.13, 0.20, 0.95),   # center top
        (0.65,  0.07, 0.14, 0.21, 1.00),   # center-right
        (0.80,  0.10, 0.12, 0.18, 0.88),   # right
        (0.91,  0.15, 0.08, 0.14, 0.75),   # far right (partial)
        (0.12,  0.30, 0.10, 0.15, 0.70),   # left mid-height
        (0.73,  0.28, 0.11, 0.16, 0.72),   # right mid-height
    ]

    for i, (cx_f, cy_f, w_f, h_f, bright) in enumerate(monitor_data):
        cx = int(cx_f * PW)
        cy = int(cy_f * DRAW_H)
        mw = int(w_f * PW)
        mh = int(h_f * DRAW_H)

        # Monitor body
        draw.rectangle([cx - mw // 2, cy, cx + mw // 2, cy + mh],
                       fill=CRT_PLASTIC, outline=VOID_BLACK, width=2)

        # Screen (inner)
        sm = 5
        sx0, sx1 = cx - mw // 2 + sm, cx + mw // 2 - sm
        sy0, sy1 = cy + sm, cy + mh - sm

        # Screen fill — ELEC_CYAN intensity at breach level
        bc = int(255 * bright)
        screen_col = (0, min(255, bc), min(255, int(bc * 1.02)))
        draw.rectangle([sx0, sy0, sx1, sy1], fill=screen_col)

        # Scan lines
        for sl_y in range(sy0, sy1, 3):
            draw.line([(sx0, sl_y), (sx1, sl_y)], fill=ELEC_CYAN_DIM, width=1)

        # Screen glow
        scx = (sx0 + sx1) // 2
        scy = (sy0 + sy1) // 2
        add_glow(img, scx, scy, int(mw * 0.65), ELEC_CYAN, steps=4, max_alpha=int(35 * bright))
        draw = ImageDraw.Draw(img)

        # Bulge rings (screens bowing outward toward our characters)
        screen_r = min(sx1 - sx0, sy1 - sy0) // 2
        for ring in range(1, 3):
            rr = int(screen_r * (1.0 + ring * 0.20))
            draw.ellipse([scx - rr, scy - int(rr * 0.80),
                          scx + rr, scy + int(rr * 0.80)],
                         outline=(*ELEC_CYAN_HI, max(0, 45 - ring * 12)), width=1)

        # Pixel confetti erupting from screen edges
        rng = random.Random(i * 91 + 50)
        for ci in range(5):
            conf_x = rng.randint(sx0, sx1)
            conf_y = rng.randint(sy0 - 15, sy0)
            conf_s = rng.randint(3, 7)
            col = ELEC_CYAN if rng.randint(0, 1) == 0 else HOT_MAGENTA
            draw_irregular_poly(draw, conf_x, conf_y, conf_s, 5, col,
                                seed=i * 37 + ci * 11)

    return draw


def draw_floor_and_room(draw, img):
    """Draw the room from floor camera POV."""
    # Horizon / floor boundary
    horizon_y = int(DRAW_H * 0.50)

    # Back wall / ceiling — dark, glitch-lit
    draw.rectangle([0, 0, PW, horizon_y], fill=WALL_DARK)

    # Shelving shapes on wall edges (barely legible)
    for shelf_x, shelf_y, shelf_w, shelf_h in [
        (0, int(DRAW_H * 0.28), int(PW * 0.10), int(DRAW_H * 0.18)),
        (int(PW * 0.90), int(DRAW_H * 0.26), int(PW * 0.10), int(DRAW_H * 0.20)),
    ]:
        draw.rectangle([shelf_x, shelf_y, shelf_x + shelf_w, shelf_y + shelf_h],
                       fill=SHELF_DARK)

    # Floor (warm, seen from mid-height camera)
    draw.rectangle([0, horizon_y, PW, DRAW_H], fill=FLOOR_WARM)

    # Floor perspective lines
    vp_x = int(PW * 0.50)
    vp_y = horizon_y
    for frac in [0.08, 0.22, 0.35, 0.50, 0.65, 0.78, 0.92]:
        fx = int(frac * PW)
        draw.line([(vp_x, vp_y), (fx, DRAW_H)], fill=(100, 80, 56), width=1)

    # Cyan glow flood on floor from monitors
    add_glow(img, PW // 2, horizon_y, int(PW * 0.50), ELEC_CYAN, steps=4, max_alpha=18)
    draw = ImageDraw.Draw(img)

    # Magenta corner accents (shadow area)
    add_glow(img, 0, int(DRAW_H * 0.42), 150, HOT_MAGENTA, steps=3, max_alpha=14)
    add_glow(img, PW, int(DRAW_H * 0.42), 140, HOT_MAGENTA, steps=3, max_alpha=12)
    draw = ImageDraw.Draw(img)

    return draw






def draw_confetti_approaching(draw, img):
    """
    Pixel confetti approaching the characters from the monitor wall ahead.
    Drifts toward camera (toward us — toward Luma and Byte).
    More dense near the monitors, sparse near Luma.
    """
    rng = random.Random(777)
    for ci in range(130):
        # Concentrated toward mid-frame, spreading left/right
        cx = rng.randint(0, PW)
        # Y: mostly in upper half (coming from monitor wall)
        cy = rng.randint(5, int(DRAW_H * 0.75))
        cs = rng.randint(2, 6)
        # Size inversely related to Y depth (closer = slightly larger)
        size_scale = 0.6 + (cy / DRAW_H) * 0.8
        cs = max(2, int(cs * size_scale))
        col_choice = rng.randint(0, 3)
        if col_choice == 0:
            col = ELEC_CYAN
        elif col_choice == 1:
            col = HOT_MAGENTA
        elif col_choice == 2:
            col = UV_PURPLE
        else:
            col = ELEC_CYAN_HI
        draw_irregular_poly(draw, cx, cy, cs, rng.randint(4, 6), col,
                            seed=ci * 13 + 500)



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

def draw_luma_back(draw, img, luma_cx, luma_floor_y, body_h):
    """Luma from back — canonical renderer (DETERMINED, facing away)."""
    scale = body_h / 400.0
    surface = draw_luma(expression="DETERMINED", scale=scale, facing="left")
    char_pil = _char_to_pil(surface)
    if char_pil.height > 0:
        aspect = char_pil.width / char_pil.height
        new_h = body_h
        new_w = int(new_h * aspect)
        char_pil = char_pil.resize((new_w, new_h), Image.LANCZOS)
    _composite_char(img, char_pil, luma_cx, luma_floor_y - char_pil.height // 2)


def draw_byte_shoulder_back(draw, img, byte_cx, byte_cy, body_h):
    """Byte on shoulder from back — canonical renderer."""
    scale = body_h / 88.0
    surface = draw_byte(expression="neutral", scale=scale, facing="left")
    char_pil = _char_to_pil(surface)
    if char_pil.height > 0:
        aspect = char_pil.width / char_pil.height
        new_h = body_h
        new_w = int(new_h * aspect)
        char_pil = char_pil.resize((new_w, new_h), Image.LANCZOS)
    _composite_char(img, char_pil, byte_cx, byte_cy)


def draw_scene(img):
    draw = ImageDraw.Draw(img)

    # ── ROOM (chaos palette) ──────────────────────────────────────────────────
    draw = draw_floor_and_room(draw, img)

    # ── MONITOR WALL (what they're looking at) ────────────────────────────────
    draw = draw_monitor_wall(draw, img)

    # ── Approaching confetti ───────────────────────────────────────────────────
    draw_confetti_approaching(draw, img)
    draw = ImageDraw.Draw(img)

    # ── LUMA — back view, center-left ─────────────────────────────────────────
    # Luma center-left gives room for Byte on her right shoulder to read.
    luma_cx      = int(PW * 0.44)
    luma_floor_y = int(DRAW_H * 0.97)
    luma_body_h  = int(DRAW_H * 0.60)

    draw = draw_luma_back(draw, img, luma_cx, luma_floor_y, luma_body_h)
    draw = ImageDraw.Draw(img)

    # ── BYTE — on Luma's right shoulder ───────────────────────────────────────
    # From behind: Byte is on the RIGHT shoulder (camera-left from behind).
    # He's turned slightly too — looking at the monitors.
    shoulder_y = luma_floor_y - int(luma_body_h * 0.70)
    shoulder_x = luma_cx + int(luma_body_h * 0.20)
    byte_body_h = int(luma_body_h * 0.13)
    draw = draw_byte_shoulder_back(draw, img, shoulder_x, shoulder_y, byte_body_h)
    draw = ImageDraw.Draw(img)

    # ── CAMERA PUSH ANNOTATION ────────────────────────────────────────────────
    # Arrow indicating slight push toward characters' backs
    font_ann  = load_font(11)
    font_ann_b = load_font(11, bold=True)

    push_cx = int(PW * 0.88)
    push_y0 = int(DRAW_H * 0.60)
    push_y1 = int(DRAW_H * 0.52)
    draw.line([(push_cx, push_y0), (push_cx, push_y1)],
              fill=(180, 160, 100), width=2)
    draw.polygon([(push_cx - 5, push_y1 + 8), (push_cx + 5, push_y1 + 8),
                  (push_cx, push_y1)], fill=(180, 160, 100))
    draw.text((push_cx - 22, push_y0 + 3), "PUSH IN",
              font=load_font(9), fill=(180, 160, 100))

    # ── Panel annotations ─────────────────────────────────────────────────────
    draw.text((10, 8), "P23  /  MED  /  behind chars (OTS reverse)  /  eye level  /  PUSH IN",
              font=font_ann, fill=ANN_COL)
    draw.text((10, 20), "PROMISE SHOT. Luma + Byte facing chaos. Show thesis in one image.",
              font=font_ann, fill=(0, 200, 220))
    draw.text((10, 32), "Despite 3 min acquaintance: side by side. Warm (Luma) vs Glitch (room).",
              font=font_ann, fill=ANN_DIM)

    # Character labels
    draw.text((luma_cx - int(luma_body_h * 0.25), luma_floor_y - luma_body_h - 14),
              "LUMA\n(center-left)",
              font=load_font(9), fill=(220, 160, 80))
    draw.text((shoulder_x + 8, shoulder_y - byte_body_h - 12),
              "BYTE\n(shoulder)",
              font=load_font(9), fill=ELEC_CYAN_DIM)

    # Shot label
    draw.rectangle([10, DRAW_H - 24, 108, DRAW_H - 6], fill=(20, 10, 12))
    draw.text((14, DRAW_H - 22), "MED / OTS REV",
              font=font_ann_b, fill=(240, 220, 140))

    # Arc indicator
    draw.rectangle([PW - 130, DRAW_H - 24, PW - 10, DRAW_H - 6], fill=(40, 0, 20))
    draw.text((PW - 126, DRAW_H - 22), "ARC: TENSE",
              font=font_ann_b, fill=ARC_TENSE)

    return draw


def make_panel():
    font_cap  = load_font(12)
    font_ann  = load_font(11)
    font_sm   = load_font(10)

    img  = Image.new('RGB', (PW, PH), DEEP_SPACE)
    draw_scene(img)
    draw = ImageDraw.Draw(img)

    # Caption bar
    draw.rectangle([0, DRAW_H, PW, PH], fill=BG_CAPTION)
    draw.line([0, DRAW_H, PW, DRAW_H], fill=(8, 6, 14), width=2)
    draw.text((10, DRAW_H + 4),
              "P23  MED  behind chars (OTS reverse)  |  SHOW'S PROMISE SHOT",
              font=font_cap, fill=(160, 150, 175))
    draw.text((10, DRAW_H + 18),
              "Luma + Byte (backs to camera) facing monitor wall. Every screen blazing.",
              font=font_cap, fill=TEXT_CAP)
    draw.text((10, DRAW_H + 33),
              "LUMA: \"Grandma's gonna be so mad.\"  BYTE: \"...I will observe from your shoulder.\"",
              font=font_ann, fill=(140, 130, 100))
    draw.text((PW - 230, DRAW_H + 46), "LTG_SB_cold_open_P23  /  Diego Vargas  /  C42",
              font=font_sm, fill=(100, 95, 108))

    # Arc border — hot magenta (TENSE)
    draw.rectangle([0, 0, PW - 1, PH - 1], outline=ARC_TENSE, width=3)

    img.thumbnail((1280, 1280))
    img.save(OUTPUT_PATH, "PNG")
    print(f"Saved: {OUTPUT_PATH}  {img.size}")
    return OUTPUT_PATH


if __name__ == "__main__":
    make_panel()
    print("P23 standalone panel generation complete.")
