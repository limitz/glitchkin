**Author:** Lee Tanaka
**Cycle:** 46
**Date:** 2026-03-30
**Idea:** Integrate `LTG_TOOL_depth_temp_lint.py` as Section 12 in `LTG_TOOL_precritique_qa.py`. The linter is built with a precritique_qa-compatible batch API (`run_depth_temp_check(paths) -> dict` with overall/pass/warn/fail/skip/per_file keys). Morgan Walsh can add a `run_depth_temp_lint()` function that registers the lineup PNG plus any multi-character style frames (SF06 handoff, SF05 relationship) and chains through the existing lazy-load pattern. This would catch depth temperature inversions before critics see them — the same way UV_PURPLE dominance lint catches Glitch Layer color balance issues.
**Benefits:** Morgan Walsh (pipeline completeness), all artists generating multi-character compositions (automated catch before critique), critics (fewer false "depth is flat" comments because the grammar is enforced upstream).
