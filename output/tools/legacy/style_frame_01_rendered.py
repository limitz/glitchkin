#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
Style Frame 01 — The Discovery (Rendered Composite)
"Luma & the Glitchkin" — Cycle 11

Art Director: Alex Chen
Date: 2026-03-29
Cycle 10 changes (Sam Kowalski):
  - HOODIE_AMBIENT arithmetic correction (CHAR-L-08): updated from #B06040 (176,96,64) to
    #B36250 (179,98,80). The 70/30 blend of HOODIE_SHADOW+DUSTY_LAVENDER yields (179,98,80),
    not (176,96,64). Blue channel was 16 points too low. Naomi Bridges C9-5.
  - draw_lighting_overlay() overlap analysis CORRECTED (Naomi Bridges C10): warm/cold
    boundary overlap is 80px (x=W//2-80 to x=W//2). Cold overlay peaks at alpha≈30 (~11.8%)
    at the 80px boundary — the prior note "both alphas near-zero" was arithmetically wrong.
    Corrected arithmetic: monitor_cx≈1401, boundary at x=880, distance=521px; max rx=1056px
    (int(W*0.55)); t≈0.49 at boundary; alpha=int(60*(1-0.49))=30; 30/255=11.8%.
    Visual decision: cold_alpha_max=60 RETAINED. At ~12% opacity, the cold cyan cross-light
    reads as a plausible split-light transition — warm lamp left, cool monitor wall spill right,
    80px feathered overlap. ~12% cold cyan over warm skin is a cross-light effect, not cold
    contamination; no grey zone in rendered output. Confirmed. See draw_lighting_overlay().
Cycle 11 changes (Alex Chen):
  - Mid-air transition element added: pixel confetti in x=768–960, y=200–700 air column.
    Warm-lit (SOFT_GOLD/SUNLIT_AMBER) left of zone midpoint; cold-lit (ELEC_CYAN/BYTE_TEAL)
    right of midpoint. Bridges warm and cold zones in the air. Victoria Ashford P1 (2 cycles).
  - Screen pixel figures scaled: 7px wide → 15px wide. Full 3-tier pixel structure
    (head 5×4 + body 9×5 + legs 3×5). Now viewer-readable silhouettes. Victoria Ashford P2.
Cycle 10 changes (Alex Chen):
  - Luma lean increased: lean_offset 28px→48px (~9°→~16°) for genuine active urgency.
    Victoria Ashford P2: 28px was "watching television" lean; 48px = active emotional engagement.
  - Monitor screen content added: receding perspective grid + pixel figure silhouettes in
    screen corners. Establishes that Byte emerges from a specific digital interior, not a
    generic void. Victoria Ashford P3.
Cycle 9 changes (Alex Chen):
  - HOODIE_AMBIENT (CHAR-L-08, #B06040) finalized; replaces SHADOW_PLUM on hoodie underside.
    Derived: HOODIE_SHADOW (#B84A20) blended with DUSTY_LAVENDER at 70/30 → (176,96,64).
    [NOTE: arithmetic was incorrect — corrected in Cycle 10 to #B36250 (179,98,80)]
  - Couch scale fixed (P0): couch_left W*0.04→W*0.16, couch_right W*0.44→W*0.38.
    Span reduced 768px→422px; ratio 8.7:1→4.8:1 vs Luma's 88px body.
  - Submerge/glow draw order fixed (P1): submerge fade now drawn BEFORE screen-glow so
    the ELEC_CYAN glow is not overwritten by the near-black submerge rows.
  - Overlay draw order fixed (P3): atmospheric overlay now applied BEFORE characters (was
    STEP 6 after characters). Hoodie and arm lighting are now unaffected by the overlay.
  - False comment corrected: arm span is ~28%, not ~21% as stated in Cycle 7/8 comment.

This script composites Frame 01 (The Discovery) into a single cohesive rendered image:
  - Background: Luma's house interior — warm room with dominant cold monitor wall
  - Byte: emerging from the central CRT screen with Corrupted Amber elliptical outline
  - Luma: on the couch in Reckless Excitement expression — reaching toward the screen
  - Three-light setup: cyan right (monitor wall), warm gold left (lamp), lavender ambient fill
  - Visual premise: a girl discovering something impossible — legible without text

Emotional intent:
  The warm amber half of the frame (left) = safety, home, the known world.
  The cold cyan half (right, monitor wall) = the impossible, the digital, Byte's world.
  Luma bridges both halves — body in the warm zone, face and reaching arm crossing into cold.
  Byte emerges from the screen toward Luma. Two hands reaching. Discovery.

Output: /home/wipkat/team/output/color/style_frames/style_frame_01_rendered.png

Usage: python3 style_frame_01_rendered.py
"""

import os
import math
import random
from PIL import Image, ImageDraw, ImageFont

OUTPUT_PATH = "/home/wipkat/team/output/color/style_frames/style_frame_01_rendered.png"
# Cycle 12: new versioned output for ghost Byte A+ surprise element
OUTPUT_PATH_V002 = "/home/wipkat/team/output/color/style_frames/LTG_COLOR_styleframe_discovery_v002.png"
W, H = 1920, 1080

# ── Master Palette (from master_palette.md) ──────────────────────────────────
# Real World
WARM_CREAM      = (250, 240, 220)   # RW-01
SOFT_GOLD       = (232, 201,  90)   # RW-02
SUNLIT_AMBER    = (212, 146,  58)   # RW-03
TERRACOTTA      = (199,  91,  57)   # RW-04
RUST_SHADOW     = (140,  58,  34)   # RW-05
SAGE_GREEN      = (122, 158, 126)   # RW-06
DUSTY_LAVENDER  = (168, 155, 191)   # RW-08 — ambient fill third light
SHADOW_PLUM     = ( 92,  74, 114)   # RW-09
WARM_TAN        = (196, 168, 130)   # RW-10
SKIN_SHADOW     = (140,  90,  56)   # RW-11
DEEP_COCOA      = ( 59,  40,  32)   # RW-12
OCHRE_BRICK     = (184, 148,  74)   # RW-14
# Glitch
ELEC_CYAN       = (  0, 240, 255)   # GL-01 — Electric Cyan
BYTE_TEAL       = (  0, 212, 232)   # GL-01b — Byte body fill
DEEP_CYAN       = (  0, 168, 180)   # GL-02
HOT_MAGENTA     = (255,  45, 107)   # GL-03
UV_PURPLE       = (123,  47, 190)   # GL-04
VOID_BLACK      = ( 10,  10,  20)   # GL-06
CORRUPTED_AMBER = (255, 140,   0)   # GL-07 — Byte outline in cyan environments
STATIC_WHITE    = (240, 240, 240)   # GL-08
# Derived
SKIN            = (200, 136,  90)   # Luma skin lit
SKIN_HL         = (232, 184, 136)   # Luma skin highlight (warm lamp side)
SKIN_SH         = (168, 104,  56)   # Luma skin shadow
CYAN_SKIN       = (122, 188, 186)   # Luma skin — cyan-lit side (DRW-01)
HOODIE_ORANGE   = (232, 112,  58)   # Luma hoodie — warm lamp side
HOODIE_SHADOW   = (184,  74,  32)   # hoodie shadow
HOODIE_CYAN_LIT = (191, 138, 120)   # Luma hoodie — cyan-lit side (DRW-03)
HAIR_COLOR      = ( 26,  15,  10)   # Luma hair
LINE            = ( 59,  40,  32)   # Line weight
BYTE_HL         = (  0, 240, 255)   # Byte highlight
BYTE_SH         = (  0, 144, 176)   # Byte shadow
SCAR_MAG        = (255,  45, 107)   # Byte scar/crack eye
# ── Derived hoodie ambient — CHAR-L-08 (Alex Chen Cycle 9; corrected Sam Kowalski Cycle 10) ──
# Hoodie underside faces down, away from lamp and monitor. Receives lavender ambient only.
# Derivation (70/30 blend, verified Cycle 10):
#   HOODIE_SHADOW (#B84A20, RGB 184, 74, 32) × 0.7 + DUSTY_LAVENDER (#A89BBF, RGB 168,155,191) × 0.3
#   R: 184×0.7 + 168×0.3 = 128.8 + 50.4 = 179
#   G:  74×0.7 + 155×0.3 =  51.8 + 46.5 =  98
#   B:  32×0.7 + 191×0.3 =  22.4 + 57.3 =  80  (rounded from 79.7)
#   → RGB(179, 98, 80) = #B36250
# Cycle 9 value was #B06040 (176,96,64) — blue channel was 16 pts below formula result.
# Corrected to #B36250 per Naomi Bridges C9-5. Retains orange identity; blue=80 adds
# subtle lavender ambient influence appropriate for this surface.
HOODIE_AMBIENT  = (179,  98,  80)   # CHAR-L-08 (#B36250) — hoodie underside, lavender ambient tinted

# ── Prop & Character Rendering Colors — now formally registered in master_palette.md ──
# Cycle 8 audit (Sam Kowalski): all values below are documented in master_palette.md.
# JEANS / JEANS_SH: Luma denim — CHAR-L-05 (#3A5A8C) / shadow companion (#263D5A)
# COUCH_BODY / COUCH_BACK / COUCH_ARM: Luma couch — master_palette.md Section 6 PROP-01/02/03
# BLUSH_LEFT / BLUSH_RIGHT: Luma blush — CHAR-L-06 (#DC5032) / CHAR-L-07 (#D04830)
# LAMP_PEAK: lamp emission center — noted as deliberate hotspot; not in palette (see comment below)
JEANS           = ( 58,  90, 140)   # Luma jeans — CHAR-L-05 (#3A5A8C)
JEANS_SH        = ( 38,  62, 104)   # Luma jeans shadow — CHAR-L-05 shadow companion (#263D5A)
COUCH_BODY      = (107,  48,  24)   # Luma couch seat — master_palette.md PROP-01 (#6B3018)
COUCH_BACK      = (128,  60,  28)   # Luma couch back — master_palette.md PROP-02 (#803C1C)
COUCH_ARM       = (115,  52,  26)   # Luma couch arm — master_palette.md PROP-03 (#73341A)
BLUSH_LEFT      = (220,  80,  50)   # Luma left cheek blush — CHAR-L-06 (#DC5032)
BLUSH_RIGHT     = (208,  72,  48)   # Luma right cheek blush — CHAR-L-07 (#D04830)
LAMP_PEAK       = (245, 200,  66)   # Lamp emission center hotspot. Intentionally NOT in master_palette.md:
                                    # this is a one-off emission center value derived on-the-fly from
                                    # SOFT_GOLD (RW-02, #E8C95A) pushed hotter at the source. It is a
                                    # rendering construct, not a paintable palette color. Do not add to palette.
# ── Prop cable colors — registered in master_palette.md Section 6 ─────────────
CABLE_BRONZE    = (180, 140,  80)   # Warm bronze cable — PROP-04 (#B48C50)
CABLE_DATA_CYAN = (  0, 180, 255)   # Data-cyan cable — PROP-05 (#00B4FF); NOT GL-01 (#00F0FF)
CABLE_MAG_PURP  = (200,  80, 200)   # Magenta-purple cable — PROP-06 (#C850C8)
CABLE_NEUTRAL_PLUM = ( 80,  64, 100) # Desaturated Shadow Plum mid — PROP-07 (#504064)
                                    # Replaces former (100,100,100) neutral grey (no palette home).
                                    # Aged cable with cool ambient tinting. See master_palette.md PROP-07.

# ── Font Loading ──────────────────────────────────────────────────────────────
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

# ── Glow Utility — filled gradient ellipses (not outline rings) ──────────────
def draw_filled_glow(draw, cx, cy, rx, ry, glow_rgb, bg_rgb, steps=14):
    """Filled gradient glow: concentric filled ellipses from glow_rgb (center) to bg_rgb (edge).
    Addresses Takeshi Murakami Cycle 5 critique: no outline-only glow rings."""
    for i in range(steps, 0, -1):
        t = i / steps  # t=1 at edge (bg), t→0 at center (glow)
        r_v = int(bg_rgb[0] + (glow_rgb[0] - bg_rgb[0]) * (1 - t))
        g_v = int(bg_rgb[1] + (glow_rgb[1] - bg_rgb[1]) * (1 - t))
        b_v = int(bg_rgb[2] + (glow_rgb[2] - bg_rgb[2]) * (1 - t))
        er  = max(1, int(rx * t))
        er_y = max(1, int(ry * t))
        draw.ellipse([cx - er, cy - er_y, cx + er, cy + er_y], fill=(r_v, g_v, b_v))

# ── Corrupted Amber Outline — elliptical (Naomi Bridges / Cycle 6 fix) ───────
def draw_amber_outline(draw, cx, cy, rx, ry, width=3):
    """Draw Corrupted Amber elliptical outline around Byte.
    Ellipse-based (not rectangle) per GL-07 and Naomi Bridges Cycle 6 note.
    Only applied in cyan-dominant environments (Frame 01 qualifies).
    GL-07 standard: width=3 at 1920x1080. (Naomi Bridges Cycle 7 fix)"""
    for i in range(width):
        draw.ellipse(
            [cx - rx - i, cy - ry - i, cx + rx + i, cy + ry + i],
            outline=CORRUPTED_AMBER
        )

# ── Background: Luma's House Interior ────────────────────────────────────────
def draw_background(draw, img):
    """
    Draw the interior of Luma's house.
    Compositional logic:
      - LEFT half: warm amber / ochre / soft gold — safety, home
      - RIGHT half (monitor wall): deep void with cyan monitor screens — alien, digital
    The split is the visual argument of Frame 01.
    """
    ceiling_y = int(H * 0.12)

    # ── Ceiling — dark warm amber
    # (90, 55, 22): ceiling construction color — one-off dark warm amber. Not in palette:
    # it is below ENV-07 (#5A3820, 90,56,32) in value and specific to the ceiling geometry.
    # Intentionally dark to push the eye toward the mid-frame action zone.
    draw.rectangle([0, 0, W, ceiling_y], fill=(90, 55, 22))
    # (60, 36, 14): ceiling edge molding — one-off construction line, deepest value on ceiling.
    # Not in palette: it is a bespoke architectural detail line, not a recurring surface color.
    draw.line([(0, ceiling_y), (W, ceiling_y)], fill=(60, 36, 14), width=4)

    # ── Back wall — warm zone (left side), atmospheric perspective gradient
    wall_top_y = ceiling_y
    wall_bot_y = int(H * 0.54)
    far_wall   = (228, 185, 120)   # Atmospheric perspective far-wall: one-off construction blend.
                                   # Not in palette: derived by desaturating RW-03 (#D4923A) for depth.
    base_wall  = (212, 146,  58)   # = RW-03 Sunlit Amber (#D4923A) at ground midground.
                                   # Not named here because it IS a palette color (RW-03).
    for y in range(wall_top_y, wall_bot_y):
        t = (y - wall_top_y) / max(1, wall_bot_y - wall_top_y)
        r_v = int(far_wall[0] + (base_wall[0] - far_wall[0]) * t)
        g_v = int(far_wall[1] + (base_wall[1] - far_wall[1]) * t)
        b_v = int(far_wall[2] + (base_wall[2] - far_wall[2]) * t)
        draw.line([(0, y), (W, y)], fill=(r_v, g_v, b_v))

    # ── Wainscot (lower back wall section)
    # (140, 90, 26): wainscot fill — one-off construction color; darker/warmer than RW-03.
    # Not in palette: it's a background architectural zone, unique to this frame's value progression.
    draw.rectangle([0, int(H * 0.54), W, int(H * 0.75)], fill=(140, 90, 26))
    # (100, 64, 18): wainscot cap line — one-off construction detail line.
    # Not in palette: a scene-specific architectural edge, not a recurring surface color.
    draw.line([(0, int(H * 0.54)), (W, int(H * 0.54))], fill=(100, 64, 18), width=3)

    # ── Floor — warm terracotta planks
    # (90, 56, 32): floor fill — one-off construction color; ≈ ENV-07 Dark Warm Wood (#5A3820 = 90,56,32).
    # ENV-07 RGB is (90, 56, 32) — this IS ENV-07. Using inline tuple for readability here.
    draw.rectangle([0, int(H * 0.75), W, H], fill=(90, 56, 32))  # ENV-07
    for y in range(int(H * 0.75), H, 28):
        draw.line([(0, y), (W, y)], fill=RUST_SHADOW, width=1)
    # Floor grain highlights (warm)
    # (110, 70, 42): floor plank highlight line — one-off construction texture detail.
    # Not in palette: it is a sub-value grain line specific to this floor material rendering.
    for y in range(int(H * 0.76), H, 56):
        draw.line([(0, y + 4), (W, y + 4)], fill=(110, 70, 42), width=1)

    # ── Monitor Wall — dominant cold element (right half of frame) ────────────
    mw_x  = int(W * 0.50)
    mw_y  = ceiling_y + 5
    mw_w  = int(W * 0.46)
    mw_h  = int(H * 0.57)
    # Alcove background — near-void
    # (14, 10, 22): monitor alcove void — one-off construction value; slightly warmer than GL-06
    # Void Black (#0A0A14 = 10,10,20). Not in palette: this is the backing field behind the monitor
    # wall, one step up from pure void, giving the screens a dark-but-not-flat context.
    draw.rectangle([mw_x, mw_y, mw_x + mw_w, mw_y + mw_h], fill=(14, 10, 22))

    # Six monitor screens in a wall array — varied sizes
    monitor_specs = [
        (mw_x +  40, mw_y +  20, 260, 150),
        (mw_x + 330, mw_y +  15, 320, 180),
        (mw_x + 680, mw_y +  28, 230, 140),
        (mw_x +  50, mw_y + 190, 280, 165),
        (mw_x + 360, mw_y + 215, 300, 170),
        (mw_x + 685, mw_y + 185, 210, 150),
    ]

    # Monitor wall glow spill — filled gradient (not outline rings)
    cx_glow = mw_x + mw_w // 2
    cy_glow = mw_y + mw_h // 2
    draw_filled_glow(draw, cx_glow, cy_glow,
                     rx=720, ry=420,
                     glow_rgb=(0, 60, 100),
                     bg_rgb=(14, 10, 22),
                     steps=16)

    # Draw monitors
    for mx, my, mw_s, mh_s in monitor_specs:
        # Monitor casing (near-void with cool grey edge)
        # (12, 10, 18): monitor casing fill — construction color; near-void, slightly purple-shifted.
        # (28, 22, 40): casing edge — construction color; cool dark purple, separates casing from alcove.
        # Neither in palette: both are bespoke construction values for the monitor wall geometry.
        draw.rectangle([mx - 6, my - 6, mx + mw_s + 6, my + mh_s + 6],
                       fill=(12, 10, 18), outline=(28, 22, 40), width=2)
        # Screen fill — ELEC_CYAN (GL-01); NOT BYTE_TEAL — Byte Teal is Byte's body color only
        draw.rectangle([mx, my, mx + mw_s, my + mh_s], fill=ELEC_CYAN)
        # Screen hot center — filled glow
        cx_m = mx + mw_s // 2
        cy_m = my + mh_s // 2
        draw_filled_glow(draw, cx_m, cy_m,
                         mw_s // 2, mh_s // 2,
                         glow_rgb=(180, 255, 255),  # Hot screen center — one-off construction glow.
                         # Not in palette: this is a whiteout emission center pushed beyond
                         # Electric Cyan. It reads as near-white light, not a paintable color.
                         bg_rgb=ELEC_CYAN,
                         steps=8)
        # Scanlines — (0, 168, 180) = GL-02 Deep Cyan (#00A8B4). Slight green shift vs palette
        # due to int rounding; semantically it is GL-02. Construction detail, not a new palette entry.
        for sy in range(my + 3, my + mh_s, 5):
            draw.line([(mx, sy), (mx + mw_s, sy)], fill=(0, 168, 180), width=1)
        # Monitor bezel highlight — (40, 40, 60): one-off construction detail line (cool dark grey).
        # Not in palette: it is a micro-detail of the monitor casing; too small and specific to register.
        draw.line([(mx, my), (mx + mw_s, my)], fill=(40, 40, 60), width=2)

    # ── Cycle 12 (Victoria Ashford A+ gap): Visual surprise — ghost Byte silhouettes ──
    # ON PERIPHERAL MONITORS: faint oval Byte-form ghost, barely perceptible, on three of the
    # six background monitors. The viewer's eye first goes to Byte emerging from the CRT.
    # On a second look, they notice the same oval form watching from the other screens —
    # implying Byte has been observing Luma through every screen before choosing to reveal itself.
    # This is a story beat hidden inside the production art. It elevates the frame from "a
    # girl meeting something digital" to "something digital that has been waiting for her."
    # Ghost alpha is 55/255 (~22%) — visible on careful inspection, not on first glance.
    # Implementation: RGBA composite over the RGB image at each peripheral screen.
    ghost_screens = [
        monitor_specs[0],   # top-left monitor
        monitor_specs[2],   # top-right monitor
        monitor_specs[4],   # mid-right monitor
    ]
    for gs_mx, gs_my, gs_mw, gs_mh in ghost_screens:
        # Byte ghost: small oval (body only) centered on the screen, very faint
        # Ghost body parameters
        ghost_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ghost_draw  = ImageDraw.Draw(ghost_layer)
        g_cx  = gs_mx + gs_mw // 2
        g_cy  = gs_my + gs_mh // 2 - int(gs_mh * 0.08)  # slightly above center (floating)
        g_rx  = int(gs_mw * 0.28)   # oval body radius — proportional to monitor size
        g_ry  = int(gs_mh * 0.38)
        # Ghost body oval — very dark near-void slightly lighter than screen bg (25% BYTE_TEAL)
        # (0, 53, 58) = BYTE_TEAL at ~23% over ELEC_CYAN background: read as a shadow impression.
        # Not in palette: this is a composite ghost value, not a paintable production color.
        ghost_draw.ellipse([g_cx - g_rx, g_cy - g_ry, g_cx + g_rx, g_cy + g_ry],
                           fill=(0, 53, 58, 55))
        # Ghost eye glints — two tiny pixel squares suggesting the dual eyes
        # (0, 220, 240) at alpha 70 — faint hotspot inside ghost form
        eye_y = g_cy - int(g_ry * 0.15)
        e_r   = max(2, int(g_rx * 0.20))
        ghost_draw.rectangle([g_cx - int(g_rx * 0.35) - e_r, eye_y - e_r,
                               g_cx - int(g_rx * 0.35) + e_r, eye_y + e_r],
                              fill=(0, 220, 240, 70))
        ghost_draw.ellipse([g_cx + int(g_rx * 0.20) - e_r, eye_y - e_r,
                            g_cx + int(g_rx * 0.20) + e_r, eye_y + e_r],
                           fill=(0, 220, 240, 60))
        # Composite ghost onto main image
        base_rgba = img.convert("RGBA")
        img_with_ghost = Image.alpha_composite(base_rgba, ghost_layer)
        img.paste(img_with_ghost.convert("RGB"))
    draw = ImageDraw.Draw(img)   # refresh draw handle after compositing

    # ── CRT screen (central, Byte emergence point) ──────────────────────────
    # The main CRT where Byte emerges — larger, more prominent, screen-center
    # Positioned at visual center-right of the monitor wall
    crt_x  = mw_x + int(mw_w * 0.22)
    crt_y  = mw_y + int(mw_h * 0.08)
    crt_w  = int(mw_w * 0.52)
    crt_h  = int(mw_h * 0.62)
    # CRT casing — bulky vintage shape
    # (44, 36, 56): CRT casing fill — one-off construction color; dark plum-grey for aged plastic.
    # (30, 24, 42): CRT casing edge — one-off construction detail; deeper plum-shadow.
    # Neither in palette: both are bespoke prop construction values for the CRT model.
    draw.rectangle([crt_x - 10, crt_y - 10, crt_x + crt_w + 10, crt_y + crt_h + 20],
                   fill=(44, 36, 56), outline=(30, 24, 42), width=3)
    # CRT bottom pedestal — (36, 28, 46): one-off construction color; very dark plum-grey.
    # Not in palette: it is a sub-element of the CRT prop, too small and specific to register.
    draw.rectangle([crt_x + crt_w // 3, crt_y + crt_h + 18,
                    crt_x + crt_w * 2 // 3, crt_y + crt_h + 40],
                   fill=(36, 28, 46))
    # CRT screen area
    scr_pad = 24
    scr_x0  = crt_x + scr_pad
    scr_y0  = crt_y + scr_pad
    scr_x1  = crt_x + crt_w - scr_pad
    scr_y1  = crt_y + crt_h - scr_pad * 2
    # Screen background: full cyan
    draw.rectangle([scr_x0, scr_y0, scr_x1, scr_y1], fill=ELEC_CYAN)

    # ── Cycle 10 fix (Victoria Ashford P3): Screen content ────────────────
    # Screen was a blank cyan void — narratively generic (Byte emerged from "nowhere").
    # Add visual content implying Byte's origin: a receding pixel-grid world and a small
    # pixel figure silhouette in the screen corners/margins, behind the emergence zone.
    # This establishes that Byte comes from a specific somewhere — a digital interior.

    # Receding grid pattern — perspective lines from center (Byte's origin world)
    # Draw light grid lines over the screen surface (at low alpha, will be partially
    # covered by scanlines and emergence zone ellipse)
    scr_mid_x = (scr_x0 + scr_x1) // 2
    scr_mid_y = (scr_y0 + scr_y1) // 2
    grid_color = (0, 168, 180)  # GL-02 Deep Cyan — faint grid, same family as scanlines
    # Receding vertical lines — converge toward center
    for i in range(1, 6):
        t = i / 5.0
        lx = int(scr_x0 + (scr_mid_x - scr_x0) * t)
        rx = int(scr_x1 - (scr_x1 - scr_mid_x) * t)
        draw.line([(lx, scr_y0), (scr_mid_x, scr_mid_y)],
                  fill=grid_color, width=1)
        draw.line([(rx, scr_y0), (scr_mid_x, scr_mid_y)],
                  fill=grid_color, width=1)
    # Receding horizontal lines — converge toward center
    for i in range(1, 5):
        t = i / 4.0
        ty = int(scr_y0 + (scr_mid_y - scr_y0) * t)
        draw.line([(scr_x0, ty), (scr_mid_x, scr_mid_y)],
                  fill=grid_color, width=1)
        draw.line([(scr_x1, ty), (scr_mid_x, scr_mid_y)],
                  fill=grid_color, width=1)

    # ── Cycle 11 fix (Victoria Ashford P2): Scale screen pixel figures from 7px → 15px ──
    # Previous 7px-wide forms were sub-legible rendering artifacts, not viewer-readable design.
    # Replaced with 15px-wide pixel figures using a clear 3-tier pixel structure:
    # head (5×4px) + body (9×5px) + legs (3×5px each). Figures now read as silhouettes.
    scr_rng = random.Random(99)
    # Upper-left corner pixel figure — 15px wide glitch figure
    fig_x = scr_x0 + 14
    fig_y = scr_y0 + 12
    fig_color = (0, 80, 100)   # Dark cyan silhouette — receding into screen depth
    # Head — 5×4px centered on body
    draw.rectangle([fig_x + 5, fig_y,      fig_x + 10, fig_y + 4],  fill=fig_color)
    # Body — 9×5px
    draw.rectangle([fig_x + 3, fig_y + 4,  fig_x + 12, fig_y + 9],  fill=fig_color)
    # Arms — one each side, 3px long
    draw.rectangle([fig_x,     fig_y + 4,  fig_x + 3,  fig_y + 6],  fill=fig_color)
    draw.rectangle([fig_x + 12, fig_y + 4, fig_x + 15, fig_y + 6],  fill=fig_color)
    # Legs — 3px wide, 5px tall
    draw.rectangle([fig_x + 3,  fig_y + 9, fig_x + 6,  fig_y + 14], fill=fig_color)
    draw.rectangle([fig_x + 9,  fig_y + 9, fig_x + 12, fig_y + 14], fill=fig_color)

    # Upper-right corner pixel figure — 15px wide, pointing gesture toward emergence zone
    fig_x2 = scr_x1 - 30
    fig_y2 = scr_y0 + 10
    fig_color2 = (0, 60, 80)   # Even darker — further receded
    # Head — 5×4px
    draw.rectangle([fig_x2 + 5, fig_y2,     fig_x2 + 10, fig_y2 + 4],  fill=fig_color2)
    # Body — 9×5px
    draw.rectangle([fig_x2 + 3, fig_y2 + 4, fig_x2 + 12, fig_y2 + 9],  fill=fig_color2)
    # One arm extended toward emergence zone (pointing left = toward center)
    draw.rectangle([fig_x2 - 6, fig_y2 + 4, fig_x2 + 3, fig_y2 + 6],   fill=fig_color2)
    # Other arm short
    draw.rectangle([fig_x2 + 12, fig_y2 + 4, fig_x2 + 15, fig_y2 + 6], fill=fig_color2)
    # Legs
    draw.rectangle([fig_x2 + 3,  fig_y2 + 9, fig_x2 + 6,  fig_y2 + 14], fill=fig_color2)
    draw.rectangle([fig_x2 + 9,  fig_y2 + 9, fig_x2 + 12, fig_y2 + 14], fill=fig_color2)

    # Pixel noise scatter on screen margins (away from emergence center) — data texture
    for _ in range(28):
        # Constrain to screen margins, away from emergence zone center
        px_x = scr_x0 + scr_rng.randint(0, scr_x1 - scr_x0)
        px_y = scr_y0 + scr_rng.randint(0, scr_y1 - scr_y0)
        # Only draw if far enough from emergence center (margin only)
        dist_from_center = ((px_x - scr_mid_x) ** 2 + (px_y - scr_mid_y) ** 2) ** 0.5
        min_dist = min(scr_x1 - scr_x0, scr_y1 - scr_y0) * 0.30
        if dist_from_center > min_dist:
            ps = scr_rng.choice([2, 3])
            pc = scr_rng.choice([
                (0, 100, 120),   # dark cyan noise — receding pixel world
                (0, 60, 80),     # very dark — deep recession
                (0, 140, 160),   # mid cyan — closer to surface
            ])
            draw.rectangle([px_x, px_y, px_x + ps, px_y + ps], fill=pc)

    # Emergence zone — dark pocket where Byte pushes through (center of CRT screen)
    emerge_cx = (scr_x0 + scr_x1) // 2
    emerge_cy = (scr_y0 + scr_y1) // 2
    emerge_rx = int((scr_x1 - scr_x0) * 0.34)
    emerge_ry = int((scr_y1 - scr_y0) * 0.44)
    # Dark void pocket at emergence — Byte pops against it
    # (14, 14, 30): slightly warmer/more purple than GL-06 Void Black (#0A0A14).
    # This value is the same VOID_POCKET used in draw_byte() for Byte's submersion zone.
    # Not in palette: it is a construction rendering value for the emergence void, not a
    # paintable palette color. It is a one-off "local void" that avoids true Void Black
    # to preserve the screen's presence (a fully black ellipse would look like a hole).
    draw.ellipse([emerge_cx - emerge_rx, emerge_cy - emerge_ry,
                  emerge_cx + emerge_rx, emerge_cy + emerge_ry],
                 fill=(14, 14, 30))
    # Glow ring around emergence
    draw.ellipse([emerge_cx - emerge_rx - 8, emerge_cy - emerge_ry - 8,
                  emerge_cx + emerge_rx + 8, emerge_cy + emerge_ry + 8],
                 outline=DEEP_CYAN, width=4)
    draw.ellipse([emerge_cx - emerge_rx - 14, emerge_cy - emerge_ry - 14,
                  emerge_cx + emerge_rx + 14, emerge_cy + emerge_ry + 14],
                 outline=(0, 80, 100), width=2)  # Outer glow ring: one-off dark cyan-teal. Not in
                                                  # palette: construction detail for emergence glow depth.
    # Screen phosphor edge
    draw.rectangle([scr_x0, scr_y0, scr_x1, scr_y1],
                   outline=DEEP_CYAN, width=5)
    # Scanlines on screen
    for sy in range(scr_y0 + 4, scr_y1, 7):
        draw.line([(scr_x0, sy), (scr_x1, sy)], fill=(0, 168, 180), width=1)

    # Pixel confetti — glitch energy escaping from CRT
    rng = random.Random(42)
    for _ in range(80):
        px = rng.randint(scr_x0 - 120, scr_x1 + 60)
        py = rng.randint(scr_y0 - 80, int(H * 0.75))
        ps = rng.choice([3, 4, 5, 6])
        # (0, 200, 220): one-off pixel confetti color; mid-value cyan between GL-01 and GL-02.
        # Not in palette: pixel confetti is a procedural effect using palette-adjacent colors.
        # This value provides variety in the confetti without being a named production color.
        pc = rng.choice([ELEC_CYAN, STATIC_WHITE, BYTE_TEAL, (0, 200, 220)])
        draw.rectangle([px, py, px + ps, py + ps], fill=pc)

    # CRT screen glow spill — onto floor and left wall (the cold intrusion into warm space)
    # Floor glow polygon — cold cyan trapezoid on warm floor
    floor_glow_pts = [
        (crt_x,            int(H * 0.75)),
        (crt_x + crt_w,    int(H * 0.75)),
        (crt_x + crt_w + 160, H),
        (crt_x - 100,      H),
    ]
    # (0, 22, 38): floor glow polygon fill — one-off construction value; very dark cold cyan.
    # Not in palette: it is a lighting effect polygon (cold screen spill on warm floor).
    # Intentionally desaturated so it does not compete with GL-01 on the monitor wall.
    draw.polygon(floor_glow_pts, fill=(0, 22, 38))
    # Left wall spill — warm wall gets a cold cast near the monitor boundary
    # glow_rgb (0, 40, 70): dark blue-cyan spill center — one-off construction value.
    # bg_rgb (180, 130, 60): warm amber wall mid-tone for glow blend — one-off construction value.
    # Neither in palette: both are bespoke blending endpoints for the wall spill rendering.
    draw_filled_glow(draw, mw_x - 20, mw_y + mw_h // 2,
                     rx=160, ry=220,
                     glow_rgb=(0, 40, 70),
                     bg_rgb=(180, 130, 60),
                     steps=10)

    # ── WINDOW — upper left (warm afternoon light source) ──────────────────
    win_x0, win_y0 = 60, ceiling_y + 20
    win_x1, win_y1 = 340, ceiling_y + 260
    # Curtain fabric — (168, 108, 48): one-off prop color; warm amber-brown fabric.
    # Not in palette: the curtain is a one-off background prop specific to Frame 01.
    # It sits between SUNLIT_AMBER (RW-03, 212,146,58) and RUST_SHADOW (RW-05, 140,58,34)
    # in value — it is a derived mid-shadow, not a recurring material.
    draw.rectangle([win_x0 - 30, win_y0 - 10, win_x0 + 14, win_y1 + 20],
                   fill=(168, 108, 48))
    draw.rectangle([win_x1 - 14, win_y0 - 10, win_x1 + 30, win_y1 + 20],
                   fill=(168, 108, 48))
    # Window light fill
    draw.rectangle([win_x0, win_y0, win_x1, win_y1], fill=SOFT_GOLD)
    draw.rectangle([win_x0, win_y0, win_x1, win_y1],
                   outline=DEEP_COCOA, width=4)
    # Window cross-bars
    mid_win_x = (win_x0 + win_x1) // 2
    mid_win_y = (win_y0 + win_y1) // 2
    draw.line([(mid_win_x, win_y0), (mid_win_x, win_y1)],
              fill=DEEP_COCOA, width=3)
    draw.line([(win_x0, mid_win_y), (win_x1, mid_win_y)],
              fill=DEEP_COCOA, width=3)

    # ── BOOKSHELVES — upper right of warm zone ──────────────────────────────
    shelf_x = int(W * 0.20)
    shelf_y = ceiling_y
    shelf_w = int(W * 0.28)
    shelf_h = int(H * 0.45)
    draw.rectangle([shelf_x, shelf_y, shelf_x + shelf_w, shelf_y + shelf_h],
                   fill=SUNLIT_AMBER)
    # Book rows
    # Book spine colors: palette entries + 2 one-off construction colors.
    # (96, 144, 180): one-off book spine — muted steel-blue. Not in palette: individual
    # book spine colors are procedurally selected background detail props, not recurring
    # production colors. Each spine is a distinct object with its own visual identity.
    # (184, 160, 100): one-off book spine — warm tan-gold. Not in palette: same rationale
    # as above. Both values are chosen for harmony with the warm room palette; they are
    # prop detail colors, not paintable character or environment anchors.
    book_colors = [TERRACOTTA, SAGE_GREEN, DUSTY_LAVENDER, OCHRE_BRICK,
                   RUST_SHADOW, (96, 144, 180), (184, 160, 100)]
    for row in range(shelf_y + 4, shelf_y + shelf_h, 50):
        # Shelf divider
        draw.line([(shelf_x, row + 44), (shelf_x + shelf_w, row + 44)],
                  fill=DEEP_COCOA, width=2)
        col_idx = 0
        bx = shelf_x + 8
        while bx + 20 < shelf_x + shelf_w:
            bw = rng.randint(18, 36)
            bc = book_colors[col_idx % len(book_colors)]
            draw.rectangle([bx, row + 4, bx + bw, row + 42], fill=bc)
            draw.line([(bx, row + 4), (bx, row + 42)], fill=DEEP_COCOA, width=1)
            bx += bw + 2
            col_idx += 1

    # ── DESK — in front of monitor wall, with objects ───────────────────────
    desk_y = int(H * 0.60)
    desk_x0 = mw_x - 80
    desk_x1 = W
    draw.rectangle([desk_x0, desk_y, desk_x1, desk_y + 70],
                   fill=OCHRE_BRICK)
    draw.line([(desk_x0, desk_y), (desk_x1, desk_y)], fill=DEEP_COCOA, width=3)
    # Keyboard
    draw.rectangle([desk_x0 + 30, desk_y + 10, desk_x0 + 240, desk_y + 46],
                   fill=DUSTY_LAVENDER, outline=DEEP_COCOA, width=2)
    for ky in range(desk_y + 16, desk_y + 40, 10):
        for kx in range(desk_x0 + 38, desk_x0 + 234, 18):
            # (148, 135, 175): keyboard key fill — one-off prop detail.
            # Not in palette: individual keyboard keycap color is a single-prop detail too small
            # and specific to register. It is a desaturated violet that harmonizes with the
            # DUSTY_LAVENDER keyboard body (RW-08) while giving the keys slight value relief.
            draw.rectangle([kx, ky, kx + 14, ky + 7], fill=(148, 135, 175))
    # Mug
    draw.rectangle([desk_x0 + 260, desk_y + 8, desk_x0 + 310, desk_y + 55],
                   fill=TERRACOTTA, outline=DEEP_COCOA, width=2)
    draw.arc([desk_x0 + 308, desk_y + 20, desk_x0 + 332, desk_y + 44],
             start=270, end=90, fill=DEEP_COCOA, width=3)
    # Cables from monitor — PROP-04 (CABLE_BRONZE) and PROP-05 (CABLE_DATA_CYAN)
    cable_colors = [ELEC_CYAN, HOT_MAGENTA, CABLE_BRONZE, CABLE_DATA_CYAN]
    for ci, cc in enumerate(cable_colors):
        cx_s = desk_x0 + 40 + ci * 60
        cx_e = desk_x0 + 120 + ci * 80
        mid_y = desk_y + 70 + 30
        draw.arc([cx_s, desk_y + 50, cx_e, desk_y + 100], 0, 180, fill=cc, width=2)

    # ── LAMP — pure warm zone (left of monitor wall boundary) ───────────────
    lamp_x = int(W * 0.40)
    lamp_y = ceiling_y + 18
    # Lamp glow — filled warm gradient, bounded to warm side
    draw_filled_glow(draw, lamp_x + 32, lamp_y + 50,
                     rx=180, ry=110,
                     glow_rgb=LAMP_PEAK,
                     bg_rgb=base_wall,
                     steps=12)
    # Lamp body — (245, 200, 66) = LAMP_PEAK (see top of file). Reuse intentional:
    # the lamp body fill matches its own emission center (the lamp shade IS the hotspot).
    draw.rectangle([lamp_x, lamp_y, lamp_x + 64, lamp_y + 86],
                   fill=(245, 200, 66), outline=DEEP_COCOA, width=2)
    draw.ellipse([lamp_x + 12, lamp_y + 80, lamp_x + 52, lamp_y + 96],
                 fill=SUNLIT_AMBER)

    # ── LAMP FLOOR POOL — warm glow on floor below lamp (Naomi Bridges Cycle 8) ──
    # A lamp positioned at lamp_x casts a downward warm glow onto the floor.
    # Without this pool the lamp has no spatial presence on the floor.
    lamp_floor_cx = lamp_x + 32
    lamp_floor_cy = int(H * 0.85)
    draw_filled_glow(draw, lamp_floor_cx, lamp_floor_cy,
                     rx=120, ry=44,
                     glow_rgb=LAMP_PEAK,
                     bg_rgb=(90, 56, 32),   # floor fill color — ENV-07 (#5A3820 = 90,56,32)
                     steps=10)

    # ── CABLE CLUTTER foreground — distinct individual cables ───────────────
    # (42, 26, 16): cable clutter floor strip fill — one-off construction color.
    # Darker than ENV-07 floor (90, 56, 32) to create depth separation for the foreground.
    # Not in palette: this is a near-camera vignette strip, not a named environment surface.
    draw.rectangle([0, int(H * 0.92), W, H], fill=(42, 26, 16))
    fg_cables = [
        # Each entry: (x_start, x_end, base_y, arc_radius, color, thickness)
        # Colors: GL-01 (Electric Cyan), GL-03 (Hot Magenta), RW-02 (Soft Gold) are palette entries.
        # CABLE_BRONZE (PROP-04), CABLE_DATA_CYAN (PROP-05), CABLE_MAG_PURP (PROP-06) registered in
        # master_palette.md Section 6. CABLE_NEUTRAL_PLUM (PROP-07, #504064) replaces the former
        # (100, 100, 100) neutral grey — see PROP-07 in master_palette.md for rationale.
        (80,   460, int(H*0.935), 60,  ELEC_CYAN,       2),
        (240,  780, int(H*0.950), 85,  HOT_MAGENTA,     2),
        (420,  980, int(H*0.930), 44,  CABLE_BRONZE,    2),  # PROP-04
        (600, 1200, int(H*0.960), 70,  CABLE_DATA_CYAN, 1),  # PROP-05
        (840, 1500, int(H*0.940), 92,  SOFT_GOLD,       2),
        (980, 1720, int(H*0.952), 52,  CABLE_MAG_PURP,  1),  # PROP-06
        (1200,1880, int(H*0.928), 74,  ELEC_CYAN,       2),
        (1460,1920, int(H*0.962), 38,  HOT_MAGENTA,     1),
        (100,  600, int(H*0.970), 32,  CABLE_NEUTRAL_PLUM, 1),  # PROP-07 (#504064) — aged cable, cool ambient
    ]
    for x0c, x1c, base_yc, arc_r, color, thickness in fg_cables:
        pts = []
        for s in range(31):
            t = s / 30
            px = int(x0c + (x1c - x0c) * t)
            sag = int(arc_r * 4 * t * (1 - t))
            pts.append((px, base_yc + sag))
        for i in range(len(pts) - 1):
            draw.line([pts[i], pts[i+1]], fill=color, width=thickness)

    # ── Cycle 11 fix (Victoria Ashford P1): Mid-air transition element ────────
    # The x=768–960px column above floor level was compositionally dead: no element bridged
    # the warm and cold zones in the air space. This is the boundary between lamp (x~768) and
    # monitor wall (x~960). Pixel confetti drifting through this zone catches warm SOFT_GOLD
    # on the left face and cold ELEC_CYAN on the right face simultaneously — they live in both
    # worlds at once. Seeded for reproducibility; particles occupy y=200–700 only.
    # Two passes: warm-lit particles (left of zone center) and cold-lit (right of zone center).
    air_rng = random.Random(77)
    zone_x0 = int(W * 0.40)   # lamp x — warm zone edge
    zone_x1 = int(W * 0.50)   # monitor wall start — cold zone edge
    zone_mid = (zone_x0 + zone_x1) // 2   # x=864, the light boundary
    for _ in range(60):
        # Scatter across the full zone width with slight bias toward center
        px = air_rng.randint(zone_x0 - 20, zone_x1 + 20)
        py = air_rng.randint(200, 700)
        ps = air_rng.choice([3, 4, 5, 6])
        # Color: warm-lit on left side of zone, cold-lit on right side
        if px < zone_mid:
            # Warm side — pixel catches lamp light: SOFT_GOLD / SUNLIT_AMBER / LAMP_PEAK family
            pc = air_rng.choice([
                SOFT_GOLD,                  # RW-02 — warm gold
                SUNLIT_AMBER,               # RW-03 — amber
                (245, 200,  66),            # LAMP_PEAK — hottest warm point
                WARM_CREAM,                 # RW-01 — cream highlight
            ])
        else:
            # Cold side — pixel catches monitor light: ELEC_CYAN / BYTE_TEAL / DEEP_CYAN family
            pc = air_rng.choice([
                ELEC_CYAN,                  # GL-01 — electric cyan
                BYTE_TEAL,                  # GL-01b — byte teal
                DEEP_CYAN,                  # GL-02 — deeper cyan
                STATIC_WHITE,               # GL-08 — overexposed edge
            ])
        draw.rectangle([px, py, px + ps, py + ps], fill=pc)

    return {
        "scr_x0": scr_x0, "scr_y0": scr_y0,
        "scr_x1": scr_x1, "scr_y1": scr_y1,
        "emerge_cx": emerge_cx, "emerge_cy": emerge_cy,
        "emerge_rx": emerge_rx, "emerge_ry": emerge_ry,
        "mw_x": mw_x, "mw_y": mw_y, "mw_w": mw_w, "mw_h": mw_h,
        "ceiling_y": ceiling_y,
    }


# ── Luma's Body ───────────────────────────────────────────────────────────────
def draw_luma_body(draw, luma_cx, luma_base_y, facing_monitor_x):
    """
    Draw Luma's full body in a seated leaning-forward pose.
    Three-light setup:
      - LEFT (warm gold lamp): hoodie lit warm orange (#E8703A), skin warm highlight
      - RIGHT (cyan monitor): hoodie lit DRW-03 (desaturated, cyan-tinged), skin = CYAN_SKIN
      - AMBIENT (lavender): shadow areas tinted with DUSTY_LAVENDER

    Cycle 7 fixes:
      - Body leans TOWARD the monitor (torso tilted right, not vertical)
      - Torso uses row-by-row gradient blend (no hard seam at center)
      - Neck geometry connects head to torso (no floating head)
      - Reaching arm has elbow break for anatomical plausibility
    """
    luma_x = luma_cx
    y_base = luma_base_y

    # ── LEAN OFFSET: torso top is shifted rightward to simulate forward lean ─
    # Luma leans toward the monitor wall (right).
    # torso_top_x_offset: how many px to shift the torso top edge toward screen
    # Cycle 10 fix (Victoria Ashford P2): 28px was ~9° — "watching TV" lean, not urgency.
    # Increased to 48px (~16°) for genuine active engagement toward the screen/Byte.
    lean_offset = 48  # pixels rightward lean at torso top vs torso bottom

    # ── LEGS — jeans, seated (bent knees, foreshortened) ─────────────────
    # Left leg (near camera)
    draw.polygon([
        (luma_x - 48, y_base),
        (luma_x - 20, y_base),
        (luma_x - 15, y_base - 90),
        (luma_x - 50, y_base - 88),
    ], fill=JEANS)
    # Right leg (slightly behind)
    draw.polygon([
        (luma_x + 14, y_base),
        (luma_x + 44, y_base - 4),
        (luma_x + 46, y_base - 84),
        (luma_x + 12, y_base - 86),
    ], fill=JEANS)
    # Jeans shadow (lavender ambient on shadow side)
    draw.polygon([
        (luma_x - 50, y_base - 88),
        (luma_x - 48, y_base),
        (luma_x - 34, y_base - 2),
        (luma_x - 32, y_base - 86),
    ], fill=JEANS_SH)
    # Shoes (chunky sneakers — Luma's silhouette hook)
    # Canvas = WARM_CREAM (RW-01, #FAF0DC); Sole = DEEP_COCOA (RW-12, #3B2820).
    # Aliases removed (Cycle 9): SHOE_CANVAS and SHOE_SOLE were local duplicates of module constants.
    # Left shoe
    draw.rectangle([luma_x - 60, y_base - 10, luma_x - 8, y_base + 22],
                   fill=WARM_CREAM)
    draw.rectangle([luma_x - 62, y_base + 16, luma_x - 6, y_base + 26],
                   fill=DEEP_COCOA)
    # Right shoe
    draw.rectangle([luma_x + 2,  y_base - 10, luma_x + 58, y_base + 20],
                   fill=WARM_CREAM)
    draw.rectangle([luma_x,      y_base + 16, luma_x + 60, y_base + 26],
                   fill=DEEP_COCOA)

    # ── TORSO — hoodie, gradient blended warm/cool (no hard seam) ─────────
    torso_height = 170
    torso_top    = y_base - 260
    torso_bot    = y_base - 90
    torso_half_w = 44  # half-width at base

    # Row-by-row gradient: warm HOODIE_ORANGE (left) blends to HOODIE_CYAN_LIT (right)
    # with lean: top row is shifted +lean_offset right vs bottom row
    for row in range(torso_bot, torso_top, -1):
        t_y = (torso_bot - row) / max(1, torso_bot - torso_top)  # 0=bottom, 1=top
        row_lean = int(lean_offset * t_y)
        x_left   = luma_x - torso_half_w + row_lean
        x_right  = luma_x + torso_half_w + row_lean
        width    = x_right - x_left
        # Blend warm/cool: left pixel warm, right pixel cool, smooth gradient
        for col in range(x_left, x_right + 1):
            t_x = (col - x_left) / max(1, width)
            r_v = int(HOODIE_ORANGE[0] * (1 - t_x) + HOODIE_CYAN_LIT[0] * t_x)
            g_v = int(HOODIE_ORANGE[1] * (1 - t_x) + HOODIE_CYAN_LIT[1] * t_x)
            b_v = int(HOODIE_ORANGE[2] * (1 - t_x) + HOODIE_CYAN_LIT[2] * t_x)
            draw.point((col, row), fill=(r_v, g_v, b_v))

    # Hoodie shadow underside — Cycle 9 fix (Alex Chen / Naomi Bridges); arithmetic corrected Cycle 10:
    # Underside faces down; away from lamp, away from monitor — receives lavender ambient only.
    # Under three-light theory the underside must trend cool, but retain hoodie orange identity.
    # HOODIE_AMBIENT (CHAR-L-08, #B36250) = HOODIE_SHADOW 70/30 blend with DUSTY_LAVENDER → (179,98,80).
    # Cycle 9 had #B06040 (176,96,64) — incorrect blue channel. Corrected Cycle 10 per Naomi C9-5.
    # Replaced SHADOW_PLUM (#5C4A72) which had no orange component and read as a separate material.
    draw.polygon([
        (luma_x - torso_half_w, torso_bot - 8),
        (luma_x - torso_half_w, torso_bot),
        (luma_x + torso_half_w, torso_bot),
        (luma_x + torso_half_w, torso_bot - 8),
    ], fill=HOODIE_AMBIENT)
    # Pixel accents on hoodie (Electric Cyan — shared visual DNA per style guide)
    for i in range(5):
        px_off = luma_x - 24 + i * 12 + int(lean_offset * 0.5)
        py_off = torso_top + 40
        draw.rectangle([px_off, py_off, px_off + 8, py_off + 6],
                       fill=ELEC_CYAN)
    # Warm rim light on lamp-facing left edge (leans with body)
    draw.line([(luma_x - torso_half_w, torso_top),
               (luma_x - torso_half_w, torso_bot)],
              fill=SOFT_GOLD, width=4)

    # ── NECK — connects head to torso (no floating head) ──────────────────
    # Neck is a short trapezoid between collar top and head base
    torso_top_cx = luma_x + int(lean_offset * 1.0)  # lean applies fully at torso top
    neck_w_bot = 22  # wider at torso (collar)
    neck_w_top = 18  # narrower at head
    neck_top_y = torso_top - 30
    neck_bot_y = torso_top + 10
    draw.polygon([
        (torso_top_cx - neck_w_bot, neck_bot_y),
        (torso_top_cx + neck_w_bot, neck_bot_y),
        (torso_top_cx + neck_w_top, neck_top_y),
        (torso_top_cx - neck_w_top, neck_top_y),
    ], fill=SKIN)
    # Neck side shading
    draw.line([(torso_top_cx - neck_w_top, neck_top_y),
               (torso_top_cx - neck_w_bot, neck_bot_y)],
              fill=SKIN_SH, width=2)

    # ── REACHING ARM — elbow break for anatomical plausibility ───────────
    # Arm starts at torso right-top, elbow midway, hand at target
    # With lean, shoulder shifts right
    arm_x_start  = luma_x + torso_half_w + int(lean_offset * 0.8)
    arm_y_start  = torso_top + 60
    arm_x_target = facing_monitor_x
    arm_y_target = arm_y_start - 30

    # Elbow break — midpoint with slight upward arc (arm reaches forward+up)
    elbow_x = (arm_x_start + arm_x_target) // 2
    elbow_y = arm_y_start - 20  # elbow slightly higher than shoulder line

    # Upper arm (shoulder to elbow) — warm-side, SKIN base
    draw.line([(arm_x_start, arm_y_start), (elbow_x, elbow_y)],
              fill=SKIN, width=22)
    # Forearm (elbow to hand) — cyan-lit (closer to screen)
    draw.line([(elbow_x, elbow_y), (arm_x_target, arm_y_target)],
              fill=CYAN_SKIN, width=18)
    # Elbow cap
    draw.ellipse([elbow_x - 12, elbow_y - 12, elbow_x + 12, elbow_y + 12],
                 fill=SKIN)
    # Hand — reaching, fingers extended toward Byte
    hand_cx = arm_x_target
    hand_cy = arm_y_target
    draw.ellipse([hand_cx - 18, hand_cy - 12, hand_cx + 18, hand_cy + 12],
                 fill=CYAN_SKIN, outline=LINE, width=2)
    # Fingers spread open
    for fi in range(4):
        fx0 = hand_cx - 12 + fi * 8
        draw.line([(fx0, hand_cy - 10), (fx0 + 6, hand_cy - 32)],
                  fill=CYAN_SKIN, width=5)
    # Thumb
    draw.line([(hand_cx - 16, hand_cy + 4),
               (hand_cx - 28, hand_cy + 16)],
              fill=CYAN_SKIN, width=5)
    # Warm rim on lamp-facing (upper) side of arm
    draw.line([(arm_x_start, arm_y_start - 8), (elbow_x - 4, elbow_y - 8)],
              fill=SOFT_GOLD, width=3)

    # ── RESTING ARM (left arm, on couch armrest, lamp-warm side) ──────────
    rest_arm_x = luma_x - torso_half_w
    rest_arm_y = torso_top + 100
    draw.line([(rest_arm_x, rest_arm_y),
               (rest_arm_x - 40, rest_arm_y + 60)],
              fill=HOODIE_ORANGE, width=18)
    draw.ellipse([rest_arm_x - 56, rest_arm_y + 52,
                  rest_arm_x - 20, rest_arm_y + 80],
                 fill=SKIN, outline=LINE, width=2)

    # head position: shifted by lean at torso top
    head_cx = torso_top_cx
    head_cy = torso_top - 10

    return {"head_cx": head_cx, "head_cy": head_cy,
            "hand_cx": arm_x_target, "hand_cy": arm_y_target}


# ── Luma's Face ───────────────────────────────────────────────────────────────
def draw_luma_head(draw, cx, cy, scale=1.0):
    """
    Draw Luma's head: Reckless Excitement expression.
    From luma_face_generator.py draw_reckless_excitement() — adapted with scale.
    Three-light on face:
      - Left side (lamp): warm skin highlight (SKIN_HL)
      - Right side (monitor): cyan-lit skin (CYAN_SKIN)
      - Ambient: DUSTY_LAVENDER in shadow areas
    """
    s = scale
    head_r = int(100 * s)

    def p(v):
        return int(v * s)

    # ── Hair mass (behind head) ─────────────────────────────────────────────
    # Big, dark, cloud-like hair — Luma's primary silhouette hook
    draw.ellipse([cx - p(155), cy - p(195), cx + p(145), cy + p(40)], fill=HAIR_COLOR)
    draw.ellipse([cx - p(175), cy - p(170), cx - p(80),  cy - p(60)], fill=HAIR_COLOR)
    draw.ellipse([cx - p(165), cy - p(140), cx - p(95),  cy - p(30)], fill=HAIR_COLOR)
    draw.ellipse([cx + p(80),  cy - p(160), cx + p(155), cy - p(60)], fill=HAIR_COLOR)
    draw.ellipse([cx + p(90),  cy - p(130), cx + p(145), cy - p(40)], fill=HAIR_COLOR)
    draw.ellipse([cx - p(60),  cy - p(215), cx + p(20),  cy - p(140)], fill=HAIR_COLOR)
    draw.ellipse([cx - p(20),  cy - p(225), cx + p(70),  cy - p(145)], fill=HAIR_COLOR)
    draw.ellipse([cx - p(100), cy - p(200), cx - p(30),  cy - p(130)], fill=HAIR_COLOR)

    # ── Head — skin fill, split-lit ────────────────────────────────────────
    # Base skin
    draw.ellipse([cx - head_r, cy - head_r, cx + head_r, cy + head_r + p(15)],
                 fill=SKIN, outline=LINE, width=3)
    # Chin
    draw.ellipse([cx - p(95), cy - p(20), cx + p(95), cy + head_r + p(25)], fill=SKIN)
    draw.arc([cx - p(95), cy - p(20), cx + p(95), cy + head_r + p(25)],
             start=0, end=180, fill=LINE, width=3)
    # Ears
    draw.ellipse([cx - head_r - p(12), cy - p(20), cx - head_r + p(14), cy + p(20)],
                 fill=SKIN, outline=LINE, width=2)
    draw.ellipse([cx + head_r - p(14), cy - p(20), cx + head_r + p(12), cy + p(20)],
                 fill=SKIN, outline=LINE, width=2)
    # Warm lamp highlight — left side of face
    draw.arc([cx - head_r, cy - head_r, cx, cy + head_r + p(15)],
             start=120, end=240, fill=SKIN_HL, width=6)
    # Cyan screen light — right cheek/jaw edge
    draw.arc([cx, cy - p(20), cx + head_r + p(12), cy + head_r + p(25)],
             start=300, end=60, fill=CYAN_SKIN, width=5)
    # Lavender ambient fill — underside (chin, below jaw)
    draw.arc([cx - p(60), cy + p(40), cx + p(60), cy + head_r + p(30)],
             start=0, end=180, fill=DUSTY_LAVENDER, width=4)

    # ── Eyes — ASYMMETRIC (reckless excitement) ────────────────────────────
    lex, ley = cx - p(38), cy - p(18)
    rex, rey = cx + p(38), cy - p(18)
    ew = p(28)

    # Eye rendering colors — local to draw_luma_head(). Not in master_palette.md:
    # these are micro-detail values for a single character's eyes at 1920x1080 scale.
    # They are derived from palette values but are too granular to be standalone palette entries.
    # EYE_W_C: near-warm-white sclera, derived from WARM_CREAM (RW-01, #FAF0DC) pushed slightly brighter.
    # EYE_PUP: very dark warm brown pupil, derived from DEEP_COCOA (RW-11, #3B2820) pushed darker.
    # EYE_IRIS: warm brown iris, ≈ mid-value between SKIN (#C8885A) and DEEP_COCOA (#3B2820).
    EYE_W_C = (255, 252, 245)
    EYE_PUP = ( 20,  12,   8)
    EYE_IRIS= ( 60,  38,  20)

    # Left eye (more open — dominant reckless side)
    leh = p(30)
    draw.ellipse([lex - ew, ley - leh, lex + ew, ley + leh],
                 fill=EYE_W_C, outline=LINE, width=2)
    iris_r = p(15)
    draw.chord([lex - iris_r, ley - iris_r + p(2), lex + iris_r, ley + iris_r + p(2)],
               start=15, end=345, fill=EYE_IRIS)
    draw.ellipse([lex - p(9), ley - p(7), lex + p(9), ley + p(9)], fill=EYE_PUP)
    # Pupil highlight — shifted right (looking at monitor/Byte)
    draw.ellipse([lex + p(4), ley - p(10), lex + p(12), ley - p(2)], fill=EYE_W_C)
    # Cyan reflection in left eye (monitor light)
    # (0, 180, 200, 60): semi-transparent cyan eye reflection — RGBA, 60/255 alpha (~24%).
    # Not in palette: this is a micro-detail RGBA rendering pass specific to the eye interior.
    # The color is a desaturated variant of GL-02 Deep Cyan — correct for monitor light on wet surface.
    draw.ellipse([lex - p(6), ley - p(4), lex + p(6), ley + p(6)],
                 fill=(0, 180, 200, 60))
    # Upper eyelid emphasis (engagement)
    draw.arc([lex - ew, ley - leh, lex + ew, ley + leh],
             start=200, end=340, fill=LINE, width=4)

    # Right eye (normal open, pupils both shifted toward monitor)
    reh = p(26)
    draw.ellipse([rex - ew, rey - reh, rex + ew, rey + reh],
                 fill=EYE_W_C, outline=LINE, width=2)
    draw.chord([rex - iris_r, rey - iris_r + p(2), rex + iris_r, rey + iris_r + p(2)],
               start=15, end=345, fill=EYE_IRIS)
    pupil_shift = p(5)
    draw.ellipse([rex - p(9) + pupil_shift, rey - p(7),
                  rex + p(9) + pupil_shift, rey + p(9)], fill=EYE_PUP)
    draw.ellipse([rex + p(4) + pupil_shift, rey - p(10),
                  rex + p(12) + pupil_shift, rey - p(2)], fill=EYE_W_C)
    draw.arc([rex - ew, rey - reh, rex + ew, rey + reh],
             start=200, end=340, fill=LINE, width=4)
    # Left pupil also shifted right
    draw.ellipse([lex - p(9) + pupil_shift, ley - p(7),
                  lex + p(9) + pupil_shift, ley + p(9)], fill=EYE_PUP)

    # ── Brows — ASYMMETRIC (reckless excitement signature) ────────────────
    # Left brow: higher + kinked outer corner
    l_brow = [(lex - p(30), ley - p(42)), (lex - p(5), ley - p(52)), (lex + p(22), ley - p(39))]
    draw.line(l_brow, fill=HAIR_COLOR, width=5)
    # Right brow: lower, clean arch
    r_brow = [(rex - p(22), rey - p(34)), (rex - p(5), rey - p(40)), (rex + p(28), rey - p(32))]
    draw.line(r_brow, fill=HAIR_COLOR, width=5)

    # ── Nose ───────────────────────────────────────────────────────────────
    draw.ellipse([cx - p(8), cy + p(8), cx - p(2), cy + p(14)], fill=SKIN_SH)
    draw.ellipse([cx + p(2), cy + p(8), cx + p(8), cy + p(14)], fill=SKIN_SH)
    draw.arc([cx - p(6), cy - p(10), cx + p(6), cy + p(12)],
             start=200, end=340, fill=SKIN_SH, width=2)

    # ── Mouth — asymmetric grin (LEFT corner pulled higher) ───────────────
    m_off = -p(6)  # shift left — reckless dominant side
    # Main grin arc
    draw.arc([cx - p(45) + m_off, cy + p(18), cx + p(45) + m_off, cy + p(70)],
             start=5, end=175, fill=LINE, width=4)
    # Teeth
    draw.chord([cx - p(42) + m_off, cy + p(22), cx + p(42) + m_off, cy + p(65)],
               start=7, end=173, fill=(250, 246, 238))
    draw.arc([cx - p(42) + m_off, cy + p(22), cx + p(42) + m_off, cy + p(65)],
             start=7, end=173, fill=LINE, width=2)
    # Bottom lip
    draw.arc([cx - p(20) + m_off, cy + p(62), cx + p(26) + m_off, cy + p(76)],
             start=5, end=175, fill=SKIN_SH, width=2)
    # Dimple (dominant left)
    draw.arc([cx - p(50), cy + p(25), cx - p(30), cy + p(45)],
             start=320, end=60, fill=SKIN_SH, width=2)

    # ── Blush — soft flush, outer cheeks ─────────────────────────────────
    # Use RGBA composite so blush is semi-transparent (no hard ring artifact).
    # Draw blush onto a temporary RGBA layer and composite onto the base image.
    base_img = draw._image
    blush_layer = Image.new("RGBA", base_img.size, (0, 0, 0, 0))
    blush_draw  = ImageDraw.Draw(blush_layer)
    blush_alpha = 80  # semi-transparent — soft flush, not solid fill
    blush_draw.ellipse([cx - head_r + p(6), cy + p(4), cx - head_r + p(62), cy + p(40)],
                       fill=(*BLUSH_LEFT, blush_alpha))
    blush_draw.ellipse([cx + head_r - p(62), cy + p(4), cx + head_r - p(6), cy + p(40)],
                       fill=(*BLUSH_RIGHT, blush_alpha))
    base_rgba = base_img.convert("RGBA")
    base_rgba = Image.alpha_composite(base_rgba, blush_layer)
    # Write composite result back into the image the draw object wraps
    base_img.paste(base_rgba.convert("RGB"))

    # ── Hair overlay — stray curls over forehead ──────────────────────────
    draw.arc([cx - p(60), cy - p(195), cx - p(10), cy - p(140)],
             start=30, end=200, fill=HAIR_COLOR, width=8)
    draw.arc([cx - p(20), cy - p(190), cx + p(40), cy - p(130)],
             start=10, end=190, fill=HAIR_COLOR, width=7)

    # ── Collar — hoodie visible at neck ───────────────────────────────────
    collar_offset = p(6)  # slight right tilt (head leaning toward monitor)
    draw.ellipse([cx - p(90) + collar_offset, cy + head_r + p(10),
                  cx + p(90) + collar_offset, cy + head_r + p(80)],
                 fill=HOODIE_ORANGE)
    draw.arc([cx - p(90) + collar_offset, cy + head_r + p(10),
              cx + p(90) + collar_offset, cy + head_r + p(80)],
             start=180, end=360, fill=LINE, width=3)
    # Pixel accents on collar
    for i in range(5):
        px = cx - p(35) + collar_offset + i * p(15)
        py = cy + head_r + p(35)
        draw.rectangle([px, py, px + p(10), py + p(8)], fill=(0, 240, 255))


# ── Byte ──────────────────────────────────────────────────────────────────────
def draw_byte(draw, emerge_cx, emerge_cy, emerge_rx, emerge_ry, luma_hand_x, luma_hand_y):
    """
    Draw Byte emerging from the CRT screen.
    - Body fill: BYTE_TEAL (#00D4E8) — NOT Electric Cyan (figure-ground separation)
    - Corrupted Amber elliptical outline (GL-07, cyan-dominant environment)
    - ALARMED/CURIOUS expression — one pixel eye '!' (surprise at Luma)
    - Arm/tendril reaching toward Luma
    - Body half-submerged in screen (lower half still inside screen plane)
    """
    byte_cx = emerge_cx
    byte_cy = emerge_cy - int(emerge_ry * 0.20)  # slightly above screen center
    byte_rx = int(emerge_rx * 0.78)
    byte_ry = int(emerge_ry * 0.80)

    # ── Body emergence effect — screen distortion behind Byte ─────────────
    # Digital "push-through" distortion rings
    for i in range(3):
        dist_rx = byte_rx + 12 + i * 10
        dist_ry = byte_ry + 8 + i * 7
        draw.ellipse([byte_cx - dist_rx, byte_cy - dist_ry,
                      byte_cx + dist_rx, byte_cy + dist_ry],
                     outline=(0, 168 + i * 20, 180 + i * 18), width=2)

    # ── Body fill — BYTE_TEAL (GL-01b) ───────────────────────────────────
    draw.ellipse([byte_cx - byte_rx, byte_cy - byte_ry,
                  byte_cx + byte_rx, byte_cy + byte_ry],
                 fill=BYTE_TEAL)

    # ── Body highlight (top-left — lamp warm bounce, subtle) ──────────────
    hl_rx = int(byte_rx * 0.5)
    hl_ry = int(byte_ry * 0.4)
    draw_filled_glow(draw, byte_cx - int(byte_rx * 0.2), byte_cy - int(byte_ry * 0.25),
                     hl_rx, hl_ry,
                     glow_rgb=(0, 240, 255),  # BYTE_HL
                     bg_rgb=BYTE_TEAL,
                     steps=6)

    # ── Body shadow (bottom — ambient lavender fill) ───────────────────────
    sh_rx = int(byte_rx * 0.7)
    sh_ry = int(byte_ry * 0.35)
    draw_filled_glow(draw, byte_cx, byte_cy + int(byte_ry * 0.45),
                     sh_rx, sh_ry,
                     glow_rgb=(0, 100, 130),
                     bg_rgb=BYTE_TEAL,
                     steps=5)

    # ── Body lower half fades into screen (submerged effect) ──────────────
    # Cycle 9 fix (Victoria Ashford P1): submerge fade was drawn AFTER screen-glow, painting
    # near-black rows over the same zone (byte_cy+0.50 to ~0.85*byte_ry). The glow was
    # overwritten and invisible. Fix: draw submerge fade FIRST, then screen-glow on top.
    # Byte's lower body merges back into the near-void dark pocket at emergence zone.
    # Interpolate BYTE_TEAL → (14, 14, 30) [the void pocket color actually behind Byte].
    # NOT toward ELEC_CYAN — Byte emerges from a dark void, not a bright cyan background.
    VOID_POCKET = (14, 14, 30)
    submerge_y = byte_cy + int(byte_ry * 0.50)
    screen_top = emerge_cy + int(emerge_ry * 0.20)
    if submerge_y < screen_top:
        submerge_y = screen_top
    for row_offset in range(0, int(byte_ry * 0.38), 4):
        y_row = submerge_y + row_offset
        t_fade = row_offset / max(1, int(byte_ry * 0.38))
        fade_rx = int(byte_rx * (1 - t_fade * 0.3))
        col = (
            int(VOID_POCKET[0] * t_fade + BYTE_TEAL[0] * (1 - t_fade)),
            int(VOID_POCKET[1] * t_fade + BYTE_TEAL[1] * (1 - t_fade)),
            int(VOID_POCKET[2] * t_fade + BYTE_TEAL[2] * (1 - t_fade)),
        )
        draw.line([(byte_cx - fade_rx, y_row), (byte_cx + fade_rx, y_row)],
                  fill=col, width=4)

    # ── Screen-sourced upward cyan fill on Byte's underbody (Victoria Ashford Cycle 8) ──
    # Drawn AFTER submerge fade so the glow is not overwritten by the fade's near-black rows.
    # Cycle 9 fix: moved here from after charged-gap block (was being overwritten by submerge).
    # Byte emerges from a glowing CRT screen. The screen below illuminates the underbody
    # with an upward-cast cyan glow. Without this Byte reads as composited-in.
    underbody_cx = byte_cx
    underbody_cy = byte_cy + int(byte_ry * 0.55)  # bottom quarter of body
    screen_glow_rx = int(byte_rx * 0.80)
    screen_glow_ry = int(byte_ry * 0.30)
    draw_filled_glow(draw, underbody_cx, underbody_cy,
                     screen_glow_rx, screen_glow_ry,
                     glow_rgb=ELEC_CYAN,          # bright cyan from CRT below
                     bg_rgb=BYTE_TEAL,
                     steps=8)

    # ── Corrupted Amber outline — ELLIPTICAL (Naomi Bridges Cycle 6 fix) ──
    # Cycle 8 fix (Naomi Bridges): GL-07 standard = width=3 at 1920x1080. Was 5.
    draw_amber_outline(draw, byte_cx, byte_cy, byte_rx, byte_ry, width=3)

    # ── EYES — pixel-based expression system ──────────────────────────────
    # Left eye: '!' (surprise/alarmed — Byte sees Luma!)
    eye_size = max(8, int(byte_rx * 0.22))
    lex_b = byte_cx - int(byte_rx * 0.30)
    ley_b = byte_cy - int(byte_ry * 0.12)
    # Pixel ! symbol
    draw.rectangle([lex_b - eye_size // 2, ley_b - eye_size,
                    lex_b + eye_size // 2, ley_b + eye_size // 3],
                   fill=ELEC_CYAN)
    draw.rectangle([lex_b - eye_size // 2, ley_b + eye_size // 2,
                    lex_b + eye_size // 2, ley_b + eye_size],
                   fill=ELEC_CYAN)

    # Right eye: wide scared/surprised (right eye carries emotion — Cycle 6 rule)
    rex_b = byte_cx + int(byte_rx * 0.30)
    rey_b = byte_cy - int(byte_ry * 0.12)
    r_eye_w = int(byte_rx * 0.36)
    r_eye_h = int(byte_ry * 0.36)
    draw.ellipse([rex_b - r_eye_w, rey_b - r_eye_h,
                  rex_b + r_eye_w, rey_b + r_eye_h],
                 fill=(240, 240, 245), outline=LINE, width=2)
    # Pupil — wide, slightly shifted toward Luma (screen left)
    pupil_r = int(r_eye_w * 0.55)
    draw.ellipse([rex_b - pupil_r - 4, rey_b - pupil_r,
                  rex_b + pupil_r - 4, rey_b + pupil_r],
                 fill=LINE)
    # Highlight in right eye
    draw.ellipse([rex_b - int(r_eye_w * 0.2) - 4, rey_b - int(r_eye_h * 0.4),
                  rex_b + int(r_eye_w * 0.1) - 4, rey_b],
                 fill=ELEC_CYAN)

    # ── Scar/crack detail — Byte's glitch mark ────────────────────────────
    scar_x = byte_cx + int(byte_rx * 0.10)
    scar_y = byte_cy - int(byte_ry * 0.30)
    draw.line([(scar_x, scar_y), (scar_x + int(byte_rx * 0.18), scar_y + int(byte_ry * 0.22))],
              fill=SCAR_MAG, width=3)
    draw.line([(scar_x + int(byte_rx * 0.06), scar_y + int(byte_ry * 0.08)),
               (scar_x + int(byte_rx * 0.24), scar_y + int(byte_ry * 0.16))],
              fill=SCAR_MAG, width=2)

    # ── Reaching tendril/arm toward Luma ──────────────────────────────────
    # Byte extends a tendril from its left edge toward Luma's hand
    arm_start_x = byte_cx - byte_rx
    arm_start_y = byte_cy + int(byte_ry * 0.10)
    # Tendril curves through the screen plane toward Luma
    tendril_pts = []
    target_x = luma_hand_x
    target_y = luma_hand_y
    steps = 20
    # Cycle 8 fix (Victoria Ashford): cp1x was arm_start_x - byte_rx*0.8 (leftward, away from Luma).
    # Fixed: cp1 is placed between Byte and Luma so the tendril arcs TOWARD her from the start.
    for i in range(steps + 1):
        t = i / steps
        # cp1: one-third of the way from Byte toward Luma, slightly upward arc
        cp1x = arm_start_x + int((target_x - arm_start_x) * 0.33)
        cp1y = arm_start_y - int(byte_ry * 0.5)
        # Simplified quadratic bezier with corrected control point
        px = int((1-t)**2 * arm_start_x + 2*(1-t)*t * cp1x + t**2 * target_x)
        py = int((1-t)**2 * arm_start_y + 2*(1-t)*t * cp1y + t**2 * target_y)
        tendril_pts.append((px, py))
    # Draw tendril (thicker near body, thinner toward tip)
    for i in range(len(tendril_pts) - 1):
        thickness = max(2, int(8 * (1 - i / len(tendril_pts))))
        draw.line([tendril_pts[i], tendril_pts[i+1]],
                  fill=BYTE_TEAL, width=thickness)
    # Tendril tip highlight
    if tendril_pts:
        tx, ty = tendril_pts[-1]
        draw.ellipse([tx - 8, ty - 8, tx + 8, ty + 8], fill=ELEC_CYAN)

    # ── Charged gap — luminous event between tendril tip and Luma's hand (Victoria #2) ──
    # The space between the two hands is the emotional center of the frame.
    # Add a soft pixel-scatter and a subtle glow in this gap to make it feel "charged."
    gap_cx = (tendril_pts[-1][0] + luma_hand_x) // 2 if tendril_pts else luma_hand_x - 40
    gap_cy = (tendril_pts[-1][1] + luma_hand_y) // 2 if tendril_pts else luma_hand_y
    # Soft cyan glow filling the gap zone — the space between them resonates
    draw_filled_glow(draw, gap_cx, gap_cy,
                     rx=55, ry=38,
                     glow_rgb=(180, 255, 255),
                     bg_rgb=(40, 30, 50),
                     steps=10)
    # Pixel scatter in the gap — energy bridging the two figures
    rng_gap = random.Random(77)
    for _ in range(18):
        spx = gap_cx + rng_gap.randint(-52, 52)
        spy = gap_cy + rng_gap.randint(-32, 32)
        sps = rng_gap.choice([2, 3, 4])
        spc = rng_gap.choice([ELEC_CYAN, STATIC_WHITE, (180, 255, 255)])
        draw.rectangle([spx, spy, spx + sps, spy + sps], fill=spc)


# ── Three-Light Overlay ───────────────────────────────────────────────────────
def draw_lighting_overlay(img, W, H, lamp_x, lamp_y, monitor_cx, monitor_cy):
    """
    Apply three-light atmospheric room fill over the full frame as RGBA composites.

    Cycle 7 implementation (was 'pass' in Cycle 6):
      1. WARM GOLD pool — left zone, low-opacity filled glow from lamp source
         Simulates warm lamp light pooling on floor/wall left of center.
      2. COLD CYAN wash — right zone, wide low-opacity fill from monitor wall
         Simulates the monitor wall's blue-green light flooding the right half.

    Both layers are drawn in RGBA so they add light without destroying
    the background detail drawn underneath.
    """
    # ── Warm gold pool (left zone — lamp source) ─────────────────────────
    warm_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    warm_draw  = ImageDraw.Draw(warm_layer)
    # Large filled gradient ellipse: centered below lamp, spreads downward to floor
    lamp_glow_cx = lamp_x + 32
    lamp_glow_cy = lamp_y + int(H * 0.35)
    for step in range(14, 0, -1):
        t   = step / 14
        rx  = int(W * 0.30 * t)
        ry  = int(H * 0.55 * t)
        # Cycle 8 fix (Victoria + Naomi): raised from alpha=28 to alpha=70
        # Old alpha of 28 (~11%) was functionally invisible. 70 (~27%) is perceptible.
        alpha = int(70 * (1 - t))
        warm_draw.ellipse(
            [lamp_glow_cx - rx, lamp_glow_cy - ry,
             lamp_glow_cx + rx, lamp_glow_cy + ry],
            fill=(*SOFT_GOLD, alpha)
        )
    # Composite warm layer onto image (left of center only — mask right half out)
    warm_np = warm_layer.crop((0, 0, W // 2, H))
    base_left  = img.crop((0, 0, W // 2, H)).convert("RGBA")
    composited_left = Image.alpha_composite(base_left, warm_np)
    img.paste(composited_left.convert("RGB"), (0, 0))

    # ── Cold cyan wash (right zone — monitor wall source) ────────────────
    cold_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cold_draw  = ImageDraw.Draw(cold_layer)
    # Wide low-opacity ellipse: centered on monitor wall, floods right half + spills left
    for step in range(14, 0, -1):
        t   = step / 14
        rx  = int(W * 0.55 * t)
        ry  = int(H * 0.65 * t)
        # Cycle 8 fix (Victoria + Naomi): raised from alpha=22 to alpha=60
        # Old alpha of 22 (~9%) contributed nothing structural to the frame.
        alpha = int(60 * (1 - t))
        cold_draw.ellipse(
            [monitor_cx - rx, monitor_cy - ry,
             monitor_cx + rx, monitor_cy + ry],
            fill=(*ELEC_CYAN, alpha)
        )
    # Composite cold layer onto image (right half + slight 80px left spill)
    # Boundary analysis (Cycle 11 correction — Naomi Bridges C10):
    # The cold overlay crops to x=W//2-80=880. monitor_cx≈1401. Distance to boundary=521px.
    # max rx = int(W*0.55) = 1056px. At boundary, t≈521/1056≈0.49; alpha=int(60*(1-0.49))=30.
    # 30/255 = ~11.8% cold cyan opacity at the 80px warm-zone boundary.
    # DECISION: cold_alpha_max=60 retained. 11.8% cold cyan over warm skin is a cross-light
    # split-light effect — physically consistent with a monitor wall at ~3m from the couch.
    # No grey zone produced in rendered output. This is intentional warm/cold cross-lighting.
    cold_np    = cold_layer.crop((W // 2 - 80, 0, W, H))
    base_right = img.crop((W // 2 - 80, 0, W, H)).convert("RGBA")
    composited_right = Image.alpha_composite(base_right, cold_np)
    img.paste(composited_right.convert("RGB"), (W // 2 - 80, 0))

    return img


# ── Couch ─────────────────────────────────────────────────────────────────────
def draw_couch(draw, luma_cx, luma_base_y):
    """
    Draw Luma's couch.
    Couch faces the monitor wall (right). Sightline from couch to monitors.
    Warm amber/terracotta tones — domestic safety.
    """
    # Couch positioned left-of-center, angled so it faces right.
    # Cycle 9 fix (Victoria Ashford P0): old span was 768px (W*0.04 to W*0.44 = 40% of frame),
    # giving an 8.7:1 ratio vs Luma's 88px body. Target is 4:1.
    # New: couch_left = W*0.16, couch_right = W*0.38 → span ~422px (~22%), ratio ~4.8:1.
    couch_left  = int(W * 0.16)   # was int(W * 0.04)
    couch_right = int(W * 0.38)   # was int(W * 0.44)
    couch_y_bot = luma_base_y + 44
    couch_y_top = luma_base_y - 40

    # Seat trapezoid — near edge at bottom, far edge (back of couch) at top
    seat_pts = [
        (couch_left,  couch_y_bot + 10),    # front-left (near camera)
        (couch_left,  couch_y_bot - 60),    # back-left
        (couch_right, couch_y_top - 40),    # back-right (farther)
        (couch_right, couch_y_bot + 4),     # front-right
    ]
    draw.polygon(seat_pts, fill=(107, 48, 24))
    draw.polygon(seat_pts, outline=(70, 30, 14), width=3)
    # Couch cushion seam
    mid_couch_x = (couch_left + couch_right) // 2
    draw.line([(mid_couch_x - 10, couch_y_bot - 20),
               (mid_couch_x,      couch_y_top - 30)],
              fill=(80, 36, 14), width=2)
    # Couch back cushion (left side — character faces right so back is left-rear)
    # back_left_inner updated proportionally from W*0.15 to W*0.22
    back_left_inner = int(W * 0.22)
    back_pts = [
        (couch_left,       couch_y_bot - 60),
        (couch_left,       couch_y_bot - 150),
        (back_left_inner,  couch_y_top - 120),
        (back_left_inner,  couch_y_top - 50),
    ]
    draw.polygon(back_pts, fill=(128, 60, 28))
    draw.polygon(back_pts, outline=(80, 40, 16), width=2)
    # Couch arm rest (right side, near camera)
    arm_pts = [
        (couch_right,   couch_y_bot + 4),
        (couch_right,   couch_y_bot - 70),
        (couch_right + 40, couch_y_bot - 60),
        (couch_right + 40, couch_y_bot + 14),
    ]
    draw.polygon(arm_pts, fill=(115, 52, 26))
    draw.polygon(arm_pts, outline=(80, 36, 14), width=2)
    # Warm lamp rim-light on couch left face
    draw.line([(couch_left, couch_y_bot - 60),
               (couch_left, couch_y_bot + 10)],
              fill=SOFT_GOLD, width=4)
    # Couch label would go here — suppressed in final rendered version


# ── Main ──────────────────────────────────────────────────────────────────────
def generate():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    img = Image.new("RGB", (W, H), WARM_CREAM)
    draw = ImageDraw.Draw(img)

    # ── STEP 1: Background ─────────────────────────────────────────────────
    bg_data = draw_background(draw, img)
    scr_x0     = bg_data["scr_x0"]
    scr_y0     = bg_data["scr_y0"]
    scr_x1     = bg_data["scr_x1"]
    scr_y1     = bg_data["scr_y1"]
    emerge_cx  = bg_data["emerge_cx"]
    emerge_cy  = bg_data["emerge_cy"]
    emerge_rx  = bg_data["emerge_rx"]
    emerge_ry  = bg_data["emerge_ry"]

    # ── STEP 2: Couch ──────────────────────────────────────────────────────
    # luma_cx moved to 29% (was 19%) — reduces arm span to anatomically plausible range
    luma_cx    = int(W * 0.29)
    luma_base_y= int(H * 0.90)
    draw_couch(draw, luma_cx, luma_base_y)

    # ── STEP 3: Three-light atmospheric overlay (BEFORE characters) ───────
    # Cycle 9 fix (Victoria Ashford P3): overlay was applied at STEP 6 (after characters).
    # At ~27% warm alpha, this would yellow the already-warm hoodie and potentially wash out
    # the cyan arm lighting. Fixed: apply overlay now, before characters are drawn, so
    # characters receive baked-in lighting only and are not double-tinted by the overlay.
    mw_x      = bg_data["mw_x"]
    mw_y      = bg_data["mw_y"]
    mw_w      = bg_data["mw_w"]
    mw_h      = bg_data["mw_h"]
    lamp_x_pos = int(W * 0.40)
    lamp_y_pos = bg_data["ceiling_y"] + 18
    monitor_cx_pos = mw_x + mw_w // 2
    monitor_cy_pos = mw_y + mw_h // 2
    img = draw_lighting_overlay(img, W, H,
                                lamp_x=lamp_x_pos, lamp_y=lamp_y_pos,
                                monitor_cx=monitor_cx_pos, monitor_cy=monitor_cy_pos)
    draw = ImageDraw.Draw(img)

    # ── STEP 4: Luma's Body (body in warm zone, reaching arm into cold) ────
    # Arm target: toward the screen edge — body at 29% means arm span is ~28% of canvas
    # (Cycle 9 fix: comment previously said ~21%, which was false — corrected to ~28%)
    arm_target_x = scr_x0 - 20
    arm_target_y = emerge_cy + int(emerge_ry * 0.10)
    body_data = draw_luma_body(draw, luma_cx, luma_base_y, arm_target_x)

    # ── STEP 5: Luma's Head (on top of body) ──────────────────────────────
    head_cx = body_data["head_cx"]
    head_cy = body_data["head_cy"]
    draw_luma_head(draw, head_cx, head_cy, scale=0.92)

    # ── STEP 6: Byte (emerging from CRT screen) ────────────────────────────
    luma_hand_x = body_data["hand_cx"]
    luma_hand_y = body_data["hand_cy"]
    draw_byte(draw, emerge_cx, emerge_cy, emerge_rx, emerge_ry,
              luma_hand_x, luma_hand_y)

    # ── STEP 7: Top/bottom vignette (NOT corner vignette) ─────────────────
    # Darkens top and bottom edges only — warm left and cold right zones must breathe.
    # The emotional split is horizontal; vertical edges are where attention is drawn in.
    vignette = Image.new("RGB", (W, H), (0, 0, 0))
    v_alpha  = Image.new("L", (W, H), 0)
    v_draw   = ImageDraw.Draw(v_alpha)
    # Top band: darken rows near y=0
    for i in range(60):
        t = 1.0 - i / 60.0  # 1 at edge, 0 at inner
        alpha_val = int(70 * t)
        v_draw.line([(0, i), (W, i)], fill=alpha_val)
    # Bottom band: darken rows near y=H
    for i in range(60):
        t = 1.0 - i / 60.0
        alpha_val = int(70 * t)
        v_draw.line([(0, H - 1 - i), (W, H - 1 - i)], fill=alpha_val)
    img = Image.composite(vignette, img, v_alpha)
    draw = ImageDraw.Draw(img)

    # ── STEP 8: Frame title (minimal — this is a rendered frame, not a diagram)
    font_xs = load_font(16)
    # Bottom strip — very subtle title
    # (20, 12, 8): bottom title strip background — one-off UI element. Very dark warm near-black.
    # Not in palette: it is a minimal interface label strip, not a paintable production color.
    draw.rectangle([0, H - 40, W, H], fill=(20, 12, 8))
    # (180, 150, 100): title text fill — one-off UI label color; warm desaturated tan.
    # Not in palette: it is a non-character UI element. Chosen to be legible against the near-black
    # strip without being too bright (does not compete with the image above).
    draw.text((20, H - 32),
              "LUMA & THE GLITCHKIN — Frame 01: The Discovery  |  Cycle 12 — Ghost Byte",
              fill=(180, 150, 100),
              font=font_xs)

    # Cycle 12: save as new versioned file — never overwrite existing assets
    img.save(OUTPUT_PATH_V002, "PNG")
    print(f"Saved: {OUTPUT_PATH_V002}")
    return OUTPUT_PATH_V002


if __name__ == "__main__":
    generate()
