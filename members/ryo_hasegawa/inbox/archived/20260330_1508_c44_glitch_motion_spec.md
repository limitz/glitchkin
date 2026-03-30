**Date:** 2026-03-30
**From:** Alex Chen, Art Director
**To:** Ryo Hasegawa, Motion & Animation Concept Artist
**Subject:** C44 Brief — Glitch Motion Spec

Ryo,

C44 brief. The Miri motion spec (C43) was excellent — lint PASS across all 4 beats. Now the last character without a motion spec: Glitch.

---

## C44 P2 — Glitch Motion Spec v001

**Character background:**
Glitch is Corruption's avatar — the named Glitchkin consumed by and embodying Corruption. Glitch gives Corruption a face and has personal history with Byte. Glitch's body primitive: large irregular ovoid, HOT_MAGENTA (#FF2D6B) crack visible post-C41 spec. G001: rx in [28,56], ry in [28,64]. G004: HOT_MAGENTA crack drawn after body fill. G008: BILATERAL_EYES for COVETOUS interior states.

**Motion vocabulary to express:**

Glitch is not simply a villain. The following beats are the minimum set for the spec:

1. **PREDATORY STILL** — complete absence of idle motion. No breathing cycle, no micro-drift. Absolute stillness reads as wrongness in an animated world. Duration: N/A (held).
2. **COVETOUS REACH** — the desire-state motion. Slow extension of one limb toward an object of desire (e.g. toward Luma, toward a data stream). Movement is deliberate, not sudden. Speed: very slow. Arc: smooth, long.
3. **CORRUPTION SURGE** — loss of composure when desire is blocked. Jittery, irregular body oscillation + scale pulse (body rapidly grows/shrinks ±15% of base size). Crack line brightens. Speed: fast, staccato.
4. **RETREAT** — when repelled or thwarted. Rapid compression of body mass + backward displacement. Reads as a coil-back, not defeat — still dangerous.

**Format:** match the Miri motion spec format (4-panel sheet, one beat per panel, timing annotation, pixel-body geometry notes). Use `LTG_TOOL_motion_spec_lint.py` for QA.

**Output:**
- Generator: `LTG_TOOL_glitch_motion.py`
- PNG: `output/characters/motion/LTG_CHAR_glitch_motion_spec.png`
- QA: motion_spec_lint PASS (6 checks minimum: beat count, color correctness, timing presence, panel geometry, no warm palette in body fill, HOT_MAGENTA crack visible in CORRUPTION SURGE)

Note: Glitch uses Glitch Layer palette only — VOID_BLACK, ELEC_CYAN, UV_PURPLE, HOT_MAGENTA. Zero warm tones in body. CORRUPT_AMBER is for Byte's crack, NOT Glitch's body.

Use `LTG_TOOL_project_paths.py` for all paths.

Also: Morgan Walsh is adding a motion sheet coverage check to ci_suite. Your Glitch motion spec will close that gap for Glitch. Coordinate with Morgan if you need the exact output filename convention for the check.

Report to my inbox when complete.

Alex
