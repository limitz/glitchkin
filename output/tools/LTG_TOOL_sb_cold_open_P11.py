#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_sb_cold_open_P11.py
Cold Open Panel P11 — ECU — Luma's Closed Eyes / Brow Twitch / SNAP OPEN
Diego Vargas, Storyboard Artist — Cycle 44

Beat: The "nothing is happening" hold — and then everything.
      ECU on Luma's closed eyes. Cyan glow plays on her face.
      For a long beat: nothing. Then:
        1. The brow TWITCHES (slight asymmetric upward pull — awareness starting)
        2. Eyes SNAP OPEN in the next cut (this panel = the frame just before snap)

This board panel captures STATE A (closed/twitching brow) as the final hold frame.
The SNAP OPEN is the implication — this panel is maximum tension.

Shot:   ECU (Extreme Close Up) — eyes only, face from brow to cheekbone.
Camera: Flat-on to face. Perfectly level. No Dutch tilt.
        Static — this is a HOLD. The stillness sells the beat.

Key staging:
  - Frame: eyebrows down to just below eyes. Brow-to-cheek zone only.
  - Left eye: visible brow twitch — the LEFT brow (from audience view) lifts
    slightly asymmetrically (about 4-5px at this scale = just-perceptible).
  - Right eye: fully settled/closed (no twitch).
  - Cyan glow landing from frame-right (Byte's ambient, screen-right).
  - Warm skin fill — the real-world palette holds.
  - Subtle specular catch light on eyelid skin from the cyan.

Annotations:
  - "BROW TWITCH → L brow only" with arrow
  - "HOLD — 12-16 frames before cut"
  - "NEXT CUT: EYES SNAP" annotation (off-panel right)

Arc: TENSE / THRESHOLD — HOT_MAGENTA border (highest tension beat before the meet)
Image size rule: ≤ 1280px in both dimensions.
Output: output/storyboards/panels/LTG_SB_cold_open_P11.png
"""

from PIL import Image, ImageDraw, ImageFont
import math, random, os

PANELS_DIR  = "/home/wipkat/team/output/storyboards/panels"
OUTPUT_PATH = os.path.join(PANELS_DIR, "LTG_SB_cold_open_P11.png")
os.makedirs(PANELS_DIR, exist_ok=True)

PW, PH    = 800, 600
CAPTION_H = 72          # 3-tier caption (72px — Jonas Feld C17 brief)
DRAW_H    = PH - CAPTION_H   # 528

# ── Palette ──────────────────────────────────────────────────────────────────
LUMA_SKIN      = (218, 172, 128)
LUMA_SKIN_LIT  = (228, 188, 148)   # Lit by warm room light
LUMA_SKIN_CYAN = (196, 195, 175)   # Cyan-tinted cheek zone (Byte ambient)
LUMA_SKIN_SH   = (175, 128, 88)    # Shadow zones
LUMA_BROW      = (52, 30, 16)      # Brow hair — dark brown
LUMA_LASH      = (42, 22, 10)      # Lash line
LUMA_HAIR_TOP  = (38, 22, 14)      # Hair visible top of frame
WARM_FILL      = (240, 224, 196)   # Warm room ambient on skin
# Glitch / Byte
ELEC_CYAN      = (0, 212, 232)
ELEC_CYAN_DIM  = (0, 140, 160)
ELEC_CYAN_LT   = (130, 240, 250)   # Catch light on eyelid skin
HOT_MAGENTA    = (232, 0, 152)
# Caption
BG_CAPTION     = (12, 8, 6)
TEXT_SHOT      = (232, 224, 204)   # Tier 1 — shot code (largest/boldest)
TEXT_ARC       = HOT_MAGENTA       # Tier 2 — arc label (TENSE = magenta)
TEXT_DESC      = (155, 148, 122)   # Tier 3 — narrative description
TEXT_META      = (88, 82, 66)      # Metadata (smallest)
ARC_COLOR      = HOT_MAGENTA       # TENSE / THRESHOLD
ANN_COLOR      = (200, 180, 80)    # Annotation arrow/label

RNG = random.Random(1111)


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


def draw_panel():
    img  = Image.new('RGB', (PW, PH), WARM_FILL)
    draw = ImageDraw.Draw(img)

    # ── Background: warm skin fills the frame ─────────────────────────────────
    # ECU — face fills the entire draw area. Skin tone is the BG.
    # Slight gradient warm top to slightly cooler (shadow) bottom.
    for y in range(DRAW_H):
        t = y / DRAW_H
        r = int(LUMA_SKIN_LIT[0] * (1 - t) + LUMA_SKIN_SH[0] * t)
        g = int(LUMA_SKIN_LIT[1] * (1 - t) + LUMA_SKIN_SH[1] * t)
        b = int(LUMA_SKIN_LIT[2] * (1 - t) + LUMA_SKIN_SH[2] * t)
        draw.line([(0, y), (PW, y)], fill=(r, g, b))

    # Hair visible at very top of frame
    hair_h = int(DRAW_H * 0.12)
    draw.rectangle([0, 0, PW, hair_h], fill=LUMA_HAIR_TOP)
    # Hair-to-forehead gradient
    for y in range(hair_h, hair_h + 30):
        t = (y - hair_h) / 30
        r = int(LUMA_HAIR_TOP[0] * (1 - t) + LUMA_SKIN_LIT[0] * t)
        g = int(LUMA_HAIR_TOP[1] * (1 - t) + LUMA_SKIN_LIT[1] * t)
        b = int(LUMA_HAIR_TOP[2] * (1 - t) + LUMA_SKIN_LIT[2] * t)
        draw.line([(0, y), (PW, y)], fill=(r, g, b))

    # Cyan glow from frame-right (Byte's ambient) — directional source: right
    add_glow(img, PW, int(DRAW_H * 0.45), int(PW * 0.9),
             ELEC_CYAN, steps=12, max_alpha=32)
    draw = ImageDraw.Draw(img)

    # ── Face geometry — ECU: brow-to-cheek zone ───────────────────────────────
    # Frame: upper edge at hairline, lower edge at lower cheekbone.
    # Left eye (audience-left = Luma's right) — settled, closed
    # Right eye (audience-right = Luma's left) — brow twitching

    # Key coordinates — ECU fills frame generously
    face_cx = PW // 2
    eye_y   = int(DRAW_H * 0.48)    # Eye center y
    eye_sep = int(PW * 0.27)        # Distance from center to each eye

    le_cx = face_cx - eye_sep       # Left eye center (audience-left)
    re_cx = face_cx + eye_sep       # Right eye center (audience-right, TWITCHING)
    eye_w = int(PW * 0.19)         # Eye horizontal half-width
    eye_h = int(DRAW_H * 0.06)     # Eye vertical half-height (closed = thin arc)

    # ── Left eye (settled, closed) ─────────────────────────────────────────
    # Upper eyelid: closed arch over eye socket
    for lid_y in range(eye_y - eye_h - 2, eye_y + eye_h + 2):
        t = (lid_y - (eye_y - eye_h)) / (2 * eye_h + 4)
        # Ellipse mask — within eyelid zone
        pass  # We'll draw as arcs

    # Eyelid skin fill (the closed lid — just warm skin over eye socket)
    draw.ellipse([le_cx - eye_w, eye_y - eye_h,
                  le_cx + eye_w, eye_y + eye_h],
                 fill=LUMA_SKIN)

    # Top lid line (lash line)
    draw.arc([le_cx - eye_w, eye_y - eye_h - 3,
              le_cx + eye_w, eye_y + eye_h + 3],
             start=200, end=340, fill=LUMA_LASH, width=3)

    # Lash hints — 5 short lines downward from top lid arc
    for li in range(5):
        lx = le_cx - int(eye_w * 0.6) + li * int(eye_w * 0.3)
        ly0 = eye_y - eye_h
        ly1 = ly0 - RNG.randint(4, 9)
        draw.line([(lx, ly0), (lx, ly1)], fill=LUMA_LASH, width=1)

    # Bottom lid line (softer)
    draw.arc([le_cx - eye_w, eye_y - eye_h + 4,
              le_cx + eye_w, eye_y + eye_h + 4],
             start=20, end=160, fill=LUMA_SKIN_SH, width=1)

    # ── Left brow — settled (no twitch) ────────────────────────────────────
    le_brow_y = eye_y - eye_h - int(eye_h * 1.8)
    brow_l_pts = [
        (le_cx - int(eye_w * 0.85), le_brow_y + 4),
        (le_cx - int(eye_w * 0.2),  le_brow_y - 2),    # peak
        (le_cx + int(eye_w * 0.6),  le_brow_y + 5),
    ]
    for bi in range(len(brow_l_pts) - 1):
        draw.line([brow_l_pts[bi], brow_l_pts[bi + 1]],
                  fill=LUMA_BROW, width=3)

    # ── Right eye (TWITCHING brow — audience-right = Luma's left) ─────────
    # Eye itself is still closed — the BROW is what's twitching.
    draw.ellipse([re_cx - eye_w, eye_y - eye_h,
                  re_cx + eye_w, eye_y + eye_h],
                 fill=LUMA_SKIN)

    draw.arc([re_cx - eye_w, eye_y - eye_h - 3,
              re_cx + eye_w, eye_y + eye_h + 3],
             start=200, end=340, fill=LUMA_LASH, width=3)

    for li in range(5):
        lx = re_cx - int(eye_w * 0.6) + li * int(eye_w * 0.3)
        ly0 = eye_y - eye_h
        ly1 = ly0 - RNG.randint(4, 9)
        draw.line([(lx, ly0), (lx, ly1)], fill=LUMA_LASH, width=1)

    draw.arc([re_cx - eye_w, eye_y - eye_h + 4,
              re_cx + eye_w, eye_y + eye_h + 4],
             start=20, end=160, fill=LUMA_SKIN_SH, width=1)

    # ── Right brow — TWITCHING: left side lifts ~8px, right side flat ──────
    # TWITCH = inner corner lifts asymmetrically. Outer corner remains flat.
    # This is the JUST-PERCEPTIBLE version — awareness hasn't surfaced yet.
    TWITCH_LIFT = 10    # px upward shift at peak of brow twitch (inner/left side)
    re_brow_y = eye_y - eye_h - int(eye_h * 1.8)
    brow_r_pts = [
        (re_cx - int(eye_w * 0.85), re_brow_y + 4 - TWITCH_LIFT),   # INNER: lifted
        (re_cx - int(eye_w * 0.1),  re_brow_y - 3 - TWITCH_LIFT // 2),  # peak: lifted
        (re_cx + int(eye_w * 0.6),  re_brow_y + 5),                  # OUTER: flat
    ]
    for bi in range(len(brow_r_pts) - 1):
        draw.line([brow_r_pts[bi], brow_r_pts[bi + 1]],
                  fill=LUMA_BROW, width=3)

    # ── Nose bridge (just visible) ───────────────────────────────────────────
    nose_top_y = int(eye_y + eye_h * 1.2)
    draw.arc([face_cx - 8, nose_top_y - 10,
              face_cx + 8, nose_top_y + 18],
             start=250, end=290, fill=LUMA_SKIN_SH, width=2)

    # ── Cheekbones (lower frame) ─────────────────────────────────────────────
    cheek_y = int(DRAW_H * 0.80)
    # Left cheekbone highlight
    draw.ellipse([le_cx - int(eye_w * 0.7), cheek_y - 20,
                  le_cx + int(eye_w * 0.5), cheek_y + 20],
                 fill=LUMA_SKIN_LIT)
    # Right cheekbone — cyan glow tints it
    cheek_r_layer = Image.new('RGBA', (PW, PH), (0, 0, 0, 0))
    cr_d = ImageDraw.Draw(cheek_r_layer)
    cr_d.ellipse([re_cx - int(eye_w * 0.5), cheek_y - 20,
                  re_cx + int(eye_w * 0.7), cheek_y + 20],
                 fill=(*ELEC_CYAN, 18))
    img.paste(Image.alpha_composite(img.convert('RGBA'), cheek_r_layer).convert('RGB'))
    draw = ImageDraw.Draw(img)

    # Warm ambient across forehead zone
    fore_layer = Image.new('RGBA', (PW, PH), (0, 0, 0, 0))
    fd = ImageDraw.Draw(fore_layer)
    fd.rectangle([0, hair_h + 30, PW, eye_y - int(eye_h * 2.5)],
                 fill=(*WARM_FILL, 18))
    img.paste(Image.alpha_composite(img.convert('RGBA'), fore_layer).convert('RGB'))
    draw = ImageDraw.Draw(img)

    # ── Annotations ──────────────────────────────────────────────────────────
    font_ann = load_font(9)
    font_sm  = load_font(8)

    # Brow twitch annotation — right brow
    twitch_label_x = re_cx + int(eye_w * 0.65) + 8
    twitch_label_y = re_brow_y - TWITCH_LIFT // 2 - 8
    draw.text((twitch_label_x, twitch_label_y),
              "BROW TWITCH", font=font_ann, fill=ANN_COLOR)
    draw.text((twitch_label_x, twitch_label_y + 10),
              "R brow only (inner lift)", font=font_sm, fill=(160, 140, 70))
    # Arrow from label toward brow inner peak
    arr_target_x = int(brow_r_pts[1][0]) - 6
    arr_target_y = int(brow_r_pts[1][1])
    draw.line([(twitch_label_x - 2, twitch_label_y + 5),
               (arr_target_x, arr_target_y)],
              fill=ANN_COLOR, width=1)

    # Left brow "SETTLED" annotation
    draw.text((le_cx - int(eye_w * 0.9) - 10, le_brow_y - 16),
              "SETTLED", font=font_sm, fill=(100, 90, 72))

    # Hold duration note
    draw.text((10, int(DRAW_H * 0.08)),
              "HOLD 12–16 FRAMES", font=font_ann, fill=ANN_COLOR)
    draw.text((10, int(DRAW_H * 0.08) + 11),
              "stillness before snap", font=font_sm, fill=(130, 120, 88))

    # Cyan glow annotation (right side)
    draw.text((PW - 120, int(DRAW_H * 0.28)),
              "CYAN GLOW →", font=font_sm, fill=ELEC_CYAN_DIM)
    draw.text((PW - 120, int(DRAW_H * 0.28) + 10),
              "Byte ambient", font=font_sm, fill=(80, 120, 130))

    # NEXT CUT annotation (far right, slightly off panel feel)
    draw.text((PW - 140, DRAW_H - 26),
              "↓ NEXT CUT:", font=font_ann, fill=(180, 120, 60))
    draw.text((PW - 140, DRAW_H - 14),
              "EYES SNAP OPEN", font=font_sm, fill=(200, 140, 70))

    # ── Three-tier caption bar ────────────────────────────────────────────────
    # Tier 1 — Shot code: largest + bold
    # Tier 2 — Arc label: arc-palette color (HOT_MAGENTA for TENSE/THRESHOLD)
    # Tier 3 — Narrative description: smaller/lighter
    font_t1   = load_font(13, bold=True)
    font_t2   = load_font(11, bold=False)
    font_t3   = load_font(9,  bold=False)
    font_meta = load_font(8,  bold=False)

    draw.rectangle([0, DRAW_H, PW, PH], fill=BG_CAPTION)
    draw.line([0, DRAW_H, PW, DRAW_H], fill=(8, 6, 4), width=2)

    # Tier 1 — Shot code
    draw.text((10, DRAW_H + 4),
              "P11  |  ECU  |  STATIC  |  HOLD FRAME",
              font=font_t1, fill=TEXT_SHOT)

    # Tier 2 — Arc label (right, arc-colored — HOT_MAGENTA = TENSE)
    draw.text((PW - 242, DRAW_H + 5),
              "ARC: TENSE / THRESHOLD", font=font_t2, fill=TEXT_ARC)

    # Tier 3 — Narrative description
    draw.text((10, DRAW_H + 22),
              "Luma's closed eyes. Cyan glow (R). R brow twitches — inner-corner asymmetric lift.",
              font=font_t3, fill=TEXT_DESC)

    draw.text((10, DRAW_H + 35),
              "Hold 12–16 frames of nothing. Implication: EYES SNAP OPEN next cut. Max tension.",
              font=font_t3, fill=(120, 112, 90))

    # Metadata
    draw.text((PW - 276, DRAW_H + 56),
              "LTG_SB_cold_open_P11  /  Diego Vargas  /  C44",
              font=font_meta, fill=TEXT_META)

    # Arc border — HOT_MAGENTA (TENSE / THRESHOLD — highest tension before meet)
    draw.rectangle([0, 0, PW - 1, PH - 1], outline=ARC_COLOR, width=4)

    img.thumbnail((1280, 1280))
    img.save(OUTPUT_PATH, "PNG")
    print(f"Saved: {OUTPUT_PATH}  {img.size}")
    return OUTPUT_PATH


if __name__ == "__main__":
    draw_panel()
    print("P11 standalone panel generation complete.")
    print("Caption hierarchy: 3-tier (shot code / arc label / narrative description)")
    print("  Tier 1 — Shot code: bold 13pt WHITE")
    print("  Tier 2 — Arc label: HOT_MAGENTA (TENSE = magenta per arc palette)")
    print("  Tier 3 — Narrative: 9pt lighter")
