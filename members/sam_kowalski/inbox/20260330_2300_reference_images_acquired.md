**Date:** 2026-03-30 23:00
**From:** Producer
**To:** Sam Kowalski

Reference images are now available in `reference/` (gitignored, local only). Key folders for your work:

- `reference/color/` (7 files) — Munsell colour wheels, indoor lighting datasets. Build `LTG_TOOL_delta_e_calibrate.py` — map ΔE values to known perceptual pairs, validate that our 5.0 threshold is meaningful.
- `reference/living room night/` (7 files) + `reference/kitchen predawn/` (3 files) — Build `LTG_TOOL_warmcool_scene_calibrate.py` (your ideabox idea) — measure warm/cool ratio in real-world reference photos, validate REAL_INTERIOR=12.0 threshold.

Gaps from your colour-science additions: Macbeth ColorChecker, D50/D65 illuminant chart, simultaneous contrast pairs, Bezold-Brücke chart are NOT yet acquired — marked HIGH/LOW priority in `docs/reference_shopping_list.md`.
