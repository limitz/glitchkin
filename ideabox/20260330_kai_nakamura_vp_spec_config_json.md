**Author:** Kai Nakamura
**Cycle:** 42
**Date:** 2026-03-30
**Idea:** Add a `vp_spec_config.json` file to `output/tools/` that maps each environment generator name to its canonical VP_X, VP_Y, and tolerance values. This would let `LTG_TOOL_sobel_vp_detect.py` (and vanishing_point_lint) look up expected VP positions automatically without requiring `--vp-x-expected` / `--vp-y-expected` flags on every invocation. The JSON would be maintained in parallel with generator specs (classroom: 192,230; kitchen: 960,540; hallway: 640,160; etc.) and could be updated whenever a background spec changes. Could also feed into the CI suite as a new VP003 check — environment VP within spec.
**Benefits:** Removes the need to remember per-file VP values when running batch QA. Enables fully automated VP compliance checking across all ENV backgrounds in the CI suite. Jordan Reed and Hana Okonkwo would benefit most (background generators), and the CI team (Morgan Walsh) could integrate it as a pipeline gate.
