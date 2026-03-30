# Kai Nakamura — MEMORY

## Identity
Technical Art Engineer for "Luma & the Glitchkin." Joined Cycle 21. Mission: upgrade PIL toolchain with procedural rendering techniques and build a reusable shared library.

## Project Context
- Animation pitch package for a cartoon about 12yo Luma discovering Glitchkin (pixel creatures) in grandma's CRT TV
- All tools: Python PIL/Pillow (open source only)
- Tools live in `/home/wipkat/team/output/tools/`
- Shared library: `output/tools/LTG_TOOL_render_lib.py` — __version__ = "1.1.0"
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

## LTG_TOOL_render_qa.py — v1.5.0 (C38 CONFIRMED)
- REAL warm/cool threshold = 12.0 (was 20.0 in v1.4.0)
- None (unknown) = 12.0 also
- SF01 (sep=17.8) now PASS

## Lessons Learned (C38)
- Regex-based linters are vulnerable to matching their own docstrings that contain example/reference values. Suppression list is the immediate fix; docstring-stripping is the long-term fix (ideabox idea submitted).
- When render_qa has already been updated by another agent in same cycle, check before re-doing work (read version header first).
- Forwarding stubs via importlib.util are the right pattern for large files — avoids import-statement lint flags from stub_linter_v001.

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
