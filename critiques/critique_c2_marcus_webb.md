# Animation Timing & Motion Critique — Cycle 2
## "Luma & the Glitchkin" — Cold Open Package

**Critic:** Marcus Webb, Animation Timing & Motion Specialist
**Date:** 2026-03-29
**Documents Reviewed:**
- `characters/main/luma.md` (v2.0)
- `characters/main/byte.md` (v2.0)
- `storyboards/ep01_cold_open.md` (v2.0)
- `production/fx_confetti_density_scale.md` (v1.0)
- `production/fx_spec_cold_open.md` (v1.0)

---

## Overall Assessment

This package has genuine conviction. You can feel the show in the storyboard, you can feel the characters in the design docs, and the FX specs show a production that has thought hard about escalation. That is real work, and I respect it.

But the question I ask of every package I review is this: **does this imply animation, or does it fight it?**

The answer here is: it implies animation in some places, describes it in others, and in a few key spots actively contradicts itself with language that will produce dead or floaty results if it reaches the animator's desk unchanged.

The problems are not catastrophic. None of them require redesigning the characters. But several of them are the kind of soft specification that sounds right when you read it and produces wrong animation when you execute it. That is the most dangerous category of problem, because nobody flags it until the shot is already blocked.

The FX specs are excellent. The storyboard is strong. Luma's action pose has a line of action that tells the truth. Byte's limb vocabulary is the most animatable part of this entire package — specific, physical, readable.

Where it falls short: Luma's hair reactivity system is emotionally described but physically unspecified. Byte's floating physics uses language that will produce floaty, weightless animation if read literally. Several storyboard panels hold too long without motion direction — an animator will park on them, and the sequence will die. And one pose in the character documents is nearly dead on arrival.

Read on. I will be specific.

---

## Character Motion Specs — Assessment

### Luma's Hair Reactivity System

The emotional states for hair behavior (Excited, Scared, Focused, Near Glitch Energy) are described with genuine feeling and are clearly drawn from observation of how expressive hair should work. The intent is correct.

**The problem: none of these states are specified in animation terms.**

"Hair lifts slightly" is not a spec. It is a feeling. An animator who reads "lifts slightly" will interpret it differently from a layout artist, who will interpret it differently from a cleanup artist. By the end of the production pipeline, "slightly" will mean four different things and the hair will be animated inconsistently across an episode.

What is missing:
- **Timing.** How many frames does the lift take? Is it a snappy pop (4-6 frames) or a slow rise (12-16 frames)? These produce completely different emotional reads. A fast hair-lift reads as startlement. A slow hair-lift reads as building excitement. Both are in the character bible — which one is the default for "Excited/Reckless"?
- **Squash and stretch values.** "Hair droops, the whole mass loses volume and flattens" — by how much? 10%? 30%? Is the flattening lateral (the mass gets wider) or purely vertical (it collapses downward)? The shape change must be specified as a ratio or it will vary between animators.
- **Follow-through specification.** The hair is described as trailing behind during the action pose — "the mass shifts backward from the momentum." This is correct and good. But the follow-through when she stops is completely unaddressed. Does the hair catch up immediately? Overshoot and bounce? Settle in two beats or five? Without a follow-through timing spec, every animator will solve this differently and the hair will feel like a different material in every scene.
- **The locked curl count creates a continuity constraint that has no animation guidance.** The spec correctly locks the curl count at 5. But what happens when the hair is at near-maximum panic state (Scared/Deflated, mass compressing) versus near-maximum energy state (Excited, mass expanding)? Are all 5 curls visible in both states? Do some curls merge into the main mass when it compresses? This matters for the cleanup artist, and it is not answered.

**The Static Electric / Near Glitch Energy state** is the one that will cause the most problems. "Curls straighten partially and lift" — this is a transformation from one hair shape to a significantly different hair shape. How many frames? Is this a held transformation or does the hair continuously vibrate in the lifted state? What is the return timing? If this appears in the storyboard during a fast-cut action sequence, the animator has nothing to work from.

**Verdict: the hair system is emotionally correct and animatably insufficient. It needs timing values and shape-change ratios before it goes to the floor.**

---

### Byte's Jitter Spec

The "glitch line" treatment in the line work section says Byte's outline can use a "slight zigzag or dual-offset line at his silhouette edges" — like "a slightly loose JPEG rendering."

