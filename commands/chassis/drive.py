from wpilib.command import Command

import subsystems


class DriveChassis(Command):
    def __init__(self, target_distance):
        super().__init__("DriveChassis")
        self.requires(subsystems._chassis)
        self.target_distance = target_distance

    def initialize(self):
        subsystems._chassis.resetEncoders()
