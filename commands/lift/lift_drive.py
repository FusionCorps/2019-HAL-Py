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
        subsystems.lift.set_drive(self.spd_new)
        if subsystems.lift.position_current != Position.BOTH_DOWN:
            self.logger.warning("The Lift is not Down!")
            self.cancel()

    def execute(self):
        if not subsystems.lift.get_back_limit():
            subsystems.lift.stop_back()
        if not subsystems.lift.get_front_limit():
            subsystems.lift.stop_front()
        if subsystems.lift.get_back_limit():
            subsystems.lift.set_position(Position.BOTH_DOWN)

    def isFinished(self):
        return self.isTimedOut()

    def interrupted(self):
        self.logger.info("Interrupted")
        self.end()

    def end(self):
        subsystems.lift.set_drive(0.0)
        subsystems.lift.stop_back()
        self.logger.warning("Ending")
