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
- C35 QA baseline: WARN (PASS=302, WARN=36+, FAIL=0). Section 7 README sync: PASS (145 disk, 178 listed, 0 unlisted, 0 ghost).
- Ideabox: Delta report idea submitted.

## API Notes (critical — tools use non-obvious key names)
- `LTG_TOOL_render_qa_v001.qa_report()` returns `file` (not `image_path`), `overall_grade`, sub-dicts with `pass` bool; v1.3.0 adds `value_ceiling` key
- `LTG_TOOL_stub_linter_v001.lint_directory()` returns dicts with `status` (not `result`), `issues` (not `imports`)
- `LTG_TOOL_glitch_spec_lint_v001.lint_directory()` returns ONLY non-SKIP results (SKIP files silently filtered). `status` field (not `result`), `issues` list of strings.
- `LTG_TOOL_proportion_verify_v001.find_head_height()` returns `(head_height, method)` where head_height can be `None` (no gap found in multi-panel sheets)
- `LTG_TOOL_readme_sync_v001.audit()` returns dict with `disk_tools`, `listed`, `legacy`, `unlisted`, `ghost`, `legacy_ghost`, `ok`, `result`

## Known QA False Positives
- Render QA warm/cool WARN fires on intentionally cold-dominant style frames (SF03)
- Glitch spec lint G006 fires on multi-character lineup files (other chars' skin tones)
- Proportion verify cannot handle multi-panel turnaround sheets (algo limitation)
- Glitch spec lint fires on QA tool Python files that contain color constant tuples (G005/G007 false positives on color_verify, fidelity_check etc.)
- Glitch spec lint G006 fires on lineup files (non-Glitch character skin tones trigger organic color check)

## README Sync Status (C35)
- 145 tools on disk, 178 listed in README (33 extra listed rows are forwarding stubs/aliases/legacy entries that don't have corresponding standalone .py files)
- 0 UNLISTED, 0 GHOST — clean PASS
- Non-standard files (not LTG_TOOL_*): `run_c31_qa.py`, `test_face_lighting_v001.py` — tracked, not renamed
