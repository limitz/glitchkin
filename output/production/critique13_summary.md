# Critique 13 — Summary

**Date:** 2026-03-29
**Critics:** Daisuke Kobayashi, Priya Nair, Sven Halvorsen, Reinhardt Böhm, Nkechi Adeyemi

---

## Scores

| Critic | Asset / Area | Score |
|--------|-------------|-------|
| Daisuke | Luma expr v007 | 62 |
| Daisuke | Luma turnaround v003 | 71 |
| Daisuke | Lineup v006 | 74 |
| Daisuke | Luma color model v002 | 80 |
| Daisuke | Glitch expr v003 | 72 |
| Priya | master_palette.md | 82 |
| Priya | SF01 v004 | 84 |
| Priya | SF02 v005 | 78 |
| Priya | SF03 v005 | 76 |
| Priya | SF04 v003 | 68 |
| Priya | Color story | 87 |
| Sven | SF01 v004 | 72 |
| Sven | SF02 v005 | 68 |
| Sven | SF03 v005 | 81 |
| Sven | SF04 v003 | 52 |
| Reinhardt | Production systems overall | 64 |
| Nkechi | Pitch brief | B+ |
| Nkechi | Glitch expr v003 | B |
| Nkechi | Luma expr v007 | C+ |
| Nkechi | Byte expr v004 | B+ |
| Nkechi | SF02 v005 | C+ |
| Nkechi | Overall | B |

---

## P1 — Blockers

1. **Eye-width semantic mismatch** (Daisuke) — `h` means head-radius (104px) in v007 but head-height (382px) in turnaround v003 → ew = 22px vs 84px at 2×. A 3.8× discrepancy. The variable name was unified but the meaning was not. Fix: canonize one definition across ALL documents and generators.

2. **Broken forwarding stubs** (Reinhardt) — C29 cleanup deleted the LTG_CHAR_* originals that C28 stubs import from. At least 8 generators throw `ModuleNotFoundError` at runtime. Fix: update stubs to import from LTG_TOOL_* replacements.

3. **luma.md proportion contradiction** (Reinhardt) — luma.md still says 3.5 heads; character_sheet_standards_v001.md says 3.2. A new artist cannot resolve this. Fix: update luma.md.

4. **add_rim_light(side="right") canvas-midpoint bug** (Sven) — uses x>0.50W mask; excludes the right torso of left-of-center characters like Luma in SF01 (~x=0.35W). Fix: make the side mask character-relative, not canvas-relative.

5. **SF04 generator missing — rebuild required** (Sven) — value ceiling at 198 (FAIL), silhouette ambiguous, Byte zero monitor contribution, shadow temperatures wrong, source stubs only. Fix: rebuild generator from scratch.

6. **CHAR-L-11 cross-reference hex wrong** (Priya) — Constraint 1 was corrected to #00F0FF but the cross-reference line on the same entry still cites #00D4E8. Fix: one-line correction in master_palette.md.

7. **Luma's signature expression missing** (Nkechi) — v008 needed. The face that shows "the kid who notices what no one else sees" does not exist on the expression sheet. Six expressions are present but all are generic. This is the central pitch promise.

8. **Glitch diamond construction spec** (Daisuke) — flagged in C12, still not written. Two consecutive critiques. Fix: write glitch.md with full construction spec.

---

## P2

- Byte shadow color in lineup (#00 90B0 vs canonical #00 A8C0) — 2 cycles unresolved (Daisuke)
- Byte unguarded warmth state absent from expr sheet (Nkechi)
- SF02 Luma interiority during sprint absent (Nkechi)
- CHAR-M-11 Miri slippers (#5A7A5A Deep Sage) contradict warm-palette guarantee (Priya)
- Glitch has no spec file — generators are the only specification (Reinhardt)
- Cosmo v004 generator byte-identical to v003, outputs _v003.png filename (Reinhardt)
- SF02 characters have no magenta fill light / no cyan specular on crack-facing torso (Sven)
- SF03 face highlight direction and UV tinting unaddressed since C12 (Sven)
- 55 W004 lint warnings (missing draw refresh) unaddressed (Reinhardt)
- DRW-18 hair warmth claim visually unsupported in SF03 (Priya)
- Luma v007 body proportion computes to 3.12 heads due to neck segment (Daisuke)

---

## What Improved Since C12

- Pitch brief interior need: C→B+ (Nkechi)
- Glitch interior states (YEARNING/HOLLOW/COVETOUS): C+→B (Nkechi)
- SF01 face lighting + rim light direction: resolved (Sven)
- UV_PURPLE_DARK saturation in SF03: resolved (Priya/Sven)
- Line weights on Luma turnaround: resolved (Daisuke)
- 22 naming violations deleted: noted (Reinhardt)
- Naming conventions and character sheet standards docs: now exist (Reinhardt)
- Reinhardt: FAIL → 64 (conditional pass on framework, failing on execution)
