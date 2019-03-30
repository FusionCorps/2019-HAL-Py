# noinspection PyUnresolvedReferences
from cscore import CameraServer, HttpCamera, MjpegServer, UsbCamera


def init():
    # limelight_http = HttpCamera("limelight_http", "http://10.66.72.11:5800")
    # cam_server = CameraServer().addCamera(limelight_http)
    cam_server = CameraServer()
    cam_server.startAutomaticCapture(dev=0)
