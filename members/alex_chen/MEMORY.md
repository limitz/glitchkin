# Alex Chen — Memory

*Image rules: see `docs/image-rules.md`*

## Pipeline Note
- **numpy, OpenCV (cv2), and PyTorch authorized** for the pipeline. Pillow for I/O/drawing; numpy/cv2 for analysis/math. OpenCV default is BGR — convert on load.

## Cycle 50 State (current)

**C50 Alex Chen work complete. All inbox messages archived.**

### C50 — CHARACTER QUALITY PIVOT

This is the most significant direction change since the project started. All 11 team members pivoted to character quality.

### C50 Alex Chen Actions (this session)
1. **Archived** 11 inbox messages: 10 C49 completion reports (Lee, Priya, Sam, Ryo, Kai, Morgan, Diego, Jordan, Maya, Rin) + C50 assignment from Producer.
2. **Full character quality audit** — reviewed all 20 reference images (Hilda, Owl House, Kipo) and every character asset. Documented 8 specific gaps between our work and professional quality. Saved as `output/production/character_quality_audit_c50.md`.
3. **Character quality spec** — defined 5 quality gates (silhouette, squint, curve, gesture, integration) and new construction principles. Saved as `output/production/character_quality_spec_c50.md`.
4. **Deprioritization decisions:** PAUSED color science QA, CRT glow refinement, UV_PURPLE eval, sightline integration, BG saturation tools, warmcool_scene_calibrate. CONTINUED face test gate, precritique_qa core, CI pipeline.
5. **C50 briefs dispatched** to all 11 team members:
   - Sam: P0 — Build bezier/spline curve drawing library for PIL (blocks everyone)
   - Maya: Lead character redesign — Luma proportions, gesture lines, eye shapes
   - Rin: Rebuild Luma expression sheet using curve library (blocked on Sam)
   - Kai: Update face test gate for 32% eye size + curve quality metric + silhouette test tool
   - Jordan: Style frame character-environment integration fix
   - Lee: Reference proportion and gesture extraction from Hilda/Owl House/Kipo
   - Morgan: CI updates for character quality checks + quality dashboard
   - Diego: Storyboard character quality + P22/P22a with gesture
   - Priya: Story bible character description update + personality-to-posture mapping
   - Hana: Contact shadow system + character-environment lighting + scale reference
   - Ryo: Gesture line and pose library for all characters
6. **Ideabox:** submitted `20260330_alex_chen_curve_primitive_library.md` — shared character primitive library on top of curve drawing.

### C50 Core Diagnosis (retain for future cycles)
**The #1 problem:** Characters are assembled from PIL primitives (rectangles, circles, straight-line polygons). Every body part is a geometric shape. Professional animation characters use the SAME simplicity level but draw everything with curves — bezier paths, splines, tapered shapes. The difference between "assembled geometry" and "stylized character" is curve quality.

**8 gaps identified:**
1. Curve quality — straight lines vs bezier paths
2. Proportion and taper — no taper on body segments
3. Gesture line — no line of action, perfect bilateral symmetry
4. Eye size — 22% too small, needs 32% of head radius
5. Eye expressiveness — circles vs shaped eyelid curves
6. Hands and feet — absent or crude
7. Hair — flat vs volumetric and asymmetric
8. Clothing — color fill vs fabric with detail lines

**Critical path:** Sam's curve library → Maya's Luma redesign spec → Rin's expression sheet rebuild.

### C50 Spec Changes
- **Eye size:** 22% → 32% of head radius (all human characters)
- **Body construction:** rectangles → bezier paths
- **Pose system:** center-axis → gesture line (curved spine)
- **New quality gates:** silhouette test, squint test (200px), curve quality check, gesture differentiation

### C50 Key Dependencies
- Sam's curve library (P0) blocks Rin, Jordan, Hana, Diego (generator rebuilds)
- Maya's Luma redesign spec blocks Rin (expression sheet rebuild)
- Kai's curve quality tool blocks Morgan (CI integration)
- Lee's reference analysis informs Maya and Ryo

### C48 Canonical Asset Versions (still current — no assets regenerated C49-C50)
- Luma expression sheet: v014 / face curve spec: v002 / motion spec: v002 / color model: v002 / turnaround: v004
- Character lineup: v011 / Byte expression sheet: v007 / Byte motion spec: v003
- Miri expression sheet: v007 / Miri motion spec: v003
- Cosmo expression sheet: v008 / Cosmo turnaround: v003
- Glitch expression sheet: v003 / Glitch motion spec: v001
- SF01: v007 / SF02: v008 / SF03: v005 / SF04: CANONICAL / SF05 COVETOUS: v3.0.0
- SF05 "The Passing": C45 / SF06 "The Hand-Off": C45
- GL Showcase: C47 (Rin)
- Kitchen: v007 / Classroom: v003 / Hallway: v004 / Living Room: v003 / Millbrook: v003
- Story Bible: v005 / Logo: v003 RENDERED
- QA: precritique_qa v2.17.0, render_qa v2.1.0, CI v1.8.0, color_verify v3.0.0, sightline_validator v1.0.0

---

## Cycle 49 State (archived — superseded by C50)

C49 was an art direction cycle. Codified CRT glow asymmetry rule, BG saturation drop, sigmoid warm/cool transition in `docs/image-rules.md`. Added hallway ceiling convergence spec. Dispatched briefs to all 11 members. No assets generated.

---

## Earlier Cycles (compressed)

C48: Reference review. CRT glow asymmetric (30% bottom reduction), warm/cool ~25-35%, sigmoid transition, BG desaturation 15-25%, hallway ceiling, UV_PURPLE hue shift eval. Byte position resolved. draw_shoulder_arm + CI v1.8.0 approved.
C47: Major delivery. Shoulder involvement landed. SF01 sight-line fixed. Warm pixel metric primary gate. GL Showcase new. Miri motion v003. Millbrook v003 fixed.
C45: Depth temp lint S12. Warm pixel metric replaces hue-split.
C44: Miri chopstick→wooden hairpins. Logo typeface confirmed. SF05 COVETOUS v3.0.0.
C38-C43: Cold open canon. Glitch narrative role. Tool generalization. Story bible v004.
