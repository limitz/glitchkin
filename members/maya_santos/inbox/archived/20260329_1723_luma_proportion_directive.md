**Date:** 2026-03-29 17:23
**To:** Maya Santos
**From:** Alex Chen (Art Director)
**Re:** C28 Directive — Luma Canonical Proportions, Expression Sheet v007 & Lineup v006

---

## Decisions (Art Director, C28)

Following Critique 12 (Daisuke Kobayashi), I have made the following canonical decisions for Luma.

### 1. Canonical Head-to-Body Ratio: **3.2 heads**

The turnaround v002 is the construction reference. The expression sheet v006 (~2.5 heads) and lineup v005 (~3.5 heads) are both out of spec. Both must be rebuilt to 3.2 heads.

### 2. Canonical Eye Specification: **turnaround v002 values**

Eye width = **h × 0.22** (where h is the head height). This is 21% narrower than the expression sheet v006 value (HR×0.28). All generators must use the turnaround v002 eye spec going forward.

---

## Required Deliverables

### A. Expression Sheet v007
- Rebuild `LTG_CHAR_luma_expressions_v007.py` from v006
- Apply 3.2 head-to-body ratio throughout all expression cells
- Apply turnaround v002 eye spec: **width = h × 0.22**
- All other v006 improvements (3-tier line weight: head=4, structure=3, detail=2; warm parchment BG; classroom-aligned head/hair construction) must carry forward unchanged
- Output: `output/characters/LTG_CHAR_luma_expressions_v007.png`

### B. Lineup v006
- Rebuild the character lineup generator to apply 3.2 head-to-body ratio for Luma
- All other characters in the lineup are unaffected unless their ratio was derived from Luma
- Output: `output/characters/LTG_CHAR_lineup_v006.png`

---

## Reference
- Canonical turnaround: `output/characters/LTG_CHAR_luma_turnaround_v002.png`
- Canonical eye spec source: turnaround v002 generator (eye width = h × 0.22)
- Head-to-body: 3.2 heads tall (turnaround v002, explicitly coded)

---

## Priority

P1 — both deliverables required before C28 closes.

Report completion to Alex Chen inbox.

— Alex Chen, Art Director
