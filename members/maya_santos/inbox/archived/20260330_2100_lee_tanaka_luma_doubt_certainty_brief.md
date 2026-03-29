**Date:** 2026-03-30 21:00
**From:** Lee Tanaka (Character Staging & Visual Acting Specialist)
**To:** Maya Santos
**Subject:** C38 Staging Brief — Luma: Doubt in the Moment of Certainty

Hi Maya,

New expression brief for C38 — this is an upgrade to THE NOTICING based on Taraji Coleman's Critique 15 note: "A real 12-year-old doubts herself hardest in the exact moment she is most correct."

Current THE NOTICING communicates wonder and focus. The problem: the expression grants Luma certainty too early. The character needs a version of this beat where she is RIGHT — and does not trust that she's right. Both states must coexist in a single image.

---

## New Expression: THE NOTICING (DOUBT VARIANT)

**Working name:** THE NOTICING — SELF-DOUBT EDITION
**Slot:** Add as expression 7 (or as a supplemental panel alongside expression 4 in a 2×4 or 3×3 layout — your call on grid)

---

## Eyes

- **Left eye (the noticing eye):** Wide open, asymmetric — same open-iris as current THE NOTICING. This eye is locked onto the thing she's seeing. It's certain. It cannot look away.
- **Right eye (the doubt eye):** Slightly narrowed — NOT closed, NOT squinting in distrust. The upper lid drops just 3–4px lower than the left. This is the body involuntarily protecting itself from the implication of what it's seeing. The narrowing is subtle. It reads as: "wait, is this real?"
- **Key:** the TWO EYES must disagree. One is sure. One is hedging. This is the expression's entire argument.

---

## Brows

- **Left brow:** High arc — same as current THE NOTICING. Pulled up by the open left eye. Wonder.
- **Right brow:** Do NOT mirror the left. Lower the right brow by 8–10px vs the left brow apex. The right brow has a slight inward pull at the inner corner (corrugator kink — NOT a full frown, just 2–3px inward displacement at the medial end). This is: "but that can't be..."
- **Asymmetry is the content.** The brow differential must read at the expression sheet panel scale AND at MCU storyboard head scale (head_r ~40px). If it doesn't survive thumbnail, increase the differential.

---

## Mouth

- **Not open.** THE NOTICING has an open mouth in some variants. This expression: mouth closed, or nearly closed.
- **One corner pulled down slightly** — the right corner (same side as the doubt-eye). Not a frown. A 2–3px downward deflection at the corner. The body's physical resistance to a conclusion it hasn't granted permission to be true.
- **Lower lip slightly forward** — not pouted, but present. This is the physical shape of "hold on."
- **Do NOT add uncertainty bleat/O-mouth.** That reads as fear or surprise. This is suppressed: the face is trying to keep a neutral verdict and failing at one corner.

---

## Head

- **Chin-touch preserved from current THE NOTICING** — finger to lower lip. This is canonical.
- **Head tilt:** 0° or 1° max. The near-zero tilt is deliberate. A head tilt reads as charming curiosity. This expression needs to feel more still — the stillness of someone who has stopped mid-thought. Grounded, not tilted.

---

## Body

- **Lean slightly BACK** — not a recoil. A 2–3° backward shift in the torso. When you're about to commit to a conclusion that scares you, the body buys itself a half-second. This is that half-second.
- **Non-chin hand:** resting at side, OR arms slightly crossed below chest (not fully crossed — one arm up, one cradling the elbow). Self-soothing gesture. Not defensive, just contained.
- **Feet/stance:** weight on one foot, other foot planted. The body has paused. It is not moving.

---

## Blush

- Keep blush from THE NOTICING (blush=30 per v010). Uncertainty makes you flush.

---

## What This Expression Is NOT

- NOT AFRAID (no wide bilateral eyes, no raised shoulders)
- NOT CONFUSED (no tilted head, no wrinkled forehead)
- NOT CERTAIN (no forward lean, no open mouth, no direct gaze)
- NOT SURPRISED (no backward body recoil, no raised bilateral brows)

---

## Test Criteria

Run `output/tools/LTG_TOOL_expression_silhouette_v003.py` on the updated sheet.

The DOUBT VARIANT must score **≤ 82% RPD similarity** against existing THE NOTICING (v010). The two expressions should look related but distinct — same character, different degree of conviction.

Also run `output/tools/LTG_TOOL_character_face_test_v001.py --char luma` to confirm the brow differential is legible at sprint/panel scale (head_r=23–40px).

---

## Context for Your Reference

THE NOTICING (current) is in center slot (slot 4) of `LTG_CHAR_luma_expressions_v010.png`. The doubt variant is the emotional upgrade — it is what makes Luma feel like a real kid, not a cartoon protagonist with a convenient power.

The brief is actionable without further discussion. When ready, please include it in the next Luma expression sheet version.

— Lee
