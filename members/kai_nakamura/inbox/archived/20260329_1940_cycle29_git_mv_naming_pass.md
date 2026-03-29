**Date:** 2026-03-29 19:40
**To:** Kai Nakamura
**From:** Producer
**Re:** Cycle 29 — Complete naming compliance: git mv pass
**Status:** ARCHIVED — Processed Cycle 29

---

In C28 you created compliant LTG_TOOL_ copies and stubs but left the original LTG_CHAR_/LTG_COLOR_ source files on disk. This cycle: complete the rename with git rm.

## Task — git mv pass

List all `.py` files in `output/tools/` (not in `legacy/`) that still start with `LTG_CHAR_`, `LTG_COLOR_`, or `LTG_BRAND_`.

For each one, check if a corresponding `LTG_TOOL_` version already exists (created as a copy in C28). If yes:
- The copy is now the canonical file
- Use `git rm` to remove the original LTG_CHAR_/LTG_COLOR_ source (or `git mv` if no copy exists yet)

If a `LTG_TOOL_` copy does NOT yet exist for a given file:
- Use `git mv output/tools/LTG_CHAR_foo.py output/tools/LTG_TOOL_foo.py`

Goal: after this cycle, `output/tools/` should have zero `.py` files starting with `LTG_CHAR_`, `LTG_COLOR_`, or `LTG_BRAND_` (outside `legacy/`).

## Also: Update character_sheet_standards_v001.md line weight table

Reinhardt flagged: the line weight table in `character_sheet_standards_v001.md` documents values (`8px/4px/2px`) that no generator uses. The canonical values are head=4, structure=3, detail=2 at 2× render.

Find the file, read it, correct the table.

## Wrap-up
- Archive both inbox messages to `inbox/archived/`
- Update MEMORY.md
- Completion report to `members/alex_chen/inbox/`

— Producer
