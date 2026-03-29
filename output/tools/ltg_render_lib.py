#!/usr/bin/env python3
"""
ltg_render_lib.py — Shared Rendering Utility Library
"Luma & the Glitchkin" — Technical Art / Kai Nakamura / Cycle 21

Provides reusable procedural rendering functions for all LTG generators.
Import with:
    import sys, os
    sys.path.insert(0, os.path.dirname(__file__))
    from ltg_render_lib import (
        perlin_noise_texture, gaussian_glow, light_shaft,
        dust_motes, catenary_wire, scanline_overlay, vignette
    )

Dependencies: Python standard library, Pillow (PIL). No numpy required.

All procedural functions use seeded RNG for reproducibility.
No circular dependencies — importable standalone.
"""

import math
import random
from PIL import Image, ImageDraw, ImageFilter


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def perlin_noise_texture(width, height, scale=50, seed=42, octaves=3, alpha=60):
    """Generate an RGBA noise texture overlay.

    Uses layered sinusoidal noise (no external deps needed).
    Multiple octaves are blended (each octave doubles frequency, halves amplitude)
    to produce organic-looking value noise without requiring numpy or external libs.

    Args:
        width  (int): Output image width in pixels.
        height (int): Output image height in pixels.
        scale  (int): Base wavelength of the lowest-frequency octave.
        seed   (int): Seed for the phase-offset RNG.
        octaves(int): Number of noise octaves to layer.
        alpha  (int): Maximum alpha value (0–255) of the returned overlay.

    Returns:
        PIL.Image (mode="RGBA"): Grayscale noise mapped to RGBA with the given
        max alpha. Composite over an existing image to add subtle texture.
    """
    rng = random.Random(seed)

    # Generate random phase offsets per octave so octaves don't overlap
    phase_offsets = [(rng.uniform(0, 2 * math.pi), rng.uniform(0, 2 * math.pi))
                     for _ in range(octaves)]

    result = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(result)

    for y in range(height):
        for x in range(width):
            value = 0.0
            amplitude = 1.0
            freq = 1.0
            total_amp = 0.0

            for i in range(octaves):
                px, py = phase_offsets[i]
                nx = (x / scale) * freq + px
                ny = (y / scale) * freq + py
                # Layered sin/cos approximation gives smooth value noise
                v = (math.sin(nx * 2.1 + py) * math.cos(ny * 1.9 + px) +
                     math.cos(nx * 1.7 - px) * math.sin(ny * 2.3 - py)) * 0.5
                value += v * amplitude
                total_amp += amplitude
                amplitude *= 0.5
                freq *= 2.0

            # Normalize to [0, 1]
            value = (value / total_amp) * 0.5 + 0.5
            value = max(0.0, min(1.0, value))
            a = int(value * alpha)
            brightness = int(value * 255)
            draw.point((x, y), fill=(brightness, brightness, brightness, a))

    return result


def gaussian_glow(img, center, radius, color, max_alpha=100, steps=10):
    """Paint a radial glow by compositing concentric ellipses with decreasing alpha.

    Works entirely in RGBA alpha-compositing space — no ImageFilter.GaussianBlur
    required. Each step draws a slightly smaller ellipse with higher alpha,
    producing a smooth falloff from the outer edge inward to the hotspot.

    Args:
        img       (PIL.Image, mode="RGBA"): Image to paint glow onto (modified in place).
        center    (tuple): (cx, cy) centre point of the glow in image coordinates.
        radius    (int): Outer radius of the glow ellipse (circular).
        color     (tuple): RGB color of the glow (e.g. (180, 200, 210)).
        max_alpha (int): Alpha at the glow hotspot (innermost step). Range 0–255.
        steps     (int): Number of concentric ellipses. More = smoother falloff.

    Returns:
        PIL.Image (RGBA): The modified image (same object as input).
    """
    cx, cy = center
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)

    for i in range(steps, 0, -1):
        t = i / steps                         # 1.0 at outermost, 1/steps at center
        r = int(radius * t)
        # Alpha is low at outer edge, higher at center (inverse of t)
        a = int(max_alpha * (1.0 - (t - 1.0 / steps)) * (1.0 / (1.0 - 1.0 / steps + 1e-6)))
        # More intuitive: center gets max_alpha, outermost gets near-zero
        a = int(max_alpha * (1.0 - (i - 1) / steps) ** 2)
        a = max(0, min(255, a))
        ld.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color + (a,))

    img.alpha_composite(layer)
    return img


def light_shaft(img, apex, base_left, base_right, color, max_alpha=60):
    """Draw a light shaft polygon with a Gaussian blur for feathered edges.

    Creates a volumetric light-shaft effect by drawing a filled polygon
    (defined by apex + base_left/right) then applying a GaussianBlur pass
    to soften the hard edges into a natural feathered beam.

    Two passes are composited:
    - Core pass: solid polygon at 60% of max_alpha
    - Feather pass: same polygon blurred with GaussianBlur(radius=16)

    Args:
        img        (PIL.Image, mode="RGBA"): Target image (modified in place).
        apex       (tuple): (x, y) top/narrow point of the light shaft.
        base_left  (tuple): (x, y) bottom-left corner of the shaft base.
        base_right (tuple): (x, y) bottom-right corner of the shaft base.
        color      (tuple): RGB color of the shaft (e.g. SUNLIT_AMBER).
        max_alpha  (int): Peak alpha of the core shaft polygon. Range 0–255.

    Returns:
        PIL.Image (RGBA): The modified image (same object as input).
    """
    shaft_pts = [apex, base_left, base_right]

    # Core pass — solid triangle at ~60% alpha
    core_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    cd = ImageDraw.Draw(core_layer)
    cd.polygon(shaft_pts, fill=color + (int(max_alpha * 0.60),))
    img.alpha_composite(core_layer)

    # Feather pass — blurred polygon for soft edges
    feather_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    fd = ImageDraw.Draw(feather_layer)
    fd.polygon(shaft_pts, fill=color + (int(max_alpha * 0.40),))
    feather_blurred = feather_layer.filter(ImageFilter.GaussianBlur(radius=16))
    img.alpha_composite(feather_blurred)

    return img


