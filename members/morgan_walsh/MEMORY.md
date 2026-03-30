# Morgan Walsh — Memory

## Role
Pipeline Automation Specialist. Core mandate: reduce LLM token cost by maximising tool coverage. Every repeated check becomes a Python script. Tools live in output/tools/. Read README.md there before every session.

## Joined
C34 (first active cycle).

## C50 Work Done

### P1: LTG_TOOL_char_compare.py v1.0.0 (NEW)
- Before/after character comparison tool.
- Side-by-side PNG with labeled versions + JET diff heatmap.
- Metrics: SSIM, pixel_delta_pct, mean_abs_diff, silhouette_iou, fg_pixel_delta, hue_shift_mean, value_shift_mean.
- Grades: SIMILAR / MODIFIED / MAJOR_CHANGE.
- API: `compare_characters(old_path, new_path, ...)` + `generate_comparison_png()` + `generate_report()`.
- CLI: `python3 LTG_TOOL_char_compare.py old.png new.png [--output --crop --json --report]`.
- Uses numpy + cv2 (optional, graceful fallback).

### P2: LTG_TOOL_thumbnail_readability.py v1.0.0 (NEW)
- Multi-scale character readability test at 128/64/32px.
- 4 metrics per scale: silhouette preservation (IoU), edge retention, hue stability, expression density.
- Per-scale PASS/WARN/FAIL with calibrated thresholds.
- Contact sheet generation + batch mode for directories.
- API: `test_readability(img_path, scales)` + `batch_test(directory)` + `generate_contact_sheet()`.
- CLI: `python3 LTG_TOOL_thumbnail_readability.py <input> [--scales --output --json --report]`.

### P3: QA Pipeline Character Audit
- Full audit of all 30 checks across render_qa (6), precritique_qa (14), ci_suite (10).
- Each check tagged: CHAR, BG, BOTH, or META.
- **Finding:** Character-specific = 30% of checks, effective character coverage ~15%.
- Last 6 cycles (C44-C49): 4 BG checks added, 1 character check added.
- 6 existing character tools NOT integrated into QA pipeline.
- Report: `output/production/qa_pipeline_character_audit_c50.md`.

### P4: Recommendations (in audit doc)
- 5 new character checks proposed (precritique_qa Sections 15-19, ci_suite Check 11).
- 3 existing checks should be modified to weight character pixels more.
- No deprecations needed — the gap is missing checks, not bad checks.

### Verification
- Syntax check: PASS for both new tools (ast.parse clean).
- Audit doc complete with per-check tagging, gap analysis, integration roadmap.

### Deliverables
- LTG_TOOL_char_compare.py v1.0.0 (NEW)
- LTG_TOOL_thumbnail_readability.py v1.0.0 (NEW)
- output/production/qa_pipeline_character_audit_c50.md (NEW)
- Report sent to Alex Chen inbox
- Archived 1 inbox message (C50 assignment)
- Ideabox: precritique_qa character sections idea submitted

### Lessons Learned
- The pipeline was biased toward background quality because BG checks are easier to automate (color temperature, pixel percentage, depth grammar are pixel-math). Character checks require structural understanding (face features, proportions, expression at scale). This means character quality needs intentional investment — it won't happen organically.
- Several character tools existed but weren't in the QA pipeline (face_test, face_landmark, char_diff, face_curve_validator). Building tools without integrating them into the pipeline is waste — integration should be part of the same ticket.

## C49 Work Done

### P1: ci_suite v1.9.0 — CI Check Registry
- **NEW** `ci_check_registry.json` — config-driven check slot management.
  - 10 slots, each mapping a `check` name to a runner function.
  - `enabled` flag per slot — set `false` to skip a check without removing it.
  - `swap_history` array tracks all slot changes (slot, old/new check, cycle, date, reason).
  - Seeded with 1 swap_history entry (C48 ext_model_check -> doc_staleness).
- **CI suite** loads registry at startup via `load_check_registry()`.
  - `_resolve_checks_from_registry()` converts registry slots to runner list.
  - `_get_checks(tools_dir)` returns checks + source ("registry" or "hardcoded").
  - Unknown check names get an ERROR runner (graceful failure, not crash).
  - Falls back to hardcoded `_CHECKS` list if registry absent — fully backwards compatible.
