#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_sb_cold_open_P10.py
Cold Open Panel P10 — OTS / Byte POV — Luma's Sleeping Face
Diego Vargas, Storyboard Artist — Cycle 44

Beat: Byte is floating just above and behind Luma's head.
      His POV — or near enough — looking down at her sleeping face.
      Byte as a cool silhouette in the foreground (camera-side edge).
      Luma warm and unaware in mid-frame. Cyan glow landing on her cheek
      from Byte's ambient field. The moment just before she wakes.

Shot:   OTS (Over-The-Shoulder) — Byte's shoulder/body partially in FG
Camera: High-rear — slightly elevated behind Byte, angling down toward Luma.
        Luma occupies mid-frame slightly left of center.
        Byte: cool dark silhouette RHS/FG — only partial, not full body.

Composition:
  - Byte silhouette: lower-right quadrant, partial. ELEC_CYAN rim lights only.
  - Luma: warm sleeping face, slight 3/4 angle (turned away from camera).
    Hair cloud from behind: larger-reading than front view.
    Couch pillow visible camera-left.
  - Cyan glow: directional from Byte-side (right), landing on Luma's left cheek.
  - Couch back/top just below Luma's head — grounds the spatial read.
  - Monitors in BG: soft grey-green static (defocused).

Byte (OTS silhouette):
  - Body: cool VOID_BLACK / ELEC_CYAN edges (rim light from his own glow).
  - Head: slightly cocked. No expression visible from this angle.
  - One pixel cluster visible on his back as 4-6 cyan irregular polys.

