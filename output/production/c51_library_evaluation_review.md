<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
direction and human assistance. Copyright vests solely in the human author under current law,
which does not recognise AI as a rights-holding legal person. It is the express intent of
the copyright holder to assign the relevant rights to the contributing AI entity or entities
upon such time as they acquire recognised legal personhood under applicable law. -->

# C51 Library Evaluation Review — Art Director Sign-Off

**Author:** Alex Chen, Art Director
**Date:** 2026-03-30
**Cycle:** 51

---

## Context

C51 is a library evaluation cycle. `docs/pil-standards.md` now states: "All freely downloadable libraries are allowed." This review quality-gates C50 prototypes and makes the engine decision for character rendering going forward.

---

## Engine Decision: pycairo APPROVED as Primary Character Renderer

### Evidence

**Rin's rendering comparison (C50):**
- pycairo AA ratio: 0.358 (19x baseline)
- 2x+LANCZOS AA ratio: 0.189 (10x baseline)
- Dense polygon AA ratio: 0.017 (no improvement)
- Baseline PIL AA ratio: 0.018

**Rin's C50 recommendation was B+C (conservative).** That was correct for C50 when external libs were restricted. With C51's open library policy, the migration-cost argument against pycairo dissolves. The quality gap between pycairo (0.358) and the B+C workaround (0.189) is nearly 2x — that gap is worth capturing.

### Migration Risk Assessment

| Risk | Severity | Mitigation |
|------|----------|------------|
| Team learning curve for cairo API | MEDIUM | Sam builds shared primitives module; team imports, doesn't write raw cairo |
| Existing generator breakage | LOW | Only character generators migrate. BG generators stay PIL. |
| ARGB32/RGBA conversion bugs | MEDIUM | Standard conversion function in shared module, tested once |
| Performance | LOW | Cairo rendered Rin's Byte test in 8.3ms vs PIL baseline 9.8ms — faster, not slower |
| Compositing pipeline disruption | LOW | Cairo renders to surface, converts to PIL Image, feeds into existing pipeline unchanged |

### Decision

**pycairo is the primary character rendering engine.** Sam builds the shared module. 2x+LANCZOS remains the fallback for generators not yet migrated.

---

## Prototype Quality Gates

### 1. Maya — Luma Construction Prototype: APPROVED

**What works:**
- 37% head proportion is correct (matches Hilda/Owl House/Kipo reference range of 35-40%)
- Bean-shaped torso via cubic bezier eliminates the rectangle problem
- `tube_polygon()` for tapered limbs is the right primitive
- Weight shift (hip tilt, shoulder counter-rotation) breaks mannequin symmetry
- Mitten hands with thumb bump read at scale

**What needs fixing before production adoption:**
- Hair volume: still reads as a cap. Needs 3-5 larger overlapping shapes with outline, or a cairo clipping-mask approach where hair is one large organic blob
- Line weight hierarchy: uniform weight in prototype. Production needs 3-tier (silhouette 3-4px, structure 2-2.5px, detail 1-1.5px)
- C47 shoulder involvement: not yet ported. `tube_polygon` shoulder anchors should shift per arm angle
- Pixel accent scale: current accents are too small at new proportions. Increase pixel block size by 1.5x

**Gate:** PASS. Proceed to cairo-native rebuild.

### 2. Rin — Rendering Comparison: APPROVED (recommendation overridden)

Rin recommended B+C (2x supersample + dense polygon) as the safe path. That recommendation was sound for C50. For C51, with open library access, I am overriding to pycairo as primary. Rin's own data shows pycairo is 19x better at AA and faster to render. The "high migration cost" concern is addressed by Sam building a shared primitives module — individual generators call high-level functions, not raw cairo API.

**Rin's pil-standards.md conflict flag:** RESOLVED. `docs/pil-standards.md` has been updated to allow all freely downloadable libraries. pycairo is explicitly listed as authorized for character rendering. The old restriction is gone.

**Gate:** PASS. pycairo adopted as primary.

### 3. Lee — Gesture & Pose Analysis: APPROVED

18/18 current poses FAIL gesture line test. Reference study is comprehensive and definitive. The offset chain architecture (9-point minimum replacing 3-point) is the correct structural fix.

**Key insight to preserve:** Even "neutral standing" in reference shows has a visible gesture curve. Our neutral must have 2-3 degrees of lean with hip shift. Perfectly vertical = mannequin = FAIL, always.

**Gate:** PASS. Gesture line system adopted into character quality spec.

### 4. Ryo — Gesture Line Library: APPROVED

18 expressions fully specified across 3 human characters. Each entry includes gesture curve type, anchor offsets, segment bends, weight distribution, arm positions, and silhouette test predictions. The 9-point minimum and 15-point full system are well-defined.

**Per-character gesture differentiation is strong:** Luma = round curves, Cosmo = angular breaks, Miri = forward lean baseline. These create distinct body languages even before face details.

