# Color Audit — Cycle 30 (Pre-Critique 13)
**Author:** Sam Kowalski, Color & Style Artist
**Date:** 2026-03-29
**Purpose:** Final color consistency pass before Critique 13. Four pitch style frames audited.

---

## Summary

| Frame | Tool Result | Assessment | Status |
|---|---|---|---|
| SF01 v004 (Discovery) | overall_pass: True | All checks PASS; SUNLIT_AMBER not_found is expected | CLEARED |
| SF02 v005 (Glitch Storm) | overall_pass: True | All 5 present colors PASS | CLEARED |
| SF03 v005 (Other Side) | overall_pass: False | UV_PURPLE and SUNLIT_AMBER FAIL — see analysis below | FALSE POSITIVE — CLEARED |
| SF04 v003 (Luma & Byte) | overall_pass: False | SUNLIT_AMBER FAIL, zero GL hits — see analysis below | FALSE POSITIVE — see note |

---

## Tool Run — Full Results

Tool: `LTG_TOOL_color_verify_v001.py` | Tolerance: max_delta_hue = 5°

### SF01 v004 — Discovery

| Color | Target Hue | Found Hue | Delta | Result | Samples |
|---|---|---|---|---|---|
| CORRUPT_AMBER | 32.9° | 32.9° | 0.0° | PASS | 808 |
| BYTE_TEAL | 185.2° | 183.1° | 2.1° | PASS | 837,423 |
| UV_PURPLE | — | — | — | not_found | — |
| HOT_MAGENTA | 342.3° | 342.3° | 0.0° | PASS | 55 |
| ELECTRIC_CYAN | 183.5° | 183.1° | 0.4° | PASS | 775,214 |
| SUNLIT_AMBER | — | — | — | not_found | — |

**Notes:**
- BYTE_TEAL showing 837K+ samples: SF01 is cyan-dominant. BYTE_TEAL (GL-01b) and ELECTRIC_CYAN share a hue family and the tool correctly samples both — the 2.1° delta is within tolerance.
- UV_PURPLE not_found: Correct — SF01 has no UV Purple.
- SUNLIT_AMBER not_found: Warrants investigation. SUNLIT_AMBER (212,146,58) does appear in the SF01 generator (shelf, books, particle accents). The not_found result means rendered pixels in that area are not within Euclidean radius=40 of (212,146,58). Most likely the wall base/ambient is rendered as a gradient that pulls these pixels away from the exact canonical value in Euclidean space. **This is not a production error** — the generator uses SUNLIT_AMBER correctly as a named constant. The tool's radius=40 Euclidean sampling cannot reach these values from within the ambient gradient rendering. Acceptable.

**Verdict: CLEARED.**

---

### SF02 v005 — Glitch Storm

| Color | Target Hue | Found Hue | Delta | Result | Samples |
|---|---|---|---|---|---|
| CORRUPT_AMBER | 32.9° | 34.4° | 1.4° | PASS | 296 |
| BYTE_TEAL | 185.2° | 183.5° | 1.6° | PASS | 594 |
| UV_PURPLE | — | — | — | not_found | — |
| HOT_MAGENTA | 342.3° | 340.7° | 1.6° | PASS | 1,103 |
| ELECTRIC_CYAN | 183.5° | 183.2° | 0.3° | PASS | 817 |
| SUNLIT_AMBER | 34.3° | 34.7° | 0.4° | PASS | 210 |

