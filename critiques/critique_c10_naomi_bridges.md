# Critique — Cycle 10
**Critic:** Naomi Bridges, Color Theory Specialist
**Date:** 2026-03-29
**Subject:** Style Frame Color Story, Master Palette Status, SF02 v004 Window Pane Alpha

---

## Priority 1 — Style Frame Color Story Document
**File:** `output/color/style_frames/ltg_style_frame_color_story.md`

### Grade: B+

The color narrative is the strongest piece of written color analysis this production has produced. The three-act color arc — warm dominant / contested / cold dominant — is not only correctly argued, it is *the* correct argument. There is no other structural reading of these three frames that holds together as well. The document earns its confidence.

That said, I have precise objections that prevent an A.

**What works:**

The SF01 analysis is genuinely sharp. The identification of Luma's face and body as the literal meeting point of warm lamp-left and cold monitor-right is good color theory, not just good writing. The hoodie pixel encoding (warm-lit Soft Gold on the lamp side, Electric Cyan on the monitor side) is a detail worth locking into the production bible as a rule, not just describing as an observation. That is a color grammar device that will pay dividends across the whole series.

SF03 is handled correctly. "The tension is entirely material" — that distinction between split-light tension and pigment-memory tension is the right analytical frame. The note about Luma's skin shifting toward "haunted lavender-warm" under UV ambient is accurate to the spec.

The three-sentence summary — "SF01: This is Luma's world. SF02: Neither world owns this frame. SF03: This is not Luma's world." — is pitch-deck quality. It should be in the pitch package as a standalone card.

**Where the document fails scrutiny:**

**Issue 1 — GL-07 Corrupted Amber value discrepancy (factual error).**

The document states: *"The Corrupted Amber outline on Byte (GL-07, #FF8C00) in this frame is also load-bearing."*

The master palette lists GL-07 Corrupted Amber as `#FF8C00` (255, 140, 0). This is correct in the master palette. However, the actual SF02 v004 generator (`LTG_TOOL_style_frame_02_glitch_storm.py`, line 51) defines:

```
CORRUPT_AMBER = (200, 122, 32)   # #C87A20
```

That is not GL-07. That is DRW-07 — the Storm-Modified Hoodie color that is listed in the Locked section of the master palette as `#C8695A`. Even that does not match: `#C87A20` is (200, 122, 32) — R:200, G:122, B:32 — a warm amber-brown. `#C8695A` is (200, 105, 90) — R:200, G:105, B:90 — a muted warm red. These are different colors. And neither is the canonical GL-07 `#FF8C00`.

The color story document is citing the master palette GL-07 value for a color that is not actually rendered in the generator. The rendered CORRUPT_AMBER is 55 points dimmer in the red channel and significantly browner (high green, low blue) compared to the master palette entry. `#FF8C00` is a bright saturated orange — television-warning orange. `#C87A20` is a dark, brownish amber. On screen against a cyan storm, these read completely differently: GL-07 would create a sharp warm-against-cold complement; `#C87A20` creates a more muted, heavy warm accent that reduces contrast rather than fighting it.

The color story document is aspirationally describing a color that is not in the render. This is not a minor annotation issue — the Byte outline is cited as "load-bearing" to the frame's color argument. If the actual rendered value is `#C87A20`, that argument needs to be made with `#C87A20`, not `#FF8C00`.

**Action required:** Either reconcile the generator's `CORRUPT_AMBER` to the master palette GL-07 value `#FF8C00` — which I would recommend, because that value is stronger — or update the color story document to cite the actual rendered value and re-argue why `#C87A20` is the correct choice. The current state is a factual error in a document presented as production truth.

**Issue 2 — SF02 DRW-07 cited value vs. master palette.**

The document names DRW-07 as `#C8695A` in the Locked section of the master palette. The generator defines `DRW_HOODIE_STORM = (200, 105, 90)` which converts to `#C8695A` — that one matches. The hoodie storm color is correctly cited. The Corrupted Amber is not.

**Issue 3 — ENV-06 value cross-check passes.**

The document describes ENV-06 as `#96ACA2` (cool gray-green). The generator defines `TERRA_CYAN_LIT = (150, 172, 162)` = `#96ACA2`. This cross-check passes exactly. Credit to Sam for getting this one right.

**Issue 4 — The SF02 narrative overstates warm window glow agency.**

The document states: *"The warmth holds the ground."* Structurally, I understand what this is trying to say, but the actual alpha values of the window glow cones undercut this reading. I will address this under Priority 3, but note here that the color story document makes a narrative claim ("warmth holds the ground") that the rendered frame may not visually support given the glow cone alpha values. The claim needs to be defensible in the render, not just in prose.

---

## Priority 2 — Master Palette Status Section
**File:** `output/color/palettes/master_palette.md` (Palette Status section, bottom)

### Grade: A−

The Locked / Provisional / Named Gaps structure is sound, and the locking criteria are correctly articulated. The section does what it claims to do. My objections are targeted.

