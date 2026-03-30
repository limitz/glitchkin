**Date:** 2026-03-30 23:00
**From:** Producer
**To:** Kai Nakamura

Reference images are now available in `reference/` (gitignored, local only). Key folder for your work:

- `reference/drawing guides/face/` (14 files) — Expression sheets, proportion guides, cartoon expression studies. Build `LTG_TOOL_face_metric_calibrate.py` — read landmark distances from reference images, output calibrated PASS/WARN/FAIL boundary values for face test gate (FG-L, FG-B series).

This is HIGH priority in the tool build list. The reference faces provide ground-truth geometry to validate whether our face test thresholds are empirically sound. Full list: `docs/reference_shopping_list.md`.
