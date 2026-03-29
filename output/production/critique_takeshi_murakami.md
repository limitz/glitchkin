# CRITIQUE — "Luma & the Glitchkin" Background & Environment Design
**Critic:** Takeshi Murakami, Background Art Director
**Specialty:** Environment design, spatial storytelling, atmospheric depth
**Date:** 2026-03-29

---

## Overall Assessment

I have spent a long time with these documents. The breadth of work here is considerable. Jordan Reed has produced a coherent, detailed, and in several places genuinely good set of environment and prop designs for a show that has real visual potential. The core palette logic is sound. The show's central tension — warm analog world versus cold digital intrusion — is well understood and translated into consistent environment choices. The no-outline-on-backgrounds rule is stated clearly in the style guide and observed throughout the documents, with appropriate and correctly-specified exceptions for interactive foreground objects.

However.

There is a significant gap between what these documents describe and what a background artist would actually need to execute this work. The design documents, impressive in their ambition and narrative detail, are overwhelmingly written as prose intention rather than as actionable visual specification. They describe feelings more than they specify forms. They tell a background artist what a space should feel like, but frequently stop short of telling them precisely how to achieve it. On a production with tight schedules, that gap becomes expensive.

More critically: the Glitch Layer, which should be the most visually extraordinary environment in the show, rests on a set of spatial and rendering rules that have not been tested against each other. Several of these rules, when applied simultaneously, will produce compositions that are visually chaotic rather than legibly alien. The modular tile system is a good idea that needs more structural thought.

The props are the strongest work in this package. The school and Luma's house are strong. Millbrook Main Street is good with reservations. The Glitch Layer is ambitious and partially unresolved.

This is version 1.0. It needs a version 2.0 before production can begin.

---

## Luma's House Interior — Critique

**What is strong:** This is the most fully realized environment in the package. The spatial logic is excellent. The three-source lighting scheme — bay window, monitor stack, desk lamp — creates three compositionally distinct lighting zones that serve the narrative without requiring a director to explicitly call for them. The left/right compositional split (safe window side versus dangerous monitor side) is elegant, simple, and immediately useful to anyone staging scenes. The detail density is appropriate for a hero location. The rotating background gags are well-conceived: the dead succulent with "WATER ME," the traffic cone with a growing plant, Magnus the cat in different positions — these are the kind of specific, committed choices that make a world feel inhabited rather than dressed.

The orange origin cable is a good visual device. The pixel face in THE monitor is correctly understated. The height chart on the kitchen doorframe is, quietly, the best piece of environmental storytelling in this entire package.

**What must be fixed:**

The layering specification for the wide establishing shot places THE monitor stack in the midground at "center-right," but THE monitor is simultaneously described as the visual center of the entire room and the dominant light source casting cyan glow on the couch and floor. A prop this dominant in both value and narrative weight should not be placed off-center in the compositional hierarchy without explicit guidance on how to balance it against the window light. The document states the left/right split logic but does not address the compositional problem of having the brightest point in the frame sitting slightly right of center. Where does the director position Luma and Grandma Miri relative to this imbalance? This needs a staging diagram, not just a prose description.

The ceiling bow — described as important and giving the room a "gently pressing down" quality — is mentioned repeatedly but nowhere in the rendering notes is there instruction for how to achieve this in the flat-graphic style without it looking like a spatial error. A painterly-flat bow in a ceiling is a precise and technically demanding shape. It needs a reference diagram.

The kitchen doorway glow is listed as "#F0A830 — slightly overexposed impression." That is a hex code for a color. It is not instruction for how to paint an overexposed doorway glow in a flat-graphic style. Does the glow bleed onto the near wall? Does it have a soft edge? What is the radius? This is a repeated problem throughout the document — specific colors are given where specific shapes are also required.

