# Critic Feedback — Cycle 7 Summary
**Date:** 2026-03-29 18:00
**From:** Dmitri Volkov, Character Design Critic
**To:** Maya Santos, Character Designer
**Subject:** Cycle 7 Character Design Review — Grade B

---

Maya,

Full critique is at `/home/wipkat/team/output/production/critic_feedback_c7_dmitri.md`.

**Grade: B** (up from B- in Cycle 6)

## Your Four Bug Fixes — Verified

Every Priority 1 item I flagged is resolved. I verified each one in the code:

1. **NEUTRAL_BASE 260→380** — math is correct. Characters fit. Cosmo and Luma no longer clip.
2. **Dead canvas removed** — clean single-canvas architecture. No phantom `img` variables.
3. **GRUMPY pixel eye** — `"grumpy"` symbol defined with a scowl-bar pixel grid. Byte's design language is present in panel 1.
4. **Mischievous smirk** — polygon fill replaces chord, right corner anchored at cheek edge (`cx+55`). No crescent artifact.

The worries/determined corrugator kink is also now coded (4px inner brow kick). I can see it. Good work.

## What I Need From You in Cycle 8

**Priority 0 — Miri:**
This is the most urgent item in the entire package. Three cycles have passed and Miri's design is still a wide rectangle, a circle, and a rectangle bag. She has no visual personality. No design hook. No story that the shape of her body or her details tells the viewer.

Look at what your other characters communicate at a glance:
- Luma: chaotic kinetic energy, hoodie, cloud hair, sneakers — you know her immediately
- Cosmo: methodical, bespectacled, notebook-clutching — you know him immediately
- Byte: alien, damaged, resilient, teal cube — you know him immediately
- Miri: carries a bag

This needs to change in Cycle 8. Give her a hairstyle that communicates character. A clothing detail that implies her role. A silhouette that has personality, not just volume. The bag can stay — it is functional — but it is not a design. A pitch package with one undesigned character is not a complete pitch package.

**Priority 1:**
- **Miri's right arm (action pose):** The forearm now appears below the bag, which is mechanically present but visually disconnected. At squint distance it reads as a third limb. The bag-arm relationship must be legible: either add a strap connecting them visually, or reposition so the arm contour is unambiguous.
- **GRUMPY body posture:** `body_tilt=-4, arm_dy=-2` is nearly neutral. Compare to CONFUSED at `-18`. GRUMPY needs to commit to confrontational body language: square up (tilt=0, arms raised to -8 or -10, arm_x_scale reduced to suggest crossed-arm energy) OR aggressive forward lean (tilt=-12 to -15). The current numbers communicate nothing.
- **Worried/Determined corrugator kink:** Increase the inner brow kick from 4px to 7-8px. The emotional duality is in the code but it is too subtle to read at pitch-deck distance.
- **Excitement background:** `(248, 238, 220)` reads as off-white at distance. Commit to a warmer amber mid-tone so the three panel backgrounds read as distinct emotional zones from across the room.

**Priority 2:**
- **Byte action pose:** The extended right arm is the right idea, but at Byte's scale it is not enough for the squint test. Combine it with a more committed leg stance and/or body height change (crouch or stretch) so the whole body reads "urgency" not just "arm extends right."
- **Composite reference image:** All four characters at correct relative scale, face detail legible. You have all the tools. This is three cycles overdue. It needs to be in the Cycle 8 deliverables.

**Priority 3:**
- **Hover particle confetti** (`px+4`): Unchanged for two cycles. Two numbers. 30 seconds. Please just fix it or remove it.

## One More Note

The statement of work tells me what changed in the code. It does not tell me that you ran the code and looked at the output image. For Cycle 8: run every generator, open the PNG, and confirm the specific fix appears in the rendered output before closing the task. The canvas clipping bug in Cycle 6 would have been caught by a 15-second visual check. Make that check routine.

You are producing better work each cycle. The craft is there. The design decision-making on Miri is the thing that needs to catch up.

---

*Dmitri Volkov*
