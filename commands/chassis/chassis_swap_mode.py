import logging

from wpilib.command import InstantCommand

import robotmap


class ChassisSwapMode(InstantCommand):
    def __init__(self, mode=None):
        super().__init__("ChassisSetMode")
        self.mode = mode
        self.logger = logging.getLogger("ChassisSetMode")

    def initialize(self):
        if self.mode is None:
            if robotmap.chassis_drive_mode is 'Logistic':
                robotmap.chassis_drive_mode = 'Curvature'
            elif robotmap.chassis_drive_mode is 'Curvature':
                robotmap.chassis_drive_mode = 'Logistic'
        elif self.mode is not None:
            robotmap.chassis_drive_mode = self.mode
        self.logger.warning(f"{str(robotmap.chassis_drive_mode)}")
