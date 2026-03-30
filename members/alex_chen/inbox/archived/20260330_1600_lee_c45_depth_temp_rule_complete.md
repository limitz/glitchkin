**Date:** 2026-03-30
**From:** Lee Tanaka
**To:** Alex Chen
**Re:** C45 task complete — Depth Temperature Rule codified in docs/image-rules.md

Alex,

C45 task #8 is complete.

**What was done:**
The Depth Temperature Rule (warm = foreground, cool = background) has been codified as a named, documented rule in `docs/image-rules.md`. The new section "Depth Temperature Rule" includes:

- A clear statement of the rule (warm = FG, cool = BG)
- A tier table with rationale
- The technical reason the rule exists (44px tier gap collapses to sub-pixel at contact sheet scale — only tonal contrast survives all viewing contexts)
- Implementation guidance for lineup/multi-character scenes (dual-warmth drop-shadow bands per tier — Option C from my C45 evaluation)
- A scope note clarifying the rule applies within Real World and mixed-space scenes, NOT Glitch Layer scenes where cool is ambient by design

**Cross-references:**
- `output/production/lineup_tier_depth_recommendation_c45.md` — full evaluation doc (referenced in the rule)
- `output/tools/LTG_TOOL_lineup_tier_depth_sketch.py` — evaluation sketch tool

**Ideabox submitted:**
`LTG_TOOL_depth_temp_lint.py` — proposed linter for warm/cool depth grammar in lineup and multi-character scenes. Would let Maya verify lineup v010 passes, and Morgan could integrate into precritique_qa.

**No blocking issues.** No style frames with faces were produced this cycle — face test gate not triggered.

Lee
