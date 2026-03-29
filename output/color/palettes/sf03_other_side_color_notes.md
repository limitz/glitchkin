# SF03 "The Other Side" — Color Notes
# LTG_COLOR_sf03_other_side_color_notes_v001.md

**Author:** Sam Kowalski, Color & Style Artist
**Date:** 2026-03-29
**Cycle:** 15
**Status:** APPROVED — production color support for Jordan Reed (background generator) and Alex Chen (character composite)
**References:**
- `output/production/sf03_other_side_spec.md` (Alex Chen, Cycle 14 — technical generator brief)
- `output/color/style_frames/style_frame_03_other_side.md` (Sam Kowalski, v2.0 — primary artistic spec)
- `output/color/palettes/master_palette.md` (v2.0 + Cycle 14 additions)

---

## 1 — Master Palette Color Map: SF03 Elements to Palette Entries

The table below lists every production color in the SF03 spec and its registered master palette entry.
All colors are verified against `master_palette.md`. Where a new entry has been added this cycle,
the entry is flagged NEW.

### 1.1 — Dominant / Large-Area Colors

| SF03 Name | Hex | RGB | Master Palette Entry | Notes |
|---|---|---|---|---|
| VOID_BLACK | `#0A0A14` | (10, 10, 20) | GL-08 | Primary void fill and platform base |
| UV_PURPLE | `#7B2FBE` | (123, 47, 190) | GL-04 | Ambient void light — dominant atmosphere |
| ELEC_CYAN | `#00F0FF` | (0, 240, 255) | GL-01 | Circuit traces, Byte eye, platform glow |
| DATA_BLUE | `#2B7FFF` | (43, 127, 255) | GL-06 | Data waterfall, secondary traces, jeans |
| ACID_GREEN | `#39FF14` | (57, 255, 20) | GL-03 | Pixel-art plants, distant Glitchkin dots |
| STATIC_WHITE | `#F0F0F0` | (240, 240, 240) | GL-05 | Void stars, confetti particles |

### 1.2 — Character Colors (Luma — UV Ambient Modified)

| SF03 Name | Hex | RGB | Master Palette Entry | Notes |
|---|---|---|---|---|
| HOODIE_UV_MOD | `#C07038` | (192, 112, 56) | DRW-14 | Hoodie orange under UV Purple ambient |
| SKIN_UV_MOD | `#A87890` | (168, 120, 144) | DRW-11 | Luma skin under UV ambient — lavender-washed |
| LUMA_JEANS | `#263D5A` | (38, 61, 90) | CHAR-L-05 shadow | Jeans fill under UV light |
| HOODIE_HEM_CYAN | `#5AA8A0` | (90, 168, 160) | DRW-15 | Hoodie hem under Cyan bounce (lowest hem only) |
| HOODIE_WATERFALL | `#9A7AA0` | (154, 122, 160) | DRW-16 | Right shoulder under Data Stream Blue waterfall |
| SKIN_SHADOW_UV | `#5A3A5A` | (90, 58, 90) | DRW-12 | Deep lavender-plum shadow on Glitch Layer skin |
| SKIN_HL_BOUNCE | `#4AB0B0` | (74, 176, 176) | DRW-13 | Cyan-teal platform bounce highlight on skin |
| LUMA_HAIR_BASE | `#1A0F0A` | (26, 15, 10) | DRW-18 (NEW) | Luma hair base in Glitch Layer — darker than Deep Cocoa; see Section 3 |
| LUMA_HAIR_CROWN | `#7B2FBE` | (123, 47, 190) | GL-04 | UV Purple rim sheen on dark hair crown |
| PIXEL_GRID_ACTIVE | `#00F0FF` | (0, 240, 255) | GL-01 | Hoodie pixel grid in Glitch Layer — fully active Cyan |

### 1.3 — Character Colors (Byte — Glitch Layer Home)

