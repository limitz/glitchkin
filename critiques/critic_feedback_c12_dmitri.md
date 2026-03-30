# Critic Feedback — Cycle 12
**Critic:** Dmitri Volkov, Character Design Lead
**Date:** 2026-03-30
**Subject:** Byte Float Annotation, Cosmo Side Glasses Refactor, Luma Neutral/Resting Expressions, Expression Sheet Metadata, Asymmetric Expression Mechanism Documentation

---

## VERDICT UPFRONT

Cycle 12 closed three items that I have been tracking across multiple notice cycles. All three are now closed. I want that acknowledged before anything else: when the team is given clear priority rankings and follows them, the work advances. That happened here.

However, "closed" is not the same as "excellent." Two of the three closures have specific technical shortcomings I will document in detail. And one item from my Cycle 11 Priority 2 list — Byte's neutral expression — is explicitly listed as open carry-forward in the Statement of Work. That is unacceptable at this stage in the pitch package.

Grade upfront: **B+**. The highest grade this package has received in three cycles. It is not an A because two deliverables have production-quality gaps, and because one clearly assigned item was not executed.

---

## SECTION 1: BYTE FLOAT-HEIGHT ANNOTATION — THIRD NOTICE CLOSED

**File:** `LTG_CHAR_lineup.png`
**Generator:** `character_lineup_generator.py`, lines 594–620

This item appeared in my Cycle 10 brief as Priority 1, was not addressed in Cycle 11, and I gave it a third notice. It is now done.

### What Was Implemented

The annotation consists of:
- A dashed horizontal line at `BASELINE_Y` spanning `byte_cx ± 70px` in `GROUNDFLOOR_COL = (100, 168, 200)` — a cool blue-gray distinct from the shared baseline color
- A label `"ground floor."` centered beneath Byte's column
- A small downward-pointing filled polygon arrow directly above the label, pointing toward the line itself

The footer text at the bottom of the image reads: `"Cycle 12 — ground floor annotation added."` — which documents the change in the asset itself.

### Assessment: Functional, But Borderline

The implementation is correct in intent and acceptable in execution. The annotation communicates that Byte floats above the ground plane. The dashed line is visually distinct from the shared baseline. The label is clear and appropriately positioned.

What it is not: production-quality dimension annotation. In my Cycle 10 brief I wrote that this annotation should "clearly communicate he hovers above the ground." It does that — barely. My specific concerns:

**1. The arrow direction is ambiguous.** The filled polygon points downward from mid-air toward the ground-floor line. This reads, at first glance, as an arrow pointing to where Byte currently is, not as an arrow pointing to the ground *below* him. A two-headed dimension arrow spanning the gap between Byte's lower limb tips and the ground-floor line — with a measured value in head units (e.g., "0.25 HU float gap") — would be unambiguous. What exists is a pointing device without a measurement.

**2. The annotation text "ground floor." reads as a label, not as a dimension.** A production-ready annotation says: *"Byte floats 0.25 HU above ground plane at rest."* This says: *"ground floor."* A junior animator reading this lineup knows the ground is there, but does not know how high to float Byte above it. The dimension value is missing.

**3. The annotation is local to Byte's column and reads as a caption, not as technical production annotation.** The font weight, the lowercase label, and the arrow construction are closer to an artistic callout than a technical drawing annotation. Compare to the height bracket system already in the file — those brackets are consistent, measured, and read as production reference. The Byte annotation reads like an afterthought in comparison.

**Verdict:** The item is closed. It is no longer a gap. But the annotation is the minimum viable version of what I asked for, not the best version. If this file goes into a pitch meeting, the Byte float gap will still generate questions because the annotation does not answer the follow-up question: *"How high does he float, exactly?"*

**Next cycle:** Upgrade to a two-headed dimension arrow with an explicit float-gap value in head units. Label: "float gap: 0.25 HU (canonical)". This should take thirty minutes.

**Grade: C+** — closed, functional, insufficient. The C+ is not for absence of effort; it is for absence of the specific production value the item requires.

---

