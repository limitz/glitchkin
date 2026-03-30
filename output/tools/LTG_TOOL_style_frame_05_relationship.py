#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_style_frame_05_relationship.py
Style Frame 05 — "The Passing" (Miri + Luma Relationship Key)
"Luma & the Glitchkin"

Author: Jordan Reed — Style Frame Art Specialist
Cycle: 44 (C44)

CONCEPT:
  The pitch package's missing intergenerational visual — independently flagged
  by Marcus Webb (74/100) and Eleanor Whitfield (74/100) at C17.

  "CRT as matrilineal heirloom — technology of seeing passed between women."
  (Alex Chen ideabox C44, carried as key concept.)

  Grandma Miri sits at the kitchen table in the pre-dawn morning quiet,
  watching the old CRT through the doorway as she does most mornings — it
  hums and casts its cool light into the warm kitchen. Luma has padded in
  quietly, still in her hoodie, and stands beside Miri's chair. Neither speaks.
  They both watch the screen together. Luma doesn't know yet what she is seeing.
  Miri does, because she came from there.

  "She came from here" — the show's core Miri truth, made visual.

STAGING:
  - Miri: left-of-center, seated at kitchen table, 3/4 back-right angle
    showing her profile toward the CRT. Terracotta rust cardigan. Silver bun.
    Her hands are folded on the table. Warm expression, eyes on the CRT.
  - Luma: right-of-Miri, standing, 3/4 left angle (faces same direction as Miri).
    Warm orange hoodie. Dark hair cloud. One hand rests lightly on the chair back.
    Her face: wide-eyed curiosity (RECOGNITION expression — not yet afraid).
  - CRT: through the doorway (far left), casting a cool desaturated blue-green
    glow into the kitchen. The glow is the primary cool source.
  - Kitchen: morning — warm amber top half, CRT cool bottom half.
    The warm-cool split is created by window light (top) vs CRT spill (bottom).

WARM/COOL STRATEGY (top-half/bottom-half, per QA tool measurement):
  - Top half: SUNLIT_AMBER overlay alpha=90 (morning window, upper-left)
  - Bottom half: CRT_COOL_SPILL alpha=85 (desaturated CRT glow from doorway)
  - Target separation ≥ 12.0 (past baseline is 13.2 for SF04)

FACE TEST GATE:
  Both Miri and Luma are drawn at pitch scale (head_r ≈ 38–42px).
  This exceeds the sprint-scale threshold (20–25px).
  Face test gate does NOT trigger at pitch scale per face_test_gate_policy.md.
  Face geometry is drawn at full fidelity regardless.

EMOTIONAL REGISTER:
  Warm, quiet, intergenerational. NOT action. NOT conflict.
  The camera is close enough to read both faces.
  Miri's face: WARM ATTENTION (she is watching, as she always watches).
  Luma's face: soft curiosity — slightly wider eyes than neutral, mouth
  slightly open. The "before" state — before she knows what the CRT means.

OUTPUT:
  /home/wipkat/team/output/color/style_frames/LTG_COLOR_styleframe_sf05.png
  1280×720 — native canvas, no thumbnail pass required (eliminates LANCZOS drift)

Usage:
  python3 output/tools/LTG_TOOL_style_frame_05_relationship.py

Author note on Miri hair accessory:
  The chopstick→hairpin replacement (FLAG 05, Priya Shah C43 brief) is pending
  Alex Chen + Maya Santos confirmation (status: "Decision pending" per Alex MEMORY C44).
  This generator uses the locked MIRI-A design (bun + chopstick pair per grandma_miri.md v1.2).
  The visual form is identical to hairpins — no change needed once Alex confirms.
  Variable named `hairpin_col` to future-proof the comment.