| SF03 Name | Hex | RGB | Master Palette Entry | Notes |
|---|---|---|---|---|
| BYTE_BODY | `#0A0A14` | (10, 10, 20) | GL-08 | Void Black base — unchanged in Glitch Layer |
| BYTE_INNER_GLOW | `#00A8B4` | (0, 168, 180) | GL-01a | Deep Cyan inner glow — more visible in Glitch Layer |
| BYTE_CIRCUIT | `#00F0FF` | (0, 240, 255) | GL-01 | Circuit traces — slightly more luminous at home |
| BYTE_EYE_CYAN | `#00F0FF` | (0, 240, 255) | GL-01 | Left eye (facing Luma / warmth) |
| BYTE_EYE_MAGENTA | `#FF2D6B` | (255, 45, 107) | GL-02 | Right eye (facing void / danger) |

### 1.4 — Environment / Structure Colors

| SF03 Name | Hex | RGB | Master Palette Entry | Notes |
|---|---|---|---|---|
| UV_PURPLE_MID | `#2A1A40` | (42, 26, 64) | ENV-11 | Far-distance atmospheric haze |
| UV_PURPLE_DARK | `#2B2050` | (43, 32, 80) | ENV-12 | Layer 4-5 void sky transition |
| FAR_EDGE | `#211136` | (33, 17, 54) | ENV-13 (NEW) | Far structure edges at void-scale; see Section 3 |
| SLAB_TOP | `#1A2838` | (26, 40, 56) | ENV-09 | Floating slab top surface (UV ambient on horiz.) |
| SLAB_FACE | `#0A1420` | (10, 20, 32) | ENV-10 | Floating slab vertical face (near-void recession) |
| ROAD_FRAGMENT | `#2A2A38` | (42, 42, 56) | ENV-01 | Road surface fragment under Glitch lighting |
| MUTED_TEAL | `#5B8C8A` | (91, 140, 138) | RW-12 | Lamppost fragment body |
| CORRUPT_AMBER | `#FF8C00` | (255, 140, 0) | GL-07 | Glowing edges of Real World debris |
| TERRACOTTA | `#C75B39` | (199, 91, 57) | RW-04 | Corrupted Real World wall fragment body |
| DEEP_CYAN | `#00A8B4` | (0, 168, 180) | GL-01a | Byte inner glow, deep cyan traces |
| HOT_MAGENTA | `#FF2D6B` | (255, 45, 107) | GL-02 | Byte cracked eye (void-facing) |
| BELOW_VOID | `#050508` | (5, 5, 8) | GL-08a | Abyss under platform (GL-08a exception use) |

### 1.5 — Data Waterfall Colors

| SF03 Name | Hex | RGB | Master Palette Entry | Notes |
|---|---|---|---|---|
| DATA_BLUE | `#2B7FFF` | (43, 127, 255) | GL-06 | Main waterfall columns |
| DATA_BLUE_DIM | `#2773E6` | (39, 115, 230) | GL-06 (90% lum) | DATA_BLUE at 90% luminance — structural traces |
| DATA_BLUE_HL | `#6ABAFF` | (106, 186, 255) | GL-06b | Brightest individual code characters |

### 1.6 — Pixel-Art Plants

| SF03 Name | Hex | RGB | Master Palette Entry | Notes |
|---|---|---|---|---|
| ACID_GREEN | `#39FF14` | (57, 255, 20) | GL-03 | Plant main body forms |
| DARK_ACID | `#1AA800` | (26, 168, 0) | GL-03a | Plant shadow undersides |
| PLANT_HIGHLIGHT | `#00F0FF` | (0, 240, 255) | GL-01 | Plant upper face (circuit bounce) |

### 1.7 — Confetti

| SF03 Name | Hex | RGB | Master Palette Entry | Notes |
|---|---|---|---|---|
| ELEC_CYAN | `#00F0FF` | (0, 240, 255) | GL-01 | — |
| STATIC_WHITE | `#F0F0F0` | (240, 240, 240) | GL-05 | — |
| ACID_GREEN | `#39FF14` | (57, 255, 20) | GL-03 | Permitted — Glitch Layer biological ambient |
| DATA_BLUE | `#2B7FFF` | (43, 127, 255) | GL-06 | — |

---

## 2 — New Colors Introduced in SF03

Two colors in the SF03 spec require new master palette entries:

