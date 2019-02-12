from wpilib.command import InstantCommand

import robotmap
import subsystems


class IntakeIntake(InstantCommand):
    def __init__(self):
        super().__init__("IntakeIntake")

    def execute(self):
        subsystems._intake._talon.set(robotmap.spd_intake)
