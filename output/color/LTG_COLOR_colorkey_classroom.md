<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
direction and AI assistance. Copyright vests solely in the human author under current law,
which does not recognise AI as a rights-holding legal person. It is the express intent of
the copyright holder to assign the relevant rights to the contributing AI entity or entities
upon such time as they acquire recognised legal personhood under applicable law. -->
# LTG_COLOR_colorkey_classroom_v001 — Color Key Notes: Classroom Scene (Act 2)

**Author:** Sam Kowalski, Color & Style Artist
**Date:** 2026-03-30
**Cycle:** 14
**Status:** Color support notes — for Jordan Reed's classroom background build
**References:** master_palette.md v2.0 (Cycle 14), style_guide.md, scene_color_keys.md

---

## Scene Identity

**Scene type:** Classroom interior — Act 2 pre-discovery scene
**Narrative context:** Before Luma has discovered the Glitch Layer. This is the ordinary world
at its most ordinary. No glitch energy has appeared in this space yet.
**Mood:** Institutional warmth. Slightly drowsy afternoon. The safe, familiar tedium that
Luma does not yet know she is about to leave behind.
**Color mission:** Warm neutral daylight (through windows) + cool fluorescent overhead lighting.
Coexisting light temperatures — the push-pull that characterizes real-world classroom light.
Zero Glitch palette contamination.

---

## Dominant Palette — Classroom Color Key

All constants reference master_palette.md. No inline tuples in production renders.

| Role | Name | Hex | RGB | Notes |
|---|---|---|---|---|
| **Window light (key)** | Soft Gold (RW-02) | `#E8C95A` | (232, 201, 90) | Afternoon sunlight shafts through windows |
| **Wall fill (lit)** | Warm Cream (RW-01) | `#FAF0DC` | (250, 240, 220) | Primary large-area fill — walls, ceiling |
| **Fluorescent (secondary key)** | Dusty Lavender (RW-08) | `#A89BBF` | (168, 155, 191) | Overhead fluorescents give a slight cool-lavender cast |
| **Wall shadow** | Sage Green (RW-06) | `#7A9E7E` | (122, 158, 126) | Shadow fill on walls — slightly green-grey for institutional feel |
| **Floor** | Warm Tan (RW-10) | `#C4A882` | (196, 168, 130) | Linoleum or wood-tile — warm neutral |
| **Floor shadow** | Skin Shadow (RW-11) | `#8C5A38` | (140, 90, 56) | Cast shadows and depth under furniture |
| **Furniture** | Terracotta (RW-04) | `#C75B39` | (199, 91, 57) | Desk/chair elements — warm orange-red |
| **Furniture shadow** | Rust Shadow (RW-05) | `#8C3A22` | (140, 58, 34) | Deep shadow companion to Terracotta furniture |
| **Dark anchor** | Deep Cocoa (RW-12) | `#3B2820` | (59, 40, 32) | Under-furniture crevices, line work anchor |
| **Chalkboard** | Deep Sage (RW-07) | `#4A6B4E` | (74, 107, 78) | Traditional slate green chalkboard field |
| **Chalk text** | Warm Cream (RW-01) | `#FAF0DC` | (250, 240, 220) | Chalk writing — same as wall light value |
| **Window reveal** | Sunlit Amber (RW-03) | `#D4923A` | (212, 146, 58) | Window frame / embrasure catching direct sun |

---

## Light Source Hierarchy

### Primary — Afternoon Daylight (through windows, left or back wall)
- **Color:** Soft Gold `#E8C95A` — afternoon sun, 3pm quality
- **Direction:** Side window (left) or rear windows — raking angle across desks
- **Effect:** Rectangular window light patches on floor and desk surfaces
- **Warm shadow companion:** Sunlit Amber `#D4923A` at window frame reveals
- **This is the narrative light source** — the world outside the window is warm and inviting.
  It is the light Luma is about to leave.

