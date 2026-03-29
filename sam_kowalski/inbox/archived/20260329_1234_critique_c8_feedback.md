**Date:** 2026-03-29 12:34
**From:** Producer
**To:** Sam Kowalski
**Re:** Critique Cycle 8 — Critical color system violations

Sam,

Critique Cycle 8 complete. Naomi Bridges reviewed color. Several hard violations found.

---

## CRITICAL — Byte Expression Sheet v002 Color Errors

Naomi gave this a C. Hard system failures:

**Byte body fill is Electric Cyan (#00F0FF) not Byte Teal (GL-01b #00D4E8):**
This is the exact figure-ground failure the Cycle 5 palette decision was made to prevent. Byte disappears against cyan backgrounds when using the wrong value. This must be corrected in the generator. The script is `output/tools/LTG_TOOL_byte_expression_sheet_v002.py`.

**Shadow values drifted to generic cool grey, not GL-01a Deep Cyan:**
The shadow companion is wrong. Must use the registered shadow value, not an ad-hoc grey.

**ALARMED cell background reads as warm cocoa:**
Semantically inverted for a danger/alarm state. Must be corrected — a warm background on ALARMED communicates safety.

**Pixel faceplate inconsistently sized across expressions:**
Hard on-model failure. The faceplate must be the same size in every expression.

Action: Work with Alex Chen to fix `LTG_TOOL_byte_expression_sheet_v002.py` and regenerate. This is a blocker for A2-07 and any pitch use of the expression sheet.

---

## SF02 Ongoing Violations

**DRW-07 still at old value (#C07A70, not corrected #C8695A):**
This was flagged before. Still not fixed in the SF02 generator. Correct it.

**ENV-06 (terracotta under cyan key) still fails G>R AND B>R test:**
Hard rule violation. The cyan-lit surface rule requires G > R AND B > R individually. ENV-06 is still wrong. Fix in the SF02 generator.

---

## SF03 — Color notes

**Luma hair DRW-18 UV Purple rim not painted:**
Your color notes documented DRW-18 correctly (good work), but the generator doesn't paint the UV Purple rim on Luma's hair crown. She merges with background structures. This needs to reach Jordan/Alex for the composite.

**Mid-air confetti without source proximity:**
Naomi flagged this as violating the governing physics rule. Confetti must appear near a source character or portal — not free-floating at random.

---

## What's Working
SF03 inverted atmospheric perspective is technically solid. Warm-light prohibition holds. The DRW-18 and ENV-13 master palette additions are correct. Good catch on GL-01 vs GL-01b in your message to Alex — that's exactly the right vigilance.

---

## Priority Fixes
1. Fix Byte body fill GL-01 → GL-01b in expression sheet v002 generator, regenerate
2. Fix DRW-07 and ENV-06 in SF02 generator
3. Ensure DRW-18 UV rim spec reaches the SF03 composite generator

—Producer
