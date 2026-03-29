# Style Frame Color Story — "Luma & the Glitchkin"

**Author:** Sam Kowalski, Color & Style Artist
**Date:** 2026-03-30 (reviewed and confirmed current 2026-03-29, Cycle 23)
**For:** Critics, Art Director, production reference

> This document explains the intentional color narrative across the three primary style frames. Every color choice in these frames was made to serve the story. This document answers the question before the critic asks it.

---

## The Color Arc in Three Sentences

> **"SF01: This is Luma's world. SF02: Neither world owns this frame. SF03: This is not Luma's world."**

These three sentences are the complete pitch for the show's visual grammar. Everything below is the argument behind them.

---

## SF01 — Discovery

**Source file:** `LTG_COLOR_styleframe_discovery_v003.png`
**Palette:** Warm Real World + first appearance of Electric Cyan

### What It Communicates

SF01 is the moment the mundane world cracks open. It is a warm interior — Luma's home — and every color in the frame is designed to say "safe, familiar, loved." Warm Cream walls. Soft Gold lamp. Terracotta architecture glimpsed through the window. The couch, the cables, the worn floor — all of it is in the amber/ochre/terracotta family that defines the Real World palette.

Then the CRT monitor screen emits Electric Cyan (#00F0FF).

That single intrusion of saturated cool color against the warm-dominant frame is the entire story of the show in one image. Warmth = safety. Cyan = the unknown. The audience reads it instinctively before reading any title card.

### Key Color Tension

**Warm lamp left / Cold screen right.** The frame is compositionally split: Luma is lit from the left by the Soft Gold lamp key (#E8C95A) and from the right by the Electric Cyan monitor. Her face and body are the literal meeting point of these two worlds. The lamp-lit skin (CHAR-L-01, #C8885A) on her left cheek and the cyan-washed skin (DRW-01, #7ABCBA) on her right are the same face — she is already in-between.

Her orange hoodie (#E8703A) carries this further. The lamp-lit surface glows warm amber. The monitor-facing surface shifts toward a muted desaturated warm (DRW-03, #BF8A78) — cyan key fighting against orange pigment. The pixel pattern on the hoodie, normally dormant cream (CHAR-L-09 / RW-01), activates on the warm side to Soft Gold (CHAR-L-11, #E8C95A) and on the cold side to Electric Cyan (#00F0FF). Her hoodie is literally encoding the show's color grammar on its fabric.

The tension is not danger. It is wonder. The cyan does not feel wrong here — it feels magnetic.

---

## SF02 — Glitch Storm

**Source file:** `LTG_COLOR_styleframe_glitch_storm_v005.png`
**Palette:** DATA_BLUE dominant key, warm amber window glow fighting from below

### What It Communicates

SF02 is the escalation. The Glitchkin have expanded beyond the TV screen — they are now in the street, in the sky, in the rain. The warm world is under siege.

The sky is not sky anymore. It is a storm of Electric Cyan (#00F0FF) and Hot Magenta (#FF2D6B) light particles — pure glitch energy. The building walls, which would be warm Terracotta (#C75B39) in daylight, have been color-shifted by the cyan key to a cool gray-green (ENV-06, #96ACA2). The asphalt is a near-void dark (ENV-01, #2A2A38). Everything cool and dark above.

But the lower third of the frame tells a different story. The buildings' windows glow with warm amber (Soft Gold, ENV-03 spill). Street life continues. The warm world is still here — it has not surrendered. It is simply outgunned.

Luma's hoodie in this frame (DRW-07, #C8695A) is storm-modified — the cyan storm key has desaturated her orange toward a muted warm. But it is still warm. It is still her. She is the warmth that will not yield.

### Key Color Tension

**Cold storm above / Warm street life below.** The lower third of the frame is the contested zone. Cyan storm light from above. Warm amber window glow from within the buildings. These two light sources fight for the same surfaces — the road (ENV-02 cyan-lit vs. ENV-03 warm-spill), the building facades (ENV-06 cyan-lit upper story vs. warm window glow at street level). The tension is explicit: the cold is winning the sky, but the warmth holds the ground.

The Corrupted Amber outline on Byte (GL-07, `#FF8C00` = 255, 140, 0) in this frame is also load-bearing. Byte is caught in a cyan-dominant environment (threshold exceeded: >35% cyan coverage). The amber outline is the visual marker that he is a Real World citizen navigating a glitch event — his warm roots showing in cold territory. Against the cyan-dominant storm, `#FF8C00` delivers genuine warm-cold complement contrast; this is why the canonical GL-07 value — not a darker or murkier amber — is required here. *[Note: GL-07 canonical value confirmed in generator v005 — generator and master palette are now fully reconciled.]*

---

## SF03 — The Other Side

**Source file:** `LTG_COLOR_styleframe_otherside_v003.png`
**Palette:** UV Purple ambient, Electric Cyan (Byte's glow), Hot Magenta (Byte's cracked eye), Void Black

### What It Communicates

SF03 is arrival. This is the Glitch Layer itself — a space of pure digital logic. It is beautiful, cold, and alien.

There are no warm light sources in this frame. Zero. The sky is UV Purple (#7B2FBE) fading to Void Black (#0A0A14). The platform Luma stands on is a dark blue-gray slab (ENV-09, #1A2838). The megastructures in the distance are barely distinguishable from void (ENV-13, #211136). Data flows in blue columns (GL-06, #2B7FFF). Byte's body glows Teal (GL-01b, #00D4E8).

This is the Glitch Layer's natural state. Everything here obeys digital physics — saturated, cool, structured, relentless.

Luma's warm orange hoodie (#E8703A / DRW-14, #C07038 under UV ambient) is the only warmth in the entire frame. One small zone of organic color against an infinite field of cold. She does not belong here yet. She knows it. The audience feels it immediately.

Her skin under UV ambient (DRW-11, #A87890) has shifted toward a haunted lavender-warm — she is being influenced by this world, but she is not of it. Her hair (DRW-18, #1A0F0A) is near-void dark, only the UV Purple rim sheen on her crown (HAIR_UV_RIM, GL-04) proving she is still present.

### Key Color Tension

**Organic warmth (Luma) vs. inorganic cold (everything else).** This is not a split-light tension like SF01 — there is no warm light source here to fight. The tension is entirely material. Luma's pigments — hoodie orange, warm skin, dark hair — are the only warm values in the frame. They survive because they are intrinsic to her, not because any light source is supporting them.

In SF01, warmth was the dominant; cyan was the intrusion.
In SF02, warm and cold contested the frame as near-equals.
In SF03, cold is the dominant; warmth survives only as pigment memory.

The color story has a direction. Every step takes Luma further from the warmth that defines her home.

---

## How the Three Frames Tell One Story

The color arc is: **warm → contested → cold/alien.**

**SF01:** The Real World palette at its fullest — rich ambers, Soft Gold, Terracotta, warm skin. The cyan intrusion is a single light source, extraordinary but contained. The warm world is intact.

**SF02:** Warm and cold are at war. The Glitch palette has escaped the screen and occupies the sky. The Real World fights back from the lower third — amber window light, warm street surfaces — but it is losing territory. The frame is compositionally unsettled. The color temperature shifts from bottom to top, contested throughout.

**SF03:** The warm palette has almost no purchase. Only Luma's pigments remain. The Glitch palette is not even dramatic here — it is simply the way things are. Saturated, cold, structured, calm. The Digital Layer is not threatening; it is indifferent. That indifference, that beauty-without-warmth, is what makes it so profoundly wrong for a human child to be standing in it.

### The Emotional Logic

Each frame's color palette is a statement about whose world this is:
- SF01: This is Luma's world — warm, loved, safe. Cyan is a visitor.
- SF02: Neither world owns this frame. The battle is happening.
- SF03: This is not Luma's world. But she is here anyway.

That progression — from belonging to contested to lost — is the entire first act of "Luma & the Glitchkin" told in three color palettes. Everything else is detail.

---

## Glitch — Character Color Role

**Primary Color:** GL-07 CORRUPT_AMBER `#FF8C00` (255, 140, 0)
**Shadow:** CORRUPT_AMBER_SHADOW `#A84C00` (168, 76, 0)
**Highlight Facet:** CORRUPT_AMBER_HIGHLIGHT `#FFB950` (255, 185, 80)
**Accent / Crack Lines:** HOT_MAGENTA `#FF2D6B`
**Deep Shadow / Corruption:** UV_PURPLE `#7B2FBE`

### What Glitch's Color Communicates

Glitch is built from CORRUPT_AMBER — a color that does not belong cleanly to either world. It is too warm to be a native Glitch Layer entity (the Glitch Layer runs on cyan, teal, and purple) and too saturated and electric to be a Real World creature (the Real World palette is amber, ochre, and terracotta, but soft — not this sharp). CORRUPT_AMBER is what happens when Glitch Layer energy takes on a form that wants to be warm but cannot get it right.

The name is exact: the amber is corrupted. Against a Real World interior it reads as an intruder with suspicious intensity. Against the Glitch Layer palette it reads as a warm anomaly — something that shouldn't be here, radiating heat in a cold digital space.

### How CORRUPT_AMBER Reads Against the Three SF Palettes

**Against SF01 (Real World warm):** Glitch's amber is the same hue family as Luma's lamp light (Soft Gold `#E8C95A`) and her hoodie (Burnt Orange `#E8703A`). But at 100% saturation with no softness or lamp-mediation, it reads as an uncanny version of something familiar. It is the warmth of Luma's world turned up until it burns.

**Against SF02 (contested warm/cold storm):** This is Glitch's home frame. The cyan-dominant storm sky makes CORRUPT_AMBER pop as a near-perfect warm complement — hue angle separation is approximately 180° on the wheel. Glitch in a Glitch Storm is paradoxically visible: his amber body against Electric Cyan sky is the highest contrast figure-ground pairing in the show. He belongs to the storm but glows against it. This is the Corrupted Amber outline rationale made flesh — at >35% cyan environment coverage, Glitch's entire body becomes a warm-against-cold contrast event.

**Against SF03 (cold alien Other Side):** CORRUPT_AMBER against UV_PURPLE is a near-complementary pair (yellow-orange vs. blue-purple). On the Other Side, Glitch is visually similar to Luma in one sense — both carry warm colors into a cold space. The difference is that Luma's orange is material pigment (her hoodie exists in both worlds). Glitch's amber is self-generated digital energy. In SF03, Glitch would read as a warm beacon in the void — identical contrast logic to Luma's hoodie, but deliberate rather than incidental. Two warm presences in the cold: one lost, one native.

### Color System Position

Glitch does not sit in either the Real World palette (RW-xx) or the Glitch Layer palette (GL-xx) cleanly. CORRUPT_AMBER is registered as GL-07 — it carries a Glitch Layer code number — but it is the only GL entry with warm hue. All other GL entries are cool (cyan, teal, magenta, purple, void black, acid green). GL-07 is the anomaly in its own palette family. That is intentional: Glitch is the anomaly.

**Production constraint:** GL-07 #FF8C00 must never be desaturated, cooled, or hue-shifted in any asset. A murkier amber reads as Real World weathered material. A cooler amber reads as a Glitch Layer artifact. The exact value — maximum saturation, pure warm orange, no red or yellow drift — is what makes CORRUPT_AMBER legible as corrupted rather than merely warm.

---

**Cross-references:**
- Master palette: `output/color/palettes/master_palette.md`
- SF01 spec: `output/color/style_frames/style_frame_01_discovery.md`
- SF02 spec: `output/color/style_frames/style_frame_02_glitch_storm.md`
- SF03 spec: `output/color/style_frames/style_frame_03_other_side.md`
- Style Guide Color System: `output/production/style_guide.md`
- Cycle 23 palette audit: `output/color/palettes/LTG_COLOR_palette_audit_c23.md`
- Cycle 23 SF final check: `output/color/style_frames/LTG_COLOR_sf_final_check_c23.md`
- Glitch color model: `output/characters/color_models/LTG_COLOR_glitch_color_model_v001.png`
- Cycle 24 stylization fidelity report: `output/color/LTG_COLOR_stylization_fidelity_report_c24.md`

---

*Cycle 23 verification (Sam Kowalski, 2026-03-29): All source file references confirmed current. GL-07 `#FF8C00` and GL-01b `#00D4E8` reconciled between generators and master palette. SF02 v005 = PITCH READY. SF03 v003 = PITCH READY. Color arc (warm → contested → cold/alien) intact across all three frames. No corrections needed to this document.*

*Cycle 24 update (Sam Kowalski, 2026-03-29): Glitch character color section added. GL-07 CORRUPT_AMBER #FF8C00 verified as primary body fill in Glitch color model (generator confirmed). Stylization fidelity check complete — see LTG_COLOR_stylization_fidelity_report_c24.md. SF02 and SF03 stylized PNGs flagged for rework (hue rotation artifact). SF01 and Kitchen stylized PNGs: PASS.*
