**Author:** Hana Okonkwo
**Date:** 2026-03-31
**Cycle:** 52

## Idea: Per-Environment Wand Compositing Presets

### Problem
The C52 SF06 rebuild required manually specifying surface color, shadow alpha, bounce alpha, edge tint alpha, color transfer strength, blur sigma, and light source positions for the Living Room. Every style frame generator will need these same parameters per environment. This is error-prone and duplicative.

### Proposal
Create `LTG_TOOL_wand_composite_presets.py` — a dictionary of per-environment compositing configs that can be imported by any style frame or compositing script.

```python
LIVING_ROOM = {
    "surface_color": (185, 165, 125),
    "shadow_alpha": 50,
    "bounce_alpha": 20,
    "bounce_ground_color": (185, 165, 125),
    "edge_tint_alpha": 18,
    "color_transfer_strength": 0.12,
    "blur_sigma": 5.0,
    "light_sources": [
        {"color": (245, 208, 140), "x_frac": 0.12, "y_frac": 0.40, "radius": 320, "intensity": 0.18, "blend": "screen"},
        {"color": (130, 175, 160), "x_frac": 0.50, "y_frac": 0.45, "radius": 260, "intensity": 0.14, "blend": "screen"},
    ]
}
```

This pairs with the C50 character_environment_lighting_c50.md but in importable code form. One source of truth for all compositing scripts.

### Benefit
Eliminates magic numbers in style frame generators. When a critic says "bounce is too strong in the classroom," we change one number in one file.
