from math import e, log, pow
from wpilib import Timer
from wpilib.drive import DifferentialDrive


class FusionDrive(DifferentialDrive):
    def __init__(self, l_motor, r_motor):
        super().__init__(l_motor, r_motor)
        self.l_motor = l_motor
        self.r_motor = r_motor

        self.adm_joystick_last_called = 0
        self.timer = Timer()

    @staticmethod
    def calculate_logistic_curve(spd_max, spd_current, time_step):
        # TODO Finish equations to find b based on spd_target and spd_current
        a = (spd_max / spd_current) - 1  # Starting velocity used as logistic variable
        b = 1  # Aggressiveness of curve
        f = (spd_max / (1 + a * (pow(e, (-b) * time_step))))  # Resultant velocity output to motors

        if not (abs(a) > 0):  # Input for log cannot be zero
            i = ((log(a) / b), (spd_max / 2))  # TODO Use inflection point in future calculations
        else:
            i = 0

        return f

    @staticmethod
    def normalize(value):
        if value > 1.0:
            return 1.0
        elif value < -1.0:
            return -1.0
        else:
            return value

    def logistic_drive(self, x_spd, z_rot):
        # # r determines the agressiveness/shape of the curve
        # # theta determines the speed of the curve
        # # b is the fixed chassis width
        # # l and r spd must be from -1.0 to 1.0
        # # acceleration as fixed constant applied to current spd - target spd
        #
        current_time = self.timer.getFPGATimestamp()
        time_differential = current_time - self.adm_joystick_last_called

        #
        # x_spd = -oi.joystick.getRawAxis(1)
        # z_rot = oi.joystick.getRawAxis(4)
        #
        # l_current = self._talon_FL.get()
        # l_spd_target = self.normalize(x_spd + z_rot)
        # if l_current != l_spd_target:
        #     if l_spd_target < 0:
        #         pass
        #     elif l_spd_target > 0:
        #         pass
        #     else:
        #         pass
        #
        # r_current = self._talon_FR.get()
        # r_spd_target = self.normalize(x_spd - z_rot)
        # if r_current != l_spd_target:
        #     if r_spd_target < 0:
        #         pass
        #     elif r_spd_target > 0:
        #         pass
        #     else:
        #         pass
        #
        # # return l_spd, r_spd
        # # l_output, r_output = self.calculate_wheel_outputs(-oi.joystick.getRawAxis(1), oi.joystick.getRawAxis(4))
        # # self.drive.curvatureDrive(
        # #     l_output,
        # #     r_output,
        # #     True,
        # # )
        #
        # self._talon_FL.set(-self.l_output)
        # self._talon_FR.set(self.r_output)
        #

        # TODO Replace fixed 0.01 "jumpstart" value with variable magnitude based on spd_target and spd_current
        # Uses set_left and set_right methods to output
        # self.set_left(self.calculate_logistic_curve(1.0, -self._talon_FL.get() + 0.01,
        #                                             time_differential))  # Current spd is negated b/c left side
        # # output is inverted
        # self.set_right(self.calculate_logistic_curve(1.0, self._talon_FR.get() + 0.01, time_differential))
        self.adm_joystick_last_called = self.timer.getFPGATimestamp()