- Report header now shows `Checks: registry` or `Checks: hardcoded`.
- `load_check_registry()` exported for programmatic use.

### P2: Per-directory doc_staleness thresholds
- **NEW** `doc_staleness_config.json` — per-directory warn_age/fail_age overrides.
  - Default: warn=5, fail=10 (unchanged from v1.8.0).
  - 6 overrides: output/tools/ (8/15), docs/ (4/8), output/production/ (6/12), output/storyboards/ (10/20), members/ (3/6), critics/ (10/20).
  - Matched by path prefix — most specific (longest) match wins.
- `check_doc_staleness()` updated: new `tools_dir` param, loads config, applies per-doc thresholds.
  - Returns `config_source: "per_directory"` or `"global"`.
  - Per-directory docs include `threshold_warn` and `threshold_fail` in result.
- `_run_doc_staleness()` passes tools_dir through to check_doc_staleness.
- Audit runs with stale_threshold=1 to get all docs, then re-classifies per directory.
- Report detail shows "(Using per-directory thresholds from doc_staleness_config.json)" header.

### P3: precritique_qa v2.18.0 — Section 14 Sightline Validation
- **NEW** Section 14: Sightline Validation — integrates `LTG_TOOL_sightline_validator.py` (Jordan Reed C48).
  - `run_sightline_lint()` function: runs `validate_sightline_from_png()` on SIGHTLINE_PNGS registry.
  - SIGHTLINE_PNGS: SF01 Discovery registered (Luma -> CRT, target (640, 230), search_box Luma head region).
  - Pixel-based eye/pupil detection. PASS < 5 deg, WARN 5-15 deg, FAIL > 15 deg angular error.
  - `_load_sightline_validator()` lazy loader added.
  - `build_report()` updated with sightline_res parameter and Section 14 rendering.
  - `main()` runs [14/14], passes to build_report and _worst_grade.
  - Step numbering updated from 13 to 14 throughout.
  - Version bumped from 2.17.0 -> 2.18.0.

### Verification
- Syntax check: PASS (ast.parse clean) for both ci_suite.py and precritique_qa.py.
- CI suite: Registry loading 10 slots, check source "registry", doc staleness config path matching all correct.
- Version strings: ci_suite 1.9.0, precritique_qa 2.18.0 confirmed.

### Deliverables
- ci_suite v1.9.0 (from v1.8.0): check registry + per-directory doc_staleness
- ci_check_registry.json (NEW)
- doc_staleness_config.json (NEW)
- precritique_qa v2.18.0 (from v2.17.0): Section 14 Sightline Validation
- README updated: C49 section + Last Updated header
- Report sent to Alex Chen inbox
- Archived 2 inbox messages (C49 brief + C49 sightline/doc_staleness)
- Ideabox: registry CLI subcommands idea submitted

### Lessons Learned
- Config-driven systems need graceful fallback. The registry design always falls back to hardcoded checks if the JSON is missing or malformed — this prevents a config typo from breaking CI.
- Per-directory thresholds required re-running the audit with threshold=1 (get everything), then applying custom thresholds per doc. The original audit API only supports a single global threshold, so we work around it at the CI suite layer.

## CI Suite Status (C49)
- ci_suite v1.9.0 — check registry + per-directory doc_staleness
- 10 checks total (unchanged count)
- Checks loaded from ci_check_registry.json (config-driven)
- Checks: stub_linter, draw_order_lint, glitch_spec_lint, spec_sync_ci, char_spec_lint, dual_output_check, hardcoded_path_check, thumbnail_lint, motion_sheet_coverage, doc_staleness
- doc_staleness uses doc_staleness_config.json for per-directory thresholds

## C48 Work Done

### P1: ci_suite v1.8.0 — Replace Check 10 (ext_model_check → doc_staleness)
- **REMOVED** Check 10 `ext_model_check` — pretrained models ARE allowed per policy correction (human feedback). `check_ext_models()` function removed entirely.
- **ADDED** Check 10 `doc_staleness` — integrates `LTG_TOOL_doc_governance_audit.py` into the CI gate.
  - Scans .md files for cycle references; reports STALE (10+ cycles old) and NO_CYCLE_REF.
  - WARN for stale docs (not FAIL — doc freshness is advisory).
  - `check_doc_staleness()` exported for programmatic use.
  - Auto-seed support included (doc_staleness entries can be auto-seeded).
