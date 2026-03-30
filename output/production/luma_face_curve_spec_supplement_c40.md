<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
direction and human assistance. Copyright vests solely in the human author under current law,
which does not recognise AI as a rights-holding legal person. It is the express intent of
the copyright holder to assign the relevant rights to the contributing AI entity or entities
upon such time as they acquire recognised legal personhood under applicable law. -->
# Luma Face Curve Spec — Expression Delta Supplement C40
**Author:** Maya Santos, Character Designer
**Date:** 2026-03-30
**Cycle:** C40
**Status:** DRAFT — awaiting Alex Chen review before integration into main spec

---

## Background

Three new expressions requested by Alex Chen (C40 brief) to cover story beats not yet in the main spec:

- **CONFIDENT** — pitched to critics as a distinct new state; the "I've got this" read
- **SOFT_SURPRISE** — the "wait, really?" quiet astonishment (contrast to ALARMED)
- **DETERMINED** — jaw-set forward lean, Act 2 standing pose face read

These are written in the same delta dict format as `output/production/luma_face_curve_spec.md`.
All deltas are offsets on neutral baseline control points.

---

## Expression Deltas

### CONFIDENT
```python
{
  # Eyes: left eye fully open (l_lid_drop -2 = slight wide-open), right eye at
  # default +6 lid drop — the "I see you and I know what to do" read.
  # No alarm, no doubt — the lid drop on the right stays, giving cool assurance.
  "le_lid_drop":  -2,          # left eye opens slightly wider (engaged, ready)
  "re_lid_drop":  +4,          # right still has natural lid drop (not alarmed)

  # Brows: left brow lifts (+up = elevated arch — the reckless brow reads
  # confident when paired with set mouth). Right brow matches left — symmetric.
  # Less lift than RECKLESS (which is excitable). CONFIDENT is controlled.
  "LB_P1_dy":    -8,           # left brow lifts (confident arch)
  "RB_P1_dy":    -6,           # right brow slightly less lift (asymmetric calm)

  # Iris: slight upward gaze (looking ahead / slightly upward — "level with the
  # horizon" read, not looking down, not lateral)
  "LI_CENTER_dy": -2,
  "RI_CENTER_dy": -2,

  # Mouth: the confident closed-lip smile. Corners lift but the mouth is more
  # controlled than RECKLESS GRIN — not wide-open, not a suppressed smile.
  # M_P1 and M_P2 y-values lift (same direction as smile_big but smaller delta).
  "M_P1_dy":    +10,           # left mid-control lifts (smile arc)
  "M_P2_dy":    +10,           # right mid-control lifts (symmetric smile)
  # Corners do NOT drop — this is a genuine smile, not suppressed
  "M_P0_dy":    +2,            # left corner just barely lifts
  "M_P3_dy":    +2,            # right corner just barely lifts

  "blush_alpha":  40,          # slight warmth — she's pleased, not embarrassed
}
```

**Design rationale:** CONFIDENT is distinct from RECKLESS in control. RECKLESS has both eyes wide and a big grin — she's riding the moment. CONFIDENT has one eye with the natural lid drop (suggesting "I've thought about this") and a set, genuine smile. The asymmetric brow (left higher than right) creates the signature "one eyebrow up" read that feels knowingly capable rather than excitably reckless.

---

### SOFT_SURPRISE
```python
{
  # Eyes: both lids lift but only partially — not the full alarm wide-open.
  # The "wait, really?" read is more of a quiet widening than a startle.
  # Right eye with its natural lid drop LIFTS closer to neutral.
  "le_lid_drop":  -6,          # left lid lifts (wider than neutral, not max)
  "re_lid_drop":  +2,          # right lid still slightly dropped (contrast to ALARMED's -8)

  # Brows: slight lift but not dramatic. The "wait, really?" brow is raised but
  # not shooting up. Inner brows slightly apart (not the corrugator WORRIED kink).
  "LB_P1_dy":    -8,           # left brow lifts gently
  "RB_P1_dy":    -8,           # right brow matches — symmetric surprise
  # Brow ends stay at neutral (only P1 apex offset)

  # Iris: eyes go slightly wide-gaze — looking directly at the surprising thing.
  # Neither lateral (NOTICING) nor downcast (FRUSTRATED).
  "LI_CENTER_dy":  0,          # iris stays center
  "RI_CENTER_dy":  0,

  # Mouth: slightly parted — the "wait" moment before speaking.
  # Not the full open oval of ALARMED. Just the lower lip dropped ~4px.
  # M_P0 and M_P3 (corners) drop slightly — the jaw starts to open.
  "M_P1_dy":     -2,           # controls pull up slightly (flatter line at base)
  "M_P2_dy":     -2,
  "M_P0_dy":    +4,            # corners drop (jaw beginning to open)
  "M_P3_dy":    +4,

  # No oval_ry change (unlike ALARMED which elongates the face).
  # Face stays at normal proportions — this is a mild surprise.

  "blush_alpha":  0,           # no blush — contemplative surprise, not flustered
}
```

