#!/usr/bin/env python3
"""
LTG_TOOL_naming_cleanup.py
================================
Removes the original LTG_CHAR_/LTG_COLOR_/LTG_BRAND_ .py files from output/tools/
now that their canonical LTG_TOOL_ copies exist.

Created by: Kai Nakamura, Cycle 29
Purpose: Complete the naming compliance pass started in C28.

Usage:
    python LTG_TOOL_naming_cleanup.py [--dry-run]

Options:
    --dry-run   Print what would be removed without actually removing anything.

Exemptions:
    - output/tools/legacy/  (all files exempt)
    - Any file that does NOT have a corresponding LTG_TOOL_ version on disk

Rules enforced:
    - Python generator .py files in output/tools/ must use LTG_TOOL_ prefix
    - Output PNGs keep their content-category prefix (LTG_CHAR_, LTG_COLOR_, etc.)
    - production/ is exempt; tools/legacy/ is exempt
"""

import os
import sys

TOOLS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))

# Map of non-compliant source files -> expected canonical LTG_TOOL_ name
# Format: (non_compliant_filename, canonical_ltg_tool_filename)
CLEANUP_MAP = [
    # LTG_CHAR_ -> LTG_TOOL_ (expression sheets)
    ("LTG_CHAR_luma_expression_sheet.py",            "LTG_TOOL_luma_expression_sheet.py"),
    ("LTG_CHAR_luma_expression_sheet.py",            "LTG_TOOL_luma_expression_sheet.py"),
    ("LTG_CHAR_luma_expression_sheet.py",            "LTG_TOOL_luma_expression_sheet.py"),
    ("LTG_CHAR_luma_expression_sheet_v005.py",            "LTG_TOOL_luma_expression_sheet.py"),
    ("LTG_CHAR_luma_expression_sheet_v006.py",            "LTG_TOOL_luma_expression_sheet.py"),
    ("LTG_CHAR_luma_turnaround_v002.py",                  "LTG_TOOL_luma_turnaround.py"),
    ("LTG_CHAR_byte_expression_sheet.py",            "LTG_TOOL_byte_expression_sheet.py"),
    ("LTG_CHAR_cosmo_expression_sheet.py",           "LTG_TOOL_cosmo_expression_sheet.py"),
    ("LTG_CHAR_cosmo_turnaround_v002.py",                 "LTG_TOOL_cosmo_turnaround.py"),
    ("LTG_CHAR_grandma_miri_expression_sheet_v003.py",    "LTG_TOOL_grandma_miri_expression_sheet.py"),
    # LTG_CHAR_ -> LTG_TOOL_ (glitch generators)
    ("LTG_CHAR_glitch_expression_sheet_v001.py",          "LTG_TOOL_glitch_expression_sheet.py"),
    ("LTG_CHAR_glitch_expression_sheet_v002.py",          "LTG_TOOL_glitch_expression_sheet.py"),
    ("LTG_CHAR_glitch_turnaround_v001.py",                "LTG_TOOL_glitch_turnaround.py"),
    ("LTG_CHAR_glitch_turnaround_v002.py",                "LTG_TOOL_glitch_turnaround.py"),
    ("LTG_CHAR_glitch_color_model_v001.py",               "LTG_TOOL_glitch_color_model.py"),
    # LTG_COLOR_ -> LTG_TOOL_ (color models)
    ("LTG_COLOR_luma_color_model_v001.py",                "LTG_TOOL_luma_color_model.py"),
    ("LTG_COLOR_byte_color_model_v001.py",                "LTG_TOOL_byte_color_model.py"),
    ("LTG_COLOR_cosmo_color_model_v001.py",               "LTG_TOOL_cosmo_color_model.py"),
    # LTG_COLOR_ -> LTG_TOOL_ (style frames)
    ("LTG_COLOR_styleframe_luma_byte_v001.py",            "LTG_TOOL_styleframe_luma_byte.py"),
    ("LTG_COLOR_styleframe_luma_byte_v002.py",            "LTG_TOOL_styleframe_luma_byte.py"),
    ("LTG_COLOR_styleframe_luma_byte_v003.py",            "LTG_TOOL_styleframe_luma_byte.py"),
    # LTG_BRAND_ -> LTG_TOOL_ (logo generators)
    ("LTG_BRAND_logo_v001.py",                            "LTG_TOOL_logo.py"),
]


def main(dry_run=False):
    removed = []
    skipped_no_canonical = []
    skipped_not_found = []

    for non_compliant, canonical in CLEANUP_MAP:
        non_compliant_path = os.path.join(TOOLS_DIR, non_compliant)
        canonical_path = os.path.join(TOOLS_DIR, canonical)

        if not os.path.exists(non_compliant_path):
            skipped_not_found.append(non_compliant)
            continue

        if not os.path.exists(canonical_path):
            skipped_no_canonical.append((non_compliant, canonical))
            print(f"  SKIP (no canonical): {non_compliant} — {canonical} not found; skipping removal")
            continue

        if dry_run:
            print(f"  [DRY RUN] Would remove: {non_compliant}")
        else:
            os.remove(non_compliant_path)
            print(f"  Removed: {non_compliant}")
        removed.append(non_compliant)

    print()
    print(f"Summary:")
    print(f"  Removed (or would remove): {len(removed)}")
    print(f"  Skipped (already gone):    {len(skipped_not_found)}")
    print(f"  Skipped (no canonical):    {len(skipped_no_canonical)}")

    if skipped_no_canonical:
        print()
        print("  Files needing manual LTG_TOOL_ copy before removal:")
        for noncompliant, canonical in skipped_no_canonical:
            print(f"    {noncompliant} -> {canonical}")


if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv
    if dry_run:
        print("=== DRY RUN MODE — no files will be deleted ===")
    print(f"Scanning: {TOOLS_DIR}")
    print()
    main(dry_run=dry_run)
