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
            if robotmap.chassis_drive_mode is 'logistic':
                robotmap.chassis_drive_mode = 'curvature'
            elif robotmap.chassis_drive_mode is 'curvature':
                robotmap.chassis_drive_mode = 'logistic'
        elif self.mode is not None:
            robotmap.chassis_drive_mode = self.mode
        self.logger.warning(f"Mode is now {str(robotmap.chassis_drive_mode)}")

    def end(self):
        pass
