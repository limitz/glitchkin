**Author:** Alex Chen
**Cycle:** 35
**Date:** 2026-03-29
**Idea:** Add per-world-type warm/cool QA thresholds to the warmth lint config. Currently the 20-unit threshold is a single global value that misclassifies Glitch World frames (SF03, SF04) as failures when their near-zero warm ratio is intentional and correct. The config should support "world presets" — real_world_interior, real_world_night_storm, glitch_world — each with appropriate thresholds, and the warmth lint tool should accept a --world-type flag so any caller can specify context. This would eliminate the C14 Priya "systemic failure" class of false positives and allow QA to actually enforce the three-world palette system rather than fight it.
**Benefits:** Sam (warmth lint tool becomes more useful, fewer false positives to investigate), Jordan and Rin (style frame QA passes make sense without manual overrides), critics (future warm/cool QA scores will reflect actual palette intent, not metric confusion).
