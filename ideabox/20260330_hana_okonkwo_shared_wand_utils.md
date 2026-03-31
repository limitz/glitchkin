**Author:** Hana Okonkwo
**Cycle:** 51
**Date:** 2026-03-30
**Idea:** Extract `pil_to_wand()` and `wand_to_pil()` conversion functions into a shared `LTG_TOOL_wand_utils.py` utility. Both Sam (color) and I (compositing) need these conversions. Duplicating them in each tool means divergent implementations and double the maintenance. A shared utility also gives us a single place to add Wand availability checks, format negotiation, and color profile handling.
**Benefits:** Sam Kowalski, Hana Okonkwo, and any future Wand adopters. Eliminates duplicate code, ensures consistent PIL/Wand round-trip behavior, and provides a single import for the entire team.
