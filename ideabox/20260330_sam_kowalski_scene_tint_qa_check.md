**Author:** Sam Kowalski
**Cycle:** 50
**Date:** 2026-03-30
**Idea:** Add a "scene tint presence" check to precritique_qa. After C50, characters should receive scene lighting via apply_scene_tint(). A simple QA check: sample pixels inside the character bounding box and compare their hue histogram to the scene's key light hue. If no pixels within the character bbox are shifted toward the scene key light (Euclidean distance in LAB < 2.0 from canonical palette values with zero scene influence), the character is NOT receiving scene light and the check should WARN. This catches the old failure mode (character painted in isolation, pasted onto lit background) automatically.
**Benefits:** Jordan, Rin, and any future character artists get immediate QA feedback when they forget to apply scene tinting. Prevents regression to the flat-character look without requiring visual review.
