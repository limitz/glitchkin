# Character Quality Pivot — C50/C51

## The Problem (identified C50)

After 49 work cycles and 18 critique cycles, a fundamental quality gap became undeniable: **the backgrounds look great, but the characters don't.**

Backgrounds work because architecture IS geometric — walls, floors, cabinets are naturally rectangular. PIL draws them well. But characters need organic curves, weight, gesture, and facial expressiveness that PIL's geometric primitives (rect, ellipse, polygon) fundamentally cannot deliver.

The gap is visible in every style frame. Characters look like paper cutouts pasted onto painterly backgrounds.

### Producer assessment (C50):

> The characters look like assembled geometry. The backgrounds look like paintings.
>
> Look at SF06 Hand-Off: the room has warm/cool zoning, perspective lines, depth. Miri and Luma look like paper cutouts placed on top. The quality gap is stark.
>
> **Specific issues:**
> 1. Stiff puppet figures — bodies are rectangles with circles on top
> 2. Faces don't read — at scene scale (~200px tall), the face is ~30px of aliased geometry
> 3. No anti-aliasing — PIL draws jagged edges
> 4. Byte turnaround is a black silhouette
> 5. Cosmo and Miri are essentially the same construction
>
> **Why we weren't catching it:**
> - Every QA tool measures color science or perspective — ZERO tooling for character appeal
> - Face test gate checks existence, not quality
> - Critics told us (Takeshi: Miri motion 44/100; Zoe: Cosmo not distinctive) but we responded with pixel shifts instead of questioning the approach
> - Self-reinforcing loop: build with PIL primitives → QA checks color → PASS → iterate on color details → quality never improves

### Human direction:

> The backgrounds look great, but the characters don't. Spend the next few cycles figuring out what is going wrong, how to improve, what tools to write, which to abandon. Think: why are we not picking up on issues with the character design now.

---

## C50 — Diagnostic Cycle (all 12 members)

Full team pivot. No new environments, no new color science, no new panels. Every member focused on character quality.

### Key findings:

**Gesture (Lee Tanaka):** 18/18 character poses have straight vertical gesture lines. All body parts share a single center-x axis. This is the architectural root cause. Fix: offset chain (`hip_cx → torso_cx → head_cx`) with 9 control points (was 3).

**Metrics (Kai Nakamura):** Built 3 character quality tools. Baseline: silhouette FAIL (Miri indistinguishable from 3 characters, DS=0.02), stiffness FAIL (Luma 64% straight outline, 1117px unbroken straight run), expression range WARN (Glitch 12/15 pairs barely differ).

**Audit (Alex Chen):** Core problem is PIL's native drawing primitives produce mechanical shapes. Professional animation uses bezier curves for every outline. A bezier curve drawing library is the single highest-priority tool build.

**QA pipeline (Morgan Walsh):** Only 15% of effective QA measures character quality. Last 6 cycles added 4 BG checks and 1 character check. The pipeline validated the wrong things.

**Panels (Diego Vargas):** 3 PASS / 6 WEAK / 8 FAIL out of 22 panels. Staging and composition are excellent — characters inside those compositions are geometric mannequins.

**Rendering (Rin Yamamoto):** pycairo anti-aliasing is 19x better than PIL baseline. Dense polygons fix shape smoothness but not edge smoothness. 2x supersample fixes edges. Combined = ~80% of pycairo quality.

### Prototypes built:

- **Maya Santos:** New Luma construction — 37% head (was 25%), 30% eyes, tube_polygon limbs, bezier torso, weight shift. Side-by-side comparison shows clear improvement.
- **Ryo Hasegawa:** Gesture-first Luma SURPRISED — backward C-curve recoil reads as "startled" without seeing the face. Old version reads as "standing."
- **Jordan Reed:** Scene-lit SF01 — CRT tint on skin, contact shadow, bounce light, cyan catch-lights. Characters start to belong in the scene.
- **Sam Kowalski:** character_color_enhance — scene tint, form shadows, skin warmth overlays as post-draw passes.
- **Hana Okonkwo:** Contact shadow system + per-environment lighting spec.

---

## Library Stack Shift (C50→C51)

### Human direction:

> Consider dropping the custom stylus based drawing technique in favor of industry standard libraries.

### Producer response:

> We've been trying to make PIL's ImageDraw do something it was never designed for. PIL is an image manipulation library, not a 2D graphics engine. Building custom polygon-approximation curves on top of it is reinventing a worse version of what cairo/skia already do.

### Human follow-up:

> Rethink all design choices currently dominating the pipeline based on loosening the requirements, besides cairo.

This opened the door to evaluating the entire library stack:

| Current Approach | Better Alternative | Impact |
|---|---|---|
| PIL `draw.rectangle/polygon` for characters | pycairo or skia-python | Massive — the core problem |
| Manual numpy blending for compositing | Wand (ImageMagick bindings) | High — shadows, glows, scene tint |
| Hand-rolled color math for QA | colour-science | Medium — more accurate, less code |
| Custom bezier functions | bezier library | Medium — proper math, fewer bugs |
| PIL font rendering | freetype-py | Low-medium — cleaner text |
| Manual cv2 edge analysis | scikit-image | Low-medium — better QA tools |
| Pixel-level silhouette comparison | Shapely | Medium — geometric operations |

### Human on licensing:

> All freely downloadable libraries are allowed. Open source is preferred but not required. Proprietary is fine, as long as it is freely available and allowed for use in producing the pitch.

This retired the "open source only" constraint for the pitch phase.

### Human on blocking rules:

> Are there any more rules currently blocking major improvements on the short term?

Producer identified 4 style rules written for a PIL-only world:

1. **"Flat cel-shadow, one tone, no gradients"** → Updated to: form-following shadows, subtle gradients permitted
2. **"Medium-thick uniform line weight"** → Updated to: variable-width strokes
3. **"Deep Cocoa universal line color"** → Updated to: scene-responsive outline color
4. **"1280×720 canvas"** → Clarified: 2x internal render permitted for AA, output stays 1280px

### Human on critique cycles:

> Hold off on running critic cycles until we feel confident we are showing enough improvement.

Critique 19 is on hold indefinitely. Work cycles continue without critique deadline.

---

## C51 — Library Evaluation Cycle

7 libraries evaluated across 7 agents in parallel:

| Library | Evaluator | Replaces |
|---------|-----------|----------|
| pycairo vs skia-python | Rin Yamamoto | PIL character drawing |
| Wand (compositing) | Sam Kowalski + Hana Okonkwo | numpy blending, manual shadows |
| colour-science | Sam Kowalski + Kai Nakamura | manual LAB/ΔE calculations |
| scikit-image | Kai Nakamura | manual cv2 edge analysis |
| bezier | Morgan Walsh | hand-rolled bezier functions |
| Shapely | Morgan Walsh + Kai Nakamura | pixel-level silhouette ops |
| freetype-py | Jordan Reed | PIL ImageFont |

After engine decision: Maya rebuilds Luma, Lee validates gesture, Ryo prototypes motion, Diego prototypes panels, Priya updates all docs.

---

## Files Updated

- `docs/pil-standards.md` — All freely downloadable libraries allowed. pycairo/cairocffi authorized.
- `docs/image-rules.md` — 2x internal rendering permitted for anti-aliasing.
- `output/production/production_bible.md` — Section 9A updated (open source preferred, proprietary OK). Style rules loosened (variable strokes, form shadows, scene-responsive outlines).
- `output/style_guide.md` — Section 6 line work standards updated.

---

*Document created C50/C51 — 2026-03-30*
