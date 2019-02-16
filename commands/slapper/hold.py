from wpilib import Timer
from wpilib.command import InstantCommand

import robotmap
import subsystems


class SlapperHold(InstantCommand):
    def __init__(self):
        super().__init__("SlapperHold")
        self.requires(subsystems._slapper)
        self.timer = Timer()
        self.error = robotmap.slapper_error

    def initialize(self):
        self.timer.reset()
        self.timer.start()

    def execute(self):
        if (
            subsystems._slapper.slapper.getQuadraturePosition()
            < robotmap.slapper_hold_position
        ):
            pass
        elif (
            subsystems._slapper.slapper.getQuadraturePosition()
            >= robotmap.slapper_hold_position
        ):
            pass

    def interrupted(self):
        self.end()

    def isFinished(self):
        return False

    def end(self):
        self.timer.stop()
        self.timer.reset()
