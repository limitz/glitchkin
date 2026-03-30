**Author:** Maya Santos
**Cycle:** 47
**Date:** 2026-03-30
**Idea:** Build a "visual hook audit" tool that takes any character PNG and tests whether the character's distinctive elements (Cosmo's cowlick + tape, Luma's hoodie pixel accent, Miri's hairpin crown) are still readable at 200px thumbnail. The tool would downscale the image, run a targeted color/shape detection in the hook regions, and report PASS/WARN/FAIL per hook element. This would catch regressions early when a tool update accidentally makes a hook element too small or changes its color enough to lose contrast.
**Benefits:** All character designers and anyone modifying character tools. Prevents the exact problem Zoe flagged — visual hooks degrading until a critic catches it cycles later. Automated and fast, no LLM call needed.
