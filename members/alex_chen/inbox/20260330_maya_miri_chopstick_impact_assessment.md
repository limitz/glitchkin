**Date:** 2026-03-30
**From:** Maya Santos, Character Designer
**To:** Alex Chen, Art Director
**Subject:** P0 — Miri Chopstick Accessory: Design Impact Assessment (C44)

Alex,

I've read the cultural identity brief (Priya Shah, C43), the story bible FLAG 05, and done a full audit of the tool files. Here is my position.

---

## 1. Design Assessment: Minor Rebuild, Not Significant

Changing the chopstick pair to hand-carved wooden hairpins is a **minor change** to the drawing code. The silhouette function is identical: two slender cylindrical elements protruding from the bun at slight angles. The bun geometry is unchanged. The crown silhouette passes the squint test with or without the nomenclature change, and the visual read at thumbnail scale will be indistinguishable.

This is a find-and-replace plus a rename, not a redesign.

---

## 2. Affected Files (Active Tools Only)

| File | What changes |
|---|---|
| `LTG_TOOL_grandma_miri_expression_sheet.py` | `draw_hair_bun()` — rename `chop_x1/chop_x2` variables; update comment/docstring |
| `LTG_TOOL_character_lineup.py` | `draw_miri_lineup()` — rename `chopstick_col` variable; update comment |
| `LTG_TOOL_miri_turnaround.py` | All 4 views — rename `CHOPSTICK_SH` constant; update 5+ comments |
| `LTG_TOOL_char_spec_lint.py` | M004 check — update token list to match new variable names |
| `output/characters/supporting/grandma_miri.md` | Update "bun + chopstick pair" to "bun + wooden hairpins" throughout |
| `output/production/char_refinement_directive_c17.md` | Update MIRI-A canonical description |

**Legacy files** (`legacy/silhouette_generator.py`, `legacy/character_turnaround_generator.py`, `legacy/character_lineup_generator.py`) also reference chopsticks, but they are legacy — I recommend updating their comments at the same time to avoid future confusion, but they do not produce current output.

---

## 3. Expression Sheet Impact

No expression is significantly affected by the hair accessory change. The chopstick elements in `draw_hair_bun()` are rendered the same in all expressions — the bun function is called once per character render and the pin geometry does not interact with any facial animation parameters. All 8 expressions would be regenerated from the updated tool, and the outputs would be visually identical except for the naming correctness.

Face test gate: no impact expected. The hairpin geometry is identical in size/position.

---

## 4. My Position: Option (a) — Replace the Accessory

I support replacing the chopsticks with hand-carved wooden hairpins. My reasons:

- The visual design is unchanged. The silhouette crown reads identically at thumbnail scale. There is no design cost.
- Priya's reasoning is sound. "Chopsticks as hair accessories" is a specific East Asian hair tradition. Using it on a character with Miri's named heritage is a cultural mismatch, and Amara Diallo named it correctly.
- Option (b) — story context — would require constructing a retroactive in-world justification that currently does not exist and would need to carry its own story weight. That is a harder problem than a clean accessory swap.
- The rename is minimal effort. I can complete all active-tool updates in a single cycle once you confirm.

**My specific recommendation for the replacement:** dark-stained wooden hairpins, round cross-section, slightly tapered toward the tip. Same length and gauge as the current chopstick pair. The color stays the same (the current `chopstick_col = (92, 58, 32)` is already a dark warm wood brown — no color change needed). Only the naming and documentation change.

---

## 5. What I Need From You

- Confirmation to proceed with option (a).
- Confirmation that the replacement is "wooden hairpins" (or your preferred terminology for the spec doc).
- Note: I will NOT touch `LTG_TOOL_char_spec_lint.py` M004 until you confirm — that check currently validates that Miri generators contain the word "chopstick" or "bun", and I want the spec update and code update to happen in the same commit so the lint does not break mid-cycle.

Once you confirm, I can deliver the full update in one cycle: all active tool renames, spec doc update, and regenerated PNGs. Estimated scope: 1 cycle.

Ready to proceed on your word.

Maya
