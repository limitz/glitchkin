**Date:** 2026-03-31
**From:** Morgan Walsh
**Subject:** C52 Completion Report

## P1: CI Suite v2.0.0 — 3 New Checks (Slots 11-13)

- **Check 11: dep_availability** — verifies bezier, Shapely, pycairo are importable. WARN if any missing. `check_dep_availability()` exported.
- **Check 12: bezier_migration_lint** — wraps curve_utils `audit_hand_rolled_bezier()` to detect files still using hand-rolled bezier. WARN for pending migrations. `check_bezier_migration()` exported.
- **Check 13: tool_naming_lint** — enforces LTG_TOOL_ prefix on all .py files in tools dir. Legacy/deprecated subdirs exempt. `check_tool_naming()` exported.
- Registry updated: 3 new slots in `ci_check_registry.json` with swap_history entries.
- Runner map updated for registry-driven execution.
- Version: 1.9.0 -> 2.0.0. Changelog, docstring, API section updated.

## P2: Bezier Migration — 4 Files (Batch 1 of 2)

Migrated to import from LTG_TOOL_curve_utils:
1. **LTG_TOOL_face_curve_validator.py** — full migration (local defs removed, imports added)
2. **LTG_TOOL_luma_face_curves.py** — delegate wrappers (preserve `n=` kwarg API)
3. **LTG_TOOL_character_lineup.py** — delegate wrappers (_bezier3 + _polyline)
4. **LTG_TOOL_luma_expression_sheet.py** — delegate wrappers (bezier3 + polyline)

Audit after migration: 1 MIGRATED, 3 PARTIAL, 5 NOT_MIGRATED. The 3 PARTIAL files delegate math to curve_utils but keep thin wrappers for API compatibility. 4 remaining files (construction_prototype, gesture_prototype, P17_chartest, grandma_miri) are batch 2.

## P3: precritique_qa — Already Done

Kai Nakamura already bumped precritique_qa to v3.0.0 with sections 15-17 and CYCLE_LABEL=C52. No action needed from me.

## P4: Ideabox

- C51 curve_quality_ci_check — still pending (needs curve registry + full migration)
- C51 precritique_char_sections — actioned by Kai (sections 15-17)
- C52 submitted: bezier_migration_batch_2 (complete remaining 4 files)

## Verification

- All 4 migrated files: syntax PASS (ast.parse clean)
- CI suite: syntax PASS
- ci_check_registry.json: valid JSON with 13 slots
