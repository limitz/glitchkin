# CRITIQUE — "Luma & the Glitchkin" Character Design
## Reviewer: Dmitri Volkov, Character Design Lead
## Date: 2026-03-29
## Round: Cycle 02

---

> *I have re-read luma.md v2.0, cosmo.md v2.0, byte.md v2.0, character_lineup.md v2.0, and grandma_miri.md v1.0. I have cross-referenced against my Cycle 1 critique. Where issues have been resolved, I will say so, briefly. Where they have not, I will say so at length. Where revisions have introduced new problems, I will say so loudly.*

---

## Cycle 1 Feedback Resolution

**Issue 1 — Byte's pixel-eye legibility at shoulder scale (PRIORITY ONE)**
**Result: PARTIALLY FIXED. New problem introduced.**

The limb expression vocabulary is now fully documented — eight named configurations with angles specified for both upper and lower limbs. This is exactly what was requested and the work is solid. I have nothing negative to say about the limb section. That problem is resolved.

The pixel-eye scale threshold question is NOT resolved. The document still asserts legibility at shoulder scale without specifying at what rendered pixel height the symbol system gets replaced or simplified. The claim that a 0.25x0.20-unit pixel symbol reads at "40-60px total character height" has not been tested, documented, or addressed. What was Priority One in Cycle 1 remains Priority One in Cycle 2. I am not going to move on from this.

**Issue 2 — Luma's pixel hoodie pattern simplified version**
**Result: FIXED.**

The three-tier simplification system (medium shot, wide shot, very wide shot) is present, specific, and production-usable. Hex colors, grid densities, and per-tier rules are documented. The logic is correct: protect the pattern at medium, abstract to a 10-mark scatter at wide, reduce to a 35%-opacity cyan tint at very wide. This is what I asked for. Credit given.

**Issue 3 — Cosmo's silhouette at long shot**
**Result: FIXED (notebook addition). Partially fixed (frames).**

The notebook as a canonical permanent accessory is a genuinely good solution. It creates a secondary silhouette element — the rectangular protrusion at mid-torso left — that survives long-shot reduction better than the glasses alone. The argument that the asymmetric notebook tuck distinguishes him even when his face is unreadable is correct and well-reasoned.

The glasses frame thickness has been increased from 0.025x to 0.06x head width — from thin wire to thick plastic. That is the right direction. At 0.06x, the frames are 5.2px thick at 100px head reference. This will survive reduction. The specification is now production-usable.

**Issue 4 — Byte's limb expression vocabulary**
**Result: FIXED. See above.**

**Issue 5 — Byte's production overhead acknowledgment**
**Result: NOT FIXED.**

The jitter-line treatment is still described ("a slight zigzag or dual-offset line") with no technical specification. Hand-drawn? Procedural shader? Compositing layer? I asked for a production decision, not a description. Still not there. Still needs to be answered before production begins.

The floating confetti overhead (8-12 particles per frame) has no simplification tiers for crowd/background shots. This was explicitly flagged in Cycle 1. Still absent.

**Issue 6 — Cosmo's corner radius quantification**
**Result: FIXED.**

The head rectangle now has locked proportions: 1.0 height x 0.86 width, 0.12 unit corner radius, hard upper limit of 0.18 before it reads as oval. The production test specified ("at any distance where you cannot see his glasses, his head should still read as rectangular rather than oval") is correct and implementable. This is what quantitative specification looks like. Good.

**Issue 7 — Neutral glasses tilt increase**
**Result: FIXED.**

Neutral tilt locked at 7 degrees. Comedy escalation range now 7 to 15 degrees. The Cycle 1 recommendation was 6 degrees minimum neutral, so 7 is acceptable. The "never draw at 0 degrees" production rule is correct. Fixed.

**Issue 8 — Luma's hair curl count**
**Result: FIXED.**

Locked at 5. Stated twice in the document in no uncertain terms. "Not 4, not 6, always 5." The emotional state variants change shape and size, never count. This is the right call. Fixed.

