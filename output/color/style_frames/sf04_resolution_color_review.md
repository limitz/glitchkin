# SF04 "Resolution" — Color Review
## "Luma & the Glitchkin"

**Reviewer:** Sam Kowalski, Color & Style Artist
**Date:** 2026-03-30
**Cycle:** 42
**Asset:** `output/style_frames/LTG_COLOR_styleframe_sf04.png`
**Generator:** `output/tools/LTG_TOOL_style_frame_04_resolution.py`

---

## 1. Overall Verdict

**CONDITIONAL PASS** — one flag to resolve (LAMP_AMBER / GL-07 usage documentation),
no production blockers.

---

## 2. Palette Cross-Check (generator constants vs. master_palette.md)

| Constant | Value | Canonical | Status | Notes |
|---|---|---|---|---|
| `HOODIE_ORANGE` | `(232,112,58)` = `#E8703A` | CHAR-L-04 | **PASS** | Canonical hoodie base |
| `HOODIE_SHADOW` | `(184,74,32)` = `#B84A20` | CHAR-L-08 | **PASS** | Canonical hoodie shadow |
| `BLUSH` | `(232,168,124)` = `#E8A87C` | CHAR-L-06 | **PASS** | Canonical blush |
| `SUNLIT_AMBER` | `(212,146,58)` = `#D4923A` | RW-03 | **PASS** | Canonical window amber |
| `CRT_TEAL` | `(0,212,232)` | GL-01b `#00D4E8` | **PASS** | Correct Byte Teal for CRT screen |
| `ELEC_CYAN` | `(0,240,255)` | GL-01 `#00F0FF` | **PASS** | Used sparingly for hoodie pixel residue — correct |
| `LAMP_AMBER` | `(255,140,0)` = `#FF8C00` | GL-07 | **FLAG — SEE BELOW** | GL-07 Corrupt Amber used as indoor lamp halo |
| `DEEP_COCOA` | `(40,24,12)` = `#28180C` | RW (deep shadow) | **PASS** | Warm deep shadow, R>G>B |
| `NEAR_BLACK_WARM` | `(28,18,8)` | Construction | **PASS** | Ultra-dark warm shadow — commented inline |

---

## 3. LAMP_AMBER Flag — GL-07 in Real World Scene

**Flag level:** P2 (document; no visual fix needed)

**Finding:** `LAMP_AMBER = (255,140,0) = #FF8C00` is the canonical Corrupted Amber (GL-07).
Jordan Reed used it as the indoor ceiling-lamp halo color. The halo is soft/radial at
alpha max ~55 (≈22% opacity) — it does not read as a Glitch character element at this opacity.

**Context:** SF04 concept is Luma returning to the Real World "changed." The lamp halo
reading slightly corrupted is thematically resonant — the Real World itself is subtly
marked. Jordan's C42 report confirms this was intentional ("canonical #FF8C00 indoor lamp").

**However:** Using GL-07 in a Real World scene without documentation creates a traceability
gap. Future agents reading the generator will see `(255,140,0)` and may not know whether
it is (a) intentional Glitch residue narrative or (b) a production error.

**Required action:** Add inline comment to the constant in the generator explaining the
intentional use. Example:
```python
LAMP_AMBER = (255, 140, 0)   # GL-07 / #FF8C00 — intentional in SF04 (C42)
                              # The kitchen lamp reads as subtly Glitch-residue marked.
                              # Approved: Jordan Reed C42 brief. NOT a production error.
```

**Additional registration:** Consider whether a new ENV entry (e.g., ENV-14) or
inline use-case note in master_palette.md GL-07 usage guidelines is warranted for
"SF04 post-crossing kitchen — lamp halo at alpha ≤55 = Real World residue, acceptable."
This is a production one-off; do not register unless it recurs.

---

## 4. Figure-Ground Verification

**Luma vs. background:**
- Hoodie orange `#E8703A` against warm wall `#E8C49A` (approx): hue difference ~20°,
  value difference ~30 pts. Marginal but acceptable in a warm-key scene where
  character-to-background separation relies on shape/silhouette, not color contrast alone.
- Luma's HAIR (DRW-18, `#1A0F0A`) provides the dark silhouette anchor. Critical for
  figure-ground at this warm palette density.
- **Recommendation:** Verify dark hair reads at thumbnail scale (120×68px simulation).
  Run `LTG_TOOL_thumbnail_preview_v001.py` if needed.

**Byte ghost vs. CRT screen:**
- Byte ghost `(20,180,200)` = BYTE_GHOST, a desaturated teal. CRT screen = GL-01b `(0,212,232)`.
  Byte ghost is meaningfully dimmer/less saturated — reads as "faded signal" per concept. PASS.

---

## 5. Glitch Residue Elements

Two canonical Glitch residue markers in SF04:
1. **ELEC_CYAN hoodie pixel streak** — single pixel detail, `GL-01 #00F0FF`. Small scale
   but color-correct. Narratively: the crossing leaves a mark.
2. **Byte ghost in CRT doorway** — desaturated teal `(20,180,200)`. Softer than canonical
   GL-01b `(0,212,232)`. This is correct — Byte as "faded signal" should not read at
   full GL-01b saturation.
3. **LAMP_AMBER (GL-07) halo** — see Flag above.

The three-element Glitch residue system in SF04 is internally consistent: strong (Byte
ghost as direct GL-01b echo) → medium (hoodie pixel as GL-01 mark) → subtle (lamp halo
as GL-07 saturation residue). Temperature arc of contamination reads correctly.

---

## 6. Warm/Cool System Verification

From Jordan's QA report: warm/cool separation = **13.2** (target ≥ 12.0 for REAL_INTERIOR).
PASS with ~1.2 points of margin. Linear gradient approach (rather than quadratic) was the
correct fix per Jordan's C42 notes.

warm top strategy: SUNLIT_AMBER from window (top half, alpha 90 linear)
cool bottom strategy: CRT_GLOW from doorway (bottom half, alpha 75 linear)
These are correctly asymmetric (warm > cool in alpha = warm-dominant Real World key).

---

## 7. Canvas Size / Thumbnail Rule

Output at 1280×720 — ≤ 1280px hard limit: **PASS**. No thumbnail() call needed; direct
output at limit size. Per docs/image-rules.md.

---

## 8. Open Items

| Item | Priority | Assigned To | Status |
|---|---|---|---|
| Add inline comment to LAMP_AMBER constant in generator | P2 | Jordan Reed (or self in C43) | OPEN |
| Thumbnail preview check for Luma dark-hair figure-ground | Low | Sam / Jordan | Low priority |
| GL-07 usage note in master_palette.md for SF04 one-off | Low | Sam | Consider C43 |

---

*Cycle 42 — Sam Kowalski, Color & Style Artist*
