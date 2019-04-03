import logging

from math import e, pow
from wpilib import Timer
from wpilib.drive import DifferentialDrive


class FusionDrive(DifferentialDrive):
    def __init__(self, l_motor, r_motor):
        super().__init__(l_motor, r_motor)
        self.l_motor = l_motor
        self.r_motor = r_motor

        self.adm_joystick_last_called = 0
        self.timer = Timer()

        self.logger = logging.getLogger("FusionDrive")

    @staticmethod
    def calculate_logistic(c, z, v, x, offset=0):
        a = (c / v) - 1
        b = 4 * (z / c)
        f = (c / (1 + a * (pow(e, -b * x))))
        return f

    def get_logistic_output(self, spd_max, spd_current, time_step) -> float:
        z = 3
        c = spd_max

        if c < 0:
            c *= -1
            v = spd_current
            if v < 0:
                v *= -1
                return -self.calculate_logistic(c, z, v, time_step)
            elif v == 0:
                v = 0.01
                return -self.calculate_logistic(c, z, v, time_step)
            elif v > 0:
                return -self.calculate_logistic((c + (2 * v)), z, v, time_step) + (2 * v)
            else:
                return 0.0
        elif c > 0:
            v = spd_current
            if v < 0:
                return self.calculate_logistic((c + (2 * v)), z, v, time_step) - (2 * v)
            elif v == 0:
                v = 0.01
                return self.calculate_logistic(c, z, v, time_step)
            elif v > 0:
                return self.calculate_logistic(c, z, v, time_step)
            else:
                return 0.0
        else:
            return 0.0

    @staticmethod
    def normalize(value):
        if value > 1.0:
            return 1.0
        elif value < -1.0:
            return -1.0
        else:
            return value

    def logistic_drive(self, x_spd, z_rot, logistic_deadzone=0.2):
        current_time = self.timer.getFPGATimestamp()
        time_differential = current_time - self.adm_joystick_last_called

        # l_target = self.limit(x_spd + z_rot)
        # r_target = self.limit(x_spd - z_rot)

        if abs(x_spd) <= logistic_deadzone:
            self.l_motor.set(-(x_spd + z_rot))
        else:
            self.l_motor.set(-(self.get_logistic_output(x_spd, -self.l_motor.get(), time_differential) + z_rot))

        if abs(x_spd) <= logistic_deadzone:
            self.r_motor.set(x_spd - z_rot)
        else:
            self.r_motor.set(self.get_logistic_output(x_spd, self.r_motor.get(), time_differential) - z_rot)

        self.feed()
        self.adm_joystick_last_called = self.timer.getFPGATimestamp()
