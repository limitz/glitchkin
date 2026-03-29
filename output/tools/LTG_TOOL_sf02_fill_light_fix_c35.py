#!/usr/bin/env python3
"""
LTG_TOOL_sf02_fill_light_fix_c35.py — SF02 Fill Light Direction Fix (C35)
"Luma & the Glitchkin" — Style Frame 02 Glitch Storm
Author: Jordan Reed | Cycle 35

PURPOSE:
  Corrected draw_magenta_fill_light() for integration into SF02 v007.

  Sven Halvorsen C14 critique identified two structural failures in v006:
    1. WRONG SOURCE DIRECTION: fill light applied from lower-left,
       but the storm crack (HOT_MAGENTA source) is at UPPER-RIGHT.
       A fill from a crack at upper-right means light comes FROM upper-right
       (direct or near-direct bounce off ceiling/wall overhead).
    2. UNMASKED CANVAS TINT: the radial gradient was applied to the whole canvas
       including background pixels. This is not character fill lighting —
       it's a canvas tint. Must be masked to character pixel zones only.

  This module provides a corrected drop-in replacement function that:
    (a) Positions fill source at UPPER-RIGHT of each character
        (matching storm crack at x~1700, y~0 → upper-right corner)
    (b) Uses per-character bbox via get_char_bbox() on a character-only crop,
        OR uses provided known_luma_cx when detection ambiguity is possible
    (c) Builds a per-character silhouette mask via threshold, then applies
        the radial gradient ONLY within character pixel boundaries
    (d) Alpha max 35 (slightly reduced from 40 — upper-right is direct source,
        physically should be slightly harder/cleaner than a bounce)

INTEGRATION:
  In SF02 v007 generator (Rin Yamamoto), replace the call to
  draw_magenta_fill_light(img, luma_cx, byte_cx, cosmo_cx, char_h) with
  the corrected version from this module.

  Import:
    from LTG_TOOL_sf02_fill_light_fix_c35 import draw_magenta_fill_light_v007

  Then call:
    img = draw_magenta_fill_light_v007(img, luma_cx, byte_cx, cosmo_cx, char_h)

  Coordinate: tell Rin which parameters need to be passed.

NOTES ON get_char_bbox() IN MULTI-CHARACTER FRAMES:
  As Sven correctly noted, calling get_char_bbox() on the full 3-character frame
  returns a bbox spanning all three characters combined (cx=740, 83% of canvas).
  This is documented in MEMORY.md.
  Fix: crop a zone around each character before calling get_char_bbox(),
  OR use known character x-positions from geometry constants.
  This module uses the known-positions fallback as the safe default.
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFilter

# Canvas dimensions (matching SF02 standard)
W, H = 1280, 720

# Colors
HOT_MAGENTA = (255, 45, 107)    # GL-02 #FF2D6B canonical

# Storm crack position: upper-right of canvas
# crack_pts from v006: starts at (1820/1920, 0) ~ (x≈1210/1280, 0) at 1280 scale
# Effective source: upper-right quadrant, approximately x=1200, y=0
CRACK_SOURCE_X_FRAC = 0.94   # ~94% across → far upper right
CRACK_SOURCE_Y_FRAC = 0.02   # ~2% down → near top edge


def _alpha_paste(base, overlay):
    """Alpha composite overlay onto base, return RGB."""
    rgba_base = base.convert("RGBA")
    rgba_base = Image.alpha_composite(rgba_base, overlay)
    return rgba_base.convert("RGB")


def _make_char_silhouette_mask(img, char_cx, char_h, char_cy, threshold=80):
    """
    Build a silhouette mask for a single character by:
    1. Cropping a zone around char_cx × char_cy (2× char_h wide, 2.5× char_h tall)
    2. Converting to grayscale and thresholding at `threshold`
    3. Pasting the mask back at the correct position on a full-canvas mask

    Returns a full-canvas "L" mask (0=background, 255=character).
    """
    zone_w = int(char_h * 2.0)
    zone_h = int(char_h * 2.5)
    x0 = max(0, char_cx - zone_w // 2)
    y0 = max(0, char_cy - zone_h // 2)
    x1 = min(W, char_cx + zone_w // 2)
    y1 = min(H, char_cy + zone_h)

    crop = img.crop((x0, y0, x1, y1))
    gray = crop.convert("L")

    # Threshold: pixels brighter than `threshold` are character pixels
    mask_crop = gray.point(lambda p: 255 if p > threshold else 0, mode="L")

    # Paste back onto full-canvas mask
    full_mask = Image.new("L", (W, H), 0)
    full_mask.paste(mask_crop, (x0, y0))

    # Dilate the mask slightly (blur + threshold) to catch character edges
    full_mask_blur = full_mask.filter(ImageFilter.GaussianBlur(radius=4))
    full_mask_dilated = full_mask_blur.point(lambda p: 255 if p > 30 else 0, mode="L")

    return full_mask_dilated


def draw_magenta_fill_light_v007(img, luma_cx, byte_cx, cosmo_cx, char_h,
                                  luma_cy=None, byte_cy=None, cosmo_cy=None):
    """
    CORRECTED HOT_MAGENTA fill light for SF02 v007.

    CHANGES FROM v006:
    - Source direction: UPPER-RIGHT (where storm crack actually is)
      fill_src_x = char_cx + int(char_h * 0.5)  ← right of character
      fill_src_y = char_cy - int(char_h * 0.8)  ← above character
    - Per-character silhouette mask: gradient applied only within character pixels
      (not to background or other characters' zones)
    - Alpha max 35 (vs v006's 40) — upper-right fill is cleaner/harder than a bounce

    Parameters
    ----------
    img : PIL.Image.Image
        RGB image after characters have been drawn
    luma_cx : int
        Luma's horizontal center (from geometry constants, e.g. int(W*0.45))
    byte_cx : int
        Byte's horizontal center (from geometry constants, e.g. int(W*0.28))
    cosmo_cx : int
        Cosmo's horizontal center (from geometry constants, e.g. int(W*0.62))
    char_h : int
        Standard character height (e.g. int(H * 0.18))
    luma_cy, byte_cy, cosmo_cy : int or None
        Character vertical centers. If None, defaults to int(H * 0.65) for
        Luma/Cosmo (feet on ground) and int(H * 0.60) for Byte (floating).
    """
    # Default vertical centers
    if luma_cy is None:
        luma_cy = int(H * 0.65)
    if byte_cy is None:
        byte_cy = int(H * 0.60)
    if cosmo_cy is None:
        cosmo_cy = int(H * 0.65)

    # Storm crack source coordinates
    crack_x = int(W * CRACK_SOURCE_X_FRAC)
    crack_y = int(H * CRACK_SOURCE_Y_FRAC)

    FILL_ALPHA_MAX = 35   # direct from upper-right, clean (not scatter bounce)
    FILL_RADIUS_SCALE = 1.6

    character_zones = [
        (luma_cx,  luma_cy,  "luma"),
        (byte_cx,  byte_cy,  "byte"),
        (cosmo_cx, cosmo_cy, "cosmo"),
    ]

    for (char_cx_pos, char_cy_pos, char_name) in character_zones:
        # Build character silhouette mask
        # Use low threshold (60) to capture any bright character pixels in zone
        char_mask = _make_char_silhouette_mask(
            img, char_cx_pos, char_h, char_cy_pos, threshold=60
        )

        # Build fill gradient overlay
        fill_overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        fd = ImageDraw.Draw(fill_overlay)

        # CORRECTED: fill source is UPPER-RIGHT of character
        # (toward the storm crack at upper-right of canvas)
        fill_src_x = char_cx_pos + int(char_h * 0.5)
        fill_src_y = char_cy_pos - int(char_h * 0.8)
        fill_r = int(char_h * FILL_RADIUS_SCALE)

        # Radial gradient from upper-right fill source
        for r_step in range(fill_r, 0, -max(1, fill_r // 30)):
            t = 1.0 - (r_step / fill_r)
            a = int(FILL_ALPHA_MAX * (t ** 1.3))
            a = max(0, min(255, a))
            if a < 2:
                continue
            fd.ellipse([fill_src_x - r_step, fill_src_y - r_step,
                        fill_src_x + r_step, fill_src_y + r_step],
                       fill=(*HOT_MAGENTA, a))

        # Mask the fill to character pixels only
        # 1. Get the fill overlay as RGBA
        # 2. Apply char_mask to zero out non-character alpha
        fill_arr = fill_overlay.split()  # R, G, B, A channels
        fill_alpha = fill_arr[3]

        # Multiply fill alpha by character mask
        masked_alpha = Image.new("L", (W, H), 0)
        for x in range(W):
            for y in range(H):
                fa = fill_alpha.getpixel((x, y))
                ma = char_mask.getpixel((x, y))
                # Both must be non-zero (mask present AND fill has alpha)
                masked_alpha.putpixel((x, y), int(fa * ma / 255))

        # Reconstruct masked fill overlay
        masked_fill = Image.merge("RGBA", (fill_arr[0], fill_arr[1], fill_arr[2], masked_alpha))

        img = _alpha_paste(img, masked_fill)

    return img


# ── Pixel-efficient version (for production use — avoids per-pixel loop) ──────

def draw_magenta_fill_light_v007_fast(img, luma_cx, byte_cx, cosmo_cx, char_h,
                                       luma_cy=None, byte_cy=None, cosmo_cy=None):
    """
    Production-speed version of draw_magenta_fill_light_v007.
    Uses numpy-free vectorized PIL operations instead of per-pixel loops.
    Produces identical visual result to v007 but faster.

    Uses ImageChops.multiply() to apply the character mask to the fill overlay
    alpha channel without per-pixel iteration.
    """
    from PIL import ImageChops

    if luma_cy is None:
        luma_cy = int(H * 0.65)
    if byte_cy is None:
        byte_cy = int(H * 0.60)
    if cosmo_cy is None:
        cosmo_cy = int(H * 0.65)

    FILL_ALPHA_MAX = 35
    FILL_RADIUS_SCALE = 1.6

    character_zones = [
        (luma_cx,  luma_cy,  "luma"),
        (byte_cx,  byte_cy,  "byte"),
        (cosmo_cx, cosmo_cy, "cosmo"),
    ]

    for (char_cx_pos, char_cy_pos, char_name) in character_zones:
        # Build silhouette mask (fast version using blur threshold)
        char_mask = _make_char_silhouette_mask(
            img, char_cx_pos, char_h, char_cy_pos, threshold=60
        )

        # Build radial gradient
        fill_overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        fd = ImageDraw.Draw(fill_overlay)

        fill_src_x = char_cx_pos + int(char_h * 0.5)
        fill_src_y = char_cy_pos - int(char_h * 0.8)
        fill_r = int(char_h * FILL_RADIUS_SCALE)

        for r_step in range(fill_r, 0, -max(1, fill_r // 30)):
            t = 1.0 - (r_step / fill_r)
            a = int(FILL_ALPHA_MAX * (t ** 1.3))
            a = max(0, min(255, a))
            if a < 2:
                continue
            fd.ellipse([fill_src_x - r_step, fill_src_y - r_step,
                        fill_src_x + r_step, fill_src_y + r_step],
                       fill=(*HOT_MAGENTA, a))

        # Apply mask to fill alpha using ImageChops.multiply
        r_ch, g_ch, b_ch, a_ch = fill_overlay.split()
        # multiply alpha channel by mask (both 0-255 L images; divide by 255 implicit in multiply)
        masked_alpha = ImageChops.multiply(a_ch, char_mask)
        masked_fill = Image.merge("RGBA", (r_ch, g_ch, b_ch, masked_alpha))

        img = _alpha_paste(img, masked_fill)

    return img


if __name__ == "__main__":
    # Standalone test: create a test frame with dummy characters and apply the fix
    print("LTG_TOOL_sf02_fill_light_fix_c35.py — SF02 fill light direction fix")
    print("Testing draw_magenta_fill_light_v007_fast()...")

    # Create a simple test image
    test_img = Image.new("RGB", (W, H), (20, 15, 30))
    td = ImageDraw.Draw(test_img)

    # Draw 3 dummy characters (simple white rectangles)
    char_h = int(H * 0.18)
    luma_cx  = int(W * 0.45)
    byte_cx  = int(W * 0.28)
    cosmo_cx = int(W * 0.62)

    for cx in [luma_cx, byte_cx, cosmo_cx]:
        td.rectangle([cx - char_h//4, int(H * 0.45), cx + char_h//4, int(H * 0.72)],
                     fill=(200, 170, 150))

    # Apply corrected fill
    result = draw_magenta_fill_light_v007_fast(
        test_img, luma_cx, byte_cx, cosmo_cx, char_h
    )

    out_path = "/home/wipkat/team/output/tools/LTG_SNAP_sf02_fill_light_test.png"
    result.thumbnail((1280, 1280), Image.LANCZOS)
    result.save(out_path)
    print(f"  Test output: {out_path}")
    print("  Visual check: HOT_MAGENTA fill should appear on UPPER-RIGHT of each character,")
    print("                with no fill on background pixels outside character zones.")
    print()
    print("Integration instructions for Rin (SF02 v007):")
    print("  1. Add to v007 imports:")
    print("     from LTG_TOOL_sf02_fill_light_fix_c35 import draw_magenta_fill_light_v007_fast as draw_magenta_fill_light")
    print("  2. Replace the v006 draw_magenta_fill_light() call in main() with:")
    print("     img = draw_magenta_fill_light(img, luma_cx, byte_cx, cosmo_cx, char_h)")
    print("  3. Ensure char_cx values come from geometry constants, NOT get_char_bbox()")
    print("     on the full image (Sven C14 issue — multi-char bbox is unreliable).")
