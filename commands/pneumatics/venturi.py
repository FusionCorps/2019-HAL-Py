from wpilib.command import Command

import robotmap
import subsystems


class PneumaticsVenturi(Command):
    def __init__(self):
        super().__init__("PneumaticsVenturi")
        if robotmap.control_mode == 1:
            self.requires(subsystems._pneumatics)
        else:
            pass

    def execute(self):
        if robotmap.control_mode == 1:
            subsystems._pneumatics.set_state(1)
        else:
            self.end()

    def isFinished(self):
        return False

    def interrupted(self):
        self.end()

    def end(self):
        pass
