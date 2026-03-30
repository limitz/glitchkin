**Author:** Jordan Reed
**Cycle:** 47
**Date:** 2026-03-30
**Idea:** Add an automated sight-line validation step to precritique_qa that runs `LTG_TOOL_sight_line_diagnostic.py` on every style frame containing character-to-target gaze geometry. Each style frame generator would export a `SIGHT_LINE_SPEC` dict (eye_xy, aim_xy, target_xy) at module level, and precritique_qa would import it and run the diagnostic automatically. This catches sight-line regressions (like the SF01 horizontal-only pupil shift) before they reach critics, instead of relying on Ingrid to flag them cycle after cycle.
**Benefits:** Lee Tanaka (staging QA automated), Rin Yamamoto (SF generators validated on every run), Ingrid Svensson (stops having to repeat the same critique). Prevents persistent regressions from reaching critique cycles. Reuses the existing diagnostic tool — no new code needed, just plumbing.
