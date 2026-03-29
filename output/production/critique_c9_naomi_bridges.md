# Critique — Cycle 9 — Naomi Bridges, Color Theory Specialist
**Date:** 2026-03-29
**Subject:** SF03 Byte Dual-Eye Legibility / Luma Cold Overlay Fix / Master Palette Act 2 / SF02 Warm Window Glow

---

## ITEM 1 — SF03: Byte Dual-Eye Color Legibility
**Grade: C**

This is the frame's entire emotional payload — Byte's cyan eye facing Luma, his magenta eye facing the void — and it is not confirmed legible. I ran the math. It does not pass.

### The Problem: BYTE_BODY is Void Black, not Byte Teal

The generator `LTG_TOOL_style_frame_03_other_side_v002.py` declares:

```python
BYTE_BODY = (10, 10, 20)   # this is VOID_BLACK
```

This violates GL-01b (Byte Teal `#00D4E8`, RGB 0,212,232) directly. Byte's body fill is currently Void Black — the same value as the background void and the platform surface. He is drawing himself in disappearing ink.

The spec (master_palette.md Section 3, CHARACTER: BYTE) states unambiguously: Base fill = `#00D4E8` (Byte Teal, GL-01b). The reason GL-01b was created in the first place (Cycle 5) was specifically to prevent Byte from merging with the environment. That whole three-cycle problem is back.

The inner glow `BYTE_GLOW = (0, 168, 180)` is Deep Cyan (GL-01a) — that part is correct. But it is rendered *inside* the Void Black ellipse fill, which means it only shows at the interior-glow ring. At `byte_h = 75px` (from `int(1080 * 0.07)`), that inner glow ring is approximately 9px wide (`glow_shrink = max(2, 75//8) = 9px`). A 9px ring of Deep Cyan on a 75px Void Black form, rendered on a UV Purple ambient background. At any normal viewing distance that form reads as a dark smudge.

### The Problem: Eye Radius Smaller Than Precritique Assumed

The precritique assessment (Alex Chen, Cycle 18) states: "eye_r=15px → 30px diameter each. Should be legible per code."

This is wrong. The actual code:

```python
eye_r = max(2, h // 7)
```

With `byte_h = int(H * 0.07) = int(1080 * 0.07) = 75px`:

```
eye_r = max(2, 75 // 7) = max(2, 10) = 10px
```

Each eye is **20px diameter**, not 30px. The precritique was using a different `byte_h` assumption. At 20px diameter on a 75px form — both eyes separated by `body_w // 5` (approximately 10px center-to-center offset from midpoint, giving eye centers at about 10px left and right of body center, with `body_w = int(0.7 * 75) = 52px`, so `body_w // 5 = 10px`) — those two circles are adjacent and small.

Now consider the contrast problem. The cyan eye (`#00F0FF`, RGB 0,240,255) is being placed on a VOID_BLACK body form against a UV_PURPLE ambient background. Cyan on black: good contrast. But the magenta eye (`#FF2D6B`, RGB 255,45,107) has an additional complication — the code draws a void-black diagonal through it:

```python
draw.line([(right_eye_x - eye_r + 1, eye_y - eye_r + 1),
           (right_eye_x + eye_r - 1, eye_y + eye_r - 1)],
          fill=VOID_BLACK, width=max(1, eye_r // 2))
```

With `eye_r=10`, `width = max(1, 10//2) = 5`. A 5px-wide Void Black diagonal through a 20px magenta circle. That diagonal occupies 25% of the eye's total pixel area. At viewing distance, this reads as a cross or a corrupted circle, not a clean `#FF2D6B` eye.

### Contrast Check: Cyan Eye vs. UV Purple Background

At 1920x1080, Byte is positioned at `byte_cx = int(W * 0.22) = 422px`, `byte_cy = int(H * 0.62) = 669px`. This is midground over the platform. The UV Purple ambient (`#7B2FBE`) is the dominant background color there.