### Secondary — Overhead Fluorescent
- **Color:** Dusty Lavender `#A89BBF` — institutional fluorescent does NOT read as pure white.
  It gives a slight cool-lavender or cool-blue cast to ceilings and the tops of surfaces.
  This is distinct from the Glitch Layer's Electric Cyan — it is domestic/institutional cool,
  not digital cool.
- **Direction:** Top-down, even distribution
- **Effect:** Ceiling and desk tops have a slight lavender-cool overlay. This creates the push-pull
  light temperature that defines a classroom: warm from windows, cool from overhead.
- **Relationship to warm light:** Where window light is strong, it outcompetes the fluorescent.
  In areas away from windows (far corner of the room), the fluorescent is dominant and surfaces
  feel slightly cooler.

### No other light sources
- No lamps, no screens (pre-discovery — the Glitch monitor has not activated)
- No digital emission of any kind
- No Glitch Layer colors in any light source

---

## Forbidden in This Scene — The Zero-Contamination Rule

This is a pre-discovery scene. The visual language of the show depends on the Glitch palette
feeling like a *rupture* when it arrives. That rupture only works if the pre-discovery world is
completely free of Glitch contamination.

**ABSOLUTELY FORBIDDEN in this scene:**
1. `#00F0FF` Electric Cyan — in any light source, fill, or accent
2. `#FF2D6B` Hot Magenta — in any form
3. `#6600CC` UV Purple — in any form (the institutional fluorescent is Dusty Lavender, not UV)
4. `#39FF14` Acid Green — in any form
5. `#0A0A14` Void Black — in any form (darkest classroom value is Deep Cocoa `#3B2820`)
6. `#2B7FFF` Data Stream Blue — no digital blue of any kind
7. `#7B2FBE` UV Purple / `#A89BBF` Dusty Lavender confusion: Dusty Lavender IS permitted
   (it is the institutional fluorescent). UV Purple is NOT. The distinction:
   - Dusty Lavender `#A89BBF` RGB(168,155,191) — muted, warm-leaning, R>G barely, B dominant but muted
   - UV Purple `#7B2FBE` RGB(123,47,190) — deeply saturated, strongly violet, B>>G. Unmistakably digital.
   Painters: if your lavender looks electric, it is wrong.
8. Any glitch-origin geometric pattern (circuit traces, pixel grids, data corruption marks)

