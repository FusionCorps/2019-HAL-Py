# noinspection PyUnresolvedReferences
from cscore import CameraServer, HttpCamera, MjpegServer, UsbCamera


def init():
    limelight_http = HttpCamera("limelight_http", "http://10.66.72.11:5800")
    # # cam_server = CameraServer().addCamera(limelight_http)
    # cam_server = CameraServer()
    # cam_server.addCamera(limelight_http).startAutomaticCapture(dev=0)
    # # cam_server.startAutomaticCapture(dev=0)
    # # cam_server.startAutomaticCapture()
    cs = CameraServer.getInstance()
    cs.enableLogging()
    usb_0 = cs.startAutomaticCapture(dev=0)
    usb_1 = cs.startAutomaticCapture(dev=1)
    limelight_http = cs.startAutomaticCapture(camera=limelight_http)

    cs.waitForever()
