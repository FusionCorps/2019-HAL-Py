import logging

from wpilib.command import InstantCommand

import robotmap


class SwitchControlMode(InstantCommand):
    def __init__(self):
        super().__init__("SwitchControlMode")

        self.logger = logging.getLogger("Control Mode")

    def execute(self):
        if robotmap.control_mode == 1:
            robotmap.control_mode = 0
        elif robotmap.control_mode == 0:
            robotmap.control_mode = 1
        self.logger.warning("Now " + str(robotmap.control_mode))
