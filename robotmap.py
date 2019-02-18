"""
Stores all robot variables. All units in metric.
"""


# Talon Port IDs
talon_front_left = 20
talon_front_right = 11
talon_back_left = 21
talon_back_right = 10
talon_intake = 4
talon_slapper = 30

# Sensor IDs
# TODO update ids
ultrasonic_ping = 1
ultrasonic_echo = 2
gyro = 1

# Solenoid Port IDs
solenoid_venturi_L = 0
solenoid_venturi_R = 1
solenoid_piston_L = 2
solenoid_piston_R = 3

# Joystick
joystick = 0
control_mode = 1  # 0 is Left, 1 is Right

# Speed Constants
spd_chassis_drive = 0.8
spd_chassis_rotate = 0.4
spd_intake = -0.5
spd_intake_shoot = -0.8
spd_slapper_hold = 0.6
spd_slapper_slap = 0.2
spd_slapper_raise1 = -0.7
spd_slapper_raise2 = -0.6
spd_chassis_vision_seeking = 0.3

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
whl_diameter = 1
encoder_counts_per_rev = 360
max_vel = 0
max_accel = 0
max_jerk = 0
