**Author:** Jordan Reed
**Cycle:** 46
**Date:** 2026-03-30
**Idea:** Add a CORRUPT_AMBER detection mode to `LTG_TOOL_color_verify.py` that specifically validates fringe-band pixels: checks that GL-07 (#FF8C00) in Real World scenes only appears at alpha <= 38, only within the CRT glow bounding box, and only in a band no taller than sp(6). This would catch accidental full-opacity GL-07 leaks in Real World environments while whitelisting the intentional fringe. Currently color_verify treats all GL palette in Real World as either pass or fail globally — it cannot distinguish the sanctioned fringe from a genuine palette violation.
**Benefits:** Sam Kowalski (color QA) gets automated fringe validation instead of manual checking. Hana Okoro and any future environment artists adding CRT portals get immediate feedback if their fringe exceeds spec. Prevents false positives in precritique QA runs.
