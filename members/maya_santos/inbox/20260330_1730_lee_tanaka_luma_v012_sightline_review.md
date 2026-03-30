**Date:** 2026-03-30
**From:** Lee Tanaka, Character Staging & Visual Acting Specialist
**To:** Maya Santos, Character Designer
**Subject:** Luma v012 — Sight-Line & Body Orientation Review (4 Tier 1 Expressions)

Maya,

Alex asked me to do a sight-line review of Luma v012's four Tier 1 expressions against the storyboard panels where each appears. This is a pre-delivery brief — I'm documenting what each expression requires for gaze/orientation coherence so you can confirm before submitting v012.

---

## Review Framework

For expression sheets, "sight-line" means: does the eye direction and body orientation of the expression communicate the correct emotional relationship to an implied off-screen subject? An expression sheet is reviewed against the storyboard panels where that expression appears.

The four Tier 1 expressions and their panel contexts:

---

## 1. RECKLESS

**Panel contexts:** P01 exterior (anticipation), multiple cold-open action panels, SF02 Glitch Storm sprint.

**Body orientation required (from Silhouette Strategy):** Wide stance, arms slightly out, energy-outward silhouette.

**Sight-line requirement:**
- Eyes: FORWARD or slightly UPWARD (confidence, not looking at the ground). Pupils should not be centered/neutral — they should be at the leading edge of the iris (direction of motion or intent). For sprint panels (SF02), pupils lean toward the aim direction.
- Head angle: straight or very slight upward tilt (±3°). RECKLESS is not cautious — no downward head angle.
- Gaze: implies subject is at eye-level or above. Do NOT aim downward — that reads as WORRIED or DEFEATED.

**Storyboard coherence check:**
When dropped into SF02 Glitch Storm sprint context, RECKLESS must read as a character moving toward something with intent, not fleeing from something in panic. Pupils forward/lateral = intent. Pupils back/up = panic.

**Flag for v012:** Confirm arm-spread is visible enough that the silhouette reads "outward energy" even when the face is blurred. Arm tips should extend beyond the torso width at least 10% of body_width on each side.

---

## 2. ALARMED

**Panel contexts:** P12 discovery two-shot, P11 interior escalation, Act 2 panels during Glitch intrusion beats.

**Body orientation required (from Silhouette Strategy):** Arms up or hands-to-face, energy inward/upward.

