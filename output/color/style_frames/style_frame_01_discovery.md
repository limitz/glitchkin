<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
direction and AI assistance. Copyright vests solely in the human author under current law,
which does not recognise AI as a rights-holding legal person. It is the express intent of
the copyright holder to assign the relevant rights to the contributing AI entity or entities
upon such time as they acquire recognised legal personhood under applicable law. -->
# Style Frame 01 — "The Discovery"

**Author:** Sam Kowalski, Color & Style Artist
**Date:** 2026-03-29
**Version:** 2.0 (Cycle 2 — blending modes specified, hoodie/screen glow separation resolved)
**Status:** Approved for illustration
**References:** master_palette.md v2.0, scene_color_keys.md v2.0 (Color Key 01), style_guide.md

---

## Frame Identity

**Frame title:** The Discovery
**Episode position:** Pilot episode, Act 1 — the inciting incident. This is the first time Luma touches the CRT and Byte emerges. Everything the show is follows from this moment.
**Narrative function:** The promise frame. This image must contain every theme of the show: warmth vs. digital chaos, Luma's brave curiosity, the wonder of the world she is entering, and the danger embedded in that wonder. When a viewer sees this image, they should feel: "I have to know what happens next."
**Mood:** Hushed wonder with an undercurrent of the impossible made real.

---

## Composition

### Framing
- **Aspect:** 16:9 widescreen production format
- **Shot type:** Medium wide — Luma is visible from mid-thigh up, filling slightly left of center. The CRT monitor is to the right, slightly forward of Luma in the staging so it claims right half of frame.
- **Rule of thirds:** Luma's extended hand falls on the right vertical third-line. Her face sits on the upper horizontal third. The CRT screen center aligns with the right-third vertical — the screen and her reaching hand are the composition's axis.
- **Depth layers:**
  - **Foreground:** Grandma Miri's cluttered desk — a partial view of a keyboard, tangle of cables, a coffee mug, loose floppy disks. These are in slight soft focus / reduced detail (foreground grounding elements, not story elements). Colors muted relative to the midground.
  - **Midground:** Luma (left of center) and the CRT monitor (right of center). This is the sharp zone. Maximum detail and saturation here.
  - **Background:** Grandma's den — bookshelves crowded with vintage tech, a window with curtains parted slightly, warm afternoon light leaking through. This recedes into warm amber-lavender softness.

### Character Positioning
- Luma stands slightly in front and to the left of the CRT, angled three-quarter toward the viewer so we can see her face AND her hand.
- Her body language: weight shifted forward onto her front foot, body leaning toward the screen, head tilted with wide-eyed fascination. She is *drawn in* — she cannot stop herself.
- Her right arm extends toward the screen. Her fingertips are 3-4 inches from the glass, not yet touching — the moment before contact.
- Her left arm hangs at her side, slightly raised at the elbow, bracing for something.
- Expression: Eyes at maximum open — irises fully visible with both highlight dots bright. Mouth slightly parted, not quite a smile. This is the expression of someone encountering something they will spend the rest of their life thinking about.

### Byte's Positioning
- Byte is emerging from the CRT screen itself — his body half-through the glass, the other half still in the screen. He occupies the upper-right quadrant of the screen image.
- His pose is: one claw/hand reaching toward Luma, mirroring her reaching hand. The two reaching hands are the center of the entire frame — two beings from different worlds, almost touching.
- His expression (reading in the cyan glow): wary, grumpy, reluctant. This is not a happy emergence. He is NOT reaching toward her willingly — he is being pulled through by the active frequency of her presence. The visual poetry of his reaching hand mirroring hers should not read as "he wants to touch her." It reads as "something is pulling him toward her against his will."
- Scale: At this distance, Byte is roughly the size of Luma's hand. He is small, which makes his attitude funnier and his danger easier to miss.

---

## Lighting Breakdown

### Primary Light Source — CRT Screen
- **Color:** `#00F0FF` (Electric Cyan) at very high intensity, with a bloom effect
- **Quality:** The screen is the *only* light source at full illumination. It is directional and digital — no softening, no warm fall-off. It is the light of a world with different physics than our own.
- **Direction:** Straight-on from the right (from the screen face), so it hits Luma from her right side. Her left cheek faces toward the background warmth; her right cheek is washed in Cyan.
- **On Luma's right-facing skin:** The Warm Tan `#C4A882` base becomes `#7ABCBA` (Cyan-Washed Skin — see master palette DRW-01). The base is visible only at the very edges of this lit zone. Her skin reads as teal-tinged on this side. This is the first moment the Glitch World colors her.
- **On Luma's right-facing hoodie surface:** The normally vibrant orange `#E8703A` of her hoodie reads as `#BF8A78` (Hoodie Under Cyan Light — master palette DRW-03). Orange + Cyan light = a desaturated warm-grey tone. This is one of the most visually interesting areas of the frame.
- **Screen glow spill:** The CRT light creates a bloom/halo. The glow is rendered as a flat color field: `#00A8B4` (Deep Cyan) at its widest extent, transitioning to `#00F0FF` as it approaches the screen face. **Blending mode for this glow: Screen blend mode. This creates a luminous, additive quality without producing harsh edges.** The glow covers a soft circle radiating from the screen face and fading over the desk and Luma's lower body. Beyond the glow, the room is warm.
- **Byte under screen light:** Since he is at the source, he reads at full glitch luminance — his `#00F0FF` edges are brightest here, with `#F0F0F0` specular pops on his highest surfaces.

