import logging

from wpilib.command import Command

import subsystems
from subsystems.sublift import Position


class LiftDrive(Command):
    def __init__(self, spd_new, time=None):
        super().__init__("LiftDrive", timeout=time)
        self.logger = logging.getLogger("LiftDrive")
        self.spd_new = spd_new

    def initialize(self):
        self.logger.warning("Lift is driving...")
        if subsystems.lift.position_current is not Position.BOTH_DOWN:
            self.logger.warning("The Lift is not Down!")
            self.end()
        subsystems.lift.set_drive(self.spd_new)

    def execute(self):
        pass

    def isFinished(self):
        return self.isTimedOut()

    def interrupted(self):
        self.logger.info("Interrupted")
        self.end()

    def end(self):
        self.logger.warning("Ending")
        subsystems.lift.set_drive(0.0)
