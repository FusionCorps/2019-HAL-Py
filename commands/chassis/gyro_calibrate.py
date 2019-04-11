from wpilib.command import InstantCommand

import subsystems


class GyroCalibrate(InstantCommand):
    def __init__(self):
        super().__init__("CalibrateGyro")

    def initialize(self):
        subsystems.chassis.reset_gyro()