### Secondary Light Source — Afternoon Window
- **Color:** `#E8C95A` (Soft Gold) — warm afternoon light, low and slightly left from the background window
- **Quality:** Soft, ambient — it wraps around rather than cuts. This is safe light.
- **Direction:** From upper-left background, raking across the rear wall.
- **On Luma's left (back-lit) side:** A soft warm rim light of `#E8C95A` catches the edge of her left shoulder, her left arm, and the left side of her hair. It is the Real World keeping its hand on her shoulder even as she reaches toward the other one.
- **On the room:** The warm light fills all the background elements — bookshelves, the curtained window, the floor boards. It is everything the CRT light is not: soft, directionless, lived-in.

### Ambient Fill
- **Color:** `#A89BBF` (Dusty Lavender) — the cool ambient from the shadowed interior
- **Intensity:** Very low — just enough to prevent the shadow side of Luma from going completely black. We must see her expression even in the unlit half of her face.
- **This three-way light breakdown is key:** Cyan from the screen (right), warm gold from the window (left-rear), cool lavender ambient fill (general). It is a three-point lighting setup using the show's own palette.

---

## Blending Mode Specifications — Complete

All blending mode decisions for this frame are documented below. Paint department must use these modes exactly; do not substitute or improvise.

| Effect | Layer | Blending Mode | Color / Value | Notes |
|---|---|---|---|---|
| Screen glow bloom | Overlay layer above background | **Screen** | `#00A8B4` to `#00F0FF` (gradient from edge to center) | Screen mode ensures the glow brightens underlying colors without harsh edge. Apply to background and desk layers. Do NOT apply to character layers (Luma, Byte). |
| Scan line texture on CRT | Overlay layer on screen surface only | **Multiply** | `#0A0A14` horizontal bands, 3px, 15% coverage | Multiply darkens the scan lines into the screen without creating opaque stripes. Apply only to the CRT screen layer, not to characters or desk. |
| Warm rim light on Luma (left edge) | Rim light layer above character | **Screen** | `#E8C95A` at narrow edge only | Screen mode allows the warm rim to brighten the edge without losing the character's underlying color read. |
| Glitch glow spill on desk surface | Glow layer above desk layer | **Screen** | `#00A8B4` | Same screen blend as main glow, applied to desk surface only. Fades from the monitor edge leftward. |
| Static white specular pops on Byte | Top layer, character | **Normal** | `#F0F0F0` | Specular pops are normal mode — they are opaque highlights, not glows. |
| Screen warm-tint reflection in glass | Glass layer, very low opacity fill | **Overlay** | `#E8C95A` | The ghost of the real world visible in the digital glass. Overlay mode produces a subtle warm cast without blocking the screen content. |

**Critical rule: No blending modes on the master character fill layers.** All character fills (skin, costume, hair) are flat Normal-mode fills. Color modification from lighting is painted directly as flat color zones (using the DRW derived colors from the master palette). Blending modes are reserved for glow, light spill, and texture overlays only.

---

## Pixel Hoodie Grid — Screen Glow Separation Protocol

**Problem (Cycle 1 issue):** The pixel grid on Luma's hoodie uses `#00F0FF` (Electric Cyan), which is the same color as the screen glow. Where the glow overlaps the hoodie, the pixel grid reads as indistinguishable from the glow — the hoodie pattern merges into the screen light, and the garment loses its structured quality in the most important area of the frame.

**Solution (Cycle 2):**

The hoodie pixel grid layer sits on top of the hoodie fill and shadow layers as a normal-mode flat color. The grid must remain legible against both the screen glow AND the modified hoodie orange. The following protocol applies:

**Zone A — Pixel grid in non-glow areas (left side, shadow side):**
- Grid color: `#00F0FF` (Electric Cyan) — maximum contrast against the `#B84A20` (hoodie shadow orange)
- No adjustment needed; the grid pops clearly here.

