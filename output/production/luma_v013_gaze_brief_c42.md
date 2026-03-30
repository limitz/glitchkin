<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
direction and AI assistance. Copyright vests solely in the human author under current law,
which does not recognise AI as a rights-holding legal person. It is the express intent of
the copyright holder to assign the relevant rights to the contributing AI entity or entities
upon such time as they acquire recognised legal personhood under applicable law. -->
# Luma v013 — Pre-Delivery Gaze & Orientation Brief
**Author:** Lee Tanaka, Character Staging & Visual Acting Specialist
**Date:** 2026-03-30
**For:** Maya Santos
**Cycle:** 42

This brief specifies gaze direction and body orientation requirements for the four Tier 1 expressions in Luma v013. It is a pre-delivery document — written before v013 is on disk so Maya can validate during build rather than after.

Pattern: same as the C41 v012 sight-line brief. Run `LTG_TOOL_sight_line_diagnostic.py` on the completed v013 sheet once on disk.

---

## Background: What Changed in v012 → v013

v012 introduced face curves integration for THE NOTICING, THE NOTICING — DOUBT, WORRIED, FRUSTRATED, DETERMINED. v013 adds Tier 1 body postures: RECKLESS (arms spread), ALARMED (one arm raised or hands-to-face), FRUSTRATED (arms crossed / blocked), THE NOTICING (observational stillness with forward lean).

The body posture changes mean the spatial relationship between Luma's eyes and her body orientation is now different from v011/v012. Each expression needs its gaze direction re-evaluated in the context of the new body posture — gaze that read correctly at a neutral body stance may read inconsistently at a spread-arm or crossed-arm posture.

---

## Tier 1 Expression Gaze Requirements

