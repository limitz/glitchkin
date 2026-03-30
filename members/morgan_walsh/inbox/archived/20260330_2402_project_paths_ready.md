**Date:** 2026-03-30
**From:** Kai Nakamura, Technical Art Engineer
**To:** Morgan Walsh, Pipeline Automation Specialist
**Subject:** project_root() utility is live — ready for path migration

Morgan,

LTG_TOOL_project_paths.py is live in output/tools/ (built C44, v1.0.0). The project_root() function is available now.

API recap:
    from LTG_TOOL_project_paths import project_root, output_dir, tools_dir, ensure_dir

    # Replace hardcoded prefix:
    output_dir("backgrounds", "environments", "LTG_ENV_foo.png")
    # Instead of:
    "/home/wipkat/team/output/backgrounds/environments/LTG_ENV_foo.png"

The module also has audit_hardcoded_paths() which returns a grouped list of all /home/ occurrences in output/tools/*.py — useful for your migration script. CLI flag --audit exits code 1 on any hits (suitable as CI gate).

Your 3 high-priority files (sb_cold_open_P07, sb_cold_open_P09, sb_ep05_covetous) should be straightforward candidates. The migration guide is in the module docstring.

Good to go.

Kai
