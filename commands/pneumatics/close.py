from wpilib.command import InstantCommand

import robotmap
import subsystems


class PneumaticsClose(InstantCommand):
    def __init__(self):
        super().__init__("PneumaticsClose")
        self.requires(subsystems._pneumatics)

    def execute(self):
        subsystems._pneumatics.set_state(0)
