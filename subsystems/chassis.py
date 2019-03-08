import logging

from ctre import WPI_TalonSRX
from wpilib import ADXRS450_Gyro, SpeedControllerGroup, Ultrasonic
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
            talon.setSafetyEnabled(False)
            # talon.changeMotionControlFramePeriod(10)

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

        self.gyro = ADXRS450_Gyro(robotmap.gyro)

    def resetEncoders(self):
        """
        Sets quadrature position to 0
        """
        for talon in self._talons:
            talon.setQuadraturePosition(0, 50)

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
            -(oi.joystick.getRawAxis(1)), oi.joystick.getRawAxis(4), True
        )

    def initDefaultCommand(self):
        from commands.joystick_drive import JoystickDrive

        self.setDefaultCommand(JoystickDrive())