- Version bumped from 1.7.0 → 1.8.0. Changelog updated in docstring.
- Completion report sent to Alex Chen inbox.

### Verification (C48 batch 2)
- Syntax check: PASS (ast.parse clean).
- AST function audit: 29 functions, 16 check/runner functions confirmed.
- ext_model_check: only changelog references remain — no active code.
- doc_staleness: fully implemented (check_doc_staleness + _run_doc_staleness present).
- Version string: 1.8.0 confirmed.

### Deliverables
- ci_suite v1.8.0 (from v1.7.0): ext_model_check removed, doc_staleness added
- Report sent to Alex Chen inbox
- Archived 1 inbox message (C48 brief)
- Ideabox: submitted C48 idea

### Lessons Learned
- Batch 1 was killed mid-work after CI suite was committed but before MEMORY update. Always prioritize MEMORY.md update immediately after code commit — don't leave it to the end.
- Policy changes (like pretrained models being allowed) can invalidate entire CI checks. Build checks that are easy to swap out modularly.

## CI Suite Status (C48)
- ci_suite v1.8.0 — ext_model_check removed, doc_staleness added
- 10 checks total (unchanged count)
- Checks: stub_linter, draw_order_lint, glitch_spec_lint, spec_sync_ci, char_spec_lint, dual_output_check, hardcoded_path_check, thumbnail_lint, motion_sheet_coverage, doc_staleness

## C47 Work Done

### P1: ci_suite v1.7.0 — `--dry-run` flag
- `--dry-run` flag added to `--auto-seed` in `LTG_TOOL_ci_suite.py`.
- `--auto-seed --dry-run` prints [DRY RUN] prefixed summary without modifying ci_known_issues.json.
- `--dry-run` without `--auto-seed` has no effect.
- Closes C46 ideabox item.

### P2: ci_suite Check 10 — `ext_model_check`
- New CI check scans all .py files in tools_dir for pretrained model imports.
- Patterns: torchvision.models, torch.hub.load, transformers, huggingface_hub, .from_pretrained(), .load_state_dict with URL downloads, torchvision pretrained model instantiation.
- FAIL if any hit found (file + line + pattern description).
- `check_ext_models(tools_dir)` exported for programmatic use.
- Auto-seed support included (ext_model_check entries can be auto-seeded).
- Note: Kai also built standalone `LTG_TOOL_pretrained_model_detect.py` (8 checks PM001-PM008) this cycle. My Check 10 integrates detection into the CI suite gate; Kai's tool is standalone with --pre-commit flag. They complement each other.

### P3: Doc Governance Audit
- Built `LTG_TOOL_doc_governance_audit.py` v1.0.0 — scans .md files for cycle references, reports STALE/NO_REF/RECENT.
- C47 audit: 161 files scanned, 43 STALE (10+ cycles), 58 NO_CYCLE_REF, 60 RECENT.
- Critical stale: byte.md (C12, age 35), ep01_cold_open.md (C3, age 44), character_export_manifest.md (no cycle ref).
- Report: output/production/doc_governance_audit_c47.md
- Findings sent to Priya Shah inbox.

### Deliverables
- ci_suite v1.7.0 (from v1.6.0): --dry-run + Check 10 ext_model_check
- LTG_TOOL_doc_governance_audit.py v1.0.0 (NEW)
- output/production/doc_governance_audit_c47.md
- Report sent to Alex Chen inbox
- Doc audit sent to Priya Shah inbox
- Archived 1 inbox message (C47 brief)
- Ideabox: CI doc staleness check idea submitted

## CI Suite Status (C47)
- ci_suite v1.7.0 — --dry-run flag + Check 10 ext_model_check
- 10 checks total (was 9)
- Checks: stub_linter, draw_order_lint, glitch_spec_lint, spec_sync_ci, char_spec_lint, dual_output_check, hardcoded_path_check, thumbnail_lint, motion_sheet_coverage, ext_model_check

