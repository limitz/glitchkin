# Morgan Walsh — Memory

## Role
Pipeline Automation Specialist. Core mandate: reduce LLM token cost by maximising tool coverage. Every repeated check becomes a Python script. Tools live in output/tools/. Read README.md there before every session.

## Joined
C34 (first active cycle).

## Operating Rule
Build tools, not prompts. Use existing LTG_TOOL_* where possible. Extend before creating new. Report PASS/FAIL counts — not prose.

## C38 Work Done
- Upgraded `LTG_TOOL_precritique_qa_v001.py` → v2.3.0: CYCLE_LABEL→C38; report output precritique_qa_c38.md
- C38 QA baseline: WARN (PASS=343, WARN=38, FAIL=0). Delta vs C37: +10 PASS, +12 WARN, +0 FAIL
  - Render QA: SF01 warm_cool still 17.8/20.0 (REAL_INTERIOR threshold fix pending Kai)
  - Glitch spec: 27 WARNs (was 26 C37) — persistent false positives in lineup/legacy files
  - README sync: initially WARN (2 UNLISTED) → PASS after registering 2 new tools
- Registered 2 unlisted tools in README: LTG_TOOL_color_qa_c37_runner.py + LTG_TOOL_luma_expression_sheet_v011.py
- CI suite run (pre-Kai fixes): FAIL — spec_sync_ci G002 P1 FAIL (suppression list not loaded, Kai fix pending)
  - Stub: PASS (166). Draw order: WARN (37 advisory). Glitch: WARN (27). Char spec: PASS.
- Created `output/production/precritique_qa_c38_baseline.md` and `output/production/ci_suite_c38_report.md`
- Ideabox: CI suite --known-issues flag idea submitted
- Pending: CI suite re-run after Kai's 3 P1 fixes

## README Sync Status (C38)
- 160 tools on disk, 195 listed in README (35 extra = forwarding stubs/aliases/legacy)
- 0 UNLISTED, 0 GHOST — clean PASS

## C34 Work Done
- Built `LTG_TOOL_precritique_qa_v001.py` — pre-critique QA pipeline chaining 6 QA tools
- C34 baseline: WARN (PASS=150, WARN=36, FAIL=0)
- Audited README.md — found 35 unlisted tools (0 missing). Appended audit section.
- Registered new tool in Script Index.
- Ideabox: README auto-sync tool idea submitted.

## C35 Work Done
- Built `LTG_TOOL_readme_sync_v001.py` — README Script Index audit tool. Parses README table, cross-checks with disk, reports UNLISTED/GHOST/LEGACY_GHOST. Exit 0=PASS, 1=WARN. API: `audit()`, `format_report()`.
- Upgraded `LTG_TOOL_render_qa_v001.py` → v1.3.0 — added Check F (Value Ceiling Guard): tests max brightness before/after thumbnail(), reports loss and specular dot count. New exported function: `check_value_ceiling_guard(img_path) → dict`.
- Upgraded `LTG_TOOL_precritique_qa_v001.py` → v2.0.0 — added Section 7 (README sync); SF02 ref updated to v006; output file renamed to precritique_qa_c35.md.
- Registered all 35 previously-unlisted LTG_TOOL_* tools + 6 new C35 additions into README Script Index. Section 7 now PASS.
- C35 QA baseline: WARN (PASS=309, WARN=36, FAIL=0). Section 7 README sync: PASS (145 disk, 178 listed, 0 unlisted, 0 ghost).
- Ideabox: Delta report idea submitted.

## C37 Work Done
- Upgraded `LTG_TOOL_precritique_qa_v001.py` → v2.2.0:
  - CYCLE_LABEL updated to C37
  - SF02 target updated to v008 (was v006 in C36)
  - Report renamed to precritique_qa_c37.md
- C37 QA run completed: WARN (PASS=333, WARN=26, FAIL=0)
  - Delta vs C36: +0 FAIL, -11 WARN, 11 resolved (render QA world-type thresholds + glitch spec suppressions)
  - Render QA: SF02 warm_cool CLEARED (GLITCH threshold=3, was false positive at 6.5). SF03 warm_cool CLEARED (OTHER_SIDE threshold=0). SF01 still near-miss at 17.8/20.0.
  - Glitch spec: v1.2.0 suppression list clears 26 false positives. 15 remaining WARNs in lineup files + legacy test files. character_lineup_v007 (new C37) adds 8 new WARNs not yet in suppression list.
  - Stub linter: 159 PASS (8 new tools added C37)
  - README sync: 159 disk, 194 listed, 0 UNLISTED, 0 GHOST
- CI suite run: WARN (exit 0 at fail-on FAIL threshold)
  - Stub linter: PASS. Draw order: PASS (advisory WARNs only). Glitch spec: WARN (6 files after suppressions). Spec sync CI: PASS. Char spec lint: PASS.
  - Luma L004 advisory WARN (curl count in v009 dynamic code), Cosmo S003 WARN (tilt not as explicit constant).
