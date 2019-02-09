from ctre import ControlMode
from wpilib.command import InstantCommand

import oi
import robotmap
import subsystems


class JoystickDrive(InstantCommand):
    def __init__(self):
        super().__init__("Joystick_Drive")
        self.requires(subsystems._chassis)

    def initialize(self):
        for talon in subsystems._chassis._talons:
            talon.set(ControlMode.PercentOutput)

    def execute(self):
        subsystems._chassis._drive.curvatureDrive(
            -(oi.joystick.getRawAxis(1)) * robotmap.spd_chassis_drive,
            oi.joystick.getRawAxis(4) * robotmap.spd_chassis_rotate,
            True,
        )
