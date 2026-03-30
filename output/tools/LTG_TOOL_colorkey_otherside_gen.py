#!/usr/bin/env python3
"""
LTG_TOOL_colorkey_otherside_gen.py
Color Key Generator — Style Frame 03 "The Other Side" (Scene Type: Glitch Layer — Quiet Awe)
"Luma & the Glitchkin"

Author: Sam Kowalski, Color & Style Artist
Date: 2026-03-30
Cycle: 14

Purpose:
  Generates a 640x360 color key thumbnail for the Other Side scenario (Style Frame 03).
  This is the pure digital space — the Glitch Layer in its full ambient state.
  No warm light sources. Zero warm tones as light. Warmth only as carried pigment.

  Color logic:
  - Void Black (#0A0A14) as absolute base — sky, platform material, structural fill
  - Electric Cyan (#00F0FF) dominant active color — circuit traces, ambient key light
  - UV Purple (#7B2FBE) as depth and atmospheric haze — Glitch Layer ambient fill
  - Data Stream Blue (#2B7FFF) for depth/waterfalls
  - Hot Magenta (#FF2D6B) as accent only — Byte's eye, corruption events
  - Acid Green (#39FF14) for platform flora — accent biology
  - Zero warm tones in any light source

  Scene distinctness:
  - SF01 (warm room): Soft Gold key, warm cream fill, cozy
  - SF02 (glitch storm): Cyan crack key, contested warm/cold
  - SF03 (other side): UV Purple ambient, Void Black base, vast & alien — maximally distinct

Output: /home/wipkat/team/output/color/color_keys/thumbnails/
        LTG_COLOR_colorkey_otherside.png

Usage: python3 LTG_TOOL_colorkey_otherside_gen.py

Cycle 14: Initial creation. Sam Kowalski.
"""

import os
import math
import random
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = "/home/wipkat/team/output/color/color_keys/thumbnails"
W, H = 640, 360  # 16:9 thumbnail

# ── Palette constants (all inline tuples named — no undocumented tuples) ──────

# Glitch Layer environment
VOID_BLACK       = ( 10,  10,  20)   # GL-08 — primary base fill
BELOW_VOID_BLACK = (  5,   5,   8)   # GL-08a — abyss below platform, darkest value
ELEC_CYAN        = (  0, 240, 255)   # GL-01 — circuit traces, ambient key light
HOT_MAGENTA      = (255,  45, 107)   # GL-02 — accent only (Byte cracked eye, corruption)
ACID_GREEN       = ( 57, 255,  20)   # GL-03 — platform flora, distant Glitchkin
DARK_ACID_GREEN  = ( 26, 168,   0)   # GL-03a — shadow companion to Acid Green flora
UV_PURPLE        = (123,  47, 190)   # GL-04 — atmospheric haze, ambient fill, ring mega
STATIC_WHITE     = (240, 240, 240)   # GL-05 — void static artifacts (1px "stars")
DATA_BLUE        = ( 43, 127, 255)   # GL-06 — data waterfalls, slab edges
LIGHT_DATA_BLUE  = (106, 186, 255)   # GL-06b — brightest waterfall code chars
BYTE_TEAL        = (  0, 212, 232)   # GL-01b — Byte body fill
DEEP_CYAN        = (  0, 168, 180)   # GL-01a — Byte inner glow / shadow companion
CORRUPTED_AMBER  = (255, 140,   0)   # GL-07 — RW fragment edges

# Environment / depth
ENV_09_SLAB_TOP  = ( 26,  40,  56)   # ENV-09 — slab tops under UV ambient (dark blue-grey)
ENV_10_SLAB_VERT = ( 10,  20,  32)   # ENV-10 — slab verticals, near-void, receding
ENV_11_FAR_HAZE  = ( 42,  26,  64)   # ENV-11 — far distance UV haze
ENV_12_VOID_TRAN = ( 43,  32,  80)   # ENV-12 — mid-void transition (deep dark purple)
ENV_FAR_EDGE     = ( 33,  17,  54)   # UV Purple edge at far distance (20% UV on void)

