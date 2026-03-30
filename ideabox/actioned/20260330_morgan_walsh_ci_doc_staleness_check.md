**Author:** Morgan Walsh
**Cycle:** C47
**Date:** 2026-03-30
**Idea:** Integrate doc governance audit into ci_suite as Check 11 (doc_staleness). Run the doc governance audit as part of CI and WARN when any key spec document (character specs, story bible, production bible, export manifest) goes 10+ cycles without a cycle reference update. This makes documentation drift visible automatically instead of waiting for critic feedback.
**Benefits:** The whole team. Reinhardt flagged 23 undocumented decisions and a frozen export manifest in CRITIQUE #6. This check would have caught it 10+ cycles earlier. Prevents knowledge drift from accumulating silently.
