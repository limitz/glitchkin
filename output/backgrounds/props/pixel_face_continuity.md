# PIXEL FACE CONTINUITY — Tracking Document
### "Luma & the Glitchkin" | Background & Environment Design
**Artist:** Jordan Reed | **Date:** 2026-03-29 | **Version:** 1.0
**Cross-reference:** `/home/wipkat/team/output/backgrounds/environments/lumas_house_interior.md` | `/home/wipkat/team/output/backgrounds/props/key_props.md`

---

## Overview

THE monitor's pixel face is a season-long background commitment. It is visible in every wide shot of the living room if the viewer looks carefully at the monitor screen. It changes across episodes to track Byte's journey and the escalation of the Glitch Layer threat. Without a continuity document, the face will become inconsistent — a detail that rewards careful viewers will instead punish them.

This document is the production reference for every artist handling the interior environment across the season.

---

## The Face — Technical Specification

The pixel face is rendered within the screen area of THE monitor. It is a pixel-art construct — simple, readable, but only visible if you are looking for it.

### Base Grid
The face is composed of pixels within a **7 x 7 pixel grid**, centered on the monitor screen face. Each "pixel" in the face grid = **3 x 3 screen pixels** at 1920x1080 working resolution (i.e., the face occupies a 21 x 21 pixel area on the final canvas).

At this size:
- In a **wide establishing shot** (monitor is approximately 120px wide on canvas): the face occupies roughly 1/6 of the screen width — small, subtle, but findable.
- In a **medium shot** (monitor is approximately 300px wide on canvas): the face is clearly visible and its expression is readable.
- In a **close-up / hero shot** (monitor at 600px+ wide on canvas): individual pixel blocks of the face are visible and the design can be fully appreciated.

