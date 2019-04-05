"""
Stores all important robot variables. All units in metric.
"""


# Speed Controller port IDs
talon_front_left = 20
talon_front_right = 11
talon_back_left = 21
talon_back_right = 10

talon_intake = 1

talon_lift_drive = 30
talon_lift_front = 2
talon_lift_back = 3

# Solenoid Port IDs
solenoid_piston_B = 0
solenoid_piston_T = 1
solenoid_piston_L = 2
solenoid_piston_R = 3

# Sensor Port IDs
ultrasonic_ping = 21
ultrasonic_echo = 22
gyro = 0

# Joystick Port
joystick = 0

# Speed Constants
spd_chassis_drive = 0.55
spd_chassis_rotate = 0.4
spd_chassis_vision_seeking = 0.3
accel_chassis_max = 5.5
decel_chassis_max = 4.0

spd_intake = 0.5
spd_intake_shoot = -0.8

spd_lift_front = 0.3
spd_lift_up = 0.4
spd_lift_back = 0.3

# Limelight variables
limelight_pipeline = 1
limelight_x_res = 320
limelight_y_res = 240
limelight_x_fov = 54
limelight_y_fov = 41

# Chassis Constants
chassis_whl_diameter = 0.2032
chassis_encoder_counts_per_rev = 4096
chassis_max_vel = 1
chassis_max_acceleration = 0.2
chassis_max_jerk = 0.1
chassis_zero_acceleration_on_start = True

# Lift constants
lift_height = 22000
lift_height_2 = 9000
lift_cruise_velocity = 800
lift_acceleration = 100
lift_front_limit = 5
lift_back_limit = 6
lift_characteristics = (800, 100)
lift_characteristics_retract = (4000, 1000)
lift_front_fpid = (0, 0.8, 0.0, 0.0)
lift_back_fpid = lift_front_fpid
lift_front_retract_fpid = (0.0, 0.8, 0.0, 0.0)
lift_back_retract_fpid = lift_front_retract_fpid
