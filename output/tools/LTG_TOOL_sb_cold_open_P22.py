#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_sb_cold_open_P22.py
Cold Open Panel P22 — ECU MONITOR — Multiple Glitchkin Pressing Against Glass
Diego Vargas, Storyboard Artist — Cycle 48

Beat: After P21's wide high-angle re-escalation, we CUT IN to what the monitors are actually
      showing. This is the ECU payoff of P21's "all monitors blazing" — we are NOW inside
      the glass. Multiple Glitchkin hands and faces pressed flat against CRT screen from the
      inside. Screen surface ripples. The glass itself is failing.

      This panel's function: make the audience SEE the individual Glitchkin (not just colored
      blobs). Each one pressing has a distinct face/hand — they are individuals, not a swarm.
      This is why we need the ECU.

Camera: ECU. Single monitor fills the frame. We are RIGHT UP to the glass. The CRT bezel
        frames the entire draw area (screen IS the shot). No Dutch tilt — the screen itself
        is stable, it is what is INSIDE that is chaotic.

Key staging:
  - CRT bezel fills frame edges — we are looking AT a single monitor, extreme close
  - Screen interior: 3-4 distinct Glitchkin pressing against glass
  - Each Glitchkin has a unique expression/posture:
    (1) Center-right: face pressed flat, wide eyes (eager), both palms on glass
    (2) Upper-left: only hand visible, fingers splayed, pressing hard (distortion rings)
    (3) Lower-center: face sideways against glass (squished), one eye visible, cracked
    (4) Center-left: smaller, further back, both hands but no face (hiding/shy)
  - Screen ripple distortion rings radiating from each press point
  - CRT static/scanline texture behind the Glitchkin (they are IN the static)
  - Screen cracks beginning at the strongest press point (center-right)
  - Phosphor band artifacts — the screen is under physical stress

Arc: TENSE / ESCALATION (HOT_MAGENTA border — the breach is spreading).
Output: output/storyboards/panels/LTG_SB_cold_open_P22.png
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
from LTG_TOOL_char_glitch import draw_glitch
from LTG_TOOL_cairo_primitives import to_pil_rgba
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

PANELS_DIR = output_dir('storyboards', 'panels')
OUTPUT_PATH = os.path.join(PANELS_DIR, "LTG_SB_cold_open_P22.png")
os.makedirs(PANELS_DIR, exist_ok=True)

PW, PH    = 800, 600
CAPTION_H = 72
DRAW_H    = PH - CAPTION_H   # 528

# ── Palette ──────────────────────────────────────────────────────────────────
VOID_BLACK    = (10, 10, 20)
ELEC_CYAN     = (0, 212, 232)
ELEC_CYAN_DIM = (0, 100, 120)
HOT_MAGENTA   = (232, 0, 152)
DEEP_SPACE    = (6, 4, 14)
BYTE_TEAL     = (0, 212, 232)
BYTE_BODY_DK  = (0, 150, 168)
STATIC_CYAN   = (0, 60, 70)
BEZEL_DARK    = (18, 14, 10)
BEZEL_EDGE    = (38, 30, 24)
SCREEN_BASE   = (4, 8, 12)

BG_CAPTION    = (12, 8, 6)
TEXT_SHOT     = (232, 224, 204)
TEXT_DESC     = (155, 148, 122)
TEXT_META     = (88, 82, 66)
ARC_COLOR     = HOT_MAGENTA
ANN_COLOR     = (220, 200, 80)
ANN_CYAN      = (0, 180, 210)
ANN_DIM       = (80, 90, 100)

RNG = random.Random(2222)


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
    for i in range(steps, 0, -1):
        r     = int(r_max * (i / steps))
        alpha = int(max_alpha * (1 - (i / steps) * 0.6))
        glow  = Image.new('RGBA', img.size, (0, 0, 0, 0))
        gd    = ImageDraw.Draw(glow)
        gd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(*color_rgb, alpha))
        base  = img.convert('RGBA')
        img.paste(Image.alpha_composite(base, glow).convert('RGB'))


def draw_irregular_poly(draw, cx, cy, r, sides, color, rng, fill=True):
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


def draw_distortion_rings(draw, cx, cy, count, base_r, rng):
    """Draw concentric distortion rings radiating from a press point."""
    for i in range(count):
        r = base_r + i * RNG.randint(8, 14)
        ring_alpha_t = 1.0 - (i / count) * 0.7
        ring_color = lerp_color(ELEC_CYAN, (255, 255, 255), 0.2 * ring_alpha_t)
        draw.ellipse([cx - r, cy - int(r * 0.85), cx + r, cy + int(r * 0.85)],
                     outline=ring_color, width=1)