"""

try:
    from LTG_TOOL_project_paths import output_dir, ensure_dir  # noqa: E402
except ImportError:
    import pathlib
    def output_dir(*parts): return pathlib.Path("/home/wipkat/team/output").joinpath(*parts)
    def ensure_dir(path): path.mkdir(parents=True, exist_ok=True); return path
import os
import sys
import math
import random
from PIL import Image, ImageDraw, ImageFilter

_here = os.path.dirname(os.path.abspath(__file__))

OUTPUT_PATH = output_dir('color', 'style_frames', 'LTG_COLOR_styleframe_sf05.png')

W, H = 1280, 720

# ── Canonical Palette ─────────────────────────────────────────────────────────
# Real World — warm domestic (kitchen morning)
WARM_CREAM       = (250, 240, 220)
WALL_WARM        = (238, 218, 182)
WALL_SHADOW      = (190, 168, 136)
CEILING_WARM     = (242, 232, 208)
FLOOR_TILE_WARM  = (200, 184, 150)
FLOOR_TILE_DARK  = (178, 162, 130)
FLOOR_WORN_PATH  = (214, 200, 166)

# Deep shadows
DEEP_COCOA       = ( 59,  40,  32)   # #3B2820 — canonical line / deepest shadow
NEAR_BLACK_WARM  = ( 28,  18,  10)   # near-black crevices
SHADOW_DEEP      = ( 70,  48,  28)
SHADOW_MID       = (110,  78,  46)

# Lighting
SUNLIT_AMBER     = (212, 146,  58)   # canonical RW-03 — window top half
CRT_COOL_SPILL   = (  0, 130, 148)   # desaturated CRT glow — bottom half

# Kitchen props
WOOD_DARK        = (100,  65,  32)
WOOD_MED         = (148,  98,  52)
WOOD_LIGHT       = (186, 138,  78)
WOOD_WORN        = (170, 128,  70)   # worn wood surfaces
COUNTERTOP       = (190, 172, 138)
FRIDGE_WHITE     = (228, 222, 208)
STOVE_CREAM      = (220, 212, 196)
CURTAIN_WARM     = (230, 188, 118)
MUG_EARTHY       = (152, 104,  64)
PLANT_GREEN      = ( 76, 126,  60)

# CRT/doorway (far left)
DOORWAY_DARK     = (120, 100,  68)
DOORWAY_DEEP     = ( 55,  38,  22)
CRT_SCREEN_GLOW  = ( 42,  98, 118)   # desaturated CRT screen
CRT_BODY         = (108,  94,  74)

LINE_DARK        = ( 88,  60,  32)   # brown line work

# ── Miri color spec (grandma_miri.md v1.2) ────────────────────────────────────
MIRI_SKIN_BASE   = (140,  84,  48)   # #8C5430 Deep Warm Brown
MIRI_SKIN_SHADOW = (106,  58,  30)   # #6A3A1E Dark Sienna
MIRI_SKIN_HIGH   = (168, 106,  64)   # #A86A40 Warm Chestnut
MIRI_BLUSH       = (212, 149, 107)   # #D4956B Warm Blush (permanent, alpha=30)
MIRI_EYE_IRIS   = (139,  94,  60)   # #8B5E3C Deep Warm Amber
MIRI_EYE_PUPIL  = ( 26,  15,  10)   # #1A0F0A Near-Black Espresso
MIRI_EYE_WHITE  = (250, 240, 220)   # #FAF0DC Warm Cream
MIRI_EYE_HIGH   = (240, 240, 240)   # #F0F0F0 Static White
MIRI_HAIR_BASE  = (216, 208, 200)   # #D8D0C8 Silver White
MIRI_HAIR_SHAD  = (168, 152, 140)   # #A8988C Warm Gray
MIRI_HAIR_HIGH  = (240, 236, 232)   # #F0ECE8 Bright Near-White
MIRI_CARDIGAN   = (184,  92,  56)   # #B85C38 Warm Terracotta Rust
MIRI_CARD_SHAD  = (138,  60,  28)   # #8A3C1C Deep Rust
MIRI_CARD_HIGH  = (212, 130,  90)   # #D4825A Dusty Apricot
MIRI_PANTS      = (200, 174, 138)   # #C8AE8A Warm Linen Tan
MIRI_SLIPPER    = ( 90, 122,  90)   # #5A7A5A Deep Sage
MIRI_BROW       = (138, 122, 112)   # #8A7A70 Warm Gray brows
hairpin_col     = ( 92,  58,  32)   # dark warm wood — MIRI-A bun accessory
                                     # (named hairpin_col: FLAG 05 pending Alex confirmation
                                     # — visual form identical; rename only when confirmed)

# ── Luma color spec (canonical Real World appearance) ─────────────────────────
LUMA_SKIN       = (200, 136,  90)   # Warm Caramel #C8885A
LUMA_SKIN_SHAD  = (155,  95,  58)   # deeper shadow
LUMA_HAIR       = ( 59,  40,  32)   # Deep Cocoa — same as line color
LUMA_HAIR_HIGH  = ( 90,  60,  40)   # warm dark highlight
LUMA_HOODIE     = (232, 114,  42)   # Warm Orange #E8722A (Real World)
LUMA_HOODIE_SH  = (185,  82,  28)   # hoodie shadow
LUMA_HOODIE_H   = (255, 160,  80)   # hoodie highlight
LUMA_PANTS      = (120, 105,  88)   # warm grey pants
LUMA_SHOE       = ( 60,  50,  42)   # dark warm shoe
LUMA_EYE_IRIS  = (200, 125,  62)   # #C87D3E Warm Amber
LUMA_EYE_PUPIL = ( 59,  40,  32)   # Deep Cocoa
LUMA_EYE_WHITE = (250, 240, 220)   # Warm Cream
LUMA_EYE_HIGH  = (240, 240, 240)   # Static White (upper-left, matching Miri)
LUMA_BROW      = ( 59,  40,  32)   # same as hair
LUMA_BLUSH     = (220, 140,  90)   # situational blush (inactive in this quiet scene)


# ── Utilities ────────────────────────────────────────────────────────────────

def lerp(a, b, t):
    return a + (b - a) * t

def lerp_color(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

def alpha_over(img, x0, y0, x1, y1, color_rgb, alpha):
    """Draw a filled rectangle at given alpha using alpha_composite."""
    ov = Image.new("RGBA", img.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    od.rectangle([x0, y0, x1, y1], fill=(*color_rgb, alpha))
    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, ov)
    return img_rgba.convert("RGB")

def alpha_over_poly(img, pts, color_rgb, alpha):
    """Draw a filled polygon at given alpha using alpha_composite."""
    ov = Image.new("RGBA", img.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    od.polygon(pts, fill=(*color_rgb, alpha))
    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, ov)
    return img_rgba.convert("RGB")

def alpha_over_ellipse(img, bbox, color_rgb, alpha):
    """Draw a filled ellipse at given alpha."""
    ov = Image.new("RGBA", img.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    od.ellipse(bbox, fill=(*color_rgb, alpha))
    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, ov)
    return img_rgba.convert("RGB")

def gaussian_glow(img, cx, cy, radius, color_rgb, alpha_max):
    """Soft radial glow via alpha_composite."""
    ov = Image.new("RGBA", img.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    for r in range(radius, 0, -max(1, radius // 16)):
        t = 1.0 - (r / radius)
        a = int(alpha_max * (t ** 1.5))
        od.ellipse([cx - r, cy - r, cx + r, cy + r],
                   fill=(*color_rgb, a))
    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, ov)
    return img_rgba.convert("RGB")


# ── Layer 1: Kitchen Environment ──────────────────────────────────────────────

def draw_kitchen_bg(img):
    """
    Simplified kitchen interior — morning, pre-dawn.
    Camera: front-facing, slight 3/4 from center-right.
    Key elements: back wall (window), left wall (doorway to CRT room),
    kitchen table (FG), cabinets (right), ceiling, floor.

    Vanishing point: slightly left of center, upper-third.
    """
    draw = ImageDraw.Draw(img)

    VP_X = int(W * 0.38)
    VP_Y = int(H * 0.36)

    # ── Ceiling ───────────────────────────────────────────────────────────────
    ceil_poly = [
        (0, 0), (W, 0),
        (W, VP_Y - 30),
        (VP_X, VP_Y),
        (0, int(H * 0.20)),
    ]
    draw.polygon(ceil_poly, fill=CEILING_WARM)

    # ── Back wall ─────────────────────────────────────────────────────────────
    BW_LEFT  = int(W * 0.14)
    BW_RIGHT = int(W * 0.70)
    BW_TOP   = VP_Y
    BW_BOT   = int(H * 0.80)
    draw.rectangle([BW_LEFT, BW_TOP, BW_RIGHT, BW_BOT], fill=WALL_WARM)

    # ── Left wall (doorway side — CRT room) ───────────────────────────────────
    lw_poly = [
        (0, int(H * 0.20)),
        (BW_LEFT, BW_TOP),
        (BW_LEFT, BW_BOT),
        (0, int(H * 0.86)),
    ]
    draw.polygon(lw_poly, fill=WALL_SHADOW)

    # ── Right wall (cabinets) ─────────────────────────────────────────────────
    rw_poly = [
        (BW_RIGHT, BW_TOP),
        (W, VP_Y - 30),
        (W, int(H * 0.80)),
        (BW_RIGHT, BW_BOT),
    ]
    draw.polygon(rw_poly, fill=WALL_SHADOW)

    # ── Floor ─────────────────────────────────────────────────────────────────
    floor_poly = [
        (0, int(H * 0.86)),
        (BW_LEFT, BW_BOT),
        (BW_RIGHT, BW_BOT),
        (W, int(H * 0.80)),
        (W, H),
        (0, H),
    ]
    draw.polygon(floor_poly, fill=FLOOR_TILE_WARM)

    return draw, VP_X, VP_Y, BW_LEFT, BW_RIGHT, BW_TOP, BW_BOT


def draw_kitchen_details(img, draw, VP_X, VP_Y, BW_LEFT, BW_RIGHT, BW_TOP, BW_BOT):
    """
    Kitchen props: window (back wall), doorway with CRT (left),
    upper cabinets (right), table leg hint (FG left), mug on table.
    """
    # ── Window (back wall center-left) ────────────────────────────────────────
    WIN_L = BW_LEFT + int((BW_RIGHT - BW_LEFT) * 0.15)
    WIN_R = BW_LEFT + int((BW_RIGHT - BW_LEFT) * 0.52)
    WIN_T = BW_TOP + 20
    WIN_B = BW_BOT - 60
    # Window frame
    draw.rectangle([WIN_L, WIN_T, WIN_R, WIN_B], fill=CURTAIN_WARM)
    draw.rectangle([WIN_L + 8, WIN_T + 8, WIN_R - 8, WIN_B - 8],
                   fill=(180, 210, 230))   # pre-dawn blue sky
    # Curtain sides
    draw.rectangle([WIN_L, WIN_T, WIN_L + 14, WIN_B], fill=CURTAIN_WARM)
    draw.rectangle([WIN_R - 14, WIN_T, WIN_R, WIN_B], fill=CURTAIN_WARM)
    # Window sill
    draw.rectangle([WIN_L - 4, WIN_B, WIN_R + 4, WIN_B + 10], fill=WOOD_LIGHT)
    # Window cross bar
    draw.line([(WIN_L + 8, (WIN_T + WIN_B) // 2), (WIN_R - 8, (WIN_T + WIN_B) // 2)],
              fill=LINE_DARK, width=2)
    draw.line([((WIN_L + WIN_R) // 2, WIN_T + 8), ((WIN_L + WIN_R) // 2, WIN_B - 8)],
              fill=LINE_DARK, width=2)

    # ── Doorway (left wall — leads to CRT room) ───────────────────────────────
    DW_L = int(W * 0.002)
    DW_R = int(W * 0.115)
    DW_T = int(H * 0.28)
    DW_B = int(H * 0.83)
    # Adjacent room — warm shadow fill
    draw.rectangle([DW_L, DW_T, DW_R, DW_B], fill=DOORWAY_DARK)
    # CRT body (far room — small, far plane)
    crt_cx = int(DW_L + (DW_R - DW_L) * 0.45)
    crt_cy = int(DW_T + (DW_B - DW_T) * 0.50)
    crt_w = int((DW_R - DW_L) * 0.75)
    crt_h = int(crt_w * 0.70)
    # CRT TV body
    draw.rectangle([crt_cx - crt_w // 2, crt_cy - crt_h // 2,
                    crt_cx + crt_w // 2, crt_cy + crt_h // 2],
                   fill=CRT_BODY)
    # CRT screen (glowing)
    scr_pad = max(3, crt_w // 8)
    draw.rectangle([crt_cx - crt_w // 2 + scr_pad,
                    crt_cy - crt_h // 2 + scr_pad,
                    crt_cx + crt_w // 2 - scr_pad,
                    crt_cy + crt_h // 2 - scr_pad],
                   fill=CRT_SCREEN_GLOW)
    # Doorway frame
    draw.rectangle([DW_L, DW_T, DW_R, DW_T + 6], fill=WOOD_MED)
    draw.rectangle([DW_R - 6, DW_T, DW_R, DW_B], fill=WOOD_MED)

    # ── Upper cabinets (right wall) ───────────────────────────────────────────
    CAB_L = int(W * 0.72)
    CAB_T = int(H * 0.20)
    CAB_R = W
    CAB_B = int(H * 0.50)
    draw.rectangle([CAB_L, CAB_T, CAB_R, CAB_B], fill=WOOD_DARK)
    # Cabinet doors (3 panels)
    for i in range(3):
        dl = CAB_L + i * ((CAB_R - CAB_L) // 3) + 4
        dr = CAB_L + (i + 1) * ((CAB_R - CAB_L) // 3) - 4
        draw.rectangle([dl, CAB_T + 6, dr, CAB_B - 6], fill=WOOD_MED, outline=WOOD_DARK, width=1)

    # Lower cabinet / counter
    CTR_T = int(H * 0.55)
    draw.rectangle([CAB_L, CTR_T, CAB_R, int(H * 0.78)], fill=COUNTERTOP)
    draw.rectangle([CAB_L, CTR_T, CAB_R, CTR_T + 8], fill=WOOD_DARK)
    # Kitchen plant on counter
    plt_cx = int(W * 0.82)
    plt_cy = CTR_T - 18
    draw.ellipse([plt_cx - 14, plt_cy - 14, plt_cx + 14, plt_cy + 8], fill=PLANT_GREEN)
    draw.rectangle([plt_cx - 6, plt_cy + 2, plt_cx + 6, CTR_T], fill=MUG_EARTHY)

    # ── Kitchen table edge (foreground left) ──────────────────────────────────
    # Table is FG left — characters are seated AT this table
    TABLE_T  = int(H * 0.58)
    TABLE_B  = int(H * 0.68)
    TABLE_L  = 0
    TABLE_R  = int(W * 0.52)
    draw.rectangle([TABLE_L, TABLE_T, TABLE_R, TABLE_B], fill=WOOD_LIGHT)
    # Table edge / thickness
    draw.rectangle([TABLE_L, TABLE_B, TABLE_R, TABLE_B + 14], fill=WOOD_DARK)
    # Table top edge highlight
    draw.line([(TABLE_L, TABLE_T), (TABLE_R, TABLE_T)], fill=WOOD_WORN, width=2)

    # Miri's mug on table
    mug_cx = int(W * 0.18)
    mug_cy = TABLE_T + 6
    draw.ellipse([mug_cx - 9, mug_cy - 12, mug_cx + 9, mug_cy + 12], fill=MUG_EARTHY)
    draw.ellipse([mug_cx - 7, mug_cy - 10, mug_cx + 7, mug_cy], fill=(165, 118, 75))
    # Handle
    draw.arc([mug_cx + 7, mug_cy - 6, mug_cx + 18, mug_cy + 6],
             start=270, end=90, fill=LINE_DARK, width=2)

    return draw


def draw_floor_detail(img, draw):
    """Perspective floor lines — linoleum grid."""
    rng = random.Random(2219)
    FLOOR_TOP = int(H * 0.80)
    VP_X = int(W * 0.38)

    # Horizontal rows (non-linear spacing — perspective recession)
    n_rows = 7
    for i in range(n_rows + 1):
        t = (i / n_rows) ** 1.4
        row_y = int(FLOOR_TOP + t * (H - FLOOR_TOP))
        col = lerp_color(FLOOR_TILE_DARK, FLOOR_TILE_WARM, t * 0.6)
        draw.line([(0, row_y), (W, row_y)], fill=col, width=1)

    # Vertical converging lines from VP
    n_vert = 9
    for i in range(n_vert + 1):
        bx = int(i * W / n_vert)
        draw.line([(VP_X, FLOOR_TOP), (bx, H)],
                  fill=FLOOR_TILE_DARK, width=1)

    # Worn traffic path (warm stripe)
    draw.polygon(
        [(int(W * 0.08), FLOOR_TOP + 10), (int(W * 0.38), FLOOR_TOP + 10),
         (int(W * 0.55), H), (0, H)],
        fill=FLOOR_WORN_PATH
    )
    return draw


# ── Layer 2: CRT Glow Atmosphere ──────────────────────────────────────────────

def draw_crt_atmosphere(img):
    """
    CRT glow spill from doorway (far left) into kitchen.
    Creates the cool lower-half temperature zone needed for warm/cool QA PASS.
    """
    # CRT screen position in doorway (matching kitchen_details coordinates)
    crt_cx = int(0.002 * W + (0.115 * W - 0.002 * W) * 0.45)
    crt_cy = int(H * 0.28 + (H * 0.83 - H * 0.28) * 0.50)

    # Primary CRT glow — from doorway outward
    img = gaussian_glow(img, crt_cx, crt_cy,
                        radius=int(W * 0.38), color_rgb=CRT_COOL_SPILL, alpha_max=28)

    # Secondary: cool floor-level wash (bottom half of canvas)
    # Linear gradient from bottom edge up to H//2
    for y in range(H // 2, H):
        t = (y - H // 2) / (H // 2)     # 0 at midpoint, 1 at bottom
        alpha = int(85 * t)
        img = alpha_over(img, 0, y, W, y + 1, CRT_COOL_SPILL, alpha)

    return img


# ── Layer 3: Miri (seated, left-of-center) ────────────────────────────────────

def draw_miri(img, draw):
    """
    Grandma Miri — seated at kitchen table, 3/4 back-right angle.
    Miri faces slightly LEFT (toward the CRT / doorway).
    Head position: approximately (W*0.26, H*0.35)
    Total height at pitch scale: ~3.2 heads. head_r = 38px.

    Expression: WARM ATTENTION — eyes open 80%, gentle amused arch brow,
    closed upward mouth curve. She is watching the CRT, as she always does.
    """
    HEAD_R   = 38
    HEAD_CX  = int(W * 0.275)
    HEAD_CY  = int(H * 0.345)

    # ── Torso / Cardigan ─────────────────────────────────────────────────────
    # 3/4 seated: torso is wide, slightly foreshortened
    # Shoulder width ~ 1.1 × head (84px). Torso height ~ 1.05 heads from neck.
    NECK_TOP = HEAD_CY + HEAD_R + 2
    TORSO_W  = int(HEAD_R * 2.3)         # slightly wider — wide settled cardigan
    TORSO_H  = int(HEAD_R * 1.8)         # foreshortened — she's seated
    TORSO_CX = HEAD_CX - int(HEAD_R * 0.08)  # slight left offset (3/4 view)

    # Main cardigan body
    draw.ellipse(
        [TORSO_CX - TORSO_W // 2, NECK_TOP,
         TORSO_CX + TORSO_W // 2, NECK_TOP + TORSO_H],
        fill=MIRI_CARDIGAN
    )
    draw = ImageDraw.Draw(img)  # refresh after any paste

    # Cardigan shadow (lower torso and sides)
    card_shad_pts = [
        (TORSO_CX - TORSO_W // 2, NECK_TOP + TORSO_H // 2),
        (TORSO_CX - TORSO_W // 2 + 8, NECK_TOP + TORSO_H),
        (TORSO_CX + TORSO_W // 2 - 8, NECK_TOP + TORSO_H),
        (TORSO_CX + TORSO_W // 2, NECK_TOP + TORSO_H // 2),
    ]
    img = alpha_over_poly(img, card_shad_pts, MIRI_CARD_SHAD, 120)
    draw = ImageDraw.Draw(img)

    # Cardigan highlight (shoulder ridge)
    draw.arc(
        [TORSO_CX - TORSO_W // 2 + 4, NECK_TOP,
         TORSO_CX + TORSO_W // 2 - 4, NECK_TOP + TORSO_H // 2],
        start=200, end=340, fill=MIRI_CARD_HIGH, width=3
    )

    # Cable-knit texture hint (vertical lines)
    for ox in [-int(TORSO_W * 0.25), 0, int(TORSO_W * 0.25)]:
        x = TORSO_CX + ox
        draw.line(
            [(x, NECK_TOP + 10), (x, NECK_TOP + TORSO_H - 10)],
            fill=MIRI_CARD_SHAD, width=1
        )

    # Arms folded on table — forearms extend forward (toward camera)
    # Left arm (far side — thinner, behind right)
    ARM_Y   = NECK_TOP + TORSO_H - 10
    draw.ellipse(
        [TORSO_CX - TORSO_W // 2 - 12, ARM_Y - 8,
         TORSO_CX - 8, ARM_Y + 20],
        fill=MIRI_CARDIGAN
    )
    draw = ImageDraw.Draw(img)

    # Right arm/hand on table
    draw.ellipse(
        [TORSO_CX - 20, ARM_Y - 6,
         TORSO_CX + TORSO_W // 4, ARM_Y + 22],
        fill=MIRI_CARDIGAN
    )
    draw = ImageDraw.Draw(img)

    # Hands (folded, visible at table surface)
    HAND_Y = int(H * 0.583)
    draw.ellipse(
        [TORSO_CX - 26, HAND_Y - 8,
         TORSO_CX + 8, HAND_Y + 14],
        fill=MIRI_SKIN_BASE
    )
    draw = ImageDraw.Draw(img)
    draw.ellipse(
        [TORSO_CX - 8, HAND_Y - 6,
         TORSO_CX + 24, HAND_Y + 12],
        fill=MIRI_SKIN_HIGH
    )
    draw = ImageDraw.Draw(img)
    # Knuckle suggestion
    for kx in [TORSO_CX - 14, TORSO_CX - 6, TORSO_CX + 2, TORSO_CX + 10]:
        draw.arc([kx - 4, HAND_Y - 4, kx + 4, HAND_Y + 4],
                 start=0, end=180, fill=LINE_DARK, width=1)

    # ── Head ─────────────────────────────────────────────────────────────────
    # Head is slightly compressed (88% circle — per grandma_miri.md spec)
    head_rx = HEAD_R
    head_ry = int(HEAD_R * 0.90)
    draw.ellipse(
        [HEAD_CX - head_rx, HEAD_CY - head_ry,
         HEAD_CX + head_rx, HEAD_CY + head_ry],
        fill=MIRI_SKIN_BASE
    )
    draw = ImageDraw.Draw(img)

    # Neck
    NECK_W = int(HEAD_R * 0.42)
    draw.rectangle(
        [HEAD_CX - NECK_W // 2, HEAD_CY + head_ry - 4,
         HEAD_CX + NECK_W // 2, NECK_TOP + 8],
        fill=MIRI_SKIN_BASE
    )
    draw = ImageDraw.Draw(img)

    # ── Cheek blush (permanent) ───────────────────────────────────────────────
    # Miri's permanent blush: MIRI_BLUSH at ~25% opacity
    # In this frame: Luma is in quiet-curiosity state (not excited blush active)
    # → No Pride Override needed. Full blush at 25%.
    BLUSH_ALPHA = 32   # ≈ 25% of 128-feeling
    img = alpha_over_ellipse(
        img,
        [HEAD_CX - head_rx + 4,  HEAD_CY - 2,
         HEAD_CX - head_rx + 28, HEAD_CY + 18],
        MIRI_BLUSH, BLUSH_ALPHA
    )
    img = alpha_over_ellipse(
        img,
        [HEAD_CX + head_rx - 28, HEAD_CY - 2,
         HEAD_CX + head_rx - 4,  HEAD_CY + 18],
        MIRI_BLUSH, BLUSH_ALPHA
    )
    draw = ImageDraw.Draw(img)

    # Skin shadow (jaw and temple)
    img = alpha_over_ellipse(
        img,
        [HEAD_CX - head_rx, HEAD_CY,
         HEAD_CX - head_rx + 20, HEAD_CY + head_ry],
        MIRI_SKIN_SHADOW, 80
    )
    draw = ImageDraw.Draw(img)

    # ── Hair (silver bun) ─────────────────────────────────────────────────────
    # Bun sits at upper-back of head, adds ~0.25 heads height
    BUN_CX = HEAD_CX + int(HEAD_R * 0.12)
    BUN_CY = HEAD_CY - head_ry + int(HEAD_R * 0.05)
    BUN_RX = int(HEAD_R * 0.55)
    BUN_RY = int(HEAD_R * 0.48)
    draw.ellipse(
        [BUN_CX - BUN_RX, BUN_CY - BUN_RY,
         BUN_CX + BUN_RX, BUN_CY + BUN_RY],
        fill=MIRI_HAIR_BASE
    )
    draw = ImageDraw.Draw(img)
    # Bun shadow (inner depth)
    img = alpha_over_ellipse(
        img,
        [BUN_CX - BUN_RX + 4, BUN_CY,
         BUN_CX + BUN_RX - 4, BUN_CY + BUN_RY - 2],
        MIRI_HAIR_SHAD, 140
    )
    draw = ImageDraw.Draw(img)
    # Bun highlight
    img = alpha_over_ellipse(
        img,
        [BUN_CX - BUN_RX + 6, BUN_CY - BUN_RY + 4,
         BUN_CX, BUN_CY],
        MIRI_HAIR_HIGH, 100
    )
    draw = ImageDraw.Draw(img)

    # Side hair arc (the part that pulls back from forehead)
    draw.arc(
        [HEAD_CX - head_rx, HEAD_CY - head_ry,
         HEAD_CX + head_rx, HEAD_CY + int(head_ry * 0.3)],
        start=195, end=345, fill=MIRI_HAIR_BASE,
        width=max(3, int(HEAD_R * 0.38))
    )
    draw = ImageDraw.Draw(img)

    # Escaping wispy curls (2–3 strands at temple)
    wisp_pts = [
        (HEAD_CX - head_rx + 4, HEAD_CY - int(head_ry * 0.3)),
        (HEAD_CX - head_rx - 5, HEAD_CY + 4),
        (HEAD_CX - head_rx + 2, HEAD_CY + 14),
    ]
    draw.line(wisp_pts, fill=MIRI_HAIR_SHAD, width=1)

    # ── Hairpins (MIRI-A design — FLAG 05 pending replacement confirmation) ──
    # Two slender elements at angles from bun — same visual form as wooden hairpins
    HP_ANGLE1 = math.radians(-30)
    HP_ANGLE2 = math.radians(10)
    HP_LEN    = int(HEAD_R * 0.65)
    for angle in [HP_ANGLE1, HP_ANGLE2]:
        hx = BUN_CX + int(HP_LEN * math.cos(angle))
        hy = BUN_CY + int(HP_LEN * math.sin(angle))
        draw.line([(BUN_CX, BUN_CY), (hx, hy)],
                  fill=hairpin_col, width=2)

    # ── Face — WARM ATTENTION expression ─────────────────────────────────────
    # Eyes: 80% aperture (calm, steady, watching)
    # Miri's eyes: eye_r = 0.16 × head_width. head_r=38 → eye_r ≈ 6px.
    # At pitch scale this is above sprint threshold — full fidelity.

    EYE_R    = max(5, int(HEAD_R * 0.165))
    EYE_Y    = HEAD_CY - int(head_ry * 0.15)
    EYE_X_L  = HEAD_CX - int(HEAD_R * 0.35)
    EYE_X_R  = HEAD_CX + int(HEAD_R * 0.35)

    for EX, LID_FRAC in [(EYE_X_L, 0.75), (EYE_X_R, 0.80)]:
        # Sclera
        draw.ellipse([EX - EYE_R, EYE_Y - EYE_R,
                      EX + EYE_R, EYE_Y + EYE_R],
                     fill=MIRI_EYE_WHITE)
        draw = ImageDraw.Draw(img)
        # Iris (slightly warm amber — deeper than Luma's)
        iris_r = max(3, EYE_R - 1)
        draw.ellipse([EX - iris_r, EYE_Y - iris_r,
                      EX + iris_r, EYE_Y + iris_r],
                     fill=MIRI_EYE_IRIS)
        draw = ImageDraw.Draw(img)
        # Pupil
        pupil_r = max(2, iris_r - 2)
        draw.ellipse([EX - pupil_r, EYE_Y - pupil_r,
                      EX + pupil_r, EYE_Y + pupil_r],
                     fill=MIRI_EYE_PUPIL)
        draw = ImageDraw.Draw(img)
        # Highlight — upper-left (shared DNA with Luma)
        hl_off = max(1, pupil_r // 2)
        draw.ellipse([EX - hl_off - 1, EYE_Y - hl_off - 1,
                      EX - hl_off + 1, EYE_Y - hl_off + 1],
                     fill=MIRI_EYE_HIGH)
        draw = ImageDraw.Draw(img)
        # Upper eyelid — slightly heavy (weighted, calm look)
        lid_y = EYE_Y - int(EYE_R * LID_FRAC)
        draw.arc([EX - EYE_R, EYE_Y - EYE_R, EX + EYE_R, EYE_Y + EYE_R],
                 start=200, end=340, fill=MIRI_SKIN_BASE,
                 width=max(2, EYE_R // 3))
        draw = ImageDraw.Draw(img)
        # Crow's feet (outer corner — 50% line weight)
        cw_x = EX + EYE_R if EX == EYE_X_R else EX - EYE_R
        cw_sign = 1 if EX == EYE_X_R else -1
        draw.line(
            [(cw_x, EYE_Y),
             (cw_x + cw_sign * 6, EYE_Y - 3)],
            fill=DEEP_COCOA, width=1
        )
        draw.line(
            [(cw_x, EYE_Y),
             (cw_x + cw_sign * 5, EYE_Y + 3)],
            fill=DEEP_COCOA, width=1
        )

    # ── Eyebrows (gentle arch — Warm Gray, narrower than Luma's) ─────────────
    BROW_Y = HEAD_CY - int(head_ry * 0.50)
    BROW_W = int(HEAD_R * 0.30)
    for bx in [EYE_X_L, EYE_X_R]:
        # Gentle arch — outer end very slightly higher
        draw.line(
            [(bx - BROW_W, BROW_Y + 2),
             (bx, BROW_Y),
             (bx + BROW_W, BROW_Y + 2)],
            fill=MIRI_BROW, width=1
        )
        draw = ImageDraw.Draw(img)

    # ── Smile lines (always present) ─────────────────────────────────────────
    for mx in [EYE_X_L, EYE_X_R]:
        sm_sign = 1 if mx == EYE_X_R else -1
        draw.arc(
            [mx - int(HEAD_R * 0.18), HEAD_CY + 4,
             mx + int(HEAD_R * 0.18), HEAD_CY + int(head_ry * 0.65)],
            start=30 if sm_sign == 1 else 150,
            end=100 if sm_sign == 1 else 220,
            fill=MIRI_SKIN_SHADOW, width=1
        )
        draw = ImageDraw.Draw(img)

    # ── Mouth — closed upward curve (natural resting warmth) ─────────────────
    MOUTH_Y = HEAD_CY + int(head_ry * 0.42)
    MOUTH_W = int(HEAD_R * 0.36)
    draw.arc(
        [HEAD_CX - MOUTH_W, MOUTH_Y - 5,
         HEAD_CX + MOUTH_W, MOUTH_Y + 5],
        start=10, end=170, fill=DEEP_COCOA, width=2
    )
    draw = ImageDraw.Draw(img)

    # ── Nose — button with bridge line (3/4 view) ─────────────────────────────
    NOSE_Y = HEAD_CY + int(head_ry * 0.08)
    # Nostril pair (slight flare)
    draw.arc(
        [HEAD_CX - 10, NOSE_Y - 4, HEAD_CX + 10, NOSE_Y + 6],
        start=180, end=360, fill=MIRI_SKIN_SHADOW, width=1
    )
    draw = ImageDraw.Draw(img)

    # ── Outline (silhouette line) ─────────────────────────────────────────────
    draw.ellipse(
        [HEAD_CX - head_rx, HEAD_CY - head_ry,
         HEAD_CX + head_rx, HEAD_CY + head_ry],
        outline=DEEP_COCOA, width=2
    )
    draw = ImageDraw.Draw(img)

    return img, draw


# ── Layer 4: Luma (standing, right-of-Miri) ───────────────────────────────────

def draw_luma(img, draw):
    """
    Luma — standing behind/beside Miri's chair, right of frame.
    She faces the same direction as Miri (left, toward the CRT).
    3/4 angle showing left face (slight profile).

    Head position: approximately (W*0.52, H*0.28)
    She is slightly taller than Miri: head_r = 40px.
    One hand rests lightly on the chair back.

    Expression: wide-eyed quiet curiosity (not yet afraid).
    Eyes: slightly wider than neutral, brows gently raised,
    mouth slightly open — the "I'm watching something I don't understand yet" face.
    """
    HEAD_R   = 40
    HEAD_CX  = int(W * 0.520)
    HEAD_CY  = int(H * 0.280)

    # ── Body (hoodie) ─────────────────────────────────────────────────────────
    NECK_TOP = HEAD_CY + HEAD_R + 2
    TORSO_W  = int(HEAD_R * 2.05)
    TORSO_H  = int(HEAD_R * 2.60)    # full standing torso
    TORSO_CX = HEAD_CX + int(HEAD_R * 0.05)

    # Main hoodie body
    draw.ellipse(
        [TORSO_CX - TORSO_W // 2, NECK_TOP,
         TORSO_CX + TORSO_W // 2, NECK_TOP + TORSO_H],
        fill=LUMA_HOODIE
    )
    draw = ImageDraw.Draw(img)

    # Hoodie shadow (lower torso, left side — 3/4 angle shading)
    img = alpha_over_poly(img, [
        (TORSO_CX - TORSO_W // 2, NECK_TOP + TORSO_H // 3),
        (TORSO_CX - TORSO_W // 2 + 10, NECK_TOP + TORSO_H),
        (TORSO_CX + TORSO_W // 4, NECK_TOP + TORSO_H),
        (TORSO_CX + TORSO_W // 4, NECK_TOP + TORSO_H // 3),
    ], LUMA_HOODIE_SH, 130)
    draw = ImageDraw.Draw(img)

    # Hoodie highlight (right shoulder)
    img = alpha_over_ellipse(img, [
        TORSO_CX,                    NECK_TOP,
        TORSO_CX + TORSO_W // 2 - 4, NECK_TOP + TORSO_H // 3,
    ], LUMA_HOODIE_H, 70)
    draw = ImageDraw.Draw(img)

    # Left arm (foreground — extends down toward chair back)
    ARM_L = TORSO_CX - TORSO_W // 2 - 6
    ARM_T = NECK_TOP + TORSO_H // 4
    ARM_W = int(HEAD_R * 0.72)
    ARM_H = int(HEAD_R * 1.55)
    draw.ellipse(
        [ARM_L, ARM_T, ARM_L + ARM_W, ARM_T + ARM_H],
        fill=LUMA_HOODIE
    )
    draw = ImageDraw.Draw(img)

    # Hand on chair back
    HAND_CX = ARM_L + ARM_W // 2
    HAND_CY = ARM_T + ARM_H
    draw.ellipse(
        [HAND_CX - 12, HAND_CY - 10,
         HAND_CX + 14, HAND_CY + 14],
        fill=LUMA_SKIN
    )
    draw = ImageDraw.Draw(img)

    # Legs (below table — partially occluded by table FG)
    LEG_TOP = NECK_TOP + TORSO_H - 4
    LEG_W   = int(HEAD_R * 0.56)
    for lx in [TORSO_CX - LEG_W, TORSO_CX + LEG_W // 4]:
        draw.ellipse(
            [lx - LEG_W // 2, LEG_TOP,
             lx + LEG_W // 2, LEG_TOP + int(HEAD_R * 1.2)],
            fill=LUMA_PANTS
        )
        draw = ImageDraw.Draw(img)

    # ── Head ─────────────────────────────────────────────────────────────────
    draw.ellipse(
        [HEAD_CX - HEAD_R, HEAD_CY - HEAD_R,
         HEAD_CX + HEAD_R, HEAD_CY + HEAD_R],
        fill=LUMA_SKIN
    )
    draw = ImageDraw.Draw(img)

    # Neck
    NECK_W = int(HEAD_R * 0.40)
    draw.rectangle(
        [HEAD_CX - NECK_W // 2, HEAD_CY + HEAD_R - 4,
         HEAD_CX + NECK_W // 2, NECK_TOP + 8],
        fill=LUMA_SKIN
    )
    draw = ImageDraw.Draw(img)

    # Skin shadow (left temple, jaw — 3/4 facing left)
    img = alpha_over_ellipse(img, [
        HEAD_CX - HEAD_R, HEAD_CY - int(HEAD_R * 0.4),
        HEAD_CX - HEAD_R + 22, HEAD_CY + HEAD_R,
    ], LUMA_SKIN_SHAD, 90)
    draw = ImageDraw.Draw(img)

    # ── Hair (explosive dark cloud) ───────────────────────────────────────────
    # Dark hair arc over top-back of head, with escaping curls
    rng = random.Random(4471)
    # Main hair mass — arc + cloud blobs
    draw.arc(
        [HEAD_CX - HEAD_R - 12, HEAD_CY - HEAD_R - 8,
         HEAD_CX + HEAD_R + 8,  HEAD_CY + int(HEAD_R * 0.5)],
        start=170, end=350, fill=LUMA_HAIR,
        width=max(4, int(HEAD_R * 0.55))
    )
    draw = ImageDraw.Draw(img)
    # Hair cloud blobs (seeded for reproducibility)
    hair_blobs = [
        (HEAD_CX + int(HEAD_R * 0.60), HEAD_CY - HEAD_R + 4, int(HEAD_R * 0.36)),
        (HEAD_CX - int(HEAD_R * 0.55), HEAD_CY - HEAD_R + 2, int(HEAD_R * 0.40)),
        (HEAD_CX + int(HEAD_R * 0.10), HEAD_CY - HEAD_R - 10, int(HEAD_R * 0.30)),
        (HEAD_CX - int(HEAD_R * 0.22), HEAD_CY - HEAD_R + 8, int(HEAD_R * 0.28)),
    ]
    for bx, by, br in hair_blobs:
        draw.ellipse([bx - br, by - br, bx + br, by + br], fill=LUMA_HAIR)
        draw = ImageDraw.Draw(img)
    # Hair highlight
    draw.arc(
        [HEAD_CX - int(HEAD_R * 0.6), HEAD_CY - HEAD_R - 4,
         HEAD_CX + int(HEAD_R * 0.6), HEAD_CY - int(HEAD_R * 0.4)],
        start=215, end=320, fill=LUMA_HAIR_HIGH, width=2
    )
    draw = ImageDraw.Draw(img)

    # ── Eyes — wide quiet curiosity ───────────────────────────────────────────
    # Luma's eyes: eye_r = 0.22 × head_width → EYE_R = int(40*0.22) = 8px
    EYE_R   = max(7, int(HEAD_R * 0.22))
    EYE_Y   = HEAD_CY - int(HEAD_R * 0.14)
    EYE_X_L = HEAD_CX - int(HEAD_R * 0.36)
    EYE_X_R = HEAD_CX + int(HEAD_R * 0.36)

    # Slightly wider than neutral (curiosity — both same size, symmetric open)
    for EX in [EYE_X_L, EYE_X_R]:
        draw.ellipse([EX - EYE_R, EYE_Y - EYE_R,
                      EX + EYE_R, EYE_Y + EYE_R],
                     fill=LUMA_EYE_WHITE)
        draw = ImageDraw.Draw(img)
        iris_r = max(5, EYE_R - 1)
        draw.ellipse([EX - iris_r, EYE_Y - iris_r,
                      EX + iris_r, EYE_Y + iris_r],
                     fill=LUMA_EYE_IRIS)
        draw = ImageDraw.Draw(img)
        pupil_r = max(3, iris_r - 2)
        # Gaze: slightly LEFT (toward the CRT)
        GAZE_DX = -int(pupil_r * 0.30)
        draw.ellipse(
            [EX + GAZE_DX - pupil_r, EYE_Y - pupil_r,
             EX + GAZE_DX + pupil_r, EYE_Y + pupil_r],
            fill=LUMA_EYE_PUPIL
        )
        draw = ImageDraw.Draw(img)
        # Highlight — upper-left (matching Miri's highlight position = visual DNA)
        hl_r = max(1, pupil_r // 2 - 1)
        draw.ellipse(
            [EX - pupil_r, EYE_Y - pupil_r,
             EX - pupil_r + hl_r * 2, EYE_Y - pupil_r + hl_r * 2],
            fill=LUMA_EYE_HIGH
        )
        draw = ImageDraw.Draw(img)

    # ── Eyebrows — gently raised (curiosity/wonder) ───────────────────────────
    BROW_Y = HEAD_CY - int(HEAD_R * 0.48)
    BROW_W = int(HEAD_R * 0.38)
    # Thick graphic brows (Luma's signature — brow_w = 0.30 × head)
    for bx in [EYE_X_L, EYE_X_R]:
        # Raised outer end — gently curious arch
        draw.line(
            [(bx - BROW_W, BROW_Y + 3),
             (bx, BROW_Y - 1),
             (bx + BROW_W, BROW_Y + 3)],
            fill=LUMA_BROW, width=2
        )
        draw = ImageDraw.Draw(img)

    # ── Mouth — slightly open (curiosity — not yet speaking) ──────────────────
    MOUTH_Y = HEAD_CY + int(HEAD_R * 0.40)
    MOUTH_W = int(HEAD_R * 0.28)
    MOUTH_H = int(HEAD_R * 0.12)
    draw.arc(
        [HEAD_CX - MOUTH_W, MOUTH_Y - MOUTH_H,
         HEAD_CX + MOUTH_W, MOUTH_Y + MOUTH_H],
        start=195, end=345, fill=DEEP_COCOA, width=2
    )
    draw = ImageDraw.Draw(img)
    # Slight parting — upper lip arc
    draw.arc(
        [HEAD_CX - MOUTH_W + 6, MOUTH_Y - MOUTH_H - 3,
         HEAD_CX + MOUTH_W - 6, MOUTH_Y - 2],
        start=15, end=165, fill=DEEP_COCOA, width=1
    )
    draw = ImageDraw.Draw(img)

    # ── Nose — apostrophe dot (Luma spec) ─────────────────────────────────────
    NOSE_Y = HEAD_CY + int(HEAD_R * 0.08)
    draw.ellipse(
        [HEAD_CX - 3, NOSE_Y - 3, HEAD_CX + 3, NOSE_Y + 3],
        fill=LUMA_SKIN_SHAD
    )
    draw = ImageDraw.Draw(img)

    # ── Head outline ──────────────────────────────────────────────────────────
    draw.ellipse(
        [HEAD_CX - HEAD_R, HEAD_CY - HEAD_R,
         HEAD_CX + HEAD_R, HEAD_CY + HEAD_R],
        outline=DEEP_COCOA, width=2
    )
    draw = ImageDraw.Draw(img)

    return img, draw


# ── Layer 5: Warm Lighting (top-half SUNLIT_AMBER overlay) ───────────────────

def draw_warm_lighting(img):
    """
    Morning window light from upper-left — creates warm top half.
    Linear alpha from 0 at top to 90 at H//2, then flat 0 below.
    """
    for y in range(0, H // 2):
        t = y / (H // 2)
        alpha = int(90 * t)
        img = alpha_over(img, 0, y, W, y + 1, SUNLIT_AMBER, alpha)
    return img


# ── Layer 6: Character Lighting ───────────────────────────────────────────────

def draw_character_lighting(img):
    """
    CRT glow brightens faces (cool fill from left).
    Window light warms the right side of both characters.
    These are atmospheric light passes — not explicit rim lights.
    """
    # CRT light hits left sides of faces — subtle cool overlay on left 40% of canvas
    # (this is already handled by CRT atmosphere layer; keep light here)
    # Warm window right-side fill on Luma and Miri — faint warm glow
    img = gaussian_glow(img,
                        cx=int(W * 0.38), cy=int(H * 0.25),
                        radius=int(H * 0.30),
                        color_rgb=SUNLIT_AMBER, alpha_max=18)
    return img


# ── Layer 7: Deep Shadow Anchors ─────────────────────────────────────────────

def draw_deep_shadows(img, draw):
    """
    Force value floor ≤ 30. Deep shadow anchors MUST run after all light passes.
    Per C35 critical lesson: light passes add brightness to near-black pixels —
    shadow must be LAST structural pass before atmosphere.
    """
    # Under-table shadow (deep foreground crevice)
    img = alpha_over(img,
                     0, int(H * 0.68), int(W * 0.52), int(H * 0.72),
                     NEAR_BLACK_WARM, 220)
    draw = ImageDraw.Draw(img)

    # Left corner (deepest shadow — wall meets doorway)
    draw.polygon(
        [(0, int(H * 0.30)), (0, int(H * 0.90)),
         (int(W * 0.04), int(H * 0.90)), (int(W * 0.04), int(H * 0.30))],
        fill=NEAR_BLACK_WARM
    )
    draw = ImageDraw.Draw(img)

    # Right corner (cabinet undersides + floor crevice)
    draw.polygon(
        [(W, int(H * 0.78)), (W, H),
         (int(W * 0.90), H), (int(W * 0.90), int(H * 0.78))],
        fill=NEAR_BLACK_WARM
    )
    draw = ImageDraw.Draw(img)

    # Floor far edge (deepest recession)
    draw.rectangle([0, int(H * 0.94), W, H], fill=NEAR_BLACK_WARM)
    draw = ImageDraw.Draw(img)

    # Under-counter shadow (right wall bottom)
    draw.rectangle([int(W * 0.72), int(H * 0.75), W, int(H * 0.82)],
                   fill=SHADOW_DEEP)
    draw = ImageDraw.Draw(img)

    # Ceiling-wall junctions (dark crevices at top corners)
    draw.polygon(
        [(0, 0), (int(W * 0.06), 0),
         (int(W * 0.06), int(H * 0.06)), (0, int(H * 0.14))],
        fill=NEAR_BLACK_WARM
    )
    draw = ImageDraw.Draw(img)
    draw.polygon(
        [(W - int(W * 0.06), 0), (W, 0),
         (W, int(H * 0.08)), (W - int(W * 0.06), int(H * 0.04))],
        fill=NEAR_BLACK_WARM
    )
    draw = ImageDraw.Draw(img)

    return img, draw


# ── Layer 7b: Value Ceiling Anchors ──────────────────────────────────────────

def draw_specular_highlights(img, draw):
    """
    Force value ceiling ≥ 225. Specular dots on window glass and mug rim.
    Applied BEFORE atmosphere so vignette doesn't clip them below threshold.
    """
    SPECULAR_WHITE = (255, 255, 250)

    # Window glass catchlights (upper-left of each pane)
    WIN_L = int(W * 0.14) + int((W * 0.70 - W * 0.14) * 0.15) + 8
    WIN_T = int(H * 0.36) + 8
    WIN_R_L = int(W * 0.14) + int((W * 0.70 - W * 0.14) * 0.52) - 8
    WIN_MID_X = (WIN_L + WIN_R_L) // 2

    # Left pane specular
    draw.ellipse([WIN_L + 4, WIN_T + 4, WIN_L + 14, WIN_T + 14],
                 fill=SPECULAR_WHITE)
    draw = ImageDraw.Draw(img)
    # Right pane specular
    draw.ellipse([WIN_MID_X + 6, WIN_T + 4, WIN_MID_X + 16, WIN_T + 14],
                 fill=SPECULAR_WHITE)
    draw = ImageDraw.Draw(img)

    # Mug rim specular
    MUG_CX = int(W * 0.18)
    MUG_CY = int(H * 0.58) + 6 - 12
    draw.ellipse([MUG_CX - 3, MUG_CY - 11, MUG_CX + 3, MUG_CY - 5],
                 fill=SPECULAR_WHITE)
    draw = ImageDraw.Draw(img)

    # Miri eye highlight (boost to specular level)
    HEAD_CX_M  = int(W * 0.275)
    HEAD_CY_M  = int(H * 0.345)
    HEAD_R_M   = 38
    head_ry_M  = int(HEAD_R_M * 0.90)
    EYE_R_M    = max(5, int(HEAD_R_M * 0.165))
    EYE_Y_M    = HEAD_CY_M - int(head_ry_M * 0.15)
    EYE_X_L_M  = HEAD_CX_M - int(HEAD_R_M * 0.35)
    for EX in [EYE_X_L_M, HEAD_CX_M + int(HEAD_R_M * 0.35)]:
        pupil_r = max(2, EYE_R_M - 3)
        draw.ellipse([EX - pupil_r, EYE_Y_M - pupil_r,
                      EX - pupil_r + 2, EYE_Y_M - pupil_r + 2],
                     fill=SPECULAR_WHITE)
        draw = ImageDraw.Draw(img)

    # Luma eye highlight (boost)
    HEAD_CX_L = int(W * 0.520)
    HEAD_CY_L = int(H * 0.280)
    HEAD_R_L  = 40
    EYE_R_L   = max(7, int(HEAD_R_L * 0.22))
    EYE_Y_L   = HEAD_CY_L - int(HEAD_R_L * 0.14)
    EYE_X_L_L = HEAD_CX_L - int(HEAD_R_L * 0.36)
    for EX in [EYE_X_L_L, HEAD_CX_L + int(HEAD_R_L * 0.36)]:
        pupil_r = max(3, EYE_R_L - 3)
        draw.ellipse([EX - pupil_r, EYE_Y_L - pupil_r,
                      EX - pupil_r + 3, EYE_Y_L - pupil_r + 3],
                     fill=SPECULAR_WHITE)
        draw = ImageDraw.Draw(img)

    return img, draw


# ── Layer 8: Atmospheric Overlay (vignette + film grain) ─────────────────────

def draw_atmosphere(img):
    """Vignette + subtle warm haze. Quiets the periphery."""
    # Vignette
    ov = Image.new("RGBA", img.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    CX, CY = W // 2, H // 2
    for r in range(max(W, H), min(W, H) // 2, -20):
        t = 1.0 - ((r - min(W, H) // 2) / (max(W, H) - min(W, H) // 2))
        a = int(55 * (t ** 2.0))
        od.ellipse([CX - r, CY - r, CX + r, CY + r],
                   fill=(18, 12, 6, a))
    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, ov)
    img = img_rgba.convert("RGB")

    # Subtle film grain (noise overlay — seeded)
    rng = random.Random(9977)
    grain = Image.new("RGBA", img.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(grain)
    for _ in range(int(W * H * 0.008)):
        gx = rng.randint(0, W - 1)
        gy = rng.randint(0, H - 1)
        bv = rng.randint(0, 32)
        ga = rng.randint(4, 14)
        gd.point([(gx, gy)], fill=(bv, bv, bv, ga))
    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, grain)
    img = img_rgba.convert("RGB")

    return img


# ── Main Render ───────────────────────────────────────────────────────────────

def render():
    """Full render pipeline — returns the final PIL Image."""
    img = Image.new("RGB", (W, H), WARM_CREAM)

    # 1. Kitchen background
    draw, VP_X, VP_Y, BW_LEFT, BW_RIGHT, BW_TOP, BW_BOT = draw_kitchen_bg(img)

    # 2. Floor detail
    draw = draw_floor_detail(img, draw)

    # 3. Kitchen details (props, window, doorway, table)
    draw = draw_kitchen_details(img, draw, VP_X, VP_Y, BW_LEFT, BW_RIGHT, BW_TOP, BW_BOT)

    # 4. CRT cool atmosphere (bottom-half cool zone — runs BEFORE characters
    #    so characters receive the ambient glow)
    img = draw_crt_atmosphere(img)
    draw = ImageDraw.Draw(img)

    # 5. Miri (seated, left-of-center)
    img, draw = draw_miri(img, draw)

    # 6. Luma (standing, right)
    img, draw = draw_luma(img, draw)

    # 7. Warm lighting overlay (top half — morning window)
    img = draw_warm_lighting(img)
    draw = ImageDraw.Draw(img)

    # 8. Character lighting fills
    img = draw_character_lighting(img)
    draw = ImageDraw.Draw(img)

    # 9. Deep shadow anchors (LAST structural pass — after all light passes)
    img, draw = draw_deep_shadows(img, draw)

    # 10. Atmosphere (vignette + grain) — before specular so vignette doesn't clip them
    img = draw_atmosphere(img)
    draw = ImageDraw.Draw(img)

    # 11. Specular highlights (value ceiling anchors — AFTER atmosphere, immune to vignette)
    img, draw = draw_specular_highlights(img, draw)

    # Enforce ≤ 1280px hard limit (already native — no thumbnail pass needed)
    assert img.width <= 1280 and img.height <= 1280, \
        f"Canvas {img.width}×{img.height} exceeds 1280px limit"

    return img


def main():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    print("[sf05_relationship] Rendering Miri+Luma relationship frame…")
    img = render()
    img.save(OUTPUT_PATH)
    print(f"[sf05_relationship] Saved: {OUTPUT_PATH}  ({img.width}×{img.height}px)")

    # Face test gate check — both characters at pitch scale
    # head_r: Miri=38px, Luma=40px. Both exceed sprint threshold (20–25px).
    # Gate does NOT trigger. Report dimensions for record.
    print()
    print("── Face Test Gate ─────────────────────────────────────────────────")
    print("  Miri head_r = 38px  — ABOVE sprint threshold (20–25px) → gate not triggered")
    print("  Luma head_r = 40px  — ABOVE sprint threshold (20–25px) → gate not triggered")
    print("  Both faces drawn at pitch scale: full fidelity geometry applied.")
    print()
    print("── Warm/Cool Strategy Summary ──────────────────────────────────────")
    print("  Top half:    SUNLIT_AMBER alpha 0–90 linear (morning window from upper-left)")
    print("  Bottom half: CRT_COOL_SPILL alpha 0–85 linear (CRT doorway glow)")
    print("  Split: top/bottom halves per render_qa measurement convention.")
    print("  Target separation ≥ 12.0  (SF04 baseline: 13.2)")
    print()
    print("── Delivery ────────────────────────────────────────────────────────")
    print(f"  Output: {OUTPUT_PATH}")
    print("  Naming: LTG_COLOR_styleframe_sf05.png — pitch-package relationship key")
    print()
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
