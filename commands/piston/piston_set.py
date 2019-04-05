from wpilib.command import Command

import subsystems


class PistonSet(Command):
    def __init__(self, state_target):
        super().__init__(self.__class__.__name__)
        self.requires(subsystems.piston)
        self.state_target = state_target

    def initialize(self):
        subsystems.piston.set_state(self.state_target)

    def execute(self):
        pass

    def isFinished(self):
        return self.isTimedOut()

    def interrupted(self):
        self.end()

    def end(self):
        from subsystems.subpiston import StatePiston

        subsystems.piston.set_state(StatePiston.IN)
