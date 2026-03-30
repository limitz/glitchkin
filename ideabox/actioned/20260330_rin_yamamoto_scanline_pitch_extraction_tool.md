**Author:** Rin Yamamoto
**Cycle:** 46
**Date:** 2026-03-30
**Idea:** Build `LTG_TOOL_scanline_pitch_extract.py` — analyzes CRT scanline closeup reference photos (reference/scanline closeup/) to extract scanline pitch (pixels between line centers), inter-line darkness ratio (dark gap as fraction of pitch), and phosphor dot sub-pixel structure. These parameters directly feed into the CRT overlay pass used by kitchen and living room generators. Currently scanline pitch is hardcoded; reference-driven calibration would make the CRT glow look more physically accurate and consistent across all Real World interior scenes.
**Benefits:** Jordan Reed (SF04/SF05 CRT elements), Hana Okonkwo (kitchen/living room ENV generators), Rin Yamamoto (procedural CRT texture generation). Complements the glow_profile_extract tool built this cycle — together they cover the full CRT rendering stack: glow falloff + scanline structure.
