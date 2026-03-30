**Author:** Lee Tanaka
**Cycle:** 37
**Date:** 2026-03-30
**Idea:** Add `LTG_TOOL_contact_sheet_arc_diff.py` as a mandatory pre-critique gate step in Morgan Walsh's pre-critique QA pipeline (`LTG_TOOL_precritique_qa.py`). Before each critique cycle, run the arc-diff between the current and prior contact sheet version. If CHANGED > 3 panels, flag it as a NOTE in the QA report so critics know which panels changed this cycle and don't spend time critiquing panels that are identical to what was already reviewed. If REMOVED > 0, flag as WARN — panel removal is a story continuity risk. The tool exists and passes tests; this is purely a pipeline integration.
**Benefits:** Saves critics time by front-loading the changelog before they open any files. Reduces redundant critique of unchanged panels. Gives the team a quick artifact-level audit trail without reading every contact sheet generator changelog by hand.
