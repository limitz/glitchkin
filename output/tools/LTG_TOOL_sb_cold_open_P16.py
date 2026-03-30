#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_sb_cold_open_P16.py
Cold Open Panel P16 — ECU — Luma Face Pressed to Floor / "...okay. ...WHAT."
Diego Vargas, Storyboard Artist — Cycle 46

Beat: Direct continuation from P15 (Luma hits floor). Now we cut to ECU of her face,
      pressed right against the floor planks. The Glitch hair-circle has faded — her hair
      is back to natural wild chaos but still faintly glowing cyan at the edges. One eye is
      open: TRACKING. She's cataloguing the situation before reacting.

      The expression is pure comedy setup: she's trying to stay calm ("...okay.") while
      the evidence in front of her is utterly absurd ("...WHAT."). The eye is WIDE OPEN —
      this is the involuntary snap of recognition. Both lines of dialogue are annotated
      in-panel since timing is critical.

Camera: EXTREME CLOSE-UP. Face fills the full draw area. Camera is floor-level
        (slightly above the floor surface so we see the floor plank she's pressed against).
        We see one eye (the left, camera-right), cheek on floor, part of the nose,
        and loose strands of hair above.

Key staging:
  - Floor plank fills the BOTTOM edge of the frame — she's literally pressed to it.
  - Face angle: 3/4 to camera, slight downward tilt (cheek-to-floor perspective).
  - Eye: WIDE OPEN — the full aperture white-of-eye read. Iris level-forward.
    This is the "against my will I am registering this" look. Brow: FLAT-TO-RAISED
    (inner corner slightly up — involuntary registration, not fear).
  - Cyan glow diffuse on her cheek from Byte's ambient field nearby.
  - Hair: back to natural chaos, but 1-2 strands still show faint geometric
    straightness (Glitch residue). Most has reasserted into wild cloud.
  - Dialogue annotated: "...okay." (small, trying-to-stay-calm) then "...WHAT."
    (larger, the crack in composure). Two lines: composure then fracture.

Arc: TENSE / COMEDY (HOT_MAGENTA border — this is the same arc-moment as P15,
     now on her face. The punchline of the fall sequence.)

Image size rule: <= 1280px both dimensions.
Output: output/storyboards/panels/LTG_SB_cold_open_P16.png
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
OUTPUT_PATH = os.path.join(PANELS_DIR, "LTG_SB_cold_open_P16.png")
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
LUMA_SKIN_SH  = (175, 128, 88)
LUMA_SKIN_HI  = (235, 196, 155)   # highlight
LUMA_HAIR     = (38, 22, 14)
FLOOR_WARM    = (155, 128, 92)
FLOOR_GRAIN   = (130, 108, 76)
FLOOR_HI      = (170, 142, 104)
DEEP_SPACE    = (6, 4, 14)

# Caption
BG_CAPTION    = (12, 8, 6)
TEXT_SHOT     = (232, 224, 204)
TEXT_DESC     = (155, 148, 122)
TEXT_META     = (88, 82, 66)
ARC_COLOR     = HOT_MAGENTA
ANN_COLOR     = (220, 200, 80)
ANN_CYAN      = (0, 180, 210)
ANN_DLG       = (240, 230, 200)    # dialogue annotation color

RNG = random.Random(1616)


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


def draw_panel():
    img  = Image.new('RGB', (PW, PH), LUMA_SKIN)
    draw = ImageDraw.Draw(img)

    # ── Background: ECU — face fills frame ───────────────────────────────────
    # Skin tone gradient fill across the whole draw area.
    # Bottom edge: floor plank strip (she is pressed against it).
    # Top: hair cloud (dark) bleeds in from top edge.

    # Skin gradient — slightly darker toward edges (natural shading for a face)
    for y in range(DRAW_H):
        t = y / DRAW_H
        # Slightly warmer at mid-face, cooler at top/bottom
        if t < 0.5:
            c = lerp_color(LUMA_SKIN_SH, LUMA_SKIN, t * 2)
        else:
            c = lerp_color(LUMA_SKIN, LUMA_SKIN_SH, (t - 0.5) * 2)
        draw.line([(0, y), (PW, y)], fill=c)

    # Floor plank strip at very bottom of draw area (3/8ths up from bottom)
    # Camera is just above floor — plank edge cuts across the bottom portion
    plank_y = int(DRAW_H * 0.72)
    draw.rectangle([0, plank_y, PW, DRAW_H], fill=FLOOR_WARM)
    # Plank grain lines
    for py in range(plank_y, DRAW_H, 22):
        draw.line([(0, py), (PW, py)], fill=FLOOR_GRAIN, width=1)
    # Plank separation line (strong edge — face meets floor)
    draw.line([(0, plank_y), (PW, plank_y)], fill=FLOOR_GRAIN, width=3)

    # Hair at top of frame — wild dark cloud, natural chaos reasserted
    hair_band_h = int(DRAW_H * 0.28)
    # Hair base fill
    draw.rectangle([0, 0, PW, hair_band_h], fill=LUMA_HAIR)
    # Irregular lower hair boundary — chaotic (NOT the Glitch circle anymore)
    for hx in range(0, PW, 12):
        hvar = RNG.randint(0, int(DRAW_H * 0.12))
        # Draw irregular hair strands downward
        draw.line([(hx, hair_band_h - 5), (hx + RNG.randint(-8, 8), hair_band_h + hvar)],
                  fill=LUMA_HAIR, width=RNG.choice([2, 3, 4]))
    # Hair highlight (natural light catching a strand)
    HAIR_HI = (62, 38, 22)
    draw.line([(int(PW * 0.20), hair_band_h - 30), (int(PW * 0.35), hair_band_h + 5)],
              fill=HAIR_HI, width=2)

    # One strand with FAINT geometric straightness (Glitch residue — just barely)
    # One almost-straight strand at edge of hair cloud
    draw.line([(int(PW * 0.62), hair_band_h + 10), (int(PW * 0.66), hair_band_h + 55)],
              fill=(52, 32, 18), width=3)   # slightly too straight but easy to miss

    # ── Cyan glow from Byte (directional — from camera-right, Byte is off-frame) ──
    add_glow(img, PW + 60, int(DRAW_H * 0.45), int(PW * 0.95),
             ELEC_CYAN, steps=12, max_alpha=28)
    draw = ImageDraw.Draw(img)

    # Cyan highlight on cheek (Byte's ambient field painting her skin)
    # Cheek is approximately right-center of draw area (camera-right = Luma's face angle)
    cheek_cx = int(PW * 0.72)
    cheek_cy = int(DRAW_H * 0.52)
    add_glow(img, cheek_cx, cheek_cy, 90, ELEC_CYAN, steps=8, max_alpha=20)
    draw = ImageDraw.Draw(img)

    # ── THE EYE — open, tracking ──────────────────────────────────────────────
    # This is the critical element. WIDE OPEN — involuntary registration.
    # Left eye of Luma (camera-right). 3/4 view so it reads forward-ish.
    # Eye center: slightly right of center, vertically mid-frame.

    eye_cx = int(PW * 0.55)
    eye_cy = int(DRAW_H * 0.46)
    eye_rw = 62    # half-width of eye
    eye_rh = 38    # half-height (open aperture — this is WIDE)

    # Eye white — full open aperture (the WIDE-OPEN read)
    draw.ellipse([eye_cx - eye_rw, eye_cy - eye_rh,
                  eye_cx + eye_rw, eye_cy + eye_rh],
                 fill=(245, 238, 228))

    # Iris — warm dark brown, tracking level-forward (she is registering, not scared)
    iris_r = 26
    # Iris positioned level-forward (not up, not down — pure "registering" gaze)
    iris_ox = 0   # no lateral shift — she's looking straight at the impossible thing
    iris_oy = 0
    draw.ellipse([eye_cx + iris_ox - iris_r, eye_cy + iris_oy - iris_r,
                  eye_cx + iris_ox + iris_r, eye_cy + iris_oy + iris_r],
                 fill=(65, 40, 22))

    # Pupil — large (low light, wide-open)
    pupil_r = 15
    draw.ellipse([eye_cx + iris_ox - pupil_r, eye_cy + iris_oy - pupil_r,
                  eye_cx + iris_ox + pupil_r, eye_cy + iris_oy + pupil_r],
                 fill=VOID_BLACK)

    # Catch light — small warm white highlight
    draw.ellipse([eye_cx + iris_ox + 6, eye_cy + iris_oy - 12,
                  eye_cx + iris_ox + 14, eye_cy + iris_oy - 4],
                 fill=(250, 248, 242))

    # Cyan catch light (Byte's ambient reflected in eye — SMALL, secondary)
    draw.ellipse([eye_cx + iris_ox - 14, eye_cy + iris_oy - 10,
                  eye_cx + iris_ox - 8,  eye_cy + iris_oy - 4],
                 fill=(*ELEC_CYAN, ))

    # Top eyelid (upper lid — barely descending; eye is OPEN)
    draw.arc([eye_cx - eye_rw - 4, eye_cy - eye_rh - 4,
              eye_cx + eye_rw + 4, eye_cy + eye_rh + 4],
             start=200, end=340, fill=(40, 20, 10), width=3)

    # Lashes — 4-5 small lines at top of eye arc
    lash_positions = [200, 218, 236, 258, 278, 300, 320]
    for la in lash_positions:
        angle = math.radians(la)
        lx0   = int(eye_cx + (eye_rw + 2) * math.cos(angle))
        ly0   = int(eye_cy - (eye_rh + 2) * abs(math.sin(angle)))
        lx1   = int(lx0 + 4 * math.cos(angle))
        ly1   = int(ly0 - 5)
        draw.line([(lx0, ly0), (lx1, ly1)], fill=(30, 14, 6), width=2)

    # Brow — flat-to-slightly-raised (inner corner up — involuntary registration)
    # Brow is above the eye, arcing over it
    brow_inner_x = eye_cx - eye_rw + 10
    brow_inner_y = eye_cy - eye_rh - 22
    brow_outer_x = eye_cx + eye_rw - 8
    brow_outer_y = eye_cy - eye_rh - 10
    # Inner corner lifted slightly (registration)
    brow_inner_y -= 5   # TWITCH LIFTED — "against my will I am seeing this"
    draw.line([(brow_inner_x, brow_inner_y),
               (int((brow_inner_x + brow_outer_x) / 2), eye_cy - eye_rh - 20),
               (brow_outer_x, brow_outer_y)],
              fill=(42, 22, 10), width=4)

    # ── Nose bridge visible (partial — 3/4 view) ─────────────────────────────
    nose_bridge_x = int(PW * 0.40)
    nose_y0       = int(DRAW_H * 0.44)
    nose_y1       = int(DRAW_H * 0.62)
    draw.arc([nose_bridge_x, nose_y0, nose_bridge_x + 22, nose_y1],
             start=270, end=180, fill=LUMA_SKIN_SH, width=2)

    # ── Nose tip resting on floor plank (slight contact shadow) ──────────────
    nose_tip_x = int(PW * 0.35)
    nose_tip_y = plank_y - 2
    draw.ellipse([nose_tip_x - 18, nose_tip_y - 12,
                  nose_tip_x + 18, nose_tip_y + 4],
                 fill=LUMA_SKIN_SH)
    # Contact shadow under nose
    draw.ellipse([nose_tip_x - 14, nose_tip_y - 2,
                  nose_tip_x + 14, nose_tip_y + 6],
                 fill=(115, 90, 62))

    # Cheek — slightly compressed against floor (squish read)
    cheek_s_x = int(PW * 0.28)
    cheek_s_y = int(plank_y - 18)
    draw.ellipse([cheek_s_x - 32, cheek_s_y - 16,
                  cheek_s_x + 38, cheek_s_y + 8],
                 fill=LUMA_SKIN)
    draw = ImageDraw.Draw(img)

    # ── Dialogue annotations ──────────────────────────────────────────────────
    font_dlg_sm  = load_font(11, bold=False)
    font_dlg_lg  = load_font(16, bold=True)
    font_ann     = load_font(9,  bold=False)
    font_ann_b   = load_font(9,  bold=True)

    # "...okay." — small, near the mouth zone (lower-left area, near floor)
    dlg_okay_x = int(PW * 0.08)
    dlg_okay_y = int(DRAW_H * 0.64)
    draw.text((dlg_okay_x, dlg_okay_y), '"...okay."',
              font=font_dlg_sm, fill=ANN_DLG)
    # Arrow pointing up toward mouth area
    draw.line([(dlg_okay_x + 34, dlg_okay_y - 2),
               (int(PW * 0.25), int(DRAW_H * 0.60))],
              fill=ANN_COLOR, width=1)

    # "...WHAT." — larger, camera-left upper zone (the crack in composure)
    dlg_what_x = int(PW * 0.06)
    dlg_what_y = int(DRAW_H * 0.22)
    draw.text((dlg_what_x, dlg_what_y), '"...WHAT."',
              font=font_dlg_lg, fill=ANN_DLG)
    # Annotation: composure fracture marker
    draw.text((dlg_what_x, dlg_what_y + 20),
              "(composure fractures)", font=font_ann, fill=(130, 120, 100))

    # Gaze tracking annotation — dotted arrow from eye forward
    gaze_x0 = eye_cx + eye_rw + 4
    gaze_y0 = eye_cy
    draw.line([(gaze_x0, gaze_y0), (gaze_x0 + 70, gaze_y0)],
              fill=ANN_CYAN, width=1)
    for dx in range(0, 70, 8):
        if dx % 16 < 8:
            draw.point((gaze_x0 + dx, gaze_y0), fill=ANN_CYAN)
    draw.text((gaze_x0 + 74, gaze_y0 - 5), "TRACKING",
              font=font_ann_b, fill=ANN_CYAN)

    # Brow annotation — "involuntary registration"
    draw.text((brow_inner_x - 4, brow_inner_y - 16),
              "involuntary registration", font=font_ann, fill=ANN_COLOR)

    # Camera note
    draw.text((8, 8), 'ECU  |  FLOOR-LEVEL  |  FACE FILLS FRAME',
              font=font_ann, fill=ANN_COLOR)

    # Cyan glow annotation
    draw.text((PW - 170, int(DRAW_H * 0.10)),
              "BYTE ambient (off-R)", font=font_ann, fill=ANN_CYAN)
    draw.text((PW - 170, int(DRAW_H * 0.10) + 10),
              "cyan on cheek", font=font_ann, fill=(60, 110, 120))

    # ── Three-tier caption bar ────────────────────────────────────────────────
    font_t1   = load_font(13, bold=True)
    font_t2   = load_font(11, bold=False)
    font_t3   = load_font(9,  bold=False)
    font_meta = load_font(8,  bold=False)

    draw.rectangle([0, DRAW_H, PW, PH], fill=BG_CAPTION)
    draw.line([0, DRAW_H, PW, DRAW_H], fill=(8, 6, 4), width=2)

    # Tier 1 — Shot code
    draw.text((10, DRAW_H + 4),
              "P16  |  ECU  |  FLOOR-LEVEL  |  ONE EYE OPEN / TRACKING",
              font=font_t1, fill=TEXT_SHOT)

    # Tier 2 — Arc label
    draw.text((PW - 236, DRAW_H + 5),
              "ARC: TENSE / COMEDY", font=font_t2, fill=HOT_MAGENTA)

    # Tier 3 — Narrative description
    draw.text((10, DRAW_H + 22),
              "Luma face-to-floor. One eye open: tracking. Composure holds, then fractures.",
              font=font_t3, fill=TEXT_DESC)
    draw.text((10, DRAW_H + 35),
              '"...okay." then "...WHAT." — the punchline of the fall sequence.',
              font=font_t3, fill=(120, 112, 90))

    # Metadata
    draw.text((PW - 276, DRAW_H + 56),
              "LTG_SB_cold_open_P16  /  Diego Vargas  /  C46",
              font=font_meta, fill=TEXT_META)

    # Arc border — HOT_MAGENTA (TENSE/COMEDY)
    draw.rectangle([0, 0, PW - 1, PH - 1], outline=ARC_COLOR, width=4)

    img.thumbnail((1280, 1280))
    img.save(OUTPUT_PATH, "PNG")
    print(f"Saved: {OUTPUT_PATH}  {img.size}")
    return OUTPUT_PATH


if __name__ == "__main__":
    draw_panel()
    print("P16 standalone panel generation complete.")
    print("Beat: ECU — Luma face pressed to floor, one eye open, tracking.")
    print('"...okay." then "...WHAT." — composure holds, then fractures.')
    print("HOT_MAGENTA border. Cyan Byte-ambient glow on cheek.")
