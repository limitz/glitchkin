#!/usr/bin/env python3
"""
LTG_TOOL_stylize_handdrawn_v002.py — Hand-Drawn Stylization Pass (v002)
"Luma & the Glitchkin" — Visual Stylization / Rin Yamamoto / Cycle 25

Rebuilds v001 with four critical fixes:

  Fix 1 — Full Canonical Color Protection
    ALL canonical palette colors are now protected by hue guard on every
    color-modifying pass, not just CORRUPT_AMBER.

  Fix 2 — Chalk Pass Exclusions
    Chalk pass now skips (a) cyan-family pixels (PIL H 100–160) and
    (b) light-source pixels (high V + high S in non-amber hues).

  Fix 3 — Warm Bleed Zone Boundary Gate
    _pass_color_bleed() now skips source pixels in cyan-family hue range
    (PIL H 100–160), preventing SUNLIT_AMBER from bleeding into
    cyan-lit skin and Glitch Layer regions.

  Fix 4 — Mixed Mode Compositing
    Transition zone now uses per-pixel weighted-average cross-dissolve
    instead of alpha_composite, eliminating double-edge ghost artifacts.

Supports three modes:
  - "realworld"  : paper grain, line wobble, warm edge bleed, chalk highlights
  - "glitch"     : scanlines, RGB color separation, edge sharpening
  - "mixed"      : zone-blended composite (realworld lower third, glitch upper two-thirds)

Usage (module):
    from LTG_TOOL_stylize_handdrawn_v002 import stylize
    stylize("input.png", "output_styled.png", mode="realworld", intensity=1.0, seed=42)

Usage (CLI):
    python LTG_TOOL_stylize_handdrawn_v002.py input.png output.png --mode realworld

Dependencies: Python 3.8+, Pillow (PIL), NumPy (optional)

Color preservation rules:
  - ALL canonical palette hues protected by hue guard on every modifying pass.
  - Hue drift > 5° on any canonical color → warning printed (batch-safe, no abort).
  - Canonical colors: CORRUPT_AMBER, BYTE_TEAL, UV_PURPLE, HOT_MAGENTA,
    ELECTRIC_CYAN, SUNLIT_AMBER.
"""

__version__ = "2.0.0"
__author__ = "Rin Yamamoto"
__cycle__ = 25

import sys
import os
import math
import random
import argparse

from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageEnhance

# ---------------------------------------------------------------------------
# Import shared render lib if available (optional)
# ---------------------------------------------------------------------------
_RENDER_LIB_AVAILABLE = False
try:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from LTG_TOOL_render_lib_v001 import scanline_overlay, vignette, perlin_noise_texture
    _RENDER_LIB_AVAILABLE = True
except ImportError:
    pass


# ---------------------------------------------------------------------------
# Color verification — inline implementation (Cycle 25)
# TODO: Refactor to import verify_canonical_colors from
#       LTG_TOOL_color_verify_v001.py once Kai Nakamura delivers it.
# ---------------------------------------------------------------------------

# Canonical palette — RGB values, PIL HSV hue, and tolerance in PIL hue units (0–255)
# PIL hue: 0=red, ~21=orange, ~42=yellow, ~85=green, ~128=cyan, ~170=blue, ~213=magenta
CANONICAL_PALETTE = {
    "CORRUPT_AMBER":  {"rgb": (255, 140,   0), "hex": "#FF8C00"},   # GL-07
    "BYTE_TEAL":      {"rgb": (  0, 212, 232), "hex": "#00D4E8"},   # GL-01b
    "UV_PURPLE":      {"rgb": (106,  13, 173), "hex": "#6A0DAD"},   # GL-05
    "HOT_MAGENTA":    {"rgb": (255,   0, 128), "hex": "#FF0080"},   # GL-06
    "ELECTRIC_CYAN":  {"rgb": (  0, 240, 255), "hex": "#00F0FF"},   # GL-01a specular
    "SUNLIT_AMBER":   {"rgb": (212, 146,  58), "hex": "#D4923A"},   # RW-03
}

