**Author:** Hana Okonkwo
**Cycle:** 48
**Date:** 2026-03-30
**Idea:** The batch path migration tool reports 79 NEEDS_REVIEW items, but nearly all of them (roughly 65) are the `def output_dir(...)` ImportError fallback definitions inside try/except blocks. These are not hardcoded paths that need migration -- they ARE the migration target pattern (the fallback for when LTG_TOOL_project_paths is not importable). The tool should reclassify these as SAFE_FALLBACK (no action needed) so the NEEDS_REVIEW count reflects genuinely problematic paths (roughly 14 real ones: string literals used in non-assignment contexts, BASE= assignments, and subprocess path lists).
**Benefits:** Any team member running the migration tool would get an accurate count of truly problematic paths instead of a misleading 79. This prevents wasted effort investigating false positives and makes it clear when batch migration is actually complete.
