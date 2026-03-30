#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_sb_cold_open_P21.py
Cold Open Panel P21 — WIDE HIGH ANGLE — Re-Escalation: All Monitors Blazing
Diego Vargas, Storyboard Artist — Cycle 47

Beat: The second crisis. Everything was settling down — P17 was stillness, P19 was comedy,
      P20 was the new normal forming. Then ALL the monitors in the den light up at once.
      Not one Byte — dozens of Glitchkin pressing against glass. "You're not the only one."

      This is the ACT BREAK DRIVER. It destroys the fragile peace P17-P20 built.
      Byte knows what this means. Luma doesn't. Byte's reaction is the story tell.

Camera: WIDE, HIGH ANGLE (camera ~8ft, looking down at 25-30 degrees).
        High angle makes Luma + Byte look SMALL against the blazing wall of monitors.
        The room is overwhelmed. Dutch tilt 5° CCW (instability returning).

Key staging:
  - ALL monitors blazing: 6-8 CRT screens filling the back wall, all cyan/magenta active
  - Glitchkin hands/faces pressing against glass from INSIDE each screen
  - Screen ripples: distortion rings radiating from press points
  - Byte: camera-right, turned AWAY from Luma, facing the monitors. Body language RIGID.
    He recognizes what is happening. Arms pulled in tight (defensive, not open like P13/P20).
  - Luma: camera-left, still on floor, looking UP at the monitors. Rising to her feet.
    Expression: ALARMED but not panicked. She processes visually.
  - Room flooded with cyan/magenta light — warm glow completely overwhelmed
  - Pixel confetti density returns to P14 levels (28+ particles)
  - Contrast: warm Luma (LUMA_HOODIE orange) is the only warm element in a cold-flooded room

