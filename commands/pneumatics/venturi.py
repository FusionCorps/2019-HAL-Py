from wpilib.command import Command

import robotmap
import subsystems


class PneumaticsVenturi(Command):
    def __init__(self):
        super().__init__("PneumaticsVenturi")
        self.requires(subsystems._pneumatics)

    def execute(self):
        subsystems._pneumatics.set_state(1)

    def isFinished(self):
        return False

    def interrupted(self):
        self.end()

    def end(self):
        pass
