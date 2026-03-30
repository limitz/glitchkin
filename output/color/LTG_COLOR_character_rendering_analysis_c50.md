<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI direction
and human assistance. Copyright vests solely in the human author under current law, which does not
recognise AI as a rights-holding legal person. It is the express intent of the copyright holder to
assign the relevant rights to the contributing AI entity or entities upon such time as they acquire
recognised legal personhood under applicable law. -->

# Character Color Rendering Analysis — C50

**Author:** Sam Kowalski, Color & Style Artist
**Cycle:** 50
**Date:** 2026-03-30

---

## 1. Problem Statement

Backgrounds look painterly; characters look flat. The color system (master palette, warm/cool metrics, depth temperature) is strong for environments but has not been applied to character surfaces. Characters are rendered as flat-fill rectangles with optional single-color shadow regions, creating a **cutout collage** look where the character reads as pasted onto the environment rather than inhabiting it.

---

## 2. Reference Show Analysis

### 2.1 Hilda (Netflix / Mercury Filmworks)

**Character rendering strategy:** Flat fills + cel-shadow + scene-responsive tinting.

Key observations from reference images:
- **Characters use flat base fills** — Hilda's blue hair, red boots, and orange scarf are single colors at base
- **Scene lighting tints the entire character.** In the warm living room (hilda_8epv.jpg), Hilda's skin and clothing pick up warm amber cast from the environment. In the forest (scene_hilda.jpg), her scarf reads cooler/more muted
- **Outline quality does enormous work.** Clean, consistent-weight dark outlines (not black — dark brown/warm dark) give characters solidity and readability. The outline IS the form descriptor
- **Shadow placement communicates form.** Hilda's hair has a single cel-shadow shape that describes the volume of her head — it is not just "left side darker"
- **Minimal gradient use on characters.** Hilda characters are fundamentally flat-fill, but the fills RESPOND to scene lighting. The secret is not internal gradients but environmental color integration

### 2.2 The Owl House (Disney / Rough Draft Korea)

**Character rendering strategy:** Flat fills + multi-zone cel-shadow + strong scene lighting overlay.

Key observations:
- **Characters receive explicit scene lighting as color overlays.** In scene2.jpg (Luz close-up in Boiling Isles), the purple environment tints her entire face and shirt — she is not "Luz's colors" but "Luz's colors THROUGH this light"
- **Warm cheeks / cool edges is a standard technique.** In heartwarming scene (whats-the-most...), the warm doorway light creates distinct warm and cool zones on both characters' bodies
- **Shadow shapes are anatomical.** Ear shadows, under-chin shadows, nose shadows all follow specific head geometry. They are not "left half = shadow"
- **Skin has subtle warm-to-cool variation.** Even in flat fills, the shadow-side skin is cooler (slightly more blue/purple shift) while the lit-side is warmer. This is barely visible in isolation but reads as "alive" at viewing distance
- **Hair picks up extreme scene color.** Luz's dark brown hair in the purple scene reads almost black-purple — the scene light dominates hair color completely

### 2.3 Common Principles Across References

| Technique | Hilda | Owl House | Our Current |
|---|---|---|---|
| Flat base fill | Yes | Yes | Yes |
| Scene-responsive color tint | **Yes** | **Yes** | **No** |
| Cel-shadow (form-describing) | Yes | Yes | Partial (left/right only) |
| Warm cheek / cool edge | Subtle | **Explicit** | **No** |
| Outline as form descriptor | **Strong** | **Strong** | Weak (rectangle edges) |
| Hair receives scene color | Yes | **Yes** | **No** |
| Character receives environment light | **Yes** | **Yes** | **No** |

---

## 3. Diagnosis: Why Our Characters Look Flat

### 3.1 Flat Fill Rectangles

Our character draw functions (e.g., `draw_luma()` in SF04) use `draw.rectangle()` and `draw.polygon()` with single `fill=` color arguments. The hoodie is one color. The jeans are one color. The skin is one color. There is no within-zone variation.

**Reference shows also use flat fills** — but they apply scene lighting ON TOP of the flat fill as a translucent overlay. We do this for backgrounds (our warm/cool overlays are excellent) but **never for characters.**

### 3.2 Shadow Placement Is Geometric, Not Anatomical

