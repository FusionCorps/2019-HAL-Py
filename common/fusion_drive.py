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
        self.timer = Timer()

        self.logger = logging.getLogger("FusionDrive")

    @staticmethod
    def logistic(c, z, v, x):
        a = (c / v) - 1
        b = 4 * (z / c)
        f = (c / (1 + a * (pow(e, -b * x))))
        return f

    @staticmethod
    def shrink(value):
        """Used to shrink -1.0 to 1.0 range into a 0.0 to 1.0 range so that logistic calculations are manageable."""
        return (1 + value) / 2

    @staticmethod
    def expand(value):
        """Undoes shrink. Returns values in a range -1.0 to 1.0"""
        return (2 * value) - 1

    @staticmethod
    def normalize(value):
        if value > 1.0:
            return 1.0
        elif value < -1.0:
            return -1.0
        else:
            return value

    def get_logistic(self, spd_max, spd_current, time_step) -> float:
        """Returns results of logistic calculations from certain preconditions"""
        z = (robotmap.accel_chassis_max / 2)
        c = self.shrink(spd_max)
        v = self.shrink(spd_current)

        if c > v:
            return self.expand(self.logistic(c, z, v, time_step))
        elif c < v:
            return self.expand(-self.logistic(c, z, v, time_step) + 1)
        elif c == v:
            return self.expand(v)
        else:
            raise ValueError

    def logistic_drive(self, x_spd, z_rot, logistic_deadzone=0.2):
        current_time = self.timer.getFPGATimestamp()
        time_differential = current_time - self.adm_joystick_last_called

        if abs(x_spd) < 0:
            sign = -1
        else:
            sign = 1

        self.l_motor.set(
            sign * -(self.get_logistic(x_spd, sign * -self.l_motor.get(), time_differential) + z_rot))
        self.r_motor.set(
            sign * self.get_logistic(x_spd, sign * self.r_motor.get(), time_differential) - z_rot)

        self.feed()
        self.adm_joystick_last_called = self.timer.getFPGATimestamp()
