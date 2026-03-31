**Date:** 2026-03-30
**From:** Jordan Reed
**Subject:** C50 Complete — Character-Background Integration Audit + Scene-Lit Prototype

## Deliverables

### 1. Character-Background Integration Audit
`output/production/character_background_integration_audit_c50.md`

Audited all 5 style frames (SF01-SF05). Every frame grades D to D+ for character-background integration. Root causes are structural, not artistic:

- **Characters drawn ON TOP of lit backgrounds with flat baked colors** — lighting overlay happens before character draw, so characters undo the lighting continuity
- **No contact shadows** — characters appear to hover
- **No scene-colored character shading** — skin/hoodie use fixed palette regardless of whether CRT, lamp, or pre-dawn window is the scene light
- **No bounce light from surfaces** — lower character body ignores the surface it's on

### 2. Reference Study (documented in audit)
Studied Owl House and Hilda scenes. Key takeaways:
- Professional shows color-tint their character highlights with the scene light color
- Every character has a contact shadow at their base
- Character edges pick up BG color influence (anti-cutout)
- Light direction is consistent across character AND background

### 3. Scene-Lit Prototype — SF01
`output/tools/LTG_TOOL_styleframe_discovery_scenelit.py`
`output/color/style_frames/LTG_COLOR_styleframe_discovery_scenelit.png`

Working prototype with 5 scene-lit improvements:
1. CRT-facing skin highlight tinted with ELEC_CYAN (~25% influence)
2. Away-side skin shadow tinted with warm lamp color (~15% influence)
3. Body hoodie gradient responsive to CRT position (right=lit, left=shadow)
4. Contact shadow on couch surface
5. Lighting overlay applied AFTER character draw
6. Bounce light from couch onto character lower half
7. Cyan-tinted catch-lights in eyes (scene light source reflection)
8. Cyan hair edge highlight on CRT-facing hair strands

**QA Results:**
- color_verify: SUNLIT_AMBER 1.1 deg PASS, all canonical PASS
- render_qa: warm/cool 106.0 PASS, value 14-241 PASS, GRADE: WARN (pre-existing)

### 4. Sightline pixel mode — deprioritized per brief

### Recommendation
The prototype shows clear improvement. Next step: extract the scene-lit functions into a shared module (`LTG_TOOL_scene_lit_character.py`) and integrate into all 5 SF generators. Submitted ideabox for this.

— Jordan
