import sys

from commandbased import CommandBasedRobot
from wpilib import run

from common.decorate_logging import DecorateLogging


class Hal(CommandBasedRobot):
    @DecorateLogging((0, "Core", "warning", "ROBOT STARTING"),
                     (1, "Core", "warning", f"ROBOT INITIALIZED on a {sys.platform} system"))
    def robotInit(self):
        import hal
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

        commands.init()
        dashboard.init()

    def robotPeriodic(self):
        pass

    def autonomousInit(self):
        from commands.chassis.encoders_reset import EncodersReset
        EncodersReset().start()

    def autonomousPeriodic(self):
        super().autonomousPeriodic()

    def teleopInit(self):
        from commands.chassis.encoders_reset import EncodersReset
        EncodersReset().start()

    def teleopPeriodic(self):
        super().teleopPeriodic()


if __name__ == "__main__":
    run(Hal)
