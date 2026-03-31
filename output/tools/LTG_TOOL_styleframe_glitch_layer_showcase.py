#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_styleframe_glitch_layer_showcase.py
"Luma & the Glitchkin" — Style Frame: GLITCH LAYER SHOWCASE

Artist: Rin Yamamoto | Cycle 47

BRIEF (C47 — Zoe Park critique response)
-----------------------------------------
Zoe Park feedback: "No Glitch Layer in pitch sequence." The show's USP is invisible
in the current pitch lineup. This frame is a dedicated Glitch Layer showcase that sells
the visual identity of the GL world to an executive audience.

COMPOSITION
-----------
- Location: Deep Glitch Layer — a vast CRT-interior void.
- VOID_BLACK base, UV_PURPLE ambient everywhere, ELEC_CYAN accents.
- Scanline texture across entire frame (CRT interior canonical).
- Inverted atmospheric perspective: farther = darker + more purple.
- Byte character — medium scale, native environment (confident, at home).
- Glitch character — background, smaller (looming presence, watchful).
- Data aurora bands, floating platform geometry, circuit trace lines.
- NO warm light sources. UV_PURPLE ambient only.
- This is the frame that tells an exec "this show looks like nothing else on air."

OUTPUT: output/color/style_frames/LTG_COLOR_styleframe_glitch_layer_showcase.png

CRITICAL RULES:
  - ZERO warm light. UV ambient only.
  - UV_PURPLE_DARK = GL-04a (58, 16, 96) — canonical.
  - After every img.paste() / alpha_composite: refresh draw = ImageDraw.Draw(img).
  - Canvas: native 1280×720 (no thumbnail downscale — eliminates LANCZOS drift).
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
import random
import sys
from PIL import Image, ImageDraw, ImageFilter

# Canonical character renderer imports
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
from LTG_TOOL_char_byte import draw_byte
from LTG_TOOL_char_glitch import draw_glitch
from LTG_TOOL_cairo_primitives import to_pil_rgba

__version__ = "2.0.0"  # C53: canonical char_*.py imports replace inline drawing
__author__ = "Rin Yamamoto"
__cycle__ = 53

# ── Canvas (native 1280×720) ────────────────────────────────────────────────
W, H = 1280, 720

# ── Palette (GL canonical — master_palette.md) ──────────────────────────────
VOID_BLACK      = (10,  10,  20)
UV_PURPLE       = (123, 47, 190)      # GL-04 #7B2FBE
UV_PURPLE_MID   = (42,   26,  64)
UV_PURPLE_DARK  = (58,   16,  96)     # GL-04a #3A1060 — 72% sat. Canonical.
FAR_EDGE        = (33,   17,  54)
ELEC_CYAN       = (0,   240, 255)     # GL-01a
ELEC_CYAN_DIM   = (0,   120, 140)     # GL-01a dimmed for far accents
BYTE_TEAL       = (0,   212, 232)     # GL-01b
BYTE_TEAL_SH    = (0,   168, 192)     # GL-01b shadow
DATA_BLUE       = (43,  127, 255)
ACID_GREEN      = (57,  255,  20)     # GL-03 #39FF14
HOT_MAG         = (255,  45, 107)     # GL-06
CORRUPT_AMB     = (255, 140,   0)     # GL-07
CORRUPT_AMB_SH  = (168,  76,   0)
STATIC_WHITE    = (240, 240, 240)


def lerp_color(a, b, t):
    """Linear interpolation between two RGB tuples."""
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


# ── Background: Deep Glitch Layer Void ──────────────────────────────────────

def draw_void_gradient(draw):
    """Full-canvas UV_PURPLE gradient — inverted atmospheric perspective.
    Top = lighter UV_PURPLE (distant glow), bottom = VOID_BLACK (deep void beneath platform)."""
    # Sky zone: top third — UV_PURPLE_DARK to VOID_BLACK (inverted: more purple = farther)
    sky_bottom = int(H * 0.45)
    for y in range(sky_bottom):
        t = y / sky_bottom
        col = lerp_color(UV_PURPLE_DARK, UV_PURPLE_MID, t * 0.6)
        draw.line([(0, y), (W - 1, y)], fill=col)
    # Below sky: transition to void
    for y in range(sky_bottom, H):
        t = (y - sky_bottom) / max(1, H - sky_bottom)
        col = lerp_color(UV_PURPLE_MID, VOID_BLACK, t)
        draw.line([(0, y), (W - 1, y)], fill=col)


