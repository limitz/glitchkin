#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_sb_cold_open_P15.py
Cold Open Panel P15 — MED — Luma Hits Floor / Glitch Forced-Hair Circle
Diego Vargas, Storyboard Artist — Cycle 45 (C48: elbow bend + torso rotation + bent knee)

Beat: Luma has hit the floor. Comedic fall. The Glitch energy briefly forces
      her hair into a PERFECT GEOMETRIC CIRCLE — against all natural physics.
      This lasts 8 frames maximum; we're capturing the HELD state (peak of
      the forced-circle beat). In the next moments, natural chaos reasserts.

This is a visual joke AND a worldbuilding beat:
  - Luma's hair is canonically wild/chaotic (her identity)
  - Glitch world imposes ORDER (circles, grids, geometry)
  - The forced-circle is WRONG for her character — unsettling + funny
  - "8 frames max" annotation tells animators: don't hold it longer

Camera: Floor-level — camera is 6 inches off the ground, looking ACROSS the floor.
        This makes Luma look flat/low (she's on the floor). Very wide horizontal field.
        No Dutch tilt — flat horizon = floor is stable (the LANDING, not the chaos).

Key staging:
  - Luma at center-left, face-down on floor (or just rolling to her back)
    We see her from the side: feet right, head left, sprawled flat.
  - Hair cloud: PERFECT CIRCLE around her head — GEOMETRIC, hard-edged.
    Outline: ELEC_CYAN single pixel width (Glitch imposition).
    Interior: Luma's natural hair color (dark brown) but arranged in RADIAL LINES
              (forced Glitch order — not natural hair texture).
  - Small annotation at the circle: "GLITCH FORCED SYMMETRY — 8 FRAMES MAX"
  - Her face: one eye just visible (she's sideways to camera or 3/4 to camera).
    Expression: DAZED / WINDED. Not hurt — cartoon-dazed stars optional.
  - Cyan glow diffuse across the floor (Byte's ambient field).
  - Confetti from Byte drifting down (he's nearby, off-panel).
  - Hoodie (LUMA_HOODIE orange) is the warm color anchor in a cool-ambient scene.

Camera note annotation: "FLOOR-LEVEL CAM — 6\" OFF GROUND"

Arc: TENSE → COMEDY BREAK (HOT_MAGENTA border — tension still high but comedy
     undercuts it, which is the show's grammar. Magenta = the world is weird.)
Image size rule: ≤ 1280px in both dimensions.
Output: output/storyboards/panels/LTG_SB_cold_open_P15.png
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
OUTPUT_PATH = os.path.join(PANELS_DIR, "LTG_SB_cold_open_P15.png")
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
LUMA_HOODIE   = (232, 112, 58)   # canonical orange — CRITICAL
LUMA_SKIN     = (218, 172, 128)
LUMA_SKIN_SH  = (175, 128, 88)
LUMA_HAIR     = (38, 22, 14)     # natural dark brown hair
LUMA_PANTS    = (70, 80, 110)    # jeans / dark pants
LUMA_SHOES    = (42, 36, 30)     # dark shoes
FLOOR_WARM    = (155, 128, 92)   # warm den floor
FLOOR_GRAIN   = (130, 108, 76)   # floor plank lines
WALL_WARM     = (190, 170, 138)
DEEP_SPACE    = (6, 4, 14)
# Caption
BG_CAPTION    = (12, 8, 6)
TEXT_SHOT     = (232, 224, 204)
TEXT_ARC      = HOT_MAGENTA
TEXT_DESC     = (155, 148, 122)
TEXT_META     = (88, 82, 66)
ARC_COLOR     = HOT_MAGENTA
ANN_COLOR     = (220, 200, 80)
ANN_CYAN      = (0, 180, 210)
ANN_WARN      = (232, 100, 40)   # orange-red for animation warning notes

RNG = random.Random(1515)


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
    img  = Image.new('RGB', (PW, PH), FLOOR_WARM)
    draw = ImageDraw.Draw(img)

    # ── Background: floor-level camera — floor dominates ─────────────────────
    # At 6" off ground, the floor fills the BOTTOM ~70% of the frame.
    # The very top strip shows baseboard + lower wall.
    wall_h  = int(DRAW_H * 0.18)    # thin sliver of wall at top
    floor_y = wall_h

    # Wall strip (top)
    draw.rectangle([0, 0, PW, wall_h], fill=WALL_WARM)

    # Baseboard
    draw.rectangle([0, wall_h - 8, PW, wall_h], fill=(120, 100, 70))

    # Floor fill
    draw.rectangle([0, floor_y, PW, DRAW_H], fill=FLOOR_WARM)

    # Floor planks — low camera makes planks prominent, converging perspective
    # They run left-right but appear to converge at a VP just above the horizon
    vp_x = PW // 2
    vp_y = wall_h + 4
    plank_spacing = 32
    for py in range(floor_y, DRAW_H, plank_spacing):
        draw.line([(0, py), (PW, py)], fill=FLOOR_GRAIN, width=1)

    # Warm ambient light from upper-left (room lamp)
    add_glow(img, int(PW * 0.02), int(DRAW_H * 0.08), int(PW * 0.55),
             SUNLIT_AMB, steps=10, max_alpha=20)
    draw = ImageDraw.Draw(img)

    # Cyan diffuse from Byte (off-panel right — Byte is nearby)
    add_glow(img, PW + 40, int(DRAW_H * 0.55), int(PW * 0.75),
             ELEC_CYAN, steps=10, max_alpha=22)
    draw = ImageDraw.Draw(img)

    # ── LUMA — sprawled on floor, side-view ──────────────────────────────────
    # Camera-left to camera-right: head (left) to feet (right).
    # Body lying flat — floor-level camera makes her look like a horizontal strip.
    # She's in the lower-center zone of the frame.

    luma_floor_y = int(DRAW_H * 0.70)   # where her body contacts the floor

    # ──── BODY: horizontal silhouette with torso rotation (C48 Lee fix) ────
    # 5° clockwise rotation to sell "just hit the floor" vs "lying flat by choice"
    torso_rot_deg = 5  # degrees CW
    torso_rot_rad = math.radians(torso_rot_deg)

    # Legs + feet (camera-right) — one leg bent (knee up) for impact read
    feet_x  = int(PW * 0.75)
    feet_y  = luma_floor_y - 12
    torso_x = int(PW * 0.38)  # shoulder/torso left edge

    # ── Straight leg (lower, closer to floor)
    draw.rectangle([torso_x + 60, feet_y - 18, feet_x - 30, feet_y + 12],
                   fill=LUMA_PANTS)
    # Shoe on straight leg
    draw.ellipse([feet_x - 40, feet_y - 8, feet_x - 10, feet_y + 12],
                 fill=LUMA_SHOES)

    # ── Bent knee (upper leg angled UP, lower leg dropped back down)
    knee_x = torso_x + 90
    knee_y = feet_y - 34   # knee raised above floor plane
    # Upper leg: hip to knee
    draw.line([(torso_x + 65, feet_y - 4), (knee_x, knee_y)],
              fill=LUMA_PANTS, width=20)
    # Lower leg: knee back down toward floor
    bent_foot_x = knee_x + 36
    bent_foot_y = feet_y + 4
    draw.line([(knee_x, knee_y), (bent_foot_x, bent_foot_y)],
              fill=LUMA_PANTS, width=18)
    # Shoe on bent leg
    draw.ellipse([bent_foot_x - 6, bent_foot_y - 8, bent_foot_x + 20, bent_foot_y + 8],
                 fill=LUMA_SHOES)

    # ── Hoodie torso — rotated 5° CW for "just landed" asymmetry
    # Draw on RGBA layer, rotate, composite
    torso_layer = Image.new('RGBA', (PW, PH), (0, 0, 0, 0))
    td = ImageDraw.Draw(torso_layer)
    torso_w = 80
    torso_h = 46
    torso_cx = torso_x + torso_w // 2
    torso_cy = feet_y - torso_h // 2 + 4
    # Torso as rotated polygon (4 corners of rectangle, rotated around center)
    cos_r = math.cos(torso_rot_rad)
    sin_r = math.sin(torso_rot_rad)
    torso_corners = [(-torso_w // 2, -torso_h // 2), (torso_w // 2, -torso_h // 2),
                     (torso_w // 2, torso_h // 2), (-torso_w // 2, torso_h // 2)]
    rotated_pts = [(int(torso_cx + lx * cos_r - ly * sin_r),
                    int(torso_cy + lx * sin_r + ly * cos_r))
                   for lx, ly in torso_corners]
    td.polygon(rotated_pts, fill=(*LUMA_HOODIE, 255))
    img.paste(Image.alpha_composite(img.convert('RGBA'), torso_layer).convert('RGB'))
    draw = ImageDraw.Draw(img)

    # ── Right arm: two-segment polyline with elbow bend + hand blob + sleeve bunching
    # Shoulder origin (right side of torso, slightly offset for rotation)
    shoulder_x = torso_x + 2
    shoulder_y = torso_cy - 8
    # Elbow (bend point — arm bends at roughly 120 degrees)
    elbow_x = int(PW * 0.30)
    elbow_y = luma_floor_y - 18
    # Hand endpoint
    hand_x = int(PW * 0.22)
    hand_y = luma_floor_y - 8
    # Upper arm segment (shoulder → elbow)
    draw.line([(shoulder_x, shoulder_y), (elbow_x, elbow_y)],
              fill=LUMA_HOODIE, width=18)
    # Hoodie sleeve bunching at elbow — small ellipse bump
    draw.ellipse([elbow_x - 12, elbow_y - 10, elbow_x + 10, elbow_y + 8],
                 fill=LUMA_HOODIE)
    # Lower arm segment (elbow → hand)
    draw.line([(elbow_x, elbow_y), (hand_x, hand_y)],
              fill=LUMA_HOODIE, width=14)
    # Hand blob at endpoint
    draw.ellipse([hand_x - 8, hand_y - 6, hand_x + 8, hand_y + 6],
                 fill=LUMA_SKIN)

    # ──── HEAD + FACE ──────────────────────────────────────────────────────
    head_cx = int(PW * 0.24)
    head_cy = luma_floor_y - 44
    head_r  = 28

    draw.ellipse([head_cx - head_r, head_cy - head_r,
                  head_cx + head_r, head_cy + head_r],
                 fill=LUMA_SKIN)

    # Face — 3/4 view, dazed. One eye visible (camera-side), slightly open.
    # DAZED: reduced aperture, iris off-center (she's winded, not focused)
    eye_cx = head_cx + 8
    eye_cy = head_cy + 2
    eye_h  = 7
    eye_w  = 12
    # White of eye
    draw.ellipse([eye_cx - eye_w, eye_cy - eye_h,
                  eye_cx + eye_w, eye_cy + eye_h],
                 fill=(240, 230, 220))
    # Iris (dazed — not focused, off-center downward)
    draw.ellipse([eye_cx - 4, eye_cy, eye_cx + 4, eye_cy + 6],
                 fill=(80, 50, 28))
    # Pupil
    draw.ellipse([eye_cx - 2, eye_cy + 1, eye_cx + 2, eye_cy + 5],
                 fill=VOID_BLACK)
    # Eyelid (droopy — winded)
    draw.arc([eye_cx - eye_w, eye_cy - eye_h - 2,
              eye_cx + eye_w, eye_cy + eye_h + 2],
             start=210, end=330, fill=(42, 22, 10), width=2)
    # Mouth: flat, slightly open — winded "ooof" face
    draw.arc([head_cx, head_cy + 8, head_cx + 16, head_cy + 18],
             start=0, end=180, fill=(120, 72, 44), width=2)

    # Daze stars (small, cartoon — 3 small asterisks around head)
    for si, (sx_off, sy_off) in enumerate([(-18, -22), (24, -30), (34, -10)]):
        sx = head_cx + sx_off
        sy = head_cy + sy_off
        star_c = (220, 200, 80) if si % 2 == 0 else ELEC_CYAN
        for ang in range(0, 360, 60):
            a = math.radians(ang)
            draw.line([(sx, sy),
                       (sx + int(6 * math.cos(a)), sy + int(6 * math.sin(a)))],
                      fill=star_c, width=1)

    # ──── GLITCH FORCED-HAIR CIRCLE ───────────────────────────────────────────
    # Canonical hair would be a wild irregular cloud (see Maya Santos character sheets).
    # Right now: GLITCH has imposed a PERFECT CIRCLE on it.
    # Circle is centered on the head center, radius = head_r * 1.55.
    # Interior: dark hair color in radial lines (forced order).
    # Outline: ELEC_CYAN (Glitch imposition — single bright edge).

    hair_circle_r = int(head_r * 1.55)
    hc_cx = head_cx
    hc_cy = head_cy

    # Hair fill inside circle — dark brown with RADIAL LINES (forced Glitch order)
    # Draw as filled circle of hair color first
    hair_layer = Image.new('RGBA', (PW, PH), (0, 0, 0, 0))
    hld        = ImageDraw.Draw(hair_layer)

    hld.ellipse([hc_cx - hair_circle_r, hc_cy - hair_circle_r,
                 hc_cx + hair_circle_r, hc_cy + hair_circle_r],
                fill=(*LUMA_HAIR, 255))

    # Radial lines inside circle (Glitch order grid) — draw on top in slightly lighter hair
    HAIR_LIGHT = (58, 36, 22)
    for ang_deg in range(0, 180, 12):
        ang = math.radians(ang_deg)
        x0  = int(hc_cx - hair_circle_r * math.cos(ang))
        y0  = int(hc_cy - hair_circle_r * math.sin(ang))
        x1  = int(hc_cx + hair_circle_r * math.cos(ang))
        y1  = int(hc_cy + hair_circle_r * math.sin(ang))
        hld.line([(x0, y0), (x1, y1)], fill=(*HAIR_LIGHT, 160), width=2)

    img.paste(Image.alpha_composite(img.convert('RGBA'), hair_layer).convert('RGB'))
    draw = ImageDraw.Draw(img)

    # ELEC_CYAN circle outline (Glitch imposition — crisp geometric edge)
    draw.ellipse([hc_cx - hair_circle_r, hc_cy - hair_circle_r,
                  hc_cx + hair_circle_r, hc_cy + hair_circle_r],
                 outline=ELEC_CYAN, width=2)

    # Small pixel artifacts on circle edge (Glitch energy leaking)
    for ci in range(0, 360, 30):
        angle = math.radians(ci)
        px = int(hc_cx + hair_circle_r * math.cos(angle))
        py = int(hc_cy + hair_circle_r * math.sin(angle))
        sz = RNG.choice([2, 4])
        draw.rectangle([px - sz // 2, py - sz // 2, px + sz // 2, py + sz // 2],
                        fill=ELEC_CYAN)

    # ── Confetti from Byte (off-panel right) drifting down ────────────────────
    for _ in range(22):
        px = RNG.randint(int(PW * 0.30), PW - 10)
        py = RNG.randint(int(DRAW_H * 0.15), int(DRAW_H * 0.80))
        sz = RNG.choice([2, 4, 4])
        draw.rectangle([px, py, px + sz, py + sz], fill=ELEC_CYAN)

    # ── Annotations ──────────────────────────────────────────────────────────
    font_ann = load_font(9)
    font_sm  = load_font(8)
    font_bold= load_font(9, bold=True)

    # Camera note
    draw.text((8, 8), 'FLOOR-LEVEL CAM  |  6" OFF GROUND',
              font=font_ann, fill=ANN_COLOR)

    # Hair circle annotation — critical animation note
    circle_label_x = hc_cx + hair_circle_r + 6
    circle_label_y = hc_cy - 18
    draw.text((circle_label_x, circle_label_y),
              "GLITCH FORCED SYMMETRY", font=font_bold, fill=ANN_CYAN)
    draw.text((circle_label_x, circle_label_y + 11),
              "8 FRAMES MAX", font=font_bold, fill=ANN_WARN)
    draw.text((circle_label_x, circle_label_y + 22),
              "then natural chaos", font=font_sm, fill=(100, 120, 130))
    draw.text((circle_label_x, circle_label_y + 32),
              "reasserts itself", font=font_sm, fill=(100, 120, 130))
    # Arrow from label to circle edge
    draw.line([(circle_label_x - 2, circle_label_y + 5),
               (hc_cx + hair_circle_r - 2, hc_cy - 4)],
              fill=ANN_CYAN, width=1)

    # Hoodie label (confirm canonical orange)
    draw.text((torso_x + 5, feet_y + 16),
              "LUMA_HOODIE #E8703A", font=font_sm, fill=(180, 100, 50))

    # Daze stars label
    draw.text((head_cx + 36, head_cy - 34),
              "DAZED", font=font_sm, fill=(160, 140, 60))

    # Cyan off-panel note
    draw.text((PW - 130, int(DRAW_H * 0.30)),
              "BYTE (off-panel R)", font=font_sm, fill=ELEC_CYAN_DIM)
    draw.text((PW - 130, int(DRAW_H * 0.30) + 10),
              "confetti drifts down", font=font_sm, fill=(70, 110, 120))

    # ── Three-tier caption bar ────────────────────────────────────────────────
    font_t1   = load_font(13, bold=True)
    font_t2   = load_font(11, bold=False)
    font_t3   = load_font(9,  bold=False)
    font_meta = load_font(8,  bold=False)

    draw.rectangle([0, DRAW_H, PW, PH], fill=BG_CAPTION)
    draw.line([0, DRAW_H, PW, DRAW_H], fill=(8, 6, 4), width=2)

    # Tier 1 — Shot code
    draw.text((10, DRAW_H + 4),
              "P15  |  MED  |  FLOOR-LEVEL CAM  |  COMEDY BEAT",
              font=font_t1, fill=TEXT_SHOT)

    # Tier 2 — Arc label
    draw.text((PW - 220, DRAW_H + 5),
              "ARC: TENSE / COMEDY", font=font_t2, fill=TEXT_ARC)

    # Tier 3 — Narrative description
    draw.text((10, DRAW_H + 22),
              "Luma hits floor. Glitch forces hair to perfect circle — WRONG for her character.",
              font=font_t3, fill=TEXT_DESC)

    draw.text((10, DRAW_H + 35),
              "8 FRAMES MAX then natural chaos reasserts. Comedy undercuts tension.",
              font=font_t3, fill=(120, 112, 90))

    # Metadata
    draw.text((PW - 276, DRAW_H + 56),
              "LTG_SB_cold_open_P15  /  Diego Vargas  /  C48",
              font=font_meta, fill=TEXT_META)

    # Arc border — HOT_MAGENTA (TENSE — weird Glitch world)
    draw.rectangle([0, 0, PW - 1, PH - 1], outline=ARC_COLOR, width=4)

    img.thumbnail((1280, 1280))
    img.save(OUTPUT_PATH, "PNG")
    print(f"Saved: {OUTPUT_PATH}  {img.size}")
    return OUTPUT_PATH


if __name__ == "__main__":
    draw_panel()
    print("P15 standalone panel generation complete.")
    print("Beat: Luma hits floor. Glitch forces hair to perfect circle (8 frames max).")
    print("Floor-level camera. LUMA_HOODIE canonical orange preserved.")
    print("FORCED CIRCLE annotation + '8 FRAMES MAX' animation note.")
