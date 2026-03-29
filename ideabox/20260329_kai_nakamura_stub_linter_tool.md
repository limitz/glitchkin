**Author:** Kai Nakamura
**Cycle:** 32
**Date:** 2026-03-29
**Idea:** Build a stub-integrity linter tool (`LTG_TOOL_stub_linter.py`) that scans all files in `output/tools/` for broken imports — specifically any `from LTG_CHAR_* import` or `from LTG_COLOR_* import` that reference deleted original generators. It should output a clear report: which stubs are broken, what they import, and whether a canonical `LTG_TOOL_*` replacement exists. Run it as a pre-commit check to catch regressions before they accumulate across cycles. The C32 P1 task required manually hunting down 8 broken stubs; this tool would catch them instantly and prevent another C29-style cleanup from silently breaking the pipeline.
**Benefits:** Saves the next engineer hours of manual grep work. Protects all team members who call generators from silent ImportErrors at runtime. Would have prevented the entire C32 P1 critical backlog.
