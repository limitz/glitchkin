#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_sb_cold_open_P03.py
Cold Open Panel P03 — CU MONITOR — First Pixel
Diego Vargas, Storyboard Artist — Cycle 41

Beat: The first Glitch Palette moment in the episode.
Tight on the hero CRT prop. Static on screen. One cyan pixel appears
in the lower-right corner, impossibly vivid. Small. Almost nothing.
The FIRST appearance of the Glitch Palette.

Shot:   CU — Object
Camera: Eye level (~8" off floor), slight low angle upward toward screen. STATIC.
Palette: Warm Real World (den) — Single ELEC_CYAN pixel is the ONLY Glitch color.
Arc:    CURIOUS — the spark.

Image size rule: ≤ 1280px in both dimensions.
Output: output/storyboards/panels/LTG_SB_cold_open_P03.png
"""

from PIL import Image, ImageDraw, ImageFont
import math, random, os

PANELS_DIR  = "/home/wipkat/team/output/storyboards/panels"
OUTPUT_PATH = os.path.join(PANELS_DIR, "LTG_SB_cold_open_P03.png")
os.makedirs(PANELS_DIR, exist_ok=True)

PW, PH    = 800, 600
CAPTION_H = 60
DRAW_H    = PH - CAPTION_H   # 540

# ── Palette ──────────────────────────────────────────────────────────────────
WARM_CREAM   = (250, 240, 220)
WARM_BG      = (210, 190, 158)      # blurred den background, warm amber shadow
DEN_SHADOW   = (170, 148, 112)
PLASTIC_OLD  = (190, 178, 142)      # yellowed CRT plastic body
PLASTIC_SIDE = (165, 154, 120)      # darker side of CRT body (shadow)
PLASTIC_HIGH = (218, 208, 174)      # highlight on plastic
CRT_BEZEL    = (155, 145, 112)      # bezel inner edge
SCREEN_STATIC= (148, 138, 128)      # warm gray-white static
SCREEN_GLOW  = (165, 160, 148)      # phosphor mid-static
SCREEN_DARK  = (110, 106, 100)      # dark static flecks
SCREEN_LIGHT = (200, 196, 186)      # light static flecks
STICKER_A    = (228, 90, 52)        # half-peeled red sticker remnant
STICKER_B    = (80, 140, 200)       # blue sticker remnant
CABLE_DARK   = (60, 52, 42)
LINE_DARK    = (80, 64, 44)
SHADOW_BODY  = (130, 116, 90)
VENT_DARK    = (125, 110, 82)
# Glitch Palette — THE KEY COLOR — only one in this frame
ELEC_CYAN    = (0, 212, 232)
ELEC_CYAN_DIM= (0, 170, 190)
# Caption
BG_CAPTION   = (14, 10, 8)
TEXT_CAP     = (235, 228, 210)
ANN_COL      = (200, 175, 120)
ANN_DIM      = (150, 135, 100)
# Arc border
ARC_CURIOUS  = (0, 212, 232)        # CURIOUS arc — cyan

RNG = random.Random(303)


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


def draw_static_texture(draw, x0, y0, x1, y1, rng):
    """Draw analog CRT static texture within bounds."""
    w = x1 - x0
    h = y1 - y0
    # Base static fill
    draw.rectangle([x0, y0, x1, y1], fill=SCREEN_STATIC)
    # Scatter light and dark static flecks for analog texture
    for _ in range(w * h // 12):
        sx = x0 + rng.randint(0, w - 1)
        sy = y0 + rng.randint(0, h - 1)
        val = rng.randint(0, 3)
        if val == 0:
            draw.point((sx, sy), fill=SCREEN_LIGHT)
        elif val == 1:
            draw.point((sx, sy), fill=SCREEN_DARK)
        # val 2/3 = leave as static base
    # Scan lines — thin, slightly darker horizontal bands (analog phosphor scanlines)
    for sl_y in range(y0, y1, 3):
        alpha_col = (SCREEN_STATIC[0] - 12, SCREEN_STATIC[1] - 12, SCREEN_STATIC[2] - 12)
        draw.line([(x0, sl_y), (x1, sl_y)], fill=alpha_col, width=1)
    # Phosphor bloom bands — very faint horizontal lighter bands
    for bl_y in range(y0 + 2, y1, 18):
        bl_col = (SCREEN_GLOW[0], SCREEN_GLOW[1], SCREEN_GLOW[2])
        draw.line([(x0, bl_y), (x1, bl_y)], fill=bl_col, width=1)


def draw_scene(img):
    draw = ImageDraw.Draw(img)

    # ── Background: soft-focus warm den behind monitor ──────────────────────
    # The den BG is shallow depth-of-field — warm amber-brown blur
    draw.rectangle([0, 0, PW, DRAW_H], fill=WARM_BG)

    # Soft shelving silhouette in BG (defocused — just shapes)
    # Back shelf unit behind monitor (warm wood tone, blurred)
    draw.rectangle([0, int(DRAW_H * 0.18), int(PW * 0.20), int(DRAW_H * 0.80)],
                   fill=DEN_SHADOW)
    draw.rectangle([int(PW * 0.78), int(DRAW_H * 0.18), PW, int(DRAW_H * 0.80)],
                   fill=DEN_SHADOW)
    # Some blurred shapes suggesting stacked monitors/equipment BG
    for bx, by, bw, bh in [
        (22, int(DRAW_H * 0.25), 80, 55),
        (18, int(DRAW_H * 0.50), 90, 40),
        (int(PW * 0.80), int(DRAW_H * 0.30), 75, 48),
        (int(PW * 0.82), int(DRAW_H * 0.55), 65, 38),
    ]:
        bc = (DEN_SHADOW[0] - 10, DEN_SHADOW[1] - 10, DEN_SHADOW[2] - 8)
        draw.rectangle([bx, by, bx + bw, by + bh], fill=bc)

    # Warm ambient glow — den lamp from the right (off-camera)
    add_glow(img, PW - 80, int(DRAW_H * 0.30), 180, (212, 146, 58), steps=5, max_alpha=22)
    draw = ImageDraw.Draw(img)

    # ── CRT Monitor — hero prop, center of frame ─────────────────────────────
    # The CRT is the focal element — it's a chunky, rounded-square old unit,
    # slightly undershooting center so the screen fills most of the panel.

    # Monitor body coordinates
    mon_cx  = int(PW * 0.50)
    mon_cy  = int(DRAW_H * 0.46)
    mon_w   = int(PW * 0.62)   # wide — screen almost fills panel width
    mon_h   = int(DRAW_H * 0.68)
    mon_x0  = mon_cx - mon_w // 2
    mon_x1  = mon_cx + mon_w // 2
    mon_y0  = mon_cy - mon_h // 2
    mon_y1  = mon_cy + mon_h // 2

    # Monitor body (deep plastic, yellowed from age)
    # Main body rounded rectangle approximation (PIL polygon)
    r = 18
    body_pts = [
        (mon_x0 + r, mon_y0), (mon_x1 - r, mon_y0),
        (mon_x1, mon_y0 + r), (mon_x1, mon_y1 - r),
        (mon_x1 - r, mon_y1), (mon_x0 + r, mon_y1),
        (mon_x0, mon_y1 - r), (mon_x0, mon_y0 + r),
    ]
    draw.polygon(body_pts, fill=PLASTIC_OLD, outline=LINE_DARK)

    # Shadow side of monitor body (right and bottom edges)
    shadow_pts = [
        (mon_x1 - r, mon_y0 + 4), (mon_x1, mon_y0 + r + 4),
        (mon_x1, mon_y1 - r), (mon_x1 - r, mon_y1),
        (mon_x0 + r, mon_y1), (mon_x0 + r + 4, mon_y1 - 4),
        (mon_x1 - r - 4, mon_y1 - 4), (mon_x1 - 4, mon_y1 - r - 4),
        (mon_x1 - 4, mon_y0 + r + 4), (mon_x1 - r - 4, mon_y0 + 4),
    ]
    draw.polygon(shadow_pts, fill=PLASTIC_SIDE)

    # Top highlight on monitor body
    draw.line([(mon_x0 + r + 6, mon_y0 + 5), (mon_x1 - r - 6, mon_y0 + 5)],
              fill=PLASTIC_HIGH, width=3)

    # Monitor ventilation slots (right side of body)
    vent_x = mon_x1 - 22
    for vi in range(4):
        vy = mon_y0 + int(mon_h * (0.40 + vi * 0.07))
        draw.rectangle([vent_x, vy, vent_x + 12, vy + 3], fill=VENT_DARK)

    # ── Screen bezel ─────────────────────────────────────────────────────────
    bz = 26    # bezel thickness
    scr_x0 = mon_x0 + bz
    scr_x1 = mon_x1 - bz
    scr_y0 = mon_y0 + bz - 4
    scr_y1 = mon_y1 - bz - 20

    draw.rectangle([scr_x0, scr_y0, scr_x1, scr_y1], fill=CRT_BEZEL, outline=LINE_DARK, width=2)

    # Screen inner (where static plays)
    scr_inner_pad = 6
    si_x0 = scr_x0 + scr_inner_pad
    si_x1 = scr_x1 - scr_inner_pad
    si_y0 = scr_y0 + scr_inner_pad
    si_y1 = scr_y1 - scr_inner_pad

    # Draw static texture
    draw_static_texture(draw, si_x0, si_y0, si_x1, si_y1, RNG)

    # Screen glow (CRT phosphor ambient — warm cool)
    add_glow(img, (si_x0 + si_x1) // 2, (si_y0 + si_y1) // 2,
             (si_x1 - si_x0) // 2, (180, 175, 165), steps=5, max_alpha=18)
    draw = ImageDraw.Draw(img)

    # ── THE PIXEL — FIRST GLITCH PALETTE MOMENT ──────────────────────────────
    # One single electric cyan pixel in the lower-right of the screen.
    # It is the most saturated thing in the entire frame.
    # It PULSES — we draw it with a subtle glow halo to suggest the pulse.
    pix_x = si_x1 - int((si_x1 - si_x0) * 0.12)   # 12% from right edge
    pix_y = si_y1 - int((si_y1 - si_y0) * 0.14)   # 14% from bottom edge
    pix_size = 5    # 5×5 pixel dot — still tiny relative to screen, but vivid

    # Phosphor glow halo around the pixel (suggests pulsing)
    add_glow(img, pix_x, pix_y, 28, ELEC_CYAN, steps=6, max_alpha=55)
    draw = ImageDraw.Draw(img)

    # The pixel itself — solid electric cyan
    draw.rectangle([pix_x - pix_size // 2, pix_y - pix_size // 2,
                    pix_x + pix_size // 2, pix_y + pix_size // 2],
                   fill=ELEC_CYAN)

    # Tiny annotation arrow pointing to the pixel (director note style)
    arrow_tip_x = pix_x - 4
    arrow_tip_y = pix_y - 4
    ann_lx = si_x1 - int((si_x1 - si_x0) * 0.45)
    ann_ly = si_y1 - int((si_y1 - si_y0) * 0.32)
    draw.line([(ann_lx + 40, ann_ly), (arrow_tip_x, arrow_tip_y)],
              fill=ELEC_CYAN_DIM, width=1)
    # Arrowhead
    draw.polygon([
        (arrow_tip_x, arrow_tip_y),
        (arrow_tip_x + 4, arrow_tip_y + 8),
        (arrow_tip_x - 2, arrow_tip_y + 6),
    ], fill=ELEC_CYAN_DIM)

    # Annotation label for the pixel
    font_ann_s = load_font(10)
    draw.text((ann_lx - 10, ann_ly - 10), "1 PIXEL (#00D4E8)",
              font=font_ann_s, fill=ELEC_CYAN_DIM)
    draw.text((ann_lx - 10, ann_ly + 1), "FIRST GLITCH PALETTE",
              font=font_ann_s, fill=ELEC_CYAN_DIM)

    # ── Stickers on monitor body (half-peeled, aging detail) ─────────────────
    # Sticker A — red, lower-left of bezel area
    stk_ax = mon_x0 + 38
    stk_ay = mon_y1 - 38
    draw.rectangle([stk_ax, stk_ay, stk_ax + 20, stk_ay + 12], fill=STICKER_A)
    # Peeled corner
    draw.polygon([(stk_ax + 12, stk_ay), (stk_ax + 20, stk_ay),
                  (stk_ax + 20, stk_ay + 8)], fill=PLASTIC_OLD)

    # Sticker B remnant — upper-right corner of body
    stk_bx = mon_x1 - 52
    stk_by = mon_y0 + 22
    draw.rectangle([stk_bx, stk_by, stk_bx + 24, stk_by + 14], fill=STICKER_B)
    draw.polygon([(stk_bx + 14, stk_by + 14), (stk_bx + 24, stk_by + 14),
                  (stk_bx + 24, stk_by + 6)], fill=PLASTIC_OLD)

    # Monitor power indicator LED (small green dot, lower front bezel)
    led_x = mon_x0 + bz + 10
    led_y = scr_y1 + 8
    draw.ellipse([led_x - 3, led_y - 3, led_x + 3, led_y + 3],
                 fill=(60, 200, 80), outline=LINE_DARK, width=1)

    # Cable from back of monitor (exits bottom)
    cable_x = mon_cx - 20
    draw.line([(cable_x, mon_y1 - 8), (cable_x - 12, DRAW_H)],
              fill=CABLE_DARK, width=4)
    draw.line([(cable_x + 30, mon_y1 - 6), (cable_x + 45, DRAW_H)],
              fill=CABLE_DARK, width=3)

    # ── FG surface texture (desk/shelf surface near camera) ──────────────────
    # The camera is near-floor level — we see the shelf surface the monitor sits on
    shelf_y = mon_y1 + 10
    if shelf_y < DRAW_H:
        draw.rectangle([0, shelf_y, PW, DRAW_H], fill=(155, 132, 98))
        # Grain
        for gx in range(0, PW, 20):
            draw.line([(gx, shelf_y + 3), (gx + 12, DRAW_H)],
                      fill=(138, 116, 84), width=1)

    # ── Panel annotations ─────────────────────────────────────────────────────
    font_ann  = load_font(11)
    font_ann_b = load_font(11, bold=True)

    draw.text((10, 8), "P03  /  CU — OBJECT  /  eye-level (~8\" off floor)  /  STATIC",
              font=font_ann, fill=ANN_COL)
    draw.text((10, 20), "Hero CRT prop — STATIC on screen — FIRST GLITCH PIXEL appears lower-right",
              font=font_ann, fill=ANN_DIM)
    draw.text((10, 32), "Screen glow = PRIMARY LIGHT SOURCE in frame  /  Den BG = soft-focus warm amber",
              font=font_ann, fill=ANN_DIM)

    # Shot label box
    draw.rectangle([10, DRAW_H - 24, 105, DRAW_H - 6], fill=(40, 32, 22))
    draw.text((14, DRAW_H - 22), "CU / OBJECT",
              font=font_ann_b, fill=(240, 220, 140))

    # Arc indicator
    draw.rectangle([PW - 130, DRAW_H - 24, PW - 10, DRAW_H - 6], fill=(0, 40, 50))
    draw.text((PW - 126, DRAW_H - 22), "ARC: CURIOUS",
              font=font_ann_b, fill=ELEC_CYAN)

    return draw


def make_panel():
    font_cap  = load_font(12)
    font_ann  = load_font(11)
    font_sm   = load_font(10)

    img  = Image.new('RGB', (PW, PH), WARM_BG)
    draw_scene(img)
    draw = ImageDraw.Draw(img)

    # Caption bar
    draw.rectangle([0, DRAW_H, PW, PH], fill=BG_CAPTION)
    draw.line([0, DRAW_H, PW, DRAW_H], fill=(10, 8, 6), width=2)
    draw.text((10, DRAW_H + 4),
              "P03  CU  OBJECT  eye-level  |  hero CRT prop — static — first pixel",
              font=font_cap, fill=(160, 155, 130))
    draw.text((10, DRAW_H + 18),
              "1 pixel: ELEC_CYAN (#00D4E8) in lower-right of screen. Static continues undisturbed.",
              font=font_cap, fill=TEXT_CAP)
    draw.text((10, DRAW_H + 33),
              "FIRST GLITCH PALETTE appearance in episode. Hold 2.5s. Digital chirp SFX.",
              font=font_ann, fill=(150, 140, 110))
    draw.text((PW - 230, DRAW_H + 46), "LTG_SB_cold_open_P03  /  Diego Vargas  /  C41",
              font=font_sm, fill=(100, 95, 78))

    # Arc-color border
    draw.rectangle([0, 0, PW - 1, PH - 1], outline=ARC_CURIOUS, width=3)

    img.thumbnail((1280, 1280))
    img.save(OUTPUT_PATH, "PNG")
    print(f"Saved: {OUTPUT_PATH}  {img.size}")
    return OUTPUT_PATH


if __name__ == "__main__":
    make_panel()
    print("P03 standalone panel generation complete.")
