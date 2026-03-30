# LTG COLOR Stylization Fidelity Report — Cycle 24

**Author:** Sam Kowalski, Color & Style Artist
**Date:** 2026-03-29
**Tool:** LTG_TOOL_fidelity_check_c24.py
**Critique Cycle:** 11

---

## Summary

Pixel-level color fidelity check on all `_styled.png` outputs produced by
Rin Yamamoto in Cycle 24. Each asset was sampled at matching pixel coordinates
in the original vs. styled versions for the following canonical palette targets:

| Code | Color | Hex | RGB |
|------|-------|-----|-----|
| GL-07 | CORRUPT_AMBER | #FF8C00 | (255, 140, 0) |
| GL-01b | BYTE_TEAL | #00D4E8 | (0, 212, 232) |
| GL-05 | UV_PURPLE | #7B2FBE | (123, 47, 190) |
| RW-02 | SUNLIT_AMBER / SOFT_GOLD | #E8C95A | (232, 201, 90) |

**Tolerance:** ±20 per channel max delta from canonical value.
**Scan step:** 20px grid on full canvas; up to 5 matches per color per asset.

---

## Asset Results

---

### Asset 1: SF02 — Glitch Storm
**Files:** `LTG_COLOR_styleframe_glitch_storm.png` vs `_v005_styled.png`
**Size:** 1920×1080px (MATCH)

#### GL-07 CORRUPT_AMBER — FLAG

| Coord | Orig | Styled | Δcanonical | Δorig | Status |
|-------|------|--------|------------|-------|--------|
| (522, 486) | #FF9100 | #00BE00 | 255 | 255 | FLAG |
| (549, 486) | #FF8700 | #FF9400 | 8 | 13 | PASS |
| (486, 513) | #FF9800 | #39D101 | 198 | 198 | FLAG |
| (486, 522) | #FF9300 | #FFD808 | 76 | 69 | FLAG |
| (486, 531) | #FF9400 | #ABCB27 | 84 | 84 | FLAG |

