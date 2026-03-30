#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_sb_cold_open_P17.py
Cold Open Panel P17 — MED — Beat of Stillness / The Chip Falls
Diego Vargas, Storyboard Artist — Cycle 46

Beat: After the chaos of P14 (ricochet), P15 (floor), P16 (ECU face), we land here:
      Luma is sitting up cross-legged in the center of the den. Byte hovers across
      the room from her. Pixel trails from his ricochet are fading (final wisps only).
      Everything has stopped. This is the FIRST QUIET — the full-stop beat before
      they actually acknowledge each other.

      Then: a single pixel chip — one small square of ELEC_CYAN — falls from mid-air
      (residue from Byte's breach) and lands on the floor between them. The sound of
      it (annotated: "soft tick") is the only thing that moves.

      This is a character beat, not an action beat. The composition does the work:
      two figures, one room, a lot of space between them, and one tiny falling chip.

Camera: MED, camera at 4-5ft height, flat horizon (no Dutch tilt — world is stable now,
        chaos has passed). Two-shot: Luma camera-left, Byte camera-right. Balanced.
        They are NOT close — at least 40% of the frame is empty floor between them.

Key staging:
  - Luma: sitting up, cross-legged, center-left. Hoodie LUMA_HOODIE orange.
    Arms loose in lap — no defensive posture. She's moved past fear, into processing.
    Face: 3/4 toward Byte (camera-right). Expression: ASSESSING (still, neutral,
    watching — not afraid, not friendly yet).
  - Byte: hovering camera-right, feet ~18" above floor. Pixel trails fading as
    soft ghost wisps behind him (from ricochet arc). No tilt — he has stopped.
    Face: 3/4 toward Luma (camera-left). Expression: STILL (mirror of Luma's stillness).
    Arms at sides — not extended, not defensive. Just hovering, watching.
  - Falling chip: one 6×6px ELEC_CYAN square, annotated with dotted descent line
    and "soft tick" text. It is BETWEEN them in the composition.
  - Desaturation ring under Byte's hovering position (floor contact zone).
  - BG: monitors behind Byte — returning to normal CRT static (gray-green).
    Den warm in BG behind Luma. The room is re-settling.

Depth temperature: Luma zone = warm (SUNLIT_AMB glow from lamp-left of frame).
                  Byte zone = cool (ELEC_CYAN ambient from monitors behind him).
                  This is exactly the warm/cool depth temperature rule: FG warm, BG cool.
                  Luma camera-left with warm BG; Byte camera-right with cool BG.

Arc: CURIOUS / FIRST ENCOUNTER (ELEC_CYAN border — this beat is the turning point.
     The chip is an object of mutual focus. It cracks the standoff.)

Image size rule: <= 1280px both dimensions.
Output: output/storyboards/panels/LTG_SB_cold_open_P17.png
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
OUTPUT_PATH = os.path.join(PANELS_DIR, "LTG_SB_cold_open_P17.png")
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
ELEC_CYAN_FD  = (0, 60, 80)   # faded cyan for ghost trails
HOT_MAGENTA   = (232, 0, 152)
LUMA_HOODIE   = (232, 112, 58)   # canonical orange
LUMA_SKIN     = (218, 172, 128)
LUMA_SKIN_SH  = (175, 128, 88)
LUMA_HAIR     = (38, 22, 14)
LUMA_PANTS    = (70, 80, 110)
FLOOR_WARM    = (155, 128, 92)
FLOOR_GRAIN   = (130, 108, 76)
WALL_WARM     = (190, 170, 138)
CRT_BG        = (32, 42, 32)      # CRT screen — dim gray-green static
CRT_STATIC    = (56, 70, 56)      # brighter static pixels
CRT_BEZEL     = (50, 45, 40)
BYTE_TEAL     = (0, 212, 232)     # ELEC_CYAN — Byte's body
BYTE_DARK     = (8, 40, 50)       # Byte body shadow
DEEP_SPACE    = (6, 4, 14)
DESAT_RING    = (200, 195, 190)   # desaturation ring (floor under Byte)

# Caption
BG_CAPTION    = (12, 8, 6)
TEXT_SHOT     = (232, 224, 204)
TEXT_DESC     = (155, 148, 122)
TEXT_META     = (88, 82, 66)
ARC_COLOR     = ELEC_CYAN
ANN_COLOR     = (220, 200, 80)
ANN_CYAN      = (0, 180, 210)
ANN_DIM       = (80, 90, 100)

RNG = random.Random(1717)


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
    """Draw a slightly irregular polygon (not rectangle) for Glitchkin pixels."""
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

    # ── Background: den room — restoring to calm ──────────────────────────────
    wall_h = int(DRAW_H * 0.38)   # top 38% wall; floor below
    floor_y = wall_h

    # Wall — warm left (Luma's zone), cool right (Byte's zone, monitor glow)
    for x in range(PW):
        t = x / PW
        c = lerp_color(WALL_WARM, (130, 148, 148), t * 0.55)
        draw.line([(x, 0), (x, wall_h)], fill=c)

    # Floor — warm on left, slight cool tint on right (depth temperature rule)
    for x in range(PW):
        t = x / PW
        c = lerp_color(FLOOR_WARM, (130, 135, 128), t * 0.35)
        draw.line([(x, floor_y), (x, DRAW_H)], fill=c)

    # Floor planks
    for py in range(floor_y, DRAW_H, 24):
        draw.line([(0, py), (PW, py)], fill=FLOOR_GRAIN, width=1)

    # ── CRT Monitors BG — right zone, behind Byte ─────────────────────────────
    # Monitors returning to normal static (breach is over)
    mon_specs = [
        (int(PW * 0.60), int(DRAW_H * 0.05), int(PW * 0.24), int(DRAW_H * 0.26)),
        (int(PW * 0.86), int(DRAW_H * 0.08), int(PW * 0.12), int(DRAW_H * 0.22)),
    ]
    for mx, my, mw, mh in mon_specs:
        # Bezel
        draw.rectangle([mx, my, mx + mw, my + mh], fill=CRT_BEZEL)
        # Screen — dim gray-green static (normal CRT)
        screen_pad = 6
        draw.rectangle([mx + screen_pad, my + screen_pad,
                         mx + mw - screen_pad, my + mh - screen_pad],
                        fill=CRT_BG)
        # Scattered static pixels
        for _ in range(60):
            sx = RNG.randint(mx + screen_pad + 2, mx + mw - screen_pad - 2)
            sy = RNG.randint(my + screen_pad + 2, my + mh - screen_pad - 2)
            draw.point((sx, sy), fill=CRT_STATIC)

    # Warm lamp glow from camera-left (den lamp — Luma's zone)
    add_glow(img, -20, int(DRAW_H * 0.20), int(PW * 0.55),
             SUNLIT_AMB, steps=10, max_alpha=18)
    draw = ImageDraw.Draw(img)

    # ── LUMA — sitting cross-legged, camera-left ──────────────────────────────
    luma_floor_y = floor_y + int((DRAW_H - floor_y) * 0.82)
    luma_cx      = int(PW * 0.24)   # center of her body

    # Cross-legged base (legs folded)
    # Legs form a wide diamond/triangle shape on the floor
    leg_w = 68   # total leg spread
    leg_h = 28
    draw.polygon([
        (luma_cx - leg_w, luma_floor_y),           # left knee
        (luma_cx, luma_floor_y - 8),               # center rise (not flat)
        (luma_cx + leg_w, luma_floor_y),            # right knee
        (luma_cx + leg_w // 2, luma_floor_y + leg_h),  # right shin
        (luma_cx - leg_w // 2, luma_floor_y + leg_h),  # left shin
    ], fill=LUMA_PANTS)

    # Shoes (tips of feet poking out)
    draw.ellipse([luma_cx - leg_w - 12, luma_floor_y - 6,
                  luma_cx - leg_w + 12, luma_floor_y + 8],
                 fill=(42, 36, 30))
    draw.ellipse([luma_cx + leg_w - 12, luma_floor_y - 6,
                  luma_cx + leg_w + 12, luma_floor_y + 8],
                 fill=(42, 36, 30))

    # Hoodie torso — CANONICAL ORANGE
    torso_top = luma_floor_y - 90
    torso_w   = 52
    draw.rectangle([luma_cx - torso_w, torso_top, luma_cx + torso_w, luma_floor_y + 4],
                   fill=LUMA_HOODIE)

    # Arms in lap — relaxed, not defensive
    # Left arm crossing to right lap
    draw.line([(luma_cx - torso_w + 8, torso_top + 40),
               (luma_cx + 20, luma_floor_y - 18)],
              fill=LUMA_HOODIE, width=22)
    # Right arm resting on right leg
    draw.line([(luma_cx + torso_w - 8, torso_top + 40),
               (luma_cx + leg_w - 10, luma_floor_y - 8)],
              fill=LUMA_HOODIE, width=22)

    # Head
    head_cy = torso_top - 32
    head_r  = 30
    draw.ellipse([luma_cx - head_r, head_cy - head_r,
                  luma_cx + head_r, head_cy + head_r],
                 fill=LUMA_SKIN)

    # Face — 3/4 toward camera-right (toward Byte)
    # Expression: ASSESSING — level, neutral. No fear, no friendliness.
    # Right eye (facing Byte direction) — the visible eye at 3/4
    eye_r_cx = luma_cx + 10
    eye_r_cy = head_cy + 4
    eye_rw   = 12
    eye_rh   = 7
    # White
    draw.ellipse([eye_r_cx - eye_rw, eye_r_cy - eye_rh,
                  eye_r_cx + eye_rw, eye_r_cy + eye_rh],
                 fill=(240, 232, 222))
    # Iris — level, tracking Byte direction
    draw.ellipse([eye_r_cx, eye_r_cy - 5, eye_r_cx + 10, eye_r_cy + 5],
                 fill=(60, 38, 20))
    draw.ellipse([eye_r_cx + 2, eye_r_cy - 3, eye_r_cx + 8, eye_r_cy + 3],
                 fill=VOID_BLACK)
    # Eyelid top (standard open)
    draw.arc([eye_r_cx - eye_rw - 2, eye_r_cy - eye_rh - 2,
              eye_r_cx + eye_rw + 2, eye_r_cy + eye_rh + 2],
             start=210, end=330, fill=(40, 20, 8), width=2)

    # Left eye (partially visible at 3/4)
    eye_l_cx = luma_cx - 4
    eye_l_cy = head_cy + 4
    draw.ellipse([eye_l_cx - 8, eye_l_cy - 5, eye_l_cx + 8, eye_l_cy + 5],
                 fill=(240, 232, 222))
    draw.ellipse([eye_l_cx - 3, eye_l_cy - 3, eye_l_cx + 3, eye_l_cy + 3],
                 fill=(60, 38, 20))

    # Brow — level / slightly set (ASSESSING — no surprise, no fear)
    draw.line([(luma_cx - head_r + 6, head_cy - 14),
               (luma_cx + head_r - 8, head_cy - 12)],
              fill=(42, 22, 10), width=3)

    # Mouth — closed, neutral (slight asymmetry — one corner thinking)
    draw.arc([luma_cx - 10, head_cy + 10, luma_cx + 10, head_cy + 22],
             start=190, end=350, fill=(120, 72, 44), width=2)

    # Hair — wild natural cloud
    hair_r = head_r + 18
    for ha in range(0, 360, 20):
        angle = math.radians(ha)
        hvar  = RNG.randint(0, 16)
        hx    = int(luma_cx + (hair_r + hvar) * math.cos(angle))
        hy    = int(head_cy + (hair_r + hvar) * math.sin(angle))
        if hy < head_cy + 14:   # only draw hair above bottom of face
            draw.line([(luma_cx + int(head_r * 0.7 * math.cos(angle)),
                        head_cy + int(head_r * 0.7 * math.sin(angle))),
                       (hx, hy)], fill=LUMA_HAIR, width=RNG.choice([2, 3, 4]))

    # ── BYTE — hovering camera-right, still ──────────────────────────────────
    byte_cx = int(PW * 0.76)
    byte_cy = int(DRAW_H * 0.52)   # hovering — feet well off floor

    # Pixel trails — fading ghost wisps from ricochet arc (only wisps remain)
    # Arc traces from upper-right (where he bounced) curving down to current position
    for t_step in range(4):
        t    = t_step / 5.0
        ghost_x = int(byte_cx + (1 - t) * 80 * math.cos(math.radians(130)))
        ghost_y = int(byte_cy + (1 - t) * 60 * math.sin(math.radians(130)))
        ghost_r = int(18 * (1 - t * 0.7))
        ghost_a = int(35 * (1 - t))   # fading alpha
        glow  = Image.new('RGBA', img.size, (0, 0, 0, 0))
        gd    = ImageDraw.Draw(glow)
        gd.ellipse([ghost_x - ghost_r, ghost_y - ghost_r,
                    ghost_x + ghost_r, ghost_y + ghost_r],
                   fill=(*ELEC_CYAN_FD, ghost_a))
        img.paste(Image.alpha_composite(img.convert('RGBA'), glow).convert('RGB'))
    draw = ImageDraw.Draw(img)

    # Desaturation ring on floor under Byte's hover position
    desat_floor_y = floor_y + int((DRAW_H - floor_y) * 0.88)
    draw.ellipse([byte_cx - 38, desat_floor_y - 10,
                  byte_cx + 38, desat_floor_y + 10],
                 outline=DESAT_RING, width=2)
    draw.text_not_available = None  # placeholder — annotations below

    # Byte body — INVERTED TEARDROP shape (canonical)
    body_h = int((DRAW_H - floor_y) * 0.42)   # hover height gives ~30% draw_h body
    body_w = int(body_h * 0.72)
    body_top_y = byte_cy - body_h // 2

    # Body fill — ELEC_CYAN (teal)
    # Teardrop: ellipse top half + triangle bottom
    draw.ellipse([byte_cx - body_w // 2, body_top_y,
                  byte_cx + body_w // 2, byte_cy + body_h // 4],
                 fill=BYTE_TEAL)
    draw.polygon([
        (byte_cx - body_w // 2, byte_cy + body_h // 8),
        (byte_cx, byte_cy + body_h // 2),
        (byte_cx + body_w // 2, byte_cy + body_h // 8),
    ], fill=BYTE_TEAL)

    # Body shadow/dark side
    draw.ellipse([byte_cx - body_w // 2, body_top_y,
                  byte_cx, byte_cy + body_h // 4],
                 fill=BYTE_DARK)

    # ── Byte face: 3/4 toward Luma (camera-left) — STILL ──────────────────────
    # Expression: STILL. Neither threatening nor friendly. Hovering. Watching.
    # This is HIS assessment beat, mirroring Luma's.
    face_cx = byte_cx - int(body_w * 0.08)
    face_cy = body_top_y + int(body_h * 0.25)
    face_r  = int(body_w * 0.45)

    # Face base
    draw.ellipse([face_cx - face_r, face_cy - face_r,
                  face_cx + face_r, face_cy + face_r],
                 fill=BYTE_TEAL)

    # Normal eye (right eye of Byte — toward Luma, camera-left side of his face at 3/4)
    ne_cx = face_cx - int(face_r * 0.35)
    ne_cy = face_cy - int(face_r * 0.18)
    ne_r  = int(face_r * 0.30)
    draw.ellipse([ne_cx - ne_r, ne_cy - ne_r, ne_cx + ne_r, ne_cy + ne_r],
                 fill=(8, 8, 18))   # dark sclera (Glitchkin: no white)
    # Iris — DEEP_CYAN
    DEEP_CYAN = (0, 155, 175)
    draw.ellipse([ne_cx - ne_r + 3, ne_cy - ne_r + 3,
                  ne_cx + ne_r - 3, ne_cy + ne_r - 3],
                 fill=DEEP_CYAN)
    # Pupil — level, aimed toward Luma (iris shift left = looking camera-left)
    iris_shift_x = -int(ne_r * 0.30)
    draw.ellipse([ne_cx + iris_shift_x - 5, ne_cy - 5,
                  ne_cx + iris_shift_x + 5, ne_cy + 5],
                 fill=VOID_BLACK)

    # Cracked eye (left eye of Byte — facing outward at 3/4)
    ce_cx = face_cx + int(face_r * 0.32)
    ce_cy = face_cy - int(face_r * 0.18)
    ce_r  = int(face_r * 0.28)
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
    # Processing dot (alive) — outward divergence (Lee Tanaka spec)
    div_x = -int(ce_r * 0.20)
    draw.ellipse([ce_cx + div_x - 3, ce_cy - 3,
                  ce_cx + div_x + 3, ce_cy + 3],
                 fill=ELEC_CYAN)

    # Mouth — closed pixel line (neutral: flat grimace with tiny curve)
    # Slight asymmetry — one corner barely lifts (reluctant acknowledgment?)
    mouth_y = face_cy + int(face_r * 0.40)
    mouth_w = int(face_r * 0.60)
    draw.rectangle([face_cx - mouth_w, mouth_y - 2,
                    face_cx + mouth_w, mouth_y + 2],
                   fill=VOID_BLACK)
    # Pixel teeth hint (barely — mostly closed)
    for mx_tooth in range(face_cx - mouth_w + 2, face_cx + mouth_w - 2, 5):
        draw.point((mx_tooth, mouth_y), fill=(200, 200, 210))

    # Stubby arms — at sides, neutral
    arm_top_y = body_top_y + int(body_h * 0.35)
    arm_bot_y = arm_top_y + int(body_h * 0.22)
    arm_l_x   = byte_cx - body_w // 2 - 6
    arm_r_x   = byte_cx + body_w // 2 + 6
    arm_w     = 10
    # Left arm
    draw.rectangle([arm_l_x - arm_w, arm_top_y, arm_l_x, arm_bot_y],
                   fill=BYTE_TEAL)
    # Right arm
    draw.rectangle([arm_r_x, arm_top_y, arm_r_x + arm_w, arm_bot_y],
                   fill=BYTE_TEAL)

    # Stubby legs — feet in air (hovering)
    leg_top_y = byte_cy + int(body_h * 0.35)
    leg_bot_y = leg_top_y + int(body_h * 0.22)
    draw.rectangle([byte_cx - 16, leg_top_y, byte_cx - 4, leg_bot_y],
                   fill=BYTE_TEAL)
    draw.rectangle([byte_cx + 4, leg_top_y, byte_cx + 16, leg_bot_y],
                   fill=BYTE_TEAL)

    # Cyan glow from Byte
    add_glow(img, byte_cx, byte_cy, int(body_w * 2.2), ELEC_CYAN,
             steps=8, max_alpha=22)
    draw = ImageDraw.Draw(img)

    # ── Falling pixel chip — THE KEY PROP ────────────────────────────────────
    # One 6×6 ELEC_CYAN pixel square, falling between Luma and Byte.
    # Position: horizontally between them, vertically ~2/3 down draw area.
    chip_x = int(PW * 0.50)
    chip_y = int(DRAW_H * 0.55)
    chip_sz = 7
    draw.rectangle([chip_x - chip_sz, chip_y - chip_sz,
                    chip_x + chip_sz, chip_y + chip_sz],
                   fill=ELEC_CYAN)
    draw.rectangle([chip_x - chip_sz + 1, chip_y - chip_sz + 1,
                    chip_x + chip_sz - 1, chip_y + chip_sz - 1],
                   outline=VOID_BLACK, width=1)   # pixel grid lines

    # Dotted descent line above chip (it is falling from above)
    for dy in range(0, 40, 6):
        draw.point((chip_x, chip_y - chip_sz - 4 - dy), fill=ELEC_CYAN_DIM)

    # ── Annotations ──────────────────────────────────────────────────────────
    font_ann  = load_font(9,  bold=False)
    font_ann_b= load_font(9,  bold=True)
    font_sm   = load_font(8,  bold=False)

    # Camera note
    draw.text((8, 8), 'MED  |  4-5FT  |  FLAT HORIZON  |  BEAT OF STILLNESS',
              font=font_ann, fill=ANN_COLOR)

    # Chip annotation
    draw.text((chip_x + chip_sz + 6, chip_y - 6), '"soft tick"',
              font=font_ann_b, fill=ANN_CYAN)
    draw.text((chip_x + chip_sz + 6, chip_y + 6), "only thing moving",
              font=font_sm, fill=ANN_DIM)

    # Luma annotation — ASSESSING
    draw.text((luma_cx - 35, head_cy - head_r - 32),
              "ASSESSING", font=font_ann_b, fill=ANN_COLOR)
    draw.text((luma_cx - 30, head_cy - head_r - 22),
              "(fear gone, processing)", font=font_sm, fill=(130, 120, 100))

    # Byte annotation — STILL
    draw.text((byte_cx + body_w // 2 + 10, face_cy - 10),
              "STILL", font=font_ann_b, fill=ANN_CYAN)
    draw.text((byte_cx + body_w // 2 + 10, face_cy + 2),
              "(mirror of Luma's beat)", font=font_sm, fill=ANN_DIM)

    # Pixel trail note
    draw.text((int(PW * 0.58), int(DRAW_H * 0.15)),
              "trail fading", font=font_sm, fill=ELEC_CYAN_DIM)
    draw.text((int(PW * 0.58), int(DRAW_H * 0.15) + 10),
              "(last wisps)", font=font_sm, fill=ELEC_CYAN_DIM)

    # Desat ring annotation
    draw.text((byte_cx + 42, desat_floor_y - 5),
              "desat ring", font=font_sm, fill=(160, 155, 150))

    # Depth temp annotation
    draw.text((int(PW * 0.08), DRAW_H - 16),
              "WARM (Luma zone)", font=font_sm, fill=(180, 130, 60))
    draw.text((int(PW * 0.68), DRAW_H - 16),
              "COOL (Byte zone)", font=font_sm, fill=ELEC_CYAN_DIM)

    # Empty floor / negative space annotation
    gap_label_x = int(PW * 0.42)
    gap_label_y = int(DRAW_H * 0.75)
    draw.text((gap_label_x - 24, gap_label_y), "NEGATIVE SPACE",
              font=font_sm, fill=(100, 96, 88))
    draw.text((gap_label_x - 16, gap_label_y + 10), "(their distance)",
              font=font_sm, fill=(80, 76, 70))

    # ── Three-tier caption bar ────────────────────────────────────────────────
    font_t1   = load_font(13, bold=True)
    font_t2   = load_font(11, bold=False)
    font_t3   = load_font(9,  bold=False)
    font_meta = load_font(8,  bold=False)

    draw.rectangle([0, DRAW_H, PW, PH], fill=BG_CAPTION)
    draw.line([0, DRAW_H, PW, DRAW_H], fill=(8, 6, 4), width=2)

    # Tier 1 — Shot code
    draw.text((10, DRAW_H + 4),
              "P17  |  MED  |  4-5FT  |  BEAT OF STILLNESS  |  CHIP FALLS",
              font=font_t1, fill=TEXT_SHOT)

    # Tier 2 — Arc label
    draw.text((PW - 260, DRAW_H + 5),
              "ARC: CURIOUS / FIRST ENCOUNTER", font=font_t2, fill=ELEC_CYAN)

    # Tier 3 — Narrative description
    draw.text((10, DRAW_H + 22),
              "Luma sitting cross-legged. Byte hovering across room. Trails fading. Everything stops.",
              font=font_t3, fill=TEXT_DESC)
    draw.text((10, DRAW_H + 35),
              "One pixel chip falls between them. \"Soft tick.\" This cracks the standoff.",
              font=font_t3, fill=(120, 112, 90))

    # Metadata
    draw.text((PW - 276, DRAW_H + 56),
              "LTG_SB_cold_open_P17  /  Diego Vargas  /  C46",
              font=font_meta, fill=TEXT_META)

    # Arc border — ELEC_CYAN (CURIOUS / FIRST ENCOUNTER — turning point)
    draw.rectangle([0, 0, PW - 1, PH - 1], outline=ARC_COLOR, width=4)

    img.thumbnail((1280, 1280))
    img.save(OUTPUT_PATH, "PNG")
    print(f"Saved: {OUTPUT_PATH}  {img.size}")
    return OUTPUT_PATH


if __name__ == "__main__":
    draw_panel()
    print("P17 standalone panel generation complete.")
    print("Beat: Beat of stillness. Luma cross-legged. Byte hovering across room.")
    print("Pixel trails fading. One chip falls between them: 'soft tick'.")
    print("ELEC_CYAN border. Warm/cool depth temperature rule applied.")
