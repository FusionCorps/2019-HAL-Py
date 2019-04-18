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
        self.logger.info("Starting")

    def execute(self):
        subsystems.chassis.drive.logistic_drive(-self.spd_x, self.spd_z, clear_accumulator=True)

    def interrupted(self):
        self.logger.info("Interrupted")
        self.end()

    def isFinished(self):
        return self.isTimedOut()

    def end(self):
        self.logger.info("Ending")
        subsystems.chassis.drive.stopMotor()
