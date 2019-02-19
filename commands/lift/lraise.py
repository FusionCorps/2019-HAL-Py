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
        # self.timer = Timer()

    def initialize(self):
        if robotmap.control_mode == 0:
            subsystems._lift.resetEncoders()
            if self.target == Position.DOWN:
                subsystems._lift.talon_drive_CBack.set(-0.6)
                subsystems._lift.talon_drive_CFront.set(-0.7)
            elif self.target == Position.UP:
                # self.timer.reset()
                # self.timer.start()
                subsystems._lift.talon_drive_CBack.set(0.4)
                subsystems._lift.talon_drive_CFront.set(0.4)
            elif self.target == Position.ZERO:
                subsystems._lift.talon_drive_CBack.set(0.0)
                subsystems._lift.talon_drive_CFront.set(0.0)
                self.end()
            # self.logger.info("Set target speed")
        else:
            self.end()

    def execute(self):
        # self.logger.info(
        #     "Target height is "
        #     + str(robotmap.lift_height)
        #     + ". Encoders report "
        #     + str(subsystems._lift.talon_drive_CBack.getPulseWidthPosition())
        # )

        if robotmap.control_mode == 0:
            # if (
            #     abs(subsystems._lift.talon_drive_CBack.getPulseWidthPosition())
            #     > self.targetHeight
            # ):
            #     subsystems._lift.talon_drive_CBack.set(0.0)
            # if (
            #     abs(subsystems._lift.talon_drive_CFront.getPulseWidthPosition())
            #     > self.targetHeight
            # ):
            #     subsystems._lift.talon_drive_CFront.set(0.0)
            if self.target == Position.UP:
                if not subsystems._lift.CFront_limit_bottom.get():
                    subsystems._lift.talon_drive_CBack.set(0.0)
                    subsystems._lift.talon_drive_CFront.set(0.0)
                    self.end()
                if not subsystems._lift.CBack_limit_bottom.get():
                    subsystems._lift.talon_drive_CBack.set(0.0)
                    subsystems._lift.talon_drive_CFront.set(0.0)
                    self.end()
            if self.target == Position.DOWN:
                if not subsystems._lift.CFront_limit_top.get():
                    subsystems._lift.talon_drive_CBack.set(0.0)
                    subsystems._lift.talon_drive_CFront.set(0.0)
                    self.end()
                if not subsystems._lift.CBack_limit_top.get():
                    subsystems._lift.talon_drive_CBack.set(0.0)
                    subsystems._lift.talon_drive_CFront.set(0.0)
                    self.end()
        else:
            self.end()

    def isFinished(self):
        if robotmap.control_mode == 0:
            # return (
            #     abs(subsystems._lift.talon_drive_CBack.getQuadraturePosition())
            #     > self.targetHeight
            #     and abs(subsystems._lift.talon_drive_CFront.getQuadraturePosition())
            #     > self.targetHeight
            # )
            return False
        else:
            return True

    def interrupted(self):
        self.end()

    def end(self):
        # self.timer.reset()
        subsystems._lift.talon_drive_CBack.set(0.0)
        subsystems._lift.talon_drive_CFront.set(0.0)
        subsystems._lift.resetEncoders()