def draw_screen_cracks(draw, origin_x, origin_y, length, branches, rng):
    """Draw screen cracks radiating from a stress point."""
    for _ in range(branches):
        angle = rng.uniform(0, 2 * math.pi)
        segs = rng.randint(3, 6)
        x, y = origin_x, origin_y
        for s in range(segs):
            seg_len = length / segs * rng.uniform(0.5, 1.5)
            angle += rng.uniform(-0.5, 0.5)
            nx = int(x + seg_len * math.cos(angle))
            ny = int(y + seg_len * math.sin(angle))
            draw.line([(x, y), (nx, ny)], fill=(255, 255, 255), width=1)
            x, y = nx, ny
            # Sub-branch occasionally
            if rng.random() > 0.65:
                ba = angle + rng.uniform(-1.0, 1.0)
                blen = seg_len * 0.5
                bx = int(x + blen * math.cos(ba))
                by = int(y + blen * math.sin(ba))
                draw.line([(x, y), (bx, by)], fill=(200, 200, 210), width=1)



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

def draw_glitchkin_face_ecl(draw, cx, cy, face_r, expression, rng):
    """Glitchkin face ECL — canonical renderer."""
    expr_map = {"neutral": "neutral", "mischievous": "mischievous",
                "panicked": "panicked", "triumphant": "triumphant"}
    expr = expr_map.get(expression, "neutral")
    scale = face_r / 38.0
    surface = draw_glitch(expression=expr, scale=scale, facing="front")
    char_pil = _char_to_pil(surface)
    if char_pil.height > 0:
        target_h = int(face_r * 2.5)
        aspect = char_pil.width / char_pil.height
        new_w = int(target_h * aspect)
        char_pil = char_pil.resize((new_w, target_h), Image.LANCZOS)
    try:
        img = draw._image
        _composite_char(img, char_pil, cx, cy)
    except AttributeError:
        pass


def draw_glitchkin_hand(draw, cx, cy, size, splay, rng):
    """Glitchkin hand — canonical renderer (uses Glitch as proxy)."""
    scale = size / 76.0
    surface = draw_glitch(expression="mischievous", scale=scale, facing="front")
    char_pil = _char_to_pil(surface)
    if char_pil.height > 0:
        target_h = size
        aspect = char_pil.width / char_pil.height
        new_w = int(target_h * aspect)
        char_pil = char_pil.resize((new_w, target_h), Image.LANCZOS)
    try:
        img = draw._image
        _composite_char(img, char_pil, cx, cy)
    except AttributeError:
        pass


