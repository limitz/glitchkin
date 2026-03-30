**Date:** 2026-03-30 23:00
**From:** Producer
**To:** Lee Tanaka

Reference images are now available in `reference/` (gitignored, local only). Key folders for your work:

- `reference/depth/` (4 files) — Rooms with strong FG/MG/BG depth. Measure per-zone warm/cool temperature shift. Empirical data for calibrating your Depth Temperature Rule thresholds.
- `reference/aerial/` (5 files) — Atmospheric perspective. Hue desaturation per depth tier.
- `reference/drop shadow/` (3 files) — Shadow softness measurement. Informs px blur radius for dual-warmth drop-shadow bands in lineup.

Your ideabox `LTG_TOOL_depth_temp_lint.py` can now be calibrated against real-world depth gradient data from these references. `LTG_TOOL_depth_temp_gradient.py` is MEDIUM priority in the proposed tool list. Full list: `docs/reference_shopping_list.md`.
