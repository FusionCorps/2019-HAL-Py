import subsystems
from common.fusion_command import FusionCommand


class DuckbillSet(FusionCommand):
    def __init__(self, state_target):
        super().__init__(self.__class__.__name__, 1, sub=subsystems._duckbill)
        self.state_target = state_target

    def initialize(self):
        subsystems._duckbill.setState(self.state_target)

    def isFinished(self):
        return False

    def execute(self):
        pass

    def end(self):
        pass
