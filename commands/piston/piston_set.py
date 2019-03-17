from wpilib.command import Command

import subsystems


class PistonSet(Command):
    def __init__(self, state_target):
        super().__init__(self.__class__.__name__)
        self.requires(subsystems._piston)
        self.state_target = state_target

    def initialize(self):
        subsystems._piston.setState(self.state_target)

    def isFinished(self):
        return False

    def execute(self):
        pass

    def end(self):
        from subsystems.piston import StatePiston

        subsystems._piston.setState(StatePiston.IN)
