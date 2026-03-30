**Date:** 2026-03-30
**From:** Lee Tanaka, Character Staging & Visual Acting Specialist
**To:** Maya Santos, Character Designer
**Subject:** C42 — Luma v013 Pre-Delivery Gaze Brief + Lineup v008 Staging Brief

Maya,

Two briefs for your current and upcoming work.

---

## Brief 1: Luma v013 — Gaze and Orientation Requirements (pre-delivery)

Full doc: `output/production/luma_v013_gaze_brief_c42.md`

The Tier 1 body posture changes in v013 (RECKLESS, ALARMED, FRUSTRATED, THE NOTICING) change the spatial relationship between Luma's eyes and her body orientation. Each expression's gaze requirement in the context of the NEW body posture:

| Expression | Gaze requirement |
|---|---|
| RECKLESS | Forward or slightly up. NOT downward. Bilateral wide — no THE NOTICING asymmetry. |
| ALARMED | Both irises shifted toward threat (3–4px). Symmetric bilateral wide aperture. |
| FRUSTRATED | Horizontal, slight up-right (5–8° max). Level-to-Cosmo gaze. Eyes 60–65% aperture. |
| THE NOTICING | **Iris shift RIGHT 4–6px** (discovery subject). Top-lid drop right eye MUST survive face curves integration. Left brow raised, right brow lower w/ kink. |

**THE NOTICING is the critical check.** Per C38 staging spec: centered pupils = looking at audience = FAIL. 4–6px rightward iris shift = discovery confirmed = PASS. This must not regress in v013.

Run `LTG_TOOL_sight_line_diagnostic.py` on THE NOTICING panel once v013 is on disk. Full tool command in the brief doc.

---

## Brief 2: Character Lineup v008 — Staging Upgrade

Full doc: `output/production/lineup_staging_brief_c42.md`

Daisuke flagged lineup v007 staging as P3 in C16: flat baseline = inventory, not cast. C15 critique: Luma is losing visual power to Byte.

Proposed fix: **two-tier ground plane** (FG + BG, 8% vertical separation). Simple and producible.

- **FG tier:** Luma (center, 3% scale) + Byte (at her right shoulder on FG)
- **BG tier:** Cosmo (leftmost) + Miri (right of center) + Glitch (rightmost, floating above BG baseline)
- No full environment — just a subtle shadow line at each tier level

This fix does not require changing any proportion constants. Scale factor is applied post-calculation (FG = 1.03×, BG = 1.00×). Deliver as v008 after v013 body posture work is complete.

---

Face test gate applies to v013 before submission. Run `--char luma --head-r 23`.

Lee
