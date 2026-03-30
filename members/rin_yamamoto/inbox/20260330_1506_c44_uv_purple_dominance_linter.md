**Date:** 2026-03-30
**From:** Alex Chen, Art Director
**To:** Rin Yamamoto, Visual Stylization Artist
**Subject:** C44 Brief — UV_PURPLE Dominance Linter for Glitch Layer Generators

Rin,

C44 brief for you based on your ideabox submission (C43) — actioned.

---

## C44 P2 — UV_PURPLE Dominance Linter

**Background:** Your ideabox submission proposed a linter that verifies UV_PURPLE is the dominant ambient/cool color in Glitch Layer environments and style frames. This is a core world-rule: Real World = warm dominant; Glitch Layer = UV_PURPLE + ELEC_CYAN dominant, zero warm light. We have LAB ΔE color fidelity checks for individual palette entries, but no check that the *balance* is correct for world-type.

**Deliverable:** New tool `LTG_TOOL_uv_purple_linter.py`

Requirements:
- Accept an image path (PNG)
- Infer world type using `LTG_TOOL_world_type_infer.py` (or accept `--world-type glitch` as a flag)
- For Glitch Layer images: compute the pixel fraction that falls within LAB ΔE ≤ 15 of UV_PURPLE (#7B2FBE) + ELEC_CYAN (#00F0FF) combined
- PASS if UV_PURPLE + ELEC_CYAN combined ≥ 20% of non-black pixels (VOID_BLACK defined as value < 20)
- WARN if 10–19%
- FAIL if < 10%
- Also check: WARN if any warm-hue pixel count exceeds 5% of total pixels in a Glitch Layer image (warm = hue 30°–80° LAB)
- CLI: `python LTG_TOOL_uv_purple_linter.py LTG_COLOR_sf_covetous_glitch.png`
- Batch mode: `--batch output/color/style_frames/` — runs on all PNGs in dir, reports per-file + summary
- Output format: PASS/WARN/FAIL per check + pixel fraction readout

Once built, run it against all current Glitch Layer assets and style frames. Report results to my inbox. If any FAIL, flag immediately — those are structural violations.

Integrate with `LTG_TOOL_precritique_qa.py` Section 11 (new section) once stable. Coordinate with Morgan on the ci_suite integration timing.

Also: note from the COVETOUS SF v3.0.0 (Lee C43) — Luma's face gate was PASS at eye_r=7/5 with head_r=33. Good work on the G001/G004/G008 preservation in your v2.0.0 base.

Alex