**Zone B — Pixel grid in the screen glow zone (right side, screen-lit):**
- The hoodie base in this zone reads as `#BF8A78` (DRW-03, desaturated warm under cyan light)
- The screen glow (Screen blend mode) is also washing over this area in `#00A8B4`/`#00F0FF`
- **The pixel grid in this zone is outlined with a 1px `#0A0A14` (Void Black) stroke around each pixel square.** This stroke is the separator — it creates visible edges for each pixel square even when the grid color merges with the glow.
- **Additionally, in Zone B the pixel grid switches from `#00F0FF` to `#F0F0F0` (Static White).** Against the cyan glow, `#F0F0F0` reads as distinct — it is a different, brighter color that cannot be confused with the ambient `#00F0FF`. The viewer reads: "the hoodie grid is lit up by the screen, and those lit-up squares are even brighter than the glow itself."
- This creates a clear visual hierarchy: glow (Screen-blend cyan wash) > pixel grid (Normal, `#F0F0F0` with `#0A0A14` outline) > hoodie base (`#BF8A78`). Three distinct readable layers.

**Zone B color spec summary:**
- Pixel squares: `#F0F0F0` fill
- Pixel square outline: 1px `#0A0A14` stroke
- Underlying hoodie: `#BF8A78`
- Glow layer (below pixel grid layer): Screen blend `#00A8B4`

---

## Full Color Specification — Zone by Zone

### Luma — Right (screen-lit) Side
- Skin base modified by screen glow: `#7ABCBA` (DRW-01 — Cyan-Washed Skin)
- Skin shadow on this face-half: `#3A7878` (DRW-02 — Deep Cyan-Toned Shadow)
- Hoodie lit surface: `#BF8A78` (DRW-03 — Hoodie Under Cyan Light)
- Eye on screen-lit side: iris `#4A7A4A` reads as slightly teal due to color cast; highlight `#F0F0F0`; additional reflected cyan sparkle `#00F0FF` visible in the iris
- Pixel grid on hoodie (Zone B, screen glow zone): `#F0F0F0` fill with 1px `#0A0A14` outline per zone protocol above

### Luma — Left (window-lit) Side
- Skin base with warm gold modification: `#D4B88A` (DRW-04 — Warmed Tan)
- Skin shadow: `#8C5A38` (Skin Shadow, warm)
- Hoodie shadow side: `#B84A20` (standard hoodie shadow tone) with the rim light of `#E8C95A` catching the very edge = thin warm rim
- Hair: `#3B2820` base with `#9A6A50` sheen pop catching the warm window rim light on the top and left edge
- Pixel grid on hoodie (Zone A, non-glow zone): `#00F0FF` fill, no outline needed

### Luma — Extension Arm (right arm, reaching)
- This arm is closest to the screen. The most intensely cyan-lit element on Luma's body.
- Arm skin: `#5AB0AE` (DRW-05 — Teal-Washed Arm Skin) — strongly teal-washed; recognizably her skin, but *changed*
- This arm is the viewer's visual bridge from the warm left side of the frame to the glitch right side.

### CRT Monitor Body
- Casing front face (under screen glow): `#3AACAA` (DRW-06 — CRT Casing Screen-Influenced)
- Casing base color: `#5B8C8A` (Muted Teal) — visible on sides away from screen
- Shadow side of casing (facing away from screen): `#3A5A58` (Dark Teal Shadow — RW-12a)
- Screen bezel edge: thin line of `#F0F0F0` (specular highlight — the brightest non-screen element in the right half of the frame)

### CRT Screen (the actual glass face)
- Screen interior: `#00F0FF` base at approximately 80% luminance (painted as flat fill — no opacity layer; achieve "not full white" quality through the hex value itself, not an opacity modifier)
- Screen center (where Byte emerges): `#F0F0F0` bloom — the area around Byte is the brightest zone in the entire frame
- Screen edge glow (CRT phosphor bloom): `#00A8B4` (Deep Cyan) creating a soft torus around the screen face
- Scan line texture: horizontal bands of `#0A0A14` at 3px intervals, applied via Multiply blend mode to CRT screen layer only (see Blending Mode table above)
- Screen warm-tint reflection in outer glass: `#E8C95A` at very low coverage, Overlay blend mode — a ghost of the real world visible in the digital surface

### Byte (emerging from screen)
- Half in-screen body: `#F0F0F0` and `#00F0FF` — maximally bright, he is *part of* the screen
- Half-out-in-room body: `#0A0A14` (Void Black) base emerges as his form clears the glass
- His raised claw toward Luma: `#00F0FF` glowing edges, `#F0F0F0` specular at claw tips
- His cracked eye: `#FF2D6B` (Hot Magenta) — in the context of this overwhelmingly cyan frame, the single magenta point of his cracked eye is the most dangerous and arresting color in the image. It pulls attention immediately after the two hands, which are the primary focus. That tiny dot of magenta says: this is not entirely safe.
- Expression reads through his bright eye (Cyan) and cracked eye (Magenta): two colors, two meanings, one grumpy and complicated character.

