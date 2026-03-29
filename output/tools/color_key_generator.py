#!/usr/bin/env python3
"""
Color Key Thumbnail Generator — Luma & the Glitchkin
Generates color-blocked thumbnails for all four scene color keys.

Cycle 5 fixes implemented:
- Key 01: Deep Shadow (#2A1A10) added as dark anchor zone (missing in prev. version)
- Key 02: Hot Magenta reduced from zone color to accent only; Cyan crack is dominant
- Key 03: UV Purple and Data Blue aurora bands separated by ≥2 value steps

Usage: python3 color_key_generator.py
Outputs to: /home/wipkat/team/output/color/color_keys/thumbnails/
"""

import os
import sys
import random  # Cycle 6: moved from inline function-level imports; seed is set per-function for deterministic per-frame output
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = "/home/wipkat/team/output/color/color_keys/thumbnails"
W, H = 640, 360  # 16:9 thumbnail

# Palette hex → RGB
def hx(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

P = {
    "warm_cream":      hx("FAF0DC"),
    "soft_gold":       hx("E8C95A"),
    "sunlit_amber":    hx("D4923A"),
    "terracotta":      hx("C75B39"),
    "sage_green":      hx("7A9E7E"),
    "dusty_lavender":  hx("A89BBF"),
    "shadow_plum":     hx("5C4A72"),
    "shadow_plum_dp":  hx("3D2F4F"),
    "warm_tan":        hx("C4A882"),
    "skin_shadow":     hx("8C5A38"),
    "deep_cocoa":      hx("3B2820"),
    "deep_shadow":     hx("2A1A10"),   # dark anchor — KEY FIX for Key 01
    "night_sky":       hx("1A1428"),
    "elec_cyan":       hx("00F0FF"),
    "byte_teal":       hx("00D4E8"),
    "hot_magenta":     hx("FF2D6B"),
    "acid_green":      hx("39FF14"),
    "uv_purple":       hx("7B2FBE"),
    "static_white":    hx("F0F0F0"),
    "void_black":      hx("0A0A14"),
    "data_blue":       hx("2B7FFF"),
    "data_blue_deep":  hx("1040A0"),   # darker data blue for value separation
    "corrupted_amber": hx("FF8C00"),
    "ochre_brick":     hx("B8944A"),
    "muted_teal":      hx("5B8C8A"),
    "moon_ambient":    hx("C8BFD8"),
    "deep_uv_sep":     hx("4A1880"),   # deeper UV for band separation (Key 03 fix)
}

def load_font(size=13, bold=False):
    paths = [
        ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold
         else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()

def lbl(draw, x, y, text, font, fg=(255, 255, 255), bg=None):
    if bg:
        bb = draw.textbbox((x, y), text, font=font)
        draw.rectangle([bb[0]-2, bb[1]-1, bb[2]+2, bb[3]+1], fill=bg)
    draw.text((x, y), text, fill=fg, font=font)

def palette_strip(draw, swatches, x, y, sw=36, sh=26, gap=4):
    """Draw a row of labeled color swatches."""
    font = load_font(9)
    for i, (col, name) in enumerate(swatches):
        sx = x + i * (sw + gap)
        draw.rectangle([sx, y, sx + sw, y + sh], fill=col)
        draw.rectangle([sx, y, sx + sw, y + sh], outline=(80, 70, 60), width=1)
        # Determine text color based on luminance
        r, g, b = col
        lum = 0.299 * r / 255 + 0.587 * g / 255 + 0.114 * b / 255
        tc = (10, 10, 10) if lum > 0.45 else (240, 235, 220)
        draw.text((sx + 2, y + 14), name[:5], fill=tc, font=font)


# ─────────────────────────────────────────────
# KEY 01 — SUNNY AFTERNOON
# FIX: Add Deep Shadow (#2A1A10) as dark anchor
# ─────────────────────────────────────────────
def generate_key01():
    img = Image.new("RGB", (W, H), P["warm_cream"])
    draw = ImageDraw.Draw(img)

    # Sky — warm cream
    draw.rectangle([0, 0, W, H // 3], fill=P["warm_cream"])
    # Soft Gold at horizon
    draw.rectangle([0, H // 4, W, H // 3 + 10], fill=P["soft_gold"])

    # Background — sage green foliage
    draw.rectangle([0, H // 3, W, H // 2], fill=P["sage_green"])

    # Architecture — terracotta buildings
    draw.rectangle([0, H // 4, W // 3, H * 3 // 4], fill=P["terracotta"])
    draw.rectangle([W // 2, H // 5, W, H * 3 // 4], fill=P["terracotta"])

    # Sunlit floor / ground
    draw.rectangle([0, H * 3 // 4, W, H], fill=P["soft_gold"])

    # Shadow areas — dusty lavender (fill light / cool shadows)
    draw.rectangle([0, H // 2, W // 4, H * 3 // 4], fill=P["dusty_lavender"])
    draw.rectangle([W * 3 // 4, H // 2, W, H * 3 // 4],
                   fill=P["dusty_lavender"])

    # Shadow cast on floor — shadow plum deep
    draw.ellipse([W * 3 // 8, H * 3 // 4 + 5, W * 5 // 8, H * 3 // 4 + 30],
                 fill=P["shadow_plum_dp"])

    # Warm tan for skin / wooden details
    draw.rectangle([W * 2 // 5, H * 3 // 8, W * 3 // 5, H * 3 // 4],
                   fill=P["warm_tan"])

    # Deep cocoa — line/furniture
    draw.rectangle([W * 2 // 5 - 2, H * 3 // 8,
                    W * 2 // 5 + 4, H * 3 // 4],
                   fill=P["deep_cocoa"])

    # Trace cyan (CRT hint)
    draw.rectangle([W * 7 // 8, H // 3, W * 15 // 16, H // 2],
                   fill=P["elec_cyan"])

    # FIX: Deep Shadow (#2A1A10) as dark anchor
    # Previously missing — tonal range was too compressed / no near-black zone.
    # Added as under-furniture / deep corner shadow zones.
    # Under the furniture (character area) base:
    draw.rectangle([W * 2 // 5, H * 7 // 10, W * 3 // 5, H * 3 // 4 + 5],
                   fill=P["deep_shadow"])
    # Corner deep shadows (bottom corners)
    draw.rectangle([0, H * 7 // 8, W // 6, H], fill=P["deep_shadow"])
    draw.rectangle([W * 5 // 6, H * 7 // 8, W, H], fill=P["deep_shadow"])
    # Under the terracotta architecture — crevice shadows
    draw.rectangle([W // 3, H * 5 // 8, W // 2, H * 3 // 4],
                   fill=P["deep_shadow"])

    # Palette strip
    swatches = [
        (P["warm_cream"],     "Cream"),
        (P["soft_gold"],      "Gold"),
        (P["terracotta"],     "Terra"),
        (P["sage_green"],     "Sage"),
        (P["dusty_lavender"], "Lavdr"),
        (P["deep_cocoa"],     "Cocoa"),
        (P["warm_tan"],       "Skin"),
        (P["elec_cyan"],      "Cyan"),
        (P["deep_shadow"],    "DkAnch"),  # FIXED — new dark anchor
    ]
    palette_strip(draw, swatches, 8, H - 38)

    lbl(draw, 8, 8,
        "Key 01 — Sunny Afternoon  [Cycle 5]",
        load_font(14, bold=True), fg=P["deep_cocoa"], bg=P["warm_cream"])
    lbl(draw, 8, 28,
        "FIX: Deep Shadow #2A1A10 added as dark anchor (bottom corners, under furniture)",
        load_font(10), fg=P["deep_cocoa"], bg=P["warm_cream"])

    out = os.path.join(OUTPUT_DIR, "key01_sunny_afternoon.png")
    img.save(out)
    print(f"Saved: {out}")
    return out


# ─────────────────────────────────────────────
# KEY 02 — NIGHTTIME GLITCH ATTACK
# FIX: Hot Magenta reduced from zone to accent only
#      Cyan crack is the dominant energy — Magenta accents only
# ─────────────────────────────────────────────
def generate_key02():
    img = Image.new("RGB", (W, H), P["night_sky"])
    draw = ImageDraw.Draw(img)

    # Sky — deep night
    draw.rectangle([0, 0, W, H * 3 // 5], fill=P["night_sky"])

    # UV purple glitch masses in sky
    draw.rectangle([W // 4, 0, W * 3 // 4, H // 4], fill=P["uv_purple"])
    draw.rectangle([W // 2, 0, W, H // 3], fill=P["uv_purple"])

    # Void black core
    draw.rectangle([W * 3 // 8, H // 8, W * 5 // 8, H // 4],
                   fill=P["void_black"])

    # Buildings — deep cocoa with terracotta walls (residual warmth)
    bldgs = [(0, H // 3), (W // 5, H // 4), (W * 2 // 5, H * 2 // 5),
             (W * 3 // 5, H // 3), (W * 4 // 5, H // 4)]
    for bx, by in bldgs:
        bw = W // 5 - 10
        draw.rectangle([bx, by, bx + bw, H * 3 // 5], fill=P["deep_cocoa"])
        draw.rectangle([bx + 4, by + 15, bx + bw - 4, H * 3 // 5],
                       fill=P["terracotta"])
        # Warm cream windows (last vestige of safety)
        draw.rectangle([bx + 10, by + 20, bx + 28, by + 38],
                       fill=P["warm_cream"])

    # Ground — dark asphalt with cyan cast
    draw.rectangle([0, H * 3 // 5, W, H], fill=(42, 42, 56))

    # ── MAIN CRACK — Electric Cyan dominant ──
    # The crack is the compositional center and the dominant glitch color.
    # (FIX: Hot Magenta is no longer a zone color here)
    crack_pts = [(W * 9 // 10, 0), (W * 8 // 10, H // 5),
                 (W * 7 // 10, H // 3), (W * 6 // 10, H // 2)]
    # Outer glow — cyan (NOT magenta zone)
    draw.line(crack_pts, fill=P["elec_cyan"], width=18)
    draw.line(crack_pts, fill=P["static_white"], width=6)
    # Cyan flood on crack area
    draw.rectangle([W * 5 // 8, 0, W, H * 2 // 3], fill=(0, 80, 100))  # cyan wash
    # Redraw crack on top
    draw.line(crack_pts, fill=P["elec_cyan"], width=14)
    draw.line(crack_pts, fill=P["static_white"], width=5)

    # FIX: Hot Magenta only as ACCENT — narrow edge burns on crack perimeter
    # Previously it was a large zone color; now it's just thin accent strokes.
    draw.line(crack_pts, fill=P["hot_magenta"], width=2)  # thin accent only
    # Small magenta accent sparks (not zone coverage)
    # random is imported at module top; seed is intentional for deterministic output
    random.seed(20)
    for _ in range(12):
        ax = random.randint(W // 2, W)
        ay = random.randint(0, H // 2)
        draw.rectangle([ax, ay, ax + 4, ay + 4], fill=P["hot_magenta"])

    # Sub-cracks (data blue at tips)
    draw.line([(W * 7 // 10, H // 3), (W * 8 // 10, H * 3 // 8)],
              fill=P["data_blue"], width=3)

    # Static white confetti / sparks
    for _ in range(50):
        px = random.randint(W // 3, W)
        py = random.randint(0, H * 2 // 3)
        ps = random.choice([2, 3])
        pc = random.choice([P["static_white"], P["elec_cyan"], P["uv_purple"]])
        draw.rectangle([px, py, px + ps, py + ps], fill=pc)

    # Palette strip
    swatches = [
        (P["night_sky"],    "Night"),
        (P["deep_cocoa"],   "Bldg"),
        (P["elec_cyan"],    "Cyan"),
        (P["hot_magenta"],  "Mag*"),    # * = accent only (FIX)
        (P["uv_purple"],    "UVPur"),
        (P["terracotta"],   "Terra"),
        (P["static_white"], "White"),
        (P["warm_cream"],   "Cream"),
    ]
    palette_strip(draw, swatches, 8, H - 38)

    lbl(draw, 8, 8,
        "Key 02 — Nighttime Glitch  [Cycle 5]",
        load_font(14, bold=True), fg=P["static_white"], bg=P["night_sky"])
    lbl(draw, 8, 28,
        "FIX: Hot Magenta = accent only (thin edge, not zone). Cyan crack is dominant.",
        load_font(10), fg=P["hot_magenta"], bg=P["night_sky"])

    out = os.path.join(OUTPUT_DIR, "key02_nighttime_glitch.png")
    img.save(out)
    print(f"Saved: {out}")
    return out


# ─────────────────────────────────────────────
# KEY 03 — GLITCH LAYER ENTRY
# FIX: Increase value separation between UV Purple and Data Blue aurora bands
#      Previous version had them at similar values — they merged at thumbnail
# ─────────────────────────────────────────────
def generate_key03():
    img = Image.new("RGB", (W, H), P["void_black"])
    draw = ImageDraw.Draw(img)

    # Void sky base
    draw.rectangle([0, 0, W, H], fill=P["void_black"])

    # ── Aurora / atmospheric bands — FIX: value separation ──
    # Previous bands: UV Purple (7B2FBE, value ~0.20) and Data Blue (2B7FFF, value ~0.35)
    # These are close enough in value to merge at thumbnail scale.
    # Fix: Separate the bands clearly using a deeper UV variant and standard data blue.
    #
    # Band 1 (top) — Deep UV Purple: #4A1880 (much darker than standard UV)
    # Band 2 (mid) — Standard UV Purple: #7B2FBE  (mid value)
    # Band 3 (lower mid) — Data Blue: #2B7FFF (clearly brighter/lighter value)
    # Band 4 (near void) — Deep Data Blue: #1040A0 (step down for depth)
    #
    # This creates a clear value ladder: deep purple → mid purple → bright blue → deep blue
    # Adjacent bands are always ≥2 value steps apart.

    band_h = H // 5

    # Band 1 — top: near void (very dark)
    draw.rectangle([0, 0, W, band_h], fill=P["void_black"])

    # Band 2 — Deep UV Purple (#4A1880 — much darker than standard)
    draw.rectangle([0, band_h, W, band_h * 2], fill=P["deep_uv_sep"])

    # Band 3 — Standard UV Purple (#7B2FBE — clearly brighter than band 2)
    draw.rectangle([0, band_h * 2, W, band_h * 3], fill=P["uv_purple"])

    # Band 4 — Data Blue (#2B7FFF — clearly lighter/more saturated than UV Purple)
    draw.rectangle([0, band_h * 3, W, band_h * 4], fill=P["data_blue"])

    # Band 5 — bottom: foreground void (darkens again at platform level)
    draw.rectangle([0, band_h * 4, W, H], fill=P["void_black"])

    # Blend band edges (simulate soft transition)
    for band_edge in [band_h, band_h * 2, band_h * 3, band_h * 4]:
        for dy in range(-4, 5):
            alpha = abs(dy) / 4
            # Draw slightly blended line at each band edge
            draw.line([(0, band_edge + dy), (W, band_edge + dy)],
                      fill=(20, 10, 32), width=1)

    # Redraw bands clean (edges were just softened slightly)
    draw.rectangle([0, band_h, W, band_h * 2], fill=P["deep_uv_sep"])
    draw.rectangle([0, band_h * 2, W, band_h * 3], fill=P["uv_purple"])
    draw.rectangle([0, band_h * 3, W, band_h * 4], fill=P["data_blue"])

    # Far distance structures
    # random is imported at module top; seed is intentional for deterministic output
    random.seed(55)
    for i in range(5):
        fx = random.randint(W // 8, W * 7 // 8)
        fy = random.randint(band_h, band_h * 2 + 20)
        fw = random.randint(30, 80)
        fh = random.randint(H // 5, H // 3)
        draw.rectangle([fx, fy, fx + fw, fy + fh], fill=(42, 16, 64))

    # Data stream waterfalls (visible across multiple bands)
    for wx in [W // 5, W * 2 // 5, W * 3 // 5, W * 4 // 5]:
        draw.line([(wx, 0), (wx, H * 4 // 5)], fill=P["data_blue"], width=2)
        for wy in range(0, H * 4 // 5, 12):
            if random.random() > 0.6:
                draw.rectangle([wx - 2, wy, wx + 2, wy + 8],
                               fill=(106, 186, 255))

    # Foreground platform
    plat_y = H * 4 // 5
    draw.rectangle([0, plat_y, W // 2, H], fill=P["void_black"])
    for tx in range(10, W // 2, 30):
        draw.line([(tx, plat_y), (tx, H)], fill=P["elec_cyan"], width=1)
    for ty in range(plat_y + 5, H, 18):
        draw.line([(0, ty), (W // 2, ty)], fill=P["elec_cyan"], width=1)

    # Pixel-art plants
    for px in [60, 120, 200]:
        draw.rectangle([px, plat_y - 20, px + 12, plat_y],
                       fill=P["acid_green"])
        draw.rectangle([px + 2, plat_y - 30, px + 10, plat_y - 20],
                       fill=P["acid_green"])

    # Character silhouette (Luma)
    luma_x3 = W // 6
    luma_y3 = plat_y
    draw.rectangle([luma_x3 - 12, luma_y3 - 60, luma_x3 + 12, luma_y3],
                   fill=(58, 80, 120))
    draw.rectangle([luma_x3 - 18, luma_y3 - 120, luma_x3 + 18, luma_y3 - 60],
                   fill=(192, 112, 56))
    draw.ellipse([luma_x3 - 16, luma_y3 - 158,
                  luma_x3 + 16, luma_y3 - 122], fill=(168, 120, 144))

    # Warm skin anchor against void — confirms Real World trace
    lbl(draw, luma_x3 - 16, luma_y3 - 168,
        "Luma", load_font(9), fg=P["warm_cream"])

    # Accents: Corrupted Amber on Real World object fragments
    draw.rectangle([W * 3 // 5, H * 2 // 5, W * 2 // 3, H // 2],
                   fill=(58, 40, 20))
    draw.rectangle([W * 3 // 5, H * 2 // 5, W * 2 // 3, H // 2],
                   outline=P["corrupted_amber"], width=2)

    # Confetti
    for _ in range(40):
        px = random.randint(0, W)
        py = random.randint(0, H)
        ps = random.choice([1, 2])
        pc = random.choice([P["elec_cyan"], P["static_white"],
                            P["acid_green"], P["data_blue"]])
        draw.rectangle([px, py, px + ps, py + ps], fill=pc)

    # Palette strip with value labels
    swatches = [
        (P["void_black"],   "Void"),
        (P["deep_uv_sep"],  "DpUV"),   # NEW — darker UV band
        (P["uv_purple"],    "UVPur"),
        (P["data_blue"],    "Data"),
        (P["data_blue_deep"],"DDat"),
        (P["elec_cyan"],    "Cyan"),
        (P["acid_green"],   "AcGrn"),
        (P["static_white"], "White"),
    ]
    palette_strip(draw, swatches, 8, H - 38)

    lbl(draw, 8, 8,
        "Key 03 — Glitch Layer Entry  [Cycle 5]",
        load_font(14, bold=True), fg=P["static_white"], bg=P["void_black"])
    lbl(draw, 8, 28,
        "FIX: UV Purple + Data Blue bands value-separated (deep UV #4A1880 added as mid band)",
        load_font(10), fg=P["elec_cyan"], bg=P["void_black"])

    out = os.path.join(OUTPUT_DIR, "key03_glitch_layer_entry.png")
    img.save(out)
    print(f"Saved: {out}")
    return out


# ─────────────────────────────────────────────
# KEY 04 — QUIET EMOTIONAL MOMENT
# No fixes needed; regenerate for consistency
# ─────────────────────────────────────────────
def generate_key04():
    img = Image.new("RGB", (W, H), P["warm_cream"])
    draw = ImageDraw.Draw(img)

    # Warm cream background
    draw.rectangle([0, 0, W, H], fill=P["warm_cream"])

    # Evening sky outside window — dusty lavender
    draw.rectangle([W * 3 // 5, 0, W, H // 2], fill=P["dusty_lavender"])

    # Window frame
    draw.rectangle([W * 2 // 3, H // 8, W * 9 // 10, H * 3 // 8],
                   fill=P["dusty_lavender"], outline=P["deep_cocoa"], width=3)

    # Warm key light source (lamp) — soft gold
    lamp_cx = W * 2 // 5
    lamp_cy = H // 3
    draw.ellipse([lamp_cx - 60, lamp_cy - 60,
                  lamp_cx + 60, lamp_cy + 60], fill=P["soft_gold"])
    draw.ellipse([lamp_cx - 40, lamp_cy - 40,
                  lamp_cx + 40, lamp_cy + 40], fill=(245, 225, 140))
    # Lamp body
    draw.rectangle([lamp_cx - 8, lamp_cy + 15,
                    lamp_cx + 8, lamp_cy + 40],
                   fill=P["warm_tan"], outline=P["deep_cocoa"], width=1)

    # Floor — warm cream / ochre
    draw.rectangle([0, H * 3 // 4, W, H], fill=P["soft_gold"])

    # Shadow plum — shadow fill on shadow side
    draw.rectangle([0, H // 4, W // 5, H * 3 // 4], fill=P["shadow_plum"])

    # Warm tan — character skin
    # Two character silhouettes (Luma left, Cosmo/other right)
    for cx in [W // 3, W // 2]:
        draw.rectangle([cx - 20, H // 3, cx + 20, H * 3 // 4],
                       fill=P["warm_tan"])
        draw.ellipse([cx - 20, H // 4, cx + 20, H // 3 + 10],
                     fill=P["warm_tan"])

    # Skin shadow
    draw.rectangle([W // 3 - 20, H // 3, W // 3, H * 3 // 4],
                   fill=P["skin_shadow"])
    draw.rectangle([W // 2, H // 3, W // 2 + 20, H * 3 // 4],
                   fill=P["skin_shadow"])

    # Deep cocoa line details
    draw.line([(W // 3 - 2, H // 4), (W // 3 - 2, H * 3 // 4)],
              fill=P["deep_cocoa"], width=2)

    # Trace cyan — Byte's barely-visible glow
    draw.ellipse([W // 3 + 22, H * 2 // 5, W // 3 + 36, H * 2 // 5 + 14],
                 fill=P["elec_cyan"])

    # Palette strip
    swatches = [
        (P["warm_cream"],      "Cream"),
        (P["soft_gold"],       "Gold"),
        (P["dusty_lavender"],  "Lavdr"),
        (P["warm_tan"],        "Skin"),
        (P["shadow_plum"],     "Shade"),
        (P["deep_cocoa"],      "Cocoa"),
        (P["elec_cyan"],       "Byte"),
    ]
    palette_strip(draw, swatches, 8, H - 38)

    lbl(draw, 8, 8,
        "Key 04 — Quiet Moment  [Cycle 5]",
        load_font(14, bold=True), fg=P["deep_cocoa"], bg=P["warm_cream"])
    lbl(draw, 8, 28,
        "No new fixes. Ambient = Warm Cream (Sunlit Amber removed in Cycle 2).",
        load_font(10), fg=P["deep_cocoa"], bg=P["warm_cream"])

    out = os.path.join(OUTPUT_DIR, "key04_quiet_moment.png")
    img.save(out)
    print(f"Saved: {out}")
    return out


if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    generate_key01()
    generate_key02()
    generate_key03()
    generate_key04()
    print("All color key thumbnails generated.")
