**Date:** 2026-03-30
**From:** Morgan Walsh
**Subject:** C51 Deliverables — Bezier Library + Shapely Integration

## Summary

### P1: LTG_TOOL_curve_utils.py v1.0.0 (NEW)
Shared bezier curve utilities wrapping the `bezier` library and Shapely.

**Section 1 — Drop-in replacements (9 files can migrate):**
- `quadratic_bezier_pts()` — replaces bezier3, _bezier3
- `cubic_bezier_pts()` — replaces bezier4, cubic_bezier_pts (local)
- `cubic_bezier_single()` — replaces bezier_point
- `draw_bezier_polyline()` — replaces draw_bezier_curve
- `polyline()` — shared PIL draw convenience

**Section 2 — Advanced ops (bezier library required):**
- `arc_length()` — true arc length (not polyline approximation)
- `subdivide_at_t()` — De Casteljau subdivision
- `curve_intersections()` — find where two curves cross
- `curvature_at_t()` — curvature (1/radius) for QA kink detection
- `uniform_t_by_arclength()` / `sample_at_arclength()` — even spacing along curves

**Section 3 — Shapely silhouette ops:**
- `mask_to_polygon()` / `mask_to_polygon_cv2()` — binary mask to Shapely Polygon
- `polygon_overlap_ratio()` — geometric SOR (replaces pixel-level in silhouette_distinctiveness)
- `polygon_iou()` — intersection over union
- `simplify_outline()` — Douglas-Peucker simplification
- `outline_to_points()` — back to PIL draw coordinates
- `polygon_width_profile()` — geometric width profile (replaces per-row pixel scan)

**Section 5 — Audit:**
- `audit_hand_rolled_bezier()` — scans codebase, reports migration status per file
- CLI: `python3 LTG_TOOL_curve_utils.py --audit`

**Design:** Graceful fallback if bezier/Shapely not installed (try/except ImportError, falls back to hand-rolled math for Section 1; raises ImportError with install instructions for Sections 2-3).

### P2: Bezier Audit — 9 files with hand-rolled bezier functions

| File | Functions | Migration |
|------|-----------|-----------|
| luma_construction_prototype.py | bezier3, bezier4 | quadratic/cubic_bezier_pts |
| luma_gesture_prototype.py | bezier_point, draw_bezier_curve | cubic_bezier_single, draw_bezier_polyline |
| face_curve_validator.py | quadratic_bezier_pts, cubic_bezier_pts | import from curve_utils (same names) |
| luma_face_curves.py | _quadratic_bezier_points, _cubic_bezier_points | quadratic/cubic_bezier_pts |
| luma_expression_sheet.py | bezier3 | quadratic_bezier_pts |
| sb_cold_open_P17_chartest.py | bezier3, bezier4 | quadratic/cubic_bezier_pts |
| character_lineup.py | _bezier3 | quadratic_bezier_pts |
| grandma_miri_expression_sheet.py | bezier3 | quadratic_bezier_pts |
| rendering_comparison.py | _bezier_edge_cairo | EXEMPT (cairo ctx.curve_to, not PIL) |

**All 8 migratable files** can switch to curve_utils imports with no logic changes — the functions are API-compatible.

### P3: CI Suite — No changes needed
- `ext_model_check` was removed in C48; no check scans for library imports.
- Stub linter checks `LTG_TOOL_*` file existence, not third-party imports. curve_utils uses try/except so it passes stub lint even without bezier/Shapely installed.
- No new CI false positives expected.

### P4: docs/pil-standards.md updated
- Added bezier and Shapely to approved dependency list.
- Added "Bezier Curve Migration (C51)" section with audit instructions.

### P5: README updated
- Script Index entry for LTG_TOOL_curve_utils.py.
- C51 section with new tool + updates.

## Next Steps
- Maya, Rin, Ryo, Kai: migrate their files to import from curve_utils (8 files, ~30 min each)
- arc_length() and curvature_at_t() are ready for integration into precritique_qa as curve quality checks
- polygon_overlap_ratio() can replace pixel-level SOR in silhouette_distinctiveness for faster, resolution-independent comparison
