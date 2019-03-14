from enum import Enum

from ctre import ControlMode, VictorSPX
from wpilib.command import Subsystem

import robotmap


class StateIntake(Enum):
    """
    Enum that stores the Victor speed values for each state
    """

    HALT = 0.0
    INTAKING = robotmap.spd_intake
    EJECTING = -robotmap.spd_intake
    SHOOTING = robotmap.spd_intake_shoot


class Intake(Subsystem):
    def __init__(self):
        super().__init__("Intake")
        self._victor = VictorSPX(robotmap.talon_intake)
        self.setState(StateIntake.HALT)

    def setVictor(self, spd_target, mode=ControlMode.PercentOutput):
        """
        Sets Intake Victor speed controller speed (uses PercentOutput as default)
        """
        if self._victor.getMotorOutputPercent() is spd_target:
            pass
        else:
            self._victor.set(mode, spd_target)

    def setState(self, state_target):
        """
        Sets the state of the Intake subsystem using the IntakeState Enum.

        `state_target` is the IntakeState Enum value to set (e.g. `INTAKING`)
        """
        if (
            state_target is not None
            and self._victor.getMotorOutputPercent() is not state_target.value
        ):
            self.setVictor(state_target.value, mode=ControlMode.PercentOutput)
        elif state_target is None:
            pass

        self.state = state_target

    def getState(self):
        return self.state
