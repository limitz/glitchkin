**Author:** Alex Chen
**Cycle:** 41
**Date:** 2026-03-30
**Idea:** Build `LTG_TOOL_pitch_arc_lint.py` — a tool that measures the warm/cool arc across the full pitch package (SF01→SF02→SF03→SF04) and asserts it follows the correct directional progression. SF04's warm/cool collapse to 1.1 went undetected for two cycles because no tool checked the cross-frame arc — only individual frame linting. The pitch arc lint would: load all 4 style frame PNGs, extract warm/cool ratios via render_qa, then assert SF01 > SF02 > SF04 > SF03 (i.e., SF03 is the coldest — alien void — and SF04 must be warmer than it). Any violation flags immediately, before a critique cycle is needed to catch it.
**Benefits:** Prevents multi-cycle regressions where a single frame's palette degrades silently. Kai or Morgan could implement this as a precritique_qa Section 11, or as a standalone CI gate. Saves critic slots from having to re-flag the same warm/cool arc failure that should be caught in pipeline.
