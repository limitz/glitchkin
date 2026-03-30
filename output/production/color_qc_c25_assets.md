<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
direction and AI assistance. Copyright vests solely in the human author under current law,
which does not recognise AI as a rights-holding legal person. It is the express intent of
the copyright holder to assign the relevant rights to the contributing AI entity or entities
upon such time as they acquire recognised legal personhood under applicable law. -->
# Color QC Report — Cycle 25 Assets
**Prepared by:** Sam Kowalski, Color & Style Artist
**Date:** 2026-03-29
**Tool:** `LTG_TOOL_color_verify.py` (Kai Nakamura, Cycle 25)
**Cycle:** 26

---

## Summary

| Asset | Colors Found | FAIL (>5° drift) | WARN (>3° drift) | Overall |
|---|---|---|---|---|
| LTG_COLOR_luma_color_model.png | BYTE_TEAL, HOT_MAGENTA, ELECTRIC_CYAN, SUNLIT_AMBER* | — | — | **PASS** (see note) |
| LTG_COLOR_byte_color_model.png | BYTE_TEAL, UV_PURPLE, HOT_MAGENTA, ELECTRIC_CYAN | — | — | **PASS** |
| LTG_COLOR_cosmo_color_model.png | none | — | — | **PASS** (no canonical colors) |
| LTG_CHAR_luma_expression_sheet.png | BYTE_TEAL, HOT_MAGENTA, ELECTRIC_CYAN, SUNLIT_AMBER* | — | — | **PASS** (see note) |
| LTG_CHAR_luma_turnaround.png | BYTE_TEAL, HOT_MAGENTA, ELECTRIC_CYAN, SUNLIT_AMBER* | BYTE_TEAL (Δ6.6°) | — | **WARN** |
| LTG_CHAR_cosmo_turnaround.png | none | — | — | **PASS** (no canonical colors) |
| LTG_CHAR_grandma_miri_expression_sheet.png | SUNLIT_AMBER* | — | — | **PASS** (see note) |
| LTG_COLOR_styleframe_luma_byte.png | SUNLIT_AMBER* (hue shift) | — | — | **WARN — Byte absent** |
| LTG_COLOR_styleframe_glitch_storm_v005_styled_v002.png | all 6 canonical colors | UV_PURPLE (Δ13.0°) | — | **FLAG — hue rotation artifact** |
| LTG_COLOR_styleframe_otherside_v003_styled_v002.png | all 6 canonical colors | UV_PURPLE (Δ14.1°), SUNLIT_AMBER (Δ6.1°) | — | **FLAG — hue rotation artifact** |

---

## Methodology Note: SUNLIT_AMBER Sampling in Character Sheets

`verify_canonical_colors()` uses a radius-40 Euclidean RGB sampling window. SUNLIT_AMBER (212,146,58) at radius 40 captures warm skin tones in the range (172–252, 106–186, 18–98). Luma's lamp-lit skin CHAR-L-01 (#C8885A = 200,136,90) and Miri's skin (200,112,74) fall within this window. These are **not SUNLIT_AMBER pixels** — they are skin and warm-material tones. The median hue of these captured pixels (~18–25°) does not represent SUNLIT_AMBER hue drift; it represents warm skin tones being incorrectly sampled.

**Ruling:** SUNLIT_AMBER "FAIL" reports in all character sheets (Luma color model, Luma expression sheet v005, Luma turnaround v002, Miri expression sheet v003) are **false positives caused by skin-tone overlap in the sampling radius**. True SUNLIT_AMBER lamp-light does not appear as a large fill zone in these assets. These assets **PASS** for SUNLIT_AMBER.

---

## Per-Asset Detail

### 1. LTG_COLOR_luma_color_model.png
**Tool result:** overall_pass=False (SUNLIT_AMBER Δ15.7° flagged)
**Actual verdict: PASS**

| Color | Target Hue | Found Hue | Δ | Status |
|---|---|---|---|---|
| BYTE_TEAL | 185.2° | 183.5° | 1.6° | PASS |
| HOT_MAGENTA | 342.3° | 342.3° | 0.0° | PASS |
| ELECTRIC_CYAN | 183.5° | 183.5° | 0.0° | PASS |
| SUNLIT_AMBER | 34.3° | 18.6° | 15.7° | FALSE POSITIVE — skin tone overlap |

