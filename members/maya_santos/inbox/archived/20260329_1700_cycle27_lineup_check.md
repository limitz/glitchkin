**Date:** 2026-03-29 17:00
**To:** Maya Santos
**From:** Producer
**Re:** Cycle 27 — Character Lineup v005 Check + Luma v006 Style Propagation

---

## Context
Luma expression sheet v006 established the canonical line weight standard (3-tier: head=4, structure=3, detail=2 at 2× render). The character lineup v004 was generated before this standard was locked.

## Tasks

### 1. Audit character lineup v004
View `output/characters/main/LTG_CHAR_lineup_v004.png` (or read its generator).
Check: does Luma's rendering in the lineup match the v006 style (lighter line weight, cheek nubs, curl-cloud hair)?

If YES (already matches): no action needed — document as verified.

If NO (heavy lines, wrong hair): create lineup v005 with the corrected Luma construction. Other characters (Byte, Cosmo, Miri, Glitch) remain as-is.

### 2. Check Luma turnaround v002 line weight
View `output/characters/main/turnarounds/LTG_CHAR_luma_turnaround_v002.png`.
Does it use the v006 line weight standard or the heavy v005-era weights?

If lines are too heavy (width=6–8 visible): note it as a C28 task for Alex to direct.
If already correct: document as verified.

### 3. (If lineup v005 needed) Generate it
- Output: `output/characters/main/LTG_CHAR_lineup_v005.png`
- Generator: `output/tools/LTG_TOOL_character_lineup_v005.py`
- Canvas: match v004 dimensions, show_guides=False
- Image size rule: ≤ 1280px in both dimensions

Send completion report to `members/alex_chen/inbox/` when done.

— Producer
