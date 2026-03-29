#!/usr/bin/env python3
"""
LTG_TOOL_cosmo_turnaround_v002.py
Naming-compliant entry point for Cosmo 4-View Turnaround v002.

C28 RENAME NOTE: The original file was LTG_CHAR_cosmo_turnaround_v002.py.
Generator files in output/tools/ must use LTG_TOOL_ prefix (Reinhardt Bohm
critique C12 / C28 compliance work).

The original LTG_CHAR_cosmo_turnaround_v002.py remains on disk until git mv
can be performed to preserve history. Once renamed, this stub can be removed.

This module re-exports all public symbols from the original file so that
both names work correctly.
"""

import os
import sys

_TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _TOOLS_DIR)

# Import everything from the original module
from LTG_CHAR_cosmo_turnaround_v002 import *
import LTG_CHAR_cosmo_turnaround_v002 as _src_module


def main():
    _src_module.main()


if __name__ == "__main__":
    main()
