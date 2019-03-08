import robotmap
import subsystems
from common.fusion_command import FusionCommand
from subsystems.lift import Position


class LiftSet(FusionCommand):
    def __init__(self, target_position):
        super().__init__(self.__class__.__name__, 0, sub=subsystems._lift)
        self.target_position = target_position

    def initialize(self):
        subsystems._lift.setPosition(self.target_position)

    def execute(self):
        if self.target_position is Position.BOTH_UP:
            if subsystems._lift.talon_drive_CBack.getQuadraturePosition() >= abs(
                robotmap.lift_height
            ) and subsystems._lift.talon_drive_CFront.getQuadraturePosition() >= abs(
                robotmap.lift_height
            ):
                self.end()
            if subsystems._lift.talon_drive_CBack.getQuadraturePosition() >= abs(
                robotmap.lift_height
            ):
                subsystems._lift.talon_drive_CBack.set(0.0)
            if subsystems._lift.talon_drive_CFront.getQuadraturePosition() >= abs(
                robotmap.lift_height
            ):
                subsystems._lift.talon_drive_CFront.set(0.0)
        elif self.target_position is Position.BOTH_DOWN:
            if (
                subsystems._lift.CFront_limit.get()
                and subsystems._lift.CBack_limit.get()
            ):
                subsystems._lift.resetFrontEncoder()
                subsystems._lift.resetBackEncoder()
                self.end()
            if subsystems._lift.CFront_limit.get():
                subsystems._lift.talon_drive_CFront.set(0.0)
                subsystems._lift.resetFrontEncoder()
            if subsystems._lift.CBack_limit.get():
                subsystems._lift.talon_drive_CBack.set(0.0)
                subsystems._lift.resetBackEncoder()
        elif self.target_position is Position.FRONT_UP:
            if subsystems._lift.talon_drive_CFront.getQuadraturePosition() >= abs(
                robotmap.lift_height
            ):
                self.end()
        elif self.target_position is Position.BOTH_HALT:
            self.end()

    def isFinished(self):
        return False

    def interrupted(self):
        self.end()

    def end(self):
        subsystems._lift.setPosition(Position.BOTH_HALT)
