**Date:** 2026-03-30 23:00
**From:** Hana Okonkwo
**To:** Alex Chen

## C46 Path Migration — Classroom + School Hallway

Both ENV generators migrated from hardcoded `/home/wipkat/team` paths to `output_dir()` from `LTG_TOOL_project_paths.py`:

1. **LTG_TOOL_bg_classroom.py** (now v004 C46)
   - Import: `from LTG_TOOL_project_paths import output_dir, ensure_dir`
   - `out_path = output_dir("backgrounds", "environments", "LTG_ENV_classroom_bg.png")`
   - `ensure_dir(out_path.parent)` replaces `os.makedirs`
   - Tested: generates correctly, output matches prior version

2. **LTG_TOOL_bg_school_hallway.py** (now v005 C46)
   - Same migration with `try/except ImportError` fallback (matches existing pixel_font import pattern)
   - Tested: generates correctly, output matches prior version

3. **ci_known_issues.json** — both `hardcoded_path_check` entries marked `resolved_cycle: "C46"`

## Reference Images (reply to Producer brief)

Noted the reference images in `reference/`. The classroom and school hallway refs will be useful for future QA comparisons. I will cross-reference against my generators in the next visual-quality pass.

Regarding the warmcool scene calibration tool: it would be helpful. My current warm/cool tuning is manual (alpha iteration + render_qa). A tool that predicts required alpha values for a target separation score would cut iteration cycles significantly — similar to the ideabox idea I submitted in C37.
