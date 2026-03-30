#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_sb_cold_open_P19.py
Cold Open Panel P19 — MED — Byte "Preferred Term Is Glitchkin"
Diego Vargas, Storyboard Artist — Cycle 46

Beat: Byte appears and delivers "The preferred term is 'Glitchkin.'"
      Beat function: comedic puncture of tension. Byte's first direct dialogue to Luma
      after the notebook reveal. He is offended by the doodles AND by whatever name
      Luma has been using in her head. This is a correction, delivered with maximum
      dignity by a six-inch creature hovering in a twelve-year-old's grandmother's den.

      The comedy: Byte is managing information even now. He is not charmed by Luma's
      drawings. He is not flattered. He is correcting the record. His expression is
      OFFENDED + RELUCTANT ACKNOWLEDGMENT — he is annoyed she noticed, but he can't
      deny the accuracy.

Camera: MED or MED WIDE. Byte in frame with Luma reacting.
        Byte camera-left (he is the speaker — dialogue subject gets left position per
        standard board grammar). Luma camera-right, reacting — her expression is
        the response: half-smile, one brow up. Not mocking. Interested.
        Byte is hovering at Luma's sitting head height (she is still on the floor
        or sitting up from the P17 position).
        CRT monitors in BG — faint static glow. Night den ambience.

Key staging:
  - Byte: hovering camera-left, 3/4 toward Luma (camera-right).
    Expression: OFFENDED / DIGNIFIED CORRECTION.
    Normal eye: narrowed (assessment / "I can't believe I have to say this").
    Cracked eye: processing dots (always processing).
    Mouth: open, mid-word. Pixel teeth visible. The mouth is PRECISE — he is
    enunciating "Glitchkin" with maximum clarity.
    Arms: one arm slightly extended outward — a declarative gesture. "Presenting
    the correct information." Not pointing at Luma — presenting to the air.
    Body: inverted teardrop, canonical teal. Slight forward lean (3-4°) toward Luma —
    he is correcting her, not retreating.
  - Luma: camera-right, sitting on floor (cross-legged or legs out from P15/P17).
    Notebook in lap (prop continuity from P18). Pencil in hand.
    Expression: half-smile, one brow up. Intrigued. NOT mocking — she respects
    this creature's dignity even as the moment is funny.
    She is looking AT Byte, not at the notebook. Full attention.
  - Dialogue balloon/annotation: "The preferred term is 'Glitchkin.'"
    Rendered as storyboard dialogue annotation (not a comic balloon — this is
    a pitch board, not a comic).
  - Den environment: warm floor (depth temp: Luma zone warm), cool right/top
    (monitor glow: Byte zone cool). Night ambience.

Arc: CURIOUS / COMEDY (ELEC_CYAN border — the relationship is forming through comedy).

Image size rule: <= 1280px both dimensions.
Output: output/storyboards/panels/LTG_SB_cold_open_P19.png
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
OUTPUT_PATH = os.path.join(PANELS_DIR, "LTG_SB_cold_open_P19.png")
os.makedirs(PANELS_DIR, exist_ok=True)

PW, PH    = 800, 600
CAPTION_H = 72
DRAW_H    = PH - CAPTION_H   # 528

# ── Palette ──────────────────────────────────────────────────────────────────
WARM_CREAM    = (250, 240, 220)
SUNLIT_AMB    = (212, 146, 58)
SUNLIT_DIM    = (180, 120, 50)
VOID_BLACK    = (10, 10, 20)
ELEC_CYAN     = (0, 212, 232)
ELEC_CYAN_DIM = (0, 100, 120)
HOT_MAGENTA   = (232, 0, 152)
LUMA_HOODIE   = (232, 112, 58)   # canonical orange
LUMA_SKIN     = (218, 172, 128)
LUMA_SKIN_SH  = (175, 128, 88)
LUMA_HAIR     = (38, 22, 14)
LUMA_PANTS    = (70, 80, 110)
FLOOR_WARM    = (155, 128, 92)
FLOOR_GRAIN   = (130, 108, 76)
WALL_WARM     = (190, 170, 138)
CRT_BG        = (32, 42, 32)
CRT_STATIC    = (56, 70, 56)
CRT_BEZEL     = (50, 45, 40)
BYTE_TEAL     = (0, 212, 232)
BYTE_DARK     = (8, 40, 50)
DEEP_SPACE    = (6, 4, 14)
DESAT_RING    = (200, 195, 190)
NOTEBOOK_COVER = (85, 75, 120)  # dark purple notebook cover
NOTEBOOK_PAGE  = (248, 244, 232)

