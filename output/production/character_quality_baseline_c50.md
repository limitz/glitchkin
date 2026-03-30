# Character Quality Baseline — Cycle 50

Generated 2026-03-30 by Kai Nakamura using three new character quality tools.

## 1. Silhouette Distinctiveness

**Overall: FAIL** — 3 FAIL, 2 WARN, 5 PASS out of 10 pairs

| Pair | 100% DS | 50% DS | 25% DS | Worst | Verdict |
|------|---------|--------|--------|-------|---------|
| Luma vs Cosmo | 0.3243 | 0.2948 | 0.3631 | 0.2948 | WARN |
| **Luma vs Miri** | **0.0215** | **0.0202** | **0.0186** | **0.0186** | **FAIL** |
| Luma vs Byte | 0.5378 | 0.5153 | 0.5503 | 0.5153 | PASS |
| Luma vs Glitch | 0.9692 | 0.9193 | 0.9788 | 0.9193 | PASS |
| **Cosmo vs Miri** | **0.0401** | **0.0396** | **0.0397** | **0.0396** | **FAIL** |
| Cosmo vs Byte | 0.5611 | 0.5258 | 0.4979 | 0.4979 | PASS |
| Cosmo vs Glitch | 0.9476 | 0.9487 | 0.9507 | 0.9476 | PASS |
| **Miri vs Byte** | **0.0195** | **0.0162** | **0.0228** | **0.0162** | **FAIL** |
| Miri vs Glitch | 0.2023 | 0.2039 | 0.2061 | 0.2023 | WARN |
| Byte vs Glitch | 0.9655 | 0.8959 | 0.9629 | 0.8959 | PASS |

**Critical findings:**
- **Luma vs Miri: DS=0.02** — essentially identical silhouettes at all scales
- **Cosmo vs Miri: DS=0.04** — near-identical
- **Miri vs Byte: DS=0.02** — near-identical (turnaround sheets may share grid layout affecting measurement, but width profile correlation at 1.0 is alarming)
- Glitch is the only character with a truly unique silhouette
- Luma vs Cosmo borderline WARN at 50% scale

## 2. Expression Range

**Overall: WARN** (Glitch expression sheet is WARN; others PASS)

| Sheet | ERS | Verdict | WARN pairs | FAIL pairs |
|-------|-----|---------|------------|------------|
| Luma | 0.1716 | PASS | 1 | 0 |
| Cosmo | 0.2160 | PASS | 7 | 0 |
| Byte | 0.2641 | PASS | 13 | 0 |
| **Glitch** | **0.0672** | **WARN** | **12** | **0** |
| Miri | 0.2715 | PASS | 3 | 0 |

**Critical findings:**
- **Glitch has 12 WARN pairs out of 15** — expressions labeled differently but face region barely changes
- Byte has 13 WARN pairs, concentrated among P0-P5 (first 6 panels) — top half of expression set is too samey
- Cosmo has 7 WARN pairs, including P0/P1/P2 cluster and P3/P4/P5 cluster — expressions within each group are too similar

## 3. Construction Stiffness

**Overall: FAIL** — 2 FAIL, 2 WARN, 1 PASS

| Character | Outline px | Straight % | Longest Run | Stiffness | Verdict |
|-----------|-----------|------------|-------------|-----------|---------|
| **Luma** | 25147 | **64.1%** | 1117px | **0.4026** | **FAIL** |
| Cosmo | 16219 | 48.2% | 91px | 0.2914 | WARN |
| Miri | 20787 | 47.1% | 783px | 0.2978 | WARN |
| **Byte** | 13888 | **65.6%** | 1437px | **0.4350** | **FAIL** |
| Glitch | 4081 | 27.2% | 36px | 0.1667 | PASS |

**Critical findings:**
- **Luma and Byte both FAIL** — over 64% straight-line outlines, long geometric runs
- Cosmo and Miri are WARN — nearly half the outline is straight lines
- Only Glitch passes — likely because its non-humanoid form uses organic shapes
- Luma has a 1117px straight run — that is a long unbroken geometric edge that screams "constructed with rectangles"

## Priority Recommendations

1. **Miri silhouette is the most urgent fix** — nearly identical to Luma, Cosmo, AND Byte. She needs a radically different body shape (height, proportions, or posture).
2. **Luma construction needs curve passes** — hoodie folds, hair wave, and posture asymmetry would break up the straight edges.
3. **Byte construction** — expected to be more geometric (digital character), but 65% is excessive even for Byte. Some organic element (screen flicker glow, antenna curve) would help.
4. **Glitch expression range** — the face region changes need to be much bolder between expressions. Non-humanoid characters should lean into extreme shape-shifting.
5. **Byte expression sheet P0-P5** — six expressions that barely differ. Need stronger eyebrow/eye/mouth shape changes.
