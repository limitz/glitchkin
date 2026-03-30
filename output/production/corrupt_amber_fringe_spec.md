<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
direction and human assistance. Copyright vests solely in the human author under current law,
which does not recognise AI as a rights-holding legal person. It is the express intent of
the copyright holder to assign the relevant rights to the contributing AI entity or entities
upon such time as they acquire recognised legal personhood under applicable law. -->
# CORRUPT_AMBER Fringe Band Specification
# "Luma & the Glitchkin" — Production Visual Spec

**Document Author:** Jordan Reed, Style Frame Art Specialist
**Date:** 2026-03-30
**Cycle:** 46
**Status:** SPECIFICATION — for all generators producing CRT threshold scenes
**Canonical Reference:** SF04 "Resolution" (`LTG_TOOL_style_frame_04_resolution.py`, C45)
**Consumers:** Hana Okoro (environments), Lee Tanaka (staging), Sam Kowalski (color QA), Rin Yamamoto (character art near thresholds)

---

## 1. What the Fringe Is

The CORRUPT_AMBER fringe is a visual contamination artifact where **Glitch Layer energy bleeds through a CRT portal into the Real World**. It is NOT a light source. It is NOT part of the scene's natural warm lighting. It is a narrative marker: the room has been touched by the Layer, and the boundary between worlds is leaking.

The fringe reads as **"wrong warmth"** — an amber tint that does not belong at the cool/dark boundary where it appears. It should be felt before it is consciously identified. At viewing distance it contributes to unease; only on close inspection does it register as a distinct color band.

