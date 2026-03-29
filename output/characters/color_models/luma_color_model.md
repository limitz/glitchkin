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
*Cycle 18 addition: Cold/Cyan Overlay Variants section (Sam Kowalski) — Recalculated C18, correct alpha-composite formula applied. Resolves pitch_package_index.md open item #6 (Naomi Bridges C10 flag).*

---

## Cold/Cyan Overlay Variants — Glitch Layer Lighting on Luma

**Recalculated C18 — correct alpha-composite formula applied.**

This section documents the correct alpha-composite results when Electric Cyan (`#00F0FF`, GL-01, R:0, G:240, B:255) is overlaid on Luma's key base surface colors at production-standard opacity levels.

**Formula (per channel, α as 0.0–1.0):**
```
C_result = C_base × (1 − α) + C_overlay × α
```

**Cyan-dominant rule:** Any surface identified as "Glitch Layer lit" must satisfy **G > R AND B > R** (individually, not just G+B > R). This rule verifies the surface reads as cool/digital rather than warm.

**Note on SF01 alpha levels:** In Style Frame 01 (`style_frame_01_rendered.py`), the cold overlay uses `cold_alpha_max=60` (60/255 ≈ 23.5% at monitor center) and produces approximately 30/255 ≈ 11.8% at the 80px boundary zone (x=880). At these SF01 levels, Luma's skin does NOT pass the cyan-dominant rule — this is intentional. The SF01 cold wash is a cross-light split-light effect, not a Glitch Layer immersion. The cyan-dominant threshold is reserved for full Glitch Layer scenes (SF03 and equivalents) where α ≥ 31% on skin.

---

### Cold Overlay on Skin (Lamp-Lit Base — CHAR-L-01: `#C8885A`, R:200, G:136, B:90)

| α | % | C_result RGB | Hex | G > R | B > R | Cyan-dominant |
|---|---|---|---|---|---|---|
| 0.10 | 10% | (180, 146, 106) | `#B4926A` | ✗ | ✗ | ✗ |
| 0.15 | 15% | (170, 152, 115) | `#AA9873` | ✗ | ✗ | ✗ |
| 0.20 | 20% | (160, 157, 123) | `#A09D7B` | ✗ | ✗ | ✗ |
| 0.25 | 25% | (150, 162, 131) | `#96A283` | ✓ | ✗ | ✗ |
| 0.30 | 30% | (140, 167, 140) | `#8CA78C` | ✓ | ✗ | ✗ |
| **0.31** | **31%** | **(138, 168, 141)** | **`#8AA88D`** | **✓** | **✓** | **✓ — threshold** |
| 0.35 | 35% | (130, 172, 148) | `#82AC94` | ✓ | ✓ | ✓ |

**Cyan-dominance threshold for lamp-lit skin: α ≥ 0.31 (31%)**

- SF01 boundary zone (α ≈ 11.8%): result ≈ (177, 148, 109) `#B1946D` — warm cross-light, NOT cyan-dominant. Correct for split-light effect.
- SF01 center zone (α ≈ 23.5%): result ≈ (153, 161, 129) `#99A181` — partial desaturation, NOT cyan-dominant. Still warm-dominant. Correct.
- Glitch Layer full exposure (α ≥ 31%): use `#8AA88D` or deeper. Cross-reference DRW-11 (`#A87890`) for UV-ambient skin, DRW-01 (`#7ABCBA`) for direct cyan key on skin.

---

### Cold Overlay on Skin (Neutral Base — RW-10: `#C4A882`, R:196, G:168, B:130)

