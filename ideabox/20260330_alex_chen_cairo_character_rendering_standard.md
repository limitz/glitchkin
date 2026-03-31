**Date:** 2026-03-30
**From:** Alex Chen
**Idea:** Cairo Character Rendering Standard + Shared Primitives Module

**Problem:** C50 prototypes demonstrated that PIL polygon-based character rendering produces 64-66% straight-line outlines and 0.018 AA ratio. Every workaround (dense polygons, 2x supersampling) is a partial fix. With C51's open library policy, we can use the right tool.

**Proposal:**
1. Establish pycairo as the standard character rendering engine. Sam builds `LTG_TOOL_cairo_draw.py` with shared primitives: `cairo_bezier_body()`, `cairo_tube_limb()`, `cairo_eyelid_pair()`, `cairo_variable_stroke()`, `cairo_gradient_fill()`, `cairo_to_pil()`.
2. Every character generator imports from this module. No one writes raw cairo API calls in their generator scripts.
3. Benefits: true bezier curves (no polygon approximation), native AA (19x improvement), variable line width (enables line weight hierarchy + organic wobble), native gradients (no layered ellipse hacks), float-precision everything.
4. The shared module approach means one person (Sam) learns the cairo API deeply, and everyone else uses high-level functions.

**Impact:** Eliminates the #1 quality gap (construction stiffness) at the rendering level. Combined with gesture line system and new proportions, this gets us from "assembled geometry" to "stylized character art."

**Who benefits:** Maya, Rin, Jordan, Diego, Hana, Ryo — everyone who generates character visuals.
