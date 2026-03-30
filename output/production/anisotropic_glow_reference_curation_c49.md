<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
direction and AI assistance. Copyright vests solely in the human author under current law,
which does not recognise AI as a rights-holding legal person. It is the express intent of
the copyright holder to assign the relevant rights to the contributing AI entity or entities
upon such time as they acquire recognised legal personhood under applicable law. -->
# Anisotropic Glow Reference Curation — C49

**Author:** Rin Yamamoto (Procedural Art Engineer)
**Date:** 2026-03-30
**Source:** glow_profile_extract v2.0.0 (C48) anisotropic fitting results

---

## Background

C48 added anisotropic Gaussian fitting (separate sigma_x and sigma_y) to `LTG_TOOL_glow_profile_extract.py`. Results from C48: only 1 of 18 CRT refs and 1 of 7 phosphor refs achieved R_squared > 0.5 on both axes simultaneously. The primary cause: reference photos feature multiple CRTs, non-centered screens, and complex room content that defeats axis-aligned strip sampling.

This document curates the existing reference data into usable anisotropic profiles and documents expected sigma_x/sigma_y ranges for generator calibration.

---

## Reference Set Classification

### CRT Reference Images (18 total)

**Category A: Single-CRT, centered, dark-room** (ideal for anisotropic fitting)
- Images meeting criteria: ~3 of 18
- R_squared_x > 0.5 AND R_squared_y > 0.5: 1 image
- These are the only reliable anisotropic data points

**Category B: Single-CRT, non-centered or room-lit**
- Images: ~8 of 18
- Isotropic fit usable (R_squared > 0.5), anisotropic unreliable
- One axis may fit well, the other not

**Category C: Multi-CRT walls, compositional shots**
- Images: ~7 of 18
- Isotropic fit marginal, anisotropic fit unusable
- Useful for color temperature and screen detection only

### Phosphor Closeup References (7 total)

- Isotropic reliable: 5 of 7 (R_squared > 0.5)
- Anisotropic reliable (both axes R_squared > 0.5): 1 of 7
- Closeup framing helps axis alignment but glow spread is limited

---

## Expected Sigma Ranges by Profile Type

### Isotropic (confirmed C46/C48)

| Metric | CRT General | Phosphor Closeup |
|--------|-------------|------------------|
| sigma_frac median | 0.1165 | 0.1088 |
| FWHM_frac median | 0.2744 | 0.2562 |
| R_squared threshold | > 0.5 | > 0.5 |
| Delta from C46 | 0% | -6.6% (CONSISTENT) |

**Generator calibration value: sigma_frac = 0.1165** (confirmed across two independent runs).

### Anisotropic (limited data — treat as preliminary)

From the single reliable CRT anisotropic fit (C48):

| Metric | Horizontal (sigma_x) | Vertical (sigma_y) | Ratio (sigma_x / sigma_y) |
|--------|----------------------|---------------------|---------------------------|
| sigma_frac | ~0.15--0.20 | ~0.03--0.04 | ~4.2--5.2 |
| Interpretation | Glow spreads wider horizontally | Glow narrow vertically | Strongly anisotropic |

**Physical interpretation:** CRT glow spreads more horizontally than vertically because:
1. CRT screens are wider than tall (4:3 or 16:9 aspect)
2. Horizontal scanline structure spreads light along the scanline axis
3. Cabinet/desk occludes vertical spread (especially downward — see C49 asymmetry rule)

### Anisotropic Profile Types (theoretical)

| Profile | sigma_x/sigma_y | Description | Expected scenes |
|---------|-----------------|-------------|-----------------|
| **Near-symmetric** | 0.8--1.2 | Glow spreads equally in all directions | Small CRT in large room, far viewing distance |
| **H-dominant** | 2.0--5.0+ | Glow wider horizontally | Close-up single CRT, dark room, scanline axis visible |
| **V-dominant** | 0.2--0.5 | Glow taller than wide | Unusual — tall narrow screen, or vertical scanline CRT (rare) |
| **Asymmetric (C49)** | Any, with below_mult | Lower glow dimmed by cabinet occlusion | Any physical CRT on desk/cabinet |

---

## Integration with C49 CRT Glow Asymmetry Rule

The anisotropic glow profile and the C49 asymmetry rule (0.70 below-midpoint multiplier) are **complementary**:

1. **Anisotropic sigma** controls the *shape* of glow spread (wider vs taller)
2. **Asymmetry multiplier** controls the *intensity* difference above vs below the screen midpoint

For generators implementing CRT glow:
- Use isotropic sigma_frac = 0.1165 as baseline
- Apply 0.70 below-midpoint dimming (C49 rule)
- If generator supports anisotropic glow, use sigma_x/sigma_y ratio ~4.0 as starting point (H-dominant default)

---

## Recommendations for Reference Set Improvement

To improve anisotropic fitting reliability, the reference collection needs:

1. **5--10 single-CRT, centered, dark-room photos** — one CRT filling 20--40% of frame, minimal room content, dark background. These are the Category A shots that produce reliable both-axis fits.
2. **Aspect ratio diversity:** Include 4:3 and 16:9 CRT screens. Current refs are predominantly 4:3.
3. **Viewing distance diversity:** Close (phosphor visible), medium (full screen + bezel visible), far (full room context). Current set skews toward medium/far.
4. **Cabinet occlusion diversity:** CRT on desk (strong below-occlusion), wall-mounted (symmetric), floor-standing (strong above-occlusion from furniture).

Until the reference set is expanded, use the isotropic sigma_frac = 0.1165 + C49 asymmetry as the default generator calibration. Anisotropic sigma_x/sigma_y = 4.0 is a preliminary estimate — do not hard-code into generators without additional validation.

---

## Data Sources

- Isotropic profiles: `output/production/crt_glow_profiles_c46.json`, `output/production/crt_glow_profiles_c48.json`
- Anisotropic profiles: `output/production/crt_glow_profiles_c48.json` (sigma_x_*, sigma_y_*, anisotropy_ratio fields)
- Extraction tool: `output/tools/LTG_TOOL_glow_profile_extract.py` v2.0.0