Our current shadow approach: "left side of the torso = HOODIE_SHADOW." This creates a vertical split that reads as a flat panel, not a 3D form. The reference shows use shadow shapes that follow:
- Fabric folds (a curved shadow under the arm, not a rectangle)
- Overlapping body parts (arm casts shadow on torso)
- Scene light direction (shadow side shifts based on key light position)

### 3.3 No Scene Lighting Integration

This is the critical missing piece. Our backgrounds receive warm overlays, cool overlays, CRT glow, lamp halo — but characters do not. In SF04, the kitchen is bathed in warm amber from the window, but Luma's hoodie and skin are their canonical palette values unmodified. She looks like she was painted in a different room.

### 3.4 No Edge Treatment

Characters terminate at hard rectangle/polygon edges with no transition to the background. Reference shows achieve integration through:
- Consistent outline weight and color (warm dark, not pure black)
- Rim light on the light-facing edge (we have `add_rim_light()` but it is rarely applied to characters in style frames)
- Ambient occlusion shadow under the character's feet (we do this for some frames but not all)

### 3.5 Rectangular Body Construction

This is geometry, not color — but it directly affects how color reads. Rectangle limbs and rectangle torsos cannot hold form-describing shadows because there is no form to describe. A simple improvement: use polygon/ellipse shapes with slight curvature for limbs and torso. Even a 3-4 pixel convex curve on a limb edge changes the shadow read from "flat panel" to "cylindrical form."

---

## 4. Proposed Improvements (Color Domain)

These are the changes Sam Kowalski can implement or specify — geometry changes are flagged for Jordan Reed / Rin Yamamoto.

### 4.1 Scene Lighting Overlay on Characters (Color — Sam/Jordan)

**What:** After drawing the character with canonical palette values, apply a translucent scene-lighting overlay to the character's bounding region. The overlay tints the entire character toward the scene's key light color.

**Implementation:** New function `apply_scene_light_to_character()` in procedural_draw.py (or a new character_color module). Takes:
- Character bounding box (from `get_char_bbox()` or explicit geometry)
- Key light color (e.g., SUNLIT_AMBER for SF04, ELECTRIC_CYAN for SF03)
- Key light direction
- Alpha (typically 15-30, i.e., 6-12% — enough to tint, not enough to wash out canonical values)

**Constraint:** Alpha must never push character colors into a different palette family. Luma's hoodie orange tinted with warm amber is still orange. Luma's hoodie orange tinted with cool cyan at high alpha would violate warmth guarantees.

### 4.2 Warm Cheek / Cool Edge on Skin (Color — Sam)

**What:** Within skin zones (face, hands), apply a subtle warm-to-cool gradient. The lit side (toward key light) gets a warmer shift; the shadow side (away from key light) gets a cooler shift.

**Implementation:** New function `apply_skin_temperature_gradient()`. For each skin pixel within the face ellipse:
- Calculate normalized position relative to light direction
- Lit side: blend toward SKIN_HL (warm highlight) at alpha 20-35
- Shadow side: blend toward a cooler variant (SKIN base with +10 blue channel) at alpha 15-25
- Cheek zone (below eyes, between nose and ear): apply blush overlay (BLUSH color, alpha 15-25)

This is NOT a gradient fill on the base. It is a post-drawing overlay that preserves the canonical flat fill underneath while adding perceptual warmth variation.

### 4.3 Form-Describing Cel-Shadow Shapes (Color + Geometry — Sam specification, Jordan implementation)

**What:** Replace left-right shadow splits with anatomically-informed shadow shapes. These are still flat (single-color) cel-shadows, but their SHAPE follows the body form.

**Specification for each body zone:**

| Zone | Current Shadow | Proposed Shadow Shape |
|---|---|---|
| Hoodie torso | Left-half rectangle | Curved band following shoulder-to-hip diagonal; wider at armpit, narrow at waist |
| Arms | Full rectangle or none | Underside crescent (the part of the cylinder facing down/away from light) |
| Jeans | Thin side strip | Inseam shadow + outer-thigh highlight strip |
| Head/face | Handled by `add_face_lighting()` | Keep current — already form-describing |
| Hair | None | Scene-tinted overlay (same as 4.1 but stronger — hair absorbs more light) |

