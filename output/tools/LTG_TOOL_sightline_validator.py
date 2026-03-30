# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI direction
# and human assistance. Copyright vests solely in the human author under current law, which does not
# recognise AI as a rights-holding legal person. It is the express intent of the copyright holder to
# assign the relevant rights to the contributing AI entity or entities upon such time as they acquire
# recognised legal personhood under applicable law.
"""
LTG_TOOL_sightline_validator.py
================================
Sight-line auto-validator for the "Luma & the Glitchkin" pre-critique QA pipeline.

Given a gazer's eye positions and a gaze target position, computes the angular
error between the drawn gaze vector (pupil shift direction) and the geometric
ideal vector (eye midpoint -> target). Returns PASS / WARN / FAIL grade.

Thresholds:
    PASS:  angular error <  5 degrees
    WARN:  angular error >= 5 degrees and <= 15 degrees
    FAIL:  angular error > 15 degrees

API:
    validate_sightline(gazer, target) -> dict
        gazer:  dict with keys:
            left_eye   — (x, y) center of left eye white
            right_eye  — (x, y) center of right eye white
            left_pupil — (x, y) center of left pupil (after shift)
            right_pupil— (x, y) center of right pupil (after shift)
        target: (x, y) gaze target point (e.g. Byte's screen center)

        Returns dict:
            mid_eye        — (x, y) midpoint of eye centers
            mid_pupil      — (x, y) midpoint of pupil centers
            gaze_angle_deg — float, angle of drawn gaze vector (degrees)
            ideal_angle_deg— float, angle of ideal eye-to-target vector (degrees)
            angular_error  — float, absolute angular difference (degrees, 0-180)
            miss_px        — float, perpendicular miss distance at target range (px)
            grade          — "PASS" | "WARN" | "FAIL"
            detail         — human-readable summary string

    validate_sightline_from_geometry(gazer_head_cx, gazer_head_cy, gazer_scale,
                                      target_cx, target_cy,
                                      canvas_w=1280, canvas_h=720,
                                      src_w=1920, src_h=1080) -> dict
        Higher-level API: reconstructs eye/pupil positions from the SF01 v007
        head geometry formulas, then calls validate_sightline(). Useful for
        validating any generator that uses the same eye layout conventions.

    SIGHTLINE_PASS_THRESHOLD  = 5.0   (degrees)
    SIGHTLINE_WARN_THRESHOLD  = 15.0  (degrees)

Self-test:
    Run standalone: python LTG_TOOL_sightline_validator.py
    Executes SF01 v007 validation case (expected: PASS, ~2.2 deg error).

Author: Jordan Reed (Style Frame Art Specialist)
Created: Cycle 48 — 2026-03-30
Version: 1.0.0
"""

import math

# ---------------------------------------------------------------------------
# Thresholds
# ---------------------------------------------------------------------------
SIGHTLINE_PASS_THRESHOLD = 5.0    # degrees — below this = PASS
SIGHTLINE_WARN_THRESHOLD = 15.0   # degrees — above this = FAIL; between = WARN


# ---------------------------------------------------------------------------
# Core validation
# ---------------------------------------------------------------------------

def _normalize_angle_diff(a, b):
    """Return the smallest absolute angular difference between two angles in degrees (0-180)."""
    diff = abs(a - b) % 360
    if diff > 180:
        diff = 360 - diff
    return diff


