#!/usr/bin/env python3
"""
LTG_TOOL_style_frame_02_glitch_storm_v005.py
Naming-compliant entry point for Style Frame 02 "Glitch Storm" v005 (Cycle 22).

C28 LOCATION NOTE: The source file was placed in output/color/style_frames/ instead
of output/tools/. Generator files must live in output/tools/ (Reinhardt Bohm
critique C12 / C28 compliance work).

The original output/color/style_frames/LTG_TOOL_style_frame_02_glitch_storm_v005.py
remains on disk until `git mv` can be performed to preserve history. Once moved,
this stub can be removed.
Output PNG name is unchanged: LTG_COLOR_style_frame_02_glitch_storm_v005.png

This module re-exports all public symbols from the original file so that
output/tools/ is the canonical location.
"""

import os
import sys

# The actual source lives in output/color/style_frames/
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_SRC_DIR = os.path.join(_PROJECT_ROOT, "color", "style_frames")
sys.path.insert(0, _SRC_DIR)

# Import everything from the original module
from LTG_TOOL_style_frame_02_glitch_storm_v005 import *
import LTG_TOOL_style_frame_02_glitch_storm_v005 as _src_module


def main():
    _src_module.main()


if __name__ == "__main__":
    main()