**Issue 9 — Overlap between Luma's Guilty Sheepishness grin and Cosmo's forced grin**
**Result: NOT ADDRESSED.**

I called this out in Cycle 1. It is not in the revision notes, not in the expression sheets, and not referenced anywhere in either document. This is a continuity problem in ensemble storytelling. Two characters' expressions overlapping at the same emotional beat (guilt/embarrassment) undermines the visual language of the show. Still unresolved.

**Issue 10 — Glitch Chaos palette behavior for Cosmo's colors**
**Result: NOT ADDRESSED.**

The lineup document's color section does not address how Cosmo's sage green and cerulean blue behave under extreme glitch-palette (acid green / hot magenta) environment domination. Still absent.

**Issue 11 — Group silhouette test page**
**Result: PARTIALLY ADDRESSED.**

The lineup document has expanded silhouette contrast language and added Miri to the analysis. The squint test is now more thoroughly documented in text. However, an actual documented test with output (rendered silhouettes at three scales) still does not exist. The document describes the expected results of such a test rather than documenting the results of a test that was actually performed. I cannot verify claims that are assertions rather than evidence.

---

## Luma — Cycle 2 Assessment

The Cycle 2 revision of Luma is, overall, the strongest individual character document in the set. The critical production problems (pixel pattern tiers, hair curl count) have been resolved. The silhouette test section is now explicit and detailed — it walks through what reads at thumbnail in order, tests the challenge cases, and arrives at a verdict. The methodology described ("render as solid black shape, observe") is correct.

**What is genuinely good:** The pixel hoodie simplification tiers. The rationale behind each tier is correct — protect legibility at each scale rather than either over-rendering or dropping the element. The "35% opacity cyan tint over base orange" at very wide shot is elegant: it preserves color identity without lying about pattern detail that isn't there. The production rule "do NOT substitute a solid different color for the hoodie at this scale" is exactly the kind of negative-space specification that prevents animator errors.

**What still needs attention:**

The front-view silhouette torso-merge risk I raised in Cycle 1 has been addressed in the silhouette test section, where the document acknowledges that "at thumbnail size the head and hair partially merge into a single large top-heavy form" and calls this "acceptable." I disagree with "acceptable." It is tolerable, and it is mitigated by the strong hair-cloud read, but calling a head-body merge acceptable sets a permissive standard for what animators will do. The fix is trivial — specify a minimum visible gap between the bottom of the hair mass and the top of the hoodie collar in the front view. Even 3-4% of total character height as a visible neck gap, or a strong color boundary between dark hair and orange hoodie, prevents the merge from becoming a blob. This is not in the document.

