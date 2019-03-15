from wpilib import Timer
from wpilib.command import Command

import subsystems


class ChassisDrive(Command):
    def __init__(self, spd_x, spd_z=0.0, time=None):
        super().__init__("ChassisDrive")
        self.requires(subsystems._chassis)
        self.spd_x = spd_x
        self.spd_z = spd_z
        self.time = time
        if time is not None:
            self.timer = Timer()

    def initialize(self):
        if self.time is not None:
            self.timer.reset()
            self.timer.start()
        subsystems._chassis._drive.curvatureDrive(self.spd_x, self.spd_z, True)

    def execute(self):
        pass

    def interrupted(self):
        self.end()

    def isFinished(self):
        if self.time is not None:
            return self.timer.hasPeriodPassed(self.time)
        else:
            return False

    def end(self):
        self.timer.stop()
        self.timer.reset()
        subsystems._chassis._drive.curvatureDrive(0.0, 0.0, True)
