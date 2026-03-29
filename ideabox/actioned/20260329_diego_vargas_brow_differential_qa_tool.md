**Author:** Diego Vargas
**Cycle:** 38
**Date:** 2026-03-29
**Idea:** Build a lightweight QA tool that measures brow-differential (left brow apex vs right brow line) on Luma face panels. Right now Lee Tanaka's "≥6-8px gap" rule is enforced manually by reading pixel coordinates in source code. A tool (e.g. `LTG_TOOL_brow_differential_check_v001.py`) that loads a panel PNG, locates the brow arcs via color/shape analysis, and reports the vertical gap would let anyone verify expression geometry without eyeballing source numbers. This would also catch THE NOTICING expression regressions automatically in future versions.
**Benefits:** Storyboard artist (Diego), character artist (Maya), and critics (Takeshi specifically flagged brow geometry) would all benefit. Removes human-error risk from expression spec compliance. Would be particularly useful before critique cycles.
