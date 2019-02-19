from ctre import WPI_TalonSRX
from wpilib.command import Subsystem

import robotmap


class Lift(Subsystem):
    def __init__(self):
        super().__init__("Lift")
        self.talon_drive_CFront = WPI_TalonSRX(robotmap.talon_lift_CFront)
        self.talon_drive_CBack = WPI_TalonSRX(robotmap.talon_lift_CBack)

    def resetEncoders(self):
        self.talon_drive_CBack.setQuadraturePosition(0, 50)
        self.talon_drive_CFront.setQuadraturePosition(0, 50)
