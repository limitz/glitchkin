# LTG_TOOL_expression_silhouette — Test Results

**Author:** Maya Santos — Cycle 33
**Date:** 2026-03-29
**Tool:** `output/tools/LTG_TOOL_expression_silhouette.py`

---

## Summary

Expression silhouette differentiation test tool built and validated.
Metric: combined similarity = 0.6 × IoM + 0.4 × XOR_similarity.
Thresholds: WARN ≥ 72%, FAIL ≥ 85%.

---

## Baseline Run — Current Expression Sheets

| Sheet | Grid | Active | Result | Worst Pair | Worst Sim |
|---|---|---|---|---|---|
| `LTG_CHAR_luma_expressions.png` | 3×3 | 7/9 | FAIL | P1↔P2 | 91.0% |
| `LTG_CHAR_glitch_expression_sheet.png` | 3×3 | 5/9 | **PASS** | P0↔P1 | 71.1% |
| `LTG_CHAR_grandma_miri_expression_sheet.png` | 3×3 | 9/9 | FAIL | P1↔P2 | 93.6% |
| `LTG_CHAR_cosmo_expression_sheet.png` | 3×3 | 9/9 | FAIL | P1↔P2 | 95.9% |
| `LTG_CHAR_byte_expression_sheet.png` | 3×3 | 9/9 | FAIL | P7↔P8 | 88.8% |

---

## Key Findings

### Glitch — PASS
- Glitch's compact diamond body with unique tilts/squashes gives distinct silhouettes.
- Dark BG (VOID_BLACK) required lowering `MIN_CHAR_FRACTION` from 5% to 1%.

### Luma v008 — FAIL (P1↔P2: CURIOUS↔DETERMINED, 91%)
- Body mass is very similar between these two expressions at panel resolution (382×282px).
- Arm position differences are small relative to total body mass.
- This confirms the critics' ongoing concern about Luma's expression differentiation.
- Recommendation: future expression sheets should exaggerate arm/leg spread on poses
  that currently look similar (CURIOUS arm should extend WIDER, DETERMINED stance wider).

### Miri v002 — FAIL (P1↔P2: 93.6%)
- P0-P2 are WARM/WELCOMING, SKEPTICAL/AMUSED, CONCERNED — similar compact postures.
- v003 would need to exaggerate these more.

### Cosmo v003 — FAIL (P1↔P2: 95.9%)
- Panels 0/1/2 form a cluster of similar upright postures.
- Body language differentiation on Cosmo is weak at this scale.

### Byte v003 — FAIL (P7↔P8: 88.8%)
- Last two expressions are the most similar.
- Overall only 1 FAIL pair (better than other characters) — Byte's pixel body is
  naturally more geometric/distinct.

---

## Algorithm Notes

- **BG tolerance = 45** (per-channel). Works well for warm parchment BGs.
  Dark BG sheets (Glitch) work because the panel BG is also dark.
- **Min char fraction = 1%** to handle compact diamond shapes (Glitch).
- **Combined metric** avoids penalizing full-body sheets for sharing body mass.
- **Limitation:** At 382×282px panel resolution, arm pose differences smaller than
  ~20px are difficult to capture in silhouette comparison. This is an inherent
  resolution limit, not a tool bug.

---

## Usage

```
python3 output/tools/LTG_TOOL_expression_silhouette.py <sheet.png> [options]
  --rows R            Override row count (auto-detected from sheet size)
  --cols C            Override column count
  --threshold 0.85    IoM fail threshold
  --warn-threshold 0.72
  --output sil.png    Save silhouette contact sheet
  --json              Output JSON result
```

Exit codes: 0=PASS, 1=WARN, 2=FAIL.

Contact sheet: `LTG_TOOL_expression_silhouette_test_luma.png`
