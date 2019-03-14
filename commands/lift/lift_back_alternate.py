import logging
from commands.lift.lift_set import LiftSet

from wpilib import Timer
from wpilib.command import Command

import subsystems
from subsystems.lift import Position


class LiftBackAlternate(Command):
    def __init__(self):
        super().__init__("LiftBackAlternate")
        self.timer = Timer()
        self.logger = logging.getLogger("Lift")

    def initialize(self):
        self.timer.reset()
        self.timer.start()

    def execute(self):
        if self.timer.hasPeriodPassed(5.0) or (
            abs(subsystems._lift.talon_drive_CBack.getQuadraturePosition())
            < abs(subsystems._lift.talon_drive_CFront.getQuadraturePosition()) - 4096
        ):
            self.logger.info("Starting downward drive")
            LiftSet(Position.BACK_DOWN).start()
            self.timer.reset()
        elif self.timer.hasPeriodPassed(0.5):
            self.logger.info("Starting halt" + str(self.timer.get()))
            LiftSet(Position.BOTH_HALT).start()

    def isFinished(self):
        return False

    def interrupted(self):
        self.end()

    def end(self):
        self.timer.stop()
        self.timer.reset()
        subsystems._lift.setPosition(Position.BOTH_HALT)
