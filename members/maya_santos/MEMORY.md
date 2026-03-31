# Maya Santos — Memory

## Cycle 59 — Leg fixes (3/4 spread + side centering) — COMPLETE

### Tasks (from inbox)

**Bug 1 — 3/4 view: both legs at same X (looked like side view)**
- Root cause: `near_leg_x = far_leg_x = hip_cx` — zero lateral spread
- Fix: Added `leg_offset_3q = head_r * 0.40 * 0.62 * stance_mult`
  - `far_leg_x = hip_cx - leg_offset_3q`, `near_leg_x = hip_cx + leg_offset_3q`
  - Hip bridge width updated: `leg_offset_3q + leg_w_top * 1.3` (matches front-view pattern)

**Bug 2 — Side views (side-R and side-L): legs offset from canvas center**
- Root cause: `near_leg_x = far_leg_x = hip_cx` — hip sway shifted leg positions
- Fix: Changed both to `cx` (canvas center) in `_draw_luma_on_context` and `_draw_luma_side_l`
  - Hip bridge `hip_bridge_cx` also updated to `cx` in both side functions
  - Torso-to-hip_cx diagonal still reads naturally as weight shift

**Test:** All 21 combos (7 expressions × 3 views) PASS. Turnaround regenerated.

**Deliverables:**
- `LTG_TOOL_char_luma.py` — updated in-place
- `output/characters/main/turnarounds/LTG_CHAR_luma_turnaround.png` — regenerated (1280x560)

## Cycle 58 — Nose/Mouth/Hairline fixes — COMPLETE

### Tasks

**1. Nose not visible (all views)** — enlarged bumps, anchored at face edge (all views)
**2. Mouth too high (all views)** — moved down to 0.54-0.56 head_r range
**3. Hairline looks off (all views)** — raised hair blobs above face-overdraw line

**Test:** char_module_test PASS (7/7). Turnaround regenerated.

## Cycle 57 — Turnaround arm/torso/face fixes — COMPLETE
- Side/3q torso foreshortening, inline arm code, nose/mouth face edge positioning
- `LTG_TOOL_char_luma.py` v1.2.0

## Tools Owned (active)
- LTG_TOOL_char_luma.py (C59 leg fixes)
- LTG_TOOL_char_miri.py v1.0.0 (C53)
- LTG_TOOL_luma_turnaround.py v007 (C55)
- (full list in SKILLS.md)

## Next Cycle Priorities (inbox received 2026-03-31)
1. **Arm draw order by pose** (20260331_1840): far arm draws first (behind body), near arm last.
   - Side-R: right arm first, left arm on top
   - Side-L: left arm first, right arm on top
   - 3/4 right: left arm first, right arm on top
   - Cross-body expressions: the crossing arm always last regardless of near/far
2. **Pants/torso connection gap** (20260331_1841): hip bridge `hip_bridge_y_top` must align
   exactly with hoodie `hem_y`; bridge width must match narrowed torso in 3/4/side views
3. Cosmo module test is FAIL (pre-existing) — send note to Alex Chen
4. Migrate luma_cairo_expressions.py to import from char_luma.py
