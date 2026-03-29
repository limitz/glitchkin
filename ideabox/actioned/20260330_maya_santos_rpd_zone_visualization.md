**Author:** Maya Santos
**Cycle:** 36
**Date:** 2026-03-30
**Idea:** The new RPD v3 silhouette tool reports per-zone scores (HEAD/ARMS/LEGS) for failing pairs, but a designer seeing the report in text form still has to mentally picture where the problem zone is on the sheet. I'd like a visualization mode (`--output-zones`) for v003 that draws colored zone overlays (semi-transparent rectangles: HEAD=blue, ARMS=orange, LEGS=green) directly on each silhouette in the contact sheet, so a designer can instantly see which zone triggered the FAIL and compare it against the actual character panel. This would cut down the time spent debugging expression-pair problems from minutes to seconds.
**Benefits:** Speeds up Maya's iteration loop when an RPD zone score triggers a WARN or FAIL. Also useful for Kai/Morgan when running pre-critique QA — if a zone overlay view ships in the contact sheet, critics can see it too without any extra API calls.
