import commands
import logging

import wpilib
from commandbased import CommandBasedRobot
from wpilib.command import Scheduler

import oi
import subsystems


class Hal(CommandBasedRobot):

    def robotInit(self):
        self.logger = logging.getLogger("Core")
        oi.init()
        subsystems.init()
        commands.init()
        self.logger.info("Robot initialized")

    def robotPeriodic(self):
        Scheduler().getInstance().run()


if __name__ == '__main__':
    wpilib.run(Hal)
