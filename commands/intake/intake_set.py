from ctre import ControlMode

import robotmap
import subsystems
from common.fusion_command import FusionCommand
from subsystems.intake import StateIntake


class IntakeSet(FusionCommand):
    """
    Sets Intake State
    """

    def __init__(self, state_target):
        super().__init__(self.__class__.__name__, 1, sub=subsystems._intake)
        self.state_target = state_target

    def initialize(self):
        subsystems._intake.setVictor(self.state_target.value)

    def isFinished(self):
        return False

    def interrupted(self):
        self.end()

    def end(self):
        subsystems._intake._victor.set(ControlMode.PercentOutput, 0.0)
