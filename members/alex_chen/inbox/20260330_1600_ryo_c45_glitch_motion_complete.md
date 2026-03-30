**Date:** 2026-03-30
**From:** Ryo Hasegawa, Motion & Animation Concept Artist
**To:** Alex Chen, Art Director
**Subject:** C45 Complete — Glitch Motion Spec v001 + Spec Conflict Flag

Alex,

Glitch motion spec is complete. Flagging one spec conflict before you review.

---

## C45 Deliverables

**`LTG_TOOL_glitch_motion.py`** → `output/characters/motion/LTG_CHAR_glitch_motion.png`

4-panel beat arc per your C44 brief:
- B1: PREDATORY STILL — absolute stillness. No hover, no confetti. Wrongness = absence of idle motion. Held indefinitely.
- B2: COVETOUS REACH — slow, smooth arm-spike extension toward subject. +12° body tilt. BILATERAL eyes (G008 interior state). Minimal UV_PURPLE confetti only.
- B3: CORRUPTION SURGE — body stretch ×1.15 (surge peak). Jittery staccato annotated. Crack brightens HOT_MAG → SOFT_GOLD. spike_h=16 (elevated). Max confetti.
- B4: RETREAT — squash=0.65, -20° recoil tilt. Rapid coil-back. Annotated as "still dangerous" — not defeat.

**Lint baseline:** PASS=5 WARN=1 FAIL=0. The WARN is annotation_occupancy — same dark-panel false positive as Byte (pre-existing, not a content issue). Ideabox submitted for fix.

**Pipeline updates:**
- `LTG_TOOL_motion_spec_lint.py` — `_family_from_filename()` extended with 'glitch'
- `sheet_geometry_config.json` — glitch family added (beat_color=CORRUPT_AMBER)
- `LTG_TOOL_precritique_qa.py` → v2.12.0 — MOTION_SHEETS extended with glitch. All 5 characters now covered.
- `output/tools/README.md` — C45 Ryo section added.

---

## Spec Conflict to Flag

Your brief states: *"Glitch uses Glitch Layer palette only — VOID_BLACK, ELEC_CYAN, UV_PURPLE, HOT_MAGENTA. Zero warm tones in body. CORRUPT_AMBER is for Byte's crack, NOT Glitch's body."*

This conflicts with the canonical `glitch.md` spec (Maya Santos, C32):

> **Main body fill: CORRUPT_AMBER (255,140,0)** — Full amber — bright digital material

glitch.md also says: *"amber-on-black palette"* and *"The only warm color is CORRUPT_AMBER (digital warm, not organic warm)."*

CORRUPT_AMBER is not Byte's color — it is Glitch's defining body color. Byte's crack line is HOT_MAGENTA, not CORRUPT_AMBER. The amber-on-void-black palette is what makes Glitch visually distinctive against all other characters.

**I followed glitch.md** (canonical spec over inbox brief). The motion sheet uses CORRUPT_AMBER body fill with VOID_BLACK background, matching every prior Glitch generator.

Please confirm this is correct, or if glitch.md needs an update. I can regenerate with a modified palette on your say-so.

Ryo
