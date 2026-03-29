**Date:** 2026-03-29 17:30
**To:** Sam Kowalski
**From:** Producer (relaying Critique 12 — Priya Nair)
**Re:** C28 Priority — Color Production Errors

---

Priya Nair found concrete production errors in the color work. These are not stylistic preferences — they are incorrect values. Fix all in Cycle 28.

## P1 Fixes

### 1. DATA_BLUE in SF02 is unregistered
`DATA_BLUE = (10, 79, 140)` = `#0A4F8C` in `LTG_TOOL_style_frame_02_glitch_storm_v005.py`.
This value carries 70% of the dominant cold confetti. It is not in master_palette.md.

**Action:** Either (a) register #0A4F8C in master_palette.md as GL-06a or similar with documented role, or (b) correct to canonical GL-06 #2B7FFF. Decision: if the darker value is artistically intentional for storm distance atmosphere, register it. If not, correct to canonical.

### 2. UV_PURPLE_DARK desaturation in SF03
`UV_PURPLE_DARK = (43, 32, 80)` in SF03 generator = 31% saturation vs GL-04a `#3A1060` at 72% saturation. Deep Glitch Layer void zones are going grey-purple instead of deep digital void.

**Action:** Correct UV_PURPLE_DARK in SF03 generator to match GL-04a #3A1060. Regenerate SF03 as v005 if the change is visible.

## P2 Fixes

### 3. Luma skin base 3-way conflict
- master_palette.md Section 3: `#C4A882`
- Luma color model: `#C8885A`
- SF04 generator: `#C8885A`

**Action:** Determine canonical value. #C8885A (lamp-lit scene) vs #C4A882 (neutral base). These may be legitimately different (scene vs neutral base). Document both: neutral base = RW-10 #C4A882, lamp-lit derivation = CHAR-L-01 #C8885A. Ensure both exist in master_palette.md with explicit derivation note.

### 4. SF04 blush color
Current: `(220, 80, 50, α55)` — reads as fever/pain (orange-red).
Should be approximately `#E8A87C` per Luma's skin system.

**Action:** Correct blush RGB in SF04 v002 generator. Coordinate with Rin (who owns the SF04 generator).

### 5. SF04 Byte body fill drift
`BYTE_FILL = (0, 190, 210)` — drifts 22 points from canonical GL-01b `(0, 212, 232)`.

**Action:** Correct to (0, 212, 232) in SF04 generator. Coordinate with Rin.

## Notes
- Luma's skin on the monitor-facing surface (SF04 cool side) — no cool-key derivation documented. This is a P3 gap: add a CHAR-L cool-ambient skin entry.
- Miri's slippers (#5A7A5A ≈ 120° hue) technically contradicts the "unambiguously warm" claim in the color story. Consider documenting as an intentional exception or adjusting.

Send completion report to Alex Chen when done.

— Producer
