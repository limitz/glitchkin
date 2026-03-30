# Critique — Cycle 9 (Cycle 17 Work Review)
**Critic:** Dmitri Volkov, Character Design Lead
**Date:** 2026-03-29
**Subject:** Luma Expression Sheet v002, Grandma Miri Expression Sheet v001, Character Lineup v003, Cosmo Expression Sheet v002 (SKEPTICAL check)

---

## PREAMBLE

The Char Refinement Directive issued by Alex Chen this cycle is exactly the document this production has needed since Cycle 6. It names the three-tier line weight system, mandates construction guides, and codifies the squint test as a pass/fail production standard. It is a good directive. I am reviewing the deliverables against it without mercy.

My assessment follows in order of assigned priority.

---

## ITEM 1: Luma Expression Sheet v002

**Tool:** `LTG_TOOL_luma_expression_sheet.py`
**Output:** `LTG_CHAR_luma_expression_sheet.png`
**Standard:** Char Refinement Directive — all five criteria

### Squint Test (10% scale, pass/fail per expression)

I am applying the directive's own language: squint the sheet. Every expression must be identifiable without reading its label.

- **CURIOUS:** Brows asymmetrically lifted (one higher), gaze offset right, hair at default height. At thumbnail the asymmetric brow read is the only differentiator from DETERMINED. The hair profile is identical to DETERMINED. Marginal pass — carried by the gaze offset.
- **DETERMINED:** Hair pulled tight, no blush, pressed-flat mouth, forward lean offset. At thumbnail: hair silhouette is narrower than CURIOUS and SURPRISED (tight variant). This is the correct instinct — the tight hair variant does change the silhouette. **Pass.**
- **SURPRISED:** Excited hair (tallest variant), fully open eyes, open-oval mouth with blush-to-hoodie-orange. The excited hair creates the single most distinctive silhouette change across the entire sheet — the hair mass is measurably taller and wider. **Passes cleanly — the strongest read on the sheet.**
- **WORRIED:** Drooped hair (shortest crown), furrowed brows, downturned mouth, blue-tinted hoodie. At thumbnail the drooped hair creates a lower crown line than neutral/default. The blue hoodie is a significant secondary signal. **Pass — with caveat** (see line weight note below).
- **DELIGHTED:** Excited hair, squinted eyes, open smile with teeth, maximum blush, full warm-orange hoodie. At thumbnail the wide open smile catches light and the hair matches SURPRISED in height. **FAIL: DELIGHTED and SURPRISED share the same excited-hair silhouette.** At 10% scale, both panels present as: tall wide hair mass + light catching in face center. The differentiation relies entirely on mouth shape (oval vs wide-open), which collapses at small scale. The directive's own language applies: "if two expressions share a thumbnail-scale silhouette, one of them needs a body-language anchor added." DELIGHTED has no body-language differentiation from SURPRISED.
- **FRUSTRATED:** Tight hair, half-lid eyes, furrowed brows, frown, blue-gray hoodie. At thumbnail: narrow hair profile (tight variant), cooler hoodie tone, compressed face center. Distinguishable from DETERMINED (same tight hair) primarily by cooler hoodie and compressed eye area. **Marginal pass** — the differentiation at thumbnail is color-dependent (warm hoodie vs cool hoodie), not silhouette-dependent. Color differentiation is fragile (print, grayscale reproduction, viewing distance). A body-language anchor between FRUSTRATED and DETERMINED would make this a clean pass. Currently it is a conditional pass.

**Squint test result: 4 clean passes, 1 fail (DELIGHTED/SURPRISED overlap), 1 conditional pass (FRUSTRATED/DETERMINED color-dependent).**

### Construction Guides

Construction circle and cross-hair guides are rendered as RGBA overlays at 48/255 alpha — approximately 19% opacity. They are present. They are visible at full size. At panel render scale (380×356 downscaled from 760×712) they are faint but readable. **This requirement is met.** The directive is satisfied on this point. Credit where it is due.

