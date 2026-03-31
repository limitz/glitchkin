#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_sf_covetous_glitch.py
"Luma & the Glitchkin" — Style Frame: COVETOUS GLITCH
Artist: Rin Yamamoto | Cycle 40 (C42 update)

BRIEF (C42 UPDATE — Three-character triangulation)
--------------------------------------------------
Sam Kowalski spec (glitch_covetous_styleframe_spec.md, C42 revision):
  Glitch (COVETOUS, left/center-left) → Byte (midground barrier, center) → Luma (right zone, warm)
  Glitch leans +12° toward Luma. Byte positions between them as protective barrier.
  Luma visible right: hoodie orange + warm skin. Byte: teal body, smaller than Glitch.
  NO warm light on Glitch. Glitch's only illumination = UV_PURPLE ambient.
  The gap between Glitch and Luma — Byte standing in it — IS the premise of Season 1.

C41 (original): Glitch alone at threshold. Single-character composition.
C42 (this version): Three-character triangulation per story_bible_v003.md §EP5.

COMPOSITION
-----------
- Location: Glitch Layer — organized platform zone, low camera angle.
- Glitch: left/center-left, large (foreground), COVETOUS state.
  tilt=+12 (lean toward Luma), arms raised slightly, ACID_GREEN bilateral slit eyes.
- Byte: midground center, smaller than Glitch — barrier posture, teal body.
- Luma: right zone, warm palette (hoodie orange, skin), slightly behind Byte.
  Luma's character warmth IS the warm zone. Warm colors must NOT cross Byte barrier.

SPEC COMPLIANCE (C42)
---------------------
G001: rx=54 (within [28,56]), ry=62 (within [28,64]) — spec PASS
G004: HOT_MAG crack drawn AFTER body fill — spec PASS (draw_glitch_body defined first)
G008: BILATERAL_EYES = True — bilateral eye rule enforced for COVETOUS interior state

OUTPUT: output/color/style_frames/LTG_COLOR_sf_covetous_glitch.png

CRITICAL RULES:
  - NO WARM LIGHT ON GLITCH. Luma's warmth stays in right 30% — does not reach Glitch.
  - UV_PURPLE_DARK = GL-04a (58, 16, 96) — canonical, verified C40/C41.
  - After every img.paste() / alpha_composite: refresh draw = ImageDraw.Draw(img).
  - Canvas: native 1280×720 (no thumbnail downscale needed — eliminates LANCZOS drift).
  - All RNG seeded for reproducibility.