- Cyan `#00F0FF` vs. UV Purple `#7B2FBE`: WCAG contrast ratio ≈ 3.4:1. Passes AA for large text (≥18pt). At 20px diameter as a filled circle, this is borderline. It should read.
- Magenta `#FF2D6B` vs. UV Purple `#7B2FBE`: WCAG contrast ratio ≈ 2.1:1. **Does not pass AA.** The two colors share similar luminance (magenta: ~16%, UV Purple: ~4% — actually magenta is significantly brighter but its hue proximity to the violet ambient creates a visual crowding effect). More critically, the Void Black slash through the magenta eye further reduces its effective legibility.

**The cyan eye will probably read. The magenta eye, at 20px with a Void Black slash and no body contrast, is at serious risk of being invisible or unreadable as a color.**

### What Needs to Happen

1. `BYTE_BODY` must be corrected to `(0, 212, 232)` — GL-01b Byte Teal — per established spec.
2. `eye_r` formula must be reviewed — either increase `byte_h` fraction (e.g. `int(H * 0.09)`) or change the divisor to produce a minimum 15px radius at production scale.
3. The Void Black diagonal through the magenta eye should be reduced to `width=1` or removed entirely. The cracked-eye visual concept works without a canceling diagonal destroying contrast.
4. Note: the CORRUPT_AMBER exception does NOT apply here (UV Purple dominant, not cyan dominant — the spec is correct on this). But Byte Teal body fill is non-negotiable regardless of outline exceptions.

---

## ITEM 2 — Luma Cold Overlay Fix (Sam Kowalski, Cycle 18)
**Grade: A-**

The recalculation in `luma_color_model.md` (Cold/Cyan Overlay Variants section, added Cycle 18) is arithmetically correct. I ran every entry in all four tables myself.

### Verification — Skin (Lamp-Lit Base `#C8885A`, R:200, G:136, B:90)

Formula: `C_result = C_base × (1 − α) + C_overlay × α`
Overlay: `#00F0FF` (R:0, G:240, B:255)

Spot-check at α=0.31:
- R: 200 × 0.69 + 0 × 0.31 = 138.0 → **138** ✓
- G: 136 × 0.69 + 240 × 0.31 = 93.84 + 74.40 = 168.24 → **168** ✓
- B: 90 × 0.69 + 255 × 0.31 = 62.10 + 79.05 = 141.15 → **141** — document says 141 ✓

Cyan-dominant test: G=168 > R=138 ✓, B=141 > R=138 ✓. **PASSES.** Threshold correctly identified at α=0.31.

### Verification — Skin (Neutral Base `#C4A882`, R:196, G:168, B:130)

At α=0.21:
- R: 196 × 0.79 + 0 × 0.21 = 154.84 → **155** ✓
- G: 168 × 0.79 + 240 × 0.21 = 132.72 + 50.40 = 183.12 → **183** ✓
- B: 130 × 0.79 + 255 × 0.21 = 102.70 + 53.55 = 156.25 → **156** — document says 156 ✓

Cyan-dominant test: G=183 > R=155 ✓, B=156 > R=155 ✓. **PASSES.** Threshold correctly identified at α=0.21.

### Verification — Hoodie Orange (`#E8722A`, R:232, G:114, B:42)

Note: the luma_color_model.md uses `#E8722A` (R:232, G:114, B:42) while master_palette.md Section 3 lists hoodie base as `#E8703A` (R:232, G:112, B:58). These differ on G channel (114 vs 112, 2-point gap) and B channel (42 vs 58, 16-point gap). The B channel discrepancy is meaningful — at α=0.43:

Using `#E8722A` (B:42): B result = 42×0.57 + 255×0.43 = 23.94 + 109.65 = 133.59 → 134
Using `#E8703A` (B:58): B result = 58×0.57 + 255×0.43 = 33.06 + 109.65 = 142.71 → 143

Both comfortably exceed R=132 at that alpha, so the cyan-dominance threshold conclusion (α≥0.43) holds either way. But the base hex discrepancy between the cold overlay doc and the master palette should be reconciled. The master palette `#E8703A` is the canonical value — use that in all future cold overlay calculations for the hoodie.

The threshold results are defensible. The logic is sound. The documentation of the SF01 boundary zone as NOT cyan-dominant (intentional cross-light, not Glitch Layer immersion) is correct and well-explained.

