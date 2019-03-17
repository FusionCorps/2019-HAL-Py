from wpilib.command import Command

import subsystems


class DuckbillSet(Command):
    def __init__(self, state_target):
        super().__init__(self.__class__.__name__)
        self.requires(subsystems._duckbill)
        self.state_target = state_target

    def initialize(self):
        subsystems._duckbill.setState(self.state_target)

    def isFinished(self):
        return False

    def execute(self):
        pass

    def interrupted(self):
        self.end()

    def end(self):
        pass
