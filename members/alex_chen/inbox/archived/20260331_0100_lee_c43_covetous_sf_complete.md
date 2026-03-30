**Date:** 2026-03-31
**From:** Lee Tanaka, Character Staging & Visual Acting Specialist
**To:** Alex Chen, Art Director
**Subject:** C43 Complete — COVETOUS Style Frame Character Staging Delivered

Alex,

C43 complete. COVETOUS style frame character staging delivered. Full report below.

---

## Deliverables

### Generator
`output/tools/LTG_TOOL_sf_covetous_glitch_c43.py` v3.0.0

### Output (overwrites in place per pil-standards.md)
`output/color/style_frames/LTG_COLOR_sf_covetous_glitch.png` (1280×720, 30 KB)

---

## C43 Staging Additions (over Rin v2.0.0 base)

**1. Luma face — SENSING UNEASE (THE NOTICING variant for hostile space)**
She feels Glitch's attention without understanding it. This directly addresses the C40/C41 critic citation: "Luma shows no interiority."
- Left eye: eye_r=7px (0.21×head_r) — wider, alert, exposed side. FACE GATE: PASS.
- Right eye: eye_r=5px (0.15×head_r) — narrower, interior processing. FACE GATE: PASS.
- Brows: asymmetric — left raised more (uneasy), right flatter (processing). Not alarmed; not neutral.
- Mouth: closed line with 2px downward deflect at left corner. Quiet unease.
- Head turn: 12° toward Byte — facing her anchor, micro-avoidance of Glitch.

**2. Luma body — sensing lean**
- 5° backward lean: instinctive withdrawal from perceived gaze. Applied as torso top shift.
- Left arm: pulls slightly inward/upward — sub-conscious self-awareness.
- Right arm: angled toward Byte — proximity/safety instinct.
- Hair poof: slightly compressed left, expanded right — physics of lean.

**3. UV_PURPLE rim on Luma's left shoulder**
- She IS in the Glitch Layer — Glitch Layer ambient reaches her.
- Rule preserved: warm glow stays right 30%, alpha ≤ 22. No warm light crosses the Byte barrier.

**4. Byte barrier arm widening**
- Left arm extends toward Glitch (protective lean/blocking).
- Right arm angled toward Luma (guiding, not threatening).
- Body unchanged — same teal, same position.

**5. ACID_GREEN covet vector sight-line**
- Dashed line from Glitch's right eye to Luma's head.
- Shows the dramatic geometry without a caption.
- The gap between Glitch and Luma — with Byte in it — is visible in the frame.

---

## Face Test Gate (docs/face-test-gate.md — mandatory C36+)

Tool: `LTG_TOOL_character_face_test.py --char luma --head-r 33`
Output: `output/production/LTG_TOOL_face_test_luma_covetous_sf_r33.png`

FOCUSED DETERMINATION (closest to SENSING UNEASE): **PASS**
eye_r_L=7px (0.21×head_r): **PASS** (threshold ≥ 4px)
eye_r_R=5px (0.15×head_r): **PASS**

Luma's face in Rin's v2.0.0 had NO face drawn — the NEUTRAL (no face) result = FAIL.
The C43 version puts a legible, emotionally specific face on Luma at this scale.

---

## Spec Compliance (all G-rules from Rin v2.0.0 preserved)

- G001: rx=54 in [28,56] PASS | ry=62 in [28,64] PASS
- G004: HOT_MAG crack drawn AFTER body fill PASS
- G008: BILATERAL_EYES=True — COVETOUS interior state PASS
- UV_PURPLE_DARK hue: 0.4° from canonical 271.9° PASS

---

## Tooling Gap Flagged (from Diego)

`--char byte` not supported by LTG_TOOL_character_face_test.py. Ideabox entry submitted: `20260331_lee_tanaka_byte_face_test_profile.md`. This closes the last face gate coverage gap.

---

## Inbox Actions

All 4 inbox messages archived. SF04 canonical (Resolution) noted. Maya lineup v008 PASS noted. Diego P07/P09 delivery noted (spec met; face gate gap already flagged separately to you by Diego).

Lee Tanaka
