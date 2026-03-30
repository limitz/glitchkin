**Author:** Kai Nakamura
**Cycle:** 35
**Date:** 2026-03-29
**Idea:** Build `LTG_TOOL_spec_sync_check_v001.py` — a CI gate that runs `LTG_TOOL_spec_extractor.py` on all character specs and then compares the extracted numeric values against the hardcoded constants in `LTG_TOOL_char_spec_lint.py`. If the spec extractor finds a head ratio that differs by >10% from the lint constant, or an eye coefficient that differs by >15%, the gate exits with code 1 and prints a clear "spec drift detected" message. This way, whenever Maya or Alex updates a spec .md file with a revised proportion, the CI run will automatically catch that the lint tool is now out of sync — no more silent drift between the spec doc and the linter. The extractor already exists (built this cycle); this tool just adds the comparison step.

**Benefits:** Protects the whole QA pipeline: ensures `char_spec_lint_v001.py` stays in sync with the canonical spec docs without manual review. Any team member who updates a spec doc will get an immediate signal that the linter also needs updating. Particularly valuable after G002 fix this cycle (which revealed a spec-doc/linter disconnect that went undetected for many cycles).
