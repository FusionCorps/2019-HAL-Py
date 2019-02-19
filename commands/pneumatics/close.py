from wpilib.command import InstantCommand

import robotmap
import subsystems


class PneumaticsClose(InstantCommand):
    def __init__(self):
        super().__init__("PneumaticsClose")
        self.requires(subsystems._pneumatics)

    def execute(self):
        if robotmap.control_mode == 1:
            subsystems._pneumatics.set_state(0)
        else:
            pass

    def isFinished(self):
        if robotmap.control_mode == 0:
            return False
        if robotmap.control_mode == 1:
            return True

    def end(self):
        pass