This is a description of an aesthetic, not an animation specification.

In animation, "jitter" means something precise: a character's position, line, or element oscillates rapidly between two or more states on a defined timing interval. Without specification, you will get three different interpretations on three different animator desks:

1. A layout artist who draws the zigzag into the character's outline as a static design element — the jitter is drawn, not animated.
2. An animator who applies a random positional offset to the character's body every 2 frames — this produces nauseating, chaotic jitter that reads as a technical error, not a style choice.
3. An animator who offsets the outline layer by 1-2px in alternating frames — this is probably the right approach, but it was not specified.

What needs to be specified:
- **Jitter amplitude:** What is the maximum pixel offset? 1px? 2px? More than 2px starts to read as a rig error.
- **Jitter frequency:** Every frame? Every 2 frames? On holds only, or during movement too?
- **Is the jitter applied to the outline only, or to the entire character body?**
- **Does jitter intensity change with emotional state?** The angry description says confetti cycles more rapidly — does the outline jitter also increase? If so, by how much?

**There is one place in the spec where jitter IS concretely described** — the floating movement in Panel 9 of the storyboard: "he moves in micro-increments, hovering with a slight vibration, as if each moment of position is a separate frame at a slightly lower framerate than the world around him." That is an excellent animation description. It tells me the character moves on twos when the world is on ones, creating a perceived framerate difference. That is a specific, implementable, correct choice. That language should be exported to the character bible and used as the foundation for all Byte motion specs.

**Verdict: the jitter spec needs the storyboard's language imported into the character document, plus amplitude and frequency numbers.**

---

### Byte's Float Physics

This is the most critical motion issue in the package. Read this note carefully.

The spec says: Byte "floats approximately 0.25 heads above any surface" and "does not walk — he floats." The floating mechanism is described as pixel confetti squares circulating below his lower limbs.

What is not specified is: **how does Byte's float respond to physical forces?**

Every object that floats in animation has an implied physics — and that physics determines whether it feels alive or dead. Balloons float differently from hummingbirds, which float differently from objects on strings, which float differently from objects in water. All of them float. None of them feel the same.

The spec gives Byte a constant hover height (0.25 heads) and a baseline wobble (5° left-right oscillation at 0.5Hz in the Processing/Idle state). But it does not answer:

- **Does the hover height change under acceleration?** When Byte moves forward, does he dip slightly (like a helicopter banking), or does he maintain exactly 0.25 heads above the surface? A constant height during movement reads as mechanical and dead. A slight dip into acceleration reads alive.
- **What is the arc of Byte's movement paths?** Characters who float should never move in straight lines between positions. They should arc through space. Is this specified for Byte? No. The danger is that an animator reads "floats" and keys him in straight-line linear interpolation between positions, which will make him look like a camera dolly, not a living creature.
- **Drag and overshoot on stops.** When Byte stops moving, does he overshoot his mark and drift back? If yes, by how much and over how many frames? If no — if he stops dead — then the float has no weight and will read as a slideshow.
- **The 5° wobble oscillation** is only specified for the Processing/Idle state. What is the wobble frequency and amplitude during action states? During the alarmed Configuration 3, does the wobble increase? Does it stop? The emotional states describe limb configurations and pixel-eye symbols very specifically, but the baseline body motion for each state is completely absent.

The storyboard (Panel 9) partially addresses this by describing movement as "micro-increments" and "slight vibration" — but this is a note for one panel, not a system. It needs to become a system.

**The specific risk:** if animators work from the character bible without the storyboard panel note, Byte will float at a constant height in straight-line paths with a wobble on holds only. This will produce the flattest, most lifeless read of a floating character I can imagine. He will look like a still image moving on rails.

**Verdict: Byte's float physics must be fully specified as a motion system, not a design description. Minimum: arc requirement for movement paths, hover height variation under acceleration, overshoot behavior on stops, wobble amplitude table per emotional state.**

---

## Storyboard — Motion Assessment

The storyboard shows strong visual thinking. Lee Tanaka understands staging and understands how to build a sequence emotionally. The glitch escalation arc is clear, the palette shift from warm to cold is well-timed, and the symmetrical two-shot in Panel 13 is the right solution for the comedy apex — it is exactly the kind of choice that makes an action legible at a glance.

I am going to call out specific panels where the motion direction is strong, and specific panels where it will cause problems.

---

### What Works

