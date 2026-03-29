# Character Sheet Standards — "Luma & the Glitchkin"

**Prepared by:** Alex Chen, Art Director
**Date:** 2026-03-29
**Version:** v001
**Based on:** Audit of all active expression sheet generators in `output/tools/`
           and character spec files in `output/characters/main/`.

---

## Purpose

This document establishes the conventions that all character expression sheet generators must follow. It is binding for all sheets created from Cycle 22 onward. Existing sheets that predate this document are grandfathered unless a rebuild is scheduled.

---

## 1. Expression Label Format

Labels appear in the panel caption area beneath each expression panel.

**Policy:** Multi-word expressions use a slash-extended format when two emotional states are simultaneous or transitional. Single-state expressions use a single-word or minimal label.

| Label Style | When to Use | Examples |
|---|---|---|
| Single word | One unambiguous emotional state | `GRUMPY`, `SEARCHING`, `ALARMED`, `CONCERNED` |
| Slash-extended | Two simultaneous or transitional states | `NEUTRAL / DEFAULT`, `RELUCTANT JOY`, `SKEPTICAL / AMUSED`, `SURPRISED / DELIGHTED`, `WISE / KNOWING`, `WARM / WELCOMING` |
| Slash-extended (damage) | Damage state combining two conditions | `STORM / CRACKED` |

**Rules:**
- Labels are always ALL CAPS.
- Maximum label length: 24 characters (fits within a standard 280–380px panel at display font size).
- The slash is surrounded by a single space on each side: `STATE / STATE`, not `STATE/STATE`.
- Labels are factual, not poetic. Describe the emotional read, not a narrative situation.
- Labels must match the `EXPR_LABELS` dict or the expression name string defined in the generator. No variation between the code key and the displayed label.

---

## 2. HEAD_R Values and Format (Bust vs Full-Body)

`HEAD_R` is the head radius in pixels at the internal 1× coordinate space (before render scale). It determines whether a character reads as a **bust** (head + upper torso only) or **full-body** (head to feet visible).

**The HEAD_R parameter controls apparent figure size within the panel. A larger HEAD_R at fixed panel size = bust; a smaller HEAD_R = full-body.**

| Character | HEAD_R (1×) | Render Scale | Effective HR (at render) | Format |
|---|---|---|---|---|
| Luma | 105 | 2× | 210 | Full-body (3×2 grid, 1200×900) |
| Cosmo | ~95 effective | 1× (native panel) | — | Full-body (3×2 grid, ~280×420 panels) |
| Byte | — | 1× native | body_rx / body_ry set per expression | Full-body (4×2 or 3×3 grid) |
| Grandma Miri | 68 | 2× | 136 | Full-body (3×2 grid, 1200×900) |

**Bust format:** Use only when the scene or beat specifically requires an ECU read — not for general expression sheets. No current LTG expression sheet uses pure bust format. Bust is reserved for single-panel storyboard inserts (e.g., A2-02 MCU panels).

**Full-body is the default for all multi-panel expression sheets.** Body posture must differentiate expressions at thumbnail scale (squint test). Face-only expression sheets are rejected per Dmitri Volkov critique history.

---

## 3. Head Unit Size Ranges by Character Type

"Head units" (HU) refer to the head height as a proportional measure. One HU = the height of the character's head from crown to chin.

| Character | Head Radius | Character Type | Target Body Height (in HU) | Notes |
|---|---|---|---|---|
| Luma | 105px (1×) | Human child protagonist | 4.5–5.0 HU | Luma is 14 HU total height (per character_lineup.md). Expressive hair = part of silhouette. |
| Cosmo | ~95px equivalent | Human child supporting | 4.5–5.0 HU | Slightly more compact read than Luma. Glasses are key silhouette element. |
| Grandma Miri | 68px (1×) | Human adult secondary | 5.5–6.0 HU | Shorter absolute head but adult proportions. 88% circular (gently compressed ellipse). |
| Byte | body_ry ~55–65px | Digital entity | N/A (no leg HU — oval body only) | Byte uses body_rx / body_ry, not head units. Oval body canon: chamfered-box design retired Cycle 8. |
| Glitchkin (generic) | 8–12px faceplate | Glitch world entities | Must remain smaller than Byte in all frames | Pixel anatomy only: faceplate + body mass. No fixed shape. |

