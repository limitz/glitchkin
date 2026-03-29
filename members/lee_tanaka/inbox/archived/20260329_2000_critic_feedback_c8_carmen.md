# Critic Feedback — Cycle 8
**From:** Carmen Reyes, Storyboard & Layout Supervisor
**To:** Lee Tanaka
**Date:** 2026-03-29 20:00
**Re:** Chaos Sequence P14–P24 + P22a / Full 26-Panel Cold Open Review

---

Full critique is at: `/home/wipkat/team/output/production/critic_feedback_c8_carmen.md`

**Overall Grade: B / 80%** — Raised from Cycle 6's B-.

---

## What You Got Right

You completed the sequence. Twenty-six panels, full arc, structurally coherent. That matters.

The MEMORY.md lessons are showing up in the code. Lower-center anchoring. Additive glow via alpha_composite. Six OTS specs in P22a. Byte at 90px for the CU. Visible FX in image geometry, not caption text. You stored those lessons and you applied them. P16 and P19 are strong panels. P22a is close to excellent — the warm-gold confetti detail on the contact point is exactly what the script asked for and it is the right detail to get right.

The `draw_byte_body()` and `draw_luma_face()` functions are now production-quality tools. Keep them.

The structural problems from Cycle 4 and Cycle 6 are resolved. Bridging panels present. Spatial logic continuous. Camera variety disciplined across the full 26 panels.

---

## What You Need to Fix for Cycle 9

**Critical (fix these first):**

1. **Dutch tilt geometry — P14 and P24.** Both panels say "12° Dutch" in the annotation but the floor geometry delivers approximately 1°. A 12° Dutch tilt at 480px wide is ~85px difference from left to right floor edge. Fix the polygon coordinates. An animator reading the geometry gets 1°. An animator reading the caption gets 12°. The geometry always wins.

2. **P21 overhead angle.** The camera is essentially straight down (90°). The script says "pulling back and up slightly" — which should be a 40-45° high angle. Characters shown as pure top-down silhouettes are hard to distinguish from the Glitchkin shapes in the monitors at thumbnail scale. Show me some profile in the overhead angle.

3. **P24 hero framing.** Luma is positioned at 38% from the top of the draw area — she is center frame, not foreground. A low-angle wide hero shot needs her figure to fill the lower third of the frame so the camera reads as looking UP at her, not across at her.

**Significant:**

4. **Expression library gap.** You have been defaulting 'curious' across P17, P18, and P20. These three panels need different states:
   - P17: Luma has just stopped screaming and is settling. Add `'settling'` state.
   - P18: Luma realizes she has been drawing Glitchkin in her margins without knowing why. This is recognition, not curiosity. Add `'recognition'` state.
   - P20: The name exchange. She is choosing warmth deliberately. Add `'warmth'` state.

5. **P17 Byte expression.** 'alarmed' is wrong for the quiet beat. Use 'resigned' or add 'post-alarm' state. Byte at maximum alarm during the chip-landing beat undercuts the silence you are trying to create.

6. **P15 body language.** Three issues:
   - Body torso needs actual squash (wider than tall, not circular) — she feels the floor coming.
   - Arms need asymmetry: LEFT arm HIGH (above head, going left), RIGHT arm pointing directly right. Not symmetric windmill.
   - Legs need to be closer to 90° from vertical for spread-eagle to read at thumbnail.

**Moderate:**

7. P16 "tik" annotation — this sound belongs to P11-12, not P16. Remove or correct.
8. P22a gaze annotation — document the three beats: shoulder → Luma's profile → monitors → decision to stay.
9. Add a production note in P14 or between P14/P15 noting Byte's location during P15 (he is off-frame toward ceiling fan).

---

## The Show is Here

P18 has Luma holding up a notebook with "what if a computer had FEELINGS???" in the margin next to drawings that look like Byte. She has been drawing him for months without knowing why.

That detail is the show's premise in 12 words of homework margin text. You put it in the image. That is the job.

Fix the Dutch tilt. Fix the expression library. Show me the revised panels.

— Carmen Reyes
