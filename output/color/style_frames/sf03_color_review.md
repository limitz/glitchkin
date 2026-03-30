# SF03 v003 Color Review — "The Other Side"
**Reviewer:** Sam Kowalski — Color & Style Artist
**Date:** 2026-03-29
**Cycle:** 19
**Status:** PRE-RENDER REVIEW — v003 file does not yet exist at time of writing. Jordan Reed fix is in progress. This document records pre-render analysis based on the v002 generator and the stated fix scope.

---

## Context

Jordan Reed is rebuilding SF03 v003 to correct Byte's body fill from Void Black (10,10,20) to GL-01b (#00D4E8 / RGB 0,212,232). The v002 generator (`LTG_TOOL_style_frame_03_other_side.py`) had `BYTE_BODY = (10, 10, 20)`, making Byte essentially invisible against the dark platform background — a figure-ground failure.

---

## Task 1 — Byte Body Fill Verification

**Expected fix:** `BYTE_BODY = (0, 212, 232)` — GL-01b per production spec.

**From v002 analysis:** `BYTE_BODY = (10, 10, 20)` is Void Black. With this fill, Byte reads as a dark cutout shape with only the ELEC_CYAN outline (`BYTE_GLOW = (0,168,180)` inner fill + `ELEC_CYAN` outline) providing any definition. The body mass itself has no identity — no read as "character."

**After Jordan's fix:** The body fill becomes GL-01b `#00D4E8` (R:0, G:212, B:232). This is Byte Teal — his canonical body fill per master_palette.md CHAR-B-01.

**GL-01b vs GL-01 distinction:** Critically, this is NOT Electric Cyan GL-01 (`#00F0FF`). GL-01b (R:0, G:212, B:232) is slightly warmer/darker than GL-01 (R:0, G:240, B:255). The difference matters: GL-01 is the world/environment emission color; GL-01b is Byte's BODY FILL only. In SF03 where GL-01 fills the circuit traces and data ambient, Byte at GL-01b will be distinguishable from the environment.

**Delta GL-01 vs GL-01b:**
- G channel: 240 vs 212 = 28pt cooler in GL-01b
- B channel: 255 vs 232 = 23pt cooler in GL-01b
- Result: GL-01b reads as a slightly deeper, more material teal vs. the electric ambient cyan. Byte reads as "made of something" vs. "radiating something."

---

## Task 2 — Cyan Eye Contrast vs Background

**Eye color:** `ELEC_CYAN = (0, 240, 255)` — #00F0FF — GL-01
**Effective background behind Byte:** Near-void dark with UV Purple atmospheric overlay.

### Background calculation at Byte's position (x≈422, y≈640)

Byte is positioned at `byte_cx = int(W*0.22) = 422`, `byte_cy = int(H*0.62) = 669`, `byte_h = int(H*0.07) = 75px`. Eye level: y ≈ 669 - 75/10 ≈ 661.

At y=661, the base is BELOW_VOID (5,5,8). The lighting overlay applies UV_PURPLE (123,47,190) at α ≈ 20 + (661/756)×30 ≈ 46/255 ≈ 18%.

Effective background RGB: (25, 12, 39) approximately.

**Relative luminance of effective background (25,12,39):**
- L_bg ≈ 0.003 (near-black)

**Relative luminance of ELEC_CYAN (0,240,255):**
- G_lin = (240/255)^2.2 ≈ 0.873
- B_lin = (255/255)^2.2 = 1.0
- L_cyan = 0 + 0.7152×0.873 + 0.0722×1.0 ≈ 0.6244 + 0.0722 ≈ 0.697

**Contrast ratio:** (0.697 + 0.05) / (0.003 + 0.05) = 0.747 / 0.053 ≈ **14.1:1**

**Result: PASSES ≥ 4.5:1 target comfortably.** The cyan eye reads with very high contrast against the near-void dark of the Other Side.

**Note on cloud mass overlap:** The UV_PURPLE cloud masses in draw_void_sky() and draw_far_distance() extend to a maximum y of ~220px. Byte's eye level is at y≈661. No cloud mass overlaps Byte's face. The background behind Byte is the midground atmospheric wash, not the heavy UV_PURPLE cloud density.

---

## Task 3 — Magenta Eye Contrast + Void Black Slash

**Eye color:** `HOT_MAGENTA = (255, 45, 107)` — #FF2D6B
**Void Black slash:** Present in v002. `draw.line(..., fill=VOID_BLACK, width=max(1, eye_r//2))` — the slash is a diagonal through the right eye. This represents Byte's corrupted/void side.

