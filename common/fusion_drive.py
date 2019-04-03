import logging

from math import e, pow
from wpilib import Timer
from wpilib.drive import DifferentialDrive

import robotmap


class FusionDrive(DifferentialDrive):
    def __init__(self, l_motor, r_motor):
        super().__init__(l_motor, r_motor)
        self.l_motor = l_motor
        self.r_motor = r_motor

        self.adm_joystick_last_called = 0
        self.timer = Timer()  # Used to get current system time

        self.logger = logging.getLogger("FusionDrive")

    @staticmethod
    def logistic(c, z, v, x):
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
        """Used to shrink -1.0 to 1.0 range into a 0.0 to 1.0 range so that logistic calculations are manageable."""
        return (1 + value) / 2

    @staticmethod
    def expand(value):
        """Undoes shrink. Returns values in a range -1.0 to 1.0."""
        return (2 * value) - 1

    @staticmethod
    def normalize_spd(l_spd, r_spd):
        """Takes an expanded value and ensures it's within a -1.0 to 1.0 range."""
        l, r = l_spd, r_spd
        maximum = max(abs(l), abs(r))
        if maximum > 1.0:
            l = l_spd / maximum
            r = r_spd / maximum
        return round(l, 2), round(r, 2)

    def get_logistic(self, spd_max, spd_current, time_step) -> float:
        """Returns results of logistic calculations from certain preconditions"""
        z = (robotmap.accel_chassis_max / 2)  # Maximum accel must be divided by 2 because of shrinking
        z_d = (robotmap.decel_chassis_max / 2)  # Unused variable for maximum deceleration
        c = self.shrink(spd_max)
        v = self.shrink(spd_current)

        # Cases for logistic curve calculations to satisfy
        if c > v:  # If spd_target > spd_current
            return self.expand(self.logistic(c, z, v, time_step))
        elif c < v:  # If spd_target < spd_current
            return self.expand(-self.logistic((1 - c), z, (1 - v), time_step) + 1)
        elif c == v:  # If they are equal, then the spd_target has been met
            return self.expand(v)
        else:
            raise ValueError

    def logistic_drive(self, x_spd, z_rot, logistic_deadzone=0.2):
        """Driving system that uses a logistic curve to accelerate/decelerate the drivetrain."""
        # if self.timer.running is False:
        #     self.timer.start()

        current_time = self.timer.getFPGATimestamp()
        time_differential = current_time - self.adm_joystick_last_called

        l_output, r_output = self.normalize_spd(x_spd + z_rot, x_spd - z_rot)

        # if self.timer.hasPeriodPassed(5):
        #     self.logger.info(
        #         f'Added (L {str(round(x_spd + z_rot, 2))} R {str(round(x_spd - z_rot, 2))}) Normalized (L {round(
        #         l_output, 2)} R {round(r_output, 2)})')

        self.set_left(self.get_logistic(l_output * robotmap.spd_chassis_drive, self.get_left(), time_differential))
        self.set_right(self.get_logistic(r_output * robotmap.spd_chassis_drive, self.get_right(), time_differential))

        self.feed()
        self.adm_joystick_last_called = self.timer.getFPGATimestamp()

    def set_left(self, spd):
        self.l_motor.set(-spd)

    def set_right(self, spd):
        self.r_motor.set(spd)

    def get_left(self):
        return -self.l_motor.get()

    def get_right(self):
        return self.r_motor.get()
