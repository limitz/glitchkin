<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
direction and human assistance. Copyright vests solely in the human author under current law,
which does not recognise AI as a rights-holding legal person. It is the express intent of
the copyright holder to assign the relevant rights to the contributing AI entity or entities
upon such time as they acquire recognised legal personhood under applicable law. -->

# Character Quality Spec — C51 (Library Evaluation Edition)

**Prepared by:** Alex Chen, Art Director
**Date:** 2026-03-30
**Supersedes:** `character_quality_spec_c50.md`

---

## What Changed in C51

C51 opens the dependency list: **all freely downloadable libraries are now allowed** (see `docs/pil-standards.md`). This changes what is achievable. C50 identified 8 quality gaps and proposed PIL-only workarounds. C51 re-evaluates each gap with full library access and defines the production rendering stack.

### C50 Prototype Summary (Quality Gates)

| Prototype | Author | Quality Gate | Verdict | Notes |
|-----------|--------|-------------|---------|-------|
| Luma construction (CURIOUS) | Maya | APPROVED | Old-to-new comparison is stark. Proportions, gesture, organic shapes all improved. Hair needs more volume. Line weight hierarchy missing. |
| Rendering comparison (4 methods) | Rin | APPROVED with caveat | B+C (2x supersample + dense polygon) is the safe path. pycairo is technically superior (19x AA ratio) but high migration cost. With C51 lib freedom, pycairo is now viable as the primary engine. |
| Gesture line library (18 poses) | Ryo | APPROVED | Comprehensive. Offset chain architecture is correct. 9-point minimum confirmed. |
| Gesture/pose reference analysis | Lee | APPROVED | 18/18 current poses FAIL gesture test. Reference study is definitive. |
| Character color enhance tool | Sam | APPROVED | 5 overlay functions. Scene tint alpha=30 is safe. Integration order: scene_tint > form_shadow > skin_warmth. |
| Scene-lit SF01 prototype | Jordan | APPROVED | 8 improvements, all QA-passing. Ready for extraction to shared module. |
| Contact shadow system | Hana | APPROVED | 6 functions. Line texture mismatch observation is critical — added to this spec. |
| Silhouette/expression/stiffness tools | Kai | APPROVED | Baseline data confirms all gaps quantitatively. Miri silhouette DS=0.02 is the most urgent problem. |
| Char compare + thumbnail readability | Morgan | APPROVED | Before/after comparison infrastructure ready. Pipeline audit shows 15% effective character coverage — needs doubling. |
| Storyboard character audit | Diego | APPROVED | 8/22 panels FAIL. Gesture is the root cause. P17 prototype shows path forward. |
| Miri body language gap analysis | Priya | APPROVED | 5 specific gaps. Miri body-language ref sheet is now a dependency for SF05/SF06. |

**All 11 prototypes APPROVED for C51 integration.**

---

## Production Rendering Stack (C51 Decision)

### Primary Drawing Engine: pycairo

**Decision: pycairo is the primary character rendering engine effective C51.**

