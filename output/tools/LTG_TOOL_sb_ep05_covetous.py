#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_sb_ep05_covetous.py
Episode 5 — COVETOUS Beat: Three-Character Triangulation Storyboard Panel
Diego Vargas, Storyboard Artist — Cycle 43

Beat: Glitch's first appearance in the series (Episode 5).
      Three-character triangulation: Glitch (COVETOUS, left) — Byte (barrier, midground center)
      — Luma (subject of desire, right zone, warm character palette).

      Glitch wants what it cannot take: Luma's ability to move freely between worlds.
      The image is the gap between Glitch and Luma. Byte stands in it.

Shot:   Low angle (approximately Glitch's center height — Glitch reads larger, imposing)
Setting: Glitch Layer — familiar location where Glitch is already present.
         UV Purple void, digital platform depth system.

Character positions:
  LEFT / CENTER-LEFT: Glitch — COVETOUS state. tilt_deg=+12 (lean toward Luma).
                       Bilateral acid-slit eyes [[5,5,5],[0,5,0],[0,0,0]].
                       Arms slightly raised (arm_l_dy=-8, arm_r_dy=-6).
                       spike_h=12. Corrupt Amber body. UV Purple shadow +3px/+4px.
  MIDGROUND CENTER:   Byte — protective barrier posture. Teal body. Smaller than Glitch.
                       Arms extended slightly (barrier lean between characters).
  RIGHT ZONE:         Luma — LUMA_HOODIE orange. Warm skin. Background-scale.
                       She is what Glitch covets: the bridge between worlds.

Color arc (left to right): Glitch amber-in-void → Byte teal-transition → Luma warm orange
Warm zone rule: Luma's warm colors must stay right 30%. Glitch NOT warmed by Luma.

Arc: no arc defined for EP5 — this is a STYLE FRAME / KEY BEAT storyboard panel.
     Border: UV_PURPLE (the Glitch Layer signature).

Image size rule: ≤ 1280px in both dimensions.
Output: output/storyboards/panels/LTG_SB_ep05_covetous.png
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
from LTG_TOOL_char_glitch import draw_glitch as _draw_glitch_canonical
from LTG_TOOL_char_byte import draw_byte as _draw_byte_canonical
from LTG_TOOL_char_luma import draw_luma as _draw_luma_canonical
from LTG_TOOL_cairo_primitives import to_pil_rgba
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

PANELS_DIR = output_dir('storyboards', 'panels')
OUTPUT_PATH = os.path.join(PANELS_DIR, "LTG_SB_ep05_covetous.png")
os.makedirs(PANELS_DIR, exist_ok=True)

PW, PH    = 800, 600
CAPTION_H = 60
DRAW_H    = PH - CAPTION_H   # 540

# ── Palette ──────────────────────────────────────────────────────────────────
# Glitch Layer background
VOID_BLACK      = (10, 10, 20)
UV_PURPLE       = (123, 47, 190)
UV_PURPLE_DIM   = (74, 28, 114)
UV_PURPLE_ATMO  = (46, 17, 80)
PLATFORM_LINE   = (0, 240, 255)      # GL-01 Electric Cyan — thin platform lines only
PLATFORM_MID    = (0, 130, 160)      # desaturated for mid-distance depth
# Glitch character
CORRUPT_AMBER   = (255, 140, 0)      # GL-07
CORRUPT_AMB_HL  = (255, 185, 80)     # highlight facet
CORRUPT_AMB_SH  = (168, 92, 0)       # shadow / bottom spike
HOT_MAG         = (255, 45, 107)     # GL-02 crack line
ACID_GREEN      = (57, 255, 20)      # GL-03 — COVETOUS eye color
# Byte character
BYTE_TEAL       = (0, 212, 232)
BYTE_TEAL_DIM   = (0, 160, 180)      # under UV ambient
ELEC_CYAN       = (0, 212, 232)
ELEC_CYAN_HI    = (90, 248, 255)
BYTE_EYE_W      = (228, 240, 248)
CRACK_LINE      = (200, 30, 100)
# Luma character (right warm zone)
LUMA_HOODIE     = (232, 112, 58)     # CANONICAL ORANGE per master_palette.md
# Character palette constants removed — canonical renderers handle their own palettes.
SOFT_GOLD       = (232, 201, 90)     # RW-02 warm ambient radiate from Luma (alpha max 50)
# Caption / annotation
BG_CAPTION      = (10, 6, 18)
TEXT_CAP        = (230, 220, 210)
ANN_COL         = (180, 155, 210)    # purple-tinted annotation
ANN_DIM         = (120, 108, 148)
BORDER_COLOR    = UV_PURPLE          # Glitch Layer frame

RNG = random.Random(555)


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


def draw_irregular_poly(draw, cx, cy, r, sides, color, seed=0, outline=None, outline_w=1):
    """4–7 sided irregular polygon — Cycle 11 standard."""
    rng = random.Random(seed)
    pts = []
    for i in range(sides):
        angle = (2 * math.pi * i / sides) + rng.uniform(-0.28, 0.28)
        dist  = r * rng.uniform(0.68, 1.22)
        pts.append((int(cx + dist * math.cos(angle)), int(cy + dist * math.sin(angle))))
    draw.polygon(pts, fill=color, outline=outline)









def draw_platform_lines(draw, n_lines=4, seed=88):
    """Canonical Glitch Layer platform depth system — thin cyan lines only."""
    rng = random.Random(seed)
    platform_y_levels = [
        int(DRAW_H * 0.68), int(DRAW_H * 0.76), int(DRAW_H * 0.84), int(DRAW_H * 0.90)
    ]
    for py in platform_y_levels:
        # Platform line: perspective-narrowed toward vanishing point
        x_l = rng.randint(0, int(PW * 0.08))
        x_r = rng.randint(int(PW * 0.88), PW)
        draw.line([(x_l, py), (x_r, py)], fill=PLATFORM_LINE, width=1)
        # Mid-ground depth markers (dimmer lines between platforms)
        for px_off in [int(PW * 0.15), int(PW * 0.38), int(PW * 0.60), int(PW * 0.82)]:
            y_off = rng.randint(-3, 3)
            draw.line([(px_off, py + y_off), (px_off, py + y_off + int(DRAW_H * 0.07))],
                      fill=PLATFORM_MID, width=1)



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

def draw_glitch(draw, cx, cy, rx=34, ry=38, tilt_deg=12,
                expression="covetous", facing="front",
                spike_h=12, arm_l_dy=0, arm_r_dy=0, scale=1.0, **kwargs):
    """Glitch — canonical renderer."""
    scale = ry / 38.0
    surface = _draw_glitch_canonical(expression=expression, scale=scale, facing=facing)
    char_pil = _char_to_pil(surface)
    if char_pil.height > 0:
        target_h = int(ry * 3.0)
        aspect = char_pil.width / char_pil.height
        new_w = int(target_h * aspect)
        char_pil = char_pil.resize((new_w, target_h), Image.LANCZOS)
    try:
        img = draw._image
        _composite_char(img, char_pil, cx, cy)
    except AttributeError:
        pass


def draw_byte_barrier(draw, cx, cy, body_h, scale=0.75):
    """Byte in barrier pose — canonical renderer."""
    byte_scale = (body_h * scale) / 88.0
    surface = _draw_byte_canonical(expression="alarmed", scale=byte_scale, facing="front")
    char_pil = _char_to_pil(surface)
    if char_pil.height > 0:
        target_h = int(body_h * scale)
        aspect = char_pil.width / char_pil.height
        new_w = int(target_h * aspect)
        char_pil = char_pil.resize((new_w, target_h), Image.LANCZOS)
    try:
        img = draw._image
        _composite_char(img, char_pil, cx, cy)
    except AttributeError:
        pass


def draw_luma_right(draw, cx, cy, scale=0.65):
    """Luma on right side — canonical renderer."""
    luma_scale = scale
    surface = _draw_luma_canonical(expression="WORRIED", scale=luma_scale, facing="right")
    char_pil = _char_to_pil(surface)
    if char_pil.height > 0:
        target_h = int(200 * scale)
        aspect = char_pil.width / char_pil.height
        new_w = int(target_h * aspect)
        char_pil = char_pil.resize((new_w, target_h), Image.LANCZOS)
    try:
        img = draw._image
        _composite_char(img, char_pil, cx, cy)
    except AttributeError:
        pass


def draw_scene(img):
    draw = ImageDraw.Draw(img)

    # ── Background — Glitch Layer void ───────────────────────────────────────
    # Far void: VOID_BLACK base
    draw.rectangle([0, 0, PW, DRAW_H], fill=VOID_BLACK)

    # UV atmospheric haze (left 75% — Glitch's zone)
    uv_layer = Image.new('RGBA', (PW, PH), (0, 0, 0, 0))
    uvd = ImageDraw.Draw(uv_layer)
    for bx in range(0, int(PW * 0.78)):
        t = 1.0 - (bx / (PW * 0.78))
        a = max(0, int(85 * t * t))
        uvd.line([(bx, 0), (bx, DRAW_H)], fill=(*UV_PURPLE, a))
    img.paste(Image.alpha_composite(img.convert('RGBA'), uv_layer).convert('RGB'))
    draw = ImageDraw.Draw(img)

    # Atmospheric mid-void band (depth separation)
    draw.rectangle([0, int(DRAW_H * 0.38), PW, int(DRAW_H * 0.55)],
                   fill=UV_PURPLE_ATMO)
    # Soften this band's edges
    add_glow(img, PW // 2, int(DRAW_H * 0.46), int(PW * 0.55), UV_PURPLE_ATMO,
             steps=3, max_alpha=18)
    draw = ImageDraw.Draw(img)

    # Platform ground void (lower 30%)
    draw.rectangle([0, int(DRAW_H * 0.72), PW, DRAW_H], fill=UV_PURPLE_DIM)

    # Platform lines
    draw_platform_lines(draw)

    # ── Right zone: Luma's warm character warmth radiates (alpha max 50) ───────
    # Soft gold radial glow from Luma's position — NOT a light source on Glitch
    luma_cx = int(PW * 0.80)
    luma_cy = int(DRAW_H * 0.40)
    warm_glow_layer = Image.new('RGBA', (PW, PH), (0, 0, 0, 0))
    wgd = ImageDraw.Draw(warm_glow_layer)
    # Radial from Luma — falls to 0 over 120px
    for r in range(120, 0, -10):
        a = max(0, int(50 * (1 - r / 120)))
        wgd.ellipse([luma_cx - r, luma_cy - r, luma_cx + r, luma_cy + r],
                    fill=(*SOFT_GOLD, a))
    img.paste(Image.alpha_composite(img.convert('RGBA'), warm_glow_layer).convert('RGB'))
    draw = ImageDraw.Draw(img)

    # ── Draw characters (back to front: Luma, Byte, Glitch) ──────────────────

    # LUMA (right zone — background scale, slightly behind Byte)
    draw_luma_right(draw, luma_cx, luma_cy, scale=0.62)

    # BYTE (midground barrier — between Glitch and Luma)
    byte_cx = int(PW * 0.53)
    byte_cy = int(DRAW_H * 0.44)
    byte_bh = int(DRAW_H * 0.30)
    draw_byte_barrier(draw, byte_cx, byte_cy, byte_bh, scale=0.78)

    # UV Purple shadow on Byte (canonical Glitch Layer ambient)
    byte_shadow = Image.new('RGBA', img.size, (0, 0, 0, 0))
    bsd = ImageDraw.Draw(byte_shadow)
    bsd.ellipse([byte_cx - int(byte_bh * 0.25) + 4, byte_cy - int(byte_bh * 0.35) + 5,
                 byte_cx + int(byte_bh * 0.25) + 4, byte_cy + int(byte_bh * 0.35) + 5],
                fill=(*UV_PURPLE_DIM, 50))
    img.paste(Image.alpha_composite(img.convert('RGBA'), byte_shadow).convert('RGB'))
    draw = ImageDraw.Draw(img)

    # GLITCH (left/center-left — foreground, dominant) — COVETOUS state
    glitch_cx = int(PW * 0.26)
    glitch_cy = int(DRAW_H * 0.42)
    glitch_rx = 44
    glitch_ry = 50

    draw_glitch(draw, glitch_cx, glitch_cy, rx=glitch_rx, ry=glitch_ry,
                tilt_deg=12, spike_h=12, arm_l_dy=-8, arm_r_dy=-6, scale=1.0)

    # COVETOUS confetti — UV Purple + dark amber only, minimal (count=4 per spec)
    for ci, (conf_col, conf_seed) in enumerate([
        (UV_PURPLE_DIM, 5501), ((168, 92, 0), 5502),
        (UV_PURPLE, 5503), (UV_PURPLE_DIM, 5504),
    ]):
        ang = math.radians(ci * 90 + 35)
        px  = glitch_cx + int(18 * math.cos(ang))
        py  = glitch_cy + int(18 * math.sin(ang))
        draw_irregular_poly(draw, px, py, 3, 5, conf_col, seed=5500 + ci)

    # Glitch ambient glow (UV Purple ambient — NOT warm light)
    add_glow(img, glitch_cx, glitch_cy, int(glitch_rx * 1.8),
             UV_PURPLE, steps=5, max_alpha=28)
    draw = ImageDraw.Draw(img)

    # ── Barrier line annotation ───────────────────────────────────────────────
    barrier_x = byte_cx
    draw.line([(barrier_x, int(DRAW_H * 0.18)), (barrier_x, int(DRAW_H * 0.88))],
              fill=(*BYTE_TEAL, ), width=1)
    # Actually draw as dashed
    dash_y = int(DRAW_H * 0.18)
    while dash_y < int(DRAW_H * 0.88):
        draw.line([(barrier_x, dash_y), (barrier_x, min(dash_y + 8, int(DRAW_H * 0.88)))],
                  fill=BYTE_TEAL_DIM, width=1)
        dash_y += 15
    draw.text((barrier_x + 4, int(DRAW_H * 0.20)), "barrier",
              font=load_font(8), fill=BYTE_TEAL_DIM)

    # ── Color arc annotation (left to right) ─────────────────────────────────
    arc_y = DRAW_H - 38
    arc_labels = [
        (int(PW * 0.18), "Glitch\namber/void"),
        (int(PW * 0.52), "Byte\nteal"),
        (int(PW * 0.80), "Luma\nwarm orange"),
    ]
    for ax, alabel in arc_labels:
        draw.text((ax - 18, arc_y), alabel, font=load_font(8), fill=ANN_DIM)

    # ── Panel annotations ─────────────────────────────────────────────────────
    font_ann   = load_font(11)
    font_ann_b = load_font(11, bold=True)

    draw.text((10, 8),
              "EP05  /  COVETOUS BEAT  /  low angle  /  Glitch Layer",
              font=font_ann, fill=ANN_COL)
    draw.text((10, 20),
              "Glitch (COVETOUS): bilateral acid-slit eyes. +12° lean. Arms slightly raised. Amber-in-void.",
              font=font_ann, fill=ANN_DIM)
    draw.text((10, 32),
              "Byte (barrier): between Glitch and Luma. Arms extended. Smaller than Glitch.",
              font=font_ann, fill=ANN_DIM)

    # Glitch label
    draw.text((glitch_cx - 20, int(DRAW_H * 0.12)), "GLITCH\nCOVETOUS",
              font=font_ann_b, fill=CORRUPT_AMBER)
    # Byte label
    draw.text((byte_cx + 5, int(DRAW_H * 0.18)), "BYTE\nbarrier",
              font=font_ann_b, fill=ELEC_CYAN)
    # Luma label
    draw.text((luma_cx - 10, int(DRAW_H * 0.16)), "LUMA\nwarm zone",
              font=font_ann_b, fill=LUMA_HOODIE)

    # Shot label
    draw.rectangle([10, DRAW_H - 24, 100, DRAW_H - 6], fill=(18, 8, 30))
    draw.text((14, DRAW_H - 22), "LOW ANGLE / STATIC",
              font=font_ann_b, fill=(200, 180, 235))

    # Rule reminder
    draw.rectangle([PW - 220, DRAW_H - 24, PW - 10, DRAW_H - 6], fill=(24, 8, 36))
    draw.text((PW - 216, DRAW_H - 22), "Glitch NOT lit by Luma (void only)",
              font=load_font(10), fill=UV_PURPLE)

    return draw


def make_panel():
    font_cap = load_font(12)
    font_ann = load_font(11)
    font_sm  = load_font(10)

    img = Image.new('RGB', (PW, PH), VOID_BLACK)
    draw_scene(img)

    # Caption bar
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, DRAW_H, PW, PH], fill=BG_CAPTION)
    draw.line([0, DRAW_H, PW, DRAW_H], fill=(6, 4, 12), width=2)
    draw.text((10, DRAW_H + 4),
              "EP05  COVETOUS BEAT  low angle  |  Three-character triangulation: Glitch / Byte / Luma",
              font=font_cap, fill=(155, 148, 185))
    draw.text((10, DRAW_H + 18),
              "Glitch: COVETOUS (bilateral acid-slit eyes, +12° lean, amber-in-void). "
              "Byte: barrier midground. Luma: warm right zone.",
              font=font_cap, fill=TEXT_CAP)
    draw.text((10, DRAW_H + 33),
              "Color arc: Glitch amber/void → Byte teal → Luma warm orange. "
              "Glitch NOT warmed by Luma. The gap IS the image.",
              font=font_ann, fill=(140, 130, 168))
    draw.text((PW - 240, DRAW_H + 46),
              "LTG_SB_ep05_covetous  /  Diego Vargas  /  C43",
              font=font_sm, fill=(95, 88, 118))

    # Border: UV_PURPLE (Glitch Layer frame)
    draw.rectangle([0, 0, PW - 1, PH - 1], outline=BORDER_COLOR, width=4)

    img.thumbnail((1280, 1280))
    img.save(OUTPUT_PATH, "PNG")
    print(f"Saved: {OUTPUT_PATH}  {img.size}")
    return OUTPUT_PATH


if __name__ == "__main__":
    make_panel()
    print("EP05 COVETOUS panel generation complete.")
