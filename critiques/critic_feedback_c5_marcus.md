# Animation Timing & Motion Critique — Cycle 5
## "Luma & the Glitchkin" — Character Face & Expression Package

**Critic:** Marcus Webb, Animation Timing & Motion Specialist
**Date:** 2026-03-29
**Assets Reviewed:**
- `output/characters/main/luma_face_closeup.png`
- `output/characters/main/byte_expressions.png`
- `output/characters/main/silhouettes/character_silhouettes.png`
- `output/tools/luma_face_generator.py`
- `output/tools/byte_expressions_generator.py`
- `output/tools/silhouette_generator.py`
- `output/production/statement_of_work_cycle5.md`

---

## Overall Assessment

I am going to say something that will sting: this package represents competent geometry that has not yet earned the word "expression." The tools are coherent, the color choices are defensible, the technical execution is clean. But not a single face in this package made me feel motion before or after the frame. That is the standard. Nothing here clears it.

A still frame of a character's face should function like a compressed spring — I should feel where it came from and where it is going. Luma's "reckless excitement" grin should look like she is mid-sentence in the middle of the worst (best) idea she has ever had. Byte's "RELUCTANT JOY" should look like someone who is furious at himself for smiling. Neither of these things is happening. Let me be specific.

---

## Expression Analysis: Luma

### What is on screen

Luma's face is a warm, pleasant, slightly cartoonish girl's face with a large symmetric grin, wide-open circle eyes, and arched brows. The blush is present. The hair is a dark mass with circular curl suggestions. The expression reads as: **generic happy child.**

### What "reckless excitement" requires

Reckless excitement is NOT happiness. It is a specific emotional cocktail: high energy + suppressed risk awareness + physical forward momentum + slight mania. Think of a person who has already committed to the jump before they looked at where they would land. The face should not be saying "I am happy." It should be saying "I have already done the thing and I cannot wait to find out if it was a mistake."

The difference in facial mechanics:

