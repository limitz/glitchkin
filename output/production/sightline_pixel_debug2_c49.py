# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""Debug: examine sclera pixel distribution around the left eye in SF01."""
import os
from PIL import Image
import numpy as np
from scipy import ndimage

sf01 = os.path.normpath(os.path.join(os.path.dirname(__file__), "..",
    "color", "style_frames", "LTG_COLOR_styleframe_discovery.png"))
img = Image.open(sf01).convert("RGB")
arr = np.array(img)

# Search box from test
x0, y0, x1, y1 = 291, 313, 531, 553
region = arr[y0:y1, x0:x1]

# Eye white detection (same as sightline_validator)
KNOWN_EYE_WHITES = [(242, 240, 248), (250, 240, 220), (255, 252, 245), (240, 240, 245)]
region_f = region.astype(np.float32)
eye_white_mask = np.zeros((y1 - y0, x1 - x0), dtype=bool)
for ref in KNOWN_EYE_WHITES:
    ref_arr = np.array(ref, dtype=np.float32)
    diff = np.sqrt(np.sum((region_f - ref_arr) ** 2, axis=2))
    eye_white_mask |= (diff <= 40)

value = np.max(region, axis=2)
min_ch = np.min(region, axis=2)
sat = np.where(value > 0, (value.astype(float) - min_ch.astype(float)) / value.astype(float), 0)
eye_white_mask &= (value >= 200)
eye_white_mask &= (sat <= 0.15)

# Dilation + labeling
struct = np.ones((13, 1), dtype=bool)
dilated = ndimage.binary_dilation(eye_white_mask, structure=struct, iterations=1)
labeled, num_labels = ndimage.label(dilated)

# Find which label is the left eye (centered near x=413-291=122, y=427-313=114)
for lbl in range(1, num_labels + 1):
    ey, ex = np.where(labeled == lbl)
    # Get original sclera pixels in this label
    mask_in_label = eye_white_mask & (labeled == lbl)
    sy, sx = np.where(mask_in_label)
    if len(sx) < 20:
        continue
    cx = np.mean(sx) + x0
    cy = np.mean(sy) + y0
    print(f"\nLabel {lbl}: {len(sx)} sclera pixels, center ({cx:.1f}, {cy:.1f})")
    bbox = (sx.min() + x0, sy.min() + y0, sx.max() + x0, sy.max() + y0)
    bbox_cx = (bbox[0] + bbox[2]) / 2
    bbox_cy = (bbox[1] + bbox[3]) / 2
    print(f"  Bbox: {bbox}, bbox center: ({bbox_cx:.1f}, {bbox_cy:.1f})")

    # Show sclera pixel distribution
    left = np.sum((sx + x0) < bbox_cx)
    right = np.sum((sx + x0) >= bbox_cx)
    top = np.sum((sy + y0) < bbox_cy)
    bot = np.sum((sy + y0) >= bbox_cy)
    print(f"  Sclera L/R: {left}/{right}, T/B: {top}/{bot}")
    print(f"  L ratio: {left/len(sx):.3f}, T ratio: {top/len(sx):.3f}")

    # Show all sclera pixel x positions (relative to bbox center)
    x_offsets = (sx + x0) - bbox_cx
    y_offsets = (sy + y0) - bbox_cy
    print(f"  X offset range: [{x_offsets.min():.1f}, {x_offsets.max():.1f}]")
    print(f"  Y offset range: [{y_offsets.min():.1f}, {y_offsets.max():.1f}]")
    print(f"  X offset mean: {x_offsets.mean():.2f}")
    print(f"  Y offset mean: {y_offsets.mean():.2f}")

    # Show actual image values in a small grid around bbox center
    print(f"\n  Grid around ({int(bbox_cx)}, {int(bbox_cy)}) — R,G,B values:")
    for dy in range(-8, 9, 2):
        row = []
        for dx in range(-8, 9, 2):
            px, py = int(bbox_cx) + dx, int(bbox_cy) + dy
            if 0 <= px < 1280 and 0 <= py < 720:
                r, g, b = arr[py, px]
                v = max(r, g, b)
                is_scl = "S" if eye_white_mask[py - y0, px - x0] else "."
                row.append(f"V={v:3d}{is_scl}")
            else:
                row.append("     ?")
        print(f"    dy={dy:+3d}: " + " ".join(row))