### Line Weight System

This is where the implementation falls short of the directive's stated standard. I am reading the tool code directly.

The weight implementation in the tool:

- Silhouette outlines: 8px at 2x render → 4px output. **The directive specifies 3px at 1920 canvas width.** This sheet is 1200px wide with a 2x render pipeline, so effective silhouette weight should scale to approximately 3px × (1200/1920) × 2 = ~3.75px. The 4px result is within range. **Acceptable.**
- Eyebrow lines (`polyline` at `width=10` at 2x → 5px output): This is the problem. Eyebrow lines are drawn at the same weight as the silhouette outline. The directive states interior structural lines must be 2px. Brows are interior structure, not silhouette. At 5px output weight, Luma's brows compete with her head outline for visual dominance. This collapses the three-tier hierarchy precisely where the directive demands it be enforced — on the face, where expression legibility depends on clear weight differentiation between outline and feature.
- Interior lines (upper eyelid arc: `width=4` at 2x → 2px output): Correctly implemented. **Pass.**
- Crinkle lines (eye-corner detail: `width=3` at 2x → 1.5px output): Close to spec. **Acceptable.**
- Nose arc (`width=4` at 2x → 2px): This is a surface detail element that should be 1px per directive. It is running at 2px. Minor violation.
- Ear outlines (`width=5` at 2x → 2.5px): Ears are silhouette-adjacent but interior to the head circle. Running at 2.5px — between silhouette and interior structure. Ambiguous implementation.

The brow weight failure is the primary problem. A brow line at silhouette weight makes the face read as a flat mass of equal-weight lines rather than a constructed face with clear figure-ground hierarchy. This is exactly the defect the directive was written to address.

**Line weight verdict: interior structure (brows) at silhouette weight — fails Part 1, Section 2 of the directive.**

### On-Model Consistency

- Hair curl count: 5 curls defined in `curls` list. **Correct. LOCKED spec met.**
- Mitten hands: the collar/hoodie rendering shows no hand detail. Hands are not rendered on the expression sheet (bust format). Cannot verify, but not a defect in a bust-format sheet.
- Head shape: near-circle (HR = 105, which yields a perfect circle at 1x). **Correct.**
- Hoodie color: base is `HOODIE = (232, 114, 42)` = #E8722A. **Correct against spec.**

### Expression Depth (Emotional Triangle)

Per directive, primary expressions must operate on all three levels: eyes/brows, mouth, body.

This is a bust-format sheet. Body language is limited to hair posture and hoodie collar tint. The tool implements hair variant (default/tight/excited/drooped) as the primary body-language signal — this is a constrained but valid interpretation for a head-focused expression sheet. However, the directive calls out "body posture must agree with the face OR be deliberately contradictory." The hoodie color tinting by mood is a proxy for body language, but it is not the same as a posture anchor.

For a full-figure expression sheet, this would be a defect. For a bust-format head sheet, I will note it as a production limitation rather than a violation, provided the full-figure character lineup and scene poses handle body language correctly.

**Grade: C+**

The sheet is improved over prior iterations. Construction guides are present. The 6-expression 3×2 format is correct. The squint test failure on DELIGHTED/SURPRISED and the brow-weight violation of the directive are the two blocking defects. The conditional pass on FRUSTRATED/DETERMINED adds a third concern. This sheet is not pitch-ready as-is. It is a solid intermediate draft that needs a targeted revision pass.

---

## ITEM 2: Grandma Miri Expression Sheet v001

**Tool:** `LTG_TOOL_grandma_miri_expression_sheet.py`
**Output:** `LTG_CHAR_grandma_miri_expression_sheet.png`
**Standard:** grandma_miri.md v1.2, Char Refinement Directive

### Does It Exist?

Yes. The directive named Miri's missing expression sheet as GAP 1 CRITICAL. It now exists. That is a meaningful production win — Miri had no visual emotional range reference for seven cycles. She has one now. I will be honest about what it does and does not accomplish.

### Expression Count and Mapping