**Locked section — defensible.**

The locked entries are correctly chosen with one exception: `CHAR-L-08 Hoodie Underside (Ambient) #B36250` is listed as locked. Looking at this value — (179, 98, 80) — it is a desaturated warm mid, which is appropriate. I have no quarrel with the lock. The `ENV-06 #96ACA2` lock is confirmed by the generator (see above). The `DRW-07 #C8695A` lock is confirmed by the generator's `DRW_HOODIE_STORM`.

**Provisional section — mostly correct, one concern.**

`CHAR-M-04 Miri Permanent Blush #D4956B` flagged as provisional because the 25% opacity spec is not yet translated to a flat render constant. This is correctly identified. My concern is that the blush at 25% over skin base `#C4A882` produces a different result than the same color at 100% as a flat fill. The flat-hex equivalent of 25% `#D4956B` over `#C4A882` is approximately `#CEAB8D`. That is what the palette should register, not `#D4956B` at an unspecified coverage. This is not just a documentation gap — it is a value that will vary depending on how different artists interpret "25% opacity." Register the composited flat value.

`TD-10/TD-11 Monitor Screen / Glow` flagged because the generator uses `MON_GLOW_BRIGHT (200, 218, 240)` vs. the palette's `#C8D4E0 (200, 212, 224)`. The delta is G+6, B+16 in the generator vs. the palette spec. That is a visible shift toward a cooler, bluer monitor glow. In a scene about digital intrusion, a bluer monitor glow is not neutral — it pushes the Tech Den slightly toward the Glitch aesthetic before the Glitchkin arrive. This should be resolved, not left provisional.

**Named Gaps — are any actually a production risk?**

The four cross-check gaps Sam flagged:

1. **UV_PURPLE construction values in SF03 vs ENV-11/ENV-12.** Sam correctly identifies that these likely match. If ENV-11 is `#2A1A40` (42,26,64) and the script's `UV_PURPLE_MID` is also `(42,26,64)`, they are identical and the resolution is a comment, not a value change. This is minor. Low production risk.

2. **CIRCUIT_TRACE_DIM (0,192,204) in SF03.** Sam correctly marks this low priority. It sits between GL-01a `#00A8B4` (0,168,180) and GL-01 `#00F0FF` (0,240,255) in the cyan range. The value is coherent with the palette system even without registration. Low production risk.

3. **JEANS_BASE (38,61,90) vs CHAR-L-05 (58,90,140).** This is not minor. The delta is R-20, G-29, B-50. That is a full value step darker and significantly desaturated. Under UV Purple ambient in the Glitch Layer, some darkening is expected — but 50 points on the blue channel under a blue-dominant light is going in the wrong direction. Under UV Purple ambient, blue surfaces should appear relatively brighter, not darker. If the jeans are supposed to read as Luma's jeans under alien light, they should be slightly brighter/cooler, not dramatically darker. Sam flags this as plausible, but it deserves a second look. I would call this a **medium production risk** — it affects Luma's legibility in SF03 and in any future Glitch Layer scenes.

4. **LUMA_SHOE (220,215,200) vs CHAR-L-09 (250,240,220).** Delta is R-30, G-25, B-20 — a significant darkening and slight warm neutralization under UV. The principle (UV ambient darkens warm surfaces) is correct. Low production risk as a construction value, provided it is commented in the script.

**Summary on Named Gaps:** Gap 3 (jeans under UV light) should be elevated from low to medium risk. The others are genuinely minor. The overall designation framework is sound.

---

## Priority 3 — SF02 v004 Window Pane Alpha
**File:** `output/tools/LTG_TOOL_style_frame_02_glitch_storm.py`

### Grade: C+

Alex flagged the window pane alpha at 160–180 vs. recommended 90–110. Having read the generator, I can now be precise about what is actually happening.

**What the generator actually does — distinguish the two alpha values:**

The `win_colors` array (line 295) defines two window fill colors:
- `(*SOFT_GOLD, 180)` — `#E8C95A` at alpha 180 (70.6% opacity)
- `(*WARM_CREAM, 160)` — `#FAF0DC` at alpha 160 (62.7% opacity)

These are the *window pane fills* — the color of the lit window rectangle itself.

The *glow cone* below each window uses a separate formula (lines 337–338):
```python
a = int((1.0 - t_step ** 0.8) * 105)
```
This produces a maximum alpha of 105 at `t_step = 0` (the top of the cone, immediately below the window) — which is exactly within the 90–110 spec. The glow cones are correctly calibrated.

**The alpha problem is in the window panes, not the glow cones.**

The spec said "Alpha 90–110" for the warm window glow. The glow cones achieve this. But the window pane fills — the actual window rectangles — are rendered at 160–180, which is considerably more opaque.

