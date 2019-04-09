import logging

import hal
import wpilib
from commandbased import CommandBasedRobot

import subsystems


class Hal(CommandBasedRobot):
    def robotInit(self):
        import subsystems
        import commands
        from common import dashboard

        if not hal.isSimulation():
            # noinspection PyUnresolvedReferences
            from cscore import CameraServer, HttpCamera, MjpegServer, UsbCamera

            limelight_http = HttpCamera("limelight_http", "http://10.66.72.11:5800")
            cs = CameraServer.getInstance()
            cs.enableLogging()
            usb_0 = cs.startAutomaticCapture(dev=0)
            usb_1 = cs.startAutomaticCapture(dev=1)
            limelight_http = cs.startAutomaticCapture(camera=limelight_http)

        self.logger = logging.getLogger("Core")

        subsystems.init()
        commands.init()
        dashboard.init()

        self.logger.info("Robot initialized")

        subsystems.chassis.gyro.calibrate()
        subsystems.chassis.reset_encoders()
        self.watchdog.setTimeout(1)

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


if __name__ == "__main__":
    wpilib.run(Hal)
