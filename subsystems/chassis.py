import logging

from ctre import ControlMode, WPI_TalonSRX
from wpilib import ADXRS450_Gyro, BuiltInAccelerometer, SpeedControllerGroup, Ultrasonic
from wpilib.command import Subsystem
from wpilib.drive import DifferentialDrive

import oi
import robotmap


class Chassis(Subsystem):
    def __init__(self):
        super().__init__("Chassis")
        self.logger = logging.getLogger("Chassis")

        # Motor objects
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
        self._drive = DifferentialDrive(self._group_L, self._group_R)

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
        self.resetAccelerometer()

        self.gyro = ADXRS450_Gyro(robotmap.gyro)

        if robotmap.chassis_zero_accel_on_start:
            self.gyro.calibrate()

    def getX(self):
        return self.accel_x

    def getY(self):
        return self.accel_y

    def getZ(self):
        return self.accel_z

    def _getX(self):
        return self.accelerometer_internal.getX()

    def _getY(self):
        return self.accelerometer_internal.getY()

    def _getZ(self):
        return self.accelerometer_internal.getZ()

    def resetEncoders(self):
        """
        Sets quadrature position to 0
        """
        for talon in self._talons:
            talon.setQuadraturePosition(0, 50)

    def resetGyro(self):
        self.gyro.reset()

    def resetAccelerometer(self):
        self.accel_x = self._getX()
        self.accel_y = self._getY()
        self.accel_z = self._getZ()

    def setUltrasonic(self, state):
        """
        Sets Ultrasonic state
        """
        self.sonar.setEnabled(True)

    def getDistance(self):
        """
        Gets Ultrasonic distance in MM
        """
        return self.sonar.getRangeMM()

    def joystickDrive(self):
        self._drive.curvatureDrive(
            -(oi.joystick.getRawAxis(1)) * robotmap.spd_chassis_drive,
            oi.joystick.getRawAxis(4) * robotmap.spd_chassis_rotate,
            True,
        )
        # self.PIDDrive()

    def PIDDrive(self):
        self._talon_FL.set(
            ControlMode.MotionMagic,
            (self.getZOutput(0.8) + self.getXOutput(0.8)) * 30000,
        )
        self._talon_FR.set(
            ControlMode.MotionMagic,
            (self.getZOutput(0.8) - self.getXOutput(0.8)) * 30000,
        )
        self._talon_BL.follow(self._talon_FL)
        self._talon_BR.follow(self._talon_FR)

    def getXOutput(self, spd_limit, deadband=0.2):
        if -(oi.joystick.getRawAxis(1)) * robotmap.spd_chassis_drive < deadband:
            return 0.0
        else:
            return -(oi.joystick.getRawAxis(1)) * robotmap.spd_chassis_drive

    def getZOutput(self, spd_limit, deadband=0.2):
        return oi.joystick.getRawAxis(4) * robotmap.spd_chassis_rotate

    def initDefaultCommand(self):
        from commands.joystick_drive import JoystickDrive

        self.setDefaultCommand(JoystickDrive())
