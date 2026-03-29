#!/usr/bin/env python3
"""
LTG_TOOL_luma_turnaround_v002.py
Luma 4-View Character Turnaround v002 — C32 STUB FIX

Original: LTG_CHAR_luma_turnaround_v002.py (Cycle 25/26 — Maya Santos)
Status: Original deleted by C29 naming cleanup. Superseded by v003 (canonical).

C32 FIX (Kai Nakamura): The original LTG_CHAR_ source was deleted by
LTG_TOOL_naming_cleanup_v001.py. v003 is the canonical turnaround with
corrected line weights (head=4, structure=3, detail=2 at 2× render) and
confirmed 3.2-head proportions. This stub delegates to v003's build_turnaround().

Output: LTG_CHAR_luma_turnaround_v002.png
"""

import os
import sys
from PIL import Image

_TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _TOOLS_DIR)

# Delegate to canonical v003 (supersedes v002)
import LTG_TOOL_luma_turnaround_v003 as _canonical


def build_turnaround():
    """Return the turnaround image (delegates to v003)."""
    return _canonical.build_turnaround()


def main():
    """Generate v002 output via v003 delegate (v002 is superseded — v003 is canonical)."""
    out_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "characters", "main", "turnarounds"
    )
    os.makedirs(out_dir, exist_ok=True)
    output_path = os.path.join(out_dir, "LTG_CHAR_luma_turnaround_v002.png")
    img = _canonical.build_turnaround()
    img.thumbnail((1280, 1280), Image.LANCZOS)
    img.save(output_path)
    print(f"Saved: {os.path.abspath(output_path)}")
    print("v002 stub: delegated to v003 canonical (original deleted C29, superseded by v003)")


if __name__ == "__main__":
    main()
