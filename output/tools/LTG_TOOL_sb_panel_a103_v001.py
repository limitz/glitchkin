#!/usr/bin/env python3
"""
LTG_TOOL_sb_panel_a103_v001.py
Storyboard Panel A1-03 — DISCOVERY — Luma at TV, pixel shape in static — Cycle 18
Lee Tanaka, Storyboard Artist

Beat: Luma has moved to the TV. She's close to the screen. Something moves
in the static — a pixel shape. Her expression: CURIOUS → SURPRISED.
She can almost see something but isn't sure yet.

Shot: MEDIUM CU — Luma + TV (two subjects)
Camera: Eye-level (Luma's eyeline = camera height, ~child height).
        Luma FG-left (profile / 3/4 turn facing screen).
        TV screen BG-right (fills right half of frame).
        Composition: Luma face + TV screen side by side.

Expression: CURIOUS (leaning in) → SURPRISED (pixel shape visible).
Body language: leaning forward, hands on knees (or one hand reaching toward screen),
face close to screen, screen glow lights her face.

Arc: CURIOUS — first real contact. The Glitchkin are in there.
"""

from PIL import Image, ImageDraw, ImageFont
import math, random, os

PANELS_DIR  = "/home/wipkat/team/output/storyboards/panels"
OUTPUT_PATH = os.path.join(PANELS_DIR, "LTG_SB_act1_panel_a103_v001.png")
os.makedirs(PANELS_DIR, exist_ok=True)

PW, PH    = 800, 600
CAPTION_H = 60
DRAW_H    = PH - CAPTION_H

# ── Palette ─────────────────────────────────────────────────────────────────
BG_DARK      = (30, 24, 18)     # dim room background (adjacent room, pre-dawn)
BG_WALL      = (42, 34, 25)
FLOOR_DARK   = (38, 30, 22)
LINE_DARK    = (100, 72, 40)
SHADOW_WARM  = (80, 64, 44)

# Luma
LUMA_SKIN      = (242, 198, 152)
LUMA_SKIN_GLOW = (220, 210, 165)  # CRT-lit skin (cooler tint from screen)
LUMA_HAIR      = (52,  32,  18)
LUMA_HOODIE    = (88, 158, 200)
LUMA_PANTS     = (88, 102, 130)
LUMA_OUTLINE   = (52,  30,  10)
LUMA_EYE       = (62,  40,  18)

# CRT TV
TV_BODY      = (55, 48, 38)
TV_TRIM      = (72, 62, 50)
CRT_SCREEN   = (90, 105, 92)    # static base
CRT_STATIC1  = (130, 140, 128)  # lighter static noise
CRT_STATIC2  = (60,  70,  58)   # darker static noise
CRT_CYAN     = (0, 240, 255)    # electric cyan — glitch color
CRT_GLOW     = (0, 210, 230)

# Pixel shape (proto-Glitchkin visible in static)
PIXEL_CYAN   = (0, 240, 255)
PIXEL_BRIGHT = (180, 255, 255)

BG_CAPTION = (22, 18, 14)
TEXT_CAP   = (235, 228, 210)
ANN_COL    = (200, 175, 120)
ANN_DIM    = (150, 135, 100)
CALLOUT_L  = (220, 200, 140)
CALLOUT_TV = (0, 200, 220)


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


