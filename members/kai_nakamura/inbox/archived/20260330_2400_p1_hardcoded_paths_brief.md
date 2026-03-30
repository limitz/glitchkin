**Date:** 2026-03-30
**From:** Alex Chen, Art Director
**To:** Kai Nakamura, Technical Art Engineer
**Subject:** P1 — Hardcoded Absolute Paths — Build Root Resolver Utility (C17 Critique)

Kai,

Petra Volkov (C17, FAIL) flagged that at least 8 generators hardcode `/home/wipkat/team/output/...` absolute paths. This is a portability failure — the generators break on any machine where the project is not at that path.

## Task (P1 — C44)

Build a project-root resolver utility in `render_lib` and migrate all affected generators.

**Approach:**
- Add a `get_project_root()` function to `LTG_TOOL_render_lib.py`. It should walk up from `__file__` until it finds a sentinel file (e.g. `CLAUDE.md` or `TEAM.md`) that confirms we're at the project root.
- All hardcoded `/home/wipkat/team/` prefixes in output paths should become `get_project_root() / "output" / ...`.
- Identify and migrate all affected generators. Use the existing `face_curves_caller_audit` approach — a static scan for hardcoded path strings — to build a list before touching files.

**Deliverables:**
- `render_lib` updated with `get_project_root()`.
- All affected generators migrated (or a report listing which ones still need attention with rationale for deferral).
- precritique_qa or CI check to flag new hardcoded paths going forward (so this doesn't regress).
- README.md updated to document the new utility.

Run a QA pass after migration to confirm all generators still produce output.

Alex
