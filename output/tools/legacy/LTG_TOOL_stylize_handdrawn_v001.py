#!/usr/bin/env python3
"""
LTG_TOOL_stylize_handdrawn_v001.py — Hand-Drawn Stylization Pass
"Luma & the Glitchkin" — Visual Stylization / Rin Yamamoto / Cycle 23

Applies organic, hand-crafted stylization to digitally generated PNGs.
Supports three modes:
  - "realworld"  : paper grain, line wobble, warm edge bleed, chalk highlights
  - "glitch"     : scanlines, RGB color separation, edge sharpening
  - "mixed"      : zone-blended composite (realworld lower third, glitch upper two-thirds)

Usage (module):
    import sys, os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from LTG_TOOL_stylize_handdrawn_v001 import stylize

    stylize("input.png", "output_styled.png", mode="realworld", intensity=1.0, seed=42)

Usage (CLI):
    python LTG_TOOL_stylize_handdrawn_v001.py input.png output.png --mode realworld --intensity 1.0 --seed 42

Dependencies: Python 3.8+, Pillow (PIL), NumPy (optional, used for faster noise)
No external data files — all textures are procedurally generated.

Color preservation rule:
  - GL-07 CORRUPT_AMBER (#FF8C00) must never be desaturated. Protected by hue lock.
  - Canonical palette hues must not shift more than 5 degrees on the color wheel.
  - Stylization must not degrade image legibility at thumbnail scale (480px wide).

Pipeline notes:
  - Always refresh draw = ImageDraw.Draw(img) after any img.paste() call.
  - All outputs at same pixel dimensions as input (no scaling).
  - Handles 1920x1080 and 1280x720 inputs.
  - Seeded for reproducibility: identical inputs + seed = identical outputs.
"""

__version__ = "1.0.0"
__author__ = "Rin Yamamoto"
__cycle__ = 23

import sys
import os
import math
import random
import argparse

from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageEnhance

# ---------------------------------------------------------------------------
# Import shared render lib if available (optional — we implement our own passes)
# ---------------------------------------------------------------------------
_RENDER_LIB_AVAILABLE = False
try:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from LTG_TOOL_render_lib_v001 import scanline_overlay, vignette, perlin_noise_texture
    _RENDER_LIB_AVAILABLE = True
except ImportError:
    pass  # We provide our own fallback implementations below


# ---------------------------------------------------------------------------
# CORRUPT_AMBER protection — GL-07 hue lock
# This color must never be desaturated in any pass.
# ---------------------------------------------------------------------------
CORRUPT_AMBER_HEX = "#FF8C00"
CORRUPT_AMBER_RGB = (255, 140, 0)

# Canonical palette colors (for reference / future hue-guard passes)
CANONICAL_PALETTE = {
    "SUNLIT_AMBER":   (212, 146, 58),    # RW-03
    "BYTE_TEAL":      (0,   212, 232),   # GL-01b
    "UV_PURPLE":      (106,  13, 173),   # GL-05 / DRW-18 variant
    "CORRUPT_AMBER":  (255, 140,   0),   # GL-07 — PROTECTED
    "VOID_BLACK":     (10,   10,  20),   # GL-00
}


# ---------------------------------------------------------------------------
# Internal utility functions
# ---------------------------------------------------------------------------

def _clamp(value, lo=0, hi=255):
    return max(lo, min(hi, int(value)))


