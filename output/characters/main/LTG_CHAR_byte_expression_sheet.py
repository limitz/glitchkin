#!/usr/bin/env python3
"""
LTG_CHAR_byte_expression_sheet_v004.py
Byte Expression Sheet Generator — "Luma & the Glitchkin"
Cycle 22 production entry point.

This script is the canonical production copy.
Tool source: output/tools/LTG_CHAR_byte_expression_sheet_v004.py

v004 Cycle 22 (Maya Santos): Critique 10 fixes — Dmitri Volkov + Victoria Ashford.
  Fix 1a — STORM/CRACKED glyph corrected per Section 9B canonical spec:
    - 7x7 grid re-implemented row-by-row (CRACK is overlay only, not a pixel state).
    - DIM_PX color corrected: (18,52,60) #123C3C -> (0,80,100) #005064.
    - Crack line INSIDE dead_zone changed to void black LINE (#0A0A14), not HOT_MAG.
      HOT_MAG crack stays on body/frame EXTERIOR only per spec.
  Fix 1b — STORM arm asymmetry: arm_l_dy=6, arm_r_dy=22 (20+ unit diff).
    Suggests physical imbalance — STORM = damaged-asymmetric at thumbnail.
    RESIGNED arms remain symmetric (14,14).
  Fix 1c — RELUCTANT JOY: stronger "fighting against joy" signal.
    body_tilt 10->12, arm_l_dy changes to -2 (one arm resisting upward push).
    reluctant_joy=True flag triggers perked antenna hint.
  Fix 1d — POWERED DOWN squash: 0.88 -> 0.75, arm_dy maxed to 18.
# TODO: update import to LTG_TOOL_render_lib_v001 after Kai's rename
"""
import sys
import os

# Run the tool from output/tools/
_tool_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "../../tools/LTG_CHAR_byte_expression_sheet_v004.py")
_tool_path = os.path.normpath(_tool_path)

if __name__ == "__main__":
    # Execute the tool script directly
    with open(_tool_path) as f:
        code = f.read()
    exec(compile(code, _tool_path, "exec"), {"__name__": "__main__", "__file__": _tool_path})