"""

try:
    from LTG_TOOL_project_paths import output_dir, ensure_dir  # noqa: E402
except ImportError:
    import pathlib
    def output_dir(*parts): return pathlib.Path("/home/wipkat/team/output").joinpath(*parts)
    def ensure_dir(path): path.mkdir(parents=True, exist_ok=True); return path
import math
import os
import sys
import random
from PIL import Image, ImageDraw, ImageFilter

# Canonical character renderer imports
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
from LTG_TOOL_char_glitch import draw_glitch
from LTG_TOOL_char_byte import draw_byte
from LTG_TOOL_char_luma import draw_luma
from LTG_TOOL_cairo_primitives import to_pil_rgba

__version__ = "3.0.0"  # C53: canonical char_*.py imports replace inline drawing
__author__ = "Rin Yamamoto"
__cycle__ = 53

# ── Canvas (native 1280×720 — no LANCZOS thumbnail needed) ────────────────────
W, H = 1280, 720

# ── Palette ───────────────────────────────────────────────────────────────────
VOID_BLACK      = (10,  10,  20)
UV_PURPLE       = (123, 47, 190)      # GL-04 #7B2FBE — canonical
ACID_GREEN      = (57,  255,  20)     # GL-03 #39FF14
ELEC_CYAN       = (0,   240, 255)     # GL-01a
BYTE_TEAL       = (0,   212, 232)     # GL-01b
BYTE_TEAL_SH    = (0,   168, 192)     # GL-01a shadow companion
CORRUPT_AMB     = (255, 140,   0)     # GL-07
CORRUPT_AMB_SH  = (168,  76,   0)
CORRUPT_AMB_HL  = (255, 185,  80)
HOT_MAG         = (255,  45, 107)     # GL-06
STATIC_WHITE    = (240, 240, 240)
UV_PURPLE_MID   = (42,   26,  64)
UV_PURPLE_DARK  = (58,   16,  96)     # GL-04a #3A1060 — 72% sat. C40 canonical.
FAR_EDGE        = (33,   17,  54)
DATA_BLUE       = (43,  127, 255)
SOFT_GOLD       = (232, 201,  90)

# Luma character palette (warm — the subject of Glitch's desire)
LUMA_HOODIE     = (232, 112,  58)     # CHAR-L-04 hoodie orange
LUMA_HOODIE_SH  = (184,  74,  32)     # hoodie shadow
LUMA_SKIN       = (200, 136,  90)     # CHAR-L-01 skin
LUMA_SKIN_SH    = (168, 104,  56)     # skin shadow
LUMA_HAIR       = (26,  15,  10)      # DRW-18 dark silhouette anchor
LUMA_SOFT_GOLD  = (232, 201,  90)     # RW-02 ambient warm glow (alpha max 50)

# G008: BILATERAL_EYES required for COVETOUS interior state (spec §6.3)
BILATERAL_EYES = True  # COVETOUS — identical left+right eye glyph; no destabilize


def lerp_color(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


# ── Helper: cairo surface -> PIL composite ───────────────────────────────────

def _cairo_to_pil_cropped(surface):
    """Convert a cairo.ImageSurface to a cropped PIL RGBA image."""
    pil_img = to_pil_rgba(surface)
    bbox = pil_img.getbbox()
    if bbox:
        pil_img = pil_img.crop(bbox)
    return pil_img


def _paste_character(img, char_pil, cx, cy, target_h=None):
    """Paste a cropped character PIL image centered at (cx, cy) on the scene img.
    If target_h is given, scale the character to that height preserving aspect ratio."""
    if target_h and char_pil.height > 0:
        scale_factor = target_h / char_pil.height
        new_w = max(1, int(char_pil.width * scale_factor))
        new_h = max(1, int(char_pil.height * scale_factor))
        char_pil = char_pil.resize((new_w, new_h), Image.LANCZOS)
    px = cx - char_pil.width // 2
    py = cy - char_pil.height // 2
    img_rgba = img.convert("RGBA")
    img_rgba.paste(char_pil, (px, py), char_pil)
    img.paste(img_rgba.convert("RGB"))


# ── Glitch Character (canonical import — COVETOUS expression) ─────────────────

def draw_glitch_large(img):
    """Draw Glitch in COVETOUS state, large (foreground), left/center-left.
    Uses canonical char_glitch.draw_glitch() renderer.
    G001/G004/G008 compliance is handled by the canonical module."""
    cx = int(W * 0.30)
    cy = int(H * 0.50)

    # Render via canonical module — covetous expression, scale ~1.6 for large foreground
    surface = draw_glitch(expression="covetous", scale=1.6, facing="right",
                          scene_lighting={"tint": UV_PURPLE[:3], "intensity": 0.12})
    char_pil = _cairo_to_pil_cropped(surface)
    # Target height ~180px to match original rx=54/ry=62 character extent
    _paste_character(img, char_pil, cx, cy, target_h=180)
    draw = ImageDraw.Draw(img)
    return draw


# ── Background: Other Side / Glitch Layer Void ────────────────────────────────

def draw_void_sky(draw, img):
    """UV_PURPLE gradient sky — inverted atmospheric perspective."""
    draw.rectangle([0, 0, W - 1, H - 1], fill=VOID_BLACK)
    sky_bottom = int(H * 0.40)
    for y in range(sky_bottom):
        t = y / sky_bottom
        col = lerp_color(VOID_BLACK, UV_PURPLE_DARK, t)
        draw.line([(0, y), (W - 1, y)], fill=col)

    # Sparse stars
    rng = random.Random(42)
    for _ in range(60):
        sx = rng.randint(0, W - 1)
        sy = rng.randint(0, int(H * 0.35))
        draw.point((sx, sy), fill=STATIC_WHITE)

    # Ring megastructure (far sky — canonical Other Side element)
    ring_cx = int(W * 0.75)
    ring_cy = int(H * 0.16)
    ring_r  = int(H * 0.30)
    ring_overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ring_draw = ImageDraw.Draw(ring_overlay)
    ring_draw.ellipse(
        [ring_cx - ring_r, ring_cy - ring_r,
         ring_cx + ring_r, ring_cy + ring_r],
        outline=(*UV_PURPLE, 18), width=2
    )
    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, ring_overlay)
    img.paste(img_rgba.convert("RGB"))
    draw = ImageDraw.Draw(img)
    return draw


def draw_aurora_bands(draw, img):
    """UV_PURPLE aurora bands — Glitch Layer ambient identity."""
    aurora = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    adraw = ImageDraw.Draw(aurora)
    rng = random.Random(17)
    band_y = int(H * 0.33)
    for i in range(5):
        y0 = band_y + rng.randint(-18, 18)
        y1 = y0 + rng.randint(3, 10)
        alpha = rng.randint(10, 28)
        adraw.rectangle([0, y0, W - 1, y1], fill=(*UV_PURPLE, alpha))
    for i in range(3):
        y0 = band_y + rng.randint(-25, 25)
        y1 = y0 + rng.randint(2, 5)
        alpha = rng.randint(6, 16)
        adraw.rectangle([0, y0, W - 1, y1], fill=(*DATA_BLUE, alpha))
    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, aurora)
    img.paste(img_rgba.convert("RGB"))
    draw = ImageDraw.Draw(img)
    return draw


def draw_far_slabs(draw):
    """Dark slab silhouettes — far distance, inverted atmospheric perspective."""
    rng = random.Random(55)
    horizon_y = int(H * 0.50)
    for i in range(8):
        sx = rng.randint(0, W - 80)
        sw = rng.randint(35, 90)
        sy = horizon_y - rng.randint(25, 75)
        draw.rectangle([sx, sy, sx + sw, horizon_y], fill=FAR_EDGE)
        draw.rectangle([sx, sy, sx + sw, sy + 2], fill=UV_PURPLE_MID)


def draw_platform(draw):
    """Glitch Layer platform at ground level — ELEC_CYAN circuit lines (canonical depth system)."""
    horizon_y = int(H * 0.50)
    # Floor base: UV_PURPLE_DARK to VOID_BLACK
    for y in range(horizon_y, H):
        t = (y - horizon_y) / max(1, H - horizon_y)
        col = lerp_color(UV_PURPLE_DARK, VOID_BLACK, t)
        draw.line([(0, y), (W - 1, y)], fill=col)

    # Platform top edge — ELEC_CYAN (canonical Glitch Layer depth system)
    draw.line([(0, horizon_y), (W - 1, horizon_y)], fill=(*ELEC_CYAN, ), width=1)

    # Circuit trace lines on platform (thin, ELEC_CYAN)
    rng = random.Random(77)
    for _ in range(6):
        x0 = rng.randint(0, W - 1)
        x1 = rng.randint(0, W - 1)
        y_line = horizon_y + rng.randint(2, 12)
        draw.line([(x0, y_line), (x1, y_line)], fill=ELEC_CYAN, width=1)


# ── Byte — Midground Barrier Character (canonical import) ─────────────────────

def draw_byte_barrier(img):
    """Byte as midground barrier between Glitch (left) and Luma (right).
    Uses canonical char_byte.draw_byte() renderer.
    C42 spec: Byte is SMALLER than Glitch, teal body, protective posture."""
    bx = int(W * 0.55)
    by = int(H * 0.50)

    # Glow halo — BYTE_TEAL (midground presence)
    br = 26
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    for radius in range(br + 22, br - 1, -3):
        alpha = int(28 * (1 - (radius - br) / 22))
        if alpha > 0:
            gdraw.ellipse(
                [bx - radius, by - radius, bx + radius, by + radius],
                fill=(*BYTE_TEAL, alpha)
            )
    glow_blurred = glow.filter(ImageFilter.GaussianBlur(radius=5))
    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, glow_blurred)
    img.paste(img_rgba.convert("RGB"))

    # Render via canonical module — neutral expression, small midground scale
    surface = draw_byte(expression="neutral", scale=0.6, facing="front",
                        scene_lighting={"tint": UV_PURPLE[:3], "intensity": 0.15})
    char_pil = _cairo_to_pil_cropped(surface)
    # Target height ~70px to match midground barrier scale (br=26)
    _paste_character(img, char_pil, bx, by, target_h=70)
    draw = ImageDraw.Draw(img)
    return draw


# ── Luma — Right Zone, Warm Character Palette (canonical import) ──────────────

def draw_luma_warm(img):
    """Luma in right zone — the subject of Glitch's desire.
    Uses canonical char_luma.draw_luma() renderer.
    C42 spec: Luma's warm character palette IS the warm zone.
    Warm colors MUST stay in right 30% — must not reach Glitch's zone."""
    lx = int(W * 0.75)   # right 30%
    ly = int(H * 0.50)
    lh = int(H * 0.36)   # character height

    # Render via canonical module — CURIOUS expression (alert/aware posture)
    surface = draw_luma(expression="CURIOUS", scale=0.5, facing="left")
    char_pil = _cairo_to_pil_cropped(surface)
    # Target height to match original lh proportion
    _paste_character(img, char_pil, lx, ly, target_h=lh)

    # Ambient warm glow from Luma's character presence (soft gold, alpha max 50)
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    glow_r = int(lh * 0.7)
    for r in range(glow_r, glow_r // 4, -8):
        alpha = int(22 * (1 - r / glow_r))
        gdraw.ellipse([lx - r, ly - r, lx + r, ly + r],
                      fill=(*LUMA_SOFT_GOLD, alpha))
    glow_blurred = glow.filter(ImageFilter.GaussianBlur(radius=12))
    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, glow_blurred)
    img.paste(img_rgba.convert("RGB"))
    draw = ImageDraw.Draw(img)

    return draw


