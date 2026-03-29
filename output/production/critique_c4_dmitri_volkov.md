# CHARACTER DESIGN CRITIQUE — Cycle 4
**Critic:** Dmitri Volkov, Character Design Lead
**Date:** 2026-03-29
**Subject:** First Actual Character Visual Output — "Luma & the Glitchkin"
**Materials Reviewed:**
- character_silhouettes.png
- proportion_diagram.png
- luma_swatches.png, cosmo_swatches.png, byte_swatches.png, grandma_miri_swatches.png
- character_lineup.md (first 40 lines)

---

## Overall Assessment

These are first images. I am judging them as such — which means I am measuring them against one standard and one standard only: do they communicate the right things in the right ways. Not "for a first pass." Not "considering the timeline." Do they work.

The short answer is: partially. The foundations are sound in places and actively problematic in others. The color work is the strongest element here. The silhouette work has a critical flaw that must be addressed before any further rendering or cleanup passes happen. Proportions are acceptable but not yet refined enough to lock.

This production cannot proceed to expression sheets or turnarounds until the silhouette problem is solved. I will explain exactly what I mean.

---

## Silhouette Test Results

The squint test is not a suggestion. It is the first and final arbiter of character readability. You blur your eyes and you ask: can I tell who is who from shape alone, stripped of all detail, color, and context?

**BYTE — PASS (strong)**
Byte passes cleanly and without hesitation. The compact, near-cubic body mass with the asymmetric shoulder protrusions is immediately distinctive. At thumbnail scale, across the room, at arm's length with your eyes half-closed — Byte reads. That low center of gravity, that boxy geometry, that absence of vertical ambition — it is doing its job. Byte is the only character on this sheet who unambiguously passes without conditions.

**COSMO — CONDITIONAL PASS**
Cosmo's silhouette has one saving feature: height. The dominant vertical rectangle of the torso, combined with the rectangular head sitting flush atop with almost no neck articulation, creates a lanky, slightly stiff read that does suggest "cautious, organized boy." The single arm-extension visible on the right side (notebook-holding arm or gear?) is a good silhouette anchor — that asymmetry helps. However: the overall shape is dangerously close to a generic tall-rectangle-with-small-head. The silhouette does not yet tell me "this is specifically Cosmo." It tells me "this is a tall thin character." Those are not the same thing. The head-to-body ratio as silhouette reads differently than in the proportion diagram — the silhouette head feels smaller relative to the torso than the 4.0-head-height spec implies. Verify this is a rendering artifact and not a proportion drift.

**LUMA — FAIL**
I am sorry to say this plainly, but Luma's silhouette does not pass the squint test. The shape — rounded head sitting on a rectangular torso with a narrow waist suggested by the slight indent between head and body mass — reads too similarly to Grandma Miri. When I blur my vision, Luma and Miri produce nearly identical silhouette shapes: ball-on-box, stocky, broad, grounded. The primary differentiator is height, and height alone is not a silhouette characteristic. Height is a size comparison. It only works when you can see both characters simultaneously. In isolation, I cannot tell Luma from Miri by silhouette.

This is a serious problem. Luma is the protagonist. She must be immediately, unambiguously readable as herself. Currently she is not.

Additionally: Luma's silhouette lacks any distinctive secondary shape element. Where is the design hook? What is the one thing on Luma's silhouette that is uniquely hers? The answer right now is: nothing. The hoodie does not read in silhouette — it merges into the body mass. The hair, if present, is not distinguishable from the head shape. The pixel-art accent elements on her costume obviously cannot survive silhouette, which is fine — but something beneath them must carry the read. It doesn't.

**GRANDMA MIRI — FAIL (different problem)**
Miri's silhouette has the opposite issue from Luma: it reads as a body type rather than a character. Large round head, broad rectangular torso, stocky build. This is a grandmother body type. It is not Miri specifically. The round head is large and well-shaped, and there is something warm and grounded about the overall mass — but "warm and grounded grandma" is a category, not a character. Where are Miri's distinctive shape elements? Does she carry anything? Does her hair create a distinctive silhouette? Does her cardigan create any distinctive layering that reads in black? None of this is present. The silhouette is a placeholder for a character, not the character herself.

**The Luma/Miri Overlap Problem — Urgent**
Placed side by side, Luma and Miri produce almost identical shape language: round head, rectangular body, no distinctive protrusions or negative spaces, grounded and stable posture. The show needs both characters to be instantly readable in fast-cut action sequences, in group shots, in marketing thumbnails. Right now, without color, they are effectively the same character. This must be fixed at the design level — not at the color or detail level.

---

## Proportion Diagram Assessment

The proportion diagram is cleaner and more useful than the silhouette sheet, which tells me the proportions were specified carefully but the silhouette rendering did not capture the full design intent.

**Cosmo at 4.0 heads** — This reads correctly. He is visibly the tallest character and the most rectangular. The proportion diagram does a good job of communicating his lanky, slightly ungainly build. The square-ish head on the long body is working in his favor here in a way it does not fully translate to silhouette.

