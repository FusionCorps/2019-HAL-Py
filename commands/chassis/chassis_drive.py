import logging

from wpilib import Timer
from wpilib.command import Command

import subsystems


class ChassisDrive(Command):
    def __init__(self, spd_x, spd_z=0.0, time=None):
        super().__init__("ChassisDrive")
        self.requires(subsystems._chassis)
        self.logger = logging.getLogger("ChassisDrive")
        self.spd_x = spd_x
        self.spd_z = spd_z
        if time is None:
            self.timeout = 1000
        else:
            self.timeout = time

    def initialize(self):
        self.logger.info("Starting")
        subsystems._chassis._drive.curvatureDrive(self.spd_x, self.spd_z, True)

    def execute(self):
        pass

    def interrupted(self):
        self.logger.info("Interrupted")
        self.end()

    def isFinished(self):
        return self.isTimedOut()

    def end(self):
        self.logger.info("Ending")
        subsystems._chassis._drive.curvatureDrive(0.0, 0.0, True)