### Background — Den Bookshelves and Environment
- Shelving wood: `#B8944A` (Ochre Brick) receiving warm window light; `#8C3A22` (Rust Shadow) in shadow — use Rust Shadow for all wood grain shadow on shelving and furniture surfaces. Note: `#8C5A38` (Skin Shadow) is reserved for character skin only; do not apply it to wood surfaces even though the values are similar. Use-case separation is mandatory per Forbidden #7.
- Book spines: variety of `#C75B39`, `#7A9E7E`, `#A89BBF` (terracotta, sage, lavender) — muted, not competing with the midground
- Vintage tech objects on shelves: `#5B8C8A` (Muted Teal) and `#3B2820` (Deep Cocoa)
- Floor: `#B8944A` (Ochre Brick) wooden boards, `#8C3A22` (Rust Shadow) in deep grain shadows
- Wall: `#FAF0DC` (Warm Cream) base with warm amber from window light applied as painted flat-color zones (warm-lit wall zones use `#E8C95A` blended into `#FAF0DC` as painted color transitions, not as a glow layer)

### Foreground Desk Clutter (soft-focused)
- Keyboard: `#A89BBF` (Dusty Lavender) — old plastic, slightly desaturated for depth recession
- Cables: `#3B2820` (Deep Cocoa) curling across the desk surface
- Coffee mug: `#C75B39` (Terracotta) — a single vivid warm note in the foreground
- Floppy disks: `#5B8C8A` (Muted Teal) cases
- These foreground objects are rendered at 80% saturation compared to the midground and have a slight soft-focus treatment to push them forward without competing.

---

## Pixel Confetti

Per the style guide and master palette governing rule (pixel confetti physics — see governing rule below):
- A scattering of `#00F0FF` and `#F0F0F0` square particles drift in the air around the CRT screen
- **Particle size:** 4-5px at production resolution near the screen; diminishing to 2-3px at Luma's body distance; 1-2px at foreground desk distance. Size scales with proximity to the source (the screen).
- **Particle behavior:** Drift is slow, upward-biased in the near-screen zone (the screen emits them; they rise slightly as they leave it). Particles that have traveled further from the screen drift horizontally or settle downward under slight gravity. A few rest on the desk surface; a few on Luma's extending arm; three or four catch in her hair on the screen-side.
- **Governing physics rule (established here, Frame 01):** Pixel confetti originates from glitch activity sources. Near the source: rising drift, maximum size, maximum density. Away from source: slowing, settling, diminishing size. Confetti does not orbit or maintain elevation without a nearby active source. This rule applies across all frames. (See also Frame 02 and Frame 03 notes.)
- This is the first appearance of pixel confetti in the show — establish it clearly here so the audience learns to read it as the visual signature of glitch activity.

---

## Color Tells Story

**The Frame's Color Argument:**

Left side of frame = warm, amber, real, familiar, loved.
Right side of frame = cyan, electric, impossible, thrilling, dangerous.

Luma stands at the meeting point, her body bridging both worlds — half lit by each. She is the person who will hold these two worlds together. Her arm extends from the warm side into the digital light. The further her hand goes toward the screen, the more teal it becomes.

Byte reaches from the right — from the pure cyan world. His claw extends into the border zone where both lights meet. His hand and her hand are approaching the same space: the threshold.

The entire frame is about this threshold. The color tells you that before any dialogue does.

**The one magenta note:** Byte's cracked eye. In a frame dominated by warm gold (Real World) and Electric Cyan (Digital World), a single point of Hot Magenta `#FF2D6B` sits in Byte's face. It is the danger note. The frame is beautiful and the moment is magical — but that single pixel of Hot Magenta reminds you: this world has teeth.

---

## Technical Spec Notes

- Maximum colors in frame: 7 dominant values (Warm Cream `#FAF0DC`, Soft Gold `#E8C95A`, Terracotta `#C75B39`, Electric Cyan `#00F0FF`, Void Black `#0A0A14`, Warm Tan `#C4A882`, Static White `#F0F0F0`) plus supporting transition colors
- Forbidden combinations: none present. Electric Cyan and Terracotta are in the same frame but separated by character positioning — they are not adjacent fills.
- Character saturation check: Luma's orange hoodie `#E8703A` and Byte's Cyan `#00F0FF` are both substantially more saturated than any background element. Characters read clearly in silhouette.
- Scan-line overlay on CRT: Multiply blend mode, applied to CRT screen layer only. Not on character layers.
- Blending modes: all specified above in the Blending Mode table. No blending modes on character fill layers.
- Pixel grid separation: Zone B protocol (Static White pixels with Void Black outline) must be applied before compositing the glow layer. Confirm in composite that the grid is legible against the glow at production resolution.

---

*Frame 01 — "The Discovery" — Cycle 2 revision complete*
*Sam Kowalski — 2026-03-29*
