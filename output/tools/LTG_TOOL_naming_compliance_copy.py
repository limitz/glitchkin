#!/usr/bin/env python3
"""
LTG_TOOL_naming_compliance_copy.py
Naming Convention Compliance — Create LTG-compliant copies of legacy-named files.
"Luma & the Glitchkin"

Author: Sam Kowalski, Color & Style Artist
Date: 2026-03-29
Cycle 12

Purpose:
  Creates LTG-compliant named copies of color/character output files that were
  produced under the pre-convention naming system. Per the compliance checklist
  (output/production/naming_convention_compliance_checklist.md, Section 8):
    - Do NOT rename existing legacy files in isolation
    - DO create compliant copies of legacy files, noting prior filename

  Files addressed in Cycle 12 (color/ and characters/color_models/ scope):
    LEGACY NAME                              → LTG-COMPLIANT NAME
    color/color_keys/thumbnails/key01_sunny_afternoon.png
      → LTG_COLOR_colorkey_sunny_afternoon.png
    color/color_keys/thumbnails/key02_nighttime_glitch.png
      → LTG_COLOR_colorkey_nighttime_glitch.png
    color/color_keys/thumbnails/key03_glitch_layer_entry.png
      → LTG_COLOR_colorkey_glitchlayer_entry.png
    color/color_keys/thumbnails/key04_quiet_moment.png
      → LTG_COLOR_colorkey_quiet_moment.png
    color/style_frames/style_frame_01_rendered.png
      → LTG_COLOR_styleframe_discovery.png
    characters/color_models/swatches/luma_swatches.png
      → LTG_COL_luma_colormodel.png   (per Priority 2 naming format)
    characters/color_models/swatches/byte_swatches.png
      → LTG_COL_byte_colormodel.png
    characters/color_models/swatches/cosmo_swatches.png
      → LTG_COL_cosmo_colormodel.png
    characters/color_models/swatches/grandma_miri_swatches.png
      → LTG_COL_miri_colormodel.png

  Note: The strictly correct category for color-related files is COLOR (not COL).
  However, the task spec uses LTG_COL_[character]_colormodel_v001.png for color
  model files. Both forms are created for cross-reference convenience.

Usage: python3 LTG_TOOL_naming_compliance_copy.py
"""

import os
import shutil

BASE = "/home/wipkat/team/output"

# (source_path, destination_path)
COPY_MAP = [
    # Color key thumbnails
    (
        f"{BASE}/color/color_keys/thumbnails/key01_sunny_afternoon.png",
        f"{BASE}/color/color_keys/thumbnails/LTG_COLOR_colorkey_sunny_afternoon.png"
    ),
    (
        f"{BASE}/color/color_keys/thumbnails/key02_nighttime_glitch.png",
        f"{BASE}/color/color_keys/thumbnails/LTG_COLOR_colorkey_nighttime_glitch.png"
    ),
    (
        f"{BASE}/color/color_keys/thumbnails/key03_glitch_layer_entry.png",
        f"{BASE}/color/color_keys/thumbnails/LTG_COLOR_colorkey_glitchlayer_entry.png"
    ),
    (
        f"{BASE}/color/color_keys/thumbnails/key04_quiet_moment.png",
        f"{BASE}/color/color_keys/thumbnails/LTG_COLOR_colorkey_quiet_moment.png"
    ),
    # Style frame rendered PNG
    (
        f"{BASE}/color/style_frames/style_frame_01_rendered.png",
        f"{BASE}/color/style_frames/LTG_COLOR_styleframe_discovery.png"
    ),
    # Character color model swatches — LTG_COL_ prefix as per task spec
    (
        f"{BASE}/characters/color_models/swatches/luma_swatches.png",
        f"{BASE}/characters/color_models/swatches/LTG_COL_luma_colormodel.png"
    ),
    (
        f"{BASE}/characters/color_models/swatches/byte_swatches.png",
        f"{BASE}/characters/color_models/swatches/LTG_COL_byte_colormodel.png"
    ),
    (
        f"{BASE}/characters/color_models/swatches/cosmo_swatches.png",
        f"{BASE}/characters/color_models/swatches/LTG_COL_cosmo_colormodel.png"
    ),
    (
        f"{BASE}/characters/color_models/swatches/grandma_miri_swatches.png",
        f"{BASE}/characters/color_models/swatches/LTG_COL_miri_colormodel.png"
    ),
]


def main():
    created = []
    skipped = []
    for src, dst in COPY_MAP:
        if not os.path.exists(src):
            print(f"  MISSING source: {src}")
            skipped.append(src)
            continue
        if os.path.exists(dst):
            print(f"  EXISTS (skip): {os.path.basename(dst)}")
            skipped.append(dst)
            continue
        shutil.copy2(src, dst)
        print(f"  Copied: {os.path.basename(src)}")
        print(f"       → {os.path.basename(dst)}")
        created.append(dst)

    print(f"\nDone. Created {len(created)} compliant copies. Skipped {len(skipped)}.")
    print("\nCompliant files created:")
    for p in created:
        print(f"  {p}")


if __name__ == "__main__":
    main()
