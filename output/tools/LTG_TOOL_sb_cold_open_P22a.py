#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_sb_cold_open_P22a.py
Cold Open Panel P22a — MCU INSERT — Byte Accidentally Lands on Luma's Shoulder
Diego Vargas, Storyboard Artist — Cycle 48

Beat: Mid-chaos insert. Byte has been at Luma's level since P21 (floated down during
      shared threat). During the monitor-breach chaos of P21-P22, Byte gets KNOCKED onto
      Luma's shoulder. This is NOT chosen — it is a practical accident. He is dodging
      something (pixel debris, a breaching Glitchkin) and his trajectory ends at her shoulder.

      Critical staging note: this is the FIRST TIME Byte's digital nature physically contacts
      Luma's analog world in a non-hostile way. Where he lands, pixel confetti contacts
      her hoodie fabric — the first mark of the digital on the analog. This is visually
      important: tiny cyan pixel artifacts on the LUMA_HOODIE orange.

      Byte's expression: STARTLED + EMBARRASSED. He did NOT want to be here. His body
      language is rigid (caught, not relaxed). He is looking AWAY from Luma (not at her).

      Byte is at Luma's level (approved C48 — Byte stays on CRT through P19-P20,
      floats to Luma's level P21, at her level for P22+).

Camera: MCU. Tight on Luma's right shoulder + Byte. Luma's face visible from chin to
        forehead (3/4 view, looking left toward the chaos). Byte occupies the shoulder
        zone — tiny against her hoodie. This is a character scale comparison shot.

Key staging:
  - Luma: 3/4 view facing camera-left. ALARMED expression (wide eyes, raised brows).
    She is looking at the monitors, NOT at Byte. She hasn't registered him yet.
    LUMA_HOODIE canonical orange fills most of the frame (MCU = hoodie dominant).
    Shoulder line follows shoulder involvement rule: right shoulder slightly raised
    (she is tense, bracing).
  - Byte: perched on Luma's right shoulder. Tiny (body_h ~ 15% of DRAW_H for scale).
    Expression: STARTLED — wide cracked eye, processing dots active, mouth open (small O).
    Body: rigid, arms pulled in (NOT comfortable). Looking camera-RIGHT (away from Luma).
    He is turned slightly away from her neck.
  - Contact zone: where Byte sits on the hoodie, 4-6 tiny ELEC_CYAN pixel artifacts
    bleed into the orange fabric. The digital marks the analog. Annotation calls this out.
  - Background: chaos blur — defocused monitor glow (cyan + magenta wash), pixel confetti
    in the air (depth-of-field blur = larger, softer polygons).
  - Hoodie fabric: shoulder bunching per shoulder involvement rule (arm not raised, but
    tension = slight fabric compression where Byte sits).

