import logging

from wpilib.command import Command

import subsystems


class ChassisDrive(Command):
    def __init__(self, spd_x, spd_z=0.0, time=None):
        super().__init__("ChassisDrive", timeout=time)
        self.requires(subsystems.chassis)
        self.logger = logging.getLogger("ChassisDrive")
        self.spd_x = spd_x
        self.spd_z = spd_z

    def initialize(self):
        self.logger.warning("Starting")
        subsystems.chassis.drive.curvatureDrive(self.spd_x, self.spd_z, True)

    def execute(self):
        pass

    def interrupted(self):
        self.logger.warning("Interrupted")
        self.end()

    def isFinished(self):
        return self.isTimedOut()

    def end(self):
        self.logger.warning("Ending")
        subsystems.chassis.drive.curvatureDrive(0.0, 0.0, True)
