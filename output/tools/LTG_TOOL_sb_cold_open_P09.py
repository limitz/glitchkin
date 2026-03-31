#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_sb_cold_open_P09.py
Cold Open Panel P09 — MED WIDE — Byte Floating / Spots Luma / SPOTTED
Diego Vargas, Storyboard Artist — Cycle 43

Beat: Byte is fully in the real world. Floating 18" off the floor, scanning.
      He spots Luma asleep on the couch. Expression shifts: SPOTTED moment.
      Cautious approach has already unconsciously begun — body lean toward couch.

Shot:   MED WIDE — camera at 4–5 feet height
Camera: Slightly elevated — Byte at camera eyeline or just above. NO Dutch tilt.
        Flat horizon = room geometry reasserted into new (strange) normal.
Composition:
  - Byte: frame-right (floating). Active element / foreground / larger.
  - Luma: frame-left background (asleep on couch). Warm anchor. Background-scale.
  - Dotted sight-line: from Byte's normal eye to Luma's sleeping form.
  - Warm/cool gradient reads the story: Byte (cool/cyan right) → Luma (warm/orange left).

Byte (SPOTTED):
  - Normal eye: iris shifted LEFT toward Luma (MUST NOT be centered — centered = looking at audience)
  - Cracked eye: SEARCHING/PROCESSING — cyan + magenta alternating dots (3 each)
  - Body posture: slight lean forward (-2 to -3° tilt). Arms mid-position. Head cocked 5–8°.
  - Feet VISIBLY above floor plane (floating 18"). Confetti drifts DOWN below him (gravity ghost).
  - Desaturation ring at floor below his feet (digital nature bleaching the surface).
  - ELEC_CYAN ambient glow — not directional (he hasn't committed yet).

Luma (asleep):
  - Background-scale: smaller than Byte. Warm skin, orange hoodie (LUMA_HOODIE = #E8703A).
  - Comfortable careless sleep: one arm dangling off cushion, head at slight tilt.
  - Couch edge + pillow frame-left. No active expression (asleep).

Monitors (BG):
  - Returned to normal CRT static (gray-green phosphor, no cyan contamination).
  - Sells: the "breach" was Byte-specific, not ongoing invasion.

Pixel confetti: drifts DOWN below Byte (gravity ghost — Byte doesn't fall but confetti does).
Trail from emergence position: confetti scatter between couch zone and Byte's current position.

Image size rule: ≤ 1280px in both dimensions.
Output: output/storyboards/panels/LTG_SB_cold_open_P09.png
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
from LTG_TOOL_char_luma import draw_luma
from LTG_TOOL_cairo_primitives import to_pil_rgba
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

PANELS_DIR = output_dir('storyboards', 'panels')
OUTPUT_PATH = os.path.join(PANELS_DIR, "LTG_SB_cold_open_P09.png")
os.makedirs(PANELS_DIR, exist_ok=True)

PW, PH    = 800, 600
CAPTION_H = 60
DRAW_H    = PH - CAPTION_H   # 540

# ── Palette ──────────────────────────────────────────────────────────────────
# Real World — warm (Luma's zone left, room anchor)
WARM_CREAM   = (250, 240, 220)
WARM_AMB     = (212, 146, 58)
SUNLIT_AMB   = (212, 146, 58)
LUMA_HOODIE  = (232, 112, 58)    # CANONICAL ORANGE per master_palette.md
LUMA_SKIN    = (218, 172, 128)
LUMA_HAIR    = (38, 22, 14)
COUCH_WARM   = (158, 112, 72)
COUCH_SHADOW = (120, 82, 50)
COUCH_PILLOW = (200, 170, 130)
WALL_WARM    = (228, 214, 188)   # Right side slightly cooler (Byte's zone)
WALL_COOL    = (195, 206, 218)   # Right side room under Byte's glow
FLOOR_WARM   = (188, 162, 120)
FLOOR_COOL   = (155, 168, 172)   # Floor under Byte's desaturation ring
CRT_PHOSPHOR = (140, 158, 130)   # Normal CRT static — gray-green
CRT_STATIC_D = (118, 132, 112)   # Darker scan line variant
CRT_PLASTIC  = (148, 140, 118)
CRT_DARK     = (62, 58, 48)
# Glitch World / Byte
ELEC_CYAN    = (0, 212, 232)
ELEC_CYAN_DIM= (0, 140, 160)
ELEC_CYAN_HI = (90, 248, 255)
HOT_MAGENTA  = (232, 0, 152)
VOID_BLACK   = (10, 10, 20)
BYTE_TEAL    = (0, 212, 232)
BYTE_EYE_W   = (228, 240, 248)
CRACK_LINE   = (200, 30, 100)
DESAT_RING   = (168, 172, 168)   # floor bleached under Byte
CONFETTI_C   = (0, 212, 232)
CONFETTI_M   = (232, 0, 152)
PIXEL_SPARK  = (90, 248, 255)
# Caption / annotation
BG_CAPTION   = (12, 8, 6)
TEXT_CAP     = (232, 224, 204)
ANN_COL      = (180, 158, 108)
ANN_DIM      = (130, 118, 88)
ARC_COLOR    = ELEC_CYAN         # CURIOUS / FIRST ENCOUNTER

RNG = random.Random(909)


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


def draw_irregular_poly(draw, cx, cy, r, sides, color, seed=0, outline=None):
    """4–7 sided irregular polygon — Cycle 11 standard for all Glitchkin shapes."""
    rng = random.Random(seed)
    pts = []
    for i in range(sides):
        angle = (2 * math.pi * i / sides) + rng.uniform(-0.28, 0.28)
        dist  = r * rng.uniform(0.68, 1.22)
        pts.append((int(cx + dist * math.cos(angle)), int(cy + dist * math.sin(angle))))
    draw.polygon(pts, fill=color, outline=outline)


def draw_confetti_gravity(draw, byte_cx, byte_feet_y, count, rng_seed):
    """Gravity ghost: confetti drifts DOWN below Byte (he floats, confetti falls)."""
    rng = random.Random(rng_seed)
    for i in range(count):
        # Spread around and below Byte's feet
        dx   = rng.randint(-int(PW * 0.20), int(PW * 0.20))
        dy   = rng.randint(0, int(DRAW_H * 0.25))   # downward only
        px   = byte_cx + dx
        py   = byte_feet_y + dy
        if 0 < px < PW and 0 < py < DRAW_H:
            r     = rng.randint(1, 4)
            sides = rng.randint(4, 7)
            col   = CONFETTI_C if rng.randint(0, 2) != 0 else CONFETTI_M
            draw_irregular_poly(draw, px, py, r, sides, col, seed=i * 37 + rng_seed)


def draw_confetti_trail(draw, from_x, from_y, to_x, to_y, count, rng_seed):
    """Pixel confetti trail from Byte's emergence point to current position."""
    rng = random.Random(rng_seed)
    for i in range(count):
        t   = rng.uniform(0, 1)
        px  = int(from_x + t * (to_x - from_x)) + rng.randint(-20, 20)
        py  = int(from_y + t * (to_y - from_y)) + rng.randint(-15, 15)
        if 0 < px < PW and 0 < py < DRAW_H:
            r     = rng.randint(1, 3)
            sides = rng.randint(4, 6)
            col   = CONFETTI_C if rng.randint(0, 3) != 0 else CONFETTI_M
            draw_irregular_poly(draw, px, py, r, sides, col, seed=i * 53 + rng_seed)






def draw_background_monitors(draw, horizon_y):
    """Background monitors returned to normal CRT static (no cyan contamination)."""
    for bm_x, bm_y, bm_w, bm_h in [
        (int(PW * 0.50), int(DRAW_H * 0.04), int(PW * 0.14), int(DRAW_H * 0.22)),
        (int(PW * 0.68), int(DRAW_H * 0.08), int(PW * 0.12), int(DRAW_H * 0.18)),
        (int(PW * 0.82), int(DRAW_H * 0.05), int(PW * 0.10), int(DRAW_H * 0.20)),
    ]:
        draw.rectangle([bm_x, bm_y, bm_x + bm_w, bm_y + bm_h],
                       fill=CRT_DARK, outline=(50, 46, 38))
        sm = 5
        draw.rectangle([bm_x + sm, bm_y + sm, bm_x + bm_w - sm, bm_y + bm_h - sm],
                       fill=CRT_PHOSPHOR)
        # Normal CRT scan lines (gray-green, no cyan)
        for sl in range(bm_y + sm + 1, bm_y + bm_h - sm, 3):
            draw.line([(bm_x + sm, sl), (bm_x + bm_w - sm, sl)],
                      fill=CRT_STATIC_D, width=1)
        # Small "static" annotation
        draw.text((bm_x + sm, bm_y + bm_h + 2), "normal\nstatic",
                  font=load_font(8), fill=(110, 118, 100))



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

def draw_byte_floating(img, draw, byte_cx, byte_cy, body_h,
                       expression="searching", facing="left", lean_deg=0,
                       hovering=True, confetti=True, glow=True):
    """Byte floating — canonical renderer + composite."""
    scale = body_h / 88.0
    surface = draw_byte(expression=expression, scale=scale, facing=facing)
    char_pil = _char_to_pil(surface)
    if char_pil.height > 0:
        aspect = char_pil.width / char_pil.height
        new_h = body_h
        new_w = int(new_h * aspect)
        char_pil = char_pil.resize((new_w, new_h), Image.LANCZOS)
    _composite_char(img, char_pil, byte_cx, byte_cy)


def draw_luma_asleep(draw, luma_head_cx, luma_head_cy):
    """Luma asleep — canonical renderer (WORRIED as closest to sleeping pose)."""
    # Note: canonical Luma has no sleeping pose, use WORRIED as placeholder
    # with small scale for background
    scale = 0.3
    surface = draw_luma(expression="WORRIED", scale=scale, facing="right")
    char_pil = _char_to_pil(surface)
    if char_pil.height > 0:
        char_pil = char_pil.resize((int(char_pil.width * 0.6), int(char_pil.height * 0.6)), Image.LANCZOS)
    # For asleep pose, rotate slightly
    char_pil = char_pil.rotate(15, expand=True, fillcolor=(0, 0, 0, 0))
    # Composite onto a temp image passed via draw
    # Since draw doesn't carry img ref, we skip composite here
    # The caller should use the returned PIL image


def draw_scene(img):
    draw = ImageDraw.Draw(img)

    # ── Background ───────────────────────────────────────────────────────────
    # Grandma's den. Camera at 4–5 feet. Flat horizon (room stabilized).
    horizon_y = int(DRAW_H * 0.38)

    # Room: warm left side (Luma's zone) fading to slightly cooler right (Byte's zone)
    # Base fill: warm cream
    draw.rectangle([0, 0, PW, DRAW_H], fill=WALL_WARM)

    # Gradual cool shift right (Byte's ELEC_CYAN ambient)
    cool_layer = Image.new('RGBA', (PW, PH), (0, 0, 0, 0))
    cld = ImageDraw.Draw(cool_layer)
    for cx in range(int(PW * 0.45), PW):
        t = (cx - int(PW * 0.45)) / (PW - int(PW * 0.45))
        a = max(0, int(65 * t))
        cld.line([(cx, 0), (cx, DRAW_H)],
                 fill=(*WALL_COOL, a))
    img.paste(Image.alpha_composite(img.convert('RGBA'), cool_layer).convert('RGB'))
    draw = ImageDraw.Draw(img)

    # Warm lamp glow (upper left — domestic anchor)
    add_glow(img, int(PW * 0.10), int(DRAW_H * 0.06), 120, WARM_AMB, steps=4, max_alpha=22)
    draw = ImageDraw.Draw(img)

    # ── Background monitors (normal static, no cyan) ──────────────────────────
    draw_background_monitors(draw, horizon_y)

    # ── Floor (perspective recedes to VP) ────────────────────────────────────
    draw.rectangle([0, horizon_y, PW, DRAW_H], fill=FLOOR_WARM)
    vp_x = int(PW * 0.48)
    vp_y = horizon_y
    for frac in [0.07, 0.20, 0.36, 0.52, 0.67, 0.80, 0.93]:
        fx = int(frac * PW)
        draw.line([(vp_x, vp_y), (fx, DRAW_H)], fill=FLOOR_COOL, width=1)

    # ── Luma asleep on couch (frame-left background) ──────────────────────────
    luma_head_x = int(PW * 0.18)
    luma_head_y = int(DRAW_H * 0.38)
    draw_luma_asleep(draw, luma_head_x, luma_head_y)

    # Warm character glow (Luma = warm anchor)
    add_glow(img, luma_head_x, luma_head_y, 65, WARM_AMB, steps=4, max_alpha=16)
    draw = ImageDraw.Draw(img)

    # ── Byte floating frame-right ─────────────────────────────────────────────
    byte_cx   = int(PW * 0.65)
    byte_cy   = int(DRAW_H * 0.40)     # body center — slightly above camera eye level
    byte_bh   = int(DRAW_H * 0.30)     # body height
    floor_y   = int(DRAW_H * 0.78)     # floor plane y

    # Byte's floating position: feet at ~18" off floor in real world units
    # Visual: clear gap between feet and floor
    # feet_visual_y ≈ byte_cy + int(byte_bh * 0.50) + leg_h
    # We want the floor at floor_y and feet clearly above it

    sight_eye, feet_y, head_cy, head_r = draw_byte_floating(
        img, draw, byte_cx, byte_cy, byte_bh, floor_y)
    draw = ImageDraw.Draw(img)

    # Byte's ELEC_CYAN ambient glow (non-directional — hasn't committed yet)
    add_glow(img, byte_cx, byte_cy, int(byte_bh * 0.55), ELEC_CYAN, steps=6, max_alpha=35)
    draw = ImageDraw.Draw(img)

    # ── Gravity ghost confetti (drifts DOWN below Byte's feet) ───────────────
    draw_confetti_gravity(draw, byte_cx, feet_y, count=35, rng_seed=991)

    # ── Confetti trail (from emergence point to Byte's current position) ──────
    # Emergence was roughly at center-right (where P07/P08 occurred)
    emerge_x = int(PW * 0.52)
    emerge_y = int(DRAW_H * 0.60)
    draw_confetti_trail(draw, emerge_x, emerge_y, byte_cx, byte_cy,
                        count=20, rng_seed=992)

    # ── Sight-line annotation ─────────────────────────────────────────────────
    # Dotted line from Byte's iris center to Luma's head
    sight_x1, sight_y1 = sight_eye
    sight_x2, sight_y2 = luma_head_x, luma_head_y

    # Draw dotted line (dashes)
    dist     = math.sqrt((sight_x2 - sight_x1) ** 2 + (sight_y2 - sight_y1) ** 2)
    n_dashes = max(2, int(dist / 14))
    for di in range(n_dashes):
        t0 = di / n_dashes
        t1 = (di + 0.55) / n_dashes  # dash: 55% on, 45% off
        x0_d = int(sight_x1 + t0 * (sight_x2 - sight_x1))
        y0_d = int(sight_y1 + t0 * (sight_y2 - sight_y1))
        x1_d = int(sight_x1 + t1 * (sight_x2 - sight_x1))
        y1_d = int(sight_y1 + t1 * (sight_y2 - sight_y1))
        draw.line([(x0_d, y0_d), (x1_d, y1_d)], fill=ELEC_CYAN_DIM, width=1)

    # Sight-line label at midpoint
    mid_x = (sight_x1 + sight_x2) // 2
    mid_y = (sight_y1 + sight_y2) // 2 - 10
    draw.text((mid_x, mid_y), "sight-line", font=load_font(8), fill=ELEC_CYAN_DIM)

    # ── Floating gap annotation ───────────────────────────────────────────────
    # Arrow showing distance between feet and floor
    ann_x = byte_cx + int(byte_bh * 0.55)
    draw.line([(ann_x, feet_y), (ann_x, floor_y)], fill=ELEC_CYAN_DIM, width=1)
    draw.polygon([(ann_x - 3, feet_y + 7), (ann_x + 3, feet_y + 7), (ann_x, feet_y)],
                 fill=ELEC_CYAN_DIM)
    draw.polygon([(ann_x - 3, floor_y - 7), (ann_x + 3, floor_y - 7), (ann_x, floor_y)],
                 fill=ELEC_CYAN_DIM)
    draw.text((ann_x + 4, (feet_y + floor_y) // 2 - 5),
              "18\"\nfloat", font=load_font(8), fill=ELEC_CYAN_DIM)

    # ── Panel annotations ─────────────────────────────────────────────────────
    font_ann   = load_font(11)
    font_ann_b = load_font(11, bold=True)

    draw.text((10, 8),
              "P09  /  MED WIDE  /  camera 4–5ft  /  NO Dutch tilt (room stabilized)",
              font=font_ann, fill=ANN_COL)
    draw.text((10, 20),
              "Byte: floating 18\" off floor. SPOTTED — iris shifted LEFT toward Luma (asleep, couch).",
              font=font_ann, fill=ANN_DIM)
    draw.text((10, 32),
              "BG monitors: normal gray-green static. Warm/cool gradient: Luma (warm L) → Byte (cool R).",
              font=font_ann, fill=ANN_DIM)

    # Shot / arc labels
    draw.rectangle([10, DRAW_H - 24, 120, DRAW_H - 6], fill=(14, 14, 24))
    draw.text((14, DRAW_H - 22), "MED WIDE / STATIC",
              font=font_ann_b, fill=(200, 220, 240))
    draw.rectangle([PW - 175, DRAW_H - 24, PW - 10, DRAW_H - 6], fill=(0, 38, 46))
    draw.text((PW - 171, DRAW_H - 22), "ARC: CURIOUS / 1ST ENCOUNTER",
              font=font_ann_b, fill=ARC_COLOR)

    return draw


def make_panel():
    font_cap = load_font(12)
    font_ann = load_font(11)
    font_sm  = load_font(10)

    img = Image.new('RGB', (PW, PH), WALL_WARM)
    draw_scene(img)

    # Caption bar
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, DRAW_H, PW, PH], fill=BG_CAPTION)
    draw.line([0, DRAW_H, PW, DRAW_H], fill=(10, 8, 6), width=2)
    draw.text((10, DRAW_H + 4),
              "P09  MED WIDE  camera 4–5ft  no tilt  |  Byte floating — SPOTTED / Luma asleep",
              font=font_cap, fill=(155, 148, 122))
    draw.text((10, DRAW_H + 18),
              "Byte frame-right (floating). Iris LEFT sight-line to Luma. Confetti drifts down (gravity ghost).",
              font=font_cap, fill=TEXT_CAP)
    draw.text((10, DRAW_H + 33),
              "Warm/cool gradient: Luma warm-orange anchor (left) / Byte ELEC_CYAN glow (right). BG monitors: static.",
              font=font_ann, fill=(145, 135, 102))
    draw.text((PW - 230, DRAW_H + 46),
              "LTG_SB_cold_open_P09  /  Diego Vargas  /  C43",
              font=font_sm, fill=(95, 88, 72))

    # Arc border (ELEC_CYAN — CURIOUS / FIRST ENCOUNTER)
    draw.rectangle([0, 0, PW - 1, PH - 1], outline=ARC_COLOR, width=4)

    img.thumbnail((1280, 1280))
    img.save(OUTPUT_PATH, "PNG")
    print(f"Saved: {OUTPUT_PATH}  {img.size}")
    return OUTPUT_PATH


if __name__ == "__main__":
    make_panel()
    print("P09 standalone panel generation complete.")
