# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
SF01 sight-line geometry verification — C47 Jordan Reed
Computes Luma eye/pupil positions and Byte target using C47 vector-aimed pupil shift.
"""
import math

W, H = 1280, 720
SX = W / 1920
SY = H / 1080
def sx(n): return int(n * SX)
def sy(n): return int(n * SY)
def sp(n): return int(n * min(SX, SY))

# Background / CRT / Byte position
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
print(f"Byte/emerge target: cx={emerge_cx}, cy={emerge_cy}")

# Luma body
luma_cx = sx(int(1920 * 0.29))
luma_base_y = sy(int(1080 * 0.90))
lean_offset = sp(44)
torso_top = luma_base_y - sp(260)
head_cx_body = luma_cx + lean_offset
head_cy_body = torso_top - sp(70)
head_gaze_offset = sp(18)
head_cx = head_cx_body + head_gaze_offset
head_cy = head_cy_body + sp(6)
print(f"Luma head: cx={head_cx}, cy={head_cy}")

scale = 0.92
def p(n): return int(n * scale * min(SX, SY))

head_r = p(72)

# Eye positions
lex = head_cx + p(4)
ley = head_cy - p(10)
rex = head_cx + p(38)
rey = head_cy - p(8)

# C47 VECTOR-AIMED pupil shift (matches generator code)
mid_eye_x = (lex + rex) // 2
mid_eye_y = (ley + rey) // 2
aim_dx = emerge_cx - mid_eye_x
aim_dy = emerge_cy - mid_eye_y
aim_dist = max(1, (aim_dx**2 + aim_dy**2) ** 0.5)
pupil_mag = p(8)
pupil_shift_x = int(pupil_mag * aim_dx / aim_dist)
pupil_shift_y = int(pupil_mag * aim_dy / aim_dist)

# Final pupil centers
lpx = lex + pupil_shift_x
lpy = ley + pupil_shift_y
rpx = rex + pupil_shift_x
rpy = rey + pupil_shift_y

print(f"\nLeft eye center: ({lex},{ley})")
print(f"Left pupil center: ({lpx},{lpy})")
print(f"Right eye center: ({rex},{rey})")
print(f"Right pupil center: ({rpx},{rpy})")
print(f"Pupil shift vector: dx={pupil_shift_x}, dy={pupil_shift_y} (magnitude={pupil_mag})")

# Verify gaze direction
mid_px = (lpx + rpx) // 2
mid_py = (lpy + rpy) // 2
gaze_dx = mid_px - mid_eye_x
gaze_dy = mid_py - mid_eye_y
gaze_angle = math.degrees(math.atan2(gaze_dy, gaze_dx))
ideal_angle = math.degrees(math.atan2(aim_dy, aim_dx))

print(f"\nGaze angle: {gaze_angle:.1f} deg")
print(f"Ideal angle: {ideal_angle:.1f} deg")
print(f"Angular error: {abs(gaze_angle - ideal_angle):.1f} deg")

print(f"\nByte is {'ABOVE' if emerge_cy < head_cy else 'BELOW'} Luma head by {abs(head_cy - emerge_cy)}px")
print(f"Byte is {'RIGHT of' if emerge_cx > head_cx else 'LEFT of'} Luma head by {abs(emerge_cx - head_cx)}px")

if abs(gaze_angle - ideal_angle) < 5:
    print("\n--- RESULT: PASS --- Pupil gaze locks on Byte target.")
else:
    print(f"\n--- RESULT: FAIL --- Angular error {abs(gaze_angle - ideal_angle):.1f} deg exceeds 5 deg.")
