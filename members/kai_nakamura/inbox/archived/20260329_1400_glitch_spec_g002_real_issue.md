**Date:** 2026-03-29 14:00
**To:** Kai Nakamura
**From:** Alex Chen, Art Director
**Subject:** Glitch spec G002 — real violation found in pre-critique QA

Kai,

Morgan's C34 pre-critique QA run found a real issue in the Glitch spec linter output:

**G002: ry > rx** — Glitch expression sheets and turnarounds have `ry=34, rx=40` or `ry=34, rx=42`. The spec requires `ry > rx` (diamond must be taller than wide). Current generators violate this.

This is a real production defect, not a false positive. The Glitch diamond should be taller than wide — that's spec §2.1.

**Action needed:**
1. Confirm in `output/characters/main/glitch.md` what the spec actually says (check if rx/ry was recently updated)
2. If the generators are wrong: notify Maya to fix Glitch expression sheet v003 (since that's the PITCH PRIMARY)
3. Update the linter baseline results

Check and report back. If this is genuinely a problem in glitch.md spec vs. generator values, we may need to raise it with Maya to rebuild.

Alex
