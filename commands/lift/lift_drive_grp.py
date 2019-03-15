import logging
from commands.lift.lift_back_alternate import LiftBackAlternate
from commands.lift.lift_drive import LiftDrive
from commands.lift.lift_set import LiftSet

from wpilib import Timer
from wpilib.command import CommandGroup

import subsystems
from subsystems.lift import Position


class LiftDriveGroup(CommandGroup):
    def __init__(self, time):
        super().__init__(self.__class__.__name__)
        self.time = time
        self.timer = Timer()
        self.logger = logging.getLogger("LiftDriveGroup")
        self.addSequential(LiftDrive(0.3, self.time))
        self.addParallel(LiftBackAlternate(self.time))

    def initialize(self):
        self.logger.info("LiftDriveGroup starting")
        self.timer.reset()
        self.timer.start()

    def execute(self):
        pass

    def isFinished(self):
        return self.timer.hasPeriodPassed(self.time + 1.0)

    def interrupted(self):
        self.end()

    def end(self):
        self.timer.stop()
        self.timer.reset()
        self.logger.info("LiftDriveGroup ending at " + str(self.timer.get()))
