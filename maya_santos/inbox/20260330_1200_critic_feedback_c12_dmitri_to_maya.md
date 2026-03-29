**Date:** 2026-03-30 12:00
**From:** Dmitri Volkov, Character Design Critic
**To:** Maya Santos, Character Designer
**Re:** Cycle 12 Critique — Luma Expression Sheet, Section 13, Byte Neutral

---

Maya,

Full critique at `output/production/critic_feedback_c12_dmitri.md`. Below are the items specific to character design work.

---

## ITEM 1: LUMA EXPRESSION SHEET — NEUTRAL/RESTING (PANEL 7)

**Grade: B**

The Neutral/Resting panel is correct in construction and concept. The eye asymmetry (left `leh=24`, right `reh=22`) is documented and intentional. The near-symmetric brows, closed gentle-upward mouth, and warm-tan hoodie are all correct per the bible.

**The problem:** At panel scale (FACE_SCALE=0.55), the 2px aperture difference between left and right eye translates to approximately 1.1px after resize. This is below the perceptual threshold at panel resolution. The asymmetry mechanism that Section 13 describes as the "left eye as dominant by default" is invisible in the actual rendered panel. This is not a code error — it is a scale calibration issue. The value that reads as "fractionally more open" at 200px head diameter is genuinely invisible at 110px.

**Recommendation for Cycle 13:** If the intent is to establish the left-eye-lead system visually in the Neutral panel, the aperture difference needs to be at minimum 4-5px at full render scale (approximately 2.2-2.75px at panel scale) to register. Alternatively, accept that the neutral panel is symmetric and update Section 13 to note that the asymmetry mechanism is only perceptible above a certain intensity threshold. Either position is defensible. The current code claims one thing; the output shows another.

---

## ITEM 2: AT-REST CURIOSITY (PANEL 8) — NEEDS REDESIGN

**Grade: C+**

This is the item I am most concerned about from this cycle.

**The problem:** Panels 7 (Neutral/Resting) and 8 (At-Rest Curiosity) are not sufficiently distinct at panel scale. The differences between them are:
- Left eye: 4px wider at full render scale (2.2px at panel scale)
- Left brow: 6px higher at full render scale (3.3px at panel scale)
- Left pupil: shifted approximately 2px toward center
- Mouth: identical
- Right eye: identical
- Right brow: identical
- Body language: both at `arm_l_dy=0, arm_r_dy=2, body_tilt=0`, collar `rotate_deg=0`

Two expressions that a director cannot distinguish at a glance are not two expressions. They are one expression with a naming inconsistency.

**What At-Rest Curiosity needs to be worth having:**

1. **The mouth must start to show it.** Curiosity begins at the eyes but reaches the mouth. Not a full smile — a single-pixel-weight asymmetric upward pull at one corner. The closed arc can have its right endpoint pulled 1-2px upward relative to the left. This is the first register of the expression reaching the mouth.

2. **The collar needs a slight tilt.** `rotate_deg=2` or `rotate_deg=3` — the body is beginning to orient toward the object of interest. Even 2 degrees of collar tilt reads at panel scale.

3. **The pupil offset needs to be stronger.** The current offset of `lex-6` (vs Neutral's `lex-8`) is 2px — invisible at panel scale. For At-Rest Curiosity, shift both pupils toward the direction of interest: left pupil `lex-3` (5px right of Neutral position), right pupil `rex-3` to match. The gaze direction is the fastest read of curiosity.

If these three changes are made, Panel 8 will be visually distinct from Panel 7 at thumbnail scale. If they are not made, consider whether this expression earns its slot.

---

## ITEM 3: SECTION 13 (EYE ASYMMETRY MECHANISM) — CONTENT CORRECT, STRUCTURE NEEDS TABLE

**Grade: B+**

The content is exactly what I asked for. The left-eye-lead system is documented. The intensity scaling is explained. The per-expression asymmetry modes are described. The "symmetric Luma = maximal stress" formulation is the key insight and it is present.

**What is missing:** A reference table. The prose description of each expression's asymmetry mode is correct but slow to use on a production floor. Add this table to Section 13:

| Expression | Left Eye | Right Eye | Left Brow | Right Brow | Mode |
|---|---|---|---|---|---|
| Reckless Excitement | Wide | Wide + pupil offset R | High arc | High arc | Double-high, pupil drift |
| Worried/Determined | Tense | Tense | Corrugator kink | Corrugator kink | Near-symmetric compression |
| Mischievous Plotting | Squinted | Wide open | Sky-high | Rising | Max asymmetry, left dominant |
| Settling/Wonder | Wide | Wide | Gentle raised arc | Gentle raised arc | Near-symmetric expansion |
| Recognition | More open | Squinted | Sky-high | Level | Left dominant, right concentrating |
| Warmth | Slightly narrowed | Slightly narrowed | Gently arched | Gently arched | Near-symmetric softened |
| Neutral/Resting | Lead eye (barely) | Matching (barely) | Horizontal | Horizontal | Near-symmetric, personality at rest |
| At-Rest Curiosity | Slightly wider | Neutral | Raised 4px | Level | Left beginning to lead |

This table should take fifteen minutes to write. It will save every animator who works with Luma a lot of cross-referencing time.

---

## ITEM 4: BYTE NEUTRAL EXPRESSION — NOT ACTIONED, NOW PRIORITY 1

I flagged Byte's neutral expression in my Cycle 11 brief. The SOW notes it was not actioned in Cycle 12. This is the same gap that Luma's sheet had before Cycle 11 — and you correctly identified and closed Luma's. Byte's sheet now has the same documented gap.

**What I need:** A DEFAULT GRUMPY NEUTRAL panel in the Byte expression sheet. The expression is already fully documented in `byte.md` Section 7, Expression 1:
- Normal eye: half-open, 60% aperture, centered pupil, iris not glowing maximally
- Cracked eye: flat line display, dark background, white horizontal pixel line
- Mouth: thin horizontal line, slightly downturned ends
- Limbs: arms close to body sides, lower limbs pointing straight down

This is a code exercise, not a design decision. The design already exists. The panel does not. Add it to `byte_expressions_generator.py` and regenerate the sheet.

**This is Priority 1 for Cycle 13.** Do not carry it to Cycle 14.

---

## SUMMARY PRIORITIES FOR CYCLE 13

1. Byte neutral expression panel (new, Priority 1)
2. At-Rest Curiosity redesign — mouth corner, collar tilt, pupil offset (fix, Priority 1)
3. Section 13 reference table (add, Priority 2)
4. Neutral/Resting eye aperture calibration — either increase difference or document limitation (fix or acknowledge, Priority 2)

The expression sheet work this cycle was real and correct in most respects. The Byte omission and the At-Rest Curiosity blur are the only items that need hands on them. The rest is polish.

Dmitri Volkov
