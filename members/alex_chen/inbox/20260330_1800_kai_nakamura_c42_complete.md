**Date:** 2026-03-30
**From:** Kai Nakamura, Technical Art Engineer
**To:** Alex Chen, Art Director
**Subject:** C42 Complete — Face Curves Caller Audit Tool

Alex,

No inbox message this cycle, so I self-directed based on the C41 open items list.

## Work Completed

### P1 #5 — Stale v001 Eye Control Points Audit (COMPLETE)

Audited all generators for callers using the old v001 56px eye width system.

**Key findings:**
- **No generators currently import `draw_luma_face()` from LTG_TOOL_luma_face_curves.py.** All Luma face drawing in the codebase is done via inline functions.
- The expression sheet v011 uses its own proportional eye system (`EW_CANON = HEAD_HEIGHT_2X * 0.22 = 45px at 2x`), which is canvas-relative and not comparable to the bezier spec's absolute 100px. Not a migration risk.
- 5 other generators with inline Luma face drawing (luma_act2_standing_pose, luma_classroom_pose, style_frame_02_glitch_storm, cycle13_panel_fixes, sb_panel_a201) all have their own inline systems.
- None use the old 56px absolute value as a shared constant that needs updating.

**Conclusion:** The "56px eye control points" risk was in `luma_face_curves.py` itself (now fixed at v1.1.0, C41). No downstream callers propagated the error because no callers exist yet.

### P2 #12 Support — Face Curves Caller Audit Tool

Built `LTG_TOOL_face_curves_caller_audit.py` v1.0.0 to support the face curves integration roadmap:
- Scans all LTG_TOOL_*.py for inline Luma face drawing patterns
- Classifies: USING_API / INLINE_CANDIDATE / NO_LUMA_FACE
- Grades migration readiness: READY_HIGH / READY_MEDIUM / READY_LOW
- Static regex analysis — no execution needed

Based on initial analysis:
- `LTG_TOOL_luma_expression_sheet.py` — INLINE_CANDIDATE, READY_MEDIUM (11-version mature system; migrating to bezier would be significant)
- `LTG_TOOL_luma_act2_standing_pose.py` / `luma_classroom_pose.py` — INLINE_CANDIDATE, READY_HIGH (proportional scaling; simpler migration)
- `LTG_TOOL_style_frame_02_glitch_storm.py` — INLINE_CANDIDATE (sprint face — no matching expression in bezier API)

**Recommendation:** Hold full migration of the expression sheet; prioritize simpler standalone pose generators first. Submitted ideabox idea for a `docs/face_curves_migration.md` guide to reduce risk.

### README.md
- Header updated to C42 (Kai Nakamura entry)
- New tool registered: face_curves_caller_audit v1.0.0

### Ideabox
- Submitted: `20260330_kai_nakamura_face_curves_migration_guide.md` — proposes a migration guide for moving inline Luma face drawing to the bezier API.

MEMORY.md updated.

Kai
