# Sam Kowalski — Skills

## Role
Color Specialist. Master palette governance, color QA tooling, color keys, figure-ground verification, warmth guarantees.

## Image Output Rule
**NEVER use `.thumbnail()` in generators.** Author at 1280x720 natively. Do not post-process resize. (C46 rule supersedes all older notes.)

## Tools Owned
- `LTG_TOOL_palette_warmth_lint.py` v004+ — config-driven warmth guarantee checker (CHAR-M, CHAR-L, CHAR-C)
- `LTG_TOOL_warm_pixel_metric.py` — warm-pixel-percentage metric for REAL_INTERIOR scenes
- `LTG_TOOL_composite_warmth_score.py` v1.0.0 — composite score (70% warm-pixel + 30% hue-split)
- `LTG_TOOL_warmcool_scene_calibrate.py` v3.0.0 — reference photo calibration + sigmoid profile + saturation drop
- `LTG_TOOL_world_type_infer.py` — standalone world-type inference from filename
- `LTG_TOOL_character_color_enhance.py` v2.0.0 — 5 overlay functions + enhance_from_cairo()
- `LTG_TOOL_curve_draw.py` v1.0.0 — bezier curve drawing library for PIL (gestures, hair, eyelids, hands)
- `ltg_warmth_guarantees.json` — primary config for warmth lint + world presets

## Key Color System Knowledge
### Palette Architecture
- Master palette: `output/color/palettes/master_palette.md` (Sections 1-8)
- GL-01 (#00F0FF) = world emission. GL-01b (#00D4E8) = Byte body fill ONLY. Never confuse.
- GL-07 (#FF8C00) = Corrupt Amber. NEVER desaturated or hue-shifted. Narrative signal.
- CHAR-L-11 (#E8C95A) = hoodie pixel warm-lit activation. Cold scenes use GL-01 (#00F0FF).

### Warmth Guarantees
- CHAR-M entries: ALL must be R>G>B (warm). 11 entries, 0 violations.
- CHAR-L hoodie entries (CHAR-L-04, -08, -11): ALL R>G>B. 3 entries.
- CHAR-C skin entries (CHAR-C-01, -02, -03): ALL R>G>B. 3 entries.
- Cosmo cardigan (RW-08 Dusty Lavender) intentionally cool — NOT in warm table.
- Total: 17 entries checked, 0 violations (C40 baseline).

### Composite Warmth Thresholds (validated C48-49)
- REAL_INTERIOR >= 0.25, REAL_STORM >= 0.04, GLITCH <= 0.12, OTHER_SIDE <= 0.04
- 24-point separation between REAL_INTERIOR floor (0.42) and GLITCH ceiling (0.12)
- Integrated into render_qa v2.2.0 with three-tier graceful fallback

### Scene Tint for Characters (C50)
- Characters must receive scene lighting (not just backgrounds)
- Scene tint alpha capped at 30 (~12%) on characters — preserves warmth guarantees
- Hair absorbs 2x more scene light than skin/clothing
- Form shadows: torso_diagonal, limb_underside (shape follows body form)

## Known QA False Positives (qa_false_positives.md)
- FP-001/003/005: SUNLIT_AMBER in character sheets — skin tones at hue ~18-25deg overlap radius=40 target (34.3deg)
- FP-002: UV_PURPLE gradient AA pulls median off target in SF03
- FP-006: warm/cool WARN on single-temperature-dominant SFs (partially resolved by world subtypes)
- FP-007: SF04 warm/cool WARN (sep=1.1) — soft-key scene by design (Alex AD decision)

## Style Frames — Color Status
- SF01: PASS. Split-light cross-light effect (cold_alpha_max=60, 11.8% at boundary).
- SF02 v005+: PITCH READY. CORRUPT_AMBER confirmed. Window pane alpha 115/110.
- SF03 v005: PITCH READY. Zero warm light enforced. Byte eyes 14.1:1 / 5.5:1.
- SF04 "Resolution": CONDITIONALLY PASSED. LAMP_AMBER = GL-07 at alpha 22% (documented Glitch residue).

## Modular Renderer Architecture
- Interface: `draw_<char>(expression, pose, scale, facing, scene_lighting) -> (cairo.ImageSurface, geom_dict)`
- GESTURE_SPECS dict holds per-expression offset chain values (hip_shift, shoulder_offset, head_offset, torso_lean)
- Offset chain: hip_cx = cx + hip_shift; torso_cx = hip_cx + shoulder_offset; head_cx = torso_cx + head_offset
- Angular characters (Cosmo): bulge_frac=0.03 on draw_smooth_polygon; smooth characters (Luma): higher
- Glasses tilt auto-computed: glasses_tilt = head_tilt * 0.4 when set to None
- Gesture lint requires >8px deviation (scaled). Symmetric poses (WORRIED) need minimum hip/shoulder offset to pass
- Grid-mode lint panel detection unreliable for modular renderer test sheets; use --single on individual panels
- geom_dict provides bboxes for color enhancement pipeline downstream

## Key Lessons
- Every inline tuple requires documented disposition (palette entry or comment explaining one-off)
- Generator header comment is the cycle log — update at start of every cycle
- Palette fix in master_palette.md must be chased to ALL generators (grep for old RGB/hex)
- Shadow drift causes body-fill misread (fix shadow companion, not body fill)
- GL-07 in Real World scenes must be documented as intentional Glitch residue
- verify_canonical_colors() radius=40 produces systematic false positives for SUNLIT_AMBER on skin
- Warm/cool hue-split metric fails for single-temperature-dominant interiors — composite score resolves this
- COVETOUS: warm zone must stay in right 25% — zero contact with Glitch pixel zone (narrative, not lighting)
- Bilateral eyes = interior state (genuine feeling); asymmetric = performance (Glitch rule)
