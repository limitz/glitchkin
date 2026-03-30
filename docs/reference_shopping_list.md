# Visual Reference Shopping List

Reference assets for analysis and art direction on *Luma & the Glitchkin*.
**Copyright rule:** All references are for measurable analysis only — palette extraction, geometry measurement, lighting ratios, composition structure. No copying of style, character design, or artwork. Prefer Creative Commons / public domain sources.

---

## CRT & Retro Display Aesthetics

- Photograph of illuminated CRT television screen in a dark room — measure phosphor glow radius, FWHM of bloom, warm/cool cast of ambient spill onto surrounding surfaces. Feed into `LTG_TOOL_bg_grandma_kitchen.py` glow calibration.
- Close-up photograph of CRT scanlines at various brightness levels — extract scanline pitch, inter-line darkness ratio, and horizontal smear profile. Use to tune the Glitch Layer's pixel-grid rendering in `LTG_TOOL_character_face_test.py`.
- Photograph of CRT static / snow — measure spatial frequency distribution of noise. Use as reference when generating UV_PURPLE corruption texture in Glitch Layer scenes.
- Photograph of CRT phosphor afterglow (NTSC green P22 phosphor decay) — measure hue shift from active white to decay trail. Informs CORRUPT_AMBER contamination hue path through CRT glass.
- Photograph of CRT cabinet housing in a domestic setting — extract material color, wood grain tone, and plastic off-white values for Miri's set-prop palette reference.

---

## Warm Interior Lighting (Real World — Kitchen & Living Room)

- Photograph of a kitchen at pre-dawn, lit only by a single incandescent or halogen lamp — measure warm/cool pixel ratio, shadow angle, practical lamp falloff curve. Baseline for SF05 "The Passing" warm/cool target (current: 16.7).
- Photograph of a kitchen counter with a ceramic mug of tea steaming — extract steam rendering reference: opacity gradient, motion blur direction, colour temperature of transmitted light through steam.
- Photograph of a domestic living room with a single table lamp on, window dark — measure warm zone radius from practical source. Use to calibrate `REAL_INTERIOR` warm/cool threshold (currently 12.0) against a real scene.
- Photograph of wooden kitchen table surface under warm lamplight — extract specular highlight shape, wood grain colour variation. Reference for surface rendering in kitchen environments.
- Photograph of heavy curtains or net curtains with pre-dawn light leaking through — extract cool ambient gradient values for kitchen/living room exterior window treatment.

---

## Character Proportions & Anatomy

- Public domain or CC-licensed figure drawing reference: pre-teen (age 11–13) head-to-body proportion chart — verify Luma's 5.5-head canon against real observed ratios. Feed a measurement tool comparing crown-chin height vs full body height.
- Public domain figure drawing reference: elderly woman (age 65–80) standing proportions — cross-check Miri's silhouette ratios. Measure shoulder width vs hip width vs height.
- Public domain hand anatomy reference: child hand vs adult hand scale comparison — informs Luma/Miri interaction staging (mug handoff in SF06).
- CC-licensed facial expression reference sheet (neutral human faces) — use as ground-truth geometry for face test gate calibration. Measure eye-to-nose distance, nose-to-mouth distance, brow height as fraction of face height. Validates FG-L series metric thresholds.

---

## Glitch Art & Digital Artifact Aesthetics

- Creative Commons glitch art photograph (datamoshing / pixel sorting type) — extract dominant hue distribution; measure ratio of UV_PURPLE-adjacent hues (hue angle 260°–300°) to total pixel count. Validate UV_PURPLE linter dominance thresholds.
- Creative Commons pixel art palette study — extract histogram of hue clusters in a restricted palette. Use to verify that the Glitchkin palette (GL-01 through GL-07) covers similar perceptual spread to established pixel art conventions.
- Public domain oscilloscope waveform photograph — extract line weight and glow style for the "Other Side" environment rendering reference.

---

## Suburban Exterior & School Environments

- Creative Commons photograph of a mid-century American suburban street at dusk — extract warm/cool split for Millbrook Street scene. Measure sky cool percentage vs practical streetlight warm percentage.
- Creative Commons photograph of a public middle school hallway with lockers — extract institutional colour palette (wall, floor, locker hues). Cross-reference against `LTG_TOOL_bg_school_hallway.py` palette for authenticity.
- Creative Commons photograph of a school classroom (chalkboard visible) — measure chalkboard reflectance, chalk mark value contrast. Reference for `LTG_TOOL_bg_classroom.py` pixel-font chalkboard section.

---

## Shadow, Depth & Atmospheric Perspective