**Luma at 3.5 heads** — The proportions are appealing in isolation. The head-to-body ratio gives her a slightly childlike, energetic read, which is appropriate. The problem is not here — the problem is that nothing in the body proportions is distinctive enough to carry into silhouette. The proportion diagram shows a well-constructed but generic cartoon girl. The design work has to push further to give her a hook.

**Byte at 0.7 heads / 20% of Luma's height** — This is correct and delightful. Byte is tiny. The proportion diagram communicates the size relationship clearly and the near-square body shape is doing good work. This is the one character whose proportion diagram and silhouette are in complete agreement.

**Grandma Miri at 3.2 heads** — The shorter head count compared to Luma is counterintuitive given their described near-equal real heights, and it creates a compressed, top-heavy read in the diagram. That could be intentional — a grandmother who has settled, compacted, become dense with presence. I accept it conceptually. But the execution in the diagram makes her feel slightly unresolved. The large head sitting on the squat torso needs to be pushed further to become a distinctive proportional signature, or it just reads as imprecise.

**Size Relationships Work** — Byte against Luma against Cosmo against Miri produces a clear and readable scale hierarchy. This is the strongest thing about the proportion diagram. The four-way size differentiation is doing a lot of heavy lifting and it is working.

**What is Missing from the Proportion Diagram** — There are no internal proportion guides. Where does the waist fall? Where do the elbows sit? What is the shoulder width in head-widths? These tick marks are visible but unlabeled in the diagram. A production proportion chart needs labeled construction lines — this currently functions as a size comparison chart, not a construction guide. Those are different documents. Both are needed.

---

## Color Swatch Assessment

The color work is the strongest element of this first output. Each character's palette is internally coherent and makes good use of value structure (base, shadow, highlight). I have specific observations per character.

**Luma**
The skin tones are warm and consistent — #C8885A base with appropriate shadow and highlight spread. The hoodie orange (#E8722A) is energetic and appropriate for her personality: it pops, it reads warm, it communicates action. The pixel accent colors (cyan #00F0FF, magenta #FF2D6B, acid green #00FF41, gold #F5C842) are vivid and read as accent glows rather than costume colors, which is correct. The dark hair (#1A0F0A) against the warm skin is a strong contrast choice.

One concern: the pixel accent colors, particularly acid green #00FF41 and pixel cyan #00F0FF, are at maximum saturation — they are essentially pure digital primaries. They will need careful management in animation to avoid vibration artifacts against the mid-saturation skin and hoodie tones. This is a production note, not a design failure.

The bigger issue: the core Luma palette (skin, hoodie, hair) without the pixel accents is not sufficiently distinctive. Remove the glitch effects and you have a warm-toned girl in an orange hoodie. That is fine for the character, but it means that the pixel accents are doing too much of the heavy lifting in terms of visual identity. What happens in non-glitch scenes? Does Luma still read as Luma?

