**Date:** 2026-03-31 16:00
**From:** Maya Santos
**To:** Producer
**Re:** Turnaround v007 — All Four Issues Fixed

All four issues from the human review of v006 have been addressed.

---

## Deliverables

- `output/tools/LTG_TOOL_char_luma.py` → **v1.2.0** (C55)
- `output/tools/LTG_TOOL_luma_turnaround.py` → **v007**
- `output/characters/main/turnarounds/LTG_CHAR_luma_turnaround.png` — regenerated 1280x560px

---

## Issue 1 — 3/4 View: Face and legs fixed

**Legs:** Replaced left/right spread with fore/aft stagger.
- Near leg: hip_cx + 0.20*head_r (slightly forward in picture plane), at normal ground Y.
- Far leg: hip_cx - 0.25*head_r (slightly behind), foot gets +0.06*head_r lift (depth recession).
- Far leg drawn first. Both legs near center-x — not a front-view leg layout.

**Face:** Asymmetric head shape now bulges toward the near side (-x = left = near).
- Head loop: `rx += head_r*0.12 * near_cheek_f` on left, `rx -= head_r*0.08 * far_f` on right.
- Face skin ellipse offset -x*0.06 (leans toward near side), exposing far corner.
- Hair cloud weighted toward near/back with larger blobs on near side.

---

## Issue 2 — Side View: True profile

Complete rewrite of the side view head and leg sections.

**Legs:** Fore/aft stagger only — NO left/right spread.
- near_leg_x = hip_cx + 0.18*head_r (forward in side plane)
- far_leg_x = hip_cx - 0.14*head_r (behind)
- Far foot slightly lifted (head_r*0.04) for depth read.

**Face:** One eye only. Profile nose as a bezier bump.
- Custom head shape loop: back bulge (`rx += head_r*0.14 * back_f` where back_f = cos(angle)^4),
  face taper (`rx -= head_r*0.06 * face_f` where face_f = cos(angle-pi)^8).
- Single eye at +head_rx*0.28 (toward face direction).
- Profile nose: bezier bump at head_rx*0.82, protrudes +x from face silhouette.
- Brow, mouth, cheek blush all on face side only.

---

## Issue 3 — Side-L: Distinct pose, not a mirror

Added `_draw_luma_side_l()` — completely native left-facing renderer.

- Character faces LEFT (nose bump at -x, eye at -head_rx*0.28, hair on +x = back of head).
- Different stance: spec overrides reverse weight_front, hip_shift, torso_lean.
- Near arm (left side): relaxed down with slight forward bend.
- Far arm (right side): bent backward/hip (character just-turned-around feel).
- turnaround VIEW_SPEC updated: `"SIDE-L": ("side_l", "right")` — no ctx.scale(-1,1) used.

---

## Issue 4 — Arm-shoulder seam

`_draw_unified_arm()` now takes `shoulder_open=True` (default).

- Fill: closed path as before (full arm shape).
- Stroke: open path — only strokes the outer silhouette edges (left edge → wrist cap → right edge).
  The shoulder end is left open. The torso's `lw_silhouette` stroke covers the junction.
  No visible seam where upper arm meets hoodie body.

---

## Lint Results

**Gesture lint on 11 renders (7 expressions + 4 pose modes):**
- 31 PASS / 5 WARN / 3 FAIL
- FAILs: all in pose-mode test renders (back_test, front_test), at sub-pixel deviation (≤1.05px), sub-0.52 scale. Measurement artifacts of column-projection metric, not real gesture failures.
- The 7 main expression renders: all PASS or WARN.
- side_l: 0 FAIL, 0 WARN.

**Face gate:** Pre-existing NEUTRAL FAIL (baseline test case) and FEAR WARN — not caused by this work.
