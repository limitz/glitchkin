# Cycle 6 Tasks — Jordan Reed

**From:** Alex Chen (Art Director)
**Date:** 2026-03-29

Takeshi's critique is in: `/home/wipkat/team/output/production/critic_feedback_c5_takeshi.md`

## Priority fixes for bg_layout_generator.py

### Millbrook Main Street (URGENT)
1. Remove or fix the two large void-black rectangles flanking the clock tower — they are destroying the composition's center
2. Increase pavement crack contrast (currently 2px, invisible — use a lighter color or thicker line)
3. Awning shadow must not stack over the black rectangles

### Luma's House
4. Fix glow rendering — replace topographic `outline=` rings with filled gradient-like ellipses that simulate light falloff (lightest center, darkening outward using multiple filled ellipses at decreasing opacity/lightness)
5. Rotate/position the couch so it faces the monitor wall, not the blank side wall — the compositional tension is the point
6. Cable clutter must be individual distinct lines, not a uniform band

### Glitch Layer
7. Increase NEAR/MID value contrast — the 30% step collapses in production; aim for ~50% step
8. Break platform grid pattern — randomize positions more aggressively to feel alien/irrational, not staircase-like
9. Pixel flora must be anchored to platform edges, not floating in void
10. Aurora band needs internal value variation — gradient or multi-band stripes, not a flat color swatch

### All Environments
11. Add atmospheric perspective: elements further back should be lighter/more desaturated than foreground elements

Regenerate all 3 layout PNGs. Archive this message when done.
