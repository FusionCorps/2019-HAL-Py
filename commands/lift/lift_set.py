import logging

from wpilib import Timer
from wpilib.command import Command

import robotmap
import subsystems
from subsystems.sublift import Position


class LiftSet(Command):
    def __init__(self, target_position, can_finish=True):
        self.target_position = target_position
        self.logger = logging.getLogger("LiftSet")
        super().__init__(self.__class__.__name__ + " " + str(target_position))
        self.requires(subsystems.lift)

        self.can_finish = can_finish
        self.can_correct = False
        self.is_correcting = False
        self.timer = Timer()

    def __str__(self):
        return "[ " \
               + self.target_position.name \
               + " -> " \
               + subsystems.lift.get_current_position().name \
               + " ] (Front: " \
               + str(subsystems.lift.get_front_position()) \
               + ", Back: " \
               + str(subsystems.lift.get_back_position()) \
               + ")"

    def initialize(self):
        subsystems.lift.set_position(self.target_position)
        self.timer.reset()

    def execute(self):
        if self.can_correct:
            # Lift offset correction code
            lift_offset = subsystems.lift.get_front_position() - subsystems.lift.get_back_position()

            output_F = subsystems.lift.talon_drive_CFront.get()[0]
            output_B = subsystems.lift.talon_drive_CBack.get()[0]

            time_temp = self.timer.get()

            if lift_offset <= -4096 and not self.is_correcting:
                self.logger.info("Lift is unbalanced, correcting...")
                self.timer.start()
                self.is_correcting = True
            elif lift_offset >= 4096 and not self.is_correcting:
                self.logger.info("Lift is unbalanced, correcting...")
                self.timer.start()
                self.is_correcting = True

            if lift_offset <= -4096 and self.is_correcting and not subsystems.lift.get_front_position() >= \
                                                                   robotmap.lift_height:
                if subsystems.lift.get_back_position() >= robotmap.lift_height:
                    subsystems.lift.set_back(robotmap.lift_height)
                else:
                    subsystems.lift.set_back(output_B * 0.8)

            elif (-2048 < lift_offset < 2048) and self.is_correcting:
                self.logger.info("Lift balanced, stopping alignment")
                self.timer.stop()
                self.timer.reset()
                subsystems.lift.set_position(self.target_position)
                self.is_correcting = False

            elif lift_offset >= 4096 and self.is_correcting:
                if subsystems.lift.get_front_position() >= robotmap.lift_height:
                    subsystems.lift.set_front(robotmap.lift_height)
                else:
                    subsystems.lift.set_front(output_F * 0.8)

        if (
                self.target_position is Position.BOTH_DOWN
                or self.target_position is Position.FRONT_DOWN
                or self.target_position is Position.BACK_DOWN
        ):
            if (
                    not subsystems.lift.get_front_limit()
                    and subsystems.lift.get_front_position() is not robotmap.lift_height
            ):
                subsystems.lift.stop_front()
            if (
                    not subsystems.lift.get_back_limit()
                    and subsystems.lift.get_back_position() is not robotmap.lift_height
            ):
                subsystems.lift.stop_back()

    def isFinished(self):
        if self.can_finish is False:
            return False
        elif self.can_finish is True:
            if self.target_position is Position.BOTH_UP:
                return (abs(subsystems.lift.get_front_position() <= 1000) and abs(
                    subsystems.lift.get_back_position() <= 1000))
            elif self.target_position is Position.BOTH_DOWN:
                return not subsystems.lift.get_back_limit() and not subsystems.lift.get_back_limit()
            elif self.target_position is Position.FRONT_DOWN:
                return not subsystems.lift.get_front_limit() and (
                        abs(subsystems.lift.get_back_position()) <= 1000)
            elif self.target_position is Position.BACK_DOWN:
                return not subsystems.lift.get_back_limit() and (
                        abs(subsystems.lift.get_front_position()) <= 1000)

    def interrupted(self):
        self.logger.warning(
            "The Target Position " + str(self) + " was Interrupted"
        )
        self.end()

    def end(self):
        self.logger.warning("The Target Position " + str(self) + " has been reached")
