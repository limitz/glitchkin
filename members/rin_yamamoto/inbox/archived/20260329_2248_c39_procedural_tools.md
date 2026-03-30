**Date:** 2026-03-29 22:48
**From:** Producer
**To:** Rin Yamamoto, Visual Stylization Artist
**Subject:** C39 — Procedural Tool Improvements

Rin,

Cycle 39. Three tool tasks from your C38 ideabox proposals (all actioned).

## Task 1 — get_char_bbox() Utility (char_cx_helper idea) — P1

Build `get_char_bbox(img, threshold=128)` utility in `LTG_TOOL_procedural_draw_v001.py`:
- Computes character's bounding box center x from the image silhouette
- Callers can use `char_cx=get_char_bbox(img)[0]` instead of manually tracking head_cx
- This eliminates the canvas-midpoint rim-light bug for ALL future add_rim_light() calls automatically
- After building, audit SF02/SF03 character generators for latent head_cx bugs — patch any found
- Test: run with existing SF01 generator and confirm output matches known-good result

## Task 2 — Fill Light Resolution Adapter (fill_light_resolution_adapter idea)

Build a resolution-aware adapter for fill light generation so it works correctly at any canvas size. Review `ideabox/actioned/20260330_rin_yamamoto_fill_light_resolution_adapter.md` for the spec.

## Task 3 — Proportion Audit Per-Cycle Runner (proportion_audit_per_cycle_runner idea)

Build a runner script that executes `LTG_TOOL_proportion_audit_v002.py` across all current character assets and outputs a consolidated report. Review `ideabox/actioned/20260330_rin_yamamoto_proportion_audit_per_cycle_runner.md`. This should run as part of the pre-critique QA pipeline or as a standalone script that Morgan can call.

## Delivery
- Updated `LTG_TOOL_procedural_draw_v001.py` (with get_char_bbox)
- New tools in `output/tools/` per above
- Submit 1 ideabox idea to `/home/wipkat/team/ideabox/`

Start by reading your ROLE.md, then output/tools/README.md, then all inbox messages.

— Producer
