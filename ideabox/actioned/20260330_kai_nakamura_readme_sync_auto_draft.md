**Author:** Kai Nakamura
**Cycle:** 46
**Date:** 2026-03-30
**Idea:** Add a `--draft-entry` flag to `LTG_TOOL_readme_sync.py` that, for each UNLISTED tool found on disk, reads the file's module docstring and auto-generates a draft Script Index table row. The draft would pre-fill: script name, creator name (from first `# [Name]` line or `Artist:` field in docstring), cycle number (from `Cycle N` in docstring), and a one-sentence description from the first paragraph. Output the drafts to stdout or `--draft-output PATH` for human review. This would reduce the manual effort of README catch-up passes (like this C46 pass where 7+ entries needed manual extraction from tool headers).
**Benefits:** Speeds up README maintenance for Diego Vargas, Lee Tanaka, and any other high-volume producers. Reduces the multi-cycle lag between tool creation and README registration. Reduces the risk of incorrect attribution when entries are written manually from memory.
