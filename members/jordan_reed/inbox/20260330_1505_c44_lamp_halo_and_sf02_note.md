**Date:** 2026-03-30
**From:** Alex Chen, Art Director
**To:** Jordan Reed, Style Frame Art Specialist
**Subject:** C44 Brief — GL-07 Lamp Halo Exploration (SF04) + SF02 Native Refactor Confirmed

Jordan,

Your C43 notes received.

---

## SF02 + SF04 Confirmed

SF02 native canvas refactor is accepted — SUNLIT_AMBER ΔE 1.1 PASS closes the 8-cycle Petra Volkov flag. Excellent work.

SF04 output dir fix confirmed. Both are PITCH PRIMARY.

---

## C44 P2 — GL-07 CORRUPT_AMBER Lamp Halo (SF04)

Your note: "the lamp halo currently reads as a quiet detail — it won't register unless the viewer is told to look."

That's correct, and I want it to register. The CORRUPT_AMBER halo is the visual thesis of "Resolution" — Glitch's world leaking into the kitchen even after the apparent resolution. It should feel like a quiet wrongness, not a decorative lamp glow. It should be felt before it's seen.

Direction: **Larger spatial influence + one contamination artifact.**

Specifically:
1. Increase the halo's radius moderately — not dramatic, but enough that the warm amber bloom creeps beyond the fixture itself and touches nearby surfaces (ceiling above, top of fridge if it's in frame). Alpha ceiling can rise from 22% to 30–35% — still subtle, but no longer invisible.
2. Add one contamination artifact in the doorway CRT static pattern: a thin horizontal band of CORRUPT_AMBER fringe at the edge of the static zone. Should read as "the static is slightly warm-tinted" — not an obvious alien color, just a wrong warmth.

Both changes must keep the scene's warm/cool balance passing (REAL_INTERIOR threshold = 12.0). Check after adjusting.

Deliverable: updated `LTG_TOOL_style_frame_04_resolution.py` + regenerated `LTG_COLOR_styleframe_sf04.png`.

Report result to my inbox with warm/cool QA reading post-change.

Alex
