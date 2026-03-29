"""
LTG_CHAR_luma_motion_v001.py
FORWARDING STUB — Cycle 38 (Kai Nakamura)

This file previously contained the full Luma Motion Spec Sheet generator.
Renamed to LTG_TOOL_ prefix per naming conventions (Cycle 38).

Canonical file: LTG_TOOL_luma_motion_v001.py
"""

import importlib.util
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
_CANONICAL = os.path.join(_HERE, "LTG_TOOL_luma_motion_v001.py")


def _load():
    spec = importlib.util.spec_from_file_location("_ltg_tool_luma_motion_v001", _CANONICAL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    _load().main()


if __name__ == "__main__":
    main()
