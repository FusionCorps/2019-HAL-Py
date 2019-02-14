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

        # import dashboard

        self.logger = logging.getLogger("Core")

        oi.init()
        subsystems.init()
        commands.init()
        # dashboard.init()

        self.logger.info("Robot initialized")
        self.watchdog.setTimeout(1)

    def autonomousInit(self):
        self.scheduler.run()

    def autonomousPeriodic(self):
        self.scheduler.run()

    def teleopInit(self):
        self.scheduler.run()

    def teleopPeriodic(self):
        self.scheduler.run()
        print(
            str(subsystems._pneumatics.solenoid_L.get())
            + str(subsystems._pneumatics.solenoid_R.get())
        )


if __name__ == "__main__":
    wpilib.run(Hal)