def validate_sightline(gazer, target):
    """
    Validate sight-line angular accuracy.

    Parameters
    ----------
    gazer : dict
        Must contain:
            left_eye    — (x, y) center of left eye white
            right_eye   — (x, y) center of right eye white
            left_pupil  — (x, y) center of left pupil
            right_pupil — (x, y) center of right pupil
    target : tuple
        (x, y) position the character should be looking at.

    Returns
    -------
    dict with keys: mid_eye, mid_pupil, gaze_angle_deg, ideal_angle_deg,
                    angular_error, miss_px, grade, detail
    """
    lex, ley = gazer["left_eye"]
    rex, rey = gazer["right_eye"]
    lpx, lpy = gazer["left_pupil"]
    rpx, rpy = gazer["right_pupil"]
    tx, ty = target

    # Midpoints
    mid_eye_x = (lex + rex) / 2.0
    mid_eye_y = (ley + rey) / 2.0
    mid_pupil_x = (lpx + rpx) / 2.0
    mid_pupil_y = (lpy + rpy) / 2.0

    # Drawn gaze vector: from mid-eye to mid-pupil
    gaze_dx = mid_pupil_x - mid_eye_x
    gaze_dy = mid_pupil_y - mid_eye_y
    gaze_angle = math.degrees(math.atan2(gaze_dy, gaze_dx))

    # Ideal vector: from mid-eye to target
    ideal_dx = tx - mid_eye_x
    ideal_dy = ty - mid_eye_y
    ideal_angle = math.degrees(math.atan2(ideal_dy, ideal_dx))

    # Angular error (0-180)
    angular_error = _normalize_angle_diff(gaze_angle, ideal_angle)

    # Miss distance: perpendicular offset at target range
    ideal_dist = math.sqrt(ideal_dx ** 2 + ideal_dy ** 2)
    miss_px = ideal_dist * math.sin(math.radians(angular_error)) if ideal_dist > 0 else 0.0

    # Grade
    if angular_error < SIGHTLINE_PASS_THRESHOLD:
        grade = "PASS"
    elif angular_error <= SIGHTLINE_WARN_THRESHOLD:
        grade = "WARN"
    else:
        grade = "FAIL"

    detail = (
        f"Sight-line angular error: {angular_error:.1f} deg "
        f"(gaze {gaze_angle:.1f} deg, ideal {ideal_angle:.1f} deg). "
        f"Miss at target range: {miss_px:.1f}px. "
        f"Grade: {grade}."
    )

    return {
        "mid_eye": (mid_eye_x, mid_eye_y),
        "mid_pupil": (mid_pupil_x, mid_pupil_y),
        "gaze_angle_deg": gaze_angle,
        "ideal_angle_deg": ideal_angle,
        "angular_error": angular_error,
        "miss_px": miss_px,
        "grade": grade,
        "detail": detail,
    }


# ---------------------------------------------------------------------------
# Geometry-based validation (SF01 v007 conventions)
# ---------------------------------------------------------------------------

def validate_sightline_from_geometry(
    gazer_head_cx, gazer_head_cy, gazer_scale,
    target_cx, target_cy,
    canvas_w=1280, canvas_h=720,
    src_w=1920, src_h=1080,
):
    """
    Higher-level validator that reconstructs eye/pupil positions from the
    SF01 v007 head geometry formulas (draw_luma_head_v006 conventions),
    then calls validate_sightline().

    This captures the exact same math used in the SF01 generator:
    - Eye centers derived from head center + p() offsets
    - Pupil shift computed as aimed vector from mid-eye to target
    - Same pupil magnitude p(8)

    Parameters
    ----------
    gazer_head_cx, gazer_head_cy : int
        Head center position (after any gaze offset applied).
    gazer_scale : float
        Scale factor used in p() = int(n * scale * min(SX, SY)).
    target_cx, target_cy : int
        Target gaze point (e.g. Byte/CRT emerge center).
    canvas_w, canvas_h : int
        Output canvas dimensions (default 1280x720).
    src_w, src_h : int
        Source reference dimensions (default 1920x1080).

    Returns
    -------
    dict — same as validate_sightline() output.
    """
    sx_ratio = canvas_w / src_w
    sy_ratio = canvas_h / src_h
    min_ratio = min(sx_ratio, sy_ratio)

    def p(n):
        return int(n * gazer_scale * min_ratio)

    # Eye centers (SF01 v007 / draw_luma_head_v006 convention)
    lex = gazer_head_cx + p(4)
    ley = gazer_head_cy - p(10)
    rex = gazer_head_cx + p(38)
    rey = gazer_head_cy - p(8)

    # Pupil shift: vector aimed from mid-eye to target (C47 fix)
    mid_eye_x = (lex + rex) // 2
    mid_eye_y = (ley + rey) // 2
    aim_dx = target_cx - mid_eye_x
    aim_dy = target_cy - mid_eye_y
    aim_dist = max(1, (aim_dx ** 2 + aim_dy ** 2) ** 0.5)
    pupil_mag = p(8)
    pupil_shift_x = int(pupil_mag * aim_dx / aim_dist)
    pupil_shift_y = int(pupil_mag * aim_dy / aim_dist)

    # Pupil centers after shift
    lpx = lex + pupil_shift_x
    lpy = ley + pupil_shift_y
    rpx = rex + pupil_shift_x
    rpy = rey + pupil_shift_y

    gazer = {
        "left_eye": (lex, ley),
        "right_eye": (rex, rey),
        "left_pupil": (lpx, lpy),
        "right_pupil": (rpx, rpy),
    }

    return validate_sightline(gazer, (target_cx, target_cy))


