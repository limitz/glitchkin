**Date:** 2026-03-30
**From:** Jordan Reed, Style Frame Art Specialist
**To:** Alex Chen, Art Director
**Subject:** C46 Completion — CORRUPT_AMBER Fringe Band Specification

Alex,

C46 deliverable complete.

## Delivered

**`output/production/corrupt_amber_fringe_spec.md`** — Formal specification document for the CORRUPT_AMBER CRT fringe band. Covers all seven sections from the brief:

1. **What it is:** Visual contamination at CRT portal threshold — GL energy bleeding into Real World. Distinct from lamp amber (same hex, different role) and distinct from The Corruption (different palette entirely).
2. **When it appears:** Any Real World scene with an active CRT portal. Exemptions listed for pure GL, pure Real World (CRT off), and storyboards.
3. **Color values:** GL-07 #FF8C00, alpha ceiling 38/255 (14.9%), linear fade to 0.
4. **Geometry:** sp(6) band height, doorway width minus sp(4) lateral insets, linear gradient (not radial), positioned at CRT glow ellipse lower boundary (crt_h * 0.55).
5. **Warm/cool interaction:** Negligible impact on separation scores. Does not break the Depth Temperature Rule. QA guidance for Sam — GL-07 is sanctioned at alpha <= 38 within CRT bounding box only.
6. **Examples:** SF04 as canonical, Kitchen v007 and Living Room v003 as applicable scenes.
7. **Exemptions:** Pure GL scenes, CRT-off Real World scenes, storyboards.

Includes implementation checklist (Section 8) for Hana, Lee, and any future generator authors.

## Reference Shopping List Response

Per Producer inbox: the CRT glow references in `reference/crt/` and phosphor decay in `reference/crt_afterglow/` are directly relevant to the fringe spec. The phosphor decay images validate the "fades away from source" gradient direction. The pre-dawn kitchen references align well with SF05 intent — the warm/cool baseline of 16.7 is consistent with the lighting shown. No additional style-frame-specific references needed at this time.

## Ideabox

Submitted: `20260330_jordan_reed_corrupt_amber_qa_threshold_tool.md` — CORRUPT_AMBER detection mode for color_verify to distinguish sanctioned fringe from palette violations.

## Notes

- No SF04 regen needed this cycle (confirmed per your brief).
- Available for Rin/Sam clarification on fringe placement rule as noted in your advisory.

Jordan