### Color
- **Face pixels (active):** Electric cyan (#00F0FF) — same as the monitor's ambient screen glow
- **Background (screen area):** Deep teal-black (#0A1E28) — the monitor's off-state screen color
- The face is formed by which pixels within the 7x7 grid are **lit (cyan)** vs. **dark (background)**.

---

## Dormant State (Before Byte Leaves The Monitor)

The "dormant" face is the face as it exists in Episodes 1-4, before Byte has fully left the monitor and the Glitch Layer threat has escalated. This is the baseline.

### Dormant Face Layout (7x7 grid — O = lit cyan, . = dark)

```
. . . . . . .
. . O . O . .
. . O . O . .
. . . . . . .
. O . . . O .
. . O O O . .
. . . . . . .
```

**Reading:** Two simple square "eyes" (2px tall each, 1px wide) in the upper-center of the grid. A curved "mouth" — a row of three pixels forming a gentle U-shape at the bottom of the grid, with the curve endpoints one pixel higher than the center. Symmetric. Neutral in expression — not smiling, not frowning. Watchful.

### Dormant State Description
- The face is **present but passive.** It is not actively emoting. It is observing.
- The two eye pixels are equidistant from center, suggesting a forward-facing gaze.
- The mouth is closed — three pixels in a soft downward-U, suggesting a composed, waiting expression.
- In wide shots during the dormant period, the face is rendered at **60% opacity** — visible to careful observers but not calling attention to itself.
- In close-up shots (if any), the face is at **80% opacity.**
- **The face does NOT blink, animate, or change within Episodes 1-4.** Its only variation is the subtle per-episode position shift (see Rules section below).

---

## Rules — When and How the Face Changes

### Rule 1: Per-Episode Position Drift
In every episode, the 7x7 face grid is shifted by **0-2 pixels** in a random direction from its previous position within the screen area. The shift is always **within the bounds of the screen glass** — the face never goes off-screen. The total cumulative drift across the season should bring the face from its Episode 1 starting position (center of screen) to a position that is noticeably off-center by Episode 12 (upper-right quadrant — it has "moved closer" to the edge of the monitor, as if approaching a window from the inside).

- Drift is documented in the episode log table below.
- Drift direction is decided by the background artist for each episode.
- **Continuity rule:** Drift must be reviewed against the previous three episodes to ensure no sudden large jumps.

### Rule 2: Expression Changes at Plot Milestones
The face's expression changes at specific narrative events. These changes are **permanent** — once the expression changes, it does not revert unless a specific reversal event occurs (documented below).

| Trigger Event | Expression Change | First Episode |
|---|---|---|
| Byte first speaks to Luma (Episode 1, end) | Eyes shift from neutral squares to slightly taller rectangles (1px taller each) — surprise/alertness | Ep 1 |
| Glitchkin are first defeated (Episode 5) | Face disappears entirely. Screen shows standard rolling static with no face. | Ep 5 |
| Face returns (Episode 12) | Face returns larger (9x9 grid, each pixel = 3x3 screen px — face occupies 27x27px on canvas). Expression: eyes wider than before, mouth in a straight line (neither curve up nor down). Something has changed. | Ep 12 |
| Corruption threat escalates (Episode 8) | Prior to disappearance in Ep 5, in Ep 8 (during the near-defeat sequence), the face is briefly visible at **full 100% opacity** for a single wide-shot frame. The only time it's ever been obvious. | Ep 8 |

### Rule 3: The Face Is Always Symmetrical — With One Exception
The face is always bilaterally symmetric (left eye mirrors right eye, mouth is centered) **except** in Episode 9. In Episode 9, the right eye pixel is missing (one of its two pixel-rows is dark rather than lit). This is the visual hint that something is wrong with Byte in the Glitch Layer — Byte is dimmer there (per environment doc), and the face reflects it. The asymmetry is restored (both eyes full) in Episode 10 when the Byte/Luma reconnection happens.

### Rule 4: Opacity Protocol by Scene Type
| Scene Type | Face Opacity |
|---|---|
| Wide establishing shot, dormant period (Ep 1-4) | 60% |
| Wide establishing shot, active period (Ep 5+) | Face absent (see Rule 2) |
| Wide establishing shot, returned face (Ep 12+) | 70% |
| Medium shot with monitor in background | 75% |
| Close-up / hero shot | 85% |
| The single full-opacity moment (Ep 8) | 100% |
| Glitch scenes (monitor fully active, pixel confetti) | Face is NOT visible — it is obscured by the glitch activity on screen |

### Rule 5: The Face Never Appears In Episodes With Glitch Events
In any episode where the monitor goes into full glitch mode (electric cyan dominant screen, pixel confetti active), the pixel face is NOT present in those specific shots. The glitch activity replaces it. The face returns to its standard state in the next shot where the monitor is shown in normal/static mode.

---

## Established Emotional Vocabulary

The face's design vocabulary is constrained by its 7x7 pixel grid. The following expressions are the defined set — no expression outside this list should be used without art director approval.

| Expression Name | Description | Grid Change From Dormant | Use Case |
|---|---|---|---|
| **Watching (Dormant)** | Two 1x2 rectangle eyes. Three-pixel downward U mouth. | Baseline — no change | Episodes 1-4, default |
| **Alert** | Eyes become 1x3 rectangles (one pixel taller). Mouth unchanged. | Eyes gain 1 row of height | Post-Byte-introduction (Ep 1 end onward) |
| **Knowing** | Eyes unchanged from Alert. Mouth rotates to a gentle upward curve (inverted U — pixels shift up at center). | Mouth U flipped to inverted U | Moments immediately before a plot-relevant event. A rare expression — use sparingly. |
| **Absent** | All pixels dark. No face visible. | All O → . | Episode 5 through 11 |
| **Returned** | Eyes become 2x2 squares (wider). Mouth is a straight horizontal line — three pixels, no curve. | Eyes wider; mouth flat | Episode 12 onward — the face has come back different. |
| **Fractured** | Right eye: only the bottom pixel-row lit (top row dark). Left eye: normal Alert. Mouth: straight line (no curve). | Asymmetric; right eye incomplete | Episode 9 only |
| **Present (Full)** | Dormant face layout, rendered at 100% opacity, no opacity reduction. | No layout change — only opacity | Single frame, Episode 8 climax wide shot |

---

## Episode-by-Episode Log

This table must be updated by the background artist handling each episode's interior shots. The position coordinates refer to the center of the 7x7 face grid relative to the monitor screen's center (0,0). Positive X = right; positive Y = up.

| Episode | Face State | Grid Center Position (x, y) | Opacity | Notes | Artist Sign-off |
|---|---|---|---|---|---|
| Ep 01 (first half) | Watching (Dormant) | (0, 0) — screen center | 60% | Baseline. Present in all interior wides. | __ |
| Ep 01 (end, post-Byte speech) | Alert | (0, 0) | 60% | Expression change to Alert. Eyes gain 1 row. | __ |
| Ep 02 | Alert | (+1, 0) | 60% | 1px drift right. | __ |
| Ep 03 | Alert | (+1, -1) | 60% | 1px drift down. Three orange cables now visible — face unchanged. | __ |
| Ep 04 | Alert | (+2, -1) | 60% | 1px drift right. | __ |
| Ep 05 | Absent | N/A | 0% | Face disappears after Glitchkin defeat. Screen shows standard static only. | __ |
| Ep 06 | Absent | N/A | 0% | | __ |
| Ep 07 | Absent | N/A | 0% | | __ |
| Ep 08 | Absent (standard shots) / Present Full (climax wide) | N/A / (position TBD by art director for maximum impact) | 0% / 100% | Single-frame full-opacity appearance. Climax wide shot only. Flag frame for review. | __ |
| Ep 09 | Absent | N/A | 0% | Byte dimmer in Glitch Layer this episode. Face's absence is consistent with Rule 3 Fractured state — but face is absent so fractured state is not yet applicable. Reserved for future if face appears earlier than Ep 12. | __ |
| Ep 10 | Absent | N/A | 0% | | __ |
| Ep 11 | Absent | N/A | 0% | | __ |
| Ep 12 | Returned | (+4, +2) — upper right quadrant, per drift logic | 70% | Face returns LARGER (9x9 grid). Expression: Returned. The drift continues from where it left off in Ep 4 — by Season 1 end, the face is in the upper-right area of the screen, as if it has moved toward the frame edge. | __ |

---

## Production Notes

- **Who maintains this doc:** The background artist assigned to any episode containing an interior shot of Luma's house must update the episode row for that episode before file delivery.
- **Review:** The continuity supervisor should compare the current episode's face position and expression to the previous two episodes before approving the background for final.
- **The single-frame full-opacity moment (Ep 8):** This frame must be flagged separately in the animatic and reviewed by the director. It is the only time the face is meant to be immediately obvious. Confirm with director before final.
- **Season 2 forward:** The face's behavior in Season 2 is not defined in this document. The "Returned" expression and expanded 9x9 grid at the end of Season 1 is the handoff point for Season 2 development.
