# Act 2 Environments — Color Brief
## "Luma & the Glitchkin"

**Author:** Sam Kowalski, Color & Style Artist
**Date:** 2026-03-29
**Cycle:** 17
**Audience:** Jordan Reed, Background / Environment Artist
**Purpose:** Production color spec for Tech Den and School Hallway environments. Ensures palette compliance, correct reading vs. Glitch Layer colors, and consistent mood/lighting.

---

## ENVIRONMENT 1 — Tech Den (Grandma Miri's Home)

### Concept
The Tech Den is the warmest, most grounded domestic space in the show. Filled with aged analog objects — CRT monitors, stacked game cartridges, shelves of books and gadgets. Miri's presence anchors the emotional temperature: this space should feel safe, slightly worn, and lived-in. The monitor glow is a critical challenge: it must read as "old analog screen" and must NOT trigger a Glitch Layer read in any frame.

### Lighting Setup
- **Key:** Daylight from LEFT window — warm amber/neutral (NOT orange, not harsh).
  - Window key: `#D4B896` RGB(212, 184, 150) — Warmed Tan, a desaturated warm amber. This is a gentler version of RW-03 (Sunlit Amber). The daylight is filtered through curtains, not direct hard sunlight.
- **Secondary fill:** Lamp warmth from Ochre Brick tone `#B8944A` RGB(184, 148, 74) — from Miri's practical desk/floor lamp. Warm ambient bouncing off walls.
- **Monitor glow:** See below — must be handled carefully.

### Key Surfaces — Specific RGB Values

| Surface | Color Name | Hex | RGB | Notes |
|---|---|---|---|---|
| Main wall | Warm Linen Wall | `#E8D8B8` | (232, 216, 184) | Aged Bone — slightly darker than Warm Cream. Decades of tea-steam and warm lamplight. |
| Wall (shadow side) | Warm Wall Shadow | `#C4A882` | (196, 168, 130) | RW-10 (Warm Tan) — same value as skin base; creates warmth in shadow without mud. |
| Floor (wooden) | Ochre Plank | `#B8944A` | (184, 148, 74) | RW-13 (Ochre Brick) — worn wooden floor, golden from decades of lamp glow. |
| Floor (deep shadow) | Floor Shadow | `#8C5A38` | (140, 90, 56) | RW-10b (Skin Shadow) — under furniture, corners. Warm brown shadow anchors the room. |
| Desk surface | Warm Dark Wood | `#8C3A22` | (140, 58, 34) | RW-05 (Rust Shadow) — aged darker wood desk. Slightly darker than floor. |
| Desk highlight | Worn Wood Sheen | `#C4A882` | (196, 168, 130) | RW-10 — specular hint on worn flat desk surface from window key. |
| Bookshelves | Deep Cocoa Wood | `#3B2820` | (59, 40, 32) | RW-11 — the darkest structural wood. Shelves recede into background. |
| CRT monitor casing | Muted Teal | `#5B8C8A` | (91, 140, 138) | RW-12 — analog aged plastic. Slightly digital but clearly desaturated/old. |
| CRT shadow side | Dark Teal Shadow | `#3A5A58` | (58, 90, 88) | RW-12a — shadow companion to Muted Teal. |

### Monitor Glow — Critical Color Safety Rule

