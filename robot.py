import logging

import wpilib
from commandbased import CommandBasedRobot

import subsystems


class Hal(CommandBasedRobot):
    def robotInit(self):
        import subsystems
        import oi
        import commands
        import dashboard
        import common.cameras

        self.logger = logging.getLogger("Core")

        oi.init()
        subsystems.init()
        commands.init()
        dashboard.init()
        common.cameras.init()

        self.logger.info("Robot initialized")
        self.watchdog.setTimeout(2)

        subsystems.chassis.reset_encoders()

        from commands.update_sd import UpdateSD

        self.update_smartdashboard = UpdateSD()
        self.update_smartdashboard.start()

    def robotPeriodic(self):
        pass

    def autonomousInit(self):
        subsystems.chassis.reset_encoders()

    def autonomousPeriodic(self):
        super().autonomousPeriodic()
        subsystems.chassis.drive.feedWatchdog()

    def teleopInit(self):
        subsystems.chassis.reset_encoders()

    def teleopPeriodic(self):
        super().teleopPeriodic()
        subsystems.chassis.drive.feedWatchdog()
        # self.logger.info("Front " + str(subsystems.lift.get_front_position()) + " Back " + str(
        #     subsystems.lift.get_back_position()))


if __name__ == "__main__":
    wpilib.run(Hal)