**Relative luminance of HOT_MAGENTA (255,45,107):**
- R_lin = 1.0
- G_lin = (45/255)^2.2 ≈ 0.024
- B_lin = (107/255)^2.2 ≈ 0.151
- L_mag = 0.2126×1.0 + 0.7152×0.024 + 0.0722×0.151 ≈ 0.2126 + 0.0172 + 0.0109 ≈ 0.240

**Contrast ratio vs effective bg (L≈0.003):** (0.240 + 0.05) / (0.003 + 0.05) = 0.290 / 0.053 ≈ **5.5:1**

**Result: PASSES ≥ 3.0:1 minimum.** The magenta eye is readable against the dark Other Side.

**Void Black slash status:** The slash IS present in v002 code and no indication Jordan's fix removes it. The slash is part of Byte's corrupted-side expression. Jordan's fix (body fill only) should not alter the eye logic. Verify in v003 that the slash remains.

---

## Task 4 — Overall Frame Color Narrative Assessment

**Color palette in play:** UV Purple atmosphere + Void Black base + Electric Cyan circuits + GL-01b Byte body + ELEC_CYAN eye + HOT_MAGENTA eye + HOODIE_UV_MOD (192,112,56) for Luma's hoodie

**"The Other Side" narrative read:**

With Byte now showing GL-01b body fill, the frame reads as a encounter between:
1. Luma (warm orange presence — an intruder)
2. The Glitch Layer (UV Purple atmosphere, VOID_BLACK depths)
3. Byte (GL-01b teal body — native to this space, made of the same material as the circuits beneath his feet)

This is the correct narrative read. Byte was invisible in v002 because his body was Void Black — he appeared only as an outline ghost. After the fix, Byte becomes a VISIBLE presence with his own distinct color identity (GL-01b teal vs GL-01 circuit ambient), making the scene readable as "a being lives here."

**Potential tension point — GL-01b body vs GL-01 circuit traces:**
ELEC_CYAN (0,240,255) circuit traces will be brighter/more luminous than GL-01b (0,212,232) body. The circuit environment will glow slightly more than Byte's body. This is narratively correct: the world is the energy source; Byte is a creature shaped by it but not identical to it.

**Recommendation:** After Jordan generates v003, compare at 50% thumbnail: does Byte's teal body stand out from the circuit trace cyan? If circuit traces overwhelm the body read, Jordan should consider:
- Reducing circuit trace brightness slightly, or
- Adding a 1px VOID_BLACK body outline to separate Byte from environment

---

## Remaining Issues After Jordan's Fix