**PROBLEM:** A blue-white monitor glow risks reading as Electric Cyan (#00F0FF, GL-01) or Byte Teal (#00D4E8, GL-01b). This is a production blocker — if the monitor reads as Glitch Layer emission, the Tech Den stops reading as a safe Real World space.

**SOLUTION — Monitor Ambient Glow:**

| Element | Hex | RGB | Notes |
|---|---|---|---|
| Monitor screen fill | `#C8D4E0` | (200, 212, 224) | Desaturated blue-white. R:200 keeps it warm enough to not read as digital cold. |
| Monitor glow ambient (on desk/face) | `#B8C8D4` | (184, 200, 212) | Even warmer, lower saturation. This is aged phosphor, not LED. No pure blue channel dominance. |
| Monitor screen dark zone | `#3A4A5A` | (58, 74, 90) | Screen shadow/inactive areas. Blue-shifted dark but not Void Black. |

**Why these values are safe:**
- Electric Cyan GL-01 = `#00F0FF` RGB(0, 240, 255). The R channel is 0 and B channel maxes. Our monitor glow has R:200 — the warm presence in the R channel alone prevents any Glitch Layer misread.
- Byte Teal GL-01b = `#00D4E8` RGB(0, 212, 232). Same issue — R:0. Our values keep R at 184-200, which shifts the glow into "aged warm-neutral" territory.
- The monitor glow must NEVER use R values below 150 in the Tech Den. If painters drift toward more saturated blue-white, this rule stops the read from breaking.

### Forbidden in Tech Den
- No Glitch Layer palette colors (GL-01 through GL-07)
- No Void Black (#0A0A14) except as deepest practical shadow under furniture against a baseboard
- No cool blue ambient as a fill — daylight is the only window, and it is warm-left

---

## ENVIRONMENT 2 — School Hallway (Millbrook Middle School)

### Concept
Institutional. Slightly depressing. The kind of hallway you have to walk through to get somewhere better. Fluorescent overhead tubes, scuffed linoleum, lockers in utilitarian colors. This space should feel neither warm nor threatening — it is the deliberate visual opposite of Grandma's Den. It is also the place where Luma is visually anonymous before the story starts.

### Lighting Setup
- **Key:** Overhead fluorescent — cool, flat, even, slightly greenish.
  - Fluorescent cast: `#D0DDD8` RGB(208, 221, 216) — a very slightly green-cool near-neutral. Not garish neon green, but enough G>B shift that it reads as institutional fluorescent rather than generic cool.
- **No directional key light.** Fluorescent tubes create a nearly even-value environment. Shadow depth comes from geometry (locker recesses, under benches), not from a light direction.

### Fluorescent Color Cast — How to Apply

The fluorescent cast modifies all surfaces slightly. Painters should shift warm surfaces toward this tone at 20-30% influence. Key rule: **warm orange tones (#C75B39, #E8703A) become slightly desaturated and greenish-cool in this light.** This is specifically relevant when Luma appears in this hallway — her orange hoodie should look slightly washed out and institutional. The moment she leaves this environment, the hoodie recovers full saturation. This color contrast IS the narrative beat about belonging.

### Key Surfaces — Specific RGB Values

| Surface | Color Name | Hex | RGB | Notes |
|---|---|---|---|---|
| Ceiling (fluorescent panels) | Institutional White | `#DDE8DF` | (221, 232, 223) | Warm white shifted green-cool by fluorescent tubes. Not pure white — slightly dingy. |
| Upper wall (above lockers) | Cool Plaster | `#C4CECC` | (196, 206, 204) | Desaturated blue-green neutral. The color of a wall that was once Warm Cream but has been under fluorescents for 20 years. |
| Lower wall (below lockers, baseboard) | Scuff Gray | `#B0BABC` | (176, 186, 188) | Slightly cooler than upper wall — collects scuffs and shadow from lockers above. |
| Locker color A (primary) | Institutional Sage | `#8A9E94` | (138, 158, 148) | Muted green-gray. The color of school equipment everywhere. Chalky, desaturated. Pairs with RW-06 (Sage Green) family but more grayed and institutional. |
| Locker color B (alternate) | Institutional Blue-Gray | `#8A96A4` | (138, 150, 164) | Muted blue-gray. Second alternating color — cool counterpart to the sage. About equal value to Locker A so the two alternate without creating a strong pattern beat. |
| Locker recesses / vent shadow | Locker Shadow | `#5A6268` | (90, 98, 104) | Cast shadow inside locker vent slits, under locker handles. Dark cool gray. |
| Locker handle/detail | Aged Metal | `#A0A8A8` | (160, 168, 168) | Flat metal — slightly teal shifted, worn. Not shiny chrome. |
| Linoleum floor (main tile) | Institutional Linoleum | `#B8B49A` | (184, 180, 154) | Warm-tan linoleum with a slightly greenish-gray overlay from the fluorescents. The base is a warm sandy tone (#C4A882 family) that has been washed cool by years of institutional cleaning fluid. |
| Linoleum floor (grout lines) | Floor Grout | `#8A887A` | (138, 136, 122) | Darker warm-gray. The seam lines between linoleum tiles. |
| Linoleum floor (deep shadow) | Floor Shadow | `#6A6A60` | (106, 106, 96) | Cast shadow under lockers, benches. Near-neutral but retains a faint warm undertone so the floor doesn't go fully dead-gray. |
| Ceiling light fixtures | Tube White | `#E8EEE8` | (232, 238, 232) | Fluorescent tube color — very slightly green. Not pure white. |

### Locker Alternation Pattern
Lockers alternate A/B/A/B along the wall. A = Institutional Sage `#8A9E94`. B = Institutional Blue-Gray `#8A96A4`. The two colors should be close enough in value that the pattern reads as "subtle variation" rather than "decorative stripe." This is intentional — this hallway should not feel designed.

### Color Safety — Luma in the Hallway
When Luma walks through this hallway, check:
1. Orange hoodie (#E8703A) against Institutional Sage (#8A9E94): these are near-complements — orange reads against green-gray. Figure-ground is safe.
2. Dark hair (#3B2820) against Cool Plaster wall (#C4CECC): strong value contrast. Safe.
3. Skin (#8C5430 if Miri reference; Luma's warm tan #C4A882) against Institutional walls: warm skin against cool-gray wall — safe by temperature contrast.
4. Do NOT use any GL colors in this environment. The school is a fully Glitch-free zone until the story beats require otherwise.

### Forbidden in School Hallway
- No warm key light or lamp warmth
- No Glitch Layer palette colors (GL-01 through GL-07)
- No Soft Gold (#E8C95A) or Sunlit Amber (#D4923A) as ambient fill — those are warm domestic/outdoor tones and would destroy the institutional mood
- No pure neutral grays (R=G=B) — all grays must have a warm or cool lean per the above specs

---

## Cross-Reference: Master Palette Entries Used

All colors in this brief either map directly to existing master_palette.md entries (RW-01 through RW-13) or are scene-specific derivations. The monitor glow values (C8D4E0, B8C8D4, 3A4A5A) and the school hallway institutional tones (DDE8DF, C4CECC, B0BABC, 8A9E94, 8A96A4, 5A6268, A0A8A8, B8B49A, 8A887A, 6A6A60, E8EEE8) are scene-specific construction values — they do not require master palette entries because they are environment-only and will not recur in other contexts. If Jordan Reed's implementation identifies any that recur in a third environment, register them as ENV-xx entries at that point.

The monitor glow values should be noted in grandma_miri_color_model.md as Miri-scene-specific, which has been done in the Cycle 17 update to that document.

---

*Sam Kowalski, Color & Style Artist — Cycle 17*
*Unblocks Jordan Reed's Act 2 environment build. Review before starting background renders.*
