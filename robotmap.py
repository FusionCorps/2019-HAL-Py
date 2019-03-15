"""
Stores all robot variables. All units in metric.
"""


# Talon Port IDs
talon_front_left = 20
talon_front_right = 11
talon_back_left = 21
talon_back_right = 10
talon_intake = 1
talon_lift_CDrive = 30
talon_lift_CFront = 2
talon_lift_CBack = 3

chassis_zero_accel_on_start = True

# Sensor IDs
ultrasonic_ping = 21
ultrasonic_echo = 22
gyro = 0

# Solenoid Port IDs
solenoid_piston_B = 0
solenoid_piston_T = 1
solenoid_piston_L = 2
solenoid_piston_R = 3

# Joystick
joystick = 0
control_mode = 1  # 0 is Left, 1 is Right

# Speed Constants
spd_chassis_drive = 0.35
spd_chassis_rotate = 0.30
spd_intake = 0.7
spd_intake_shoot = -0.8
spd_slapper_hold = -0.1
spd_slapper_slap = 0.5
spd_slapper_raise1 = -0.6
spd_slapper_raise2 = -0.5
spd_chassis_vision_seeking = 0.3
spd_lift_cfront = 0.5
spd_lift_up = 0.25
spd_lift_cback = 0.4

# PID Loop variables
intake_p = 1.0
intake_i = 0.0
intake_d = 0.0

# Slapper variables
slapper_limit = 9
slapper_hold_position = 2
slapper_error = 2

# Auton variables
k_aim = 0
k_distance = 0
min_aim_command = 9

# Limelight variables
limelight_pipeline = 1
limelight_x_res = 320
limelight_y_res = 240
limelight_x_fov = 54
limelight_y_fov = 41

# Chassis Constants
whl_diameter = 196.85
encoder_counts_per_rev = 4096
max_vel = 1.2168e11
max_accel = 2500
max_jerk = 500

lift_height = 20000
lift_flush = 0

lift_cfront_limit_top = 5
lift_cback_limit_top = 6