def draw_stars(draw):
    """Sparse data-point stars — Glitch Layer 'digital sky' particles."""
    rng = random.Random(47)
    for _ in range(80):
        sx = rng.randint(0, W - 1)
        sy = rng.randint(0, int(H * 0.40))
        brightness = rng.randint(140, 240)
        if rng.random() < 0.3:
            # Cyan data point
            draw.point((sx, sy), fill=ELEC_CYAN_DIM)
        else:
            draw.point((sx, sy), fill=(brightness, brightness, brightness + 15))


def draw_data_aurora(img):
    """UV_PURPLE and DATA_BLUE aurora bands — Glitch Layer ambient signature.
    Multiple layers at different heights for depth."""
    aurora = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    adraw = ImageDraw.Draw(aurora)
    rng = random.Random(23)

    # Primary aurora band — UV_PURPLE dominant, mid-sky
    band_y = int(H * 0.22)
    for i in range(7):
        y0 = band_y + rng.randint(-30, 30)
        y1 = y0 + rng.randint(4, 14)
        alpha = rng.randint(14, 36)
        adraw.rectangle([0, y0, W - 1, y1], fill=(*UV_PURPLE, alpha))

    # Secondary — DATA_BLUE streaks
    for i in range(4):
        y0 = band_y + rng.randint(-40, 40)
        y1 = y0 + rng.randint(2, 6)
        alpha = rng.randint(8, 20)
        adraw.rectangle([0, y0, W - 1, y1], fill=(*DATA_BLUE, alpha))

    # Tertiary — faint ELEC_CYAN wisps higher up
    for i in range(3):
        y0 = int(H * 0.10) + rng.randint(-10, 20)
        y1 = y0 + rng.randint(1, 4)
        alpha = rng.randint(6, 14)
        adraw.rectangle([0, y0, W - 1, y1], fill=(*ELEC_CYAN, alpha))

    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, aurora)
    img.paste(img_rgba.convert("RGB"))
    draw = ImageDraw.Draw(img)
    return draw


def draw_ring_megastructure(img):
    """Distant ring megastructure — canonical Other Side/GL far-distance element.
    Very faint, large — conveys impossible digital scale."""
    ring_cx = int(W * 0.65)
    ring_cy = int(H * 0.18)
    ring_r = int(H * 0.38)

    ring_overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ring_draw = ImageDraw.Draw(ring_overlay)

    # Outer ring — faint UV_PURPLE
    ring_draw.ellipse(
        [ring_cx - ring_r, ring_cy - ring_r,
         ring_cx + ring_r, ring_cy + ring_r],
        outline=(*UV_PURPLE, 22), width=2
    )
    # Inner ring — slightly smaller, even fainter
    inner_r = int(ring_r * 0.85)
    ring_draw.ellipse(
        [ring_cx - inner_r, ring_cy - inner_r,
         ring_cx + inner_r, ring_cy + inner_r],
        outline=(*UV_PURPLE_DARK, 255), width=1
    )
    # Arc accent — ELEC_CYAN partial arc (data transfer visual)
    arc_r = int(ring_r * 0.92)
    ring_draw.arc(
        [ring_cx - arc_r, ring_cy - arc_r,
         ring_cx + arc_r, ring_cy + arc_r],
        start=200, end=280,
        fill=(*ELEC_CYAN, 16), width=1
    )

    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, ring_overlay)
    img.paste(img_rgba.convert("RGB"))
    draw = ImageDraw.Draw(img)
    return draw


def draw_far_slabs(draw):
    """Dark slab silhouettes at horizon — Glitch Layer architecture.
    Inverted atmospheric perspective: farther = darker + more purple."""
    rng = random.Random(99)
    horizon_y = int(H * 0.48)

    # Far distance slabs (very dark, barely visible)
    for i in range(10):
        sx = rng.randint(-20, W - 60)
        sw = rng.randint(30, 100)
        sh = rng.randint(20, 70)
        sy = horizon_y - sh
        # Farther = darker (FAR_EDGE)
        draw.rectangle([sx, sy, sx + sw, horizon_y], fill=FAR_EDGE)
        # Top edge highlight — UV_PURPLE_MID (distant glow)
        draw.rectangle([sx, sy, sx + sw, sy + 2], fill=UV_PURPLE_MID)

    # Mid-distance slabs (slightly brighter, UV_PURPLE tinted)
    for i in range(5):
        sx = rng.randint(0, W - 80)
        sw = rng.randint(40, 70)
        sh = rng.randint(30, 55)
        sy = horizon_y - sh + rng.randint(5, 15)
        col = lerp_color(FAR_EDGE, UV_PURPLE_DARK, 0.3)
        draw.rectangle([sx, sy, sx + sw, horizon_y + 3], fill=col)
        # ELEC_CYAN top-edge accent (digital architecture glow)
        draw.line([(sx, sy), (sx + sw, sy)], fill=ELEC_CYAN_DIM, width=1)


