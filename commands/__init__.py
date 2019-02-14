import logging

import oi

from .intake.eject import IntakeEject
from .intake.halt import IntakeHalt
from .intake.intake import IntakeIntake
from .intake.shoot import IntakeShoot
from .joystick_drive import JoystickDrive
from .pneumatics.extend import Extend
from .pneumatics.halt import Halt
from .pneumatics.retract import Retract


def init():
    """Adds all commands to controller"""
    logger = logging.getLogger("Commands")

    oi.X.whenPressed(Extend())
    oi.B.whenPressed(Retract())
    oi.A.whenPressed(Halt())

    logger.info("Commands initialized")