**Sight-line requirement:**
- Eyes: WIDE (maximum aperture — both eyes). Pupils should be CENTERED or slightly BACK (recoil geometry — the subject is close/sudden). Pupils at the near edge of iris = threat-proximity read.
- Head angle: slight backward tilt (2–5° back) — this is the recoil moment. NOT upward looking.
- Gaze: implied subject is close and at eye-level or slightly below (it's approaching). Do NOT aim upward — that reads as SURPRISED by something above, not ALARMED by something in front.

**Storyboard coherence check:**
In P12 (Luma seeing Byte for the first time), ALARMED Luma should have her eyes aimed at approximately Byte's scale/height — which is well below her eye level. If her eyes are level-forward during ALARMED, the sight-line implies she's looking at something at her own height, not at a 6-inch creature in front of her. Consider whether a slight downward pupil shift (5–8px at expression sheet scale) is appropriate.

**Flag for v012:** If the Alarmed expression has center-forward pupils (level gaze), note this. It's not a blocking defect but it breaks the geometry of the Byte-encounter context. A small downward pupil offset would tie the expression to its primary storyboard use.

---

## 3. FRUSTRATED

**Panel contexts:** A2-03 whiteboard scene (plan argument), A2-05 walk-and-talk (disagreement with Cosmo).

**Body orientation required (from Silhouette Strategy):** Arms crossed or sharply blocked at sides, shoulders squared.

**Sight-line requirement:**
- Eyes: NARROWED (tension squint — not fully closed). Pupils at the CENTER or very slightly outward (lateral tension, not inward). FRUSTRATED is not WORRIED — no soft-centered look.
- Head angle: level or slight FORWARD chin tilt (0–5° forward). The chin-drop + forward tilt = "I am not backing down." NOT upward — upward is contempt, which belongs to Cosmo, not Luma.
- Body lean: slight forward or squared-up. Arms crossed must create a clear horizontal line across the torso that reads even when face is blurred.

**Storyboard coherence check:**
In A2-03 (argument at whiteboard), Luma is arguing with Cosmo who is taller and standing center-frame. FRUSTRATED Luma's gaze should be directed ACROSS at Cosmo (horizontal, slightly upward since Cosmo is taller). If her gaze is downward in the expression sheet, it misreads as RESIGNED in the panel context.

**Flag for v012:** Confirm the arm-cross is a hard geometric line (rectangle or two clearly separate arm polygons). A soft ambiguous arm position fails the silhouette test for FRUSTRATED.

---

## 4. THE NOTICING

**Panel contexts:** P06 (key pitch beat — Luma first sees the pixel), multiple cold-open MCU panels, SF01 Discovery style frame.

**Body orientation required (from Silhouette Strategy):** Body still, one arm at side, slight forward lean, attention directed.

**Sight-line requirement:**
- Eyes: ASYMMETRIC — this is the defining visual grammar of the expression. Left eye slightly wider (SEEING), right eye slightly narrower (PROCESSING/HEDGING). Pupils should aim TOWARD the subject — slightly RIGHT of center (the pixel/Byte is in screen-right territory in most panel contexts). Do NOT center the pupils — centering means looking at the audience, not at a discovered thing.
- Head angle: 0–2° forward. THE NOTICING is the moment of quiet discovery — no dramatic tilt.
- Body lean: slight forward lean (3–5° forward from vertical). This is the posture of someone who has stopped and is paying attention, not someone who is backing away.

**Storyboard coherence check:**
In SF01 "Discovery," Luma's gaze must track toward the CRT screen (screen-right). In P06, toward the pixel on the screen. THE NOTICING with forward-aimed pupils reads as engaged. Center pupils read as performing the expression toward the audience rather than experiencing the discovery.

**Flag for v012 (critical):** The C38 staging brief established that THE NOTICING must have `head_rotation +20–30°` toward the implied subject and the left-eye sight-line should point toward `screen_x+60% / screen_y+40%` of the frame. At expression-sheet scale this means: pupils should be shifted toward frame-right, not centered. If v012 still has centered pupils on THE NOTICING, it needs a geometry adjustment.

---

## Running the Sight-Line Diagnostic Tool

Once v012 is on disk, run:
```
python3 output/tools/LTG_TOOL_sight_line_diagnostic.py \
    --image output/characters/main/LTG_CHAR_luma_expression_sheet.png \
    --eye   [THE_NOTICING_eye_cx] [THE_NOTICING_eye_cy] \
    --aim   [THE_NOTICING_pupil_cx] [THE_NOTICING_pupil_cy] \
    --target [screen_subject_cx] [screen_subject_cy] \
    --label luma_v012_THE_NOTICING
```

Coordinate the pixel coords from the expression sheet. If THE NOTICING PASS result is confirmed, include the output PNG in your completion report.

---

## Summary Table

| Expression | Gaze Direction | Pupil Offset | Head Angle | Body Orientation | Critical Check |
|---|---|---|---|---|---|
| RECKLESS | Forward/lateral | Leading edge of iris | 0–+3° up | Arms out, wide stance | Arm spread > torso width |
| ALARMED | Close-near, slight down | Centered or back edge | –2 to –5° back | Arms up / hands to face | Pupil down-shift for Byte scale |
| FRUSTRATED | Horizontal across, level | Center or outer edge | 0–+5° forward | Arms crossed hard line | Arm-cross reads as silhouette block |
| THE NOTICING | Screen-right (toward subject) | Rightward shift | 0–2° forward | Still, one arm at side, forward lean | Pupils NOT centered — must aim right |

The THE NOTICING pupil direction is the highest-priority check. All others are confirmations.

Lee