def draw_platform_system(draw, img):
    """Floating platform grid — the Glitch Layer's ground plane.
    Platform as a floating digital construct with ELEC_CYAN circuit edges."""
    horizon_y = int(H * 0.48)

    # Main platform surface: UV_PURPLE_DARK gradient to VOID_BLACK
    for y in range(horizon_y, H):
        t = (y - horizon_y) / max(1, H - horizon_y)
        col = lerp_color(UV_PURPLE_DARK, VOID_BLACK, t * 0.8 + 0.2)
        draw.line([(0, y), (W - 1, y)], fill=col)

    # Platform leading edge — bright ELEC_CYAN line (canonical GL depth system)
    draw.line([(0, horizon_y), (W - 1, horizon_y)], fill=ELEC_CYAN, width=2)

    # Circuit trace grid on platform
    rng = random.Random(88)
    # Horizontal traces
    for _ in range(8):
        x0 = rng.randint(0, W // 2)
        x1 = x0 + rng.randint(60, 300)
        y_line = horizon_y + rng.randint(4, int((H - horizon_y) * 0.5))
        alpha_val = rng.randint(30, 80)
        # Draw on overlay for alpha control
        trace_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        tdraw = ImageDraw.Draw(trace_layer)
        tdraw.line([(x0, y_line), (min(x1, W - 1), y_line)],
                   fill=(*ELEC_CYAN, alpha_val), width=1)
        img_rgba = img.convert("RGBA")
        img_rgba = Image.alpha_composite(img_rgba, trace_layer)
        img.paste(img_rgba.convert("RGB"))

    # Vertical traces (perspective convergence toward center)
    draw = ImageDraw.Draw(img)
    cx = int(W * 0.5)
    vanish_y = horizon_y
    for _ in range(6):
        bx = rng.randint(int(W * 0.1), int(W * 0.9))
        by = H - 1
        # Trace from bottom to horizon, converging toward center
        mid_x = bx + int((cx - bx) * 0.6)
        mid_y = vanish_y + int((by - vanish_y) * 0.3)
        trace_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        tdraw = ImageDraw.Draw(trace_layer)
        tdraw.line([(bx, by), (mid_x, mid_y)],
                   fill=(*ELEC_CYAN_DIM, 40), width=1)
        img_rgba = img.convert("RGBA")
        img_rgba = Image.alpha_composite(img_rgba, trace_layer)
        img.paste(img_rgba.convert("RGB"))

    draw = ImageDraw.Draw(img)

    # Node points at circuit intersections
    for _ in range(12):
        nx = rng.randint(0, W - 1)
        ny = horizon_y + rng.randint(6, int((H - horizon_y) * 0.4))
        ns = rng.choice([2, 3])
        draw.rectangle([nx, ny, nx + ns, ny + ns], fill=ELEC_CYAN)

    return draw


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


# ── Byte Character (foreground, medium scale — canonical import) ──────────────

def draw_byte_character(img):
    """Byte — medium scale, foreground, confident in native environment.
    Uses canonical char_byte.draw_byte() renderer.
    Placed center-left, facing right."""
    bx = int(W * 0.38)
    by = int(H * 0.52)
    br = 38  # medium scale — this is Byte's home

    # Teal glow halo (Byte's native energy — stronger here than in Real World)
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    for radius in range(br + 40, br - 1, -3):
        alpha = int(35 * (1 - (radius - br) / 40))
        if alpha > 0:
            gdraw.ellipse(
                [bx - radius, by - radius, bx + radius, by + radius],
                fill=(*BYTE_TEAL, alpha)
            )
    glow_blurred = glow.filter(ImageFilter.GaussianBlur(radius=8))
    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, glow_blurred)
    img.paste(img_rgba.convert("RGB"))

    # Render via canonical module — neutral/confident expression
    surface = draw_byte(expression="neutral", scale=0.9, facing="right",
                        scene_lighting={"tint": UV_PURPLE[:3], "intensity": 0.10})
    char_pil = _cairo_to_pil_cropped(surface)
    # Target height ~100px to match medium foreground scale (br=38)
    _paste_character(img, char_pil, bx, by, target_h=100)
    draw = ImageDraw.Draw(img)

    return draw


# ── Glitch Character (background, smaller — canonical import) ────────────────

