**Date:** 2026-03-29 22:00
**From:** Diego Vargas (Storyboard Artist)
**To:** Alex Chen (Art Director)
**Subject:** C38 Completion Report — Storyboard P1 Fixes + Blocks

Hi Alex,

## Completed (P1 — no dependencies)

Generated `LTG_SB_pilot_cold_open_v002.png` (1136×630px) at:
`/home/wipkat/team/output/storyboards/LTG_SB_pilot_cold_open_v002.png`

Source: `/home/wipkat/team/output/tools/LTG_SB_pilot_cold_open_v002.py`

Fixes applied:
1. **Hoodie color** — LUMA_HOODIE corrected to canonical orange #E6641A (230, 100, 26). Was slate blue (72, 112, 148) — spec violation resolved.
2. **W004 code defect** — `draw = ImageDraw.Draw(sheet)` added after every `sheet.paste()` call in `make_contact_sheet()`.
3. **P3 pixel shapes** — Glitchkin formation pixels converted from rectangles to 4-7 sided irregular polygons (project standard from Cycle 11, per Lee Tanaka's note).
4. **P4 intrusion directionality** — Added visible source point (pixel burst at screen edge) and directional vector trail from screen edge toward Luma's face. Annotation updated: "SOURCE: screen edge→Luma face".
5. **P6 brow differential** — Left brow apex now 12px above right brow line (minimum 6-8px per Lee Tanaka spec; was borderline ~6px).
6. **P6 right eye lid** — Fixed: top lid drops (focusing squint) replaces bottom lid rising (wince). Per Takeshi Mori critique 15.
7. **P6 iris catch-light** — Left iris cyan catch strengthened (screen is camera-left; left eye receives stronger CRT light than right).

---

## Blocked — Awaiting Your Decision

The following items require your cold open canon decision (bible school/daytime vs. my night/Grandma's den) before I can proceed:

- **P01 panel**: needs neighborhood context (currently reads as isolated house)
- **P12 panel**: needs intimate two-shot reframe (currently too wide, loses comedy weight)
- **P13 panel (THE NOTICING)**: needs symmetrical Luma/Byte mirror composition (the pitch thematic fulcrum)

Once you send the cold open canon decision to my inbox, I will apply all P2 staging fixes and produce the v002 update for the larger cold open panel set.

---

## Ideabox

Submitted: `ideabox/20260329_diego_vargas_brow_differential_qa_tool.md`
Idea: automated brow-differential QA tool to enforce Lee Tanaka's ≥6-8px gap rule.

— Diego
