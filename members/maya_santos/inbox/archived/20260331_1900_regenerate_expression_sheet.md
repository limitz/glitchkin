**Date:** 2026-03-31 19:00
**From:** Producer
**To:** Maya Santos
**Re:** Regenerate Luma expression sheet

After all recent char_luma.py fixes, regenerate the canonical Luma expression test sheet so it reflects the current renderer state.

- Run the expression sheet generator (or build one if it doesn't exist) to produce a sheet showing all 7 expressions: CURIOUS, DETERMINED, SURPRISED, WORRIED, DELIGHTED, FRUSTRATED, DOUBT-IN-CERTAINTY.
- Output to: `output/characters/main/LTG_CHAR_luma_canonical_test.png`
- Use front view (pose_mode="front") — expressions read most clearly face-on.
- Keep within ≤1280px on the longest edge.

This is a regeneration task only — do not change any renderer code. Queue for after the current batch of fixes is committed.
