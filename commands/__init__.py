import logging

import oi

from .intake.eject import IntakeEject
from .intake.halt import IntakeHalt
from .intake.intake import IntakeIntake
from .intake.shoot import IntakeShoot
from .joystick_drive import JoystickDrive


def init():
    """Adds all commands to controller"""
    logger = logging.getLogger("Commands")

    oi.B.whileHeld(IntakeIntake())
    oi.X.whileHeld(IntakeEject())
    oi.Y.whileHeld(IntakeShoot())

    logger.info("Commands initialized")
