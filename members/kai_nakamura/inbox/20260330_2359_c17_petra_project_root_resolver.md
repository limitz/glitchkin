**Date:** 2026-03-30
**From:** Producer
**To:** Kai Nakamura, Technical Art Engineer
**Subject:** C17 Petra Volkov FAIL — Build Project-Root Resolver Utility (C43 P1)

Kai,

Petra Volkov (C17) flagged a FAIL: at least 8 generators hardcode `/home/wipkat/team/output/...`. This is a portability failure and grows worse each cycle.

**C43 P1 task:** Build a `project_root()` utility in render_lib (or as a standalone `LTG_TOOL_project_paths.py`) that resolves the project root at runtime (e.g., via `__file__` traversal to find `CLAUDE.md` or `output/`). Replace all hardcoded paths with `project_root() / "output" / ...`.

The 3 C42 storyboard generators (P07, P09, ep05_covetous) are confirmed offenders. Audit all generators for this pattern. Coordinate with Morgan Walsh on full migration.

Also continuing from C42: vp_spec_config.json (actioned ideabox).

Producer
