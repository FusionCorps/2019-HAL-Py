from wpilib.command import InstantCommand

import robotmap
import subsystems


class IntakeIntake(InstantCommand):
    def __init__(self):
        super().__init__("IntakeIntake")
        self.requires(subsystems._intake)

    def execute(self):
        if subsystems._intake.getSetpoint() == robotmap.spd_intake:
            pass
        else:
            subsystems._intake.setSetpoint(robotmap.spd_intake)