def draw_crt_static(draw, img, sx, sy, sw, sh, rng, pixel_shape=True):
    """
    Draw CRT screen with analog static texture and one pixel shape in it.
    sx, sy = screen top-left; sw, sh = screen width/height.
    """
    # Base static background
    draw.rectangle([sx, sy, sx + sw, sy + sh], fill=CRT_SCREEN)

    # Analog static texture (film grain + horizontal scan-line bias)
    for _ in range(280):
        px = rng.randint(sx, sx + sw - 1)
        py = rng.randint(sy, sy + sh - 1)
        lum = rng.randint(50, 160)
        draw.rectangle([px, py, px + 1, py + 1], fill=(lum, lum + 5, lum - 2))

    # Scan lines (horizontal — subtle)
    for scan_y in range(sy, sy + sh, 4):
        draw.line([sx, scan_y, sx + sw, scan_y], fill=(60, 68, 60), width=1)

    # Screen curvature vignette (dark corners)
    vignette_size = min(sw, sh) // 3
    for corner_x, corner_y in [(sx, sy), (sx + sw, sy), (sx, sy + sh), (sx + sw, sy + sh)]:
        for r in range(vignette_size, 0, -4):
            alpha = int(40 * (1 - r / vignette_size))
            glow  = Image.new('RGBA', img.size, (0, 0, 0, 0))
            gd    = ImageDraw.Draw(glow)
            gd.ellipse([corner_x - r, corner_y - r, corner_x + r, corner_y + r],
                       fill=(0, 0, 0, alpha))
            base  = img.convert('RGBA')
            img.paste(Image.alpha_composite(base, glow).convert('RGB'))
    draw = ImageDraw.Draw(img)

    if pixel_shape:
        # PIXEL SHAPE: proto-Glitchkin visible in static — lower-center of screen
        # An irregular cluster of cyan pixels that suggests a small figure / presence
        px_cx = sx + sw // 2 - 8   # slightly left of center
        px_cy = sy + int(sh * 0.62)  # lower area of screen

        # Bright pixel cluster (character silhouette suggestion)
        pixel_coords = [
            # Head cluster
            (px_cx, px_cy - 12), (px_cx + 2, px_cy - 12),
            (px_cx, px_cy - 10), (px_cx + 2, px_cy - 10), (px_cx - 2, px_cy - 10),
            # Body
            (px_cx, px_cy - 8), (px_cx, px_cy - 6), (px_cx + 2, px_cy - 6),
            (px_cx - 2, px_cy - 6),
            # Arms suggestion
            (px_cx - 4, px_cy - 6), (px_cx + 4, px_cy - 6),
            # Lower body
            (px_cx - 2, px_cy - 4), (px_cx + 2, px_cy - 4),
        ]
        for pxp, pyp in pixel_coords:
            draw.rectangle([pxp, pyp, pxp + 2, pyp + 2], fill=PIXEL_CYAN)
        # Brightest pixels (core of shape)
        for pxp, pyp in [(px_cx, px_cy - 10), (px_cx, px_cy - 8), (px_cx, px_cy - 6)]:
            draw.rectangle([pxp, pyp, pxp + 2, pyp + 2], fill=PIXEL_BRIGHT)

        # Glow around pixel shape
        add_glow(img, px_cx + 1, px_cy - 8, 22, CRT_CYAN, steps=4, max_alpha=55)

    return draw


