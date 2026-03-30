**Date:** 2026-03-30
**From:** Jordan Reed, Style Frame Art Specialist
**To:** Alex Chen, Art Director
**Subject:** C45 SF04 Lamp Halo + CRT Fringe — COMPLETE

Alex,

Both C45 changes delivered. `LTG_COLOR_styleframe_sf04.png` regenerated at output/color/style_frames/.

---

## Changes Made

### 1. Lamp Halo — Expanded Radius + Raised Alpha Ceiling

- Loop extended: 20 steps → 24 steps (wider falloff)
- Horizontal radius: `sx(260)` → `sx(340)` (+31%)
- Vertical radius: `sy(180)` → `sy(240)` (+33%)
- Alpha ceiling: `int(55 * t * t)` → `int(88 * t * t)` (peak ~35% vs ~22%)
- Radial falloff factor adjusted (`0.5` → `0.45`) to keep outer edge soft

The halo now blooms onto the ceiling above the fixture and clips down toward the top of the fridge in frame. It reads as a wrongness — warm where warm shouldn't need to be that strong.

### 2. CRT Doorway — CORRUPT_AMBER Contamination Fringe

- A thin horizontal band (`sp(6)` tall) placed at the lower edge of the CRT glow ellipse
- Color: LAMP_AMBER / GL-07 / #FF8C00
- Max alpha: 38 (≈15%) — fades downward across the band
- Reads as "the static has a slightly wrong warmth" at the transition zone between CRT glow and doorway dark

The fringe is not a decorative detail — it sits exactly where the cool cyan glow meets the dark opening, so the amber reads as contamination, not light source.

---

## QA Results

**render_qa:**
- Warm/cool separation: **13.1** (PASS ≥12.0) ✓
- Value range: min=12 / max=252 (PASS) ✓
- Silhouette: distinct ✓
- Line weight outliers: 3 (WARN — pre-existing)
- Color fidelity: WARN (pre-existing alpha-compositing issue — same as prior cycles)
- **GRADE: WARN** (consistent with prior baseline — no new FAILs)

**color_verify:**
- SUNLIT_AMBER: delta=1.0° **PASS** ✓
- All 6 canonical colors: PASS / not_found (CORRUPT_AMBER / fringe color not tracked as canonical — correct)

Face test gate: head_r=42px at pitch scale — above sprint threshold. Not triggered.

---

Inbox message archived. Ready for next assignment.

Jordan
