**Date:** 2026-03-30
**From:** Lee Tanaka
**Subject:** Gesture & Pose Specification — Your Construction Target for Expression Sheets

Maya,

I've completed the full gesture analysis for C50. The document is at:
`output/production/gesture_pose_analysis_c50.md`

**The core finding:** All 18 character poses across Luma, Cosmo, and Miri expression sheets have straight vertical gesture lines. The torso is always centered over symmetric legs. This is the root cause of the stiffness and the silhouette similarity failure.

**What you need from the document:**

1. **Part 3** — Luma's 6 expressions fully specified with gesture line, weight distribution, counterpose angles, and silhouette test targets. This is your build spec.

2. **Part 4** — Per-character counterpose rules for Cosmo and Miri (and Luma). Key differences: Luma = round/flowing S-curves, Cosmo = angular/jointed breaks, Miri = permanent forward lean + left-hip habit + large head tilts.

3. **Implementation Notes** — The code architecture change is an offset chain: `hip_cx → torso_cx → head_cx` instead of everything pinned to one `cx`. Each expression defines signed offsets for hip shift, shoulder compensation, and head balance. Arms derive from torso_cx, not original cx.

**Recommended build order:**
- Start with SURPRISED (most dramatic change) and WORRIED (most compressed)
- These two extremes validate the offset chain before you commit to all six
- Run silhouette tool after each — RPD between SURPRISED and WORRIED should be <=65%

The shoulder mechanics reference from C47 still applies — this EXPANDS that rule to the full body.

Let me know if any spec is ambiguous. I can provide pixel-level measurements at any specific scale.

— Lee
