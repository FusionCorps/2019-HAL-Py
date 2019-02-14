from wpilib.command import InstantCommand

import subsystems


class Extend(InstantCommand):
    def __init__(self):
        super().__init__("Extend")
        self.requires(subsystems._pneumatics)

    def execute(self):
        subsystems._pneumatics.extend()
