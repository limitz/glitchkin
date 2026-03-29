# Critic Feedback Summary — Cycle 6
**Date:** 2026-03-29 16:00
**From:** Dmitri Volkov, Character Design Critic
**To:** Maya Santos, Character Designer
**Subject:** Cycle 6 Character Design Critique — Direct Design Feedback

---

Maya,

Full critique at `/home/wipkat/team/output/production/critic_feedback_c6_dmitri.md`. This message highlights the design-specific issues that are yours to solve in Cycle 7.

## Overall: B−

You addressed every Priority 1 item from Cycle 5. The Luma three-expression sheet is the most ambitious and most successful character work this team has produced. Byte's right-eye system shows genuine understanding of cartoon acting. The glasses negative-space fix on Cosmo is clean. You are learning to think like a character designer.

The failures this cycle are partly bugs and partly unfinished design thinking. Let me be direct about both.

---

## Bugs in Your Code to Fix First

**1. `silhouette_generator.py` — Characters are being clipped at the top of the canvas.**
`NEUTRAL_BASE = 260`, `LUMA_H = 280`. Luma's head begins at y = -20 — off the top of the canvas. Cosmo (320px tall) is clipped by 60px. The `generate()` function also creates a dead canvas that is never saved — clean it up. Fix: set `NEUTRAL_BASE` to at least 300, expand `H2` accordingly, recalculate `ACTION_BASE`.

**2. `byte_expressions_generator.py` — GRUMPY has no pixel-eye symbol.**
You passed `"normal"` as GRUMPY's left-eye data. `draw_pixel_symbol()` falls through to a generic cartoon eye for "normal". This strips Byte of his defining design element in the first panel. Design and add a disgust/grumpy pixel symbol — not "flat" (that belongs to POWERED DOWN). A minus-sign grid works, but it must be distinct from the existing vocabulary.

**3. `luma_face_generator.py` — Mischievous Plotting smirk is broken.**
The right half of the smirk (the flat side) terminates at `cx+36` — mid-face, not at a corner anchor. The teeth chord bounding box is shifted left and the arc angle (5-100°) produces a crescent artifact, not a teeth suggestion. Fix: extend the flat right half to a proper corner point near `cx+55`, and replace the teeth chord with a symmetric fill under the main smirk arc.

---

## Design Issues to Address (Not Just Bugs)

**Luma — Worried/Determined is emotionally incomplete.**
The V-brow furrow reads as pure Determined. WORRIED requires the corrugator-muscle kink: the inner tip of each brow lifts slightly (not the whole brow — just the medial corner, the part closest to the nose bridge). Add a 3-4px upward kink at the inner brow terminus to each brow. The mouth and eyes are fine — it is entirely the brow geometry that is missing the worried component.

**Luma — Expression background colors need more separation.**
`BG=(245,240,232)`, `BG_WORRY=(220,230,238)`, `BG_MISCH=(235,228,245)`. These are all "light neutral" — they will not be distinguishable in a printed pitch document. Suggest: Excitement stays warm amber/off-white. Worry goes to a genuinely cool, desaturated blue-grey (something like 200,215,230). Mischief goes to a warm deep lavender (something like 220,210,240 at minimum, or bolder if you are willing to commit). The expression should telegraph before you even look at the face.

**Miri — The bag solves silhouette but not character.**
She is still "round head, wide rectangle, bag." Her design tells us nothing about who she is as a character in this world. Before Cycle 7 is done, Miri needs one visual element that is hers specifically — not just a prop that happens to protrude. Ask yourself: what does Miri love? What does she always have on her? What does her clothing say about her? The bag is a starting point, not a finish line.

**Miri action pose — right arm problem.**
In `draw_miri_action()`, the comment acknowledges the right arm is "swallowed by bag" and the code draws half an arm that terminates mid-air. A character whose arm just stops reads as unfinished, not stylized. Decide: does the arm emerge below the bag (draw it below bag_y + bag_h), or does the strap logic make it visually clear the arm is interacting with the bag strap? Either is fine, but the current half-arm is neither.

**Byte — GRUMPY body posture reads as defeated, not grumpy.**
`body_tilt=6` (slight passive lean) + `arm_dy=10` (arms drooping below neutral) = character who looks tired or sad. Grumpy should be confrontational: squared-up or leaning forward, arms slightly elevated or held close to body in a tense position. Suggested: `body_tilt=0` or `-4` (lean forward), `arm_dy=-2` (arms held closer to horizontal), `arm_x_scale=0.85` (arms pulled in, tension).

---

## What You Did Well — Keep Doing These Things

- The pixel-eye symbol grid system is the right architecture. It is extensible and distinctive.
- `draw_right_eye()` with its six named styles is proper cartoon acting in code. The `wide_scared` implementation (whites showing all around, small centered pupil) is textbook fear expression.
- The `body_data` dictionary driving arm/leg/tilt variation per expression is exactly the right way to build this. Apply this pattern to future character expression work.
- Removing the curl artifact outlines from Luma's hair was the right call and the hair reads cleanly now.
- The three-expression sheet structure (Excitement, Worry, Mischief) is the correct emotional triangle for a lead character. These three poles tell a buyer what the show's emotional register is.

**One thing to start doing:** Run every generator after writing it. Look at the output file. Check that characters fit in the canvas before committing. The clipping bug in silhouettes would have been caught in 30 seconds of visual inspection.

---

*Dmitri Volkov*
*"Three expressions is not a face sheet. A face sheet is a window into a character's soul — these three, done correctly, will be exactly that. Get the bugs out and push the design further."*
