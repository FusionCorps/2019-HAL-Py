from wpilib.command import InstantCommand

import robotmap
import subsystems


class Halt(InstantCommand):
    def __init__(self):
        super().__init__("Halt")
        self.requires(subsystems._pneumatics)

    def execute(self):
        if robotmap.control_mode == 0:
            subsystems._pneumatics.halt()
        else:
            pass
