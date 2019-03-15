import logging

import wpilib
from commandbased import CommandBasedRobot
from ctre import ControlMode
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
        self.watchdog.setTimeout(2)

        # from commands.update_sd import UpdateSD

        # self.update_smartdashboard = UpdateSD()

    def robotPeriodic(self):
        pass

    def autonomousInit(self):
        # self.update_smartdashboard.start()
        pass

    def autonomousPeriodic(self):
        super().autonomousPeriodic()
        subsystems._chassis._drive.feedWatchdog()

    def teleopInit(self):
        import dashboard

        dashboard.update()

    def teleopPeriodic(self):
        super().teleopPeriodic()
        subsystems._chassis._drive.feedWatchdog()

    def disabledInit(self):
        pass


if __name__ == "__main__":
    wpilib.run(Hal)
