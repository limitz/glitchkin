**Date:** 2026-03-31 18:41
**From:** Producer
**To:** Maya Santos
**Re:** Pants top not connecting to torso

Human feedback:

> "top of pants not connecting correctly to torso"

The waistband/top of pants is visibly separated or misaligned from the hoodie hem in some views.

**Fix:** The pants top (hip bridge + leg tops) must meet the hoodie hem with no gap and no overlap. Check each view:

- The hoodie hem y-position (`hem_y`) and the pants hip bridge top (`hip_bridge_y_top`) should be at the same y, or the bridge should slightly overlap (1–2px) into the hoodie hem — never below it with a visible gap.
- The leg tops (`torso_bot_y - leg_overlap`) must start at or slightly above `torso_bot_y`, which should match `hem_y` closely.
- In 3/4 and side views the torso is narrower — make sure the hip bridge width matches the narrowed torso bottom, not the full front-view width.

Check all pose modes where the connection is visible (front, side, side_l, 3/4). Fix the y-values and widths so the join is seamless.

Queue for next available cycle — do not interrupt current work.
