**Author:** Diego Vargas
**Cycle:** 37
**Date:** 2026-03-30
**Idea:** Add a lightweight storyboard thumbnail QA tool — `LTG_TOOL_sb_thumbnail_qa_v001.py`. The tool would take a storyboard contact sheet PNG and check: (1) are all panels visually distinct (average per-panel pixel hue variance > threshold — catches duplicate/near-duplicate panels), (2) does each panel have a readable dark annotation/caption area at bottom (checks that at least 8% of panel pixels in bottom 15% rows are below luminance 60), (3) are all panels within the expected aspect ratio range (16:9 ± 10%). Results printed as PASS/WARN/FAIL per check per panel. No LLM involved — pure pixel statistics. Currently I'm doing these checks by eye, which is slow and error-prone at thumbnail scale.
**Benefits:** Diego (storyboard) and Lee Tanaka (storyboard), plus critics who currently have no automated QA for storyboard panels. Reduces manual review time and catches issues before critique.
