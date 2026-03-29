#!/usr/bin/env python3
"""
LTG_TOOL_luma_expression_sheet_v005.py
Luma Expression Sheet v005 — C32 STUB FIX

Original: LTG_CHAR_luma_expression_sheet_v005.py (Cycle 25/26 — Maya Santos)
Status: Original deleted by C29 naming cleanup. Superseded by v007 (canonical).

C32 FIX (Kai Nakamura): The original LTG_CHAR_ source was deleted by
LTG_TOOL_naming_cleanup_v001.py. Since v007 supersedes v005 and incorporates
all v005 improvements (body-language differentiation, 3-tier line weight,
classroom-style head/hair/eyes), this stub now delegates to v007's build_sheet().

Output: LTG_CHAR_luma_expression_sheet_v005.png
"""

import os
import sys
from PIL import Image

_TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _TOOLS_DIR)

# Delegate to canonical v007 (supersedes v005)
import LTG_TOOL_luma_expression_sheet_v007 as _canonical


def build_sheet(show_guides=False):
    """Return the expression sheet image (delegates to v007)."""
    return _canonical.build_sheet(show_guides=show_guides)


def main():
    """Generate v005 output via v007 delegate (v005 is superseded — v007 is canonical)."""
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "..", "characters", "main")
    os.makedirs(out_dir, exist_ok=True)
    output_path = os.path.join(out_dir, "LTG_CHAR_luma_expression_sheet_v005.png")
    sheet = _canonical.build_sheet(show_guides=False)
    sheet.thumbnail((1280, 1280), Image.LANCZOS)
    sheet.save(output_path)
    print(f"Saved: {os.path.abspath(output_path)}")
    print("v005 stub: delegated to v007 canonical (original deleted C29, superseded by v007)")


if __name__ == "__main__":
    main()
