from wpilib.command import InstantCommand

import robotmap
import subsystems


class Shoot(InstantCommand):
    def __init__(self):
        super().__init__("Shoot")
        self.requires(subsystems._intake)

    def execute(self):
        subsystems._intake._talon.set(robotmap.spd_intake_shoot)
