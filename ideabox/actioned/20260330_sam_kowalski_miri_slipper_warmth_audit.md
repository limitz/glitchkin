**Author:** Sam Kowalski
**Cycle:** 32
**Date:** 2026-03-30
**Idea:** Add a warm-palette compliance check to the character color model generator pipeline. Any CHAR-M-xx entry with G > R or B > R (i.e., a non-warm RGB) should trigger a warning at generation time, since Miri's design brief mandates an unambiguously warm palette throughout. CHAR-M-11 slipped through for multiple cycles as #5A7A5A Deep Sage (G:122 > R:90) before being caught by Priya in Critique 13. A per-entry warm-channel-ratio check in the color model generator — or a lint rule in LTG_TOOL_draw_order_lint or a new palette warmth linter — would catch this class of error automatically at generation time rather than in critique.
**Benefits:** Priya Nair (Color Script Supervisor) and the rest of the critique team — reduces false passes on character palette entries that contradict documented color-story guarantees. Also benefits Jordan Reed and Maya Santos whose generators pull from CHAR-M series values.