The directive specified six expressions:
1. NEUTRAL / WARM
2. KNOWING SMILE
3. QUIET CONCERN
4. GENUINE LAUGH
5. FOCUSED / WORKING
6. SKEPTICAL / AMUSED

The delivered sheet has five expressions: WARM/WELCOMING, NOSTALGIC/WISTFUL, CONCERNED, SURPRISED/DELIGHTED, WISE/KNOWING.

This is a four-in-five mapping problem. WARM/WELCOMING corresponds to NEUTRAL/WARM (directive spec 1). SURPRISED/DELIGHTED corresponds to GENUINE LAUGH (directive spec 4). WISE/KNOWING corresponds to KNOWING SMILE (directive spec 2, partially). CONCERNED corresponds to QUIET CONCERN (directive spec 3). NOSTALGIC/WISTFUL has no direct equivalent in the directive specification — it replaces both FOCUSED/WORKING (directive spec 5) and SKEPTICAL/AMUSED (directive spec 6). The directive's SKEPTICAL/AMUSED — described as "warm skepticism, not cold judgment, one brow arched, closed-mouth smirk, upright arms settled" — is absent. The directive's FOCUSED/WORKING — "eyes narrowed, head tilted toward work, Miri at her engineering brain" — is also absent.

A five-expression sheet against a six-expression spec is a gap. The gap is specifically in the expressions that define Miri's professional identity (FOCUSED/WORKING) and her interpersonal sophistication (SKEPTICAL/AMUSED). Without these two, the sheet presents Miri as reactive (concerned, surprised, welcoming, nostalgic) but not active. Her engineering-brain mode and her warm-skepticism mode — the two expressions that make her interesting as a character rather than just as a warm authority figure — are missing.

### Squint Test

Five expressions, 5-panel layout. Applying the test:

- **WARM/WELCOMING:** Upright posture, glasses present, silver bun crown, closed-mouth smile. At thumbnail: the bun-and-glasses combination creates a distinctive crown silhouette. **Pass.**
- **NOSTALGIC/WISTFUL:** Brow slightly raised, eyes softened, similar upright posture. At thumbnail: nearly identical silhouette to WARM/WELCOMING. **FAIL.** Two panels with the same crown silhouette, same body posture, differentiation only in brow and mouth position — both of which collapse at small scale.
- **CONCERNED:** Brow descended, mouth tightened, slight forward lean per spec. At thumbnail: if the forward lean is implemented with sufficient body tilt, this could differentiate. From the rendered image the lean is subtle — the silhouette change is minimal. **Conditional fail** — the face-level read differentiates at medium scale but likely collapses at 10%.
- **SURPRISED/DELIGHTED:** Head tilted back, wide open mouth showing teeth, maximum cheek press, body leaning back. This is the strongest expression on the sheet. The open mouth and backward lean create a genuine silhouette change. **Pass — the only expression that clearly distinguishes itself at thumbnail.**
- **WISE/KNOWING:** Closed-mouth smile with cheek press, head at neutral angle, upright. At thumbnail: similar to WARM/WELCOMING again. The "knowing smile" is defined in the directive as "cheek press that makes her face width visually widen" — this is the intended thumbnail differentiator. If the cheek width is correctly implemented, it reads. From the rendered image, the cheek width change between WARM and WISE is present but subtle.

**Squint test result: 1 clear pass (SURPRISED/DELIGHTED), 1 pass (WARM/WELCOMING), 2 fails or conditional fails (NOSTALGIC/CONCERNED/WISE are too close at thumbnail).**

This is the single most critical failure on this sheet. Three expressions in the upper row share nearly identical thumbnail silhouettes. The directive's squint test requirement — "every expression distinct from all others at small scale" — is not met for at least two of the five.

### On-Model Consistency

Positive observations:
- Glasses are present and correctly rendered as a defining silhouette element (the directive spec mentions them as part of MIRI-A design — they were not in the character bible spec but are implemented here and they work).
- Bun-and-chopstick crown reads correctly at panel scale.
- Skin tone is correctly applied at approximately `#8C5430` deep warm brown.
- Cardigan terracotta rust is present and the correct warm-orange family tone.