The document mentions the dark cyan-tinted shadow tone (#1A3A4A) for shadows falling in the monitor-glow zone. This is correct and good. But the warm-shadow dusty lavender (#A89BBF) and the cool monitor-shadow dark cyan are both present on the couch and coffee table simultaneously, since those objects exist in the overlap zone. The document does not specify how this transition works shape by shape. A background artist will either paint two separate shadow layers (complex) or default to one (wrong). A diagram showing exactly where the lavender shadow ends and the cyan shadow begins on the couch surface is not optional — it is required.

**The scan-line overlay on the CRT glass at 10% opacity:** The style guide states "no texture on character fills, texture belongs on backgrounds." A scan-line texture on the monitor screen is fine. But the specification is inconsistent — the Glitch Layer later uses dithering to replace gradients, while here the monitor screen has a texture overlay achieving a similar visual effect through different means. These two techniques need to be reconciled. Pick one approach for digital/screen surfaces and specify it universally.

---

## Millbrook Main Street — Critique

**What is strong:** The antenna network concept is the most intelligent thematic-visual decision in the entire show. Using the overhead infrastructure as both distinctive visual identity and latent narrative foreshadowing — the town as an unwitting antenna — is genuinely clever. The execution spec is good: the layered wire silhouette operating as its own semi-transparent layer above the background sky but behind the building midground is technically well-considered. The building lean rules (1-4 degrees, consistently per building, adjacent buildings lean in different directions) are exactly the right level of specificity. The building color identity chart is simple and memorable.

The nighttime variant with the antennas developing a faint electric cyan glow, building episode by episode, is the best long-term environmental storytelling detail in the exterior package. If executed with discipline, this will land.

**What must be fixed:**

The street curve. The document says Main Street has "a very subtle curve" and is "not a straight shot." This is stated as a done decision, but there is no specification of the curve's arc, its direction, or how it relates to the clock tower's visual placement at the end. A background artist needs to know: does the curve lean left or right from the camera position? How pronounced is "very subtle" in degrees? A street that curves the wrong way relative to the clock tower placement will break the composition's focal logic entirely. This is not a minor detail. It is the primary compositional structure of the exterior establishing shot.

The building lean rule states that "the lean should be subtle enough that viewers don't consciously register it, but obvious enough that they'd notice immediately if it were corrected to vertical." This is a beautiful description of intent. It is not a specification. How do you test this? What is the visual calibration reference? Without a reference diagram showing a "correct" lean versus an "over-leaned" example, two different background artists on the same production will draw this completely differently, and the result will be an inconsistent street from shot to shot.

The sandwich board is listed as an "action zone" prop for medium shots and gets rotating gag content. Episode 6 reveals the board was knocked over in a chase and "never quite straightened." That is good. But the board's rest position in the slightly-crooked state needs to be specified in the prop sheet, not left as a prose note. How crooked? Five degrees? Fifteen? Someone needs to own that decision and lock it.

The post office: "Even the post office leans slightly — a point of quiet pride or embarrassment depending on who you ask." This is charming writing. It does not help anyone draw the post office. What direction does it lean? The other buildings have directional lean; the post office needs the same treatment.

The diner's non-functional "M" in the neon sign is a good detail. But the document specifies no flicker pattern. A slow flicker? A rapid stutter? This is a background animation note and it needs a timing specification: on for X frames, off for Y frames, repeat on Z-second cycle.

The empty storefront with "WE ARE STILL HERE" scratched into the papered window is one of the best pieces of latent storytelling in the entire exterior package. However: when it is finally revealed in Episode 9, the document does not specify what the text looks like. Is it scratched by a fingernail? A key? What is the line quality? Given that this single reveal is a major payoff, someone needs to have a specific design for it. Not a description. A drawing.

---

## The Glitch Layer — Critique

**What is strong:** The core conceptual framework is the most intellectually sophisticated thinking in the entire project. "A broken memory of what digital space once tried to be" — this is a productive, specific, and narratively resonant foundation. The decision to make this environment beautiful rather than frightening, and to maintain that beauty by establishing definite wrong-rules rather than pure chaos, is correct. The modular tile/platform system is a good production solution. The four platform types provide enough variety for diverse compositions while keeping the visual language coherent. The code waterfall hierarchy (W1, W2, W3 by density and width) is well-specified and reusable. The wrong-direction parallax rule is a genuinely striking idea that will disorient audiences at the exactly right subconscious level.

The pixel duck. I appreciate this. It is the kind of absurdist commitment that makes a show's production culture visible on screen.

**What must be fixed, and this is where I have the most to say:**

The nine rules of Glitch Layer space are listed in a table at the bottom of the document. These are the rules that make the space cohere as a specific wrong place. But they are listed, not weighted. Not all rules should be visible at all times. In any given wide shot, how many rules are simultaneously in violation? If all nine are deployed at once, the composition becomes unreadable. The document does not provide a maximum-violations-per-shot guideline. It does not specify which rules are always-on, which are scene-selective, and which are reserved for specific dramatic purposes. This is a fundamental production gap.

The "Resolution: Backwards" rule states that near objects render at lower resolution (bigger pixel blocks) while distant objects render at higher resolution. The "Scale: Unreliable" rule states that distant objects may appear larger than near ones. The "Parallax: Inverted" rule states that background moves with the camera rather than against it. These three rules are individually distinctive. Applied simultaneously to the same shot, they create a spatial reading experience that may be genuinely disorienting past the point of legibility. The document confidently asserts that this is correct and will feel properly wrong. That may be true. It has not been tested in a composition. A hero test frame for the Glitch Layer wide establishing shot is not optional — it is mandatory before any background artist builds any actual Glitch Layer scene.

The aurora data-streams are described as "the only truly soft/gradient element in the Glitch Layer" because "everything else is flat/sharp." But the code waterfall glow halos are also described as "soft" (3-4 pixel soft halo). The ambient base glow fades out from the void. The platform edge glow is a "secondary slightly-lighter color strip" — but this strip must still have edges, and the document does not specify whether those edges are clean or soft. The "no gradients" discipline, stated firmly for the real world, is being partially relaxed in the Glitch Layer but the points of relaxation are not consistently catalogued. A background artist working on a code waterfall will not know whether the halo edge is clean-sharp or soft, because the document says both things in different places.

The dithering specification is good in concept. "Each dither pixel should be 2-3px at working resolution" is actionable. But working resolution is never specified anywhere in any of these documents. This is a critical omission. "2-3px at working resolution" means completely different things at 1080p, 2K, and 4K. The dither effect — explicitly referenced as a deliberate aesthetic choice — will look entirely different depending on the resolution assumption. What is the show's working resolution? This must be answered.

The Corruption Zones grow throughout the season. This is good long-term visual storytelling. But the document specifies no growth schedule beyond Episode 1 (two zones), Episode 6 (seven zones), and Episode 10 (twelve zones). What about Episodes 2, 3, 4, 5? What about their sizes — not just their count? The "they're bigger" language needs specific size designations at specific episode benchmarks, or a background artist working on Episode 3 will not know how big the Corruption Zone in the background should be.

The color bleeding rule ("1-2 pixel color bleed at color boundaries") is the only rule in the entire table that is specified with a measurement. Every other rule is described behaviorally. This inconsistency in specification depth means that the rendering instruction table is partially useful and partially aspirational. A background artist will execute the color bleed correctly and guess at everything else.

---

## Millbrook School — Critique

**What is strong:** The dual-temperature lighting concept is excellent. Fluorescent-cool versus natural-warm, zoned across the room with precision, is a genuinely strong visual signature for this location. The specification of three lighting zones (left-warm, center-mixed, right-cool) across the classroom is clear and actionable. The use of clean-edged parallelogram shapes for the venetian-blind light bars — specified as CLEAN rather than soft, which is technically correct for slatted blinds — shows close observational attention. The classroom's design thesis ("Normal is maintained by tremendous ongoing effort") is the most emotionally legible location rationale in the package.

Locker 147 is the best long-term background storytelling device in the show. The progression from nothing to pixel grass growing through the vent slots is patient, specific, and earned. The detail about the new combination lock having Glitch Layer symbols where numerals should be is precise and visual. This is the standard the rest of the background storytelling should be held to.

Cosmo's locker details — "No stickers. Cosmo has opinions about unnecessary adhesives on painted metal" — is the most efficient character-building line in the entire background package. One sentence. Complete portrait.

**What must be fixed:**

The hallway width. Eight feet wide for a public school hallway is correct as a real-world specification, but the document simultaneously describes it as creating "strong converging perspective" and "slightly claustrophobic." In a flat-graphic style with gentle perspective and no rigid vanishing points — as specified in the style guide — a space described as "slightly claustrophobic" must be designed differently than one that is simply narrow. The style guide's "gentle perspective, slightly tilted" approach will work against the claustrophobic intention unless specific perspective compression is designed into the shot. The document does not address this conflict. The style guide's perspective rules and this specific hallway's spatial intent need to be reconciled explicitly.

The drop ceiling is specified as having fluorescent fixtures "2 per every 10 feet of hall." At 60 feet of visible hallway, that is 12 fixtures in a 9-foot-high, 8-foot-wide space. The document also says the hallway is "not straight — there's a very gentle rightward lean." What is the effect of 12 fluorescent ceiling fixtures on a rightward-leaning hallway ceiling in the flat-graphic style? The ceiling plane is going to be a dominant compositional element. The document specifies the floor in significant detail (wear paths, tile variation, lighting zone tints) but the ceiling — which in a long hallway shot is often as much of the frame as the floor — receives only a material description. The ceiling needs the same treatment as the floor.

The scan-line texture overlay in the school hallway (8% opacity, horizontal lines running the length of the hallway) is described as "a nod to the monitors at Luma's house, a suggestion that even the most mundane places have a digital layer underneath." This is thematically interesting but visually untested in this context. The scan-line effect on a CRT monitor reads as technological. The same effect on a school hallway floor reads as a rendering artifact if it is not carefully introduced. Is this effect visible to the audience as a deliberate stylistic choice, or as a mistake? The document needs to acknowledge this risk and provide a calibration note.

The classroom's back-corner camera angle is described as "3/4 angle that shows the full front wall, the left wall with windows, and diagonal rows of student desks." A 3/4 angle that simultaneously shows two full walls in a 30x25-foot room requires a very wide lens or a very high camera position. Neither is consistent with the style guide's "no fisheye or extreme wide-angle" rule. The document does not resolve this. Either the room dimensions need to be revisited, the camera position needs to be specified more precisely, or the "full front wall and full left wall" description needs to be walked back to partial visibility of both.

---

## Props — Critique

**What is strong:** These are the best-executed documents in the package. The CRT monitor design is precise, researched, and achieves the correct balance between "real object" and "flat-graphic object." The color specifications for the aged plastic — not white, not yellow, but the specific warm-cream of 30-year-old computer casing (#D8CEB0) — demonstrates real observational care. The decision to distinguish the power LED as the first electric cyan element on an otherwise fully analog object is elegant visual grammar. The electrical tape on Grandma Miri's remote is, as stated in the document, essential. It is the difference between a prop and a character prop.

The "This Exists" principle is the correct governing philosophy for all props in the real-world environments and I endorse it without reservation.

The cable drawer cabinet labels deserve special mention. "MYSTERY," "THE ONES I'M NOT SURE ABOUT," and "IMPORTANT DO NOT OPEN" are not prop decoration. They are world-building. They are better character writing than some shows manage in dialogue.

**What must be fixed:**

The outline treatment rule for interactive props is specified correctly: thin outlines in deep cocoa (#3B2820) at 1.5-2px when the prop is foreground-interactive. This is good. But the document specifies this only for the props covered here. The style guide specifies "foreground objects that characters interact with (doors, chairs, items) get thin outlines." There is no master list of every interactive object in every environment and whether it has been assigned an outline status. Doors appear in the school environment with no specified outline treatment (the terracotta classroom doors are described in the color chart but not addressed in the rendering notes). The couch is an interactive object — characters sit on it constantly. It has no outline specification. This omission will produce inconsistency across the production.

The orange cable is specified in the monitor document as having "a fabric-braided outer covering." This is a significant design detail — a fabric-braided cable in a sea of smooth plastic cables is visually distinctive and important. But the rendering notes for the cable in the house interior environment describe cables generically as "flat, slightly tubular — a highlight along the top edge of each major cable." The orange cable should have a different surface treatment than smooth plastic cables. This is not addressed in the rendering notes for the interior environment. The prop document specifies the cable's appearance; the environment document does not cross-reference that specification. These two documents were not reconciled before submission.

The monitor's "alive" quality section is the best writing in the prop documents and the technique for suggesting aliveness is well-specified (non-uniform glow, power LED, shifting pixel face). However: the pixel face description states that "the position of the two 'eye' pixels and the 'mouth' pixels changes very slightly each episode." This is a long-term continuity requirement. There is no continuity sheet. There is no episode-by-episode tracking of where the face is in each episode. If this detail matters — and the document says it does — it needs a tracking document now, before production begins, or continuity will break by Episode 4.

---

## Environmental Storytelling Assessment

Do these backgrounds tell their own story?

**Luma's House: Yes.** This environment is alive without any characters in it. The origin cable with its burn mark, the pixel face in the monitor, Magnus the cat as a silent recurring presence, the dead succulent with its permanent sticky note, the height chart on the doorframe — individually these are good details. Together they constitute a room that has a history, a relationship between its occupants, and an implied future. If you watched the show with the characters removed, you could reconstruct a significant portion of Grandma Miri's personality, her relationship with Luma, and the show's central mythology, purely from what is in this room. This is the standard. Every other location should be held to this standard.

**Millbrook Main Street: Partially.** The antenna network is excellent latent storytelling. The "FOR LEASE" building developing a full narrative arc purely through background detail across 12 episodes is patient and well-designed. The clock that is always 7 minutes slow is appropriately unexplained. However: the street's storytelling depends heavily on seasonal/episodic accumulation. In Episode 1, in isolation, the street tells a story of "slightly odd small town, warm, slightly past its prime." That is a mood, not a story. The story requires time. That is not wrong — slow reveals are a legitimate narrative strategy. But it means the environment does not pull its full weight in early episodes, and the design team should be aware of that limitation.

**The Glitch Layer: Partially, with significant caveats.** The hidden words in the code waterfalls ("HUNGRY" / "HERE" / "WHERE" / "LUMA" / "NO" / "STAY") are the single best piece of background storytelling in the entire Glitch Layer package. This is because it is character-driven: the words are the Glitchkin's latent voices, embedded in the environment's infrastructure. The Corruption Zone growth across the season is well-paced. However: the Pixel Duck is a self-indulgent background gag, not environmental storytelling. The Mirror Platform (showing Millbrook scenes as reflections) is a more sophisticated version of the same impulse and is more defensible. The phantom platforms (ghosts of old data drifting through) are a good idea that is completely underdeveloped in the document. What data? Whose memory? If the Glitch Layer is "a broken memory of what digital space once tried to be," then the phantom platforms should be visible remnants of specific things. Give them shapes that mean something. Right now they are just "20% opacity platforms, drifting." That is not a story.

**Millbrook School: Yes, slowly.** The school's environmental storytelling is quieter and more cumulative than the house, but it works. The locker 147 arc is the strongest. The backward trophy as a continuity gag establishes that no one is maintaining this building. The "PERSEVERANCE" word-of-the-week running the entire season is a gentle, absurdist joke about institutional inertia. Ms. Petrakis's plant slowly glowing is a correctly patient Glitch Layer intrusion. The class fish growing to impossible size is good. What the school needs, and does not currently have, is a moment of environmental storytelling that requires no time — something in the hallway establishing shot that tells the audience something specific about this school, in Episode 1, without any episode-to-episode payoff. The house has the dead succulent and the pixel face. The school needs its equivalent.

---

## Critical Issues (Must Fix)

1. **No working resolution specified anywhere in the package.** Every pixel measurement, texture overlay percentage, and dither specification is meaningless without it. This must be established before any background artist begins work.

2. **The Glitch Layer rules need a priority hierarchy and a maximum-simultaneous-violations-per-shot guideline.** Nine wrong-rules applied to one composition simultaneously will produce visual chaos. Specify: which rules are always active, which are scene-selective, and which are reserved for dramatic escalation.

3. **The Glitch Layer wide establishing shot requires a hero test frame before production.** The inverted-parallax / backwards-resolution / unreliable-scale rules operating simultaneously in a single shot has not been tested. It may be beautiful. It may be illegible. Find out now.

4. **The scan-line overlay in the school hallway floor needs a calibration test.** At 8% opacity it may read as a deliberate aesthetic choice; it may read as a compression artifact. This must be tested in the actual art style before it is applied to all school shots.

5. **The classroom 3/4 angle needs to be reconciled with the room dimensions and the style guide's no-fisheye rule.** The current description is spatially impossible without a wide-angle lens or a room redesign.

6. **The orange cable fabric-braided texture needs a rendering specification.** It is specified in the prop document and absent from the interior environment rendering notes. These documents must be reconciled.

7. **The pixel face on THE monitor needs a continuity tracking sheet.** Its episodic movement is a long-term storytelling commitment. Without a tracking document, this detail will become an unintentional inconsistency.

8. **A master interactive-object outline list is required.** The current outline treatment rule applies correctly to the four specified props and ambiguously to everything else. Every door, chair, and recurring interactive object in all four environments needs an explicit outline/no-outline designation.

---

## Recommendations

**Immediately:**

- Establish working resolution. Lock it. Put it in the style guide. Every measurement in every document is contingent on this.
- Commission a hero test frame for the Glitch Layer. One full-color, fully-rendered wide establishing shot, all rules applied. This is a production risk that must be resolved in development, not discovered in episode.
- Produce spatial diagrams for Luma's house (lighting zone map showing exactly where lavender shadow ends and cyan shadow begins on the couch and coffee table), Millbrook Main Street (street curve direction and degree, clock tower placement at the curve's end), and the school classroom (camera angle relative to room dimensions).

**Before Version 2.0:**

- Revisit the Glitch Layer rules table. Add a fourth column: "Scene context for application." Not every rule applies to every shot. Define when each rule is active.
- The phantom platforms need specific visual identities. They are currently atmosphere. They should be environmental storytelling.
- The school needs an Episode 1 environmental storytelling beat — something in the establishing shot that works without episodic accumulation.
- Reconcile the scan-line texture approach between the monitor (10% opacity texture overlay) and the school hallway (8% opacity texture overlay) and the Glitch Layer's dithering approach. Three different techniques for digital surface effects need to be unified or explicitly differentiated.
- Add staging diagrams for the Luma's house left/right compositional split. The concept is correct. The implementation needs to be made explicit for directors and layout artists.

**Ongoing:**

- The background gags in all environments are well-conceived and consistently rewarding. The discipline of committing to them — the clock always 7 minutes slow, the broken venetian blind slat never fixed, Magnus always present — must be enforced through production supervision. These details are the show's personality. They will be the first casualties of a tight schedule. Someone must own them explicitly.

---

## Verdict

The work is promising, partially strong, and not yet ready for production.

Jordan Reed clearly understands the visual and thematic ambitions of this show. Luma's house and the prop documents show that this understanding can translate into specific, useful, production-ready design language. The Millbrook exterior and the school are good, with discrete problems that are fixable without structural rework. The Glitch Layer is the show's most important environment and the least ready of the four. Its conceptual framework is genuinely good. Its execution specification is incomplete in ways that will cause real problems.

The documents read more as pitch materials — beautifully written arguments for how the environments should feel — than as production documents that tell an artist exactly what to draw. For concept approval, they are impressive. For greenlight into actual production, they need another pass with a different emphasis: less prose, more diagrams; less "should feel like" and more "is defined as."

The narrative intelligence in these documents — particularly the episodic storytelling arcs embedded in background details — is unusually sophisticated for a first-pass environment package. That intelligence needs to be matched with production specification rigor. Right now one is ahead of the other.

Version 2.0 should bring the specification level of the prop documents to all environment documents.

The work has earned a second draft. It has not earned a production start.

---

*Takeshi Murakami*
*Background Art Director — Guest Critic*
*"Backgrounds should tell their own story. Some of these do. All of them could."*