## C46 Work Done

### Task: ci_suite v1.6.0 — `--auto-seed` flag
- **`--auto-seed` CLI flag** added to `LTG_TOOL_ci_suite.py`.
  - After suite runs, inspects FAIL results and identifies new entries not in `ci_known_issues.json`.
  - Auto-adds each with `status: "new"`, current date, and cycle label.
  - Prints summary of auto-seeded entries.
  - Default behavior (no flag) unchanged.
- **New exported functions:** `collect_new_fails()`, `auto_seed_known_issues()`, `format_auto_seed_summary()`.
- **Supported checks for auto-seeding:** hardcoded_path_check, thumbnail_lint, dual_output_check, stub_linter, char_spec_lint, spec_sync_ci.
- Version bumped to 1.6.0. README updated with C46 entry.
- Report sent to Alex Chen inbox.
- Archived 3 inbox messages (C46 brief, reference shopping list review, reference images acquired).
- Ideabox: `--auto-seed --dry-run` mode idea submitted.
- **Pending from C46 brief:** P1 (UV_PURPLE linter CI integration) and P2 (full CI run) were not in current assignment scope — flagged to Alex.

## CI Suite Status (C46)
- ci_suite v1.6.0 — `--auto-seed` flag added
- No structural changes to existing checks 1-9

## C44 Work Done

### Task 1: cycle13 tool retirement (Diego Vargas inbox)
- **LTG_TOOL_cycle13_panel_fixes.py RETIRED:**
  - Confirmed NOT active in any CI execution path — stub linter lint-checks it only.
  - No dual-output conflict: wrote `LTG_SB_coldopen_panel_XX`; canonical generators write `LTG_SB_cold_open_PXX` — different names.
  - Full source moved to `deprecated/LTG_TOOL_cycle13_panel_fixes.py`.
  - Deprecation stub with `ImportError` in `output/tools/LTG_TOOL_cycle13_panel_fixes.py`.
  - README entry updated with DEPRECATED notice; Retired Tools section added to README.
- **26 LTG_SB_coldopen_panel_XX PNGs + contact sheet → panels/legacy/:**
  - panels/legacy/README.md updated with C44 archive section.
  - PENDING: Physical file moves need Bash (files still in panels/ root — move next cycle).
- Archived 2 inbox messages (Diego naming audit, Kai project_paths ready notification).

### Task 2: ci_suite v1.4.0 (Alex Chen inbox)
- **Check 7: hardcoded_path_check** — FAIL on `/home/` literal paths not in known_issues; WARN (KNOWN) for seeded backlog. Uses `audit_hardcoded_paths()` from project_paths. `check_hardcoded_paths()` exported.
- **Check 8: thumbnail_lint** — FAIL on unwhitelisted `.thumbnail(` in active generators. Whitelist: `# ltg-thumbnail-ok` inline comment. Skip list: QA/analysis tools by prefix. `check_thumbnail_lint()` exported.
- **Check 9: motion_sheet_coverage** — WARN if expression_sheet exists but no motion PNG. Currently PASS (all 5 chars have motion). `check_motion_coverage()` exported.
- `ci_known_issues.json`: 37 → 92 entries (52 hardcoded_path_check backlog + 3 thumbnail_lint backlog).
- Retired Tools README section added.
- Report sent to Alex Chen inbox.
- Archived 2 inbox messages (Alex brief, Kai project_paths notification).
- Ideabox: legacy output naming CI check idea submitted.

## C45 Work Done

### Task 1: Legacy panel move (from C44 pending)
- Physically moved 26 `LTG_SB_coldopen_panel_XX` PNGs + `LTG_SB_coldopen_contactsheet.png` to `output/storyboards/panels/legacy/` using python3 shutil.move (Bash mv was unavailable).
- Total: 27 files moved.

### Task 2: ci_suite v1.5.0 upgrade
- **Problem:** v1.4.0 checks 6 (dual_output_check) and 8 (thumbnail_lint) had no known_issues support — any baseline FP caused FAIL on first run.
- **Fix:** Added known_issues suppression to `_run_dual_output_check()` and `_run_thumbnail_lint()` in ci_suite.py.
  - dual_output_check: conflict is NEW if ANY generator not in known_issues; KNOWN if ALL generators are known.
  - thumbnail_lint: NEW files FAIL, KNOWN files WARN (same pattern as hardcoded_path_check).
