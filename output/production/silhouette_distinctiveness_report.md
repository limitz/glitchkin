# Silhouette Distinctiveness Report

**Characters:** luma_turnaround, cosmo_turnaround, miri_turnaround, byte_turnaround, glitch_turnaround
**Scales:** 100%, 50%, 25%

**Overall: FAIL** — 5 PASS, 2 WARN, 3 FAIL out of 10 pairs

## Pairwise Results

| Pair | Scale | DS | SOR | WPC | Verdict |
|------|-------|----|-----|-----|---------|
| luma_turnaround vs cosmo_turnaround | 100% | 0.3243 | 0.8322 | 0.5192 | PASS |
| luma_turnaround vs cosmo_turnaround | 50% | 0.2948 | 0.8387 | 0.5717 | WARN |
| luma_turnaround vs cosmo_turnaround | 25% | 0.3631 | 0.8255 | 0.4483 | PASS |
| luma_turnaround vs miri_turnaround | 100% | 0.0215 | 0.9569 | 1.0000 | FAIL |
| luma_turnaround vs miri_turnaround | 50% | 0.0202 | 0.9597 | 1.0000 | FAIL |
| luma_turnaround vs miri_turnaround | 25% | 0.0186 | 0.9628 | 1.0000 | FAIL |
| luma_turnaround vs byte_turnaround | 100% | 0.5378 | 0.4696 | 0.4549 | PASS |
| luma_turnaround vs byte_turnaround | 50% | 0.5153 | 0.4785 | 0.4910 | PASS |
| luma_turnaround vs byte_turnaround | 25% | 0.5503 | 0.4435 | 0.4559 | PASS |
| luma_turnaround vs glitch_turnaround | 100% | 0.9692 | 0.0584 | 0.0032 | PASS |
| luma_turnaround vs glitch_turnaround | 50% | 0.9193 | 0.0646 | 0.0968 | PASS |
| luma_turnaround vs glitch_turnaround | 25% | 0.9788 | 0.0425 | -0.0345 | PASS |
| cosmo_turnaround vs miri_turnaround | 100% | 0.0401 | 0.9197 | 1.0000 | FAIL |
| cosmo_turnaround vs miri_turnaround | 50% | 0.0396 | 0.9209 | 1.0000 | FAIL |
| cosmo_turnaround vs miri_turnaround | 25% | 0.0397 | 0.9206 | 1.0000 | FAIL |
| cosmo_turnaround vs byte_turnaround | 100% | 0.5611 | 0.4574 | 0.4205 | PASS |
| cosmo_turnaround vs byte_turnaround | 50% | 0.5258 | 0.4573 | 0.4911 | PASS |
| cosmo_turnaround vs byte_turnaround | 25% | 0.4979 | 0.4557 | 0.5485 | PASS |
| cosmo_turnaround vs glitch_turnaround | 100% | 0.9476 | 0.1048 | -0.5902 | PASS |
| cosmo_turnaround vs glitch_turnaround | 50% | 0.9487 | 0.1027 | -0.5940 | PASS |
| cosmo_turnaround vs glitch_turnaround | 25% | 0.9507 | 0.0986 | -0.5734 | PASS |
| miri_turnaround vs byte_turnaround | 100% | 0.0195 | 0.9611 | 1.0000 | FAIL |
| miri_turnaround vs byte_turnaround | 50% | 0.0162 | 0.9675 | 1.0000 | FAIL |
| miri_turnaround vs byte_turnaround | 25% | 0.0228 | 0.9544 | 1.0000 | FAIL |
| miri_turnaround vs glitch_turnaround | 100% | 0.2023 | 0.5954 | 1.0000 | WARN |
| miri_turnaround vs glitch_turnaround | 50% | 0.2039 | 0.5922 | 1.0000 | WARN |
| miri_turnaround vs glitch_turnaround | 25% | 0.2061 | 0.5877 | 1.0000 | WARN |
| byte_turnaround vs glitch_turnaround | 100% | 0.9655 | 0.0691 | -0.1945 | PASS |
| byte_turnaround vs glitch_turnaround | 50% | 0.8959 | 0.0651 | 0.1431 | PASS |
| byte_turnaround vs glitch_turnaround | 25% | 0.9629 | 0.0741 | -0.0679 | PASS |

## Metric Definitions
- **DS** (Distinctiveness Score): 1.0 = completely distinct, 0.0 = identical. DS = 1 - (0.5*SOR + 0.5*WPC)
- **SOR** (Silhouette Overlap Ratio): intersection / min(area). High = similar.
- **WPC** (Width Profile Correlation): Pearson r of per-row width. High = similar shape.
- **Thresholds**: FAIL < 0.15, WARN < 0.30, PASS >= 0.30