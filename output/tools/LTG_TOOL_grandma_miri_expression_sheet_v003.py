#!/usr/bin/env python3
"""
LTG_TOOL_grandma_miri_expression_sheet_v003.py
Grandma Miri Expression Sheet v003 — C32 STUB FIX

Original: LTG_CHAR_grandma_miri_expression_sheet_v003.py (Cycle 25 — Maya Santos)
Status: Original deleted by C29 naming cleanup. No v003 LTG_TOOL_ generator exists.

C32 FIX (Kai Nakamura): The original LTG_CHAR_ source was deleted by
LTG_TOOL_naming_cleanup_v001.py. v002 is the best available canonical
(ground-up rebuild, full body posture differentiation, 5/5 squint test pass).
This stub delegates to v002's build_sheet() until a proper v003 is authored.

v003 was noted as "narrative expression addition" (Cycle 25) — this content
is not recoverable from existing sources. v002 output is used as a stand-in.

Output: LTG_CHAR_grandma_miri_expression_sheet_v003.png
"""

import os
import sys
from PIL import Image

_TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _TOOLS_DIR)

# Delegate to v002 (best available — v003 original was deleted, no LTG_TOOL_ v003 exists)
import LTG_TOOL_grandma_miri_expression_sheet_v002 as _canonical


def build_sheet():
    """Return the expression sheet image (delegates to v002)."""
    return _canonical.build_sheet()


def main():
    """Generate v003 output via v002 delegate (v003 original deleted C29)."""
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "..", "characters", "main")
    os.makedirs(out_dir, exist_ok=True)
    output_path = os.path.join(out_dir, "LTG_CHAR_grandma_miri_expression_sheet_v003.png")
    sheet = _canonical.build_sheet()
    sheet.thumbnail((1280, 1280), Image.LANCZOS)
    sheet.save(output_path)
    print(f"Saved: {os.path.abspath(output_path)}")
    print("v003 stub: delegated to v002 canonical (v003 original deleted C29 — no v003 LTG_TOOL_ exists)")


if __name__ == "__main__":
    main()
