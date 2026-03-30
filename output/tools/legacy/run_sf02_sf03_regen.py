#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
run_sf02_sf03_regen_v002.py — Regenerate SF02 and SF03 styled outputs
"Luma & the Glitchkin" — Rin Yamamoto / Cycle 28

Applies LTG_TOOL_stylize_handdrawn_v002 (v2.0.2) to:
  SF02: LTG_COLOR_styleframe_glitch_storm_v005.png  → mixed mode
  SF03: LTG_COLOR_styleframe_otherside_v003.png     → glitch mode

Both outputs go to: output/color/style_frames/

Run from project root:
    cd /home/wipkat/team
    python3 output/tools/run_sf02_sf03_regen_v002.py

Changes in v2.0.2 (C28):
  - _restore_canonical_colors() added as post-pass step
  - UV_PURPLE drift at region boundaries corrected
  - SUNLIT_AMBER bleed in glitch mode corrected
  - Warm bleed guard in _apply_glitch_treatment explicitly documented
"""

import sys
import os

# Ensure we can find the tool in the legacy directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEGACY_TOOLS_DIR = os.path.join(PROJECT_ROOT, "output", "tools", "legacy")
sys.path.insert(0, LEGACY_TOOLS_DIR)

from LTG_TOOL_stylize_handdrawn_v002 import stylize, verify_canonical_colors
from PIL import Image

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
STYLE_FRAMES_DIR = os.path.join(PROJECT_ROOT, "output", "color", "style_frames")

SF02_SOURCE = os.path.join(STYLE_FRAMES_DIR, "LTG_COLOR_styleframe_glitch_storm_v005.png")
SF02_OUTPUT = os.path.join(STYLE_FRAMES_DIR, "LTG_COLOR_styleframe_glitch_storm_v005_styled_v002.png")

SF03_SOURCE = os.path.join(STYLE_FRAMES_DIR, "LTG_COLOR_styleframe_otherside_v003.png")
SF03_OUTPUT = os.path.join(STYLE_FRAMES_DIR, "LTG_COLOR_styleframe_otherside_v003_styled_v002.png")

# ---------------------------------------------------------------------------
# Validate sources exist
# ---------------------------------------------------------------------------
def check_source(path):
    if not os.path.exists(path):
        print(f"  [ERROR] Source not found: {path}")
        return False
    img = Image.open(path)
    print(f"  [OK] Source found: {path} ({img.width}x{img.height})")
    return True


# ---------------------------------------------------------------------------
# Regenerate SF02 — mixed mode
# ---------------------------------------------------------------------------
def regen_sf02():
    print("\n=== SF02: Glitch Storm — mixed mode (intensity=1.0) ===")
    if not check_source(SF02_SOURCE):
        return False

    print(f"  Output: {SF02_OUTPUT}")
    stylize(
        input_path=SF02_SOURCE,
        output_path=SF02_OUTPUT,
        mode="mixed",
        intensity=1.0,
        seed=42,
    )
    print("  [SF02 DONE]")
    return True


# ---------------------------------------------------------------------------
# Regenerate SF03 — glitch mode
# ---------------------------------------------------------------------------
def regen_sf03():
    print("\n=== SF03: Other Side — glitch mode (intensity=1.0) ===")
    if not check_source(SF03_SOURCE):
        return False

    print(f"  Output: {SF03_OUTPUT}")
    stylize(
        input_path=SF03_SOURCE,
        output_path=SF03_OUTPUT,
        mode="glitch",
        intensity=1.0,
        seed=42,
    )
    print("  [SF03 DONE]")
    return True


# ---------------------------------------------------------------------------
# Post-verification: check SUNLIT_AMBER in SF03
# ---------------------------------------------------------------------------
def check_sf03_sunlit_amber():
    """Confirm SF03 output has zero SUNLIT_AMBER region (warm bleed guard check)."""
    print("\n=== SF03 SUNLIT_AMBER guard check ===")
    if not os.path.exists(SF03_OUTPUT):
        print("  [SKIP] SF03 output not found, cannot check.")
        return

    import numpy as np
    img = Image.open(SF03_OUTPUT).convert("RGB")
    arr = np.array(img)

    # SUNLIT_AMBER canonical RGB: (212, 146, 58)
    cr, cg, cb = 212, 146, 58
    diff = arr.astype(int) - np.array([cr, cg, cb])
    dist = np.sqrt(np.sum(diff ** 2, axis=2))
    amber_pixels = int(np.sum(dist <= 25))

    if amber_pixels == 0:
        print(f"  [PASS] Zero SUNLIT_AMBER pixels in SF03 output. Warm bleed guard is clean.")
    else:
        print(f"  [WARN] {amber_pixels} SUNLIT_AMBER pixels detected in SF03 output.")
        print(f"         These should not exist in a cold Glitch Layer scene.")
        print(f"         Check source image for accidental warm regions.")

    # Also check source for comparison
    src_img = Image.open(SF03_SOURCE).convert("RGB")
    src_arr = np.array(src_img)
    src_diff = src_arr.astype(int) - np.array([cr, cg, cb])
    src_dist = np.sqrt(np.sum(src_diff ** 2, axis=2))
    src_amber = int(np.sum(src_dist <= 25))
    print(f"  Source SUNLIT_AMBER pixels: {src_amber}")
    if src_amber > 0:
        print(f"  [NOTE] Source has warm pixels — generation issue, not a bleed gate failure.")
        print(f"         Flag to Sam/Alex: SF03 source should contain no SUNLIT_AMBER.")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("LTG Styleframe Regen v002 — C28 Fix 5 (Canonical Color Restore)")
    print("=" * 60)

    ok_sf02 = regen_sf02()
    ok_sf03 = regen_sf03()

    if ok_sf02 and ok_sf03:
        check_sf03_sunlit_amber()
        print("\n=== ALL DONE ===")
        print(f"SF02 output: {SF02_OUTPUT}")
        print(f"SF03 output: {SF03_OUTPUT}")
        print("Run verify_canonical_colors() results shown above.")
        print("UV_PURPLE must show < 5° drift. SUNLIT_AMBER in SF03 must be 0.")
    else:
        print("\n=== PARTIAL FAILURE — check errors above ===")