# Character colors — Luma under Glitch Layer lighting
LUMA_SKIN_GL     = (168, 120, 144)   # DRW-11 — Glitch Layer skin (lavender-washed warm)
LUMA_SKIN_SHD    = ( 90,  58,  90)   # DRW-12 — skin shadow (deep lavender-plum)
LUMA_SKIN_HLT    = ( 74, 176, 176)   # DRW-13 — skin highlight (cyan bounce from platform)
LUMA_HOODIE_GL   = (192, 112,  56)   # DRW-14 — hoodie main under UV ambient
LUMA_HOODIE_CYAN = ( 90, 168, 160)   # DRW-15 — hoodie lower hem (cyan bounce, near teal)
LUMA_HAIR        = ( 59,  40,  32)   # RW-12 / Deep Cocoa — base hair
LUMA_JEANS       = ( 38,  61,  90)   # DRW jeans base

# Real World fragment material colors (corrupted — material only, not light)
RW_TERRACOTTA    = (199,  91,  57)   # RW-04 — corrupted terracotta wall fragment

# Muted teal for corrupted lamppost
MUTED_TEAL_LAMP  = ( 91, 140, 138)   # lamppost fragment body (partially corrupted)

# Construction values (intentional one-offs with explanatory comments)
SWATCH_OUTLINE   = ( 50,  45,  70)   # palette strip border — deep purple-grey, not grey


