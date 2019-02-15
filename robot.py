import logging

import wpilib
from commandbased import CommandBasedRobot
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
        dashboard.init()

        self.logger.info("Robot initialized")
        self.watchdog.setTimeout(1)

        from commands.update_sd import UpdateSD

        self.update_smartdashboard = UpdateSD()

    def autonomousInit(self):
        self.update_smartdashboard.start()
        from commands.autonomous.auton_profile import Auton_Profile

        self.auton_profile = Auton_Profile("example")
        self.auton_profile.start()
        self.scheduler.run()

    def autonomousPeriodic(self):
        self.update_smartdashboard.start()
        self.scheduler.run()

    def teleopInit(self):
        self.update_smartdashboard.start()
        self.scheduler.run()

    def teleopPeriodic(self):
        self.update_smartdashboard.start()
        self.scheduler.run()


if __name__ == "__main__":
    wpilib.run(Hal)