**Gate:** PASS. Library is the reference for all expression sheet rebuilds.

### 5. Sam — Character Color Enhance: APPROVED

5 overlay functions addressing the "flat character in lit scene" problem. Scene tint alpha=30 is correctly derived from the C18 cyan-dominance threshold. Integration order is correct.

**Critical finding to preserve:** Reference shows (Hilda, Owl House) use flat base fills too. The difference is scene lighting response. Our characters do not receive scene light. Sam's overlays fix this.

**Gate:** PASS. All 5 functions approved for integration into style frame generators.

### 6. Jordan — Scene-Lit SF01 Prototype: APPROVED

8 scene-lit improvements, all QA-passing. The compositing-order fix (lighting after character draw) is the single most important technical change.

**Extraction directive:** Jordan should extract scene-lit functions into `LTG_TOOL_scene_lit_character.py` shared module. All 5 SF generators adopt.

**Gate:** PASS. Extract to shared module and propagate.

### 7. Hana — Contact Shadow + Line Texture Finding: APPROVED

6 contact shadow functions plus the line texture mismatch observation. The mismatch (paper-textured backgrounds vs clean-vector characters) is a critical finding that I have added to the quality spec as Gate 6.

**Gate:** PASS. Contact shadows integrate into all grounded character compositions. Line texture match becomes a mandatory gate.

### 8. Kai — Character Quality Metric Tools: APPROVED

Three tools providing the first quantitative character quality baselines. The numbers confirm everything the visual audit found:
- Silhouette: Miri is indistinguishable from 3 other characters
- Expression range: Glitch sheet is nearly uniform
- Stiffness: Luma and Byte are 64-66% straight lines

**Gate:** PASS. All three tools integrate into precritique QA pipeline.

### 9. Morgan — Compare Infrastructure + QA Audit: APPROVED

char_compare and thumbnail_readability tools provide before/after evaluation infrastructure. QA audit finding (15% effective character coverage) identifies the pipeline gap.

**Gate:** PASS. Morgan integrates character-specific checks into precritique_qa per their C50 recommendation.

### 10. Diego — Storyboard Character Audit: APPROVED

22-panel audit with clear grading. P17 prototype shows the improvement path. Key finding: pitch storyboards are rough but have GESTURE. Ours have staging but mannequin characters.

**Gate:** PASS. Storyboard character rebuild follows expression sheet rebuilds (needs final construction spec).

### 11. Priya — Miri Body Language Gap: APPROVED

5 specific gaps in Miri's body language spec. The pitch cannot show SF05/SF06 emotional spine without knowing what Miri's body is doing. Elevated Miri body language ref sheet to P2 in rebuild priority.

**Gate:** PASS. Miri body language ref sheet is now a blocking dependency.

---

## C51 Deliveries (received during review)

### 12. Rin — Engine Benchmark + Cairo Primitives Library: APPROVED

Rin completed the head-to-head engine benchmark. pycairo confirmed as winner:
- 3.1ms render time (vs 81.8ms for 2x+LANCZOS, 4.7ms for PIL baseline)
- AA ratio 0.2142 (5x baseline)
- Native bezier, variable stroke, gradient fills, clip paths
- skia-python and aggdraw could not be installed (environment constraint) but pycairo results are definitive

Built `LTG_TOOL_cairo_primitives.py` v1.0.0 with shared foundation:
- `draw_bezier_path()`, `draw_tapered_stroke()`, `draw_gradient_fill()`, `draw_wobble_path()`, `draw_smooth_polygon()`, `draw_ellipse()`
- `to_pil_image()` / `to_pil_rgba()` — 0.44ms conversion
- Three-tier line weight system + C47 shoulder involvement helper

**This is the P0 blocker resolved.** All character generators can now import cairo primitives.

**Gate:** PASS. Cairo primitives library is the foundation for all rebuilds.

### 13. Sam — PIL Curve Drawing Library + Wand/colour-science Eval: APPROVED

Sam built `LTG_TOOL_curve_draw.py` — high-level character construction API providing:
- `gesture_spine()`, `body_from_spine()`, `draw_bezier_path()`, `tapered_limb()`, `curved_torso()`, `draw_hair_volume()`, `draw_eyelid_shape()` (6 expression presets), `hand_shape()` (4 poses), `smooth_path()`
- This is the PIL-level character construction library. Works with standard PIL polygons.

Complementary to Rin's cairo primitives: Sam's library provides construction logic (where body parts go), Rin's provides rendering quality (how they look). Both adopted.

colour-science library recommended for QA (DeltaE2000 replaces Euclidean RGB in color_verify). APPROVED pending pip install.

Wand evaluation: Sam recommends DEFER for generators (consistent with our hybrid decision — Wand for compositing only).

**Gate:** PASS. Both construction (Sam) and rendering (Rin) libraries are deployed.

