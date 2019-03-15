import logging

import robotmap
import subsystems
from common.fusion_command import FusionCommand
from subsystems.lift import Position


class LiftSet(FusionCommand):
    def __init__(self, target_position):
        self.target_position = target_position
        self.logger = logging.getLogger("Lift")
        super().__init__(
            self.__class__.__name__ + str(target_position), 0, sub=subsystems._lift
        )

    def initialize(self):
        subsystems._lift.talon_drive_CBack.setQuadraturePosition(0, 50)
        subsystems._lift.talon_drive_CFront.setQuadraturePosition(0, 50)
        subsystems._lift.setPosition(self.target_position)
        self.logger.info("Position has been set to " + str(self.target_position))

    def execute(self):
        if self.target_position is Position.BOTH_UP:
            if (
                abs(subsystems._lift.talon_drive_CBack.getQuadraturePosition())
                >= robotmap.lift_height
                and abs(subsystems._lift.talon_drive_CFront.getQuadraturePosition())
                >= robotmap.lift_height
            ):
                self.logger.info("Encoder stopped lift movement")
                subsystems._lift.talon_drive_CBack.setQuadraturePosition(0, 50)
                subsystems._lift.talon_drive_CFront.setQuadraturePosition(0, 50)
                self.end()
            if (
                abs(subsystems._lift.talon_drive_CBack.getQuadraturePosition())
                >= robotmap.lift_height
            ):
                subsystems._lift.talon_drive_CBack.set(0.0)
            if (
                abs(subsystems._lift.talon_drive_CFront.getQuadraturePosition())
                >= robotmap.lift_height
            ):
                subsystems._lift.talon_drive_CFront.set(0.0)
        elif self.target_position is Position.BOTH_DOWN:
            if (
                not subsystems._lift.CFront_limit.get()
                and not subsystems._lift.CBack_limit.get()
            ):
                subsystems._lift.resetFrontEncoder()
                subsystems._lift.resetBackEncoder()
                self.end()
            if not subsystems._lift.CFront_limit.get():
                subsystems._lift.talon_drive_CFront.set(0.0)
                subsystems._lift.resetFrontEncoder()
            if not subsystems._lift.CBack_limit.get():
                subsystems._lift.talon_drive_CBack.set(0.0)
                subsystems._lift.resetBackEncoder()
        elif self.target_position is Position.FRONT_UP:
            if (
                abs(subsystems._lift.talon_drive_CFront.getQuadraturePosition())
                >= robotmap.lift_height
            ):
                self.end()
        elif self.target_position is Position.BACK_UP:
            if (
                abs(subsystems._lift.talon_drive_CBack.getQuadraturePosition())
                >= robotmap.lift_height
            ):
                self.end()
        elif self.target_position is Position.BACK_DOWN:
            pass
        elif self.target_position is Position.FRONT_DOWN:
            if not subsystems._lift.CBack_limit.get():
                self.end()
        elif self.target_position is Position.BOTH_HALT:
            self.end()

    def isFinished(self):
        if self.target_position is Position.BOTH_UP:
            return False
        elif self.target_position is Position.BOTH_DOWN:
            return (
                not subsystems._lift.CFront_limit.get()
                and not subsystems._lift.CBack_limit.get()
            )
        elif self.target_position is Position.BOTH_HALT:
            return True
        elif (
            self.target_position is Position.FRONT_UP
            or self.target_position is Position.BACK_UP
        ):
            return False
        if self.target_position is Position.BACK_DOWN:
            return not subsystems._lift.CBack_limit.get()

    def interrupted(self):
        self.end()

    def end(self):
        if self.target_position is Position.BOTH_DOWN:
            subsystems._lift.talon_drive_CBack.setQuadraturePosition(0, 50)
            subsystems._lift.talon_drive_CFront.setQuadraturePosition(0, 50)
        if self.target_position is Position.BACK_DOWN:
            self.logger.info(
                "Current lift command is " + str(subsystems._lift.getCurrentCommand())
            )
            self.logger.info("Stopping back down")
        subsystems._lift.setPosition(Position.BOTH_HALT)
