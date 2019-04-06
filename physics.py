from pyfrc.physics import motor_cfgs, tankmodel
from pyfrc.physics.units import units

import robotmap


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
            120 * units.lbs,  # robot mass
            10.71,  # drivetrain gear ratio
            2,  # motors per side
            26 * units.inch,  # robot wheelbase
            23 * units.inch + bumper_width * 2,  # robot width
            32 * units.inch + bumper_width * 2,  # robot length
            8 * units.inch,  # wheel diameter
        )
        # fmt: on

    @staticmethod
    def encode(item, tm_diff, rate=1.0, ticks=4096):
        """Updates encoder pos and velocity in simulation."""
        spd = int(ticks * rate * item["value"] * tm_diff)
        item["quad_position"] += spd
        item["quad_velocity"] = spd

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
        # Simulate lift system
        f_lift = hal_data["CAN"][2]
        b_lift = hal_data["CAN"][3]

        f_switch = hal_data["dio"][5]
        b_switch = hal_data["dio"][6]

        self.encode(f_lift, tm_diff, rate=3.0)
        self.encode(b_lift, tm_diff, rate=3.0)
        self.encode(l_motor, tm_diff)
        self.encode(r_motor, tm_diff)

        # gyro = hal_data["Spi"][0]

        x, y, angle = self.drivetrain.get_distance(
            l_motor["value"], r_motor["value"], tm_diff
        )
        self.physics_controller.distance_drive(x, y, angle)

        if abs(f_lift["quad_position"]) + 580 > robotmap.lift_height:
            f_switch["value"] = False
        else:
            f_switch["value"] = True
        if abs(b_lift["quad_position"]) + 580 > robotmap.lift_height:
            b_switch["value"] = False
        else:
            b_switch["value"] = True
