from wpilib.command import InstantCommand

import subsystems


class IntakeHalt(InstantCommand):
    def __init__(self):
        super().__init__("IntakeHalt")

    def execute(self):
        subsystems._intake._talon.set(0.0)
