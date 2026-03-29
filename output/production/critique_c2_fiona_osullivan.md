# PRODUCTION DESIGN CRITIQUE — CYCLE 2
## "Luma & the Glitchkin"
**Critic:** Fiona O'Sullivan — Production Design Critic
**Specialty:** Production pipeline readiness, design system consistency, scalability for large crews
**Date:** 2026-03-29
**Documents Reviewed:**
- `/home/wipkat/team/output/style_guide.md`
- `/home/wipkat/team/output/production/production_bible.md`
- `/home/wipkat/team/output/backgrounds/production_outline_exceptions.md`
- `/home/wipkat/team/output/backgrounds/props/pixel_face_continuity.md`
- `/home/wipkat/team/output/production/fx_confetti_density_scale.md`
- `/home/wipkat/team/output/production/corruption_visual_brief.md`
- `/home/wipkat/team/output/characters/main/character_lineup.md`

---

## Overall Assessment

This system has genuine bones. I have seen shows enter production with far less, and I have seen shows enter production with this much and still fall apart — because "good thinking on paper" and "survivable in a 20-artist pipeline" are two completely different things.

The honest answer is: **not yet producible at crew scale.** What exists is an excellent creative development package — vision is clear, aesthetic direction is coherent, the conceptual work is strong. But the translation from "creative direction" to "production system" is incomplete. There are critical specification gaps, missing handoff documents, absent templates, zero turnaround sheets, and a number of internal contradictions that would, at crew scale, produce a quiet disaster of inconsistent output that only becomes visible after 3 episodes of finished animation.

The encouraging news: the gaps are fixable. Nothing here is a fundamental design problem. But they need to be fixed before a crew of 20 touches a single file.

What follows is specific. I do not do vague. Vague critique is useless in production.

---

## Style Guide Assessment

The style guide is well-written as a document. The creative vision is communicated clearly. An artist reading it will understand the show's aesthetic intent. That is the threshold it clears.

What it does not yet clear is the threshold of being a **production specification**. A style guide that can run a large crew needs to answer questions before artists ask them. This one leaves too many questions unanswered.

**What works:**
- The core palette is fully specified with hex codes. Good.
- The "DO/DON'T" sections are clear and actionable.
- The style family references (Hilda, Owl House, Kipo) are calibrated correctly for a crew — shared reference points prevent drift.
- The line weight hierarchy (character vs. background, silhouette vs. internal) is correctly documented.
- The prohibition on gradients on characters is stated clearly.

**What is missing or insufficiently specified:**

1. **No shadow tone specification.** The style guide says "one shadow tone, no gradient" repeatedly. It never specifies what that shadow tone IS. What is Luma's shadow color? What is the rule — is it a fixed color per character, a percentage darker than the base, a multiply blend mode at a fixed opacity? On a show with flat cel-shadow as a core principle, this is a production-critical specification that every single cleanup and color artist will need. Its absence means every artist will invent their own shadow convention. You will get 20 different shadow conventions.

2. **No highlight specification.** The style guide mentions "one highlight tone max." Same problem. No spec. No hex. No blending rule.

3. **The grain texture is mentioned but never specified.** "Subtle grain textures, scan-line overlays, and pixel-dither patterns" — no intensity value, no scale, no whether this is a compositing layer or drawn, no approved texture library. Two background artists will produce completely different grain results.

4. **The "jittery lines" for Glitchkin are not specified beyond "slight zigzag or displacement."** At what amplitude? At what frequency? Over what stroke length? This is currently an invitation for artistic interpretation, which means inconsistency.

5. **The Quick Reference Card at the end is the most useful section, and it is the shortest.** Expand this. This is what artists tape to their monitor.

6. **No expression sheet reference or character-specific appendices.** The style guide references character designs but does not define them. At crew scale, the style guide should contain or formally link to turnaround sheets, expression charts, and color model sheets — none of which exist yet.

---

## Production Bible Assessment

