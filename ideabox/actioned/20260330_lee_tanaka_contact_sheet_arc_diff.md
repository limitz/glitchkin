**Author:** Lee Tanaka
**Cycle:** 36
**Date:** 2026-03-30
**Idea:** Build a contact-sheet arc-diff tool (`LTG_TOOL_contact_sheet_arc_diff_v001.py`) that takes two contact sheets (old and new version) and generates a side-by-side comparison PNG highlighting which panels changed and whether the arc-color-coded border sequence still reads coherently. Currently, comparing contact sheet versions requires manual visual inspection across two separate files. The diff tool would flag: (1) panels where thumbnail content changed significantly (pixel diff > threshold), (2) panels where the arc-color border label changed, (3) any new or removed panels. Output ≤ 800×600px.
**Benefits:** Helps Lee and Alex verify that a contact sheet revision doesn't accidentally break arc continuity. Also useful for critics who need to check "what changed since last cycle" without loading two full contact sheets. Reduces LLM vision calls in critique cycles.