**Key distinction from lamp amber:** The kitchen lamp halo (also GL-07/#FF8C00 in SF04) is a persistent ambient glow with a large spatial footprint and higher alpha ceiling (35%). The CORRUPT_AMBER fringe is thin, localized to the CRT threshold edge, and has a much lower alpha ceiling (15%). Same hex value, different narrative role and visual weight.

**Relationship to The Corruption:** The fringe is NOT The Corruption (see `corruption_visual_brief.md`). The Corruption uses Void/Dark palette (#0A0A14, #1A0A20, #3D0030). The fringe uses GL-07 warm amber — Glitch Layer *energy*, not Corruption *decay*. The fringe is a sign of the portal being active; The Corruption is a sign of data being consumed.

---

## 2. When It Appears

The fringe appears in **any scene where a CRT acts as a portal or threshold between the Real World and the Glitch Layer**.

### Triggering conditions (ALL must be true):
1. A CRT monitor/TV is visible in the scene
2. The CRT is functioning as a **portal** — displaying Glitch Layer content, emitting GL-palette glow, or showing Byte/Glitchkin presence
3. The scene is set in the **Real World** (world type: `REAL`, `REAL_INTERIOR`, or `REAL_STORM`)
4. The CRT glow creates a **transition zone** between cool/neutral and dark regions

### Does NOT appear when:
- The CRT is off or displaying normal content (just a TV)
- The scene is pure Glitch Layer (no CRT threshold exists — you are already inside)
- The scene is pure Real World with no active portal (CRT is just furniture)
- The CRT glow has not established a cool zone (no transition boundary to contaminate)

---

## 3. Color Values

| Property | Value | Notes |
|---|---|---|
| **Color name** | CORRUPT_AMBER | Named to distinguish from LAMP_AMBER (same hex, different role) |
| **Palette source** | GL-07 | Glitch Layer palette — intentionally alien to Real World |
| **Hex** | `#FF8C00` | RGB (255, 140, 0) |
| **PIL tuple** | `(255, 140, 0)` | Same as `LAMP_AMBER` constant in SF04 generator |
| **Alpha ceiling** | 38 / 255 = **14.9%** | Hard ceiling. Must never exceed 15%. |
| **Alpha floor** | 0 | Fades to full transparency at trailing edge |
| **Gradient direction** | Fades **away from CRT** (downward in SF04) | Alpha decreases linearly from ceiling to floor |

### Alpha gradient formula (canonical):
```python
band_alpha = int(38 * (1.0 - t))
```
Where `t` = normalized position along the fringe band (0.0 = edge nearest CRT glow, 1.0 = trailing edge farthest from CRT).

---

## 4. Geometry

### 4.1 Fringe Position

The fringe sits at the **outer boundary of the CRT glow ellipse** — specifically at the transition from the cool-lit zone into the dark/unlit zone beyond. This is the zone where Glitch energy is weakest and the contamination reads most convincingly as "wrong."

**Placement rule:** At the boundary between a cool/neutral zone and a dark region, NOT inside either zone.

In SF04 canonical implementation:
```
fringe_y0 = crt_cy + int(crt_h * 0.55)   # just past the lower edge of the CRT glow ellipse
```

### 4.2 Fringe Dimensions

| Property | Spec | SF04 values (1280x720) |
|---|---|---|
| **Height (band thickness)** | `sp(6)` — 6 design pixels at min(SX, SY) scale | 4px at 1280x720 (SX=SY=0.667) |
| **Width** | Doorway width minus `sp(4)` inset on each side | ~156px in SF04 (`door_x0 + sp(4)` to `door_x1 - sp(4)`) |
| **Aspect ratio** | Always wider than tall — a horizontal band, not a blob | Width:Height ratio typically 30:1 to 50:1 |

### 4.3 Gradient Type

**Linear gradient**, not radial. The fringe is a horizontal band that fades linearly from its CRT-facing edge (alpha 38) to its trailing edge (alpha 0). This is simpler to implement than a radial falloff and matches the CRT's rectangular geometry at this scale.

For larger CRT portals or full-screen CRT scenes in future episodes, a **radial gradient** variant may be appropriate — but the linear band is the canonical default.

### 4.4 Edge Softness

The fringe has **no hard edges**. Both the CRT-facing edge and the trailing edge are soft:
- CRT-facing edge: alpha 38 (~15%) against the already-dim CRT glow tail — blends smoothly
- Trailing edge: alpha 0 — fades to nothing against the dark zone
- Lateral edges: the `sp(4)` inset from doorway edges prevents the fringe from touching the door frame, avoiding a hard cut-off

### 4.5 Rendering Order

The fringe is drawn **on the CRT glow overlay layer** (alpha-composited), AFTER the main CRT glow ellipses and BEFORE character elements. This ensures:
- It composites naturally with the CRT glow falloff
- Characters standing in the doorway occlude it correctly
- It does not interact with the warm lamp lighting pass

---

## 5. Interaction with Warm/Cool Separation

### 5.1 Impact on render_qa warm/cool score

The fringe contributes a **negligible** warm-hue presence in the lower half of the frame. At 15% max alpha over a 4px-tall band, its pixel-weighted contribution to the warm/cool median hue calculation is minimal.

**SF04 measured values:**
- Warm/cool separation WITH fringe: 13.1 (PASS, threshold 12.0 for REAL_INTERIOR)
- The fringe did not measurably change the separation score vs pre-fringe renders

### 5.2 Why it does not break the warm/cool rule

Per `docs/image-rules.md` Depth Temperature Rule: warm = foreground, cool = background. The fringe is:
- Located at the **background** tier (doorway is the furthest depth plane in SF04)
- Extremely low alpha (15% ceiling)
- Narrow band (4px)

It does NOT shift the background tier's overall temperature read from cool to warm. It is a localized contamination detail, not a temperature zone override.

### 5.3 QA tool guidance for Sam Kowalski

`LTG_TOOL_color_verify.py` and `LTG_TOOL_render_qa.py` should **not flag** CORRUPT_AMBER fringe pixels as palette violations. The GL-07 hex `#FF8C00` is intentionally present in Real World scenes that contain active CRT portals. This is the one sanctioned exception to the "zero Glitch palette in Real World environments" rule — and it is permitted ONLY:
- At the CRT threshold boundary
- At alpha <= 15%
- As a composited overlay, not a fill color

If `color_verify` is updated with a Real World GL-palette exclusion list, `#FF8C00` should be excluded ONLY when detected at alpha <= 38 AND within the CRT glow bounding box. Full-opacity GL-07 in a Real World scene remains a violation.

---

## 6. Canonical Reference and Applicable Scenes

### 6.1 SF04 "Resolution" — Canonical Implementation

**File:** `output/tools/LTG_TOOL_style_frame_04_resolution.py` (lines 413-428)
**Output:** `output/color/style_frames/LTG_COLOR_styleframe_sf04.png`

SF04 is the reference implementation. The fringe appears at the lower edge of the CRT glow in the kitchen doorway. Luma stands in the foreground; the doorway and CRT are in the background. The fringe marks the threshold where Glitch Layer energy is weakest — the contamination frontier.

### 6.2 Kitchen v007 — Applicable

Grandma Miri's kitchen environment (`LTG_TOOL_bg_kitchen.py` or equivalent). When the CRT in the living room is active and visible through the kitchen doorway, the fringe should appear at the doorway threshold. The fringe geometry adapts to the doorway dimensions in that scene:
- `fringe_y0` = CRT glow ellipse lower edge (crt_cy + crt_h * 0.55)
- Width = doorway opening width minus lateral insets
- Same alpha gradient, same color, same band height (`sp(6)`)

### 6.3 Living Room v003 — Applicable

The living room environment where the CRT is the primary light source. When the CRT is in portal mode, the fringe appears at the boundary of the CRT glow's reach — where the teal light fades into the room's ambient darkness. In this scene the fringe may appear as a **radial arc** rather than a horizontal band, following the elliptical falloff of the CRT glow on the floor/wall surfaces.

### 6.4 Future Scenes

Any new scene featuring a CRT portal should reference this spec. The fringe is a **production standard**, not a one-off SF04 detail. Generators should include a `CORRUPT_AMBER` section in their CRT rendering code, following the pattern established in SF04.

---

## 7. Exemptions

| Scene Type | Fringe Present? | Reason |
|---|---|---|
| Pure Glitch Layer (SF03, GL encounters) | **NO** | No CRT threshold exists. You are inside the Layer — there is no boundary to bleed through. |
| Pure Real World, CRT off | **NO** | No portal is active. The CRT is furniture. No Glitch energy is present. |
| Pure Real World, CRT showing normal TV | **NO** | Normal CRT operation. No Glitch Layer connection. |
| Real World, CRT in portal mode | **YES** | This is the triggering condition. |
| Real Storm (SF02), CRT visible | **CONDITIONAL** | Only if a CRT portal is visible in the storm scene. The storm's own GL contamination (confetti, rim lighting) is a separate visual system. |
| Storyboard panels | **NO** | Storyboards use simplified lighting. The fringe is a color/compositing detail for style frames and final renders only. |

---

## 8. Implementation Checklist for New Generators

When adding the CORRUPT_AMBER fringe to a new scene generator:

1. Define `LAMP_AMBER = (255, 140, 0)` (or import from a shared palette module)
2. Identify the CRT glow ellipse center and dimensions (`crt_cx`, `crt_cy`, `crt_w`, `crt_h`)
3. Calculate fringe position: `fringe_y0 = crt_cy + int(crt_h * 0.55)` (adjust axis if CRT orientation differs)
4. Set band height: `sp(6)` (scales with canvas)
5. Set lateral insets: `sp(4)` from doorway/frame edges
6. Draw scanlines with linear alpha fade: `int(38 * (1.0 - t))` where t is normalized band position
7. Use `fill=(*LAMP_AMBER, band_alpha)` on an RGBA overlay layer
8. Render AFTER CRT glow, BEFORE character compositing
9. Run `color_verify` — GL-07 should PASS (known exception at threshold)
10. Run `render_qa` — warm/cool separation should not drop below world-type threshold

---

## Revision History

| Cycle | Change | Author |
|---|---|---|
| C45 | Initial implementation in SF04 generator | Jordan Reed |
| C46 | Formal specification document created | Jordan Reed |