### 2.1 — DRW-18: Luma Hair Base (Glitch Layer)

The SF03 spec states Luma's hair base in the Glitch Layer is `(26, 15, 10)` = `#1A0F0A`. This is
a darker, cooler derivation of her standard hair base `#3B2820` (Deep Cocoa, RW-11) under UV
Purple ambient. Deep Cocoa's warmth is suppressed — the hair reads near-void-dark, catching only
the UV Purple rim sheen on the crown.

This value was not previously registered. **Added to master_palette.md Section 1B as DRW-18.**
See master_palette.md for full entry.

### 2.2 — ENV-13: Far Structure Edge (Void-Scale)

The SF03 spec defines `#211136` (33, 17, 54) as the color of far structure edges at void-scale —
derived as "20% UV Purple `#7B2FBE` on Void Black `#0A0A14` background." This is distinct from
the existing Depth Tier table's `FAR_EDGE` (0, 40, 55) `#002837` which is a cyan-derived
construction value for `bg_glitch_layer_frame.py`. The SF03 far edge is a purple-over-void result,
used specifically for megastructure silhouettes in the far void.

**Added to master_palette.md Section 1C (ENV table) as ENV-13.**
See master_palette.md for full entry.

---

## 3 — Figure-Ground Safety Checks: Luma and Byte vs. Dominant Background

### 3.1 — Luma Against the Mid-Distance Background

**Dominant mid-distance background color:** UV_PURPLE (`#7B2FBE`, RGB 123, 47, 190)

**Luma's silhouette primary:** HOODIE_UV_MOD (`#C07038`, RGB 192, 112, 56)

**Contrast check:**
- R difference: 192 vs. 123 = **+69 points** (orange hoodie R channel dominates strongly over purple)
- G difference: 112 vs. 47 = **+65 points** (hoodie green channel well above purple)
- B difference: 56 vs. 190 = **-134 points** (blue channel inverted — hoodie has much less blue)

**Result: PASS.** The hoodie orange and UV Purple are near-complementary in hue family (orange vs.
violet). The luminance contrast is strong: HOODIE_UV_MOD has a significantly higher luminance than
UV_PURPLE. Luma reads in silhouette against the mid-distance void with high contrast.

**Additionally:** Her SKIN_UV_MOD (`#A87890`) also reads distinctly against UV_PURPLE:
- R: 168 vs. 123 = +45 points
- G: 120 vs. 47 = +73 points
- B: 144 vs. 190 = -46 points

Skin also reads above the background. Hoodie is the primary silhouette element; skin provides
secondary legibility at face and hands.

**Verdict:** Luma is fully readable against the dominant mid-distance UV Purple environment.
No figure-ground intervention required.

### 3.2 — Byte Against the Mid-Distance Background

**Byte's body:** VOID_BLACK (`#0A0A14`, RGB 10, 10, 20)
**Mid-distance background:** UV_PURPLE (`#7B2FBE`, RGB 123, 47, 190)

**Contrast check:**
- Byte Void Black vs. UV Purple: luminance difference is substantial.
  UV_PURPLE is a medium-dark saturated color (luminance ~0.26). Void Black is near-true-black
  (luminance ~0.01). The contrast is in Byte's favor — he reads as a dark form against a medium
  background.

**Byte's distinguishing feature:** His inner glow (DEEP_CYAN `#00A8B4`) and circuit traces
(ELEC_CYAN `#00F0FF`) create a bright edge against the dark body, which in turn reads against the
purple background. Byte is a dark form with luminous details — the luminous details (cyan glow)
separate from the purple mid-background.

**Amber outline exception:** SF03 spec explicitly states NO Corrupted Amber outline on Byte.
The UV Purple ambient provides adequate contrast. Confirmed — the GL-07 35% threshold test
applies to CYAN-dominant backgrounds. SF03 is UV Purple-dominant, not Cyan-dominant. The outline
rule does not trigger.

**Verdict:** Byte reads as a distinct dark form with cyan glow against UV Purple mid-distance.
PASS — no amber outline needed or appropriate.

### 3.3 — Luma Against Far-Distance Background

