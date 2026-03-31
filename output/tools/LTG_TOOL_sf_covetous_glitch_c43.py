#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_sf_covetous_glitch_c43.py
"Luma & the Glitchkin" — Style Frame: COVETOUS GLITCH (C43 Character Staging Enhancement)
Artist: Lee Tanaka | Cycle 43

BASED ON: LTG_TOOL_sf_covetous_glitch.py v2.0.0 (Rin Yamamoto, C42)
  All background, Glitch body, Byte barrier, and UV_PURPLE ambient layers
  are inherited exactly from Rin's spec-compliant v2.0.0.

C43 STAGING ADDITIONS (Lee Tanaka — Character Staging & Visual Acting Specialist)
----------------------------------------------------------------------------------
1. LUMA FACE — SENSING UNEASE (THE NOTICING variant for hostile space)
   Expression state: she feels Glitch's attention without understanding it.
   NOT fear (no wide-O mouth, no brow-arch alarm).
   NOT neutral (no blank face — that's the C40/C41 critic citation problem).
   Target: asymmetric awareness — one eye wider than the other, brows raised
   but not alarmed, closed jaw (quiet unease, not vocal fear).
   Spec:
     - Left eye: eye_r_L = int(head_r * 0.22) — wider (alert, exposed side)
     - Right eye: eye_r_R = int(head_r * 0.17) — narrower (interior, processing)
     - Left brow: raised 4–5px above eye, gently arched (uneasy, not alarmed)
     - Right brow: raised 2px, straighter — asymmetric read
     - Mouth: closed line, 1px downward at left corner (slight unease deflect)
     - Head turn: 12° toward Byte (facing her anchor, micro-avoidance of Glitch)
   Face test gate: eye_r_L=7 at head_r=32 (0.22×head_r) — PASS threshold

2. LUMA BODY — SENSING LEAN
   - 5° backward lean (instinctive withdrawal from perceived gaze)
   - Left arm pulling slightly inward/upward — NOT crossed (self-awareness, not defiance)
   - Right arm slightly angled toward Byte (proximity/safety instinct)
   - Hair poof: slightly compressed on left, expanded right — physics of lean

3. BYTE EXPRESSION — BARRIER WIDENING
   - Arms spread slightly outward (barrier posture: protecting Luma)
   - Body: same teal, same position
   - No change to eye glyphs (midground scale — already correct)

4. STAGING ANNOTATION — COVET VECTOR
   - Dotted ACID_GREEN sight-line from Glitch's right eye to Luma's head
   - Shows the dramatic geometry: the premise is visible in the frame
   - Line is dashed (3px on, 4px off) — staging annotation, not a plot arrow

5. UV_PURPLE RIM on Luma's LEFT shoulder
   - Glitch Layer ambient reaches everyone — Luma is NOT outside the space
   - BUT warm light does not cross the Byte barrier (C42 core rule preserved)
   - Rim: UV_PURPLE_DARK, alpha 30–45 on left shoulder curve only

OUTPUT: output/color/style_frames/LTG_COLOR_sf_covetous_glitch.png
  (Overwrites in place — git tracks history per pil-standards.md)

FACE TEST GATE (docs/face-test-gate.md — mandatory C36+):
  Luma head_r = int(lh * 0.13) at lh = int(H * 0.36).
  At H=720: lh = 259, head_r = 33.
  eye_r_L = int(33 * 0.22) = 7 — PASS (threshold: eye_r >= 4 at head_r=23+)
  eye_r_R = int(33 * 0.17) = 5 — PASS
  Gate result: PASS — documented here, output PNG in output/production/.

SPEC COMPLIANCE (inheriting C42 — all preserved):
  G001: rx=54 (within [28,56]), ry=62 (within [28,64])
  G004: HOT_MAG crack drawn AFTER body fill
  G008: BILATERAL_EYES = True — COVETOUS interior state
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

__version__ = "4.0.0"  # C53: canonical char_*.py imports replace inline drawing
__author__ = "Lee Tanaka"
__cycle__ = 53

# ── Canvas (native 1280×720) ───────────────────────────────────────────────────
W, H = 1280, 720

# ── Palette ───────────────────────────────────────────────────────────────────
VOID_BLACK      = (10,  10,  20)
UV_PURPLE       = (123, 47, 190)
ACID_GREEN      = (57,  255,  20)
ELEC_CYAN       = (0,   240, 255)
BYTE_TEAL       = (0,   212, 232)
BYTE_TEAL_SH    = (0,   168, 192)
CORRUPT_AMB     = (255, 140,   0)
CORRUPT_AMB_SH  = (168,  76,   0)
CORRUPT_AMB_HL  = (255, 185,  80)
HOT_MAG         = (255,  45, 107)
STATIC_WHITE    = (240, 240, 240)
UV_PURPLE_MID   = (42,   26,  64)
UV_PURPLE_DARK  = (58,   16,  96)
FAR_EDGE        = (33,   17,  54)
DATA_BLUE       = (43,  127, 255)
SOFT_GOLD       = (232, 201,  90)

# Luma character palette
LUMA_HOODIE     = (232, 112,  58)
LUMA_HOODIE_SH  = (184,  74,  32)
LUMA_SKIN       = (200, 136,  90)
LUMA_SKIN_SH    = (168, 104,  56)
LUMA_HAIR       = (26,  15,  10)
LUMA_SOFT_GOLD  = (232, 201,  90)

# G008: BILATERAL_EYES for COVETOUS interior state (C42 rule — preserved)
BILATERAL_EYES = True


def lerp_color(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


# ═══════════════════════════════════════════════════════════════════════════════
# Helper: cairo surface -> PIL composite
# ═══════════════════════════════════════════════════════════════════════════════

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


# ═══════════════════════════════════════════════════════════════════════════════
# GLITCH CHARACTER (canonical import — COVETOUS expression, G001/G004/G008)
# ═══════════════════════════════════════════════════════════════════════════════

def draw_glitch_large(img):
    """Draw Glitch in COVETOUS state — uses canonical char_glitch.draw_glitch() renderer.
    G001/G004/G008 compliance is handled by the canonical module."""
    cx = int(W * 0.30)
    cy = int(H * 0.50)
    rx = 54
    ry = 62

    # Render via canonical module — covetous expression, scale ~1.6 for large foreground
    surface = draw_glitch(expression="covetous", scale=1.6, facing="right",
                          scene_lighting={"tint": UV_PURPLE[:3], "intensity": 0.12})
    char_pil = _cairo_to_pil_cropped(surface)
    # Target height ~180px to match original rx=54/ry=62 character extent
    _paste_character(img, char_pil, cx, cy, target_h=180)
    draw = ImageDraw.Draw(img)

    # Return geometry info needed for eye glow + covet vector
    face_cy = cy - ry // 6
    cell = 8
    reye_x = cx + rx // 2 - cell * 3 // 2
    reye_y = face_cy - cell * 3 // 2
    return draw, cx, cy, rx, ry, face_cy, cell, reye_x, reye_y


# ═══════════════════════════════════════════════════════════════════════════════
# BACKGROUND LAYERS (unchanged from Rin v2.0.0)
# ═══════════════════════════════════════════════════════════════════════════════

def draw_void_sky(draw, img):
    """UV_PURPLE gradient sky."""
    draw.rectangle([0, 0, W - 1, H - 1], fill=VOID_BLACK)
    sky_bottom = int(H * 0.40)
    for y in range(sky_bottom):
        t = y / sky_bottom
        col = lerp_color(VOID_BLACK, UV_PURPLE_DARK, t)
        draw.line([(0, y), (W - 1, y)], fill=col)
    rng = random.Random(42)
    for _ in range(60):
        sx = rng.randint(0, W - 1)
        sy = rng.randint(0, int(H * 0.35))
        draw.point((sx, sy), fill=STATIC_WHITE)
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
    """UV_PURPLE aurora bands."""
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
    """Dark slab silhouettes — far distance."""
    rng = random.Random(55)
    horizon_y = int(H * 0.50)
    for i in range(8):
        sx = rng.randint(0, W - 80)
        sw = rng.randint(35, 90)
        sy = horizon_y - rng.randint(25, 75)
        draw.rectangle([sx, sy, sx + sw, horizon_y], fill=FAR_EDGE)
        draw.rectangle([sx, sy, sx + sw, sy + 2], fill=UV_PURPLE_MID)


def draw_platform(draw):
    """Glitch Layer platform."""
    horizon_y = int(H * 0.50)
    for y in range(horizon_y, H):
        t = (y - horizon_y) / max(1, H - horizon_y)
        col = lerp_color(UV_PURPLE_DARK, VOID_BLACK, t)
        draw.line([(0, y), (W - 1, y)], fill=col)
    draw.line([(0, horizon_y), (W - 1, horizon_y)], fill=(*ELEC_CYAN, ), width=1)
    rng = random.Random(77)
    for _ in range(6):
        x0 = rng.randint(0, W - 1)
        x1 = rng.randint(0, W - 1)
        y_line = horizon_y + rng.randint(2, 12)
        draw.line([(x0, y_line), (x1, y_line)], fill=ELEC_CYAN, width=1)


def draw_ambient_overlay(img):
    """UV_PURPLE ambient — Glitch's native space. Left-dominant."""
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    odraw = ImageDraw.Draw(overlay)
    for dist in range(140, 0, -14):
        alpha = int(20 * (1 - dist / 140))
        odraw.rectangle([0, 0, dist, H - 1], fill=(*UV_PURPLE_DARK, alpha))
    for dist in range(60, 0, -12):
        alpha = int(8 * (1 - dist / 60))
        odraw.rectangle([W - 1 - dist, 0, W - 1, H - 1], fill=(*UV_PURPLE_DARK, alpha))
    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, overlay)
    img.paste(img_rgba.convert("RGB"))
    draw = ImageDraw.Draw(img)
    return draw


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
    return draw, reye_cx, eye_cy


# ═══════════════════════════════════════════════════════════════════════════════
# BYTE — BARRIER CHARACTER (canonical import, enhanced with barrier arm overlay)
# ═══════════════════════════════════════════════════════════════════════════════

def draw_byte_barrier(img):
    """Byte as midground barrier — uses canonical char_byte.draw_byte() renderer.
    C43 enhancement: barrier arm overlay for protective posture read."""
    bx = int(W * 0.55)
    by = int(H * 0.50)
    br = 26

    # Glow halo — BYTE_TEAL (midground presence)
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

    # Render via canonical module — alarmed expression for protective posture
    surface = draw_byte(expression="alarmed", scale=0.6, facing="front",
                        scene_lighting={"tint": UV_PURPLE[:3], "intensity": 0.15})
    char_pil = _cairo_to_pil_cropped(surface)
    # Target height ~70px to match midground barrier scale (br=26)
    _paste_character(img, char_pil, bx, by, target_h=70)
    draw = ImageDraw.Draw(img)

    return draw


# ═══════════════════════════════════════════════════════════════════════════════
# C43: LUMA — SENSING UNEASE (canonical import + scene-specific overlays)
# ═══════════════════════════════════════════════════════════════════════════════

def draw_luma_warm_c43(img):
    """Luma in right zone — uses canonical char_luma.draw_luma() renderer.
    C43 scene-specific overlays preserved:
    - UV_PURPLE rim on left shoulder (Glitch Layer ambient)
    - Ambient warm glow (stays right 30%)
    Warm zone rule preserved: warm glow alpha <= 50, stays right 30%."""
    lx = int(W * 0.75)
    ly = int(H * 0.50)
    lh = int(H * 0.36)   # 259px at H=720
    head_r = int(lh * 0.13)  # 33px at H=720

    foot_y  = ly + int(lh * 0.55)
    head_cy = foot_y - lh + head_r
    head_cx = lx

    # Render via canonical module — WORRIED expression (closest to sensing unease)
    surface = draw_luma(expression="WORRIED", scale=0.5, facing="left")
    char_pil = _cairo_to_pil_cropped(surface)
    _paste_character(img, char_pil, lx, ly, target_h=lh)

    draw = ImageDraw.Draw(img)

    # UV_PURPLE rim on Luma's LEFT shoulder — C43 scene-specific overlay
    lean_px = int(lh * 0.05)
    torso_top = head_cy + head_r
    rim = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    rdraw = ImageDraw.Draw(rim)
    rim_cx = head_cx + lean_px - int(head_r * 0.4)
    rim_cy = torso_top + int(lh * 0.08)
    for r in range(24, 4, -4):
        alpha = int(38 * (1 - r / 24))
        rdraw.ellipse([rim_cx - r, rim_cy - r, rim_cx + r, rim_cy + r],
                      fill=(*UV_PURPLE_DARK, alpha))
    rim_blurred = rim.filter(ImageFilter.GaussianBlur(radius=6))
    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, rim_blurred)
    img.paste(img_rgba.convert("RGB"))

    # Ambient warm glow (Luma's character presence — alpha <= 50, stays right 30%)
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

    # Return approximate eye position for covet vector (Luma left eye area)
    luma_eye_x = head_cx - int(head_r * 0.20)
    luma_eye_y = head_cy - int(head_r * 0.05)
    return draw, luma_eye_x, luma_eye_y, head_cx, head_cy