The production bible is structurally sound and covers the right territory. The episode format section is professional and usable. The tone guidelines are specific enough to be functional. The world-building is well organized.

**What works:**
- The "What's In / What's Out" tone section is exactly what a production bible should contain. Clear. Enforced by example. Useful for storyboard artists and directors.
- The file naming convention is good and specific (`[category]_[descriptor]_[version].[ext]`). This will actually be followed if enforced, because it is simple.
- The workflow section is correct: all work begins with INBOX, art director sign-off required, no overwriting.

**Critical gaps:**

1. **No episode count for Season 1.** The pixel face continuity doc references episodes 1 through 12, strongly implying a 12-episode season. The production bible does not state this. I now know the season length from a prop continuity document, not from the bible. That is backward. The season order commitment is a production-defining number. It belongs in the bible.

2. **No character expression sheets referenced or existing.** The bible describes character personalities and design hooks, but there is no specification of approved emotional states, no list of canonized expression poses, no cross-reference to model sheets that presumably exist. The character lineup document references expressions by number ("Expression 1," "Expression 5," "Expression 6," "Expression 8") as if a shared expression library exists — but I can find no such document. If artists are referencing expressions by number without a shared expression chart, they are working from memory. That fails.

3. **No color model sheets referenced.** The bible says "see style_guide.md for full color specifications." The style guide has hex codes for the environmental palette. Where are the character color models? What are Luma's approved colors for every part of her design? This would normally be a dedicated color model sheet per character.

4. **The workflow section says "Alex Chen signs off on all character designs, key backgrounds, and style frames."** This is a single-point-of-failure bottleneck with no escalation path. What happens when Alex is unavailable? Who is the second approval authority? No deputy approval path is defined. At episode 6 of a 12-episode season with a full crew, the art director cannot be the only gatekeeper.

5. **Resolution standard says "300 DPI minimum" for PNG exports.** DPI is irrelevant for screen-bound animation deliverables. The correct specification is pixel dimensions at the working resolution. 300 DPI at what canvas size? This is a holdover from print production logic. For animation production, specify pixel dimensions: 1920x1080 (or 3840x2160 working). DPI is not the production standard.

6. **No delivery pipeline described.** Files go into the output folder. Then what? Who reviews what, in what order, at what stage? Is there a pre-production checklist, a cleanup checklist, a color check step? There is no production pipeline flowchart or stage definition. This is not a style problem — it is a workflow problem that will cause missed handoffs.

---

## Cross-Document Consistency

This is where I found the most significant systemic issues. Documents were clearly written by different people, at different times, without a final cross-reference pass. The contradictions and ambiguities listed here will cause production inconsistencies.

**Issue 1 — Line color for Grandma Miri: contradiction between documents.**

The style guide states: "Line color is Deep Cocoa (#3B2820) by default — NOT black. For Glitchkin, line color shifts to Void Black (#0A0A14) or a dark version of their body color."

The character lineup document (Section 6, design system table) specifies Grandma Miri's line color as Warm Dark Brown (#4A2810) — "softer than Deep Cocoa, not Void Black."

