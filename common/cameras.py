from cscore import CameraServer, MjpegServer, UsbCamera


def init():
    # CameraServer().getInstance().startAutomaticCapture(0)
    cam_server1 = CameraServer()
    cam_back = UsbCamera(name="Back", dev=0)
    cam_server1.startAutomaticCapture(camera=cam_back)