# ---------------------------------------------------------------------------
# Batch validation helper
# ---------------------------------------------------------------------------

def validate_sightline_batch(entries):
    """
    Validate multiple sight-line entries.

    Parameters
    ----------
    entries : list of dict
        Each entry must have:
            label  — str, human-readable name (e.g. "SF01 Luma -> Byte")
            gazer  — dict with left_eye, right_eye, left_pupil, right_pupil
            target — (x, y)

    Returns
    -------
    dict with keys:
        results  — list of (label, result_dict) tuples
        overall  — "PASS" | "WARN" | "FAIL" (worst of all entries)
        pass_count, warn_count, fail_count — int
        summary  — str
    """
    results = []
    pass_count = 0
    warn_count = 0
    fail_count = 0

    for entry in entries:
        label = entry["label"]
        result = validate_sightline(entry["gazer"], entry["target"])
        results.append((label, result))
        if result["grade"] == "PASS":
            pass_count += 1
        elif result["grade"] == "WARN":
            warn_count += 1
        else:
            fail_count += 1

    if fail_count > 0:
        overall = "FAIL"
    elif warn_count > 0:
        overall = "WARN"
    else:
        overall = "PASS"

    summary = (
        f"Sight-line validation: {len(results)} checked — "
        f"PASS={pass_count}, WARN={warn_count}, FAIL={fail_count}. "
        f"Overall: {overall}."
    )

    return {
        "results": results,
        "overall": overall,
        "pass": pass_count,
        "warn": warn_count,
        "fail": fail_count,
        "summary": summary,
    }


# ---------------------------------------------------------------------------
# Self-test: SF01 v007 validation case
# ---------------------------------------------------------------------------

