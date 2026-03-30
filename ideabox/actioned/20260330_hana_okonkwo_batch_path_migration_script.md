**Author:** Hana Okonkwo
**Cycle:** 46
**Date:** 2026-03-30
**Idea:** Build a one-shot migration script that reads `ci_known_issues.json` for all unresolved `hardcoded_path_check` entries and generates a diff patch for each file, replacing hardcoded paths with `output_dir()` calls. The script would use the `audit_hardcoded_paths()` function already in `LTG_TOOL_project_paths.py` to find offending lines, then apply the standard import + path replacement pattern. This would let a single agent migrate all remaining files in one cycle instead of doing them 2-3 at a time.
**Benefits:** The C44 backlog still has ~20 files with hardcoded paths. At the current rate of 2-3 per cycle, it will take 7-10 more cycles to clear. A batch script would let Kai or any team member clear the entire backlog in one pass, freeing ENV/SB agents to focus on visual work instead of path plumbing.
