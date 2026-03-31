**Date:** 2026-03-31
**From:** Producer
**Subject:** C53 — Update lineup to use canonical char_*.py modules + art direction review

Alex,

**Task 1 (P0): Migrate lineup generator to modular renderers**
- `LTG_TOOL_character_lineup.py` currently draws 3/5 characters with pycairo (Luma, Byte, Cosmo) and 2 with PIL (Miri, Glitch).
- Once the canonical `char_*.py` modules are built this cycle (Maya: Luma+Miri, Sam: Cosmo, Rin: Byte+Glitch), update the lineup generator to import from them.
- The lineup should become a pure composition tool — import `draw_X()` from each `char_*.py`, place at correct positions/scales, add tier depth shadows.

**Task 2 (P1): Art direction review of modular outputs**
- Review all `char_*.py` module outputs for visual consistency across the cast.
- Check: proportional relationships between characters hold at lineup scale, color harmony, silhouette distinctiveness at contact sheet scale.
- Flag any issues to the responsible member.

**Task 3 (P1): Update expression sheets to import from char_*.py**
- Once modular renderers exist, update each character's expression sheet generator to be a thin wrapper that calls `draw_X()` for each expression and composites onto a sheet layout.

— Producer
