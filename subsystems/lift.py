from enum import Enum

from ctre import WPI_TalonSRX
from wpilib import DigitalInput
from wpilib.command import Subsystem

import robotmap


class Position(Enum):
    UP = "up"
    DOWN = "down"
    ZERO = "zero"


class Lift(Subsystem):
    def __init__(self):
        super().__init__("Lift")
        self.talon_drive_CFront = WPI_TalonSRX(robotmap.talon_lift_CFront)
        self.talon_drive_CBack = WPI_TalonSRX(robotmap.talon_lift_CBack)
        self.resetEncoders()

        self.CFront_limit_top = DigitalInput(robotmap.lift_cfront_limit_top)
        self.CFront_limit_bottom = DigitalInput(robotmap.lift_cfront_limit_bottom)
        self.CBack_limit_top = DigitalInput(robotmap.lift_cback_limit_top)
        self.CBack_limit_bottom = DigitalInput(robotmap.lift_cback_limit_bottom)

    def resetEncoders(self):
        self.talon_drive_CBack.setPulseWidthPosition(0, 50)
        self.talon_drive_CFront.setPulseWidthPosition(0, 50)
