#!/usr/bin/env python3
"""
LTG_TOOL_luma_expression_sheet_v006.py
Naming-compliant entry point for Luma Expression Sheet v006 (Cycle 27).

C28 RENAME NOTE: The original file was LTG_CHAR_luma_expression_sheet_v006.py.
Generator files in output/tools/ must use LTG_TOOL_ prefix (Reinhardt Bohm
critique C12 / C28 compliance work).

The original LTG_CHAR_luma_expression_sheet_v006.py remains on disk until git mv
can be performed to preserve history. Once renamed, this stub can be removed.
Output PNG name is unchanged: LTG_CHAR_luma_expression_sheet_v006.png

This module re-exports all public symbols from the original file so that
both names work correctly.
"""

import os
import sys

_TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _TOOLS_DIR)

# Import everything from the original module
from LTG_CHAR_luma_expression_sheet_v006 import *
import LTG_CHAR_luma_expression_sheet_v006 as _src_module


def main():
    _src_module.main()


if __name__ == "__main__":
    main()
