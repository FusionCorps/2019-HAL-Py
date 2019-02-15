from wpilib import Timer
from wpilib.command import Command

import robotmap
import subsystems


class GrpEject(Command):
    def __init__(self):
        super().__init__("GrpEject")
        from commands import Extend, Halt, Retract

        self.requires(subsystems._pneumatics)
        self.timer = Timer()

        self.extend = Extend()
        self.retract = Retract()
        self.halt = Halt(0)

        self.is_finished = False

    def initialize(self):
        self.is_finished = False
        self.timer.start()

    def execute(self):
        if not self.timer.hasPeriodPassed(0.5):
            self.retract.start()
        elif self.timer.hasPeriodPassed(0.5) and not self.timer.hasPeriodPassed(1):
            self.halt.start()
        elif self.timer.hasPeriodPassed(1):
            self.is_finished = True
            self.end()

    def isFinished(self):
        return self.is_finished

    def interrupted(self):
        self.end()

    def end(self):
        self.is_finished = False
        self.timer.stop()
        self.timer.reset()
