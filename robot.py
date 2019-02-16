import logging

import wpilib
from commandbased import CommandBasedRobot
from wpilib import Watchdog

import subsystems
from cscore import CameraServer, UsbCamera


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
        CameraServer().getInstance().addServer(
            name="Front", port=5800, server="10.66.72.11"
        )
        cam_back = UsbCamera(0)
        CameraServer().getInstance().addCamera(cam_back)
        CameraServer().startAutomaticCapture()

    def autonomousInit(self):
        self.update_smartdashboard.start()
        # from commands.autonomous.auton_profile import Auton_Profile

        # self.auton_profile = Auton_Profile("example")
        # self.auton_profile.start()
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


if __name__ == "__main__":
    wpilib.run(Hal)
