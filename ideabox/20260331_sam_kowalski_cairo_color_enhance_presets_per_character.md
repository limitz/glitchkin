# Idea: Per-character color enhancement presets

**From:** Sam Kowalski
**Date:** 2026-03-31
**Type:** Pipeline improvement

## Problem
The color enhancement pipeline (LTG_TOOL_character_color_enhance.py) currently requires callers to pass character-specific skin/shadow/highlight values manually. Every expression sheet and style frame generator must know the correct CHAR-C/CHAR-L/CHAR-M values.

## Proposal
Add a `CHARACTER_PRESETS` dict to `character_color_enhance.py` that maps character names to their palette values:

```python
CHARACTER_PRESETS = {
    "luma": {"skin_base": (200, 136, 90), "skin_hl": (232, 184, 136), ...},
    "cosmo": {"skin_base": (217, 192, 154), "skin_hl": (238, 212, 176), ...},
    "miri": {"skin_base": (140, 84, 48), "skin_hl": (192, 142, 96), ...},
}
```

Then `enhance_from_cairo(surface, ..., character="cosmo", scene="warm_domestic")` resolves all colors automatically. Eliminates copy errors between generators and centralizes palette values in one place alongside the enhancement logic.

## Benefit
Reduces error surface when building new expression sheets or integrating characters into style frames. One source of truth for per-character color enhancement parameters.
