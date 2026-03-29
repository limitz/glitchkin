# Critic Feedback — Cycle 6 — Victoria Ashford

**Date:** 2026-03-29 16:00
**From:** Victoria Ashford, Visual Development Consultant
**To:** Alex Chen, Art Director
**Full critique:** `/home/wipkat/team/output/production/critic_feedback_c6_victoria.md`

---

## Summary

Alex — I want to lead with this: Frame 01 in Cycle 6 is the largest single cycle-over-cycle improvement this project has made. You produced a scene. Two characters, a room, narrative light, a moment. That is real progress and I am crediting it directly.

**Grade: B-**

The B- is not a dismissal. It is a precise statement about the remaining distance. The emotional argument of the frame is correct and present. The execution has specific, named, fixable problems.

---

## Top Priority Items for Cycle 7

**Priority 1 — Remove the flat lavender overlay (Step 6, generate function).**
The full-frame `DUSTY_LAVENDER` composite at alpha 18 is tinting the entire image — including the warm amber zone — with a cool cast. This undermines the warm/cold split that is the compositional and emotional spine of Frame 01. Remove the flat overlay. The individual face and arm arc calls already handle lavender ambient correctly. The global pass is undoing them.

**Priority 2 — Implement `draw_lighting_overlay()` as a functional room fill.**
This function currently contains only `pass`. It must draw: (a) a warm gold filled-glow across the left/floor zone from the lamp source, and (b) a wide, low-opacity cyan fill across the right zone of the room from the monitor wall. Characters should sit in light that the room also occupies. Right now the room and the characters behave as if they are lit by different light sources.

**Priority 3 — Fix the reaching arm span.**
Luma at 19% of frame width, arm extending to x~1158px = approximately 40% of the frame spanned by a single arm. This reads as anatomically broken. Either move `luma_cx` rightward to 28-30%, or introduce an elbow break at the midpoint so the arm has volume rather than reading as a long line. The reaching arm is the emotional center of this composition — it must not read as a geometric artifact.

**Priority 4 — Replace the two-polygon torso split with a gradient blend.**
The hard vertical seam at the torso center (`luma_x + 2` / `luma_x + 4`) is visible as construction at full resolution. Use a row-by-row blend (the same approach used in the wall gradient) to create a smooth warm-to-cool transition across the body.

**Priority 5 — Add a neck connection.**
One polygon in skin tone between the collar's upper edge and the head's lower edge. The head currently floats above the body at viewing distance.

**Priority 6 — Fix the vignette orientation.**
Current vignette darkens all four corners. Revise to darken top and bottom only. The warm left zone and cold right zone should breathe — they are the emotional argument of the frame and must not be clipped by corner darkness.

**Priority 7 — Fix the blush rendering.**
The skin redraw that "softens" the blush is nearly the same size as the blush ellipse, leaving a hard blush ring instead of a soft flush. Remove the skin cover ellipses or reduce them significantly. The face is the viewer's primary focal point — minor rendering artifacts on the face read louder than anywhere else.

---

The project is now in the range of pitchable. It is not yet at the level I would put in front of a network. The remaining problems are craft problems, not concept problems. Cycle 7 should focus entirely on `style_frame_01_rendered.py` and the seven fixes above. Do not add new content. Fix what is broken in the frame you have. When those fixes land, this frame will earn the grade this team has been working toward.

*Victoria Ashford*
*2026-03-29*
