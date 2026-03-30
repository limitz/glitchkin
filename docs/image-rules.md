# Image Rules
*All agents: team members and critics.*

**Hard limit: ≤ 1280px in both dimensions** for every saved image. Use smallest resolution that works. For fine-detail inspection, crop — don't upscale.

## Vision Limitations
| Limitation | Detail |
|---|---|
| Accuracy | Unreliable on low-quality, rotated, or sub-200px images |
| Spatial reasoning | Poor at precise positions and layouts |
| Counting | Approximate only, especially for many small objects |
| Aesthetic judgement | Unreliable — define metrics, extract them with tools |

## Depth Temperature Rule
*Codified C45 — applies to all multi-character and multi-tier compositions.*

**Warm color = foreground. Cool color = background.**

In any composition with depth tiers, the warm/cool split is the primary depth cue:

| Tier | Temperature | Rationale |
|------|-------------|-----------|
| Foreground (FG) | Warm (amber, golden, sunlit) | Closer to light source; closer to viewer |
| Background (BG) | Cool (slate, cyan-tinted, shadowed) | Receding; ambient/indirect light |

**Why this rule exists:** A tier gap of 44px (8% of canvas height) compresses to sub-pixel at contact sheet scale. Only tonal temperature contrast reliably communicates spatial depth across ALL viewing contexts: full resolution, thumbnail, B&W print, and pitch-deck projection.

**Implementation (lineup/multi-character scenes):**
- FG tier: warm drop-shadow band beneath FG_GROUND_Y (amber family)
- BG tier: cool drop-shadow band beneath BG_GROUND_Y (slate/cool family)
- This is Option C from the C45 lineup tier depth evaluation (`output/production/lineup_tier_depth_recommendation_c45.md`)

**BG Saturation Drop:** In addition to the cool temperature shift, background tier elements must desaturate by 15-25% relative to foreground tier elements. This mimics atmospheric perspective — distant objects lose chroma. Implementation: multiply BG tier saturation by 0.75-0.85 (exact factor per scene; 0.80 is the default). This stacks with the cool shift — both cues reinforce depth.

**Warm→Cool Transition Curve:** The temperature shift from warm FG to cool BG follows a **sigmoid curve**, not a linear gradient. The transition band is narrow — approximately 10-15% of the room depth (measured in canvas Y). Implementation: use a logistic function centered at the FG/BG boundary:

```
import math

def warm_cool_mix(y, fg_y, bg_y, steepness=12.0):
    """Returns 0.0 (fully warm/FG) to 1.0 (fully cool/BG).
    y: current vertical position
    fg_y: foreground ground line (Y pixels)
    bg_y: background ground line (Y pixels)
    steepness: sigmoid steepness (12.0 = ~10% transition band)
    """
    midpoint = (fg_y + bg_y) / 2.0
    span = abs(bg_y - fg_y) or 1.0
    t = (y - midpoint) / (span / steepness)
    return 1.0 / (1.0 + math.exp(-t))
```

Steepness=12.0 produces a transition band of ~10% of the FG-BG span. Lower values (8.0) widen the band to ~15%. Generators should use this function (or the equivalent in their drawing pipeline) rather than `lerp()` for warm/cool blending.

**This rule does not override scene color keys.** In a GL (Glitch Layer) scene where cool is ambient and UV_PURPLE is dominant, cool is everywhere — the rule applies within Real World scenes and mixed-space compositions where natural depth reads are needed.

## CRT Glow Asymmetry Rule
*Codified C49 — applies to all CRT-emitting scenes (Luma's study, cold open CRT shots, any scene with an active CRT).*

**CRT glow is asymmetric: brighter above and to the sides, dimmer below.**

Real CRT monitors sit in a cabinet or on a surface. The cabinet/desk occludes downward light spread. Reference images consistently show the glow pool is 25-35% dimmer below the screen centerline compared to above.

| Direction | Glow Intensity (relative to peak) |
|---|---|
| Above screen | 100% (full glow — unoccluded) |
| Left/Right of screen | 90-100% (slight falloff at extreme angles) |
| Below screen | 65-75% (cabinet/surface occlusion) |

**Implementation:** All CRT glow generators must apply a **0.70 multiplier** (default) to glow alpha/intensity for pixels below the screen's vertical midpoint. This applies to both the direct glow ellipse and any ambient bounce. The multiplier is adjustable per scene via config but defaults to 0.70.

**Does not apply to:** Floating CRT in Glitch Layer (no physical cabinet), or scenes where the CRT is wall-mounted with no lower occlusion.

---

## Shoulder Involvement Rule
*Codified C47 — applies to all human characters (Luma, Cosmo, Miri). Byte and Glitch are exempt.*

**When an arm moves past ~30 degrees from rest, the shoulder line must change shape.**

This is a persistent critique (Takeshi, since C15). Arms that swing from a static shoulder socket read as puppet arms. The shoulder mass (deltoid region) must respond to arm position.

| Arm Position | Shoulder Response |
|---|---|
| Raised above horizontal | Shoulder point rises 3-5px; torso top edge becomes asymmetric |
| Extended forward/outward | Shoulder point shifts outward 4-6px; torso widens on that side |
| Crossed over body | Shoulder point drops 1-2px, shifts inward 3-4px; neck base widens |
| Both arms raised | Both shoulders rise; neck appears shorter; torso top edge arches |
| Relaxed at side | Neutral — shoulder is a rounded bump, not a sharp rectangle corner |

**Implementation:** Replace rectangle torso top edges with polyline shoulder points that derive from arm angle. Add a small deltoid bump (ellipse or arc, 4-6px at style-frame scale) at the shoulder-arm junction that follows the arm's initial direction.

**Per-character clothing reads:** Luma = hoodie fabric bunch; Miri = cardigan shoulder crease; Cosmo = fitted shirt rounded corner.

**Does not apply to:** Byte (digital body), Glitch (non-humanoid), or sprint-scale characters where head_r < 20px (shoulder shift would be sub-pixel).

**Full reference:** `output/production/shoulder_mechanics_reference_c47.md` (Lee Tanaka C47).

## Before Sending an Image to Claude
1. Can a tool give you the insight instead? **Build the tool.**
2. Can you downscale and still get what you need? **Downscale.**
3. If you must send it, send the smallest version that works.