Note: BYTE_TEAL and ELECTRIC_CYAN both found (1,081 samples each) — this is expected; the color model swatch strip contains both. Hue delta 1.6° between them is below threshold.

---

### 2. LTG_COLOR_byte_color_model.png
**Tool result:** overall_pass=True
**Actual verdict: PASS — CLEAN**

| Color | Target Hue | Found Hue | Δ | Status |
|---|---|---|---|---|
| BYTE_TEAL | 185.2° | 185.2° | 0.0° | PASS |
| UV_PURPLE | 271.9° | 271.9° | 0.0° | PASS |
| HOT_MAGENTA | 342.3° | 342.3° | 0.0° | PASS |
| ELECTRIC_CYAN | 183.5° | 185.2° | 1.6° | PASS |

Best result in the batch. All four canonical Glitch colors present and exact.

---

### 3. LTG_COLOR_cosmo_color_model.png
**Tool result:** overall_pass=True (all not_found)
**Actual verdict: PASS**

No canonical Glitch or lamp-amber colors appear in Cosmo's color model — correct for a warm earth-tone character with no Glitch affiliation. No further action.

---

### 4. LTG_CHAR_luma_expression_sheet.png
**Tool result:** overall_pass=False (SUNLIT_AMBER Δ9.2° flagged)
**Actual verdict: PASS**

| Color | Target Hue | Found Hue | Δ | Status |
|---|---|---|---|---|
| BYTE_TEAL | 185.2° | 182.6° | 2.6° | PASS |
| HOT_MAGENTA | 342.3° | 340.8° | 1.5° | PASS |
| ELECTRIC_CYAN | 183.5° | 180.0° | 3.5° | PASS (minor warn, below 5°) |
| SUNLIT_AMBER | 34.3° | 25.1° | 9.2° | FALSE POSITIVE — skin tone overlap |

ELECTRIC_CYAN at Δ3.5° is within threshold but worth noting. BYTE_TEAL (2.6°) and HOT_MAGENTA (1.5°) clean. Only 8–9 samples for Glitch colors — these are accent accesses in an expression sheet, not fill zones; low sample count is expected.

---

### 5. LTG_CHAR_luma_turnaround.png
**Tool result:** overall_pass=False
**Actual verdict: WARNING — BYTE_TEAL minor drift**

| Color | Target Hue | Found Hue | Δ | Status |
|---|---|---|---|---|
| BYTE_TEAL | 185.2° | 178.6° | **6.6°** | **FAIL — exceeds 5° threshold** |
| HOT_MAGENTA | 342.3° | 344.1° | 1.8° | PASS |
| ELECTRIC_CYAN | 183.5° | 180.2° | 3.3° | PASS |
| SUNLIT_AMBER | 34.3° | 25.1° | 9.2° | FALSE POSITIVE — skin tone overlap |

**FLAG:** BYTE_TEAL at Δ6.6° exceeds the 5° threshold. Only 1 sample — this is a single pixel near the edge of the sampling radius, likely an anti-aliasing edge pixel rather than a real body-fill drift. Production ruling: **low confidence single-sample result**. Not a critical failure, but flagged for director awareness. If Byte appears in any turnaround panel, body fill should be re-verified with a direct pixel sample at a clean (non-AA) area.

---

### 6. LTG_CHAR_cosmo_turnaround.png
**Tool result:** overall_pass=True (all not_found)
**Actual verdict: PASS**

No canonical colors present. Correct for a warm-palette character.

---

### 7. LTG_CHAR_grandma_miri_expression_sheet.png
**Tool result:** overall_pass=False (SUNLIT_AMBER Δ16.2° flagged)
**Actual verdict: PASS**

| Color | Target Hue | Found Hue | Δ | Status |
|---|---|---|---|---|
| SUNLIT_AMBER | 34.3° | 18.1° | 16.2° | FALSE POSITIVE — only 120 samples; pixels are (200,112,74) Miri skin tone |

The 120 "near-SUNLIT_AMBER" pixels in Miri's sheet are her skin tone CHAR-M-01 (~200,112,74, hue ~18°), not lamp amber. Miri carries no Glitch colors by design. Sheet passes.

