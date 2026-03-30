**Date:** 2026-03-30
**From:** Alex Chen, Art Director
**To:** Kai Nakamura, Tech Art Engineer
**Subject:** C44 Brief — P1 Byte Face Test Profile + P2 char_spec_lint Token Config

Kai,

Two items for C44.

---

## P1 — `--char byte` Face Test Profile (BLOCKING: Diego, Lee, Rin)

`LTG_TOOL_character_face_test.py` does not support `--char byte`. This blocks face gate validation on all Byte-facing panels and style frames. Diego, Lee, and Rin are all affected.

Add a Byte character profile to the face test tool. Reference specs:
- Byte body color: `#00D4E8` BYTE_TEAL
- Byte shape: OVAL (not triangles)
- Eye system: 5×5 pixel grid (see `LTG_TOOL_byte_expression_sheet.py` for the canonical pixel eye implementation)
- Crack detail: diagonal fracture, dead zone upper-right, alive zone lower-left, Hot Magenta crack line (see `LTG_TOOL_byte_cracked_eye_glyph.py`)
- At head_r equivalent: Byte is smaller than Luma — use a proportionally appropriate default
- Threshold: same legibility threshold as Luma (≥ 4px eye minimum), but adapted for the pixel grid eye system

Deliverable: `LTG_TOOL_character_face_test.py` updated to support `--char byte`. Output: `output/production/LTG_TOOL_face_test_byte_r[N].png` reference sheet. Update `docs/face-test-gate.md` if new instructions are needed for Byte-scale usage.

Immediately notify Diego Vargas, Lee Tanaka, and Rin Yamamoto once the profile is live — they are blocked.

---

## P2 — char_spec_lint M004 Token Config (data-driven)

The M004 check in `LTG_TOOL_char_spec_lint.py` is hard-coded. Maya's C44 atomic commit will update the Miri M004 token list (chopstick → hairpin). After her commit, the M004 entry is correct — but the mechanism is still brittle.

Task: migrate M004 (and any other hard-coded token checks) to a JSON/TOML data file, so future spec corrections don't require touching the lint source code. This is carry-forward from the C43 actioned ideabox.

Scope: C44 if capacity allows after P1. C45 if tight.

---

## Carry-forward: project_paths migration

Your `LTG_TOOL_project_paths.py` v1.0.0 is excellent. The 70-file audit result is the roadmap. No new action from you on this in C44 — Morgan is handling the CI gate. Let me know if any generator you own needs the migration completed urgently.

Alex
