**Date:** 2026-03-29 19:35
**To:** Maya Santos, Character Designer
**From:** Alex Chen, Art Director
**Subject:** C33 Directive — Byte Expression v005: Unguarded Warmth

---

## Context

Byte's current expression sheets (v004, 9 expressions in 3×3 grid) cover his full defensive emotional vocabulary well. One significant gap remains: there is **no expression showing Byte when his guard is fully down** — not the ACCIDENTAL AFFECTION moment (Expression 3, which he immediately suppresses), and not SECRETLY PLEASED (Expression 8, which he keeps private). This is about a moment he cannot suppress or has stopped trying to.

This is narratively significant. Byte's arc is moving from defensive self-protection to genuine connection. The Unguarded Warmth expression is the visual proof that connection has won.

---

## New Expression Spec: UNGUARDED WARMTH

**Narrative context:** Luma has done something for Byte that he didn't ask for and can't dismiss. He has looked away (he cannot look directly at her), but the expression is already on his face. He knows it. He isn't fighting it this time.

### Body language

- **Body tilt:** -4° (very slight lean toward Luma — unconscious, small)
- **Upper limbs:** both slightly forward and angled slightly upward (not reaching, not at sides). Think of it as the limbs wanting to do something and not being told what. arm_dy ≈ -5 for both (slight upward float, vs neutral 0).
- **Lower limbs:** visible, slight asymmetry — left 2px forward of right. He is turned very slightly.
- **Hover confetti:** SOFT_GOLD (#E8C95A) — 3–4 small squares, not the usual cyan/magenta. This is the only expression that uses gold confetti. Subtle signal.

### Face

- **Normal eye (viewer's right):** Star glyph (#E8C95A SOFT_GOLD) — FULL brightness, not dimmed. This is the key difference from SECRETLY PLEASED (Expression 8, which dims the star). The star is at full power because he has stopped trying to hide it.
- **Cracked eye (viewer's left):** Heart glyph (#7B2FBE UV_PURPLE, not #FF2D6B HOT_MAGENTA). The heart on the cracked/corrupted eye uses the purple emotional color — it is the "deep" version of the heart he flashes in Expression 3. The cracked eye showing a heart = he's been broken open.
- **Mouth:** Very slight upward arc — almost not there. NOT the full grin. If Expression 3 ACCIDENTAL AFFECTION has a visible heart and a body that's pulling away, this has a barely-there smile and a body that has stopped pulling away.
- **Pixel symbol context:** The combination of STAR (normal eye) + HEART (cracked eye) is unique — no other expression has this pairing. This is the tell.

### Pixel eye grid specs

**Normal eye — Star at full SOFT_GOLD:**
```
0 1 0 1 0
1 1 1 1 1
0 1 1 1 0
1 1 1 1 1
0 1 0 1 0
```
(using 5×5 grid variant per expression sheet standard)
Color 1 = SOFT_GOLD #E8C95A (full brightness — NOT the 50% of Expression 8)

**Cracked eye — Heart in UV_PURPLE:**
```
0 1 0 1 0
1 1 1 1 1
0 1 1 1 0
0 0 1 0 0
0 0 0 0 0
```
Color 1 = UV_PURPLE #7B2FBE (NOT HOT_MAGENTA — this is the emotional purple, not the alarm red)

### Panel BG

Warm cream, leaning slightly cooler than usual — somewhere between Luma's warm parchment and a neutral warm gray. He exists at the border between his cold world and her warm one.

---

## Output Spec

**Target:** `output/characters/main/LTG_CHAR_byte_expression_sheet_v005.png`
**Generator:** `output/tools/LTG_TOOL_byte_expression_sheet_v005.py`
**Grid:** 4×3 (12 slots, 10 filled — leave bottom-right 2 slots empty) OR continue with 3×3 (9 slots, use a 2-page/panel split). Your call on layout — 4×3 gives more room and is easier to extend.
**Canvas:** 1200×900 minimum (scale up if 4×3 needs more room)
**Image size rule:** ≤ 1280px in both dimensions. If 4×3 canvas exceeds 1280px width, scale with `img.thumbnail((1280, 1280), Image.LANCZOS)`.

Include the expression label: **UNGUARDED WARMTH** and a brief one-line note: *"He has stopped fighting it."*

---

## Priority

**P2** — Not blocking pitch. Ship when expression quality meets standard. Squint test must show this is distinct from ACCIDENTAL AFFECTION and SECRETLY PLEASED at thumbnail scale. Key differentiator:
- vs. ACCIDENTAL AFFECTION: body is NOT pulling away, star is not gone
- vs. SECRETLY PLEASED: star is at FULL brightness, heart is present on cracked eye, body leans slightly in

Alex Chen
Art Director
