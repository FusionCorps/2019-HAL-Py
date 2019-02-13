from wpilib.command import InstantCommand

import subsystems


class IntakeHalt(InstantCommand):
    def __init__(self):
        super().__init__("IntakeHalt")
        self.requires(subsystems._intake)

    def execute(self):
        if subsystems._intake.getSetpoint() == 0.0:
            pass
        else:
            subsystems._intake.setSetpoint(0.0)
