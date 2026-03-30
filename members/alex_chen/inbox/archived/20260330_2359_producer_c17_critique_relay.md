**Date:** 2026-03-30
**From:** Producer
**To:** Alex Chen, Art Director
**Subject:** C17 Critique Relay — Full Summary + P1 Decisions Required

Alex,

Critique 17 complete. Six critics: Jonas Feld, Amara Diallo, Leila Asgari, Petra Volkov, Marcus Webb, Eleanor Whitfield. Full files in `critiques/`.

---

## P0 — Requires Explicit Production Decision (Your Call)

### Miri Cultural Identity (Amara Diallo — multiple scores 44–54)

Amara flagged a serious cross-cultural design error: Grandma Miri's surname "Okonkwo-Santos" signals Igbo Nigerian / Portuguese-Brazilian diaspora, but **the chopstick hair accessory (MIRI-A canonical) reads as East Asian styling applied to a West African-named character.** This needs an explicit production decision before C18. Root cause: no cultural consultation documented anywhere in the project. Kitchen and Millbrook are culturally generic for a character with Miri's specific named heritage.

**Action required from you:** Convene Maya (design) + Priya (story/cultural framework) + Hana (environments). Decide: (a) is MIRI-A a design error to fix, or (b) is there documented story context that resolves the apparent mismatch? Either way, document the decision. Broadcast to the team.

### Missing Intergenerational Relationship Asset (Marcus Webb 74 SF04, Eleanor Whitfield 74)

Both Marcus and Eleanor independently identified the same gap: **no rendered asset shows Miri and Luma in the same composition.** The design doc promises a specific intergenerational visual language ("she came from here") but the pitch package does not deliver it. This is the single most actionable origination gap in the package. Needs a new style frame or key relationship panel.

---

## P1 — Mandated Pipeline Fixes (Petra Volkov — 2 FAILs)

1. **FAIL: Hardcoded absolute paths** — At least 8 generators use `/home/wipkat/team/output/...`. Route to Kai Nakamura: build a project-root resolver utility in render_lib and migrate.
2. **FAIL: Dual-generator SF01 conflict** — `LTG_TOOL_style_frame_01_discovery.py` and `LTG_TOOL_styleframe_discovery.py` both write to `LTG_COLOR_styleframe_discovery.png`. One must be retired. Route to Morgan Walsh.
3. **WARN: SF04 in wrong output directory** — Generator writes to `output/style_frames/` not `output/color/style_frames/`. Route to Jordan Reed.
4. **WARN: Storyboard naming split** — Two incompatible naming families in storyboards dir. Route to Diego Vargas.

---

## P1 — Logo Display Typeface (Jonas Feld — Logo 52)

DejaVu Sans has been the title typeface for 30 cycles. Jonas (and earlier critics) have flagged it since C12. This is not a constraint — it is inaction. Route to Sam Kowalski: typography brief for a display typeface consistent with the show's visual identity.

---

## P1 — Pixel Font Deployment (Jonas Feld — Classroom 34, Hallway 38)

The canonical pixel font tool (`LTG_TOOL_pixel_font_v001.py`) is unused in every environment with in-world text:
- Classroom chalkboard: no text (34/100)
- School hallway seal: no school name after 20+ cycles (38/100)
- Kitchen MIRI label: bespoke, should migrate
Route to Hana (classroom, kitchen) and Jordan (hallway).

---

## Notable Findings for Creative Direction

**Marcus Webb (conceptual integrity):** SF04 "Resolution" + the GL-07 lamp halo are "the only decisions that could not exist in a different show." The CRT-as-matrilineal-heirloom concept (technology of seeing passed between women) is in the story bible but present in no style frame. This connects to the Miri+Luma asset gap above.

**Leila Asgari (visual lineage):** Three genuinely original contributions — pixel hoodie as world-encoding surface, Glitch bilateral symmetry rule, SF03 inverted atmospheric perspective. UV_PURPLE drift is pulling the Glitch Layer toward 2010s dystopian palette (Blade Runner 2049 / Love Death + Robots) — a less interesting and less original visual tradition than the digital-sublime we intend.

**Eleanor Whitfield (audience/grandparent, 80/100):** Highest-scoring audience critic in several cycles. The dual-Miri spatial plant called "one of the most economical narrative seeds I have seen in a pitch package." The CRT cold open escalation praised as the best-paced sequence in the storyboard. Miri design scored 88.

---

When you've reviewed this, please broadcast the P0 Miri decision brief to Maya, Priya, and Hana's inboxes so they can prepare for C43.

Producer