Rationale:
- 19x anti-aliasing improvement over baseline PIL (Rin's data: AA ratio 0.358 vs 0.018)
- Native cubic bezier curves (no polygon approximation needed)
- Native variable line width (float-precision `set_line_width`)
- Native radial/linear gradients (no layered ellipse hacks)
- Sub-pixel rendering matches broadcast 2D animation quality
- With all libraries now allowed, the migration-cost argument against pycairo is moot
- pycairo is open source (LGPL), freely downloadable, and widely packaged

**Migration path:**
1. **DONE:** Rin built `LTG_TOOL_cairo_primitives.py` v1.0.0 — shared cairo rendering primitives (bezier paths, tapered strokes, gradient fills, variable-width strokes, wobble paths, cairo-to-PIL conversion). Sam built `LTG_TOOL_curve_draw.py` — high-level character construction API (gesture spine, body-from-spine, eyelid shapes, hand shapes, tapered limbs, curved torso). Both libraries are deployed and importable.
2. New character generators import from both: `curve_draw` for construction logic, `cairo_primitives` for rendering quality. Or use `curve_draw` alone for PIL-based generators that don't need cairo AA yet.
3. Cairo surfaces convert to PIL Images for compositing with existing BG pipeline
4. Existing PIL compositing, glow, overlay, and texture passes remain unchanged
5. Background generators stay PIL-based (no migration needed — backgrounds are not the problem)

**Fallback:** 2x supersample + LANCZOS remains the fallback for any generator not yet migrated to cairo. This is Rin's B+C approach and provides ~50% of cairo's quality improvement with zero code changes.

### Compositing Pipeline: Wand (hybrid — NEW C51)

**Decision: Wand (ImageMagick Python bindings) adopted for character-environment compositing.**

Rationale (Hana's C51 evaluation):
- Native blend modes (Screen, Multiply, Soft Light, Overlay) replace verbose numpy Porter-Duff workarounds
- Screen blend for additive light (bounce, window glow, lamp spill) is physically correct
- Soft Light blend enables environment-to-character color transfer (the #1 compositing gap from C50)
- Native Gaussian blur with configurable sigma replaces PIL's fixed-kernel approximation
- Native morphology operations replace N-iteration MinFilter loops

**Architecture: PIL generates, pycairo renders characters, Wand composites, PIL runs QA.**

```
Environment Generator (PIL) → background PNG
Character Generator (pycairo → PIL) → character PNG + mask
Wand Compositor:
  - Contact shadows (gaussian blur, proper kernel)
  - Scene lighting overlays (Screen blend)
  - Environment-to-character color transfer (Soft Light blend)
  - Bounce light (Screen blend)
  - Edge tint (native morphology)
PIL QA → final validation
```

Cairo-to-PIL conversion uses Rin's `to_pil_rgba()` from `LTG_TOOL_cairo_primitives.py` (0.44ms overhead). PIL-to-Wand and Wand-to-PIL conversions use standard file I/O or numpy buffer sharing.

**Fallback:** If libmagickwand is unavailable, compositing falls back to PIL + numpy Porter-Duff (existing C50 approach). Hana's tool degrades gracefully.

### Post-Draw Overlays: Wand + PIL + numpy

Sam's character_color_enhance overlays (scene_tint, form_shadow, skin_warmth, hair_absorption, scene_outline) can use either Wand blend modes or PIL/numpy post-processing. Wand is preferred for blend-mode operations (Screen, Soft Light). PIL/numpy remains for pixel-level manipulation.

### QA Tools: PIL + OpenCV + PyTorch (unchanged)

Kai's silhouette, expression range, and stiffness tools plus Morgan's compare/thumbnail tools remain PIL/OpenCV-based.

---

## Quality Gates (Updated from C50)

Every character asset must pass ALL 7 gates before submission. Gates 1-5 carry forward from C50. Gates 6-7 are new for C51.

### Gate 1: Silhouette Test
Fill the character solid black. Is it recognizable? Can you tell which character it is? Can you tell the emotion?

**Metric:** Silhouette Distinctiveness Score (DS) >= 0.15 for every character pair. Tool: `LTG_TOOL_silhouette_distinctiveness.py`.

**C50 baseline failures:** Luma/Miri DS=0.02, Cosmo/Miri DS=0.04, Miri/Byte DS=0.02. Miri's silhouette must become radically different.

**Miri silhouette fix spec:**
- Permanent forward lean (15-20 degrees from vertical) — elderly posture, distinct from children
- Wider at hips than shoulders (inverted from Luma/Cosmo)
- Cardigan extends below hip line — creates a distinct hem silhouette
- Head-forward-of-shoulders posture (chin juts slightly)
- Walking stick or tea cup as silhouette-breaking prop in at least 2/6 expression poses
- Target: DS >= 0.20 vs every other character

### Gate 2: Squint Test (200px Thumbnail)
Scale the character to 200px tall. Can you identify the character and read the emotion?

**Metric:** Thumbnail Readability Score per-scale PASS at 128px and 64px. Tool: `LTG_TOOL_thumbnail_readability.py`.

**C51 improvement path:** Larger heads (37% of body) and larger eyes (32% of head radius) directly improve thumbnail readability. Cairo's anti-aliased curves will retain shape information at smaller scales better than aliased PIL polygons.

### Gate 3: Curve Quality
Zoom to 100% on any body part outline. Is it a smooth curve?

**Metric:** Construction Stiffness Score < 0.25 (PASS) or < 0.30 (WARN). Straight-line percentage < 40%. Tool: `LTG_TOOL_construction_stiffness.py`.

**C51 improvement path:** Cairo native bezier curves eliminate the polygon-approximation problem entirely. Every organic form is drawn as a true bezier path. Expected straight-line percentage with cairo: < 15% for human characters (only intentionally geometric elements like pixel accents and glasses frames).

**C50 baseline failures:** Luma 64% straight (FAIL), Byte 66% straight (FAIL), Cosmo 48% (WARN), Miri 47% (WARN).

### Gate 4: Gesture Read
Cover the character's face. Can you still tell the emotion from body posture alone?

**Metric:** Ryo's gesture line library defines per-expression gesture curves. Each pose must have a visibly different gesture line. Silhouette RPD (Radial Profile Difference) between expression pairs >= threshold per Lee's spec.

**C51 implementation:** Every character generator starts with a gesture line (bezier curve from head to weight-bearing foot). Body is constructed AROUND this line, not on a vertical axis. The 9-point minimum anchor system (head, neck, shoulder L/R, hip center, hip L/R, weight foot, free foot) replaces the 3-point system (cx, ground_y, head_top).

**Per-character gesture signatures (from Lee + Ryo):**
- **Luma:** Round S-curves and C-curves. Weight shifts are gentle arcs. Energy direction matches curiosity/determination.
- **Cosmo:** Angular joint breaks. Elbows and knees create zigzag gesture lines. Stiff, awkward energy.
- **Miri:** Permanent forward lean baseline. Gentle curves layered on the lean. Large head tilts. Left-hip weight habit. Calm, grounded energy.
- **Byte:** Tilt-counterpose (no ground contact). Float angle communicates mood. Digital snap between poses.
- **Glitch:** Exempt from human gesture rules. Shape-shifts between expressions.

### Gate 5: Integration
Place the character in an environment. Does it look like they belong in that space?

**Metric:** Jordan's integration audit grades (target: B or above per style frame). Requires:
1. Contact shadow at character base (Hana's `LTG_TOOL_contact_shadow.py`)
2. Scene-tinted character highlights (Sam's `apply_scene_tint()`)
3. Form-following shadows (Sam's `apply_form_shadow()`)
4. Compositing order: background > lighting overlay > character draw > character lighting > contact shadow > final overlay
5. Bounce light from ground surface onto character lower body

### Gate 6: Line Texture Consistency (NEW — C51)
Characters and backgrounds must have matching line texture. No "vector on paper" mismatch.

**Source:** Hana's C50 line texture mismatch observation. Backgrounds have paper-grain texture from `paper_texture()` final pass. Characters have perfectly clean uniform lines. This creates a visual language split that reads as "pasted on" even when lighting and shadows are correct.

**Implementation (two approaches, use both):**
1. **Variable-width stroke on character outlines.** Cairo's native variable line width makes this trivial: modulate `set_line_width()` along the path with +/- 0.5px random variation on a 2-3px base. Seeded RNG for reproducibility. This gives organic hand-drawn line quality.
2. **Subtle paper texture pass on character layer.** After character is drawn but before compositing onto background, apply a reduced-opacity paper grain pass (alpha 15-25%, using same grain source as backgrounds). This unifies the texture language.

**Why both:** Variable stroke addresses the line itself. Paper texture addresses the fill areas. Together they integrate the character into the same visual medium as the background.

### Gate 7: Expression Sheet Body Variation (NEW — C51)
Every expression on an expression sheet must have a visibly different BODY posture, not just a different face.

**Source:** Lee's C50 gesture analysis (18/18 poses FAIL — all straight vertical gesture lines). The expression sheet reference image shows professional sheets where every cell has distinct body language.

**Metric:** No two expressions on a sheet may share the same gesture line shape. Minimum body variation between any two expressions:
- Hip angle difference >= 5 degrees OR
- Shoulder angle difference >= 5 degrees OR
- Gesture line curvature category change (C-curve vs S-curve vs diagonal vs vertical snap)
- Hands must be in different positions in at least 4/6 expressions

---

## Construction Principles (Updated for Cairo)

### Body Construction: Cairo Bezier Paths

Every organic body part is a closed cairo path built from `curve_to()` (cubic bezier) calls. No `rectangle()` or `arc()` for organic forms.

**Torso:** Bean-shaped closed path. 4+ cubic bezier segments. Shoulder width > waist width (taper). Slight asymmetry in every pose (gesture line determines which side compresses).

**Limbs:** Tapered tube shapes via paired bezier curves (inner edge + outer edge). Wider at shoulder/hip joint, narrower at elbow/knee, slightly wider again at wrist/ankle. Maya's `tube_polygon()` concept translates directly to cairo `curve_to()` pairs.

**Head:** Circle-based with chin taper via bezier. Not a perfect `arc()` — use `curve_to()` to create an ellipse-with-chin. Exception: Cosmo keeps rectangular head as design signature, but edges are curved (rounded-rectangle via bezier, not `rectangle()`).

### Line Weight Hierarchy (3-tier, cairo native)

Cairo's float-precision `set_line_width()` enables proper line weight hierarchy:

| Tier | Width (at 2x render) | Width (at output) | Use |
|------|---------------------|-------------------|-----|
| Silhouette | 6-8px | 3-4px | Outer character boundary |
| Structure | 4-5px | 2-2.5px | Major body part separations (arm/torso, leg/hip) |
| Detail | 2-3px | 1-1.5px | Eyes, mouth, clothing folds, fingers |

Apply variable-width modulation (+/- 0.5px at output scale) on all tiers for organic feel.

### Eye System (cairo bezier eyelids)

Each eye is composed of cairo paths:
1. **Upper eyelid:** Single cubic bezier defining eye top. Control points shift per expression.
2. **Lower eyelid:** Single cubic bezier defining eye bottom. Pushed up for happy squint, dropped for surprise.
3. **Iris:** Large filled circle (65-75% of eye opening height). Cairo `arc()` is fine here (geometric is correct for iris).
4. **Pupil:** Smaller circle within iris.
5. **Dual highlights:** Primary catch light (upper, scene-light-colored) + secondary catch light (lower, smaller, complementary). Cairo radial gradient for soft-edge highlights.

**Eye size:** 32% of head radius (up from 22%). Confirmed in C50 spec and all reference analysis.

**Eyelid expression table:**

| Expression | Upper Lid | Lower Lid | Iris Visible | Pupil Size |
|------------|-----------|-----------|-------------|------------|
| Neutral | Gentle arc | Gentle arc | 80% | Normal |
| Happy | Slightly lowered | Pushed up (squint) | 60% | Normal |
| Sad | Outer corners droop | Straight/slight rise | 70% | Normal |
| Angry | Inner corners drop (V toward nose) | Tenses up | 75% | Contracted |
| Surprised | Rises above iris top | Drops below iris bottom | 100%+ white shows | Dilated |
| Worried | Slight inner-corner rise | Slight outer droop | 75% | Normal |
| Determined | Slight lower overall | Slight rise | 70% | Contracted |

### Gesture Line System (9-point minimum)

Every pose starts with a gesture line — a cubic bezier from head to weight-bearing foot. Body parts attach to anchor points sampled along this curve.

**Anchor points (minimum 9):**
1. Head center (top of gesture line)
2. Neck base
3. Shoulder left
4. Shoulder right
5. Hip center
6. Hip left
7. Hip right
8. Weight-bearing foot
9. Free foot

**Full system (15 points, for detailed poses):**
Add: 10. Elbow left, 11. Elbow right, 12. Knee left, 13. Knee right, 14. Hand left, 15. Hand right

The gesture line curve determines anchor positions. Hip tilt derives from gesture line curvature at the hip segment. Shoulder counter-rotation derives from the opposite direction. This is Ryo's offset chain architecture.

### Proportion Targets (Unchanged from C50)

| Character | Head Size | Body Height (HU) | Shoulder Width | Waist Width | Key Proportion |
|-----------|-----------|-------------------|----------------|-------------|----------------|
| Luma | 1.0 HU | 4.5 HU total | 1.6 HU | 1.1 HU | Hair mass adds 0.3 HU above head circle |
| Cosmo | 1.0 HU | 4.0 HU total | 1.5 HU | 1.2 HU | Wider, boxier build. Head taller than wide. |
| Miri | 0.9 HU | 5.0 HU total | 1.3 HU | 1.1 HU | Shorter head, compact, permanent forward lean |

### Hand Shapes (4 minimum per character, unchanged)

1. **Rest** — relaxed at side, fingers together, slight curve
2. **Fist** — clenched, determination/frustration
3. **Open** — palm forward, surprise/welcoming
4. **Point/Hold** — index extended or wrapped around object

Mitten shapes at our scale. 3-4 cairo control points. Must CHANGE between poses.

### Miri-Specific Body Language Spec (NEW — C51)

Priya's gap analysis elevated Miri body language to a blocking dependency for SF05/SF06.

**Default posture (KNOWING CALM):**
- Standing: 15-degree forward lean, weight on left hip, hands clasped or holding tea cup
- Seated: upright but forward-leaning, hands in lap or around cup, feet together

**Tea cup positions (5, mapped to emotion):**
1. Held in both hands at chest level = comfort / contemplation
2. Extended toward another person = offering / connection
3. Resting on knee (seated) = settled / at ease
4. Lowered to side, one hand = concern / distraction
5. Set down on surface = serious moment / full attention on other person

**THE LOOK ("I already know" expression):**
- Head tilted slightly left
- Eyes half-lidded, slight upward gaze
- One eyebrow barely raised
- Mouth: gentle closed smile, asymmetric (left corner higher)
- Body: perfectly still, weight settled, tea cup held at chest (position 1)
- The stillness IS the expression — Miri's body language communicates through calm, not movement

**THE HANDOFF (SF06):**
- Full-body spec needed: arm extended holding object, weight shifted forward onto front foot
- Other hand at side (not symmetrically extended)
- Head tilted slightly down (looking at recipient, not at object)
- Cardigan drapes asymmetrically due to arm extension
- Gesture line: forward-leaning diagonal, head-to-front-foot

**Cardigan shape by emotion:**
- Neutral: symmetric drape, hem at mid-thigh
- Warm/welcoming: open front, arms visible
- Concerned: pulled closed, hands clasping front edges
- Active (reaching, handing): drapes back on extended-arm side, bunches on other side

---

## Scene Lighting Integration Spec (NEW — C51)

From Sam and Jordan's C50 work. Every character in a scene receives:

1. **Scene tint** — `apply_scene_tint()` with alpha <= 30. Light source color tints character highlights on the facing side.
2. **Form shadows** — `apply_form_shadow()`. Curved anatomical shadows (torso-diagonal, limb-underside, inseam), not geometric left-half rectangles.
3. **Skin warmth** — `apply_skin_warmth()`. Warm-cheek / cool-edge gradient on all exposed skin. Blush zones on cheekbones.
4. **Hair absorption** — `apply_hair_absorption()`. Dark hair picks up 2x scene tint. Light hair picks up 1x.
5. **Scene-derived outline** — `derive_scene_outline()`. Character outline color influenced by scene palette rather than universal dark brown.
6. **Contact shadow** — Hana's `LTG_TOOL_contact_shadow.py`. Every grounded character gets a contact shadow band.
7. **Bounce light** — Lower character body picks up surface color influence. Couch = warm bounce. Street = cool bounce. Glitch platform = cyan bounce.

**Compositing order (CRITICAL — Jordan's finding):**
```
1. Draw background (all layers)
2. Apply background lighting overlay
3. Draw character (cairo -> PIL)
4. Apply character scene lighting (scene_tint, form_shadow, skin_warmth, hair_absorption)
5. Apply variable-width outline with scene-derived color
6. Apply contact shadow
7. Apply bounce light
8. Apply paper texture pass on character layer
9. Composite character onto lit background
10. Final passes (scanlines, vignette, etc.)
```

Steps 3-8 happen on the character layer BEFORE compositing onto the background. This is the fix for Jordan's "lighting overlay drawn before character" problem.

---

## Tier 2 Character Rebuild Priority (C51 Decision)

With the rendering stack decided, character rebuilds proceed in this order:

| Priority | Character | Asset | Rationale |
|----------|-----------|-------|-----------|
| P0 | (engine) | `LTG_TOOL_cairo_draw.py` | Shared cairo drawing primitives. Blocks all rebuilds. |
| P1 | Luma | Expression sheet | Protagonist. Most screen time. Maya's prototype proves the path. |
| P2 | Miri | Body language ref sheet | SF05/SF06 dependency. Priya's gap analysis. Silhouette emergency (DS=0.02). |
| P3 | Luma | Turnaround | Needed after expression sheet to validate all angles. |
| P4 | Byte | Expression sheet | Second-most-important character. Currently FAIL on stiffness despite being the best-designed. |
| P5 | Cosmo | Expression sheet | Third rebuild. Turnaround can follow quickly since Cosmo's geometry is simpler. |
| P6 | Miri | Expression sheet | After body language ref establishes her visual vocabulary. |
| P7 | Glitch | Expression sheet | Lowest priority — already PASSes curve quality, needs bolder expression range only. |
| P8 | All | Character lineup | After all individual sheets are rebuilt. |

**Why Miri body language (P2) before Luma turnaround (P3):** Miri's silhouette is the most urgent failure (DS=0.02 against 3 characters). The body language reference sheet establishes her distinct proportions and posture, which then flow into her expression sheet and all scene appearances. Without this, SF05 and SF06 cannot be rendered correctly.

---

## What Cairo Unlocks That PIL Could Not

| Capability | PIL Workaround (C50) | Cairo Native (C51) | Quality Delta |
|-----------|---------------------|-------------------|---------------|
| Smooth curves | 64-point polygon approximation | `curve_to()` cubic bezier | True curves vs polygon facets |
| Anti-aliased edges | 2x render + LANCZOS downscale | Native sub-pixel AA | 19x AA ratio improvement (Rin's data) |
| Variable line width | Not possible (uniform `line()` width) | `set_line_width()` accepts float, changes along path | Enables line weight hierarchy + organic wobble |
| Gradient fills | Layered semi-transparent ellipses | Native `LinearGradient` / `RadialGradient` | Analytical gradients, no banding |
| Tapered strokes | Filled polygon pairs (tube_polygon) | Varying `set_line_width()` along `curve_to()` path | Cleaner, fewer artifacts at joints |
| Path operations | Manual polygon clipping | `clip()`, `mask()`, path boolean ops | Clean hair-over-face, clothing-over-body |

---

## Metrics Summary

| Gate | Tool | PASS Threshold | Current Worst | Target |
|------|------|---------------|---------------|--------|
| 1. Silhouette | silhouette_distinctiveness | DS >= 0.15 | Luma/Miri 0.02 | All pairs >= 0.20 |
| 2. Squint | thumbnail_readability | PASS at 128px + 64px | All FAIL | All PASS at 128px |
| 3. Curves | construction_stiffness | Straight < 40%, Score < 0.25 | Byte 66% straight | All < 20% straight |
| 4. Gesture | gesture line audit (manual + RPD) | Distinct gesture per expression | 18/18 FAIL | 18/18 PASS |
| 5. Integration | integration audit grade | B or above | D average | B average |
| 6. Line texture | visual inspection + stiffness secondary | Variable stroke present, paper texture match | Not measured | All character generators include both |
| 7. Body variation | expression sheet body audit | Distinct body per expression | 0% body variation | 100% body variation |

---

*Character Quality Spec C51 — Alex Chen, Art Director*
