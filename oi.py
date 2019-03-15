import logging

from wpilib import Joystick
from wpilib.buttons import JoystickButton, Trigger

import robotmap

logger, joystick, A, B, X, Y, bumper_L, bumper_R, trigger_L, trigger_R, back, start, stick_L, stick_R = (
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
)


def init():
    """Creates joystick and buttons"""
    global logger, joystick, A, B, X, Y, bumper_L, bumper_R, back, start, stick_L, stick_R

    logger = logging.getLogger("Outside Input")
    joystick = Joystick(robotmap.joystick)
    A = JoystickButton(joystick, 1)
    B = JoystickButton(joystick, 2)
    X = JoystickButton(joystick, 3)
    Y = JoystickButton(joystick, 4)
    bumper_L = JoystickButton(joystick, 5)
    bumper_R = JoystickButton(joystick, 6)
    back = JoystickButton(joystick, 7)
    start = JoystickButton(joystick, 8)
    stick_L = JoystickButton(joystick, 9)
    stick_R = JoystickButton(joystick, 10)
    logger.info("OI initialized")
