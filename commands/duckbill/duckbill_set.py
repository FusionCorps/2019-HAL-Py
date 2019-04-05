from wpilib.command import Command

import subsystems


class DuckbillSet(Command):
    def __init__(self, state_target, timeout=0):
        super().__init__(self.__class__.__name__, timeout=0)
        self.requires(subsystems.duckbill)
        self.state_target = state_target

    def initialize(self):
        subsystems.duckbill.set_state(self.state_target)

    def isFinished(self):
        return False

    def execute(self):
        pass

    def interrupted(self):
        self.end()

    def end(self):
        pass
