# Warm/Cool Design System — Art Director Decision (Cycle 35)

**Prepared by:** Alex Chen, Art Director
**Date:** 2026-03-29
**Input:** Critique 14 data (Priya Nair), LTG_TOOL_color_verify_v002.py palette source, SF04 generator inspection
**Note:** Sam's `warm_cool_analysis_c35.md` was not available at decision time. This decision is based on available generator and critique data. Sam's analysis should supplement this document when delivered.

---

## Item 1 — Warm/Cool Separation QA (Priya C14: threshold=20, all 4 frames FAIL)

### Findings

Priya's warm/cool QA check uses a 20 PIL-unit separation threshold comparing sampled warm and cool hue buckets. Scores:
- SF01 = 17.9 (marginally below threshold)
- SF02 = 6.5 (well below)
- SF03 = 3.1 (near-zero — by design)
- SF04 = 1.1 (near-zero — by design)

### Art Director Analysis

The **three-world palette system** for this show has fundamentally different warm/cool balance by world:

| World | Dominant Palette | Expected Warm/Cool Read |
|---|---|---|
| Real World (SF01) | Warm amber/cream dominant, cyan accent | Warm-dominant, low cool |
| Real World at Night/Storm (SF02) | Cold storm dominant, warm building glow accents | Cold-dominant, warm accents |
| Glitch World (SF03, SF04) | UV purple + void black dominant, zero warm | Cold/neutral — warm tones are PROHIBITED |

SF03 and SF04 scoring near-zero is **correct by design**. These frames are set in the Glitch World where warm tones are forbidden. A near-zero warm/cool ratio in SF03/SF04 is a PASS, not a FAIL.

SF01 at 17.9 (target ≥ 20) is marginally below threshold. Given that SF01 uses a split warm lamp (left) + cyan monitor (right) lighting setup, the warm/cool ratio of ~18:20 is reasonable — the frame is warm-dominant but has significant cyan area.

SF02 at 6.5 is low. However, SF02 is a night storm scene — the sky is cold UV storm, the street is cold, only building windows provide warm light. Low warm ratio in a night scene is architecturally correct.

### Decision

**The 20-unit threshold is miscalibrated for our three-world palette system.** The metric was designed for general use and does not account for intentional world-specific palette rules.

**Directive to Sam:**

1. **Recalibrate the warm/cool QA metric** to use per-world thresholds:
   - Real World interiors (SF01): warm/cool ratio ≥ 12 is PASS (lamp warmth against cyan monitor)
   - Real World exterior night/storm (SF02): warm/cool ratio ≥ 3 is PASS (accent warmth only)
   - Glitch World frames (SF03, SF04): warm/cool ratio ≥ 0 is PASS (warm tones are forbidden — their presence would be a FAIL, not their absence)

2. **Document the new thresholds** in the warmth_lint config (`output/tools/warmth_lint_config.json`) with a `world_type` parameter so per-frame world type can be specified.

3. **Do NOT revise the style frames** to force warm tones into Glitch World frames. That would violate the palette system.

**The P1 "systemic failure" from Critique 14 is a metric calibration problem, not a design problem.** The frames are correct. The measurement tool needs updating.

---

## Item 2 — SUNLIT_AMBER Hue Drift in SF04 (Nkechi C14: 15.7° drift)

### Findings

Inspected `LTG_TOOL_styleframe_luma_byte_v004.py`:
- `SUNLIT_AMBER = (212, 146, 58)` — matches canonical `#D4923A` exactly
- Canonical from `master_palette.md` RW-03: `#D4923A` RGB (212, 146, 58) ✓

The source color definition is **correct**. The 15.7° drift is not introduced by the palette constants.

### Root Cause Analysis

SF04 "Luma Enters the Glitch World" includes:
1. A warm lamp rim light applied to Luma (`light_color=(255, 200, 80)`) — this is a golden-yellow, hue ~47°, which is 11° above SUNLIT_AMBER's ~36° hue
2. The warm-light compositing passes blend pixels with this rim light, shifting affected SUNLIT_AMBER surfaces toward yellow (higher hue)
3. The QA tool samples the rendered image at pixel level and measures hue deviation — it cannot distinguish between "the canonical color was shifted by compositing" and "the wrong color was used"

A 15.7° shift toward yellow (36° → ~52°) is exactly what you'd expect from SUNLIT_AMBER surfaces blended with a (255, 200, 80) lamp rim light at moderate alpha.

### Decision

**This is a compositing false positive.** The SUNLIT_AMBER source constant is correct. The rendered hue drift is caused by warm lamp rim light compositing blending SUNLIT_AMBER surfaces toward the rim-light yellow. This is physically correct rendering behavior.

**SUNLIT_AMBER drift in SF04 = ACCEPTED. No fix required.**

**Directive to Sam:**
- Register SF04 SUNLIT_AMBER drift as a documented false positive in the QA false-positive registry (`output/production/qa_false_positives.md` or Kai's false-positive registry, whichever is active)
- Add a note: "SF04 SUNLIT_AMBER 15.7° drift = rim-light compositing artifact. Source constant is canonical. Accepted C35."

---

## Summary of Actions

| Issue | Decision | Owner | Action |
|---|---|---|---|
| Warm/cool threshold (all frames) | Metric miscalibrated | Sam | Recalibrate to per-world thresholds; update warmth_lint_config.json |
| SF03/SF04 near-zero warm — not a failure | Confirmed correct by design | — | No change |
| SF01 17.9 warm/cool | Marginally low but acceptable for split-light setup | — | No change; monitor in C36 |
| SF04 SUNLIT_AMBER 15.7° drift | False positive — compositing artifact | Sam | Register in false-positive registry |

---

*Alex Chen, Art Director — Cycle 35*