Arc: TENSE / COMEDY (HOT_MAGENTA border — chaos context, but this moment is character).
Output: output/storyboards/panels/LTG_SB_cold_open_P22a.png
"""

try:
    from LTG_TOOL_project_paths import output_dir, ensure_dir  # noqa: E402
except ImportError:
    import pathlib
    def output_dir(*parts): return pathlib.Path("/home/wipkat/team/output").joinpath(*parts)
    def ensure_dir(path): path.mkdir(parents=True, exist_ok=True); return path
from PIL import Image, ImageDraw, ImageFont
import math, random, os

PANELS_DIR = output_dir('storyboards', 'panels')
OUTPUT_PATH = os.path.join(PANELS_DIR, "LTG_SB_cold_open_P22a.png")
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
LUMA_HOODIE_DK = (180, 80, 38)
LUMA_SKIN     = (218, 172, 128)
LUMA_SKIN_SH  = (188, 142, 100)
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

RNG = random.Random(22220)


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
    img  = Image.new('RGB', (PW, DRAW_H), DEEP_SPACE)
    draw = ImageDraw.Draw(img)

    # ── Background: defocused chaos blur ─────────────────────────────────────
    # Gradient wash simulating out-of-focus monitor glow
    for row in range(DRAW_H):
        t = row / DRAW_H
        bg_color = lerp_color(
            lerp_color(ELEC_CYAN_DIM, HOT_MAGENTA, t * 0.4),
            DEEP_SPACE, 0.65
        )
        draw.line([(0, row), (PW, row)], fill=bg_color)

    # Defocused confetti (large, soft — depth of field blur)
    for _ in range(14):
        cx_p = RNG.randint(0, PW)
        cy_p = RNG.randint(0, DRAW_H)
        pr = RNG.randint(6, 14)  # larger than in-focus confetti
        sides = RNG.randint(4, 6)
        pc = lerp_color(ELEC_CYAN if RNG.random() > 0.3 else HOT_MAGENTA,
                        DEEP_SPACE, RNG.uniform(0.4, 0.7))
        draw_irregular_poly(draw, cx_p, cy_p, pr, sides, pc, RNG, fill=True)

    # ── Luma — 3/4 view, MCU framing ────────────────────────────────────────
    # MCU: face from chin to forehead, hoodie fills lower 60% of frame
    # Luma positioned center-left, facing camera-left (looking at monitors off-screen)

    # Hoodie mass — fills most of the lower frame
    hoodie_top = int(DRAW_H * 0.38)
    hoodie_pts = [
        (0, DRAW_H),                          # bottom-left
        (0, hoodie_top + 40),                  # left edge
        (int(PW * 0.15), hoodie_top + 10),     # left shoulder zone
        (int(PW * 0.38), hoodie_top - 8),      # neck left
        (int(PW * 0.52), hoodie_top - 14),     # neck center (slightly higher = tense)
        (int(PW * 0.65), hoodie_top - 4),      # right shoulder base
        # RIGHT SHOULDER RAISED — shoulder involvement rule: tense, bracing
        (int(PW * 0.72), hoodie_top - 20),     # right shoulder PEAK (raised 16px)
        (int(PW * 0.82), hoodie_top + 8),      # right shoulder slope down
        (int(PW * 0.92), hoodie_top + 30),     # right arm continuation
        (PW, hoodie_top + 60),                 # right edge
        (PW, DRAW_H),                          # bottom-right
    ]
    draw.polygon(hoodie_pts, fill=LUMA_HOODIE)

    # Hoodie shadow side (left = further from camera light)
    shadow_pts = [
        (0, DRAW_H),
        (0, hoodie_top + 40),
        (int(PW * 0.15), hoodie_top + 10),
        (int(PW * 0.32), hoodie_top),
        (int(PW * 0.32), DRAW_H),
    ]
    draw.polygon(shadow_pts, fill=LUMA_HOODIE_DK)

    # Hoodie fabric lines (texture) — dense for edge detail
    for fy in range(hoodie_top + 8, DRAW_H, 7):
        x_start = RNG.randint(0, int(PW * 0.12))
        x_end = RNG.randint(int(PW * 0.55), PW)
        shade = lerp_color(LUMA_HOODIE, LUMA_HOODIE_DK, RNG.uniform(0.15, 0.4))
        draw.line([(x_start, fy), (x_end, fy + RNG.randint(-4, 4))],
                  fill=shade, width=RNG.choice([1, 1, 2]))
    # Vertical fold lines (fabric drape) — multiple passes
    fold_positions = [int(PW * x) for x in [0.12, 0.22, 0.35, 0.48, 0.58, 0.68]]
    for fx in fold_positions:
        fold_top = hoodie_top + RNG.randint(5, 30)
        fold_bot = min(DRAW_H - 5, fold_top + RNG.randint(60, 160))
        fold_shade = lerp_color(LUMA_HOODIE, LUMA_HOODIE_DK, RNG.uniform(0.2, 0.45))
        draw.line([(fx, fold_top), (fx + RNG.randint(-8, 8), fold_bot)],
                  fill=fold_shade, width=RNG.randint(2, 3))
        # Highlight line next to fold
        draw.line([(fx + 3, fold_top + 4), (fx + RNG.randint(2, 6), fold_bot - 4)],
                  fill=lerp_color(LUMA_HOODIE, WARM_CREAM, 0.15), width=1)
    # Collar / neckline detail
    collar_y = hoodie_top - 2
    draw.arc([int(PW * 0.35), collar_y - 12, int(PW * 0.55), collar_y + 12],
             start=0, end=180, fill=LUMA_HOODIE_DK, width=4)
    # Hoodie seam lines (structural detail)
    draw.line([(int(PW * 0.42), hoodie_top + 5), (int(PW * 0.42), DRAW_H)],
              fill=lerp_color(LUMA_HOODIE, LUMA_HOODIE_DK, 0.3), width=2)
    draw.line([(int(PW * 0.62), hoodie_top + 10), (int(PW * 0.65), DRAW_H)],
              fill=lerp_color(LUMA_HOODIE, LUMA_HOODIE_DK, 0.3), width=2)

    # Hood bunching at right shoulder (fabric compression where Byte sits)
    shoulder_cx = int(PW * 0.72)
    shoulder_cy = hoodie_top - 14
    for i in range(4):
        fx = shoulder_cx + RNG.randint(-12, 12)
        fy = shoulder_cy + RNG.randint(-6, 10)
        fl = RNG.randint(8, 16)
        draw.line([(fx, fy), (fx + RNG.randint(-4, 4), fy + fl)],
                  fill=lerp_color(LUMA_HOODIE, LUMA_HOODIE_DK, 0.35), width=1)

    # ── Luma's head / face — 3/4 view facing camera-left ────────────────────
    head_cx = int(PW * 0.42)
    head_cy = int(DRAW_H * 0.22)
    head_r  = int(DRAW_H * 0.16)

    # Neck
    neck_w = int(head_r * 0.55)
    draw.rectangle([head_cx - neck_w, head_cy + head_r - 6,
                    head_cx + neck_w, hoodie_top + 4],
                   fill=LUMA_SKIN)
    draw.rectangle([head_cx - neck_w, head_cy + head_r - 6,
                    head_cx - neck_w + 6, hoodie_top + 4],
                   fill=LUMA_SKIN_SH)

    # Head
    draw.ellipse([head_cx - head_r, head_cy - head_r,
                  head_cx + head_r, head_cy + head_r],
                 fill=LUMA_SKIN)

    # Hair — messy, upper hemisphere + sides
    hair_pts = []
    for i in range(18):
        angle = math.pi + (math.pi * i / 17)
        hr = head_r + RNG.randint(4, 14)
        hair_pts.append((int(head_cx + hr * math.cos(angle)),
                         int(head_cy + hr * math.sin(angle) - 6)))
    hair_pts.insert(0, (head_cx + head_r + 6, head_cy + 4))
    hair_pts.append((head_cx - head_r - 6, head_cy + 4))
    draw.polygon(hair_pts, fill=LUMA_HAIR)

    # 3/4 face — eyes shifted LEFT (she's looking camera-left at the chaos)
    eye_y = head_cy + 2
    face_offset = -int(head_r * 0.12)  # 3/4 view: features shifted left

    # Left eye (closer to us) — WIDE (alarmed)
    le_cx = head_cx + face_offset - int(head_r * 0.28)
    le_rx, le_ry = int(head_r * 0.22), int(head_r * 0.18)
    draw.ellipse([le_cx - le_rx, eye_y - le_ry, le_cx + le_rx, eye_y + le_ry],
                 fill=(240, 236, 228))
    # Iris shifted LEFT (looking at monitors)
    iris_r = max(3, int(le_rx * 0.5))
    draw.ellipse([le_cx - iris_r - 4, eye_y - iris_r,
                  le_cx + iris_r - 4, eye_y + iris_r],
                 fill=(55, 42, 32))
    # Cyan catch in left eye (monitor glow)
    draw.ellipse([le_cx - iris_r - 2, eye_y - iris_r + 1,
                  le_cx - iris_r + 2, eye_y - iris_r + 4],
                 fill=ELEC_CYAN)

    # Right eye (further, 3/4 foreshortened) — also WIDE
    re_cx = head_cx + face_offset + int(head_r * 0.18)
    re_rx = int(le_rx * 0.75)  # foreshortened
    re_ry = le_ry
    draw.ellipse([re_cx - re_rx, eye_y - re_ry, re_cx + re_rx, eye_y + re_ry],
                 fill=(240, 236, 228))
    iris_r_r = max(2, int(re_rx * 0.5))
    draw.ellipse([re_cx - iris_r_r - 3, eye_y - iris_r_r,
                  re_cx + iris_r_r - 3, eye_y + iris_r_r],
                 fill=(55, 42, 32))

    # Brows — RAISED (alarmed)
    draw.arc([le_cx - le_rx - 2, eye_y - le_ry - 16,
              le_cx + le_rx + 2, eye_y - le_ry],
             start=200, end=340, fill=LUMA_HAIR, width=3)
    draw.arc([re_cx - re_rx - 2, eye_y - re_ry - 14,
              re_cx + re_rx + 2, eye_y - re_ry],
             start=200, end=340, fill=LUMA_HAIR, width=2)

    # Mouth — slightly open (processing alarm)
    mouth_cx = head_cx + face_offset - int(head_r * 0.05)
    mouth_cy = head_cy + int(head_r * 0.42)
    draw.ellipse([mouth_cx - 6, mouth_cy - 3, mouth_cx + 6, mouth_cy + 4],
                 fill=(180, 120, 95))

    # Nose — simple line
    nose_x = head_cx + face_offset - int(head_r * 0.08)
    draw.line([(nose_x, eye_y + 8), (nose_x - 3, head_cy + int(head_r * 0.3))],
              fill=LUMA_SKIN_SH, width=2)

    # Cyan glow wash on Luma's face from monitors
    add_glow(img, head_cx - 30, head_cy, 50, ELEC_CYAN, steps=4, max_alpha=12)
    draw = ImageDraw.Draw(img)

    # ── Byte — perched on Luma's right shoulder ──────────────────────────────
    # Tiny relative to Luma at MCU scale
    byte_cx = shoulder_cx + 2
    byte_cy = shoulder_cy - 28  # sitting ON the shoulder
    byte_hr = 12  # tiny head
    byte_bw = 15
    byte_bh = 22

    # Body — rigid, arms pulled in (NOT comfortable)
    bt_top = byte_cy + byte_hr - 2
    # Inverted teardrop body
    draw.ellipse([byte_cx - byte_bw // 2, bt_top,
                  byte_cx + byte_bw // 2, bt_top + byte_bh // 2],
                 fill=BYTE_TEAL)
    draw.polygon([
        (byte_cx - byte_bw // 2, bt_top + byte_bh // 3),
        (byte_cx + byte_bw // 2, bt_top + byte_bh // 3),
        (byte_cx, bt_top + byte_bh)
    ], fill=BYTE_TEAL)

    # Arms pulled in tight — rigid, not relaxed
    draw.line([(byte_cx - byte_bw // 2, bt_top + 6),
               (byte_cx - byte_bw // 2 + 2, bt_top + 16)],
              fill=BYTE_BODY_DK, width=3)
    draw.line([(byte_cx + byte_bw // 2, bt_top + 6),
               (byte_cx + byte_bw // 2 - 2, bt_top + 16)],
              fill=BYTE_BODY_DK, width=3)

    # Stubby legs dangling on hoodie surface
    draw.line([(byte_cx - 4, bt_top + byte_bh - 2),
               (byte_cx - 5, bt_top + byte_bh + 6)],
              fill=BYTE_TEAL, width=3)
    draw.line([(byte_cx + 4, bt_top + byte_bh - 2),
               (byte_cx + 3, bt_top + byte_bh + 6)],
              fill=BYTE_TEAL, width=3)

    # Head — facing camera-RIGHT (AWAY from Luma)
    draw.ellipse([byte_cx - byte_hr, byte_cy - byte_hr,
                  byte_cx + byte_hr, byte_cy + byte_hr],
                 fill=BYTE_TEAL)

    # Eyes — STARTLED. Looking right (away from Luma).
    # Normal eye (left — closer to Luma, but looking away)
    ne_cx = byte_cx + int(byte_hr * 0.30)
    ne_cy = byte_cy - 1
    ne_r = max(3, int(byte_hr * 0.28))
    draw.ellipse([ne_cx - ne_r, ne_cy - ne_r, ne_cx + ne_r, ne_cy + ne_r],
                 fill=(0, 240, 255))
    # Wide open — startled
    iris_ne = max(2, ne_r // 2)
    draw.ellipse([ne_cx + 1 - iris_ne, ne_cy - iris_ne,
                  ne_cx + 1 + iris_ne, ne_cy + iris_ne],
                 fill=VOID_BLACK)

    # Cracked eye (right side) — processing dots active
    ce_cx = byte_cx - int(byte_hr * 0.30)
    ce_cy = byte_cy - 1
    ce_r = ne_r
    draw.ellipse([ce_cx - ce_r, ce_cy - ce_r, ce_cx + ce_r, ce_cy + ce_r],
                 fill=(0, 200, 220))
    # Crack scar
    draw.line([(ce_cx - ce_r, ce_cy - ce_r + 1),
               (ce_cx + ce_r, ce_cy + ce_r - 1)],
              fill=HOT_MAGENTA, width=1)
    # Processing dots (3 alternating)
    for di, dc in enumerate([ELEC_CYAN, HOT_MAGENTA, ELEC_CYAN]):
        dx = ce_cx - 3 + di * 3
        dy = ce_cy + ce_r + 3
        draw.ellipse([dx - 1, dy - 1, dx + 1, dy + 1], fill=dc)

    # Mouth — small O (startled)
    draw.ellipse([byte_cx - 2, byte_cy + int(byte_hr * 0.4),
                  byte_cx + 2, byte_cy + int(byte_hr * 0.6)],
                 fill=(0, 160, 180))

    # HOT_MAGENTA scar diagonal
    draw.line([(byte_cx + byte_hr - 3, byte_cy - byte_hr + 4),
               (byte_cx - byte_hr + 4, byte_cy + byte_hr - 4)],
              fill=HOT_MAGENTA, width=1)

    # ── Contact zone: pixel artifacts on hoodie ──────────────────────────────
    # Where Byte sits, digital bleeds into analog — ELEC_CYAN pixels on orange hoodie
    contact_y = bt_top + byte_bh + 2
    for i in range(6):
        px = byte_cx + RNG.randint(-10, 10)
        py = contact_y + RNG.randint(0, 12)
        ps = RNG.randint(2, 4)
        sides = RNG.randint(4, 6)
        # Cyan pixels on orange fabric
        draw_irregular_poly(draw, px, py, ps, sides, ELEC_CYAN, RNG, fill=True)

    # Desaturation bleed around Byte's seat
    desat = Image.new('RGBA', img.size, (0, 0, 0, 0))
    dd = ImageDraw.Draw(desat)
    dd.ellipse([byte_cx - 20, contact_y - 4,
                byte_cx + 20, contact_y + 14],
               fill=(180, 200, 210, 15))
    base = img.convert('RGBA')
    img.paste(Image.alpha_composite(base, desat).convert('RGB'))
    draw = ImageDraw.Draw(img)

    # Byte glow
    add_glow(img, byte_cx, byte_cy, 22, ELEC_CYAN, steps=4, max_alpha=18)
    draw = ImageDraw.Draw(img)

    # ── In-focus confetti near Byte (foreground debris) ──────────────────────
    for _ in range(8):
        cx_p = RNG.randint(int(PW * 0.5), int(PW * 0.9))
        cy_p = RNG.randint(0, int(DRAW_H * 0.5))
        pr = RNG.randint(2, 4)
        sides = RNG.randint(4, 7)
        pc = ELEC_CYAN if RNG.random() > 0.3 else HOT_MAGENTA
        draw_irregular_poly(draw, cx_p, cy_p, pr, sides, pc, RNG, fill=True)

    # ── Annotations ──────────────────────────────────────────────────────────
    font_ann   = load_font(9,  bold=False)
    font_ann_b = load_font(9, bold=True)
    font_sm    = load_font(8,  bold=False)

    draw.text((8, 8),
              'MCU INSERT  |  BYTE LANDS ON SHOULDER  |  ACCIDENTAL',
              font=font_ann, fill=ANN_COLOR)

    # Contact zone callout
    draw.text((byte_cx + 24, contact_y + 2),
              "FIRST DIGITAL-ON-ANALOG CONTACT", font=font_ann_b, fill=ANN_CYAN)
    draw.text((byte_cx + 24, contact_y + 14),
              "pixel artifacts bleed into hoodie", font=font_sm, fill=ANN_DIM)

    # Byte expression note
    draw.text((byte_cx - 60, byte_cy - byte_hr - 16),
              "STARTLED — not chosen, accident", font=font_sm, fill=ANN_DIM)

    # Luma gaze direction
    draw.line([(le_cx - le_rx - 4, eye_y),
               (le_cx - le_rx - 30, eye_y - 4)],
              fill=ANN_CYAN, width=1)
    draw.text((le_cx - le_rx - 90, eye_y - 10),
              "looking at monitors", font=font_sm, fill=ANN_DIM)

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
              "P22a  |  MCU INSERT  |  BYTE ON SHOULDER  |  ACCIDENTAL",
              font=font_t1, fill=TEXT_SHOT)

    draw.text((PW - 200, DRAW_H + 5),
              "ARC: TENSE / COMEDY", font=font_t2, fill=HOT_MAGENTA)

    draw.text((10, DRAW_H + 22),
              "Byte knocked onto Luma's shoulder mid-chaos. Not chosen — practical accident.",
              font=font_t3, fill=TEXT_DESC)
    draw.text((10, DRAW_H + 35),
              "First digital-on-analog contact: pixel artifacts bleed into hoodie fabric.",
              font=font_t3, fill=(120, 112, 90))

    draw.text((PW - 278, DRAW_H + 56),
              "LTG_SB_cold_open_P22a  /  Diego Vargas  /  C48",
              font=font_meta, fill=TEXT_META)

    draw.rectangle([0, 0, PW - 1, PH - 1], outline=ARC_COLOR, width=4)

    final.thumbnail((1280, 1280))
    final.save(OUTPUT_PATH, "PNG")
    print(f"Saved: {OUTPUT_PATH}  {final.size}")
    return OUTPUT_PATH


if __name__ == "__main__":
    draw_panel()
    print("P22a standalone panel generation complete.")
    print("Beat: Byte accidentally lands on Luma's shoulder mid-chaos.")
    print("First digital-on-analog contact. HOT_MAGENTA border.")
