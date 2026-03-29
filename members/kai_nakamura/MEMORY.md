# Kai Nakamura — MEMORY

## Identity
Technical Art Engineer for "Luma & the Glitchkin." Joined Cycle 21. Mission: upgrade PIL toolchain with procedural rendering techniques and build a reusable shared library.

## Project Context
- Animation pitch package for a cartoon about 12yo Luma discovering Glitchkin (pixel creatures) in grandma's CRT TV
- All tools: Python PIL/Pillow (open source only)
- Tools live in `/home/wipkat/team/output/tools/`
- Shared library: `output/tools/LTG_TOOL_render_lib_v001.py` — __version__ = "1.1.0"
- Naming: `LTG_[CATEGORY]_[descriptor]_v[###].[ext]`

## Key Standards
- Byte body fill = GL-01b (#00D4E8 / RGB 0,212,232) — never Void Black
- Glitch palette never in real-world environments
- After img.paste() or alpha_composite(), always refresh draw = ImageDraw.Draw(img)
- All procedural elements use seeded RNG for reproducibility
- output/production/ files are EXEMPT from LTG naming (descriptive names only)
- **IMAGE SIZE RULE: prefer smallest resolution appropriate for the task. Hard limit ≤ 1280px in both dimensions.** Use `img.thumbnail((1280, 1280), Image.LANCZOS)` before saving. Preserve aspect ratio. Only use large sizes when detail inspection requires it; use smaller sizes otherwise. Detail crops also ≤ 1280×1280px.

## Palette Reference (verified C25 from master_palette.md)
- CORRUPT_AMBER:  (255, 140, 0)    #FF8C00  GL-07
- BYTE_TEAL:      (0, 212, 232)    #00D4E8  GL-01b
- UV_PURPLE:      (123, 47, 190)   #7B2FBE  GL-04
- HOT_MAGENTA:    (255, 45, 107)   #FF2D6B  GL-02  (NOT #FF0090)
- ELECTRIC_CYAN:  (0, 240, 255)    #00F0FF  GL-01
- SUNLIT_AMBER:   (212, 146, 58)   #D4923A  RW-03

## LTG_TOOL_render_lib_v001.py — API Summary (Canonical)
__version__ = "1.1.0" (C24: paper_texture added)
Functions: perlin_noise_texture, gaussian_glow, light_shaft, dust_motes,
           catenary_wire, scanline_overlay, vignette, paper_texture
Import: `from LTG_TOOL_render_lib_v001 import ...`

## LTG_TOOL_color_verify_v001.py (C25 NEW)
- `verify_canonical_colors(img, palette_dict, max_delta_hue=5)` → per-color + overall_pass dict
- `get_canonical_palette()` → standard 6-color LTG palette dict
- Sampling: pixels within Euclidean RGB radius=40 of target; median hue; not_found = not a fail
- Standalone (stdlib colorsys + Pillow only)

## LTG_TOOL_batch_stylize_v001.py — RETIRED (C26)
- Moved to `output/tools/legacy/` along with stylize v001 and v002
- Post-processing stylization pipeline fully retired C26
- UV_PURPLE color protection issue in stylize tools is moot — tools no longer active

## LTG_TOOL_render_qa_v001.py — v1.1.0 (C27 UPDATED)
- Full QA pipeline: silhouette, value range, color fidelity, warm/cool, line weight
- `qa_report(img_path, asset_type="auto") → dict` — single image, 5 checks, overall_grade PASS/WARN/FAIL
- `qa_batch(directory, asset_type="auto") → list[dict]` — all PNGs in a directory
- `qa_summary_report(results, output_path)` — writes Markdown report
- `silhouette_test(img) → PIL.Image` — 100×100 B&W (compatible with Rin's procedural_draw)
- `value_study(img) → PIL.Image` — grayscale auto-contrast (compatible with Rin's procedural_draw)
- asset_type values: "auto"|"style_frame"|"character_sheet"|"color_model"|"turnaround"|"environment"
- character_sheet/color_model/turnaround → warm/cool SKIPPED (not a WARN); grade from active checks only
- Import: `from LTG_TOOL_render_qa_v001 import qa_report, qa_batch, qa_summary_report`
- Depends on: LTG_TOOL_color_verify_v001 (must be in same directory / sys.path)

## Cycle 27 — COMPLETE
- Updated LTG_TOOL_render_qa_v001.py → v1.1.0: asset_type param, warm/cool skip for char sheets
- Ran QA on 29 C27 pitch assets → saved `output/production/qa_report_cycle27.md`
- Processed post-processing pipeline retirement notice (inbox archived)

## C27 QA Findings (29 assets: 6 PASS / 21 WARN / 2 FAIL)
- **2 FAILs:**
  - LTG_CHAR_lineup_v004.png — silhouette=blob (character sheet; warm/cool correctly skipped)
  - LTG_ENV_classroom_bg_v002.png — silhouette=blob + multiple WARNs
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
- 5 conflict cases archived to legacy/: LTG_CHAR_luma_expression_sheet v002/v003/v004, LTG_CHAR_byte_expression_sheet_v004, LTG_CHAR_cosmo_expression_sheet_v004
- Original LTG_CHAR_/LTG_COLOR_ source files remain on disk — require `git mv` for history preservation

**P2 — README.md updated:**
- 37 new entries added to Script Index in `output/tools/README.md`
- C28 legacy archive section added
- LTG_TOOL_render_qa_v001 entry updated to reflect v1.1.0 asset_type parameter

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
- character_sheet_standards_v001.md line weight table: corrected to head=4, structure=3, detail=2 at 2× (was 8/4/2px) — note: appeared already corrected by prior pass
- Created `LTG_TOOL_naming_cleanup_v001.py` — removes 22 non-compliant originals once LTG_TOOL_ canonical confirmed
- Updated README.md: C29 legacy archive section, cleanup tool entry, header updated to C29
- Archived all 3 C29 inbox messages to inbox/archived/
- **22 LTG_CHAR_/LTG_COLOR_/LTG_BRAND_ .py files remain on disk** — all have LTG_TOOL_ canonicals; need `LTG_TOOL_naming_cleanup_v001.py` run to delete
- Image handling policy incorporated (see below)

**Pending (requires script execution):**
- Run `python LTG_TOOL_naming_cleanup_v001.py` in output/tools/ to delete the 22 originals
- After run: remove forwarding stubs (they reference now-deleted originals)

## Image Handling Policy (C29 — ALL agents)
- Before sending any image to Claude for inspection: ask if a tool could extract the insight. **If so, make the tool.**
- Before sending an image: ask if lower resolution suffices. **If so, downscale.**
- Never send high-res images to Claude unless absolutely necessary.
- Claude vision limitations: may hallucinate on low-quality/rotated/tiny images; limited spatial reasoning; approximate counting only.
- For QA pipeline: `LTG_TOOL_render_qa_v001.py` should downscale images before any vision-based inspection step.
- Image size rule: ≤ 1280px in both dimensions for all saved images.

## Lessons Learned (C29)
- When Bash is restricted and no git repo exists: write a cleanup script, document it, can't execute directly
- character_sheet_standards: corrections may already be applied by prior same-day agent passes — always verify before re-editing
- Forwarding stub cleanup is a follow-on task after the cleanup script runs

## Cycle 30 — C30 Draw Order Audit + README/Index Gaps + QA Downscale

**Status:** COMPLETE

**Tasks completed:**
- Draw order audit: reviewed all C29 generators (v007, lineup v006, styleframe_discovery_v004) and representative older generators. No critical draw-order failures found. Findings:
  - LTG_TOOL_styleframe_discovery_v004: CORRECT — bg → couch (midground) → lighting overlay → body → head+face lighting+rim light → Byte (FG) → vignette → title
  - LTG_TOOL_luma_expression_sheet_v007: body drawn BEFORE head (correct). Hair drawn AFTER head — hair cloud is mostly above head (no face overlap), foreground strand arcs correctly on top. Minor cosmetic issue only; not critical.
  - LTG_TOOL_character_lineup_v006: hair drawn before head = CORRECT back-to-front
  - All audited generators: shadows/fills before outlines = CORRECT
- README gaps fixed: added 3 unregistered C29 generators (luma_expression_sheet_v007, character_lineup_v006, styleframe_discovery_v004). naming_cleanup_v001 was already registered. Updated README header to C30. Updated render_qa entry to note v1.2.0.
- pitch_package_index.md updated: added Cycle 29 Additions section (v007 expression sheet, lineup v006, SF01 v004). Updated lineup and SF01 sections to mark v006 and v004 as PITCH PRIMARY.
- LTG_TOOL_render_qa_v001.py updated to v1.2.0: added automatic downscale to ≤1280px on input images before all QA checks. Uses img.thumbnail((1280,1280), Image.LANCZOS). Changelog updated.
- Ideabox: submitted draw order linter idea to /home/wipkat/team/ideabox/20260329_kai_nakamura_draw_order_linter.md
- Inbox: 20260329_2030_ideabox.md archived. Other 3 inbox messages (1730, 1940, 2000) already in archived/ — file removal blocked by restricted Bash.

## LTG_TOOL_render_qa_v001.py — v1.2.0 (C30 UPDATED)
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
- Built `LTG_TOOL_draw_order_lint_v001.py` — static draw-order linter (regex, no AST/execution)
  - Detects W001 head/face before body, W002 outline before fill, W003 shadow after element, W004 missing draw refresh after paste/composite
  - Ran against all 114 LTG_TOOL_*.py: 59 PASS / 55 WARN / 0 ERROR
  - Most WARNs are W004 (missing draw refresh) — widespread issue in older generators
  - W002 false positives: `draw.rectangle([...], fill=..., outline=...)` is valid PIL (single call, not order issue) — linter flags these conservatively
  - Report saved to `output/tools/LTG_TOOL_draw_order_lint_v001_report.txt`
- Built `LTG_TOOL_color_verify_v002.py` — histogram mode addition to color_verify
  - `verify_canonical_colors(..., histogram=True)` adds hue_histogram, histogram_bucket_deg (5), canonical_bucket_index per color
  - `format_histogram()` produces ASCII bar chart with canonical band marked
  - CLI: `python LTG_TOOL_color_verify_v002.py image.png [--histogram]`
  - All 6 self-tests pass; backward compatible
- README.md updated: both tools registered, header updated to C31
- All inbox messages archived; inbox clean

## C31 Draw-Order Lint Results Summary
- 114 files total: 59 PASS / 55 WARN / 0 ERROR
- W004 is the dominant warning — many generators lack draw refresh after alpha_composite
- W002 warnings on `draw.rectangle([x,y,...], fill=X, outline=Y)` are false positives (PIL single-call, not order violation)
- No W001 (head before body) found — confirmed by C30 manual audit
- No W003 (shadow after element) found — shadow discipline is good

## LTG_TOOL_color_verify_v002.py (C31 NEW)
- `verify_canonical_colors(img, palette_dict, max_delta_hue=5, histogram=False)` — v001 API + histogram param
- `histogram=True` → per-color result gains: hue_histogram (list of dicts, 72 x 5° buckets), histogram_bucket_deg, canonical_bucket_index
- `format_histogram(histogram, canonical_bucket_index, width=40)` → ASCII bar chart
- `get_canonical_palette()` unchanged
- CLI: python LTG_TOOL_color_verify_v002.py [image.png] [--histogram]

## LTG_TOOL_draw_order_lint_v001.py (C31 NEW)
- `lint_file(path) → dict` — result: PASS/WARN, warnings list with line/code/message
- `lint_directory(directory, pattern) → list` — batch lint
- `format_report(results) → str` — human-readable summary
- Warning codes: W001 head/face before body, W002 outline before fill, W003 shadow after element, W004 missing draw refresh
- CLI: run with file globs, saves report to LTG_TOOL_draw_order_lint_v001_report.txt

## Lessons Learned (C31)
- W002 linter rule generates false positives on PIL draw.rectangle(fill=X, outline=Y) — this is valid single-call syntax, not a draw-order violation. Future v002 could skip single-call fill+outline combos.
- W004 is widespread in older generators — good candidate for a team-wide fix sprint
- Histogram mode in color_verify v002 is a powerful false-positive elimination tool — see Test 5: peak at 170-175° vs canonical at 180-185° makes drift obvious at a glance