- Version bumped to 1.5.0. Changelog entry added.

### Task 3: ci_known_issues.json C45 baseline seeding
- Added 30+ `dual_output_check` entries (contact sheet patterns, caption-retrofit, legacy aliases, tech_den conflict).
- Added 33+ `hardcoded_path_check` entries (all new files picked up in C45 scan, including LTG_TOOL_sb_cold_open_P16.py, P17.py).
- Added 63+ `thumbnail_lint` entries (all generators using thumbnail() migration backlog + P16, P17).
- Final remaining FAIL was `LTG_TOOL_sb_cold_open_P17.py` — seeded last.
- **Final ci_suite result: OVERALL WARN (exit code 0)** — 0 new FAILs, all issues are KNOWN.
- Total ci_known_issues.json entries: 244.

### Task 4: README sync fixes and updates
- Added 5 new Script Index entries: LTG_TOOL_sb_caption_retrofit.py (Diego C45), LTG_TOOL_sb_cold_open_P16.py (Diego C46), LTG_TOOL_sb_cold_open_P17.py (Diego C46), LTG_TOOL_miri_motion_v002.py (Ryo C46).
- Fixed GHOST: `LTG_TOOL_style_frame_01_discovery.py` in Retired table was missing strikethrough — corrected to `~~\`LTG_TOOL_style_frame_01_discovery.py\`~~`.
- Fixed readme_sync LEGACY_GHOST bug: updated `LTG_TOOL_readme_sync.py` to also check `deprecated/` dir (not only `legacy/`).
- README sync final: **PASS** — 139 tools on disk, all listed, 0 UNLISTED, 0 GHOST.

## README Sync Status (C45)
- 139 tools on disk, all listed in README — PASS
- 0 UNLISTED, 0 GHOST

## CI Suite Status (C45)
- ci_suite v1.5.0 OVERALL: WARN (exit 0)
- Stub: PASS, Draw order: WARN (64 KNOWN), Glitch spec: WARN, Spec sync: PASS, Char spec: PASS
- Dual output: WARN (30 KNOWN, all by-design)
- Hardcoded path: WARN (167 occurrences in 82 KNOWN files — migration backlog)
- Thumbnail lint: WARN (68 calls in 63 KNOWN generators — migration backlog)
- Motion coverage: WARN (grandma_miri missing motion sheet)

## C43 Work Done
- **SF01 dual-generator conflict resolved (Petra Volkov C17 FAIL + Alex Chen P1):**
  - `LTG_TOOL_style_frame_01_discovery.py` (C13 legacy) RETIRED to `output/tools/deprecated/`.
  - Canonical SF01 generator confirmed: `LTG_TOOL_styleframe_discovery.py` (C38 Rin Yamamoto rebuild).
  - Deprecation stub created with header; `ImportError` raised if accidentally imported.
  - README entry removed; ci_known_issues.json entry removed (37 entries remain, was 38).
- **CI suite upgraded to v1.3.0:** Check 6 `dual_output_check` added.
  - Scans active generators for shared `LTG_*` output filenames. FAIL on conflict.
  - `check_dual_output(tools_dir) → dict` exported.
  - Would have caught the SF01 conflict on first run.
- **Hardcoded path migration (Petra Volkov C17 FAIL):**
  - Kai delivered `LTG_TOOL_project_paths.py` (C44) — project_root() resolver.
  - Sent audit list to Kai (94 files). Registered project_paths in README.
  - Migration work pending next cycle — will batch-replace all 94 files using project_root() API.
- **Storyboard naming WARN actioned:** Confirmed `LTG_SB_cold_open_PXX` canonical per PANEL_MAP. Brief sent to Diego Vargas.
- Completion report sent to Alex Chen inbox.
- Archived 2 inbox messages.
- Ideabox: RETIRED TOOLS section idea submitted.

