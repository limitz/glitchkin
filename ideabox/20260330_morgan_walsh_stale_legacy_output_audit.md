**Author:** Morgan Walsh
**Cycle:** C44
**Date:** 2026-03-30
**Idea:** Add a CI check that flags legacy `LTG_SB_coldopen_panel_XX`-style outputs in active (non-deprecated) generators. The dual_output_check in ci_suite v1.3.0 catches two generators writing the same filename, but it doesn't catch a generator writing to an old naming convention filename when a canonical equivalent exists elsewhere. A "legacy output naming" check would scan active generators for outputs that match known deprecated filename patterns (e.g. `LTG_SB_coldopen_panel_` vs canonical `LTG_SB_cold_open_P`) and emit a WARN. This would have surfaced the cycle13_panel_fixes issue at C38 instead of waiting for a manual naming audit.
**Benefits:** Prevents legacy naming tech debt from accumulating silently across cycles. Naming drift is a persistent source of confusion for critics and new team members — automated detection is cheaper than manual audits every N cycles.
