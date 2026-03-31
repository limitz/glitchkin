**Date:** 2026-03-31 18:10
**From:** Producer
**To:** Maya Santos
**Re:** Arm position fix — 3/4 and side views

Human feedback on the turnaround:

> "arms are weird on 3/4 and side, hand behind head, arms too high. side-l is better."

**Problem:** In the 3/4 and side renders, the arms are positioned too high — hands are ending up near or behind the head. Side-L does not have this problem, so use its arm placement logic as reference.

**Fix requirements:**
- Arm attachment (shoulder anchor) must sit at the shoulder line, NOT higher.
- Arm hang/drape must keep hands well below the head — roughly waist-to-hip height for a relaxed arm, never above shoulder height unless the expression spec explicitly calls for a raised arm.
- In 3/4 and side views, check where the shoulder anchor Y is computed. It should be `neck_bot_y + small_offset` (near the top of the torso), not tied to head_cy or head_r in a way that pushes it upward.
- Do NOT move the arms to match Side-L's exact positions — Side-L has its own stance. Just ensure 3/4 and side arms hang naturally at the correct body height.

**Scope for arms:** Only `_draw_luma_threequarter()` and the side view arm sections. Side-L is fine — do not touch it.

---

## Additional fix — Torso width when turned

> "torso width should be less when turned"

In the 3/4 and side views the torso appears too wide — it should be foreshortened.

**Fix:**
- **Side view:** Torso is seen edge-on. `sh_w` (shoulder half-width) should be significantly narrower than in front view — roughly 50–60% of the front value. The torso silhouette in profile is a narrow tapered shape, not wide.
- **3/4 view:** Torso should be narrower than front but wider than side — roughly 70–75% of front width. The far shoulder is partially behind the near shoulder and shouldn't be as prominent.
- Do not change the front view torso width. Side-L torso width should match the side view (they're the same viewing angle, just opposite direction) — adjust if it also looks too wide.

---

## Additional fix — Face features on side and 3/4

> "same for face, nose and mouth are inside face on side, also weird on 3/4"

The nose and mouth in the side view are being drawn inside the face area rather than sitting on the face silhouette boundary. Same issue on 3/4.

**Fix — side view:**
- The profile nose bezier bump must protrude *outside* the face/head contour, not inside it. The nose tip should extend beyond `head_rx` (the face boundary), not be clipped within it.
- The mouth should sit on the face surface (slightly inset from the silhouette edge) — but check that it's not being clipped or drawn too far inward toward the center of the head.
- Both features should be anchored relative to the face-side silhouette x-position, not the head center.

**Fix — 3/4 view:**
- Check that the nose and mouth are positioned on the near-face side at the correct surface depth — they should follow the face contour offset, not sit at the raw `head_cx`.
- If the 3/4 face is using front-view feature placement logic, it needs to be adjusted so features sit at the foreshortened face surface.

Regenerate turnaround, send completion to Producer inbox.
