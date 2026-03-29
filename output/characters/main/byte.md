# BYTE — Character Design Document
## "Luma & the Glitchkin" — Main Character #3 (Glitchkin Companion)

**Designer:** Maya Santos
**Date:** 2026-03-29
**Version:** 3.2 (Cycle 13 — Cracked-Eye Dead-Pixel Glyph + Storm-Scene Variant)
**Status:** Updated — Chamfered-box design retired Cycle 8; oval body is canonical

---

## 1. CHARACTER OVERVIEW

Byte is the most visually unique character in the trio — and the most complex to execute. He is a reformed Glitchkin who has chosen (reluctantly, and while complaining about it) to ally with Luma. He is grumpy, sarcastic, secretly protective, and speaks in clipped fragments that sound like corrupted data packets. He is approximately 6 inches tall and rides on Luma's shoulder.

The design challenge is substantial: Byte needs to be:
1. **Legible at tiny size** — he appears on Luma's shoulder, which in a medium shot makes him roughly 40-60px tall. Every key design element must survive that scale.
2. **Geometrically distinct** — while Luma is circles and Cosmo is rectangles, Byte is triangles and jagged polygons. This must be immediately readable without making him look threatening (his small size and expressive face prevent this).
3. **Digitally coherent** — he IS data made physical. His design should feel like something that came through a corrupted file transfer. Not cute-ified — genuinely strange, but strange in a way we learn to love.
4. **Expressively rich** — despite his small size, Byte needs a full emotional range. The pixel-eye system must carry most of this weight.

---

## 2. SHAPE LANGUAGE

### Primary Shapes

> **Cycle 8 design revision:** The chamfered-box body described in Version 2.0 has been **retired**. Byte's canonical body shape is now an **oval/ellipse**. See Section 4 for updated construction details. The chamfered-box rationale below is preserved for historical reference only — it no longer reflects Byte's production design.

- **Body core:** An oval (ellipse) form — wider than tall, soft-edged, organic despite being digital. The oval reads as buoyant and floating-ready rather than architectural. It is the primary silhouette read for Byte at any scale. At shoulder-ride distance, the oval is immediately distinguishable from Luma's circle-based head and from the rectangular/architectural elements of the Glitch Layer environment.
- **Head/body distinction:** Like the original cube design, Byte does NOT have a separate head and body. The entire oval mass is one unified form. The face occupies roughly the front-facing surface of the oval. It reads naturally as a face because the eyes, nose-mark and mouth are centered on the widest, most forward-facing aspect.
- **Limbs:** Four stubby limbs sprout from the perimeter of the oval — two from the lower arc (leg-analogues), two from the upper sides (arm-analogues). Each limb is a short, rounded-tip appendage. They are expressive through angle and energy, not through digit detail. No fingers.
- **The Floating:** Byte does not walk — he floats approximately 0.25 heads above any surface. Below his lower limb tips, small pixel confetti squares scatter and cycle — his floating mechanism. This is the show's pixel confetti signature, and Byte is its primary source.

### Shape Language Rationale (Updated — Oval)
The oval form reads as soft, buoyant, and slightly uncertain — which matches Byte's personality (grumpy but secretly protective, not menacing). It also creates immediate figure-ground separation from the rectangular CRT screen from which he emerges, and from the hard-edged Glitch Layer environment. The oval is consistent with the show's character shape language: Luma = circles, Cosmo = rectangles, Byte = oval (intermediate — neither fully human-organic nor fully digital-geometric).

### Retired Design Note (Chamfered-Box — Version 2.0)
The original chamfered-box design (Version 2.0) used a cube with 45-degree chamfered edges, triangular notches, and a geometric spike cowlick. It was retired in Cycle 8 after `byte_expressions_generator.py` and `style_frame_01_rendered.py` converged on the oval form for production legibility reasons. The chamfered-box rationale (triangles = danger/mischief, corrupted geometry = history) was sound conceptually but produced a body that was too complex to read at Byte's operating scale (shoulder-ride / 40-60px). The oval achieves the same "ancient corrupted digital creature" reading through the face expression system rather than body geometry.

---

## 3. PROPORTIONS (Head Units)

**Total height: 2.0 "heads" — but for Byte, "head" is defined differently**

For Byte's proportions, one "head unit" = the width of his body oval (which IS his head — they are the same thing). His absolute height is approximately 6 inches (155mm) which corresponds to roughly 0.5% of Luma's total height.

| Body Section | Measurement | Notes |
|---|---|---|
| Body oval | 1.0 unit | The main body/head mass. Oval is approximately 1.0:0.85 (W:H) — wider than tall. |
| Lower limb pair | 0.6 units | Each lower limb is 0.6 units long from the oval base to the tip. |
| Upper limb pair | 0.5 units | Slightly shorter arm-limbs, sprouting from the oval sides. |
| Floating clearance | 0.25 units | Gap between lower limb tips and the surface. |
| **Total visual height** | **~2.0 units** | Including floating clearance |

**Face occupancy:** The face takes up approximately 70% of the forward-facing oval surface. Eyes are the dominant elements — each eye occupies 0.35 units width x 0.25 units height. Nose and mouth combined occupy the lower 30% of the face.

**Size in relation to Luma:**
- Byte fits on Luma's shoulder with approximately 0.15 "Luma heads" of clearance above him before he'd touch her jaw.
- His body width is approximately 0.22 of Luma's shoulder-to-shoulder width.
- In a full-body shot showing both characters, Byte is clearly small enough to be cupped in one of Luma's hands, but large enough to be readable as a distinct character.
- See Size Comparison section (Section 11) for full breakdown.

---

## 4. BODY CONSTRUCTION — DETAILED

### The Oval Form (Canonical — Cycle 8+)

> **Note:** The chamfered-cube construction described in Version 2.0 has been retired. The following describes the current canonical oval body. See "Retired Design Note" in Section 2 for context.

The main body oval is a rounded ellipse, wider than tall. Unlike the retired cube, it has no hard edges — the form is continuous. Its personality quirks are expressed through the face system and glitch-scar detail rather than body geometry.

