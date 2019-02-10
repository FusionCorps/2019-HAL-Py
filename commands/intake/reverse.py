from wpilib.command import InstantCommand

import subsystems


class Reverse(InstantCommand):
    def __init__(self):
        super().__init__("Reverse")

    def execute(self):
        subsystems._intake.reverse()
