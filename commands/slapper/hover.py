from wpilib import Timer
from wpilib.command import Command

import robotmap
import subsystems


class SlapperHover(Command):
    def __init__(self):
        super().__init__("SlapperHover")
        self.timer = Timer()
        if robotmap.control_mode == 1:
            self.requires(subsystems._slapper)
        else:
            pass

    def initialize(self):
        if robotmap.control_mode == 1:
            self.timer.reset()
            self.timer.start()
            subsystems._slapper.slapper.set(robotmap.spd_slapper_slap)
        else:
            pass

    def execute(self):
        if robotmap.control_mode == 1:
            if self.timer.hasPeriodPassed(0.2):
                if subsystems._slapper.slapper.get() == robotmap.spd_slapper_hold:
                    pass
                else:
                    subsystems._slapper.slapper.set(robotmap.spd_slapper_hold)
        else:
            pass

    def isFinished(self):
        return False

    def interrupted(self):
        self.end()

    def end(self):
        self.timer.stop()
        self.timer.reset()
