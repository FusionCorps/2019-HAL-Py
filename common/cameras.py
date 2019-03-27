# noinspection PyUnresolvedReferences
from cscore import CameraServer, HttpCamera, MjpegServer, UsbCamera


def init():
    cam_server = CameraServer()
    cam_server.startAutomaticCapture()
