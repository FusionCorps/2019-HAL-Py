import logging

from ctre import WPI_TalonSRX
from wpilib import ADXRS450_Gyro, BuiltInAccelerometer, Timer, Ultrasonic
from wpilib.command import Subsystem

import robotmap
from common.fusion_drive import FusionDrive


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
            talon.configMotionCruiseVelocity(
                (robotmap.chassis_max_vel / robotmap.chassis_whl_diameter) * robotmap.chassis_encoder_counts_per_rev, 0)
            talon.configMotionAcceleration(
                (robotmap.chassis_max_vel / robotmap.chassis_whl_diameter) * robotmap.chassis_encoder_counts_per_rev, 0)

            talon.config_kF(0, robotmap.chassis_fpid[0], 0)
            talon.config_kP(0, robotmap.chassis_fpid[1], 0)
            talon.config_kI(0, robotmap.chassis_fpid[2], 0)
            talon.config_kD(0, robotmap.chassis_fpid[3], 0)
            talon.config_IntegralZone(0, 0, 0)

            talon.configPeakOutputForward(1.0, 0)
            talon.configPeakOutputReverse(-1.0, 0)

            talon.set(0.0)

        # Drive class instance & following
        self.drive = FusionDrive(self._talon_FL, self._talon_FR)
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

        self.timer = Timer()

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

    def get_left_position(self, target=0):
        if target == 0:
            return self._talon_FL.getQuadraturePosition()
        elif target == 1:
            return self._talon_FL.getPulseWidthPosition()

    def get_right_position(self, target=0):
        if target == 0:
            return self._talon_FR.getQuadraturePosition()
        elif target == 1:
            return self._talon_FR.getPulseWidthPosition()

    def reset_encoders(self):
        """Sets all talon quadrature encoders to 0"""
        for talon in self._talons:
            talon.setQuadraturePosition(0, 20)

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

    def initDefaultCommand(self):
        from commands.chassis.joystick_drive import JoystickDrive

        self.setDefaultCommand(JoystickDrive())
