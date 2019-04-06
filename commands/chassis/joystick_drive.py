from wpilib.command import Command

import oi
import robotmap
import subsystems


class JoystickDrive(Command):
    def __init__(self):
        super().__init__("Joystick_Drive")
        self.requires(subsystems.chassis)

    def initialize(self):
        pass

    def execute(self):
        if robotmap.chassis_drive_mode is 'curvature':
            subsystems.chassis.drive.curvatureDrive(-robotmap.spd_chassis_drive * oi.joystick.getRawAxis(1),
                                                    robotmap.spd_chassis_rotate * oi.joystick.getRawAxis(4), True)
        elif robotmap.chassis_drive_mode is 'logistic':
            subsystems.chassis.drive.logistic_drive(-robotmap.spd_chassis_drive * oi.joystick.getRawAxis(1),
                                                    robotmap.spd_chassis_rotate * oi.joystick.getRawAxis(4))
        else:
            raise ValueError("Cannot drive using joystick control!")

    def interrupted(self):
        self.end()

    def isFinished(self):
        pass

    def end(self):
        pass
