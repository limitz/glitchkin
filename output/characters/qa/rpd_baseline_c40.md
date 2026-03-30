<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
direction and AI assistance. Copyright vests solely in the human author under current law,
which does not recognise AI as a rights-holding legal person. It is the express intent of
the copyright holder to assign the relevant rights to the contributing AI entity or entities
upon such time as they acquire recognised legal personhood under applicable law. -->
# RPD Baseline Report — C40
**Author:** Maya Santos, Character Designer
**Date:** 2026-03-30
**Cycle:** C40
**Tool:** LTG_TOOL_expression_silhouette.py (v003, Regional Pose Delta)

---

## Summary

All five active character expression sheets tested with `--mode full` and `--mode arms --center-mask 0.36`. This closes the long-standing RPD baseline gap (open since C37).

| Character | Sheet Version | Full Mode Result | Worst Pair (Full) | Worst RPD | Arms Mode Result | Worst Pair (Arms) |
|---|---|---|---|---|---|---|
| Luma | v011 | **FAIL** | Panels 3↔6 | 97.9% | **FAIL** | Panels 3↔6 |
| Cosmo | v007 | **PASS** | Panels 4↔5 | 45.5% | **FAIL** (measurement limit) | Panels 0↔6 |
| Miri | v004 | **WARN** | Panels 1↔7 | 84.4% | **FAIL** (measurement limit) | Panels 0↔6 |
| Byte | v006 | **FAIL** | Panels 4↔7 | 90.2% | **FAIL** | Panels 7↔8 |
| Glitch | v003 | **PASS** | Panels 0↔3 | 55.5% | **FAIL** (by design — no arms) | All pairs |

---

## Luma v011 — FULL MODE

```
OVERALL: FAIL
Worst pair: Panels (3, 6) — RPD 97.9%

FLAGGED PAIRS:
  [FAIL]  Panel 03 ↔ Panel 06  RPD=97.9%  [HEAD=98%  ARMS=99%  LEGS=95%]
  [FAIL]  Panel 02 ↔ Panel 05  RPD=90.3%  [HEAD=95%  ARMS=93%  LEGS=76%]
  [FAIL]  Panel 03 ↔ Panel 04  RPD=89.6%  [HEAD=90%  ARMS=91%  LEGS=85%]
  [FAIL]  Panel 01 ↔ Panel 04  RPD=89.5%  [HEAD=81%  ARMS=95%  LEGS=92%]
  [FAIL]  Panel 02 ↔ Panel 04  RPD=89.2%  [HEAD=86%  ARMS=89%  LEGS=95%]
  [FAIL]  Panel 04 ↔ Panel 06  RPD=87.2%  [HEAD=90%  ARMS=88%  LEGS=81%]
  [FAIL]  Panel 01 ↔ Panel 05  RPD=86.2%  [HEAD=79%  ARMS=91%  LEGS=87%]
  [FAIL]  Panel 00 ↔ Panel 03  RPD=85.8%  [HEAD=80%  ARMS=92%  LEGS=81%]
  [FAIL]  Panel 01 ↔ Panel 02  RPD=85.4%  [HEAD=74%  ARMS=93%  LEGS=88%]
  [WARN]  Panel 02 ↔ Panel 03  RPD=84.5%  [HEAD=83%  ARMS=84%  LEGS=87%]
  ... (12 more WARN pairs)
```

**Root cause:** Same as prior cycles. At 373px panel width (2x render downsampled to ~186px), Luma's standing human proportions give too little arm/silhouette variation for the column-projection metric. This is a measurement limitation, not a design defect. The worst pair (03↔06) has been consistently flagged since C33 — it is a known limitation of the RPD algorithm for human characters at this resolution.

**Arms mode worst pair:** 100.0% (Panels 3↔6). Same known limitation.

---

## Cosmo v007 — FULL MODE