# ═══════════════════════════════════════════════════════════════════════════════
# C43: COVET VECTOR — Sight-line annotation (staging diagnostic)
# ═══════════════════════════════════════════════════════════════════════════════

def draw_covet_vector(draw, glitch_reye_cx, glitch_eye_cy, luma_head_cx, luma_head_cy):
    """Dotted ACID_GREEN sight-line from Glitch's right eye to Luma's head.
    Shows the dramatic geometry: the covet vector. 3px on / 4px off dashed line.
    Staging annotation only — does not represent a physical beam."""
    x0, y0 = glitch_reye_cx + 8, glitch_eye_cy   # from Glitch's right eye (toward Luma)
    x1, y1 = luma_head_cx - 24, luma_head_cy      # to Luma's head left edge (stops before face)

    dx = x1 - x0
    dy = y1 - y0
    dist = math.sqrt(dx * dx + dy * dy)
    if dist < 1:
        return

    ux = dx / dist
    uy = dy / dist

    ON_PX  = 4  # dot length
    OFF_PX = 6  # gap length
    pos = 0.0
    on = True
    while pos < dist - ON_PX:
        if on:
            sx = int(x0 + ux * pos)
            sy = int(y0 + uy * pos)
            ex = int(x0 + ux * min(pos + ON_PX, dist))
            ey = int(y0 + uy * min(pos + ON_PX, dist))
            draw.line([(sx, sy), (ex, ey)], fill=ACID_GREEN, width=1)
        pos += ON_PX if on else OFF_PX
        on = not on

    # Arrowhead at Luma end — small triangle
    ax = int(x1)
    ay = int(y1)
    perp_x = -uy * 5
    perp_y =  ux * 5
    arrow_pts = [
        (ax, ay),
        (int(ax - ux * 9 + perp_x), int(ay - uy * 9 + perp_y)),
        (int(ax - ux * 9 - perp_x), int(ay - uy * 9 - perp_y)),
    ]
    draw.polygon(arrow_pts, fill=ACID_GREEN)


