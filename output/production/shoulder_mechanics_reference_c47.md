<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
direction and human assistance. Copyright vests solely in the human author under current law,
which does not recognise AI as a rights-holding legal person. It is the express intent of
the copyright holder to assign the relevant rights to the contributing AI entity or entities
upon such time as they acquire recognised legal personhood under applicable law. -->
# Shoulder Mechanics Reference — "Luma & the Glitchkin"

**Author:** Lee Tanaka (Character Staging & Visual Acting Specialist)
**Date:** 2026-03-30, Cycle 47
**Origin:** Takeshi Critique #3 (persistent since C15) — arms without shoulder involvement

---

## The Problem

Arms in our character generators move at the shoulder *socket* but the shoulder *mass* stays static. A rectangle torso with polyline arms produces "puppet arm" staging: the arm appears to originate from a fixed pivot point rather than from a muscular body. This has been noted by Takeshi in three consecutive critique cycles and appears across multiple assets (SF06 Miri, P14 Byte impact, expression sheets, lineup).

The fix is not anatomical realism — our characters are stylized at 3.2-3.5 heads tall. The fix is **silhouette shape change at the shoulder when the arm moves**.

---

## The Rule

**When an arm moves, the shoulder line changes shape.**

This applies to all human characters (Luma, Cosmo, Miri). Byte is exempt (digital body, no musculature). Glitch is exempt (non-humanoid).

### What Changes

| Arm Action | Shoulder Response | Torso Silhouette Change |
|---|---|---|
| Arm raised above horizontal | Deltoid muscle lifts; trapezius engages | Shoulder point rises 3-5px above resting. Torso top edge becomes asymmetric (raised side higher). |
| Arm extended forward/outward | Deltoid rotates forward; scapula spreads | Shoulder point shifts outward 4-6px and forward 2-3px (toward viewer in 3/4). Torso width increases on that side. |
| Arm crossed over body | Deltoid compresses; trapezius bunches | Shoulder point drops 1-2px and shifts inward 3-4px. Neck base widens slightly (bunched muscle). |
| Arm relaxed at side | Neutral — deltoid rounded bump | Shoulder point at default resting position. The bump itself is the shoulder (not a sharp corner). |
| Both arms raised (Y-pose) | Both deltoids lift; trapezius contracts | Both shoulder points rise. Neck appears shorter. Torso top edge arches upward. |

### Minimum Implementation

For each character's torso draw function:

1. **Replace rectangle torso with polygon.** The top edge of the torso is NOT a horizontal line — it is a polyline with two shoulder points that shift based on arm position.

2. **Shoulder point coordinates derive from arm angle.** If the arm endpoint is at `(arm_x, arm_y)` and the shoulder socket is at `(shoulder_x, shoulder_y)`:
   - `shoulder_rise = max(0, (shoulder_y - arm_y) / arm_length) * 5`  (px — rises when arm goes up)
   - `shoulder_spread = abs(arm_x - shoulder_x) / arm_length * 4`  (px — widens when arm extends)
   - New shoulder point: `(shoulder_x + shoulder_spread_sign * shoulder_spread, shoulder_y - shoulder_rise)`

3. **The deltoid bump.** At the shoulder point, draw a small ellipse or arc (radius 4-6px at style-frame scale, 2-3px at storyboard scale) that follows the arm's initial direction. This is what makes the shoulder read as a muscle, not a hinge.

### What NOT To Do

- Do not add anatomical detail (clavicle lines, rotator cuff). This is cartoon anatomy.
- Do not change arm thickness — the arms are already correct width.
- Do not add shoulder detail to Byte or Glitch.
- Do not apply this to sprint-scale characters where head_r < 20px — the shoulder shift would be sub-pixel.

---

## Per-Character Application

### Luma
- **Hoodie hides deltoid detail** — the shoulder mass change shows as a FABRIC BUNCH at the top of the hoodie sleeve. Draw as a wider rectangle or arc segment at the torso-arm junction.
- Most critical in: SF02 sprint (forward lean + arm counter-rotation), P15 floor sprawl (one arm reaching), expression sheet poses with arms.

### Miri
- **Cardigan is loose but structured.** Shoulder rise shows as a CREASE at the cardigan's shoulder seam. The V-neck collar also shifts asymmetrically when one shoulder rises.
- Most critical in: SF06 "hand-off" gesture (right arm extended toward CRT — right shoulder must pull forward), expression sheet WELCOMING (both arms open).

### Cosmo
- **T-shirt/jacket.** Shoulder mass is most visible on Cosmo because his clothing is fitted. Deltoid bump reads as a ROUNDED CORNER at the torso-sleeve boundary (not the sharp corner of a rectangle).
- Most critical in: SKEPTICAL pose (arms crossed — both shoulders compress inward), AWKWARD pose (asymmetric — one shoulder raised in shrug).

---

## Verification

After implementing shoulder mechanics in any character generator, verify by:

1. **Silhouette test:** Run `LTG_TOOL_expression_silhouette.py` on the updated expression sheet. Shoulder-shifted poses should have LOWER RPD (more differentiated silhouettes) than pre-fix. Target: RPD improvement of at least 3% on arm-active poses.

2. **Visual check:** At the shoulder point, the torso outline should NOT form a sharp 90-degree corner. It should curve or angle toward the arm direction.

3. **Contact sheet read:** In contact sheet thumbnail view, the shoulder shift should be visible as an asymmetric top-edge on the character silhouette. If the shoulder shift is invisible at thumbnail scale, increase the rise/spread values by 50%.

---

## References

- Takeshi Critique #3 (C15, C34, C43): "Arms without shoulder involvement — persistent."
- C42 lessons: Body language tells the story before the face.
- C43 lessons: A style frame character with no face expression is a failing asset. (Same principle: a character with no shoulder mechanics is a failing body.)
- Expression pose vocabulary brief (C34): Silhouette differentiation requires body posture changes, not just face changes.