**Panel 03 — The First Pixel.** "One pixel changes. Electric cyan. It pulses slowly once. Twice." This is perfect. The beat is specific, it is restrained, and it gives the animator exactly one thing to do. The directive to make the pixel "the most saturated thing in the frame by a factor of ten" is exactly right — this is how you direct color as a motion tool.

**Panel 07 — The Phase-Through.** "He passes through the surface like breaking the tension of a soap bubble." This is a physical reference that every animator understands. The action has a quality. Soap bubble tension breaking is a specific physical event with a specific feel: surface tension holds, then sudden release, then scatter. This is good.

**Panel 11 — Eyes Snap Open.** "Closed. OPEN. No intermediate blink." This is the correct call. The hard cut from fully closed to fully open is the most startling thing possible. The spec is clear and the animator cannot misread it.

**Panel 12 — The Comma.** "Full hold. 1.5 seconds. Nobody moves. Nobody blinks." This is correctly used as a held moment because the content of the hold is meaningful — the audience is processing. The pixel confetti "in slow motion" during the hold is the right detail.

**Panel 13 — Symmetrical Apex.** The compositional spec for this panel is the best-directed panel in the storyboard. Every element is placed, every trajectory is described, the symmetry is justified. This panel will work. The only note: "This is a HELD FRAME — 1.5 seconds. Everything is FROZEN at the apex. No in-betweens for this 1.5s." This is correct — at a comedy apex, holding a single extreme frame without in-betweens creates a visual BANG. This is the right choice. Good.

---

### What Will Cause Problems

**Panel 04 — Luma's Introduction.** This is the single longest sustained description in the storyboard, and it contains a critical failure: Luma's breathing is specified as "a 3-second loop," but NO other motion is specified for her during the hold. "The NEON CRUNCH bag crinkles imperceptibly from her breathing." That is too soft. A 2-second hold with only imperceptible crinkle for motion will die completely on screen.

The panel note says: "The sleeping POSITION must communicate recklessness and impulsiveness before a single line of dialogue." This is correct and the pose itself is well-described. But a hold is not a pose — it is time. Two seconds of a static sleeping character with imperceptible bag crinkle will read as a freeze frame to most audiences, and they will assume something went wrong. You need at least one more motion element: the dangling leg swinging slightly on the breathing cycle, the notebook page riffling from a breath, the chip puffs on the couch shifting. Something with enough amplitude to confirm "this is animation, not a still." The breathing rise-and-fall alone is insufficient at this character scale.

**Panel 08 — Byte's Character Introduction.** "He does a full 360° turn taking in the room." This is a full character turn on a first reveal. That is a significant ask, and the timing is completely unspecified. A 360° turn at 12 frames is a snap that reads as agitated. At 48 frames it reads as methodical. At 72 frames it reads as awestruck. Which one is correct for a character who is "disgusted but assessing"? I would say 36-48 frames (a deliberate but not ponderous survey) — but it should be stated. Also: does he stay at constant height through the turn, or does the floating bob slightly as he rotates? This affects whether the turn reads as a mechanical camera pan or a living creature looking around.

**Panel 09 — Byte Floating Toward Luma.** "He moves in micro-increments, hovering with a slight vibration, as if each moment of position is a separate frame at a slightly lower framerate than the world around him." As noted above, this is excellent motion direction. However: the overall movement path is not specified. Is he moving in a straight horizontal line toward the couch? Is he arcing slightly upward as he gains elevation and then descending toward the couch level? The path of travel matters enormously for read. A straight horizontal float reads as mechanical. An arcing approach reads as cautious, living movement.

**Panel 14 — Byte Ricocheting.** The multi-ghost exposure idea (approach in cyan, impact in magenta, exit in white-cyan) is a strong visual choice for communicating trajectory in a still frame. This panel works well on paper. The risk: "smear frames appropriate and encouraged" is too loose as a direction. Smear frames work when the motion direction is clear to the animator executing them. What is the arc of Byte's ricochet? Is the impact on the bookshelf a bounce at equal angle of incidence, or does he deform around the shelf and launch at a steeper angle? The pixel trail spec shows the path (lower-left entry, upper-right impact, upper-left arc continuation) but not the velocity profile. Does he decelerate into the impact or arrive at full speed? The deceleration profile changes the smear shape entirely.

