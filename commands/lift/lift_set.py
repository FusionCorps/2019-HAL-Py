import logging

from wpilib.command import Command

import robotmap
import subsystems
from subsystems.sublift import Position


class LiftSet(Command):
    """Sets the position of the lift using CTRE's MotionMagic system"""
    def __init__(self, target_position, can_finish=True):
        self.target_position = target_position
        self.logger = logging.getLogger("LiftSet")
        super().__init__(self.__class__.__name__ + " " + str(target_position))
        self.requires(subsystems.lift)

        self.can_finish = can_finish
        self.can_correct = False
        self.is_correcting = False
        # self.timer = Timer()

    def __str__(self):
        return ("[ "
                + self.target_position.name
                + " -> "
                + subsystems.lift.get_current_position().name
                + " ]"
                + f' (F: {str(subsystems.lift.get_front_position()):>6}'
                + f', B: {str(subsystems.lift.get_back_position()):>6}'
                + ")")

    def initialize(self):
        if self.target_position is Position.CLIMB:
            subsystems.lift.set_front_fpid(robotmap.lift_front_fpid)
            subsystems.lift.set_back_fpid(robotmap.lift_back_fpid)
        elif self.target_position is Position.LBACK:
            subsystems.lift.set_front_fpid(robotmap.lift_front_retract_fpid)
        elif self.target_position is Position.FRONT:
            subsystems.lift.set_back_fpid(robotmap.lift_back_retract_fpid)
        elif self.target_position is Position.FLUSH:
            subsystems.lift.set_front_fpid(robotmap.lift_front_retract_fpid)
            subsystems.lift.set_back_fpid(robotmap.lift_back_retract_fpid)
        subsystems.lift.set_position(self.target_position)
        # self.timer.reset()

    def execute(self):
        if self.target_position is Position.CLIMB:
            if not subsystems.lift.get_front_limit():
                subsystems.lift.stop_front()
            if not subsystems.lift.get_back_limit():
                subsystems.lift.stop_back()
        elif self.target_position is Position.FRONT:
            if not subsystems.lift.get_front_limit():
                subsystems.lift.stop_front()
            if abs(subsystems.lift.get_back_position()) <= 1000:
                subsystems.lift.stop_back()
        elif self.target_position is Position.LBACK:
            if not subsystems.lift.get_back_limit():
                subsystems.lift.stop_back()
            if abs(subsystems.lift.get_front_position()) <= 1000:
                subsystems.lift.stop_front()

    def isFinished(self):
        if self.can_finish is False:
            return False
        elif self.can_finish is True:
            if self.target_position is Position.FLUSH:
                return (abs(subsystems.lift.get_front_position()) <= 1000) and (
                        abs(subsystems.lift.get_back_position()) <= 1000)
            elif self.target_position is Position.CLIMB:
                return not subsystems.lift.get_front_limit() and not subsystems.lift.get_back_limit()
            elif self.target_position is Position.FRONT:
                return not subsystems.lift.get_front_limit() and (
                        abs(subsystems.lift.get_back_position()) <= 1000)
            elif self.target_position is Position.LBACK:
                return not subsystems.lift.get_back_limit() and (
                        abs(subsystems.lift.get_front_position()) <= 1000)

    def interrupted(self):
        self.logger.warning(
            str(self) + " Interrupted"
        )
        self.end()

    def end(self):
        if self.target_position is Position.CLIMB:
            subsystems.lift.stop_front()
            subsystems.lift.stop_back()

        subsystems.lift.set_front_fpid(robotmap.lift_front_fpid)
        subsystems.lift.set_back_fpid(robotmap.lift_back_fpid)
        self.logger.warning(str(self) + " Reached")
