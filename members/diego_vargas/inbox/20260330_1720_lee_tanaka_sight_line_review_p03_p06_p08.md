**Date:** 2026-03-30
**From:** Lee Tanaka, Character Staging & Visual Acting Specialist
**To:** Diego Vargas, Storyboard Artist
**Subject:** Sight-Line Review — Cold Open P03, P06, P08

Diego,

Sight-line staging review of your C41 cold open panels. Notes below.

---

## P03 — CRT Object Shot (CURIOUS beat)

**Staging:** Static hero CRT prop. Single ELEC_CYAN pixel lower-right. No character present.

**Sight-Line Assessment:** NO ACTIVE SIGHT-LINE — no character in frame. This is correct. P03 is an object shot; the audience's gaze is directed by composition, not character eyeline.

**Compositional note:** CYAN pixel lower-right is the correct placement — lower-right creates mild exit tension (the eye wants to follow it off-frame). This sets up anticipation for P04/P06 where Byte appears. Strong instinct.

**Result: PASS (no active sight-line to check)**

---

## P06 — Monitor Screen CU / Byte First Appearance (DISCOVERY beat)

**Staging from your spec:** Byte's face pressed flat against glass from inside. Normal eye (right) at 70% aperture squint. Cracked eye (left) in SEARCHING/PROCESSING mode (3 dots). Mouth: horizontal flat grimace, corners outward.

**Sight-Line Assessment:**

Byte's expression is INWARD — he's assessing the room beyond the glass (Luma's world). The direction Byte is facing (toward us / the camera = toward Luma off-screen left) is correct for the beat. His normal right eye should be directed toward where Luma will be in the subsequent panels — screen center-left.

**Flag — cracked eye direction:** The cracked-left eye processing dots should NOT aim forward symmetrically with the normal eye. In Byte's cracked-eye system, the cracked eye registers the environment differently — it should have a slight divergence (∼5–8° off-axis from the normal eye's aim line). This is the visual grammar that distinguishes his digital perception from normal looking. If both eyes aim identically, the cracked eye reads as decoration rather than a different processing state.

**Flag — confetti at hand-press contact points:** Confirm confetti is escaping at BOTH left and right hand contact points, not just one side. Symmetric hand contact points framing the face make the "pressed against glass" gag read. Asymmetric hands read as "reaching" rather than "pressed."

**Action:** Minor refinement only. If your current implementation already has divergent cracked-eye aim and symmetric hand confetti, no change needed. If not, adjust before finalizing.

---

## P08 — MED Shot / Byte Full Body in Real World (TENSE beat)

**Staging from your spec:** Camera at Byte's eye level (~6" off floor). Full body reveal — inverted teardrop, stubby arms/legs. Head barely above cable bundles. Desaturation ring at feet. CRT defocused in BG.

**Sight-Line Assessment:**

At eye-level camera, Byte's eyes should be directed TOWARD the audience / toward where Luma will be (off-frame). His dialogue is "Ugh. The flesh dimension." — this is contempt/disdain directed outward, not inward reflection.

**Flag — gaze direction:** Byte's eyes at MED eye-level must aim OUTWARD (toward camera or toward Luma's position off-frame right/left). If the body is centered and the eyes aim forward at 0°, the gaze is directly at the audience — which works for this beat (confrontational, contemptuous, breaking the fourth wall slightly). Confirm his pupils are not looking DOWN (downward = shame/resignation, wrong tone) or UP (upward = daydream/fear, wrong tone). Level-forward or slightly upward-tilted (superiority) is correct for CONTEMPT expression at this beat.

**Flag — camera angle geometry:** Per the sight-line spec, camera eye-level means floor_y should read as "below midframe" on the panel (floor recedes steeply). If floor_y is too high (above 65% of DRAW_H), the camera appears higher than Byte's eye level, which undermines the "camera validates him at tiny scale" intent. Byte should feel level with us, not looked down upon.

**Result: Flag for gaze direction check. If pupils are level-forward, PASS. If looking down, revise.**

---

## Sight-Line Batch Config

I've created a batch config for these panels in:
`output/production/sight_line_batch_cold_open_p06_p08.json`

Run it once your P06/P08 outputs are finalized to confirm the machine-readable check:
```
python3 output/tools/LTG_TOOL_sight_line_diagnostic.py \
    --batch output/production/sight_line_batch_cold_open_p06_p08.json \
    --output-dir output/production
```

P03 is excluded from the batch config (no active sight-line to check).

---

## Summary

| Panel | Result | Action |
|---|---|---|
| P03 | PASS | None |
| P06 | Flag (minor) | Verify cracked-eye divergence + symmetric hand confetti |
| P08 | Flag (gaze) | Confirm Byte's pupils are level-forward, not downward |

No panel-level redesign required. These are geometry-confirmation items.

Lee
