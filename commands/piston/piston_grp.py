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
        if self.step == 0 and self.timer.hasPeriodPassed(0.1):
            subsystems.duckbill.set_state(StateDuckbill.DOWN)
            self.step = 1
        elif self.step == 1 and self.timer.hasPeriodPassed(1.0):
            subsystems.duckbill.set_state(StateDuckbill.UP)
            self.step = 2

    def isFinished(self):
        return self.step == 2

    def interrupted(self):
        self.end()

    def end(self):
        subsystems.piston.set_state(StatePiston.IN)
        self.step = 0
        self.timer.stop()
