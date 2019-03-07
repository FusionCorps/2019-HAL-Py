from ctre import ControlMode
from wpilib.command import InstantCommand

import oi
import robotmap
import subsystems


class JoystickDrive(InstantCommand):
    def __init__(self):
        super().__init__("Joystick_Drive")
        self.requires(subsystems._chassis)

    def execute(self):
        subsystems._chassis.joystickDrive()
