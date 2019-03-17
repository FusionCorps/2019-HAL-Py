from ctre import ControlMode
from wpilib.command import Command

import robotmap
import subsystems
from subsystems.intake import StateIntake


class IntakeSet(Command):
    """
    Sets Intake State
    """

    def __init__(self, state_target):
        super().__init__(self.__class__.__name__)
        self.state_target = state_target
        self.requires(subsystems._intake)

    def initialize(self):
        subsystems._intake.setVictor(self.state_target.value)

    def isFinished(self):
        return False

    def interrupted(self):
        self.end()

    def end(self):
        subsystems._intake._victor.set(ControlMode.PercentOutput, 0.0)