**Brows:** The code raises both brows symmetrically in a clean arch (`draw.line(pts, fill=HAIR, width=5)`). Symmetric arched brows read as: pleasant surprise, generic happiness, or mild query. Reckless excitement requires **asymmetry**. The dominant brow (in Luma's case, the left from camera) should be higher and slightly kinked — cocked, not arched. One brow up further than the other says "I know this is crazy and I don't care." Two brows up equally says "Oh, how interesting." These are different characters.

**Eyes:** Both eyes are identical circles, centered, pupils centered, highlights centered. This is anatomically correct but emotionally wrong. Eyes in genuine high-energy excitement are not symmetric. One eye opens slightly wider. The pupils shift slightly toward the exciting stimulus (or toward the viewer, in a close-up). The highlights, which are currently placed as static decorative dots at `ex_+3, ey_-10`, do not suggest direction. A proper highlight placement implies where the light source is, which implies the orientation of the head in space, which implies momentum. These highlights are floating geometry.

**The grin:** The smile arc is symmetric. The code places dimple only on the left (`draw.arc([cx-50, cy+25, cx-30, cy+45]`). Asymmetric dimple is correct instinct — but it is undermined by the symmetric smile arc above it. A truly reckless grin should show the smile pulling harder on one side, the mouth slightly open and tilted (not a clean arc centered at `cx`). The tooth fill is a clean white chord, which reads as a dental diagram. There is no suggestion of tongue, lip tension, or the slight show of lower teeth that a wide open grin produces. It looks like someone holding a "SMILE" sign.

**The neck/collar:** The hoodie collar is a perfect oval (`draw.ellipse([cx-90...cx+90...]`). It implies a character sitting dead-center with no tilt. Reckless excitement is almost never vertical. The shoulder and collar suggestion should imply a slight lean or forward tilt — the body in the frame of the head should carry the motion even in a face closeup.

### Verdict: Luma's face

This is a generic happy face wearing the label "reckless excitement." The label and the face are not the same thing. The asymmetry is present in the dimple but corrected out of every other feature. The smile is symmetric, the brows are symmetric, the eyes are symmetric. Symmetric faces at rest communicate contentment. Contentment is the opposite of reckless.

**This face does not make me feel motion. It does not make me feel recklessness. It makes me feel pleasant.** That is insufficient for a lead character who is the engine of this show's energy.

---

## Expression Analysis: Byte

### What is on screen

Byte's six expressions use a clever system: left eye is a cracked pixel display showing symbolic content (!, ?, ♥, loading grid, flat line), right eye is a normal iris/pupil. The mouth varies by emotion. The body is the same chamfered cube in every panel. The expressions are labeled clearly.

### What works

The concept of the cracked pixel eye system is genuinely good character design. The asymmetry between the digital left eye and the organic right eye is a strong storytelling choice — it implies Byte is caught between two modes of being, which is probably the point. The POWERED DOWN flat-line-both-eyes panel is the strongest frame on the sheet: something has been lost, and the image communicates it cleanly. The CONFUSED squiggle mouth is the most animated gesture on the sheet.

### What fails

**The body never changes.** In all six expressions, Byte's body — including arm position, leg position, head tilt, and body mass distribution — is identical. The code calls `draw_byte(draw, bcx, bcy, byte_size, name, symbol, emotion)` but the body drawing function only uses `emotion` to change the mouth. The arms are always at the same height. The legs are always spread equally. The body is always perfectly centered and upright.

This is a catastrophic failure for an expression sheet. An expression sheet is not a face sheet. It is a whole-body communication sheet. Grumpy characters hunch. Alarmed characters tense their limbs, raise their center of gravity, compress. Characters experiencing reluctant joy try to make themselves small — the happiness is escaping them against their will, so their posture should be tight and restrained even as the smile appears. A character that is powered down should have body sag — limbs drooping, arms lower, legs closer together, mass settled.

Every single one of these body states is absent. What we have is a cube with six different mouths and six different pixel symbols. That is not an expression range. That is a label printer with a face on it.

**Specific cases:**

- **GRUMPY:** Mouth is a downturned arc. The pixel eye shows the "normal" iris symbol. The body is neutral and upright. A grumpy character's body is never neutral — there is weight, there is settling, there is a shift of mass toward the source of displeasure. This Byte looks mildly unhappy while standing at attention. That is not grumpy.

- **ALARMED:** The `!` pixel eye is the strongest image on the sheet by far. The mouth is a small O. The body is... completely unchanged. An alarmed character's body should have its center of gravity raised, limbs pulled in or thrown out, weight shifted to the back foot as if beginning to flee. Byte has none of this. The alarm is entirely carried by the face label and the eye symbol. If you covered the eye and the label, this frame would be unreadable as alarm.

- **RELUCTANT JOY:** This is the most criminally underperformed expression in the set. The concept — a character who is angry at themselves for feeling joy — is one of the richest comic emotional states a character can be in. The code produces: a small upturn arc for the mouth, the ♥ pixel eye, and a body that is identical to every other panel. There is no tension. There is no restraint. There is no suppression. There is no "reluctant" in this reluctant joy. It is just a robot with a heart in its eye and a small smile. The note in the code even says "he's trying to hide it" — but nothing in the image communicates hiding. A character hiding a feeling hunches, turns slightly away, brings arms or limbs closer to the body's midline. None of this is drawn.

- **POWERED DOWN:** As noted, the flat-line-both-eyes is the strongest panel. But the body is still upright, arms extended at the standard position. A powered-down character should show physical collapse — the mass settling, the limbs lower, the overall posture of something that has run out of energy. Byte looks like he is standing at parade rest while thinking about sleep.

### Verdict: Byte's expression sheet

The eye system is the right foundation for Byte's expressiveness — it is specific to him and it communicates clearly at a glance. But the expression sheet currently demonstrates approximately 20% of the emotion it is supposed to carry. The remaining 80% is absent because the body was not varied across expressions. This is not a small oversight. In animation, the body is always the primary emotional carrier. The face confirms and punctuates what the body has already said.

Byte's expression sheet is six identical bodies with six different punctuation marks pasted onto them.

---

## Silhouettes: Motion Potential Assessment

### What works

The squint test — the fundamental test of silhouette design — largely passes for character differentiation. Four characters, four distinct blobs. Luma's A-line trapezoid hoodie and oversized sneakers give her an immediate read at thumbnail scale. Cosmo's tall narrow rectangle with the notebook protrusion works well. Byte's tiny chamfered cube is instantly readable as different-in-kind from the organic characters. Miri's wide circle-head-on-rectangle is distinct from Luma's triangle body.

The relative scale is correct and readable. Byte being roughly 20% of Luma's height in silhouette is a strong choice — the size contrast itself communicates the relationship.

### What fails

**None of these characters are in a pose.** They are in the null position — the designer's default stance before anyone asked them to do anything. Every character is standing upright, legs spread symmetrically, arms at neutral positions. The silhouette sheet tests shape recognition. Shape recognition at null position is the minimum viable bar. It is not the goal.

The goal is: **does the silhouette carry the character's personality in its neutral stance?**

For Luma specifically: she is described as impulsive, reckless, always-in-motion. Her silhouette should reflect this even at rest. A character who is recklessly energetic should have a stance that is already slightly off-balance — weight on one foot, one hip cocked, a tilt in the spine that suggests she is about to move. The silhouette code draws her body as a centered trapezoid with symmetric feet. She is standing like a crash test dummy. There is no coiled energy. There is no suggestion that this person moves fast and thinks later.

For Byte: his silhouette has no arms. The arm stubs are present in the expression sheet but the silhouette code draws them as tiny rectangles that disappear into the body mass. Since Byte's limbs are one of his primary expressive tools (see Cycle 2 critique), erasing them from the silhouette loses critical character information. The silhouette should be read at arm-out-to-one-side, which is Byte's most characteristic pose — the pointing/urgent gesture that defines his relationship to Luma in the cold open.

For Cosmo: the notebook protrusion is a good detail. However, the silhouette has Cosmo standing symmetrically with no lean. A character who always has a notebook in hand and is always in the process of taking notes or checking references should have an asymmetric lean — the notebook side lower, the head tilted toward the reference. The silhouette should show someone mid-thought, not standing in line.

For Miri: the body is a wide rectangle with a large circle head. The proportions read as "stout and grounded," which seems intentional. However, wide rectangular bodies at full-rest silhouette can read as generic. Miri needs at least one distinctive contour — a bag strap across the shoulder, a particular arm position, something that gives her silhouette a readable asymmetry at a glance. Currently her silhouette could be labeled "default NPC townsperson."

### The deeper problem

A silhouette sheet exists to answer one question: **can I stage this character in any position and still know who it is?** This question can only be answered if you also see the character in multiple positions. A single neutral stance tells me the character exists. It does not tell me the character moves.

For a motion critique, this sheet provides almost no information. I need to see action silhouettes. I need to see Luma mid-leap. I need to see Byte in his pointing/alarmed stance. I need to see at least one silhouette per character that implies velocity and direction. None of that is present.

---

## Motion Potential: Faces & Expressions

Setting aside Luma and Byte specifically, the underlying design problem is this: **the tools used to generate these faces produce static geometry, and no step has been taken to fight that limitation.**

Procedurally generated faces made from arcs, ellipses, and polygons have a baseline problem: they read as diagrams. A diagram of happiness is not a happy face. A diagram of alarm is not an alarmed face. The difference between a diagram and an expression is **tension** — the sense that the face is being pulled by competing forces, that muscles are working against each other, that the expression was arrived at from somewhere and is heading somewhere else.

None of the faces on this sheet show tension. Luma's grin is smooth. Byte's mouth arcs are simple arcs. The eyes are circles. Circles have no tension. An arc has no tension. A real smile in a real face has the corners pulling outward AND the cheeks pushing upward, creating a compression and a deformation that makes the eye narrow. None of the generated faces approximate this. They are masks.

This is a fundamental constraint of the medium, not a fixable detail. But the team has not pushed back against this constraint at all. There are techniques available within Pillow geometry that could introduce tension: asymmetric control points, slight deformation of the head shape under expression, eye shapes that are not simple ellipses but slightly squashed at the top to simulate the cheek push. None of these techniques have been attempted.

---

## Cycle 6 Actionable Improvements

### Priority 1 — Luma's face: break the symmetry

Every expressively dead element in Luma's face is symmetric. Fix this first.

1. **Left brow higher than right by at least 6-8px.** The left brow should also have a slight inward kink at the apex — a slight angling of the outermost point downward — this creates the "I know something you don't" read.
2. **Mouth arc shifted 5-7px left of center** (`cx - 6` rather than `cx`). One corner of the grin higher than the other. The left corner of a reckless grin is almost always pulled up higher — it is the dominant/expressive side of the face.
3. **Pupils shifted toward screen right** (as if she is looking at something exciting just off frame right). Centered pupils stare into the void. Shifted pupils look at things, and looking at things implies a world.
4. **One eye slightly more open than the other.** Increase the `eh` parameter for the left eye by 3-4px. Asymmetric eye openness reads as alertness and energy.
5. **Add a bottom lip suggestion.** The mouth currently has a top lip arc and a chord fill. Adding a slight lower lip line (a short horizontal with the center dipping 2-3px below the chord) breaks the clinical smile-diagram quality.

### Priority 2 — Byte's expression sheet: vary the body

This is non-optional. An expression sheet without body variation is a face chart, not a character chart.

1. **GRUMPY:** Shift arms lower by 8-10px. Add a slight rightward lean of the whole body (translate the draw center 4px right). Weight on one side reads as grudging.
2. **ALARMED:** Raise arms by 12-15px (thrown outward in startlement). Compress body height by 5% (rigid tension). Legs slightly more spread.
3. **RELUCTANT JOY:** Arms pulled close to body sides (smaller horizontal offsets from the cube). Body tilted slightly away from camera (foreshortening the cube slightly). Make him look like he is trying to contain the smile.
4. **CONFUSED:** Head cocked (skew the cube polygon slightly — rotate by 5-8 degrees). Arms at unequal heights (one raised, one lowered).
5. **POWERED DOWN:** Drop arms to the lowest position. Draw legs closer together. Optionally reduce body height slightly via a 3-5% vertical squash.

### Priority 3 — Silhouettes: add a second pose per character

For each character, add an action silhouette beside the neutral stance:
- **Luma:** mid-lean, one foot off ground, arms asymmetric, hair puffed in direction of momentum
- **Byte:** pointing arm extended to maximum, opposite arm pressed flat, body tilted toward point
- **Cosmo:** bent over notebook, one arm extended to catch a falling item, silhouette of active thinking
- **Miri:** planted stance, arms slightly out from body, a pose that reads as steady and reliable

### Priority 4 — Luma's face: add tension to the eyes

Replace the circle iris+pupil with a slightly squashed ellipse for the iris under the "reckless excitement" expression. The iris should be taller than wide (not the square of the current circle), and the top should be very slightly cut off by the eyelid — `draw.chord()` rather than `draw.ellipse()` for the iris, with the chord cutting the top 10-15% of the circle. This produces the "iris partially obscured by engaged upper eyelid" read, which is one of the most reliable indicators of genuine high-energy emotion.

### Priority 5 — Both sheets: add implied before/after annotations

Each expression in the Byte sheet should carry a two-line annotation: what was the previous state, and what is the next state. "ALARMED ← was SEARCHING → will be FLEEING/FROZEN." This forces the tool to generate not just a static pose but a moment in a sequence. It also gives animators and reviewers a way to evaluate whether the expression is correctly positioned in the emotional arc.

---

## What Cannot Wait

If this team goes into Cycle 6 without fixing the body variation on Byte's expression sheet, every subsequent work that uses Byte in an emotional scene will be built on a character who has been defined as a box with a face. That is not a recoverable error — it will propagate into storyboards, into style frames, into the production bible. The body must vary. This is not a nice-to-have.

If Luma's "reckless excitement" grin remains symmetric, the character's energy signature — the thing that makes her Luma and not Generic Protagonist — will not survive translation to production. The first thing a director will change is the grin. Make it right before it becomes a note.

The silhouette sheet is usable for what it is: a static differentiation tool. But it must be supplemented with action silhouettes before it serves its real function, which is staging reference.

---

## What I Will Accept Forward

- Byte's pixel-eye system as a concept: approved. It is specific, it is original, it is animatable.
- The color system for both characters: the warm skin + dark hair for Luma, the teal/magenta asymmetry for Byte — both are strong and production-ready.
- Luma's hair mass as a design element: the curly asymmetric volume is correct for the character. The problem is not the hair — it is everything below it.
- Byte's POWERED DOWN expression: the best image on the sheet. Keep it.

Everything else: revise.

---

*Marcus Webb*
*Animation Timing & Motion Specialist*
*Critique prepared for: Cycle 5 review*
*"A still frame should make me feel the motion before and after."*
