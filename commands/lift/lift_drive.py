import logging
from commands.lift.lift_set import LiftSet

from wpilib.command import Command

import robotmap
import subsystems
from subsystems.lift import Position


class LiftDrive(Command):
    def __init__(self, spd_new, time=None):
        super().__init__("LiftDrive", timeout=time)
        self.logger = logging.getLogger("LiftDrive")
        self.spd_new = spd_new
        self.lift_down = LiftSet(Position.BACK_DOWN)

    def initialize(self):
        subsystems._lift.resetEncoders()
        subsystems._lift.setDrive(self.spd_new)

    def execute(self):
        # if (
        #     subsystems._lift.getBackPosition()
        #     < (subsystems._lift.getFrontPosition() - 100)
        #     or subsystems._lift.getBackLimit()
        # ):
        #     self.logger.info("Compensating for tilt")
        #     self.lift_down.start()
        pass

    def isFinished(self):
        return self.isTimedOut()

    def interrupted(self):
        self.logger.info("Interrupted")
        self.end()

    def end(self):
        self.logger.info("Ending")
        subsystems._lift.setDrive(0.0)