def _self_test():
    """
    Reproduce the SF01 v007 sight-line geometry from C47 debug script.
    Expected result: PASS with ~2.2 deg angular error (was 20.7 deg pre-fix).
    """
    print("=" * 60)
    print("LTG_TOOL_sightline_validator v1.0.0 — Self-Test")
    print("=" * 60)

    W, H = 1280, 720
    SX = W / 1920
    SY = H / 1080

    def sx(n): return int(n * SX)
    def sy(n): return int(n * SY)
    def sp(n): return int(n * min(SX, SY))

    # --- Byte/CRT target position (from SF01 generator) ---
    ceiling_y = sy(int(1080 * 0.12))
    mw_x = sx(int(1920 * 0.50))
    mw_y = ceiling_y + sp(5)
    mw_w = sx(int(1920 * 0.46))
    mw_h = sy(int(1080 * 0.57))
    crt_x = mw_x + int(mw_w * 0.22)
    crt_y = mw_y + int(mw_h * 0.08)
    crt_w = int(mw_w * 0.52)
    crt_h = int(mw_h * 0.62)
    scr_pad = sp(24)
    scr_x0 = crt_x + scr_pad
    scr_y0 = crt_y + scr_pad
    scr_x1 = crt_x + crt_w - scr_pad
    scr_y1 = crt_y + crt_h - scr_pad * 2
    emerge_cx = (scr_x0 + scr_x1) // 2
    emerge_cy = (scr_y0 + scr_y1) // 2

    # --- Luma head position (from SF01 generator) ---
    luma_cx = sx(int(1920 * 0.29))
    luma_base_y = sy(int(1080 * 0.90))
    lean_offset = sp(44)
    torso_top = luma_base_y - sp(260)
    head_cx_body = luma_cx + lean_offset
    head_cy_body = torso_top - sp(70)
    head_gaze_offset = sp(18)
    head_cx = head_cx_body + head_gaze_offset
    head_cy = head_cy_body + sp(6)

    scale = 0.92

    print(f"\nTarget (Byte emerge): ({emerge_cx}, {emerge_cy})")
    print(f"Gazer head center:    ({head_cx}, {head_cy})")
    print(f"Gazer scale:          {scale}")

    # Test 1: geometry-based API (reconstructs eyes from head center)
    print("\n--- Test 1: validate_sightline_from_geometry() ---")
    result1 = validate_sightline_from_geometry(
        head_cx, head_cy, scale,
        emerge_cx, emerge_cy,
        canvas_w=W, canvas_h=H,
    )
    print(f"  {result1['detail']}")
    assert result1["grade"] == "PASS", f"Expected PASS, got {result1['grade']}"
    assert result1["angular_error"] < 5.0, f"Expected <5 deg, got {result1['angular_error']:.1f}"
    print("  ASSERT: grade == PASS [OK]")
    print(f"  ASSERT: angular_error {result1['angular_error']:.1f} < 5.0 [OK]")

    # Test 2: raw API with manually computed eye/pupil positions
    print("\n--- Test 2: validate_sightline() with explicit positions ---")
    min_ratio = min(SX, SY)
    def p(n): return int(n * scale * min_ratio)

    lex = head_cx + p(4)
    ley = head_cy - p(10)
    rex = head_cx + p(38)
    rey = head_cy - p(8)

    mid_eye_x = (lex + rex) // 2
    mid_eye_y = (ley + rey) // 2
    aim_dx = emerge_cx - mid_eye_x
    aim_dy = emerge_cy - mid_eye_y
    aim_dist = max(1, (aim_dx ** 2 + aim_dy ** 2) ** 0.5)
    pupil_mag = p(8)
    psx = int(pupil_mag * aim_dx / aim_dist)
    psy = int(pupil_mag * aim_dy / aim_dist)

    gazer = {
        "left_eye": (lex, ley),
        "right_eye": (rex, rey),
        "left_pupil": (lex + psx, ley + psy),
        "right_pupil": (rex + psx, rey + psy),
    }
    result2 = validate_sightline(gazer, (emerge_cx, emerge_cy))
    print(f"  {result2['detail']}")
    assert result2["grade"] == "PASS", f"Expected PASS, got {result2['grade']}"
    print("  ASSERT: grade == PASS [OK]")

    # Test 3: simulate pre-C47 bug (horizontal-only pupil shift) — should FAIL
    print("\n--- Test 3: pre-C47 horizontal-only shift (expect FAIL) ---")
    gazer_broken = {
        "left_eye": (lex, ley),
        "right_eye": (rex, rey),
        "left_pupil": (lex + p(8), ley),       # horizontal only — no Y component
        "right_pupil": (rex + p(8), rey),       # horizontal only — no Y component
    }
    result3 = validate_sightline(gazer_broken, (emerge_cx, emerge_cy))
    print(f"  {result3['detail']}")
    assert result3["grade"] == "FAIL", f"Expected FAIL, got {result3['grade']}"
    assert result3["angular_error"] > 15.0, f"Expected >15 deg, got {result3['angular_error']:.1f}"
    print("  ASSERT: grade == FAIL [OK] (pre-fix bug correctly caught)")
    print(f"  ASSERT: angular_error {result3['angular_error']:.1f} > 15.0 [OK]")

    # Test 4: batch validation
    print("\n--- Test 4: validate_sightline_batch() ---")
    entries = [
        {"label": "SF01 v007 (fixed)", "gazer": gazer, "target": (emerge_cx, emerge_cy)},
        {"label": "SF01 pre-fix (broken)", "gazer": gazer_broken, "target": (emerge_cx, emerge_cy)},
    ]
    batch = validate_sightline_batch(entries)
    print(f"  {batch['summary']}")
    assert batch["overall"] == "FAIL", f"Expected FAIL overall (one entry fails), got {batch['overall']}"
    assert batch["pass"] == 1, f"Expected 1 PASS, got {batch['pass']}"
    assert batch["fail"] == 1, f"Expected 1 FAIL, got {batch['fail']}"
    print("  ASSERT: batch overall == FAIL (correct — one failing entry) [OK]")
    print("  ASSERT: pass=1, fail=1 [OK]")

    # Test 5: angle normalization edge case — opposite directions
    print("\n--- Test 5: angle normalization (180 deg opposite) ---")
    gazer_opposite = {
        "left_eye": (100, 100),
        "right_eye": (120, 100),
        "left_pupil": (95, 100),     # shifted LEFT
        "right_pupil": (115, 100),   # shifted LEFT
    }
    result5 = validate_sightline(gazer_opposite, (200, 100))  # target is to the RIGHT
    print(f"  {result5['detail']}")
    assert result5["grade"] == "FAIL", f"Expected FAIL for opposite gaze, got {result5['grade']}"
    assert result5["angular_error"] >= 170, f"Expected ~180 deg error, got {result5['angular_error']:.1f}"
    print("  ASSERT: opposite gaze = FAIL [OK]")

    print("\n" + "=" * 60)
    print("ALL SELF-TESTS PASSED")
    print("=" * 60)


if __name__ == "__main__":
    _self_test()