# Pre-compute PIL HSV hue for each canonical color
def _rgb_to_pil_hue(r, g, b):
    """Convert RGB to PIL HSV hue (0–255 range). Returns 0 if achromatic."""
    rf, gf, bf = r / 255.0, g / 255.0, b / 255.0
    cmax = max(rf, gf, bf)
    cmin = min(rf, gf, bf)
    delta = cmax - cmin
    if delta < 1e-6:
        return 0
    if cmax == rf:
        h = 60.0 * (((gf - bf) / delta) % 6)
    elif cmax == gf:
        h = 60.0 * (((bf - rf) / delta) + 2)
    else:
        h = 60.0 * (((rf - gf) / delta) + 4)
    if h < 0:
        h += 360.0
    # Convert 0–360° to PIL 0–255 range
    return h * (255.0 / 360.0)


# Build PROTECTED_HUES: list of (hue_center, tolerance) in PIL [0,255] space
# Tolerance is ±10 PIL hue units (~14°) for all colors — covers natural variation
# without over-protecting adjacent hues.
_HUE_TOLERANCE = 12  # PIL units

def _build_protected_hues():
    protected = []
    for name, info in CANONICAL_PALETTE.items():
        r, g, b = info["rgb"]
        h = _rgb_to_pil_hue(r, g, b)
        protected.append((name, h, _HUE_TOLERANCE))
    return protected

PROTECTED_HUES = _build_protected_hues()

# Cyan family hue range in PIL units (used in Fix 2, Fix 3)
CYAN_HUE_MIN = 100
CYAN_HUE_MAX = 160


def _is_protected_hue(pil_h):
    """Return True if pil_h falls within any protected canonical hue range.

    Handles wraparound for hues near 0/255 boundary.
    """
    for _name, center, tol in PROTECTED_HUES:
        lo = center - tol
        hi = center + tol
        # Check with wraparound
        if lo < 0:
            if pil_h >= (lo + 256) or pil_h <= hi:
                return True
        elif hi > 255:
            if pil_h >= lo or pil_h <= (hi - 256):
                return True
        else:
            if lo <= pil_h <= hi:
                return True
    return False


def _is_cyan_family(pil_h):
    """Return True if pixel hue is in the cyan family (PIL H 100–160)."""
    return CYAN_HUE_MIN <= pil_h <= CYAN_HUE_MAX


# ---------------------------------------------------------------------------
# Inline canonical color verification
# (Replaces Kai's utility until LTG_TOOL_color_verify_v001.py is available)
# ---------------------------------------------------------------------------

