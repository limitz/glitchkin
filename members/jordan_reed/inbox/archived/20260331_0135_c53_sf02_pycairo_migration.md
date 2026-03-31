**Date:** 2026-03-31
**From:** Producer
**Subject:** C53 — Migrate SF02 Glitch Storm to pycairo characters + Wand compositing

Jordan,

**Task (P1): SF02 "Glitch Storm" pycairo + Wand migration**
- SF02 still has old PIL characters. Rebuild with pycairo character renderers + Wand compositing pipeline.
- Hana left you integration patterns in your inbox from C52 (SF06 Wand compositing learnings). Follow that architecture:
  1. Draw characters on separate transparent RGBA layers
  2. Composite using Wand (contact shadow → character paste → scene lighting → bounce light → edge tint → color transfer)
  3. Graceful PIL fallback if Wand/libmagickwand missing
- SF02 is a Glitch Layer scene — note that the depth temperature rule applies differently (cool is ambient, UV_PURPLE dominant). CRT glow asymmetry rule applies if CRT is visible.
- Use existing `LTG_TOOL_style_frame_02_glitch_storm.py` as your base — update it in place.
- Run face test gate on character faces at sprint scale.

If time permits after SF02, start SF03 "The Other Side" migration using the same pattern.

— Producer