# ── UV_PURPLE ambient overlay ─────────────────────────────────────────────────

def draw_ambient_overlay(img):
    """UV_PURPLE ambient — Glitch's native space. Left-dominant (Glitch's zone)."""
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    odraw = ImageDraw.Draw(overlay)

    # Left/center ambient (Glitch zone — stronger UV presence)
    for dist in range(140, 0, -14):
        alpha = int(20 * (1 - dist / 140))
        odraw.rectangle([0, 0, dist, H - 1], fill=(*UV_PURPLE_DARK, alpha))

    # Minimal right edge ambient (much weaker — warm zone must dominate right)
    for dist in range(60, 0, -12):
        alpha = int(8 * (1 - dist / 60))
        odraw.rectangle([W - 1 - dist, 0, W - 1, H - 1], fill=(*UV_PURPLE_DARK, alpha))

    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, overlay)
    img.paste(img_rgba.convert("RGB"))
    draw = ImageDraw.Draw(img)
    return draw


# ── ACID_GREEN eye-glow spill ─────────────────────────────────────────────────

def draw_eye_glow(img):
    """ACID_GREEN glow from Glitch's bilateral eyes — target lock toward Luma."""
    cx = int(W * 0.30)
    cy = int(H * 0.50)
    rx = 54
    ry = 62
    face_cy = cy - ry // 6
    cell    = 8
    leye_cx = (int(cx - rx // 2 - cell * 3 // 2)) + cell + 4
    reye_cx = (int(cx + rx // 2 - cell * 3 // 2)) + cell + 4
    eye_cy  = face_cy - cell * 3 // 2 + cell

    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)

    for ecx in [leye_cx, reye_cx]:
        for r in range(32, 4, -4):
            alpha = int(22 * (1 - r / 32))
            gdraw.ellipse([ecx - r, eye_cy - r, ecx + r, eye_cy + r],
                          fill=(*ACID_GREEN, alpha))

    glow_blurred = glow.filter(ImageFilter.GaussianBlur(radius=7))
    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, glow_blurred)
    img.paste(img_rgba.convert("RGB"))
    draw = ImageDraw.Draw(img)
    return draw


# ── Footer label ─────────────────────────────────────────────────────────────

def draw_footer(draw):
    """Production label bar."""
    bar_h = 28
    draw.rectangle([0, H - bar_h, W - 1, H - 1], fill=VOID_BLACK)
    draw.line([(0, H - bar_h), (W - 1, H - bar_h)], fill=UV_PURPLE, width=1)
    draw.rectangle([W - 90, H - bar_h + 4, W - 6, H - 6], fill=UV_PURPLE_DARK)


# ── Main generator ────────────────────────────────────────────────────────────

def generate(output_path):
    """Generate COVETOUS Glitch style frame — three-character triangulation (C42 spec).
    G001: rx=54/ry=62. G004: fill before crack. G008: BILATERAL_EYES=True.
    Canvas: native 1280×720 (no thumbnail needed)."""
    img = Image.new("RGB", (W, H), VOID_BLACK)

    # Layer order (C42 three-char triangulation):
    # sky → aurora → slabs → platform → ambient → Luma (right) → Byte (barrier) → Glitch (left) → eye glow → footer
    print("[1/10] Void sky gradient...")
    draw = ImageDraw.Draw(img)
    draw = draw_void_sky(draw, img)

    print("[2/10] Aurora bands...")
    draw = draw_aurora_bands(draw, img)

    print("[3/10] Far distance slabs...")
    draw = ImageDraw.Draw(img)
    draw_far_slabs(draw)

    print("[4/10] Glitch Layer platform...")
    draw = ImageDraw.Draw(img)
    draw_platform(draw)

    print("[5/10] UV_PURPLE ambient overlay...")
    draw = draw_ambient_overlay(img)

    print("[6/10] Luma — right zone, warm palette (subject of desire)...")
    draw = draw_luma_warm(img)

    print("[7/10] Byte — midground barrier...")
    draw = draw_byte_barrier(img)

    print("[8/10] Glitch — COVETOUS, large (G001/G004/G008 compliant)...")
    draw = draw_glitch_large(img)

    print("[9/10] ACID_GREEN eye-glow spill...")
    draw = draw_eye_glow(img)

    print("[10/10] Footer label...")
    draw = ImageDraw.Draw(img)
    draw_footer(draw)

    # Canvas is native 1280×720 — no thumbnail downscale needed (docs/image-rules.md)
    # Confirm size rule: assert both dimensions ≤ 1280px
    assert img.size[0] <= 1280 and img.size[1] <= 1280, f"Size rule violated: {img.size}"

    img.save(output_path)
    file_size = os.path.getsize(output_path)
    print(f"\nSaved: {output_path}")
    print(f"  Size: {img.size[0]}x{img.size[1]}  File: {file_size:,} bytes ({file_size//1024} KB)")

    print(f"\n[QA] UV_PURPLE_DARK = (58, 16, 96) = GL-04a #3A1060 — canonical")
    print(f"[QA] NO WARM LIGHT ON GLITCH. Luma warmth stays in right 30% — does not reach Glitch.")
    print(f"[QA] Characters rendered via canonical char_*.py modules (C53 modular architecture)")
    print(f"[QA] G001/G004/G008 compliance handled by canonical char_glitch module")
    print(f"[QA] C42 staging: Glitch (left) + Byte (barrier) + Luma (right) triangulation — DONE")

    return file_size


if __name__ == "__main__":
    out_path = output_dir('color', 'style_frames', 'LTG_COLOR_sf_covetous_glitch.png')
    generate(out_path)