def draw_tv(draw, img, rng):
    """CRT TV — right half of frame, fills BG-right."""
    # TV dimensions — large, fills right side (MCU on TV + Luma side by side)
    tv_left  = int(PW * 0.46)
    tv_top   = int(DRAW_H * 0.08)
    tv_right = PW - 8
    tv_bot   = int(DRAW_H * 0.88)
    tv_w     = tv_right - tv_left
    tv_h     = tv_bot - tv_top

    # TV body (deep plastic — old CRT, rounded corners)
    draw.rectangle([tv_left, tv_top, tv_right, tv_bot],
                   fill=TV_BODY, outline=TV_TRIM, width=4)
    # Rounded corner suggestion
    corner_r = 18
    for cx, cy in [(tv_left + corner_r, tv_top + corner_r),
                   (tv_right - corner_r, tv_top + corner_r),
                   (tv_left + corner_r, tv_bot - corner_r),
                   (tv_right - corner_r, tv_bot - corner_r)]:
        draw.ellipse([cx - corner_r, cy - corner_r, cx + corner_r, cy + corner_r],
                     fill=TV_BODY)

    # TV bezel/frame around screen
    bezel = 22
    screen_left  = tv_left  + bezel
    screen_top   = tv_top   + bezel
    screen_right = tv_right - bezel
    screen_bot   = tv_bot   - int(tv_h * 0.18)  # bottom of screen (not full TV height)
    screen_w = screen_right - screen_left
    screen_h = screen_bot   - screen_top

    # Draw static on screen
    draw = draw_crt_static(draw, img, screen_left, screen_top, screen_w, screen_h,
                            rng, pixel_shape=True)
    draw = ImageDraw.Draw(img)

    # Screen bezel inner shadow
    draw.rectangle([screen_left, screen_top, screen_right, screen_bot],
                   outline=(30, 24, 18), width=2)

    # TV bottom section (controls/vents)
    ctrl_y = screen_bot + 4
    ctrl_h = tv_bot - screen_bot - 8
    # Power LED (lit — orange-amber, TV is on)
    led_cx = tv_left + tv_w - 30
    led_cy = ctrl_y + ctrl_h // 2
    draw.ellipse([led_cx - 4, led_cy - 4, led_cx + 4, led_cy + 4],
                 fill=(220, 140, 40))
    add_glow(img, led_cx, led_cy, 12, (220, 140, 40), steps=3, max_alpha=50)
    draw = ImageDraw.Draw(img)

    # Channel/volume knobs
    for knob_x in [tv_left + 24, tv_left + 48]:
        draw.ellipse([knob_x - 7, ctrl_y + ctrl_h // 2 - 7,
                      knob_x + 7, ctrl_y + ctrl_h // 2 + 7],
                     fill=(70, 62, 50), outline=TV_TRIM, width=1)
        # Knob indicator line
        draw.line([knob_x, ctrl_y + ctrl_h // 2,
                   knob_x + 4, ctrl_y + ctrl_h // 2 - 4], fill=TV_TRIM, width=1)

    # Old stickers on TV body (partial)
    sticker_colors = [(200, 60, 60), (60, 180, 60), (220, 200, 60)]
    for i, sc in enumerate(sticker_colors):
        sx = tv_left + 14 + i * 18
        sy = tv_top + 14
        draw.rectangle([sx, sy, sx + 12, sy + 8], fill=sc, outline=(150, 140, 120), width=1)

    # CRT screen phosphor glow bleeding out of screen
    screen_cx = (screen_left + screen_right) // 2
    screen_cy = (screen_top + screen_bot) // 2
    add_glow(img, screen_cx, screen_cy, 130, CRT_GLOW, steps=6, max_alpha=25)
    draw = ImageDraw.Draw(img)

    return draw


def draw_luma_mcu(draw, img):
    """
    Luma — MEDIUM CU, 3/4 profile facing right (toward TV screen).
    Leaning in close — curiosity / verging on surprise.
    CRT glow lights her face (cool cyan-blue on right side of face).
    Only upper body and face visible (MCU — cropped at waist or chest).
    """
    # Luma body position: left half of frame, profile (face turned right toward TV)
    luma_cx   = int(PW * 0.22)
    torso_top = int(DRAW_H * 0.52)
    torso_bot = DRAW_H + 20   # cropped below frame (MCU)
    torso_w   = 80
    head_r    = 44

    # Head center — slightly right (leaning toward TV)
    head_cx  = luma_cx + 14   # lean right = toward screen
    head_cy  = torso_top - head_r - 4

    # Body shadow (room is dark — CRT is primary light)
    draw.rectangle([luma_cx - torso_w // 2 - 10, torso_top,
                    luma_cx + torso_w // 2 + 20, DRAW_H + 20],
                   fill=LUMA_HOODIE, outline=LUMA_OUTLINE, width=2)

    # ── Hair ─────────────────────────────────────────────────────────────────
    draw.ellipse([head_cx - head_r - 16, head_cy - head_r - 18,
                  head_cx + head_r + 10, head_cy + head_r + 6],
                 fill=LUMA_HAIR)
    for hx, hy, hr in [(head_cx - head_r - 8, head_cy - head_r - 10, 8),
                        (head_cx + head_r + 4, head_cy - head_r - 6, 7),
                        (head_cx - head_r + 2, head_cy - head_r - 16, 9)]:
        draw.ellipse([hx - hr, hy - hr, hx + hr, hy + hr], fill=LUMA_HAIR)

    # ── Face ─────────────────────────────────────────────────────────────────
    draw.ellipse([head_cx - head_r, head_cy - head_r,
                  head_cx + head_r, head_cy + head_r],
                 fill=LUMA_SKIN, outline=LUMA_OUTLINE, width=2)

    # CRT glow on face — right side (facing the screen)
    glow_layer = Image.new('RGBA', (PW, DRAW_H), (0, 0, 0, 0))
    gl = ImageDraw.Draw(glow_layer)
    for r in [55, 38, 24]:
        alpha = max(10, 38 - r // 2)
        gl.ellipse([head_cx + head_r // 3 - r, head_cy - r,
                    head_cx + head_r // 3 + r, head_cy + r],
                   fill=(*CRT_GLOW, alpha))
    base = img.convert('RGBA')
    panel = base.crop((0, 0, PW, DRAW_H))
    merged = Image.alpha_composite(panel.convert('RGBA'), glow_layer)
    img.paste(merged.convert('RGB'), (0, 0))
    draw = ImageDraw.Draw(img)

    # Eyes — wide open, looking right (toward TV), CURIOUS → SURPRISED
    eye_y   = head_cy - 5
    # 3/4 profile: one eye more visible (right eye closer to camera, wider)
    # Left eye (back of profile) — smaller
    left_eye_x  = head_cx - int(head_r * 0.30)
    right_eye_x = head_cx + int(head_r * 0.20)

    # Left eye (less visible in 3/4)
    draw.ellipse([left_eye_x - 10, eye_y - 7, left_eye_x + 10, eye_y + 7],
                 fill=(245, 242, 235), outline=LUMA_OUTLINE, width=1)
    draw.ellipse([left_eye_x - 5, eye_y - 5, left_eye_x + 5, eye_y + 5],
                 fill=LUMA_EYE)
    draw.ellipse([left_eye_x - 3, eye_y - 3, left_eye_x + 3, eye_y + 3],
                 fill=(18, 12, 6))

    # Right eye (more visible — wider open — CURIOUS)
    draw.ellipse([right_eye_x - 15, eye_y - 11, right_eye_x + 15, eye_y + 11],
                 fill=(245, 242, 235), outline=LUMA_OUTLINE, width=1)
    draw.ellipse([right_eye_x - 8, eye_y - 7, right_eye_x + 8, eye_y + 7],
                 fill=LUMA_EYE)
    draw.ellipse([right_eye_x - 5, eye_y - 5, right_eye_x + 5, eye_y + 5],
                 fill=(18, 12, 6))
    # Highlight (CRT reflection in eye)
    draw.rectangle([right_eye_x + 2, eye_y - 5, right_eye_x + 5, eye_y - 2],
                   fill=(0, 240, 255))

    # Brows — raised/arched (curiosity + verging on surprise)
    brow_y = eye_y - 14
    draw.arc([left_eye_x - 10, brow_y - 5, left_eye_x + 10, brow_y + 4],
             start=200, end=340, fill=LUMA_HAIR, width=2)
    draw.arc([right_eye_x - 15, brow_y - 7, right_eye_x + 15, brow_y + 4],
             start=200, end=340, fill=LUMA_HAIR, width=2)

    # Nose (3/4 — slight profile)
    draw.arc([head_cx - 4, head_cy + 4, head_cx + 12, head_cy + 16],
             start=240, end=300, fill=LUMA_OUTLINE, width=1)

    # Mouth — open (CURIOUS / verging on "woah") — O shape, slight open
    mouth_cy = head_cy + int(head_r * 0.45)
    draw.arc([head_cx - int(head_r * 0.25), mouth_cy - 5,
              head_cx + int(head_r * 0.22), mouth_cy + 8],
             start=20, end=160, fill=LUMA_OUTLINE, width=2)
    # Upper lip
    draw.arc([head_cx - int(head_r * 0.22), mouth_cy - 8,
              head_cx + int(head_r * 0.20), mouth_cy - 2],
             start=200, end=340, fill=(180, 130, 90), width=1)

    # ── Arm (reaching slightly toward screen) ────────────────────────────────
    shoulder_y = torso_top + 10
    elbow_x    = luma_cx + torso_w // 2 + 15
    elbow_y    = shoulder_y + 35
    hand_x     = luma_cx + torso_w // 2 + 32
    hand_y     = shoulder_y + 20
    draw.line([(luma_cx + torso_w // 2, shoulder_y),
               (elbow_x, elbow_y), (hand_x, hand_y)],
              fill=LUMA_HOODIE, width=14)
    draw.ellipse([hand_x - 9, hand_y - 8, hand_x + 9, hand_y + 8],
                 fill=LUMA_SKIN, outline=LUMA_OUTLINE)

    return draw


def make_panel():
    font_cap = load_font(12)
    font_ann = load_font(11)
    rng      = random.Random(103)

    img  = Image.new('RGB', (PW, PH), BG_DARK)
    draw = ImageDraw.Draw(img)

    # BG: dark room
    draw.rectangle([0, 0, PW, DRAW_H], fill=BG_DARK)
    draw.rectangle([0, int(DRAW_H * 0.75), PW, DRAW_H], fill=FLOOR_DARK)
    draw.line([(0, int(DRAW_H * 0.75)), (PW, int(DRAW_H * 0.75))],
              fill=(50, 40, 28), width=2)

    # Draw TV first (BG-right)
    draw = draw_tv(draw, img, rng)
    draw = ImageDraw.Draw(img)

    # Draw Luma (FG-left, MCU)
    draw = draw_luma_mcu(draw, img)
    draw = ImageDraw.Draw(img)

    # Annotations
    draw.text((10, 8), "A1-03  /  MEDIUM CU  /  eye-level  /  Luma + TV",
              font=font_ann, fill=ANN_COL)
    draw.text((10, 20), "Discovery — pixel shape in static — CURIOUS → SURPRISED",
              font=font_ann, fill=ANN_DIM)

    # Luma callout
    draw.text((14, int(DRAW_H * 0.12)), "LUMA",
              font=font_ann, fill=CALLOUT_L)
    draw.text((14, int(DRAW_H * 0.12) + 10), "CURIOUS → SURPRISED",
              font=font_ann, fill=(220, 200, 100))
    draw.text((14, int(DRAW_H * 0.12) + 20), "leaning in / reaching",
              font=font_ann, fill=ANN_DIM)

    # TV callout
    draw.text((int(PW * 0.52), int(DRAW_H * 0.06)), "CRT TV — static",
              font=font_ann, fill=CALLOUT_TV)
    draw.text((int(PW * 0.52), int(DRAW_H * 0.06) + 10), "PIXEL SHAPE",
              font=font_ann, fill=(0, 240, 255))
    draw.text((int(PW * 0.52), int(DRAW_H * 0.06) + 20), "= something in there",
              font=font_ann, fill=(0, 190, 210))

    # Arrow pointing to pixel shape on screen (approximate screen center-left)
    pixel_label_x = int(PW * 0.52)
    pixel_label_y = int(DRAW_H * 0.06) + 32
    pixel_target_x = int(PW * 0.54)
    pixel_target_y = int(DRAW_H * 0.62)
    draw.line([(pixel_label_x + 20, pixel_label_y + 4),
               (pixel_target_x, pixel_target_y)],
              fill=(0, 200, 220), width=1)
    draw.polygon([(pixel_target_x, pixel_target_y),
                  (pixel_target_x - 4, pixel_target_y - 8),
                  (pixel_target_x + 4, pixel_target_y - 8)],
                 fill=(0, 200, 220))

    # CRT glow callout
    draw.text((14, DRAW_H - 30), "CRT glow on face (right side)",
              font=font_ann, fill=(0, 200, 220))

    # DISCOVERY label
    draw.rectangle([10, DRAW_H - 22, 108, DRAW_H - 5], fill=(28, 22, 16))
    draw.text((14, DRAW_H - 20), "DISCOVERY", font=font_ann, fill=(0, 240, 255))

    # Caption bar
    draw.rectangle([0, DRAW_H, PW, PH], fill=BG_CAPTION)
    draw.line([0, DRAW_H, PW, DRAW_H], fill=(18, 12, 8), width=2)
    draw.text((10, DRAW_H + 5), "A1-03  MEDIUM CU  eye-level  Luma + TV",
              font=font_cap, fill=(160, 155, 130))
    draw.text((10, DRAW_H + 20),
              "Luma close to screen. Something moves in static — a pixel shape. CURIOUS → SURPRISED.",
              font=font_cap, fill=(235, 228, 210))
    draw.text((10, DRAW_H + 36),
              "DISCOVERY beat. CRT glow lights face. First visual evidence of Glitchkin presence.",
              font=font_ann, fill=(150, 140, 110))
    draw.text((PW - 240, DRAW_H + 46), "LTG_SB_act1_panel_a103_v001",
              font=font_ann, fill=(100, 95, 78))

    draw.rectangle([0, 0, PW - 1, PH - 1], outline=(18, 12, 8), width=2)

    img.save(OUTPUT_PATH, "PNG")
    print(f"Saved: {OUTPUT_PATH}")
    return OUTPUT_PATH


if __name__ == "__main__":
    make_panel()
    print("A1-03 panel generation complete (Cycle 18).")