| α | % | C_result RGB | Hex | G > R | B > R | Cyan-dominant |
|---|---|---|---|---|---|---|
| 0.10 | 10% | (176, 175, 142) | `#B0AF8E` | ✗ | ✗ | ✗ |
| 0.15 | 15% | (167, 179, 149) | `#A7B395` | ✓ | ✗ | ✗ |
| 0.20 | 20% | (157, 182, 155) | `#9DB69B` | ✓ | ✗ | ✗ |
| **0.21** | **21%** | **(155, 183, 156)** | **`#9BB79C`** | **✓** | **✓** | **✓ — threshold** |
| 0.25 | 25% | (147, 186, 161) | `#93BAA1` | ✓ | ✓ | ✓ |
| 0.30 | 30% | (137, 190, 168) | `#89BEA8` | ✓ | ✓ | ✓ |
| 0.35 | 35% | (127, 193, 174) | `#7FC1AE` | ✓ | ✓ | ✓ |

**Cyan-dominance threshold for neutral skin: α ≥ 0.21 (21%)**

Note: Neutral skin (#C4A882) has a higher G and B channel than lamp-lit skin (#C8885A), so it reaches cyan-dominance at a lower alpha. Use this table for standard/outdoor Real World scenes where Luma's skin is at the neutral base.

---

### Cold Overlay on Hoodie Orange (Base — `#E8722A`, R:232, G:114, B:42)

| α | % | C_result RGB | Hex | G > R | B > R | Cyan-dominant |
|---|---|---|---|---|---|---|
| 0.10 | 10% | (209, 127, 63) | `#D17F3F` | ✗ | ✗ | ✗ |
| 0.20 | 20% | (186, 139, 85) | `#BA8B55` | ✗ | ✗ | ✗ |
| 0.30 | 30% | (162, 152, 106) | `#A2986A` | ✗ | ✗ | ✗ |
| 0.35 | 35% | (151, 158, 117) | `#979E75` | ✓ | ✗ | ✗ |
| **0.43** | **43%** | **(132, 168, 134)** | **`#84A886`** | **✓** | **✓** | **✓ — threshold** |
| 0.50 | 50% | (116, 175, 149) | `#74AF95` | ✓ | ✓ | ✓ |

**Cyan-dominance threshold for hoodie orange: α ≥ 0.43 (43%)**

The orange hoodie resists cyan-dominance until very high overlay alpha — this is physically correct. Highly saturated orange (R:232) is the hardest surface to make cyan-dominant. At the DRW-15 level (Hoodie Hem Under Cyan Bounce, `#5AA8A0`), a strong localized bounce source is used rather than a global overlay.

---

### Cold Overlay on Hoodie Shadow (Base — `#B85520`, R:184, G:85, B:32)

| α | % | C_result RGB | Hex | G > R | B > R | Cyan-dominant |
|---|---|---|---|---|---|---|
| 0.10 | 10% | (166, 100, 54) | `#A66436` | ✗ | ✗ | ✗ |
| 0.20 | 20% | (147, 116, 77) | `#93744D` | ✗ | ✗ | ✗ |
| 0.30 | 30% | (129, 132, 99) | `#818463` | ✓ | ✗ | ✗ |
| **0.38** | **38%** | **(114, 144, 117)** | **`#729075`** | **✓** | **✓** | **✓ — threshold** |
| 0.40 | 40% | (110, 147, 121) | `#6E9379` | ✓ | ✓ | ✓ |

**Cyan-dominance threshold for hoodie shadow: α ≥ 0.38 (38%)**

---

### Summary — Cyan-Dominance Thresholds

| Surface | Base Hex | Min α for G>R AND B>R | Notes |
|---|---|---|---|
| Skin (lamp-lit) | `#C8885A` | **31%** | SF01 never reaches this — intentional cross-light only |
| Skin (neutral) | `#C4A882` | **21%** | Glitch Layer neutral-skin exposure |
| Hoodie orange | `#E8722A` | **43%** | Use DRW-15 for localized bounce |
| Hoodie shadow | `#B85520` | **38%** | — |

**Rule:** Do NOT apply a "Glitch Layer lit" label to any surface color derived from an α below its cyan-dominance threshold. SF01 cold overlay values are cross-light effects, not Glitch Layer immersion values. See master_palette.md Section 1B (C10-1 RESOLVED) and DRW-01/DRW-11/DRW-13 for full Glitch Layer skin derivations.

---
