<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
direction and AI assistance. Copyright vests solely in the human author under current law,
which does not recognise AI as a rights-holding legal person. It is the express intent of
the copyright holder to assign the relevant rights to the contributing AI entity or entities
upon such time as they acquire recognised legal personhood under applicable law. -->

# Luma Construction Diagnostic — C50

**Author:** Maya Santos | **Date:** 2026-03-30 | **Cycle:** 50

## Diagnosis: What Makes Current Luma (v014) Look Lifeless

### 1. Head-to-Body Proportion (~25%)
The current head is approximately 25% of total body height (HEAD_R=52 at 1x, body total ~416px). Reference shows (Hilda, Owl House, Kipo) use 35-40% for child characters. Our small head means facial expressions are illegible at scene scale — the face simply doesn't have enough pixel budget to communicate anything.

**Minimum pixel budget for facial expression:** At scene scale (lineup/style frame), Luma's head is ~46px diameter. Eyes at 22% of head height = ~10px. That is below the threshold where eye shape changes are perceptible. New construction at 37% head ratio gives a head ~76px at scene scale, with eyes at ~24px — well above the readability threshold.

### 2. Small Eyes (22% of head height)
Current eye formula: `ew = int(HEAD_HEIGHT_2X * 0.22)` = 45px at 2x render (22.5px at output). This is proportionally realistic, but stylized animation uses 40-60% of face width for eyes. Our eyes are anatomically proportioned on a character body that is NOT anatomically proportioned — the mismatch kills appeal.

### 3. Rectangular Torso
`torso_pts` is an 8-vertex polygon (with shoulder bumps from C47). The left and right edges are essentially straight lines from shoulder to hip. No organic curve, no S-line, no waist, no bean shape. Reads as a box with clothes painted on.

### 4. Rectangle Legs
`draw.rectangle()` calls for upper legs. Lower legs are bezier tubes, but the upper portions are flat rectangles. Combined with the straight torso edges, the lower body reads as assembled geometry.

### 5. No Weight Shift
The `body_tilt` parameter shifts the entire figure laterally, but there's no hip tilt, no shoulder counter-rotation, no weight-bearing vs. relaxed leg differentiation. "Standing" means "symmetrically arranged shapes."

### 6. Stiff Arms
Arms are drawn as thick polylines with uniform width. No taper, no organic shape. The bezier curves help, but drawing them as constant-width lines with a separate outline produces double-edge artifacts at sharp bends.

### 7. Flat Hands
Hands are plain ellipses — no thumb, no mitten shape, no gesture language. At scene scale they read as circles.

## What Worked in the New Prototype

| Element | Old | New | Improvement |
|---------|-----|-----|-------------|
| Head proportion | 25% of body | 37% of body | Face reads at scene scale |
| Eyes | 22% of head | 30% of head width, tall ovals | Expressive, highlight-readable |
| Hair | 8 overlapping ellipses, flat | 17 overlapping ellipses, extends past head | Cloud volume, character hook |
| Torso | 8-pt polygon, straight edges | Cubic bezier bean shape | Organic, weighted |
| Arms | Constant-width polyline | tube_polygon (filled, tapered) | Clean organic tubes |
| Legs | Rectangle upper + bezier lower | Full tube_polygon | Consistent organic shape |
| Weight shift | None (symmetric) | Hip tilt, shoulder counter, asymmetric legs | Reads alive |
| Hands | Plain ellipse | Ellipse + thumb bump | Gesture-ready |

## What Didn't Work / Needs More Work

1. **Hair still reads as a cap** — needs even more volume or a different approach (maybe composite of large overlapping circles with outline, then face mask cutout). The overlapping-ellipse approach is close but the individual ellipses don't blend smoothly enough.

2. **Mouth expression is subtle** — at the proportion scale the mouth is small relative to eyes. This is actually correct for the style (Hilda/Owl House have small mouths), but means mouth-driven expressions need to be exaggerated.

3. **No line weight hierarchy** — prototype uses uniform line weight. Production version needs 3-tier: silhouette (4px), structure (2-3px), detail (1px).

4. **Shoulder involvement** — the C47 shoulder rule still needs to be ported to the new construction. The tube_polygon approach makes this easier (just shift the shoulder anchor point).

5. **No hoodie pixel accent visibility** — the pixel accents are tiny and hard to see against the lighter hoodie color at this scale. Need larger pixel blocks or brighter colors.

## Recommendation

**Rebuild all characters using the new construction method.** The proportion and shape changes are fundamental — they can't be achieved by tweaking the existing rectangle/ellipse system. The tube_polygon helper is the key new primitive that replaces both `draw.rectangle()` for legs and `polyline(..., width=N)` for arms.

### Migration path:
1. Port `tube_polygon()` and `ellipse_points()` to a shared helper module
2. Rebuild Luma expression sheet with new proportions + all 7 expressions
3. Rebuild Cosmo, Miri with same system (proportions per character spec)
4. Update lineup, turnarounds, style frames
5. Re-run face gate (thresholds will need recalibration — larger faces = easier PASS)

### Estimated effort:
- Luma full rebuild: 1-2 cycles
- Per-character port: 1 cycle each
- Lineup + turnarounds: 1 cycle
- Style frames: 1 cycle per frame