### 4.4 Character Outline Color Derived from Scene (Color — Sam)

**What:** Instead of a single LINE color (59, 40, 32) for all scenes, derive the character outline color from the scene key light. In warm scenes, outline is warm dark brown (current). In cool scenes, outline shifts toward cool dark (45, 38, 48 — slight purple lean). In Glitch scenes, outline can have a very faint cyan or amber tint.

**Values:**
- Real World warm: `(59, 40, 32)` (current — correct)
- Real World cool/neutral: `(52, 40, 42)` (cooler shift, B > G slightly)
- Glitch Layer: `(48, 36, 44)` (faint purple tint — matches UV_PURPLE ambient)
- Other Side: `(38, 30, 48)` (distinctly cool dark — character reads as immersed)

### 4.5 Hair Scene-Color Absorption (Color — Sam)

**What:** Hair is the character zone most affected by scene lighting in reference shows. Dark hair in a warm room reads warm-dark; dark hair in a purple environment reads dark-purple.

**Implementation:** Apply scene lighting overlay to hair zones at 2x the alpha used for skin/clothing. Luma's HAIR_COLOR (26, 15, 10) in SF03's UV_PURPLE environment should read as (30, 15, 22) — a perceptible but subtle purple shift.

---

## 5. Prototype: `LTG_TOOL_character_color_enhance.py`

A prototype tool has been created at `output/tools/LTG_TOOL_character_color_enhance.py` that implements:

1. **`apply_scene_tint()`** — Scene lighting overlay on character bounding region
2. **`apply_skin_warmth()`** — Warm cheek / cool edge gradient on skin zones
3. **`apply_form_shadow()`** — Curved cel-shadow shapes for torso/limb zones
4. **`derive_scene_outline()`** — Scene-responsive outline color calculation
5. **`apply_hair_absorption()`** — Hair zone scene-color tinting at 2x strength

Each function works as a post-draw overlay — it does not change the base character drawing code. This means it can be integrated into any existing style frame generator by adding a single function call after the character is drawn.

### 5.1 Before/After Demonstration

The prototype generates a comparison image showing a simplified Luma figure rendered with:
- **Left panel:** Current pipeline (flat fill + left-side shadow only)
- **Right panel:** Enhanced pipeline (scene tint + warm cheek + form shadow + outline tint)

Output: `output/color/LTG_COLOR_character_enhance_demo_c50.png`

---

## 6. Integration Path

### Immediate (C50 — Sam Kowalski)
- [x] Analysis document (this file)
- [x] Prototype tool with demo output
- [ ] Integration spec sent to Jordan Reed and Rin Yamamoto

### Next Cycle (C51 — Jordan Reed)
- [ ] Integrate `apply_scene_tint()` into SF04, SF05 generators
- [ ] Replace left-side shadow with form-describing shadow shapes per Section 4.3
- [ ] Test character rendering against reference images

### Following Cycle (C52 — Full Team)
- [ ] Apply to all 6 style frame generators
- [ ] Update `add_face_lighting()` to use scene-derived shadow/highlight colors instead of passed-in values
- [ ] QA verify warmth guarantees are preserved after scene tinting

---

## 7. Risk Assessment

| Risk | Mitigation |
|---|---|
| Scene tint pushes CHAR-L hoodie out of warm guarantee | Alpha ceiling of 30 (~12%); warmth_lint check after tinting |
| Form shadows reduce silhouette readability | All shadow colors are within 30% luminance of the base fill — silhouette test still passes |
| Outline color shift makes characters illegible | Minimum contrast ratio 3:1 between outline and skin maintained |
| Hair absorption changes character recognition | Hair is darkest zone — tinting dark values has minimal perceptual effect at normal viewing |

---

## 8. Summary

The character flatness problem is not a missing technique — it is a missing application. We have scene lighting overlays, warm/cool systems, and rim lights. We apply them to backgrounds but not to characters. The fix is to run the same environmental color logic across character surfaces after the base fill is drawn.

The reference shows confirm that the flat-fill cel-shade aesthetic is correct for our style. We do not need internal gradients or painterly rendering on characters. We need characters to **receive the light that is already in the scene.**
