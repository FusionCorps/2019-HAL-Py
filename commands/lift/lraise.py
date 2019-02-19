from wpilib.command import Command

import robotmap
import subsystems


class SetLift(Command):
    def __init__(self, target):
        super().__init__("Lift Raise " + str(target))
        self.requires(subsystems._lift)
        self.target = target
        self.targetHeight = robotmap.lift_height

    def initialize(self):
        if robotmap.control_mode == 1:
            pass
        elif robotmap.control_mode == 0:
            # subsystems._lift.resetEncoders()
            subsystems._lift.talon_drive_CBack.set(self.target * 2)
            subsystems._lift.talon_drive_CFront.set(self.target * 0.5)

    def execute(self):
        if robotmap.control_mode == 0:
            # if (
            #     subsystems._lift.talon_drive_CBack.getQuadraturePosition()
            #     > self.targetHeight
            # ):
            #     subsystems._lift.talon_drive_CBack.set(0.0)
            # if (
            #     subsystems._lift.talon_drive_CFront.getQuadraturePosition()
            #     > self.targetHeight
            # ):
            #     subsystems._lift.talon_drive_CFront.set(0.0)
            pass
        else:
            self.end()

    def isFinished(self):
        # return (
        #     subsystems._lift.talon_drive_CBack.getQuadraturePosition() > self.targetHeight
        #     and subsystems._lift.talon_drive_CFront.getQuadraturePosition() > self.targetHeight
        # )
        pass

    def interrupted(self):
        self.end()

    def end(self):
        pass
