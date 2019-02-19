from wpilib import Timer
from wpilib.command import Command

import robotmap
import subsystems


class SlapperSlap(Command):
    def __init__(self):
        super().__init__("Slap")
        self.timer = Timer()
        if robotmap.control_mode == 1:
            self.requires(subsystems._slapper)
        else:
            pass

    def initialize(self):
        if robotmap.control_mode == 1:
            if subsystems._slapper.slapper.get() == robotmap.spd_slapper_slap:
                pass
            else:
                subsystems._slapper.slapper.set(robotmap.spd_slapper_slap)
        else:
            pass

    def execute(self):
        if self.timer.hasPeriodPassed(0.5):
            subsystems._slapper.slapper.set(0.0)
            self.end()

    def isFinished(self):
        if robotmap.control_mode == 1:
            if self.timer.hasPeriodPassed(0.5):
                return True
            else:
                return False
        elif robotmap.control_mode == 0:
            return True

    def interrupted(self):
        self.end()

    def end(self):
        self.timer.stop()
        self.timer.reset()
