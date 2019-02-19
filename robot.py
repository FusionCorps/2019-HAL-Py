import logging

import wpilib
from commandbased import CommandBasedRobot
from networktables import NetworkTablesInstance
from wpilib import Watchdog

import subsystems


class Hal(CommandBasedRobot):
    def robotInit(self):
        import subsystems
        import oi
        import commands
        import dashboard

        # import common.cameras

        self.logger = logging.getLogger("Core")

        oi.init()
        subsystems.init()
        commands.init()
        dashboard.update()
        # common.cameras.init()

        self.logger.info("Robot initialized")
        self.watchdog.setTimeout(1)

        from commands.update_sd import UpdateSD

        self.update_smartdashboard = UpdateSD()

    def autonomousInit(self):
        self.update_smartdashboard.start()
        from commands.pneumatics.close import PneumaticsClose

        PneumaticsClose().start()
        self.scheduler.run()

    def autonomousPeriodic(self):
        self.update_smartdashboard.start()
        self.scheduler.run()

    def teleopInit(self):
        self.update_smartdashboard.start()
        self.scheduler.run()

    def teleopPeriodic(self):
        subsystems._chassis._drive.feedWatchdog()
        self.update_smartdashboard.start()
        self.scheduler.run()

    def disabledInit(self):
        self.scheduler.removeAll()


if __name__ == "__main__":
    wpilib.run(Hal)
