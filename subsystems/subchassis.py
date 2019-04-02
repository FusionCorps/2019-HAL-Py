import logging

from ctre import WPI_TalonSRX
from math import e, pow
from wpilib import ADXRS450_Gyro, BuiltInAccelerometer, Timer, Ultrasonic
from wpilib.command import Subsystem
from wpilib.drive import DifferentialDrive

import robotmap


class SubChassis(Subsystem):
    """Chassis Subsystem for drivetrain, etc."""

    def __init__(self):
        super().__init__("Chassis")
        self.logger = logging.getLogger("Chassis")

        self._talon_FL = WPI_TalonSRX(robotmap.talon_front_left)
        self._talon_FR = WPI_TalonSRX(robotmap.talon_front_right)
        self._talon_BL = WPI_TalonSRX(robotmap.talon_back_left)
        self._talon_BR = WPI_TalonSRX(robotmap.talon_back_right)

        self._talons = [self._talon_FL, self._talon_FR, self._talon_BL, self._talon_BR]

        for talon in self._talons:
            talon.configMotionCruiseVelocity(30000, 0)
            talon.configMotionAcceleration(1000, 0)

            talon.config_kP(0, 0.8, 0)
            talon.config_kI(0, 0, 0)
            talon.config_kD(0, 0, 0)
            talon.config_kF(0, 0, 0)
            talon.config_IntegralZone(0, 0, 0)

            talon.configPeakOutputForward(1.0, 0)
            talon.configPeakOutputReverse(-1.0, 0)

            talon.set(0.0)

        # Drive class instance & following
        self.drive = DifferentialDrive(self._talon_FL, self._talon_FR)
        self._talon_BL.follow(self._talon_FL)
        self._talon_BR.follow(self._talon_FR)

        # Sensors
        self.sonar = Ultrasonic(
            robotmap.ultrasonic_ping,
            robotmap.ultrasonic_echo,
            Ultrasonic.Unit.kMillimeters,
        )

        self.accelerometer_internal = BuiltInAccelerometer(
            BuiltInAccelerometer.Range.k4G
        )
        self.accel_x, self.accel_y, self.accel_z = None, None, None
        self.reset_accelerometer()

        self.gyro = ADXRS450_Gyro(robotmap.gyro)

        if robotmap.chassis_zero_acceleration_on_start:
            self.gyro.calibrate()

        self.accel_rate_l = 0.0
        self.accel_rate_r = 0.0

        self.l_output = 0.0
        self.r_output = 0.0

        self.jerk_rate = 0.05

        self.timer = Timer()
        self.last_called = 0

    def get_x(self):
        """Returns relative x position"""
        return self.accel_x - self._get_x()

    def get_y(self):
        """Returns relative y position"""
        return self.accel_y - self._get_y()

    def get_z(self):
        """Returns relative z position"""
        return self.accel_z - self._get_z()

    def _get_x(self):
        """Internal method that returns the accelerometer x position"""
        return self.accelerometer_internal.getX()

    def _get_y(self):
        """Internal method that returns the accelerometer y position"""
        return self.accelerometer_internal.getY()

    def _get_z(self):
        """Internal method that returns the accelerometer z position"""
        return self.accelerometer_internal.getZ()

    def reset_encoders(self):
        """Sets all talon quadrature encoders to 0"""
        for talon in self._talons:
            talon.setQuadraturePosition(0, 50)

    def reset_gyro(self):
        """Zeroes the gyro"""
        self.gyro.reset()

    def reset_accelerometer(self):
        """Zeroes all accelerometer values"""
        self.accel_x = self._get_x()
        self.accel_y = self._get_y()
        self.accel_z = self._get_z()

    def set_ultrasonic(self, state):
        """Sets Ultrasonic state"""
        self.sonar.setEnabled(state)

    def set_left(self, spd_new):
        self._talon_FL.set(-spd_new)

    def set_right(self, spd_new):
        self._talon_FR.set(spd_new)

    def get_distance(self):
        """Gets Ultrasonic distance in MM"""
        return self.sonar.getRangeMM()

    def joystick_drive(self):
        # # r determines the agressiveness/shape of the curve
        # # theta determines the speed of the curve
        # # b is the fixed chassis width
        # # l and r spd must be from -1.0 to 1.0
        # # acceleration as fixed constant applied to current spd - target spd
        #
        current_time = self.timer.getFPGATimestamp()
        time_differential = current_time - self.last_called

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

        # Uses set_left and set_right methods to output
        self.set_left(self.calculate_logistic_curve(1.0, -self._talon_FL.get() + 0.01,
                                                    time_differential))  # Current spd is negated b/c left side
        # output is inverted
        self.set_right(self.calculate_logistic_curve(1.0, self._talon_FR.get() + 0.01, time_differential))
        self.last_called = self.timer.getFPGATimestamp()

    @staticmethod
    def calculate_logistic_curve(spd_max, spd_current, time_step):
        # TODO Finish equations to find b based on spd_target and spd_current
        a = (spd_max / spd_current) - 1  # Starting velocity used as logistic variable
        b = 1  # Aggressiveness of curve
        f = (spd_max / (1 + a * (pow(e, -b * time_step))))  # Resultant velocity output to motors
        # i = ((log(a) / b), (v_max / 2))

        return f

    @staticmethod
    def normalize(value):
        if value > 1.0:
            return 1.0
        elif value < -1.0:
            return -1.0
        else:
            return value

    def initDefaultCommand(self):
        from commands.chassis.joystick_drive import JoystickDrive

        self.setDefaultCommand(JoystickDrive())