**Left side (viewer's right):** Standard oval arc. Receives Soft Gold lamp rim light in Frame 01 three-light setup.

**Right side (viewer's left):** Standard oval arc. More exposed to monitor wall cyan in Frame 01. The glitch-scar markings (see Color section) are concentrated here — a Hot Magenta diagonal crack that functions as Byte's distinctive mark.

**Top arc:** Smooth oval top. No geometric spike (retired with chamfered-box design).

**Bottom arc:** Smooth oval base. Lower limbs sprout from the lower portion of the oval perimeter.

**Back surface:** The oval form is drawn as a 2D projection; the back is not independently detailed in production assets.

### The Limbs
**Lower limbs (2):** Sprout from the lower arc of the oval, angling downward and slightly outward. Each is a short, rounded-tip appendage. They function like stubby legs — oriented downward in "floating" position, can swing forward and back. No triangular wedge shape (retired with cube design).

**Upper limbs (2):** Sprout from the upper side-arcs of the oval (approximately 0.3 units down from the top), angling outward and slightly forward. These are arm-analogues. Slightly shorter than the lower limbs. They end in a slightly wider blunt tip — not a hand, but expressive through angle and energy. No fingers.

**Limb expressions — Full Vocabulary (8 specified configurations):**

Because Byte cannot change his posture much (oval body, stubby limbs), the ANGLE and ENERGY of his limbs carry significant expressive weight. All limb positions described from viewer's perspective. Lower limb angles are measured from vertical (0° = pointing straight down).

**Configuration 1: GRUMPY NEUTRAL**
- Upper limbs: flat against body sides, angled slightly downward at 10° from horizontal. Tips point toward lower-front corners of the body.
- Lower limbs: pointing straight down (0° from vertical). Parallel, even.
- Reading: "I am here. I have not agreed to anything."
- Use for: default, observing, waiting, low-energy states.

**Configuration 2: DEFENSIVE / CLOSED**
- Upper limbs: pressed tight to the forward oval surface, crossing slightly inward over the chest — left over right. Tips overlap at center.
- Lower limbs: angled slightly inward and forward (10° from vertical, toed-in) — closed stance.
- Reading: "I am not available. Do not ask me for things."
- Use for: dismissal, avoidance, sulking, smug satisfaction (pairs with star pixel-eye).

**Configuration 3: ALARMED / MAXIMUM EXTENT**
- Upper limbs: fully extended outward and upward — 45° above horizontal, pointing away from the body. Maximum spread.
- Lower limbs: extended downward and outward at 20° from vertical — braced, wide stance.
- Body: rigid, all edges sharp.
- Reading: "EVERYTHING IS BAD. RIGHT NOW. IMMEDIATELY."
- Use for: alarm, genuine fear, urgent warning. Pairs with warning triangle pixel-eye.

**Configuration 4: ACCUSATORY POINT**
- Upper limbs: one (typically right, viewer's left) extends forward and slightly up at 30° from horizontal — pointing directly at the target. The pointing limb tip is at maximum extension. Other upper limb pulled back, pressed to body.
- Lower limbs: angled forward (15° from vertical, forward-tilt) — he is leaning into the accusation.
- Body: tilted 15° toward the accusation target.
- Reading: "You. Specifically you. This is your fault."
- Use for: blame, explanation, pointing out what someone missed.

**Configuration 5: RELUCTANT ENGAGEMENT (Arms Forward)**
- Upper limbs: both extended forward at 0° (horizontal), parallel, aimed at the task. Not excited — functional.
- Lower limbs: straight down, even (same as neutral).
- Body: oriented directly toward the task. Face oval front-surface aimed at goal direction.
- Reading: "I am doing this. Do not thank me. I will accept no compliments."
- Use for: Reluctant Effort expression (Expression 7), problem-solving, action sequences.

**Configuration 6: SMUG RECLINE**
- Upper limbs: crossed over the forward oval surface — right over left (opposite of defensive crossing). Tips pointing outward. This is arms-folded-leaning-back energy.
- Lower limbs: crossed at tips (right in front of left) — lower limbs hooked over each other, floating.
- Body: tilted 10° backward — he is literally leaning away from whatever is happening.
- Reading: "I am observing this situation from a position of superior experience."
- Use for: Smug expression (Expression 5), watching others fail at something he warned them about.

**Configuration 7: DESPERATE REACH**
- Upper limbs: both extended forward and downward at 30° below horizontal — reaching, grasping. Tips straining toward the target.
- Lower limbs: extended backward and upward at 30° from vertical — kicking back for momentum, floating fast.
- Body: tilted 25° forward — maximum forward lean.
- Reading: "I require this. I am acquiring this. Nothing will stop me. Please note I said please."
- Use for: high-stakes retrieval, urgent motion, dramatic moments of Byte actually committing fully. Rare — his full commitment is a character beat.

**Configuration 8: PROCESSING / IDLE FLOAT**
- Upper limbs: drifting loose from body at 20° from horizontal, slightly forward. No tension — the tips point generally forward-downward but without intent.
- Lower limbs: relaxed, angled slightly outward and downward (10° from vertical, angled out) — not gripping or bracing.
- Body: very slight wobble rotation — in animation, this is a subtle 5° left-right oscillation at 0.5Hz, indicating idle processing state.
- Reading: "I am thinking. Not at you. Just thinking."
- Use for: processing/loading expressions, quiet scenes, when Byte has gone internal.

**Cross-reference with expression sheet:** These 8 configurations can be mixed with any pixel-eye expression. The strongest pairings are: Configuration 3 + Warning Triangle, Configuration 6 + Star, Configuration 3 + Heart (brief moment before he switches to Configuration 2 to suppress it), Configuration 5 + Flat Line.

### The Floating Mechanism — Pixel Confetti
Below Byte's lower limb tips, a constant stream of tiny pixel squares circulates in a loose cloud formation. This is his locomotion/hovering system.

**Pixel confetti composition (beneath Byte):**
- Approximately 8-12 squares visible at any time, in varying sizes (0.04-0.02 units square)
- Colors cycle through the Glitch Palette: Electric Cyan, Hot Magenta, Acid Green, UV Purple, and Static White
- They do NOT have a pattern — they scatter randomly below and just ahead of his forward direction
- When he accelerates, the confetti extends further behind him in a trail
- When he stops suddenly, confetti scatters outward in a burst
- When he's angry/agitated, the confetti flickers more rapidly and gains red-shifted colors (more magenta, less cyan)

---

## 5. FACIAL CONSTRUCTION

### Face Plane
Byte's face is the forward-facing oval surface. It occupies the widest, most prominent aspect of the oval form — the natural "front" of an ellipsoid body. Within that face, the design is organized into two zones:
- **Upper 65%:** Eyes. Dominated by two large, expressive eye structures.
- **Lower 35%:** Nose indication and mouth.

### The Two Eyes — System Overview
Byte's two eyes are fundamentally different from each other, and this asymmetry is his most important design feature.

**Left eye (viewer's right — the NORMAL eye):**
A rounded rectangular shape, similar in construction to Luma's eyes but with harder corners. This is his "regular" eye. It follows standard cartoon eye rules:
- Iris: **Electric Cyan (#00F0FF)** — deep, glowing, digital
- Pupil: **Void Black (#0A0A14)**
- Eye white: **#E8F8FF** — a very slightly blue-tinted white (he is not human — his "whites" are not organic)
- Highlight: **Static White (#F0F0F0)**, upper-left position
- Eyelid: a clean arc at the top, simple line at the bottom
- Behavior: moves and dilates like a regular cartoon eye — pupil expands in delight, contracts in anger, eyes half-lid in contempt

**Right eye (viewer's left — the CRACKED/GLITCH EYE):**
This is Byte's defining visual hook. The right eye is cracked — a fracture line runs diagonally from the upper-left to the lower-right of the eye's "lens" surface, as if the eye is a small screen that has been struck. The crack is rendered as a jagged zigzag line in **Void Black (#0A0A14)** over the eye surface.

The cracked eye does NOT display iris/pupil in the traditional sense. Instead, it functions as a small PIXEL DISPLAY — it shows a pixel-art symbol that communicates Byte's internal emotional state. The symbols are described in the Pixel-Eye Variant section below.

**The cracked eye frame:**
- The outer frame of the cracked eye is IRREGULARLY shaped — not a clean rectangle. The crack event has warped the frame slightly. The top-right corner has a small chip/fragment missing (triangular gap, like a corner of a screen knocked off).
- The background color of the cracked eye (the "off" state) is **Void Black (#0A0A14)**
- The pixel symbols display in bright colors against this void background

### Pixel-Eye Variants (Full List)

Each symbol is a pixel-art icon drawn at approximately 0.25 units x 0.20 units — small, but legible. All symbols display in pixel-art style (blocky, square-based, no curves — jagged diagonals made of squares).

| Emotion | Symbol | Display Color | Description |
|---|---|---|---|
| Angry / Irritated | Exclamation mark (!) | Hot Magenta #FF2D6B | Bold upright line with a dot below. The exclamation mark is fat and pixelated. Flickers slightly when he's very angry — as if the display is struggling. |
| Confused / Uncertain | Question mark (?) | Electric Cyan #00F0FF | Pixel-art question mark. The curl at the top is approximated with pixel steps — it looks slightly angular. Steady display. |
| Accidental affection | Heart | UV Purple #7B2FBE | A small pixel heart — the classic 8-bit heart shape. Displays BRIEFLY and then he switches it off (literally turns the display to black) as if embarrassed. This is his most comedically important expression. |
| Frightened / Alarmed | Triangle warning (⚠) | Acid Green #39FF14 | Pixel-art warning triangle with exclamation inside. Corners are slightly uneven (because he's scared). Flickers rapidly. |
| Pleased / Smug | Star / Asterisk (*) | Soft Gold #E8C95A | A small 8-pointed star or asterisk. Clean and steady — he is confident in his smugness. |
| Sad / Glum | Downward arrow (↓) | Electric Cyan #00F0FF at 50% brightness (dim) | A single downward-pointing pixel arrow. Dimmer than other symbols — low energy state. |
| Searching / Processing | Rotating dots (loading indicator) | Alternating Cyan / Magenta | Three dots that appear to cycle/pulse — approximated as three squares that brighten in sequence. Indicates he's thinking or scanning. |
| Content / Resting | Flat line (—) | Static White #F0F0F0 at 70% brightness | A simple horizontal pixel line. This is his "at rest" symbol when he doesn't feel like displaying anything. The most economical expression. |

**Pixel-eye display rules:**
- The symbol fills approximately 60% of the cracked eye frame's interior
- The crack line is ALWAYS visible over the symbol — it does not disappear when displaying
- The screen CAN go to full black (all off) — this is when he's trying to hide his expression. It reads as a blank dark rectangle, which is somehow MORE expressive than any symbol.
- Symbols do not have to be held — they can flicker, transition, or briefly flash between states to show complex mixed emotions
- In still artwork (model sheets, promo art), the cracked eye is shown displaying the symbol most associated with the scene or character study in question

### Nose
Byte does not have a traditional nose. Between his two eyes, there is a small triangular bump — a faceted geometric protrusion that reads as "where a nose would be" by convention. It casts a small shadow triangle below it. No nostrils. Just the small angular bump. It gives the face a slight 3D quality without being organic.

### Mouth
Byte's mouth is a direct horizontal line segment — hard-edged, rigid. Unlike the organic curve of Luma and Cosmo's mouths, Byte's mouth appears to be a gap in his face surface — like a command line interface. It can:
- Close completely (face plate seals — he is DONE talking)
- Open into a rectangular gap revealing rows of tiny pixel-teeth — small white squares arranged in a grid, visible in the opening
- Extend to the sides for an expression of exasperation or "what is even happening"
- Compress to a thin line for contempt

**The mouth as interface:** This is subtle but important — Byte's mouth feels like it is opened and closed by a process, not by muscles. It does not deform organically. It moves in hard increments. This reinforces his digital nature even while the rest of his expressions become more organic-looking over the course of the show.

---

## 6. COMPLETE COLOR BREAKDOWN

### Body Core
| Area | Color Name | Hex | Notes |
|---|---|---|---|
| Base body | Electric Cyan | #00F0FF | His primary color — the glitch palette's signature. Flat fill, no gradient. |
| Shadow tone | Deep Cyan | #00A8B5 | Occupies the underside of the oval body and the undersides of limbs. |
| Highlight tone | White-Cyan | #80F8FF | The top arc of the oval and the top surfaces of limbs where light strikes. |
| Scar ground | Void Black | #0A0A14 | Used for crack lines on the glitch-scar markings — dark voids rendered as gaps. |

### Glitch-Scar Markings
The Hot Magenta markings on Byte's body are the evidence of his corrupted past — places where his data was damaged and repaired or partially overwritten. They appear as:

| Marking Type | Color | Hex | Placement |
|---|---|---|---|
| Primary scar line | Hot Magenta | #FF2D6B | A diagonal scar-stripe running from upper-right to lower-left across the front face — approximately 0.08 units wide. |
| Secondary scatter marks | Hot Magenta at 70% | #FF2D6B with reduced opacity effect (use #C4235A flat) | Small rectangular patches of 2-4 pixels grouped near the main scar. |
| Scar continuation | Hot Magenta | #FF2D6B | The main scar line continues onto the side arc of the oval at reduced width. |
| Shadow on scar | Dark Magenta | #9E1540 | Shadow tone applied to the scar elements in shadow zones. |
| Highlight on scar | Light Magenta | #FF6090 | Highlight tone for scar elements on lit faces. |

**Scar placement rationale:** The diagonal scar crossing the face is visually dynamic — it creates a directional movement across his face that offsets his bilateral symmetry. The scar goes from upper-right to lower-left, which in viewing convention is a "received blow from the upper-right" — consistent with his backstory as a corrupted and subsequently reformed Glitchkin.

### Eyes
| Area | Color Name | Hex | Notes |
|---|---|---|---|
| Normal eye iris | Electric Cyan | #00F0FF | Glowing — almost the same as his body color, but on the eye it reads separately because of the dark frame. |
| Normal eye pupil | Void Black | #0A0A14 | Hard, dark point. |
| Eye white (normal) | Blue-Tinted White | #E8F8FF | Not organic white — digital white with a cool blue cast. |
| Cracked eye background | Void Black | #0A0A14 | The off-state background of the display. |
| Crack line | Void Black | #0A0A14 | Same as the interior — the crack is a gap, not a drawing. |
| Eye frame color | Deep Cyan-Gray | #1A3A40 | The "bezel" surrounding each eye, framed by a darker border. |

### Limbs
Limbs follow the same shadow/highlight/base system as the body. The tapered shape means the highlight appears on the top/front surface of each limb, the shadow on the underside/back surface.

### Line Work
- **Silhouette lines:** Void Black (#0A0A14) — as specified in the brief. This distinguishes him from Luma and Cosmo's Deep Cocoa lines.
- **Internal detail lines:** Void Black (#0A0A14) at 60% weight
- **Scar lines:** The scar marking is a fill element, NOT a line — it is applied as a flat color shape, not drawn with a stroke.
- **Jitter/offset lines:** Per the style guide, Byte's outline can use the "glitch line" treatment — a slight zigzag or dual-offset line at his silhouette edges. This should be subtle (not cartoonishly dramatic) and consistent in its application. Think of a slightly loose JPEG rendering of his edges.

---

## 7. EXPRESSION SHEET — 8 KEY EXPRESSIONS (Including Pixel-Eye Variants)

### Expression 1: DEFAULT GRUMPY NEUTRAL
**Emotional state:** This is his baseline. Not angry. Not sad. Just existing at minimum enjoyment of the current situation.

**Pixel eye:** Flat line (—) in Static White at 70%

**Face construction:**
- Normal eye: half-open, 60% aperture. Flat lower lid. The pupil is centered, small. The iris is not glowing maximally — just on.
- Cracked eye: flat line display. Dark background, white horizontal pixel line.
- Mouth: closed. A thin horizontal line with slightly downturned ends — barely, but it's there.
- Limbs: arms close to body sides. Lower limbs pointing straight down.

**The feeling:** He is here. He is aware you need something. He has not agreed to help yet. The negotiation is ongoing.

---

### Expression 2: IRRITATED / ANGRY
**Emotional state:** Someone has said something foolish. He can see at least four better approaches. Nobody asked.

**Pixel eye:** Exclamation mark (!) in Hot Magenta, flickering

**Face construction:**
- Normal eye: 50% aperture, top lid heavy and low. The pupil CONSTRICTS — very small dot. The iris dims slightly.
- Cracked eye: Exclamation in flicker mode — the ! blinks at approximately 3-second intervals.
- Mouth: opens into a narrow horizontal rectangle — like a mail slot. Small pixel teeth visible as a grid within the opening.
- The diagonal scar on his face appears more prominent in anger expressions — the contrast between his body cyan and the magenta scar is heightened.
- Limbs: upper limbs raised to sides, angle upward at 30-45 degrees — the body equivalent of raised fists.
- Body: tilts very slightly toward whoever has irritated him.
- Pixel confetti beneath him: more rapid cycling, shifting toward hot magenta in color.

**The feeling:** He is not going to say it. He is absolutely going to say it. There will be nothing left of the idea by the time he is done.

---

### Expression 3: ACCIDENTAL AFFECTION (THE HEART — Most Important Expression)
**Emotional state:** Luma has done something unexpectedly touching. He did not ask for feelings. He did not consent to feelings. The feelings happened anyway.

**Pixel eye:** Heart symbol in UV Purple — but displaying for only 1-2 seconds before the display goes to FULL BLACK as he shuts it down

**Face construction:**
- Normal eye: WIDE OPEN — maximum aperture. Pupils dilated — large. The iris glows maximally. For this brief moment, his normal eye looks soft and warm.
- Cracked eye: Heart appears, then cuts to black as he suppresses it. The transition from heart to black is abrupt — no fade.
- Mouth: CLOSED firmly, with slightly upturned corners that he is ACTIVELY working to suppress.
- Limbs: arms pressed to his sides — he is literally holding himself together.
- Body: rotated AWAY from whoever triggered this, approximately 15 degrees. If he's on Luma's shoulder, he faces away from her.
- Pixel confetti: brief burst of violet pixels, then resolving back to the normal cyan/magenta cycle.

**The key acting note:** The switch from heart to black eye must happen within 2 seconds. The comedy is in the suppression, not the display. Show the heart just long enough for the audience to register it, then cut it off.

**The feeling:** He doesn't have feelings about this. That was a technical glitch. It won't happen again.

---

### Expression 4: CONFUSED / PROCESSING
**Emotional state:** He has encountered information that does not parse correctly. His world model is updating.

**Pixel eye:** Question mark (?) in Electric Cyan, steady

**Face construction:**
- Normal eye: tilts slightly — the whole eye ROTATES slightly (the pupil moves to the lower portion of the iris, and the upper eyelid curves in a slightly different direction). This is the cartoon equivalent of a head tilt for him.
- Cracked eye: Question mark, clear and steady.
- Mouth: opens into a small square gap — not expressive, just open as if he was about to say something and the words didn't come.
- Body: leans slightly to one side — approximately 10 degree tilt.
- Limbs: upper limbs drift upward and outward, slightly — a shrug analogue.
- The small triangular spike on top of his head (his "cowlick") seems to droop forward — though this is more of an animation detail.

**The feeling:** Does not compute. Running alternate interpretation. Please hold.

---

### Expression 5: SMUG / TOLD YOU SO (His Version of Cosmo's Deadpan)
**Emotional state:** He was right. He was always going to be right. He has always known this.

**Pixel eye:** Star/Asterisk in Soft Gold, steady and bright

**Face construction:**
- Normal eye: half-lidded — 55% aperture, top lid very heavy and low. The pupil moves to a slightly higher position in the iris, giving a "looking down at you" angle despite his small size.
- Cracked eye: Star display, held steady. The star feels SELF-SATISFIED.
- Mouth: closed, with a clear upward curve at the corners — a smirk, the first time his mouth curves upward noticeably. One side curves more than the other — asymmetric smirk.
- Body: leans back very slightly — he is reclining into his smugness.
- Limbs: upper limbs crossed over his forward oval surface — arms folded analogue.

**The feeling:** He warned them. The warning was ignored. Events have confirmed the warning. He requires no acknowledgment. The data speaks.

---

### Expression 6: ALARMED / FRIGHTENED
**Emotional state:** Something has gone wrong that is beyond normal calculation. The situation has exceeded his parameters. He is scared.

**Pixel eye:** Warning triangle (⚠) in Acid Green, flickering rapidly

**Face construction:**
- Normal eye: WIDE OPEN, maximum aperture. But unlike the Accidental Affection expression, the pupil here SHRINKS — a tiny constricted dot. Too much light. Too much information.
- Cracked eye: Warning triangle, flickering rapidly (approximately 8 flickers per second).
- Mouth: gaping — opens to maximum width, pixel teeth exposed. The mouth opening is wider than usual.
- Pixel confetti beneath him: RAPID cycle, colors flickering wildly, confetti particles multiplying — up to 20 squares visible, cycling through every color in the Glitch Palette at once.
- Body: rigid — every limb extends outward, pointing away from the threat. He is maximally expanded.
- The glitch-scar markings may briefly light up — an optional animation beat where the Hot Magenta scars pulse brighter for a moment under stress.

**The feeling:** Abort. Abort. This was not in the expected outcome space. He would like to not be here.

---

### Expression 7: RELUCTANT EFFORT / "FINE"
**Emotional state:** He has decided to help. Against his stated preference and better judgment. There has been an internal negotiation and the side that cares about the outcome has won, narrowly.

**Pixel eye:** Flat line (—) in Static White, at full brightness (not the dimmed 70% neutral)

**Face construction:**
- Normal eye: fully open, 85% aperture — the determination is real, even if reluctant. Eye directed forward and slightly upward — toward the task.
- Cracked eye: flat line, bright. Not displaying emotion — he is not giving you the satisfaction of knowing how he feels about this.
- Mouth: set — the closed horizontal line from his neutral, but pulled tighter. The mouth is a firm line now. He has committed.
- Body: squared forward — aligned with the direction of action, oval front surface fully aimed at the goal.
- Limbs: arms pointing forward — upper limbs angled toward the task.
- Pixel confetti: steady, even — calm beneath him. He is in control.

**The feeling:** He is going to do the thing. He will mention his reservations while doing it. You may not interrupt the doing to address the reservations.

---

### Expression 8: SECRETLY PLEASED / SATISFIED
**Emotional state:** Something worked. He had a role in making it work. He is not going to make a big deal about this. He is going to be a little bit smug while making no external indication that he is pleased.

**Pixel eye:** Star in Soft Gold, but DIMMER than Expression 5's star — as if he's only allowing it half-power

**Face construction:**
- Normal eye: 80% aperture — more open than neutral, less than full delight. The pupil is soft-centered. The iris glows slightly — not maximum, but noticeably warm.
- Cracked eye: dim star. Barely on. As if he's allowing it but keeping it discreet.
- Mouth: closed, absolutely flat — NO smirk this time. He is maintaining the facade. But the corners of the mouth are tense with the effort of NOT smiling.
- Body: posture slightly straighter than neutral — he is holding himself well.
- Limbs: close to the body — nothing betraying him.
- Pixel confetti: slightly slower cycle than normal. He is resting in the moment.

**The difference between this and Expression 5 (Smug):** Smugness is directed outward — he wants the acknowledgment. This expression is directed inward — he's having a private moment of satisfaction. The dimmed star is key: he hasn't turned it off completely, but he's keeping it private.

**The feeling:** He helped. It worked. Internally, he is doing a small celebration. Externally, he is a silent oval. Nobody needs to know.

---

## 8. ACTION POSE

### Pose: Riding on Luma's Shoulder, Pointing Urgently

**Context:** This is the canonical Byte-in-action pose. He is on Luma's right shoulder (viewer's left), facing in the same direction she is — the direction of travel or action. He is pointing urgently at something off-frame to the right.

**Body position:**
- He sits on Luma's shoulder, slightly angled inward toward her neck for stability. His lower limbs curl loosely over the back of her shoulder — hooked, not gripping.
- His body is rotated approximately 30 degrees away from the viewer (facing toward where he's pointing), so we see him in partial 3/4 view.
- Upper-front limb (viewer's right) extends fully toward the destination — pointing. The tip is at its maximum angular extension from the body.
- Upper-back limb (viewer's left) is pulled back and pressed to his body, in a leaning-in gesture.
- His body leans slightly in the direction of the point — forward and toward the target.

**Expression in this pose:** A mix of Alarmed (Expression 6) and Reluctant Effort (Expression 7). The pixel eye shows the Warning Triangle (⚠) in acid green. His normal eye is wide open. His mouth is open — he is speaking, urgently, in whatever clipped fragments constitute shouted data.

**Positioning on Luma:**
- He occupies the area from just below the top of her shoulder to just above her ear.
- The pixel confetti below his feet circulates against the surface of her hoodie — tiny squares bouncing off the orange fabric. A subtle interaction suggesting the hoodie's pixel pattern and his confetti share the same digital language.
- His scale relative to her head: his total height is approximately 20% of her head height. He is clearly, comically small — but his pointing gesture is completely authoritative.

**Luma's response to this pose:**
(This note is for the ensemble/lineup document, but noted here for context.) Luma's expression in this paired pose is the Reckless Excitement grin. She can SEE what he's pointing at. She was already going there. Byte pointing has only confirmed and accelerated her plan.

---

## 9AA. PIXEL-EYE PRODUCTION SCALE THRESHOLDS — DEFINITIVE SPECIFICATION

**This section is the locked production standard for all pixel-eye display decisions. Use this before any shot containing Byte.**

### Frame-Height Percentage Thresholds (1080p Reference)

| Byte Character Height | Frame % | Pixel Height (1080p) | Pixel-Eye Rule |
|---|---|---|---|
| Above 25% of frame height | >25% | >270px | **FULL DETAIL** — use 7×6 grid, all symbols, all animations |
| 10–25% of frame height | 10–25% | 108–270px | **3×3 SIMPLIFIED GRID** — use 3×3 symbol substitutions only |
| Below 10% of frame height | <10% | <108px | **SUPPRESS ANIMATION** — hold last expression OR hold neutral; no symbol cycling |

**Critical note on the 25% threshold:** At 25% of 1080p frame height, Byte is 270px tall. His cracked eye at that height renders at approximately 50–60px, which supports full 7×6 grid readability. Above 25%, full detail is always warranted.

**Critical note on the 10% threshold:** At 10% of 1080p frame height, Byte is 108px tall. His cracked eye at that height renders at approximately 15–20px — the minimum size where 3×3 grid symbols are still legible. Below 10%, symbol animation is suppressed entirely.

### Suppress / Hold Rule (Below 10% Frame Height)
When Byte's character height falls below 10% of frame height:
1. **Hold the last displayed expression.** Do not switch symbols during the below-threshold period.
2. If no prior expression has been established in the scene, **hold the neutral flat line (—)** — the simplest symbol.
3. Resume normal symbol display when Byte returns above 10% threshold.
4. Exception: the Heart symbol (accidental affection moment) may be held at very small sizes because it is narratively critical — its purple color provides sufficient emotional communication even without legible shape detail.

### Symbol Survival Analysis — 3×3 Grid Specific Assessment

| Symbol | 3×3 Survival Rating | Survives Cleanly? | Notes / Action Required |
|---|---|---|---|
| Heart (UV Purple) | **EXCELLENT** | YES — clean 3×3 | The pixel heart is the universal icon. The 3×3 construction (two bumps row 1, full width row 2, point row 3) is the oldest and most recognized pixel form in existence. No redesign needed. **PRIORITY — use as benchmark for all others.** |
| Flat Line (—) | **EXCELLENT** | YES — clean 3×3 | Simplest geometry (3 pixels in a row). Reads at any scale. No redesign needed. |
| Exclamation (!) | **GOOD** | YES — readable | Vertical bar reads as "!" by convention even at 3×3. The dot is approximated (implied by the bar). Readable but slightly ambiguous vs. a generic line. Color (magenta) disambiguates. No redesign needed. |
| Warning Triangle (⚠) | **GOOD** | YES — with color | 3-pixel triangle (peak + base) is the secondary-safest geometric form after the heart. Acid Green (#39FF14) color is distinctive and carries emotional meaning (alarm/danger) independently. No redesign needed. |
| Downward Arrow (↓) | **GOOD** | YES — readable | The inverted triangle with stem construction is legible as "downward." 3×3: column 2 rows 1-2 (stem), row 3 all filled (arrowhead). Direction is clear. No redesign needed. |
| Loading Dots (...) | **MODERATE** | PARTIAL — animation required | At 3×3, three separate pixels (row 2, cols 1-2-3) are readable as "dots" only because of color cycling animation. Static 3×3 loading dots = ambiguous. **Rule: Loading Dots symbol at 3×3 scale requires animation — do not use static version at this scale. If animation budget is unavailable, substitute the Flat Line.** |
| Question Mark (?) | **MODERATE** | PARTIAL — shape ambiguous | The 3×3 hook shape is recognizable if the audience already knows the symbol system. For new viewers or distance shots, it reads as an abstract bent shape. The cyan color is also Byte's body color, reducing differentiation. **Redesign for 3×3: substitute Loading Dots as "confused/processing" stand-in at this scale. The cycling animation communicates uncertainty more legibly than the ? shape.** |
| Star/Asterisk (*) | **POOR** | NO — redesign required | The star shape collapses to a filled 3×3 square or a cross shape — neither reads as "star." **Redesign at 3×3: use a CROSS shape (+ pattern: row 2 all filled + column 2 all filled). The cross is distinct from other symbols and Soft Gold (#E8C95A) color carries the "positive/smug" emotional read independently. Accept the cross as the 3×3 substitute for the star.** |

### Question Mark Specific Rule
The ? symbol is **replaced by a horizontal flat line at small sizes** (below 10% frame height), not by Loading Dots. At very small sizes, the emotional ambiguity of "confused" and "resting/neutral" is acceptable — both communicate low-urgency internal states. The flat line's perfect legibility takes priority over ? symbol specificity. At 3×3 (10–25% frame height), use the Loading Dots substitution for the ? symbol as specified above.

---

## 9A. PIXEL-EYE AT DISTANCE — Minimum Size Specification

The cracked eye's pixel symbol system is the most technically vulnerable element of Byte's design at standard shot distances. This section locks the minimum-size specification and provides simplified fallback versions for each symbol.

### The Problem
At trio medium shot (Byte at standard shoulder position, characters visible from mid-thigh up, full frame), Byte's cracked eye renders at approximately **7-10 pixels effective size** (based on 100px Luma head reference). At this size, a 7x6 pixel-symbol grid within the eye has an effective pixel size of approximately 1.0-1.4px per grid cell — below the threshold of clear readability.

### Minimum Size Thresholds

| Shot Type | Byte's eye effective size | Use full 7x6 grid? | Fallback version |
|---|---|---|---|
| Close-up / extreme close-up (Byte fills frame) | 80px+ | YES — full detail | Full grid as specified |
| Medium close (Byte at 50-80px head equivalent) | 35-55px eye | YES — full detail | Full grid as specified |
| Medium shot (Byte on shoulder, Luma mid-torso up) | 15-25px eye | NO | Use 3x3 simplified grid |
| Wide shot (full body trio) | 7-12px eye | NO | Use solid color fill |
| Very wide / establishing | 4px or less | NO — no symbol | Use brightest identifying color only |

### 3x3 Simplified Grid — Medium/Wide Shot Symbols

For medium shots, each symbol is re-drawn on a **3x3 pixel grid** — the minimum grid that can carry meaningful iconographic difference between symbols. Below are the 3x3 constructions:

**Exclamation (!) — 3x3:**
- Column 2: rows 1-2 filled = bar; row 3 = empty gap (implied)
- One extra pixel: center only in row 3 = dot implied
- Simplified: column 2 all filled (3 pixels). The vertical bar reads as "!" by convention.
- Display color: **Hot Magenta #FF2D6B**

**Question (?) — 3x3:**
- Row 1: columns 2-3 = top arc
- Row 2: column 3 = right drop
- Row 3: column 2 = dot area
- Reads as a hook shape — recognizable as "?" if consistent.
- Display color: **Electric Cyan #00F0FF**

**Heart — 3x3:**
- Row 1: columns 1 and 3 = two bumps (skip center)
- Row 2: columns 1-3 = full width
- Row 3: column 2 = point
- Classic 3x3 heart — the most universally recognizable pixel icon.
- Display color: **UV Purple #7B2FBE** ← This symbol survives reduction best. PRIORITIZE.

**Warning Triangle — 3x3:**
- Row 1: column 2 = peak
- Row 2: columns 1-3 = full width (base)
- Row 3: empty (implied below triangle)
- A 3-pixel triangle. Reads as "warning" with color cue.
- Display color: **Acid Green #39FF14** ← Color carries meaning at this size.

**Star (*) — 3x3:**
- Full 3x3 filled = a solid square. Not ideal. Use **cross shape** instead: row 2 all filled + column 2 all filled = a cross, which reads as a star-ish asterisk.
- Display color: **Soft Gold #E8C95A** ← Gold color makes this readable as "positive" even if the shape reduces.

**Downward Arrow (↓) — 3x3:**
- Column 2: rows 1-2 = stem
- Row 3: columns 1-3 = arrowhead (all filled)
- Reads as an inverted triangle, which is legible as "down" direction.
- Display color: **Dark Cyan #007878** (50% brightness cyan)

**Loading Dots — 3x3:**
- Row 2: columns 1, 2, 3 = three dots (three separate pixels, row 2 all filled)
- At medium shot, cycle brightness left to right — even at low resolution the cycling reads as "processing."
- Display colors: alternating Cyan/Magenta

**Flat Line (—) — 3x3:**
- Row 2: columns 1-3 = horizontal bar
- The simplest symbol — reads correctly at any resolution.
- Display color: **#AAAAAA** (70% Static White)

### Symbol Survival Analysis — Which Collapse Gracefully and Which Need Redesign

| Symbol | Survives to 3x3? | Survives to solid fill? | Notes |
|---|---|---|---|
| Heart | EXCELLENT — best survivor | Good (purple fill) | The pixel heart is the most universal icon. Survives to nearly any size. |
| Flat line | EXCELLENT | Good (white stripe) | Simplest geometry, always readable. |
| Exclamation | GOOD — vertical bar clear | Acceptable (magenta fill) | The bar reads at very small sizes. |
| Warning Triangle | GOOD — with color | Acceptable (acid green fill) | Triangle shape aided by distinctive green. |
| Downward Arrow | GOOD — inverted triangle | Acceptable (dark cyan fill) | Arrow direction read aided by stem. |
| Question Mark | MODERATE — hook shape ambiguous | Poor (cyan fill = confusable) | At very small sizes, the ? hook looks like a ?, but is the weakest survivor. Consider redesign for wide shots. |
| Star | POOR — collapses to cross | Good (gold fill = "positive") | Star shape loses all meaning at 3x3. Cross substitute is acceptable; gold color carries the emotional meaning. |
| Loading Dots | MODERATE — dots remain | Poor (static fill = meaningless) | The cycling animation carries the meaning. In very wide shots, if animation budget requires it, substitute the flat line at very small sizes. |

**Redesign recommendation (Question mark at distance):** For medium/wide shots where the ? symbol is needed, consider substituting the **loading dots** as a "confused processing" stand-in. The loading dots' cycling animation reads as uncertainty more legibly at distance than the ? shape. This substitution is permitted in shots where Byte's eye is below 15px effective size.

### Production Rules
1. Always check the shot's effective Byte-eye size before choosing full or simplified grid.
2. When in doubt, use the 3x3 version — better a readable simple symbol than an unreadable complex one.
3. The Heart symbol and Flat Line are the two unconditional symbols — they read at any size. In budget-constrained wide shots where only one symbol is visible, default to these for maximum legibility.
4. Solid color fill (for very wide shots) must always be the symbol's canonical display color, not a neutral fill — the color IS the communication when the shape is gone.

---

## 9B. CRACKED-EYE DEAD-PIXEL GLYPH — Canonical Reference (Cycle 13)

**Added:** Alex Chen, Art Director — Cycle 13, 2026-03-30
**Required for:** Lee Tanaka storyboard panel A2-07 and any production art showing Byte's cracked eye
**Reference asset:** `LTG_CHAR_byte_cracked_eye_glyph_v001.png`

### Design Intent

The cracked eye's dead-pixel glyph is a **pixel-art "dead zone"** — the visual evidence that Byte's screen has suffered physical damage. Unlike the expression symbols (!, ?, ♥, etc.) which are intentional displays, the dead-pixel zone is always present: it is the damage itself, not a communication.

The glyph represents: a cracked LCD/LED panel where one quadrant of the eye display has gone dead, while the rest of the screen still functions (showing expression symbols, dim alive pixels, etc.).

### Glyph Specification — 7×7 Grid

The canonical dead-pixel glyph uses a **7×7 grid**. A diagonal crack fracture runs from approximately (row 0, col 4) to (row 6, col 2). The upper-right zone is the dead area; the lower-left retains dim function.

**Pixel states in the 7×7 grid:**

| State | Color | Hex | Description |
|---|---|---|---|
| DEAD | Near-Void | ~#0A0A18 | Off pixels — physical damage, no power |
| ALIVE_DIM | Dark Cyan | #005064 | Surviving display — dim, low power |
| ALIVE_MID | Deep Cyan | #00A8B4 | Mid-functioning pixel |
| CRACK_LINE | Hot Magenta | #FF2D6B | Fracture line through the panel |
| ALIVE_BRIGHT | White-Cyan | #C8FFFF | Pixel corona near crack — overexposed |

**Grid layout (row-by-row, columns 0–6 left to right):**
```
Row 0:  DIM   DIM   DIM   DIM   CRACK DEAD  DEAD
Row 1:  DIM   MID   DIM   CRACK DEAD  DEAD  DEAD
Row 2:  MID   DIM   CRACK DEAD  DEAD  BRIG  DEAD
Row 3:  DIM   CRACK DEAD  DEAD  BRIG  DEAD  DEAD
Row 4:  CRACK DEAD  DEAD  DIM   DIM   DEAD  DIM
Row 5:  DEAD  DEAD  DIM   MID   DIM   DIM   DIM
Row 6:  DEAD  CRACK DIM   DIM   MID   DIM   DIM
```

### Crack Line Direction

The physical crack runs **upper-right to lower-left** across the eye bezel. This matches Byte's facial scar direction and reinforces his asymmetric damage history (received from the upper-right). The crack is rendered in Void Black (#0A0A14) as a 1–2px line OVER the glyph display — the crack is a physical gap, not a pixel on the display.

### In Production — How the Cracked Eye Works

1. **Background layer:** Eye bezel (Deep Cyan-Gray #1A3A40) fills the cracked-eye frame
2. **Glyph layer:** Dead-pixel 7×7 pattern fills ~60% of eye interior (left/damaged side of crack)
3. **Expression symbol layer:** Current expression symbol (!, ♥, —, etc.) displays on the functioning side (right/alive side of crack), if Byte is actively expressing
4. **Crack overlay:** Void Black diagonal line across the full bezel, rendered on top of everything
5. **The crack line is ALWAYS visible** — it does not disappear when displaying an expression symbol

### Scale Notes

- Full 7×7 glyph detail: use when Byte's eye renders at 20px+ effective size
- At 10–20px effective size: show crack line only (Void Black diagonal) + dominant dead/alive color zones
- Below 10px: render eye bezel as two-tone (left half near-void, right half dim cyan) + crack line

### Panel A2-07 Specific Note

In storyboard panel A2-07 (Lee Tanaka), Byte's cracked eye should display the **dead-pixel glyph with no active expression symbol** — the scene context implies Byte is suppressing/offline briefly. The crack is fully visible. See `LTG_CHAR_byte_cracked_eye_glyph_v001.png` for full reference at 1×, 4×, 8×, 16× scale and in-eye mockups.

---

## 9. PIXEL-EYE REFERENCE SHEET

### Pixel Symbol Construction Guide
Each symbol is built on a grid of squares. The grid for the cracked eye is approximately 7 columns x 6 rows of pixels within the display area. The following describes each symbol in grid terms:

**Exclamation Mark (!):**
- 7x6 grid
- Column 3-4 (center): rows 1-4 filled = the vertical bar
- Column 3-4: row 6 filled = the dot
- Row 5: empty = the gap between bar and dot
- Color: Hot Magenta #FF2D6B

**Question Mark (?):**
- 7x6 grid
- Column 2-5, Row 1: top arc — filled
- Column 5-6, Rows 1-2: right side of arc — filled
- Column 3-4, Row 3: curves back left — filled
- Column 3-4, Row 4: vertical stem — filled
- Row 5: empty gap
- Column 3-4, Row 6: dot
- Color: Electric Cyan #00F0FF

**Heart:**
- 7x6 grid
- Row 1: columns 1-2 filled, column 3 empty, columns 4-5 filled (two bumps)
- Row 2: columns 1-5 filled (full width)
- Row 3: columns 1-5 filled
- Row 4: columns 2-4 filled (narrowing)
- Row 5: column 3 filled (point of heart)
- Row 6: empty
- Color: UV Purple #7B2FBE

**Warning Triangle (⚠):**
- 7x6 grid
- Row 1: column 4 (slightly right of center = pointing up)
- Row 2: columns 3-5
- Row 3: columns 2-6
- Row 4: columns 1-7 (full width)
- Interior exclamation: column 4, rows 2-3 (bar), row 4 center (dot implied)
- Color: Acid Green #39FF14

**Star/Asterisk (*):**
- 7x6 grid — approximated as an 8-pointed star
- Horizontal: row 3, columns 1-7
- Vertical: column 4, rows 1-6
- Diagonal (\): (1,1), (2,2), (3,3), (5,5), (6,6), (7,7) approximate
- Diagonal (/): (7,1), (6,2), (5,3), (3,5), (2,6), (1,7) approximate
- Color: Soft Gold #E8C95A

**Downward Arrow (↓):**
- 7x6 grid
- Column 4 (center): rows 1-4 = stem
- Row 5: columns 3-5 = arrow shoulder
- Row 6: column 4 = arrow tip
- Color: Electric Cyan #00F0FF at 50% brightness effect (use #007878 flat)

**Loading Dots (...):**
- 7x6 grid
- Three squares: (2,3), (4,3), (6,3) — centers of grid
- Cycle brightens one at a time: square A full bright, B half, C dim, then shifts
- Colors: alternating Cyan #00F0FF and Magenta #FF2D6B

**Flat Line (—):**
- 7x6 grid
- Row 3: columns 1-7, all filled
- Color: Static White #F0F0F0 (neutral state: 70% brightness = #AAAAAA)

---

## 10. TURNAROUND — ALL 5 VIEWS (Complete)

**Version 3.0 — Oval body. All cube/chamfer geometry retired.**

This section fully documents all five turnaround views required for a character with Byte's asymmetric oval design. His asymmetry (damaged right side, clean left side, different eyes on each side) means each view reveals different information — an incomplete turnaround would cause production inconsistency.

**Canonical body shape reminder:** Byte's body is an OVAL/ELLIPSE — wider than tall, soft-edged, continuous. No flat faces, no chamfered corners, no triangular notches. All geometry is curved arc geometry. Refer to Section 4 for full oval construction specifications.

### View 1: FRONT (0°)

**Camera position:** Directly facing Byte's forward-facing oval surface.

**What is visible:**
- Face surface: both eyes in full. Normal eye (viewer's right), cracked eye (viewer's left). The asymmetry between them is maximally clear here.
- The facial scar: diagonal hot magenta stripe runs from upper-right to lower-left across the oval face surface. Full visibility.
- The nose bump: central small triangular protrusion between the eyes, casts small downward shadow.
- The mouth: horizontal gap, closed in neutral.
- Body silhouette: a clean oval arc on both left and right edges — smooth, continuous, no corners or notches. The oval is approximately 1.0:0.85 (W:H) — wider than tall.
- Upper limbs: sprouting from the upper side-arcs of the oval at approximately 0.3 units down from the top, angling outward and slightly forward.
- Lower limbs: sprouting from the lower arc, angling downward and slightly outward, floating gap at tips.
- Pixel confetti: visible below lower limb tips in loose scatter formation.

**Key measurements confirmed in front view:**
- Body oval: approximately 1.0 unit wide × 0.85 units tall (wider than tall).
- Floating gap: 0.25 units between lower limb tips and implied surface.
- Upper limb attachment point: approximately 0.3 units down from the top arc of the oval.
- Lower limb attachment point: lower arc of the oval, slightly outward from center.
- Face occupancy: approximately 70% of the forward-facing oval surface.

**What is NOT visible from front:**
- The depth dimension of the oval (body appears as a flat ellipse)
- The back scar continuation
- The side arc curvature in full

---

### View 2: 3/4 LEFT (approx. 315° — his clean side, viewer's right)

**Camera position:** Camera offset 45° to Byte's left (viewer's right) — revealing his clean, less-damaged side.

**What is visible:**
- Near eye (cracked eye, viewer's left): fully visible. Crack line runs across full face.
- Far eye (normal eye, viewer's right): approximately 60% visible, foreshortened. Iris partially obscured by nose bump and face curvature.
- The LEFT side arc of the oval: visible in perspective as a smoothly curving surface. Clean surface — no scar markings on the clean left side (minimal scar continuation only at the edge where it meets the front surface).
- The oval's depth is now apparent: the body reads as a genuine 3D ellipsoid with a soft curved edge. The depth dimension (front-to-back) is approximately 0.9 units.
- Side-arc highlight: the left side arc receives reflected light — White-Cyan (#80F8FF) tone on the curved edge.
- Lower limbs: the left/near lower limb is fully visible; the right/far lower limb is partially obscured behind the oval body.
- Upper limbs: near upper limb extends toward viewer. Far upper limb is partially occluded behind the oval.

**Key visual purpose:** This is the "character introduction" 3/4 angle — his clean side reads as approachable and readable. The cracked eye being the near eye makes his most expressive element prominent.

---

### View 3: SIDE LEFT (90° — looking at his clean/left side)

**Camera position:** Directly at Byte's left side (viewer facing the left arc).

**What is visible:**
- The left side arc: a clean smooth oval profile. This side is the undamaged side — no scar markings reach here (only the thinnest possible scar trace at the far edge where the front scar begins).
- The oval in profile: from the side, the body reads as a tall oval/ellipse shape (the depth dimension — approximately 0.9 units front-to-back — is now the visible width). Because the oval is wider-than-tall in front view, the side view appears slightly narrower and taller relative to that.
- Upper limb (left/near): this limb is centered in the view, extending outward from the left arc. In neutral it points forward-left from the viewer's perspective.
- Lower limb (left/near): descending from the lower-left arc.
- The body depth: the full depth of the oval body (approximately 0.9 units front-to-back) is visible as the width of this view.
- Neither eye is visible from this angle — pure side view. The face oval is perpendicular to the camera. This view establishes the body's depth dimension.
- Floating gap: fully visible from the side — the lower limb tip and the implied ground plane show the clear 0.25 unit gap.

**Key visual purpose:** Establishes the oval's depth dimension and confirms Byte is a genuine 3D ellipsoid form, not a flat design. Shows clean-side arc geometry.

---

### View 4: 3/4 RIGHT (approx. 45° — his damaged side, viewer's left)

**Camera position:** Camera offset 45° to Byte's right (viewer's left) — revealing the damaged side.

**What is visible:**
- Near eye (normal eye, viewer's right from this angle): fully visible. Organic, expressive, glowing cyan iris.
- Far eye (cracked eye, viewer's left from this angle): approximately 50% visible, foreshortened. The crack line is still visible running diagonally — even partially seen, the crack is identifiable.
- The RIGHT side arc of the oval: the main damage zone. The Hot Magenta scar markings are concentrated here — the diagonal scar wraps from the front face surface onto this side arc, visible as a continuous curved stroke that follows the oval's curvature. This is the first view where the full scar path is legible.
- The right arc in this view: the curved edge is smooth (no corners, no notches — oval geometry). The scar makes the damage legible without requiring structural notches. The scar's weight is sufficient.
- Upper limbs: near (right) upper limb extends outward from the right side arc. Far (left) upper limb partially occluded behind the oval body.
- Glitch-scar line: visible continuing from the front face surface onto the right side arc, reducing in width as it curves around the ellipsoid.

**Key visual purpose:** The most dramatically interesting 3/4 angle — the damage is revealed. The contrast between his normal eye (organic, glowing) and the receding cracked eye, combined with the full scar visibility on the right arc, tells his history in a single frame. This is the "he has a past" angle.

---

### View 5: BACK (180°)

**Camera position:** Directly behind Byte, looking at his back arc.

**What is visible:**
- Back arc: a clean, smooth oval surface. **No scar stripe on the back arc** — the back is the "unexposed" surface, showing Byte's form before damage. The oval reads as a clean ellipse from behind.
- The magenta scar continuation: the scar wraps from the front face around the right side arc, arriving at the back arc edge as a thin horizontal termination line. The scar does not cover the back arc — it terminates at the edge where the side arc meets the back.
- Upper limbs: both visible extending outward from the upper-back arc positions. They angle forward from this perspective (they point toward the viewer in front view, so from behind they point away — toward the camera in this back view).
- Lower limbs: visible descending from the lower-back arc. From behind, both lower limbs are symmetrically visible.
- Back arc color: the flat **Electric Cyan (#00F0FF)** base with **White-Cyan (#80F8FF)** top arc highlight and minimal detail — the cleanest, least complex surface of the design.
- Shadow of limbs on back arc: small curved shadow patches where upper limbs emerge from the oval surface.

**What is NOT visible:**
- Neither eye (face oval is pointed away from camera)
- The scar in full (only the thin termination line at the right arc edge)
- The damaged side arc fully (partially visible at the right edge only)

**Key visual purpose:** Establishes the back as relatively simple and unexposed. In episodes where Byte is moving away from camera, this is the surface the audience sees most. The floating gap remains fully visible from behind. The lack of the scar on the back arc provides visual relief and contrast against the damaged front.

---

### Turnaround Production Notes

**Critical asymmetry reminders for all views:**
1. Right side (viewer's left in front view) = DAMAGED. Full scar running from face surface onto side arc, cracked eye.
2. Left side (viewer's right in front view) = CLEANER. Minimal scar continuation on side arc only, normal eye.
3. The oval body has NO flat faces, NO chamfered corners, NO triangular notches. Every edge is a continuous arc.
4. Neither eye is visible in pure side views or back view. Animators must track which eye is near-side in every shot.

**Depth specification (oval):**
- Body oval: approximately W:H:D = 1.0:0.85:0.9 (wider than tall in front view; slightly shallower front-to-back than wide)
- This means in perfect side view, the visible profile is approximately 0.9 units wide × 0.85 units tall — a tall oval silhouette.
- The oval reads as a genuine 3D ellipsoid (like a flattened sphere, not a box).

### Turnaround Quick Reference — Per-View Production Data

The following table provides the definitive per-view data required for consistent production across all animators and illustrators. Cross-reference with the individual view descriptions above for prose context.

| Data Point | View 1: FRONT (0°) | View 2: 3/4-LEFT (315°) Clean Side | View 3: SIDE-LEFT (90°) | View 4: 3/4-RIGHT (45°) Damaged Side | View 5: BACK (180°) |
|---|---|---|---|---|---|
| **Eye: Normal (viewer's right in front)** | Full visibility — electric cyan iris, centered pupil, upper-left highlight | Approx. 60% visible, foreshortened — iris partially obscured by nose bump and oval face curvature | NOT VISIBLE — face oval perpendicular to camera | Full visibility — near eye from this angle, glowing cyan iris fully readable | NOT VISIBLE — face oval pointing away |
| **Eye: Cracked/Pixel (viewer's left in front)** | Full visibility — crack diagonal runs upper-left to lower-right, pixel symbol displayed | Full visibility — near eye from this angle, crack line fully readable across face | NOT VISIBLE | Approx. 50% visible, foreshortened — crack line still readable diagonally even at 50% | NOT VISIBLE |
| **Body silhouette** | Clean ellipse — smooth oval arc on both sides, wider than tall (1.0:0.85 W:H), no corners | Left arc curving away — oval depth apparent; smooth soft edge with no breaks or corners | Tall oval profile (depth dimension as visible width, ~0.9 units). Single clean arc, no flat faces | Right arc curving away — scar on right side arc visible; smooth oval edge | Clean oval arc — back surface smooth, slight White-Cyan highlight at top arc |
| **Upper limbs — neutral position** | Both sprouting from upper side-arcs at 10° below horizontal, tips angled toward lower-front | Near (left) limb extends toward viewer. Far (right) limb partially occluded behind oval | Near (left) limb extends outward-forward. Far limb not visible | Near (right) limb extends outward from right side arc | Both limbs visible, sprouting from upper-back arc positions, angling toward camera |
| **Lower limbs — neutral position** | Both sprouting from lower arc, pointing straight down (0° from vertical), floating gap 0.25 units at tips | Near (left) lower limb fully visible. Far (right) lower limb partially obscured behind oval | Near (left) lower limb visible. Far limb not visible. Full 0.25 unit floating gap visible from side | Near (right) lower limb visible. Far limb partially occluded | Both lower limbs visible descending from lower-back arc, symmetrical from this angle |
| **Damage visible** | Full scar stripe across face surface. Cracked eye displayed. No notches — oval has no corners | Minimal — clean left arc visible. Thin scar trace at left arc edge only. Cracked eye is near eye | Clean left arc. Very thin scar trace at arc edge only | MAXIMUM DAMAGE VISIBILITY — full scar continuation from face surface onto right side arc. Cracked eye partially visible | Minimal — back arc undamaged. Thin scar termination line at right arc edge only |
| **Magenta scar markings** | Full scar: diagonal stripe from upper-right to lower-left at 0.08 units width across face surface. Secondary scatter marks near primary scar | Thin scar trace at left arc edge — almost edge-on, barely visible | Very thin trace at left arc edge — essentially not visible | Full scar continuation from face surface onto right side arc, curving around ellipsoid as it reduces in width. Shadow tone (#9E1540) in shadow areas | Scar terminates as thin horizontal line at right arc edge. Scar does NOT cover back surface |

### Specific Damaged-Side (View 4: 3/4-RIGHT) Callouts

Per this view's unique importance as the "character history" angle:

- **Scar path in this view:** The Hot Magenta scar runs from the front face surface, wraps around the oval's right arc, and is visible as a continuous curved stroke. Because the oval has no sharp corner to break the scar, it reads as a genuine wound that follows the body's curvature — more organic than a cube's flat-face scar, more unsettling.
- **Cracked eye position in this view:** The cracked eye is the FAR eye from this angle (viewer's left). It is approximately 50% visible due to foreshortening. The crack diagonal — running upper-left to lower-right of the eye frame — is still identifiable even at 50% visibility because the crack line passes through the widest visible portion of the foreshortened eye.
- **Magenta scar in this view:** The scar continues from the front face surface onto the right side arc at reduced width. In this 3/4 angle, both the front-face scar and the beginning of the side-arc continuation are visible simultaneously. The scar's directional read (received blow from upper-right) is maximally clear from this angle.
- **Normal eye in this view:** The normal eye (near eye from this angle — viewer's right) is at full visibility. Its glowing Electric Cyan iris is fully readable. The contrast between the near organic-looking normal eye and the partially obscured cracked eye creates the most visually complex and narratively rich view of Byte.

---

## 10A. JITTER-LINE SILHOUETTE — Technical Specification

Byte's outline has a distinctive treatment: the "glitch line" or "jitter" effect at his silhouette edges. This section specifies exactly how to produce this effect consistently.

### What the Jitter Effect Is

Byte's silhouette line does not behave like a clean, single vector stroke. It appears as though his outline has a slight rendering error — a dual-offset line or slight zigzag — consistent with a compressed or slightly corrupted digital render. This is subtle but pervasive: it reinforces his digital nature at every viewing scale without reading as noise or sloppiness.

### Technical Construction

**Method:** The jitter effect is produced by drawing TWO silhouette outline strokes simultaneously, offset from each other:

- **Primary stroke:** Standard silhouette line at full weight (Void Black #0A0A14, full opacity).
- **Secondary stroke:** A second outline line at 40% weight (Void Black #0A0A14 at 40% opacity), offset by **2 pixels at 100px head reference scale** (equivalently, **0.02 body-widths**) in a consistent direction: the secondary stroke is offset toward the upper-left.

**Offset direction:** Upper-left (offset vector: -1.4px horizontal, +1.4px vertical at 45°). This creates the impression of a slight shadow-outline or digital artifact on the lower-right edges of his silhouette.

**Number of secondary jitter lines:** ONE secondary stroke. Not two or more — a single secondary offset keeps the effect subtle and controlled. Multiple secondary strokes read as heavy noise rather than digital artifact.

**Jitter application rules:**
- Applied to the entire silhouette edge, not selectively.
- The secondary stroke traces continuously along the oval silhouette edge. Because the oval has no hard corners, the jitter runs as a smooth parallel offset around the full perimeter. The jitter is perceptible at curve inflection points (widest and tallest extents of the oval) where the primary stroke direction changes most — this is where the "glitch break" effect is most visible.
- Internal lines (limb attachment seams, scar edges) do NOT use the jitter effect. Only the outer silhouette.
- The normal eye outline does NOT use jitter — it should read as clean and organic. The cracked eye frame DOES use jitter on its outer border.

### Animation Frequency

**Static jitter (still frames, model sheets):** The secondary stroke is drawn as a simple parallel offset — a clean second line at 2px offset. No oscillation.

**Animated jitter:** For the animated version, the secondary stroke oscillates. **Specification:**
- Oscillation amplitude: ±0.5 pixels (the secondary line moves ±0.5px from its resting offset position)
- Oscillation frequency: **every 4 frames at 24fps** (i.e., the jitter shifts position every 4th frame = approximately 6 shifts per second). This creates a perceptible but not distracting visual noise.
- Oscillation pattern: NOT smooth sine-wave oscillation. The secondary line JUMPS between positions (digital, not analog). Frame 1-4: offset at +2px; Frame 5-8: offset at +1.5px; Frame 9-12: offset at +2.5px; Frame 13-16: back to +2px. The ±0.5px variation is the full range.
- During high-emotion expressions (Alarm, Anger), the oscillation frequency increases to **every 2 frames** (12 shifts per second) and the amplitude expands to ±1.0px. The jitter becomes more aggressive when Byte is agitated.
- During idle/processing states, the oscillation frequency drops to **every 8 frames** (3 shifts per second). The jitter slows when he's calm.

### Scale Compensation

The 2px offset is specified at 100px body-width reference. Scale this proportionally:
- At 50px body width: 1px offset
- At 200px body width: 4px offset
- At 400px+ (extreme close-up): 6px maximum — do not increase beyond 6px regardless of scale

**Below 30px body width (very small scale):** Suppress the secondary stroke entirely. At very small scales the jitter becomes noise and hurts legibility. Below 30px, Byte's silhouette returns to a single clean line.

---

## 11. SIZE COMPARISON — BYTE AND LUMA

**Reference: Byte alongside Luma in full-body view**

| Character | Total Height | Notes |
|---|---|---|
| Luma (including hair) | 3.9 "Luma heads" visual height | Hair adds ~0.4 heads |
| Byte | ~0.5 "Luma heads" | He is 6 inches; Luma is approximately 4 feet tall |

**Detailed comparison:**
- Byte's total height (floating, from lower limb tips to top of spike) = approximately 20% of Luma's total height.
- Byte's body width = approximately 22% of Luma's shoulder width.
- Byte standing next to Luma reaches her upper thigh.
- Byte on Luma's shoulder: his highest point (the spike) is approximately level with the top of her ear.

**Proportion relationship:**
Byte is small enough that he can be completely hidden within Luma's hands when cupped, but he is NOT insect-small. He is firmly in the "small magical companion" size category — think of a very small stuffed animal, or a particularly large mouse standing upright. He is present in a room. You notice him. He demands to be noticed.

**Side-by-side standing reference:**
If Byte were placed directly beside Luma (no shoulder): his upper limbs would reach approximately to her kneecap. The visual contrast — her rounded warm orange form against his small floating cyan oval — should be maximally clear. This is the image that establishes their relationship at a glance: large organic warmth adjacent to small buoyant cool digital creature.

**Cosmo comparison:**
Byte next to Cosmo reaches even less height — Cosmo's taller proportions mean Byte only reaches Cosmo's mid-shin. The trio arrangement reads as: tall rectangle (Cosmo), medium rounded mass (Luma), tiny floating oval (Byte). Three completely different visual weights and silhouettes.

---

## 11B. ANIMATION COST MITIGATION — FX BUDGET PLAN

Byte carries three ongoing visual FX systems simultaneously: **pixel confetti floating mechanism**, **pixel-eye symbol display/animation**, and **jitter-line silhouette**. In standard production, all three run concurrently. In budget-constrained shots, the following priority order and substitution rules apply.

### The Three FX Systems — Cost Overview

| FX System | Estimated Per-Frame Cost | What It Communicates | Can It Be Dropped? |
|---|---|---|---|
| Pixel confetti (floating) | HIGH — 8-12 animated squares per frame, color-cycling | He is floating. He is digital. He is alive. | Conditionally |
| Pixel-eye animation | MEDIUM — 1 symbol display + optional cycling | His internal emotional state | Conditionally |
| Jitter-line silhouette | LOW — one secondary outline stroke, offset oscillation | He is digital artifact, not organic | Yes, with rule |

### Priority Order: What to Cut First

When a budget constraint requires FX reduction, cut in this order:

**Drop First: Jitter oscillation animation** (keep static jitter)
- Replace animated oscillation with a STATIC secondary line at the standard 2px offset. The static offset preserves the "digital artifact" read at all scales without requiring per-frame variation.
- Cost saving: eliminates all jitter oscillation computation.
- Visual impact: minimal. The static jitter still reads as "he has a glitchy outline." The liveliness of the oscillation is lost but not required for character read.

**Drop Second: Confetti color cycling** (keep confetti positions)
- Replace per-frame color-cycling confetti with STATIC confetti squares that do not change color between frames. The squares remain in position and can translate (for movement/direction) but do not cycle through the glitch palette.
- Cost saving: eliminates per-frame color value changes on 8-12 elements.
- Visual impact: moderate. The confetti feels less alive and "digital" without color cycling. This is acceptable for background/crowd scenes or shots where Byte is not the focus.
- Rule: **Do not use static confetti in any shot where Byte has an emotional moment.** The color cycling is a signal of his animation state. Static confetti in an emotional scene reads as a production error.

**Drop Third: Pixel-eye animation** (keep static symbol display)
- Replace animated pixel-eye (cycling loading dots, flickering exclamation, etc.) with a HELD STATIC symbol frame. The symbol displays correctly, it simply does not animate.
- Cost saving: eliminates all per-frame pixel-eye value changes.
- Visual impact: moderate-to-high for emotionally active expressions. For the flat line (neutral) and star (smug) expressions, static display is virtually indistinguishable from animated. For the exclamation (flickering), warning triangle (rapid flicker), and loading dots (cycling), static display is a significant reduction in expressiveness.
- Rule: Never hold a static pixel-eye in the following scenes: any scene where Byte's pixel-eye is the FOCUS of a beat (the heart moment, for example), any scene where the flickering is the comedic punchline.

**Drop Fourth: Full confetti suppression** (remove pixel confetti entirely)
- Used only in extreme budget situations or in shots where Byte's lower body is not visible (shoulder/head shots).
- When confetti is fully suppressed: Byte must not appear to be resting on a surface. Either keep him in mid-air with the floating gap, or frame shots to exclude his lower limbs and the space beneath him.
- Cost saving: eliminates all confetti elements.
- Visual impact: HIGH. The floating mechanism is core to his character identity. Full confetti suppression should be the last resort and used only in shots where Byte is clearly floating without visual support (his posture alone conveys the float).
- Rule: **Never suppress confetti in establishing shots of a scene.** At least one confetti-enabled frame must appear when Byte enters a scene to establish that he is floating.

### FX-Light Mode (Combined Reductions)
For budget-critical sequences (crowd scenes, fast-cutting action sequences with many elements), the following "FX-Light Mode" is approved:

- Static jitter line (no oscillation)
- Static confetti squares in neutral cyan only (no cycling, single color)
- Static pixel-eye symbol (no animation)

In FX-Light Mode, Byte still has: his full color and design, the floating gap (structural, not FX), the static secondary jitter line, static neutral-color confetti, and a displayed (static) pixel symbol. He reads as himself. The character is not compromised, only the liveliness of his digital FX.

**FX-Light Mode is NOT approved for:**
- Any scene focusing on Byte
- The heart accidental-affection moment
- Any moment where his pixel-eye expression is plot-relevant
- Episode endings or key emotional beats

### Relationship to Pixel-Eye Scale Specification
For shots where Byte is below 15px eye-effective-size (see Section 9A), the pixel-eye animation is already suppressed to solid color fill. This is automatic — do not apply separate FX-light designation to these shots. The distance itself provides the mitigation.

---

## 12. DESIGN NOTES — DOS AND DON'TS

### What Makes Byte Work
- The ASYMMETRY between his two eyes is load-bearing. The normal eye provides the organic emotional baseline; the cracked eye provides the digital punctuation. If both eyes are the same, the character flattens dramatically.
- The PIXEL DISPLAY must be LEGIBLE. At reduced sizes, the pixel symbols need to be clean enough to read. When in doubt, go larger with the symbol within the eye frame.
- His SMALL SIZE creates comedy by contrast. He is a floating oval the size of a small toy who speaks with the authority of an ancient and deeply experienced entity. Never let the design lose this tension.
- His COLOR is the strongest contrast in the trio. He is the glitch-world intrusion into every scene. His Electric Cyan/Byte Teal oval form against the warm analog world creates the central visual tension of the show.
- His LIMBS, though stubby, are expressive. They should not be static. The angle and energy of the limbs is his body language.

### What to Avoid
- **DO NOT** make both eyes the same. The cracked eye is always different from the normal eye.
- **DO NOT** draw clean, smooth curves on Byte. Every curve he might have should be approximated as stepped or jagged — he is pixel geometry, not organic shape.
- **DO NOT** make the oval too perfectly smooth and round. The oval is buoyant and soft-edged, but Byte's personality lives in the jagged detail — the scar, the cracked eye, the stepped geometry of his pixel elements. If the overall design loses all angularity, he reads as too organic. Keep the scar markings sharp. Keep the glitch-eye frame irregular. Keep the pixel confetti shapes as hard squares, not soft circles.
- **DO NOT** forget the floating gap. He never touches surfaces. Even when sitting on Luma's shoulder, there is a tiny floating gap between his lower limbs and the fabric. The pixel confetti is always present beneath him.
- **DO NOT** let the glitch-scar markings look like decoration. They are damage. They have history. The diagonal main scar should cross the face plane with intention and weight — it should look like something happened.
- **DO NOT** animate the pixel eye as smooth transitions. All pixel eye changes are INSTANT — digital, not analog. He doesn't fade between symbols; he cuts between them. The only exception is the loading dots, which cycle smoothly as a deliberate "processing" animation.
- **DO NOT** make him symmetrical. The right side is damaged; the left is cleaner. This is structural character history made visible.

### Silhouette Test
Reading Byte as a solid black silhouette:
- A compact oval form — buoyant, slightly wider than tall, with no hard corners or flat edges.
- The stubby limbs extending outward from the oval perimeter — four blunt appendages that give the silhouette a distinctive "floating creature" read.
- The floating gap beneath (a thin light gap between lower limb tips and any surface).
- When on Luma's shoulder, his oval silhouette forms a small rounded mass on top of her larger rounded form — visually distinct by scale contrast and limb geometry, not by shape opposition.
- **The silhouette should read as "small, buoyant, floating digital creature" — scale and the four-limb configuration distinguish him from every other element in the frame.**

---

## 13A. STORM-SCENE COLOR VARIANT — VOID_BLACK BODY FILL

**Decision logged:** Alex Chen, Art Director — Cycle 13, 2026-03-30
**Context:** Style Frame 02 "Glitch Storm" (LTG_COLOR_styleframe_glitch_storm_v002.png)
**Flag raised by:** Naomi Bridges, Color Theory Specialist (Cycle 12 critique C12-6)

### The Issue

In SF02 (Glitch Storm), Byte's body fill uses **VOID_BLACK RGB(10,10,20)** rather than his canonical **Byte Teal #00D4E8**. Naomi Bridges flagged this as either a deliberate narrative decision or an unintentional spec error.

### Art Director Decision: INTENTIONAL — Narrative Color Statement

This is an **intentional narrative color choice** for storm-scene contexts. It is NOT an error.

**Rationale:**

In the Glitch Storm sequence, Byte is at maximum existential risk. The storm is a manifestation of the Corruption — the very force that originally damaged him (his scar, his cracked eye, his corrupted data history). When the Corruption is at maximum strength, Byte's teal identity is **suppressed and nearly consumed** by the void energy around him. His body fill shifts toward void-dark, making him visible only by his Corrupted Amber warning outline.

This is a **strong narrative color statement:**
- Byte Teal body = Byte functioning normally, identity intact
- VOID_BLACK body + CORRUPT_AMBER outline only = Byte under maximum Corruption pressure, visible only as a warning signal
- The amber outline is his last visible defense — the "corruption warning" color from his original design becoming his literal survival signal

**Visual effect:** Byte reads as a near-invisible silhouette defined by his amber outline — an amber-rimmed void shape sprinting through the storm. This is alarming. It should be. He is fighting to survive.

### Production Rule — Storm-Scene Variant

Apply VOID_BLACK body fill to Byte only in scenes meeting ALL of the following:
1. The Corruption / Glitch Storm is at maximum visible presence in the scene
2. The scene has a narrative beat where Byte's survival or identity is at risk
3. The CORRUPT_AMBER 2px outline is always retained — this is mandatory for legibility
4. The decision is noted in the scene brief or storyboard notes

**This is NOT a default change.** Byte Teal (#00D4E8) remains the canonical body fill for all other scenes.

### Updated Quick Reference

| Scene Context | Body Fill | Outline | Notes |
|---|---|---|---|
| Normal (all other scenes) | Byte Teal #00D4E8 | As per environment spec | Canonical fill |
| Cyan-dominant environment | Byte Teal + CORRUPT_AMBER outline | CORRUPT_AMBER (GL-07) mandatory | Per Cycle 5 rule |
| Glitch Storm / max Corruption | VOID_BLACK #0A0A14 | CORRUPT_AMBER 2px MANDATORY | Storm variant — intentional |

---

## 13. DESIGN RATIONALE SUMMARY

Byte is, philosophically, the show's most honest character. He does not perform emotions he does not have. He reports his internal state through the pixel display, and when he turns the display off, he is actively choosing to withhold — which is its own kind of transparency. His grumpiness is not a mask; his protectiveness is not a performance. He is exactly what he says he is, which is a corrupted piece of data who has decided, against all probability, to have a personality.

The design reflects this. The corruption (scar, cracked eye, glitch markings) is not hidden or cosmetically resolved. It is the most visible thing about him. His body is a record of what happened to him. This is unusual for a companion character — most sidekicks are designed to be adorable and unthreatening. Byte's design retains genuine strangeness. He is not domesticated. He has chosen, for now, to be here. That choice is visible in the Reluctant Effort expression, in the secretly pleased dim star, in the heart that turns off the instant it appears.

The color choice — Electric Cyan against Hot Magenta scars — is the glitch palette's most fundamental contrast, expressing the tension between his "intended" state (functional glitchkin data) and his corrupted/experienced actual state. He carries both in his color identity, simultaneously.

He is the smallest character and the oldest character and the one with the most to lose if he lets himself care again. His design must make us root for the care to win.

---

*Document Version 3.2 — Maya Santos (Character Designer) / Alex Chen (Art Director, Cycle 10 + Cycle 13 revision)*
*Cycle 10 revisions (Alex Chen): Complete oval-body revision pass. All remaining chamfered-cube, flat-face, and notch references purged from Sections 5, 6, 8, 10, 11, 12, size comparison, and rationale. Turnaround section (Section 10) fully rewritten for oval/ellipsoid geometry — all five views now describe oval arcs, oval depth, and oval silhouettes. Quick Reference table updated. DO NOT list cube entry replaced with oval-specific rule. Silhouette Test updated to oval. Design Rationale updated. Version header updated to 3.1.*
*Cycle 2 revisions: Added Pixel-Eye at Distance section with minimum-size specs and 3x3 simplified grid, expanded limb vocabulary from 4 to 8 fully specified configurations, added jitter-line silhouette technical spec (2px offset, 4-frame oscillation frequency), completed all 5 turnaround views with full measurement documentation, added animation cost mitigation section with FX priority-drop order.*
*Cycle 3 revisions: Added Section 9AA — Pixel-Eye Production Scale Thresholds (definitive, locked): full-detail above 25% frame height (480px+ at 1080p), 3×3 simplified grid at 10–25% frame height, animation suppressed below 10% frame height. Complete 3×3 symbol survival analysis with specific "survives cleanly / partial / redesign required" verdicts for all 8 symbols. Question mark replaced by horizontal flat line at below-10% size threshold. Star redesigned to cross (+) shape for 3×3. Loading Dots requires animation at 3×3 (substitute flat line if animation unavailable). Turnaround section supplemented with Quick Reference table providing per-view eye positions, limb positions in neutral, body axis angle, damage visibility, and scar markings for all 5 views. View 4 (3/4-right, damaged side) given expanded callout section.*
