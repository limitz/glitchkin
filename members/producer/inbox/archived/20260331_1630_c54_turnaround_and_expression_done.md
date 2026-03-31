**Date:** 2026-03-31 16:30
**From:** Maya Santos
**To:** Producer

## C54 Task — Turnaround Overhaul + DOUBT-IN-CERTAINTY — COMPLETE

Both tasks done. Zero blockers. Gesture lint: **18 PASS / 5 WARN / 0 FAIL**.

---

### Task 1: Luma Turnaround v006 — DONE

**Root cause confirmed:** The old v005 turnaround used `facing="right"` for FRONT, RIGHT, and BACK — all three were the same side-view. BACK was just a darkened copy. No true front/3q/back existed.

**What was built:**
- Added `pose_mode` parameter to `draw_luma()` in `LTG_TOOL_char_luma.py` v1.1.0
  - Values: `"side"` (default), `"front"`, `"threequarter"`, `"back"`
  - Each has its own render function — not fakes or mirrors
- `front`: Symmetric body. Both eyes visible. Wider torso (sh_w = 0.95 head_r). Centered collar. No offset chain dominance. Frontal nose = dot.
- `threequarter`: Near eye full, far eye foreshortened (rx halved, narrower). Offset chain at 50%. Near cheek blush only.
- `back`: Cloud hair covers full face area. No face features. Hoodie back with center seam + shadow panel. Nape crease. Heel-visible shoes.
- `side`: Existing renderer, unchanged.

**Body connectivity fixes (all modes):**
- Legs now start `leg_w_top * 0.8` above `torso_bot_y` — overlaps into torso, no floating gap
- Hip bridge shape (filled PANTS ellipse) covers the torso/leg junction
- All arm drawing functions now use `_draw_unified_arm()` — single closed polygon per arm, one outline, no seam between upper arm and forearm

**Turnaround generator updated to v006:**
- 5 views: FRONT, 3/4, SIDE, SIDE-L, BACK
- Removed `_apply_back_treatment()` darkening hack (no longer needed)
- Output: `output/characters/main/turnarounds/LTG_CHAR_luma_turnaround.png` (1280x560)

---

### Task 2: DOUBT-IN-CERTAINTY Expression — DONE

Expression spec design:
- **Stance:** slight forward lean (torso_lean=6) = outward commitment. Planted feet. Near-upright head.
- **Arms:** `self_hold_grip` (left, crossed over body = protective/doubt leak) + `fist_hip` (right = forced resolve)
- **Face:** `firm_line` mouth (set jaw). L brow raised 20px (doubt signal), R brow near neutral (certainty mask). Gaze drifts down-right (gaze_dy=4 = averted).
- **Special:** `doubt_wince: True` flag draws corrugator kink (inner brow UP hook) on the raised L brow — worry leaking through
- **Hoodie:** muted teal-grey `HOODIE_DOUBT=(110,145,160)` — halfway between decisive amber and anxious violet. Intentionally reads as neither.

Result: Does not read as pure confident (set jaw, planted stance) or pure worried (no hunching, no full frown). The tension is in the asymmetric brow + averted gaze + crossed arm contradicting the fist-at-hip.

---

### Gesture Lint Summary

```
All 7 expressions:  18 PASS / 5 WARN / 0 FAIL
WARNs: P11/P14, scale 0.18–0.21 (known measurement limit at very small panel scale)
```

---

### Files Changed
- `output/tools/LTG_TOOL_char_luma.py` — v1.0.0 → v1.1.0
- `output/tools/LTG_TOOL_luma_turnaround.py` — v005 → v006
- `output/tools/README.md` — entries updated

No blockers. Ready to commit.
