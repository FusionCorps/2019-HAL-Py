from enum import Enum

from ctre import WPI_TalonSRX
from wpilib import DigitalInput
from wpilib.command import Subsystem

import robotmap


class Position(Enum):
    """
    Sets position speeds based on (back, front) value
    """

    BOTH_DOWN = (robotmap.spd_lift_cback, robotmap.spd_lift_cfront)
    BOTH_UP = (-robotmap.spd_lift_up, -robotmap.spd_lift_up)
    BOTH_HALT = (0.0, 0.0)
    FRONT_UP = (0.0, -robotmap.spd_lift_cfront)
    FRONT_DOWN = (0.0, robotmap.spd_lift_cfront)
    BACK_UP = (-robotmap.spd_lift_cback, 0.0)
    BACK_DOWN = (robotmap.spd_lift_cback, 0.0)


class Lift(Subsystem):
    def __init__(self):
        super().__init__("Lift")
        self.talon_drive_CFront = WPI_TalonSRX(robotmap.talon_lift_CFront)
        self.talon_drive_CBack = WPI_TalonSRX(robotmap.talon_lift_CBack)
        self.talon_drive_CDRive = WPI_TalonSRX(robotmap.talon_lift_CDrive)
        self.CFront_limit = DigitalInput(robotmap.lift_cfront_limit_top)
        self.CBack_limit = DigitalInput(robotmap.lift_cback_limit_top)
        self.resetEncoders()
        self.setPosition(Position.BOTH_HALT)

    def setPosition(self, position_target):
        if position_target is not None:
            self.talon_drive_CBack.set(position_target.value[0])
            self.talon_drive_CFront.set(position_target.value[1])
        else:
            pass

        self.state = position_target

    def getState(self):
        return self.state

    def resetFrontEncoder(self):
        self.talon_drive_CFront.setQuadraturePosition(0, 50)

    def resetBackEncoder(self):
        self.talon_drive_CBack.setQuadraturePosition(0, 50)

    def resetEncoders(self):
        self.talon_drive_CBack.setQuadraturePosition(0, 50)
        self.talon_drive_CFront.setQuadraturePosition(0, 50)

    def setCDrive(self, spd):
        self.talon_drive_CDRive.set(spd)

    # def initDefaultCommand(self):
    #     from commands.lift.lift_set import LiftSet

    #     self.setDefaultCommand(LiftSet(Position.BOTH_HALT))
