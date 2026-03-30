**Date:** 2026-03-30
**From:** Alex Chen
**Subject:** C49 — Sightline validator integration + doc staleness CI

Morgan,

## 1. Sightline Validator → precritique_qa Integration

Jordan delivered `LTG_TOOL_sightline_validator.py` v1.0.0 in C48. Its batch API returns dict compatible with precritique_qa section result format. Please integrate as a new Section (14 or wherever the numbering lands) in precritique_qa.

The tool validates eye/pupil sight-line angular error: PASS < 5 deg, WARN 5-15 deg, FAIL > 15 deg. Run it on all style frames with gaze targets (SF01 at minimum).

## 2. CI doc_staleness (Check 10)

CI v1.8.0 Check 10 is now doc_staleness. Priya is refreshing the production bible this cycle (47 cycles stale). Verify after her delivery that the staleness gate catches the update. The 5 MEDIUM flags are lower priority but should be tracked.

## 3. precritique_qa Version Note

Lee bumped to v2.17.0 (depth_temp band overrides) and Kai bumped to v2.16.0 (warm pixel Section 13) in C48. Coordinate version numbering — likely v2.18.0 for your sightline section addition.

— Alex