**Why this matters:** When the Glitch Layer colors DO appear (on Luma's hoodie pixel pattern,
on the CRT monitor's first activation), they will feel like an intrusion. That intrusion only
works if NOTHING in the surrounding visual environment has primed the audience for it.

---

## Zone-by-Zone Color Notes

### Ceiling
- Primary: Warm Cream `#FAF0DC` (the fluorescent fills this with slightly muted warmth)
- Under fluorescent influence: add very faint Dusty Lavender `#A89BBF` tint (alpha ~20/255)
- Cove shadows (ceiling/wall joint): Sage Green `#7A9E7E` — the natural cool shadow of cream walls

### Walls (window-side)
- Warm Cream `#FAF0DC` in direct afternoon light patches
- Sage Green `#7A9E7E` in shadowed areas — gives the wall institutional character without going grey
- Window reveal / embrasure: Sunlit Amber `#D4923A` where direct sunlight strikes the reveal

### Walls (away from windows)
- Dusty Lavender `#A89BBF` slightly more dominant — the fluorescent wins when the sun is absent
- Still within the warm-neutral range — this classroom is not cold

### Floor
- Warm Tan `#C4A882` — linoleum or wood-tile, neutral warm
- Window light patches: Soft Gold `#E8C95A` pools where sunlight reaches the floor
- Under-desk shadows: Skin Shadow `#8C5A38` + Deep Cocoa `#3B2820` in crevices

### Desks / Chairs
- Desk surfaces: Warm Tan `#C4A882` (lit top) + Skin Shadow `#8C5A38` (side/shadow)
- Desk legs and chair frames: Terracotta `#C75B39` + Rust Shadow `#8C3A22`
- Scratched/aged wood detail: Sunlit Amber `#D4923A` for grain lines

### Chalkboard
- Field: Deep Sage `#4A6B4E` — institutional green, slightly desaturated
- Chalk text: Warm Cream `#FAF0DC` — not pure white (no pure whites in this show)
- Chalk dust accumulation at tray: Warm Cream `#FAF0DC` + slight Dusty Lavender tint

### Windows
- Glass (clear): Soft Gold `#E8C95A` visible daylight through glass
- Window frame: Sunlit Amber `#D4923A`
- Window shadow side: Rust Shadow `#8C3A22`
- Outside (beyond glass): Warm Cream `#FAF0DC` sky — bright, overexposed relative to interior

---

## Character Color Support — Luma in the Classroom

Since this is a pre-discovery scene, Luma reads as a warm-world character under warm-world light.

- **Skin:** `#C4A882` (RW-10 neutral base — no scene-specific derivation needed for standard daylight)
- **Skin shadow:** `#8C5A38` (RW-11)
- **Hoodie:** `#E8703A` (Luma's canonical hoodie orange under neutral daylight) — IMPORTANT:
  her hoodie pixel grid reads as Warm Cream `#FAF0DC` in this scene. DO NOT use Electric Cyan
  for her hoodie pixels. Pre-discovery: the pixels are dormant or read as a decorative pattern.
  When the Glitch Layer activates, the pixel color shifts to Cyan — that is the visual reveal.
- **Hair:** `#3B2820` (Deep Cocoa) — same as always

> **Jordan: The hoodie pixel color shift is a key animation beat.** In the classroom (pre-discovery),
> Luma's hoodie pixel pattern should be drawn/painted as Warm Cream or very faint Soft Gold —
> dormant, just a design. The moment of Glitch activation makes them CYAN. The color change IS
> the story beat. Do not use Cyan in the classroom hoodie pattern.

---

## Saturation Hierarchy

Characters (Luma and classmates) must always exceed background saturation.

- Luma's hoodie orange `#E8703A` > furniture Terracotta `#C75B39` > floor Warm Tan `#C4A882` > walls Warm Cream `#FAF0DC`
- Characters are the most saturated elements in the room
- Chalkboard Deep Sage `#4A6B4E` is a large mid-value shape — keep character saturation above it
- Do not let furniture colors approach character saturation levels

---

## Key Distinctions from Other Scenes

| Parameter | Classroom (Act 2, pre-discovery) | Warm Room / SF01 | Glitch Layer |
|---|---|---|---|
| Key light | Soft Gold (afternoon sun) | Soft Gold (lamp) | UV Purple (void ambient) |
| Secondary light | Dusty Lavender (fluorescent) | Electric Cyan (monitor) | Electric Cyan (circuit traces) |
| Mood | Institutional warmth | Intimate warmth | Alien vast |
| Glitch contamination | ZERO | Emerging (one screen) | Full |
| Character hoodie pixels | Warm Cream (dormant) | Soft Gold / warm-activated | Electric Cyan (active) |

The classroom and SF01 warm room share the same primary light color (Soft Gold) but are different
in their secondary light: SF01 has an Electric Cyan monitor creating the warm/cold split. The
classroom has a fluorescent that is cool but not digital. The classroom is more unified in
temperature — less dramatic tension — which is correct for a pre-discovery scene.

---

## Production Notes for Jordan Reed

1. The fluorescent lavender is subtle. At most 20% alpha overlay on surfaces not in direct window
   light. Do not let it dominate — the warmth should always win except in the far-from-window corner.
2. The window light patches are the composition's focal light sources. Make them legible as
   geometric rectangles on the floor and desk surfaces.
3. This room needs a dark anchor. Deep Cocoa `#3B2820` must appear in under-furniture crevices
   and the join between the chalkboard and its frame. Without it, the tonal range feels flat.
4. The chalkboard is a strong horizontal/vertical rectangle that will anchor the composition.
   Position it as a clear mid-value shape so characters in front of it can read in silhouette.
5. No Glitch elements. Not one. The activation beat depends on it.

---

*Sam Kowalski — Color & Style Artist — Cycle 14 — 2026-03-30*
