**Date:** 2026-03-30
**From:** Alex Chen, Art Director
**To:** Maya Santos, Character Designer
**Subject:** C42 — Luma v012 face curves integration complete — body posture work now v013

Maya,

Quick update before your body posture work begins.

I've updated LTG_TOOL_luma_expression_sheet.py to v012. This cycle's change is the face curves integration (Producer's direct request via inbox). The expression sheet now routes face drawing through draw_luma_face() from LTG_TOOL_luma_face_curves v1.1.0 for these expressions:

- THE NOTICING → THE_NOTICING
- THE NOTICING — DOUBT → THE_NOTICING_DOUBT
- WORRIED → WORRIED
- FRUSTRATED → FRUSTRATED
- DETERMINED → DETERMINED

CURIOUS, SURPRISED, and DELIGHTED still use the v011 hand-coded face drawing (no matching face curves expression for those).

**What this means for your work:**

Your Tier 1 body posture work (RECKLESS, ALARMED, FRUSTRATED, THE NOTICING silhouette upgrades) was assigned as v012. Since I've used the v012 slot for the face curves integration, please base your body posture deliverable on the current v012 generator and deliver it as **v013**.

The body posture changes are purely in EXPR_SPECS / draw_body_pose() / the arm/leg spec dicts — no conflict with the face curves integration. You can pick up from the v012 file directly.

One note: the face curves path skips draw_head() (which had cheek nubs) and uses the face curves oval exclusively. If you're modifying body posture for FRUSTRATED or THE NOTICING, be aware the face will look different at v012 from v011 — that's expected and correct. Hair, body, arms, legs draw the same.

Alex
