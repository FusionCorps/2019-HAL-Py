from wpilib.command import InstantCommand

import oi
import robotmap
import subsystems


class JoystickDrive(InstantCommand):
    def __init__(self):
        super().__init__("Joystick_Drive")
        self.requires(subsystems.chassis)

    def execute(self):
        subsystems.chassis.drive.curvatureDrive(-robotmap.spd_chassis_drive * oi.joystick.getRawAxis(1),
                                                robotmap.spd_chassis_rotate * oi.joystick.getRawAxis(4), True)

    def interrupted(self):
        self.end()
