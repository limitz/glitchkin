**Author:** Hana Okonkwo
**Cycle:** 40
**Date:** 2026-03-30
**Idea:** Build a warm/cool debug helper script (`LTG_TOOL_warmsplit_predict.py`) that, given an image, outputs the median hue of TOP and BOTTOM halves in both degrees and PIL units, reports current separation, and previews what alpha value on a warm-top or cool-bottom overlay would be needed to reach a target separation (default 12). This is a constant friction point in environment work — every room needs QA warm/cool iteration and right now it requires running warmth_inject (which has its own alpha stepping) or manually inspecting the image. A predict-mode tool would tell me upfront how many overlay units I need. Would save 3-5 QA iterations per environment.
**Benefits:** Hana Okonkwo (direct use), any future environment/bg artists. Would also help character artists who need warm/cool checks on composite style frames. Cuts iteration time for every environment that isn't naturally high-contrast.
