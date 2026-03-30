#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_sb_cold_open_P20.py
Cold Open Panel P20 — MED WIDE — Two-Shot: Names Exchanged, New Normal Forming
Diego Vargas, Storyboard Artist — Cycle 47

Beat: First quiet two-shot AFTER the naming beat (P19). The tension has broken.
      Luma sits camera-left with notebook in lap (prop continuity from P18/P19).
      Byte floats camera-right at Luma's eye level (concession — he descended).
      They are talking. Not friends yet, but the hostility is gone.
      The room has settled: CRT static gray-green, warm lamp glow restored.
      Key visual: the NEGATIVE SPACE between them has SHRUNK compared to P17.
      In P17 the gap was 40%+ of the frame. Here it is ~25%. They moved closer
      without either of them deciding to. The composition sells the shift.

Camera: MED WIDE, camera at 4-5ft, flat horizon. Two-shot: Luma L, Byte R.
        Wider framing than P19 — more room context visible. Den settling down.

Key staging:
  - Luma: sitting cross-legged, notebook in lap (open, pencil in hand),
    body angled toward Byte. Expression: INTERESTED (one brow raised, slight
    lean forward). Hoodie LUMA_HOODIE canonical orange.
  - Byte: floating at Luma's seated eye level, NOT on CRT. Arms at sides
    but relaxed (not extended, not hiding). Expression: WARY ACCEPTANCE —
    normal eye 70% open, cracked eye processing dots. Slight rightward
    orientation (3/4 toward Luma).
  - Notebook: open in Luma's lap, tiny doodle marks visible (callback to P18).
  - Den: warm lamp glow left, CRT static right (normal). Monitors NOT blazing.
  - Falling pixel confetti: 3-4 residual pieces drifting down (last of the breach).
  - Depth temperature: Luma warm zone / Byte cool zone (per rule).
  - Negative space between them annotated: "~25% — CLOSER THAN P17"

