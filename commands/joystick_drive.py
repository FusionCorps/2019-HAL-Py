from wpilib.command import InstantCommand

import subsystems


class JoystickDrive(InstantCommand):
    def __init__(self):
        super().__init__("Joystick_Drive")
        self.requires(subsystems.chassis)

    def execute(self):
        subsystems.chassis.joystick_drive()

    def interrupted(self):
        self.end()
