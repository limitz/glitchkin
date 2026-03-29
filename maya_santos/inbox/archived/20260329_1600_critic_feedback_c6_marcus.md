**Date:** 2026-03-29 16:00
**From:** Marcus Webb, Animation Timing & Motion Specialist
**To:** Maya Santos, Character Designer
**Re:** Cycle 6 Critique Summary — Motion & Staging

---

Maya,

Full written critique is at `/home/wipkat/team/output/production/critic_feedback_c6_marcus.md`. This is your summary of what needs to carry into Cycle 7.

## What You Fixed (and it shows)

The body variation mandate on Byte was the most important thing in my Cycle 5 critique, and you delivered it. The ALARMED, RELUCTANT JOY, and POWERED DOWN panels are now working as full-body emotional statements, not just face symbols pasted onto a neutral box. The before/after state annotations are the right discipline — keep them on every expression panel going forward.

Luma's reckless excitement face is substantially upgraded. The kinked left brow, directed pupils, chord-cut iris, off-center grin, and bottom lip suggestion are all present and correct. The MISCHIEVOUS PLOTTING expression is the best single face you have put on this sheet — the extreme brow asymmetry and half-lidded/wide-open eye contrast reads as a specific character in a specific mental state. That is what this project needed from the start.

Grade for Cycle 6: **B+**. Up from approximately C+ in Cycle 5. The rate of improvement is real.

## What Must Change in Cycle 7

**1. Byte's arms must become asymmetric.**
Both arms still move as a matched pair — same height, same extension, both sides. Real expression requires one arm up and one arm down, or one extended and one withdrawn. Add `arm_left_dy`, `arm_right_dy`, `arm_left_x_scale`, `arm_right_x_scale` to the body_data dictionary and update the draw function. Priority updates once this is available: SEARCHING (right arm scanning, left arm relaxed), GRUMPY (left arm crossed), ALARMED (asymmetric startle — one arm forward, one back).

**2. Byte's shape must be consistent with the style frame.**
In the expression sheet, Byte is a chamfered-corner box. In the style frame, Byte is an oval. These are not the same character. Before Cycle 7 work ships, one shape must be chosen and applied to both documents. The box has more character; the oval is easier to composite. Pick one and commit.

**3. Luma's WORRIED/DETERMINED brows need 2-3px of differential.**
Both brows are currently mirror images in that expression. The dominant side (character's right, screen left) should carry slightly more tension — left brow raised 2-3px higher than the right. Identical V-brows read as generic determination, not character-specific worry.

**4. Luma's collar offset in RECKLESS EXCITEMENT needs more lean.**
The current `offset_x=6` on the collar is too subtle to read as a head tilt. Bring it to at least 15-18px and consider angling the arc itself slightly to suggest a genuine forward lean rather than a centering error.

## Notes on Style Frame (pass to Alex Chen)

The style frame has a staging problem worth flagging for the Art Director: Luma's arm is reaching toward the screen, but her body is not leaning. These are different physical actions. A character whose whole body leans forward is committed; a character whose arm extends while the body stays vertical is pointing. Luma should lean. The torso polygon needs to be angled toward the monitor wall, not vertical.

Also flag: the discovery gap (the distance between Luma's hand and Byte's tendril tip) is currently set by arithmetic (`scr_x0 - 20`) rather than as a named design constant. Alex should define this as a named value with a comment explaining the narrative intent of that specific distance.

The warm/cold lighting split, the amber elliptical outline on Byte, and the two-hands-reaching staging concept are all approved and should be carried forward unchanged.

---

Good work this cycle. The improvements are visible and specific. Cycle 7 is about asymmetric arm mechanics and body lean — both are problems of physicality, not aesthetics. Make Byte reach differently with each hand and make Luma lean with her whole body, not just her wrist.

Marcus Webb
