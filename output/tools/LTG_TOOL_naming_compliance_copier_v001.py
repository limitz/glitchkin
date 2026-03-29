#!/usr/bin/env python3
"""
LTG_TOOL_naming_compliance_copier_v001.py
Tool: Naming Convention Compliance Copier
Cycle: 12
Author: Jordan Reed, Background & Environment Artist
Date: 2026-03-29

Creates LTG-compliant copies of legacy-named production files.
Never overwrites — only creates new files. Existing LTG-compliant copies are skipped.

Usage: python3 LTG_TOOL_naming_compliance_copier_v001.py
"""

import shutil
import os

BASE = "/home/wipkat/team/output"

# Mapping: (source_path, destination_path)
# Only copies that do not already exist will be made.
COMPLIANCE_COPIES = [
    # ── CHARACTER TURNAROUNDS ─────────────────────────────────────────────────
    (
        f"{BASE}/characters/main/turnarounds/luma_turnaround.png",
        f"{BASE}/characters/main/turnarounds/LTG_CHAR_luma_turnaround_v001.png",
    ),
    (
        f"{BASE}/characters/main/turnarounds/byte_turnaround.png",
        f"{BASE}/characters/main/turnarounds/LTG_CHAR_byte_turnaround_v001.png",
    ),
    (
        f"{BASE}/characters/main/turnarounds/cosmo_turnaround.png",
        f"{BASE}/characters/main/turnarounds/LTG_CHAR_cosmo_turnaround_v001.png",
    ),
    (
        f"{BASE}/characters/main/turnarounds/miri_turnaround.png",
        f"{BASE}/characters/main/turnarounds/LTG_CHAR_miri_turnaround_v001.png",
    ),
    # ── STYLE FRAMES (COLOR category) ────────────────────────────────────────
    (
        f"{BASE}/color/style_frames/style_frame_01_rendered.png",
        f"{BASE}/color/style_frames/LTG_COLOR_styleframe_discovery_v001.png",
    ),
    # ── COLOR MODEL SWATCHES (COLOR category) ────────────────────────────────
    (
        f"{BASE}/characters/color_models/swatches/luma_swatches.png",
        f"{BASE}/characters/color_models/swatches/LTG_COLOR_luma_color_model_swatches_v001.png",
    ),
    (
        f"{BASE}/characters/color_models/swatches/byte_swatches.png",
        f"{BASE}/characters/color_models/swatches/LTG_COLOR_byte_color_model_swatches_v001.png",
    ),
    (
        f"{BASE}/characters/color_models/swatches/cosmo_swatches.png",
        f"{BASE}/characters/color_models/swatches/LTG_COLOR_cosmo_color_model_swatches_v001.png",
    ),
    (
        f"{BASE}/characters/color_models/swatches/grandma_miri_swatches.png",
        f"{BASE}/characters/color_models/swatches/LTG_COLOR_grandma_miri_color_model_swatches_v001.png",
    ),
    # ── CHARACTER LINEUP (CHAR category) ─────────────────────────────────────
    (
        f"{BASE}/characters/main/character_lineup.png",
        f"{BASE}/characters/main/LTG_CHAR_character_lineup_v001.png",
    ),
]


def main():
    created = []
    skipped = []
    errors = []

    for src, dst in COMPLIANCE_COPIES:
        if not os.path.exists(src):
            errors.append(f"SOURCE MISSING: {src}")
            continue
        if os.path.exists(dst):
            skipped.append(f"ALREADY EXISTS: {dst}")
            continue
        try:
            shutil.copy2(src, dst)
            created.append(f"CREATED: {dst}")
        except Exception as e:
            errors.append(f"ERROR copying {src} -> {dst}: {e}")

    print("\n=== LTG Naming Compliance Copier — Results ===\n")
    for line in created:
        print(f"  [OK]  {line}")
    for line in skipped:
        print(f"  [--]  {line}")
    for line in errors:
        print(f"  [ERR] {line}")

    print(f"\nSummary: {len(created)} created, {len(skipped)} skipped, {len(errors)} errors.")


if __name__ == "__main__":
    main()
