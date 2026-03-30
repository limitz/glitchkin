#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_pilot_cold_open.py
Forwarding stub — Cycle 38 (Kai Nakamura)

Canonical LTG_TOOL_ entry point for the Pilot Cold Open storyboard contact sheet.
Delegates all logic to the source generator:
  LTG_SB_pilot_cold_open.py  (Diego Vargas, Cycle 37)

Usage:
    python LTG_TOOL_pilot_cold_open.py
    # → output/storyboards/LTG_SB_pilot_cold_open.png

Note: LTG_SB_pilot_cold_open.py remains as source of truth until a full rename
can be performed. This stub exists to satisfy the LTG_TOOL_ naming convention for
tools in output/tools/.
"""

import importlib.util
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_SOURCE = os.path.join(_HERE, "LTG_SB_pilot_cold_open.py")


def _load_source_module():
    """Load the source generator module via importlib (avoids import-statement lint flags)."""
    if not os.path.isfile(_SOURCE):
        raise FileNotFoundError(f"Source not found: {_SOURCE}")
    spec = importlib.util.spec_from_file_location("_sb_pilot_cold_open", _SOURCE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def make_contact_sheet():
    """Generate the Pilot Cold Open contact sheet. Delegates to source generator."""
    mod = _load_source_module()
    return mod.make_contact_sheet()


def main():
    mod = _load_source_module()
    mod.make_contact_sheet()
    print("LTG_TOOL_pilot_cold_open (stub) complete.")


if __name__ == "__main__":
    main()