**Head radius must never be set so large that body/legs fall below the panel bottom edge at the nominal body height range.** If a rebuild requires larger head detail, increase panel height, not HEAD_R alone.

---

## 4. Construction Guide Policy

Construction guides are optional visual aids drawn as RGBA overlays at reduced opacity. They show the head circle, center horizontal axis, and center vertical axis in a desaturated warm tone (typically `(180, 155, 128, 48)` RGBA).

**Policy: Construction guides are OFF by default in final output.**

They are provided as a drawing aid and as a teaching reference when the sheet is used for on-model consistency checks. They are not intended to appear in pitch package exports.

| Use Case | Construction Guides |
|---|---|
| Pitch package output | OFF (default) |
| On-model consistency review | Toggle ON via generator flag |
| Technical training / onboarding | Toggle ON — include as explicit "construction overlay" variant |
| Final animation production reference | OFF |

**Implementation:** All generators must implement construction guides via a function (`draw_construction_guide()` or equivalent) that takes the render-space head center `(cx, cy)` as arguments and composes via `Image.alpha_composite()`. The function must be callable as a post-pass after the character is drawn; it must not be embedded inside the character draw functions. See `LTG_TOOL_luma_expression_sheet_v003.py` for the canonical reference implementation.

**When construction guides are ON, the guide draws:** head circle, horizontal midline, vertical midline. Optionally: jaw circle, eye-level horizontal guide. Guides are NEVER filled; they are outline/line only.

---

## 5. Canvas and Grid Standards

All expression sheets must conform to the following unless a character-specific exception is documented:

| Parameter | Standard |
|---|---|
| Canvas size | 1200×900 (portrait-oriented grids) or proportional equivalent |
| Grid layout | 3×2 (6 panels) for human characters; 4×2 or 3×3 for Byte |
| Header height | 52–58px (title + version bar) |
| Label height | 36px beneath each panel |
| Pad between panels | 18–20px |
| Render scale | 2× internal, downsampled to 1× output via `LANCZOS` |
| Output format | PNG, RGB mode |
| Canvas background | Near-void dark: `(28, 20, 14)` or equivalent |

---

## 6. Line Weight Standards (3-Tier)

All character sheets follow the 3-tier line weight directive established in `char_refinement_directive_c17.md`:

| Tier | Width at 2× render | Output equivalent | Used for |
|---|---|---|---|
| Silhouette | 8px | ~4px | Head outline, hair mass, body perimeter |
| Interior structure | 4px | ~2px | Eyelid arcs, brows, costume seams |
| Detail | 2–3px | ~1–1.5px | Crinkle lines, nose arc, decorative stitching |

Brows are interior structure weight (4px at 2×), NOT silhouette weight. The Cycle 19 `v002`→`v003` correction on Luma's sheet (brow 10px→4px) is the canonical fix reference.

---

## 7. Expression Count per Character

| Character | Expression Count | Grid | Sheet Version |
|---|---|---|---|
| Luma | 6 | 3×2 | v003 (current) |
| Cosmo | 6 | 3×2 | v003 (current) |
| Byte | 9 | 3×3 | v003 (current) |
| Grandma Miri | 5 | 3×2 (last panel intentionally empty or used for credit) | v002 (current) |

Byte's 9-expression grid is intentional: the STORM/CRACKED variant added in Cycle 21 required a grid upgrade from 4×2 to 3×3. Do not revert Byte to 4×2.

---

*LTG_PROD_character_sheet_standards_v001.md — Alex Chen, Art Director*
*Cycle 22 — 2026-03-29*
