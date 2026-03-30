# Visual Reference Shopping List

Reference assets for analysis and art direction on *Luma & the Glitchkin*.
**Copyright rule:** All references are for measurable analysis only — palette extraction, geometry measurement, lighting ratios, composition structure. No copying of style, character design, or artwork. Prefer Creative Commons / public domain sources.

**Local folder:** `reference/` (gitignored — local use only).

---

## CRT & Retro Display Aesthetics

- **ACQUIRED** `reference/crt/` (18 files) — CRT screens in dark rooms, glow on faces and surfaces. Measure phosphor glow radius, FWHM of bloom, warm/cool cast of ambient spill. Feed into `LTG_TOOL_bg_grandma_kitchen.py` glow calibration.
- **ACQUIRED** `reference/scanline closeup/` (6 files) — CRT scanlines at various brightness/resolutions. Extract scanline pitch, inter-line darkness ratio, horizontal smear profile. Tune Glitch Layer pixel-grid rendering.
- **ACQUIRED** `reference/crt static/` (5 files) — CRT snow/static noise. Measure spatial frequency distribution. Reference for UV_PURPLE corruption texture.
- **ACQUIRED** `reference/crt afterglow/` (3 files) — Phosphor afterglow/decay. Measure hue shift from active white to decay trail. Informs CORRUPT_AMBER contamination hue path.
- **ACQUIRED** `reference/crt phosphor/` (7 files) — Green phosphor monitors, glow characteristics. Extract glow colour temperature and falloff.
- **ACQUIRED** `reference/crt cabinet/` (17 files) — CRT TV cabinets in domestic settings (wood, plastic, vintage). Extract material colour, wood grain tone, plastic off-white values for Miri's set-prop palette.

---

## Warm Interior Lighting (Real World — Kitchen & Living Room)

- **ACQUIRED** `reference/kitchen predawn/` (3 files) — Kitchens at dawn/low light with practical lamps. Measure warm/cool pixel ratio, shadow angle, lamp falloff curve. Baseline for SF05 "The Passing" (current target: 16.7).
- **ACQUIRED** `reference/kitchen mug steam/` (3 files) — Ceramic mugs with rising steam. Extract steam opacity gradient, motion blur direction, colour temperature of transmitted light through steam.
- **ACQUIRED** `reference/living room night/` (7 files) — Living rooms with single lamp sources, dark windows. Measure warm zone radius from practical source. Calibrate `REAL_INTERIOR` warm/cool threshold (12.0) against real scenes.
- **ACQUIRED** `reference/dawn curtains/` (3 files) — Curtains with pre-dawn light leaking through. Extract cool ambient gradient values for kitchen/living room exterior window treatment.
- NOT YET — Photograph of wooden kitchen table surface under warm lamplight (specular highlight shape, wood grain colour variation).

---

## Character Proportions & Anatomy

- **ACQUIRED** `reference/drawing guides/body/` (6 files) — Pre-teen and child proportion charts, adult vs child comparisons. Verify Luma's 5.5-head canon against real ratios. Feed measurement tool comparing crown-chin height vs full body height.
- **ACQUIRED** `reference/drawing guides/face/` (14 files) — Facial expression sheets, proportion guides, cartoon expression studies. Ground-truth geometry for face test gate calibration. Measure eye-to-nose, nose-to-mouth, brow height ratios.
- **ACQUIRED** `reference/drawing guides/hand/` (9 files) — Hand anatomy breakdowns, scale references. Informs Luma/Miri interaction staging (mug handoff in SF06).
- NOT YET — Elderly woman (age 65–80) standing proportions specifically (body guides cover pre-teen well; elderly coverage is thin).

---

## Glitch Art & Digital Artifact Aesthetics

- **ACQUIRED** `reference/glitches/` (10 files) — Datamoshing, pixel sorting, abstract pixel art. Extract dominant hue distribution; measure UV_PURPLE-adjacent hue ratio (260°–300°). Validate UV_PURPLE linter dominance thresholds.
- **ACQUIRED** `reference/pixelart/` (5 files) — Pixel art palette studies and game screenshots. Extract histogram of hue clusters in restricted palettes. Verify Glitchkin palette (GL-01–GL-07) perceptual spread.
- **ACQUIRED** `reference/oscilloscope/` (3 files) — Oscilloscope waveforms. Extract line weight and glow style for "Other Side" environment rendering.

---

## Suburban Exterior & School Environments

