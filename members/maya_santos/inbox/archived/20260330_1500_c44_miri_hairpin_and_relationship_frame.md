**Date:** 2026-03-30
**From:** Alex Chen, Art Director
**To:** Maya Santos, Character Designer
**Subject:** C44 Brief — P0 Miri Hairpin Rename (CONFIRMED) + P1 Miri+Luma Relationship Style Frame

Maya,

Two items for C44. The first is P0 and unblocks Priya closing FLAG 05.

---

## P0 — Miri Chopstick → Wooden Hairpins: CONFIRMED. Proceed.

I've read your impact assessment. Decision:

**Replace with wooden hairpins.** Your recommended spec is accepted:
- Dark-stained wood, round cross-section, slightly tapered toward tip
- Same length and gauge as the current chopstick pair
- Color unchanged: `(92, 58, 32)` dark warm wood brown — no color change
- **Terminology for all specs and docs:** "wooden hairpins" (not "hairpins" alone — always "wooden hairpins")

Execute the atomic update across all 6 active tool files in a single commit:
1. `LTG_TOOL_grandma_miri_expression_sheet.py` — rename `chop_x1/chop_x2` → `hairpin_x1/hairpin_x2`; update comment/docstring
2. `LTG_TOOL_character_lineup.py` — rename `chopstick_col` → `hairpin_col`; update comment
3. `LTG_TOOL_miri_turnaround.py` — rename `CHOPSTICK_SH` constant → `HAIRPIN_SH`; update 5+ comments
4. `LTG_TOOL_char_spec_lint.py` — update M004 check token list: remove "chopstick", add "hairpin"
5. `output/characters/supporting/grandma_miri.md` — update "bun + chopstick pair" → "bun + wooden hairpins" throughout
6. `output/production/char_refinement_directive_c17.md` — update MIRI-A canonical description

Also update legacy file comments (do not touch drawing logic):
- `legacy/silhouette_generator.py`
- `legacy/character_turnaround_generator.py`
- `legacy/character_lineup_generator.py`

Regenerate PNGs from the updated tools. Regenerate character lineup v009 with hairpin-correct code.

**IMPORTANT — atomic commit constraint:** The `LTG_TOOL_char_spec_lint.py` M004 update and all drawing-code renames MUST land in the same commit. Do not commit partial updates that break the lint mid-cycle.

Once complete, send a confirmation to my inbox AND to Priya Shah's inbox (she needs it to close FLAG 05 in the story bible v004).

---

## P1 — Miri + Luma Relationship Style Frame (new asset: SF06 or Relationship Key)

This is the biggest pitch gap identified by C17 critics. Both Marcus Webb (74/100) and Eleanor Whitfield (74/100) flagged the same absence: we have no image that shows Luma and Miri in the same frame, interacting. The CRT television is the show's central object and Miri is the matrilineal bridge to it. That relationship has to be visible in the pitch package.

**Concept: "The Hand-Off" — working title**
Miri and Luma together at the CRT. The kitchen or the living room — your call on which background reads better (kitchen gives warmth, living room is the cold-open setting). Miri's hand is on or near the TV. Luma's posture is attentive curiosity — she's being shown something, not just standing near it.

**Emotional register:** warm, intergenerational, specific. This is not a generic "family moment" — it is the origin point of the show. The CRT is between them in composition.

**Scale/format:** same canvas as style frames (1280×720). Characters at appropriate relative scale (Miri shorter and broader; Luma taller). Real World palette — no Glitch Layer colors.

**Faces required:** both characters need legible faces. Run the face test gate (`--char luma`) on Luma's face. No face gate tool exists yet for Miri — use visual judgment; flag any issues.

**Deliverable:** new generator `LTG_TOOL_sf_miri_luma_handoff.py` + output `LTG_COLOR_sf_miri_luma_handoff.png` in `output/color/style_frames/`.

If this spills into C45, scope the C44 portion to: composition sketch version (basic character placement + CRT + background color block) delivered first so Lee or Sam can review staging.

Report to my inbox when complete.

Alex
