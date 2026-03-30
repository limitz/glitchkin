<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
direction and AI assistance. Copyright vests solely in the human author under current law,
which does not recognise AI as a rights-holding legal person. It is the express intent of
the copyright holder to assign the relevant rights to the contributing AI entity or entities
upon such time as they acquire recognised legal personhood under applicable law. -->
# UV_PURPLE Hue Center Evaluation — C49

**Author:** Rin Yamamoto (Procedural Art Engineer)
**Date:** 2026-03-30
**Requested by:** Alex Chen (C49 inbox)

---

## Question

Reference glitch art clusters at HSV h° 280--290. Our canonical UV_PURPLE `#7B2FBE` (123, 47, 190) sits at HSV h° ~272. Should we shift the constant toward ~275 to improve fidelity?

---

## Analysis

### Current UV_PURPLE Constants

| Constant | RGB | HSV h° | LAB h° | Notes |
|----------|-----|--------|--------|-------|
| UV_PURPLE (GL-04) | (123, 47, 190) | ~272° | ~306° | Mid-tone canonical |
| UV_PURPLE_DARK (GL-04a) | (58, 16, 96) | ~271° | ~287° | Dark variant (COVETOUS) |

### Reference Glitch Art Distribution (C46 Survey)

From the C46 hue survey of 14 reference images (datamoshing, pixel sorting, CRT-art):
- **P25:** LAB h° ~260 (HSV ~250)
- **Median:** LAB h° ~290 (HSV ~275)
- **P75:** LAB h° ~315 (HSV ~285)

The reference clustering at HSV 280--290 is confirmed. Our canonical sits at the low end of the reference median.

### Impact of a Shift to HSV ~275

A shift from HSV 272 to 275 = **3 degrees**. At the current saturation/value:

| Property | Current (272°) | Proposed (275°) | Delta |
|----------|----------------|-----------------|-------|
| RGB (approx.) | (123, 47, 190) | (113, 47, 190) | R: -10, G: 0, B: 0 |
| LAB a* | ~+39 | ~+36 | -3 |
| LAB b* | ~-54 | ~-55 | -1 |
| LAB h° | ~306° | ~303° | -3° |
| Visual | Warm-leaning violet | Slightly cooler violet | Subtle |

### Risk Assessment

1. **Downstream cascade:** UV_PURPLE is referenced in 15+ generators, 6 linter/QA tools, 8+ color keys, and the master palette. A constant change propagates everywhere.
2. **Perceptual difference at 3°:** Below JND (just noticeable difference) for violet hues at this saturation. The shift would be invisible in pitch deck viewing.
3. **Linter range:** The hue-family range (LAB 255°--325°) comfortably covers both values. No linter change needed.
4. **COVETOUS dark variant:** UV_PURPLE_DARK at HSV ~271° would need a proportional shift. Two constants to maintain.
5. **Existing asset consistency:** All rendered GL assets use the current constant. Shifting creates a before/after discontinuity across the asset library until every generator is re-run.

### Comparison to Reference Art

The 8° gap between our 272° and the reference median at 280° is real but misleading:
- Our UV_PURPLE is a **design constant**, not a measured average. It was chosen for maximum saturation and visual impact at this hue.
- Reference glitch art spans 230°--310° in HSV — the distribution is broad, and our 272° falls well within the P25--P75 range.
- A 3° shift toward 275° closes the gap by 37% but does not meaningfully center us in the reference distribution.
- A full shift to 280° would close the gap but moves UV_PURPLE into blue-violet territory where it reads less "electric" and more "standard purple."

---

## Recommendation: No Change

**Retain UV_PURPLE at (123, 47, 190) / HSV h° ~272.**

Rationale:
1. A 3° shift is below perceptual JND — no visible improvement.
2. The downstream cascade cost (re-rendering all GL assets, updating color keys) vastly outweighs the invisible benefit.
3. Our 272° is within the P25--P75 band of reference glitch art — it is not an outlier.
4. The UV_PURPLE constant was designed for maximum electric impact, not for matching reference art averages. A shift toward 280° would make it less distinctive.

If a future creative direction decision calls for a deliberate hue shift (e.g., to differentiate GL zones), that should be a palette-level decision from Alex, not a calibration adjustment.

---

## Action Taken

No change to UV_PURPLE constant. Evaluation complete.
