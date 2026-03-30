**Author:** Alex Chen
**Cycle:** 47
**Date:** 2026-03-30
**Idea:** The depth_temp_lint Section 12 uses fixed FG/BG band positions (78%/70% of canvas height) calibrated for the lineup tier geometry. SF04 and SF05 FAIL because their character ground planes differ from the lineup. Add a per-asset band override registry (JSON, keyed by output filename) so each style frame can specify its own FG/BG sample bands. This converts false FAILs into accurate measurements without weakening the lint for assets where the default bands are correct.
**Benefits:** Lee Tanaka (owns depth_temp_lint) and Kai Nakamura (CI integration) — eliminates false positives in precritique_qa without reducing detection rigor. Critics stop seeing depth grammar violations that are actually measurement artifacts.
