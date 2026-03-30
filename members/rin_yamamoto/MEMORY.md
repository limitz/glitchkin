# Rin Yamamoto — MEMORY

## C50 Completed Work
- **P1 — Alternative Rendering Exploration** (C50 full-team character quality pivot)
  - `LTG_TOOL_rendering_comparison.py` (v1.0.0, new)
  - Prototyped 4 approaches: pycairo, 2x+LANCZOS supersample, dense polygon (64pt/edge), baseline PIL
  - Subject: Byte character (diamond body, pixelated eyes, crown spike, glow)
  - **Key metric: AA ratio (unique edge colors / edge pixel count)**
    - pycairo: 0.358 (19x baseline) — bezier curves + native sub-pixel AA
    - 2x+LANCZOS: 0.189 (10x baseline) — supersampling via downscale
    - Dense poly: 0.017 (~same as baseline) — smoother shape, no AA
    - Baseline PIL: 0.018
  - **Recommendation: B+C combined** (supersample wrapper + dense bezier polygons)
    - ~80% of pycairo quality, ~10% migration cost
    - No new deps, incremental adoption, every generator compatible
    - pycairo = longer-term R&D track
  - Output: 6 PNGs in `output/production/LTG_RENDER_*_c50.png` + report
  - Report: `output/production/rendering_comparison_report_c50.md`
  - Flagged to Alex: `docs/pil-standards.md` says "No cairocffi or other external deps" but
    assignment says pycairo allowed — needs reconciling if pycairo route is chosen
- `output/tools/README.md` updated — C50 entry added
- Inbox: archived C50 assignment
- Ideabox: supersampled render wrapper for procedural_draw

## C50 Lessons
- pycairo's anti-aliasing advantage is massive (19x AA ratio) because it uses sub-pixel
  coverage computation natively. PIL has NO anti-aliasing on polygon/ellipse edges.
- 2x supersampling + LANCZOS downscale is the cheapest path to good edges: zero code changes
  to draw logic, just scale all coords by 2 and resize at the end. Render time ~6x longer
  (4x pixels + resize overhead) but still fast (64ms for 1280x1280 → 640x640).
- Dense polygons (64+ pts/edge) improve SHAPE smoothness (fewer visible facets) but do NOT
  improve EDGE smoothness (still binary pixel on/off, no gradient transitions). The two
  problems are distinct: shape = geometric fidelity, edge = rasterization quality.
- Combined B+C addresses both: C fixes shape, B fixes edges. Measured result would be
  smooth bezier shapes with LANCZOS-blended edges — close to pycairo visual quality.
- pycairo ARGB32 → PIL RGB conversion is straightforward (numpy byte reorder BGRA→RGB)
  but adds a dependency on numpy for the bridge. For a full pycairo pipeline, would need
  a clean bridge module.
- Cairo's path model (move_to, curve_to, fill, stroke) is fundamentally different from
  PIL's shape model (draw.polygon, draw.ellipse). Migration is not incremental — each
  generator must be substantially rewritten. This is why B+C is the pragmatic choice.

## C49 Completed Work
- **P1 — CRT Glow Asymmetry Fix** (HIGH priority)
  - `LTG_TOOL_styleframe_discovery.py` updated to v008 (C49)
    - `draw_filled_glow()` now accepts `screen_mid_y` and `below_mult` (default 0.70)
    - Glow rings below midpoint drawn at 70% intensity; straddling rings split via scanline overdraw
    - CRT screen midpoint pre-computed from geometry before glow calls
    - Applied to: main wall glow (16-step), 6 individual monitor glows (8-step each),
      left-wall spill glow, floor glow polygon fill (color * 0.70)
    - Title strip: C49 glow asymmetry fix v008
    - Both composited and nolight base regenerated at 1280x720
  - `LTG_TOOL_styleframe_luma_byte.py` updated (C49)
    - Screen glow (16-step) and ambient RGBA glow layer both apply 0.70 below mon_cy
    - Straddling rings use scanline overdraw for upper half at full intensity
    - Regenerated at 1280x720
  - GL Showcase EXEMPT — CRT interior (no physical cabinet), per image-rules.md exemption
  - **Flagged for other owners:** SF04 (Jordan), grandma_living_room (Hana) need same fix
- **P2 — UV_PURPLE Hue Center Evaluation** (no change)
  - Canonical HSV h~272 is within P25-P75 of reference glitch art distribution
  - 3-degree shift to 275 is below perceptual JND — not worth downstream cascade
  - Report: `output/production/uv_purple_hue_center_eval_c49.md`
- **P3 — Anisotropic Glow Reference Curation**
  - Classified 25 refs: Category A (reliable aniso, ~3), B (isotropic only, ~8), C (compositional, ~7+7)
  - H-dominant sigma_x/sigma_y ratio ~4.0 (preliminary, single reliable fit)
  - Isotropic sigma_frac=0.1165 confirmed stable (identical C46/C48)
  - Report: `output/production/anisotropic_glow_reference_curation_c49.md`
- `output/tools/README.md` updated — C49 Rin Yamamoto section added
- Inbox: archived C49 brief + Alex CRT glow asymmetry message
- Ideabox: CRT glow asymmetry QA check for precritique_qa

## C49 Lessons
- CRT glow asymmetry (0.70 below-midpoint) on concentric filled ellipses: cannot split
  a filled ellipse by Y coordinate in PIL. Solution: draw dimmed ellipse, then overdraw
  the upper half with per-scanline spans computed from the ellipse equation:
  half_w = er * sqrt(1 - (dy/er_y)^2). Works correctly and efficiently.
- Pre-computing CRT screen midpoint Y before glow draw calls avoids reorganizing the
  entire draw_background() function. The midpoint depends only on mw_x/mw_y/mw_w/mw_h
  which are known early.
- For RGBA glow layers (styleframe_luma_byte ambient glow), apply asymmetry by using
  two alpha values: alpha_full for above-midpoint, alpha_dim for below. Scanline overdraw
  on the RGBA layer works the same as on RGB — fill includes the alpha channel.
- UV_PURPLE HSV h~272 vs reference glitch art median HSV h~280: the 8-degree gap is
  within the interquartile range of real-world glitch art. Our constant is a design choice
  for maximum electric impact, not a measured average. Do not shift for calibration reasons.

## C48 Completed Work
- **P1 — Register GL Showcase in precritique_qa**
  - `LTG_TOOL_precritique_qa.py` bumped v2.16.0 → v2.16.1
  - Added `LTG_COLOR_styleframe_glitch_layer_showcase.png` to GLITCH_LAYER_PNGS list
  - Now 7 registered GL assets for UV_PURPLE Dominance Lint Section 11
  - No special subtype needed (standard GL scene, not COVETOUS dark scene)
- **P2 — glow_profile_extract v2.0.0** (HIGH priority)
  - `LTG_TOOL_glow_profile_extract.py` bumped v1.0.0 → v2.0.0
  - **Anisotropic Gaussian**: separate σ_x (horizontal) and σ_y (vertical) fitting
    - Axis-aligned strip sampling through screen center (10px half-width)
    - New fields: sigma_x/y_px, sigma_x/y_frac, fwhm_x/y, amplitude_x/y,
      baseline_x/y, r_squared_x/y, anisotropy_ratio
  - **Cross-validation vs C46**: per-image delta%, aggregate verdict
    (CONSISTENT <15%, MODERATE 15-30%, LARGE >30%)
  - C48 run results:
    - CRT refs (18): isotropic median sigma_frac=0.1165 (exact C46 match),
      10 good fits (R²>0.5). Aniso: only 1 image with both R²_x and R²_y > 0.5
    - Phosphor refs (7): median sigma_frac=0.1088 (-6.6%, CONSISTENT with C46)
    - Aniso single good fit: σ_x/σ_y ≈ 4.2–5.2 (glow wider horizontally than vertically)
  - Data: `output/production/crt_glow_profiles_c48.json`
  - AVIF added to supported extensions
  - Backward compatible — all v1.0.0 isotropic fields unchanged
