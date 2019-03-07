from enum import Enum

from ctre import VictorSPX
from wpilib.command import Subsystem

import robotmap


class IntakeState(Enum):
    HALT = 0.0
    INTAKING = robotmap.spd_intake
    EJECTING = -robotmap.spd_intake
    SHOOTING = robotmap.spd_intake_shoot


class Intake(Subsystem):
    def __init__(self):
        super().__init__("Intake")
        self._victor = VictorSPX(robotmap.talon_intake)

    def setVictor(self, spd_target):
        from ctre import ControlMode

        if self._victor.getMotorOutputPercent() is spd_target:
            pass
        else:
            self._victor.set(ControlMode.PercentOutput, demand0=spd_target)

    def setState(self, state_target):
        from ctre import ControlMode

        if state_target is not None:
            self._victor.set(ControlMode.PercentOutput, demand0=state_target)

    def initDefaultCommand(self):
        from commands.intake.intake_set import IntakeSet

        self.setDefaultCommand(IntakeSet(IntakeState.HALT))
