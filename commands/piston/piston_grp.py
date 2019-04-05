from wpilib import Timer
from wpilib.command import Command

import subsystems
from subsystems.subduckbill import StateDuckbill
from subsystems.subpiston import StatePiston


class PistonGrp(Command):
    def __init__(self):
        super().__init__("PistonGrp")
        self.requires(subsystems.duckbill)
        self.requires(subsystems.piston)
        self.step = 0
        self.timer = Timer()

    def initialize(self):
        self.timer.reset()
        self.timer.start()
        subsystems.piston.set_state(StatePiston.OUT)

    def execute(self):
        if not self.step == 5:
            if self.step == 0 and self.timer.hasPeriodPassed(0.1):
                subsystems.duckbill.set_state(StateDuckbill.DOWN)
                self.step = 1
            elif self.step == 1 and self.timer.hasPeriodPassed(1.0):
                subsystems.piston.set_state(StatePiston.IN)
                self.step = 2
            elif self.step == 2 and self.timer.hasPeriodPassed(1.5):
                self.step = 3
        else:
            pass

    def isFinished(self):
        return self.step == 3

    def interrupted(self):
        self.end()

    def end(self):
        # subsystems.duckbill.set_state(StateDuckbill.UP)
        subsystems.piston.set_state(StatePiston.IN)
        self.step = 0
        self.timer.stop()
