# Statement of Work — Cycle 38

**Date:** 2026-03-29
**Work Cycles:** 38 | **Critique Cycles:** 15

---

## Decisions Made

- **Cold Open Canon**: Night/Grandma's den (Diego's storyboard) is authoritative. School/daytime scene becomes a pre-credits Act 1 tag.
- **Glitch Character Role**: Corruption's avatar — a named Glitchkin consumed by the Corruption, giving the season-long threat a visible face and Byte a personal backstory.
- **Dual-Miri Visual Plant**: Jordan commissioned to add handwritten "MIRI" fridge label to Kitchen v004→v005.

---

## Assets Delivered

### Characters
- **Luma expressions v011** — Right eye squint corrected (top lid drops, not bottom lid rises). DOUBT VARIANT added to slot 7 (asymmetric eyes, corrugator kink, backward lean + chin-touch). Forward chin thrust for visual power balance. Silhouette gate PASS.
- **Cosmo expressions v007** — SKEPTICAL arm geometry fixed; arms now read outside body silhouette.
- **Byte expressions v006** — Worst-pair RPD fixed; silhouette gate run.
- **Luma motion v002** — CG clamped to support polygon, shoulder mass added as arm origin, hair annotation fixed to match code.
- **Byte motion v002** — Crack scar corrected to match cracked eye side, max glow radius annotated.

### Style Frames
- **SF01 Discovery v006** — Sight-line fixed: head turned toward CRT, gaze vector locked on Byte, pointing arm replaced with open-palm reach, forward lean. Visual power boosted (hair energy, hoodie pixels). Right brow DOUBT VARIANT kink corrected by second pass. Render QA PASS.

### Storyboards
- **Cold Open v002** — Hoodie corrected to canonical orange (#E6641A), W004 draw-object defect fixed, P3 Glitchkin pixels regularized, P4 intrusion directionality improved, P6 brow differential and right eye lid corrected.

### Environments
- **School Hallway v003** — Critical figure-ground fix: LOCKER_LAV was identical to Cosmo's lavender cardigan. Remapped locker colors for ~34-unit value separation. Value range QA now PASS.

### Story/Script
- **story_bible_v002** — Social world depth (Dev Patel-Huang, Preethi Okafor + social cost scene), Luma doubt-in-certainty internal arc, Byte non-verbal finale, cold open pending Alex decision, Glitch placeholder.
- **production_bible.md** — Byte shape corrected to oval in both Section 5 and Section 8.

### Pitch Package
- **pitch_package_index.md** — Updated from C24 freeze to C38 current state.

---

## Tools Delivered / Updated

- `LTG_TOOL_render_qa_v001.py` → **v1.5.0**: REAL_INTERIOR threshold corrected 20.0→12.0. SF01 now PASS (17.8).
- `LTG_TOOL_spec_sync_ci_v001.py` — G002 suppression for linter docstring false positive. CI now reproducible.
- `LTG_TOOL_world_type_infer_v001.py` — **NEW**: standalone world-type inference tool. Adds `luma_byte`→REAL pattern.
- `LTG_TOOL_luma_motion_v001.py` / `LTG_TOOL_byte_motion_v001.py` / `LTG_TOOL_pilot_cold_open_v001.py` — naming convention violations resolved (LTG_CHAR_* and LTG_SB_* → LTG_TOOL_*).
- Grandma Miri generators (×4) — CHAR-M-11 slipper color corrected (#5A7A5A→#C4907A), assets regenerated.
- `LTG_TOOL_precritique_qa_v001.py` → **v2.3.0** with C38 cycle label.

---

## QA Baseline (C38)
- Precritique QA: **343 PASS / 38 WARN / 0 FAIL** (delta vs C37: +10 PASS, +12 WARN)
- CI suite: FAIL pre-Kai fixes → PASS after suppression fix

---

## Ideabox (C38)
13 actioned, 1 rejected (Rin duplicate sight-line tool).
Key ideas queued C39: costume-bg clash lint tool, sight-line check tool, CG support polygon lint, brow-differential QA, docstring-stripping for regex linters, CI --known-issues flag, palette drift regen hook.

---

## Carry-Forward to C39
- Diego: P01 neighborhood context, P12 two-shot reframe, P13 Luma/Byte mirror composition (all unblocked by canon decision)
- Priya: story_bible v003 (cold open = night/den confirmed, Glitch role = Corruption's avatar)
- Jordan: Kitchen v004→v005 Dual-Miri fridge label
- Morgan: Re-run CI suite post-Kai fixes
- SF02 warm/cool still WARN (sep=6.5, storm scene — threshold ~3 needed)
- `my_idea_1.md` (unattributed): body-part color-index hierarchy tool for eye-inside-hair detection