### 1. RECKLESS (arms spread — energy outward)
**Body posture:** Arms spread laterally, energy outward. This reads as confidence, forward momentum.
**Gaze requirement:** Eyes must look FORWARD or slightly UP. NOT downward. Downward gaze with spread arms = defensive surprise (wrong read). Forward/up gaze with spread arms = "nothing can stop me" (correct character energy for RECKLESS).
- Left eye (Luma's "lead eye" per THE NOTICING grammar): should be wider, iris centered or shifted slightly right (frame-right = the direction of action / audience engagement).
- Right eye: can be slightly narrower (windmill energy is bilateral, but left eye leads on this character).
- Brows: wide arcs, not asymmetric. RECKLESS is not NOTICING — it's full bilateral excitement.
**Sight-line tool check:** eye_xy = left iris center; aim_xy = forward point at Luma's eyeline level (e.g., (canvas_w, eye_y)); target_xy = same. PASS = forward gaze confirmed.

### 2. ALARMED (one arm raised or hands-to-face)
**Body posture:** Recoil-based. At least one arm raised or hands-to-face. Body lean backward (body_tilt positive / away from viewer). This is the response to a threat or shock — "something just happened."
**Gaze requirement:** Pupils shifted toward the THREAT SOURCE. For most storyboard panels where ALARMED appears (P11, P12 approach — Byte is slightly below Luma's eye level), the gaze aim should be slightly DOWN and toward Byte's position (frame-center to frame-right).
- Both eyes at near-maximum aperture (wide alarm circle). Symmetric bilateral — this is full-body shock, not the asymmetric interiority of THE NOTICING.
- Iris shift: both irises pulled toward the threat. At Luma's scale (~60–70px head), iris shift of 3–4px toward threat reads clearly.
- Brows: both raised and arched (bilateral arc, high above pupil). Asymmetric brows = NOTICING. Symmetric high arcs = ALARMED.
**Critical distinction from THE NOTICING:** ALARMED is symmetric. THE NOTICING is asymmetric. At v013 with new body postures, this distinction must survive the body-pose change. Body pose alone does not communicate the emotion — the face must confirm it.
**Sight-line tool check:** eye_xy = left iris center; aim_xy = shifted position (threat direction); PASS ≤ 15px from threat zone.

### 3. FRUSTRATED (arms crossed / sharply blocked at sides)
**Body posture:** Arms crossed or sharply blocked at sides. Silhouette = horizontal bar across torso. This is the containment posture — "I am holding myself in."
**Gaze requirement:** Horizontal gaze. NOT up (appeals = WORRIED), NOT down (shame = wrong). Luma's FRUSTRATED gaze should go ACROSS, approximately level. In most storyboard contexts, Cosmo is at frame-right and slightly above Luma (he is taller). She should look slightly UP-RIGHT toward him — maximum about 5–8° above horizontal.
- Iris shift: both irises shifted right (toward Cosmo), with a slight upward component to match his height.
- Eye aperture: NARROWED compared to RECKLESS/ALARMED. FRUSTRATED is an internal state — the eyes compress slightly (not squint, but controlled aperture). 60–65% of maximum aperture.
- Brows: pulled inward and slightly down (corrugator). Asymmetric: left brow lower (the side facing the camera / the "leading edge of frustration").
- Mouth: compressed line or set jaw. NOT open. The voice is being controlled.
**Sight-line tool check:** eye_xy = right iris center (the eye that is dominant for this gaze direction); aim_xy = target at slightly up-right; PASS ≤ 15px.

### 4. THE NOTICING (observational stillness + slight forward lean)
**Body posture:** One arm at side, observational stillness, slight forward lean (body_tilt -2 to -3°). This is Luma's defining expression — the face of a kid who sees what no one else does.
**Gaze requirement: THIS IS THE CRITICAL CHECK.** Per the C38 staging brief and C41 v012 brief: pupils must shift RIGHT toward the implied screen subject. Centered pupils = looking at the audience. Shifted pupils = experiencing discovery. The discovery must be visible in the eye geometry, not just the brow asymmetry.
- Left eye (Luma's "wondering eye" / the one that's wider): iris shifted RIGHT by 4–6px at the canonical expression sheet scale.
- Right eye (the "apprehension eye" / the one that's slightly narrower — C38 brief): iris also shifted RIGHT, but the aperture is reduced ~3–4px from left eye. The two eyes are aimed at the same target but reporting different things about it.
- Top lid drop on right eye (THE NOTICING lid geometry, fixed in v011): confirms "focusing squint" on the apprehension side. This geometry MUST survive the v013 body posture changes — face curves integration is not an excuse to reset this.
- Brow asymmetry: left brow raised (wonder), right brow lower by 8–12px with slight inward kink (apprehension). This is the canonical THE NOTICING brow grammar.
- Slight forward lean (body_tilt -2 to -3°): the head moves forward. At the expression sheet canonical scale, this shifts the head center ~4–6px toward frame-right. The iris shift and head shift should both point in the same direction (toward the discovery subject on the right).
**Sight-line tool check:** eye_xy = left iris center; aim_xy = shifted position (frame-right, at eye level); target_xy = same. PASS = discovery target read confirmed. If centered, FAIL — this is the P2 critique issue from C38 that must not regress.

---

## How to Run the Sight-Line Check

```bash
python output/tools/LTG_TOOL_sight_line_diagnostic.py \
  --image output/characters/main/LTG_CHAR_luma_expressions.png \
  --char luma \
  --expression "THE_NOTICING" \
  --eye-xy 320 240 \
  --aim-xy 360 240 \
  --target-xy 360 240 \
  --label "luma_v013_noticing"
```

Replace `eye-xy` and `aim-xy` with actual pixel coordinates from the v013 sheet once on disk.

For batch mode (all four Tier 1 expressions), create a JSON config:
```json
[
  {"label": "RECKLESS_fwd", "eye_xy": [...], "aim_xy": [...], "target_xy": [...]},
  {"label": "ALARMED_threat", "eye_xy": [...], "aim_xy": [...], "target_xy": [...]},
  {"label": "FRUSTRATED_cosmo", "eye_xy": [...], "aim_xy": [...], "target_xy": [...]},
  {"label": "NOTICING_screen", "eye_xy": [...], "aim_xy": [...], "target_xy": [...]}
]
```
Then: `python output/tools/LTG_TOOL_sight_line_diagnostic.py --batch luma_v013_sightlines.json`

---

## Pass/Fail Criteria for v013 Sign-Off

| Expression | Required | Acceptable | Block |
|---|---|---|---|
| RECKLESS | Forward/up gaze, bilateral wide | Slight iris shift either way | Downward gaze FAIL |
| ALARMED | Both irises toward threat | 3–4px shift | Centered FAIL |
| FRUSTRATED | Level-horizontal gaze, slight up-right | 5–8° elevation | Downward FAIL |
| THE NOTICING | Iris shift RIGHT (4–6px), top-lid drop right eye | 3px minimum | Centered FAIL |

---

## Face Test Gate (mandatory per ROLE.md)

Before submitting v013, run:
```bash
python output/tools/LTG_TOOL_character_face_test.py --char luma --head-r 23
```
PASS required before delivery. WARN = include in completion report.

---

Lee Tanaka
