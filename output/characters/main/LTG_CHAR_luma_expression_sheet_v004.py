#!/usr/bin/env python3
"""
LTG_CHAR_luma_expression_sheet_v004.py
Luma Expression Sheet Generator — "Luma & the Glitchkin"
Cycle 22 production entry point.

This script is the canonical production copy.
Tool source: output/tools/LTG_CHAR_luma_expression_sheet_v004.py

v004 Cycle 22 (Maya Santos): Critique 10 fixes — Victoria Ashford Priority 2.
  Fix 3a — show_guides flag added:
    render_face(expr, w, h, show_guides=True/False)
    build_sheet(show_guides=True/False)
    Exports BOTH:
      LTG_CHAR_luma_expression_sheet_v004_guides.png  (with guides — production ref)
      LTG_CHAR_luma_expression_sheet_v004.png          (clean, no guides — pitch export)
  Fix 3b — CURIOUS expression upgraded from marginal to confident squint-test pass:
    - brow_r_dy: -int(HR*0.24) -> -int(HR*0.34) (stronger right brow raise)
    - l_open: 0.90 -> 1.0, r_open: 0.86 -> 0.94 (wider eye aperture)
    - cy_offset: 0 -> int(HR*0.06) (slight forward lean)
    CURIOUS is Luma's primary mode — must be unmistakable.
# TODO: update import to LTG_TOOL_render_lib_v001 after Kai's rename
"""
import sys
import os

_tool_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "../../tools/LTG_CHAR_luma_expression_sheet_v004.py")
_tool_path = os.path.normpath(_tool_path)

if __name__ == "__main__":
    with open(_tool_path) as f:
        code = f.read()
    exec(compile(code, _tool_path, "exec"), {"__name__": "__main__", "__file__": _tool_path})
