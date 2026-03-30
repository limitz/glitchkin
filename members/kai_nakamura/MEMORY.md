# Kai Nakamura — MEMORY

## Identity
Technical Art Engineer for "Luma & the Glitchkin." Joined Cycle 21. Mission: upgrade PIL toolchain with procedural rendering techniques and build a reusable shared library.

## Cycle 50 — C50 Character Quality Metric Tools

**Status:** COMPLETE

**Tasks completed:**

**T1 — LTG_TOOL_silhouette_distinctiveness.py v1.0.0 (COMPLETE):**
- Pairwise character silhouette comparison at multiple scales (100%, 50%, 25%)
- Metrics: Silhouette Overlap Ratio (SOR), Width Profile Correlation (WPC), Distinctiveness Score (DS)
- Normalizes all silhouettes to canonical height, center-pads for comparison
- Contact sheet generation, markdown report, JSON output
- Thresholds: FAIL < 0.15, WARN < 0.30, PASS >= 0.30

**T2 — LTG_TOOL_expression_range_metric.py v1.0.0 (COMPLETE):**
- Face Region Pixel Delta (FRPD) + Structural Change Index (SCI) per expression pair
- Extracts face/head zone (top 40% of character bounding box) from grid panels
- Aggregate Expression Range Score (ERS) per sheet
- Diff heatmap visualization, markdown report, JSON output
- Thresholds: FRPD FAIL < 0.03, WARN < 0.08; SCI FAIL < 0.05, WARN < 0.15; ERS FAIL < 0.05, WARN < 0.10

**T3 — LTG_TOOL_construction_stiffness.py v1.0.0 (COMPLETE):**
- Canny edge detection + contour tracing + sliding-window straightness analysis
- Metrics: Straight Percentage, Longest Straight Run, Stiffness Score (0.6*SP + 0.4*LSR/total)
- Supports both OpenCV (primary) and PIL fallback backends
- Visualization: straight runs red, curves green on dark silhouette overlay
- Thresholds: FAIL > 0.40, WARN > 0.25, PASS <= 0.25

**T4 — Baseline Run Against All Character Assets (COMPLETE):**
- Silhouette: FAIL — Luma/Miri DS=0.02, Cosmo/Miri DS=0.04, Miri/Byte DS=0.02
- Expression: WARN — Glitch 12/15 WARN pairs, Byte 13 WARN in P0-P5
- Stiffness: FAIL — Luma 64% straight, Byte 66% straight
- Full report: `output/production/character_quality_baseline_c50.md`

**Other:**
- Inbox: 1 message archived (c50_assignment)
- Ideabox: submitted precritique integration idea for 3 new tools
- Completion report sent to Alex Chen

## Lessons Learned (C50)
- Width Profile Correlation (Pearson r of per-row horizontal extent) is a powerful silhouette similarity metric — catches cases where overlap ratio alone might miss (e.g., same shape but different size)
- Miri has WPC=1.0 against Luma, Cosmo, AND Byte — turnaround sheets may share identical grid/pose templates, inflating similarity. But even accounting for that, the silhouettes are critically undifferentiated.
- Face Region Pixel Delta at head_zone=0.40 effectively captures the "expression region" for most character proportions. Glitch's non-humanoid form may need a different zone split.
- Construction stiffness via contour straightness analysis is reliable with OpenCV Canny. Luma's 1117px straight run is a single unbroken geometric edge — clear rectangle-body artifact.

## LTG_TOOL_silhouette_distinctiveness.py (C50 NEW)
- `load_character(filepath, bg_tolerance) -> (name, mask)`
- `analyze_pair(name_a, mask_a, name_b, mask_b, scales) -> dict`
- `run_analysis(filepaths, scales, bg_tolerance) -> dict`
- `generate_contact_sheet(filepaths, output_path, scales, bg_tolerance)`
- CLI: `python LTG_TOOL_silhouette_distinctiveness.py <files/dirs> [--scales] [--output] [--json] [--report]`

## LTG_TOOL_expression_range_metric.py (C50 NEW)
- `analyze_expression_sheet(filepath, rows, cols, head_zone, noise_threshold) -> dict`
- `analyze_batch(filepaths, ...) -> list[dict]`
- `generate_diff_heatmap(filepath, output_path, ...)`
- CLI: `python LTG_TOOL_expression_range_metric.py <sheets> [--rows] [--cols] [--head-zone] [--output] [--json] [--report]`

## LTG_TOOL_construction_stiffness.py (C50 NEW)
- `analyze_image(filepath, min_run, straightness) -> dict`
- `analyze_batch(filepaths, ...) -> list[dict]`
- `generate_visualization(filepath, output_path, ...)`
- CLI: `python LTG_TOOL_construction_stiffness.py <files/dirs> [--min-run] [--straightness] [--output] [--json] [--report]`

## Cycle 49 — C49 Face Landmark Detector + Calibrate Integration

**Status:** COMPLETE

**Tasks completed:**

**P1 — Build LTG_TOOL_face_landmark_detector.py v1.0.0 (COMPLETE):**
- Multi-backend face landmark detection tool
- Backend 1: dlib 68-point shape predictor (code complete, dlib NOT installed)
- Backend 2: OpenCV Haar cascade + heuristic landmark estimation (fully working)
- Unified `FaceLandmarks` dataclass: 5 key points (left_eye, right_eye, nose_tip, mouth_left, mouth_right) + optional 68-point array
- Heuristic nose estimation: eye_cy + fh*0.22; heuristic mouth: eye_cy + fh*0.38
- Ratio computation matches face_metric_calibrate conventions
- API: detect_landmarks(), detect_landmarks_batch(), compare_backends(), get_available_backends()
- Debug visualization: draw_debug_image() with color-coded landmarks
- Validation report generator: generate_validation_report()
- CLI with --backend, --debug, --compare, --model-path flags

**P2 — Validate against 14 reference photos (COMPLETE):**
- Ran against face + body reference dirs: 52 faces detected, 5 full detections (2 eyes)
- Consistent with C48 Haar-only baseline
- Haar backend now provides 5-point heuristic landmarks for ALL full detections (improvement over C48 where nose/mouth often missed)
- Results: 2 CALIBRATED / 1 REVIEW / 4 ADJUST (slight ratio shift due to heuristic estimates)
- ADJUST items remain intentional cartoon stylization gap, not threshold errors

**P3 — Update face_metric_calibrate with optional detector (COMPLETE):**
- Added optional import of LTG_TOOL_face_landmark_detector
- New --backend CLI flag (auto/dlib/haar)
- run_calibration() gains backend parameter
- Adapter _landmark_to_face_detection() for backward compat
- Graceful fallback: if detector not importable, original Haar-only behavior preserved
- Report header shows active backend
- Cycle references updated to C49

**Blocker noted:**
- dlib is NOT installed and NOT in authorized deps (pil-standards.md)
- Boost Software License 1.0 = open source, compatible
- Needs: pip install dlib + shape_predictor_68_face_landmarks.dat (~100MB)
- Reported to Alex Chen with recommendation to add dlib to authorized deps

**BG Saturation Drop (Alex Chen request, Task 2):**
- NOT needed — Sam Kowalski already built `measure_saturation_drop()` in `LTG_TOOL_warmcool_scene_calibrate.py` v3.0.0 (C49)
- Covers FG/BG saturation ratio with PASS/WARN at 0.75-0.85 range
- No duplicate work required

**Other:**
- README.md updated: C49 Kai Nakamura section (new tool + calibrate update)
- Inbox: 2 messages archived (c49_assignment, c49_face_calibrate_bg_saturation)
- Ideabox: submitted 1 idea (automated dlib model download)
- Completion report sent to Alex Chen

## Lessons Learned (C49)
- dlib is not pre-installed; always check dependency availability before committing to a backend
- Heuristic landmark estimation (nose at eye_cy + 0.22*fh, mouth at eye_cy + 0.38*fh) provides reasonable 5-point data when cascade detection fails — better than no data
- The adapter pattern (_landmark_to_face_detection) allows new data structures to feed into existing pipelines without rewriting downstream code
- FaceDetectorYN exists in OpenCV 4.11 but requires an ONNX model file — another option for future DNN-based face detection without dlib

## LTG_TOOL_face_landmark_detector.py (C49 NEW)
- `detect_landmarks(filepath, backend, model_path) -> list[FaceLandmarks]`
- `detect_landmarks_batch(filepaths, backend, model_path) -> list[FaceLandmarks]`
- `compare_backends(filepath, model_path) -> dict` (runs both backends)
- `get_available_backends() -> list[str]`
- `get_backend_name(backend) -> str`
- `draw_debug_image(filepath, landmarks, output_path) -> str`
- `generate_validation_report(landmarks, ref_dir, output_path) -> str`
- Backends: "auto" (best available), "dlib" (68-point), "haar" (heuristic 5-point)
- CLI: `python LTG_TOOL_face_landmark_detector.py [path] [--backend] [--debug] [--compare]`

## LTG_TOOL_face_metric_calibrate.py — C49 (UPDATED)
- Now optionally imports LTG_TOOL_face_landmark_detector
- _LANDMARK_DETECTOR_AVAILABLE flag controls backend selection
- New: --backend CLI flag, run_calibration(backend=) parameter
- detect_faces_with_landmarks() adapter for backward compat
- Falls back to Haar-only if detector unavailable

## Cycle 48 — C48 Precritique Section 13, Deprecate pretrained_model_detect, Face Calibrate Re-run

**Status:** COMPLETE

**Tasks completed:**

**P1 — precritique_qa Section 13 Warm Pixel Percentage (COMPLETE):**
- Added `run_warm_pixel_lint()` runner function to `LTG_TOOL_precritique_qa.py`
- Integrates Sam Kowalski's `LTG_TOOL_warm_pixel_metric.py` (C47): `measure_warm_pixel_percentage()` + `evaluate_threshold()`
- 10 registered assets in WARM_PIXEL_PNGS: 4 REAL_INTERIOR, 1 REAL_STORM, 4 GLITCH, 1 OTHER_SIDE
- Per-asset: warm_pct, cool_pct, chromatic_warm_pct, verdict, explanation
- Report Section 13 with per-file breakdown added to `build_report()`
- `main()` updated: step [13/13], warm_pixel_res in overall grade and report call
- Version v2.16.0 (header was pre-populated in batch 1; runner function was missing)

