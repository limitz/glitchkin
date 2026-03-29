"""
run_color_verify_c32.py
=======================
C32 spot-check: Run LTG_TOOL_color_verify_v002 with histogram=True
on the master_palette.md spot-check set after C32 fixes.

Fixes applied this cycle:
- CHAR-L-11 cross-reference corrected (#00D4E8 → #00F0FF in cross-ref line)
- CHAR-M-11 Miri slippers corrected (#5A7A5A Deep Sage → #C4907A Warm Apricot)
- DRW-18 warmth claim clarified (7% lightness = visually not warm)

Author: Sam Kowalski — Cycle 32 — 2026-03-30
"""

import sys
import os

# Add tools directory to path
sys.path.insert(0, "/home/wipkat/team/output/tools")

from LTG_TOOL_color_verify_v002 import verify_canonical_colors, get_canonical_palette, format_histogram

try:
    from PIL import Image
except ImportError:
    print("ERROR: Pillow not available.")
    sys.exit(1)

# Spot-check assets — pitch-primary set + Miri color model
ASSETS = [
    # Style frames
    ("/home/wipkat/team/output/color/style_frames/LTG_COLOR_styleframe_discovery_v004.png",  "SF01 Discovery v004 (pitch primary)"),
    ("/home/wipkat/team/output/color/style_frames/LTG_COLOR_styleframe_glitch_storm_v005.png", "SF02 Glitch Storm v005 (pitch primary)"),
    ("/home/wipkat/team/output/color/style_frames/LTG_COLOR_styleframe_otherside_v005.png",  "SF03 Other Side v005 (pitch primary, DRW-18 scene)"),
    ("/home/wipkat/team/output/color/style_frames/LTG_COLOR_styleframe_luma_byte_v003.png",  "SF04 Luma+Byte v003"),
    # Character color models
    ("/home/wipkat/team/output/characters/color_models/LTG_COLOR_grandma_miri_color_model_v001.png", "Miri color model v001 (CHAR-M-11 scene)"),
    ("/home/wipkat/team/output/characters/color_models/LTG_COLOR_luma_color_model_v002.png", "Luma color model v002 (CHAR-L-11 scene)"),
    ("/home/wipkat/team/output/characters/color_models/LTG_COLOR_byte_color_model_v001.png", "Byte color model v001"),
]

palette = get_canonical_palette()
results = []

for path, label in ASSETS:
    if not os.path.exists(path):
        results.append(f"### {label}\n**SKIP** — file not found: {path}\n")
        continue
    try:
        img = Image.open(path).convert("RGB")
        # Downscale to ≤1280px for efficient processing
        img.thumbnail((1280, 1280))
        r = verify_canonical_colors(img, palette, max_delta_hue=5, histogram=True)
        lines = [f"### {label}", f"**Overall:** {'PASS' if r['overall_pass'] else 'FAIL/NOT_FOUND'}"]
        for color_name, data in r.items():
            if color_name == "overall_pass":
                continue
            status = data.get("status", "")
            if status == "not_found":
                lines.append(f"- **{color_name}:** not_found (not present in image — expected for some assets)")
                continue
            target = data.get("target_hue", "?")
            found = data.get("found_hue", "?")
            delta = data.get("delta", "?")
            passed = data.get("pass", False)
            flag = "PASS" if passed else "FAIL"
            lines.append(f"- **{color_name}:** target={target:.1f}° found={found:.1f}° Δ={delta:.1f}° → {flag}")
            # Show histogram if available
            hist = data.get("hue_histogram")
            cb = data.get("canonical_bucket_index")
            if hist is not None and cb is not None:
                hist_str = format_histogram(hist, cb)
                # Compact: first 5 lines of histogram only
                hist_lines = hist_str.split("\n")[:6]
                lines.append("  Histogram (5°/bucket, canonical band marked with *):")
                for hl in hist_lines:
                    lines.append("  " + hl)
        lines.append("")
        results.append("\n".join(lines))
    except Exception as e:
        results.append(f"### {label}\n**ERROR:** {e}\n")

# Write report
report_path = "/home/wipkat/team/output/production/color_verify_c32_spot_check.md"
header = """# Color Verify C32 Spot-Check Report

**Run by:** Sam Kowalski — Cycle 32 — 2026-03-30
**Tool:** LTG_TOOL_color_verify_v002.py with histogram=True
**Purpose:** Post-fix verification after C32 palette corrections
  - CHAR-L-11 cross-ref: #00D4E8 → #00F0FF
  - CHAR-M-11 slippers: #5A7A5A Deep Sage → #C4907A Warm Apricot
  - DRW-18 warmth clarification (documented, no hex change)

**Palette verified:** 6 canonical colors (CORRUPT_AMBER, BYTE_TEAL, UV_PURPLE, HOT_MAGENTA, ELECTRIC_CYAN, SUNLIT_AMBER)
**Threshold:** Δhue ≤ 5° = PASS

---

"""

with open(report_path, "w") as f:
    f.write(header)
    f.write("\n".join(results))

print(f"Report written: {report_path}")
print("---")
print("\n".join(results))
