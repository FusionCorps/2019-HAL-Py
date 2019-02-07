import logging

import wpilib
from commandbased import CommandBasedRobot
from wpilib.command import Scheduler


class Hal(CommandBasedRobot):

    def robotInit(self):
        import subsystems, oi, commands, dashboard
        self.logger = logging.getLogger("Core")

        oi.init()
        subsystems.init()
        commands.init()
        dashboard.init()

        self.logger.info('Robot initialized')


if __name__ == '__main__':
    wpilib.run(Hal)