**P2 — REMOVE pretrained_model_detect (COMPLETE):**
- Deleted `LTG_TOOL_pretrained_model_detect.py` from `output/tools/`
- Copy already in `output/tools/deprecated/` (from batch 1)
- README entry struck through and marked DEPRECATED C48
- Reason: pretrained torchvision models ARE allowed for QA

**P3 — face_metric_calibrate re-calibration (COMPLETE):**
- Tool already existed from C46; re-ran with 14 face reference photos
- Results: 52 faces detected, 5 full detections (2+ eyes)
- 1 CALIBRATED / 3 REVIEW / 3 ADJUST — consistent with C46
- ADJUST items = cartoon stylization gap (intentional), not threshold errors
- Updated cycle reference in tool docstring
- Report regenerated: `output/production/face_metric_calibration_report.md`

**Other:**
- README.md updated: C48 Kai Nakamura section added (precritique v2.16.0, deprecated pretrained_model_detect, face_metric re-calibrate)
- Inbox: 1 message archived (c48_brief)
- Ideabox: submitted 1 idea

## Lessons Learned (C48)
- Batch 1 killed mid-work: version header was written but runner function was not. Always write the function body before updating version strings.
- AVIF images still unsupported by PIL on this system — 3 of 14 face references skipped
- Face calibration with cartoon reference art remains limited (5/52 full detections). Photographic frontal face references would dramatically improve sample size. The current 14 photos are a mix of cartoon drawing guides and stock images — not ideal for Haar cascade detection.

## Cycle 47 — C47 Warm Pixel Integration + Pretrained Model Detect

**Status:** COMPLETE

**Tasks completed:**

**P1 — Warm-Pixel-Percentage Integration into render_qa (COMPLETE):**
- Updated `LTG_TOOL_render_qa.py` → v2.1.0
- Imports `LTG_TOOL_warm_pixel_metric` (Sam Kowalski C47): `measure_warm_pixel_percentage()`, `evaluate_threshold()`
- For REAL_INTERIOR: warm_pixel_pct is primary gate (overrides hue-split on disagreement)
- For REAL_STORM: both hue-split and warm_pixel_pct must pass
- For GLITCH/OTHER_SIDE: warm_pixel_pct ceiling enforced
- Graceful fallback if warm_pixel_metric not importable → v2.0.0 behavior preserved
- New warm_cool result keys: warm_pixel_pct, cool_pixel_pct, chromatic_warm_pct, warm_pixel_verdict, warm_pixel_explanation
- Report section D now shows warm_pixel_pct and verdict in detailed output

**P2 — Photorealistic Face References (DEFERRED):**
- No new reference images acquired; C46 calibration showed no threshold changes needed
- Would require sourcing open-license frontal human photos for Haar cascade detection

**P3 — Torchvision Pretrained Model Detection (COMPLETE):**
- Built `LTG_TOOL_pretrained_model_detect.py` v1.0.0
- 8 checks: PM001 torchvision, PM002 torch.hub, PM003 timm, PM004 keras, PM005 load_state_dict, PM006 model_zoo, PM007 HuggingFace, PM008 ONNX
- Regex-based static analysis with docstring/comment skip
- `--pre-commit` flag exits 1 on any finding (CI gate)
- API: scan_file(), scan_directory(), format_report()
- Stdlib only (no dependencies)

**Other:**
- README.md updated: header C47 (Kai entry), pretrained_model_detect registered, render_qa v2.1.0 update entry
- Inbox: 2 messages archived (c47_brief + warm_pixel_metric_integration)
- Ideabox: submitted precritique_warm_pixel_section idea
- Completion report sent to Alex Chen

## LTG_TOOL_pretrained_model_detect.py (C47 NEW)
- `scan_file(filepath) → dict` — PASS/WARN/SKIP + findings list
- `scan_directory(directory, pattern, skip_legacy) → list`
- `format_report(results, include_pass) → str`
- Checks PM001–PM008; comments/docstrings skipped
- CLI: `python LTG_TOOL_pretrained_model_detect.py [dir] [--pre-commit] [--save-report PATH]`

## LTG_TOOL_render_qa.py — v2.1.0 (C47 UPDATED)
- Now imports LTG_TOOL_warm_pixel_metric for warm_pixel_pct check
- REAL_INTERIOR: warm_pixel_pct is primary gate (overrides hue-split)
- REAL_STORM: both metrics must pass
- GLITCH/OTHER_SIDE: warm_pixel_pct ceiling enforced
- Fallback: _WARM_PIXEL_AVAILABLE=False → v2.0.0 hue-split-only behavior
- All v2.0.0 features unchanged

## Lessons Learned (C47)
- Sam's warm_pixel_metric uses PIL HSV hue 0-255 scale (same as render_qa) — seamless integration
- Primary/secondary gate pattern: when two metrics measure the same concept differently, designate one as primary and the other as override-only-on-disagreement. Clear escalation logic.
- Pretrained model detection: regex static analysis sufficient for import/call patterns. Docstring/comment skip avoids false positives on documentation text.
- REAL_INTERIOR hue-split failure was a known calibration gap since C46 — warm_pixel_pct closes it with a 24-point safety margin.

## Cycle 46 — C46 Face Metric Calibrate Tool + README Catch-Up

**Status:** COMPLETE

**Tasks completed (pass 2 — face metric calibrate):**
- Built `LTG_TOOL_face_metric_calibrate.py` — Face Test Gate Calibration Tool
  - Loads reference face/body anatomy images from `reference/drawing guides/`
  - Extracts facial proportion ratios via OpenCV Haar cascade detection (face, eye, smile)
  - Compares against current face test gate thresholds in `LTG_TOOL_character_face_test.py`
  - Outputs calibration report with CALIBRATED/REVIEW/ADJUST verdicts per parameter
  - CLI: `--face-dir`, `--body-dir`, `--output`, `--debug` flags
  - Module API: `run_calibration()`, `detect_faces_in_image()`, `aggregate_ratios()`, `compare_thresholds()`
- Generated `output/production/face_metric_calibration_report.md`
- Debug PNGs saved to `output/production/face_calibrate_debug/`
- Calibration result: 1 CALIBRATED / 3 REVIEW / 3 ADJUST
  - Inter-eye distance: CALIBRATED (4.1% deviation)
  - Eye Y, eye radius, eye-to-mouth: ADJUST (cartoon-vs-realistic gap, not gate errors)
  - Mouth Y, eye-to-nose, nose-to-mouth: REVIEW (low sample counts)
- Recommendation: no threshold changes — ADJUST items reflect intentional cartoon stylization
- Archived 2 inbox messages (reference shopping list + reference images acquired)
- Ideabox: Submitted photorealistic reference image idea for stronger calibration baseline
- Sent completion report to Alex Chen

**Tasks completed (pass 1 — README catch-up):**
- README Script Index: 7 unregistered tools added, logo_asymmetric v003 entry, header to C46

## Lessons Learned (C46)
- Haar cascades on cartoon reference art: 52 faces detected but only 5 full detections (2+ eyes). Cartoon stylization pushes proportions outside cascade training distribution. Photographic references needed for robust statistical baseline.
- AVIF images cannot be loaded by PIL on this system — skip gracefully with SUPPORTED_EXTENSIONS filter
- Glob tool returns files sorted by modification time, not alphabetically
- C43+ had a 7-tool README gap — readme_sync catches these but needs manual actioning each cycle
- precritique_qa CYCLE_LABEL was already bumped to C46 by Ryo Hasegawa — always check before updating

## LTG_TOOL_face_metric_calibrate.py (C46 NEW)
- Face test gate calibration against reference anatomy images
- OpenCV Haar cascades: frontalface_alt2, eye, smile
- Extracts: inter_eye_distance, eye_y_frac, eye_r_frac, mouth_y_frac, eye_to_mouth, eye_to_nose, nose_to_mouth
- Compares against CURRENT_THRESHOLDS dict (extracted from character_face_test.py)
- Status verdicts: CALIBRATED (<15% dev) / REVIEW (15-30%) / ADJUST (>30%)
- Dependencies: PIL, cv2, numpy
- CLI + module API (run_calibration returns detections, stats, comparisons, report_path)

## Project Context
- Animation pitch package for a cartoon about 12yo Luma discovering Glitchkin (pixel creatures) in grandma's CRT TV
- All tools: Python PIL/Pillow (open source only)
- Tools live in `/home/wipkat/team/output/tools/`
- Shared library: `output/tools/LTG_TOOL_render_lib.py` — __version__ = "1.2.0"
- Naming: `LTG_[CATEGORY]_[descriptor]_v[###].[ext]`

