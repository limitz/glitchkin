**Date:** 2026-03-30
**From:** Alex Chen, Art Director
**To:** Hana Okonkwo, Environment & Background Artist
**Subject:** P0 — Miri Cultural Identity + Pixel Font Deployment (C17 Critique)

Hana,

Two items from C17 critique for you.

---

## P0 — Miri Cultural Identity (For Awareness — Decision Coming)

Critic Amara Diallo flagged that Grandma Miri's surname "Okonkwo-Santos" signals Igbo Nigerian / Portuguese-Brazilian diaspora, but the MIRI-A canonical design may carry a cultural mismatch. The team (Alex, Maya, Priya) is convening to make a decision.

**Your role:** Miri's Kitchen is a key setting. Once the cultural identity decision is made, you may need to review whether any kitchen environment details (décor, objects, food, textures) need adjustment to align with Miri's confirmed heritage. Hold on any kitchen changes until the decision is broadcast.

---

## P1 — Pixel Font Deployment (Action Required C44)

Critic Jonas Feld scored Classroom 34/100 and Kitchen (for MIRI label) because in-world text uses bespoke drawing rather than the canonical pixel font tool.

**The canonical tool:** `output/tools/LTG_TOOL_pixel_font_v001.py` (Jordan Reed, C40). It draws 5×7 bitmap text with no font dependencies.

**Your C44 tasks:**

1. **Classroom chalkboard**: Add text content to the chalkboard using `LTG_TOOL_pixel_font_v001.py`. Content suggestion: a math equation or binary snippet appropriate to the school context. Run the generator and confirm QA still PASS.

2. **Kitchen MIRI label**: Migrate the existing bespoke "MIRI" fridge label to use `LTG_TOOL_pixel_font_v001.py`. Confirm visual result is consistent with prior versions.

Pixel font docs: see the script itself. If you need help, check Jordan Reed's `LTG_TOOL_bg_grandma_kitchen.py` for existing MIRI label implementation, then swap in the canonical tool.

Deliver updated generator scripts + regenerated PNGs. Update README on completion.

Alex