# Caption
BG_CAPTION    = (12, 8, 6)
TEXT_SHOT     = (232, 224, 204)
TEXT_DESC     = (155, 148, 122)
TEXT_META     = (88, 82, 66)
ARC_COLOR     = ELEC_CYAN
ANN_COLOR     = (220, 200, 80)
ANN_CYAN      = (0, 180, 210)
ANN_DIM       = (80, 90, 100)
DLG_COLOR     = (245, 240, 225)   # dialogue annotation text

RNG = random.Random(1919)


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
    """Draw a slightly irregular polygon for Glitchkin pixel shapes."""
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
    img  = Image.new('RGB', (PW, PH), WALL_WARM)
    draw = ImageDraw.Draw(img)

    # ── Background: den room — night ambience ────────────────────────────────
    wall_h = int(DRAW_H * 0.38)
    floor_y = wall_h

    # Wall — warm left, cool right (monitor glow)
    for x in range(PW):
        t = x / PW
        c = lerp_color(WALL_WARM, (130, 148, 148), t * 0.50)
        draw.line([(x, 0), (x, wall_h)], fill=c)

    # Floor — warm left (Luma zone), cooler right
    for x in range(PW):
        t = x / PW
        c = lerp_color(FLOOR_WARM, (130, 135, 128), t * 0.30)
        draw.line([(x, floor_y), (x, DRAW_H)], fill=c)

    # Floor planks
    for py in range(floor_y, DRAW_H, 24):
        draw.line([(0, py), (PW, py)], fill=FLOOR_GRAIN, width=1)

    # ── CRT Monitors BG — right zone ────────────────────────────────────────
    mon_specs = [
        (int(PW * 0.62), int(DRAW_H * 0.04), int(PW * 0.22), int(DRAW_H * 0.24)),
        (int(PW * 0.86), int(DRAW_H * 0.07), int(PW * 0.12), int(DRAW_H * 0.20)),
    ]
    for mx, my, mw, mh in mon_specs:
        draw.rectangle([mx, my, mx + mw, my + mh], fill=CRT_BEZEL)
        sp = 6
        draw.rectangle([mx + sp, my + sp, mx + mw - sp, my + mh - sp], fill=CRT_BG)
        for _ in range(50):
            sx = RNG.randint(mx + sp + 2, mx + mw - sp - 2)
            sy = RNG.randint(my + sp + 2, my + mh - sp - 2)
            draw.point((sx, sy), fill=CRT_STATIC)

    # Warm lamp glow camera-left
    add_glow(img, -20, int(DRAW_H * 0.20), int(PW * 0.50),
             SUNLIT_AMB, steps=10, max_alpha=16)
    draw = ImageDraw.Draw(img)

    # ── BYTE — camera-left, hovering, OFFENDED / DIGNIFIED CORRECTION ────────
    byte_cx = int(PW * 0.28)
    byte_cy = int(DRAW_H * 0.40)   # hovering at seated Luma's head height

    # Body — inverted teardrop
    body_h = int(DRAW_H * 0.28)
    body_w = int(body_h * 0.72)
    body_top_y = byte_cy - body_h // 2

    # Slight forward lean toward Luma (3-4°)
    lean_offset = int(body_h * 0.04)

    # Teardrop: ellipse upper half + triangle lower half
    draw.ellipse([byte_cx - body_w // 2 + lean_offset, body_top_y,
                  byte_cx + body_w // 2 + lean_offset, byte_cy + body_h // 4],
                 fill=BYTE_TEAL)
    draw.polygon([
        (byte_cx - body_w // 2 + lean_offset, byte_cy + body_h // 8),
        (byte_cx + lean_offset, byte_cy + body_h // 2),
        (byte_cx + body_w // 2 + lean_offset, byte_cy + body_h // 8),
    ], fill=BYTE_TEAL)

    # Body shadow/dark side (left — away from Luma)
    draw.ellipse([byte_cx - body_w // 2 + lean_offset, body_top_y,
                  byte_cx + lean_offset, byte_cy + body_h // 4],
                 fill=BYTE_DARK)

    # ── Byte face: 3/4 toward Luma — OFFENDED / DIGNIFIED CORRECTION ────────
    face_cx = byte_cx + int(body_w * 0.10) + lean_offset  # face shifted toward Luma
    face_cy = body_top_y + int(body_h * 0.25)
    face_r  = int(body_w * 0.45)

    draw.ellipse([face_cx - face_r, face_cy - face_r,
                  face_cx + face_r, face_cy + face_r],
                 fill=BYTE_TEAL)

    # Normal eye (right eye — toward Luma, camera-right side of face at 3/4)
    # NARROWED (assessment / "I can't believe I have to say this")
    ne_cx = face_cx + int(face_r * 0.30)
    ne_cy = face_cy - int(face_r * 0.18)
    ne_r  = int(face_r * 0.28)

    # Narrow eye: reduced vertical opening
    ne_rh = int(ne_r * 0.55)  # narrowed height
    draw.ellipse([ne_cx - ne_r, ne_cy - ne_rh, ne_cx + ne_r, ne_cy + ne_rh],
                 fill=(8, 8, 18))
    # Iris
    DEEP_CYAN = (0, 155, 175)
    draw.ellipse([ne_cx - ne_r + 3, ne_cy - ne_rh + 2,
                  ne_cx + ne_r - 3, ne_cy + ne_rh - 2],
                 fill=DEEP_CYAN)
    # Pupil — aimed at Luma (right shift)
    iris_shift = int(ne_r * 0.25)
    draw.ellipse([ne_cx + iris_shift - 4, ne_cy - 4,
                  ne_cx + iris_shift + 4, ne_cy + 4],
                 fill=VOID_BLACK)
    # Top lid line (narrowed — the annoyance)
    draw.arc([ne_cx - ne_r - 2, ne_cy - ne_rh - 3,
              ne_cx + ne_r + 2, ne_cy + ne_rh + 3],
             start=200, end=340, fill=VOID_BLACK, width=2)

    # Cracked eye (left eye — facing outward at 3/4)
    ce_cx = face_cx - int(face_r * 0.28)
    ce_cy = face_cy - int(face_r * 0.18)
    ce_r  = int(face_r * 0.26)
    draw.ellipse([ce_cx - ce_r, ce_cy - ce_r, ce_cx + ce_r, ce_cy + ce_r],
                 fill=(8, 8, 18))
    # Crack lines
    for crack_ang in [30, 70, 120, 160]:
        ca = math.radians(crack_ang)
        draw.line([(int(ce_cx + ce_r * 0.2 * math.cos(ca)),
                    int(ce_cy + ce_r * 0.2 * math.sin(ca))),
                   (int(ce_cx + ce_r * 0.9 * math.cos(ca)),
                    int(ce_cy + ce_r * 0.9 * math.sin(ca)))],
                  fill=HOT_MAGENTA, width=1)
    # Processing dots (outward divergence per Lee Tanaka)
    div_x = -int(ce_r * 0.20)
    for di, dc in enumerate([ELEC_CYAN, HOT_MAGENTA, ELEC_CYAN]):
        draw.ellipse([ce_cx + div_x - 2 + di * 5, ce_cy - 2,
                      ce_cx + div_x + 2 + di * 5, ce_cy + 2],
                     fill=dc)

    # Mouth — OPEN, mid-word, enunciating "Glitchkin"
    # Wider opening than neutral. Pixel teeth visible.
    mouth_y = face_cy + int(face_r * 0.38)
    mouth_w = int(face_r * 0.55)
    mouth_h = int(face_r * 0.28)  # open mouth
    # Mouth opening
    draw.rectangle([face_cx - mouth_w, mouth_y - mouth_h // 2,
                    face_cx + mouth_w, mouth_y + mouth_h // 2],
                   fill=VOID_BLACK)
    # Pixel teeth — top row
    for mx_tooth in range(face_cx - mouth_w + 3, face_cx + mouth_w - 3, 6):
        draw.rectangle([mx_tooth, mouth_y - mouth_h // 2,
                        mx_tooth + 4, mouth_y - mouth_h // 2 + 4],
                       fill=(210, 210, 220))
    # Pixel teeth — bottom row
    for mx_tooth in range(face_cx - mouth_w + 5, face_cx + mouth_w - 5, 6):
        draw.rectangle([mx_tooth, mouth_y + mouth_h // 2 - 4,
                        mx_tooth + 4, mouth_y + mouth_h // 2],
                       fill=(195, 195, 205))

    # Brow — narrowed, one side higher (offended expression asymmetry)
    # Left brow (outward side) slightly raised (indignation)
    draw.line([(face_cx - int(face_r * 0.55), face_cy - int(face_r * 0.48)),
               (face_cx - int(face_r * 0.10), face_cy - int(face_r * 0.40))],
              fill=VOID_BLACK, width=2)
    # Right brow (Luma side) lower/flatter (the assessment)
    draw.line([(face_cx + int(face_r * 0.10), face_cy - int(face_r * 0.38)),
               (face_cx + int(face_r * 0.50), face_cy - int(face_r * 0.35))],
              fill=VOID_BLACK, width=2)

    # HOT_MAGENTA scar diagonal
    scar_len = int(face_r * 0.7)
    scar_cx  = face_cx - int(face_r * 0.05)
    scar_cy  = face_cy + int(face_r * 0.05)
    draw.line([(scar_cx - scar_len // 2, scar_cy - scar_len // 3),
               (scar_cx + scar_len // 2, scar_cy + scar_len // 3)],
              fill=HOT_MAGENTA, width=2)

    # Arms — right arm (camera-right, toward Luma) extended in declarative gesture
    arm_top_y = body_top_y + int(body_h * 0.35)
    # Right arm — extended outward, presenting (declarative)
    arm_r_shoulder = (byte_cx + body_w // 2 + 6 + lean_offset, arm_top_y)
    arm_r_tip      = (byte_cx + body_w // 2 + 42 + lean_offset,
                      arm_top_y - int(body_h * 0.08))
    draw.line([arm_r_shoulder, arm_r_tip], fill=BYTE_TEAL, width=10)
    # Hand at end of extended arm (small square — Glitchkin hand)
    draw.rectangle([arm_r_tip[0] - 6, arm_r_tip[1] - 6,
                    arm_r_tip[0] + 6, arm_r_tip[1] + 6],
                   fill=BYTE_TEAL)

    # Left arm — at side, neutral
    arm_l_shoulder = (byte_cx - body_w // 2 - 6 + lean_offset, arm_top_y)
    arm_l_bot      = (byte_cx - body_w // 2 - 6 + lean_offset,
                      arm_top_y + int(body_h * 0.22))
    draw.line([arm_l_shoulder, arm_l_bot], fill=BYTE_TEAL, width=10)

    # Legs — feet in air (hovering)
    leg_top_y = byte_cy + int(body_h * 0.35)
    leg_bot_y = leg_top_y + int(body_h * 0.20)
    draw.rectangle([byte_cx - 14 + lean_offset, leg_top_y,
                    byte_cx - 4 + lean_offset, leg_bot_y],
                   fill=BYTE_TEAL)
    draw.rectangle([byte_cx + 4 + lean_offset, leg_top_y,
                    byte_cx + 14 + lean_offset, leg_bot_y],
                   fill=BYTE_TEAL)

    # Desaturation ring on floor below Byte
    desat_floor_y = floor_y + int((DRAW_H - floor_y) * 0.85)
    draw.ellipse([byte_cx - 32, desat_floor_y - 8,
                  byte_cx + 32, desat_floor_y + 8],
                 outline=DESAT_RING, width=2)

    # Byte glow
    add_glow(img, byte_cx + lean_offset, byte_cy, int(body_w * 2.0),
             ELEC_CYAN, steps=8, max_alpha=20)
    draw = ImageDraw.Draw(img)

    # ── LUMA — camera-right, sitting on floor, reacting ──────────────────────
    luma_floor_y = floor_y + int((DRAW_H - floor_y) * 0.82)
    luma_cx      = int(PW * 0.70)

    # Cross-legged base
    leg_w = 62
    leg_h = 26
    draw.polygon([
        (luma_cx - leg_w, luma_floor_y),
        (luma_cx, luma_floor_y - 6),
        (luma_cx + leg_w, luma_floor_y),
        (luma_cx + leg_w // 2, luma_floor_y + leg_h),
        (luma_cx - leg_w // 2, luma_floor_y + leg_h),
    ], fill=LUMA_PANTS)

    # Shoes
    draw.ellipse([luma_cx - leg_w - 10, luma_floor_y - 5,
                  luma_cx - leg_w + 10, luma_floor_y + 7],
                 fill=(42, 36, 30))
    draw.ellipse([luma_cx + leg_w - 10, luma_floor_y - 5,
                  luma_cx + leg_w + 10, luma_floor_y + 7],
                 fill=(42, 36, 30))

    # Hoodie torso — CANONICAL ORANGE
    torso_top = luma_floor_y - 86
    torso_w   = 48
    draw.rectangle([luma_cx - torso_w, torso_top,
                    luma_cx + torso_w, luma_floor_y + 2],
                   fill=LUMA_HOODIE)

    # Notebook in lap (prop continuity from P18)
    nb_left  = luma_cx - 30
    nb_top   = luma_floor_y - 32
    nb_right = luma_cx + 35
    nb_bot   = luma_floor_y - 2
    draw.rectangle([nb_left, nb_top, nb_right, nb_bot], fill=NOTEBOOK_COVER)
    # Pages visible (open notebook)
    draw.rectangle([nb_left + 3, nb_top + 2, nb_right - 3, nb_bot - 2],
                   fill=NOTEBOOK_PAGE)
    # Tiny doodle marks on the open page (callback to P18)
    for _ in range(6):
        dx = RNG.randint(nb_left + 6, nb_right - 6)
        dy = RNG.randint(nb_top + 5, nb_bot - 5)
        draw.ellipse([dx - 1, dy - 1, dx + 1, dy + 1], fill=(120, 110, 95))

    # Left arm — resting on notebook, pencil in hand
    draw.line([(luma_cx - torso_w + 6, torso_top + 38),
               (luma_cx - 10, luma_floor_y - 22)],
              fill=LUMA_HOODIE, width=20)
    # Hand on notebook
    draw.ellipse([luma_cx - 16, luma_floor_y - 28,
                  luma_cx + 4, luma_floor_y - 16],
                 fill=LUMA_SKIN)
    # Pencil in hand
    draw.line([(luma_cx - 6, luma_floor_y - 26),
               (luma_cx + 18, luma_floor_y - 36)],
              fill=(220, 195, 50), width=3)

    # Right arm — resting on right knee
    draw.line([(luma_cx + torso_w - 6, torso_top + 38),
               (luma_cx + leg_w - 8, luma_floor_y - 6)],
              fill=LUMA_HOODIE, width=20)

    # Head
    head_cy = torso_top - 30
    head_r  = 28
    draw.ellipse([luma_cx - head_r, head_cy - head_r,
                  luma_cx + head_r, head_cy + head_r],
                 fill=LUMA_SKIN)

    # Face — 3/4 toward Byte (camera-left)
    # Expression: half-smile, one brow up. Intrigued, not mocking.

    # Left eye (toward Byte — visible eye at 3/4)
    eye_l_cx = luma_cx - 8
    eye_l_cy = head_cy + 4
    eye_lw   = 11
    eye_lh   = 7
    draw.ellipse([eye_l_cx - eye_lw, eye_l_cy - eye_lh,
                  eye_l_cx + eye_lw, eye_l_cy + eye_lh],
                 fill=(240, 232, 222))
    # Iris — tracking Byte
    draw.ellipse([eye_l_cx - 8, eye_l_cy - 5, eye_l_cx + 2, eye_l_cy + 5],
                 fill=(60, 38, 20))
    draw.ellipse([eye_l_cx - 6, eye_l_cy - 3, eye_l_cx, eye_l_cy + 3],
                 fill=VOID_BLACK)
    # Eyelid
    draw.arc([eye_l_cx - eye_lw - 2, eye_l_cy - eye_lh - 2,
              eye_l_cx + eye_lw + 2, eye_l_cy + eye_lh + 2],
             start=210, end=330, fill=(40, 20, 8), width=2)

    # Right eye (partially visible at 3/4)
    eye_r_cx = luma_cx + 6
    eye_r_cy = head_cy + 4
    draw.ellipse([eye_r_cx - 7, eye_r_cy - 5, eye_r_cx + 7, eye_r_cy + 5],
                 fill=(240, 232, 222))
    draw.ellipse([eye_r_cx - 2, eye_r_cy - 3, eye_r_cx + 2, eye_r_cy + 3],
                 fill=(60, 38, 20))

    # Brows — one up (left, toward Byte — intrigued), one level
    # Left brow RAISED (the interested one)
    draw.line([(luma_cx - head_r + 4, head_cy - 18),
               (luma_cx - 2, head_cy - 16)],
              fill=(42, 22, 10), width=3)
    # Right brow level (neutral)
    draw.line([(luma_cx + 4, head_cy - 13),
               (luma_cx + head_r - 6, head_cy - 12)],
              fill=(42, 22, 10), width=3)

    # Mouth — half-smile (asymmetric: left corner up)
    draw.arc([luma_cx - 12, head_cy + 10, luma_cx + 8, head_cy + 22],
             start=200, end=360, fill=(120, 72, 44), width=2)
    # Left corner lift (the half-smile)
    draw.arc([luma_cx - 14, head_cy + 8, luma_cx - 4, head_cy + 18],
             start=240, end=320, fill=(120, 72, 44), width=2)

    # Hair — wild natural cloud
    hair_r = head_r + 16
    for ha in range(0, 360, 18):
        angle = math.radians(ha)
        hvar  = RNG.randint(0, 14)
        hx    = int(luma_cx + (hair_r + hvar) * math.cos(angle))
        hy    = int(head_cy + (hair_r + hvar) * math.sin(angle))
        if hy < head_cy + 12:
            draw.line([(luma_cx + int(head_r * 0.7 * math.cos(angle)),
                        head_cy + int(head_r * 0.7 * math.sin(angle))),
                       (hx, hy)], fill=LUMA_HAIR, width=RNG.choice([2, 3, 4]))

    # Cyan glow from Byte on Luma's face (faint)
    add_glow(img, luma_cx - head_r, head_cy, int(head_r * 1.8),
             ELEC_CYAN, steps=4, max_alpha=10)
    draw = ImageDraw.Draw(img)

    # ── Pixel confetti (light scatter — residual from earlier chaos) ─────────
    for _ in range(12):
        cx_conf = RNG.randint(int(PW * 0.15), int(PW * 0.55))
        cy_conf = RNG.randint(int(DRAW_H * 0.15), int(DRAW_H * 0.80))
        sides   = RNG.randint(4, 7)
        conf_r  = RNG.randint(2, 5)
        conf_c  = RNG.choice([ELEC_CYAN, HOT_MAGENTA, ELEC_CYAN_DIM])
        draw_irregular_poly(draw, cx_conf, cy_conf, conf_r, sides, conf_c, RNG)

    # ── Dialogue annotation ──────────────────────────────────────────────────
    font_dlg   = load_font(14, bold=True)
    font_dlg_s = load_font(11, bold=False)

    # Dialogue text — storyboard annotation style (line from Byte, not comic balloon)
    dlg_x = int(PW * 0.08)
    dlg_y = int(DRAW_H * 0.08)

    # Dialogue box background (semi-transparent dark strip)
    dlg_bg_left  = dlg_x - 6
    dlg_bg_top   = dlg_y - 4
    dlg_bg_right = dlg_x + 380
    dlg_bg_bot   = dlg_y + 40

    # Draw a dark strip behind dialogue text for legibility
    dlg_overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    dlg_d = ImageDraw.Draw(dlg_overlay)
    dlg_d.rectangle([dlg_bg_left, dlg_bg_top, dlg_bg_right, dlg_bg_bot],
                    fill=(10, 8, 6, 160))
    img.paste(Image.alpha_composite(img.convert('RGBA'), dlg_overlay).convert('RGB'))
    draw = ImageDraw.Draw(img)

    # Byte's line
    draw.text((dlg_x, dlg_y),
              'BYTE: "The preferred term is \'Glitchkin.\'"',
              font=font_dlg, fill=DLG_COLOR)
    draw.text((dlg_x, dlg_y + 20),
              "(offended dignity / correcting the record)",
              font=font_dlg_s, fill=ANN_DIM)

    # Dialogue leader line from text to Byte
    draw.line([(dlg_bg_left + 30, dlg_bg_bot),
               (byte_cx + lean_offset + int(face_r * 0.5), face_cy - face_r - 4)],
              fill=DLG_COLOR, width=1)

    # ── Annotations ──────────────────────────────────────────────────────────
    font_ann   = load_font(9,  bold=False)
    font_ann_b = load_font(9,  bold=True)
    font_sm    = load_font(8,  bold=False)

    # Camera note
    draw.text((PW - 320, DRAW_H - 14),
              'MED  |  4-5FT  |  COMEDIC PUNCTURE  |  FIRST DIALOGUE',
              font=font_ann, fill=ANN_COLOR)

    # Byte expression annotation
    draw.text((byte_cx + body_w // 2 + lean_offset + 14, face_cy - 8),
              "OFFENDED", font=font_ann_b, fill=ANN_CYAN)
    draw.text((byte_cx + body_w // 2 + lean_offset + 14, face_cy + 4),
              "(dignified correction)", font=font_sm, fill=ANN_DIM)

    # Luma expression annotation
    draw.text((luma_cx + head_r + 6, head_cy - 14),
              "INTRIGUED", font=font_ann_b, fill=ANN_COLOR)
    draw.text((luma_cx + head_r + 6, head_cy - 2),
              "(half-smile, one brow up)", font=font_sm, fill=(130, 120, 100))

    # Arm gesture annotation
    draw.text((arm_r_tip[0] + 8, arm_r_tip[1] - 10),
              "DECLARATIVE", font=font_sm, fill=ANN_CYAN)
    draw.text((arm_r_tip[0] + 8, arm_r_tip[1]),
              "(presenting, not pointing)", font=font_sm, fill=ANN_DIM)

    # Notebook annotation
    draw.text((nb_left - 4, nb_bot + 4),
              "notebook (from P18)", font=font_sm, fill=(130, 120, 100))

    # Depth temp annotation
    draw.text((int(PW * 0.58), DRAW_H - 14),
              "WARM (Luma zone)", font=font_sm, fill=(180, 130, 60))
    draw.text((int(PW * 0.08), DRAW_H - 14),
              "COOL (Byte zone)", font=font_sm, fill=ELEC_CYAN_DIM)

    # ── Three-tier caption bar ────────────────────────────────────────────────
    font_t1   = load_font(13, bold=True)
    font_t2   = load_font(11, bold=False)
    font_t3   = load_font(9,  bold=False)
    font_meta = load_font(8,  bold=False)

    draw.rectangle([0, DRAW_H, PW, PH], fill=BG_CAPTION)
    draw.line([0, DRAW_H, PW, DRAW_H], fill=(8, 6, 4), width=2)

    # Tier 1 — Shot code
    draw.text((10, DRAW_H + 4),
              'P19  |  MED  |  "PREFERRED TERM IS GLITCHKIN"  |  COMEDY BEAT',
              font=font_t1, fill=TEXT_SHOT)

    # Tier 2 — Arc label
    draw.text((PW - 210, DRAW_H + 5),
              "ARC: CURIOUS / COMEDY", font=font_t2, fill=ELEC_CYAN)

    # Tier 3 — Narrative description
    draw.text((10, DRAW_H + 22),
              "Byte delivers first direct dialogue. Offended by Luma's doodles AND her terminology.",
              font=font_t3, fill=TEXT_DESC)
    draw.text((10, DRAW_H + 35),
              "Luma reacts with intrigued half-smile. The working relationship begins through comedy.",
              font=font_t3, fill=(120, 112, 90))

    # Metadata
    draw.text((PW - 276, DRAW_H + 56),
              "LTG_SB_cold_open_P19  /  Diego Vargas  /  C46",
              font=font_meta, fill=TEXT_META)

    # Arc border — ELEC_CYAN (CURIOUS / COMEDY)
    draw.rectangle([0, 0, PW - 1, PH - 1], outline=ARC_COLOR, width=4)

    img.thumbnail((1280, 1280))
    img.save(OUTPUT_PATH, "PNG")
    print(f"Saved: {OUTPUT_PATH}  {img.size}")
    return OUTPUT_PATH


if __name__ == "__main__":
    draw_panel()
    print("P19 standalone panel generation complete.")
    print('Beat: Byte delivers "The preferred term is Glitchkin." Comedic puncture.')
    print("Byte offended + dignified. Luma intrigued half-smile. First direct dialogue.")
    print("ELEC_CYAN border. MED two-shot: Byte camera-left, Luma camera-right.")
