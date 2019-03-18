# noinspection PyUnresolvedReferences
from cscore import CameraServer, HttpCamera, MjpegServer, UsbCamera


def init():
    cam_server1 = CameraServer()
    # cam_limelight_server = MjpegServer(
    #     name="limelight_mjpeg", listenAddress="limelight.local", port=5800
    # )
    # cam_limelight = HttpCamera(name="limelight_cscore", url="http://limelight.local")

    # cam_server1.addServer(name="", port=5800, server=cam_limelight_server)
    # cam_server1.addCamera(camera=cam_limelight)
    cam_server1.startAutomaticCapture()