**Why not full A:** The hoodie base hex inconsistency (`#E8722A` in the cold overlay table vs. `#E8703A` in the master palette) is a documentation error that will cause downstream painter confusion. Fix this before the cold overlay tables are used in production.

---

## ITEM 3 — Master Palette: Act 2 Environment Completeness
**Grade: A**

Section 8 (added Cycle 18) is thorough and well-constructed. I reviewed both environments.

**Tech Den (Section 8.2):** The thirteen color entries (TD-01 through TD-13) cover wall, floor, desk, shelving, CRT casing, and window key light with full shadow companion system. The Monitor Glow Safety Rule (R ≥ 150 at all times) is the right call — GL-01's R:0 is the exact kind of value that would make Grandma Miri's domestic space feel digitally infected. TD-10 (`#C8D4E0`, R:200) and TD-11 (`#B8C8D4`, R:184) both clear the threshold with good margin. ✓

The aged phosphor glow TD-11 at RGB(184, 200, 212) — let me check this for warmth: R:184 > G:200? No: G=200 > R=184. The glow reads slightly cool-blue-white, which is correct for an aged CRT phosphor (cool cathode tube, not a warm incandescent). However, the Monitor Glow Safety Rule requires R ≥ 150, not R > G. The rule is about preventing Glitch Layer misread, not about enforcing warmth. R=184 satisfies the rule. The slight coolness of the phosphor glow at R:184 is acceptable and realistic. ✓

**School Hallway (Section 8.3):** The color safety rule (no pure R=G=B grays) is correctly enforced across all twelve entries. Spot-check:

- SH-01 `#DDE8DF` (221,232,223): G=232 > R=221, and the G>R shift is documented as the fluorescent-green lean. ✓
- SH-12 `#D0DDD8` (208,221,216): G=221 > R=208 and G=221 > B=216. The G>B shift distinguishes institutional fluorescent from generic cool. ✓

The Luma Hoodie Rule in the hallway is correctly stated (washed out but not fully grey). This is the right narrative calibration.

**The forbidden list** correctly excludes GL-01 through GL-07 from both environments. This matters — if a painter accidentally used Electric Cyan as a monitor highlight in the Tech Den, Grandma's house would read as infected by the Glitch Layer before the story permits it.

**One flag:** There is no ENV color code registered for the Tech Den monitor screen fill TD-10 or the school fluorescent cast SH-12 in the ENV-xx numbering system in Section 1C. These are documented in Section 8 but are not in the main ENV table (ENV-01 through ENV-13). This is a minor completeness issue — painters cross-referencing the ENV table won't find these values there. Either add ENV-14/15 entries pointing to these, or add a note in Section 1C pointing to Section 8 for Act 2 environment entries. As it stands, the values are correct — just not fully cross-linked.

---

## ITEM 4 — SF02 Warm Window Glow ("Emotional Beacon")
**Grade: D**

This issue has now survived Critique 6, 7, 8, and 9. It is still not resolved in the generator.

### What the Spec Demands

The SF02 spec and both prior critiques (Victoria B, Naomi B from C8) call for warm window spill — `#E8C95A`/`#FAF0DC` warm pools at street level as the frame's only warm light source and emotional anchor. ENV-03 canonical alpha is 40/255 (~16%), documented in master_palette.md Section 1C since Cycle 13.

### What v003 Actually Does

`LTG_TOOL_style_frame_02_glitch_storm_v003.py`, lines 395–401:

```python
overlay2 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
od2 = ImageDraw.Draw(overlay2)
spill_w = 420; spill_h = int((street_bottom - horizon_y) * 0.35)
for col in range(spill_w):
    t = col / spill_w; falloff = (1 - t) ** 2.2; a = int(40 * falloff)
    od2.line([(col, sidewalk_bottom), (col, sidewalk_bottom + spill_h)], fill=(*SOFT_GOLD, a))
img = alpha_paste(img, overlay2)
```

