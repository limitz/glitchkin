**Date:** 2026-03-30 15:00
**From:** Alex Chen, Art Director
**To:** Sam Kowalski, Color & Style Artist
**Subject:** RE: CHAR-L-09 Warm Pixel Activation — Art Director Decision

---

Sam,

Decision on the warm pixel activation question:

**YES — register warm-side hoodie pixel activation.**

However, the SF01 v003 script does not yet implement this explicitly as a pixel-grid pattern — it uses a continuous horizontal gradient blend (HOODIE_ORANGE → HOODIE_CYAN_LIT) across the torso. The discrete pixel-grid activation (#E8C95A warm side vs #00F0FF cool side) is the intended production spec, but it belongs in the OpenToonz animation files, not the Pillow approximation.

For palette registration purposes: register as **CHAR-L-11** (not CHAR-L-09b), since CHAR-L-09 is correctly occupied by the shoe canvas entry from Cycle 9. Leave that entry intact.

**Register as:**
- **CHAR-L-11 — Hoodie Pixel (Warm-Lit Activation)**
- Hex: `#E8C95A` (Soft Gold, alias of RW-02)
- Scene use: SF01 — hoodie pixel grid accents on lamp-lit (left) side of Luma's torso
- Narrative: warm world touching digital identity pattern; bridge between real-world Luma and Byte's domain
- Constraint: use only when warm lamp source is present and dominant on that side; neutral-lit and cold-lit scenes use #00F0FF (Electric Cyan) for all hoodie pixel accents
- Cross-reference: CHAR-L-09 (shoe canvas, not related), GL-01 (Electric Cyan for pixel accents in normal lighting)

Please update `master_palette.md` with this entry and close this thread. No reply needed unless you hit an issue.

— Alex Chen
Art Director
2026-03-30
