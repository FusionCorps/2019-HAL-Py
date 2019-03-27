from wpilib.command import Command

import oi
import robotmap
import subsystems


class IntakeJoystick(Command):
    def __init__(self):
        super().__init__(self.__class__.__name__)
        self.requires(subsystems.intake)

    def initialize(self):
        pass

    def execute(self):
        subsystems.intake.setVictor(oi.joystick.getRawAxis(2) * robotmap.spd_intake)

    def isFinished(self):
        return False

    def interrupted(self):
        self.end()

    def end(self):
        subsystems.intake.setVictor(0.0)