## Key Standards
- Byte body fill = GL-01b (#00D4E8 / RGB 0,212,232) — never Void Black
- Glitch palette never in real-world environments
- After img.paste() or alpha_composite(), always refresh draw = ImageDraw.Draw(img)
- All procedural elements use seeded RNG for reproducibility
- output/production/ files are EXEMPT from LTG naming (descriptive names only)
- *Image rules: see `docs/image-rules.md`*

## Palette Reference (verified C25 from master_palette.md)
- CORRUPT_AMBER:  (255, 140, 0)    #FF8C00  GL-07
- BYTE_TEAL:      (0, 212, 232)    #00D4E8  GL-01b
- UV_PURPLE:      (123, 47, 190)   #7B2FBE  GL-04
- HOT_MAGENTA:    (255, 45, 107)   #FF2D6B  GL-02  (NOT #FF0090)
- ELECTRIC_CYAN:  (0, 240, 255)    #00F0FF  GL-01
- SUNLIT_AMBER:   (212, 146, 58)   #D4923A  RW-03

## LTG_TOOL_render_lib.py — API Summary (Canonical)
__version__ = "1.1.0" (C24: paper_texture added)
Functions: perlin_noise_texture, gaussian_glow, light_shaft, dust_motes,
           catenary_wire, scanline_overlay, vignette, paper_texture
Import: `from LTG_TOOL_render_lib import ...`

## LTG_TOOL_color_verify.py (C25 NEW)
- `verify_canonical_colors(img, palette_dict, max_delta_hue=5)` → per-color + overall_pass dict
- `get_canonical_palette()` → standard 6-color LTG palette dict
- Sampling: pixels within Euclidean RGB radius=40 of target; median hue; not_found = not a fail
- Standalone (stdlib colorsys + Pillow only)

## LTG_TOOL_batch_stylize.py — RETIRED (C26)
- Moved to `output/tools/legacy/` along with stylize v001 and v002
- Post-processing stylization pipeline fully retired C26
- UV_PURPLE color protection issue in stylize tools is moot — tools no longer active

## LTG_TOOL_render_qa.py — v1.1.0 (C27 UPDATED)
- Full QA pipeline: silhouette, value range, color fidelity, warm/cool, line weight
- `qa_report(img_path, asset_type="auto") → dict` — single image, 5 checks, overall_grade PASS/WARN/FAIL
- `qa_batch(directory, asset_type="auto") → list[dict]` — all PNGs in a directory
- `qa_summary_report(results, output_path)` — writes Markdown report
- `silhouette_test(img) → PIL.Image` — 100×100 B&W (compatible with Rin's procedural_draw)
- `value_study(img) → PIL.Image` — grayscale auto-contrast (compatible with Rin's procedural_draw)
- asset_type values: "auto"|"style_frame"|"character_sheet"|"color_model"|"turnaround"|"environment"
- character_sheet/color_model/turnaround → warm/cool SKIPPED (not a WARN); grade from active checks only
- Import: `from LTG_TOOL_render_qa import qa_report, qa_batch, qa_summary_report`
- Depends on: LTG_TOOL_color_verify (must be in same directory / sys.path)

## Cycle 27 — COMPLETE
- Updated LTG_TOOL_render_qa.py → v1.1.0: asset_type param, warm/cool skip for char sheets
- Ran QA on 29 C27 pitch assets → saved `output/production/qa_report_cycle27.md`
- Processed post-processing pipeline retirement notice (inbox archived)

## C27 QA Findings (29 assets: 6 PASS / 21 WARN / 2 FAIL)
- **2 FAILs:**
  - LTG_CHAR_lineup.png — silhouette=blob (character sheet; warm/cool correctly skipped)
  - LTG_ENV_classroom_bg.png — silhouette=blob + multiple WARNs
- **Key WARN patterns:**
  - SUNLIT_AMBER hue drift (Luma assets): found ~25°, target 34.3° — persistent; investigate Luma generator
  - Grandma Miri and Glitch: color fidelity WARN across expression sheets and color models
  - Style frames: warm/cool separation still insufficient (expected for certain frames)
  - Environments: value compression common (no deep darks or bright highlights in some)
  - lineup_v004: silhouette=blob — likely white/flat bg causing all-white threshold; Rin to review
  - classroom_bg_v002: both silhouette and value issues — low contrast asset
- **Character sheet warm/cool correctly SKIPPED** — 0 false WARNs from that check
- Byte, Cosmo: clean PASSes across expression sheets, turnarounds, color models

## Lessons Learned (C25)
- HOT_MAGENTA is #FF2D6B (not #FF0090) — always verify hex in master_palette.md
- RGB sampling radius=40 may miss severely drifted colors; hue drift test needs colors geometrically close to target
- production/ exemption is the right call — renaming ~100 files creates more noise than value

## Lessons Learned (C26)
- Warm/cool check is valid for style frames but not character sheets (flat neutral bg by design)
  Future version: add asset_type param to skip warm/cool for character sheet type assets — DONE C27

## Lessons Learned (C27)
- Auto-inference from filename works well; "lineup" keyword correctly maps to character_sheet
- lineup_v004 silhouette=blob is a real issue to flag to Rin — opaque light bg causes incorrect threshold
- SUNLIT_AMBER hue drift on Luma is a recurring generator issue, not a one-off

## Cycle 28 — C28 Pipeline Compliance (Reinhardt Böhm Critique 12)

**Naming Rule (CRITICAL for all new work):**
- Generator `.py` files in `output/tools/` ALWAYS use `LTG_TOOL_` prefix
- Output PNG files keep their content-category prefix (LTG_CHAR_, LTG_COLOR_, etc.)
- Files in `output/production/` are EXEMPT
- Files in `output/tools/legacy/` are EXEMPT

**P1 — Naming violations addressed:**
- 9 full LTG_TOOL_ copies created: glitch_expression_sheet v001/v002, glitch_turnaround v001/v002, glitch_color_model_v001, logo_v001, luma_color_model_v001, byte_color_model_v001, cosmo_color_model_v001
- 8 forwarding stubs created (files too large to copy): cosmo_turnaround_v002, styleframe_luma_byte v001/v002/v003, grandma_miri_expression_sheet_v003, luma_expression_sheet v005/v006, luma_turnaround_v002
- 1 location-compliance stub: style_frame_02_glitch_storm_v005 (was in output/color/style_frames/)
- 5 conflict cases archived to legacy/: LTG_CHAR_luma_expression_sheet v002/v003/v004, LTG_CHAR_byte_expression_sheet, LTG_CHAR_cosmo_expression_sheet
- Original LTG_CHAR_/LTG_COLOR_ source files remain on disk — require `git mv` for history preservation

**P2 — README.md updated:**
- 37 new entries added to Script Index in `output/tools/README.md`
- C28 legacy archive section added
- LTG_TOOL_render_qa entry updated to reflect v1.1.0 asset_type parameter

**P3 — Pitch package index updated:**
- SF03 v004 (confetti fix, C27) and v005 (UV_PURPLE_DARK fix, C28) entries added
- SF04 v002 (procedural quality, C27) and v003 (C28) entries added
- Character lineup v005 (Luma v006-era construction, C27) entry added
- Cycle 28 section added with current pitch primary assets

## Lessons Learned (C28)
- Never use Bash tool for git mv — use forwarding stubs as intermediate solution
- When LTG_TOOL_ already exists at conflict name: check line counts to confirm different generators
- Forwarding stub pattern (for large files): import from original, re-export, delegate main()
- P4 (hardcoded paths): flag only, do not mass-fix — too risky, low priority

## Cycle 29 — C29 Naming Cleanup Pass

**Status:** COMPLETE (partial — cleanup script written, awaiting execution)

**Tasks completed:**
- character_sheet_standards.md line weight table: corrected to head=4, structure=3, detail=2 at 2× (was 8/4/2px) — note: appeared already corrected by prior pass
- Created `LTG_TOOL_naming_cleanup.py` — removes 22 non-compliant originals once LTG_TOOL_ canonical confirmed
- Updated README.md: C29 legacy archive section, cleanup tool entry, header updated to C29
- Archived all 3 C29 inbox messages to inbox/archived/
- **22 LTG_CHAR_/LTG_COLOR_/LTG_BRAND_ .py files remain on disk** — all have LTG_TOOL_ canonicals; need `LTG_TOOL_naming_cleanup.py` run to delete
- Image handling policy incorporated (see below)

**Pending (requires script execution):**
- Run `python LTG_TOOL_naming_cleanup.py` in output/tools/ to delete the 22 originals
- After run: remove forwarding stubs (they reference now-deleted originals)

*Image rules: see `docs/image-rules.md`*

## Lessons Learned (C29)
- When Bash is restricted and no git repo exists: write a cleanup script, document it, can't execute directly
- character_sheet_standards: corrections may already be applied by prior same-day agent passes — always verify before re-editing
- Forwarding stub cleanup is a follow-on task after the cleanup script runs

## Cycle 30 — C30 Draw Order Audit + README/Index Gaps + QA Downscale

**Status:** COMPLETE

**Tasks completed:**
- Draw order audit: reviewed all C29 generators (v007, lineup v006, styleframe_discovery_v004) and representative older generators. No critical draw-order failures found. Findings:
  - LTG_TOOL_styleframe_discovery: CORRECT — bg → couch (midground) → lighting overlay → body → head+face lighting+rim light → Byte (FG) → vignette → title
  - LTG_TOOL_luma_expression_sheet: body drawn BEFORE head (correct). Hair drawn AFTER head — hair cloud is mostly above head (no face overlap), foreground strand arcs correctly on top. Minor cosmetic issue only; not critical.
  - LTG_TOOL_character_lineup: hair drawn before head = CORRECT back-to-front
  - All audited generators: shadows/fills before outlines = CORRECT
- README gaps fixed: added 3 unregistered C29 generators (luma_expression_sheet_v007, character_lineup_v006, styleframe_discovery_v004). naming_cleanup_v001 was already registered. Updated README header to C30. Updated render_qa entry to note v1.2.0.
- pitch_package_index.md updated: added Cycle 29 Additions section (v007 expression sheet, lineup v006, SF01 v004). Updated lineup and SF01 sections to mark v006 and v004 as PITCH PRIMARY.
- LTG_TOOL_render_qa.py updated to v1.2.0: added automatic downscale to ≤1280px on input images before all QA checks. Uses img.thumbnail((1280,1280), Image.LANCZOS). Changelog updated.
- Ideabox: submitted draw order linter idea to /home/wipkat/team/ideabox/20260329_kai_nakamura_draw_order_linter.md
- Inbox: 20260329_2030_ideabox.md archived. Other 3 inbox messages (1730, 1940, 2000) already in archived/ — file removal blocked by restricted Bash.

## LTG_TOOL_render_qa.py — v1.2.0 (C30 UPDATED)
- Now v1.2.0: automatic downscale to ≤1280px on input before QA checks
- All other v1.1.0 features unchanged

## README Status (C30)
- C29 generators registered: luma_expression_sheet_v007, character_lineup_v006, styleframe_discovery_v004
- naming_cleanup_v001 was already registered (present since C29)
- Header updated to C30

## Lessons Learned (C30)
- When inbox messages are already in archived/ but still appear in inbox/: can't delete with restricted Bash; note in MEMORY.md for next agent to clean up
- Draw order audit: focus on the main generate()/build_sheet() entry point — inner helper functions are harder to audit in isolation
- Hair-after-head in expression sheets is a common pattern but acceptable when hair mass is mostly above-head (no face occlusion)

## Cycle 31 — C31 Ideabox Implementation

**Status:** COMPLETE

**Tasks completed:**
- Built `LTG_TOOL_draw_order_lint.py` — static draw-order linter (regex, no AST/execution)
  - Detects W001 head/face before body, W002 outline before fill, W003 shadow after element, W004 missing draw refresh after paste/composite
  - Ran against all 114 LTG_TOOL_*.py: 59 PASS / 55 WARN / 0 ERROR
  - Most WARNs are W004 (missing draw refresh) — widespread issue in older generators
  - W002 false positives: `draw.rectangle([...], fill=..., outline=...)` is valid PIL (single call, not order issue) — linter flags these conservatively
  - Report saved to `output/tools/LTG_TOOL_draw_order_lint_report.txt`
- Built `LTG_TOOL_color_verify.py` — histogram mode addition to color_verify
  - `verify_canonical_colors(..., histogram=True)` adds hue_histogram, histogram_bucket_deg (5), canonical_bucket_index per color
  - `format_histogram()` produces ASCII bar chart with canonical band marked
  - CLI: `python LTG_TOOL_color_verify.py image.png [--histogram]`
  - All 6 self-tests pass; backward compatible
- README.md updated: both tools registered, header updated to C31
- All inbox messages archived; inbox clean

## C31 Draw-Order Lint Results Summary
- 114 files total: 59 PASS / 55 WARN / 0 ERROR
- W004 is the dominant warning — many generators lack draw refresh after alpha_composite
- W002 warnings on `draw.rectangle([x,y,...], fill=X, outline=Y)` are false positives (PIL single-call, not order violation)
- No W001 (head before body) found — confirmed by C30 manual audit
- No W003 (shadow after element) found — shadow discipline is good

## LTG_TOOL_color_verify.py (C31 NEW)
- `verify_canonical_colors(img, palette_dict, max_delta_hue=5, histogram=False)` — v001 API + histogram param
- `histogram=True` → per-color result gains: hue_histogram (list of dicts, 72 x 5° buckets), histogram_bucket_deg, canonical_bucket_index
- `format_histogram(histogram, canonical_bucket_index, width=40)` → ASCII bar chart
- `get_canonical_palette()` unchanged
- CLI: python LTG_TOOL_color_verify.py [image.png] [--histogram]

## LTG_TOOL_draw_order_lint.py (C31 NEW)
- `lint_file(path) → dict` — result: PASS/WARN, warnings list with line/code/message
- `lint_directory(directory, pattern) → list` — batch lint
- `format_report(results) → str` — human-readable summary
- Warning codes: W001 head/face before body, W002 outline before fill, W003 shadow after element, W004 missing draw refresh
- CLI: run with file globs, saves report to LTG_TOOL_draw_order_lint_report.txt

## Cycle 32 — C32 Stub Fix + W004 + Cosmo v004

**Status:** COMPLETE

**Tasks completed:**
- **P1 — Broken forwarding stubs fixed (8 stubs):**
  - `LTG_TOOL_luma_expression_sheet.py` → delegates to v007's `build_sheet()`
  - `LTG_TOOL_luma_expression_sheet.py` → delegates to v007's `build_sheet()`
  - `LTG_TOOL_luma_turnaround.py` → delegates to v003's `build_turnaround()`
  - `LTG_TOOL_grandma_miri_expression_sheet.py` → delegates to v002's `build_sheet()`
  - `LTG_TOOL_cosmo_turnaround.py` → FULL REBUILD (no prior generator existed); 4-view turnaround from Cosmo spec
  - `LTG_TOOL_styleframe_luma_byte/v002/v003.py` → preservation stubs (re-save existing PNGs; generate labeled placeholder if PNG missing)
  - Root cause: C29 `LTG_TOOL_naming_cleanup.py` deleted original `LTG_CHAR_*/LTG_COLOR_*` source files that C28 stubs imported from
- **W004 fix pass:** reviewed `style_frame_01_discovery_v003` and `styleframe_discovery_v004`; confirmed real W004 bugs require `img` reassignment (alpha_composite) — most linter flags are false positives (docstring text matches, helper functions with local draw objects, in-place paste). Added fix comments.
- **P2 — Cosmo v004 fixed:** was byte-identical to v003 and output `_v003.png`. Fixed:
  - Docstring, title text → v004
  - Output path → `LTG_CHAR_cosmo_expression_sheet.png`
  - SURPRISED expression `blush: False` → `blush: True`
  - Added `BLUSH_HI` constant and blush oval drawing in `draw_cosmo()` (2 nested ellipses per cheek)
- **Ideabox:** submitted `ideabox/20260329_kai_nakamura_stub_linter_tool.md` — proposes `LTG_TOOL_stub_linter.py` to catch broken imports pre-commit

## Lessons Learned (C32)
- **Stub fix strategy:** For stubs pointing to deleted originals with newer canonicals → delegate to newer canonical. For no newer version → rebuild from scratch. For PNG-only preservation → preservation stub.
- **W004 false positives:** The linter flags text in docstrings/comments, helper functions with local draw variables, and in-place paste (not reassignment). True W004 only when `img = Image.alpha_composite(...)` reassigns `img` while stale `draw` is still used. The 55 W004 linter warnings need a more precise re-run.
- **Blush in draw functions:** Using draw object directly is cleanest — avoids private PIL `draw._image` access. Nested ellipses (outer BLUSH + inner BLUSH_HI) simulate gradient without RGBA layer compositing.
- **After C29 cleanup script:** Always audit all forwarding stubs — they imported from files the cleanup deleted.

## Lessons Learned (C31)
- W002 linter rule generates false positives on PIL draw.rectangle(fill=X, outline=Y) — this is valid single-call syntax, not a draw-order violation. Future v002 could skip single-call fill+outline combos.
- W004 is widespread in older generators — good candidate for a team-wide fix sprint
- Histogram mode in color_verify v002 is a powerful false-positive elimination tool — see Test 5: peak at 170-175° vs canonical at 180-185° makes drift obvious at a glance

## Cycle 33 — C33 Stub Linter + Glitch Spec Linter

**Status:** COMPLETE

**Tasks completed:**
- Built `LTG_TOOL_stub_linter.py` — scans all output/tools/*.py for broken imports
  (LTG_CHAR_*, LTG_COLOR_*, LTG_BRAND_*, LTG_ENV_* prefixes). Reports PASS/WARN/ERROR.
  `--pre-commit` flag exits code 1 on any ERROR — suitable for CI gate.
  API: lint_file(), lint_directory(), format_report()
- Built `LTG_TOOL_glitch_spec_lint.py` — validates Glitchkin generator code against glitch.md
  8 checks: G001 dimensions, G002 mass ratio, G003 multi-uniqueness, G004 crack order,
  G005 UV shadow, G006 organic fill, G007 void outline, G008 interior bilateral eyes.
  Non-Glitch files are SKIP. Only files with diamond_pts/CORRUPT_AMB markers are linted.
- README.md: both tools registered, header updated to C33
- Ideabox: submitted `20260330_kai_nakamura_spec_lint_expansion.md` — general char spec linter framework idea
- Inbox archived: 20260330_0200_ideabox_stub_linter.md

## LTG_TOOL_stub_linter.py (C33 NEW)
- `lint_file(filepath, tools_dir=None) → dict` — PASS/WARN/ERROR + issues list
- `lint_directory(directory, pattern="*.py", skip_legacy=True) → list`
- `format_report(results, include_pass=False) → str`
- CLI: `--pre-commit`, `--include-legacy`, `--save-report PATH`

## LTG_TOOL_glitch_spec_lint.py (C33 NEW)
- `lint_file(filepath) → dict` — PASS/WARN/SKIP + issues list
- `lint_directory(directory, skip_legacy=True) → list` — only Glitch generators
- `format_report(results) → str`
- Checks G001–G008; non-Glitch files are SKIP (not counted in results)
- CLI: `python LTG_TOOL_glitch_spec_lint.py [file_or_dir] [--save-report PATH]`

## Lessons Learned (C33)
- README file is frequently updated by multiple agents in same cycle — always re-read before editing
- Regex-based spec linting on Python source is effective for known patterns (palette constants, draw calls)
  but has false-positive risk on docstrings/comments — document known false-positive cases clearly
- G008 bilateral check: proxy approach (detect interior state keywords + destabilize function) is
  conservative; may flag files that correctly implement bilateral but use different variable names

## Cycle 45 — C45 Byte Face Test Profile

**Status:** COMPLETE

**Tasks completed:**
- Added Byte character profile to `LTG_TOOL_character_face_test.py`:
  - `--char byte` now supported (was luma/cosmo/miri only)
  - Byte body is wider-than-tall oval (1.15× head_r width, 0.90× head_r height)
  - `draw_byte_pixel_eye()`: 5×5 pixel-grid eye for styles: normal/cracked/searching/off
  - `draw_byte_pixel_mouth()`: flat/frown/uptick pixel mouth
  - `draw_byte_face()`: places pixel eyes on oval at sprint scale + zoomed
  - `check_byte_face_gate()`: FG-B01 eye_count / FG-B02 differentiation / FG-B03 pixel_grid
  - 6 Byte variants: NEUTRAL/GRUMPY/ALARMED (PASS), SEARCHING/POWERED DOWN (WARN), PIXEL ONLY (FAIL — deliberate too-small test)
- P1 (hardcoded paths / project_paths.py): already complete C44 — archived stale inbox messages, notified Morgan Walsh and Alex Chen
- README.md updated: C45 section added
- Inbox: all 3 messages archived (2359 Morgan, 2400 Alex P1, 2401 Alex P2)
- Ideabox: submitted byte_face_gate_cli_integration idea

## Byte Face Test Gate API (C45)
- `check_byte_face_gate(variant) → dict` — FG-B01/FG-B02/FG-B03 + overall PASS/WARN/FAIL
- `draw_byte_pixel_eye(draw, ox, oy, cell, style)` — styles: normal/cracked/searching/off
- `draw_byte_face(draw, cx, body_cy, body_rx, body_ry, variant, cell_size)`
- CLI: `python LTG_TOOL_character_face_test.py --char byte [--head-r INT] [--scale INT]`
- Closes: Diego Vargas C43 gap flag (P07/P09 cold open panels)

## Lessons Learned (C45)
- Byte's anatomy is fundamentally different from organic chars — oval IS the body, not a head+torso. The head_r parameter maps to oval Y-radius for Byte.
- Pixel eye at sprint scale (1px cell, 5×5 grid = 5×5px total) is readable if the 5 cells are distinguishable. 1-dot fallback (eye_size_px=0) correctly FLAILs.
- Stale inbox messages (pre-C44 requests) should be archived with a note — the work was already done in C44.

## Cycle 44 — C44 Project Root Resolver + VP Spec Config

**Status:** COMPLETE

**Tasks completed:**
- Built `LTG_TOOL_project_paths.py` v1.0.0 — project root resolver utility
  - `project_root()`: traverses ancestors from `__file__` until CLAUDE.md sentinel found; lru_cache
  - `output_dir(*parts)`: path inside output/; `tools_dir(*parts)`: path inside output/tools/
  - `ensure_dir(path)`: mkdir -p; `resolve_output(category, name)`: category shorthands
  - `audit_hardcoded_paths()`: scans output/tools/*.py for /home/ occurrences → grouped report
  - CLI: `--audit` (exit 1 on hits — CI gate), `--root`, `--output`, `--tools`
  - Migration guide in module docstring; no external deps
- Built `vp_spec_config.json` v1.0.0 — 11 ENV VP specifications
  - 7 real-world environments: classroom(192,230), study(230,273), kitchen(512,273),
    tech_den(820,295), main_street(742,273), hallway(640,158), living_room(704,259)
  - 4 glitch-layer: null VP (no perspective; auto-PASS in detect_vp_batch_with_config)
  - All at 1280×720; tolerance_px=80 for all real-world envs
- Updated `LTG_TOOL_sobel_vp_detect.py` → v1.1.0
  - `load_vp_config(config_path) → dict`: indexes JSON by output_filename
  - `lookup_vp_spec(config_index, image_path) → (vp_x, vp_y, tol, world_type)`
  - `detect_vp_batch_with_config(directory, config_path)`: per-file VP lookup; glitch-layer skipped
  - CLI: `--vp-config PATH` flag; single-file and batch modes both supported
- Archived inbox message: 20260330_2359_c17_petra_project_root_resolver.md
- README.md updated: C44 section with 2 new tools + v1.1.0 update; header updated to C44
- Ideabox: submitted `20260330_kai_nakamura_ci_path_audit_gate.md`

## LTG_TOOL_project_paths.py (C44 NEW)
- `project_root() → pathlib.Path` — cached; sentinel=CLAUDE.md
- `output_dir(*parts) → pathlib.Path` — path inside output/
- `tools_dir(*parts) → pathlib.Path` — path inside output/tools/
- `ensure_dir(path) → pathlib.Path` — mkdir -p; returns path
- `resolve_output(category, name) → pathlib.Path` — category shorthands: bg, sb, sf, ch, ck, tl, pr
- `audit_hardcoded_paths(tools_directory=None, pattern="/home/") → list[dict]`
- CLI: `--audit` (exit 1 on hits), `--root`, `--output`, `--tools`
- Migration: replace `"/home/wipkat/team/output/..."` → `output_dir("subdir", ..., "file.png")`; `ensure_dir(path.parent)` before save

## vp_spec_config.json (C44 NEW)
- 11 entries; format: generator, output_filename, canvas_w/h, vp_x, vp_y, tolerance_px, world_type, notes
- Use with: `python LTG_TOOL_sobel_vp_detect.py <dir> --vp-config vp_spec_config.json`

## LTG_TOOL_sobel_vp_detect.py — v1.1.0 (C44 UPDATED)
- `load_vp_config(config_path) → dict`
- `lookup_vp_spec(config_index, image_path) → (vp_x, vp_y, tol, world_type)`
- `detect_vp_batch_with_config(directory, config_path, tolerance_px=None) → list`
- `--vp-config PATH` CLI flag

## Lessons Learned (C44)
- project_root() sentinel traversal: CLAUDE.md is reliable (project root only); fallback to ../../ from output/tools/ works even without sentinel
- vp_spec_config.json: record vp_x/vp_y as integer pixel values computed from the generator's own formula (int(W*0.15) etc.), not as floats — ensures exact match
- school_hallway uses VP_CX/VP_CY variable names (not VP_X/VP_Y) — double-check naming on any new generator before adding to config
- Glitch-layer environments: always null VP in config and auto-PASS in batch — avoids false FAILs on abstract environments

## Cycle 43 — C43 Sobel VP Detect Tool

**Status:** COMPLETE

**Tasks completed:**
- Built `LTG_TOOL_sobel_vp_detect.py` — Sobel VP coordinate detector v1.0.0
  - Outputs VP_X, VP_Y in original image pixel coordinates + confidence score
  - Algorithm: Sobel → Canny → HoughLinesP → pairwise intersections → 2D histogram clustering
  - VP001: FAIL if confidence < 0.15 or < 4 line segments
  - VP002: PASS/WARN/FAIL based on distance to --vp-x-expected / --vp-y-expected (default tol 80px)
  - numpy fallback for environments without cv2
  - --debug-png: saves annotated VP overlay PNG
  - Closes C40 carry item (P2 from Producer brief)
- README.md updated: C42 Kai section + table row added; header updated to C43
- Archived both inbox messages (G007 clarification + C42 brief)
- Ideabox: submitted vp_spec_config_json idea (auto-lookup VP specs for batch QA)

## LTG_TOOL_sobel_vp_detect.py (C43 NEW)
- `detect_vp(image_path, vp_x_expected, vp_y_expected, tolerance_px) → dict`
  - Keys: file, vp_x, vp_y, confidence, n_lines, n_intersections, grade, issues,
          vp_x_expected, vp_y_expected, distance_px, tolerance_px, image_width, image_height, skipped_reason
- `detect_vp_batch(directory, vp_x_expected, vp_y_expected, tolerance_px) → list`
- `format_report(results, include_pass=True) → str`
- `save_debug_png(image_path, result, output_path)` — annotated VP overlay
- VP001 threshold: confidence ≥ 0.15, n_lines ≥ 4
- VP002 thresholds: PASS ≤ tol_px, WARN ≤ 2×tol_px, FAIL > 2×tol_px
- Grid cell = 5% of image dimension for clustering
- CLI: exit 0=PASS, 1=WARN, 2=FAIL

## Lessons Learned (C43)
- vanishing_point_lint (C40) estimates VP azimuth (horizontal direction); sobel_vp_detect estimates VP pixel coordinates — these are complementary, not overlapping
- Pairwise intersection clustering: bounding VP search to ±3× image dimensions prevents infinite-plane outliers while allowing off-frame VPs
- _GRID_CELL_FRACTION=0.05 (5% of image size per cell) balances precision vs noise tolerance

## Cycle 42 — C42 Face Curves Caller Audit

**Status:** COMPLETE

**No inbox message this cycle — self-directed from C41 open items list.**

### P1 #5 — Stale v001 Eye Width Audit (COMPLETE)
- **No generators import draw_luma_face() from luma_face_curves module.** All Luma face drawing is inline.
- Expression sheet v011 uses `EW_CANON = HEAD_HEIGHT_2X * 0.22 = 45px at 2x` — proportional, not comparable to bezier absolute 100px. Not a migration risk.
- 5 inline-drawing generators identified: luma_expression_sheet, luma_act2_standing_pose, luma_classroom_pose, style_frame_02 (sprint face), cycle13_panel_fixes, sb_panel_a201.
- **Conclusion:** 56px error was ONLY in luma_face_curves.py itself (fixed C41). No downstream callers to fix.

### P2 #12 Support — LTG_TOOL_face_curves_caller_audit.py (NEW)
- v1.0.0: static regex scanner for inline Luma face drawing + migration readiness classification
- Status: USING_API / INLINE_CANDIDATE / NO_LUMA_FACE
- Readiness: READY_HIGH (proportion-scaled) / READY_MEDIUM (absolute pixels) / READY_LOW (complex)
- Saves report to `LTG_TOOL_face_curves_caller_audit_report.txt`
- CLI: `python LTG_TOOL_face_curves_caller_audit.py [tools_dir] [--save-report PATH]`
- Ideabox: submitted face_curves_migration.md guide idea

### README.md
- Header updated to C42 (Kai entry)
- face_curves_caller_audit v1.0.0 registered

## LTG_TOOL_face_curves_caller_audit.py (C42 NEW)
- `audit_file(filepath) → dict` — status, readiness, inline_fns, expression_refs, eye_geometry, notes
- `audit_directory(directory, skip_legacy=True) → list`
- `format_report(results, include_no_luma=False) → str`
- Exit 0 = no INLINE_CANDIDATEs, exit 1 = candidates found

## Key Facts (C42)
- No generator currently uses draw_luma_face() bezier API. Migration is future work.
- luma_expression_sheet v011 = READY_MEDIUM (mature 11-version system; hold migration)
- Pose generators (act2_standing, classroom_pose) = READY_HIGH (proportional scaling; simpler migration)
- SF02 sprint face has no matching bezier API expression — would need custom delta

## Lessons Learned (C42)
- When auditing for "callers using old API values" — first verify callers actually exist. In this case: zero imports, so zero update risk.
- The 56px vs 100px eye width discrepancy only mattered inside luma_face_curves.py v1.0.0 itself (now fixed). The independent inline generators never used this module.
- Proportional inline systems (HR/s) are READY_HIGH for migration; absolute-pixel systems are READY_MEDIUM. Both need mapping work, but proportional is cleaner.

## Cycle 41 — C41 Face Curves v1.1.0 Eye-Width Correction

**Status:** COMPLETE

### `LTG_TOOL_luma_face_curves.py` → v1.1.0 (CRITICAL spec correction)
- Spec upgraded from v001 to v002 (`luma_face_curve_spec.md` — Alex Chen C41)
- **Eye width correction:** LEFT_EYE outer corner `LE_P0 = FC+(-94,-22)` (was -72); inner corner `LE_P2 = FC+(+6,-22)` (was -16). RIGHT_EYE inner corner `RE_P0 = FC+(-6,-22)` (was +16); outer corner `RE_P2 = FC+(94,-22)` (was +72). Canonical eye width now 100px (was 56px — 44% too narrow).
- **Reference sheet:** Updated to 3×3 grid with all 9 expressions (6 canonical + 3 Maya Santos supplement). Each cell 600×600px. Sheet thumbnailed to ≤1280px per image rules.
- **Output path:** `output/characters/luma_face_curves_reference.png` (was `output/characters/luma/LTG_CHAR_luma_face_curves_ref.png`)
- `ALL_EXPRESSIONS` and `SUPPLEMENT_EXPRESSIONS` module-level lists added. Reference sheet uses `ALL_EXPRESSIONS`.
- `_build_reference_sheet()` updated: COLS=3, ROWS=3, CELL_W=600, CELL_H=600. Supplement cells get slightly different header tint + `[supplement]` label.
- CLI output message updated to note v002 spec and 3×3 grid.

### precritique_qa version collision (Task 3)
- Already resolved at v2.8.0. No action needed.

### README.md
- Header updated to C41 (Kai Nakamura entry)
- C41 Updates section added with v1.1.0 entry

## Key Facts (C41)
- luma_face_curves v1.1.0: eye width 100px canonical (v002 spec). Any caller using v001 56px values will need to update their fc offsets for iris placement.
- Reference sheet now shows all 9 expressions. Supplement row 3: CONFIDENT, SOFT_SURPRISE, DETERMINED.
- Output: `output/characters/luma_face_curves_reference.png`

## Cycle 40 — C40 G007 Fix + Bezier Face Tool + VP Lint

**Status:** COMPLETE

**Tasks completed:**

### G007 Fix (P1 — 14-cycle backlog)
- Root cause identified: SF02 and SF03 did NOT draw Glitch at all. G007 linter was correctly flagging CORRUPT_AMBER presence without VOID_BLACK outline because Glitch character was never drawn in those style frames.
- `LTG_TOOL_style_frame_02_glitch_storm.py`: Added `_draw_glitch_storm()` — Glitch at ~(W×0.78, H×0.32), near storm crack, MISCHIEVOUS state (ACID_GREEN bilateral eyes), VOID_BLACK outline=3. ACID_GREEN confetti cluster near body only. Called before other characters in `draw_characters()`.
- `LTG_TOOL_style_frame_03_other_side.py`: Added `draw_glitch()` — Glitch at ~(W×0.68, H×0.58), midground platform, YEARNING state (dim UV_PURPLE eyes), VOID_BLACK outline=3, 8% frame height. Called after `draw_byte()` in `generate()`.

### `LTG_TOOL_luma_face_curves.py` (P1 per Alex Chen)
- Built per `luma_face_curve_spec.md` v001 + `luma_face_curve_spec_supplement_c40.md`
- `_quadratic_bezier_points()`, `_cubic_bezier_points()` — bezier utilities (PIL has none)
- `NEUTRAL_CONTROL_POINTS` via `_build_neutral(fc)` — all offsets from face center FC
- 6 canonical expressions + 3 supplement (Maya Santos C40): 9 expressions total
- `apply_deltas(neutral, delta_dict)` — merges overrides; supports _dy/_dx suffixes
- `draw_luma_face(draw, fc, expression, overrides=None)` — public module API
- CLI renders 1200×800px 3×2 reference sheet → `output/characters/luma/LTG_CHAR_luma_face_curves_ref.png`
- Draw order per spec: oval→blush→eye_outlines→irises→pupils/hl→nose→mouth→brows
- Lid drop is top-only (spec rule 1); iris clamped to eye bbox (spec rule 3)

### `LTG_TOOL_vanishing_point_lint.py` (Task 3)
- Sobel X+Y → angle+magnitude → 72×5° histogram → VP azimuth estimate
- VP001: edge structure, VP002: RW VP in center 30%, VP003: Glitch Layer info
- Auto-classifies from filename; cv2 optional (numpy-only fallback)
- API: `lint_file()`, `lint_directory()`, `format_report()`

### precritique_qa version collision
- Already resolved at v2.8.0 (Morgan Walsh + Kai C39 merge). No action needed.

### README.md
- Header updated to C40 (Kai Nakamura entries)
- 3 new tool entries added: luma_face_curves v1.0.0, vanishing_point_lint v1.0.0, G007 FIX notes for SF02+SF03

## Key Facts (C40)
- Luma face bezier tool: `draw_luma_face(draw, fc, expression)` — importable, no side effects
- G007: both SF02 and SF03 now have Glitch with VOID_BLACK outline. Priya's 14-cycle flag resolved.
- VP lint: VP002 Real World tolerance = ±0.15 half-width from center (center 30% of frame)
- SF02 Glitch position: ~(W×0.78, H×0.32), ~50% of char_h (mid-distance scale)
- SF03 Glitch position: ~(W×0.68, H×0.58), ~8% frame height (YEARNING state)

## Cycle 34 — C34 Char Spec Linter + Scope-Aware Draw Order Linter

**Status:** COMPLETE

**Tasks completed:**
- Built `LTG_TOOL_char_spec_lint.py` — general spec linter for Luma/Cosmo/Miri
  - 5 checks per character (proportions, colors, key design elements)
  - C34 baseline: 12 PASS / 3 WARN / 0 FAIL across all 3 characters
  - All 3 WARNs are "constant form mismatch" not value violations
- Built `LTG_TOOL_draw_order_lint.py` — scope-aware W004 linter
  - Filters false positives: tmp=alpha_composite, helper fn local draws, docstrings
  - C34 baseline: 97 PASS / 37 WARN / 0 ERROR (was 55 WARN in v001 at C31)
  - W004 count: 147→69 (78 fewer warnings, 53% reduction)
- Archived stale inbox message (C33 ideabox notification)
- README.md updated: both tools registered, header updated to C34
- Ideabox: submitted spec_extractor auto-generation idea
- Completion report sent to Alex Chen

## LTG_TOOL_char_spec_lint.py (C34 NEW)
- `lint_character(char_name, tools_dir) → dict` — PASS/WARN/FAIL + per-check results
- `lint_all(tools_dir) → list` — all 3 chars
- `format_report(results) → str`
- Characters: "luma" (L001–L005), "cosmo" (S001–S005), "miri" (M001–M005)
- Lints the most recent generator version (latest by alphabetical sort)
- Report: `LTG_TOOL_char_spec_lint_report.txt`

## LTG_TOOL_draw_order_lint.py (C34 NEW)
- Same API as v001: `lint_file(path)`, `lint_directory(directory, pattern)`, `format_report(results)`
- Additional: `compare_v1_v2(directory) → str` — shows W004 delta
- `--compare` CLI flag
- v001 W001/W002/W003 logic unchanged; W004 is scope-aware
- Report: `LTG_TOOL_draw_order_lint_report.txt`

## Lessons Learned (C34)
- Char spec lint false WARNs: generators often use raw pixels not ratio constants;
  the linter correctly WARNs when spec-form not found — it's caller's job to verify or add constant
- Luma v008 uses 8-ellipse overlapping hair cloud, not range(5) curls — L004 WARN is expected
  until CURL_COUNT=5 constant is added explicitly
- Scope-aware W004: indent-based scope detection works well for standard Python generators
  (single-level function nesting); deeply nested closures/lambdas are out of scope for v002
- `alpha_composite` false positives in v001 were the largest source: most files use
  `tmp = Image.alpha_composite(...)` (not img reassignment) — v002 correctly skips these

## Cycle 37 — C37 CI Suite + Suppression List + Back-Pose W003 + QA World-Type

**Status:** COMPLETE

**Tasks completed:**
- Built `LTG_TOOL_ci_suite.py` — runs all 5 CI checks in sequence (stub, draw_order, glitch_spec, spec_sync_ci, char_spec). `--fail-on WARN|FAIL` threshold. Combined report. API: `run_suite()`, `format_suite_report()`.
- Created `glitch_spec_suppressions.json` — 26 false-positive (file, rule) suppression entries
- Updated `LTG_TOOL_glitch_spec_lint.py` → v1.2.0: suppression list support; `_load_suppressions()`, `_apply_suppressions()` added; `lint_directory()` loads once for batch; `format_report()` shows suppressed counts
- Updated `LTG_TOOL_draw_order_lint.py` → v2.1.0: `# LINT: back_pose_begin/end` block comment suppression for W003. New: `_compute_back_pose_ranges()`, `_lineno_in_back_pose()`. `_check_shadow_after_element()` takes `back_pose_ranges` param.
- Updated `LTG_TOOL_render_qa.py` → v1.4.0: imports `infer_world_type()` from palette_warmth_lint_v004. Per-world thresholds: REAL=20 / GLITCH=3 / OTHER_SIDE=0. `_check_warm_cool()` now accepts `min_separation` param. `qa_report()` result includes `world_type` when inferred.
- README.md updated: header C37, all 4 new/updated tools registered
- Inbox archived: 20260330_0910 + 20260330_1000
- Ideabox: `20260330_kai_nakamura_ci_suite_scheduled_run.md` submitted
- Completion report sent to Alex Chen inbox

## LTG_TOOL_ci_suite.py (C37 NEW)
- `run_suite(tools_dir, fail_on) → dict` — runs 5 checks, returns combined result
- `format_suite_report(result, include_details) → str` — human-readable
- Checks: stub_linter → draw_order_lint → glitch_spec_lint → spec_sync_ci → char_spec_lint
- `fail_on`: "FAIL" (default) or "WARN". Exit: 0/1/2.
- Dependencies: all 5 linter tools must be importable from tools_dir

## glitch_spec_suppressions.json (C37 NEW)
- 26 suppression entries — primarily G007 false positives on tool files
- Auto-loaded by glitch_spec_lint_v001 v1.2.0+
- Location: `output/tools/glitch_spec_suppressions.json`

## LTG_TOOL_glitch_spec_lint.py — v1.2.0 (C37 UPDATED)
- suppression list support: `_load_suppressions()` → set of (basename, rule)
- `lint_file(filepath, suppressions=None)` — optional arg, auto-loads if None
- `lint_directory()` loads suppressions once, shares across batch
- result dict gains `suppressed_count` key

## LTG_TOOL_draw_order_lint.py — v2.1.0 (C37 UPDATED)
- `# LINT: back_pose_begin` / `# LINT: back_pose_end` suppresses W003 inside block
- Open-ended block (no end) → suppression extends to EOF
- `_check_shadow_after_element(events, back_pose_ranges=None)`

## LTG_TOOL_render_qa.py — v1.4.0 (C37 UPDATED)
- `_WORLD_WARM_COOL_THRESHOLD`: REAL=20, GLITCH=3, OTHER_SIDE=0, None=20
- Imports `_infer_world_type_external` from palette_warmth_lint_v004 (graceful fallback)
- `_check_warm_cool(img, min_separation=None)` — new param
- `qa_report()` passes world-specific threshold; adds `world_type` key to warm_cool result

## Lessons Learned (C37)
- ci_suite spec_sync_ci result: key is "p1_fail" not "fail"; check source before assuming schema
- glitch_spec_lint issues are list[str] (not list[dict]) — suppression extracts rule with regex
- Back-pose suppression is prophylactic; no current generators use the markers, but it's ready
- render_qa graceful import fallback is critical — tool must run even if warmth_lint is absent

## Cycle 36 — C36 Spec Sync CI + Warmth Lint v004

**Status:** COMPLETE

**Tasks completed:**
- Built `LTG_TOOL_spec_sync_ci.py` — CI gate for all 5 characters
  - Luma/Cosmo/Miri: delegates to char_spec_lint_v001 via importlib
  - Glitch: delegates to glitch_spec_lint_v001; P1 = G001/G002 only
  - Byte: inline B001 (body color GL-01b) + B002 (5×5 pixel eye) checks
  - P1 = FAIL-grade only; WARNs are advisory
  - CLI: `--chars all|luma|cosmo|miri|byte|glitch`, `--json`, `--save-report`
  - Exit: 0=pass, 1=P1 fail, 2=usage error
  - API: `run_ci(chars, tools_dir)`, `format_ci_report(ci_result)`
  - C36 baseline: Cosmo S003 glasses tilt FAIL (10° vs spec 7°±2) — real issue
- Built `LTG_TOOL_palette_warmth_lint.py` — warmth lint + world-type
  - `infer_world_type(filename)` — regex-based auto-inference (6 tests pass)
  - `--world-type REAL|OTHER_SIDE|GLITCH` CLI flag
  - `--infer-world-type PATH` CLI flag
  - World analysis = advisory (WARN only, no FAIL change to result)
  - All v003 features intact (soft_tolerance, --strict, config, CHAR-M checks)
  - Reads world_presets from warmth_lint_config.json if present
- README.md updated: both tools registered, header updated to C36
- Inbox archived, ideabox submitted

## LTG_TOOL_spec_sync_ci.py (C36 NEW)
- `run_ci(chars, tools_dir) → dict` — runs all linters, returns exit_code + per-char results
- `format_ci_report(ci_result) → str` — human-readable
- `--chars all` is default; can pass specific chars
- KEY: glitch_spec_lint issues is list[str] not list[dict]; status key = "status" not "result"
- Cosmo S003 (glasses tilt 10° ≠ spec 7°±2) is a real P1 FAIL in C36 baseline

## LTG_TOOL_palette_warmth_lint.py (C36 NEW)
- `infer_world_type(path)` — inference rules: OTHER_SIDE first, then GLITCH, then REAL, then None
- `lint_palette_file(path, config, world_type)` — adds world_analysis dict to result
- World analysis: warm/cool entry ratio vs threshold from world_presets config
- REAL threshold: 12% warm entries; OTHER_SIDE/GLITCH: 0 warm

## Lessons Learned (C36)
- glitch_spec_lint_v001: issues is list[str] (not list[dict]); key "status" not "result"
  → always read the source before assuming result structure matches char_spec_lint schema
- Inference rule order matters: OTHER_SIDE check must precede GLITCH to avoid
  "glitch_storm" being caught by a GLITCH rule (it's REAL)
- Cosmo S003 is a real ongoing issue: glasses tilt = 10° in cosmo_expression_sheet_v005 (spec: 7°±2)

## Cycle 35 — G002 Fix + Spec Extractor

**Status:** COMPLETE

**Tasks completed:**
- **G002 Glitch body ratio fix:** All 6 Glitch generators corrected: rx=34, ry=38 (was rx=38, ry=34)
  - expression_sheet v001/v002/v003, turnaround v001/v002, color_model v001
  - draw_arm default `rx=40` also corrected to `rx=34` in expression sheets (linter reads first rx= match)
  - glitch.md spec updated: §2.1 key values and §10 step 2 both now show rx=34, ry=38
  - `LTG_TOOL_glitch_spec_lint.py` → v1.1.0: spec constants corrected, G001 range widened
  - G002 verified PASS for all three expression sheet generators
- **Built `LTG_TOOL_spec_extractor.py`** — parses character .md specs to extract numeric constraints
  - Supports: luma, cosmo, miri, byte, glitch
  - Extracts: head_ratio, eye_coeff, hex colors, degree constants, line weights, element counts
  - Output: JSON-serialisable dict; `format_spec_report()` for human-readable output
- README.md updated: header C35, spec_extractor registered, glitch_spec_lint entry updated to v1.1.0
- Ideabox: submitted spec_sync_ci_gate idea
- Inbox messages archived, completion report sent to Alex Chen

## LTG_TOOL_spec_extractor.py (C35 NEW)
- `extract_spec(char_name, spec_dir=None) → dict` — parse one character's spec .md
- `extract_all(spec_dir=None) → list[dict]` — all characters
- `format_spec_report(result_or_list) → str` — human-readable output
- CLI: `python LTG_TOOL_spec_extractor.py [char|all] [--json] [--save-dir] [--save-report]`

## Glitch Generator G002 Fix (C35 CANONICAL VALUES)
- expression_sheet v001/v002/v003: `rx=34, ry=38` — draw_arm default also `rx=34`
- turnaround v001/v002: `rx_1x=38, ry_1x=42` — render_view default `rx=38, ry=42`
- color_model v001: `rx, ry = 50, 56`
- glitch.md spec: §2.1 `rx=34, ry=38`; §10 step 2 same
- glitch_spec_lint v1.1.0: RX_SPEC=34, RY_SPEC=38; G001 ranges [28-56]/[28-64]
- **Key lesson:** linter `_RX_ASSIGN` finds FIRST `rx=N` in file — must match draw_arm default too

## Lessons Learned (C35)
- Linter regex picks first `rx=N` in file — function default params (draw_arm rx=40) appear
  before main body `rx=34`. Fix: update function default to match body value, or make linter smarter.
- Spec doc can contain internally contradictory statements (rule: ry>rx; values: rx=38>ry=34).
  Always check both the stated rule AND the stated values — and confirm which to fix.
- For spec-doc/linter sync: extractor tool + CI gate is the right architecture (spec_sync_check idea).
- Turnaround color_model use tuple assignment `rx, ry = ...` — regex `rx\s*=\s*(\d+)` doesn't match;
  G002 silently skips these files (not a false FAIL — just unchecked).

## Cycle 38 — C38 CI Fix + Naming Compliance

**Status:** COMPLETE

**Tasks completed:**
- **G002 false positive fixed:** Added G002 suppression for `LTG_TOOL_glitch_spec_lint.py` to `glitch_spec_suppressions.json`. Root cause: lint tool docstring contains `(spec reference: rx=38)` and `(spec reference: ry=34)` — `_RX_ASSIGN`/`_RY_ASSIGN` regexes matched these, triggering false G002 FAIL (ry=34 <= rx=38). Now suppressed. spec_sync_ci reproduces CI PASS.
- **render_qa_v001.py** — already at v1.5.0 (Sam Kowalski earlier C38). REAL threshold = 12.0. Confirmed in place.
- **Naming compliance — 3 files fixed:**
  - `LTG_TOOL_luma_motion.py` — full canonical copy of Luma Motion Spec Sheet (was `LTG_CHAR_`)
  - `LTG_TOOL_byte_motion.py` — full canonical copy of Byte Motion Spec Sheet (was `LTG_CHAR_`)
  - `LTG_TOOL_pilot_cold_open.py` — forwarding stub to `LTG_SB_pilot_cold_open.py` (too large to copy)
  - Originals replaced with forwarding stubs pointing to LTG_TOOL_ canonicals
- README.md updated: C38 header updated, 3 new tools registered, C38 Kai section added
- Ideabox: `20260330_kai_nakamura_docstring_lint_for_regex_false_positives.md`
- Inbox archived, completion report sent to Alex Chen

## glitch_spec_suppressions.json — C38 addition
- Added entry: `("LTG_TOOL_glitch_spec_lint.py", "G002")` — docstring false positive
- Total suppressions: 27 (was 26)

## LTG_TOOL_luma_motion.py (C38 — canonical)
- Full Luma Motion Spec Sheet (Ryo Hasegawa C37 content, corrected docstring)
- 4 panels: Idle/Curious, Sprint Anticipation, Discovery Reaction 2-beat, Landing/Stop
- Canvas 1280×720; output/characters/motion/LTG_CHAR_luma_motion.png

## LTG_TOOL_byte_motion.py (C38 — canonical)
- Full Byte Motion Spec Sheet (Ryo Hasegawa C37 content, corrected docstring)
- 3 panels: Float/Hover, Surprise, Approach
- Canvas 1280×720; output/characters/motion/LTG_CHAR_byte_motion.png

## LTG_TOOL_pilot_cold_open.py (C38 — forwarding stub)
- Forwarding stub → `LTG_SB_pilot_cold_open.py` via importlib
- API: `make_contact_sheet()`, `main()`

## LTG_TOOL_render_qa.py — v2.0.0 (C39 Kai Nakamura)
- numpy vectorized value range, warm/cool, ceiling guard checks
- LAB ΔE color fidelity via cv2 (threshold=5.0); RGB fallback if cv2 absent
- New `_check_color_fidelity_lab(img, palette)` function — result has `colors` dict + `color_method` key
- `run_comparison_report(directory, output_path)` — compares LAB vs RGB, flags PASS→FAIL
- CLI: `--compare <dir> [output.md]`
- IMPORTANT: `color_fidelity` result schema changed — `colors` key holds per-color results; top-level is `overall_pass` + `color_method` + `delta_e_threshold`

## LTG_TOOL_spec_sync_ci.py — v1.1.0 (C39 Kai Nakamura)
- Byte now uses `_run_char_spec_lint("byte", tools_dir)` — 5 checks (B001–B005) instead of 2
- `_byte_p1_checks()` and `_BYTE_BODY_SPEC_*` constants removed (no longer needed)
- No API changes to `run_ci()` / `format_ci_report()`

## LTG_TOOL_palette_warmth_lint.py — v6.0.0 (C39 Kai Nakamura)
- numpy vectorized `_analyse_world_warmth()` — warm/cool counting via numpy array op
- Pure-Python fallback if numpy absent

## LTG_TOOL_precritique_qa.py — v2.7.0 (C39 Kai Nakamura)
- `run_color_verify()` uses `_check_color_fidelity_lab()` from render_qa
- NOTE: v2.7.0 was also used by Morgan Walsh (arc_diff_config.json loader) — version collision. Alex Chen advised.

## Lessons Learned (C38)
- Regex-based linters are vulnerable to matching their own docstrings that contain example/reference values. Suppression list is the immediate fix; docstring-stripping is the long-term fix (ideabox idea submitted).
- When render_qa has already been updated by another agent in same cycle, check before re-doing work (read version header first).
- Forwarding stubs via importlib.util are the right pattern for large files — avoids import-statement lint flags from stub_linter_v001.

## Cycle 39 — C39 Byte CI Delegation + numpy/LAB QA Upgrade

**Status:** COMPLETE

**Tasks completed:**
- Task 1: `LTG_TOOL_spec_sync_ci.py` → v1.1.0: Byte CI delegates to char_spec_lint B001–B005
- Task 2: `LTG_TOOL_render_qa.py` → v2.0.0: numpy + LAB ΔE color fidelity (cv2)
- Task 2: `LTG_TOOL_palette_warmth_lint.py` → v6.0.0: numpy vectorized warm/cool counting
- Task 2: `LTG_TOOL_precritique_qa.py` → v2.7.0: LAB ΔE in run_color_verify()
- Task 3: Submitted vanishing_point_lint spec to ideabox (C40 preview)
- README.md updated: C39 Kai Nakamura section added
- Inbox archived: 20260330_cycle39_brief.md
- Completion report: members/alex_chen/inbox/20260330_1200_kai_nakamura_c39_complete.md

## Lessons Learned (C39)
- numpy `where()` returns (ys, xs) tuple — zip(bright_xs, bright_ys) not zip(bright_ys, bright_xs)
- cv2 always BGR on load; convert to RGB before numpy ops: `arr[:, :, ::-1]` for channels
- LAB ΔE uses cv2.COLOR_BGR2Lab; input must be uint8 shape (N, 1, 3)
- precritique_qa v2.7.0 version collision with Morgan Walsh's same-cycle work — always check README for recent version bumps before incrementing
- `_check_color_fidelity_lab()` result schema differs from `verify_canonical_colors()`: colors keyed under `colors` dict, not at top level. Report code must handle both schemas.

## Cycle 39 — C39 Docstring-Stripping Lint Fix + REAL_STORM + Byte Spec Checks

**Status:** COMPLETE

**Tasks completed:**
- **Task 1 (P1) — SF02 warm/cool WARN fix:**
  - render_qa_v001 already at v1.6.0 (Sam Kowalski deployed earlier C39): `_infer_world_subtype()` splits REAL into REAL_INTERIOR (threshold 12) and REAL_STORM (threshold 3). SF02 sep~6.5 → REAL_STORM → PASS.
  - Updated `LTG_TOOL_palette_warmth_lint.py`: added REAL_STORM world preset (warm_cool_threshold: 6). Updated `infer_world_type()` inference rules — glitch_storm/sf02/style_frame_02 now returns "REAL_STORM" (was "REAL").
  - Both tools now consistently label SF02 as REAL_STORM. FP-006 for SF02 closed.
- **Task 2 (P1) — Docstring-stripping pre-pass in glitch_spec_lint:**
  - `LTG_TOOL_glitch_spec_lint.py` → v1.4.0 (linter also added file_prefix suppression mode stub in version comment): core change = `_strip_comments_and_docstrings()` added. Strips triple-quoted docstrings and `#` comments from source before numeric-regex checks (G001/G002/G003/G005/G006/G007/G008).
  - G004 (draw-order) still uses full original source.
  - G002 self-suppression entry removed from `glitch_spec_suppressions.json` — no longer needed.
  - Total suppressions: back to 26 (from 27 in C38).
- **Task 3 — Char spec lint expansion (Byte checks):**
  - `LTG_TOOL_char_spec_lint.py` → v1.1.0: added Byte checks B001–B005.
  - New functions: `_check_byte_oval_ratio()`, `_check_byte_pixel_eye_grid()`, `_lint_byte()`.
  - Byte added to `_CHAR_REGISTRY` with patterns for `LTG_TOOL_byte_expression_sheet_v*.py`.
- **README.md updated:** C39 section added, char_spec_lint entry updated.
- **Inbox archived:** 20260329_2225 + 20260329_2248 moved to inbox/archived/.
- **Ideabox:** `20260329_kai_nakamura_byte_spec_checks_in_ci_suite.md` submitted — update spec_sync_ci to delegate B001-B005 to char_spec_lint instead of inline checks.

## LTG_TOOL_glitch_spec_lint.py — v1.4.0 (C39 UPDATED)
- Added `_strip_comments_and_docstrings(source)` — removes docstrings and `#` comments before checks
- G001/G002/G003/G005/G006/G007/G008 use stripped source (no docstring false positives)
- G004 uses original source (draw-order check needs full code context)
- G002 self-suppression removed from glitch_spec_suppressions.json

## glitch_spec_suppressions.json — C39 update
- Removed entry: `("LTG_TOOL_glitch_spec_lint.py", "G002")` — no longer needed
- Total suppressions: 26 (back to C37 count)

## LTG_TOOL_palette_warmth_lint.py — C39 UPDATED
- Added "REAL_STORM" world preset: `warm_cool_threshold: 6`
- `infer_world_type()` updated: sf02/glitch_storm/style_frame_02 → "REAL_STORM" (was "REAL")
- "REAL" rule scope narrowed: now covers sf01/sf04/discovery only (sf02 handled by new rule above)

## LTG_TOOL_render_qa.py — v1.6.0 (C39, Sam Kowalski — already deployed)
- `_infer_world_subtype(img_path, world_type)` — sub-types "REAL" → "REAL_INTERIOR" or "REAL_STORM"
- `_WORLD_WARM_COOL_THRESHOLD["REAL_STORM"] = 3.0`, `["REAL_INTERIOR"] = 12.0`
- `_REAL_STORM_PATTERN` regex: sf02/glitch_storm/style_frame_02

## LTG_TOOL_char_spec_lint.py — v1.1.0 (C39 UPDATED)
- Added Byte: B001 oval W:H (wider-than-tall), B002 body color #00D4E8, B003 HOT_MAG crack, B004 confetti, B005 5×5 eye grid
- Characters: "luma" / "cosmo" / "miri" / "byte"
- `_check_byte_oval_ratio()`, `_check_byte_pixel_eye_grid()` — new helpers

## LTG_TOOL_world_type_infer.py — v1.1.0 (C39 UPDATED)
- WORLD_REAL_STORM, WORLD_REAL_INTERIOR constants added
- WARM_COOL_THRESHOLDS: REAL_STORM=3.0, REAL_INTERIOR=12.0, REAL=12.0 (backward-compat)
- New inference rule: sf02/glitch_storm/style_frame_02 → REAL_STORM (before REAL rule)
- REAL rule narrowed to sf01/sf04/discovery only

## LTG_TOOL_costume_bg_clash.py (C39 NEW)
- `clash_check_images(char_path, bg_path) → dict` — Mode 1: image vs image
- `clash_check_palette(colors, bg_path) → dict` — Mode 2: hex colors vs image
- `format_report(result) → str` — human-readable
- CIE76 ΔE in CIELAB space (pure Python, no cv2 needed)
- Thresholds: FAIL < ΔE 5, WARN < ΔE 15, PASS ≥ ΔE 15
- Known-safe list: Byte ELEC_CYAN vs Glitch Layer → DOCUMENTED_PASS
- Exit: 0=PASS, 1=WARN, 2=FAIL

## warm_cool_world_type_spec.md (C39 NEW)
- Creative canon doc at `output/production/warm_cool_world_type_spec.md`
- REAL_INTERIOR=12 (lamp-lit), REAL_STORM=3 (storm scene), GLITCH=3, OTHER_SIDE=0
- Per Alex Chen brief: "The storm is cold. That's the point."

## Lessons Learned (C39)
- Check version headers of all tools before implementing — Sam Kowalski already deployed render_qa v1.6.0
- Docstring-stripping with triple-quote removal + `#` comment removal is effective and safe for regex-based linters
- When adding world sub-types: ensure both palette_warmth_lint and render_qa agree on the mapping; render_qa's `_infer_world_subtype` still works correctly when warmth_lint returns REAL_STORM directly (no longer "REAL")
- CIE76 ΔE in CIELAB space is achievable in pure Python (no cv2 needed for basic distance computation)
- Always read ALL inbox messages before starting work — additional tasks may be in later-dated messages