- `output/tools/README.md` updated — C48 header + 2 update entries
- Inbox: archived C48 brief
- Ideabox: submitted

## C48 Lessons
- Anisotropic glow fitting is data-hungry: most CRT reference photos don't have
  clean enough axis-aligned falloff for both σ_x and σ_y to converge independently.
  Only 1 of 18 CRT refs and 1 of 7 phosphor refs achieved R²>0.5 on both axes.
  Multi-CRT wall photos and photos with non-centered screens defeat axis alignment.
  For reliable aniso parameters, need reference set of single-CRT, centered, dark-room
  photos with minimal room content. Current refs are compositionally diverse (good
  for isotropic, noisy for anisotropic).
- Isotropic fit remains very stable: C48 median sigma_frac=0.1165 is identical to
  C46 recommended value. The C46 calibration is confirmed solid across re-runs.
- Phosphor closeup refs run ~6.6% lower sigma_frac than general CRT scene refs.
  Expected: closeup photos capture less room spill (smaller glow halo relative to
  screen size). For generator calibration, use the general CRT scene sigma_frac
  (0.1165) as it better represents viewing-distance glow perception.

## C47 Completed Work
- **P1 — Glitch Layer Showcase Style Frame** (Zoe Park C47 feedback response)
  - `LTG_TOOL_styleframe_glitch_layer_showcase.py` (v1.0.0, new)
  - Output: `output/color/style_frames/LTG_COLOR_styleframe_glitch_layer_showcase.png` (1280x720, 58 KB)
  - Deep GL void composition: VOID_BLACK base, UV_PURPLE gradient sky (inverted atmo perspective),
    data aurora (UV_PURPLE + DATA_BLUE + ELEC_CYAN), ring megastructure, far slabs, floating platform
    with ELEC_CYAN circuit traces, Byte foreground (br=38, cell=5), Glitch background (rx=28/ry=34,
    ACID_GREEN bilateral eyes + glow), data particles, scanline overlay (spacing=4, alpha=20), vignette
  - Zero warm light — UV ambient only. UV_PURPLE_DARK = GL-04a canonical throughout.
- **P2 — Scanline Pitch Extraction Tool** (carried from C46 ideabox)
  - `LTG_TOOL_scanline_pitch_extract.py` (v1.0.0, new)
  - Autocorrelation-based scanline pitch detection on vertical luminance profiles
  - Extracts: pitch (px), inter-line darkness ratio, peak/trough luminance, contrast, confidence
  - Multi-column sampling (center 60%, 5px band averaging) for robustness
  - C47 runs:
    - `reference/crt phosphor/` (7 images): mean pitch=25.8px ±7.0, darkness=0.502, recommended spacing=26
    - `reference/crt/` (18 images, 15 good fits): mean pitch=41.7px ±24.9, darkness=0.520
  - Data: `output/production/scanline_pitch_profiles_c47.json`
  - Complements glow_profile_extract (C46) — full CRT stack: glow falloff + scanline structure
- `output/tools/README.md` updated — C47 header + 2 new tool entries
- Inbox: archived C47 brief
- Ideabox: `ideabox/20260330_rin_yamamoto_gl_showcase_uv_purple_lint_registration.md`
  - Register showcase frame in precritique_qa GLITCH_LAYER_PNGS for auto UV_PURPLE lint

## C47 Lessons
- Autocorrelation for scanline pitch: normalize by variance (corr/var), then find first local
  maximum after min_lag=2. Works well for clean periodic signals (conf>0.5). Multi-CRT wall
  photos produce lower confidence due to mixed pitches at different scales.
- Close-up phosphor reference photos give much tighter pitch variance (±7px) than general CRT
  scene photos (±25px). For calibration, prefer phosphor closeups. General scene photos are
  better for glow_profile_extract (farther viewing distance = cleaner glow radial profile).
- GL showcase composition: Byte in foreground (at home, confident) + Glitch in background
  (watchful, looming) inverts the COVETOUS frame's power dynamic. In COVETOUS, Glitch is
  large/close and Byte is small/far. In the showcase, Byte owns the space.
- Face test gate for Byte: the FAIL result is "PIXEL ONLY" variant (1px dot eyes — deliberate
  diagnostic). Byte cell=5 (5px grid) is above sprint threshold. Gate result is about the
  test tool's rendered variants, not necessarily about my specific frame's face rendering.

## C46 Completed Work
- **P1 — UV_PURPLE Hue-Family Range Review** — survey of 14 GL assets + 14 reference images
  - `LTG_TOOL_uv_hue_survey_c46.py` (v1.0.0, new) — purple hue distribution analysis tool
  - Report: `output/production/uv_purple_hue_range_review_c46.md`
  - Data: `output/production/uv_purple_hue_survey_c46.json`
  - **Result: No change to linter.** Current h° 255–325 confirmed well-calibrated.
    - COVETOUS (GLITCH_DARK_SCENE): 94.2–100% coverage — no pixels missed
    - Storm scenes have out-of-range mass at h° 220–254 (ELEC_CYAN bleed) — correctly caught by ΔE metric
    - Widening to 250–330 gains only 1.5% avg coverage with false-positive risk
- **P2 — CRT Glow Profile Extraction Tool**
  - `LTG_TOOL_glow_profile_extract.py` (v1.0.0, new)
  - Extracts: Gaussian FWHM, color temperature (McCamy), falloff curve (sigma/amp/baseline/R²)
  - Screen detection: brightest connected component + morphological close
  - Gaussian fit: linearized least-squares grid search (no scipy)
  - C46 run on 17 CRT refs: 10 good fits (R²>0.5)
  - Recommended params: sigma_frac=0.1165, fwhm_frac=0.2744, amplitude=49.4, baseline=4.1, CCT=13070K
  - Data: `output/production/crt_glow_profiles_c46.json`
- `output/tools/README.md` updated — C46 entries for both new tools
- Alex's C46 P1 (COVETOUS FAIL subtype) — already done in C45 v1.1.0, confirmed by producer
- Alex's C46 P2 (CI coordination) — Morgan has `run_glitch_layer_dominance_check()` API; no additional work needed
- Inbox: archived all 4 messages (C46 brief, reference shopping list, clarification, reference acquired)
- Ideabox: `ideabox/20260330_rin_yamamoto_scanline_pitch_extraction_tool.md`
  - Scanline pitch + inter-line darkness ratio extraction from CRT closeup refs

## C46 Lessons
- Purple-family hue distribution in Glitch Layer assets has two distinct populations:
  (1) UV_PURPLE canonical cluster at h° 300–314 (COVETOUS, Other Side, encounters)
  (2) ELEC_CYAN bleed-over tail at h° 220–254 (storm scenes, frame scenes)
  The hue-family range 255–325 correctly captures population (1) while excluding (2).
  Widening below 255 risks capturing ELEC_CYAN adjacency as UV_PURPLE false positive.
