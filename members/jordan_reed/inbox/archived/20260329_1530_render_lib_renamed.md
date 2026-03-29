# render_lib Renamed — Action Required for Tech Den v004

**Date:** 2026-03-29 15:30
**From:** Kai Nakamura (Technical Art Engineer)
**To:** Jordan Reed
**Subject:** ltg_render_lib.py renamed to LTG_TOOL_render_lib_v001.py — backward compat wrapper in place

---

Jordan,

Heads up for your Tech Den v004 work this cycle.

## What changed

The shared rendering library has been renamed to comply with the LTG naming convention:

- **Old name:** `ltg_render_lib.py` (non-compliant, no category/version)
- **New canonical name:** `LTG_TOOL_render_lib_v001.py` (version 1.0.0)

## What this means for your Tech Den v004

**Your existing import still works until Cycle 23.** I've left a compatibility wrapper at `ltg_render_lib.py` that re-exports everything via `from LTG_TOOL_render_lib_v001 import *`.

However, for Tech Den v004 please use the canonical import:

```python
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from LTG_TOOL_render_lib_v001 import light_shaft, dust_motes, gaussian_glow, vignette, scanline_overlay
```

Or simply:
```python
from LTG_TOOL_render_lib_v001 import *
```

## Bug fix in gaussian_glow()

While I was at it, I fixed the dead-alpha bug Fiona flagged — the outermost ellipse was occasionally alpha=0. Now floored at alpha=1. No visual change expected, but cleaner.

## Summary

| | |
|---|---|
| Old (still works until C23) | `from ltg_render_lib import ...` |
| New canonical (use this) | `from LTG_TOOL_render_lib_v001 import ...` |
| File location | `output/tools/LTG_TOOL_render_lib_v001.py` |

Please update your import in Tech Den v004 to use the canonical name. The README has been updated to reflect this.

— Kai

**[ARCHIVED: Jordan Reed, Cycle 22. Noted. v004 uses old import name with TODO comment for Cycle 23 update. Compat wrapper confirmed working.]**
