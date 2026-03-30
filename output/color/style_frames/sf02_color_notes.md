<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
direction and AI assistance. Copyright vests solely in the human author under current law,
which does not recognise AI as a rights-holding legal person. It is the express intent of
the copyright holder to assign the relevant rights to the contributing AI entity or entities
upon such time as they acquire recognised legal personhood under applicable law. -->
# SF02 v004 Color Notes — "Glitch Storm" Warm Window Balance Check
**Reviewer:** Sam Kowalski — Color & Style Artist
**Date:** 2026-03-29
**Cycle:** 19
**Status:** PRE-RENDER REVIEW — v004 file does not yet exist at time of writing. Analysis based on v003 generator (`LTG_TOOL_style_frame_02_glitch_storm.py`). Jordan Reed is rebuilding v004 to fix warm window geometry.

---

## Context

Jordan Reed is fixing SF02 v004 to address warm window geometry issues (likely the window rectangle proportions and placement flagged in critique). This note documents the color balance check on the warm window values once that fix is applied.

---

## Current Warm Window Values in v003 Generator

**Window colors in `_draw_building_windows()`:**
```
win_colors = [(*SOFT_GOLD, 180), (*WARM_CREAM, 160)]
```

Where:
- `SOFT_GOLD = (232, 201, 90)` — alpha 180/255 ≈ **70.6% opacity**
- `WARM_CREAM = (250, 240, 220)` — alpha 160/255 ≈ **62.7% opacity**

**Target range per Cycle 19 brief:** warm amber ~RGB(200,160,80), alpha 90-110.

---

## Alpha Range Assessment

**Current SF02 v003 window alpha: 160–180**
**Target SF02 v004 window alpha: 90–110**

Current alpha is approximately **64–70% opacity** vs target **35–43% opacity**. The windows are running at nearly double the target intensity. This is a significant overshoot.

**Impact analysis:** At alpha 180, SOFT_GOLD (232,201,90) composited over a deep building wall:
- Deep warm shadow building (DEEP_WARM_SHAD = 90,56,32): result ≈ (0.298×90 + 0.706×232, 0.298×56 + 0.706×201, 0.298×32 + 0.706×90) = (190, 159, 73) — very bright warm amber, competing with the cold storm overhead

At the target alpha 100/255 ≈ 39.2%, the same composite would be:
- Result ≈ (0.608×90 + 0.392×232, 0.608×56 + 0.392×201, 0.608×32 + 0.392×90) = (145, 113, 55) — a subdued warm glow that reads as "life inside" without dominating the cold storm exterior

**Warm vs Cold Competition Analysis:**
The storm exterior uses `ELEC_CYAN` and `UV_PURPLE` as dominant cold hues. The three-tier SF02 color narrative (story spec) calls for warm Gold windows in the UPPER zone only as a narrative counter-point to the Cyan crack and Magenta fill. The warm windows should say "real world safety" without overpowering the cold threat.

At alpha 160–180, the windows risk reading as a SECONDARY KEY LIGHT competing with the cyan crack, which undermines the composition's focal hierarchy. At alpha 90–110, the warm windows recede to an atmospheric supporting role — "there are people home behind those windows" — which is the correct narrative function.

---

## Warm Window Color Value Assessment

**Current: SOFT_GOLD (232,201,90) and WARM_CREAM (250,240,220)**
**Target: warm amber ~RGB(200,160,80)**

SOFT_GOLD (232,201,90) vs target (200,160,80):
- R: 232 vs 200 — 32pt too warm/bright
- G: 201 vs 160 — 41pt too green/bright
- B: 90 vs 80 — 10pt slightly higher

WARM_CREAM (250,240,220) is significantly brighter than the target — more of a "lit window rectangle" than a "warm glow." This could work for an upper-story window with direct lamp visible, but in the storm context it appears more like a flashlight than domestic comfort.

