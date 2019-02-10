from wpilib.command import InstantCommand

import subsystems


class Halt(InstantCommand):
    def __init__(self):
        super().__init__("Halt")

    def execute(self):
        subsystems._intake.stop()
