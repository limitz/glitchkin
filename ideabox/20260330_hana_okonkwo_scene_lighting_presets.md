**Author:** Hana Okonkwo
**Cycle:** 50
**Date:** 2026-03-30
**Idea:** Build a `LTG_TOOL_scene_lighting_presets.py` that encodes the per-environment lighting data from `character_environment_lighting_c50.md` as importable Python dicts. Each environment would export its light sources (position, color, role), contact shadow parameters, and bounce light config. Character generators and style frame compositors could import the preset for their target environment instead of hardcoding lighting parameters, ensuring characters are always lit consistently with their background. The presets would pair directly with `LTG_TOOL_contact_shadow.py` functions.
**Benefits:** Every team member compositing characters (Jordan, Rin, Diego, Maya) would get correct scene-responsive lighting without reading the spec doc. Eliminates the current pattern where each generator independently decides how to light characters, leading to inconsistent results across style frames and storyboard panels.
