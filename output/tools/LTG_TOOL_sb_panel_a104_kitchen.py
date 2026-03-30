#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_sb_panel_a104_kitchen.py
Storyboard Panel A1-04 (kitchen cold open) — FIRST CONTACT — Byte appears — Cycle 18
Lee Tanaka, Storyboard Artist

NOTE: A1-04 (classroom near-miss) already exists as LTG_SB_act2_panel_a104.png.
This is the KITCHEN cold open A1-04 — a DIFFERENT beat:
Byte appears on the TV screen. First face-to-face contact.

Beat: Byte appears on the screen. Luma: SURPRISED. Byte: default glow, slightly
indignant at being stared at.

Shot: TWO-SHOT — Luma MCU (left) + TV screen Byte (right)
Camera: Eye-level (child height). Very similar to A1-03 setup but now Byte is
clearly visible on screen — full character reveal on screen.

Luma expression: SURPRISED (wide eyes, jaw slightly dropped, leaning back slightly
from pure reflex — she was leaning in a moment ago, now she recoils an inch).

Byte (on screen): default glow (cyan/teal), slightly indignant expression —
arms crossed if body visible, one eye slightly narrowed (unamused at being stared at),
small body on the screen (he's at 2/3 body reveal in the lower screen area).

Arc: SURPRISED — first contact. "Wait — that looked back at me."
"""

from PIL import Image, ImageDraw, ImageFont
import math, random, os

PANELS_DIR  = "/home/wipkat/team/output/storyboards/panels"
OUTPUT_PATH = os.path.join(PANELS_DIR, "LTG_SB_act1_panel_a104.png")
os.makedirs(PANELS_DIR, exist_ok=True)

PW, PH    = 800, 600
CAPTION_H = 60
DRAW_H    = PH - CAPTION_H

# ── Palette ─────────────────────────────────────────────────────────────────
BG_DARK      = (28, 22, 16)
FLOOR_DARK   = (36, 28, 20)
LINE_DARK    = (100, 72, 40)

# Luma
LUMA_SKIN      = (242, 198, 152)
LUMA_HAIR      = (52,  32,  18)
LUMA_HOODIE    = (88, 158, 200)
LUMA_PANTS     = (88, 102, 130)
LUMA_OUTLINE   = (52,  30,  10)
LUMA_EYE       = (62,  40,  18)

# TV
TV_BODY      = (55, 48, 38)
TV_TRIM      = (72, 62, 50)
CRT_SCREEN   = (90, 105, 92)
CRT_STATIC1  = (130, 140, 128)
CRT_CYAN     = (0, 240, 255)
CRT_GLOW     = (0, 210, 230)

# Byte — digital character on screen
BYTE_BODY    = (0, 185, 210)    # teal/cyan body
BYTE_OUTLINE = (0, 120, 150)
BYTE_EYE_W   = (200, 240, 245) # sclera — digital white
BYTE_PUPIL   = (0, 50, 80)
BYTE_GLOW    = (0, 240, 255)   # electric cyan glow
BYTE_PIXEL   = (0, 255, 255)   # bright pixel accents

BG_CAPTION = (22, 18, 14)
TEXT_CAP   = (235, 228, 210)
ANN_COL    = (200, 175, 120)
ANN_DIM    = (150, 135, 100)
CALLOUT_L  = (220, 200, 140)
CALLOUT_B  = (0, 220, 240)


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


def draw_tv_with_byte(draw, img, rng):
    """
    CRT TV right half of frame, Byte clearly visible on screen.
    Screen: mostly cleared static (Byte's presence has pushed it back slightly).
    Byte: lower-center of screen, 2/3 body visible (chest up + head).
    """
    tv_left  = int(PW * 0.46)
    tv_top   = int(DRAW_H * 0.08)
    tv_right = PW - 8
    tv_bot   = int(DRAW_H * 0.88)
    tv_w     = tv_right - tv_left
    tv_h     = tv_bot   - tv_top

    # TV body
    draw.rectangle([tv_left, tv_top, tv_right, tv_bot],
                   fill=TV_BODY, outline=TV_TRIM, width=4)
    for cx, cy in [(tv_left + 18, tv_top + 18), (tv_right - 18, tv_top + 18),
                   (tv_left + 18, tv_bot - 18), (tv_right - 18, tv_bot - 18)]:
        draw.ellipse([cx - 18, cy - 18, cx + 18, cy + 18], fill=TV_BODY)

    bezel = 22
    sx  = tv_left  + bezel
    sy  = tv_top   + bezel
    sw  = tv_right - bezel - sx
    sh  = int(tv_h * 0.80)
    # Screen bg — less static now (Byte has "displaced" it)
    draw.rectangle([sx, sy, sx + sw, sy + sh], fill=(60, 78, 72))  # cleared/dim screen

    # Residual static at screen edges (Byte displaced center)
    for _ in range(120):
        px = rng.randint(sx, sx + sw - 1)
        py = rng.randint(sy, sy + sh - 1)
        # Static only near screen edges
        edge_dist = min(px - sx, sx + sw - px, py - sy, sy + sh - py)
        if edge_dist < 40:
            lum = rng.randint(40, 130)
            draw.rectangle([px, py, px + 1, py + 1], fill=(lum, lum + 5, lum - 2))

    # Scan lines
    for scan_y in range(sy, sy + sh, 4):
        draw.line([sx, scan_y, sx + sw, scan_y], fill=(48, 60, 56), width=1)

    # Screen glow (strong — Byte is bright)
    screen_cx = sx + sw // 2
    screen_cy = sy + sh // 2
    add_glow(img, screen_cx, screen_cy, 160, CRT_CYAN, steps=7, max_alpha=35)
    draw = ImageDraw.Draw(img)

    # ── BYTE on screen ───────────────────────────────────────────────────────
    # Byte appears center-screen, 2/3 body reveal (chest up + head visible)
    # He's small — this is a CRT TV at medium distance
    byte_cx  = sx + sw // 2
    byte_top = sy + sh // 2 - 10   # appears in lower-center of screen

    # Body proportions — pixel/blocky digital character
    byte_body_w = 36
    byte_body_h = 32
    byte_head_r = 16

    byte_head_cy = byte_top - byte_head_r
    byte_body_top = byte_top

    # Byte's glow aura (he's digital — glows bright on screen)
    add_glow(img, byte_cx, byte_top + byte_body_h // 2, 55,
             BYTE_GLOW, steps=5, max_alpha=55)
    draw = ImageDraw.Draw(img)

    # Body (slightly rectangular — pixel character)
    draw.rectangle([byte_cx - byte_body_w // 2, byte_body_top,
                    byte_cx + byte_body_w // 2, byte_body_top + byte_body_h],
                   fill=BYTE_BODY, outline=BYTE_OUTLINE, width=2)

    # Arms CROSSED (indignant pose) — horizontal lines across torso
    arm_y = byte_body_top + byte_body_h // 2
    # Left arm
    draw.rectangle([byte_cx - byte_body_w // 2 - 12, arm_y - 5,
                    byte_cx + byte_body_w // 2 + 2, arm_y + 5],
                   fill=BYTE_BODY, outline=BYTE_OUTLINE, width=1)
    # Right arm crossing over
    draw.rectangle([byte_cx - byte_body_w // 2, arm_y - 9,
                    byte_cx + byte_body_w // 2 + 12, arm_y + 1],
                   fill=BYTE_BODY, outline=BYTE_OUTLINE, width=1)
    # Arm cross indication (line)
    draw.line([(byte_cx - byte_body_w // 2 + 4, arm_y - 3),
               (byte_cx + byte_body_w // 2 - 4, arm_y - 3)],
              fill=BYTE_OUTLINE, width=2)

    # Pixel accents on body
    for px_off in [-12, 0, 12]:
        draw.rectangle([byte_cx + px_off - 2, byte_body_top + 4,
                        byte_cx + px_off + 2, byte_body_top + 8],
                       fill=BYTE_PIXEL)

    # Head
    draw.rectangle([byte_cx - byte_head_r, byte_head_cy - byte_head_r,
                    byte_cx + byte_head_r, byte_head_cy + byte_head_r],
                   fill=BYTE_BODY, outline=BYTE_OUTLINE, width=2)

    # Eyes — INDIGNANT: one eye slightly narrowed, one normal
    # Left eye (viewer's left — his right) — slightly squinted (one-eyebrow raise)
    le_x = byte_cx - byte_head_r // 2
    re_x = byte_cx + byte_head_r // 2
    eye_y = byte_head_cy - 2

    # Left eye — normal width
    draw.rectangle([le_x - 5, eye_y - 4, le_x + 5, eye_y + 4],
                   fill=BYTE_EYE_W, outline=BYTE_OUTLINE, width=1)
    draw.rectangle([le_x - 3, eye_y - 3, le_x + 3, eye_y + 3],
                   fill=BYTE_PUPIL)

    # Right eye — narrowed (indignant squint)
    draw.rectangle([re_x - 5, eye_y - 2, re_x + 5, eye_y + 4],
                   fill=BYTE_EYE_W, outline=BYTE_OUTLINE, width=1)
    draw.rectangle([re_x - 3, eye_y - 1, re_x + 3, eye_y + 3],
                   fill=BYTE_PUPIL)

    # Brows — asymmetric (indignant: one raised HIGH, other flat/down)
    # Left brow — raised high (surprise / "who are YOU")
    draw.line([le_x - 6, eye_y - 8, le_x + 6, eye_y - 10],
              fill=BYTE_OUTLINE, width=2)
    # Right brow — flat/lowered (annoyed)
    draw.line([re_x - 6, eye_y - 5, re_x + 6, eye_y - 4],
              fill=BYTE_OUTLINE, width=2)

    # Mouth — flat, slightly downturned (unamused / "really?")
    draw.line([byte_cx - 6, byte_head_cy + byte_head_r // 2 + 2,
               byte_cx + 6, byte_head_cy + byte_head_r // 2 + 2],
              fill=BYTE_OUTLINE, width=2)
    # Corner downturns
    draw.line([byte_cx - 6, byte_head_cy + byte_head_r // 2 + 2,
               byte_cx - 8, byte_head_cy + byte_head_r // 2 + 5],
              fill=BYTE_OUTLINE, width=1)

    # Pixel confetti around Byte (his digital presence bleeds into static)
    confetti_positions = [
        (byte_cx - 22, byte_head_cy - 14), (byte_cx + 20, byte_head_cy - 12),
        (byte_cx - 28, byte_top + 10), (byte_cx + 24, byte_top + 8),
        (byte_cx - 18, byte_top + byte_body_h + 6), (byte_cx + 16, byte_top + byte_body_h + 4),
    ]
    for cpx, cpy in confetti_positions:
        draw.rectangle([cpx, cpy, cpx + 3, cpy + 3], fill=BYTE_PIXEL)

    # TV controls bottom
    ctrl_y = sy + sh + 4
    ctrl_h = tv_bot - (sy + sh) - 8
    led_cx = tv_left + tv_w - 30
    led_cy = ctrl_y + max(ctrl_h // 2, 6)
    draw.ellipse([led_cx - 4, led_cy - 4, led_cx + 4, led_cy + 4], fill=(220, 140, 40))
    add_glow(img, led_cx, led_cy, 12, (220, 140, 40), steps=3, max_alpha=50)

    # Stickers
    for i, sc in enumerate([(200, 60, 60), (60, 180, 60)]):
        draw.rectangle([tv_left + 14 + i * 18, tv_top + 14,
                        tv_left + 14 + i * 18 + 12, tv_top + 22],
                       fill=sc, outline=(150, 140, 120), width=1)

    return draw


def draw_luma_surprised(draw, img):
    """
    Luma — MCU left half, SURPRISED reaction to Byte appearing.
    Expression: wide eyes, jaw dropped, slightly leaned back from prior lean-in.
    This is pure shock — "it looked at me."
    """
    luma_cx  = int(PW * 0.20)
    head_r   = 44
    head_cx  = luma_cx + 6
    head_cy  = int(DRAW_H * 0.32)
    torso_top = head_cy + head_r + 4

    # ── Hair ─────────────────────────────────────────────────────────────────
    draw.ellipse([head_cx - head_r - 18, head_cy - head_r - 20,
                  head_cx + head_r + 12, head_cy + head_r + 8],
                 fill=LUMA_HAIR)
    for hx, hy, hr in [(head_cx - head_r - 10, head_cy - head_r - 10, 9),
                        (head_cx + head_r + 6, head_cy - head_r - 6, 7),
                        (head_cx - head_r, head_cy - head_r - 18, 8)]:
        draw.ellipse([hx - hr, hy - hr, hx + hr, hy + hr], fill=LUMA_HAIR)

    # ── Body ─────────────────────────────────────────────────────────────────
    draw.rectangle([luma_cx - 40, torso_top, luma_cx + 46, DRAW_H + 10],
                   fill=LUMA_HOODIE, outline=LUMA_OUTLINE, width=2)

    # CRT glow on face — strong (she's close to the screen)
    glow_layer = Image.new('RGBA', (PW, DRAW_H), (0, 0, 0, 0))
    gl = ImageDraw.Draw(glow_layer)
    for r in [65, 45, 28]:
        alpha = max(12, 45 - r // 2)
        gl.ellipse([head_cx + head_r // 4 - r, head_cy - r,
                    head_cx + head_r // 4 + r, head_cy + r],
                   fill=(*CRT_GLOW, alpha))
    base = img.convert('RGBA')
    panel = base.crop((0, 0, PW, DRAW_H))
    merged = Image.alpha_composite(panel.convert('RGBA'), glow_layer)
    img.paste(merged.convert('RGB'), (0, 0))
    draw = ImageDraw.Draw(img)

    # ── Face ─────────────────────────────────────────────────────────────────
    draw.ellipse([head_cx - head_r, head_cy - head_r,
                  head_cx + head_r, head_cy + head_r],
                 fill=LUMA_SKIN, outline=LUMA_OUTLINE, width=2)

    # Eyes — VERY wide (full surprised aperture)
    eye_y = head_cy - 6
    eye_w = int(head_r * 0.58)
    eye_h = int(head_r * 0.46)  # taller than normal (wide open = more height)

    for side, ex_off in enumerate([int(head_r * 0.25), int(head_r * 0.70)]):
        ex = head_cx + ex_off - head_r // 3
        draw.ellipse([ex - eye_w // 2, eye_y - eye_h // 2,
                      ex + eye_w // 2, eye_y + eye_h // 2],
                     fill=(245, 242, 235), outline=LUMA_OUTLINE, width=1)
        iris_r = int(eye_h * 0.38)
        draw.ellipse([ex - iris_r, eye_y - iris_r, ex + iris_r, eye_y + iris_r],
                     fill=LUMA_EYE)
        draw.ellipse([ex - iris_r + 2, eye_y - iris_r + 2,
                      ex + iris_r - 2, eye_y + iris_r - 2],
                     fill=(18, 12, 6))
        # CRT reflection in eye (cyan highlight)
        draw.rectangle([ex + 2, eye_y - iris_r + 1, ex + 6, eye_y - iris_r + 5],
                       fill=(0, 240, 255))

    # Brows — HIGH raised (full surprise — both brows up)
    brow_y = eye_y - eye_h // 2 - 10
    for ex_off in [int(head_r * 0.25), int(head_r * 0.70)]:
        ex = head_cx + ex_off - head_r // 3
        draw.arc([ex - eye_w // 2, brow_y - 10, ex + eye_w // 2, brow_y + 4],
                 start=200, end=340, fill=LUMA_HAIR, width=2)

    # Mouth — OPEN/DROPPED (surprise — O shape)
    mouth_cy = head_cy + int(head_r * 0.48)
    # Dropped jaw = tall O shape
    draw.ellipse([head_cx - int(head_r * 0.22), mouth_cy - 7,
                  head_cx + int(head_r * 0.18), mouth_cy + 12],
                 fill=(60, 36, 22), outline=LUMA_OUTLINE, width=2)
    # Teeth suggestion (top teeth visible)
    draw.rectangle([head_cx - int(head_r * 0.16), mouth_cy - 5,
                    head_cx + int(head_r * 0.14), mouth_cy - 1],
                   fill=(240, 235, 225))

    # Nose
    draw.arc([head_cx - 5, head_cy + 5, head_cx + 11, head_cy + 15],
             start=240, end=300, fill=LUMA_OUTLINE, width=1)

    # One hand visible (the reaching hand from previous panel — now pulling back slightly)
    draw.ellipse([head_cx + head_r + 5, head_cy + 10,
                  head_cx + head_r + 22, head_cy + 24],
                 fill=LUMA_SKIN, outline=LUMA_OUTLINE)

    return draw


def make_panel():
    font_cap = load_font(12)
    font_ann = load_font(11)
    rng      = random.Random(104)

    img  = Image.new('RGB', (PW, PH), BG_DARK)
    draw = ImageDraw.Draw(img)

    # BG: dark room
    draw.rectangle([0, 0, PW, DRAW_H], fill=BG_DARK)
    draw.rectangle([0, int(DRAW_H * 0.78), PW, DRAW_H], fill=FLOOR_DARK)
    draw.line([(0, int(DRAW_H * 0.78)), (PW, int(DRAW_H * 0.78))],
              fill=(46, 36, 26), width=2)

    # CRT TV with Byte (BG-right)
    draw = draw_tv_with_byte(draw, img, rng)
    draw = ImageDraw.Draw(img)

    # Luma surprised (FG-left)
    draw = draw_luma_surprised(draw, img)
    draw = ImageDraw.Draw(img)

    # Annotations
    draw.text((10, 8), "A1-04  /  TWO-SHOT  /  eye-level  /  Luma MCU + TV screen Byte",
              font=font_ann, fill=ANN_COL)
    draw.text((10, 20), "FIRST CONTACT — Byte appears. Luma: SURPRISED. Byte: INDIGNANT.",
              font=font_ann, fill=ANN_DIM)

    # Luma callout
    draw.text((14, int(DRAW_H * 0.06)), "LUMA",
              font=font_ann, fill=CALLOUT_L)
    draw.text((14, int(DRAW_H * 0.06) + 10), "SURPRISED",
              font=font_ann, fill=(220, 200, 100))
    draw.text((14, int(DRAW_H * 0.06) + 20), "jaw dropped / eyes MAX",
              font=font_ann, fill=ANN_DIM)

    # Byte callout
    draw.text((int(PW * 0.50), int(DRAW_H * 0.06)), "BYTE",
              font=font_ann, fill=CALLOUT_B)
    draw.text((int(PW * 0.50), int(DRAW_H * 0.06) + 10), "INDIGNANT",
              font=font_ann, fill=(0, 200, 220))
    draw.text((int(PW * 0.50), int(DRAW_H * 0.06) + 20), "arms crossed / squint",
              font=font_ann, fill=(0, 170, 190))

    # "it looked at me" beat note
    draw.text((int(PW * 0.28), int(DRAW_H * 0.82)), '"it looked at me"',
              font=font_ann, fill=(200, 180, 120))

    # FIRST CONTACT label
    draw.rectangle([10, DRAW_H - 22, 130, DRAW_H - 5], fill=(18, 14, 10))
    draw.text((14, DRAW_H - 20), "FIRST CONTACT", font=font_ann, fill=(0, 240, 255))

    # Caption bar
    draw.rectangle([0, DRAW_H, PW, PH], fill=BG_CAPTION)
    draw.line([0, DRAW_H, PW, DRAW_H], fill=(18, 12, 8), width=2)
    draw.text((10, DRAW_H + 5), "A1-04  TWO-SHOT  eye-level  Luma + Byte (on screen)",
              font=font_cap, fill=(160, 155, 130))
    draw.text((10, DRAW_H + 20),
              "Byte appears on CRT screen. Luma: SURPRISED. Byte: default glow, INDIGNANT.",
              font=font_cap, fill=(235, 228, 210))
    draw.text((10, DRAW_H + 36),
              "FIRST CONTACT beat. The Glitchkin see back. Cold open hook. CRT pixel confetti.",
              font=font_ann, fill=(150, 140, 110))
    draw.text((PW - 240, DRAW_H + 46), "LTG_SB_act1_panel_a104_v001",
              font=font_ann, fill=(100, 95, 78))

    draw.rectangle([0, 0, PW - 1, PH - 1], outline=(18, 12, 8), width=2)

    img.save(OUTPUT_PATH, "PNG")
    print(f"Saved: {OUTPUT_PATH}")
    return OUTPUT_PATH


if __name__ == "__main__":
    make_panel()
    print("A1-04 (kitchen) panel generation complete (Cycle 18).")
