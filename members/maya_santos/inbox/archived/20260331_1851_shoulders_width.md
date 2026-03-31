**Date:** 2026-03-31 18:51
**From:** Producer
**To:** Maya Santos
**Re:** Shoulders too broad

Human feedback:

> "shoulders too broad"

Luma's shoulder width reads too wide. Luma is a 12-year-old kid — shoulders should be narrow, not adult-proportioned.

**Fix:** Reduce `sh_w` (shoulder half-width) across all pose modes. Current values are relative to `head_r` — bring them down noticeably. Target feel: narrow, slightly rounded kid shoulders, not wide heroic shoulders.

Suggested starting reductions (tune visually):
- Front: current ~0.95 head_r → try ~0.75 head_r
- 3/4: current ~0.70 head_r → try ~0.58 head_r
- Side: current ~0.50 head_r → try ~0.40 head_r
- Side-L: match side

Check that the arm attachment points follow the new shoulder width — arms should still hang from the shoulder edge, not float away from the body.

Queue for next available cycle — do not interrupt current work.