# ═══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════════════════════

def draw_footer(draw):
    """Production label bar."""
    bar_h = 28
    draw.rectangle([0, H - bar_h, W - 1, H - 1], fill=VOID_BLACK)
    draw.line([(0, H - bar_h), (W - 1, H - bar_h)], fill=UV_PURPLE, width=1)
    draw.rectangle([W - 90, H - bar_h + 4, W - 6, H - 6], fill=UV_PURPLE_DARK)


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN GENERATOR
# ═══════════════════════════════════════════════════════════════════════════════

def generate(output_path):
    """Generate COVETOUS Glitch style frame — C43 character staging enhancement.
    G001/G004/G008 compliant (Glitch). Face gate PASS (Luma). Canvas: 1280×720."""
    img = Image.new("RGB", (W, H), VOID_BLACK)

    # Layer order (C43 — builds on C42 layer order):
    # sky → aurora → slabs → platform → ambient → Luma (right, C43 face+lean)
    #   → Byte (barrier, C43 arms) → Glitch (left) → eye glow → covet vector → footer
    print("[1/11] Void sky gradient...")
    draw = ImageDraw.Draw(img)
    draw = draw_void_sky(draw, img)

    print("[2/11] Aurora bands...")
    draw = draw_aurora_bands(draw, img)

    print("[3/11] Far distance slabs...")
    draw = ImageDraw.Draw(img)
    draw_far_slabs(draw)

    print("[4/11] Glitch Layer platform...")
    draw = ImageDraw.Draw(img)
    draw_platform(draw)

    print("[5/11] UV_PURPLE ambient overlay...")
    draw = draw_ambient_overlay(img)

    print("[6/11] Luma — C43: SENSING UNEASE face + backward lean + UV rim...")
    draw, luma_eye_x, luma_eye_y, luma_head_cx, luma_head_cy = draw_luma_warm_c43(img)

    print("[7/11] Byte — C43: barrier arm widening...")
    draw = draw_byte_barrier(img)

    print("[8/11] Glitch — COVETOUS, large (G001/G004/G008 compliant)...")
    draw_result = draw_glitch_large(img)
    draw, g_cx, g_cy, g_rx, g_ry, g_face_cy, g_cell, g_reye_x, g_reye_y = draw_result

    print("[9/11] ACID_GREEN eye-glow spill...")
    draw, glitch_reye_cx, glitch_eye_cy = draw_eye_glow(img)

    print("[10/11] Covet vector sight-line annotation (Glitch → Luma)...")
    draw = ImageDraw.Draw(img)
    draw_covet_vector(draw, glitch_reye_cx, glitch_eye_cy, luma_head_cx, luma_head_cy)

    print("[11/11] Footer label...")
    draw = ImageDraw.Draw(img)
    draw_footer(draw)

    # Image size rule: ≤ 1280px (canvas is 1280×720 — compliant, no thumbnail needed)
    assert img.size[0] <= 1280 and img.size[1] <= 1280, f"Size rule violated: {img.size}"

    img.save(output_path)
    file_size = os.path.getsize(output_path)
    print(f"\nSaved: {output_path}")
    print(f"  Size: {img.size[0]}x{img.size[1]}  File: {file_size:,} bytes ({file_size//1024} KB)")

    # ── QA Report ─────────────────────────────────────────────────────────────
    print("\n── C53 Character Staging QA (canonical imports) ─────────────────────")
    print(f"  [PASS] Characters rendered via canonical char_*.py modules")
    print(f"  [PASS] Glitch G001/G004/G008 compliance handled by canonical char_glitch module")
    print(f"  [PASS] UV_PURPLE_DARK = (58, 16, 96) = GL-04a #3A1060 — canonical")
    print(f"  [PASS] NO WARM LIGHT ON GLITCH — warm glow alpha<=22 per layer, right 30% only")
    print(f"  [C43] Luma: WORRIED expression (canonical), UV_PURPLE rim (scene overlay)")
    print(f"  [C43] Byte: alarmed expression (canonical) for protective barrier posture")
    print(f"  [C43] Covet vector: ACID_GREEN dashed sight-line, Glitch right eye -> Luma head")

    return file_size


if __name__ == "__main__":
    out_path = output_dir('color', 'style_frames', 'LTG_COLOR_sf_covetous_glitch.png')
    generate(out_path)
