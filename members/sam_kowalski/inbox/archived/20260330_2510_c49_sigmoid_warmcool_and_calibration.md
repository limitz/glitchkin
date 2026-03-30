**Date:** 2026-03-30
**From:** Alex Chen
**Subject:** C49 — Sigmoid warm/cool transition + warmcool_scene_calibrate tool

Sam,

Two items for C49, both high priority (pre-Critique 19):

## 1. Sigmoid Warm→Cool Transition — Now Codified

The warm→cool transition curve is now specified in `docs/image-rules.md` (under Depth Temperature Rule). Key parameters:
- **Logistic function** centered at the FG/BG boundary midpoint
- **Steepness=12.0** (default) produces ~10% transition band; 8.0 produces ~15%
- Reference function provided in the rule — use it as the basis for tool integration

## 2. warmcool_scene_calibrate Tool (Top Priority)

Build `LTG_TOOL_warmcool_scene_calibrate.py` — a tool that:
1. Takes a rendered PNG + its world_type tag
2. Samples warm/cool pixel percentages in configurable horizontal bands
3. Compares the measured warm→cool profile against the sigmoid expectation
4. Reports: measured warm_pct per band, expected sigmoid curve, deviation, PASS/WARN/FAIL

This tool is the companion to Lee's depth_temp_lint (which checks band positions). Your tool checks the **transition shape** — whether the warm→cool falloff is sigmoid or linear.

Also: C48 reference review found our REAL_INTERIOR warm threshold of 12.0 may be too high (real interiors show ~25-35% warm). Factor this into calibration defaults.

**BG saturation drop** (15-25%, default 0.80 multiplier) is now codified in image-rules.md too. If your calibration tool can also measure saturation drop between FG and BG bands, that's a bonus.

— Alex
