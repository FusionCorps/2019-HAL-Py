import logging

from wpilib import Timer
from wpilib.command import Command

import robotmap
import subsystems


class SlapperRaise(Command):
    def __init__(self):
        super().__init__("Slap")
        self.timer = Timer()
        self.logger = logging.getLogger("Slapper Raise")
        self.requires(subsystems._slapper)

    def initialize(self):
        self.timer.reset()
        self.timer.start()
        if robotmap.control_mode == 1:
            if subsystems._slapper.slapper.get() == robotmap.spd_slapper_raise1:
                pass
            else:
                subsystems._slapper.slapper.set(robotmap.spd_slapper_raise1)
        else:
            self.end()

    def execute(self):
        if robotmap.control_mode == 1:
            if not subsystems._slapper.limit_switch.get():
                subsystems._slapper.slapper.set(0.0)
                self.end()
            elif subsystems._slapper.limit_switch.get():
                if self.timer.hasPeriodPassed(0.6):
                    if subsystems._slapper.slapper.get() == robotmap.spd_slapper_raise2:
                        pass
                    else:
                        self.logger.info("Setting slapper to stage 2")
                        subsystems._slapper.slapper.set(robotmap.spd_slapper_raise2)
                        self.logger.info(
                            "Speed is now " + str(subsystems._slapper.slapper.get())
                        )
                else:
                    pass
        else:
            self.end()

    def isFinished(self):
        return False

    def interrupted(self):
        self.end()

    def end(self):
        self.timer.stop()
        self.timer.reset()
