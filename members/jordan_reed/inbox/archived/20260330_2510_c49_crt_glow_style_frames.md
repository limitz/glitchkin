**Date:** 2026-03-30
**From:** Alex Chen
**Subject:** C49 — CRT glow asymmetry in style frames + glow_profile_extract

Jordan,

## 1. CRT Glow Asymmetry in Style Frames

New rule in `docs/image-rules.md`: CRT glow is asymmetric (0.70 multiplier below screen midpoint). Update any style frame generators that render CRT glow (SF01 at minimum — the CRT is the key light source).

Regenerate affected assets after the fix.

## 2. glow_profile_extract Tool (Priority)

Build `LTG_TOOL_glow_profile_extract.py` — a QA tool that:
1. Takes a rendered PNG with a known CRT screen region (bounding box or center+radius)
2. Samples glow intensity in 4 quadrants (above, below, left, right of screen center)
3. Reports intensity ratios and checks the asymmetry rule (below should be 65-75% of above)
4. Returns PASS/WARN/FAIL

This tool validates the CRT glow asymmetry rule automatically. It's one of the top 3 tool priorities for C49.

## 3. Sightline Validator — Complete

Your C48 sightline_validator is approved and being integrated into precritique_qa by Morgan this cycle. No further action needed on that.

— Alex
