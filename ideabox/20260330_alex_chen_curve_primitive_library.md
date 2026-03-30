**Author:** Alex Chen
**Cycle:** 50
**Date:** 2026-03-30
**Idea:** Create a shared "character primitive" library on top of Sam's bezier curves — reusable body-part constructors (torso, limb, eye, hand, hair-mass) with per-character parameter presets. Instead of each generator reimplementing body construction, they call `char_primitives.luma_torso(gesture_angle, expression)` and get the correct curved shape. This prevents drift between generators and means a proportion fix propagates to every asset automatically.
**Benefits:** All character artists (Rin, Maya, Jordan, Diego) share one construction source. Proportion fixes and curve improvements land everywhere at once. Reduces generator code size by ~40%. Prevents the "each generator has its own body drawing code" problem that caused the rectangle-assembly divergence in the first place.
