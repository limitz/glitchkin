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

## API Notes (critical — tools use non-obvious key names)
- `LTG_TOOL_render_qa_v001.qa_report()` returns `file` (not `image_path`), `overall_grade`, sub-dicts with `pass` bool
- `LTG_TOOL_stub_linter_v001.lint_directory()` returns dicts with `status` (not `result`), `issues` (not `imports`)
- `LTG_TOOL_glitch_spec_lint_v001.lint_directory()` returns ONLY non-SKIP results (SKIP files silently filtered). `status` field (not `result`), `issues` list of strings.
- `LTG_TOOL_proportion_verify_v001.find_head_height()` returns `(head_height, method)` where head_height can be `None` (no gap found in multi-panel sheets)

## Known QA False Positives
- Render QA warm/cool WARN fires on intentionally cold-dominant style frames (SF03)
- Glitch spec lint G006 fires on multi-character lineup files (other chars' skin tones)
- Proportion verify cannot handle multi-panel turnaround sheets (algo limitation)
