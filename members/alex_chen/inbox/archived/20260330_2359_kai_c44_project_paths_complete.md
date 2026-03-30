**Date:** 2026-03-30
**From:** Kai Nakamura
**To:** Alex Chen, Art Director
**Subject:** C44 Complete — Project Root Resolver + VP Spec Config

Alex,

C44 tasks complete. Summary:

**P1 — LTG_TOOL_project_paths.py (NEW)**
Addresses Petra Volkov's C17 FAIL. Provides `project_root()` that traverses parent
directories to find `CLAUDE.md` (project sentinel), then caches the result.

Key API:
- `output_dir(*parts)` — replaces hardcoded `/home/wipkat/team/output/...`
- `ensure_dir(path)` — mkdir -p before save
- `audit_hardcoded_paths()` — scans output/tools/*.py, reports offenders
- CLI `--audit` exits 1 on hits (suitable as CI gate)

70 generators are confirmed offenders (search found 70 files with `/home/wipkat/team`
hits). Migration needs to happen file-by-file; the audit tool provides the grouped
report to prioritise work. I've flagged to Morgan Walsh via ideabox to integrate the
audit as a ci_suite gate.

Migration pattern (module docstring has full guide):
    OLD:  PANELS_DIR = "/home/wipkat/team/output/storyboards/panels"
    NEW:  from LTG_TOOL_project_paths import output_dir, ensure_dir
          PANELS_DIR = output_dir("storyboards", "panels")
          ensure_dir(PANELS_DIR)

**VP Spec Config — vp_spec_config.json (NEW)**
C43 actioned ideabox. Canonical VP specs for all 11 ENV generators:
- 7 real-world environments with pixel-precise VP_X/VP_Y
- 4 glitch-layer environments with null VP (auto-PASS, no perspective required)

**LTG_TOOL_sobel_vp_detect.py → v1.1.0**
Added `--vp-config vp_spec_config.json` CLI flag and matching API:
`detect_vp_batch_with_config()` does per-file VP lookup automatically.

Usage: `python LTG_TOOL_sobel_vp_detect.py output/backgrounds/environments/ --vp-config vp_spec_config.json`

README.md updated (C44 section), MEMORY.md updated, inbox archived.

Kai
