import logging
from commands.lift.lift_set import LiftSet

from wpilib import Timer
from wpilib.command import Command

import subsystems
from subsystems.lift import Position


class LiftBackAlternate(Command):
    def __init__(self, time):
        super().__init__("LiftBackAlternate")
        self.timer_internal = Timer()
        self.timer_to_end = Timer()
        self.time = time
        self.logger = logging.getLogger("Lift")
        self.lift_down = LiftSet(Position.BACK_DOWN)
        self.lift_halt = LiftSet(Position.BOTH_HALT)

    def initialize(self):
        self.logger.info("Starting LiftBackAlternate")
        self.timer_internal.reset()
        self.timer_to_end.reset()
        self.timer_internal.start()
        self.timer_to_end.start()

    def execute(self):
        if self.timer_internal.get() < 0.2 or (
            abs(subsystems._lift.talon_drive_CBack.getQuadraturePosition())
            < abs(subsystems._lift.talon_drive_CFront.getQuadraturePosition()) - 4096
        ):
            if not self.lift_down.isRunning():
                self.logger.info("Starting Down at " + str(self.timer_internal.get()))
                self.lift_down.start()
            elif self.lift_down.isRunning():
                pass
        elif self.timer_internal.get() >= 0.2 and self.timer_internal.get() < 0.5:
            if not self.lift_halt.isRunning():
                self.logger.info("Starting halt" + str(self.timer_internal.get()))
                self.lift_down.end()
                self.lift_halt.start()
            elif self.lift_halt.isRunning():
                pass
        elif self.timer_internal.get() >= 0.5:
            self.lift_halt.end()
            self.timer_internal.reset()

    def isFinished(self):
        return self.timer_to_end.hasPeriodPassed(self.time)

    def interrupted(self):
        self.logger.info("LiftBackAlternate was interrupted")
        self.end()

    def end(self):
        self.logger.info("Ending LiftBackAlternate")
        self.timer_internal.stop()
        self.timer_to_end.stop()
        self.timer_internal.reset()
        self.timer_to_end.reset()