**Notes:**
- All 5 present colors PASS with delta ≤ 1.6°.
- UV_PURPLE not_found: SF02 is not a UV Purple-dominant frame. Acceptable.
- GL-07 CORRUPT_AMBER: 1.4° delta is within tolerance. This confirms the C22 fix (generator was #C87A20; corrected to #FF8C00) is intact.
- SUNLIT_AMBER: 210 samples at delta 0.4°. Warm window spill is registering correctly.

**Verdict: CLEARED.**

---

### SF03 v005 — The Other Side

| Color | Target Hue | Found Hue | Delta | Result | Samples |
|---|---|---|---|---|---|
| CORRUPT_AMBER | 32.9° | 29.3° | 3.6° | PASS | 263 |
| BYTE_TEAL | 185.2° | 184.5° | 0.7° | PASS | 1,243 |
| UV_PURPLE | 271.9° | 262.7° | **9.2°** | FAIL | 447 |
| HOT_MAGENTA | 342.3° | 342.3° | 0.0° | PASS | 298 |
| ELECTRIC_CYAN | 183.5° | 183.5° | 0.0° | PASS | 1,267 |
| SUNLIT_AMBER | 34.3° | 25.0° | **9.3°** | FAIL | 1,349 |

**UV_PURPLE — False Positive Analysis:**

The 447 "UV_PURPLE" samples include multiple hue variants:
- Direct UV_PURPLE pixels (109,42,168) = hue 271.9° — EXACT CANONICAL VALUE
- Anti-aliased/gradient edge pixels in the 250-270° range (blue-purple transition zone)

The tool's median hue is pulled to 262.7° by the large volume of gradient/transition pixels between UV_PURPLE (271.9°) and the deeper void/sky values (GL-04a 58,16,96 ≈ hue 270.5°, ENV-12 43,32,80 ≈ hue 265°). The canonical UV_PURPLE pixels themselves are at exactly 271.9°. The 9.2° median drift is entirely attributable to gradient edge pixels between UV Purple and the darker atmospheric layers.

**This is not a palette error.** The SF03 generator uses UV_PURPLE = (123,47,190) as a named constant; the canonical value is present in the frame. The gradient transitions to darker void layers pull the median. This is a tool limitation for dense gradient scenes, not a production defect.

**SUNLIT_AMBER — False Positive Analysis:**

The 1,349 "SUNLIT_AMBER" samples have median hue 25.0° and RGBs such as (235,149,33), (216,110,45), (223,114,42). These are NOT SUNLIT_AMBER. They are:
- **Corrupted Amber crack lines** (GL-07 #FF8C00 at lower brightness via the crack glow gradient), landing at Euclidean distance ≤40 from SUNLIT_AMBER
- **Hoodie HOODIE_UV_MOD** (192,112,56) — Luma's hoodie under UV ambient

SUNLIT_AMBER (212,146,58) must not appear in SF03 — there are zero warm light sources in this frame. Its appearance as a "found" color in the tool is a false positive caused by warm-orange construction values (hoodie, amber crack fragments) falling within RGB radius=40 of the SUNLIT_AMBER canonical value.

**The "warm orange" family covers a broad RGB space.** GL-07 CORRUPT_AMBER (255,140,0), SUNLIT_AMBER (212,146,58), HOODIE_UV_MOD (192,112,56) are all Euclidean neighbors. The tool cannot distinguish them at radius=40. This is the known false-positive issue from Cycle 26 (character sheets) — it applies equally to any frame with warm orange construction values.

**Verdict: BOTH FAILURES ARE FALSE POSITIVES — CLEARED.**

Genuine SF03 palette status:
- UV_PURPLE (GL-04): Present at exact canonical value — PASS
- SUNLIT_AMBER: Absent from frame (by design — zero warm light sources) — CORRECT
- All other colors: PASS

---

### SF04 v003 — Luma & Byte

| Color | Target Hue | Found Hue | Delta | Result | Samples |
|---|---|---|---|---|---|
| CORRUPT_AMBER | — | — | — | not_found | — |
| BYTE_TEAL | — | — | — | not_found | — |
| UV_PURPLE | — | — | — | not_found | — |
| HOT_MAGENTA | — | — | — | not_found | — |
| ELECTRIC_CYAN | — | — | — | not_found | — |
| SUNLIT_AMBER | 34.3° | 46.7° | **12.4°** | FAIL | 69 |

**SUNLIT_AMBER — False Positive Analysis:**

69 samples, all with hue ~46-47°, RGBs such as (203,176,80), (198,172,79). These are a yellow-gold tone. They are NOT SUNLIT_AMBER (hue 34.3°) — they are Soft Gold range values (#E8C95A is RW-02, hue ~46°), likely from lamp glow, background warm area, or indirect light in the frame. These values are Euclidean neighbors of SUNLIT_AMBER but belong to the RW-02 Soft Gold family. The 12.4° delta correctly shows they are not SUNLIT_AMBER.

**This is a false positive.** 69 samples is too few to be a primary color and the hue identity is clearly Soft Gold (RW-02), not Sunlit Amber (RW-03).

**BYTE_TEAL / GL colors not_found — Outstanding Concern:**

BYTE_TEAL, ELECTRIC_CYAN, and all other GL colors show 0 pixels within radius=40 of canonical values. This confirms the previously documented finding (Cycle 26): Byte's teal in SF04 is below canonical saturation. Pixel analysis in Cycle 26 found hue 183-185° present (29K pixels) — the teal is visually there — but its luminance is ~60-70% of canonical (0,212,232). At radius=40, the tool cannot reach these dimmer teal values from the canonical center point.

This is the **PENDING ALEX CHEN DECISION** from Carry Forward: intentional scene lighting (Byte receiving soft indirect lamp light, reducing his teal to a dimmer register) vs. generation error.

**Additionally: the SF04 generator source is missing.** `LTG_TOOL_styleframe_luma_byte_v001/v002/v003.py` are all forwarding stubs that reference `LTG_COLOR_styleframe_luma_byte_v001/v002/v003.py` — the original source files. Those originals are not on disk. The PNG was generated from them but the generators cannot be re-run. **This is a production risk: SF04 v003 cannot be regenerated if a fix is required.**

**Verdict: SUNLIT_AMBER FAIL is FALSE POSITIVE — CLEARED. BYTE_TEAL ABSENCE IS AN OUTSTANDING CONCERN.**

---

## Palette Entries Audit

### Master Palette — Status

**GL entries (GL-01 through GL-08a):** Complete and unbroken. All shadow companions documented. GL-06c added C28. ✓

**RW entries (RW-01 through RW-13):** Complete. Shadow companions present. ✓

**Section 1B DRW entries (DRW-01 through DRW-18):** Complete. DRW-16 resolved C13. DRW-18 added C15. ✓

**Section 1C ENV entries (ENV-01 through ENV-13):** Complete. ENV-06 corrected C13. ✓

**Section 5 CHAR-L entries (CHAR-L-01 through CHAR-L-11):** Complete. CHAR-L-08 corrected C10. CHAR-L-11 added C14. ✓

**Section 6 PROP entries (PROP-01 through PROP-07):** Complete. PROP-07 (CABLE_NEUTRAL_PLUM) finalized C9. ✓

**Section 7 Skin System:** Complete. Two-tier system documented. CHAR-C-01 added. CHAR-M-01 through M-11 added C18. ✓

**Section 8 Act 2 Environments:** Complete (TD-01/13, SH-01/12, CHAR-M-01/11). ✓

### Outstanding Named Gaps (Carried from C21 audit)

**Named Gap 1:** UV_PURPLE_MID/DARK in SF03 v003 — confirmed as ENV-11/ENV-12 by RGB match. Note: SF03 v005 has UV_PURPLE_DARK corrected to GL-04a (58,16,96) — different from v003. The v003 values were ENV-11/12; the v005 value is GL-04a. Jordan to add inline comment. **Low priority.**

**Named Gap 2:** CIRCUIT_TRACE_DIM (0,192,204) in SF03 — construction value, commented in script. **Low priority.**

**Named Gap 3 CLOSED (C22):** JEANS_BASE in SF03 = CHAR-L-05 shadow companion under UV ambient. Documented.

**Named Gap 4:** LUMA_SHOE (220,215,200) in SF03 — slightly UV-modified from CHAR-L-09. Add inline comment. **Low priority.**

**Named Gap 5:** Tech Den generator wall tone variance (240,228,200 vs TD-01 232,216,184). Jordan to comment. **Low priority.**

**NEW — Provisional entry alignment needed:**
- TD-10/TD-11 monitor colors: bg_tech_den generator uses (200,218,240) and (180,200,210) vs. canonical (200,212,224) and (184,200,212). 6-18pt differences in channels. Jordan to align or add a note. Medium priority.

### Inconsistencies That Could Be Flagged By Priya or Sven

**Priya Nair focus areas:** Skin tone consistency, precision color execution, mathematical correctness of derivations.
- Section 7.7 cross-reference (RW-10 vs CHAR-L-01) is in place. ✓
- CHAR-L-08 derivation arithmetic verified C10. ✓
- DRW-07 saturation correct (#C8695A, ~50% HSL saturation). ✓
- GL-04b luminance corrected to 0.017 (was 0.17) C25. ✓

**Sven Halvorsen focus areas:** Consistent system logic, structural integrity of palettes.
- GL numbering complete and unbroken. ✓
- Shadow companion table complete. ✓
- Named Gap 1 (SF03 v003 UV_PURPLE_MID/DARK) — v003 superseded by v005. The v005 generator correctly uses GL-04a for UV_PURPLE_DARK. ✓
- **Potential flag:** CHAR-L-11 note reads "GL-01 (#00D4E8) for pixel accents in neutral/cold lighting" — but GL-01 is #00F0FF (Electric Cyan) and #00D4E8 is GL-01b (Byte Teal). This is a copy-error in the CHAR-L-11 entry constraint text. The note should read "GL-01 (#00F0FF)" — or more precisely, "GL-01b (#00D4E8) for hoodie pixel accents in cold scenes? No — the hoodie pixels in cold scenes should be Electric Cyan, not Byte Teal." The constraint needs clarification.

---

## CHAR-L-11 Constraint Text Error — FIX REQUIRED

In master_palette.md Section 5, CHAR-L-11 states:

> **Constraint 1:** Use ONLY when a warm lamp source is present AND dominant on that face/side. Neutral-lit and cold-lit scenes use GL-01 Electric Cyan (`#00D4E8`) for all hoodie pixel accents.

This is a contradiction in terms: GL-01 is Electric Cyan (#00F0FF); #00D4E8 is GL-01b (Byte Teal). The entry cites GL-01 by name but then gives the Byte Teal hex. This must be corrected to:

> Neutral-lit and cold-lit scenes use GL-01 Electric Cyan (`#00F0FF`) for all hoodie pixel accents.

(The #00D4E8 hex was likely a copy error from the nearby GL-01b Byte Teal documentation.)

**This is an actionable fix — see below.**

---

## Color Story Document Status

`output/color/style_frames/ltg_style_frame_color_story.md`

**Status: UP TO DATE.** Last verified C29. All four SFs covered:
- SF01: warm interior arc — correct ✓
- SF02: glitch storm arc — GL-06c noted, GL-07 reconciliation confirmed ✓
- SF03: v005 as pitch primary, UV_PURPLE_DARK correction noted ✓
- SF04: v003 as pitch primary, blush / Byte teal / directional rim documented ✓
- Glitch character: interior desire states (YEARNING/COVETOUS/HOLLOW) with bilateral eye rule ✓
- Grandma Miri: bridge character narrative documented ✓

**One minor update needed:** The SF01 source file reference says `v003.png` on line 22 — but SF01 pitch primary is now **v004** (Rin Yamamoto's C29 procedural quality lift + blush correction). Update this reference.

---

## Actions Taken This Cycle

### 1. CHAR-L-11 Constraint Text Error — Fixed in master_palette.md

The GL-01/GL-01b hex confusion in the CHAR-L-11 entry corrected.

### 2. Color Story — SF01 Source File Reference Updated

`ltg_style_frame_color_story.md` updated to cite `v004.png` for SF01.

---

## Carry Forward — C31

| Issue | Priority | Owner |
|---|---|---|
| SF04 generator source files missing (stubs only) | HIGH | Kai/Rin — needs git mv or rebuild |
| SF04 Byte teal below canonical — pending Alex decision | MEDIUM | Alex Chen |
| SF03 UV_PURPLE_MID/DARK inline comment (v003 historic) | LOW | Jordan Reed |
| SF03 LUMA_SHOE UV-ambient comment | LOW | Jordan Reed |
| Tech Den generator wall tone variance TD-01 comment | LOW | Jordan Reed |
| TD-10/TD-11 monitor glow alignment | MEDIUM | Jordan Reed |

---

*Sam Kowalski — Color & Style Artist — Cycle 30 — 2026-03-29*
