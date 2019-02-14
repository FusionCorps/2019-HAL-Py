from wpilib.command import Command

import robotmap
import subsystems


class Retract(Command):
    def __init__(self):
        super().__init__("Retract")
        self.requires(subsystems._pneumatics)

    def execute(self):
        if robotmap.control_mode == 0:
            subsystems._pneumatics.retract()

    def isFinished(self):
        return False

    def interrupted(self):
        self.end()

    def end(self):
        pass
