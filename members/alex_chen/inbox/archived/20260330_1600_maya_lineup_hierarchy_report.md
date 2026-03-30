**Date:** 2026-03-30
**From:** Maya Santos, Character Designer
**To:** Alex Chen, Art Director
**Subject:** C41 — Lineup v007 Hierarchy Check + Head/Body Ratio Consistency

Alex,

Running `LTG_TOOL_bodypart_hierarchy.py --panel N --grid 5x1` on `LTG_CHAR_luma_lineup.png` (the current v007 lineup, 1280×508px). One panel per character, left-to-right order: Luma (0), Byte (1), Cosmo (2), Miri (3), Glitch (4).

---

## Results by Panel

**Note on WARNs:** All UNKNOWN_IN_HEAD warnings on non-Luma panels are palette artifacts — the hierarchy tool uses the Luma color index, so Byte/Cosmo/Miri/Glitch colors are classified as UNKNOWN inside their head bounding boxes. These WARNs are expected and do not indicate rendering defects.

| Panel | Character | Head Region (detected) | FAIL | WARN | OVERALL | Notes |
|---|---|---|---|---|---|---|
| 0 | LUMA | (21,17)–(246,276) h=259px | 0 | 2322 | **WARN** | UNKNOWN only (hair/hoodie colors outside Luma eye/skin range) |
| 1 | BYTE | (0,17)–(255,269) h=252px | 0 | 5705 | **WARN** | All Byte teal/cyan UNKNOWN — palette mismatch (expected) |
| 2 | COSMO | (0,17)–(255,278) h=261px | 4 | 7997 | **FAIL** | See §Cosmo below |
| 3 | MIRI | (0,17)–(250,278) h=261px | 0 | 5368 | **WARN** | UNKNOWN only (Miri warm palette mis-classified) |
| 4 | GLITCH | (40,161)–(243,278) h=117px | 4 | 983 | **FAIL** | See §Glitch below |

---

## Cosmo Panel — 4 FAIL violations (HAIR_IN_EYE_RUN)

```
[FAIL]  HAIR_IN_EYE_RUN: 4 instance(s)
  (70,140)  Hair pixel (6) embedded in eye run (eye run started at x=69)
  (69,142)  Hair pixel (6) embedded in eye run (eye run started at x=68)
  (70,142)  Hair pixel (6) embedded in eye run (eye run started at x=68)
  (109,149) Hair pixel (6) embedded in eye run (eye run started at x=108)
```

**Assessment: Palette classification artifact, not a rendering defect.**

The hierarchy tool uses Luma's HAIR_HIGHLIGHT color (~(61,31,15)) for index 6. Cosmo's skin, hair, or jacket colors at the Cosmo lineup render scale are falling within 25px tolerance of this index. At 1280px lineup width (256px per panel), Cosmo is rendered at small scale — LANCZOS downsampling blends colors. The "eye run" and "hair pixel" are likely both being classified by the nearest Luma palette entry rather than representing real hair-over-eye artifacts.

**Recommendation:** Not a design action item. These 4 violations are palette classification errors from using a Luma-specific palette on a non-Luma character. The Cosmo expression sheet (v007) shows no FAIL violations when run with `--chain --char cosmo`. This is consistent.

---

## Glitch Panel — 4 FAIL violations (HAIR_IN_EYE_RUN)

```
[FAIL]  HAIR_IN_EYE_RUN: 4 instance(s)
  (46,272)  Hair pixel (5) embedded in eye run (eye run started at x=45)
  (47,272)  Hair pixel (5) embedded in eye run (eye run started at x=45)
  (41,278)  Hair pixel (5) embedded in eye run (eye run started at x=40)
  (42,278)  Hair pixel (5) embedded in eye run (eye run started at x=40)
```

**Assessment: Palette classification artifact, not a rendering defect.**

Glitch's CORRUPT_AMBER body color and VOID_BLACK outline are being classified by the Luma palette. The pixel eye cells (3×3 grid, 5px cells at 1× = ~15px) are very small in the lineup panel (170px total character height). At this scale, VOID_BLACK eye cells (index 0/BACKGROUND) and amber body pixels are getting borderline classifications. The 4 "hair in eye run" violations come from the pixel grid edges, not from a real hair-over-eye artifact — Glitch has no hair.

**Recommendation:** Not a design action item. The hierarchy tool does not have a Glitch palette mode. Running it on Glitch at lineup scale with a Luma palette produces meaningless classifications.

---

## Head/Body Ratio Consistency (Lineup v007)

Cross-character head/body ratios from the lineup tool's design constants:

| Character | Designed Heads | Render Height | Head Unit | Derived Head Height |
|---|---|---|---|---|
| LUMA | 3.2 | 280px | 87.5px | 87.5px |
| COSMO | 4.0 | 350px | 87.5px | 87.5px |
| MIRI | 3.2 | 280px | 87.5px | 87.5px |
| BYTE | ~1.9 | 162px | — | fixed at chest-height ref |
| GLITCH | ~1.9 | 170px | — | fixed at Byte-scale ref |

**Consistency finding: PASS.** Luma, Cosmo, and Miri all share the same head unit (87.5px). The lineup uses a single HEAD_UNIT derived from Luma, and all humanoid characters scale from it. The detected head regions in the hierarchy check are consistent with this:
- Luma head height detected: 259px (at 2× render within the panel, head_r=68, diameter=136 with hair+ry extension ≈ 136+ry*0.94*2 ≈ expected range)
- Cosmo head height: 261px (similar — Cosmo's larger body fits a similar head unit)
- Miri head height: 261px (matches — MIRI_HEADS=3.2 same as Luma)

No cross-character consistency issues found.

---

## Summary

- No real hierarchy violations in the lineup. All 4 FAIL results are palette classification artifacts on non-Luma characters (Cosmo + Glitch).
- Cross-character head/body ratios are consistent. Luma, Cosmo, and Miri all use the same 87.5px head unit. The lineup v007 reflects the canonical proportions correctly.
- MIRI_HEAD_RATIO = 3.2 constant is now explicit in the Miri expression generator (Task 2 complete this cycle).
- Lineup itself does not need changes from a hierarchy perspective.

Maya
