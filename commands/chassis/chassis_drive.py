from wpilib import Timer
from wpilib.command import Command

import subsystems


class ChassisDrive(Command):
    def __init__(self, spd_x, spd_z, time):
        super().__init__("ChassisDrive")
        self.requires(subsystems._chassis)
        self.spd_x = spd_x
        self.spd_z = spd_z
        if time is None:
            pass
        else:
            self.timer = Timer()
            self.time = time

    def initialize(self):
        if self.time is not None:
            self.timer.reset()
            self.timer.start()
        subsystems._chassis._drive.curvatureDrive(self.spd_x, self.spd_z, True)

    def execute(self):
        if self.time is not None:
            if self.timer.hasPeriodPassed(self.time):
                self.end()
        else:
            pass

    def interrupted(self):
        self.end()

    def isFinished(self):
        return False

    def end(self):
        subsystems._chassis._drive.curvatureDrive(0.0, 0.0, True)
