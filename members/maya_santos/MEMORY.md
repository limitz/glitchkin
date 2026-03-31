# Maya Santos — Memory

## Cycle 60 — Arm draw order + pants/torso join — COMPLETE

### Tasks from inbox (both archived from C59)

**Bug 1 — Arm draw order wrong in all profile/3q views**
- Root cause: near arm drawn first, far arm drawn on top — reversed
- Fix: swapped draw order in all 3 inline arm sections:
  - `_draw_luma_on_context` (side-R): far arm first, near arm last
  - `_draw_luma_threequarter` (3/4): far arm first, near arm last
  - `_draw_luma_side_l` (side-L): far arm first, near arm last
- Front view: symmetric, left arm drawn first (fine as-is per spec)
- Back view: arms not near/far in the same way (not affected)

**Bug 2 — Pants top not connecting to torso (gap visible)**
- Root cause: `hip_bridge_y_top = torso_bot_y - torso_h * 0.04` but
  `hem_y = torso_bot_y - torso_h * 0.10` — 6% of torso_h gap
- Fix: Changed ALL 5 view functions to
  `hip_bridge_y_top = torso_bot_y - torso_h * 0.10`
  so bridge top aligns exactly with hem_y
- Affected: side-R, front, 3/4, back, side-L

**Test:** char_module_test PASS (7/7 Luma expressions). Turnaround regenerated.
**Version:** `LTG_TOOL_char_luma.py` v1.3.0

**Deliverables:**
- `LTG_TOOL_char_luma.py` — updated in-place (v1.3.0)
- `output/characters/main/turnarounds/LTG_CHAR_luma_turnaround.png` — regenerated (1280x560)

## Cycle 59 — Leg fixes (3/4 spread + side centering) — COMPLETE

**Bug 1 — 3/4 view: both legs at same X (looked like side view)**
- Fix: Added `leg_offset_3q = head_r * 0.40 * 0.62 * stance_mult`

**Bug 2 — Side views (side-R and side-L): legs offset from canvas center**
- Fix: Changed both to `cx` (canvas center) in both side functions

**Test:** All 21 combos (7 expressions × 3 views) PASS.

## Ongoing Notes
- Cosmo module test is FAIL (pre-existing) — Alex Chen notified C58, note still in inbox
- No new tasks in inbox this cycle (both tasks were already in archived from C59)

## Tools Owned (active)
- LTG_TOOL_char_luma.py v1.3.0 (C60 arm order + pants join)
- LTG_TOOL_char_miri.py v1.0.0 (C53)
- LTG_TOOL_luma_turnaround.py v007 (C55)
- (full list in SKILLS.md)