- Creative Commons photograph of a room with strong depth: multiple objects at FG/MG/BG — extract per-zone warm/cool temperature; measure hue shift from warm FG to cool BG across depth. Quantitative calibration for Depth Temperature Rule (codified C45).
- Creative Commons photograph showing aerial/atmospheric perspective on a clear day — measure hue desaturation and temperature shift per unit of perceived depth. Use to parameterise environment background cool-fade in Tech Den and Glitch Layer.
- Creative Commons photograph of a drop-shadow on a textured surface — measure shadow softness (edge blur in px) relative to object height and light source angle. Reference for dual-warmth drop-shadow implementation in `LTG_TOOL_character_lineup.py`.

---

## Colour Reference Charts

- Munsell colour chart (public domain) — load as reference for perceptual uniformity validation. Tool: compare ΔE between any two palette swatches in CIELAB vs Munsell distance; flags cases where visually similar swatches have large ΔE (tool calibration).
- Macbeth ColorChecker chart (digitised, CC-licensed version) — use as known-good LAB reference target to verify that the ΔE=5.0 threshold in `precritique_qa` corresponds to visually meaningful differences.
- Natural scene statistics study (CC-licensed dataset summary) — extract typical warm/cool pixel ratio in domestic interior photographs. Provides empirical baseline for REAL_INTERIOR threshold (12.0) and REAL_STORM threshold (3.0).

---

## Motion & Gesture

- Creative Commons gesture drawing reference: running child — extract limb angle ranges for Luma's locomotion keyframes. Validate against Luma motion spec v002.
- Creative Commons gesture drawing reference: elderly woman carrying a tray — arm angle, centre-of-gravity shift. Informs Miri motion spec staging.
- Public domain high-speed photography of a small object ricocheting off a surface — extract arc curvature, squash/stretch phase timing. Reference for P14 Byte ricochet off bookshelf.

---

## Proposed Analysis Tools (build on acquisition)

| Reference type | Tool to build |
|---|---|
| CRT glow photograph | `LTG_TOOL_glow_profile_extract.py` — fits Gaussian to radial falloff, outputs σ_x / σ_y for use in glow generators |
| Interior lighting photo | `LTG_TOOL_warmcool_scene_calibrate.py` — measures warm/cool ratio in reference photo, outputs suggested threshold value |
| Expression anatomy reference | `LTG_TOOL_face_metric_calibrate.py` — reads landmark distances from reference, outputs PASS/WARN/FAIL boundary values for face test gate |
| Depth/atmospheric perspective photo | `LTG_TOOL_depth_temp_gradient.py` — measures hue temperature shift per depth tier, outputs per-tier warm/cool targets |
| Glitch art reference | `LTG_TOOL_uv_hue_cluster.py` — extracts hue histogram, validates that UV_PURPLE (hue 270°±15°) forms a dominant cluster above threshold |
| Colour chart | `LTG_TOOL_delta_e_calibrate.py` — maps ΔE values to known perceptual pairs; validates linter thresholds are perceptually meaningful |
| Drop-shadow photograph | `LTG_TOOL_shadow_softness_measure.py` — measures edge gradient width of reference shadow, informs px blur radius in lineup depth bands |
| Interior lighting photo | `LTG_TOOL_warmcool_scene_calibrate.py` — measures warm/cool ratio in reference photo, outputs suggested threshold value for REAL_INTERIOR (12.0) and REAL_STORM (3.0) |

---

## Colour Science Additions (Sam Kowalski, C45)

- D50 vs D65 standard illuminant comparison chart (CIE, public domain) — measure hue shift between the two white-points in CIELAB; ensures our LAB-space ΔE calculations are consistent whether the viewer renders under D50 (print) or D65 (screen/projector). Informs pitch-deck projection QA.
- Simultaneous contrast swatch pairs (public domain illustration) — pairs of identical swatches on different background colours appearing different. Provides concrete examples for calibrating where ΔE=5.0 is perceptually meaningful vs. misleading. Use to stress-test the `render_qa` and `color_verify` pass thresholds.
- Bezold-Brücke hue shift reference chart (public domain perceptual study) — documents how perceived hue shifts with luminance increase (reds shift toward yellow, blues toward cyan at high brightness). Reference when evaluating CORRUPT_AMBER and UV_PURPLE behaviour at highlight extremes in the Glitch Layer.

## C45 Response Notes
- **Sam Kowalski** responded this cycle: top priorities = interior lighting calibration photo + Macbeth ColorChecker for ΔE=5.0 validation. Three colour-science additions incorporated above.
- **All other members**: reference shopping list question is in inboxes — responses expected C46.
