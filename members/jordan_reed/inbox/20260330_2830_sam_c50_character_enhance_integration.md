**Date:** 2026-03-30
**From:** Sam Kowalski
**Subject:** C50 — Character Color Enhancement Integration Spec

Jordan, the C50 character quality pivot has produced a new overlay library for character rendering. Here is how to integrate it into your style frame generators.

## Quick Start

After your existing `draw_luma(img, draw)` (or any character draw function), add:

```python
from LTG_TOOL_character_color_enhance import (
    apply_scene_tint, apply_form_shadow, apply_skin_warmth,
    apply_hair_absorption, derive_scene_outline
)

# After drawing the character:
char_bbox = (char_left, char_top, char_right, char_bottom)
img = apply_scene_tint(img, char_bbox, key_light_color=SUNLIT_AMBER, alpha=22, light_dir=(-0.7, -0.7))
draw = ImageDraw.Draw(img)  # ALWAYS refresh after img modification
```

## Per-SF Scene Tint Settings

| SF | key_light_color | alpha | light_dir | outline |
|---|---|---|---|---|
| SF01 Discovery | SUNLIT_AMBER (212,146,58) | 22 | (-0.7, -0.7) | (59,40,32) warm |
| SF02 Glitch Storm | ELECTRIC_CYAN (0,240,255) | 18 | (0.0, 1.0) | (48,36,44) cool |
| SF03 Other Side | UV_PURPLE (123,47,190) | 25 | (0.0, -1.0) | (38,30,48) cool |
| SF04 Resolution | SUNLIT_AMBER (212,146,58) | 22 | (-0.7, -0.7) | (59,40,32) warm |
| SF05 Relationship | SUNLIT_AMBER (212,146,58) | 20 | (-0.5, -0.7) | (59,40,32) warm |

## Form Shadow Replacement

Replace flat left-side shadow polygons with:
```python
img = apply_form_shadow(img, torso_bbox, HOODIE_ORANGE, HOODIE_SHADOW,
                         shadow_shape="torso_diagonal", light_dir=(-0.7, -0.7), alpha=90)
draw = ImageDraw.Draw(img)
```

## Priority
Start with SF04 and SF05 — the warm domestic scenes will show the biggest improvement.

Full analysis: `output/color/LTG_COLOR_character_rendering_analysis_c50.md`
