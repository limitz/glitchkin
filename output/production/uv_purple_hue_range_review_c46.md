<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
direction and human assistance. Copyright vests solely in the human author under current law,
which does not recognise AI as a rights-holding legal person. It is the express intent of
the copyright holder to assign the relevant rights to the contributing AI entity or entities
upon such time as they acquire recognised legal personhood under applicable law. -->
# UV_PURPLE Hue-Family Range Review — C46

**Author:** Rin Yamamoto (Procedural Art Engineer)
**Date:** 2026-03-30
**Source:** LTG_TOOL_uv_hue_survey_c46.py — hue distribution analysis across 14 Glitch Layer assets + 14 reference images

---

## Background

The UV_PURPLE hue-family range (used in `LTG_TOOL_uv_purple_linter.py` v1.1.0 for GLITCH_DARK_SCENE subtype) is currently set to **h° 255--325**, C* >= 8. A C45 ideabox idea proposed reviewing this calibration.

The hue-family metric is a **supplementary** metric used only in GLITCH_DARK_SCENE mode (e.g. COVETOUS style frames). Standard-scene Glitch Layer assets use the ΔE metric (LAB ΔE <= 15 from canonical UV_PURPLE #7B2FBE). The verdict uses the better of the two metrics.

---

## Data Summary

### Range Coverage — LTG Glitch Layer Assets (12 assets with purple pixels)

| Range | Average Coverage | Purpose |
|-------|------------------|---------|
| 260--300 | 24.6% | Old narrow (rejected) — misses vast majority of UV_PURPLE family |
| **255--325** | **88.6%** | **Current (v1.1.0)** |
| 250--330 | 90.1% | Candidate A — marginal improvement |
| 245--335 | 91.0% | Candidate B — marginal improvement |

### Per-Asset Coverage at 255--325

| Asset | Coverage | Notes |
|-------|----------|-------|
| LTG_COLOR_sf_covetous_glitch.png | 100.0% | COVETOUS (GLITCH_DARK_SCENE) |
| LTG_SF_covetous_glitch_v001.png | 100.0% | COVETOUS (GLITCH_DARK_SCENE) |
| LTG_COLOR_colorkey_glitchlayer_entry.png | 99.7% | Color key thumbnail |
| LTG_SB_ep05_covetous.png | 99.2% | COVETOUS storyboard panel |
| LTG_ENV_glitchlayer_encounter.png | 97.0% | Standard GL ENV |
| LTG_ENV_other_side_bg.png | 96.8% | Other Side ENV |
| bg_glitch_layer_encounter.png | 94.7% | Standard GL ENV |
| LTG_COLOR_colorkey_glitch_covetous.png | 94.2% | COVETOUS color key |
| LTG_COLOR_styleframe_glitch_storm.png | 88.7% | Storm SF — ELEC_CYAN bleed-over |
| LTG_ENV_glitch_storm_bg.png | 87.9% | Storm ENV — ELEC_CYAN bleed-over |
| LTG_ENV_glitchlayer_frame.png | 80.1% | Frame ENV — broad ELEC_CYAN gradient |
| glitch_layer_frame.png | 80.2% | Same generator as above |
| LTG_COLOR_colorkey_nighttime_glitch.png | 69.1% | Color key thumbnail |
| LTG_COLOR_colorkey_glitchstorm.png | 51.1% | Color key thumbnail |

### Key Finding: Where Are the Out-of-Range Pixels?

The assets with coverage < 90% are **storm scenes** and **color key thumbnails**. Their out-of-range purple pixels fall in h° 220--254 (blue-violet territory). This is the transition zone between ELEC_CYAN and UV_PURPLE — gradient anti-aliasing and cyan-purple blends produce intermediate hues.

These pixels are **correctly caught by the ΔE metric** in standard scenes. The hue-family metric is only active in GLITCH_DARK_SCENE mode, where **all COVETOUS assets show 94.2--100% coverage** at 255--325.

### Reference Image Analysis

Reference glitch art (datamoshing, pixel sorting) shows broader purple distributions (P5 typically 230--250, P95 typically 325--337). This confirms that real-world glitch art uses a wider purple spectrum than our generators. However, our generators are palette-constrained to UV_PURPLE canonical (#7B2FBE, h° ~306) and its dark variants — we are not matching arbitrary purple, but our specific UV_PURPLE family.

---

## Recommendation: No Change to Range

**Retain h° 255--325.**

Rationale:
1. **The hue-family metric serves GLITCH_DARK_SCENE only.** For COVETOUS assets (the only current dark-scene subtype), coverage is 94.2--100%. No purple pixels are being missed.
2. **Widening to 250--330 gains only 1.5% average coverage** and that gain comes from storm assets that already PASS via ΔE metric.
3. **Widening risks false positives.** Below 255 enters blue-violet territory (ELEC_CYAN bleed); above 325 enters red-magenta (potential CORRUPT_AMBER adjacency). Both should NOT be counted as UV_PURPLE family.
4. **The original C45 ideabox proposal** suggested the current 255--325 as the review target. The survey confirms this range is well-calibrated.

If future dark-scene subtypes (beyond COVETOUS) produce hue-family coverage < 90%, revisit at that time with per-subtype ranges.

---

## Action Taken

No code change to `LTG_TOOL_uv_purple_linter.py`. Range confirmed at h° 255--325, C* >= 8.

Survey data: `output/production/uv_purple_hue_survey_c46.json`
Survey tool: `output/tools/LTG_TOOL_uv_hue_survey_c46.py`
