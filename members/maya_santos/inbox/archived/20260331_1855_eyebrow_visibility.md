**Date:** 2026-03-31 18:55
**From:** Producer
**To:** Maya Santos
**Re:** Eyebrows hidden inside hair

Human feedback:

> "eyebrows inside hair, not visible in front, only somewhat in 3/4"

The eyebrows are being drawn behind/under the hair blobs and aren't visible. They need to sit on the face, below the hairline.

**Fix:**
- **Draw order:** Eyebrows must be drawn AFTER the hair, not before. Currently the hair blobs overdraw the brows. Move brow drawing to after the hair pass in all affected renderers.
- **Position:** Brows sit on the forehead, clearly below the hairline. The hairline should be above the brows — if brows are currently at a Y position that puts them inside the hair mass, lower the hair blobs or raise the brow Y until they sit visibly on the forehead skin.
- **Front view:** Both brows should be fully visible — they're a key expression signal. Check that brow Y is in the upper forehead area, below where the hair blobs terminate.
- **3/4 view:** Near brow fully visible, far brow partially visible (foreshortened) — both should read.
- **Side view:** One brow visible on the face side, just above the eye.

The fix is likely two things: (1) move brow draw calls to after hair, (2) adjust brow Y so they sit below the hairline in all views.

Queue for next available cycle — do not interrupt current work.