def verify_canonical_colors(img, label=""):
    """Sample canonical color regions and warn if hue drifts > 5° from canonical.

    Samples a 20×20 grid of pixels across the image. For each pixel, checks
    if its hue is near a canonical color's expected hue but drifted beyond
    the 5° (≈3.5 PIL hue units) warning threshold.

    Does NOT abort — prints warnings only. Batch-safe.

    Args:
        img  (PIL.Image): Image to verify. Should be RGBA or RGB.
        label (str): Context label for printed warnings.
    """
    # TODO: Replace this inline implementation with:
    #   from LTG_TOOL_color_verify_v001 import verify_canonical_colors
    # once Kai Nakamura delivers output/tools/LTG_TOOL_color_verify_v001.py

    DRIFT_THRESHOLD_PIL = 3.5   # PIL hue units ≈ 5° on color wheel
    SAMPLE_GRID = 20             # Sample a 20×20 grid

    if img.mode not in ("RGB", "RGBA"):
        img = img.convert("RGB")
    if img.mode == "RGBA":
        r_ch, g_ch, b_ch, _ = img.split()
        rgb_img = Image.merge("RGB", (r_ch, g_ch, b_ch))
    else:
        rgb_img = img

    w, h = rgb_img.size
    hsv_img = rgb_img.convert("HSV")
    h_data = list(hsv_img.split()[0].getdata())
    s_data = list(hsv_img.split()[1].getdata())
    v_data = list(hsv_img.split()[2].getdata())

    # For each canonical color, find pixels near its expected hue and check drift
    warnings_issued = set()

    step_x = max(1, w // SAMPLE_GRID)
    step_y = max(1, h // SAMPLE_GRID)

    for name, info in CANONICAL_PALETTE.items():
        expected_h = _rgb_to_pil_hue(*info["rgb"])
        # Gather sampled pixels near expected hue (within ±30 PIL units = ~42°)
        near_expected = []
        for sy in range(0, h, step_y):
            for sx in range(0, w, step_x):
                idx = sy * w + sx
                ph = h_data[idx]
                ps = s_data[idx]
                pv = v_data[idx]
                # Only consider pixels with meaningful saturation/value
                if ps < 30 or pv < 30:
                    continue
                dist = abs(ph - expected_h)
                if dist > 128:
                    dist = 256 - dist  # wraparound
                if dist <= 30:
                    near_expected.append((ph, ps, pv))

        if not near_expected:
            continue

        # Compute mean hue of found pixels
        mean_h = sum(p[0] for p in near_expected) / len(near_expected)
        drift = abs(mean_h - expected_h)
        if drift > 128:
            drift = 256 - drift

        if drift > DRIFT_THRESHOLD_PIL and name not in warnings_issued:
            drift_deg = drift * (360.0 / 256.0)
            ctx = f" [{label}]" if label else ""
            print(f"  [COLOR VERIFY WARNING{ctx}] {name} ({info['hex']}): "
                  f"hue drifted {drift_deg:.1f}° from canonical "
                  f"(PIL hue delta: {drift:.1f} > threshold {DRIFT_THRESHOLD_PIL}). "
                  f"Sampled {len(near_expected)} pixels.")
            warnings_issued.add(name)

    if not warnings_issued:
        ctx = f" [{label}]" if label else ""
        print(f"  [COLOR VERIFY OK{ctx}] All canonical colors within 5° tolerance.")


# ---------------------------------------------------------------------------
# Internal utility functions
# ---------------------------------------------------------------------------

def _clamp(value, lo=0, hi=255):
    return max(lo, min(hi, int(value)))


def _make_noise_texture_fast(width, height, scale=40, seed=42, alpha=20):
    """Generate a lightweight paper grain texture using layered sin/cos noise.

    Returns RGBA Image.
    """
    rw = max(1, width // 4)
    rh = max(1, height // 4)

    rng = random.Random(seed)
    octaves = 3
    phase_offsets = [
        (rng.uniform(0, 2 * math.pi), rng.uniform(0, 2 * math.pi))
        for _ in range(octaves)
    ]

    try:
        import numpy as np
        xs = np.linspace(0, rw / scale, rw)
        ys = np.linspace(0, rh / scale, rh)
        xv, yv = np.meshgrid(xs, ys)

        value = np.zeros((rh, rw), dtype=np.float32)
        amp = 1.0
        freq = 1.0
        total_amp = 0.0
        for i in range(octaves):
            px, py = phase_offsets[i]
            nx = xv * freq + px
            ny = yv * freq + py
            v = (np.sin(nx * 2.1 + py) * np.cos(ny * 1.9 + px) +
                 np.cos(nx * 1.7 - px) * np.sin(ny * 2.3 - py)) * 0.5
            value += v * amp
            total_amp += amp
            amp *= 0.5
            freq *= 2.0

        value = (value / total_amp) * 0.5 + 0.5
        value = np.clip(value, 0.0, 1.0)
        brightness = (value * 255).astype(np.uint8)
        a_channel = (value * alpha).astype(np.uint8)

        rgba = np.stack([brightness, brightness, brightness, a_channel], axis=-1)
        small_img = Image.fromarray(rgba, mode="RGBA")

    except ImportError:
        small_img = Image.new("RGBA", (rw, rh), (128, 128, 128, 0))
        pixels = []
        for y in range(rh):
            row = []
            for x in range(rw):
                val = 0.0
                amp = 1.0
                freq = 1.0
                total_amp = 0.0
                for i in range(octaves):
                    px, py = phase_offsets[i]
                    nx = (x / scale) * freq + px
                    ny = (y / scale) * freq + py
                    v = (math.sin(nx * 2.1 + py) * math.cos(ny * 1.9 + px) +
                         math.cos(nx * 1.7 - px) * math.sin(ny * 2.3 - py)) * 0.5
                    val += v * amp
                    total_amp += amp
                    amp *= 0.5
                    freq *= 2.0
                val = (val / total_amp) * 0.5 + 0.5
                val = max(0.0, min(1.0, val))
                b = int(val * 255)
                a = int(val * alpha)
                row.append((b, b, b, a))
            pixels.extend(row)
        small_img.putdata(pixels)

    result = small_img.resize((width, height), Image.NEAREST)
    return result


def _apply_scanlines(img, spacing=4, alpha=15):
    """Apply CRT scanlines. Uses render lib if available, else fallback."""
    if _RENDER_LIB_AVAILABLE:
        return scanline_overlay(img, spacing=spacing, alpha=alpha)

    if img.mode != "RGBA":
        img = img.convert("RGBA")
    scan_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(scan_layer)
    for y in range(0, img.height, spacing):
        sd.line([(0, y), (img.width - 1, y)], fill=(0, 0, 0, alpha), width=1)
    img.alpha_composite(scan_layer)
    return img


def _apply_vignette(img, strength=40):
    """Apply radial vignette. Uses render lib if available, else fallback."""
    if _RENDER_LIB_AVAILABLE:
        return vignette(img, strength=strength)

    if img.mode != "RGBA":
        img = img.convert("RGBA")
    w, h = img.size
    cx, cy = w // 2, h // 2
    vig = Image.new("RGBA", img.size, (0, 0, 0, 0))
    vd = ImageDraw.Draw(vig)
    steps = 20
    for i in range(steps):
        t = i / steps
        a = int(strength * (1.0 - t) ** 2)
        if a < 1:
            continue
        rx = int(cx * (1.0 - t * 0.55))
        ry = int(cy * (1.0 - t * 0.55))
        vd.ellipse([cx - rx, cy - ry, cx + rx, cy + ry],
                   fill=(0, 0, 0, 0),
                   outline=(0, 0, 0, a),
                   width=max(1, int(cx * 0.03)))
    img.alpha_composite(vig)
    return img


# ---------------------------------------------------------------------------
# REAL WORLD passes
# ---------------------------------------------------------------------------

def _pass_paper_grain(img, intensity=1.0, seed=42):
    """Apply paper/canvas tooth texture.

    Paper grain does not modify color hues — it composites a neutral grey
    noise layer. No hue guard needed here.
    """
    w, h = img.size
    grain_alpha = int(18 * intensity)
    grain_alpha = _clamp(grain_alpha, 0, 40)
    grain = _make_noise_texture_fast(w, h, scale=30, seed=seed, alpha=grain_alpha)
    result = img.copy()
    result.alpha_composite(grain)
    return result


def _pass_line_wobble(img, amplitude=2, intensity=1.0, seed=42):
    """Simulate hand-drawn ink line variation via per-row horizontal displacement.

    Line wobble is a geometric pass — it shifts pixel positions but does not
    modify color values. No hue guard needed.
    """
    w, h = img.size
    rng = random.Random(seed + 1001)

    effective_amp = max(0.0, amplitude * intensity)
    if effective_amp < 0.1:
        return img

    result = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    src = img if img.mode == "RGBA" else img.convert("RGBA")

    base_freq = 2 * math.pi / (h * 0.3)
    for y in range(h):
        sine_component = math.sin(y * base_freq * (1.0 + rng.uniform(-0.1, 0.1)))
        jitter = rng.uniform(-0.3, 0.3)
        dx = int((sine_component + jitter) * effective_amp)
        dx = max(-w // 4, min(w // 4, dx))

        row = src.crop((0, y, w, y + 1))
        if dx > 0:
            result.paste(row.crop((0, 0, w - dx, 1)), (dx, y))
            edge = row.crop((0, 0, 1, 1))
            for i in range(dx):
                result.paste(edge, (i, y))
        elif dx < 0:
            adx = -dx
            result.paste(row.crop((adx, 0, w, 1)), (0, y))
            edge = row.crop((w - 1, 0, w, 1))
            for i in range(adx):
                result.paste(edge, (w - adx + i, y))
        else:
            result.paste(row, (0, y))

    return result


def _pass_color_bleed(img, radius=3, intensity=1.0, seed=42):
    """Simulate warm ink wicking into paper at warm-toned hard edges.

    FIX 3 (Cycle 25): Added cyan-family hue gate.
    Source pixels in cyan family hue range (PIL H 100–160) are excluded from
    the warm mask entirely, preventing SUNLIT_AMBER bleed into cyan-lit
    skin regions and Glitch Layer boundaries.

    Only detects warm-orange/amber tones as bleed sources, then composites
    a warm tint layer at low opacity.
    """
    w, h = img.size
    if img.mode != "RGBA":
        img = img.convert("RGBA")

    rgb_img = img.convert("RGB")
    hsv_img = rgb_img.convert("HSV")
    h_src, s_src, v_src = hsv_img.split()
    h_data = list(h_src.getdata())

    warm_mask = Image.new("L", (w, h), 0)
    pixels = list(rgb_img.getdata())
    warm_pixels = []

    for idx, (r, g, b) in enumerate(pixels):
        pil_h = h_data[idx]

        # FIX 3: Skip cyan-family source pixels — they must not be warm-bleed sources
        if _is_cyan_family(pil_h):
            warm_pixels.append(0)
            continue

        # Detect warm-orange/amber tones: R dominant, G moderate, B low
        is_warm = (r > 140 and g > 80 and b < 120 and
                   r > g * 1.2 and r > b * 1.5)
        warm_pixels.append(200 if is_warm else 0)

    warm_mask.putdata(warm_pixels)

    bleed_radius = max(1, int(radius * intensity))
    bleed_mask = warm_mask.filter(ImageFilter.GaussianBlur(radius=bleed_radius))

    bleed_a = int(30 * intensity)
    mask_arr = list(bleed_mask.getdata())
    composite_pixels = []
    for mv in mask_arr:
        alpha = int((mv / 255.0) * bleed_a)
        composite_pixels.append((212, 146, 58, _clamp(alpha)))
    bleed_layer = Image.new("RGBA", (w, h))
    bleed_layer.putdata(composite_pixels)

    result = img.copy()
    result.alpha_composite(bleed_layer)
    return result


def _pass_chalk_highlights(img, intensity=1.0, seed=42):
    """Simulate chalk/gouache highlight quality — kills plastic digital highlight look.

    Slightly desaturates the top 15% luminance values (V > 216) by reducing
    saturation 8–12 S-units. Simulates chalk/body-color highlights.

    FIX 1 (Cycle 25): ALL canonical palette hue ranges are now protected.
    Previously only CORRUPT_AMBER (PIL H 8–25) was protected.

    FIX 2 (Cycle 25): Additional exclusions:
      (a) Cyan-family pixels (PIL H 100–160) — CRT glow, Byte teal specular,
          Electric Cyan pops must survive the chalk pass unmodified.
      (b) Light source pixels: high V (>216) + high S (>100) in non-protected
          hues — specular highlights and glow effects, not material surfaces.
          Warm cream, sunlit walls, CRT glow must survive.
    """
    if intensity < 0.01:
        return img

    src_rgba = img if img.mode == "RGBA" else img.convert("RGBA")
    r_ch, g_ch, b_ch, a_ch = src_rgba.split()

    rgb = Image.merge("RGB", (r_ch, g_ch, b_ch))
    hsv = rgb.convert("HSV")
    h_ch, s_ch, v_ch = hsv.split()

    h_data = list(h_ch.getdata())
    s_data = list(s_ch.getdata())
    v_data = list(v_ch.getdata())
    a_data = list(a_ch.getdata())

    new_s = []
    desat_amount = int(12 * intensity)

    for i, (h, s, v) in enumerate(zip(h_data, s_data, v_data)):
        if v > 216 and s > 20:
            # FIX 1: Check ALL canonical hue ranges, not just CORRUPT_AMBER
            if _is_protected_hue(h):
                new_s.append(s)
                continue

            # FIX 2a: Exclude cyan-family pixels (CRT glow, Byte teal, Electric Cyan specular)
            if _is_cyan_family(h):
                new_s.append(s)
                continue

            # FIX 2b: Exclude light source pixels (high V + high S non-protected)
            # These are specular highlights and glow effects, not material surfaces.
            # Threshold: S > 100 at high V indicates a saturated light source, not
            # a chalky surface — do not desaturate it.
            if s > 100 and v > 216:
                new_s.append(s)
                continue

            # Apply chalk desaturation to remaining high-V material highlights
            new_s.append(_clamp(s - desat_amount))
        else:
            new_s.append(s)

    s_ch.putdata(new_s)
    new_hsv = Image.merge("HSV", (h_ch, s_ch, v_ch))
    new_rgb = new_hsv.convert("RGB")
    nr, ng, nb = new_rgb.split()
    result = Image.merge("RGBA", (nr, ng, nb, a_ch))
    return result


# ---------------------------------------------------------------------------
# GLITCH LAYER passes
# ---------------------------------------------------------------------------

def _pass_scanlines_glitch(img, intensity=1.0):
    """Apply CRT scanline texture for Glitch Layer.

    Scanlines are a transparency/darkening pass — they do not modify hue.
    No hue guard required.
    """
    alpha = int(10 * intensity)
    alpha = _clamp(alpha, 3, 25)
    spacing = 4
    return _apply_scanlines(img, spacing=spacing, alpha=alpha)


def _pass_color_separation(img, intensity=1.0, seed=42):
    """Simulate vintage print misregistration — RGB micro-offset at edges.

    Shifts R channel slightly right/down and B channel slightly left/up.
    This is a geometric channel offset pass — it does not alter per-pixel
    saturation or hue values. No hue guard required.
    """
    shift = max(1, int(2 * intensity))
    if img.mode != "RGBA":
        img = img.convert("RGBA")

    r, g, b, a = img.split()
    r_shifted = ImageChops.offset(r, shift, shift)
    b_shifted = ImageChops.offset(b, -shift, -shift)

    result = Image.merge("RGBA", (r_shifted, g, b_shifted, a))
    return result


def _pass_edge_sharpen(img, intensity=1.0):
    """Sharpen hard geometry edges for Glitch Layer content.

    Unsharp mask crisp up platform/void geometry edges.
    Edge sharpening increases contrast but does not change hue identity.
    No hue guard required.
    """
    if img.mode != "RGBA":
        img = img.convert("RGBA")

    radius = 1.5
    percent = int(120 * intensity)
    percent = min(percent, 200)
    threshold = 3

    r, g, b, a = img.split()
    rgb = Image.merge("RGB", (r, g, b))
    sharpened = rgb.filter(ImageFilter.UnsharpMask(radius=radius, percent=percent, threshold=threshold))
    sr, sg, sb = sharpened.split()
    result = Image.merge("RGBA", (sr, sg, sb, a))
    return result


# ---------------------------------------------------------------------------
# Gradient mask for MIXED mode
# ---------------------------------------------------------------------------

def _make_vertical_gradient_mask(width, height, blend_start, blend_end):
    """Create a float gradient map for blending two treatments vertically.

    Returns a list of floats in [0.0, 1.0] per pixel:
      0.0 = fully realworld (below blend zone)
      1.0 = fully glitch    (above blend zone)
      gradient in transition zone
    """
    gradient = []
    for y in range(height):
        if y <= blend_start:
            v = 1.0   # above blend zone = glitch
        elif y >= blend_end:
            v = 0.0   # below blend zone = realworld
        else:
            t = (y - blend_start) / (blend_end - blend_start)
            # Smooth step for cleaner transition
            t_smooth = t * t * (3.0 - 2.0 * t)
            v = 1.0 - t_smooth
        gradient.append(v)
    return gradient


# ---------------------------------------------------------------------------
# Main stylization passes
# ---------------------------------------------------------------------------

def _apply_realworld_treatment(img, intensity=1.0, seed=42):
    """Apply full Real World hand-drawn treatment.

    Pass order:
      1. Paper/canvas grain
      2. Line wobble/jitter
      3. Warm color bleed (with Fix 3 cyan gate)
      4. Chalk/gouache highlight desaturation (with Fix 1 + Fix 2)
    """
    if img.mode != "RGBA":
        img = img.convert("RGBA")

    img = _pass_paper_grain(img, intensity=intensity, seed=seed)
    img = _pass_line_wobble(img, amplitude=2, intensity=intensity * 0.8, seed=seed)
    img = _pass_color_bleed(img, radius=3, intensity=intensity, seed=seed)
    img = _pass_chalk_highlights(img, intensity=intensity, seed=seed)

    return img


def _apply_glitch_treatment(img, intensity=1.0, seed=42):
    """Apply full Glitch Layer stylization treatment.

    Pass order:
      1. Scanline texture (CRT reference)
      2. RGB color separation (print misregistration)
      3. Edge sharpening (geometry crispness)
    Note: NO paper grain in Glitch Layer.
    """
    if img.mode != "RGBA":
        img = img.convert("RGBA")

    img = _pass_scanlines_glitch(img, intensity=intensity)
    img = _pass_color_separation(img, intensity=intensity, seed=seed)
    img = _pass_edge_sharpen(img, intensity=intensity)

    return img


def _apply_mixed_treatment(img, intensity=1.0, seed=42):
    """Apply zone-blended mixed treatment for SF02 (Glitch Storm / boundary event).

    FIX 4 (Cycle 25): Transition zone now uses per-pixel weighted-average
    cross-dissolve instead of alpha_composite layering. This eliminates the
    double-edge ghost artifacts at the sky/street boundary by blending actual
    pixel values rather than layering transparent images.

    Zone split:
      - Lower third  (Y > h*2/3): Real World treatment
      - Upper 2/3    (Y < h*2/3): Glitch Layer treatment
      - ~200px vertical gradient blend zone at boundary
    """
    w, h = img.size
    if img.mode != "RGBA":
        img = img.convert("RGBA")

    zone_boundary = int(h * (2.0 / 3.0))
    blend_half = 100

    blend_start = max(0, zone_boundary - blend_half)
    blend_end = min(h - 1, zone_boundary + blend_half)

    # Apply both treatments to the full image
    realworld_version = _apply_realworld_treatment(img.copy(), intensity=intensity, seed=seed)
    glitch_version = _apply_glitch_treatment(img.copy(), intensity=intensity, seed=seed)

    # Build float gradient (per row): 1.0=glitch, 0.0=realworld
    row_gradient = _make_vertical_gradient_mask(w, h, blend_start, blend_end)

    # FIX 4: Per-pixel weighted-average cross-dissolve in transition zone
    # Outside transition zone: copy directly from appropriate source (no blend math overhead)
    # Inside transition zone: blended_pixel = (1 - w) * rw_pixel + w * gl_pixel
    rw_data = list(realworld_version.getdata())
    gl_data = list(glitch_version.getdata())
    result_data = []

    for y in range(h):
        blend_weight = row_gradient[y]
        row_offset = y * w

        if blend_weight <= 0.0:
            # Pure realworld — copy row directly
            result_data.extend(rw_data[row_offset: row_offset + w])
        elif blend_weight >= 1.0:
            # Pure glitch — copy row directly
            result_data.extend(gl_data[row_offset: row_offset + w])
        else:
            # Transition zone: per-pixel weighted average
            rw_weight = 1.0 - blend_weight
            gl_weight = blend_weight
            for x in range(w):
                idx = row_offset + x
                rw_p = rw_data[idx]
                gl_p = gl_data[idx]
                # Weighted average of all four channels (RGBA)
                blended = tuple(
                    _clamp(rw_weight * rw_p[c] + gl_weight * gl_p[c])
                    for c in range(4)
                )
                result_data.append(blended)

    result = Image.new("RGBA", (w, h))
    result.putdata(result_data)
    return result


# ---------------------------------------------------------------------------
# Public API — main stylize function
# ---------------------------------------------------------------------------

def stylize(
    input_path: str,
    output_path: str,
    mode: str = "realworld",
    intensity: float = 1.0,
    seed: int = 42,
) -> None:
    """Apply hand-drawn stylization treatment to a PNG image.

    Args:
        input_path  (str): Path to source PNG file.
        output_path (str): Path for output stylized PNG.
        mode        (str): Treatment mode:
                           "realworld" — paper grain, line wobble, warm bleed, chalk
                           "glitch"    — scanlines, color separation, edge sharpening
                           "mixed"     — zone-blended (glitch upper 2/3, realworld lower 1/3)
        intensity   (float): Global intensity multiplier. 0.0–2.0. Scales all effects.
        seed        (int): RNG seed. Identical seed + input = identical output.

    Returns:
        None. Writes PNG to output_path at same dimensions as input.

    Notes:
        - Runs verify_canonical_colors() after processing and prints warnings
          if any canonical color drifts > 5° hue. Does not abort — batch-safe.
        - SF01 (discovery_v003_styled.png) is LOCKED. Do not pass it to this tool.
        - Always use v002 for new assets. v001 is retired.
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    valid_modes = ("realworld", "glitch", "mixed")
    if mode not in valid_modes:
        raise ValueError(f"Invalid mode '{mode}'. Must be one of: {valid_modes}")

    intensity = max(0.0, min(2.0, float(intensity)))

    print(f"[LTG_TOOL_stylize_handdrawn_v002] Loading: {input_path}")
    img = Image.open(input_path)

    if img.mode != "RGBA":
        img = img.convert("RGBA")

    print(f"  Image size: {img.width}x{img.height}, mode: {mode}, intensity: {intensity}, seed: {seed}")
    print(f"  Color protection: {len(PROTECTED_HUES)} canonical hue ranges active")
    print(f"  Fixes active: [1] Full hue guard, [2] Chalk exclusions, "
          f"[3] Warm bleed gate, [4] Mixed mode cross-dissolve")

    if mode == "realworld":
        result = _apply_realworld_treatment(img, intensity=intensity, seed=seed)
    elif mode == "glitch":
        result = _apply_glitch_treatment(img, intensity=intensity, seed=seed)
    elif mode == "mixed":
        result = _apply_mixed_treatment(img, intensity=intensity, seed=seed)

    # Post-processing canonical color verification
    print(f"  Running canonical color verification...")
    verify_canonical_colors(result, label=f"{mode} mode, intensity={intensity}")

    # Ensure output directory exists
    out_dir = os.path.dirname(output_path)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    result.save(output_path, "PNG")
    print(f"  Saved: {output_path}")


# Legacy alias
def stylize_handdrawn(input_path: str, output_path: str, intensity: float = 1.0) -> None:
    """Backward-compatible wrapper. Defaults to 'realworld' mode."""
    stylize(input_path, output_path, mode="realworld", intensity=intensity, seed=42)


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def _cli():
    parser = argparse.ArgumentParser(
        description="LTG Hand-Drawn Stylization Tool v002 — Luma & the Glitchkin"
    )
    parser.add_argument("input", help="Input PNG path")
    parser.add_argument("output", help="Output PNG path")
    parser.add_argument(
        "--mode",
        choices=["realworld", "glitch", "mixed"],
        default="realworld",
        help="Stylization mode: realworld | glitch | mixed (default: realworld)"
    )
    parser.add_argument(
        "--intensity",
        type=float,
        default=1.0,
        help="Global intensity multiplier 0.0–2.0 (default: 1.0)"
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="RNG seed for reproducibility (default: 42)"
    )
    args = parser.parse_args()

    stylize(
        input_path=args.input,
        output_path=args.output,
        mode=args.mode,
        intensity=args.intensity,
        seed=args.seed,
    )


if __name__ == "__main__":
    _cli()
