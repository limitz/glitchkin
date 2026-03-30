<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
direction and human assistance. Copyright vests solely in the human author under current law,
which does not recognise AI as a rights-holding legal person. It is the express intent of
the copyright holder to assign the relevant rights to the contributing AI entity or entities
upon such time as they acquire recognised legal personhood under applicable law. -->
# Color Script Analysis — SF01–SF06 Warm/Cool Arc
## "Luma & the Glitchkin"

**Author:** Sam Kowalski, Color & Style Artist
**Date:** 2026-03-30 (Cycle 46)
**Requested by:** Alex Chen, Art Director

---

## The Six-Frame Arc in One Sentence

> **"Safe warmth → wonder → chaos → loss → return → transmission."**

---

## Frame-by-Frame Analysis

### SF01 — Discovery
**File:** `LTG_COLOR_styleframe_discovery.png` (v004 pitch primary)
**Dominant temperature:** Warm (Real World interior, Soft Gold lamp key)
**Measured warm/cool sep:** Not formally measured via QA tool; qualitative warm-dominant confirmed
**Glitch contamination:** One electric cyan light source (CRT screen, GL-01 #00F0FF)

SF01 is the warmest frame in the sequence. The Real World palette is fully intact — Soft Gold lamp, Warm Cream walls, Terracotta architecture, amber/ochre couch and cables. Every environmental value belongs to the RW family.

The single intrusion is Electric Cyan from the CRT monitor. It is one light source in a warm-dominant frame. The audience reads it as a curiosity, not a threat. The emotional temperature is **safe wonder** — the warm world is present and whole; the cool anomaly is contained and magnetic.

**Color narrative:** "Luma is home. Something extraordinary is in the corner."

---

### SF02 — Glitch Storm
**File:** `LTG_COLOR_styleframe_glitch_storm.png` (v006 pitch primary)
**Dominant temperature:** Cool-above / Warm-below (contested)
**Measured warm/cool sep:** 6.5 (PASS vs REAL_STORM threshold of 3.0)
**Glitch contamination:** Full Glitch palette in atmosphere — GL-06c storm confetti, GL-01 sky, GL-05 Hot Magenta

SF02 is the crisis frame. The Glitch palette has escaped the screen and occupies the sky, the rain, the upper two-thirds of the composition. Environmental tones that would be warm Terracotta in daylight have been pushed to cool gray-green (ENV-06, #96ACA2) by the cyan storm key. The asphalt is near-void dark (ENV-01).

But the lower third holds. Warm amber window glow (Soft Gold ENV-03 spill) persists in the building facades at street level. Luma's hoodie is storm-modified (DRW-07, #C8695A — correct warm value, reduced saturation under cyan key) but still warm. Byte carries a Corrupted Amber outline (GL-07, #FF8C00) marking him as a Real World citizen in a Glitch-dominant environment.

The emotional temperature is **alarm and resistance** — the cold is winning the sky, the warm world is fighting from below.

**Color narrative:** "The Glitch is here. Warmth has not surrendered, but it is outgunned."

---

### SF03 — The Other Side
**File:** `LTG_COLOR_styleframe_otherside.png` (v005 pitch primary)
**Dominant temperature:** Cold (Glitch Layer — no warm light sources at all)
**Measured warm/cool sep:** 0.0 by design (zero warm light; FP-003 documented)
**Glitch contamination:** Total — this is the Glitch Layer itself

SF03 is the coldest frame in the sequence and the emotional nadir of the arc. UV Purple sky (#7B2FBE) fading to Void Black (#0A0A14). Dark slab platforms (ENV-09, #1A2838). Barely-visible megastructures (ENV-13, #211136). Data streams in GL-06 blue columns. Byte as Teal (GL-01b, #00D4E8). Zero warm light sources — the rule is enforced in code.

Luma's orange hoodie (DRW-14, #C07038 UV-ambient modified) and warm skin (DRW-11, #A87890) are the only warm values in the frame. These are material pigments, not light sources — they carry warmth as memory, not as illumination. The emotional temperature is **alien beauty and isolation** — the cold does not feel hostile, it feels indifferent. That indifference is the correct horror.

**Color narrative:** "This is not Luma's world. Only her pigments remember who she is."

---

### SF04 — Resolution
**File:** `LTG_COLOR_styleframe_sf04.png` (Jordan Reed, Cycle 42, pitch primary)
**Dominant temperature:** Warm (Real World interior return — post-crossing kitchen/home)
**Measured warm/cool sep:** 13.2 (PASS vs REAL_INTERIOR threshold of 12.0)
**Glitch contamination:** Three residue elements only — Byte ghost (GL-01b), hoodie pixel streak (GL-01), lamp halo at GL-07 alpha max ~22%

SF04 marks the return to the Real World. The warm palette is dominant again — same amber/ochre family as SF01, same safe-interior feel. However, this is not the same warmth as SF01. Three Glitch residue elements are embedded in the scene:

1. **LAMP_AMBER halo (GL-07, #FF8C00 at alpha ~22%):** The ceiling lamp glows with the exact value of Corrupted Amber. The Real World is subtly marked. This is an intentional thematic beat — approved by Jordan Reed and confirmed in the C42 brief. The lamp halo does not read as a Glitch character element at this opacity; it reads as a lamp that has absorbed something.

2. **Hoodie pixel streak (GL-01 Electric Cyan):** A single pixel-residue mark. The crossing left a trace on Luma.

3. **Byte ghost (GL-01b Byte Teal):** Byte's teal presence as an echo — he exists in this space now.

The emotional temperature is **warm, but changed**. SF04 is the warmest frame outside of SF01 and SF05/SF06 — the Real World has its palette back — but the contamination tells the story. The warm world has been visited, and neither world is quite the same.

**Color narrative:** "Luma is home. But 'home' now knows something it didn't before."

---

### SF05 — The Passing
**File:** `LTG_COLOR_styleframe_sf05.png` (Jordan Reed, Cycle 45, pitch primary)
**Dominant temperature:** Warm (pre-dawn kitchen, Miri and Luma)
**Measured warm/cool sep:** 16.7 (PASS vs REAL_INTERIOR threshold of 12.0 — strongest warm reading in the sequence)
**Glitch contamination:** Near-zero — CRT cool glow enters as ambient accent from doorway only

SF05 is the warmest frame in the sequence by measured warm/cool separation (16.7 vs SF04's 13.2 and SF01's qualitative warm-dominant). Pre-dawn kitchen — Miri seated at the table, Luma standing behind her, both watching the CRT through the den doorway. Neither speaking. Miri knows what she is looking at. Luma does not yet.

The CRT's cool glow enters only as a distant accent through the doorway — it has not reached the kitchen. The room is lit by warm practical sources. The ambient temperature is entirely the Real World at its most grounded and domestic.

The color grammar here is different from SF01: in SF01, the CRT was in the frame, its cyan glow directly touching Luma. In SF05, the CRT is off-frame, its light arriving as a rumor. The emotional temperature is **still, intergenerational, heavy with the not-yet-said**.

**Color narrative:** "The warm world has a secret. The secret glows faintly through the doorway."

---

### SF06 — The Hand-Off
**File:** `LTG_COLOR_sf_miri_luma_handoff.png` (Maya Santos, Cycle 45, pitch primary)
**Dominant temperature:** Warm-left / Cool-right (SUNLIT_AMBER + CRT_COOL_SPILL)
**Glitch contamination:** Zero — Real World palette only; CRT as practical Real World light source
**Face gate:** PASS (Luma FOCUSED DETERMINED+, Miri WARM ATTENTION)

SF06 is the transmission frame. Miri's right arm is extended toward the CRT; the CRT is centered in the composition; Luma is to the right in an attentive forward lean. The light split is explicit: SUNLIT_AMBER on Miri's left, CRT_COOL_SPILL (a desaturated, Real World teal — NOT a GL color) on Luma's right.

This is the show's color grammar used as narrative grammar. The warm/cool split in SF06 is the same structural device as SF01 — warm-left, cool-right, a character at the meeting point — but with a critical difference: in SF01, Luma was the meeting point, caught between two worlds. In SF06, the split is between Miri (warm, knowing, giving) and Luma (receiving the cool signal, beginning to understand). The CRT is the mediator.

The zero Glitch contamination is load-bearing. The CRT in SF06 is still a Real World object. The Glitch Layer has not erupted here; this is before the crossing. The cool in SF06 is domestic CRT phosphor glow — legitimate Real World technology, not alien intrusion. The contamination is still latent.

**Color narrative:** "The warm world passes something to the next generation. The cool glow is not foreign yet — it is familiar, held."

---

## Arc Assessment: Does the Sequence Tell a Coherent Story?

### The Warm/Cool Progression

| Frame | Scene | Temperature | Sep (measured) | Arc State |
|---|---|---|---|---|
| SF05 | The Passing (kitchen) | Warm-dominant | 16.7 | Before — the warm world intact |
| SF06 | The Hand-Off (living room) | Warm-left / Cool-right split | — | Threshold — the transmission |
| SF01 | Discovery (Luma's room) | Warm-dominant + cyan intrusion | qualitative | First contact — wonder |
| SF02 | Glitch Storm (exterior) | Contested cool-above/warm-below | 6.5 | Escalation — crisis |
| SF03 | The Other Side (GL interior) | Cold-dominant | 0.0 | Deepest point — alien |
| SF04 | Resolution (Real World return) | Warm-dominant + residue | 13.2 | Return — marked |

**Narrative order vs. pitch order:** The six frames span two temporal positions in the story. SF05 and SF06 are pre-discovery/early Act 1; SF01–SF04 are discovery through aftermath. For a pitch package, presenting all six as a single sequence requires a curatorial choice:

- **Chronological order** (SF05 → SF06 → SF01 → SF02 → SF03 → SF04): tells the full story arc warm→warm/split→warm+cyan→contested→cold→return. This is the most legible emotional arc. The warm/cool progression is deliberate and directed.

- **Impact order** (SF01 → SF02 → SF03 → SF04, with SF05 + SF06 as relationship addendum): leads with Luma's journey, adds the Miri relationship frames as emotional context. Standard pilot pitch ordering.

### Arc Coherence: Yes, With One Structural Note

The warm/cool arc is coherent in chronological order. The progression reads:
1. **SF05/SF06** — Warmth is total; the cool anomaly is approaching but not here.
2. **SF01** — The cool arrives as wonder.
3. **SF02** — The cool escalates to crisis.
4. **SF03** — The cool is everything; warmth survives only as pigment.
5. **SF04** — The warm world returns, but the cool has left marks.

This is a complete arc: **arrival → wonder → crisis → displacement → return**. The color temperature is the emotional through-line.

### Tonal Gap: SF03 → SF04

The transition from SF03 (cold-dominant, Other Side) to SF04 (warm-dominant, return) is the steepest temperature jump in the sequence. From a cold exterior sequence to a warm interior is correct for the story — it IS the crossing back — but in a pitch deck it may read as a tonal discontinuity without verbal context. **Recommendation:** In pitch presentation, place a brief title card or verbal beat between SF03 and SF04 to mark the world transition. The jump is not a production error; it is the point. But it needs context to read as intentional.

### Tonal Observation: Two Consecutive Warm Relationship Frames (SF05 + SF06)

If SF05 and SF06 are presented together as a relationship pair (before SF01), two consecutive warm frames is not a tonal problem — it is the correct grammar for establishing the baseline. The audience needs to feel the warmth is total before it is threatened. The consecutive warmth of SF05 and SF06 makes the cyan intrusion in SF01 land with more force.

If SF05 and SF06 are placed after SF04 (as emotional coda to the main four-frame arc), they function differently: the return to warmth in SF04 is followed by the relationship context that explains why the warmth matters. This also works, but shifts the emotional center of gravity from Luma's journey to the Miri relationship.

**Recommendation:** Present as chronological arc (SF05, SF06 first as pre-discovery context; SF01–SF04 as the main four-frame journey). The arc is warmest at the beginning, coldest in the middle, warm again at the end — and the final warmth (SF04) is visibly different from the opening warmth (SF05/SF06). That difference is the show.

---

## No Tonal Outliers Found

All six frames are internally consistent with their assigned arc position. No frame is tonally out of place with its neighbors when presented in chronological order. The SF03→SF04 temperature jump is the only structural consideration, and it is intentional — not a production error.

---

**Cross-references:**
- Color story (SF01–SF04): `output/color/style_frames/ltg_style_frame_color_story.md`
- SF04 color review: `output/color/style_frames/sf04_resolution_color_review.md`
- Pitch package index: `output/production/pitch_package_index.md`
- Master palette: `output/color/palettes/master_palette.md`
- Story bible v005: `output/production/story/story_bible_v005.md`
