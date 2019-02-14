from wpilib.command import InstantCommand

import subsystems


class Halt(InstantCommand):
    def __init__(self):
        super().__init__("Halt")
        self.requires(subsystems._pneumatics)

    def execute(self):
        subsystems._pneumatics.halt()
