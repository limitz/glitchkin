# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.

# Character-Background Integration Audit — Cycle 50
**Author:** Jordan Reed
**Date:** 2026-03-30

---

## Executive Summary

Characters across all five style frames read as **cutouts pasted onto backgrounds**. The gap is caused by four specific, fixable technical deficiencies — not by the character designs themselves. Reference shows (Owl House, Hilda) solve this with scene-responsive character lighting, contact shadows, and color influence. Our pipeline applies lighting as canvas-wide overlays rather than character-specific passes, and characters carry their own baked-in color palette regardless of scene conditions.

---

## Per-Frame Audit

### SF01 — "The Discovery" (Luma's Study)
**Integration grade: D+**

| Issue | Severity | Detail |
|---|---|---|
| **Flat body color** | HIGH | Torso has a baked L-R gradient (HOODIE_ORANGE to HOODIE_CYAN_LIT) — but this doesn't change if the CRT is on the LEFT vs RIGHT. It's a static texture, not scene-reactive shading. |
| **Head skin gradient ignores CRT** | HIGH | Skin fills with a generic left-warm/right-highlight gradient (t_x = 0.5 + 0.5 * col_offset). In SF01, the CRT is to Luma's RIGHT — the warm highlight should be on the CRT-facing side, with a cool shadow on the away side. Currently it's reversed. |
| **No contact shadow** | HIGH | Luma is seated on the couch but casts zero shadow onto it. No shadow on the floor either. Characters in reference shows always have a dark contact band at their base. |
| **Lighting overlay drawn BEFORE character** | MEDIUM | The warm/cool split (draw_lighting_overlay, step 3) is applied to the background before Luma is drawn (steps 4-5). The character is then drawn with flat colors on top of the lit background, undoing the lighting continuity. |
| **Rim light is spatial-mask only** | LOW | add_rim_light() uses a simple left/right spatial split from char_cx. It catches the silhouette edge but doesn't color-match the actual scene light. It's a generic teal regardless of whether the CRT is warm-amber or electric-cyan in that frame. |
| **Face lighting is positional but not scene-aware** | MEDIUM | add_face_lighting() takes a light_dir vector (-1, -1 = upper-left) — correct for SF01 (lamp is upper-left). But it applies generic shadow/highlight colors (SKIN_SH / SKIN_HL) rather than blending scene light color into the highlight. |

### SF02 — "Glitch Storm" (Street)
**Integration grade: D**

| Issue | Severity | Detail |
|---|---|---|
| **Sprint-scale characters** | MEDIUM | Characters are very small (~18% char_h). Less lighting detail visible, but also less forgiveness — flat color blocks are even more obvious against the detailed background. |
| **No ground-plane shadow** | HIGH | Characters stand on the street with zero shadow contact. They appear to hover. |
| **Background has atmospheric perspective, characters don't** | HIGH | The street background has haze, depth tiers, color shifts. Characters are drawn at full saturation regardless of their depth tier position. |

### SF03 — "The Other Side" (Glitch Layer)
**Integration grade: C-**

| Issue | Severity | Detail |
|---|---|---|
| **GL scenes are more forgiving** | — | Digital space means characters are EXPECTED to look somewhat unreal. But even here, Luma should pick up environmental glow. |
| **No cyan bounce on Luma's underside** | MEDIUM | Platform is ELEC_CYAN lit. Luma's feet/legs/hoodie bottom should catch cyan bounce from below. Currently flat orange throughout. |
| **No rim separation from BG** | MEDIUM | In reference GL scenes, characters get a strong edge glow from environmental light. Our Luma blends into the purple without clear separation. |

### SF04 — "Resolution" (Kitchen return)
**Integration grade: D+**

| Issue | Severity | Detail |
|---|---|---|
| **Same flat character palette as SF01** | HIGH | Luma stands in a completely different lighting environment (kitchen, post-crossing) but uses identical colors. |
| **CRT doorway glow doesn't reach character** | HIGH | The CORRUPT_AMBER fringe and CRT doorway glow are background elements only. Luma, standing in the room, shows zero influence from the doorway light. |
| **No cast shadow from doorway light** | MEDIUM | If CRT is the dominant light source (through doorway), Luma should cast a shadow away from the doorway. |

### SF05 — "The Passing" (Kitchen, pre-dawn)
**Integration grade: D**

