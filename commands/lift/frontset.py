import logging

from wpilib import Timer
from wpilib.command import Command

import robotmap
import subsystems
from subsystems.lift import Position


class FrontSet(Command):
    def __init__(self, target, target_spd=None):
        super().__init__("BackSet")
        self.target = target
        self.requires(subsystems._lift)
        self.target_height = robotmap.lift_height
        self.logger = logging.getLogger("BackSet")
        self.target_spd = target_spd
        self.timer = Timer()

    def initialize(self):
        subsystems._lift.resetEncoders()
        self.timer.reset()
        self.timer.start()
        if robotmap.control_mode == 0:
            if self.target == Position.DOWN:
                subsystems._lift.talon_drive_CFront.set(-0.6)
            elif self.target == Position.UP:
                subsystems._lift.talon_drive_CFront.set(0.4)
            elif self.target == Position.ZERO:
                subsystems._lift.talon_drive_CFront.set(0.0)
                self.end()
        else:
            pass

    def execute(self):
        if robotmap.control_mode == 0:
            # if (
            #     subsystems._lift.talon_drive_CBack.getPulseWidthPosition()
            #     > self.target_height
            # ):
            #     self.logger.info(
            #         "Back encoders report "
            #         + str(subsystems._lift.talon_drive_CBack.getPulseWidthPosition())
            #     )
            #     subsystems._lift.talon_drive_CBack.set(0.0)
            #     self.end()
            # else:
            #     pass
            if self.target == Position.DOWN and not subsystems._lift.CFront_limit.get():
                subsystems._lift.talon_drive_CFront.set(0.0)
                self.end()
            elif self.target == Position.UP and self.timer.hasPeriodPassed(2):
                subsystems._lift.talon_drive_CFront.set(0.0)
                self.end()
            else:
                self.end()
        else:
            self.end()

    def isFinished(self):
        # return (
        #     subsystems._lift.talon_drive_CBack.getPulseWidthPosition()
        #     > self.target_height
        # )
        return False

    def interrupted(self):
        self.end()

    def end(self):
        self.timer.stop()
        self.timer.reset()
        subsystems._lift.resetEncoders()
