"""
Stores all important robot variables. All units in metric.
"""

# Speed Controller port IDs
talon_f_l = 20
talon_f_r = 11
talon_b_l = 21
talon_b_r = 10

talon_intake = 1

talon_lift_drive = 30
talon_lift_front = 2
talon_lift_back = 3

# Solenoid Port IDs
solenoid_piston_b = 0
solenoid_piston_t = 1
solenoid_piston_l = 2
solenoid_piston_r = 3

# Sensor Port IDs
ultrasonic_ping = 21
ultrasonic_echo = 22
gyro = 0

# Joystick Port
joystick = 0

# Speed Constants
spd_chassis_drive = 0.55  # Arbitrary chassis speed multiplier
spd_chassis_rotate = 0.4  # ''
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
chassis_max_vel = 5.0  # (m/s) maximum chassis velocity used for profile generation
chassis_max_acceleration = 5.0  # (m/s^2) maximum chassis acceleration used for profile generation
chassis_max_jerk = 1.0  # (m/s^3) maximum chassis jerk used for profile generation
chassis_whl_diameter = 0.2032  # (m) drivetrain wheel diameter
chassis_encoder_counts_per_rev = 4096
chassis_zero_acceleration_on_start = True
chassis_fpid = (0.0, 0.8, 0.0, 0.0)
chassis_drive_mode = 'Curvature'  # Determines whether to joystick_drive in logistic or curvature mode

# Lift constants
lift_height = 22000  # Hab 3 height (encoder ticks)
lift_height_2 = 9000  # Hab 2 height (encoder ticks)
lift_front_limit = 5  # Front limit switch port
lift_back_limit = 6  # Back limit switch port
lift_characteristics = (800, 100)  # MotionMagic (v_max, a_max) values for extending lift racks
lift_characteristics_retract = (4000, 1000)  # MotionMagic (v_max, a_max) values for retracting lift racks
lift_front_fpid = (0, 0.8, 0.0, 0.0)  # FPID values for use in MotionMagic extension
lift_front_retract_fpid = (0.0, 0.8, 0.0, 0.0)  # FPID values for use in MotionMagic retraction
lift_back_fpid = lift_front_fpid
lift_back_retract_fpid = lift_front_retract_fpid

# Hal simulation conditions
simulation_lift_target = 0  # Used to test individual lift setting commands (0 for Hab 3, 1 for Hab 2)
