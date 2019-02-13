import logging

import wpilib
from commandbased import CommandBasedRobot


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

    def autonomousInit(self):
        from commands.autonomous.auton_profile import Auton_Profile

        self.auton = Auton_Profile("example")
        self.scheduler.add(self.auton)

    def teleopPeriodic(self):
        self.scheduler.run()


if __name__ == "__main__":
    wpilib.run(Hal)
