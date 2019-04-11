from wpilib.command import InstantCommand

import subsystems


class EncodersReset(InstantCommand):
    def __init__(self):
        super().__init__("ResetEncoder")

    def initialize(self):
        subsystems.chassis.reset_encoders()