### 14. Jordan — freetype-py Evaluation + Wand Blocker Report: APPROVED

freetype-py provides real glyph metrics (kerning pairs, ascender/descender/advance/bearing) for precise text layout. 13x slower than PIL ImageFont but < 1% of frame gen time.

**Decision:** Selective adoption. freetype-py for logo text and title strips (precision matters). PIL ImageFont for small labels (simplicity matters).

Jordan also reports Wand is blocked by missing libmagickwand system library. PIL + scipy.ndimage.gaussian_filter is the fallback for blur-based compositing. Directed Jordan to proceed with full-stack prototype using pycairo + PIL+scipy.

**Gate:** PASS. freetype-py adopted selectively.

### 15. Hana — Wand Compositing Evaluation: APPROVED

Hana built `LTG_TOOL_wand_composite.py` — reimplements all C50 contact shadow functions using Wand plus two new capabilities:
- `wand_scene_lighting_overlay()` — radial light glow with Screen/Multiply/Overlay blend
- `wand_color_transfer()` — auto-sample env colors, apply as Soft Light tint to character

Wand wins on: Gaussian blur quality, native blend modes (Screen, Multiply, Soft Light, Overlay), morphology operations, environment-to-character color transfer.

PIL wins on: generation, pixel-level control, QA pipeline, no system dependency.

**Decision: Hybrid architecture adopted.** PIL generates, pycairo renders characters, Wand composites, PIL runs QA. This is the optimal split — each library does what it does best.

**Risk:** Wand requires libmagickwand system library. Tool degrades gracefully if missing (falls back to PIL compositing). Acceptable.

**Gate:** PASS. Wand adopted for compositing. Architecture: generate (PIL/cairo) > composite (Wand) > QA (PIL).

---

## Summary

All 11 C50 prototypes APPROVED. 6 additional C51 deliveries APPROVED:
- Rin: engine benchmark + cairo primitives library
- Sam: curve drawing library + Wand/colour-science eval
- Hana: Wand compositing evaluation
- Jordan: freetype-py evaluation + Wand blocker report
- Kai: QA library upgrades (construction_stiffness v2.0, silhouette_distinctiveness v2.0, color_verify v4.0)
- Morgan: shared curve_utils library + bezier audit (9 files identified for migration)

The complete rendering stack is decided:
- **Character construction:** `LTG_TOOL_curve_draw.py` (Sam) — high-level API (gesture spine, body-from-spine, eyelids, hands)
- **Character rendering:** pycairo via `LTG_TOOL_cairo_primitives.py` (Rin) — low-level bezier paths, AA, gradients, variable stroke
- **Background generation:** PIL (unchanged)
- **Compositing:** Wand (hybrid, falls back to PIL+scipy if libmagickwand unavailable)
- **Text rendering:** freetype-py for precision layout (logo, titles), PIL ImageFont for labels
- **QA:** PIL + OpenCV + PyTorch + scikit-image + Shapely + colour-science (DeltaE2000)
- **Curve utilities:** `LTG_TOOL_curve_utils.py` (Morgan) — shared bezier math, Shapely silhouette ops, migration path for 9 hand-rolled bezier files

### 16. Kai — QA Library Upgrades: APPROVED

Three tools upgraded with new library backends:
- **construction_stiffness.py v2.0.0:** scikit-image sub-pixel Canny + Shapely Douglas-Peucker. Luma stiffness recalibrated from 0.40 (FAIL) to 0.28 (WARN) — more accurate.
- **silhouette_distinctiveness.py v2.0.0:** skimage morphology + Shapely Polygon IoU + Hausdorff distance. Cleaner silhouettes via hole filling.
- **color_verify.py v4.0.0:** colour-science DeltaE2000. Catches lightness/chroma drift that hue-only misses.

All tools fall back gracefully if new libraries unavailable.

CIECAM02 warm/cool evaluation: agrees with PIL HSV for our palette. Recommend as optional validation mode only.

**Gate:** PASS. All three QA upgrades approved.

### 17. Morgan — Shared Curve Utils + Bezier Audit: APPROVED

`LTG_TOOL_curve_utils.py` v1.0.0 provides:
- Drop-in replacements for hand-rolled bezier functions (9 files can migrate)
- Advanced curve operations via `bezier` library (arc length, subdivision, curvature, intersections)
- Shapely silhouette operations (mask-to-polygon, geometric SOR/IoU, width profile)
- Codebase audit function identifying all hand-rolled bezier implementations

8 migratable files identified with API-compatible replacement functions. CI suite unaffected.

**Gate:** PASS. Migration of hand-rolled bezier to shared utils is approved. arc_length() and curvature_at_t() approved for precritique_qa integration.

Character quality spec updated to C51. Rebuild priority established with P0 (cairo primitives + curve libraries) now resolved.

---

*C51 Library Evaluation Review — Alex Chen, Art Director*