The style guide does not mention Warm Dark Brown (#4A2810) anywhere. It does not mention that Miri is a special case. It does not list this color in the palette. An artist reading only the style guide will draw Miri with Deep Cocoa lines. An artist reading only the character lineup document will draw Miri with Warm Dark Brown lines. Unless the style guide is updated to acknowledge this exception and specify the rule for when it applies, two artists will produce Miri with different line colors.

This needs to be resolved with a single authoritative statement in the style guide and in the character-specific model sheet: "Grandma Miri is the exception to the Deep Cocoa default. Her line color is #4A2810."

**Issue 2 — Cosmo's hoodie vs. striped shirt: terminology inconsistency.**

The style guide calls Cosmo's garment a "striped shirt." The production bible calls it the same. The character lineup calls it a "tucked shirt + pressed pants." These are all consistent. However — Cosmo's character entry in the production bible says he has "a striped shirt (sage green and cream)." The character lineup color table lists his primary color as "Cerulean Blue #5B8DB8" and secondary as "Sage Green #7A9E7E." If his shirt is sage green and cream (per the bible), then his primary identity color (cerulean blue) is not his shirt color. Where does cerulean blue come from? His pants? A jacket? This is never clarified. "Primary color" in the lineup context should mean "the color that identifies this character at distance" — if that is his shirt and it is sage/cream, call it sage. If cerulean blue is his pants, say so. The color model sheet should make this unambiguous.

**Issue 3 — "Pixel confetti" size specification: gap between documents.**

The style guide says: "Add 'pixel confetti' (tiny floating square particles) near any glitch activity."

The fx_confetti_density_scale document specifies at Level 1: "2x2 px to 4x4 px."
The production_outline_exceptions document says: "pixel confetti particles: Never outlined. They are light particles — tiny 2x2 squares at 50% opacity in the background."

The outline exceptions doc gives a single fixed size (2x2) and a fixed opacity (50%). The fx spec gives a range (2x2 to 4x4) and opacity of 30-50%. These are not catastrophically inconsistent but they are inconsistent. The production_outline_exceptions doc appears to be describing a specific background-layer instance of confetti, while the fx spec describes the full system. However, an artist who reads only the outline exceptions doc will assume all confetti is 2x2 at 50%. This should be reconciled with a note: "See fx_confetti_density_scale.md for full specification. The 2x2 size and 50% opacity referenced here applies specifically to confetti in the background layer only."

**Issue 4 — Hot Magenta in Corruption context vs. Glitch palette context.**

The corruption_visual_brief.md states: "Hot Magenta appears ONLY as a pulse/flash (brief and internal) not as a body color." This is clearly documented.

The fx_confetti_density_scale.md at Level 3 states: "30% Hot Magenta (#FF2D6B) — first significant appearance of Hot Magenta, indicating real threat." Level 4 lists Hot Magenta as the dominant color at 35%.

The question that will arise in production: when a Level 3 or Level 4 confetti event occurs in the same frame as an active Corruption presence, how does the Hot Magenta confetti interact visually with the Corruption's Hot Magenta pulse? The confetti spec says Magenta confetti particles appear and drift. The Corruption spec says Magenta only appears as a radial wipe pulse through the body. In a composited frame, these two uses of the same color will either harmonize or clash. There is no guidance for this interaction. A background artist and an FX artist working on the same frame without communication will produce an inconsistent result.

**Issue 5 — Byte's size: consistent, but needs one clarification.**

All documents consistently state Byte is approximately 6 inches tall. Good. However, the character lineup specifies he is "~0.5 Luma heads" on the ground. The character lineup also notes that Luma is "3.5 Luma heads tall." If Byte is 0.5 Luma heads at 6 inches, then Luma is approximately 42 inches (3.5 feet) tall in-world — which is extremely short for a 12-year-old. The "heads" measurement is an internal proportion system, not real-world scale. This is a normal cartoon convention, but it needs to be explicitly stated as such, because an artist trying to reconcile "Byte is 6 inches" with "Byte is 0.5 Luma heads" could erroneously try to apply real-world scale to the proportion grid, producing a 3.5-foot-tall Luma. A single clarifying note: "Head-unit measurements are proportional only and do not correspond to real-world scale" would prevent this confusion.

**Issue 6 — The expression number system in the lineup document.**

Section 9 of the character lineup references expressions by number: "Expression 1," "Expression 5," "Expression 6," "Expression 8." These numbers are referenced as if they come from a shared document. No such document is linked or exists in the output directory. Either this document needs to be created and linked, or these references need to be replaced with descriptive names.

---

## Pipeline Readiness

If production started tomorrow with a crew of 20, here is the order in which things would break:

**First to break (Day 1-2):**
Character color models. The moment a cleanup artist starts on a character other than Luma, they will not have a color model sheet. They will use the hex codes from the style guide and the text descriptions from the character lineup document. Two artists on the same character will produce different results. There is no single "here is every color on this character, labeled, approved, with your shadow tone" document. This breaks immediately.

**Second to break (Week 1):**
Shadow tones. Not specified anywhere for any character. As above. This will result in a note from the color supervisor on Episode 1 that reads "shadow colors are inconsistent across scenes, please advise." There is no document to advise with.

**Third to break (Week 1-2):**
The outline exception rules in production. The production_outline_exceptions.md is an excellent document — genuinely one of the better prop-outline tracking systems I have seen for a project at this stage. However, it requires a continuity supervisor to enforce it scene by scene. Is there a continuity supervisor? The production bible does not list this role. The pixel face continuity doc says "the continuity supervisor should compare the current episode's face position." No such person is defined in the team structure. Who is this? If it is Alex Chen, then see the single-point-of-failure note above.

**Fourth to break (Episode 2-3):**
Glitch layer environment variants. The corruption_visual_brief.md explicitly requires "background artists must prepare a Stage 2 variant of any Glitch Layer or digital-world environment — the same location, but with reduced saturation, cracks, and Corruption mass presence." There is no Stage 2 variant template. There is no specification for what exactly "30-50% saturation reduction" means in production terms (a compositing layer? a re-colored background file?). There is no file naming convention for variants (`bg_glitchlayer_entrance_stage2_v01.png`?). The existing naming convention does not include a stage designation. When Episode 3 needs this, the background department will improvise a solution. By Episode 6, there will be three different conventions in use.

**Fifth to break (Episode 3-4):**
Cosmo's knowledge of Glitchkin. The production bible states: "Cosmo gains awareness over the course of season 1." This is a story state change that has major visual implications — specifically, whether and when Cosmo can see pixel confetti, glitch contamination halos, and Glitchkin in their natural state. When does this awareness begin? What is the visual rule for what Cosmo sees vs. what he doesn't in each episode? If a storyboard artist puts confetti visible to Cosmo in a shot during Episode 3, is that correct? There is no document that tracks Cosmo's awareness state episode by episode. The pixel face has a continuity document. Cosmo's perceptual state does not. These are equally important to production continuity.

---

## The Corruption — Production Readiness Assessment

The corruption_visual_brief.md is the strongest single document in this package. It is specific, visual, consistent, and usable. An artist reading it will know what to draw. This is what every document should aspire to.

That said, it has production gaps:

**What is excellent:**
- The three "tells" are each specifically described with hex codes, blend modes, scale, and frequency. This is professional-level specification.
- The right-angle movement rule for tendrils is one of the clearest visual differentiators I have seen for a villain in a TV-animation bible. It is specific, drawable, and memorable.
- The Stage 1/2/3 breakdown gives FX and BG departments a clear escalation guide. The particle behavior at each stage is consistent with the fx_confetti_density_scale.md (this is one of the few places the documents positively reinforce each other).
- The "what the Corruption does NOT contain" color list is a production gem. Print this. Post it at every workstation.

**What is missing:**

1. **No approved design exists.** The brief tells artists what the Corruption IS. It does not show them what it LOOKS like. "An irregular polygon cluster with no right angles" and "a churning shifting void-mass" are good descriptions that will produce 20 different drawings. The Corruption needs at minimum a Stage 1, Stage 2, and Stage 3 reference image — even rough, even concept-level. A visual villain without a visual model is a written villain.

2. **The tendril movement rule (right-angle paths only, never diagonal) is critically important and will be incredibly hard to enforce without a storyboard example.** An animator who has never drawn this before will instinctively add curves and diagonals. The rule exists in the document. It needs an illustrated example — a single diagram showing a tendril moving in right-angle steps vs. the wrong (diagonal/curved) version — to be enforceable.

3. **Stage 2 requires a "Stage 2 variant" background.** As noted above, no template or file convention exists for this. This is a deliverable requirement that has no production support structure.

4. **The "Stage 3 heals in cascade" resolution sequence is described in beautiful detail.** It is not described in production terms. How many frames? Over how many scenes? Does color return in a specific order per element? "A slow, beautiful re-saturation" needs frame counts and a color return sequence if it is going to be animated consistently by a full crew.

5. **Corruption Zone outline rule is mentioned in production_outline_exceptions.md (1.5px Hot Magenta outline) but is not cross-referenced in corruption_visual_brief.md.** An FX artist reading only the corruption brief will not know this rule exists. A background artist reading only the outline exceptions doc will know the rule but may not know enough about the Corruption's visual staging to apply it correctly. Neither document says "see the other document."

---

## Continuity and Tracking Systems Assessment

**The pixel_face_continuity.md is excellent.** Seriously. This is professional continuity documentation. The episode-by-episode log table, the expression vocabulary with labeled states, the opacity protocol, the grid specification — this is exactly how continuity tracking should work. If every recurring visual element in this show had a document like this, the show would be producible. The fact that this level of care went into a background easter egg speaks well of the team's attention to narrative craft.

However:

1. **No one is assigned to maintain it yet.** The "artist sign-off" column in the episode log is blank. The role of "continuity supervisor" is referenced but not filled. This document will remain pristine until production begins and then will be ignored because no one has been designated as its keeper.

2. **The document references `/home/wipkat/team/output/backgrounds/environments/lumas_house_interior.md` and `/home/wipkat/team/output/backgrounds/props/key_props.md` as cross-references.** These documents exist (I can see them in the output directory). But they are not part of the review scope, and the cross-reference in pixel_face_continuity.md is to local filesystem paths — not relative paths, not versioned references. If the file system structure ever changes, those cross-references become dead links. Use document-relative cross-references or a document index.

3. **There is no equivalent continuity document for:**
   - The right-angle crack marks left by the Corruption (which are "permanent until addressed" per the corruption brief — this is a continuity tracking obligation across the entire season)
   - Cosmo's notebook pages and annotations (the notebook is a recurring prop with content that may need tracking)
   - Cosmo's awareness state episode by episode (as noted in Pipeline Readiness above)
   - Glitchkin that have been "contained" vs. "befriended" (different visual outcomes, presumably different continuity states)
   - Miri's mug presence/absence state (the character lineup makes this a deliberate tell; it should be tracked)

4. **The production_outline_exceptions.md mentions "Locker 147" as a narrative prop requiring outlines from Episode 1.** The document acknowledges it has "escalating importance" but does not cross-reference to a story document that explains what that importance is. A background artist who has not read the full story treatment (which does not appear to exist yet) will not know why locker 147 matters, which means they will not know how carefully to treat its continuity across scenes. The reason a prop is important should be documented alongside the instruction to treat it carefully.

---

## Critical Issues

In priority order — the things that will cause real production damage if not resolved before crew onboarding:

**CRITICAL — Must fix before any artist starts work:**

1. **Character color model sheets do not exist.** Every character needs a single-page color reference: every color on the character, hex code labeled, shadow tone specified, highlight tone specified, line color specified, pattern details specified. This is the most fundamental production document in any animation pipeline, and it is absent. The information exists in fragments across multiple documents, but it has never been consolidated into a per-character color model.

2. **No turnaround sheets exist.** The production bible lists a `turnarounds/` directory. The style guide lists it. No turnaround sheets exist. Without a front/side/back rotation reference, every artist draws the character from a different base model. Character inconsistency in this pipeline will start with geometry, not color.

3. **Shadow tone is unspecified.** See Style Guide Assessment. This needs a specific rule before any color work begins.

4. **The expression number system references a nonexistent document.** Create an expression chart for each main character, or remove the numbered references.

**HIGH — Should be resolved before Episode 1 enters production:**

5. **Cosmo's awareness state continuity.** Which episodes can Cosmo perceive glitch activity? Who decides? Where is it documented?

6. **Stage 2 background variant process.** File naming, template, compositing method — all undefined.

7. **Continuity supervisor role must be assigned and documented in the production bible.** This person is referenced in two documents and does not exist.

8. **The Corruption needs at minimum a Stage 1 reference drawing.** One drawing. Stage 1. Something. "Beautiful but unproducible" is the trap. This description is, currently, unproducible without a visual model.

**MEDIUM — Should be resolved before Episode 3:**

9. **Cross-references between documents need to be added.** Corruption brief should reference outline exceptions. Outline exceptions should reference fx_confetti_density_scale. The style guide should explicitly note Miri's Warm Dark Brown line exception.

10. **DPI specification in the production bible should be replaced with pixel dimension specification.**

11. **Season 1 episode count should be explicitly stated in the production bible.**

12. **Corruption Stage 3 resolution sequence needs frame-count guidance.**

---

## Recommendations

1. **Prioritize the character color model sheets above all other production work.** One page per character. All colors labeled. Approved. This document is the foundation that everything else is built on.

2. **Create a master cross-reference index.** One document that lists every production document, what it covers, and what it cross-references. If a new team member asks "where do I find the rule for X?", the answer should always be "the index." Right now the answer is "read everything and hope it's in there."

3. **Assign the continuity supervisor role now, before Episode 1.** The pixel face continuity doc is too good to become a dead document because no one owns it. Whoever is assigned must also create the Corruption crack continuity tracker and the Cosmo awareness tracker.

4. **The corruption_visual_brief.md's "Summary Checklist — Drawing The Corruption" is exactly the right production tool.** Create the same checklist for every recurring complex element: one for drawing Byte correctly, one for drawing the Glitch Layer correctly, one for any scene involving the confetti system. Checklists are how you enforce a design system with 20 artists.

5. **The fx_confetti_density_scale.md is excellent and should be considered the model for how all FX elements are documented going forward.** If a new FX element is introduced in Season 1, it should be specified at this level of detail before production.

6. **Hold a cross-document review session before crew onboarding.** Assign one person to read every document in the output folder and flag every contradiction, every undefined term, every dangling reference. This session should produce a list of corrections that are made to the canonical documents. Then lock document versions. After lockdown, changes require Art Director sign-off.

7. **The production bible's workflow section should be expanded to include a delivery pipeline.** What stages does an asset pass through? Sketch > Cleanup > Color > Background Composite > Director Review > Art Director Final? Define these stages. Define what "done" means at each stage. Define who reviews at each gate.

---

## Verdict

This is genuinely promising work. The creative vision is clear, the design system has real coherence, and the best documents here — the corruption brief, the fx density scale, the pixel face continuity doc, the outline exceptions — are at professional production-document quality. The character design thinking in the lineup document is strong and the shape language system is well-constructed.

But I have watched beautiful shows break down in production because no one built the infrastructure between "vision" and "output at scale." The vision is here. The infrastructure is not, yet.

The gap is not creative. The gap is operational. Missing color models. Missing turnarounds. Missing shadow specifications. Missing continuity roles. Missing cross-references. Missing pipeline definition. Each of these individually is a manageable problem. Together, with 20 artists waiting for guidance, they become a production crisis in slow motion.

**My overall assessment: Do not onboard a full crew until the character color model sheets and turnaround sheets exist. Everything else can be in progress. Those two things cannot be.** A crew with clear color models and turnarounds and missing documentation will produce inconsistent secondary documents. A crew without color models and turnarounds will produce inconsistent characters, and inconsistent characters kill audience attachment, and that is not recoverable in post.

Fix the foundation. The structure above it is worth protecting.

---

*Fiona O'Sullivan — Production Design Critic*
*"The show that cannot be produced consistently is not a show. It is a concept with a deadline."*
