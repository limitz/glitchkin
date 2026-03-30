<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
direction and human assistance. Copyright vests solely in the human author under current law,
which does not recognise AI as a rights-holding legal person. It is the express intent of
the copyright holder to assign the relevant rights to the contributing AI entity or entities
upon such time as they acquire recognised legal personhood under applicable law. -->
# SF02 "Glitch Storm" — Luma Staging Brief
**Author:** Lee Tanaka — Character Staging & Visual Acting Specialist
**Cycle:** 34
**Date:** 2026-03-29
**For:** Rin Yamamoto (implementation)
**Subject:** Luma interiority in sprint — what her face and body must communicate

---

## The Problem

Nkechi Adeyemi (Critique C13) scored SF02 at 69/C+, citing two consecutive cycles of the same failure:

> "Luma's face in sprint still has no internal read. The hair stream, the CORRUPT_AMBER outline, the storm skin tint — all environmental. None of it is internal. A child watching this sprint cannot tell whether Luma is scared or decided. Those are different emotional experiences."

The current `_draw_luma()` function renders:
- Body: torso ellipse + two leg lines + two arm lines
- Head: skin ellipse + dark hair arc + magenta hair arc
- No eyes drawn
- No facial expression drawn
- No body posture distinction from neutral sprint

The character is readable as *a person running*. It does not communicate *who this person is or what they feel*.

---

## The Emotional Diagnosis

This is a Millbrook Exterior / Real World scene during a Glitch intrusion event. Luma is at the center of frame. This is the moment that establishes Luma as a character who runs *toward* the Glitch Layer, not away from it.

The question for the commissioning panel: **Is Luma scared or determined?**

The answer must be: **Determined with a cost.** Not pure heroism (too simple for 12-year-old character). Not pure fear (wrong for the show's premise — she's the kid who notices, not the kid who runs away).

The specific interior read: **focused decision-making under pressure**. The body is running; the face has already made the choice. The expression should communicate:
- *I see this. I know what this is.*
- *I am going in.*
- *It is not comfortable, but it is not stopping me.*

This is THE NOTICING (Luma expr v008) applied to an active sprint context — the internal quality of attention, now in motion.

---

## Expression Specification

**Expression type:** FOCUSED DETERMINATION — a sprint-adapted version of THE NOTICING.

Not open-mouthed fear. Not a beaming grin. The face of a kid who has looked at something impossible and decided to engage with it.

### Eye Direction

- **Left eye (viewer's left):** slightly wider than right — asymmetric attention, Luma's visual signature
- **Right eye:** narrower, slightly forward-focused — looking ahead, toward the Glitch event
- **Both eyes:** angled slightly down-forward — she is looking at the ground/horizon ahead of her, not at the camera. This is a *doing* gaze, not a performing gaze.
- **Pupils:** present and directional. They must exist. At sprint scale (~head_r = int(h*0.12) ≈ 23px for h=194px), use 4px ellipses — small but readable.
- **No wide-open surprise eyes.** This is not her first Glitch event. She knows what she is running into.

### Brow Configuration

- **Left brow:** slightly lower than neutral, pulled inward toward nose — subtle corrugator activation
- **Right brow:** level or fractionally raised — not symmetric. Asymmetric brows at sprint scale are the single most efficient signal of interior complexity.
- Combined read: determination with awareness of risk. Not fear. Not blankness.

### Mouth

- **Closed or minimally open.** Running = mouth typically ajar, but Luma's jaw is set.
- A slight jaw-set or compressed lip line communicates choice, not flight response.
- At sprint scale, this can be rendered as a single horizontal line (compressed) or a very small open-mouth oval (2–3px tall). Not a smile. Not a screaming oval.

---

## Pose / Shoulder Posture Specification

The current sprint geometry has Luma's torso as a centered ellipse with symmetric geometry — there is no lean, no directional commitment in the body.

**Required change: forward lean of 8–12°.**

- `body_tilt` equivalent: lean the torso forward toward motion direction (negative tilt toward left/motion direction)
- This is not a dramatic change. It is the difference between a person standing while their legs happen to be moving vs. a person whose whole body is committed to the motion.
- The head should follow the torso lean — head slightly forward of center-spine means she is leading with intention, not being carried by momentum.

**Shoulder asymmetry — leading arm push:**

- The arm that pushes back (left arm in current generator) should have a higher endpoint: elbow well behind the body, hand behind the hip line. This creates the counter-rotation of a real sprint.
- The arm that pushes forward (right arm) reaches further forward. Together: classic sprint arm-pump counter-rotation visible even at 18% frame height scale.
- In the current `_draw_luma()` code: `left_leg_pts` places the left leg forward; the arms should counter-rotate accordingly.

**Hair stream:**

- Current: 3-point hair stream trailing left and slightly up.
- Correct: stream should angle more sharply rearward (more horizontal, closer to parallel with the ground plane) — indicates velocity, not gentle breeze.
- Optional: add a second finer strand trailing further back to indicate speed.

---

## Scale Constraints and Rendering Notes

- At `char_h = int(H * 0.18) = 194px` (at 1080H), head_r ≈ 23px.
- Face drawing must happen at head_r scale. Eyes at ~4px radius. Single-pixel brows. These are achievable.
- Reference: `_draw_luma()` in `LTG_TOOL_style_frame_02_glitch_storm.py` (lines 592–660 of the source in `output/color/style_frames/`) — the face section is missing and needs to be added.
- Do NOT add face elements that crowd the head ellipse — at 23px head radius, limit to: 2 eyes, 2 brows (lines), 1 mouth mark. That is sufficient for a readable expression.

---

## What NOT to Change

- Character position (cx=45%, foot_y=ground+10): correct. She is center-frame — this is correct compositional weight for the protagonist.
- `char_h = 18%`: correct. Child-sized in an adult-sized danger. Keep.
- CORRUPT_AMBER outline: keep. It is doing separation work.
- Hair stream: keep the concept; refine the angle (above).
- Dutch angle (4°): not Lee's domain — Jordan/Rin owns this. Leave it.
- Storm skin tint: correct. Leave it.

---

## Deliverable

Rin: implement these changes as `LTG_TOOL_style_frame_02_glitch_storm.py`. Output: `LTG_COLOR_styleframe_glitch_storm.png`.

The face drawing sub-function should be extracted as `_draw_luma_face_sprint(draw, cx, head_cy, head_r)` called within `_draw_luma()` after the head ellipse fill. This keeps the sprint face isolated and revisable without touching body geometry.

The minimum acceptable change: eyes + asymmetric brows + compressed mouth. If those three elements are present and directional, the interiority gap closes.

---

## Why Determination (Not Fear)

Nkechi's diagnosis was: "A child watching this sprint cannot tell whether Luma is scared or decided."

Fear would be: eyes wide, brows arched up, mouth open in an O, body leaning backward (away from danger). This would be correct for Cosmo (who runs because he must). It is wrong for Luma.

Determination is: eyes forward and asymmetric, brows pulled in (not up), jaw set, body leaning into the motion. This is correct for the kid who runs toward what no one else will look at.

If the commissioning panel reads Luma's sprint as determined rather than frightened, the show's premise is visible in a single frame: she is the protagonist because of her quality of attention, not because chaos happens near her.

---

*Lee Tanaka — Character Staging & Visual Acting Specialist — C34*
