<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
direction and human assistance. Copyright vests solely in the human author under current law,
which does not recognise AI as a rights-holding legal person. It is the express intent of
the copyright holder to assign the relevant rights to the contributing AI entity or entities
upon such time as they acquire recognised legal personhood under applicable law. -->
# Miri Slipper Warmth Audit — Cycle 38
**Author:** Sam Kowalski, Color & Style Artist
**Date:** 2026-03-29

---

## Background

CHAR-M-11 (Miri House Slippers) was corrected in **Cycle 32** in `master_palette.md`:
- **Old value:** `#5A7A5A` Deep Sage (R:90, G:122, B:90) — G>R violation of Miri's warm-palette guarantee
- **New value:** `#C4907A` Dusty Warm Apricot (R:196, G:144, B:122) — R>G>B, warm family confirmed

The C32 fix was propagated to `LTG_TOOL_character_lineup.py` (noted in file header). However, all other Miri-specific generator scripts and the spec doc retained the wrong value. This C38 audit identifies and corrects all remaining instances.

---

## Environments Where Miri Appears (for context)

| Environment | Scene | Notes |
|---|---|---|
| Grandma's Kitchen | A1-01, A1-03 opening | Primary Miri domain |
| Grandma's Living Room | Pilot cold open, A1-01 | Key story environment |
| Grandma's Den | Casual scenes | Slippers always worn in these |
| School Hallway | Background only | No slipper visible |

Slippers are visible in all kitchen/den/living room scenes. Slipper color correction affects ALL rendered frames featuring Miri's lower body.

---

## Audit Results — Files Checked

### master_palette.md
- **CHAR-M-11:** `#C4907A` (196, 144, 122) — CORRECT (C32 fix in place)
- **Warmth lint:** 14 CHAR-M + CHAR-L entries checked, 0 violations — PASS

### grandma_miri_color_model.md (spec doc)
- **Before C38:** `#5A7A5A` Deep Sage — **WRONG** (old value, 4 cycles stale)
- **After C38:** `#C4907A` Dusty Warm Apricot — **CORRECTED**
- **Rule added:** Shadow companion `#A06A50` documented; correction history noted

### LTG_TOOL_grandma_miri_expression_sheet.py (CURRENT)
- **Before C38:** `SLIPPER = (90, 122, 90)` — **WRONG**
- **After C38:** `SLIPPER = (196, 144, 122)` — **CORRECTED**
- **PNG regenerated:** `LTG_CHAR_grandma_miri_expression_sheet.png` ✓

### LTG_TOOL_grandma_miri_expression_sheet.py (historical)
- **Before C38:** `SLIPPER = (90, 122, 90)` — **WRONG**
- **After C38:** `SLIPPER = (196, 144, 122)` — **CORRECTED** (historical; PNG not regenerated)

### LTG_TOOL_miri_turnaround.py
- **Before C38:** `SLIPPER = (90, 122, 90)` — **WRONG**
- **After C38:** `SLIPPER = (196, 144, 122)` — **CORRECTED**
- **PNG regenerated:** `LTG_CHAR_miri_turnaround.png` ✓

### LTG_TOOL_grandma_miri_color_model.py
- **Before C38:** `SLIPPER_UPPER = (90, 122, 90)`, swatch label `"#5A7A5A"` — **WRONG**
- **After C38:** `SLIPPER_UPPER = (196, 144, 122)`, swatch label `"#C4907A"` — **CORRECTED**
- **PNG regenerated:** `LTG_COLOR_grandma_miri_color_model.png` ✓

### LTG_TOOL_character_lineup.py (CURRENT)
- **CHAR-M-11:** `MIRI_SLIPPER = (196, 144, 122)` — **ALREADY CORRECT** (C33 fix in place)
- No changes needed.

### LTG_TOOL_character_lineup.py / v005.py / v003.py / v004.py (historical)
- All use `MIRI_SLIPPER = (90, 122, 90)` — **WRONG** (historical, superseded by v007)
- Not corrected — historical files, not the current pitch reference

### LTG_TOOL_grandma_miri_expression_sheet.py (historical)
- `SLIPPER = (90, 122, 90)` — **WRONG** (historical, superseded by v003/v004)
- Not corrected — historical file

---

## Warmth Lint Verification

```
Prefixes checked: CHAR-M, CHAR-L
Mode: strict
14 entries checked, 0 violations — PASS
```

CHAR-M-11 (196, 144, 122): R=196 > G=144 > B=122 → R>G✓, R>B✓ — warm family confirmed.

---

## Cross-Environment Color Note

Miri's slipper color (#C4907A) reads correctly in all three lighting conditions:
1. **Kitchen morning (warm key):** Dusty Apricot under SUNLIT_AMBER glow — warm harmony ✓
2. **Living room lamp (OCHRE_BRICK key):** Soft warm apricot in low lamp light — warm harmony ✓
3. **Any fluorescent/cool secondary fill:** Apricot holds warm read even under blue bounce ✓

The old Deep Sage (#5A7A5A) would have read as a warm/cool conflict in all environments — a domestic character with an inexplicably cool-green footwear accent.

---

## Rule for Future Work

**Any generator drawing Grandma Miri's lower body must use `#C4907A` / (196, 144, 122) for slipper upper fill.**

Run `LTG_TOOL_palette_warmth_lint.py` before submitting any Miri generator to verify CHAR-M entries. The lint tool will catch G>R or B>R violations on all CHAR-M entries.