Here is why this matters: the window pane alpha of 160–180 composited over the building color produces a significantly warm, nearly-opaque warm square on each building face. At alpha 180/255 = 70.6% opacity, the Soft Gold `#E8C95A` composited over a `DEEP_WARM_SHAD (90,56,32)` building produces approximately:

- R: 90*(1-0.706) + 232*0.706 ≈ 26 + 164 = **190**
- G: 56*(1-0.706) + 201*0.706 ≈ 16 + 142 = **158**
- B: 32*(1-0.706) + 90*0.706 ≈ 9 + 64 = **73**

Result: approximately `#BE9E49` — a strong, warm gold-amber that is quite readable even against the cyan storm background.

At the recommended alpha 90–110 (say alpha 100 = 39.2% opacity):

- R: 90*(0.608) + 232*0.392 ≈ 55 + 91 = **146**
- G: 56*(0.608) + 201*0.392 ≈ 34 + 79 = **113**
- B: 32*(0.608) + 90*0.392 ≈ 19 + 35 = **54**

Result: approximately `#927136` — a muted, warm brown that whispers rather than speaks.

**The question: is 160–180 defensible as a color decision?**

The color story document's thesis is "the warmth holds the ground." If that is the intended reading, then alpha 160–180 on the window panes is *supporting* the narrative: the windows are genuinely warm-opaque, visually competitive with the cyan storm above them. The warm glow is not a suggestion — it is a statement.

The counterargument — and this is the one that worries me — is that at 160–180 pane alpha, the windows compete with Luma's hoodie for the role of "the warm thing in this frame." Luma's hoodie is `DRW_HOODIE_STORM (200,105,90)` = `#C8695A`. Her hoodie is the *character's* warmth. The windows are the *world's* warmth. These two warmths should be in a clear hierarchy: Luma's warmth should dominate because it is the emotional anchor of the scene. If the windows are rendered at near-full opacity warm gold, they are visually competing with her.

Standard chromatic hierarchy practice: the character's signature color should be the highest-saturation instance of its hue family in any frame. Luma's hoodie is a muted warm (it is storm-modified). The window panes at 160–180 alpha over gold are rendering a cleaner, brighter warm than her hoodie. That is a hierarchy inversion. The windows are more aggressively warm than the character who is supposed to embody warmth.

**My conclusion:** The 160–180 pane alpha is a problem, but not for the reason Alex flagged (warm vs. cold competition). The actual problem is character-warmth hierarchy. The windows are winning a fight they should be losing. Recommended correction: reduce pane alpha to 110–130. This keeps them readable as warm-lit windows (they do not disappear), preserves the "warmth holds the ground" narrative, but restores Luma's hoodie to its correct position as the dominant warm element in the frame.

The glow cones at max alpha 105 are correct. Do not touch those.

---

## Top 3 Priority Fixes

**1. Reconcile CORRUPT_AMBER in SF02 v004 to GL-07 `#FF8C00`.**

The generator uses `#C87A20` (200, 122, 32). The master palette and the color story document cite `#FF8C00` (255, 140, 0). These are not the same color. Against a cyan-dominant storm, `#FF8C00` delivers a genuine warm-cold complement (the complement to `#00F0FF` Electric Cyan sits near orange-red; `#FF8C00` is close). `#C87A20` delivers a murky brownish amber that loses contrast. The narrative claim that the Byte outline is "load-bearing" to the frame's color argument rests on using the high-contrast version. Currently the rendered frame does not deliver that. Fix the generator; update the color story document to reflect the correct value.

**2. Reduce SF02 v004 window pane alpha from 160–180 to 110–130.**

At 160–180, the warm gold windows are more saturated-visible than Luma's storm-modified hoodie, inverting the character-warmth hierarchy. The window warmth should support the narrative; it should not compete with the protagonist for the role of "warm thing in this frame." Reduce pane alpha, preserve glow cone alpha (already correctly at 90–110 max). Update `win_colors` line 295 accordingly.

**3. Elevate JEANS_BASE gap (Gap 3) from low to medium risk and force resolution.**

`JEANS_BASE (38,61,90)` in SF03 is 50 points darker on the blue channel than the canonical `CHAR-L-05 #3A5A8C`. Under UV Purple ambient, a blue-range surface should not become this much darker. Either confirm the value as the existing jeans shadow entry `#263D5A` and comment accordingly, or register it as `CHAR-L-05a` with an explicit note explaining the UV-ambient physics. Leaving this undocumented creates a precedent: future Glitch Layer scenes will reference SF03 as the visual spec, and painters will use `#263D5A`-range jeans as canonical for that environment. If that is wrong, it compounds with every subsequent frame.

---

**Overall assessment:** The narrative ambition of this production's color work is higher than most shows I review at this stage. The color story document, even with its errors, represents genuine strategic color thinking. But strategic thinking that rests on factual errors in the render is a liability, not an asset. Fix the generator values to match the arguments, or fix the arguments to match the generators. Aspirational documentation is not production documentation.

— Naomi Bridges, Color Theory Specialist
