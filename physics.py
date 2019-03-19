from pyfrc.physics import motor_cfgs, tankmodel
from pyfrc.physics.units import units


class PhysicsEngine(object):
    """
        Simulates a motor moving something that strikes two limit switches,
        one on each end of the track. Obviously, this is not particularly
        realistic, but it's good enough to illustrate the point
    """

    def __init__(self, physics_controller):
        """
            :param physics_controller: `pyfrc.physics.core.PhysicsInterface` object
                                       to communicate simulation effects to
        """

        self.physics_controller = physics_controller
        self.position = 0

        # Change these parameters to fit your robot!
        bumper_width = 3.25 * units.inch

        # fmt: off
        self.drivetrain = tankmodel.TankModel.theory(
            motor_cfgs.MOTOR_CFG_CIM,  # motor configuration
            110 * units.lbs,  # robot mass
            10.71,  # drivetrain gear ratio
            2,  # motors per side
            26 * units.inch,  # robot wheelbase
            23 * units.inch + bumper_width * 2,  # robot width
            32 * units.inch + bumper_width * 2,  # robot length
            8 * units.inch,  # wheel diameter
        )
        # fmt: on

    def update_sim(self, hal_data, now, tm_diff):
        """
            Called when the simulation parameters for the program need to be
            updated.
            
            :param now: The current time as a float
            :param tm_diff: The amount of time that has passed since the last
                            time that this function was called
        """

        # Simulate the drivetrain
        l_motor = hal_data["CAN"][21]
        r_motor = hal_data["CAN"][11]
        f_lift = hal_data["CAN"][2]
        b_lift = hal_data["CAN"][3]

        spd_f = int(4096 * 4 * f_lift["value"] * tm_diff)
        spd_b = int(4096 * 4 * b_lift["value"] * tm_diff)

        f_lift["quad_position"] += spd_f
        f_lift["quad_velocity"] = spd_f
        b_lift["quad_position"] += spd_b
        b_lift["quad_velocity"] = spd_f

        gyro = hal_data["Spi"][0]

        x, y, angle = self.drivetrain.get_distance(
            l_motor["value"], r_motor["value"], tm_diff
        )
        self.physics_controller.distance_drive(x, y, angle)

        # update position (use tm_diff so the rate is constant)
        # self.position += hal_data["pwm"][4]["value"] * tm_diff * 3

        # update limit switches based on position
        # if self.position <= 0:
        #     switch1 = True
        #     switch2 = False

        # elif self.position > 10:
        #     switch1 = False
        #     switch2 = True

        # else:
        #     switch1 = False
        #     switch2 = False

        # set values here
        # hal_data["dio"][1]["value"] = switch1
        # hal_data["dio"][2]["value"] = switch2

        # hal_data["analog_in"][2]["voltage"] = self.position