## SECTION 2: COSMO SIDE-VIEW GLASSES REFACTOR

**File:** `LTG_CHAR_cosmo_turnaround.png`
**Generator:** `character_turnaround_generator.py`, lines 518–551, 708–715

This item has been open since Cycle 10. I gave it a second notice in Cycle 11. It is now closed.

### What Was Implemented

`_draw_cosmo_glasses()` now accepts an `is_side=True` parameter. The side-view draw logic — rim ellipse, NEG_SPACE lens cutout, ear arm rectangle — has been moved into the helper function. `draw_cosmo_side()` now calls `_draw_cosmo_glasses(draw, cx=front_x, gy=gy, gr=gr, is_front=False, is_back=False, is_side=True, front_x=front_x)`. The inline code is gone.

The consistency guarantee is restored: if the glasses geometry is updated in `_draw_cosmo_glasses()`, the side view updates automatically. This is the correct structural change and it is executed correctly.

### Does the Side View Now Match Front/3-Quarter Views?

Structurally: yes. The same rim value (`rim=3`), the same lens size scaling relative to `gr`, the same NEG_SPACE color — these are now shared. The ear arm extends to `back_x + int(gr * 0.33)` which is a reasonable estimate of the glasses temple arm reaching to the ear.

Visually: the lens placement is correct. `lens_cx = front_x - int(gr * 0.4)` places the lens slightly ahead of the front face edge, which is the correct reading for profile glasses. This matches how the front-view lens width reads at the face silhouette edge.

**One concern I will flag:** The `front_x` parameter passed into `_draw_cosmo_glasses()` is the same as the `cx` passed to the function. Inside the helper, `lens_cx = front_x - int(gr * 0.4)` — the lens center is placed relative to `front_x` which is `cx - int(head_depth * 0.60)`. This creates a small ambiguity: `cx` in the side view is the character center, not the head front edge. The parameter name `front_x=front_x` is doing double duty as both the function's `cx` argument and the `front_x` keyword argument. It works because the caller sets both to the same value. But a future engineer updating this code could reasonably read `cx=front_x` and `front_x=front_x` as a redundancy error rather than intentional geometry. A comment would close this ambiguity.

This is a maintenance concern, not a visual defect. The output is correct.

**Grade: A-** — the refactor is real, it is structurally correct, and the consistency guarantee is restored. The minus is for the `front_x` dual-use without documentation.

---

## SECTION 3: NEUTRAL/RESTING EXPRESSION PANEL

**File:** `luma_expression_sheet.png` (updated to 1210×886, 4×2 grid)
**Generator:** `LTG_CHAR_luma_expression_sheet.py`, `draw_neutral_resting()` and `draw_at_rest_curiosity()`

This is the most substantive new design work in Cycle 12. I will be thorough.

### Two New Expressions — Overview

Panel 7: **NEUTRAL / RESTING** — described as "Luma's calm, at-rest default face."
Panel 8: **AT-REST CURIOSITY** — described as "very mild interest; lowest-intensity expressive state."

Both were requested in my Cycle 11 brief under Priority 2/3. The request was for a neutral panel to anchor the emotional range. The team delivered two panels: the neutral itself, plus a second panel at the "just barely above neutral" register. I did not ask for two panels. I asked for one. That the team delivered two is either an insight or a mistake. I will assess which.

### Panel 7: Neutral/Resting

**Eye construction:**
- Left eye: `leh=24` (half-height 24px above/below center at full render scale before FACE_SCALE reduction)
- Right eye: `reh=22` (2px less)
- Both eyes have standard iris and pupil. No blush. No expression modifier.

The 2px aperture difference at full render scale (`200px` head diameter) translates to approximately 1.1px at panel scale (FACE_SCALE=0.55). That is below perceptual threshold in a rendered JPEG at panel size. You cannot see this asymmetry at panel scale. The asymmetry mechanism documented in Section 13 of `luma.md` correctly states this is "barely perceptible" — but barely perceptible is different from invisible. At panel scale, this reads as **symmetric**. The intent is correct. The execution at scale is invisible.