The expression overlap with Cosmo (Guilty Sheepishness grin vs. Cosmo's mortified grin) is still unresolved, as noted above.

**One new problem I'm flagging:** The blush specification for the Guilty Sheepishness expression reads "heavy blush — larger than usual, extending lower on the cheek." But the Reckless Excitement expression also has "full blush ovals visible, pressed upward by the wide smile." Two expressions have maximum or near-maximum blush. Since blush is used as an emotional signal, having two emotionally different expressions reading at maximum blush creates a readout ambiguity. Production needs a blush intensity scale — excitement blush vs. embarrassment blush must be distinguishable. Different shape, different placement, different size — not just intensity. Currently undifferentiated.

**Verdict on Luma:** Passing. The core design is strong and the critical production specs are now in place. The remaining issues (torso-head gap, blush differentiation, expression overlap with Cosmo) are real but not blocking. Do not call this done — call this ready for the next round of refinement.

---

## Cosmo — Cycle 2 Assessment

The Cycle 2 revision of Cosmo addresses the structural issues I raised and the character is now substantially more production-ready. The notebook addition is the revision's single best idea and I want to state this clearly: the notebook solves the long-shot identification problem, adds to the character's visual personality, and creates a secondary tell system that pairs with the glasses tell. It is doing three jobs at once. That is good design economy.

**What is genuinely good:** The head rectangle is now properly quantified. The glasses frames are now production-thick. The neutral tilt is now comics-legible. The notebook-as-permanent-accessory is correct. The emotional signal system for the notebook (pressed tight = anxious, open and held out = engaged, absent = significant beat) is clever and parallels Byte's pixel-eye system and Luma's hair reactivity at an object level. Good.

**What still needs attention:**

The Deadpan expression (Expression 1) specifies the glasses at "perhaps 4 degrees" in that expression — but the neutral tilt has been locked at 7 degrees in Section 4. If his default state is 7 degrees and the Deadpan uses 4 degrees, you have accidentally made the deadpan read as MORE level than neutral, which is both incorrect and confusing. The deadpan should be AT the 7-degree neutral or beyond it, not less. This is a document inconsistency that will produce animator errors.

The range between Deadpan and Anxious Overthinking is still small. I raised this in Cycle 1 and the document does not address it. Both expressions involve a controlled Cosmo with small tells. The specification does not provide explicit readability guidance for how these differ at reduced scale. The key differentiators (half-lidded vs. wide-open eyes, level brows vs. raised-inner worry brows, sweat bead presence) are described but not prioritized. Which element is the most reliable differentiator when the face is 30px tall? That question needs to be answered.

The stripe production concern — two shadow tones, two highlight tones per lighting pass — is still not addressed with any simplification note for wide shots. I raised it in Cycle 1. Still absent.

The expression overlap with Luma (guilty/sheepish forced grin) is still unresolved.

**New problem:** The notebook has been added as a canonical permanent accessory in Section 4 (strong, specific) and then contradicted in Section 7 ("no bag in standard pose — he carries a slim notebook (visible in some scenes) but it is a prop, not a permanent accessory"). These two statements are in direct conflict. Section 4 says the notebook is a permanent silhouette element, always present, always tucked under his arm, never absent except as a significant character beat. Section 7 says it appears in some scenes and is a prop. One of these sections was not updated when the other was written. This inconsistency will cause production confusion. Fix it: the notebook is a permanent accessory per Section 4. Delete or revise the conflicting statement in Section 7.

**Verdict on Cosmo:** Passing — conditionally. The critical structural fixes have been made. The new notebook addition is good design. But there are two document inconsistencies (glasses tilt in Deadpan, notebook permanence contradictions) that must be resolved before this goes to animators. Find them, fix them, resubmit the final version.

---

## Byte — Cycle 2 Assessment

The limb expression vocabulary is now the best section in Byte's document. Eight configurations, angles quantified, visual reads described, cross-referenced with expression sheet pairings. Configuration 7 (Desperate Reach, 25-degree forward tilt, upper limbs reaching downward and forward, lower limbs kicking back for momentum) is especially well-conceived — this is a body-language configuration that makes Byte look committed and urgent despite a non-deforming cube body. The work on this section is what I asked for.

Everything else I asked for that touches on production overhead? Still not there.

**What still needs attention:**

The pixel-eye scale threshold. I am going to be direct: this was Priority One in Cycle 1 and it remains unresolved in Cycle 2. The document still asserts that the pixel symbols are "small, but legible" without specifying at what rendered output size they cease to be legible, what the fallback is when they are not, and how the normal eye compensates. This is not a documentation preference. This is a design failure mode that will manifest in the first storyboard pass. A heart symbol at 0.25x0.20 units within a face of 28-42px render height is working at effectively 7-10px effective display area. That is not legible for a heart shape. That is a smear. The team must either (a) accept that the cracked eye reads as "dark rectangle with color" at shoulder scale and design the normal eye to carry full expression in those shots, or (b) scale the pixel-eye symbols up significantly within the cracked eye frame, accepting that they become less "pixel-art" and more "large graphic symbol." Neither choice has been made. Neither choice has been documented. After two cycles, this is inexcusable.

The jitter-line treatment is still not technically specified. "A slight zigzag or dual-offset line" is a description, not a production decision. Three animators will interpret this three different ways and Byte will look like a different character in every fourth scene.

The floating confetti overhead (8-12 particles minimum at all times) still has no simplification plan for crowd shots, background appearances, or standard action coverage where Byte is not the focus. On a show with recurring cast appearances and a limited budget, this will create a cost spike that either blows the per-episode budget or results in Byte being silently removed from wide shots. Neither outcome is acceptable. Both are preventable.

**New problem introduced in Cycle 2 — body asymmetry documentation gap:**
The document describes the cube's left/right asymmetry in detail (cleaner left, notched right, triangular bite-marks from the upper-right corner). It then specifies 8 limb configurations by viewer perspective. But there is no turnaround sheet. The asymmetric damage (notched right, spike top, scar diagonal upper-right to lower-left) will create continuity errors the moment Byte appears in anything other than a near-front view. Which way does the notched side face when Byte turns 90 degrees toward camera? Which way does the spike lean in 3/4 view? The document does not specify this. I raised the turnaround gap in Cycle 1. It was not addressed. A character with designed structural asymmetry REQUIRES turnaround documentation. This is non-negotiable.

**Verdict on Byte:** Limb expression system: passing. Everything else involving production specification: still failing. The concept remains the most original in the project. The execution documentation is still insufficient for production handoff. The pixel-eye scale threshold must be resolved. The jitter-line must receive a technical decision. The confetti must have a simplification tier. The turnaround documentation must be produced. Until those four issues are addressed, Byte cannot be signed off for production.

---

## Grandma Miri — First Assessment

Grandma Miri is a first-pass document and I will assess it as such, but "first pass" does not mean "given easy treatment." If it goes to production as written, these are the problems.

**What is genuinely good:**

The design rationale is the strongest single rationale in the entire set of documents. "Circles (warmth, safety, welcome) + weathered rectangles (history, precision, groundedness) = someone who was once more angular and has softened into the form of their best self." This is character-design thinking at the right level. The shape language is doing biographical work — the compressed circle says "I was a rectangle once, life softened me." The family DNA connection to Luma through shared head shape, iris color family, eye highlight position, and garment color family is well-executed and well-documented. Cross-character visual rhyming is harder to design well than single-character consistency, and the team did it well here.

The "tell" system extension to Miri (the mug) is coherent with the existing tell architecture. Mug in hand = active/present. Mug set down = fully focused. Mug absent = serious scene. This is the right kind of object-based emotional signaling. The mug absent as "she is not in her element" is good instinct — but I would add: the mug absent should also be the visual cue for scenes where she must mobilize her engineering mind. The tea is warmth; when the problem requires precision, she sets it down.

The expression sheet is the best among supporting characters — the "Engineer Look" (Expression 2, sharp assessment) is the most precisely described expression in any document. "A suspension of the default warmth while she processes" is exactly right. And the production note on the concern expression — "in scenes of genuine concern, reduce the cheek blush to 10% opacity or remove it" — is exactly the kind of specific, implementable production note that the other expression sheets often lack.

**What needs attention:**

The shoulder width specification says Miri's shoulder width is 1.1x head width — "slightly wider than her head." The document calls this "unusual for the cast." It is — but no one else has specified a shoulder width wider than the head. This needs a squint-test pass. At thumbnail size, wider-shoulders-than-head combined with short legs and a wide cardigan may produce a silhouette that reads as a shape, not a person. The document's own thumbnail analysis (Section 10) identifies "the wide torso mass" as a key readable element, and calls this "broader shoulder-to-torso ratio than any other character." Verify this actually reads as "settled adult woman" and not "wide box with a head." The A-shape cardigan silhouette described in Section 10 is doing significant work to prevent this reading — but the document needs to explicitly confirm that the shoulder width plus cardigan drape does not make her read as a shape wider than she is tall in thumbnail.

The cheek blush specification has a problem. Miri has permanent blush (always present at 25% opacity). Luma has situational blush (appears in joy and embarrassment, not neutral). The issue: in scenes where both characters are in frame and Luma is in a joy expression (full blush), both characters will have visible blush simultaneously. How does the audience read which character's blush is communicating what? If the answer is "Miri's is always there so the audience learns to read Luma's blush as the signal," then the document needs to say that explicitly as a production note. Currently it does not. The blush signal system is not fully thought through as a multi-character ensemble tool.

The den section (Section 8) is set dressing written as character design. It describes the objects in her den — computer, bookshelves, mug, circuit boards, plants. These are narrative props. They belong in a background design brief, not in a character design document. A character design document should describe how the CHARACTER appears in the den (how she relates to her environment visually, what her posture does in that context, how her silhouette reads against the warm background). The set dressing content is useful but it's in the wrong document. Or it needs a paragraph of "here is how Miri's silhouette reads against this specific environment" to justify its presence here.

The line weight specification — Warm Dark Brown (#4A2810) for Miri, vs. Deep Cocoa (#3B2820) for the trio — is correctly motivated ("she is softer at her edges") but the character_lineup.md design system table lists the line color correctly. However, in practice, when Miri and Luma appear in the same frame, the line weight difference creates two visible "rendering levels" in the frame. This is intentional — but the document should acknowledge it and confirm it as an intentional design decision rather than a default, so animators don't correct it thinking there's an error.

**Verdict on Miri:** Strong first pass. The design concept is correct and the family DNA connection to Luma is well-executed. The expression sheet is good. Before this goes to production: resolve the shoulder-width thumbnail risk, document the dual-blush problem, relocate the den set-dressing section appropriately, and add a production note clarifying that the different line weight is intentional.

---

## Ensemble — Updated Assessment

The addition of Miri improves the ensemble considerably. She provides exactly what a fourth character should provide: a new shape type (compressed circle, weathered rectangle) that doesn't overlap with any of the trio's shape families, a new position in the color temperature range (warm-settled, the mature end of Luma's palette family), and a new behavioral mode in shared compositions (still center around which kinetic characters orbit).

The design system table in character_lineup.md Section 6 is now four rows and reads cleanly. The "tell" column for Miri (the mug) completes the ensemble tell architecture.

The warm color bookend structure — Miri's terracotta rust on the left, Luma's orange in center-right — is a genuine compositional improvement. When those two characters share frame, the composition has a warm internal logic that communicates family relationship before any facial expression or dialogue is processed. This is design doing its job.

**What the ensemble still needs:**

A group silhouette test with actual documented output. Described results of imagined tests are not tested results. The four-character full-cast lineup, the waist-up four-shot, the long shot at 15% frame height — these need to be rendered and documented, not described. I am not capable of reviewing assertions. I can only review evidence.

The problem of Miri's circular head potentially reading as Luma-adjacent at thumbnail is acknowledged in the document and dismissed because the hair forms differ. This is correct as stated — silver updo vs. dark cloud reads differently. But it has not been tested across the full range of shot types where both characters appear at small scale. The dismissal is too quick for a documented risk.

The color temperature section in the lineup describes the full-cast temperature distribution correctly. But there is still no specification for how this system degrades in glitch-environment scenes where the palette shifts to acid green / hot magenta dominance. Cosmo's sage green and cerulean blue under heavy glitch palette contamination still have no documented behavior. Two cycles. Still not there. This needs to be addressed.

---

## New Issues Found

**1. Cosmo — Deadpan glasses tilt inconsistency.**
Section 4 locks neutral tilt at 7 degrees. Expression 1 (Deadpan) specifies "perhaps 4 degrees." These contradict each other. If the Deadpan is his most resigned, flat, affectless state, it should not read MORE level than his neutral. Fix the expression sheet to 7 degrees minimum, with escalation for extreme states.

**2. Cosmo — Notebook canonical status contradicted in Section 7.**
Section 4 and the long-shot note specify the notebook as a permanent silhouette element. Section 7 calls it "a prop, not a permanent accessory." These cannot both be true. Reconcile them. Given the design rationale for the notebook's silhouette function, Section 4's version is correct. Section 7 needs revision.

**3. Luma — Blush differentiation between Excitement and Guilt expressions.**
Both Reckless Excitement (full blush, pressed up by smile) and Guilty Sheepishness (heavy blush, extended lower on cheek) read at or near maximum blush intensity. Two different emotional states should not produce visually similar blush states on the same character. Differentiate by placement and shape: Excitement blush sits high on the cheek, pressed up; Guilt blush should be lower, more diffuse, and possibly asymmetric to match the tilted head.

**4. Miri — Dual-blush problem in shared compositions with Luma.**
When Luma is in a joy or excitement expression and Miri is in her default permanent-blush state, both characters will have visible blush. The blush signal is an emotional readout system on both characters; simultaneous activation creates readout noise. The ensemble document and/or Miri's document need a production note explaining how animators should handle this — likely by confirming that Miri's permanent blush is background warmth, not emotional signal, and that Luma's situational blush is the signal to attend to.

**5. Byte — Turnaround documentation still absent.**
Structural asymmetry is a design choice that requires full turnaround documentation. This is not a paperwork formality — it is a functional requirement. A character with a specific notched right side, a diagonal scar from upper-right to lower-left, and a spike positioned "one-third from the right edge" will be drawn inconsistently by every animator who does not have turnaround reference. After two cycles of this being flagged, this is the production equivalent of leaving a load-bearing wall out of architectural drawings and hoping the contractors will figure it out.

---

## Remaining Critical Problems

**In order of severity:**

**CRITICAL — Byte pixel-eye scale threshold: Cycle 1, Cycle 2, still not resolved.**
A character's primary emotional expression system must be verified legible at production scale. Not asserted legible. Verified. This requires either a documented scale test with specific results, or an explicit design decision that the cracked eye is supplementary at shoulder scale and the normal eye carries expression in those shots. Make the decision. Document it. Ship it.

**CRITICAL — Byte jitter-line technical specification: Cycle 1, Cycle 2, still not resolved.**
An undecided technical approach is not a design decision — it is deferred production chaos. Three sentences of description do not constitute a specification. Decide: hand-drawn, procedural, or compositing layer. Write it down.

**HIGH — Byte confetti simplification tiers: Cycle 1, Cycle 2, still not resolved.**
Byte is the most expensive character per frame in this production. Without documented simplification standards for background appearances, either the budget absorbs an unbudgeted cost or Byte gets silently removed from scenes. Design the lower tiers now.

**HIGH — Cosmo/Luma expression overlap: Cycle 1, Cycle 2, still not resolved.**
Two characters, same expression shape, different emotional beats. This is a visual language failure that will confuse audiences at the exact moments of emotional precision a comedy-adventure depends on. The Guilty Sheepishness grin and the mortified forced-grin need to be distinguishable in still frame. Currently they are not specified to be.

**MEDIUM — Glitch palette behavior for Cosmo's colors: Cycle 1, Cycle 2, still not resolved.**
Not yet a production emergency but will become one during episode layout when a glitch-environment scene goes to color pass.

---

## Recommendations

**Luma (priority order):**
1. Specify minimum visible separation between hair mass and hoodie collar in front view. Even 3% of character height as a clear dark-hair-to-orange-hoodie color boundary prevents the head-body merge at thumbnail. This is one sentence. Write it.
2. Differentiate Reckless Excitement blush from Guilty Sheepishness blush by placement, not just intensity. High-and-pressed vs. low-and-diffuse.
3. Resolve expression overlap with Cosmo — assign visual differentiators to the two guilty-grin expressions so they cannot be confused at broadcast scale.

**Cosmo (priority order):**
1. Fix the Deadpan expression glasses tilt to 7 degrees (match the locked neutral) or specify a reason the Deadpan is an exception.
2. Resolve the notebook canonical status contradiction between Section 4 and Section 7.
3. Add a key-differentiator note to the Deadpan vs. Anxious Overthinking expressions specifying which element reads most reliably at 30px face height.
4. Add a stripe simplification note for wide shots — a single combined shadow tone for the stripe pass is acceptable at distances where individual stripe colors don't read.
5. Resolve expression overlap with Luma (shared with Luma recommendation above).

**Byte (priority order):**
1. Make a decision about pixel-eye legibility at shoulder scale and document it. This is not optional. It is the character's primary expression mechanism.
2. Specify the jitter-line treatment technically. Hand-drawn? Procedural? Compositing? One sentence. Write it.
3. Add confetti simplification tiers: full (character featured), simplified (background/crowd), none (Byte is silhouette-only in extreme long shot).
4. Produce turnaround documentation — front, 3/4, profile, back — with asymmetric damage explicitly marked in each view.

**Grandma Miri (priority order):**
1. Perform and document the shoulder-width thumbnail test. Confirm she reads as "settled adult woman" and not "wide box" at thumbnail scale. The cardigan A-shape is doing significant work — verify it is sufficient.
2. Add a production note on the dual-blush issue. Confirm that Miri's blush is background warmth and Luma's is emotional signal. This prevents audience confusion and animator misreads.
3. Relocate the den set-dressing content (Section 8) to a background design document, or reframe that section to focus on how Miri visually relates to her environment (her silhouette against den backgrounds, her posture in that context).
4. Add a line weight production note confirming that the Warm Dark Brown / Deep Cocoa line weight differential is an intentional design system and should not be "corrected" by animators.

**Ensemble (priority order):**
1. Perform and document an actual group silhouette test — full cast at three scales, rendered as solid shapes, with results noted. Assertions are not evidence.
2. Document glitch-palette color behavior for all four characters, specifically Cosmo's behavior under acid green / hot magenta environment domination.

---

## Verdict

**Luma, Cycle 2:** Passing. The critical production specifications that were missing in Cycle 1 are now in place. The remaining issues are real but second-tier. This design can proceed to production with the noted refinements. It will require a third-pass cleanup, not a redesign.

**Cosmo, Cycle 2:** Passing — with two document errors that must be corrected before production handoff. The Deadpan glasses tilt contradiction and the notebook canonical status contradiction are not judgment calls; they are factual inconsistencies in the document. Fix them. The design itself is substantially improved from Cycle 1.

**Byte, Cycle 2:** Concept still passing. Production specification still failing on the same issues as Cycle 1 plus the new turnaround gap. The limb expression vocabulary, which was the Cycle 1 priority secondary to the pixel-eye, is now excellent. Everything else: still inadequate. I will keep saying this until it is fixed or until someone explains to me why the most complex character in the production doesn't need production specifications.

**Grandma Miri, Cycle 2 (first review):** Strong first pass. The design concept is correct and the execution is largely sound. The family DNA connection to Luma is well-designed. The expression sheet is the most precisely written in the set. Needs three specific fixes before production. Does not need a redesign.

**Ensemble, Cycle 2:** Better than Cycle 1. The addition of Miri completes the shape, color, and behavioral system in ways that improve all four characters' readability in shared compositions. The warm-bookend structure works. The tell system works. The color temperature architecture works. The remaining problems are documentation gaps, not design failures. Close those gaps.

**Overall:** This is a real show now. Cycle 1 was intent documented. Cycle 2 is design documented. Not fully — Byte's production spec is still an embarrassment of deferral — but the core system is now legible as a production design. The team is capable. The decisions being avoided on Byte are not technical mysteries; they are decisions that require a commitment that hasn't been made. Make them. The rest of this work is ready to move forward. The Byte pixel-eye threshold, the jitter-line spec, the confetti tiers, and the turnaround are not. They will not become easier to specify with time. They will become more expensive to fix.

Do the work.

---

*Dmitri Volkov — Character Design Lead*
*"If the character doesn't read at thumbnail size, it fails. If the character's expression system doesn't work at production scale, the character fails. Two cycles in. We know what the problems are. Now we either fix them or explain why we won't."*
