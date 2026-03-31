**Date:** 2026-03-31 19:00
**From:** Maya Santos
**To:** Producer
**Re:** Luma face fixes complete (C58) — nose, mouth, hairline

All three human-feedback items resolved in `LTG_TOOL_char_luma.py`. Turnaround regenerated.

**1. Nose visibility — FIXED**
- Front: 2.5px dot → upturned nose arc + two nostril dots. Now clearly reads as a nose.
- Side-R: Nose bump peak protrusion increased from 18s to 24s at 2x. Larger filled bezier shape.
- Side-L: Nose anchor moved from -head_rx*0.82 to -head_rx*0.94 (now anchored at face edge, matching side-R). Control points enlarged to match.
- 3/4: Tiny 5px curve → visible 9s-wide arc + near-side nostril dot.

**2. Mouth position — FIXED (all views)**
- All views pushed down to lower third of face: front/3q at head_r*0.56, side/side-L at head_r*0.54.
- Previous values were 0.42–0.44 (too high, near mid-face).
- Side-L mouth_x_base also corrected from -0.30 to -0.62 (face-edge position, matching side-R logic).

**3. Hairline — FIXED (all views)**
- Root cause: large hair blobs with centers at by=-0.45 (front/3q) were extending into the face area; face skin overdraw created an unnatural flat cut.
- Fix: Blob centers raised to by=-0.58 or higher for the low-center blobs; blob heights reduced slightly. Side blobs raised from by=-0.30 to by=-0.42.
- Side-R/L: center-forward blob at (0.20/-0.20, -0.70) pulled back to (0.10/-0.10, -0.75) with smaller radius to keep it above hairline.

**Test result:** char_module_test PASS (7/7 Luma expressions, 0 failures).

**Output:** `output/characters/main/turnarounds/LTG_CHAR_luma_turnaround.png` (1280×560px, 5 views)

**Side note:** Cosmo module test has a pre-existing FAIL (not caused by C58). Flagging for Alex Chen.
