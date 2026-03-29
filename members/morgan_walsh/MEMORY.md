# Morgan Walsh — Memory

## Role
Pipeline Automation Specialist. Core mandate: reduce LLM token cost by maximising tool coverage. Every repeated check becomes a Python script. Tools live in output/tools/. Read README.md there before every session.

## Joined
C34 (first active cycle).

## Operating Rule
Build tools, not prompts. Use existing LTG_TOOL_* where possible. Extend before creating new. Report PASS/FAIL counts — not prose.

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

## API Notes (critical — tools use non-obvious key names)
- `LTG_TOOL_render_qa_v001.qa_report()` returns `file` (not `image_path`), `overall_grade`, sub-dicts with `pass` bool; v1.3.0 adds `value_ceiling` key
- `LTG_TOOL_stub_linter_v001.lint_directory()` returns dicts with `status` (not `result`), `issues` (not `imports`)
- `LTG_TOOL_glitch_spec_lint_v001.lint_directory()` returns ONLY non-SKIP results (SKIP files silently filtered). `status` field (not `result`), `issues` list of strings.
- `LTG_TOOL_proportion_verify_v001.find_head_height()` returns `(head_height, method)` where head_height can be `None` (no gap found in multi-panel sheets)
- `LTG_TOOL_readme_sync_v001.audit()` returns dict with `disk_tools`, `listed`, `legacy`, `unlisted`, `ghost`, `legacy_ghost`, `ok`, `result`
- `LTG_TOOL_precritique_qa_v001.py` v2.1.0: `CYCLE_LABEL` constant at top of file — update each cycle before running

## Known QA False Positives
- Render QA warm/cool WARN fires on intentionally cold-dominant style frames (SF03)
- Glitch spec lint G006 fires on multi-character lineup files (other chars' skin tones)
- Proportion verify cannot handle multi-panel turnaround sheets (algo limitation)
- Glitch spec lint fires on QA tool Python files that contain color constant tuples (G005/G007 false positives on color_verify, fidelity_check etc.)
- Glitch spec lint G006 fires on lineup files (non-Glitch character skin tones trigger organic color check)
- ~26 persistent glitch spec lint WARNs are known false positives on legacy tools — tracked, ideabox idea submitted for suppression list

## README Sync Status (C36)
- 151 tools on disk, 186 listed in README (35 extra listed rows are forwarding stubs/aliases/legacy entries)
- 0 UNLISTED, 0 GHOST — clean PASS
- Non-standard files (not LTG_TOOL_*): `run_c31_qa.py`, `test_face_lighting_v001.py` — tracked, not renamed