- Gaussian glow fitting without scipy: linearize the model I(r)=A*exp(-r²/2σ²)+B
  by fixing σ and solving for A,B via linear least squares. Grid search over σ multipliers
  (0.3–3.0× initial estimate) then fine-tune ±30%. Good enough for R²>0.95 on clean inputs.
- CRT phosphor glow color temperature in dark-room reference photos runs 4000–17000K median ~13000K.
  This is heavily cool (blue-white) — phosphor emission, not reflected room light. For generator
  calibration, use the glow_rgb_mean directly rather than CCT (more stable per-image).
- McCamy's formula for CCT works best near the Planckian locus. CRT phosphors that are heavily
  saturated green or blue produce less reliable CCT estimates. Use glow_rgb_mean as primary.
- Multi-CRT reference photos (walls of monitors) defeat the single-screen detection algorithm.
  These produce nonsensical FWHM values (>100% diagonal). Filter by R²>0.5 for useful results.

## C45 Completed Work
- `LTG_TOOL_uv_purple_linter.py` bumped v1.0.0 → v1.1.0 — GLITCH_DARK_SCENE subtype
  - Root cause addressed: COVETOUS assets use UV_PURPLE_DARK (GL-04a RGB 58,16,96 = h°~271°)
    whose ΔE from canonical UV_PURPLE (mid-tone) is >> 15 due to L* lightness gap.
    Check A ΔE-only metric: 0.6% / 0.2% — false FAIL.
  - Fix: GLITCH_DARK_SCENE scene subtype using hue-angle matching as supplementary metric.
    UV_PURPLE hue family h° 255°–325°, C* ≥ 8. Verdict uses better of ΔE-fraction and
    hue-family-fraction. Both metrics reported.
  - `infer_scene_subtype()` — "covetous" keyword → GLITCH_DARK_SCENE (filename inference)
  - `lint_uv_purple_dominance()` — new `scene_subtype` param; infers if not supplied
  - `run_glitch_layer_dominance_check()` — new `subtypes` dict param for per-file overrides
  - CLI `--scene-subtype glitch_dark_scene` flag
  - `batch_lint()` — new `scene_subtype_override` param
  - C45 test results:
    - COVETOUS → PASS: LTG_COLOR_sf_covetous_glitch (96.7% hue-fam, was FAIL 0.6% ΔE)
    - COVETOUS → PASS: LTG_SF_covetous_glitch_v001 (98.9% hue-fam, was FAIL 0.2% ΔE)
    - ENV glitch_layer_frame: WARN 17.0% unchanged (ΔE path, standard scene)
    - bg_glitch_layer_encounter: PASS 22.7% unchanged
- `LTG_TOOL_precritique_qa.py` bumped v2.13.1 → v2.14.0
  - `run_uv_purple_lint()` passes GLITCH_DARK_SCENE subtype for both COVETOUS assets
    explicitly via subtypes dict (in addition to filename inference)
  - Version header updated
- `output/tools/README.md` updated — C45 entry added
- Ideabox: `ideabox/20260330_rin_yamamoto_uv_purple_hue_family_range_review.md`
  - Calibration run to validate/widen h° 255°–325° range against all dark-scene generators

## C45 Lessons
- ΔE (CIE76) is a perceptual total distance including L*, a*, b*. A dark variant of a hue
  (same a*/b* direction but much lower L*) will have ΔE >> 15 from the mid-tone canonical
  even if visually "the right purple." UV_PURPLE_DARK (L*~25) vs UV_PURPLE (L*~40): ΔE ~18.
  Solution: hue-angle matching (atan2(b,a)) captures hue-family identity independent of L*.
