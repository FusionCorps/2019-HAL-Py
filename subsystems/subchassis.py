import logging

from ctre import WPI_TalonSRX
from wpilib import ADXRS450_Gyro, BuiltInAccelerometer, SpeedControllerGroup, Ultrasonic
from wpilib.command import Subsystem
from wpilib.drive import DifferentialDrive

import oi
import robotmap


class SubChassis(Subsystem):
    def __init__(self):
        super().__init__("Chassis")
        self.logger = logging.getLogger("Chassis")

        self._talon_FL = WPI_TalonSRX(robotmap.talon_front_left)
        self._talon_FR = WPI_TalonSRX(robotmap.talon_front_right)
        self._talon_BL = WPI_TalonSRX(robotmap.talon_back_left)
        self._talon_BR = WPI_TalonSRX(robotmap.talon_back_right)
        self._talons = [self._talon_FL, self._talon_FR, self._talon_BL, self._talon_BR]

        for talon in self._talons:
            # 17 ft/sec
            talon.configMotionCruiseVelocity(30000, 0)
            talon.configMotionAcceleration(1000, 0)

            talon.config_kP(0, 0.2, 0)
            talon.config_kI(0, 0.2, 0)
            talon.config_kD(0, 0.2, 0)
            talon.config_kF(0, 0.05, 0)
            talon.config_IntegralZone(0, 0.025, 0)

            talon.configPeakOutputForward(1.0, 0)
            talon.configPeakOutputReverse(-1.0, 0)

            talon.set(0.0)
            talon.setSafetyEnabled(False)

        # Speed Controller Groups
        self._group_L = SpeedControllerGroup(self._talon_BL, self._talon_FL)
        self._group_R = SpeedControllerGroup(self._talon_BR, self._talon_FR)

        # Drive class instance
        self.drive = DifferentialDrive(self._group_L, self._group_R)

        # Sensors
        self.ultrasonic = Ultrasonic(
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
        self.ultrasonic.setEnabled(state)
        if state is True:
            self.ultrasonic.setAutomaticMode(True)
        elif state is False:
            self.ultrasonic.setAutomaticMode(False)

    def get_distance(self):
        """Gets Ultrasonic distance in mm"""
        return self.ultrasonic.getRangeMM()

    def joystick_drive(self):
        self.drive.curvatureDrive(
            -(oi.joystick.getRawAxis(1)) * robotmap.spd_chassis_drive,
            oi.joystick.getRawAxis(4) * robotmap.spd_chassis_rotate,
            True,
        )

    def initDefaultCommand(self):
        from commands.joystick_drive import JoystickDrive

        self.setDefaultCommand(JoystickDrive())
