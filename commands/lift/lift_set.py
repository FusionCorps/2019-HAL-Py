import logging

from wpilib.command import Command
from math import pow
import robotmap
import subsystems
from subsystems.lift import Position

from wpilib import Timer


class LiftSet(Command):
    def __init__(self, target_position):
        self.target_position = target_position
        self.logger = logging.getLogger("LiftSet")
        super().__init__(self.__class__.__name__ + " " + str(target_position))
        self.requires(subsystems._lift)

        self.has_lift_correction_started = False
        self.timer = Timer()

    @staticmethod
    def get_correction_setpoint(time):
        if time > 1:
            return robotmap.lift_height * pow((1 / time), 2)
        elif time < -1:
            return robotmap.lift_height * pow((1 / time), 2)
        else:
            return robotmap.lift_height

    def initialize(self):
        subsystems._lift.set_position(self.target_position)
        self.timer.reset()

    def execute(self):
        lift_offset = subsystems._lift.get_front_position() - subsystems._lift.get_back_position()
        output_F = subsystems._lift.talon_drive_CFront.get()
        output_B = subsystems._lift.talon_drive_CBack.get()

        if lift_offset <= -1000 and not self.has_lift_correction_started and not (output_B <= 0 or output_F <= 0):
            self.logger.info("Lift is unbalanced, correcting...")
            self.timer.start()
            self.has_lift_correction_started = True
        elif lift_offset >= 1000 and not self.has_lift_correction_started and not (output_B <= 0 or output_F <= 0):
            self.logger.info("Lift is unbalanced, correcting...")
            self.timer.start()
            self.has_lift_correction_started = True

        time_temp = self.timer.get()

        if self.has_lift_correction_started and subsystems._lift.get_back_position() > self.get_correction_setpoint(time_temp):
            pass
        elif lift_offset <= -1000 and self.has_lift_correction_started:
            self.logger.info("New back setpoint at " + str(self.get_correction_setpoint(self.timer.get())))
            if subsystems._lift.get_back_position() > self.get_correction_setpoint(time_temp):
                subsystems._lift.set_back(self.get_correction_setpoint(time_temp))
        elif lift_offset > -750 and lift_offset < 750 and self.has_lift_correction_started:
            self.logger.info("Lift balanced, stopping alignment")
            self.timer.stop()
            self.timer.reset()
            subsystems._lift.set_position(self.target_position)
            self.has_lift_correction_started = False
        elif lift_offset >= 1000 and self.has_lift_correction_started:
            self.logger.info("New front setpoint at " + str(self.get_correction_setpoint(self.timer.get())))
            if subsystems._lift.get_front_position() > self.get_correction_setpoint(time_temp):
                subsystems._lift.set_front(self.get_correction_setpoint(time_temp))

        if self.target_position is Position.BOTH_UP:
            pass
        if self.target_position is Position.BOTH_DOWN:
            pass
        elif (
                self.target_position is Position.BOTH_DOWN
                or self.target_position is Position.FRONT_DOWN
                or self.target_position is Position.BACK_DOWN
        ):
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
