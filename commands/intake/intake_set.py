from ctre import ControlMode

import robotmap
import subsystems
from common.fusion_command import FusionCommand
from subsystems.intake import IntakeState


class IntakeSet(FusionCommand):
    """
    Sets Intake State (Control Mode 1)
    """

    def __init__(self, state_target):
        super().__init__(self.__class__.__name__, 1, sub=subsystems._intake)
        self.state_target = state_target

    def initialize(self):
        subsystems._intake.setState(self.state_target)

    def isFinished(self):
        return False

    def interrupted(self):
        self.end()

    def end(self):
        pass
