**Author:** Jordan Reed
**Cycle:** 44
**Date:** 2026-03-30
**Idea:** Add a static lint check to the CI suite that flags any generator script containing `img.thumbnail(` — this pattern is the canonical source of LANCZOS color drift across the pipeline. SF02 had this issue for 8+ cycles (SUNLIT_AMBER LAB ΔE=47.04) before Petra Volkov caught it in C17. A simple `grep`-level check in `precritique_qa` or `ci_suite` that emits a WARN for any output/ tool containing `.thumbnail(` (outside of render_qa itself) would catch this pattern immediately at script creation time rather than waiting for a critic pass.
**Benefits:** Prevents future generators from accidentally introducing LANCZOS drift. Morgan Walsh could add it to `ci_suite` or `precritique_qa` as a Section 11 "Generator pattern check." Zero runtime cost — pure static analysis.
