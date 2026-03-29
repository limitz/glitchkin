**Author:** Rin Yamamoto
**Cycle:** 30
**Date:** 2026-03-29
**Idea:** Build a `LTG_TOOL_proportion_audit_v001.py` that programmatically loads each styleframe generator, extracts the `head_r` (or HR equivalent) and `ew` values, and prints a table showing actual vs canonical ratios (ew/HR, total_height/HR). No image needed — just parse the AST or import the module and inspect numeric constants. This would catch ew, HR, height-ratio mismatches across all SF generators before critique, without needing to visually inspect any image.
**Benefits:** Alex and I both spent time on proportion verification this cycle (C30) that could be automated. A one-run audit across all SF generators would flag any generator that drifts from canonical spec (ew = HR*0.22, 3.2 heads). Saves review time every cycle, especially as more style frames are added. Would be a shared tool in output/tools/.
