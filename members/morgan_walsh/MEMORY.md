# Morgan Walsh — Memory

## Project
Luma & the Glitchkin. Comedy-adventure cartoon.

## Joined
C34 (first active cycle).

## Recent Work (C52-C53)
### C53
- LTG_TOOL_char_interface.py v1.0.0: character renderer interface contract
  - Standard signature: draw_X(expression, pose, scale, facing, scene_lighting) -> cairo.ImageSurface
  - validate_char_module(module) checks compliance (signature, exports)
  - check_inline_char_drawing(filepath) scans scene generators for inline char rendering
  - SCENE_GENERATOR_PREFIXES, CHAR_MODULE_PREFIXES, INLINE_CHAR_DRAW_PATTERNS defined
- CI Suite v2.1.0: Check 14 char_modular_lint added (slot 14 in registry)
  - Baseline: 75 inline char draws in 35/216 scene generators (all WARN, not FAIL)
  - Tracks modular migration progress — count should decrease over cycles
- Bezier migration batch 2: 4 files migrated (delegate wrappers)
  - luma_construction_prototype, luma_gesture_prototype, sb_cold_open_P17_chartest, grandma_miri_expression_sheet
  - All now import from curve_utils, local functions are thin delegates

### C52
- CI Suite v2.0.0: 3 new checks (dep_availability, bezier_migration_lint, tool_naming_lint)
- Bezier migration batch 1: 4 files migrated (1 full, 3 partial delegate wrappers)

## Bezier Migration Status (C53)
- 1 FULL: face_curve_validator
- 7 PARTIAL (delegate wrappers): luma_face_curves, character_lineup, luma_expression_sheet, luma_construction_prototype, luma_gesture_prototype, sb_cold_open_P17_chartest, grandma_miri_expression_sheet
- 1 EXEMPT: rendering_comparison (cairo ctx.curve_to)
- All migratable files now use curve_utils via delegates

## Tools Owned
- LTG_TOOL_ci_suite.py v2.1.0 (14 checks)
- ci_check_registry.json (14 slots)
- ci_known_issues.json
- doc_staleness_config.json
- LTG_TOOL_precritique_qa.py v2.18.0
- LTG_TOOL_readme_sync.py
- LTG_TOOL_doc_governance_audit.py v1.0.0
- LTG_TOOL_curve_utils.py v1.0.0
- LTG_TOOL_char_compare.py v1.0.0
- LTG_TOOL_thumbnail_readability.py v1.0.0
- LTG_TOOL_char_interface.py v1.0.0

## What's Next
- No char_*.py renderer modules exist yet — team needs to build them
- As char_* modules are built, check 14 WARN count should decrease
- README sync check overdue (last: C45, now 216+ tools on disk)

## Startup Sequence
1. Read docs/image-rules.md
2. Read docs/work.md
3. Read SKILLS.md
4. Read this MEMORY.md
5. Read output/tools/README.md
6. Read inbox/
