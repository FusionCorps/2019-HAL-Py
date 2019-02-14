from wpilib.command import InstantCommand

import subsystems


class Retract(InstantCommand):
    def __init__(self):
        super().__init__("Retract")
        self.requires(subsystems._pneumatics)

    def execute(self):
        subsystems._pneumatics.retract()
