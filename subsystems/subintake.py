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


class SubIntake(Subsystem):
    """Subsystem used to intake and eject cargo"""

    def __init__(self):
        super().__init__("Intake")
        self._victor = VictorSPX(robotmap.talon_intake)
        self.state = None
        self.set_state(StateIntake.HALT)

    def set_victor(self, spd_target: float, mode: ControlMode = ControlMode.PercentOutput):
        """Sets Intake Victor speed (uses PercentOutput as default mode)"""
        self._victor.set(mode, -spd_target)

    def set_state(self, state_target: StateIntake):
        """Sets the state of the Intake subsystem using the IntakeState Enum.
        Parameters
        ---
        `state_target`: (IntakeState) Value to set (e.g. `INTAKING`)"""
        if state_target is not None and self.get_state() is not state_target:
            self.set_victor(state_target.value, mode=ControlMode.PercentOutput)
        else:
            pass

    def get_state(self) -> StateIntake:
        """Returns current IntakeState"""
        for name, value in StateIntake.__members__.items():
            if self._victor.getMotorOutputPercent() == value.value:
                return value
        raise LookupError

    def initDefaultCommand(self):
        from commands.intake.intake_joystick import IntakeJoystick

        self.setDefaultCommand(IntakeJoystick())
