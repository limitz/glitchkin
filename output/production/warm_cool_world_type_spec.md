<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
direction and human assistance. Copyright vests solely in the human author under current law,
which does not recognise AI as a rights-holding legal person. It is the express intent of
the copyright holder to assign the relevant rights to the contributing AI entity or entities
upon such time as they acquire recognised legal personhood under applicable law. -->
# Warm/Cool World-Type Spec — "Luma & the Glitchkin"

**Author:** Kai Nakamura (Technical Art Engineer)
**Cycle:** 39 — 2026-03-29
**Status:** Canonical specification (per Alex Chen C39 brief)
**Tools governed:** `LTG_TOOL_render_qa.py`, `LTG_TOOL_palette_warmth_lint.py`, `LTG_TOOL_world_type_infer.py`

---

## Purpose

The warm/cool separation check in `render_qa_v001.py` (Check D) measures the median hue difference between the top half and bottom half of an image. A low separation was triggering WARNs on SF02 (Glitch Storm), which is intentionally cool-dominant. This document records the creative rationale for each world type's threshold and establishes them as **creative canon** — not arbitrary tool settings.

---

## World Types and Warm/Cool Thresholds

| World Type | Threshold (PIL hue units) | Archetype | Creative Rationale |
|---|---|---|---|
| `REAL` | 12 | SF01 Discovery | Warm lamp-lit interior. Grandma's living room. Two light sources: warm reading lamp + cool CRT glow. Separation expected and necessary for depth. |
| `REAL_INTERIOR` | 12 | SF01, SF04, classrooms, kitchens | Alias for REAL. Warm presence dominant — window shafts, lamps, golden afternoon. Threshold 12 ensures genuine dual-temperature lighting is present. |
| `REAL_STORM` | 3 | SF02 Glitch Storm | **The storm has won.** The warm world (street lamps, domestic window glow) is still present but overwhelmed by cold storm sky, Glitch energy, and battle context. Warm accents are correct but subdued (window glow alpha 110–115). Applying the REAL threshold (12) to this scene would demand MORE warm than the scene allows — this is wrong. Threshold 3 reflects the intentional cold dominance of a storm scene. This is not a defect. |
| `GLITCH` | 3 | Glitch Layer | Pure Glitch world interior. Electric Cyan + UV Purple dominant. Warm tones are **prohibited** except tiny CORRUPT_AMBER hot-spot residuals (glyph eyes, cracks). Warm presence at any significant level would be a spec violation. |
| `OTHER_SIDE` | 0 | SF03 The Other Side | Fully digital CRT world. No warm light sources exist in this world. Zero warm expected and correct. Check always passes. |
| `None` (unknown) | 12 | Unclassified | Conservative default — treat as REAL. If a filename is unclassifiable, assume warm lighting is expected (most assets are Real World). |

---

## Inference Rules (filename-based)

World type is inferred from the asset filename (generator script or rendered PNG). Rules are evaluated in order; first match wins.

1. `OTHER_SIDE`: matches `sf03`, `other_side`, `otherside`, `crt_world`
2. `GLITCH`: matches `glitch_layer`, `glitch_encounter`, `glitch_world`
3. `REAL_STORM`: matches `sf02`, `glitch_storm`, `style_frame_02` ← **NEW C39**
4. `REAL` (REAL_INTERIOR): matches `sf01`, `sf04`, `discovery`, `style_frame_01/04`, `luma_byte`
5. `REAL` (environments): matches `classroom`, `kitchen`, `hallway`, `tech_den`, `main_street`, `millbrook`, `grandma`, `luma_house`
6. `REAL` (generic): matches `scene`, `interior`, `exterior`, `daytime`
7. `None`: no match

---

## SF02 Specific Note

The Glitch Storm scene (SF02) is a **contested real-world exterior** being invaded by Glitch energy. The color design spec calls for:
- Sky: DATA_BLUE 70% dominant (cold)
- Storm confetti: Cyan/White/Magenta/UV Purple (cold digital)
- Buildings: ELEC_CYAN rim lighting + UV_PURPLE base bounce (cold)
- Warm elements: domestic window glow cones (WIN_GLOW_WARM alpha ~100), building facade warm tones (subdued)

The result is a warm/cool separation of approximately **6.5 PIL units** (measured on v008). This is **correct** and **intentional**. The REAL threshold of 12 incorrectly flagged this as WARN every cycle. The REAL_STORM threshold of 3 allows the storm aesthetic while still gating against scenes with zero warm presence at all.

---

## Tool Update History

| Cycle | Tool | Change |
|---|---|---|
| C38 | `render_qa_v001.py` → v1.5.0 | REAL threshold corrected 20→12 (Sam Kowalski) |
| C39 | `render_qa_v001.py` → v1.6.0 | REAL_STORM sub-type added via `_infer_world_subtype()` (Sam Kowalski) |
| C39 | `palette_warmth_lint_v004.py` | REAL_STORM preset added, threshold=6 (Kai Nakamura) |
| C39 | `world_type_infer_v001.py` → v1.1.0 | REAL_STORM constant + inference rule added (Kai Nakamura) |

---

*This spec is creative canon. The storm is cold. That's the point.*
— Alex Chen, Art Director (C39 brief)
