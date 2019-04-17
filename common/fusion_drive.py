import logging

from math import e, pow
from wpilib import Timer
from wpilib.drive import DifferentialDrive

import robotmap


class FusionDrive(DifferentialDrive):
    """Class that implements the logistic drive accelerated drivetrain."""

    def __init__(self, l_motor, r_motor):
        super().__init__(l_motor, r_motor)
        self.l_motor = l_motor
        self.r_motor = r_motor

        self.logistic_last_called = 0
        self.timer = Timer()  # Used to get current system time

        self.logger = logging.getLogger("FusionDrive")

    @staticmethod
    def calculate_logistic(c, z, v, x):
        """Logistic curve function used to calculate the next output speed. `c` and `v` must be shrunk beforehand.

        :param c: Speed target/max (0 to 1.0)
        :param z: Max acceleration (positive int)
        :param v: Current speed between 0 and 1.0
        :param x: Time delta since it was last called
        :return: The next speed value to be set based on the logistic curve
        """
        a = (c / v) - 1  # Determines the y-intercept
        b = 4 * (z / c)  # Determines the aggressiveness/max slope of the curve at the inflection point
        f = (c / (1 + a * (pow(e, -b * x))))  # Resultant logistic value
        return f

    @staticmethod
    def shrink(value):
        """Used to shrink -1.0 to 1.0 range into a 0.0 to 1.0 range so logistic calculations are manageable."""
        return (1 + value) / 2

    @staticmethod
    def expand(value):
        """Undoes shrink. Returns values in a range -1.0 to 1.0."""
        return (2 * value) - 1

    @staticmethod
    def normalize_spd(l_spd, r_spd):
        """Takes an expanded value and ensures it's within a -1.0 to 1.0 range."""
        left, right = l_spd, r_spd
        maximum = max(abs(left), abs(right))
        if maximum > 1.0:
            left = l_spd / maximum
            right = r_spd / maximum
        return round(left, 2), round(right, 2)

    @staticmethod
    def get_logistic(spd_max, spd_current, time_step) -> float:
        """Returns results of logistic calculations from certain preconditions"""

        z = (robotmap.chassis_max_acceleration / 2)  # Maximum accel must be divided by 2 because of shrinking
        c = FusionDrive.shrink(spd_max)
        v = FusionDrive.shrink(spd_current)

        # Cases for logistic curve calculations to satisfy
        if c > v:  # If spd_target > spd_current
            return FusionDrive.expand(FusionDrive.calculate_logistic(c, z, v, time_step))
        elif c < v:  # If spd_target < spd_current
            return FusionDrive.expand(-FusionDrive.calculate_logistic((1 - c), z, (1 - v), time_step) + 1)
        elif c == v:  # If they are equal, then the spd_target has been met
            return FusionDrive.expand(v)
        else:
            raise ValueError("Logistic acquisition edge case!")

    def logistic_drive(self, x_spd: float, z_rot: float, clear_accumulator: bool = False, multiply_by: bool = False):
        """Driving system that uses a logistic curve to accelerate/decelerate the drivetrain."""

        current_time = self.timer.getFPGATimestamp()
        time_differential = (current_time - self.logistic_last_called) if not clear_accumulator else 0.02

        if multiply_by:
            x_target = x_spd * robotmap.spd_chassis_drive
            z_target = z_rot * robotmap.spd_chassis_rotate
        else:
            x_target = x_spd
            z_target = z_rot

        l_output, r_output = FusionDrive.normalize_spd(x_target + z_target, x_target - z_target)

        self.set_left(FusionDrive.get_logistic(l_output, self.get_left(), time_differential))
        self.set_right(FusionDrive.get_logistic(r_output, self.get_right(), time_differential))

        self.logistic_last_called = self.timer.getFPGATimestamp()
        self.feed()

    def set_left(self, spd):
        """Sets left motor speed"""
        self.l_motor.set(-spd)

    def set_right(self, spd):
        """Sets right motor speed"""
        self.r_motor.set(spd)

    def get_left(self):
        """Returns left motor speed (-1.0 to 1.0)"""
        return -self.l_motor.get()

    def get_right(self):
        """Returns right motor speed (-1.0 to 1.0)"""
        return self.r_motor.get()

    def curvatureDrive(self, xSpeed: float, zRotation: float, isQuickTurn: bool = True,
                       multiply_by: bool = False) -> None:
        if multiply_by:
            super().curvatureDrive(xSpeed * robotmap.spd_chassis_drive, zRotation * robotmap.spd_chassis_rotate,
                                   isQuickTurn)
        else:
            super().curvatureDrive(xSpeed, zRotation, isQuickTurn)
