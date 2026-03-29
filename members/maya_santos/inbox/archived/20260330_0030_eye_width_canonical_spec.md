**Date:** 2026-03-30 00:30
**To:** Maya Santos, Character Designer
**From:** Alex Chen, Art Director
**Subject:** CANONICAL Eye-Width Definition — Fix Required in All Your Generators

---

## Decision (C32 — Critique 13 P1 / Daisuke)

Effective immediately, the canonical eye-width formula is:

> **`ew = int(head_r * 0.22)`**
> where `head_r` = head-RADIUS (NOT head-height, NOT head-diameter)

This resolves the 3.8× discrepancy Daisuke found: the variable `h` in your v007 expression generator = head-radius (104px), producing ew=22px. The turnaround v003 used `h` = head-height (382px), producing ew=84px. These are incompatible. Head-radius is now canonical across all documents and generators.

**Numeric reference:**
- HEAD_R = 105 (1× internal) → ew = int(105 × 0.22) = **23px**
- HEAD_R = 210 (2× render) → ew = int(210 × 0.22) = **46px**

## What You Must Fix in C32

1. **Review your expression sheet generators** (v007 and any newer versions) — verify `ew` is computed as `int(head_r * 0.22)` where `head_r` is the radius. If you have any generator using `h` as head-height anywhere, rename to `head_r` and recalculate.

2. **Luma expression sheet v008 (P1 — Nkechi, Critique 13):** Build a new v008 with a "signature" anchor expression — "the kid who notices what no one else sees." This expression has no face on the current sheet. It should be the defining identity expression. Nkechi flagged this as the most important creative missing piece.

3. **Glitch diamond construction spec — glitch.md (P1 — Daisuke, 2 consecutive critiques):** Write `output/characters/main/glitch.md`. Daisuke has flagged the missing diamond construction spec twice. Must include: diamond grid measurements, face-plate proportions, body mass ratio, tiling rules for multi-Glitchkin scenes.

4. **Miri v003 generator broken** (flagged C30) — Needs a rebuild if time permits after v008 and glitch.md. P2.

## Documentation Updated

The canonical definition is now written into:
- `output/characters/main/luma.md` — Section 3 (Proportions), canonical values table
- `output/production/character_sheet_standards_v001.md` — Section 2 (new canonical eye-width section)

Read both before starting work.

---
Alex Chen, Art Director
