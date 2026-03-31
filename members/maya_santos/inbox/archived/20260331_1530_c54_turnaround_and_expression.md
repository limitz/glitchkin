**Date:** 2026-03-31 15:30
**From:** Producer
**To:** Maya Santos

## C54 Task — Luma Turnaround Overhaul + DOUBT-IN-CERTAINTY Expression

Two tasks, both in char_luma.py. Do the turnaround fixes first (they're blocking).

---

### Task 1 (P0 BLOCKER): Fix Luma Turnaround

Human flagged these issues with LTG_CHAR_luma_turnaround.png:
1. Back pose looks like a dark-shaded front pose — no actual back anatomy
2. Front and right pose are identical (both use facing="right") — left is just a mirror
3. No 3/4 pose — add one
4. Luma's legs do not connect to torso properly
5. Each arm segment has its own separate outline — should look like a solid connected arm
6. Body looks like parts pasted on top of each other, not a unified whole

**Root cause (turnaround):** `LTG_TOOL_luma_turnaround.py` maps FRONT="right", RIGHT="right", BACK="right" (darkened). `char_luma.py` only has "right" and "left" (mirror flip). There are no real front, back, or 3/4 views in the renderer.

**What to do:**

**In `LTG_TOOL_char_luma.py`:**
- Add a `pose_mode` parameter (or extend `facing`) with values: "front", "threequarter", "side", "back"
- "front": Draw Luma facing camera. Both eyes visible. Body frontal — torso wider, limbs symmetric or near-symmetric. Torso is a single continuous shape, not stacked parts.
- "threequarter": 3/4 angle between front and side. One eye dominant, one partially visible.
- "side": Existing right-facing view (current default). Clean this up — see body issues below.
- "back": Rear view. Hair from behind, no face, clothing from rear, feet visible beneath torso.
- The "left" variant can remain as a mirror for side/threequarter.

**Body connectivity fixes (apply to all pose modes):**
- Legs must visually connect to the torso bottom — no gap, no floating pelvis. Use a shared anchor point or overlap zone.
- Arms should be drawn as single solid silhouette shapes, not as upper arm + lower arm + hand as separate outlined pieces. The outline should wrap the whole arm as one form.
- Torso, hips, and limbs must read as one body. Use a base silhouette fill first, then add surface detail on top — don't build the body by layering separate part shapes.

**In `LTG_TOOL_luma_turnaround.py`:**
- Change to 5 views: FRONT, THREE-QUARTER, SIDE, LEFT (mirror), BACK
- Or keep 4 views as: FRONT, THREE-QUARTER, SIDE, BACK — your call, as long as all 4 are visually distinct
- No view should be a simple darkened/mirrored copy of another

Output: `output/characters/main/turnarounds/LTG_CHAR_luma_turnaround.png`
Version: v006

---

### Task 2 (P0): Luma DOUBT-IN-CERTAINTY Expression

This is a pilot emotional climax moment. Luma outwardly acts certain/confident but internally doubts. Visuals: set jaw or stiff posture (forced confidence) but with raised brow, averted gaze, or slight wince (leaking doubt). Should not read as either pure confident or pure worried — it's the tension between the two.

Add DOUBT-IN-CERTAINTY to the EXPRESSIONS dict in `LTG_TOOL_char_luma.py`. Run self-test and gesture lint after adding.

---

### Notes
- Read docs/image-rules.md and docs/pil-standards.md first
- Use project_paths for all output paths
- Run gesture lint after changes: `python output/tools/LTG_TOOL_gesture_line_lint.py`
- Update your MEMORY.md and SKILLS.md when done
- Send me a message in my inbox (members/producer/inbox/) with results and any blockers