def dust_motes(draw, bounds, count=20, seed=42, color=(255, 252, 240), alpha_range=(50, 90)):
    """Scatter small dust particles (circles r=1–4) within bounds (x0, y0, x1, y1).

    Each mote is a small filled circle with a random radius (1–4 pixels) and a
    random alpha within alpha_range. Drawn directly onto the ImageDraw target.

    Note: The draw object must be attached to an RGBA image so per-pixel alpha
    works. If drawing on an RGB image, alpha in fill tuples is silently ignored.

    Args:
        draw        (ImageDraw.Draw): Draw handle on an RGBA image.
        bounds      (tuple): (x0, y0, x1, y1) bounding rectangle for scatter.
        count       (int): Number of dust motes to scatter.
        seed        (int): RNG seed for reproducibility.
        color       (tuple): RGB base color of the motes.
        alpha_range (tuple): (min_alpha, max_alpha) for per-mote alpha variation.
    """
    rng = random.Random(seed)
    x0, y0, x1, y1 = bounds
    a_min, a_max = alpha_range

    for _ in range(count):
        mx = rng.randint(int(x0), int(x1))
        my = rng.randint(int(y0), int(y1))
        r  = rng.randint(1, 4)
        a  = rng.randint(a_min, a_max)
        draw.ellipse([mx - r, my - r, mx + r, my + r], fill=color + (a,))


def catenary_wire(draw, p0, p1, sag=0.05, color=(40, 35, 30), width=2):
    """Draw a wire with catenary sag as a polyline of N=40 segments.

    Approximates the natural droop of a hanging cable using a parabolic
    catenary curve. The sag parameter controls how much the midpoint drops
    relative to the horizontal distance between the two endpoints.

    Args:
        draw  (ImageDraw.Draw): Draw handle to render onto.
        p0    (tuple): (x, y) start point.
        p1    (tuple): (x, y) end point.
        sag   (float): Fraction of horizontal distance to sag downward at midpoint.
                       Typical values: 0.03 (tight) – 0.12 (loose).
        color (tuple): RGB wire color.
        width (int): Line width in pixels.
    """
    N = 40
    x0, y0 = p0
    x1, y1 = p1
    dx = x1 - x0
    dy = y1 - y0
    sag_amount = abs(dx) * sag  # pixels of sag at midpoint

    points = []
    for i in range(N + 1):
        t = i / N
        # Linear interpolation between endpoints
        x = x0 + t * dx
        y = y0 + t * dy
        # Parabolic sag: max at t=0.5, zero at t=0 and t=1
        sag_y = sag_amount * 4 * t * (1 - t)
        points.append((int(x), int(y + sag_y)))

    if len(points) >= 2:
        draw.line(points, fill=color, width=width)


def scanline_overlay(img, spacing=4, alpha=15):
    """Add CRT-style horizontal scanlines. Returns modified img.

    Draws semi-transparent dark horizontal lines at regular intervals across
    the entire image. This simulates the phosphor-row gaps visible on CRT
    displays. The effect is subtle — use alpha <= 20 for a realistic look.

    Args:
        img     (PIL.Image): Source image (RGBA or RGB). Converted to RGBA
                             internally, returned as RGBA.
        spacing (int): Pixel gap between scanline centers (default 4 = every 4th row).
        alpha   (int): Darkness of each scanline. 0=invisible, 255=solid black.
                       Typical range: 10–30.

    Returns:
        PIL.Image (RGBA): The modified image with scanlines composited over it.
    """
    # Ensure we work in RGBA
    if img.mode != "RGBA":
        img = img.convert("RGBA")

    # Build a scanline overlay at full image size
    scan_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(scan_layer)

    for y in range(0, img.height, spacing):
        sd.line([(0, y), (img.width - 1, y)], fill=(0, 0, 0, alpha), width=1)

    img.alpha_composite(scan_layer)
    return img


def vignette(img, strength=60):
    """Darken image edges with a radial gradient vignette. Returns modified img.

    Draws a series of concentric ellipses from the image boundary inward,
    each with decreasing alpha and black fill. The result is a smooth darkening
    toward the corners and edges, focusing the viewer's eye on the center.

    Args:
        img      (PIL.Image): Source image (RGBA or RGB). Converted to RGBA internally.
        strength (int): Maximum alpha at the very edge. 0=no effect, 255=solid black rim.
                        Typical range: 40–100.

    Returns:
        PIL.Image (RGBA): The modified image with vignette composited over it.
    """
    if img.mode != "RGBA":
        img = img.convert("RGBA")

    w, h = img.size
    cx, cy = w // 2, h // 2

    vig_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    vd = ImageDraw.Draw(vig_layer)

    steps = 24
    for i in range(steps):
        # t: 0 = outermost ring, 1 = full inward extent
        t = i / steps
        # Alpha falls off quadratically from edge to center
        a = int(strength * (1.0 - t) ** 2)
        if a < 1:
            continue
        # Ellipse that shrinks toward center as t increases
        rx = int(cx * (1.0 - t * 0.55))
        ry = int(cy * (1.0 - t * 0.55))
        vd.ellipse([cx - rx, cy - ry, cx + rx, cy + ry],
                   fill=(0, 0, 0, 0),
                   outline=(0, 0, 0, a),
                   width=max(1, int(cx * 0.03)))

    img.alpha_composite(vig_layer)
    return img