**Panel 15 — Luma Falling.** "Her hair defying gravity — it has expanded further upward in the fall, forming a perfect circle." A perfect circle of hair is a significant departure from the character design's asymmetric triangular mass. For a panic state, some expansion is correct. But "perfect circle" is symmetrical — and the character design explicitly forbids symmetrical hair at all times, including in motion. The description here contradicts the design document. The panic hair should expand and lift, but it should not become symmetrical. The correct description would be: "the mass puffs upward and forward (in the direction of fall), the volume increasing dramatically, flyaways multiplying, but the asymmetric silhouette maintained."

---

## FX Motion Specs — Assessment

### Confetti Density Scale (`fx_confetti_density_scale.md`)

This is the best document in the package from a production standpoint. The five-level system is clear, the particle count ranges are specific, the color mix ratios are specific, and the motion behavior descriptions are specific enough to implement.

**Level 1** — "Occasional micro-flutter: a particle may twitch one pixel in a random direction once every 8–12 frames. Not on a schedule — randomized." This is a correct and implementable spec. The randomization caveat is important and correctly stated.

**Level 2** — "Pixel tumble: particles rotate 90 degrees on their axis occasionally (every 6–10 frames). Since they are square, this creates a subtle flip effect." This is specific and correct. The observation that a square rotating 90 degrees is a flip is accurate and shows real understanding of pixel-based motion.

**Level 3** — "Collision behavior: Large particles that pass near each other briefly form composite shapes (L-shaped, T-shaped, irregular rectangles) for 1–2 frames before separating." This is good. It is specific about duration (1-2 frames), specific about shape result, and gives the visual reason for the behavior.

**Level 4** — "Magnetism: Small particles snap to character silhouettes and crawl along the outline." This is the most complex behavior specified, and it needs one more piece of information: the crawl speed. "Crawl along the outline" at 1px per frame is extremely slow and menacing. At 5px per frame it reads as frantic. At 10px per frame it reads as the character being consumed. Which register is intended for a climactic Level 4 moment?

**The transition rules** are solid. The prohibition on jumping from Level 1 to Level 4 in a single cut is important and correctly stated. The "return to Level 1, never 0 after a Level 3 event" rule is also correct — the world should never feel fully clean again after a significant breach.

**One gap:** the document specifies particle sizes as pixel multiples but does not specify whether particle SIZE changes between density levels. At Level 1, sizes are 2-4px. At Level 4, sizes range up to 32px. But when a scene transitions from Level 2 to Level 3, do the existing particles grow, or do new larger particles spawn alongside the existing small ones? The transition behavior between levels is described as sequential escalation, but the particle generation mechanics during a transition are not specified. This will create inconsistency between animators.

---

### Cold Open FX Spec (`fx_spec_cold_open.md`)

This document is exceptional in its frame-by-frame specificity. The frame counts, the pixel sizes, the opacity fade rates, the layer order stacks — this is production-ready specification language. Whoever wrote this has done this before and understands what animators need. My notes are refinements, not corrections.

**FX Moment 1 — Phase-Through:**

The phase shimmer ("every other frame, the character art has a 1–2px cyan offset duplicate at 50% opacity, shifted 2 pixels right and 1 pixel up") is correct in principle and correctly specified. My one question: when Byte's lower body is still inside the screen and only his upper body has emerged, does the phase shimmer apply to the entire character or only to the portion inside the screen? The answer is: only to the portion inside the screen (the emerging portion should feel materialized while the portion still inside has misregistered). This is not addressed and needs to be.

**The landing arc described as "a slight upward trajectory like a person climbing out of water"** is a vivid and correct physical reference. A person climbing out of water pushes up and arcs slightly upward before gravity takes them back down. This is the correct trajectory for Byte clearing the screen surface. This reference is good enough to use in a directing session.

**FX Moment 2 — Pixel Shockwave:**

"Byte body at lowest contact position (squash pose — Byte compresses vertically ~20% for maximum impact read)." The 20% compression value is specific and correct — this is enough to read clearly on a small character without looking like a deformation error. Well specified.

"A second ring spawns at the landing point at Frame 9." The echo ring is a correct physical choice (real impacts produce multiple wave fronts) and specifying the spawn frame (9, not 8, not 10 — frame 9) is the right level of precision for a document like this.

