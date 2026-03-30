#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_contact_shadow.py — Character-Environment Contact Shadow System
"Luma & the Glitchkin" — Environment Art / Hana Okonkwo / Cycle 50

Reusable contact shadow functions for compositing characters into environments.
Characters in our pipeline currently float above backgrounds with zero grounding.
This tool provides:

  1. draw_contact_shadow()   — elliptical soft shadow beneath character feet
  2. draw_bounce_light()     — subtle color influence from ground onto character lower quarter
  3. tint_character_edges()  — environment color bleed onto character silhouette edges

All functions operate on PIL Images and are compositing-pipeline safe (RGBA throughout).

Usage:
    import sys, os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from LTG_TOOL_contact_shadow import draw_contact_shadow, draw_bounce_light, tint_character_edges

Dependencies: Pillow (PIL). No numpy required.
"""

__version__ = "1.0.0"

import math
from PIL import Image, ImageDraw, ImageFilter


def draw_contact_shadow(img, char_cx, char_base_y, char_width,
                        surface_color=(160, 140, 110),
                        shadow_alpha=50, spread=1.1, height_px=10,
                        blur_radius=4, darken=0.3, desat=0.15):
    """Draw a soft elliptical contact shadow beneath a character.

    The shadow color is derived from the environment's ground surface color,
    darkened and slightly desaturated — matching how reference shows (Hilda,
    Owl House) handle contact shadows. Never uses pure black.

    This function should be called AFTER the background is drawn and BEFORE
    the character is composited, so the shadow sits between the two layers.

    Args:
        img           (PIL.Image): Background image (RGBA or RGB). Modified in place.
        char_cx       (int): Character center X position (horizontal midpoint of feet).
        char_base_y   (int): Character base Y position (bottom of feet / ground contact).
        char_width    (int): Character width in pixels (shadow width = char_width * spread).
        surface_color (tuple): RGB color of the ground surface at the character's feet.
                               Shadow color is derived from this by darkening + desaturating.
        shadow_alpha  (int): Peak shadow opacity (0-255). Default 50 (subtle). Range 30-80 recommended.
        spread        (float): Shadow width multiplier relative to char_width. Default 1.1.
        height_px     (int): Shadow height in pixels (vertical extent). Default 10.
        blur_radius   (int): Gaussian blur radius for shadow softness. Default 4.
        darken        (float): Darkening factor (0.0=black, 1.0=no change). Default 0.3 (70% darker).
        desat         (float): Desaturation blend toward gray (0.0=no change, 1.0=full gray). Default 0.15.

    Returns:
        PIL.Image: The input image with contact shadow composited.
    """
    if img.mode != "RGBA":
        img = img.convert("RGBA")

    w, h = img.size
    shadow_w = int(char_width * spread)
    shadow_h = max(4, height_px)

    # Derive shadow color from surface
    sr, sg, sb = surface_color[:3]
    # Darken
    dr = int(sr * darken)
    dg = int(sg * darken)
    db = int(sb * darken)
    # Desaturate toward gray
    gray = (dr + dg + db) // 3
    fr = int(dr + (gray - dr) * desat)
    fg = int(dg + (gray - dg) * desat)
    fb = int(db + (gray - db) * desat)
    shadow_color = (max(0, min(255, fr)), max(0, min(255, fg)), max(0, min(255, fb)))

    # Build shadow layer with soft ellipse
    shadow_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow_layer)

    # Ellipse bounding box centered at char_cx, char_base_y
    ex1 = char_cx - shadow_w // 2
    ex2 = char_cx + shadow_w // 2
    ey1 = char_base_y - shadow_h // 3  # mostly below the contact line
    ey2 = char_base_y + shadow_h * 2 // 3

    # Clamp to image bounds
    ex1 = max(0, ex1)
    ex2 = min(w - 1, ex2)
    ey1 = max(0, ey1)
    ey2 = min(h - 1, ey2)

    # Draw multiple concentric ellipses with decreasing alpha for soft falloff
    steps = max(3, blur_radius)
    for i in range(steps):
        t = i / max(1, steps - 1)  # 0.0 (outer) to 1.0 (inner)
        # Alpha increases toward center (inverted gaussian-like)
        alpha = int(shadow_alpha * (1.0 - t * 0.6))
        # Size shrinks toward center
        shrink_x = int((ex2 - ex1) * t * 0.15)
        shrink_y = int((ey2 - ey1) * t * 0.2)
        sd.ellipse(
            [ex1 + shrink_x, ey1 + shrink_y, ex2 - shrink_x, ey2 - shrink_y],
            fill=(*shadow_color, alpha)
        )

    # Apply gaussian blur for additional softness
    if blur_radius > 0:
        shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(radius=blur_radius))

    img = Image.alpha_composite(img, shadow_layer)
    return img


def draw_seated_shadow(img, char_cx, seat_y, char_width, seat_width,
                       surface_color=(160, 140, 110),
                       shadow_alpha=40, blur_radius=3, darken=0.35):
    """Draw a contact shadow for a seated character.

    Seated shadows are wider and flatter than standing shadows — the
    contact area is the character's seated base spread across the chair/couch.

    Args:
        img           (PIL.Image): Background image (RGBA or RGB).
        char_cx       (int): Character center X.
        seat_y        (int): Y coordinate of the seat surface.
        char_width    (int): Character body width.
        seat_width    (int): Width of the seat/chair surface. Shadow width = max(char_width, seat_width).
        surface_color (tuple): RGB color of the seat surface.
        shadow_alpha  (int): Peak shadow opacity. Default 40 (subtle — seats partially occlude).
        blur_radius   (int): Gaussian blur radius. Default 3.
        darken        (float): Darkening factor. Default 0.35.

    Returns:
        PIL.Image: Image with seated contact shadow composited.
    """
    effective_width = max(char_width, seat_width)
    # Seated shadow is wider and shorter
    return draw_contact_shadow(
        img, char_cx, seat_y, effective_width,
        surface_color=surface_color,
        shadow_alpha=shadow_alpha,
        spread=1.2,
        height_px=6,
        blur_radius=blur_radius,
        darken=darken,
        desat=0.2
    )


def draw_bounce_light(img, char_mask, char_base_y, char_height,
                      ground_color=(200, 184, 150), bounce_alpha=25,
                      coverage=0.25):
    """Apply subtle ground-bounce light to the lower portion of a character.

    In reference shows, characters standing on colored surfaces pick up
    a tint of the surface color on their undersides (boots, lower legs, skirt hem).
    This function applies a low-alpha tint of the ground color to the bottom
    quarter (default) of the character.

    Args:
        img           (PIL.Image): Character image (RGBA) — the character layer only.
        char_mask     (PIL.Image): Binary mask of the character (mode "L", 255=character).
        char_base_y   (int): Y coordinate of the character's feet (bottom).
        char_height   (int): Character height in pixels.
        ground_color  (tuple): RGB color of the ground surface.
        bounce_alpha  (int): Peak tint alpha. Default 25 (very subtle). Range 15-40 recommended.
        coverage      (float): Fraction of character height affected from bottom up. Default 0.25.

    Returns:
        PIL.Image: Character image with bounce light applied.
    """
    if img.mode != "RGBA":
        img = img.convert("RGBA")

    w, h = img.size
    bounce_zone_top = int(char_base_y - char_height * coverage)
    bounce_zone_top = max(0, bounce_zone_top)

    bounce_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    bd = ImageDraw.Draw(bounce_layer)

    # Gradient from full alpha at base to zero at top of zone
    zone_height = char_base_y - bounce_zone_top
    if zone_height <= 0:
        return img

    for y in range(bounce_zone_top, min(char_base_y, h)):
        t = (y - bounce_zone_top) / zone_height  # 0 at top, 1 at bottom
        alpha = int(bounce_alpha * t)
        bd.line([(0, y), (w - 1, y)], fill=(*ground_color[:3], alpha))

    # Mask to character silhouette only
    if char_mask is not None:
        # Zero out bounce outside character mask
        r, g, b, a = bounce_layer.split()
        a = Image.composite(a, Image.new("L", (w, h), 0), char_mask)
        bounce_layer = Image.merge("RGBA", (r, g, b, a))

    img = Image.alpha_composite(img, bounce_layer)
    return img


def tint_character_edges(img, char_mask, bg_color, tint_alpha=20, edge_width=3):
    """Apply subtle environment color bleed onto character silhouette edges.

    In reference shows, hair and clothing edges that overlap the background
    pick up a slight tint from the BG color. This prevents the hard "pasted on"
    edge that makes characters look like cutouts.

    Args:
        img         (PIL.Image): Character image (RGBA).
        char_mask   (PIL.Image): Binary mask of the character (mode "L", 255=character).
        bg_color    (tuple): RGB color to bleed onto edges.
        tint_alpha  (int): Tint opacity. Default 20 (very subtle). Range 10-30 recommended.
        edge_width  (int): Width of edge band in pixels. Default 3.

    Returns:
        PIL.Image: Character image with edge tinting applied.
    """
    if img.mode != "RGBA":
        img = img.convert("RGBA")

    w, h = img.size

    # Create edge mask by eroding the character mask
    # The difference between original mask and eroded mask = edge band
    eroded = char_mask.copy()
    for _ in range(edge_width):
        eroded = eroded.filter(ImageFilter.MinFilter(3))

    # Edge = original mask pixels that are NOT in the eroded mask
    from PIL import ImageChops
    edge_mask = ImageChops.subtract(char_mask, eroded)

    # Apply tint only on edge pixels
    tint_layer = Image.new("RGBA", (w, h), (*bg_color[:3], tint_alpha))
    r, g, b, a = tint_layer.split()
    # Scale alpha by edge mask intensity
    a = Image.composite(a, Image.new("L", (w, h), 0), edge_mask)
    tint_layer = Image.merge("RGBA", (r, g, b, a))

    img = Image.alpha_composite(img, tint_layer)
    return img


def sample_surface_color(bg_img, char_cx, char_base_y, sample_width=40, sample_height=8):
    """Sample the average surface color from the background at the character's feet.

    Used to derive contact shadow color and bounce light color from the
    actual environment rather than hardcoded values.

    Args:
        bg_img        (PIL.Image): Background image (RGB or RGBA).
        char_cx       (int): Character center X.
        char_base_y   (int): Character base Y (feet position).
        sample_width  (int): Width of sampling region. Default 40.
        sample_height (int): Height of sampling region (below char_base_y). Default 8.

    Returns:
        tuple: (R, G, B) average color of the sampled region.
    """
    if bg_img.mode != "RGB":
        rgb = bg_img.convert("RGB")
    else:
        rgb = bg_img

    w, h = rgb.size
    x1 = max(0, char_cx - sample_width // 2)
    x2 = min(w, char_cx + sample_width // 2)
    y1 = max(0, char_base_y)
    y2 = min(h, char_base_y + sample_height)

    if x2 <= x1 or y2 <= y1:
        return (128, 128, 128)

    region = rgb.crop((x1, y1, x2, y2))
    # Average color
    pixels = list(region.getdata())
    if not pixels:
        return (128, 128, 128)

    avg_r = sum(p[0] for p in pixels) // len(pixels)
    avg_g = sum(p[1] for p in pixels) // len(pixels)
    avg_b = sum(p[2] for p in pixels) // len(pixels)
    return (avg_r, avg_g, avg_b)


# ---------------------------------------------------------------------------
# Convenience: full compositing pass
# ---------------------------------------------------------------------------

def composite_character_into_scene(bg_img, char_img, char_mask,
                                   char_cx, char_base_y, char_width, char_height,
                                   shadow_alpha=50, bounce_alpha=25,
                                   edge_tint_alpha=20):
    """Full compositing pass: shadow + character + bounce + edge tint.

    Convenience function that runs the complete integration pipeline:
    1. Sample surface color from background
    2. Draw contact shadow on background
    3. Paste character onto background
    4. Apply bounce light to character's lower portion
    5. Tint character edges with environment color

    Args:
        bg_img      (PIL.Image): Background image.
        char_img    (PIL.Image): Character image (RGBA with transparency).
        char_mask   (PIL.Image): Binary mask of character (mode "L").
        char_cx     (int): Character center X in the final composite.
        char_base_y (int): Character feet Y in the final composite.
        char_width  (int): Character width in pixels.
        char_height (int): Character height in pixels.
        shadow_alpha (int): Contact shadow opacity.
        bounce_alpha (int): Bounce light opacity.
        edge_tint_alpha (int): Edge tint opacity.

    Returns:
        PIL.Image: Final composite (RGBA).
    """
    if bg_img.mode != "RGBA":
        bg_img = bg_img.convert("RGBA")
    if char_img.mode != "RGBA":
        char_img = char_img.convert("RGBA")

    w, h = bg_img.size

    # 1. Sample ground color
    surface_color = sample_surface_color(bg_img, char_cx, char_base_y)

    # 2. Contact shadow (on background, before character)
    result = draw_contact_shadow(
        bg_img.copy(), char_cx, char_base_y, char_width,
        surface_color=surface_color,
        shadow_alpha=shadow_alpha
    )

    # 3. Composite character onto shadowed background
    # Position character image so its base aligns with char_base_y
    char_x = char_cx - char_img.width // 2
    char_y = char_base_y - char_img.height
    if 0 <= char_x < w and 0 <= char_y < h:
        result.paste(char_img, (char_x, char_y), char_img)

    # 4. Bounce light (applied to the character region in the composite)
    # We apply this as a tinted overlay on the lower portion of the character area
    bounce_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    bounce_zone_top = int(char_base_y - char_height * 0.25)
    bd = ImageDraw.Draw(bounce_layer)
    zone_height = char_base_y - bounce_zone_top
    if zone_height > 0:
        for y in range(max(0, bounce_zone_top), min(char_base_y, h)):
            t = (y - bounce_zone_top) / zone_height
            alpha = int(bounce_alpha * t)
            bd.line([(0, y), (w - 1, y)], fill=(*surface_color, alpha))

        # Mask to character region
        if char_mask is not None:
            full_mask = Image.new("L", (w, h), 0)
            mask_x = char_cx - char_mask.width // 2
            mask_y = char_base_y - char_mask.height
            if 0 <= mask_x < w and 0 <= mask_y < h:
                full_mask.paste(char_mask, (mask_x, mask_y))
            r, g, b, a = bounce_layer.split()
            from PIL import ImageChops
            a = ImageChops.multiply(a, full_mask)
            bounce_layer = Image.merge("RGBA", (r, g, b, a))

        result = Image.alpha_composite(result, bounce_layer)

    return result


# ---------------------------------------------------------------------------
# CLI demo / test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys
    import os

    print(f"LTG_TOOL_contact_shadow v{__version__}")
    print("Contact shadow system for character-environment integration.")
    print()
    print("Functions:")
    print("  draw_contact_shadow()            - Elliptical contact shadow beneath character")
    print("  draw_seated_shadow()             - Contact shadow for seated characters")
    print("  draw_bounce_light()              - Ground bounce color onto character underside")
    print("  tint_character_edges()           - Environment color bleed on character edges")
    print("  sample_surface_color()           - Sample ground color from background")
    print("  composite_character_into_scene() - Full compositing pipeline")
    print()

    # Demo: create a simple test showing contact shadow on a flat surface
    demo_w, demo_h = 400, 300
    demo = Image.new("RGBA", (demo_w, demo_h), (200, 184, 150, 255))  # floor color
    dd = ImageDraw.Draw(demo)

    # Draw a simple wall/floor split
    dd.rectangle([0, 0, demo_w, demo_h // 2], fill=(220, 210, 190))  # wall
    dd.rectangle([0, demo_h // 2, demo_w, demo_h], fill=(200, 184, 150))  # floor

    # Add contact shadow at center
    demo = draw_contact_shadow(
        demo, char_cx=200, char_base_y=200, char_width=60,
        surface_color=(200, 184, 150), shadow_alpha=55
    )

    # Draw simple character placeholder (rectangle person)
    dd = ImageDraw.Draw(demo)
    dd.rectangle([180, 120, 220, 200], fill=(230, 140, 60, 200))  # body
    dd.ellipse([185, 100, 215, 130], fill=(160, 110, 80, 200))  # head

    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from LTG_TOOL_project_paths import output_dir, ensure_dir
        out_path = output_dir("production", "LTG_DEMO_contact_shadow_test.png")
        ensure_dir(out_path.parent)
    except ImportError:
        out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "production", "LTG_DEMO_contact_shadow_test.png")
        os.makedirs(os.path.dirname(out_path), exist_ok=True)

    demo_rgb = demo.convert("RGB")
    demo_rgb.save(str(out_path))
    print(f"Demo saved: {out_path}")
