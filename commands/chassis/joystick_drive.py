from wpilib.command import Command

import robotmap
import subsystems
from inputs import controller


class JoystickDrive(Command):
    def __init__(self):
        super().__init__("Joystick_Drive")
        self.requires(subsystems.chassis)

    def initialize(self):
        pass

    def execute(self):
        if robotmap.chassis_drive_mode is 'Curvature':
            subsystems.chassis.drive.curvatureDrive(controller.get_x(), controller.get_y(), multiply_by=True)
        elif robotmap.chassis_drive_mode is 'Logistic':
            subsystems.chassis.drive.logistic_drive(controller.get_x(), controller.get_y(), multiply_by=True)
        else:
            raise ValueError("Cannot drive using joystick control!")

    def interrupted(self):
        self.end()

    def isFinished(self):
        pass

    def end(self):
        pass