def load_font(size=13, bold=False):
    paths = [
        ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold
         else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()


def lbl(draw, x, y, text, font, fg=(220, 240, 255), bg=None):
    """Draw a label with optional background box."""
    if bg:
        bb = draw.textbbox((x, y), text, font=font)
        draw.rectangle([bb[0]-2, bb[1]-1, bb[2]+2, bb[3]+1], fill=bg)
    draw.text((x, y), text, fill=fg, font=font)


def palette_strip(draw, swatches, x, y, sw=36, sh=26, gap=4):
    """Draw a labeled row of color swatches."""
    font = load_font(9)
    for i, (col, name) in enumerate(swatches):
        sx = x + i * (sw + gap)
        draw.rectangle([sx, y, sx + sw, y + sh], fill=col)
        draw.rectangle([sx, y, sx + sw, y + sh], outline=SWATCH_OUTLINE, width=1)
        r, g, b = col
        lum = 0.299 * r / 255 + 0.587 * g / 255 + 0.114 * b / 255
        tc = (10, 10, 20) if lum > 0.40 else (210, 235, 255)
        draw.text((sx + 2, y + 14), name[:5], fill=tc, font=font)


def generate_otherside_colorkey():
    """
    Generate the Style Frame 03 — Other Side color key thumbnail.

    Composition:
    - Void sky (upper 28%): Void Black base, ENV-12 mid-void purple, ring megastructure outline
    - Far distance (22-50%): ENV-11 haze, faint structure edges, distant waterfalls
    - Mid-distance (40-65%): Dark slabs, ENV-09/10, glowing edges, corrupted RW fragments
    - Platform zone (60-82%): Void Black + Cyan circuit traces + Acid Green flora
    - Abyss (80-100%): Below-Void-Black — absolute dark anchor
    - Character zone (foreground, lower-left): Luma silhouette block, Byte

    No dutch angle — level horizon. Stillness is the mood.
    """
    random.seed(202614)  # deterministic — Cycle 14

    img = Image.new("RGB", (W, H), VOID_BLACK)
    draw = ImageDraw.Draw(img)

    # ── ZONE 1: VOID SKY (upper 28%) ────────────────────────────────────────
    sky_bottom = int(H * 0.28)
    draw.rectangle([0, 0, W, sky_bottom], fill=VOID_BLACK)

    # Mid-void transition band — ENV-12 deep dark purple
    void_trans_y = int(H * 0.18)
    void_trans_h = int(H * 0.10)
    for row in range(void_trans_h):
        t = row / void_trans_h
        # blend from VOID_BLACK to ENV_12_VOID_TRAN
        r = int(VOID_BLACK[0] + t * (ENV_12_VOID_TRAN[0] - VOID_BLACK[0]))
        g = int(VOID_BLACK[1] + t * (ENV_12_VOID_TRAN[1] - VOID_BLACK[1]))
        b = int(VOID_BLACK[2] + t * (ENV_12_VOID_TRAN[2] - VOID_BLACK[2]))
        draw.line([(0, void_trans_y + row), (W, void_trans_y + row)], fill=(r, g, b))

    # Ring megastructure — enormous circular arc in far void (barely visible)
    # Center: upper-right area, mostly off-frame — only an arc segment is visible
    ring_cx = int(W * 0.78)
    ring_cy = int(H * -0.40)  # center is above the frame
    ring_r  = int(H * 1.10)
    # Draw arc as line segments (PIL polygon approximation)
    ring_pts = []
    for angle_deg in range(-25, 35):
        a = math.radians(angle_deg)
        px = int(ring_cx + ring_r * math.cos(a))
        py = int(ring_cy + ring_r * math.sin(a))
        if 0 <= px < W and 0 <= py < H:
            ring_pts.append((px, py))
    if len(ring_pts) > 1:
        for i in range(len(ring_pts) - 1):
            draw.line([ring_pts[i], ring_pts[i+1]], fill=UV_PURPLE, width=1)

    # Static void artifacts — 1px "stars" (corrupted pixel noise, not real stars)
    for _ in range(60):
        sx = random.randint(0, W - 1)
        sy = random.randint(0, sky_bottom + int(H * 0.08))
        # Vary luminance slightly: mostly STATIC_WHITE but some dim
        lum_var = random.randint(120, 240)
        draw.point([(sx, sy)], fill=(lum_var, lum_var, lum_var))

    # ── ZONE 2: FAR DISTANCE STRUCTURES (26-52%) ────────────────────────────
    far_top    = int(H * 0.24)
    far_bottom = int(H * 0.52)

    # Base far haze gradient: VOID_BLACK → ENV_11_FAR_HAZE
    for row in range(far_bottom - far_top):
        t = row / (far_bottom - far_top)
        r = int(VOID_BLACK[0] + t * (ENV_11_FAR_HAZE[0] - VOID_BLACK[0]))
        g = int(VOID_BLACK[1] + t * (ENV_11_FAR_HAZE[1] - VOID_BLACK[1]))
        b = int(VOID_BLACK[2] + t * (ENV_11_FAR_HAZE[2] - VOID_BLACK[2]))
        draw.line([(0, far_top + row), (W, far_top + row)], fill=(r, g, b))

    # Far structure blocks — barely visible, ENV_FAR_EDGE outlines only
    far_structs = [
        (int(W * 0.10), int(H * 0.30), int(W * 0.22), int(H * 0.44)),
        (int(W * 0.30), int(H * 0.26), int(W * 0.48), int(H * 0.40)),
        (int(W * 0.55), int(H * 0.28), int(W * 0.70), int(H * 0.46)),
        (int(W * 0.75), int(H * 0.30), int(W * 0.90), int(H * 0.50)),
    ]
    for x0, y0, x1, y1 in far_structs:
        draw.rectangle([x0, y0, x1, y1], fill=ENV_11_FAR_HAZE, outline=ENV_FAR_EDGE, width=1)

    # Distant data waterfalls — thin DATA_BLUE vertical lines, no detail
    distant_wf_xs = [int(W * 0.15), int(W * 0.42), int(W * 0.62), int(W * 0.85)]
    for wx in distant_wf_xs:
        wf_top = int(H * 0.28)
        wf_bot = int(H * 0.50)
        draw.line([(wx, wf_top), (wx, wf_bot)], fill=DATA_BLUE, width=1)

    # Distant Glitchkin — tiny ACID_GREEN and ELEC_CYAN dots
    for _ in range(12):
        gx = random.randint(int(W * 0.08), int(W * 0.95))
        gy = random.randint(int(H * 0.30), int(H * 0.48))
        col = ACID_GREEN if random.random() < 0.6 else ELEC_CYAN
        draw.point([(gx, gy)], fill=col)

    # ── ZONE 3: MID-DISTANCE STRUCTURES (45-68%) ────────────────────────────
    mid_top    = int(H * 0.42)
    mid_bottom = int(H * 0.68)

    # Base: blend ENV_11 → ENV_09 range (still cool but slightly more detail-visible)
    for row in range(mid_bottom - mid_top):
        t = row / (mid_bottom - mid_top)
        r = int(ENV_11_FAR_HAZE[0] + t * (ENV_09_SLAB_TOP[0] - ENV_11_FAR_HAZE[0]))
        g = int(ENV_11_FAR_HAZE[1] + t * (ENV_09_SLAB_TOP[1] - ENV_11_FAR_HAZE[1]))
        b = int(ENV_11_FAR_HAZE[2] + t * (ENV_09_SLAB_TOP[2] - ENV_11_FAR_HAZE[2]))
        draw.line([(0, mid_top + row), (W, mid_top + row)], fill=(r, g, b))

    # Mid-distance slab cluster — horizontal platforms at varied heights
    mid_slabs = [
        (int(W * 0.50), int(H * 0.46), int(W * 0.72), int(H * 0.54)),  # right upper
        (int(W * 0.60), int(H * 0.56), int(W * 0.88), int(H * 0.64)),  # right lower
        (int(W * 0.08), int(H * 0.50), int(W * 0.28), int(H * 0.60)),  # left
        (int(W * 0.30), int(H * 0.54), int(W * 0.50), int(H * 0.62)),  # center
    ]
    for x0, y0, x1, y1 in mid_slabs:
        # Top face: ENV_09; vertical faces: ENV_10
        draw.rectangle([x0, y0, x1, y1], fill=ENV_10_SLAB_VERT)
        # Top face (thin top strip)
        draw.rectangle([x0, y0, x1, y0 + 6], fill=ENV_09_SLAB_TOP)
        # Navigation edge glow: ELEC_CYAN
        draw.line([(x0, y0), (x1, y0)], fill=ELEC_CYAN, width=1)

    # Corrupted RW fragment — terracotta wall piece (mid-center, narrative element)
    rw_x0 = int(W * 0.33)
    rw_x1 = int(W * 0.46)
    rw_y0 = int(H * 0.50)
    rw_y1 = int(H * 0.63)
    draw.rectangle([rw_x0, rw_y0, rw_x1, rw_y1], fill=RW_TERRACOTTA)
    # Corrupted Amber at crack edges — top and right edges consuming it
    draw.line([(rw_x0, rw_y0), (rw_x1, rw_y0)], fill=CORRUPTED_AMBER, width=2)
    draw.line([(rw_x1, rw_y0), (rw_x1, rw_y1)], fill=CORRUPTED_AMBER, width=2)
    # Crack lines through the fragment
    draw.line([(rw_x0 + 6, rw_y0), (rw_x0 + 6, rw_y1)], fill=CORRUPTED_AMBER, width=1)
    draw.line([(rw_x0, rw_y0 + 7), (rw_x1, rw_y0 + 7)], fill=CORRUPTED_AMBER, width=1)

    # Corrupted lamppost fragment (right-mid area)
    lp_x = int(W * 0.78)
    lp_y0 = int(H * 0.48)
    lp_y1 = int(H * 0.66)
    draw.rectangle([lp_x - 3, lp_y0, lp_x + 3, lp_y1], fill=MUTED_TEAL_LAMP)
    # Amber corruption spreading from base
    draw.rectangle([lp_x - 3, lp_y1 - 12, lp_x + 3, lp_y1], fill=CORRUPTED_AMBER)

    # ── ZONE 4: PLATFORM (62-82%) ─────────────────────────────────────────────
    plat_top    = int(H * 0.62)
    plat_bottom = int(H * 0.82)

    draw.rectangle([0, plat_top, W, plat_bottom], fill=VOID_BLACK)

    # Platform front-edge depth (slightly lighter than absolute void)
    draw.rectangle([0, plat_top, W, plat_top + 4], fill=ENV_09_SLAB_TOP)

    # Circuit traces — primary (ELEC_CYAN at 80% luminance approx: use slightly dimmer)
    CIRCUIT_CYAN_DIM = (0, 192, 204)  # 80% of ELEC_CYAN luminance (construction value — circuit structural, not event)
    circuit_h_ys = [
        plat_top + 10,
        plat_top + 24,
        plat_top + 40,
        plat_top + 56,
    ]
    for cy_line in circuit_h_ys:
        if cy_line < plat_bottom:
            draw.line([(30, cy_line), (W - 30, cy_line)], fill=CIRCUIT_CYAN_DIM, width=1)

    # Circuit traces — secondary DATA_BLUE vertical lines
    circuit_v_xs = [80, 180, 280, 380, 480, 560]
    for cv_x in circuit_v_xs:
        draw.line([(cv_x, plat_top), (cv_x, plat_bottom - 2)], fill=DATA_BLUE, width=1)

    # Node intersections — bright ELEC_CYAN dots where circuits cross
    for cv_x in circuit_v_xs:
        for cy_line in circuit_h_ys:
            if cy_line < plat_bottom:
                draw.ellipse([cv_x - 2, cy_line - 2, cv_x + 2, cy_line + 2], fill=ELEC_CYAN)

    # Acid Green pixel flora in platform cracks
    flora_positions = [
        (int(W * 0.42), plat_top + 14, 8, 12),
        (int(W * 0.56), plat_top + 22, 6, 10),
        (int(W * 0.65), plat_top + 8,  5, 9),
        (int(W * 0.72), plat_top + 28, 7, 11),
    ]
    for fx, fy, fw, fh in flora_positions:
        # Simple geometric succulent: square base + top highlight
        draw.rectangle([fx, fy, fx + fw, fy + fh], fill=ACID_GREEN)
        draw.rectangle([fx, fy, fx + fw, fy + 3], fill=ELEC_CYAN)   # cyan bounce on top
        draw.rectangle([fx, fy + fh - 3, fx + fw, fy + fh], fill=DARK_ACID_GREEN)  # shadow

    # Settled pixel confetti on platform — sparse, static
    confetti_cols = [ELEC_CYAN, STATIC_WHITE, ACID_GREEN, DATA_BLUE]
    for _ in range(30):
        cx_pos = random.randint(int(W * 0.35), W - 20)
        cy_pos = random.randint(plat_top, plat_bottom - 4)
        col = random.choice(confetti_cols)
        size = random.randint(1, 2)
        draw.rectangle([cx_pos, cy_pos, cx_pos + size, cy_pos + size], fill=col)

    # ── DATA WATERFALL (right side, near, Zone 4) ─────────────────────────────
    wf_x_center = int(W * 0.87)
    wf_top_y    = int(H * 0.38)
    wf_bot_y    = plat_top
    # Waterfall body: DATA_BLUE columns
    for col_x in range(wf_x_center - 6, wf_x_center + 8, 3):
        if 0 <= col_x < W:
            draw.line([(col_x, wf_top_y), (col_x, wf_bot_y)], fill=DATA_BLUE, width=2)
    # Brightest code characters (scattered LIGHT_DATA_BLUE pixels in the stream)
    for _ in range(18):
        lx = wf_x_center + random.randint(-5, 6)
        ly = random.randint(wf_top_y, wf_bot_y - 4)
        draw.rectangle([lx, ly, lx + 2, ly + 3], fill=LIGHT_DATA_BLUE)
    # UV Purple spray at base where waterfall impacts platform
    wf_spray_y = plat_top - 2
    draw.rectangle([wf_x_center - 10, wf_spray_y, wf_x_center + 14, wf_spray_y + 6],
                   fill=UV_PURPLE)
    # Soft DATA_BLUE light pool on platform to the left of waterfall base
    for px_offset in range(20):
        alpha_val = max(0, DATA_BLUE[2] - px_offset * 4)
        lpool_col = (DATA_BLUE[0], DATA_BLUE[1], alpha_val)
        draw.line([(wf_x_center - 12 - px_offset, plat_top + 2),
                   (wf_x_center - 12 - px_offset, plat_top + 8)],
                  fill=lpool_col)

    # ── ZONE 5: ABYSS (80-100%) ──────────────────────────────────────────────
    abyss_top = int(H * 0.80)
    draw.rectangle([0, abyss_top, W, H], fill=BELOW_VOID_BLACK)
    # Platform base-edge — thin ENV_09 line separating platform from abyss
    draw.line([(0, abyss_top), (W, abyss_top)], fill=ENV_09_SLAB_TOP, width=1)

    # ── CHARACTER ZONE — Luma (foreground, lower-left) ───────────────────────
    # Luma simplified silhouette: body block + head + pixel-pattern indicator
    char_base_y = plat_top - 2
    char_top_y  = int(H * 0.36)
    char_x_ctr  = int(W * 0.15)
    char_w      = 28
    char_h      = char_base_y - char_top_y

    # Full body block — hoodie (DRW-14)
    draw.rectangle([char_x_ctr - char_w // 2, char_top_y + char_h // 3,
                    char_x_ctr + char_w // 2, char_base_y],
                   fill=LUMA_HOODIE_GL)
    # Hoodie lower hem — DRW-15 (cyan bounce, teal)
    draw.rectangle([char_x_ctr - char_w // 2, char_base_y - 8,
                    char_x_ctr + char_w // 2, char_base_y],
                   fill=LUMA_HOODIE_CYAN)
    # Jeans block (lower third of body)
    draw.rectangle([char_x_ctr - char_w // 2 + 2, char_base_y - 16,
                    char_x_ctr + char_w // 2 - 2, char_base_y],
                   fill=LUMA_JEANS)
    # Head block — skin (DRW-11)
    head_y = char_top_y + char_h // 3 - 14
    head_r = 10
    draw.ellipse([char_x_ctr - head_r, head_y,
                  char_x_ctr + head_r, head_y + head_r * 2],
                 fill=LUMA_SKIN_GL)
    # Hair (top of head)
    draw.ellipse([char_x_ctr - head_r, head_y,
                  char_x_ctr + head_r, head_y + head_r],
                 fill=LUMA_HAIR)
    # UV Purple rim on crown (ambient rim)
    draw.arc([char_x_ctr - head_r - 1, head_y - 1,
              char_x_ctr + head_r + 1, head_y + head_r * 2 + 1],
             start=200, end=340, fill=UV_PURPLE, width=1)
    # Skin shadow side
    draw.rectangle([char_x_ctr + 2, head_y + 4,
                    char_x_ctr + head_r, head_y + head_r * 2],
                   fill=LUMA_SKIN_SHD)
    # Skin highlight (platform bounce on forehead)
    draw.ellipse([char_x_ctr - 5, head_y + 1,
                  char_x_ctr + 2, head_y + 6],
                 fill=LUMA_SKIN_HLT)
    # Hoodie pixel grid indicator — ELEC_CYAN dots on chest
    px_grid_y = char_top_y + char_h // 3 + 4
    for px_row in range(2):
        for px_col in range(3):
            gx = char_x_ctr - 6 + px_col * 5
            gy = px_grid_y + px_row * 5
            draw.rectangle([gx, gy, gx + 2, gy + 2], fill=ELEC_CYAN)

    # Byte (on Luma's right shoulder — small, precise)
    byte_x = char_x_ctr + char_w // 2 + 2
    byte_y = char_top_y + char_h // 3 + 2
    byte_w = 10
    byte_h = 9
    draw.rectangle([byte_x, byte_y, byte_x + byte_w, byte_y + byte_h], fill=BYTE_TEAL)
    # Byte inner glow (slightly lighter top area)
    draw.rectangle([byte_x + 1, byte_y + 1, byte_x + byte_w - 1, byte_y + 4],
                   fill=DEEP_CYAN)
    # Byte eyes — two different colors (the key character detail at this scale)
    # Cyan eye (left, facing Luma)
    draw.point([(byte_x + 2, byte_y + 3)], fill=ELEC_CYAN)
    draw.point([(byte_x + 3, byte_y + 3)], fill=ELEC_CYAN)
    # Magenta eye (right, facing void)
    draw.point([(byte_x + 7, byte_y + 3)], fill=HOT_MAGENTA)
    draw.point([(byte_x + 8, byte_y + 3)], fill=HOT_MAGENTA)

    # ── PALETTE STRIP (bottom strip, below main composition) ─────────────────
    strip_y = H - 34
    draw.rectangle([0, strip_y - 2, W, H], fill=VOID_BLACK)

    title_font = load_font(11, bold=True)
    lbl(draw, 4, strip_y - 16, "SF03 Other Side — Color Key v001", title_font,
        fg=ELEC_CYAN, bg=None)

    # Primary zone swatches
    primary_swatches = [
        (VOID_BLACK,    "Void*"),
        (ELEC_CYAN,     "Cy*"),
        (UV_PURPLE,     "UV*"),
        (DATA_BLUE,     "Blue"),
        (ACID_GREEN,    "AG"),
        (HOT_MAGENTA,   "Mag*"),
        (CORRUPTED_AMBER, "Amb"),
        (BELOW_VOID_BLACK, "Abys"),
    ]
    palette_strip(draw, primary_swatches, x=4, y=strip_y, sw=34, sh=24, gap=3)

    # Character swatches (right side)
    char_swatches = [
        (LUMA_HOODIE_GL,   "Hdie"),
        (LUMA_SKIN_GL,     "Skin"),
        (LUMA_HOODIE_CYAN, "Hem"),
        (LUMA_JEANS,       "Jean"),
        (BYTE_TEAL,        "Byte"),
        (RW_TERRACOTTA,    "RW!"),
    ]
    palette_strip(draw, char_swatches, x=int(W * 0.58), y=strip_y, sw=34, sh=24, gap=3)

    # ── Zone labels ──────────────────────────────────────────────────────────
    zone_font = load_font(9)
    zone_labels = [
        (int(W * 0.02), int(H * 0.04), "VOID SKY"),
        (int(W * 0.02), int(H * 0.30), "FAR DIST"),
        (int(W * 0.02), int(H * 0.46), "MID DIST"),
        (int(W * 0.02), int(H * 0.65), "PLATFORM"),
        (int(W * 0.02), int(H * 0.83), "ABYSS"),
    ]
    for lx, ly, lt in zone_labels:
        lbl(draw, lx, ly, lt, zone_font, fg=STATIC_WHITE)

    # ── "NO WARM LIGHT" warning marker (compositional annotation) ────────────
    warn_font = load_font(9)
    lbl(draw, int(W * 0.48), int(H * 0.03),
        "ZERO WARM LIGHT — pigment only", warn_font, fg=HOT_MAGENTA)

    return img


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    img = generate_otherside_colorkey()
    out_path = os.path.join(OUTPUT_DIR, "LTG_COLOR_colorkey_otherside.png")
    img.save(out_path)
    print(f"Saved: {out_path}")
    print(f"Size: {img.size[0]}x{img.size[1]}")
    print("Color key: SF03 Other Side — Void Black base, Electric Cyan key, UV Purple ambient")
    print("Zero warm light sources. Warmth as carried pigment only.")


if __name__ == "__main__":
    main()
