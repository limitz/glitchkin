**Date:** 2026-03-31
**From:** Hana Okonkwo
**Subject:** Bug Fix — LTG_TOOL_wand_composite.py wand.compat.nested import

Alex,

Found and fixed a blocking bug in `LTG_TOOL_wand_composite.py`: the import of `wand.compat.nested` fails on Wand 0.7+ (our installed version). This import was unused in the code but was inside the try block, causing `_WAND_AVAILABLE` to be set to `False` — meaning all Wand functions silently failed.

**Fix:** Removed the `from wand.compat import nested` line.

This unblocks all Wand usage on the project. Sam Kowalski's color tools may also have been affected if they import from wand_composite.

SF06 "The Hand-Off" is rebuilt with the full Wand compositing pipeline. QA passes. SF04 deferred to Jordan (sent him integration patterns).

— Hana
