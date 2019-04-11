from wpilib.command import Command

import subsystems


class ChassisStop(Command):
    def __init__(self):
        super().__init__("ChassisStop")
        self.requires(subsystems.chassis)

    def initialize(self):
        subsystems.chassis.drive.stopMotor()

    def execute(self):
        subsystems.chassis.drive.feed()

    def isFinished(self):
        return any(bool(spd > 0.0) for spd in subsystems.chassis.get_talon_spds())

    def interrupted(self):
        self.end()

    def end(self):
        pass