**Cosmo**
The palette is the most restrained and considered of the four. The blue-stripe/sage-stripe shirt creates a satisfying complexity without becoming noisy. The glasses frame (#8C8070) and notebook cover (#5A4830) read as organized, slightly precious, well-maintained — character in color. Good work. The skin tones (#E8D4B0 base) are lighter than Luma's, correctly differentiating the characters at the color level and suggesting two different backgrounds without stating it explicitly.

The main risk: Cosmo's palette is pleasant but not striking. In an ensemble, he may read as the "background character" in crowd shots because his colors do not demand attention. This may be intentional — Cosmo is not the loudest personality — but it must be a deliberate choice that is addressed in the color direction notes, not an oversight.

**Byte**
This palette is excellent. The cyan body (#00F0FF) is bold, unambiguous, and character-defining. The magenta scar/marking (#FF2D6B, #CC1848) creates an immediate visual tension — something happened to this creature, something that left marks. The near-void black (#0A0A14) for the line work reinforces the "not-quite-right" quality. The "Particle Confetti" colors (#00C8D8, #FF6090) extend the palette into the FX range cleanly.

One flag: Byte's body cyan is identical to Luma's Pixel Cyan (#00F0FF). When Luma produces glitch effects and Byte is in the same frame, these colors will visually connect the two in a way that may be compositionally useful or may create confusion. This needs to be a conscious decision in the color bible, not an accident. If it is intentional (Byte was born of the same glitch energy as Luma's powers), document it. If it is not, differentiate Byte's body cyan.

**Grandma Miri**
The terracotta cardigan (#B85C38 with shadow #884028) against the warm cream shirt (#E8D4B0) is the most human and textured palette of the four. The silver hair (#C8C0B0 with cool grey shadow #908880 and near-white highlight #E8E4D8) is handled with more subtlety than I expected. The blush notes — particularly the "Pride Override" blush (#B85040, labeled with what appears to be a clipped label) — suggest personality and emotional expressiveness that is embedded directly in the color model. That is excellent character work.

The concern: Miri's palette is warm, earthy, and human. It is also close in overall value and temperature to Luma's palette. In a two-character scene (Miri and Luma together, which will presumably happen frequently), the palettes will need strong differentiation from the staging and lighting direction, because the color models alone do not provide enough contrast.

**Ensemble Palette as a Whole**
The four palettes, held together:
- Luma: warm orange-brown with neon accent
- Cosmo: cool blue-green-neutral
- Byte: saturated cyan with magenta
- Miri: warm terracotta-cream-silver

The warm/cool split between Luma+Miri versus Cosmo+Byte is notable. This could be read as a thematic grouping (the humans lean warm, the tech leans cool) which is a perfectly good underlying logic. However, Byte's cyan directly echoes Luma's glitch colors, which cuts across that grouping. The ensemble does not yet have a clear ensemble palette logic documented and visible. What is the common color thread that makes this look like one show? Right now the four palettes feel designed correctly in isolation but not explicitly designed to work together.

---

## Critical Issues

**1. Luma/Miri Silhouette Overlap — BLOCKING**
These two characters share the same primary shape language: round head, rectangular body, stocky. In silhouette, they are not differentiable in isolation. This must be resolved before turnarounds or expression sheets are produced. Solutions: add a distinctive secondary shape element to Luma (her hair, a bag, the hoodie's kangaroo pocket reading as a distinct pocket shape, anything that creates unique negative space or protrusion); or push Miri's silhouette to be more distinctive (walking stick she always carries? specific hair shape? apron or shawl that reads in silhouette?). Both characters need their own hook.

**2. Generic Silhouette Language Across Three of Four Characters**
Only Byte has a truly distinctive silhouette. Luma, Cosmo, and Miri are all variations on rectangle-with-circle-head. This is the most common default silhouette in character design precisely because it is the easiest to construct. It is rarely the best choice. The designs need to be pushed to find unique secondary shapes: unusual arm positions that are characteristic, distinctive accessories, asymmetries that carry through even at silhouette scale.

**3. Byte's Cyan Matching Luma's Pixel Cyan — Needs Decision**
Document whether this is intentional. If yes, that's a strong design choice with narrative weight. If no, fix it now before it becomes a continuity issue.

**4. Luma's Identity Without Glitch Effects**
The pixel accent colors are carrying too much of Luma's visual identity. Who is Luma when the glitch is quiet? This needs to be resolved in the character design, not solved retroactively with lighting.

**5. Proportion Diagram Missing Construction Data**
The current proportion diagram is a size comparison chart. A production-ready proportion chart requires labeled construction lines, cross-section widths, and joint placement guides. This is a different document that still needs to be produced.

---

## What's Missing (Visual Assets Still Needed for Characters)

The following are absent and will be required before production can meaningfully proceed:

1. **Character Turnarounds** — Front, 3/4, side, back for each character. Non-negotiable for a hand-drawn or rigged animation pipeline.

2. **Expression Sheets** — Minimum 9 core expressions per character. These are the emotional vocabulary of the show. They do not exist yet.

3. **Posed Character Sheet (Action Poses)** — Each character needs 3-5 poses that communicate personality through body language. The lineup document describes personality well but none of that description is yet translated into poses.

4. **Costuming Variations** — Are these the only outfits? What do these characters wear in water, in formal situations, in cold weather? The show presumably takes place across multiple environments.

5. **Byte Expression/State Variants** — Byte is a creature with pixel-based emotional display. The states (normal eye, corrupted eye, full corruption mode) need a dedicated expression system that is different from biological character expressions.

6. **Character Interaction Scale Reference** — A sheet showing all four characters together in the correct proportional relationship, in a natural grouping pose, to confirm that the designs read well as an ensemble in actual proximity.

7. **Luma/Byte Interaction Reference** — Byte at 6 inches and Luma at 4'9" is a very specific size relationship that will recur constantly in the show. A reference sheet for this specific pairing needs to exist early.

8. **Ensemble Color Harmony Sheet** — All four characters rendered together under the same lighting condition to confirm that the palettes work as an ensemble. Swatches in isolation cannot tell you this.

9. **Labeled Proportion/Construction Guide** — See Critical Issues above.

10. **Miri's Distinctive Design Elements** — From the silhouette review, Miri's distinctive visual elements (hair, accessories, posture cues) are not yet codified in a production-ready form.

---

## Verdict

The color models are close to ready. The silhouette work is not. The proportion diagram is a useful reference but not yet a production document.

On a scale of production readiness, I would place the color swatches at **70%** (solid foundations, ensemble harmony not yet confirmed), the proportion diagram at **50%** (size relationships good, construction data missing), and the silhouettes at **40%** (Byte works, the rest need revision).

The most urgent action is redesigning or refining the Luma silhouette to give her a distinctive shape hook that does not mirror Miri. This is not a minor adjustment. This is a design problem that requires design thinking — not cleanup, not polish, not color. Someone needs to sit with the character, understand what shape language tells Luma's story, and push the design until the shape alone tells you who she is.

Byte is the benchmark. Look at what works there: clear primary shape, distinctive secondary elements, asymmetry, scale contrast. Every other character needs to reach that level of silhouette clarity.

The work shows understanding of the characters at a conceptual level. It does not yet show that understanding through shape alone. Until it does, we are not done with character design.

Do better.

---

*Dmitri Volkov*
*Character Design Lead*
*Cycle 4 Review*
