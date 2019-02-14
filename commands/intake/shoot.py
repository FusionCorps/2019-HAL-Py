from wpilib.command import InstantCommand

import robotmap
import subsystems


class IntakeShoot(InstantCommand):
    def __init__(self):
        super().__init__("IntakeShoot")
        self.requires(subsystems._intake)

    def initialize(self):
        if subsystems._intake.getPIDController().isEnabled():
            pass
        else:
            subsystems._intake.enable()

    def execute(self):
        if subsystems._intake.getSetpoint() == robotmap.spd_intake_shoot:
            pass
        else:
            subsystems._intake.setSetpoint(robotmap.spd_intake_shoot)
