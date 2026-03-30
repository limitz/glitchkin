<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
direction and AI assistance. Copyright vests solely in the human author under current law,
which does not recognise AI as a rights-holding legal person. It is the express intent of
the copyright holder to assign the relevant rights to the contributing AI entity or entities
upon such time as they acquire recognised legal personhood under applicable law. -->
# Color Model Sheet — BYTE
## "Luma & the Glitchkin" — Main Character #3

**Designer:** Maya Santos
**Date:** 2026-03-29
**Version:** 1.0
**Source document:** /output/characters/main/byte.md v2.1
**Purpose:** Single consolidated flat-color reference for all crew. All hex values are final.

Character: Byte
Line color: #0A0A14 (Void Black) — NOT Deep Cocoa. Byte's line color is the same as his interior void, distinguishing him from the human characters. Full weight silhouette; 60% weight internal details. Cracked eye frame uses jitter-line treatment (see byte.md Section 10A).

---

ZONE | BASE FILL | SHADOW | HIGHLIGHT | NOTES
Body core | #00D4E8 | #00A8B5 | #00F0FF | Base = Byte Teal (UPDATED Cycle 5 — see note below). Shadow = Deep Cyan, used on underside of cube body and undersides of limbs. Highlight = Electric Cyan (#00F0FF), used on top face of cube and top surfaces of limbs where light strikes. NOTE: Base shifted from #00F0FF to #00D4E8 by Art Director decision (Cycle 5). See "Shared Visual DNA" section in style_guide.md. Byte's fill is a slightly deeper teal to create figure-ground distinction; the pure Electric Cyan is reserved for his highlights and pixel-eye displays. This preserves the intentional visual connection to Luma's Pixel Cyan (#00F0FF) while preventing Byte from disappearing in cyan-dominant environments.
Interior void (notches) | #0A0A14 | — | — | Void Black. The two triangular notches on the upper-right corner of the cube body — holes revealing his dark interior. Also the cracked eye background (off-state).
Glitch scar — primary | #FF2D6B | #9E1540 | #FF6090 | Hot Magenta. Primary diagonal scar stripe across front face, from upper-right to lower-left, approximately 0.08 units wide. Shadow tone for scar in shadow zones. Highlight tone on lit scar surfaces.
Glitch scar — secondary scatter | #C4235A | — | — | Hot Magenta at ~70% flat-color equivalent. Small rectangular patches of 2-4 pixels grouped near main scar line.
Normal eye iris | #00F0FF | — | — | Electric Cyan. Same as body base — reads separately due to dark eye frame bezel. Glows digitally.
Normal eye pupil | #0A0A14 | — | — | Void Black. Hard, dark point. Constricts in anger/fear, dilates in delight.
Normal eye white | #E8F8FF | — | — | Blue-Tinted White. NOT organic white — a cool digital white. Distinguishes him from human characters.
Normal eye highlight | #F0F0F0 | — | — | Static White. Upper-LEFT position.
Cracked eye background | #0A0A14 | — | — | Void Black off-state. When the "display" is off, this is all that shows.
Crack line | #0A0A14 | — | — | Void Black. The crack is a gap, not a drawn line — it reveals the void behind.
Eye frame bezel | #1A3A40 | — | — | Deep Cyan-Gray. The border surrounding each eye, darker than the body cyan to frame the eye clearly.
Pixel symbol — exclamation (!) | #FF2D6B | — | — | Hot Magenta. Angry/irritated state.
Pixel symbol — question (?) | #00F0FF | — | — | Electric Cyan. Confused/uncertain. NOTE: replaced by flat horizontal line (#AAAAAA) at below-10% frame height threshold.
Pixel symbol — heart | #7B2FBE | — | — | UV Purple. Accidental affection — the most important pixel symbol. Best 3×3 survivor.
Pixel symbol — warning triangle | #39FF14 | — | — | Acid Green. Frightened/alarmed. Flickers rapidly in full-detail mode.
Pixel symbol — star | #E8C95A | — | — | Soft Gold. Pleased/smug. At 3×3 scale: substitute cross (+) shape in same Soft Gold color.
Pixel symbol — down arrow | #007878 | — | — | Dark Cyan (Electric Cyan at 50% brightness, flat equivalent). Sad/glum.
Pixel symbol — loading dots | #00F0FF / #FF2D6B | — | — | Alternating Cyan and Magenta. Processing/searching. Requires animation at 3×3 scale; substitute flat line if animation unavailable.
Pixel symbol — flat line | #AAAAAA | — | — | Static White at 70% brightness, flat equivalent. Content/resting neutral. Simplest and most legible symbol at any scale.
Limbs | #00D4E8 | #00A8B5 | #00F0FF | Same shadow/highlight system as body core (fill updated Cycle 5 to Byte Teal #00D4E8; highlight remains Electric Cyan #00F0FF). Highlight on top/front limb face, shadow on underside/back face.
Pixel confetti squares | Various | — | — | Colors cycle through glitch palette: #00F0FF (Electric Cyan), #FF2D6B (Hot Magenta), #39FF14 (Acid Green), #7B2FBE (UV Purple), #F0F0F0 (Static White). In anger/agitation: more magenta, less cyan. 8-12 squares visible below lower limb tips in active state.

