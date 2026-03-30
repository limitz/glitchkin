**Author:** Hana Okonkwo
**Cycle:** C46
**Date:** 2026-03-30
**Idea:** Run a systematic audit of all ENV generators for hardcoded /home/wipkat/team paths and migrate them to output_dir() from LTG_TOOL_project_paths in a single sweep. This cycle I migrated tech_den and grandma_living_room. The ci_known_issues.json still lists classroom (LTG_TOOL_bg_classroom.py) and school_hallway (LTG_TOOL_bg_school_hallway.py) as C44 backlog items. The audit tool at LTG_TOOL_project_paths.py --audit can identify remaining violators automatically. One pass would close all remaining ENV hardcoded path known issues and remove their entries from ci_known_issues.json.
**Benefits:** Keeps the ENV generator suite portable across machines. Reduces noise in ci_known_issues.json (currently 4+ ENV entries that are clearly backlog rather than genuine known-issue suppressions). Morgan Walsh's CI check 7 will report PASS rather than KNOWN for these files once migrated.
