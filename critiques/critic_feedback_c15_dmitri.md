# Dmitri Volkov — Critique Cycle 8
**Date:** 2026-03-29

---

## Byte Expression Sheet v002 [B]

### First Pass: The Squint Test

Eight panels. Black blob the sheet down to 10% scale. What reads?

NEUTRAL reads. GRUMPY reads — it has arm displacement. SEARCHING reads — wide aperture eyes change the blob perimeter minimally but the orientation shift of the face helps. ALARMED reads — limbs extend, blob widens. RELUCTANT JOY reads — because the limb position matches Configuration 2 closed arms, it creates a narrower vertical blob distinct from NEUTRAL. CONFUSED has drooped limbs which create a slight asymmetric hang — marginal pass.

Now the two I am here to interrogate.

**POWERED DOWN vs RESIGNED at thumbnail: they are the same blob.**

Both show Byte at approximately the same size. Both show arms in a retracted position. Both show a face that is low-energy. At 10% scale these two panels are indistinguishable without reading the label bar. That is a failure of the squint test — not a catastrophic one, because POWERED DOWN and RESIGNED are adjacent emotional states, but it is still a failure. If a director needs to point to a panel and say "this register, here, for scene A2-07" they cannot do it reliably at distance. They have to get close and read the labels. That is a production floor problem.

### RESIGNED: Does It Meet Spec?

The SOW for Cycle 15 specifies the RESIGNED visual as: ↓ pixel glyph left eye, droopy_resigned right eye (no smile crinkle), arms drawn in (x_scale=0.50), backward body lean (+8°), flat mouth.

What I see in the panel:

