# Maya Santos — Memory

## Cycle 62 — Three structural bugs fixed — COMPLETE

### 3 fixes from inbox (archived):

**Bug 1 — Pants/torso mismatch**
- Root cause: `hip_bridge_y_top = torso_bot_y - torso_h * 0.10` was trying to align
  with hem_y via math, creating an unreliable seam.
- Fix: Changed `hip_bridge_y_top = torso_bot_y` in ALL 5 views (side, front, 3q, back, side_l).
  Hoodie torso fill (drawn after hip bridge) now naturally covers the junction. No gap math needed.

**Bug 2 — Arm draw order: 3/4 and side-L wrong**
- 3/4 view (right-facing): character's LEFT side faces viewer. `ls_pt` = near arm.
  Was: far=ls_pt first, near=rs_pt last (WRONG). Fixed: far=rs_pt first, near=ls_pt last.
  Arm geometry offsets mirrored to match new attachment points (+x for far, -x for near).
- Side-L (left-facing): character's RIGHT arm is near viewer (canvas-left side = face direction).
  Was: far=ls_pt first, near=rs_pt last (WRONG). Fixed: far=rs_pt first, near=ls_pt last.
  Arm geometry offsets mirrored accordingly.
- Side-R: ALREADY CORRECT — no change.

**Bug 3 — 3/4 near/far leg labels reversed**
- Was: `fl_x = hip_cx - leg_offset_3q` labeled "far", `fr_x` labeled "near" — WRONG.
- Fix: `fl_x` (canvas-left, character's LEFT) = near; `fr_x` (canvas-right) = far.
  `near_leg_x = fl_x`, `far_leg_x = fr_x`.
  Draw order: far leg (fr_x) first, near leg (fl_x) last — unchanged variable references,
  just assignments corrected.

**Test:** char_module_test PASS (7/7 Luma). Turnaround + canonical test regenerated.
**Version:** LTG_TOOL_char_luma.py v1.5.0

**Deliverables:**
- `output/tools/LTG_TOOL_char_luma.py` v1.5.0 (in-place)
- `output/characters/main/turnarounds/LTG_CHAR_luma_turnaround.png` — regenerated
- `output/characters/main/LTG_CHAR_luma_canonical_test.png` — regenerated

## Cycle 61 — Human feedback head/body polish — COMPLETE

6 fixes: shoulders, hair ear taper, neck-face blend, brow ridge, nose free-edge, eyebrow draw order.
v1.4.0

## Cycle 60 — Arm draw order + pants/torso join — COMPLETE
v1.3.0

## Ongoing Notes
- Cosmo module test is FAIL (pre-existing, noted for Alex Chen)

## Tools Owned (active)
- LTG_TOOL_char_luma.py v1.5.0 (C62 hip seam + arm order + 3q leg fix)
- LTG_TOOL_char_miri.py v1.0.0 (C53)
- LTG_TOOL_luma_turnaround.py v007 (C55)
- (full list in SKILLS.md)