**The one structural problem:** the sequence describes Byte's squash at the impact frame and then the spring-up as the shockwave expands — but there is no specification of the spring-up timing or the overshoot. "Byte springs back up from the squash pose (stretch up)" — how many frames? How far does the stretch take him above his rest height? Does he wobble after the spring, or land at exactly his float height and hold? Without this, the animator will guess, and the guess will probably be too slow (making him look heavy) or too fast (making the landing feel weightless).

**FX Moment 3 — Monitors Flickering:**

The cascading flicker sequence (dominant monitor first, then nearest two, then further, then edges) is a well-designed escalation. This is correct physics — a power surge propagates outward from a source, and you should always see the chain. The specific frame numbers for each stage (Frame 19, 22, 23, 24) are the right level of precision.

"The cool blue room-wash overlay: gradually normalizes as the eye adjusts. Fade the overlay from 20% → 8% opacity over these 30 frames." This is a strong production note. The fade implies the characters' eyes adjusting — the audience reads this as the room settling into its new state, not as a correction. This is sophisticated use of lighting in a flat-art style.

**The subliminal content table** (Byte's eye at Frame 35 for 1 frame at 60% opacity; "HELP" at Frame 48 for 1 frame at 40% opacity, etc.) is correctly specified for subliminal function. 1-frame flashes at 40-70% opacity on background monitors will register subliminally for most viewers and consciously for the pause-framers. This is exactly right.

---

## Pose Dynamism Assessment

### Luma — "Mid-Leap, Arms Out, About to Grab Something"

**The pose has a stated line of action** — "a strong C-curve runs from the rear raised foot, through the spine, to the reaching lead arm." This is correct. A C-curve is a real line of action for a leaping character with a trailing leg. The pose is not dead.

**What is missing:** The spec describes body positioning in terms of angles from vertical, which is technically correct but produces no feel when read. "Lead leg extended forward and downward" is geometry. What is missing is the WHY the pose reads as mid-leap and not mid-fall.

The difference between a leap and a fall in animation is: **anticipation of landing** versus **resignation to impact**. A leaping character has their weight forward, their head UP (looking toward the target, not down at the ground), their reaching arm active and reaching (not just extended). Luma's pose description has all of these elements — but they are described individually, not in terms of how they work together to create the leap read.

The critical note: "Head is upright relative to the body (not tilted with the torso lean) — she's looking forward at her target." This is correct and important. The head upright while the body leans is what separates a controlled leap from a stumble. This is well-specified and the animator should be directed to it explicitly.

**The pixel confetti trail** — "approximately 6-8 particles, each a different glitch color" — is too few for a mid-leap action pose. At this speed and energy level, the confetti trail should be more like 15-20 particles in a clear directional stream behind her. 6-8 reads as ambient presence, not momentum trail. This is a density mismatch with the energy of the pose.

**Overall verdict for Luma's pose:** Not dead. The C-curve is correct, the head direction is correct, the extended lead arm is correct. The pose will read as a leap if the line of action is maintained in execution. The confetti count is too low for the energy level.

---

### Byte — "Riding on Luma's Shoulder, Pointing Urgently"

This pose is the most animatable design spec in the package. Every element is specified in terms of angle and relationship to the body. The limb configuration gives a clear read (pointing limb at maximum extension, back limb pressed to body, body tilted toward the point). The expression pairing (Alarmed + Reluctant Effort, Warning Triangle pixel eye) is specific and correct.

**One concern:** the pose describes Byte's lower limbs as "curl loosely over the back of her shoulder — hooked, not gripping." Loose curling at a low-contact point on a character who is floating and moving provides almost no stability rationale. Why isn't he floating off her shoulder when she moves? The spec doesn't address this. It is a storytelling logic gap that audiences won't consciously notice but will feel as a faint wrongness. The solution is simple: the pixel confetti below his feet should react to the hoodie's surface — the spec briefly notes this ("tiny squares bouncing off the orange fabric") — and this interaction should be specified as the mechanism that keeps him stable on her shoulder. Establish this clearly and it becomes a character physics rule.

---

## Critical Issues

**1. Byte's float physics is underspecified in a way that will produce dead animation.**
No arc specification, no hover height variation under acceleration, no overshoot behavior. This is the highest-priority fix.

**2. Luma's hair system is emotionally correct and physically useless.**
Timing values, shape-change ratios, and follow-through specs are absent. Without these, the hair will be animated inconsistently across the episode.

**3. Byte's jitter has no amplitude or frequency values.**
The storyboard contains better motion language for Byte's movement than the character bible. This needs to be fixed. The storyboard language should be imported and formalized.

**4. Panel 04's hold is undertimed.**
Two seconds of a sleeping character with imperceptible motion will read as a freeze frame at standard viewing conditions. More motion is needed during this hold.

**5. Panel 15's "perfect circle" hair contradicts the character design document.**
Luma's hair is never symmetrical. A perfect circle during the fall breaks a production rule. Fix the description.

**6. Luma's leap pose pixel confetti count (6-8) is too low for the energy level.**
The mid-leap action pose should have a directional confetti trail of 15-20 particles, not ambient 6-8.

**7. The Phase-Through spec does not address which portion of Byte receives the shimmer during partial emergence.**
This gap will produce inconsistent results across animators.

---

## Recommendations

**Immediate (before animation floor opens):**

1. **Write Byte's Float Physics System** as a standalone half-page spec. Minimum required: movement arc specification (all paths must arc, never linear), hover height variation (+/- 0.1 heads under acceleration), overshoot amount on stops (0.15 heads past the mark, settle over 8 frames), and a wobble amplitude table per emotional state (idle: 5°/0.5Hz as specified; alarmed: 12°/2Hz; action: no wobble, replaced by arc momentum).

2. **Add timing values to Luma's hair states.** Four states, four timing pairs: onset (how many frames to transition into the state) and return (how many frames to return from the state). Also: shape change ratios (Scared state: height -25%, width +10%; Excited state: height +15%, width +10%; etc.). These numbers can be approximate. Approximate numbers are infinitely more useful than no numbers.

3. **Formalize Byte's jitter spec.** Adopt the storyboard's "lower framerate than the world around him" approach as the character-level standard. Specify: body moves on 2s when the scene is on 1s (default). Outline offset: 1px alternating per frame during holds, synchronized with the 2s body motion during movement. Jitter increases to 2px offset in alarmed/frightened states.

4. **Panel 04: add a second motion element** to the sleeping Luma hold. Suggestion: her dangling left leg swings gently on a 5-second pendulum cycle, offset from the 3-second breathing cycle. Two overlapping slow cycles are enough to confirm animation without overpowering the quiet of the scene.

5. **Panel 15: rewrite "perfect circle" to maintain asymmetry.** Suggest: "the hair mass puffs upward and in the direction of forward fall (toward screen-left), expanding approximately 40% in volume. The right side (viewer's left) gains more volume than the left — the directional weight of the fall pushes the mass asymmetrically. Flyaways multiply dramatically."

6. **Phase-Through spec: clarify shimmer application.** Add: "The phase shimmer duplicate applies only to the portion of Byte's body that is inside the screen surface. The emerged portion of Byte's body is rendered at full opacity without shimmer. The dividing line between shimmer and no-shimmer is the plane of the CRT glass surface."

**Secondary (before pencil test):**

7. **Add a movement path arc requirement** to Byte's character bible, drawn from the storyboard's panel language. One paragraph is sufficient.

8. **Increase leap pose confetti** from 6-8 particles to 15-20, described as a directional stream trailing behind the motion, not ambient scatter.

9. **Level 4 density scale: add crawl speed for magnetism behavior.** Suggest: 3px per frame along the silhouette, randomized direction per particle (some clockwise, some counter-clockwise). This is slow enough to feel menacing without overwhelming the character art.

---

## Verdict

This is a project with a strong visual identity and a production team that is thinking seriously about execution. The FX spec in particular represents a level of frame-specific precision that most productions don't hit until they are already in trouble. The storyboard communicates what it needs to communicate. The characters are designed with genuine understanding of how shape language and color carry emotion.

The motion problems in this package are not conceptual. They are specification gaps — places where the work stopped at "what it should feel like" and did not take the additional step to "what the animator must do to produce that feel." Those two things are different. The first is design. The second is production.

The gap between them is where animation goes to die.

Fix the float physics. Fix the hair timing. Fix the jitter spec. Add motion to Panel 04. Correct the hair in Panel 15. The package will be production-ready when those fixes are in.

Until then, I am approving the FX specs, the storyboard structure, and Byte's limb vocabulary. Everything else goes back to the desk.

---

*Marcus Webb*
*Animation Timing & Motion Specialist*
*Critique prepared for: Cycle 2 review*