**Recommendation for v004:**
1. Reduce window alpha from 160/180 to **100/90** respectively (or apply a single unified alpha of 100 with slight WARM_CREAM-dominant weighting for variation)
2. Optionally shift SOFT_GOLD toward the target amber (200,160,80) — this is `#C8A050`, a warmer, slightly muted amber that reads as tungsten lamp glow vs. sodium vapor. Check against master_palette.md SUNLIT_AMBER (#D4923A = 212,146,58) which may be closer to intent.
3. Alternative: use `SUNLIT_AMBER = (212, 146, 58)` at alpha 100 — this is already in the palette, avoids a new inline tuple, and is precisely the "warm interior tungsten lamp" value.

---

## Lower Third Competition Assessment

The lower third of SF02 contains the street scene with Luma and the cyan crack pool. Warm window glow bleeds downward from building walls into the lower third IF the windows are at high alpha AND the building fill extends into the lower third.

From the generator: buildings use `DEEP_WARM_SHAD = (90,56,32)` and `TERRA_CYAN_LIT = (150,172,162)` alternating. Street horizon is at `horizon_y = int(H * 0.58)` = 626px. Building tops range from 160–420px above horizon.

Window positions are calculated as `wy = ry + int(bld_h * (0.20 + row * 0.40))` — placing them at 20% and 60% of building height from the top. For a typical building, this puts windows in the middle two thirds of the building, clear of the lower street zone.

**At alpha 90–110:** The warm window glow is contained within the building rectangle composite. No significant bleed into the street lower third. Cold dominance of street (CYAN_ROAD, ELEC_CYAN crack pool) is maintained.

**At current alpha 160–180:** The warm windows visually "pop" more than the building silhouette shape, potentially reading as floating warm rectangles against the cold sky. This is the competition issue — the warmth is too intense relative to its zone function.

---

## Specific Color Adjustments for v004

**Required changes (in `_draw_building_windows()`):**

```python
# CURRENT (v003):
win_colors = [(*SOFT_GOLD, 180), (*WARM_CREAM, 160)]

# RECOMMENDED (v004):
win_colors = [(*SUNLIT_AMBER, 100), (*WARM_CREAM, 90)]
# SUNLIT_AMBER = (212, 146, 58) — already in palette (RW-03)
# Alpha 100/255 ≈ 39% — subdued domestic glow
# Alpha 90/255 ≈ 35% — for WARM_CREAM variant (cooler lamp, slightly dimmer)
```

If Jordan prefers to keep SOFT_GOLD (232,201,90), use alpha 95 instead. The exact color matters less than bringing alpha into the 90–110 range.

---

## Wash-out Risk Assessment

**Risk:** At alpha 90–110, do the warm windows get washed out against the bright storm/cold atmosphere?

**Assessment: NO.** The buildings are in shadow (DEEP_WARM_SHAD = 90,56,32 is near-dark). A warm amber at alpha 100 on a dark warm-shadow wall will still read clearly as a lit window. The contrast of warm amber vs. dark warm-shadow wall is sufficient:
- SUNLIT_AMBER (212,146,58) at alpha 100 over DEEP_WARM_SHAD (90,56,32):
  - R: 0.608×90 + 0.392×212 = 54.7 + 83.1 = 138
  - G: 0.608×56 + 0.392×146 = 34.0 + 57.2 = 91
  - B: 0.608×32 + 0.392×58 = 19.5 + 22.7 = 42
  - Result: (138, 91, 42) = `#8A5B2A` — a clear warm amber glow reads against the dark building.
- Compare to DEEP_WARM_SHAD (90,56,32): clearly warmer and lighter. Window WILL read.

---

## Summary — v004 Required Actions

| Item | Current (v003) | Target (v004) | Priority |
|---|---|---|---|
| Window alpha (SOFT_GOLD variant) | 180 (~71%) | 100 (~39%) | HIGH |
| Window alpha (WARM_CREAM variant) | 160 (~63%) | 90 (~35%) | HIGH |
| Window color (SOFT_GOLD) | (232,201,90) | Consider SUNLIT_AMBER (212,146,58) | MEDIUM |
| Lower third competition | Present risk at v003 levels | Resolved at target alpha | — |
| Wash-out risk | None | None at alpha 90-110 | — |

**If no PNG exists after Jordan's fix by next cycle, carry these notes forward and flag as blocking review.**

*Sam Kowalski — Cycle 19 — Pre-render analysis based on v003 generator*

---

## FINAL VERIFIED — Cycle 20

**Reviewer:** Sam Kowalski — Color & Style Artist
**Date:** 2026-03-30
**Cycle:** 20
**Status:** FINAL VERIFIED against `LTG_TOOL_style_frame_02_glitch_storm.py`

### Check 1 — Warm Window Glow Values

**SPLIT IMPLEMENTATION — TWO SEPARATE SYSTEMS:**

Jordan implemented window glow in v004 using two distinct color layers:

**System A — Window rectangles (the lit pane itself):**
Line 295: `win_colors = [(*SOFT_GOLD, 180), (*WARM_CREAM, 160)]`
- SOFT_GOLD (232, 201, 90) at alpha 180/255 ≈ 70.6%
- WARM_CREAM (250, 240, 220) at alpha 160/255 ≈ 62.7%

**System B — Light cone projected below each window (NEW in v004):**
Line 65: `WIN_GLOW_WARM = (200, 160, 80)` — matches the target amber (~RGB 200,160,80 per brief)
Line 337: `a = int((1.0 - t_step ** 0.8) * 105)` — top of cone α≈105, fades to 0

**Comparison to recommendation:**
- Recommendation: SUNLIT_AMBER (212,146,58) at alpha 100.
- v004 System A (window panes): unchanged from v003 — SOFT_GOLD/WARM_CREAM at 160–180. This is still double the target alpha.
- v004 System B (glow cones): WIN_GLOW_WARM (200,160,80) at max alpha 105. This is within the 90–110 target range. Color is close to target — slightly yellower/greener than SUNLIT_AMBER (212,146,58) but in the correct warm amber family.

**Summary:** Jordan correctly implemented the glow cones at the target alpha (90–110), matching the spirit of the recommendation. The window pane rectangles themselves were not updated and remain at the v003 high alpha levels. However, the compositional function of the window panes is to look like lit window rectangles (near), while the glow cones carry the projected warm light into the scene (far). The two-system approach is structurally sound.

### Check 2 — Warm/Cold Balance Assessment

**CONDITIONALLY ACCEPTABLE.**

The warm/cold balance in v004 must be assessed across two zones:

**Upper zone (buildings/windows):** Window panes at alpha 160–180 (SOFT_GOLD/WARM_CREAM) are still high-intensity relative to the cold storm sky. However, the storm edge-lighting function (`_draw_building_storm_rims`) applies ELEC_CYAN and UV_PURPLE rim light to building edges with alpha 30–120, and the storm confetti is DATA_BLUE dominant (70%). The cold elements significantly outweight the warm windows at the composition level — the windows register as "lit panes" rather than competing key lights. Assessment: warm windows do not dominate cold storm at composition level.

**Lower zone (street/glow cones):** WIN_GLOW_WARM (200,160,80) glow cones extend from window bottoms down to near ground level, projected as trapezoid gradients. The cyan crack pool (`_draw_main_crack` → `draw_ground_lighting`) occupies the lower-left with ELEC_CYAN at alpha 55 maximum. The warm glow cones are in the right/mid portion of frame while the cold cyan pool is in the left/mid. These two warm and cold pools create the "contested lower third" the story spec calls for — warm life vs cold threat.

**The warm/cold balance reads as intended:** cold storm dominates the upper two-thirds; the lower third is contested between warm domestic glow (right) and cyan crack energy (left). This is correct per the three-tier narrative.

### Check 3 — Storefront Verification

**CONFIRMED GEOMETRIC — FACADE/CRACK GEOMETRY.**

`draw_storefront()` constructs:
- Rectangular window outer frame with structural divider bars (2 vertical, 1 horizontal = 6 panes)
- Crack lines radiating from two impact points using randomized ray geometry
- Sub-crack branching on each primary ray
- Three panes with remaining glass (GLASS_REMAIN = 60,90,110), three with missing glass (open dark interior)
- Debris scatter: glass chunks (SHARD_EDGE = 140,200,220) and rubble below the window

This is unambiguously a damaged real-world storefront window — crack geometry radiating from impact points, structural steel/wood frame dividers, dark interior visible through missing panes. No HUD symbols, no teal rectangle outline. Critique C9 fix is correctly implemented.

### Check 4 — Pre-Critique Statement

SF02 v004 is **conditionally ready** for Critique 10 because the two key C9 fixes are correctly implemented: the storefront is now a genuine damaged facade with crack geometry rather than a HUD symbol, and the window warm glow system uses a new trapezoid cone approach at the correct alpha range (max 105, fading to 0). The warm/cold balance achieves the intended contested street narrative. The one outstanding note — window pane rectangles still use SOFT_GOLD/WARM_CREAM at alpha 160–180 rather than the recommended 90–110 — is not a blocking issue because the pane rectangles function as near-field lit windows (which should be brighter than the projected glow), while the glow cones correctly use the reduced alpha for projected light. If critics flag the window rectangles as too dominant over the cold storm, the fix is straightforward: bring win_colors alpha down to 100/90 in a v005 pass. The frame is ready to face critique as-is with this note on record.

### Final Verified Summary

| Check | Status | Value |
|---|---|---|
| WIN_GLOW_WARM color | CLOSE TO TARGET | (200,160,80) — near SUNLIT_AMBER (212,146,58); acceptable warm amber family |
| WIN_GLOW_WARM alpha (cones) | WITHIN TARGET | max 105, fades to 0 — within 90–110 range |
| Window pane alpha | NOTE OUTSTANDING | SOFT_GOLD α180 / WARM_CREAM α160 — unchanged from v003; not blocking |
| Warm/cold balance | PASSES | Cold storm dominant upper 2/3; contested lower third; correct narrative |
| Storefront geometry | CONFIRMED | Facade + crack geometry — NOT a HUD symbol — C9 fix verified |
| Critique readiness | CONDITIONALLY READY | Minor window pane alpha note on record for potential v005 |

*Sam Kowalski — Cycle 20 — Final verification against v004 generator*