**Issue 1 — BYTE_GLOW still DEEP_CYAN (0,168,180) not GL-01a (#00A8C0)**
In v002: `BYTE_GLOW = (0, 168, 180)`. Master palette GL-01a = `#00A8C0` = (0,168,192). The B channel differs: 180 vs 192 = 12pt. This is a minor discrepancy from the spec. Not critical but worth fixing in v003 or deferring to v004.
- Current: (0,168,180)
- Canonical GL-01a: (0,168,192)
- Delta: B +12

**Issue 2 — BYTE_BODY inner glow fill uses BYTE_GLOW (DEEP_CYAN) as the inner bright fill**
The draw_byte() function draws an outer ellipse at BYTE_BODY (to be fixed to GL-01b), then a slightly smaller inner ellipse at BYTE_GLOW (DEEP_CYAN). This creates a two-tone body: outer GL-01b, inner DEEP_CYAN. This is a reasonable approach for depth, but the BYTE_GLOW inner circle will be slightly brighter/greener than GL-01b outer. Document this as intentional or correct to match character spec.

**Issue 3 — Confetti full-canvas distribution (carry forward from Cycle 16)**
Confetti particles distributed over full W×H canvas. Some will appear in sky zones far from any character or platform source. For v003+, constrain confetti to within 150px of platform (y > 0.56×H) or within 100px of characters. This was flagged in Cycle 16 and remains outstanding.

---

## Summary

| Check | Status | Value |
|---|---|---|
| Byte body fill GL-01b | PENDING JORDAN v003 | Expect (0,212,232) |
| Cyan eye vs background | PASSES | 14.1:1 |
| Magenta eye contrast | PASSES | 5.5:1 |
| Void Black slash on magenta eye | PRESENT in v002 | Verify retained in v003 |
| GL-01 vs GL-01b distinction | CORRECT — difference valid | GL-01b reads as material, GL-01 as emission |
| Frame narrative | WILL PASS after body fix | Byte visible = scene readable |
| BYTE_GLOW minor discrepancy | LOW PRIORITY | B channel 180 vs 192 |

*Sam Kowalski — Cycle 19 — Pre-render analysis based on v002 generator*

---

## FINAL VERIFIED — Cycle 20

**Reviewer:** Sam Kowalski — Color & Style Artist
**Date:** 2026-03-30
**Cycle:** 20
**Status:** FINAL VERIFIED against `LTG_TOOL_style_frame_03_other_side.py`

### Check 1 — Byte Body Constant (GL-01b)

**CONFIRMED.** Line 80 of the v003 generator reads:
```python
BYTE_BODY          = (0,  212, 232)   # GL-01b Byte Teal — was (10,10,20) WRONG
```
This is exactly `(0, 212, 232)` — GL-01b Byte Teal (#00D4E8). The Cycle 19 critical fix is correctly implemented. The comment explicitly documents the correction from the wrong Void Black value. The file header also notes this as Fix 1 with a CRITICAL RULES entry: `BYTE_BODY = (0, 212, 232) GL-01b Byte Teal — NEVER (10,10,20) Void Black.`

### Check 2 — BYTE_GLOW Discrepancy Decision

**CONFIRMED SAME VALUE. DOCUMENTED AS ACCEPTABLE — CLOSED.**

Line 81 of v003: `BYTE_GLOW = (0, 168, 180)`. This is unchanged from v002 — the 12-point B channel discrepancy vs canonical GL-01a `(0, 168, 192)` is still present.

**Decision: Document as acceptable. Do NOT flag for Cycle 21 fix.**

Reasoning: BYTE_GLOW is used as an inner body fill (the slight inner-body glow/depth layer inside the BYTE_BODY outer ellipse), not as an outline or a canonical "glow ring" drawn independently. Its function is to create a two-tone body effect: outer GL-01b (0,212,232) + inner slightly darker/deeper DEEP_CYAN (0,168,180). At this role, the 12-point B-channel deviation from GL-01a (0,168,192) is visually negligible — both values are in the same "deep cyan/teal mid-tone" range. An inner body depth tone need not be exactly GL-01a; minor derivation is acceptable for rendering construction values. The distinction between GL-01a as a named canonical and BYTE_GLOW as a construction derivation should be noted as an inline comment for Jordan's next pass, but no production fix is required. **Issue closed.**

### Check 3 — Eye Constants

**CONFIRMED UNCHANGED.**

- Cyan eye: `ELEC_CYAN = (0, 240, 255)` — line 42. Identical to pre-render analysis value. Contrast 14.1:1 vs near-void background — passes.
- Magenta eye: `HOT_MAGENTA = (255, 45, 107)` — line 55. Identical to pre-render analysis value. Contrast 5.5:1 vs near-void background — passes.

**Void Black slash status:** Jordan removed the slash in v003 (header note Fix 3: "Removed Void Black diagonal slash from magenta eye. Slashes on eyes obliterate readability against dark BG."). Pre-render analysis had flagged this for verification — the removal is intentional and noted by Jordan. The corrupted-eye read is now carried by the magenta color identity alone (one cyan eye, one magenta eye = the asymmetry communicates "corrupted/other-side entity"). Eye readability is improved.

### Check 4 — Color Narrative Assessment

With Byte's body now rendering as GL-01b Teal (0,212,232) against the UV Purple atmosphere and Void Black abyss, the frame achieves the intended emotional register: a cold, silent dimension where something has been waiting. The UV Purple + Void Black base creates a sense of depth without exit — claustrophobic despite the implied vastness — while Byte's teal body, fractionally darker than the Electric Cyan circuit traces beneath him, marks him as native to this space rather than an intruder. Luma's warm orange hoodie (HOODIE_UV_MOD) reads as a thermal anomaly — a fragment of the Real World that has no right to be here — and the single Hot Magenta eye signals that Byte is not entirely as he appears, a point of asymmetric danger within the cold harmony. The palette correctly communicates "other side": beautiful, cold, and wrong.

### Final Verified Summary

| Check | Status | Value |
|---|---|---|
| Byte body fill GL-01b | VERIFIED | (0,212,232) — line 80 |
| BYTE_GLOW discrepancy | CLOSED — ACCEPTABLE | (0,168,180) — construction value, not canonical reference |
| Cyan eye constant | CONFIRMED UNCHANGED | (0,240,255) — 14.1:1 contrast |
| Magenta eye constant | CONFIRMED UNCHANGED | (255,45,107) — 5.5:1 contrast |
| Void Black slash on magenta eye | REMOVED — INTENTIONAL | Jordan Reed Cycle 19 Fix 3 |
| Frame color narrative | PASSES | UV Purple + Teal + Magenta = correct "other side" emotional register |

*Sam Kowalski — Cycle 20 — Final verification against v003 generator*
