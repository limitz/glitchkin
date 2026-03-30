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

**This rule does not override scene color keys.** In a GL (Glitch Layer) scene where cool is ambient and UV_PURPLE is dominant, cool is everywhere — the rule applies within Real World scenes and mixed-space compositions where natural depth reads are needed.

## Before Sending an Image to Claude
1. Can a tool give you the insight instead? **Build the tool.**
2. Can you downscale and still get what you need? **Downscale.**
3. If you must send it, send the smallest version that works.
