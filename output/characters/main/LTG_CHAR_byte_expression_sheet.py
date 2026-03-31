#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_CHAR_byte_expression_sheet.py
Byte Expression Sheet Generator — "Luma & the Glitchkin"
Cycle 52 production entry point.

This script is the canonical production copy.
Tool source: output/tools/LTG_TOOL_byte_expression_sheet.py

v008 Cycle 52 (Rin Yamamoto): pycairo rebuild — anti-aliased rendering,
wobble outlines, bezier confetti trails. All 10 expressions preserved.
"""
import sys
import os

# Run the tool from output/tools/
_tool_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "../../tools/LTG_TOOL_byte_expression_sheet.py")
_tool_path = os.path.normpath(_tool_path)

if __name__ == "__main__":
    # Execute the tool script directly
    with open(_tool_path) as f:
        code = f.read()
    exec(compile(code, _tool_path, "exec"), {"__name__": "__main__", "__file__": _tool_path})
