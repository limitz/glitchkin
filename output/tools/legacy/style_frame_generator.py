#!/usr/bin/env python3
"""
Style Frame Composition Generator — Luma & the Glitchkin
Generates color-blocked composition thumbnails for the three main style frames.

Cycle 5 fixes implemented:
- Frame 01: Corrupted Amber outline on Byte + monitor screen darkened at emergence point
- Frame 01: Soft Gold lamp glow moved entirely to warm zone (no overlap into Glitch monitor zone)
- Frame 02: Corrupted Amber outline applied to Byte silhouette
- Frame 03: Dark separation zone (shadow) beneath Luma on cyan platform

Cycle 6 fixes implemented:
- draw_amber_outline(): now draws offset ellipses (not rectangles) so Byte's circular
  silhouette receives a correctly shaped circular amber outline. Accepts shape="ellipse"
  (default, for Byte) or shape="rect" (for rectangular subjects if ever needed).
- Corrupted Amber outline rule: threshold-governed (35% cyan-dominant), NOT applied to
  every frame. Frame 03 (UV Purple-dominant) outline call removed per spec.
- Named all previously-unnamed inline color tuples into C dict (DRW-09, DRW-11, DRW-14,
  atmospheric structure purple, far structure void).
- Moved all import random calls to module top level.
- Screen glow in Frame 01: replaced inline arithmetic with interpolation between
  named palette values (deep_cyan → elec_cyan).

Usage: python3 style_frame_generator.py
Outputs to: /home/wipkat/team/output/color/style_frames/compositions/
"""

import sys
import os
import random
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = "/home/wipkat/team/output/color/style_frames/compositions"
W, H = 960, 540  # 16:9 thumbnail

# ---------- palette ----------
C = {
    # Real World
    "warm_cream":     (250, 240, 220),
    "soft_gold":      (232, 201,  90),
    "sunlit_amber":   (212, 146,  58),
    "terracotta":     (199,  91,  57),
    "rust_shadow":    (140,  58,  34),
    "sage_green":     (122, 158, 126),
    "dusty_lavender": (168, 155, 191),
    "shadow_plum":    ( 92,  74, 114),
    "warm_tan":       (196, 168, 130),
    "skin_shadow":    (140,  90,  56),
    "deep_cocoa":     ( 59,  40,  32),
    "muted_teal":     ( 91, 140, 138),
    "ochre_brick":    (184, 148,  74),
    "night_sky":      ( 26,  20,  40),
    # Glitch
    "elec_cyan":      (  0, 240, 255),
    "byte_teal":      (  0, 212, 232),
    "deep_cyan":      (  0, 168, 180),
    "hot_magenta":    (255,  45, 107),
    "acid_green":     ( 57, 255,  20),
    "uv_purple":      (123,  47, 190),
    "static_white":   (240, 240, 240),
    "void_black":     ( 10,  10,  20),
    "data_blue":      ( 43, 127, 255),
    "corrupted_amber":(255, 140,   0),  # GL-07 — Byte outline in cyan envs
    # Derived
    "cyan_skin":      (122, 188, 186),  # DRW-01
    "hoodie_orange":  (232, 112,  58),  # Luma hoodie
    "hoodie_shadow":  (184,  74,  32),  # hoodie shadow
    "hoodie_cyan_lit":(191, 138, 120),  # DRW-03
    # Fix: deep anchor
    "deep_shadow":    ( 42,  26,  16),  # #2A1A10 dark anchor
    # Env
    "asphalt_night":  ( 42,  42,  56),
    "asphalt_cyan":   ( 42,  90, 106),
    "roofline":       ( 26,  24,  32),
    "glitch_platform":( 26,  24,  32),  # ENV-09
    # Named derived colors (previously inline tuples — Cycle 6 fix)
    "drw_09_jacket":  (128, 192, 204),  # DRW-09 Storm-Modified Jacket (Cosmo)
    "drw_11_skin":    (168, 120, 144),  # DRW-11 Glitch Layer Skin (UV Ambient)
    "drw_14_hoodie":  (192, 112,  56),  # DRW-14 Glitch Layer Hoodie (UV Ambient)
    "atm_struct_purp":( 42,  16,  64),  # GL-04b atmospheric structure purple (far structures)
}

def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def load_font(size=14, bold=False):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()

def draw_label(draw, x, y, text, font, fill=(255, 255, 255), bg=None):
    if bg:
        bbox = draw.textbbox((x, y), text, font=font)
        draw.rectangle(bbox, fill=bg)
    draw.text((x, y), text, fill=fill, font=font)

