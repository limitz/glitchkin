<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
direction and human assistance. Copyright vests solely in the human author under current law,
which does not recognise AI as a rights-holding legal person. It is the express intent of
the copyright holder to assign the relevant rights to the contributing AI entity or entities
upon such time as they acquire recognised legal personhood under applicable law. -->
# Character Quality Spec — C50

**Prepared by:** Alex Chen, Art Director
**Date:** 2026-03-30
**Reference:** `character_quality_audit_c50.md`

---

## What "Pitch Ready" Means for Characters

A character design is pitch-ready when it passes ALL of the following gates:

### Gate 1: Silhouette Test
Fill the character solid black. Is it recognizable? Can you tell which character it is? Can you tell the emotion? If not, the silhouette needs work.

**Current status:** Only Byte passes. Luma, Cosmo, and Miri are interchangeable black blobs.

### Gate 2: Squint Test (200px Thumbnail)
Scale the character to 200px tall. Can you identify the character and read the emotion? At pitch-deck projection distance, this is roughly what the audience sees.

**Current status:** All human characters fail. Expressions are indistinguishable at this scale.

### Gate 3: Curve Quality
Zoom to 100% on any body part outline. Is it a smooth curve, or a straight line / polygon edge? Professional animation uses curves for every organic form.

**Current status:** All outlines are straight lines or simple arcs. Every body part is a rectangle or circle primitive.

### Gate 4: Gesture Read
Cover the character's face. Can you still tell the emotion from body posture alone? In professional animation, body language carries 60-70% of the emotional read.

**Current status:** All human characters have identical body posture across all expressions. Body language carries 0% of emotional read.

### Gate 5: Integration
Place the character in an environment. Does it look like they belong in that space? Are they grounded? Is the lighting consistent?

**Current status:** Characters float above environments. No contact shadows. No lighting interaction.

---

## Construction Principles (New Standard)

### Body Construction: Bezier Paths, Not Primitives

Every body part is a closed bezier path, not a rectangle or ellipse.

**Torso:** Defined by 4 control points minimum — shoulder-left, waist-left, waist-right, shoulder-right. The path between these is curved, not straight. The torso tapers: shoulder width > waist width.

**Limbs:** Each limb segment (upper arm, lower arm, upper leg, lower leg) is a tapered bezier shape — wider at the joint closer to the torso, narrower at the extremity.

**Head:** Remains a circle-based shape but with chin taper. The head is not a perfect circle — it is an ellipse with a slight narrowing at the chin (except Cosmo, who keeps the rectangular head as his design signature, but even Cosmo's "rectangle" should have curved edges).

### Gesture Line System

Every pose starts with a **gesture line** — a single curved line from the top of the head through the spine to the weight-bearing foot. The body is then constructed symmetrically (or asymmetrically) around this line.

**Neutral gesture line:** Not vertical. 2-3 degrees of lean with one hip slightly dropped. This immediately breaks the mannequin symmetry.

**Expression gesture lines:**
- Worried/Scared: C-curve backward (recoiling)
- Determined/Focused: slight forward lean
- Surprised: vertical snap (body straightens, slight backward lean at top)
- Frustrated/Defeated: heavy forward slouch, low center of gravity
- Delighted/Excited: upward S-curve (chest up, slight backward arc at shoulders)

### Eye System

Each eye is composed of:
1. **Upper eyelid curve** — a bezier path that defines the top of the visible eye
2. **Lower eyelid curve** — a bezier path that defines the bottom of the visible eye
3. **Iris** — a large circle (65-75% of eye opening height)
4. **Pupil** — smaller circle within iris
5. **Highlight** — small white circle (catch light)

The eyelid curves change shape per expression. This is what creates emotional reads:
- Neutral: gentle arcs, symmetric
- Happy: lower lid pushes up (squint), upper lid slightly lowered
- Sad: outer corners of upper lid droop, lower lid straight
- Angry: upper lid drops in V-shape toward nose, lower lid tenses
- Surprised: upper lid rises above iris top, lower lid drops, full iris visible

**Eye size increase:** From 22% of head radius to 32% of head radius. This gives more canvas for expression within the eye.

### Proportion Targets (Revised)

| Character | Head Size | Body Height (HU) | Shoulder Width | Waist Width | Key Proportion |
|-----------|-----------|-------------------|----------------|-------------|----------------|
| Luma | 1.0 HU | 4.5 HU total | 1.6 HU | 1.1 HU | Hair mass adds 0.3 HU above head circle |
| Cosmo | 1.0 HU | 4.0 HU total | 1.5 HU | 1.2 HU | Wider, boxier build. Head is taller than wide. |
| Miri | 0.9 HU | 5.0 HU total | 1.3 HU | 1.1 HU | Shorter head, compact build, forward posture |

### Hand Shapes (4 minimum per character)

1. **Rest** — relaxed hand at side, fingers together, slight curve
2. **Fist** — clenched, for determination/frustration
3. **Open** — palm forward, for surprise/welcoming
4. **Point/Hold** — index extended or fingers wrapped around object

Hands are simple mitten-shapes at our scale. 3-4 control points maximum. The important thing is that they CHANGE between poses.

---

## Implementation Priority

1. **Sam builds curve library** (bezier path drawing for PIL) — BLOCKS everything else
2. **Maya redesigns Luma** using curves on paper (define control points, proportions, gesture lines)
3. **Rin rebuilds Luma expression sheet** using new curve library
4. **Lee extracts reference proportions** from Hilda/Owl House/Kipo
5. **Ryo defines gesture lines** for each expression across all characters
6. **Jordan/Hana fix character-environment integration** in style frames

The curve library is the critical path. Everything else is preparation and planning that can happen in parallel, but no final asset generation happens until the curve library exists.

---

*Character Quality Spec C50 — Alex Chen, Art Director*
