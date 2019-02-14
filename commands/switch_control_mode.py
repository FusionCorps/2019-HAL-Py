import logging

from wpilib.command import InstantCommand

import robotmap


class SwitchControlMode(InstantCommand):
    def __init__(self, target_control_mode):
        super().__init__("SwitchControlMode")
        self.target_control_mode = target_control_mode
        self.logger = logging.getLogger("Control Mode")

    def execute(self):
        robotmap.control_mode = self.target_control_mode
        self.logger.warning("Now " + str(robotmap.control_mode))