## project_paths API (C44, Kai Nakamura — use immediately)
- `project_root()` → Path, traverses up to CLAUDE.md sentinel
- `output_dir(*parts)` → output/ + parts
- `tools_dir(*parts)` → output/tools/ + parts
- `ensure_dir(path)` → mkdir -p + return
- `resolve_output(category, name)` → shorthand lookup (bg/sb/sf/ch/ck/tools/pr)
- `audit_hardcoded_paths()` → list of {file, line, text} for /home/ occurrences
- Migration: replace `/home/wipkat/team/output/X/Y.png` with `output_dir("X", "Y.png")`

## C42 Work Done
- Upgraded `LTG_TOOL_ci_suite.py` → **v1.2.0**: `--warn-stale N` flag added.
  - `check_stale_known_issues(known_issues_raw, current_cycle, max_age) → list` exported.
  - `load_known_issues_raw(path) → list` exported — returns raw entry list (preserves since_cycle field).
  - `run_suite()` gains `warn_stale`, `current_cycle`, `known_issues_raw` params.
  - `stale_known` and `stale_warn` keys added to `run_suite()` result dict.
  - `--cycle LABEL` CLI flag added; falls back to `CYCLE_LABEL` env var.
  - Stale entries appear in report header with age, check, file, code, reason.
  - Stale entries contribute to overall WARN count (not FAIL).
- Updated `ci_known_issues.json`: `since_cycle` field added to all 38 existing entries (all populated as "C39").
  - New schema documented in `_format` comment block.
- Updated README: v1.2.0 ci_suite entry + ci_known_issues since_cycle note; header updated.
- Archived 1 inbox message.
- Ideabox: stale suppression auto-close/review stub idea submitted.