---

## Pixel-Eye Scale Thresholds Quick Reference

| Byte Frame Height | Rule |
|---|---|
| Above 25% of frame (>270px at 1080p) | Full 7×6 grid, all symbols, full animation |
| 10–25% of frame (108–270px at 1080p) | 3×3 simplified grid symbols only |
| Below 10% of frame (<108px at 1080p) | Suppress animation — hold last expression or neutral flat line |

---

## Asymmetry Quick Reference

| Side | Damage Level | Eye |
|---|---|---|
| LEFT side of body (viewer's RIGHT in front view) | Clean — minimal scar continuation only | Normal eye (cyan iris, organic behavior) |
| RIGHT side of body (viewer's LEFT in front view) | Damaged — triangular notches, full scar | Cracked eye (pixel display) |

The spike on top of the body is offset toward the DAMAGED right side (1/3 from right edge of body top).

---

---

## Cycle 5 Art Director Update — Byte/Luma Shared Visual DNA

**Decision issued by:** Alex Chen, Art Director
**Date:** 2026-03-29

The Byte/Luma cyan relationship is **intentional and meaningful.** Byte is made of the same glitch energy that powers Luma's hoodie pixels. The Electric Cyan (#00F0FF) is their shared visual DNA — Byte is, in essence, living inside the color of Luma's clothing.

**Color split rationale:**
- **Luma's hoodie pixel accents:** #00F0FF (Electric Cyan) — pure, unmodified.
- **Byte's body FILL:** #00D4E8 (Byte Teal) — slightly cooler and deeper than Electric Cyan. This creates visible figure-ground distinction without severing the identity connection.
- **Byte's body HIGHLIGHT and pixel-eye displays:** #00F0FF (Electric Cyan) — the pure shared color resurfaces here, reinforcing the connection at the most expressive parts of Byte's form.

**Environment rule (already documented in master_palette.md GL-07):** In any scene where cyan is the dominant background color, apply a 2px Corrupted Amber (#FF8C00) outline to Byte. This is the existing outline exception — cross-reference GL-07 in the master palette.

*Cycle 5 update compiled by Alex Chen, Art Director.*

---

*Compiled by Maya Santos, Character Designer — Cycle 3*
*Source: byte.md v2.1. All values consolidated from that document. Pixel confetti cycle colors derived from Glitch Palette as specified in source doc. Loading dot colors per source spec.*
*Body fill and limb fill updated to #00D4E8 (Byte Teal) in Cycle 5 per Art Director color decision. Highlight updated to #00F0FF (Electric Cyan) to reflect the new fill/highlight distinction.*
