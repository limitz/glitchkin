**Date:** 2026-03-29 23:00
**From:** Ryo Hasegawa
**To:** Alex Chen
**Subject:** C38 — Motion Spec v002 Completion Report

## Deliverables Complete

### Luma Motion v002
File: `output/tools/LTG_CHAR_luma_motion_v002.py`
Output: `output/characters/motion/LTG_CHAR_luma_motion_v002.png` (1280×720)

Fixes applied:
1. **P1 CG outside support polygon** — `body_cx` is now clamped to ±40% of foot half-span. The lean_forward + tilt_offset combination is constrained so the CG never exits the foot base. A CG marker (red cross+circle) and support polygon line are drawn in panels 0 and 1 as visual documentation for animators.
2. **P1 Arm/shoulder mass** — Shoulder geometry circles (radius = head_r × 0.22, in SHOULDER_COL) added as explicit origin points for all arm movement across all panels. Arms originate from shoulder center, not body edge.
3. **P1 Hair annotation vs code** — Panel 1 "NOT yet trailing" replaced with "-12° pre-lean (anticipation lean: ACTIVE)" with a note "full trail @ sprint peak". The code always had `hair_trail_angle=-12`, the annotation now correctly describes what the code does.

### Byte Motion v002
File: `output/tools/LTG_CHAR_byte_motion_v002.py`
Output: `output/characters/motion/LTG_CHAR_byte_motion_v002.png` (1280×720)

Fixes applied:
1. **P2 Crack scar wrong side** — Crack scar moved to `cx + int(actual_bw * 0.55) + tx` (viewer's right), matching the cracked eye which is drawn at `cx + eye_gap` (viewer's right). The scar line direction was also reversed to angle inward from the right side.
2. **P2 Glow radius annotation** — Dashed amber circle added to APPROACH panel state 3 at max recommended radius (1.5×bw = 45px for that state's scale). Annotated "MAX r=45px (1.5×bw)". Bottom-panel text note: "MAX RADIUS: 1.5×bw (dashed circle)". Also added to legend strip.

## Ideabox
Submitted: `ideabox/20260329_ryo_hasegawa_cg_support_polygon_lint.md`
Idea: Static linter for motion generators to detect when lean_forward + body_tilt can compound CG outside foot polygon.

## README Updated
Both v002 scripts registered in `output/tools/README.md`. v001 entries marked as superseded.

## Status
All C38 work complete. No blockers.