def _make_noise_texture_fast(width, height, scale=40, seed=42, alpha=20):
    """Generate a lightweight paper grain texture using layered sin/cos noise.

    Pure Python implementation — no NumPy required. Works at reduced resolution
    then upscales to avoid the O(W*H) pixel loop on large canvases.

    Returns RGBA Image.
    """
    # Work at 1/4 resolution to keep performance reasonable
    rw = max(1, width // 4)
    rh = max(1, height // 4)

    rng = random.Random(seed)
    octaves = 3
    phase_offsets = [
        (rng.uniform(0, 2 * math.pi), rng.uniform(0, 2 * math.pi))
        for _ in range(octaves)
    ]

    # Try numpy first for performance
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
        # Pure Python fallback
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

    # Upscale back to full resolution with nearest-neighbor (preserve grain character)
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
    """Apply paper/canvas tooth texture — subtle felt-tip-on-paper roughness.

    Uses noise texture in OVERLAY blend mode equivalent (soft light compositing).
    At full intensity: barely perceptible at 100%, visible at 50% zoom.
    """
    w, h = img.size
    # Alpha calibrated for barely-perceptible at full res
    grain_alpha = int(18 * intensity)
    grain_alpha = _clamp(grain_alpha, 0, 40)

    grain = _make_noise_texture_fast(w, h, scale=30, seed=seed, alpha=grain_alpha)

    # Composite grain over image — adds texture without darkening overall
    result = img.copy()
    result.alpha_composite(grain)
    return result


def _pass_line_wobble(img, amplitude=2, intensity=1.0, seed=42):
    """Simulate hand-drawn ink line variation via per-row horizontal displacement.

    Applies a subtle sinusoidal + noise-based horizontal shift to each row.
    Maximum displacement: 1–3px depending on amplitude * intensity.
    Effect is most visible on hard vertical edges (ink wobble characteristic).
    """
    w, h = img.size
    rng = random.Random(seed + 1001)

    # Build displacement map per row: small sinusoidal + random jitter
    effective_amp = max(0.0, amplitude * intensity)
    if effective_amp < 0.1:
        return img

    # Create output by shifting rows
    result = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    src = img if img.mode == "RGBA" else img.convert("RGBA")

    # Phase varies smoothly over height with added per-row jitter
    base_freq = 2 * math.pi / (h * 0.3)
    for y in range(h):
        # Smooth sinusoidal displacement + tiny random jitter
        sine_component = math.sin(y * base_freq * (1.0 + rng.uniform(-0.1, 0.1)))
        jitter = rng.uniform(-0.3, 0.3)
        dx = int((sine_component + jitter) * effective_amp)

        # Clamp displacement to [-(w//4), w//4]
        dx = max(-w // 4, min(w // 4, dx))

        # Crop and paste the row with offset
        row = src.crop((0, y, w, y + 1))
        if dx > 0:
            # Shift right: paste starting at dx, fill left edge with first pixel
            result.paste(row.crop((0, 0, w - dx, 1)), (dx, y))
            edge = row.crop((0, 0, 1, 1))
            for i in range(dx):
                result.paste(edge, (i, y))
        elif dx < 0:
            # Shift left
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

    At warm color boundaries (amber/terracotta regions), creates a soft
    hue-warm blur that bleeds outward 2–4px. Simulates capillary action
    of ink on paper tooth.

    Implementation: dilate warm-hue regions with a small Gaussian blur,
    then composite at low opacity to add warmth at edges.
    """
    w, h = img.size
    if img.mode != "RGBA":
        img = img.convert("RGBA")

    # Extract warm-hue regions (hues roughly 20–50 degrees: amber, gold, terracotta)
    rgb_img = img.convert("RGB")
    warm_mask = Image.new("L", (w, h), 0)
    pixels = list(rgb_img.getdata())
    warm_pixels = []

    for r, g, b in pixels:
        # Detect warm-orange/amber tones: R dominant, G moderate, B low
        # Also avoid pure desaturated greys
        is_warm = (r > 140 and g > 80 and b < 120 and
                   r > g * 1.2 and r > b * 1.5)
        warm_pixels.append(200 if is_warm else 0)

    warm_mask.putdata(warm_pixels)

    # Dilate the warm mask outward (simulates bleed radius)
    bleed_radius = max(1, int(radius * intensity))
    bleed_mask = warm_mask.filter(ImageFilter.GaussianBlur(radius=bleed_radius))

    # Create warm-toned bleed layer (soft amber tint)
    bleed_color = Image.new("RGBA", (w, h), (212, 146, 58, 0))  # SUNLIT_AMBER base
    bleed_a = int(30 * intensity)
    bleed_color_arr = list(bleed_color.getdata())

    mask_arr = list(bleed_mask.getdata())
    composite_pixels = []
    for i, mv in enumerate(mask_arr):
        alpha = int((mv / 255.0) * bleed_a)
        composite_pixels.append((212, 146, 58, _clamp(alpha)))
    bleed_layer = Image.new("RGBA", (w, h))
    bleed_layer.putdata(composite_pixels)

    result = img.copy()
    result.alpha_composite(bleed_layer)
    return result


def _pass_chalk_highlights(img, intensity=1.0, seed=42):
    """Simulate chalk/gouache highlight quality — kills plastic digital highlight look.

    Slightly desaturates the top 15% luminance values (specular highlights)
    by reducing saturation 8–12%. This simulates chalk/body-color highlights
    that absorb into paper rather than specularly reflecting.

    CORRUPT_AMBER (#FF8C00) hue region is protected — no desaturation applied there.
    """
    if intensity < 0.01:
        return img

    # Work in RGB for HSV operations
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
    desat_amount = int(12 * intensity)  # Reduce S by 8–12 in PIL HSV scale (0–255)

    for i, (h, s, v) in enumerate(zip(h_data, s_data, v_data)):
        # Only affect high-luminance pixels (top 15% brightness = V > 216)
        if v > 216 and s > 20:
            # PIL HSV: H in 0–255, S in 0–255, V in 0–255
            # Hue of CORRUPT_AMBER ~25 degrees = ~17-18 in PIL 0–255 space
            # Protect range: ~12–25 in PIL hue space (orange/amber region)
            # PIL hue: 0 = red, 42 = yellow, 85 = green, 128 = cyan, 170 = blue, 213 = magenta
            # Orange/amber range: approximately 8–22 in PIL 0-255 hue
            in_amber_hue_range = (8 <= h <= 25)
            if not in_amber_hue_range:
                s = _clamp(s - desat_amount)
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

    Uses very low alpha (5–10%) as per creative brief — subliminal CRT reference.
    """
    alpha = int(10 * intensity)
    alpha = _clamp(alpha, 3, 25)
    spacing = 4
    return _apply_scanlines(img, spacing=spacing, alpha=alpha)


def _pass_color_separation(img, intensity=1.0, seed=42):
    """Simulate vintage print misregistration — RGB micro-offset at high-contrast edges.

    Shifts R channel slightly right/down and B channel slightly left/up
    by 1–2px. Effect is subliminal on flat areas, visible at high-contrast edges.
    Simulates Risograph-style color registration drift.
    """
    shift = max(1, int(2 * intensity))
    if img.mode != "RGBA":
        img = img.convert("RGBA")

    r, g, b, a = img.split()

    # R channel: shift +shift right, +shift down
    r_shifted = ImageChops.offset(r, shift, shift)
    # B channel: shift -shift left, -shift up
    b_shifted = ImageChops.offset(b, -shift, -shift)
    # G channel: no shift (anchor)

    result = Image.merge("RGBA", (r_shifted, g, b_shifted, a))
    return result


def _pass_edge_sharpen(img, intensity=1.0):
    """Sharpen hard geometry edges for Glitch Layer content.

    Applies an unsharp mask pass to crisp up platform/void geometry edges.
    Counter-intuitive vs Real World treatment — Glitch Layer edges are defined
    and geometric, not organic.
    """
    if img.mode != "RGBA":
        img = img.convert("RGBA")

    # Unsharp mask: sharpen edges with controlled radius and percent
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
    """Create a gradient mask for blending two treatments vertically.

    Returns RGBA image. Alpha = 0 (fully realworld) below blend_start,
    Alpha = 255 (fully glitch) above blend_end, gradient in between.
    Used to composite glitch-treated upper portion over realworld-treated lower.
    """
    mask = Image.new("L", (width, height), 0)
    pixels = []
    for y in range(height):
        if y <= blend_start:
            v = 255  # above blend zone = glitch
        elif y >= blend_end:
            v = 0    # below blend zone = realworld
        else:
            # Gradient: fade from glitch (top) to realworld (bottom)
            t = (y - blend_start) / (blend_end - blend_start)
            v = int(255 * (1.0 - t))
        pixels.append(v)

    # Expand to full width
    full_pixels = []
    for v in pixels:
        full_pixels.extend([v] * width)
    mask.putdata(full_pixels)
    return mask


# ---------------------------------------------------------------------------
# Main stylization passes
# ---------------------------------------------------------------------------

def _apply_realworld_treatment(img, intensity=1.0, seed=42):
    """Apply full Real World hand-drawn treatment.

    Pass order (per Alex Chen's creative brief):
      1. Paper/canvas grain
      2. Line wobble/jitter
      3. Warm color bleed at edges
      4. Chalk/gouache highlight desaturation
    """
    if img.mode != "RGBA":
        img = img.convert("RGBA")

    # Pass 1: Paper grain
    img = _pass_paper_grain(img, intensity=intensity, seed=seed)

    # Pass 2: Line wobble
    img = _pass_line_wobble(img, amplitude=2, intensity=intensity * 0.8, seed=seed)

    # Pass 3: Warm color bleed
    img = _pass_color_bleed(img, radius=3, intensity=intensity, seed=seed)

    # Pass 4: Chalk highlights
    img = _pass_chalk_highlights(img, intensity=intensity, seed=seed)

    return img


def _apply_glitch_treatment(img, intensity=1.0, seed=42):
    """Apply full Glitch Layer stylization treatment.

    Pass order (per Alex Chen's creative brief):
      1. Scanline texture (CRT reference)
      2. RGB color separation (print misregistration)
      3. Edge sharpening (geometry crispness)
      Note: NO paper grain
    """
    if img.mode != "RGBA":
        img = img.convert("RGBA")

    # Pass 1: Scanlines
    img = _pass_scanlines_glitch(img, intensity=intensity)

    # Pass 2: Color separation
    img = _pass_color_separation(img, intensity=intensity, seed=seed)

    # Pass 3: Edge sharpening
    img = _pass_edge_sharpen(img, intensity=intensity)

    return img


def _apply_mixed_treatment(img, intensity=1.0, seed=42):
    """Apply zone-blended mixed treatment for SF02 (Glitch Storm / boundary event).

    Zone split:
      - Lower third (Luma, Cosmo, street level): Real World treatment
      - Upper two-thirds (storm sky, Glitch cloud masses): Glitch Layer treatment
      - ~200px vertical gradient blend zone at the boundary (per brief)
    """
    w, h = img.size
    if img.mode != "RGBA":
        img = img.convert("RGBA")

    # Zone boundaries: lower third starts at h * 2/3
    zone_boundary = int(h * (2.0 / 3.0))  # Y where boundary sits
    blend_half = 100  # 200px total blend zone

    blend_start = max(0, zone_boundary - blend_half)  # top of blend zone
    blend_end = min(h - 1, zone_boundary + blend_half)  # bottom of blend zone

    # Apply both treatments to the full image
    realworld_version = _apply_realworld_treatment(img.copy(), intensity=intensity, seed=seed)
    glitch_version = _apply_glitch_treatment(img.copy(), intensity=intensity, seed=seed)

    # Build vertical gradient mask
    # Above blend_start = glitch (mask alpha = 255)
    # Below blend_end   = realworld (mask alpha = 0)
    grad_mask = _make_vertical_gradient_mask(w, h, blend_start, blend_end)

    # Composite: start with realworld base, paste glitch on top using gradient mask
    result = realworld_version.copy()
    # Use the gradient mask as alpha for the glitch layer
    glitch_rgba = glitch_version.copy()
    r, g, b, a = glitch_rgba.split()
    # Multiply existing alpha by gradient mask
    new_a = ImageChops.multiply(a, grad_mask)
    glitch_masked = Image.merge("RGBA", (r, g, b, new_a))

    result.alpha_composite(glitch_masked)
    return result


# ---------------------------------------------------------------------------
# Public API — main stylize function
# ---------------------------------------------------------------------------

def stylize(
    input_path: str,
    output_path: str,
    mode: str = "realworld",    # "realworld" | "glitch" | "mixed"
    intensity: float = 1.0,     # 0.0–2.0 global intensity multiplier
    seed: int = 42,             # seeded for reproducibility
) -> None:
    """Apply hand-drawn stylization treatment to a PNG image.

    Args:
        input_path  (str): Path to source PNG file.
        output_path (str): Path for output stylized PNG.
        mode        (str): Treatment mode:
                           "realworld" — paper grain, line wobble, warm bleed, chalk highlights
                           "glitch"    — scanlines, color separation, edge sharpening
                           "mixed"     — zone-blended (glitch upper 2/3, realworld lower 1/3)
        intensity   (float): Global intensity multiplier. 0.0 = no effect, 1.0 = standard,
                           2.0 = maximum. Scales all effect alphas proportionally.
        seed        (int): RNG seed. Identical seed + input produces identical output.

    Returns:
        None. Writes PNG to output_path at same dimensions as input.

    Raises:
        FileNotFoundError: If input_path does not exist.
        ValueError: If mode is not one of "realworld", "glitch", "mixed".
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    valid_modes = ("realworld", "glitch", "mixed")
    if mode not in valid_modes:
        raise ValueError(f"Invalid mode '{mode}'. Must be one of: {valid_modes}")

    intensity = max(0.0, min(2.0, float(intensity)))

    print(f"[LTG_TOOL_stylize_handdrawn_v001] Loading: {input_path}")
    img = Image.open(input_path)

    # Ensure RGBA for consistent alpha compositing throughout
    if img.mode != "RGBA":
        img = img.convert("RGBA")

    print(f"  Image size: {img.width}x{img.height}, mode: {mode}, intensity: {intensity}, seed: {seed}")

    if mode == "realworld":
        result = _apply_realworld_treatment(img, intensity=intensity, seed=seed)
    elif mode == "glitch":
        result = _apply_glitch_treatment(img, intensity=intensity, seed=seed)
    elif mode == "mixed":
        result = _apply_mixed_treatment(img, intensity=intensity, seed=seed)

    # Ensure output directory exists
    out_dir = os.path.dirname(output_path)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    # Save as RGBA PNG
    result.save(output_path, "PNG")
    print(f"  Saved: {output_path}")


# Legacy alias for backward compatibility
def stylize_handdrawn(input_path: str, output_path: str, intensity: float = 1.0) -> None:
    """Backward-compatible wrapper. Defaults to 'realworld' mode, seed=42."""
    stylize(input_path, output_path, mode="realworld", intensity=intensity, seed=42)


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def _cli():
    parser = argparse.ArgumentParser(
        description="LTG Hand-Drawn Stylization Tool v001 — Luma & the Glitchkin"
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
