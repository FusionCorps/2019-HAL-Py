from wpilib.command import Command

import robotmap
import subsystems


class PneumaticsPiston(Command):
    def __init__(self):
        super().__init__("PneumaticsPiston")
        if robotmap.control_mode == 1:
            self.requires(subsystems._pneumatics)
        else:
            pass

    def execute(self):
        if robotmap.control_mode == 1:
            subsystems._pneumatics.set_state(2)
        else:
            self.end()

    def isFinished(self):
        if robotmap.control_mode == 1:
            return False
        elif robotmap.control_mode == 0:
            return True

    def interrupted(self):
        self.end()

    def end(self):
        pass
