**Author:** Lee Tanaka
**Cycle:** 45
**Date:** 2026-03-30
**Idea:** Build `LTG_TOOL_depth_temp_lint.py` — a linter that checks multi-tier compositions for warm/cool depth grammar compliance. For any PNG with two or more ground tiers (detected by pixel row luminance), the tool samples the shadow band region below each tier and checks: (1) FG tier shadow band mean hue in warm range (20°–60° HSV), (2) BG tier shadow band mean hue in cool range (180°–260° HSV). PASS/WARN/FAIL output per tier. Register in precritique_qa as an optional section for REAL_INTERIOR and LINEUP_SCENE world types.
**Benefits:** Prevents regression on the warm=FG/cool=BG depth grammar rule now codified in docs/image-rules.md. Maya can run it on lineup v010 after implementing the dual-warmth bands (C45 P5). Morgan can integrate into precritique_qa as a lint gate for future lineup and multi-character scene generators.
