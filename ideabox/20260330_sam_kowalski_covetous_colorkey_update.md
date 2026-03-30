**Author:** Sam Kowalski
**Cycle:** 42
**Date:** 2026-03-30
**Idea:** Update `LTG_TOOL_colorkey_glitch_covetous_gen.py` to reflect the three-character triangulation staging in the COVETOUS spec (Glitch + Byte + Luma). The current color key thumbnail (640×360) shows only Glitch and a warm-bleed threshold, matching the C41 single-character spec. Now that the spec is updated to include Byte and Luma in frame, the color key should be regenerated to show the three-character color arc: Glitch amber-in-void (left) → Byte teal silhouette (center) → Luma warm orange (right). This makes the color key useful as a reference for Diego/Jordan when executing the full style frame.
**Benefits:** Diego Vargas (style frame executor) would have a visual reference matching the actual scene layout. Prevents the executor from using the old single-character color key as a staging guide and producing a single-character style frame. Low effort — existing generator just needs new character zones added.
