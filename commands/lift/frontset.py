from wpilib.command import Command

import robotmap
import subsystems


class FrontSet(Command):
    def __init__(self, target):
        super().__init__("BackSet")
        self.target = target
        self.requires(subsystems._lift)
        self.target_height = robotmap.lift_height

    def initialize(self):
        subsystems._lift.resetEncoders()
        if robotmap.control_mode == 0:
            subsystems._lift.talon_drive_CFront.set(self.target)
        else:
            pass

    def execute(self):
        if robotmap.control_mode == 0:
            if (
                subsystems._lift.talon_drive_CFront.getQuadraturePosition()
                > self.target_height
            ):
                subsystems._lift.talon_drive_CFront.set(0.0)
            else:
                pass
        else:
            self.end()

    def isFinished(self):
        return (
            subsystems._lift.talon_drive_CFront.getQuadraturePosition()
            > self.target_height
        )

    def interrupted(self):
        self.end()

    def end(self):
        subsystems._lift.resetEncoders()
