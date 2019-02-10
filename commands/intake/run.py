from wpilib.command import InstantCommand

import subsystems


class Run(InstantCommand):
    def __init__(self):
        super().__init__("Run")

    def execute(self):
        subsystems._intake.intake()