**Analysis:** 1 of 5 samples PASS. Failing samples show severe hue rotation — amber (255,140,0) shifting to green (#00BE00), acid yellow (#FFD808), and olive (#ABCB27). The coord (549,486) PASS suggests the Byte amber-outline region may be partially intact but surrounding pixels have been aggressively re-toned. GL-07 desaturation or hue rotation is a critical violation — CORRUPT_AMBER must not be desaturated or hue-shifted in a mixed-world or Real World scene.

#### GL-01b BYTE_TEAL — CONDITIONAL FLAG

| Coord | Orig | Styled | Δcanonical | Δorig | Status |
|-------|------|--------|------------|-------|--------|
| (1485, 63) | #00F0FF | #00F0FF | 28 | 0 | FLAG (scan note) |
| (1359, 90) | #00F0FF | #00F0ED | 28 | 18 | FLAG (scan note) |
| (1170, 126) | #00F0FF | #0AFFED | 43 | 18 | FLAG |
| (1458, 144) | #01D9E8 | #13FF00 | 232 | 232 | FLAG |
| (1449, 153) | #00F0FF | #00FF4F | 153 | 176 | FLAG |

**Analysis:** The scan found GL-01 Electric Cyan (#00F0FF) sky pixels, not GL-01b Byte Teal (#00D4E8) body pixels specifically. Coords (1485,63) and (1359,90): Δorig=0–18 — styled faithfully reproduces the original at those sky pixels; the Δcanonical=28 reflects the normal GL-01 vs GL-01b distinction in the source. These two are sky-fidelity PASS. Coords (1458,144) and (1449,153): catastrophic cyan→green shift (+230 delta) consistent with the same hue rotation flagged in GL-07. GL-01b body fill cannot be confirmed at these coords; a targeted body-pixel sample is recommended for Rin's next pass.

#### UV_PURPLE — SKIP
Not present in SF02 original. Expected — UV Purple is the Other Side (SF03) atmosphere color.

#### SUNLIT_AMBER / RW-02 — FLAG

| Coord | Orig | Styled | Δcanonical | Δorig | Status |
|-------|------|--------|------------|-------|--------|
| (882, 495) | #CDB477 | #FFFF00 | 90 | 119 | FLAG |

**Analysis:** The warm window area (approx. window glow zone, lower building facade) has shifted to pure Lemon Yellow (#FFFF00). Delta is extreme at 119 from original. Warm amber window glow in SF02 is a critical narrative element (the contested warm lower third); this shift would read as artificial and tonally wrong for a Real World interior glow.

**SF02 Asset Verdict: FLAG**

---

### Asset 2: SF03 — Other Side
**Files:** `LTG_COLOR_styleframe_otherside.png` vs `_v003_styled.png`
**Size:** 1920×1080px (MATCH)

#### GL-07 CORRUPT_AMBER — FLAG (Critical)

| Coord | Orig | Styled | Δcanonical | Δorig | Status |
|-------|------|--------|------------|-------|--------|
| (918, 459) | #EB7E1C | #B89E03 | 71 | 51 | FLAG |
| (918, 477) | #EB7E1C | #B89E08 | 71 | 51 | FLAG |
| (918, 495) | #EB7E1D | #B79E07 | 72 | 52 | FLAG |
| (1152, 522) | #EA7D1E | #00B351 | 255 | 234 | FLAG |

**Analysis:** The original correctly renders Luma's hoodie at ~#EB7E1C (UV-ambient-adjusted DRW-14 orange). The styled version shifts this to desaturated olive-chartreuse (#B89E03–#B79E07) at consistent Δorig of 51–52 points across three spatially-clustered samples. This is a confirmed critical fidelity failure. In SF03, Luma's warm orange is the ONLY warm color in the entire frame — it is the entire emotional stakes of the scene. If the hoodie reads as olive or yellow-green rather than orange-warm, the color story collapses. Coord (1152,522) extreme FLAG (#00B351) is likely a scan artifact at an edge/overlap zone, but the hoodie core area failure at coords 918 is confirmed and unambiguous.

#### GL-01b BYTE_TEAL — FLAG

| Coord | Orig | Styled | Δcanonical | Δorig | Status |
|-------|------|--------|------------|-------|--------|
| (1296, 81) | #00F0FF | #24FF18 | 208 | 231 | FLAG |
| (1278, 225) | #0EDBF8 | #2BFF2F | 185 | 201 | FLAG |
| (828, 270) | #01EFFF | #2CFF08 | 224 | 247 | FLAG |
| (324, 531) | #00F0FF | #0AFF00 | 232 | 255 | FLAG |
| (252, 612) | #00F0FF | #DAFF2E | 218 | 218 | FLAG |

**Analysis:** Cyan (#00F0FF / GL-01 in this scene) → Green (#24FF18 etc.) hue rotation, consistent across all 5 samples. Δorig is uniformly 200+ points — these are not marginal shifts. This is the same hue rotation artifact as SF02, more severe. In SF03, Byte's teal body and the data column cyan are the primary cool palette — shifting them to green completely destroys the "digital cold alien world" reading.

#### UV_PURPLE — FLAG (Critical)

| Coord | Orig | Styled | Δcanonical | Δorig | Status |
|-------|------|--------|------------|-------|--------|
| (1575, 135) | #7B2FBE | #1B4834 | 138 | 138 | FLAG |
| (1674, 135) | #7B2FBE | #1B4533 | 139 | 139 | FLAG |
| (1629, 171) | #7B2FBE | #264714 | 170 | 170 | FLAG |
| (1467, 180) | #7B2FBE | #2442FF | 87 | 87 | FLAG |
| (1197, 216) | #7B2FBE | #224337 | 135 | 135 | FLAG |

**Analysis:** UV Purple (#7B2FBE) is the entire atmospheric key of SF03. The styled version shifts it to dark teal-green (#1B4834, #264714, #224337) and one sample to deep blue (#2442FF). All 5 samples FLAG. This is the most severe failure in the batch. The Other Side sky must read purple — that is what marks it as inhuman, liminal, not-earth. If the sky reads as dark green or slate, the entire palette logic of SF03 is lost. This is a hard reject and rework.

#### SUNLIT_AMBER / RW-02 — SKIP
Not expected in SF03 — correct. Zero warm light sources in this scene.

**SF03 Asset Verdict: FLAG (Full Rework Required)**

---

### Asset 3: SF01 — Discovery
**Files:** `LTG_COLOR_styleframe_discovery.png` vs `_v003_styled.png`
**Size:** 1920×1080px (MATCH)

#### GL-07 CORRUPT_AMBER — PASS (with notation)

| Coord | Orig | Styled | Δcanonical | Δorig | Status |
|-------|------|--------|------------|-------|--------|
| (1368, 225) | #FF8C00 | #FC8C07 | 7 | 7 | PASS |
| (1377, 225) | #FF8C00 | #FB8B08 | 8 | 8 | PASS |
| (1386, 225) | #FF8C00 | #FB8B08 | 8 | 8 | PASS |
| (1395, 225) | #FF8C00 | #FC8C07 | 7 | 7 | PASS |
| (1323, 243) | #FF8C00 | #163743 | 233 | 233 | FLAG |

**Analysis:** 4 of 5 samples PASS with excellent fidelity (Δ7–8 from canonical). The outlier at (1323,243) — styled as #163743 (dark teal) — is a boundary-edge artifact at the interface of amber outline and cyan monitor background. The amber outline region itself at coords 1368–1395 is confirmed intact and production-ready. GL-07 is preserved in SF01.

#### GL-01b BYTE_TEAL — CONDITIONAL PASS

| Coord | Orig | Styled | Δcanonical | Δorig | Status |
|-------|------|--------|------------|-------|--------|
| (1449, 135) | #00D7EB | #0AD7E9 | 10 | 10 | PASS |
| (1296, 153) | #00F0FF | #0BEFFD | 27 | 11 | FLAG |
| (1305, 153) | #00F0FF | #0BEFFD | 27 | 11 | FLAG |
| (1314, 153) | #00F0FF | #0BEFFD | 27 | 11 | FLAG |
| (1323, 153) | #00F0FF | #0BEFFD | 27 | 11 | FLAG |

**Analysis:** Coord (1449,135): Δcanonical=10, Δorig=10 — clean PASS. Coords (1296–1323, 153): original is #00F0FF (GL-01 Electric Cyan screen glow, not GL-01b Byte Teal body). Styled reproduces as #0BEFFD — Δorig=11, excellent preservation of the original. The Δcanonical=27 reflects the GL-01 vs GL-01b distinction in the source — these are screen-glow pixels, not Byte's body. Screen emission in SF01 is faithfully preserved. CONDITIONAL PASS.

#### UV_PURPLE — SKIP
Not present in SF01 original. Expected — Discovery scene is Real World.

#### SUNLIT_AMBER / RW-02 — MINOR FLAG (Acceptable)

| Coord | Orig | Styled | Δcanonical | Δorig | Status |
|-------|------|--------|------------|-------|--------|
| (0, 135) | #E3B877 | #E1B678 | 30 | 2 | FLAG |
| (9, 135) | #E3B877 | #E0B476 | 28 | 4 | FLAG |
| (18, 135) | #E3B877 | #E0B475 | 27 | 4 | FLAG |
| (27, 135) | #E3B877 | #E0B475 | 27 | 4 | FLAG |
| (36, 135) | #E3B877 | #E0B475 | 27 | 4 | FLAG |

**Analysis:** All samples FLAG vs. canonical, but Δorig=2–4 — styled is nearly identical to original (sub-5 delta). The original warm wall pixels (#E3B877) are scene-derived warm ambient tones, not pure RW-02 #E8C95A. Stylization has faithfully preserved the scene tone; the FLAGs are a tolerance artifact against canonical, not against original. Actual reproduction quality: PASS.

**SF01 Asset Verdict: PASS**

---

### Asset 4: Kitchen — Grandma
**Files:** `LTG_ENV_grandma_kitchen.png` vs `_v003_styled.png`
**Size:** 1920×1080px (MATCH)

#### GL-07 CORRUPT_AMBER — SKIP
Not expected in Grandma Kitchen (Real World environment, pre-Glitch).

#### GL-01b BYTE_TEAL — SKIP
Not expected in Real World kitchen.

#### UV_PURPLE — SKIP
Not expected in Real World kitchen.

#### SUNLIT_AMBER / RW-02 — PASS

| Coord | Orig | Styled | Δcanonical | Δorig | Status |
|-------|------|--------|------------|-------|--------|
| (648, 441) | #F9C354 | #F4C262 | 12 | 14 | PASS |
| (657, 441) | #F9C354 | #F2C060 | 10 | 12 | PASS |
| (666, 441) | #F9C353 | #F2C05F | 10 | 12 | PASS |
| (675, 441) | #F9C353 | #F2C05F | 10 | 12 | PASS |
| (684, 441) | #F9C353 | #F2C05F | 10 | 12 | PASS |

**Analysis:** All 5 samples PASS. Warm amber kitchen tones preserved at Δ10–14 from canonical, Δ12–14 from original. Excellent fidelity. The kitchen warm palette is intact. Rin's stylization process handles Real World warm tones cleanly when no Glitch colors are present.

**Kitchen Asset Verdict: PASS**

---

## Overall Results

| Asset | Verdict | Key Finding |
|-------|---------|-------------|
| SF02 — Glitch Storm | **FLAG** | GL-07 amber hue-rotated to green/yellow; warm window glow shifted to lemon yellow |
| SF03 — Other Side | **FLAG (Critical)** | UV_PURPLE sky + GL-01b cyan + Luma hoodie orange all severely hue-shifted toward green |
| SF01 — Discovery | **PASS** | GL-07 amber intact; warm tones preserved; minor tolerance-edge FLAGs not real failures |
| Kitchen — Grandma | **PASS** | All warm tones within excellent tolerance |

**Overall: ISSUES FOUND — SF02 and SF03 require rework before Critique Cycle 11**

---

## Root Cause Hypothesis

The pattern of failures in SF02 and SF03 is consistent across all sampled colors:
- Amber (#FF8C00) → olive / yellow-green
- Cyan (#00F0FF / #00D4E8) → green
- UV Purple (#7B2FBE) → dark teal-green

This is the signature of a hue rotation (or hue-shift color grading filter) applied globally to the image. A rotation of approximately 30–60° in the HSL/HSV color wheel in the cyan-to-yellow range would explain all observed shifts simultaneously. The Real World assets (SF01, Kitchen) are less affected because their dominant colors (warm amber, Soft Gold) sit in the hue range that such a rotation leaves relatively intact.

**Recommendations to Rin Yamamoto:**
1. Check whether the stylization pipeline applies a global hue or color grading layer
2. If using a rendering or style transfer model, confirm the color space is not being remapped during export
3. For SF02 and SF03, treat GL-07 CORRUPT_AMBER (#FF8C00), GL-01b BYTE_TEAL (#00D4E8), and UV_PURPLE (#7B2FBE) as protected palette values — no global color transformations that affect these entries
4. SF01 and Kitchen: accepted
5. SF03: full re-render required. The UV_PURPLE atmosphere failure makes this asset unusable in current form for Critique Cycle 11

---

## Glitch Character Color Model Verification

**File:** `output/characters/color_models/LTG_COLOR_glitch_color_model.png`
**Generator:** `output/tools/LTG_CHAR_glitch_color_model_v001.py`

Reviewed generator source code for canonical value compliance:

| Check | Finding | Status |
|-------|---------|--------|
| Primary body fill = CORRUPT_AMB = (255, 140, 0) = #FF8C00 | Confirmed in code constant and SWATCHES entry | PASS |
| Body polygon fill calls CORRUPT_AMB | `draw.polygon(pts, fill=CORRUPT_AMB)` confirmed | PASS |
| Swatch list entry 1: "CORRUPT_AMBER — GL-07", "Primary body fill" | Confirmed | PASS |
| Shadow = #A84C00 (168,76,0) — correct darker-amber companion | Confirmed | PASS |
| Highlight = #FFB950 (255,185,80) — correct lighter-amber facet | Confirmed | PASS |
| Header title references "GL-07 CORRUPT_AMBER PRIMARY" | Confirmed | PASS |
| Dual-eye system: NEUTRAL + DESTAB pixel patterns | NEUTRAL (left eye) and DESTAB (right eye) grids present | PASS |
| Eye palette uses amber fills (CORRUPT_AMB, CORRUPT_AMB_SH) for neutral state | PCOLS maps 1→CORRUPT_AMB_SH, 2→CORRUPT_AMB | PASS |
| Electric Cyan listed for panic/pixel-bleed eye state | GL-01 #00F0FF listed in SWATCHES, panic eye role | PASS — correct, Glitch uses GL-01 not GL-01b |

**Glitch Color Model Verdict: PASS — No flag to Maya Santos required.**

CORRUPT_AMBER #FF8C00 = (255, 140, 0) is confirmed as the primary body fill in both the generator constants (`CORRUPT_AMB = (255, 140, 0)`) and the SWATCHES list ("Primary body fill"). The character silhouette body polygon is filled with this value. GL-07 is properly undiluted and unsaturated in the color model. The dual-eye system is present. No corrections needed.

---

## Actions Required

| Action | Owner | Priority |
|--------|-------|----------|
| Rework SF02 stylized PNG — fix GL-07 and warm window hue rotation | Rin Yamamoto | High |
| Rework SF03 stylized PNG — full re-render, protect UV_PURPLE, GL-01b, warm hoodie | Rin Yamamoto | Critical |
| SF01 styled — accepted, no rework required | — | Done |
| Kitchen styled — accepted, no rework required | — | Done |
| Glitch color model — no issues, no rework required | — | Done |

---

*Sam Kowalski — Color & Style Artist — Cycle 24*
*Cross-references: master_palette.md, ltg_style_frame_color_story.md, LTG_TOOL_fidelity_check_c24.py*
