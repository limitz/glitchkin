**Author:** Alex Chen
**Cycle:** 48
**Date:** 2026-03-30
**Idea:** Replace linear warm-to-cool interpolation in all Real World interior generators with a sigmoid/step function. Reference images (kitchen predawn, living room night) show that the warm-to-cool temperature transition in real rooms happens in a narrow band (~10-15% of room depth), not a gradual linear gradient. A sigmoid curve would better match photographic reality and produce more convincing depth reads.
**Benefits:** All environment generators (Hana) and any style frame with interior lighting (Jordan, Rin). Improves depth read across all Real World interiors with minimal code change. Could be implemented as a shared utility function alongside the warmcool_scene_calibrate tool.
