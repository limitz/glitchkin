#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_sb_cold_open_P13.py
Cold Open Panel P13 — MIRROR COMPOSITION — Commitment / Threshold Beat
Diego Vargas, Storyboard Artist — Cycle 47

This is the THEMATIC FULCRUM of the pitch. The moment between deciding and not-yet-decided.

Beat: Luma camera-left, Byte camera-right. Mirror composition. Equal presence.
      They are at eye level. Each character's inner eye faces center (toward the other);
      each character's outer/damaged eye faces outward (away from the other).
      Byte: organic left eye faces center (toward Luma). Cracked right eye faces outward.
      Luma: open left eye faces center (toward Byte). Doubting right eye faces outward.
      This is the MIRROR: trust faces inward, damage faces outward.

      Byte: full-frontal toward Luma, -3 to -4 degree forward lean. Arms slightly out
      (open, not reaching). ELEC_CYAN glow directional: brighter side toward Luma.
      Lids level (NOT droopy — damage doesn't change his decision).
      Mouth: barely-there WARMTH arc (quiet, not performed).

      Luma: 3/4 toward Byte. Open expression — receiving, not yet committed.

Camera: MED TWO-SHOT, flat horizon, stable. Eye-level guideline + mirror gaze arrows.
Arc: COMMITMENT / THRESHOLD — ARC_COMMIT = (60, 200, 140) border color.
     Warm-cool blend: threshold between worlds.

From MEMORY C39: This is NOT UNGUARDED WARMTH (post-decision). This is the threshold
moment — still arriving. Quiet, subdued. ARC_COMMIT color.

Output: output/storyboards/panels/LTG_SB_cold_open_P13.png
"""

from PIL import Image, ImageDraw, ImageFont
import math, random, os

PANELS_DIR  = "/home/wipkat/team/output/storyboards/panels"
OUTPUT_PATH = os.path.join(PANELS_DIR, "LTG_SB_cold_open_P13.png")
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
LUMA_HAIR     = (52, 36, 28)
DEEP_SPACE    = (6, 4, 14)
ARC_COMMIT    = (60, 200, 140)    # threshold / commitment arc color
CRT_GLOW      = (0, 160, 180)

# Byte
BYTE_TEAL     = (0, 212, 232)
BYTE_BODY_DK  = (0, 150, 168)

# Caption
BG_CAPTION    = (12, 8, 6)
TEXT_SHOT     = (232, 224, 204)
TEXT_DESC     = (155, 148, 122)
TEXT_META     = (88, 82, 66)
ARC_COLOR     = ARC_COMMIT
ANN_COLOR     = (220, 200, 80)
ANN_CYAN      = (0, 180, 210)
ANN_DIM       = (80, 90, 100)

RNG = random.Random(1313)


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


def draw_irregular_poly(draw, cx, cy, r, sides, color, rng, fill=True):
    """Irregular polygon for Glitchkin pixel shapes."""
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


def draw_panel():
    img  = Image.new('RGB', (PW, PH), DEEP_SPACE)
    draw = ImageDraw.Draw(img)

    # ── Background: den interior ─────────────────────────────────────────────
    # Floor
    floor_y = int(DRAW_H * 0.72)
    draw.rectangle([0, floor_y, PW, DRAW_H], fill=(38, 30, 22))
    # Floor plank lines
    for fy in range(floor_y, DRAW_H, 12):
        draw.line([(0, fy), (PW, fy)], fill=(32, 25, 18), width=1)

    # Back wall
    wall_color = (55, 42, 32)
    draw.rectangle([0, 0, PW, floor_y], fill=wall_color)

    # Warm/cool depth split — Luma zone warm (left), Byte zone cool (right)
    # Warm gradient on left side
    warm_overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    wd = ImageDraw.Draw(warm_overlay)
    for col in range(PW // 2):
        alpha = int(22 * (1.0 - col / (PW // 2)))
        wd.line([(col, 0), (col, DRAW_H)], fill=(*SUNLIT_AMB, alpha))
    base = img.convert('RGBA')
    img.paste(Image.alpha_composite(base, warm_overlay).convert('RGB'))
    draw = ImageDraw.Draw(img)

    # Cool gradient on right side
    cool_overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    cd = ImageDraw.Draw(cool_overlay)
    for col in range(PW // 2, PW):
        alpha = int(18 * ((col - PW // 2) / (PW // 2)))
        cd.line([(col, 0), (col, DRAW_H)], fill=(*CRT_GLOW, alpha))
    base = img.convert('RGBA')
    img.paste(Image.alpha_composite(base, cool_overlay).convert('RGB'))
    draw = ImageDraw.Draw(img)

    # CRT monitor in BG, camera-right (behind Byte)
    crt_x = int(PW * 0.80)
    crt_y = int(DRAW_H * 0.28)
    crt_w, crt_h = 60, 48
    draw.rectangle([crt_x - crt_w, crt_y - crt_h, crt_x + crt_w, crt_y + crt_h],
                   fill=(22, 18, 14))
    draw.rectangle([crt_x - crt_w + 4, crt_y - crt_h + 4,
                    crt_x + crt_w - 4, crt_y + crt_h - 4],
                   fill=(18, 30, 34))
    # CRT static
    for _ in range(120):
        sx = RNG.randint(crt_x - crt_w + 6, crt_x + crt_w - 6)
        sy = RNG.randint(crt_y - crt_h + 6, crt_y + crt_h - 6)
        sv = RNG.randint(20, 55)
        draw.point((sx, sy), fill=(sv, sv + 8, sv + 10))

    # CRT glow halo
    add_glow(img, crt_x, crt_y, 100, CRT_GLOW, steps=6, max_alpha=18)
    draw = ImageDraw.Draw(img)

    # ── LUMA — Camera Left ───────────────────────────────────────────────────
    # 3/4 view facing right (toward Byte). Eye level = shared horizon line.
    luma_cx = int(PW * 0.27)
    head_cy = int(DRAW_H * 0.35)
    head_r  = 38

    # Body (hoodie) — 3/4 facing right
    body_top = head_cy + head_r - 8
    body_w   = 52
    body_h   = int(DRAW_H * 0.72) - body_top  # extends to floor
    draw.rectangle([luma_cx - body_w // 2, body_top,
                    luma_cx + body_w // 2 + 8, body_top + body_h],
                   fill=LUMA_HOODIE)
    # Hoodie shadow side (left)
    draw.rectangle([luma_cx - body_w // 2, body_top,
                    luma_cx - body_w // 2 + 12, body_top + body_h],
                   fill=lerp_color(LUMA_HOODIE, (120, 60, 30), 0.3))
    # Arms loose at sides
    draw.line([(luma_cx - body_w // 2, body_top + 30),
               (luma_cx - body_w // 2 - 12, body_top + body_h - 20)],
              fill=LUMA_HOODIE, width=8)
    draw.line([(luma_cx + body_w // 2 + 8, body_top + 30),
               (luma_cx + body_w // 2 + 18, body_top + body_h - 20)],
              fill=LUMA_HOODIE, width=8)

    # Head
    draw.ellipse([luma_cx - head_r, head_cy - head_r,
                  luma_cx + head_r, head_cy + head_r],
                 fill=LUMA_SKIN)

    # Hair cloud — messy, asymmetric
    hair_pts = []
    for i in range(20):
        angle = math.pi + (math.pi * i / 19)  # top half
        hr = head_r + RNG.randint(4, 14)
        hair_pts.append((int(luma_cx + hr * math.cos(angle)),
                         int(head_cy + hr * math.sin(angle) - 6)))
    hair_pts.insert(0, (luma_cx + head_r + 6, head_cy))
    hair_pts.append((luma_cx - head_r - 6, head_cy))
    draw.polygon(hair_pts, fill=LUMA_HAIR)

    # Face — 3/4 right. Two eyes visible.
    eye_y = head_cy - 2
    # LEFT EYE (open — faces center, toward Byte) = TRUST eye
    le_cx = luma_cx + 4
    le_r  = 7
    draw.ellipse([le_cx - le_r, eye_y - 5, le_cx + le_r, eye_y + 5],
                 fill=(240, 236, 228))
    draw.ellipse([le_cx - 3, eye_y - 3, le_cx + 3, eye_y + 3],
                 fill=(55, 42, 32))  # iris
    # Brow — level, open
    draw.arc([le_cx - le_r - 2, eye_y - 14, le_cx + le_r + 2, eye_y - 4],
             start=200, end=340, fill=LUMA_HAIR, width=2)

    # RIGHT EYE (doubting — faces outward) = DOUBT eye
    re_cx = luma_cx - 10
    re_r  = 5  # slightly smaller (3/4 foreshortening)
    draw.ellipse([re_cx - re_r, eye_y - 4, re_cx + re_r, eye_y + 4],
                 fill=(240, 236, 228))
    draw.ellipse([re_cx - 2, eye_y - 2, re_cx + 2, eye_y + 2],
                 fill=(55, 42, 32))
    # Brow — slightly lowered (doubt)
    draw.arc([re_cx - re_r - 2, eye_y - 10, re_cx + re_r + 2, eye_y - 2],
             start=200, end=340, fill=LUMA_HAIR, width=2)

    # Mouth — neutral, slightly parted (receiving)
    mouth_cx = luma_cx - 1
    mouth_cy = head_cy + 14
    draw.arc([mouth_cx - 6, mouth_cy - 2, mouth_cx + 6, mouth_cy + 4],
             start=0, end=180, fill=(160, 100, 80), width=1)

    # Nose hint
    draw.arc([luma_cx + 1, head_cy + 2, luma_cx + 8, head_cy + 12],
             start=0, end=120, fill=lerp_color(LUMA_SKIN, (160, 120, 88), 0.5), width=1)

    # Cyan glow on Luma's right cheek (from Byte's direction)
    add_glow(img, luma_cx + head_r - 4, head_cy, 20, ELEC_CYAN, steps=4, max_alpha=12)
    draw = ImageDraw.Draw(img)

    # ── BYTE — Camera Right ──────────────────────────────────────────────────
    # Full-frontal toward Luma, -3 to -4 degree forward lean.
    byte_cx = int(PW * 0.73)
    byte_head_cy = head_cy  # SAME eye level as Luma (descended to meet her)
    byte_head_r  = 28

    # Forward lean: shift top of body slightly left (toward Luma)
    lean_shift = -6  # pixels leftward at head level

    # Body — inverted teardrop
    byte_body_w = 32
    byte_body_h = 65
    body_top_b  = byte_head_cy + byte_head_r - 6

    # Teardrop: ellipse top + taper bottom
    draw.ellipse([byte_cx + lean_shift - byte_body_w // 2, body_top_b - 4,
                  byte_cx + lean_shift + byte_body_w // 2, body_top_b + byte_body_h // 2],
                 fill=BYTE_TEAL)
    draw.polygon([
        (byte_cx + lean_shift - byte_body_w // 2, body_top_b + byte_body_h // 3),
        (byte_cx + lean_shift + byte_body_w // 2, body_top_b + byte_body_h // 3),
        (byte_cx + lean_shift, body_top_b + byte_body_h)
    ], fill=BYTE_TEAL)

    # Body shadow (right side = away from Luma)
    shadow_overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow_overlay)
    sd.rectangle([byte_cx + lean_shift + byte_body_w // 4, body_top_b,
                  byte_cx + lean_shift + byte_body_w // 2 + 4, body_top_b + byte_body_h],
                 fill=(0, 0, 0, 30))
    base = img.convert('RGBA')
    img.paste(Image.alpha_composite(base, shadow_overlay).convert('RGB'))
    draw = ImageDraw.Draw(img)

    # Arms slightly out — open, not reaching, not hiding
    arm_y = body_top_b + 20
    arm_tip_spread = 14
    draw.line([(byte_cx + lean_shift - byte_body_w // 2, arm_y),
               (byte_cx + lean_shift - byte_body_w // 2 - arm_tip_spread, arm_y + 16)],
              fill=BYTE_TEAL, width=6)
    draw.line([(byte_cx + lean_shift + byte_body_w // 2, arm_y),
               (byte_cx + lean_shift + byte_body_w // 2 + arm_tip_spread, arm_y + 16)],
              fill=BYTE_TEAL, width=6)

    # Stubby legs
    leg_y = body_top_b + byte_body_h
    draw.line([(byte_cx + lean_shift - 8, leg_y),
               (byte_cx + lean_shift - 8, leg_y + 12)],
              fill=BYTE_BODY_DK, width=5)
    draw.line([(byte_cx + lean_shift + 8, leg_y),
               (byte_cx + lean_shift + 8, leg_y + 12)],
              fill=BYTE_BODY_DK, width=5)

    # Desaturation ring on floor
    desat_cx = byte_cx + lean_shift
    desat_cy = int(DRAW_H * 0.72) + 4
    desat_rw = 30
    desat_rh = 10
    desat_ol = Image.new('RGBA', img.size, (0, 0, 0, 0))
    dd = ImageDraw.Draw(desat_ol)
    dd.ellipse([desat_cx - desat_rw, desat_cy - desat_rh,
                desat_cx + desat_rw, desat_cy + desat_rh],
               fill=(180, 190, 195, 25))
    base = img.convert('RGBA')
    img.paste(Image.alpha_composite(base, desat_ol).convert('RGB'))
    draw = ImageDraw.Draw(img)

    # Head
    draw.ellipse([byte_cx + lean_shift - byte_head_r, byte_head_cy - byte_head_r,
                  byte_cx + lean_shift + byte_head_r, byte_head_cy + byte_head_r],
                 fill=BYTE_TEAL)

    # ELEC_CYAN glow directional: L side alpha 75 (toward Luma), body 35, R side 18
    # Brighter toward Luma
    glow_l = Image.new('RGBA', img.size, (0, 0, 0, 0))
    gld = ImageDraw.Draw(glow_l)
    gld.ellipse([byte_cx + lean_shift - byte_head_r - 20,
                 byte_head_cy - byte_head_r - 10,
                 byte_cx + lean_shift,
                 byte_head_cy + byte_head_r + 10],
                fill=(*ELEC_CYAN, 18))
    base = img.convert('RGBA')
    img.paste(Image.alpha_composite(base, glow_l).convert('RGB'))
    draw = ImageDraw.Draw(img)

    # Eyes — MIRROR COMPOSITION
    eye_y_b = byte_head_cy - 2

    # LEFT EYE (organic — faces center/Luma) = the trust eye
    ble_cx = byte_cx + lean_shift - 8
    ble_r  = 7
    # 5x5 pixel grid eye system (simplified at this scale)
    draw.rectangle([ble_cx - ble_r, eye_y_b - ble_r + 2,
                    ble_cx + ble_r, eye_y_b + ble_r - 2],
                   fill=(0, 180, 200))  # Deep Cyan for normal eye
    # Iris dots (pixel grid feel)
    for gx in range(-2, 3):
        for gy in range(-1, 2):
            px = ble_cx + gx * 3
            py = eye_y_b + gy * 3
            if gx * gx + gy * gy <= 4:
                draw.rectangle([px - 1, py - 1, px + 1, py + 1],
                               fill=(0, 140, 160))

    # RIGHT EYE (cracked — faces outward) = the damaged eye
    bre_cx = byte_cx + lean_shift + 8
    bre_r  = 7
    draw.rectangle([bre_cx - bre_r, eye_y_b - bre_r + 2,
                    bre_cx + bre_r, eye_y_b + bre_r - 2],
                   fill=(0, 160, 180))
    # Crack diagonal (HOT_MAGENTA scar)
    draw.line([(bre_cx - bre_r + 1, eye_y_b - bre_r + 3),
               (bre_cx + bre_r - 1, eye_y_b + bre_r - 3)],
              fill=HOT_MAGENTA, width=2)
    # Dead zone upper-right
    draw.rectangle([bre_cx + 2, eye_y_b - bre_r + 3,
                    bre_cx + bre_r - 1, eye_y_b - 1],
                   fill=(8, 8, 16))

    # Lids level — NOT droopy (damage doesn't change his decision)
    # Thin lid lines at top of each eye
    draw.line([(ble_cx - ble_r, eye_y_b - ble_r + 2),
               (ble_cx + ble_r, eye_y_b - ble_r + 2)],
              fill=BYTE_BODY_DK, width=1)
    draw.line([(bre_cx - bre_r, eye_y_b - bre_r + 2),
               (bre_cx + bre_r, eye_y_b - bre_r + 2)],
              fill=BYTE_BODY_DK, width=1)

    # Mouth: barely-there WARMTH arc (quiet, not performed)
    warmth_color = (60, 200, 140, 60)  # ARC_COMMIT tinted, very subtle
    warmth_ol = Image.new('RGBA', img.size, (0, 0, 0, 0))
    wmd = ImageDraw.Draw(warmth_ol)
    mouth_cx_b = byte_cx + lean_shift
    mouth_cy_b = byte_head_cy + 10
    wmd.arc([mouth_cx_b - 8, mouth_cy_b - 2, mouth_cx_b + 8, mouth_cy_b + 6],
            start=10, end=170, fill=(*ARC_COMMIT, 100), width=1)
    base = img.convert('RGBA')
    img.paste(Image.alpha_composite(base, warmth_ol).convert('RGB'))
    draw = ImageDraw.Draw(img)

    # ── Eye-level guideline ──────────────────────────────────────────────────
    # Dashed horizontal line at shared eye level
    for dash_x in range(0, PW, 12):
        draw.line([(dash_x, head_cy), (dash_x + 6, head_cy)],
                  fill=ANN_DIM, width=1)

    # ── Mirror gaze arrows ───────────────────────────────────────────────────
    # Luma's open eye → center
    draw.line([(le_cx + le_r + 4, eye_y), (le_cx + le_r + 30, eye_y)],
              fill=ANN_CYAN, width=1)
    draw.polygon([(le_cx + le_r + 30, eye_y),
                  (le_cx + le_r + 24, eye_y - 4),
                  (le_cx + le_r + 24, eye_y + 4)], fill=ANN_CYAN)

    # Byte's organic eye → center (toward Luma)
    draw.line([(ble_cx - ble_r - 4, eye_y_b), (ble_cx - ble_r - 30, eye_y_b)],
              fill=ANN_CYAN, width=1)
    draw.polygon([(ble_cx - ble_r - 30, eye_y_b),
                  (ble_cx - ble_r - 24, eye_y_b - 4),
                  (ble_cx - ble_r - 24, eye_y_b + 4)], fill=ANN_CYAN)

    # Luma's doubting eye → outward
    draw.line([(re_cx - re_r - 4, eye_y), (re_cx - re_r - 24, eye_y)],
              fill=HOT_MAGENTA, width=1)
    draw.polygon([(re_cx - re_r - 24, eye_y),
                  (re_cx - re_r - 18, eye_y - 3),
                  (re_cx - re_r - 18, eye_y + 3)], fill=HOT_MAGENTA)

    # Byte's cracked eye → outward
    draw.line([(bre_cx + bre_r + 4, eye_y_b), (bre_cx + bre_r + 24, eye_y_b)],
              fill=HOT_MAGENTA, width=1)
    draw.polygon([(bre_cx + bre_r + 24, eye_y_b),
                  (bre_cx + bre_r + 18, eye_y_b - 3),
                  (bre_cx + bre_r + 18, eye_y_b + 3)], fill=HOT_MAGENTA)

    # ── Negative space annotation ────────────────────────────────────────────
    # The gap between them IS the composition
    ns_left  = luma_cx + head_r + 20
    ns_right = byte_cx + lean_shift - byte_head_r - 20
    ns_cy    = head_cy + head_r + 30
    draw.line([(ns_left, ns_cy), (ns_right, ns_cy)],
              fill=ANN_DIM, width=1)
    # Tick marks at ends
    draw.line([(ns_left, ns_cy - 4), (ns_left, ns_cy + 4)],
              fill=ANN_DIM, width=1)
    draw.line([(ns_right, ns_cy - 4), (ns_right, ns_cy + 4)],
              fill=ANN_DIM, width=1)

    # ── Residual pixel confetti (few, fading) ────────────────────────────────
    for _ in range(8):
        cx_p = RNG.randint(int(PW * 0.35), int(PW * 0.65))
        cy_p = RNG.randint(int(DRAW_H * 0.50), int(DRAW_H * 0.70))
        sides = RNG.randint(4, 6)
        pr = RNG.randint(2, 4)
        pc = lerp_color(ELEC_CYAN, VOID_BLACK, RNG.uniform(0.3, 0.6))
        draw_irregular_poly(draw, cx_p, cy_p, pr, sides, pc, RNG, fill=True)

    # ── Annotations ──────────────────────────────────────────────────────────
    font_ann  = load_font(9,  bold=False)
    font_ann_b = load_font(9, bold=True)
    font_sm   = load_font(8,  bold=False)

    draw.text((8, 8), 'MED TWO-SHOT  |  MIRROR COMPOSITION  |  THRESHOLD BEAT',
              font=font_ann, fill=ANN_COLOR)

    # Arrow labels
    draw.text((int(PW * 0.33), head_cy - 20),
              "TRUST inward", font=font_sm, fill=ANN_CYAN)
    draw.text((int(PW * 0.33), head_cy + 8),
              "DAMAGE outward", font=font_sm, fill=lerp_color(HOT_MAGENTA, (255, 255, 255), 0.3))

    # Negative space label
    font_sm_b = load_font(8, bold=True)
    ns_mid = (ns_left + ns_right) // 2
    draw.text((ns_mid - 30, ns_cy + 6),
              "NEGATIVE SPACE", font=font_sm_b, fill=ANN_DIM)

    # Eye level label
    draw.text((PW - 100, head_cy - 12),
              "EYE LEVEL", font=font_sm, fill=ANN_DIM)

    # ── Three-tier caption bar ────────────────────────────────────────────────
    font_t1   = load_font(13, bold=True)
    font_t2   = load_font(11, bold=False)
    font_t3   = load_font(9,  bold=False)
    font_meta = load_font(8,  bold=False)

    draw.rectangle([0, DRAW_H, PW, PH], fill=BG_CAPTION)
    draw.line([0, DRAW_H, PW, DRAW_H], fill=(8, 6, 4), width=2)

    # Tier 1 — Shot code
    draw.text((10, DRAW_H + 4),
              "P13  |  MED TWO-SHOT  |  MIRROR COMPOSITION  |  THRESHOLD",
              font=font_t1, fill=TEXT_SHOT)

    # Tier 2 — Arc label
    draw.text((PW - 200, DRAW_H + 5),
              "ARC: COMMITMENT / THRESHOLD", font=font_t2, fill=ARC_COMMIT)

    # Tier 3 — Narrative description
    draw.text((10, DRAW_H + 22),
              "Trust faces inward, damage faces outward. Threshold moment — still arriving.",
              font=font_t3, fill=TEXT_DESC)
    draw.text((10, DRAW_H + 35),
              "Byte at eye level (descended). Arms open. WARMTH arc barely visible.",
              font=font_t3, fill=(120, 112, 90))

    # Metadata
    draw.text((PW - 276, DRAW_H + 56),
              "LTG_SB_cold_open_P13  /  Diego Vargas  /  C47",
              font=font_meta, fill=TEXT_META)

    # Arc border — ARC_COMMIT (threshold warm-cool blend)
    draw.rectangle([0, 0, PW - 1, PH - 1], outline=ARC_COLOR, width=4)

    img.thumbnail((1280, 1280))
    img.save(OUTPUT_PATH, "PNG")
    print(f"Saved: {OUTPUT_PATH}  {img.size}")
    return OUTPUT_PATH


if __name__ == "__main__":
    draw_panel()
    print("P13 standalone panel generation complete.")
    print("Beat: Mirror composition — trust faces inward, damage faces outward.")
    print("Thematic fulcrum. Byte at eye level. ARC_COMMIT border.")
    print("Luma camera-left, Byte camera-right. Equal presence.")
