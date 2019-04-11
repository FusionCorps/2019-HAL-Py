import logging

from commandbased import CommandBasedRobot
from wpilib import run


class Hal(CommandBasedRobot):
    def robotInit(self):
        import hal
        import commands
        from common import dashboard

        self.logger = logging.getLogger("Core")

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

        self.logger.info("Robot initialized")

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
