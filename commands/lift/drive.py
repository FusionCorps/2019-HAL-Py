from wpilib.command import InstantCommand

import subsystems


class LiftDrive(InstantCommand):
    def __init__(self, target):
        super().__init__("Lift Drive " + str(target))
        self.requires(subsystems._lift)
        self.target = target

    def initialize(self):
        pass
