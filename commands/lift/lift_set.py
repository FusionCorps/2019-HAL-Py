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
            self.__class__.__name__ + "" + str(target_position), 0, sub=subsystems._lift
        )

    def initialize(self):
        subsystems._lift.talon_drive_CBack.setQuadraturePosition(0, 50)
        subsystems._lift.talon_drive_CFront.setQuadraturePosition(0, 50)
        subsystems._lift.setPosition(self.target_position)

    def execute(self):
        if self.target_position is Position.BOTH_UP:
            if abs(subsystems._lift.getBackPosition()) >= robotmap.lift_height:
                subsystems._lift.talon_drive_CBack.set(0.0)
            if abs(subsystems._lift.getFrontPosition()) >= robotmap.lift_height:
                subsystems._lift.talon_drive_CFront.set(0.0)
        elif self.target_position is Position.BOTH_DOWN:
            if not subsystems._lift.getFrontLimit():
                subsystems._lift.talon_drive_CFront.set(0.0)
                subsystems._lift.resetFrontEncoder()
            if not subsystems._lift.getBackLimit():
                subsystems._lift.talon_drive_CBack.set(0.0)
                subsystems._lift.resetBackEncoder()

    def isFinished(self):
        if self.target_position is Position.BOTH_UP:
            return (
                abs(subsystems._lift.getBackPosition()) >= robotmap.lift_height
                and abs(subsystems._lift.getFrontPosition()) >= robotmap.lift_height
            )
        elif self.target_position is Position.BOTH_DOWN:
            return (
                not subsystems._lift.getFrontLimit()
                and not subsystems._lift.getBackLimit()
            )
        elif self.target_position is Position.FRONT_UP:
            return abs(subsystems._lift.getFrontPosition()) >= robotmap.lift_height
        elif self.target_position is Position.BACK_UP:
            return abs(subsystems._lift.getBackPosition()) >= robotmap.lift_height
        elif self.target_position is Position.FRONT_DOWN:
            return not subsystems._lift.getFrontLimit()
        elif self.target_position is Position.BACK_DOWN:
            return not subsystems._lift.getBackLimit()
        elif self.target_position is Position.BOTH_HALT:
            return True

    def interrupted(self):
        self.end()

    def end(self):
        if self.target_position is Position.BOTH_UP:
            subsystems._lift.resetBackEncoder()
            subsystems._lift.resetFrontEncoder()
        elif self.target_position is Position.BOTH_DOWN:
            subsystems._lift.resetBackEncoder()
            subsystems._lift.resetFrontEncoder()
        elif self.target_position is Position.BACK_DOWN:
            pass
        subsystems._lift.setPosition(Position.BOTH_HALT)
