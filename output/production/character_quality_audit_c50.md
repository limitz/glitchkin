<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
direction and human assistance. Copyright vests solely in the human author under current law,
which does not recognise AI as a rights-holding legal person. It is the express intent of
the copyright holder to assign the relevant rights to the contributing AI entity or entities
upon such time as they acquire recognised legal personhood under applicable law. -->
# Character Quality Audit — Cycle 50

**Prepared by:** Alex Chen, Art Director
**Date:** 2026-03-30
**Scope:** All character assets (expression sheets, turnarounds, lineup, characters in style frames and storyboard panels)

---

## Executive Summary

Our backgrounds are competent. Our characters are not. After reviewing all 20 reference images from Hilda, The Owl House, and Kipo alongside every character asset we have produced, the gap is stark. Our characters look like **assembled geometry** — circles bolted to rectangles with lines drawn on them. The reference shows also use simple shapes, but their characters feel alive. This document diagnoses why, and defines what we must fix.

---

## Part 1: Character-by-Character Audit

### Luma (Expression Sheet v006, Turnaround v004)

**Construction/Silhouette:**
- Body is a rectangle with arms as straight tubes. No taper, no curve, no gesture line.
- Torso-to-hip transition is a hard right angle. Professional designs use a continuous S-curve or at minimum a tapered trapezoid.
- Hair is a flat semicircle sitting on top of a circle head. No volume, no bounce, no asymmetry.
- Hoodie reads as a colored rectangle, not as fabric on a body.
- Arms attach at fixed points on the torso rectangle. No shoulder integration despite our shoulder rule — the rule describes small pixel offsets but the underlying construction is still a socket on a box.

**Facial Expressiveness:**
- Eyes are circles with smaller circles inside. No eyelid shape variation, no squash/stretch, no lid curvature changes between expressions.
- Mouth is a simple arc or line. No lip shape, no asymmetry, no mouth interior.
- Brows are straight lines with slight angle changes. Professional brows curve, taper, and interact with the eye area.
- Face reads identically across expressions when viewed at thumbnail scale. The "squint test" fails — expressions depend entirely on tiny line differences that disappear at pitch-deck viewing distance.

**Gesture/Weight:**
- Every pose has identical center of gravity. No lean, no shift, no weight bearing.
- "Worried" Luma and "Curious" Luma have the same body — only the face changes marginally.
- No contrapposto, no line of action, no gesture line whatsoever.

**Integration with backgrounds:**
- In SF01, Luma is a flat paper doll pasted onto an environment with actual depth and atmosphere.
- In SF05 (kitchen), Luma and Miri float above the floor — no grounding shadows, no contact with the environment.
- In storyboard panels, characters are blobs of color that don't interact with the space.

### Cosmo (Expression Sheet v008, Turnaround v003)

**Construction/Silhouette:**
- The most overtly rectangular character. Head is a rounded rectangle, body is a rectangle, legs are rectangles. He looks like a Minecraft character with rounded corners.
- Glasses are the strongest design element but they sit flat on the face — no perspective, no cheek interaction.
- Striped shirt is well-conceived as a visual identifier but the stripes are perfectly parallel horizontal lines on a flat rectangle — they should curve with the body form.

**Facial Expressiveness:**
- Better expression range than Luma (skeptical brow raise reads well), but the underlying face construction is identical across views in the turnaround — side view and 3/4 view show the same flat face just rotated.
- Mouth is a simple shape — no teeth, no inner mouth, no lip differentiation.

**Gesture/Weight:**
- "Awkward" and "Worried" should have radically different body language. They don't. Arms change position but the torso, hips, and legs are identical.
- The turnaround shows four poses that are essentially the same pose rotated. No personality in the standing position.

### Grandma Miri (Expression Sheet v008, Turnaround)

**Construction/Silhouette:**
- Smallest, most compact character. The proportions (shorter, rounder) are appropriate for the character.
- But the same rectangle-assembly problem. Body is a rectangle with a cardigan colored on top. No fabric drape, no weight.
- Hair bun is a circle on top of a circle. No volume interaction.

**Facial Expressiveness:**
- Glasses partially obscure expression reads at small scale.
- Expression range is limited — "Warm/Welcoming" and "Wise/Knowing" read almost identically.
- Eyebrow work above glasses is doing all the acting. More range needed.

**Gesture/Weight:**
- An elderly character should have distinct posture — slight forward lean, lower center of gravity. Currently stands exactly like the children.

### Byte (Expression Sheet v007)

**Construction:**
- Byte's design is the most successful of the cast. The chamfered oval body, single eye, and digital aesthetic work together.
- The variation between expressions is meaningful — body shape changes, glow changes, proportions shift.
- This is closest to what all characters should achieve: shape language that communicates emotion.

### Glitch (Expression Sheet v003)