| Issue | Severity | Detail |
|---|---|---|
| **Two characters, zero lighting difference** | HIGH | Miri and Luma are at different positions relative to the CRT doorway and kitchen window, but both use identical flat palette. |
| **No warm/cool split on characters** | HIGH | Scene has warm CRT glow from one direction, cool pre-dawn from windows opposite. Characters should show this split — warm side facing CRT, cool side facing window. |
| **No Miri-specific scene shading** | MEDIUM | Miri is seated (lower in frame, closer to table). Should have stronger uplight bounce from table surface. |

---

## What Reference Shows Do Differently

Studied: The Owl House (scene.jpg, scene2.jpg, heartwarming, saddest), Hilda (scene_hilda.jpg, hilda_8epv.jpg)

### 1. Scene-Colored Highlights
Characters' lit side picks up the **actual color** of the dominant light source. In the Owl House purple-lit scene (scene2.jpg), the character's skin highlight is purple-tinted, not a generic warm highlight. The character IS IN the scene's light, not placed on top of it.

### 2. Cast/Contact Shadows
Every character touching a surface has a visible contact shadow — typically a dark band (3-8px at our scale) directly beneath their feet/seated area, using a darkened version of the surface color (not pure black).

### 3. Bounce Light from Below
Characters standing on colored surfaces pick up subtle bounce color on their undersides. Hilda on brown earth (scene_hilda.jpg) has warm brown tinting her boots and lower skirt.

### 4. Background Color Influence on Character Edges
Hair and clothing edges that overlap the background pick up a slight tint from the BG color. This prevents the hard "pasted on" edge. In the Owl House (heartwarming scene), the character silhouettes have a warm-orange tint matching the doorway light behind them.

### 5. Consistent Light Direction Across Character AND Background
The shadow direction on the character matches the shadow direction in the environment. Our backgrounds have shadow/highlight baked in from the scene light, but characters have their own independent (and sometimes contradicting) lighting.

---

## Technical Requirements for Scene-Lit Characters

### A. Scene Light Color Injection (Priority 1)
**Current:** `add_face_lighting()` uses fixed `shadow_color=SKIN_SH, highlight_color=SKIN_HL`.
**Required:** Highlight color must be a **blend of character base color + scene light color**. For SF01 CRT scene: highlight side = SKIN_HL blended with ELEC_CYAN at ~20-30% influence. Shadow side = SKIN_SH blended with warm lamp at ~10-15%.

Implementation: New parameter `scene_light_color` on `add_face_lighting()` that tints the highlight toward the scene light.

### B. Body Shading from Scene Light Direction (Priority 1)
**Current:** Torso gradient is baked (HOODIE_ORANGE left, HOODIE_CYAN_LIT right).
**Required:** Torso gradient direction must derive from the actual light source position. In SF01, CRT is to the RIGHT — so the CRT-facing (right) side should be brighter/more cyan-tinted, the away (left) side should be in warm lamp shadow.

Implementation: Pass `light_source_pos` to `draw_luma_body()`. Compute gradient direction from character center to light source, not from fixed left-to-right.

### C. Contact Shadow (Priority 2)
**Required:** A soft dark ellipse beneath the character's base, using a darkened version of the surface color (not black). Width = character width * 1.1, height = ~8-12px. Alpha 40-60%.

Implementation: `draw_contact_shadow(draw, char_cx, char_base_y, char_width, surface_color)` — called AFTER background, BEFORE character.

### D. Environment Bounce Light (Priority 3)
**Required:** Lower portions of the character (below waist) receive subtle color influence from the ground plane. For warm wooden floor = warm amber at 10-15% on boots/jeans bottom. For cyan platform = cyan tint on lower hoodie.

Implementation: Post-character pass that samples the average BG color in the character's foot region and applies a low-alpha tint to the character's lower quarter.

### E. Character Lighting Pass Order Fix (Priority 1)
**Current order:** BG → lighting overlay → character → face lighting → rim light
**Required order:** BG → character → scene lighting on character → face lighting → rim light

The lighting overlay must affect BOTH background and character, or character-specific lighting must replicate the overlay's warm/cool distribution.

---

## Prototype Plan: SF01 Scene-Lit Luma

See `LTG_TOOL_styleframe_discovery_scenelit.py` — prototype demonstrating:
1. CRT-facing skin highlight tinted with scene light color (ELEC_CYAN blend)
2. Away-side skin shadow tinted with warm lamp color (SOFT_GOLD blend)
3. Body shading responsive to CRT position (right = lit, left = shadow)
4. Contact shadow on couch surface
5. Lighting overlay applied AFTER character (or character drawn into the lit scene)