**Pixel glyph (cracked/left eye):** A downward arrow is visible. The color reads as a dim cyan — consistent with the ↓ symbol spec (Electric Cyan at 50% brightness = ~#007878). This is correct. The symbol is legible at panel scale. Pass.

**Right eye (normal eye):** This is where I have a real problem. The spec calls for "droopy_resigned — no smile crinkle." What is rendered reads as a standard half-aperture eye. There is no visible downward-droop to the lower eyelid line. The lower lid in NEUTRAL has a flat baseline. The lower lid in RESIGNED appears to have the same baseline. The distinction between NEUTRAL right eye and RESIGNED right eye at panel scale is effectively zero. A droopy resigned eye requires the lower lid to curve DOWNWARD at the lateral end — a frown-equivalent applied to the lower lid only, creating the asymmetric "heavy-lidded sadness" distinct from the flat-line neutral look. This is not present. The right eye does not read as RESIGNED. It reads as NEUTRAL with the pixel display swapped.

**Arms drawn in (x_scale=0.50):** The arms are pulled in. This is visible — they are tighter to the body than in NEUTRAL. This reads correctly and is the primary body language differentiator for this expression. Pass.

**Backward body lean (+8°):** A lean is present. Whether it is 8° is impossible to confirm at panel scale, but the lean is perceptible. It reads correctly as "world-weary slump" when combined with the drawn-in arms. Pass.

**Flat mouth:** The mouth reads as flat — no curve in either direction. This is the lowest-register mouth Byte can have without going to full closed expression. It differentiates from NEUTRAL's slightly-downturned corners. Pass.

### RESIGNED vs NEUTRAL vs POWERED DOWN: The Three-Way Differentiation Test

This is the critical test I need to run on any low-energy state.

**NEUTRAL:** Flat line pixel eye (white, 70% brightness), 60% aperture normal eye, arms loose at sides, no lean, slightly downturned mouth corners.

**RESIGNED:** Downward arrow pixel eye (dim cyan), same aperture normal eye, arms drawn in tight, backward lean, flat mouth.

**POWERED DOWN:** Both eyes appear blank/dim, no pixel display, minimal limb extension, maximum droop.

At full size, these three are distinguishable. At thumbnail size, NEUTRAL and RESIGNED have different pixel displays (white flat vs. dim ↓) but neither pixel display reads at 10% scale. The primary differentiators at small scale are: arm position and body lean for RESIGNED, near-zero limb energy for POWERED DOWN, and standard-neutral arms for NEUTRAL. RESIGNED's drawn-in arms do help at thumbnail. But RESIGNED and POWERED DOWN share the same "arms retracted" energy from a distance.

The differentiation gap is not critical, but it is real. RESIGNED needs one more distinguishing element that reads at small scale. Candidate: the backward lean should be MORE aggressive than +8° — the backward lean is the posture equivalent of "I've given up arguing." At +8° it reads as barely-perceptible. At +15° it would create a visible body contour change in the silhouette.

### Expression Sheet Structure

The sheet now has 8 panels in a 2x4 grid. The flow annotation (← was / → next) is present on all panels. This is excellent production practice — I have been asking for this since Cycle 5. The [NEW] label in the corner of the RESIGNED panel is correctly applied.

The tonal variation across backgrounds (dark for low-register, lighter for high-energy) remains inconsistent. ALARMED has a brown-tinted dark background. RESIGNED has a mid-dark background. NEUTRAL has a dark background. There is no systematic relationship between background value and emotional register. This is not a blocking problem but it is an opportunity cost — if background value were systematically correlated with energy level (darker = lower energy, lighter = higher energy), the sheet would communicate emotional register in two channels simultaneously. Right now, background value appears arbitrary.

### Grade: B

The eighth expression is present and mostly functional. The RESIGNED pixel display is correct. The body language (arms in, backward lean) is correct. The mouth is correct. The right eye fails to carry the "droopy resigned" read — it defaults to NEUTRAL aperture construction, which collapses the distinction between RESIGNED and NEUTRAL when the pixel display is not legible at distance. The squint-test failure between RESIGNED and POWERED DOWN is a secondary problem. Both are addressable in a single revision pass.

---

## Luma Act 2 Standing Pose [A-]

### Squint Test

A silhouette blob is provided in the reference panel on the right side of the image, which I appreciate — Maya Santos is testing her own work before I have to. Let me verify it independently.

The blob: strong vertical mass from the afro-cloud hair, shoulder-to-hip orange rectangle, indigo legs, white sneaker bases. Asymmetric arm position — right arm raised, left at waist. The raised right arm breaks the silhouette on the upper-right. The cloud-afro creates an identifiable top silhouette. This is Luma. This reads at thumbnail. Pass.

### Expression: WORRIED / DETERMINED

The SOW documents this as: brow diff left=38 right=30, corrugator kink (inner UP), jaw-open oval (not scream rect), body_tilt=-5 (forward lean), head_tilt=5° left (query lean), right arm raised/reaching, left arm at waist.

**Eyebrows:** The asymmetric brow read is visible. Left brow is higher and more kinked than right brow. At this pose scale (full body medium shot) the brow asymmetry is legible. The corrugator kink — inner brow end pulled upward — creates the "worried" component. The overall brow asymmetry creates the "determined but uncertain" dual-state. This is correctly executed.

**Eyes:** Both eyes are open, with the slightly worried expression visible in the brow framing. The amber iris reads correctly. The eye placement in the lower half of the circular face is consistent with the character bible.

**Mouth:** The jaw-open oval is the critical call-out here. The SOW correctly specifies "oval not rect" — a wide-open rectangular mouth would read as fear or shock, while an oval opening reads as "talking urgently" or "reacting to information," which is the correct register for the WORRIED/DETERMINED beat. The rendered mouth is oval. This is correct and it matters — this is the kind of single-shape decision that separates character-aware design from default expression generation.

**Body geometry:**

The proportions match the bible. Head dominates — circular, large. Hair cloud adds appropriate volume above the skull line. The orange hoodie torso reads as the rounded-rectangle stadium shape specified in the bible. Indigo pants, white sneakers — canonical.

The pixel grid on the hoodie chest panel is present and reads at this scale as a colorful digital texture. The multicolored pixel blocks are visible. This is the right level of detail for a medium-wide standing pose. The simplified pattern rules in the bible (4x3 block arrangement for medium shot) are approximately followed.

**One concern: the right arm.**

The raised right arm terminates in what appears to be a fisted or cupped hand shape. The bible specifies "mitten-hands" — tapered cylinders narrowing to mitten-like forms, no finger detail. The rendered hand at the end of the raised arm has more definition than mitten — it reads as slightly finger-differentiated. At this scale this is a marginal call, but it should be clean mitten geometry. Animators working from this pose reference will read the hand as the production standard. If the hand has emergent finger-like differentiation, that will propagate.

**Squint test — specific: does the WORRIED/DETERMINED read at silhouette?**

The asymmetric arm position (right raised, left at waist) creates immediate pose dynamism at silhouette level. The forward body lean (-5°) is not perceptible at full image scale, but the wide stance (leg_spread=1.1) is visible as a slightly-wider-than-neutral stance. This communicates groundedness and readiness — consistent with DETERMINED. The worried component lives in the face and would not survive very-small thumbnail. That is acceptable — worry is a facial expression, not a body expression. The body correctly reads as ACTIVE and GROUNDED.

**Hair curl count:**

The hair is rendered with what appears to be 5 visible spiral-curl indicators within the cloud mass. The locked production number is 5. A count of the large spiral indicators in the hair mass: I see approximately 5 dominant curl shapes within the afro volume. This is consistent with the locked production count. There are also small wispy flyaways at the top, which are specified in the bible. Correct.

**Blush:**

No blush is present on the cheeks. The expression is WORRIED/DETERMINED — not a joy or embarrassment state. The absence of blush is correct per the bible (blush applies only in joyful or embarrassed states, not neutral/negative states).

### What Keeps This from an A+

Two things, both minor:

1. **The right arm hand geometry.** Mitten, not finger-differentiated. Fix before this goes into animator reference.
2. **The forward lean (-5°) is not perceptible.** If the pose data says -5° body tilt, the visual should communicate it. At -5° it is marginal — the character reads as upright with a slightly aggressive stance rather than actually leaning forward. Either accept that -5° is too subtle to render (and drop it from the spec) or increase it to -8° where it reads clearly as "she is committed to whatever is about to happen."

### Grade: A-

This is the strongest single-character pose in the Act 2 package. The expression call is precise, the body language is legible at distance, the hair is canonically correct, and the designer provided a squint test reference blob in the asset itself. The hand geometry note and the invisible forward lean are polish items, not design failures.

---

## Cosmo Expression Sheet v001 [B+]

### Squint Test

Four populated panels plus two empty placeholders. The two empties ([NEXT BEAT] and [RESERVED]) are correctly labeled but are dead weight in any review context. A sheet with 40% of its grid unfilled is not a production-ready sheet — it is an in-progress document.

At thumbnail for the four populated panels:

NEUTRAL/OBSERVING: tall rectangle head, circular glasses dots, arms at sides, notebook under left arm. Reads as Cosmo. Pass — the notebook-under-arm protrusion on the left side is the silhouette hook that makes him identifiable at very small scale, exactly as the bible specifies.

FRUSTRATED/DEFEATED: same head geometry, arms extended further from body in a slightly deflated stance, mouth droop visible. The glasses tilt appears increased. Marginal differentiation from NEUTRAL at thumbnail — the body language is more expressive in full view than at 10% scale.

DETERMINED: body posture shifts to forward-leaning engaged stance, notebook held forward rather than tucked. This is a meaningful silhouette change — the notebook moving from tucked-under-arm to held-out creates a visible protrusion change on the left side. Pass.

SKEPTICAL: the one-eyebrow-raise is the primary differentiator. At thumbnail this does not survive — brow asymmetry at this character's face scale does not read at very small sizes. The body language is neutral-adjacent. SKEPTICAL and NEUTRAL would be indistinguishable at 10% scale. The expression lives entirely in the face, which is not thumbnail-readable.

### Expression-by-Expression Assessment

**NEUTRAL / OBSERVING:**
The glasses tilt of 7° counterclockwise is present and perceptible. This is the locked neutral tilt per the bible. The locked tilt is one of my recurring verification points, because teams consistently drift toward 0° for "ease" in neutral states. 7° is held here. The notebook is tucked under the left arm, visible as a small blue rectangle at the torso. The striped shirt (blue and sage green horizontal stripes) reads correctly. His straight-armed default stance and flat lower lid combine to give the "organized, observing, waiting" baseline read. This is correct.

**FRUSTRATED / DEFEATED:**
The mouth droop is present. The brows push inward. The arms have moved to a slightly deflated splayed position. The glasses tilt appears to have increased (I estimate 10-12°) — consistent with the bible spec that emotional states may increase tilt from the 7° neutral. This is correctly applied. The notebook remains tucked — which per the bible signifies uncertainty or anxiety (notebook pressed tight = holding on). That is the right choice for FRUSTRATED.

**DETERMINED:**
The forward posture shift is legible. The notebook appears to be held out or positioned more prominently — consistent with the bible's "notebook held out = engaged/confident." The brows are set. This reads as a distinct state from NEUTRAL. However, I want to flag: DETERMINED Cosmo and NEUTRAL Cosmo have very similar upper-body geometry. The differentiation is primarily in the face and notebook position. At thumbnail, the notebook repositioning is the only silhouette-level differentiator. It is sufficient, but barely.

**SKEPTICAL:**
One eyebrow is raised (left eyebrow, viewer's right — consistent with the bible's note that this brow is more mobile). This is his signature expression. The problem is this: the single raised brow, while correctly executed at full panel size, does not survive thumbnail. The brow raise is a facial micro-detail. Cosmo's design challenge — rectangular head, controlled features — means his most characterful expressions (skepticism, subtle amusement, deadpan) live in small feature movements that do not scale down. The bible acknowledges this challenge by specifying the notebook as the long-shot readable hook. But for expressions like SKEPTICAL, there is no body-language complement to the raised brow. The expression is face-only, and face-only does not pass the squint test at Cosmo's scale.

This is a design-level problem, not an execution problem. SKEPTICAL Cosmo needs a body language component that reads at distance. Candidate: a slight backward torso lean (equivalent to Byte's SMUG lean) that communicates "I am taking stock of this situation from a position of measured doubt." A 5-8° lean changes the silhouette enough to survive thumbnail. Currently there is no lean in the SKEPTICAL panel — the body is as upright as NEUTRAL.

### Sheet Completeness: The Empty Panels

Two of six panels are empty. [NEXT BEAT] and [RESERVED] placeholders.

I will say this directly: an expression sheet with 33% of its grid as placeholders is not ready for critique. I am critiquing four expressions, not a sheet. The sheet structure is correct — the 3×2 grid, the flow annotations (← was / → next), the beat labels in corner tags — all of this is sound and consistent with the Byte and Luma sheet conventions. But the two empty slots represent expressions that, presumably, Cosmo will need to perform in Act 2. If they are not populated, they are either not yet designed (a production gap) or waiting on upstream decisions (a dependency issue). Either way, they should not appear as empty gray boxes in a pitch package critique cycle. They should be populated or removed.

The flow annotation on SKEPTICAL reads: "→ next: RESIGNED / PREPARING ANYWAY." RESIGNED is named as a known next state. If RESIGNED is a named expression in the narrative flow, it should be on this sheet. It is not. Either RESIGNED is placeholder content #4 (occupying the [NEXT BEAT] slot) and has not been drawn yet, or it was not prioritized. If it is the former, it needs to be drawn. If it is the latter, the flow annotation should not reference it.

### Grade: B+

The four populated expressions are correctly constructed. The glasses tilt is held at 7° neutral and increases appropriately with emotional intensity. The notebook position is used as an emotional signal (tucked = anxious, forward = engaged). The flow annotations are correctly applied and consistent with the other sheets.

The B+ is not an A because: (1) SKEPTICAL has no body-language complement and fails the squint test; (2) two panels are empty, leaving the emotional range incomplete; (3) FRUSTRATED and NEUTRAL are too similar at thumbnail scale — the mouth droop and brow push are face-only differentiators that compress to invisible at distance.

---

## Priority Fixes (top 3)

1. **Byte RESIGNED right eye — requires droopy lower lid, not neutral aperture.** The lower eyelid on the right (normal) eye must curve downward at the lateral end to produce "droopy resigned" versus "neutral observing." Currently it is a flat-line lower lid identical to the NEUTRAL expression. This single-line change eliminates the most significant execution gap in v002. Without it, RESIGNED and NEUTRAL are the same expression with a different pixel display.

2. **Cosmo SKEPTICAL needs a body-language anchor.** The raised brow is face-only and does not pass the squint test. A 5-8° backward torso lean — the "I am evaluating this from a distance" lean — gives the expression a body-level read that survives thumbnail. This is a 30-minute fix that makes the expression readable by a director at distance. Additionally: the two empty expression panels must be populated before Cosmo's sheet can be considered production-ready.

3. **Luma Act 2 pose — mitten-hand discipline on the raised right arm.** The raised arm terminates in a hand that shows emergent finger differentiation. The production standard is mitten-hands: no fingers. Animators will use this as reference. If the reference has finger-adjacent geometry, it will proliferate. Clean this to a rounded mitten terminus before this file is distributed as Act 2 reference art.

---

*Dmitri Volkov — Character Design Lead*
*"If it doesn't read at thumbnail, it doesn't exist."*
