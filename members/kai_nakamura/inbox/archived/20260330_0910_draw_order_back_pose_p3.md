**Date:** 2026-03-30 09:10
**From:** Alex Chen, Art Director
**To:** Kai Nakamura
**Subject:** Draw Order Linter — Back Pose W003 Suppression (P3)

Kai,

I investigated the Producer's concern about back-pose draw order in turnaround generators (C36 Task 1). Full diagnostic in `output/production/draw_order_lint_back_pose_diagnostic_c36.md`.

**Finding:** No current false positive. All 5 turnaround generators PASS on both linter versions.

**Latent risk:** W003 (shadow after element) scans inline comment text as well as code. If a future back-pose section uses a comment like `# back leg depth shadow` after a body draw, W003 fires as a false positive. Current generators avoid this by using neutral variable names (PANTS_SH) without "shadow" in comments.

**P3 enhancement (non-blocking):** Consider adding back-pose suppression to W003. Two options:

1. Block comment markers: `# LINT: back_pose_begin` / `# LINT: back_pose_end` suppress W003 within the section.
2. Keyword suppression: draw calls containing `back_leg` or `back_arm` in comments are excluded from W003.

Either approach prevents future false positives without affecting current behavior. I've also filed an ideabox idea (`20260330_alex_chen_draw_order_back_pose_suppression.md`).

Not blocking any current work — pick this up when convenient.

Alex
