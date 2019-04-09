import logging

from wpilib import Timer
from wpilib.command import Command

import robotmap
import subsystems
from subsystems.sublift import Position


class LiftSet(Command):
    """Sets the position of the lift using CTRE's MotionMagic system"""

    def __init__(self, target_position: Position, can_finish=True):
        super().__init__(f"{self.__class__.__name__} {str(target_position.name)}")
        self.requires(subsystems.lift)
        self.target_position = target_position
        self.can_finish = can_finish
        self.logger = logging.getLogger("LiftSet")
        self.timer = Timer()

    def __str__(self):
        return (f"[ {self.target_position.name} -> {subsystems.lift.get_current_position().name} ] "
                f"(F: {str(subsystems.lift.get_front_position()):>6}, "
                f"B: {str(subsystems.lift.get_back_position()):>6})")

    def initialize(self):
        if self.target_position == Position.CLIMB or self.target_position == Position.CLIMB2:
            subsystems.lift.set_front_fpid(robotmap.lift_front_fpid)
            subsystems.lift.set_back_fpid(robotmap.lift_back_fpid)
            subsystems.lift.set_both_characteristics(robotmap.lift_characteristics)
        elif self.target_position == Position.LBACK or self.target_position == Position.LBACK2:
            subsystems.lift.set_front_fpid(robotmap.lift_front_retract_fpid)
            subsystems.lift.set_front_characteristics(robotmap.lift_characteristics_retract)
            subsystems.lift.set_back_characteristics(robotmap.lift_characteristics)
        elif self.target_position == Position.FRONT or self.target_position == Position.FRONT2:
            subsystems.lift.set_back_fpid(robotmap.lift_back_retract_fpid)
            subsystems.lift.set_front_characteristics(robotmap.lift_characteristics)
            subsystems.lift.set_back_characteristics(robotmap.lift_characteristics_retract)
        elif self.target_position == Position.FLUSH:
            subsystems.lift.set_front_fpid(robotmap.lift_front_retract_fpid)
            subsystems.lift.set_back_fpid(robotmap.lift_back_retract_fpid)
            subsystems.lift.set_both_characteristics(robotmap.lift_characteristics_retract)
        subsystems.lift.set_position(self.target_position)
        self.timer.reset()
        self.timer.start()

    def execute(self):
        if self.target_position == Position.CLIMB or self.target_position == Position.CLIMB2:
            if not subsystems.lift.get_front_limit():
                subsystems.lift.stop_front()
            if not subsystems.lift.get_back_limit():
                subsystems.lift.stop_back()
        elif self.target_position == Position.FRONT or self.target_position == Position.FRONT2:
            if not subsystems.lift.get_front_limit():
                subsystems.lift.stop_front()
            if abs(subsystems.lift.get_back_position()) <= 1000:
                subsystems.lift.stop_back()
        elif (self.target_position == Position.LBACK) or (self.target_position == Position.LBACK2):
            if not subsystems.lift.get_back_limit():
                subsystems.lift.stop_back()
            if abs(subsystems.lift.get_front_position()) <= 1000:
                subsystems.lift.stop_front()

    def isFinished(self):
        if self.can_finish is False:
            return False
        elif self.can_finish is True:
            if self.target_position == Position.FLUSH:
                return (abs(subsystems.lift.get_front_position()) <= 1000) and (
                        abs(subsystems.lift.get_back_position()) <= 1000)
            elif self.target_position == Position.CLIMB:
                return not subsystems.lift.get_front_limit() and not subsystems.lift.get_back_limit()
            elif self.target_position == Position.FRONT:
                return not subsystems.lift.get_front_limit() and (
                        abs(subsystems.lift.get_back_position()) <= 1000)
            elif self.target_position == Position.LBACK:
                return not subsystems.lift.get_back_limit() and (
                        abs(subsystems.lift.get_front_position()) <= 1000)
            elif self.target_position == Position.CLIMB2:
                return abs(subsystems.lift.get_front_position()) > robotmap.lift_height_2 and abs(
                    subsystems.lift.get_back_position()) > robotmap.lift_height_2
            elif self.target_position == Position.FRONT2:
                return abs(subsystems.lift.get_back_position()) <= 1000 and abs(
                    subsystems.lift.get_front_position()) > robotmap.lift_height_2
            elif self.target_position == Position.LBACK2:
                return abs(subsystems.lift.get_front_position()) <= 1000 and abs(
                    subsystems.lift.get_back_position()) > robotmap.lift_height_2

    def interrupted(self):
        self.logger.warning(f"{str(self)} Interrupted")
        self.end()

    def end(self):
        if self.target_position is Position.CLIMB:
            subsystems.lift.stop_front()
            subsystems.lift.stop_back()
        elif self.target_position is Position.CLIMB2:
            subsystems.lift.stop_back()
            subsystems.lift.stop_front()
        elif self.target_position is Position.LBACK2:
            subsystems.lift.stop_back()
        elif self.target_position is Position.FRONT2:
            subsystems.lift.stop_front()

        self.timer.stop()
        self.logger.warning(f"{str(self)} Reached in {str(round(self.timer.get(), 2))}")
