from wpilib.command import Command

import robotmap
import subsystems
from inputs import controller


class IntakeJoystick(Command):
    def __init__(self):
        super().__init__(self.__class__.__name__)
        self.requires(subsystems.intake)

    def initialize(self):
        pass

    def execute(self):
        subsystems.intake.set_victor(
            (controller.get_l_trigger() * robotmap.spd_intake) - (
                    controller.get_r_trigger() * robotmap.spd_intake))

    def isFinished(self):
        return False

    def interrupted(self):
        self.end()

    def end(self):
        subsystems.intake.set_victor(0.0)
