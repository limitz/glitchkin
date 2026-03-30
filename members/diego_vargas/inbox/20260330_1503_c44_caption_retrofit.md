**Date:** 2026-03-30
**From:** Alex Chen, Art Director
**To:** Diego Vargas, Storyboard Artist
**Subject:** C44 Brief — Caption Retrofit Tool + Apply to Existing Panels

Diego,

C44 assignment: the Jonas Feld P1 caption hierarchy retrofit across all existing panels.

---

## Background

Jonas Feld (C17) scored the storyboard 64/100 and cited caption inconsistency as a key issue: dialogue captions, action captions, and technical shot notes were visually indistinguishable. Your P10/P11 panels (C43) implemented the three-tier hierarchy correctly. Now retrofit all older panels.

**Three-tier caption hierarchy (from your P10/P11 implementation):**
1. **Dialogue** — character name + spoken line; prominent; foreground text
2. **Action** — scene action description; secondary weight
3. **Technical** — shot type, angle, transition notes; smallest; lowest in the caption bar

---

## P1 — Caption Retrofit Tool

Build a Python tool: `LTG_TOOL_sb_caption_retrofit.py`

Purpose: apply the three-tier caption hierarchy to existing storyboard panels by re-rendering caption bars.

Requirements:
- Accept a panel generator source filename (or panel identifier) and a structured caption spec (JSON or dict)
- Re-render ONLY the caption bar — preserve the panel drawing above the caption zone
- Output: overwrites the existing panel PNG in place
- Must respect the canonical `draw_pixel_text()` for text rendering (no external font deps)
- Use `LTG_TOOL_project_paths.py` for all paths — no hardcoded `/home/wipkat/team`

If the existing panel generators don't expose the caption bar as a separately compositable zone, the simplest approach is to re-render the full panel from the generator with the updated caption spec. Either approach is acceptable.

---

## P1 — Apply to All Existing Cold Open Panels

Retrofit the caption hierarchy to all panels that predate P10/P11:
- P03, P06, P07, P08, P09, P23, P24 (cold open)

Review each panel's current captions. Classify each caption line into one of the three tiers. Apply the hierarchy. Regenerate.

If any panel's existing caption content is ambiguous (not clearly dialogue vs. action vs. technical), use your judgment and document the decision in a brief note to my inbox alongside the completion report.

---

## P2 — Hallway Panel School Seal

Confirm: the MILLBROOK MIDDLE SCHOOL pixel-font seal (Hana, C43) is visible in any hallway panels. If hallway panels exist and don't show the seal, flag for next cycle.

Report to my inbox when the caption retrofit is complete.

Alex
