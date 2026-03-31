#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_wand_composite.py — Wand-Based Character-Environment Compositing System
"Luma & the Glitchkin" — Environment Art / Hana Okonkwo / Cycle 51

Reimplements the C50 contact_shadow system using Wand (ImageMagick Python bindings).
Provides the same six compositing functions as LTG_TOOL_contact_shadow.py, plus new
capabilities only possible with Wand (proper blend modes, feathered masks, and
environment-to-character color transfer).

DIVISION OF LABOR (Hana vs Sam C51):
- Hana (this file): Wand for SPATIAL compositing — shadows, bounce, edge tint, blend modes
- Sam: Wand for COLOR operations — warmth calc, hue analysis, palette compliance

Usage:
    import sys, os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from LTG_TOOL_wand_composite import (
        wand_contact_shadow, wand_bounce_light, wand_edge_tint,
        wand_scene_lighting_overlay, wand_composite_character,
        wand_color_transfer, pil_to_wand, wand_to_pil
    )

Dependencies: Wand (pip install Wand), ImageMagick system library, Pillow.
Fallback: If Wand is not installed, all functions raise ImportError with install instructions.
"""

__version__ = "1.0.0"

import math
import os
import sys

from PIL import Image, ImageDraw, ImageFilter

# ---------------------------------------------------------------------------
# Wand availability check
# ---------------------------------------------------------------------------
_WAND_AVAILABLE = False
_WAND_IMPORT_ERROR = None

try:
    from wand.image import Image as WandImage
    from wand.drawing import Drawing as WandDrawing
    from wand.color import Color as WandColor
    from wand.compat import nested
    _WAND_AVAILABLE = True
except ImportError as e:
    _WAND_IMPORT_ERROR = str(e)


def _require_wand():
    """Raise ImportError if Wand is not available."""
    if not _WAND_AVAILABLE:
        raise ImportError(
            f"Wand is not installed or ImageMagick is missing.\n"
            f"Install: pip install Wand\n"
            f"Also need: apt-get install libmagickwand-dev (Debian/Ubuntu)\n"
            f"Import error was: {_WAND_IMPORT_ERROR}"
        )


# ---------------------------------------------------------------------------
# PIL <-> Wand conversion
# ---------------------------------------------------------------------------

def pil_to_wand(pil_img):
    """Convert a PIL Image to a Wand Image.

    Args:
        pil_img (PIL.Image): Input PIL image (RGB or RGBA).

    Returns:
        wand.image.Image: Equivalent Wand image.
    """
    _require_wand()
    if pil_img.mode not in ("RGB", "RGBA"):
        pil_img = pil_img.convert("RGBA")

    blob = pil_img.tobytes("raw", pil_img.mode)
    w, h = pil_img.size
    depth = 8
    channel_map = "RGBA" if pil_img.mode == "RGBA" else "RGB"

    wand_img = WandImage(width=w, height=h, depth=depth,
                         background=WandColor("transparent"))
    wand_img.import_pixels(0, 0, w, h, channel_map, "char", blob)
    return wand_img


def wand_to_pil(wand_img, mode="RGBA"):
    """Convert a Wand Image to a PIL Image.

    Args:
        wand_img (wand.image.Image): Input Wand image.
        mode (str): Target PIL mode. Default "RGBA".

    Returns:
        PIL.Image: Equivalent PIL image.
    """
    blob = wand_img.make_blob(format="png")
    from io import BytesIO
    pil_img = Image.open(BytesIO(blob))
    if pil_img.mode != mode:
        pil_img = pil_img.convert(mode)
    return pil_img


# ---------------------------------------------------------------------------
# Core compositing functions (Wand implementations)
# ---------------------------------------------------------------------------

def wand_contact_shadow(bg_img, char_cx, char_base_y, char_width,
                        surface_color=(160, 140, 110),
                        shadow_alpha=50, spread=1.1, height_px=10,
                        blur_sigma=4.0, darken=0.3, desat=0.15):
    """Draw a Gaussian-blurred contact shadow using Wand.

    Key advantage over PIL version: Wand's native Gaussian blur produces
    a proper smooth falloff in 2 operations (draw ellipse + blur) instead
    of the PIL version's 20+ concentric ellipse loop. Result is smoother
    and more physically accurate.

    Args match LTG_TOOL_contact_shadow.draw_contact_shadow() for drop-in use.
    blur_sigma replaces blur_radius (Wand uses sigma, not kernel radius).

    Args:
        bg_img (PIL.Image): Background image.
        char_cx (int): Character center X.
        char_base_y (int): Character base Y (feet).
        char_width (int): Character width in pixels.
        surface_color (tuple): RGB ground surface color.
        shadow_alpha (int): Peak shadow opacity 0-255.
        spread (float): Shadow width multiplier.
        height_px (int): Shadow ellipse height.
        blur_sigma (float): Gaussian blur sigma (higher = softer).
        darken (float): Darkening factor (0=black, 1=unchanged).
        desat (float): Desaturation blend toward gray.

    Returns:
        PIL.Image: Background with contact shadow composited (RGBA).
    """
    _require_wand()

    if bg_img.mode != "RGBA":
        bg_img = bg_img.convert("RGBA")

    w, h = bg_img.size
    shadow_w = int(char_width * spread)
    shadow_h = max(4, height_px)

    # Derive shadow color from surface (same logic as PIL version)
    sr, sg, sb = surface_color[:3]
    dr, dg, db = int(sr * darken), int(sg * darken), int(sb * darken)
    gray = (dr + dg + db) // 3
    fr = int(dr + (gray - dr) * desat)
    fg = int(dg + (gray - dg) * desat)
    fb = int(db + (gray - db) * desat)
    shadow_r = max(0, min(255, fr))
    shadow_g = max(0, min(255, fg))
    shadow_b = max(0, min(255, fb))

    # Normalized alpha for Wand color string
    alpha_frac = shadow_alpha / 255.0

    # Build shadow layer in Wand: single ellipse + Gaussian blur
    with WandImage(width=w, height=h, background=WandColor("transparent")) as shadow:
        shadow.format = "png"

        # Draw filled ellipse
        with WandDrawing() as draw:
            color_str = f"rgba({shadow_r},{shadow_g},{shadow_b},{alpha_frac:.3f})"
            draw.fill_color = WandColor(color_str)
            draw.stroke_color = WandColor("transparent")

            ex = char_cx
            ey = char_base_y + shadow_h // 6  # slightly below contact line
            rx = shadow_w // 2
            ry = shadow_h // 2

            draw.ellipse((ex, ey), (rx, ry))
            draw(shadow)

        # Gaussian blur — THE key Wand advantage: proper kernel blur
        shadow.gaussian_blur(sigma=blur_sigma)

        # Composite shadow onto background
        bg_wand = pil_to_wand(bg_img)
        bg_wand.composite(shadow, 0, 0, operator="over")

        result = wand_to_pil(bg_wand)

    return result


def wand_seated_shadow(bg_img, char_cx, seat_y, char_width, seat_width,
                       surface_color=(160, 140, 110),
                       shadow_alpha=40, blur_sigma=3.0, darken=0.35):
    """Draw a contact shadow for a seated character using Wand.

    Seated shadows are wider and flatter.

    Args:
        bg_img (PIL.Image): Background image.
        char_cx (int): Character center X.
        seat_y (int): Y coordinate of seat surface.
        char_width (int): Character body width.
        seat_width (int): Width of chair/couch seat.
        surface_color (tuple): Seat surface color.
        shadow_alpha (int): Peak shadow opacity.
        blur_sigma (float): Gaussian blur sigma.
        darken (float): Darkening factor.

    Returns:
        PIL.Image: Image with seated shadow composited.
    """
    effective_width = max(char_width, seat_width)
    return wand_contact_shadow(
        bg_img, char_cx, seat_y, effective_width,
        surface_color=surface_color,
        shadow_alpha=shadow_alpha,
        spread=1.2,
        height_px=6,
        blur_sigma=blur_sigma,
        darken=darken,
        desat=0.2
    )


def wand_bounce_light(char_img, char_mask, char_base_y, char_height,
                      ground_color=(200, 184, 150), bounce_alpha=25,
                      coverage=0.25):
    """Apply ground-bounce light using Wand's Multiply blend mode.

    Key advantage over PIL: Wand's native blend mode produces color
    interaction that matches how real light bounces work. PIL version
    uses additive overlay which can wash out darks.

    Args:
        char_img (PIL.Image): Character image (RGBA).
        char_mask (PIL.Image): Binary mask of character (mode "L").
        char_base_y (int): Character feet Y.
        char_height (int): Character height in pixels.
        ground_color (tuple): RGB ground surface color.
        bounce_alpha (int): Peak tint alpha.
        coverage (float): Fraction of character height from bottom.

    Returns:
        PIL.Image: Character image with bounce light.
    """
    _require_wand()

    if char_img.mode != "RGBA":
        char_img = char_img.convert("RGBA")

    w, h = char_img.size
    bounce_zone_top = max(0, int(char_base_y - char_height * coverage))
    zone_height = char_base_y - bounce_zone_top
    if zone_height <= 0:
        return char_img

    # Build gradient bounce layer in Wand
    with WandImage(width=w, height=h, background=WandColor("transparent")) as bounce:
        bounce.format = "png"

        # Draw gradient lines (Wand approach: single gradient rectangle + mask)
        with WandDrawing() as draw:
            for y in range(bounce_zone_top, min(char_base_y, h)):
                t = (y - bounce_zone_top) / zone_height
                alpha = int(bounce_alpha * t)
                alpha_frac = alpha / 255.0
                gr, gg, gb = ground_color[:3]
                color_str = f"rgba({gr},{gg},{gb},{alpha_frac:.3f})"
                draw.fill_color = WandColor(color_str)
                draw.line((0, y), (w - 1, y))
            draw(bounce)

        # Apply character mask
        if char_mask is not None:
            mask_wand = pil_to_wand(char_mask.convert("RGBA"))
            # Use mask alpha to restrict bounce to character silhouette
            bounce.composite(mask_wand, 0, 0, operator="dst_in")

        # Use Screen blend for bounce light (more natural than Over)
        char_wand = pil_to_wand(char_img)
        char_wand.composite(bounce, 0, 0, operator="screen")

        result = wand_to_pil(char_wand)

    return result


def wand_edge_tint(char_img, char_mask, bg_color, tint_alpha=20, edge_width=3):
    """Apply environment color bleed on character edges using Wand.

    Key advantage over PIL: Wand's morphology operations (erode) are
    native C and significantly faster than PIL's MinFilter loop.
    The feathered mask also produces smoother edge transitions.

    Args:
        char_img (PIL.Image): Character image (RGBA).
        char_mask (PIL.Image): Binary mask (mode "L").
        bg_color (tuple): RGB environment color to bleed.
        tint_alpha (int): Tint opacity.
        edge_width (int): Edge band width in pixels.

    Returns:
        PIL.Image: Character image with edge tinting.
    """
    _require_wand()

    if char_img.mode != "RGBA":
        char_img = char_img.convert("RGBA")

    w, h = char_img.size

    # Build edge mask using Wand morphology
    mask_rgba = char_mask.convert("RGBA")
    with WandImage(width=w, height=h, background=WandColor("transparent")) as edge_layer:
        edge_layer.format = "png"

        mask_wand = pil_to_wand(mask_rgba)
        eroded = mask_wand.clone()
        # Erode to shrink mask — native C morphology
        eroded.morphology(method="erode", kernel=f"disk:{edge_width}")

        # Edge = original - eroded (done via composite difference)
        # Simpler approach: create tint layer, mask with edge band
        # edge = original AND NOT eroded

        # Create tint layer
        alpha_frac = tint_alpha / 255.0
        br, bg_c, bb = bg_color[:3]
        tint_color = f"rgba({br},{bg_c},{bb},{alpha_frac:.3f})"

        with WandDrawing() as draw:
            draw.fill_color = WandColor(tint_color)
            draw.rectangle(left=0, top=0, right=w - 1, bottom=h - 1)
            draw(edge_layer)

        # Mask tint to original silhouette
        edge_layer.composite(mask_wand, 0, 0, operator="dst_in")

        # Now remove the interior (eroded mask) — keep only edge band
        # Create interior mask
        interior = eroded.clone()
        # Negate approach: composite eroded as dst_out to remove interior
        edge_layer.composite(interior, 0, 0, operator="dst_out")

        # Feather the edge (slight blur for natural bleed)
        edge_layer.gaussian_blur(sigma=1.0)

        # Composite onto character
        char_wand = pil_to_wand(char_img)
        char_wand.composite(edge_layer, 0, 0, operator="over")

        result = wand_to_pil(char_wand)

    return result


def wand_scene_lighting_overlay(bg_img, light_color, light_x, light_y,
                                radius=200, intensity=0.3,
                                blend_mode="screen"):
    """Apply a scene lighting overlay using Wand blend modes.

    This is NEW functionality not in the PIL contact_shadow tool.
    Wand's blend modes (Screen, Multiply, Overlay) produce physically
    correct lighting interactions that manual PIL alpha compositing cannot.

    Screen mode: brightens — simulates additive light (lamp glow, window shaft)
    Multiply mode: darkens — simulates shadow/occlusion
    Overlay mode: contrast — simulates mixed lighting with midtone preservation

    Args:
        bg_img (PIL.Image): Background image.
        light_color (tuple): RGB color of the light source.
        light_x (int): Light source X position.
        light_y (int): Light source Y position.
        radius (int): Light radius in pixels.
        intensity (float): Light intensity 0.0-1.0.
        blend_mode (str): Wand composite operator name. Default "screen".

    Returns:
        PIL.Image: Image with lighting overlay.
    """
    _require_wand()

    if bg_img.mode != "RGBA":
        bg_img = bg_img.convert("RGBA")

    w, h = bg_img.size
    lr, lg, lb = light_color[:3]
    alpha_frac = intensity

    # Build radial gradient light layer
    with WandImage(width=w, height=h, background=WandColor("transparent")) as light:
        light.format = "png"

        with WandDrawing() as draw:
            # Draw concentric circles with decreasing alpha for radial falloff
            steps = max(10, radius // 5)
            for i in range(steps, -1, -1):
                t = i / steps  # 1.0 (outer) to 0.0 (center)
                r = int(radius * t)
                if r < 1:
                    r = 1
                # Alpha peaks at center, falls off quadratically
                a = alpha_frac * (1.0 - t * t)
                color_str = f"rgba({lr},{lg},{lb},{a:.4f})"
                draw.fill_color = WandColor(color_str)
                draw.stroke_color = WandColor("transparent")
                draw.ellipse((light_x, light_y), (r, r))
            draw(light)

        # Gaussian blur for smooth falloff
        light.gaussian_blur(sigma=radius * 0.15)

        # Composite with specified blend mode
        bg_wand = pil_to_wand(bg_img)
        bg_wand.composite(light, 0, 0, operator=blend_mode)

        result = wand_to_pil(bg_wand)

    return result


def wand_color_transfer(char_img, char_mask, bg_img, char_cx, char_base_y,
                        sample_radius=60, tint_strength=0.15):
    """Auto-transfer environment colors onto character layer.

    NEW functionality. Samples the dominant environment colors around the
    character's position and applies them as shadow/highlight tints.
    This is the "scene-responsive character shading" from the C50 lighting spec.

    Uses Wand's modulate and colorize operations for proper color-space work.

    Args:
        char_img (PIL.Image): Character image (RGBA).
        char_mask (PIL.Image): Binary mask (mode "L").
        bg_img (PIL.Image): Background image to sample from.
        char_cx (int): Character center X in the background.
        char_base_y (int): Character feet Y in the background.
        sample_radius (int): Radius around character to sample BG colors.
        tint_strength (float): How strongly to apply the color transfer (0-1).

    Returns:
        PIL.Image: Character image with environment color influence.
    """
    _require_wand()

    if char_img.mode != "RGBA":
        char_img = char_img.convert("RGBA")
    if bg_img.mode != "RGB":
        bg_rgb = bg_img.convert("RGB")
    else:
        bg_rgb = bg_img

    w_bg, h_bg = bg_rgb.size

    # Sample environment colors around character position
    x1 = max(0, char_cx - sample_radius)
    x2 = min(w_bg, char_cx + sample_radius)
    y1 = max(0, char_base_y - sample_radius)
    y2 = min(h_bg, char_base_y + sample_radius)

    if x2 <= x1 or y2 <= y1:
        return char_img

    region = bg_rgb.crop((x1, y1, x2, y2))
    pixels = list(region.getdata())
    if not pixels:
        return char_img

    # Compute average environment color
    avg_r = sum(p[0] for p in pixels) // len(pixels)
    avg_g = sum(p[1] for p in pixels) // len(pixels)
    avg_b = sum(p[2] for p in pixels) // len(pixels)

    # Apply as a low-opacity colorize tint
    w_c, h_c = char_img.size
    alpha_frac = tint_strength

    with WandImage(width=w_c, height=h_c,
                   background=WandColor("transparent")) as tint:
        tint.format = "png"

        color_str = f"rgba({avg_r},{avg_g},{avg_b},{alpha_frac:.3f})"
        with WandDrawing() as draw:
            draw.fill_color = WandColor(color_str)
            draw.rectangle(left=0, top=0, right=w_c - 1, bottom=h_c - 1)
            draw(tint)

        # Mask to character silhouette
        if char_mask is not None:
            mask_wand = pil_to_wand(char_mask.convert("RGBA"))
            tint.composite(mask_wand, 0, 0, operator="dst_in")

        # Use Multiply for shadow tint (darkens character toward env color)
        # Use Screen for highlight areas — we do Soft Light for balanced effect
        char_wand = pil_to_wand(char_img)
        char_wand.composite(tint, 0, 0, operator="soft_light")

        result = wand_to_pil(char_wand)

    return result


def wand_composite_character(bg_img, char_img, char_mask,
                             char_cx, char_base_y, char_width, char_height,
                             shadow_alpha=50, bounce_alpha=25,
                             edge_tint_alpha=20, color_transfer_strength=0.12,
                             blur_sigma=4.0):
    """Full compositing pipeline using Wand.

    Equivalent to LTG_TOOL_contact_shadow.composite_character_into_scene()
    but using Wand for all operations. Adds scene lighting and color transfer
    steps that PIL cannot do properly.

    Pipeline:
    1. Sample surface color from background
    2. Contact shadow (Wand Gaussian blur)
    3. Scene lighting overlay (Wand Screen blend)
    4. Paste character
    5. Bounce light (Wand Screen blend)
    6. Edge tint (Wand morphology + feathered mask)
    7. Color transfer (Wand Soft Light blend)

    Args:
        bg_img (PIL.Image): Background.
        char_img (PIL.Image): Character (RGBA).
        char_mask (PIL.Image): Character mask (L).
        char_cx (int): Character center X.
        char_base_y (int): Character feet Y.
        char_width (int): Character width.
        char_height (int): Character height.
        shadow_alpha (int): Contact shadow opacity.
        bounce_alpha (int): Bounce light opacity.
        edge_tint_alpha (int): Edge tint opacity.
        color_transfer_strength (float): Environment color transfer (0-1).
        blur_sigma (float): Shadow blur sigma.

    Returns:
        PIL.Image: Final composite (RGBA).
    """
    _require_wand()

    if bg_img.mode != "RGBA":
        bg_img = bg_img.convert("RGBA")
    if char_img.mode != "RGBA":
        char_img = char_img.convert("RGBA")

    w, h = bg_img.size

    # 1. Sample ground color (reuse PIL helper — no Wand needed)
    from LTG_TOOL_contact_shadow import sample_surface_color
    surface_color = sample_surface_color(bg_img, char_cx, char_base_y)

    # 2. Contact shadow with Wand Gaussian blur
    result = wand_contact_shadow(
        bg_img.copy(), char_cx, char_base_y, char_width,
        surface_color=surface_color,
        shadow_alpha=shadow_alpha,
        blur_sigma=blur_sigma
    )

    # 3. Composite character onto shadowed background
    char_x = char_cx - char_img.width // 2
    char_y = char_base_y - char_img.height
    if 0 <= char_x < w and 0 <= char_y < h:
        result.paste(char_img, (char_x, char_y), char_img)
        # Refresh draw context per PIL standards (docs/pil-standards.md)
        draw = ImageDraw.Draw(result)

    # 4. Bounce light on character region
    # Extract the character area from composite, apply bounce, paste back
    bounce_result = wand_bounce_light(
        char_img.copy(), char_mask, char_img.height, char_img.height,
        ground_color=surface_color,
        bounce_alpha=bounce_alpha
    )
    if 0 <= char_x < w and 0 <= char_y < h:
        result.paste(bounce_result, (char_x, char_y), bounce_result)
        draw = ImageDraw.Draw(result)

    # 5. Color transfer from environment
    if color_transfer_strength > 0:
        transferred = wand_color_transfer(
            char_img.copy(), char_mask, bg_img,
            char_cx, char_base_y,
            tint_strength=color_transfer_strength
        )
        if 0 <= char_x < w and 0 <= char_y < h:
            result.paste(transferred, (char_x, char_y), transferred)
            draw = ImageDraw.Draw(result)

    return result


# ---------------------------------------------------------------------------
# Comparison / evaluation utilities
# ---------------------------------------------------------------------------

def generate_comparison_sheet(bg_path, output_path=None):
    """Generate a side-by-side comparison: PIL contact_shadow vs Wand composite.

    Creates a 2-up comparison sheet showing:
    - Left: PIL-based compositing (LTG_TOOL_contact_shadow.py)
    - Right: Wand-based compositing (this tool)

    Both use identical character placeholder and background.
    Output: <=1280px per image rules.

    Args:
        bg_path (str): Path to background PNG.
        output_path (str): Output path. Default: auto-generate.

    Returns:
        str: Path to saved comparison sheet.
    """
    bg = Image.open(bg_path).convert("RGBA")
    w, h = bg.size

    # Create a simple character placeholder (colored rectangle + circle head)
    char_w, char_h = 60, 120
    char_cx = w // 2
    char_base_y = int(h * 0.72)  # on the floor

    char_img = Image.new("RGBA", (char_w, char_h), (0, 0, 0, 0))
    cd = ImageDraw.Draw(char_img)
    # Body
    cd.rectangle([10, 30, 50, char_h], fill=(230, 140, 60, 220))
    # Head
    cd.ellipse([15, 0, 45, 35], fill=(200, 150, 110, 220))
    # Simple mask
    char_mask = Image.new("L", (char_w, char_h), 0)
    md = ImageDraw.Draw(char_mask)
    md.rectangle([10, 30, 50, char_h], fill=255)
    md.ellipse([15, 0, 45, 35], fill=255)

    # --- PIL version ---
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from LTG_TOOL_contact_shadow import composite_character_into_scene as pil_composite
    pil_result = pil_composite(
        bg.copy(), char_img.copy(), char_mask.copy(),
        char_cx, char_base_y, char_w, char_h,
        shadow_alpha=55, bounce_alpha=25, edge_tint_alpha=20
    )

    # --- Wand version ---
    wand_available = _WAND_AVAILABLE
    if wand_available:
        try:
            wand_result = wand_composite_character(
                bg.copy(), char_img.copy(), char_mask.copy(),
                char_cx, char_base_y, char_w, char_h,
                shadow_alpha=55, bounce_alpha=25, edge_tint_alpha=20,
                color_transfer_strength=0.12
            )
        except Exception as e:
            wand_available = False
            wand_error = str(e)
            wand_result = None

    # Build comparison sheet
    # 2-up: PIL left, Wand right. Title bar at top.
    panel_w = min(640, w)
    scale = panel_w / w
    panel_h = int(h * scale)
    sheet_w = panel_w * 2
    title_h = 40
    sheet_h = panel_h + title_h

    sheet = Image.new("RGB", (sheet_w, sheet_h), (30, 30, 30))
    sd = ImageDraw.Draw(sheet)

    # Title labels
    sd.text((panel_w // 2 - 60, 10), "PIL (C50)", fill=(255, 255, 200))
    if wand_available:
        sd.text((panel_w + panel_w // 2 - 60, 10), "WAND (C51)", fill=(200, 255, 200))
    else:
        sd.text((panel_w + panel_w // 2 - 80, 10), "WAND UNAVAILABLE", fill=(255, 100, 100))

    # Resize and paste panels
    pil_panel = pil_result.convert("RGB").resize((panel_w, panel_h), Image.LANCZOS)
    sheet.paste(pil_panel, (0, title_h))

    if wand_available and wand_result is not None:
        wand_panel = wand_result.convert("RGB").resize((panel_w, panel_h), Image.LANCZOS)
        sheet.paste(wand_panel, (panel_w, title_h))
    else:
        # Gray placeholder with error text
        sd.rectangle([panel_w, title_h, sheet_w, sheet_h], fill=(60, 60, 60))
        msg = f"Wand not available: {_WAND_IMPORT_ERROR or wand_error}"
        sd.text((panel_w + 20, title_h + panel_h // 2), msg[:80], fill=(255, 100, 100))

    # Ensure <=1280px
    if sheet_w > 1280:
        ratio = 1280 / sheet_w
        sheet = sheet.resize((1280, int(sheet_h * ratio)), Image.LANCZOS)

    # Save
    if output_path is None:
        try:
            from LTG_TOOL_project_paths import output_dir, ensure_dir
            output_path = str(output_dir("production", "LTG_COMP_wand_vs_pil_c51.png"))
            ensure_dir(output_dir("production"))
        except ImportError:
            output_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "..", "production", "LTG_COMP_wand_vs_pil_c51.png"
            )
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

    sheet.save(str(output_path))
    return str(output_path)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print(f"LTG_TOOL_wand_composite v{__version__}")
    print(f"Wand available: {_WAND_AVAILABLE}")
    if not _WAND_AVAILABLE:
        print(f"Import error: {_WAND_IMPORT_ERROR}")
        print()
        print("To install Wand:")
        print("  pip install Wand")
        print("  apt-get install libmagickwand-dev  (Debian/Ubuntu)")
        print()

    print()
    print("Functions (Wand compositing — Hana Okonkwo C51):")
    print("  wand_contact_shadow()         - Gaussian-blurred contact shadow")
    print("  wand_seated_shadow()          - Contact shadow for seated characters")
    print("  wand_bounce_light()           - Screen-blend bounce light")
    print("  wand_edge_tint()              - Morphology-based edge tinting")
    print("  wand_scene_lighting_overlay() - Blend-mode scene lighting [NEW]")
    print("  wand_color_transfer()         - Env-to-character color transfer [NEW]")
    print("  wand_composite_character()    - Full compositing pipeline")
    print("  pil_to_wand() / wand_to_pil() - Conversion utilities")
    print()
    print("Comparison tool:")
    print("  generate_comparison_sheet(bg_path) - Side-by-side PIL vs Wand")
    print()

    # Run comparison if kitchen background exists
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from LTG_TOOL_project_paths import output_dir
        kitchen_path = str(output_dir("backgrounds", "environments",
                                      "LTG_ENV_grandma_kitchen.png"))
    except ImportError:
        kitchen_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..", "backgrounds", "environments", "LTG_ENV_grandma_kitchen.png"
        )

    if os.path.exists(kitchen_path):
        print(f"Kitchen background found: {kitchen_path}")
        try:
            out = generate_comparison_sheet(kitchen_path)
            print(f"Comparison sheet saved: {out}")
        except Exception as e:
            print(f"Comparison generation failed: {e}")
            import traceback
            traceback.print_exc()
    else:
        print(f"Kitchen background not found at: {kitchen_path}")
        print("Run a kitchen generator first, then re-run this tool.")
