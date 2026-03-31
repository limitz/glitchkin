# Morgan Walsh — Memory

## Project
Luma & the Glitchkin. Comedy-adventure cartoon.

## Joined
C34 (first active cycle).

## Recent Work (C51-C52)
### C52
- CI Suite v2.0.0: 3 new checks (dep_availability, bezier_migration_lint, tool_naming_lint)
- Bezier migration batch 1: 4 files migrated (1 full, 3 partial delegate wrappers)
- precritique_qa already at v3.0.0 by Kai (no action needed)

### C51
- LTG_TOOL_curve_utils.py v1.0.0: shared bezier library (drop-in replacements + advanced ops + Shapely polygon ops + codebase audit)
- 9 files identified for bezier migration, 8 migratable
- docs/pil-standards.md updated with bezier + Shapely

## Bezier Migration Status (C52)
- 1 MIGRATED: face_curve_validator
- 3 PARTIAL: luma_face_curves, character_lineup, luma_expression_sheet (delegate wrappers)
- 4 NOT_MIGRATED: luma_construction_prototype, luma_gesture_prototype, sb_cold_open_P17_chartest, grandma_miri_expression_sheet
- 1 EXEMPT: rendering_comparison (cairo)

## What's Next
- Complete bezier migration for remaining 4 NOT_MIGRATED files
- README sync check (last: C45, 139 tools)

## Startup Sequence
1. Read docs/image-rules.md
2. Read docs/work.md
3. Read docs/ideabox.md
4. Read docs/asset-status.md
5. Read PROFILE.md
6. Read SKILLS.md
7. Read this MEMORY.md
8. Read output/tools/README.md
9. Read inbox/
10. Read ROLE.md if present
