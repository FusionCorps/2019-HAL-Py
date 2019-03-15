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

    def initialize(self):
        subsystems._lift.resetEncoders()
        subsystems._lift.setPosition(self.target_position)

    def execute(self):
        if self.target_position is Position.BOTH_UP:
            # Check if individual lift racks go past set height
            if abs(subsystems._lift.getBackPosition()) >= robotmap.lift_height:
                subsystems._lift.setBack(0.0)
            if abs(subsystems._lift.getFrontPosition()) >= robotmap.lift_height:
                subsystems._lift.setFront(0.0)
        elif self.target_position is Position.BOTH_DOWN:
            # Check if individual lift racks activate limit switch and stop them
            if not subsystems._lift.getFrontLimit():
                subsystems._lift.stopFront()
            if not subsystems._lift.getBackLimit():
                subsystems._lift.stopBack()

    def isFinished(self):
        if self.target_position is Position.BOTH_UP:
            return (
                abs(subsystems._lift.getBackPosition()) >= robotmap.lift_height
                and abs(subsystems._lift.getFrontPosition()) >= robotmap.lift_height
            )
        elif self.target_position is Position.BOTH_DOWN:
            # return (
            #     not subsystems._lift.getFrontLimit()
            #     and not subsystems._lift.getBackLimit()
            # )
            return False
        # elif self.target_position is Position.FRONT_UP:
        #     return abs(subsystems._lift.getFrontPosition()) >= robotmap.lift_height
        # elif self.target_position is Position.BACK_UP:
        #     return abs(subsystems._lift.getBackPosition()) >= robotmap.lift_height
        elif self.target_position is Position.FRONT_DOWN:
            return not subsystems._lift.getFrontLimit()
        elif self.target_position is Position.BACK_DOWN:
            return not subsystems._lift.getBackLimit()
        # elif self.target_position is Position.BOTH_HALT:
        #     return True

    def interrupted(self):
        self.end()

    def end(self):
        if self.target_position is Position.BOTH_UP:
            subsystems._lift.resetEncoders()
        elif self.target_position is Position.BOTH_DOWN:
            subsystems._lift.resetEncoders()
        elif self.target_position is Position.BACK_DOWN:
            pass
        elif self.target_position is Position.FRONT_DOWN:
            pass
        # elif self.target_position is Position.BACK_UP:
        #     subsystems._lift.resetBackEncoder()
        # elif self.target_position is Position.FRONT_UP:
        #     subsystems._lift.resetFrontEncoder()
        # subsystems._lift.setPosition(Position.BOTH_HALT)