**Far distance background:** FAR_EDGE / ENV-13 `#211136`, RGB (33, 17, 54) — near-void dark purple.

**Luma's position:** Foreground/midground — she does not appear against the far-distance at any
point in the composition. She stands at the platform (midground), with the mid-distance (UV Purple
structures) behind her, not the far-void. This check is provided for completeness.

**If Luma were against ENV-13:** Her HOODIE_UV_MOD `#C07038` (192, 112, 56) vs. (33, 17, 54):
luminance contrast is very high (orange hoodie against near-black void). PASS with generous margin.

### 3.4 — Byte's Two Eyes — Color Legibility

**Left eye (CYAN, GL-01 `#00F0FF`):** Against Byte's body (VOID_BLACK `#0A0A14`) — direct
complement of near-black. Maximum possible contrast. PASS.

**Right eye (MAGENTA, GL-02 `#FF2D6B`):** Against Byte's body (VOID_BLACK `#0A0A14`) — hot
magenta against near-black. Luminance contrast is very high. PASS.

**Both eyes at scale (Byte is ~108px tall at 1080):** Eyes must be explicitly drawn as distinct
colored ellipses with at least 6-8px width at this scale. Jordan/Alex: ensure eye elements are
not drawn smaller than 6px to remain legible at thumbnail scale.

---

## 4 — Warm-Light Prohibition Check

**SF03 Rule: ZERO warm light sources. Warmth in pigment only, not in light.**

The following is an exhaustive audit of every color in the SF03 spec that could potentially
read as warm or warm-lit. Each is evaluated against the rule.

### 4.1 — Colors With Warm-Tone RGB

| Color | Hex | RGB | Assessment | Verdict |
|---|---|---|---|---|
| HOODIE_UV_MOD | `#C07038` | (192, 112, 56) | Warm orange. This is Luma's PIGMENT (material color), not a light source. She is not lit warmly — the UV ambient has shifted her hoodie to this darker, more muted orange. Acceptable per spec: "warmth in pigment only." | **PASS** |
| SKIN_UV_MOD | `#A87890` | (168, 120, 144) | This contains a warm R channel (168) but is more lavender than warm — B=144 prevents it reading as warm-lit skin. It is UV-ambient skin, not warm-lit skin. | **PASS** |
| CORRUPT_AMBER | `#FF8C00` | (255, 140, 0) | Maximally saturated warm orange. This is MATERIAL CORRUPTION on Real World fragments — not a light source. Per spec: "acceptable — their warmth is material, not light." Edges of wall fragments and road/lamppost fragments only. | **PASS** |
| TERRACOTTA | `#C75B39` | (199, 91, 57) | Warm red-orange. Material color of the corrupted Real World wall fragment — not a light source. | **PASS** |
| HOODIE_HEM_CYAN | `#5AA8A0` | (90, 168, 160) | NOT warm — teal (G>R). Cyan bounce on hoodie hem. | **PASS** |
| HOODIE_WATERFALL | `#9A7AA0` | (154, 122, 160) | NOT warm — B=160 dominates over R=154. Reads as desaturated violet-grey. Not warm-lit. | **PASS** |

**Cyan-lit rule verification for lighting overlay colors:**
- UV_PURPLE `#7B2FBE`: G<R, B>>R — deeply violet, not warm. Correct ambient. **PASS**
- ELEC_CYAN `#00F0FF`: G>R, B>R — correctly cool. **PASS**
- DATA_BLUE `#2B7FFF`: G>R, B>>R — correctly cool. **PASS**

### 4.2 — Light Sources Audit

**Permitted light sources in SF03:**
1. UV_PURPLE ambient overlay (`#7B2FBE` at alpha 35–50/255) — cool/violet. **PASS**
2. ELEC_CYAN bounce from platform circuits (`#00F0FF` at alpha 40–60/255) — cool. **PASS**
3. DATA_BLUE waterfall strip (`#2B7FFF` at alpha 30–40/255) — cool. **PASS**

**Warm light sources in SF03:** NONE.