**Brow construction:** Nearly symmetric — left brow apex at `ley-36`, right brow apex at `rey-36`. The slight outward slope is consistent between both. This is correct for neutral.

**Mouth:** Gentle upward arc, closed. Radius and span comparable to Warmth but without the Warmth-narrowed eyes. This reads as "about to smile" — correct per bible Section 4.

**Squint test at thumbnail:** The NEUTRAL expression faces a real problem. Strip it down to a thumbnail. The face has: standard-aperture eyes, near-symmetric brows in low position, closed gentle-upward mouth, no blush. This is a face that communicates... nothing identifiable. That is the point — it is neutral — but it means the panel thumbnail does not add information to the sheet's emotional range story. It provides a zero-point, which is useful, but it does not "read" as a named expression. A director scanning this sheet at 20% zoom will see the warm-tan hoodie and warm-gray background and identify this as "the calm one" — they will not be able to distinguish it from a character at rest between takes.

This is the inherent problem with neutral expression documentation. It is still worth having for production reference. It does its job. But it is the weakest visual in the sheet, by definition.

**Grade for Neutral/Resting: B** — correct construction, correct concept, invisible asymmetry at production scale, necessary for the sheet's reference function.

### Panel 8: At-Rest Curiosity

**Eye construction:**
- Left eye: `leh=26` (2px wider than Neutral's left eye)
- Right eye: `reh=22` (unchanged from Neutral)
- Left eye pupil: shifted +2px toward center (`lex-6` to `lex+10` vs neutral's `lex-8` to `lex+8`) — "tracking something"

**Brow construction:**
- Left brow apex: `ley-42` (vs `ley-36` in Neutral — 6px higher at full render scale)
- Right brow: unchanged from Neutral at `rey-36`

**Mouth:** Identical to Neutral — same arc, same width, same weight.

At full render scale: left brow is 6px higher and left eye is 4px wider. At panel scale (FACE_SCALE=0.55): left brow is approximately 3.3px higher, left eye is approximately 2.2px wider than Neutral. These are genuinely small differences.

**The critical question: Are Neutral and At-Rest Curiosity distinct enough?**

Here is my honest answer: **They are not sufficiently distinct at panel scale.** The mouth is identical. The right eye is identical. The right brow is identical. The left eye difference is 2.2px at panel scale. The left brow difference is 3.3px at panel scale. These are below the threshold of fast visual recognition. Side by side in the 4×2 grid, a production designer will not be able to tell these two panels apart quickly without reading the label bar.

This is a design problem. Two expressions that occupy adjacent slots in an emotional range need to be distinguishable by someone who has NOT memorized which panel is which. These two do not pass that test.

**What would make them distinct:**
- AT-REST CURIOSITY's mouth should show the first hint of the expression reaching the mouth. Not an open smile — a very slight asymmetric upward pull at one corner (1-2px). The curiosity is beginning to manifest. The mouth is the last register. Let it show the first sign.
- The head tilt in AT-REST CURIOSITY should be encoded in the body language: a 2-3 degree collar tilt (`rotate_deg=2`) to suggest the body beginning to orient. Currently both panels use `rotate_deg=0`.
- The pupil offset in AT-REST CURIOSITY is the only visible differentiation. Make it bigger: shift both pupils toward the "object of interest" direction more aggressively. Curiosity has a direction. Show it.

**Grade for At-Rest Curiosity: C+** — the concept is correct, the documentation intent is sound, but the visual execution does not differentiate sufficiently from Neutral at panel scale. These two expressions blur together. That defeats the purpose of having both.

### The 4x2 Grid: Does It Work as a Sheet?

The expansion from 3×2 to 4×2 is structurally correct. The layout matches the metadata specification. The new panels are tagged "[NEW]" in soft green text in the label bar.

Row 1 (heightened states): Reckless Excitement / Worried Determined / Mischievous Plotting / Settling Wonder
Row 2 (lower register + baseline): Recognition / Warmth / Neutral Resting / At-Rest Curiosity

The emotional arc from Row 1 to Row 2 still works. The problem is the right end of Row 2: Recognition flows to Warmth flows to Neutral flows to At-Rest Curiosity. That arc makes narrative sense (recognition → earned connection → rest → mild attention returning), but the last two panels are too visually similar to anchor the arc's endpoints.

**The WARMTH prev_state annotation correction is confirmed.** "← was: ANY EARNED MOMENT" is now in place, replacing the over-specific "← was: RECOGNITION" from Cycle 11. This was my note. It was acted on correctly.

---

## SECTION 4: EXPRESSION SHEET METADATA

**File:** `luma_expression_sheet_metadata.md`

This document is exactly what I asked for. I will verify the specific requests from my Cycle 11 brief:

**1. Head unit reference:** Present. `1 head unit = 200px` at full render scale, `≈ 110px` at panel scale (FACE_SCALE=0.55). Canvas dimensions: 1210×886px. Panel size: 280×390px. Grid: 4×2. All present.

**2. Version history:** Present. v1.0 (Cycle 11, 6 expressions) → v2.0 (Cycle 12, 8 expressions). The change log documents both the structural expansion and the WARMTH annotation correction, and credits my Cycle 11 note. This is the correct way to maintain version history.

**3. Expression index:** Present. All 8 expressions listed with background color, hoodie color, and body language summary. This is usable production reference.

**4. Sneaker width documentation:** Present. `hw = int(hu × 0.52) = 73px` — the Cycle 11 canonical normalization is documented in the metadata. This closes a cross-document consistency gap that had existed since Cycle 11.

**Is it actually useful for production?**

Yes, with one gap. The metadata documents the canvas geometry and expression index correctly. What is missing: the face draw function signatures. A layout TD or technical animator picking up this work needs to know which function drives which panel — the metadata indexes expressions by slot and visual properties, but does not list the function name. `draw_neutral_resting()` does not appear in the metadata. This is a minor gap, but it is the one thing a developer would want that is not there.

**Grade for Metadata: A-** — complete, correct, genuinely usable. The minus is for the missing function-to-slot mapping.

---

## SECTION 5: ASYMMETRIC EXPRESSION MECHANISM — SECTION 13

**File:** `luma.md`, Section 13, lines ~488–490

My Cycle 11 brief asked for explicit documentation of Luma's asymmetric expression mechanism in the character bible. This exists now. Let me assess it.

Section 13 is a single paragraph. It documents:
- The left eye as the "lead eye" — fractionally more open at rest (the Neutral panel now encodes this)
- The intensity scaling: asymmetry amplifies with emotional intensity
- The specific asymmetry per expression: Reckless Excitement (left wider, right pupil shifted), Recognition (left brow sky-high, right level), Mischievous Plotting (left brow launches, right nearly vanishes)
- The inversion for negative states: Worried/Determined compresses to near-symmetry — "symmetric Luma reads as maximal stress or shutdown"
- The animator guidance: "left eye aperture and brow height as the primary dials: every +10% asymmetry toward the left eye reads as +1 unit of Luma's characteristic reckless personality"

**This is exactly what I asked for.** The mechanism is documented. It is discoverable without code access. The formulation "symmetric Luma reads as maximal stress or shutdown" is the key insight and it is stated clearly. The "+10% asymmetry = +1 unit of personality" framing is memorable and repeatable.

**One technical note:** Section 13 does not include a table. The described mechanism — six expressions, each with a specific asymmetry mode — would be substantially more useful as a reference table than as a prose paragraph. An animator in the middle of a production day does not have time to parse "in Mischievous Plotting the entire left brow launches above the resting arc while the right brow nearly vanishes behind the squinted left lid." They need: Expression | Left Eye | Right Eye | Left Brow | Right Brow | Asymmetry Mode. That table does not exist.

This is a documentation structure complaint, not a content complaint. The content is correct. The structure is not optimized for production reference.

**Grade for Section 13: B+** — correct content, correct placement, missing the reference table structure that would make it genuinely fast to use on a production floor.

---

## SECTION 6: BYTE NEUTRAL EXPRESSION — EXPLICITLY NOT ACTIONED

The Statement of Work for Cycle 12 includes this under Open Items: *"Neutral expression for Byte: Dmitri Volkov flagged this alongside Luma's. Not yet actioned."*

I flagged this in my Cycle 11 brief as Priority 2. The Luma expression sheet was Priority 2 item #1. Byte's neutral expression was Priority 2 item #3. The team addressed Luma's. They did not address Byte's.

I understand prioritization. I do not accept this prioritization.

The Byte expression sheet now has a documented sibling (Luma's sheet) that includes a neutral panel. The Byte sheet does not. This asymmetry in the documentation set is a production problem: a director trying to establish a baseline communication register for Byte — "what does he look like when nothing is happening?" — has to read Expression 1 (DEFAULT GRUMPY NEUTRAL) in the character bible rather than being able to point to a panel and say "that one."

Expression 1 in `byte.md` Section 7 documents the Default Grumpy Neutral: flat line pixel eye, 60% aperture, limbs close to body. This is sufficient documentation in the bible. It is not sufficient documentation in the expression sheet context. The sheet shows eight emotional states. None of them is his resting face. This is the same gap that existed in Luma's sheet before Cycle 11.

Byte's sheet should have been updated in tandem with Luma's. It was not.

**Status: Carries to Cycle 13. This is now its second notice specifically as an expression sheet item (third notice counting the Cycle 11 brief).**

---

## SECTION 7: OVERALL CYCLE ASSESSMENT

### What Cycle 12 Resolved

- **Byte float-height annotation**: closed, functional, insufficient dimensioning — **done, needs upgrade**
- **Cosmo side-view glasses**: refactored to shared helper, consistency guarantee restored — **done**
- **Luma neutral expression panel**: exists, correct concept, two panels (Neutral + At-Rest Curiosity) — **done, At-Rest Curiosity too close to Neutral**
- **Expression sheet metadata**: complete and correct — **done**
- **Asymmetric expression mechanism documentation**: exists in Section 13 — **done, missing reference table**

### What Must Be Done in Cycle 13

Priority ranking, no exceptions:

**Priority 1 — Must fix this cycle:**
1. **Byte neutral expression panel** — add to `byte_expressions_generator.py`. This is a DEFAULT GRUMPY NEUTRAL panel at the same structural quality as the Luma Neutral. It is not optional at this stage of the pitch package.
2. **At-Rest Curiosity differentiation** — either (a) add asymmetric mouth pull to differentiate it visually from Neutral, or (b) remove it from the sheet if it cannot be made visually distinct. Two expressions that blur together at panel scale are worse than one expression.

**Priority 2 — Should fix:**
3. **Byte float annotation upgrade** — two-headed dimension arrow, explicit "0.25 HU float gap" value, production-spec annotation weight. Replace the current caption-style annotation.
4. **Section 13 reference table** — add left/right eye and brow state table for each expression. Prose description is not production reference.

**Priority 3 — Polish:**
5. **Metadata function-to-slot mapping** — add function names to the expression index in `luma_expression_sheet_metadata.md`.
6. **Style Frame 03** — referenced in SOW as spec approved, background pending. When is this shipping?

---

## CYCLE 12 GRADE

**Grade: B+**

This is the team's strongest cycle. Three multi-cycle items are closed. The expression sheet expansion was real design work. The metadata document is genuinely useful. Section 13 is the character bible annotation the package needed.

The B+ is not an A because:
- The Byte float annotation is the minimum viable version, not the production version
- At-Rest Curiosity cannot be distinguished from Neutral at panel scale — two expressions that look like the same expression is a net negative, not a net positive
- Byte's neutral expression was explicitly noted as not actioned in the SOW — that is not a surprise carry, that is a known omission

The A requires all three of those to be resolved. They are not hard problems. Two of them are thirty-minute fixes. One (Byte neutral expression) is two to three hours of work. Schedule it.

---

*"Three notices and a fourth notice might become five. I have been patient. The team has been productive. Byte's face needs an anchor. Give it one."*

*Dmitri Volkov — Character Design Critic*
*"Production-ready is not a destination. It is a daily practice."*
