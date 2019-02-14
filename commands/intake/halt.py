import logging

from wpilib.command import InstantCommand

import subsystems


class IntakeHalt(InstantCommand):
    def __init__(self):
        super().__init__("IntakeHalt")
        self.requires(subsystems._intake)

    def initialize(self):
        if subsystems._intake.getPIDController().isEnabled():
            pass
        else:
            subsystems._intake.enable()

    def execute(self):
        logging.getLogger("Intake Halt").info("Executing")
        if subsystems._intake.getSetpoint() == 0.0:
            pass
        else:
            subsystems._intake.setSetpoint(0.0)
