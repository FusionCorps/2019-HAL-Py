import logging

from ctre import WPI_TalonSRX
from wpilib import SpeedControllerGroup
from wpilib.command import Subsystem
from wpilib.drive import DifferentialDrive

import oi
import robotmap


class Chassis(Subsystem):

    def __init__(self):
        super().__init__('Chassis')
        self.logger = logging.getLogger("Chassis")

        # Motor objects
        _talon_FL = WPI_TalonSRX(robotmap.talon_front_left)
        _talon_FR = WPI_TalonSRX(robotmap.talon_front_right)
        _talon_BL = WPI_TalonSRX(robotmap.talon_back_left)
        _talon_BR = WPI_TalonSRX(robotmap.talon_back_right)

        # Speed Controller Groups
        _group_L = SpeedControllerGroup(_talon_BL, _talon_FL)
        _group_R = SpeedControllerGroup(_talon_BR, _talon_FR)

        # Drive class instance
        self._drive = DifferentialDrive(_group_L, _group_R)

    def initDefaultCommand(self):
        from commands import Joystick_Drive
        self.setDefaultCommand(Joystick_Drive())
