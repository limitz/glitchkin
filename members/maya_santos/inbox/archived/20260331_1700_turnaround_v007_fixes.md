**Date:** 2026-03-31 17:00
**From:** Producer
**To:** Maya Santos
**Re:** Luma Turnaround — Human Review Fixes (v007)

Human reviewed v006. Three issues to fix. Critique 19 is on hold until these are signed off — so this is the only active task.

---

## Issue 1 — 3/4 View: Face and legs look frontal

**What the human said:** "face, legs are facing front, offset in x axis"

**Root cause visible in code:**
- `_draw_luma_threequarter()` places legs as `front_leg_x` (left) and `back_leg_x` (right) — spread symmetrically side-to-side around `hip_cx`. That IS a front-facing leg layout.
- The face in threequarter appears to be drawn with front-facing elements just shifted horizontally.

**What a true 3/4 view requires:**
- **Legs:** stagger fore/aft, not left/right. Near leg slightly in front of the body plane, far leg slightly behind. In the rendered image this reads as the near foot being lower on the canvas (closer to viewer = lower), far foot slightly higher. The hip spread shrinks — you're looking across the hips at an angle, not straight at them.
- **Face:** profile nose silhouette visible on far-side edge. Near eye full and dominant. Far eye genuinely foreshortened — not just narrower, but partially cut off by the face contour. The head itself is not a symmetric oval — it bulges toward the near side. One cheek visible, the other is behind.
- **Torso:** narrow on the far side (foreshortened), shoulder-line tilts back into depth, not horizontal.

---

## Issue 2 — Side View: Looks like front except torso looks like 3/4

**What the human said:** "side looks like front except torso which looks like 3/4 torso"

This means the side view has:
- A face that's too frontal (both eyes partially visible, or a front-style nose)
- Legs that spread laterally instead of being stacked in the side plane
- A torso that may be drawn at an angle (from the old 3/4 torso code)

The side view should be a clean profile:
- **Face:** true profile — one eye only, profile nose (extends as a bump off the face contour), one cheek only. No second eye.
- **Legs:** stagger front/back in the depth axis. In side view, one foot is forward (in front of the body in space) and one is behind. They don't spread sideways — they both sit near center-x with one slightly forward, one slightly back.
- **Torso:** proper side silhouette — narrow (you're looking across the body's thin dimension), hoodie pocket visible on the near side, no visible far shoulder.

Audit `_draw_luma_on_context()` against these criteria and fix where it fails.

---

## Issue 3 — Side-L: Must be a distinct pose, not a mirror

**What the human said:** "side-l is just mirror image of side. must be separate pose"

The turnaround code confirms this: `"SIDE-L": ("side", "left")` which just applies `ctx.scale(-1, 1)`. A mirror flip is not acceptable.

**What Side-L needs to be:**
- Add `pose_mode="side_l"` to `draw_luma()` and the VIEW_SPEC in the turnaround.
- Side-L is not just "facing left" — it should show a **different natural side stance**: different weight distribution, different arm positions, or a different expression-specific pose beat than Side. For example:
  - If Side shows weight on the right foot with left arm raised, Side-L could show weight on the left foot with a different arm read.
  - The character should feel like she naturally moved and turned around, not like a flip.
- The head/face should be drawn left-facing natively, not mirror-transformed. Same for body elements.

---

## Issue 4 — Arms: Still disconnected at shoulder joint

**What the human said:** "arms now single outline, good, but still disconnected from torso visually (outline where upper arm meets shoulder)"

`_draw_unified_arm()` is an improvement but the shoulder cap joint still leaves a visible seam where it meets the hoodie body.

**Fix approach:**
- The arm silhouette should merge into the hoodie body at the shoulder — no outline stroke at the join. Draw the arm+shoulder as one combined path that includes the shoulder cap as part of the hoodie body boundary. Only the outer silhouette gets the stroke.
- Think of it as: the hoodie body outline and arm outline are one continuous path — the arm "grows out of" the torso without a seam. No separate circle or rounded cap at the shoulder that creates a double line.

---

## Deliverables

- `LTG_TOOL_char_luma.py` → v1.2.0
  - Fix `_draw_luma_threequarter()` — proper 3/4 face + fore/aft leg stagger
  - Fix `_draw_luma_on_context()` / side view — true profile face + legs
  - Add `_draw_luma_side_l()` for the left-facing distinct pose
  - Fix arm-shoulder joint (all pose modes)
- `LTG_TOOL_luma_turnaround.py` → v007
  - Update VIEW_SPEC: `"SIDE-L": ("side_l", "right")` (or however you implement it)
  - Regenerate `output/characters/main/turnarounds/LTG_CHAR_luma_turnaround.png`
- Run gesture lint — 0 FAIL target

When done, send completed task report to Producer inbox as usual.