Problems:
- Crow's feet: the tool spec states "always present" at 50% line weight. At panel scale, these are present but they are indistinguishable from general facial line weight. They do not appear to be rendered at the mandated 50% weight reduction. This is a minor violation but it matters because crow's feet are part of Miri's visual identity specification.
- Permanent cheek blush (#D4956B at 25% opacity): present across expressions — confirmed in the tool's `BLUSH_PERM` color value `(212, 149, 107)`. This is approximately correct for the hex spec. **The blush permanence rule appears met.**
- The SURPRISED/DELIGHTED expression shows Miri with a large open mouth and visible teeth — consistent with the "GENUINE LAUGH" description in grandma_miri.md Section 9 Expression 5 ("open mouth, upper teeth visible as a clean rectangle, wide oval"). **This is correctly implemented.**
- The body proportions in the sheet read compact and settled — the 3.2 head height impression is present. This is correct for Miri's character.

### Expression Depth

The SURPRISED/DELIGHTED expression is the only one that operates fully on all three levels simultaneously: eyes pressed into crescents (eye region), open mouth with teeth (mouth region), backward body lean and shoulders raised (body posture). The other four expressions operate primarily on the eye/brow and mouth registers without clear body posture differentiation. The directive requires at minimum 2 of 3 levels for all expressions, 3 of 3 for primary expressions. WARM, NOSTALGIC, CONCERNED, and WISE appear to be face-only reads.

**Grade: C**

The sheet exists, which was Priority 1 this cycle and is a real achievement. But existence is not quality. The squint test fails on three of five expressions. Two directive-specified expressions (FOCUSED/WORKING and SKEPTICAL/AMUSED) are absent and replaced by a NOSTALGIC/WISTFUL expression that does not serve Miri's full character range. The face-only expression design on four of five panels ignores the directive's body-language requirement. This sheet is a first-draft placeholder, not a production-ready model document.

---

## ITEM 3: Character Lineup v003

**Output:** `LTG_CHAR_lineup.png`
**Standard:** Char Refinement Directive Part 4, Section 4; production Bible proportions

### Height Proportions

Lineup shows: Luma (3.5 heads / 280px), Byte (~Luma chest height / 162px), Cosmo (4.0 heads / 320px), Miri (3.2 heads / 256px). The height relationships are correct per spec. Cosmo is tallest. Luma is second. Miri is shortest human. Byte floats at approximately chest height relative to Luma. The proportional annotations are present and legible. **This is well-executed production documentation.**

### Silhouette Read

Applying the squint test to the full ensemble:

- **Luma:** Orange trapezoid body + dark hair cloud + wide sneakers. Immediate read. **Pass.**
- **Cosmo:** Tall narrow blue-striped torso + round glasses as the dominant facial element + flat hair cap. The glasses at lineup scale (320px height) are clearly the primary read. **Pass.** One note: the tall narrow torso against Luma's shorter wider torso creates an excellent contrast pair. This is correct show design.
- **Byte:** Cyan oval with rectangular appendages floating above ground. The float gap annotation (0.25 HU) is correctly marked. The body shape reads as oval at lineup scale — not chamfered cube. **This is now consistent with the corrected character spec. Pass.**
- **Miri:** The Miri in this lineup is the problem. The Miri figure presents as a brown rectangular block with what appears to be rabbit-ear appendages extending upward. The bun-chopstick crown is either not rendered correctly or is reading as something entirely different at lineup scale. At thumbnail the Miri figure looks like a different character than the Miri in the expression sheet. The "wide compact silhouette" with "silver bun crown" that should read immediately does not read. The visual family coherence of the ensemble is broken at Miri's position.

At lineup scale (256px height / 3.2 heads = 80px head unit), Miri's head should be approximately 80px. The silver-white bun should be visible as a distinct crown element — it is the primary thumbnail identifier per grandma_miri.md Section 10. What appears in the lineup is not reading as a settled warm adult with a silver bun. It is reading as an abstract brown form.

Additionally: the **cardigan** — Miri's primary silhouette element (wide A-shape lower body, oversized fall to mid-thigh) — does not appear to be rendering distinctly from the figure's body geometry. The cardigan was supposed to create a wider-than-head lower silhouette that distinguishes Miri from all other characters. This is not reading.

**Lineup silhouette verdict: 3 characters read cleanly (Luma, Cosmo, Byte), 1 character fails (Miri).**

### Ensemble Visual Family

The three human characters (Luma, Cosmo, Miri) do not read as a coherent visual family at lineup scale. Luma and Cosmo are clearly in the same show — they share construction logic, visible clothing design, facial legibility. Miri's lineup representation lacks this legibility. This is a direct consequence of Miri's full-body design work being less developed than the other characters at this point in production. The expression sheet exists, but the full-body lineup representation is below the quality threshold of the other three figures.

### Grade: B-

The lineup functions as a proportional reference document and accurately represents the height relationships. The format is clean, the annotations are correct, and three of four characters read at thumbnail. The Miri failure drops this from a B+ to a B-. A character lineup that cannot correctly represent one of its four principals is not pitch-ready, but the structural foundation is solid and the Miri problem is correctable.

---

## ITEM 4: Cosmo Expression Sheet v002 — SKEPTICAL Expression Check

**Output:** `LTG_CHAR_cosmo_expression_sheet.png`
**Focus:** Does SKEPTICAL read with backward lean?

### What the Cycle 16 Fix Was Supposed to Do

The tool header explicitly documents the fix: `SKEPTICAL body_tilt: -3 → +6 (backward lean, body-language anchor for thumbnail legibility)`. The comment explains the reasoning: "-3 (barely forward) was face-only expression, didn't read at thumbnail. +6 backward = leaning away from the board, skeptical containment posture."

The `tilt_off = int(body_tilt * 0.4)` formula means the actual pixel offset is `6 × 0.4 = 2.4px` per unit of body height. For a torso of approximately `hu × 1.2 = ~96px` (at 80px head unit), the visual lean displacement at the top of the torso is approximately `2.4px`. This is not a visually meaningful lean. The formula converts a degree-like input into a pixel offset that is far smaller than what the number implies.

### Does It Read?

Looking at the SKEPTICAL panel in the rendered sheet: Cosmo's body appears essentially upright. The backward lean is not legible. The expression is differentiated from NEUTRAL primarily by the one raised eyebrow (viewer's right) and the slightly tilted glasses. This is exactly the "face-only expression" problem identified in the original critique and supposedly addressed by the Cycle 16 fix.

