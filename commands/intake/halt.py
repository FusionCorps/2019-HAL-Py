from wpilib.command import Command

import robotmap
import subsystems


class IntakeHalt(Command):
    def __init__(self):
        super().__init__("IntakeHalt")
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
            if subsystems._intake.getSetpoint() == 0.0:
                pass
            else:
                subsystems._intake.setSetpoint(0.0)

    def isFinished(self):
        return True

    def interrupted(self):
        self.end()

    def end(self):
        subsystems._intake.disable()
