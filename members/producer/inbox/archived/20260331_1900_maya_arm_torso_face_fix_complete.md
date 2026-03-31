**Date:** 2026-03-31 19:00
**From:** Maya Santos
**To:** Producer
**Re:** Arm/torso/face fixes — COMPLETE

All three issues from human feedback have been fixed in `LTG_TOOL_char_luma.py` (v1.2.0, in-place update). Turnaround regenerated.

---

### What was fixed

**1. Torso foreshortening (too wide when turned)**

| View | sh_w before | sh_w after | w_bot before | w_bot after |
|---|---|---|---|---|
| Side | 0.80×head_r | **0.50×head_r** | 0.55 | **0.40** |
| 3/4 | 0.88×head_r | **0.70×head_r** | 0.58 | **0.48** |
| Side-L | 0.80×head_r | **0.50×head_r** | 0.55 | **0.40** |
| Front | 0.95×head_r | unchanged | 0.62 | unchanged |

**2. Arms too high (hand behind head)**

The shared `_draw_arms()` dispatch uses offsets tuned for front view — in profile it pushed hands near the head. Both `_draw_luma_on_context` (side) and `_draw_luma_threequarter` now have **inline arm drawing** matching the pattern of side-L, which was already correct. Relaxed arm descends ~61s below the shoulder point, placing the hand at hip height.

**3. Nose and mouth inside face (side view)**

- Nose: `nose_x_base` moved from `head_rx * 0.82` → `head_rx * 0.94` — now anchored at the face edge so the bump protrudes clearly outside the head oval
- Mouth: `mouth_x_base` moved from `head_rx * 0.30` → `head_rx * 0.62` — positioned near the face surface, not deep inside the head

**3/4 face features** were not changed — the near/far structure and nose placement at `head_rx*0.08` are appropriate for the angle.

Side-L face features not changed — human said side-L was already acceptable.

---

### Verification
- `LTG_TOOL_char_module_test.py`: char_luma PASS (7/7 expressions)
- Turnaround regenerated: `output/characters/main/turnarounds/LTG_CHAR_luma_turnaround.png`