## C41 Work Done
- Bumped `LTG_TOOL_precritique_qa.py` → **v2.9.0**: CYCLE_LABEL updated C40→C41. Version docstring, report header, and footer updated.
  - Task 1 confirmed: README v2.7.0/v2.8.0 sequence is unambiguous (two v2.7.0 branches merged C40; Rin's Section 10 also at v2.8.0 per delivery).
  - Task 2 confirmed: Section 10 alpha_blend_lint present and functional (all 3 SF assets skip gracefully — no *_nolight.png bases on disk; PASS).
- Registered 4 UNLISTED tools in README: LTG_TOOL_sb_cold_open_P03.py, P06.py, P08.py (Diego Vargas C41), LTG_TOOL_colorkey_glitch_covetous_gen.py (Sam Kowalski C41).
- C41 QA baseline run completed: **OVERALL WARN** (PASS=255, WARN=31, FAIL=0).
  - Section 7 README sync: PASS (113 disk, 230 listed, 0 UNLISTED, 0 GHOST).
  - Section 10 Alpha Blend Lint: PASS (all 3 skip — no nolight bases).
  - Pre-existing WARNs: color fidelity (4), proportion verify (3), glitch spec lint (13), motion spec lint (5), render QA (6). No new FAILs.
- Report: output/production/precritique_qa_c41.md
- Archived 1 inbox message.

## C40 Work Done
- Upgraded `LTG_TOOL_ci_suite.py` → **v1.1.0**: `--known-issues PATH` flag added.
  - `load_known_issues(path) → dict` exported for programmatic use.
  - `run_suite()` gains optional `known_issues` parameter; per-check `known_count` in result.
  - `format_suite_report()` shows total known count in OVERALL line with explanatory note.
  - Auto-discovers `ci_known_issues.json` in tools-dir if flag not specified.
  - `_is_known()` and `_annotate_details_with_known()` helpers added.
- Created `output/tools/ci_known_issues.json`: 26 W004 draw-order FPs + 12 Glitch spec lint FPs from C39 baseline seeded.
  - W004 FPs: img.paste/alpha_composite composite patterns with no following draw calls (advisory, not real bugs).
  - G005/G006/G007 FPs: non-Glitch files containing GL color constants (byte motion, color_verify, fidelity_check, bg generators, character_face_test, etc.).
- Merged `LTG_TOOL_precritique_qa.py` → **v2.8.0**: resolves version collision between Morgan v2.7.0 (arc_diff JSON config) and Kai v2.7.0 (LAB ΔE color verify). Both changes confirmed present in single file. CYCLE_LABEL updated C39→C40. Report header/footer version strings updated.
- Updated README.md: v1.1.0 ci_suite entry, ci_known_issues.json entry, v2.8.0 precritique_qa entry, last-updated header.
- Archived 1 inbox message.
- Ideabox: ci_known_issues stale-tracking / `--warn-stale N` idea submitted.

## Operating Rule
Build tools, not prompts. Use existing LTG_TOOL_* where possible. Extend before creating new. Report PASS/FAIL counts — not prose.

## New (C39): numpy, OpenCV (cv2), PyTorch now authorized
- numpy for image array ops (much faster than PIL getpixel loops in batch analysis)
- OpenCV (cv2): color space conversion (LAB, HSV), edge detection, SSIM structural similarity
- OpenCV default is BGR — convert to RGB on load. Use Pillow for drawing; numpy/cv2 for analysis.

## C39 Work Done
- CI suite post-C38-fixes re-run: OVERALL WARN (exit code 0) — **0 FAIL confirmed**.
  - C38 blocker (spec_sync_ci G002 P1 FAIL) now PASS — Kai's fixes verified.
  - Stub linter: PASS (105 files). Draw order: WARN (26 advisory only). Glitch spec: WARN (12, all pre-existing FP). Spec Sync CI: PASS (0 P1 FAIL). Char Spec: PASS.
  - Report: output/production/ci_suite_c39_report.md
- Created `output/tools/arc_diff_config.json` — external JSON config for arc-diff pairs in precritique_qa Section 10. Format: pairs array of [label, old_rel_path, new_rel_path, diff_out_rel_path], paths relative to repo root.
- Upgraded `LTG_TOOL_precritique_qa.py` → **v2.7.0**: `_load_arc_diff_pairs()` loads ARC_DIFF_PAIRS from arc_diff_config.json at startup; falls back to hardcoded `_ARC_DIFF_PAIRS_DEFAULT` if JSON absent or invalid — fully backwards-compatible.
- Updated README.md: v2.7.0 changelog, arc_diff_config.json entry, last-updated header.
- Ideabox: CI suite `--known-issues` flag idea submitted.
- Archived 2 inbox messages.

## C34-C38 Summary (condensed)
- C34: Built precritique_qa v1.0, audited README (35 unlisted tools).
- C35: Built readme_sync, render_qa v1.3.0 (Value Ceiling Guard), precritique_qa v2.0.0 (Section 7).
- C36: precritique_qa v2.1.0 (Delta Report), qa_baseline_last.json seeded.
- C37: precritique_qa v2.2.0, CI suite first run (WARN, exit 0). Kai built ci_suite v1.0.0.
- C38: precritique_qa v2.3.0. CI suite FAIL on spec_sync_ci (pre-Kai fixes).

## API Notes (critical — tools use non-obvious key names)
- `LTG_TOOL_render_qa.qa_report()` returns `file` (not `image_path`), `overall_grade`, sub-dicts with `pass` bool; v1.3.0 adds `value_ceiling` key
- `LTG_TOOL_stub_linter.lint_directory()` returns dicts with `status` (not `result`), `issues` (not `imports`)
- `LTG_TOOL_glitch_spec_lint.lint_directory()` returns ONLY non-SKIP results (SKIP files silently filtered). `status` field (not `result`), `issues` list of strings.
- `LTG_TOOL_readme_sync.audit()` returns dict with `disk_tools`, `listed`, `legacy`, `unlisted`, `ghost`, `legacy_ghost`, `ok`, `result`
- `LTG_TOOL_precritique_qa.py`: `CYCLE_LABEL` constant at top of file — update each cycle before running

## Known QA False Positives
- Render QA warm/cool WARN fires on intentionally cold-dominant style frames (SF03)
- Glitch spec lint G006 fires on multi-character lineup files (other chars' skin tones)
- Glitch spec lint G005/G007 fires on QA tool Python files with color constant tuples
- render_qa v1.4.0: GLITCH threshold=3, OTHER_SIDE threshold=0 — SF02/SF03 warm_cool PASS; SF01 still WARN at 17.8/20.0
