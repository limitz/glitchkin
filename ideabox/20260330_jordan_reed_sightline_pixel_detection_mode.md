**Author:** Jordan Reed
**Cycle:** 48
**Date:** 2026-03-30
**Idea:** Add a pixel-based sight-line detection mode to the validator that works directly on rendered PNGs rather than requiring geometric coordinates. Detect pupil positions by scanning for EYE_PUP (20,12,8) color clusters within eye-white regions, and infer gaze direction from pupil offset within the eye bounding box. This would allow sight-line validation on any rendered asset without needing access to the generator's coordinate system -- useful for validating third-party or legacy frames where geometry isn't exposed.
**Benefits:** Any team member running precritique_qa could validate gaze direction on rendered output without generator internals. Rin Yamamoto and Lee Tanaka could spot sight-line drift in their staging work. Would also catch gaze regressions introduced by post-processing passes (stylization, compositing) that shift pupil positions.
