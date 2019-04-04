import logging

from wpilib.command import Command

import subsystems
from subsystems.sublift import Position


class LiftDrive(Command):
    """Drives front lift bottom motor"""
    def __init__(self, spd_new, time=None):
        super().__init__("LiftDrive", timeout=time)
        self.logger = logging.getLogger("LiftDrive")
        self.spd_new = spd_new

    def initialize(self):
        self.logger.warning("Starting")
        subsystems.lift.set_drive(self.spd_new)

    def execute(self):
        if not subsystems.lift.get_back_limit():
            subsystems.lift.stop_back()
        if not subsystems.lift.get_front_limit():
            subsystems.lift.stop_front()
        if subsystems.lift.get_back_limit():
            subsystems.lift.set_position(Position.CLIMB)

    def isFinished(self):
        return self.isTimedOut()

    def interrupted(self):
        self.logger.info("Interrupted")
        self.end()

    def end(self):
        subsystems.lift.set_drive(0.0)
        subsystems.lift.stop_back()
        self.logger.warning("Ending")


class LiftDrive2(Command):
    """Drives front lift bottom motor"""

    def __init__(self, spd_new, time=None):
        super().__init__("LiftDrive", timeout=time)
        self.logger = logging.getLogger("LiftDrive")
        self.spd_new = spd_new

    def initialize(self):
        self.logger.warning("Starting")
        subsystems.lift.set_drive(self.spd_new)

    def execute(self):
        if not subsystems.lift.get_back_limit():
            subsystems.lift.stop_back()
        if not subsystems.lift.get_front_limit():
            subsystems.lift.stop_front()
        # if subsystems.lift.get_back_limit():
        #     subsystems.lift.set_position(Position.CLIMB2)

    def isFinished(self):
        return self.isTimedOut()

    def interrupted(self):
        self.logger.info("Interrupted")
        self.end()

    def end(self):
        subsystems.lift.set_drive(0.0)
        subsystems.lift.stop_back()
        self.logger.warning("Ending")
