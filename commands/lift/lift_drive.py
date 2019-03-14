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
        self.back_alternate = LiftBackAlternate()

    def initialize(self):
        self.timer.reset()
        self.timer.start()
        subsystems._lift.setCDrive(self.spd_new)
        self.back_alternate.start()

    def execute(self):
        if self.timer.hasPeriodPassed(self.time):
            self.end()
        else:
            pass

    def isFinished(self):
        return self.timer.hasPeriodPassed(self.time)

    def interrupted(self):
        self.end()

    def end(self):
        self.timer.stop()
        self.back_alternate.end()
        subsystems._lift.setCDrive(0.0)
