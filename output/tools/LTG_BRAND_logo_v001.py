#!/usr/bin/env python3
"""
LTG_BRAND_logo_v001.py
Canonical Show Logo — "Luma & the Glitchkin"
Art Director: Alex Chen — Cycle 25

Decision record:
  The canonical logo is the asymmetric layout developed in Cycle 13
  (LTG_TOOL_logo_asymmetric_v002.py, received A grade from Victoria Ashford).
  Design: "Luma" dominant/warm-amber left, "&" warm-to-cold gradient hinge,
  "the Glitchkin" stacked/electric-cyan right. Bi-color scan bar. Void Black BG.

  This script is the canonical entry point. It produces:
    output/production/LTG_BRAND_logo_v001.png

  The underlying generator is LTG_TOOL_logo_asymmetric_v002.py.
  No design changes from v002 — this is a canonical alias for delivery.

Usage:
  python3 output/tools/LTG_BRAND_logo_v001.py
"""

import os
import sys
import shutil

# Import the underlying generator
TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, TOOLS_DIR)

from LTG_TOOL_logo_asymmetric_v002 import generate as _gen_asymmetric_v002

CANONICAL_OUTPUT = "/home/wipkat/team/output/production/LTG_BRAND_logo_v001.png"
UNDERLYING_OUTPUT = "/home/wipkat/team/output/production/LTG_BRAND_logo_asymmetric_v002.png"


def generate():
    os.makedirs(os.path.dirname(CANONICAL_OUTPUT), exist_ok=True)
    # Generate (or regenerate) via the underlying v002 generator
    _gen_asymmetric_v002()
    # Copy to canonical output path
    shutil.copy2(UNDERLYING_OUTPUT, CANONICAL_OUTPUT)
    print(f"Canonical logo saved: {CANONICAL_OUTPUT}")
    return CANONICAL_OUTPUT


if __name__ == "__main__":
    generate()
