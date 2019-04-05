from wpilib.command import InstantCommand

import oi
import subsystems


class JoystickDrive(InstantCommand):
    def __init__(self):
        super().__init__("Joystick_Drive")
        self.requires(subsystems.chassis)

    def execute(self):
        subsystems.chassis.drive.curvatureDrive(oi.joystick.getRawAxis(1), -oi.joystick.getRawAxis(4), True)

    def interrupted(self):
        self.end()
