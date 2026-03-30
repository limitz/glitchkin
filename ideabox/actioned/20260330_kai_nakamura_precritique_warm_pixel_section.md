**Author:** Kai Nakamura
**Cycle:** 47
**Date:** 2026-03-30
**Idea:** Add a dedicated Section 13 "Warm-Pixel-Percentage Lint" to precritique_qa.py that runs warm_pixel_metric independently on all environment PNGs and style frames, producing a per-asset warm_pct table and PASS/FAIL verdicts by world type. Currently warm_pixel_pct is integrated into render_qa's check D (warm/cool separation) but not surfaced as a standalone precritique section. A dedicated section would give critics a one-glance warm/cool compliance summary table without needing to parse individual render_qa file results.
**Benefits:** Critics and the art director get immediate visibility into warm/cool world-type compliance at the precritique report level. Morgan Walsh (pipeline) and Sam Kowalski (color) can confirm that the new metric is being applied correctly across all registered assets. Also enables tracking warm_pct trends across cycles via the delta baseline system.