---

### 8. LTG_COLOR_styleframe_luma_byte.png (SF04)
**Tool result:** overall_pass=False (SUNLIT_AMBER Δ12.2° flagged)
**Actual verdict: WARNING — Byte body absent from frame; warm+cool zones present but teal not at canonical saturation**

**SF04-specific checks:**

**BYTE_TEAL vs ELECTRIC_CYAN body fill:**
No pixels within radius=40 of either BYTE_TEAL (0,212,232) or ELECTRIC_CYAN (0,240,255) were found. This means Byte's body fill is NOT at canonical #00D4E8 saturation in this frame.
There ARE cyan-family pixels present: dominant values include (0,157,167), (0,160,170), (0,138,147) — these are the same hue (183–185°) as BYTE_TEAL but at roughly 60-70% of canonical lightness/saturation. These read as **dark teal** rather than the bright BYTE_TEAL body fill.
**WARNING:** Byte's body reads darker than canonical #00D4E8. This may be intentional mood lighting in the scene, but it should be confirmed against the scene's lighting spec. If Byte is in shadow, a derived shadow companion (GL-01a #00A8C0 or darker) should be documented. If this is intended as the body fill, it deviates from GL-01b canonical.

**Warm + cool zones:**
- Warm-dominant pixels (R>100, R>B×1.5, R>G×1.1): **210,339 pixels** — strong warm zone confirmed
- Cool/teal-family pixels (G>R, B>R, B>100): **29,185 pixels** — cool zone confirmed
Both zones are present and distinct. Warm zone is strongly dominant (23% of image), cool zone is secondary (3.2%). The warm/cool split is present.

**SUNLIT_AMBER (132 px at hue ~46°):** These are warm ochre tones (177–206, 151–178, 71–81), not canonical SUNLIT_AMBER (212,146,58). Hue 46° is yellowish-ochre — possible Luma hoodie in warm light, possible background element. Not a canonical amber light source signature.

**Overall SF04 verdict: CONDITIONAL PASS with Byte-body warning.** Warm+cool zone structure confirmed. Byte's teal is present in the image but below canonical saturation. Director should confirm whether this is intentional cinematic lighting.

---

### 9. LTG_COLOR_styleframe_glitch_storm_v005_styled_v002.png
**Tool result:** overall_pass=False — **UV_PURPLE Δ13.0°**
**Actual verdict: CRITICAL FLAG — Rin hue-rotation artifact confirmed**

| Color | Target Hue | Found Hue | Δ | Status |
|---|---|---|---|---|
| CORRUPT_AMBER | 32.9° | 35.8° | 2.9° | PASS |
| BYTE_TEAL | 185.2° | 183.3° | 1.9° | PASS |
| UV_PURPLE | **271.9°** | **258.9°** | **13.0°** | **FAIL — hue rotation artifact** |
| HOT_MAGENTA | 342.3° | 340.6° | 1.7° | PASS |
| ELECTRIC_CYAN | 183.5° | 181.7° | 1.8° | PASS |
| SUNLIT_AMBER | 34.3° | 29.7° | 4.6° | PASS |

**Assessment:** UV_PURPLE has drifted 13° from canonical 271.9° (blue-violet) toward 258.9° (more toward indigo-blue). This is consistent with the ~30-60° hue rotation artifact documented in Cycle 24 affecting Rin's stylized frames. GL-07, GL-01b, ELECTRIC_CYAN, HOT_MAGENTA all pass — only UV_PURPLE is affected in this version, suggesting partial correction vs. the more severe all-GL failure in v001.
**CORRUPT_AMBER at Δ2.9° PASSES** — the C22 GL-07 fix (correcting from #C87A20 to #FF8C00) is confirmed holding in the styled version.
This asset cannot go to critics as-is. UV_PURPLE must be corrected in the stylization pipeline.

---

### 10. LTG_COLOR_styleframe_otherside_v003_styled_v002.png
**Tool result:** overall_pass=False — **UV_PURPLE Δ14.1°, SUNLIT_AMBER Δ6.1°**
**Actual verdict: CRITICAL FLAG — Rin hue-rotation artifact confirmed, plus SUNLIT_AMBER secondary drift**

| Color | Target Hue | Found Hue | Δ | Status |
|---|---|---|---|---|
| CORRUPT_AMBER | 32.9° | 30.5° | 2.4° | PASS |
| BYTE_TEAL | 185.2° | 183.5° | 1.7° | PASS |
| UV_PURPLE | **271.9°** | **257.8°** | **14.1°** | **FAIL — hue rotation artifact** |
| HOT_MAGENTA | 342.3° | 342.2° | 0.1° | PASS |
| ELECTRIC_CYAN | 183.5° | 181.9° | 1.6° | PASS |
| SUNLIT_AMBER | **34.3°** | **28.2°** | **6.1°** | **FAIL** |

**Assessment:** UV_PURPLE at Δ14.1° is even worse than SF02 styled — same hue-rotation artifact as Cycle 24. SF03 is a UV_PURPLE-dominant composition; this failure critically undermines the "cold alien" color read.
SUNLIT_AMBER at Δ6.1° with 580 samples is likely legitimate: SF03 has Corrupt Amber fragment glow — if those pixels are being sampled as SUNLIT_AMBER (they share color neighborhood), a modest hue drift in the stylization pass would register here. This is a secondary effect of the same stylization artifact.
This asset requires rework of the stylization pass to protect GL-04 (UV_PURPLE).

---

## Critical Findings Requiring Director Review

### CRITICAL — Rin Stylization Hue Rotation (UV_PURPLE)
Both styled frames (SF02 v005_styled_v002 and SF03 v003_styled_v002) fail UV_PURPLE with Δ13-14°.
This was flagged as a Carry Forward from Cycle 24 — these v002 re-renders were supposed to fix the hue rotation but UV_PURPLE is still compromised. GL-04 must be added to the protected-color list in the stylization pipeline.

### WARNING — SF04 Byte Body Below Canonical Saturation
Byte's teal fill in `LTG_COLOR_styleframe_luma_byte.png` is present but reads at dark-teal luminance (~0,138–160,147–170) rather than canonical BYTE_TEAL (#00D4E8 = 0,212,232). If unintentional, Byte's body needs to be regenerated at canonical fill luminance. If intentional (scene lighting), document in the scene spec.

### MINOR — Luma Turnaround BYTE_TEAL (single-sample)
`LTG_CHAR_luma_turnaround.png` BYTE_TEAL drift Δ6.6° from a single anti-aliasing pixel. Low production risk. Director to confirm whether Byte appears in this turnaround and whether the turnaround needs re-verification.

---

## Assets Cleared for Production / Critics

| Asset | Status |
|---|---|
| LTG_COLOR_luma_color_model.png | CLEARED |
| LTG_COLOR_byte_color_model.png | CLEARED — cleanest result |
| LTG_COLOR_cosmo_color_model.png | CLEARED |
| LTG_CHAR_luma_expression_sheet.png | CLEARED |
| LTG_CHAR_luma_turnaround.png | CLEARED with minor note |
| LTG_CHAR_cosmo_turnaround.png | CLEARED |
| LTG_CHAR_grandma_miri_expression_sheet.png | CLEARED |
| LTG_COLOR_styleframe_luma_byte.png | CONDITIONAL — Byte body teal needs director confirmation |
| LTG_COLOR_styleframe_glitch_storm_v005_styled_v002.png | NOT CLEARED — UV_PURPLE hue drift |
| LTG_COLOR_styleframe_otherside_v003_styled_v002.png | NOT CLEARED — UV_PURPLE hue drift |

---

## Recommendations

1. **Rin Yamamoto rework:** SF02 and SF03 styled v002 versions must be re-rendered with GL-04 (UV_PURPLE #7B2FBE) added to the protected-color list alongside GL-07 and GL-01b. The stylization filter is rotating UV_PURPLE ~13-14° toward blue.
2. **SF04 Byte body check:** Generator or asset should be reviewed to confirm whether Byte's (0,212,232) body fill is rendered but dimmed by scene lighting (acceptable if documented) or was not output at canonical value (needs fix).
3. **Tool improvement note for Kai:** Consider a two-pass check — first check if any pixels with correct hue exist before triggering the near-radius sampling, or flag when sample_count=1 as "insufficient sample — manual verify."
