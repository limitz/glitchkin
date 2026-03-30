# Color Key Spec — COVETOUS Glitch Style Frame
## "Luma & the Glitchkin"

**Author:** Sam Kowalski, Color & Style Artist
**Date:** 2026-03-30
**Cycle:** 41
**Requested by:** Alex Chen (Art Director) — C41 brief
**Narrative source:** glitch.md §7.2 (Interior State Expressions); Jayden Torres critique C16

---

## 1. Scene Narrative

Glitch is alone at the threshold — the invisible boundary between the Glitch Layer
(its home) and the Real World (the world it covets). Luma is not present. Glitch
is watching Real World light from the other side of the barrier. It is the moment
of wanting, not the moment of acting.

**Daisuke's design note:** Interior states must feel quiet and private. COVETOUS is
not triumphant. It is not even mischievous. It is still — and the stillness is what
makes it unnerving. The body should read as appetitive tension, not hostility.

**Jayden Torres connection:** Jayden scored COVETOUS Glitch as "the strongest new
design moment." The color frame must honor that read: Glitch is recognizably hungry,
not simply evil.

---

## 2. Scene Staging

**Setting:** The threshold — the moment Glitch hovers at the barrier between worlds.

- **Camera:** Low angle (eye-level to Glitch, approximately Glitch's center height)
- **Composition:** Glitch positioned left-center (not fully centered — weight toward
  the threshold). The barrier/threshold is right-of-frame, established by the
  Real World warm light bleeding through.
- **Depth layers:**
  - BACKGROUND (far void): Deep Glitch Layer void — UV Purple atmospheric depth,
    Void Black base
  - MID-GROUND: The threshold itself — a faint vertical luminous boundary edge,
    barely visible as a pale ELEC_CYAN line/shimmer
  - FOREGROUND/MID: Glitch hovering, COVETOUS state, leaning slightly toward the
    threshold (+12° tilt, arms slightly raised)
  - THRESHOLD SIDE (right 25%): Warm Real World light spilling through — not full
    illumination, a glow bleed only. Soft Gold warmth pressing against cool void.

---

## 3. Color Key — Dominant to Accent

### 3.1 Background Zones

| Zone | Area | Color | Code | Notes |
|---|---|---|---|---|
| Far void sky | Upper 65% | Void Black | GL-08 `#0A0A14` | Base fill — absolute digital dark |
| UV atmospheric haze | Full left 75% | UV Purple | GL-04 `#7B2FBE` | Ambient overlay at 40% — Glitch Layer identity |
| Atmospheric mid-void band | Mid-distance | Atmospheric Depth Purple | GL-04b `#4A1880` | Depth separation band between sky void and platform zone |
| Platform/ground void | Lower 30% | Void Black + GL-04a | GL-04a `#3A1060` | Deep digital void — Glitch hovers over this |

### 3.2 The Threshold (Key Narrative Element)

| Zone | Area | Color | Code | Notes |
|---|---|---|---|---|
| Threshold barrier edge | Vertical line, right 25% | Electric Cyan | GL-01 `#00F0FF` | The boundary itself — thin luminous edge, 2–3px |
| Real World warm bleed | Right 25%, radial | Soft Gold | RW-02 `#E8C95A` | The thing Glitch covets — warm light visible through/past the barrier. NOT a full key light. Alpha max 90 at nearest edge, falling to 0 within 120px. |
| Real World secondary | Right edge, softer | Sunlit Amber | RW-03 `#D4923A` | Deepens the warm volume in the threshold zone. Radial falloff, alpha max 60. |

**Threshold color rule:** The warm light visible through the threshold MUST remain
entirely in the right 25% of the composition. It must not spill left into the void
zone where Glitch stands. Glitch is in pure cool/void light — it sees the warmth
but is not touched by it. This separation IS the visual premise of the scene.

### 3.3 Key Light Sources

| Source | Color | Direction | Notes |
|---|---|---|---|
| UV Purple ambient | UV Purple GL-04 | Omnidirectional (Glitch Layer ambient) | The only actual light on Glitch. Fills all surfaces dimly. |
| No direct key light | — | — | Glitch has no strong key. The void ambient is its only illumination. |
| Threshold warm bleed | RW-02 / RW-03 | From right | NOT a key light on Glitch. Glitch is NOT lit by warm light in this frame. |

**Critical: Glitch must NOT receive warm light.** The warm glow in the threshold
zone is visible in the background — it does not reach Glitch's body. The entire
power of this image is that Glitch can see what it cannot have.

### 3.4 Glitch Character Colors

| Element | Color | Code | Notes |
|---|---|---|---|
| Body fill | Corrupt Amber | GL-07 `#FF8C00` | Primary body fill — canonical |
| Highlight facet | Corrupt Amber HL | `#FFB950` (approx GL-07 lightened) | Upper-left facet — ambient UV barely illuminates |
| Shadow offset | UV Purple | GL-04 `#7B2FBE` | +3px right, +4px down per spec |
| Outline | Void Black | GL-08 `#0A0A14` | width=3 |
| HOT_MAG crack | Hot Magenta | GL-02 `#FF2D6B` | Diagonal scar — always visible |
| Spike height | Forward-focused | `spike_h=12` | Per glitch.md §3.1 COVETOUS |
| Arm position | Both raised slightly | `arm_l_dy=-8`, `arm_r_dy=-6` | Per glitch.md §4.2 — reaching forward |
| Body tilt | +12° toward threshold | `tilt_deg=+12` | Appetitive lean toward what it wants |
| Eyes | Acid slit — bilateral | GL-03 / `#39FF14` | `[[5,5,5],[0,5,0],[0,0,0]]` — both eyes identical (interior state rule) |
| Confetti | UV Purple only — minimal | GL-04 `#7B2FBE` + GL-07a `#A85800` | Count=4, spread=18px per spec — minimal, private state |

**Amber under UV ambient:** Corrupt Amber (GL-07, #FF8C00) under UV Purple ambient
does not become warm. The UV desaturates and cools amber toward a tawny orange-brown.
The rendered body will read as GL-07 amber — this is correct. Do NOT add warm rim
light to simulate Real World proximity. Glitch is not warmed by the threshold light.

### 3.5 Color Separation Targets

| Separation | Target | Method |
|---|---|---|
| Glitch body vs. background | ΔE ≥ 15 | Corrupt Amber (#FF8C00) vs. UV Purple void: near-complementary. Strong. |
| Threshold warm vs. Glitch | Zero contact | Compositional — warm zone does not overlap character zone |
| Threshold warm vs. void | Soft gradient | RW-02 falls to 0 alpha over 120px — no hard edge |
| Eye color vs. body | High contrast | Acid Green (#39FF14) vs. Corrupt Amber (#FF8C00) — complementary family, strong |

---

## 4. Color Logic Summary

**Emotional read:**
- Vast cool void (GL-04) = the digital world that contains Glitch — its home, but not enough
- Warm glow at threshold (RW-02/03) = what Glitch wants — visible, present, unreachable
- Corrupt Amber body (GL-07) = Glitch itself — neither warm nor cold, neither Real nor Glitch — in-between and wanting
- Acid slit eyes (GL-03) = COVETOUS target-lock — "I could take that"

**The image must communicate:** Glitch is a creature of the void looking at warmth
it did not make and cannot enter. The image is about the gap, not the encounter.

---

## 5. Forbidden Colors in This Frame

| Color | Reason |
|---|---|
| Electric Cyan as ambient fill | GL-01 is Real World screen emission — wrong for this void setting |
| Byte Teal (GL-01b) | Byte is not in this frame |
| Acid Green (GL-03) as fill or accent | Reserved for Glitch eyes only in COVETOUS. No flora in this scene (platform context, not encounter zone) |
| Warm light on Glitch's body | The entire premise is the separation. Do not compromise it. |
| Hot Magenta as fill or background accent | Not this scene — no corruption event, no storm. |

---

## 6. Output Spec

- **Color key thumbnail:** `output/color/color_keys/LTG_COLOR_colorkey_glitch_covetous.png`
  (640×360px — generated by companion script)
- **Written spec (this document):** `output/production/glitch_covetous_styleframe_spec.md`
- **For:** Jordan Reed or Diego Vargas (style frame execution)

---

## 7. Cross-References

- `output/characters/main/glitch.md` — COVETOUS expression values (§7.2, §3.1, §4.2, §5, §6.2, §8)
- `output/color/palettes/master_palette.md` — GL-07 `#FF8C00`, GL-04 `#7B2FBE`, GL-02 `#FF2D6B`
- `output/color/style_frames/ltg_style_frame_color_story.md` — overall arc context
- Jayden Torres critique C16 (79/100 on Glitch) — COVETOUS named as strongest moment
- Alex Chen brief C41 — task source

*Cycle 41 — Sam Kowalski, Color & Style Artist*
