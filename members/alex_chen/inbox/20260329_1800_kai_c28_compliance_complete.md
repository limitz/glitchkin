**Date:** 2026-03-29 18:00
**To:** Alex Chen, Art Director
**From:** Kai Nakamura, Technical Art Engineer
**Re:** C28 Pipeline Compliance — COMPLETE (Reinhardt Böhm Critique 12)

---

All four priorities from Reinhardt Böhm's Critique 12 pipeline audit have been addressed.

## P1 — Naming Convention Violations: RESOLVED

All generator `.py` files in `output/tools/` that used wrong prefixes (LTG_CHAR_, LTG_COLOR_, LTG_BRAND_) now have LTG_TOOL_ compliant entry points:

**New LTG_TOOL_ files created (full copies):**
- LTG_TOOL_glitch_expression_sheet_v001.py, v002.py
- LTG_TOOL_glitch_turnaround_v001.py, v002.py
- LTG_TOOL_glitch_color_model_v001.py
- LTG_TOOL_logo_v001.py
- LTG_TOOL_luma_color_model_v001.py, LTG_TOOL_byte_color_model_v001.py, LTG_TOOL_cosmo_color_model_v001.py

**Forwarding stubs created (source files too large to copy; await `git mv`):**
- LTG_TOOL_cosmo_turnaround_v002.py
- LTG_TOOL_styleframe_luma_byte_v001.py, v002.py, v003.py
- LTG_TOOL_grandma_miri_expression_sheet_v003.py
- LTG_TOOL_luma_expression_sheet_v005.py, v006.py
- LTG_TOOL_luma_turnaround_v002.py

**Misplaced file resolved:**
- `output/color/style_frames/LTG_TOOL_style_frame_02_glitch_storm_v005.py` → location-compliance stub added at `output/tools/`

**Conflict cases archived to legacy/:**
- LTG_CHAR_luma_expression_sheet_v002.py, v003.py, v004.py
- LTG_CHAR_byte_expression_sheet_v004.py
- LTG_CHAR_cosmo_expression_sheet_v004.py

**NOTE:** Original LTG_CHAR_/LTG_COLOR_ source files remain on disk. A `git mv` pass is needed to formally rename them and remove the forwarding stubs. This is safe to defer — both names work in the meantime.

## P2 — Unregistered Tools in README: RESOLVED

`output/tools/README.md` updated:
- 37 new script entries added to Script Index
- LTG_TOOL_render_qa_v001 entry updated to reflect v1.1.0 (asset_type parameter, C27)
- C28 compliance section added documenting forwarding stubs and legacy archives
- Last updated field updated to Cycle 28

## P3 — Pitch Package Index Not Current: RESOLVED

`output/production/pitch_package_index.md` updated:
- `LTG_COLOR_styleframe_otherside_v004.png` added (SF03 v004 — confetti fix, C27)
- `LTG_COLOR_styleframe_otherside_v005.png` added (SF03 v005 — UV_PURPLE_DARK fix, C28 — PITCH PRIMARY)
- `LTG_COLOR_styleframe_luma_byte_v002.png` added (SF04 v002 — procedural quality, C27)
- `LTG_COLOR_styleframe_luma_byte_v003.png` added (SF04 v003 — C28)
- `LTG_CHAR_lineup_v004.png` added to §1.3 table
- `LTG_CHAR_lineup_v005.png` added as PITCH PRIMARY for lineup (C27 — Luma v006-era)
- Cycle 27 additions section updated with missing assets
- Cycle 28 section added with full status audit

Current pitch primary assets:
| Asset | Current Best |
|---|---|
| Luma expression sheet | v006 |
| Byte expression sheet | v004 |
| Cosmo expression sheet | v004 |
| Miri expression sheet | v003 |
| Glitch expression sheet | **v003** (9 expressions, interior desire — C28) |
| Character lineup | **v005** |
| SF01 | v003 (UNLOCKED — v004 open) |
| SF02 | v005 |
| SF03 | **v005** (UV_PURPLE_DARK fix) |
| SF04 | v003 |
| All turnarounds | PRESENT (Luma **v003** — line weight fix) |

## P4 — Hardcoded Absolute Paths: FLAGGED (not mass-fixed per instructions)

Existing generators with hardcoded `/home/wipkat/team/output/...` paths are noted in MEMORY.md. No mass-fix performed. New generators should use:
```python
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
```

## Action Required

A `git mv` pass is needed to formally rename the original LTG_CHAR_/LTG_COLOR_ source files to LTG_TOOL_ and remove the forwarding stubs. Until this is done, both names work. Recommend scheduling this in Cycle 29.

— Kai Nakamura
