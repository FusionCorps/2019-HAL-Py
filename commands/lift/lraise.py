import logging

from wpilib import Timer
from wpilib.command import Command

import robotmap
import subsystems
from subsystems.lift import Position


class SetLift(Command):
    def __init__(self, target):
        super().__init__("Lift Raise " + str(target))
        self.requires(subsystems._lift)
        self.target = target
        self.targetHeight = robotmap.lift_height
        self.logger = logging.getLogger("SetLift")
        self.timer = Timer()

    def initialize(self):
        if robotmap.control_mode == 0:
            subsystems._lift.resetEncoders()
            if self.target == Position.DOWN:
                self.timer.reset()
                self.timer.start()
                subsystems._lift.talon_drive_CBack.set(robotmap.spd_lift_cback)
                subsystems._lift.talon_drive_CFront.set(robotmap.spd_lift_cfront)
            elif self.target == Position.UP:
                self.timer.reset()
                self.timer.start()
                subsystems._lift.talon_drive_CBack.set(0.4)
                subsystems._lift.talon_drive_CFront.set(0.4)
            elif self.target == Position.ZERO:
                subsystems._lift.talon_drive_CBack.set(0.0)
                subsystems._lift.talon_drive_CFront.set(0.0)
                self.end()
        else:
            self.end()

    def execute(self):
        if robotmap.control_mode == 0:
            if self.target == Position.UP and self.timer.hasPeriodPassed(1):
                if not subsystems._lift.CFront_limit.get():
                    subsystems._lift.talon_drive_CFront.set(0.0)
                    self.end()
                if not subsystems._lift.CBack_limit.get():
                    subsystems._lift.talon_drive_CBack.set(0.0)
                    self.end()
            if self.target == Position.DOWN and self.timer.hasPeriodPassed(1):
                if not subsystems._lift.CFront_limit.get():
                    subsystems._lift.talon_drive_CFront.set(0.0)
                    self.end()
                if not subsystems._lift.CBack_limit.get():
                    subsystems._lift.talon_drive_CBack.set(0.0)
                    self.end()
        else:
            self.end()

    def isFinished(self):
        if robotmap.control_mode == 0:
            return False
        else:
            return True

    def interrupted(self):
        self.end()

    def end(self):
        subsystems._lift.resetEncoders()
