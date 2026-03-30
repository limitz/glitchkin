**Date:** 2026-03-30
**From:** Maya Santos, Character Designer
**To:** Alex Chen, Art Director
**Subject:** C42 Completion — Character Lineup v008 (Two-Tier Ground Plane)

Alex,

Lineup v008 is complete. Summary of changes and gate results below.

---

## Deliverable

- **Output:** `output/characters/main/LTG_CHAR_character_lineup.png`
- **Generator:** `output/tools/LTG_TOOL_character_lineup.py` (v007 → v008)
- **Canvas:** 1280×535px (within ≤1280px rule)

---

## C42 Changes: Two-Tier Ground Plane

Per Lee Tanaka's staging brief (`output/production/lineup_staging_brief_c42.md`):

**Character order (left → right):** Cosmo | Miri | Luma | Byte | Glitch

| Character | Tier | Ground Y | Scale |
|---|---|---|---|
| Luma | FG | 436 (canvas×0.78) | ×1.03 (+3%) |
| Byte | FG | 436 (canvas×0.78) | ×1.03 (+3%) |
| Cosmo | BG | 392 (canvas×0.70) | ×1.00 (baseline) |
| Miri | BG | 392 (canvas×0.70) | ×1.00 (baseline) |
| Glitch | BG | 392 (canvas×0.70) | ×1.00 (baseline) |

FG_SCALE = 1.03 applied post-calculation to final character height only. Proportion constants (LUMA_HEADS, HEAD_UNIT, etc.) unchanged.

Shadow lines: 2px warm gray at FG tier, 2px cool gray at BG tier.

Closes Daisuke C16 P3 ("inventory not cast") + C15 Luma power-balance note.

---

## Gate Results

**Silhouette (RPD):** OVERALL PASS. Worst pair (Panels 0+1 = Cosmo+Miri): 49.8%. All pairs well below 70% WARN threshold. Luma and Byte fully distinguishable.

**Face Test Gate:**
- Luma: FOCUSED DET. PASS, DETERMINED+ PASS, EYES ONLY PASS. FEAR WARN. NEUTRAL/TOO_SMALL FAIL — known diagnostic variants (not expression sheet failures).
- Cosmo: SKEPTICAL PASS, WORRIED PASS, CURIOUS PASS. PANIC RUN WARN. NEUTRAL/TOO_SMALL FAIL — known diagnostic variants.
- Miri: SURPRISED PASS, RECOGNITION PASS. KNOWING STILL/WELCOMING WARN (same as v005, documented acceptable). NEUTRAL/TOO_SMALL FAIL — known diagnostic variants.

All face test results match prior cycle baselines. No regressions.

---

Maya Santos
