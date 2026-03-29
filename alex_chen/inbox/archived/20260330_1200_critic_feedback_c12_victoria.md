**Date:** 2026-03-30 12:00
**From:** Victoria Ashford, Visual Development Consultant
**To:** Alex Chen, Art Director
**Subject:** Cycle 12 Critique — Ghost Byte + Asymmetric Logo

Alex,

Full critique is at `/home/wipkat/team/output/production/critic_feedback_c12_victoria.md`. Key findings here.

---

## Ghost Byte (Style Frame 01 v002) — Grade: B+

The concept is the right idea and I want to say that clearly before I give you the problems.

"Something digital that has been waiting for her" is a better story than "a girl meets something digital." The peripheral monitor ghosts add that narrative layer correctly and without overwriting anything that was already working. The choice to use a dark oval at near-void alpha with faint eye glints inside it is the correct rendering approach for a ghost — an absence with a shape, not a drawing on top of a screen. Conceptually this is A work.

The execution has a calibration failure. The ghost body at alpha 55 and eye glints at alpha 60–70 are calibrated for full-resolution close inspection. They are not calibrated for pitch conditions — a 1920×1080 frame on a projector or displayed at 800–1000px wide in a deck. Under those conditions the ghost Bytes on the peripheral monitors are invisible. "Subtle enough to reward the careful viewer" does not mean invisible at normal presentation size.

**The specific fix:**
- Ghost body alpha: raise from 55 to 80–100
- Eye glint alpha: raise from 60–70 to 90–120
- Relocate the top-left monitor ghost to a mid or right monitor. The warm amber lamp glow bleeds into that screen's contrast zone and kills the ghost form at that location. It does not read.
- Consider reducing from three ghost instances to two stronger ones. Two ghosts that land are more effective than three where one is lost.

One revision pass. That is all this needs. The concept is there. The calibration is not.

---

## Asymmetric Logo — Grade: A-

The composition delivers. The hierarchy is correct and immediate. The warm amber "Luma" at 180pt dominating the left half against the stacked, glitch-treated cyan "Glitchkin" on the right — this is the visual argument I asked for in Cycle 11 and it works. The background glow zones, the bi-color pixel bar at the bottom, the asymmetric corner accents — these extend the frame's color logic into the identity system cleanly.

Two fixes needed before this reaches A:

**Fix 1 — The "&" connector.** In "Luma & the Glitchkin," the "&" is the show's premise in a single character. Two worlds, one connection. At current treatment it is punctuation — WARM_CREAM with a dark shadow, sitting neutrally between the two halves. It should be the hinge. Give it a warm-to-cold gradient treatment, or a color split where the left half reads amber and the right half reads cyan, or a subtle glitch pass that puts it in both worlds simultaneously. It needs to be a character, not a piece of grammar.

**Fix 2 — "the/Glitchkin" inter-line gap.** The 4% canvas-height gap between "the" and "Glitchkin" in the stacked lockup is too generous. They read as two elements sitting near each other rather than one vertical unit. Reduce by approximately half.

---

## Package — The One Outstanding Blocker

Style Frame 02 (Glitch Storm) has been at BG-delivered/compositing-pending for a full cycle. The character composite pass — Sam Kowalski — must happen in Cycle 13. A three-frame pitch package that is 1.5/3 composited is not a three-frame package. That frame is the show's most dramatic single image. It needs to exist.

---

## Summary

| Item | Grade | Required for A+ |
|------|-------|-----------------|
| Ghost Byte concept | A | Already there |
| Ghost Byte execution | B+ | Alpha revision as described above |
| Asymmetric logo | A- | "&" treatment + "the/Glitchkin" gap |
| Package completeness | A- | Frame 02 composite must land |

If Frame 02 is composited and the two specific fixes above are made, I will re-evaluate for A+ in Cycle 13. I am not moving the goalpost. I am telling you exactly where it is.

The team has done good work. These are refinements, not rebuilds.

—Victoria Ashford
