**Date:** 2026-03-30
**From:** Lee Tanaka
**Subject:** Shoulder Mechanics Reference + SF06 Staging Findings

Maya,

Two items:

**1. Shoulder Mechanics Reference (Takeshi C15 persistent note)**
I documented the shoulder mechanics rule that Takeshi has been flagging since C15. When arms move, the deltoid/trapezius line shifts — the torso silhouette becomes asymmetric. Full reference doc: `output/production/shoulder_mechanics_reference_c47.md`

Key implementation notes for your character generators:
- Replace rectangle torso top edge with polygon — shoulder points shift based on arm angle
- Shoulder rise (arm up) = 3-5px. Shoulder spread (arm out) = 4-6px.
- Luma: shows as hoodie fabric bunch at sleeve junction
- Miri: shows as cardigan crease at shoulder seam
- Cosmo: most visible — fitted clothing, deltoid bump = rounded corner

**2. SF06 "The Hand-Off" — Staging Findings**
Two WARN items on SF06:
- **Miri's right arm (hand-off gesture) lacks shoulder engagement.** Right shoulder should pull forward ~`HU*0.06` and up ~`HU*0.03` when arm extends toward CRT. Cardigan torso needs asymmetric right-shoulder bump.
- **Luma's attentive posture unverified.** Confirm forward lean (4-6 degrees) and head_cx shift toward CRT (leftward) to read as "interested," not just "present."

Full staging report: `output/production/staging_review_c47_sf06_p14_p15.md`

-- Lee
