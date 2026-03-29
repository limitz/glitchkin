#!/usr/bin/env python3
"""
LTG_CHAR_cosmo_expression_sheet_v004.py
Cosmo Expression Sheet Generator — "Luma & the Glitchkin"
Cycle 22 production entry point.

This script is the canonical production copy.
Tool source: output/tools/LTG_CHAR_cosmo_expression_sheet_v004.py

v004 Cycle 22 (Maya Santos): Critique 10 fix — Dmitri Volkov Priority 3.
  SKEPTICAL arm posture redesigned:
    PROBLEM: arm_l_dy=-14, arm_r_dy=-10 pushes arms UPWARD -> reads as mild SURPRISED at thumbnail.
    FIX (Option B): arms lowered to near-neutral (arm_l_dy=2, arm_r_dy=2) + body_squash=0.92
    to read as "compressed/contained". Asymmetric brow remains as face-level signal.
    Goal: SKEPTICAL reads as "contracted inward" at thumbnail, NOT "arms raised".
# TODO: update import to LTG_TOOL_render_lib_v001 after Kai's rename
"""
import sys
import os

_tool_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "../../tools/LTG_CHAR_cosmo_expression_sheet_v004.py")
_tool_path = os.path.normpath(_tool_path)

if __name__ == "__main__":
    with open(_tool_path) as f:
        code = f.read()
    exec(compile(code, _tool_path, "exec"), {"__name__": "__main__", "__file__": _tool_path})