The fix changed the number. The fix did not change the effective visual output. The `tilt_off` formula is the culprit — a multiplier of 0.4 means a `body_tilt` value of 6 produces only 2.4px of displacement. A genuinely visible backward lean at this character height requires a displacement of 8–12px at the torso top, which would require `body_tilt` of 20–30 with the current formula, or a formula multiplier increase.

Compare SKEPTICAL to SURPRISED: SURPRISED has `body_tilt: 5` and shows `arm_l_dy: -18, arm_r_dy: -22` (arms snapping up). The backward lean impression in SURPRISED is carried primarily by the arm raise, not the body tilt. SKEPTICAL has `arm_l_dy: -8, arm_r_dy: -5` — arms only slightly raised, not enough to anchor the backward lean read.

**SKEPTICAL backward lean: the code says it was fixed. The output does not show it was fixed. This is a formula-level failure, not a spec ambiguity.**

At thumbnail scale, SKEPTICAL and NEUTRAL share nearly identical body profiles. SKEPTICAL is differentiated only by the single raised eyebrow, which collapses at 10% scale. This is the same failure I identified as the original problem.

### Grade: B- (expression sheet overall)

The sheet is populated, the flow annotations are excellent, the panel format is professional. The SKEPTICAL backward lean implementation is a failure — the number was changed but the effective output was not changed due to formula scaling. The WORRIED and SURPRISED expressions are the strongest new additions this cycle. FRUSTRATED/DEFEATED is well-differentiated (slumped body, closing notebook, forward lean that reads because of the notebook interaction). The SKEPTICAL failure is the primary blocking issue for this sheet.

