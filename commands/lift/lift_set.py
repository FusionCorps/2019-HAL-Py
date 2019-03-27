import logging
from math import pow

from wpilib import Timer
from wpilib.command import Command

import robotmap
import subsystems
from subsystems.sublift import Position


class LiftSet(Command):
    def __init__(self, target_position):
        self.target_position = target_position
        self.logger = logging.getLogger("LiftSet")
        super().__init__(self.__class__.__name__ + " " + str(target_position))
        self.requires(subsystems.lift)

        self.can_correct = False
        self.is_correcting = False
        self.timer = Timer()

    @staticmethod
    def get_back_correction(time, decay_rate=0.1):
        """Returns the encoder tick amount (from a decay function) that needs to be added to the current lift height"""
        # return (robotmap.lift_height - subsystems._lift.get_back_position()) * pow(1 - decay_rate, time)
        return (robotmap.lift_height) * pow(1 - decay_rate, time)

    @staticmethod
    def get_front_correction(time, decay_rate=0.1):
        """Returns the encoder tick amount (from a decay function) that needs to be added to the current lift height"""
        # return (robotmap.lift_height - subsystems._lift.get_front_position()) * pow(1 - decay_rate, time)
        return (robotmap.lift_height) * pow(1 - decay_rate, time)

    def initialize(self):
        subsystems.lift.set_position(self.target_position)
        self.timer.reset()

    def execute(self):
        if self.can_correct:
            # Lift offset correction code
            lift_offset = subsystems.lift.get_front_position() - subsystems.lift.get_back_position()

            output_F = subsystems.lift.talon_drive_CFront.get()
            output_B = subsystems.lift.talon_drive_CBack.get()

            time_temp = self.timer.get()

            if lift_offset <= -4096 and not self.is_correcting:
                self.logger.info("Lift is unbalanced, correcting...")
                self.timer.start()
                self.is_correcting = True
            elif lift_offset >= 4096 and not self.is_correcting:
                self.logger.info("Lift is unbalanced, correcting...")
                self.timer.start()
                self.is_correcting = True

            # front_correction_setpoint = self.get_front_correction(time_temp) + subsystems._lift.get_front_position()
            front_correction_setpoint = self.get_front_correction(time_temp)
            # back_correction_setpoint = self.get_back_correction(time_temp) + subsystems._lift.get_back_position()
            back_correction_setpoint = self.get_back_correction(time_temp)

            if lift_offset <= -4096 and self.is_correcting and not subsystems.lift.get_front_position() >= \
                                                                   robotmap.lift_height:
                self.logger.info(back_correction_setpoint)

                if subsystems.lift.get_back_position() >= robotmap.lift_height:
                    subsystems.lift.set_back(robotmap.lift_height)
                elif back_correction_setpoint > subsystems.lift.get_back_position():
                    subsystems.lift.set_back(back_correction_setpoint)

            elif lift_offset > -2048 and lift_offset < 2048 and self.is_correcting:
                self.logger.info("Lift balanced, stopping alignment")
                self.timer.stop()
                self.timer.reset()
                subsystems.lift.set_position(self.target_position)
                self.is_correcting = False

            elif lift_offset >= 4096 and self.is_correcting:
                self.logger.info(front_correction_setpoint)

                if subsystems.lift.get_front_position() >= robotmap.lift_height:
                    subsystems.lift.set_front(robotmap.lift_height)
                elif front_correction_setpoint > subsystems.lift.get_front_position():
                    subsystems.lift.set_front(front_correction_setpoint)

        # Special Execution Conditions for each Position
        # if self.target_position is Position.BOTH_UP:
        #     pass
        # if self.target_position is Position.BOTH_DOWN:
        #     pass
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
        if self.target_position is Position.BOTH_UP:
            return False
        elif self.target_position is Position.BOTH_DOWN:
            return False
        elif self.target_position is Position.FRONT_DOWN:
            return False
        elif self.target_position is Position.BACK_DOWN:
            return False

    def interrupted(self):
        self.logger.warning(
            "The Target Position ["
            + self.target_position.name
            + " -> "
            + subsystems.lift.get_current_position().name
            + "] was Interrupted"
        )
        self.end()

    def end(self):
        self.logger.info("The Target Position [ " + self.target_position.name + " -> "
                         + subsystems.lift.get_current_position().name + " ] has been reached")

        if self.target_position is Position.BOTH_UP or self.target_position is Position.BOTH_DOWN:
            subsystems.lift.stop_front()
            subsystems.lift.stop_back()
        elif self.target_position is Position.FRONT_DOWN:
            subsystems.lift.stop_front()
        elif self.target_position is Position.BACK_DOWN:
            subsystems.lift.stop_back()
