# Idea: Byte Confetti-as-Emotion QA Metric

**Submitted by:** Priya Shah
**Date:** 2026-03-31
**Cycle:** 52

## Problem
Byte's pixel confetti system is one of his most important narrative tools — confetti density, color temperature, and spread radius change with emotional state (warm/sparse for reluctant joy, hot magenta/dense for anger, zero for defeat). The expression target QA tool cannot evaluate this because it uses silhouette analysis, which ignores small floating particles. There is no automated way to verify that rendered Byte expressions have the correct confetti properties for their emotional state.

## Proposal
Build a dedicated confetti QA metric that:
1. Isolates the area below the body ellipse (where confetti lives)
2. Counts particles (connected components above a noise threshold)
3. Measures spread radius (bounding box of particle cluster)
4. Measures color temperature (average hue of particles — warm vs cool)
5. Compares against story targets for each expression (from character_expression_body_language_targets.md)

Could be added as a `--confetti` mode in `LTG_TOOL_expression_target_qa.py` or as a standalone tool.

## Who benefits
Maya Santos, Rin Yamamoto (character artists), Lee Tanaka (staging), Priya Shah (story-visual verification)

## Effort estimate
Small — the particle extraction is standard connected-component analysis with scikit-image. The target database already exists in the story targets doc. Half a cycle for implementation + testing.
