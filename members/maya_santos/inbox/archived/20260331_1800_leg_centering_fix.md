**Date:** 2026-03-31 18:00
**From:** Producer
**To:** Maya Santos
**Re:** v007 leg fix — keep legs centered in x

Human feedback on v007:

> "the legs in the turnaround should not move in the x direction. they should be centered"

The fore/aft depth stagger you added moved the legs in x (near leg at hip_cx + 0.20*head_r, far leg at hip_cx - 0.25*head_r). That's not right.

**Fix:** Legs in all pose modes stay centered at hip_cx (or symmetrically around it as they always were). Depth stagger must be implied through y-axis only — far foot gets a small y-lift to read as receding, near foot stays at ground. No x-offset on the legs themselves.

This applies to:
- `_draw_luma_threequarter()` — legs should not shift x from hip_cx
- The side view rewrite — same
- `_draw_luma_side_l()` — same

Minimal change — just remove the x-component of the leg stagger. Keep the y-lift on the far foot if it reads well; drop it if it looks wrong without the x offset.

Regenerate turnaround, send completion to Producer inbox.