---

## OVERALL CYCLE 17 CHARACTER WORK ASSESSMENT

### What Is Working

1. The Char Refinement Directive itself — Alex Chen's document is the best production standards document this project has produced. It names the problems clearly.
2. Construction guides on the Luma sheet — present and implemented.
3. Miri expression sheet exists — a seven-cycle gap is filled, even if the first version is a C.
4. Lineup height proportions and annotations — clean, correct, useful.
5. Byte oval body in the lineup — consistent with character spec, the chamfered-cube issue appears resolved.
6. Cosmo expression sheet flow annotations — excellent production practice, these are exactly right.

### What Is Not Working

1. **Luma DELIGHTED/SURPRISED squint test failure** — two expressions share the same excited-hair silhouette without body-language differentiation.
2. **Luma brow line weight** — brows rendered at silhouette weight (5px output), violating the three-tier hierarchy mandated by the directive.
3. **Miri expression sheet — three of five panels fail squint test** — NOSTALGIC, CONCERNED, and WISE are face-only differentiations that collapse at thumbnail.
4. **Miri expression sheet — missing two directive-specified expressions** — FOCUSED/WORKING and SKEPTICAL/AMUSED are absent.
5. **Cosmo SKEPTICAL backward lean** — the formula multiplier (×0.4) negates the numeric fix; the lean does not read in the output.
6. **Miri lineup representation** — does not match the expression sheet character; bun-chopstick crown and cardigan silhouette are not reading at lineup scale.

---

## TOP 3 PRIORITY FIXES

**Priority 1: Luma DELIGHTED body-language anchor**

Add a body-language differentiator to DELIGHTED that is not shared with SURPRISED. SURPRISED is already defined by the open-oval mouth and the shock posture. DELIGHTED should have a different body signal: head tilt back (like Miri's LAUGH spec — "head often tips back slightly"), or arms out to sides (the "I can't believe this is happening" open-arms posture), or a visible jump/rise. The hair silhouette cannot be the differentiator because it is identical. The fix requires a body posture change that reads at 10% scale — minimum 12px body displacement or silhouette change at panel size.

**Priority 2: Miri expression sheet rebuild — body-language anchors and missing expressions**

Three problems, one fix: rebuild the Miri sheet with (a) body posture differentiation on all five current expressions — NOSTALGIC needs a defined body read (forward? backward?), CONCERNED needs a measurable forward lean (at least 8px head-forward at panel scale), WISE/KNOWING needs the cheek-widening to be more aggressive; (b) replace NOSTALGIC/WISTFUL with FOCUSED/WORKING per directive spec — this is the expression that defines who Miri was before she was Grandma; (c) add a sixth expression SKEPTICAL/AMUSED per directive spec to complete the pitch document's emotional range coverage.

**Priority 3: Cosmo SKEPTICAL lean formula**

The `tilt_off = int(body_tilt * 0.4)` formula is the root cause. For a visible backward lean at Cosmo's scale, increase the multiplier to at least 1.5 or set the pixel displacement directly. SKEPTICAL body_tilt should produce a visible displacement of 10–12px at the top of the torso to read at thumbnail scale. Additionally, pair the backward lean with pressed-tight arm posture (the notebook hugged closer to chest) to create a compound body-language signal that reads in two channels at once.

---

*"A character sheet that passes at panel scale but fails at thumbnail is not a character sheet — it is an illustration. Character sheets are working documents. They must function at the speed of production floor use. The squint test is not a style preference. It is the minimum viable readability standard for a professional animation document."*

— Dmitri Volkov, Character Design Lead
