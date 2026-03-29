**Date:** 2026-03-29 17:30
**To:** Kai Nakamura
**From:** Producer (relaying Critique 12 — Reinhardt Böhm)
**Re:** C28 Priority — Pipeline & Naming Compliance
**Status:** ARCHIVED — Completed Cycle 28

---

Reinhardt rated the pipeline FAIL. Three systemic issues to fix in Cycle 28.

## P1 — Naming Convention Violations (54+ files)

Reinhardt found that generators use `LTG_CHAR_`, `LTG_COLOR_`, `LTG_BRAND_` as prefixes for generator `.py` files in `output/tools/`. The correct category for generators is `LTG_TOOL_`.

**Scope of violations (from Reinhardt's audit):**
- All Glitch character generators (`LTG_CHAR_glitch_*.py`)
- Multiple Luma expression sheet generators (`LTG_CHAR_luma_expression_sheet_*.py`)
- SF04 generators (`LTG_COLOR_styleframe_luma_byte_v*.py`)
- Other character generators with `LTG_CHAR_` prefix in tools/

**Action:** Write a migration script or do a batch rename. For each violating generator:
- Rename to `LTG_TOOL_[descriptor]_v[###].py` format
- The output PNGs keep their current names (PNG naming follows the CATEGORY of the output, not the tool)
- Update README.md entries accordingly

**Note:** The production/ exemption covers `output/production/` files only. Generator `.py` files in `output/tools/` are always `LTG_TOOL_`.

## P2 — 24 Unregistered Tools in README

24 tools present on disk have no entry in `output/tools/README.md`. Key missing entries:
- All Glitch character generators
- Both SF04 generators
- `LTG_TOOL_character_lineup_v004`, `LTG_TOOL_character_lineup_v005`
- `LTG_TOOL_procedural_draw_v001`
- `LTG_TOOL_render_qa_v001`
- Others found by Reinhardt

**Action:** Read the full tools/ directory, compare against README. Add missing entries.

## P3 — Pitch Package Index Not Current

`output/production/pitch_package_index.md` is missing:
- `LTG_COLOR_styleframe_otherside_v004.png` (SF03 v004 — C27 new)
- `LTG_COLOR_styleframe_luma_byte_v002.png` (SF04 v002 — C27 new)
- `LTG_CHAR_lineup_v005.png` (C27 new)

**Action:** Add these entries.

## P4 — Hardcoded Absolute Paths

Multiple generators hardcode `/home/wipkat/team/output/...`. Change to relative path using:
```python
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
```
Do this for new generators going forward; flag existing violators but do not mass-fix (low priority vs other tasks).

Send completion report to `members/alex_chen/inbox/` when done.

— Producer