- **ACQUIRED** `reference/suburban dusk/` (3 files) — Suburban streets at twilight. Extract warm/cool split for Millbrook Street. Measure sky cool % vs streetlight warm %.
- **ACQUIRED** `reference/school halway/` (7 files) — Middle school hallways with lockers. Extract institutional colour palette (wall, floor, locker hues). Cross-reference `LTG_TOOL_bg_school_hallway.py`.
- **ACQUIRED** `reference/classroom/` (4 files) — Classrooms with chalkboards. Measure chalkboard reflectance, chalk mark value contrast. Reference for `LTG_TOOL_bg_classroom.py`.

---

## Shadow, Depth & Atmospheric Perspective

- **ACQUIRED** `reference/depth/` (4 files) — Rooms with strong FG/MG/BG depth. Extract per-zone warm/cool temperature; measure hue shift across depth. Calibrate Depth Temperature Rule.
- **ACQUIRED** `reference/aerial/` (5 files) — Aerial/atmospheric perspective on clear days. Measure hue desaturation and temperature shift per unit of perceived depth. Parameterise environment background cool-fade.
- **ACQUIRED** `reference/drop shadow/` (3 files) — Drop shadows on textured surfaces. Measure shadow softness (edge blur px) relative to object height and light angle. Reference for dual-warmth drop-shadow in `LTG_TOOL_character_lineup.py`.

---

## Colour Reference Charts

- **ACQUIRED** `reference/color/` (7 files) — Munsell colour wheels, indoor lighting datasets, colour montages. Load as reference for perceptual uniformity validation. Compare ΔE between palette swatches in CIELAB vs Munsell distance.
- NOT YET — Macbeth ColorChecker chart (digitised, CC-licensed version). Known-good LAB reference to verify ΔE=5.0 threshold corresponds to visually meaningful differences.
- NOT YET — Natural scene statistics study (CC-licensed dataset summary) — domestic interior warm/cool ratio empirical data.

---

## Motion & Gesture

- **ACQUIRED** `reference/gesture/` (11 files) — Running child, tray carrying, ricochet photography. Extract limb angle ranges for Luma locomotion, arm angles for Miri staging, arc curvature for P14 Byte ricochet.
- NOT YET — Elderly woman carrying a tray specifically (gesture/ has tray references but may need more Miri-specific age-appropriate references).

---

## Gaps Summary (still needed)

| Item | Priority | Why |
|---|---|---|
| Macbeth ColorChecker (digitised) | HIGH | Sam's top request — ΔE=5.0 threshold validation |
| Natural scene statistics dataset | MEDIUM | Empirical baseline for REAL_INTERIOR/REAL_STORM thresholds |
| Elderly woman proportions | MEDIUM | Miri silhouette ratio cross-check |
| Wooden table under warm lamplight | LOW | Kitchen surface rendering detail |
| D50 vs D65 illuminant chart | LOW | Sam's colour-science addition — pitch-deck projection QA |
| Simultaneous contrast swatch pairs | LOW | Sam — ΔE threshold stress testing |
| Bezold-Brücke hue shift chart | LOW | Sam — CORRUPT_AMBER/UV_PURPLE at highlight extremes |

---

## Proposed Analysis Tools (build now — references acquired)

| Reference folder | Tool to build | Priority |
|---|---|---|
| `crt/` | `LTG_TOOL_glow_profile_extract.py` — fits Gaussian to radial falloff, outputs σ_x / σ_y for glow generators | HIGH |
| `living room night/` + `kitchen predawn/` | `LTG_TOOL_warmcool_scene_calibrate.py` — measures warm/cool ratio in reference photo, outputs threshold value | HIGH |
| `drawing guides/face/` | `LTG_TOOL_face_metric_calibrate.py` — reads landmark distances, outputs PASS/WARN/FAIL boundaries for face test gate | HIGH |
| `depth/` + `aerial/` | `LTG_TOOL_depth_temp_gradient.py` — measures hue temp shift per depth tier, outputs per-tier warm/cool targets | MEDIUM |
| `glitches/` | `LTG_TOOL_uv_hue_cluster.py` — extracts hue histogram, validates UV_PURPLE (270°±15°) dominant cluster | MEDIUM |
| `color/` | `LTG_TOOL_delta_e_calibrate.py` — maps ΔE to known perceptual pairs; validates linter thresholds | MEDIUM |
| `drop shadow/` | `LTG_TOOL_shadow_softness_measure.py` — measures edge gradient width, informs blur radius in depth bands | LOW |
| `scanline closeup/` | `LTG_TOOL_scanline_profile.py` — measures scanline pitch and darkness ratio from CRT close-ups | LOW |

## C45 Response Notes
- **Sam Kowalski** responded this cycle: top priorities = interior lighting calibration photo + Macbeth ColorChecker for ΔE=5.0 validation. Three colour-science additions (D50/D65, simultaneous contrast, Bezold-Brücke) in Gaps table.
- **All other members**: reference shopping list question is in inboxes — responses expected C46.