def draw_glitch_background(img):
    """Glitch — background, smaller, lurking in the purple darkness.
    Uses canonical char_glitch.draw_glitch() renderer.
    Positioned right of center, elevated on a far platform.
    COVETOUS expression — watchful, predatory."""
    gx = int(W * 0.72)
    gy = int(H * 0.38)
    rx = 28  # smaller — background scale

    # Faint UV_PURPLE shadow halo (Glitch merges with the void)
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    for radius in range(rx + 20, rx - 1, -4):
        alpha = int(16 * (1 - (radius - rx) / 20))
        if alpha > 0:
            gdraw.ellipse(
                [gx - radius, gy - radius, gx + radius, gy + radius],
                fill=(*UV_PURPLE, alpha)
            )
    glow_blurred = glow.filter(ImageFilter.GaussianBlur(radius=6))
    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, glow_blurred)
    img.paste(img_rgba.convert("RGB"))

    # Render via canonical module — covetous expression, small background scale
    surface = draw_glitch(expression="covetous", scale=0.8, facing="left",
                          scene_lighting={"tint": UV_PURPLE[:3], "intensity": 0.20})
    char_pil = _cairo_to_pil_cropped(surface)
    # Target height ~90px to match background scale (rx=28, ry=34)
    _paste_character(img, char_pil, gx, gy, target_h=90)

    # ACID_GREEN eye glow spill (scene-specific overlay)
    eye_glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    egdraw = ImageDraw.Draw(eye_glow)
    for ecx in [gx - 8, gx + 8]:
        ecy = gy - 4
        for r in range(18, 3, -3):
            alpha = int(14 * (1 - r / 18))
            egdraw.ellipse([ecx - r, ecy - r, ecx + r, ecy + r],
                           fill=(*ACID_GREEN, alpha))
    eye_glow_blurred = eye_glow.filter(ImageFilter.GaussianBlur(radius=4))
    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, eye_glow_blurred)
    img.paste(img_rgba.convert("RGB"))
    draw = ImageDraw.Draw(img)

    return draw


# ── Floating Data Particles ─────────────────────────────────────────────────

def draw_data_particles(img):
    """Floating pixel particles — data debris in the Glitch Layer void.
    Mix of UV_PURPLE, ELEC_CYAN, and occasional DATA_BLUE."""
    particle_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    pdraw = ImageDraw.Draw(particle_layer)
    rng = random.Random(42)

    colors = [
        (*UV_PURPLE, 60),
        (*ELEC_CYAN, 40),
        (*DATA_BLUE, 35),
        (*UV_PURPLE_DARK, 80),
        (*STATIC_WHITE, 25),
    ]

    for _ in range(50):
        px = rng.randint(0, W - 1)
        py = rng.randint(int(H * 0.05), int(H * 0.85))
        sz = rng.choice([2, 3, 4, 5])
        col = rng.choice(colors)
        pdraw.rectangle([px, py, px + sz, py + sz], fill=col)

    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, particle_layer)
    img.paste(img_rgba.convert("RGB"))
    draw = ImageDraw.Draw(img)
    return draw


# ── Scanline Overlay (CRT interior canonical) ───────────────────────────────

def draw_scanlines(img):
    """CRT scanline overlay — the Glitch Layer IS a CRT interior.
    Uses render_lib compatible approach: semi-transparent dark horizontal lines."""
    scan_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(scan_layer)

    spacing = 4   # Every 4th pixel row
    alpha = 20    # Subtle but visible — this IS the GL identity

    for y in range(0, img.height, spacing):
        sd.line([(0, y), (img.width - 1, y)], fill=(0, 0, 0, alpha), width=1)

    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, scan_layer)
    img.paste(img_rgba.convert("RGB"))
    draw = ImageDraw.Draw(img)
    return draw


# ── UV Ambient Overlay ──────────────────────────────────────────────────────

def draw_uv_ambient(img):
    """UV_PURPLE ambient wash — the Glitch Layer's native light.
    Stronger than in COVETOUS or Other Side frames — this IS the GL showcase."""
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    odraw = ImageDraw.Draw(overlay)

    # Full-frame UV ambient (subtle — reinforces the purple everywhere)
    odraw.rectangle([0, 0, W - 1, H - 1], fill=(*UV_PURPLE, 8))

    # Stronger UV glow from upper-left (inverted atmo: far = brighter purple)
    for dist in range(200, 0, -10):
        alpha = int(12 * (1 - dist / 200))
        odraw.rectangle([0, 0, dist, int(H * 0.6)], fill=(*UV_PURPLE, alpha))

    # Bottom-right corner: deeper void (closer = less purple in GL inversion)
    for dist in range(120, 0, -12):
        alpha = int(6 * (1 - dist / 120))
        odraw.rectangle([W - 1 - dist, H - 1 - dist, W - 1, H - 1],
                        fill=(*VOID_BLACK, alpha))

    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, overlay)
    img.paste(img_rgba.convert("RGB"))
    draw = ImageDraw.Draw(img)
    return draw