Arc: CURIOUS / FIRST ENCOUNTER (ELEC_CYAN border — relationship forming).
Output: output/storyboards/panels/LTG_SB_cold_open_P20.png
"""

from PIL import Image, ImageDraw, ImageFont
import math, random, os

PANELS_DIR  = "/home/wipkat/team/output/storyboards/panels"
OUTPUT_PATH = os.path.join(PANELS_DIR, "LTG_SB_cold_open_P20.png")
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
LUMA_HOODIE   = (232, 112, 58)
LUMA_SKIN     = (218, 172, 128)
LUMA_HAIR     = (52, 36, 28)
DEEP_SPACE    = (6, 4, 14)
BYTE_TEAL     = (0, 212, 232)
BYTE_BODY_DK  = (0, 150, 168)
CRT_GLOW      = (0, 160, 180)

BG_CAPTION    = (12, 8, 6)
TEXT_SHOT     = (232, 224, 204)
TEXT_DESC     = (155, 148, 122)
TEXT_META     = (88, 82, 66)
ARC_COLOR     = ELEC_CYAN
ANN_COLOR     = (220, 200, 80)
ANN_CYAN      = (0, 180, 210)
ANN_DIM       = (80, 90, 100)

RNG = random.Random(2020)


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


def draw_panel():
    img  = Image.new('RGB', (PW, PH), DEEP_SPACE)
    draw = ImageDraw.Draw(img)

    # ── Background: den interior (settled) ───────────────────────────────────
    floor_y = int(DRAW_H * 0.70)
    # Floor
    draw.rectangle([0, floor_y, PW, DRAW_H], fill=(40, 32, 24))
    for fy in range(floor_y, DRAW_H, 14):
        draw.line([(0, fy), (PW, fy)], fill=(34, 27, 20), width=1)

    # Wall
    draw.rectangle([0, 0, PW, floor_y], fill=(52, 40, 30))

    # Warm zone (left) — den lamp glow
    add_glow(img, -40, int(DRAW_H * 0.25), int(PW * 0.55), SUNLIT_AMB, steps=8, max_alpha=18)
    draw = ImageDraw.Draw(img)

    # Bookshelf BG left
    shelf_x = 30
    for sy in [int(DRAW_H * 0.12), int(DRAW_H * 0.28), int(DRAW_H * 0.44)]:
        draw.rectangle([shelf_x, sy, shelf_x + 90, sy + 3], fill=(60, 48, 36))
        # Books on shelf
        bx = shelf_x + 4
        for _ in range(RNG.randint(3, 5)):
            bw = RNG.randint(6, 14)
            bh = RNG.randint(16, 28)
            bc = (RNG.randint(60, 140), RNG.randint(40, 100), RNG.randint(30, 80))
            draw.rectangle([bx, sy - bh, bx + bw, sy], fill=bc)
            bx += bw + 2

    # CRT monitors BG right — normal gray-green static (NOT blazing)
    for ci, (cx_m, cy_m, mw, mh) in enumerate([
        (int(PW * 0.78), int(DRAW_H * 0.20), 50, 38),
        (int(PW * 0.90), int(DRAW_H * 0.30), 40, 30),
        (int(PW * 0.82), int(DRAW_H * 0.44), 44, 34),
    ]):
        draw.rectangle([cx_m - mw, cy_m - mh, cx_m + mw, cy_m + mh],
                       fill=(22, 18, 14))
        draw.rectangle([cx_m - mw + 3, cy_m - mh + 3,
                        cx_m + mw - 3, cy_m + mh - 3],
                       fill=(20, 28, 24))
        # Gray-green static
        for _ in range(40):
            sx = RNG.randint(cx_m - mw + 5, cx_m + mw - 5)
            sy = RNG.randint(cy_m - mh + 5, cy_m + mh - 5)
            sv = RNG.randint(22, 45)
            draw.point((sx, sy), fill=(sv, sv + 6, sv + 4))

    # Cool zone (right) — CRT ambient
    add_glow(img, PW + 20, int(DRAW_H * 0.30), int(PW * 0.45), CRT_GLOW, steps=6, max_alpha=12)
    draw = ImageDraw.Draw(img)

    # ── LUMA — Camera Left ───────────────────────────────────────────────────
    luma_cx  = int(PW * 0.30)
    luma_head_cy = int(DRAW_H * 0.38)
    head_r   = 32

    # Body — sitting cross-legged, angled toward Byte (right)
    body_top = luma_head_cy + head_r - 6
    body_w   = 56
    # Hoodie body
    draw.rectangle([luma_cx - body_w // 2, body_top,
                    luma_cx + body_w // 2 + 6, floor_y + 8],
                   fill=LUMA_HOODIE)
    # Shadow on left
    draw.rectangle([luma_cx - body_w // 2, body_top,
                    luma_cx - body_w // 2 + 10, floor_y + 8],
                   fill=lerp_color(LUMA_HOODIE, (120, 60, 30), 0.3))

    # Crossed legs on floor
    leg_y = floor_y - 4
    draw.ellipse([luma_cx - 30, leg_y, luma_cx + 30, leg_y + 18],
                 fill=lerp_color(LUMA_HOODIE, (160, 80, 40), 0.15))

    # Notebook in lap (prop continuity from P18/P19)
    nb_cx = luma_cx + 4
    nb_cy = leg_y + 4
    nb_w, nb_h = 28, 20
    draw.rectangle([nb_cx - nb_w, nb_cy - nb_h // 2,
                    nb_cx + nb_w, nb_cy + nb_h // 2],
                   fill=(245, 240, 228))
    # Tiny doodle marks on the open page
    for _ in range(6):
        dx = nb_cx + RNG.randint(-nb_w + 4, nb_w - 4)
        dy = nb_cy + RNG.randint(-nb_h // 2 + 3, nb_h // 2 - 3)
        draw.point((dx, dy), fill=(80, 72, 60))
    # Ruled lines
    for ry in range(nb_cy - nb_h // 2 + 4, nb_cy + nb_h // 2, 5):
        draw.line([(nb_cx - nb_w + 2, ry), (nb_cx + nb_w - 2, ry)],
                  fill=(180, 200, 218), width=1)

    # Arms — right arm forward holding pencil near notebook, left arm relaxed
    draw.line([(luma_cx + body_w // 2 + 4, body_top + 24),
               (nb_cx + nb_w - 4, nb_cy - 6)],
              fill=LUMA_HOODIE, width=7)
    # Pencil in right hand
    draw.line([(nb_cx + nb_w, nb_cy - 8), (nb_cx + nb_w + 16, nb_cy - 18)],
              fill=(220, 195, 50), width=3)
    # Left arm at side
    draw.line([(luma_cx - body_w // 2, body_top + 24),
               (luma_cx - body_w // 2 - 10, floor_y - 10)],
              fill=LUMA_HOODIE, width=7)

    # Head
    draw.ellipse([luma_cx - head_r, luma_head_cy - head_r,
                  luma_cx + head_r, luma_head_cy + head_r],
                 fill=LUMA_SKIN)

    # Hair
    hair_pts = []
    for i in range(18):
        angle = math.pi + (math.pi * i / 17)
        hr = head_r + RNG.randint(3, 12)
        hair_pts.append((int(luma_cx + hr * math.cos(angle)),
                         int(luma_head_cy + hr * math.sin(angle) - 5)))
    hair_pts.insert(0, (luma_cx + head_r + 5, luma_head_cy))
    hair_pts.append((luma_cx - head_r - 5, luma_head_cy))
    draw.polygon(hair_pts, fill=LUMA_HAIR)

    # Face — 3/4 right (toward Byte). INTERESTED expression.
    eye_y = luma_head_cy - 2
    # Left eye (toward Byte) — open, engaged
    le_cx = luma_cx + 5
    draw.ellipse([le_cx - 6, eye_y - 5, le_cx + 6, eye_y + 5],
                 fill=(240, 236, 228))
    draw.ellipse([le_cx - 3, eye_y - 3, le_cx + 3, eye_y + 3],
                 fill=(55, 42, 32))
    # Raised brow (interested)
    draw.arc([le_cx - 8, eye_y - 16, le_cx + 8, eye_y - 4],
             start=200, end=340, fill=LUMA_HAIR, width=2)

    # Right eye (3/4 foreshortening)
    re_cx = luma_cx - 9
    draw.ellipse([re_cx - 4, eye_y - 4, re_cx + 4, eye_y + 4],
                 fill=(240, 236, 228))
    draw.ellipse([re_cx - 2, eye_y - 2, re_cx + 2, eye_y + 2],
                 fill=(55, 42, 32))
    # Level brow
    draw.arc([re_cx - 6, eye_y - 12, re_cx + 6, eye_y - 3],
             start=200, end=340, fill=LUMA_HAIR, width=2)

    # Nose
    draw.arc([luma_cx + 2, luma_head_cy + 2, luma_cx + 9, luma_head_cy + 12],
             start=0, end=120, fill=lerp_color(LUMA_SKIN, (160, 120, 88), 0.5), width=1)

    # Mouth — slight smile (interested, not grinning)
    draw.arc([luma_cx - 4, luma_head_cy + 12, luma_cx + 8, luma_head_cy + 20],
             start=10, end=170, fill=(170, 110, 85), width=1)

    # ── BYTE — Camera Right ──────────────────────────────────────────────────
    byte_cx   = int(PW * 0.62)
    byte_head_cy = luma_head_cy  # at Luma's seated eye level
    byte_hr   = 24

    # Body — inverted teardrop, floating
    byte_body_w = 28
    byte_body_h = 55
    bt_top = byte_head_cy + byte_hr - 4

    draw.ellipse([byte_cx - byte_body_w // 2, bt_top - 2,
                  byte_cx + byte_body_w // 2, bt_top + byte_body_h // 2],
                 fill=BYTE_TEAL)
    draw.polygon([
        (byte_cx - byte_body_w // 2, bt_top + byte_body_h // 3),
        (byte_cx + byte_body_w // 2, bt_top + byte_body_h // 3),
        (byte_cx, bt_top + byte_body_h)
    ], fill=BYTE_TEAL)

    # Arms at sides, relaxed
    arm_y_b = bt_top + 18
    draw.line([(byte_cx - byte_body_w // 2, arm_y_b),
               (byte_cx - byte_body_w // 2 - 10, arm_y_b + 14)],
              fill=BYTE_TEAL, width=5)
    draw.line([(byte_cx + byte_body_w // 2, arm_y_b),
               (byte_cx + byte_body_w // 2 + 10, arm_y_b + 14)],
              fill=BYTE_TEAL, width=5)

    # Legs (stubby, dangling — he's floating)
    leg_yb = bt_top + byte_body_h
    draw.line([(byte_cx - 6, leg_yb), (byte_cx - 6, leg_yb + 10)],
              fill=BYTE_BODY_DK, width=4)
    draw.line([(byte_cx + 6, leg_yb), (byte_cx + 6, leg_yb + 10)],
              fill=BYTE_BODY_DK, width=4)

    # Desaturation ring on floor below
    desat_cx = byte_cx
    desat_cy = floor_y + 4
    desat_ol = Image.new('RGBA', img.size, (0, 0, 0, 0))
    dd = ImageDraw.Draw(desat_ol)
    dd.ellipse([desat_cx - 24, desat_cy - 8, desat_cx + 24, desat_cy + 8],
               fill=(180, 190, 195, 22))
    base = img.convert('RGBA')
    img.paste(Image.alpha_composite(base, desat_ol).convert('RGB'))
    draw = ImageDraw.Draw(img)

    # Head
    draw.ellipse([byte_cx - byte_hr, byte_head_cy - byte_hr,
                  byte_cx + byte_hr, byte_head_cy + byte_hr],
                 fill=BYTE_TEAL)

    # Eyes — 3/4 toward Luma (facing left)
    be_y = byte_head_cy - 2
    # Left eye (toward Luma) — normal, 70% open
    ble_cx = byte_cx - 6
    ble_r  = 6
    draw.rectangle([ble_cx - ble_r, be_y - ble_r + 2,
                    ble_cx + ble_r, be_y + ble_r - 2],
                   fill=(0, 180, 200))
    # 70% lid (slight squint — wary acceptance, not full open)
    draw.rectangle([ble_cx - ble_r, be_y - ble_r + 2,
                    ble_cx + ble_r, be_y - ble_r + 5],
                   fill=BYTE_TEAL)

    # Right eye (cracked, toward camera/outward)
    bre_cx = byte_cx + 6
    bre_r  = 5
    draw.rectangle([bre_cx - bre_r, be_y - bre_r + 2,
                    bre_cx + bre_r, be_y + bre_r - 2],
                   fill=(0, 160, 180))
    draw.line([(bre_cx - bre_r + 1, be_y - bre_r + 3),
               (bre_cx + bre_r - 1, be_y + bre_r - 3)],
              fill=HOT_MAGENTA, width=1)
    # Processing dots (3, alternating)
    for di in range(3):
        dx = bre_cx - 3 + di * 3
        dy = be_y + bre_r - 4
        dc = ELEC_CYAN if di % 2 == 0 else HOT_MAGENTA
        draw.rectangle([dx - 1, dy - 1, dx + 1, dy + 1], fill=dc)

    # Mouth — neutral (not grimace, not smile)
    draw.line([(byte_cx - 5, byte_head_cy + 8), (byte_cx + 5, byte_head_cy + 8)],
              fill=BYTE_BODY_DK, width=1)

    # ── Residual pixel confetti (very few — last of the breach) ──────────────
    for _ in range(4):
        cx_p = RNG.randint(int(PW * 0.35), int(PW * 0.65))
        cy_p = RNG.randint(int(DRAW_H * 0.55), int(DRAW_H * 0.68))
        sides = RNG.randint(4, 6)
        pr = RNG.randint(2, 3)
        pc = lerp_color(ELEC_CYAN, VOID_BLACK, RNG.uniform(0.4, 0.65))
        draw_irregular_poly(draw, cx_p, cy_p, pr, sides, pc, RNG, fill=True)
        # Dotted descent line
        for dt in range(3):
            draw.point((cx_p, cy_p + dt * 4 + 4), fill=ANN_DIM)

    # ── Annotations ──────────────────────────────────────────────────────────
    font_ann   = load_font(9,  bold=False)
    font_ann_b = load_font(9, bold=True)
    font_sm    = load_font(8,  bold=False)

    draw.text((8, 8), 'MED WIDE  |  TWO-SHOT  |  NAMES EXCHANGED  |  NEW NORMAL',
              font=font_ann, fill=ANN_COLOR)

    # Negative space annotation — CLOSER than P17
    ns_left  = luma_cx + head_r + 14
    ns_right = byte_cx - byte_hr - 14
    ns_cy    = luma_head_cy + head_r + 28
    draw.line([(ns_left, ns_cy), (ns_right, ns_cy)], fill=ANN_DIM, width=1)
    draw.line([(ns_left, ns_cy - 4), (ns_left, ns_cy + 4)], fill=ANN_DIM, width=1)
    draw.line([(ns_right, ns_cy - 4), (ns_right, ns_cy + 4)], fill=ANN_DIM, width=1)
    ns_mid = (ns_left + ns_right) // 2
    draw.text((ns_mid - 40, ns_cy + 5),
              "~25%  CLOSER THAN P17", font=font_sm, fill=ANN_DIM)

    # Notebook callback annotation
    draw.text((nb_cx - nb_w, nb_cy + nb_h // 2 + 4),
              "NOTEBOOK (P18 prop)", font=font_sm, fill=ANN_DIM)

    # ── Three-tier caption bar ────────────────────────────────────────────────
    font_t1   = load_font(13, bold=True)
    font_t2   = load_font(11, bold=False)
    font_t3   = load_font(9,  bold=False)
    font_meta = load_font(8,  bold=False)

    draw.rectangle([0, DRAW_H, PW, PH], fill=BG_CAPTION)
    draw.line([0, DRAW_H, PW, DRAW_H], fill=(8, 6, 4), width=2)

    draw.text((10, DRAW_H + 4),
              "P20  |  MED WIDE  |  TWO-SHOT  |  NAMES EXCHANGED",
              font=font_t1, fill=TEXT_SHOT)

    draw.text((PW - 220, DRAW_H + 5),
              "ARC: CURIOUS / ENCOUNTER", font=font_t2, fill=ELEC_CYAN)

    draw.text((10, DRAW_H + 22),
              "First quiet two-shot after naming. Gap has shrunk — they moved closer.",
              font=font_t3, fill=TEXT_DESC)
    draw.text((10, DRAW_H + 35),
              "Notebook in lap (P18 continuity). Byte at seated eye level (concession).",
              font=font_t3, fill=(120, 112, 90))

    draw.text((PW - 276, DRAW_H + 56),
              "LTG_SB_cold_open_P20  /  Diego Vargas  /  C47",
              font=font_meta, fill=TEXT_META)

    draw.rectangle([0, 0, PW - 1, PH - 1], outline=ARC_COLOR, width=4)

    img.thumbnail((1280, 1280))
    img.save(OUTPUT_PATH, "PNG")
    print(f"Saved: {OUTPUT_PATH}  {img.size}")
    return OUTPUT_PATH


if __name__ == "__main__":
    draw_panel()
    print("P20 standalone panel generation complete.")
    print("Beat: First quiet after naming. Gap shrunk. New normal forming.")
    print("ELEC_CYAN border. MED WIDE two-shot.")