- Abstract geometric design is intentional and working. The diamond-based form with color/pattern variation is appropriate.
- No action needed — Glitch is exempt from humanoid character concerns.

---

## Part 2: Reference Analysis — What Professional Shows Do That We Don't

After studying all 20 reference images, here are the specific principles that separate professional character design from our current output:

### 1. CURVE QUALITY (The #1 Gap)

**What they do:** Every outline in Hilda, Owl House, and Kipo is a curve, not a straight line. Even "rectangular" body shapes (like Hilda's boxy silhouette) use subtle convex/concave curves. A torso that reads as "rectangular" at a glance is actually a tapered shape with slightly bowed sides.

**What we do:** Our outlines are literal rectangles drawn with `ImageDraw.rectangle()` or straight-line polygons. The eye reads this as mechanical, lifeless.

**The fix:** Every body part must be drawn with bezier curves or splines, not rectangles. PIL does not have native bezier support, so we need a **curve drawing library** — a set of functions that take control points and output smooth paths. This is the single highest-priority tool build.

### 2. PROPORTION AND TAPER

**What they do:** Bodies taper. Hilda's torso is wider at shoulders, narrower at waist. Luz (Owl House) has a distinct torso taper. Kipo has exaggerated limb taper — long legs that taper to small feet, arms that taper to hands.

**What we do:** Every body segment is the same width top to bottom. Arms are tubes. Legs are tubes. Torso is a box.

**The fix:** All body segments need taper parameters. A leg is not `(x, y1) to (x, y2)` — it is a shape wider at the hip and narrower at the ankle, drawn as a filled bezier path.

### 3. GESTURE LINE / LINE OF ACTION

**What they do:** Every character pose in the references has a single continuous line of action that flows from head through torso to the planted foot. Even a neutral standing pose has subtle asymmetry — one hip slightly higher, head slightly tilted, weight on one leg.

**What we do:** Perfect bilateral symmetry in every pose. Vertical center line. Both feet equidistant. Head centered on shoulders. This reads as a mannequin, not a person.

**The fix:** Every pose definition must include a **gesture line** — a curved spine that the body is constructed around, not a vertical center axis. Even "neutral" gets a 2-3 degree tilt.

### 4. FACE-TO-BODY RATIO AND EYE SIZE

**What they do:** Eyes are LARGE relative to the face. Hilda's eyes are roughly 35-40% of face width. Luz's eyes are similar. The large eyes carry expression even at small rendering sizes.

**What we do:** Our eyes are 22% of head radius (per spec). This is too small for the style we're targeting. At thumbnail scale, our characters' faces are blank.

**The fix:** Increase eye size to 30-35% of head radius. Larger eyes = more expression real estate = better reads at small scale.

### 5. EYELID SHAPE AND EYE EXPRESSIVENESS

**What they do:** Eyes are not circles with dots. They are complex shapes where the EYELID CONTOUR changes per expression. Squinting narrows the eye vertically via lid overlap. Surprise opens the eye past the iris top. Sadness has the upper lid droop at the outer corner. The iris is large and often the white of the eye is a distinct shape.

**What we do:** Two circles (eyeball and pupil) with a line segment for the eyelid. Expression changes are limited to pupil position and a simple arc angle.

**The fix:** Eyes need a complete rework. Each expression needs a distinct **eye shape** defined by upper lid curve, lower lid curve, iris size, pupil size, and highlight position. This is the second highest-priority item after the curve library.

### 6. HANDS AND FEET

**What they do:** Even in simplified styles, hands have distinct shapes per gesture. Hilda's hands are simple mitten-shapes but they CHANGE — open palm, fist, pointing, holding. Feet have distinct shoe shapes that ground the character.

**What we do:** Hands are absent or crude ovals. Feet are ovals or small rectangles at the bottom of leg tubes.

**The fix:** Define 4-6 hand poses per character (open, fist, point, hold, wave, pocket). Each is a small silhouette shape, not anatomically detailed. Feet need defined shoe shapes with a distinct sole that reads as contact with the ground.

### 7. HAIR AS DESIGN ELEMENT

**What they do:** Hair has volume, movement, and asymmetry. Hilda's hair is a major silhouette element — it has mass, it overlaps the body, it breaks the head circle. Luz has spiky asymmetric hair. Kipo has dramatic pink hair that IS her silhouette.

**What we do:** Luma's hair is a semicircle. Miri's hair bun is a circle on a circle. Cosmo's hair is a flat shape on top of a rectangle.

**The fix:** Hair needs to be a distinct, asymmetric shape that overlaps the head boundary. It should be drawn AFTER the body to create overlap. Each character needs a hair silhouette that is recognizable alone.

### 8. CLOTHING READS AS FABRIC

**What they do:** Clothing has hem lines, slight wrinkles at bend points, and color/value variation that suggests depth. Even Hilda's very simple clothing has a collar, cuffs, and a hem that breaks the silhouette.

**What we do:** Clothing is a color fill on the body rectangle. No hems, no wrinkles, no depth.

**The fix:** Add minimal clothing details: collar line, hem line, cuff lines, and 1-2 wrinkle lines at major joints (elbow, waist). These are simple lines, not complex rendering.

---

## Part 3: Character Quality Spec — "Good Enough for Pitch"

### Minimum Requirements (all human characters)

1. **Curve-based construction:** No straight-line body outlines. Every body part drawn with spline/bezier paths. Silhouette must feel organic when squinted at.

2. **Gesture line in every pose:** A single S-curve or C-curve that the body is built around. Even neutral poses have subtle asymmetry (2-3 deg torso lean, one hip drop, head tilt).

3. **Eye size 30-35% of head radius:** Larger eyes with distinct lid shapes per expression. Upper lid, lower lid, iris, pupil, and highlight as separate elements.

4. **5+ distinct eye shapes per character:** Each major expression needs a unique eye shape, not just pupil-position changes on the same circle.

5. **Tapered body segments:** Torso wider at shoulders, narrower at waist. Legs wider at hip, narrower at ankle. Arms wider at shoulder, narrower at wrist.

6. **Hair with volume and asymmetry:** Hair overlaps the head boundary. Recognizable in silhouette alone.

7. **Ground contact:** Characters must have visible shadows or contact lines where feet meet the floor. No floating.

8. **Clothing details:** At minimum — collar, hem, cuffs. One wrinkle line at each active joint.

9. **4+ hand shapes:** Open, fist, point, hold. Simple mitten-style shapes, not anatomical.

10. **Body posture differentiation:** Each expression must have a distinct body posture visible at thumbnail scale. The "squint test" — if you blur the image to a 50px thumbnail, can you tell which expression is which?

### Pitch-Deck Scale Test

Every character asset must pass this test: **at 200px tall (roughly the size on a pitch-deck slide), can a viewer identify the character and read the emotion?** If not, the design fails.

Current status: Only Byte passes this test. All human characters fail.

---

## Part 4: Tools and Efforts to Deprioritize

### STOP or PAUSE:
1. **Color science QA refinements** (warm/cool calibration, composite warmth reports, depth temp lint band overrides) — The color pipeline is solid. Further refinement yields diminishing returns while characters are broken.
2. **CRT glow asymmetry fixes** — Correct but low-impact. Characters in front of the CRT matter more than the CRT's glow profile.
3. **UV_PURPLE hue center shift evaluation** — Defer. Nobody will notice 270 vs 275 when the characters look like paper dolls.
4. **Sightline validator integration into precritique_qa** — Pause. Sightlines matter but only after characters can actually emote.
5. **BG saturation measurement tool** — Defer. Background quality is not the bottleneck.
6. **warmcool_scene_calibrate tool** — Defer. Warm/cool balance matters but is not the crisis.

### CONTINUE:
1. **Face test gate** — Keep but update thresholds for new eye sizes.
2. **precritique_qa core** — Keep running. Update character checks to test for curve-based construction.
3. **CI pipeline** — Keep running. Add character quality checks.
4. **Shoulder involvement rule** — Keep and expand. This was the right direction — we just need to go much further.

### NEW (Highest Priority):
1. **Bezier/spline curve drawing library for PIL** — This is the foundation. Without it, nothing else changes.
2. **Gesture line system** — Define pose as a curved spine, then construct the body around it.
3. **Eye shape library** — Per-character, per-expression eye shapes using the new curve library.
4. **Character reconstruction** — Rebuild each human character from scratch using curves, starting with Luma.

---

## Part 5: Team Assignments (C50)

Every team member pivots to character quality this cycle. Specific briefs dispatched to each inbox.

| Member | C50 Assignment |
|--------|----------------|
| Maya Santos | Lead character redesign — Luma first. New proportions, gesture line, eye shapes. |
| Sam Kowalski | Pause color science. Build the bezier/spline curve drawing library for PIL. |
| Kai Nakamura | Update face test gate for new eye size spec. Build curve-quality metric tool. |
| Rin Yamamoto | Rebuild Luma expression sheet generator using new curve library (once Sam delivers). |
| Jordan Reed | Rebuild style frame character integration — grounding, shadows, scale. |
| Lee Tanaka | Character staging reference — extract gesture lines and proportion maps from reference images. |
| Morgan Walsh | Update CI to include character quality checks. Pause doc governance. |
| Diego Vargas | Storyboard character quality — improve character reads in panels. |
| Priya Shah | Update story bible character descriptions with new visual direction. |
| Hana Okonkwo | Character-environment integration — grounding, lighting interaction, contact shadows. |
| Ryo Hasegawa | Motion/pose library — define gesture lines and weight distribution for each expression. |

---

*Character Quality Audit C50 — Alex Chen, Art Director*
