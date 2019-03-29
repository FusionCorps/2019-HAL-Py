import logging

from wpilib.command import Command

import subsystems
from subsystems.sublift import Position
from .lift_set import LiftSet


class LiftDrive(Command):
    def __init__(self, spd_new, time=None):
        super().__init__("LiftDrive", timeout=time)
        self.logger = logging.getLogger("LiftDrive")
        self.spd_new = spd_new
        self.lift_down = LiftSet(Position.BOTH_DOWN)

    def initialize(self):
        self.logger.warning("Lift is driving...")
        if subsystems.lift.position_current is not Position.BOTH_DOWN:
            self.logger.warning("The Lift is not Down!")
            self.end()
        subsystems.lift.set_drive(0.2)

    def execute(self):
        if subsystems.lift.get_back_limit() and subsystems.lift.get_back()[0] != 0.2:
            subsystems.lift.set_drive(0.2)
        elif not subsystems.lift.get_back_limit():
            subsystems.lift.stop_back()

    def isFinished(self):
        return self.isTimedOut()

    def interrupted(self):
        self.logger.info("Interrupted")
        self.end()

    def end(self):
        self.logger.warning("Ending")
        subsystems.lift.set_drive(0.0)
