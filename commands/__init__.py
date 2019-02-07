import logging

import oi

from .joystick_drive import Joystick_Drive


def init():
    logger = logging.getLogger("Commands")
    logger.info("Commands initialized")
