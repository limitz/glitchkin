# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
run_c31_qa.py
=============
C31 QA runner for Sam Kowalski — runs LTG_TOOL_render_qa.py on all
pitch-primary assets for Critique 13.

Assets:
  Style Frames: SF01 v004, SF02 v005, SF03 v005, SF04 v003
  Character Sheets:
    - Luma expressions v007
    - Luma turnaround v003
    - Luma color model v002
    - Byte expression sheet v004
    - Cosmo expression sheet v004
    - Grandma Miri expression sheet v003
    - Glitch expression sheet v003
    - Character lineup v006

Output: /home/wipkat/team/output/production/qa_c31_pitch_assets.md
"""

import sys
import os
from pathlib import Path

# Add tools dir to path
TOOLS_DIR = Path(__file__).parent
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from LTG_TOOL_render_qa import qa_report, qa_summary_report

ROOT = Path("/home/wipkat/team")

ASSETS = [
    # Style frames
    (ROOT / "output/color/style_frames/LTG_COLOR_styleframe_discovery.png",     "style_frame",    "SF01 v004"),
    (ROOT / "output/color/style_frames/LTG_COLOR_styleframe_glitch_storm.png",  "style_frame",    "SF02 v005"),
    (ROOT / "output/color/style_frames/LTG_COLOR_styleframe_otherside.png",     "style_frame",    "SF03 v005"),
    (ROOT / "output/color/style_frames/LTG_COLOR_styleframe_luma_byte.png",     "style_frame",    "SF04 v003"),
    # Character sheets
    (ROOT / "output/characters/main/LTG_CHAR_luma_expressions.png",             "character_sheet","Luma expr v007"),
    (ROOT / "output/characters/main/turnarounds/LTG_CHAR_luma_turnaround.png",  "character_sheet","Luma turnaround v003"),
    (ROOT / "output/characters/color_models/LTG_COLOR_luma_color_model.png",    "color_model",    "Luma color model v002"),
    (ROOT / "output/characters/main/LTG_CHAR_byte_expression_sheet.png",        "character_sheet","Byte expr sheet v004"),
    (ROOT / "output/characters/main/LTG_CHAR_cosmo_expression_sheet.png",       "character_sheet","Cosmo expr sheet v004"),
    (ROOT / "output/characters/main/LTG_CHAR_grandma_miri_expression_sheet.png","character_sheet","Miri expr sheet v003"),
    (ROOT / "output/characters/main/LTG_CHAR_glitch_expression_sheet.png",      "character_sheet","Glitch expr sheet v003"),
    (ROOT / "output/characters/main/LTG_CHAR_luma_lineup.png",                  "character_sheet","Character lineup v006"),
]

results = []
labels = []

for asset_path, asset_type, label in ASSETS:
    print(f"[QA] Checking: {label} ({asset_path.name})")
    if not asset_path.exists():
        print(f"  MISSING: {asset_path}")
        results.append({
            "file": str(asset_path),
            "asset_type": asset_type,
            "error": "File not found",
            "overall_grade": "FAIL",
            "_label": label,
        })
        labels.append(label)
        continue
    try:
        r = qa_report(str(asset_path), asset_type=asset_type)
        r["_label"] = label
        results.append(r)
        grade = r["overall_grade"]
        sil = r["silhouette"]["score"]
        vr = r["value_range"]
        cf_pass = r["color_fidelity"].get("overall_pass", True)
        wc = r["warm_cool"]
        lw = r["line_weight"]
        wc_str = "SKIP" if wc.get("status") == "SKIPPED" else ("PASS" if wc.get("pass", True) else "WARN")
        print(f"  Grade={grade}  Silhouette={sil}  Value=min{vr['min']}/max{vr['max']}/range{vr['range']}  Color={'PASS' if cf_pass else 'WARN'}  WarmCool={wc_str}  LineWeight={'PASS' if lw['pass'] else 'WARN'}")
    except Exception as e:
        print(f"  ERROR: {e}")
        results.append({
            "file": str(asset_path),
            "asset_type": asset_type,
            "error": str(e),
            "overall_grade": "FAIL",
            "_label": label,
        })
    labels.append(label)

# Write report
OUT = ROOT / "output/production/qa_c31_pitch_assets.md"
qa_summary_report(results, str(OUT))
print(f"\n[QA] Report written to: {OUT}")

# Print summary
passes = sum(1 for r in results if r.get("overall_grade") == "PASS")
warns = sum(1 for r in results if r.get("overall_grade") == "WARN")
fails = sum(1 for r in results if r.get("overall_grade") == "FAIL")
print(f"\nSUMMARY: {passes} PASS / {warns} WARN / {fails} FAIL  (out of {len(results)} assets)")