def draw_panel():
    img  = Image.new('RGB', (PW, DRAW_H), SCREEN_BASE)
    draw = ImageDraw.Draw(img)

    # ── CRT Bezel — fills the frame edges ────────────────────────────────────
    bezel_w = 28  # thick bezel at ECU
    # Outer bezel
    draw.rectangle([0, 0, PW - 1, DRAW_H - 1], outline=BEZEL_DARK, width=bezel_w)
    # Inner bezel edge highlight
    draw.rectangle([bezel_w - 3, bezel_w - 3,
                    PW - bezel_w + 2, DRAW_H - bezel_w + 2],
                   outline=BEZEL_EDGE, width=2)

    # Screen area bounds
    sx1, sy1 = bezel_w, bezel_w
    sx2, sy2 = PW - bezel_w, DRAW_H - bezel_w
    sw, sh = sx2 - sx1, sy2 - sy1

    # ── Screen base: CRT static texture ──────────────────────────────────────
    # Static noise — per-pixel scatter
    n_static = (sw * sh) // 10
    for _ in range(n_static):
        px = RNG.randint(sx1, sx2 - 1)
        py = RNG.randint(sy1, sy2 - 1)
        brightness = RNG.randint(10, 45)
        sc = lerp_color(SCREEN_BASE, ELEC_CYAN, brightness / 200)
        draw.point((px, py), fill=sc)

    # Scanlines
    for sy in range(sy1, sy2, 3):
        draw.line([(sx1, sy), (sx2, sy)], fill=lerp_color(SCREEN_BASE, VOID_BLACK, 0.15), width=1)

    # Phosphor bands (under stress)
    for _ in range(5):
        band_y = RNG.randint(sy1 + 20, sy2 - 20)
        band_color = lerp_color(ELEC_CYAN, HOT_MAGENTA, RNG.uniform(0.0, 0.5))
        draw.rectangle([sx1, band_y, sx2, band_y + 3],
                       fill=lerp_color(band_color, SCREEN_BASE, 0.7))

    # ── Cyan/Magenta light flood inside screen ───────────────────────────────
    flood = Image.new('RGBA', img.size, (0, 0, 0, 0))
    fd = ImageDraw.Draw(flood)
    for row in range(sy1, sy2, 2):
        t = (row - sy1) / sh
        fc = lerp_color(ELEC_CYAN, HOT_MAGENTA, t * 0.6)
        alpha = int(30 + 18 * math.sin(t * math.pi))
        fd.line([(sx1, row), (sx2, row)], fill=(*fc, alpha))
    base = img.convert('RGBA')
    img.paste(Image.alpha_composite(base, flood).convert('RGB'))
    draw = ImageDraw.Draw(img)

    # ── Glitchkin 4: small, further back, both hands no face (shy/hidden) ────
    gk4_cx = int(sx1 + sw * 0.28)
    gk4_cy = int(sy1 + sh * 0.50)
    gk4_size = 14
    draw_glitchkin_face_ecl(draw, gk4_cx, gk4_cy, gk4_size, "hidden", RNG)
    # Both small hands visible, close together
    draw_glitchkin_hand(draw, gk4_cx - 12, gk4_cy - 18, 8, False, RNG)
    draw_glitchkin_hand(draw, gk4_cx + 10, gk4_cy - 16, 7, False, RNG)
    draw_distortion_rings(draw, gk4_cx, gk4_cy, 2, gk4_size + 6, RNG)

    # ── Glitchkin 3: lower-center, face sideways, cracked eye ────────────────
    gk3_cx = int(sx1 + sw * 0.45)
    gk3_cy = int(sy1 + sh * 0.72)
    gk3_r = 28
    draw_glitchkin_face_ecl(draw, gk3_cx, gk3_cy, gk3_r, "squished_side", RNG)
    draw_distortion_rings(draw, gk3_cx, gk3_cy, 3, gk3_r + 8, RNG)

    # ── Glitchkin 2: upper-left, hand only, splayed fingers ──────────────────
    gk2_cx = int(sx1 + sw * 0.20)
    gk2_cy = int(sy1 + sh * 0.22)
    draw_glitchkin_hand(draw, gk2_cx, gk2_cy, 18, True, RNG)
    draw_distortion_rings(draw, gk2_cx, gk2_cy, 4, 28, RNG)
    # Extra glow at this press point
    add_glow(img, gk2_cx, gk2_cy, 50, ELEC_CYAN, steps=5, max_alpha=40)
    draw = ImageDraw.Draw(img)

    # ── Glitchkin 1: center-right, face pressed flat, eager, palms on glass ──
    gk1_cx = int(sx1 + sw * 0.68)
    gk1_cy = int(sy1 + sh * 0.42)
    gk1_r = 38
    draw_glitchkin_face_ecl(draw, gk1_cx, gk1_cy, gk1_r, "eager", RNG)
    # Both palms pressed on glass flanking the face
    draw_glitchkin_hand(draw, gk1_cx - gk1_r - 20, gk1_cy - 8, 14, True, RNG)
    draw_glitchkin_hand(draw, gk1_cx + gk1_r + 18, gk1_cy - 6, 13, True, RNG)
    # Strong distortion rings at this primary press point
    draw_distortion_rings(draw, gk1_cx, gk1_cy, 5, gk1_r + 10, RNG)
    # Glow
    add_glow(img, gk1_cx, gk1_cy, 70, ELEC_CYAN, steps=6, max_alpha=45)
    draw = ImageDraw.Draw(img)

    # ── Screen cracks starting at strongest press point (GK1) ────────────────
    crack_ox = gk1_cx + gk1_r + 5
    crack_oy = gk1_cy - 10
    draw_screen_cracks(draw, crack_ox, crack_oy, 80, 5, RNG)
    # Secondary crack from GK2 hand press
    draw_screen_cracks(draw, gk2_cx + 10, gk2_cy + 14, 40, 3, RNG)

    # ── Pixel confetti inside the screen space ───────────────────────────────
    for _ in range(18):
        cx_p = RNG.randint(sx1 + 10, sx2 - 10)
        cy_p = RNG.randint(sy1 + 10, sy2 - 10)
        sides = RNG.randint(4, 7)
        pr = RNG.randint(2, 5)
        pc_base = ELEC_CYAN if RNG.random() > 0.3 else HOT_MAGENTA
        pc = lerp_color(pc_base, VOID_BLACK, RNG.uniform(0.0, 0.3))
        draw_irregular_poly(draw, cx_p, cy_p, pr, sides, pc, RNG, fill=True)

    # ── Additional scanline overlay for CRT texture ──────────────────────────
    scanline_ol = Image.new('RGBA', img.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(scanline_ol)
    for sy in range(sy1, sy2, 2):
        sd.line([(sx1, sy), (sx2, sy)], fill=(0, 0, 0, 12))
    base = img.convert('RGBA')
    img.paste(Image.alpha_composite(base, scanline_ol).convert('RGB'))
    draw = ImageDraw.Draw(img)

    # ── Annotations ──────────────────────────────────────────────────────────
    font_ann   = load_font(9,  bold=False)
    font_ann_b = load_font(9,  bold=True)
    font_sm    = load_font(8,  bold=False)

    draw.text((bezel_w + 4, bezel_w + 4),
              'ECU  |  SINGLE MONITOR  |  GLITCHKIN PRESSING',
              font=font_ann, fill=ANN_COLOR)

    # Label each Glitchkin
    draw.text((gk1_cx + gk1_r + 30, gk1_cy - 6),
              "GK#1: eager, palms flat", font=font_sm, fill=ANN_DIM)
    draw.text((gk2_cx + 24, gk2_cy + 4),
              "GK#2: hand only, splayed", font=font_sm, fill=ANN_DIM)
    draw.text((gk3_cx + gk3_r + 8, gk3_cy - 4),
              "GK#3: sideways, cracked eye", font=font_sm, fill=ANN_DIM)
    draw.text((gk4_cx + 18, gk4_cy + 10),
              "GK#4: shy, hands only", font=font_sm, fill=ANN_DIM)

    # Crack annotation
    draw.text((crack_ox + 20, crack_oy - 16),
              "SCREEN CRACKS BEGIN", font=font_ann_b, fill=(255, 220, 180))

    # ── Three-tier caption bar ────────────────────────────────────────────────
    final = Image.new('RGB', (PW, PH), DEEP_SPACE)
    final.paste(img, (0, 0))
    draw = ImageDraw.Draw(final)

    font_t1   = load_font(13, bold=True)
    font_t2   = load_font(11, bold=False)
    font_t3   = load_font(9,  bold=False)
    font_meta = load_font(8,  bold=False)

    draw.rectangle([0, DRAW_H, PW, PH], fill=BG_CAPTION)
    draw.line([0, DRAW_H, PW, DRAW_H], fill=(8, 6, 4), width=2)

    draw.text((10, DRAW_H + 4),
              "P22  |  ECU MONITOR  |  GLITCHKIN PRESSING THROUGH",
              font=font_t1, fill=TEXT_SHOT)

    draw.text((PW - 200, DRAW_H + 5),
              "ARC: TENSE / ESCALATION", font=font_t2, fill=HOT_MAGENTA)

    draw.text((10, DRAW_H + 22),
              "Multiple Glitchkin pressing against glass from inside. Screen cracks begin.",
              font=font_t3, fill=TEXT_DESC)
    draw.text((10, DRAW_H + 35),
              "4 distinct Glitchkin: eager, hand-only, squished, shy. Individuals, not swarm.",
              font=font_t3, fill=(120, 112, 90))

    draw.text((PW - 276, DRAW_H + 56),
              "LTG_SB_cold_open_P22  /  Diego Vargas  /  C48",
              font=font_meta, fill=TEXT_META)

    draw.rectangle([0, 0, PW - 1, PH - 1], outline=ARC_COLOR, width=4)

    final.thumbnail((1280, 1280))
    final.save(OUTPUT_PATH, "PNG")
    print(f"Saved: {OUTPUT_PATH}  {final.size}")
    return OUTPUT_PATH


if __name__ == "__main__":
    draw_panel()
    print("P22 standalone panel generation complete.")
    print("Beat: ECU monitor. Multiple Glitchkin pressing against glass. Screen cracks.")
    print("HOT_MAGENTA border. 4 distinct Glitchkin with individual expressions.")
