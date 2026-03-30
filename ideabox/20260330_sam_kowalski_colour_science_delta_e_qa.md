# Idea: Replace Euclidean RGB with ΔE2000 in color_verify

**Submitted by:** Sam Kowalski
**Date:** 2026-03-30
**Category:** Pipeline Improvement

## Problem
`LTG_TOOL_color_verify.py` uses Euclidean RGB distance (radius=40) to match pixels to canonical palette entries. This produces systematic false positives: SUNLIT_AMBER triggers on skin tones (hue 18-25 degrees within radius=40 of target 34.3 degrees), UV_PURPLE fails due to gradient AA edge pixels. These false positives have consumed investigation time across Cycles 26-49.

## Proposal
Install `colour-science` library and replace `_euclidean_distance()` with `colour.delta_E(lab1, lab2, method='CIE 2000')`. ΔE2000 weights perceptual differences correctly — skin tones and lamp amber are perceptually distinct even when Euclidean-close. Threshold: ΔE2000 < 3.0 (imperceptible) for canonical verification, < 5.0 (noticeable at inspection) for general matching.

## Expected Impact
- Eliminates FP-001, FP-003, FP-005 (SUNLIT_AMBER on character sheets)
- Reduces FP-002 (UV_PURPLE gradient AA) severity
- Zero false positives expected in C47 validation set (31 assets)

## Assigned To
Kai Nakamura (QA tool owner). Sam to provide integration code from `wand_colour_science_evaluation_c51.md`.

## Evaluation Details
Full evaluation at: `output/production/wand_colour_science_evaluation_c51.md`
