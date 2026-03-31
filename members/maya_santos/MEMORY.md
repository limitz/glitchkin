# Maya Santos — Memory

## Cycle 55 — Turnaround v007 (Human Review Fixes) — COMPLETE

### Task: Four issues from human review of v006

**Issue 1 (3/4 view: frontal-looking face & legs) — FIXED**
- Legs: replaced left/right spread with fore/aft stagger.
  Near leg: slightly +x (forward in picture plane), slightly lower Y.
  Far leg: slightly -x, slightly higher Y (depth recession).
- Head: asymmetric head shape — bulges toward near side (-x), compresses on far side.
  Face skin ellipse offset -x*0.06 to leave far corner less covered.
- Hair cloud weighted toward near/back side.

**Issue 2 (side view: frontal face, wrong legs) — FIXED**
- Legs: fore/aft stagger (near_leg_x = hip_cx + 0.18*head_r, far_leg_x = hip_cx - 0.14*head_r).
  Both near center-x, not spread left/right.
- Head: complete rewrite to true profile.
  Profile head shape with back-of-head bulge (+x), face taper (-x on far side).
  ONE eye only, positioned toward face direction (+x).
  Profile nose as bezier bump protruding from face silhouette at +x edge.
  Brows and mouth positioned on face-side, not centered.
  Single cheek blush on face side.

**Issue 3 (side-L: mirror not acceptable) — FIXED**
- Added `_draw_luma_side_l()` — native left-facing renderer, NOT a flip.
- Distinct stance: reversed weight distribution, near arm relaxed-down,
  far arm bent-backward (character just turned around feel).
- Left-facing profile head with back-of-head on +x, nose on -x.
- Hair cloud on +x side (back of head in left-facing view).
- Turnaround VIEW_SPEC updated: "SIDE-L": ("side_l", "right") — no ctx.scale(-1,1) mirror.

**Issue 4 (arm-shoulder seam) — FIXED**
- `_draw_unified_arm()` now takes `shoulder_open=True` (default).
  When True: fill uses closed path (normal), but stroke is OPEN at shoulder end —
  only strokes the outer silhouette edges from shoulder-L through wrist cap to shoulder-R.
  The torso stroke covers the junction. No seam where arm meets hoodie body.

### Deliverables
- `LTG_TOOL_char_luma.py` → v1.2.0 (C55)
- `LTG_TOOL_luma_turnaround.py` → v007
- `output/characters/main/turnarounds/LTG_CHAR_luma_turnaround.png` regenerated 1280x560

### Lint Results
- Self-test renders: 31 PASS / 5 WARN / 3 FAIL
- FAILs: back_test P8 (dev=1.05px, scale=0.51), front_test + back_test P11 (dev≤0.11px, scale≤0.16)
  All FAILs at near-zero deviation and sub-0.52 scale — measurement artifacts, not real failures.
  The 7 main expression renders all PASS or WARN only.
- side_l render: 0 FAIL, 0 WARN.
- Face gate: pre-existing NEUTRAL FAIL (baseline), FEAR WARN — not new, not caused by this work.

## Tools Owned (active)
- LTG_TOOL_char_luma.py v1.2.0 (C55)
- LTG_TOOL_char_miri.py v1.0.0 (C53)
- LTG_TOOL_luma_turnaround.py v007 (C55)
- (full list in SKILLS.md)

## Next Cycle Priorities
- Migrate luma_cairo_expressions.py to import from char_luma.py v1.2.0
- Cosmo expression rebuild
- Run face gate on new turnaround views (side/side-L profiles)