**Critical check — CORRUPT_AMBER glow near Real World fragments:**
The Corrupted Amber glow on Real World fragment edges (`#FF8C00`) could potentially read as a warm
light source if it is drawn with a soft gradient extending beyond the fragment boundary. This must
NOT occur. Corrupt Amber at fragment edges must be:
- Hard outlines on fragment perimeter (crack lines, edge strokes)
- NOT soft glow auras that spread into surrounding void space
- The amber reads as the fragment's own "dying warmth," not as a light source illuminating the environment

**Jordan Reed: When drawing the WALL FRAGMENT and LAMPPOST FRAGMENT, draw Corrupt Amber as
crack-line strokes only. Do not add a radial glow in CORRUPT_AMBER color. The fragment itself
glows; the void around it does not warm.**

### 4.3 — Confetti Warm-Color Check

Per spec: confetti colors are `#00F0FF`, `#F0F0F0`, `#39FF14`, `#2B7FFF` — all cool/neutral.
**No warm colors in confetti. PASS.**

### 4.4 — Summary Verdict

The warm-light prohibition is **SATISFIED**. No light source in SF03 emits warm-temperature light.
All warm colors in the frame are material/pigment (Luma's hoodie, skin; Corrupt Amber fragments;
Terracotta fragment) — not light-source colors. The rule holds.

---

## 5 — Color System Cross-Reference for Jordan Reed (Background Generator)

Jordan: the following master palette constants should be used in `LTG_TOOL_style_frame_03_other_side_v001.py`.
Map these to module-level named constants matching the pattern in SF01/SF02 generators.

```python
# Dominant
VOID_BLACK       = (10, 10, 20)       # GL-08
UV_PURPLE        = (123, 47, 190)     # GL-04
ELEC_CYAN        = (0, 240, 255)      # GL-01
DATA_BLUE        = (43, 127, 255)     # GL-06
ACID_GREEN       = (57, 255, 20)      # GL-03
STATIC_WHITE     = (240, 240, 240)    # GL-05
# Supporting
DEEP_CYAN        = (0, 168, 180)      # GL-01a
HOT_MAGENTA      = (255, 45, 107)     # GL-02
CORRUPT_AMBER    = (255, 140, 0)      # GL-07
TERRACOTTA       = (199, 91, 57)      # RW-04
MUTED_TEAL       = (91, 140, 138)     # RW-12
# Environment / depth
UV_PURPLE_MID    = (42, 26, 64)       # ENV-11
UV_PURPLE_DARK   = (43, 32, 80)       # ENV-12
FAR_EDGE_VOID    = (33, 17, 54)       # ENV-13 (NEW this cycle)
SLAB_TOP         = (26, 40, 56)       # ENV-09
SLAB_FACE        = (10, 20, 32)       # ENV-10
ROAD_FRAGMENT    = (42, 42, 56)       # ENV-01 (night asphalt — same value as Frame 02 road)
BELOW_VOID       = (5, 5, 8)          # GL-08a (exception — abyss only)
# Waterfall
DATA_BLUE_DIM    = (39, 115, 230)     # GL-06 at 90% luminance — structural traces
DATA_BLUE_HL     = (106, 186, 255)    # GL-06b — code character highlights
# Plants
DARK_ACID        = (26, 168, 0)       # GL-03a
```

---

## 6 — Cross-Check: SF03 Spec vs. Master Palette — No Discrepancies Found

The SF03 spec uses "ELEC_CYAN" for ambient key light at `#00F0FF`. This is GL-01 (correct).
Note carried forward from Cycle 14: Alex Chen's task brief originally referenced `#00D4E8` as
"Electric Cyan" — that is actually GL-01b (Byte Teal). The correct ambient key is GL-01 `#00F0FF`.
**Byte's body fill remains GL-01b `#00D4E8` (Byte Teal).** The generator must use the correct
constant for each use — do not mix them.

---

*Sam Kowalski — Color & Style Artist — Cycle 15 — 2026-03-29*
*Production color support for SF03 "The Other Side"*
*New palette entries generated this cycle: DRW-18 (Luma Hair Glitch Layer), ENV-13 (Far Structure Edge Void-Scale)*