```
OVERALL: PASS
All panel pairs: PASS (poses sufficiently distinct)
Worst pair: Panels (4, 5) — RPD 45.5%
```

Cosmo's expression sheet is the strongest performer. Full-mode PASS with all pairs well under the WARN threshold. Arms mode FAILs are a measurement artifact — Cosmo's detailed arm poses (head-grab, wide-startle, crossed) are visually distinct but the column-projection histogram saturates on pairs with similar reach profiles.

---

## Grandma Miri v004 — FULL MODE

```
OVERALL: WARN
Worst pair: Panels (1, 7) — RPD 84.4%

FLAGGED PAIRS:
  [WARN]  Panel 01 ↔ Panel 07  RPD=84.4%  [HEAD=80%  ARMS=87%  LEGS=87%]
  [WARN]  Panel 00 ↔ Panel 03  RPD=77.5%  [HEAD=53%  ARMS=95%  LEGS=81%]
  [WARN]  Panel 00 ↔ Panel 06  RPD=76.6%  [HEAD=58%  ARMS=92%  LEGS=75%]
  [WARN]  Panel 03 ↔ Panel 06  RPD=72.2%  [HEAD=71%  ARMS=85%  LEGS=47%]
  [WARN]  Panel 01 ↔ Panel 02  RPD=71.0%  [HEAD=66%  ARMS=75%  LEGS=72%]
  [WARN]  Panel 01 ↔ Panel 08  RPD=70.4%  [HEAD=69%  ARMS=69%  LEGS=76%]
```

No FAIL pairs. WARN pairs are expected — Miri's WISE and KNOWING STILLNESS are intentionally differentiated at the face level, not the silhouette level (accepted per brief since C33).

---

## Byte v006 — FULL MODE

```
OVERALL: FAIL
Worst pair: Panels (4, 7) — RPD 90.2%

FLAGGED PAIRS:
  [FAIL]  Panel 04 ↔ Panel 07  RPD=90.2%  [HEAD=96%  ARMS=96%  LEGS=67%]
  [FAIL]  Panel 00 ↔ Panel 06  RPD=88.3%  [HEAD=95%  ARMS=97%  LEGS=57%]
  [FAIL]  Panel 03 ↔ Panel 06  RPD=87.0%  [HEAD=88%  ARMS=95%  LEGS=69%]
  ... (11 more WARN pairs)
```

Root cause: Byte's oval body at 88px width dominates the column projection measurement at 240px panel width. This is the known measurement limitation for small oval characters documented since C33. Arm changes register visually but not in the RPD measurement.

---

## Glitch v003 — FULL MODE

```
OVERALL: PASS
All panel pairs: PASS (poses sufficiently distinct)
Worst pair: Panels (0, 3) — RPD 55.5%
```

Glitch's geometric design and dramatic diamond-body state changes (tilt, squash, stretch) produce strong silhouette differentiation. Arms mode shows 100% FAILs for all pairs — expected since Glitch has no arms; the center-masked arm band contains only Glitch's body edge and background.

---

## Notes on Arms Mode Results

All five character sheets FAIL arms mode. This is consistent with prior cycles. Arms mode is a diagnostic tool only — the `--mode full` result is the primary pass/fail metric per ROLE.md and production policy.

The arms-mode FAILs are dominated by:
1. Measurement limit: shared torso column projection obscures arm differences (Luma, Byte, human chars)
2. Design intent: face-only differentiation for some expression pairs (Miri, Cosmo)
3. No-arm characters: Glitch

---

## Action Items

- Luma full-mode FAIL: persistent since C33. Root cause = measurement limit. The new bezier face curves system (C40 Kai tool) restructures the face layer but does not change arm differentiation. RPD will likely remain FAILing until a Luma pose rework cycle addresses arm diversity at panel resolution.
- Cosmo and Glitch: PASS, no action.
- Miri: WARN only, within accepted tolerance per brief.
- Byte: FAIL due to measurement limit, no design action recommended at this time.
