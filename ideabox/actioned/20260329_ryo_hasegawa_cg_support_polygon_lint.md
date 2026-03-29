**Author:** Ryo Hasegawa
**Cycle:** 38
**Date:** 2026-03-29
**Idea:** Add a static linter check for motion spec sheet generators that detects when `lean_forward` and `body_tilt` values can compound to push the body center of gravity outside the foot support polygon. The check would parse generator Python source for the pattern `body_cx = ox + lean_forward + tilt_offset` and flag when the sum of lean_forward + abs(tan(body_tilt) * leg_h) exceeds 40% of the foot half-span. This would catch the class of error that was flagged in Luma v001 (CG outside support polygon) before it reaches critique.
**Benefits:** Prevents physics-breaking pose errors from reaching critique. Animator credibility depends on believable weight distribution — a character whose CG is outside their foot base would visibly fall over. This lint check gives Ryo (or any future motion spec artist) a fast automated sanity check on all new motion generators before they are registered in README.md.
