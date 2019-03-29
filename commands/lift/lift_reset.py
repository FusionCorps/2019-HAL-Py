import logging

from wpilib.command import Command

import robotmap
import subsystems


class LiftReset(Command):
    def __init__(self, target=1):
        super().__init__("LiftReset")
        self.requires(subsystems.lift)
        self.logger = logging.getLogger("LiftReset")
        self.target = target

    def initialize(self):
        self.logger.warning("Lift is driving up to reset")
        if self.target is 1:
            subsystems.lift.set_back(-robotmap.spd_lift_back, target=1)
        elif self.target is 0:
            subsystems.lift.set_front(-robotmap.spd_lift_front, target=1)

    def execute(self):
        pass

    def isFinished(self):
        return False

    def interrupted(self):
        self.end()

    def end(self):
        subsystems.lift.stop_front()
        subsystems.lift.stop_back()
        subsystems.lift.reset_encoders()
        self.logger.warning("Lift has stopped driving up, encoders reset")