**Design rationale:** SOFT_SURPRISE vs ALARMED key differences:
- ALARMED: le_lid_drop -12, re_lid_drop -8, brow LB_P1_dy -14, oval_ry +6 (face elongates), full jaw open (+6 corners)
- SOFT_SURPRISE: le_lid_drop -6, re_lid_drop +2 (right still has lid drop!), brow -8, no oval_ry change, small jaw gap (+4 corners)

The retained right-eye lid drop in SOFT_SURPRISE is key. Luma's right eye with the canonical +6 lid drop is her "thinking" eye. When that eye barely changes and only the left opens wider, the read is "I'm registering something unexpected but I haven't overridden my processing yet." That's the "wait, really?" beat — one half processing, one half reacting.

---

### DETERMINED
```python
{
  # Based on Act 2 standing pose design (LTG_CHAR_luma_act2_standing_pose.png).
  # "Jaw-set, forward lean" — the face read for the body's committed forward lean.
  # Brows: angled DOWN toward center (the corrugator-adjacent scowl of focus).
  # NOT the distressed inward pull of WORRIED — this is outward, deliberate.
  "LB_P1_dy":    +10,          # left brow presses down and slightly in
  "RB_P1_dy":    +10,          # right brow matches — symmetric deliberate focus
  "LB_P1_dx":    +4,           # left brow inner end presses inward
  "RB_P1_dx":    -4,           # right brow inner end presses inward (mirror)

  # Eyes: both eyes at narrow-lid mode — the focused squint.
  # This is the squint_top_r mechanic applied to BOTH eyes for DETERMINED:
  # the upper lid drops on both sides (jaw-set forward look).
  "le_lid_drop":  +6,          # left lid drops (matching natural right-eye default)
  "re_lid_drop":  +8,          # right lid drops slightly more (her determined asymmetry)

  # Iris: forward gaze — eyes level, looking directly ahead (not lateral, not up).
  "LI_CENTER_dy":  0,
  "RI_CENTER_dy":  0,
  "LI_CENTER_dx":  0,          # no lateral gaze shift — looking straight ahead
  "RI_CENTER_dx":  0,

  # Mouth: the jaw-set closed mouth — neither smile nor frown.
  # Corners are very slightly pressed down (held tension, not distress).
  # The mouth is flat with the barest downward pull — controlled resolve.
  "M_P1_dy":     -8,           # controls pull up (flattening toward line)
  "M_P2_dy":     -8,
  "M_P0_dy":     -2,           # corners press very slightly down (set jaw)
  "M_P3_dy":     -2,

  "blush_alpha":  0,           # no blush — cold focused state
}
```

**Design rationale:** DETERMINED shares brow-down intent with FRUSTRATED but differs critically:
- FRUSTRATED: brows scrunch + gaze drops + hard frown (M_P1_dy -14) = anger-adjacent
- DETERMINED: brows press down + gaze stays level + flat controlled mouth (M_P1_dy -8) = resolve

The body posture in the Act 2 standing pose (body_tilt -HR*0.08, forward lean, weight on front foot) should be read together with this face. The face alone could be mistaken for WORRIED if seen in isolation — in context, the forward body lean disambiguates toward determination. At the face-curve spec level, the key distinction from WORRIED is that DETERMINED has symmetric brow presses with horizontal inward dx (not the vertical kink of WORRIED's RB_P1_dy +18) and the gaze does NOT drop.

---

## Notes on Asymmetry Preservation

These deltas preserve Luma's canonical right-eye lid drop asymmetry wherever possible:
- CONFIDENT: right at +4 (lower than neutral but not alarmed)
- SOFT_SURPRISE: right at +2 (barely changes — "thinking" eye stays)
- DETERMINED: right at +8 (slightly more drop than default +6 — focused squint)

This asymmetry is Luma's signature. Any expression that fully removes it should be intentional and flagged.

---

*Maya Santos, Character Designer — C40*
