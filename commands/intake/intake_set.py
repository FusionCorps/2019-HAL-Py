from ctre import ControlMode
from wpilib.command import Command

import subsystems


class IntakeSet(Command):
    """
    Sets Intake State
    """

    def __init__(self, state_target):
        super().__init__(self.__class__.__name__)
        self.state_target = state_target
        self.requires(subsystems.intake)

    def initialize(self):
        subsystems.intake.set_victor(self.state_target.value)

    def isFinished(self):
        return False

    def interrupted(self):
        self.end()

    def end(self):
        subsystems.intake._victor.set(ControlMode.PercentOutput, 0.0)
