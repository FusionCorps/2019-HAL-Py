import logging

from wpilib.command import Command

import robotmap
import subsystems
from subsystems.lift import Position


class LiftSet(Command):
    def __init__(self, target_position):
        self.target_position = target_position
        self.logger = logging.getLogger("LiftSet")
        super().__init__(self.__class__.__name__ + " " + str(target_position))
        self.requires(subsystems._lift)

    def initialize(self):
        subsystems._lift.set_position(self.target_position)

    def execute(self):
        if self.target_position is Position.BOTH_UP:
            pass
        elif (
                self.target_position is Position.BOTH_DOWN
                or self.target_position is Position.FRONT_DOWN
                or self.target_position is Position.BACK_DOWN
        ):
            # if subsystems._lift.get_front_position() > robotmap.lift_height - 500:
            #     self.logger.info("Front done")
            # if subsystems._lift.get_back_position() > robotmap.lift_height - 500:
            #     self.logger.info("Back done")
            if (
                    not subsystems._lift.get_front_limit()
                    and subsystems._lift.get_front_position() is not robotmap.lift_height
            ):
                subsystems._lift.stop_front()
            if (
                    not subsystems._lift.get_back_limit()
                    and subsystems._lift.get_back_position() is not robotmap.lift_height
            ):
                subsystems._lift.stop_back()

    def isFinished(self):
        # LiftSet is not supposed to finish because of backsliding from Position.BOTH_DOWN
        if self.target_position is Position.BOTH_UP:
            # return (
            #     abs(subsystems._lift.getFrontPosition()) <= 30
            #     and abs(subsystems._lift.getBackPosition()) <= 30
            # )
            return False
        elif self.target_position is Position.BOTH_DOWN:
            # return (
            #     not subsystems._lift.getFrontLimit()
            #     and not subsystems._lift.getBackLimit()
            # )
            # return subsystems._lift.get_front_position() > robotmap.lift_height - 500 \
            #        and subsystems._lift.get_back_position() > robotmap.lift_height - 500
            return False
        elif self.target_position is Position.FRONT_DOWN:
            # return not subsystems._lift.getFrontLimit()
            return False
        elif self.target_position is Position.BACK_DOWN:
            # return not subsystems._lift.getBackLimit()
            return False

    def interrupted(self):
        self.logger.warning(
            "The Target Position ["
            + self.target_position.name
            + " -> "
            + subsystems._lift.get_current_position().name
            + "] was Interrupted"
        )
        self.end()

    def end(self):
        self.logger.info("The Target Position [ " + self.target_position.name + " -> "
                         + subsystems._lift.get_current_position().name + " ] has been reached")

        if self.target_position is Position.BOTH_UP or self.target_position is Position.BOTH_DOWN:
            subsystems._lift.stop_front()
            subsystems._lift.stop_back()
        elif self.target_position is Position.FRONT_DOWN:
            subsystems._lift.stop_front()
        elif self.target_position is Position.BACK_DOWN:
            subsystems._lift.stop_back()
