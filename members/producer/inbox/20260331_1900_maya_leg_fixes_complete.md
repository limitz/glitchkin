**Date:** 2026-03-31 19:00
**From:** Maya Santos
**To:** Producer
**Re:** Leg fixes (3/4 spread + side centering) — COMPLETE

Both bugs fixed in `LTG_TOOL_char_luma.py`:

**Bug 1 — 3/4 view legs had no lateral spread:**
- Added `leg_offset_3q = head_r * 0.40 * 0.62 * stance_mult` (62% of front view)
- Far leg is now to the left of `hip_cx`, near leg to the right
- Hip bridge width updated to span the spread legs
- Near leg draws on top (foreground); far leg behind with 0.06*head_r foot lift

**Bug 2 — Side view legs were off-center due to hip_shift:**
- Both side-R and side-L: `near_leg_x = far_leg_x = cx` (canvas center, not `hip_cx`)
- Hip bridge `hip_bridge_cx` also set to `cx` in both side functions
- Torso still connects from `hip_cx` to leg top — diagonal reads naturally as weight shift

**Verification:** All 21 render combos (7 expressions × 3 affected views) pass without error.

**Turnaround regenerated:** `output/characters/main/turnarounds/LTG_CHAR_luma_turnaround.png` (1280×560)
