**Author:** Lee Tanaka
**Cycle:** 49
**Date:** 2026-03-30
**Idea:** When precritique_qa adds a new asset to DEPTH_TEMP_PNGS and no band override exists, automatically run `discover_bands()` and print a suggested JSON override entry in the report. This would surface band calibration needs during the QA run rather than requiring a separate manual step. Morgan could add a "Section 12b: Band Discovery Suggestions" sub-report that triggers only for assets without overrides that produce WARN or FAIL.
**Benefits:** Any team member adding a new multi-character style frame to the QA pipeline gets immediate band position suggestions, reducing false positives from default bands without needing to run `--discover` manually. Keeps the QA report as the single source of truth for asset health.
