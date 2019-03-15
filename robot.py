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

        self.logger = logging.getLogger("Core")

        oi.init()
        subsystems.init()
        commands.init()
        dashboard.update()

        self.logger.info("Robot initialized")
        self.watchdog.setTimeout(1)

        from commands.update_sd import UpdateSD

        self.update_smartdashboard = UpdateSD()

    def robotPeriodic(self):
        pass

    def autonomousInit(self):
        self.update_smartdashboard.start()

        subsystems._lift.talon_drive_CFront.setQuadraturePosition(10000, 0)
        subsystems._lift.talon_drive_CBack.setQuadraturePosition(0, 0)

    def autonomousPeriodic(self):
        super().autonomousPeriodic()

    def teleopInit(self):
        pass

    def teleopPeriodic(self):
        super().teleopPeriodic()
        subsystems._chassis._drive.feedWatchdog()

    def disabledInit(self):
        pass


if __name__ == "__main__":
    wpilib.run(Hal)
