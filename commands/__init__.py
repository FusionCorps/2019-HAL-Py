import logging

import oi

from .intake.halt import Halt
from .intake.reverse import Reverse
from .intake.run import Run
from .intake.shoot import Shoot
from .joystick_drive import JoystickDrive


def init():
    """Adds all commands to controller"""
    logger = logging.getLogger("Commands")

    oi.A.whenPressed(Halt())
    oi.B.whenPressed(Run())
    oi.X.whenPressed(Reverse())
    oi.Y.whenPressed(Shoot())

    logger.info("Commands initialized")
