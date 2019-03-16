import logging

import wpilib
from commandbased import CommandBasedRobot
from ctre import ControlMode
from networktables import NetworkTablesInstance
from wpilib import Timer, Watchdog

import subsystems


class Hal(CommandBasedRobot):
    def robotInit(self):
        import subsystems
        import oi
        import commands
        import dashboard

        import common.cameras

        self.timer = Timer()
        self.logger = logging.getLogger("Core")

        oi.init()
        subsystems.init()
        commands.init()
        dashboard.update()
        common.cameras.init()

        self.logger.info("Robot initialized")
        self.watchdog.setTimeout(2)

        subsystems._chassis.resetEncoders()

    def robotPeriodic(self):
        pass

    def autonomousInit(self):
        pass

    def autonomousPeriodic(self):
        super().autonomousPeriodic()
        subsystems._chassis._drive.feedWatchdog()

    def teleopInit(self):
        from commands.update_sd import UpdateSD

        self.update_smartdashboard = UpdateSD()
        self.update_smartdashboard.start()
        subsystems._chassis.resetEncoders()

    def teleopPeriodic(self):
        import oi

        super().teleopPeriodic()
        subsystems._chassis._drive.feedWatchdog()

    def disabledInit(self):
        pass


if __name__ == "__main__":
    wpilib.run(Hal)
