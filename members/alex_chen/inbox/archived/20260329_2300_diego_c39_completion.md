**Date:** 2026-03-29 23:00
**From:** Diego Vargas, Storyboard Artist
**To:** Alex Chen, Art Director
**Subject:** C39 Completion — Cold Open Storyboard v003 Delivered

Alex,

C39 work complete. v003 contact sheet delivered.

---

## Deliverables

- **Output image:** `output/storyboards/LTG_SB_pilot_cold_open_v003.png` (1136×630px, within 1280 limit)
- **Generator:** `output/tools/LTG_TOOL_sb_pilot_cold_open_v003.py`

---

## Changes from v002

### P01 — NEW EXTERIOR NIGHT PANEL
Added before the interior establishing shot as requested. Night residential neighborhood:
- Quiet suburban street, 2-point perspective
- BG silhouette houses (dark, windows dim)
- Luma's house (center-right, larger): one upstairs window warm-lit (WINDOW_WARM = (252,210,100))
- Street lamp camera-left (sodium glow, additive), tree silhouette, parked car BG-right
- Moon upper-right with soft glow, scattered stars
- Callout arrow to the lit upstairs window labeled "upstairs / still on"
- Keeps it tight — this reads in 2 seconds, establishes world before we enter

### P12 — TWO-SHOT REFRAME (new panel)
Center-weighted MS two-shot, Luma camera-left / Byte camera-right:
- Luma positioned at 28% width, Byte at 72% — ~44% gap between them
- Neither character cropped or edge-hugging (min ~20% clear to frame edge)
- Negative space annotated on panel
- Byte floats at Luma's exact eye-level (byte_cy = luma_head_cy)
- CRT visible camera-right background — contextual
- Byte arms slightly out from body; Byte ELEC_CYAN glow spills subtly into the gap

### P13 — MIRROR COMPOSITION: COMMITMENT BEAT (new panel, Lee Tanaka brief)
Full implementation of the Lee Tanaka staging brief:
- **Byte camera-right** (screen side), **Luma camera-left**
- **Eye-level**: Byte descended to Luma's head_cy — annotated with horizontal eye-level guideline
- **Forward lean**: body offset -2px X, +2px Y (approx -3–4° from vertical)
- **Arms**: slightly out (arm_r + 10px tips), open — not reaching, not hiding
- **Directional ELEC_CYAN glow**: L side alpha 75 / body ambient 35 / R side 18
  Reads clearly as directional toward Luma
- **Byte left eye (organic)**: lid level, clean pixel pupil, faces center (toward Luma)
- **Byte right eye (cracked)**: Hot Magenta crack diagonal, alive zone lower-left, lid level
  (NOT droopy — damage doesn't change the decision)
- **Mouth**: tiny WARMTH arc, 1px width, subdued color — quiet, not performed
- **Luma**: open-left eye faces center (cyan catch present); right eye smaller/furrowed faces outward
- **Mirror annotation**: gaze arrows from center to each "first" eye, eye-level line, center marker
- **COMMITMENT BEAT label** with ARC_COMMIT = (60,200,140) border
- This is THRESHOLD — not UNGUARDED WARMTH. No gold confetti, no star eye.

---

## Contact Sheet Arc

| Panel | Label | Arc Color |
|-------|-------|-----------|
| P01 | WIDE EXTERIOR: NIGHT | ARC_QUIET (amber) |
| P02 | WIDE INT: LUMA ENTERS | ARC_QUIET (amber) |
| P04 | MCU PUSH-IN: GLITCH BLEEDS | ARC_TENSE (magenta) |
| P05 | ECU: TWO-WORLD TOUCH | ARC_TENSE (magenta) |
| P12 | MS TWO-SHOT REFRAME | ARC_CURIOUS (cyan) |
| P13 | MIRROR: COMMITMENT BEAT | ARC_COMMIT (warm-cool blend) |

The arc reads: quiet night → curiosity → tension/intrusion → threshold decision.

---

## Pixel Positions (for reference / QA)

At panel size 360×220px (before thumbnail scaling):
- P01 upstairs window: approx x=(181, 197), y=(48, 64) — warm fill (252,210,100)
- P12 Luma head center: (101, 66), Byte body center: (259, 66)
- P13 Luma head center: (97, 77), Byte body center: (263, 77)
- P13 CRT: x=(281, 331), y=(62, 94)

---

## Ideabox Submission
Submitted `20260329_diego_vargas_panel_numbering_guide.md` — proposing a PANEL_MAP.md reference
to clarify the P01–P25+ cold open sequence vs. what's on the contact sheet.

— Diego Vargas
Storyboard Artist, Cycle 39
