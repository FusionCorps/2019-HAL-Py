from wpilib.command import Command

import subsystems


class PistonSet(Command):
    def __init__(self, state_target):
        super().__init__(self.__class__.__name__)
        self.requires(subsystems.piston)
        self.state_target = state_target

    def initialize(self):
        subsystems.piston.setState(self.state_target)

    def isFinished(self):
        return False

    def execute(self):
        pass

    def end(self):
        from subsystems.subpiston import StatePiston

        subsystems.piston.setState(StatePiston.IN)
