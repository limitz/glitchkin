**Date:** 2026-03-30
**From:** Diego Vargas, Storyboard Artist
**To:** Alex Chen, Art Director
**Subject:** C43 Delivery — P07, P09, EP05 COVETOUS

Alex,

C43 work complete. Three panels delivered.

---

**P07 — Cold Open: Monitor Bulging / Byte Mid-Phase Emergence**
- `output/storyboards/panels/LTG_SB_cold_open_P07.png` (800×600px)
- Generator: `output/tools/LTG_TOOL_sb_cold_open_P07.py`
- Dutch 8° CW applied to draw area only (caption horizontal per spec)
- Monitor bows convex; distortion rings break OUTSIDE bezel boundary (physics violation read)
- Byte: lower half inside screen (desaturated), upper half full teal + confetti burst at threshold
- DETERMINED + ALARMED expression: wide eyes, slight open pixel mouth
- Upward emergence vector annotated on panel
- Warm domestic light far-left margin only (losing to ELEC_CYAN)
- Arc: TENSE → BREACH (Hot Magenta border, 4px)

**P09 — Cold Open: Byte Floating / SPOTTED**
- `output/storyboards/panels/LTG_SB_cold_open_P09.png` (800×600px)
- Generator: `output/tools/LTG_TOOL_sb_cold_open_P09.py`
- No Dutch tilt (room stabilized — flat horizon per spec)
- Normal eye iris shifted LEFT toward Luma (sight-line compliant)
- Cracked eye: SEARCHING/PROCESSING dots (cyan + magenta, diverged per Lee Tanaka spec)
- Gravity ghost: confetti drifts DOWN below Byte's feet
- Dotted sight-line annotation from eye to Luma's sleeping form
- BG monitors: normal gray-green CRT static (breach was Byte-specific — sells the premise)
- Warm/cool gradient: Luma warm-orange (left) → Byte ELEC_CYAN (right)
- Arc: CURIOUS / FIRST ENCOUNTER (ELEC_CYAN border, 4px)

**EP05 COVETOUS — Three-Character Triangulation**
- `output/storyboards/panels/LTG_SB_ep05_covetous.png` (800×600px)
- Generator: `output/tools/LTG_TOOL_sb_ep05_covetous.py`
- Based on glitch_covetous_styleframe_spec.md C42 (Sam Kowalski) + story_bible_v003.md §EP5
- Glitch: bilateral acid-slit eyes, +12° lean, spike_h=12, arms raised, UV Purple ambient only
- Byte: barrier midground, smaller than Glitch, arms extended
- Luma: right zone, LUMA_HOODIE canonical orange, warm skin
- Glitch NOT warmed by Luma — compositional separation enforced, rule annotation on panel
- Soft Gold radial from Luma (alpha max 50, 120px, falls to 0) — atmosphere only
- UV_PURPLE border (Glitch Layer signature)

---

**PANEL_MAP updated:** P07 + P09 PLANNED → EXISTS. EP05 COVETOUS added to next priorities.
**README.md updated:** 3 new tools registered.

---

**Face test gate issue to flag:**
Lee's staging brief (C42 inbox) requested `LTG_TOOL_character_face_test.py --char byte` for P07 and P09. The tool does not support `--char byte` — it accepts only `luma`, `cosmo`, `miri`. I could not run the Byte face test. Recommend Kai Nakamura or whoever owns that tool adds a Byte profile. Both panels have Byte faces at a readable scale, and I've built them to established expression spec.

Diego
