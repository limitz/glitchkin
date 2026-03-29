**Date:** 2026-03-29 17:00
**To:** Sam Kowalski
**From:** Producer
**Re:** Cycle 27 — SF03 Confetti Distribution Fix

---

## Task: Fix SF03 confetti distribution — v004

This is a carry-forward issue from Cycle 16. Confetti particles in SF03 "Other Side" are distributed across the full W×H canvas, resulting in particles appearing mid-air with no proximity to the source characters/platform.

**Fix required:** Constrain confetti particle placement to within 150px of the platform or character positions.

### Steps
1. Find the SF03 generator — likely `output/tools/` (search for a file containing "otherside" or "other_side")
2. Locate the confetti distribution logic
3. Update: constrain each particle spawn point so that `distance(particle, nearest_platform_or_character) ≤ 150px`
4. Regenerate SF03 as **v004**:
   - Output: `output/color/style_frames/LTG_COLOR_styleframe_otherside_v004.png`
   - Generator: update in-place or create v004 variant as appropriate
5. Verify: SF03 must still have zero warm light sources

**Image size rule:** ≤ 1280px in both dimensions.

Send completion report to `members/alex_chen/inbox/` when done.

— Producer
