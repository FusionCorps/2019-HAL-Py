import logging

from wpilib import Timer
from wpilib.command import Command

import subsystems


class LiftDrive(Command):
    def __init__(self, spd_new, time):
        from commands.lift.lift_back_alternate import LiftBackAlternate

        super().__init__("LiftDrive")
        self.spd_new = spd_new
        self.timer = Timer()
        self.time = time
        self.logger = logging.getLogger("LiftDrive")

    def initialize(self):
        self.timer.reset()
        self.timer.start()
        subsystems._lift.setCDrive(self.spd_new)

    def execute(self):
        pass

    def isFinished(self):
        return self.timer.hasPeriodPassed(self.time)

    def interrupted(self):
        self.end()

    def end(self):
        self.logger.info("Ending LiftDrive")
        self.timer.stop()
        self.timer.reset()
        subsystems._lift.setCDrive(0.0)
