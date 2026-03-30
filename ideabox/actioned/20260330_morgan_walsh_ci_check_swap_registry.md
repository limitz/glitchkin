**Author:** Morgan Walsh
**Cycle:** C48
**Date:** 2026-03-30
**Idea:** Add a check registry/manifest to ci_suite that maps check slot numbers to module functions, so swapping a check (like the C48 ext_model_check → doc_staleness replacement) is a config change rather than a code surgery. A JSON or dict-based registry would let us enable/disable checks, reorder them, and track check history without touching runner code.
**Benefits:** Reduces risk when swapping CI checks mid-cycle. Makes it easier for any team member to propose new checks without understanding ci_suite internals. Would have made the C48 swap a 2-line config edit instead of a multi-function code change.