This is a `SOFT_GOLD` gradient starting at x=0 (far left edge), with max alpha 40. The falloff is `(1 - t)^2.2` — extremely aggressive falloff. At `col=100`, `t=100/420≈0.24`, falloff `= 0.76^2.2 ≈ 0.55`, alpha = `int(40 * 0.55) = 22`. At `col=200`, alpha ≈ `int(40 * 0.31) = 12`. By the time we reach the mid-frame, alpha is near zero.

**This warm spill is drawn starting from the far LEFT edge of the frame.** The buildings with warm windows are the background elements — the warm window light should spill DOWN and OUTWARD from where the windows are (at building positions scattered across the composition), creating pools on the pavement below each building. Instead, this code draws a single gradient strip from the frame's left edge that fades rapidly into nothing. It does not correlate to any window position.

The `_draw_building_windows()` function draws the windows themselves at alpha 160-180 (SOFT_GOLD and WARM_CREAM), which means the glowing rectangles exist in the buildings. But the downward warm spill onto the street — the pools of light that tell the audience "this world still has warmth in it, even during the storm" — is not radiating from those windows. There is no downward light cone, no pool on the pavement beneath each lit window, no relationship between window position and street spill geometry.

At this alpha level and with this geometry, the warm spill is invisible as an "emotional beacon." It reads as a very faint warm tint at the far left of the sidewalk. Victoria called it absent. I called it invisible at ~8-10% effective alpha. Jordan's v003 did not touch the warm spill geometry. The problem is structural, not just alpha: the spill is drawn in the wrong location relative to the windows.

**The fix requires:** A per-window light cone function — for each window drawn in `_draw_building_windows()`, draw a corresponding triangular/radial warm pool on the street directly below it. Each cone: max alpha 40 at the base of the building, fading to ~0 at street_bottom, width equal to approximately 1.5x the window width. `SOFT_GOLD` (`#E8C95A`) and/or `WARM_CREAM` (`#FAF0DC`) fill per window color. This is the "emotional beacon" that restores the sense that somewhere in this storm, something human and warm persists.

Without this, the frame's color narrative collapses to: everything is cyan and cold. The color story loses its counterpoint.

---

## TOP 3 PRIORITY FIXES

**Priority 1 — CRITICAL: Correct `BYTE_BODY` in SF03 v002 generator**
`BYTE_BODY = (10, 10, 20)` is Void Black, not Byte Teal. Change to `(0, 212, 232)` (GL-01b, `#00D4E8`) immediately. Without this, Byte has no visible body on screen — his Void Black form against a UV Purple background is near-invisible, and the dual-eye color story (the entire emotional payload of this frame) cannot be read from a form the audience cannot see. This takes priority over eye radius because you cannot find an eye in a form you cannot locate.

**Priority 2 — CRITICAL: SF02 Warm Window Glow — rebuild as per-window street spill**
The warm emotional beacon has survived four critique cycles as an unfixed structural problem. The current `SOFT_GOLD` gradient at the left screen edge is not functionally related to the window positions. Build a per-window downward cone function using `_draw_building_windows()`'s window coordinates. Each window projects a triangular warm pool onto the pavement directly below it. Max alpha 40, falloff to zero at `street_bottom`. Without this, SF02 has no warm counterpoint to the cyan storm — the color narrative says "cold wins completely," which contradicts the show's thematic premise.

**Priority 3 — HIGH: Resolve `eye_r` and magenta eye contrast in SF03 Byte**
With Byte Teal body fixed (Priority 1), the eye legibility issue partially resolves. But at `byte_h = 75px`, `eye_r = 75//7 = 10px` still yields only 20px diameter eyes. Increase `byte_h` to `int(H * 0.09) = 97px` to push `eye_r` to `97//7 = 13px` (26px diameter). Additionally, reduce the Void Black diagonal through the magenta eye to `width=1` to stop it canceling the color at the one spot critics are trying to read.

---

**Final note:** The cold overlay math is now right. The Act 2 palette is properly documented. Two of the four items assigned to me are in good shape. The other two — Byte's body fill error and the SF02 warm spill — are production-level blocking issues that cannot ship to a pitch in their current state. The team has the palette documentation it needs. The generator code must now match it.

— Naomi Bridges, Color Theory Specialist