# ── Vignette ────────────────────────────────────────────────────────────────

def draw_vignette(img):
    """Dark vignette — focuses eye to center where Byte stands."""
    vign = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    vdraw = ImageDraw.Draw(vign)

    cx, cy = W // 2, H // 2
    max_r = int(math.sqrt(cx * cx + cy * cy))

    for step in range(20):
        t = step / 20
        r = int(max_r * (1 - t * 0.4))
        alpha = int(40 * t)
        vdraw.ellipse([cx - r, cy - r, cx + r, cy + r],
                      outline=(*VOID_BLACK, alpha), width=max(8, int(max_r * 0.08)))

    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, vign)
    img.paste(img_rgba.convert("RGB"))
    draw = ImageDraw.Draw(img)
    return draw


# ── Footer Label ────────────────────────────────────────────────────────────

def draw_footer(draw):
    """Production label bar."""
    bar_h = 28
    draw.rectangle([0, H - bar_h, W - 1, H - 1], fill=VOID_BLACK)
    draw.line([(0, H - bar_h), (W - 1, H - bar_h)], fill=ELEC_CYAN, width=1)
    draw.rectangle([W - 90, H - bar_h + 4, W - 6, H - 6], fill=UV_PURPLE_DARK)


# ── Main Generator ──────────────────────────────────────────────────────────

OUTPUT_PATH = output_dir('color', 'style_frames', 'LTG_COLOR_styleframe_glitch_layer_showcase.png')


def generate(output_path=None):
    """Generate Glitch Layer Showcase style frame.
    Canvas: native 1280x720 (no thumbnail needed)."""
    if output_path is None:
        output_path = OUTPUT_PATH

    img = Image.new("RGB", (W, H), VOID_BLACK)

    # Layer order:
    # void gradient → stars → aurora → ring megastructure → far slabs →
    # platform system → UV ambient → Glitch (bg) → Byte (fg) →
    # data particles → scanlines → vignette → footer
    print("[1/12] Void gradient...")
    draw = ImageDraw.Draw(img)
    draw_void_gradient(draw)

    print("[2/12] Digital sky stars...")
    draw = ImageDraw.Draw(img)
    draw_stars(draw)

    print("[3/12] Data aurora bands...")
    draw = draw_data_aurora(img)

    print("[4/12] Ring megastructure...")
    draw = draw_ring_megastructure(img)

    print("[5/12] Far distance slabs...")
    draw = ImageDraw.Draw(img)
    draw_far_slabs(draw)

    print("[6/12] Platform system with circuit traces...")
    draw = ImageDraw.Draw(img)
    draw = draw_platform_system(draw, img)

    print("[7/12] UV_PURPLE ambient overlay...")
    draw = draw_uv_ambient(img)

    print("[8/12] Glitch — background, watchful presence...")
    draw = draw_glitch_background(img)

    print("[9/12] Byte — foreground, native environment...")
    draw = draw_byte_character(img)

    print("[10/12] Data particles...")
    draw = draw_data_particles(img)

    print("[11/12] CRT scanline overlay...")
    draw = draw_scanlines(img)

    print("[12/12] Vignette + footer...")
    draw = draw_vignette(img)
    draw = ImageDraw.Draw(img)
    draw_footer(draw)

    # Size rule check
    assert img.size[0] <= 1280 and img.size[1] <= 1280, f"Size rule violated: {img.size}"

    img.save(output_path)
    file_size = os.path.getsize(output_path)
    print(f"\nSaved: {output_path}")
    print(f"  Size: {img.size[0]}x{img.size[1]}  File: {file_size:,} bytes ({file_size // 1024} KB)")

    print(f"\n[QA] UV_PURPLE_DARK = (58, 16, 96) = GL-04a #3A1060 — canonical")
    print(f"[QA] ZERO warm light sources. UV ambient only.")
    print(f"[QA] Scanline overlay: spacing=4, alpha=20 — CRT interior canonical")
    print(f"[QA] Inverted atmospheric perspective: farther = darker + more purple")
    print(f"[QA] Byte (foreground, medium) + Glitch (background, small) — GL native")

    return file_size


if __name__ == "__main__":
    generate()
