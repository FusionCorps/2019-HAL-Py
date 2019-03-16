import logging

from wpilib.command import Command

import robotmap
import subsystems
from subsystems.lift import Position


class LiftSet(Command):
    def __init__(self, target_position):
        self.target_position = target_position
        self.logger = logging.getLogger("Lift")
        super().__init__(self.__class__.__name__ + "" + str(target_position))
        self.requires(subsystems._lift)

    def initialize(self):
        subsystems._lift.setPosition(self.target_position)

    def execute(self):
        if self.target_position is Position.BOTH_UP:
            pass
        elif self.target_position is Position.BOTH_DOWN:
            if not subsystems._lift.getFrontLimit():
                subsystems._lift.stopFront()
            if not subsystems._lift.getBackLimit():
                subsystems._lift.stopBack()

    def isFinished(self):
        if self.target_position is Position.BOTH_UP:
            return False
        elif self.target_position is Position.BOTH_DOWN:
            return (
                not subsystems._lift.getFrontLimit()
                and not subsystems._lift.getBackLimit()
            )
        elif self.target_position is Position.FRONT_DOWN:
            return not subsystems._lift.getFrontLimit()
        elif self.target_position is Position.BACK_DOWN:
            return not subsystems._lift.getBackLimit()

    def interrupted(self):
        self.logger.info(
            "("
            + self.target_position.name
            + " -> "
            + subsystems._lift.position_current.name
            + ") "
            + "Interrupted"
        )
        self.end()

    def end(self):
        if self.target_position is Position.BOTH_UP:
            pass
        elif self.target_position is Position.BOTH_DOWN:
            subsystems._lift.setFrontPosition(robotmap.lift_height)
            subsystems._lift.setBackPosition(robotmap.lift_height)
        elif self.target_position is Position.BACK_DOWN:
            pass
        elif self.target_position is Position.FRONT_DOWN:
            pass