Arc: TENSE / ESCALATION (HOT_MAGENTA border — crisis returning).
Output: output/storyboards/panels/LTG_SB_cold_open_P21.png
"""

from PIL import Image, ImageDraw, ImageFont
import math, random, os

PANELS_DIR  = "/home/wipkat/team/output/storyboards/panels"
OUTPUT_PATH = os.path.join(PANELS_DIR, "LTG_SB_cold_open_P21.png")
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

BG_CAPTION    = (12, 8, 6)
TEXT_SHOT     = (232, 224, 204)
TEXT_DESC     = (155, 148, 122)
TEXT_META     = (88, 82, 66)
ARC_COLOR     = HOT_MAGENTA
ANN_COLOR     = (220, 200, 80)
ANN_CYAN      = (0, 180, 210)
ANN_DIM       = (80, 90, 100)

RNG = random.Random(2121)


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


def draw_glitchkin_hand_press(draw, cx, cy, size, rng):
    """Draw a Glitchkin hand pressing against glass from inside — played/fist press."""
    # Palm
    draw.ellipse([cx - size, cy - size, cx + size, cy + size],
                 fill=lerp_color(BYTE_TEAL, ELEC_CYAN, 0.3))
    # Fingers (3-4 stubby digits spreading)
    for fi in range(rng.randint(3, 4)):
        angle = math.radians(-40 + fi * 30 + rng.randint(-8, 8))
        fx = int(cx + (size + 4) * math.cos(angle))
        fy = int(cy + (size + 4) * math.sin(angle))
        draw.ellipse([fx - 3, fy - 3, fx + 3, fy + 3],
                     fill=BYTE_TEAL)
    # Distortion ring
    ring_r = size + rng.randint(6, 14)
    ring_color = lerp_color(ELEC_CYAN, (255, 255, 255), 0.3)
    draw.ellipse([cx - ring_r, cy - ring_r, cx + ring_r, cy + ring_r],
                 outline=(*ring_color,), width=1)
    # Second ring (wider, fainter)
    ring_r2 = ring_r + rng.randint(4, 8)
    draw.ellipse([cx - ring_r2, cy - ring_r2, cx + ring_r2, cy + ring_r2],
                 outline=lerp_color(ring_color, VOID_BLACK, 0.4), width=1)


def draw_glitchkin_face_press(draw, cx, cy, size, rng):
    """Draw a Glitchkin face pressed flat against glass."""
    # Squished face circle
    face_r = size
    draw.ellipse([cx - face_r, cy - int(face_r * 0.8),
                  cx + face_r, cy + int(face_r * 0.8)],
                 fill=lerp_color(BYTE_TEAL, ELEC_CYAN, rng.uniform(0.1, 0.4)))
    # Two eyes (pixel grid style)
    for ex in [-int(face_r * 0.35), int(face_r * 0.35)]:
        er = max(2, int(face_r * 0.2))
        draw.rectangle([cx + ex - er, cy - er, cx + ex + er, cy + er],
                       fill=(0, 180, 200))
    # One cracked eye (random)
    if rng.random() > 0.4:
        crack_x = cx + int(face_r * 0.35)
        draw.line([(crack_x - 2, cy - 3), (crack_x + 3, cy + 3)],
                  fill=HOT_MAGENTA, width=1)


def draw_panel():
    # Build on slightly larger canvas for Dutch tilt crop
    canvas_w, canvas_h = PW + 40, DRAW_H + 40
    img  = Image.new('RGB', (canvas_w, canvas_h), DEEP_SPACE)
    draw = ImageDraw.Draw(img)

    # ── Background: den from high angle ──────────────────────────────────────
    # Floor visible as large area (high angle = more floor)
    floor_y = int(canvas_h * 0.55)
    draw.rectangle([0, floor_y, canvas_w, canvas_h], fill=(32, 25, 18))
    for fy in range(floor_y, canvas_h, 16):
        draw.line([(0, fy), (canvas_w, fy)], fill=(28, 22, 15), width=1)

    # Wall — shorter due to high angle
    draw.rectangle([0, 0, canvas_w, floor_y], fill=(44, 34, 26))

    # ── MONITOR WALL — all blazing ───────────────────────────────────────────
    # 7 CRT monitors across the back wall, ALL active
    monitors = [
        (int(canvas_w * 0.10), int(canvas_h * 0.12), 52, 40),
        (int(canvas_w * 0.26), int(canvas_h * 0.08), 58, 44),
        (int(canvas_w * 0.42), int(canvas_h * 0.14), 50, 38),
        (int(canvas_w * 0.56), int(canvas_h * 0.06), 54, 42),
        (int(canvas_w * 0.70), int(canvas_h * 0.12), 56, 42),
        (int(canvas_w * 0.84), int(canvas_h * 0.08), 50, 40),
        (int(canvas_w * 0.50), int(canvas_h * 0.28), 46, 36),  # lower shelf
    ]

    for mi, (mx, my, mw, mh) in enumerate(monitors):
        # CRT bezel
        draw.rectangle([mx - mw, my - mh, mx + mw, my + mh],
                       fill=(18, 14, 10))
        # Screen — blazing cyan/magenta
        screen_color = lerp_color(ELEC_CYAN, HOT_MAGENTA, RNG.uniform(0.0, 0.35))
        draw.rectangle([mx - mw + 4, my - mh + 4,
                        mx + mw - 4, my + mh - 4],
                       fill=screen_color)

        # Scanlines on screen
        for sy in range(my - mh + 5, my + mh - 5, 3):
            sc = lerp_color(screen_color, VOID_BLACK, 0.15)
            draw.line([(mx - mw + 5, sy), (mx + mw - 5, sy)],
                      fill=sc, width=1)

        # Glitchkin pressing against glass (hand OR face per monitor)
        n_presses = RNG.randint(1, 3)
        for _ in range(n_presses):
            px = mx + RNG.randint(-mw + 10, mw - 10)
            py = my + RNG.randint(-mh + 10, mh - 10)
            ps = RNG.randint(6, 12)
            if RNG.random() > 0.5:
                draw_glitchkin_hand_press(draw, px, py, ps, RNG)
            else:
                draw_glitchkin_face_press(draw, px, py, ps, RNG)

    # Massive combined glow from all monitors
    for mx, my, mw, mh in monitors:
        add_glow(img, mx, my, max(mw, mh) + 20,
                 lerp_color(ELEC_CYAN, HOT_MAGENTA, RNG.uniform(0.0, 0.3)),
                 steps=4, max_alpha=20)
    draw = ImageDraw.Draw(img)

    # Floor wash — cyan/magenta flood from monitors
    flood = Image.new('RGBA', img.size, (0, 0, 0, 0))
    fd = ImageDraw.Draw(flood)
    for row in range(floor_y, canvas_h, 2):
        t = (row - floor_y) / (canvas_h - floor_y)
        fc = lerp_color(ELEC_CYAN, HOT_MAGENTA, t * 0.5)
        alpha = int(28 * (1.0 - t * 0.5))
        fd.line([(0, row), (canvas_w, row)], fill=(*fc, alpha))
    base = img.convert('RGBA')
    img.paste(Image.alpha_composite(base, flood).convert('RGB'))
    draw = ImageDraw.Draw(img)

    # ── BYTE — Camera Right, facing monitors, RIGID ──────────────────────────
    byte_cx   = int(canvas_w * 0.68)
    byte_cy   = int(canvas_h * 0.52)  # higher up = further from camera at high angle
    byte_hr   = 18  # smaller — high angle makes them look small
    byte_bw   = 22
    byte_bh   = 42

    # Body — stiff, arms pulled IN (defensive)
    bt_top = byte_cy + byte_hr - 3
    draw.ellipse([byte_cx - byte_bw // 2, bt_top,
                  byte_cx + byte_bw // 2, bt_top + byte_bh // 2],
                 fill=BYTE_TEAL)
    draw.polygon([
        (byte_cx - byte_bw // 2, bt_top + byte_bh // 3),
        (byte_cx + byte_bw // 2, bt_top + byte_bh // 3),
        (byte_cx, bt_top + byte_bh)
    ], fill=BYTE_TEAL)

    # Arms pulled in tight — defensive, NOT open
    draw.line([(byte_cx - byte_bw // 2, bt_top + 12),
               (byte_cx - byte_bw // 2 + 2, bt_top + 24)],
              fill=BYTE_TEAL, width=4)
    draw.line([(byte_cx + byte_bw // 2, bt_top + 12),
               (byte_cx + byte_bw // 2 - 2, bt_top + 24)],
              fill=BYTE_TEAL, width=4)

    # Head — facing AWAY from Luma, toward monitors (back of head visible to us)
    draw.ellipse([byte_cx - byte_hr, byte_cy - byte_hr,
                  byte_cx + byte_hr, byte_cy + byte_hr],
                 fill=BYTE_TEAL)
    # Back of head shading (facing monitors = we see back)
    draw.ellipse([byte_cx - byte_hr + 4, byte_cy - byte_hr + 4,
                  byte_cx + byte_hr - 4, byte_cy + byte_hr - 4],
                 fill=BYTE_BODY_DK)
    # Cracked eye visible in profile (right side)
    draw.rectangle([byte_cx + byte_hr - 6, byte_cy - 3,
                    byte_cx + byte_hr - 1, byte_cy + 3],
                   fill=(0, 160, 180))
    draw.line([(byte_cx + byte_hr - 5, byte_cy - 2),
               (byte_cx + byte_hr - 1, byte_cy + 2)],
              fill=HOT_MAGENTA, width=1)

    # Cyan rim light from monitors
    rim_ol = Image.new('RGBA', img.size, (0, 0, 0, 0))
    rd = ImageDraw.Draw(rim_ol)
    rd.arc([byte_cx - byte_hr - 2, byte_cy - byte_hr - 2,
            byte_cx + byte_hr + 2, byte_cy + byte_hr + 2],
           start=200, end=340, fill=(*ELEC_CYAN, 80), width=2)
    base = img.convert('RGBA')
    img.paste(Image.alpha_composite(base, rim_ol).convert('RGB'))
    draw = ImageDraw.Draw(img)

    # Desaturation ring
    desat_ol = Image.new('RGBA', img.size, (0, 0, 0, 0))
    dd = ImageDraw.Draw(desat_ol)
    dd.ellipse([byte_cx - 18, int(canvas_h * 0.62) - 5,
                byte_cx + 18, int(canvas_h * 0.62) + 5],
               fill=(180, 190, 195, 20))
    base = img.convert('RGBA')
    img.paste(Image.alpha_composite(base, desat_ol).convert('RGB'))
    draw = ImageDraw.Draw(img)

    # ── LUMA — Camera Left, still on floor, rising ───────────────────────────
    luma_cx  = int(canvas_w * 0.30)
    luma_cy  = int(canvas_h * 0.56)
    l_hr     = 22  # smaller at high angle

    # Body — getting up from floor, one knee down, one hand pushing up
    body_top = luma_cy + l_hr - 4
    # Hoodie mass (hunched, rising)
    body_pts = [
        (luma_cx - 28, body_top + 40),
        (luma_cx - 22, body_top),
        (luma_cx + 22, body_top - 4),
        (luma_cx + 30, body_top + 36),
    ]
    draw.polygon(body_pts, fill=LUMA_HOODIE)
    # Shadow side
    draw.polygon([
        body_pts[0], body_pts[1],
        (luma_cx - 14, body_top),
        (luma_cx - 20, body_top + 40),
    ], fill=lerp_color(LUMA_HOODIE, (120, 60, 30), 0.3))

    # One arm pushing up from floor
    draw.line([(luma_cx + 24, body_top + 30),
               (luma_cx + 38, body_top + 44)],
              fill=LUMA_HOODIE, width=6)
    # Hand on floor
    draw.ellipse([luma_cx + 36, body_top + 42, luma_cx + 46, body_top + 50],
                 fill=LUMA_SKIN)

    # Other arm bracing on knee
    draw.line([(luma_cx - 20, body_top + 14),
               (luma_cx - 28, body_top + 28)],
              fill=LUMA_HOODIE, width=6)

    # Head — looking UP at monitors
    draw.ellipse([luma_cx - l_hr, luma_cy - l_hr,
                  luma_cx + l_hr, luma_cy + l_hr],
                 fill=LUMA_SKIN)

    # Hair
    hair_pts = []
    for i in range(14):
        angle = math.pi + (math.pi * i / 13)
        hr = l_hr + RNG.randint(2, 8)
        hair_pts.append((int(luma_cx + hr * math.cos(angle)),
                         int(luma_cy + hr * math.sin(angle) - 4)))
    hair_pts.insert(0, (luma_cx + l_hr + 4, luma_cy))
    hair_pts.append((luma_cx - l_hr - 4, luma_cy))
    draw.polygon(hair_pts, fill=LUMA_HAIR)

    # Face — looking UP. Eyes wide (ALARMED but processing).
    # Upward gaze: eyes in lower half of head, irises shifted up
    eye_y_l = luma_cy + 1
    # Left eye
    draw.ellipse([luma_cx + 2, eye_y_l - 4, luma_cx + 12, eye_y_l + 4],
                 fill=(240, 236, 228))
    draw.ellipse([luma_cx + 5, eye_y_l - 4, luma_cx + 9, eye_y_l - 1],
                 fill=(55, 42, 32))  # iris shifted UP
    # Right eye
    draw.ellipse([luma_cx - 10, eye_y_l - 3, luma_cx, eye_y_l + 3],
                 fill=(240, 236, 228))
    draw.ellipse([luma_cx - 7, eye_y_l - 3, luma_cx - 4, eye_y_l],
                 fill=(55, 42, 32))  # iris shifted UP
    # Brows — raised (alarm)
    draw.arc([luma_cx + 1, eye_y_l - 14, luma_cx + 13, eye_y_l - 4],
             start=200, end=340, fill=LUMA_HAIR, width=2)
    draw.arc([luma_cx - 11, eye_y_l - 12, luma_cx + 1, eye_y_l - 4],
             start=200, end=340, fill=LUMA_HAIR, width=2)
    # Mouth — open, small (processing alarm)
    draw.ellipse([luma_cx - 2, luma_cy + 8, luma_cx + 5, luma_cy + 13],
                 fill=(160, 100, 80))

    # Cyan light wash on Luma from monitors
    add_glow(img, luma_cx, luma_cy, 40, ELEC_CYAN, steps=4, max_alpha=10)
    draw = ImageDraw.Draw(img)

    # ── Pixel confetti — FULL DENSITY RETURN ─────────────────────────────────
    for _ in range(30):
        cx_p = RNG.randint(20, canvas_w - 20)
        cy_p = RNG.randint(int(canvas_h * 0.20), int(canvas_h * 0.85))
        sides = RNG.randint(4, 7)
        pr = RNG.randint(2, 5)
        pc_base = ELEC_CYAN if RNG.random() > 0.3 else HOT_MAGENTA
        pc = lerp_color(pc_base, VOID_BLACK, RNG.uniform(0.0, 0.35))
        draw_irregular_poly(draw, cx_p, cy_p, pr, sides, pc, RNG, fill=True)

    # ── Apply Dutch tilt 5° CCW ──────────────────────────────────────────────
    # Crop the draw area, rotate, paste back
    draw_crop = img.crop([0, 0, canvas_w, canvas_h])
    rotated = draw_crop.rotate(5, expand=False, fillcolor=DEEP_SPACE)
    # Crop to final draw area size
    ox = (canvas_w - PW) // 2
    oy = (canvas_h - DRAW_H) // 2
    final_draw = rotated.crop([ox, oy, ox + PW, oy + DRAW_H])

    # Build final image with caption bar
    final = Image.new('RGB', (PW, PH), DEEP_SPACE)
    final.paste(final_draw, (0, 0))
    draw = ImageDraw.Draw(final)

    # ── Annotations (on final, post-tilt) ────────────────────────────────────
    font_ann   = load_font(9,  bold=False)
    font_ann_b = load_font(9, bold=True)
    font_sm    = load_font(8,  bold=False)

    draw.text((8, 8), 'WIDE  |  HIGH ANGLE  |  RE-ESCALATION  |  DUTCH 5 CCW',
              font=font_ann, fill=ANN_COLOR)

    # Monitor wall annotation
    draw.text((int(PW * 0.30), 22),
              "ALL MONITORS BLAZING — Glitchkin pressing through", font=font_sm, fill=ANN_CYAN)

    # Byte annotation
    draw.text((int(PW * 0.62), int(DRAW_H * 0.46)),
              "BYTE: rigid, facing monitors", font=font_sm, fill=ANN_DIM)
    draw.text((int(PW * 0.62), int(DRAW_H * 0.49)),
              "(he KNOWS what this means)", font=font_sm, fill=ANN_DIM)

    # Luma annotation
    draw.text((int(PW * 0.08), int(DRAW_H * 0.72)),
              "LUMA: rising, eyes UP", font=font_sm, fill=ANN_DIM)

    # ── Three-tier caption bar ────────────────────────────────────────────────
    font_t1   = load_font(13, bold=True)
    font_t2   = load_font(11, bold=False)
    font_t3   = load_font(9,  bold=False)
    font_meta = load_font(8,  bold=False)

    draw.rectangle([0, DRAW_H, PW, PH], fill=BG_CAPTION)
    draw.line([0, DRAW_H, PW, DRAW_H], fill=(8, 6, 4), width=2)

    draw.text((10, DRAW_H + 4),
              "P21  |  WIDE HIGH ANGLE  |  RE-ESCALATION  |  ALL MONITORS",
              font=font_t1, fill=TEXT_SHOT)

    draw.text((PW - 200, DRAW_H + 5),
              "ARC: TENSE / ESCALATION", font=font_t2, fill=HOT_MAGENTA)

    draw.text((10, DRAW_H + 22),
              "Second crisis. All monitors blazing. Glitchkin pressing through glass.",
              font=font_t3, fill=TEXT_DESC)
    draw.text((10, DRAW_H + 35),
              "Byte rigid (he knows). Luma rising (she doesn't). Act break driver.",
              font=font_t3, fill=(120, 112, 90))

    draw.text((PW - 276, DRAW_H + 56),
              "LTG_SB_cold_open_P21  /  Diego Vargas  /  C47",
              font=font_meta, fill=TEXT_META)

    draw.rectangle([0, 0, PW - 1, PH - 1], outline=ARC_COLOR, width=4)

    final.thumbnail((1280, 1280))
    final.save(OUTPUT_PATH, "PNG")
    print(f"Saved: {OUTPUT_PATH}  {final.size}")
    return OUTPUT_PATH


if __name__ == "__main__":
    draw_panel()
    print("P21 standalone panel generation complete.")
    print("Beat: Re-escalation. All monitors blazing. Second crisis.")
    print("HOT_MAGENTA border. WIDE HIGH ANGLE. Dutch 5 CCW.")
