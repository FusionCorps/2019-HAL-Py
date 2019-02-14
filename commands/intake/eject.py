from wpilib.command import Command

import robotmap
import subsystems


class IntakeEject(Command):
    def __init__(self):
        super().__init__("IntakeEject")
        self.requires(subsystems._intake)

    def initialize(self):
        if robotmap.control_mode == 1:
            if subsystems._intake.getPIDController().isEnabled():
                pass
            else:
                subsystems._intake.enable()
        else:
            pass

    def execute(self):
        if robotmap.control_mode == 1:
            if subsystems._intake.getSetpoint() == -robotmap.spd_intake:
                pass
            else:
                subsystems._intake.setSetpoint(-robotmap.spd_intake)
        else:
            pass

    def isFinished(self):
        return True

    def interrupted(self):
        self.end()

    def end(self):
        subsystems._intake.disable()
