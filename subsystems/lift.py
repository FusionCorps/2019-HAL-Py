from enum import Enum

from ctre import WPI_TalonSRX
from wpilib import DigitalInput
from wpilib.command import Subsystem

import robotmap


class Position(Enum):
    """
    Sets position speeds based on (back, front) value
    """

    BOTH_UP = (robotmap.spd_lift_cback, robotmap.spd_lift_cfront)
    BOTH_DOWN = (-robotmap.spd_lift_cback, -robotmap.spd_lift_cfront)
    BOTH_HALT = (0.0, 0.0)
    FRONT_UP = (0.0, robotmap.spd_lift_cfront)


class Lift(Subsystem):
    def __init__(self):
        super().__init__("Lift")
        self.talon_drive_CFront = WPI_TalonSRX(robotmap.talon_lift_CFront)
        self.talon_drive_CBack = WPI_TalonSRX(robotmap.talon_lift_CBack)
        self.CFront_limit = DigitalInput(robotmap.lift_cfront_limit_top)
        self.CBack_limit = DigitalInput(robotmap.lift_cback_limit_top)
        self.resetEncoders()

    def setPosition(self, position_target):
        if position_target is not None:
            self.talon_drive_CBack.set(position_target.value[0])
            self.talon_drive_CFront.set(position_target.value[1])
        else:
            pass

    def resetFrontEncoder(self):
        self.talon_drive_CFront.setQuadraturePosition(0, 50)

    def resetBackEncoder(self):
        self.talon_drive_CBack.setQuadraturePosition(0, 50)

    def resetEncoders(self):
        self.talon_drive_CBack.setQuadraturePosition(0, 50)
        self.talon_drive_CFront.setQuadraturePosition(0, 50)
