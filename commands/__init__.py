import logging

import oi

from .joystick_drive import JoystickDrive


def init():
    """Adds all commands to controller"""
    logger = logging.getLogger("Commands")
    logger.info("Commands initialized")
