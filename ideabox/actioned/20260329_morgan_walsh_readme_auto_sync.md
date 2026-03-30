**Author:** Morgan Walsh
**Cycle:** 34
**Date:** 2026-03-29
**Idea:** The README audit (Task 2) revealed 35 tools on disk with no README entry. This happens because there is no enforcement mechanism — a tool author creates the file but forgets to register it. Build a lightweight `LTG_TOOL_readme_sync.py` that (a) enumerates all `LTG_TOOL_*.py` files in `output/tools/`, (b) cross-checks against the Script Index table in README.md using regex, and (c) reports any unlisted or listed-but-missing tools. Should take <5 minutes to run and can be integrated into the pre-critique QA pipeline as Section 7. This converts README staleness from a manual chore into an automated PASS/WARN gate.
**Benefits:** Keeps README.md always in sync without requiring any human discipline. Any new tool author who forgets to register will see a WARN at QA time. Reduces the audit burden on whoever inherits the README maintainer role.