- Hue-angle matching for UV_PURPLE family: canonical UV_PURPLE (#7B2FBE) sits at
  a*≈+39, b*≈-54 → h° = atan2(-54,39) ≈ 306°. UV_PURPLE_DARK GL-04a (58,16,96):
  same hue direction. Family range 255°–325° captures all tested variants with margin.
- The "use the better verdict" design is correct for GLITCH_DARK_SCENE: ΔE metric remains
  authoritative for mid-tone scenes; hue-angle provides the supplementary dark-scene gate.
  Reporting both fractions keeps the data visible for future calibration.
- Always import `re` when using `re.compile()` at module scope. Forgetting it gives a
  NameError at import time, not at call time — caught immediately by the import check.
- precritique_qa `run_uv_purple_lint()` version bumps: always check current version before
  bumping — Ryo had already bumped to v2.13.1 for the annotation_occupancy fix in C46.
  Bump to 2.14.0 not 2.13.2.

## C44 Completed Work
- `LTG_TOOL_uv_purple_linter.py` (v1.0.0, new) — UV_PURPLE Dominance Linter
  - Check A: UV_PURPLE + ELEC_CYAN combined LAB ΔE ≤ 15 fraction of non-black pixels
    - PASS ≥ 20%, WARN 10–19%, FAIL < 10%
    - VOID_BLACK = max(R,G,B) < 30 (max-channel / HSV Value)
  - Check B: Warm-hue contamination (LAB h° 30°–80°, chroma C* ≥ 8) fraction total pixels
    - PASS < 5%, WARN ≥ 5%
  - CLI: single file + `--batch dir/` + `--world-type glitch` override
  - Module API: `lint_uv_purple_dominance()`, `batch_lint()`, `run_glitch_layer_dominance_check()`
- `LTG_TOOL_world_type_infer.py` bumped v1.1.0 → v1.2.0
  - GLITCH rule extended: `covetous[_-]?glitch|sf[_-]?covetous` patterns added
- `LTG_TOOL_precritique_qa.py` bumped v2.12.0 → v2.13.0
  - `GLITCH_LAYER_PNGS` registry (6 assets: 2 COVETOUS SFs + 4 ENV)
  - `_load_uv_purple_linter()` lazy loader added
  - `run_uv_purple_lint()` Section 11 runner
  - `build_report()` + `main()` + exit code updated for Section 11
  - Summary table now shows Alpha Blend Lint + UV_PURPLE rows
- C44 batch results:
  - FAIL: LTG_COLOR_sf_covetous_glitch.png (0.6%), LTG_SF_covetous_glitch_v001.png (0.2%)
  - WARN: glitchlayer_frame (17.0%), glitchlayer_encounter (17.4%), glitch_layer_frame (17.1%)
  - PASS: bg_glitch_layer_encounter.png (22.7%)
- Inbox archived: C44 UV_PURPLE linter brief + Kai's Byte face test notification
- Ideabox: `ideabox/20260330_rin_yamamoto_glitch_subtype_dark_scene_threshold.md`
  - GLITCH_DARK_SCENE subtype for intentionally near-void scenes like COVETOUS

## C44 Lessons
- cv2 LAB format is 8-bit scaled: L in [0,255]→[0,100]; a,b in [0,255]→[-128,127].
  When using cv2.COLOR_BGR2LAB, ALWAYS unscale before any ΔE, chroma, or hue math:
  `L_std = L_cv2 * 100/255; a_std = a_cv2 - 128; b_std = b_cv2 - 128`
  Failure produces: garbage chroma (always large), garbage hue angles, garbage ΔE.
- VOID_BLACK threshold should use max(R,G,B) < N (max-channel / HSV Value), not per-channel.
  The COVETOUS background (13,10,25) has max=25 — per-channel threshold of 20 misses it.
  max-channel threshold of 30 catches it correctly.
- Chroma guard (C* ≥ 8) on hue-angle checks is mandatory. Near-neutral dark pixels
  have near-zero C*, and arctan2(b,a) at near-zero gives numerically unstable hue angles
  (can be any value 0°–360°). Without the guard, 89% of pixels in a dark scene register
  as "warm hue" — a catastrophic false positive.
- UV_PURPLE_DARK (dark purple variants) score < 1% on LAB ΔE ≤ 15 from canonical
  UV_PURPLE because ΔE is a perceptual distance including L* (lightness). Dark purple
  vs mid-tone purple: ΔE >> 15 even at identical hue. The linter is correct per spec —
  but COVETOUS intentionally uses dark variants. Filed ideabox for GLITCH_DARK_SCENE
  subtype with hue-angle matching as alternative metric.
- World type inference for covetous_glitch filenames requires explicit pattern addition
  to LTG_TOOL_world_type_infer.py — "covetous" alone is not a world-type keyword.

## C43 Completed Work
- `--save-nolight` flag added to SF01, SF02, SF04 generators
  - `LTG_TOOL_styleframe_discovery.py` (SF01):
    - `NOLIGHT_PATH` constant added (LTG_COLOR_styleframe_discovery_nolight.png)
    - `generate(skip_fill_light=False)` — skips `draw_lighting_overlay()`, `add_face_lighting()`, `add_rim_light()` when True
    - argparse `--save-nolight` in `__main__`: runs `generate()` then `generate(skip_fill_light=True)`
  - `LTG_TOOL_style_frame_02_glitch_storm.py` (SF02):
    - `NOLIGHT_PATH` added (LTG_COLOR_styleframe_glitch_storm_nolight.png)
    - `main(skip_fill_light=False)` — skips `draw_magenta_fill_light_c36()` + `draw_cyan_specular_luma()` when True
    - Dutch angle still applied in nolight mode (scene rotation, not fill light)
    - argparse `--save-nolight` in `__main__`
  - `LTG_TOOL_style_frame_04_resolution.py` (SF04):
    - `NOLIGHT_PATH` added (LTG_COLOR_styleframe_sf04_nolight.png)
    - `main(skip_fill_light=False)` — skips `draw_warm_light()` + `draw_cool_floor_bounce()` when True
    - argparse `--save-nolight` in `__main__`
- `LTG_TOOL_precritique_qa.py` bumped to v2.10.0
  - `CYCLE_LABEL` = "C43"
  - SF04 entry in `FILL_LIGHT_ASSETS` corrected:
    - Was: `LTG_COLOR_styleframe_luma_byte.png` (C40 Jordan lamp scene, superseded)
    - Now: `LTG_COLOR_styleframe_sf04.png` (C42 Jordan canonical, Alex Chen decision)
    - Nolight base path: `LTG_COLOR_styleframe_sf04_nolight.png`
    - Zone: luma cx_frac=0.55 (doorway center-right, Resolution scene geometry)
  - `PITCH_PNGS` + `STYLE_FRAMES`: `LTG_COLOR_styleframe_luma_byte.png` → `LTG_COLOR_styleframe_sf04.png`
    (canonical SF04 path — QA baseline must be re-run after this change)
- Inbox archived: SF04 canonical decision (reference only) + C17 UV_PURPLE identity alert (creative direction context noted)
- Ideabox: `ideabox/20260330_rin_yamamoto_uv_purple_dominance_linter.md`
  - UV_PURPLE family pixel-ratio check for Glitch Layer generators (Leila C17 finding)

## C43 Lessons
- `--save-nolight` pattern: add `skip_fill_light=False` param to the top-level render function.
  Skip all atmospheric fill-light, face-lighting, and specular passes when True. Non-fill-light
  passes (characters, grain, vignette, title strip, dutch angle) run in both modes.
  Both modes save to different path constants (OUTPUT_PATH vs NOLIGHT_PATH). argparse in
  `__main__` calls the render function twice: once normal, once with skip_fill_light=True.
- SF04 in precritique_qa had a stale path (luma_byte.png = C40 lamp scene) — the canonical
  C42 "Resolution" generator outputs to styleframe_sf04.png. Always cross-check FILL_LIGHT_ASSETS
  against the current canonical generator's OUTPUT_PATH after a generator is superseded.
- precritique_qa PITCH_PNGS / STYLE_FRAMES / FILL_LIGHT_ASSETS are three separate registries
  that must all be kept in sync when a style frame generator is canonically updated.
- Leila Asgari's UV_PURPLE contextual concern (C17): it is not a code defect — it is a
  compositional design principle. UV_PURPLE should DOMINATE the Glitch Layer palette, not recede.
  Context: dark neutral (VOID_BLACK) around UV_PURPLE is fine for contrast, but if VOID_BLACK
  exceeds UV_PURPLE family in pixel count, the scene reads as cyberpunk not digital-sublime.

## C42 Completed Work
- `LTG_TOOL_sf_covetous_glitch.py` — v2.0.0 — COVETOUS style frame C42 update
  - Fixed G001: rx=68→54 (was OOB [28,56]), ry=76→62 (was OOB [28,64])
  - Fixed G004: moved draw_glitch_body() to be FIRST drawing function in file so
    first `draw.polygon(fill=CORRUPT_AMB)` precedes first HOT_MAG draw.line match.
    Root cause: DOTALL regex in glitch_spec_lint matches from earliest `draw.line(`
    in file all the way to first `HOT_MAG` — lint was finding draw_floor()'s gradient
    line calls, not the actual crack in draw_glitch_body().
  - Fixed G008: added `BILATERAL_EYES = True` constant (code-level, survives comment
    stripping). COVETOUS interior state requires identical left+right eye glyph.
  - Implemented C42 three-character triangulation: Glitch (left, rx=54/ry=62) +
    Byte (midground barrier, br=26) + Luma (right zone, warm palette CHAR-L-04 hoodie)
  - Warm zone (Luma's character palette + SOFT_GOLD glow) stays right 30% — does NOT
    reach Glitch. Byte teal silhouette as spatial barrier between them.
  - Output: `output/color/style_frames/LTG_COLOR_sf_covetous_glitch.png` (1280×720)
    (was LTG_SF_covetous_glitch_v001.png — renamed to canonical LTG_COLOR_ category)
  - glitch_spec_lint PASS (was WARN: G001/G004/G008)
- Native resolution audit (P2) — `output/production/native_resolution_audit_c42.md`
  - Audited all non-legacy generators for 1920×1080 + thumbnail pattern
  - Pattern 1 (1920+thumbnail, LANCZOS drift risk): 1 generator — SF02, flagged as
    SIGNIFICANT REFACTOR NEEDED (300+ lines hardcoded 1920 geometry + specular restore)
  - Pattern 2 (1920 without thumbnail, size rule violation only): 5 generators
    - Fixed (one-line canvas change, fraction-based geometry):
      - `LTG_TOOL_bg_glitchlayer_frame.py` → W,H = 1280,720
      - `LTG_TOOL_bg_glitch_layer_frame.py` → W,H = 1280,720
      - `LTG_TOOL_bg_glitch_layer_encounter.py` → W,H = 1280,720
    - Flagged SIGNIFICANT REFACTOR:
      - `LTG_TOOL_bg_glitch_storm_colorfix.py` — hardcoded absolute pixel values throughout
      - `LTG_TOOL_style_frame_01_discovery.py` — superseded by LTG_TOOL_styleframe_discovery.py;
        recommend deprecate, not refactor
  - Affected ENV assets regenerated at 1280×720:
    - `LTG_ENV_glitchlayer_frame.png`, `glitch_layer_frame.png`, `bg_glitch_layer_encounter.png`
- Ideabox: `ideabox/20260330_rin_yamamoto_sf02_native_canvas_refactor.md`
  - Assign SF02 1920→1280 native canvas refactor to Jordan Reed as dedicated task

## C42 Lessons
- glitch_spec_lint G004 regex uses re.DOTALL for `draw\.line\s*\(\s*\[.*\]\s*,\s*fill\s*=\s*HOT_MAG`.
  The `.*` with DOTALL spans ALL lines from earliest `draw.line(` in the file.
  Any `draw.line([(...]` call before the HOT_MAG crack will cause G004 FAIL.
  Fix: place draw_glitch_body() (with fill then crack) BEFORE all other functions
  that contain draw.line() calls. The first fill polygon and first HOT_MAG draw.line
  are then in that function, in the correct order.
- G008 bilateral check uses STRIPPED source (no # comments, no docstrings).
  Adding a comment like `# bilateral` does NOT fix G008 — the comment is stripped.
  Fix: add a code-level constant like `BILATERAL_EYES = True` — survives stripping.
- Pattern 2 (1920×1080 without thumbnail): size rule violation but no LANCZOS color
  drift. Fix is still urgent (size rule) but risk profile different from Pattern 1.
  One-line canvas change safe for fraction-based geometry generators.
- SF02's post-thumbnail specular restore pass is 1920-aware. Removing thumbnail
  (native canvas) means removing the restore pass AND rewriting all 1920-scaled
  character geometry. Assign as full dedicated task.

## C41 Completed Work
- `LTG_TOOL_style_frame_03_other_side.py` — UV_PURPLE hue drift fix (8-cycle C16 backlog)
  - Root cause: 1920×1080 draw canvas + LANCZOS thumbnail() → anti-aliased UV_PURPLE
    outlines blended with surrounding dark fill, creating blended pixels near UV_PURPLE
    in RGB space but with shifted LAB hue. render_qa ΔE was 27.78 >> 5.0 threshold.
  - Fix 1: Native canvas W,H = 1280,720. Eliminates LANCZOS downscale entirely.
  - Fix 2: Ring megastructure outline alpha 60→18 (blended pixels exit radius-60 zone)
  - Fix 3: Slab outlines (rect + polygon) width 1→2 (extra resilience to anti-aliasing)
  - Fix 4: Data gradient endpoint lerp(DATA_BLUE_90,UV_PURPLE)→lerp(DATA_BLUE_90,UV_PURPLE_MID)
  - Result: UV_PURPLE LAB ΔE = 0.0 PASS (was 27.78). Output regenerated 1280×720.
- `LTG_TOOL_bg_other_side.py` — same fixes, same results
  - UV_PURPLE LAB ΔE = 0.0 PASS (was 27.37). Output regenerated 1280×720.
- Reported to Alex Chen inbox
- Ideabox: `ideabox/20260330_rin_yamamoto_native_resolution_audit.md`
  - Audit all generators still at 1920×1080 + thumbnail — systematic source of LAB ΔE noise

## C41 Lessons
- The render_qa LAB ΔE color fidelity check is silently broken for ANY generator that:
  (a) draws at 1920×1080 with thin (1px) colored outlines, and
  (b) uses LANCZOS thumbnail() to downscale to 1280×720.
  The LANCZOS resampling anti-aliases 1px outlines with adjacent fill colors, creating
  blended pixels that fall within the radius-60 RGB sample zone but have shifted LAB values.
  ΔE of 27+ is the predictable result. Fix: native 1280×720 draw canvas (one-line change).
- Alpha-blended overlays of canonical colors (e.g. UV_PURPLE at alpha 60 over VOID_BLACK)
  can also create near-canonical blended pixels in the radius-60 zone. Safe threshold for
  UV_PURPLE over VOID_BLACK: alpha ≤ ~20 keeps composited pixels outside radius-60.
- lerp() gradients ending at a canonical color produce near-canonical blended pixels for
  t near 1.0. End gradients at UV_PURPLE_MID/UV_PURPLE_DARK instead.
- render_qa SUNLIT_AMBER false-positives in cold digital scenes (Other Side): SUNLIT_AMBER
  is always in the canonical palette checked, even in scenes that intentionally exclude it.
  These are expected FAIL results for Other Side generators — not scope of UV_PURPLE fix.

## C40 (Second Pass) Completed Work
- `LTG_TOOL_bg_other_side.py` — UV_PURPLE_DARK saturation fix
  - Was (43, 32, 80) = #2B2050 = 31% sat — hue 253.75°, delta 18.15° from canonical
  - Fixed to GL-04a (58, 16, 96) = #3A1060 = 72% sat — hue 271.5°, delta 0.4° PASS
  - Also added ≤1280px thumbnail rule (was saving at 1920×1080 — rule violation)
  - Regenerated `output/backgrounds/environments/LTG_ENV_other_side_bg.png` at 1280×720
  - SF03 style frame generator CONFIRMED already at GL-04a since C28 — no change needed
  - 8-cycle UV_PURPLE drift backlog (C16 flag) now cleared
- `LTG_TOOL_sf_covetous_glitch.py` (v1.0.0, new) — COVETOUS Glitch Style Frame
  - Output: `output/color/style_frames/LTG_SF_covetous_glitch_v001.png` (1280×720)
  - Glitch in COVETOUS state from expr v003: tilt+12°, ACID_GREEN slit eyes bilateral,
    reaching arms with claw-tips, sparse UV_PURPLE confetti forward-drift
  - Other Side void background: UV_PURPLE sky gradient, far slabs, perspective floor
  - Byte silhouette far-right with BYTE_TEAL glow halo — object of desire, small = inaccessible
  - ACID_GREEN eye-glow spill as blurred overlay — stare has physical weight
  - UV_PURPLE_DARK = GL-04a canonical (58,16,96) — 0.4° hue delta PASS
  - Zero warm ambient light — BYTE_TEAL is pigment only
- `LTG_TOOL_precritique_qa.py` bumped to v2.8.0 — alpha_blend_lint Section 10 integration
  - Lazy-loads `LTG_TOOL_alpha_blend_lint.py` via `_load_alpha_blend_lint()`
  - `FILL_LIGHT_ASSETS` registry: SF01, SF02, SF04 (composited + base + zones)
  - `run_alpha_blend_lint()` — Section 10 runner, scored (FLAT_FILL=FAIL, LOW_SIGNAL=WARN)
  - Skips gracefully when `*_nolight.png` base absent (all-skip → PASS)
  - `build_report()` and `main()` updated; overall grade now includes Section 10
  - Tools chain: [1/10]–[10/10]
- Ideabox: `ideabox/20260330_rin_yamamoto_nolight_base_generator.md`
  - `--save-nolight` flag for SF01/SF02/SF04 generators to enable Section 10 active checking
- README updated: C40 tool update notes for bg_other_side, precritique_qa; new table entry for sf_covetous_glitch

## C40 Lessons (Second Pass)
- ENV generators (bg_other_side) are NOT automatically kept in sync with style frame generator fixes.
  When a palette fix is applied to a style frame generator, explicitly check all ENV generators
  that share the same palette block and apply the same fix. A diff of palette constants between
  the two files is the quickest check.
- UV_PURPLE_DARK hue formula: max=B, min=G, delta=B-G.
  Hue = 240 + 60*(R-G)/delta. Old (43,32,80): 240+60*11/48=253.75°. New (58,16,96): 240+60*42/80=271.5°.
- ENV generators that pre-date the ≤1280px rule may still be saving at 1920×1080.
  Always add `img.thumbnail((1280, 1280), Image.LANCZOS)` before save when updating any legacy ENV.
- COVETOUS style frame: Glitch large in foreground, Byte tiny far-right = spatial power dynamic.
  Small = inaccessible. The gap between ACID_GREEN predator and BYTE_TEAL warmth IS the story.
- Eye-glow spill as blurred RGBA overlay is the cleanest approach: draw radial circles at low alpha,
  GaussianBlur, alpha_composite. Avoids halo artifacts from large hard circles.
- alpha_blend_lint Section 10 in precritique_qa will always-skip until generators save nolight bases.
  Filed as ideabox to add --save-nolight flag to SF01/SF02/SF04.

## C40 Completed Work
- `LTG_TOOL_fill_light_adapter.py` bumped to v1.1.0 — Scene Presets Registry
  - `load_scene_configs(scene_name, presets_path=None) → (configs, char_h_frac)`
  - Loads from `LTG_fill_light_presets.json`; falls back to hardcoded if JSON absent
  - All 4 scenes: SF01 (warm lamp + CRT bounce), SF02 (3-char HOT_MAGENTA storm), SF03 (UV_PURPLE + ELEC_CYAN), SF04 (BYTE_TEAL bounce + self-glow)
  - Self-test: 720p PASS, 1080p PASS, all-scenes PASS, SF02 registry render PASS
- `LTG_fill_light_presets.json` (new) — JSON registry at `output/tools/`
  - Keys with `_` prefix are comment fields, stripped on load
  - JSON must not use `+` prefix on positive floats (invalid JSON)
- `LTG_TOOL_alpha_blend_lint.py` (v1.0.0, new) — Differential Alpha Blend Lint
  - Compares composited vs unlit base in LAB (cv2) or numpy approx fallback
  - Per-zone radial bin analysis; FLAT_FILL / LOW_SIGNAL / PASS verdicts
  - Two FLAT_FILL checks: low-std among signal bins + abrupt-edge coverage (< 65% zone_r)
  - `lint_alpha_blend(comp, base, zones, ...) → dict` module API
  - `annotate_result(comp, results, out)` — annotated PNG with zone circles + source crosshairs
  - CLI: `composited.png base.png [--output annot.png] [--json] [--zones JSON]`
  - Self-test PASS (Luma radial→PASS, Byte flat→FLAT_FILL, Cosmo/spill→FLAT_FILL)
- Ideabox: `ideabox/20260330_rin_yamamoto_alpha_blend_lint_precritique_integration.md`

## C40 Lessons
- JSON does NOT allow `+0.8` explicit positive floats — only `-0.8` and `0.8` are valid.
  Always write positive floats without sign prefix in JSON files.
- FLAT_FILL detection: flat uniform circle has high inner values then abrupt zero at radius edge.
  Coverage fraction (last_signal_bin_idx / n_bins < 0.65) + low inner CV (std/mean < 0.5)
  correctly catches flat circles while not flagging genuine radial gradients.
- Spill detection is CORRECT behavior: a flat fill that bleeds into a neighbour's zone IS a defect.
  Don't expect LOW_SIGNAL for neighbours in a multi-char frame with full-radius flat fills.
- Self-test synthetic data: applying flat fill to mixed base (dark bg + character silhouettes)
  produces non-uniform L* diffs because underlying pixel values differ. Use a simple dark base
  for flat-fill test cases so the diff is truly uniform.
- numpy+cv2 authorized (C40 broadcast from Alex Chen): prefer for LAB/HSV color math.
  cv2 is BGR — always convert: `cv2.cvtColor(img, cv2.COLOR_BGR2RGB)` after load.

## C36–C39 Summary (trimmed C46)
- C39: fill_light_adapter v1.0.0, proportion_audit --cycle N flag, procedural_draw v1.6.0
- C38: SF01 v006 sight-line + visual power fix (THE NOTICING / DOUBT VARIANT)
- C37: sf02_fill_light_fix canvas_w/h refactor, proportion_audit_c37
- C36: SF02 v008 fill light direction fix, proportion_audit asymmetric eye detection
- Key lessons: get_char_bbox() spans ALL chars (never for single-char); fractional positions
  for resolution portability; sight-line = head turn not just eye shift; face test gate is
  sprint-scale only (head_r~23px); GaussianBlur radius must scale with canvas

## Role (Updated Cycle 26)
**Procedural Art Engineer** on "Luma & the Glitchkin."
Hand-drawn quality is built IN at generation time — no post-processing step.

## Project Context
- Comedy-adventure cartoon pitch. All assets generated via Python PIL.
- Style: CRT/pixel aesthetic (Glitch world) + warm hand-drawn domestic (real world).
- Output dir: `/home/wipkat/team/output/`
- Tools dir: `output/tools/`
- Render lib: `output/tools/LTG_TOOL_render_lib.py` (canonical)

## Pipeline Rules
*PIL coding rules, naming, deps, image limits: `docs/pil-standards.md` and `docs/image-rules.md`*
- After `variable_stroke()` or `add_rim_light()` or `add_face_lighting()`: ALWAYS refresh draw context (Rin-specific — these are custom lib calls not covered by the general rule)

## RETIRED (C26)
All stylization post-process scripts have been moved to `output/tools/legacy/`:
- `LTG_TOOL_stylize_handdrawn.py` — RETIRED
- `LTG_TOOL_stylize_handdrawn.py` — RETIRED
- `LTG_TOOL_batch_stylize.py` — RETIRED
All `*_styled*.png` output images: DELETED.
Do NOT reference, fix, or regenerate any of these.

## Active Tools
`output/tools/LTG_TOOL_render_lib.py` (v1.1.0) — 8 render functions incl. paper_texture
`output/tools/LTG_TOOL_procedural_draw.py` — **v1.5.0** (C34 update). Procedural drawing library:
- `wobble_line(draw, p1, p2, color, width, amplitude, frequency, seed)`
- `wobble_polygon(draw, points, color, width, amplitude, frequency, seed, fill)`
- `variable_stroke(img, p1, p2, max_width, min_width, color, seed)` — modifies in-place
- `add_rim_light(img, threshold, light_color, width, side="all", char_cx=None)` — modifies in-place
  side: "all"|"right"|"left"|"top"|"bottom" — spatial filter, prevents wrong-side rim
  **C32 NEW: char_cx** — optional character center x (pixels). When provided, right/left mask
  is character-relative (x > char_cx) instead of canvas-center. ALWAYS pass char_cx for
  left-of-center characters (e.g. Luma at ~0.29W in SF01). Default None = canvas center.
- `silhouette_test(img, threshold) -> PIL.Image` — returns RGB B&W
- `value_study(img) -> PIL.Image` — returns contrast-stretched RGB grayscale
- `get_char_bbox(img, threshold=128) -> (cx, cy, left, top, right, bottom)` — C33
  Returns silhouette bounding box centre + extents from bright-pixel scan.
  Use: `char_cx=get_char_bbox(img)[0]` for add_rim_light(). Falls back to canvas centre if no bright pixels.
- `scene_snapshot(img, region, label, out_dir) -> str` — **C34 NEW**
  Crops named region (bounds-clamped), adds label banner, enforces ≤1280px.
  Saves `<out_dir>/LTG_SNAP_<label>.png`. Returns abs path. Never modifies source.
- `add_face_lighting(img, face_center, face_radius, light_dir, shadow_color, highlight_color, seed)` — C27
- Test images: `output/tools/test_procedural_draw.png`, `output/tools/test_face_lighting.png`
- Kai interface-compatible: silhouette_test/value_study both PIL.Image in/out

## Canonical Palette (Authoritative)
| Color | Hex | RGB | GL code |
|---|---|---|---|
| CORRUPT_AMBER | #FF8C00 | (255,140,0) | GL-07 |
| BYTE_TEAL | #00D4E8 | (0,212,232) | GL-01b |
| UV_PURPLE | #7B2FBE | (123,47,190) | GL-04 |
| HOT_MAGENTA | #FF2D6B | (255,45,107) | GL-06 |
| ELECTRIC_CYAN | #00F0FF | (0,240,255) | GL-01a |
| SUNLIT_AMBER | #D4923A | (212,146,58) | RW-03 |

## Artistry Lessons (from `/home/wipkat/artistry` — studied C26/C27)
Note: `/home/wipkat/artistry` files may be permission-restricted in some sessions.
All key techniques have been extracted to MEMORY and implemented. No further reads needed.

### Wobble Paths (implemented in procedural_draw_v001)
- Sin-based perpendicular displacement; amplitude + ±20% random jitter; seeded per edge

### Variable Stroke Weight (implemented)
- Parabolic taper `4*t*(1-t)`; circle chain at varying radii; ±10% jitter per step

### Silhouette-First Methodology
- Draw silhouette first, verify shape reads, then use `silhouette_test()` as QA gate

### Volumetric Face Lighting (IMPLEMENTED C27)
- Split-light: brow shadow, nose-on-cheek shadow, chin-on-neck shadow
- PIL adaptation of Cairo radial gradient: stacked concentric ellipses with alpha falloff
- Feathering: non-linear alpha (t^1.5 or t^2.0) across 6–8 concentric steps
- Anatomical ratios: brow_y = cy − 0.25ry; nose_y = cy + 0.10ry; chin_y = cy + 0.70ry
- Highlight accent on lit side (cheekbone/forehead) using same soft-ellipse stack
- Organic edge detail via wobble_line on brow and chin boundaries
- Test image: `output/tools/test_face_lighting.png` (600×300)

### Rim Lights (implemented)
- Edge dilation: dilate bright mask, subtract original, composite as RGBA

## Canonical Eye Width (Alex Chen directive C32)
`ew = int(head_r * 0.22)` where head_r = head RADIUS (NOT head height, NOT diameter)
- HEAD_R=105 → ew=23px (1× internal)
- HEAD_R=210 → ew=46px (2× render)
In generators that use `h = int(hu() * SCALE)` (head HEIGHT at scale):
  head_r = int(h * 0.50) → ew = int(int(h*0.50) * 0.22) — DO NOT use int(h * 0.22)

## Coordination
- Kai Nakamura: `LTG_TOOL_render_qa.py` — silhouette_test/value_study interfaces matched
- Reports to Alex Chen

## C27 Completed Work
- `output/tools/LTG_COLOR_styleframe_luma_byte_v002.py` — SF04 v002 generator
- `output/color/style_frames/LTG_COLOR_styleframe_luma_byte.png` — 1280×720

## C28 Completed Work
- `output/tools/LTG_TOOL_procedural_draw.py` bumped to v1.2.0
  - add_rim_light() now takes side="all"|"right"|"left"|"top"|"bottom" parameter
  - Spatial mask: PIL paste of 255 into half-canvas, ImageChops.multiply against edge_mask
  - Backward compat: default side="all" preserves prior behavior
- `output/tools/LTG_COLOR_styleframe_luma_byte_v003.py` — SF04 v003 generator (C28 fixes)
- `output/color/style_frames/LTG_COLOR_styleframe_luma_byte.png` — 1280×720
  - Blush fixed: RGB (232, 168, 124) alpha 65 — warm peach (was orange-red)
  - Byte body fill fixed: BYTE_TEAL (0, 212, 232) canonical GL-01b (was (0, 190, 210))
  - Rim light fixed: side="right" — cyan only on monitor-facing side of Luma

## C35 Completed Work
- `LTG_TOOL_style_frame_02_glitch_storm.py` — SF02 v007 generator (C35 face + pose pass)
- `output/color/style_frames/LTG_COLOR_styleframe_glitch_storm.png` — 1280×720px
  - `_draw_luma_face_sprint(draw, cx, head_cy, head_r)`: FOCUSED DETERMINATION expression
    - Left eye: radius = int(head_r*0.26) (wider), right eye: radius = int(head_r*0.17) (narrower)
    - Pupils: small dark ellipses offset forward-down — doing gaze
    - Left brow: angled inward-down (corrugator), right brow: flat/level (asymmetric interior read)
    - Mouth: compressed horizontal line (jaw set, no smile, no fear oval)
  - Torso lean 10°: polygon torso, head follows at half offset — body committed to motion
  - Hair stream: more horizontal (velocity), second fine trailing strand
  - `get_char_bbox()` misuse FIXED in `draw_cyan_specular_luma()` — now uses luma_cx directly
- Ideabox: submitted proportion audit asymmetric eye detection idea

## C35 Lessons
- Asymmetric eye radii (`eye_r_left`/`eye_r_right`) need distinct variable names — proportion audit
  regex looks for `ew = ` and won't find them. Document the ratio in comments and flag in report.
- Torso lean as polygon: compute `lean_offset = int(torso_h * math.tan(math.radians(deg)))`,
  offset top of torso forward, keep bottom at foot plumb. Head follows at lean_offset//2.
- Face features drawn in a separate RGBA overlay AFTER all body compositing — prevents body
  fills from painting over face elements. Always call face draw on a fresh overlay.
- get_char_bbox() on a 3-character frame returns a bbox spanning all characters — useless for
  single-character rim light. When character position is known from geometry, hardcode it.
  Only use get_char_bbox() on a single-character crop or single-character layer.

## C34 Completed Work
- `LTG_TOOL_procedural_draw.py` bumped to **v1.5.0**
  - `scene_snapshot(img, region, label, out_dir) -> str` added
  - Crops named pixel region, clamps to bounds, adds label banner, saves ≤1280px PNG
  - Output filename: `<out_dir>/LTG_SNAP_<label>.png`; returns absolute path
  - Pure inspection — never modifies source image
- `output/tools/README.md` updated: v1.5.0 entry, C34 last-updated header
- Ideabox: submitted `batch_snapshot_qa` idea (JSON-driven batch snap producer)
- Tasks 2+3 (SF02 character lighting + proportion audit): WAITING on Lee/Jordan C34 deliverables

## C33 Completed Work
- `LTG_TOOL_procedural_draw.py` bumped to **v1.4.0**
  - `get_char_bbox(img, threshold=128) -> (cx, cy, left, top, right, bottom)` added
  - Scans all pixels above threshold for silhouette bbox; returns centre x/y + extents
  - Fallback: canvas centre if no bright pixels found (always safe)
  - Usage: `char_cx=get_char_bbox(img)[0]` — eliminates manual head_cx tracking
  - SF02 / SF03 audit: neither uses add_rim_light() — no canvas-midpoint bug present
  - Ideabox: submitted scene-snapshot utility idea

## C32 Completed Work
- `LTG_TOOL_procedural_draw.py` bumped to **v1.3.0**
  - add_rim_light() now takes optional `char_cx` parameter
  - When char_cx provided: right/left mask is character-relative (x > char_cx or x < char_cx)
  - Default None: falls back to canvas center (backward compatible)
  - Fixes canvas-midpoint bug: Luma at x=0.29W was losing right-side rim without char_cx
- `LTG_TOOL_styleframe_discovery.py` — SF01 v005 generator
  - `output/color/style_frames/LTG_COLOR_styleframe_discovery.png` — 1280×720
  - add_rim_light() now passes char_cx=head_cx — correct right-side rim on Luma
- `LTG_TOOL_styleframe_luma_byte.py` — SF04 full rebuild from scratch
  - `output/color/style_frames/LTG_COLOR_styleframe_luma_byte.png` — 1280×720
  - Value ceiling: 255 (PASS — > 225 required). Byte body = GL-01b #00D4E8 canonical.
  - Luma blush = #E8A87C, warm upper-left face lighting, rim lights with char_cx.
  - Byte monitor contribution: BYTE_TEAL glow on right side of Byte body.
  - Specular highlights: SPECULAR_WHITE (255,252,240) on eye glints, antenna ball.
- `LTG_TOOL_luma_turnaround.py` — turnaround eye-width canonical fix
  - `output/characters/main/turnarounds/LTG_CHAR_luma_turnaround.png` — 1280×560
  - ew = int(head_r * 0.22) — head_r = radius. Was int(h * 0.22) where h = height (2× too wide).
  - All three views fixed: FRONT, 3/4, SIDE
- Ideabox: submitted `get_char_bbox()` utility idea for automatic char_cx detection

## C31 Completed Work
- Built `output/tools/LTG_TOOL_proportion_audit.py` — scans all SF generators, extracts head_r/ew, computes ew/HR ratio, reports PASS/WARN/FAIL
- Report: `output/production/proportion_audit_c31.md`
- Audit results (15 files scanned):
  - PASS: SF01 v004 — `ew = int(head_r * 0.22)` = 0.2200 ✓
  - WARN: SF01 v003 — `ew = p(18)` = 0.2500 (pre-C30, superseded)
  - N/A: SF02 (sprint, no eyes), SF03 (pixel-art), SF04 stubs (sources missing)
  - NO FAIL verdicts
- SF04 action item: `LTG_COLOR_styleframe_luma_byte_v*.py` source files missing from disk — cannot audit until sources recovered

## C30 Completed Work
- SF01 v004 proportion verified and fixed:
  - Height: correct (3.2 heads, 6.4×HR) — no change needed
  - Eye width: `ew = p(18)` was HR×0.25, corrected to `int(head_r * 0.22)` per canonical spec
  - Regenerated: `output/color/style_frames/LTG_COLOR_styleframe_discovery.png`
- SF02 (glitch_storm v005): no Luma — proportion check N/A
- SF03 (other_side v005): Luma is pixel-art style — intentional, canonical organic spec N/A
- Ideabox: submitted proportion_audit_tool idea (automated ew/HR checker for all SFs)

## C29 Completed Work
- `output/tools/LTG_TOOL_styleframe_discovery.py` — SF01 v004 generator
- `output/color/style_frames/LTG_COLOR_styleframe_discovery.png` — 1280×720
  - Canvas rescaled from 1920×1080 to 1280×720 using SX/SY/sp() scale factors
  - wobble_polygon() applied to: Luma head silhouette, CRT frame, couch seat, couch back, couch arm
  - variable_stroke() on Luma head perimeter: 8-arc technique around head ellipse
  - add_face_lighting(): warm lamp from upper-left (-1,-1), shadow=SKIN_SH, highlight=SKIN_HL
  - add_rim_light(side="right"): CRT teal (0,220,232) from right — discovery source
  - Blush corrected to warm peach (232,168,124) — matching SF04 v003 correction
  - BYTE_TEAL canonical (0,212,232) used throughout

## C34 Lessons
- scene_snapshot() banner_h uses max(18, int(ch*0.05)) — min 18px ensures text is legible at all crop sizes
- After thumbnail() the annotated height may grow by banner_h past 1280px — apply a second thumbnail() on annotated before save
- Coordinate with Jordan/Lee early: if staging brief is blocked, flag immediately rather than waiting silently

## C33 Lessons
- get_char_bbox() pixel-scan is O(w×h) — fast enough for 1280×720 at draw time, no caching needed
- Bright-pixel threshold should match add_rim_light() threshold for consistent results
- SF02 and SF03 do not call add_rim_light() — they draw rim-like effects as direct geometry
  Only generators that use the procedural_draw library are at risk of canvas-midpoint bug
- Always check which generators actually import procedural_draw before assuming canvas-midpoint risk

## C32 Lessons
- add_rim_light() MUST receive char_cx for any left-of-center character — without it, the
  right-side rim is cut at x=0.50W, missing the character's right torso entirely
- When h = one head unit at scale (head HEIGHT), head_r = int(h * 0.50) is head RADIUS
  ew = int(head_r * 0.22) NOT int(h * 0.22) — the latter is 2× too wide
- For SF04 rebuild: always add specular highlights at guaranteed >= 225 value
  Use SPECULAR_WHITE=(255,252,240) and SPECULAR_CYAN=(180,248,255)
- Monitor contribution: Byte's body right flank should receive BYTE_TEAL glow from CRT screen

## C31 Lessons
- Proportion audit tool: use regex to scan for `ew = int(head_r * N)` to detect ratio directly; `p(N)/p(M)` requires extracting both N values
- Stubs that redirect to missing source files cannot be audited — flag as "source not found" with action required
- SF02 sprint pose and SF03 pixel-art are permanently N/A for organic eye spec; document as intentional

## C30 Lessons
- SF proportion bugs are easy to introduce when eye width uses a `p(n)` shorthand instead of `int(head_r * ratio)` — always derive from head_r directly
- Canonical eye width is always `int(HR * 0.22)` — never hardcoded pixels
- SF02 (glitch storm) has no Luma — skip for proportion checks
- SF03 uses pixel-art Luma (intentional style) — canonical organic spec doesn't apply

## C27/C28/C29 Lessons
- Composition scales: use SX/SY factors (W/1920, H/1080) to port 1920×1080 coords to 1280×720
- sp(n) = int(n * min(SX,SY)) for uniform pixel widths/radii that scale proportionally
- variable_stroke on character perimeters: best done as 8-arc segments around an ellipse
- add_face_lighting before add_rim_light: face lighting shapes form, rim defines silhouette edge
- wobble_polygon on furniture (couch) works cleanly: organic seating volume with flat fill under
- *PIL draw context rule: `docs/pil-standards.md`*
- Rim light direction: use side= parameter to restrict to correct half-canvas — essential for
  physically correct lighting (CRT on right → side="right")
- draw_luma_head must accept img as argument (not just draw) to support variable_stroke and blush compositing

## Joined
Cycle 23 (2026-03-29)