def draw_amber_outline(draw, rect, width=3, shape="ellipse"):
    """Draw Corrupted Amber outline — the figure-ground protection rule for Byte.

    Governed by the 35% cyan-dominant threshold rule (GL-07). Only call this
    function in frames where cyan (#00F0FF + #00D4E8) exceeds 35% of background.
    Frame 01 and Frame 02 qualify. Frame 03 (UV Purple-dominant) does NOT.

    Args:
        draw: ImageDraw instance
        rect: [x0, y0, x1, y1] bounding box of the character
        width: number of offset passes (outline thickness in pixels)
        shape: "ellipse" (default, for Byte's circular body) or "rect"
               Use "ellipse" whenever drawing around a circular/elliptical character.
               Offset ellipses follow the curve correctly; offset rectangles produce
               squared corners on a round character (shape mismatch — Cycle 5 defect).
    """
    x0, y0, x1, y1 = rect
    for i in range(width):
        if shape == "ellipse":
            draw.ellipse([x0-i, y0-i, x1+i, y1+i],
                         outline=C["corrupted_amber"])
        else:
            draw.rectangle([x0-i, y0-i, x1+i, y1+i],
                           outline=C["corrupted_amber"])


# ─────────────────────────────────────────────
# FRAME 01 — THE DISCOVERY
# Fixes: Corrupted Amber outline on Byte,
#         monitor screen darkened at emergence,
#         Soft Gold lamp moved entirely to warm zone
# ─────────────────────────────────────────────
def generate_frame01():
    img = Image.new("RGB", (W, H), C["warm_cream"])
    draw = ImageDraw.Draw(img)
    font_sm = load_font(12)
    font_md = load_font(14, bold=True)
    font_lg = load_font(20, bold=True)

    # ── Background: den / bookshelves ──
    draw.rectangle([0, 0, W, H], fill=C["warm_cream"])

    # Back wall — warm cream with amber light zones
    draw.rectangle([0, 0, W, H*2//3], fill=C["warm_cream"])

    # Floor — ochre boards
    draw.rectangle([0, H*2//3, W, H], fill=C["ochre_brick"])
    # Floor grain shadows
    for y in range(H*2//3, H, 18):
        draw.line([(0, y), (W, y)], fill=C["rust_shadow"], width=1)

    # ── Bookshelves — background right ──
    shelf_x = W*2//3
    draw.rectangle([shelf_x, 0, W, H*2//3], fill=C["sunlit_amber"])
    for row in range(0, H*2//3, 40):
        book_colors = [C["terracotta"], C["sage_green"], C["dusty_lavender"],
                       C["muted_teal"], C["ochre_brick"]]
        for i, bc in enumerate(book_colors):
            bx = shelf_x + 10 + i * 34
            if bx + 28 < W:
                draw.rectangle([bx, row+4, bx+28, row+36], fill=bc)

    # ── Window — upper left (warm afternoon light source) ──
    win_rect = [30, 40, 200, 200]
    draw.rectangle(win_rect, fill=C["soft_gold"])
    draw.rectangle(win_rect, outline=C["deep_cocoa"], width=3)
    draw.line([(115, 40), (115, 200)], fill=C["deep_cocoa"], width=2)
    draw.line([(30, 120), (200, 120)], fill=C["deep_cocoa"], width=2)

    # ── LAMP — FIX: moved entirely to warm zone (left of CRT, no overlap) ──
    # The lamp glow is strictly in the warm left half of the frame.
    # It does NOT bleed into the monitor zone (right side).
    lamp_cx = W * 2 // 7  # well within warm zone, left side
    lamp_cy = H * 3 // 8
    lamp_r = 60
    # Lamp body
    draw.ellipse([lamp_cx - 12, lamp_cy - 30, lamp_cx + 12, lamp_cy],
                 fill=C["ochre_brick"], outline=C["deep_cocoa"], width=1)
    # Lamp glow — soft gold, warm zone only, hard boundary at W//2
    for r in range(lamp_r, 0, -8):
        alpha = max(40, 120 - r)
        col = (
            min(255, C["soft_gold"][0]),
            min(255, C["soft_gold"][1]),
            max(0, C["soft_gold"][2] - r)
        )
        # Only draw glow in the warm zone (left of center)
        x0 = max(0, lamp_cx - r)
        x1 = min(W // 2 - 10, lamp_cx + r)  # hard stop before monitor zone
        y0 = max(0, lamp_cy - r)
        y1 = min(H, lamp_cy + r)
        if x1 > x0:
            draw.ellipse([x0, y0, x1, y1], fill=col)
    # Redraw lamp body on top
    draw.ellipse([lamp_cx - 12, lamp_cy - 30, lamp_cx + 12, lamp_cy],
                 fill=C["ochre_brick"], outline=C["deep_cocoa"], width=2)

    # ── CRT Monitor — right of center ──
    mon_x0 = W * 9 // 16
    mon_y0 = H // 8
    mon_x1 = W * 15 // 16
    mon_y1 = H * 3 // 4
    # Monitor body (muted teal casing)
    draw.rectangle([mon_x0, mon_y0, mon_x1, mon_y1],
                   fill=C["muted_teal"], outline=C["deep_cocoa"], width=3)
    # Screen bezel
    scr_pad = 18
    scr_x0 = mon_x0 + scr_pad
    scr_y0 = mon_y0 + scr_pad
    scr_x1 = mon_x1 - scr_pad
    scr_y1 = mon_y1 - scr_pad * 3

    # FIX: Monitor screen — darkened at the emergence point where Byte appears.
    # The screen base is Electric Cyan, but the zone around Byte is shifted
    # to a near-void dark so Byte (Byte Teal) pops against it.
    # Draw base screen in cyan
    draw.rectangle([scr_x0, scr_y0, scr_x1, scr_y1], fill=C["elec_cyan"])
    # Emergence zone (upper-right of screen) — darkened to near-void
    emerge_x0 = scr_x0 + (scr_x1 - scr_x0) * 2 // 3
    emerge_y0 = scr_y0
    emerge_x1 = scr_x1
    emerge_y1 = scr_y0 + (scr_y1 - scr_y0) * 2 // 3
    draw.rectangle([emerge_x0, emerge_y0, emerge_x1, emerge_y1],
                   fill=(20, 20, 40))  # dark void at emergence — Byte pops
    # Bloom around emergence: bright cyan rim
    draw.rectangle([emerge_x0 - 4, emerge_y0 - 4,
                    emerge_x1 + 4, emerge_y1 + 4],
                   outline=C["deep_cyan"], width=3)
    # Screen edge phosphor bloom
    draw.rectangle([scr_x0, scr_y0, scr_x1, scr_y1],
                   outline=C["deep_cyan"], width=4)
    # Screen specular bezel highlight
    draw.line([(scr_x0 - 2, scr_y0 - 2), (scr_x1 + 2, scr_y0 - 2)],
              fill=C["static_white"], width=2)

    # Scan lines on screen (thin horizontal Void Black bands)
    for sy in range(scr_y0 + 4, scr_y1, 6):
        draw.line([(scr_x0, sy), (scr_x1, sy)], fill=(10, 10, 20), width=1)

    # Pixel confetti around screen
    random.seed(42)
    for _ in range(60):
        px = random.randint(scr_x0 - 80, scr_x1 + 20)
        py = random.randint(scr_y0 - 60, H * 3 // 4)
        ps = random.choice([3, 4, 5])
        pc = random.choice([C["elec_cyan"], C["static_white"]])
        draw.rectangle([px, py, px + ps, py + ps], fill=pc)

    # ── Screen glow spill on surroundings ──
    # Glow gradient interpolates from deep_cyan (inner) to elec_cyan (outer).
    # Using named palette values ensures the gradient is traceable to the palette.
    for r in range(120, 0, -15):
        gx = (scr_x0 + scr_x1) // 2
        gy = (scr_y0 + scr_y1) // 2
        mix = (120 - r) / 120.0  # 0 at outer edge (r=120), 1 at inner (r=15)
        dc = C["deep_cyan"]
        ec = C["elec_cyan"]
        col = (
            int(ec[0] * mix + dc[0] * (1 - mix)),
            int(ec[1] * mix + dc[1] * (1 - mix)),
            int(ec[2] * mix + dc[2] * (1 - mix)),
        )
        draw.ellipse([gx - r, gy - r, gx + r, gy + r], fill=col)
    # Redraw monitor body and screen on top of glow
    draw.rectangle([mon_x0, mon_y0, mon_x1, mon_y1],
                   fill=C["muted_teal"], outline=C["deep_cocoa"], width=3)
    draw.rectangle([scr_x0, scr_y0, scr_x1, scr_y1], fill=C["elec_cyan"])
    draw.rectangle([emerge_x0, emerge_y0, emerge_x1, emerge_y1],
                   fill=(20, 20, 40))
    draw.rectangle([scr_x0, scr_y0, scr_x1, scr_y1],
                   outline=C["deep_cyan"], width=4)
    for sy in range(scr_y0 + 4, scr_y1, 6):
        draw.line([(scr_x0, sy), (scr_x1, sy)], fill=(10, 10, 20), width=1)
    draw.rectangle([emerge_x0 - 4, emerge_y0 - 4,
                    emerge_x1 + 4, emerge_y1 + 4],
                   outline=C["deep_cyan"], width=3)

    # ── BYTE — emerging from screen, upper-right quadrant of screen ──
    byte_cx = emerge_x0 + (emerge_x1 - emerge_x0) // 2
    byte_cy = emerge_y0 + (emerge_y1 - emerge_y0) // 2
    byte_r = 20
    byte_rect = [byte_cx - byte_r, byte_cy - byte_r,
                 byte_cx + byte_r, byte_cy + byte_r]
    # Byte body fill — Byte Teal (not Electric Cyan)
    draw.ellipse(byte_rect, fill=C["byte_teal"])
    # FIX: Corrupted Amber outline — figure-ground protection (cyan-dominant env)
    # Per GL-01b and style_guide "environment rule — cyan-dominant scenes"
    draw_amber_outline(draw, [byte_cx - byte_r, byte_cy - byte_r,
                               byte_cx + byte_r, byte_cy + byte_r], width=3)
    # Eyes
    draw.ellipse([byte_cx - 7, byte_cy - 5, byte_cx - 1, byte_cy + 5],
                 fill=C["elec_cyan"])  # main eye
    draw.ellipse([byte_cx + 1, byte_cy - 5, byte_cx + 8, byte_cy + 5],
                 fill=C["hot_magenta"])  # cracked eye
    # Byte claw reaching toward Luma
    draw.line([(byte_cx - byte_r, byte_cy),
               (byte_cx - byte_r - 30, byte_cy + 10)],
              fill=C["byte_teal"], width=4)
    draw.ellipse([byte_cx - byte_r - 36, byte_cy + 6,
                  byte_cx - byte_r - 24, byte_cy + 18],
                 fill=C["elec_cyan"])  # claw tip highlight

    # ── LUMA — left of center ──
    luma_x = W * 5 // 16
    luma_y_base = H * 3 // 4
    # Body — simplified silhouette
    # Legs (jeans)
    draw.rectangle([luma_x - 20, luma_y_base - 80,
                    luma_x + 20, luma_y_base],
                   fill=(58, 90, 140))
    # Hoodie body — orange (screen-lit side modified to DRW-03 on right, orange on left)
    torso_rect = [luma_x - 30, luma_y_base - 160, luma_x + 30, luma_y_base - 80]
    # Left half (warm)
    draw.rectangle([luma_x - 30, luma_y_base - 160,
                    luma_x, luma_y_base - 80], fill=C["hoodie_orange"])
    # Right half (cyan-lit — DRW-03)
    draw.rectangle([luma_x, luma_y_base - 160,
                    luma_x + 30, luma_y_base - 80], fill=C["hoodie_cyan_lit"])
    # Head
    head_rect = [luma_x - 22, luma_y_base - 210, luma_x + 22, luma_y_base - 162]
    draw.ellipse(head_rect, fill=C["warm_tan"])
    # Hair
    draw.arc(head_rect, 180, 360, fill=C["deep_cocoa"], width=8)
    # Eyes
    draw.ellipse([luma_x - 12, luma_y_base - 196,
                  luma_x - 4, luma_y_base - 185], fill=C["static_white"])
    draw.ellipse([luma_x + 4, luma_y_base - 196,
                  luma_x + 12, luma_y_base - 185], fill=C["static_white"])
    draw.ellipse([luma_x - 10, luma_y_base - 194,
                  luma_x - 5, luma_y_base - 187], fill=(74, 122, 74))
    draw.ellipse([luma_x + 5, luma_y_base - 194,
                  luma_x + 10, luma_y_base - 187], fill=(74, 122, 74))
    # Reaching arm (right arm — most cyan-lit)
    # Arm extends toward the monitor
    arm_y = luma_y_base - 130
    arm_end_x = mon_x0 - 10
    draw.line([(luma_x + 30, arm_y), (arm_end_x, arm_y + 10)],
              fill=C["cyan_skin"], width=12)
    draw.ellipse([arm_end_x - 8, arm_y + 2, arm_end_x + 8, arm_y + 18],
                 fill=C["cyan_skin"])

    # Warm rim light on Luma's left side
    draw.line([(luma_x - 30, luma_y_base - 180),
               (luma_x - 30, luma_y_base - 80)],
              fill=C["soft_gold"], width=3)

    # ── Foreground desk ──
    desk_top = H * 3 // 5
    draw.rectangle([0, desk_top, mon_x0, H], fill=C["ochre_brick"])
    # Keyboard
    draw.rectangle([60, desk_top + 10, 280, desk_top + 40],
                   fill=C["dusty_lavender"], outline=C["deep_cocoa"], width=1)
    # Mug
    draw.rectangle([300, desk_top + 5, 340, desk_top + 45],
                   fill=C["terracotta"], outline=C["deep_cocoa"], width=1)
    # Cables
    draw.arc([100, desk_top + 20, 250, desk_top + 60], 0, 180,
             fill=C["deep_cocoa"], width=3)

    # ── Label ──
    draw_label(draw, 10, 10,
               "Frame 01 — The Discovery  [Cycle 5]",
               load_font(16, bold=True),
               fill=C["deep_cocoa"], bg=C["warm_cream"])
    draw_label(draw, 10, 34,
               "FIX: Byte has Corrupted Amber outline | Monitor darkened at emergence | Lamp in warm zone only",
               load_font(11), fill=C["rust_shadow"], bg=C["warm_cream"])

    out = os.path.join(OUTPUT_DIR, "frame01_discovery_composition.png")
    img.save(out)
    print(f"Saved: {out}")
    return out


# ─────────────────────────────────────────────
# FRAME 02 — GLITCH STORM
# Fix: Corrupted Amber outline on Byte
# ─────────────────────────────────────────────
def generate_frame02():
    img = Image.new("RGB", (W, H), C["night_sky"])
    draw = ImageDraw.Draw(img)
    font_sm = load_font(11)
    font_md = load_font(14, bold=True)

    # ── Sky — upper 65% ──
    # Base night sky
    draw.rectangle([0, 0, W, H * 65 // 100], fill=C["night_sky"])

    # UV Purple glitch storm masses (angular, blocky)
    storm_zones = [
        [W // 4, 0, W * 3 // 4, H // 4],
        [W // 2, 0, W, H // 3],
        [W * 3 // 8, H // 6, W * 7 // 8, H * 2 // 5],
    ]
    for z in storm_zones:
        draw.rectangle(z, fill=C["uv_purple"])

    # Void Black core in storm masses
    draw.rectangle([W // 2, H // 8, W * 3 // 4, H // 4], fill=C["void_black"])

    # ── The Crack — main jagged fracture, upper-right to lower-middle ──
    # Outer crack (Hot Magenta burning edge)
    crack_pts = [
        (W * 9 // 10, 0),
        (W * 8 // 10, H // 6),
        (W * 7 // 10, H // 4),
        (W * 65 // 100, H * 2 // 5),
        (W * 6 // 10, H // 2),
    ]
    draw.line(crack_pts, fill=C["hot_magenta"], width=10)
    # Inner crack (Electric Cyan core)
    draw.line(crack_pts, fill=C["elec_cyan"], width=5)
    # Static White center
    draw.line(crack_pts, fill=C["static_white"], width=2)

    # Sub-cracks branching
    draw.line([(W * 7 // 10, H // 4), (W * 8 // 10, H * 3 // 8)],
              fill=C["elec_cyan"], width=3)
    draw.line([(W * 65 // 100, H * 2 // 5), (W * 55 // 100, H * 3 // 8)],
              fill=C["data_blue"], width=2)

    # ── Town roofline silhouettes (mid-background) ──
    roofline_y = H * 55 // 100
    buildings = [
        (0, roofline_y, 100, H),
        (80, roofline_y - 30, 200, H),
        (180, roofline_y + 10, 300, H),
        (270, roofline_y - 20, 380, H),
        (350, roofline_y, 450, H),
        (420, roofline_y - 40, 550, H),
        (520, roofline_y + 5, 640, H),
        (610, roofline_y - 25, 730, H),
        (700, roofline_y, 820, H),
        (790, roofline_y - 15, 900, H),
        (870, roofline_y, W, H),
    ]
    for bx0, by0, bx1, by1 in buildings:
        draw.rectangle([bx0, by0, bx1, by1], fill=C["roofline"])
        # Terracotta building walls (residual warmth)
        draw.rectangle([bx0 + 2, by0 + 10, bx1 - 2, by1],
                       fill=C["terracotta"])
        # Window lights (warm cream — last safe warmth)
        for wx in range(bx0 + 8, bx1 - 8, 20):
            draw.rectangle([wx, by0 + 15, wx + 12, by0 + 28],
                           fill=C["warm_cream"])

    # ── Cyan-lit street ──
    draw.rectangle([0, H * 7 // 10, W, H], fill=C["asphalt_cyan"])
    draw.rectangle([0, H * 8 // 10, W, H], fill=C["asphalt_night"])

    # ── Pixel confetti in storm ──
    # Seed is intentionally per-function to ensure deterministic per-frame output.
    random.seed(7)
    for _ in range(120):
        px = random.randint(0, W)
        py = random.randint(0, H * 2 // 3)
        ps = random.choice([2, 3, 4])
        pc = random.choice([C["static_white"], C["elec_cyan"],
                            C["hot_magenta"], C["uv_purple"]])
        draw.rectangle([px, py, px + ps, py + ps], fill=pc)

    # ── LUMA — foreground left, running ──
    luma_x = W // 5
    luma_y = H * 65 // 100

    # Legs in motion (jeans)
    draw.polygon([(luma_x - 18, luma_y),
                  (luma_x - 5, luma_y - 60),
                  (luma_x + 5, luma_y - 60),
                  (luma_x + 18, luma_y)],
                 fill=(58, 90, 140))
    # Hoodie body
    draw.rectangle([luma_x - 25, luma_y - 120, luma_x + 25, luma_y - 60],
                   fill=C["hoodie_cyan_lit"])  # storm-modified hoodie
    # Head
    head_rect2 = [luma_x - 20, luma_y - 160, luma_x + 20, luma_y - 122]
    draw.ellipse(head_rect2, fill=C["cyan_skin"])  # DRW-08
    draw.arc(head_rect2, 180, 360, fill=C["deep_cocoa"], width=7)
    # Eyes wide
    draw.ellipse([luma_x - 10, luma_y - 152,
                  luma_x - 2, luma_y - 140], fill=C["static_white"])
    draw.ellipse([luma_x + 2, luma_y - 152,
                  luma_x + 10, luma_y - 140], fill=C["static_white"])
    # Arms pumping
    draw.line([(luma_x - 25, luma_y - 100), (luma_x - 50, luma_y - 70)],
              fill=C["cyan_skin"], width=10)
    draw.line([(luma_x + 25, luma_y - 90), (luma_x + 55, luma_y - 120)],
              fill=C["cyan_skin"], width=10)

    # ── BYTE on Luma's shoulder ──
    # FIX: Byte has Corrupted Amber outline (cyan-dominant scene)
    by_cx = luma_x + 25
    by_cy = luma_y - 135
    by_r = 10
    byte_r2 = [by_cx - by_r, by_cy - by_r, by_cx + by_r, by_cy + by_r]
    draw.ellipse(byte_r2, fill=C["byte_teal"])
    draw_amber_outline(draw, byte_r2, width=2)
    # Byte tiny eyes (scared, squeezed)
    draw.line([(by_cx - 4, by_cy - 1), (by_cx - 1, by_cy - 1)],
              fill=C["void_black"], width=2)
    draw.line([(by_cx + 1, by_cy - 1), (by_cx + 4, by_cy - 1)],
              fill=C["void_black"], width=2)

    # ── COSMO — one stride behind Luma ──
    cosmo_x = luma_x + 70
    cosmo_y = H * 67 // 100
    # Legs
    draw.polygon([(cosmo_x - 18, cosmo_y),
                  (cosmo_x - 5, cosmo_y - 55),
                  (cosmo_x + 5, cosmo_y - 55),
                  (cosmo_x + 22, cosmo_y)],
                 fill=(58, 90, 140))
    # Jacket (storm-modified dusty lavender — DRW-09)
    draw.rectangle([cosmo_x - 22, cosmo_y - 110,
                    cosmo_x + 22, cosmo_y - 55],
                   fill=C["drw_09_jacket"])
    # Head — facing viewer
    head_rect3 = [cosmo_x - 18, cosmo_y - 148, cosmo_x + 18, cosmo_y - 112]
    draw.ellipse(head_rect3, fill=C["cyan_skin"])
    draw.arc(head_rect3, 180, 360, fill=(80, 64, 48), width=6)
    # Glasses
    draw.rectangle([cosmo_x - 14, cosmo_y - 140,
                    cosmo_x - 3, cosmo_y - 126],
                   outline=C["deep_cocoa"], width=2)
    draw.rectangle([cosmo_x + 3, cosmo_y - 140,
                    cosmo_x + 14, cosmo_y - 126],
                   outline=C["deep_cocoa"], width=2)
    # Mouth open (panic)
    draw.arc([cosmo_x - 8, cosmo_y - 128, cosmo_x + 8, cosmo_y - 116],
             0, 180, fill=C["deep_cocoa"], width=2)

    # ── Shattered storefront right ──
    draw.rectangle([W * 3 // 4, H * 5 // 8, W * 9 // 10, H * 4 // 5],
                   fill=C["deep_cocoa"], outline=C["terracotta"], width=2)
    # Glitch cracks spreading from storefront
    for crack_dx, crack_dy in [(30, -20), (50, 10), (-10, 30)]:
        sx = W * 3 // 4 + 20
        sy = H * 5 // 8 + 30
        draw.line([(sx, sy), (sx + crack_dx, sy + crack_dy)],
                  fill=C["elec_cyan"], width=2)

    # ── Label ──
    draw_label(draw, 10, 10,
               "Frame 02 — Glitch Storm  [Cycle 5]",
               load_font(16, bold=True),
               fill=C["static_white"], bg=(26, 20, 40))
    draw_label(draw, 10, 34,
               "FIX: Byte has Corrupted Amber outline (small + cyan-adjacent)",
               font_sm, fill=C["corrupted_amber"], bg=(26, 20, 40))

    out = os.path.join(OUTPUT_DIR, "frame02_glitch_storm_composition.png")
    img.save(out)
    print(f"Saved: {out}")
    return out


# ─────────────────────────────────────────────
# FRAME 03 — THE OTHER SIDE
# Fix: Dark separation beneath Luma (shadow on platform)
# ─────────────────────────────────────────────
def generate_frame03():
    img = Image.new("RGB", (W, H), C["void_black"])
    draw = ImageDraw.Draw(img)
    font_sm = load_font(11)

    # ── Sky / void (Layer 5) ──
    draw.rectangle([0, 0, W, H], fill=C["void_black"])
    # Atmospheric purple gradient (simulated with bands)
    for yi in range(0, H, 4):
        frac = yi / H
        # Transition void black -> uv purple -> data blue atmosphere
        if frac < 0.5:
            mix = frac * 2
            r = int(C["void_black"][0] * (1 - mix) + C["uv_purple"][0] * mix)
            g = int(C["void_black"][1] * (1 - mix) + C["uv_purple"][1] * mix)
            b = int(C["void_black"][2] * (1 - mix) + C["uv_purple"][2] * mix)
        else:
            mix = (frac - 0.5) * 2
            r = int(C["uv_purple"][0] * (1 - mix) + 43 * mix)
            g = int(C["uv_purple"][1] * (1 - mix) + 127 * mix)
            b = int(C["uv_purple"][2] * (1 - mix) + 255 * mix)
        draw.line([(0, yi), (W, yi)], fill=(r, g, b))

    # Far distance star-like noise
    # random is imported at module top; seed is intentional for deterministic per-frame output
    random.seed(99)
    for _ in range(80):
        sx = random.randint(0, W)
        sy = random.randint(0, H // 2)
        draw.point((sx, sy), fill=C["static_white"])

    # ── Far structures (Layer 4) ──
    for i in range(6):
        fx = W // 8 + i * (W // 6)
        fy = H // 4 + random.randint(-20, 20)
        fh = random.randint(H // 6, H // 3)
        fw = random.randint(40, 90)
        draw.rectangle([fx, fy - fh, fx + fw, fy],
                       fill=C["atm_struct_purp"])  # GL-04b atmospheric depth purple

    # ── Data stream waterfalls ──
    for wx in [W // 3, W * 2 // 3, W * 5 // 6]:
        draw.line([(wx, 0), (wx, H * 3 // 4)],
                  fill=C["data_blue"], width=3)
        # Code character highlights
        for cy2 in range(0, H * 3 // 4, 12):
            if random.random() > 0.6:
                draw.rectangle([wx - 2, cy2, wx + 2, cy2 + 8],
                               fill=(106, 186, 255))  # GL-06b

    # ── Mid-distance structures (Layer 3) ──
    mid_platforms = [
        (W // 4, H // 2, W * 2 // 5, H // 2 + 20),
        (W * 3 // 5, H * 2 // 5, W * 3 // 4, H * 2 // 5 + 25),
    ]
    for px0, py0, px1, py1 in mid_platforms:
        draw.rectangle([px0, py0, px1, py1], fill=(26, 24, 50))
        # Circuit traces
        draw.line([(px0 + 5, py0 + 5), (px1 - 5, py0 + 5)],
                  fill=C["elec_cyan"], width=1)
        # Corrupted amber glow at edges (RW objects in Glitch Layer)
        draw.rectangle([px0, py0, px1, py1],
                       outline=C["corrupted_amber"], width=1)

    # ── Foreground platform — Layer 1 (where Luma stands) ──
    plat_y = H * 7 // 10
    plat_left = 0
    plat_right = W * 2 // 5
    draw.rectangle([plat_left, plat_y, plat_right, H],
                   fill=C["void_black"])
    # Circuit traces on platform
    for ty in range(plat_y + 5, H, 20):
        draw.line([(plat_left + 10, ty), (plat_right - 10, ty)],
                  fill=C["elec_cyan"], width=1)
    for tx in range(plat_left + 20, plat_right, 40):
        draw.line([(tx, plat_y), (tx, H)],
                  fill=C["data_blue"], width=1)
    # Pixel-art plants
    for plant_x in [80, 150, 220]:
        draw.rectangle([plant_x, plat_y - 18, plant_x + 14, plat_y],
                       fill=C["acid_green"])
        draw.rectangle([plant_x + 2, plat_y - 28, plant_x + 12, plat_y - 18],
                       fill=C["acid_green"])
        draw.rectangle([plant_x + 4, plat_y - 36, plant_x + 10, plat_y - 28],
                       fill=C["acid_green"])

    # ── LUMA — lower left ──
    luma_x = W * 3 // 16
    luma_y_base = plat_y

    # FIX: Dark separation zone beneath Luma on platform
    # A cast shadow shape (shadow plum deep / near-void) under her feet
    # creates clear figure-ground separation — warm skin reads against dark
    sep_pad = 14
    shadow_rect = [luma_x - sep_pad * 2, luma_y_base - 6,
                   luma_x + sep_pad * 2, luma_y_base + 10]
    draw.ellipse(shadow_rect, fill=(20, 8, 30))  # near-void dark anchor
    # Also darken the platform directly under Luma's feet
    draw.rectangle([luma_x - sep_pad, luma_y_base - 2,
                    luma_x + sep_pad, luma_y_base + 8],
                   fill=(10, 8, 20))  # void black separation strip

    # Legs (jeans — glitch-modified)
    draw.rectangle([luma_x - 15, luma_y_base - 80,
                    luma_x + 15, luma_y_base],
                   fill=(58, 80, 120))
    # Hoodie — UV-ambient modified (DRW-14)
    draw.rectangle([luma_x - 25, luma_y_base - 160,
                    luma_x + 25, luma_y_base - 80],
                   fill=C["drw_14_hoodie"])
    # Head — Glitch Layer skin (DRW-11)
    head_rect4 = [luma_x - 20, luma_y_base - 210,
                  luma_x + 20, luma_y_base - 162]
    draw.ellipse(head_rect4, fill=C["drw_11_skin"])
    draw.arc(head_rect4, 180, 360, fill=C["deep_cocoa"], width=7)
    # Eyes — wide with awe
    draw.ellipse([luma_x - 12, luma_y_base - 200,
                  luma_x - 3, luma_y_base - 188], fill=C["static_white"])
    draw.ellipse([luma_x + 3, luma_y_base - 200,
                  luma_x + 12, luma_y_base - 188], fill=C["static_white"])
    draw.ellipse([luma_x - 10, luma_y_base - 198,
                  luma_x - 5, luma_y_base - 190], fill=(74, 122, 74))
    draw.ellipse([luma_x + 5, luma_y_base - 198,
                  luma_x + 10, luma_y_base - 190], fill=(74, 122, 74))

    # ── BYTE on Luma's shoulder ──
    by_cx3 = luma_x + 28
    by_cy3 = luma_y_base - 148
    by_r3 = 12
    by_rect3 = [by_cx3 - by_r3, by_cy3 - by_r3,
                by_cx3 + by_r3, by_cy3 + by_r3]
    draw.ellipse(by_rect3, fill=C["byte_teal"])
    # Per GL-07 threshold rule and style_frame_03 spec: Frame 03 ambient is UV Purple
    # (NOT cyan-dominant). The 35% cyan threshold is NOT met. Corrupted Amber outline
    # is NOT applied here. UV Purple background provides adequate contrast for Byte Teal.
    draw.ellipse([by_cx3 - 5, by_cy3 - 3, by_cx3 - 1, by_cy3 + 3],
                 fill=C["elec_cyan"])
    draw.ellipse([by_cx3 + 1, by_cy3 - 3, by_cx3 + 5, by_cy3 + 3],
                 fill=C["hot_magenta"])

    # ── Ambient confetti ──
    random.seed(13)
    for _ in range(40):
        px = random.randint(0, W)
        py = random.randint(0, H)
        ps = random.choice([1, 2, 3])
        pc = random.choice([C["elec_cyan"], C["static_white"],
                            C["acid_green"], C["data_blue"]])
        draw.rectangle([px, py, px + ps, py + ps], fill=pc)

    # ── Label ──
    draw_label(draw, 10, 10,
               "Frame 03 — The Other Side  [Cycle 5]",
               load_font(16, bold=True),
               fill=C["static_white"], bg=(10, 10, 20))
    draw_label(draw, 10, 34,
               "FIX: Dark separation zone beneath Luma (near-void shadow on platform)",
               font_sm, fill=C["elec_cyan"], bg=(10, 10, 20))

    out = os.path.join(OUTPUT_DIR, "frame03_other_side_composition.png")
    img.save(out)
    print(f"Saved: {out}")
    return out


if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    generate_frame01()
    generate_frame02()
    generate_frame03()
    print("All style frame compositions generated.")
