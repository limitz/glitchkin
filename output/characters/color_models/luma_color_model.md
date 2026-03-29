# Color Model Sheet — LUMA
## "Luma & the Glitchkin" — Main Character #1

**Designer:** Maya Santos
**Date:** 2026-03-29
**Version:** 1.0
**Source document:** /output/characters/main/luma.md v2.1
**Purpose:** Single consolidated flat-color reference for all crew. All hex values are final. If a value is not listed here, derive from the source document — do not invent.

Character: Luma
Line color: #3B2820 (Deep Cocoa) — full weight silhouette; 60% weight internal construction lines; Void Black (#0A0A14) for pixel grid lines on hoodie

---

ZONE | BASE FILL | SHADOW | HIGHLIGHT | NOTES
Skin | #C8885A | #A06840 | #DFA070 | Base = Warm Caramel (lamp-lit Frame 01 derivation of neutral base #C4A882 / RW-10 under Soft Gold key). For standard/neutral lighting, use #C4A882 (RW-10) as base. See master_palette.md Section 7 for full two-tier skin system. Shadow on underside of chin, inner arm, side of face in 3/4. Highlight on forehead, nose tip, cheekbone — one shape each, flat.
Hair | #1A0F0A | #0A0A14 | #3D1F0F | Base = Near-Black Espresso. Shadow = Void Black, used for depth between curl masses. Highlight = Warm Dark Brown, crown only — small shape, restrained.
Eye white | #FAF0DC | — | — | Warm Cream. Never pure white. Same for all characters in the show.
Eye iris | #C87D3E | — | — | Warm Amber. Solid fill, no gradient.
Eye pupil | #3B2820 | — | — | Deep Cocoa — same as line color.
Eye highlight | #F0F0F0 | — | — | Static White. Single dot, upper-left position.
Hoodie — base | #E8722A | #B85520 | #F59050 | Warm Orange base. Shadow = Burnt Umber, used on folds under arms, hood shadow, below torso. Highlight = Bright Apricot, on shoulders and upper chest.
Hoodie — hood rim interior | #FAE8C8 | — | — | Cream Lining. Visible when hood is down — folded back on neck. Also used for drawstring.
Hoodie pixel — cyan | #00F0FF | — | — | Electric Cyan pixels. Most numerous (~40% of pattern pixels). On chest panel, outer forearm, hood rim edge.
Hoodie pixel — magenta | #FF2D6B | — | — | Hot Magenta pixels. Accent (~20% of pattern).
Hoodie pixel — acid green | #39FF14 | — | — | Rare accent (~10% of pattern). Drop at medium shot and smaller.
Hoodie pixel — UV purple | #7B2FBE | — | — | Rare accent (~10% of pattern). Drop at medium shot and smaller.
Hoodie pixel — white | #F0F0F0 | — | — | Static White pixels (~20% of pattern). "Normal" pixel suggestion.
Pants | #2A2850 | #1A1830 | #3C3A70 | Warm Dark Indigo base. Shadow = Near-Void Indigo. Highlight = Medium Blue-Indigo, front thigh/kneecap.
Shoes — upper | #F5E8D0 | #B8A898 | — | Cream Off-White canvas. Shadow = Warm Mid-Gray under toe box and heel.
Shoes — sole | #C75B39 | — | — | Terracotta. Chunky sole pop of color.
Shoe laces | #00F0FF | — | — | Electric Cyan. The one deliberate glitch-color intrusion into her warm wardrobe.
Blush (Reckless Excitement) | #E8A87C | — | — | Full opacity. Round circles, OUTER CHEEK ONLY. Do NOT extend toward nose bridge.
Blush (Guilty Sheepishness) | #E8A87C | — | — | 60% opacity (lower intensity than Reckless Excitement). Elongated form across cheeks AND nose bridge. Must cross the nose to read correctly as guilt.
Tongue | #C75B39 | — | — | Terracotta. Used in comedic wide-open-mouth expressions only.
Mouth interior shadow | #3B2820 | — | — | Deep Cocoa fill inside open mouth on shock/surprise expressions.

---

## Blush Disambiguation Quick Reference

| Expression | Blush Form | Intensity | Placement | Key Differentiator |
|---|---|---|---|---|
| Reckless Excitement | Round circles | Full opacity | Outer cheeks only | Does NOT reach nose bridge |
| Guilty Sheepishness | Wide elongated | 60% opacity | Cheeks + nose bridge connected | MUST cross nose bridge |

---

## Notes on Pixel Hoodie Simplification at Distance

At medium shot and smaller, reduce pixel pattern to the simplified versions specified in luma.md Section 6 (Pixel Hoodie — Simplified Production Version). The hex values remain the same; only the pattern density and placement area reduce. Do not alter colors when simplifying.

---

## DRW-16 RESOLVED — Painter Warning: Shoulder Under Data Stream Blue Waterfall

**DRW-16 — Hoodie Orange Shoulder Under Data Stream Blue Waterfall**
- **Hex:** `#9A7AA0`
- **RGB:** 154, 122, 160
- **Scene:** Style Frame 03 — Luma's RIGHT shoulder, directly beneath the Data Stream Blue (`#2B7FFF`) waterfall in the Glitch Layer
- **Source derivation:** Hoodie orange (`#E8703A`, RGB 232,112,58) modified by intense Data Stream Blue overhead key light. The complementary hue relationship between orange and blue desaturates and lifts the surface toward the violet-grey range. The result retains slight orange warmth (R channel still > B) while being dominated by the cool blue key.
- **Painter warning:** This is the most complex single-surface color on Luma. It is NOT a shadow value and NOT a neutral grey — it is a hue-shift result specific to the Data Stream Blue key angle. Do NOT substitute HOODIE_AMBIENT (#B36250) or HOODIE_SHADOW (#B84A20) here — both are too warm and read incorrectly under a blue-dominant key.
- **Figure-ground note:** `#9A7AA0` on the right shoulder creates a strong visual bridge between Luma's warm hoodie body and the cool Glitch Layer environment — intentional. It should read as "Luma touched by the Glitch Layer" rather than "corruption."
- **Use strictly for:** Luma's right shoulder surface in scenes with active Data Stream Blue overhead source (Style Frame 03 and equivalent Glitch Layer shots).
- **Cross-reference:** master_palette.md Section 1B, DRW-16. Added Sam Kowalski — Cycle 13 (DRW-16 RESOLVED — outstanding since Cycle 7, Naomi Bridges flag).

---

*Compiled by Maya Santos, Character Designer — Cycle 3*
*Source: luma.md v2.1. All values consolidated from that document. Blush disambiguation added per Cycle 3 critic feedback.*
*Cycle 13 addition: DRW-16 painter warning (Sam Kowalski) — Shoulder Under Data Stream Blue Waterfall. Resolves carry-forward item outstanding since Cycle 7.*