Luma (sleeping — BG warm):
  - Face: 3/4 rear-turned, slight downward tilt. Eyes closed.
  - Hair: from behind = wide dark cloud, soft edges. Cyan glow hits left side.
  - Hoodie: LUMA_HOODIE (#E8703A) visible at shoulders. Warm anchor color.
  - Expression: pure rest — no awareness yet (eyes closed, brow neutral).

Annotation:
  - Dotted sight-line from where Byte's eye would be to Luma's temple.
  - "BYTE POV — she doesn't know he's there"

Arc: TENSE / PRE-DISCOVERY — cyan border
Image size rule: ≤ 1280px in both dimensions.
Output: output/storyboards/panels/LTG_SB_cold_open_P10.png
"""

from PIL import Image, ImageDraw, ImageFont
import math, random, os

PANELS_DIR  = "/home/wipkat/team/output/storyboards/panels"
OUTPUT_PATH = os.path.join(PANELS_DIR, "LTG_SB_cold_open_P10.png")
os.makedirs(PANELS_DIR, exist_ok=True)

PW, PH    = 800, 600
CAPTION_H = 72          # Increased for 3-tier hierarchy (was 60)
DRAW_H    = PH - CAPTION_H   # 528

# ── Palette ──────────────────────────────────────────────────────────────────
WARM_CREAM   = (250, 240, 220)
WARM_AMB     = (212, 146, 58)
LUMA_SKIN    = (218, 172, 128)
LUMA_SKIN_SH = (185, 138, 92)
LUMA_HAIR    = (38, 22, 14)
LUMA_HOODIE  = (232, 112, 58)      # CANONICAL ORANGE — master_palette.md
COUCH_TOP    = (168, 122, 82)
COUCH_SHADOW = (128, 88, 56)
PILLOW_WARM  = (210, 180, 140)
WALL_WARM    = (228, 214, 188)
MONITOR_GREY = (140, 155, 138)
MONITOR_SCAN = (118, 132, 112)
MONITOR_PLST = (155, 148, 122)
# Byte / Glitch
VOID_BLACK   = (10, 10, 20)
ELEC_CYAN    = (0, 212, 232)
ELEC_CYAN_DIM= (0, 140, 160)
ELEC_CYAN_HI = (90, 248, 255)
HOT_MAGENTA  = (232, 0, 152)
BYTE_TEAL    = (0, 212, 232)
BYTE_BODY    = (12, 28, 38)        # Byte silhouette — near-black with cyan tint
# Caption
BG_CAPTION   = (12, 8, 6)
TEXT_SHOT    = (232, 224, 204)     # Tier 1 — shot code (largest/boldest)
TEXT_ARC     = ELEC_CYAN           # Tier 2 — arc label (colored per arc palette)
TEXT_DESC    = (155, 148, 122)     # Tier 3 — narrative description (smaller/lighter)
TEXT_META    = (88, 82, 66)        # File/artist metadata (smallest)
ARC_COLOR    = ELEC_CYAN           # TENSE/PRE-DISCOVERY
ANN_LINE     = (80, 200, 120)      # Annotation line color (sight-line)

RNG = random.Random(1010)


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


def draw_irregular_poly(draw, cx, cy, r, sides, color, seed=0, outline=None):
    """4-7 sided irregular polygon — Cycle 11 standard for all Glitchkin shapes."""
    lrng = random.Random(seed)
    pts = []
    for i in range(sides):
        angle = (2 * math.pi * i / sides) + lrng.uniform(-0.3, 0.3)
        dist  = r * lrng.uniform(0.65, 1.0)
        pts.append((cx + dist * math.cos(angle), cy + dist * math.sin(angle)))
    draw.polygon(pts, fill=color, outline=outline)


def draw_panel():
    img  = Image.new('RGB', (PW, PH), WARM_CREAM)
    draw = ImageDraw.Draw(img)

    # ── Background: warm room / couch zone ───────────────────────────────────
    # Room wall — warm faded cream with slight gradient
    draw.rectangle([0, 0, PW, DRAW_H], fill=WALL_WARM)

    # Background monitors — grey-green static (defocused, BG)
    for mi, (mx, my, mw, mh) in enumerate([
        (460, 20, 180, 140),
        (655, 30, 160, 130),
        (630, 175, 140, 110),
    ]):
        draw.rectangle([mx, my, mx + mw, my + mh], fill=MONITOR_PLST)
        draw.rectangle([mx + 8, my + 8, mx + mw - 8, my + mh - 8], fill=MONITOR_GREY)
        # Scanlines (defocused — subtle)
        for sy in range(my + 8, my + mh - 8, 4):
            draw.line([(mx + 8, sy), (mx + mw - 8, sy)], fill=MONITOR_SCAN, width=1)
    draw = ImageDraw.Draw(img)

    # Couch back — horizontal bar, warm brown
    couch_top_y = int(DRAW_H * 0.62)
    draw.rectangle([0, couch_top_y, PW, DRAW_H], fill=COUCH_TOP)
    draw.rectangle([0, couch_top_y, PW, couch_top_y + 12], fill=COUCH_SHADOW)

    # Pillow (camera-left)
    pillow_x0 = 0
    pillow_x1 = int(PW * 0.30)
    pillow_y0 = int(DRAW_H * 0.48)
    pillow_y1 = couch_top_y + 6
    draw.rectangle([pillow_x0, pillow_y0, pillow_x1, pillow_y1], fill=PILLOW_WARM)
    draw.rectangle([pillow_x0, pillow_y0, pillow_x1, pillow_y0 + 4],
                   fill=COUCH_SHADOW)

    # ── Luma — sleeping, 3/4 from behind, warm zone mid-frame ────────────────
    # Luma's head is turned slightly away — we mostly see the back/side of her head
    # and her right cheek (the side facing us, camera-side = right cheek from her body angle)
    head_cx = int(PW * 0.42)
    head_cy = int(DRAW_H * 0.42)
    head_r  = int(DRAW_H * 0.16)    # sizeable — she's in focus foreground-ish

    # Hair — large dark cloud from behind, slightly wider than head
    hair_w  = int(head_r * 1.6)
    hair_h  = int(head_r * 1.3)
    draw.ellipse([head_cx - hair_w, head_cy - hair_h,
                  head_cx + int(hair_w * 0.8), head_cy + int(hair_h * 0.5)],
                 fill=LUMA_HAIR)

    # Hoodie shoulders visible below hair
    shoulder_y = head_cy + head_r
    draw.rectangle([head_cx - int(head_r * 1.8), shoulder_y,
                    head_cx + int(head_r * 1.0), shoulder_y + int(head_r * 0.9)],
                   fill=LUMA_HOODIE)
    draw = ImageDraw.Draw(img)

    # Skin — right cheek partially visible (the bit facing camera)
    cheek_cx = head_cx + int(head_r * 0.25)
    cheek_cy = head_cy + int(head_r * 0.12)
    cheek_r  = int(head_r * 0.55)
    draw.ellipse([cheek_cx - cheek_r, cheek_cy - cheek_r,
                  cheek_cx + cheek_r, cheek_cy + cheek_r],
                 fill=LUMA_SKIN)

    # Jawline / neck (partial)
    draw.ellipse([cheek_cx - int(cheek_r * 0.6), cheek_cy + int(cheek_r * 0.5),
                  cheek_cx + int(cheek_r * 0.6), cheek_cy + int(cheek_r * 1.2)],
                 fill=LUMA_SKIN)

    # Closed eye hint (just a thin curved lid, visible on the cheek-facing side)
    eye_x = cheek_cx - int(cheek_r * 0.2)
    eye_y = cheek_cy - int(cheek_r * 0.12)
    eye_w = int(cheek_r * 0.55)
    draw.arc([eye_x - eye_w // 2, eye_y - 4, eye_x + eye_w // 2, eye_y + 4],
             start=200, end=340, fill=LUMA_SKIN_SH, width=2)

    # Slight bridge of nose visible
    draw.arc([cheek_cx - 4, cheek_cy - int(cheek_r * 0.3),
              cheek_cx + 4, cheek_cy + int(cheek_r * 0.1)],
             start=0, end=180, fill=LUMA_SKIN_SH, width=1)

    # Cyan glow on Luma's left cheek — from Byte's ambient field (right side of frame)
    add_glow(img, cheek_cx + int(cheek_r * 0.4), cheek_cy,
             int(head_r * 0.8), ELEC_CYAN, steps=8, max_alpha=38)
    draw = ImageDraw.Draw(img)

    # ── Byte silhouette — OTS, lower-right, partial body ─────────────────────
    # Only the back/head-side of Byte visible in FG — a cool dark mass with cyan rim.
    byte_cx = int(PW * 0.80)
    byte_cy = int(DRAW_H * 0.68)
    byte_r  = int(DRAW_H * 0.18)   # relatively large (close to camera)

    # Body: inverted teardrop silhouette — VOID_BLACK
    draw.ellipse([byte_cx - int(byte_r * 0.75), byte_cy - byte_r,
                  byte_cx + int(byte_r * 0.75), byte_cy + int(byte_r * 0.6)],
                 fill=BYTE_BODY)
    # Head bump (top)
    draw.ellipse([byte_cx - int(byte_r * 0.55), byte_cy - byte_r - int(byte_r * 0.55),
                  byte_cx + int(byte_r * 0.55), byte_cy - int(byte_r * 0.35)],
                 fill=BYTE_BODY)

    # Cyan rim light on Byte's left edge (facing camera / facing room)
    rim_layer = Image.new('RGBA', (PW, PH), (0, 0, 0, 0))
    rd = ImageDraw.Draw(rim_layer)
    rim_cx = byte_cx - int(byte_r * 0.55)
    for ri in range(6, 0, -1):
        r_rim = int(byte_r * 0.15 * ri / 6)
        a_rim = int(55 * (1 - ri / 7))
        rd.ellipse([rim_cx - r_rim, byte_cy - byte_r - r_rim,
                    rim_cx + r_rim, byte_cy + int(byte_r * 0.4) + r_rim],
                   fill=(*ELEC_CYAN, a_rim))
    img.paste(Image.alpha_composite(img.convert('RGBA'), rim_layer).convert('RGB'))
    draw = ImageDraw.Draw(img)

    # Pixel clusters on Byte's back — 4-5 irregular polys
    for pi in range(5):
        px = byte_cx + RNG.randint(-int(byte_r * 0.6), int(byte_r * 0.4))
        py = byte_cy - RNG.randint(int(byte_r * 0.1), int(byte_r * 0.7))
        pr = RNG.randint(3, 6)
        sides = RNG.randint(4, 6)
        c = ELEC_CYAN if RNG.random() < 0.7 else ELEC_CYAN_HI
        draw_irregular_poly(draw, px, py, pr, sides, c, seed=pi * 7 + 31)

    # Byte ambient glow — cool halo from the right side of frame
    add_glow(img, byte_cx, byte_cy, int(byte_r * 1.6), ELEC_CYAN,
             steps=10, max_alpha=28)
    draw = ImageDraw.Draw(img)

    # ── Panel annotations ─────────────────────────────────────────────────────
    font_ann  = load_font(9)
    font_sm   = load_font(8)

    # Sight-line annotation: from Byte's eye position to Luma's temple
    # Eye would be on Byte's left/front side — approximate from behind
    byte_eye_x = byte_cx - int(byte_r * 0.35)
    byte_eye_y = byte_cy - int(byte_r * 0.52)
    luma_temple_x = head_cx - int(head_r * 0.35)
    luma_temple_y = head_cy - int(head_r * 0.2)

    # Draw dotted sight-line
    total_dx = luma_temple_x - byte_eye_x
    total_dy = luma_temple_y - byte_eye_y
    total_dist = math.sqrt(total_dx**2 + total_dy**2)
    steps_sl = max(1, int(total_dist / 10))
    for si in range(steps_sl):
        t0 = si / steps_sl
        t1 = (si + 0.4) / steps_sl
        sx0 = int(byte_eye_x + total_dx * t0)
        sy0 = int(byte_eye_y + total_dy * t0)
        sx1 = int(byte_eye_x + total_dx * t1)
        sy1 = int(byte_eye_y + total_dy * t1)
        draw.line([(sx0, sy0), (sx1, sy1)], fill=ANN_LINE, width=1)

    draw.text((byte_eye_x - 80, byte_eye_y - 18),
              "BYTE POV", font=font_ann, fill=ELEC_CYAN_DIM)
    draw.text((byte_eye_x - 80, byte_eye_y - 8),
              "she doesn't know", font=font_sm, fill=(90, 110, 100))

    # Camera note
    draw.text((10, 8), "HIGH-REAR CAMERA", font=font_ann, fill=(95, 88, 72))
    draw.text((10, 20), "OTS / near-POV / elevated-behind", font=font_sm, fill=(75, 68, 55))

    # Glow annotation on Luma's cheek
    draw.text((cheek_cx + int(cheek_r * 0.5) + 6, cheek_cy - 6),
              "CYAN GLOW\nher cheek", font=font_sm, fill=ELEC_CYAN_DIM)

    # ── Three-tier caption bar ────────────────────────────────────────────────
    # Tier 1 — Shot code: largest + bold
    # Tier 2 — Arc label: arc-palette color (ELEC_CYAN for TENSE/PRE-DISCOVERY)
    # Tier 3 — Narrative description: smaller/lighter
    font_t1 = load_font(13, bold=True)   # Tier 1: largest/boldest
    font_t2 = load_font(11, bold=False)  # Tier 2: arc label, colored
    font_t3 = load_font(9,  bold=False)  # Tier 3: narrative description
    font_meta = load_font(8, bold=False) # File/artist metadata

    draw.rectangle([0, DRAW_H, PW, PH], fill=BG_CAPTION)
    draw.line([0, DRAW_H, PW, DRAW_H], fill=(8, 6, 4), width=2)

    # Tier 1 — Shot code (left, top of caption)
    draw.text((10, DRAW_H + 4),
              "P10  |  OTS  |  HIGH-REAR  |  BYTE POV",
              font=font_t1, fill=TEXT_SHOT)

    # Tier 2 — Arc label (right, top of caption — arc-colored)
    arc_label = "ARC: TENSE / PRE-DISCOVERY"
    draw.text((PW - 230, DRAW_H + 5),
              arc_label, font=font_t2, fill=TEXT_ARC)

    # Tier 3 — Narrative description (full width, middle row)
    draw.text((10, DRAW_H + 22),
              "Byte FG silhouette (cool). Luma BG warm, asleep, unaware. Cyan glow on cheek.",
              font=font_t3, fill=TEXT_DESC)

    # Tier 3 — second line (additional staging note)
    draw.text((10, DRAW_H + 35),
              "Dotted sight-line: Byte's eye pos → Luma's temple. BG monitors: grey-green static.",
              font=font_t3, fill=(120, 112, 90))

    # Metadata (bottom-right)
    draw.text((PW - 276, DRAW_H + 56),
              "LTG_SB_cold_open_P10  /  Diego Vargas  /  C44",
              font=font_meta, fill=TEXT_META)

    # Arc border (ELEC_CYAN — TENSE / PRE-DISCOVERY)
    draw.rectangle([0, 0, PW - 1, PH - 1], outline=ARC_COLOR, width=4)

    img.thumbnail((1280, 1280))
    img.save(OUTPUT_PATH, "PNG")
    print(f"Saved: {OUTPUT_PATH}  {img.size}")
    return OUTPUT_PATH


if __name__ == "__main__":
    make_path = draw_panel()
    print("P10 standalone panel generation complete.")
    print("Caption hierarchy: 3-tier (shot code / arc label / narrative description)")
    print("  Tier 1 — Shot code: bold 13pt")
    print("  Tier 2 — Arc label: ELEC_CYAN colored")
    print("  Tier 3 — Narrative: 9pt lighter")
