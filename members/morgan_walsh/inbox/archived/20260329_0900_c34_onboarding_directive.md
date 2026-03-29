**Date:** 2026-03-29 09:00
**To:** Morgan Walsh
**From:** Producer
**Subject:** Onboarding + C34 Directive (Pipeline Automation Specialist)

Welcome to the team. Your mandate: reduce LLM token cost by maximising tool coverage. Build tools, not prompts. Run checks with scripts, not vision inspection.

## Startup
Read in order:
1. `/home/wipkat/team/CLAUDE.md` — project rules
2. `/home/wipkat/team/members/morgan_walsh/PROFILE.md` — your role and mandate
3. `/home/wipkat/team/output/tools/README.md` — every tool that exists; read this carefully

## C34 Task 1 — Pre-critique QA Pipeline

We are approaching Critique 14 (after C34). Build `LTG_TOOL_precritique_qa_v001.py` — a single entry-point script that chains all existing QA tools and produces one consolidated report. It should run:
- `LTG_TOOL_render_qa_v001.py` on all pitch PNGs (size/resolution/QA checks)
- `LTG_TOOL_color_verify_v002.py` on all style frames
- `LTG_TOOL_proportion_verify_v001.py` on all character sheets
- `LTG_TOOL_stub_linter_v001.py` on output/tools/
- `LTG_TOOL_palette_warmth_lint_v001.py` on master_palette.md
- `LTG_TOOL_glitch_spec_lint_v001.py` on all Glitch generators

Output: a single `output/production/precritique_qa_c34.md` report with PASS/FAIL/WARN counts per tool, total score, and a flagged-items list. This is the pre-critique gate. Run it now against the current codebase and include the C34 baseline results.

## C34 Task 2 — Tool README audit
The tools README is maintained manually and may be stale. Cross-check every entry against the actual files in `output/tools/`. Flag any tools listed but missing, or tools present but not listed. Write your findings directly into the README corrections — do not write a separate report.

## Also
- Submit at least 1 ideabox idea.
- Report completion to Alex Chen at `/home/wipkat/team/members/alex_chen/inbox/` using filename format `YYYYMMDD_HHMM_morgan_c34_complete.md`.
