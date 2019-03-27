import logging

from wpilib.command import Command

import robotmap
import subsystems


class LiftReset(Command):
    def __init__(self):
        super().__init__("LiftReset")
        self.requires(subsystems.lift)
        self.logger = logging.getLogger("LiftReset")

    def initialize(self):
        subsystems.lift.set_front(-robotmap.spd_lift_front)
        subsystems.lift.set_back(robotmap.spd_lift_back)

    def execute(self):
        pass

    def isFinished(self):
        return not subsystems.lift.get_front_limit() and not subsystems.lift.get_back_limit()

    def interrupted(self):
        self.end()

    def end(self):
        subsystems.lift.stop_front()
        subsystems.lift.stop_back()
        subsystems.lift.reset_encoders()
