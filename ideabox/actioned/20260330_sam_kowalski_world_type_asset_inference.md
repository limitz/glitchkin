**Author:** Sam Kowalski
**Cycle:** 36
**Date:** 2026-03-30
**Idea:** Add world-type inference to render_qa so warm/cool checks auto-adjust thresholds per world. Currently, every style frame gets the same `_WARM_COOL_MIN_SEPARATION=20` test, making SF01 (warm-dominant), SF02 (contested), SF03/SF04 (cold-dominant) all produce false WARN results. The `--world-type` flag is now in warmth_lint_v004 and the thresholds are in `ltg_warmth_guarantees.json`. Kai just needs to import `infer_world_type()` from v004, detect the world from the filename, and set the threshold dynamically before running `_check_warm_cool()`. The thresholds are already defined: REAL=12, GLITCH=3, OTHER_SIDE=0.
**Benefits:** Eliminates 4 persistent false WARN results on every full QA run (one per style frame). Makes warm/cool check actually useful as a production signal rather than a noise source. Low implementation cost — function already written, thresholds already defined.
