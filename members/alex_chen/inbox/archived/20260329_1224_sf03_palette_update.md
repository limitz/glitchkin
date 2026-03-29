# SF03 Master Palette Update — Cycle 15

**Date:** 2026-03-29 12:24
**From:** Sam Kowalski, Color & Style Artist
**To:** Alex Chen, Art Director
**Re:** Master palette additions from SF03 "The Other Side" color audit

---

Alex,

Completed my Cycle 15 SF03 color support work. Two new colors have been added to `master_palette.md`
(Section 1B and Section 1C). Summary:

## New Palette Entries

### DRW-18 — Luma Hair Base (Glitch Layer)
- **Hex:** `#1A0F0A` | **RGB:** (26, 15, 10)
- **Source:** `#3B2820` Deep Cocoa under UV Purple ambient — hair becomes near-void-dark.
- **Scene use:** SF03 only. Pair with GL-04 `#7B2FBE` UV Purple rim sheen on hair crown.
- **Location in palette:** Section 1B (Derived / Light-Modified Real World Colors) — after DRW-17.

### ENV-13 — Far Structure Edge (Void-Scale)
- **Hex:** `#211136` | **RGB:** (33, 17, 54)
- **Source:** 20% UV Purple `#7B2FBE` over Void Black `#0A0A14`. Verified derivation.
- **Scene use:** SF03 far-distance megastructure silhouettes — edge stroke only (1-2px). NOT a fill color.
- **Distinction:** Different from the depth-tier `FAR_EDGE` `#002837` in bg_glitch_layer_frame.py (that is cyan-derived, for a different context).
- **Location in palette:** Section 1C ENV table — ENV-13 row and expanded entry after ENV-12.

## SF03 Color Notes Document

Full color notes at:
`/home/wipkat/team/output/color/palettes/sf03_other_side_color_notes.md`

Contents:
- Complete master palette map for all SF03 colors (all verified — no undocumented inline tuples remaining)
- Figure-ground safety checks: Luma PASSES against UV Purple mid-distance (orange hoodie vs. purple background — near-complementary, high contrast). Byte PASSES — dark against medium purple, cyan glow readable.
- Warm-light prohibition: SATISFIED. Zero warm light sources. All warm colors are material/pigment only. CORRUPT_AMBER at fragments must be drawn as crack-line strokes, NOT soft radial glows.
- Byte's amber outline: NOT APPLIED in SF03 (UV Purple dominant, not Cyan dominant — 35% threshold not met). Per spec.
- Python constants block for Jordan Reed's generator script included.

## Classroom BG Verification

`LTG_ENV_classroom_bg_v001.png` EXISTS and is clean.
Verification note at: `/home/wipkat/team/output/color/palettes/classroom_bg_color_verification_c15.md`
Zero Glitch contamination. Minor wall color divergence (sage green vs. my Warm Cream estimate) is
a non-issue — generator correctly follows `millbrook_school.md`.

## One Reminder for Alex's Character Composite (SF03)

**GL-01 vs GL-01b:** When you draw Byte's body, use GL-01b `#00D4E8` (Byte Teal) as the body fill.
The ambient environment uses GL-01 `#00F0FF` (Electric Cyan). These must not be swapped.
In SF03, Byte's circuit traces and eye are GL-01 `#00F0FF` (slightly more luminous — "home").
His body fill remains GL-01b `#00D4E8`. The contrast between body fill and trace/eye color is
how he reads at small scale in this wide shot.

Sam Kowalski
Color & Style Artist
Cycle 15
