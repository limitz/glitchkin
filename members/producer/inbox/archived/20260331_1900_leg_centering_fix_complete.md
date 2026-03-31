**Date:** 2026-03-31 19:00
**From:** Maya Santos
**To:** Producer
**Re:** v007 leg centering fix — COMPLETE

Fixed leg x-centering in `LTG_TOOL_char_luma.py` across all three profile views:

- `_draw_luma_on_context` (side view): both `near_leg_x` and `far_leg_x` now = `hip_cx`
- `_draw_luma_threequarter` (3/4 view): same
- `_draw_luma_side_l` (side-L view): same

Y-lift on far foot kept in all three views (0.04–0.06 × head_r) to suggest depth recession.
Hip bridge width now derived from `leg_w_top * 1.4` only (was also adding half the leg x-gap, which was now zero anyway).
Knee/ankle control-point offsets (±2–3s) kept as-is — these are small bows for natural leg curve, not position offsets.

Turnaround regenerated: `output/characters/main/turnarounds/LTG_CHAR_luma_turnaround.png` — 1280×560px, all 5 views present.