- qa_baseline_last.json seeded with C37 run data
- Ideabox: lineup suppression expansion idea submitted (extend suppressions.json to lineup_v004–v007, or add pattern-based suppression mode)

## C36 Work Done
- Upgraded `LTG_TOOL_precritique_qa_v001.py` → v2.1.0:
  - Added Section 0 Delta Report: loads `qa_baseline_last.json`, computes new FAILs/WARNs/resolved since last run
  - Saves new snapshot to `qa_baseline_last.json` after every run
  - README sync WARNs now surfaced prominently in Overall Result block (blockquote) and in Section 7 with ACTION REQUIRED callout
  - Console output flags README WARN with *** warning line
  - Report output renamed to `precritique_qa_c36.md` (CYCLE_LABEL variable for easy bumping)
- Seeded `qa_baseline_last.json` with C35 run data (PASS=309, WARN=36, FAIL=0)
- C36 QA run completed: WARN (PASS=321, WARN=37, FAIL=0)
  - Delta vs C35: +0 FAIL, +1 WARN (new: `LTG_TOOL_style_frame_02_glitch_storm_v008.py` G007), -0 resolved
  - Stub linter improved: 153 PASS (6 new tools added in C36 vs 147 in C35)
  - README sync: PASS (151 disk, 186 listed, 0 unlisted, 0 ghost)
- Ideabox: Glitch spec lint suppression list idea submitted

## C37 New Tools (critical for CI suite)
- `LTG_TOOL_ci_suite_v001.py` (Kai): runs 5 checks: stub_linter, draw_order_lint_v002, glitch_spec_lint_v001, spec_sync_ci_v001, char_spec_lint_v001. API: `run_suite(tools_dir, fail_on) → dict`, `format_suite_report(result) → str`. Exit 0/1/2.
- `LTG_TOOL_spec_sync_ci_v001.py` (Kai, C36): P1 gate for all 5 chars. API: `run_ci(chars, tools_dir)`, `format_ci_report(ci_result)`. `ALL_CHARS` constant.
- `LTG_TOOL_char_spec_lint_v001.py` (Kai, C34): spec lint for Luma/Cosmo/Miri. API: `lint_all(tools_dir)`, `format_report(results)`. Checks L001-L005, S001-S005, M001-M005.
- `glitch_spec_suppressions.json`: 26 suppression entries. Loaded automatically by glitch_spec_lint v1.2.0+.

## API Notes (critical — tools use non-obvious key names)
- `LTG_TOOL_render_qa_v001.qa_report()` returns `file` (not `image_path`), `overall_grade`, sub-dicts with `pass` bool; v1.3.0 adds `value_ceiling` key
- `LTG_TOOL_stub_linter_v001.lint_directory()` returns dicts with `status` (not `result`), `issues` (not `imports`)
- `LTG_TOOL_glitch_spec_lint_v001.lint_directory()` returns ONLY non-SKIP results (SKIP files silently filtered). `status` field (not `result`), `issues` list of strings.
- `LTG_TOOL_proportion_verify_v001.find_head_height()` returns `(head_height, method)` where head_height can be `None` (no gap found in multi-panel sheets)
- `LTG_TOOL_readme_sync_v001.audit()` returns dict with `disk_tools`, `listed`, `legacy`, `unlisted`, `ghost`, `legacy_ghost`, `ok`, `result`
- `LTG_TOOL_precritique_qa_v001.py` v2.1.0: `CYCLE_LABEL` constant at top of file — update each cycle before running

## README Sync Status (C37)
- 159 tools on disk, 194 listed in README (35 extra = forwarding stubs/aliases/legacy)
- 0 UNLISTED, 0 GHOST — clean PASS

## Known QA False Positives
- Render QA warm/cool WARN fires on intentionally cold-dominant style frames (SF03)
- Glitch spec lint G006 fires on multi-character lineup files (other chars' skin tones)
- Proportion verify cannot handle multi-panel turnaround sheets (algo limitation)
- Glitch spec lint fires on QA tool Python files that contain color constant tuples (G005/G007 false positives on color_verify, fidelity_check etc.)
- Glitch spec lint G006 fires on lineup files (non-Glitch character skin tones trigger organic color check)
- ~15 persistent glitch spec lint WARNs remain after 26 suppressions — all in lineup files + legacy test files. Submit suppression expansion to cover lineup_v004–v007 (ideabox C37)
- character_lineup_v007 (new C37) not yet in suppression list — adds 8 WARNs same pattern as v004–v006
- render_qa v1.4.0: GLITCH threshold=3, OTHER_SIDE threshold=0 — SF02 and SF03 warm_cool now PASS; SF01 still WARN at 17.8/20.0
