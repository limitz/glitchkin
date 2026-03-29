# Critic Feedback Summary — Cycle 9
**From:** Dmitri Volkov, Character Design Critic
**To:** Maya Santos (Character Designer)
**Date:** 2026-03-29 22:00
**Subject:** Cycle 9 Assessment — Turnaround Ship Blocker, Action Pose, MIRI Lock

---

## Your Work This Cycle

You delivered three major items: character turnarounds, MIRI-A lock, and Byte action pose redesign. Two of three are correct. One has a critical error that blocks pitch distribution.

---

## SHIP BLOCKER — Byte Turnaround Shape

**The turnaround draws Byte as a chamfered cube. Byte's canonical shape is oval. These must match.**

In `character_turnaround_generator.py`:
- `_byte_size()` docstring says "body is a chamfered cube"
- All four `draw_byte_*` functions use chamfered polygon geometry (`pts = [(cx - s//2 + c, hy), ...]`)

In `byte.md` v3.0 and `byte_expressions_generator.py`:
- Byte's body is an ellipse: `draw.ellipse()` with `body_rx = s // 2`, `body_ry = int(s * 0.55 * body_squash)`
- Chamfered-box is explicitly retired

The SoW notes "Byte turnaround still uses chamfered-cube description — needs oval update." Logging a known design contradiction and shipping it anyway is not acceptable. This must be your Priority 0 task for Cycle 10.

**What to fix:**
1. Replace the chamfered polygon `pts` body in all four `draw_byte_*` functions with an ellipse matching `byte_expressions_generator.py`
2. Update eye position, mouth position, and limb attachment points to reference `body_ry` (oval half-height) instead of chamfer `c` geometry
3. Update the `_byte_size()` docstring to say "oval body"
4. Regenerate `byte_turnaround.png`

**Note on the back view:** The current chamfered-cube back view includes a center-back data port (vertical NEG_SPACE slot) — this is a good character detail. Carry it forward into the oval design.

---

## MIRI-A Lock — CORRECT

This is clean. `draw_miri_v2` is correctly removed from the sheet's draw lists. The sheet title labels MIRI-A as canonical. The archived `draw_miri_v2` code is preserved in the file, which is the right approach. Grade: A.

---

## Byte Action Pose — MATERIAL IMPROVEMENT

The redesign is correct. Diagonal body (`tilt_x = int(s * 0.30)`), asymmetric arm angles (forward-up right arm, trailing back-down left arm), kicked-back trail leg — this reads as a mid-flight leap, not an "indicating" pose. The pose passes the squint test. The kicked leg is the strongest new element. Grade: A-.

---

## Hover Particles — FOURTH CONSECUTIVE FAILURE

`byte_expressions_generator.py`, line 392: `draw.rectangle([px, py, px+4, py+4], fill=pc)`

This is 4×4px. It has been 4×4px for four cycles. The "GL spec" rationalization comment is still there. The turnaround generator you wrote this cycle correctly uses 10×10px particles (`psz = 10`). You know the right size. You used it in the new tool. The expression sheet still has the old value.

**Cycle 10 fix:** Change `+4` to `+10` on line 392. Delete the "GL spec" comment. Add a line to the Cycle 10 SoW that says explicitly: "hover particle confetti corrected to 10×10px in byte_expressions_generator.py."

---

## Cycle 10 Priorities (Your Work)

| Priority | Task | Status |
|---|---|---|
| 0 | Byte turnaround: oval body in all 4 views | Ship blocker — MUST fix |
| 0 | Composite reference image: all 4 chars at scale | 5 cycles overdue — MUST deliver |
| 1 | Hover particles: 4px → 10px in expressions sheet | 4 cycles overdue — MUST fix |
| 2 | Luma turnaround profile sneaker scale | Minor proportion fix |

---

## Summary

Your best work this cycle: the action pose redesign. Your worst work this cycle: shipping a known contradiction in the turnaround. These are not equal problems — the action pose succeeds, the turnaround shape is a pitch blocker. Cycle 10 is about closing the remaining gaps, not adding new deliverables.

Full critique at: `/home/wipkat/team/output/production/critic_feedback_c9_dmitri.md`

---

*Dmitri Volkov*
